---
title: The Tanner graph represents H exactly, and its girth and peeling operations are correct
proves: [correctness]
status: full
---

Let $H$ be an $m \times n$ binary matrix. The graph has variable nodes $v_0, \ldots, v_{n-1}$ and check nodes $c_0, \ldots, c_{m-1}$. Write $N(c_i)$ for the variable neighbors of $c_i$ and $N(v_j)$ for the check neighbors of $v_j$.

**Claim 1 (construction).** After lines L1 to L6, $j \in$ `chk_adj[i]` if and only if $H_{ij} = 1$, if and only if $i \in$ `var_adj[j]`, and each such pair appears once in each list.

*Proof.* Lines L3 and L4 visit each pair $(i, j)$ exactly once and test $H_{ij} = 1$. Lines L5 and L6 then append $j$ to the list of $i$ and $i$ to the list of $j$. No other line changes the lists. $\square$

**Claim 2 (syndrome).** The parity of check $c_i$ on a word $x$, $\sum_{j \in N(c_i)} x_j \bmod 2$, is the $i$th entry of $H x^T$. So $x$ is a codeword if and only if every check node has even parity.

*Proof.* $(H x^T)_i = \sum_j H_{ij} x_j = \sum_{j : H_{ij} = 1} x_j$, and by Claim 1 the index set is $N(c_i)$. $\square$

**Claim 3 (girth).** The method `girth` returns the length $g$ of a shortest cycle, or None for a forest.

*Proof.* The graph is simple, because $H$ has entries 0 and 1, so a cycle has length at least 4.

*Every reported value is the length of a closed walk that contains a cycle.* A value $c = d(u) + d(w) + 1$ is reported when $w$ is a neighbor of $u$ that is already labeled and is not the parent of $u$. It is also not a child of $u$: a child of $u$ gets its label while $u$ is processed, on its single occurrence in the adjacency list of $u$, and goes into the first branch. So the edge $uw$ is not a tree edge. The tree path from the root to $u$, the edge $uw$, and the tree path from $w$ back to the root form a closed walk of length $c$ in which the edge $uw$ appears once. Removing the shared part of the two tree paths leaves a cycle through $uw$ of length at most $c$. So every reported value is at least $g$, and nothing is reported in a forest.

*The value $g$ is reported.* Let $C$ be a cycle of length $g = 2k$ (the graph is bipartite) and let the root $r$ be a node of $C$. First, for any two nodes $x, y$ of $C$ the distance in the graph equals the distance along $C$: a shorter path and the shorter arc of $C$ would be two different paths between $x$ and $y$, whose union contains a cycle shorter than $g$. Let $a$ be the node of $C$ at distance $k$ from $r$ along both arcs, and $a_1$, $a_2$ its two neighbors on $C$, both at distance $k - 1$. The node $a$ has one parent, so for one of them, say $a_2$, the parent of $a$ is not $a_2$; and the parent of $a_2$ is not $a$, since $a_2$ is closer to the root. When $a$ is processed, $a_2$ is already labeled, so the value $k + (k - 1) + 1 = g$ is reported. The early stop, which ends a search when $2 d(u) \ge$ best, does not prevent this: it fires before $a$ only if best $\le 2k = g$, and since best $\ge g$ always, best $= g$ already. Any later value from $u$ is at least $d(u) + (d(u) - 1) + 1 = 2 d(u)$, since a labeled neighbor has $d(w) \ge d(u) - 1$, so the early stop never skips a smaller value. $\square$

A set $S$ of variable nodes is a *stopping set* when no check node has exactly one neighbor in $S$.

**Lemma 4.** The union of two stopping sets is a stopping set. So every set $E$ of variable nodes contains a unique largest stopping set $S^*(E)$, the union of all stopping sets inside $E$.

*Proof.* Suppose a check $c$ has exactly one neighbor $j$ in $S_1 \cup S_2$, with $j \in S_1$. Then $c$ is a neighbor of $S_1$ with exactly one neighbor in $S_1$, which is not allowed. The empty set is a stopping set, so the union of all stopping sets inside $E$ exists and is the largest. $\square$

**Claim 5 (peeling).** `peel(E)` returns $S^*(E)$.

*Proof.* Let `left` be the current set, starting at $E$, and `count[i]` the number of neighbors of $c_i$ in `left`. The counts are right at the start, and when $j$ leaves `left` every check of $j$ is decremented, so they stay right.

*Invariant: $S^* \subseteq$ `left`.* It holds at the start. A node $j$ is removed only when its check $c_i$ has `count[i]` $= 1$, so $j$ is the only neighbor of $c_i$ in `left`. If $j$ were in $S^*$, then $c_i$ would have exactly one neighbor in $S^* \subseteq$ `left`, which is not allowed. So $j \notin S^*$.

*At the end `left` is a stopping set.* A count only decreases. A check whose count is 1 at the start is in the queue, and a check whose count becomes 1 later is put in the queue at that moment. When such a check is taken from the queue with count 1, its single node is removed and its count becomes 0. If it is taken with count 0, its count stays 0. So when the queue is empty no count is 1, and no check has exactly one neighbor in `left`.

So `left` is a stopping set inside $E$, hence `left` $\subseteq S^*$, and with the invariant `left` $= S^*$. $\blacksquare$

**Meaning for decoding on the erasure channel.** A check with exactly one erased neighbor gives the value of that neighbor as the sum of the others. Claim 5 shows that peeling recovers every erased position outside $S^*(E)$ and none inside it. No other order of the same steps can do better, because the result does not depend on the order. The support of every nonzero codeword is a stopping set, by Claim 2, so the smallest stopping set is never larger than the minimum distance.
