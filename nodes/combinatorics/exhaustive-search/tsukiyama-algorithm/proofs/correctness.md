---
title: The Tsukiyama algorithm lists each maximal independent set exactly once
proves: [correctness]
status: full
---

We use the notation of the page: $G_i$ is the subgraph induced by $v_1, \ldots, v_i$, a set is *maximal in $G_i$* when it is a maximal independent set of $G_i$, and $\mathcal{M}_i$ is the family of these sets. The *nodes at level $i$* are the sets $S$ for which a call TSUKIYAMA$(S, i)$ happens, counted with multiplicity.

**Lemma 1 (GREEDY).** If $X$ is independent in $G_i$, then GREEDY$_i(X)$ is maximal in $G_i$ and contains $X$.

*Proof.* GREEDY starts from $X$ and only adds a vertex with no neighbor in the current set, so the result is independent and contains $X$. Each vertex $u$ of $G_i$ is examined once. If it is not in the result, it had a neighbor in the set at that time, and that neighbor stays in the set. So the result is maximal. $\square$

**Lemma 2 (children are maximal).** If $S \in \mathcal{M}_i$ and $v = v_{i+1}$, then every child made at lines L4, L6 and L9 is in $\mathcal{M}_{i+1}$.

*Proof.* *Line L4.* $S \cap N(v) = \emptyset$, so $S \cup \{v\}$ is independent. A vertex $u$ of $G_i$ outside $S$ has a neighbor in $S$ because $S$ is maximal in $G_i$. So $S \cup \{v\}$ is maximal in $G_{i+1}$.

*Line L6.* $S$ is independent in $G_{i+1}$. A vertex of $G_i$ outside $S$ has a neighbor in $S$, and $v$ has a neighbor in $S$ because $S \cap N(v) \ne \emptyset$. So $S$ is maximal in $G_{i+1}$.

*Line L9.* $T = (S \setminus N(v)) \cup \{v\}$ is independent, because $S \setminus N(v)$ is independent and has no neighbor of $v$. Line L8 tests that it is maximal in $G_{i+1}$. $\square$

**Lemma 3 (unique parent).** Let $T \in \mathcal{M}_{i+1}$ and $v = v_{i+1}$. Exactly one pair of a set $S \in \mathcal{M}_i$ and a line among L4, L6, L9 produces $T$ from $S$.

*Proof.* Lines L4 and L9 produce sets that contain $v$, and line L6 produces a set without $v$.

*Case $v \notin T$.* Only line L6 can produce $T$, from $S = T$. Indeed $T$ is independent in $G_i$, and a vertex of $G_i$ outside $T$ has a neighbor in $T$, so $T \in \mathcal{M}_i$. Since $T$ is maximal in $G_{i+1}$ and $v \notin T$, the vertex $v$ has a neighbor in $T$, so $T \cap N(v) \neq \emptyset$ and the call at $S = T$ takes the branch of line L6. So $T$ has exactly one parent.

*Case $v \in T$.* Let $X = T \setminus \{v\}$. Then $X \cap N(v) = \emptyset$, because $T$ is independent.

If $X \in \mathcal{M}_i$, line L4 at $S = X$ produces $T$, since $X \cap N(v) = \emptyset$. Line L4 at any other $S$ produces $S \cup \{v\} \ne T$. Line L9 at some $S$ would need $S \setminus N(v) = X$ and $S \cap N(v) \ne \emptyset$, so $X \subsetneq S$ with $S$ independent, which contradicts the maximality of $X$. So $T$ has exactly one parent.

If $X \notin \mathcal{M}_i$, line L4 cannot produce $T$, since it would need $S = X$. Line L9 at $S$ produces $T$ if and only if $S \cap N(v) \ne \emptyset$, $S \setminus N(v) = X$, $T$ is maximal in $G_{i+1}$ (true), and GREEDY$_i(X) = S$. The last condition allows at most one $S$, namely $S^* = \mathrm{GREEDY}_i(X)$. We show that $S^*$ satisfies the other two. By Lemma 1, $S^* \in \mathcal{M}_i$ and $X \subseteq S^*$. Since $X \subseteq S^*$ and $X \cap N(v) = \emptyset$, we have $X \subseteq S^* \setminus N(v)$. Suppose some $u \in S^* \setminus N(v)$ is not in $X$. Then $u \ne v$ and $u \notin T$, so by the maximality of $T$ in $G_{i+1}$, $u$ has a neighbor $w \in T$. Here $w \ne v$, because $u \notin N(v)$, so $w \in X \subseteq S^*$. Then $u$ and $w$ are adjacent members of $S^*$, a contradiction. So $S^* \setminus N(v) = X$. Finally $S^* \ne X$, because $S^*$ is maximal and $X$ is not, so $S^*$ has a vertex outside $X$, and by the equality just shown that vertex is in $N(v)$. So $S^* \cap N(v) \ne \emptyset$, the call at $S^*$ takes the branch of line L5, and line L9 produces $T$. So $T$ has exactly one parent. $\square$

**Theorem.** For each $i = 0, \ldots, n$, the nodes at level $i$ are the sets of $\mathcal{M}_i$, each exactly once. In particular, the outputs of line L1 are the maximal independent sets of $G = G_n$, each exactly once.

*Proof.* By induction on $i$. At level 0 the only node is $\emptyset$, and $\mathcal{M}_0 = \{\emptyset\}$. Assume the claim at level $i < n$. By Lemma 2, every node at level $i + 1$ is in $\mathcal{M}_{i+1}$. By Lemma 3 and the induction hypothesis, each $T \in \mathcal{M}_{i+1}$ has exactly one parent node at level $i$, which makes $T$ exactly once. $\blacksquare$

**No dead ends.** Every call at a level $i < n$ makes at least one recursive call: line L4 or line L6 always runs. So every root-to-leaf path has length $n$ and ends with an output, which gives the bound on the delay on the page.
