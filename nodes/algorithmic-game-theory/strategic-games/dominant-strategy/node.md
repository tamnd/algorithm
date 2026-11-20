---
tag: 98QV9Y
kind: definition
slug: dominant-strategy
name: Dominant strategy
aliases:
- strictly dominant strategy
- weakly dominant strategy
area: algorithmic-game-theory/strategic-games
level: intro
summary: A strategy that is a best response to every profile of the other players; strictly dominant if it beats every other strategy against every profile.
prereqs: [normal-form-game, best-response]
see_also: [iterated-elimination-of-dominated-strategies, prisoners-dilemma, nash-equilibrium, vickrey-auction, dominant-strategy-incentive-compatibility, pure-nash-equilibrium, coarse-correlated-equilibrium]
sources:
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 4 (strictly and weakly dominated actions)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 3 (dominant strategies and dominant-strategy equilibrium) and Chapter 4 (dominated strategies)
  - paper: "William Vickrey, Counterspeculation, auctions, and competitive sealed tenders, Journal of Finance 16(1) (1961), 8-37"
    title: Counterspeculation, auctions, and competitive sealed tenders
    locator: the second-price sealed-bid auction, in which bidding the true value is a dominant strategy
---

A dominant strategy of a player is a strategy that is a [best response](/best-response/) to every possible choice of the other players, so the player can choose it without any prediction of what the others do. When every player has one, the profile of dominant strategies is the obvious outcome of the game, as defection in the [prisoner's dilemma](/prisoners-dilemma/) and truthful bidding in the [Vickrey auction](/vickrey-auction/). Most games have no dominant strategy; the weaker idea of removing dominated strategies one at a time is [iterated elimination of dominated strategies](/iterated-elimination-of-dominated-strategies/).

## Definition

Let $G = (N, (S_i), (u_i))$ be a [normal-form game](/normal-form-game/), with payoffs that the players maximize. Fix a player $i$ and two strategies $s_i, s_i' \in S_i$.

- $s_i$ *strictly dominates* $s_i'$ if $u_i(s_i, s_{-i}) > u_i(s_i', s_{-i})$ for every profile $s_{-i}$ of the others.
- $s_i$ *weakly dominates* $s_i'$ if $u_i(s_i, s_{-i}) \ge u_i(s_i', s_{-i})$ for every $s_{-i}$, with strict inequality for at least one $s_{-i}$.

A strategy $s_i$ is *strictly dominant* if it strictly dominates every other strategy of player $i$, and *weakly dominant* if it weakly dominates every other strategy. Some authors call $s_i$ weakly dominant when $u_i(s_i, s_{-i}) \ge u_i(s_i', s_{-i})$ for all $s_i'$ and $s_{-i}$, without the strict part; this is the same as being a best response to every $s_{-i}$, and it is the form used in [dominant-strategy incentive compatibility](/dominant-strategy-incentive-compatibility/).

A profile in which every player plays a strictly (or weakly) dominant strategy is a *dominant-strategy equilibrium*.

In the other direction, $s_i'$ is *strictly dominated* if some strategy strictly dominates it. The dominator may be pure or a [mixed strategy](/mixed-strategy/) $\sigma_i$, with $u_i(\sigma_i, s_{-i}) > u_i(s_i', s_{-i})$ for every $s_{-i}$; say which one is meant, because a strategy can be dominated by a mix and by no pure strategy.

**Pure profiles are enough.** The conditions quantify over pure profiles $s_{-i}$. They then hold against every mixed profile $\sigma_{-i}$ too, because $u_i(s_i, \sigma_{-i})$ is an average of the values $u_i(s_i, s_{-i})$ with the same weights for every $s_i$. So a strictly dominant strategy is the unique best response to every $\sigma_{-i}$.

**Basic facts.**

1. A player has at most one strictly dominant strategy: two would each beat the other.
2. A dominant-strategy equilibrium is a [Nash equilibrium](/nash-equilibrium/), since every player plays a best response to everything.
3. If every player has a strictly dominant strategy, their profile is the unique Nash equilibrium, also among mixed profiles: in any equilibrium, every strategy in the support of $\sigma_i$ is a best response, and the only best response is the dominant one.
4. A strictly dominated strategy gets probability 0 in every Nash equilibrium and in every [correlated equilibrium](/correlated-equilibrium/), but it can get positive probability in a [coarse correlated equilibrium](/coarse-correlated-equilibrium/), which compares only with fixed deviations.

## Examples and non-examples

Each table lists the payoff of the row player first.

**Prisoner's dilemma.** Each player can cooperate (C) or defect (D).

| | C | D |
| --- | --- | --- |
| C | 3, 3 | 0, 5 |
| D | 5, 0 | 1, 1 |

For the row player, D gives $5 > 3$ against C and $1 > 0$ against D, so D is strictly dominant; the game is symmetric, so D is strictly dominant for the column player too. (D, D) is the dominant-strategy equilibrium and the unique Nash equilibrium, with payoffs $(1, 1)$, although (C, C) gives both players 3.

**Second-price auction.** Three bidders have values 10, 7 and 3 for one item. Each submits a bid, the highest bid wins, and the winner pays the second highest bid; ties go to the bidder with the smallest index. A bidder with value $v$ who wins at price $p$ gets $v - p$, and a loser gets 0. Bidding the true value is weakly dominant for every bidder ([Vickrey auction](/vickrey-auction/)). With truthful bids the bidder with value 10 wins and pays 7. Truthful bidding is not strictly dominant: against bids 7 and 3, the first bidder gets 3 with a bid of 8 as well as with a bid of 10. But against the bids 9 and 0, a bid of 8 loses and gets 0, while the bid of 10 wins at 9 and gets 1.

**Other equilibria beside a weakly dominant one.** In the same auction, the bids $(0, 100, 0)$ form a Nash equilibrium in which the bidder with value 7 wins at price 0. The bidder with value 10 would have to bid at least 100 to win, and would then pay 100; the bidder with value 3 is in the same position. So a weakly dominant equilibrium need not be the only equilibrium, and the other equilibria can use weakly dominated strategies.

**Non-example: battle of the sexes and chicken.** In the battle of the sexes, with payoffs $(2, 1)$ at (Opera, Opera), $(1, 2)$ at (Football, Football) and $(0, 0)$ elsewhere, the best strategy of each player is to match the other, so neither strategy is dominant for anyone. In chicken, dare is best against chicken out and chicken out is best against dare, so again no strategy is dominant. Both games have several equilibria, which a dominance argument cannot select from.

**Non-example: dominated but not by a pure strategy.** If the row player's rows pay $(3, 0)$, $(0, 3)$ and $(1, 1)$ against the two columns, no row dominates row 3, but the mix $(1/2, 1/2, 0)$ gets $3/2$ against each column and strictly dominates it. No row is dominant.

## Related definitions

- **Iterated dominance.** Remove a dominated strategy, then look again in the smaller game ([iterated elimination of dominated strategies](/iterated-elimination-of-dominated-strategies/)). A game is *dominance solvable* if this leaves one profile.
- **Best response.** A dominant strategy is a best response to every profile; a never-best response is the same as a strictly dominated strategy in two-player games ([best response](/best-response/)).
- **Pure Nash equilibrium.** Each strategy is a best response to the others' actual strategies only ([pure Nash equilibrium](/pure-nash-equilibrium/)).
- **Dominant-strategy incentive compatibility.** A mechanism in which truth telling is a weakly dominant strategy for every agent ([DSIC](/dominant-strategy-incentive-compatibility/)).

## References
