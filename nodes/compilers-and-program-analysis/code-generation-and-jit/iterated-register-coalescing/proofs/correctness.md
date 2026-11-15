---
title: The Briggs and George tests are safe, and iterated register coalescing gives a correct program and stops
proves: [correctness, termination]
status: full
---

We prove the safety of the two coalescing tests on a fixed graph (Lemmas 1 and 2), then four facts about IRC-ALLOCATE: one round stops (Lemma 3), select is proper (Lemma 4), a graph with an empty $k$-core is never spilled (Lemma 5), and the output is correct (Lemma 6). Lemma 7 shows that the outer loop stops.

## Graphs and merges

$G = (V, E)$ is a finite simple graph and $k \ge 1$. $N(x)$ is the set of neighbors of $x$, and $\deg(x) = |N(x)|$. For $U \subseteq V$, $G[U]$ is the induced subgraph and $G - U = G[V \setminus U]$. For two vertices $u \ne v$ that are not adjacent, the *merge* $G'$ replaces $u$ and $v$ by one new vertex $w$ with $N_{G'}(w) = N(u) \cup N(v)$; all other edges stay.

The *$k$-core* of $G$ is the largest induced subgraph whose vertices all have degree at least $k$ in it. It exists because the union of two such vertex sets is again such a set, and it is empty exactly when every nonempty induced subgraph has a vertex of degree less than $k$. Chaitin's allocator colors $G$ with no spill exactly when the $k$-core is empty (Lemma 3 of the proof file of [Chaitin's allocator](/chaitin-register-allocation/)).

We use the simplify rule (Lemma 1 there): if $\deg(x) < k$, then $G$ is $k$-colorable if and only if $G - \{x\}$ is. Applied to a set $L$ of vertices removed one at a time, it needs each vertex to have degree less than $k$ only at its turn. Removing vertices never raises a degree, so it is enough that each vertex of $L$ has degree less than $k$ in $G$. Then $G$ is $k$-colorable if and only if $G - L$ is.

Also, an induced subgraph of a graph with an empty $k$-core has an empty $k$-core, because a $k$-core of the subgraph would be an induced subgraph of the larger graph with all degrees at least $k$.

**Lemma 1 (Briggs test).** Let $u, v$ be non-adjacent vertices of $G$, let $G'$ be the merge, and suppose that fewer than $k$ neighbors of $w$ have degree at least $k$ in $G'$. Then:

1. if $G$ is $k$-colorable, so is $G'$;
2. if $G$ has an empty $k$-core, so has $G'$.

*Proof.* (1) Let $L$ be the set of neighbors of $w$ with degree less than $k$ in $G'$, and $H$ the set of the other neighbors, so $|H| < k$. By the simplify rule, $G'$ is $k$-colorable if and only if $G' - L$ is. In $G' - L$, the neighbors of $w$ are those in $H$, fewer than $k$, so by the simplify rule again, $G' - L$ is $k$-colorable if and only if $G' - L - \{w\}$ is. That graph is $G - (L \cup \{u, v\})$, an induced subgraph of $G$, and it is $k$-colorable because $G$ is.

(2) Suppose $G'$ has a nonempty $k$-core, with vertex set $K$. If $w \notin K$, then $G'[K] = G[K]$, which has all degrees at least $k$, so the $k$-core of $G$ is not empty. If $w \in K$, then $w$ has at least $k$ neighbors in $K$. Each of them has degree at least $k$ in $G'[K]$, so also in $G'$. These are $k$ neighbors of $w$ with degree at least $k$ in $G'$, against the test. $\square$

**Lemma 2 (George test).** Let $u, v$ be non-adjacent vertices of $G$ such that every neighbor of $v$ is a neighbor of $u$ or has degree less than $k$ in $G$. Let $G'$ be the merge. Then (1) and (2) of Lemma 1 hold.

*Proof.* Let $L = N(v) \setminus N(u)$. Each $x \in L$ has $\deg_G(x) < k$. In $G'$, the vertex $x$ loses its neighbor $v$ and gains $w$, and it was not adjacent to $u$, so $\deg_{G'}(x) = \deg_G(x) < k$.

(1) By the simplify rule, $G'$ is $k$-colorable if and only if $G' - L$ is. In $G' - L$, the neighbors of $w$ are $(N(u) \cup N(v)) \setminus L = N(u)$, because $N(v) \setminus L \subseteq N(u)$ and $L \cap N(u) = \emptyset$. So $G' - L$ is $G - (L \cup \{v\})$ with $u$ renamed to $w$. It is an induced subgraph of $G$, so it is $k$-colorable.

(2) Suppose $G'$ has a nonempty $k$-core with vertex set $K$. If $w \notin K$, then $G[K] = G'[K]$ is a nonempty induced subgraph of $G$ with all degrees at least $k$. If $w \in K$, each neighbor $x$ of $w$ in $K$ has $\deg_{G'}(x) \ge k$, so $x \notin L$, and so $x \in N(u)$. Let $K_0 = (K \setminus \{w\}) \cup \{u\}$. Map $w$ to $u$ and every other vertex to itself. Each edge of $G'[K]$ that does not touch $w$ is an edge of $G[K_0]$, and each edge $\{w, x\}$ of $G'[K]$ gives the edge $\{u, x\}$ of $G[K_0]$, because $x \in N(u)$. So every vertex of $G[K_0]$ has degree at least its degree in $G'[K]$, which is at least $k$. So the $k$-core of $G$ is not empty. $\square$

**Aggressive merges are not safe.** Take the path $a, x, y, b$ and $k = 2$. It is 2-colorable and has an empty 2-core. Merging $a$ and $b$ gives the triangle $\{a, b\}, x, y$, which is not 2-colorable and is its own 2-core. Both tests refuse this merge: the merged vertex has the two neighbors $x$ and $y$ of degree 2, and $x \notin N(b)$, $y \notin N(a)$, both of degree 2.

## One round

In a round, the vertices of $G$ are sets of names, at first single names. A vertex $X$ is adjacent to $Y$ when a name of $X$ interferes with a name of $Y$. Line L14 merges $u$ and $v$ only if they are not adjacent (line L13), so by induction **no two names of one vertex interfere**. Let $G_t$ be the graph $G$ after $t$ passes of the loop at line L7. Every vertex leaves $G$ either at line L9, as a whole, or at line L14, as part of a larger vertex. A vertex pushed at line L9 never changes after that. So the vertices on the stack at the end are disjoint, and every name is in exactly one of them. Call this set of vertices the *final vertices*, and let $G^*$ be the graph on them with the same adjacency rule. Line L22 uses adjacency in $G^*$.

**Lemma 3 (one round stops).** The loop at line L7 stops after a finite number of passes.

*Proof.* When the conditions of lines L8 and L16 fail, every vertex of $G_t$ has degree at least $k \ge 1$: a vertex of degree less than $k$ is either not move-related or move-related. So line L19 always finds a vertex with a positive degree. Also, when line L19 runs there is no spill candidate in $G_t$, because line L8 would apply to it first.

Let $V_t$ be the number of vertices of $G_t$, $D_t$ the number of live copies, $N_t$ the number of vertices that are not spill candidates, and $W_t$ the size of $W$. Each pass lowers the tuple $(V_t, D_t, N_t, W_t)$ in the lexicographic order. Line L9 and line L14 lower $V_t$. Lines L12 and L13 do not change $V_t$ and lower $D_t$. Line L17 lowers $D_t$, because $v$ is move-related. Line L19 keeps $V_t$, does not raise $D_t$, and lowers $N_t$. Line L15 keeps the first three and lowers $W_t$: a copy goes back to $W$ only when a degree drops or after a merge, and both happen only at lines L9 and L14. So the loop stops. $\square$

**Lemma 4 (select).** Every vertex pushed at line L9 that is not a spill candidate gets a color at line L23. At the end of select, the colors form a $k$-coloring of the colored final vertices in $G^*$.

*Proof.* Let $X$ be pushed at pass $t$, not as a spill candidate, so line L8 gave $\deg_{G_t}(X) < k$. Line L21 visits the stack from the top down, so when it reaches $X$, the colored vertices were all pushed after $X$. Let $Q$ be such a vertex that is adjacent to $X$ in $G^*$, by names $x \in X$ and $y \in Q$ that interfere. At pass $t$, the name $y$ is in some vertex $Y$ of $G_t$: it was not pushed yet, since $Q$ is pushed later and $Y \subseteq Q$. So $Y$ is a neighbor of $X$ in $G_t$. Distinct vertices $Q$ come from distinct vertices $Y$, because the final vertices are disjoint. So fewer than $k$ colored vertices are adjacent to $X$, they use fewer than $k$ colors, and line L22 finds a free color.

Line L23 uses only colors in $\{0, \ldots, k-1\}$. For an edge of $G^*$ between two colored vertices, the one colored second avoided the color of the other at line L22, and colors never change. $\square$

**Lemma 5 (no spill on easy graphs).** Let TEST be the Briggs test, the George test, or both. If the interference graph built at line L4 has an empty $k$-core, the round never runs line L19 and ends with an empty set *spill*.

*Proof.* We show by induction on $t$ that $G_t$ has an empty $k$-core. It holds for $t = 0$. Line L9 removes a vertex, which gives an induced subgraph. Line L14 merges two non-adjacent vertices that pass TEST in $G_t$, so Lemma 1 or Lemma 2 applies. The other lines do not change the graph.

Suppose line L19 runs at pass $t$. As in the proof of Lemma 3, every vertex of $G_t$ has degree at least $k$, and $G_t$ is not empty. So $G_t$ is its own nonempty $k$-core, a contradiction. So there is no spill candidate, and by Lemma 4 every vertex gets a color. $\square$

With aggressive coalescing, Lemma 5 fails: the second program of the example has an empty 2-core, and aggressive coalescing spills $y$.

## The output is correct

The program model, the liveness rule and the renaming and spill lemmas are those of the proof file of [Chaitin's allocator](/chaitin-register-allocation/) (its Lemmas 4 and 5). The renaming lemma needs only a $k$-coloring of the interference graph of the program. The spill lemma holds for any set of spilled names.

**Lemma 6 (correct output).** If IRC-ALLOCATE returns, its result uses only the registers $r_0, \ldots, r_{k-1}$ and the memory slots, and it has the same outcome as $P$ on every input.

*Proof.* Line L26 runs only when *spill* is empty, so every final vertex has a color by Lemma 4. Let $c(x)$ be the color of the final vertex of the name $x$. For an interference edge $\{x, y\}$, the names $x$ and $y$ are in different final vertices, because no two names of one vertex interfere, and these vertices are adjacent in $G^*$. By Lemma 4 they have different colors. So $c$ is a $k$-coloring of the interference graph, and line L26 keeps the outcome by the renaming lemma. A copy whose two names are in one vertex becomes `r = r` and is deleted. Line L27 keeps the outcome by the spill lemma, and line L1 keeps it because it only moves the parameters through their slots. $\square$

## Termination

Call the non-slot names of the program after line L1 the *original names*, and the names made by line L27 the *temporaries*. A vertex is *original* if it holds an original name. Its cost is finite: it is the sum of the finite costs of its names. A vertex that holds only temporaries has an infinite cost.

The parameter loads that line L1 puts in the entry block are the only loads that write original names. A *load temporary* is a temporary whose write is a load and whose only read is the first instruction after the write that is not a load. A *store temporary* is a temporary whose only read is a store just after its write. We prove four statements together, by induction on the rounds.

- **(T) Shape.** Each temporary is written once and is a load temporary or a store temporary, and no load temporary is in the entry block.
- **(M) Moves.** A temporary is move-related only if it is a load temporary read by a copy, or a store temporary written by a copy. Such a temporary has no temporary neighbor in the interference graph.
- **(V) Few edges.** In $G_t$, a vertex that holds only temporaries has at most one neighbor that holds only temporaries.
- **(O) Original spills.** Each time line L19 runs, it chooses an original vertex.

**(T) implies (M).** A load or a store copies between a name and a slot, so it is not a copy in $W$. So a move-related temporary is read by a copy (then it is not a store temporary, which is read by a store) or written by a copy (then it is not a load temporary, which is written by a load). Now take an interference edge between two temporaries. It is made at the write of one of them, $t$, with the other, $u$, live just after. If $u$ is a store temporary, it is live only between its write and its store, so the write of $t$ is the write of $u$ and $t = u$, which is not an edge. So $u$ is a load temporary, live from its load to its reader $j$. Every instruction in that stretch before $j$ is a load, and none of them is in the entry block. So $t$ is written by a load that is followed only by loads up to $j$. If $t$ were a store temporary, its store would come right after its write and before $j$, and a store is not a load. So $t$ is a load temporary with the reader $j$ too. Then $j$ reads two different names $t$ and $u$, so $j$ is an `op`, not a copy, and neither $t$ nor $u$ is move-related.

**(M) and (T) imply (V).** Merges at line L14 follow copies, so a vertex of two or more names that holds only temporaries holds only move-related temporaries, and by (M) none of them has a temporary neighbor. So that vertex has no neighbor that holds only temporaries. A vertex of one temporary $t$ has at most as many such neighbors as $t$ has temporary neighbors. By the proof of (M), these are load temporaries with the same reader as $t$, and that reader reads at most two names, so there is at most one.

**(V) implies (O).** When line L19 runs, every vertex of $G_t$ has degree at least $k \ge 2$ (proof of Lemma 3). If no vertex of $G_t$ were original, each would have degree at most 1 by (V). So some vertex is original. Its cost is finite and its degree is positive, so its ratio is finite, while every vertex of only temporaries has ratio infinity. So line L19 chooses an original vertex.

**(O) implies (T) in the next round.** By Lemma 4 and (O), each vertex in *spill* is original. Line L27 spills all names of these vertices. Such a name is original, or it is a temporary in an original vertex, which is move-related because merges follow copies. The new temporaries have the two shapes: the loads before a reader $j$ are placed just before $j$, and the temporary of a definition is followed by its store. No new load is in the entry block: the instructions there read only slots and store temporaries of parameters, and a store temporary written by a load is not move-related, so it is never spilled. For an old temporary that is not spilled:

- if it is a store temporary, line L27 puts nothing between its write and its store, because its write defines no spilled name and its store reads no spilled name;
- if it is a load temporary $t$ with reader $j$, line L27 adds loads just before $j$, which keeps the shape. It adds a store between the load of $t$ and $j$ only after a load there that writes a spilled temporary $u$. By (T), $u$ is a load temporary with reader $j$, and it is move-related, so by (M) $j$ is a copy. But $j$ reads both $t$ and $u$, and a copy reads one name. So this does not happen.

**Lemma 7 (termination).** Let $n_0$ be the number of original names. IRC-ALLOCATE with $k \ge 2$ returns after at most $n_0 + 1$ rounds.

*Proof.* Each round stops by Lemma 3. A round that does not return has a nonempty set *spill*, and each of its vertices is original by Lemma 4 and (O). Line L27 replaces every occurrence of the spilled names by new temporaries, and later rounds make only temporaries, so a spilled original name never appears again. So each round that does not return removes at least one of the $n_0$ original names for good, and at most $n_0$ rounds do not return. $\square$

Together, Lemmas 3, 6 and 7 show that IRC-ALLOCATE stops with a correct program that uses $k$ registers. Lemmas 1, 2 and 5 show that conservative coalescing never makes a $k$-colorable graph uncolorable, and never causes a spill on a graph that Chaitin's allocator colors.
