---
tag: 08RYR5
kind: theorem
slug: lax-equivalence-theorem
name: Lax equivalence theorem
aliases:
- Lax-Richtmyer equivalence theorem
- Lax-Richtmyer theorem
area: numerical/differential-equations
level: advanced
summary: "For a consistent difference scheme for a well-posed linear initial value problem, convergence is equivalent to stability: uniform boundedness of the powers of the one-step operator."
prereqs: [consistency, finite-difference-method, heat-equation]
see_also: [von-neumann-stability-analysis, dahlquist-equivalence-theorem, courant-friedrichs-lewy-condition, ftcs-method, lax-friedrichs-scheme, lax-wendroff-method, gronwall-inequality, order-of-accuracy]
sources:
  - paper: doi:10.1002/cpa.3160090206
    title: P. D. Lax and R. D. Richtmyer, Survey of the stability of linear finite difference equations, Communications on Pure and Applied Mathematics 9 (1956) 267-293
  - book: isbn:9780898715675
    title: John C. Strikwerda, Finite Difference Schemes and Partial Differential Equations, second edition, SIAM, 2004
    locator: Chapter 1 (consistency and stability), Chapter 2 (von Neumann analysis) and Chapter 10 (the Lax-Richtmyer equivalence theorem and convergence estimates)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 9 (Lax-Richtmyer stability and the Lax equivalence theorem for the heat equation) and Chapter 10 (advection)
  - book: isbn:9780521607933
    title: K. W. Morton and D. F. Mayers, Numerical Solution of Partial Differential Equations, second edition, Cambridge University Press, 2005
    locator: Chapter 5 (consistency, convergence and stability; the Lax equivalence theorem)
---

The Lax equivalence theorem is the basic convergence theorem for finite difference methods for linear partial differential equations. For a linear evolution problem that is well posed, and a difference scheme that is consistent with it, the scheme converges for every initial value if and only if it is stable, meaning that the powers of its one-step operator stay bounded as the grid is refined. Consistency is usually a short Taylor expansion and stability can often be checked mode by mode with [von Neumann analysis](/von-neumann-stability-analysis/), so the theorem turns the hard question of convergence into two easier ones. It is the PDE counterpart of the [Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/) for multistep methods.

## Statement

**Setting.** Let $B$ be a Banach space (for example $L^2$ of the spatial domain) and consider the linear initial value problem $u_t = \mathcal{A}u$, $u(0) = u_0$, on $[0, T]$. The problem is *well posed*: there are solution operators $S(t)$, $0 \le t \le T$, bounded and linear, with $\sup_{t \le T}\|S(t)\| = K_S < \infty$, such that $t \mapsto S(t)u_0$ is continuous for every $u_0 \in B$ and is a classical solution for $u_0$ in a dense subspace $D \subset B$.

A difference scheme is a family of bounded linear operators $C(\Delta t)$ on $B$, $0 < \Delta t < \tau_0$, with the mesh width tied to the time step by a fixed refinement path such as $\Delta x = \Delta t/\lambda$ or $\Delta x = \sqrt{\Delta t/\mu}$; one step is $U^{n+1} = C(\Delta t)U^n$.

- **Consistency.** For every $u_0 \in D$, with $u(t) = S(t)u_0$,
$$\sup_{0 \le t \le T - \Delta t} \frac{\|C(\Delta t)u(t) - u(t + \Delta t)\|}{\Delta t} \to 0 \quad (\Delta t \to 0).$$
- **Stability.** There are $\tau > 0$ and $K$ with $\|C(\Delta t)^n\| \le K$ for all $0 < \Delta t < \tau$ and all $n$ with $n\Delta t \le T$.
- **Convergence.** For every $u_0 \in B$, every $t \in [0, T]$, and all sequences $\Delta t_j \to 0$ and $n_j$ with $n_j\Delta t_j \to t$: $\|C(\Delta t_j)^{n_j}u_0 - S(t)u_0\| \to 0$.

**Theorem (Lax and Richtmyer, 1956).** A consistent scheme for a well-posed linear initial value problem is convergent if and only if it is stable.

**Addendum (rate).** If the scheme is stable with constant $K$ and the consistency error for the solution from $u_0$ is at most $c\,\Delta t^{p+1}$ per step, then $\|C(\Delta t)^n u_0 - u(t_n)\| \le K c\, t_n\, \Delta t^p$. With a refinement path $\Delta t \propto \Delta x$ or $\Delta t \propto \Delta x^2$ this is the order of the scheme in space as well.

## In plain words

A numerical method for an evolving system makes a small error in every step, and then carries all earlier errors forward. Two things must hold for the answer to get better as the grid gets finer. Each single step must be nearly right; this is consistency. And the method must not blow up the errors it carries forward, no matter how many small steps it takes; this is stability.

The theorem says that for linear problems these two are not just enough but also necessary. If a consistent method is unstable, some starting data exist for which the computed answer does not approach the truth, however fine the grid. In practice rounding errors supply such data by themselves.

## Proof

**Stability and consistency imply convergence.** First let $u_0 \in D$ and $u(t) = S(t)u_0$, and write $t_k = k\Delta t$ and $C = C(\Delta t)$. The global error after $n$ steps telescopes:

$$C^n u_0 - u(t_n) = \sum_{k=0}^{n-1} C^{n-1-k}\bigl(Cu(t_k) - u(t_{k+1})\bigr),$$

because the sum is $\sum_k (C^{n-k}u(t_k) - C^{n-1-k}u(t_{k+1}))$, whose terms cancel in pairs except $C^n u(t_0) - u(t_n)$. Stability bounds each $\|C^{n-1-k}\|$ by $K$, and consistency bounds each defect by $\Delta t\,\varepsilon(\Delta t)$ with $\varepsilon(\Delta t) \to 0$. Hence

$$\|C^n u_0 - u(t_n)\| \le K\, n\Delta t\, \varepsilon(\Delta t) \le K T \varepsilon(\Delta t). \tag{1}$$

Now take sequences $\Delta t_j \to 0$ and $n_j\Delta t_j \to t$. By (1) and the continuity of $s \mapsto S(s)u_0$, $\|C(\Delta t_j)^{n_j}u_0 - S(t)u_0\| \le KT\varepsilon(\Delta t_j) + \|S(n_j\Delta t_j)u_0 - S(t)u_0\| \to 0$. For a general $u_0 \in B$ and $\eta > 0$ pick $v_0 \in D$ with $\|u_0 - v_0\| \le \eta$ (density). Then

$$\|C^{n_j}u_0 - S(t)u_0\| \le \|C^{n_j}(u_0 - v_0)\| + \|C^{n_j}v_0 - S(t)v_0\| + \|S(t)(v_0 - u_0)\| \le K\eta + o(1) + K_S\eta.$$

So the $\limsup$ is at most $(K + K_S)\eta$ for every $\eta > 0$, which is convergence. The same calculation with a defect $c\,\Delta t^{p+1}$ gives the addendum.

**Convergence implies stability.** Suppose the scheme converges but is not stable. Then for every $j$ (taking $\tau = 1/j$ in the definition) there are $\Delta t_j < 1/j$ and $n_j$ with $n_j\Delta t_j \le T$ and $\|C(\Delta t_j)^{n_j}\| > j$. Passing to a subsequence, $n_j\Delta t_j \to t \in [0, T]$. For every $u_0 \in B$ the sequence $C(\Delta t_j)^{n_j}u_0$ converges to $S(t)u_0$, so it is bounded. By the uniform boundedness principle (Banach-Steinhaus), a family of bounded linear operators on a Banach space that is bounded at every point is bounded in operator norm: $\sup_j \|C(\Delta t_j)^{n_j}\| < \infty$. This contradicts $\|C(\Delta t_j)^{n_j}\| > j$. $\blacksquare$

The second half does not use consistency. Both halves are proved here in full, given the uniform boundedness principle, a standard theorem of functional analysis.

## Consequences

- **Convergence proofs reduce to two checks.** For a constant-coefficient scheme on a periodic grid, $C(\Delta t)$ is diagonalised by the discrete Fourier transform, and in $L^2$ stability means $|g(\theta)|^n \le K$ for the amplification factor, which holds exactly when $|g(\theta)| \le 1 + c\Delta t$ (the von Neumann condition). This is how the CFL limits $|\nu| \le 1$ of the [Lax-Friedrichs](/lax-friedrichs-scheme/) and [Lax-Wendroff](/lax-wendroff-method/) schemes and $\mu = \Delta t/\Delta x^2 \le \frac12$ of [FTCS](/ftcs-method/) for the [heat equation](/heat-equation/) are turned into convergence theorems.
- **Instability means failure, not just inaccuracy.** For FTCS on $u_t = u_{xx}$, $u_0 = \sin\pi x$ on $[0, 1]$ with zero boundary values and $T = 0.1$, the max errors at $\Delta x = 1/10, 1/20, 1/40, 1/80, 1/160$ are, for $\mu = 0.5$: $6.2 \cdot 10^{-3}$, $1.5 \cdot 10^{-3}$, $3.8 \cdot 10^{-4}$, $9.5 \cdot 10^{-5}$, $2.4 \cdot 10^{-5}$; for $\mu = 0.51$: $6.4 \cdot 10^{-3}$, $1.6 \cdot 10^{-3}$, $3.9 \cdot 10^{-4}$, $1.9 \cdot 10^{4}$, $3.9 \cdot 10^{67}$. The data contain only the smooth mode, but rounding errors excite the mode with $g = 1 - 4\mu = -1.04$, which grows by $1.04^{1255}$ in 1255 steps. This is an observed run in double precision.
- **Stability depends on the refinement path.** The centred FTCS scheme for $u_t + u_x = 0$ has $|g(\theta)|^2 = 1 + \nu^2\sin^2\theta > 1$. At fixed $\nu = 0.5$ it is unstable: with $u_0 = \sin 2\pi x$, $T = 1$ and $\Delta x = 1/10, \dots, 1/640$ the max errors are $1.54$, $0.63$, $0.28$, $0.13$, $0.38$, $9.5 \cdot 10^{14}$, $5.4 \cdot 10^{45}$. Along the path $\Delta t = \Delta x^2$ it is stable, since $|g|^{2n} \le (1 + \Delta x^2)^{T/\Delta x^2} \le e^{T}$, and the errors are $0.48$, $0.12$, $0.029$, $0.0072$ for $\Delta x = 1/10, \dots, 1/80$: order 2 in $\Delta x$, as the addendum predicts.
- **Order of convergence equals order of consistency** for stable schemes and smooth data, by the addendum. For data that are not smooth (only in $B$), convergence holds but without a rate.
- **Analogue for ODEs.** For linear multistep methods, stability in the sense of the theorem is [zero-stability](/zero-stability/), and the [Dahlquist equivalence theorem](/dahlquist-equivalence-theorem/) is the corresponding statement, proved there for nonlinear $f$ as well.

## Tightness

- **Linearity.** The proof uses $C^n u_0 - C^n v_0 = C^n(u_0 - v_0)$ and the uniform boundedness principle, both linear tools. For nonlinear conservation laws, consistent and stable schemes in conservation form converge (when they do) to weak solutions, but not necessarily to the right one: an upwind scheme with Roe's speed applied to Burgers' equation with $u = -1$ left and $u = 1$ right of $0$ keeps the entropy-violating stationary step forever. Nonlinear theory needs extra structure, such as monotonicity.
- **Well-posedness.** For the backward heat equation $u_t = -u_{xx}$ the solution operators are unbounded, and no consistent scheme can converge for all data in $L^2$; the theorem does not apply.
- **The norm.** Stability and convergence refer to the same norm $\|\cdot\|$. A scheme stable in $L^2$ need not be stable in the max norm; the Lax-Wendroff scheme is a contraction in $L^2$ but not in the max norm.
- **Consistency is needed for sufficiency.** $C(\Delta t) = I$ is stable and converges to the wrong limit for any non-stationary problem.
- **The constant.** Stability allows growth like $e^{ct}$, not only $\|C\| \le 1$; requiring $\|C(\Delta t)\| \le 1$ would exclude valid schemes for problems whose solutions grow.

## History

Lax found the theorem in the early 1950s at New York University; it was published with Richtmyer in the 1956 survey "Survey of the stability of linear finite difference equations", which also set out the framework of a Banach space, a dense set of genuine solutions and families of difference operators. Richtmyer's 1957 book (with Morton's 1967 second edition) made it the standard starting point for the analysis of difference schemes. The CFL paper of 1928 had already identified the domain-of-dependence condition; von Neumann's Fourier method, developed at Los Alamos in the 1940s, became the practical test for stability. Kreiss (1962) characterised power boundedness for families of matrices (the Kreiss matrix theorem), which matters when the amplification matrices of a system are not normal and the von Neumann condition is not sufficient.

## References
