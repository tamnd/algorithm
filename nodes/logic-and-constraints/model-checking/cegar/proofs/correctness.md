---
title: CEGAR is sound and terminates on finite systems
proves: [correctness]
status: full
---

We use the notation of the page. $S$ is finite, $n = |S|$. A partition $\mathcal{B}$ of $S$ is *proper* if each block is a subset of $\mathit{Bad}$ or disjoint from it. For $s \in S$, $h(s)$ is the block that contains $s$. The abstract system $\hat M$ has the blocks as states, the initial blocks $\{B : B \cap I \ne \emptyset\}$, and the edges $B \to C$ iff $R(s, t)$ for some $s \in B$ and $t \in C$. A block is bad if it is a subset of $\mathit{Bad}$.

**Lemma 1.** After line L1, and after each execution of line L8, the blocks form a proper partition of $S$.

*Proof.* Line L1 splits each part of $P_0$ into its intersection with $\mathit{Bad}$ and the rest, and drops empty pieces. Line L8 replaces a block by two nonempty pieces of it (Lemma 4 below), and subsets of a block that is inside or outside $\mathit{Bad}$ are again inside or outside $\mathit{Bad}$. ∎

**Lemma 2 (existential abstraction).** If $s_0, \ldots, s_k$ is a path of $M$ with $s_0 \in I$, then $h(s_0), \ldots, h(s_k)$ is a path of $\hat M$ from an initial block. If $s_k \in \mathit{Bad}$, then $h(s_k)$ is a bad block.

*Proof.* $h(s_0)$ meets $I$ in $s_0$. Each $R(s_j, s_{j+1})$ gives the edge $h(s_j) \to h(s_{j+1})$. If $s_k \in \mathit{Bad}$, the block $h(s_k)$ meets $\mathit{Bad}$, so it is a subset of $\mathit{Bad}$ by Lemma 1. ∎

**Theorem 1 (soundness of HOLDS).** If line L5 returns HOLDS, no state of $\mathit{Bad}$ is reachable from $I$.

*Proof.* Line L4 is a breadth-first search over $\hat M$ from the initial blocks, so it finds a path to a bad block whenever one exists. A concrete path from $I$ to $\mathit{Bad}$ would give one by Lemma 2. ∎

**Lemma 3.** In line L6, for each $j \le i$, $S_j$ is exactly the set of states $t \in B_j$ for which there is a concrete path $t_0, \ldots, t_j = t$ with $t_0 \in I$ and $t_l \in B_l$ for all $l \le j$.

*Proof.* By induction on $j$. For $j = 0$ this is $I \cap B_0$. For $j \ge 1$, $t \in \mathrm{post}(S_{j-1}) \cap B_j$ iff $t \in B_j$ and $t$ has a predecessor in $S_{j-1}$, which by the induction hypothesis is the end of such a path of length $j - 1$. ∎

**Theorem 2 (soundness of FAILS).** If line L7 returns FAILS, the returned sequence is a concrete path from $I$ to $\mathit{Bad}$.

*Proof.* Here $i = L$, so $S_L \ne \emptyset$, and $S_L \subseteq B_L \subseteq \mathit{Bad}$. The implementation picks $t_L \in S_L$ and, for $j = L - 1, \ldots, 0$, a predecessor $t_j \in S_j$ of $t_{j+1}$. It exists, since $t_{j+1} \in \mathrm{post}(S_j)$. So $t_0, \ldots, t_L$ is a path with $t_0 \in S_0 \subseteq I$ and $t_L \in \mathit{Bad}$. ∎

**Lemma 4 (progress).** If line L8 runs, both $S_i$ and $B_i \setminus S_i$ are nonempty. After the split, the path $\pi$ is no longer an abstract path whose concrete simulation reaches step $i + 1$ through the dead-end block.

*Proof.* $S_i \ne \emptyset$ by the choice of $i$, as $S_0 \ne \emptyset$ because $B_0$ meets $I$. Since $i < L$ and $S_{i+1} = \emptyset$, no state of $S_i$ has a successor in $B_{i+1}$. The abstract edge $B_i \to B_{i+1}$ exists, so some state of $B_i$ has a successor in $B_{i+1}$, and that state is not in $S_i$. Hence $B_i \setminus S_i \ne \emptyset$. After the split, the block $S_i$ has no edge to $B_{i+1}$, and by Lemma 3 every concrete path that follows $B_0, \ldots, B_i$ ends step $i$ in $S_i$. ∎

**Theorem 3 (termination).** The loop runs at most $n$ rounds, so the algorithm stops with HOLDS or FAILS. With Theorems 1 and 2, the answer is correct.

*Proof.* Each round that does not return executes line L8, which by Lemma 4 increases the number of blocks by one. After line L1 there is at least one block, and a partition of $S$ into nonempty blocks has at most $n$ blocks. So at most $n - 1$ rounds execute line L8, and the round after the last of them returns. ∎

**Remark (general properties).** The same simulation argument proves the theorem of Clarke, Grumberg and Long (1994): the relation $\{(s, h(s))\}$ is a simulation of $M$ by $\hat M$ that respects the propositions, so every ACTL* formula that holds in $\hat M$ holds in $M$. CEGAR for ACTL and LTL uses this in place of Lemma 2, and checks lasso-shaped counterexamples in place of the finite paths of line L6.
