---
title: VF2 outputs exactly the mappings of the requested kind, each once
proves: [correctness, termination]
status: full
---

**Setting.** $G_1 = (V_1, E_1)$ and $G_2 = (V_2, E_2)$ are simple undirected graphs with vertex labels $\ell_1, \ell_2$, and $n_1 \le n_2$. A *target* is an injective map $m : V_1 \to V_2$ with $\ell_2(m(u)) = \ell_1(u)$ for all $u$ and, for all $u \ne w$ in $V_1$:

- mode mono: $\{u, w\} \in E_1 \implies \{m(u), m(w)\} \in E_2$;
- modes iso and induced: $\{u, w\} \in E_1 \iff \{m(u), m(w)\} \in E_2$, and in iso mode also $n_1 = n_2$.

A state is a partial injective map $M$. For a state, $T_i$ is the set of unmapped vertices of $G_i$ with at least one mapped neighbor and $\tilde N_i$ the set of unmapped vertices with none. A state $M$ *extends* to a target $m$ when $m(u) = M(u)$ for every $u$ mapped by $M$.

**Invariant (I).** For every state on the search path, any two mapped pattern vertices $u, w$ satisfy the edge condition of the mode for $M(u), M(w)$, labels agree on mapped vertices, and $M$ is injective.

*Proof of (I).* It holds for $M = \emptyset$. Let $(u, v)$ be added in L6. Both are unmapped, since L3 draws $u$ from unmapped pattern vertices and $v$ from unmapped host vertices, so $M \cup \{(u, v)\}$ is injective. L9 checks the label. For a mapped $w$: if $\{u, w\} \in E_1$, L10 checks $\{v, M(w)\} \in E_2$. In iso and induced mode, if $\{v, M(w)\} \in E_2$, then $M(w)$ is a mapped neighbor of $v$ and L10 checks $\{u, w\} \in E_1$. Pairs not involving $u$ are unchanged. $\square$

**Lemma 1 (soundness).** Every output of L2 is a target.

*Proof.* At L2, $|M| = n_1$, so $M$ is a total injective map $V_1 \to V_2$, and by (I) it satisfies the labels and the edge condition for every pair. In iso mode the algorithm starts only when $n_1 = n_2$. $\square$

**Lemma 2 (the rules keep every extendable state).** Let $M$ extend to a target $m$, let $u$ be unmapped, and let $v = m(u)$. Then $(u, v)$ passes L9 to L12.

*Proof.* L9: $m$ keeps labels. In iso mode $m$ is an isomorphism, so $\deg u = \deg v$. Otherwise $m$ maps the neighbors of $u$ injectively to neighbors of $v$, so $\deg u \le \deg v$. L10 holds because $m$ satisfies the edge condition for $u$ and each mapped vertex.

For L11 and L12 let $w$ be an unmapped neighbor of $u$. Then $m(w)$ is unmapped by $M$, since $m$ is injective and agrees with $M$ on the mapped vertices, and $m(w)$ is a neighbor of $v$.

- If $w \in T_1$, $w$ has a mapped neighbor $w'$, so $m(w)$ is adjacent to $M(w')$ and $m(w) \in T_2$. Hence $m$ maps $N_1(u) \cap T_1$ injectively into $N_2(v) \cap T_2$, and $|N_1(u) \cap T_1| \le |N_2(v) \cap T_2|$ in every mode.
- In iso and induced mode, if $w \in \tilde N_1$, then $m(w)$ has no mapped neighbor: a mapped neighbor $M(w')$ of $m(w)$ would make $w'$ a mapped neighbor of $w$. So $m(w) \in \tilde N_2$, and $|N_1(u) \cap \tilde N_1| \le |N_2(v) \cap \tilde N_2|$. This proves the induced rule.
- In mono mode, $m$ maps $N_1(u) \setminus M$ injectively into $N_2(v) \setminus M$, which proves the second mono rule.
- In iso mode, $m$ is a bijection with $m(T_1) = T_2$ and $m(\tilde N_1) = \tilde N_2$: the argument above applied to $m^{-1}$, which is an isomorphism extending $M^{-1}$, gives the reverse inclusions. Since $m$ maps $N_1(u)$ onto $N_2(v)$, the counts are equal. $\square$

**Lemma 3 (the right candidate is present).** Let $M$ extend to a target $m$ with $|M| < n_1$, and let $u$ be the pattern vertex chosen in L3. Then $(u, m(u))$ is in the candidate list.

*Proof.* If $T_1 \ne \emptyset$, then $u \in T_1$, and by the first point of the proof of Lemma 2, $m(u) \in T_2$, so $T_2 \ne \emptyset$ and $(u, m(u))$ is listed. If $T_1 = \emptyset$, $u$ is the smallest unmapped vertex. In mono and induced mode, every unmapped host vertex is listed, including $m(u)$. In iso mode, $m$ is a bijection that maps $T_1$ onto $T_2$, so $T_2 = \emptyset$ as well, and all unmapped host vertices are listed. $\square$

**Theorem.** VF2 terminates, and its outputs are exactly the targets, each output once.

*Proof.* *Termination.* Each step L6 increases $|M|$, which is at most $n_1$, and each state has a finite candidate list that is scanned once from left to right; so the search tree is finite, and the explicit stack visits each node once.

*Soundness* is Lemma 1.

*Completeness.* Let $m$ be a target. Start at $M_0 = \emptyset$, which extends to $m$. If $M_k$ extends to $m$ and $|M_k| < n_1$, Lemma 3 puts $(u_k, m(u_k))$ in the list of $M_k$, and Lemma 2 shows that it passes FEASIBLE; so the search enters $M_{k+1} = M_k \cup \{(u_k, m(u_k))\}$, which also extends to $m$. After $n_1$ steps L2 outputs $m$.

*Uniqueness.* The choice of $u$ in L3 depends only on the state, and distinct candidates at one state have distinct host vertices $v$, so distinct children of a node hold different values $M(u)$. Two output leaves with the same map would agree on every pair along the path from the root and so be the same leaf. Hence each target is output once. $\blacksquare$
