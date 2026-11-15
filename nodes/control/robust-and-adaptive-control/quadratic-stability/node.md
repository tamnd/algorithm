---
tag: Y5XMRN
kind: definition
slug: quadratic-stability
name: Quadratic stability
aliases:
- quadratic stability of uncertain systems
area: control/robust-and-adaptive-control
level: advanced
summary: "An uncertain linear system is quadratically stable if one Lyapunov function x^T P x decreases for every system in the set. For a polytope of state matrices this is an LMI at the vertices."
prereqs: [lyapunov-theorem-for-linear-systems, linear-matrix-inequality]
see_also: [common-lyapunov-function, switched-system, lpv-system, s-procedure, bounded-real-lemma, model-uncertainty, kharitonov-theorem, gain-scheduling]
sources:
  - book: isbn:089871334X
    title: Stephen Boyd, Laurent El Ghaoui, Eric Feron and Venkataramanan Balakrishnan, Linear Matrix Inequalities in System and Control Theory, SIAM Studies in Applied Mathematics 15, SIAM, 1994
    locator: Section 5.1, Quadratic Stability (polytopic and norm-bound linear differential inclusions), and the Notes and References of Chapter 5
  - paper: "B. Ross Barmish, Necessary and sufficient conditions for quadratic stabilizability of an uncertain system, Journal of Optimization Theory and Applications 46(4), 399-408, 1985"
    locator: the definition of quadratic stability and quadratic stabilizability for uncertain systems
---

A set of linear systems is quadratically stable if a single quadratic function $V(x) = x^T P x$ is a Lyapunov function for all of them at once. This is stronger than asking that each system in the set be Hurwitz: it also proves that the state decays when the system jumps or drifts inside the set over time, at any speed. Its value is that it is easy to test. When the state matrix depends affinely on the uncertain parameters and they lie in a box or a polytope, quadratic stability is a [linear matrix inequality](/linear-matrix-inequality/) at the vertices, solved as a semidefinite program. The price is conservatism: a set of systems can be robustly stable without any common quadratic Lyapunov function.

## Definition

**Uncertain system.** Let $\mathcal{A}$ be a set of real $n \times n$ matrices, for example $\{A(\delta) : \delta \in \Delta\}$ for a parameter set $\Delta$. The uncertain system is $x' = A x$ with $A \in \mathcal{A}$. The time-varying version is $x'(t) = A(t) x(t)$ with $A(t) \in \mathcal{A}$ for all $t$ and $A(\cdot)$ measurable, a linear differential inclusion in the language of Boyd et al. (1994).

**Quadratic stability.** The set $\mathcal{A}$ (or the uncertain system) is quadratically stable if there are a symmetric matrix $P > 0$ and a number $\varepsilon > 0$ with

$$A^T P + P A \le -\varepsilon I \qquad \text{for every } A \in \mathcal{A}.$$

Then $V(x) = x^T P x$ decreases along every solution of the time-varying system: $V' = x^T (A(t)^T P + P A(t)) x \le -\varepsilon |x|^2 \le -(\varepsilon / \lambda_{\max}(P)) V$. So

$$|x(t)|^2 \le \frac{\lambda_{\max}(P)}{\lambda_{\min}(P)} e^{-\varepsilon t / \lambda_{\max}(P)} |x(0)|^2,$$

an exponential decay with the same rate for every allowed $A(\cdot)$. For a compact set $\mathcal{A}$, the condition $A^T P + P A < 0$ for every $A$ already gives a uniform $\varepsilon$.

**Robust stability is weaker.** $\mathcal{A}$ is robustly stable if every $A \in \mathcal{A}$ is [Hurwitz](/hurwitz-matrix/). Quadratic stability implies it, by the [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/) applied to each $A$ with the same $P$. The converse is false (see below).

**Polytopes: a test at the vertices.** If $\mathcal{A} = \operatorname{conv}\{A_1, \dots, A_N\}$, then $\mathcal{A}$ is quadratically stable if and only if there is $P$ with

$$P > 0, \qquad A_i^T P + P A_i < 0 \quad (i = 1, \dots, N).$$

The map $A \mapsto A^T P + P A$ is linear, so $\sum_i \theta_i (A_i^T P + P A_i) < 0$ for convex weights $\theta_i$. This holds when $A(\delta) = A_0 + \delta_1 A_1 + \dots + \delta_k A_k$ with each $\delta_j$ in an interval: the vertices are the $2^k$ corners of the box. The LMI has $n(n+1)/2$ scalar unknowns and $N + 1$ blocks of size $n$; it is a [semidefinite program](/semidefinite-programming/). The number of vertices grows exponentially with the number of parameters.

**Norm-bounded uncertainty.** If $\mathcal{A} = \{A + B \Delta C : \Delta \in \mathbb{R}^{m \times p},\ \sigma_{\max}(\Delta) \le 1\}$ with $C \ne 0$, then $\mathcal{A}$ is quadratically stable if and only if $A$ is Hurwitz and the [H-infinity norm](/h-infinity-norm/) of $C (sI - A)^{-1} B$ is less than 1. Proof: the vectors $\Delta C x$ with $\sigma_{\max}(\Delta) \le 1$ are exactly the vectors $p$ with $|p| \le |C x|$. So quadratic stability asks that $2 x^T P (A x + B p) < 0$ whenever $(x, p) \ne 0$ and $|p| \le |C x|$. By the [S-procedure](/s-procedure/), this holds if and only if $\begin{bmatrix} A^T P + P A + \tau C^T C & P B \\ B^T P & -\tau I \end{bmatrix} < 0$ for some $\tau > 0$, and after division by $\tau$ this is the [bounded real lemma](/bounded-real-lemma/) with $\gamma = 1$.

**Quadratic stabilizability.** A system $x' = A x + B u$ with $A$ uncertain is quadratically stabilizable if there is one state feedback $u = K x$ that makes $\{A + B K : A \in \mathcal{A}\}$ quadratically stable (Barmish 1985). For a polytope of $A_i$ and a fixed $B$, the change of variables $Q = P^{-1}$, $Y = K Q$ gives the LMI $Q > 0$, $A_i Q + Q A_i^T + B Y + Y^T B^T < 0$ for all $i$, and $K = Y Q^{-1}$.

## Examples and non-examples

- **A spring with an uncertain stiffness, the check value.** $x'' + x' + k x = 0$ with $k \in [k_1, k_2]$, so $A(k) = \begin{bmatrix} 0 & 1 \\ -k & -1 \end{bmatrix}$, Hurwitz for every $k > 0$. For $P = \begin{bmatrix} p_1 & p_2 \\ p_2 & p_3 \end{bmatrix}$,
$$A(k)^T P + P A(k) = \begin{bmatrix} -2 k p_2 & p_1 - p_2 - k p_3 \\ p_1 - p_2 - k p_3 & 2 (p_2 - p_3) \end{bmatrix}.$$
It is negative definite if and only if $0 < p_2 < p_3$ and $(p_1 - p_2 - k p_3)^2 < 4 k p_2 (p_3 - p_2)$. The right side is at most $k p_3^2$, with equality at $p_2 = p_3 / 2$. With $p_3 = 1$ and $c = p_1 - p_2$, the condition for one $k$ is $k - \sqrt k < c < k + \sqrt k$. For $k_1 \ge 1/4$ both ends increase with $k$, so a common $P$ exists if and only if $k_2 - \sqrt{k_2} < k_1 + \sqrt{k_1}$.
  - For $k \in [1, 3]$: $3 - \sqrt 3 = 1.268 < 2$, so the set is quadratically stable. With $c = 1.5$, $P = \begin{bmatrix} 2 & 1/2 \\ 1/2 & 1 \end{bmatrix}$ gives $\begin{bmatrix} -1 & 1/2 \\ 1/2 & -1 \end{bmatrix}$ at $k = 1$ and $\begin{bmatrix} -3 & -3/2 \\ -3/2 & -1 \end{bmatrix}$ at $k = 3$, both with determinant $3/4$ and negative trace.
  - For $k \in [1, 4]$: $4 - 2 = 2 = 1 + 1$, so no common $P$ exists, although every $A(k)$ is Hurwitz. This shows only that no quadratic function proves stability for every time-varying $k(t)$; it does not show that some $k(t)$ makes the state grow.
- **Non-example: robustly stable but not quadratically stable.** $A_1 = \begin{bmatrix} -0.1 & 1 \\ -10 & -0.1 \end{bmatrix}$ and $A_2 = \begin{bmatrix} -0.1 & 10 \\ -1 & -0.1 \end{bmatrix}$. Every convex combination $\theta A_1 + (1 - \theta) A_2$ has the eigenvalues $-0.1 \pm j\sqrt{(10 - 9\theta)(1 + 9\theta)}$, so the whole segment is Hurwitz. But switch between them: use $A_1$ while $x_1 x_2 < 0$ and $A_2$ while $x_1 x_2 > 0$. Each quarter turn takes the time $\pi / (2\sqrt{10})$ and multiplies $|x|$ by $\sqrt{10}\, e^{-\pi / (20\sqrt{10})} = 3.009$, and a simulation from $x(0) = (1, 0)$ gives $|x(4)|$ of about 6900. A common $P$ would force decay for every switching signal, so the set is not quadratically stable. See [switched system](/switched-system/).
- **Norm-bounded scalar.** $x' = (-1 + \delta) x$ with $|\delta| \le r$. Write $\delta = r \Delta$ with $|\Delta| \le 1$, so $A = -1$, $B = r$, $C = 1$, and $C(sI - A)^{-1}B = r/(s + 1)$ has H-infinity norm $r$. The set is quadratically stable (with $P = 1$) exactly when $r < 1$. At $r = 1$, $\delta = 1$ gives $A = 0$, which is not Hurwitz.
- **Non-example: the vertex test without convexity.** If $A(\delta)$ depends on $\delta$ in a nonlinear way, for example through $\delta^2$, the set $\{A(\delta)\}$ is not the convex hull of a few vertex matrices, and the vertex LMIs do not prove quadratic stability. One remedy is to cover the set by a larger polytope, which adds conservatism.

## Related definitions

- [Common Lyapunov function](/common-lyapunov-function/): the same idea for general (not only quadratic) Lyapunov functions and nonlinear systems.
- [Switched system](/switched-system/): systems that jump between modes; quadratic stability of the modes proves stability under arbitrary switching.
- [LPV system](/lpv-system/) and [gain scheduling](/gain-scheduling/): parameter-dependent systems, for which parameter-dependent Lyapunov functions reduce the conservatism of one fixed $P$ when the parameter changes slowly.
- [S-procedure](/s-procedure/) and [bounded real lemma](/bounded-real-lemma/): the tools for norm-bounded uncertainty.
- [Kharitonov theorem](/kharitonov-theorem/): robust stability (not quadratic stability) of a family of polynomials with interval coefficients.
- [Model uncertainty](/model-uncertainty/): the other ways to describe a set of plants.

## References
