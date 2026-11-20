---
tag: 67YX8R
kind: model
slug: prisoners-dilemma
name: "Prisoner's dilemma"
aliases:
- prisoner's dilemma game
area: algorithmic-game-theory/strategic-games
level: intro
summary: A two-player game in which defecting is a dominant strategy for both players, yet mutual cooperation gives both a higher payoff.
prereqs: [bimatrix-game, dominant-strategy, pure-nash-equilibrium]
see_also: [nash-equilibrium, pareto-optimality, price-of-anarchy, subgame-perfect-equilibrium, evolutionarily-stable-strategy, replicator-dynamics, correlated-equilibrium, iterated-elimination-of-dominated-strategies]
sources:
  - paper: doi:10.1287/mnsc.5.1.5
    title: "Merrill M. Flood, Some experimental games, Management Science 5(1) (1958), 5-26"
    locator: the RAND experiments of January 1950 by Flood and Dresher, including the 100-round game that became the prisoner's dilemma (first issued as RAND report RM-789, 1952)
  - paper: "Albert W. Tucker, On jargon, the prisoner's dilemma, UMAP Journal 1 (1980), 101"
    title: "On jargon: the prisoner's dilemma"
    locator: the prison story and the name, first told in a talk at Stanford in May 1950
  - paper: "Robert Axelrod, Effective choice in the prisoner's dilemma, Journal of Conflict Resolution 24(1) (1980), 3-25; and More effective choice in the prisoner's dilemma, Journal of Conflict Resolution 24(3) (1980), 379-403"
    title: Effective choice in the prisoner's dilemma, and More effective choice in the prisoner's dilemma
    locator: the two computer tournaments of the iterated game, both won by tit for tat
  - paper: doi:10.1126/science.7466396
    title: "Robert Axelrod and William D. Hamilton, The evolution of cooperation, Science 211(4489) (1981), 1390-1396"
    locator: the conditions under which tit for tat is stable in the iterated game with continuation probability w
  - paper: "Drew Fudenberg and Eric Maskin, The folk theorem in repeated games with discounting or with incomplete information, Econometrica 54(3) (1986), 533-554"
    title: The folk theorem in repeated games with discounting or with incomplete information
    locator: the folk theorem for subgame perfect equilibria of discounted repeated games
  - paper: "Martin Nowak and Karl Sigmund, A strategy of win-stay, lose-shift that outperforms tit-for-tat in the Prisoner's Dilemma game, Nature 364 (1993), 56-58"
    title: A strategy of win-stay, lose-shift that outperforms tit-for-tat in the Prisoner's Dilemma game
    locator: evolutionary simulations of the iterated game with errors
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 2 (the prisoner's dilemma as a strategic game) and Chapter 8 (repeated games and the folk theorems)
---

The prisoner's dilemma is a two-player game in which each player can cooperate or defect, defecting is better for each player whatever the other does, and yet both players get more when both cooperate than when both defect. It is the standard model of a conflict between individual and group interest: the only [Nash equilibrium](/nash-equilibrium/) is mutual defection, which is not [Pareto optimal](/pareto-optimality/). Merrill Flood and Melvin Dresher at RAND used the game in experiments in January 1950, and Albert Tucker gave it its name and its story in May 1950.

## The machine

The game is a symmetric [bimatrix game](/bimatrix-game/) with two strategies per player, C (cooperate) and D (defect). Each table lists the payoff of the row player first.

| | C | D |
| --- | --- | --- |
| C | R, R | S, T |
| D | T, S | P, P |

The four numbers are the *reward* $R$ for mutual cooperation, the *temptation* $T$ to defect against a cooperator, the *punishment* $P$ for mutual defection and the *sucker's payoff* $S$. The game is a prisoner's dilemma when

$$T > R > P > S.$$

Many authors also ask that $2R > T + S$, so that in a repeated game, taking turns at exploiting each other gives less than steady cooperation. The values used on this site, and in Axelrod's tournaments, are $T = 5$, $R = 3$, $P = 1$ and $S = 0$:

| | C | D |
| --- | --- | --- |
| C | 3, 3 | 0, 5 |
| D | 5, 0 | 1, 1 |

**Tucker's story.** Two suspects are held in separate cells. If both stay silent (C), both get a short sentence. If one confesses (D) and the other stays silent, the one who confesses goes free and the other gets a long sentence. If both confess, both get a medium sentence. In years in prison the story is a cost game, which the players minimize; negating the years gives a utility table with $T > R > P > S$.

**The donation game.** A common special case: cooperating costs the cooperator $c > 0$ and gives the other player $b > c$. Then $T = b$, $R = b - c$, $P = 0$ and $S = -c$, and $2R > T + S$ holds because $b > c$.

**The repeated game.** In the *iterated* prisoner's dilemma the same two players play the stage game again and again and see all past moves. With a discount factor $\delta \in (0, 1)$, or a probability $\delta$ that one more round is played, the payoff of a stream $x_0, x_1, \ldots$ is $\sum_{t \ge 0} \delta^t x_t$. A strategy maps each history to C or D. *Tit for tat* plays C in round 0 and then copies the other player's last move; *grim trigger* plays C until the other player defects once and D forever after.

## What it counts

The model counts the payoff of each player at the outcome, and for questions of efficiency the sum of the two payoffs, the social welfare.

- At (C, C) the welfare is $2R$, the largest of the four outcomes when $2R > T + S$. At (D, D) it is $2P$.
- The equilibrium outcome (D, D) is worse for both players than (C, C), so it is not Pareto optimal.
- With the standard values, the welfare is 6 at (C, C) and 2 at (D, D). The unique equilibrium is (D, D), so the [price of anarchy](/price-of-anarchy/) and the price of stability in the welfare form are both $6/2 = 3$; for general values with $P > 0$ and $2R > T + S$, both are $R/P$.

In the repeated game the model counts the discounted sum of stage payoffs, or the average payoff per round.

## Relation to other models

- **Other two-by-two games.** Changing the order of the four numbers gives other games: with $T > R > S > P$ it is the game of chicken, where each player wants to do the opposite of the other; with $R > T > P > S$ it is the stag hunt, where both (C, C) and (D, D) are equilibria. In neither of these is D dominant.
- **Many players.** In the public goods game, each of $n$ players chooses a contribution, the total is multiplied by a factor $r$ with $1 < r < n$ and shared equally. Contributing nothing is dominant, and full contribution by all is better for everyone; it is the $n$-player form of the dilemma.
- **Repeated games and the folk theorem.** The one-shot game has a unique equilibrium, but its infinite repetition with patient players has many. The folk theorem (Fudenberg and Maskin 1986 for subgame perfect equilibria with discounting) says that, for $\delta$ close enough to 1, every feasible pair of average payoffs that gives each player more than $P$ is the outcome of a [subgame perfect equilibrium](/subgame-perfect-equilibrium/) of the repeated prisoner's dilemma. Mutual cooperation is one of these outcomes; mutual defection in every round is another.
- **Evolution.** In a population that plays the one-shot game, D is a strictly dominant strategy, so it is an [evolutionarily stable strategy](/evolutionarily-stable-strategy/), and under the [replicator dynamics](/replicator-dynamics/) the share of C tends to 0 from every interior start. Cooperation can evolve in the repeated game (Axelrod and Hamilton 1981) or with population structure.
- **Hierarchy of equilibria.** The game is the simplest case where all four standard solution sets, [pure Nash](/pure-nash-equilibrium/), mixed Nash, [correlated](/correlated-equilibrium/) and [coarse correlated](/coarse-correlated-equilibrium/) equilibria, coincide; see the first result below.

## Known results in the model

**1. D is strictly dominant, and (D, D) is the only equilibrium in every standard sense.** $T > R$ means D beats C against C, and $P > S$ means D beats C against D, so D is a strictly [dominant strategy](/dominant-strategy/) for both players. So (D, D) is the unique pure and mixed Nash equilibrium. It is also the unique coarse correlated equilibrium, and so the unique correlated equilibrium: for any distribution $p$ on the four profiles, the fixed deviation to D gives the row player $\sum_s p(s)\, u_1(D, s_2) \ge \sum_s p(s)\, u_1(s)$, with strict inequality as soon as $p$ puts positive weight on a profile where the row player plays C. The same holds for the column player. A single round of [iterated elimination of dominated strategies](/iterated-elimination-of-dominated-strategies/) solves the game.

**2. In the finitely repeated game, every subgame perfect equilibrium defects in every round.** If the number of rounds $K$ is known, then in the last round the players face the one-shot game, and every subgame perfect equilibrium plays (D, D) there whatever happened before. So play in round $K - 1$ does not change the future, and (D, D) is again the only choice. Backward induction gives defection in every round.

**3. Grim trigger sustains cooperation if and only if $\delta \ge (T - R)/(T - P)$.** Against grim trigger, cooperating forever gives $R/(1 - \delta)$. The best deviation defects in some round and then, since the other player defects forever, defects forever, which gives $T + \delta P/(1 - \delta)$ from that round on. The first is at least the second if and only if $R \ge (1 - \delta) T + \delta P$, that is $\delta (T - P) \ge T - R$. With the standard values the threshold is $\delta \ge 2/4 = 1/2$; at $\delta = 1/2$ both sides equal 6. Since the punishment phase is the stage equilibrium (D, D), both players using grim trigger is then a subgame perfect equilibrium.

**4. Tit for tat is a best reply to itself if and only if $\delta \ge \max\big((T - R)/(T - P),\ (T - R)/(R - S)\big)$.** Against tit for tat, the opponent's move tomorrow is the player's move today, so the player faces a problem with two states, and some stationary plan is optimal. Steady cooperation gives $R/(1 - \delta)$; defecting forever gives $T + \delta P/(1 - \delta)$; alternating D and C gives $(T + \delta S)/(1 - \delta^2)$. Cooperation is optimal when it beats both, which gives the two thresholds. With the standard values they are $2/4 = 1/2$ and $2/3$, so the condition is $\delta \ge 2/3$; at $\delta = 2/3$ steady cooperation and alternation both give 9. Axelrod and Hamilton (1981) state this condition, with $\delta$ as the probability $w$ of one more round. Tit for tat against itself is a Nash equilibrium of the repeated game, but not a subgame perfect one: after a single defection it locks into alternation.

**5. Tournaments (measurements).** Axelrod (1980) invited strategies for the iterated game with the standard values. The first tournament had 14 entries plus a random strategy, and matches of 200 rounds; the second had 62 entries plus a random strategy, with match lengths that the entrants did not know. Tit for tat, entered by Anatol Rapoport, had the highest total score in both. These are results of particular fields of entries, not theorems: a strategy's score depends on the other entries. With errors in the moves, simulations of Nowak and Sigmund (1993) found that win-stay, lose-shift (repeat the last move after payoff $R$ or $T$, switch after $P$ or $S$) outperforms tit for tat in evolving populations.

**6. Experiments (measurements).** Flood and Dresher's first experiment at RAND in January 1950 had two colleagues play 100 rounds of a variant of the game; the players cooperated in many rounds instead of defecting in all of them, as the equilibrium analysis predicts (Flood 1958). This is one pair of players, not a controlled study.

## References
