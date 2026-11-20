---
tag: MZRKQA
kind: algorithm
slug: dpsv-algorithm
name: Devanur-Papadimitriou-Saberi-Vazirani algorithm
aliases:
- DPSV algorithm
- primal-dual Fisher market algorithm
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: advanced
summary: Computes an equilibrium of a linear Fisher market in polynomial time by raising prices and computing max flows in a primal-dual way.
model: real-ram
complexity:
  vars: {n: the number of buyers, m: the number of goods, U: the largest utility, M: the total budget}
  time: {worst: "O(m^4 (log m + m log U + log M))"}
  space: {extra: O(n m)}
properties: {deterministic: true, recursive: false}
history:
  year: 2002
  people: [Nikhil R. Devanur, Christos H. Papadimitriou, Amin Saberi, Vijay V. Vazirani]
  note: The algorithm appeared at FOCS 2002. The journal version (2008) fixed a flaw in the first running time analysis with balanced flows.
prereqs: [fisher-market, eisenberg-gale-program, max-flow-min-cut-theorem]
see_also: [orlin-fisher-market-algorithm, proportional-response-dynamics, tatonnement, kkt-conditions, edmonds-karp, demange-gale-sotomayor-auction, competitive-equilibrium, arrow-debreu-market]
sources:
  - paper: doi:10.1145/1411509.1411512
    title: "Nikhil R. Devanur, Christos H. Papadimitriou, Amin Saberi and Vijay V. Vazirani, Market equilibrium via a primal-dual algorithm for a convex program, Journal of the ACM 55(5), Article 22 (2008)"
    locator: "Section 3 (the network N(p) and the Invariant), Section 5 (Algorithm 1 and Lemma 5.1), Section 6 (Lemma 6.4, finding the tight set), Section 7 (Lemma 7.1 and Corollary 7.5), Section 8 (balanced flows and the polynomial bound)"
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 5, Vijay V. Vazirani, Combinatorial algorithms for market equilibria
  - paper: doi:10.1145/1806689.1806731
    title: "James B. Orlin, Improved algorithms for computing Fisher's market clearing prices, STOC 2010, 291-300"
    locator: the whole paper (a strongly polynomial algorithm, which answers the open question that the DPSV paper states)
  - paper: doi:10.1214/aoms/1177706369
    title: "Edmund Eisenberg and David Gale, Consensus of subjective probabilities: the pari-mutuel method, Annals of Mathematical Statistics 30(1), 165-168 (1959)"
    locator: the whole paper (the convex program whose KKT conditions the algorithm satisfies)
---

The DPSV algorithm, by Devanur, Papadimitriou, Saberi and Vazirani, computes the exact equilibrium of a [Fisher market](/fisher-market/) with linear utilities. It was the first combinatorial polynomial time algorithm for this problem. It is a primal-dual algorithm for the [Eisenberg-Gale program](/eisenberg-gale-program/): the prices are the dual variables, the money that flows from buyers to goods is the primal solution, and the algorithm is guided by the [KKT conditions](/kkt-conditions/) of the program instead of by [LP duality](/lp-duality/). Prices start low and only go up. At all times, every good can be sold to buyers who like it best per unit of money, and the only defect is that buyers may keep money that they cannot spend. A [maximum flow](/max-flow-min-cut-theorem/) tells which sets of goods are already as expensive as they can be, and the algorithm raises the prices of the other goods until the surplus money is gone. The simple version below is easy to state and is exact, but its proven bound is exponential; the journal version adds balanced flows to get a polynomial bound, and [Orlin's algorithm](/orlin-fisher-market-algorithm/) later made the bound strongly polynomial.

## In plain words

Each buyer has money and likes each good to some degree. At given prices, a buyer only wants the goods that give her the most pleasure for each coin. Start with prices so low that every buyer could buy everything she wants, and make sure every good is wanted by someone. Then raise prices slowly, all by the same factor. At some point a group of goods becomes exactly as expensive as the total money of the buyers who want them. Those goods and their buyers are done, so freeze them and keep raising the other prices. If a buyer who is still active starts to like a frozen good as much as her own, wake up that frozen group again. When every good is frozen, every coin is spent and every good is sold.

## The problem

There are $n$ buyers and $m$ goods, with one unit of each good. Buyer $i$ has a budget $e_i > 0$ and a linear utility $\sum_j u_{ij} x_{ij}$ with $u_{ij} \ge 0$. Every buyer likes some good and every good is liked by some buyer. Find prices $p > 0$ and an allocation in which every buyer spends her whole budget on goods of maximum *bang per buck* $u_{ij} / p_j$ and every good is sold completely. This is the Fisher market equilibrium, and the prices are unique.

At prices $p$, let $\alpha_i = \max_j u_{ij} / p_j$. The *equality graph* has an edge $(i, j)$ when $u_{ij} / p_j = \alpha_i$. The network $N(p)$ has arcs from a source to each good $j$ with capacity $p_j$, from good $j$ to buyer $i$ with infinite capacity on every equality edge, and from buyer $i$ to a sink with capacity $e_i$. For a set $S$ of goods, $\Gamma(S)$ is the set of buyers joined to $S$ by an equality edge, $p(S) = \sum_{j \in S} p_j$ and $e(\Gamma(S)) = \sum_{i \in \Gamma(S)} e_i$. The algorithm keeps the *Invariant* of the paper: the cut that separates the source from everything else is a minimum cut of $N(p)$. By the [max-flow min-cut theorem](/max-flow-min-cut-theorem/), this holds exactly when $p(S) \le e(\Gamma(S))$ for every set $S$ of goods (Lemma 5.1 of the paper). A set $S$ is *tight* when $p(S) = e(\Gamma(S))$. Prices are an equilibrium exactly when the whole set of goods is also tight, so that a maximum flow saturates both the source arcs and the sink arcs.

## The algorithm

The goods are split into *active* goods and *frozen* blocks. Each frozen block comes with its buyers, who are also frozen. The equality graph of the active part uses only active buyers, with $\alpha_i$ taken over active goods. All arithmetic is exact.

```pseudo id=main
DPSV(utilities u, budgets e)
L1  p_j ← min_i e_i / m for every good j
L2  p_j ← max_i u_ij / α_i for every good j, where α_i = max_k u_ik / p_k at the prices of L1
L3  all goods and all buyers are active; no block is frozen
L4  while some good is active do
L5      (x1, S) ← the least factor x ≥ 1 at which a set of active goods goes tight, and the largest such set S
L6      x2 ← min over active buyers i and frozen goods j with u_ij > 0 of α_i p_j / u_ij  (∞ if none)
L7      multiply the price of every active good by x = min(x1, x2)
L8      if x2 < x1 then make the frozen block that contains the good of x2 active again, with its buyers
L9      else freeze S with its buyers Γ(S) as a new block
L10 compute a maximum flow in N(p) and read the money that buyer i spends on good j from it
L11 return p and the money flows
```

Line L1 makes every price so low that the goods together cost at most the smallest budget. Line L2 lowers the price of each good until some buyer has it among her best buys, so every good has an edge; prices only go down in line L2, and the Invariant holds because every set of goods costs at most $\min_i e_i$ and has at least one buyer.

Line L5 is Section 6 of the paper. Raising the active prices by a factor $x$ multiplies $p(S)$ by $x$ and keeps the equality graph of the active part, so a set $S$ goes tight at $x = e(\Gamma(S)) / p(S)$, and $x_1$ is the least of these ratios. Start with $S$ the set of all active goods and $x = e(\Gamma(S)) / p(S)$. Compute a maximum flow in the network of $S$ with the source arcs scaled by $x$. If it has value $e(\Gamma(S))$, return $(x, S)$. Otherwise, replace $S$ by the goods on the source side of the minimum cut whose source side is largest (the nodes that cannot reach the sink in the residual graph), and repeat. Each round removes at least one good (Lemma 6.3 of the paper), so line L5 costs at most $m$ maximum flows (Lemma 6.4).

Line L6 finds the first factor at which an active buyer $i$ starts to like a frozen good $j$ as much as her best active goods. Line L8 is the event in which this happens before any set goes tight; line L9 is the event in which a set goes tight first, and it also covers ties.

## Example

Three buyers and three goods with $u_1 = (1, 4, 3)$, $u_2 = (4, 2, 1)$, $u_3 = (1, 1, 2)$ and budgets $e = (1, 1, 3)$. Line L1 sets every price to $1/3$, and line L2 keeps it: buyer 1 likes good 2 best, buyer 2 likes good 1 best, and buyer 3 likes good 3 best.

| iteration | active goods | $x_1$ and the largest tight set | $x_2$ | event | prices after |
|---|---|---|---|---|---|
| 1 | 1, 2, 3 | $3$, goods $\{1, 2\}$ with buyers $\{1, 2\}$ | none | freeze $\{1, 2\}$ at factor $3$ | $(1, 1, 1)$ |
| 2 | 3 | $3$, good $\{3\}$ with buyer $\{3\}$ | $2$, buyer 3 and good 1 | unfreeze $\{1, 2\}$ at factor $2$ | $(1, 1, 2)$ |
| 3 | 1, 2, 3 | $5/4$, all goods with all buyers | none | freeze all at factor $5/4$ | $(5/4, 5/4, 5/2)$ |

In iteration 1 the set $\{1, 2\}$ has ratio $e(\{1, 2\}) / p(\{1, 2\}) = 2 / (2/3) = 3$, the set $\{3\}$ has ratio $9$, and all goods together have ratio $5$. In iteration 2, buyer 3 has bang per buck $2$ on good 3, and goods 1 and 2 give her $1$ per unit of money; when good 3 costs twice as much, they tie, so $x_2 = 2 < 3 = x_1$. In iteration 3, buyer 3 is indifferent between all three goods, and all goods together cost $4$ while the budgets add up to $5$, so the ratio is $5/4$. The flow of line L10 lets buyer 1 spend $1$ on good 2, buyer 2 spend $1$ on good 1, and buyer 3 spend $1/4$, $1/4$ and $5/2$ on goods 1, 2 and 3. In units, buyer 1 gets $4/5$ of good 2, buyer 2 gets $4/5$ of good 1, and buyer 3 gets $1/5$ of goods 1 and 2 and all of good 3, and every buyer's bang per buck on her goods is her maximum.

For the market $u_1 = (2, 1)$, $u_2 = (1, 2)$ with budgets $(1, 1)$, line L1 gives prices $(1/2, 1/2)$, the whole set goes tight at factor $2$, and the algorithm returns $p = (1, 1)$, with each buyer spending her budget on her favorite good.

## Correctness

The proof is in `proofs/correctness.md`. It keeps four invariants at the start of each iteration: the Invariant holds for the active part; no active buyer strictly prefers a frozen good to her best active goods; every frozen block is tight, satisfies the Invariant on its own, and its buyers like its goods best among all goods; and all prices are positive. Line L5 returns the true least factor and the largest tight set, because every set that goes tight first stays on the source side of every minimum cut. Prices never fall. After line L9 the remaining active part has no tight set, which bounds the number of iterations at a fixed price vector; and the prices of goods at the moments they are frozen or at which an unfreeze happens come from a finite set fixed by $u$ and $e$, which bounds the number of iterations that raise prices. At the end every block is tight and every buyer is frozen, so the flow of line L10 spends every budget on best goods and sells every good.

## Complexity

Each iteration costs at most $m + 1$ maximum flows on $n + m + 2$ nodes and at most $nm + n + m$ arcs. With Edmonds-Karp, as in the implementation, one flow costs $O((n + m) (nm)^2)$ exact operations on rationals. With integer utilities and budgets, Corollary 7.5 of the paper bounds its Algorithm 1 by at most $M \Delta^2$ phases and $O(M m^2 \Delta^2)$ max-flow computations, where $\Delta = m U^m$. This bound is exponential in $m$, and the paper does not know a polynomial bound for this version.

The balanced-flow version of Section 8 raises only the prices of goods next to buyers with large surplus, measured in a flow that minimizes the $\ell_2$ norm of the surplus vector. It needs $O(m^4 (\log m + m \log U + \log M))$ max-flow computations, which is polynomial in the bit length of the input. It is not strongly polynomial: the number of flows depends on $U$ and $M$. The extra space is $O(nm)$ for the network and the flows.

## Properties

- **Prices only rise.** Every factor in line L7 is at least $1$. Equality edges still appear and disappear, because the bang per buck of a buyer falls when her goods get dearer.
- **Exact and rational.** With rational data, every price is rational, and the output is exact. Lemma 7.1 of the paper bounds the denominators of the prices of a newly tight set by $\Delta = m U^m$, which also shows that the equilibrium has polynomial bit length.
- **Primal-dual with KKT conditions.** At all times buyers spend only on equality edges and no buyer has a better good than her edges; only the condition that each buyer spends her whole budget is relaxed, and it holds at the end.
- **Deterministic.** The output is the unique equilibrium price vector, with one equilibrium allocation.

## Variants and improvements

- **Balanced flows.** The polynomial version of Section 8 measures progress by the $\ell_2$ norm of the surplus vector, which falls by a polynomial factor in each phase.
- **Strongly polynomial.** [Orlin's algorithm](/orlin-fisher-market-algorithm/) (2010) combines the same flow network with scaling and finds the equilibrium with a number of operations that depends only on $n$ and $m$.
- **Other utilities.** The paper and the AGT book chapter describe extensions of the primal-dual approach, for example to spending constraint utilities (Vazirani). For utilities that are not linear, some market problems are PPAD-hard; see [PPAD-hardness of market equilibria](/ppad-hardness-of-arrow-debreu/).
- **Dynamics instead of algorithms.** [Proportional response dynamics](/proportional-response-dynamics/) and [tatonnement](/tatonnement/) approach the same equilibrium without a central planner, but only in the limit.

## When to use it

Use it when an exact equilibrium of a linear Fisher market is needed and the market is small or medium sized, and when exact rational prices matter more than speed. It is also a good model for primal-dual algorithms that are guided by KKT conditions. For large markets where an approximate answer is enough, a convex solver on the [Eisenberg-Gale program](/eisenberg-gale-program/) or [proportional response dynamics](/proportional-response-dynamics/) is simpler. For guaranteed worst-case bounds, use the balanced-flow version or [Orlin's algorithm](/orlin-fisher-market-algorithm/).

## Pitfalls

- Starting with prices that are too high in line L1 breaks the Invariant before the first iteration: a buyer who wants a set of goods may not be able to pay for it, and later tight sets are then wrong. The prices of line L1 must cost at most the smallest budget together.
- Skipping line L2 leaves goods with no equality edge. Such a good has no buyer, so the set that contains only it violates $p(S) \le e(\Gamma(S))$.
- Raising all prices in line L7, frozen ones included, breaks the tight blocks: their price then exceeds the money of their buyers.
- Freezing $S$ in line L9 without its buyers leaves buyers whose money is already used up by $S$ in the active part, so their budgets are counted twice in later tight sets.
- Floating point arithmetic in lines L2, L5 and L6 makes the equality tests $u_{ij} / p_j = \alpha_i$ fail at random, so edges are lost. Use exact rationals.
- Reading the allocation from the last flow of line L5 is wrong, because that flow covers only the last active part. Line L10 computes a fresh flow over all goods.

## Implementations

## History

Devanur, Papadimitriou, Saberi and Vazirani presented the algorithm at FOCS 2002. Their first analysis had a subtle flaw, and the journal version (Journal of the ACM, 2008) fixed it with balanced flows and proved a polynomial bound. It was the first combinatorial polynomial time algorithm for the linear Fisher market, and it showed that the primal-dual method works for a convex program whose KKT conditions mix primal and dual variables. The paper stated a strongly polynomial algorithm as an open question, and Orlin answered it in 2010.

## References
