---
tag: 93TXRN
kind: technique
slug: nitsche-method
name: "Nitsche's method"
aliases:
- Nitsche method
area: scientific-computing/finite-element-practice
level: advanced
summary: Imposes Dirichlet conditions weakly by consistency and penalty terms on the boundary, keeping optimal convergence without a conforming space.
prereqs: [weak-formulation, finite-element-method, boundary-conditions]
see_also: [symmetric-interior-penalty-galerkin, cut-finite-element-method, isogeometric-analysis, extended-finite-element-method, penalty-method, lagrange-multiplier, boundary-conditions, hybridizable-discontinuous-galerkin]
sources:
  - paper: doi:10.1007/BF02995904
    title: J. Nitsche, Über ein Variationsprinzip zur Lösung von Dirichlet-Problemen bei Verwendung von Teilräumen, die keinen Randbedingungen unterworfen sind, Abhandlungen aus dem Mathematischen Seminar der Universität Hamburg 36(1) (1971) 9-15
    locator: the modified variational form with the consistency terms and the penalty term on the boundary, and the error estimates in the energy and L2 norms
  - paper: doi:10.1016/0377-0427(95)00057-7
    title: Rolf Stenberg, On some techniques for approximating boundary conditions in the finite element method, Journal of Computational and Applied Mathematics 63(1-3) (1995) 139-148
    locator: the derivation of Nitsche's method from a stabilized Lagrange multiplier method by eliminating the multiplier
  - paper: doi:10.1090/S0025-5718-08-02183-2
    title: Mika Juntunen and Rolf Stenberg, Nitsche's method for general boundary conditions, Mathematics of Computation 78(267) (2009) 1353-1374
    locator: the extension to Robin conditions that is uniform from the Neumann limit to the Dirichlet limit
  - paper: doi:10.1016/S0045-7825(02)00524-8
    title: Anita Hansbo and Peter Hansbo, An unfitted finite element method, based on Nitsche's method, for elliptic interface problems, Computer Methods in Applied Mechanics and Engineering 191(47-48) (2002) 5537-5552
    locator: the use of Nitsche terms on an interface that cuts through the elements of a fixed mesh
---

Nitsche's method imposes a Dirichlet condition $u = g$ on the boundary weakly: the finite element space does not satisfy the condition, and the variational form gets boundary terms that make the discrete solution satisfy it approximately. Unlike the plain [penalty method](/penalty-method/), the added terms keep the form consistent, so the exact solution satisfies the discrete equations, and the method keeps the optimal order of convergence with a penalty parameter of fixed size. Unlike a [Lagrange multiplier](/lagrange-multiplier/), it adds no unknowns and the matrix stays symmetric positive definite, provided the penalty parameter is larger than a constant from an inverse inequality. It is the standard way to impose boundary and interface conditions on meshes that do not fit the boundary, on spline spaces, and between the elements of a [discontinuous Galerkin method](/symmetric-interior-penalty-galerkin/).

## In plain words

A finite element program usually forces the boundary values directly into the unknowns. That is easy when there are mesh nodes on the boundary, and hard when the boundary cuts through elements or when the shape functions do not take the boundary values at nodes. Nitsche's method leaves the boundary values free and adds a few terms on the boundary to the equations. One term pulls the solution toward the given boundary values, like a spring. The other terms correct for the fact that the boundary values are not exact, so the method stays as accurate as with forced values. The spring must be stiff enough, with a strength that depends on the mesh size and on the polynomial degree.

## When it applies

- A second-order elliptic problem, or a system such as elasticity or Stokes flow, with Dirichlet conditions on all or part of the boundary.
- The finite element space cannot satisfy the condition easily: [cut and unfitted meshes](/cut-finite-element-method/), [isogeometric](/isogeometric-analysis/) spline spaces, [enriched spaces](/extended-finite-element-method/) and meshless shape functions.
- Interface conditions between subdomains with nonmatching meshes, between patches of a spline model, or across a material interface inside an element.
- The interior faces of a discontinuous Galerkin method, where the same terms give the [symmetric interior penalty method](/symmetric-interior-penalty-galerkin/).
- A constant $C_I$ in the inverse inequality below must be known or estimated. When small cut cells make $C_I$ large, extra stabilization is needed.

## The template

**Notation.** The model problem is $-\Delta u = f$ in $\Omega$ and $u = g$ on $\partial\Omega$, with outward unit normal $n$ and $\partial_nu = \nabla u\cdot n$. $V_h \subset H^1(\Omega)$ is a finite element space with no boundary constraint, $h_F$ is the size of the element at the boundary face $F$, $\gamma > 0$ is the penalty parameter, and $\langle\cdot, \cdot\rangle$ is the $L^2$ inner product on $\partial\Omega$. The method finds $u_h \in V_h$ with $a_h(u_h, v) = \ell_h(v)$ for all $v \in V_h$, where

$$a_h(u, v) = (\nabla u, \nabla v) - \langle\partial_nu, v\rangle - \langle\partial_nv, u\rangle + \langle\tfrac{\gamma}{h}u, v\rangle, \qquad \ell_h(v) = (f, v) - \langle\partial_nv, g\rangle + \langle\tfrac{\gamma}{h}g, v\rangle.$$

```pseudo id=main
NITSCHE(f, g, mesh, γ)
L1  choose a space V_h with no boundary constraint                  ▷ hole: fitted, cut or spline space
L2  A[i, j] ← (∇φ_j, ∇φ_i) and F[i] ← (f, φ_i)                      ▷ hole: quadrature for the integrals
L3  for each boundary face F with size h_F do
L4      A[i, j] ← A[i, j] - ⟨∂_n φ_j, φ_i⟩_F - ⟨∂_n φ_i, φ_j⟩_F + (γ/h_F) ⟨φ_j, φ_i⟩_F
L5      F[i] ← F[i] - ⟨∂_n φ_i, g⟩_F + (γ/h_F) ⟨g, φ_i⟩_F               ▷ hole: γ from the inverse inequality
L6  solve A U = F                                                    ▷ A is symmetric positive definite for γ > C_I²
L7  return u_h = Σ_j U[j] φ_j
```

**Consistency (theorem).** If $u$ is smooth and solves the problem, then $a_h(u, v) = \ell_h(v)$ for all $v \in V_h$. Integration by parts gives $(\nabla u, \nabla v) - \langle\partial_nu, v\rangle = (f, v)$, and the two other terms are equal on both sides because $u = g$ on $\partial\Omega$. So the error $u - u_h$ is orthogonal to $V_h$ in the form $a_h$, as in the [Galerkin method](/galerkin-method/).

**Coercivity (theorem).** Assume the inverse inequality $\|h^{1/2}\partial_nv\|_{\partial\Omega} \le C_I\|\nabla v\|_\Omega$ for all $v \in V_h$. By the Cauchy-Schwarz and Young inequalities, $2|\langle\partial_nv, v\rangle| \le \delta\|\nabla v\|^2 + (C_I^2/\delta)\|h^{-1/2}v\|_{\partial\Omega}^2$ for every $\delta > 0$, so

$$a_h(v, v) \ge (1 - \delta)\|\nabla v\|^2 + \Bigl(\gamma - \frac{C_I^2}{\delta}\Bigr)\|h^{-1/2}v\|_{\partial\Omega}^2.$$

If $\gamma > C_I^2$, any $\delta$ with $C_I^2/\gamma < \delta < 1$ makes both coefficients positive. With consistency this gives the error bounds $\|\nabla(u - u_h)\| + \|h^{-1/2}(u - u_h)\|_{\partial\Omega} \le Ch^k|u|_{H^{k+1}}$ for elements of degree $k$, and $\|u - u_h\| \le Ch^{k+1}|u|_{H^{k+1}}$ on a convex domain (theorem, Nitsche 1971). For piecewise polynomials of degree $k$, $C_I^2$ grows like $k^2$, so $\gamma$ is usually chosen as a fixed multiple of $k^2$ (heuristic).

**The threshold in 1D, by hand.** Take linear elements on a mesh of size $h$ and a function $v$ with $v(0) = a$ and $v(h) = b$. On the first element $v' = (b - a)/h$, $\partial_nv(0) = -v'(0)$, and the boundary part of $a_h(v, v)$ plus the energy of the first element is

$$h\,v'^2 + 2v'(0)v(0) + \frac{\gamma}{h}a^2 = \frac{1}{h}\bigl[(b - a)^2 + 2(b - a)a + \gamma a^2\bigr] = \frac{1}{h}\bigl[b^2 + (\gamma - 1)a^2\bigr].$$

So $C_I = 1$ here, and the bound $\gamma > 1$ is sharp: for $\gamma = 1$ the hat function at $x = 0$ has $a_h(v, v) = 0$, and for $\gamma < 1$ it has $a_h(v, v) = (\gamma - 1)/h < 0$.

**A full example, by hand.** Solve $-u'' = 2$ on $(0, 1)$ with $u(0) = 0$ imposed by Nitsche's method and $u(1) = 0$ imposed strongly, on 2 elements of size $h = 1/2$. The exact solution is $u = x(1 - x)$. The unknowns are $u_0 = u_h(0)$ and $u_1 = u_h(1/2)$. The stiffness matrix is $\begin{pmatrix} 2 & -2 \\ -2 & 4\end{pmatrix}$, the consistency terms add $\begin{pmatrix} -4 & 2 \\ 2 & 0\end{pmatrix}$ and the penalty adds $2\gamma$ to the first entry, so

$$\begin{pmatrix} 2\gamma - 2 & 0 \\ 0 & 4\end{pmatrix}\begin{pmatrix} u_0 \\ u_1\end{pmatrix} = \begin{pmatrix} 1/2 \\ 1\end{pmatrix}, \qquad u_0 = \frac{1}{4(\gamma - 1)}, \quad u_1 = \frac14.$$

The value $u_1$ is exact, and the boundary value $u_0$ goes to $0$ as $\gamma$ grows. For $\gamma = 10$, $u_0 = 1/36$.

**Refinement (measurement).** On $m = 2, 4, 8, 16, 32$ elements, computed exactly in rational arithmetic, the boundary value is $u_h(0) = h^2/(\gamma - 1)$ for $\gamma = 2, 10, 100$, and it is the largest nodal error in each case. So the boundary condition holds to $O(h^2)$, the same order as the nodal error of the interior, for every fixed $\gamma > 1$.

## Classic examples

- **[Symmetric interior penalty Galerkin](/symmetric-interior-penalty-galerkin/).** Nitsche's terms on every interior face, with the jump of $u_h$ in place of $u_h - g$, couple the discontinuous elements.
- **[Cut finite element method](/cut-finite-element-method/).** The boundary cuts through the elements of a fixed background mesh, and Nitsche's terms impose the condition on the cut part of each element.
- **Unfitted interface problems (Hansbo and Hansbo 2002).** The solution is doubled on the cut elements, and Nitsche's terms impose the continuity of the solution and of the flux across the interface.
- **[Isogeometric analysis](/isogeometric-analysis/).** Spline basis functions do not interpolate the boundary values, and the patches of a model may not match, so both the boundary conditions and the patch coupling use Nitsche's terms.
- **[Extended finite element method](/extended-finite-element-method/).** Conditions on cracks and interfaces that are not mesh lines.
- **Comparison with the [penalty method](/penalty-method/).** The penalty method keeps only $\langle\frac{\gamma}{h}u, v\rangle$ and is not consistent, so its error has a term of order $1/\gamma$, and $\gamma$ must grow as $h \to 0$, which hurts the condition number.
- **Comparison with a [Lagrange multiplier](/lagrange-multiplier/).** A multiplier on the boundary needs a pair of spaces with an [inf-sup bound](/inf-sup-condition/). Stenberg (1995) showed that a stabilized multiplier method gives Nitsche's method after the multiplier is eliminated, with $-\partial_nu_h$ as the discrete multiplier.

## Variations

- **Nonsymmetric Nitsche.** Change the sign of $\langle\partial_nv, u\rangle$ and of $\langle\partial_nv, g\rangle$. Then $a_h(v, v) = \|\nabla v\|^2 + \gamma\|h^{-1/2}v\|_{\partial\Omega}^2$, which is coercive for every $\gamma > 0$ (theorem), at the cost of a nonsymmetric matrix. The duality argument for the $L^2$ estimate needs the symmetric form, so the $L^2$ bound of the nonsymmetric version is weaker.
- **Robin and general conditions (Juntunen and Stenberg 2009).** For $\epsilon\partial_nu + u = g$, a modified penalty gives a method that is uniformly accurate from the Neumann limit to the Dirichlet limit.
- **Variable coefficients.** For $-\nabla\cdot(\kappa\nabla u) = f$ the terms use $\kappa\partial_nu$, and $\gamma$ is scaled with $\kappa$ on the face.
- **Elasticity and contact.** The same construction with the traction $\sigma(u)n$ in place of $\partial_nu$, and nonlinear forms of it for frictionless and frictional contact.
- **Ghost penalty.** On cut meshes, terms that penalize the jumps of derivatives across faces near the boundary make $C_I$ independent of how the boundary cuts the elements.

## Pitfalls

- **Penalty too small.** For $\gamma \le C_I^2$ the matrix can be singular or indefinite, as the 1D threshold shows. A wrong estimate of $C_I$ gives a method that works on one mesh and fails on another.
- **Penalty too large.** The boundary condition is then imposed almost strongly, and the condition number grows like $\gamma$. Keep $\gamma$ a moderate multiple of the bound, for example a factor of 2 to 10 above it (heuristic).
- **Small cut cells.** If the boundary cuts off a tiny part of an element, $\|h^{1/2}\partial_nv\|$ on that part is not controlled by $\|\nabla v\|$ on the same part, and $C_I$ is unbounded. Use a ghost penalty or merge small cells with their neighbors.
- **Missing load terms.** The terms $-\langle\partial_nv, g\rangle$ and $\langle\frac{\gamma}{h}g, v\rangle$ in $\ell_h$ are needed for consistency when $g \ne 0$. Without the first one the method loses its order.
- **Normal and sign errors.** The normal must be the outward normal of the domain, and on interfaces each side must use the same normal for the jump and the average.
- **Higher degree.** The constant $C_I^2$ grows like $k^2$, so a $\gamma$ that works for linear elements can fail for degree $k \ge 2$.

## Exercises

1. Show that the exact solution of $-\Delta u = f$, $u = g$ satisfies $a_h(u, v) = \ell_h(v)$ for every $v \in V_h$, and say which step fails for the penalty method.
2. In the 2-element example, compute $u_h(0)$ for the penalty method with the same $\gamma$, that is with the consistency terms removed, and compare it with $1/(4(\gamma - 1))$.
3. Prove that the nonsymmetric version is coercive for every $\gamma > 0$, and compute $u_0$ and $u_1$ for it in the 2-element example with $\gamma = 1$.
4. For linear elements in 1D, show that the inverse inequality holds with $C_I = 1$, and for quadratic elements find the best $C_I$ on one element.

## References
