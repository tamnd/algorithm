---
title: Properties of HNSW search, the level law, and exactness without pruning
proves: [correctness]
status: full
---

Let $\delta$ be a distance on a set of elements, with $\delta(x, x) = 0$. HNSW is approximate, so we prove three properties: what SEARCH-LAYER returns, the law of the levels, and that the search is exact in a limiting setting.

**Lemma 1 (SEARCH-LAYER).** SEARCH-LAYER$(q, E, ef, l)$ ends, and it returns the $\min(ef, |O|)$ elements nearest to $q$ among the set $O$ of elements ever added to $W$, where $E \subseteq O \subseteq V$.

*Proof.* An element enters $V$ at most once, at line L1 or line L5, and enters $C$ only when it enters $V$. So $C$ receives at most as many elements as there are elements on layer $l$, and the loop of line L2, which removes one element of $C$ per pass, ends. $W$ is a max-heap with at most $ef$ elements. An element is removed from $W$ only when $|W| > ef$, and the removed one is the farthest. So after each offer $W$ holds the $\min(ef, |O|)$ nearest elements of $O$, by induction on the offers, exactly as for a bounded heap in top-k selection. $\square$

**Lemma 2 (levels).** If $U$ is uniform in $(0, 1]$ and $\ell = \lfloor -\ln U / \ln M \rfloor$ with $M \ge 2$, then $\Pr[\ell \ge j] = M^{-j}$ for every integer $j \ge 0$, and $\mathbb{E}[\ell] = 1/(M - 1)$.

*Proof.* $\ell \ge j$ if and only if $-\ln U / \ln M \ge j$, that is, $U \le M^{-j}$, which has probability $M^{-j}$. Then $\mathbb{E}[\ell] = \sum_{j \ge 1} \Pr[\ell \ge j] = \sum_{j \ge 1} M^{-j} = 1/(M - 1)$. $\square$

So an element lies on $1 + 1/(M-1)$ layers in expectation, and the expected number of elements on layer $j$ is $n M^{-j}$.

**Lemma 3 (reach).** If $ef \ge n$, where $n$ is the number of elements on layer $l$, then SEARCH-LAYER$(q, E, ef, l)$ adds to $V$ every element reachable from $E$ along the directed links $N_l$.

*Proof.* Since $|W| \le n \le ef$, line L1 cuts nothing, and the removal of line L6 never happens: $W$ would need more than $ef \ge n$ elements. So every element of $V$ is in $W$. The test of line L6 holds for every new $e$, since $|W| < ef$ unless $|W| = n$, in which case all elements are in $V$ and there is no new $e$. So every element of $V$ enters $C$. An element $c$ taken from $C$ is in $W$, so $\delta(q, c) \le \delta(q, \text{farthest of } W)$, and line L4 never breaks. So every element of $V$ is expanded at line L5. Then $V$ is closed under the links: if $c \in V$ and $e \in N_l(c)$, then $e \in V$. A set that contains $E$ and is closed under the links contains everything reachable from $E$. $\square$

**Lemma 4 (connectivity).** Suppose no list $N_0$ is ever cut at line L15 (for example $M_0 \ge n - 1$) and SELECT returns a nonempty set whenever $W$ is not empty. Then after any number of insertions, every element is reachable from every other along layer-0 links.

*Proof.* Without cuts, line L14 adds each link in both directions and no link is removed, so the layer-0 links form an undirected graph. The first element alone is connected. When a later element $x$ is inserted, layer 0 is among its layers, and the search of line L14 on layer 0 starts from a nonempty set, so $W$ is not empty and SELECT links $x$ to at least one earlier element. The simple rule keeps the nearest element of $W$; the heuristic keeps it too, since the set of kept elements is empty when it is scanned. So the graph stays connected. $\square$

**Theorem.** Under the conditions of Lemma 4, K-NN-SEARCH$(q, k, ef)$ with $ef \ge n$ returns $k$ elements whose distances to $q$ are the $k$ smallest.

*Proof.* Line L8 gives a nonempty entry set on layer 0. By Lemma 4 every element is reachable from it, and by Lemma 3 with $ef \ge n$ every element is added to $V$ and, by the proof of Lemma 3, to $W$. So $O$ is the set of all elements, and by Lemma 1 the returned $W$ holds the $\min(ef, n) = n$ elements in order of distance. Line L10 returns the first $k$. $\blacksquare$
