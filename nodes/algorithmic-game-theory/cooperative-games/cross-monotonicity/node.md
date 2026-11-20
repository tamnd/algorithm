---
tag: 1BKTYH
kind: definition
slug: cross-monotonicity
name: Cross-monotonic cost sharing
aliases:
- population monotonic cost sharing
area: algorithmic-game-theory/cooperative-games
level: advanced
summary: A cost-sharing method in which no agent's share rises when more agents are served. A budget-balanced cross-monotonic method gives core allocations.
prereqs: [cost-sharing-mechanism, core-of-a-cooperative-game]
see_also: [moulin-mechanism, convex-game, submodular-function, shapley-value, airport-game, bird-rule, jain-vazirani-steiner-cost-sharing, least-core]
sources:
  - paper: "Yves Sprumont, Population monotonic allocation schemes for cooperative games with transferable utility, Games and Economic Behavior 2(4) (1990), 378-394"
    title: Population monotonic allocation schemes for cooperative games with transferable utility
    locator: the definition of a population monotonic allocation scheme, its relation to the core of every subgame, and the existence of such schemes for convex games
  - paper: "Herve Moulin, Incremental cost sharing: characterization by coalition strategy-proofness, Social Choice and Welfare 16(2) (1999), 279-320"
    title: "Incremental cost sharing: characterization by coalition strategy-proofness"
    locator: cross-monotonic cost-sharing methods and the group strategyproof mechanisms built from them
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 15 (Kamal Jain and Mohammad Mahdian, Cost Sharing), Section 15.3 on cross-monotonic cost-sharing methods
  - paper: "Nicole Immorlica, Mohammad Mahdian and Vahab S. Mirrokni, Limitations of cross-monotonic cost-sharing schemes, ACM Transactions on Algorithms 4 (2008), Article 24"
    title: Limitations of cross-monotonic cost-sharing schemes
    locator: upper bounds on the budget balance that cross-monotonic methods can reach for several optimization problems
---

Cross-monotonicity is the condition that a cost share never rises when more players are served. It is the key property of a cost-sharing method: with it, the [Moulin mechanism](/moulin-mechanism/) is group strategyproof, and a budget balanced method gives an allocation in the core of every subgame. In cooperative game theory the same idea, for profits, is a population monotonic allocation scheme (Sprumont 1990).

## Definition

Let $A$ be a finite set of players and $C : 2^A \to \mathbb{R}_{\ge 0}$ a cost function with $C(\emptyset) = 0$. A [cost-sharing method](/cost-sharing-mechanism/) $\xi$ gives a share $\xi(i, S) \ge 0$ to each player $i$ of each nonempty set $S \subseteq A$.

The method is **cross-monotonic** if for all sets $S \subseteq T \subseteq A$ and every $i \in S$,

$$\xi(i, S) \ge \xi(i, T).$$

It is **$\beta$-budget balanced** if $C(S) \le \sum_{i \in S} \xi(i, S) \le \beta\, C(S)$ for every nonempty $S$, and **budget balanced** if $\beta = 1$.

For a profit game $(N, v)$, a **population monotonic allocation scheme** (PMAS) is a family of vectors $(x_{S, i})_{i \in S}$, one for each nonempty $S \subseteq N$, with $\sum_{i \in S} x_{S, i} = v(S)$ and $x_{S, i} \le x_{T, i}$ whenever $i \in S \subseteq T$. Each player's payoff can only rise when the coalition grows. A budget balanced cross-monotonic method is exactly a PMAS of the cost game, with the inequality reversed because costs replace profits.

**Proposition.** If $\xi$ is cross-monotonic and budget balanced, then for every nonempty $T \subseteq A$ the vector $(\xi(i, T))_{i \in T}$ is in the [core](/core-of-a-cooperative-game/) of the cost game restricted to $T$.

*Proof.* The shares sum to $C(T)$. For a nonempty $S \subseteq T$, cross-monotonicity and budget balance give $\sum_{i \in S} \xi(i, T) \le \sum_{i \in S} \xi(i, S) = C(S)$. So no coalition inside $T$ pays more than its own cost. $\square$

The same argument for a $\beta$-budget balanced method shows that the shares of $T$ divided by $\beta$ charge no coalition $S \subseteq T$ more than $C(S)$, and cover at least $C(T)/\beta$. So the scaled shares are in an approximate core.

The proposition shows that a budget balanced cross-monotonic method needs a nonempty core in every subgame. So the game must be totally balanced, which is a strong condition.

## Examples and non-examples

- **Equal split of a fixed cost.** If $C(S) = 1$ for every nonempty $S$, then $\xi(i, S) = 1/|S|$ is cross-monotonic and budget balanced.
- **Submodular costs.** If $C$ is [submodular](/submodular-function/), the cost game is concave, and the [Shapley value](/shapley-value/) of the game restricted to $S$ is a cross-monotonic, budget balanced method. In profit form, Sprumont (1990) showed that every [convex game](/convex-game/) has a PMAS. The [airport game](/airport-game/) is an example: each segment of the runway is split equally among the players that need it, and a segment is shared by more players when the set grows.
- **Not cross-monotonic: Bird's rule.** In a minimum cost spanning tree game with $c(0, 1) = 8$, $c(0, 2) = 9$, $c(0, 3) = 7$, $c(1, 2) = 1$, $c(1, 3) = 8$ and $c(2, 3) = 4$, [Bird's rule](/bird-rule/) charges player 2 the amount 1 in $\{1, 2\}$ and 4 in $\{1, 2, 3\}$. Its shares are budget balanced and in the core of each subgame, but player 2's share rises when player 3 joins.
- **A nonempty core is not enough.** Let $C(\{1\}) = C(\{2\}) = 1$, $C(\{3\}) = 10$, $C(\{1, 2\}) = 3$, $C(\{1, 3\}) = C(\{2, 3\}) = 11$ and $C(\{1, 2, 3\}) = 3$. The vector $(1, 1, 1)$ is in the core of the whole game. But the subgame on $\{1, 2\}$ has an empty core, since $C(\{1, 2\}) > C(\{1\}) + C(\{2\})$. So no budget balanced method is cross-monotonic for this game.
- **Steiner trees.** For Steiner tree costs exact budget balance is NP-hard, and the core of a subgame can be empty. [Jain-Vazirani cost sharing](/jain-vazirani-steiner-cost-sharing/) is cross-monotonic and 2-budget balanced. Immorlica, Mahdian and Mirrokni (2008) showed that for some problems no cross-monotonic method can reach a budget balance factor close to 1.

## Related definitions

- **Group strategyproofness.** The Moulin mechanism built on a cross-monotonic method is group strategyproof, so no coalition of players can lie in a way that helps one member and hurts none.
- **Core.** Cross-monotonicity with budget balance gives a core allocation for every subgame, not only for the whole set of players.
- **[Least core](/least-core/).** When the core is empty, the least core relaxes the core inequalities; a $\beta$-budget balanced cross-monotonic method gives a different relaxation, by a factor instead of an additive amount.
- **Cost monotonicity.** A different condition on allocation rules: a player's share does not fall when one of its costs rises. The folk rule of minimum cost spanning tree games has both properties.

## References
