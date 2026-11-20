---
tag: MES401
kind: algorithm
slug: sequential-posted-pricing
name: Sequential posted pricing
aliases:
- posted price mechanism
- sequential posted price mechanism
area: algorithmic-game-theory/auctions
level: advanced
summary: Offers the buyers one at a time a take-it-or-leave-it price. With prices from the ex ante relaxation it earns at least a 1 - 1/e fraction of the optimal revenue for one item.
model: word-ram
complexity:
  vars: {n: the number of buyers, N: the total support size of the value distributions}
  time: {worst: O(N log N)}
  space: {extra: O(N)}
properties: {deterministic: false, comparison: true, recursive: false}
history:
  year: 2010
  people: [Shuchi Chawla, Jason D. Hartline, David L. Malec, Balasubramanian Sivan]
  note: Chawla, Hartline, Malec and Sivan showed that sequential posted prices approximate the optimal revenue in single-parameter settings, with the factor e/(e - 1) for one item and for uniform and partition matroids, and used them for multi-parameter unit-demand buyers.
prereqs: [myerson-optimal-auction, virtual-valuation, prophet-inequality]
see_also: [ironing, reserve-price, vickrey-auction, bulow-klemperer-theorem, regular-distribution, uniform-matroid, matroid, simple-versus-optimal-multi-item]
sources:
  - paper: doi:10.1145/1806689.1806733
    title: "Shuchi Chawla, Jason D. Hartline, David L. Malec and Balasubramanian Sivan, Multi-parameter mechanism design and sequential posted pricing, Proceedings of the 42nd ACM Symposium on Theory of Computing (STOC 2010), 311-320"
    locator: "Lemma 2 (the ex ante upper bound on the optimal revenue), Section 4.2 and Table 1 (the factor e/(e - 1) for uniform and partition matroids, and 2 for general matroids), and the example of two buyers with values uniform on [100, 200] in the introduction"
  - book: isbn:9781107172661
    title: Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016
    locator: Lecture 6, Simple near-optimal auctions, Sections 6.2 and 6.3 (the prophet inequality and simple single-item auctions built on it)
  - paper: "Jason D. Hartline, Mechanism Design and Approximation, book draft, version with Chapters 1 to 7 revised in September 2021, https://jasonhartline.com/MDnA/"
    locator: Chapter 4, Bayesian approximation (the prophet inequality, posted pricings and the ex ante relaxation)
---

Sequential posted pricing sells one item to buyers with independent private values by offering them, one at a time, a take-it-or-leave-it price, and the first buyer who accepts gets the item at that price. The prices come from the *ex ante relaxation*, which bounds the optimal revenue, and are offered in decreasing order. The expected revenue is at least $1 - (1 - 1/n)^n \ge 1 - 1/e \approx 0.632$ times the revenue of [Myerson's optimal auction](/myerson-optimal-auction/). The [prophet inequality](/prophet-inequality/) is a statement about stopping rules for a sequence of random rewards. This page is about the mechanism: how to choose prices from the value distributions, and why the result is truthful and earns a constant fraction of the optimal revenue.

## In plain words

A seller has one item and a list of buyers. Instead of running an auction, the seller visits the buyers one by one and names a price to each. A buyer who likes the price buys and the sale ends. A buyer who does not like it walks away and the seller moves on. Each buyer sees one price and can only say yes or no, so no buyer has a reason to lie or to plan ahead. The seller picks the prices in advance from what it knows about the buyers. It asks how often it would like to sell to each buyer, with the chances adding up to at most one, and turns each chance into a price. Visiting the buyers from the highest price to the lowest loses at most about a third of the best possible revenue.

## The problem

There are $n$ buyers and one item. Buyer $i$ has a private value $v_i$ drawn from a known distribution $F_i$, independently of the others, and quasilinear utility. The seller wants a simple truthful mechanism whose expected revenue is close to the optimal revenue $\mathrm{OPT}$ over all [BIC](/bayesian-incentive-compatibility/) and [individually rational](/individual-rationality/) mechanisms.

For buyer $i$ the revenue curve maps a sale probability $q$ to the revenue $q \cdot F_i^{-1}(1 - q)$ of the posted price that sells with probability $q$. Let $\bar R_i$ be its concave hull, which is the best revenue of a random price with sale probability $q$ ([ironing](/ironing/)). The *ex ante relaxation* is

$$\mathrm{EAR} = \max \Bigl\{ \sum_i \bar R_i(q_i) : \sum_i q_i \le 1,\ q_i \ge 0 \Bigr\}.$$

Any mechanism sells to buyer $i$ with some ex ante probability $Q_i$, with $\sum_i Q_i \le 1$, and earns at most $\bar R_i(Q_i)$ from it, so $\mathrm{OPT} \le \mathrm{EAR}$.

## The algorithm

The implementation takes discrete distributions and computes in exact fractions.

```pseudo id=main
SEQUENTIAL-POSTED-PRICING(F_1, ..., F_n, v_1, ..., v_n)
L1  for each buyer i: H_i ← vertices of the concave hull of the revenue curve of F_i, from (0, 0)
L2  S ← the hull segments of all buyers with positive slope, sorted by slope, largest first
L3  cap ← 1; q_i ← 0 for all i; for each segment (i, length ℓ) in S while cap > 0:
L4      t ← min(cap, ℓ); q_i ← q_i + t; cap ← cap - t
L5  for each buyer i: lottery_i ← the hull vertex at q_i, or a mix of the two vertices around q_i
L6  draw a price P_i from lottery_i for each buyer i
L7  for each buyer i in decreasing order of P_i:
L8      if v_i ≥ P_i: sell to i at price P_i and stop
L9  keep the item
```

Lines L1 to L5 depend only on the distributions. They solve the relaxation as a fractional knapsack: each hull segment is an item of size $\ell$ and value density equal to its slope. In line L5, a vertex of $\bar R_i$ at $(q, s q)$ means the price $s$, and the vertex $(0, 0)$ means no offer. If $q_i$ lies strictly between vertices with prices $s_a > s_b$ and quantiles $q_a < q_b$, the lottery offers $s_a$ with probability $(q_b - q_i)/(q_b - q_a)$ and $s_b$ otherwise. At most one buyer gets such a lottery. Lines L6 to L9 run the mechanism, and a buyer accepts exactly when its value is at least its price.

## Example

**A discrete instance.** Two buyers have values in $\{2, 3, 5\}$ with probabilities $1/2, 1/6, 1/3$. The revenue curve has the points $(0, 0)$, $(1/3, 5/3)$, $(1/2, 3/2)$ and $(1, 2)$, and its hull has the vertices $(0, 0)$, $(1/3, 5/3)$ and $(1, 2)$, with slopes 5 and $1/2$. The greedy rule takes the slope-5 segment of buyer 1, then that of buyer 2, and then $1/3$ of the slope-$1/2$ segment of buyer 1. So $q_1 = 2/3$, $q_2 = 1/3$ and $\mathrm{EAR} = 5/3 + 5/3 + 1/6 = 7/2$. Buyer 2 gets the price 5. Buyer 1 sits halfway between the vertices of prices 5 and 2, so it gets 5 or 2 with probability $1/2$ each.

- Prices $(5, 5)$: buyer 1 is first by the tie rule, and the revenue is $5 \cdot 1/3 + (2/3) \cdot 5 \cdot 1/3 = 25/9$.
- Prices $(2, 5)$: buyer 2 is first, and the revenue is $5 \cdot 1/3 + (2/3) \cdot 2 = 3$.

The expected revenue is $26/9 \approx 2.89$. Myerson's optimal auction earns $3$ here, and the guarantee is $(1 - 1/4) \cdot 7/2 = 21/8$, so $21/8 \le 26/9 \le 3 \le 7/2$.

**Uniform values.** Two buyers have values uniform on $[100, 200]$ (Chawla, Hartline, Malec and Sivan 2010, introduction). Here $\bar R_i(q) = q(200 - 100q)$, and the relaxation sets $q_1 = q_2 = 1/2$, the price 150 for both, and $\mathrm{EAR} = 150$. Offering 150 to both in turn earns $150 \cdot (1 - 1/4) = 112.5$, exactly $3/4 = 1 - (1 - 1/2)^2$ of EAR. The optimal auction is the [Vickrey auction](/vickrey-auction/) here, with revenue $\mathbb{E}[\min(v_1, v_2)] = 400/3 \approx 133.3$. Better prices exist: 150 to the first buyer and then 100 to the second earn $125$.

**A tight case.** Three buyers have values uniform on $\{1, 2, 3\}$. The relaxation gives each buyer the price 3 with $q_i = 1/3$, and $\mathrm{EAR} = 3$. The mechanism earns $3 \cdot (1 - (2/3)^3) = 19/9$, which is exactly $1 - (1 - 1/3)^3$ times EAR.

## Correctness

The proof is in `proofs/correctness.md`.

- **Truthful and IR.** Each buyer faces one price that does not depend on its own value, so accepting exactly when $v_i \ge P_i$ is a dominant strategy, and no buyer pays more than its value.
- **The plan.** The greedy rule solves the fractional knapsack over hull segments, so $\sum_i \bar R_i(q_i) = \mathrm{EAR}$. Each lottery sells to buyer $i$ with probability $q_i$ and earns $\bar R_i(q_i)$ from it.
- **The guarantee.** Write the revenue as $\int_0^\infty \Pr[\text{sale price} \ge t]\, dt$. Because prices go in decreasing order, the sale price is at least $t$ exactly when some buyer with $P_i \ge t$ accepts, and these events are independent. With $a_i(t) = \Pr[P_i \ge t, v_i \ge P_i]$ and $\sum_i a_i(t) \le \sum_i q_i \le 1$, the probability is $1 - \prod_i (1 - a_i(t)) \ge (1 - (1 - 1/n)^n) \sum_i a_i(t)$, and integrating gives the bound. With $\mathrm{OPT} \le \mathrm{EAR}$ the mechanism earns at least $(1 - 1/e)\, \mathrm{OPT}$.

## Complexity

The hulls take $O(N)$ time for sorted supports, sorting the at most $N$ segments takes $O(N \log N)$, and the greedy scan and the lotteries take $O(N)$. A run of the mechanism sorts $n$ prices and makes at most $n$ offers, $O(n \log n)$. The extra space is $O(N)$ for the hulls. Since only one buyer can have a two-price lottery, the exact expected revenue needs only two orderings of the prices.

## Properties

- **Dominant-strategy truthful and simple.** Each buyer makes one yes or no decision and never needs to know the others' values or the prior.
- **Randomized only at one buyer.** The plan is deterministic except for at most one buyer, and for continuous regular distributions no randomization is needed at all.
- **Factor depends on $n$.** The guarantee $1 - (1 - 1/n)^n$ is $1$ for one buyer, $3/4$ for two, $19/27$ for three, and decreases to $1 - 1/e$.
- **Not optimal.** Myerson's auction earns more in general, as in both examples above.
- **The bound is against EAR.** The analysis is tight against EAR (the tight case above), but EAR can be larger than OPT, so the true ratio to OPT can be better.

## Variants and improvements

- **Matroid and multi-unit settings.** For $k$ identical items ([uniform matroid](/uniform-matroid/)) and for partition matroids the factor is still $e/(e - 1)$, and for a general [matroid](/matroid/) a sequential posted pricing earns half of the optimum (Chawla, Hartline, Malec and Sivan 2010, Table 1).
- **Unit-demand buyers with several items.** Chawla, Hartline, Malec and Sivan use sequential posted prices for multi-parameter unit-demand buyers, where the optimal mechanism is not known, and bound their revenue against a single-parameter relaxation.
- **Order not chosen by the seller.** In an order-oblivious posted pricing an adversary picks the order of the offers. Prices chosen as in the [prophet inequality](/prophet-inequality/) still give a constant factor, 2 for $k$ identical items (Chawla, Hartline, Malec and Sivan 2010, Table 1).
- **The best order and prices.** Better prices than those of the relaxation can be found by search or dynamic programming over a fixed order, as in the uniform example with 150 and 100.
- **Anonymous prices.** One price for all buyers loses more revenue when the buyers differ, but it is the natural choice when the seller cannot treat buyers differently.

## When to use it

Use it when an auction is hard to run, for example when the buyers arrive one at a time, or when the seller cannot collect bids from all buyers at once, and the value distributions are known. It also gives a simple benchmark and a building block for multi-parameter settings, where the optimal mechanism is complex. When all bids can be collected and the prior is trusted, Myerson's auction earns more. When the prior is unknown but the buyers are i.i.d., a [Vickrey auction](/vickrey-auction/) with an extra buyer ([Bulow-Klemperer theorem](/bulow-klemperer-theorem/)) needs no prior at all.

## Pitfalls

- **Offer order.** The analysis needs the offers in decreasing order of price. In another order, a buyer with a low price can take the item before a buyer who would pay a high price.
- **Irregular distributions.** With the raw revenue curve instead of its concave hull, the relaxation is no longer an upper bound on OPT. A sale probability between two hull vertices needs a random price to earn $\bar R_i(q_i)$.
- **Correlated values.** The independence of the acceptance events is essential. With correlated values the bound can fail.
- **One offer per buyer.** If a buyer who declines could come back later at a lower price, it would wait, and the analysis would fail. Each buyer must get exactly one offer.
- **Floating point.** Hull tests and comparisons of slopes decide the plan. With discrete distributions they should be done in exact arithmetic.

## Implementations

## History

Posted prices are the oldest selling method, and their revenue for one buyer is the starting point of Myerson's theory. Prophet inequalities, whose single-item form goes back to Krengel, Sucheston and Samuel-Cahn, are statements about stopping rules. Chawla, Hartline, Malec and Sivan (2010) used them to bound the revenue of posted prices. They bounded the optimal revenue by the ex ante relaxation, showed that sequential posted prices approximate it within $e/(e - 1)$ for one item and for uniform and partition matroids and within 2 for general matroids, and used these single-parameter results to design approximately optimal mechanisms for multi-parameter unit-demand buyers. Posted prices have since become a standard tool for simple and approximately optimal mechanism design.

## References
