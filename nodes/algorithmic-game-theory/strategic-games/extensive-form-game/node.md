---
tag: CHA01F
kind: definition
slug: extensive-form-game
name: Extensive-form game
aliases:
- extensive game
- game in extensive form
area: algorithmic-game-theory/strategic-games
level: core
summary: A game given by a tree of moves with chance nodes, payoffs at the leaves and information sets that group the nodes a player cannot tell apart.
prereqs: [game-tree, normal-form-game, mixed-strategy]
see_also: [information-set, perfect-recall, kuhn-theorem-behavioral-strategies, subgame-perfect-equilibrium, imperfect-information-game, perfect-information-game, sequence-form, bayesian-game]
sources:
  - book: "H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games, Volume II, Annals of Mathematics Studies 28, Princeton University Press, 1953"
    title: "Harold W. Kuhn, Extensive games and the problem of information"
    locator: pp. 193 to 216 (the general extensive game with chance moves and information sets, pure and behavior strategies)
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press, 1994
    locator: Chapter 6 (extensive games with perfect information) and Chapter 11 (extensive games with imperfect information)
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: the chapter on extensive-form games (game trees, information sets, strategies and the strategic form of a tree)
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 5 (games with sequential actions, the extensive form)
---

An extensive-form game is a game written as a rooted tree: each inner node is a move of one player or of chance, each leaf carries a payoff for every player, and the information sets group the nodes that a player cannot tell apart when it is their turn. It keeps the order of the moves and what each player knows at each move, which the [normal form](/normal-form-game/) forgets. This page gives the general model of game theory with any number of players and any payoffs; the [game tree](/game-tree/) page treats the search tree of two-player games in game-playing programs, and [imperfect-information games](/imperfect-information-game/) treats hidden information from the side of game-playing algorithms such as [counterfactual regret minimization](/counterfactual-regret-minimization/).

## Definition

A finite extensive-form game $\Gamma$ has these parts (Kuhn 1953).

- A finite set of players $N = \{1, \ldots, n\}$.
- A finite rooted tree. Its nodes are the histories $h$, the sequences of actions from the root, and its leaves are the terminal histories $z \in Z$. The edges out of an inner node $h$ are labelled with the actions $A(h)$, and each label appears once at $h$.
- A player function $P$ that gives each inner node either a player $P(h) \in N$ or chance, $P(h) = c$.
- For each chance node $h$, a fixed probability distribution $p_c(\cdot \mid h)$ on $A(h)$. All players know these probabilities.
- For each player $i$, a partition $\mathcal{I}_i$ of the nodes with $P(h) = i$ into [information sets](/information-set/). Two nodes in the same set $I$ have the same actions, written $A(I)$. When the play reaches a node of $I$, player $i$ knows that it is in $I$ and nothing more.
- For each player $i$, a payoff function $u_i : Z \to \mathbb{R}$, which the player maximizes in expectation.

The game has *perfect information* if every information set has one node. Then each player sees all earlier moves, as in chess, and the tree is a [perfect-information game](/perfect-information-game/).

**Strategies.** A *pure strategy* of player $i$ chooses an action at every information set of $i$: $s_i(I) \in A(I)$ for all $I \in \mathcal{I}_i$. It is a full plan, and it also names moves at information sets that the plan itself never reaches. The set of pure strategies is $S_i = \prod_{I \in \mathcal{I}_i} A(I)$. A *mixed strategy* $\sigma_i$ is a probability distribution on $S_i$, as on [mixed strategy](/mixed-strategy/). A *behavior strategy* $b_i$ gives a distribution $b_i(I) \in \Delta(A(I))$ at each information set, with independent draws at different sets.

**Outcomes and payoffs.** A profile of behavior strategies $b = (b_1, \ldots, b_n)$ reaches the leaf $z$ with the probability

$$P_b(z) = \prod_{h a \sqsubseteq z} \pi(h, a), \qquad \pi(h, a) = \begin{cases} p_c(a \mid h) & \text{if } P(h) = c, \\ b_i(I(h))(a) & \text{if } P(h) = i, \end{cases}$$

where the product runs over the edges $(h, a)$ on the path from the root to $z$ and $I(h)$ is the information set of $h$. A pure strategy is a behavior strategy with all its mass on one action at each set. A mixed profile $\sigma$ reaches $z$ with the probability $P_\sigma(z) = \sum_{s} \prod_i \sigma_i(s_i)\, P_s(z)$. The expected payoff of player $i$ is $u_i(\sigma) = \sum_{z \in Z} P_\sigma(z)\, u_i(z)$, and in the same way for $b$.

**The induced normal form.** The extensive game defines a normal-form game with the strategy sets $S_i$ and the payoffs $u_i(s) = \sum_z P_s(z) u_i(z)$. A [Nash equilibrium](/nash-equilibrium/) of $\Gamma$ is a Nash equilibrium of this game. Two pure strategies that differ only at information sets that both of them make unreachable give the same outcome against every profile of the others. If we merge them, we get the *reduced normal form*.

**Size.** The tree has $|Z|$ leaves and fewer than $|Z|$ inner nodes when every inner node has at least two actions. The normal form has $|S_i| = \prod_{I} |A(I)|$ strategies for player $i$, which is exponential in the number of information sets. A player with $k$ information sets and two actions at each has $2^k$ pure strategies. For this reason, algorithms for extensive games work on the tree. With [perfect recall](/perfect-recall/), [Kuhn's theorem](/kuhn-theorem-behavioral-strategies/) shows that behavior strategies, which need only $\sum_I |A(I)|$ numbers, lose nothing. The [sequence form](/sequence-form/) then gives a strategy representation of size linear in the tree.

## Examples and non-examples

**An entry game.** Player 1 chooses Out, which ends the game with payoffs $(0, 2)$, or In. After In, player 2 chooses Fight, with payoffs $(-1, -1)$, or Accommodate, with payoffs $(1, 1)$. Each player has one information set with one node, so the game has perfect information. The normal form is a 2 by 2 game with the pure equilibria (Out, Fight) and (In, Accommodate). Only the second is a [subgame perfect equilibrium](/subgame-perfect-equilibrium/), since Fight is a threat that player 2 would not carry out after In.

**Matching pennies as a tree.** Player 1 chooses Heads or Tails, then player 2 chooses Heads or Tails without seeing the first choice. The two nodes of player 2 form one information set, so player 2 has two pure strategies, not four. Player 1 gets 1 if the coins match and $-1$ if not. The tree gives the same normal form as the simultaneous game. So the extensive form can express moves made at the same time, by an information set that hides the earlier move.

**Counting strategies.** In a game where player 1 moves at the root with 2 actions and then moves again after each action, each time with 2 actions, player 1 has 3 information sets (one at the root and two singletons below it) and $2^3 = 8$ pure strategies. Each pure strategy reaches only one of the two lower nodes, so the reduced normal form has 4 strategies: the root action and one action at the node it leads to. A behavior strategy needs 3 numbers, one probability per binary choice.

**A chance move.** In a card game, chance deals a high or a low card to player 1 with probability $1/2$ each, player 1 sees the card and bets or folds, and player 2 sees the bet but not the card. The two nodes of player 2 after a bet form one information set. A game of this type in which chance picks the private information is also a [Bayesian game](/bayesian-game/) written as a tree (Harsanyi 1967).

**Non-example: a payoff that depends on a strategy.** An extensive game assigns payoffs to leaves, that is, to what happened. A game in which a player is paid for what they would have done at a node that was not reached cannot be written in this form.

**Non-example: an infinite game.** A game with infinitely long plays, such as a repeated game without a last round, or with a continuum of actions, such as a bid in $[0, 1]$, is not a finite extensive game. The definition extends to these cases, but Kuhn's results and the counting above are for finite trees.

## Related definitions

- **Information set and perfect recall.** The [information set](/information-set/) is the unit at which a player chooses. [Perfect recall](/perfect-recall/) is the condition that no player forgets their own earlier moves or what they knew; most algorithms need it.
- **Subgame.** The part of the tree below a node $h$ is a *subgame* if $h$ is alone in its information set and every information set that meets the part lies inside it. [Subgame perfection](/subgame-perfect-equilibrium/) and [trembling-hand perfection](/trembling-hand-perfect-equilibrium/) refine Nash equilibrium for extensive games.
- **Perfect-information game.** Every information set is a singleton. Backward induction then gives a pure equilibrium ([Zermelo's theorem](/zermelo-theorem/) for win, lose and draw games).
- **Stochastic game.** A game played over states with moves repeated at each state, not a finite tree ([stochastic game](/stochastic-game/), [Markov game](/markov-game/)).
- **Normal form.** Every finite normal-form game is an extensive game with one information set per player and no player seeing another player's move.

## References
