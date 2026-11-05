---
title: The Fredman-Tarjan algorithm returns a minimum spanning forest and stops after few phases
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a finite undirected graph with $n$ vertices and a real weight $w(e)$ on each edge. Parallel edges and self-loops are allowed, weights may tie, and $G$ need not be connected. Order the edges by the pair $(w(e), \text{index of } e)$. This is a strict total order that refines the order by weight, so a spanning forest that is minimum for this order is a minimum spanning forest (MSF) for $w$. With all keys distinct, the MSF for the order is unique; call it $F^*$.

We prove that the algorithm (lines L1 to L11 of the page) stops, and that the set $F$ it returns is $F^*$.

## Facts used

**Fact 1 (the cut property for distinct keys).** If $S$ is a set of vertices and $e$ is the edge of least key with exactly one end in $S$, then $e \in F^*$. This is the [cut property](/cut-property/) for a strict order.

**Fact 2 (what a contracted vertex is).** At the start of each phase, every vertex of the current graph $H$ stands for a set of vertices of $G$, and these sets partition the vertices that still have edges. Every edge of $H$ stands for one edge of $G$ whose ends lie in two different sets, and it is the edge of least key among all edges of $G$ between those two sets. Every edge of $G$ with both ends in one set is a loop of $H$ and has been removed.

*Proof of Fact 2.* By induction on the phases. At the start, the sets are single vertices, and line L10 (the same cleaning step, applied to the input) removes loops and keeps the least key among parallel edges. At the end of a phase, line L10 replaces each vertex of $H$ by the tree of this phase that holds it and merges their sets. An edge of $G$ between two new sets was, by induction, represented by an edge of $H$ between two old sets in different trees, or was dominated by such an edge with a smaller key; so keeping the least key over the parallel edges of $H$ keeps the least key over all edges of $G$ between the two new sets. $\square$

## Invariant

**Invariant I.** At every moment, $F \subseteq F^*$, and for every vertex $x$ of the current graph, the edges of $F$ inside the set of $x$ form a spanning tree of that set.

**Lemma 1 (each added edge is in $F^*$).** Suppose line L6 extracts $u$ and adds the edge $e$ while the tree $T$ is growing. Let $S \subseteq V$ be the union of the sets of the vertices of $T$. Then $e$ is the edge of least key of $G$ with exactly one end in $S$, so $e \in F^*$.

*Proof.* The heap holds every vertex $x \notin T$ of $H$ that has an edge to $T$, with the least key among the edges of $H$ from $T$ to $x$: line L4 inserts the neighbours of $v_0$, and line L8 inserts or lowers each neighbour of each new vertex, which is the usual invariant of [Prim's algorithm](/prim/), here maintained by a [Fibonacci heap](/fibonacci-heap/). So the minimum of the heap is the edge of least key of $H$ with one end in $T$. By Fact 2, the edges of $G$ with exactly one end in $S$ are the edges between the set of a vertex of $T$ and the set of a vertex outside $T$, and the least key among them is carried by an edge of $H$. So $e$ is the edge of least key of $G$ that leaves $S$, and Fact 1 gives $e \in F^*$. $\square$

Lemma 1 holds whether $u$ belongs to an earlier tree of the phase or not, and it does not depend on the heap limit $k$. Since every edge added is in $F^*$, which is a forest, no edge added closes a cycle with $F$. When $u$ is new, $e$ joins $u$ to $T$; when $u$ is in an earlier tree $T_0$, $e$ joins $T$ to $T_0$, and $T$ takes the label of $T_0$ at line L7. So, at the end of the phase, the vertices with one label are joined by the edges added in the phase, and together with the edges inside each old set they form a spanning tree of the new set. This keeps Invariant I through line L10.

## Termination

**Lemma 2.** Every phase lowers the number of vertices that have edges by at least half.

*Proof.* Each tree starts at a vertex $v_0$ with an edge, so its heap is not empty, and the loop at line L5 runs at least once: the tree adds at least one edge before any stop. Either the first extracted vertex is new, and the tree has at least two vertices, or it belongs to an earlier tree, and $v_0$ joins that tree. Either way, every label that holds a vertex with edges holds at least two vertices of $H$. $\square$

So the number of phases is at most $\log_2 n + 1$, and the algorithm stops.

## The result

**Theorem.** The algorithm returns $F^*$, a minimum spanning forest of $G$.

*Proof.* When the loop at line L1 stops, the current graph has no edges. By Fact 2, no edge of $G$ joins two different sets, so each set is a whole connected component of $G$, or a single vertex with no edges. By Invariant I, $F$ has a spanning tree of each set and $F \subseteq F^*$. So $F$ is a spanning forest of $G$ inside the spanning forest $F^*$; both have $n - c$ edges, where $c$ is the number of components, so $F = F^*$. $\blacksquare$

## The bound on the number of phases

This part is about the running time, not about correctness. Let $m$ be the number of edges after the first cleaning, and let phase $i$ start with $t_i$ vertices and use the limit $k_i = 2^{2m/t_i}$.

**Lemma 3.** After phase $i$, at most $2m / k_i$ labels hold a vertex that still has edges.

*Proof.* Take such a label, and its first tree $T$ of the phase. $T$ did not join an earlier tree, so it stopped because its heap was empty or held more than $k_i$ vertices. If the heap was empty, every edge at $T$ had its other end in $T$, so $T$ is a whole component of $H$, and after line L10 it has no edges, which is excluded. So the heap held more than $k_i$ distinct vertices, each joined to $T$ by its own edge of $H$. These edges have an end in the label's set; each edge of $H$ has two ends, so the labels of this kind number less than $2m / k_i$. $\square$

So $t_{i+1} \le 2m / k_i$ (after dropping the vertices without edges), and $k_{i+1} = 2^{2m/t_{i+1}} \ge 2^{k_i}$. Starting from $k_1 = 2^{2m/n} \ge 2^{m/n}$, an induction gives $\log^{(i-1)} k_i \ge m/n$ for every phase $i$ that is reached. A phase with $k_i \ge t_i$ is the last one: no heap can hold more than $k_i$ vertices, so every tree grows to a whole component. Since $t_i \le n$, this happens as soon as $k_i \ge n$, and that holds once $\log^{(i-1)} n \le m/n$. Hence the number of phases is at most $\beta(m, n) + 1$, where $\beta(m, n) = \min\{i : \log^{(i)} n \le m/n\}$, which is at most $\log^* n$.
