---
tag: H40E6J
kind: algorithm
slug: osem
name: Ordered subsets expectation maximization
aliases:
- OSEM
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: Speed up MLEM by applying its multiplicative update with one subset of projections at a time, cycling through the subsets.
model: real-ram
complexity:
  vars: {n: "the side of the n x n image", a: "the number of projection angles", d: "the number of detector bins", K: "the number of passes over all subsets", T: "the number of subsets"}
  time: {per_iteration: "O(a d n + T n^2)", total: "O(K (a d n + T n^2))"}
  space: {extra: "O(a d + T n^2)"}
properties: {deterministic: true, iterative: true, in_place: false, recursive: false, keeps_nonnegativity: true, monotone_likelihood: false, convergent_on_noisy_data: false, order_dependent: true}
history:
  year: 1994
  people: [H. Malcolm Hudson, Richard S. Larkin]
  note: Hudson and Larkin applied the EM update to ordered subsets of the projection data and showed a large speedup over MLEM.
prereqs: [mlem-reconstruction, emission-tomography-model]
see_also: [sart, kaczmarz-method, stochastic-gradient-descent, one-step-late-algorithm, separable-paraboloidal-surrogates, semi-convergence, richardson-lucy-deconvolution, sirt]
sources:
  - paper: doi:10.1109/42.363108
    title: H. M. Hudson and R. S. Larkin, Accelerated image reconstruction using ordered subsets of projection data, IEEE Transactions on Medical Imaging 13(4), 1994
    locator: pp. 601 to 609 (the OSEM update, subset balance, convergence with exact data, and the speedup)
  - paper: doi:10.1109/TMI.1982.4307558
    title: L. A. Shepp and Y. Vardi, Maximum likelihood reconstruction for emission tomography, IEEE Transactions on Medical Imaging 1(2), 1982
    locator: pp. 113 to 122 (the MLEM update that OSEM applies to each subset)
---

OSEM is a faster form of [MLEM](/mlem-reconstruction/) for the [emission tomography model](/emission-tomography-model/) $y_i \sim \operatorname{Poisson}((A x + b)_i)$. It splits the detector bins into $T$ subsets, usually groups of whole views, and applies the MLEM update with the bins of one subset at a time: $x_j \leftarrow (x_j / s^t_j) \sum_{i \in S_t} a_{ij} y_i / (A x + b)_i$, with $s^t_j$ the sensitivity of the subset. One pass over all subsets costs about as much as one MLEM iteration. In the early passes it raises the likelihood about as much as $T$ MLEM iterations; this is a measurement, not a theorem. The price is that OSEM does not maximize the likelihood. With noisy data its iterates do not converge to the maximum likelihood image and can cycle. Like MLEM, it keeps the image nonnegative and is stopped early in practice. It is the standard reconstruction of clinical PET and SPECT.

## In plain words

MLEM looks at all the data before it changes the image once. That is slow, because each change needs a full pass over the data. OSEM cuts the data into a few groups, for example every fourth view of the scanner. It does the MLEM step with the first group only, and changes the image at once. Then it does the step with the next group, starting from the new image, and so on.

Each group alone gives a fair picture of the object, so each small step goes in about the right direction. So one pass over all groups does about as much work as several MLEM steps, for the same cost. But no group sees all the data. Near the end, each group pulls the image to its own best answer, and the image moves in a circle among them instead of settling.

## The problem

The same as for MLEM: given counts $y$, a matrix $A$ with $a_{ij} \ge 0$ and a background $b \ge 0$, find a nonnegative image $x$ with a high Poisson log-likelihood
$$L(x) = \sum_i \big[y_i \log \bar y_i - \bar y_i\big], \qquad \bar y = A x + b.$$
OSEM also needs a partition of the bins into subsets $S_1, \ldots, S_T$. In practice the goal is not the maximizer of $L$, which is noisy, but a good image after a few passes. The subsets are *balanced* if every pixel has the same sensitivity in every subset, $s^t_j = s_j / T$.

## The algorithm

```pseudo id=main
OSEM(A, y, b, x0, S_1..S_T, K)            ▷ x0 > 0; the subsets partition the bins
L1  s^t_j ← Σ_{i ∈ S_t} a_ij for each subset t and pixel j
L2  x ← x0
L3  for k ← 1 to K do
L4      for t ← 1 to T do                  ▷ one sub-iteration per subset
L5          ȳ_i ← (A x)_i + b_i for i ∈ S_t
L6          r_i ← y_i / ȳ_i for i ∈ S_t    ▷ r_i ← 0 if y_i = 0
L7          g_j ← Σ_{i ∈ S_t} a_ij r_i for each pixel j
L8          x_j ← x_j g_j / s^t_j for each pixel j with s^t_j > 0
L9  return x
```

Lines L5 and L7 are a forward and a back projection of the views in $S_t$ only, so a sub-iteration costs about $1/T$ of an MLEM iteration. A pixel that no bin of $S_t$ sees is not changed by line L8. With $T = 1$, OSEM is MLEM.

The usual subsets are interleaved views: with $a$ angles, subset $t$ holds the angles $t, t + T, t + 2T, \ldots$. Then each subset covers the whole range of angles, and for a parallel-beam scan the subsets are close to balanced. The number of subsets is a tuned design choice: more subsets give a faster start, but each subset then holds fewer views and more noise. The order of the subsets also matters, and orders that make successive subsets far apart in angle are common. These choices are heuristics.

## Example

**Rows, then columns.** Take a $2 \times 2$ image in row-major order, the counts of the two rows $(3, 7)$ and of the two columns $(4, 6)$, no background, and the subsets $S_1 = \{\text{rows}\}$ and $S_2 = \{\text{columns}\}$. Each pixel lies on one row and one column, so $s^1_j = s^2_j = 1$ and the subsets are balanced. From $x = (1, 1, 1, 1)$:

| step | $x_0$ | $x_1$ | $x_2$ | $x_3$ |
|---|---|---|---|---|
| start | 1 | 1 | 1 | 1 |
| rows: scale row 0 by $3/2$ and row 1 by $7/2$ | 3/2 | 3/2 | 7/2 | 7/2 |
| columns: scale column 0 by $4/5$ and column 1 by $6/5$ | 6/5 | 9/5 | 14/5 | 21/5 |

The result fits all four counts after one pass, and later passes do not change it. Here OSEM is iterative proportional fitting of a table to its row and column sums. Four counts do not determine four pixels: MLEM from the same start reaches a different solution, $(1.142, 1.858, 2.858, 4.142)$, and the image that made the data could have been $(1, 2, 3, 4)$. All three fit the data.

**A cycle.** Take one pixel seen by two bins with $a_{11} = a_{21} = 1$, the counts $y = (1, 3)$ and one bin per subset. The first sub-iteration sets $x = 1$ and the second sets $x = 3$, from every positive start. So the sub-iterates are $1, 3, 1, 3, \ldots$, and every pass ends at 3. The maximum likelihood estimate is 2. The subsets are balanced; the data are inconsistent, as noisy data always are.

**A limit cycle.** Take the $2 \times 2$ image with the rows, the columns and the diagonal through $x_0$ and $x_3$, and the inconsistent counts $(3, 8, 4, 6, 5)$. The maximum likelihood image is $(43/55, 229/110, 188/55, 232/55) = (0.782, 2.082, 3.418, 4.218)$ with $L = 18.2505$. OSEM with the three subsets rows, columns and diagonal converges to a cycle. After the rows the image is $(19, 41, 69, 91)/20$, and after the columns and after the diagonal it is $(19, 41, 69, 91)/22$, with $L = 18.2259$. Neither point is the maximizer.

**The speedup, measured.** The image is $16 \times 16$ on $[-1, 1]^2$, with pixel $(i, j)$ centered at $x_j = -1 + (2j+1)/n$ and $y_i = 1 - (2i+1)/n$. The object is a disk of radius 0.6 with value 1, scanned at 12 angles in $[0, \pi)$ with 23 bins and the pixel-driven matrix of the shared helper. The counts are Poisson with mean 50 times the projections (seed 7, 5676 counts). The table compares one OSEM pass with $T$ interleaved view subsets and $T$ iterations of MLEM, from the same flat start. The error is $\|x / 50 - x^\dagger\| / \|x^\dagger\|$.

| $T$ | $L$ after one OSEM pass | $L$ after $T$ MLEM iterations | error after one OSEM pass |
|---|---|---|---|
| 1 | 14794.1 | 14794.1 | 0.637 |
| 2 | 15440.5 | 15439.9 | 0.464 |
| 3 | 15813.7 | 15810.2 | 0.365 |
| 4 | 16015.5 | 16006.8 | 0.297 |
| 6 | 16191.1 | 16170.7 | 0.250 |
| 12 | 16133.2 | 16266.5 | 0.462 |

Up to 6 subsets, one pass does a little more than $T$ MLEM iterations. With 12 subsets of one view each, it does much less: one view alone is a poor picture of the object. With $T = 6$, five passes reach $L = 16294.0$, about as much as 30 MLEM iterations, and the error has risen to $0.351$: the best MLEM error in this setup is $0.235$, after 10 iterations, so five passes are already too many. These numbers are measurements of this setup, not properties of the method.

## Correctness

Each sub-iteration is one MLEM iteration for the data of its subset. So by the MLEM theorem it keeps the image nonnegative and does not decrease the subset likelihood $L_t(x) = \sum_{i \in S_t} [y_i \log \bar y_i - \bar y_i]$. It can decrease the full likelihood $L = \sum_t L_t$, so OSEM is not a monotone method for $L$, and the tests do not check a monotone $L$. If the data are consistent, that is $A x + b = y$ for some $x \ge 0$, every such $x$ is a fixed point of every sub-iteration. Hudson and Larkin (1994) proved that with exact data and balanced subsets, OSEM converges to such a solution. With inconsistent data there is no such point, and the examples above show a cycle and a limit cycle away from the maximizer. The proofs are in [proofs/correctness.md](proofs/correctness.md).

## Complexity

In the real-RAM model, with $a$ angles of $d$ bins, an $n \times n$ image and $T$ subsets that split the views:

- Line L1 takes one pass over the nonzero entries of $A$, $O(a d n)$, and stores $T$ sensitivity images, $O(T n^2)$ space.
- In one pass, lines L5 and L7 touch every nonzero entry of $A$ twice, $O(a d n)$ in total. Line L8 runs $T$ times over the image, $O(T n^2)$.

So a pass costs $O(a d n + T n^2)$ time, which is $O(a d n)$ when $T \le a$ and $a d \ge n^2$, and $K$ passes cost $O(K (a d n + T n^2))$. The extra space is $O(a d + T n^2)$. As with MLEM, the number of passes is the regularization parameter, and every stopping rule without a known noise level is a heuristic.

## Properties

- **Nonnegative.** As in MLEM, each sub-iteration multiplies by nonnegative numbers.
- **Not monotone.** The full likelihood can decrease from one sub-iteration to the next. Each sub-iteration raises only its own subset likelihood.
- **Not convergent with noisy data.** The passes approach a limit cycle, not the maximizer. With exact data and balanced subsets, OSEM converges to a solution (Hudson and Larkin).
- **Fast at the start.** In the early passes, one pass with $T$ subsets does about the work of $T$ MLEM iterations, for $T$ up to a limit that depends on the data. This is a measurement, as in the table above.
- **Order dependent.** The result depends on the subsets and on their order, like [ART](/kaczmarz-method/) and [SART](/sart/). OSEM is to MLEM what SART is to [SIRT](/sirt/), and what [stochastic gradient descent](/stochastic-gradient-descent/) with a fixed step is to gradient descent.

## Variants and improvements

- **Relaxed and convergent forms.** RAMLA (Browne and De Pierro, 1996) updates with one block of bins at a time and a relaxation parameter that goes to 0, and it converges to the maximizer. COSEM keeps a running sum of the subset terms and also converges. Both trade some of the early speed for convergence.
- **Fewer subsets later.** Start with many subsets and reduce $T$ in later passes. Then the method ends closer to MLEM. The schedule is a heuristic.
- **Penalized forms.** The one-step-late update of [OSL](/one-step-late-algorithm/) and the [SPS](/separable-paraboloidal-surrogates/) update can both use ordered subsets. The penalized forms with ordered subsets have the same convergence problem as OSEM unless the step size goes to 0.
- **Block iterative EM.** Byrne gave rescaled block forms (RBI-EM) that converge with consistent data without the balance condition.

## When to use it

Use OSEM when you need an MLEM-like image from emission data in a few passes, as in clinical PET and SPECT. Choose the subsets as interleaved views, keep enough views in each subset that it covers the full range of angles, and fix the number of subsets and passes for a protocol, because the image depends on both. Use MLEM or a convergent method when you need the maximum likelihood image itself, for example to study the method, and use a penalized method when you want the result not to depend on where you stop.

## Pitfalls

- **Too many subsets.** A subset of one or two views gives a poor picture of the object, and the method becomes noisy and unstable. In the table above, 12 subsets of one view each did worse than 6.
- **Unbalanced subsets.** If the sensitivity of a pixel differs much between subsets, the image changes in a different way in each sub-iteration, and the cycle is larger.
- **Reading convergence into it.** After a few passes the image changes little, but this is not convergence to the maximum likelihood image. With more passes, the noise grows as in MLEM.
- **Testing a monotone likelihood.** The full likelihood is not monotone. Only the likelihood of the subset that was just used is.
- **Comparing by iterations.** Compare OSEM and MLEM by the number of projections, or by the total time, not by the number of passes or sub-iterations.

## Implementations

The Python code takes the system matrix as sparse rows of (column, weight) pairs and a list of subsets of row indices, and it works with float or `fractions.Fraction` data. A helper builds interleaved view subsets for the row order of `imgkit.parallel_beam_matrix`. The tests check the rows-then-columns example exactly, that one subset gives MLEM, the cycle of the one-pixel example, the limit cycle of the $2 \times 2$ example and its gap to the maximizer, the monotone subset likelihood of each sub-iteration on random problems, the convergence to a solution with exact data and balanced subsets, the adjoint test of the projector pair, and the measured speedup on the disk phantom.

## History

Hudson and Larkin published OSEM in 1994 in IEEE Transactions on Medical Imaging. They applied the MLEM update of Shepp and Vardi (1982) to ordered subsets of the projections, proved convergence for exact data with balanced subsets, and reported a speedup by about the number of subsets in the early iterations. The idea is the same as in the algebraic methods, where ART updates after each ray and SART after each view, instead of after all data as SIRT does. OSEM made iterative reconstruction fast enough for clinical use, and it became the standard method for PET and SPECT. Browne and De Pierro (1996) introduced the convergent row-action form RAMLA.

## References
