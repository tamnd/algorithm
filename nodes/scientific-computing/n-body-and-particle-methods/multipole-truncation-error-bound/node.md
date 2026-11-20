---
tag: PA4064
kind: theorem
slug: multipole-truncation-error-bound
name: Multipole truncation error bound
area: scientific-computing/n-body-and-particle-methods
level: core
summary: "For charges of total absolute size A within radius r, the p-term multipole error at distance R > r is at most A/(R - r) (r/R)^(p+1) in 3D (1/r) and A/((p+1)(1 - r/R)) (r/R)^(p+1) in 2D (log)."
prereqs: [multipole-expansion]
see_also: [fast-multipole-method, multipole-to-local-translation, multipole-acceptance-criterion, barnes-hut-algorithm, adaptive-fast-multipole-method, legendre-polynomials]
sources:
  - paper: doi:10.1016/0021-9991(87)90140-9
    title: "Leslie Greengard and Vladimir Rokhlin, A fast algorithm for particle simulations, Journal of Computational Physics 73(2), 1987, 325-348"
    locator: the multipole expansion of the 2D logarithmic potential and its truncation error bound
  - url: https://math.nyu.edu/~greengar/shortcourse_fmm.pdf
    title: "Rick Beatson and Leslie Greengard, A short course on fast multipole methods, in Wavelets, Multilevel Methods and Elliptic PDEs, Oxford University Press, 1997"
    locator: "Lemma 4.2 and the bound (4.11) for 2D; Theorem 5.2 for the 3D Coulomb kernel; Section 5 for the decay rates in an FMM box geometry"
  - book: isbn:9780262071109
    title: Leslie Greengard, The Rapid Evaluation of Potential Fields in Particle Systems, MIT Press, 1988
    locator: the multipole expansion in spherical harmonics and its error bound in three dimensions
---

## Statement

Let $q_1, \ldots, q_m$ be real charges and $A = \sum_{i=1}^{m} |q_i|$ their total absolute size. All of them lie within distance $r$ of the center, which is the origin. The order $p \ge 0$ is an integer, and the target is at distance $R > r$ from the origin.

**Theorem 1 (two dimensions, logarithmic kernel).** Let the charges sit at $z_i \in \mathbb{C}$ with $|z_i| \le r$, and let $u(z) = \sum_i q_i \log|z - z_i|$. Let $a_0 = \sum_i q_i$ and $a_k = -\sum_i q_i z_i^k / k$ for $k \ge 1$. Then for every $z$ with $|z| = R > r$ and every $p \ge 1$,

$$\left| u(z) - \mathrm{Re}\left( a_0 \log z + \sum_{k=1}^{p} \frac{a_k}{z^k} \right) \right| \le \frac{A}{p + 1} \cdot \frac{1}{1 - r/R} \left( \frac{r}{R} \right)^{p+1}.$$

**Theorem 2 (three dimensions, Coulomb kernel).** Let the charges sit at $\mathbf{x}_i \in \mathbb{R}^3$ with $|\mathbf{x}_i| = r_i \le r$, and let $\Phi(\mathbf{x}) = \sum_i q_i / |\mathbf{x} - \mathbf{x}_i|$. For $|\mathbf{x}| = R$ and the angle $\gamma_i$ between $\mathbf{x}$ and $\mathbf{x}_i$, the term of degree $n$ of the multipole expansion of $\Phi$ is $\sum_i q_i \, r_i^n P_n(\cos \gamma_i) / R^{n+1}$, where $P_n$ is the Legendre polynomial; written in spherical harmonics, it is the sum over $m = -n, \ldots, n$ of the terms $M_n^m Y_n^m(\theta, \varphi) / R^{n+1}$. Let $\Phi_p$ be the sum of the terms of degree $0$ to $p$. Then for every $\mathbf{x}$ with $|\mathbf{x}| = R > r$,

$$|\Phi(\mathbf{x}) - \Phi_p(\mathbf{x})| \le \frac{A}{R - r} \left( \frac{r}{R} \right)^{p+1}.$$

Both bounds depend on the charges only through $A$ and $r$, and on the target only through $R$. With $c = R / r$, the 2D bound is $\frac{A}{(p+1)(c - 1)} c^{-p}$, the form of Lemma 4.2 of Beatson and Greengard.

## In plain words

Far from a group of charges, the field of the group is smooth, and a short series describes it. The series has one term for each order: the total charge, then the dipole, then the quadrupole, and so on. If you stop after a few terms, you make an error.

The theorem says how large the error can be. It depends on the ratio of the size of the group to the distance of the target. Each extra term multiplies the bound by this ratio. If the target is twice as far as the edge of the group, each term gains about one binary digit. The bound uses only the size of the group, the total of the charges without signs, and the distance, so it holds for every arrangement of the charges inside the group.

## Proof

*Theorem 1.* Fix a charge $q_i$ at $z_i$ and let $t = z_i / z$, so $|t| \le r / R < 1$. For $|t| < 1$ the power series $\log(1 - t) = -\sum_{k \ge 1} t^k / k$ converges, and $\log|z - z_i| = \log|z| + \log|1 - t| = \mathrm{Re}\left( \log z + \log(1 - t) \right)$. So

$$q_i \log|z - z_i| = \mathrm{Re}\left( q_i \log z - \sum_{k \ge 1} \frac{q_i z_i^k}{k z^k} \right).$$

Summing over $i$ gives $u(z) = \mathrm{Re}\left( a_0 \log z + \sum_{k \ge 1} a_k z^{-k} \right)$, where the sums over $i$ and $k$ can be exchanged because the series converges absolutely. The error of the truncation after $k = p$ is the real part of $-\sum_i q_i \sum_{k > p} t_i^k / k$, with $t_i = z_i / z$. Its modulus is at most

$$\sum_i |q_i| \sum_{k > p} \frac{|t_i|^k}{k} \le \sum_i |q_i| \frac{1}{p + 1} \sum_{k > p} \left( \frac{r}{R} \right)^k = \frac{A}{p + 1} \cdot \frac{(r / R)^{p+1}}{1 - r / R}. \qquad \square$$

*Theorem 2.* Fix a charge at $\mathbf{x}_i$, with $r_i = |\mathbf{x}_i| \le r < R$. The generating function of the Legendre polynomials gives, for $r_i < R$,

$$\frac{1}{|\mathbf{x} - \mathbf{x}_i|} = \frac{1}{\sqrt{R^2 - 2 R r_i \cos \gamma_i + r_i^2}} = \sum_{n=0}^{\infty} \frac{r_i^n}{R^{n+1}} P_n(\cos \gamma_i).$$

By the addition theorem for spherical harmonics, $P_n(\cos \gamma_i)$ is a finite sum of products $Y_n^m(\theta, \varphi)$ times a function of the direction of $\mathbf{x}_i$, so the degree $n$ part of this series is the degree $n$ part of the multipole expansion. Since $|P_n(s)| \le 1$ for $|s| \le 1$, the tail after degree $p$ is at most

$$\sum_{n > p} \frac{r_i^n}{R^{n+1}} = \frac{1}{R} \cdot \frac{(r_i / R)^{p+1}}{1 - r_i / R} = \frac{(r_i / R)^{p+1}}{R - r_i} \le \frac{(r / R)^{p+1}}{R - r},$$

because the middle expression grows with $r_i$. Multiply by $|q_i|$ and sum over $i$. $\square$

## Consequences

- **A digit per term at twice the distance.** In 2D with $c = R / r \ge 2$, the bound is at most $A (1/2)^p / (p + 1) \le A (1/2)^p$, the estimate (4.11) of Beatson and Greengard. So $p = \lceil \log_2(1/\varepsilon) \rceil$ terms give an error below $\varepsilon A$. In 3D with $R \ge 2r$, the bound is at most $(A / r) (1/2)^{p+1}$, since $R - r \ge r$, with $(p + 1)^2$ coefficients.
- **Box geometry of the FMM.** A square box of side $w$ fits in a disk of radius $w / \sqrt{2}$. A target in a box that is not a near neighbour is at distance at least $1.5 w$ from the center, so $r / R \le \sqrt{2} / 3 \approx 0.47$. For cubes, the ratio is $\sqrt{3} / 3 \approx 0.58$, which is why 3D codes need more terms (Beatson and Greengard, Section 5). These ratios come from the theorem and the geometry; the error of the full FMM also has the M2L step, which needs both boxes (see [multipole-to-local translation](/multipole-to-local-translation/)).
- **Monopole error.** With $p = 0$, Theorem 2 gives $A r / (R (R - r))$ for the [Barnes-Hut](/barnes-hut-algorithm/) monopole about any center inside the ball. About the center of mass of positive masses the dipole term is zero, so the bound for $p = 1$ applies to the monopole, and the error is at most $A r^2 / (R^2 (R - r))$.
- **The bound is relative to A, not to the potential.** For charges of both signs, $|\Phi|$ can be much smaller than $A / R$, and the relative error of the potential can be much larger than the bound divided by $|\Phi|$. This matters for neutral systems (a rule of thumb, not a theorem: check against direct summation).
- **Use in acceptance criteria.** Error-bound criteria for tree codes choose, for each cell, the order or the opening distance from bounds of this form; see [multipole acceptance criterion](/multipole-acceptance-criterion/).

## Tightness

The 3D bound is attained. Put one unit charge at distance $r$ on the axis and the target on the same axis at distance $R$. Then $\cos \gamma = 1$, every $P_n(1) = 1$, and the tail is exactly $\sum_{n > p} r^n / R^{n+1} = (r/R)^{p+1} / (R - r)$. With $r = 0.5$ and $R = 1$, the exact potential is $1 / 0.5 = 2$, and the truncated series $1 + 0.5 + 0.25 + \cdots$ gives:

| $p$ | $\Phi_p$ | error | bound $\frac{A}{R - r} (r/R)^{p+1}$ |
|---|---|---|---|
| 0 | 1 | 1 | 1 |
| 1 | 1.5 | 0.5 | 0.5 |
| 3 | 1.875 | 0.125 | 0.125 |

In the direction at a right angle to the charge, the odd Legendre terms vanish and the error is much smaller: $0.1056$, $0.0194$ and $0.0040$ for $p = 1$, $2$ and $4$, against bounds $0.5$, $0.25$ and $0.0625$.

The 2D bound is tight up to the factor $1 - r/R$. One unit charge at $z_1 = r$ and the target at $z = R$ on the real axis give the error $\sum_{k > p} (r/R)^k / k$, which is at least $(r/R)^{p+1} / (p + 1)$, so the ratio of the error to the bound is at least $1 - r/R$, and it tends to 1 as $p$ grows. With $r = 0.5$ and $R = 1$, the exact value is $\log 0.5 = -0.693147$:

| $p$ | truncated series | error | bound | error / bound |
|---|---|---|---|---|
| 1 | $-0.5$ | 0.193147 | 0.25 | 0.77 |
| 3 | $-0.666667$ | 0.026481 | 0.03125 | 0.85 |
| 5 | $-0.688542$ | 0.004606 | 0.005208 | 0.88 |

For $p = 1$ the series is $a_0 \log 1 + a_1 / 1 = -0.5$, and the bound is $\frac{1}{2} \cdot \frac{1}{1 - 0.5} \cdot 0.25 = 0.25$; both can be checked by hand. The geometric rate $r / R$ cannot be improved in either dimension, since the error of these examples falls by the factor $r / R$ per term as $p$ grows.

## History

Greengard and Rokhlin (1987) gave the 2D expansion in complex form with this bound, as the base of the [fast multipole method](/fast-multipole-method/). Greengard's thesis, published by MIT Press in 1988, gave the 3D bound with spherical harmonics. The lecture notes of Beatson and Greengard (1997) state both bounds in the form above, with the box geometries that set the decay rates in practice.

## References
