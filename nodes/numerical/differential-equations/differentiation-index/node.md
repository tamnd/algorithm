---
tag: HQCXS3
kind: concept
slug: differentiation-index
name: Differentiation index of a DAE
aliases:
- index of a DAE
- DAE index
- differential index
area: numerical/differential-equations
level: advanced
summary: "The least number of times all or part of F(t, y, y') = 0 must be differentiated so that y' is determined as a function of t and y. An ODE has index 0; constrained mechanics has index 3."
prereqs: [differential-algebraic-equations]
see_also: [backward-differentiation-formulas, radau-iia-methods, backward-euler-method, stiff-ode-problem, implicit-runge-kutta-methods, lagrange-multiplier, hamiltonian-systems, ode-initial-value-problem]
sources:
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section VII.1 (the index of differential-algebraic equations; differentiation index and perturbation index, linear equations with constant coefficients, Hessenberg forms)
  - book: isbn:9780898713534
    title: K. E. Brenan, S. L. Campbell and L. R. Petzold, Numerical Solution of Initial-Value Problems in Differential-Algebraic Equations, SIAM Classics in Applied Mathematics 14, 1996
    locator: Chapter 2 (the index, the derivative array, semi-explicit and Hessenberg systems, linear constant coefficient systems)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 9 (index definitions, Hessenberg forms, index reduction)
  - paper: doi:10.1137/0909014
    title: Constantinos C. Pantelides, The consistent initialization of differential-algebraic systems, SIAM Journal on Scientific and Statistical Computing 9(2) (1988) 213-231
    locator: the structural algorithm that decides which equations to differentiate, from the incidence graph
---

The differentiation index of a [differential-algebraic equation](/differential-algebraic-equations/) $F(t, y, y') = 0$ is the smallest number $m$ such that the equations $F = 0$, $\tfrac{d}{dt}F = 0, \ldots, \tfrac{d^m}{dt^m}F = 0$ together determine $y'$ uniquely as a continuous function of $t$ and $y$. Then $y$ solves an ODE, the underlying ODE. An [ODE](/ode-initial-value-problem/) has index 0. The index tells how many hidden constraints the initial values must satisfy, how strongly the solution reacts to perturbations, and how much accuracy standard implicit methods lose; problems of index 2 and higher are much harder than index 1.

## In plain words

A system with built-in rules, such as a pendulum whose bob must stay on a circle, has some quantities that are never given a rate of change, like the force in the rod. To compute them you can take the rule and ask how it changes in time, and how that change changes, and so on, until every quantity has a formula for its rate of change. The number of such rounds is the index. A rule that fixes a hidden quantity directly needs one round. A rule on position that only fixes a force through the acceleration needs three. More rounds mean more hidden rules for the starting values, and a stronger magnification of small errors, because each round amounts to differentiating noisy data.

## The idea

**Notation.** $F : [t_0, T] \times \mathbb{R}^d \times \mathbb{R}^d \to \mathbb{R}^d$ smooth, solution $y(t) \in \mathbb{R}^d$. In semi-explicit form $y' = f(t, y, z)$, $0 = g(t, y, z)$, with differential variables $y$ and algebraic variables $z$.

**Definition (differentiation index).** Form the derivative array: the system $\frac{d^j}{dt^j}F(t, y, y') = 0$ for $j = 0, \ldots, m$, viewed as equations in the unknowns $y', y'', \ldots, y^{(m+1)}$ for given $(t, y)$. The index is the least $m$ for which this system determines $y'$ uniquely (not necessarily the higher derivatives) as a continuous function of $(t, y)$ on the relevant set (Brenan, Campbell and Petzold 1996, Chapter 2; HW II, Section VII.1).

**Semi-explicit rules.**

- **Index 1:** $g_z$ is nonsingular. One differentiation of $0 = g$ gives $g_t + g_yy' + g_zz' = 0$, which can be solved for $z'$.
- **Index 2 (Hessenberg):** $g$ does not depend on $z$, and $g_yf_z$ is nonsingular. Differentiating $0 = g(t, y)$ once gives the hidden constraint $0 = g_t + g_yf(t, y, z)$, which has index 1 in $z$.
- **Index 3 (Hessenberg):** $x' = f(t, x, y, z)$, $y' = h(t, x, y)$, $0 = g(t, y)$ with $g_yh_xf_z$ nonsingular. Two hidden constraints appear, one after each of the first two differentiations.

**Linear constant coefficient case.** For $Ey' = Ay + q(t)$ with a regular pencil ($\det(\lambda E - A) \not\equiv 0$), there are nonsingular $P, Q$ with $PEQ = \operatorname{diag}(I, N)$ and $PAQ = \operatorname{diag}(C, I)$, $N$ nilpotent (Weierstrass-Kronecker form). The fast part solves $Nw' = w + r(t)$, and repeated substitution gives $w = -\sum_{i=0}^{\nu-1}N^ir^{(i)}(t)$, where $\nu$ is the nilpotency index of $N$ ($N^\nu = 0 \ne N^{\nu-1}$). The differentiation index equals $\nu$, and the solution depends on $\nu - 1$ derivatives of the data.

**Other indices.** The **perturbation index** is the least $k$ such that the solution of $F(t, \hat y, \hat y') = \delta(t)$ satisfies $\|\hat y(t) - y(t)\| \le C\big(\|\hat y(t_0) - y(t_0)\| + \max\|\delta\| + \max\|\delta'\| + \cdots + \max\|\delta^{(k-1)}\|\big)$ on $[t_0, T]$; it measures sensitivity directly. It equals the differentiation index for linear constant coefficient and for Hessenberg systems, but the two can differ in general (HW II, Section VII.1). The **structural index**, computed by Pantelides' graph algorithm from the sparsity pattern alone, can underestimate the true index when cancellations make a Jacobian singular that is generically nonsingular. The tractability index (März) and the strangeness index (Kunkel and Mehrmann) are further variants designed for linear time-varying and over- or underdetermined systems.

**Why it matters numerically.**

- *Initial values.* An index $m$ semi-explicit problem has hidden constraints that consistent initial values must satisfy; inconsistent ones make the first steps of BDF or [backward Euler](/backward-euler-method/) produce $O(1)$ errors or fail.
- *Perturbations.* Rounding errors of size $\varepsilon$ in the equations are differentiated $m - 1$ times by the discrete method, which amplifies them by about $h^{1-m}$.
- *Order.* Methods with order $p$ on ODEs keep it on index 1 problems when they are stiffly accurate and stable at infinity, but generally lose order in the algebraic variables for index 2 and 3 ([Radau IIA](/radau-iia-methods/), [BDF](/backward-differentiation-formulas/); HW II, Chapter VII).

## Examples

**Index 1.** $y' = -y + z$, $0 = z - \sin t$. One differentiation of the constraint gives $z' = \cos t$, so $m = 1$.

**A nilpotent chain of index 3.** $z_2' = z_1 + q_1(t)$, $z_3' = z_2 + q_2(t)$, $0 = z_3 + q_3(t)$, which is $Nz' = z + q$ with $N$ the $3 \times 3$ shift matrix ($N^3 = 0$, $N^2 \ne 0$). Solving from the bottom: $z_3 = -q_3$, $z_2 = z_3' - q_2 = -q_3' - q_2$, $z_1 = z_2' - q_1 = -q_3'' - q_2' - q_1$. Every component is fixed by the data; there are no free initial values at all. To get $z_1'$ one needs $q_3'''$, which takes three differentiations of the constraint: index 3, and the solution depends on second derivatives of $q$.

**The pendulum.** With position $q$, velocity $v$, rod force $\lambda$ and unit length: $q' = v$, $v' = -\lambda q - g_0e_2$, $0 = \|q\|^2 - 1$. First derivative of the constraint: $q \cdot v = 0$. Second: $\|v\|^2 - \lambda - g_0q_2 = 0$, which gives $\lambda$ but not yet $\lambda'$. Third: an ODE for $\lambda$. So the index is 3; written with the velocity constraint in place of the position constraint it is 2, and with the formula for $\lambda$ it is 1.

**Incompressible flow.** After space discretization, $u' = -Ku - Gp + b$, $0 = G^Tu$ with discrete gradient $G$ of full column rank: here $g_yf_z = -G^TG$ is nonsingular, so the pressure system has index 2.

**Non-example: a stiff ODE.** $y' = f(y, z)$, $\varepsilon z' = g(y, z)$ with small $\varepsilon > 0$ is an ODE (index 0), however stiff. Its limit $\varepsilon = 0$ is an index 1 DAE when $g_z$ is nonsingular, which is why stiff solvers handle index 1 problems well.

## Where it is used

- Choosing a solver: BDF and Radau IIA codes such as DASSL, IDA and RADAU5 accept index 1 directly and index 2 or 3 only with special error control or in Hessenberg form.
- Index reduction in modelling languages such as Modelica, via Pantelides' algorithm and dummy derivatives.
- Computing consistent initial values from the hidden constraints.
- Error analysis of methods for constrained mechanics, circuit simulation and incompressible flow, where the order of each component depends on the index.

## References
