---
tag: ZX2TRR
kind: definition
slug: consistent-heuristic
name: Consistent heuristic
aliases:
- monotone heuristic
- monotonic heuristic
area: games-and-search/heuristic-search
level: core
summary: A heuristic with h(n) <= c(n, n') + h(n') for each action and h = 0 at goals. It is admissible, it makes f nondecreasing along paths, and A* with it never reopens a state.
prereqs: [admissible-heuristic, triangle-inequality]
see_also: [a-star-search, a-star-optimality, pathmax, potential-function-reduced-costs, heuristic-dominance, optimal-efficiency-of-a-star, graph-search-vs-tree-search, alt-algorithm]
sources:
  - paper: doi:10.1109/TSSC.1968.300136
    title: Peter E. Hart, Nils J. Nilsson and Bertram Raphael, A formal basis for the heuristic determination of minimum cost paths, IEEE Transactions on Systems Science and Cybernetics 4(2) (1968)
    locator: pp. 100 to 107 (the consistency assumption h(m) <= h*(m, n) + h(n) and its use in the optimality of A*)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 3 (the monotone restriction, its equivalence with consistency, and its consequences for A*)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.5.2 (consistency as a triangle inequality, consistent implies admissible, and A* with a consistent heuristic)
  - paper: doi:10.1016/j.artint.2011.02.001
    title: Ariel Felner, Uzi Zahavi, Robert Holte, Jonathan Schaeffer, Nathan Sturtevant and Zhifu Zhang, Inconsistent heuristics in theory and practice, Artificial Intelligence 175(9-10) (2011)
    locator: Section 3 (consistent and inconsistent heuristics, the monotonicity of f, and the reopening of nodes) and Section 6 (sources of inconsistent heuristics)
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications
    locator: Chapter 2 (consistent heuristics, the reweighting of edges, and A* as Dijkstra's algorithm on the reweighted graph)
---

A [heuristic function](/heuristic-function/) $h$ is *consistent* if it never drops by more than the cost of an action: $h(n) \le c(n, n') + h(n')$ for each action from $n$ to $n'$, and $h(t) = 0$ for each goal $t$. This is a [triangle inequality](/triangle-inequality/) between the estimate at $n$, the action, and the estimate at $n'$. A consistent heuristic is [admissible](/admissible-heuristic/), but not each admissible heuristic is consistent. Consistency is what makes [A*](/a-star-search/) simple: with it, the values $f = g + h$ never go down along a path, each state leaves OPEN with its least cost, and no state is expanded twice. Pearl called the same condition the *monotone restriction*, which is the source of the aliases.

## Definition

Let a state space have nonnegative action costs $c(n, n')$ and a set of goal states, and let $d(u, v)$ be the cost of a cheapest path from $u$ to $v$, with $d(u, v) = \infty$ when there is none. A function $h$ from states to the nonnegative reals, or to $\infty$, is **consistent** if

$$ h(n) \le c(n, n') + h(n') \quad \text{for each action } n \to n', \qquad h(t) = 0 \quad \text{for each goal } t. $$

The *global form* is $h(u) \le d(u, v) + h(v)$ for all states $u$ and $v$. It is the form of the consistency assumption of Hart, Nilsson and Raphael.

**Fact 1 (the two forms are the same).** The edge form holds if and only if the global form holds.

*Proof.* The global form gives the edge form, since $d(n, n') \le c(n, n')$. For the other way, let $u = u_0, u_1, \ldots, u_k = v$ be a cheapest path. Adding $h(u_{i-1}) \le c(u_{i-1}, u_i) + h(u_i)$ for $i = 1, \ldots, k$ gives $h(u) \le d(u, v) + h(v)$. If no path exists, $d(u, v) = \infty$ and there is nothing to show. $\square$

**Fact 2 (consistent implies admissible).** If $h$ is consistent, then $h(n) \le h^*(n)$ for each state $n$, where $h^*(n) = \min_t d(n, t)$ over the goals $t$.

*Proof.* Take $v = t$ a goal in the global form, so $h(n) \le d(n, t) + 0$, and take the least over $t$. $\square$

**Fact 3 (f is monotone).** If $h$ is consistent, then along each path $n_0, n_1, \ldots$ the values $f(n_i) = g(n_i) + h(n_i)$, with $g$ the cost of the path up to $n_i$, do not go down.

*Proof.* $f(n_{i+1}) = g(n_i) + c(n_i, n_{i+1}) + h(n_{i+1}) \ge g(n_i) + h(n_i) = f(n_i)$. $\square$

Felner et al. (2011, Section 3) stress the difference between the two words. Consistency is a property of $h$, and monotonicity is a property of $f$ along a path. On an undirected graph the edge form applies in both directions and becomes $|h(n) - h(n')| \le c(n, n')$.

**Fact 4 (consistent means reduced costs are nonnegative).** $h$ is consistent if and only if the reduced costs $c_h(n, n') = c(n, n') - h(n) + h(n')$ are all nonnegative and $h = 0$ at the goals. A* with $h$ is then [Dijkstra's algorithm](/dijkstra/) with the costs $c_h$, and the cost of each path from $s_0$ to $v$ changes by the same amount $h(v) - h(s_0)$. The page [potential functions and reduced costs](/potential-function-reduced-costs/) proves this.

**Fact 5 (closure).** If $h_1$ and $h_2$ are consistent, so are $\max(h_1, h_2)$, $\min(h_1, h_2)$ and $\lambda h_1 + (1 - \lambda) h_2$ for $0 \le \lambda \le 1$. The function $h = 0$ and the perfect heuristic $h^*$ are consistent.

*Proof.* For the maximum, $h_i(n) \le c(n, n') + h_i(n') \le c(n, n') + \max(h_1, h_2)(n')$ for $i = 1, 2$, so the inequality holds for the larger of the two left sides. The minimum is the same with the roles turned, and the convex combination adds the two inequalities with weights. For $h^*$, a cheapest path from $n'$ to a goal, with the action $n \to n'$ in front, is a path from $n$ that costs $c(n, n') + h^*(n')$. $\square$

## Examples and non-examples

- **Manhattan distance on a grid.** On a 4-connected grid with unit costs, a move changes the Manhattan distance to the goal by exactly 1, so it is consistent. With cell costs at least $c_{\min}$, $c_{\min}$ times the Manhattan distance is consistent.
- **Straight-line distance on a road map.** For a road of length $c(u, v)$, the straight-line distances to the goal satisfy $\lVert u - t \rVert \le \lVert u - v \rVert + \lVert v - t \rVert \le c(u, v) + \lVert v - t \rVert$, by the triangle inequality in the plane and because no road is shorter than the straight line between its ends.
- **Sliding-tile puzzles.** A move shifts one tile by one place. The number of misplaced tiles changes by at most 1, and the Manhattan sum of the tiles changes by exactly 1, so both are consistent. So is the maximum of several [pattern databases](/pattern-database/), by Fact 5. A pattern database built by a search of its abstract space is consistent, because each action of the real space maps to an action of the abstract space or to no move.
- **Landmarks.** The heuristic $|d(L, t) - d(L, n)|$ of the [ALT algorithm](/alt-algorithm/) for a landmark $L$ on an undirected graph is consistent by the triangle inequality of $d$.
- **Admissible but not consistent.** The directed graph has the actions S→A 1, S→B 3, A→B 1, B→C 1, C→G 1 and the goal G, with $h(S) = 0$, $h(A) = 3$, $h(B) = h(C) = h(G) = 0$. The true costs to the goal are $h^* = 4, 3, 2, 1, 0$, so $h$ is admissible. At the action A→B, $h(A) = 3 > 1 + h(B) = 1$, so it is not consistent. A* first reaches B by S→B with $g = 3$ and expands it with $f = 3$, before A, which has $f = 4$. When it later expands A, it finds the path S-A-B with $g = 2$. A* that reopens B goes on and returns S-A-B-C-G of cost 4, after 6 expansions, B and C twice each. A* that keeps B closed returns S-B-C-G of cost 5. The values of $f$ of the expanded states are 0, 3, 4, 4, 2, 3, which is not monotone.
- **The edge inequality alone is not enough.** The constant $h = 5$ satisfies $h(n) \le c(n, n') + h(n')$ for each action, but it is not 0 at the goal, and it is not admissible on a graph with $C^* < 5$. The condition at the goals is part of the definition.
- **Sources of inconsistency.** Felner et al. (2011, Section 6) list heuristics that are admissible and often inconsistent: a random choice among several pattern databases at each state, a compressed pattern database that stores one value for several entries, and the dual lookup of a pattern database. A heuristic that a program learns, or that it takes from a table with errors, is usually not consistent either.

## Related definitions

- **[Admissible heuristic](/admissible-heuristic/).** The weaker condition $h \le h^*$. It is enough for A* to return a cheapest path when it may reopen states, but not for A* without reopening.
- **Monotone f, and [pathmax](/pathmax/).** Pathmax raises $h$ of a child to $h(\text{parent}) - c$ when that is larger, so $f$ does not go down from a parent to a child. This is weaker than consistency: A* with pathmax still reopens B and C in the example above, as the page on pathmax shows.
- **Type 1 and type 2 inconsistency.** In the terms of Felner et al., $h$ can drop too much from a parent to a child (type 1, which pathmax repairs) or rise too much (type 2, which matters on undirected graphs and which bidirectional pathmax uses).
- **[Heuristic dominance](/heuristic-dominance/).** A comparison of two heuristics. By Fact 5, the maximum of consistent heuristics dominates each of them and is still consistent.
- **[Potential function](/potential-function-reduced-costs/).** A consistent $h$ is a feasible potential for the reversed problem: the reduced costs are nonnegative. The same idea gives Johnson's reweighting for all pairs shortest paths.
- **[Optimal efficiency of A*](/optimal-efficiency-of-a-star/).** With a consistent $h$, no admissible algorithm with the same information can avoid the states that A* must expand. Without consistency this fails.

## References
