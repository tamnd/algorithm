---
tag: QT7VWZ
kind: definition
slug: mixed-strategy
name: Mixed strategy
aliases:
- randomized strategy
area: algorithmic-game-theory/strategic-games
level: intro
summary: A probability distribution over a player's pure strategies; the player draws one pure strategy from it, independently of the other players.
prereqs: [normal-form-game, probability-distribution, expected-value]
see_also: [nash-equilibrium, best-response, minimax-theorem, indifference-principle, support-enumeration, kuhn-theorem-behavioral-strategies, correlated-equilibrium, evolutionarily-stable-strategy]
sources:
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 3 (mixed strategy Nash equilibrium, and the interpretations of mixed strategies)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 3 (strategies in normal-form games, mixed strategies and their expected utility)
  - paper: "J. von Neumann, Zur Theorie der Gesellschaftsspiele, Mathematische Annalen 100 (1928), 295-320"
    title: Zur Theorie der Gesellschaftsspiele
    locator: mixed strategies in two-person zero-sum games and the minimax theorem
  - paper: "John C. Harsanyi, Games with randomly disturbed payoffs, a new rationale for mixed-strategy equilibrium points, International Journal of Game Theory 2 (1973), 1-23"
    title: Games with randomly disturbed payoffs, a new rationale for mixed-strategy equilibrium points
    locator: the purification of mixed equilibria by small private payoff shocks
---

A mixed strategy of a player is a probability distribution over the player's pure strategies: the player uses a private random device to pick one pure strategy, independently of the other players. Mixed strategies are what makes [Nash's theorem](/nash-existence-theorem/) true, since many games, such as matching pennies, have no equilibrium in pure strategies. They also give the security levels of the [minimax theorem](/minimax-theorem/). A distribution over whole profiles that the players share is a different object, the [correlated equilibrium](/correlated-equilibrium/).

## Definition

Let $G = (N, (S_i), (u_i))$ be a finite [normal-form game](/normal-form-game/). A *mixed strategy* of player $i$ is a [probability distribution](/probability-distribution/) $\sigma_i$ on $S_i$, a point of the simplex

$$\Delta(S_i) = \Big\{\sigma_i : S_i \to [0, 1] \ :\ \sum_{s_i \in S_i} \sigma_i(s_i) = 1\Big\}.$$

The pure strategy $s_i$ is identified with the distribution that puts probability 1 on $s_i$, so the pure strategies are the vertices of the simplex. The *support* of $\sigma_i$ is $\{s_i : \sigma_i(s_i) > 0\}$. A mixed strategy is *completely mixed* (or fully mixed) if its support is all of $S_i$.

A *mixed profile* $\sigma = (\sigma_1, \ldots, \sigma_n)$ has one mixed strategy per player, and the players draw independently, so profile $s$ comes up with probability $\prod_{k \in N} \sigma_k(s_k)$. The payoff of player $i$ is the [expected value](/expected-value/)

$$u_i(\sigma) = \sum_{s \in S} \Big(\prod_{k \in N} \sigma_k(s_k)\Big)\, u_i(s).$$

**Linearity in the own strategy.** For a fixed $\sigma_{-i}$,

$$u_i(\sigma_i, \sigma_{-i}) = \sum_{s_i \in S_i} \sigma_i(s_i)\, u_i(s_i, \sigma_{-i}),$$

a weighted average of the payoffs of the pure strategies. Two consequences follow. First, no mixed strategy does better against $\sigma_{-i}$ than the best pure strategy, so to test a profile for an equilibrium it is enough to test pure deviations. Second, $\sigma_i$ is a [best response](/best-response/) to $\sigma_{-i}$ if and only if every pure strategy in its support is a best response; in particular, all pure strategies in the support give the same payoff. This indifference is what [support enumeration](/support-enumeration/) and the [indifference principle](/indifference-principle/) solve for.

**Payoffs must be cardinal.** The expected payoff is meaningful only if $u_i$ is a von Neumann-Morgenstern utility, so that the player ranks lotteries by their expected utility. If the payoffs only rank the outcomes, a mixed strategy has no well defined value.

**Three readings.** A mixed strategy can be read as a deliberate randomization by the player; as the frequencies of pure strategies in a large population, each member playing one pure strategy (the reading of [evolutionary stability](/evolutionarily-stable-strategy/)); or as the belief of the other players about a choice that is in fact pure. Harsanyi (1973) showed that, in almost all finite games, every mixed equilibrium is the limit of equilibria in pure strategies of games in which each player's payoffs have small private random shocks, which supports the third reading.

## Examples and non-examples

Each table lists the payoff of the row player first.

**Matching pennies.** The row player wins 1 if the two coins match and loses 1 otherwise. Each pure strategy of the row player loses 1 against the right reply, so its security level in pure strategies is $-1$. The mix $(1/2, 1/2)$ gets 0 against both columns, so its security level is 0. Against the column mix $(3/4, 1/4)$, Heads gives the row player $3/4 - 1/4 = 1/2$ and Tails gives $-1/2$; the mix $(1/2, 1/2)$ gives their average, 0, which is not a best response. Only $(1/2, 1/2)$ for both players is an equilibrium.

**Chicken.** Each driver can dare (D) or chicken out (C).

| | D | C |
| --- | --- | --- |
| D | 0, 0 | 7, 2 |
| C | 2, 7 | 6, 6 |

If the column player plays C with probability $q$, the row player gets $7q$ from D and $2(1 - q) + 6q = 2 + 4q$ from C. These are equal when $q = 2/3$. So in the symmetric mixed equilibrium each player plays C with probability $2/3$, both pure strategies give $14/3$, and each player gets $14/3$.

**Dominance by a mixed strategy.** Let the row player have three rows with payoffs $(3, 0)$, $(0, 3)$ and $(1, 1)$ against the two columns. No row dominates the third one: row 1 gets 0 in column 2 and row 2 gets 0 in column 1. But the mix $(1/2, 1/2, 0)$ gets $3/2$ in each column, more than 1. Against a column mix that plays column 1 with probability $y$, rows 1 and 2 give $3y$ and $3 - 3y$, and the larger of the two is at least $3/2$, so row 3 is never a best response. The [iterated elimination of dominated strategies](/iterated-elimination-of-dominated-strategies/) removes row 3 only with the mixed test.

**Non-example: a shared lottery.** In the battle of the sexes, the distribution that puts $1/2$ on (Opera, Opera) and $1/2$ on (Football, Football) is not a mixed profile. If independent mixes $x$ and $y$ gave positive probability to both of these profiles, then $x$ and $y$ would both give positive probability to Opera and to Football, and (Opera, Football) would also have positive probability. The players need a common coin for this lottery, which is a correlated strategy.

**Non-example: a behavior strategy.** In a game tree, a strategy that randomizes separately at each decision point is a *behavior strategy*, not a mixed strategy. The two give the same outcomes in games with perfect recall ([Kuhn's theorem](/kuhn-theorem-behavioral-strategies/)), but a behavior strategy needs one distribution per decision point, while a mixed strategy needs one probability per complete plan.

## Related definitions

- **Mixed extension.** The game with strategy sets $\Delta(S_i)$ and payoffs $u_i(\sigma)$. A [Nash equilibrium](/nash-equilibrium/) of $G$ in mixed strategies is a pure equilibrium of its mixed extension.
- **Security level.** $\max_{\sigma_i} \min_{s_{-i}} u_i(\sigma_i, s_{-i})$, the payoff that player $i$ can guarantee. In two-player [zero-sum games](/zero-sum-game/) the two security levels meet at the value ([minimax theorem](/minimax-theorem/)).
- **Correlated strategy.** A distribution on the whole set of profiles $S$; the mixed profiles are the product distributions among them ([correlated equilibrium](/correlated-equilibrium/)).
- **Behavior strategy.** One distribution per information set of a game tree ([extensive-form game](/extensive-form-game/)).

## References
