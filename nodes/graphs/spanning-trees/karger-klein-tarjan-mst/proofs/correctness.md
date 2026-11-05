---
title: The Karger-Klein-Tarjan algorithm returns the minimum spanning forest on every run, and stops
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a finite undirected graph with $n$ vertices and a real weight on each edge. Parallel edges are allowed, weights may tie, and $G$ need not be connected; self-loops are dropped at the start, since no forest contains one. Give each edge the key $(w(e), i)$, where $i$ is its index in the input, and compare keys lexicographically. Keys are distinct, so for every subgraph $H$ of $G$ (or of a graph obtained from $G$ by contraction) there is exactly one minimum spanning forest for the keys, written $\mathrm{MSF}(H)$; it is also a minimum spanning forest for the weights.

We prove that KKT (lines L1 to L6 of the page) stops on every sequence of coin flips and returns $\mathrm{MSF}(G)$. The coins change only the running time.

## Facts used

**Fact 1 (cut property).** For every vertex $v$ with an edge, the edge of least key at $v$ is in $\mathrm{MSF}(H)$. It is the edge of least key that crosses the cut $(\{v\}, V \setminus \{v\})$; see the [cut property](/cut-property/).

**Fact 2 (cycle property).** If an edge $e$ lies on a cycle of $H$ and has the largest key on that cycle, then $e \notin \mathrm{MSF}(H)$; see the [cycle property](/cycle-property/). Consequently, deleting such an edge does not change $\mathrm{MSF}(H)$: the forest does not use $e$, and it stays a minimum spanning forest of the smaller graph, which has the same components.

**Fact 3 (contraction).** Let $C \subseteq \mathrm{MSF}(H)$, and let $H / C$ be $H$ with each tree of $C$ contracted to one vertex and the loops removed; each remaining edge keeps its key and its identity. Then $\mathrm{MSF}(H) = C \cup \mathrm{MSF}(H / C)$.

*Proof of Fact 3.* Spanning forests of $H$ that contain $C$ correspond one to one to spanning forests of $H / C$, by deleting or adding the edges of $C$: a set $F' \subseteq E(H / C)$ is acyclic and has the components of $H / C$ exactly when $C \cup F'$ is acyclic and has the components of $H$. The key sums differ by the constant total of $C$. The unique minimum spanning forest of $H$ contains $C$, so it is the image of the minimum of $H / C$. $\square$

## The Borůvka steps

**Lemma 1.** One call of the Borůvka step on a graph $H$ returns a set $P \subseteq \mathrm{MSF}(H)$ and the graph $H / P$, with isolated vertices removed, in which the number of vertices is at most half the number of vertices of $H$ that have an edge.

*Proof.* Each selected edge is the edge of least key at some vertex, so $P \subseteq \mathrm{MSF}(H)$ by Fact 1; in particular $P$ has no cycle, and the union-find test that skips edges whose ends are already joined skips only repeats of the same edge, chosen from both ends. Every vertex with an edge is incident to a selected edge, so each tree of $P$ that holds such a vertex has at least two vertices, and the contracted graph has at most half as many vertices with edges. Removing isolated vertices does not change any minimum spanning forest. $\square$

By Fact 3, after line L2, $\mathrm{MSF}(G) = C \cup \mathrm{MSF}(G')$, where $C$ is the set of edges chosen in the two steps and $G'$ is the contracted graph.

## The filtering step

Let $H$ be the sample of line L3 and $F = \mathrm{MSF}(H)$, which the recursive call of line L4 returns by induction. For an edge $e = (u, v)$ of $G'$, call $e$ *$F$-heavy* if $u$ and $v$ lie in the same tree of $F$ and the key of $e$ is larger than every key on the path $P_F(u, v)$ in $F$; otherwise $e$ is *$F$-light*. Line L5 keeps exactly the $F$-light edges; call this graph $G''$.

**Lemma 2.** $\mathrm{MSF}(G'') = \mathrm{MSF}(G')$.

*Proof.* $F$ is a set of edges of $G'$, since $H \subseteq G'$. An $F$-heavy edge $e$ closes, with the path $P_F(u, v)$, a cycle of $G'$ on which it has the largest key, so by Fact 2 it is not in $\mathrm{MSF}(G')$. Deleting all $F$-heavy edges one at a time, each still closes the same cycle with $F$, since no edge of $F$ is ever deleted (an edge of $F$ has a key equal to the maximum of its own one-edge path, so it is $F$-light). By Fact 2, applied at each deletion, the minimum spanning forest does not change. $\square$

## The theorem

**Theorem.** On every sequence of coin flips, KKT stops and returns $\mathrm{MSF}(G)$.

*Proof.* By induction on the number $N$ of vertices that have an edge.

*Termination.* If the graph has no edge, line L1 returns. Otherwise the first Borůvka step makes $N$ at least halve (Lemma 1), so $G'$ has $N' \le N/2 < N$ vertices with edges, and so do the sample $H$ and the filtered graph $G''$, which are subgraphs of $G'$ on its vertex set. So both recursive calls are on graphs with fewer than $N$ vertices with edges, and the recursion ends.

*Correctness.* If line L1 or the early return inside line L2 ends the call, the answer is $\emptyset$, or $C$ with no edge left, which is $\mathrm{MSF}(G)$ by Fact 3. Otherwise, by the induction hypothesis, line L4 returns $F = \mathrm{MSF}(H)$ and line L6 returns $\mathrm{MSF}(G'')$. By Lemma 2 this is $\mathrm{MSF}(G')$, and line L6 returns $C \cup \mathrm{MSF}(G') = \mathrm{MSF}(G)$ by Fact 3. Nothing depended on which edges were sampled. $\blacksquare$

**Ties.** The order by (weight, index) makes keys distinct, so the answer is the same on every run. For the weights alone it is one of the minimum spanning forests, and an edge of the same weight as a path maximum is kept, which is safe: Lemma 2 deletes only edges strictly heavier in the key order.
