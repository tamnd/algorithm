---
tag: H6Y499
kind: definition
slug: demand-query
name: Demand query
aliases:
- demand oracle
area: algorithmic-game-theory/auctions
level: advanced
summary: "A query to a bidder that gives a price for each item and asks for a bundle that maximizes value minus price. It is stronger than a value query and solves the LP relaxation of winner determination."
prereqs: [combinatorial-auction, quasilinear-utility]
see_also: [bidding-languages, winner-determination-problem, simultaneous-ascending-auction, gross-substitutes, competitive-equilibrium, ellipsoid-method, lp-duality, communication-complexity]
sources:
  - paper: doi:10.1137/050641181
    title: "Liad Blumrosen and Noam Nisan, On the computational power of demand queries, SIAM Journal on Computing 39(4) (2009), 1372-1391"
    locator: the comparison of demand and value queries, the polynomial solution of the linear programming relaxation with demand queries, and approximation with item prices
  - book: isbn:9780521872829
    title: "Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007"
    locator: Chapter 11 (Blumrosen and Nisan, Combinatorial auctions), Section 11.5 (iterative auctions and the query model)
---

A demand query is a question that an auction asks a bidder in a [combinatorial auction](/combinatorial-auction/): "here is a price for each item; which bundle would you buy?" The bidder answers with a bundle that maximizes its value minus the sum of the prices. Ascending auctions with item prices, such as the [simultaneous ascending auction](/simultaneous-ascending-auction/), ask exactly such questions in each round. A demand query is at least as strong as a *value query*, which asks for the value of one bundle: a value query can be simulated by polynomially many demand queries, but not the other way round. With demand queries, the linear programming relaxation of the [winner determination problem](/winner-determination-problem/) can be solved in polynomial time.

## Definition

Let $M$ be a set of $m$ items and $v : 2^M \to \mathbb{R}_{\ge 0}$ a valuation with $v(\emptyset) = 0$. For a price vector $p \in \mathbb{R}^m_{\ge 0}$, the **demand set** is

$$D(p) = \arg\max_{S \subseteq M} \Big( v(S) - \sum_{j \in S} p_j \Big).$$

A **demand query** gives $p$ to the bidder, and the answer is some bundle in $D(p)$. A **value query** gives a bundle $S$, and the answer is $v(S)$. The **query model** measures an auction by how many queries it asks, with each answer counted as one step, and allows any computation between the queries.

Two facts relate the two kinds of query (Blumrosen and Nisan 2009):

- A value query can be answered with a number of demand queries polynomial in $m$ and in the number of bits of the values.
- Some demand queries need exponentially many value queries.

The dual of the linear programming relaxation of winner determination has one variable for each item price and one for each bidder utility. A violated constraint of the dual is a bundle that some bidder demands at the current prices, so a demand query is a separation oracle, and the [ellipsoid method](/ellipsoid-method/) solves the relaxation with polynomially many demand queries; see [LP duality](/lp-duality/).

## Examples and non-examples

- **Unit demand**, $v(S) = \max_{j \in S} v_j$. The answer is $\{j\}$ for an item with the largest $v_j - p_j$, or $\emptyset$ if that value is negative. One pass over the items.
- **Additive**, $v(S) = \sum_{j \in S} v_j$. The answer is the set of items with $v_j > p_j$.
- **Single-minded** with bundle $S^*$ and value $w$. The answer is $S^*$ if $w \ge \sum_{j \in S^*} p_j$, and $\emptyset$ otherwise.
- **Gross substitutes.** For [gross substitutes](/gross-substitutes/) valuations given by value queries, a greedy rule that adds the item of largest marginal utility answers a demand query with $O(m^2)$ value queries.
- **XOR bids.** If the valuation is an XOR of $k$ atomic bids, try each atom: $O(k m)$ time.
- **Non-example: OR bids.** If the valuation is an OR of atomic bids, answering a demand query is itself a weighted [set packing](/set-packing/) problem, NP-hard to compute even though the valuation is short.
- **Non-example: value queries for complements.** With general valuations, a value query reveals one number, and finding a demanded bundle can need exponentially many such numbers.

## Related definitions

- **Value query.** The weaker query that returns $v(S)$.
- **Walrasian equilibrium.** A [competitive equilibrium](/competitive-equilibrium/) of a combinatorial auction is a price vector and an allocation in which every bidder gets a bundle in its demand set and unsold items have price 0. It exists exactly when the linear programming relaxation has an integral optimum.
- **General queries and communication.** Any protocol in which bidders send bits is covered by [communication complexity](/communication-complexity/). Lower bounds there, such as the exponential bound for exact welfare maximization with general valuations (Nisan and Segal 2006), hold for demand queries too.
- **Item-price auctions.** An auction that asks only demand queries with item prices gets an approximation of $\min(n, O(\sqrt m))$ of the optimal welfare, and some valuations show that item prices cannot do much better (Blumrosen and Nisan 2009).
- **Bidding languages.** A [bidding language](/bidding-languages/) describes the whole valuation at once, while queries learn it step by step.

## References
