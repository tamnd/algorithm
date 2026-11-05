---
title: DECOMPOSE returns a tree decomposition of width at most 4k + 4, or a true answer that the treewidth exceeds k
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a simple graph with $n$ vertices, and $k \ge 0$. For $C \subseteq V$, $N(C)$ is the set of vertices outside $C$ with a neighbour in $C$. A task $(C, S)$ has $C$ nonempty and connected, and $S = N(C)$.

**Lemma 1 (edges).** If $\mathrm{tw}(G) \le k$, then $|E| \le kn$.

*Proof.* Take a tree decomposition of width at most $k$ and remove bags that are subsets of a neighbouring bag; this keeps a decomposition. If $n \ge 1$, some leaf bag $X_t$ with neighbour $X_s$ has a vertex $v \in X_t \setminus X_s$ (or $t$ is the only bag). By the subtree condition, $v$ is in no other bag, so all neighbours of $v$ are in $X_t$, and $\deg v \le k$. Removing $v$ keeps the treewidth at most $k$. By induction on $n$, $|E| \le kn$. $\square$

**Lemma 2 (balanced separator).** Let $H$ be a graph with $\mathrm{tw}(H) \le k$ and $W \subseteq V(H)$. There is a set $X$ of at most $k + 1$ vertices such that every connected component of $H - X$ contains at most $|W|/2$ vertices of $W$.

*Proof.* Take a tree decomposition $(T, \{X_t\})$ of $H$ of width at most $k$ and root $T$. For a node $t$, let $V_t$ be the union of the bags in the subtree of $t$. At the root, $|W \cap V_t| = |W| \ge |W|/2$. Choose a node $t$ with $|W \cap V_t| \ge |W|/2$ such that every child $t'$ of $t$ has $|W \cap V_{t'}| < |W|/2$; it exists, by walking down from the root. Let $X = X_t$, so $|X| \le k + 1$. By the subtree condition, a vertex in $V_{t'} \setminus X_t$ for a child $t'$ appears only in bags of the subtree of $t'$, and a vertex outside $V_t$ appears only outside the subtree of $t$. Every edge lies in a bag, so an edge of $H - X$ cannot join two of the sets $V_{t'} \setminus X_t$ (for different children $t'$) and $V \setminus V_t$. So each component $D$ of $H - X$ lies in one of these sets. If $D \subseteq V_{t'} \setminus X_t$, then $|W \cap D| \le |W \cap V_{t'}| < |W|/2$. If $D \subseteq V \setminus V_t$, then $|W \cap D| \le |W| - |W \cap V_t| \le |W|/2$. $\square$

**Lemma 3 (grouping).** Let $a_1, \ldots, a_r \ge 0$ with $\sum a_i \le w$ and each $a_i \le w/2$. The indices can be split into two groups, each with sum at most $2w/3$.

*Proof.* If some $a_i \ge w/3$, put $i$ alone in the first group: its sum is at most $w/2$, and the rest sum to at most $w - w/3$. Otherwise add indices to the first group one at a time until its sum is at least $w/3$, or no index is left. Before the last addition the sum was below $w/3$, and the last $a_i$ is below $w/3$, so the first group sums to less than $2w/3$; the second sums to at most $w - w/3 = 2w/3$, or to $0$. $\square$

**Lemma 4 (a split exists).** Let $(C, S)$ be a task with $|S| = 3k + 4$, and $\mathrm{tw}(G) \le k$. Then line L6 finds a split.

*Proof.* Apply Lemma 2 to $H = G[C \cup S]$, which has treewidth at most $k$, and $W = S$. Let $X$ be the set, $S_X = X \cap S$, and $Y_0 = X \cap C$. Each component of $H - X$ contains at most $|S|/2$ vertices of $S \setminus X$. By Lemma 3, with $w = |S|$, the components can be grouped so that the vertices of $S \setminus X$ in the two groups, $S_A$ and $S_B$, number at most $2|S|/3 = 2k + 8/3$ each, so at most $2k + 2$ each, being integers. No path in $H - X$ joins $S_A$ to $S_B$, since they lie in different components, so $Y_0$ meets every path from $S_A$ to $S_B$ in $H - S_X$, and $|Y_0| \le k + 1 - |S_X|$. Line L6 tries this split, and the flow finds a cut $Y \subseteq C$ of the least size, which is at most $|Y_0|$. $\square$

**Invariant.** Every task on the stack satisfies: $C$ is nonempty and connected; $S = N(C)$; $|S| \le 3k + 4$; $C$ is disjoint from all bags made so far; and the node $\mathit{parent}$, if any, has a bag that contains $S$.

*Initialization.* At line L2, $C$ is a component, so $N(C) = \emptyset$.

*Maintenance.* Take a task $(C, S)$ and its bag $B \supseteq S$, with $B \setminus S \subseteq C$. Let $D$ be a component of $G[C \setminus B]$. It is nonempty, connected, and disjoint from $B$ and the older bags. A neighbour $u \notin D$ of a vertex of $D$ is either in $C$, and then in $B$, since $D$ is a whole component of $G[C \setminus B]$; or outside $C$, and then in $N(C) = S \subseteq B$. So $N(D) \subseteq B$, the bag of the new node. For the size: if line L5 was used, $|N(D)| \le |B| \le |S| + 1 \le 3k + 4$. If line L8 was used, then $D$ is connected and avoids $Y \cup S$, and every vertex of $N(D) \cap S$ outside $S_X$ is joined to $D$ by an edge. If $N(D)$ met both $S_A$ and $S_B$, there would be a path from $S_A$ to $S_B$ through $D$ that avoids $Y$ and $S_X$, against the choice of $Y$. So $N(D) \subseteq S_A \cup S_X \cup Y$ or $N(D) \subseteq S_B \cup S_X \cup Y$, and $|N(D)| \le (2k + 2) + (k + 1) = 3k + 3$.

*Progress.* Each task adds at least one vertex of $C$ to its bag. At line L5 this is clear. At line L8, $|S \setminus S_X| \ge 3k + 4 - (k + 1) = 2k + 3$, and $|S_A|, |S_B| \le 2k + 2$, so both $S_A$ and $S_B$ are nonempty. If $Y \cap C = \emptyset$, then $Y = \emptyset$, and in $G[C \cup S] - S_X$ the connected set $C$ is adjacent to every vertex of $S_A \cup S_B$, since $S = N(C)$, which joins $S_A$ to $S_B$, a contradiction. So $Y$ contains a vertex of $C$.

**Termination.** By the invariant and progress, the sets $C$ of all tasks taken from the stack contain distinct new vertices in their bags, and these vertices are never in a later $C$. So there are at most $n$ tasks, and every loop of the algorithm is finite. The search of line L6 is finite.

**Theorem.** If DECOMPOSE returns "treewidth $> k$", then $\mathrm{tw}(G) > k$. Otherwise it returns a tree decomposition of $G$ in which every bag has at most $4k + 5$ vertices. If $\mathrm{tw}(G) \le k$, it does not return "treewidth $> k$".

*Proof.* The answer "treewidth $> k$" comes from line L1, which is right by Lemma 1, or from line L7, which is right by Lemma 4. So if $\mathrm{tw}(G) \le k$ the decomposition is returned.

Suppose a decomposition is returned. The nodes form a forest, since each node except the first of a component is joined to an older node. Bag sizes: at line L5, $|B| \le 3k + 4$; at line L8, $|B| \le |S| + |Y| \le 3k + 4 + k + 1 = 4k + 5$.

*Each vertex is covered, and its bags are connected.* Let $v \in V$. It lies in the first task's $C$ for its component. Follow the tasks whose $C$ contains $v$: each next one is a child task of the last, until a task $\tau$ puts $v$ in its bag, which must happen since every task with $v \in C$ either puts $v$ in its bag or passes it to exactly one child task, and there are finitely many tasks. After $\tau$, $v$ is in no later $C$. A later bag holds $v$ only through its boundary, as $B = S \cup (B \cap C)$. A child task $(D, N(D))$ of a node $\sigma$ with $v \in N(D)$ has $v \in B_\sigma$, since $N(D) \subseteq B_\sigma$, and its own node is joined to $\sigma$. So every bag that holds $v$ is joined, by a chain of nodes whose bags hold $v$, to the node of $\tau$; these bags form a connected subtree.

*Each edge is covered.* Let $uv \in E$, and let $\tau$ be the first task that puts $u$ or $v$ in its bag, say $u$. At that moment $v$ is not in an older bag, so it is in $C_\tau$, as $u$ and $v$ were together in each earlier $C$ (they are adjacent, and none of the earlier bags holds either). If $v \in B_\tau$, the edge is covered. Otherwise $v$ lies in a component $D$ of $G[C_\tau \setminus B_\tau]$ with $u \in N(D)$, and the task for $D$ has $u \in S$. Repeat with this task: $u$ stays in the boundary, by the same argument, until a task puts $v$ in its bag, whose bag also contains $u$ as part of $S$. $\blacksquare$

**Running time.** At most $n$ tasks; each tries at most $3^{|S|} \le 3^{3k+4}$ splits, each with a flow of at most $k + 2$ augmenting paths on a graph of $O(n + m)$ size, and $m \le kn$ after line L1. So the time is $O(27^k k^2 n^2)$.
