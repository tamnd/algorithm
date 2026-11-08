---
tag: V93RZ2
kind: problem
slug: differential-algebraic-equations
name: Differential-algebraic equations
aliases:
- DAEs
- descriptor systems
- implicit differential equations
- singular systems of differential equations
area: numerical/differential-equations
level: advanced
summary: "Solve F(t, y, y') = 0 when the Jacobian with respect to y' is singular, for example y' = f(y, z) with a constraint 0 = g(y, z). The index measures how far it is from an ODE."
prereqs: [ode-initial-value-problem, stiff-ode-problem, newton-method-for-systems]
see_also: [differentiation-index, backward-differentiation-formulas, radau-iia-methods, implicit-runge-kutta-methods, backward-euler-method, lagrange-multiplier, hamiltonian-systems, delay-differential-equations]
sources:
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Chapter VI (singular perturbation problems and index 1 problems), Chapter VII (differential-algebraic equations of higher index; the index, multistep and Runge-Kutta methods for index 2 and index 3, constrained mechanical systems)
  - book: isbn:9780898713534
    title: K. E. Brenan, S. L. Campbell and L. R. Petzold, Numerical Solution of Initial-Value Problems in Differential-Algebraic Equations, SIAM Classics in Applied Mathematics 14, 1996
    locator: Chapter 2 (theory of DAEs, the index, semi-explicit and Hessenberg forms), Chapter 3 (multistep methods, BDF convergence), Chapter 4 (one-step methods), Chapter 5 (the code DASSL)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 9 (differential-algebraic equations, index, index reduction and stabilization), Chapter 10 (numerical methods for DAEs)
  - paper: doi:10.1109/TCT.1971.1083221
    title: C. W. Gear, Simultaneous numerical solution of differential-algebraic equations, IEEE Transactions on Circuit Theory 18(1) (1971) 89-95
    locator: the proposal to apply BDF methods directly to the coupled differential and algebraic equations
  - paper: doi:10.1137/0909014
    title: Constantinos C. Pantelides, The consistent initialization of differential-algebraic systems, SIAM Journal on Scientific and Statistical Computing 9(2) (1988) 213-231
    locator: the graph algorithm that finds which equations must be differentiated
---

A differential-algebraic equation (DAE) is a system $F(t, y, y') = 0$ in which some equations contain no derivatives, or more generally in which the Jacobian $\partial F/\partial y'$ is singular, so the system cannot be solved for $y'$ as an [ODE](/ode-initial-value-problem/). Constrained mechanical systems, electrical circuits and chemical processes with equilibrium conditions all lead to DAEs. The [index](/differentiation-index/) counts how many times the constraints must be differentiated to obtain an ODE; it decides which initial values are allowed, how sensitive the solution is to perturbations, and which methods converge. Index 1 problems are solved much like [stiff ODEs](/stiff-ode-problem/) by [BDF](/backward-differentiation-formulas/) or [Radau IIA](/radau-iia-methods/) methods; higher index problems need care or reformulation.

## In plain words

Some systems obey rules that hold at every instant, not just laws of change. A pendulum's bob must stay at a fixed distance from the pivot. The currents into a node of an electrical circuit must add up to zero. Writing such a system down gives a mix of equations: some say how quantities change, others say how they must be related right now. You cannot simply step forward in time as for an ordinary equation, because each step must also satisfy the fixed rules. Some hidden quantities, such as the tension in the pendulum's string, never appear with a rate of change at all; they are fixed only through the rules. The more indirect this link, the harder the problem is for a computer, and the more small errors in the data are magnified.

## Definition

**Notation.** $y(t) \in \mathbb{R}^d$; in semi-explicit form the variables split into differential variables $y \in \mathbb{R}^{d_1}$ and algebraic variables $z \in \mathbb{R}^{d_2}$. Step $h$, values $y_n, z_n$.

**Problem (initial value problem for a DAE).** Given $F : [t_0, T] \times \mathbb{R}^d \times \mathbb{R}^d \to \mathbb{R}^d$ with $\partial F/\partial y'$ singular, and initial data, find $y$ on $[t_0, T]$ with $F(t, y(t), y'(t)) = 0$. The most common form is the **semi-explicit** DAE

$$y' = f(t, y, z), \qquad 0 = g(t, y, z).$$

**Consistent initial values.** Initial data cannot be arbitrary. They must satisfy the constraint $g = 0$ and, for index 2 or more, also the hidden constraints obtained by differentiating it. Finding them is part of the problem.

**Index (informal; see [differentiation index](/differentiation-index/)).** The semi-explicit system has index 1 if $g_z$ is nonsingular near the solution: then $z$ is a function of $(t, y)$ by the implicit function theorem, and the system is an ODE for $y$ in disguise. It has index 2 if $g$ does not depend on $z$ and $g_y f_z$ is nonsingular. Mechanical systems with position constraints have index 3. An ODE has index 0.

**Well-posedness.** For index 1 with smooth $f, g$ and consistent initial values, a unique solution exists locally and depends smoothly on the initial values, as for an ODE. For index $k$, the solution depends on derivatives of the data up to order $k - 1$: a perturbation $\delta(t)$ of size $\varepsilon$ in the equations can produce changes of size $\max\|\delta^{(k-1)}\|$ in the solution (HW II, Section VII.1, the perturbation index).

## Variants

- **Linear constant coefficient DAEs** $Ey' = Ay + q(t)$ with singular $E$. If the matrix pencil $(E, A)$ is regular ($\det(\lambda E - A) \not\equiv 0$), the Weierstrass-Kronecker canonical form splits the system into an ODE and a nilpotent part $Nw' = w + r(t)$, whose solution is $w = -\sum_{i<\nu}N^ir^{(i)}$; the nilpotency index $\nu$ is the index.
- **Hessenberg forms.** Index 2: $y' = f(y, z)$, $0 = g(y)$ with $g_yf_z$ nonsingular. Index 3: $x' = f(x, y, z)$, $y' = h(x, y)$, $0 = g(y)$ with $g_yh_xf_z$ nonsingular. Constrained mechanics is index 3 Hessenberg.
- **Singularly perturbed problems.** $y' = f(y, z)$, $\varepsilon z' = g(y, z)$ is a stiff ODE whose limit $\varepsilon \to 0$ is a semi-explicit DAE; the theory of index 1 problems and of stiff problems meet here (HW II, Chapter VI).
- **Fully implicit** $F(t, y, y') = 0$, the general form handled by codes such as DASSL and IDA.
- **Partial differential-algebraic equations**, such as the incompressible [Navier-Stokes equations](/navier-stokes-equations/), where the pressure is an algebraic variable enforcing $\nabla \cdot u = 0$; after space discretization they are index 2 DAEs.

## Examples

**Index 1.** $y' = -y + z$, $0 = z - \sin t$. Here $g_z = 1$, so $z = \sin t$ can be eliminated and the problem becomes the ODE $y' = -y + \sin t$.

**The pendulum, index 3.** A unit mass on a rod of unit length in Cartesian coordinates $(q_1, q_2)$, velocity $(v_1, v_2)$, gravity $g_0$ and the rod force $\lambda$ as algebraic variable:

$$q_1' = v_1, \quad q_2' = v_2, \quad v_1' = -\lambda q_1, \quad v_2' = -\lambda q_2 - g_0, \quad 0 = q_1^2 + q_2^2 - 1.$$

Differentiating the constraint once gives the hidden velocity constraint $q_1v_1 + q_2v_2 = 0$ (index 2 form), and again gives $\lambda = v_1^2 + v_2^2 - g_0q_2$ (index 1 form). One more differentiation would give an ODE for $\lambda$, so the original system has index 3. Consistent initial values must satisfy both the position and the velocity constraint.

**Backward Euler on an index 3 problem.** The system $y_1' = y_2$, $y_2' = z$, $0 = y_1 - e^t$ has index 3 and the solution $y_1 = y_2 = z = e^t$. [Backward Euler](/backward-euler-method/) with consistent $y_2(0) = 1$ gives $y_{1,n} = e^{t_n}$, $y_{2,n} = (e^{t_n} - e^{t_{n-1}})/h$ and $z_n = (y_{2,n} - y_{2,n-1})/h$. The errors $z_n - z(t_n)$ for the first three steps are:

| $h$ | $n = 1$ | $n = 2$ | $n = 3$ |
|---|---|---|---|
| 0.1 | $-0.5881$ | $-0.1153$ | $-0.1274$ |
| 0.01 | $-0.5084$ | $-0.0101$ | $-0.0102$ |
| 0.001 | $-0.5008$ | $-0.0010$ | $-0.0010$ |

The first value of $z$ has an error near $-\tfrac12$ that does not go to zero with $h$, because $z_1 = ((e^h - 1)/h - 1)/h \to \tfrac12$. From the second step on, the error is $O(h)$. If the values of the constraint are perturbed by $10^{-10}$ (rounding level), the error in $z$ over steps 3 to 29 is $1.3 \cdot 10^{-2}$ at $h = 10^{-2}$, $1.2 \cdot 10^{-3}$ at $h = 10^{-3}$, and $1.9 \cdot 10^{-2}$ at $h = 10^{-4}$: the perturbation enters $z$ multiplied by about $h^{-2}$, the signature of index 3.

**Non-example.** $y' = f(t, y)$ written as $F(t, y, y') = y' - f(t, y) = 0$ has $\partial F/\partial y' = I$, nonsingular: an ODE, index 0.

## Known algorithms

- **BDF methods** applied directly to $F(t, y, y') = 0$ by replacing $y'$ with the BDF difference, Gear's 1971 proposal. A $k$-step BDF with $k \le 6$ converges with order $k$ for index 1, and for semi-explicit index 2 problems with constant steps (Brenan, Campbell and Petzold 1996, Chapter 3). Codes: DASSL, DASPK, IDA.
- **Radau IIA** collocation methods (code RADAU5): for index 1 the order $2s - 1$ of the ODE case is kept in both components; for index 2 and 3 the algebraic components converge with reduced order (HW II, Sections VI.1 and VII.4). The stiff accuracy ($b^T$ equals the last row of $A$) is what makes the numerical solution satisfy the constraint at each step.
- **Index reduction.** Differentiate the constraints until the index is 1 or 0. The structural algorithm of Pantelides (1988) finds, from the sparsity graph of the equations, which equations to differentiate; dummy derivatives (Mattsson and Söderlind 1993) then select variables to keep the result square. The differentiated system drifts away from the original constraints, which is corrected by projection or by stabilization (Baumgarte's method adds a damping combination of the lost constraints).
- **Formulations for mechanics.** Solve the index 2 form (velocity constraints) with projection onto the position constraint, or use coordinate partitioning to integrate an ODE in local minimal coordinates. For Hamiltonian systems with holonomic constraints, the SHAKE and RATTLE methods are [symplectic](/symplectic-integrators/) and keep the constraints exactly.

## Bounds

- **Order reduction (proved).** Methods that have order $p$ for ODEs may have lower order on DAEs: for index $k$ Hessenberg problems, many implicit Runge-Kutta methods lose about $k - 1$ orders in the algebraic variables, and the stage order matters, not just the classical order (HW II, Chapter VII).
- **Sensitivity (proved for linear constant coefficient problems).** With index $\nu$ the solution involves derivatives of the data up to order $\nu - 1$, so any method that uses only function values loses up to $\nu - 1$ orders of $h$ in the effect of rounding errors: an error $\varepsilon$ in the equations gives errors of order $\varepsilon h^{1-\nu}$, as in the table above for $\nu = 3$.
- **Cost per step.** An implicit method needs a Newton iteration on the full system of size $d$ per step (BDF) or $sd$ (an $s$-stage Runge-Kutta method), with the iteration matrix built from $\partial F/\partial y'$ and $\partial F/\partial y$; the iteration matrix is nonsingular for small $h$ when the index is 1, and its condition number grows like $h^{-k}$ for index $k$.

## Reductions

- **Index 1 to ODE.** Solve $0 = g(t, y, z)$ for $z = G(t, y)$ and substitute.
- **Higher index to lower index.** Each differentiation of the constraints lowers the index by one, at the price of drift off the original constraint manifold.
- **To stiff ODEs.** Replacing $0 = g$ by $\varepsilon z' = g$ gives a stiff ODE whose solution approaches that of the index 1 DAE as $\varepsilon \to 0$; this is how many stiff ODE results transfer to DAEs.

## Applications

Multibody mechanics (vehicle dynamics, robotics, biomechanics) with holonomic constraints; electrical circuit simulation, where modified nodal analysis produces DAEs of index 1 or 2; chemical process engineering with equilibrium and conservation constraints; incompressible fluid flow after space discretization; power networks; and optimal control, where the necessary conditions form a DAE in the state, costate and control.

## References
