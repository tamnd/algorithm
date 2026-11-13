---
title: A* with an admissible heuristic returns a cheapest path, and with a consistent heuristic it expands no state twice
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The graph is directed, each state has finitely many successors, each action cost $c(n, n')$ is a nonnegative real number, and $h(n) \ge 0$ for each state. Let $g^*(n)$ be the cost of a cheapest path from $s_0$ to $n$, $h^*(n)$ the cost of a cheapest path from $n$ to a goal, and $C^* = h^*(s_0)$. The heuristic is *admissible* when $h(n) \le h^*(n)$ for all $n$, and *consistent* when $h(n) \le c(n, n') + h(n')$ for each action and $h(t) = 0$ for each goal $t$.

A state is *in OPEN* when it was put in OPEN at line L11 (or line L2) and not removed at line L4 since then. The heap of the implementation can hold old entries of a state, but it skips them, so this is the same thing. Each state that has a value $g[n]$ is in OPEN or in CLOSED, and not in both: line L4 removes it from OPEN, line L6 puts it in CLOSED, line L10 removes it from CLOSED and line L11 puts it back in OPEN.

**Fact 1.** The value $g[n]$ only goes down. It is never below $g^*(n)$, and $g[n] \ge g[\mathit{parent}[n]] + c(\mathit{parent}[n], n)$ for each $n \ne s_0$ that has a parent.

*Proof.* Line L9 changes $g[n']$ only when the new value is smaller. Each value given to $g[n']$ is $g[n] + c(n, n')$, where $g[n]$ is the cost of a path to $n$ by induction on time, so it is the cost of a walk from $s_0$ to $n'$, which is at least $g^*(n')$. When line L9 sets $\mathit{parent}[n'] = n$, the inequality holds with equality. Later, $g[n']$ stays until the parent changes, and $g[n]$ can only go down, so the inequality stays true. $\square$

**Fact 2 (the parent pointers form a tree).** Following parent pointers from a state never returns to it, and it ends at $s_0$.

*Proof.* By Fact 1 and $c \ge 0$, $g$ does not go down along parent pointers from a state to its children. Suppose line L9 sets $\mathit{parent}[m] = n$ where $m$ is an ancestor of $n$, so $g[m] \le g[n]$. The test of line L8 requires $g[n] + c(n, m) < g[m] \le g[n]$, which is false. So no assignment closes a cycle. The pointers from each state lead to a state with no parent, and only $s_0$ has none. $\square$

**Fact 3 (a value of g is the cost of a path that repeats no state).** For each value $v$ that line L9 gives to $g[m]$, there is a path from $s_0$ to $m$ that repeats no state and costs exactly $v$.

*Proof.* Attach to each value a walk: the value $0$ of $s_0$ gets the empty walk, and the value $g[n] + c(n, m)$ gets the walk of the current value of $g[n]$ followed by the action $(n, m)$. The walk costs the value. Along the walk, the values of the prefixes were given in strictly increasing order of time, because each one was the current value of its state when the next one was computed. Suppose the walk visits a state $u$ twice, with the values $a$ at time $t_1$ and $a'$ at the later time $t_2$. The part of the walk between the visits is a cycle, of cost $a' - a \ge 0$. At time $t_2$, Fact 1 gives $g[u] \le a$, and line L8 sets $g[u] = a'$ only if $a' < g[u] \le a$. This is false, so the walk repeats no state. $\square$

**Theorem 1 (termination on a finite graph).** If finitely many states can be reached from $s_0$, the search stops for each heuristic $h$.

*Proof.* A state has finitely many paths from $s_0$ that repeat no state. By Fact 3 and Fact 1, $g[m]$ takes distinct values among their costs, so line L9 runs finitely often for $m$. So line L11 runs finitely often, OPEN gets finitely many entries, and each pass of the loop removes one of them at line L4. $\square$

**Lemma 2 (a good state stays in OPEN).** Let $P = (p_0, p_1, \ldots, p_k)$ be a cheapest path from $s_0 = p_0$ to a state $p_k$, and suppose that $p_k$ is not in CLOSED with $g[p_k] = g^*(p_k)$. Then, each time the search is at line L3, some $p_j$ is in OPEN with $g[p_j] = g^*(p_j)$.

*Proof.* Call $p_i$ *done* when it is in CLOSED and $g[p_i] = g^*(p_i)$. By Fact 1, a done state stays done: its $g$ cannot go lower, so line L10 never removes it. The state $p_k$ is not done, so let $j$ be the least index such that $p_j$ is not done.

If $j = 0$, then $p_0 = s_0$ has $g = 0 = g^*(s_0)$ from line L1 on, and it is not in CLOSED, so it is in OPEN.

If $j \ge 1$, then $p_{j-1}$ is done. Look at the last expansion of $p_{j-1}$. After it, $p_{j-1}$ stayed in CLOSED, so its $g$ did not change, and $g[p_{j-1}] = g^*(p_{j-1})$ during that expansion. Line L7 then looked at the action to $p_j$, so after line L11 we have $g[p_j] \le g^*(p_{j-1}) + c(p_{j-1}, p_j) = g^*(p_j)$, where the equality holds because a part of a cheapest path is a cheapest path. By Fact 1, $g[p_j] = g^*(p_j)$ from then on. At that time $p_j$ was in OPEN, or it was in CLOSED with $g = g^*$, which would make it done for ever. Since then $p_j$ has not been expanded, because an expansion would also make it done. So $p_j$ is still in OPEN. $\square$

**Theorem 2 (a returned cost is optimal).** Let $h$ be admissible. If the search returns at line L5, the returned path goes from $s_0$ to a goal and costs $C^*$.

*Proof.* Let $t$ be a goal with $g^*(t) = C^*$, and $P$ a cheapest path from $s_0$ to $t$. A goal is never put in CLOSED, because line L5 returns before line L6, so Lemma 2 applies to $P$ before each removal at line L4. It gives a state $p_j$ in OPEN with
$$ f(p_j) = g^*(p_j) + h(p_j) \le g^*(p_j) + h^*(p_j) = C^* , $$
because $h^*(p_j)$ is at most the cost of the rest of $P$. Line L4 removes a state $n$ of least $f$, so $f(n) \le C^*$. If $n$ is a goal, then $g[n] \le g[n] + h(n) = f(n) \le C^*$ since $h \ge 0$, and $g[n] \ge g^*(n) \ge C^*$ by Fact 1. So $g[n] = C^*$.

By Fact 2, the parent pointers from $n$ give a path $q_0 = s_0, \ldots, q_r = n$. By Fact 1, its cost is
$$ \sum_{i=1}^{r} c(q_{i-1}, q_i) \le \sum_{i=1}^{r} \bigl(g[q_i] - g[q_{i-1}]\bigr) = g[n] - g[s_0] = C^* , $$
and no path to a goal costs less than $C^*$. So the path costs exactly $C^*$. $\square$

**Theorem 3 (completeness).** Let $h$ be admissible and let some goal be reachable. If the graph is finite, or if each action costs at least some $\delta > 0$, the search returns a path of cost $C^*$.

*Proof.* On a finite graph, the search stops by Theorem 1. While a goal is reachable, Lemma 2 applied to a cheapest path to a goal shows that OPEN is not empty at line L3, so the search does not reach line L12. It stops at line L5, and Theorem 2 gives the cost.

On an infinite graph with costs at least $\delta$, the proof of Theorem 2 shows that each state removed at line L4 has $g[n] \le f(n) \le C^*$. By Fact 3 this value is the cost of a path that repeats no state, and such a path has at most $C^*/\delta$ actions. With finite branching there are finitely many such paths, so finitely many entries can ever be removed with $f \le C^*$, and the loop cannot go on for ever. As before, it can stop only at line L5. $\square$

**Lemma 4.** If $h$ is consistent, then $h(u) \le d(u, v) + h(v)$ for all states $u$ and $v$, where $d(u, v)$ is the cost of a cheapest path from $u$ to $v$. In particular $h$ is admissible.

*Proof.* Add the inequalities $h(u_{i-1}) \le c(u_{i-1}, u_i) + h(u_i)$ along a cheapest path from $u$ to $v$. For admissibility, take $v$ a goal, where $h(v) = 0$. $\square$

**Theorem 5 (no reopening with a consistent heuristic).** Let $h$ be consistent. Each time line L4 removes a state $n$, $g[n] = g^*(n)$. So the test of line L8 never holds for a state in CLOSED, line L10 never removes a state from CLOSED, and each state is expanded at most once.

*Proof.* Suppose line L4 removes $n$ with $g[n] > g^*(n)$. Then $n$ is not done in the sense of Lemma 2, which we apply to a cheapest path $P$ from $s_0$ to $n$. It gives $p_j$ in OPEN with $g[p_j] = g^*(p_j)$, and $p_j \ne n$ because $g[n] \ne g^*(n)$. By Lemma 4 with $u = p_j$ and $v = n$,
$$ f(p_j) = g^*(p_j) + h(p_j) \le g^*(p_j) + d(p_j, n) + h(n) = g^*(n) + h(n) < g[n] + h(n) = f(n) . $$
So $n$ does not have the least $f$ in OPEN, a contradiction. After $n$ is expanded with $g[n] = g^*(n)$, Fact 1 shows that its $g$ never goes down again, so line L8 never holds for it. $\square$

**Theorem 6 (the f values are nondecreasing with a consistent heuristic).** Let $h$ be consistent. The values $f(n)$ of the states removed at line L4 form a nondecreasing sequence.

*Proof.* When $n$ is expanded, each successor $n'$ that is put in OPEN gets $f(n') = g[n] + c(n, n') + h(n') \ge g[n] + h(n) = f(n)$ by consistency. So all entries of OPEN have $f \ge f(n)$ after the expansion, as they had before it, and the next state removed has $f \ge f(n)$. $\blacksquare$
