---
tag: WKH6V6
kind: algorithm
slug: lepskii-balancing-principle
name: Lepskii balancing principle
aliases:
- Lepskii principle
- balancing principle
- Lepskii method
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: advanced
summary: Choose the largest parameter on a grid whose solution stays within a noise-driven bound of every solution with a smaller parameter.
solves: [regularization-parameter-choice]
model: real-ram
complexity:
  vars: {m: the number of measurements, n: the number of unknowns (n <= m), N: the number of grid points}
  time: {worst: Θ(m n + N^2 n), average: Θ(m n + N^2 n), best: Θ(m n + N n)}
  space: {extra: Θ(N n)}
properties: {deterministic: true, a_posteriori: true, needs_noise_level: true, convergent_regularization: true, adaptive: true}
history:
  year: 1990
  people: [Oleg V. Lepskii, Peter Mathé, Sergei V. Pereverzev]
  note: Lepskii (1990) introduced the method for adaptive estimation in statistics. Mathé and Pereverzev (2003) and later papers turned it into the balancing principle for ill-posed problems.
prereqs: [regularization-parameter-choice, tikhonov-regularization, source-condition]
see_also: [morozov-discrepancy-principle, tikhonov-convergence-rates, qualification-of-regularization, quasi-optimality-criterion, unbiased-predictive-risk-estimator, bakushinskii-veto, semi-convergence, landweber-iteration]
sources:
  - paper: doi:10.1137/1135065
    title: O. V. Lepskii, On a problem of adaptive estimation in Gaussian white noise, Theory of Probability and Its Applications 35(3), 1990
    locator: pages 454 to 466 (the English translation is dated 1991)
  - paper: doi:10.1088/0266-5611/19/3/319
    title: Peter Mathé and Sergei V. Pereverzev, Geometry of linear ill-posed problems in variable Hilbert scales, Inverse Problems 19(3), 2003
    locator: pages 789 to 803
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: chapters 4 and 5 (order optimality and the saturation of the discrepancy principle, for comparison)
---

The balancing principle chooses the regularization parameter by comparing regularized solutions with each other. On a grid $\alpha_0 < \alpha_1 < \dots < \alpha_{N-1}$ the error of $x_{\alpha}$ splits into an approximation part $\varphi(\alpha)$ that grows with $\alpha$ and a noise part bounded by a known $\psi(\alpha)$ that falls with $\alpha$. The best $\alpha$ balances the two, but $\varphi$ depends on the unknown solution. The rule replaces it by a test that uses only computed solutions: take the largest $\alpha_j$ with

$$\lVert x_{\alpha_j} - x_{\alpha_i}\rVert \le 4\kappa\,\psi(\alpha_i) \quad\text{for all } i < j,$$

with a safety factor $\kappa \ge 1$. For Tikhonov regularization with $\lVert e\rVert \le \delta$, the bound is $\psi(\alpha) = \delta/(2\sqrt\alpha)$. The rule needs $\delta$ but no knowledge of the smoothness of $x^\dagger$, and it is proved to reach the best balance up to a constant factor. As a consequence it is order optimal for every source condition the method can exploit, without the saturation at $\nu = 1/2$ of the [discrepancy principle](/morozov-discrepancy-principle/). Lepskii introduced the idea in 1990 for adaptive estimation in statistics, and Mathé and Pereverzev brought it to inverse problems.

## In plain words

A smoothing method has a knob, and you know how big the noise is. Too little smoothing lets the noise through, and you can bound that damage exactly from the noise size. Too much smoothing blurs the answer, and you cannot measure that damage because it depends on the true answer. The trick is to compare answers with each other. Start with little smoothing and turn the knob up step by step. As long as each new answer is close to all the less smoothed ones, within what the noise alone could explain, the extra smoothing has not yet hurt. Stop at the last setting that passes this test. It is safe and adapts to the problem, but tends to smooth a bit too much.

## The problem

The model is $y^\delta = Ax^\dagger + e$ with an $m \times n$ matrix $A$, $\lVert e\rVert \le \delta$ and a known $\delta$. Here $x^\dagger$ is the minimum norm solution of $Ax = Ax^\dagger$. The Tikhonov solution for $\alpha > 0$ is $x_\alpha = (A^TA + \alpha I)^{-1}A^Ty^\delta$. The page [Tikhonov regularization](/tikhonov-regularization/) writes $\lambda$ for this $\alpha$. With the thin SVD $A = \sum_{i \le r} s_iu_iv_i^T$ and $b_i = \langle u_i, y^\delta\rangle$, $x_\alpha = \sum_i s_ib_i/(s_i^2 + \alpha)\,v_i$.

Let $\bar x_\alpha$ be the solution for exact data. Then $\lVert x_\alpha - x^\dagger\rVert \le \varphi(\alpha) + \psi(\alpha)$ with

$$\varphi(\alpha) = \lVert\bar x_\alpha - x^\dagger\rVert, \qquad \lVert x_\alpha - \bar x_\alpha\rVert \le \psi(\alpha) = \frac{\delta}{2\sqrt\alpha},$$

because $s/(s^2 + \alpha) \le 1/(2\sqrt\alpha)$ for all $s > 0$. The function $\varphi$ is nondecreasing and unknown, $\psi$ is decreasing and known. Given a grid, the task is to find an $\alpha_j$ whose error is within a constant factor of $\min_j(\varphi(\alpha_j) + \psi(\alpha_j))$.

## The algorithm

```pseudo id=main
BALANCING(U, s, V, y, delta, alpha_0 < ... < alpha_{N-1}, kappa)   ▷ thin SVD of A
L1  b_i ← <u_i, y> for i ≤ r
L2  c_j ← (s_i b_i / (s_i² + alpha_j))_i for every j          ▷ x_{alpha_j} in the basis v_i
L3  psi_j ← delta / (2 sqrt(alpha_j)) for every j
L4  for j = N - 1 down to 0
L5      for i = 0, ..., j - 1
L6          if ‖c_j - c_i‖ > 4 kappa psi_i then j fails; go to the next j
L7      if no i made j fail
L8          return alpha_j, x = Σ_k c_{j,k} v_k, j
```

Line L1 projects the data on the left singular vectors. Line L2 stores each solution by its coefficients in the basis $v_i$, where distances are plain Euclidean distances, and line L3 computes the noise bounds. Lines L4 to L8 scan from the largest parameter down and return the first index that passes the test against every smaller parameter. That is the largest admissible index. Index $0$ is always admissible, because it has nothing to test against, so the scan always returns.

## Example

Take the same problem as on the GCV page: $A = \mathrm{diag}(s_1, \dots, s_{32})$ with $s_i = 1/i^2$, $x^\dagger_i = 1/i^2$, and $e_i = 10^{-3}g_i$ with $g_i$ from `random.Random(0).gauss(0, 1)`. Then $\delta = \lVert e\rVert = 0.006508$. The grid is $\alpha_j = 10^{-6}\cdot 2^j$ for $j = 0, \dots, 20$, and $\kappa = 1$. The table shows $\psi$, the unknown $\varphi$, the error, and the worst ratio $\max_{i < j}\lVert x_{\alpha_j} - x_{\alpha_i}\rVert/(4\psi_i)$, which must be at most 1 for $j$ to pass.

| $j$ | $\alpha_j$ | $\psi_j$ | $\varphi_j$ | $\lVert x_{\alpha_j} - x^\dagger\rVert$ | worst ratio |
|---|---|---|---|---|---|
| 8 | 0.000256 | 0.20337 | 0.02350 | 0.09195 | 0.193 |
| 10 | 0.001024 | 0.10169 | 0.03975 | 0.05823 | 0.199 |
| 11 | 0.002048 | 0.07190 | 0.05161 | 0.06198 | 0.200 |
| 12 | 0.004096 | 0.05084 | 0.06698 | 0.07351 | 0.201 |
| 14 | 0.016384 | 0.02542 | 0.11273 | 0.11659 | 0.270 |
| 15 | 0.032768 | 0.01798 | 0.14628 | 0.14932 | 0.496 |
| 16 | 0.065536 | 0.01271 | 0.18931 | 0.19141 | 0.906 |
| 17 | 0.131072 | 0.00899 | 0.24411 | 0.24521 | 1.654 |
| 18 | 0.262144 | 0.00636 | 0.32012 | 0.32042 | 3.219 |
| 19 | 0.524288 | 0.00449 | 0.43288 | 0.43273 | 6.521 |
| 20 | 1.048576 | 0.00318 | 0.58065 | 0.58039 | 12.048 |

The scan of line L4 starts at $j = 20$, which fails, as do 19, 18 and 17. Index 16 passes with a worst ratio of $0.906$, so the rule returns $\alpha = 0.065536$ with error $0.19141$. The best error on the grid is $0.05823$, at $j = 10$.

The guarantee holds: the balancing index of the theory is $j^\ast = 11$, the last $j$ with $\varphi_j \le \psi_j$, and the proof gives the bound $6\psi_{j^\ast} = 0.4314$ on the error, which $0.19141$ respects. But the rule over-smooths here by a factor of about 3 in the error, because $\psi$ is a worst-case bound: at $\alpha_{11}$ the actual noise in the solution is $0.0191$, while $\psi_{11} = 0.0719$. The same effect appears with the default grid of the implementation, from $s_{32}^2/100$ to $s_1^2$ with ratio $1.5$, which returns $\alpha = 0.0703$ and error $0.1962$.

## Correctness

The proof is in `proofs/correctness.md`. Lines L4 to L8 return the largest admissible index, and they always return, because index $0$ is admissible. The main result is an oracle inequality. Assume $\varphi(\alpha_0) \le \psi(\alpha_0)$, which holds when the grid starts at a small enough $\alpha$, and let $j^\ast$ be the largest $j$ with $\varphi_j \le \psi_j$. For all $i < j \le j^\ast$,

$$\lVert x_{\alpha_j} - x_{\alpha_i}\rVert \le \varphi_j + \psi_j + \varphi_i + \psi_i \le 2\psi_j + 2\psi_i \le 4\psi_i,$$

so $j^\ast$ is admissible and the chosen index $\hat j$ is at least $j^\ast$. Then, by the test at $i = j^\ast$,

$$\lVert x_{\alpha_{\hat j}} - x^\dagger\rVert \le \lVert x_{\alpha_{\hat j}} - x_{\alpha_{j^\ast}}\rVert + \lVert x_{\alpha_{j^\ast}} - x^\dagger\rVert \le 4\kappa\psi_{j^\ast} + 2\psi_{j^\ast} = (4\kappa + 2)\psi_{j^\ast}.$$

If the grid is geometric with ratio $\rho = \alpha_{j+1}/\alpha_j$, then $\psi_{j^\ast} \le \sqrt\rho\,\min_j(\varphi_j + \psi_j)$, and so the error is at most $(4\kappa + 2)\sqrt\rho$ times the best balance on the grid. This is a theorem.

Under a source condition $x^\dagger = (A^TA)^\nu w$ with $0 < \nu \le 1$, the approximation error of Tikhonov satisfies $\varphi(\alpha) \le \alpha^\nu\lVert w\rVert$, and the best balance is of order $\delta^{2\nu/(2\nu + 1)}$. The rule reaches this order for every $\nu$ up to the qualification $1$ of Tikhonov, without knowing $\nu$, provided the grid covers the balancing point. The discrepancy principle stops at $\nu = 1/2$. See [Tikhonov convergence rates](/tikhonov-convergence-rates/) and [qualification](/qualification-of-regularization/).

## Complexity

With the thin SVD given, line L1 costs $\Theta(mn)$ and lines L2 and L3 cost $\Theta(Nr)$. Each distance in line L6 costs $\Theta(r)$. In the worst case the scan tests all pairs, $\Theta(N^2r)$. In the best case the largest index passes at once after $N - 1$ tests. Line L8 costs $\Theta(n^2) \subseteq O(mn)$. The total is $\Theta(mn + N^2n)$ in the worst case and $\Theta(mn + Nn)$ in the best, with $\Theta(Nn)$ extra space for the stored solutions. With a geometric grid, $N$ grows only like $\log(\alpha_{\max}/\alpha_{\min})$, so $N^2$ is small. The SVD itself costs $O(mn^2)$ and dominates.

## Properties

- A posteriori: it needs $\delta$ and $y^\delta$, not $x^\dagger$ or its smoothness.
- Adaptive: one rule is order optimal for all smoothness classes the method can exploit. For Tikhonov that is $0 < \nu \le 1$.
- Proved oracle inequality on the grid, with the constant $(4\kappa + 2)\sqrt\rho$.
- Works for any regularization method with a known noise bound $\psi$: [Landweber](/landweber-iteration/) with $\psi_k = \sqrt k\,\delta$, truncated SVD with $\psi_k = \delta/s_k$, and statistical noise models with a stochastic bound.
- Tends to over-smooth in practice, because $\psi$ bounds the worst case of the noise, not the typical case.

## Variants and improvements

- **Statistical noise.** For white noise of variance $\sigma^2$, replace $\psi$ by a bound on the typical noise in the solution, such as $\sigma\sqrt{\sum_i s_i^2/(s_i^2 + \alpha)^2}$ times a factor that grows with $\log N$. This is the setting of Lepskii's original work.
- **Smaller constants.** Many users replace $4\kappa$ by $2$ or less. The rule then picks smaller $\alpha$ and is often more accurate, but the proof above no longer applies.
- **Nonlinear problems and iterations.** The same comparison works for iteratively regularized Gauss-Newton and for stopping Landweber, with the appropriate $\psi$.

## When to use it

Use it when the noise level is known, the smoothness of the solution is not, and you want a rule with a proved guarantee that does not saturate. It is a natural choice for theory-driven work and for methods with high qualification, where the [discrepancy principle](/morozov-discrepancy-principle/) loses the best rate. If you want the most accurate $\alpha$ for one dataset and the noise is white, [UPRE](/unbiased-predictive-risk-estimator/) is usually closer to the best. If $\delta$ is unknown, the rule cannot be used; see the [quasi-optimality criterion](/quasi-optimality-criterion/) and the [Bakushinskii veto](/bakushinskii-veto/).

## Pitfalls

- A grid that starts too high. The oracle inequality needs $\varphi(\alpha_0) \le \psi(\alpha_0)$. If $\alpha_0$ already over-smooths, the rule has nothing to balance against. Start the grid well below $s_r^2$.
- A wrong $\psi$. For Tikhonov the noise bound is $\delta/(2\sqrt\alpha)$, not $\delta/\alpha$. A too large $\psi$ in line L3 makes every index admissible, and line L8 returns the largest $\alpha$.
- Testing only against the previous index in line L5. The proof needs the test against every smaller index; a chain of small steps can drift far.
- Scanning from the small end and stopping at the first failure. This gives a different rule, with a different index, unless the admissible set is an interval. The implementation scans from the large end and returns the largest admissible index, as the theory requires.
- Expecting the best $\alpha$. The guarantee is a factor of $6\sqrt\rho$ in the worst case, and in the example the rule loses a factor of 3. Use it for safety, not for the last few percent.

## Implementations

## History

Lepskii (1990) introduced the method to choose a bandwidth in nonparametric estimation in Gaussian white noise, without knowing the smoothness of the signal, and showed that it adapts to the unknown smoothness. Goldenshluger and Pereverzev applied it to ill-posed problems with random noise around 2000. Mathé and Pereverzev (2003) used it for linear ill-posed problems in variable Hilbert scales, and Mathé (2006) revisited the method for linear ill-posed problems. It is now a standard tool for adaptive parameter choice in regularization and in learning theory.

## References
