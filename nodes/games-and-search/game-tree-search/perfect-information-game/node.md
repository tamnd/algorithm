---
tag: PS4NMS
kind: definition
slug: perfect-information-game
name: Perfect-information game
aliases:
- perfect-information two-player game
area: games-and-search/game-tree-search
level: intro
summary: A game in which each player, when it is time to move, knows every move made so far, so each information set of the game tree is one node.
prereqs: [game-tree]
see_also: [imperfect-information-game, zero-sum-game, zermelo-theorem, minimax, stochastic-game, expectiminimax, nash-equilibrium, solved-game]
sources:
  - paper: doi:10.1515/9781400881970-012
    title: Harold W. Kuhn, Extensive games and the problem of information, in Contributions to the Theory of Games II, Annals of Mathematics Studies 28, Princeton University Press (1953)
    locator: pp. 193 to 216 (information sets, the definition of perfect information as information sets of one move each, and the existence of an equilibrium in pure strategies for such games)
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press (1994)
    locator: Chapter 6, Definition 89.1 (extensive game with perfect information) and Proposition 99.2 (Kuhn's theorem, by backward induction)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 5, Section 5.1 (deterministic, fully observable two-player games) and Section 5.5 (games with chance)
---

A game has *perfect information* if every player, each time it is their turn, knows the whole history of the game: every move of every player and every outcome of chance so far. In the [game tree](/game-tree/), the player to move always knows which node the game is at. Chess, checkers, Go, tic-tac-toe and Nim have perfect information; poker and bridge do not, because some cards are hidden. Perfect information is the condition under which a game tree can be solved by [minimax](/minimax/) from the leaves up, and under which [Zermelo's theorem](/zermelo-theorem/) and Kuhn's theorem give each finite game a solution in pure strategies.

## Definition

Take a game in extensive form, as defined by Kuhn (1953): a [game tree](/game-tree/) in which each inner node belongs to a player or to chance, with the probabilities of the chance moves given, and a payoff for each player at each leaf. The nodes of each player are split into *information sets*. A player who moves at a node knows the information set of that node, but not which node of the set it is. So all nodes of one information set must have the same player to move and the same set of moves.

The game has **perfect information** if every information set has exactly one node.

Osborne and Rubinstein define an extensive game with perfect information directly, without information sets: the players, the set of histories, the player function that says who moves after each history, and the preferences over the terminal histories. Their basic form has no chance moves; they add chance as an extension.

Two points are often confused.

- **Perfect information is about moves, not about rules.** A game of *complete information* is one in which all players know the rules and each other's payoffs. Poker is a game of complete information but of imperfect information.
- **Perfect information allows chance.** In backgammon the dice are random, but both players see each roll before the next move. The game has perfect information. Its tree has chance nodes, and it is solved by [expectiminimax](/expectiminimax/), not by minimax.

## Examples and non-examples

**Chess, checkers, Go, tic-tac-toe, Connect Four, Hex.** Two players move in turn, and the whole board is visible. These are perfect-information games with no chance, and the [zero-sum](/zero-sum-game/) ones are the subject of [Zermelo's theorem](/zermelo-theorem/): each has a value, and some of them are [solved](/solved-game/).

**Nim and other impartial games.** The heaps are visible, so these are perfect-information games. [Nim](/nim/) and its relatives are solved by a formula instead of a search.

**Backgammon.** Perfect information with chance. Each node of the tree is known when the player moves, and the dice outcomes are chance nodes.

**A sequential game with more than two players or with payoffs that do not sum to zero.** For example, a firm decides to enter a market and the firm already in the market decides to fight or to accept. Each player sees the earlier moves, so the game has perfect information. Kuhn's theorem still gives an equilibrium in pure strategies, found by working back from the leaves.

**Non-example: poker.** A player does not see the cards of the others. The nodes that differ only in these cards form one information set. This is an [imperfect-information game](/imperfect-information-game/).

**Non-example: rock-paper-scissors.** The two players move at the same time. As a tree, the second player moves at an information set with three nodes, one for each choice of the first player. The game has no value in pure strategies; the [minimax theorem](/minimax-theorem/) gives a value in mixed strategies.

**Non-example: Kriegspiel and Stratego.** The rules are those of a board game, but each player sees only their own pieces, or only the type of their own pieces. The game tree is the same as for a perfect-information game, but the information sets are large.

## Related definitions

- [Imperfect-information game](/imperfect-information-game/): some information set has more than one node. The values then need mixed or behavior strategies, and the methods are different, for example [counterfactual regret minimization](/counterfactual-regret-minimization/).
- [Zero-sum game](/zero-sum-game/): the other condition for the [minimax](/minimax/) value to be the value of the game for two players.
- [Zermelo's theorem](/zermelo-theorem/): a finite two-player game with perfect information and no chance, with outcomes win, loss and draw, is determined.
- **Kuhn's theorem.** Every finite extensive game with perfect information has an equilibrium in pure strategies, which backward induction finds. Kuhn (1953) proved the existence. The equilibrium that backward induction gives is also *subgame perfect*, a term that Selten introduced later, in 1965. See [Nash equilibrium](/nash-equilibrium/) for the general notion.
- [Stochastic game](/stochastic-game/): a game tree with chance nodes. With perfect information it is solved by [expectiminimax](/expectiminimax/).

## References
