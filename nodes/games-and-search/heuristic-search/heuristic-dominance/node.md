---
tag: Y12ZFE
kind: definition
slug: heuristic-dominance
name: Heuristic dominance
aliases:
- more informed heuristic
area: games-and-search/heuristic-search
level: core
summary: An admissible heuristic h2 dominates another one h1 when h2(n) is at least h1(n) at every state. Then A* with h2 expands only states that A* with h1 also expands, up to ties at the optimal cost.
prereqs: [admissible-heuristic, a-star-search]
see_also: [a-star-optimality, consistent-heuristic, effective-branching-factor, relaxation-heuristic, pattern-database, sliding-tile-puzzle, optimal-efficiency-of-a-star, weighted-a-star]
sources:
  - paper: doi:10.1109/TSSC.1968.300136
    title: Peter E. Hart, Nils J. Nilsson and Bertram Raphael, A formal basis for the heuristic determination of minimum cost paths, IEEE Transactions on Systems Science and Cybernetics 4(2) (1968)
    locator: pp. 100 to 107 (the definition of one version of A* as more informed than another, and the result that the more informed version expands no state that the other one does not expand)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 3 (the conditions for node expansion and the comparison of heuristics by how informed they are)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.6.1 (the effect of heuristic accuracy on performance, dominance of the Manhattan distance over the misplaced tiles, and the maximum of several admissible heuristics)
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications
    locator: Chapter 2 (A* and the properties of admissible and consistent heuristics)
---

Heuristic dominance compares two [admissible heuristics](/admissible-heuristic/) for the same problem. If $h_2(n) \ge h_1(n)$ at every state $n$, then $h_2$ dominates $h_1$: it is everywhere at least as close to the true cost $h^*$ from below. The definition matters because of a theorem about [A*](/a-star-search/). If the inequality is strict at each state that is not a goal, A* with $h_2$ expands only states that A* with $h_1$ also expands, for any tie rules. If it is not strict, the same holds except for states whose path cost plus heuristic equals the optimal cost $C^*$, and there the tie rule decides. Hart, Nilsson and Raphael (1968) called the version of A* with the larger heuristic *more informed*. The Manhattan distance of the [sliding tile puzzles](/sliding-tile-puzzle/) dominates the number of misplaced tiles, and on the same instances A* with it expands far fewer states.

## Definition

Let $h_1$ and $h_2$ be admissible heuristics for the same [state-space search](/state-space-search/) problem, so $0 \le h_i(n) \le h^*(n)$ for each state $n$. Then $h_2$ **dominates** $h_1$ if

$$ h_2(n) \ge h_1(n) \quad \text{for every state } n. $$

It dominates $h_1$ **strictly** if $h_2(n) > h_1(n)$ for every state $n$ that is not a goal. Both heuristics are 0 at a goal, so strictness can only be asked at the other states. Hart, Nilsson and Raphael defined "more informed" by the strict form.

Dominance is a partial order on the admissible heuristics of a problem. Its least element is $h = 0$, with which A* is [uniform-cost search](/uniform-cost-search/), and its greatest element is $h^*$. Two admissible heuristics need not be comparable.

The facts below use the setting of the page [optimality of A*](/a-star-optimality/): finite branching, nonnegative costs, a finite space or costs of at least some $\delta > 0$, and $C^* < \infty$. Write $E(h)$ for the set of states that A* with $h$ expands. The goal that A* returns is removed from OPEN but not expanded, so it is not in $E(h)$.

**Fact 1 (path lemma).** Let $h$ be admissible. If A* with $h$ expands a state $n$, then there is a path $P$ from $s_0$ to $n$ with no goal on it and with $g_P(m) + h(m) \le C^*$ for each state $m$ on $P$, where $g_P(m)$ is the cost of $P$ up to $m$.

*Proof.* Let $q_0 = s_0, q_1, \ldots, q_k = n$ be the chain of parent pointers of $n$ at the moment that A* removes $n$, and let $P$ be this path. For $i < k$, the pointer of $q_{i+1}$ was set when $q_i$ was expanded. Call $\gamma_i$ the value of $g[q_i]$ at that expansion. A* sets $g$ and the pointer of a state together, and the pointer of $q_{i+1}$ has not changed since, so $g[q_{i+1}] = \gamma_i + c(q_i, q_{i+1})$ now. The values of $g$ only go down, so $g[q_i] \le \gamma_i$ now. By induction on $i$, $g_P(q_i) \le g[q_i]$: it holds for $q_0$, and $g_P(q_{i+1}) = g_P(q_i) + c(q_i, q_{i+1}) \le \gamma_i + c(q_i, q_{i+1}) = g[q_{i+1}]$. Each time A* removes a state, OPEN holds a state with $f \le C^*$ by the lemma of the optimality page, so each removed state has $f \le C^*$. This gives $g_P(q_i) + h(q_i) \le \gamma_i + h(q_i) \le C^*$ for $i < k$, and $g_P(n) + h(n) \le g[n] + h(n) \le C^*$. Each $q_i$ was expanded, and A* stops when it removes a goal, so no $q_i$ is a goal. $\square$

**Fact 2 (strict dominance).** If $h_2$ dominates $h_1$ strictly, then $E(h_2) \subseteq E(h_1)$, whatever the tie rules of the two runs are.

*Proof.* Let $n \in E(h_2)$ and let $P$ be the path of Fact 1 for $h_2$. No state on $P$ is a goal, so $h_1(m) < h_2(m)$ and $g_P(m) + h_1(m) < g_P(m) + h_2(m) \le C^*$ for each $m$ on $P$. By the sufficient condition, part 3 of the theorem on the optimality page, A* with $h_1$ expands $n$. $\square$

**Fact 3 (dominance that is not strict).** Let $h_2$ dominate $h_1$. If $n \in E(h_2)$ but $n \notin E(h_1)$, then the path $P$ of Fact 1 for $h_2$ has a state $m$ with $g_P(m) + h_1(m) = g_P(m) + h_2(m) = C^*$. If both heuristics are also [consistent](/consistent-heuristic/), then $n$ itself has $g^*(n) + h_1(n) = g^*(n) + h_2(n) = C^*$.

*Proof.* On $P$, $g_P(m) + h_1(m) \le g_P(m) + h_2(m) \le C^*$. If the first sum were below $C^*$ at each $m$, part 3 would make A* with $h_1$ expand $n$. So it equals $C^*$ at some $m$, and then both sums do. For consistent heuristics, part 5 of the theorem says that A* with $h_2$ expands no state with $g^*(n) + h_2(n) > C^*$ and that A* with $h_1$ expands each state with $g^*(n) + h_1(n) < C^*$. So $C^* \le g^*(n) + h_1(n) \le g^*(n) + h_2(n) \le C^*$. $\square$

So the dominating heuristic can expand more states only on the contour $f = C^*$, where the tie rule decides the order.

**Fact 4 (maximum).** If $h_1, \ldots, h_k$ are admissible, then $h = \max(h_1, \ldots, h_k)$ is admissible and dominates each $h_i$. If each $h_i$ is consistent, then $h$ is consistent.

*Proof.* The maximum of lower bounds on $h^*(n)$ is a lower bound. For an action from $n$ to $n'$ of cost $c$, $h_i(n) \le c + h_i(n') \le c + h(n')$ for each $i$, so $h(n) \le c + h(n')$. $\square$

The sum of admissible heuristics is not admissible in general: $h^* + h^* = 2h^*$ overestimates. It is admissible when the heuristics count disjoint sets of moves, as for the tiles in the Manhattan distance or for disjoint additive [pattern databases](/pattern-database/).

## Examples and non-examples

- **The graph of the A* page.** The page [A* search](/a-star-search/) runs A* on one graph with $h = 0$, with the Manhattan distance and with $h^*$, and the expanded sets are $\{S, F, A, B, D, C, E\} \supseteq \{S, A, D, B, C\} \supseteq \{S, B, C\}$. The Manhattan distance is positive at each state other than the goal, so Fact 2 gives the first inclusion for any tie rule. The perfect $h^*$ equals the Manhattan distance at B, C and E, so only Fact 3 applies to the second inclusion. The state D, which A* with the Manhattan distance expands and A* with $h^*$ does not, has $g^*(D) + h(D) = 5 + 2 = 7 = C^*$. With the Manhattan distance, the tie rule of that page, which prefers the larger $g$, expands S, A, D, B, C. A tie rule that prefers goals and then the first name in alphabetical order expands only S, A, B, C.
- **Misplaced tiles and the Manhattan distance on the 8-puzzle.** Let $h_{\text{mis}}$ count the tiles that are not on their goal squares, and let $h_{\text{man}}$ sum the Manhattan distances of the tiles to their goal squares, the blank not counted. A misplaced tile is at least one square from its goal square, so $h_{\text{man}}$ dominates $h_{\text{mis}}$. The dominance is not strict: among the 181,440 states that can reach the goal $(1, 2, 3, 4, 5, 6, 7, 8, \text{blank})$, 248 states other than the goal have $h_{\text{mis}} = h_{\text{man}}$, those in which each misplaced tile is one square from its goal square. Both heuristics are consistent, so Fact 3 applies.
- **Measured counts.** For each depth $d$, the table uses 20 states at distance $d$ from the goal above, drawn with Python's `random.Random(1)` from the sorted list of the states at that distance, one generator for all depths in order. The search is the implementation of the A* page, with ties broken toward the larger $g$. $N$ is the number of entries put in OPEN, the start not counted, averaged over the 20 instances. The [effective branching factor](/effective-branching-factor/) $b^*$ is solved from the mean $N$ by bisection to a tolerance of $10^{-6}$. The expansions are totals over the 20 instances.

| $d$ | mean $N$, misplaced | mean $N$, Manhattan | $b^*$, misplaced | $b^*$, Manhattan | expansions, misplaced | expansions, Manhattan | instances where Manhattan expands an extra state | extra states |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | 15.15 | 13.1 | 1.2724 | 1.2284 | 149 | 127 | 0 | 0 |
| 8 | 26.65 | 17.95 | 1.2660 | 1.1783 | 278 | 182 | 0 | 0 |
| 12 | 131.1 | 44.5 | 1.3432 | 1.1908 | 1,523 | 488 | 2 | 6 |
| 16 | 651.8 | 129.45 | 1.3844 | 1.2211 | 7,955 | 1,525 | 2 | 5 |
| 20 | 3,815.6 | 515.15 | 1.4213 | 1.2642 | 47,244 | 6,313 | 11 | 95 |

The dominating heuristic has the smaller $b^*$ and fewer expansions at each depth, and at depth 20 it expands about 7.5 times fewer states. The set of states that it expands is not always a subset of the other one: at depths 12, 16 and 20 some instances have extra states. Each of these 106 extra states has $g^*(n) + h_{\text{mis}}(n) = g^*(n) + h_{\text{man}}(n) = d = C^*$, as Fact 3 says.

- **A tie that the larger heuristic loses.** Take the arcs S to P of cost 1, S to X of cost 2, P to G of cost 3 and X to G of cost 10, with the goal G and $C^* = 4$. Let $h_1(S, P, X, G) = (3, 2, 2, 0)$ and $h_2(S, P, X, G) = (4, 3, 2, 0)$. Both are consistent and $h_2 \ge h_1$, with equality at X. With ties toward the larger $g$, A* with $h_1$ expands S and P, with $f$ values 3 and 3. A* with $h_2$ expands S, X and P, all with $f = 4$, because X and P tie at $f = 4$ and X has the larger $g$. The state X has $g^*(X) + h_1(X) = 2 + 2 = 4 = C^*$. Both runs return S, P, G of cost 4.
- **Heuristics that cross.** With the same goal, let $h_A$ be the sum of the Manhattan distances of the tiles 1 to 4 and $h_B$ that of the tiles 5 to 8. Both are admissible. On the state $(1, 2, 3, 4, 5, 6, 7, \text{blank}, 8)$, $h_A = 0$ and $h_B = 1$. On the state $(\text{blank}, 1, 2, 4, 5, 3, 7, 8, 6)$, $h_A = 3$ and $h_B = 1$. So neither dominates the other. By Fact 4, $\max(h_A, h_B)$ dominates both. Each move changes the position of one tile only, so here the sum $h_A + h_B = h_{\text{man}}$ is also admissible, and it dominates the maximum.
- **Not dominance: a heuristic that overestimates.** The function $2 h_{\text{man}}$ is at least $h_{\text{man}}$ at every state, but it is not admissible: on the state $(1, 2, 3, 4, 5, 6, 7, \text{blank}, 8)$, one move from the goal, it is 2. Dominance is defined only between admissible heuristics, and the facts above do not hold for it. A* with such a heuristic is [weighted A*](/weighted-a-star/), which can return a path that costs more than $C^*$.
- **Fewer expansions is not less time.** Dominance compares the number of states expanded, not the time per state. The heuristic $h^*$ dominates every admissible heuristic, but to compute it is to solve the problem. A [pattern database](/pattern-database/) gives a larger heuristic than the Manhattan distance for one table lookup per state, but it needs memory and a search to build the table. The total work is the number of expansions times the cost of one expansion, the heuristic included.

## Related definitions

- **[Admissible heuristic](/admissible-heuristic/).** A heuristic with $h \le h^*$. Dominance is a relation between two of them.
- **[Consistent heuristic](/consistent-heuristic/).** A heuristic with $h(n) \le c(n, n') + h(n')$. For consistent heuristics the expanded sets differ only on the contour $f = C^*$, by Fact 3.
- **[Effective branching factor](/effective-branching-factor/).** A measured number that sums up the work of a run. A dominating heuristic gives a smaller value on the same instances, up to ties.
- **[Relaxation heuristic](/relaxation-heuristic/).** The cost of an optimal solution of a problem with fewer constraints. If one relaxed problem has all the actions of another and more, its distances are no longer, so the heuristic of the less relaxed problem dominates.
- **[Pattern database](/pattern-database/).** For abstractions in which one refines the other, the heuristic of the finer abstraction dominates that of the coarser one.
- **[Optimal efficiency of A*](/optimal-efficiency-of-a-star/).** It compares algorithms that use the same heuristic. Dominance compares heuristics that are used by the same algorithm.

## References
