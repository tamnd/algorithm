---
title: Chaitin's allocator gives a correct program with k registers and stops
proves: [correctness, termination]
status: full
---

We prove six facts about CHAITIN-ALLOCATE. Lemmas 1 to 3 are about one round on a graph. Lemmas 4 and 5 show that renaming and spill code keep the outcome of every run. Lemma 6 shows that the loop stops.

Throughout, $G = (V, E)$ is a finite simple graph and $k \ge 1$. For $U \subseteq V$, $G[U]$ is the subgraph induced by $U$, and $G - v = G[V \setminus \{v\}]$. A *$k$-coloring* is a map $c: V \to \{0, \ldots, k-1\}$ with $c(x) \ne c(y)$ for every edge $\{x, y\}$.

## One round on the graph

**Lemma 1 (simplify rule).** If $\deg_G(v) < k$, then $G$ has a $k$-coloring if and only if $G - v$ has one.

*Proof.* If $c$ is a $k$-coloring of $G$, its restriction to $V \setminus \{v\}$ is a $k$-coloring of $G - v$. Conversely, let $c'$ be a $k$-coloring of $G - v$. The neighbors of $v$ use at most $\deg_G(v) < k$ colors, so some color $j \in \{0, \ldots, k-1\}$ is used by no neighbor of $v$. Set $c(v) = j$ and $c(x) = c'(x)$ for $x \ne v$. Each edge at $v$ joins $v$ to a neighbor of another color, and each other edge is an edge of $G - v$, so $c$ is a $k$-coloring of $G$. $\square$

**Lemma 2 (select).** If a round ends with an empty set *spill*, then line L15 gives each vertex a color in $\{0, \ldots, k-1\}$, and the result is a $k$-coloring of $G$.

*Proof.* With no spill, every vertex was pushed at line L9. Let $v_1, \ldots, v_n$ be the push order and $G_i = G[\{v_i, \ldots, v_n\}]$, the graph just before $v_i$ was removed. Line L8 gives $\deg_{G_i}(v_i) < k$. Line L14 visits $v_n, v_{n-1}, \ldots, v_1$. When it reaches $v_i$, the colored vertices are exactly $v_{i+1}, \ldots, v_n$, so the colored neighbors of $v_i$ are its neighbors in $G_i$. There are fewer than $k$ of them, so they use fewer than $k$ colors, and line L15 finds a color below $k$. For an edge $\{v_i, v_j\}$ with $i < j$, the vertex $v_j$ is colored first, and line L15 gives $v_i$ a color different from $c(v_j)$. So no edge has two equal colors. $\square$

Lemma 2 is the step-by-step form of Lemma 1: the vertices go back in the reverse order, and each one finds a free color.

The *$k$-core* of $G$ is $C = G[K]$, where $K$ is the union of all sets $U \subseteq V$ such that every vertex of $G[U]$ has degree at least $k$ in $G[U]$. If every vertex of $G[U_1]$ and of $G[U_2]$ has degree at least $k$, then so does every vertex of $G[U_1 \cup U_2]$, because adding vertices never lowers a degree. So $C$ itself has minimum degree at least $k$ when it is not empty, and it contains every induced subgraph with that property.

**Lemma 3 (when a round spills).** A round chooses a spill at line L12 if and only if the $k$-core of $G$ is not empty.

*Proof.* Suppose $K \ne \emptyset$. The loop of line L7 removes every vertex, so it removes some vertex of $K$; let $v$ be the first one. When $v$ is removed, all of $K$ is still in the graph, so $v$ has degree at least $\deg_C(v) \ge k$. Line L8 does not apply to $v$, and line L11 removes $v$ only if line L8 applies to no vertex at all. So $v$ is removed at line L12, and the round spills.

Suppose the round spills, and look at the first time line L12 runs. Let $U$ be the set of vertices still in the graph then. Line L8 did not apply, so every vertex of $G[U]$ has degree at least $k$ in $G[U]$, and $U \ne \emptyset$. So $U \subseteq K$ and the $k$-core is not empty. $\square$

So a round colors $G$ with no spill exactly when $G$ has degeneracy less than $k$: every nonempty induced subgraph has a vertex of degree less than $k$. A $k$-colorable graph with a nonempty $k$-core, such as the cycle of length 4 for $k = 2$, is spilled.

## Renaming and spill code keep the outcome

A program here is a toy IR program with `const`, `copy` and `op` instructions. Its names are of two kinds: the memory slots, whose names start with `mem.`, and the other names, which are the vertices of the interference graph. We assume that no run of the program reads a name before it writes it; the toy IR interpreter stops with an error otherwise. Line L1 makes this true for the parameters: it reads each live parameter from its slot at the start, and the new program has the slots as its parameters.

The outcome of a run is its return value, a trap, or no end. Two runs *correspond* when they visit the same blocks in the same order and run the same instructions there, apart from instructions that one of them adds or deletes as stated.

We use one fact about liveness. Let instruction $i$ define $x$ and read the names in $\mathrm{use}(i)$. Then the names live just before $i$ are $\mathrm{use}(i) \cup (\mathrm{out}(i) \setminus \{x\})$, where $\mathrm{out}(i)$ is the set live just after $i$. At the end of a block $B$, the names live before the terminator are $\mathrm{liveout}(B)$ plus the name the terminator reads, and $\mathrm{liveout}(B)$ contains the live-in set of each successor.

**Lemma 4 (renaming).** Let $Q$ be a program with interference graph $G$, and let $c$ be a $k$-coloring of $G$. Let $Q'$ be $Q$ with each non-slot name $x$ renamed to $r_{c(x)}$ and each copy that becomes `r = r` deleted. Then for every input, $Q$ and $Q'$ have the same outcome.

*Proof.* Run $Q$ and $Q'$ on the same input. Write $\sigma$ and $\sigma'$ for their stores. We show that the runs correspond, with $Q'$ skipping the deleted copies, and that this invariant holds at every point between two instructions:

> **(R)** For each non-slot name $x$ that is live at the point and has been written on the run, $\sigma'(r_{c(x)}) = \sigma(x)$. For each slot $m$, $\sigma'(m) = \sigma(m)$.

At the start, no non-slot name has been written, and both programs got the same arguments in the same slots. So (R) holds.

Take an instruction $i$ that defines $x$, with (R) true just before it. Each non-slot operand $a$ is in $\mathrm{use}(i)$, so it is live just before $i$, and it has been written by our assumption. By (R), the register of $a$ in $Q'$ holds $\sigma(a)$, and slot operands agree too. So both programs compute the same value $w$, or both trap on the same operands. After the step, $\sigma(x) = w$. We check (R) just after $i$.

- If $x$ is a slot (a store), $Q'$ writes $w$ to the same slot, and no register changes.
- If $i$ is a deleted copy `x = a` with $c(x) = c(a)$, the register $r_{c(x)}$ already holds $\sigma(a) = w$.
- Otherwise $Q'$ writes $w$ to $r_{c(x)}$, so the claim holds for $x$.

Now let $y \ne x$ be a non-slot name in $\mathrm{out}(i)$ that has been written. Then $y$ was live just before $i$ and $\sigma(y)$ did not change, so before the step $\sigma'(r_{c(y)}) = \sigma(y)$. If $c(y) \ne c(x)$, the step did not touch $r_{c(y)}$. If $c(y) = c(x)$, then $\{x, y\}$ is not an edge of $G$. Since $y \in \mathrm{out}(i)$ and $y \ne x$, the definition rule of the interference graph adds this edge unless $i$ is the copy `x = y`. So $i$ is that copy, and the value written to $r_{c(x)} = r_{c(y)}$ is $\sigma(y)$ itself. In each case $\sigma'(r_{c(y)}) = \sigma(y)$ after the step.

A terminator reads a name that is live before it, so by (R) both programs take the same branch or return the same value. The names live at the start of the next block are live before the terminator, so (R) holds there. By induction over the steps of the run, the runs correspond, and they end in the same way: with the same return value, with the same trap, or not at all. $\square$

**Lemma 5 (spill everywhere).** Let $S$ be a set of non-slot names of $Q$, and let $Q_2$ be the result of line L17: for each $x \in S$, each instruction that reads $x$ is preceded by a load `t = mem.x` into a new name $t$ and reads $t$ instead, and each instruction that defines $x$ defines a new name $t$ instead and is followed by the store `mem.x = t`. Then $Q$ and $Q_2$ have the same outcome on every input, and $Q_2$ reads no name before it writes it.

*Proof.* The new names appear nowhere else, so the other names keep their meaning. For $x \in S$, $Q$ never writes `mem.x` itself: a slot of a non-slot name is written only by a store added when that name is spilled, and a spilled name no longer occurs in the program. $Q$ may read `mem.x` only in the entry block, when $x$ is a parameter loaded there. We show that the runs correspond, $Q_2$ running the added loads and stores, with this invariant at the points of $Q$:

> **(S)** For each non-slot name $y \notin S$ written so far, $\sigma_2(y) = \sigma(y)$. For each $x \in S$ written so far, $\sigma_2(\mathtt{mem.}x) = \sigma(x)$. Each slot that no added store has written so far has the same value in both runs.

It holds at the start. Take an instruction $i$ of $Q$. For each operand $x \in S$, the name $x$ was written before $i$ on this run, so the added load reads $\sigma_2(\mathtt{mem.}x) = \sigma(x)$. The other operands agree by (S). So $Q_2$ computes the same value $w$, or traps in the same way. If $i$ defines $y \notin S$, then $\sigma_2(y) = w$. If $i$ defines $x \in S$, the new name gets $w$ and the store sets $\mathtt{mem.}x$ to $w = \sigma(x)$. Terminators are handled in the same way. Each new name is written just before its only read, so $Q_2$ reads nothing before it writes it. $\square$

By Lemmas 4 and 5, every program that CHAITIN-ALLOCATE returns has the outcome of the program after line L1, and line L1 keeps the outcome because it only moves the parameters through their slots. The returned program uses only the registers $r_0, \ldots, r_{k-1}$ by Lemma 2.

## Termination

Call the non-slot names of the program after line L1 the *original names*, and the names made by line L17 the *temporaries*.

The only loads that write original names are the parameter loads of the entry block made by line L1. The instructions of that block read only slots and, after a parameter is spilled, the store temporary of that parameter. By (O) below for the earlier rounds, temporaries are never spilled, so line L17 never adds a load in that block.

We prove three statements together, by induction on the rounds.

- **(T) Shape.** Each temporary $t$ is written once and read once. Either $t$ is a *load temporary*: its write is a load, and its read is the first instruction after the write that is not a load. Or $t$ is a *store temporary*: its read is the store just after its write.
- **(U) Few temporary edges.** In the interference graph of the round, each temporary has at most one neighbor that is a temporary.
- **(O) Original spills.** Each time line L11 runs, it chooses an original name.

**(T) holds in round 1**, which has no temporary, and it carries over from a round to the next if (O) holds in that round. Line L17 creates temporaries of the two shapes. By (O) it spills only original names. It adds loads just before an instruction $j$ that reads a spilled name; $j$ is not a store of a temporary, which reads only a temporary, and not a load, which reads only a slot. If $j$ is the reader of an old load temporary, only loads now lie between that temporary's write and $j$, so its shape holds. Line L17 adds stores just after an instruction that writes a spilled original name; that instruction is not the write of an old temporary, so no old store temporary is separated from its store.

**(T) implies (U) in the same round.** An edge between temporaries $t$ and $u$ needs, say, $u$ live just after the write of $t$. If $u$ is a store temporary, it is live only just after its own write, so $t = u$, which is not an edge. If $u$ is a load temporary, it is live from just after its load to its reader $j$, and dead after $j$. The writes inside that stretch are loads, and none of them is in the entry block. So $t$ is a load temporary whose first following instruction that is not a load is also $j$: $t$ and $u$ have the same reader. An instruction reads at most two names, and each spilled name read by it gets one load, so at most two load temporaries share a reader. So each temporary has at most one temporary neighbor.

**(U) implies (O) in the same round.** When line L11 runs, every vertex left has degree at least $k \ge 2$ in the current graph. If all of them were temporaries, the current graph would be induced by temporaries, and by (U) each of its vertices would have degree at most 1. So some original name is left. Its cost is finite and its degree is positive, so its ratio is finite, while every temporary has ratio infinity. So line L11 chooses an original name.

**Lemma 6 (termination).** Let $n_0$ be the number of original names. CHAITIN-ALLOCATE with $k \ge 2$ returns after at most $n_0 + 1$ rounds.

*Proof.* By (O), each round that spills spills at least one original name, because line L12 runs only after line L11. Line L17 replaces every occurrence of a spilled name by temporaries, and later rounds create only temporaries, so a spilled original name never appears again and is never spilled again. There are $n_0$ original names, so at most $n_0$ rounds spill, and the next round returns. $\square$

Together, Lemmas 2, 4, 5 and 6 prove that CHAITIN-ALLOCATE stops and returns a program that uses only $k$ registers and has the same outcome as its input on every input. Lemma 3 tells exactly when a round spills.
