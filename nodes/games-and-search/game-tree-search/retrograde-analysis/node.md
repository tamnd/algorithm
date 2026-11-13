---
tag: CADFGP
kind: algorithm
slug: retrograde-analysis
name: Retrograde analysis
aliases:
- backward induction on positions
area: games-and-search/game-tree-search
level: advanced
summary: Works backward from terminal positions to label every position as win, loss or draw.
solves: [endgame-solving]
model: word-ram
complexity:
  vars: {v: the number of positions in the set, e: the number of moves between them}
  time: {worst: O(v + e)}
  space: {extra: O(v)}
properties: {deterministic: true, recursive: false}
prereqs: [winning-losing-states, game-tree, breadth-first-search]
see_also: [endgame-tablebase, endgame-solving, solved-game, games-on-graphs, principle-of-optimality, zermelo-theorem, minimax, proof-number-search]
sources:
  - paper: "Richard Bellman, On the application of dynamic programming to the determination of optimal play in chess and checkers, Proceedings of the National Academy of Sciences of the USA 53(2) (1965)"
    locator: pp. 244 to 247 (the values of all positions of an endgame computed backward from the end of the game, by dynamic programming)
  - url: https://centaur.reading.ac.uk/90000/1/Stroehlein%2050th.pdf
    title: Guy Haworth, Ströhlein's endgame tables, a 50th anniversary, ICGA Journal (2020), doi 10.3233/ICG-200151
    locator: the whole article (Thomas Ströhlein's 1970 doctoral thesis at the TU München, which computed the first chess endgame tables by retrograde analysis)
  - paper: doi:10.3233/ICG-1986-9302
    title: Ken Thompson, Retrograde analysis of certain endgames, ICCA Journal 9(3) (1986)
    locator: pp. 131 to 139 (the method used to build tables of chess endgames with up to five pieces)
  - url: https://www.chessprogramming.org/Syzygy_Bases
    title: Chess Programming Wiki, Syzygy Bases
    locator: the description of the WDL and DTZ tables and their relation to the fifty-move rule
---

Retrograde analysis finds the value of every position in a set of game positions by working backward from the end of the game. It starts from the positions in which the side to move is mated, finds the positions with a move into them (they are won), then the positions all of whose moves lead to won positions (they are lost), and so on, one ply further from the mate in each round. The positions that are never reached are draws. The rule behind it, and the general counter method with its $O(V + E)$ bound, are on the page on [winning and losing states](/winning-losing-states/). This page is about the use of that rule on game positions made from rules, as in chess endgames: the predecessors are made by *unmoves*, not read from a stored graph; the round in which a position is labeled is its exact *distance to mate*; and the result is the [endgame tablebase](/endgame-tablebase/). Bellman (1965) proposed the method for chess and checkers, Ströhlein (1970) built the first chess endgame tables with it, and Thompson (1986) used it for endgames with up to five pieces.

## In plain words

Think of all the positions of one small endgame, for example king and rook against a lone king. Some of them are mate. Start there.

Any position in which White has a move that gives mate is won for White, in one move. Any position in which every Black move walks into a mate in one is lost for Black. Positions one step back from those are won in two moves, and so on.

To step back, the program does not need a list of all the moves. It takes a position and moves a piece backwards: "where could this rook have come from?" When no more positions get a label, the rest are draws: neither side can force a mate there.

## The problem

The input is a finite set $S$ of positions closed under the moves that stay in the game being solved, for example all legal positions with a white king, a white rook and a black king. A move may leave $S$, for example by a capture into a smaller endgame, and then its value comes from that endgame; in the toy here, a move out of $S$ is a draw. The output is, for each position, its value for the side to move (win, loss or draw) and, for a won or lost position, its distance to mate in plies with optimal play: the winner mates as fast as possible, and the loser delays the mate as long as possible. This is one way to solve the [endgame solving](/endgame-solving/) problem for every position at once.

## The algorithm

UNMOVES$(q)$ lists the positions $p$ in $S$ that have a move to $q$. It is made from the rules by moving a piece of the side that just moved backwards, and it must be the exact inverse of MOVES on $S$.

```pseudo id=main
RETROGRADE(S)
L1  for each p in S: if p is a mate then val[p] ← LOSS; dist[p] ← 0; put p in F
L2  n ← 0
L3  while F is not empty do
L4      for each q in F, and each p in UNMOVES(q) that has no label, do
L5          if val[q] = LOSS then val[p] ← WIN; dist[p] ← n + 1; put p in F'
L6          else count[p] ← count[p] − 1 (it starts at |MOVES(p)|); if count[p] = 0 then val[p] ← LOSS; dist[p] ← n + 1; put p in F'
L7      F ← F'; F' ← the empty set; n ← n + 1
L8  for each p in S with no label: val[p] ← DRAW
```

Line L1 is the only place that needs the rules for the end of the game. Each round of lines L4 to L6 labels exactly the positions whose distance is $n + 1$. A position is won as soon as one move leads to a loss, in line L5. It is lost when its counter reaches 0 in line L6, because then every move leads to a position that is won for the opponent. A move that leaves $S$, such as the capture of the rook, never lowers the counter, so a position with such a move is never lost through line L6. The counter is set only when a position is first reached, so it needs no pass over all of $S$.

## Example

The tests use a chess-like toy, not chess: king and rook against king on a 4 by 4 board, with the files a to d and the ranks 1 to 4. White has a king and a rook, Black has a king. Black loses when it is checkmated. A stalemate and the capture of the rook are draws. There are no other pieces, no castling and no move counter.

- $S$ has 3,496 legal positions: 2,184 with Black to move and 1,312 with White to move. A position with White to move in which the black king is in check is illegal, and the kings may not touch.
- There are 40 mates. Every position with White to move is won. With Black to move, 1,572 positions are lost and 612 are draws, because Black can take the rook or is stalemated.
- The longest mate with White to move takes 13 plies, from 12 positions. With Black to move it takes 14 plies.

| plies to mate, White to move | 1 | 3 | 5 | 7 | 9 | 11 | 13 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| positions | 120 | 404 | 316 | 236 | 168 | 56 | 12 |

One of the longest mates is White Ka1, Rd2 against Black Kc3, White to move. Following the table, with White taking a shortest mate and Black a longest defence, the play is 1. Rd1 Kc2 2. Rb1 Kc3 3. Rc1+ Kd4 4. Kb1 Kd3 5. Kb2 Kd4 6. Kb3 Kd3 7. Rd1 mate. In the first move the rook leaves d2, where it blocks its own checks, and in the second move Black's king attacks it, so White guards it on b1. Then the king walks to b3 while the rook on the c-file keeps the black king on the d-file.

## Correctness

The [proof](proofs/correctness/) defines $W_n$, the positions in which the side to move can force a mate within $n$ plies, and $L_n$, those in which the side to move is mated within $n$ plies whatever it does. It shows three things:

- **The layers.** After round $n$, the labeled positions are exactly $W_n \cup L_n$, and the distance of each is the least $n$ at which it enters. A counter reaches 0 in round $n + 1$ exactly when all moves lead to $W_n$.
- **Draws.** A position in no $W_n$ or $L_n$ is a draw. If a side could force a mate, its strategy would give a finite tree of plays, by König's lemma, so the mate would come within some bound $n$. A draw by repetition, an infinite play, is one kind of draw.
- **Exact distances.** A won position is one more than the shortest distance of its moves to lost positions, and a lost one is one more than the longest distance of its moves. So the distance is the distance to mate (DTM) with optimal play.

The tests check the values and distances against a forward computation of the sets $W_n$ and $L_n$ on the toy and on 400 random graphs with cycles, and against a plain game-tree search with the rule that a repeated position is a draw on 300 small graphs. They also check that UNMOVES is the inverse of MOVES on all 3,496 positions, and the two equations of the exact distances at every position.

## Complexity

**Time.** Each position enters a layer at most once, and when $q$ is processed, each move into $q$ is looked at once. So the total time is $O(v + e)$ for $v$ positions and $e$ moves, plus the cost of the move and unmove generators, and of one call of MOVES per position for its counter. The number of rounds is one more than the largest distance.

**Space.** The labels, distances and counters take $O(v)$ words, and there is no stored graph, because UNMOVES makes the predecessors from the rules. In a real table, the positions are numbered by an index function, and the labels are arrays of bytes or of single bits; see [endgame tablebase](/endgame-tablebase/).

## Properties

- **Exhaustive.** It labels every position of $S$, not only one. A forward search, such as [proof-number search](/proof-number-search/) or [alpha-beta](/alpha-beta-pruning/), labels one position.
- **Iterative, not recursive.** It works in rounds, with no recursion and no stack, so the depth of the game does not limit it.
- **Optimal distances.** The round of a label is the distance with optimal play, a form of the [principle of optimality](/principle-of-optimality/).
- **Draws need no extra work.** A draw by repetition or by any infinite play is what is left at the end.

## Variants and improvements

- **Without counters.** When a position $q$ is labeled WIN, each unlabeled predecessor $p$ is checked again: generate all moves of $p$, and label it LOSS if all lead to WIN positions. This trades memory for time.
- **Bit sets per layer.** Each layer is kept as an array of bits over the index of the positions, and the rounds sweep these arrays. This uses one bit per position and per set.
- **Other metrics.** Distance to mate (DTM) is the metric here. Distance to conversion (DTC) counts the plies to a capture or a promotion that leaves the endgame. Distance to zeroing (DTZ) counts the plies to a capture or a pawn move, which resets the fifty-move counter. WDL keeps only win, draw or loss. The Chess Programming Wiki describes the Syzygy tables as WDL tables for the search together with DTZ tables for play.
- **The fifty-move rule.** Under this rule a player can claim a draw after 50 moves by each side with no capture and no pawn move. Some forced wins take longer, and they are draws under the rule. To respect it, the move counter must be part of the position, or the table must use DTZ and mark the wins that the rule turns into draws.
- **Smaller endgames first.** A capture or a promotion leaves $S$ for a smaller endgame. Its tables are built first, and their values are used for the moves out of $S$.
- **Games with scores.** In games such as awari, the value is a score, not only win or loss, and the backward rounds compute the best score. See [solved game](/solved-game/).
- **Parallel and external memory.** Large tables are built on many processors or with the arrays on disk, round by round.

## When to use it

Use retrograde analysis when the set of positions is small enough to store one or a few bits for each, and you want the value of all of them, for example to build a table that a program probes during play. It also fits any finite game with cycles, where a forward search must deal with repetitions. When only one position matters and the set is far too large, use a forward search, such as proof-number search or alpha-beta, as in [endgame solving](/endgame-solving/).

## Pitfalls

- **UNMOVES that are not the inverse of MOVES.** A missing predecessor leaves a counter above 0 for ever, and a position that is lost becomes a draw. Test the inverse on every position.
- **Illegal positions.** A position in which the side that is not to move is in check cannot arise. Exclude it, or its labels will be wrong and it will feed the labels of others.
- **Moves out of the set.** A capture into a smaller endgame must take its value from that endgame. In the toy here it is always a draw, which is a special case.
- **The rules of the full game.** Castling rights, en passant and the fifty-move counter are part of a chess position. Tables usually leave out castling, and they handle the fifty-move rule only with a DTZ metric or a counter.
- **Recursion.** A recursive forward solve can go as deep as the longest line. Retrograde analysis works in rounds and needs no recursion.

## Implementations

## History

Bellman (1965) proposed computing the values of the positions of chess and checkers endgames backward, by dynamic programming. Ströhlein's 1970 doctoral thesis at the TU München, as described by Haworth (2020), built the first chess endgame tables by retrograde analysis. Thompson (1986) described the analysis of chess endgames with up to five pieces. Later tables, the Nalimov, Lomonosov and Syzygy tables, are on the page on [endgame tablebases](/endgame-tablebase/). The name *retrograde analysis* is also used in chess problems for the logical deduction of the moves that led to a position, which is a different task.

## References
