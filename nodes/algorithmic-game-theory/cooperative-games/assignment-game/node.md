---
tag: ER4JDQ
kind: model
slug: assignment-game
name: Shapley-Shubik assignment game
aliases:
- assignment game
area: algorithmic-game-theory/cooperative-games
level: core
summary: A TU game of buyers and sellers in which each coalition is worth its maximum weight matching. Its core equals the set of optimal dual solutions of the assignment LP.
prereqs: [transferable-utility-game, core-of-a-cooperative-game, assignment-problem, lp-duality]
see_also: [maximum-weight-matching, hungarian-algorithm, competitive-equilibrium, demange-gale-sotomayor-auction, vcg-mechanism, stable-matching, nucleolus, bondareva-shapley-theorem]
sources:
  - paper: doi:10.1007/BF01753437
    title: "Lloyd S. Shapley and Martin Shubik, The assignment game I, the core, International Journal of Game Theory 1(1) (1971), 111-130"
    locator: the model, the core as the set of optimal dual solutions, competitive prices, and the lattice structure with the buyer-optimal and seller-optimal points
  - paper: doi:10.1086/261410
    title: "Gabrielle Demange, David Gale and Marilda Sotomayor, Multi-item auctions, Journal of Political Economy 94(4) (1986), 863-872"
    locator: an ascending auction that ends at the minimum competitive prices
  - paper: "Herman B. Leonard, Elicitation of honest preferences for the assignment of individuals to positions, Journal of Political Economy 91(3) (1983), 461-479"
    locator: the minimum competitive prices give each buyer its marginal contribution and make truthful reports a dominant strategy
  - paper: doi:10.1007/BF01240179
    title: "Tamas Solymosi and T. E. S. Raghavan, An algorithm for finding the nucleolus of assignment games, International Journal of Game Theory 23 (1994), 119-143"
    locator: a polynomial algorithm for the nucleolus of the assignment game
---

The assignment game is a market of buyers and sellers, studied as a [TU game](/transferable-utility-game/). Each seller has one indivisible good, each buyer wants at most one good, and money can be paid. A coalition is worth the largest total gain from trade that it can make by pairing its buyers with its sellers. Computing that value is the [assignment problem](/assignment-problem/), a [maximum weight matching](/maximum-weight-matching/) problem in a bipartite graph; this page is about how to share the value. Shapley and Shubik showed in 1971 that the [core](/core-of-a-cooperative-game/) of the game is exactly the set of optimal solutions of the dual LP of the assignment problem, so it is never empty, and that its points are the competitive equilibria of the market.

## The machine

There is a set $B$ of $m$ buyers and a set $Q$ of $k$ sellers, and $N = B \cup Q$. Seller $j$ owns one house and values it at $c_j$; buyer $i$ values house $j$ at $h_{ij}$. Utility is money, so a sale of house $j$ to buyer $i$ creates the gain

$$a_{ij} = \max(0,\ h_{ij} - c_j),$$

and any price splits this gain between the two. The input is the $m \times k$ matrix $a \ge 0$.

A coalition $S$ can only trade inside itself. Its value is

$$v(S) = \max \Big\{ \sum_{(i, j) \in M} a_{ij} : M \text{ a matching between } S \cap B \text{ and } S \cap Q \Big\}.$$

So $v(S) = 0$ when $S$ has only buyers or only sellers, and $v(\{i, j\}) = a_{ij}$ for a buyer $i$ and a seller $j$. The game is superadditive, and every subgame is again an assignment game.

A payoff vector is a pair $(u, w)$, with $u_i$ for buyer $i$ and $w_j$ for seller $j$. When buyer $i$ buys house $j$ at price $p_j$, the payoffs are $u_i = h_{ij} - p_j$ and $w_j = p_j - c_j$.

## What it counts

The value $v(N)$ is the optimum of the assignment LP

$$\max \sum_{i, j} a_{ij} x_{ij} \quad \text{subject to} \quad \sum_j x_{ij} \le 1, \quad \sum_i x_{ij} \le 1, \quad x \ge 0,$$

which has an integral optimal solution, because the constraint matrix of bipartite matching is [totally unimodular](/total-unimodularity/). Its dual is

$$\min \sum_i u_i + \sum_j w_j \quad \text{subject to} \quad u_i + w_j \ge a_{ij} \text{ for all } i, j, \quad u, w \ge 0.$$

**Theorem (Shapley and Shubik 1971).** The core of the assignment game is the set of optimal solutions of the dual LP. In particular it is not empty.

*Proof.* Let $(u, w)$ be in the core. The core constraints for the single players and for the pairs $\{i, j\}$ say $u, w \ge 0$ and $u_i + w_j \ge a_{ij}$, so $(u, w)$ is feasible for the dual, with value $v(N)$, the primal optimum. By [weak duality](/weak-duality/) it is optimal. Conversely, let $(u, w)$ be an optimal dual solution. By strong duality its value is $v(N)$. For a coalition $S$, take an optimal matching $M$ inside $S$: then $v(S) = \sum_{(i, j) \in M} a_{ij} \le \sum_{(i, j) \in M} (u_i + w_j) \le (u, w)(S)$, since the payoffs of players in $S$ that $M$ leaves unmatched are at least 0. So $(u, w)$ is in the core. $\square$

So the core is cut out by the $mk$ pair constraints and the $m + k$ sign constraints alone; the other $2^{m+k}$ coalitions add nothing. Since every subgame is an assignment game, the game is totally balanced.

A core point is also a competitive equilibrium. Set the price of house $j$ to $p_j = c_j + w_j$. At these prices each buyer is assigned a house that gives it the most surplus $h_{ij} - p_j$, which is $u_i$, or buys nothing if every surplus is at most 0, and every house that is not sold has $w_j = 0$. Conversely, every [competitive equilibrium](/competitive-equilibrium/) gives a core point.

### Example

Two buyers 1 and 2 and two houses A and B, with gains

| | A | B |
|---|---|---|
| buyer 1 | 5 | 3 |
| buyer 2 | 4 | 1 |

The matching 1B, 2A gains $3 + 4 = 7$ and the matching 1A, 2B gains $5 + 1 = 6$, so $v(N) = 7$. In the core, $u_1 + w_B = 3$ and $u_2 + w_A = 4$, and the other two pair constraints give $2 \le w_A - w_B \le 3$. The buyer-optimal core point is $u = (3, 2)$, $w = (2, 0)$, and the seller-optimal one is $u = (1, 0)$, $w = (4, 2)$. At the buyer-optimal point each buyer gets its marginal contribution: $v(N) - v(N \setminus \{1\}) = 7 - 4 = 3$ and $v(N) - v(N \setminus \{2\}) = 7 - 5 = 2$. At the seller-optimal point each seller does: $7 - 3 = 4$ for A and $7 - 5 = 2$ for B.

## Relation to other models

- **The assignment problem.** The [assignment problem](/assignment-problem/) asks for the best matching. The game asks how to split its value. The [Hungarian algorithm](/hungarian-algorithm/) solves the primal and the dual together, so it gives $v(N)$ and one core point in $O(n^3)$ time for $n = \max(m, k)$.
- **Stable matching.** The [stable matching](/stable-matching/) problem is the same two-sided market without money. Its stable matchings form a [lattice](/lattice-of-stable-matchings/) with a best point for each side, and the core of the assignment game has the same structure.
- **Auctions and mechanisms.** The [Demange-Gale-Sotomayor auction](/demange-gale-sotomayor-auction/) raises prices on overdemanded houses and ends at the minimum competitive prices, the buyer-optimal core point. At this point each buyer pays what the [VCG mechanism](/vcg-mechanism/) charges. The [auction algorithm](/auction-algorithm/) of Bertsekas uses the same idea with a small bid increment to solve the assignment problem.
- **The glove game.** With one buyer, two sellers and gains $a_{1j} = 1$, the assignment game is the glove game: $v(S) = 1$ exactly when $S$ contains the buyer and a seller. Its core is the point that gives the buyer 1 and the sellers 0, so competition between the two sellers drives their price to their reservation value.
- **Other combinatorial games.** The [minimum cost spanning tree game](/minimum-cost-spanning-tree-game/) is another game defined by an optimization problem, also with a nonempty core. Both cores are found by a duality argument, an instance of the [Bondareva-Shapley theorem](/bondareva-shapley-theorem/).

## Known results in the model

- **Core.** The core equals the set of optimal dual solutions of the assignment LP, so it is a nonempty polytope, and the game is totally balanced (Shapley and Shubik 1971).
- **Lattice.** If $(u, w)$ and $(u', w')$ are core points, so are $(\max(u, u'), \min(w, w'))$ and $(\min(u, u'), \max(w, w'))$, taken entrywise. So the core has a buyer-optimal point, best for all buyers at once and worst for all sellers, and a seller-optimal point (Shapley and Shubik 1971).
- **Marginal contributions.** At the buyer-optimal point each buyer gets $v(N) - v(N \setminus \{i\})$, its marginal contribution. So the minimum competitive prices are the VCG prices, and a buyer cannot gain by misreporting its values when these prices are used (Leonard 1983; Demange, Gale and Sotomayor 1986).
- **Computation.** The value $v(S)$ of any coalition takes one maximum weight matching. A core point, and both extreme points of the lattice, take a polynomial number of matchings. The [nucleolus](/nucleolus/) can be computed in polynomial time (Solymosi and Raghavan 1994), although the general sequential LP for it has exponentially many constraints.
- **The Shapley value need not be in the core.** In the glove game the [Shapley value](/shapley-value/) gives the buyer $2/3$ and each seller $1/6$, while the core gives the buyer everything. Assignment games are in general not [convex](/convex-game/).

## References
