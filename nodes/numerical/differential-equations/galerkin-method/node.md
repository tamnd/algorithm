---
tag: JTKJZE
kind: technique
slug: galerkin-method
name: Galerkin method
aliases:
- Ritz-Galerkin method
- Bubnov-Galerkin method
- Galerkin projection
- method of weighted residuals
area: numerical/differential-equations
level: advanced
summary: "Write the equation in weak form a(u, v) = l(v) for all test functions v, then look for u_h in a finite-dimensional space V_h with the same identity on V_h. The error is near-best in V_h (Céa)."
prereqs: [poisson-equation, boundary-conditions, least-squares-approximation]
see_also: [finite-element-method, spectral-methods, collocation-method, finite-volume-method, sturm-liouville-problem, conjugate-gradient-method, gmres, finite-difference-method]
sources:
  - book: isbn:9780387759333
    title: Susanne C. Brenner and L. Ridgway Scott, The Mathematical Theory of Finite Element Methods, third edition, Springer, 2008
    locator: Chapter 0 (basic concepts in one dimension; weak formulation, Ritz-Galerkin approximation, error estimates), Chapter 2 (variational formulation of elliptic boundary value problems; the Lax-Milgram theorem and Céa's lemma)
  - book: isbn:9780898715149
    title: Philippe G. Ciarlet, The Finite Element Method for Elliptic Problems, SIAM Classics in Applied Mathematics 40, 2002
    locator: Chapter 1 (elliptic boundary value problems, abstract problem, Céa's lemma), Chapter 2 (introduction to the finite element method)
  - paper: doi:10.5802/aif.181
    title: Jean Céa, Approximation variationnelle des problèmes aux limites, Annales de l'Institut Fourier 14(2) (1964) 345-444
    locator: the quasi-optimality estimate of the Galerkin approximation for coercive problems
  - paper: doi:10.1515/crll.1909.135.1
    title: Walther Ritz, Über eine neue Methode zur Lösung gewisser Variationsprobleme der mathematischen Physik, Journal für die reine und angewandte Mathematik 135 (1909) 1-61
    locator: minimizing the energy over finite linear combinations of trial functions
---

The Galerkin method turns a differential equation into a finite linear system by projection. One writes the equation in weak form: find $u$ in a function space $V$ with $a(u, v) = \ell(v)$ for every test function $v \in V$. Then one picks a finite-dimensional subspace $V_h \subset V$ and asks for $u_h \in V_h$ with $a(u_h, v) = \ell(v)$ for every $v \in V_h$. Equivalently, the residual of $u_h$ is orthogonal to $V_h$. With a basis of $V_h$ this is a linear system of size $\dim V_h$. For coercive problems the error is within a constant factor of the best approximation of $u$ in $V_h$ (Céa's lemma), and for symmetric problems it is the best approximation in the energy norm. Local piecewise polynomial bases give the [finite element method](/finite-element-method/); global orthogonal bases give [spectral methods](/spectral-methods/).

## In plain words

Suppose you cannot find the exact shape of a bent beam, but you are willing to accept any shape built from a fixed menu of simple pieces, mixed in some proportions. Which mix is best? The Galerkin method answers: choose the mix so that the leftover error in the equation is invisible to every piece on the menu. You test the equation against each piece and demand that it balance. For many physical problems, this choice is the same as picking the mix with the lowest energy, and it is provably close to the best possible mix from that menu. A richer menu, with more or finer pieces, gives a better answer. The method then reduces to solving one system of linear equations.

## When it applies

- The problem has a weak (variational) form $a(u, v) = \ell(v)$ on a Hilbert space $V$, with $a$ bilinear and bounded, $|a(u, v)| \le M\|u\|\,\|v\|$, and $\ell$ linear and bounded. Second-order elliptic problems such as the [Poisson equation](/poisson-equation/) in $V = H_0^1(\Omega)$ are the model case.
- Céa's lemma needs coercivity, $a(v, v) \ge \alpha\|v\|^2$ with $\alpha > 0$. Indefinite or non-coercive problems (Helmholtz, saddle points such as Stokes) need a discrete inf-sup condition instead, which is not automatic.
- The trial space $V_h$ can be built so that $V_h \subset V$ (conforming) and approximates $u$ well; boundary conditions of Dirichlet type are built into $V_h$, natural (Neumann) ones come out of the weak form.
- The cost model is the assembly of $A_{ij} = a(\phi_j, \phi_i)$ and $F_i = \ell(\phi_i)$ by quadrature, plus the solution of an $N \times N$ system, $N = \dim V_h$.

## The template

**Notation.** $V$ a Hilbert space with norm $\|\cdot\|$; $a$, $\ell$ as above; $V_h = \operatorname{span}\{\phi_1, \ldots, \phi_N\} \subset V$; $u_h = \sum_jU_j\phi_j$. For time-dependent problems $u_h(t) = \sum_jU_j(t)\phi_j$ and the same projection gives an ODE system.

```pseudo id=main
GALERKIN(a, ℓ, V_h)
L1  choose a basis φ_1..φ_N of the trial space V_h ⊂ V          ▷ hole: the trial space
L2  for i ← 1 to N do
L3      for j ← 1 to N do
L4          A[i, j] ← a(φ_j, φ_i)                                 ▷ hole: quadrature for the integrals
L5      F[i] ← ℓ(φ_i)
L6  solve A U = F                                                  ▷ hole: direct or iterative solver
L7  return u_h = Σ_j U[j] φ_j
```

Lines L2 to L5 compute the stiffness matrix $A$ and the load vector $F$. For a local basis most $A_{ij}$ are zero and are never formed; finite element codes loop over elements instead of pairs. If $a$ is symmetric and coercive, $A$ is symmetric positive definite and the [conjugate gradient method](/conjugate-gradient-method/) applies at line L6; otherwise [GMRES](/gmres/) or a direct solver.

**Galerkin orthogonality.** Subtracting $a(u_h, v) = \ell(v)$ from $a(u, v) = \ell(v)$ for $v \in V_h$ gives $a(u - u_h, v) = 0$ for all $v \in V_h$.

**Céa's lemma (proved).** If $a$ is bounded with constant $M$ and coercive with constant $\alpha$, then $u_h$ exists, is unique, and

$$\|u - u_h\| \le \frac{M}{\alpha}\min_{v \in V_h}\|u - v\|.$$

*Proof.* Existence and uniqueness: $A$ is nonsingular, because $AU = 0$ gives $\alpha\|u_h\|^2 \le a(u_h, u_h) = U^{\mathsf T}AU = 0$. For any $v \in V_h$, by coercivity, orthogonality ($u_h - v \in V_h$) and boundedness, $\alpha\|u - u_h\|^2 \le a(u - u_h, u - u_h) = a(u - u_h, u - v) \le M\|u - u_h\|\,\|u - v\|$. Divide by $\alpha\|u - u_h\|$. $\square$

If $a$ is symmetric, $a$ is an inner product, $u_h$ is the $a$-orthogonal projection of $u$ onto $V_h$, and it minimizes the energy $\tfrac12a(v, v) - \ell(v)$ over $V_h$ (the Ritz method); the constant improves to $\sqrt{M/\alpha}$, and to 1 in the energy norm $\|v\|_a = a(v, v)^{1/2}$.

## Classic examples

**Linear elements in one dimension.** For $-u'' = f$ on $(0, 1)$, $u(0) = u(1) = 0$: $V = H_0^1(0, 1)$, $a(u, v) = \int_0^1u'v'$, $\ell(v) = \int_0^1fv$. Hat functions on a uniform grid with spacing $h$ give $A = \tfrac1h\operatorname{tridiag}(-1, 2, -1)$, the same matrix as the [finite difference method](/finite-difference-method/) up to the factor $h$, with load $F_i = \int f\phi_i$. For $f = \pi^2\sin(\pi x)$, with exact load integrals:

| $J = 1/h$ | max nodal error | $\|u' - u_h'\|_{L^2}$ | $\|u - u_h\|_{L^2}$ |
|---|---|---|---|
| 4 | $3 \cdot 10^{-16}$ | 0.4985 | $3.928 \cdot 10^{-2}$ |
| 8 | $2 \cdot 10^{-16}$ | 0.2512 | $9.921 \cdot 10^{-3}$ |
| 16 | $1 \cdot 10^{-15}$ | 0.1258 | $2.487 \cdot 10^{-3}$ |
| 32 | $1 \cdot 10^{-14}$ | 0.06295 | $6.220 \cdot 10^{-4}$ |

The nodal values are exact to rounding: in one dimension the Galerkin solution of $-u'' = f$ with linear elements interpolates $u$ at the nodes, because the Green's function for a node lies in $V_h$. The energy error is first order (it is the interpolation error, by Céa with constant 1), and the $L^2$ error is second order, by the Aubin-Nitsche duality argument.

**Spectral Galerkin.** For the same problem with the basis $\sin(k\pi x)$, $k = 1, \ldots, N$, the matrix is diagonal, $A_{kk} = (k\pi)^2/2$, and $u_h$ is the truncated sine series of $u$. For smooth periodic-compatible data the error decays faster than any power of $1/N$ ([spectral methods](/spectral-methods/)).

**Finite elements in two and three dimensions.** Piecewise polynomials on triangles or tetrahedra, continuous across element faces, give the [finite element method](/finite-element-method/), with error $O(h^k)$ in $H^1$ for degree $k$ when $u \in H^{k+1}$.

**Time-dependent problems.** For the [heat equation](/heat-equation/), $u_h(t) = \sum_jU_j(t)\phi_j$ gives $MU' + KU = F(t)$ with the mass matrix $M_{ij} = \int\phi_j\phi_i$: a semi-discrete Galerkin method, then integrated in time as in the [method of lines](/method-of-lines/).

**[Sturm-Liouville eigenvalues](/sturm-liouville-problem/).** The Rayleigh-Ritz method is the Galerkin method for $a(u, v) = \lambda(u, v)$; the discrete eigenvalues are upper bounds of the exact ones, by the min-max principle.

## Variations

- **Petrov-Galerkin.** Take test functions from a different space $W_h$. Streamline upwind Petrov-Galerkin (SUPG) adds a test function component along the flow to stabilize convection-dominated problems.
- **Discontinuous Galerkin.** Allow functions discontinuous across elements and couple them through numerical fluxes on faces, as in the [finite volume method](/finite-volume-method/), of which the lowest-order DG method is an instance.
- **Least-squares methods** minimize the residual norm, which leads to a symmetric positive definite system even for non-symmetric problems.
- **Collocation** asks the equation to hold at points instead of in the weak sense; it is a Petrov-Galerkin method with delta test functions ([collocation method](/collocation-method/)).
- **Nonconforming methods** use $V_h \not\subset V$, which adds a consistency error term to Céa's bound (Strang's lemmas).
- **Galerkin in time.** Continuous and discontinuous Galerkin time stepping; the discontinuous Galerkin method in time with degree $q$ polynomials coincides at the nodes with the Radau IIA method with $q + 1$ stages for linear constant coefficient problems.

## Pitfalls

- **Convection dominance.** For $-\varepsilon u'' + u' = 1$, $u(0) = u(1) = 0$, $\varepsilon = 0.01$, the standard Galerkin method with linear elements oscillates when the mesh Péclet number $h/(2\varepsilon)$ exceeds 1. With $h = 0.1$ (Péclet number 5) the nodal values near $x = 1$ are $0.417, 1.019, 0.365, 1.596$ and the maximum error is $0.70$, while the exact solution increases monotonically to about $0.944$ and then drops to 0 in a boundary layer of width about $\varepsilon$. With $h = 0.01$ (Péclet number 0.5) the error is $0.035$ and the values are monotone. Céa's lemma still holds, but $M/\alpha$ grows like $1/\varepsilon$.
- **Inexact quadrature.** Replacing integrals by quadrature changes $a$ and $\ell$; the rule must be exact enough for the degree used, or the order drops.
- **Inf-sup failure.** For mixed problems such as Stokes, unstable pairs of velocity and pressure spaces give spurious pressure modes; coercivity of $a$ on the whole space does not hold.
- **Dirichlet conditions.** Imposing them by interpolation in $V_h$ is standard; imposing them weakly needs penalty or Nitsche terms with a parameter that must be large enough.
- **Conditioning.** The stiffness matrix of a second-order problem has condition number of order $h^{-2}$; high-degree global bases (monomials) can be far worse. Use local or orthogonal bases and preconditioners.

## Exercises

1. Compute $A$ and $F$ for $-u'' = 1$ with three interior hat functions on a uniform grid, solve, and check that the nodal values equal $\tfrac12x(1 - x)$.
2. Prove that in one dimension the linear-element Galerkin solution of $-u'' = f$ is exact at the nodes, using the Green's function $G(x, x_i)$.
3. For a symmetric coercive $a$, show $\|u - u_h\|_a = \min_{v \in V_h}\|u - v\|_a$ and that $u_h$ minimizes $\tfrac12a(v, v) - \ell(v)$ over $V_h$.
4. Derive the linear-element equations for $-\varepsilon u'' + u' = 1$ and find the mesh Péclet number at which the coefficient of $u_{j+1}$ changes sign.

## References
