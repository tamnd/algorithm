---
title: Björklund's algorithm returns the chromatic number
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a finite simple undirected graph with $V = \{0, \ldots, n - 1\}$, and identify subsets of $V$ with bit masks. A set $T \subseteq V$ is *independent* if no edge has both ends in $T$; the empty set is independent. For $S \subseteq V$ let

$$f(S) = |\{ T \subseteq S : T \text{ independent} \}|.$$

If $n = 0$, line L1 returns $0 = \chi(G)$. Assume $n \ge 1$ from now on.

**Lemma 1 (lines L2 and L3).** After line L3 has run for every nonempty mask, $\mathrm{ind}[S] = 1$ if $S$ is independent and $0$ otherwise, for every $S$.

*Proof.* Induction on the mask value. $\mathrm{ind}[\emptyset] = 1$ and $\emptyset$ is independent. For $S \ne \emptyset$, let $v$ be its smallest vertex. The mask of $S - v$ is smaller, so $\mathrm{ind}[S - v]$ is already correct when $S$ is processed. $S$ is independent if and only if $S - v$ is independent and $v$ has no neighbor in $S - v$; since $v \notin N(v)$, the second condition is $N(v) \cap S = \emptyset$. $\square$

**Lemma 2 (lines L4 and L5).** After line L5 has run for every vertex, $f[S] = f(S)$ for every $S$.

*Proof.* Let $v_1, \ldots, v_n$ be the vertices in the order of line L4, and $D_j = \{v_1, \ldots, v_j\}$. We claim that after the first $j$ rounds,

$$f[S] = \sum \{ \mathrm{ind}[T] : T \subseteq S,\ S \setminus T \subseteq D_j \}.$$

For $j = 0$ the only such $T$ is $S$, and $f = \mathrm{ind}$. In round $j$, line L5 changes only the entries $f[S]$ with $v_j \in S$, and it reads $f[S - v_j]$, which round $j$ does not change because $v_j \notin S - v_j$. So, for $v_j \in S$, the new $f[S]$ is the sum of the old $f[S]$ and the old $f[S - v_j]$. By the claim for $j - 1$, the first sums over the $T \subseteq S$ with $S \setminus T \subseteq D_{j-1}$, which are those with $v_j \in T$; the second sums over the $T \subseteq S - v_j$ with $(S - v_j) \setminus T \subseteq D_{j-1}$, which are those with $v_j \notin T$. Together they are the $T \subseteq S$ with $S \setminus T \subseteq D_j$. For $v_j \notin S$, no $T \subseteq S$ differs from $S$ at $v_j$, and the entry is already right. After round $n$, $D_n = V$, so $f[S] = \sum_{T \subseteq S} \mathrm{ind}[T] = f(S)$ by Lemma 1. $\square$

**Lemma 3 (covers).** For every $k \ge 1$, the value $c$ of line L7 equals the number $\mathrm{cov}_k$ of $k$-tuples $(I_1, \ldots, I_k)$ of independent sets with $I_1 \cup \cdots \cup I_k = V$.

*Proof.* By Lemma 2, $f(S)^k$ is the number of $k$-tuples of independent sets that all lie in $S$, that is, whose union $U$ satisfies $U \subseteq S$. So

$$c = \sum_{S \subseteq V} (-1)^{n - |S|} f(S)^k = \sum_{(I_1, \ldots, I_k)} \ \sum_{U \subseteq S \subseteq V} (-1)^{n - |S|},$$

where the outer sum on the right runs over all $k$-tuples of independent sets and $U$ is the union of the tuple. Writing $S = U \cup R$ with $R \subseteq V \setminus U$, and $r = |V \setminus U|$, the inner sum is $\sum_{R} (-1)^{r - |R|} = (1 - 1)^r$, which is 1 if $r = 0$ and 0 if $r > 0$. So each tuple with union $V$ counts once and every other tuple counts zero. $\square$

**Lemma 4.** For $k \ge 1$, $\mathrm{cov}_k > 0$ if and only if $\chi(G) \le k$.

*Proof.* If $c : V \to \{1, \ldots, k\}$ is a proper coloring, the color classes $I_i = c^{-1}(i)$ are independent, possibly empty, and their union is $V$, so $\mathrm{cov}_k \ge 1$. Conversely, given a cover $(I_1, \ldots, I_k)$ by independent sets, color each vertex $v$ with the least $i$ such that $v \in I_i$. Every vertex gets a color, since the union is $V$. If $uv$ is an edge and both get color $i$, then $u, v \in I_i$, which contradicts independence. So this is a proper coloring with at most $k$ colors. $\square$

**Theorem.** BJORKLUND-CHROMATIC$(G)$ terminates and returns $\chi(G)$.

*Proof.* The case $n = 0$ is line L1. For $n \ge 1$, lines L2 to L5 are loops over finite ranges. The loop of line L6 tries $k = 1, 2, \ldots, n$ in order. By Lemmas 3 and 4, at round $k$ line L8 returns exactly when $\chi(G) \le k$. Since $1 \le \chi(G) \le n$, because the $n$ singletons form a proper coloring, the loop returns at round $k = \chi(G)$ and not before. In the implementation, line L7 builds $f(S)^k$ as the product of the stored $f(S)^{k-1}$ and $f(S)$, which equals the value in the pseudocode. $\blacksquare$
