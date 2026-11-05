---
title: Color refinement terminates, is isomorphism-invariant, and returns the coarsest equitable refinement
proves: [correctness, termination]
status: full
---

**Setting.** Let $X = (V, E)$ be a finite simple undirected graph with $N$ vertices and an initial coloring $c_0$. In WL-TEST, $X$ is the disjoint union $G \uplus H$ and $N = 2n$. Write $N(v)$ for the set of neighbors of $v$, and for a coloring $c$ write $\{\!\{ c(w) : w \in N(v) \}\!\}$ for the multiset of neighbor colors. A coloring $d$ **refines** $c$ when $d(u) = d(v)$ implies $c(u) = c(v)$. Let $c_i$ be the coloring held after $i$ executions of L6, with $c_0$ the ranked coloring of L1.

**Lemma 1 (refinement).** For every $i$, $c_{i+1}$ refines $c_i$.

*Proof.* By L3 and L4, $c_{i+1}(u) = c_{i+1}(v)$ holds exactly when $\mathrm{sig}(u) = \mathrm{sig}(v)$. The first component of $\mathrm{sig}(v)$ is $c_i(v)$, so equal signatures give $c_i(u) = c_i(v)$. $\square$

**Lemma 2 (termination).** The loop runs at most $N$ times, and on return the coloring $c$ satisfies: for all $u, v$, $c(u) = c(v)$ implies $\{\!\{ c(w) : w \in N(u) \}\!\} = \{\!\{ c(w) : w \in N(v) \}\!\}$.

*Proof.* By Lemma 1 the partition of $c_{i+1}$ refines that of $c_i$, so it has at least as many classes, and it has exactly as many only when the two partitions are equal. L5 returns as soon as the number of classes does not grow. The number of classes is between 1 and $N$, so after at most $N$ iterations it stops growing. When L5 returns $c = c_i$, the partitions of $c_i$ and $c' = c_{i+1}$ are equal. If $c_i(u) = c_i(v)$ then $c_{i+1}(u) = c_{i+1}(v)$, so $\mathrm{sig}(u) = \mathrm{sig}(v)$, and the second components give equal multisets of neighbor colors under $c_i$. The sorted list in L3 represents the multiset exactly. $\square$

A coloring with the property of Lemma 2 is **equitable**: two vertices of the same color have, for each color $x$, the same number of neighbors of color $x$.

**Lemma 3 (invariance).** Let $\varphi : V \to V$ be a bijection with $\{u, v\} \in E \iff \{\varphi(u), \varphi(v)\} \in E$ and $c_0(\varphi(v)) = c_0(v)$ for all $v$. Then $c_i(\varphi(v)) = c_i(v)$ for all $i$ and all $v$.

*Proof.* By induction on $i$. The case $i = 0$ is the hypothesis, since L1 applies the same rank map to equal values. Assume the claim for $i$. The map $\varphi$ sends $N(v)$ bijectively onto $N(\varphi(v))$, so
$$\{\!\{ c_i(w) : w \in N(\varphi(v)) \}\!\} = \{\!\{ c_i(\varphi(w)) : w \in N(v) \}\!\} = \{\!\{ c_i(w) : w \in N(v) \}\!\}.$$
With $c_i(\varphi(v)) = c_i(v)$, this gives $\mathrm{sig}(\varphi(v)) = \mathrm{sig}(v)$ in round $i + 1$, and L4 gives both the same rank. $\square$

**Theorem 1 (soundness of WL-TEST).** If WL-TEST returns "not isomorphic", then there is no isomorphism from $G$ to $H$ that keeps the initial colors.

*Proof.* Assume $\psi : V(G) \to V(H)$ is such an isomorphism. Define $\varphi$ on $V = V(G) \uplus V(H)$ by $\varphi(v) = \psi(v)$ for $v \in V(G)$ and $\varphi(w) = \psi^{-1}(w)$ for $w \in V(H)$. Then $\varphi$ is a bijection of $V$, it maps edges of $X$ to edges and non-edges to non-edges (edges of $G$ go to edges of $H$ and back, and there are no edges between the two parts), and it keeps $c_0$. By Lemma 3 the returned coloring $c$ satisfies $c(\psi(v)) = c(v)$ for $v \in V(G)$. Since $\psi$ is a bijection from $V(G)$ onto $V(H)$, the multisets $\{\!\{ c(v) : v \in V(G) \}\!\}$ and $\{\!\{ c(w) : w \in V(H) \}\!\}$ are equal, so L8 does not report "not isomorphic". $\square$

**Theorem 2 (coarsest equitable refinement).** The returned coloring $c$ is equitable, refines $c_0$, and is refined by every equitable coloring $d$ that refines $c_0$. Hence its partition is the unique coarsest equitable partition that refines $c_0$.

*Proof.* Equitability is Lemma 2, and $c$ refines $c_0$ by Lemma 1 and transitivity. Let $d$ be equitable and refine $c_0$. We show by induction on $i$ that $d$ refines $c_i$. For $i = 0$ this is the hypothesis. Assume $d$ refines $c_i$, and let $d(u) = d(v)$. Then $c_i(u) = c_i(v)$. Since $d$ is equitable, for each $d$-color $y$ the vertices $u$ and $v$ have the same number of neighbors of color $y$. Each $c_i$-class is a union of $d$-classes, because $d$ refines $c_i$. Summing over the $d$-classes inside a $c_i$-class $x$, $u$ and $v$ have the same number of neighbors of $c_i$-color $x$, for every $x$. So their multisets of neighbor colors under $c_i$ are equal, $\mathrm{sig}(u) = \mathrm{sig}(v)$ in round $i + 1$, and $c_{i+1}(u) = c_{i+1}(v)$. So $d$ refines $c_{i+1}$, and in particular $d$ refines the returned $c$. If two equitable partitions both refine $c_0$ and are both refined by every such partition, each refines the other, so they are equal. $\square$

Lemma 2 gives termination, Theorem 1 gives the correctness of every "not isomorphic" answer, and Theorem 2 shows that the result does not depend on the order in which an implementation splits cells, so any correct [partition refinement](/partition-refinement/) computes the same stable partition. $\blacksquare$
