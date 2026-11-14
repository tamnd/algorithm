---
title: The AND/OR graph holds every monotone two-handed plan once, and its nodes are connected subassemblies
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The product has parts $P = \{1, \ldots, n\}$ with $n \ge 1$, a liaison graph $L$, and a test FEASIBLE on splits. A *split* of a set $S$ is an unordered pair $\{S_1, S_2\}$ of nonempty sets with $S_1 \cup S_2 = S$ and $S_1 \cap S_2 = \emptyset$. A split is *admissible* when $S_1$ and $S_2$ are connected in $L$ and FEASIBLE($S_1$, $S_2$) holds. Under the motion model of the page, FEASIBLE holds when one side can leave the other by one translation to infinity along a direction of $M$; the proofs below use only that FEASIBLE is a fixed test on the pair, symmetric in its two arguments.

A *plan* for a set $S$ is a full binary tree whose leaves are the parts of $S$, with unordered children, such that for every internal node $v$ with children $v_1$ and $v_2$, the split $\{\mathrm{leaves}(v_1), \mathrm{leaves}(v_2)\}$ of $\mathrm{leaves}(v)$ is admissible. This is the monotone two-handed model: each step joins two subassemblies that are already finished, and no part moves again inside its subassembly. A *solution tree* below a node $S$ of the graph is $S$ itself when $|S| = 1$, and otherwise a choice of one hyperarc $S \to \{S_1, S_2\}$ together with a solution tree below $S_1$ and one below $S_2$.

**Lemma 1 (each admissible split is one hyperarc).** When line L3 makes a node $S$ with $|S| \ge 2$, lines L5 to L9 add exactly one hyperarc for each admissible split of $S$, and no other hyperarc.

*Proof.* Let $v$ be the lowest part of $S$. Every split $\{S_1, S_2\}$ of $S$ has exactly one side that contains $v$. Name it $S_1$. Then $S_1$ is a connected set with $v \in S_1 \subsetneq S$. Line L6 runs GROW of the [liaison graph](/liaison-graph/) from $\{v\}$ inside $S$, which lists every connected set that contains $v$ and lies inside $S$ exactly once (the proof is on the liaison graph page). So the split comes up exactly once, line L7 forms its other side, and line L8 adds it exactly when $S_2$ is connected and FEASIBLE holds, that is, exactly when the split is admissible. $\square$

**Lemma 2 (nodes).** Every set that DECOMPOSE turns into a node is $P$ or a connected set. Every side of every hyperarc becomes a node.

*Proof.* The stack starts with $P$. A set is pushed on line L9 only as a side of an admissible split, and such a side is connected. Line L2 makes each popped set a node once. $\square$

**Theorem 1 (plans are solution trees).** For each node $S$, the map that sends a solution tree below $S$ to the binary tree of its chosen splits is a bijection onto the plans for $S$.

*Proof.* By induction on $|S|$. If $|S| = 1$ both sides have exactly one element, the leaf. Let $|S| \ge 2$. A solution tree below $S$ chooses a hyperarc $S \to \{S_1, S_2\}$, whose split is admissible by Lemma 1, and solution trees below $S_1$ and $S_2$, which are nodes by Lemma 2. By induction these map to plans for $S_1$ and $S_2$, so the whole maps to a plan for $S$. Conversely, take a plan for $S$. Its root split is admissible, so by Lemma 1 it is exactly one hyperarc of $S$. Its two subtrees are plans for $S_1$ and $S_2$, which by induction come from exactly one solution tree each. So each plan comes from exactly one solution tree. $\square$

In words: the graph holds every monotone two-handed plan in which each intermediate subassembly is connected and each joining step passes FEASIBLE, it holds each such plan once, and it holds nothing else.

**Corollary 1 (counting by recursion).** For a node $S$, the number of plans for $S$ is $\mathrm{PLANS}(S)$ of lines L12 and L13: 1 if $|S| = 1$, and otherwise the sum over the hyperarcs $S \to \{S_1, S_2\}$ of $\mathrm{PLANS}(S_1) \cdot \mathrm{PLANS}(S_2)$.

*Proof.* By Theorem 1 we count solution trees. A solution tree below $S$ is a hyperarc together with an independent choice of a solution tree below each side, and different hyperarcs give different trees. $\square$

**Theorem 2 (size).** Let $N$ be the number of connected nonempty sets of parts. The graph has at most $N$ nodes when $P$ is connected, and at most $N + 1$ otherwise. Each node $S$ has at most $c(S) - 1$ hyperarcs, where $c(S)$ is the number of connected sets inside $S$ that contain the lowest part of $S$.

*Proof.* The first claim is Lemma 2. For the second, Lemma 1 maps each hyperarc of $S$ to its side $S_1$, a connected set inside $S$ that contains the lowest part, with $S_1 \ne S$, and the map is one to one. $\square$

The bounds are reached. If all parts touch each other and every split is feasible, then every one of the $2^n - 1$ nonempty sets is a node, the number of hyperarcs is $\sum_k \binom{n}{k}(2^{k-1} - 1) = (3^n - 2^{n+1} + 1)/2$, and the number of plans is $(2n - 3)!! = 1 \cdot 3 \cdot 5 \cdots (2n - 3)$, because a plan for $n$ parts comes from a plan for $n - 1$ parts in exactly $2n - 3$ ways, by putting the new leaf above one of the $2n - 3$ nodes of the smaller tree. So the number of plans grows like $n!$ times an exponential, while the graph has fewer than $3^n$ nodes and hyperarcs together.

For a chain of $n$ parts in which each split of a contiguous block is feasible, the connected sets are the $n(n+1)/2$ contiguous blocks, a block of $k$ parts has $k - 1$ hyperarcs, so there are $\sum_k (n - k + 1)(k - 1) = \binom{n+1}{3}$ hyperarcs, and the plans are the binary bracketings of $n$ symbols, counted by the Catalan number $C_{n-1}$.

**Termination and cost.** Each set is expanded at most once by line L2, and there are at most $N + 1$ sets, so DECOMPOSE stops. Expanding $S$ lists $c(S)$ sets on line L6 and runs line L8 on each. With bit masks of the blocking sets, the connectivity test costs $O(|S|^2)$ word operations and FEASIBLE costs $O(|M| \cdot |S|)$, so the build costs $O\big(\sum_S c(S)\,(|S|^2 + |M|\,|S|)\big)$ over the nodes $S$. PLANS visits each node and each hyperarc once with memoization, with arithmetic on integers of at most $O(n \log n)$ bits.
