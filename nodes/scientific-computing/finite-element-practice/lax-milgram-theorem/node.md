---
tag: 6MJR1Z
kind: theorem
slug: lax-milgram-theorem
name: Lax-Milgram theorem
area: scientific-computing/finite-element-practice
level: core
summary: A bounded coercive bilinear form on a Hilbert space gives a unique solution of a(u, v) = l(v) for all v, bounded by the norm of l over the coercivity constant.
prereqs: [weak-formulation, sobolev-space]
see_also: [cea-lemma, galerkin-method, finite-element-method, inf-sup-condition, banach-fixed-point-theorem, positive-definite-matrix, poisson-equation]
sources:
  - paper: doi:10.1515/9781400882182-010
    title: P. D. Lax and A. N. Milgram, Parabolic equations, in Contributions to the Theory of Partial Differential Equations, Annals of Mathematics Studies 33, Princeton University Press, 1954, 167-190
  - book: isbn:9780387759333
    title: Susanne C. Brenner and L. Ridgway Scott, The Mathematical Theory of Finite Element Methods, third edition, Springer, 2008
    locator: Chapter 2 (the Lax-Milgram theorem and its use for variational problems)
  - book: isbn:9780821849743
    title: Lawrence C. Evans, Partial Differential Equations, second edition, Graduate Studies in Mathematics 19, American Mathematical Society, 2010
    locator: Chapter 6, Section 6.2 (existence of weak solutions and the Lax-Milgram theorem)
  - book: isbn:9780898715149
    title: Philippe G. Ciarlet, The Finite Element Method for Elliptic Problems, SIAM Classics in Applied Mathematics 40, 2002
    locator: Chapter 1 (abstract variational problems and the Lax-Milgram lemma)
---

The Lax-Milgram theorem is the basic existence and uniqueness theorem for linear [weak formulations](/weak-formulation/): if a bilinear form on a Hilbert space is bounded and coercive, then $a(u, v) = l(v)$ for all $v$ has exactly one solution $u$, and $\|u\| \le \|l\|/\alpha$. The form does not need to be symmetric, so the theorem also covers convection-diffusion problems that have no energy to minimize. Applied to a finite element subspace, the same theorem says that the stiffness matrix is nonsingular, and it is the first step of [Céa's lemma](/cea-lemma/).

## Statement

**Setting.** Let $V$ be a real Hilbert space with norm $\|\cdot\|$. Let $a : V \times V \to \mathbb{R}$ be bilinear and let $l : V \to \mathbb{R}$ be linear. Assume that there are constants $M$ and $\alpha > 0$ with

$$|a(u, v)| \le M \|u\|\,\|v\| \quad \text{(continuity)}, \qquad a(v, v) \ge \alpha \|v\|^2 \quad \text{(coercivity)}$$

for all $u, v \in V$, and that $l$ is bounded, with $\|l\|_{V'} = \sup_{v \ne 0} |l(v)|/\|v\| < \infty$.

**Theorem (Lax and Milgram, 1954).** There is exactly one $u \in V$ with

$$a(u, v) = l(v) \quad \text{for all } v \in V,$$

and it satisfies $\|u\| \le \|l\|_{V'}/\alpha$.

The map $l \mapsto u$ is therefore linear and bounded with norm at most $1/\alpha$: the problem is well posed. For complex Hilbert spaces the same holds for a sesquilinear $a$ with $\operatorname{Re} a(v, v) \ge \alpha\|v\|^2$.

## In plain words

Many physical problems ask for a state that balances given forces against every possible small test motion. The theorem gives two conditions under which exactly one such state exists. The first is that the response of the system to a state is never larger than a fixed multiple of the state. The second is that every state costs a positive amount of energy, at least a fixed fraction of its own size. Under these conditions the balance problem has one answer, and a small change in the forces gives only a small change in the answer. The response does not have to be the same in both directions, so flows that carry material along are included. The same theorem then applies to every finite element model of the problem, so its linear system can always be solved.

## Proof

**Step 1: an operator.** For a fixed $u$, the map $v \mapsto a(u, v)$ is linear and bounded by $M\|u\|$. The Riesz representation theorem gives one $Au \in V$ with $(Au, v) = a(u, v)$ for all $v$, and also one $\tau \in V$ with $(\tau, v) = l(v)$ and $\|\tau\| = \|l\|_{V'}$. Bilinearity makes $A$ linear, and $\|Au\| = \sup_v a(u,v)/\|v\| \le M\|u\|$. The weak problem is now the operator equation $Au = \tau$.

**Step 2: $A$ is bounded below.** For every $u$, coercivity and the Cauchy-Schwarz inequality give

$$\alpha\|u\|^2 \le a(u, u) = (Au, u) \le \|Au\|\,\|u\|, \qquad \text{so} \qquad \|Au\| \ge \alpha\|u\|.$$

Hence $A$ is one to one. Its range is closed: if $Au_n \to y$, then $\|u_n - u_m\| \le \|Au_n - Au_m\|/\alpha$, so $(u_n)$ is a Cauchy sequence with a limit $u$, and $Au = y$ because $A$ is bounded.

**Step 3: $A$ is onto.** Let $w$ be orthogonal to the range of $A$. Then $0 = (Aw, w) = a(w, w) \ge \alpha\|w\|^2$, so $w = 0$. A closed subspace whose orthogonal complement is $\{0\}$ is all of $V$.

**Step 4: the solution and its bound.** So $u = A^{-1}\tau$ exists and is unique. Take $v = u$ in the equation:

$$\alpha\|u\|^2 \le a(u, u) = l(u) \le \|l\|_{V'}\|u\|,$$

and divide by $\alpha\|u\|$ (the bound is trivial when $u = 0$). $\square$

**Second proof, by a contraction.** For $\rho > 0$ let $T(u) = u - \rho(Au - \tau)$. A fixed point of $T$ solves $Au = \tau$. With $e = u - w$,

$$\|T(u) - T(w)\|^2 = \|e\|^2 - 2\rho(Ae, e) + \rho^2\|Ae\|^2 \le (1 - 2\rho\alpha + \rho^2 M^2)\|e\|^2 .$$

For $0 < \rho < 2\alpha/M^2$ the factor is less than 1, so the [Banach fixed point theorem](/banach-fixed-point-theorem/) gives one fixed point. This proof does not use the orthogonal complement, and it also gives an iteration that converges to $u$.

## Consequences

**The model problem is well posed.** For $-\nabla\cdot(\kappa\nabla u) = f$ with $u = 0$ on $\Gamma_D$, $|\Gamma_D| > 0$ and $0 < \kappa_0 \le \kappa \le \kappa_1$, the [Friedrichs inequality](/sobolev-space/) gives coercivity on $V = \{v \in H^1 : v = 0 \text{ on } \Gamma_D\}$. So there is one weak solution, with $\|u\|_1 \le C\|f\|_0$.

**Symmetry is not needed.** On $H^1_0(0,1)$ take $a(u, v) = \int_0^1 u'v'\,dx + b\int_0^1 u'v\,dx$ with a constant $b$, the weak form of $-u'' + bu' = f$. Then $\int_0^1 v'v\,dx = \tfrac12[v^2]_0^1 = 0$, so $a(v, v) = |v|_1^2$ for every $b$. In the norm $|\cdot|_1$ this gives $\alpha = 1$ and $M = 1 + |b|/\pi$, by the Poincaré constant $1/\pi$. The form is not symmetric and has no energy, but the theorem applies.

**A two-dimensional check.** On $V = \mathbb{R}^2$ with the Euclidean norm, let $a(u, v) = v^\top A u$ with $A = \begin{pmatrix} 1 & 1 \\ -1 & 1\end{pmatrix}$ and $l(v) = v_1$. Then $u^\top A u = u_1^2 + u_2^2$, so $\alpha = 1$, and $A$ is $\sqrt2$ times a rotation, so $M = \sqrt2$. The equation is $Au = (1, 0)$, with the solution $u = (\tfrac12, \tfrac12)$. Its norm $1/\sqrt2$ is below the bound $\|l\|/\alpha = 1$.

**Galerkin systems are nonsingular.** Every subspace $V_h \subset V$ of finite dimension is closed and inherits $M$ and $\alpha$, so the [Galerkin](/galerkin-method/) problem on $V_h$ has one solution with $\|u_h\| \le \|l\|/\alpha$. In the basis $\phi_1, \ldots, \phi_N$ the stiffness matrix $A_{ij} = a(\phi_j, \phi_i)$ satisfies $x^\top A x = a(v_h, v_h) \ge \alpha\|v_h\|^2 > 0$ for $v_h = \sum_j x_j\phi_j \ne 0$. So $A$ is positive definite in this sense even if it is not symmetric, and it is a [symmetric positive definite matrix](/positive-definite-matrix/) when $a$ is symmetric.

**Céa's lemma.** Subtract the discrete equation from the continuous one and use the two constants again: $\|u - u_h\| \le (M/\alpha)\inf_{v_h \in V_h}\|u - v_h\|$. See [Céa's lemma](/cea-lemma/).

## Tightness

**Coercivity cannot be dropped.** On $V = H^1(0, 1)$ with no boundary condition, $a(u, v) = \int_0^1 u'v'\,dx$ is bounded and $a(v, v) \ge 0$, but $a(1, 1) = 0$. Every constant solves the homogeneous problem, and for $l(v) = \int_0^1 v\,dx$ the test function $v = 1$ gives $0 = 1$, so no solution exists.

**Indefinite forms can fail.** On $H^1_0(0, 1)$ take $a(u, v) = \int_0^1 u'v' - \pi^2\int_0^1 uv$, the Helmholtz operator at a resonance. Then $a(\sin\pi x, v) = 0$ for every $v$, so solutions are not unique, and for $l(v) = \int_0^1 \sin(\pi x)\, v\,dx$ no solution exists.

**Positivity is not coercivity.** On $V = \ell^2$ let $a(u, v) = \sum_n u_n v_n/n$. Then $a(v, v) > 0$ for $v \ne 0$, but no $\alpha > 0$ works. For $l(v) = \sum_n v_n/n$, which is bounded because $(1/n) \in \ell^2$, the equation forces $u_n = 1$ for all $n$, and that is not in $\ell^2$.

**The bound $1/\alpha$ is sharp.** For $a(u, v) = \alpha(u, v)$ the solution is $u = \tau/\alpha$, so $\|u\| = \|l\|/\alpha$ exactly.

**Coercivity is sufficient, not necessary.** On $H^1_0(0, 1)$ take $a(u, v) = \int_0^1 u'v' - 2\pi^2\int_0^1 uv$. It is not coercive, because $a(\sin\pi x, \sin\pi x) = (\pi^2 - 2\pi^2)/2 < 0$. But $2\pi^2$ is not an eigenvalue $n^2\pi^2$ of $-u''$, so the problem has exactly one solution for every $l$. The Stokes problem in velocity-pressure form is another well-posed problem that is not coercive. The exact condition is an [inf-sup condition](/inf-sup-condition/) together with a condition on the adjoint. That is the Banach-Nečas-Babuška theorem, which also allows different trial and test spaces.

## History

Peter Lax and Arthur Milgram proved the theorem in 1954, in a paper on parabolic equations, to get weak solutions of elliptic problems without a symmetric form. For symmetric forms the result is the Riesz representation theorem of 1907 applied to the energy inner product. Guido Stampacchia extended it in 1964 to variational inequalities on convex sets. Jindřich Nečas (1962) and Ivo Babuška (1971) replaced coercivity by the inf-sup condition, which became the basis of the analysis of mixed and Petrov-Galerkin finite element methods.

## References
