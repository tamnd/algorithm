---
tag: M3JJEH
kind: problem
slug: currency-arbitrage
name: Currency arbitrage detection
aliases:
- Arbitrage
area: graphs/shortest-paths
level: core
summary: Find a cycle of currency exchanges whose rate product exceeds one by detecting a negative cycle with Bellman-Ford on log rates.
prereqs: [arbitrage-detection, negative-cycle, bellman-ford]
see_also: [arbitrage-detection, currency-arbitrage-detection, negative-cycle-detection, minimum-mean-cycle-problem, karp-minimum-mean-cycle, potential-function-reduced-costs, lp-duality, floyd-warshall]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 22, Problem 22-3, Arbitrage
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.4, Shortest Paths (the arbitrage application of negative cycle detection, with a table of exchange rates)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 15, Generalized flows (gains, flow-generating cycles, and currency exchange as an example)
  - url: https://en.wikipedia.org/wiki/Triangular_arbitrage
    title: Wikipedia, Triangular arbitrage
    locator: the definition and the role of bid-ask spreads and transaction costs
---

Currency arbitrage is a sequence of currency exchanges that starts and ends in the same currency and returns more money than it started with; detecting it means finding a cycle in the graph of exchange rates whose rates multiply to more than 1. With edge weights $-\ln r$, such a cycle is a [negative cycle](/negative-cycle/), so [Bellman-Ford](/bellman-ford/) finds one in $O(nm)$ time. This page covers the financial side: what the rates are, how spreads and fees enter, and which versions of "the best arbitrage" are easy or hard. The general problem is [arbitrage detection](/arbitrage-detection/), and the detection routine is on [currency arbitrage detection](/currency-arbitrage-detection/).

## In plain words

A bank quotes how many euros you get for a dollar, how many pounds for a euro, and so on. If you change dollars to euros, euros to pounds, and pounds back to dollars, you may end with a little more than you started with. That loop is an arbitrage, and if it exists you could repeat it forever.

Real quotes have two prices, one to buy and one to sell, and the gap between them is the bank's margin. Fees take a further cut. Once both are counted, loops with a profit are rare and small.

To find one, turn each rate into a cost with a logarithm and a minus sign. A profitable loop then has a negative total cost, and a shortest-path method that finds negative loops does the rest.

## Definition

**Input.** A set of $n$ currencies and, for some ordered pairs $(a, b)$, a rate $r(a, b) > 0$: one unit of $a$ buys $r(a, b)$ units of $b$, after the spread and any proportional fee. Missing pairs cannot be traded directly. Optionally, a home currency $s$.

**Output.** A cycle of currencies $a_1 \to a_2 \to \cdots \to a_k \to a_1$ with $r(a_1, a_2) \cdots r(a_k, a_1) > 1$, or a report that none exists. With a home currency, the cycle must be reachable from $s$ by a sequence of trades and must lead back to $s$.

**Weight assumptions.** With $w(a, b) = -\ln r(a, b)$, an arbitrage is a negative cycle. The weights are real, of either sign, and not integers. A rate above 1, such as USD→JPY 150, gives a large negative weight on its own, which is why only whole cycles are judged. Quoted rates are usually decimal numbers with a few digits, so the products are exact rationals, but their logarithms are not; see the floating-point notes on [currency arbitrage detection](/currency-arbitrage-detection/).

## Variants

- **Bid and ask.** A pair has a bid $b$ and an ask $a > b$ for the price of one unit of the base currency in the quote currency. Selling the base gives the rate $b$; buying it gives the rate $1/a$. The round trip has product $b / a < 1$, so no two-currency loop is ever an arbitrage.
- **Fees.** A fee that takes a fraction $f$ of each trade multiplies each rate by $1 - f$, and a cycle of $k$ trades loses a factor $(1 - f)^k$. A fixed fee per trade is not a rate; it makes the profit depend on the amount traded.
- **Triangular arbitrage.** Only cycles of three currencies, in practice through a common currency such as the dollar. Checking all of them takes $O(n^3)$ time with no graph algorithm.
- **Best mean rate.** Maximize the average gain per trade, the geometric mean of the rates. This is the [minimum mean cycle problem](/minimum-mean-cycle-problem/) on the weights $-\ln r$, solvable in $O(nm)$.
- **Best simple cycle.** Maximize the product over simple cycles. This is NP-hard; see [arbitrage detection](/arbitrage-detection/).
- **With volume limits.** If each quote holds only up to some amount, the largest profit is a [linear program](/linear-programming-problem/) over a network with gains (a generalized flow problem), solved by LP or by special generalized flow algorithms.

## Examples

**A profitable cycle.** Rates USD→EUR 0.9, EUR→GBP 0.8, GBP→USD 1.4. Starting with 1000 dollars: 900 euros, then 720 pounds, then 1008 dollars, a profit of 0.8 percent. The weights are $-\ln 0.9 = 0.10536$, $-\ln 0.8 = 0.22314$ and $-\ln 1.4 = -0.33647$, with sum $-0.00797 < 0$.

**The same cycle after fees.** A fee of 0.5 percent per trade multiplies the product by $0.995^3 \approx 0.98507$, giving $1.008 \cdot 0.98507 \approx 0.99295 < 1$. The arbitrage is gone. A fee of $f$ per trade removes every cycle of $k$ trades with product below $(1 - f)^{-k}$.

**No arbitrage from consistent prices.** If each currency has a price $p$ in some unit and every rate is $r(a, b) = p(b) / p(a)$, every cycle has product exactly 1. If every rate is at most $p(b) / p(a)$, as bid-ask spreads ensure, every cycle has product at most 1, and there is no arbitrage. Bellman-Ford ends with no edge to relax, and its distances give such prices.

**A cycle the holder cannot reach.** Suppose the CHF→SEK→CHF loop has product 1.1, but no quote converts dollars into francs or kronor. A holder of dollars cannot use it, and a search from USD correctly does not report it. A search over all cycles does report it.

## Known algorithms

- **[Bellman-Ford](/bellman-ford/) on $-\ln r$**, with a virtual source of weight-0 edges to every currency or a home currency, and the cycle extracted from the predecessors: $O(nm)$, which is $O(n^3)$ for a full table.
- **[Floyd-Warshall](/floyd-warshall/)** on $-\ln r$: $\Theta(n^3)$, with a negative diagonal entry for every currency on a negative cycle. For a full rate table it costs the same as Bellman-Ford.
- **Multiplicative relaxation.** Run Bellman-Ford directly on rates: keep the best amount $q(b)$ obtainable and relax $q(b) \leftarrow \max(q(b), q(a) \cdot r(a, b))$. This avoids logarithms and can use exact rationals.
- **[Karp's algorithm](/karp-minimum-mean-cycle/)** for the best mean rate: $O(nm)$.
- **Enumeration** of the $O(n^3)$ triangles for triangular arbitrage.

## Bounds

The rate table can be complete, with $m = n(n - 1)$, so the Bellman-Ford bound is $O(n^3)$. Each rate must be read in the worst case, since an unread rate could close a profitable cycle; so $\Omega(m)$ is a lower bound. Finding the most profitable simple cycle is NP-hard. The time to compute logarithms is $O(m)$ calls, negligible next to the search.

## Reductions

- **To negative cycles.** The map $r \mapsto -\ln r$ sends arbitrage cycles to negative cycles and back.
- **No-arbitrage and duality.** "No arbitrage" is the feasibility of the system $\ln p(b) - \ln p(a) \ge \ln r(a, b)$, a system of [difference constraints](/difference-constraints/) in the unknowns $\ln p$. By [LP duality](/lp-duality/), it is infeasible exactly when a cycle of constraints sums to a contradiction, which is a profitable cycle. So the rates admit no arbitrage if and only if there are consistent prices, a one-period, no-uncertainty form of the link between no-arbitrage and prices in finance.
- **Generalized flow.** With volume limits, the problem is a generalized maximum flow, and a flow-generating cycle with spare capacity is an arbitrage.

## Applications

- **Trading.** Banks and trading firms scan quoted rates for triangular and longer cycles. Real opportunities last only a short time and are small, so speed of detection and exact fee accounting matter more than asymptotic time.
- **Checking quotes.** A set of quoted cross rates should have no arbitrage after spreads; a cycle found by the check points at a stale or wrong quote.
- **Exchange design.** Venues and automated market makers check that their own posted prices do not admit cycles with profit.

## References
