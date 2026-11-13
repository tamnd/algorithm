---
tag: V7ZSNV
kind: technique
slug: killer-heuristic
name: Killer heuristic
aliases:
- killer moves
area: games-and-search/game-tree-search
level: advanced
summary: Move ordering that keeps, for each ply, the last one or two quiet moves that caused a cutoff, and tries them early at the other nodes of the same ply.
prereqs: [move-ordering]
see_also: [history-heuristic, alpha-beta-pruning, transposition-table, iterative-deepening-search, null-move-pruning, principal-variation-search]
sources:
  - paper: doi:10.1145/800179.810240
    title: Selim G. Akl and Monroe M. Newborn, The principal continuation and the killer heuristic, Proceedings of the ACM Annual Conference (ACM '77)
    locator: pp. 466 to 473 (the killer heuristic in alpha-beta, and its effect on the number of nodes)
  - paper: doi:10.1109/34.42858
    title: Jonathan Schaeffer, The history heuristic and alpha-beta search enhancements in practice, IEEE Transactions on Pattern Analysis and Machine Intelligence 11(11) (1989)
    locator: pp. 1203 to 1212 (killer moves compared with the history heuristic and other enhancements, in chess)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition, Pearson (2020)
    locator: Chapter 5, Section 5.2 (killer moves as a source of move ordering)
---

The killer heuristic is a [move ordering](/move-ordering/) rule for [alpha-beta](/alpha-beta-pruning/) search. When a move causes a cutoff at a node, the search remembers it in a small table indexed by the ply, the distance from the root. At the next node of the same ply, it tries the remembered moves first, if they are legal there. The idea is that the nodes of one ply are often siblings or cousins, positions that differ only in one earlier move, and a move that refuted one of them often refutes the others. A threat to capture the queen, for example, refutes most of the quiet moves of the opponent. The table keeps one to three moves per ply, usually two, and only quiet moves, because captures are ordered by their own rule. The value of the search does not change.

## In plain words

Suppose your opponent tried a move, and you found a strong reply that shut it down. Now your opponent tries a different move in the same spot. Very often the same strong reply works again, because the new move did nothing about the threat.

So you keep a short note for each level of the search: "this reply worked last time". When you come to the same level again, you try the noted reply first, if it is allowed. If it works again, you are done with this move fast.

The note is just a guess. If the reply is not allowed or does not work, you go on with the other moves as usual, and the answer stays the same.

## When it applies

The killer heuristic applies to any alpha-beta search where:
- the moves have an identity that makes sense across positions, such as "knight from g1 to f3" in chess or a column in Connect Four, and
- sibling positions are alike, so a refutation of one is often a refutation of the next.

It suits quiet moves that no static rule ranks high. Captures and promotions have their own order, and the move from the [transposition table](/transposition-table/) comes before the killers.

## The template

```pseudo id=main
KILLER-ALPHABETA(n, d, α, β, ply)
L1  if d = 0 or n is terminal then return EVALUATE(n)
L2  order the moves of n: the moves of K[ply] that are legal at n first, in slot order, then the others
L3  m ← −∞
L4  for each move x in this order, giving the child c, do
L5      t ← −KILLER-ALPHABETA(c, d − 1, −β, −max(m, α), ply + 1)
L6      if t > m then m ← t
L7      if m ≥ β then
L8          if x is quiet then put x in slot 1 of K[ply], and move the old killers down one slot   ▷ hole: the number of slots
L9          return m
L10 return m
```

**The holes.** The number of slots per ply is usually 2. With one slot, a second refutation replaces the first at once. With more slots, the killers crowd out moves that the base order ranks well. Line L8 moves $x$ to slot 1 if it is already a killer, so the table holds distinct moves, newest first. "Quiet" is a rule of the game, for example "not a capture and not a promotion" in chess. In line L2 a killer must be legal at $n$. A program that keeps the killers as bare moves must check this, since the same move can be impossible in a sibling position.

**Why the value does not change.** Lines L2 and L8 only change the order of the moves. The proof on the [alpha-beta](/alpha-beta-pruning/) page holds for any order, so the result is the same, and with the full window it is the [negamax](/negamax/) value.

**Cost.** The table has $O(1)$ slots per ply, so line L2 and line L8 cost $O(1)$ work each, plus one pass over the moves.

**What the tests measure.** In tic-tac-toe from the empty board, with the squares in a random fixed order for each of 10 seeds, plain alpha-beta visits 194578 nodes in total and alpha-beta with two killers per ply visits 75093. In a random game where move $m$ adds a gain $w_m$ plus noise to the score of the mover, with $b = 4$ and $d = 6$, the total over 20 seeds falls from 27496 to 16943 nodes. The values are the same in every run. The killers help in this game because a move with a high $w_m$ is good in every position, so a refutation found at one node works at its siblings.

## Classic examples

- **Chess programs.** Programs since the 1970s keep two killers per ply and try them after the move from the [transposition table](/transposition-table/) and the good captures, and before the other quiet moves, which are sorted by the [history heuristic](/history-heuristic/).
- **Mate threats.** When the opponent threatens mate, the mating move refutes every move that does not defend. It becomes the killer at the ply, and the search finds the refutation of the next bad move at once.
- **Null-move searches.** In [null-move pruning](/null-move-pruning/), the move that refutes the null move is the threat of the position, and some programs use it as a killer for the following moves.
- **Connect Four and other drop games.** The moves are columns, which are the same in every position, so a column that blocks a threat in one position is a good first try in the next.

## Variations

- **Mate killers.** A separate slot for moves that gave a mate score, tried before the other killers.
- **Killers from two plies up.** Some programs also try the killers of ply $p - 2$, the last ply with the same side to move.
- **Counter moves.** A table indexed by the last move of the opponent, which stores the reply that refuted it. This ties the killer to the move that it answers, not only to the ply.
- **Killer counters.** Each killer has a count of its cutoffs, and the replace rule keeps the move with the higher count.
- **A history of all moves.** The [history heuristic](/history-heuristic/) generalizes the idea from the last few moves of one ply to a score for every move over the whole tree.

## Pitfalls

- **Illegal killers.** A killer from a sibling may be illegal in the current position. A program that plays it without a check corrupts the board. Check legality, or take the killers only from the list of legal moves, as the implementation does.
- **Storing captures.** A capture that caused a cutoff is usually tried early anyway, by the capture order. As a killer it pushes out a quiet move that needed the slot.
- **Stale tables.** A killer table from the previous search of a different root has plies that no longer match. Clear it, or shift it by two plies when the game advances by one move of each side.
- **Duplicates in the slots.** If line L8 stores a move that is already in another slot, the table holds one move twice and loses the second killer.

## Exercises

1. A table has two slots per ply, both empty at first. The cutoff moves at ply 3 come in the order a, b, a, c, c. Give the content of the slots after each one. The test file checks the final state.
2. Construct a uniform tree of depth 3 and branching factor 3 where the base order visits all 27 leaves, but the killer heuristic with one slot visits fewer. (Hint: give every MIN node the same refuting move index.)
3. Explain why the killers of ply $p$ are more useful for the next sibling of a node of ply $p - 1$ than for a node of ply $p$ in another part of the tree. What does this suggest about clearing the slots of the plies below a node when the search returns from it?

## References
