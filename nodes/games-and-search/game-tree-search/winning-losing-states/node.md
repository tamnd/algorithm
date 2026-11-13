---
tag: RX8R4R
kind: concept
slug: winning-losing-states
name: Winning and losing states
area: games-and-search/game-tree-search
level: intro
summary: A position is losing for the player to move if every move leads to a winning position, winning if some move leads to a losing one, and a draw if neither can be forced.
prereqs: [game-tree, perfect-information-game]
see_also: [games-on-graphs, retrograde-analysis, zermelo-theorem, solved-game, nim, grundy-number, sprague-grundy-theorem, endgame-tablebase]
sources:
  - book: isbn:9781568812779
    title: Michael H. Albert, Richard J. Nowakowski and David Wolfe, Lessons in Play, An Introduction to Combinatorial Game Theory, A K Peters (2007)
    locator: Chapter 2, Outcome Classes, from p. 35 (the classes P and N of impartial games, the rule that a position is in P exactly when every option is in N, and subtraction games)
---

In a game for two players who move in turn, with no chance and nothing hidden, each position has an outcome for the player whose turn it is. It is *winning* (written W, or N for "next player wins") if that player can force a win, *losing* (L, or P for "previous player wins") if the opponent can force a win whatever the player does, and a *draw* (D) if neither player can force a win. The labels follow from two local rules: a position is winning if some move goes to a losing position, and losing if every move goes to a winning position. On a finite game graph, one pass backward from the positions where the game is over finds all the labels in $O(V + E)$ time, with a counter per position. This page is about these labels and the labeling method; [games on graphs](/games-on-graphs/) treats the general problem of games played on a directed graph, and [retrograde analysis](/retrograde-analysis/) the same method at the scale of endgame databases.

## In plain words

Say you are about to move. If one of your moves leaves your opponent in a hopeless spot, your spot is good: make that move. If every move you have leaves your opponent in a good spot, your spot is hopeless.

This lets you sort all positions by working back from the end of the game. Where the game is over, you know who has won. One move before that, you know which spots are good. One more step back, you find spots where every move helps the opponent, and so on.

Some games can go round in circles. A spot that never gets sorted this way is one where both players can keep the game going for ever, so neither can force a win, and it counts as a draw.

## The idea

### The two rules

Take a game graph: a finite set of positions and, for each position $p$, the positions $p$ can move to. Under the *normal play* rule, a player who cannot move loses, so a position with no moves is L. Other games give each terminal position its own label, for example L for the player to move after the opponent has made three in a row, and D for a full board.

- $p$ is **W** if some move from $p$ leads to an L position.
- $p$ is **L** if $p$ has moves and every move leads to a W position, or if $p$ is terminal and the rules say so.
- $p$ is **D** if neither holds after all the labels that these rules force have been given.

If the graph has no cycles, every position gets W or L (or a terminal D) by working from the leaves, and the labels are the [minimax](/minimax/) values $+1$, $-1$ and $0$ for the side to move. This is [Zermelo's theorem](/zermelo-theorem/) for win, loss and draw. With cycles, some positions may never be forced either way, and these are draws: the player who would lose can always move to a position that is not lost, and can do so for ever.

### Labeling with counters

```pseudo id=main
LABEL(G)
L1  for each position p do count[p] ← number of moves from p
L2  give each terminal position its label; put the W and L ones in a queue Q
L3  while Q is not empty do take q from Q
L4      for each move p → q with p not labeled do
L5          if q is L then label p as W and put p in Q
L6          else count[p] ← count[p] − 1; if count[p] = 0 then label p as L and put p in Q
L7  label every position that is still not labeled as D
```

The counter of $p$ is the number of its moves that are not yet known to lead to a W position. When it reaches 0, every move leads to a win for the opponent, so $p$ is lost. A move listed twice counts twice. The method needs the reverse graph, the list of the moves into each position, which costs one pass over the moves.

**Cost.** Each position enters the queue at most once, when it gets its label, and each move $p \to q$ is looked at once, when $q$ leaves the queue. With the reverse graph built in one pass, the total time is $O(V + E)$ for $V$ positions and $E$ moves, and the space is $O(V + E)$. The input size here is the game graph, not the rules of the game: for chess the graph is far too big, and the method is used only on parts of it, as in [endgame tablebases](/endgame-tablebase/).

**Why it is right.** A position labeled W has a move to a position labeled L earlier, and one labeled L has only moves to positions labeled W earlier (or no moves). By induction on the order of labeling, the player to move at a W position wins in at most as many moves as the order shows, and so on for L. For D: a position that ends with the label D has no move to an L position, or it would be W, and not all its moves go to W positions, or its counter would be 0. So it has a move to another D position. The player to move can always stay in D positions, so the game either goes on for ever or ends in a terminal draw, and neither player can force a win. The order in which W and L positions are found also gives the number of moves to the end, which is the distance used in endgame tables.

## Examples

**Take 1, 2 or 3.** From a heap of $n$ counters, a move takes 1, 2 or 3, and the player who takes the last counter wins. The positions $0, 1, \ldots, 8$ are labeled L W W W L W W W L. The losing positions are the multiples of 4, because from $4k$ every move goes to $4k - 1$, $4k - 2$ or $4k - 3$, and from those the player to move can go back to $4(k - 1)$.

**Take 1, 3 or 4.** The positions $0, 1, \ldots, 12$ are labeled L W L W W W W L W L W W W. The losing positions are those with $n \bmod 7$ equal to 0 or 2. The tests check both rules up to $n = 300$ against a direct recursive solve, and 40 random subtraction sets with a fixed seed.

**A graph with a cycle.** The positions are $t, a, b, c, d, e, f$ with the moves $a \to t$, $a \to b$, $b \to a$, $b \to c$, $c \to b$, $c \to d$, $d \to c$, $e \to a$, $f \to e$, $f \to c$. The position $t$ has no move, so it is L. Then $a$ is W, because it can move to $t$. The counter of $e$ goes from 1 to 0, so $e$ is L, and then $f$ is W. The counter of $b$ goes from 2 to 1, and nothing more happens. The positions $b$, $c$ and $d$ stay unlabeled and are draws: from $b$ the player to move goes to $c$, not to $a$, and the play can go round $b$, $c$, $d$ for ever.

| position | t | a | e | f | b | c | d |
| --- | --- | --- | --- | --- | --- | --- | --- |
| label | L | W | L | W | D | D | D |
| found in round | 1 | 2 | 3 | 4 | never | never | never |

**Tic-tac-toe.** The 5,478 positions that can be reached form an acyclic graph with 16,167 moves. A finished board is L for the player to move if the opponent has three in a row, and D if the board is full. The labeling gives 2,836 W, 1,574 L and 1,068 D positions, for the player to move, and the empty board is D. The tests check every label against a recursive negamax.

**Random graphs.** The tests also check the labels on 300 random graphs with up to 14 positions, many with cycles, against a separate method that asks, for each position, whether the player to move can force a win within $2V + 1$ plies.

## Where it is used

- **[Nim](/nim/) and impartial games.** The P and N positions of combinatorial game theory are the L and W labels. The [Grundy number](/grundy-number/) refines them: a position is P exactly when its Grundy number is 0, and the [Sprague-Grundy theorem](/sprague-grundy-theorem/) extends this to sums of games.
- **[Retrograde analysis](/retrograde-analysis/) and [endgame tablebases](/endgame-tablebase/).** The same counters, run on all chess positions with a few pieces, or on all positions of awari, give tables of exact results.
- **[Games on graphs](/games-on-graphs/).** Reachability games and safety games on a directed graph are solved by the same backward pass. Parity games need more than this.
- **[Solved games](/solved-game/).** A strong solution is a W, L or D label for every position.
- **[Zermelo's theorem](/zermelo-theorem/).** The labeling on a finite acyclic graph is a proof that each such game is determined.

## References
