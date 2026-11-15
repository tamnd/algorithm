---
title: The CBF-QP algorithm returns the unique minimizer or correctly reports infeasibility, and the filtered closed loop keeps the safe set forward invariant
proves: [correctness, termination, safety]
status: full
---

At a fixed state, the problem is

$$\min_{u \in B} \ \tfrac12 |u - u_{\text{nom}}|^2 \quad \text{subject to} \quad a \cdot u + b \ge 0,$$

where $a \in \mathbb{R}^m$, $b \in \mathbb{R}$, and $B = \prod_j [\ell_j, r_j]$ is a box in which a bound may be absent ($\ell_j = -\infty$ or $r_j = +\infty$), with $\ell_j \le r_j$. The factor $\frac12$ does not change the minimizer. Write $\operatorname{clip}$ for the projection onto $B$, which clamps each coordinate to $[\ell_j, r_j]$. For $\lambda \ge 0$ put

$$u(\lambda) = \operatorname{clip}(u_{\text{nom}} + \lambda a), \qquad \psi(\lambda) = a \cdot u(\lambda) + b.$$

## Termination

Lines L1 to L3 and L6 are loops over the $m$ coordinates. Line L4 makes at most $2m$ breakpoints. The binary search of line L5 halves the interval $[lo, hi)$ of indices at each step, so it ends after at most $\lceil \log_2(2m + 1) \rceil$ steps. So the algorithm ends.

## Lemma 1: the inner minimization

For each $\lambda \ge 0$, $u(\lambda)$ minimizes $L(u, \lambda) = \frac12 |u - u_{\text{nom}}|^2 - \lambda (a \cdot u + b)$ over $B$.

*Proof.* $L(u, \lambda) = \sum_j \bigl(\frac12 (u_j - u_{\text{nom}, j})^2 - \lambda a_j u_j\bigr) - \lambda b = \sum_j \frac12 \bigl(u_j - (u_{\text{nom}, j} + \lambda a_j)\bigr)^2 + \text{const}$, where the constant does not depend on $u$. The sum is separable, and the minimizer of $\frac12 (u_j - c)^2$ over an interval is $c$ clamped to the interval. $\square$

## Lemma 2: the shape of psi

$\psi$ is continuous and nondecreasing on $[0, \infty)$. It is linear between consecutive points of $\Lambda = \{ \lambda > 0 : \lambda = (\ell_j - u_{\text{nom}, j}) / a_j \text{ or } \lambda = (r_j - u_{\text{nom}, j}) / a_j, \ a_j \neq 0 \}$, the set of line L4. After the largest point of $\Lambda$ (after 0 if $\Lambda$ is empty), its slope is $s = \sum \{ a_j^2 : a_j > 0, r_j = \infty \text{ or } a_j < 0, \ell_j = -\infty \}$.

*Proof.* $\psi(\lambda) - b = \sum_j a_j\, \operatorname{clamp}_j(u_{\text{nom}, j} + \lambda a_j)$. Terms with $a_j = 0$ are zero. If $a_j > 0$, the argument increases with $\lambda$, the clamp is continuous and nondecreasing, and the term is $a_j$ times it, so it is nondecreasing. If $a_j < 0$, the argument decreases, the clamp of it is nonincreasing, and the factor $a_j < 0$ makes the term nondecreasing. The clamp is linear (slope 1 or 0) between the values of $\lambda$ where the argument crosses $\ell_j$ or $r_j$, and these values are in $\Lambda$ when they are positive. So each term is linear between points of $\Lambda$, with slope $a_j^2$ when the coordinate is strictly inside its interval and 0 when it is clamped. After the last point of $\Lambda$, a coordinate with $a_j > 0$ has passed every finite bound that it can cross. If $r_j$ is finite it is clamped at $r_j$; otherwise it is free. The case $a_j < 0$ is the same with $\ell_j$. This gives $s$. $\square$

## Lemma 3: the feasibility test

The problem is feasible if and only if $M + b \ge 0$, where $M = \sup_{u \in B} a \cdot u = \sum_j \sup_{u_j \in [\ell_j, r_j]} a_j u_j$. $M = \infty$ if and only if some $a_j > 0$ has $r_j = \infty$ or some $a_j < 0$ has $\ell_j = -\infty$; otherwise $M = \sum_{a_j > 0} a_j r_j + \sum_{a_j < 0} a_j \ell_j$, and the supremum is attained.

*Proof.* The supremum of a separable linear function over a box is the sum of the suprema over the intervals. If $M$ is finite it is attained at the point described, so a feasible point exists if and only if $M + b \ge 0$. If $M = \infty$, some point of $B$ has $a \cdot u + b \ge 0$. Line L3 computes exactly this test. $\square$

## Theorem 1: the QP step

If the problem is infeasible, the algorithm returns INFEASIBLE. Otherwise it returns the unique minimizer $u^*$ and a multiplier $\lambda^* \ge 0$ with $u^* = u(\lambda^*)$ and $\lambda^* \psi(\lambda^*) = 0$.

*Proof.* *Sufficiency of the conditions.* Suppose $\lambda \ge 0$, $u(\lambda)$ is feasible and $\lambda \psi(\lambda) = 0$. For every feasible $v$,

$$\tfrac12 |v - u_{\text{nom}}|^2 \ge \tfrac12 |v - u_{\text{nom}}|^2 - \lambda (a \cdot v + b) = L(v, \lambda) \ge L(u(\lambda), \lambda) = \tfrac12 |u(\lambda) - u_{\text{nom}}|^2 - \lambda \psi(\lambda) = \tfrac12 |u(\lambda) - u_{\text{nom}}|^2,$$

using $\lambda \ge 0$ and $a \cdot v + b \ge 0$, then Lemma 1. So $u(\lambda)$ is a minimizer. The objective is strictly convex and the feasible set is convex, so the minimizer is unique.

*Line L2.* If $\psi(0) \ge 0$, then $\lambda = 0$ satisfies the conditions, and the answer is $u(0) = \operatorname{clip}(u_{\text{nom}})$.

*Line L3.* If the test fails, the problem is infeasible by Lemma 3, and the answer is correct. From now on $\psi(0) < 0$ and the problem is feasible.

*Lines L4 and L5.* Let $\lambda_1 < \dots < \lambda_K$ be the sorted points of $\Lambda$. By Lemma 2 the values $\psi(\lambda_k)$ are nondecreasing in $k$, so the predicate $\psi(\lambda_k) \ge 0$ is false and then true, and the binary search returns the first index with a true value, or $K + 1$ if there is none. Put $\lambda_0 = 0$.

- If the index $k$ is at most $K$, then $\psi(\lambda_{k-1}) < 0 \le \psi(\lambda_k)$. $\psi$ is linear on $[\lambda_{k-1}, \lambda_k]$, so the linear interpolation of line L5 gives the root $\lambda^*$ in this interval exactly.
- If no point has $\psi \ge 0$, then $\psi(\lambda_K) < 0$ (or $\psi(0) < 0$ if $K = 0$). If $M$ were finite, then at $\lambda \ge \lambda_K$ every coordinate with $a_j \neq 0$ would sit at the bound that attains $M$, so $\psi(\lambda_K) = M + b \ge 0$, a contradiction. So $M = \infty$, and the slope $s$ of Lemma 2 is positive. Then $\lambda^* = \lambda_K + (-\psi(\lambda_K)) / s$ is the root.

In both cases $\lambda^* > 0$ and $\psi(\lambda^*) = 0$, so $u(\lambda^*)$ is feasible, and the conditions hold. Line L6 returns $u(\lambda^*)$. Every operation is a field operation, so the result is exact with rational data. $\square$

## Theorem 2: forward invariance of the safe set

Let $x' = f(x) + g(x) u$ with $f$, $g$ locally Lipschitz on an open set $D$. Let $h : D \to \mathbb{R}$ be continuously differentiable, let $C = \{x \in D : h(x) \ge 0\}$ be closed in $\mathbb{R}^n$, and let $\alpha : \mathbb{R} \to \mathbb{R}$ be locally Lipschitz, strictly increasing, with $\alpha(0) = 0$. Suppose that for every $x \in D$ the QP with $a = \nabla h(x)^T g(x)$, $b = \nabla h(x)^T f(x) + \alpha(h(x))$ and the box $B$ is feasible, and that its solution $k(x)$ makes $F(x) = f(x) + g(x) k(x)$ locally Lipschitz on $D$. Then every solution with $x(0) \in C$ stays in $C$ on its whole interval of existence.

*Proof.* The closed loop has unique solutions (Picard-Lindelöf). Let $x$ be a solution with $x(0) \in C$ on $[0, t_f)$, and let $T$ be the supremum of the times $t < t_f$ with $x([0, t]) \subset D$. On $[0, T)$, put $\eta(t) = h(x(t))$. By the chain rule and the constraint of the QP,

$$\dot\eta = \nabla h(x)^T \bigl(f(x) + g(x) k(x)\bigr) = a \cdot k(x) + b - \alpha(\eta) \ge -\alpha(\eta).$$

Let $y$ be the solution of $\dot y = -\alpha(y)$, $y(0) = \eta(0) \ge 0$. It is unique because $\alpha$ is locally Lipschitz. The constant $0$ is a solution, so a solution with $y(0) \ge 0$ cannot cross zero, and $y(t) \ge 0$. By the comparison lemma (Khalil 2002, Lemma 3.4, applied to $v = -\eta$, which satisfies $\dot v \le \alpha(-v)$), $\eta(t) \ge y(t) \ge 0$ on $[0, T)$. So $x(t) \in C$ for $t < T$.

If $T < t_f$, then $x(T) \in C$ because $C$ is closed and $x$ is continuous, so $x(T) \in D$. $D$ is open, so $x$ stays in $D$ a little longer after $T$, which contradicts the choice of $T$. So $T = t_f$, and $x(t) \in C$ for all $t \in [0, t_f)$.

For $\alpha(s) = \gamma s$ the comparison is explicit: $\frac{d}{dt}(e^{\gamma t} \eta) = e^{\gamma t} (\dot\eta + \gamma \eta) \ge 0$, so $\eta(t) \ge e^{-\gamma t} \eta(0) \ge 0$. $\square$

## Remark: when the closed loop is Lipschitz

Without the box, Theorem 1 gives the closed form $k(x) = u_{\text{nom}} + \max(0, -\psi(0))\, a / |a|^2$. If $u_{\text{nom}}$, $a$ and $b$ are locally Lipschitz in $x$ and $a(x) \neq 0$ on $D$, then $k$ is locally Lipschitz, because sums, products, the maximum of two Lipschitz functions and the quotient by a function that stays away from zero on compact sets are locally Lipschitz. So the hypothesis of Theorem 2 holds in this case. The theorem says nothing about a controller that holds $k(x(t_k))$ between sampling times; then $\dot\eta \ge -\alpha(\eta)$ holds only at the sampling instants. $\blacksquare$
