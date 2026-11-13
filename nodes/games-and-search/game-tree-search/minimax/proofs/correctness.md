---
title: Minimax returns the value of the game tree, and each player can guarantee it
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode MINIMAX of the page. The input is a finite [game tree](/game-tree/) of a two-player [zero-sum game](/zero-sum-game/) with [perfect information](/perfect-information-game/) and no chance moves. Each node $n$ is a MAX node or a MIN node, as given by the flag max-to-move, and each terminal node $t$ has a number $u(t)$, its value for MAX. The *height* $h(n)$ of a node is 0 for a terminal node and $1 + \max_c h(c)$ over the children $c$ otherwise.

Define the *minimax value* $V(n)$ by recursion on the height:
$$ V(n) = \begin{cases} u(n) & \text{if } n \text{ is terminal,} \\ \max_{c} V(c) & \text{if } n \text{ is a MAX node,} \\ \min_{c} V(c) & \text{if } n \text{ is a MIN node.} \end{cases} $$

**Theorem 1 (termination and the returned value).** For each node $n$, the call MINIMAX($n$, flag of $n$) stops and returns $V(n)$.

*Proof.* By induction on $h(n)$. If $h(n) = 0$, then $n$ is terminal, line L1 returns $u(n) = V(n)$, and the call stops.

Let $h(n) = k \ge 1$ and let the claim hold for all nodes of height less than $k$. Each child $c$ has $h(c) \le k - 1$, so each recursive call stops and returns $V(c)$. The children of the opposite type get the opposite flag, so each child gets its own flag. Let $n$ be a MAX node with children $c_1, \ldots, c_m$, where $m \ge 1$ because $n$ is not terminal. Line L3 sets $v = -\infty$. After the $i$-th turn of the loop in line L4, $v = \max(V(c_1), \ldots, V(c_i))$, by induction on $i$, because $\max(-\infty, x) = x$ and $\max$ is associative. The loop has $m$ turns, so line L8 returns $\max_c V(c) = V(n)$. The case of a MIN node is the same with lines L6 and L7, with $+\infty$ and $\min$. $\square$

A *strategy* for MAX picks one child at each MAX node, and a strategy for MIN picks one child at each MIN node. A pair of strategies $(\sigma, \tau)$ gives one path from $n$ to a terminal node $t(\sigma, \tau)$, and the *outcome* is $u(t(\sigma, \tau))$.

**Theorem 2 (the value is guaranteed for both players).** For each node $n$ there is a strategy $\sigma^*$ for MAX with $u(t(\sigma^*, \tau)) \ge V(n)$ for every strategy $\tau$ of MIN, and a strategy $\tau^*$ for MIN with $u(t(\sigma, \tau^*)) \le V(n)$ for every strategy $\sigma$ of MAX. Hence
$$ \max_\sigma \min_\tau u(t(\sigma, \tau)) = \min_\tau \max_\sigma u(t(\sigma, \tau)) = V(n). $$

*Proof.* Let $\sigma^*$ pick, at each MAX node $m$, a child $c$ with $V(c) = V(m)$. Such a child exists because $V(m)$ is the maximum over the finitely many children. Let $\tau^*$ pick, at each MIN node $m$, a child with $V(c) = V(m)$.

Fix any $\tau$ and follow the path of $(\sigma^*, \tau)$ from $n$. At a MAX node, $\sigma^*$ goes to a child with the same value. At a MIN node $m$, $\tau$ goes to some child $c$, and $V(c) \ge \min_{c'} V(c') = V(m)$. So the value $V$ does not decrease along the path. The path ends at a terminal node $t$ with $V(t) = u(t)$, so $u(t) \ge V(n)$. The proof for $\tau^*$ is the same with the inequalities reversed.

For the equation: $\min_\tau u(t(\sigma^*, \tau)) \ge V(n)$ gives $\max_\sigma \min_\tau u \ge V(n)$, and $\max_\sigma u(t(\sigma, \tau^*)) \le V(n)$ gives $\min_\tau \max_\sigma u \le V(n)$. For every function of two arguments, $\max_\sigma \min_\tau \le \min_\tau \max_\sigma$. These three inequalities give the two equalities. $\square$

By Theorems 1 and 2, MINIMAX returns the number that MAX can guarantee and that MIN can hold MAX to. This is the value of the game at $n$.

**Theorem 3 (cost).** The call MINIMAX($n$, flag) makes exactly one call for each node of the subtree of $n$. On a uniform tree of branching factor $b \ge 2$ and depth $d$ it evaluates exactly $b^d$ leaves and makes $(b^{d+1} - 1)/(b - 1)$ calls. The largest number of calls active at the same time is $h(n) + 1$.

*Proof.* Each call on a node $m$ calls MINIMAX once on each child of $m$ and on no other node, and the root is called once. By induction on the depth, each node of the subtree is called exactly once. A uniform tree has $b^i$ nodes at depth $i$, so it has $b^d$ leaves and $\sum_{i=0}^{d} b^i = (b^{d+1} - 1)/(b - 1)$ nodes. The active calls at any time are on the nodes of one path from $n$, and a path has at most $h(n) + 1$ nodes. $\blacksquare$
