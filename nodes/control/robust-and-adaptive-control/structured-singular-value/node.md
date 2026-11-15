---
tag: KV0FBQ
kind: definition
slug: structured-singular-value
name: Structured singular value
aliases:
- SSV
- structured singular value mu
area: control/robust-and-adaptive-control
level: advanced
summary: The inverse of the size of the smallest block structured perturbation that makes I - M Delta singular. It gives a robust stability test that is exact for that structure.
prereqs: [linear-fractional-transformation, singular-value-decomposition, spectral-radius]
see_also: [mu-analysis, dk-iteration, model-uncertainty, small-gain-theorem, h-infinity-norm, linear-matrix-inequality, np-hard, power-iteration]
sources:
  - paper: doi:10.1049/ip-d.1982.0053
    title: John C. Doyle, Analysis of feedback systems with structured uncertainties, IEE Proceedings D 129(6), 242, 1982
    locator: the definition of mu, the bounds by the spectral radius and by D scaling, and exactness for three full blocks
  - paper: doi:10.1049/ip-d.1982.0054
    title: Michael G. Safonov, Stability margins of diagonally perturbed multivariable feedback systems, IEE Proceedings D 129(6), 251, 1982
    locator: the multivariable stability margin k_m, the inverse of mu, for diagonal perturbations
  - paper: doi:10.1016/0005-1098(93)90175-S
    title: Andrew Packard and John C. Doyle, The complex structured singular value, Automatica 29(1), 71-109, 1993
    locator: the general block structure, the lower bound as a maximum of spectral radii, and the cases 2S + F at most 3 where the D scaling bound is exact
  - paper: doi:10.1109/9.284879
    title: Richard D. Braatz, Peter M. Young, John C. Doyle and Manfred Morari, Computational complexity of mu calculation, IEEE Transactions on Automatic Control 39(5), 1000-1002, 1994
    locator: NP-hardness of computing mu with real or mixed real and complex uncertainty
  - paper: doi:10.1109/9.661609
    title: Onur Toker and Hitay Ozbay, On the complexity of purely complex mu computation and related problems in multidimensional systems, IEEE Transactions on Automatic Control 43(3), 409-414, 1998
    locator: NP-hardness of purely complex mu
  - paper: doi:10.1109/9.62265
    title: Michael K. H. Fan, Andre L. Tits and John C. Doyle, Robustness in the presence of mixed parametric uncertainty and unmodeled dynamics, IEEE Transactions on Automatic Control 36(1), 25-38, 1991
    locator: the upper bound for mixed real and complex uncertainty with D and G scalings
  - paper: doi:10.1109/CDC.1988.194710
    title: Andrew Packard, Michael K. H. Fan and John C. Doyle, A power method for the structured singular value, Proceedings of the 27th IEEE Conference on Decision and Control, 2132-2137, 1988
    locator: the power iteration for the lower bound
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 11, Structured Singular Value
---

The structured singular value $\mu_{\boldsymbol\Delta}(M)$ of a complex matrix $M$ measures how small a perturbation $\Delta$ of a given block diagonal form can be and still make $I - M \Delta$ singular. John Doyle defined it in 1982. Michael Safonov defined the same quantity in the same issue of IEE Proceedings D as the multivariable stability margin $k_m = 1/\mu$. In a feedback loop written as a [linear fractional transformation](/linear-fractional-transformation/) of a known system $M$ and an unknown $\Delta$, $\mu$ evaluated at each frequency gives an exact test of robust stability against all $\Delta$ with that structure and a bound on the size ([mu analysis](/mu-analysis/)). The [spectral radius](/spectral-radius/) and the largest singular value are the two extreme cases of $\mu$. In general $\mu$ is hard to compute, so practical tools compute an upper and a lower bound.

## Definition

**Block structure.** Fix nonnegative integers $S$ and $F$, sizes $r_1, \ldots, r_S$ and $m_1, \ldots, m_F$ with $\sum r_i + \sum m_j = n$. The set of structured perturbations is

$$\boldsymbol\Delta = \{\mathrm{diag}(\delta_1 I_{r_1}, \ldots, \delta_S I_{r_S}, \Delta_1, \ldots, \Delta_F) : \delta_i \in \mathbb{C},\ \Delta_j \in \mathbb{C}^{m_j \times m_j}\}.$$

The $\delta_i I_{r_i}$ are repeated scalar blocks and the $\Delta_j$ are full blocks. A $1 \times 1$ block counts as a full block. Non-square full blocks are also allowed; they change only the notation.

**Structured singular value** (Doyle 1982). For $M \in \mathbb{C}^{n \times n}$,

$$\mu_{\boldsymbol\Delta}(M) = \frac{1}{\min\{\bar\sigma(\Delta) : \Delta \in \boldsymbol\Delta,\ \det(I - M \Delta) = 0\}},$$

and $\mu_{\boldsymbol\Delta}(M) = 0$ if no $\Delta \in \boldsymbol\Delta$ makes $I - M \Delta$ singular. Here $\bar\sigma$ is the largest singular value. So $\mu \ge \beta$ exactly when some $\Delta$ in the structure with $\bar\sigma(\Delta) \le 1/\beta$ makes $I - M \Delta$ singular.

**Real and mixed $\mu$.** If some $\delta_i$ must be real, the same formula defines the real or mixed $\mu$. Real parameters model uncertain physical constants; complex blocks model unmodeled dynamics.

**Basic facts** (Doyle 1982; Packard and Doyle 1993).

- If $\boldsymbol\Delta = \{\delta I_n : \delta \in \mathbb{C}\}$, then $\mu(M) = \rho(M)$, the spectral radius.
- If $\boldsymbol\Delta = \mathbb{C}^{n \times n}$, then $\mu(M) = \bar\sigma(M)$.
- For every complex structure, $\rho(M) \le \mu(M) \le \bar\sigma(M)$, and $\mu(\alpha M) = |\alpha|\,\mu(M)$. But $\mu$ is not a norm: it can be 0 for $M \ne 0$, and it can fail the triangle inequality.

**The bounds that are used.** Let $\mathcal{U}$ be the unitary matrices in $\boldsymbol\Delta$, and let $\mathcal{D}$ be the matrices $\mathrm{diag}(D_1, \ldots, D_S, d_1 I_{m_1}, \ldots, d_F I_{m_F})$ with $D_i = D_i^* > 0$ of size $r_i$ and $d_j > 0$. Each $D \in \mathcal{D}$ commutes with each $\Delta \in \boldsymbol\Delta$. Then

$$\max_{U \in \mathcal{U}} \rho(M U) = \mu(M) \le \inf_{D \in \mathcal{D}} \bar\sigma(D M D^{-1}).$$

The left equality is a theorem, but the function $\rho(M U)$ can have local maxima that are not global, so a local search gives only a lower bound. The right side is a convex problem: $\bar\sigma(D M D^{-1}) < \beta$ holds exactly when $M^* X M - \beta^2 X < 0$ for $X = D^* D$, a [linear matrix inequality](/linear-matrix-inequality/) in $X$ for fixed $\beta$.

**When the upper bound is exact** (Packard and Doyle 1993). The upper bound equals $\mu$ for every $M$ if and only if $2S + F \le 3$. So it is exact for up to three full blocks (Doyle 1982), or one repeated scalar block and one full block. For larger structures there are matrices with a gap between the bound and $\mu$.

**Complexity.** Computing $\mu$ exactly is [NP-hard](/np-hard/) for real and for mixed real and complex structures (Braatz, Young, Doyle and Morari 1994), and also for some purely complex structures (Toker and Ozbay 1998). So no polynomial algorithm for exact $\mu$ is expected, and practical codes compute the two bounds. For mixed structures, Fan, Tits and Doyle (1991) give an upper bound with an extra scaling $G$ for the real blocks, again an LMI.

## Examples and non-examples

**Equal bounds.** Let $M = \begin{bmatrix} 1 & 4 \\ 1 & 1 \end{bmatrix}$ and $\boldsymbol\Delta = \{\mathrm{diag}(\delta_1, \delta_2)\}$, two $1 \times 1$ blocks, so $F = 2$ and the D bound is exact. The eigenvalues of $M$ are 3 and $-1$, so $\rho(M) = 3$. The unscaled bound is $\bar\sigma(M) = \sqrt{(19 + \sqrt{325})/2} = 4.3028$. With $D = \mathrm{diag}(d, 1)$, $D M D^{-1} = \begin{bmatrix} 1 & 4/d \\ d & 1 \end{bmatrix}$, and $d = 2$ makes it the symmetric matrix $\begin{bmatrix} 1 & 2 \\ 2 & 1 \end{bmatrix}$ with $\bar\sigma = 3$. So $3 \le \mu(M) \le 3$, and $\mu(M) = 3$. The perturbation $\Delta = \mathrm{diag}(1/3, 1/3)$ has $\bar\sigma(\Delta) = 1/3$ and $\det(I - M\Delta) = 0$, because 3 is an eigenvalue of $M$. The scaling cut the bound by 30 percent.

**Mu can be 0.** Let $M = \begin{bmatrix} 0 & a \\ 0 & 0 \end{bmatrix}$ with $a \ne 0$ and the same diagonal structure. Then $M \Delta = \begin{bmatrix} 0 & a \delta_2 \\ 0 & 0 \end{bmatrix}$ is nilpotent, so $\det(I - M \Delta) = 1$ for every diagonal $\Delta$, and $\mu(M) = 0$, while $\bar\sigma(M) = |a|$. With $D = \mathrm{diag}(d, 1)$, $\bar\sigma(D M D^{-1}) = |a| d$, which tends to 0 as $d \to 0$. So the infimum in the upper bound is 0 but no $D$ reaches it. In a loop, the two uncertain channels do not form a cycle through $M$, so no size of diagonal uncertainty can destabilize it. For a full $2 \times 2$ block, $\mu(M) = \bar\sigma(M) = |a|$: a full block can close the cycle.

**One repeated scalar.** For $\boldsymbol\Delta = \{\delta I_2\}$ and the same nilpotent $M$, $\mu(M) = \rho(M) = 0$. A repeated scalar models one uncertain parameter that appears in two places, and here it cannot destabilize.

**A non-example: the plain singular value.** The test $\bar\sigma(M(j\omega)) < 1$ is the [small gain theorem](/small-gain-theorem/) for a full block. For a diagonal $\Delta$ it is only sufficient. In the first example it would allow perturbations up to $1/4.3028 = 0.232$ in size, while the true limit is $1/3 = 0.333$.

## Related definitions

- **Mu analysis.** For $M(s) \in RH_\infty$ and structured $\Delta(s) \in RH_\infty$ with $\|\Delta\|_\infty < 1/\beta$, the loop is internally stable for all such $\Delta$ if and only if $\sup_\omega \mu(M(j\omega)) \le \beta$ (theorem; Zhou, Doyle and Glover 1996, chapter 11). Robust performance is the same test with one more full block. See [mu analysis](/mu-analysis/).
- **Mu synthesis.** The search for a controller that makes the peak of $\mu$ small. The usual heuristic is [D-K iteration](/dk-iteration/), which alternates H-infinity synthesis with a fit of the D scalings.
- **Multivariable stability margin.** Safonov's $k_m(M) = 1/\mu(M)$, the size of the smallest destabilizing structured perturbation.
- **Lower bound by power iteration.** Packard, Fan and Doyle (1988) gave a [power iteration](/power-iteration/) for $\max_U \rho(M U)$. It is fast and usually tight, but has no guarantee of convergence to the global maximum.
- **Model uncertainty.** The block structure comes from how each uncertain element enters the plant. See [model uncertainty](/model-uncertainty/).

## References
