---
tag: 2TG2GJ
kind: problem
slug: asymmetric-tsp
name: Asymmetric TSP
aliases:
- ATSP
- directed TSP
- asymmetric traveling salesman problem
area: approximation/tsp-approximation
level: advanced
summary: The TSP on a complete directed graph where the cost from u to v can differ from the cost from v to u, with the directed triangle inequality. Ratios go from log n (1982) to a constant (2018).
prereqs: [metric-tsp, assignment-problem, eulerian-circuit, strongly-connected-components]
see_also: [asadpour-atsp-algorithm, subtour-elimination-lp, hungarian-algorithm, metric-tsp, held-karp-algorithm, metric-tsp-inapproximability, general-tsp-inapproximability, christofides-algorithm]
sources:
  - paper: doi:10.1002/net.3230120103
    title: Alan M. Frieze, Giulia Galbiati and Francesco Maffioli, On the worst-case performance of some algorithms for the asymmetric traveling salesman problem, Networks 12(1), 1982
    locator: pages 23 to 39 (the repeated cycle cover algorithm and its log2 n bound)
  - paper: doi:10.1287/opre.2017.1603
    title: Arash Asadpour, Michel X. Goemans, Aleksander Mądry, Shayan Oveis Gharan and Amin Saberi, An O(log n / log log n)-approximation algorithm for the asymmetric traveling salesman problem, Operations Research 65(4), 2017
    locator: pages 1043 to 1061 (first version at SODA 2010)
  - paper: doi:10.1145/3188745.3188824
    title: Ola Svensson, Jakub Tarnawski and László A. Végh, A constant-factor approximation algorithm for the asymmetric traveling salesman problem, STOC 2018
    locator: pages 204 to 213
  - title: Vera Traub and Jens Vygen, An improved approximation algorithm for ATSP, STOC 2020 (journal version in SIAM Journal on Computing 51(1), 2022)
    locator: the main theorem (ratio 22 plus epsilon, and integrality gap at most 22)
  - paper: doi:10.1016/j.jcss.2015.06.003
    title: Marek Karpinski, Michael Lampis and Richard Schmied, New inapproximability bounds for TSP, Journal of Computer and System Sciences 81(8), 2015
    locator: pages 1665 to 1677 (no ratio below 75/74 for ATSP unless P = NP)
  - title: Moses Charikar, Michel X. Goemans and Howard Karloff, On the integrality ratio for the asymmetric traveling salesman problem, Mathematics of Operations Research 31(2), 2006
    locator: pages 245 to 252 (the integrality gap of the ATSP LP is at least 2)
---

The asymmetric TSP (ATSP) is the [traveling salesman problem](/traveling-salesman-problem/) on a complete directed graph, where the cost $c_{uv}$ of going from $u$ to $v$ need not equal $c_{vu}$. With the directed triangle inequality $c_{uw} \le c_{uv} + c_{vw}$, the repeated cycle cover algorithm of Frieze, Galbiati and Maffioli (1982) gives a ratio of $\log_2 n$, which this page proves in full. The tree-based methods for the symmetric case do not carry over, and for decades the best ratios stayed logarithmic: $O(\log n / \log \log n)$ by [Asadpour et al.](/asadpour-atsp-algorithm/) (2010), then the first constant ratio by Svensson, Tarnawski and Végh (2018). No ratio below $75/74$ is possible unless P = NP.

## In plain words

In a city with one-way streets, the way from your home to the shop can be much longer than the way back. Or a machine needs a short setup to switch from red paint to black, but a long cleaning to switch from black to red. So the cost depends on the direction.

The task is the same as in the usual salesman problem: visit each place once and come back, at least total cost. Going straight is never worse than a detour through a third place.

The simple tricks for the usual problem fail here. A good method is to cover all places by small loops at least cost, keep one place from each loop, and repeat with these places. Each round at least halves the number of places, so after a few rounds one place is left, and the loops together form one long route.

## Definition

**Input.** A set $V$ of $n \ge 2$ vertices and a cost $c_{uv} \ge 0$ for each ordered pair $u \ne v$, with the *directed triangle inequality*

$$c_{uw} \le c_{uv} + c_{vw} \qquad \text{for all distinct } u, v, w.$$

**Output.** A directed Hamiltonian cycle $v_1 \to v_2 \to \cdots \to v_n \to v_1$ (a *tour*). Its cost is $\sum_{i} c_{v_i v_{i+1}}$ with $v_{n+1} = v_1$.

**Goal.** Minimize the cost. OPT is the least cost of a tour and ALG the cost of the returned tour. This page uses ALG $\le \rho \cdot \text{OPT}$ with $\rho \ge 1$; ratios are worst case unless the page says "in expectation" or "with high probability".

**The same problem without the triangle inequality.** On a strongly connected digraph with arc lengths, the least closed walk that visits every vertex equals OPT for the shortest path costs, which satisfy the directed triangle inequality. So "visit each vertex at least once" on any strongly connected digraph is an instance of this problem. Without either the triangle inequality or revisits, no ratio is possible, by the same argument as for [general TSP](/general-tsp-inapproximability/).

**The ATSP LP.** The directed form of the [subtour elimination LP](/subtour-elimination-lp/) has a variable $x_a \ge 0$ for each arc and the constraints

$$x(\delta^{+}(v)) = x(\delta^{-}(v)) = 1 \ \ (v \in V), \qquad x(\delta^{+}(S)) \ge 1 \ \ (\emptyset \ne S \subsetneq V),$$

where $\delta^{+}(S)$ is the set of arcs that leave $S$. Each tour is a 0/1 solution, so its value LP* is at most OPT. Without the cut constraints this LP is the [assignment problem](/assignment-problem/), whose 0/1 solutions are cycle covers.

## Variants

- **Symmetric TSP.** The special case $c_{uv} = c_{vu}$; see [metric TSP](/metric-tsp/). It has ratio $3/2$ and slightly below.
- **Symmetric in disguise.** If $c_{uv} = s_{uv} + h_v - h_u$ with $s$ symmetric and any numbers $h_v$, then the terms $h_v - h_u$ add up to 0 around each cycle. So each tour costs the same as for $s$, and the instance is symmetric TSP. A road cost with a fixed penalty per meter of climbing, $c_{uv} = d_{uv} + \max(0, h_v - h_u)$, has this form with $s_{uv} = d_{uv} + \tfrac12 |h_v - h_u|$, so a tour and its reverse always cost the same.
- **Path ATSP.** Find a directed Hamiltonian path from $s$ to $t$. Constant ratios are known here as well, through a reduction to ATSP by Feige and Singh (2007).
- **Without the triangle inequality, no revisits.** No polynomial ratio is possible unless P = NP.
- **Bottleneck ATSP.** Minimize the largest arc of the tour; see [bottleneck TSP](/bottleneck-tsp/) for the symmetric case.

## Examples

**One-way streets.** Eight places $A$ to $H$ are joined by one-way roads with lengths $AC\,3$, $BE\,4$, $CB\,2$, $DB\,2$, $DF\,3$, $DG\,4$, $EA\,3$, $EF\,1$, $EG\,4$, $FA\,4$, $FE\,2$, $GB\,4$, $GH\,2$ and $HD\,4$. The costs are the shortest path distances, so they satisfy the directed triangle inequality; for example $c_{AD} = 19$ but $c_{DA} = 7$. The values below were computed by a script, with OPT and each cycle cover found by trying all permutations.

| step | vertex set $S$ | least cycle cover of $S$ | cost | OPT on $S$ |
|---|---|---|---|---|
| round 1 | $A, \ldots, H$ | $A \to C \to B \to E \to F \to A$ and $D \to G \to H \to D$ | 24 | 26 |
| round 2 | $A, D$ (one vertex per cycle) | $A \to D \to A$ | 26 | 26 |
| stop | $A$ | | | |

The arcs of both rounds cost $24 + 26 = 50$. An Eulerian circuit of them is $A\,D\,G\,H\,D\,A\,C\,B\,E\,F\,A$, and shortcutting the second visits gives the tour $A\,D\,G\,H\,C\,B\,E\,F$ of cost 50. The optimal tour is $A\,C\,B\,E\,G\,H\,D\,F$ with cost 26, and its reverse costs 71. The ATSP LP has value 26 here, with the optimal tour as its solution. So ALG/OPT $= 50/26 \approx 1.92$, within the bound $\lfloor \log_2 8 \rfloor = 3$. Round 2 is the costly one: the two representatives $A$ and $D$ are far apart in both directions together.

**Random checks.** On 60 random instances of the same kind (shortest path costs of random one-way road networks, with 4 to 8 vertices and seeds 1982 to 2041), the algorithm stayed within $\lfloor \log_2 n \rfloor \cdot \text{OPT}$ each time, and its worst ratio was $1.375$.

## Known algorithms

| algorithm | ratio | type | status |
|---|---|---|---|
| repeated cycle cover (Frieze, Galbiati and Maffioli 1982) | $\lfloor \log_2 n \rfloor$ | deterministic, $O(n^3)$ | proved on this page |
| refined cycle covers (Bläser 2003; Kaplan, Lewenstein, Shafrir and Sviridenko 2005; Feige and Singh 2007) | $0.999 \log_2 n$, then $\tfrac43 \log_3 n$, then $\tfrac23 \log_2 n$ | deterministic | cited |
| [Asadpour et al.](/asadpour-atsp-algorithm/) (thin trees) | $O(\log n / \log \log n)$ | randomized, with high probability | outline on that page |
| Svensson, Tarnawski and Végh 2018 | a constant (5500 in the first version) | deterministic, polynomial | cited |
| Traub and Vygen 2020 | $22 + \varepsilon$ | deterministic, polynomial | cited |
| [Held-Karp dynamic program](/held-karp-algorithm/) | exact | $O(n^2 2^n)$ | exact algorithm |
| branch and bound with the assignment bound or with reduced costs, as in [Little's algorithm](/little-algorithm/) | exact | exponential | exact algorithm |

The algorithms after 2010 all round the ATSP LP. Anari and Oveis Gharan (2015) showed that its integrality gap is at most $(\log \log n)^{O(1)}$, by a proof that does not give an algorithm; Svensson, Tarnawski and Végh gave the first constant bound on the gap, and Traub and Vygen improved it to 22.

## Bounds

**The $\log_2 n$ ratio (proved here; Frieze, Galbiati and Maffioli 1982).** The algorithm:

1. Set $S = V$ and $F = \emptyset$ ($F$ is a multiset of arcs).
2. While $|S| \ge 2$: find a least-cost *cycle cover* $C$ of $S$, a set of directed cycles, each of length at least 2, that together pass through each vertex of $S$ once, with the costs $c$ restricted to $S$. Add the arcs of $C$ to $F$. Keep one vertex of each cycle, and let $S$ be the set of these vertices.
3. Find an [Eulerian circuit](/eulerian-circuit/) of $F$ and shortcut it to a tour.

*Lemma 1. Each cycle cover in step 2 costs at most OPT.* Let $H$ be an optimal tour. Walk along $H$ and keep only the vertices of $S$; by the directed triangle inequality, each arc of the new cycle costs at most the part of $H$ that it replaces, so this is a directed Hamiltonian cycle on $S$ of cost at most OPT. Since $|S| \ge 2$, it is one cycle of length at least 2, so it is a cycle cover of $S$, and the least cycle cover costs no more.

*Lemma 2. Step 2 runs at most $\lfloor \log_2 n \rfloor$ times.* Each cycle has at least 2 vertices and gives one vertex to the new $S$, so each round at least halves $|S|$. If round $r$ runs, then before it $2 \le |S| \le n / 2^{r-1}$, so $2^r \le n$ and $r \le \lfloor \log_2 n \rfloor$.

*Lemma 3. $F$ has an Eulerian circuit that passes through all of $V$.* Each cycle adds one arc into and one arc out of each of its vertices, so in $F$ each vertex has as many arcs in as out. For connection, the claim "each vertex of $V$ lies in the same strongly connected part of $F$ as some vertex of $S$" holds at the start, since $S = V$, and stays true in each round, because each old vertex of $S$ lies on a cycle with the vertex that its cycle keeps. When the loop stops, $S$ has one vertex $r$, so all of $V$ is strongly connected to $r$ in $F$. A directed multigraph with equal in-degree and out-degree at each vertex that is strongly connected has an Eulerian circuit.

*Theorem.* The tour costs at most $c(F) \le \lfloor \log_2 n \rfloor \cdot \text{OPT}$. *Proof.* Shortcutting the circuit does not raise the cost, by the directed triangle inequality applied along each skipped piece, as in the shortcut lemma of [metric TSP](/metric-tsp/). By Lemmas 1 and 2, $c(F)$ is the sum of at most $\lfloor \log_2 n \rfloor$ cycle covers of cost at most OPT each. $\blacksquare$

*Cost.* A least cycle cover of $S$ is a least-cost perfect matching between a copy of $S$ for the tails and a copy for the heads, with the pairs $(v, v)$ forbidden: a permutation with no fixed point is exactly a set of disjoint cycles of length at least 2. The [Hungarian algorithm](/hungarian-algorithm/) finds it in $O(|S|^3)$ time. The sizes halve, so the total time is $O(n^3)$.

**Lower bounds on OPT.** The least cycle cover of $V$ (the assignment bound) and the value LP* of the ATSP LP are both at most OPT. The integrality gap of the ATSP LP is at least 2 (Charikar, Goemans and Karloff 2006) and at most 22 (Traub and Vygen).

**Hardness (cited).** No polynomial algorithm reaches a ratio below $75/74$ unless P = NP (Karpinski, Lampis and Schmied 2015). The decision version is NP-complete, already for costs 1 and 2: a digraph on $n$ vertices has a directed Hamiltonian cycle exactly when the costs 1 on arcs and 2 on non-arcs, which satisfy the directed triangle inequality, give OPT $= n$.

## Reductions

- **From symmetric TSP.** A symmetric instance is an ATSP instance with $c_{uv} = c_{vu}$, so each ATSP ratio holds for the symmetric case. The converse fails: no method for symmetric TSP is known to give a constant ratio for ATSP.
- **To symmetric TSP, exactly.** Jonker and Volgenant (1983) replace each vertex $v$ by two vertices $v^{-}$ and $v^{+}$ with an edge of cost 0 between them, give the edge $\{u^{+}, v^{-}\}$ the cost $c_{uv} + M$ for a large $M$, and give all other edges a cost larger still. An optimal symmetric tour uses all $n$ edges of cost 0, so read in the right direction it passes $v^{-}, v^{+}$ for each $v$ and is an ATSP tour plus $nM$. This keeps optimal tours, but not ratios, because the new costs break the triangle inequality.
- **From directed Hamiltonian cycle.** The 1 and 2 costs above.
- **To the assignment problem.** Each cycle cover round is an [assignment problem](/assignment-problem/); the [Hungarian algorithm](/hungarian-algorithm/) solves it.

## Applications

- **Scheduling with setup times.** Jobs on one machine where the setup time from job $u$ to job $v$ depends on the order, for example in painting, printing and chemical batches; the cyclic order of jobs is an ATSP tour.
- **Routing on directed networks.** One-way streets, river currents, wind and slopes make travel costs directed.
- **Shortest common superstring.** The overlap graph of strings gives an ATSP instance, and approximation algorithms for the superstring problem use cycle covers in the same way as the algorithm above.
- **Theory.** ATSP drove much of the work on thin trees, maximum entropy distributions and LP rounding for routing problems.

## References
