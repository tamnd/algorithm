---
title: Negamax returns the value for the side to move, which is the minimax value with the sign of the player
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode NEGAMAX of the page. The input is a finite [game tree](/game-tree/) of a two-player [zero-sum game](/zero-sum-game/) with perfect information and no chance moves, in which the players MAX and MIN alternate. Each terminal node $t$ has a value $u(t)$ for MAX, and the evaluation of the page is
$$ e(t) = \begin{cases} u(t) & \text{if MAX is to move at } t, \\ -u(t) & \text{if MIN is to move at } t, \end{cases} $$
that is, the value of $t$ for the player to move there. Let $s(n) = +1$ if MAX is to move at $n$ and $s(n) = -1$ if MIN is to move, so $e(t) = s(t)\, u(t)$. The players alternate, so $s(c) = -s(n)$ for each child $c$ of $n$.

Let $V(n)$ be the minimax value of $n$ for MAX, as on [minimax](/minimax/): $V(t) = u(t)$ at a terminal node, the maximum over the children at a MAX node and the minimum at a MIN node. The *height* $h(n)$ is 0 at a terminal node and $1 + \max_c h(c)$ otherwise.

**Lemma 1.** For real numbers, or $\pm\infty$, $\min(x_1, \ldots, x_m) = -\max(-x_1, \ldots, -x_m)$.

*Proof.* The map $x \mapsto -x$ reverses the order, so it sends the least element of a finite set to the greatest element of the image. $\square$

**Theorem 1 (termination and the returned value).** For each node $n$, the call NEGAMAX($n$) stops and returns $N(n) = s(n)\, V(n)$, the minimax value for the player to move at $n$.

*Proof.* By induction on $h(n)$. If $h(n) = 0$, line L1 returns $e(n) = s(n)\, u(n) = s(n)\, V(n)$.

Let $h(n) = k \ge 1$, let the claim hold below height $k$, and let $c_1, \ldots, c_m$ be the children, with $m \ge 1$. Each recursive call stops and returns $N(c_i) = s(c_i)\, V(c_i) = -s(n)\, V(c_i)$. Line L2 sets $v = -\infty$, and after the $i$-th turn of line L3, $v = \max_{j \le i} (-N(c_j))$, because $\max(-\infty, x) = x$. After the last turn,
$$ v = \max_{j} \bigl(-N(c_j)\bigr) = \max_j \bigl(s(n)\, V(c_j)\bigr). $$
If $s(n) = +1$, this is $\max_j V(c_j) = V(n) = s(n)\, V(n)$, because $n$ is a MAX node. If $s(n) = -1$, it is $\max_j (-V(c_j)) = -\min_j V(c_j)$ by Lemma 1, and $\min_j V(c_j) = V(n)$ because $n$ is a MIN node, so $v = -V(n) = s(n)\, V(n)$. Line L4 returns $v$. $\square$

**Corollary 2 (agreement with minimax).** For a root where MAX moves, NEGAMAX(root) $=$ MINIMAX(root, true). For a root where MIN moves, NEGAMAX(root) $= -$MINIMAX(root, false). The best move for the player to move is a child $c$ with $-N(c) = N(n)$, the same child that minimax picks.

*Proof.* The first two claims are Theorem 1 with $s = \pm 1$ and the correctness of minimax. For the third, $-N(c) = s(n)\, V(c)$, so $-N(c) = N(n)$ if and only if $V(c) = V(n)$. $\square$

**Theorem 3 (cost).** NEGAMAX($n$) makes one call for each node of the subtree of $n$, evaluates each leaf once, and has at most $h(n) + 1$ calls active at the same time. On a uniform tree of branching factor $b$ and depth $d$ it evaluates $b^d$ leaves.

*Proof.* Each call calls NEGAMAX once on each child and on no other node, so by induction on the depth each node is called exactly once. The active calls lie on one path from $n$, which has at most $h(n) + 1$ nodes. A uniform tree has $b^d$ leaves. $\blacksquare$
