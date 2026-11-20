---
tag: JY84QQ
kind: model
slug: rubinstein-bargaining-model
name: Rubinstein bargaining model
aliases:
- alternating offers bargaining
area: algorithmic-game-theory/cooperative-games
level: advanced
summary: Two players alternate offers to split a surplus with discounting. Its unique subgame perfect equilibrium gives immediate agreement.
prereqs: [subgame-perfect-equilibrium, extensive-form-game]
see_also: [nash-bargaining-solution, perfect-information-game, nash-equilibrium, pareto-optimality, eisenberg-gale-program]
sources:
  - paper: "Ariel Rubinstein, Perfect equilibrium in a bargaining model, Econometrica 50(1) (1982), 97-109"
    title: Perfect equilibrium in a bargaining model
    locator: the alternating offers game with discounting and the theorem that it has a unique subgame perfect equilibrium
  - paper: "Avner Shaked and John Sutton, Involuntary unemployment as a perfect equilibrium in a bargaining model, Econometrica 52(6) (1984), 1351-1364"
    title: Involuntary unemployment as a perfect equilibrium in a bargaining model
    locator: the short proof of uniqueness from the largest and smallest subgame perfect equilibrium payoffs
  - book: "Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994"
    title: A Course in Game Theory
    locator: Chapter 7, Bargaining Games (from p. 117), Section 7.2 and Proposition 122.1 on the subgame perfect equilibrium of the bargaining game of alternating offers
  - paper: doi:10.2307/2555382
    title: "Ken Binmore, Ariel Rubinstein and Asher Wolinsky, The Nash bargaining solution in economic modelling, RAND Journal of Economics 17(2) (1986), 176-188"
    locator: the limit of the equilibrium agreement as the time between offers goes to 0, which is the Nash bargaining solution
---

The Rubinstein bargaining model is a game in which two players split a surplus by taking turns to make offers. Each delay costs both players, because a payoff received later is worth less. The model has many [Nash equilibria](/nash-equilibrium/), but Rubinstein (1982) proved that it has exactly one [subgame perfect equilibrium](/subgame-perfect-equilibrium/). In it the first offer is accepted at once, and the split depends on the players' patience and on who moves first. The model gives a strategic account of bargaining power, and in the limit of fast offers it selects the [Nash bargaining solution](/nash-bargaining-solution/).

## The machine

Two players split a pie of size 1. Time is divided into periods $t = 0, 1, 2, \ldots$.

- In even periods player 1 proposes a split $(x, 1 - x)$ with $0 \le x \le 1$, and player 2 accepts or rejects.
- In odd periods player 2 proposes a split, and player 1 accepts or rejects.
- If a proposal $(x_1, x_2)$ is accepted in period $t$, the game ends with the payoffs $(\delta_1^t x_1, \delta_2^t x_2)$, where $0 < \delta_i < 1$ is the discount factor of player $i$.
- If no proposal is ever accepted, both players get 0.

This is an [extensive form game](/extensive-form-game/) with [perfect information](/perfect-information-game/) and an infinite horizon. A strategy says, for every history, what to propose and which proposals to accept. The finite-horizon version, with a last period after which both get 0, is solved by backward induction from the last period, where the proposer takes everything. With one period it is the ultimatum game.

## What it counts

The model predicts when agreement happens and how the pie is split. It answers through the subgame perfect equilibrium, which requires that the strategies form a Nash equilibrium in every subgame, so that no threat is empty. The equilibrium of the infinite game is stationary:

- Player 1 always proposes $(x^*, 1 - x^*)$ and accepts a proposal exactly when its share is at least $\delta_1 x^* = 1 - y^*$.
- Player 2 always proposes $(1 - y^*, y^*)$ and accepts a proposal exactly when its share is at least $\delta_2 y^* = 1 - x^*$.

The two thresholds make the responder indifferent between accepting now and proposing next period: $1 - x^* = \delta_2 y^*$ and $1 - y^* = \delta_1 x^*$. Solving the two equations gives

$$x^* = \frac{1 - \delta_2}{1 - \delta_1 \delta_2}, \qquad y^* = \frac{1 - \delta_1}{1 - \delta_1 \delta_2}.$$

The first proposal is accepted, so the outcome is $(x^*, 1 - x^*)$ in period 0, with no delay and no waste.

- **Equal patience.** If $\delta_1 = \delta_2 = \delta$, then $x^* = 1/(1 + \delta)$, which is more than $1/2$: moving first is an advantage, and it disappears as $\delta \to 1$.
- **Patience is power.** With $\delta_1 = 0.9$ and $\delta_2 = 0.8$, $x^* = 0.2/0.28 = 5/7$. As $\delta_1 \to 1$ with $\delta_2$ fixed, $x^*$ goes to 1.
- **Finite horizon.** With $T$ periods and $\delta = 9/10$, let $x_T$ be the share of the first proposer. Then $x_1 = 1$ and $x_T = 1 - \delta x_{T-1}$, which gives $1$, $1/10$, $91/100$, $181/1000$, $8371/10000$, $24661/100000$ for $T = 1, \ldots, 6$. The shares alternate around the infinite-horizon value $10/19 \approx 0.526$ and converge to it.

## Relation to other models

- **Nash bargaining solution.** Let a period last $\Delta$ units of time, and let $\delta_i = e^{-r_i \Delta}$ for discount rates $r_1, r_2 > 0$. As $\Delta \to 0$, $x^* \to r_2/(r_1 + r_2)$. This is the asymmetric [Nash bargaining solution](/nash-bargaining-solution/) of the problem with weights $1/r_1$ and $1/r_2$, and the symmetric one if $r_1 = r_2$ (Binmore, Rubinstein and Wolinsky 1986). So the axiomatic solution can be read as the limit of a noncooperative game.
- **Ultimatum game.** The one-period game, in which the proposer offers the responder 0 (or the smallest unit) in the subgame perfect equilibrium.
- **Nash equilibrium.** For every split $(x, 1 - x)$ there is a Nash equilibrium of the infinite game with this immediate agreement: player 1 always demands $x$ and rejects anything less, and player 2 always demands $1 - x$ and rejects anything less. Most of these equilibria rely on threats that are not credible, and subgame perfection removes them.
- **General surplus sets.** The pie can be replaced by a set of utility pairs with a Pareto frontier. The equilibrium is then described by two agreements $x^*$ and $y^*$ with $y^*_1 = \delta_1 x^*_1$ and $x^*_2 = \delta_2 y^*_2$, which again converge to the Nash solution as the period length goes to 0.

## Known results in the model

- **Uniqueness (Rubinstein 1982).** The game has a unique subgame perfect equilibrium, the stationary one above, and agreement is immediate. Osborne and Rubinstein (1994) give it as Proposition 122.1.
- **Short proof of uniqueness (Shaked and Sutton 1984).** Let $M_1$ and $m_1$ be the largest and smallest subgame perfect payoffs of player 1 in subgames where player 1 proposes, and let $M_2$ and $m_2$ be the same for player 2 when player 2 proposes. In a subgame where player 1 proposes, player 2 can reject and propose next period, so it accepts any share above $\delta_2 M_2$ and gets at least $\delta_2 m_2$. If it rejects, player 1 gets at most $\delta_1 (1 - m_2) \le 1 - \delta_2 m_2$. Hence $m_1 \ge 1 - \delta_2 M_2$ and $M_1 \le 1 - \delta_2 m_2$. In the same way $m_2 \ge 1 - \delta_1 M_1$ and $M_2 \le 1 - \delta_1 m_1$. Then $M_1 \le 1 - \delta_2 (1 - \delta_1 M_1)$, so $M_1 \le x^*$, and $m_1 \ge 1 - \delta_2 (1 - \delta_1 m_1)$, so $m_1 \ge x^*$. So $M_1 = m_1 = x^*$, and in the same way $M_2 = m_2 = y^*$.
- **Many players.** With three or more players who must all agree, the subgame perfect equilibrium is not unique when the players are patient enough, and any split can be an equilibrium outcome.
- **Incomplete information.** If a player's discount factor or value is private, equilibria with delay appear, and the model becomes a tool to explain strikes and other costly disagreements.

## References
