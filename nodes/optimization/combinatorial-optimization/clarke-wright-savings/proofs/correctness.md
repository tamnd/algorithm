---
title: The savings algorithm returns feasible routes whose cost is the start cost minus the applied savings, and no feasible positive merge remains
proves: [correctness, termination, maximality]
status: full
---

Let the costs be symmetric, $c(i, j) = c(j, i)$, and let $0 \le q_i \le Q$ for every customer $i$. A *route* is a sequence $(i_1, \ldots, i_k)$ of distinct customers, $k \ge 1$, driven as $0, i_1, \ldots, i_k, 0$. Its cost is $c(0, i_1) + \sum_{t<k} c(i_t, i_{t+1}) + c(i_k, 0)$, its load is $\sum_t q_{i_t}$, and its *ends* are $i_1$ and $i_k$. Write $s(i, j) = c(0, i) + c(0, j) - c(i, j)$ and $C_0 = 2 \sum_{i=1}^n c(0, i)$.

**Invariant.** Before each iteration of line L2 the current routes satisfy:

> **(P)** every customer is on exactly one route;
>
> **(L)** every route has load at most $Q$;
>
> **(C)** the total cost is $C_0 - \sum_{m \in M} s(m)$, where $M$ is the list of pairs merged so far.

*Initialization.* Line L1 makes the $n$ routes $(i)$. Each customer is on one route, each load is $q_i \le Q$, and the total cost is $\sum_i 2 c(0, i) = C_0$ with $M$ empty.

*Maintenance.* If one of lines L3 to L6 rejects the pair, nothing changes. Otherwise $i$ is an end of a route $A$, $j$ is an end of a different route $B$, and $\mathrm{load}(A) + \mathrm{load}(B) \le Q$. Line L7 reverses $A$ if needed so that $A = (a_1, \ldots, a_k)$ with $a_k = i$, and reverses $B$ if needed so that $B = (b_1, \ldots, b_m)$ with $b_1 = j$. A reversal does not change the cost, because the costs are symmetric, and it does not change the load. Line L8 forms $(a_1, \ldots, a_k, b_1, \ldots, b_m)$. The customers of $A$ and $B$ are distinct, since $A \ne B$ and (P) held, so the result is a route and (P) holds. Its load is $\mathrm{load}(A) + \mathrm{load}(B) \le Q$, so (L) holds. The new route uses all edges of $A$ and $B$ except $(a_k, 0)$ and $(0, b_1)$, and adds $(a_k, b_1) = (i, j)$. So the total cost changes by $c(i, j) - c(i, 0) - c(0, j) = -s(i, j)$, and (C) holds with $(i, j)$ appended to $M$. $\square$

**Lemma 1 (termination).** The algorithm stops after at most $n(n-1)/2$ iterations of line L2, and makes at most $n - 1$ merges.

*Proof.* Line L2 runs over a finite list. Each merge lowers the number of routes by one, and the number is at least 1 while $n \ge 1$. $\square$

**Lemma 2 (monotone ends).** Once a customer is not an end of its route, it is never an end again. Two customers on the same route stay on the same route. The load of the route of a customer never decreases.

*Proof.* A merge in line L8 changes only the routes $A$ and $B$. The ends of the new route are $a_1$ and $b_m$, which were ends of $A$ and $B$. Every interior customer of $A$ or $B$ stays interior, and $i$ and $j$ become interior (or, if $A = (i)$ or $B = (j)$, the customer stays an end only as $a_1$ or $b_m$). So the set of ends only shrinks. The other claims follow because routes are only joined, never split, and demands are non-negative. $\square$

**Theorem.** The output is a feasible solution of the capacitated vehicle routing problem, with cost $C_0 - \sum_{m \in M} s(m) \le C_0$. Moreover, there is no pair $(i, j)$ with $s(i, j) > 0$ such that $i$ and $j$ are ends of two different output routes whose loads add up to at most $Q$.

*Proof.* By Lemma 1 the algorithm stops. By the invariant, the output satisfies (P), (L) and (C), which is feasibility and the cost formula. Every merged pair passed line L3, so $s(m) > 0$ for $m \in M$, and the cost is at most $C_0$.

For the last claim, suppose that such a pair $(i, j)$ exists. Since $s(i, j) > 0$ and the list is in decreasing order of saving, line L3 did not stop the loop before the pair, so the pair was examined. By Lemma 2, at that time $i$ and $j$ were ends (they are ends at the end), they were on different routes (they are on different routes at the end), and the loads of their routes were at most the final loads, so their sum was at most $Q$. So lines L4, L5 and L6 all passed, and line L8 merged the two routes, which put $i$ and $j$ on the same route. By Lemma 2 they stay on the same route, which contradicts the assumption. $\blacksquare$
