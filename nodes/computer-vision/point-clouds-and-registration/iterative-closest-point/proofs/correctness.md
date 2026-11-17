---
title: ICP never increases the mean squared error and stops at a fixed point
proves: [correctness, termination]
status: full
---

We use the notation of the page. The source is $P = (p_1, \ldots, p_n)$ and the target is $Q = \{q_1, \ldots, q_m\}$, both in $\mathbb{R}^3$, with $n, m \ge 1$. For a rigid motion $(R, t)$ with $R \in SO(3)$ and a match $c : \{1, \ldots, n\} \to \{1, \ldots, m\}$, let

$$F(R, t, c) = \frac{1}{n} \sum_{i=1}^{n} |R p_i + t - q_{c(i)}|^2, \qquad E(R, t) = \min_{c} F(R, t, c) = \frac{1}{n} \sum_{i=1}^{n} \min_j |R p_i + t - q_j|^2 .$$

Line L3 computes the closest-point match $c_k$ of the pose $(R_k, t_k)$, with ties broken by the lowest index. Line L4 computes $e_k = F(R_k, t_k, c_k) = E(R_k, t_k)$. Line L6 computes $(R_{k+1}, t_{k+1}) = \mathrm{FIT}(c_k)$, the motion that the Kabsch step with the sign fix returns for the pairs $(p_i, q_{c_k(i)})$. We assume exact arithmetic and the default tol $= 0$.

**Claim.** (a) The costs that ICP meets never increase: $e_k \ge F(R_{k+1}, t_{k+1}, c_k) \ge e_{k+1}$ for every $k$. (b) With tol $= 0$ and no iteration cap, ICP stops after at most $m^n + 2$ executions of line L3. (c) When it stops at line L5, the returned pose $(R, t)$ has a closest-point match $c$ such that $(R, t)$ minimizes $F(\cdot, \cdot, c)$ over $SO(3) \times \mathbb{R}^3$. So $(R, t)$ is a fixed point of the two steps.

**Lemma 1 (the fit step).** For a fixed match $c$, $\mathrm{FIT}(c)$ minimizes $F(R, t, c)$ over $R \in SO(3)$ and $t \in \mathbb{R}^3$.

*Proof.* With $c$ fixed, $F(\cdot, \cdot, c)$ is $1/n$ times the cost of the [optimal superposition](/optimal-superposition/) problem for the pairs $(p_i, q_{c(i)})$. The [Kabsch algorithm](/kabsch-algorithm/) with the sign fix $R = V \operatorname{diag}(1, 1, d) U^{\mathsf T}$, $d = \operatorname{sign}\det(V U^{\mathsf T})$, returns a global minimizer of that cost over proper rotations and translations (Umeyama 1991, and the proof on the Kabsch page). $\square$

**Lemma 2 (the match step).** For a fixed pose $(R, t)$ and every match $c$, $E(R, t) \le F(R, t, c)$, with equality when $c$ is a closest-point match.

*Proof.* Each term of $F$ is at least $\min_j |R p_i + t - q_j|^2$, and a closest-point match attains this minimum in every term. $\square$

*Proof of (a).* By Lemma 1, $(R_{k+1}, t_{k+1})$ minimizes $F(\cdot, \cdot, c_k)$, and $(R_k, t_k)$ is one candidate, so $F(R_{k+1}, t_{k+1}, c_k) \le F(R_k, t_k, c_k) = e_k$. By Lemma 2 applied at the pose $(R_{k+1}, t_{k+1})$, $e_{k+1} = E(R_{k+1}, t_{k+1}) \le F(R_{k+1}, t_{k+1}, c_k)$. $\square$

*Proof of (b).* Suppose ICP does not stop at line L5 in the iterations $1, \ldots, K$ after the first. With tol $= 0$ the test of line L5 fails only when $e_{k-1} - e_k > 0$, so $e_0 > e_1 > \cdots > e_K$. Suppose $c_j = c_k$ for some $j < k \le K - 1$. FIT is a deterministic function of the match, so $(R_{j+1}, t_{j+1}) = (R_{k+1}, t_{k+1})$, and then $e_{j+1} = e_{k+1}$. This contradicts the strict decrease. So $c_0, \ldots, c_{K-1}$ are distinct maps from a set of $n$ elements to a set of $m$ elements, and $K \le m^n$. So ICP stops at line L5 in some iteration $k \le m^n + 1$, and line L3 runs at most $m^n + 2$ times (iterations $0, \ldots, m^n + 1$). $\square$

*Proof of (c).* ICP stops at line L5 in iteration $k \ge 1$ in one of two cases.

Case $c_k = c_{k-1}$. The returned pose is $(R_k, t_k) = \mathrm{FIT}(c_{k-1}) = \mathrm{FIT}(c_k)$, which minimizes $F(\cdot, \cdot, c_k)$ by Lemma 1, and $c_k$ is its closest-point match by line L3.

Case $e_k = e_{k-1}$. By part (a), $e_{k-1} \ge F(R_k, t_k, c_{k-1}) \ge e_k = e_{k-1}$, so $F(R_k, t_k, c_{k-1}) = e_k = E(R_k, t_k)$. Each term of $F(R_k, t_k, c_{k-1})$ is at least the matching term of $E(R_k, t_k)$, and the sums are equal, so every term is equal. Thus $c_{k-1}$ is also a closest-point match of $(R_k, t_k)$. It may differ from $c_k$ only where line L3 breaks a tie. The returned pose $(R_k, t_k) = \mathrm{FIT}(c_{k-1})$ minimizes $F(\cdot, \cdot, c_{k-1})$ by Lemma 1.

In both cases there is a closest-point match $c$ of the returned pose such that the returned pose minimizes $F(\cdot, \cdot, c)$. In the first iteration ($k = 0$) the test cannot hold, since $e_{-1} = \infty$ and there is no previous match. $\square$

**Theorem.** With tol $= 0$, ICP returns after finitely many iterations a pose $(R, t)$ with $\det R = +1$, the sequence of costs it meets never increases, and the returned pose is a fixed point of the two steps in the sense of (c).

*Proof.* Part (a) gives the monotone costs, part (b) the finite stop, and part (c) the fixed point property. The rotation is proper because each fit uses the sign fix of Lemma 1, and the start rotation is proper by assumption. $\blacksquare$

**Remarks.** The theorem does not say that the fixed point is a local minimum of $E$. When a moved point is at the same distance from two target points, $E$ is not differentiable there, and the page gives an example where a small translation lowers $E$ although ICP has stopped. The theorem gives no rate and no global optimum. The bound $m^n + 2$ is a crude count of matches, not a statement about the usual number of iterations.
