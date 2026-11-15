---
tag: Q3981F
kind: definition
slug: lyapunov-function
name: Lyapunov function
aliases:
- Lyapunov candidate function
area: control/stability
level: core
summary: A Lyapunov function of an equilibrium is a positive definite function that does not increase along the solutions. Its level sets trap the state, which proves Lyapunov stability.
prereqs: [lyapunov-stability, positive-definite-matrix]
see_also: [lyapunov-direct-method, lasalle-invariance-principle, lyapunov-theorem-for-linear-systems, converse-lyapunov-theorem, control-lyapunov-function, lie-derivative, sum-of-squares-programming, region-of-attraction]
sources:
  - paper: doi:10.1080/00207179208934253
    title: "A. M. Lyapunov, The general problem of the stability of motion, translated by A. T. Fuller, International Journal of Control 55(3), 531-773, 1992"
    locator: the second method, in which a function of the state with a sign-definite derivative along the motion decides stability
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.1 (Lyapunov functions for autonomous systems, the pendulum examples and the variable gradient method), Section 4.3 (quadratic functions for linear systems) and Section 4.4 (bounds by class K functions)
---

A Lyapunov function is a scalar function of the state that is zero at an equilibrium, positive everywhere else near it, and does not increase along the solutions of the differential equation. The function plays the part of an energy: if the energy cannot grow, a solution that starts with little energy stays where the energy is small, that is, near the equilibrium. Finding such a function proves [Lyapunov stability](/lyapunov-stability/) without solving the equation; this is [Lyapunov's direct method](/lyapunov-direct-method/). A strict decrease gives [asymptotic stability](/asymptotic-stability/). This page defines the function and its variants; the theorems that use it are on their own pages.

## Definition

**Setting.** $\dot x = f(x)$ with $f : D \to \mathbb{R}^n$ locally Lipschitz on a domain $D \subseteq \mathbb{R}^n$ that contains the origin, and $f(0) = 0$.

**Derivative along solutions.** For a continuously differentiable $V : D \to \mathbb{R}$, write

$$\dot V(x) = \nabla V(x) \cdot f(x) = \sum_{i=1}^n \frac{\partial V}{\partial x_i}(x)\, f_i(x) .$$

This is the [Lie derivative](/lie-derivative/) $L_f V$. Along a solution $x(t)$, the chain rule gives $\frac{d}{dt} V(x(t)) = \dot V(x(t))$. So $\dot V$ is computed from $f$ alone, without any solution.

**Sign words.** A function $V$ with $V(0) = 0$ is *positive definite* on $D$ if $V(x) > 0$ for all $x \in D \setminus \{0\}$, and *positive semidefinite* if $V(x) \ge 0$. It is negative definite or semidefinite if $-V$ is positive definite or semidefinite. For a quadratic form $V = x^T P x$ with $P$ symmetric, $V$ is positive definite if and only if $P > 0$ (see [positive definite matrix](/positive-definite-matrix/)).

**Definition.** A continuously differentiable function $V : D \to \mathbb{R}$ is a *Lyapunov function* for the equilibrium $x = 0$ of $\dot x = f(x)$ on $D$ if

1. $V(0) = 0$ and $V(x) > 0$ for $x \in D \setminus \{0\}$, and
2. $\dot V(x) \le 0$ for all $x \in D$.

It is a *strict Lyapunov function* if also $\dot V(x) < 0$ for $x \in D \setminus \{0\}$. It is *radially unbounded* if $D = \mathbb{R}^n$ and $V(x) \to \infty$ as $|x| \to \infty$.

What each kind proves, by the [direct method](/lyapunov-direct-method/): a Lyapunov function proves Lyapunov stability; a strict one proves asymptotic stability; a strict one that is radially unbounded on $\mathbb{R}^n$ proves global asymptotic stability. A Lyapunov function that is not strict can still prove asymptotic stability with the [invariance principle](/lasalle-invariance-principle/).

**Bounds by class K functions.** If $V$ is continuous and positive definite on a ball $B_r = \{|x| < r\}$ in $D$, there are class K functions $\alpha_1, \alpha_2$ on $[0, r)$ with

$$\alpha_1(|x|) \le V(x) \le \alpha_2(|x|) \quad \text{for } |x| < r ,$$

and if $V$ is radially unbounded the functions can be taken of class K-infinity (Khalil 2002, Section 4.4). A strict Lyapunov function has in addition $\dot V(x) \le -\alpha_3(|x|)$ on a smaller ball, for a class K function $\alpha_3$, because $-\dot V$ is continuous and positive definite. The theorems on [exponential stability](/exponential-stability/) and [input-to-state stability](/input-to-state-stability/) are stated with such bounds.

**Level sets.** For $c > 0$, let $\Omega_c$ be the connected component of $\{x \in D : V(x) \le c\}$ that contains the origin. If $\Omega_c$ is bounded and its closure lies in $D$, it is compact and [positively invariant](/positively-invariant-set/): a solution cannot cross the boundary $\{V = c\}$ outward while $V$ does not increase. The level sets shrink to the origin as $c \to 0$. This is the geometric content of the direct method, and the same sets give inner estimates of the [region of attraction](/region-of-attraction/).

**Quadratic Lyapunov functions.** For the linear system $\dot x = A x$ and $V = x^T P x$,

$$\dot V(x) = x^T (A^T P + P A)\, x .$$

So $V$ is a strict Lyapunov function exactly when $P > 0$ and $A^T P + P A < 0$. Such a $P$ exists if and only if $A$ is Hurwitz, and it is found from the [Lyapunov equation](/lyapunov-equation/) $A^T P + P A = -Q$; see [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/). The same $P$ is a strict Lyapunov function near the origin for every nonlinear system $\dot x = f(x)$ with $f$ continuously differentiable and Jacobian $A$ at $0$; this is the proof of the [indirect method](/lyapunov-indirect-method/).

**Ways to find one.** There is no general recipe, but there are standard sources:

- the physical energy, for mechanical and electrical systems;
- a quadratic form from the linearization, valid near the equilibrium;
- the variable gradient method: choose $\nabla V$ with free coefficients so that $\dot V \le 0$, then check that $\nabla V$ is a gradient (Khalil 2002, Section 4.1);
- Krasovskii's choice $V = f(x)^T P f(x)$, which works when the Jacobian $J(x)$ of $f$ satisfies $P J(x) + J(x)^T P \le -Q$ with $P > 0$, $Q > 0$, and when $f(x) = 0$ only at $x = 0$;
- a search over polynomials by [sum-of-squares programming](/sum-of-squares-programming/), which turns the two sign conditions into a semidefinite program.

The [converse Lyapunov theorem](/converse-lyapunov-theorem/) says that a Lyapunov function exists for every asymptotically stable equilibrium of a system with locally Lipschitz $f$, but its proof builds $V$ from the solutions, so it does not give a formula.

## Examples and non-examples

- **Damped pendulum.** $\dot x_1 = x_2$, $\dot x_2 = -\sin x_1 - b x_2$ with $b > 0$. The energy $V = \tfrac12 x_2^2 + 1 - \cos x_1$ is positive definite on $D = \{|x_1| < 2\pi\}$, and $\dot V = x_2 \sin x_1 + x_2(-\sin x_1 - b x_2) = -b x_2^2 \le 0$. So $V$ is a Lyapunov function, and the bottom equilibrium is Lyapunov stable. It is not strict: $\dot V = 0$ on the whole line $x_2 = 0$. The [invariance principle](/lasalle-invariance-principle/) still gives asymptotic stability.
- **A cubic decay.** For $\dot x = -x^3$, $V = x^2/2$ gives $\dot V = -x^4$, a strict and radially unbounded Lyapunov function: the origin is globally asymptotically stable. No quadratic $V$ satisfies $\dot V \le -k_3 |x|^2$ here, since the origin is not exponentially stable.
- **The check matrix.** $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$ and $P = \begin{bmatrix} 5/4 & 1/4 \\ 1/4 & 1/4 \end{bmatrix}$ give $A^T P + P A = -I$ exactly, so $V = \tfrac54 x_1^2 + \tfrac12 x_1 x_2 + \tfrac14 x_2^2$ has $\dot V = -(x_1^2 + x_2^2)$.
- **The wrong quadratic for the same system (non-example).** With $V = x_1^2 + x_2^2$ and the same $A$, $\dot V = 2 x^T A x = -2 x_1 x_2 - 6 x_2^2$. At $x = (-1, 0.1)$ this is $0.2 - 0.06 = 0.14 > 0$. So $|x|^2$ is not a Lyapunov function, although $A$ is Hurwitz. A failed choice of $V$ proves nothing about the system.
- **Not positive definite (non-example).** On $\mathbb{R}^2$, $V = x_1^2$ is zero on the whole $x_2$ axis, so it is only positive semidefinite. It cannot be used in the direct method as it stands, although the invariance principle accepts some such functions.
- **Not radially unbounded.** $V = x_1^2 / (1 + x_1^2) + x_2^2$ is positive definite on $\mathbb{R}^2$, but the level sets $\{V \le c\}$ with $c \ge 1$ are unbounded, because $V < 1 + x_2^2$ for every $x_1$. A strict Lyapunov function of this form does not prove global asymptotic stability; the [direct method](/lyapunov-direct-method/) page gives a system where the conclusion fails.

## Related definitions

- [Control Lyapunov function](/control-lyapunov-function/): for $\dot x = f(x, u)$, a positive definite $V$ such that for each $x \ne 0$ some input makes $\dot V < 0$. It is a design tool.
- [Common Lyapunov function](/common-lyapunov-function/): one $V$ that decreases for each mode of a switched system.
- [Barrier certificate](/barrier-certificate/): a function whose sign separates safe and unsafe states. It proves safety, not stability.
- *ISS-Lyapunov function*: a $V$ with $\dot V \le -\alpha_3(|x|) + \sigma(|u|)$; see [input-to-state stability](/input-to-state-stability/).
- *Chetaev function*: a function that is positive and increasing on a region that touches the equilibrium; it proves instability. It is used on [Lyapunov's indirect method](/lyapunov-indirect-method/).
- [Converse Lyapunov theorem](/converse-lyapunov-theorem/): conditions under which a Lyapunov function must exist.

## References
