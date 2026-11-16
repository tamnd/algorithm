---
title: With a large enough step parameter, every CHOMP step decreases the objective, and the covariant gradient norms are summable
proves: [correctness]
status: full
---

We use the notation of the page and of the code. The free waypoints are $q_1, \dots, q_n \in \mathbb R^2$, stacked in $\xi$; $q_0$ and $q_{n+1}$ are fixed; $\Delta t = 1/(n+1)$. Obstacles are discs with centers $o_j$ and radii $r_j > 0$, $j = 1, \dots, m$. The objective is $U = F_{\text{obs}} + \lambda F_{\text{smooth}}$ with

$$F_{\text{smooth}}(\xi) = \frac12 \sum_{t=0}^{n} \left\| \frac{q_{t+1} - q_t}{\Delta t} \right\|^2 = \frac12 \xi^{\mathsf T} A \xi + \xi^{\mathsf T} b + c, \qquad F_{\text{obs}}(\xi) = \sum_{t=1}^n \sum_{j=1}^m c(D_j(q_t)),$$

where $D_j(p) = \|p - o_j\| - r_j$ and $c$ is the cost of line L3 with threshold $\varepsilon > 0$. For each coordinate, $A$ is the $n \times n$ matrix with $2/\Delta t^2$ on the diagonal and $-1/\Delta t^2$ next to it. The vector $g$ of line L4 is $g = \tilde\nabla F_{\text{obs}}(\xi) + \lambda (A\xi + b)$, where $\tilde\nabla F_{\text{obs}}$ has the entry $\sum_j c'(D_j(q_t))\, u_j(q_t)$ for waypoint $t$, with $u_j(p) = (p - o_j)/\|p - o_j\|$, and $u_j(o_j) = 0$.

The step of lines L6 and L7 is $\delta = -\frac1\eta A^{-1} g$. Let $\mu = 4\sin^2(\pi/(2(n+1)))/\Delta t^2$ and

$$L = \lambda + \frac{m}{\varepsilon \mu}.$$

## Step 1: the smallest eigenvalue of A

The eigenvalues of the tridiagonal matrix with $2$ on the diagonal and $-1$ next to it are $2 - 2\cos(k\pi/(n+1))$ for $k = 1, \dots, n$ (eigenvectors $\sin(k t \pi/(n+1))$). The smallest is $2 - 2\cos(\pi/(n+1)) = 4\sin^2(\pi/(2(n+1)))$. Dividing by $\Delta t^2$ gives $\mu$. So $A$ is positive definite and $\|\delta\|^2 \le \delta^{\mathsf T} A \delta / \mu$ for every $\delta$ (applied to each coordinate and summed).

## Step 2: an upper model for one obstacle term

Fix one disc $(o, r)$ and write $\rho = \|p - o\|$, so $D = \rho - r$. Put $\varphi(\rho) = c(\rho - r)$ and $\psi(\rho) = \varphi(\rho) + \rho$ for $\rho \ge 0$.

From the formula for $c$: $c'(D) = -1$ for $D < 0$, $c'(D) = (D - \varepsilon)/\varepsilon$ for $0 \le D \le \varepsilon$, and $c'(D) = 0$ for $D > \varepsilon$. So $c'$ is continuous, nondecreasing, with values in $[-1, 0]$, and Lipschitz with constant $1/\varepsilon$. Hence $\psi'(\rho) = c'(\rho - r) + 1$ is continuous, nondecreasing, in $[0, 1]$, Lipschitz with constant $1/\varepsilon$, and zero for $\rho \le r$.

**Lemma 1.** The function $G(p) = \psi(\|p - o\|)$ is convex, and its gradient $\nabla G(p) = \psi'(\rho)\, u(p)$ (zero for $\rho \le r$) is Lipschitz with constant $1/\varepsilon$.

*Proof.* $\psi$ is convex and nondecreasing ($\psi'$ is nondecreasing and nonnegative), and $p \mapsto \|p - o\|$ is convex, so the composition is convex. The gradient formula holds for $\rho > 0$ by the chain rule, and $G$ is constant near $o$ because $\psi' = 0$ for $\rho \le r$. The map $p \mapsto \nabla G(p)$ is continuous. Off the circles $\rho = r$ and $\rho = r + \varepsilon$ it is differentiable, with derivative $\psi''(\rho) u u^{\mathsf T} + (\psi'(\rho)/\rho)(I - u u^{\mathsf T})$. Its eigenvalues are $\psi''(\rho) \in \{0, 1/\varepsilon\}$ and $\psi'(\rho)/\rho$; since $\psi'(r) = 0$ and $\psi'$ is $1/\varepsilon$-Lipschitz, $\psi'(\rho) \le (\rho - r)/\varepsilon \le \rho/\varepsilon$, so both are at most $1/\varepsilon$. A segment meets the two circles in at most four points, and between them the map has derivative of norm at most $1/\varepsilon$; since the map is continuous, integrating along the segment gives $\|\nabla G(p') - \nabla G(p)\| \le \|p' - p\|/\varepsilon$. $\square$

**Lemma 2.** For all $p, p'$, with $f(p) = c(D(p))$ and $\tilde\nabla f(p) = c'(D(p))\, u(p)$,

$$f(p') \le f(p) + \tilde\nabla f(p)^{\mathsf T}(p' - p) + \frac{1}{2\varepsilon}\|p' - p\|^2.$$

*Proof.* $f(p) = G(p) - \|p - o\|$. By Lemma 1 and the standard bound for functions with a Lipschitz gradient, $G(p') \le G(p) + \nabla G(p)^{\mathsf T}(p' - p) + \frac{1}{2\varepsilon}\|p' - p\|^2$. The function $H(p) = -\|p - o\|$ is concave, and $-u(p)$ is a supergradient of it at every $p$: for $p \ne o$ it is the gradient, and at $p = o$ the vector $0$ works because $H(p') \le 0 = H(o)$. So $H(p') \le H(p) - u(p)^{\mathsf T}(p' - p)$. Adding the two bounds, and using $\nabla G(p) - u(p) = (\psi'(\rho) - 1) u(p) = c'(D)\,u(p)$ (also at $p = o$, where both sides are zero), gives the claim. $\square$

## Step 3: sufficient decrease

**Lemma 3.** For every $\xi$ and $\delta$, $U(\xi + \delta) \le U(\xi) + g^{\mathsf T}\delta + \frac L2 \delta^{\mathsf T} A \delta$.

*Proof.* Sum Lemma 2 over the $n$ waypoints and the $m$ discs: $F_{\text{obs}}(\xi + \delta) \le F_{\text{obs}}(\xi) + \tilde\nabla F_{\text{obs}}^{\mathsf T}\delta + \frac{m}{2\varepsilon}\|\delta\|^2$. $F_{\text{smooth}}$ is quadratic, so $F_{\text{smooth}}(\xi + \delta) = F_{\text{smooth}}(\xi) + (A\xi + b)^{\mathsf T}\delta + \frac12 \delta^{\mathsf T} A\delta$ exactly. Multiply the second by $\lambda$, add, and bound $\|\delta\|^2$ by Step 1. $\square$

**Theorem.** If $\eta \ge L$, then each pass of lines L3 to L7 gives

$$U(\xi_{k+1}) \le U(\xi_k) - \frac{1}{2\eta}\, g_k^{\mathsf T} A^{-1} g_k,$$

so the values $U(\xi_k)$ never increase, and for every $K \ge 1$

$$\min_{0 \le k < K} g_k^{\mathsf T} A^{-1} g_k \le \frac{2\eta\, U(\xi_0)}{K}.$$

*Proof.* Put $\delta = -\frac1\eta A^{-1} g_k$ in Lemma 3: $g_k^{\mathsf T}\delta = -\frac1\eta g_k^{\mathsf T} A^{-1} g_k$ and $\delta^{\mathsf T} A\delta = \frac1{\eta^2} g_k^{\mathsf T} A^{-1} g_k$. So $U(\xi_{k+1}) \le U(\xi_k) - \frac1\eta(1 - \frac{L}{2\eta}) g_k^{\mathsf T} A^{-1} g_k$, and $1 - L/(2\eta) \ge 1/2$. Summing over $k < K$ and using $U \ge 0$ (both terms are sums of nonnegative numbers) gives $\sum_{k<K} g_k^{\mathsf T} A^{-1} g_k \le 2\eta\, U(\xi_0)$, and the minimum is at most the average. $\blacksquare$

## What the theorem does not say

The quantity that goes to zero is the covariant norm of $g$. Where the obstacle cost is differentiable, $g = 0$ means a stationary point of $U$. A stationary point need not be a minimum, and need not be free of collision: if the straight start line passes through the center of a disc and the problem is symmetric about that line, then every $g_k$ has a zero component across the line, every iterate stays on it, and the limit is in collision. The theorem is also not a statement about the number of iterations to reach a collision-free trajectory; the iteration counts on the page are measurements.

The default step parameter of the code is exactly $L$. The paper tunes its parameters on a set of training problems, and uses the speed-weighted obstacle term, for which the constant $L$ above does not apply.

**Remark (one step without obstacles).** With $m = 0$ and $\eta = \lambda$, the step is $\xi - A^{-1}(A\xi + b) = -A^{-1} b$, the exact minimizer of $\lambda F_{\text{smooth}}$: the evenly spaced straight line. The tests check this.
