---
title: Optimistic coloring gives a correct program, spills only where Chaitin's allocator spills, and stops
proves: [correctness, termination]
status: full
---

We prove five facts about BRIGGS-ALLOCATE. Lemmas 1 and 2 are about select. Lemma 3 compares one round with one round of Chaitin's allocator on the same graph. Lemma 4 shows that the output keeps the outcome, and Lemma 5 shows that the loop stops.

Throughout, $G = (V, E)$ is a finite simple graph and $k \ge 1$. For $U \subseteq V$, $G[U]$ is the subgraph induced by $U$. A *$k$-coloring* of a set $W \subseteq V$ is a map $c: W \to \{0, \ldots, k-1\}$ with $c(x) \ne c(y)$ for every edge $\{x, y\}$ with $x, y \in W$. Let $v_1, \ldots, v_n$ be the order in which lines L7 to L12 push the vertices, and let $G_i = G[\{v_i, \ldots, v_n\}]$ be the graph just before $v_i$ is removed. Call $v_i$ a *low* vertex if line L9 pushed it and a *candidate* if line L12 pushed it.

## Select

**Lemma 1 (low vertices get a color).** Line L15 finds a free color for every low vertex. So the set *spill* contains only candidates.

*Proof.* Line L14 visits $v_n, v_{n-1}, \ldots, v_1$. When it reaches $v_i$, the vertices that have a color are among $v_{i+1}, \ldots, v_n$, so each colored neighbor of $v_i$ is a neighbor of $v_i$ in $G_i$. If $v_i$ is low, line L8 gives $\deg_{G_i}(v_i) < k$. So fewer than $k$ neighbors of $v_i$ have a color, they use fewer than $k$ of the $k$ colors, and line L15 finds a free one. $\square$

**Lemma 2 (proper coloring).** At the end of select, the map *color* is a $k$-coloring of the set of colored vertices. If *spill* is empty, it is a $k$-coloring of $G$.

*Proof.* Line L16 gives only colors in $\{0, \ldots, k-1\}$. Let $\{x, y\}$ be an edge with both ends colored, and say line L14 colored $y$ first. When it reached $x$, the color of $y$ was used by a colored neighbor of $x$, so line L16 gave $x$ another color. Colors never change after line L16, so the edge has two different colors. If *spill* is empty, every vertex is colored. $\square$

## Comparison with Chaitin's allocator

**Lemma 3 (subset of Chaitin's spills).** Run one round of Chaitin's allocator and one round of BRIGGS-ALLOCATE on the same graph $G$ with the same costs, the same $k$ and the same order of the names. Then:

1. both simplify phases push the same vertices in the same order, and the candidates of BRIGGS-ALLOCATE are exactly the vertices that Chaitin's allocator puts in its set *spill*;
2. the set *spill* of BRIGGS-ALLOCATE is a subset of the set *spill* of Chaitin's allocator;
3. if Chaitin's allocator spills nothing, BRIGGS-ALLOCATE spills nothing and gives the same colors.

*Proof.* (1) Lines L7 to L11 are the same in both allocators. Each loop pass removes one vertex $v$ from the current graph, and it chooses $v$ from the current graph, the degrees in it, the costs and the order of the names. Chaitin's allocator adds $v$ to its set *spill* at line L12 and BRIGGS-ALLOCATE pushes it as a candidate, but in both the graph after the pass is the current graph minus $v$. So, by induction on the passes, the two loops see the same graphs and choose the same vertices, and the vertices chosen at line L11 are the same.

(2) By Lemma 1, the set *spill* of BRIGGS-ALLOCATE contains only candidates, and by (1) those are the vertices that Chaitin's allocator spills.

(3) If Chaitin's allocator spills nothing, then by (1) there is no candidate, and by (2) *spill* is empty in BRIGGS-ALLOCATE. Both allocators then color the same stack, in the same order, with the least free color. So they give the same colors. $\square$

Part 3 is the claim that optimistic coloring colors every graph that Chaitin's allocator colors. The inclusion in part 2 can be strict. On the cycle $a, b, c, d$ with $k = 2$, Chaitin's allocator spills one vertex, while optimistic select finds that the two neighbors of the candidate have the same color and colors it.

**A caution about later rounds.** Lemma 3 compares rounds on the same graph. When both allocators spill, they spill different sets, so their next programs and graphs differ. The lemma does not say that over a full run, BRIGGS-ALLOCATE spills a subset of the names that Chaitin's allocator spills.

## The output keeps the outcome

The program model, the liveness rule and the definition of the interference graph are those of the proof file of [Chaitin's allocator](/chaitin-register-allocation/). Its Lemma 4 (renaming) and Lemma 5 (spill everywhere) speak only about a program, a $k$-coloring of its interference graph and a set of spilled names. They do not use the way the coloring or the set was found. We restate them.

- **Renaming.** If $c$ is a $k$-coloring of the interference graph of $Q$, then renaming each non-slot name $x$ to $r_{c(x)}$ and deleting each copy that becomes `r = r` gives a program with the same outcome as $Q$ on every input. The key step: if $x$ and $y$ get the same register and $y$ is live just after a definition of $x$, then that definition is the copy `x = y`, because otherwise the definition rule gives the edge $\{x, y\}$.
- **Spill everywhere.** Replacing each read of a spilled name $x$ by a load from `mem.x` into a new name just before the reader, and each definition of $x$ by a definition of a new name followed by a store to `mem.x`, gives a program with the same outcome that reads no name before it writes it.

**Lemma 4 (correct output).** If BRIGGS-ALLOCATE returns, the result uses only the registers $r_0, \ldots, r_{k-1}$ and the memory slots, and it has the same outcome as $P$ on every input.

*Proof.* Line L1 keeps the outcome, because it only moves the parameters through their slots. Line L20 keeps it by the spill lemma. The loop returns at line L19 only when *spill* is empty, and then *color* is a $k$-coloring of the graph by Lemma 2. So line L19 keeps the outcome by the renaming lemma, and it uses only the registers $r_0, \ldots, r_{k-1}$. $\square$

## Termination

The termination proof of Chaitin's allocator uses three statements, proved together by induction on the rounds: (T) each temporary is a load temporary, read by the first instruction after its load that is not a load, or a store temporary, read by the store just after it; (U) each temporary has at most one temporary neighbor; (O) each time line L11 runs, it chooses an original name, that is a name of the program after line L1.

The same induction works here, with one change. In Chaitin's allocator, line L17 spills exactly the vertices chosen at line L11. Here, line L20 spills the set *spill*, which by Lemma 1 contains only vertices chosen at line L11. So (O) again gives that line L20 spills only original names, and the step from (O) to (T) in the next round is unchanged. The steps from (T) to (U) and from (U) to (O) do not depend on select at all: they use only the shape of the temporaries, the fact that $k \ge 2$, and the infinite cost of the temporaries set at line L5.

**Lemma 5 (termination).** Let $n_0$ be the number of original names. BRIGGS-ALLOCATE with $k \ge 2$ returns after at most $n_0 + 1$ rounds.

*Proof.* A round that does not return has a nonempty set *spill*, and by Lemma 1 and (O) its vertices are original names. Line L20 replaces every occurrence of these names by temporaries, and later rounds create only temporaries, so a spilled original name never appears again. So each round that does not return removes at least one of the $n_0$ original names for good, and at most $n_0$ rounds do not return. $\square$

Together, Lemmas 4 and 5 prove that BRIGGS-ALLOCATE stops and returns a program that uses only $k$ registers and has the same outcome as its input. Lemma 3 proves that, round by round, it never spills where Chaitin's allocator would not.
