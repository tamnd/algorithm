---
tag: CPP7JC
kind: definition
slug: stochastic-game
name: Stochastic game
aliases:
- game with chance nodes
area: games-and-search/game-tree-search
level: advanced
summary: A game tree in which some nodes are random events with known probabilities, such as dice rolls, valued by the expected payoff under optimal play.
prereqs: [game-tree, perfect-information-game, expected-value]
see_also: [expectiminimax, markov-game, minimax-q, imperfect-information-game, zero-sum-game, markov-decision-process, zermelo-theorem, monte-carlo-tree-search]
sources:
  - book: "H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games, Volume II, Annals of Mathematics Studies 28, Princeton University Press, 1953"
    title: "Harold W. Kuhn, Extensive games and the problem of information"
    locator: pp. 193 to 216 (game trees with chance moves as moves of a chance player, and information sets)
  - paper: doi:10.1073/pnas.39.10.1095
    title: "L. S. Shapley, Stochastic games, Proceedings of the National Academy of Sciences 39(10) (1953), 1095-1100"
    locator: the other sense of the name, repeated matrix games with random transitions between states
  - paper: doi:10.1016/0890-5401(92)90048-K
    title: "Anne Condon, The complexity of stochastic games, Information and Computation 96(2) (1992), 203-224"
    locator: simple stochastic games, and the result that deciding whether the value exceeds 1/2 is in NP and coNP
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 5 (the section on stochastic games, chance nodes and expected values in backgammon)
---

In game-tree search, a stochastic game is a game tree that has chance nodes as well as the moves of the players. At a chance node nothing is chosen: a random event, such as a roll of dice, picks the next node with known probabilities, and all players see the result. The value of such a game is an expected payoff, and [expectiminimax](/expectiminimax/) computes it. The same name also means Shapley's stochastic games, which are a different model (see below).

## Definition

A **stochastic game tree** for two players, MAX and MIN, is a finite rooted tree with:

- a partition of the internal nodes into MAX nodes, MIN nodes and **chance nodes**;
- for every chance node $n$, a probability distribution $p_n$ on its children, with $p_n(c) \ge 0$ and $\sum_c p_n(c) = 1$;
- a payoff $u(\ell) \in \mathbb{R}$ to MAX at every leaf $\ell$. In the zero-sum case MIN gets $-u(\ell)$.

A play starts at the root. At a MAX or MIN node that player picks a child; at a chance node a child is drawn from $p_n$, independently of earlier draws. Both players know the tree, the probabilities and the whole history, so the game has *perfect information*. In the language of extensive games (Kuhn 1953), chance is an extra player who moves at random with fixed probabilities, and every information set is a single node.

A pure strategy of a player picks a child at each of that player's nodes. A pair $(\sigma, \tau)$ of strategies gives a probability distribution on the leaves, and $E(\sigma, \tau)$ is the expected payoff to MAX. The **value** of the game is

$$v = \max_\sigma \min_\tau E(\sigma, \tau) = \min_\tau \max_\sigma E(\sigma, \tau).$$

The two orders give the same number, and pure strategies reach it. This is the version of [Zermelo's theorem](/zermelo-theorem/) for games with chance, and the proof on the page [expectiminimax](/expectiminimax/) is backward induction: the value of a chance node is the average of the values of its children, weighted by $p_n$.

For games with more than two players or with general payoffs, the same backward induction with expectations at chance nodes gives a subgame perfect equilibrium in pure strategies.

## Examples and non-examples

- **A coin flip.** MAX may take a safe payoff of 1, or gamble. If MAX gambles, a fair coin is tossed. On heads MIN chooses between payoffs 3 and $-1$ and takes $-1$. On tails the payoff is 4. The gamble is worth $\tfrac12 \cdot (-1) + \tfrac12 \cdot 4 = 3/2$, so the value is $3/2$ and MAX gambles. A MAX who expected the worst at every chance node would value the gamble at $-1$ and play safe.
- **Backgammon.** Each turn starts with a roll of two dice, a chance node with 21 distinct outcomes: the 6 doubles with probability $1/36$ each and the 15 other rolls with $1/18$ each. Both players see the roll and the board. It is the standard example of this kind of game.
- **Dice games such as Pig,** where a player rolls a die again and again and may stop at any time to bank the points of the turn, but loses them on a roll of 1. All information is public.
- **Card games with open cards.** A card drawn from a shuffled deck and turned face up is a chance node. If it stays face down for one player, the game is not of this kind.
- **Non-example: poker.** The cards are dealt at random, but each player sees only their own cards. Players do not know which node they are at, so the game is an [imperfect-information game](/imperfect-information-game/). Expectiminimax does not apply, and the optimal strategies may need to be mixed.
- **Non-example: rock, paper, scissors.** The players move at the same time, so neither sees the other's move. There is no chance node, and yet the optimal strategy is random; this is a matrix game ([minimax theorem](/minimax-theorem/)).
- **Non-example: a game with a random opponent.** If MIN is replaced by a player who moves uniformly at random, the MIN nodes become chance nodes and the game becomes a one-player problem, a finite-horizon [Markov decision process](/markov-decision-process/).

## Related definitions

- **Shapley's stochastic games.** Shapley (1953) used the name for a different model: a finite set of states, and in each state the two players play a matrix game with simultaneous moves. The joint action gives a payoff and a random move to the next state, and the game stops at each stage with positive probability (or the payoffs are discounted). Shapley proved that each state has a value and that the values solve $v(s) = \mathrm{val}\big[R_s(a, b) + \sum_{s'} P(s' \mid s, a, b)\, v(s')\big]$, where val is the value of a matrix game, and that the map on the right is a contraction. The states may repeat, the moves are simultaneous, and optimal strategies are mixed, so it is not a game tree. This model has its own page, [Markov game](/markov-game/), and [minimax-Q](/minimax-q/) is a learning method for it.
- **Simple stochastic games (Condon 1992).** A directed graph, which may have cycles, with MAX vertices, MIN vertices, average vertices (each with two successors chosen with probability $1/2$) and two sinks with payoffs 0 and 1. The value is the probability of reaching the 1-sink under optimal play. Condon proved that deciding whether the value is greater than $1/2$ is in NP and coNP. No polynomial algorithm is known. On an acyclic graph, the value is computed by expectiminimax in time linear in the size of the graph.
- **Game tree.** A [game tree](/game-tree/) without chance nodes, valued by [minimax](/minimax/).
- **Markov decision process.** One player against chance, with states that may repeat. A finite-horizon MDP unrolled into a tree is a stochastic game tree with MAX and chance nodes only.
- **Imperfect-information game.** Chance outcomes, or moves of the other player, may be hidden. See [imperfect-information games](/imperfect-information-game/).

## References
