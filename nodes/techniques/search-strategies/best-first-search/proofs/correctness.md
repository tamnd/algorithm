---
title: Best-first search is sound and stops on finite spaces, and with f = g + h for an admissible h it returns a cheapest path
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, with action costs $c \ge 0$. A node is *live* while it is the node stored in *reached* for its state. Line L6 skips each popped node that is not live. A node is *expanded* when it passes line L6 and line L7 and reaches line L8.

**Fact 1 (each node is a path).** Each node $n$ is the end of a chain of parent pointers that spells a path $s_0 = x_0, x_1, \ldots, x_k = n.\mathrm{state}$ of the state space, with $n.g$ the sum of the costs of its actions and $n.\mathrm{depth} = k$. This holds for the root of line L1, and line L9 adds one action of cost $c$ to the path of the parent, $c$ to $g$ and $1$ to the depth. $\square$

**Fact 2 (stored costs decrease).** For each state $s$, the value $\mathrm{reached}[s].g$ only decreases strictly over time, because line L11 overwrites the entry only after line L10 found a strictly smaller $g$. A state never leaves *reached*.

**Fact 3 (live nodes).** Each node in the chain of parents of a pushed node was pushed, at line L2 or line L12. A live node is in the frontier or was expanded: it was pushed when it became live, and a live node that is popped is either returned at line L7 or expanded.

**Theorem 1 (soundness).** If the search returns $(P, g)$, then $P$ is a path from $s_0$ to a goal state and $g$ is its cost.

*Proof.* The search returns only at line L7, with $P$ the path of a node $n$ whose state passes IS-GOAL, and $g = n.g$. By Fact 1, $P$ is a path from $s_0$ to $n.\mathrm{state}$ with cost $n.g$. $\square$

**Lemma 2 (no repeated state).** Each node pushed at line L12 is a path without a repeated state. Two pushed nodes never have the same path.

*Proof.* Suppose a pushed node $m$ has the path $x_0, \ldots, x_k$ with $x_i = x_j$ for some $i < j$. Let $p_i$ and $p_j$ be the nodes of the prefixes that end at positions $i$ and $j$. By Fact 3 both were pushed, and $p_i$ was pushed before $p_j$ was created, since $p_j$ descends from $p_i$. From the push of $p_i$ on, $\mathrm{reached}[x_i].g \le p_i.g$ by Fact 2. The cycle from position $i$ to position $j$ has cost at least $0$, so $p_j.g \ge p_i.g \ge \mathrm{reached}[x_j].g$ when $p_j$ was created. Then the test at line L10 failed, and $p_j$ was not pushed, a contradiction. If two pushed nodes had the same path, they would have the same $g$, and the second would fail the test at line L10 in the same way. $\square$

**Theorem 3 (finite spaces, any $f$).** If finitely many states can be reached from $s_0$, the search stops for every evaluation function $f$. If it returns failure, then no goal state can be reached from $s_0$.

*Proof.* A finite space has finitely many paths from $s_0$ without a repeated state. By Lemma 2, each of them is pushed at most once and no other path is pushed. So the number of pushes is finite. Each iteration pops a node, so the loop stops.

Suppose the search returns failure at line L13, so the frontier is empty. By Fact 3, the live node of each state in *reached* was expanded. Let $s_0 = y_0, y_1, \ldots, y_r$ be a path to a goal state $y_r$. We show by induction that each $y_i$ is in *reached*. The state $y_0$ is in *reached* from line L3. If $y_i$ is in *reached*, its live node was expanded, so line L10 was run for a child with state $y_{i+1}$, and after it $y_{i+1}$ was in *reached*, which by Fact 2 it never leaves. So $y_r$ is in *reached*, and its live node was expanded. But a live node of a goal state is returned at line L7 and never expanded. This contradiction shows that no goal is reachable. $\square$

**Lemma 4 (a good node in the frontier).** Let $f(n) = n.g + h(n.\mathrm{state})$, where $h$ is admissible: $0 \le h(s) \le h^*(s)$ for each state $s$, with $h^*(s)$ the least cost of a path from $s$ to a goal. Let $\pi = x_0, \ldots, x_r$ be a path from $s_0$ to a goal state $x_r$ with cost $C$. At the start of each iteration of line L4, if the search has not yet returned, the frontier holds a live node $q$ with $f(q) \le C$.

*Proof.* Write $C_j$ for the cost of the prefix $x_0, \ldots, x_j$. Call $x_j$ *covered* when $x_j$ is in *reached* and $\mathrm{reached}[x_j].g \le C_j$. By Fact 2, a covered state stays covered. The state $x_0$ is covered, since its root node has $g = 0 = C_0$. Let $j$ be the largest index such that $x_0, \ldots, x_j$ are all covered, and let $q$ be the live node of $x_j$, so $q.g \le C_j$.

If $j < r$ and $q$ was expanded, then line L10 was run for a child with state $x_{j+1}$ and $g = q.g + c(x_j, x_{j+1}) \le C_{j+1}$, and afterwards $\mathrm{reached}[x_{j+1}].g \le C_{j+1}$. Then $x_{j+1}$ is covered, against the choice of $j$. If $j = r$, then $q$ is a live node of a goal state, and it was not expanded, by line L7. So in both cases $q$ was not expanded, and by Fact 3 it is in the frontier. The rest of $\pi$ is a path from $x_j$ to a goal with cost $C - C_j$, so $h(x_j) \le h^*(x_j) \le C - C_j$, and
$$ f(q) = q.g + h(x_j) \le C_j + (C - C_j) = C. \qquad \square $$

**Theorem 5 (optimality for $f = g + h$).** Let $f = g + h$ with $h$ admissible. If the search returns $(P, g)$, then $g = C^*$, the infimum of the costs of the paths from $s_0$ to a goal.

*Proof.* Let the search return the node $n$ at line L7. By Theorem 1, $n.g$ is the cost of a path to a goal, so $n.g \ge C^*$. Since $n$ is at a goal, $0 \le h(n.\mathrm{state}) \le h^*(n.\mathrm{state}) = 0$, so $f(n) = n.g$. Take any path $\pi$ from $s_0$ to a goal, with cost $C$. In the iteration that pops $n$, Lemma 4 gives a node $q$ in the frontier with $f(q) \le C$, and POP-MIN returned $n$, so $n.g = f(n) \le f(q) \le C$. This holds for each such $\pi$, so $n.g \le C^*$. Hence $n.g = C^*$. $\square$

With $h = 0$, Theorem 5 is the optimality of [uniform-cost search](/uniform-cost-search/).

**Theorem 6 (infinite spaces for $f = g + h$).** Let $f = g + h$ with $h$ admissible, let each state have finitely many successors, let each action cost be at least $\epsilon > 0$, and let some goal be reachable from $s_0$. Then the search stops and returns a path of cost $C^*$.

*Proof.* Fix a path $\pi$ to a goal, with cost $C$. By Lemma 4, until the search returns, the frontier is not empty, and POP-MIN returns a node with $f \le C$. Each node $m$ has $f(m) \ge m.g \ge \epsilon \cdot m.\mathrm{depth}$, so each popped node has depth at most $\lfloor C/\epsilon \rfloor$. With finite branching there are finitely many paths from $s_0$ of at most this depth, and by Lemma 2 each is pushed at most once. So only finitely many pops are possible, and the loop cannot end at line L13, because the frontier is not empty. So the search returns, and by Theorem 5 the cost is $C^*$. $\square$

**Remark (other $f$).** Theorems 1 and 3 hold for every $f$. Theorems 5 and 6 need $f = g + h$ with $h$ admissible. For $f = h$, greedy best-first search, they fail. Let $s_0$ have two children: a state $y$ with $h(y) = 1$, whose child is a goal, and a state $x_1$ that starts an infinite chain $x_1 \to x_2 \to \cdots$ with no goal and $h(x_i) = 1/(i+1)$. All costs are 1. Each $x_i$ has $f(x_i) < 1 = f(y)$, so the search pops $x_1, x_2, \ldots$ and never pops $y$. It runs for ever, while a goal is reachable. $\blacksquare$
