---
tag: AW27VP
kind: model
slug: weighted-voting-game
name: Weighted voting game
aliases:
- weighted majority game
area: algorithmic-game-theory/cooperative-games
level: core
summary: A simple game in which each player has a weight and a coalition wins if its total weight reaches a quota.
prereqs: [transferable-utility-game]
see_also: [shapley-shubik-index, banzhaf-index, power-index-dynamic-programming, power-index-hardness, core-of-a-cooperative-game, subset-sum-problem, boolean-function, apportionment-problem]
sources:
  - book: isbn:9781608456529
    title: Georgios Chalkiadakis, Edith Elkind and Michael Wooldridge, Computational Aspects of Cooperative Game Theory, Morgan and Claypool, 2011
    locator: Chapter 4, Weighted voting games (definition, power indices, their complexity, and the core)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Section 12.3.1, Weighted majority games and weighted voting games
  - paper: doi:10.2307/1951053
    title: "Lloyd S. Shapley and Martin Shubik, A method for evaluating the distribution of power in a committee system, American Political Science Review 48(3) (1954), 787-792"
    locator: voting bodies as simple games, and the power of a player as the fraction of orders in which it is pivotal
  - paper: doi:10.1007/s10472-009-9162-5
    title: "Edith Elkind, Leslie Ann Goldberg, Paul W. Goldberg and Michael Wooldridge, On the computational complexity of weighted voting games, Annals of Mathematics and Artificial Intelligence 56(2) (2009), 109-131"
    locator: the complexity of dummy players, the core, the least core and the nucleolus of weighted voting games
  - paper: doi:10.3390/g9020029
    title: "Alexander Mayer, Luxembourg in the early days of the EEC: null player or not?, Games 9(2) (2018), article 29"
    locator: the weights and quota of the Council of the EEC from 1958, and the discussion of Luxembourg as a null player
---

A weighted voting game models a body that decides by weighted votes: shareholders with shares, parties with seats, or member states with votes in a council. Each player has a weight, and a coalition wins if its total weight reaches the quota. The game is the standard compact form of a *simple game*, a TU game in which every coalition has the value 0 or 1. It is compact (it needs only $n + 1$ numbers), but its weights can hide the real distribution of power: a player can have a large weight and no influence, or a small weight and as much influence as a large player. The [Shapley-Shubik index](/shapley-shubik-index/) and the [Banzhaf index](/banzhaf-index/) measure this power.

## The machine

**Players and weights.** $N = \{1, \ldots, n\}$. Player $i$ has a weight $w_i \ge 0$. The game has a quota $q$ with $0 < q \le w(N)$, where $w(S) = \sum_{i \in S} w_i$. We write the game as $[q; w_1, \ldots, w_n]$. For computation, the weights and the quota are integers in binary, so the input has $O(n \log w_{\max})$ bits.

**Worth.** The characteristic function is

$$v(S) = 1 \text{ if } w(S) \ge q, \qquad v(S) = 0 \text{ if } w(S) < q.$$

A coalition with $v(S) = 1$ *wins* and one with $v(S) = 0$ *loses*. Since $q > 0$ and $q \le w(N)$, the empty coalition loses and $N$ wins. Since the weights are nonnegative, the game is *monotone*: a superset of a winning coalition wins. If $q > w(N)/2$, the game is *proper*: two disjoint coalitions cannot both win.

**Roles of players.** Player $i$ is a *swing* for a coalition $S \not\ni i$ if $S$ loses and $S \cup \{i\}$ wins. Player $i$ is a *dummy* (a null player) if it is a swing for no coalition. Player $i$ is a *veto player* if every winning coalition contains $i$, that is, if $w(N) - w_i < q$. Player $i$ is a *dictator* if $\{i\}$ wins and every winning coalition contains $i$.

**Standing assumptions.** The worth 1 of a winning coalition is transferable: it stands for the power to pass a decision, which the members can share in any way. The players are the voters themselves, and they vote as blocs.

## What it counts

The model is used to measure the *voting power* of each player: how much a player can change the outcome. The two classic measures are:

- the [Shapley-Shubik index](/shapley-shubik-index/), the fraction of the $n!$ orders in which player $i$ is the pivot, the player whose arrival first makes the coalition win; and
- the [Banzhaf index](/banzhaf-index/), based on the number of coalitions for which $i$ is a swing.

The model is also used for the [core](/core-of-a-cooperative-game/) and the least core, as a way to share a fixed prize among the players so that no winning coalition wants to break away.

## Relation to other models

- **Simple games.** Every weighted voting game is a monotone simple game, but not every monotone simple game is weighted. Let the minimal winning coalitions be $\{1, 2\}$ and $\{3, 4\}$. If weights existed, then $w_1 + w_2 \ge q$ and $w_3 + w_4 \ge q$, while the losing coalitions $\{1, 3\}$ and $\{2, 4\}$ give $w_1 + w_3 < q$ and $w_2 + w_4 < q$. Adding each pair gives $w(N) \ge 2q$ and $w(N) < 2q$, which is a contradiction.
- **Threshold functions.** A weighted voting game is a monotone linear threshold [Boolean function](/boolean-function/) on the indicator vector of the coalition: it outputs 1 when $\sum_i w_i x_i \ge q$.
- **Subset sum and knapsack.** Counting the coalitions with a given total weight is the counting version of the [subset sum problem](/subset-sum-problem/). This link gives both the [dynamic programming algorithm](/power-index-dynamic-programming/) for the indices and their [hardness](/power-index-hardness/).
- **Other compact forms.** A [marginal contribution net](/marginal-contribution-nets/) can express any game, but threshold games rarely have short nets. Intersections of several weighted games (vector weighted games) express every monotone simple game, with enough components.
- **Seat allocation.** In a parliament, the seat counts of the parties, as given by an [apportionment](/apportionment-problem/) method, are the weights, and the quota is the majority.

## Known results in the model

**Weight is not power.** In $[51; 50, 49, 1]$ every winning coalition contains player 1 and one of the others. Players 2 and 3 are symmetric in the game, though their weights are 49 and 1. The Shapley-Shubik index is $(2/3, 1/6, 1/6)$. The swings are 3, 1 and 1, so the raw Banzhaf index is $(3/4, 1/4, 1/4)$ and the normalized one is $(3/5, 1/5, 1/5)$. Player 1 is a veto player, and the core is the single point $(1, 0, 0)$.

**A dummy with a positive weight.** The Council of the European Economic Community from 1958 had the weights 4 for France, Germany and Italy, 2 for Belgium and the Netherlands, and 1 for Luxembourg, with the quota 12: the game $[12; 4, 4, 4, 2, 2, 1]$. Every total of weights of the other five members is even. So a coalition without Luxembourg with weight 11 does not exist, and Luxembourg is never a swing: it is a dummy. The Shapley-Shubik index is $(7/30, 7/30, 7/30, 3/20, 3/20, 0)$, the swing counts are $(10, 10, 10, 6, 6, 0)$, and the normalized Banzhaf index is $(5/21, 5/21, 5/21, 1/7, 1/7, 0)$. Mayer (2018) argues that, in the full institutional setting, this does not mean that Luxembourg had no influence.

**The core.** For a simple game, the core is nonempty if and only if there is a veto player. If $V$ is the set of veto players, the core is the set of vectors $x \ge 0$ with $x(V) = 1$ and $x_i = 0$ for $i \notin V$. In a weighted voting game the veto players are found in $O(n)$ time by the test $w(N) - w_i < q$. Elkind, Goldberg, Goldberg and Wooldridge (2009) study the least core and the nucleolus, which are harder.

**Computing the power indices.** Both indices of all players take pseudo-polynomial time, $O(n^3 q)$ arithmetic operations for the Shapley-Shubik index and less for the Banzhaf index, by [dynamic programming](/power-index-dynamic-programming/) over the weights. With the weights in binary, computing either index is #P-complete, and deciding whether a player is a dummy is coNP-complete ([hardness of power indices](/power-index-hardness/)). The problem is only weakly hard: with weights bounded by a polynomial in $n$, the dynamic program is polynomial.

**Sensitivity.** The power of a player can change in unexpected ways when the rules change. In $[3; 1, 1, 2]$ the Shapley-Shubik index is $(1/6, 1/6, 2/3)$; raise the quota to 4 and every coalition except $N$ loses, so the index becomes $(1/3, 1/3, 1/3)$ and the two small players gain. In $[4; 1, 1, 2]$ all players have $1/3$; add a fourth player of weight 1 and the index becomes $(1/6, 1/6, 1/2, 1/6)$, so a new member raises the power of an old one. With the quota and the other weights fixed, a larger weight never lowers a player's raw index, because every swing stays a swing.

## References
