---
tag: 5FC9J8
kind: definition
slug: nash-equilibrium
name: Nash equilibrium
aliases:
- Nash equilibrium point
area: games-and-search/game-tree-search
level: intro
summary: A strategy profile in which no player can raise their own expected payoff by changing only their own strategy.
prereqs: [zero-sum-game, expected-value]
see_also: [nash-existence-theorem, nash-equilibrium-computation, minimax-theorem, imperfect-information-game, counterfactual-regret-minimization, regret, pareto-optimality, ppad]
sources:
  - paper: doi:10.1073/pnas.36.1.48
    title: "John F. Nash, Equilibrium points in n-person games, Proceedings of the National Academy of Sciences 36(1) (1950), 48-49"
    locator: the definition of an equilibrium point and the existence proof
  - paper: doi:10.2307/1969529
    title: "John Nash, Non-cooperative games, Annals of Mathematics 54(2) (1951), 286-295"
    locator: the definition of equilibrium points, the condition on the pure strategies used, and symmetric equilibria
  - paper: doi:10.1016/0304-4068(74)90037-8
    title: "Robert J. Aumann, Subjectivity and correlation in randomized strategies, Journal of Mathematical Economics 1(1) (1974), 67-96"
    locator: the definition of correlated equilibrium and the example where it beats every Nash equilibrium
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 2 (Nash equilibrium of strategic games) and Chapter 3 (mixed and correlated equilibrium)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 3 (best response, Nash equilibrium, epsilon-Nash equilibrium and correlated equilibrium)
---

A Nash equilibrium is a choice of strategy for each player such that no player can do better by changing only their own choice. It is the basic solution concept of noncooperative game theory, for games with any number of players and any payoffs. Every finite game has one in mixed strategies ([Nash's theorem](/nash-existence-theorem/)), but a game can have many, with different payoffs, and finding one is hard in general ([computation](/nash-equilibrium-computation/)).

## Definition

A finite game in normal form (a *strategic game*) has a finite set of players $N = \{1, \ldots, n\}$, a finite set $S_i$ of pure strategies for each player $i$, and a payoff function $u_i : S \to \mathbb{R}$ for each player on the set of profiles $S = S_1 \times \cdots \times S_n$. The players choose at the same time, and each player wants a high payoff for themselves only.

A *mixed strategy* of player $i$ is a probability distribution $\sigma_i$ on $S_i$. A profile $\sigma = (\sigma_1, \ldots, \sigma_n)$ of independent mixed strategies gives player $i$ the [expected](/expected-value/) payoff

$$u_i(\sigma) = \sum_{s \in S} \Big(\prod_{k \in N} \sigma_k(s_k)\Big)\, u_i(s).$$

Write $\sigma_{-i}$ for the strategies of all players except $i$, and $(\sigma_i', \sigma_{-i})$ for the profile in which only player $i$ changes to $\sigma_i'$.

**Definition.** A profile $\sigma^*$ is a *Nash equilibrium* if for every player $i$ and every mixed strategy $\sigma_i'$ of player $i$,

$$u_i(\sigma_i', \sigma^*_{-i}) \le u_i(\sigma^*).$$

A strategy $\sigma_i$ is a *best response* to $\sigma_{-i}$ if it maximizes $u_i(\cdot, \sigma_{-i})$. So an equilibrium is a profile in which every player plays a best response to the others. It is a *pure* equilibrium if every $\sigma_i^*$ puts probability 1 on one strategy.

**Two equivalent tests.** Because $u_i(\sigma_i', \sigma_{-i}) = \sum_{s_i} \sigma_i'(s_i)\, u_i(s_i, \sigma_{-i})$ is an average of the pure payoffs, these three statements are equivalent for each player $i$:

1. no mixed deviation $\sigma_i'$ gains;
2. no pure deviation $s_i \in S_i$ gains: $u_i(s_i, \sigma^*_{-i}) \le u_i(\sigma^*)$ for all $s_i$;
3. every pure strategy that $\sigma_i^*$ plays with positive probability is a best response: if $\sigma^*_i(s_i) > 0$ then $u_i(s_i, \sigma^*_{-i}) = \max_{t \in S_i} u_i(t, \sigma^*_{-i})$.

Test 2 needs only $\sum_i |S_i|$ comparisons, so a claimed equilibrium is easy to check exactly. Test 3 says that each player is *indifferent* among the strategies in the support. This is the equation that support enumeration solves.

**Approximate equilibria.** For $\varepsilon \ge 0$, $\sigma$ is an *$\varepsilon$-equilibrium* if no player gains more than $\varepsilon$ by a deviation: $u_i(s_i, \sigma_{-i}) \le u_i(\sigma) + \varepsilon$ for all $i$ and $s_i$. With payoffs in $[0, 1]$ this is the notion used in the complexity results and in [counterfactual regret minimization](/counterfactual-regret-minimization/), where the *exploitability* of a strategy pair in a two-player zero-sum game measures the gain of the two best responses.

**Extensive games.** For a game tree, the definition is the same with strategies that give a move at every decision point. In a game with hidden information the strategy chooses at each information set ([imperfect-information games](/imperfect-information-game/)), and by Kuhn's theorem, with perfect recall, behavior strategies give the same equilibria as mixed strategies.

## Examples and non-examples

Each table lists the payoff of the row player first.

**Prisoner's dilemma.** Each player can cooperate (C) or defect (D).

| | C | D |
| --- | --- | --- |
| C | 3, 3 | 0, 5 |
| D | 5, 0 | 1, 1 |

D is better than C for each player whatever the other does, so (D, D) is the only equilibrium, with payoffs (1, 1). The profile (C, C) gives both players more, but it is not an equilibrium: each player gains 2 by switching to D. An equilibrium need not be [Pareto optimal](/pareto-optimality/).

**Matching pennies.** The row player wins 1 if the coins match and loses 1 if not. No pure profile is an equilibrium: in each of the four cells one player gains by a switch. The unique equilibrium is $(1/2, 1/2)$ for both, with value 0. It is the maximin pair of the [minimax theorem](/minimax-theorem/); in a [zero-sum game](/zero-sum-game/), equilibria and pairs of optimal strategies are the same thing.

**Battle of the sexes.** The two players want to meet, but the row player prefers the opera (O) and the column player football (F).

| | O | F |
| --- | --- | --- |
| O | 2, 1 | 0, 0 |
| F | 0, 0 | 1, 2 |

There are three equilibria: (O, O) with payoffs (2, 1), (F, F) with (1, 2), and a mixed one. In the mixed one the column player must make the row player indifferent: $2q = 1 - q$ for the probability $q$ of O, so $q = 1/3$. In the same way the row player plays O with $p = 2/3$. Both players get $2/3$, less than in either pure equilibrium. So equilibria are not unique and do not have the same payoffs, unlike in zero-sum games.

**Game of chicken and correlated equilibrium.** Each driver can dare (D) or chicken out (C).

| | D | C |
| --- | --- | --- |
| D | 0, 0 | 7, 2 |
| C | 2, 7 | 6, 6 |

The equilibria are (D, C), (C, D) and the mixed profile where each player dares with probability $1/3$, which gives each $14/3$. Now let a referee draw one of (C, C), (D, C) and (C, D) with probability $1/3$ each and tell each player only their own part. A player told D knows the other was told C, and D gives 7 against 6. A player told C knows the other has C or D with probability $1/2$ each, and C gives $(6 + 2)/2 = 4$ against $(7 + 0)/2 = 3.5$ for D. Nobody wants to disobey, so this is a *correlated equilibrium* (Aumann 1974), and each player gets 5. The payoff pair (5, 5) has sum 10, more than any mix of the Nash payoffs, whose sums are 9, 9 and $28/3$.

**An $\varepsilon$-equilibrium far from every equilibrium.** Let the row player choose T with payoff 1 or B with payoff $1 + \varepsilon$, and let the column player have one strategy. Playing T is an $\varepsilon$-equilibrium, but the only equilibrium plays B. So a small deviation gain does not mean that the profile is near an equilibrium.

**A non-example: a maximin profile in a general-sum game.** In the battle of the sexes, the row player can guarantee $2/3$ by playing O with probability $1/3$, and the column player can guarantee $2/3$ by playing O with probability $2/3$. If both play these safe strategies, they meet at the opera with probability $2/9$ and at football with probability $2/9$, so the row player gets $2/9 \cdot 2 + 2/9 \cdot 1 = 2/3$. Against the column player's mix, the row player could get $2 \cdot 2/3 = 4/3$ by playing O for sure. In general-sum games, safe strategies need not form an equilibrium.

## Related definitions

- **Strict equilibrium.** Every deviation loses strictly. A strict equilibrium is pure, and it stays an equilibrium under small changes of the payoffs.
- **Dominant strategy equilibrium.** Each player's strategy is a best response to every profile of the others, as D in the prisoner's dilemma. It is a Nash equilibrium, but most games have none.
- **Correlated and coarse correlated equilibrium.** A distribution on $S$ from which no player wants to deviate after hearing their own part (correlated), or before hearing it (coarse correlated). Every Nash equilibrium is a correlated equilibrium, and the set of correlated equilibria is a polytope given by linear inequalities. No-regret learners converge to these sets, not to Nash equilibria ([regret](/regret/)).
- **Subgame perfect equilibrium.** In a game tree, an equilibrium that is also an equilibrium of every subgame. In a finite game of [perfect information](/perfect-information-game/), backward induction gives a pure one.
- **Equilibria of stochastic games.** In Shapley's [Markov games](/markov-game/) a stationary strategy profile is an equilibrium if no player gains by a change at any state.
- **Existence and computation.** Existence is [Nash's theorem](/nash-existence-theorem/); the complexity of finding one is on [Nash equilibrium computation](/nash-equilibrium-computation/), with the class [PPAD](/ppad/).

## References
