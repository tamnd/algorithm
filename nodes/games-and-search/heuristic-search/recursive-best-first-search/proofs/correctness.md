---
title: RBFS ends and returns a cheapest path with an admissible heuristic on a finite graph
proves: [correctness]
status: full
---

We use the pseudocode of the page. The graph is finite, each action cost is positive, and $h$ is admissible: $0 \le h(u) \le h^*(u)$, where $h^*(u)$ is the cost of a cheapest path from $u$ to a goal, so $h = 0$ at goals. A *tree node* is a simple path $P$ from $s_0$, that is, a path that repeats no state. Its $g$ is its cost, and its $f$ is $g + h$ of its last state. A call RBFS$(n, g, F, B)$ is made on a tree node $P$ that ends in $n$, and PATH is $P$ during the call. For a tree node $P$, let $c^*(P)$ be the least cost of a simple path from $s_0$ to a goal that has $P$ as a prefix, or $\infty$ if there is none. When a goal is reachable, $C^*$ is the cost of a cheapest path from $s_0$ to a goal. A cheapest path repeats no state, since costs are positive, so $c^*(s_0) = C^*$, and $c^*(P) \ge C^*$ for every $P$.

Two facts follow from the definitions. First, $f(P) \le c^*(P)$: a goal path through $P$ costs $g$ plus the cost of a path from $n$ to a goal, which is at least $g + h^*(n) \ge g + h(n)$. Second, if $n$ is not a goal, then $c^*(P)$ is the least $c^*(P + m)$ over the children $m$ that line L5 keeps, because a simple goal path that extends $P$ must continue with a state that is not on $P$. Let $V$ be the set of the values $f(P)$ over all tree nodes, together with $\infty$. The graph is finite, so there are finitely many simple paths, and $V$ is finite.

**Lemma 1 (values).** Every value that the search stores or returns is in $V$.

*Proof.* Line L3 returns some $f(P)$, line L6 returns $\infty$, and line L11 returns a stored value. Line L7 stores $f(m)$ or $\max(F, f(m))$, and line L10 stores a returned value. The first call has $F = h(s_0) = f(s_0)$. By induction on the steps of the search, all these values are in $V$. $\square$

**Lemma 2 (a call returns above its bound).** If a call RBFS$(n, g, F, B)$ returns a value $r$, then $r > B$ or $r = \infty$.

*Proof.* At line L3, $r = f(n) > B$. At line L6, $r = \infty$. At line L11, the loop of line L8 has ended, so the least stored value is above $B$ or equals $\infty$, and that value is $r$. $\square$

**Lemma 3 (termination).** Each call ends, by returning or by stopping the whole search at line L4.

*Proof.* By induction on the number of states that are not on PATH. A call on a tree node that has no child at line L5 returns at line L3, L4 or L6. Otherwise each recursive call at line L10 is on a longer tree node, so it ends by induction. Consider one pass of the loop at line L8 with the least stored value $F[m_1]$. The loop condition gives $F[m_1] \le B$ and $F[m_1] < \infty$, and $F_2 \ge F[m_1]$ since $F_2$ is the second least value, so the bound $B' = \min(B, F_2)$ of the call satisfies $B' \ge F[m_1]$. If the call returns $r$, then by Lemma 2 $r > B' \ge F[m_1]$ or $r = \infty > F[m_1]$. So each pass strictly raises one stored value, and no pass lowers one. By Lemma 1 the stored values are in the finite set $V$, so the sum of their ranks in $V$ rises at each pass and is bounded, and the loop runs finitely many passes. $\square$

**Lemma 4 (stored values are lower bounds).** For each call made on a tree node $P$ with the value $F$, we have $F \le c^*(P)$. Each value $F[m]$ stored for a child $m$ satisfies $F[m] \le c^*(P + m)$. A call on $P$ that returns gives a value at most $c^*(P)$.

*Proof.* By induction on the steps of the search. The first call has $F = h(s_0) \le c^*(s_0)$. At line L7, $f(m) \le c^*(P + m)$ by the first fact, and $F \le c^*(P) \le c^*(P + m)$, because a goal path through $P + m$ goes through $P$. So both choices of line L7 are at most $c^*(P + m)$. At line L10, the call on $P + m_1$ gets the value $F[m_1] \le c^*(P + m_1)$, and by induction it returns a value at most $c^*(P + m_1)$, which line L10 stores. For the returns: line L3 returns $f(P) \le c^*(P)$. Line L6 returns $\infty$ only if $n$ is not a goal and has no child off $P$, and then no simple goal path extends $P$, so $c^*(P) = \infty$. Line L11 returns the least stored value, which is at most the least $c^*(P + m)$, and that is $c^*(P)$ by the second fact, since line L4 did not stop the search, so $n$ is not a goal. $\square$

**Lemma 5 (the bound of a call).** Let a call on a tree node $P = (p_0, \ldots, p_t)$ have the bound $B$. For each $i < t$ and each child $m \ne p_{i+1}$ that the call on $(p_0, \ldots, p_i)$ stored, $B$ is at most the value of $m$ that was stored when the call on $(p_0, \ldots, p_{i+1})$ in this chain was made.

*Proof.* The call on $(p_0, \ldots, p_{i+1})$ gets the bound $\min(B_i, F_2)$, where $B_i$ is the bound of its parent call and $F_2$ is the second least stored value at that moment. The child $p_{i+1}$ has the least value, so $F_2 \le F[m]$ for every other child $m$. By induction on $t - i$, the bound of each call in the chain is at most the bounds of the calls above it, and so at most each such $F_2$. $\square$

**Theorem 6 (optimality).** If a goal is reachable, RBFS stops at line L4 with a path of cost $C^*$.

*Proof.* First, RBFS finds a goal. If $s_0$ is a goal, the first call passes line L3, since $f(s_0) = 0 \le \infty$, and stops at line L4. Otherwise, let $Q = (q_0, \ldots, q_k)$ be a cheapest path to a goal. The first call stores a value for $q_1$, and by Lemma 4 that value is at most $c^*((q_0, q_1)) = C^* < \infty$ at all times. With $B = \infty$, the loop of line L8 can only end when all stored values are $\infty$, which never happens. By Lemma 3 the first call ends, so it ends by stopping the search at line L4.

Now let line L4 stop the search in a call on $P = (p_0, \ldots, p_t)$ with the bound $B$. Line L3 passed, and $h(p_t) = 0$, so the cost of $P$ is $g = f(P) \le B$. If $P$ is a prefix of $Q$, then $p_t$ is a goal on $Q$. A goal $q_i$ with $i < k$ would give a goal path cheaper than $C^*$, so $P = Q$ and $g = C^*$. Otherwise let $j$ be the largest index with $(q_0, \ldots, q_j) = (p_0, \ldots, p_j)$. Then $j < t$ and $j < k$, and $q_{j+1} \ne p_{j+1}$. The state $q_{j+1}$ is not on $(q_0, \ldots, q_j)$, since $Q$ is simple, so the call on $(p_0, \ldots, p_j)$ stored a value for it at line L7. By Lemma 4 that value is at most $c^*((q_0, \ldots, q_{j+1})) = C^*$ at all times, and by Lemma 5 $B$ is at most that value. So $g \le B \le C^*$. Every path to a goal costs at least $C^*$, so $g = C^*$. $\square$

**Theorem 7 (failure).** If no goal is reachable, RBFS returns failure.

*Proof.* By Lemma 3 the first call ends. Line L4 never stops the search, since no tree node ends in a goal, so the first call returns and nothing is recorded. Line L2 returns failure. $\square$

**Remark.** Korf also proved that RBFS expands the tree nodes for the first time in best-first order of their values, also when $f$ falls along a path, and that SRBFS, without the inheritance of line L7, has this order only when $f$ never falls. The argument above does not use that order. It uses line L7 only through the bound $F \le c^*(P)$, so it also holds for SRBFS. It uses neither consistency nor a bound on the number of expansions, which can be much larger than for A*.
