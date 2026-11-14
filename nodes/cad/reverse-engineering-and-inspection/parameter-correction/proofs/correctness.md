---
title: Parameter correction never increases the error, bounds the orthogonal error, stops at points where the error vectors are normal to the curve, and keeps the true curve on noise-free data
proves: [correctness, termination]
status: full
---

**Setup.** $N_{1,p}, \dots, N_{n,p}$ are the B-spline basis functions of degree $p$ on a clamped knot vector with parameter interval $[a, b]$. For control points $P = (P_1, \dots, P_n)$ in $\mathbb{R}^d$ the curve is $C_P(t) = \sum_i N_{i,p}(t) P_i$. The data are $Q_0, \dots, Q_m$, and for parameters $t = (t_0, \dots, t_m) \in [a, b]^{m+1}$,
$$ E(P, t) = \sum_{k=0}^{m} \lvert Q_k - C_P(t_k) \rvert^2, \qquad D(P) = \sum_{k=0}^{m} \min_{s \in [a, b]} \lvert Q_k - C_P(s) \rvert^2 . $$
The minimum in $D$ exists because $C_P$ is continuous on the compact interval. $N(t)$ is the $(m + 1) \times n$ collocation matrix with entries $N_{i,p}(t_k)$. One iteration of the algorithm maps $(P^j, t^j)$ to $(P^{j+1}, t^{j+1})$: line L4 gives $t^{j+1}$ with
$$ \lvert Q_k - C_{P^j}(t^{j+1}_k) \rvert \le \lvert Q_k - C_{P^j}(t^j_k) \rvert \quad \text{for every } k, \tag{1} $$
and line L5 gives $P^{j+1}$, a minimizer of $E(\cdot, t^{j+1})$. Line L2 gives $P^0$, a minimizer of $E(\cdot, t^0)$. Write $E_j = E(P^j, t^j)$.

**Termination.** Each iteration does a fixed amount of work: $S + 1$ curve samples, at most $k$ Newton steps per data point, and one linear solve. The loop runs at most the iteration limit. So the algorithm stops.

**Lemma 1 (the fit step).** For fixed $t$, $E(P, t) = \lVert \mathbf{Q} - N(t) \mathbf{P} \rVert_F^2$, where $\mathbf{Q}$ and $\mathbf{P}$ have the points as rows. Its minimizers are the solutions of $N^{\mathsf T} N \mathbf{P} = N^{\mathsf T} \mathbf{Q}$, and the minimizer is unique exactly when $N(t)$ has full column rank.

*Proof.* $C_P(t_k) = \sum_i N_{i,p}(t_k) P_i$ is row $k$ of $N \mathbf{P}$, so the formula for $E$ holds. The Frobenius norm splits into the $d$ columns, and each column is a linear least squares problem $\lVert q - N x \rVert^2$. Its gradient is $2 N^{\mathsf T}(N x - q)$, and it is convex, so the minimizers are exactly the solutions of the normal equations. They form an affine set of dimension equal to the nullity of $N$, so the minimizer is unique exactly when $N$ has full column rank. $\square$

**Theorem 1 (monotone error).** $E_{j+1} \le E_j$ for every $j$. So the sequence $E_j$ converges to a limit $E_\infty \ge 0$.

*Proof.* By (1), summed over $k$, $E(P^j, t^{j+1}) \le E(P^j, t^j) = E_j$. By Lemma 1, $P^{j+1}$ minimizes $E(\cdot, t^{j+1})$, so $E_{j+1} = E(P^{j+1}, t^{j+1}) \le E(P^j, t^{j+1})$. Together $E_{j+1} \le E_j$. A nonincreasing sequence bounded below by $0$ converges. $\square$

The code keeps the end parameters fixed and keeps any new $t_k$ only when it is not farther than the old one, so (1) holds for every $k$ in the code, whether or not Newton's method converges.

**Theorem 2 (the orthogonal error).** (a) $D(P) \le E(P, t)$ for every $P$ and $t$, so $D(P^j) \le E_j$. (b) If in every iteration each $t^{j+1}_k$ is a global foot point, $\lvert Q_k - C_{P^j}(t^{j+1}_k) \rvert = \min_s \lvert Q_k - C_{P^j}(s) \rvert$ for all $k$, then $D(P^{j+1}) \le D(P^j)$.

*Proof.* (a) Each term of $D$ is a minimum over $s$, which is at most the value at $s = t_k$. (b) With global foot points, $E(P^j, t^{j+1}) = D(P^j)$. Then by (a) and Lemma 1, $D(P^{j+1}) \le E(P^{j+1}, t^{j+1}) \le E(P^j, t^{j+1}) = D(P^j)$. $\square$

In the code the foot points come from samples and Newton steps and are global foot points in practice, not by proof; and the end parameters stay fixed, so (b) applies only when the end points are not moved. Part (a) holds always.

**Theorem 3 (fixed points are stationary).** Let $(P, t)$ satisfy: $P$ minimizes $E(\cdot, t)$, and each $t_k$ with $a < t_k < b$ is a local minimizer of $s \mapsto \lvert Q_k - C_P(s) \rvert^2$, at which $C_P$ is differentiable. Then for each such $k$
$$ \bigl( Q_k - C_P(t_k) \bigr) \cdot C_P'(t_k) = 0 , \tag{2} $$
and $\partial E / \partial P = 0$ and $\partial E / \partial t_k = 0$ for each such $k$. If, in addition, every $t_k$ is interior, the unique global minimizer of its term, and nondegenerate (the second derivative of the term is positive there), then $D$ is differentiable at $P$ and $\nabla D(P) = 0$.

*Proof.* $\partial E / \partial t_k = -2 (Q_k - C_P(t_k)) \cdot C_P'(t_k)$, which is zero at an interior local minimizer of the $k$-th term because only that term depends on $t_k$. This is (2). $\partial E / \partial P = -2 N^{\mathsf T}(\mathbf{Q} - N \mathbf{P})$ is zero by Lemma 1. For the last part, let $h_k(P, s) = \lvert Q_k - C_P(s) \rvert^2$, which is smooth in $P$ and, on each knot span, in $s$. At the nondegenerate minimizer, $\partial h_k / \partial s = 0$ and $\partial^2 h_k / \partial s^2 > 0$, so by the implicit function theorem there is a smooth $s_k(P')$ near $P$ with $\partial h_k / \partial s (P', s_k(P')) = 0$; since the global minimizer is unique and the minimum depends continuously on $P'$, $s_k(P')$ is the global minimizer for $P'$ near $P$. Then $D(P') = \sum_k h_k(P', s_k(P'))$ and, by the chain rule, $\nabla D(P) = \sum_k \bigl( \partial h_k / \partial P + \partial h_k / \partial s \cdot \nabla s_k \bigr) = \sum_k \partial h_k / \partial P = \partial E / \partial P (P, t) = 0$. $\square$

Equation (2) says that every error vector at an interior parameter is normal to the curve, which is Hoschek's intrinsic parameterization. When $t_k$ is a knot where $C_P$ has only $C^{p-1}$ continuity with $p = 1$, the curve may have a corner there and (2) need not hold.

**Theorem 4 (noise-free data).** Let $Q_k = C_{P^*}(\tau_k)$ for some control points $P^*$ and parameters $\tau \in [a, b]^{m+1}$ with $\tau_0 = a$, $\tau_m = b$, and let $N(\tau)$ have full column rank. Started at $t^0 = \tau$, the algorithm returns $P^j = P^*$ and $E_j = 0$ for every $j$, provided the collocation matrices of the later parameters have full rank. In the code, $t^j = \tau$ for every $j$.

*Proof.* $E(P^*, \tau) = 0$, which is the least possible value, so $P^*$ minimizes $E(\cdot, \tau)$; by Lemma 1 it is the only minimizer, so $P^0 = P^*$ and $E_0 = 0$. Suppose $P^j = P^*$ and $E_j = 0$. By (1), every new parameter satisfies $\lvert Q_k - C_{P^*}(t^{j+1}_k) \rvert \le 0$, so $C_{P^*}(t^{j+1}_k) = Q_k$ and $E(P^*, t^{j+1}) = 0$. Again $P^*$ is a minimizer of $E(\cdot, t^{j+1})$, the only one when $N(t^{j+1})$ has full rank, so $P^{j+1} = P^*$ and $E_{j+1} = 0$. In the code, the search starts at the old parameter with squared distance $0$; a sample replaces it only when strictly closer, which is impossible, and the first Newton step has $g = (C(t) - Q_k) \cdot C'(t) = 0$, so it does not move. Hence $t^{j+1} = \tau$, the rank condition holds by assumption, and the induction goes through. $\blacksquare$
