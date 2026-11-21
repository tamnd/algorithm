---
tag: DG54BX
kind: algorithm
slug: separable-paraboloidal-surrogates
name: Separable paraboloidal surrogates
aliases:
- SPS
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: Minimize penalized likelihood for transmission or emission tomography by minimizing at each step a separable quadratic surrogate that majorizes the cost.
model: real-ram
complexity:
  vars: {n: "the side of the n x n image", a: "the number of projection angles", d: "the number of detector bins", K: "the number of iterations"}
  time: {per_iteration: "O(a d n)", total: "O(K a d n)"}
  space: {extra: "O(a d + n^2)"}
properties: {deterministic: true, iterative: true, in_place: false, recursive: false, monotone_objective: true, keeps_nonnegativity: true, parallel_over_pixels: true}
history:
  year: 1999
  people: [Hakan Erdogan, Jeffrey A. Fessler]
  note: Erdogan and Fessler built separable quadratic surrogates with an optimal curvature for transmission tomography, and Fessler and Erdogan applied them to emission data.
prereqs: [emission-tomography-model, mlem-reconstruction, convex-function]
see_also: [one-step-late-algorithm, osem, expectation-maximization, coordinate-descent, projected-gradient-descent, kkt-conditions, markov-random-field, beer-lambert-law]
sources:
  - paper: doi:10.1109/42.802758
    title: H. Erdogan and J. A. Fessler, Monotonic algorithms for transmission tomography, IEEE Transactions on Medical Imaging 18(9), 1999
    locator: pp. 801 to 814 (paraboloidal surrogates for the transmission log-likelihood, the optimal curvature, and the separable SPS update)
  - paper: doi:10.1088/0031-9155/44/11/311
    title: H. Erdogan and J. A. Fessler, Ordered subsets algorithms for transmission tomography, Physics in Medicine and Biology 44(11), 1999
    locator: pp. 2835 to 2851 (ordered subsets with precomputed curvatures)
  - paper: doi:10.1109/nssmic.1998.774361
    title: J. A. Fessler and H. Erdogan, A paraboloidal surrogates algorithm for convergent penalized-likelihood emission image reconstruction, IEEE Nuclear Science Symposium Conference Record, vol. 2, 1998
    locator: pp. 1132 to 1135 (paraboloidal surrogates for emission data with a background)
  - paper: doi:10.1109/42.370409
    title: A. R. De Pierro, A modified expectation maximization algorithm for penalized likelihood estimation in emission tomography, IEEE Transactions on Medical Imaging 14(1), 1995
    locator: pp. 132 to 137 (the convexity split that makes a surrogate separable)
---

Separable paraboloidal surrogates (SPS) is a monotone method for penalized likelihood reconstruction. For the [emission tomography model](/emission-tomography-model/) it minimizes $\Phi(x) = \sum_i h_i([A x]_i) + \beta R(x)$ over $x \ge 0$, where $h_i(l) = (l + b_i) - y_i \log(l + b_i)$ is the negative Poisson log-likelihood of bin $i$ and $R$ is a convex penalty. Each iteration does two things. First, it replaces each $h_i$ by a parabola that touches it at the current line sum and lies above it for all nonnegative line sums. Second, it splits the sum of parabolas and the penalty into a sum of one-pixel quadratics with De Pierro's convexity trick. The minimizer of the result is a clipped Newton step for each pixel, all in parallel. The cost never increases, the image stays nonnegative, and any $\beta \ge 0$ works. This is the difference from the [one-step-late algorithm](/one-step-late-algorithm/), which can fail for a large $\beta$. Erdogan and Fessler introduced the method for transmission tomography in 1999.

## In plain words

The cost of an image measures how badly it explains the counts, plus a charge for roughness. It is hard to minimize directly, because each count depends on many pixels at once.

SPS builds, at each step, a simpler cost that is never below the true one and is equal to it at the current image. The simpler cost is a sum of terms with one pixel each, and each term is a parabola, so its lowest point has a formula. If the lowest point is negative, the pixel is set to 0. Moving to the lowest point of the simpler cost cannot raise the true cost, because the simpler cost is above the true cost everywhere and equal at the start.

The method is safe for any strength of the smoothing. The price is speed: each step is cautious, so it can need more steps than MLEM.

## The problem

Given counts $y_i \ge 0$, a matrix $A$ with $a_{ij} \ge 0$ and row sums $a_i = \sum_j a_{ij} > 0$, a background $b_i > 0$ for every bin with $y_i > 0$, a weight $\beta \ge 0$, and the quadratic neighbor penalty
$$R(x) = \tfrac12 \sum_{\{j,k\} \in E} w_{jk} (x_j - x_k)^2, \qquad w_{jk} \ge 0,$$
minimize $\Phi(x) = \sum_i h_i([A x]_i) + \beta R(x)$ over $x \ge 0$. This is the negative of the penalized log-likelihood of the [one-step-late](/one-step-late-algorithm/) page, up to a constant. $\Phi$ is a [convex function](/convex-function/), so its minimizers are the points that satisfy the [KKT conditions](/kkt-conditions/) for $x \ge 0$. The background must be positive where there are counts: if $b_i = 0$ and $y_i > 0$, then $h_i(0) = +\infty$, and no finite parabola lies above $h_i$ on $[0, \infty)$.

The surrogate has two parts. For the data, at the current line sum $l_i = [A x]_i$, take the parabola
$$q_i(t) = h_i(l_i) + h_i'(l_i)(t - l_i) + \tfrac{c_i}{2}(t - l_i)^2, \qquad c_i = \frac{2\,[h_i(0) - h_i(l_i) + h_i'(l_i)\, l_i]}{l_i^2} \ (l_i > 0), \quad c_i = \frac{y_i}{b_i^2} \ (l_i = 0).$$
This optimal curvature makes $q_i(0) = h_i(0)$, and it is the smallest curvature for which $q_i \ge h_i$ on $[0, \infty)$. Then De Pierro's split writes $[A z]_i = \sum_j (a_{ij}/a_i)\big(a_i(z_j - x_j) + l_i\big)$, a convex combination, so the convexity of $q_i$ gives a sum of one-pixel terms that lies above $q_i([A z]_i)$. The same trick on the penalty gives one-pixel terms of curvature $2 \sum_k w_{jk}$ for pixel $j$.

## The algorithm

```pseudo id=main
SPS(A, y, b, β, w, x0, K)                 ▷ x0 ≥ 0; b_i > 0 where y_i > 0
L1  a_i ← Σ_j a_ij for each ray i
L2  p_j ← 2 Σ_k w_jk for each pixel j     ▷ the penalty curvature
L3  x ← x0
L4  for k ← 1 to K do
L5      l ← A x                           ▷ the line sums
L6      h'_i ← 1 - y_i / (l_i + b_i)      ▷ the slopes of the data terms
L7      c_i ← the optimal curvature of h_i at l_i
L8      d ← A^T (a ⊙ c)                   ▷ d_j = Σ_i a_ij a_i c_i
L9      g ← A^T h'                        ▷ the gradient of the data part
L10     x_j ← max(0, x_j - (g_j + β ∂R/∂x_j(x)) / (d_j + β p_j)) for each pixel j
L11 return x
```

One iteration has one forward projection (L5) and two back projections (L8 and L9). The curvatures $c_i$ cost $O(1)$ each. Line L10 updates all pixels at once, from the same old image, so it is parallel over the pixels. If a pixel has $d_j + \beta p_j = 0$, only rays with $y_i = 0$ see it and it has no penalty neighbor; then the cost is linear in $x_j$ and increasing, and the code sets $x_j = 0$.

## Example

Take the $2 \times 2$ image of the [MLEM](/mlem-reconstruction/) page, with 5 rays: the two rows, the two columns and one diagonal (pixels 1 and 4), and $a_{ij} \in \{0, 1\}$, so $a_i = 2$. The counts are $y = (3, 7, 4, 6, 5)$ and the background is $b_i = 0.5$. These data are consistent: $A x + b = y$ at $x^* = (0.75, 1.75, 2.75, 3.75)$, so $x^*$ is the minimizer for $\beta = 0$. Start from $x = (1, 1, 1, 1)$.

Every line sum is $l_i = 2$. The slopes are $h_i'(2) = 1 - y_i/2.5 = (-0.2, -1.8, -0.6, -1.4, -1.0)$, and the optimal curvatures are $c = (1.2142, 2.8330, 1.6189, 2.4283, 2.0236)$. For pixel 1, which lies on rays 1, 3 and 5, $g_1 = -0.2 - 0.6 - 1.0 = -1.8$ and $d_1 = 2(1.2142 + 1.6189 + 2.0236) = 9.7133$, so $x_1 \leftarrow 1 + 1.8/9.7133 = 1.1853$. The first iterate is $(1.1853, 1.2196, 1.2695, 1.2883)$.

| iteration | 1 | 2 | 3 | 10 | 50 | 100 | 300 |
|---|---|---|---|---|---|---|---|
| $\Phi$ for SPS | $-12.514$ | $-13.816$ | $-14.615$ | $-16.013$ | $-16.2600$ | $-16.26013$ | $-16.26013$ |
| max error of SPS | 2.46 | 2.19 | 1.94 | 0.87 | 0.024 | 2.1e-3 | 2.4e-7 |
| max error of MLEM | 1.35 | 0.75 | 0.58 | 0.18 | 5.5e-3 | 8.5e-5 | 5.1e-12 |

$\Phi$ starts at $-10.407$ and decreases at each step to the minimum $-16.26013$. On this problem, a measurement, SPS needs about twice as many iterations as MLEM for the same error. With $\beta = 1$ and the 4 edges of the $2 \times 2$ grid, SPS converges to $(1.9701, 2.1354, 2.3045, 2.4754)$, a smoother image, again with a decreasing cost.

A larger measurement uses a $16 \times 16$ disk phantom of radius 0.6, 12 angles, 23 bins, a count scale of 50, a background of 1 per bin and Poisson noise with seed 7 (5958 counts). The image covers $[-1, 1]^2$, and pixel $(i, j)$ has its center at $x_j = -1 + (2j+1)/n$, $y_i = 1 - (2i+1)/n$. The table gives the relative error after $K$ iterations. $\Phi$ decreased at every step for every $\beta$.

| $\beta$ | $K = 10$ | $K = 50$ | $K = 100$ | $K = 300$ | OSL after 300 |
|---|---|---|---|---|---|
| 1 | 0.579 | 0.250 | 0.214 | 0.253 | 0.271 |
| 5 | 0.583 | 0.261 | 0.226 | 0.227 | 0.227 |
| 20 | 0.595 | 0.294 | 0.272 | 0.272 | fails: a denominator $\le 0$ |
| 100 | 0.649 | 0.392 | 0.366 | 0.364 | fails: a denominator $\le 0$ |

With $\beta = 0$, MLEM reaches $\Phi = -16663.9$ after 10 iterations, and SPS needs between 50 and 100 iterations for the same value.

## Correctness

Three facts give a monotone method. They are theorems, proved in [proofs/correctness.md](proofs/correctness.md).

1. **The parabola lies above the data term.** For $l \ge 0$ and the optimal curvature, $q_i(t) \ge h_i(t)$ for all $t \ge 0$. The proof uses that $h_i''(t) = y_i/(t + b_i)^2$ decreases, so $q_i - h_i$ has a convex derivative; with zeros of $q_i - h_i$ at $0$ and $l_i$ and a zero slope at $l_i$, this forces $q_i - h_i \ge 0$ on $[0, \infty)$.
2. **The split keeps it above.** The weights $a_{ij}/a_i$ form a convex combination, so Jensen's inequality for the convex $q_i$ gives the separable surrogate $S$ with $S \ge \Phi$ on $x \ge 0$ and $S = \Phi$ at the current image. The split can evaluate $q_i$ at negative arguments; that is fine, because only the convexity of $q_i$ is used there, and $q_i \ge h_i$ is needed only at $[A z]_i \ge 0$.
3. **Line L10 minimizes $S$.** $S$ is a sum of one-pixel quadratics with slope $\partial_j \Phi(x)$ and curvature $d_j + \beta p_j$ at the current image, and L10 is the clipped Newton step for each.

So $\Phi(x') \le S(x') \le S(x) = \Phi(x)$. The fixed points with positive curvatures are exactly the points that satisfy the KKT conditions, which are the minimizers since $\Phi$ is convex. The convergence of the iterates themselves is not proved on this page; it needs conditions such as a strictly convex cost.

## Complexity

In the real-RAM model, with $a$ angles of $d$ bins and an $n \times n$ image, a forward or back projection costs $O(a d n)$. One iteration costs one forward and two back projections plus $O(a d + n^2)$ for the curvatures and the penalty, so $O(a d n)$ time and $O(a d + n^2)$ extra space. $K$ iterations cost $O(K a d n)$. The number of iterations for a given accuracy has no general bound.

## Properties

- **Monotone for any $\beta$.** The cost does not increase. This is a theorem.
- **Nonnegative.** The clipping keeps $x \ge 0$, and a pixel can reach exactly 0 in one step. MLEM keeps a positive pixel positive unless every ray through it has no counts.
- **Parallel over the pixels.** All pixels update from the same old image, so the update is a vector operation, like MLEM.
- **Correct fixed points.** A fixed point satisfies the KKT conditions, so it is a minimizer.
- **Slow when the curvatures are large.** The surrogate is a safe upper bound, and its curvature $d_j$ adds up the curvatures of all the rays through the pixel. So the steps are short. In the measurements above, SPS needed more iterations than MLEM.
- **Any convex penalty with a quadratic surrogate.** The quadratic penalty is the simplest case. Edge-keeping penalties such as the Huber function have parabolas above them too, and fit in the same way.

## Variants and improvements

- **Transmission data.** The original setting of Erdogan and Fessler. For transmission scans, the mean count is $\bar y_i = B_i e^{-[A \mu]_i} + r_i$ by the [Beer-Lambert law](/beer-lambert-law/), and $h_i$ is not convex for every data value. Erdogan and Fessler showed that the optimal curvature formula, with the same form, still gives a parabola above $h_i$ on $[0, \infty)$ for this model.
- **Precomputed curvatures.** A fixed curvature, computed once from the data, avoids line L7 and the back projection of line L8 at each iteration. It is not always above $h_i$, so the method is no longer monotone in general.
- **Ordered subsets.** Using one subset of the rays per sub-iteration, with the gradient scaled by the number of subsets, gives OS-SPS. Like [OSEM](/osem/), it is fast early but has no monotone guarantee and does not converge in general. The number of subsets is a tuned design choice.
- **Coordinate descent.** The paraboloidal surrogate can be minimized one pixel at a time, with the line sums updated after each pixel, as in [coordinate descent](/coordinate-descent/). This uses less cautious steps but is harder to run in parallel.
- **De Pierro's modified EM.** De Pierro (1995) used the same separable trick on the penalty with an EM-type data surrogate. SPS uses parabolas for both parts.

## When to use it

Use SPS when you need a penalized likelihood image and a guarantee that the cost decreases, for any penalty weight. It is a good reference method to check faster methods against, for example OSL with a small $\beta$ or an ordered subsets method. When speed matters more than a guarantee, use an ordered subsets form for the first iterations and then a monotone method.

## Pitfalls

- **No background.** With $b_i = 0$ and $y_i > 0$ the data term is infinite at a zero line sum, and no parabola lies above it. Add a small positive background, or use a method for the case without background.
- **The curvature at a zero line sum.** For $l_i = 0$ the formula has a $0/0$; the right value is the limit $h_i''(0) = y_i/b_i^2$. Rounding errors near $l_i = 0$ can give a slightly negative value; clip it at 0.
- **A small background gives a huge curvature.** Then $c_i = y_i/b_i^2$ is large for rays with a small line sum, and those pixels move very slowly.
- **Clipping before the sum.** Clip each pixel after the full step. Clipping inside the sums changes the surrogate and breaks the proof.
- **Testing the wrong property.** Test that $\Phi$ does not increase. Do not test that the error to the true image decreases: with noisy data it does not, as the $\beta = 1$ row of the table shows.

## Implementations

The Python code takes the system matrix as sparse rows of (column, weight) pairs and the penalty as a list of weighted edges. It raises an error when a bin has counts and no background. The tests check that the optimal curvature gives a parabola above $h_i$ on $[0, \infty)$ and that it is the smallest such curvature, that the separable surrogate is above the cost and equal at the current image, that one step minimizes the surrogate, the first iterate of the example and its limit, that the cost does not increase on a phantom for $\beta = 0$ and $\beta = 20$, the KKT conditions at the limit with pixels at 0, the gradient against finite differences, and the adjoint test of the projector pair. It uses the shared `imgkit` helper for the phantom and the projector.

## History

De Pierro (1995) found that the convexity of the penalty lets one split it into one-pixel terms, which gave a monotone EM method for penalized likelihood in emission tomography. Erdogan and Fessler (1999) used quadratic surrogates for the transmission log-likelihood, found the optimal curvature, combined it with De Pierro's split and got the SPS method; they also gave ordered subsets forms. Fessler and Erdogan (1998) applied paraboloidal surrogates to emission data with a background.

## References
