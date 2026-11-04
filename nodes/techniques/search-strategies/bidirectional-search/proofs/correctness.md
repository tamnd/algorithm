---
title: Bidirectional breadth-first search with complete layers returns a shortest path
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, with unit action costs. Write $d_s(v)$ for the least number of actions from $s$ to $v$, $d_t(v)$ for the least number from $v$ to $t$ (each is $\infty$ when there is no path), and $d = d_s(t)$. Write $F$ and $B$ for the key sets of *parent_f* and *parent_b*. We assume $s \ne t$; otherwise line L1 returns the path $[s]$ with 0 actions.

**Invariant 1 (exact layers).** Each time line L4 tests the loop condition, there are integers $a, \beta \ge 0$ with
$$ F = \{ v : d_s(v) \le a \}, \quad \mathrm{front}_f = \{ v : d_s(v) = a \}, \quad B = \{ v : d_t(v) \le \beta \}, \quad \mathrm{front}_b = \{ v : d_t(v) = \beta \}, $$
and for each $v \in F$ other than $s$, $\mathrm{parent}_f[v]$ is a state $u$ with $d_s(u) = d_s(v) - 1$ and $v$ a successor of $u$. The same holds for the backward side with predecessors.

*Proof.* At the start, $a = \beta = 0$, $F = \mathrm{front}_f = \{s\}$ and $B = \mathrm{front}_b = \{t\}$. Assume the invariant and let the loop expand the forward side without returning. Lines L7 to L12 add to $F$ exactly the successors of states with $d_s = a$ that were not in $F$. A successor $v$ of a state with $d_s = a$ has $d_s(v) \le a + 1$, and if $v \notin F$ then $d_s(v) = a + 1$. Each state with $d_s(v) = a + 1$ has a predecessor on a shortest path with $d_s = a$, so it is found. So after line L13, $F = \{ v : d_s(v) \le a + 1 \}$ and $\mathrm{front}_f$ is the new layer, with the parents as claimed. The backward case is the same with predecessors. $\square$

**Invariant 2 (disjoint tables).** Until the search returns, $F \cap B = \emptyset$.

*Proof.* At the start $F \cap B = \{s\} \cap \{t\} = \emptyset$. A state enters $F$ or $B$ only at line L10, and line L11 returns at once if it is already in the other table. $\square$

**Lemma 3 (no meeting means a long path).** If $F \cap B = \emptyset$ with $a$ and $\beta$ as in Invariant 1, then $d \ge a + \beta + 1$.

*Proof.* Suppose $d \le a + \beta$, and let $s = x_0, x_1, \ldots, x_d = t$ be a shortest path. Let $i = \min(a, d)$. Then $d_s(x_i) = i \le a$ and $d_t(x_i) = d - i \le \beta$, because $d - a \le \beta$ when $i = a$ and $d - i = 0$ when $i = d$. So $x_i \in F \cap B$, a contradiction. $\square$

**Theorem 4 (a returned path is shortest).** If the search returns a path, it goes from $s$ to $t$ and has exactly $d$ actions.

*Proof.* Let the return happen at line L11, while the forward side expands its layer $a$, at the state $v$. Then $v$ has just entered $F$ with $d_s(v) = a + 1$, and $v \in B$, so $d_t(v) \le \beta$. JOIN follows the parents in $F$ from $v$ back to $s$, a path of $d_s(v)$ actions by Invariant 1, and the parents in $B$ from $v$ to $t$, a path of $d_t(v)$ actions. Together they form a path from $s$ to $t$ with at most $a + 1 + \beta$ actions. Before this layer, the tables were disjoint by Invariant 2, so $d \ge a + \beta + 1$ by Lemma 3. The path has at least $d$ actions, so it has exactly $d$. The backward case is the same with the roles of the sides exchanged. $\square$

**Theorem 5 (failure and termination).** If $t$ can be reached from $s$, the search returns a path after at most $d$ layer expansions. If it returns failure, $t$ cannot be reached from $s$. If the graph is finite, the search stops.

*Proof.* Each expansion that does not return adds one to $a$ or to $\beta$, so after $k$ such expansions $a + \beta = k$. By Invariant 2 and Lemma 3, $k + 1 \le d$ at each test of line L4, so when $d$ is finite at most $d - 1$ expansions end without a return. A frontier that is not empty contains states at distance $a$ from $s$ (or $\beta$ to $t$), and when $t$ is reachable from $s$ neither frontier is empty: a shortest path from $s$ to $t$ has a state at each distance $i \le d$, and for $a < d$ the state at distance $a$ lies in $\mathrm{front}_f$, and likewise for the backward side. So the loop keeps expanding until it returns, within $d$ expansions, and by Theorem 4 with a shortest path.

If the search returns failure at line L14, one frontier is empty, say $\mathrm{front}_f$. By Invariant 1 no state has $d_s = a$, so no state has $d_s > a$, and $F$ is the set of all states reachable from $s$. If $t$ were reachable, then $t \in F$, while $t \in B$ always, against Invariant 2. The backward case is the same.

If the graph is finite, each expansion that does not return adds a non-empty set of new states to $F$ or to $B$, or leaves a frontier empty, which ends the loop. The tables are finite, so the loop stops. $\blacksquare$
