---
title: IDA* ends and returns a cheapest path with an admissible heuristic and costs bounded away from zero
proves: [correctness]
status: full
---

We use the pseudocode of the page. Each state has finitely many successors, each action cost is at least some $\epsilon > 0$, and $h$ is admissible: $0 \le h(u) \le h^*(u)$, where $h^*(u)$ is the cost of a cheapest path from $u$ to a goal, so $h = 0$ at goals. We write $g^*(u)$ for the cost of a cheapest path from $s_0$ to $u$ and $C^* = h^*(s_0)$ when a goal is reachable. A *tree node* is a simple path from $s_0$, that is, a path that repeats no state; its $g$ is its cost and its $f$ is $g + h$ of its last state. DFS$(s_0, 0, T)$ walks the tree of tree nodes, and the stack PATH is the current tree node.

**Lemma 1 (one iteration).** For each threshold $T$, the call DFS$(s_0, 0, T)$ ends. If it returns FOUND, PATH is a path from $s_0$ to a goal of cost at most $T$. Otherwise it returns the least $f$ over the tree nodes that it cut off at line L8, or $\infty$ if it cut off none. It visits every tree node $P$ whose proper prefixes all have $f \le T$ and none of them ends in a goal, unless it returns FOUND first.

*Proof.* A call is made on a tree node only from its parent, and only if the parent has $f \le T$ (line L8) and is not a goal (line L9). A tree node with $f \le T$ has $g \le T$, so it has at most $T / \epsilon$ actions. Each node has finitely many children, so the tree of calls is finite, and the call ends. Line L11 tries every successor that is not on PATH, so every child of an expanded tree node gets a call. By induction on the depth, every tree node whose proper prefixes have $f \le T$ and are not goals gets a call, unless FOUND stops the search first. A call that returns FOUND has passed lines L8 and L9, so its state is a goal and $f = g + 0 \le T$, and PATH holds that tree node, whose cost is $g$. Lines L8 and L15 return the least value of $f$ among the cut-off nodes below the call, by induction on the height. $\square$

**Lemma 2 (the threshold stays at most $C^*$).** Let a goal be reachable and let $T \le C^*$ at line L4. If the iteration does not return FOUND, its result $r$ satisfies $T < r \le C^*$.

*Proof.* The result is the $f$ of a cut-off node, and line L8 cuts off only nodes with $f > T$, so $r > T$ if it is finite. Let $Q = (q_0, \ldots, q_k)$ be a cheapest path from $s_0$ to a goal. It repeats no state, since costs are positive, so each prefix of $Q$ is a tree node, and the prefix ending in $q_i$ has $g = g^*(q_i)$ and
$$f = g^*(q_i) + h(q_i) \le g^*(q_i) + h^*(q_i) = C^*,$$
because $q_i$ lies on a cheapest path to a goal. No proper prefix ends in a goal: such a goal would cost less than $C^*$. The prefix ending in $q_k$ has $f = C^*$. If all prefixes had $f \le T$, then by Lemma 1 the iteration would visit the prefix ending in $q_k$, which passes line L8 and is a goal, and it would return FOUND. So let $i$ be the least index with $f > T$ for the prefix ending in $q_i$. Its proper prefixes have $f \le T$ and are not goals, so Lemma 1 says that the iteration visits it, and line L8 cuts it off. So $r \le f \le C^*$. $\square$

**Theorem 3 (optimality).** If a goal is reachable, IDA* ends and returns a path from $s_0$ to a goal of cost $C^*$.

*Proof.* The first threshold is $h(s_0) \le C^*$. By Lemma 2 and induction, every threshold is at most $C^*$, and the thresholds rise strictly while no iteration returns FOUND. Each threshold after the first is the $f$ of a tree node with $f \le C^*$, so with $g \le C^*$ and at most $C^* / \epsilon$ actions. There are finitely many such tree nodes, so there are finitely many possible thresholds, and some iteration returns FOUND. By Lemma 1 the path reaches a goal and costs at most $T \le C^*$. Every path to a goal costs at least $C^*$, so it costs exactly $C^*$. Line L5 is never reached, since by Lemma 2 the result is finite. $\square$

**Theorem 4 (failure).** If finitely many states are reachable from $s_0$ and no goal is reachable, IDA* returns failure.

*Proof.* There are finitely many simple paths, so finitely many tree nodes and finitely many values of $f$. No iteration returns FOUND, since that needs a goal. Each finite result is the $f$ of a cut-off node, which is above $T$, so the thresholds rise strictly through this finite set of values. So after finitely many iterations no node has $f$ above $T$, nothing is cut off, line L15 keeps $\infty$, and line L5 returns failure. $\square$

**Remark.** The proof never uses consistency. It uses positive costs twice: to bound the depth of an iteration, and to show that a cheapest path repeats no state, so that skipping the states on PATH loses no optimal path. With zero-cost actions, the check against PATH is what keeps each iteration finite, and the same argument goes through with $\epsilon$ replaced by a bound on the length of simple paths on a finite graph.
