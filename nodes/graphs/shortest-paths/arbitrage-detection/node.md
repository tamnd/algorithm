---
tag: KFJGX0
kind: problem
slug: arbitrage-detection
name: Arbitrage detection
area: graphs/shortest-paths
level: core
summary: Problem of finding a cycle of currency exchanges whose rates multiply to more than one, found via negative cycles.
prereqs: [negative-cycle, negative-cycle-detection, bellman-ford]
see_also: [currency-arbitrage, currency-arbitrage-detection, negative-cycle-detection, floyd-warshall, minimum-mean-cycle-problem, karp-minimum-mean-cycle, potential-function-reduced-costs, longest-path-problem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 22, Problem 22-3, Arbitrage (the reduction to a negative cycle with weights -ln R[i][j], and printing the cycle)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.4, Shortest Paths (negative cycles and the arbitrage application)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 5, Section 5.5, Detecting negative cycles; Chapter 15, Generalized flows (gains on arcs and flow-generating cycles)
---

Arbitrage detection is the problem of finding, in a directed graph whose edges carry positive multipliers, a cycle whose multipliers have a product greater than 1. The standard case is a table of currency exchange rates, where such a cycle turns a sum of money into more of the same money. Taking the weight $-\ln r$ for an edge with rate $r$ turns products into sums and "greater than 1" into "less than 0", so the problem is exactly [negative cycle detection](/negative-cycle-detection/), solved by [Bellman-Ford](/bellman-ford/) in $O(nm)$ time.

## In plain words

Picture a set of goods that can be traded for one another at fixed rates. One unit of the first buys a certain amount of the second, one unit of the second buys some of the third, and so on.

Follow a loop of trades back to where you started. Multiply the rates along the loop. If the result is more than one, you end with more than you began with, and you can repeat the loop as often as you like. That loop is an arbitrage. The problem is to find one, or to show that none exists.

Logarithms turn the multiplying into adding. With a minus sign, a profitable loop becomes a loop with a negative total, which the standard shortest-path tools can already find.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, and a rate $r(u, v) > 0$ on each edge. Optionally, a start vertex $s$.

**Output.** A directed cycle $C = (v_1, v_2, \ldots, v_k, v_1)$ with

$$\prod_{i=1}^{k} r(v_i, v_{i+1}) > 1 \qquad (v_{k+1} = v_1),$$

or a report that no such cycle exists. With a start vertex $s$, the cycle must be reachable from $s$ (and, if the profit is to come back as $s$, the cycle must also reach $s$).

**The weight transform.** Set $w(u, v) = -\ln r(u, v)$. Then for each cycle $C$,

$$\prod_{e \in C} r(e) > 1 \iff \sum_{e \in C} \ln r(e) > 0 \iff w(C) < 0.$$

The weights $w$ are real numbers of any sign; a rate below 1 gives a positive weight and a rate above 1 a negative one. There is no assumption that weights are nonnegative or integers, and negative cycles are the very object sought, so the algorithms used must allow them.

## Variants

- **Decision or search.** Decide whether an arbitrage exists, or return one cycle. Bellman-Ford does both in the same time.
- **From a fixed start.** Only cycles that the start vertex $s$ can reach count. A vertex that $s$ cannot reach, and any cycle through it, is out of play.
- **All cycles.** With no start vertex, every cycle counts. Add a new vertex with an edge of rate 1 to every vertex, or start every estimate at 0, and run Bellman-Ford once.
- **Best arbitrage.** Find the cycle with the largest product. For simple cycles this is NP-hard, since it contains the [longest cycle problem](/longest-path-problem/) (see Bounds).
- **Best rate per trade.** Maximize the geometric mean of the rates on a cycle. With weights $-\ln r$, this is the [minimum mean cycle problem](/minimum-mean-cycle-problem/), solved by [Karp's algorithm](/karp-minimum-mean-cycle/) in $O(nm)$ time.
- **With capacities.** If each exchange has a volume limit, the most money that can be made is a [linear program](/linear-programming-problem/) on a network with gains (generalized flow), not a cycle problem.
- **The financial setting.** Bid and ask rates, fees and triangular arbitrage are on [currency arbitrage](/currency-arbitrage/); the detection routine and its numerical issues are on [currency arbitrage detection](/currency-arbitrage-detection/).

## Examples

**An arbitrage.** Four currencies with the rates USD→EUR 0.9, EUR→USD 1.1, EUR→GBP 0.8, GBP→USD 1.4, USD→JPY 150, JPY→USD 0.0066 and GBP→JPY 190. The cycles and their products are:

| cycle | product | weight $\sum -\ln r$ |
|---|---|---|
| USD → EUR → USD | 0.99 | 0.01005 |
| USD → JPY → USD | 0.99 | 0.01005 |
| USD → EUR → GBP → USD | 1.008 | −0.00797 |
| USD → EUR → GBP → JPY → USD | 0.90288 | 0.10217 |

The cycle USD → EUR → GBP → USD is an arbitrage: 1000 dollars become 900 euros, then 720 pounds, then 1008 dollars. It is also the only negative cycle.

**No arbitrage.** Change GBP→USD to 1.38. The three-currency cycle has product $0.9 \cdot 0.8 \cdot 1.38 = 0.9936 < 1$, and every cycle weight is positive. Bellman-Ford ends with no edge left to relax.

**An unreachable cycle.** Add CHF and SEK with CHF→SEK 11 and SEK→CHF 0.1 (product 1.1), and no edge from the other four currencies into them. From the start USD, the CHF-SEK cycle is not reachable, so a holder of dollars cannot use it; Bellman-Ford from USD leaves CHF and SEK at $\infty$ and reports nothing about them. With every estimate started at 0, the same cycle is found.

## Known algorithms

| algorithm | finds | time |
|---|---|---|
| [Bellman-Ford](/bellman-ford/) with an extra pass and a walk back along predecessors | one negative cycle | $O(nm)$ |
| [SPFA](/spfa/) with [subtree disassembly](/tarjan-subtree-disassembly/) | one negative cycle, often fast in practice | $O(nm)$ |
| [Floyd-Warshall](/floyd-warshall/) | a negative diagonal entry for every vertex on a negative cycle | $\Theta(n^3)$ |
| [Karp's algorithm](/karp-minimum-mean-cycle/) | the cycle with the best mean rate | $O(nm)$ |
| [Near-linear negative SSSP](/near-linear-negative-sssp/) | one negative cycle, integer weights only | $O(m \log^{O(1)} n \log W)$ |

The near-linear algorithms need integer weights, so they apply to rates only after rounding the logarithms to a fixed precision.

## Bounds

- **Upper bound.** $O(nm)$ by Bellman-Ford. For complete rate tables, $m = n(n - 1)$ and the time is $O(n^3)$, the same as Floyd-Warshall.
- **Hardness of the best cycle.** Deciding whether some simple cycle has product at least a given value is [NP-complete](/np-complete/). Give each edge of a directed graph the rate $e$, so a cycle with $k$ edges has product $e^k$; a product of at least $e^n$ means a cycle through all $n$ vertices, a [Hamiltonian cycle](/hamiltonian-cycle-problem/).
- **Unbounded profit.** If the cycle may be repeated, any arbitrage can be run again and again, and the product has no upper bound; so "best" makes sense only for simple cycles or per trade.

## Reductions

- **To negative cycle detection.** Map each rate $r$ to the weight $-\ln r$. A cycle is an arbitrage if and only if its weight is negative.
- **From negative cycle detection.** Map each weight $w$ to the rate $e^{-w}$. A cycle is negative if and only if its product exceeds 1. So the two problems are the same problem, up to the cost of the logarithms.
- **No arbitrage and prices.** There is no arbitrage if and only if there are prices $p(v) > 0$ with $r(u, v) \le p(v) / p(u)$ for every edge: the [potentials](/potential-function-reduced-costs/) $\ln p$ of the shortest-path optimality conditions. When no arbitrage exists, distances from an added source give such prices.

## Applications

- **Foreign exchange.** Triangular arbitrage among three currencies, and longer cycles, in quoted rates; see [currency arbitrage](/currency-arbitrage/).
- **Decentralized exchanges.** Cycles of trading pools whose marginal prices multiply to more than 1.
- **Consistency checks.** A table of conversion factors, such as units or prices quoted by different sources, is consistent exactly when no cycle has product other than 1; testing for arbitrage in both directions finds the inconsistent cycles.
- **Gain networks.** In flow networks with gains, a cycle with product above 1 creates flow; AMO Chapter 15 calls it a flow-generating cycle.

## References
