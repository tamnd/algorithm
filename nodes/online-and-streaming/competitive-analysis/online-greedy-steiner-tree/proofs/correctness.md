---
title: The online greedy Steiner tree is 2(H_k - 1)-competitive
proves: [correctness]
status: full
---

**Model.** $G = (V, E)$ is a connected undirected graph with nonnegative edge weights $w$, and $d$ is its shortest path metric. Terminals $t_1, \ldots, t_k$ arrive online, and we may assume that they are distinct, because a repeated terminal costs nothing. $\mathrm{OPT}$ is the weight of a minimum Steiner tree for $\{t_1, \ldots, t_k\}$. Let $T_i$ be the tree of the algorithm after step $i$, and $c_i$ the cost of step $i$, so $c_1 = 0$ and $\mathrm{ALG} = \sum_{i=1}^{k} c_i$.

**Lemma 1 (the output is a Steiner tree).** For each $i$, $T_i$ is a tree that contains $t_1, \ldots, t_i$, and its weight is $c_1 + \cdots + c_i$.

*Proof.* By induction on $i$. $T_1$ is the single vertex $t_1$. If $t_i \in T_{i-1}$, nothing changes. Otherwise line L5 takes a shortest path $P$ from $t_i$ to the first vertex $z$ of $T_{i-1}$ that Dijkstra's algorithm settles. Each vertex of $P$ before $z$ is an ancestor of $z$ in the search tree, so it was settled before $z$. The search stops at the first settled vertex of $T_{i-1}$, so no vertex of $P$ before $z$ is in $T_{i-1}$. So $P$ meets $T_{i-1}$ only in $z$, adding $P$ keeps the graph connected and acyclic, and the weight grows by $w(P) = c_i$. $\square$

**Lemma 2 (step cost).** For $i \ge 2$, $c_i \le \min_{j < i} d(t_i, t_j)$.

*Proof.* Each $t_j$ with $j < i$ is a vertex of $T_{i-1}$, and $c_i = d(t_i, V(T_{i-1}))$ is the distance to the nearest vertex of the tree. $\square$

**Lemma 3 (a walk around the optimal tree).** Let $U$ be any set of terminals with $\lvert U \rvert = q \ge 2$ whose points are pairwise at distance at least $\lambda$. Then $q \lambda \le 2\,\mathrm{OPT}$.

*Proof.* Let $T^*$ be an optimal Steiner tree. A depth-first walk around $T^*$ uses each edge twice, so it is a closed walk of length $2\,\mathrm{OPT}$ that visits every terminal. List the points of $U$ in the order of their first visit, as $u_1, \ldots, u_q$, and let $u_{q+1} = u_1$. The walk passes from $u_r$ to $u_{r+1}$ for each $r$, and these $q$ parts of the closed walk are disjoint. Each part has length at least $d(u_r, u_{r+1}) \ge \lambda$. So $q\lambda \le 2\,\mathrm{OPT}$. $\square$

**Theorem 4.** $\mathrm{ALG} \le 2 (H_k - 1)\,\mathrm{OPT}$, where $H_k = \sum_{i=1}^{k} 1/i$. The bound holds with additive constant $0$, and also for the variant that connects $t_i$ to the nearest earlier terminal.

*Proof.* Sort the costs of steps $2, \ldots, k$ as $c_{(1)} \ge c_{(2)} \ge \cdots \ge c_{(k-1)}$. Fix $j$ with $1 \le j \le k - 1$. Let $I$ be the indices of $j$ steps with the largest costs, so that $c_i \ge c_{(j)}$ for $i \in I$, and let $U = \{t_1\} \cup \{t_i : i \in I\}$. The set $U$ has $j + 1$ distinct terminals, because $1 \notin I$.

Take two points of $U$, and let $t_b$ be the one that arrived later. Then $b \in I$, and the other point arrived before $t_b$. By Lemma 2 their distance is at least $c_b \ge c_{(j)}$. So the points of $U$ are pairwise at distance at least $c_{(j)}$, and Lemma 3 with $q = j + 1$ gives

$$c_{(j)} \le \frac{2\,\mathrm{OPT}}{j + 1}.$$

Summing over $j$,

$$\mathrm{ALG} = \sum_{j=1}^{k-1} c_{(j)} \le 2\,\mathrm{OPT} \sum_{j=1}^{k-1} \frac{1}{j + 1} = 2 (H_k - 1)\,\mathrm{OPT}.$$

For the variant, the step cost is exactly $\min_{j < i} d(t_i, t_j)$, and the same argument applies. $\square$

**Corollary 5.** $\mathrm{ALG} \le 2 \ln k \cdot \mathrm{OPT}$, since $H_k - 1 \le \ln k$.

**Remark (tightness).** The ratio of the greedy rule is $\Theta(\log k)$. On the diamond graph of level $L$ with $k = 2^L + 1$ terminals, the adversary that requests the midpoint on the lighter side of each segment makes greedy pay $(1 + L/2)\,\mathrm{OPT}$. The lower bound $\mathrm{ALG} \ge \tfrac{1}{4} \log_2 (k - 1)\,\mathrm{OPT}$ for every online algorithm, deterministic or randomized, is proved on the online Steiner tree problem page.
