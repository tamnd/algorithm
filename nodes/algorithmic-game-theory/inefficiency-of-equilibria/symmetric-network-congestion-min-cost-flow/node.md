---
tag: KZRBES
kind: algorithm
slug: symmetric-network-congestion-min-cost-flow
name: Equilibria of symmetric network congestion games by min-cost flow
aliases:
- Fabrikant-Papadimitriou-Talwar algorithm
- min-cost flow algorithm for symmetric network congestion games
area: algorithmic-game-theory/inefficiency-of-equilibria
level: advanced
summary: Finds a pure Nash equilibrium of a symmetric network congestion game by minimizing Rosenthal's potential as a min-cost flow.
model: word-ram
complexity:
  vars: {n: the number of players, m: the number of edges, v: the number of vertices}
  time: {worst: O(n v m)}
  space: {extra: O(v + m)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 2004
  people: [Alex Fabrikant, Christos Papadimitriou, Kunal Talwar]
  note: Fabrikant, Papadimitriou and Talwar gave the reduction to min-cost flow at STOC 2004, in the same paper that proved the general problem PLS-complete; the potential is from Rosenthal 1973.
prereqs: [rosenthal-potential-theorem, min-cost-flow-problem]
see_also: [atomic-congestion-game, pls-completeness-of-congestion-games, successive-shortest-path, cycle-canceling, bellman-ford, best-response-dynamics, braess-paradox, atomic-linear-congestion-price-of-anarchy]
sources:
  - paper: doi:10.1145/1007352.1007445
    title: "Alex Fabrikant, Christos Papadimitriou and Kunal Talwar, The complexity of pure Nash equilibria, Proceedings of the 36th Annual ACM Symposium on Theory of Computing (STOC 2004), 604-612"
    locator: the polynomial algorithm for symmetric network congestion games by reduction to min-cost flow, and the PLS-completeness of the general case
  - paper: doi:10.1007/BF01737559
    title: "Robert W. Rosenthal, A class of games possessing pure-strategy Nash equilibria, International Journal of Game Theory 2 (1973), 65-67"
    locator: the potential function whose minimizers are pure Nash equilibria
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications, Prentice Hall, 1993
    locator: Chapter 9 (the successive shortest path algorithm) and Chapter 14 (convex cost flows)
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 19 (pure Nash equilibria, PLS-completeness and the tractable symmetric routing case)
---

In a symmetric network congestion game, every player sends one unit from the same source $s$ to the same sink $t$ of a directed graph, and the cost of an edge depends on how many players use it. This algorithm finds a pure Nash equilibrium in polynomial time. It builds a flow of value $n$ that minimizes Rosenthal's potential, by successive shortest paths on the marginal terms of the potential, and then splits the flow into $n$ paths. It differs from the [min-cost flow problem](/min-cost-flow-problem/) in its costs: the cost to minimize is the potential, a separable convex function of the loads, not a linear cost per unit, and the answer must be read as a profile of paths. It differs from [cycle canceling](/cycle-canceling/) in method: it never starts from a feasible flow, but grows the flow one unit at a time, as [successive shortest paths](/successive-shortest-path/) does.

## In plain words

Many drivers go from the same start to the same goal. Each road gets slower when more drivers use it, and each driver picks the route that is fastest for that driver. A stable state is one where no driver can change route and arrive sooner. There is a score of the whole traffic such that, when one driver changes route, the score changes by exactly the time that driver gains or loses. So the state with the lowest score is stable. The algorithm finds that state by adding drivers one at a time. Each new driver takes the cheapest route, and the route may move some earlier drivers to other roads. At the end it reads off one route for each driver.

## The problem

The input is a directed graph $G = (V, E)$ with $v = |V|$ and $m = |E|$, a source $s$ and a sink $t \ne s$, a number of players $n \ge 1$, and for each edge $e$ the costs $c_e(1), \ldots, c_e(n)$, where $c_e(j)$ is what each of the $j$ players on $e$ pays. The costs are nonnegative and nondecreasing in $j$. The strategy set of every player is the set of simple directed $s$-$t$ paths, so the game is symmetric. In a profile $P = (P_1, \ldots, P_n)$ the load of $e$ is $x_e$, the number of players whose path uses $e$, and player $i$ pays $c_i(P) = \sum_{e \in P_i} c_e(x_e)$ and minimizes it. The output is a pure Nash equilibrium: a profile where no player can lower its own cost by a change of path while the others stay. One exists by [Rosenthal's theorem](/rosenthal-potential-theorem/), because every minimizer of the potential

$$\Phi(P) = \sum_{e \in E} \sum_{j=1}^{x_e} c_e(j)$$

is one. The number of paths can be exponential in $v$, so the game is given by the graph and the cost tables, not as a table of payoffs.

## The algorithm

```pseudo id=main
SYM-CONGESTION-EQ(G, s, t, n, c)
L1  x_e ← 0 for each edge e
L2  for k ← 1 to n do
L3      P ← a cheapest s-t path, by Bellman-Ford, in the residual graph: arc u→v of cost c_e(x_e + 1) if x_e < n, and arc v→u of cost -c_e(x_e) if x_e > 0, for each edge e = (u, v)
L4      for each arc of P: x_e ← x_e + 1 if the arc is forward, x_e ← x_e - 1 if it is backward
L5  for k ← 1 to n do
L6      walk from s along edges with x_e > 0 until the walk reaches t
L7          if the walk comes back to a vertex on it: x_e ← x_e - 1 on that cycle, and cut the cycle from the walk
L8      P_k ← the walk; x_e ← x_e - 1 on each edge of P_k
L9  return (P_1, ..., P_n)
```

The forward arc of $e$ costs $c_e(x_e + 1)$, the amount that one more unit on $e$ adds to the potential. The backward arc costs $-c_e(x_e)$, the amount that one unit less on $e$ removes from it. These are the marginal costs of a separable convex cost, so line L3 is one step of [successive shortest paths](/successive-shortest-path/) on the network where each edge is $n$ parallel unit arcs of costs $c_e(1), \ldots, c_e(n)$. A backward arc moves part of the route of an earlier player. The flow after line L4 can hold cycles of zero cost, and line L7 removes them, so each $P_k$ is simple.

## Example

Take the graph with vertices $s, a, b, t$, $n = 3$ players and these edges, where $x$ is the load: $s \to a$ costs $2x$, $a \to t$ costs 5, $s \to b$ costs 5, $b \to t$ costs $2x$, and $a \to b$ costs 0. The three paths are $s a t$, $s a b t$ and $s b t$. The table traces lines L2 to L4. The loads are listed in the order $s a$, $a t$, $s b$, $b t$, $a b$.

| round | cheapest residual path | length | loads after line L4 |
|---|---|---|---|
| 1 | $s \to a \to b \to t$ | $2 + 0 + 2 = 4$ | 1, 0, 0, 1, 1 |
| 2 | $s \to a \to b \to t$ | $4 + 0 + 4 = 8$ | 2, 0, 0, 2, 2 |
| 3 | $s \to b$, back over $a \to b$, then $a \to t$ | $5 - 0 + 5 = 10$ | 2, 1, 1, 2, 1 |

In round 3 the direct paths $s a t$ and $s b t$ both cost $6 + 5 = 11$ and the path $s a b t$ costs $6 + 0 + 6 = 12$, so the backward arc wins with 10. It moves the tail of one earlier player from $b \to t$ to $a \to t$. The potential is $4 + 8 + 10 = 22$, the sum of the three lengths. Lines L5 to L9 split the loads into $s a t$, $s a b t$ and $s b t$. The players pay $4 + 5 = 9$, $4 + 0 + 4 = 8$ and $5 + 4 = 9$, so the total cost is 26.

This profile is an equilibrium. The player on $s a t$ would pay $4 + 0 + 6 = 10$ on $s a b t$ and $5 + 6 = 11$ on $s b t$. The player on $s a b t$ would pay $4 + 5 = 9$ on either direct path. The player on $s b t$ would pay $6 + 5 = 11$ on $s a t$ and $6 + 0 + 4 = 10$ on $s a b t$. A search over all 10 profiles shows that it is the only pure Nash equilibrium. The least total cost is 25, with two players on one direct path and one on the other, so the price of anarchy and the price of stability of this game are both $26/25$. Without the edge $a \to b$ the algorithm returns that optimum, with potential 23, so the free edge raises the equilibrium cost from 25 to 26, as in [Braess's paradox](/braess-paradox/).

## Correctness

The file proofs/correctness.md has the full proof. Replace each edge by $n$ parallel unit arcs of costs $c_e(1) \le \cdots \le c_e(n)$. A flow that uses the cheapest $x_e$ copies of each edge costs exactly $\Phi(x)$, and no flow with the same loads costs less, so a min-cost flow of value $n$ in this network gives loads that minimize $\Phi$. The residual graph of line L3 is the residual graph of the expanded network with only the cheapest copy kept, so it has the same shortest paths and no negative cycle, and an augmentation keeps the "cheapest copies" form. By the successive shortest path theorem, after $k$ rounds the loads minimize $\Phi$ among integral flows of value $k$. Removing a cycle cannot raise $\Phi$, because the costs are nonnegative, so the $n$ paths of lines L5 to L9 still minimize $\Phi$ over all flows of value $n$, and so over all profiles. If one player changes path, $\Phi$ changes by exactly the change of that player's cost, so at a minimizer no change gains.

## Complexity

Line L3 runs Bellman-Ford with at most $v - 1$ rounds over $2m$ arcs, so it takes $O(v m)$ time, and lines L2 to L4 take $O(n v m)$. In the split, each step either extends a simple walk, at most $v - 1$ times between two cuts, or cuts a cycle and lowers $\sum_e x_e \le n m$ by at least 1. A pointer per vertex skips the edges whose load is already 0, which never become positive again, so lines L5 to L9 take $O(n (v + m))$ time. The total is $O(n v m)$. The loads, labels and predecessors take $O(v + m)$ extra space, and the output takes $O(n v)$. These bounds count arithmetic on costs as unit steps. The input holds $n$ costs per edge, so $n$ is at most the input size and the running time is polynomial in it.

## Properties

- **It returns a global minimizer of the potential.** That is more than an equilibrium: [best-response dynamics](/best-response-dynamics/) stops at any local minimum of $\Phi$, and those can be worse.
- **Social cost at most twice the optimum for affine costs.** If $c_e(x) = a_e x + b_e$ with $a_e, b_e \ge 0$, then $\Phi \le C \le 2 \Phi$ for the total cost $C$, so the output has $C \le 2 \Phi(\text{out}) \le 2 \Phi(\text{opt}) \le 2 C(\text{opt})$. The [price of anarchy for linear congestion games](/atomic-linear-congestion-price-of-anarchy/) bounds the worst equilibrium by $5/2$ times the optimum.
- **Exact.** With rational costs the code uses exact fractions, so ties and equilibrium checks are decided exactly.
- **Deterministic.** The output depends on the order of the edges only through ties between paths of equal length.

## Variants and improvements

- **Dijkstra with potentials.** Keep the distance labels of the previous round as node potentials. The reduced costs are then nonnegative, and [Dijkstra's algorithm](/dijkstra/) replaces Bellman-Ford, which gives $O(n (m + v \log v))$ time with a Fibonacci heap. This is the usual form of successive shortest paths.
- **Large $n$.** When the costs are given by formulas and $n$ is written in binary, $n$ augmentations take time exponential in the input size. Capacity scaling for convex cost flows (Ahuja, Magnanti and Orlin, Chapter 14) handles that case.
- **Parallel links.** If every path is one edge, line L3 just picks the edge with the least $c_e(x_e + 1)$ and never needs a backward arc. This greedy rule gives an equilibrium of a symmetric game on parallel links.
- **Several sources or sinks.** With different source-sink pairs the loads would have to come from an integral multicommodity flow, and the reduction breaks. Fabrikant, Papadimitriou and Talwar proved that this case is PLS-complete; see [PLS-completeness of congestion games](/pls-completeness-of-congestion-games/).

## When to use it

Use it when all players share one source and one sink and you need an equilibrium with a proof, or the equilibrium of least potential, for example as the start of a price of stability bound. For games with different source-sink pairs, or for symmetric games whose strategies are not paths of a graph, no polynomial method is known, and the search problem is PLS-complete; there, best-response dynamics is the usual heuristic.

## Pitfalls

- **Minimizing the total cost in place of the potential.** The marginal social cost $(x + 1) c_e(x + 1) - x\, c_e(x)$ on the arcs gives the social optimum, not an equilibrium. In the example that returns cost 25 with two players on one direct path, and each of them gains by moving to $s a b t$, from 9 to 8.
- **No backward arcs.** Routing the players one by one on cheapest paths with costs $c_e(x_e + 1)$, without the arcs of line L3 that go back, is a greedy heuristic. In the example its third player takes a direct path at cost 11, which gives potential 23 and a profile that is not an equilibrium.
- **Plain Dijkstra on the residual graph.** The backward arcs have negative costs. Use Bellman-Ford, or Dijkstra on reduced costs with valid potentials.
- **Decreasing costs.** With economies of scale the cheapest copies are no longer the first ones, the problem becomes a concave cost flow, and the reduction fails. Rosenthal's theorem still gives an equilibrium, but this algorithm does not find it. The code rejects such input.
- **Splitting a flow that holds cycles.** Edges of cost 0 in both directions can carry flow around a cycle. A split that does not cut cycles may never reach $t$ or may return a path that repeats a vertex.

## Implementations

## History

Rosenthal defined congestion games in 1973 and showed that a minimizer of his potential is a pure Nash equilibrium. Fabrikant, Papadimitriou and Talwar asked in 2004 how hard it is to find one. They showed that in the symmetric network case the minimizer is a min-cost flow and can be found in polynomial time, and that the problem is PLS-complete for general congestion games, for symmetric congestion games and for asymmetric network games. Ackermann, Roglin and Vocking later showed that matroid congestion games are also easy, because best-response dynamics converges after polynomially many steps there.

## References
