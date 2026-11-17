---
title: The trimmed mean squared error of TrICP never increases, and TrICP stops
proves: [correctness, termination]
status: full
---

We use the notation of the page. The source is $P = (p_1, \ldots, p_n)$ and the target is $Q = \{q_1, \ldots, q_m\}$ in $\mathbb{R}^3$. The overlap is $\xi \in (0, 1]$, and line L1 sets the number of kept pairs to $N_{po} = \max(3, \lfloor \xi n \rfloor)$, with $N_{po} \le n$. For a pose $(R, t)$ let $d_i(R, t) = \min_j |R p_i + t - q_j|$. For a set $S$ of $N_{po}$ source indices and a match $c$, let

$$F(R, t, S, c) = \frac{1}{N_{po}} \sum_{i \in S} |R p_i + t - q_{c(i)}|^2, \qquad e(R, t) = \min_{|S| = N_{po}} \frac{1}{N_{po}} \sum_{i \in S} d_i(R, t)^2 .$$

So $e(R, t)$ is the mean of the $N_{po}$ least squared closest-point distances, the trimmed MSE. In iteration $k$, line L3 computes the closest-point match $c_k$ of the pose $(R_k, t_k)$, line L4 the set $S_k$ of the $N_{po}$ indices with the least distances, and line L5 the value $e_k = F(R_k, t_k, S_k, c_k) = e(R_k, t_k)$. Line L7 computes $(R_{k+1}, t_{k+1}) = \mathrm{FIT}(S_k, c_k)$, the Kabsch motion with the sign fix for the pairs $(p_i, q_{c_k(i)})$, $i \in S_k$. We assume exact arithmetic, eps $= 0$ and tol $= 0$.

**Claim.** (a) $e_k \ge F(R_{k+1}, t_{k+1}, S_k, c_k) \ge e_{k+1}$ for every $k$, so the trimmed MSE never increases. (b) TrICP stops at line L6 after finitely many iterations. (c) When it stops, there is a set $S$ of $N_{po}$ indices and a closest-point match $c$ of the returned pose $(R, t)$ such that $S$ holds $N_{po}$ least distances at $(R, t)$ and $(R, t)$ minimizes $F(\cdot, \cdot, S, c)$. (d) With $\xi = 1$ and $n \ge 3$, TrICP is point-to-point ICP.

**Lemma 1 (the fit step).** For fixed $S$ and $c$, $\mathrm{FIT}(S, c)$ minimizes $F(R, t, S, c)$ over $R \in SO(3)$ and $t \in \mathbb{R}^3$.

*Proof.* With $S$ and $c$ fixed, $N_{po} F$ is the least squares cost of the matched pairs $(p_i, q_{c(i)})$, $i \in S$. The [Kabsch algorithm](/kabsch-algorithm/) with the sign fix returns a global minimizer of that cost over proper rotations and translations. $\square$

**Lemma 2 (the match and trim step).** For a fixed pose and every set $S$ of $N_{po}$ indices and every match $c$, $e(R, t) \le F(R, t, S, c)$.

*Proof.* Each term $|R p_i + t - q_{c(i)}|^2$ is at least $d_i(R, t)^2$. The sum of $d_i^2$ over $S$ is at least the sum of the $N_{po}$ least values of $d_i^2$, which is $N_{po}\, e(R, t)$. $\square$

*Proof of (a).* $(R_k, t_k)$ is one candidate for the fit of $(S_k, c_k)$, so Lemma 1 gives $F(R_{k+1}, t_{k+1}, S_k, c_k) \le F(R_k, t_k, S_k, c_k) = e_k$. Lemma 2 at the pose $(R_{k+1}, t_{k+1})$ gives $e_{k+1} \le F(R_{k+1}, t_{k+1}, S_k, c_k)$. $\square$

*Proof of (b).* If TrICP does not stop in iterations $1, \ldots, K$, then $e_0 > e_1 > \cdots > e_K$, because line L6 stops when $e_{k-1} - e_k \le 0$. If $(S_j, c_j) = (S_k, c_k)$ for some $j < k \le K - 1$, then $(R_{j+1}, t_{j+1}) = (R_{k+1}, t_{k+1})$, since FIT is deterministic, and $e_{j+1} = e_{k+1}$, a contradiction. The pairs $(S_k, c_k)$ take at most $\binom{n}{N_{po}} m^n$ values, so $K$ is at most this number, and TrICP stops. $\square$

*Proof of (c).* If TrICP stops by $e_k \le$ eps $= 0$, then $e_k = 0$, so $(R_k, t_k)$ minimizes $F(\cdot, \cdot, S_k, c_k) \ge 0$, and $S_k$, $c_k$ are as required. Otherwise it stops in iteration $k \ge 1$ with $e_k = e_{k-1}$. By part (a), $F(R_k, t_k, S_{k-1}, c_{k-1}) = e_k = e(R_k, t_k)$. Every term in this sum is at least the matching $d_i(R_k, t_k)^2$, and the sum equals the sum of the $N_{po}$ least values. So every term equals $d_i^2$, and $S_{k-1}$ holds $N_{po}$ least distances at $(R_k, t_k)$. We can extend $c_{k-1}$ on $S_{k-1}$ by $c_k$ outside $S_{k-1}$ to a closest-point match $c$ of $(R_k, t_k)$, with $F(\cdot, \cdot, S_{k-1}, c) = F(\cdot, \cdot, S_{k-1}, c_{k-1})$. By Lemma 1, $(R_k, t_k) = \mathrm{FIT}(S_{k-1}, c_{k-1})$ minimizes it. $\square$

*Proof of (d).* With $\xi = 1$ and $n \ge 3$, $N_{po} = n$, so $S_k = \{1, \ldots, n\}$, and $e$ and $F$ are the cost of point-to-point ICP. The fit, the costs and the stop test are those of ICP with tol $= 0$, except that ICP also stops when the match repeats; a repeated match gives the same fit and the same cost, so TrICP stops one iteration later at the same pose. $\square$

**Theorem.** With eps $= 0$ and tol $= 0$, TrICP returns after finitely many iterations a pose with a proper rotation. The trimmed MSE of the poses it visits never increases, and the returned pose is a fixed point of the match, trim and fit steps in the sense of (c).

*Proof.* Parts (a), (b) and (c), and the sign fix of Lemma 1 for $\det R = +1$. $\blacksquare$

**What this proof does not give.** As for ICP, the result is local: the fixed point can be far from the true pose, and it need not be a local minimum of $e$ when distances tie. The proof also says nothing about the choice of $\xi$. If $\xi$ is larger than the true overlap, some kept pairs are wrong, and the fit is biased. The rule of Chetverikov et al. that chooses $\xi$ by minimizing $e(\xi)/\xi^{1 + \lambda}$ is a heuristic, not part of this theorem.
