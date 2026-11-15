---
tag: K4K1P5
kind: definition
slug: common-lyapunov-function
name: Common Lyapunov function
aliases:
- common quadratic Lyapunov function
- CQLF
area: control/discrete-event-and-hybrid-systems
level: advanced
summary: "One Lyapunov function that decreases along every mode of a switched system. If it exists, the origin is GUAS under arbitrary switching."
prereqs: [switched-system, lyapunov-function]
see_also: [joint-spectral-radius, dwell-time-theorem, linear-matrix-inequality, semidefinite-programming, lyapunov-theorem-for-linear-systems, converse-lyapunov-theorem, lie-bracket, sum-of-squares-programming]
sources:
  - book: isbn:9780817642976
    title: Daniel Liberzon, Switching in Systems and Control, Birkhäuser, 2003
    locator: the chapter on stability under arbitrary switching (common Lyapunov functions, the converse theorem, commuting and Lie-algebraic conditions, the counterexample to quadratic common Lyapunov functions)
  - paper: doi:10.1109/37.793443
    title: Daniel Liberzon and A. Stephen Morse, Basic problems in stability and design of switched systems, IEEE Control Systems Magazine 19(5), 59-70, 1999
    locator: the section on stability under arbitrary switching
  - paper: "Kumpati S. Narendra and Jeyendran Balakrishnan, A common Lyapunov function for stable LTI systems with commuting A-matrices, IEEE Transactions on Automatic Control 39(12), 2469-2471, 1994"
    locator: the main theorem and the chain of Lyapunov equations that builds the function
  - paper: "Wijesuriya P. Dayawansa and Clyde F. Martin, A converse Lyapunov theorem for a class of dynamical systems which undergo switching, IEEE Transactions on Automatic Control 44(4), 751-760, 1999"
    locator: the converse theorem and the planar example with no common quadratic Lyapunov function
---

A common Lyapunov function of a [switched system](/switched-system/) is one function that is a [Lyapunov function](/lyapunov-function/) for every mode at the same time. Whatever mode is active, the function goes down along the solution. So it goes down for every switching signal, and the origin is globally uniformly asymptotically stable (GUAS) under arbitrary switching, with no need to know or restrict the switching. For linear modes the usual search is for a quadratic function $x^\top P x$, a common quadratic Lyapunov function, which is the solution of a set of [linear matrix inequalities](/linear-matrix-inequality/). The quadratic form is a special case: a system can have a common Lyapunov function and no quadratic one.

## Definition

Let $\dot x = f_\sigma(x)$ be a switched system with a finite set of modes $\mathcal{P}$, each $f_p$ locally Lipschitz with $f_p(0) = 0$. A $C^1$ function $V : \mathbb{R}^n \to \mathbb{R}$ is a **common Lyapunov function** if there are class $\mathcal{K}_\infty$ functions $\alpha_1, \alpha_2$ and a positive definite continuous function $W$ with

$$\alpha_1(|x|) \le V(x) \le \alpha_2(|x|), \qquad \nabla V(x) \cdot f_p(x) \le -W(x) \quad \text{for all } x \text{ and all } p \in \mathcal{P}.$$

With finitely many modes, it is enough that each $\nabla V \cdot f_p$ is negative definite, since the minimum over $p$ of the bounds is again positive definite. The bound $W$ does not depend on $p$, and this uniformity is what gives a uniform result.

**Common quadratic Lyapunov function (CQLF).** For a switched linear system $\dot x = A_\sigma x$, a CQLF is $V(x) = x^\top P x$ with

$$P = P^\top \succ 0, \qquad A_p^\top P + P A_p \prec 0 \quad \text{for all } p \in \mathcal{P}.$$

For the discrete-time system $x(t+1) = A_{\sigma(t)} x(t)$ the conditions are $A_p^\top P A_p - P \prec 0$ for all $p$. In both cases the conditions are linear in $P$, so a CQLF is found, or shown not to exist, by [semidefinite programming](/semidefinite-programming/).

**Main facts.**

- If a common Lyapunov function exists, the origin is GUAS under arbitrary switching. If $\alpha_1$, $\alpha_2$ and $W$ are quadratic, as for a CQLF, it is globally uniformly exponentially stable (GUES).
- Converse: if the origin is GUAS under arbitrary switching, a common Lyapunov function exists (Dayawansa and Martin 1999). It need not be quadratic.
- A CQLF for $\dot x = A_\sigma x$ is also a Lyapunov function for every convex combination $\sum_p \lambda_p A_p$, because the conditions are linear in $A_p$. So if some convex combination is not Hurwitz, no CQLF exists.

## Examples and non-examples

**Commuting matrices.** Take

$$A_1 = \begin{bmatrix} -1 & 1 \\ 0 & -1 \end{bmatrix}, \qquad A_2 = \begin{bmatrix} -3 & 2 \\ 0 & -3 \end{bmatrix} = 2A_1 - I.$$

They commute and both are Hurwitz. Narendra and Balakrishnan build a CQLF by a chain of [Lyapunov equations](/lyapunov-equation/). First solve $A_1^\top P_1 + P_1 A_1 = -I$, then $A_2^\top P_2 + P_2 A_2 = -P_1$:

$$P_1 = \begin{bmatrix} 1/2 & 1/4 \\ 1/4 & 3/4 \end{bmatrix}, \qquad P_2 = \begin{bmatrix} 1/12 & 5/72 \\ 5/72 & 37/216 \end{bmatrix}.$$

$P_2$ is positive definite (its determinant is $49/5184$). The derivative along mode 2 is $-x^\top P_1 x$, negative definite by construction. Along mode 1,

$$A_1^\top P_2 + P_2 A_1 = \begin{bmatrix} -1/6 & -1/18 \\ -1/18 & -11/54 \end{bmatrix},$$

which is negative definite (its diagonal is negative and its determinant is $5/162 > 0$). So $V(x) = x^\top P_2 x$ is a CQLF and the switched system is GUES. The construction works for any number of commuting Hurwitz matrices, with one more equation per matrix.

**GUES with no CQLF.** Take

$$A_1 = \begin{bmatrix} -1 & -1 \\ 1 & -1 \end{bmatrix}, \qquad A_2 = \begin{bmatrix} -1 & -10 \\ 0.1 & -1 \end{bmatrix}.$$

Both have eigenvalues $-1 \pm j$. Scale $P$ to $\begin{bmatrix} 1 & q \\ q & r \end{bmatrix}$. The condition $A_1^\top P + P A_1 \prec 0$ is $q^2 + (r - 3)^2/8 < 1$, which needs $0.17 < r < 5.83$. The condition for $A_2$ is $q^2 + (r - 300)^2/800 < 100$, which needs $17.2 < r < 582.8$. The two ranges do not meet, so there is no CQLF. Yet this switched system is GUES under arbitrary switching, so by the converse theorem it has a common Lyapunov function that is not quadratic. This is the example of Dayawansa and Martin (1999), in the form that Liberzon (2003) uses.

**Non-examples.**

- A separate Lyapunov function for each mode is not a common Lyapunov function. With $V_p(x) = x^\top P_p x$ for each mode, $V_\sigma$ can jump up at every switch, and the switched system can be unstable. The example on the [switched system](/switched-system/) page has two Hurwitz modes, so each has a quadratic Lyapunov function, but the state grows under one switching rule. Separate functions are useful only with a bound on the switching, as in the [dwell-time theorem](/dwell-time-theorem/).
- A function that goes down along each mode only in the region where that mode is used is a piecewise or multiple Lyapunov function for one state-dependent rule, not a common one. It proves stability for that rule only.
- The Lyapunov function of the average system $\dot x = \frac{1}{2}(A_1 + A_2) x$ is not, in general, a common Lyapunov function of the modes.

## Related definitions

- [Lyapunov function](/lyapunov-function/): the case of one mode. A common Lyapunov function is one function that works for all modes, and the proof of stability is the [direct method](/lyapunov-direct-method/) applied along each piece of the solution.
- [Converse Lyapunov theorem](/converse-lyapunov-theorem/): its switched version is the converse result above.
- [Joint spectral radius](/joint-spectral-radius/): in discrete time, a norm $\|x\|$ with $\|A_p x\| < \|x\|$ for all $p$ and $x \ne 0$ is a common Lyapunov function, and one exists if and only if the joint spectral radius is below 1. A CQLF gives the ellipsoidal norm $\sqrt{x^\top P x}$.
- [Linear matrix inequality](/linear-matrix-inequality/) and [sum-of-squares programming](/sum-of-squares-programming/): the computational tools. Polynomial common Lyapunov functions found by sum-of-squares programming can succeed where the quadratic search fails.
- [Lie bracket](/lie-bracket/): commuting matrices, and more generally Hurwitz matrices that generate a solvable Lie algebra, always have a CQLF (Liberzon 2003).
- [Dwell-time theorem](/dwell-time-theorem/): the alternative when no common function exists. It allows a different Lyapunov function per mode and asks the switching to be slow.

## References
