---
tag: 566A6K
kind: definition
slug: bayes-nash-equilibrium
name: Bayes-Nash equilibrium
aliases:
- Bayesian Nash equilibrium
- BNE
area: algorithmic-game-theory/strategic-games
level: core
summary: A profile of maps from types to strategies in which each type of each player best responds in expectation over the types of the others.
prereqs: [bayesian-game, nash-equilibrium]
see_also: [first-price-auction-equilibrium, bayesian-incentive-compatibility, revelation-principle, independent-private-values, vickrey-auction, dominant-strategy, nash-existence-theorem, np-complete]
sources:
  - paper: doi:10.1287/mnsc.14.5.320
    title: "John C. Harsanyi, Games with incomplete information played by Bayesian players, Part II. Bayesian equilibrium points, Management Science 14(5) (1968), 320-334"
    locator: the definition of a Bayesian equilibrium point and its relation to the equilibria of the game with a chance move
  - paper: doi:10.1287/mnsc.14.3.159
    title: "John C. Harsanyi, Games with incomplete information played by Bayesian players, I-III. Part I. The basic model, Management Science 14(3) (1967), 159-182"
    locator: types, the common prior and the Harsanyi transformation
  - paper: doi:10.1016/j.geb.2008.02.015
    title: "Vincent Conitzer and Tuomas Sandholm, New complexity results about Nash equilibria, Games and Economic Behavior 63(2) (2008), 621-641"
    locator: Section 4, Theorem 2 (deciding whether a pure-strategy Bayes-Nash equilibrium exists is NP-complete, even in symmetric two-player games)
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 2 (Bayesian games and their Nash equilibria)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 6 (Bayes-Nash equilibrium, ex post equilibrium)
---

A Bayes-Nash equilibrium of a [Bayesian game](/bayesian-game/) is a profile that gives each player a strategy for each of their types, such that every type of every player plays a best response, in expectation over the types of the others, to the strategies of the others. It is the [Nash equilibrium](/nash-equilibrium/) of the game in which chance first draws the types (Harsanyi 1968). Every finite Bayesian game has one in mixed strategies. It is the equilibrium notion behind the analysis of auctions, for example the bid $b(v) = v/2$ in the two-bidder [first-price auction](/first-price-auction-equilibrium/), and behind [Bayesian incentive compatibility](/bayesian-incentive-compatibility/) in mechanism design.

## Definition

Let $G$ be a finite Bayesian game with players $N$, actions $S_i$, types $T_i$, a common prior $p$ on $T = T_1 \times \cdots \times T_n$ and payoffs $u_i(s, t)$. A strategy of player $i$ is a map $\sigma_i : T_i \to \Delta(S_i)$. For a type $t_i$ with $p(t_i) > 0$, the interim payoff of the action $s_i$ against $\sigma_{-i}$ is

$$U_i(s_i, \sigma_{-i} \mid t_i) = \sum_{t_{-i}} p(t_{-i} \mid t_i)\, \mathbb{E}_{s_{-i} \sim \sigma_{-i}(t_{-i})}\big[u_i(s_i, s_{-i}, t_i, t_{-i})\big],$$

where $\sigma_{-i}(t_{-i})$ draws the actions of the others independently, each from $\sigma_j(t_j)$.

**Definition.** A profile $\sigma$ is a *Bayes-Nash equilibrium* if for every player $i$, every type $t_i$ with $p(t_i) > 0$ and every action $s_i \in S_i$,

$$U_i(\sigma_i(t_i), \sigma_{-i} \mid t_i) \ge U_i(s_i, \sigma_{-i} \mid t_i).$$

This is the *interim* form: each type is checked separately, after it knows itself. As for Nash equilibrium, a mixed action is a best response if and only if every action in its support is one, so it is enough to check pure deviations, and to check that every action that $\sigma_i(t_i)$ plays with positive probability reaches the maximum of $U_i(\cdot, \sigma_{-i} \mid t_i)$. This needs $\sum_i |T_i| \cdot |S_i|$ interim payoffs, so a claimed equilibrium is easy to check exactly.

**The ex ante form.** The ex ante payoff of $\sigma_i$ is $\sum_{t_i} p(t_i)\, U_i(\sigma_i(t_i), \sigma_{-i} \mid t_i)$. Since every type with $p(t_i) > 0$ has positive weight and can change its action alone, $\sigma$ is a Bayes-Nash equilibrium if and only if no player can raise their ex ante payoff by a change of strategy. So a Bayes-Nash equilibrium is exactly a Nash equilibrium of the normal form of the Harsanyi tree, in which a pure strategy is a map $T_i \to S_i$. It is also a Nash equilibrium of the agent form, with one player for each pair $(i, t_i)$.

**Existence.** The agent form is a finite normal-form game, so by [Nash's theorem](/nash-existence-theorem/) it has a mixed equilibrium, and every finite Bayesian game has a Bayes-Nash equilibrium. A pure one may not exist, already when every $T_i$ has one element (matching pennies).

**Continuous types.** When the types have densities, as in auctions with values in $[0, 1]$, the condition is asked for almost every type $t_i$, since a single type has probability 0. Existence then needs extra conditions on the payoffs, and the equilibria are usually found by solving a differential equation for a monotone bid function.

**Stronger notions.**

- An *ex post equilibrium* asks that $\sigma_i(t_i)$ be a best response to $\sigma_{-i}(t_{-i})$ for every profile $t$ of types, so no player would regret their action after learning all types. It does not depend on the prior.
- A *dominant strategy equilibrium* asks that $\sigma_i(t_i)$ be a best response to every action profile of the others, for every type ([dominant strategy](/dominant-strategy/)).

Each notion implies the next: dominant strategy, then ex post, then Bayes-Nash.

## Examples and non-examples

**A meeting with an unknown partner.** This is the game on [Bayesian game](/bayesian-game/). Player 1 chooses B or S. Player 2 is of type meet or avoid, with probability $1/2$ each. With type meet, the payoffs are $(2, 1)$ at (B, B), $(1, 2)$ at (S, S) and $(0, 0)$ otherwise. With type avoid, they are $(2, 0)$ at (B, B), $(0, 2)$ at (B, S), $(0, 1)$ at (S, B) and $(1, 0)$ at (S, S). Let player 1 play B with probability $p$, and let type meet and type avoid play B with probabilities $q_m$ and $q_a$.

- Type meet gets $p$ from B and $2(1 - p)$ from S, so it plays B if $p > 2/3$ and S if $p < 2/3$.
- Type avoid gets $1 - p$ from B and $2p$ from S, so it plays B if $p < 1/3$ and S if $p > 1/3$.
- Player 1 gets $\tfrac12 (2 q_m) + \tfrac12 (2 q_a) = q_m + q_a$ from B and $\tfrac12 (1 - q_m) + \tfrac12 (1 - q_a)$ from S, so B is better if $q_m + q_a > 2/3$.

Go through the cases for $p$. If $p > 2/3$, then $q_m = 1$ and $q_a = 0$, the sum is $1 > 2/3$, and so $p = 1$. If $p = 2/3$, then $q_a = 0$ and player 1 must be indifferent, so $q_m = 2/3$. If $1/3 < p < 2/3$, both types play S, so player 1 plays S, which contradicts $p > 1/3$. If $p = 1/3$, then $q_m = 0$ and $q_a = 2/3$. If $p < 1/3$, then $q_m = 0$ and $q_a = 1$, the sum is 1, and player 1 plays B, a contradiction. So there are exactly three Bayes-Nash equilibria:

| player 1 | type meet | type avoid | payoff of player 1 |
| --- | --- | --- | --- |
| B | B | S | 1 |
| B with $2/3$ | B with $2/3$ | S | $2/3$ |
| B with $1/3$ | S | B with $2/3$ | $2/3$ |

In the first one, check the payoffs directly: player 1 gets 1 from B and $1/2$ from S; type meet gets 1 from B and 0 from S; type avoid gets 0 from B and 2 from S.

**Not an ex post equilibrium.** In the first equilibrium, when player 2 is of type avoid, the outcome is (B, S) and player 1 gets 0, while S would give player 1 the payoff 1 against S. So player 1 would regret B after learning the type. The profile is a Bayes-Nash equilibrium but not an ex post equilibrium.

**Non-example: best responses type by type, but not for the uninformed player.** In the profile where player 1 plays S, type meet plays S and type avoid plays B, both types of player 2 best respond to S. But player 1 gets $\tfrac12 \cdot 1 + \tfrac12 \cdot 0 = 1/2$ from S and $\tfrac12 \cdot 0 + \tfrac12 \cdot 2 = 1$ from B, so it is not an equilibrium.

**The first-price auction.** Two bidders have independent values $v_i \sim U[0, 1]$, the higher bid wins and pays its bid. Suppose bidder 2 bids $v_2/2$. A bid $b \in [0, 1/2]$ of bidder 1 wins when $v_2 < 2b$, with probability $2b$, and gives the expected utility $(v_1 - b) \cdot 2b$. Its derivative $2v_1 - 4b$ is 0 at $b = v_1/2$, and bids above $1/2$ win for sure at a higher price. So $b(v) = v/2$ is a symmetric Bayes-Nash equilibrium, and with $n$ bidders the equilibrium bid is $(n - 1)v/n$ ([first-price auction equilibrium](/first-price-auction-equilibrium/)).

**The second-price auction.** In the [Vickrey auction](/vickrey-auction/), bidding the true value is a dominant strategy, so truth telling is a dominant strategy equilibrium and therefore also ex post and Bayes-Nash. It also has other Bayes-Nash equilibria, for example one bidder bids 1 and the others bid 0, whatever the values.

## Related definitions

- **Bayesian incentive compatibility.** A direct mechanism is [Bayesian incentive compatible](/bayesian-incentive-compatibility/) if truth telling is a Bayes-Nash equilibrium. By the [revelation principle](/revelation-principle/), any outcome of a Bayes-Nash equilibrium of any mechanism is also the truthful outcome of such a direct mechanism.
- **Independent private values.** In the [independent private values](/independent-private-values/) model, the interim belief of a bidder does not depend on their own value, which makes the equilibrium analysis of auctions tractable.
- **Computation.** A finite Bayesian game is a finite normal-form game in its agent form, so the methods and the complexity of [Nash equilibrium computation](/nash-equilibrium-computation/) apply. Deciding whether a *pure* Bayes-Nash equilibrium exists is [NP-complete](/np-complete/), even for symmetric two-player Bayesian games (Conitzer and Sandholm 2008), while for a normal-form game given by its table the same question is answered by checking every cell.
- **Refinements.** In Bayesian games written as trees with several stages, such as signaling games, beliefs at unreached information sets matter, and refinements such as perfect Bayesian equilibrium are used.

## References
