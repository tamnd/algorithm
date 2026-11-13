---
title: Fringe search returns a cheapest path with an admissible heuristic, and expands each state once with a consistent one
proves: [correctness]
status: full
---

We use the pseudocode of the page. Each action cost is positive, each state has finitely many successors, and $h$ is admissible: $0 \le h(u) \le h^*(u)$, where $h^*(u)$ is the cost of a cheapest path from $u$ to a goal, so $h = 0$ at goals. We write $g^*(u)$ for the cost of a cheapest path from $s_0$ to $u$, $C^* = h^*(s_0)$ when a goal is reachable, and $g(u)$ for the value in CACHE. A state is *seen* once it is in CACHE, and $f(u) = g(u) + h(u)$ always uses the current $g(u)$.

**Fact 1 (real paths).** For each seen state $u$, $g(u)$ is the cost of some path from $s_0$ to $u$, so $g(u) \ge g^*(u)$. The value $g(u)$ never rises. The parents in CACHE lead from $u$ back to $s_0$ with no cycle, along a path of cost at most $g(u)$.

*Proof.* Line L2 sets $g(s_0) = 0$, and line L12 sets $g(m) = g(n) + c$ for an action from $n$ to $m$, so by induction $g(m)$ is the cost of a path. Line L9 changes $g(m)$ only to a smaller value. When line L12 sets the parent of $m$ to $n$, $g(m) = g(n) + c > g(n)$, and later $g(n)$ can only fall, so $g(u) > g(\text{parent}(u))$ at all times. So the parents strictly lower $g$ and end at $s_0$, whose value 0 never changes, since a new value would be positive. By induction along the parents, the path costs at most $g(u)$, as each step adds $c(\text{parent}(u), u) \le g(u) - g(\text{parent}(u))$. $\square$

**Fact 2 (the list).** At each moment, a seen state is in FRINGE if and only if it has not been expanded since its value $g$ was last set. A goal state is never expanded.

*Proof.* Lines L11 and L12 put a state in FRINGE and set its value together, line L10 makes sure it is in the list only once, and line L13 takes a state out of FRINGE right after its expansion. Line L7 returns before a goal could be expanded. $\square$

**Lemma 3 (a good state).** Let a goal be reachable and let $Q = (q_0, \ldots, q_k)$ be a cheapest path from $s_0$ to a goal. Until the search returns, FRINGE holds some $q_i$ with $g(q_i) = g^*(q_i)$, so with $f(q_i) \le C^*$.

*Proof.* The prefix of $Q$ that ends in $q_i$ is a cheapest path to $q_i$, so $g^*(q_{i+1}) = g^*(q_i) + c(q_i, q_{i+1})$. Since $g(q_0) = 0 = g^*(q_0)$, let $i$ be the largest index such that $g(q_j) = g^*(q_j)$ for all $j \le i$. If $q_i$ is in FRINGE, we are done. Otherwise, by Fact 2, $q_i$ was expanded after its value was last set, so with $g(q_i) = g^*(q_i)$, since by Fact 1 the value cannot fall below $g^*(q_i)$. In that expansion, line L9 either found $g(q_{i+1}) \le g^*(q_i) + c = g^*(q_{i+1})$ or set it to that value. By Fact 1 it stays $g^*(q_{i+1})$, which contradicts the choice of $i$ when $i < k$. When $i = k$, the state $q_k$ is a goal, which is never expanded by Fact 2, so it is in FRINGE. The bound on $f$ follows from $f(q_i) = g^*(q_i) + h(q_i) \le g^*(q_i) + h^*(q_i) = C^*$, since $q_i$ lies on a cheapest path to a goal. $\square$

**Lemma 4 (the end of a pass).** When a pass ends without a return, each state in FRINGE has $f > $ flim, and fmin is at most the least of these values. So the next threshold is above the current one and at most the least $f$ in FRINGE.

*Proof.* Line L11 puts a state just after the state $n$ that the pass is at, so the pass visits it later. A state that keeps its place in the list was visited by the pass after its value was last set. At that visit, it was not expanded, since it is still in the list, so line L6 found $f > $ flim and lowered fmin to at most that $f$. Its value has not changed since, or line L11 would have moved it. So fmin is at most the current $f$ of each state in FRINGE. Each value that line L6 takes into fmin is above flim. $\square$

**Theorem 5 (optimality).** If a goal is reachable and the search returns, it returns a path from $s_0$ to a goal of cost $C^*$, and its reported cost is $C^*$.

*Proof.* The first threshold is $h(s_0) \le C^*$. If a pass with a threshold at most $C^*$ ends without a return, then by Lemmas 3 and 4 the next threshold is at most $f(q_i) \le C^*$. So every threshold is at most $C^*$. Line L7 returns a goal $n$ with $g(n) = f(n) \le $ flim $\le C^*$. By Fact 1 the path by the parents leads from $s_0$ to $n$ and costs at most $g(n)$. Every path to a goal costs at least $C^*$, so the path and $g(n)$ both equal $C^*$. $\square$

**Theorem 6 (termination).** On a finite graph, the search ends. It returns failure only if no goal is reachable.

*Proof.* Let $\epsilon > 0$ be the least action cost. Each value $g(u)$ is the cost of a path, and it only falls from the first value $g_0(u)$ that it gets. Paths of cost at most $g_0(u)$ have at most $g_0(u) / \epsilon$ actions, so there are finitely many, and $g(u)$ changes finitely often. By Fact 2, a state is expanded at most once per value, so there are finitely many expansions in all. Each pass makes finitely many visits, since each visit expands a state or moves past it, and the list grows only at expansions. A pass that expands nothing ends with fmin equal to the least $f$ in FRINGE, by Lemma 4 and line L6, so the next pass expands that state or returns. So there are finitely many passes, and the search ends. If a goal is reachable, Lemma 3 says that FRINGE is never empty, so the loop of line L3 does not end, and the search returns at line L7. $\square$

**Theorem 7 (consistent heuristics).** Let $h$ be consistent: $h(u) \le c(u, m) + h(m)$ for each action. Then each state expanded in a pass with the threshold flim has $f = $ flim when it is expanded, and no state is expanded twice.

*Proof.* By Lemma 4, at the start of a pass each state in FRINGE has $f \ge $ flim. This holds for the first pass too, where the list is $(s_0)$ and flim $= f(s_0)$. A child put in the list at line L11 has $f(m) = g(n) + c + h(m) \ge g(n) + h(n) = f(n)$. So by induction over the pass, each state that the pass expands has $f \ge $ flim, and line L6 expands it only if $f \le $ flim, so $f = $ flim. Now suppose that a state $u$ is expanded in a pass with the threshold $T_1$ and later gets a smaller value $g'(u)$ from the expansion of a state $v$ in a pass with the threshold $T_2 \ge T_1$. Then $f(v) \le g'(u) + h(u) < g(u) + h(u) = T_1$, by consistency and because the value of $u$ fell. But $v$ was expanded with $f(v) = T_2 \ge T_1$. This is a contradiction, so the value of an expanded state never changes, and by Fact 2 it is never put in the list again. $\square$

**Remark.** With an admissible $h$ that is not consistent, a pass can expand a state, then expand a state of smaller $f$ that gives it a cheaper path, and expand it again, as in the second example of the page. Theorems 5 and 6 still hold, since they use only admissibility.
