---
tag: MJT9DD
kind: problem
slug: winner-determination-problem
name: Winner determination problem
aliases:
- combinatorial auction winner determination
area: algorithmic-game-theory/auctions
level: core
summary: "Given package bids in a combinatorial auction, accept bids with disjoint bundles of the largest total value. It is weighted set packing, so it is NP-hard and hard to approximate."
prereqs: [combinatorial-auction, set-packing, np-hard]
see_also: [bidding-languages, single-minded-bidder-mechanism, vcg-mechanism, maximum-independent-set, linear-programming-problem, knapsack-problem, assignment-problem, approximation-ratio]
sources:
  - paper: "Michael H. Rothkopf, Aleksandar Pekec and Ronald M. Harstad, Computationally manageable combinational auctions, Management Science 44(8) (1998), 1131-1147"
    locator: the NP-hardness of winner determination for general package bids and the polynomial cases, such as nested bundles and intervals of a line
  - paper: "Tuomas Sandholm, Algorithm for optimal winner determination in combinatorial auctions, Artificial Intelligence 135 (2002), 1-54"
    locator: the hardness and inapproximability of winner determination and a search algorithm that solves large instances
  - paper: "Daniel Lehmann, Liadan Ita O'Callaghan and Yoav Shoham, Truth revelation in approximately efficient combinatorial auctions, Journal of the ACM 49(5) (2002), 577-602"
    locator: the reduction from independent set that gives the m^(1/2 - epsilon) hardness for single-minded bids, and the greedy sqrt(m) approximation
  - book: isbn:9780262033428
    title: "Peter Cramton, Yoav Shoham and Richard Steinberg (eds.), Combinatorial Auctions, MIT Press, 2006"
    locator: the part on complexity and algorithmic considerations (the complexity of winner determination, exact algorithms and tractable cases)
---

The winner determination problem asks which package bids a [combinatorial auction](/combinatorial-auction/) should accept. Each bid names a bundle of items and a price, two accepted bids may not share an item, and the goal is the largest total price. With one bid per bidder it is exactly weighted [set packing](/set-packing/), so it is [NP-hard](/np-hard/), and for general bids no polynomial algorithm approximates it within $m^{1/2 - \epsilon}$ for $m$ items unless $\mathrm{P} = \mathrm{NP}$. Every mechanism that maximizes the reported welfare, such as the [VCG mechanism](/vcg-mechanism/), must solve it, often many times.

## In plain words

An auctioneer has many items and a pile of offers. Each offer says: I will pay this much for exactly this group of items. Two accepted offers cannot both claim the same item. The auctioneer wants to pick the offers that bring in the most money. With a few offers this is easy, but the number of ways to choose grows very fast, and no fast method is known that always finds the best choice. Special shapes of offers, such as groups of neighboring items on a line, make the problem easy again.

## Definition

**Input.** A set $M$ of $m$ items and a list of bids $(S_1, w_1), \ldots, (S_k, w_k)$ with bundles $S_t \subseteq M$ and prices $w_t \ge 0$. Each bid belongs to a bidder.

**Output.** A set $A$ of accepted bids whose bundles are pairwise disjoint, and, in the XOR form below, at most one bid per bidder.

**Goal.** Maximize $\sum_{t \in A} w_t$.

As an integer program, with $x_t \in \{0, 1\}$:

$$\max \sum_t w_t x_t \quad \text{subject to} \quad \sum_{t : j \in S_t} x_t \le 1 \text{ for every item } j.$$

The decision version, which asks whether the total price can reach a given bound, is [NP-complete](/np-complete/).

## Variants

- **OR bids.** A bidder may win any set of its bids with disjoint bundles. This is the plain set packing form above.
- **XOR bids.** A bidder may win at most one of its bids. Add a dummy item per bidder to every one of its bundles, and the problem becomes plain set packing; see [bidding languages](/bidding-languages/).
- **Value oracles.** With a valuation $v_i$ for each bidder, the goal is to maximize $\sum_i v_i(S_i)$ over allocations, with access by value or [demand queries](/demand-query/).
- **Multi-unit items.** With several copies of each item, the constraints become $\sum_t a_{tj} x_t \le c_j$, a packing integer program. With one item type it is the [knapsack problem](/knapsack-problem/).
- **Reverse auctions.** In a procurement auction the buyer covers all items at least cost, a weighted set cover problem.

## Examples

Items $\{a, b, c\}$ and bids $(\{a, b\}, 5)$, $(\{b, c\}, 5)$, $(\{a\}, 3)$, $(\{c\}, 3)$. The bids $\{a, b\}$ and $\{b, c\}$ clash on $b$. The best choice is $(\{a, b\}, 5)$ and $(\{c\}, 3)$, or $(\{a\}, 3)$ and $(\{b, c\}, 5)$, each for 8; accepting both single bids alone gives 6.

The reduction from independent set: given a graph, make each edge an item and each vertex $u$ a bid on the set of edges at $u$ with price 1. Two bids are disjoint exactly when their vertices are not adjacent, so the accepted bids form an [independent set](/independent-set/).

## Known algorithms

- **Exact search.** Branch and bound over the bids, with linear programming bounds, solves many real instances with thousands of bids (Sandholm 2002). General integer programming solvers are also used in practice.
- **Dynamic programming over subsets.** With all bundles as states, $O(3^m)$ time solves any instance, which is practical only for small $m$.
- **Greedy.** Sort the bids by $w_t / \sqrt{|S_t|}$ and accept disjoint ones; this gives a $\sqrt m$ approximation and is the core of the [Lehmann-O'Callaghan-Shoham mechanism](/single-minded-bidder-mechanism/). Greedy by $w_t$ gives a $d$ approximation when every bundle has at most $d$ items.
- **Linear programming.** The relaxation with $0 \le x_t \le 1$ is a [linear program](/linear-programming-problem/). It is integral when single item prices clear the market, for example under [gross substitutes](/gross-substitutes/).
- **Polynomial cases.** Bundles of at most two items reduce to maximum weight matching; bundles that are intervals of a line are solved by dynamic programming; nested (laminar) bundles are solved by dynamic programming on the tree (Rothkopf, Pekec and Harstad 1998). Unit-demand bidders give the [assignment problem](/assignment-problem/).

## Bounds

- **NP-hard** already when each bundle has at most three items, by reduction from set packing with sets of size three.
- **Inapproximability.** By the reduction from independent set above, with $m$ about $N^2$ items for a graph on $N$ vertices, the $N^{1 - \epsilon}$ hardness of [maximum independent set](/maximum-independent-set/) (Håstad 1999; Zuckerman 2007) gives no $m^{1/2 - \epsilon}$ approximation in polynomial time unless $\mathrm{P} = \mathrm{NP}$. In terms of the number of bids $k$, there is no $k^{1 - \epsilon}$ approximation.
- **The greedy $\sqrt m$ bound** matches this hardness up to the $\epsilon$.
- **Communication.** With valuations held privately, exact and even $m^{1/2 - \epsilon}$ approximate solutions need communication exponential in $m$ (Nisan and Segal 2006).

## Reductions

- **From maximum independent set**, as in the example. This gives NP-hardness and the approximation bound.
- **To weighted set packing** and to [maximum independent set](/maximum-independent-set/) in the conflict graph, whose vertices are the bids and whose edges join bids that share an item.
- **XOR to OR**, with one dummy item per bidder.
- **To integer linear programming**, as in the definition.

## Applications

Winner determination runs in every package auction: spectrum auctions with package bids, procurement auctions for transport lanes and supplies, airport landing slots, and the allocation step of the [VCG mechanism](/vcg-mechanism/), which solves it once for the allocation and once more without each winner for the payments.

## References
