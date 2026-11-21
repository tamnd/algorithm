---
tag: 4809JZ
kind: algorithm
slug: quasi-optimality-criterion
name: Quasi-optimality criterion
aliases:
- quasi-optimality rule
- quasi-optimality principle
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: advanced
summary: Choose the parameter on a geometric grid where the distance between successive regularized solutions is smallest, with no noise level needed.
solves: [regularization-parameter-choice]
model: real-ram
complexity:
  vars: {m: the number of measurements, n: the number of unknowns (n <= m), N: the number of grid steps}
  time: {worst: Θ(m n + N n), average: Θ(m n + N n), best: Θ(m n + N n)}
  space: {extra: Θ(N + n)}
properties: {deterministic: true, heuristic: true, needs_noise_level: false, convergent_regularization: false}
history:
  year: 1965
  people: [Andrey N. Tikhonov, Vladimir B. Glasko]
  note: Tikhonov and Glasko (1965) proposed to choose the parameter where the regularized solution changes least with the parameter. Bauer and Reiss (2008) proved optimality results for it under random noise.
prereqs: [regularization-parameter-choice, tikhonov-regularization, singular-value-decomposition]
see_also: [l-curve-method, generalized-cross-validation, lepskii-balancing-principle, morozov-discrepancy-principle, bakushinskii-veto, semi-convergence, landweber-iteration, truncated-svd]
sources:
  - paper: doi:10.1016/0041-5553(65)90150-3
    title: A. N. Tikhonov and V. B. Glasko, Use of the regularization method in non-linear problems, USSR Computational Mathematics and Mathematical Physics 5(3), 1965
    locator: pages 93 to 107
  - paper: doi:10.1088/0266-5611/24/5/055009
    title: Frank Bauer and Markus Reiss, Regularization independent of the noise level, an analysis of quasi-optimality, Inverse Problems 24(5), 2008
    locator: article 055009
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: chapter 4 (heuristic parameter choice rules and the Bakushinskii result)
---

The quasi-optimality criterion chooses the parameter of a regularization method from the data alone. Its idea: near the best parameter the regularized solution should be stable, so it should change little when the parameter changes a little. For Tikhonov regularization on a geometric grid $\alpha_j = \alpha_0q^j$ with $0 < q < 1$, the discrete rule picks the $\alpha_j$ that minimizes

$$d_j = \lVert x_{\alpha_{j+1}} - x_{\alpha_j}\rVert.$$

The continuous form minimizes $\alpha\lVert dx_\alpha/d\alpha\rVert$, which is the limit of $d_j/(1 - q)$ as $q \to 1$. Tikhonov and Glasko proposed the rule in 1965. It needs neither the noise level nor the noise variance, so it is a heuristic rule, and by the [Bakushinskii veto](/bakushinskii-veto/) it cannot be convergent for all noise. Under conditions on the noise it is: Bauer and Reiss (2008) proved oracle-type results for random noise, and Kindermann and Neubauer proved convergence for deterministic noise that satisfies a noise condition. It is simple, cheap, and works for any method with a parameter, including iteration counts.

## In plain words

You want to know how much to smooth, and you do not know how noisy the data are. Compute the result for a sequence of knob settings, each a fixed factor smaller than the last. With too much smoothing, each step brings in new real detail, so the result changes a lot. With too little, each step brings in more noise, so the result also changes a lot. In between, the result hardly moves. The rule picks the setting where two neighbouring results are closest to each other. It needs no noise estimate, it is easy to code, and like every rule of this kind it can be fooled.

## The problem

The model is $y = Ax^\dagger + e$ with an $m \times n$ matrix $A$ and unknown noise $e$. The Tikhonov solution for $\alpha > 0$ is $x_\alpha = (A^TA + \alpha I)^{-1}A^Ty$. The page [Tikhonov regularization](/tikhonov-regularization/) writes $\lambda$ for this $\alpha$. With the thin SVD $A = \sum_{i \le r} s_iu_iv_i^T$ and $b_i = \langle u_i, y\rangle$,

$$x_\alpha = \sum_i \frac{s_ib_i}{s_i^2 + \alpha}v_i, \qquad d_j^2 = \sum_i s_i^2b_i^2\Big(\frac{1}{s_i^2 + \alpha_{j+1}} - \frac{1}{s_i^2 + \alpha_j}\Big)^2.$$

Given $\alpha_0$, $q$ and $N$, the task is to find the index $j \in \{0, \dots, N - 1\}$ with the smallest $d_j$ and return $x_{\alpha_j}$. By default $\alpha_0 = s_1^2$, $q = 1/2$, and $N$ is the first index with $\alpha_N \le s_r^2$.

## The algorithm

```pseudo id=main
QUASI-OPTIMALITY(U, s, V, y, alpha_0, q, N)   ▷ thin SVD of A, s descending, r positive values
L1  b_i ← <u_i, y> for i ≤ r
L2  alpha_j ← alpha_0 q^j for j = 0, ..., N
L3  d_j ← sqrt(Σ_i (s_i b_i (1/(s_i² + alpha_{j+1}) - 1/(s_i² + alpha_j)))²) for j = 0, ..., N - 1
L4  j* ← the index of the smallest d_j
L5  return alpha_{j*}, x = Σ_i s_i b_i / (s_i² + alpha_{j*}) · v_i, j*, and the list d
```

Line L1 projects the data on the left singular vectors. Line L2 builds the grid. Line L3 computes the distance between neighbouring solutions in the coordinates of the $v_i$, where it is a sum over $r$ terms, so no solution vector is formed. Line L4 picks the smallest distance, and line L5 returns the solution at the larger of the two parameters of that pair, $\alpha_{j^\ast}$.

## Example

Take the same problem as on the GCV page: $A = \mathrm{diag}(s_1, \dots, s_{32})$ with $s_i = 1/i^2$, so $U = V = I$, the true solution $x^\dagger_i = 1/i^2$, and $e_i = 10^{-3}g_i$ with $g_i$ from `random.Random(0).gauss(0, 1)`. The defaults give $\alpha_0 = s_1^2 = 1$, $q = 1/2$ and $N = 20$, since $\alpha_{20} = 2^{-20} = s_{32}^2$.

| $j$ | $\alpha_j$ | $d_j$ | $\lVert x_{\alpha_j} - x^\dagger\rVert$ |
|---|---|---|---|
| 0 | 1 | 0.167317 | 0.5697 |
| 4 | 0.0625 | 0.051397 | 0.1882 |
| 7 | $7.81 \times 10^{-3}$ | 0.023777 | 0.0902 |
| 8 | $3.91 \times 10^{-3}$ | 0.018896 | 0.0725 |
| 9 | $1.95 \times 10^{-3}$ | 0.017480 | 0.0615 |
| 10 | $9.77 \times 10^{-4}$ | 0.022928 | 0.0583 |
| 11 | $4.88 \times 10^{-4}$ | 0.036868 | 0.0672 |
| 12 | $2.44 \times 10^{-4}$ | 0.061400 | 0.0946 |
| 14 | $6.10 \times 10^{-5}$ | 0.160611 | 0.2430 |
| 19 | $1.91 \times 10^{-6}$ | 0.564121 | 1.8197 |

The distances fall while the steps add signal and rise once they add noise. Line L4 picks $j^\ast = 9$, so the rule returns $\alpha = 2^{-9} = 0.001953$ with error $0.06146$. The best $\alpha$ on a fine grid gives $0.05817$, so the rule loses 6 percent. Its neighbour $j = 10$ has the smallest error on this grid, and the error curve is flat there. The noise level was not used at any point.

## Correctness

The proof is in `proofs/correctness.md`. It shows that line L3 computes $\lVert x_{\alpha_{j+1}} - x_{\alpha_j}\rVert$, that the derivative is $dx_\alpha/d\alpha = -(A^TA + \alpha I)^{-1}x_\alpha$, so that $d_j/(1 - q) \to \alpha_j\lVert dx_\alpha/d\alpha\rVert$ as $q \to 1$, and that the rule returns the minimizer over the finite grid. Termination is clear: the loop of line L3 has $N$ steps.

Why the minimizer is a good parameter is a separate question. Split $x_\alpha$ into the noise-free part $\bar x_\alpha$ and the noise part. The noise-free difference $\lVert\bar x_{\alpha_{j+1}} - \bar x_{\alpha_j}\rVert$ is at most the approximation error at $\alpha_j$, and the noise difference is at most of the size of the noise propagation error at $\alpha_{j+1}$. So $d_j$ is bounded by the sum of the two errors, and a small $d_j$ is necessary for a good $\alpha_j$. The converse needs assumptions, because a small $d_j$ can occur by cancellation. Bauer and Reiss (2008) prove for white noise, under conditions on the decay of the singular values and of the coefficients of $x^\dagger$, that the quasi-optimal choice reaches the oracle error up to constant and logarithmic factors with high probability. For deterministic noise the Bakushinskii veto rules out convergence for every $e$; Kindermann and Neubauer proved convergence under a condition that excludes noise too regular to tell apart from the signal. The good result in the example is a measurement.

## Complexity

With the thin SVD given, line L1 costs $\Theta(mn)$, line L3 costs $\Theta(Nr) \subseteq O(Nn)$, and line L5 costs $\Theta(n^2) \subseteq O(mn)$. The total is $\Theta(mn + Nn)$ with $\Theta(N + n)$ extra space. With the default grid, $N = \lceil\log(s_1^2/s_r^2)/\log(1/q)\rceil$, which is $20$ in the example. The SVD itself costs $O(mn^2)$. Without an SVD the rule needs $N + 1$ regularized solutions, but they can share work: for [Landweber](/landweber-iteration/) or CG the iterates come in order anyway.

## Properties

- Heuristic: it uses only $A$ and $y$.
- Scale free: replacing $A$ and $y$ by $cA$ and $cy$, with the grid scaled by $c^2$, multiplies the chosen $\alpha$ by $c^2$ and leaves $x$ unchanged. The default grid scales this way because it starts at $s_1^2$.
- Works for any family of regularized solutions with an ordered parameter: Tikhonov, [truncated SVD](/truncated-svd/), iteration counts of Landweber or CGLS.
- The result is always one of the grid points. A ratio $q$ between $1/2$ and $0.9$ is typical; very small $q$ makes the grid coarse, very large $q$ makes $d_j$ small everywhere and sensitive to noise.

## Variants and improvements

- **Continuous form.** Minimize $\alpha\lVert dx_\alpha/d\alpha\rVert = \lVert\alpha(A^TA + \alpha I)^{-1}x_\alpha\rVert$, the limit of the discrete rule as $q \to 1$, divided by $1 - q$. The implementation includes it.
- **Iterative methods.** For Landweber or [semi-convergent](/semi-convergence/) iterations, use $\lVert x_{2k} - x_k\rVert$ or $\lVert x_{k+1} - x_k\rVert$ over $k$.
- **Truncated SVD.** The distance between neighbouring truncations is $|b_k|/s_k$, so the rule picks the smallest $|b_k|/s_k$ over $k$, a test of the Picard condition.
- **Residual-based heuristic rules.** Other heuristic rules minimize a function of the residual instead of a difference of solutions. The heuristic discrepancy rule minimizes $\lVert Ax_\alpha - y\rVert/\sqrt\alpha$, and the Hanke-Raus rule is of the same type. They share the same theory of noise conditions.
- **Restricted search.** Limit $j$ to a range where $x_{\alpha_j}$ is not dominated by rounding, for example $\alpha_j \ge s_r^2$ as in the default grid.

## When to use it

Use it when the noise level is unknown and you want a rule that is easy to apply to any regularization method, including iterations. It is often more reliable than [GCV](/generalized-cross-validation/) on small or square problems and less sensitive to the shape of the curve than the [L-curve](/l-curve-method/). If the noise level is known, prefer the [discrepancy principle](/morozov-discrepancy-principle/) or the [balancing principle](/lepskii-balancing-principle/), which have proofs without conditions on the noise.

## Pitfalls

- Local minima. The sequence $d_j$ can have several local minima, and a spurious one at small $\alpha$ when the noise happens to be small in a few components. Line L4 takes the global minimum; look at the whole sequence.
- Too small parameters. If the grid in line L2 runs far below $s_r^2$, the solutions stop changing because every filter factor is close to 1, and $d_j$ tends to zero there. The rule then picks the noisiest solution. Stop the grid at $s_r^2$.
- Returning the wrong member of the pair in line L5. The pair $(\alpha_j, \alpha_{j+1})$ has two solutions; the classical rule returns $x_{\alpha_j}$. Mixing the two conventions shifts the result by one grid step.
- Measuring the distance in the wrong norm. If the solution is regularized with a penalty $\lVert Lx\rVert$, the distance in line L3 is often measured in the same seminorm; mixing norms changes the rule.
- No noise level does not mean no assumptions. The rule fails when the noise looks like signal, for example for very smooth noise.

## Implementations

## History

Tikhonov and Glasko (1965) introduced the quasi-optimal choice of the regularization parameter, in a paper on nonlinear problems, as the parameter where the solution is least sensitive to the parameter. It became one of the standard heuristic rules in the Russian school of regularization. Bakushinskii (1984) showed that no rule of this kind can be convergent for all noise, and the question became under which noise conditions it converges. Bauer and Reiss (2008) gave an analysis for white noise, and Kindermann and Neubauer gave a convergence analysis for deterministic noise under noise conditions.

## References
