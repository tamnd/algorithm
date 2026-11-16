---
title: The discretized time-optimal problem in b = s'^2 is convex, and the barrier method returns a feasible point within M / t of the optimum
proves: [correctness]
status: full
---

We use the notation of the page. The grid is $s_0 < \dots < s_N$ with steps $\Delta_k > 0$. The variables are $b_0, \dots, b_N$ with $b_0 = b_N = 0$, and $a_k = (b_{k+1} - b_k)/(2\Delta_k)$ for $k < N$. The constraints are $b_k \ge 0$ and, for each row $(A, B, c, \ell, h)$ at $s_k$, $\ell \le A a_k + B b_k + c \le h$. Substituting $a_k$, each of these is an affine inequality $g_j(b) \le 0$ in $b$; there are $M$ of them. The objective is

$$T(b) = \sum_{k=0}^{N-1} \frac{2\Delta_k}{\sqrt{b_k} + \sqrt{b_{k+1}}}.$$

## Step 1: T is the traversal time

**Lemma 1.** If the path acceleration $\ddot s$ is the constant $a_k$ on $[s_k, s_{k+1}]$ and $\dot s^2 = b_k$ at $s_k$, then $\dot s^2 = b_{k+1}$ at $s_{k+1}$ exactly when $a_k = (b_{k+1} - b_k)/(2\Delta_k)$, and the time to cross the interval is $2\Delta_k / (\sqrt{b_k} + \sqrt{b_{k+1}})$.

*Proof.* $d(\dot s^2)/ds = 2\dot s \ddot s / \dot s = 2\ddot s$, so $\dot s^2$ is affine in $s$ on the interval: $\beta(s) = b_k + 2a_k (s - s_k)$, which gives the first claim. The time is $\int_{s_k}^{s_{k+1}} ds / \sqrt{\beta(s)}$. If $a_k \ne 0$ this is $(\sqrt{b_{k+1}} - \sqrt{b_k})/a_k = 2\Delta_k (\sqrt{b_{k+1}} - \sqrt{b_k})/(b_{k+1} - b_k) = 2\Delta_k/(\sqrt{b_k} + \sqrt{b_{k+1}})$. If $a_k = 0$ then $b_k = b_{k+1}$ and the time is $\Delta_k/\sqrt{b_k}$, the same value. $\square$

So the program "minimize $T(b)$ subject to $g_j(b) \le 0$" is exactly the discretized time-optimal path parameterization.

## Step 2: the program is convex

**Lemma 2.** $T$ is convex on $\{b \ge 0\}$, with the value $+\infty$ where some term has a zero denominator.

*Proof.* For one term, $\sigma(x, y) = \sqrt x + \sqrt y$ is concave on $[0, \infty)^2$ as a sum of concave functions, and $\phi(z) = 1/z$ is convex and decreasing on $(0, \infty)$. For points $p, q$ and $\theta \in [0, 1]$, concavity gives $\sigma(\theta p + (1 - \theta) q) \ge \theta \sigma(p) + (1 - \theta)\sigma(q)$; because $\phi$ is decreasing and then convex,

$$\phi(\sigma(\theta p + (1 - \theta) q)) \le \phi(\theta \sigma(p) + (1 - \theta)\sigma(q)) \le \theta \phi(\sigma(p)) + (1 - \theta)\phi(\sigma(q)).$$

With $\phi(0) = +\infty$ the inequality also holds when a denominator is zero. A sum of convex functions with positive weights $2\Delta_k$ is convex. $\square$

The constraints are affine, so the feasible set is a convex polyhedron, and every local minimum of $T$ on it is a global minimum.

## Step 3: the iterates stay strictly feasible

Line L1 accepts a start only if every slack $-g_j$ is positive. Line L8 accepts a step only if the barrier value is finite, that is, only if every slack of the new point is positive. So every iterate $b$, and the returned point, has $g_j(b) < 0$ for all $j$: it meets every limit and has $b_k > 0$ at the interior grid points.

## Step 4: the gap bound

For $t > 0$ let $\Phi_t(b) = t\,T(b) - \sum_j \log(-g_j(b))$ on the open set $D = \{b : g_j(b) < 0 \text{ for all } j\}$, and let $b(t)$ be its minimizer (the "central point").

**Lemma 3.** If $b(t)$ exists, then $T(b(t)) - T^* \le M/t$, where $T^*$ is the least value of $T$ on the feasible set.

*Proof.* At $b(t)$ the gradient of $\Phi_t$ is zero:

$$t \nabla T(b(t)) + \sum_j \frac{1}{-g_j(b(t))} \nabla g_j = 0.$$

Put $\lambda_j = 1/(t \cdot (-g_j(b(t)))) > 0$. Dividing by $t$, $\nabla T(b(t)) + \sum_j \lambda_j \nabla g_j = 0$, so $b(t)$ is a stationary point of the Lagrangian $\mathcal L(b) = T(b) + \sum_j \lambda_j g_j(b)$. $\mathcal L$ is convex (Lemma 2, plus affine terms), so $b(t)$ minimizes $\mathcal L$ over the open set where it is differentiable, and by continuity of $\mathcal L$ with values in $(-\infty, +\infty]$, also over its closure. For any feasible $\hat b$, $g_j(\hat b) \le 0$ and $\lambda_j > 0$, so

$$T(\hat b) \ge T(\hat b) + \sum_j \lambda_j g_j(\hat b) = \mathcal L(\hat b) \ge \mathcal L(b(t)) = T(b(t)) + \sum_j \lambda_j g_j(b(t)) = T(b(t)) - \frac{M}{t},$$

because each $\lambda_j g_j(b(t)) = -1/t$. Taking the infimum over feasible $\hat b$ gives $T^* \ge T(b(t)) - M/t$. $\square$

## Theorem

**Theorem.** Assume the start of line L1 is strictly feasible and each centering loop (lines L4 to L9) ends at the central point $b(t)$. Then the algorithm returns a point $b$ that meets every limit strictly, and $T(b) \le T^* + \varepsilon$.

*Proof.* Feasibility is Step 3. The algorithm returns at line L10 with $M/t < \varepsilon$, at the central point $b(t)$, so Lemma 3 gives $T(b) \le T^* + M/t < T^* + \varepsilon$. $\blacksquare$

## Remarks

The code stops each centering loop when half the squared Newton decrement $\lambda^2/2$ is below a tolerance $\eta$. For a self-concordant barrier problem, $\Phi_t(b) - \Phi_t(b(t)) \le \lambda^2$ when $\lambda$ is small (Boyd and Vandenberghe, Chapter 9), so the gap bound becomes $M/t + O(\eta/t)$. The function $1/(\sqrt x + \sqrt y)$ is not known to be self-concordant, so the classical bound on the number of Newton steps does not apply to this direct form. Verscheure et al. (2009) write the problem as a second-order cone program with auxiliary variables, for which the barrier is self-concordant and an interior point method needs $O(\sqrt M \log(M/\varepsilon))$ Newton steps. The step counts reported on the page are measurements.
