---
tag: C7A0S3
kind: concept
slug: update-query-tradeoff
name: Update-query tradeoff
aliases:
- update-time versus query-time tradeoff
area: graphs/dynamic-graphs
level: core
summary: Dynamic structures often trade faster updates for slower queries, or the reverse.
prereqs: [dynamic-graph, amortized-update-time]
see_also: [worst-case-update-time, dynamic-partial-sums-lower-bound, dynamic-connectivity-lower-bound, dynamic-lower-bounds, fenwick-tree, square-root-decomposition, dynamic-connectivity, dynamic-transitive-closure]
sources:
  - paper: doi:10.1137/S0097539705447256
    title: Mihai Pătraşcu and Erik D. Demaine, Logarithmic lower bounds in the cell-probe model, SIAM Journal on Computing 35(4), 932 to 963 (2006)
    locator: the main theorems (trade-offs between update time and query time for partial sums and for dynamic connectivity)
  - paper: doi:10.1145/2746539.2746609
    title: Monika Henzinger, Sebastian Krinninger, Danupon Nanongkai and Thatchaphol Saranurak, Unifying and strengthening hardness for dynamic problems via the online matrix-vector multiplication conjecture, Proceedings of STOC 2015, 21 to 30
    locator: Section 1 (conditional lower bounds stated as pairs of update time and query time)
  - paper: doi:10.1145/502090.502095
    title: Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Poly-logarithmic deterministic fully-dynamic algorithms for connectivity, minimum spanning tree, 2-edge, and biconnectivity, Journal of the ACM 48(4), 723 to 760 (2001)
    locator: the connectivity theorem (O(log^2 n) amortized update time with O(log n / log log n) query time)
  - paper: "Liam Roditty and Uri Zwick, Improved dynamic reachability algorithms for directed graphs, SIAM Journal on Computing 37(5), 1455 to 1471 (2008)"
    locator: the main theorems (fully dynamic reachability with update time and query time traded against each other)
---

The update-query tradeoff is the observation that a dynamic data structure can usually make its updates cheaper by making its queries more expensive, or the reverse, by choosing how much of the answer it computes in advance. At one extreme, an update only records the change and a query computes the answer from scratch; at the other, an update recomputes every answer and a query only reads one. Good structures sit between the extremes, and for many problems, such as [dynamic connectivity](/dynamic-connectivity/) and prefix sums, lower bounds show exactly which pairs of update time and query time are possible.

## In plain words

A structure that answers questions about changing data has two kinds of work: work when the data changes, and work when someone asks. It can do the work early or late. If it does everything at change time, every question is instant, but every change is slow. If it does nothing at change time, every change is instant, but every question is slow.

Most good designs split the work: they do some at change time and keep a summary that makes questions fast enough. Which split is best depends on how many changes and how many questions the program expects. Some problems also have a floor: no split makes both kinds of work small at the same time.

## The idea

Let a dynamic structure have update time $t_u$ and query time $t_q$ (each worst case, amortized or expected, as stated). A program that performs $U$ updates and $Q$ queries pays

$$U \cdot t_u + Q \cdot t_q,$$

so the best structure for it is the one that minimizes this sum, not the one with the smallest $t_u$ or the smallest $t_q$ alone.

**The two extremes.** Every dynamic problem has two trivial solutions. *Lazy:* store the input, and compute the answer on each query, so $t_u = O(1)$ and $t_q = T_{\text{static}}$, the time of the best static algorithm. *Eager:* recompute and store all possible answers after each update, so $t_u = T_{\text{all}}$ and $t_q = O(1)$. A nontrivial dynamic algorithm must beat both on the sum above for some mix of $U$ and $Q$.

**Parameters in between.** Many structures have a parameter $b$ that moves along a curve between the extremes. Blocks of size $b$, trees of degree $b$ and rebuilding after $b$ updates are the usual knobs. Choosing $b$ to equalize the two costs gives the balanced point, such as $O(n^{1/2})$ for both in a [square root decomposition](/square-root-decomposition/).

**Lower bounds as trade-off curves.** A lower bound for a dynamic problem is often a statement about the pair $(t_u, t_q)$, not about one of them. Pătraşcu and Demaine (2006) proved in the [cell-probe model](/cell-probe-model/) that both the prefix sums problem and fully dynamic connectivity satisfy

$$t_q \cdot \lg\!\left(2 + \frac{t_u}{t_q}\right) = \Omega(\lg n) \qquad\text{and}\qquad t_u \cdot \lg\!\left(2 + \frac{t_q}{t_u}\right) = \Omega(\lg n),$$

with amortized costs. So $\max\{t_u, t_q\} = \Omega(\log n)$, and making one side much smaller than $\log n$ forces the other side to grow: with $t_q = O(1)$, the first inequality needs $\lg(t_u) = \Omega(\lg n)$, so $t_u = n^{\Omega(1)}$. The precise statement and proof for prefix sums are on the [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/) page. Conditional lower bounds from the [OMv conjecture](/omv-conjecture/) are also stated as forbidden pairs: for several graph problems they rule out a structure whose update time and query time are both polynomially smaller than the trivial bounds; see [dynamic lower bounds](/dynamic-lower-bounds/).

**Amortized against worst case.** The trade-off curve depends on the measure. Amortized bounds allow periodic rebuilding, which often moves the curve; a [worst-case update time](/worst-case-update-time/) bound may sit on a worse curve.

## Examples

**Prefix sums on 16 numbers.** Keep $A[1..16]$ under "add $x$ to $A[i]$" and "return $A[1] + \cdots + A[i]$". The table counts the cells written by an update and the cells read by a query, in the worst case.

| structure | update | query |
|---|---|---|
| plain array (lazy) | 1 | 16 |
| array of prefix sums (eager) | 16 | 1 |
| blocks of 4 with block sums | 2 | 7 |
| [Fenwick tree](/fenwick-tree/) | 5 | 4 |

The plain array and the prefix array are the two extremes. Blocks of size $b$ cost 2 per update and up to $n/b - 1 + b$ reads per query, here $3 + 4 = 7$. The Fenwick tree costs $\lfloor \lg n \rfloor + 1$ writes per update and at most $\lfloor \lg n \rfloor$ reads per query, the balanced point that the lower bound above shows to be optimal up to a constant factor. A tree of degree $b$ instead of 2 moves along the curve: $O(\log_b n)$ per update and $O(b \log_b n)$ per query.

**Dynamic connectivity.** Lazy: store the edges and run a [breadth-first search](/breadth-first-search/) per query, $t_u = O(1)$ and $t_q = O(n + m)$. Eager: recompute the [connected components](/connected-components/) after each update, $t_u = O(n + m)$ and $t_q = O(1)$. The [Holm-de Lichtenberg-Thorup algorithm](/holm-de-lichtenberg-thorup/) has $t_u = O(\log^2 n)$ amortized and $t_q = O(\log n / \log\log n)$ worst case. By the first trade-off inequality, a query time of $\Theta(\log n / \log\log n)$ forces $\lg(2 + t_u/t_q) = \Omega(\log\log n)$, so $t_u / t_q \ge (\lg n)^{\Omega(1)}$: the update must be slower than the query by a polylogarithmic factor. In this algorithm the ratio is $\Theta(\log n \log\log n)$.

**Dynamic reachability in directed graphs.** The eager method keeps the full [transitive closure](/transitive-closure/): queries take $O(1)$ time, and Demetrescu and Italiano update it in $O(n^2)$ amortized time per update; see [dynamic transitive closure](/dynamic-transitive-closure/). Roditty and Zwick (2008) give points with cheaper updates and slower queries, such as $O(m n^{1/2})$ amortized update time with $O(n^{1/2})$ query time. The lazy method, a graph search per query, has $t_u = O(1)$ and $t_q = O(m)$.

**Choosing a point.** A program with $U = 10^6$ updates and $Q = 10$ queries on a graph with $m = 10^5$ edges should prefer the lazy connectivity structure: about $10^6 + 10 \cdot 10^5 = 2 \cdot 10^6$ steps, against about $10^6 \cdot 10^5 = 10^{11}$ for the eager one. With $Q = 10^6$ and $U = 10$ the order reverses.

## Where it is used

- **Stating results.** A result for a dynamic problem is a pair, or a curve, of update time and query time; tables of results for [dynamic connectivity](/dynamic-connectivity/), [dynamic reachability](/dynamic-reachability/) and [dynamic all-pairs shortest paths](/dynamic-all-pairs-shortest-paths/) list both.
- **Lower bounds.** The [dynamic connectivity lower bound](/dynamic-connectivity-lower-bound/) and the [dynamic partial sums lower bound](/dynamic-partial-sums-lower-bound/) are trade-off curves in the cell-probe model.
- **Design.** [Square root decomposition](/square-root-decomposition/), trees of higher degree and periodic rebuilding are the standard ways to move along the curve; the [Fenwick tree](/fenwick-tree/) and the [segment tree](/segment-tree/) sit at the balanced point for prefix sums.
- **Choosing a structure.** For a known ratio of updates to queries, pick the point that minimizes $U t_u + Q t_q$; for real-time limits on each operation, see [worst-case update time](/worst-case-update-time/).

## References
