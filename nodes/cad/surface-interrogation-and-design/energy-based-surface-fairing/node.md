---
tag: 9P66FN
kind: technique
slug: energy-based-surface-fairing
name: Energy-based surface fairing
aliases:
- variational surface fairing
- thin plate energy fairing
area: cad/surface-interrogation-and-design
level: core
summary: Smooths a B-spline curve or surface by minimising a quadratic energy such as the thin plate energy plus a fitting term, so it is fair and close to the data.
prereqs: [b-spline, tensor-product-surface, least-squares-approximation, positive-definite-matrix]
see_also: [minimum-variation-surface, knot-removal-fairing, smoothing-spline, kkt-conditions, implicit-fairing, reflection-lines, quadratic-programming, cholesky-decomposition]
sources:
  - paper: doi:10.1111/1467-8659.1330143
    title: "Günther Greiner, Variational design and fairing of spline surfaces, Computer Graphics Forum 13(3), 143 to 154, 1994"
    locator: fairness functionals as simplified thin plate energies for parametric surfaces, made quadratic by a reference parametrization
  - paper: doi:10.1145/122718.122746
    title: "George Celniker and Dave Gossard, Deformable curve and surface finite-elements for free-form shape design, SIGGRAPH 1991, 257 to 266"
    locator: surfaces that minimize a stretching and bending energy under geometric constraints and loads
  - paper: "William Welch and Andrew Witkin, Variational surface modeling, SIGGRAPH 1992, Computer Graphics 26(2), 157 to 166"
    title: Welch and Witkin 1992
    locator: free-form surfaces whose shape, within the constraints set by the user, is fixed by a smoothness criterion
  - paper: doi:10.1145/142920.134035
    title: "Henry P. Moreton and Carlo H. Séquin, Functional optimization for fair surface design, Computer Graphics 26(2), 167 to 176, 1992"
    locator: the comparison of the thin plate energy with the curvature variation functional
---

Energy-based fairing makes a curve or a surface smooth by choosing its control points to minimize an energy. The energy measures how much the surface bends, and a second term, if there is one, measures how far it is from the data. The usual choice is the linearized thin plate energy $\iint |S_{uu}|^2 + 2 |S_{uv}|^2 + |S_{vv}|^2 \, du \, dv$. It is a quadratic form in the control points, so with linear constraints, such as fixed boundary curves or points to interpolate, the best control points solve one linear system. That is the main reason for its use: the fairest surface in this sense costs one sparse linear solve. The nonlinear energies of [minimum variation surfaces](/minimum-variation-surface/) give better shapes at a much higher cost.

## In plain words

Think of a thin sheet of steel. Pin it at some points, or clamp its edges, and it settles into the shape that bends least. That shape is smooth and calm, with no bumps that the pins do not force. Energy-based fairing imitates this sheet. It writes down a number that is large when the surface bends a lot, and it moves the control points to make that number as small as possible, while the surface still meets the conditions the designer set. If the surface must also follow measured points, a second number counts the misfit, and a weight says how much smoothness may cost in accuracy. Because both numbers are simple sums of squares, the best control points come from one system of linear equations.

## When it applies

Use it when a surface is given by a control net and some linear conditions, and the shape between the conditions is free: a patch with fixed boundary curves, a surface through scattered points, a surface fitted to noisy measured points, or a surface whose control net was edited by hand and has bumps. It applies to B-spline and Bezier curves and surfaces, to subdivision surfaces and, in discrete form, to meshes. It needs a parametrization that is not too far from uniform in arc length, since the linearized energy measures parameter derivatives, not curvature.

## The template

**The energies.** Let $S(u, v) = \sum_{i, j} N_i(u) M_j(v) P_{ij}$ be a [tensor product](/tensor-product-surface/) B-spline surface on $[a, b] \times [c, d]$. The *membrane energy* and the linearized *thin plate energy* are

$$E_m(P) = \iint |S_u|^2 + |S_v|^2 \, du \, dv, \qquad E_t(P) = \iint |S_{uu}|^2 + 2 |S_{uv}|^2 + |S_{vv}|^2 \, du \, dv.$$

The true bending energy of a thin plate is $\iint \kappa_1^2 + \kappa_2^2 \, dA$, with the principal curvatures $\kappa_1, \kappa_2$. For a height field $z(x, y)$ with small slopes, $\kappa_1^2 + \kappa_2^2 = (\kappa_1 + \kappa_2)^2 - 2 \kappa_1 \kappa_2 \approx (z_{xx} + z_{yy})^2 - 2 (z_{xx} z_{yy} - z_{xy}^2) = z_{xx}^2 + 2 z_{xy}^2 + z_{yy}^2$, which is $E_t$. For a parametric surface $E_t$ is close to the bending energy only where the parametrization is close to an isometry. The fitting term for data points $Q_k$ at parameters $(u_k, v_k)$ is $D(P) = \sum_k |S(u_k, v_k) - Q_k|^2$.

```pseudo id=main
FAIR(knots, degrees, data Q_k at (u_k, v_k), weights λ, α, β, constraints C p = r)
L1  G_a ← the Gram matrix of the a-th derivatives in u, (G_a)_{ik} = ∫ N_i^{(a)} N_k^{(a)} du, for a = 0, 1, 2; H_a the same in v
L2  K ← α (G_1 ⊗ H_0 + G_0 ⊗ H_1) + β (G_2 ⊗ H_0 + 2 G_1 ⊗ H_1 + G_0 ⊗ H_2)
L3  A ← the collocation matrix, A_{k,(ij)} = N_i(u_k) M_j(v_k)
L4  M ← AᵀA + λ K; b ← AᵀQ, one column for each coordinate
L5  solve [M Cᵀ; C 0] [p; μ] = [b; r] for each coordinate      ▷ hole: a sparse symmetric solver
L6  return the surface with the control net p
```

Line L2 is the energy matrix $K$ of $\alpha E_m + \beta E_t$, and line L4 adds the fitting term. The constraints $C p = r$ are any linear conditions: fixed control points, points the surface must interpolate, or tangent conditions along a boundary. Line L5 is the system of the [KKT conditions](/kkt-conditions/), with Lagrange multipliers $\mu$. With no constraints it is $M p = b$, and with fixed control points only, it is $M p = b$ restricted to the free points. Each coordinate is solved with the same matrix, so one factorization serves all three.

**Theorem 1 (the energies are quadratic forms).** For each coordinate, write $p$ for the vector of that coordinate of the control points. Then $E_t(P) = \sum_{\text{coordinates}} p^{\mathsf T} K_t p$ with $K_t = G_2 \otimes H_0 + 2 G_1 \otimes H_1 + G_0 \otimes H_2$, and $K_t$ is symmetric and positive semidefinite. The same holds for $E_m$ with $K_m = G_1 \otimes H_0 + G_0 \otimes H_1$.

*Proof.* The surface is linear in the control points, and so are its derivatives: $S_{uu} = \sum_{i, j} N_i''(u) M_j(v) P_{ij}$. For one coordinate,

$$\iint S_{uu}^2 \, du \, dv = \sum_{i, j} \sum_{k, l} p_{ij} p_{kl} \int N_i'' N_k'' \, du \int M_j M_l \, dv = \sum_{(i, j), (k, l)} p_{ij} (G_2)_{ik} (H_0)_{jl} \, p_{kl},$$

because the integrand is a product of a function of $u$ and a function of $v$. The matrix with the entries $(G_2)_{ik} (H_0)_{jl}$ is the Kronecker product $G_2 \otimes H_0$. The terms with $S_{uv}$ and $S_{vv}$ give $G_1 \otimes H_1$ and $G_0 \otimes H_2$ in the same way, and the sum over the coordinates gives $|S_{uu}|^2$ and the rest. Each Gram matrix is symmetric, so $K_t$ is symmetric. Since $E_t \ge 0$ for every $p$, $K_t$ is positive semidefinite. $\square$

The kernel of $K_t$ is the set of nets with $E_t = 0$, that is with $S_{uu} = S_{uv} = S_{vv} = 0$, which are the nets of the affine maps $S = a + b u + c v$. So $E_t$ alone does not fix a surface: the constraints or the data must rule out the affine motions.

**Theorem 2 (the minimizer solves a linear system).** Let $M = A^{\mathsf T} A + \lambda K$ with $\lambda \ge 0$, so that the objective is $F(p) = |A p - Q|^2 + \lambda p^{\mathsf T} K p = p^{\mathsf T} M p - 2 b^{\mathsf T} p + |Q|^2$. A vector $p^\ast$ with $C p^\ast = r$ minimizes $F$ over $\{p : C p = r\}$ if and only if there is a $\mu$ with $M p^\ast + C^{\mathsf T} \mu = b$. If $C$ has full row rank and $h^{\mathsf T} M h > 0$ for every $h \ne 0$ with $C h = 0$, the system of line L5 is nonsingular, and the minimizer is unique.

*Proof.* Every feasible point is $p = p^\ast + h$ with $C h = 0$, and

$$F(p^\ast + h) - F(p^\ast) = 2 h^{\mathsf T} (M p^\ast - b) + h^{\mathsf T} M h.$$

If $M p^\ast - b = -C^{\mathsf T} \mu$, the first term is $-2 (C h)^{\mathsf T} \mu = 0$, and the second is at least $0$ because $M$ is positive semidefinite (Theorem 1, and $A^{\mathsf T} A$ is a Gram matrix). So $p^\ast$ is a minimizer. Conversely, if $p^\ast$ is a minimizer, then for each $h$ with $C h = 0$ the function $t \mapsto F(p^\ast + t h)$ has its minimum at $t = 0$, so its derivative $2 h^{\mathsf T}(M p^\ast - b)$ there is $0$. Hence $M p^\ast - b$ is orthogonal to the null space of $C$, so it is in the range of $C^{\mathsf T}$, which gives $\mu$. For the last claim, let $M h + C^{\mathsf T} \nu = 0$ and $C h = 0$. Then $0 = h^{\mathsf T} M h + (C h)^{\mathsf T} \nu = h^{\mathsf T} M h$, so $h = 0$, then $C^{\mathsf T} \nu = 0$, and $\nu = 0$ because $C$ has full row rank. $\square$

**Worked example.** Take a bicubic Bezier patch, so each $N_i$ and $M_j$ is a cubic Bernstein polynomial on $[0, 1]$, with the control points $(\frac i3, \frac j3, z_{ij})$. Fix the twelve boundary points, with the heights $0, 1, 1, 0$ along each edge, and let the four inner points be free. Use $E_t$ alone ($\lambda = 0$, $\alpha = 0$, $\beta = 1$). The $x$ and $y$ coordinates of the net are affine, so they have zero energy and stay on the grid, and only the four inner heights are unknown. For the cubic Bernstein basis $G_0$ has the entries $\frac{1}{7} \binom{3}{i} \binom{3}{k} / \binom{6}{i + k}$, and $G_2$ is

$$G_2 = \begin{pmatrix} 12 & -18 & 0 & 6 \\ -18 & 36 & -18 & 0 \\ 0 & -18 & 36 & -18 \\ 6 & 0 & -18 & 12 \end{pmatrix}.$$

The $4 \times 4$ system of line L5 has the same right side $\frac{54}{5}$ in each row, and its solution is $z_{11} = z_{12} = z_{21} = z_{22} = \frac{12}{11}$. On the line where the four inner heights are equal to $s$, the energy is $E_t = \frac15 (198 s^2 - 432 s + 432)$, with its minimum $\frac{432}{11} \approx 39.27$ at $s = \frac{12}{11}$. The obvious guess $s = 1$ gives $\frac{198}{5} = 39.6$, and $s = 0$ gives $86.4$. At the centre the fair patch has height $\frac{87}{88}$, against $\frac{15}{16}$ for $s = 1$. The fair surface lifts the inner points a little above the edge points, to round off the top, as a bent plate does.

## Classic examples

- **Variational design.** Welch and Witkin show the user a surface with no fixed control points: within the constraints that the user places, the shape is the one that minimizes a smoothness energy, so the user edits by constraints and not by control points.
- **Deformable finite elements.** Celniker and Gossard build curve and surface elements that deform to minimize an energy functional under geometric constraints and loads that the user controls.
- **Data dependent energies.** Greiner keeps the energy quadratic but measures the derivatives with the help of a reference surface, so that the functional is a simplified form of the geometric thin plate energy and is still cheap to minimize.
- **Smoothing splines.** For curves, $\sum_k |c(t_k) - Q_k|^2 + \lambda \int |c''|^2$ is the [smoothing spline](/smoothing-spline/) functional, and its minimizer over all functions is a natural cubic spline.
- **Mesh fairing.** On a mesh, the [cotangent Laplacian](/cotangent-laplacian/) gives discrete membrane and thin plate energies, and [implicit fairing](/implicit-fairing/) solves the same kind of sparse system.

## Variations

- **Other quadratic energies.** Third derivative energies, such as $\iint |S_{uuu}|^2 + 3 |S_{uuv}|^2 + 3 |S_{uvv}|^2 + |S_{vvv}|^2$, measure the change of curvature and are still quadratic.
- **Hard and soft constraints.** A condition can be a row of $C$, which holds exactly, or a term of the fitting sum, which holds approximately with a weight.
- **Fairing within a tolerance.** Minimize the energy subject to $|S(u_k, v_k) - Q_k| \le \varepsilon$. The constraints are then quadratic inequalities, and the problem is a convex program, not a linear system.
- **Nonlinear energies.** The exact thin plate energy $\iint \kappa_1^2 + \kappa_2^2 \, dA$ and the curvature variation energy of [minimum variation surfaces](/minimum-variation-surface/) depend on the geometry, not on the parametrization, and need nonlinear optimization.
- **Local fairing.** Minimize the energy over the control points of one region only, with the rest fixed, to remove a local defect.

## Pitfalls

- **The measure is a design criterion.** No energy defines fairness. A minimum of $E_t$ is the fairest surface only in the sense of $E_t$, and designers judge the result by [reflection lines](/reflection-lines/) and curvature plots, which can disagree with the energy.
- **Parametrization dependence.** $E_t$ measures parameter derivatives. A surface with uneven parameter speed is faired toward even speed, which can move the surface in ways that are not wanted, and the same shape with another parametrization gives another result.
- **Too few constraints.** Without data or enough fixed points the affine nets have zero energy, and $M$ is singular on the null space of $C$.
- **Weights.** The result depends on $\lambda$, $\alpha$ and $\beta$. A large weight on smoothness pulls the surface away from the data, and a small one keeps the noise. The weights also depend on the units of the data.
- **Shrinking.** With the membrane energy alone, the surface pulls inward like a soap film and flattens bumps that should stay.
- **Dense assembly.** The matrix $M$ is sparse and banded for B-splines, with bandwidth set by the degrees. Assembling it as a dense matrix wastes time and memory for large nets. Use a sparse [Cholesky factorization](/cholesky-decomposition/) or the [conjugate gradient method](/conjugate-gradient-method/).

## Exercises

1. Show that for a cubic Bezier curve with control values $b_0, \dots, b_3$ on $[0, 1]$, $\int_0^1 (c'')^2 \, dt = 12 (a_0^2 + a_0 a_1 + a_1^2)$ with $a_0 = b_0 - 2 b_1 + b_2$ and $a_1 = b_1 - 2 b_2 + b_3$.
2. In the worked example, verify $E_t(s) = \frac15 (198 s^2 - 432 s + 432)$ from the matrices $G_0$, $G_1$ and $G_2$, and explain by symmetry and Theorem 2 why the four inner heights of the minimizer are equal.
3. Show that the bilinear surface $S = (u, v, u v)$ written as a bicubic Bezier patch minimizes $E_t$ among all bicubic patches with its boundary. Hint: check that $S_{uu} = S_{vv} = 0$ and compute the derivative of $E_t$ along any change of the inner points.
4. Let the constraints fix some control points, with $f$ the indices of the free points and $c$ those of the fixed ones. Show that the system of line L5 reduces to $M_{ff} p_f = b_f - M_{fc} r$, and that $M_{ff}$ is positive definite when the minimizer is unique.

## References
