---
tag: GSS56Z
kind: algorithm
slug: jain-iterative-rounding-network-design
name: Jain iterative rounding for network design
aliases:
- Jain 2-approximation for SNDP
- Jain's algorithm for the generalized Steiner network problem
area: approximation/lp-rounding
level: advanced
summary: Solve the cut LP, buy every edge with value at least 1/2, and repeat on the residual requirements; a vertex always has such an edge, so the cost is at most twice the LP.
solves: [survivable-network-design, generalized-steiner-network]
model: real-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, L: the time to find a vertex solution of one cut LP}
  time: {worst: O(m L)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2001
  people: [Kamal Jain]
  note: Jain proved that each vertex of the cut LP of a weakly supermodular requirement has an edge with value at least 1/2, and so gave the first constant factor approximation for the survivable network design problem with general requirements.
prereqs: [generalized-steiner-network, lp-relaxation, extreme-point, edge-connectivity, submodular-function, separation-oracle]
see_also: [iterative-rounding, iterative-relaxation, survivable-network-design, goemans-williamson-steiner-forest, steiner-forest, primal-dual-schema, ellipsoid-method, max-flow-min-cut-theorem]
sources:
  - paper: doi:10.1007/s004930170004
    title: Kamal Jain, A factor 2 approximation algorithm for the generalized Steiner network problem, Combinatorica 21(1), 2001
    locator: the main theorem (an extreme point has an edge with value at least 1/2) and the algorithm built on it
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 11.3 (the survivable network design problem)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 23 (Steiner network)
  - book: isbn:9781107007512
    title: Lap Chi Lau, R. Ravi and Mohit Singh, Iterative Methods in Combinatorial Optimization
    locator: Chapter 10 (network design), with the token counting proof
  - paper: doi:10.1016/j.orl.2010.02.006
    title: Viswanath Nagarajan, R. Ravi and Mohit Singh, Simpler analysis of LP extreme points for traveling salesman and survivable network design problems, Operations Research Letters 38(3), 2010
    locator: the fractional token argument used in the proof file
---

Jain's algorithm is a 2-approximation for the [survivable network design problem](/survivable-network-design/): given a graph with edge costs and a number $r_{uv}$ for each pair of vertices, buy the cheapest set of edges that has $r_{uv}$ edge-disjoint paths between each $u$ and $v$. It is the first and main example of [iterative rounding](/iterative-rounding/). The algorithm solves the cut LP for a vertex solution, buys every edge whose value is at least $1/2$, lowers the requirements by the bought edges, and solves again. The key fact, Jain's theorem, is that every vertex of the LP has an edge with value at least $1/2$, so each round makes progress. Each bought edge costs at most twice its LP value, so the total cost is at most twice the first LP value, and so at most $2 \cdot \text{OPT}$.

## In plain words

You must buy roads so that certain towns are joined by enough separate routes. First solve a relaxed problem where you may buy part of a road, such as half of it. Look at the answer. If some road is bought at least halfway, buy all of it; that costs at most twice what the relaxed answer paid for it.

Now the roads you bought already give some of the needed routes, so the remaining needs are smaller. Solve the relaxed problem again for what is left, and repeat until all needs are met.

The deep part is a promise: in a corner answer of the relaxed problem, at least one road is always bought halfway or more. So you never get stuck. Each round, the relaxed cost drops by at least half of what you spend, so you spend at most twice the first relaxed cost.

## The problem

The input is an undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, costs $c_e \ge 0$, and a nonnegative integer $r_{uv}$ for each pair of vertices. Each edge may be bought once. A set $F \subseteq E$ is feasible if, for each pair, $F$ has $r_{uv}$ edge-disjoint $u$-$v$ paths. By [Menger's theorem](/menger-theorem/), this holds exactly when $|F \cap \delta(S)| \ge f(S)$ for each $S \subseteq V$, where $\delta(S)$ is the set of edges with one end in $S$, and

$$f(S) = \max \{ r_{uv} : |S \cap \{u, v\}| = 1 \},$$

with $f(S) = 0$ when $S$ separates no pair. For a set $F$ of bought edges, the residual requirement is $g(S) = f(S) - |F \cap \delta(S)|$, and the cut LP on the other edges is

$$\min \sum_{e \in E \setminus F} c_e x_e \ \text{ s.t. } \ x(\delta(S) \setminus F) \ge g(S) \text{ for each } S \subseteq V, \quad 0 \le x_e \le 1.$$

The bound $x_e \le 1$ is needed, since each edge may be bought once. With $F = \emptyset$, the incidence vector of each feasible set is a point of this LP, so the LP value is at most OPT. The proof uses only that $f$ is *weakly supermodular* (see the proof file), so the algorithm works for every such requirement function. The [generalized Steiner network](/generalized-steiner-network/) page has more on the LP.

## The algorithm

```pseudo id=main
JAIN-ITERATIVE-ROUNDING(G, c, r)
L1  F ← ∅
L2  while g(S) = f(S) − |F ∩ δ(S)| > 0 for some S do
L3      find a vertex x of the cut LP on E \ F with residual requirement g
L4      if the LP is infeasible then return "the requirements cannot be met"
L5      H ← { e ∈ E \ F : x_e ≥ 1/2 }
L6      F ← F ∪ H
L7  return F
```

Line L3 must return a vertex (an [extreme point](/extreme-point/)) of the LP, not just any optimal point; the theorem below is about vertices. The simplex method gives one directly. The LP has a row for each subset of $V$, but it has a polynomial [separation oracle](/separation-oracle/): for a point $x$, give each bought edge capacity 1 and each other edge capacity $x_e$, and for each pair compute a minimum $u$-$v$ cut by [max flow](/max-flow-problem/); a cut of capacity less than $r_{uv}$ is a violated row. So the [ellipsoid method](/ellipsoid-method/) solves the LP in polynomial time and can be made to return a vertex. Line L5 never gives an empty set, by Jain's theorem, so each round buys at least one edge, and there are at most $m$ rounds.

## Example

Take vertices $a, b, c, d, e$ with the edges and costs below, and the requirements $r_{ab} = 1$, $r_{ac} = 1$ and $r_{ad} = 2$. So $a$ and $d$ need two edge-disjoint paths.

| edge | $ab$ | $bc$ | $ca$ | $cd$ | $de$ | $ea$ | $bd$ |
|---|---|---|---|---|---|---|---|
| cost $c_e$ | 1 | 1 | 1 | 2 | 2 | 2 | 4 |
| LP vertex $x_e$ | 1/2 | 0 | 1 | 1 | 1/2 | 1/2 | 1/2 |
| bought in round 1 | yes | no | yes | yes | yes | yes | yes |

The LP value is $1/2 + 1 + 2 + 1 + 1 + 2 = 15/2$. The cut around $a$ has value $x_{ab} + x_{ca} + x_{ea} = 2$, as $r_{ad} = 2$ requires, and so does the cut around $d$: $x_{cd} + x_{de} + x_{bd} = 2$. The cut around $b$ has value $1 = r_{ab}$. Every edge except $bc$ has $x_e \ge 1/2$, so round 1 buys six edges. These already give all requirements: $a$ and $d$ are joined by $a c d$, $a e d$ and $a b d$. So the loop ends after one round.

The algorithm pays $1 + 1 + 2 + 2 + 2 + 4 = 12 \le 2 \cdot 15/2 = 15$. The optimum is $8$, with the edges $ab, ca, cd, de, ea$: the paths $a c d$ and $a e d$ join $a$ and $d$. So the ratio here is $12 / 8 = 3/2$. The edge $bd$ cost the most for its use: the LP paid $2$ for half of it, and the algorithm paid $4$.

## Correctness

**Theorem (Jain 2001).** Let $f$ be weakly supermodular with integer values, $F \subseteq E$, and let $x$ be a vertex of the cut LP on $E \setminus F$ with residual requirement $g = f - |F \cap \delta(\cdot)|$, where $g(S) > 0$ for some $S$. Then $x_e \ge 1/2$ for some edge $e$.

The proof has three steps, given in full in the proof file below.

1. *Weak supermodularity.* For every two sets $A$ and $B$, $g(A) + g(B) \le g(A \cap B) + g(A \cup B)$ or $g(A) + g(B) \le g(A \setminus B) + g(B \setminus A)$. This holds for $f$ by a case check on where the pairs that give $f(A)$ and $f(B)$ lie, and subtracting the cut function of $F$ keeps it.
2. *Uncrossing.* Remove the edges with $x_e = 0$. If some $x_e = 1$, the theorem holds. Otherwise $x$ is fixed by $|E'|$ independent tight cut rows, and two tight crossing sets can be replaced by two tight sets that do not cross. So some *laminar* family $\mathcal{L}$ of $|E'|$ tight sets has independent rows.
3. *Counting.* If all $x_e < 1/2$, each edge $e = uv$ gives $x_e$ to the smallest set of $\mathcal{L}$ that holds $u$, $x_e$ to the smallest that holds $v$, and $1 - 2 x_e$ to the smallest that holds both. Each set of $\mathcal{L}$ gets an integer amount that is positive, so at least 1. But a maximal set of $\mathcal{L}$ has an edge in its cut whose share $1 - 2x_e > 0$ goes to no set. So the total given is less than $|E'| = |\mathcal{L}|$, a contradiction.

**The ratio.** Let $x$ be the vertex of some round, $H$ the edges it buys, and $\text{LP}$, $\text{LP}'$ the values of this round and the next. The point $x$ restricted to $E \setminus (F \cup H)$ is feasible for the next LP, since removing $H$ lowers each cut by at most $|H \cap \delta(S)|$, the same amount that $H$ lowers the requirement. So $\text{LP}' \le \text{LP} - \sum_{e \in H} c_e x_e \le \text{LP} - c(H)/2$, that is, $c(H) \le 2(\text{LP} - \text{LP}')$. The sum over all rounds telescopes, with the value 0 after the last round, to

$$c(F) \le 2 \cdot \text{LP}_1 \le 2 \cdot \text{OPT}.$$

This also shows that each LP after the first is feasible.

**The lower bound used.** The value $\text{LP}_1$ of the first cut LP, with $x_e \le 1$.

**Tight example.** On a cycle of odd length $k$ with unit costs and $r_{uv} = 1$ for all pairs, the only optimal vertex is $x_e = 1/2$ on every edge, with value $k/2$. The algorithm buys all $k$ edges, so its cost is exactly $2 \cdot \text{LP}_1$, while OPT is $k - 1$. So the factor 2 against the LP cannot be improved, and the [integrality gap](/integrality-gap/) of the cut LP tends to 2 as $k$ grows.

## Complexity

- **Time.** At most $m$ rounds, since each round buys at least one edge, and each round solves one LP for a vertex, in time $L$. With the ellipsoid method and a separation oracle that runs $O(n^2)$ max-flow computations, or $n - 1$ of them with a [Gomory-Hu tree](/gomory-hu-tree/), $L$ is polynomial in $n$, $m$ and the bit size of the costs. The total is $O(m L)$ in the worst case. This is polynomial, but slow in practice.
- **Space.** The bought set, the residual data and the current vertex take $O(n + m)$ extra space, besides the LP solver.

## Properties

- **Ratio 2 for every weakly supermodular $f$.** The proof never uses the special form of $f$, only weak supermodularity and integer values. This covers Steiner forest, Steiner tree, $k$-edge-connected spanning subgraph and their mixes.
- **The best known ratio.** No algorithm with ratio below 2 is known for the general problem, and 2 matches the integrality gap of the cut LP.
- **Deterministic.** With a fixed LP solver that returns a fixed vertex, the output depends only on the input.
- **Threshold 1/2 is fixed.** Buying only the edges with $x_e = 1$ can get stuck, since a vertex may have no integral edge, as on the odd cycle.

## Variants and improvements

- **Earlier methods.** Williamson, Goemans, Mihail and Vazirani (1995) gave a primal-dual $2 r_{\max}$ ratio, where $r_{\max} = \max r_{uv}$, and Goemans, Goldberg, Plotkin, Shmoys, Tardos and Williamson (1994) improved it to $2 \mathcal{H}(r_{\max})$, with $\mathcal{H}$ the harmonic number. For $r_{uv} \in \{0, 1\}$, the [Goemans-Williamson](/goemans-williamson-steiner-forest/) primal-dual algorithm gives $2 - 2/k$ with no LP solving.
- **Element connectivity.** Fleischer, Jain and Williamson (2006) extended iterative rounding to paths that must not share edges or non-terminal vertices, with ratio 2.
- **Vertex connectivity.** When the paths must be vertex-disjoint, the problem is much harder, and no constant ratio is known for general requirements; see [vertex connectivity](/vertex-connectivity/).
- **Degree bounds.** [Iterative relaxation](/iterative-relaxation/) adds degree bounds: Lau, Naor, Salavatipour and Singh (2007) get cost at most $2 \cdot \text{OPT}$ with each degree at most $2 b_v + 3$.
- **A simpler count.** Nagarajan, Ravi and Singh (2010) replaced Jain's original counting with the fractional token argument used here.

## When to use it

Use it when the network must survive edge failures with different needs for different pairs, and a provable factor 2 matters more than speed. For $0$-$1$ requirements, the primal-dual algorithm of Goemans and Williamson is faster and needs no LP solver, with a slightly better ratio. In practice, an integer programming solver with cut separation often solves moderate instances exactly, and the LP of this algorithm is its relaxation.

## Pitfalls

- **Using an optimal point that is not a vertex.** Jain's theorem holds only for vertices. An optimal point in the middle of a face can have all values below $1/2$, and then line L5 buys nothing.
- **Dropping $x_e \le 1$.** Without the upper bound, the LP can put value above 1 on a cheap edge, the rounding buys it once, and the requirement is not met.
- **Not lowering the requirement.** After buying $H$, the next LP must use $g(S) = f(S) - |F \cap \delta(S)|$ on the edges not yet bought. Solving the original LP again gives the same vertex and no progress.
- **Rounding everything at once.** Buying all edges with $x_e > 0$ in one round can cost far more than $2 \cdot \text{OPT}$; it is the rounds of re-solving that keep the factor 2.

## Implementations

## History

Agrawal, Klein and Ravi (1995) and Goemans and Williamson (1995) gave factor 2 for $0$-$1$ requirements by primal-dual methods. For general requirements, the primal-dual ratios grew with $r_{\max}$: $2 r_{\max}$ by Williamson, Goemans, Mihail and Vazirani (1995) and $2 \mathcal{H}(r_{\max})$ by Goemans, Goldberg, Plotkin, Shmoys, Tardos and Williamson (1994). Jain (1998 conference, 2001 journal) studied the vertices of the cut LP instead, proved that one coordinate is always at least $1/2$, and so got factor 2 for all requirements. The method, called iterative rounding, has since been used for many other problems, and with iterative relaxation it led to the bounded degree results of Singh and Lau (2007).

## References
