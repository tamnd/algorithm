---
tag: BGTTNH
kind: algorithm
slug: clarke-wright-savings
name: Clarke-Wright savings algorithm
aliases:
- savings heuristic
- savings algorithm
- Clarke and Wright savings method
area: optimization/combinatorial-optimization
level: core
summary: Merge routes greedily by the savings from connecting customer pairs.
solves: [vehicle-routing-problem]
model: word-ram
complexity:
  vars: {n: the number of customers}
  time: {worst: Θ(n^2 log n), average: Θ(n^2 log n), best: Θ(n^2 log n)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1964
  people: [G. Clarke, J. W. Wright]
  note: Clarke and Wright published the savings method in Operations Research in 1964, as an improvement on the method of Dantzig and Ramser.
prereqs: [vehicle-routing-problem, greedy-algorithm]
see_also: [vehicle-routing-problem, traveling-salesman-problem, nearest-neighbor-heuristic, greedy-edge-heuristic, two-opt, large-neighborhood-search, tabu-search, local-search]
sources:
  - paper: doi:10.1287/opre.12.4.568
    title: G. Clarke and J. W. Wright, Scheduling of vehicles from a central depot to a number of delivery points, Operations Research 12(4), 568 to 581, 1964
    locator: the definition of the savings and the merge procedure
  - book: isbn:9780898714982
    title: Paolo Toth and Daniele Vigo (editors), The Vehicle Routing Problem, SIAM, 2002
    locator: Chapter 5, Classical heuristics for the capacitated VRP, by Gilbert Laporte and Frédéric Semet (the savings algorithm, its parallel and sequential versions, and its improvements)
  - paper: doi:10.1016/0377-2217(92)90192-C
    title: Gilbert Laporte, The vehicle routing problem, an overview of exact and approximate algorithms, European Journal of Operational Research 59(3), 345 to 358, 1992
    locator: the section on classical heuristics and the savings method
  - paper: doi:10.1287/mnsc.6.1.80
    title: George B. Dantzig and John H. Ramser, The truck dispatching problem, Management Science 6(1), 80 to 91, 1959
    locator: the problem statement and the earlier pairing method
---

The Clarke-Wright savings algorithm is a greedy heuristic for the capacitated [vehicle routing problem](/vehicle-routing-problem/). It starts with one route per customer, from the depot and back, and merges two routes end to end whenever this saves distance and the load still fits, trying the pairs in order of decreasing *saving* $s(i, j) = c(0, i) + c(0, j) - c(i, j)$. It runs in $\Theta(n^2 \log n)$ time for $n$ customers, always returns a feasible solution, and is still a standard first step in routing software. It has no proved worst-case ratio; its quality is known from experiments.

## In plain words

Imagine that every shop first gets its own truck, which drives out from the depot and comes straight back. That is wasteful. If one truck visits shop $i$ and then shop $j$ before it returns, it skips the drive from $i$ back to the depot and the drive from the depot out to $j$, and it adds only the drive from $i$ to $j$. The difference is the *saving* of the pair.

The method lists all pairs of shops by their saving, the largest first. For each pair, it joins the two trucks into one if the two shops are at the ends of their routes, if they are on different trucks, and if the joined load still fits. Then it moves on to the next pair.

## The problem

The input is a depot $0$, customers $1, \ldots, n$ with demands $0 \le q_i \le Q$, a vehicle capacity $Q$, and symmetric costs $c(i, j)$. The output is a set of routes from the depot and back that serve each customer once, with load at most $Q$ each. The goal of the [vehicle routing problem](/vehicle-routing-problem/) is the least total cost. The savings algorithm aims at a low cost but does not guarantee the optimum.

## The algorithm

```pseudo id=main
CLARKE-WRIGHT(c, q[1 .. n], Q)
L1  for each customer i: route(i) ← (i), load(i) ← q[i]       ▷ n routes 0, i, 0
L2  for each pair i < j, in order of decreasing s(i, j) = c(0, i) + c(0, j) − c(i, j) do
L3      if s(i, j) ≤ 0 then stop the loop
L4      if i and j are on the same route then skip this pair
L5      if i is not an end of its route, or j is not an end of its route, then skip this pair
L6      if load(route of i) + load(route of j) > Q then skip this pair
L7      reverse the routes if needed, so that i is the last customer of its route and j the first of its route
L8      append the route of j to the route of i, and add the loads
L9  return the routes
```

The *ends* of a route are its first and last customer, the two customers next to the depot. A route with one customer has that customer as both ends. Line L8 replaces the edges $(i, 0)$ and $(0, j)$ by the edge $(i, j)$, so the total cost goes down by exactly $s(i, j)$.

## Example

Take the instance of the [vehicle routing problem](/vehicle-routing-problem/) page: depot $(0, 0)$, Manhattan distances, capacity $Q = 10$, customers 1 to 5 at $(2, 4)$, $(-5, 1)$, $(-2, -2)$, $(-4, 3)$, $(-5, 5)$ with demands 2, 3, 2, 6, 4. The 5 routes of line L1 cost $2(6 + 6 + 4 + 7 + 10) = 66$. The positive savings, in the order of line L2, are:

| pair | saving | routes before | test | action | cost after |
| --- | --- | --- | --- | --- | --- |
| (4, 5) | 14 | (1) (2) (3) (4) (5) | load $6 + 4 = 10$ | merge into (4, 5) | 52 |
| (2, 5) | 12 | (1) (2) (3) (4, 5) | load $3 + 10 > 10$ | skip (L6) | 52 |
| (2, 4) | 10 | same | load $3 + 10 > 10$ | skip (L6) | 52 |
| (1, 5) | 8 | same | load $2 + 10 > 10$ | skip (L6) | 52 |
| (1, 4) | 6 | same | load $2 + 10 > 10$ | skip (L6) | 52 |
| (2, 3) | 4 | same | load $3 + 2 = 5$ | merge into (2, 3) | 48 |
| (3, 4) | 4 | (1) (2, 3) (4, 5) | load $5 + 10 > 10$ | skip (L6) | 48 |
| (3, 5) | 4 | same | load $5 + 10 > 10$ | skip (L6) | 48 |
| (1, 2) | 2 | same | load $2 + 5 = 7$ | merge into (1, 2, 3) | 46 |

The next saving, of the pair (1, 3), is 0, so line L3 stops. The result is the routes $0, 1, 2, 3, 0$ (cost 26) and $0, 4, 5, 0$ (cost 20), total 46. The optimum is 42, with routes $0, 3, 4, 0$ and $0, 1, 5, 2, 0$. The first merge, of the two closest heavy customers, fills one truck completely and blocks every later merge with it.

## Correctness

The algorithm keeps four invariants. (1) The routes partition the customers. (2) Every route has load at most $Q$. (3) The total cost equals $2 \sum_i c(0, i)$ minus the sum of the savings of the merges done so far. (4) A customer that is not an end of its route never becomes an end again, and a route only grows. Line L1 makes (1) to (3) true. Lines L4 to L6 allow a merge only of two different routes, at their ends, with joint load at most $Q$, and line L8 changes the cost by $-s(i, j)$, so each merge keeps (1) to (3). Line L8 makes $i$ and $j$ interior and keeps the other two ends, so (4) holds. The loop is finite, so the algorithm stops, and by (1) and (2) its output is feasible.

At the end, no pair with a positive saving can still be merged: if $i$ and $j$ are ends of different final routes with joint load at most $Q$, then by (4) they were ends of different routes with no larger loads when line L2 reached the pair, so line L8 would have merged them. The proof file below gives the details.

## Complexity

- **Savings.** There are $n(n-1)/2$ pairs. Computing and sorting the savings takes $\Theta(n^2 \log n)$ time and $\Theta(n^2)$ space. A heap gives the same worst case but can stop early.
- **Tests.** With an array that maps each customer to its route, and each route kept with its two ends and its load, lines L4 to L6 take $O(1)$ per pair.
- **Merges.** At most $n - 1$ merges happen, because each removes one route. A merge that relabels and possibly reverses the shorter route costs $O(n)$, so all merges cost $O(n^2)$. The implementation below relabels the second route, which is also $O(n)$ per merge.
- **Total.** $\Theta(n^2 \log n)$ time, dominated by the sort, and $\Theta(n^2)$ space for the list of savings.

## Properties

- **Always feasible.** The output serves every customer once and respects the capacity, if every single demand is at most $Q$.
- **Cost never above the start.** Each merge saves $s(i, j) > 0$, so the result costs at most $2 \sum_i c(0, i)$.
- **Maximal.** No two route ends on different routes can be joined with a positive saving and a feasible load.
- **Greedy.** A merge is never undone, which is why the first merge in the example blocks the optimum.
- **No guarantee.** The sources cited here prove no constant worst-case ratio for the method. Its quality is measured.
- **Measured behavior.** We ran the implementation below on 200 instances with 8 customers at random integer points in $[-50, 50]^2$ and a depot also at a random point, Euclidean distances times 100 rounded to integers, demands uniform in $\{1, \ldots, 10\}$, $Q = 20$, generated with Python `random.Random(31)`, against the exact optimum from dynamic programming over subsets. The mean ratio was 1.019, the median 1.000, the maximum 1.225, and the result was optimal in 60 percent of the instances.

## Variants and improvements

- **Sequential version.** Grow one route at a time: take the best saving that extends the current route at one of its ends, and start a new route when none fits. The parallel version above, which grows all routes at once, usually gives better results (Laporte and Semet in Toth and Vigo, Chapter 5).
- **Route shape parameter.** Use $s(i, j) = c(0, i) + c(0, j) - \lambda\, c(i, j)$ with a parameter $\lambda > 0$, run several values of $\lambda$, and keep the best result.
- **Local search after the merges.** Improve each route by [2-opt](/two-opt/) or [3-opt](/three-opt/), and move customers between routes. Savings solutions are a common start for [tabu search](/tabu-search/) and [large neighborhood search](/large-neighborhood-search/).
- **Other constraints.** The merge test of lines L4 to L6 can check route length, the number of stops or time windows as well as the load.
- **One vehicle, no capacity.** With $Q = \infty$ the method becomes a TSP heuristic: grow paths from a hub by the largest saving.

## When to use it

Use it when a good feasible routing is needed quickly, when the instance is too large for exact methods, or as the start for a metaheuristic. It is easy to extend with extra feasibility checks. Do not use it when you need a guarantee on the quality: for unit demands, iterated tour partitioning has a proved ratio. Do not use it as the final answer if a few percent matter: a [local search](/local-search/) or a [large neighborhood search](/large-neighborhood-search/) after it usually improves the solution.

## Pitfalls

- **Merging at an interior customer.** If $i$ is in the middle of its route, joining it to $j$ would make a branch, not a route. Check line L5.
- **Forgetting to reverse.** If $i$ is the first customer of its route, the route must be reversed before it is extended at $i$. With symmetric costs the reversal does not change the cost.
- **Stale loads.** After a merge, the load of the new route is the sum of the two loads. Code that keeps a load per customer instead of per route allows overfull trucks.
- **Negative savings.** With costs that break the triangle inequality, a saving can be negative, and merging then makes the solution worse. Line L3 stops at the first saving that is not positive.
- **Ties.** Many pairs can have equal savings, especially on grids. The order in which ties are tried changes the result, so fix a rule if results must be repeatable.

## Implementations

## History

Dantzig and Ramser (1959) stated the truck dispatching problem and proposed a method that pairs customers in stages. Clarke and Wright (1964) replaced it by the savings method, which merges routes in one pass in order of the savings. It became the standard classical heuristic for vehicle routing. Laporte (1992) and Laporte and Semet (in Toth and Vigo, 2002) survey it with its variants.

## References
