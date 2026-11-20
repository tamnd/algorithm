---
tag: JTGEM5
kind: theorem
slug: cea-lemma
name: Cea's lemma
aliases:
- quasi-optimality of the Galerkin method
area: scientific-computing/finite-element-practice
level: core
summary: The Galerkin solution is within a factor M/alpha of the best approximation in the finite element space, the ratio of continuity and coercivity constants.
prereqs: [lax-milgram-theorem, galerkin-method]
see_also: [bramble-hilbert-lemma, finite-element-method, sobolev-space, inf-sup-condition, finite-element-locking, streamline-upwind-petrov-galerkin, least-squares-approximation]
sources:
  - paper: doi:10.5802/aif.181
    title: Jean Céa, Approximation variationnelle des problèmes aux limites, Annales de l'Institut Fourier 14(2) (1964) 345-444
    locator: the quasi-optimality estimate for conforming approximations of coercive problems
  - book: isbn:9780387759333
    title: Susanne C. Brenner and L. Ridgway Scott, The Mathematical Theory of Finite Element Methods, third edition, Springer, 2008
    locator: Chapter 0 (Galerkin orthogonality in one dimension) and Chapter 2 (Céa's theorem and the symmetric case)
  - book: isbn:9780898715149
    title: Philippe G. Ciarlet, The Finite Element Method for Elliptic Problems, SIAM Classics in Applied Mathematics 40, 2002
    locator: Chapter 2 (Céa's lemma) and Chapter 4 (numerical integration and nonconforming methods, with Strang's lemmas)
---

Céa's lemma says that the [Galerkin](/galerkin-method/) approximation $u_h$ of a coercive problem is as good as the best approximation of $u$ in the same subspace, up to the factor $M/\alpha$: $\|u - u_h\| \le (M/\alpha)\inf_{v_h \in V_h}\|u - v_h\|$. Here $M$ is the continuity constant and $\alpha$ the coercivity constant of the form $a$. The lemma splits finite element error analysis into two separate questions: how stable the problem is, which fixes $M/\alpha$, and how well the space approximates smooth functions, which the [Bramble-Hilbert lemma](/bramble-hilbert-lemma/) answers. For a symmetric form the Galerkin solution is exactly the best approximation in the energy norm.

## Statement

**Setting.** Let $V$ be a real Hilbert space, let $a$ be a bilinear form on $V$ with $|a(u, v)| \le M\|u\|\,\|v\|$ and $a(v, v) \ge \alpha\|v\|^2$, $\alpha > 0$, and let $l \in V'$. Let $u \in V$ solve $a(u, v) = l(v)$ for all $v \in V$, as the [Lax-Milgram theorem](/lax-milgram-theorem/) allows. Let $V_h \subset V$ be a closed subspace (for example a finite element space) and let $u_h \in V_h$ solve

$$a(u_h, v_h) = l(v_h) \quad \text{for all } v_h \in V_h .$$

**Theorem (Céa, 1964).** The Galerkin solution satisfies

$$\|u - u_h\| \le \frac{M}{\alpha} \inf_{v_h \in V_h} \|u - v_h\| .$$

**Symmetric case.** If also $a(u, v) = a(v, u)$, let $\|v\|_a = a(v, v)^{1/2}$ be the energy norm. Then

$$\|u - u_h\|_a = \min_{v_h \in V_h} \|u - v_h\|_a \qquad \text{and} \qquad \|u - u_h\| \le \sqrt{M/\alpha}\, \inf_{v_h \in V_h}\|u - v_h\| .$$

## In plain words

A finite element method cannot give the exact answer, because it can only produce shapes from a limited family. The best it could hope for is the member of that family that is closest to the exact answer. This lemma says that the method gets within a fixed factor of that best member. The factor depends only on the problem, not on the mesh. So to know how accurate the method is, you only need to know how well the family can imitate the exact answer, which is a question about approximation alone. When the problem has a symmetric energy, the method finds the best member exactly, measured in that energy.

## Proof

**Galerkin orthogonality.** Subtract the discrete equation from the continuous one with the same test function $w_h \in V_h \subset V$:

$$a(u - u_h, w_h) = 0 \quad \text{for all } w_h \in V_h .$$

**The general case.** Let $v_h \in V_h$ be arbitrary. Then $u_h - v_h \in V_h$, so orthogonality gives $a(u - u_h, u_h - v_h) = 0$. With coercivity and continuity,

$$\alpha\|u - u_h\|^2 \le a(u - u_h, u - u_h) = a(u - u_h, u - v_h) + a(u - u_h, v_h - u_h) = a(u - u_h, u - v_h) \le M\|u - u_h\|\,\|u - v_h\| .$$

Divide by $\alpha\|u - u_h\|$ (nothing is to prove if it is zero) and take the infimum over $v_h$.

**The symmetric case.** Now $a$ is an inner product on $V$, and orthogonality says that $u_h$ is the $a$-orthogonal projection of $u$ onto $V_h$. For every $v_h \in V_h$, the vector $u_h - v_h$ is in $V_h$, so by the Pythagorean theorem

$$\|u - v_h\|_a^2 = \|u - u_h\|_a^2 + \|u_h - v_h\|_a^2 \ge \|u - u_h\|_a^2,$$

with equality only for $v_h = u_h$. The norms satisfy $\alpha\|v\|^2 \le \|v\|_a^2 \le M\|v\|^2$, so $\alpha\|u - u_h\|^2 \le \|u - u_h\|_a^2 \le \|u - v_h\|_a^2 \le M\|u - v_h\|^2$, which gives the factor $\sqrt{M/\alpha}$. $\square$

## Consequences

**A priori error estimates.** Take $v_h = I_h u$, the nodal interpolant into continuous piecewise polynomials of degree $k$ on a shape regular mesh $\mathcal{T}_h$. The [Bramble-Hilbert lemma](/bramble-hilbert-lemma/) gives $\|u - I_h u\|_1 \le C h^k |u|_{k+1}$, so

$$\|u - u_h\|_1 \le \frac{M}{\alpha}\, C h^k |u|_{k+1} .$$

If the problem has full elliptic regularity, for example the Poisson problem on a convex polygon, the Aubin-Nitsche duality argument adds one power: $\|u - u_h\|_0 \le C h^{k+1}|u|_{k+1}$. The [finite element method](/finite-element-method/) page shows these rates in a table.

**A hand check of the Pythagorean identity.** Take $-u'' = 1$ on $(0,1)$ with $u(0) = u(1) = 0$, so $u = x(1-x)/2$ and $a(u, v) = \int_0^1 u'v'$. Use P1 elements with $h = \tfrac12$. The one unknown satisfies $(2/h)U = h$, so $U = \tfrac18 = u(\tfrac12)$ and $u_h$ is the interpolant. Then $|u|_1^2 = \int_0^1 (\tfrac12 - x)^2 dx = \tfrac1{12}$ and $|u_h|_1^2 = 2\cdot\tfrac12\cdot(\tfrac14)^2 = \tfrac1{16}$. On $[0, \tfrac12]$ the error derivative is $\tfrac14 - x$, so $|u - u_h|_1^2 = 2\int_{-1/4}^{1/4} t^2\,dt = \tfrac1{48}$. Indeed $\tfrac1{12} = \tfrac1{16} + \tfrac1{48}$, which is orthogonality $a(u - u_h, u_h) = 0$ in numbers.

**Convection makes the constant large.** For $-\varepsilon u'' + bu' = f$ on $H^1_0(0,1)$ in the norm $|\cdot|_1$ we have $\alpha = \varepsilon$ and $M = \varepsilon + |b|/\pi$, so $M/\alpha = 1 + |b|/(\pi\varepsilon)$. When convection dominates, the bound allows a Galerkin error far larger than the best approximation error, and in practice the solution oscillates. [Streamline upwind Petrov-Galerkin](/streamline-upwind-petrov-galerkin/) changes the test functions to bring the constant down.

**Locking.** For nearly incompressible linear elasticity the ratio $M/\alpha$ grows like $\lambda/\mu$, and low-order elements show [locking](/finite-element-locking/): the bound is uniform in $h$ but not in $\lambda$.

**The error is a property of the space.** The Galerkin error lies between the best approximation error and $M/\alpha$ times it, so $u_h$ converges at exactly the rate of the best approximation. Better accuracy needs a better space: smaller $h$, higher $k$, or a mesh adapted to the singularities of $u$.

## Tightness

**The factor $M/\alpha$ is attained.** Let $V = \mathbb{R}^2$ with the Euclidean norm, $V_h = \operatorname{span}\{e_1\}$, and $a(u, v) = v^\top A u$ with $A = \begin{pmatrix} 1 & t \\ -t & 1\end{pmatrix}$. Then $\alpha = 1$ and $M = \sqrt{1 + t^2}$. For $u = (0, 1)$ the Galerkin equation $a(ce_1, e_1) = a(u, e_1)$ reads $c = t$, so $u_h = (t, 0)$ and $\|u - u_h\| = \sqrt{1 + t^2}$. The best approximation is $0$ with error $1$. The ratio is exactly $M/\alpha$, for every $t$.

**Conformity is needed.** The proof uses $V_h \subset V$ and the exact $a$ and $l$. With numerical quadrature, nonconforming elements or curved boundaries approximated by polygons, the Strang lemmas add a consistency term to the bound.

**Coercivity on $V_h$ is needed.** For a problem that is only inf-sup stable, such as Stokes, a subspace pair can be unstable, and then no quasi-optimality holds. The discrete [inf-sup condition](/inf-sup-condition/) with a constant independent of $h$ restores a bound of the same form with a different constant.

**The norm matters.** The best approximation property in the energy norm does not hold in $L^2$. In the hand check above, $u_h$ is not the $L^2$ projection of $u$ onto P1 functions, which has a smaller $L^2$ error.

## History

Jean Céa proved the estimate in his 1964 thesis on variational approximation of boundary value problems. The name "Céa's lemma" spread with the textbooks of the 1970s, in particular Ciarlet's book of 1978. For symmetric problems the best approximation property in the energy norm was already part of the Rayleigh-Ritz method. Gilbert Strang extended the estimate in 1972 to nonconforming methods and to methods with quadrature.

## References
