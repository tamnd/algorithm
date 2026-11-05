---
tag: N0EAZN
kind: problem
slug: k-machine-interval-scheduling
name: k-machine interval scheduling
aliases:
- Weighted interval scheduling on k identical machines
area: sequences/interval-problems
level: advanced
summary: Schedule weighted intervals on k machines to maximize total weight.
prereqs: [weighted-interval-scheduling, interval-coloring-depth-theorem, min-cost-flow-problem]
see_also: [k-colorable-interval-subgraph, weighted-interval-dp, interval-partitioning-greedy, activity-selection, consecutive-ones-property, total-unimodularity, maximum-overlap, online-interval-scheduling]
sources:
  - paper: doi:10.1016/0166-218X(87)90037-0
    title: "Esther M. Arkin and Ellen B. Silverberg, Scheduling jobs with fixed start and end times, Discrete Applied Mathematics 18(1) (1987), pages 1 to 8"
    locator: the weighted problem on k identical machines, solved as a minimum cost flow
  - paper: doi:10.1016/0166-218X(93)E0174-W
    title: "Martin C. Carlisle and Errol L. Lloyd, On the k-coloring of intervals, Discrete Applied Mathematics 59(3) (1995), pages 225 to 235"
    locator: the O(k + n) algorithm for the unweighted case with presorted end points, and the flow algorithm for the weighted case
  - paper: doi:10.1016/0020-0190(87)90107-4
    title: "Mihalis Yannakakis and Fanica Gavril, The maximum k-colorable subgraph problem for chordal graphs, Information Processing Letters 24(2) (1987), pages 133 to 137"
    locator: the maximum k-colorable subgraph of an interval graph, the same problem in graph terms
---

In $k$-machine interval scheduling, each of $n$ jobs must run during a fixed interval of time, has a weight, and needs one of $k$ identical machines for its whole interval; the task is to accept a set of jobs of largest total weight that fits on the machines. By the [interval coloring depth theorem](/interval-coloring-depth-theorem/), a set of jobs fits if and only if no point of time lies in more than $k$ of them, so the problem asks for a heaviest subfamily of depth at most $k$. Arkin and Silverberg solve it as a [minimum cost flow](/min-cost-flow-problem/) of $k$ units along the time line, and for unit weights a greedy by end time is optimal. For $k = 1$ it is [weighted interval scheduling](/weighted-interval-scheduling/), and whether jobs that touch at an end point can share a machine depends on the end point type.

## In plain words

You run a hire shop with $k$ identical machines. Customers ask for a machine from one time to another, and each offers a price. A machine can serve only one customer at a time. You want to accept the offers that earn the most.

A set of offers can be served exactly when, at every moment, at most $k$ of them are running. So you are choosing offers so that the pile at any moment is at most $k$ high.

Think of the $k$ machines as $k$ workers walking along the time line. At each offer, a worker may step onto it, collect its price, and step off at its end, or the worker may walk past. The best plan for $k$ walkers is a flow problem that a computer solves quickly.

## Definition

**Input.** Intervals $I_1, \ldots, I_n$, $I_j = \langle l_j, r_j \rangle$, all of one type, with weights $w_j > 0$, and an integer $k \ge 1$. Closed intervals have $l_j \le r_j$, half-open and open intervals $l_j < r_j$.

**Feasible sets.** A set $A$ of jobs is *feasible* if there is a map $m : A \to \{1, \ldots, k\}$ such that $m(i) = m(j)$ implies $I_i \cap I_j = \emptyset$. Closed intervals that share an end point meet, so they need different machines; half-open and open intervals that share an end point are disjoint.

**Output.** A feasible set $A$ of largest weight $w(A) = \sum_{j \in A} w_j$, with its machine assignment.

**Depth form.** Let $d(A) = \max_x |\{ j \in A : x \in I_j \}|$ be the depth of $A$. By the [depth theorem](/interval-coloring-depth-theorem/), $A$ is feasible if and only if $d(A) \le k$, and the [interval partitioning greedy](/interval-partitioning-greedy/) turns any such $A$ into an assignment on $d(A)$ machines in $O(|A| \log |A|)$ time. So the problem is: maximize $w(A)$ subject to $d(A) \le k$.

**Integer program.** Let $x_1 < \cdots < x_q$ be points such that every intersection pattern is seen at one of them; for intervals of one type, the left ends serve for closed and half-open intervals, and for open intervals a point just right of each left end. Then $A$ is feasible if and only if $\sum_{j : x_t \in I_j} y_j \le k$ for every $t$, where $y_j \in \{0, 1\}$ says whether $j \in A$. The constraint matrix has the [consecutive ones property](/consecutive-ones-property/) for columns in the order of the points, so it is [totally unimodular](/total-unimodularity/), and the linear relaxation with $0 \le y_j \le 1$ has an integral optimum.

## Variants

- **One machine.** $k = 1$ is [weighted interval scheduling](/weighted-interval-scheduling/).
- **Unit weights.** Maximize the number of accepted jobs. Sorting by right end and giving each job to a free machine, the one whose last job ends latest among those free in time, rejecting the job if none is free, is optimal; Carlisle and Lloyd do this in $O(k + n)$ time with presorted end points.
- **Enough machines.** If $k$ is at least the depth of all the jobs, every job is accepted, and the problem is [interval partitioning](/interval-partitioning-greedy/).
- **The fewest machines for all jobs.** The dual question, the depth, is [maximum overlap](/maximum-overlap/).
- **Machines that differ.** If each job can run only on some machines, the problem becomes NP-hard in general; Arkin and Silverberg study this case as well.
- **Graph form.** Choose a heaviest set of vertices of an interval graph that can be colored with $k$ colors: the [maximum weight k-colorable subgraph](/k-colorable-interval-subgraph/) of an interval graph, which Yannakakis and Gavril study for chordal graphs in general.
- **Online.** Jobs arrive in order of start and must be accepted or rejected at once: [online interval scheduling](/online-interval-scheduling/).

## Examples

Take the six jobs of the [weighted interval scheduling](/weighted-interval-scheduling/) page:

| job | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ |
|---|---|---|---|---|---|---|
| interval | $(0, 3)$ | $(3, 6)$ | $(1, 5)$ | $(5, 8)$ | $(6, 9)$ | $(8, 10)$ |
| weight | 2 | 4 | 5 | 3 | 4 | 2 |

The best weights, found by a search over all 64 subsets, are:

| $k$ | closed | half-open |
|---|---|---|
| 1 | 9, $\{c, e\}$ | 10, $\{a, b, e\}$ |
| 2 | 15, $\{b, c, e, f\}$ | 20, all six |
| 3 | 20, all six | 20, all six |

*Half-open, $k = 2$.* The depth of all six jobs is 2, so all fit: machine 1 runs $[0, 3), [3, 6), [6, 9)$ and machine 2 runs $[1, 5), [5, 8), [8, 10)$, each machine passing a job to the next at a touching point.

*Closed, $k = 2$.* The depth of all six is 3, at the points 3, 5, 6 and 8: for example $[0, 3], [1, 5], [3, 6]$ all contain 3. Dropping $a$ and $d$, weight 5, leaves depth 2: machine 1 runs $[1, 5], [6, 9]$ and machine 2 runs $[3, 6], [8, 10]$. No set of weight more than 15 has depth 2.

*Closed, $k = 3$.* The depth is 3, so all jobs fit.

**Edge cases.** With $k \ge n$ every job is accepted. If all jobs contain one common point, the answer is the $k$ heaviest jobs.

## Known algorithms

- **Minimum cost flow (Arkin and Silverberg).** Sort the distinct end points, with a left end placed before a right end at the same value for closed intervals and after it for half-open and open intervals, into nodes $v_1, \ldots, v_q$. Add an arc $v_t \to v_{t+1}$ of capacity $k$ and cost 0 for each $t$, and an arc from the node of $l_j$ to the node of $r_j$ of capacity 1 and cost $-w_j$ for each job. Send $k$ units from $v_1$ to $v_q$ at least cost. An integral flow splits into $k$ paths from $v_1$ to $v_q$, each of which uses job arcs of pairwise disjoint jobs in time order, so it is a schedule for one machine; conversely each machine's jobs give such a path. So the least cost is $-w(A)$ for an optimal $A$. The graph is acyclic with $O(n)$ nodes and arcs, so $k$ rounds of successive shortest paths with [Dijkstra](/dijkstra/) and potentials take $O(k n \log n)$ time.
- **Linear programming.** By total unimodularity, any LP solver that returns a vertex solves the integer program.
- **Dynamic programming for $k = 1$.** The [weighted interval DP](/weighted-interval-dp/), $O(n \log n)$.
- **Greedy for unit weights.** As in the Variants section, $O(n \log n)$, or $O(k + n)$ with sorted end points.
- **Brute force.** Try all $2^n$ subsets and test the depth, for checking.

## Bounds

**Upper bound.** $O(k n \log n)$ time and $O(n)$ space by the flow. Carlisle and Lloyd state their weighted bound as $O(k S(n))$, with $S(n)$ the time of one shortest path computation.

**Lower bound.** $\Omega(n \log n)$ in the algebraic decision tree model for every $k$, even with unit weights. Given numbers $x_1, \ldots, x_n$, take $k$ copies of each closed point interval $[x_j, x_j]$, $nk$ jobs of weight 1. The answer is $nk$ if and only if no point lies in more than $k$ of them, that is, if and only if all $x_j$ are distinct, which is [element distinctness](/element-distinctness/). For fixed $k$ this is $nk = O(n)$ jobs.

## Reductions

- **From weighted interval scheduling.** The case $k = 1$.
- **To minimum cost flow.** As above.
- **To a maximum weight $k$-colorable subgraph.** By the depth theorem, the feasible sets are the vertex sets of $k$-colorable induced subgraphs of the interval graph.
- **To linear programming.** Through the consecutive ones property and total unimodularity.

## Applications

- **Rental and fleet planning.** Accept the most profitable bookings for $k$ cars, rooms, gates or cranes.
- **Register allocation.** With $k$ registers and live ranges of straight-line code as intervals, keep the most valuable variables in registers and spill the rest; Carlisle and Lloyd name this application.
- **Bandwidth and channels.** Accept the most valuable reservations of $k$ channels over time.
- **Crew and processor scheduling.** Fixed-time tasks on $k$ identical processors, where the tasks that cannot be served are lost.

## References
