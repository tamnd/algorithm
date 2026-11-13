---
title: PEA* returns a cheapest path with an admissible heuristic, and with C = 0 it stores no node above the optimal cost
proves: [correctness]
status: full
---

We use the pseudocode of the page. Each action cost is positive, each state has finitely many successors, $C \ge 0$, and $h$ is admissible: $0 \le h(u) \le h^*(u)$, where $h^*(u)$ is the cost of a cheapest path from $u$ to a goal, so $h = 0$ at goals. We write $g^*(u)$ for the cost of a cheapest path from $s_0$ to $u$, and $C^* = h^*(s_0)$ when a goal is reachable. A state is *seen* once it has a value $g$. For a seen state $u$ and an action from $u$ to $m$ of cost $c$, we say that $m$ is *covered* by $u$ if $g(m) \le g(u) + c$. The values in OPEN are the current ones: the implementation skips heap entries whose $F$ or $g$ has changed.

**Fact 1 (real paths).** For each seen state $u$, $g(u)$ is the cost of a path from $s_0$ to $u$, so $g(u) \ge g^*(u)$, and $g(u)$ never rises. The parents lead from $u$ back to $s_0$ along a path of cost at most $g(u)$.

*Proof.* As for A*: line L11 sets $g(m) = g(n) + c$ only when this is smaller, and the parent $n$ then has $g(n) < g(m)$, which stays true as $g(n)$ can only fall. So the parents strictly lower $g$, end at $s_0$, and give a path of cost at most $g(u)$ by induction. $\square$

**Fact 2 (OPEN).** A seen state is in OPEN unless it has been taken out at line L4 since its value $g$ was last set and was not put back at line L12. A goal state is never expanded, so its $F$ equals its $g$. A child $m$ that is covered by $u$ stays covered as long as $g(u)$ does not change.

*Proof.* Line L11 puts a state in OPEN when it sets $g$, line L4 takes it out, and line L12 puts it back. Line L5 returns before a goal is expanded, so the only value $F$ that a goal gets is the one of line L11, which is $g + h = g$. The last claim holds because $g(m)$ never rises. $\square$

**Lemma 3 (one expansion).** When line L12 puts $n$ back with $F(n) = $ REST, every child of $n$ that is not covered by $n$ has $g(n) + c + h(m) \ge$ REST. When line L12 does not put $n$ back, every child of $n$ is covered by $n$.

*Proof.* In the loop, a child $m$ either passes line L9, and then lines L10 and L11 make it covered, or it is skipped at line L9, and then REST is at most its $f$. So after the loop, a child that is not covered was skipped, and has $f \ge$ REST. If REST $= \infty$, no child was skipped, so every child is covered. $\square$

**Lemma 4 (a good state).** Let a goal be reachable and let $Q = (q_0, \ldots, q_k)$ be a cheapest path from $s_0$ to a goal. Until the search returns, OPEN holds some $q_i$ with $g(q_i) = g^*(q_i)$ and $F(q_i) \le C^*$.

*Proof.* Since the prefixes of $Q$ are cheapest paths, $g^*(q_{j+1}) = g^*(q_j) + c(q_j, q_{j+1})$, and $g^*(q_j) + h(q_j) \le C^*$ for each $j$. Let $i$ be the largest index such that $g(q_j) = g^*(q_j)$ for all $j \le i$. By Fact 1, $g(q_i)$ stays $g^*(q_i)$.

If $i = k$, the goal $q_k$ is seen and never expanded, so by Fact 2 it is in OPEN, with $F(q_k) = g^*(q_k) = C^*$.

If $i < k$, then $q_{i+1}$ is not covered by $q_i$, since otherwise $g(q_{i+1}) \le g^*(q_{i+1})$ and so, by Fact 1, $g(q_{i+1}) = g^*(q_{i+1})$, against the choice of $i$. Since the value $g(q_i)$ was last set, $q_i$ may have been expanded some number of times. If none of these expansions closed it, then by Fact 2 it is in OPEN. Lemma 3 says that none closed it, since $q_{i+1}$ is not covered. Its value $F(q_i)$ is either the one set at line L11, which is $g^*(q_i) + h(q_i) \le C^*$, or the value REST of its last expansion. In that expansion $q_{i+1}$ was not covered, so by Lemma 3 REST $\le g^*(q_i) + c + h(q_{i+1}) = g^*(q_{i+1}) + h(q_{i+1}) \le C^*$. $\square$

**Theorem 5 (optimality).** If a goal is reachable and the search returns, it returns a path from $s_0$ to a goal of cost $C^*$.

*Proof.* Line L5 returns a goal $n$ that had the least $F$ in OPEN. By Lemma 4, $F(n) \le C^*$, and by Fact 2, $F(n) = g(n)$. By Fact 1, the path by the parents is a path from $s_0$ to $n$ of cost at most $g(n) \le C^*$. Every path to a goal costs at least $C^*$, so it costs $C^*$. $\square$

**Theorem 6 (no surplus nodes).** If a goal is reachable, each state stored at line L11 has $f \le C^* + C$. With $C = 0$, no state with $f > C^*$ is ever put in OPEN by line L11.

*Proof.* The state $n$ of line L4 has the least $F$ in OPEN, so by Lemma 4, $F(n) \le C^*$. Line L9 lets a child pass only if $f \le F(n) + C \le C^* + C$. The start has $f = h(s_0) \le C^*$. $\square$

**Theorem 7 (termination).** On a finite graph, the search ends. It returns failure only if no goal is reachable.

*Proof.* Let $\epsilon > 0$ be the least action cost. Each value $g(u)$ is the cost of a path and only falls from the first value it gets, and there are finitely many paths of cost at most that value, as they have at most that value divided by $\epsilon$ actions. So $g(u)$ changes finitely often. While $g(n)$ stays the same, each expansion of $n$ either closes it or sets $F(n)$ to REST, which is above $F(n) + C \ge F(n)$, and REST is the $f$ of one of the finitely many children of $n$ under this $g$. So $n$ is expanded at most $b + 1$ times for each value of $g(n)$, where $b$ is the number of its successors, and there are finitely many expansions in all. Each pass of the loop of line L3 is an expansion or a return, so the search ends. If a goal is reachable, Lemma 4 says that OPEN is never empty before a return, so line L13 is not reached. $\square$

**Theorem 8 (consistent heuristics).** If $h$ is consistent, that is, $h(u) \le c(u, m) + h(m)$ for each action, then each state has $g = g^*$ the first time it is expanded, and its value $g$ never changes after that.

*Proof.* Let $n$ be taken out at line L4 with $g(n) > g^*(n)$, and let $P = (p_0, \ldots, p_t)$ be a cheapest path from $s_0$ to $n$. The proof of Lemma 4, with $P$ in place of $Q$ and $n$ in place of the goal, gives some $p_i$ in OPEN with $g(p_i) = g^*(p_i)$ and $F(p_i) \le g^*(p_j) + h(p_j)$ for $j = i$ or $j = i + 1$, where $i < t$ since $g(n) > g^*(n)$. By consistency, $g^* + h$ does not fall along a cheapest path, so $F(p_i) \le g^*(n) + h(n) < g(n) + h(n) \le F(n)$. Here $F(n) \ge g(n) + h(n)$ because $F$ starts at $f$ and only rises while $g$ stays the same. So $n$ does not have the least $F$, which is a contradiction. So each state is expanded only with $g = g^*$, and by Fact 1 its $g$ cannot fall below $g^*$. $\square$

**Remark.** Theorem 8 gives the bound on the page: with a consistent $h$, each state is expanded at most $b + 1$ times in all, once for each distinct value of $F$ it takes. Without consistency, a state can also be expanded again after its $g$ falls, as in A* with reopening.
