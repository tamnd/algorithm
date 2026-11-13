---
tag: 4P38GP
kind: definition
slug: game-tree
name: Game tree
aliases:
- game graph
- game search tree
area: games-and-search/game-tree-search
level: intro
summary: The rooted tree of all move sequences of a game, with the player to move at each inner node and the outcome at each leaf.
prereqs: [rooted-tree, search-tree]
see_also: [minimax, game-tree-evaluation, perfect-information-game, zero-sum-game, branching-factor, games-on-graphs, imperfect-information-game, solved-game]
sources:
  - paper: doi:10.1515/9781400881970-012
    title: Harold W. Kuhn, Extensive games and the problem of information, in Contributions to the Theory of Games II, Annals of Mathematics Studies 28, Princeton University Press (1953)
    locator: pp. 193 to 216 (the game tree with a player assigned to each move, chance moves, information sets, and the payoff at each play)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 5, Section 5.1 (two-player zero-sum games, plies, the game tree of tic-tac-toe, and the game tree against the search tree)
  - paper: doi:10.26481/dis.19940923la
    title: Louis Victor Allis, Searching for solutions in games and artificial intelligence, PhD thesis, University of Limburg, Maastricht (1994)
    locator: Section 6.2.4 (state-space complexity against game-tree complexity, with tic-tac-toe as the example)
  - paper: doi:10.1080/14786445008521796
    title: Claude E. Shannon, Programming a computer for playing chess, Philosophical Magazine, Series 7, 41(314) (1950)
    locator: pp. 256 to 275 (the tree of move sequences of chess and the estimate of its size)
---

A game tree is the rooted tree of all the ways a game can be played. The root is the start of the game, each edge is a legal move, and each node is the sequence of moves that leads to it. An inner node says which player moves there, and a leaf, where the game is over, gives the outcome. The algorithms of this area, from [minimax](/minimax/) to [alpha-beta pruning](/alpha-beta-pruning/) and [Monte Carlo tree search](/monte-carlo-tree-search/), all work on a game tree or on a part of it. It is a [search tree](/search-tree/) in which the levels belong to players who want opposite things.

## Definition

A game tree for two players MAX and MIN who move in turn is a finite or infinite [rooted tree](/rooted-tree/) $T$ with

- a *player function* that gives each inner node the player to move there, MAX or MIN;
- for each inner node, one child for each legal move, with the edge labeled by the move;
- for each leaf $t$, called a *terminal node*, a *utility* $u(t)$, the outcome for MAX.

A node is a *history*: the sequence of moves from the root. A *position* is what the players see after the history, for example a board and the player to move. Different histories can lead to the same position, a *transposition*, and the tree then has a separate node for each history.

One move of one player is a *ply*. The *depth* of a node is its number of plies from the root, and the depth $d$ of a finite tree is the largest depth of a leaf. The *[branching factor](/branching-factor/)* $b$ is the number of children of a node. In a *uniform* tree each inner node has $b$ children and each leaf is at depth $d$, so there are $b^d$ leaves. The full node count of a uniform tree is given on [search tree](/search-tree/).

The model of this page is the one used in most of this area: two players, alternate moves, [perfect information](/perfect-information-game/), no chance, and a [zero-sum](/zero-sum-game/) outcome. Kuhn (1953) gave the general form, the *extensive form*. It allows more players, *chance nodes* where a random move is made with known probabilities, payoffs for each player, and *information sets*, which group the nodes that a player cannot tell apart. A game tree with chance nodes is a [stochastic game](/stochastic-game/) in the sense of this area, and one with information sets of more than one node is an [imperfect-information game](/imperfect-information-game/).

A *game graph* has one node per position instead of one per history. It has an edge from each position to each position one move later. If positions can repeat, it has cycles. The game tree is the unfolding of the game graph from the start position. Algorithms that work on the graph, with one entry per position, are on [games on graphs](/games-on-graphs/) and [retrograde analysis](/retrograde-analysis/). A game-tree search with a [transposition table](/transposition-table/) works on the tree but saves work by sharing the values of equal positions.

Allis (1994) gave two measures of the size of a game. The *state-space complexity* is the number of legal positions that can be reached from the start, the number of nodes of the game graph. The *game-tree complexity* is the number of leaves of the game tree of a solution search, which he estimates as $b^d$ for an average branching factor and an average game length.

## Examples and non-examples

**Tic-tac-toe.** X is MAX and moves first. The game ends when a player has three in a row or the board is full. The game tree has 549,946 nodes and 255,168 leaves, one leaf per possible game. The game graph has only 5,478 positions, because many move orders give the same board.

| depth (plies) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nodes | 1 | 9 | 72 | 504 | 3,024 | 15,120 | 54,720 | 148,176 | 200,448 | 127,872 |

Up to depth 5 the counts are the falling products $9 \cdot 8 \cdots$, because no game can end before ply 5. After that, games that are over have no children, so the counts grow less. Of the 255,168 games, X wins 131,184, O wins 77,904, and 46,080 are draws. These counts come from a full walk of the tree, which the tests of [solved game](/solved-game/) run.

**A small subtraction game.** There are 4 counters, and a move takes 1 or 2 of them. The player who takes the last counter wins. The game tree has the root 4, children 3 and 2, and so on down to 0. Its leaves are the histories that reach 0, and there are 5 of them, the ways to write 4 as an ordered sum of 1s and 2s. The game graph has only the 5 positions 0 to 4.

**Chess.** The game tree is finite only because of the rules that end a game, such as the fifty-move rule and repetition. Shannon (1950) estimated about $10^{120}$ games, from about $10^3$ choices for a move pair and a game of 40 move pairs. Allis (1994) estimated a game-tree complexity of $10^{123}$, from $b = 35$ and 80 plies. Both are estimates, not counts.

**Non-example: the position graph.** The 5,478 positions of tic-tac-toe with their moves form a directed acyclic graph, not a tree, because a board can be reached in many ways. It is the game graph.

**Non-example: a game with repetition and no end rule.** If players can move back and forth for ever, the unfolding has infinite paths. It is an infinite game tree, and minimax on it does not stop. Such games are handled on the game graph, where positions that are never decided are draws; see [winning and losing states](/winning-losing-states/).

**Non-example: simultaneous moves.** In rock-paper-scissors, both players choose at once. As a tree it needs an information set that hides the first choice from the second player, so it is not a game tree with perfect information.

**Non-example: a search tree of a puzzle.** The tree of [state-space search](/state-space-search/) for one agent has no players and no outcomes for an opponent. All levels belong to the same agent.

## Related definitions

- [Search tree](/search-tree/): the tree of paths of a single-agent search. A game tree has the same shape, but its levels alternate between two players with opposite goals, and its leaves carry outcomes instead of goal tests.
- [State-space tree](/state-space-tree/): the tree of partial solutions of backtracking.
- [Perfect-information game](/perfect-information-game/) and [zero-sum game](/zero-sum-game/): the two conditions that make the minimax value of a game tree the value of the game.
- [Branching factor](/branching-factor/): the number of moves per node, the main parameter of the cost.
- [Game tree evaluation](/game-tree-evaluation/): the problem of computing the value of the root.
- [Winning and losing states](/winning-losing-states/) and [solved game](/solved-game/): what a full evaluation of the tree tells about the game.

## References
