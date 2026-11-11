---
title: The echo algorithm sends exactly 2m messages, builds a spanning tree and decides only when the wave is complete
proves: [correctness, termination, complexity]
status: full
---

**Claim.** Run ECHO on a connected undirected graph $G = (V, E)$ with $n \ge 2$ nodes and $m$ edges, from the initiator $s$, with reliable channels, no failures and any finite delays. Then:

1. every node is reached, and the parent pointers of the nodes other than $s$ form a spanning tree rooted at $s$;
2. exactly one token crosses each edge in each direction, so the run sends exactly $2m$ messages;
3. $s$ decides exactly one time, and at that moment every node has received a token on every incident edge and no token is in transit;
4. in the synchronous model, $s$ decides in round $r$ with $2e \le r \le 2e + 1$, where $e = \max_v \mathrm{dist}(s, v)$;
5. in the asynchronous model with every delay at most 1, $s$ decides by time $e + 1 + h$, where $h$ is the height of the tree.

For $n = 1$ the initiator has no neighbour, sends nothing and decides at once; we leave this case out.

**Notation.** $N(v)$ is the set of neighbours of $v$, $\deg(v) = |N(v)|$, and $\mathit{rec}(v)$ is the counter of line L5. A node *completes* when line L9 finds $\mathit{rec} = \deg(v)$. A token that a node sends at line L3 or line L8 is a *flood token*; a token sent at line L11 is an *echo*.

**Step 1 (flooding part).** Lines L1 to L8 are the flooding algorithm with one change: line L5 counts every token, and the test of line L6 decides whether the node forwards. A node runs line L7 at most one time, since afterwards $\mathit{reached}$ is true. The argument of the flooding proof applies without change: on every edge from a reached node $x$ to a node $y \ne \mathit{parent}(x)$ a flood token is sent, so every node is reached; and $\mathit{parent}(v)$ was reached before $v$, so the parent pointers form a spanning tree rooted at $s$. The tokens sent along the way to the parent are echoes and do not change who is reached first, because an echo goes from a reached node to a reached node.

**Step 2 (at most one token per directed edge).** Fix a node $v$ and a neighbour $w$. If $v = s$, then $v$ sends to $w$ only at line L3, one time; $s$ never runs line L11. If $v \ne s$ and $w \ne \mathit{parent}(v)$, then $v$ sends to $w$ only at line L8, which runs one time. If $w = \mathit{parent}(v)$, then line L8 skips $w$, and $v$ sends to $w$ only at line L11. Line L11 runs only when $\mathit{rec}(v) = \deg(v)$ is reached; the counter grows by one per token, and by the claim of this step (applied to the senders) at most $\deg(v)$ tokens arrive at $v$, so the equality holds after exactly one receipt and line L11 runs at most one time. Formally, induct on the order of events: as long as no directed edge has carried two tokens, $\mathit{rec}(v) \le \deg(v)$ for all $v$, and each line that sends on a directed edge runs at most one time, so the next event does not create a second token on any directed edge.

**Step 3 (every node completes).** Induct on the height of the subtree of $v$ in the tree of Step 1. Take $v \ne s$ and assume all children of $v$ complete. A neighbour $w$ of $v$ sends a token to $v$: if $w$ is the parent of $v$, at line L3 or line L8 (since $v \ne \mathit{parent}(w)$); if $w$ is a child of $v$, at line L11 when $w$ completes; otherwise $v \ne \mathit{parent}(w)$, so at line L8 or line L3. By Step 2 each of these tokens is the only one on its directed edge, so $v$ receives exactly $\deg(v)$ tokens and completes. A leaf of the tree has no children, so the induction has a base. Finally $s$ receives one token from each neighbour by the same case analysis and completes.

**Step 4 (the count).** By Steps 2 and 3, each node $v \ne s$ sends a token on each of its $\deg(v)$ edges: on the $\deg(v) - 1$ non-parent edges at line L8, and to the parent at line L11. The initiator sends $\deg(s)$ tokens at line L3. The total is $\sum_{v} \deg(v) = 2m$, under every schedule.

**Step 5 (the decision is safe).** The initiator decides at line L10, when it completes, which happens exactly one time. At that moment it has received an echo from each child $c$, so $c$ had completed. A node completes only after receiving the echoes of all its children, so by induction down the tree every node $v$ had completed, that is, had received $\deg(v)$ tokens. So $\sum_v \deg(v) = 2m$ tokens had been received. At most $2m$ tokens are ever sent (Step 2), so every sent token has been received and none is in transit. Since every node has completed, no node will send again: lines L3, L8 and L11 have all run where they can run. So when $s$ decides the run is over.

**Step 6 (synchronous rounds).** A node that receives tokens in round $r$ sends in round $r + 1$, and those tokens arrive in round $r + 1$. In the synchronous model the tree is a breadth-first tree, as in flooding, so a node at depth $d$ is at distance $d$ and is reached in round $d$. Let $c(v)$ be the round in which $v$ completes.

*Upper bound.* A non-parent neighbour $w$ of $v$ is at distance at most $\mathrm{dist}(s, v) + 1 \le e$, is reached by round $e$, and sends its flood token by round $\min(e, \mathrm{dist}(s, v) + 1) + 1$. So the flood tokens arrive at a node of depth $d$ by round $\min(d + 2, e + 1)$. We show $c(v) \le 2e - d + 1$ for each node $v$ of depth $d$, by induction on $e - d$. For $d = e$, $v$ has no children (they would have depth $e + 1$), so $c(v) \le e + 1$. For $d < e$, each child $c$ has $c(c) \le 2e - d$ and its echo arrives by round $2e - d + 1$, while flood tokens arrive by round $d + 2 \le 2e - d + 1$. So $c(v) \le 2e - d + 1$. For $s$ at depth $0$, the decision round is $c(s) \le 2e + 1$.

*Lower bound.* Let $v$ be at distance $e$. It is reached in round $e$. Each node $x$ on the tree path from $v$ to $s$ completes only after the echo of the next node toward $v$ arrives, and the echo arrives at least one round after that node completes. So $c(s) \ge c(v) + e \ge 2e$.

**Step 7 (asynchronous time).** Let every delay be at most 1. By the flooding proof, node $w$ is reached by time $\mathrm{dist}(s, w) \le e$ and sends its flood tokens then, so all flood tokens arrive by time $e + 1$. Let $\mathrm{ht}(v)$ be the height of the subtree of $v$. We show that $v$ completes by time $e + 1 + \mathrm{ht}(v)$, by induction on $\mathrm{ht}(v)$. A leaf receives only flood tokens and completes by time $e + 1$. For an inner node, each child $c$ completes by time $e + 1 + \mathrm{ht}(c) \le e + \mathrm{ht}(v)$ and its echo arrives by time $e + 1 + \mathrm{ht}(v)$, and the flood tokens arrive by time $e + 1$. So $v$ completes by time $e + 1 + \mathrm{ht}(v)$, and $s$ decides by time $e + 1 + h$. Since $e \le D \le n - 1$ and $h \le n - 1$, this is $O(n)$. ∎
