---
title: Distributed BFS, the synchronous algorithm, the Bellman-Ford form and the layered form compute BFS trees within the stated message and time bounds
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G = (V, E)$ is a connected undirected graph with $n$ nodes and $m$ edges, $r$ is the root, $\mathrm{dist}(v) = \mathrm{dist}(r, v)$, $e = \max_v \mathrm{dist}(v) \le D$, and $L_k = \{v : \mathrm{dist}(v) = k\}$. Channels are reliable and need not be FIFO; there are no failures. For asynchronous time bounds every delay is at most 1 and local steps take no time. A *BFS tree* is a spanning tree rooted at $r$ in which every $v \ne r$ has a parent in $L_{\mathrm{dist}(v) - 1}$.

## Part A. The synchronous algorithm (lines L1 to L6)

**Claim A.** In the synchronous model, node $v$ sets $\mathit{dist}(v) = \mathrm{dist}(v)$ in round $\mathrm{dist}(v)$, its parent is in $L_{\mathrm{dist}(v) - 1}$, the run sends exactly $2m - (n - 1)$ messages, and the last message is sent in round $e$ or $e + 1$.

*Proof.* Induct on $k$: the nodes that set $\mathit{dist}$ in round $k$ are exactly the nodes of $L_k$, and they set it to $k$. For $k = 0$ this is line L1. Let $k \ge 1$. A message that arrives in round $k$ was sent in round $k$ by a node that set its value in round $k - 1$, so it carries $k - 1$ and comes from $L_{k-1}$. A node that gets such a message is at distance at most $k$, and if it is at distance less than $k$ its value is already set (induction), so line L3 skips it. A node $v \in L_k$ has a neighbour $u \in L_{k-1}$; $u$ sent $k - 1$ in round $k$ to every neighbour except its parent, which is in $L_{k-2}$ (or $u = r$ sent to all), so $v$ receives a message in round $k$ and sets $\mathit{dist}(v) = k$ at line L4, with a parent from $L_{k-1}$.

Each node runs line L4 and line L5 exactly one time (line L3 blocks a second time), so $r$ sends $\deg(r)$ messages and every other node sends $\deg(v) - 1$. The sum is $2m - (n - 1)$. Nodes of $L_e$ send in round $e + 1$ if they have a neighbour other than the parent, and no node sends later. ∎

## Part B. The asynchronous Bellman-Ford form

A node keeps $\mathit{dist}(v)$, starting at $\infty$ (and $0$ at $r$). On receipt of $d$ from $u$ with $d + 1 < \mathit{dist}(v)$, it sets $\mathit{dist}(v) \leftarrow d + 1$, $\mathit{parent}(v) \leftarrow u$, and sends $d + 1$ to every neighbour except $u$.

**Claim B.** Under every schedule: (1) the value $\mathit{dist}(v)$ is always at least $\mathrm{dist}(v)$ and at most $n - 1$ once it is finite; (2) each $v \ne r$ updates at most $n - \mathrm{dist}(v)$ times; (3) the number of messages is at most $\deg(r) + \sum_{v \ne r} (n - \mathrm{dist}(v))(\deg(v) - 1) \le 2nm$; (4) in the end $\mathit{dist}(v) = \mathrm{dist}(v)$ and the parents form a BFS tree; (5) with delays of at most 1, every node holds its final value by time $\mathrm{dist}(v)$ and the last message arrives by time $e + 1$.

*Proof of (1).* Each update of $v$ to the value $d + 1$ is caused by an earlier update of $u$ to $d$ (or by the start at $r$, for $d = 0$). Following causes back gives a sequence of nodes $r = x_0, x_1, \dots, x_{d+1} = v$, each adjacent to the next, where $x_i$ took the value $i$, and the updates happen in increasing time order. So $\mathit{dist}(v)$ is the length of a walk from $r$ and is at least $\mathrm{dist}(v)$. The nodes $x_i$ are distinct: if $x_i = x_j$ with $i < j$, the node took the value $i$ before taking the value $j > i$, but values at a node only decrease. A sequence of distinct nodes has at most $n$ entries, so $d + 1 \le n - 1$.

*Proof of (2) and (3).* The successive values of $v \ne r$ strictly decrease and lie in $\{\mathrm{dist}(v), \dots, n - 1\}$, a set of $n - \mathrm{dist}(v)$ values. Each update sends $\deg(v) - 1$ messages; the start at $r$ sends $\deg(r)$. Since $n - \mathrm{dist}(v) \le n$ and $\sum_v \deg(v) = 2m$, the total is at most $2nm$, which is $O(nm)$.

*Proof of (4) and (5).* Induct on $k = \mathrm{dist}(v)$ to show that $v$ holds the value $k$ by time $k$. For $k = 0$ this is the start. Let $v \in L_k$, $k \ge 1$, and take $u \in L_{k-1}$ adjacent to $v$. By induction $u$ took the value $k - 1$ at some time $t \le k - 1$, on receipt from some $u'$ whose value was $k - 2$ (or $u = r$). By (1), $\mathrm{dist}(u') \le k - 2$, so $u' \ne v$, and $u$ sent $k - 1$ to $v$ at time $t$. It arrives by time $t + 1 \le k$, and then $\mathit{dist}(v) \le k$. With (1), $\mathit{dist}(v) = k$ from then on. The final parent of $v$ sent the value $k - 1$, so by (1) it is at distance at most $k - 1$; it is adjacent to $v$, so it is at distance exactly $k - 1$. Hence the parents form a BFS tree. No update happens after time $e$, so the last message is sent by time $e$ and arrives by time $e + 1$. ∎

Without a delay bound the run still ends, since the number of updates is finite by (2). No node learns that the run has ended; this needs [termination detection](/termination-detection/).

## Part C. The asynchronous layered form

The root runs phases $k = 1, 2, \dots$. In phase $k$: a PULSE travels from $r$ down the current tree to the nodes of depth $k - 1$ (a node of smaller depth forwards it to its children, or reports at once if it has none); each node of depth $k - 1$ sends EXPLORE to all neighbours other than its parent; a node that is not in the tree joins on its first EXPLORE with depth $k$ and that sender as parent and answers ACK, and every other EXPLORE is answered REJECT; a node of depth $k - 1$ that has all its answers sends REPORT to its parent, carrying whether it got an ACK; an inner node sends REPORT when all its children have reported. The root starts phase $k + 1$ if some ACK was reported and stops otherwise.

**Claim C.** (1) At the start of phase $k$ the tree consists exactly of the nodes of $L_0 \cup \dots \cup L_{k-1}$, each with depth equal to its distance, a parent one layer up and a correct list of children, and no message is in transit. (2) The root stops after phase $e + 1$. (3) The run sends exactly
$$2(2m - n + 1) + 2 \sum_{k=1}^{e+1} \big(|L_0 \cup \dots \cup L_{k-1}| - 1\big) \le 4m + 2(e + 1)(n - 1)$$
messages, which is $O(m + nD)$. (4) With delays of at most 1 it ends by time $(e + 1)(e + 2)$, which is $O(D^2)$.

*Proof of (1) and (2).* Induct on $k$. Phase 1 starts with the tree $\{r\}$ and no message in transit. Assume (1) at the start of phase $k$. The PULSE follows tree edges, so it reaches every tree node, and the nodes of depth $k - 1$ are exactly the nodes of $L_{k-1}$. A node $w \in L_k$ is not in the tree and has a neighbour in $L_{k-1}$, so it receives at least one EXPLORE; the first one makes it join with depth $k$ and a parent in $L_{k-1}$, and that parent adds $w$ to its children on the ACK. A node not in the tree with $\mathrm{dist}(w) > k$ has no neighbour in $L_{k-1}$ and receives no EXPLORE. A node in the tree, or one that has already joined in this phase, answers REJECT and does not change. So at the end of phase $k$ the tree is $L_0 \cup \dots \cup L_k$ with the stated properties.

Every EXPLORE gets exactly one answer, a node of depth $k - 1$ reports only after all its answers have arrived, and an inner node reports only after all its children have. So when the root has all reports, every PULSE, EXPLORE, answer and REPORT of the phase has been received: no message is in transit, which gives (1) for phase $k + 1$. The reports carry, by an OR up the tree, whether $L_k \ne \emptyset$. For $k \le e$ the layer $L_k$ is not empty and the root continues; in phase $e + 1$ no ACK is sent and the root stops.

*Proof of (3).* In phase $k$ the PULSE crosses each tree edge one time, and so does the REPORT: $|L_0 \cup \dots \cup L_{k-1}| - 1$ messages each. Each node $v$ sends EXPLORE exactly in the phase in which it is a frontier node, on $\deg(v)$ edges if $v = r$ and on $\deg(v) - 1$ edges otherwise; phases run up to $e + 1$, so every node is a frontier node exactly once. That gives $\sum_v \deg(v) - (n - 1) = 2m - n + 1$ EXPLOREs over the run, and as many answers. Adding up gives the formula, and $|L_0 \cup \dots \cup L_{k-1}| - 1 \le n - 1$ gives the bound.

*Proof of (4).* In phase $k$ the PULSE reaches depth $k - 1$ within $k - 1$ time units, the EXPLOREs and their answers take at most 2 more, and a REPORT from depth $j$ reaches the root within $j$ units after it is sent, by induction up the tree; so phase $k$ takes at most $(k - 1) + 2 + (k - 1) = 2k$ units. The sum over $k = 1, \dots, e + 1$ is $(e + 1)(e + 2)$. ∎
