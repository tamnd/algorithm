---
tag: P1AP78
kind: definition
slug: exponential-stability
name: Exponential stability
aliases:
- exponentially stable equilibrium
area: control/stability
level: core
summary: An equilibrium is exponentially stable if nearby solutions obey |x(t)| <= k e^(-lambda t) |x(0)| for constants k and lambda > 0. For linear systems this is the same as asymptotic stability.
prereqs: [asymptotic-stability]
see_also: [asymptotic-stability, hurwitz-matrix, lyapunov-theorem-for-linear-systems, lyapunov-indirect-method, lyapunov-function, matrix-exponential, contraction-analysis, converse-lyapunov-theorem]
sources:
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.5 (the definition of exponential stability and the Lyapunov test with quadratic bounds), Section 4.3 (linear systems and linearization), the converse theorems of Chapter 4, and Chapter 9 (stability of perturbed systems)
  - book: isbn:9780691193984
    title: Karl Johan Åström and Richard M. Murray, Feedback Systems, second edition, Princeton University Press, 2021
    locator: Chapter 5, Dynamic Behavior (stability of linear systems and the exponential decay of the modes)
---

An equilibrium is exponentially stable when the solutions that start near it approach it at least as fast as a decaying exponential: $|x(t)| \le k e^{-\lambda t} |x(0)|$ with a rate $\lambda > 0$ and a constant $k \ge 1$. It is the strongest of the three Lyapunov notions, after [Lyapunov stability](/lyapunov-stability/) and [asymptotic stability](/asymptotic-stability/). For a linear system $\dot x = A x$ all three strong notions agree: asymptotic stability, exponential stability and the [Hurwitz](/hurwitz-matrix/) property of $A$. For a nonlinear system with a continuously differentiable right-hand side, local exponential stability is the same as a Hurwitz linearization, and it survives small perturbations of the model; plain asymptotic stability does not.

## Definition

**Setting.** As on [Lyapunov stability](/lyapunov-stability/): $\dot x = f(x)$ with $f : D \to \mathbb{R}^n$ locally Lipschitz on a domain $D$ that contains the origin, $f(0) = 0$, and $|\cdot|$ a norm on $\mathbb{R}^n$.

**Definition.** The equilibrium $x = 0$ is *exponentially stable* if there are constants $c > 0$, $k \ge 1$ and $\lambda > 0$ such that

$$|x(t)| \le k\, e^{-\lambda t}\, |x(0)| \quad \text{for all } t \ge 0 \text{ and all } |x(0)| < c .$$

It is *globally exponentially stable* if the bound holds for every $x(0) \in \mathbb{R}^n$ (with $D = \mathbb{R}^n$). The number $\lambda$ is a *decay rate*. The constant $k$ bounds the transient: $k = 1$ means that the norm never grows, and $k > 1$ allows a peak before the decay. A change of norm changes $k$ but not the set of admissible rates. Exponential stability implies asymptotic stability, with the class KL function $\beta(r, t) = k r e^{-\lambda t}$. For time-varying systems the bound is $|x(t)| \le k e^{-\lambda (t - t_0)} |x(t_0)|$ for all $t_0$, which makes it uniform in $t_0$ (Khalil 2002, Section 4.5).

**A Lyapunov test.** Let $V : D \to \mathbb{R}$ be continuously differentiable, and let $k_1, k_2, k_3 > 0$ and $a > 0$ be constants with

$$k_1 |x|^a \le V(x) \le k_2 |x|^a, \qquad \dot V(x) = \nabla V(x) \cdot f(x) \le -k_3 |x|^a$$

on a ball $|x| < r$ in $D$. Then the origin is exponentially stable, with the rate $\lambda = k_3 / (a k_2)$ and $k = (k_2 / k_1)^{1/a}$. If the bounds hold on all of $\mathbb{R}^n$, it is globally exponentially stable (Khalil 2002, Section 4.5).

Proof. Pick $c \le r$ with $k_2 c^a < k_1 r^a$, and let $|x(0)| < c$. As long as the solution stays in the ball, $\dot V \le -k_3 |x|^a \le -(k_3 / k_2) V \le 0$, so $V(x(t)) \le V(x(0)) < k_2 c^a < k_1 r^a$ and $|x(t)| \le (V(x(t)) / k_1)^{1/a} < r$. So the solution cannot reach the sphere $|x| = r$, and it stays in the ball for all $t \ge 0$. The comparison of $\dot V \le -(k_3/k_2) V$ with its linear equality gives $V(x(t)) \le V(x(0)) e^{-(k_3 / k_2) t}$. Then

$$|x(t)| \le \left(\frac{V(x(t))}{k_1}\right)^{1/a} \le \left(\frac{k_2}{k_1}\right)^{1/a} e^{-k_3 t / (a k_2)}\, |x(0)| . \qquad \blacksquare$$

**Linear systems.** For $\dot x = A x$, with $\alpha(A) = \max \operatorname{Re} \lambda_i(A)$ the spectral abscissa:

- The origin is exponentially stable if and only if $A$ is Hurwitz ($\alpha(A) < 0$). Then the bound holds globally.
- Every rate $\lambda < -\alpha(A)$ is admissible with some $k$. The rate $\lambda = -\alpha(A)$ itself is admissible if and only if every eigenvalue with real part $\alpha(A)$ has only Jordan blocks of size 1. No rate above $-\alpha(A)$ is admissible, because an eigenvector gives a solution that decays exactly like $e^{\alpha(A) t}$.

The first point is proved on [asymptotic stability](/asymptotic-stability/) and [Hurwitz matrix](/hurwitz-matrix/). For a quadratic $V = x^T P x$ with $A^T P + P A = -Q$, $P > 0$ and $Q > 0$, the test above with $a = 2$ and the Euclidean norm gives

$$|x(t)| \le \sqrt{\frac{\lambda_{\max}(P)}{\lambda_{\min}(P)}}\; e^{-\frac{\lambda_{\min}(Q)}{2 \lambda_{\max}(P)} t}\; |x(0)| ,$$

since $\lambda_{\min}(P) |x|^2 \le V \le \lambda_{\max}(P) |x|^2$ and $\dot V = -x^T Q x \le -\lambda_{\min}(Q) |x|^2$. See [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/) and [Lyapunov equation](/lyapunov-equation/).

**Nonlinear systems and linearization.** Let $f$ be continuously differentiable near the origin and $A = \partial f / \partial x\,(0)$ its Jacobian. The origin of $\dot x = f(x)$ is exponentially stable if and only if $A$ is Hurwitz (Khalil 2002, Chapter 4). The "if" direction is the [indirect method](/lyapunov-indirect-method/). The "only if" direction uses the [converse Lyapunov theorem](/converse-lyapunov-theorem/). So exponential stability is the notion that a linear model can certify, and it is the one that the [Jacobian linearization](/jacobian-linearization/) of a model keeps.

**Robustness.** Exponential stability survives a perturbation that vanishes at the origin. Let $A$ be Hurwitz, $A^T P + P A = -Q$ with $P, Q > 0$, and $|g(x)| \le \gamma |x|$ near $0$. For $\dot x = A x + g(x)$ the same $V = x^T P x$ gives

$$\dot V = -x^T Q x + 2 x^T P g(x) \le -\bigl(\lambda_{\min}(Q) - 2 \gamma \lambda_{\max}(P)\bigr) |x|^2 ,$$

so the origin stays exponentially stable when $\gamma < \lambda_{\min}(Q) / (2 \lambda_{\max}(P))$ (Khalil 2002, Chapter 9). Plain asymptotic stability has no such margin: $\dot x = -x^3$ is asymptotically stable, but $\dot x = -x^3 + \gamma x$ is unstable for every $\gamma > 0$.

## Examples and non-examples

- **The check matrix.** $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$ has the eigenvalues $-1$ and $-2$, so $\alpha(A) = -1$ and the true rate is $1$, with semisimple eigenvalues. With $Q = I$ the Lyapunov equation gives $P = \begin{bmatrix} 5/4 & 1/4 \\ 1/4 & 1/4 \end{bmatrix}$ exactly. Its eigenvalues are $(3 \mp \sqrt{5})/4 = 0.19098$ and $1.30902$. The quadratic bound gives $k = \sqrt{1.30902 / 0.19098} = (3 + \sqrt{5})/2 = 2.61803$ and the rate $1 / (2 \cdot 1.30902) = (3 - \sqrt{5})/2 = 0.38197$. The bound is valid but conservative: the rate is less than half of the true rate. The same numbers say that a perturbation with $|g(x)| \le \gamma |x|$ and $\gamma < 0.38197$ keeps the origin exponentially stable.
- **A large transient.** $A = \begin{bmatrix} -1 & 10 \\ 0 & -1 \end{bmatrix}$ is Hurwitz, with the double eigenvalue $-1$ in one Jordan block. Here $e^{At} = e^{-t} \begin{bmatrix} 1 & 10 t \\ 0 & 1 \end{bmatrix}$. The $(1,2)$ entry peaks at $10/e = 3.6788$ at $t = 1$, and the induced 2-norm of $e^{At}$ peaks at $3.7160$ near $t = 0.98$. So every admissible pair has $k > 3.716$, and the rate $\lambda = 1$ is not admissible with any $k$, because $10 t e^{-t}$ is not bounded by $k e^{-t}$. Every rate below $1$ is admissible.
- **Global, nonlinear.** $\dot x = -x - x^3$: with $V = x^2$, $\dot V = -2x^2 - 2x^4 \le -2 V$, so $|x(t)| \le e^{-t} |x(0)|$ for every $x(0)$.
- **Asymptotically but not exponentially stable (non-example).** $\dot x = -x^3$ has $x(t) = x_0 / \sqrt{1 + 2 x_0^2 t}$, which decays like $1/\sqrt{2t}$. No exponential bound holds, in line with the Jacobian $0$, which is not Hurwitz.
- **Exponentially stable, not globally (non-example of the global notion).** $\dot x = -x + x^2$: the Jacobian at $0$ is $-1$, so the origin is exponentially stable. The solution from $x_0 = 2$ escapes to infinity at $t = \ln 2$, so the property is not global.

## Related definitions

- [Asymptotic stability](/asymptotic-stability/): convergence without a rate.
- [Hurwitz matrix](/hurwitz-matrix/): the matrix form of exponential stability for linear systems.
- [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/): the Lyapunov equation characterization, which gives the quadratic $V$ used above.
- [Lyapunov's indirect method](/lyapunov-indirect-method/): exponential stability from the linearization.
- [Contraction analysis](/contraction-analysis/): exponential convergence of any two solutions toward each other, not only toward an equilibrium.
- *Discrete time.* For $x_{k+1} = F(x_k)$ the bound is $|x_k| \le c \rho^k |x_0|$ with $0 \le \rho < 1$. For $x_{k+1} = A x_k$ it holds if and only if the [spectral radius](/spectral-radius/) of $A$ is less than 1, the Schur property.
- [Input-to-state stability](/input-to-state-stability/): a nonlinear system whose origin is globally exponentially stable, and whose right-hand side is continuously differentiable and globally Lipschitz in $(x, u)$, is input-to-state stable (Khalil 2002, Chapter 4, the section on input-to-state stability).

## References
