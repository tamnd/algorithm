---
tag: P58CEA
kind: definition
slug: lipschitz-condition
name: Lipschitz condition
aliases:
- Lipschitz continuity
- Lipschitz constant
area: numerical/differential-equations
level: intro
summary: "f satisfies a Lipschitz condition in y with constant L when |f(t, u) - f(t, v)| <= L |u - v| for all u, v. It gives existence, uniqueness and error bounds for the IVP."
prereqs: []
see_also: [ode-initial-value-problem, picard-lindelof-theorem, gronwall-inequality, global-error, stiff-ode-problem, euler-method, picard-iteration, banach-fixed-point-theorem]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section I.7 (the Lipschitz condition and existence theory) and Section I.10 (differential inequalities, logarithmic norms and one-sided Lipschitz estimates)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 1, Section 1.1 (the Lipschitz condition)
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.12 (one-sided Lipschitz condition and B-stability)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 5 (Lipschitz continuity and well-posedness of the initial value problem)
---

A function $f(t, y)$ satisfies a Lipschitz condition in $y$ when the change of $f$ is at most a fixed constant $L$ times the change of $y$, uniformly in $t$. It is the standard hypothesis of the [initial value problem](/ode-initial-value-problem/) $y' = f(t, y)$: with it, the solution exists, is unique ([Picard-Lindelöf theorem](/picard-lindelof-theorem/)) and depends continuously on the data, and the [global error](/global-error/) of a convergent method is bounded by a constant that contains $e^{L(T - t_0)}$. A large $L$ with strongly damped solutions is the mark of a [stiff problem](/stiff-ode-problem/), where the one-sided version below gives the useful bound.

## Definition

Let $\|\cdot\|$ be a norm on $\mathbb{R}^d$ and $D \subseteq \mathbb{R} \times \mathbb{R}^d$. A function $f : D \to \mathbb{R}^d$ **satisfies a Lipschitz condition in $y$ on $D$ with constant $L \ge 0$** when

$$\|f(t, u) - f(t, v)\| \le L\, \|u - v\| \qquad \text{for all } (t, u), (t, v) \in D.$$

The smallest such $L$ is the **Lipschitz constant** of $f$ on $D$. The condition is **global** when $D = [t_0, T] \times \mathbb{R}^d$. It is **local** when each point of $D$ has a neighbourhood on which it holds with some constant. The same words apply to a function $g$ of $y$ alone.

**The choice of norm.** All norms on $\mathbb{R}^d$ are equivalent: $c_1 \|u\|_a \le \|u\|_b \le c_2 \|u\|_a$. So $f$ is Lipschitz in one norm if and only if it is Lipschitz in each other norm, but the constant can change, by a factor up to $c_2 / c_1$.

**A test with derivatives.** Let $f$ be continuously differentiable in $y$, let the $y$-sections $\{u : (t, u) \in D\}$ be convex, and let $\|f_y(t, u)\| \le L$ on $D$, where $f_y = \partial f / \partial y$ and the matrix norm is the one induced by the vector norm. Then $f$ is Lipschitz in $y$ on $D$ with constant $L$.

*Proof.* For $(t, u), (t, v) \in D$, the segment from $v$ to $u$ stays in $D$, and

$$f(t, u) - f(t, v) = \int_0^1 f_y\bigl(t, v + s(u - v)\bigr)\,(u - v)\, ds,$$

so $\|f(t, u) - f(t, v)\| \le \int_0^1 L \|u - v\|\, ds = L\|u - v\|$. $\square$

Conversely, a function that is Lipschitz with constant $L$ and differentiable in $y$ has $\|f_y\| \le L$ at each interior point, so for $C^1$ functions on convex sets the Lipschitz constant equals $\sup \|f_y\|$. A $C^1$ function is locally Lipschitz on an open set, because $f_y$ is bounded on each closed ball inside it.

**One-sided Lipschitz condition.** Let $\langle \cdot, \cdot \rangle$ be an inner product with norm $\|\cdot\|$. The function $f$ satisfies a **one-sided Lipschitz condition** with constant $\nu \in \mathbb{R}$ when

$$\langle f(t, u) - f(t, v),\, u - v \rangle \le \nu\, \|u - v\|^2 \qquad \text{for all } (t, u), (t, v) \in D.$$

Here $\nu$ may be negative. A Lipschitz function satisfies it with $\nu = L$, by the Cauchy-Schwarz inequality, but $\nu$ can be much smaller than $L$. For two solutions $y$ and $z$ of $y' = f(t, y)$, the derivative of $\|y - z\|^2$ is $2\langle f(t, y) - f(t, z), y - z \rangle \le 2\nu \|y - z\|^2$, so $\|y(t) - z(t)\| \le e^{\nu(t - t_0)} \|y(t_0) - z(t_0)\|$ (HNW I, Section I.10). For $f(t, y) = A y$ with the Euclidean norm, the best $\nu$ is the largest eigenvalue of $(A + A^T)/2$, the logarithmic norm $\mu_2(A)$.

## Examples and non-examples

- **Linear functions.** $f(t, y) = \lambda y$ is Lipschitz on $\mathbb{R}$ with $L = |\lambda|$. For $f(t, y) = A y$ the Lipschitz constant is the induced norm $\|A\|$. For $A = \begin{pmatrix} -1 & 100 \\ 0 & -1 \end{pmatrix}$ it is $101$ in the 1-norm and in the max-norm, and $100.0100$ in the 2-norm, while the one-sided constant in the 2-norm is $\mu_2(A) = 49$.
- **Bounded derivative.** $f(t, y) = \sin y$ is globally Lipschitz with $L = 1$, because $|\cos y| \le 1$.
- **The logistic right-hand side.** $f(y) = y(1 - y)$ has $f'(y) = 1 - 2y$, so it is Lipschitz with $L = 1$ on $0 \le y \le 1$. It is not globally Lipschitz, since $|f'(y)| \to \infty$ as $|y| \to \infty$.
- **A test problem.** $f(t, y) = -2 t y^2$ has $f_y = -4 t y$, so on $[0, 1] \times [-1, 1]$ it is Lipschitz with $L = 4$.
- **Lipschitz but not differentiable.** $f(y) = |y|$ is Lipschitz with $L = 1$, by the triangle inequality, but it has no derivative at $0$. So the Lipschitz condition is weaker than a bounded derivative.
- **Stiff example.** $f(y) = -1000\, y$ has $L = 1000$, but its one-sided constant is $\nu = -1000$. The bound $e^{L t}$ grows quickly, while the true bound $e^{\nu t}$ says that solutions contract.
- **Non-example: a square root.** $f(y) = \sqrt{|y|}$ is continuous but not Lipschitz near $0$: with $v = 0$ the ratio $|f(u) - f(0)| / |u| = 1/\sqrt{|u|}$ is unbounded as $u \to 0$. The problem $y' = \sqrt{|y|}$, $y(0) = 0$ has the two solutions $0$ and $t^2/4$.
- **Non-example: a quadratic on the whole line.** $f(y) = y^2$ is locally Lipschitz but not globally: $|u^2 - v^2| / |u - v| = |u + v|$ is unbounded. The solution of $y' = y^2$, $y(0) = 1$ is $1/(1 - t)$, which does not exist past $t = 1$.
- **Non-example: a jump.** The sign function is not Lipschitz at $0$, because it is not even continuous there.

## Related definitions

- **[Picard-Lindelöf theorem](/picard-lindelof-theorem/).** A continuous $f$ that is Lipschitz in $y$ gives a unique solution of the IVP. Local Lipschitz continuity gives a unique solution on some interval around $t_0$.
- **[Gronwall's inequality](/gronwall-inequality/).** The tool that turns the Lipschitz condition into the bound $e^{L(t - t_0)}$ on the growth of differences between solutions, and into error bounds for numerical methods.
- **[Global error](/global-error/) bounds.** For a one-step method, the increment function inherits a Lipschitz constant from $f$, and the error bound grows like $(e^{L(T - t_0)} - 1)/L$.
- **Contraction.** A map $g$ with Lipschitz constant less than 1 is a contraction, and the [Banach fixed-point theorem](/banach-fixed-point-theorem/) gives a unique fixed point. [Picard iteration](/picard-iteration/) and the [fixed-point iteration](/fixed-point-iteration/) for the stage equations of implicit methods use this with the condition $h L |a_{ii}| < 1$, which is too strict for stiff problems.
- **Stiffness.** A problem is stiff when $L (T - t_0)$ is large while the one-sided constant $\nu$ is small or negative; see [stiff ODE problem](/stiff-ode-problem/).
- **Hölder condition.** $\|f(t, u) - f(t, v)\| \le C \|u - v\|^\alpha$ with $0 < \alpha < 1$. The function $\sqrt{|y|}$ satisfies it with $\alpha = 1/2$, which is not enough for uniqueness.

## References
