---
tag: WAWMJQ
kind: definition
slug: zero-sum-game
name: Zero-sum game
aliases:
- constant-sum game
area: games-and-search/game-tree-search
level: intro
summary: A game in which the payoffs of the players add up to zero in every outcome, so one player gains exactly what the others lose.
prereqs: []
see_also: [minimax-theorem, nash-equilibrium, minimax, negamax, perfect-information-game, game-tree, linear-programming-problem, yao-minimax-principle]
sources:
  - book: isbn:9780262650403
    title: Martin J. Osborne and Ariel Rubinstein, A Course in Game Theory, MIT Press (1994)
    locator: Chapter 2, Section 2.5 (strictly competitive games, Definition 21.1, maxminimization, and the value of a strictly competitive game on p. 23)
  - book: isbn:9780691130613
    title: John von Neumann and Oskar Morgenstern, Theory of Games and Economic Behavior, commemorative edition
    locator: the chapters on zero-sum two-person games and the reduction of general games to zero-sum games with an added fictitious player
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 5, Section 5.1 (two-player zero-sum games, and constant-sum outcomes such as 1, 0 and 1/2 in chess)
---

A *zero-sum game* is a game in which the payoffs of all players add up to zero in every outcome. With two players, whatever one player wins the other loses, so the players have exactly opposite goals and there is no room for cooperation. The payoffs of a two-player zero-sum game are one number per outcome, the gain of the first player. This is what [minimax](/minimax/) and [negamax](/negamax/) search use, and what the [minimax theorem](/minimax-theorem/) is about. A *constant-sum game*, in which the payoffs add up to the same constant in every outcome, is a zero-sum game after a shift of the payoffs.

## Definition

A game has a set of players $1, \ldots, k$, a set $O$ of outcomes (the leaves of a [game tree](/game-tree/), or the strategy profiles of a game in normal form), and a payoff $u_i(o)$ for each player $i$ and outcome $o$. The game is

- **zero-sum** if $\sum_{i=1}^{k} u_i(o) = 0$ for every outcome $o$;
- **constant-sum** if $\sum_{i=1}^{k} u_i(o) = c$ for every outcome $o$, for one constant $c$.

For two players, a zero-sum game is given by the payoff $u(o) = u_1(o)$ alone, because $u_2 = -u$. In normal form this is one $m \times n$ matrix $A$: the row player picks a row $i$, the column player a column $j$, the row player gets $a_{ij}$ and the column player gets $-a_{ij}$.

**Constant-sum reduces to zero-sum.** For two players, replace $u_2$ by $u_2 - c$. For $k$ players, replace each $u_i$ by $u_i - c/k$. A shift by a constant does not change which strategy is better for a player against any fixed strategies of the others, so best responses, equilibria and the optimal strategies stay the same, and the value moves by the shift. Positive scaling of all payoffs by the same factor does not change them either.

**Strictly competitive games.** Osborne and Rubinstein call a two-player game *strictly competitive* when the two players rank the outcomes in exactly opposite order. A zero-sum game is strictly competitive. For games with randomness the ranking must hold for expected payoffs, and then the definitions agree up to a positive affine change of one player's payoff.

## Examples and non-examples

**Chess, with win $+1$, draw $0$ and loss $-1$.** A two-player zero-sum game. With the tournament scores 1, 1/2 and 0, the two scores add up to 1, a constant-sum game, which is the same game after a shift by 1/2.

**Matching pennies.** Each player shows heads or tails. If they match, the row player wins 1 from the column player, otherwise the column player wins 1. The matrix is
$$ A = \begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix}. $$
With pure strategies, the row player can only guarantee $\max_i \min_j a_{ij} = -1$, and the column player can only hold the row player to $\min_j \max_i a_{ij} = +1$. The two numbers differ, so the game has no value in pure strategies. With mixed strategies, both are 0 at the strategy (1/2, 1/2), as the [minimax theorem](/minimax-theorem/) says.

**Poker among friends.** The money won equals the money lost, so the game is zero-sum. In a casino that takes a fee from each pot, the sum is negative and depends on the pot, so the game is not constant-sum.

**Non-example: the prisoner's dilemma.** Both players are better off if both cooperate than if both defect, so the sum of the payoffs is not constant. The game is general-sum, and an equilibrium is a [Nash equilibrium](/nash-equilibrium/) that need not be a min-max point.

**Non-example: a game that is zero-sum for three players.** Three players with payoffs that add up to zero are zero-sum by the definition, but the two-player theory does not apply: two of the players can gain together at the cost of the third. Von Neumann and Morgenstern showed that each game with $k$ players and any payoffs becomes a zero-sum game with $k + 1$ players, by an added fictitious player who gets the negative of the sum. So zero-sum is a strong condition only for two players.

## Related definitions

- [Minimax theorem](/minimax-theorem/): every finite two-player zero-sum game has a value in mixed strategies, and each player has an optimal mixed strategy. The value and the strategies come from one [linear program](/linear-programming-problem/).
- [Perfect-information game](/perfect-information-game/): with perfect information and no chance, a two-player zero-sum game has a value in pure strategies, which [minimax](/minimax/) computes on the game tree.
- [Nash equilibrium](/nash-equilibrium/): the solution of a general-sum game. In a two-player zero-sum game the equilibria are exactly the pairs of optimal strategies, they all give the same payoff, and any optimal strategy of one player can be paired with any optimal strategy of the other.
- [Negamax](/negamax/): the form of minimax that uses $u_2 = -u_1$ directly.
- [Yao's minimax principle](/yao-minimax-principle/): the minimax theorem applied to the zero-sum game between an algorithm and its input, a tool for lower bounds on randomized algorithms.

## References
