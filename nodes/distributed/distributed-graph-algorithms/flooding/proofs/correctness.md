---
title: Flooding reaches every node, builds a spanning tree and sends exactly 2m − (n − 1) messages
proves: [correctness, termination, complexity]
status: full
---

**Claim.** Run FLOOD on a connected undirected graph $G = (V, E)$ with $n$ nodes and $m$ edges, from the source $s$, with reliable channels and no failures. Then:

1. every node is reached, and each node runs line L7 at most one time;
2. the run sends exactly $2m - (n - 1)$ messages, in every timing model and under every schedule;
3. the parent pointers form a spanning tree of $G$ rooted at $s$;
4. in the synchronous model, node $v$ is reached in round $\mathrm{dist}(s, v)$, its parent is at distance $\mathrm{dist}(s, v) - 1$, and no message is sent after round $e + 1$, where $e = \max_v \mathrm{dist}(s, v)$;
5. in the asynchronous model with every message delay at most 1, node $v$ is reached by time $\mathrm{dist}(s, v)$, and the last message arrives by time $e + 1$.

**Notation.** $N(v)$ is the set of neighbours of $v$ and $\deg(v) = |N(v)|$. A node is *reached* when it sets $\mathit{reached} \leftarrow \mathit{true}$ (line L2 for $s$, line L7 for the others). Write $t(v)$ for the time (or round) at which $v$ is reached.

**Step 1 (each node sends at most one batch).** A node sends only at line L3 or line L8. Line L3 runs only at $s$, at the start. Line L8 runs only directly after line L7, and line L7 runs only when $\mathit{reached}$ is false (line L5), after which $\mathit{reached}$ stays true. So $s$ sends one batch of $\deg(s)$ messages, $s$ never runs line L7 (it is reached at the start), and every other node runs line L7 at most one time and then sends $\deg(v) - 1$ messages, one to each neighbour other than the sender $u$.

**Step 2 (every node is reached).** Suppose some node is never reached. Since $G$ is connected and $s$ is reached, there is an edge $\{x, y\}$ with $x$ reached and $y$ not reached. If $x = s$, line L3 sends M to $y$. If $x \ne s$, line L8 sends M to every neighbour of $x$ except $\mathit{parent}(x)$, and $y \ne \mathit{parent}(x)$ because $\mathit{parent}(x)$ sent a message, so it was reached. In both cases a message travels to $y$, channels are reliable, and on its arrival $y$ runs line L7 if it is not yet reached. This contradicts the choice of $y$. So every node is reached, and by Step 1 every $v \ne s$ runs line L7 exactly one time.

**Step 3 (the count).** By Steps 1 and 2 the number of messages is

$$\deg(s) + \sum_{v \ne s} (\deg(v) - 1) = \sum_{v \in V} \deg(v) - (n - 1) = 2m - (n - 1).$$

The count uses only which lines run, not when they run, so it holds for every schedule and in every timing model.

**Step 4 (the tree).** For $v \ne s$, $\mathit{parent}(v)$ is the sender of the copy that reached $v$. That sender was reached before it sent, and the message takes a positive time (or arrives in the round in which it is sent, one round after its sender was reached). So $t(\mathit{parent}(v)) < t(v)$. Following parent pointers from any node, $t$ strictly decreases, so no node repeats, and the walk stops only at a node whose parent is itself, which is $s$. The $n - 1$ edges $\{v, \mathit{parent}(v)\}$, $v \ne s$, are edges of $G$, and each node has a path to $s$ along them. A connected graph with $n$ nodes and $n - 1$ edges is a tree, so the parent pointers form a spanning tree rooted at $s$.

**Step 5 (synchronous rounds).** In round $r$ every node sends the messages that it produced in round $r - 1$, and they arrive in round $r$. So a node reached in round $r$ sends in round $r + 1$ (the source sends in round 1). We show by strong induction on $r$ that the nodes reached in round $r$ are exactly the nodes at distance $r$.

For $r = 0$ only $s$ is reached. Let $r \ge 1$ and assume the claim for all rounds before $r$. A node reached in round $r$ gets a message from a node reached in round $r - 1$, which is at distance $r - 1$, so it is at distance at most $r$; it is not at a smaller distance, since those nodes were reached in earlier rounds. Conversely, let $\mathrm{dist}(s, v) = r$ and let $u$ be a neighbour of $v$ at distance $r - 1$. Then $u$ is reached in round $r - 1$ and sends in round $r$ to all its neighbours except its parent, which is at distance $r - 2$ (or $u = s$ and it sends to all). So $v$ gets M in round $r$ and was not reached before. The node that $v$ takes as its parent sent in round $r$, so it is at distance $r - 1$.

Nodes at distance at most $e$ are reached by round $e$ and send by round $e + 1$. No node sends later.

**Step 6 (asynchronous time).** Let every delay be at most 1 and let local steps take no time. By induction on $d = \mathrm{dist}(s, v)$: $t(s) = 0$. For $d \ge 1$, take a neighbour $u$ of $v$ at distance $d - 1$, so $t(u) \le d - 1$. If $v = \mathit{parent}(u)$, then $t(v) < t(u)$. Otherwise $u$ sends M to $v$ at time $t(u)$, and it arrives by $t(u) + 1 \le d$. Either way $t(v) \le d$. All sends happen at reach times, which are at most $e$, so every message arrives by time $e + 1$. $\blacksquare$
