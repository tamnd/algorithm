---
tag: 8F990D
kind: problem
slug: parameterized-dominating-set
name: Parameterized dominating set
aliases: []
area: complexity/parameterized-complexity
level: advanced
summary: "Decide whether a graph has a dominating set of size k, with k as the parameter. W[2]-complete; n^(k+o(1)) time for k >= 7, and no O(n^(k-e)) algorithm for k >= 3 unless SETH fails."
prereqs: [dominating-set, fixed-parameter-tractable, w-hierarchy]
see_also: [dominating-set, set-cover, parameterized-hitting-set, w-hardness, parameterized-clique, strong-exponential-time-hypothesis, bidimensionality-theory, parameterized-inapproximability]
sources:
  - paper: doi:10.1137/S0097539792228228
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness I: basic results, SIAM Journal on Computing 24(4), 873-921 (1995)"
    locator: dominating set is W[2]-complete
  - paper: "Mihai Pătraşcu and Ryan Williams, On the possibility of faster SAT algorithms, Proceedings of the 21st ACM-SIAM Symposium on Discrete Algorithms (SODA 2010), 1065-1075"
    locator: the n^(k+o(1)) algorithm for k >= 7 and the SETH lower bound for every k >= 3
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 13 (the reduction from multicolored independent set and W[2]-membership), Chapter 14 (ETH and SETH lower bounds) and Chapter 7 (planar graphs and bidimensionality)
  - paper: doi:10.1145/990308.990309
    title: "Jochen Alber, Michael R. Fellows and Rolf Niedermeier, Polynomial-time data reduction for dominating set, Journal of the ACM 51(3), 363-384 (2004)"
    locator: a kernel with at most 335k vertices on planar graphs
  - paper: doi:10.1137/050646354
    title: "Jianer Chen, Henning Fernau, Iyad A. Kanj and Ge Xia, Parametric duality and kernelization: lower bounds and upper bounds on kernel size, SIAM Journal on Computing 37(4), 1077-1106 (2007)"
    locator: a kernel with at most 67k vertices for planar dominating set
---

Parameterized dominating set, p-Dominating-Set, asks whether a graph has $k$ vertices such that every vertex is chosen or has a chosen neighbor, with the size $k$ as the [parameter](/parameter/). It is the standard W[2]-complete problem (Downey and Fellows 1995), one level above [clique](/parameterized-clique/) in the [W-hierarchy](/w-hierarchy/). The trivial algorithm takes time about $n^{k+1}$; Pătraşcu and Williams (2010) brought it to $n^{k + o(1)}$ for $k \ge 7$ and proved that no $O(n^{k - \varepsilon})$ algorithm exists for any $k \ge 3$ unless the Strong Exponential Time Hypothesis fails. This page gives the parameterized view only; the [dominating set](/dominating-set/) page has the classical problem and its approximation.

## In plain words

You want to place a given number of fire stations in a network of towns so that every town has a station or is next to a town with one. The question is whether the given number is enough.

Trying every choice of towns works, but the cost grows like the number of towns raised to the number of stations. For this problem experts believe that you cannot do much better: a method that saved even a small part of that power would also give a much faster general method for logic puzzles, which most researchers think does not exist. On maps that can be drawn without crossings, the problem is much easier.

## Definition

The input is a graph $G = (V, E)$ with $n = |V|$ and $m = |E|$, given by adjacency lists, and a number $k$. The closed neighborhood of $v$ is $N[v] = \{v\} \cup \{u : uv \in E\}$. A set $D \subseteq V$ is *dominating* if $\bigcup_{v \in D} N[v] = V$. The least size of a dominating set is $\gamma(G)$.

**p-DOMINATING-SET**

- Instance: a graph $G = (V, E)$ and an integer $k \ge 0$.
- Parameter: $k$.
- Question: does $G$ have a dominating set $D$ with $|D| \le k$?

A superset of a dominating set dominates, so for $k \le n$ "at most $k$" and "exactly $k$" give the same answer. A yes-instance has a certificate of $k$ vertex names, checked in $O(n + m)$ time.

**Complexity.** p-Dominating-Set is W[2]-complete under [parameterized reductions](/parameterized-reduction/) (Downey and Fellows 1995, SIAM Journal on Computing 24). Membership: the formula $\bigwedge_{v \in V} \bigvee_{u \in N[v]} x_u$ is a monotone CNF, a circuit of weft 2, and its satisfying assignments of weight $k$ are the dominating sets of size $k$. The classical problem is NP-complete.

## Variants

- *Set cover and hitting set.* Set cover with $k$ sets and [hitting set](/parameterized-hitting-set/) with $k$ elements and unbounded set size are W[2]-complete as well, by the reductions below. With sets of size at most $d$, hitting set is FPT for each fixed $d$.
- *Parameter $n - k$.* If $G$ has no isolated vertex, then $\gamma(G) \le n/2$ (Ore). Isolated vertices must be in every dominating set, so remove them and lower $k$. With $\ell = n - k$ as the parameter, either $n \ge 2\ell$ and the answer is yes, or $n < 2\ell$, a kernel. So this dual parameterization is FPT, while the parameter $k$ is W[2]-complete.
- *Planar graphs.* On [planar graphs](/planar-graph/) the problem is FPT with a kernel of at most $335k$ vertices (Alber, Fellows and Niedermeier 2004), later $67k$ vertices (Chen, Fernau, Kanj and Xia 2007). [Bidimensionality](/bidimensionality-theory/) gives time $2^{O(\sqrt{k})} n^{O(1)}$. The problem stays NP-complete on planar graphs, so $k$ is needed in the bound.
- *Treewidth.* With the [treewidth](/treewidth/) of a given tree decomposition as the parameter, [dynamic programming](/dp-on-tree-decompositions/) decides the problem in FPT time, for any $k$.

## Examples

The Petersen graph has 10 vertices of degree 3, so each closed neighborhood has 4 vertices. Two vertices dominate at most 8 vertices, so $\gamma \ge 3$. Its numbers of dominating sets of sizes 1 to 5 are 0, 0, 10, 75 and 192. So $\gamma = 3$: (Petersen, 3) is a yes-instance and (Petersen, 2) is a no-instance.

A worked SETH reduction. Take the CNF formula with the four clauses $(x_1 \vee x_2 \vee \neg x_3)$, $(\neg x_1 \vee x_3 \vee x_4)$, $(\neg x_2 \vee \neg x_3 \vee \neg x_4)$ and $(x_1 \vee \neg x_2 \vee x_4)$, and split the variables into $k = 2$ blocks $\{x_1, x_2\}$ and $\{x_3, x_4\}$. The graph has:

- for each block $i$, a clique on its 4 partial assignments and an extra vertex $y_i$ joined to those 4 vertices only;
- for each clause, one vertex joined to every partial assignment, of either block, that makes one of its literals true.

The graph has $2 \cdot 4 + 2 + 4 = 14$ vertices and 40 edges. The formula has 8 satisfying assignments, and the graph has 9 dominating sets of size 2. A satisfying assignment, say $x_1 = 1, x_2 = 0, x_3 = 0, x_4 = 1$, maps to the set of its two partial assignments $\{(1, 0), (0, 1)\}$, which dominates both blocks, both $y_i$ and every clause vertex. Conversely, each dominating set of size 2 must dominate $y_1$ and $y_2$, so it has one vertex in each block, or $y_i$ itself in place of a block vertex. Its block vertices satisfy every clause, and any values for a block with no chosen vertex complete them. For example, $\{y_1, (0, 1)\}$ dominates the graph because $x_3 = 0, x_4 = 1$ alone satisfies all four clauses.

## Known algorithms

- *Brute force.* Try all $\binom{n}{k}$ sets and check each in $O(n + m)$ time: $O(n^{k+1})$ in dense graphs. The problem is in [XP](/xp/).
- *Pătraşcu and Williams (2010).* Time $n^{k + o(1)}$ for every $k \ge 7$, with fast rectangular matrix multiplication. The idea goes back to Eisenbrand and Grandoni (2004).
- *Planar graphs.* Time $2^{O(\sqrt{k})} n^{O(1)}$ by bidimensionality, after a linear kernel. See [bidimensionality theory](/bidimensionality-theory/).
- *Exact algorithms in $n$.* For the minimum dominating set without a parameter, branching with [measure and conquer](/measure-and-conquer/) gives time $O(c^n)$ for constants $c < 2$.

## Bounds

- *W[2]-completeness.* No algorithm in time $f(k) \cdot n^{O(1)}$ unless $\mathsf{FPT} = \mathsf{W}[2]$, and no kernel of any size under the same condition.
- *ETH bound.* Conditional on the [Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), there is no algorithm in time $f(k) \cdot n^{o(k)}$. The reduction from multicolored independent set below keeps $k' = k$, so the bound for [independent set](/parameterized-independent-set/) (Chen, Huang, Kanj and Xia 2006) carries over.
- *SETH bound.* Conditional on the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), for every $k \ge 3$ and every $\varepsilon > 0$ there is no $O(n^{k - \varepsilon})$ algorithm (Pătraşcu and Williams 2010). With the reduction of the example, a formula with $N$ variables and $M$ clauses gives a graph with $k \cdot 2^{N/k} + k + M$ vertices, and an $O(n^{k - \varepsilon})$ algorithm would decide it in time $2^{(1 - \varepsilon/k) N} M^{O(1)}$, which SETH forbids. With the upper bound, this pins the exponent at $k$ for $k \ge 7$.
- *Approximation.* Whether an FPT algorithm can approximate the least size is studied on [parameterized inapproximability](/parameterized-inapproximability/).

## Reductions

- *To set cover, k' = k.* The universe is $V$ and the sets are the $N[v]$; $D$ dominates $G$ exactly when $\{N[v] : v \in D\}$ covers $V$.
- *From set cover, k' = k.* Given a universe $U$, a family $\mathcal{F}$ and $k \le |\mathcal{F}|$, if some element is in no set, output a fixed no-instance. Otherwise make one vertex for each set and join all of them into a clique, and one vertex for each element, joined to the sets that contain it. A cover of $k$ sets dominates the graph. Conversely, in a dominating set, replace each element vertex by a set that contains it; the result still dominates, because every set vertex dominates all the set vertices. The sets that remain cover $U$.
- *To weighted CNF satisfiability, k' = k.* One clause $\bigvee_{u \in N[v]} x_u$ for each vertex. See [weighted satisfiability](/weighted-satisfiability/).
- *From multicolored independent set, k' = k.* Make each class $V_i$ a clique, add two vertices $x_i, y_i$ joined to all of $V_i$, and for each edge $uv$ with $u \in V_i$, $v \in V_j$ add a vertex $w_{uv}$ joined to every vertex of $V_i \cup V_j$ except $u$ and $v$. A dominating set of size $k$ must take one vertex of each $V_i$ to dominate $x_i$ and $y_i$, and $w_{uv}$ is dominated exactly when the chosen pair in $V_i \cup V_j$ is not $\{u, v\}$. This is the textbook proof that dominating set is W[1]-hard, and it gives the ETH bound.
- *From CNF-SAT, for SETH,* as in the worked example.

## Applications

- *Facility placement.* Placing $k$ facilities so that each site has one at distance at most 1 is dominating set; larger radii are dominating set in a power of the graph. The hardness explains why exact solvers need small $k$ or planar structure.
- *Monitoring.* Placing $k$ monitors in a network so that every node is watched by a neighbor is the same problem.
- *Source of W[2]-hardness.* Dominating set and set cover are the usual starting points for W[2]-hardness proofs.

## References
