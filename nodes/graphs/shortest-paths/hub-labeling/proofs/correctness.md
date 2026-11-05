---
title: Pruned landmark labeling gives labels with the cover property, and queries return exact distances
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a directed graph with weights $w : E \to \mathbb{R}_{\ge 0}$ and let $v_1, \ldots, v_n$ be the order of the vertices. Write $d(x, y)$ for the shortest-path distance, $+\infty$ if $y$ is not reachable from $x$. The *rank* of $v_k$ is $k$. For vertices $u, v$ with $d(u, v) < \infty$, let

$$S(u, v) = \{ x \in V : d(u, x) + d(x, v) = d(u, v) \}.$$

Round $k$ is the execution of lines L3 and L4 for this $k$.

**Fact 1 (pruned search is Dijkstra on a subgraph).** In one call of PRUNED-SEARCH from $h$ in $H$, let $P$ be the set of vertices skipped in line L7. The decision for a vertex $x$ is made when $x$ is extracted, and it only decides whether the arcs out of $x$ are relaxed, which happens after $x$ is extracted in any case. So the run is the same as a run of Dijkstra from $h$ in the graph $H'$ obtained from $H$ by deleting the arcs out of the vertices of $P$. As all weights are nonnegative, Dijkstra is correct on $H'$: every vertex $x$ reachable from $h$ in $H'$ is extracted exactly once, with key $D(x) = d_{H'}(h, x)$, and vertices not reachable in $H'$ are never extracted.

**Fact 2 (upper bounds).** For every pair $(k, D)$ in $\mathrm{Lin}(x)$, $D \ge d(v_k, x)$, and for every pair $(k, D)$ in $\mathrm{Lout}(x)$, $D \ge d(x, v_k)$. Consequently, at any time, $\mathrm{QUERY}(u, v) \ge d(u, v)$.

*Proof.* A pair $(k, D)$ in $\mathrm{Lin}(x)$ is appended in line L8 of the forward search of round $k$, with $D = d_{H'}(v_k, x)$ by Fact 1. Every path in $H'$ is a path in $G$, so $D \ge d(v_k, x)$. Backward searches run on the reverse of $G$, where a path from $v_k$ to $x$ is a path from $x$ to $v_k$ in $G$, so the same holds for out-labels. A query value is $a + b$ for some $k$ with $(k, a) \in \mathrm{Lout}(u)$ and $(k, b) \in \mathrm{Lin}(v)$, so $a + b \ge d(u, v_k) + d(v_k, v) \ge d(u, v)$ by the triangle inequality. $\square$

**Fact 3 (what the labels hold during round $k$).** While the forward search of round $k$ runs, every out-label holds only pairs with rank less than $k$. While the backward search of round $k$ runs, every in-label holds only pairs with rank at most $k$, and the out-label of a vertex $x$ that has not yet been extracted in this search holds only ranks less than $k$.

*Proof.* Pairs with rank $k$ are appended to out-labels only in the backward search of round $k$, which starts after the forward search ends, and a vertex gets its pair from this search only when it is extracted. Pairs of rank $k' > k$ are appended only in later rounds. $\square$

**Lemma 4 (no prune on the path from the first vertex).** Let $d(u, v) < \infty$, and let $h = v_k$ be the vertex of $S(u, v)$ of least rank. (The set is not empty, as $u \in S(u, v)$.)

(a) Let $h = x_0, x_1, \ldots, x_r = v$ be a shortest path from $h$ to $v$ in $G$. In the forward search of round $k$, each $x_j$ is extracted with key $d(h, x_j)$ and is not pruned.

(b) Let $u = y_r, y_{r-1}, \ldots, y_0 = h$ be a shortest path from $u$ to $h$ in $G$. In the backward search of round $k$, each $y_j$ is extracted with key $d(y_j, h)$ and is not pruned.

*Proof of (a).* First, every $x_j$ is in $S(u, v)$: the prefix and suffix of a shortest path are shortest, so $d(h, x_j) + d(x_j, v) = d(h, v)$, and

$$d(u, x_j) + d(x_j, v) \le d(u, h) + d(h, x_j) + d(x_j, v) = d(u, h) + d(h, v) = d(u, v),$$

where the last equality holds because $h \in S(u, v)$. The reverse inequality is the triangle inequality, so equality holds.

Now induct on $j$. Assume $x_0, \ldots, x_{j-1}$ are extracted and not pruned (nothing is assumed for $j = 0$). Then their arcs are kept in $H'$, so the path $x_0, \ldots, x_j$ lies in $H'$, and by Fact 1, $x_j$ is extracted with key $D = d_{H'}(h, x_j) \le d(h, x_j)$. As $H'$ is a subgraph of $G$, $D = d(h, x_j)$.

Suppose $x_j$ were pruned in line L7: $\mathrm{QUERY}(h, x_j) \le D$. Then there are a rank $k'$ and values $a, b$ with $(k', a) \in \mathrm{Lout}(h)$, $(k', b) \in \mathrm{Lin}(x_j)$ and $a + b \le d(h, x_j)$. By Fact 3, $k' < k$; write $h' = v_{k'}$. By Fact 2, $d(h, h') + d(h', x_j) \le a + b \le d(h, x_j)$. Then

$$d(u, h') + d(h', v) \le d(u, h) + d(h, h') + d(h', x_j) + d(x_j, v) \le d(u, h) + d(h, x_j) + d(x_j, v) = d(u, v),$$

using $x_j \in S(u, v)$ and $h \in S(u, v)$ in the last step as above. So $h' \in S(u, v)$ and $h'$ has rank $k' < k$, against the choice of $h$. Hence $x_j$ is not pruned, which completes the induction.

*Proof of (b).* The same argument on the reverse of $G$. Each $y_j$ is in $S(u, v)$ by the symmetric computation. If $y_j$ were pruned, $\mathrm{QUERY}(y_j, h) \le d(y_j, h)$ would give a rank $k'$ with $(k', a) \in \mathrm{Lout}(y_j)$ and $(k', b) \in \mathrm{Lin}(h)$. By Fact 3, $\mathrm{Lout}(y_j)$ holds only ranks below $k$ when $y_j$ is extracted, so $k' < k$, and $h' = v_{k'}$ gives $d(y_j, h') + d(h', h) \le d(y_j, h)$. As before this puts $h'$ into $S(u, v)$ with rank less than $k$, a contradiction. $\square$

**Theorem (cover property).** For all $u, v$ with $d(u, v) < \infty$, with $h = v_k$ as in Lemma 4, the final labels contain $(k, d(u, h)) \in \mathrm{Lout}(u)$ and $(k, d(h, v)) \in \mathrm{Lin}(v)$.

*Proof.* By Lemma 4(a) with $j = r$, the vertex $v$ is extracted in the forward search of round $k$ with key $d(h, v)$ and is not pruned, so line L8 appends $(k, d(h, v))$ to $\mathrm{Lin}(v)$. By Lemma 4(b) with $j = r$, line L8 of the backward search appends $(k, d(u, h))$ to $\mathrm{Lout}(u)$. Pairs are never removed. $\square$

**Corollary (queries are exact).** After line L5, $\mathrm{QUERY}(u, v) = d(u, v)$ for all $u, v$.

*Proof.* Each label holds at most one pair per rank, because a vertex is extracted at most once per search, and the pairs are appended in increasing order of rank, because rounds run in increasing $k$. So both lists are sorted by rank with distinct ranks, and the merge in lines L9 and L10 finds exactly the ranks in both lists. If $d(u, v) < \infty$, the theorem gives a common rank $k$ with sum $d(u, h) + d(h, v) = d(u, v)$, since $h \in S(u, v)$; by Fact 2 no sum is smaller, so line L11 returns $d(u, v)$. If $d(u, v) = +\infty$, a common rank $k$ with finite values would give $d(u, v_k) < \infty$ and $d(v_k, v) < \infty$, so $v$ would be reachable from $u$; hence there is none and line L11 returns $\infty$. $\square$

**Termination.** Line L2 runs $n$ rounds, each with two searches. A search is Dijkstra on a finite graph: each vertex is extracted at most once and each arc relaxed at most once, so the heap receives at most $m + 1$ entries and the search ends. Each query in line L7 merges two finite lists. So the algorithm stops after $2n$ searches. $\blacksquare$
