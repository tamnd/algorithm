---
tag: 5DRK8N
kind: definition
slug: control-barrier-function
name: Control barrier function
aliases:
- CBF
area: control/nonlinear-control
level: research
summary: A function whose zero superlevel set some input can keep forward invariant, used to state safety the way a CLF states stability.
prereqs: [control-lyapunov-function, positively-invariant-set, lie-derivative]
see_also: [cbf-safety-filter, barrier-certificate, control-invariant-set, control-lyapunov-function, sontag-universal-formula, relative-degree, hamilton-jacobi-reachability, model-predictive-control]
sources:
  - paper: doi:10.1109/TAC.2016.2638961
    title: "Aaron D. Ames, Xiangru Xu, Jessy W. Grizzle and Paulo Tabuada, Control barrier function based quadratic programs for safety critical systems, IEEE Transactions on Automatic Control 62(8), 3861-3876, 2017"
    locator: the definitions of reciprocal and zeroing control barrier functions and the forward invariance results
  - paper: doi:10.23919/ECC.2019.8796030
    title: "Aaron D. Ames, Samuel Coogan, Magnus Egerstedt, Gennaro Notomista, Koushil Sreenath and Paulo Tabuada, Control barrier functions: theory and applications, European Control Conference, 3420-3431, 2019"
    locator: the definition with an extended class K infinity function, the safety theorem, and high relative degree
  - paper: "Peter Wieland and Frank Allgöwer, Constructive safety using control barrier functions, IFAC Proceedings Volumes 40(12), 462-467, 2007"
    title: Constructive safety using control barrier functions
    locator: the first definition of a control barrier function, by analogy with control Lyapunov functions
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 3.4, the comparison principle, used in the proof of forward invariance
---

A control barrier function (CBF) for a system with an input is a function $h$ such that, at each state, some input keeps $h$ from falling too fast. The safe set is $C = \{x : h(x) \ge 0\}$. If the input always satisfies the CBF condition, a state that starts in $C$ stays in $C$. A [control Lyapunov function](/control-lyapunov-function/) says that some input can make a function decrease to zero, which gives stability. A CBF says that some input can stop a function from becoming negative, which gives safety. The condition is linear in the input for a control-affine system, so it fits in a quadratic program: the [CBF safety filter](/cbf-safety-filter/) is the controller that uses it. A [barrier certificate](/barrier-certificate/) is a different object: it proves that a system without a free input, or with a fixed feedback, never reaches an unsafe set.

## Definition

**Setting.** The system is $\dot x = f(x) + g(x) u$ with $x \in \mathbb{R}^n$, $u \in U \subseteq \mathbb{R}^m$, and $f$, $g$ locally Lipschitz. The function $h : D \to \mathbb{R}$ is continuously differentiable on an open set $D \subseteq \mathbb{R}^n$, and the safe set is $C = \{x \in D : h(x) \ge 0\}$, with $C \subseteq D$ closed. The [Lie derivatives](/lie-derivative/) are $L_f h(x) = \nabla h(x)^T f(x)$ and $L_g h(x) = \nabla h(x)^T g(x)$, so $\dot h = L_f h(x) + L_g h(x)\, u$ along a solution.

**Extended class K function.** A function $\alpha : (-b, a) \to \mathbb{R}$, with $a, b > 0$, is an extended class K function if it is continuous, strictly increasing and $\alpha(0) = 0$. It is extended class K infinity if it is defined on all of $\mathbb{R}$ and $\alpha(s) \to \pm\infty$ as $s \to \pm\infty$. The common choice is $\alpha(s) = \gamma s$ with $\gamma > 0$.

**Definition (zeroing CBF, Ames et al. 2017).** $h$ is a control barrier function on $D$ if there is an extended class K function $\alpha$ with

$$\sup_{u \in U} \bigl[ L_f h(x) + L_g h(x)\, u + \alpha(h(x)) \bigr] \ge 0 \quad \text{for all } x \in D.$$

The set of good inputs at $x$ is $K_{\text{cbf}}(x) = \{u \in U : L_f h(x) + L_g h(x)\, u + \alpha(h(x)) \ge 0\}$. With $U = \mathbb{R}^m$ the supremum is $+\infty$ when $L_g h(x) \neq 0$, so the condition reduces to

$$L_g h(x) = 0 \quad \Longrightarrow \quad L_f h(x) + \alpha(h(x)) \ge 0, \qquad x \in D.$$

**What it gives (theorem, Ames et al. 2017).** If $h$ is a CBF on $D$ and $k : D \to U$ is a locally Lipschitz feedback with $k(x) \in K_{\text{cbf}}(x)$ for all $x \in D$, then $C$ is forward invariant for $\dot x = f(x) + g(x) k(x)$: a solution that starts in $C$ stays in $C$ while it exists. The proof is the comparison argument: $\dot h \ge -\alpha(h)$ along the solution, and the solution of $\dot y = -\alpha(y)$ from $y(0) \ge 0$ never becomes negative. The full proof is on the [CBF safety filter](/cbf-safety-filter/) page. The [positively invariant set](/positively-invariant-set/) page gives the general notion.

**Reading the condition.** Inside $C$, where $h > 0$, the term $\alpha(h)$ is positive, so $h$ may decrease, but less fast as it nears 0. On the boundary $h = 0$, the condition says $\dot h \ge 0$ for some input. Outside $C$ but in $D$, $\alpha(h) < 0$, so the condition asks that $h$ increase, and a state that starts a little outside $C$ is pushed back. This is why $D$ is an open set that is larger than $C$. It makes the condition robust to small errors.

**Other forms.**

- *Reciprocal CBF.* A function $B$ that goes to $+\infty$ at the boundary of $C$, with $\dot B \le \gamma / B$ for some input. Ames et al. (2014, 2017) defined it before the zeroing form. It is not defined outside $C$, so it has no robustness margin, and it is less used now.
- *Bounded inputs.* With a bounded $U$, the reduction to the test on $L_g h = 0$ fails, and $h$ may be a CBF for $U = \mathbb{R}^m$ but not for $U$ (see the second example).
- *High relative degree.* If $L_g h = 0$ on all of $D$, the input does not appear in $\dot h$, and the condition is a constraint on the state, not on the input. Exponential CBFs (Nguyen and Sreenath 2016) and high-order CBFs (Xiao and Belta 2019) apply the condition to a chain of derivatives of $h$ instead. The number of derivatives is the [relative degree](/relative-degree/) of $h$.

## Examples and non-examples

**Interval with a free input.** For $\dot x = u$ with $u \in \mathbb{R}$ and $h(x) = 1 - x^2$, $C = [-1, 1]$. $L_f h = 0$ and $L_g h = -2x$. $L_g h = 0$ only at $x = 0$, where $h = 1$ and $\alpha(1) > 0$. So $h$ is a CBF on $D = \mathbb{R}$ for every extended class K infinity $\alpha$.

**The same set with a bounded input.** Take $|u| \le 1$ and $\alpha(s) = s$. The supremum over $|u| \le 1$ of $-2x u + (1 - x^2)$ is $2|x| + 1 - x^2$, which is nonnegative for $|x| \le 1 + \sqrt 2$. So $h$ is a CBF on $D = (-(1 + \sqrt 2), 1 + \sqrt 2)$, an open set that contains $C$.

**Unstable system, bounded input: a non-example.** For $\dot x = x + u$ and $h(x) = 2 - x$, $L_f h = -x$ and $L_g h = -1$. With $u \in \mathbb{R}$, $L_g h \neq 0$ everywhere, so $h$ is a CBF on $\mathbb{R}$. With $|u| \le 1$, the supremum at $x = 2$ is $-2 + 1 + \alpha(0) = -1 < 0$, so $h$ is not a CBF for any $\alpha$. At $x = 2$ every allowed input gives $\dot x \ge 1$, and the state leaves $C$. The set $C = (-\infty, 2]$ cannot be kept invariant.

**The same system with a smaller set.** With $|u| \le 1$, the set $x \le 1$ is the largest set of the form $(-\infty, c]$ that the input can hold, because $\dot x = x + u \le 0$ at $x = c$ needs $c \le 1$. Take $h(x) = 0.5 - x$ and $\alpha(s) = s$. The supremum is $-x + 1 + 0.5 - x = 1.5 - 2x$, which is nonnegative for $x \le 0.75$. So $h$ is a CBF on $D = (-\infty, 0.75)$. The gap between $C$ and the largest holdable set gives the margin.

**Relative degree 2: a non-example.** For the double integrator $\dot x_1 = x_2$, $\dot x_2 = u$ and $h = -x_1$ (stay at $x_1 \le 0$), $L_g h = 0$ everywhere and $L_f h = -x_2$. The condition reads $-x_2 + \alpha(-x_1) \ge 0$, which fails at states with $x_1 \le 0$ and a large $x_2$, for every $\alpha$. So $h$ is not a CBF, and the set $C$ is not even holdable: at $x = (0, 1)$ the state leaves for every input. The function $h_1 = -x_2 - \gamma x_1$ with $\gamma > 0$ has $L_g h_1 = -1$, so it is a CBF on $\mathbb{R}^2$, and its safe set $\{x_2 \le -\gamma x_1\}$ intersected with $C$ is a set that the input can hold. This is the construction of exponential and high-order CBFs.

**The case without an input.** For $\dot x = -x$, $h = 1 - x^2$ has $\dot h = 2x^2 \ge 0$, so $\dot h \ge -\alpha(h)$ holds on $\mathbb{R}$ with no input to choose. Here the CBF condition is the condition of a barrier certificate, and it proves that $[-1, 1]$ is invariant. The two notions differ only when there is an input: a CBF says that a good input exists, and a barrier certificate says that the system is safe as it is.

## Related definitions

- **[Control Lyapunov function](/control-lyapunov-function/).** A CLF $V$ asks for $\dot V < 0$ away from the origin; a CBF asks for $\dot h \ge -\alpha(h)$ on $D$. A CLF is positive definite; a CBF changes sign at the boundary of $C$. Both are combined in one quadratic program with the CLF condition relaxed by a slack variable, so that safety wins when the two conflict (Ames et al. 2017).
- **[Barrier certificate](/barrier-certificate/).** A function that proves safety of a system without a free input, often found by [sum of squares programming](/sum-of-squares-programming/). A CBF certifies that an input exists that keeps the system safe.
- **[Control invariant set](/control-invariant-set/).** A set that some input can keep invariant. If $h$ is a CBF and a locally Lipschitz selection of $K_{\text{cbf}}$ exists, $C$ is control invariant. The largest control invariant subset of a constraint set is what [Hamilton-Jacobi reachability](/hamilton-jacobi-reachability/) computes.
- **[CBF safety filter](/cbf-safety-filter/).** The quadratic program $\min |u - u_{\text{nom}}|^2$ over $K_{\text{cbf}}(x)$. It is the standard way to use a CBF.
- **Sontag-like formulas.** Wieland and Allgöwer (2007) gave a formula for a safe feedback from a CBF, in the style of [Sontag's universal formula](/sontag-universal-formula/) for CLFs.

## References
