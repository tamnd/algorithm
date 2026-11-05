---
tag: RMV7CH
kind: problem
slug: currency-arbitrage-detection
name: Currency arbitrage detection
aliases:
- Currency exchange / arbitrage
area: graphs/shortest-paths
level: core
summary: Finds a cycle of currency exchanges whose rate product exceeds one, which is a negative cycle in a graph with logarithmic edge weights.
prereqs: [arbitrage-detection, bellman-ford, negative-cycle-detection]
see_also: [currency-arbitrage, arbitrage-detection, negative-cycle, spfa, tarjan-subtree-disassembly, floyd-warshall, floating-point-arithmetic, karp-minimum-mean-cycle]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 22, Problem 22-3, Arbitrage (the weights -ln R[i][j], and printing the cycle when one exists); Section 22.1 for Bellman-Ford
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.4, Shortest Paths (the arbitrage client of the Bellman-Ford negative cycle finder)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 5, Section 5.5, Detecting negative cycles
---

Currency arbitrage detection is the computational task of taking a table of exchange rates and returning a cycle of currencies whose rates multiply to more than 1, or certifying that there is none. The standard method maps each rate $r$ to the edge weight $-\ln r$, adds a virtual source, runs [Bellman-Ford](/bellman-ford/) for $n$ passes, and walks back along the predecessors from an edge that can still be relaxed to read off a [negative cycle](/negative-cycle/). It takes $O(nm)$ time, $O(n^3)$ for a full table. The catch is numerical: logarithms in floating point can report a cycle whose true product is exactly 1.

## In plain words

Write each exchange rate as a cost: take its logarithm and flip the sign. Good rates become negative costs, bad rates positive ones. A loop of trades that makes money is now a loop whose costs add up to less than zero.

Start every currency at cost zero. Go over all the rates again and again, each time lowering a currency's cost if some trade reaches it more cheaply. Without a money-making loop, the costs settle within as many rounds as there are currencies. If a cost still drops after that, a loop is to blame. Follow the record of which trade last lowered each cost backward, and it leads into the loop.

Rounding can fool this test, so near-zero loops need care.

## Definition

**Input.** Currencies $1, \ldots, n$ and a list of $m$ quotes $(a, b, r)$ with $r > 0$: one unit of $a$ buys $r$ units of $b$, with spread and proportional fees already applied. Optionally, a home currency $s$.

**Output.** A list of currencies $a_1, \ldots, a_k$ with $r(a_1, a_2) \cdots r(a_{k-1}, a_k) \cdot r(a_k, a_1) > 1$, or "no arbitrage". If a home currency is given, only cycles reachable from $s$ count.

**Weight assumptions.** The weights $w(a, b) = -\ln r(a, b)$ are real numbers of either sign, not integers, and negative cycles are expected, so neither [Dijkstra's algorithm](/dijkstra/) (which needs nonnegative weights) nor algorithms that assume no negative cycle apply. Currencies with no path from $s$ have distance $+\infty$ and play no part.

## Variants

- **All cycles or from a home currency.** For all cycles, start every estimate at 0, which is the same as a virtual source with an edge of weight 0 to every currency. For a home currency $s$, start only $d[s]$ at 0.
- **All arbitrage currencies.** List every currency that lies on some profitable cycle. [Floyd-Warshall](/floyd-warshall/) does this in $\Theta(n^3)$: the currencies with a negative diagonal entry are exactly those on a negative cycle.
- **Exact arithmetic.** Relax on amounts instead of logarithms: $q(b) \leftarrow \max(q(b), q(a) \cdot r(a, b))$, with rational numbers. A cycle is profitable exactly when the products say so.
- **With a profit threshold.** Report only cycles with product above $1 + \varepsilon$, which absorbs rounding and small costs. With weights, this is a cycle of weight below $-\ln(1 + \varepsilon)$, which needs the [minimum mean cycle](/minimum-mean-cycle-problem/) or a search with a shifted weight, not plain Bellman-Ford.
- **Streaming quotes.** When rates change one at a time, keep the distances and re-run only from the changed edge, as in [SPFA](/spfa/).

## Examples

**A run.** Currencies USD, EUR, GBP, JPY and the quotes, in this order: USD→EUR 0.9, EUR→USD 1.1, EUR→GBP 0.8, GBP→USD 1.4, USD→JPY 150, JPY→USD 0.0066, GBP→JPY 190. Their weights are 0.10536, −0.09531, 0.22314, −0.33647, −5.01064, 5.02069, −5.24702. Every estimate starts at 0.

| after pass | USD | EUR | GBP | JPY |
|---|---|---|---|---|
| 1 | −0.33647 | 0 | 0 | −5.34711 |
| 2 | −0.34444 | −0.23111 | −0.00797 | −5.35508 |
| 3 | −0.35241 | −0.23908 | −0.01594 | −5.36304 |
| 4 | −0.36038 | −0.24705 | −0.02390 | −5.37101 |

Pass 4 is pass $n$, and it still lowers estimates, so a negative cycle exists. The predecessors are USD ← GBP, EUR ← USD, GBP ← EUR, JPY ← USD. Walking back from USD gives USD, GBP, EUR, USD, and reversing it gives the cycle USD → EUR → GBP → USD, with product $0.9 \cdot 0.8 \cdot 1.4 = 1.008$. Each pass lowers the three estimates on the cycle by its weight $0.00797$.

**No arbitrage.** With GBP→USD 1.38 instead, the estimates stop changing before pass 4, and the answer is "no arbitrage". The final estimates are the logarithms of consistent prices: $p(c) = e^{-d[c]}$ satisfies $r(a, b) \le p(b)/p(a)$ for every quote.

**An unreachable cycle.** Add CHF→SEK 11 and SEK→CHF 0.1, with no quote into CHF or SEK from the others. From the home currency USD, both stay at $+\infty$, and no cycle is reported. With every estimate started at 0, the CHF-SEK cycle (product 1.1) is reported.

**A false alarm from rounding.** In [floating-point arithmetic](/floating-point-arithmetic/), quote USD→EUR 0.7, EUR→GBP 1.3 and GBP→USD $1/0.91$, rounded to a double. The exact product of the decimal quotes 0.7 and 1.3 and the exact value $100/91$ is 1, and the product of the three doubles also rounds to 1.0. But in double precision, $-\ln 0.7 - \ln 1.3 - \ln(1/0.91)$ evaluates to about $-2.8 \cdot 10^{-17}$, a negative cycle. A test $d[u] + w < d[v]$ with no tolerance reports an arbitrage that does not exist.

## Known algorithms

1. **Bellman-Ford with a virtual source** (CLRS Problem 22-3, Sedgewick and Wayne 4.4). Set $d[c] = 0$ for every currency, relax every quote for $n$ passes, and if pass $n$ still relaxes an edge into $v$, follow $\pi$ from $v$ for $n$ steps to land on the cycle, then follow $\pi$ around it. Time $O(nm)$, space $O(n)$.
2. **Early termination.** Stop as soon as a pass makes no change: then there is no arbitrage. On rate tables without arbitrage this often ends after a few passes.
3. **[SPFA](/spfa/) with periodic cycle checks** or [subtree disassembly](/tarjan-subtree-disassembly/): the same worst case, usually faster.
4. **Floyd-Warshall** for all currencies on profitable cycles, $\Theta(n^3)$.
5. **Triangle enumeration** for triangular arbitrage only, $O(n^3)$ checks of $r(a, b)\, r(b, c)\, r(c, a)$.

## Bounds

The time is $O(nm)$ by Bellman-Ford and $\Omega(m)$ because every quote must be read. For a full table both Bellman-Ford and Floyd-Warshall take $\Theta(n^3)$ in the worst case. Floating-point Bellman-Ford can err only on cycles whose true weight is within a few rounding units of 0, roughly $k \cdot 2^{-52}$ times the sum of $|\ln r|$ along a cycle of $k$ edges; with a tolerance of that size the answers are correct for every cycle outside that band.

## Reductions

- **To negative cycle detection** by $r \mapsto -\ln r$, and back by $w \mapsto e^{-w}$; see [arbitrage detection](/arbitrage-detection/).
- **Certificate of no arbitrage.** When Bellman-Ford ends without a change, the estimates $d$ satisfy $d[b] \le d[a] - \ln r(a, b)$ for every quote, so $p = e^{-d}$ is a set of prices under which no quote is better than fair. A checker needs only $O(m)$ time to verify it. When a cycle is returned, its product is the certificate.

## Applications

The detection routine is the core of the scans described on [currency arbitrage](/currency-arbitrage/): checking quoted cross rates for errors, finding short-lived opportunities in foreign exchange and in cryptocurrency markets, and checking that a venue's own prices admit no profitable cycle. The same routine finds inconsistent cycles in any table of conversion factors.

## References
