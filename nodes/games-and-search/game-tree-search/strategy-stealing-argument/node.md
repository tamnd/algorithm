---
tag: G3BS01
kind: theorem
slug: strategy-stealing-argument
name: Strategy-stealing argument
aliases:
- strategy stealing
area: games-and-search/game-tree-search
level: advanced
summary: "In a finite symmetric game where an extra move never hurts, the second player cannot have a winning strategy, so the first player wins (Hex, Chomp) or at least draws (tic-tac-toe)."
prereqs: [zermelo-theorem, perfect-information-game]
see_also: [hex-game, solved-game, winning-losing-states, game-tree, minimax, combinatorial-game-theory, nim, zero-sum-game]
sources:
  - paper: doi:10.1080/00029890.1979.11994922
    title: David Gale, The game of Hex and the Brouwer fixed-point theorem, The American Mathematical Monthly 86(10) (1979)
    locator: pp. 818 to 827 (the first player wins Hex, by strategy stealing, and a full Hex board always has a winner; the account of the invention of Hex by Piet Hein and John Nash)
  - paper: "\"A curious Nim-type game\""
    title: David Gale, A curious Nim-type game, The American Mathematical Monthly 81(8) (1974)
    locator: pp. 876 to 879 (Chomp on a rectangle, and the proof that the first player wins without a known strategy)
  - book: isbn:9780521461009
    title: József Beck, Combinatorial Games, Tic-Tac-Toe Theory, Cambridge University Press (2008)
    locator: the part on strong positional games, where strategy stealing shows that the first player can force at least a draw (general locator)
---

The strategy-stealing argument proves that in a finite game of perfect information, if the start looks the same to both players and an extra move never hurts, the second player has no winning strategy. So the first player can force at least a draw, and wins when draws are impossible. The proof is by contradiction: if the second player had a winning strategy, the first player could make any move and then follow that strategy as if they were second, and the extra move would only help. The argument shows that the first player wins Hex and Chomp, and at least draws tic-tac-toe, but it gives no strategy.

## Statement

**Setting.** A *positional game* has a finite set $B$ of cells and two families $\mathcal{W}_1$, $\mathcal{W}_2$ of subsets of $B$, the winning sets of player 1 and player 2. The players claim cells in turn, one unclaimed cell per move, player 1 first. The first player to own every cell of some set in their own family wins. If all cells are claimed and nobody has won, the game is a draw.

**Hypothesis (S), symmetry.** There is a permutation $\sigma$ of $B$ with $\sigma(\mathcal{W}_1) = \mathcal{W}_2$ and $\sigma(\mathcal{W}_2) = \mathcal{W}_1$, where $\sigma(\mathcal{W}) = \{\sigma(W) : W \in \mathcal{W}\}$.

**Theorem.**

- **(a)** Under (S), player 1 has a strategy that guarantees at least a draw. Equivalently, player 2 has no winning strategy.
- **(b)** If, in addition, no play can end in a draw (for every $A \subseteq B$, either $A$ contains a set of $\mathcal{W}_1$ or $B \setminus A$ contains a set of $\mathcal{W}_2$), then player 1 has a winning strategy.
- **(c)** *A dominating move.* Let $G$ be a finite game under the normal rule (the player who cannot move loses), and let $s$ be a position. If $s$ has a move to a position $t$ such that every move from $t$ leads to a position that is also reachable from $s$ in one move, then the player to move at $s$ has a winning strategy.

"An extra move never hurts" is built into the setting: owning more cells never removes a winning set. In (c), the move to $t$ plays the role of the extra move.

## In plain words

Suppose the player who moves second had a sure way to win. The first player could then steal it. They make any move at all, and then pretend that this stone is not on the board. Now they are, in their own mind, the second player, so they follow the sure way to win.

If the plan ever tells them to play where the forgotten stone already sits, they play anywhere else instead, and forget that stone now. An extra stone of your own can only help you. So the first player would win too.

Both players cannot have a sure win. So the second player has no sure win. The first player can always avoid losing, and if a draw is impossible, the first player wins.

The argument says nothing about which move to make. It proves that a winning strategy exists without finding it.

## Proof

**(a).** By [Zermelo's theorem](/zermelo-theorem/) applied to this finite game, exactly one of three things holds: player 1 can force a win, player 2 can force a win, or each player can force at least a draw. So it is enough to show that player 2 has no winning strategy.

Suppose that $S$ is a winning strategy for player 2. Since (S) maps the families onto each other, $S$ is also a winning strategy for the *second* player in the *imagined game*: the same game with the cells renamed by $\sigma$, where player 2 of the real game is the first player (called role 1, with winning sets $\mathcal{W}_1$) and player 1 of the real game is the second player (role 2, with winning sets $\mathcal{W}_2$). In other words, $S$ is a strategy for the second mover such that in every play that follows $S$, role 2 completes a set of $\mathcal{W}_2$ before role 1 completes a set of $\mathcal{W}_1$. (After the imagined game is decided, $S$ may answer with any free cell; this does not matter.)

Define a strategy $T$ for real player 1. Player 1 keeps imagined sets $X$ (cells of role 1) and $Y$ (cells of role 2) and an *extra cell* $e$. At the start, player 1 claims any cell $e$, and $X = Y = \emptyset$. After each move of player 1 these invariants hold:

1. the real cells of player 2 are exactly $\sigma(X)$;
2. the real cells of player 1 are exactly $\sigma(Y) \cup \{e\}$, with $e \notin \sigma(X \cup Y)$;
3. $(X, Y)$ is a position of the imagined game reached by a play in which role 2 follows $S$, and $|X| = |Y|$.

They hold at the start. When player 2 claims a free cell $c$, then $c \notin \sigma(X \cup Y) \cup \{e\}$, so $x = \sigma^{-1}(c)$ is free in the imagined game; player 1 sets $X \leftarrow X \cup \{x\}$ and asks $S$ for its reply $z \notin X \cup Y$, and sets $Y \leftarrow Y \cup \{z\}$. If $\sigma(z) \ne e$, the cell $\sigma(z)$ is free in the real game, because it is not in $\sigma(X \cup Y)$ and not $e$, and player 1 claims it. If $\sigma(z) = e$, player 1 already owns $\sigma(z)$; it claims any free cell $e'$ and sets $e \leftarrow e'$. (If no free cell is left, the real board is full and the game is over.) In both cases invariants 1 to 3 hold again.

Now suppose that player 2 wins a play against $T$, by completing a set $C \in \mathcal{W}_2$ with the cell $c$. By invariant 1, $C \subseteq \sigma(X)$ after $X$ gets $\sigma^{-1}(c)$, so role 1 owns $\sigma^{-1}(C)$, which lies in $\mathcal{W}_1$ because $\sigma^{-1}(\mathcal{W}_2) = \mathcal{W}_1$. The imagined play follows $S$, which is winning for role 2, so role 2 completed some $D \in \mathcal{W}_2$ at an earlier move: $D \subseteq Y$ already after an earlier reply of player 1. At that earlier moment, by invariant 2, player 1 owned $\sigma(D) \in \mathcal{W}_1$. So player 1 had already won, and the play had ended before player 2's move: a contradiction. Hence player 1 never loses against any play of player 2 when it uses $T$.

But $S$ was assumed to win against every strategy of player 1, $T$ included. This contradiction shows that player 2 has no winning strategy, and by Zermelo's theorem player 1 can force at least a draw. $\square$

**(b).** By (a), player 1 can force at least a draw. Every play ends with a full board or with a win; if the board is full, the set $A$ of player 1's cells contains a set of $\mathcal{W}_1$ or its complement contains a set of $\mathcal{W}_2$, so somebody has won and no play is a draw. A strategy that never loses is then a winning strategy. $\square$

**(c).** $G$ is finite, so every position is a win or a loss for the player to move ([winning and losing states](/winning-losing-states/)). If $t$ is a loss for the player to move there, moving from $s$ to $t$ wins. Otherwise $t$ has a move to a position $u$ that is a loss for the player to move. By hypothesis $u$ is reachable from $s$ in one move, so moving from $s$ to $u$ wins. In both cases the player to move at $s$ has a winning move. $\square$

## Consequences

- **Hex.** Take the cells of the $n \times n$ board, Red's winning sets the chains from top to bottom and Blue's the chains from left to right. The reflection $\sigma(r, c) = (c, r)$ swaps the two families, so (S) holds. A full board always has exactly one winner (the Hex theorem, see [Hex](/hex-game/)), so draws are impossible, and by (b) the first player wins on every empty $n \times n$ board. Search confirms it on boards up to $4 \times 4$, but no explicit strategy is known for large boards.
- **Tic-tac-toe and its relatives.** In tic-tac-toe both players have the eight lines as winning sets, so $\sigma$ is the identity, and by (a) the first player can force at least a draw. The same holds for tic-tac-toe on any board in any dimension, and for $k$ in a row. Full search shows that $3 \times 3$ tic-tac-toe is a draw, so "at least a draw" is the most the argument can give.
- **Chomp.** The board is a rectangle of squares, the bottom-left one poisoned; a move picks a square and removes it with every square above and to the right of it, and the player who must take the poison loses. Let $t$ be the position after taking only the top-right square. Every move from $t$ removes a square together with everything above and to its right, which includes the top-right square, so it gives the same position as making that move from the start. By (c), the first player wins every rectangle except $1 \times 1$.
- **The argument is not constructive.** In Chomp the winning move is known only for some shapes: on a square board, take the square diagonally next to the poison, leaving two equal arms, then copy the opponent's move on the other arm; on a board with two rows, take the top-right square. With three rows the winning first move changes with the width (search gives $(2,1)$, $(1,1)$, $(1,2)$, $(2,3)$, $(1,3)$ for widths 2 to 6, as (row, column) with the poison at $(0, 0)$).
- **Swap rules.** Because the first player wins Hex, tournament play uses the swap rule: the second player may take over the first stone, which forces the first player to open with a move of unclear value.

## Tightness

- **Symmetry is needed.** On a Hex board with 3 rows and 2 columns, where the first player must join the two rows that are 3 apart and the second player the two columns that are 2 apart, search shows that the second player wins. The $2 \times 3$ board with the roles exchanged is a first-player win. Without $\sigma$, the stolen strategy would aim at the wrong sets.
- **An extra move must never hurt.** In games where a player must move and moving can be bad, the conclusion fails even when the start looks the same to both players. In [Nim](/nim/) with heaps $1, 1$ or $2, 2$, the second player wins by copying. Positional games avoid this because owning more cells never removes a winning set; in a misère positional game, where completing a set loses, the argument breaks.
- **First to complete wins.** The setting ends the game at the first completed set. Part (a) uses this when it compares the moments at which the two players complete their sets.
- **Draws.** Without (b), part (a) cannot be improved: tic-tac-toe satisfies (S) and is a draw.
- **Finiteness.** Zermelo's theorem needs a finite game; for infinite games the three-way split of outcomes can fail, and then the step from "player 2 has no winning strategy" to "player 1 can force at least a draw" is lost.

## History

Gale introduced Chomp in 1974 and proved by this argument that the first player wins. In 1979 he published a proof that a full Hex board always has a winner, presented the strategy-stealing proof that the first player wins Hex, which is due to Nash, and told the history of the game, invented by Piet Hein in 1942 and again by John Nash in the late 1940s. Beck's 2008 book treats strategy stealing as a basic tool for strong positional games such as tic-tac-toe, where it gives the first player at least a draw.

## References
