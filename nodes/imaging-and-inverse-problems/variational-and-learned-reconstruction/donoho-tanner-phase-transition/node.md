---
tag: VQAV4Y
kind: theorem
slug: donoho-tanner-phase-transition
name: Donoho-Tanner phase transition
aliases:
- phase transition of L1 recovery
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: research
summary: For random Gaussian measurements L1 recovery has a sharp threshold in the sparsity and sampling ratios, computed from the face counts of random polytopes.
prereqs: [basis-pursuit, null-space-property, convex-polytope]
see_also: [candes-romberg-tao-theorem, approximate-message-passing, restricted-isometry-property, mutual-coherence, compressed-sensing, sparse-signal-recovery, linear-programming-problem, johnson-lindenstrauss-lemma]
sources:
  - paper: doi:10.1007/s00454-005-1220-0
    title: David L. Donoho, High-dimensional centrally symmetric polytopes with neighborliness proportional to dimension, Discrete and Computational Geometry 35(4), 2006
    locator: pages 617 to 652 (l1 recovery as a face of the projected cross-polytope, neighborliness, and the existence of the weak and strong thresholds for Gaussian projections)
  - paper: doi:10.1090/S0894-0347-08-00600-0
    title: David L. Donoho and Jared Tanner, Counting faces of randomly projected polytopes when the projection radically lowers dimension, Journal of the American Mathematical Society 22(1), 2009
    locator: pages 1 to 53 (the expected face counts of projected cross-polytopes and simplices, and the weak and strong threshold curves)
  - paper: doi:10.1073/pnas.0502258102
    title: David L. Donoho and Jared Tanner, Neighborliness of randomly projected simplices in high dimensions, Proceedings of the National Academy of Sciences 102(27), 2005
    locator: pages 9452 to 9457 (the nonnegative case, with the simplex in place of the cross-polytope)
  - paper: doi:10.1098/rsta.2009.0152
    title: David L. Donoho and Jared Tanner, Observed universality of phase transitions in high-dimensional geometry, with implications for modern data analysis and signal processing, Philosophical Transactions of the Royal Society A 367(1906), 2009
    locator: pages 4273 to 4293 (experiments with many non-Gaussian matrix ensembles; measurements, not theorems)
  - paper: doi:10.1093/imaiai/iau005
    title: Dennis Amelunxen, Martin Lotz, Michael B. McCoy and Joel A. Tropp, Living on the edge, phase transitions in convex programs with random data, Information and Inference 3(3), 2014
    locator: pages 224 to 294; Theorem II (the two-sided transition at the statistical dimension of the descent cone), Section 4 (the statistical dimension of the l1 descent cone and the formula for psi)
---

The Donoho-Tanner phase transition is the exact boundary between success and failure of $\ell_1$ minimization, [basis pursuit](/basis-pursuit/), for recovering a sparse vector from random Gaussian measurements. With $n$ unknowns, $m$ measurements and $s$ nonzeros, recovery succeeds with probability near 1 below a curve in the plane of $\delta = m/n$ and $\rho = s/m$, and fails with probability near 1 above it. The curve is computed exactly, not up to an unknown constant. This differs from the [Candes-Romberg-Tao theorem](/candes-romberg-tao-theorem/), which treats random Fourier samples and has an explicit but small constant, and from the [restricted isometry property](/restricted-isometry-property/), which gives sufficient conditions far below the curve. It is the random-matrix answer to the question that the [null space property](/null-space-property/) answers for one matrix. [Approximate message passing](/approximate-message-passing/) reaches the same curve.

## Statement

Let $A$ be an $m \times n$ matrix with independent standard Gaussian entries, with $m < n$. Let $x \in \mathbb{R}^n$ be a fixed vector with $s$ nonzero entries, chosen independently of $A$, and let $y = Ax$. Say that $\ell_1$ minimization succeeds if $x$ is the unique solution of $\min\|z\|_1$ subject to $Az = y$. Let $C = \{z : \|z\|_1 \le 1\}$ be the cross-polytope in $\mathbb{R}^n$ and $f_k(\cdot)$ the number of $k$-dimensional faces of a polytope.

**Theorem (Donoho 2006; Donoho and Tanner 2009).**

1. For every $n$, $m$ and $s \le m$, with probability 1 over $A$, $\ell_1$ minimization succeeds if and only if $A$ maps the $(s - 1)$-face of $C$ that contains $x/\|x\|_1$ onto a face of the polytope $AC$. The probability of success depends only on $n$, $m$ and $s$, and equals $\mathbb{E}f_{s-1}(AC)/f_{s-1}(C)$.
2. There is a curve $\rho_W(\delta)$, given by a formula in terms of the internal and external angles of the cross-polytope, with the following property. Let $n \to \infty$ with $m/n \to \delta \in (0, 1)$ and $s/m \to \rho$. If $\rho < \rho_W(\delta)$, the probability of success tends to 1.
3. There is a lower curve $\rho_S(\delta) < \rho_W(\delta)$, the strong threshold, such that for $\rho < \rho_S(\delta)$ the probability that $\ell_1$ minimization succeeds for every $s$-sparse vector at once tends to 1. This is the condition that $AC$ is centrally $s$-neighborly, which by the null space property is the uniform version.

**Theorem (Amelunxen, Lotz, McCoy and Tropp 2014, Theorem II and Section 4).** Let $D$ be the descent cone of $\|\cdot\|_1$ at $x$, and let its statistical dimension be $\delta(D) = \mathbb{E}\|\Pi_D(g)\|^2$, with $g$ a standard Gaussian vector in $\mathbb{R}^n$ and $\Pi_D$ the projection onto $D$. For every $\eta \in (0, 1)$ there is a constant $a_\eta$ such that $\ell_1$ minimization succeeds with probability at least $1 - \eta$ if $m \ge \delta(D) + a_\eta\sqrt n$, and with probability at most $\eta$ if $m \le \delta(D) - a_\eta\sqrt n$. Moreover $\delta(D) = n\,\psi(s/n) + O(\sqrt n)$, where

$$\psi(r) = \inf_{\tau \ge 0}\Big[r(1 + \tau^2) + (1 - r)\,\mathbb{E}\big(|Z| - \tau\big)_+^2\Big], \qquad Z \sim N(0, 1).$$

So the transition sits at $m/n = \psi(s/n)$, with a window of width of order $\sqrt n$ in $m$. This curve agrees with the weak threshold $\rho_W$ of Donoho and Tanner. Both theorems hold for a fixed $x$ and a Gaussian $A$, with probability over $A$. Neither covers other matrix laws.

## In plain words

Draw a map with the fraction of measurements on one axis and the fraction of nonzero entries on the other. One curve cuts this map in two. Below the curve, the convex method recovers the sparse signal almost always. Above it, the method almost always fails. The change is abrupt when the signal is long. The curve is known exactly, and it comes from counting the corners and edges that survive when a high-dimensional diamond is squashed into fewer dimensions.

## Proof

The geometric part, item 1, is short and is proved here. The asymptotic face counts of items 2 and 3 and the concentration in the second theorem are long and are only cited. The formula for $\psi$ is derived here as an upper bound on the statistical dimension.

**Success is a property of the null space.** By the definition of the descent cone, $D = \{d : \|x + td\|_1 \le \|x\|_1 \text{ for some } t > 0\}$, the vector $x$ is the unique minimizer if and only if $\ker A \cap D = \{0\}$. Let $S$ be the support of $x$. A short computation gives $D = \{d : \sum_{i \in S}\operatorname{sgn}(x_i)d_i + \sum_{i \notin S}|d_i| \le 0\}$, which depends only on $S$ and the signs on $S$.

**Faces.** The set $F = \operatorname{conv}\{\operatorname{sgn}(x_i)e_i : i \in S\}$ is the $(s - 1)$-face of $C$ that contains $x/\|x\|_1$. $AF$ is a face of $AC$ exactly when some linear functional is maximal on $AC$ exactly at $AF$. Pulled back through $A$, this is a functional in the row space of $A$ that is maximal on $C$ exactly at $F$, that is a dual certificate $u = A^T\lambda$ with $u_i = \operatorname{sgn}(x_i)$ on $S$ and $|u_i| < 1$ off $S$. By duality for the linear program of basis pursuit, such a certificate exists if and only if $\ker A \cap D = \{0\}$ (when $A_S$ is injective, which holds almost surely for $s \le m$). So success is the face condition of item 1.

**Symmetry.** The law of a Gaussian matrix does not change when its columns are permuted or multiplied by signs. These maps permute the $(s - 1)$-faces of $C$ transitively. So every face survives with the same probability $p$, and $\mathbb{E}f_{s-1}(AC) = p\,f_{s-1}(C)$. The kernel of $A$ is a uniformly distributed subspace of dimension $n - m$, and the second theorem uses only this fact.

**The formula for $\psi$.** The polar cone of $D$ is the cone generated by the subdifferential $\partial\|x\|_1 = \{u : u_i = \operatorname{sgn} x_i \text{ on } S,\ |u_i| \le 1 \text{ off } S\}$, and $\delta(D) = \mathbb{E}\operatorname{dist}^2(g, D^\circ)$. For each fixed $\tau \ge 0$ the set $\tau\,\partial\|x\|_1$ lies in $D^\circ$, so

$$\delta(D) \le \mathbb{E}\operatorname{dist}^2\big(g, \tau\,\partial\|x\|_1\big) = \sum_{i \in S}\mathbb{E}(g_i - \tau\operatorname{sgn} x_i)^2 + \sum_{i \notin S}\mathbb{E}(|g_i| - \tau)_+^2 = s(1 + \tau^2) + (n - s)\,\mathbb{E}(|Z| - \tau)_+^2.$$

The infimum over $\tau$ is $n\,\psi(s/n)$. Amelunxen, Lotz, McCoy and Tropp prove the matching lower bound up to $O(\sqrt n)$. For computation, $\mathbb{E}(|Z| - \tau)_+^2 = 2[(1 + \tau^2)Q(\tau) - \tau\varphi(\tau)]$ with the Gaussian density $\varphi$ and tail $Q(\tau) = \Pr(Z > \tau)$.

## Consequences

**The curve (computed).** The values below come from minimizing over $\tau$ and solving $\psi(s/n) = m/n$ by bisection. They are computed from the formula, not measured.

| $\delta = m/n$ | $s/n$ at the transition | $\rho = s/m$ at the transition |
|---|---|---|
| 0.1 | 0.0189 | 0.189 |
| 0.2 | 0.0487 | 0.243 |
| 0.3 | 0.0872 | 0.291 |
| 0.4 | 0.1349 | 0.337 |
| 0.5 | 0.1928 | 0.386 |
| 0.6 | 0.2630 | 0.438 |
| 0.7 | 0.3492 | 0.499 |
| 0.8 | 0.4587 | 0.573 |
| 0.9 | 0.6104 | 0.678 |

For example, with $n = 128$ and $m = 64$, the transition is at $s \approx 24.7$. Three values of the function itself are $\psi(0.05) \approx 0.204$, $\psi(0.1) \approx 0.329$ and $\psi(0.2) \approx 0.511$. A few lines reproduce the table:

```python
import math

def tail2(t):  # E (|Z| - t)_+^2
    q = 0.5 * math.erfc(t / math.sqrt(2))
    phi = math.exp(-t * t / 2) / math.sqrt(2 * math.pi)
    return 2 * ((1 + t * t) * q - t * phi)

def psi(r, lo=0.0, hi=10.0):
    f = lambda t: r * (1 + t * t) + (1 - r) * tail2(t)
    for _ in range(200):  # ternary search, f is convex in t
        a, b = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        lo, hi = (lo, b) if f(a) < f(b) else (a, hi)
    return f((lo + hi) / 2)

def transition(delta):  # s/n with psi(s/n) = delta
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if psi(mid) < delta else (lo, mid)
    return lo
```

The same values come out of the parametric formula of Donoho, Maleki and Montanari for the minimax risk of soft thresholding, which they used to show that [approximate message passing](/approximate-message-passing/) has this phase transition. The two formulas agreed to 4 decimals at $\delta = 0.1, 0.25, 0.5, 0.9$ in a check for this page.

**Very sparse signals.** As $s/n \to 0$, $\psi(r) \sim 2r\log(1/r)$, so the transition is at $m \approx 2s\log(n/s)$. This is the familiar $s\log(n/s)$ of [compressed sensing](/compressed-sensing/), now with the constant 2. The approach to this limit is slow: the computed ratio $\psi(r)/(2r\log(1/r))$ is 0.68 at $r = 10^{-3}$ and 0.76 at $r = 10^{-6}$, so for practical sizes $2s\log(n/s)$ overestimates the number of measurements.

**Comparison with sufficient conditions.** Bounds from the restricted isometry property or from [mutual coherence](/mutual-coherence/) guarantee recovery only far below the curve. For $64 \times 128$ Gaussian matrices, coherence guarantees $s = 1$, while the curve is near $s = 25$. Those conditions are uniform over all sparse vectors and hold for one matrix, which explains part of the gap.

**Universality (measurement).** Donoho and Tanner (2009, Philosophical Transactions) ran $\ell_1$ minimization for many matrix laws, for example random signs, partial Fourier and partial Hadamard matrices, and found transitions at the same place as for Gaussian matrices. This is an empirical observation, not part of the theorem. Later theorems proved it for some classes of random matrices with independent entries.

**Nonnegative signals.** When $x \ge 0$ is known and the program adds $z \ge 0$, the cross-polytope is replaced by the simplex, and the transition curve is higher. Donoho and Tanner treated this case in the 2005 PNAS paper on simplices and in the 2009 paper.

## Tightness

**Width of the window.** The transition has width of order $\sqrt n$ in $m$, so in the ratios it narrows like $1/\sqrt n$. For small $n$ the change from success to failure is gradual.

**An exact small case.** Let $n = 3$, $m = 2$, $s = 1$, $x = e_1$. The kernel of $A$ is a line in a uniformly random direction $v$, and recovery fails exactly when $\pm v$ is in $D = \{d : -d_1 \ge |d_2| + |d_3|\}$. This cone meets the unit sphere in a spherical quadrilateral with corners in the directions $(-1, \pm1, 0)$ and $(-1, 0, \pm1)$. The angle at each corner is $\arccos(-\tfrac13)$, so its area is $4\arccos(-\tfrac13) - 2\pi \approx 1.359$. The line hits $D$ or $-D$, so the failure probability is

$$\frac{2\,(4\arccos(-\tfrac13) - 2\pi)}{4\pi} \approx 0.216,$$

and success has probability about 0.784. A Monte Carlo check with 400000 random directions gave 0.2161 for the failure rate. Here $s/n = 1/3$ is close to the asymptotic transition at $\delta = 2/3$, and the answer is far from 0 or 1: in small dimensions the transition is blurred.

**Weak and strong.** The weak threshold applies to one fixed vector, or to most vectors. The strong threshold, for all vectors at once, is strictly lower. A matrix drawn once and used for many signals is covered by the strong threshold, or by the weak one only for each signal separately.

**Only Gaussian, only noiseless.** The theorems need a Gaussian matrix, or a kernel with a rotation invariant law, and exact measurements. With noise the same curve is the boundary of the region where the error of the LASSO stays bounded relative to the noise, a result of Donoho, Maleki and Montanari for the minimax setting.

## History

Donoho (2006) turned the question of $\ell_1$ recovery into a question about faces of randomly projected cross-polytopes, and proved that the weak and strong thresholds are positive for every $\delta$. Donoho and Tanner computed both curves from the asymptotics of internal and external angles, for simplices in their 2005 PNAS paper and for cross-polytopes and simplices in the 2009 paper. They also measured the universality of the curve over many matrix laws in 2009. Donoho, Maleki and Montanari (2009) found the same weak curve as the boundary of approximate message passing. Amelunxen, Lotz, McCoy and Tropp (2014) explained the transition for general convex programs by the statistical dimension of the descent cone, and proved that the transition window has width of order $\sqrt n$. The question of the number of faces of a randomly projected polytope goes back to Affentranger and Schneider (1992) and Vershik and Sporyshev (1992).

## References
