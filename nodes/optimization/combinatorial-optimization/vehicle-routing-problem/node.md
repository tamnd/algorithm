---
tag: STCSB2
kind: problem
slug: vehicle-routing-problem
name: Vehicle routing problem
aliases:
- VRP
- capacitated vehicle routing problem
- CVRP
- truck dispatching problem
area: optimization/combinatorial-optimization
level: core
summary: Route a fleet of vehicles from a depot to serve customers under capacity and other constraints.
prereqs: [traveling-salesman-problem, bin-packing]
see_also: [clarke-wright-savings, traveling-salesman-problem, column-generation, branch-and-price, large-neighborhood-search, tabu-search, set-cover, christofides-algorithm]
sources:
  - book: isbn:9780898714982
    title: Paolo Toth and Daniele Vigo (editors), The Vehicle Routing Problem, SIAM, 2002
    locator: Chapter 1 (an overview of vehicle routing problems and their formulations), Chapter 5 (classical heuristics for the capacitated VRP, including the savings and sweep methods), Chapter 6 (metaheuristics)
  - paper: doi:10.1287/mnsc.6.1.80
    title: George B. Dantzig and John H. Ramser, The truck dispatching problem, Management Science 6(1), 80 to 91, 1959
    locator: the problem statement and the first method
  - paper: doi:10.1287/opre.12.4.568
    title: G. Clarke and J. W. Wright, Scheduling of vehicles from a central depot to a number of delivery points, Operations Research 12(4), 568 to 581, 1964
    locator: the savings method
  - paper: doi:10.1287/moor.10.4.527
    title: Mordecai Haimovich and Alexander H. G. Rinnooy Kan, Bounds and heuristics for capacitated routing problems, Mathematics of Operations Research 10(4), 527 to 542, 1985
    locator: the radial lower bound and iterated tour partitioning with its worst-case ratio
  - paper: doi:10.1287/trsc.1050.0135
    title: Stefan Ropke and David Pisinger, An adaptive large neighborhood search heuristic for the pickup and delivery problem with time windows, Transportation Science 40(4), 455 to 472, 2006
    locator: the adaptive large neighborhood search method
  - paper: "Artur Pessoa, Ruslan Sadykov, Eduardo Uchoa and François Vanderbeck, A generic exact solver for vehicle routing and related problems, Mathematical Programming 183, 483 to 523, 2020"
    locator: the branch-cut-and-price solver and its results on benchmark instances
---

The vehicle routing problem (VRP) asks for a set of routes, each starting and ending at a depot, that together serve every customer once at least total cost, subject to limits on each vehicle. The basic form is the *capacitated* VRP (CVRP), where each customer has a demand and each vehicle carries at most $Q$. It contains the [traveling salesman problem](/traveling-salesman-problem/) (one vehicle, no capacity limit) and [bin packing](/bin-packing/) (the number of vehicles), so it is NP-hard in the strong sense and, with metric costs, [APX](/apx/)-hard. For unit demands, iterated tour partitioning gives a ratio below $1 + \alpha$, where $\alpha$ is the ratio of the TSP algorithm it uses. In practice, [branch and price](/branch-and-price/) solves instances with a few hundred customers exactly, and the [savings algorithm](/clarke-wright-savings/), [tabu search](/tabu-search/) and [large neighborhood search](/large-neighborhood-search/) are used for larger ones.

## In plain words

A company has one depot and a fleet of trucks of the same size. Each shop on a list orders some amount of goods. Each truck leaves the depot, visits some shops, drops their goods, and comes back. A truck cannot carry more than it holds. Which shops should each truck visit, and in what order, so that the total driving is as short as possible?

There are two hard questions in one. The first is how to split the shops into groups that fit in a truck, which is like packing boxes. The second is the best order in each group, which is a small traveling salesman problem. Even with one truck that holds everything, the problem is already as hard as the traveling salesman problem.

## Definition

**Input (CVRP).** A depot $0$ and customers $1, \ldots, n$. Symmetric costs $c(i, j) \ge 0$ between all of them. A demand $0 < q_i \le Q$ for each customer and a vehicle capacity $Q$. Sometimes also a number $K$ of vehicles.

**Output.** A set of routes $R_1, \ldots, R_m$ (with $m \le K$ if $K$ is given). Each route is a cycle $0, i_1, \ldots, i_k, 0$. Every customer is on exactly one route, and each route has load $\sum_{i \in R} q_i \le Q$. The objective is to minimize the total cost $\sum_{r} c(R_r)$.

As a *set partitioning* program over the family $\mathcal{R}$ of all feasible routes, with $c_R$ the cost of route $R$:

$$ \min \sum_{R \in \mathcal{R}} c_R \, y_R \quad \text{s.t.} \quad \sum_{R \ni i} y_R = 1 \ \ (i = 1, \ldots, n), \qquad y_R \in \{0, 1\}. $$

The family $\mathcal{R}$ is exponentially large. [Column generation](/column-generation/) solves the LP relaxation by pricing new routes, and [branch and price](/branch-and-price/) uses it inside a search tree.

## Variants

- **Distance-constrained VRP.** Each route has a maximum length or duration instead of, or in addition to, a capacity.
- **VRP with time windows (VRPTW).** Each customer must be served within a time interval, and service takes time.
- **Pickup and delivery.** Goods move from a pickup point to a delivery point on the same route, with the pickup first.
- **Multi-depot, heterogeneous fleet, split delivery.** Several depots, vehicles of different sizes and costs, or customers that may be served by more than one vehicle.
- **Periodic, stochastic and dynamic VRP.** Routes over several days, uncertain demands, or requests that arrive during the day.
- **Unit demands.** All $q_i = 1$. This case is the subject of most approximation results.

## Examples

Take the depot at $(0, 0)$ and five customers on a grid with the Manhattan distance, capacity $Q = 10$:

| customer | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| position | $(2, 4)$ | $(-5, 1)$ | $(-2, -2)$ | $(-4, 3)$ | $(-5, 5)$ |
| demand | 2 | 3 | 2 | 6 | 4 |
| cost from depot | 6 | 6 | 4 | 7 | 10 |

The total demand is 17, so at least 2 vehicles are needed. Serving each customer by its own vehicle costs $2(6 + 6 + 4 + 7 + 10) = 66$. The optimum, found by checking all partitions into feasible routes, is 42:

- route $0, 3, 4, 0$, load 8, cost $4 + 7 + 7 = 18$;
- route $0, 1, 5, 2, 0$, load 9, cost $6 + 8 + 4 + 6 = 24$.

Customers 4 and 5 are close to each other, but putting them on one truck fills it to $6 + 4 = 10$. The optimum splits them. The [Clarke-Wright savings algorithm](/clarke-wright-savings/) joins 4 and 5 first and ends at 46 on this instance.

## Known algorithms

- **Exact.** [Branch and price](/branch-and-price/) and branch-cut-and-price on the set partitioning model, with pricing by a shortest path with resource constraints, and cuts such as rounded capacity inequalities $x(\delta(S)) \ge 2 \lceil q(S)/Q \rceil$. Pessoa, Sadykov, Uchoa and Vanderbeck (2020) report instances with a few hundred customers solved to optimality. Dynamic programming over subsets solves very small instances.
- **Classical heuristics** (Toth and Vigo, Chapter 5). The [Clarke-Wright savings algorithm](/clarke-wright-savings/) merges routes by the largest saving. The sweep algorithm sorts the customers by angle around the depot and cuts the order into feasible groups. Route-first, cluster-second methods build one TSP tour and split it optimally into routes.
- **Approximation.** Iterated tour partitioning (Haimovich and Rinnooy Kan, 1985) takes an $\alpha$-approximate TSP tour and cuts it into segments of load at most $Q$. For unit demands its ratio is $1 + (1 - \frac{1}{Q})\alpha$, so $\frac{5}{2} - \frac{3}{2Q}$ with [Christofides' algorithm](/christofides-algorithm/).
- **Metaheuristics** (Toth and Vigo, Chapter 6). [Tabu search](/tabu-search/), [large neighborhood search](/large-neighborhood-search/) and its adaptive form (Ropke and Pisinger, 2006), and hybrid genetic search with local search. These give the best known solutions on standard benchmarks with up to thousands of customers.

## Bounds

- **Hardness.** CVRP is NP-hard in the strong sense: with $Q \ge \sum_i q_i$ and one vehicle it is the TSP. Deciding if $K$ vehicles suffice is [bin packing](/bin-packing/), which is strongly NP-complete, so even finding a feasible solution with a given $K$ is NP-hard. With metric costs it is APX-hard, because metric TSP is.
- **Radial lower bound.** Each route $R$ costs at least $2 \max_{i \in R} c(0, i) \ge \frac{2}{Q} \sum_{i \in R} q_i \, c(0, i)$ under the triangle inequality, so $\mathrm{OPT} \ge \frac{2}{Q} \sum_{i} q_i \, c(0, i)$. Together with $\mathrm{OPT} \ge \mathrm{OPT}_{\text{TSP}}$, this is the bound behind the ratio of iterated tour partitioning.
- **Number of vehicles.** At least $\lceil \sum_i q_i / Q \rceil$ vehicles are needed, and with unsplittable demands possibly more.
- **Approximation.** For unit demands and metric costs, the ratio $1 + (1 - \frac{1}{Q})\alpha$ above. For general unsplittable demands, iterated tour partitioning needs a correction and its ratio is larger.

## Reductions

- **From TSP.** One vehicle with capacity at least the total demand. So CVRP inherits all hardness of the [TSP](/traveling-salesman-problem/).
- **From bin packing.** Put all customers at one point at distance 1 from the depot. Then $K$ vehicles suffice if and only if the demands pack into $K$ bins of size $Q$.
- **To set partitioning.** The model above. Its LP relaxation is solved by [column generation](/column-generation/), and its pricing problem is an elementary shortest path problem with a capacity resource, which is itself NP-hard.
- **To TSP, approximately.** Route-first, cluster-second: an optimal split of a fixed tour into routes is a shortest path in an acyclic graph over the positions of the tour.

## Applications

- **Distribution.** Delivery of goods from a warehouse to shops, fuel to gas stations, and parcels to homes. Dantzig and Ramser (1959) studied gasoline delivery.
- **Collection.** Waste collection, milk collection from farms, and mail pickup.
- **Services.** School buses, home care visits and technician schedules, often with time windows.
- **Inside other models.** Inventory routing and location routing use VRP as a step, and VRP itself uses [TSP](/traveling-salesman-problem/) for each route.

## References
