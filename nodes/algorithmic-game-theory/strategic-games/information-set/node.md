---
tag: ZVET4T
kind: definition
slug: information-set
name: Information set
aliases:
- information partition
area: algorithmic-game-theory/strategic-games
level: core
summary: A set of decision nodes of one player in an extensive-form game that the player cannot distinguish, so the same action must be taken at all of them.
prereqs: [extensive-form-game]
see_also: [perfect-recall, kuhn-theorem-behavioral-strategies, imperfect-information-game, counterfactual-regret-minimization, sequence-form, bayesian-game, conditional-probability, subgame-perfect-equilibrium]
sources:
  - book: "H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games, Volume II, Annals of Mathematics Studies 28, Princeton University Press, 1953"
    title: "Harold W. Kuhn, Extensive games and the problem of information"
    locator: pp. 193 to 216 (information sets as a partition of the moves of each player, and the condition that all moves of one set have the same alternatives)
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 11 (extensive games with imperfect information, the information partition of each player)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 5 (imperfect-information extensive-form games and their information sets)
---

An information set is a set of decision nodes of one player in an [extensive-form game](/extensive-form-game/) that the player cannot tell apart when it is their turn to move. The player knows that the play is at one of these nodes but not at which one, so a strategy must choose the same action, or the same distribution over actions, at all of them. The information sets of a player form a partition of that player's decision nodes, called the player's information partition. Information sets are how the extensive form models hidden cards, hidden earlier moves and moves made at the same time; the game-playing side of this topic is on [imperfect-information games](/imperfect-information-game/).

## Definition

Let $\Gamma$ be a finite extensive-form game with players $N$, and let $H_i$ be the set of inner nodes $h$ at which player $i$ moves, $P(h) = i$. An *information partition* of player $i$ is a partition $\mathcal{I}_i$ of $H_i$ into sets, the *information sets* of $i$, with this condition:

- if $h$ and $h'$ are in the same set $I$, then $A(h) = A(h')$.

The common action set is written $A(I)$. The condition is needed because a player who sees which actions are available could use them to tell the nodes apart. Chance nodes belong to no information set.

When the play reaches a node $h \in I$, player $i$ is told $I$ and nothing more. So a pure strategy of player $i$ is a map $s_i$ with $s_i(I) \in A(I)$ for each $I \in \mathcal{I}_i$, and a behavior strategy gives a distribution $b_i(I) \in \Delta(A(I))$ for each $I$. A strategy that chose differently at two nodes of one set would use information the player does not have.

Many texts add a second condition: no path from the root meets an information set twice. Without it, a player can be at a node and later at its own descendant without knowing which of the two it is. The absent-minded driver of [perfect recall](/perfect-recall/) shows what goes wrong in that case. The stronger condition of perfect recall implies this one.

**Beliefs.** Fix a behavior profile $b$ and an information set $I$ with $P_b(I) = \sum_{h \in I} P_b(h) > 0$, where $P_b(h)$ is the probability that the play passes through $h$. By the rule of [conditional probability](/conditional-probability/), the belief of the player at $I$ is

$$\mu(h \mid I) = \frac{P_b(h)}{P_b(I)}, \qquad h \in I,$$

and the expected payoff of an action $a \in A(I)$ is the average, with weights $\mu(h \mid I)$, of the expected payoff after $h a$. If $P_b(I) = 0$, the formula does not define a belief. Equilibrium refinements such as [trembling-hand perfection](/trembling-hand-perfect-equilibrium/) exist mainly to fix what happens at such sets.

## Examples and non-examples

**Perfect information.** In chess, both players see every move, so every information set has one node. A strategy chooses a move at each position, and the game is a [perfect-information game](/perfect-information-game/).

**A simultaneous move.** In matching pennies written as a tree, player 1 moves first and player 2 then moves at one of two nodes, after Heads or after Tails. Both nodes are in one information set $\{H, T\}$ of player 2. So player 2 has two pure strategies, Heads and Tails, as in the simultaneous game, and not the four strategies that a player who saw the coin would have.

**Hidden cards.** In Kuhn poker (described on [imperfect-information games](/imperfect-information-game/)), three cards J, Q, K are dealt, one to each player. When player 2 holds K and player 1 bets, player 2 is at one of two nodes, after the deals (J, K) and (Q, K), and these form one information set. Each player has 6 information sets: 3 possible cards, and 2 points of decision for each card. With two actions at each set, each player has $2^6 = 64$ pure strategies.

**A belief computed from reach probabilities.** In the hidden-card set above, if player 1 bets with J with probability $1/3$ and always bets with Q, the two deals are equally likely, and player 2 has seen a bet, then $\mu(\text{J} \mid I) = (1/2 \cdot 1/3)/(1/2 \cdot 1/3 + 1/2 \cdot 1) = 1/4$ and $\mu(\text{Q} \mid I) = 3/4$.

**Non-example: different actions.** A set that holds a node with the actions $\{\text{bet}, \text{check}\}$ and a node with the actions $\{\text{call}, \text{fold}\}$ is not an information set: the player would know which node it is from the menu.

**Non-example: two players.** A set that holds nodes of two players is not an information set. The partition is made separately for each player.

**Non-example: a chance node.** Chance has no information sets. Its moves have fixed probabilities that do not depend on what anyone knows.

## Related definitions

- **Perfect recall.** A player has [perfect recall](/perfect-recall/) if two nodes in one information set have the same sequence of the player's own earlier information sets and actions. With perfect recall, [Kuhn's theorem](/kuhn-theorem-behavioral-strategies/) lets behavior strategies replace mixed strategies.
- **Sequences.** With perfect recall, each information set $I$ of player $i$ has a unique sequence $\mathrm{seq}(I)$ of the player's own actions that leads to it. The [sequence form](/sequence-form/) uses these sequences as variables.
- **Information sets in learning.** [Counterfactual regret minimization](/counterfactual-regret-minimization/) keeps one regret table for each information set, weighted by the reach probability of the opponents and of chance.
- **Types in a Bayesian game.** In a [Bayesian game](/bayesian-game/) written as a tree, chance first draws the types, and each player's information sets are the sets of nodes with the same own type.
- **Subgames.** A [subgame](/subgame-perfect-equilibrium/) must start at a node that is alone in its information set and must not cut any information set.
- **Knowledge partitions.** In Aumann's model of knowledge, each player has a partition of a set of states of the world, and the player knows the cell that holds the true state. The information sets of a game are the same idea applied to the nodes of a tree.

## References
