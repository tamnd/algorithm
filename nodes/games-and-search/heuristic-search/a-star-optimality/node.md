---
tag: QFQ6NX
kind: theorem
slug: a-star-optimality
name: Optimality of A*
aliases:
- A* optimality theorem
area: games-and-search/heuristic-search
level: core
summary: With an admissible heuristic, finite branching and costs bounded below by a positive number, A* returns a cheapest solution. With a consistent heuristic, it expands no state twice.
prereqs: [a-star-search, admissible-heuristic, consistent-heuristic]
see_also: [optimal-efficiency-of-a-star, heuristic-dominance, pathmax, completeness-and-optimality-of-search, graph-search-vs-tree-search, weighted-a-star, dijkstra, uniform-cost-search]
sources:
  - paper: doi:10.1109/TSSC.1968.300136
    title: Peter E. Hart, Nils J. Nilsson and Bertram Raphael, A formal basis for the heuristic determination of minimum cost paths, IEEE Transactions on Systems Science and Cybernetics 4(2) (1968)
    locator: pp. 100 to 107 (the lemma that OPEN holds a state of an optimal path with f at most the optimal cost, and the theorem that A* is admissible)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 3 (formal properties of A*, its termination, admissibility and the conditions for node expansion)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.5.2 (the cost optimality of A* with an admissible heuristic, and the contours of a consistent heuristic)
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications
    locator: Chapter 2 (the correctness of A* with admissible and with consistent heuristics)
---

The optimality theorem of [A*](/a-star-search/) says that A* with an [admissible heuristic](/admissible-heuristic/) returns a cheapest path to a goal. It needs three conditions besides $h \le h^*$: each state has finitely many successors, each action costs at least some $\delta > 0$ (or the graph is finite), and a state that is reached again by a cheaper path goes back into OPEN. With a [consistent heuristic](/consistent-heuristic/) the last condition is never used, because each state leaves OPEN with its optimal cost. The same proof tells which states A* must expand and which it cannot: all states with $g^* + h < C^*$ on the right paths must be expanded, and no state with $g^* + h > C^*$ is. This page is about the solution that A* returns. The page [optimal efficiency of A*](/optimal-efficiency-of-a-star/) is about the number of states that it expands compared with other algorithms.

## Statement

Let a [state-space search](/state-space-search/) problem have a start $s_0$, a goal set $G$, nonnegative action costs and finitely many successors at each state. Let $g^*(n)$ and $h^*(n)$ be the costs of a cheapest path from $s_0$ to $n$ and from $n$ to a goal, and let $C^* = h^*(s_0) < \infty$. A* is the algorithm of the page [A* search](/a-star-search/): it removes a state of least $f = g + h$ from OPEN, tests for a goal when a state is removed, and puts a state back in OPEN when it finds a cheaper path to it.

**Theorem.** Let $h$ be admissible, and let the state space be finite or each action cost be at least some $\delta > 0$.

1. **(Optimal solution.)** A* stops, and it returns a path from $s_0$ to a goal of cost $C^*$.
2. **(Necessary condition.)** Each state $n$ that A* expands has $g^*(n) + h(n) \le C^*$.
3. **(Sufficient condition.)** If a path $P$ from $s_0$ to a state $n$ has $g_P(m) + h(m) < C^*$ for each state $m$ on $P$, where $g_P(m)$ is the cost of $P$ up to $m$, then A* expands $n$.

If $h$ is also consistent, then:

4. **(No reopening.)** Each state that A* removes from OPEN has $g = g^*$ at that moment, so no state is expanded twice.
5. **(Contours.)** A* expands each state with $g^*(n) + h(n) < C^*$ and no state with $g^*(n) + h(n) > C^*$.

## In plain words

An admissible heuristic never says that the goal is farther away than it is. So the path that A* will take to the cheapest goal always looks at least as good as it is, and the search can not settle for a worse goal while a piece of that path is still waiting.

The same reasoning tells which states the search must look at. A state that looks cheaper than the best answer, by the cost so far plus the estimate, must be looked at. A state that looks more expensive is never looked at.

## Proof

Two facts about the bookkeeping of A* are proved on the page [A* search](/a-star-search/): $g[n]$ only goes down, and the parent pointers form a tree rooted at $s_0$ in which the path to $n$ costs at most $g[n]$. Each value $g[n]$ is the cost of some path from $s_0$ to $n$, so $g[n] \ge g^*(n)$. A state $n$ is *settled* if it is in CLOSED with $g[n] = g^*(n)$. A settled state is never reopened, because its $g$ can not drop further.

**Lemma.** Let $P = (p_0 = s_0, p_1, \ldots, p_k)$ be a cheapest path from $s_0$ to a state $p_k$. At each moment at the start of the main loop, either all states of $P$ are settled, or the first state $p_j$ of $P$ that is not settled is in OPEN with $g[p_j] = g^*(p_j)$.

*Proof.* At the start $p_0 = s_0$ is in OPEN with $g = 0$. Let $j \ge 1$. The state $p_{j-1}$ is settled, so it was expanded with $g[p_{j-1}] = g^*(p_{j-1})$. At that expansion $p_j$ got $g[p_j] \le g^*(p_{j-1}) + c(p_{j-1}, p_j) = g^*(p_j)$, since a prefix of a cheapest path is a cheapest path. So $g[p_j] = g^*(p_j)$ from then on. The expansion either put $p_j$ in OPEN or found it in OPEN or in CLOSED with this $g$ already. It is not settled, so it is not in CLOSED with this $g$, and it can only leave OPEN by an expansion, which would settle it. So it is in OPEN. $\square$

**Corollary.** Let $P$ be a cheapest path from $s_0$ to a goal. While no state of $P$ after the last settled one has been removed, OPEN holds a state $p$ with $f(p) = g^*(p) + h(p) \le g^*(p) + h^*(p) = C^*$. So the least $f$ in OPEN is at most $C^*$ until a goal is removed.

*Part 2.* Before a goal is removed, A* removes a state of least $f$, so by the corollary each expanded $n$ has $g^*(n) + h(n) \le g[n] + h(n) \le C^*$.

*Part 1.* If the space is finite, A* stops, because each value of $g[n]$ is the cost of a path without repeated states, there are finitely many such paths, and each new expansion of $n$ uses a smaller value of $g[n]$. If each action costs at least $\delta$, then by part 2 each expanded state has $g[n] \le C^*$, so it is reached by a path of at most $C^* / \delta$ actions. With finite branching there are finitely many such paths, so again A* makes finitely many expansions. It does not return failure, since by the lemma OPEN is not empty before the goal of $P$ is removed. So it stops by removing a goal $t$. Then $h(t) = 0$, because $0 \le h(t) \le h^*(t) = 0$, and by the corollary $g[t] = f(t) \le C^*$. The path of parent pointers from $s_0$ to $t$ costs at most $g[t] \le C^*$, and it is a solution, so it costs exactly $C^*$.

*Part 3.* By part 1, A* stops when it removes a goal $t$ with $f(t) = C^*$. Suppose that $n$ is not expanded by then. Let $m_j$ be the first state of $P = (m_0, \ldots, m_r = n)$ that has not been expanded with $g[m_j] \le g_P(m_j)$. If $j > 0$, then $m_{j-1}$ was, and at that expansion $m_j$ got $g[m_j] \le g_P(m_j)$. If $j = 0$, then $g[s_0] = 0$ from the start. If $m_j$ were in CLOSED now, its last expansion would have been with its current $g$, because a drop of $g$ in CLOSED reopens a state. So $m_j$ is in OPEN with $f(m_j) \le g_P(m_j) + h(m_j) < C^* = f(t)$, and A* would have removed $m_j$ before $t$. This is a contradiction.

*Part 4.* Let $h$ be consistent. Then $h(p) \le c_Q + h(n)$ for each path $Q$ from $p$ to $n$ of cost $c_Q$, by adding the edge inequalities along $Q$. Suppose that A* removes a state $n$ with $g[n] > g^*(n)$. Apply the lemma to a cheapest path $P$ from $s_0$ to $n$. The state $n$ is not settled, so some state $p$ of $P$ is in OPEN with $g[p] = g^*(p)$, and $p \ne n$ because $g[n] \ne g^*(n)$. Let $Q$ be the part of $P$ from $p$ to $n$. Then

$$ f(p) = g^*(p) + h(p) \le g^*(p) + c_Q + h(n) = g^*(n) + h(n) < g[n] + h(n) = f(n), $$

so A* would not remove $n$ before $p$. This is a contradiction.

*Part 5.* The second half is part 2. For the first half, let $g^*(n) + h(n) < C^*$ and let $P$ be a cheapest path from $s_0$ to $n$. For a state $m$ of $P$, with $Q$ the part of $P$ from $m$ to $n$, consistency gives $g^*(m) + h(m) \le g^*(m) + c_Q + h(n) = g^*(n) + h(n) < C^*$. Here $g_P(m) = g^*(m)$, so part 3 applies to $P$, and A* expands $n$. $\square$

## Consequences

- **Dijkstra and uniform-cost search.** $h = 0$ is consistent, so [uniform-cost search](/uniform-cost-search/) returns a cheapest path, expands each state at most once and expands every state with $g^* < C^*$. This is the correctness of [Dijkstra's algorithm](/dijkstra/) stopped at the goal.
- **Weighted A*.** The corollary with $f = g + w h$, $w \ge 1$, gives $f(p) = g^*(p) + w h(p) \le w(g^*(p) + h^*(p)) = w C^*$. So [weighted A*](/weighted-a-star/) returns a path of cost at most $w C^*$.
- **Better heuristics expand fewer states.** Parts 2 and 3 give the sets of states that A* surely expands and that it can expand, and both shrink as $h$ grows. This is the theorem of [heuristic dominance](/heuristic-dominance/).
- **What "optimal" does not mean.** The theorem is about the solution, not about the time. The number of expansions can still be exponential, and with an inconsistent $h$ A* can expand one state many times.
- **Tree search.** The lemma does not need CLOSED, so A* tree search, which keeps no CLOSED set, is also optimal with an admissible $h$ under the same conditions, see [graph search versus tree search](/graph-search-vs-tree-search/).

## Tightness

Each hypothesis is needed.

- **Reopening, when $h$ is not consistent.** Take the arcs S to A of cost 1, S to B of cost 3, A to B, B to C and C to G of cost 1 each, with $h(A) = 3$ and $h = 0$ elsewhere. This $h$ is admissible, since $h^*(A) = 3$, but not consistent, since $h(A) = 3 > c(A, B) + h(B) = 1$. A* expands S, then B with $g = 3$, then C, and puts G in OPEN with $g = 5$. Then it expands A, which lowers $g[B]$ to 2. Without reopening, B is in CLOSED and the search returns G with cost 5. With reopening it expands B and C again and returns cost $C^* = 4$.
- **Admissibility.** Take the arcs S to G of cost 3, S to A of cost 1 and A to G of cost 1, with $h(A) = 5 > h^*(A) = 1$. After S, OPEN holds G with $f = 3$ and A with $f = 6$, so A* returns the path of cost 3, not 2.
- **Goal test at removal.** A search that tests for the goal when it generates a state returns a path of cost 8 instead of 7 on the example of the page [A* search](/a-star-search/).
- **Costs bounded below by $\delta > 0$.** Let $s_0$ have an arc of cost 2 to the goal $t$ and an infinite chain $s_0 \to v_1 \to v_2 \to \cdots$ whose $i$-th arc costs $2^{-i}$, with $h = 0$. Each $v_i$ has $g = 1 - 2^{-i} < 2$, so A* expands the chain forever and never removes $t$. Here part 2 still holds, but the expanded states are not reached by a bounded number of actions.
- **Ties at $f = C^*$.** Parts 2 and 3 leave open the states with $g^* + h = C^*$. In the example of the page on A*, D has $g^*(D) + h(D) = 5 + 2 = 7 = C^*$, and it is expanded only because of the tie rule. A different rule can skip it.

## History

Hart, Nilsson and Raphael (1968) proved that A* is admissible when $h$ is a lower bound on $h^*$, with the lemma about a state of an optimal path in OPEN as the key step. Their proofs assume costs bounded below by a positive number and finite branching. Pearl's book of 1984 gave the conditions for expansion in the form of parts 2 and 3 and the version for consistent heuristics. Dechter and Pearl (1985) extended the conditions to best-first searches with general evaluation functions.

## References
