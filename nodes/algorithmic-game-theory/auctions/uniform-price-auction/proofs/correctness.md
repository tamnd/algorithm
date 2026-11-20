---
title: The uniform price auction sells to the highest marginal bids at a clearing price, and it is truthful only for unit demand
proves: [correctness]
status: full
---

We use the pseudocode of the page. Bidder $i$ reports a list of marginal bids $b_{i,1} \ge b_{i,2} \ge \cdots \ge b_{i,d_i} \ge 0$, where $b_{i,j}$ is its offer for its $j$-th unit. There are $k$ units. Line L2 sorts all triples $(b_{i,j}, i, j)$ by bid, highest first, then by $i$, then by $j$. Call the first $q = \min(k, |E|)$ triples *winning* and the rest *losing*.

**Claim 1 (the allocation).** Each bidder wins a prefix of its list: if $(b_{i,j}, i, j)$ wins and $j' < j$, then $(b_{i,j'}, i, j')$ wins. The allocation $x$ maximizes the reported welfare $\sum_i \sum_{j \le x_i} b_{i,j}$ over all allocations with $\sum_i x_i \le k$ and $x_i \le d_i$.

*Proof.* If $j' < j$, then $b_{i,j'} \ge b_{i,j}$, and on a tie the smaller unit index comes first in the order of line L2. So the triple of unit $j'$ is earlier than the triple of unit $j$, and it wins if that one wins. Any feasible allocation $y$ selects at most $k$ triples, one for each unit given out, and its welfare is the sum of their bids. The sum of at most $k$ entries of $E$ is at most the sum of the $q$ largest bids, because all bids are at least 0. Lines L3 and L4 select exactly the $q$ largest bids, and by the first part they form an allocation. $\square$

**Claim 2 (the price clears the market).** Under the highest losing rule (line L5), every winning bid is at least $p$ and every losing bid is at most $p$. Under the lowest winning rule (line L6), the same holds when at least one unit is sold. Every winner pays $p$ for each unit, so a bidder that wins $x_i$ units pays $p\,x_i$ (line L7).

*Proof.* The list is sorted. Under line L5, $p$ is the bid of triple $k + 1$, the first losing triple, or $p = 0$ if no triple loses; in both cases every winning bid is at least $p$ (bids are at least 0) and every losing bid is at most $p$. Under line L6, $p$ is the bid of the last winning triple, which is at most every earlier bid and at least every later bid. $\square$

So with truthful bids, the units go to the $k$ highest marginal values, and every bidder demands, at the price $p$, the number of units it gets, up to ties.

**Claim 3 (unit demand: truthful bidding is dominant under the highest losing rule).** Suppose every bidder wants at most one unit and reports one bid. Fix bidder $i$ with value $v$ and the bids of the others. Then bidding $v$ gives at least the utility of any other bid, and at least 0.

*Proof.* Let $\theta$ be the $k$-th highest bid of the other bidders, and $\theta = 0$ if there are fewer than $k$ others. Bidder $i$ wins if $b > \theta$ and loses if $b < \theta$: in the first case at most $k - 1$ other bids are at least $b$, and in the second case at least $k$ other bids are above $b$. If bidder $i$ wins, at most $k - 1$ other triples are ahead of it, so the $k$ winning triples are $i$ and the $k - 1$ highest other bids, and the first losing triple is the $k$-th highest other bid; if there are fewer than $k$ others, no triple loses and the price is $0 = \theta$. So the price is $\theta$, which does not depend on $b$. If $v > \theta$, the bid $v$ wins and gives $v - \theta > 0$, and any other bid gives $v - \theta$ or 0. If $v < \theta$, the bid $v$ gives 0, and a winning bid gives $v - \theta < 0$. If $v = \theta$, every bid gives 0. $\square$

This is the $(k + 1)$-th price auction, the case of the [VCG mechanism](/vcg-mechanism/) for identical units and unit demand.

**Claim 4 (the lowest winning rule is not truthful, even for unit demand).** With one unit and bids $(5, 3)$, the first bidder wins and pays its own bid 5, so its utility is 0. With the bid 4 it still wins and pays 4, so its utility is 1.

**Claim 5 (demand reduction: with multi-unit demand, truthful bidding is not dominant).** Take $k = 2$, a bidder $A$ with marginal values $(10, 10)$ and a bidder $B$ with one value 6. Under the highest losing rule, truthful bids give $A$ both units at the price 6, so $A$ gets $20 - 12 = 8$. If $A$ bids $(10, 0)$, the sorted bids are $10, 6, 0$, so $A$ and $B$ win one unit each and the price is the losing bid 0. Then $A$ gets 10 > 8. The bids $((10, 0), 6)$ form a Nash equilibrium: $B$ already gets its whole value 6, and $A$ can get two units only with a second bid of at least 6, and then the losing bid 6 of $B$ sets the price to 6 and $A$ gets 8. With one unit, $A$ gets at most 10. The equilibrium welfare is $10 + 6 = 16$, below the optimum 20. $\square$

The reason is that a bidder's own losing bid on a later unit can set the price it pays on its earlier units. With unit demand this cannot happen, because a bidder that wins has no losing bid.
