---
title: The simple DPSV algorithm keeps its invariants, terminates, and returns the Fisher market equilibrium
proves: [correctness, termination]
status: full
---

Fix $n$ buyers with budgets $e_i > 0$, $m$ goods with one unit each, and utilities $u_{ij} \ge 0$, where every buyer likes some good and every good is liked by some buyer. All arithmetic is exact. Write $p(T) = \sum_{j \in T} p_j$ and $e(K) = \sum_{i \in K} e_i$.

At the start of an iteration, let $H$ be the set of active goods and $A$ the set of active buyers. For $i \in A$ let $a_i = \max_{j \in H} u_{ij} / p_j$. The *active graph* has an edge $(i, j)$ for $i \in A$, $j \in H$ with $u_{ij} / p_j = a_i$, and $\Gamma(T)$ is the set of buyers joined to $T \subseteq H$ in it. For a frozen block $(B, K)$ (goods $B$, buyers $K$) and a buyer $k \in K$, let $\beta_k = \max_j u_{kj} / p_j$ over all goods, and $\Gamma_K(T)$ for $T \subseteq B$ the buyers $k \in K$ with $u_{kj} / p_j = \beta_k$ for some $j \in T$.

**Invariants.** At line L4:

- (I0) All prices are positive. $H$ and the blocks partition the goods, $A$ and the blocks partition the buyers, and $a_i > 0$ for every $i \in A$.
- (I1) $p(T) \le e(\Gamma(T))$ for every $T \subseteq H$.
- (I2) $u_{ij} / p_j \le a_i$ for every $i \in A$ and every frozen good $j$.
- (I3) Every block $(B, K)$ has $p(B) = e(K)$ and $p(T) \le e(\Gamma_K(T))$ for every $T \subseteq B$, and every $k \in K$ attains $\beta_k$ on some good of $B$.

**Claim 1 (start).** The invariants hold at the first iteration.

*Proof.* Let $c = \min_i e_i / m$ be the price of line L1 and $\alpha_i = \max_k u_{ik} / c > 0$. Line L2 sets $p_j = \max_i u_{ij} / \alpha_i$, which is positive because some buyer likes $j$, and at most $c$ because $u_{ij} / \alpha_i \le c$. For every buyer, the maximum of $u_{ij} / p_j$ is still $\alpha_i$ (a good of maximum utility keeps price $c$, and no ratio rises above $\alpha_i$ by the choice of $p_j$), and every good $j$ has an edge to the buyer that attains its maximum. So for every nonempty $T$, $\Gamma(T)$ is nonempty and $p(T) \le m c = \min_i e_i \le e(\Gamma(T))$. No block is frozen, so (I2) and (I3) are empty. $\square$

**Claim 2 (line L5).** Let $x^* = \min_{\emptyset \ne T \subseteq H} e(\Gamma(T)) / p(T)$. Line L5 makes at most $m$ rounds and returns $x_1 = x^*$ and the largest set $S$ with $e(\Gamma(S)) = x^* p(S)$. By (I1), $x^* \ge 1$.

*Proof.* For a set $S$ of goods and a factor $x$, the network of line L5 has source arcs of capacity $x p_j$ for $j \in S$, infinite arcs on the edges of $S$, and sink arcs of capacity $e_i$ for $i \in \Gamma(S)$. A cut whose source side contains the goods $X \subseteq S$ must contain $\Gamma(X)$ to be finite, and the cheapest such cut has capacity $c(X) = x \, p(S \setminus X) + e(\Gamma(X))$. The function $c$ is submodular in $X$, because $X \mapsto e(\Gamma(X))$ is a coverage function.

Call a set *critical* if its ratio $e(\Gamma(T)) / p(T)$ equals $x^*$. Critical sets are closed under union: for critical $T, T'$, $e(\Gamma(T \cup T')) + e(\Gamma(T \cap T')) \le e(\Gamma(T)) + e(\Gamma(T')) = x^* (p(T) + p(T'))$, and $e(\Gamma(T \cap T')) \ge x^* p(T \cap T')$ (trivially if the intersection is empty), so $e(\Gamma(T \cup T')) \le x^* p(T \cup T')$, with equality by the definition of $x^*$. So there is a largest critical set $S^*$.

Suppose the current $S$ contains $S^*$, which holds at the start since $S = H$. Let $x = e(\Gamma(S)) / p(S) \ge x^*$. The cut $X = \emptyset$ has capacity $x \, p(S) = e(\Gamma(S))$, the same as $X = S$. If the maximum flow has this value, then $c(X) \ge c(\emptyset)$ for all $X \subseteq S$, that is $e(\Gamma(X)) \ge x \, p(X)$, so $x \le x^*$, hence $x = x^*$; then $S$ is critical, and since $S \supseteq S^*$, $S = S^*$. Line L5 returns the right pair.

Otherwise $x > x^*$, and let $X_1$ be the goods of any minimum cut. Then $X_1 \ne S$, since $c(S) = c(\emptyset)$ is not minimum, and $X_1 \supseteq S^*$. Indeed, let $D = S^* \setminus X_1$ and suppose $D \ne \emptyset$. By the choice of $x^*$, $e(\Gamma(S^* \cap X_1)) \ge x^* p(S^* \cap X_1)$, so $e(\Gamma(S^*)) - e(\Gamma(S^* \cap X_1)) \le x^* p(D) < x \, p(D)$, that is $c(S^*) < c(S^* \cap X_1)$. By submodularity, $c(X_1 \cup S^*) \le c(X_1) + c(S^*) - c(X_1 \cap S^*) < c(X_1)$, which contradicts the minimality of $X_1$. So the new $S = X_1$ is a proper subset of the old one and still contains $S^*$. Each round removes a good, so there are at most $m$ rounds. $\square$

**Claim 3 (line L6).** $x_2 \ge 1$, and when it is finite, raising the active prices by any $x \le x_2$ keeps $u_{ij} / p_j \le a_i$ (with the new prices and the new $a_i$) for all $i \in A$ and frozen $j$.

*Proof.* By (I2), $a_i p_j / u_{ij} \ge 1$ for each pair in line L6. Multiplying the active prices by $x$ divides every $a_i$ by $x$ and keeps $p_j$ for frozen $j$, so $u_{ij} / p_j \le a_i / x_2 \le a_i / x$. $\square$

Raising all active prices by one factor keeps the active graph: every $u_{ij} / p_j$ with $j \in H$ and every $a_i$ are divided by the same number. Frozen buyers are unaffected, because their $\beta_k$ is attained on frozen goods whose prices stay, and active goods only get dearer.

**Claim 4 (line L9 keeps the invariants, and the new active part has no tight set).** Suppose $x = x_1 \le x_2$. After line L9, the invariants hold, and every nonempty $T$ of the new active goods has $p(T) < e(\Gamma'(T))$, where $\Gamma'$ is the new active graph.

*Proof.* After line L7, every $T \subseteq H$ has $e(\Gamma(T)) \ge x_1 p_{\text{old}}(T) = p(T)$, with equality for $T = S$, the largest such set (Claim 2). Let $K = \Gamma(S)$ be frozen with $S$.

(I3) for the new block: $p(S) = e(K)$. For $T \subseteq S$, $\Gamma(T) \subseteq K$ and $p(T) \le e(\Gamma(T))$. A buyer $k \in K$ has an edge into $S$, so $a_k$ is attained on $S$; by Claim 3, no frozen good beats $a_k$; so $\beta_k = a_k$ is attained on $S$, and $\Gamma_K(T) \supseteq \Gamma(T)$ for $T \subseteq S$. Old blocks keep (I3) by the remark after Claim 3.

New active buyers $A' = A \setminus K$ and goods $H' = H \setminus S$. A buyer $i \in A'$ has no edge into $S$, so her maximum over $H$ is attained in $H'$: her $a_i$ is unchanged and positive, and her edges are the same. So $\Gamma'(T) = \Gamma(T) \setminus K$ for $T \subseteq H'$. Then $\Gamma(S \cup T) \subseteq K \cup \Gamma'(T)$, and if $T \ne \emptyset$ had $p(T) \ge e(\Gamma'(T))$, then $e(\Gamma(S \cup T)) \le e(K) + e(\Gamma'(T)) \le p(S) + p(T)$, so $S \cup T$ would be a tight set larger than $S$. Hence $p(T) < e(\Gamma'(T))$, which gives (I1).

(I2): for $j \in S$ and $i \in A'$, $u_{ij} / p_j < a_i$ because $(i, j)$ is not an edge; for older frozen goods it is Claim 3. (I0) is clear. $\square$

**Claim 5 (line L8 keeps the invariants).** Suppose $x = x_2 < x_1$, attained by $i_0 \in A$ and a good $j_0$ of the block $(B, K)$. After line L8, the invariants hold, and every set $T$ of the new active goods with $p(T) = e(\Gamma''(T))$ in the new active graph $\Gamma''$ is a subset of $B \setminus \{j_0\}$.

*Proof.* After line L7, every nonempty $T \subseteq H$ has $e(\Gamma(T)) \ge x_1 p_{\text{old}}(T) > x_2 p_{\text{old}}(T) = p(T)$. By Claim 3, (I2) holds at the new prices, with equality for $(i_0, j_0)$.

The new active goods are $H'' = H \cup B$ and buyers $A'' = A \cup K$. For $i \in A$, the maximum over $H''$ equals $a_i$ by (I2), so her old edges stay and she may gain edges into $B$, among them $(i_0, j_0)$. For $k \in K$, the maximum over $H''$ is $\beta_k$, attained in $B$ by (I3), so her block edges stay. Take $T = T_1 \cup T_2$ with $T_1 \subseteq H$ and $T_2 \subseteq B$. Then $\Gamma''(T)$ contains the disjoint sets $\Gamma(T_1) \subseteq A$ and $\Gamma_K(T_2) \subseteq K$, so $e(\Gamma''(T)) \ge e(\Gamma(T_1)) + e(\Gamma_K(T_2)) \ge p(T_1) + p(T_2)$, which is (I1). Equality needs $T_1 = \emptyset$, and it fails if $j_0 \in T_2$, because then $i_0 \in \Gamma''(T) \setminus K$ adds $e_{i_0} > 0$.

(I2) for the remaining blocks: buyers of $A$ by Claim 3, buyers of $K$ because $\beta_k$ is the maximum over all goods. (I3) for the remaining blocks holds by the remark after Claim 3. (I0) is clear. $\square$

**Claim 6 (termination).** The loop of lines L4 to L9 ends after finitely many iterations.

*Proof.* Every factor is at least $1$ (Claims 2 and 3), so prices never fall. Call an iteration *flat* if its factor is $1$ and *rising* otherwise.

Flat iterations. By Claim 4, after a freeze the next $x_1$ is above $1$, so the next iteration is not a flat freeze. By Claim 5, a flat freeze right after an unfreeze of the block $B$ freezes fewer goods than $B$ has. At the very start there is no preceding unfreeze. So in a maximal run of consecutive flat iterations, every freeze except possibly the first is right after an unfreeze in the run. Group the run, after the possible first freeze, into units: an unfreeze alone, or an unfreeze followed by a freeze. Each unit lowers the number of frozen goods by at least $1$, and the first freeze raises it by at most $m$, so a run has at most $2m$ units and at most $4m + 1$ iterations.

Rising iterations. Let $P$ be the set of all numbers of the form $e(K) \, r_j / \sum_{l \in C} r_l$, where $C$ is a set of goods, $K$ a set of buyers, and $r$ a vector on $C$ obtained by choosing a spanning tree of a bipartite graph on $C \cup K$ whose edges have $u_{ij} > 0$ and setting $r$ along the tree by $r_{j'} = r_j u_{ij'} / u_{ij}$ from one root with $r = 1$. $P$ is finite. When line L9 freezes $S$ with $K = \Gamma(S)$, the components of the equality graph on $(S, K)$ split $S$ and $K$, each satisfies $p(C) \le e(\Gamma(C))$, and they add up to equality, so each component is tight; along its edges $p_{j'} / p_j = u_{ij'} / u_{ij}$, so every price in $S$ is in $P$. A frozen price does not change, so frozen goods always have prices in $P$. When line L8 fires at a rising factor, the buyer $i_0$ ties her best active good $k$ with $j_0$, so $p_k = p_{j_0} u_{i_0 k} / u_{i_0 j_0}$ lies in the finite set $Q = P \cup \{q \, u_{ik} / u_{ij} : q \in P\}$. At a rising freeze, the prices of $S$ lie in $P \subseteq Q$. So each rising iteration leaves some good $k$ whose price it has just strictly raised at a value in $Q$. For a fixed good, these values strictly increase from one such iteration to the next, since prices never fall. So there are at most $m \, |Q|$ rising iterations.

Between two rising iterations there is at most one run of flat iterations, so the loop makes at most $(m |Q| + 1)(4m + 2)$ iterations. $\square$

The bound is far from sharp. With integer data, Lemma 7.1 of the paper bounds the denominators of the prices in a newly tight set by $\Delta = m U^m$, and Corollary 7.5 bounds the phases of its Algorithm 1 by $M \Delta^2$.

**Claim 7 (output).** The returned $(p, x)$ is the Fisher market equilibrium: every buyer spends exactly $e_i$, only on goods $j$ with $u_{ij} / p_j = \max_k u_{ik} / p_k$, and every good $j$ receives exactly $p_j$, so it is sold completely.

*Proof.* The loop ends with $H = \emptyset$. In the last iteration, line L9 froze all active goods $S = H$, and every active buyer had an edge into $H$ because $a_i$ is attained there, so all buyers are frozen too. By (I3), every block $(B, K)$ is tight, its buyers attain their global maximum $\beta_k$ on $B$, and $p(T) \le e(\Gamma_K(T))$ for $T \subseteq B$. The edges of $\Gamma_K$ are equality edges of $N(p)$. By the max-flow min-cut theorem (Lemma 5.1 of the paper), the network of the block has a flow that saturates every source arc of $B$, of total $p(B) = e(K)$, so it saturates every sink arc of $K$ too. The blocks partition goods and buyers, so $N(p)$ has a flow of value $\sum_i e_i = \sum_j p_j$, and the maximum flow of line L10 saturates all source and sink arcs. Its flow from good $j$ to buyer $i$ is the money she spends on $j$, on equality edges only. A buyer who spends her whole budget only on goods of maximum bang per buck has an optimal bundle, so this is an equilibrium. The equilibrium prices of a linear Fisher market are unique (see the [Eisenberg-Gale program](/eisenberg-gale-program/)). $\blacksquare$
