---
tag: CZJ24B
kind: algorithm
slug: streamline-upwind-petrov-galerkin
name: Streamline upwind Petrov-Galerkin method
aliases:
- SUPG
area: scientific-computing/finite-element-practice
level: core
summary: Adds test functions shifted along the flow direction, which stabilizes convection-dominated problems without losing consistency.
solves: [advection-equation]
model: real-ram
complexity:
  vars: {m: the number of cells of the one-dimensional mesh}
  time: {worst: "Θ(m)"}
  space: {extra: "Θ(m)"}
properties: {deterministic: true, consistent: true, symmetric_matrix: false, nodally_exact_in_1d_with_optimal_tau: true}
history:
  year: 1982
  people: [Alexander N. Brooks, Thomas J. R. Hughes]
  note: Brooks and Hughes published the streamline upwind Petrov-Galerkin formulation in 1982, after the upwind Petrov-Galerkin weights of Christie, Griffiths, Mitchell and Zienkiewicz in 1976.
prereqs: [galerkin-method, finite-element-assembly, upwind-scheme]
see_also: [finite-element-method, upwind-scheme, thomas-algorithm, discontinuous-galerkin-method, navier-stokes-equations, taylor-hood-element, gmres, finite-volume-method]
sources:
  - paper: doi:10.1016/0045-7825(82)90071-8
    title: Alexander N. Brooks and Thomas J. R. Hughes, Streamline upwind/Petrov-Galerkin formulations for convection dominated flows with particular emphasis on the incompressible Navier-Stokes equations, Computer Methods in Applied Mechanics and Engineering 32 (1982) 199-259
    locator: the SUPG weighting functions, the one-dimensional optimal parameter and the advection-diffusion examples
  - paper: doi:10.1002/nme.1620100617
    title: I. Christie, D. F. Griffiths, A. R. Mitchell and O. C. Zienkiewicz, Finite element methods for second order differential equations with significant first derivatives, International Journal for Numerical Methods in Engineering 10(6) (1976) 1389-1396
    locator: asymmetric linear and quadratic weighting functions for the two-point convection-diffusion problem
  - paper: doi:10.1016/0045-7825(84)90158-0
    title: Claes Johnson, Uno Nävert and Juhani Pitkäranta, Finite element methods for linear hyperbolic problems, Computer Methods in Applied Mechanics and Engineering 45 (1984) 285-312
    locator: the streamline diffusion method and its error estimate of order h^(k+1/2)
  - book: isbn:9783540344667
    title: Hans-Görg Roos, Martin Stynes and Lutz Tobiska, Robust Numerical Methods for Singularly Perturbed Differential Equations, second edition, Springer Series in Computational Mathematics 24, 2008
    locator: Part III (convection-diffusion problems in several dimensions), the streamline diffusion finite element method
---

The streamline upwind Petrov-Galerkin method (SUPG) solves convection-diffusion problems such as $-\varepsilon\Delta u + a\cdot\nabla u = f$ with continuous finite elements when the convection $a$ is much stronger than the diffusion $\varepsilon$. On each cell it tests the equation with $v + \tau\,a\cdot\nabla v$ in place of $v$, which adds diffusion only along the streamlines, and because the added term multiplies the residual of the equation, the exact solution still satisfies the discrete equations. On coarse meshes the plain [Galerkin method](/galerkin-method/) gives node-to-node oscillations, and SUPG removes most of them while it keeps the order of accuracy that plain upwinding loses.

## In plain words

Smoke carried by a strong wind spreads only a little. A computer model that treats upwind and downwind points the same way can produce a pattern of high and low values that alternate along the wind, which is not in the real flow. The old fix is to look only upwind, but that smears the smoke as if the air were thick. SUPG gives each test point a small lean into the wind. The lean is large where the wind is strong compared to the spreading and almost zero where it is weak. Because the lean is applied to how badly the equation fails, and not to the solution itself, a correct answer still passes the test. So the method stays accurate where the solution is smooth and stays calm near steep fronts.

## The problem

**Input.** A domain $\Omega$, a diffusion coefficient $\varepsilon > 0$, a velocity field $a$, a source $f$, boundary values $g$, and a mesh $\mathcal{T}_h$ with a continuous finite element space $V_h$ of degree $k$. The reference code takes $\Omega = (0, 1)$, constant $\varepsilon$ and $a \ne 0$, $m$ cells of width $h = 1/m$, P1 elements, and $u(0) = g_0$, $u(1) = g_1$.

**Output.** $u_h \in V_h$ with the boundary values and

$$\varepsilon(\nabla u_h, \nabla v) + (a\cdot\nabla u_h, v) + \sum_{K}\tau_K\bigl(-\varepsilon\Delta u_h + a\cdot\nabla u_h - f,\ a\cdot\nabla v\bigr)_K = (f, v)$$

for all $v \in V_h$ that vanish on the boundary. The cell Péclet number is $\mathrm{Pe}_K = |a|h_K/(2\varepsilon)$. Some sources omit the factor 2 and write $|a|h_K/\varepsilon$. The problem is convection dominated when $\mathrm{Pe}_K > 1$.

## The algorithm

The standard parameter is

$$\tau_K = \frac{h_K}{2|a|}\Bigl(\coth\mathrm{Pe}_K - \frac{1}{\mathrm{Pe}_K}\Bigr).$$

In one dimension with P1 elements and constant data this choice is proved to give the exact solution at the nodes (Claim 4 of the proof). In several dimensions and for higher degree it is a heuristic choice, and other formulas such as $\tau_K = \min\bigl(h_K/(2|a|),\ h_K^2/(12\varepsilon)\bigr)$ behave about the same. The steps for the one-dimensional P1 case are:

```pseudo id=main
SUPG(eps, a, f, m, g0, g1)                    ▷ -eps u'' + a u' = f on (0, 1), P1 on m cells
L1  h <- 1/m; Pe <- |a| h / (2 eps)
L2  tau <- (h / (2 |a|)) (coth(Pe) - 1/Pe)     ▷ use a series when Pe is small
L3  for j <- 0 to m - 1 do                     ▷ cell [x_j, x_{j+1}] with local hats phi_0, phi_1
L4      A_K[r, s] <- (eps + tau a^2) (phi_s', phi_r')_K + a (phi_s', phi_r)_K   for r, s in {0, 1}
L5      b_K[r] <- (f, phi_r + tau a phi_r')_K by quadrature
L6      add A_K into rows and columns j, j + 1 of the tridiagonal arrays, and b_K into the right side
L7  move the known values U_0 = g0 and U_m = g1 to the right side of rows 1 and m - 1
L8  (U_1, ..., U_{m-1}) <- THOMAS(sub, diag, super, rhs) on rows 1 to m - 1
L9  return (g0, U_1, ..., U_{m-1}, g1)
```

Line L4 uses the fact that a P1 function has $u_h'' = 0$ inside a cell, so the SUPG term $\tau(-\varepsilon u_h'' + a u_h' - f, a v')$ becomes $\tau a^2(u_h', v')$ on the matrix side and $\tau(f, a v')$ on the load side. In 1D with P1 elements, SUPG therefore equals the Galerkin method with the diffusion $\varepsilon + \tau a^2$ and a corrected load. Lines L6 to L8 are the [assembly](/finite-element-assembly/) loop and the [Thomas algorithm](/thomas-algorithm/), because the matrix is tridiagonal. For elements of degree 2 or more, line L4 must keep the term $-\varepsilon\Delta u_h$, since it is not zero inside the cell.

## Example

Take $\varepsilon = 0.01$, $a = 1$, $f = 0$, $u(0) = 0$, $u(1) = 1$ and $m = 10$, so $h = 0.1$ and $\mathrm{Pe} = 5$. The exact solution $u = (e^{100x} - 1)/(e^{100} - 1)$ is almost $0$ up to a boundary layer of width about $0.01$ at $x = 1$.

For the Galerkin method ($\tau = 0$), each interior row reads $-0.6\,U_{i-1} + 0.2\,U_i + 0.4\,U_{i+1} = 0$. The characteristic equation $0.4\rho^2 + 0.2\rho - 0.6 = 0$ has the roots $\rho = 1$ and $\rho = -3/2$. In general the second root is $(1 + \mathrm{Pe})/(1 - \mathrm{Pe})$, which is negative exactly when $\mathrm{Pe} > 1$. So $U_i = C\bigl((-3/2)^i - 1\bigr)$ with $C = 1/\bigl((3/2)^{10} - 1\bigr) = 0.017648$, and the sign alternates from node to node.

For SUPG, line L2 gives $\tau = 0.05\,(\coth 5 - 0.2) = 0.0400045$, so the diffusion in line L4 is $\varepsilon + \tau = 0.05\coth 5 = 0.0500454$. The second root becomes $(1 + \tanh 5)/(1 - \tanh 5) = e^{10}$, which is the ratio $e^{ah/\varepsilon}$ of the exact solution from one node to the next.

| $x$ | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 |
|---|---|---|---|---|---|---|---|---|---|
| Galerkin | -0.0441 | 0.0221 | -0.0772 | 0.0717 | -0.1517 | 0.1834 | -0.3192 | 0.4346 | -0.6961 |
| SUPG | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000454 |
| exact | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000454 |

With $f = 1$ and $u(0) = u(1) = 0$ on the same mesh, the Galerkin values at $x = 0.1, \ldots, 0.9$ are $0.1441$, $0.1779$, $0.3772$, $0.3283$, $0.6517$, $0.4166$, $1.0192$, $0.3654$, $1.5961$, while the exact solution is close to $x$ there. SUPG reproduces the exact nodal values up to rounding (a difference of $2.2 \times 10^{-16}$).

**Smooth data (measurement).** For $u = \sin(\pi x)$ with $a = 1$, the maximum nodal error of SUPG at $m = 8, 16, 32, 64$ is $2.75 \times 10^{-6}$, $1.72 \times 10^{-7}$, $1.08 \times 10^{-8}$, $6.74 \times 10^{-10}$ for $\varepsilon = 1$, an observed order of 4.0. The Galerkin errors are $9.69 \times 10^{-4}$, $2.44 \times 10^{-4}$, $6.10 \times 10^{-5}$, $1.52 \times 10^{-5}$, order 2. For $\varepsilon = 0.01$ the SUPG errors are $6.01 \times 10^{-3}$, $9.90 \times 10^{-4}$, $1.01 \times 10^{-4}$, $7.44 \times 10^{-6}$, with observed orders 2.6, 3.3 and 3.8 before the asymptotic range.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). It shows four facts. First, the method is consistent: the exact solution makes the residual zero on every cell, so it satisfies the SUPG equations, and the error is orthogonal to $V_h$ in the SUPG form. Second, for P1 elements the SUPG matrix is the Galerkin matrix with diffusion $\varepsilon' = \varepsilon + \tau a^2$. Third, the form is coercive with $B(z, z) = \varepsilon'\|z'\|^2$ on functions that vanish at the ends, so the solution exists and is unique, and when $\varepsilon' \ge |a|h/2$ the matrix is diagonally dominant and the Thomas algorithm meets no zero pivot. Fourth, with the $\tau$ of line L2, $\varepsilon' = \frac{|a|h}{2}\coth\mathrm{Pe}$, and the discrete equations hold exactly for $1$, $x$ and $e^{ax/\varepsilon}$, so the nodal values are exact for a constant $f$.

## Complexity

In the 1D code each cell costs a constant amount of work: four matrix entries and five quadrature points for the load. The loop of lines L3 to L6 costs $\Theta(m)$, and the Thomas algorithm in line L8 does one forward and one backward pass, also $\Theta(m)$. So the total is $\Theta(m)$ time in the worst case on the real-RAM model, with $\Theta(m)$ extra memory for the four arrays. In several dimensions, SUPG has the same cost per cell as the Galerkin assembly, up to a constant, and the same sparsity pattern. The matrix is not symmetric, so the solve uses a sparse direct method or [GMRES](/gmres/) in place of conjugate gradients.

## Properties

- **Consistency (theorem).** The exact solution satisfies the discrete equations, so the error obeys Galerkin orthogonality for the SUPG form. Plain upwinding with diffusion $\varepsilon + |a|h/2$ is not consistent and is only first order.
- **Error bound (theorem).** For degree $k$, $\varepsilon \le h$ and $\tau_K \sim h_K/|a|$, the error in the streamline diffusion norm $\bigl(\varepsilon|v|_1^2 + \sum_K\tau_K\|a\cdot\nabla v\|_K^2\bigr)^{1/2}$ is $O(h^{k+1/2})$ with a constant that does not depend on $\varepsilon$ (Johnson, Nävert and Pitkäranta).
- **Nodal exactness in 1D (theorem).** With the coth formula, P1 elements and constant $\varepsilon$, $a$ and $f$, the nodal values are exact for every $h$. This is the Il'in-Allen-Southwell scheme written as a finite element method.
- **No maximum principle in general.** In two and three dimensions SUPG still shows small overshoots and undershoots near sharp layers, in particular across the flow.
- **Nonsymmetric matrix.** The convection term makes the matrix nonsymmetric even without the stabilization.

## Variants and improvements

- **Streamline diffusion.** The method of Johnson and Nävert drops the residual and keeps only $\tau(a\cdot\nabla u_h, a\cdot\nabla v)$ and the matching load term for P1, and it is often the same method under another name.
- **Galerkin least squares (GLS).** Tests with $\tau L v$ for the whole operator $L$, including the diffusion part. For Stokes flow with equal-order velocity and pressure, the same idea (PSPG) gives a stable method although the pair fails the [inf-sup condition](/inf-sup-condition/).
- **Shock capturing.** Adds a nonlinear crosswind diffusion that depends on the residual and reduces the overshoots near layers. These methods are called SOLD methods (spurious oscillations at layers diminishing).
- **Residual-free bubbles and variational multiscale.** Derive $\tau$ from a local solve with bubble functions, which explains the coth formula.
- **Continuous interior penalty and local projection.** Penalize jumps of the gradient across faces or fluctuations of a projection in place of the residual. They have a symmetric stabilization term and are easier to use in time-dependent problems.
- **Time-dependent problems.** Common choices of $\tau$ include the time step, for example $\tau = \bigl((2/\Delta t)^2 + (2|a|/h)^2 + (4\varepsilon/h^2)^2\bigr)^{-1/2}$. This is a heuristic.
- **[Discontinuous Galerkin](/discontinuous-galerkin-method/).** Puts the upwinding into the numerical flux on faces in place of the test function.

## When to use it

Use SUPG when a continuous finite element code must solve a transport problem with $\mathrm{Pe}_K > 1$ on part of the mesh, for example the momentum equation of the [Navier-Stokes equations](/navier-stokes-equations/) at high Reynolds number or a temperature carried by a fast flow. It keeps the mesh, the element and the order of the Galerkin method and adds a small amount of code per cell. When strict bounds such as $0 \le u \le 1$ matter more than accuracy, a monotone scheme such as a first-order [upwind scheme](/upwind-scheme/), a [finite volume method](/finite-volume-method/) with limiters, or algebraic flux correction is safer. When the problem has steep fronts and needs local conservation, discontinuous Galerkin methods are the usual choice.

## Pitfalls

- **Dropping the second-order term.** For elements of degree 2 or more, a code that copies line L4 and leaves out $-\varepsilon\Delta u_h$ in the residual is no longer consistent, and the convergence order drops. Keep the full residual on each cell.
- **Stabilizing the load wrongly.** Line L5 must test $f$ with $\phi_r + \tau a\phi_r'$. If it tests with $\phi_r$ only, the method is the inconsistent "artificial diffusion" scheme, and the observed order falls to 1 when $f$ is not constant.
- **Mixing Péclet conventions.** A formula for $\tau$ written for $\mathrm{Pe} = |a|h/\varepsilon$ and evaluated with $\mathrm{Pe} = |a|h/(2\varepsilon)$ gives the wrong amount of diffusion. Check which definition the source uses.
- **Cancellation in the coth formula.** For small $\mathrm{Pe}$, $\coth\mathrm{Pe} - 1/\mathrm{Pe}$ loses all digits in floating point. Use the series $\mathrm{Pe}/3 - \mathrm{Pe}^3/45$ there, as line L2 says.
- **Using conjugate gradients.** The matrix is not symmetric, so conjugate gradients can fail or converge to a wrong vector. Use GMRES, BiCGSTAB or a direct solver.
- **Expecting monotone results in 2D.** The 1D nodal exactness does not carry over. Small oscillations near layers remain, and if they are not acceptable a shock-capturing term is needed.

## Implementations

## History

D. N. de G. Allen and Richard Southwell used an exponentially fitted difference scheme for viscous flow past a cylinder in 1955, and A. M. Il'in analyzed such schemes in 1969. In 1976 Christie, Griffiths, Mitchell and Zienkiewicz showed that asymmetric linear and quadratic test functions remove the Galerkin oscillations of the two-point problem. Hughes and Brooks proposed streamline upwinding without crosswind diffusion in 1979, and their 1982 paper gave SUPG in its consistent Petrov-Galerkin form, with applications to the incompressible Navier-Stokes equations. Johnson, Nävert and Pitkäranta proved the $h^{k+1/2}$ error bound in 1984. Hughes, Franca and Hulbert generalized the method to Galerkin least squares in 1989.

## References
