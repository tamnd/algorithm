---
tag: 5T10ZF
kind: definition
slug: bayesian-game
name: Bayesian game
aliases:
- game of incomplete information
- Harsanyi game
area: algorithmic-game-theory/strategic-games
level: core
summary: A game in which each player has a private type drawn from a common prior, and payoffs depend on the types and the actions.
prereqs: [normal-form-game, conditional-probability]
see_also: [bayes-nash-equilibrium, independent-private-values, common-value-auction, first-price-auction-equilibrium, bayesian-incentive-compatibility, revelation-principle, extensive-form-game, information-set]
sources:
  - paper: doi:10.1287/mnsc.14.3.159
    title: "John C. Harsanyi, Games with incomplete information played by Bayesian players, I-III. Part I. The basic model, Management Science 14(3) (1967), 159-182"
    locator: types, the common prior, and the transformation of a game of incomplete information into a game of imperfect information with a chance move
  - paper: doi:10.1287/mnsc.14.5.320
    title: "John C. Harsanyi, Games with incomplete information played by Bayesian players, Part II. Bayesian equilibrium points, Management Science 14(5) (1968), 320-334"
    locator: the equilibrium points of the Bayesian game
  - paper: doi:10.1287/mnsc.14.7.486
    title: "John C. Harsanyi, Games with incomplete information played by Bayesian players, Part III. The basic probability distribution of the game, Management Science 14(7) (1968), 486-502"
    locator: consistency of the players' beliefs with one common prior
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 2 (Bayesian games, strategic games with imperfect information)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 6 (Bayesian games and their equivalent forms)
---

A Bayesian game is a game in which each player has private information, called the player's type, and the types are drawn from a probability distribution, the common prior, that all players know. A player's payoff depends on the actions of all players and on the types. Harsanyi (1967, 1968) introduced the model to handle games in which players do not know each other's payoffs: he replaced the unknown parts of the game by a chance move that draws the types, which turns incomplete information into imperfect information about a move of chance. Auctions, where each bidder knows only their own value, are the main example in algorithmic game theory; the solution concept is the [Bayes-Nash equilibrium](/bayes-nash-equilibrium/).

## Definition

A finite *Bayesian game* has

- a finite set of players $N = \{1, \ldots, n\}$;
- for each player $i$, a finite set $S_i$ of actions;
- for each player $i$, a finite set $T_i$ of types, with $T = T_1 \times \cdots \times T_n$;
- a *common prior*, a probability distribution $p$ on $T$; we assume that every type has positive marginal probability $p(t_i) > 0$;
- for each player $i$, a payoff function $u_i : S \times T \to \mathbb{R}$, where $S = S_1 \times \cdots \times S_n$, which the player maximizes in expectation.

The timing is: chance draws $t \sim p$; each player $i$ learns $t_i$ and nothing else; the players choose actions at the same time; player $i$ gets $u_i(s, t)$. All parts of the game, including $p$, are common knowledge.

**Beliefs.** A player of type $t_i$ holds the *interim belief*

$$p(t_{-i} \mid t_i) = \frac{p(t_i, t_{-i})}{p(t_i)}$$

about the types of the others, by the rule of [conditional probability](/conditional-probability/). The types are *independent* if $p = p_1 \times \cdots \times p_n$; then $p(t_{-i} \mid t_i) = \prod_{j \ne i} p_j(t_j)$ does not depend on $t_i$. Otherwise the types are *correlated*. Say which case a result needs: much of auction and mechanism design theory assumes independence.

**Strategies.** A strategy of player $i$ is a map $\sigma_i : T_i \to \Delta(S_i)$, one mixed action for each type. A pure strategy is a map $T_i \to S_i$, so player $i$ has $|S_i|^{|T_i|}$ pure strategies. The *interim* expected payoff of type $t_i$ from action $s_i$ against $\sigma_{-i}$ is

$$U_i(s_i, \sigma_{-i} \mid t_i) = \sum_{t_{-i}} p(t_{-i} \mid t_i) \sum_{s_{-i}} \Big(\prod_{j \ne i} \sigma_j(t_j)(s_{j})\Big) u_i(s_i, s_{-i}, t_i, t_{-i}),$$

and the *ex ante* payoff of a strategy is the average of the interim payoffs over $t_i \sim p$. The three stages, *ex ante* (before the types), *interim* (each player knows their own type) and *ex post* (all types known), recur in the definitions of mechanism design, for example in individual rationality.

**Values.** The game has *private values* if each $u_i$ depends on $t$ only through $t_i$, as in the [independent private values](/independent-private-values/) model of auctions. Otherwise it has *interdependent values*, as in a [common-value auction](/common-value-auction/), where the value of the object to one bidder depends on the information of the others.

**The Harsanyi transformation.** The Bayesian game is the [extensive-form game](/extensive-form-game/) in which chance first draws $t$ with probability $p(t)$, and then each player moves once without seeing the other moves. The [information sets](/information-set/) of player $i$ are the sets of nodes with the same own type $t_i$. A behavior strategy of this tree is a map $T_i \to \Delta(S_i)$, so the strategies are the same as above, and the tree has perfect recall. An equivalent normal form, the *agent form*, has one player for each pair $(i, t_i)$, with the interim payoff above; its Nash equilibria are the Bayes-Nash equilibria.

**Size.** The game is given by $p$, with $|T|$ numbers, and the payoffs, with $n |S| |T|$ numbers. With independent types, $p$ needs only $\sum_i |T_i|$ numbers.

**Infinite types.** In auction models, types are often values in an interval with a density, such as $t_i \sim U[0, 1]$. Then the sums become integrals, and statements about "every type" hold for almost every type.

## Examples and non-examples

**A meeting with an unknown partner.** Player 1 and player 2 want to go to a concert, of Bach (B) or Stravinsky (S). Player 2 is of type *meet* or type *avoid*, with probability $1/2$ each, and only player 2 knows the type; player 1 has one type. With type meet, the payoffs are $(2, 1)$ at (B, B), $(1, 2)$ at (S, S) and $(0, 0)$ otherwise. With type avoid, they are $(2, 0)$ at (B, B), $(0, 2)$ at (B, S), $(0, 1)$ at (S, B) and $(1, 0)$ at (S, S). Player 1 has 2 pure strategies, player 2 has $2^2 = 4$: B or S for each type. The pure strategy "B if meet, S if avoid" of player 2 against B of player 1 gives player 1 the payoff $\tfrac12 \cdot 2 + \tfrac12 \cdot 0 = 1$. The equilibria of this game are on [Bayes-Nash equilibrium](/bayes-nash-equilibrium/).

**A first-price auction.** Two bidders have values $v_1, v_2$ drawn independently from $U[0, 1]$; the value is the type. Each bids $b_i \ge 0$, the higher bid wins, and the winner pays their bid, so $u_i = v_i - b_i$ for the winner and 0 for the loser. The types are independent and the values are private. The equilibrium bid is $b(v) = v/2$ ([first-price auction equilibrium](/first-price-auction-equilibrium/)).

**A Cournot duopoly with an unknown cost.** Firm 1 has the unit cost $c$, known to all. Firm 2 has the cost $c_L$ or $c_H$ and knows which. Both choose quantities, and the price is $a - q_1 - q_2$. Firm 2's type changes only its own payoff, so this is a game with private values and one-sided incomplete information.

**A game with no uncertainty.** If every $T_i$ has one element, the Bayesian game is an ordinary [normal-form game](/normal-form-game/).

**Non-example: beliefs with no common prior.** If player 1 thinks the type of player 2 is meet with probability $1/2$, while player 2 thinks that player 1 thinks it is meet with probability $3/4$, the beliefs of the players are inconsistent: they do not come from one prior by conditioning. Harsanyi's Part III studies when beliefs are consistent. Models without a common prior exist, but the standard Bayesian game and its equilibrium need one.

**Non-example: a game of imperfect information about actions only.** In matching pennies played in a tree where player 2 does not see the first move, nobody has private information about payoffs. It is an [extensive-form game](/extensive-form-game/) with imperfect information but not, in the sense used here, a game of incomplete information.

## Related definitions

- **Bayes-Nash equilibrium.** A profile of strategies in which every type of every player best responds in expectation, under the interim belief ([Bayes-Nash equilibrium](/bayes-nash-equilibrium/)).
- **Mechanism design.** A mechanism is a Bayesian game whose rules a designer chooses. It is [Bayesian incentive compatible](/bayesian-incentive-compatibility/) if truth telling is a Bayes-Nash equilibrium, and by the [revelation principle](/revelation-principle/) any Bayes-Nash outcome can be reached by such a direct mechanism.
- **Type spaces.** Mertens and Zamir (1985) showed that a general hierarchy of beliefs (beliefs about types, beliefs about beliefs, and so on) can be put into a universal type space, so the type model loses no generality.
- **Correlated types.** With correlated types, Crémer and McLean showed ([Crémer-McLean theorem](/cremer-mclean-theorem/)) that a seller can extract the full surplus in some auction settings, which is not possible with independent types.

## References
