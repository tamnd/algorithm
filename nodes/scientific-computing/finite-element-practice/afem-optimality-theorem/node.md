---
tag: M20MET
kind: theorem
slug: afem-optimality-theorem
name: Optimality of adaptive finite element methods
aliases:
- AFEM convergence theorem
area: scientific-computing/finite-element-practice
level: research
summary: For symmetric elliptic problems with exact solves, small theta, minimal Dorfler sets and newest vertex bisection, AFEM converges at the best rate of the approximation class.
prereqs: [adaptive-finite-element-method, dorfler-marking, newest-vertex-bisection]
see_also: [residual-error-estimator, cea-lemma, galerkin-method, finite-element-method, poisson-equation, hp-finite-element-method, adaptive-mesh-refinement]
sources:
  - paper: doi:10.1137/07069047X
    title: J. Manuel Cascon, Christian Kreuzer, Ricardo H. Nochetto and Kunibert G. Siebert, Quasi-optimal convergence rate for an adaptive finite element method, SIAM Journal on Numerical Analysis 46(5) (2008) 2524-2550
    locator: the contraction of the error plus the scaled estimator, the optimal marking lemma and the quasi-optimal rate for the total error
  - paper: doi:10.1007/s10208-005-0183-0
    title: Rob Stevenson, Optimality of a standard adaptive finite element method, Foundations of Computational Mathematics 7(2) (2007) 245-269
    locator: the discrete upper bound and the first optimality proof without coarsening
  - paper: doi:10.1007/s00211-003-0492-7
    title: Peter Binev, Wolfgang Dahmen and Ronald DeVore, Adaptive finite element methods with convergence rates, Numerische Mathematik 97(2) (2004) 219-268
    locator: the closure estimate for newest vertex bisection and the first optimal rate, with coarsening
  - paper: doi:10.1007/s00365-013-9192-4
    title: Michael Karkulik, David Pavlicek and Dirk Praetorius, On 2D newest vertex bisection, optimality of mesh-closure and H1-stability of L2-projection, Constructive Approximation 38(2) (2013) 213-234
    locator: the closure estimate in 2D for an arbitrary initial labeling
  - paper: doi:10.1016/j.camwa.2013.12.003
    title: Carsten Carstensen, Michael Feischl, Marcus Page and Dirk Praetorius, Axioms of adaptivity, Computers and Mathematics with Applications 67(6) (2014) 1195-1253
    locator: the four axioms (stability, reduction, discrete reliability, quasi-orthogonality) that give linear convergence and optimal rates
  - paper: doi:10.1007/978-3-642-03413-8_12
    title: "Ricardo H. Nochetto, Kunibert G. Siebert and Andreas Veeser, Theory of adaptive finite element methods: an introduction, in Multiscale, Nonlinear and Adaptive Approximation, Springer, 2009, 409-542"
    locator: the full proof for the model problem, with the approximation classes and the cost of the loop
---

The AFEM optimality theorem says that the simple adaptive loop SOLVE, ESTIMATE, MARK, REFINE is as good as the best possible choice of meshes, up to a constant. Fix a rate $s > 0$. If the solution can be approximated with error $O(N^{-s})$ on some sequence of meshes with $N$ elements, made by [newest vertex bisection](/newest-vertex-bisection/) from the initial mesh, then the [adaptive finite element method](/adaptive-finite-element-method/) also reaches error $O(N^{-s})$, although it does not know $s$ or the good meshes. The hypotheses are a symmetric elliptic problem, exact discrete solves, the [residual estimator](/residual-error-estimator/), [Dorfler marking](/dorfler-marking/) with a small enough parameter $\theta$ and a marked set of nearly minimal size, and newest vertex bisection with a suitable initial mesh. The form below is the theorem of Cascon, Kreuzer, Nochetto and Siebert (2008).

## Statement

**Setting.** Let $\Omega \subset \mathbb{R}^d$, $d \ge 2$, be a polyhedral domain, and consider $-\nabla\cdot(A\nabla u) = f$ in $\Omega$ with $u = 0$ on $\partial\Omega$, where $A$ is symmetric, uniformly positive definite and piecewise Lipschitz on the initial mesh $\mathcal{T}_0$, and $f \in L^2(\Omega)$. Let $|v| = (A\nabla v, \nabla v)^{1/2}$ be the energy norm. For a conforming mesh $\mathcal{T}$ made by newest vertex bisection from $\mathcal{T}_0$, let $U_{\mathcal{T}}$ be the Galerkin solution with continuous piecewise polynomials of degree $n \ge 1$, let $\eta_{\mathcal{T}}(K)$ be the residual indicators with the weight $h_K = |K|^{1/d}$, and let $\mathrm{osc}_{\mathcal{T}}$ be the data oscillation. The **total error** is
$$\mathcal{E}_{\mathcal{T}}^2 = |u - U_{\mathcal{T}}|^2 + \mathrm{osc}_{\mathcal{T}}^2 .$$

**The loop.** Starting from $\mathcal{T}_0$, step $k$ computes $U_k$ exactly, computes the indicators $\eta_k(K)$, selects a set $\mathcal{M}_k$ with $\sum_{K \in \mathcal{M}_k}\eta_k(K)^2 \ge \theta\sum_{K \in \mathcal{T}_k}\eta_k(K)^2$ whose size is at most a fixed constant times the minimal size, and bisects every marked element at least once, with the closure that keeps the mesh conforming.

**Approximation class.** For $s > 0$, the data $(u, f, A)$ is in $\mathbb{A}_s$ if
$$|(u, f, A)|_s = \sup_{N > 0} N^s\min_{\#\mathcal{T} - \#\mathcal{T}_0 \le N}\ \inf_{V \in \mathbb{V}_{\mathcal{T}}}\big(|u - V|^2 + \mathrm{osc}_{\mathcal{T}}(V)^2\big)^{1/2} < \infty ,$$
where the minimum is over the meshes made by newest vertex bisection from $\mathcal{T}_0$.

**Theorem (Cascon, Kreuzer, Nochetto and Siebert, 2008).** Assume that the initial mesh has a labeling for which the closure estimate below holds. There is a $\theta^* \in (0, 1)$, which depends only on the shape regularity of the meshes, the degree $n$ and the coefficient $A$, such that for every $\theta \in (0, \theta^*)$:

1. **Contraction.** There are $\gamma > 0$ and $\alpha \in (0, 1)$ with
$$|u - U_{k+1}|^2 + \gamma\eta_{k+1}^2 \le \alpha^2\big(|u - U_k|^2 + \gamma\eta_k^2\big) \quad \text{for all } k .$$
2. **Optimal rate.** If $(u, f, A) \in \mathbb{A}_s$, then
$$\mathcal{E}_{\mathcal{T}_k} \le C\,|(u, f, A)|_s\,(\#\mathcal{T}_k - \#\mathcal{T}_0)^{-s} \quad \text{for all } k \ge 1,$$
with $C$ that depends on $s$, $\theta$, $\mathcal{T}_0$, the shape regularity, $n$ and $A$, but not on $u$ or $k$.

The contraction holds for every $\theta \in (0, 1]$. Only the rate needs the bound $\theta < \theta^*$ and the nearly minimal marked sets.

## In plain words

Think of the best meshes as a list made by someone who knows the exact solution. For each budget of $N$ elements they choose the mesh with the smallest error. The theorem says that the adaptive loop, which only sees the computed solution and its residuals, keeps up with this list: its error at $N$ elements is at most a constant times the error of the best mesh with about $N$ elements. Two facts make this work. First, the error plus the estimator shrinks by a fixed factor in each step, so the loop never wastes many steps. Second, a modest $\theta$ and a smallest marked set mean that each step refines no more elements than the best mesh would need for the same improvement.

## Proof

The proof has four steps. Write $e_k = |u - U_k|^2$ and $\eta_k^2 = \sum_{K \in \mathcal{T}_k}\eta_k(K)^2$.

**Step 1, contraction.** The spaces are nested, so Galerkin orthogonality gives the Pythagoras identity $e_{k+1} = e_k - |U_{k+1} - U_k|^2$ for a symmetric problem. Each marked element is bisected at least once, so its $h_K$ shrinks by the factor $2^{-1/d}$, and this gives the **estimator reduction**: for every $\delta > 0$,
$$\eta_{k+1}^2 \le (1 + \delta)\big(\eta_k^2 - \lambda\eta_k(\mathcal{M}_k)^2\big) + (1 + \delta^{-1})C_{\mathrm{est}}|U_{k+1} - U_k|^2, \qquad \lambda = 1 - 2^{-1/d} .$$
With Dorfler marking, $\eta_k(\mathcal{M}_k)^2 \ge \theta\eta_k^2$. Take $\gamma = 1/((1 + \delta^{-1})C_{\mathrm{est}})$, so that the terms with $|U_{k+1} - U_k|^2$ cancel:
$$e_{k+1} + \gamma\eta_{k+1}^2 \le e_k + \gamma(1 + \delta)(1 - \lambda\theta)\eta_k^2 .$$
Reliability, $e_k \le C_{\mathrm{rel}}^2\eta_k^2$, allows us to move a small part $\beta e_k$ to the estimator side: the right side is at most $(1 - \beta)e_k + \gamma\big((1 + \delta)(1 - \lambda\theta) + \beta C_{\mathrm{rel}}^2/\gamma\big)\eta_k^2$. Choose $\delta$ so that $(1 + \delta)(1 - \lambda\theta) < 1$, and then $\beta$ small. Both factors are less than 1, and their maximum is $\alpha^2$.

**Step 2, optimal marking.** Let $\mathcal{T}_*$ be any refinement of $\mathcal{T}_k$ with $\mathcal{E}_{\mathcal{T}_*}^2 \le \mu\,\mathcal{E}_{\mathcal{T}_k}^2$ for a fixed small $\mu$. Let $\mathcal{R}$ be the set of elements of $\mathcal{T}_k$ that are refined in $\mathcal{T}_*$. **Discrete reliability**, found by Stevenson, says that $|U_* - U_k|^2 \le C_{\mathrm{drel}}^2\sum_{K \in \mathcal{R}}\eta_k(K)^2$: the change of the discrete solution is controlled by the indicators on the refined elements only. Together with the lower bound $\eta_k^2 \le C_{\mathrm{eff}}^2\mathcal{E}_{\mathcal{T}_k}^2$ and the stability of the oscillation, this gives $\sum_{K \in \mathcal{R}}\eta_k(K)^2 \ge \theta\eta_k^2$ whenever $\theta < \theta^*$. So $\mathcal{R}$ satisfies the Dorfler property. This is the step that needs $\theta$ small.

**Step 3, counting the marked elements.** Let $\varepsilon^2 = \mu\,\mathcal{E}_{\mathcal{T}_k}^2$ up to a constant. Because $(u, f, A) \in \mathbb{A}_s$, there is a mesh $\mathcal{T}_\varepsilon$ with $\#\mathcal{T}_\varepsilon - \#\mathcal{T}_0 \le |(u, f, A)|_s^{1/s}\varepsilon^{-1/s}$ and total error at most $\varepsilon$. Let $\mathcal{T}_*$ be the smallest common refinement of $\mathcal{T}_k$ and $\mathcal{T}_\varepsilon$. For bisection meshes, $\#\mathcal{T}_* \le \#\mathcal{T}_k + \#\mathcal{T}_\varepsilon - \#\mathcal{T}_0$. The total error is quasi-optimal for the Galerkin solution, by a [Céa type](/cea-lemma/) argument, and it does not grow under refinement up to a constant, so $\mathcal{T}_*$ satisfies the hypothesis of Step 2. Then $\mathcal{R}$ is a Dorfler set, and the marked set, which is nearly minimal, satisfies
$$\#\mathcal{M}_k \le C\#\mathcal{R} \le C(\#\mathcal{T}_* - \#\mathcal{T}_k) \le C|(u, f, A)|_s^{1/s}\,\mathcal{E}_{\mathcal{T}_k}^{-1/s} .$$

**Step 4, closure and the geometric series.** The closure estimate of Binev, Dahmen and DeVore says that the conforming closure of newest vertex bisection does not cost too much in total:
$$\#\mathcal{T}_k - \#\mathcal{T}_0 \le C_{\mathrm{cl}}\sum_{j=0}^{k-1}\#\mathcal{M}_j .$$
Let $Q_j = e_j + \gamma\eta_j^2$ be the quasi error. By reliability, efficiency and the bound $\mathrm{osc} \le \eta$, $Q_j$ is equivalent to $\mathcal{E}_{\mathcal{T}_j}^2$. The contraction gives $Q_j \ge \alpha^{-2(k-j)}Q_k$, so
$$\#\mathcal{T}_k - \#\mathcal{T}_0 \le C\sum_{j=0}^{k-1}Q_j^{-1/(2s)} \le C\,Q_k^{-1/(2s)}\sum_{j=0}^{k-1}\alpha^{(k-j)/s} \le \frac{C}{1 - \alpha^{1/s}}\,Q_k^{-1/(2s)} .$$
Solve for $Q_k$: $\mathcal{E}_{\mathcal{T}_k} \le CQ_k^{1/2} \le C|(u, f, A)|_s(\#\mathcal{T}_k - \#\mathcal{T}_0)^{-s}$. $\blacksquare$

**The geometric series, by hand.** Take $\alpha^2 = \tfrac14$, $s = \tfrac12$, $Q_0 = 1$, closure constant 1, and assume the worst case allowed by Steps 1 and 3: $Q_k = 4^{-k}$ and $\#\mathcal{M}_k = 3Q_k^{-1} = 3\cdot4^k$.

| $k$ | $Q_k$ | $\#\mathcal{M}_k$ | $\#\mathcal{T}_k - \#\mathcal{T}_0 \le \sum_{j<k}\#\mathcal{M}_j$ | $Q_k^{1/2}$ | $(\#\mathcal{T}_k - \#\mathcal{T}_0)^{-1/2}$ |
|---|---|---|---|---|---|
| 1 | $\tfrac14$ | 12 | 3 | 0.500 | 0.577 |
| 2 | $\tfrac1{16}$ | 48 | 15 | 0.250 | 0.258 |
| 3 | $\tfrac1{64}$ | 192 | 63 | 0.125 | 0.126 |
| 4 | $\tfrac1{256}$ | 768 | 255 | 0.0625 | 0.0626 |

The sum is $4^k - 1$, so $Q_k^{1/2} = 2^{-k} \le (4^k - 1)^{-1/2}$ for every $k$. Each step marks more elements than all earlier steps together, so the last term of the sum dominates, and the total count stays within the constant $\tfrac1{1 - \alpha^{1/s}} = \tfrac43$ of the last term. That is why a contraction by a fixed factor turns the bound for one step into a bound for the whole run.

## Consequences

- **The L-shaped domain.** For P1 elements in 2D, the solution with the corner singularity $r^{2/3}\sin(2\phi/3)$ is in $\mathbb{A}_{1/2}$, which is the rate for smooth solutions, while uniform refinement gives only $N^{-1/3}$. The theorem predicts the error $N^{-1/2}$ for AFEM, and the reference run on the [AFEM](/adaptive-finite-element-method/) page shows this rate.
- **No extra steps.** The standard loop needs no coarsening step, no separate marking for the oscillation and no interior node in each refined element. Earlier proofs needed one or more of these.
- **Linear convergence.** The contraction alone, which holds for all $\theta \in (0, 1]$, gives $Q_k \le \alpha^{2k}Q_0$: the error falls geometrically in the number of steps.
- **Axioms of adaptivity.** Carstensen, Feischl, Page and Praetorius showed that the proof uses only four properties of the estimator: stability on unrefined elements, reduction on refined ones, discrete reliability and a general quasi-orthogonality. Any method with these properties has the same theorem, which covers nonsymmetric problems, nonconforming and mixed methods and boundary element methods.
- **Choosing $\theta$.** The theorem supports moderate values of $\theta$. Values that are too large make the loop close to uniform refinement, which loses the rate.

## Tightness

- **The rate cannot exceed the class.** The theorem compares AFEM with the best meshes. For degree $n$ in dimension $d$, no sequence of meshes gives a better rate than $N^{-n/d}$ for a generic solution, so $s \le n/d$ in practice.
- **$\theta$ cannot be too large.** With $\theta = 1$ every element is marked, AFEM is uniform refinement, and on the L-shaped domain the rate drops from $N^{-1/2}$ to $N^{-1/3}$, measured on the [Dorfler marking](/dorfler-marking/) page. So the rate needs a bound on $\theta$. The value $\theta^*$ from the proof is small and pessimistic, and in practice larger values also give the optimal rate.
- **The marked sets must be nearly minimal.** A marking that adds many elements beyond a Dorfler set satisfies the contraction but can lose the rate. A constant factor is allowed, which covers the linear time marking by binning of Stevenson.
- **Exact solves and symmetry.** The Pythagoras identity uses Galerkin orthogonality in the energy norm. For an inexact solver, a stopping rule tied to the estimator is needed. For nonsymmetric problems, the identity becomes a quasi-orthogonality that holds only for fine meshes.
- **The initial mesh matters.** The closure estimate of Binev, Dahmen and DeVore needs a compatible labeling of $\mathcal{T}_0$ in 2D. Stevenson extended it to all dimensions under a condition on $\mathcal{T}_0$, and Karkulik, Pavlicek and Praetorius removed the condition in 2D. Without a closure estimate, the count in Step 4 fails.
- **The constant is not computed.** $C$ depends on $\theta$, $s$, $\mathcal{T}_0$ and the constants of the estimator. The theorem is about the rate, not about the size of the error at a given $N$.

## History

Willy Dorfler proved the first convergence of the adaptive loop in 1996, with bulk marking and a fine initial mesh. Pedro Morin, Ricardo Nochetto and Kunibert Siebert proved convergence in 2000 without the condition on the initial mesh, with oscillation marking and an interior node in each refined element. Peter Binev, Wolfgang Dahmen and Ronald DeVore proved the first optimal rate in 2004, with a coarsening step, and their closure estimate for newest vertex bisection is used in all later proofs. Rob Stevenson showed in 2007 that coarsening is not needed, using the discrete upper bound. Manuel Cascon, Christian Kreuzer, Nochetto and Siebert proved in 2008 the form above, with the contraction of the quasi error and marking by the estimator alone, for symmetric problems with variable coefficients in any dimension. The survey of Nochetto, Siebert and Andreas Veeser (2009) gives the full theory, and the axioms of adaptivity of Carsten Carstensen, Michael Feischl, Marcus Page and Dirk Praetorius (2014) put the many later extensions into one framework.

## References
