---
tag: ZZQA5X
kind: algorithm
slug: moulin-mechanism
name: Moulin mechanism
aliases:
- Moulin-Shenker mechanism
area: algorithmic-game-theory/cooperative-games
level: advanced
summary: Drops every player whose bid is below its cross-monotonic cost share and repeats until all can pay. It is group strategyproof and budget balanced.
model: word-ram
complexity:
  vars: {n: the number of players, t: the time to compute the shares of one set}
  time: {worst: O(n (n + t))}
  space: {extra: O(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1999
  people: [Herve Moulin, Scott Shenker]
  note: Moulin defined the mechanism and proved group strategyproofness in 1999, and Moulin and Shenker studied its budget balance and efficiency for submodular costs in 2001.
prereqs: [cost-sharing-mechanism, cross-monotonicity]
see_also: [shapley-value, budget-balance, green-laffont-theorem, vcg-mechanism, airport-game, jain-vazirani-steiner-cost-sharing, bird-rule, submodular-function]
sources:
  - paper: "Herve Moulin, Incremental cost sharing: characterization by coalition strategy-proofness, Social Choice and Welfare 16(2) (1999), 279-320"
    title: "Incremental cost sharing: characterization by coalition strategy-proofness"
    locator: the mechanism defined by a cross-monotonic cost-sharing method, its coalition strategyproofness, and the characterization for submodular costs
  - paper: "Herve Moulin and Scott Shenker, Strategyproof sharing of submodular costs: budget balance versus efficiency, Economic Theory 18(3) (2001), 511-533"
    title: "Strategyproof sharing of submodular costs: budget balance versus efficiency"
    locator: the Shapley value mechanism for submodular costs, compared with the marginal cost mechanism, and its efficiency loss
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 15 (Kamal Jain and Mohammad Mahdian, Cost Sharing), Section 15.3, Proposition 15.15 and Theorem 15.16
  - paper: doi:10.1145/1538902.1538907
    title: Quantifying inefficiency in cost-sharing mechanisms
    locator: Tim Roughgarden and Mukund Sundararajan, Journal of the ACM 56(4), Article 23, 2009, the social cost approximation of the Shapley value mechanism for submodular costs and the bounds for Steiner tree mechanisms
---

The Moulin mechanism decides which players to serve and what to charge them when a shared service has a cost and each player has a private value for it. It takes a cost-sharing method that says what each player of a set would pay if exactly that set were served. Starting with all players, it removes every player whose bid is below its share, recomputes the shares for the smaller set, and repeats until every remaining player can pay. If the method is [cross-monotonic](/cross-monotonicity/), so that no share goes up when the set grows, then the mechanism is group strategyproof: no group of players can lie in a way that helps one member and hurts none. If the method covers the cost exactly, the mechanism is also budget balanced. Moulin defined it in 1999.

## In plain words

A group must decide who gets a shared service, such as a road or a data stream, and how to split its cost. Each person says how much the service is worth to them. The organizer proposes a price for each person, based on who is still in. Anyone who said less than their price is out. With fewer people, the prices may go up, so the organizer checks again and removes more people. This stops when everyone left accepts their price. The people left are served and pay their final prices. If prices never go down when someone leaves, nobody can gain by lying, not even a group of friends who agree on what to say. The payments cover the cost of serving the people who stay.

## The problem

There is a set $A$ of $n$ players and a cost function $C : 2^A \to \mathbb{R}_{\ge 0}$ with $C(\emptyset) = 0$, where $C(S)$ is the cost of serving the set $S$. Player $i$ has a private value $v_i$ for being served. A [cost-sharing mechanism](/cost-sharing-mechanism/) collects bids $b_i$, chooses a set $S$ to serve and charges payments $p_i$. The utility of player $i$ is $v_i - p_i$ if $i \in S$ and $-p_i$ otherwise, which is [quasilinear](/quasilinear-utility/). The goals are:

- **Group strategyproofness.** For every coalition $K$ and every way the members of $K$ change their bids, if no member of $K$ is worse off, then no member is better off.
- **Budget balance.** The payments cover the cost, $C(S) \le \sum_{i \in S} p_i \le \beta\, C(S)$, with $\beta = 1$ for exact budget balance. This page uses this form of $\beta$-budget balance; some papers divide by $\beta$ instead and write $\frac{1}{\beta} C(S) \le \sum_i p_i \le C(S)$.
- **Participation.** No positive transfers ($p_i \ge 0$), voluntary participation (a truthful player has utility at least 0), and consumer sovereignty (a high enough bid guarantees service).

The mechanism uses a cost-sharing method $\xi$, which gives a share $\xi(i, S) \ge 0$ to each $i \in S$ for each nonempty set $S$. The method is cross-monotonic if $\xi(i, S) \ge \xi(i, T)$ for $i \in S \subseteq T$, and $\beta$-budget balanced if $C(S) \le \sum_{i \in S} \xi(i, S) \le \beta\, C(S)$ for every $S$.

## The algorithm

```pseudo id=main
MOULIN(A, b, ξ)
L1  S ← A
L2  repeat:
L3      D ← {i ∈ S : b_i < ξ(i, S)}
L4      S ← S \ D
L5  until D = ∅
L6  p_i ← ξ(i, S) for i ∈ S; p_i ← 0 for i ∉ S
L7  return S, p
```

Line L1 starts with all players. Each round computes the shares of the current set once, and line L3 finds the players who bid less than their share. Line L4 removes them. Removing players can raise the shares of the others, so the loop runs again until a round removes nobody (line L5). Line L6 charges each served player its share in the final set, and the others pay nothing.

With a cross-monotonic method, a player who can afford its share in some set can afford its share in every larger set. So a player who belongs to an affordable set is never removed, and the loop ends at the largest set in which every member can pay its share. This set is unique, and the order of removals does not change it. Removing all short bidders at once, as in line L3, or one at a time gives the same result.

## Example

Three planes share a runway. Plane $i$ needs length $r_i$, with $r_1 = 2$, $r_2 = 4$ and $r_3 = 6$, and the cost of a set is the longest length it needs, $C(S) = \max_{i \in S} r_i$. This is an [airport game](/airport-game/). The method is the [Shapley value](/shapley-value/) of the game restricted to $S$: each segment of the runway is split equally among the planes of $S$ that need it. This method is cross-monotonic, because each segment is shared by more planes when the set grows, and it is budget balanced.

The bids are $b = (1, 3/2, 5)$.

| round | $S$ | shares $\xi(i, S)$ | removed |
|---|---|---|---|
| 1 | {1, 2, 3} | $2/3$, $2/3 + 1 = 5/3$, $5/3 + 2 = 11/3$ | 2, since $3/2 < 5/3$ |
| 2 | {1, 3} | $1$, $1 + 4 = 5$ | none |

Planes 1 and 3 are served and pay 1 and 5, and the payments sum to $6 = C(\{1, 3\})$. The removal of plane 2 raised both other shares, from $2/3$ to 1 and from $11/3$ to 5, but both planes could still pay. If plane 2 bids 2 instead, nobody is removed in round 1, all three planes are served, and plane 2 pays $5/3$.

The removed plane cannot gain by a higher bid: to be served it must pay at least $5/3$, which is more than its value $3/2$ if it bid truthfully. Planes 1 and 3 cannot lower their payments by bidding less, because their payments depend only on the served set, and a lower bid can only remove players and raise the shares.

## Correctness

The file proofs/correctness.md gives the full proof. Call a set $T$ affordable if $b_i \ge \xi(i, T)$ for every $i \in T$. By cross-monotonicity, the union of two affordable sets is affordable, so there is a unique largest affordable set $M(b)$. The loop never removes a member of $M(b)$, since its share in any superset of $M(b)$ is at most its share in $M(b)$, and the final set is affordable. So the mechanism serves exactly $M(b)$ (Nisan et al. 2007, Proposition 15.15).

For group strategyproofness, let a coalition $K$ change its bids from the true values $v$ to $b$, and let $F = M(v)$ and $F' = M(b)$. Assume no member of $K$ loses. A member of $K$ served under $b$ then has value at least its share in $F'$, and a player outside $K$ bids truthfully. So every player of $F \cup F'$ can pay its share in $F \cup F'$ at the true values, and $F \cup F'$ is affordable for $v$. Hence $F' \subseteq F$. By cross-monotonicity, every share in $F'$ is at least the share in $F$, so no member of $K$ gains. This is Theorem 15.16 of Nisan et al. (2007).

Budget balance holds because the payments are the shares of the served set. Voluntary participation holds because the served set is affordable, and consumer sovereignty holds because a player who bids at least its share in $\{i\}$ can join any affordable set.

## Complexity

Each round except the last removes at least one player, so there are at most $n + 1$ rounds. A round computes the shares of one set and compares at most $n$ bids. If one call of the method takes time $t$, the total time is $O(n (n + t))$, with $O(n)$ extra space for the current set and the payments. The cost of the method dominates for many problems. For the airport game the shares take $O(n \log n)$ time; for a Steiner tree method such as [Jain-Vazirani cost sharing](/jain-vazirani-steiner-cost-sharing/) each call runs a primal-dual algorithm. For a general cost function given by an oracle, the Shapley value needs the costs of exponentially many sets.

## Properties

- **Group strategyproof** if the method is cross-monotonic. In particular, truthful bidding is a dominant strategy, so the mechanism is [dominant-strategy incentive compatible](/dominant-strategy-incentive-compatibility/).
- **$\beta$-budget balanced** if the method is. The payments are exactly the shares of the served set.
- **No positive transfers, voluntary participation and consumer sovereignty**, for every cross-monotonic method with nonnegative shares.
- **Not efficient.** The served set need not maximize total value minus cost. Let $C(S) = 1$ for every nonempty $S$, with equal shares, and let the values be $(0.6, 0.3, 0.3)$. In round 1 the shares are $1/3$, so players 2 and 3 leave. Then player 1 alone has share 1 and leaves too. Nobody is served, although serving all three gives a surplus of $1.2 - 1 = 0.2$. This loss is not a defect of the method: by the [Green-Laffont theorem](/green-laffont-theorem/), no strategyproof mechanism is both efficient and budget balanced in general.
- **Bounded efficiency loss for submodular costs.** For a [submodular](/submodular-function/) cost, the Shapley value is cross-monotonic and budget balanced. Roughgarden and Sundararajan (2009) showed that the Shapley value mechanism then has social cost (the cost of the served set plus the values of the excluded players) at most $H_n$ times the optimum, where $H_n$ is the $n$th harmonic number.

## Variants and improvements

- **Shapley value mechanism.** For submodular costs, the method is the Shapley value of the cost function restricted to the current set. Moulin and Shenker (2001) compared it with the marginal cost mechanism, which is efficient but not budget balanced.
- **Approximate budget balance.** For hard problems, the exact cost is not available, and the method is only $\beta$-budget balanced for some $\beta > 1$, relative to the optimal cost. For Steiner tree, [Jain-Vazirani cost sharing](/jain-vazirani-steiner-cost-sharing/) gives a cross-monotonic 2-budget balanced method. Roughgarden and Sundararajan (2009) showed that its Moulin mechanism has social cost within $O(\log^2 k)$ of the optimum for $k$ players, and that no Moulin mechanism with constant budget balance for Steiner tree does better than $\Omega(\log^2 k)$.
- **Limits of cross-monotonicity.** For some problems, every cross-monotonic method recovers only a small fraction of the cost, and group strategyproof mechanisms that are not Moulin mechanisms exist when the cost is not submodular (Immorlica, Mahdian and Mirrokni 2008).
- **Strategyproof but not group strategyproof.** The [VCG mechanism](/vcg-mechanism/) with the [Clarke pivot rule](/clarke-pivot-rule/) chooses the efficient set, but it can run a deficit and is not group strategyproof.

## When to use it

Use the Moulin mechanism when a service with a shared cost is offered to players with private values, the payments must cover the cost, and collusion among players is a concern. It needs a cross-monotonic cost-sharing method for the problem. Such methods exist for submodular costs (the Shapley value), for the airport game, for public goods with a fixed cost (equal split), and with approximate budget balance for Steiner trees and facility location. Do not use it when efficiency matters more than budget balance, or when no cross-monotonic method with a useful budget balance factor is known for the problem.

## Pitfalls

- **A method that is not cross-monotonic.** The proof needs cross-monotonicity at every step. With [Bird's rule](/bird-rule/) on a spanning tree game whose shares are $(8)$, $(8, 1)$ and $(1, 4, 7)$ on $\{1\}$, $\{1, 2\}$ and $\{1, 2, 3\}$, and $(4, 7)$ on $\{2, 3\}$, a player 2 with value 2 is not served when it bids truthfully against bids 8 and 0. If it bids 4, it is served at price 1 and gains 1.
- **Inexact arithmetic.** Line L3 compares a bid with a share. With floating point shares, a player whose bid equals its share can be removed by a rounding error, which changes the outcome. Use exact rationals, as the code does.
- **Ties.** The mechanism serves a player whose bid equals its share. Any fixed rule for ties keeps the proof, but the bid grid in a test must include the share values to check this case.
- **Payments from the wrong set.** Each served player pays its share in the final set, not in the set of an earlier round. The shares of earlier rounds are smaller, and using them breaks budget balance.
- **Group strategyproofness is not efficiency.** A group strategyproof, budget balanced mechanism can serve nobody when serving everyone is better, as in the example under Properties.

## Implementations

## History

Moulin (1999) introduced the mechanism for a cross-monotonic cost-sharing method and proved that it is coalition strategyproof. For submodular costs he showed that these mechanisms are the budget balanced, group strategyproof mechanisms that satisfy the participation conditions. Moulin and Shenker (2001) studied the trade-off between budget balance and efficiency for submodular costs and compared the Shapley value mechanism with the marginal cost mechanism. Computer scientists then applied the mechanism to multicast and network design. Jain and Vazirani (2001) gave a cross-monotonic method for Steiner trees, and later work found methods for facility location and other problems and measured their efficiency loss (Roughgarden and Sundararajan 2009).

## References
