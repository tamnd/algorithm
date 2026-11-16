---
title: Correctness of the SuperGlue optimal matching layer
proves: [correctness]
status: full
---

This proof covers the optimal matching layer only: lines L1 to L9 of the main page, on a given score matrix $S \in \mathbb{R}^{M \times N}$, with $M, N \ge 1$, and a given dustbin score $z$. Nothing here says that the network gives good scores; that is a measured property.

Line L1 builds $\bar S$ of size $(M + 1) \times (N + 1)$: $\bar S_{ij} = S_{ij}$ for $i < M$ and $j < N$, and $\bar S_{ij} = z$ in the last row and the last column. Line L2 sets $a = (1, \dots, 1, N)$ of length $M + 1$ and $b = (1, \dots, 1, M)$ of length $N + 1$. Write $\mathbf{1}$ for a vector of ones, and

$$U(a, b) = \{ P \in \mathbb{R}_{\ge 0}^{(M+1) \times (N+1)} : P \mathbf{1} = a, \; P^T \mathbf{1} = b \}.$$

For $P \ge 0$ let $H(P) = -\sum_{ij} P_{ij} (\log P_{ij} - 1)$, with $0 \log 0 = 0$, and $F(P) = \langle \bar S, P \rangle + H(P)$, where $\langle X, Y \rangle = \sum_{ij} X_{ij} Y_{ij}$.

**Lemma 1 (exact columns).** After each pass of lines L5 and L6, the matrix $P_{ij} = \exp(\bar S_{ij} + u_i + v_j)$ has column sums exactly $b$.

*Proof.* Line L6 sets $v_j = \log b_j - \log \sum_i \exp(\bar S_{ij} + u_i)$. Then $\sum_i P_{ij} = e^{v_j} \sum_i \exp(\bar S_{ij} + u_i) = b_j$. The log-sum-exp of the code subtracts the maximum before the exponentials, which changes no value in exact arithmetic. $\square$

**Lemma 2 (the target is feasible).** $\sum_i a_i = \sum_j b_j = M + N$, and $U(a, b)$ is a non-empty compact set.

*Proof.* $\sum_i a_i = M \cdot 1 + N$ and $\sum_j b_j = N \cdot 1 + M$. The matrix $P_{ij} = a_i b_j / (M + N)$ is in $U(a, b)$. The set is closed and each entry is at most $M + N$, so it is compact. $\square$

**Lemma 3 (a fixed point is the entropic optimum).** Suppose $P_{ij} = \exp(\bar S_{ij} + u_i + v_j)$ for some vectors $u, v$, and $P \in U(a, b)$. Then $P$ is the unique maximizer of $F$ over $U(a, b)$.

*Proof.* Each term $s p - p \log p + p$ is concave in $p \ge 0$ and strictly concave, so $F$ is strictly concave on the non-negative orthant. All entries of $P$ are positive, so $F$ is differentiable at $P$, with

$$\frac{\partial F}{\partial P_{ij}} = \bar S_{ij} - \log P_{ij} = -u_i - v_j.$$

Take $Q \in U(a, b)$. The function $t \mapsto F(P + t (Q - P))$ is concave on $[0, 1]$ and differentiable at $0$, so

$$F(Q) \le F(P) + \sum_{ij} (-u_i - v_j)(Q_{ij} - P_{ij}) = F(P) - \sum_i u_i (a_i - a_i) - \sum_j v_j (b_j - b_j) = F(P).$$

If $F(Q) = F(P)$ with $Q \ne P$, strict concavity gives $F((P + Q)/2) > F(P)$, and $(P + Q)/2$ is in the convex set $U(a, b)$, which contradicts the first part. $\square$

For a matrix $\exp(\bar S)$ with positive entries and positive marginals of equal sum, the alternating scaling of lines L5 and L6 converges to a matrix of the form in Lemma 3. This is Sinkhorn's theorem on matrix scaling, which Sinkhorn and Knopp proved for doubly stochastic targets; we use it and do not prove it here. Lemma 1 holds after every pass, and the row sums tend to $a$.

**Lemma 4 (temperature).** Let $\beta > 0$ and let $P_\beta$ be the maximizer of $\langle \beta \bar S, P \rangle + H(P)$ over $U(a, b)$, which is the limit of the algorithm on the input $\beta S$ and $\beta z$. Then for every $Q \in U(a, b)$,

$$\langle \bar S, Q \rangle - \langle \bar S, P_\beta \rangle \le \frac{H(P_\beta) - H(Q)}{\beta},$$

and the right side tends to 0 as $\beta \to \infty$.

*Proof.* $P_\beta$ also maximizes $\langle \bar S, P \rangle + H(P)/\beta$, so $\langle \bar S, P_\beta \rangle + H(P_\beta)/\beta \ge \langle \bar S, Q \rangle + H(Q)/\beta$. Rearrange. $H$ is continuous on the compact set $U(a, b)$ of Lemma 2, so $H(P_\beta) - H(Q)$ is bounded by $\max_U H - \min_U H$. $\square$

**Lemma 5 (the limit problem is a partial matching).** For $P \in U(a, b)$ let $Q$ be its real block, $Q_{ij} = P_{ij}$ for $i < M$ and $j < N$. Then

$$\langle \bar S, P \rangle = \sum_{i < M, j < N} (S_{ij} - z) Q_{ij} + z (M + N),$$

$Q$ is doubly substochastic (non-negative, with row and column sums at most 1), and each doubly substochastic $M \times N$ matrix is the real block of exactly one $P \in U(a, b)$. So $\max_{U(a,b)} \langle \bar S, P \rangle - z(M + N)$ is the maximum weight of a partial matching between rows and columns with edge weights $S_{ij} - z$.

*Proof.* Let $\sigma = \sum_{ij} Q_{ij}$. For $i < M$, row $i$ of $P$ sums to 1, so $P_{iN} = 1 - \sum_j Q_{ij} \ge 0$. For $j < N$, column $j$ sums to 1, so $P_{Mj} = 1 - \sum_i Q_{ij} \ge 0$. Row $M$ sums to $N$, so $P_{MN} = N - \sum_{j < N} P_{Mj} = N - (N - \sigma) = \sigma$; column $N$ then sums to $(M - \sigma) + \sigma = M$, as needed. So $P$ is determined by $Q$, any doubly substochastic $Q$ gives a $P \ge 0$ in $U(a, b)$, and

$$\langle \bar S, P \rangle = \sum S_{ij} Q_{ij} + z (M - \sigma) + z (N - \sigma) + z \sigma = \sum (S_{ij} - z) Q_{ij} + z (M + N).$$

The doubly substochastic matrices form the bipartite matching polytope, whose constraint matrix is totally unimodular, so its vertices are the 0-1 matrices of partial matchings. A linear function on a polytope reaches its maximum at a vertex. $\square$

So as the scale $\beta$ grows, the plan approaches the optimum of the linear program of Lemma 5: a pair can be matched only when $S_{ij} > z$, and the best partial matching of the weights $S_{ij} - z$ is chosen. When this matching is unique, the plan converges to it.

**Lemma 6 (the output is a partial matching).** The list of line L9 has each row index and each column index at most once, and each listed $P_{ij}$ is above the threshold $\theta$.

*Proof.* Line L8 gives one best column per row and one best row per column, with ties to the smaller index. A row $i$ is listed only with its own best column, so at most once. If two rows $i \ne i'$ were listed with the same column $j$, both would equal the best row of $j$, which is one index. The threshold test is in line L9. $\square$

**Theorem.** For any $T \ge 1$, the plan of line L7 has exact column sums $b$, and the output is a partial matching of pairs with $P_{ij} > \theta$. When the iterations converge, the plan is the unique maximizer of $\langle \bar S, P \rangle + H(P)$ over $U(a, b)$, and with scores scaled by $\beta$ its value is within $(\max_U H - \min_U H)/\beta$ of the best partial matching with weights $S_{ij} - z$, shifted by $z(M + N)$.

*Proof.* Lemmas 1 and 6 give the first sentence. Lemmas 2 and 3 give the second, and Lemmas 4 and 5 the third. $\blacksquare$
