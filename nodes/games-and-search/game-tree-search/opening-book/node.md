---
tag: 398VMX
kind: data-structure
slug: opening-book
name: Opening book
aliases:
- book moves
area: games-and-search/game-tree-search
level: advanced
summary: Precomputed table mapping opening positions to recommended moves.
model: word-ram
complexity:
  vars: {k: the number of book moves of a position, v: the number of book positions, e: the number of book moves in all}
  time: {expected: O(1), worst: O(k), build: O(v + e)}
  space: {extra: O(v + e)}
prereqs: [zobrist-hashing, hash-table, game-tree, minimax]
see_also: [transposition-table, endgame-tablebase, topological-sort, negamax, monte-carlo-tree-search, evaluation-function, solved-game]
sources:
  - paper: "Robert M. Hyatt, Book learning, a methodology to tune an opening book automatically, ICCA Journal 22(1) (1999)"
    locator: pp. 3 to 12 (book learning in the program Crafty, which changes the weights of book moves after games from the results and from the search scores just after the program leaves the book)
  - paper: doi:10.3233/ICG-1999-22204
    title: Michael Buro, Toward opening book learning, ICCA Journal 22(2) (1999)
    locator: pp. 98 to 102 (a book for the Othello program Logistello that keeps the games as a graph, backs up negamax values over it, and adds a deviation so that the program does not lose the same way twice)
  - url: http://digital.library.wisc.edu/1793/57624
    title: Albert L. Zobrist, A new hashing method with application for game playing, Technical Report 88, Computer Sciences Department, University of Wisconsin, April 1970
    locator: the whole report (the hash of a position by XOR of random numbers, which books use as their key)
---

An opening book is a table, made before play, that gives a game program its moves in the first part of the game. It maps a position to a short list of *book moves*, each with a weight and a record of the games in which it was played. While the current position is in the book, the program plays a book move, chosen at random in proportion to the weights, and does not search. When the position is not in the book, the program is *out of book* and starts to search. The key of a position is its [Zobrist hash](/zobrist-hashing/), so two move orders that reach the same position share one entry: the book is a directed acyclic graph of positions, not a tree of move sequences. Books are built from game records, from analysis, or from the program's own searches, and *book learning* changes the weights after the program's own games, as in Hyatt (1999) for chess and Buro (1999) for Othello.

## In plain words

A chess player does not think hard about the first moves of a game. They know good first moves from study and from earlier games. A program does the same with a book: a list of known positions, and for each one the moves that are known to be good.

Because a position can be reached in different ways, the book is keyed by the position, not by the moves that led to it. So a book is more like a map of crossroads than a list of routes.

The book does not always give the same move. Each move has a weight, and the program picks at random, with the heavier moves more often, so that an opponent cannot prepare for one fixed line. After each game, the program can make the moves that lost lighter and the moves that won heavier.

## The abstract type

An opening book $B$ holds a set of positions, and for each position $p$ a set of book moves $x$ with a weight $w(p, x) \ge 0$, a count of games and the points of the mover in them. It has these operations:

- BOOK-PROBE$(B, p)$: the book moves of $p$, or nothing if $p$ is not in the book.
- BOOK-ADD$(B, \text{line}, r)$: add one game with the result $r$, up to a fixed number $h$ of plies.
- BOOK-CHOOSE$(B, p)$: a book move of $p$, drawn with probability $w(p, x) / \sum_y w(p, y)$ over the moves of positive weight, or NIL if there is none.
- BOOK-LEARN$(B, \text{line}, s, r)$: change the weights of the book moves that the side $s$ played in a game with result $r$.
- BOOK-BACKUP$(B, \text{leaf})$: the negamax value of each book position when both sides play book moves, with the positions just after the book scored by leaf.

The positions and the book moves form a graph. It is a DAG in every game in which a move cannot undo itself, as in tic-tac-toe, Othello or the opening of chess. Positions with two parents are *transpositions*.

## Representation

A [hash table](/hash-table/) maps the key $Z(p)$ of each position to a small table from moves to entries (weight, games, points). The key is the XOR of one random 64-bit word per piece on the board, plus a word for the side to move when the board alone does not tell it. The key of the next position is the old key XOR the word of the new piece, so a line is followed with one XOR per move. Real books often store the entries sorted by key in a file and probe it by [binary search](/binary-search/), since the book is read often and written rarely.

The implementation here is a toy for tic-tac-toe. A position is a board of 9 cells; X moves first, so the side to move follows from the pieces. It keeps the board of each key beside the entry so that the tests can check that no two positions share a key; a real book stores only the key.

## Operations

```pseudo id=main
BOOK-PROBE(B, p)
L1  return B.table[Z(p)], or the empty list if there is no entry

BOOK-ADD(B, line, r)
L2  z ← 0; p ← the start position
L3  for each move x of line, while the ply is less than h, do
L4      e ← the entry of x in B.table[z], made with zero counts if missing
L5      e.games ← e.games + 1; e.points ← e.points + score of r for the mover; e.weight ← e.games
L6      z ← z XOR Z[x, mover]; p ← the position after x

BOOK-CHOOSE(B, p)
L7  E ← the book moves of p with weight > 0
L8  if E is empty then return NIL                     ▷ out of book: search instead
L9  return x in E with probability e.weight / (the sum of the weights in E)

BOOK-LEARN(B, line, s, r)
L10 if r is a draw then return; f ← 3/2 if s won, else 1/2
L11 for each book move e that s played on line: e.weight ← f · e.weight, and 0 if below 1/4

BOOK-BACKUP(B, leaf)
L12 for each book position p, by decreasing number of pieces, do
L13     val[p] ← the maximum over the book moves x of p, to c, of −(val[c] if c is in B, else leaf(c))
L14 return val
```

The score in line L5 is 1 for a win of the mover, 1/2 for a draw and 0 for a loss. Line L5 sets the weight to the number of games, so a fresh book plays its moves as often as they occur in the games it was built from. Line L11 is a simple learning rule based only on the result: it is in the spirit of book learning, but it is not the exact formula of Hyatt (1999), whose program also uses the search score of the first positions after the book. Line L12 uses the number of pieces as a [topological order](/topological-sort/) of the book graph, so that line L13 sees each child before its parent.

## Example

The tests build a book from 500 games of tic-tac-toe made with `random.Random(7)`. In each game, each side plays a random best move, and with probability 0.2 a random legal move instead. X won 169 games, O won 75 and 256 were draws. The book keeps the first 4 plies, and the Zobrist words come from `random.Random(1970)`.

- The 500 games have 2,000 moves in their first 4 plies, but the book has only 211 positions and 527 book moves, and 76 positions in it have two parents. So most of the games share their openings, and many differ only in move order.
- At the empty board, the center move 4 was played in 52 games, with 33 points for X. The edge move 7 was played in 59 games with 40 points, and the edge move 1 in 66 games with 35 points.
- With the leaves scored by an exact solver, the backed-up value of the empty board is 0, a draw.
- With `random.Random(99)`, 10,000 calls of BOOK-CHOOSE at the empty board give each move within 2 percentage points of its share of the weight.

A complete book of the first 4 plies of tic-tac-toe has 334 positions (those with 0 to 3 pieces) and 2,097 book moves. The same moves as a tree of move sequences would have 586 inner nodes. Every position with two pieces of the side that just moved has two parents, 1,008 positions in all. The backed-up value of the empty board is again 0.

The **learning** test starts from two games in which X opened with move 4 or move 0, each with weight 1. After a loss on the line that opens with 4, the weight of 4 becomes 1/2, after a second loss 1/4, and after a third loss 0, so X then opens with 0 in each of 200 calls. A win on the line that opens with 0 raises its weight to 3/2, and a draw changes nothing. The moves of the other side are not changed.

## Correctness

The [proof](proofs/correctness/) shows five facts:

- **One key per position.** The key after a line depends only on the position, not on the order of the moves, because XOR is associative and commutative. So transpositions share an entry. The tests check that the 5,478 positions that can arise in tic-tac-toe have 5,478 different keys with the words of the tests.
- **No cycles.** Each move adds a piece, so the book graph is a DAG.
- **Backup.** BOOK-BACKUP returns the negamax value over the book moves. The tests compare it with a plain negamax recursion over the same moves as a tree, with no sharing, on 40 random books.
- **Choice by weight.** BOOK-CHOOSE returns a move with probability equal to its share of the weight.
- **Learning.** A move whose weight falls below the floor gets weight 0 and is never chosen again.

## Complexity

In the front matter, the expected time is that of one probe, the worst time is that of one choice, and the build time is that of the backup. BOOK-PROBE is one probe of the hash table, $O(1)$ expected time. BOOK-ADD and BOOK-LEARN cost $O(h)$ for a line of $h$ plies in the book, with one XOR per move for the key. BOOK-CHOOSE costs $O(k)$ for a position with $k$ book moves. BOOK-BACKUP costs $O(v + e)$ for $v$ positions and $e$ book moves, plus the cost of leaf, when the positions are put into buckets by the number of pieces; the implementation sorts them instead, which adds $O(v \log v)$. The space is $O(v + e)$. We have no checked source for the size of real chess books, so we give none.

## Variants

- **Hand-made books.** Entries come from opening theory, with moves marked as good, playable or bad, and weights set by hand.
- **Books from game records.** As in the example: moves from a large set of games, weighted by how often and how well they were played.
- **Searched books.** The program searches each book position offline and keeps the moves whose search value is close to the best.
- **Books with backed-up values.** Buro (1999) keeps the games of the Othello program Logistello as a graph, backs up negamax values over it, and adds a best new move at positions in the book, so that the program can leave the book at a good place and does not lose the same way twice.
- **Book learning.** Hyatt (1999) changes the weights of the book moves of Crafty after its own games, from the result and from the search score just after the book.
- **Learned openings.** A program can also learn openings with no book at all, from its own search, for example with [Monte Carlo tree search](/monte-carlo-tree-search/) and self-play.

## When to use it

Use a book when the opening of a game has been studied far better than a program can search it in the time of a move, and when a program must vary its play so that an opponent cannot exploit one fixed line. Do not use a book in a game with no known theory, or in a game so small that a [solved game](/solved-game/) table or a full search covers it. In the endgame the matching structure is the [endgame tablebase](/endgame-tablebase/), which is exact, while a book is only as good as the games it came from.

## Pitfalls

- **Keys by move sequence.** A book keyed by the moves misses transpositions and stores the same position many times.
- **Missing state in the key.** In chess the key must include the side to move, castling rights and the en passant square; two boards that look equal with different rights are different positions.
- **Leaving the book in a bad place.** A book move can lead to a position that the program does not understand. Backed-up values and learning from the score after the book help.
- **Bad moves from many games.** A move that was played often is not always good. Weights from frequency alone repeat the errors of the games.
- **Learning from noise.** A loss can come from a later mistake, not from the opening. The floor and the factors in the rule above are arbitrary, and they decide how fast a move leaves the book.
- **Hash collisions.** Two positions with the same key would share moves, and a book move could be illegal in the real position. Check the legality of a book move before playing it.

## Implementations

## History

Opening books are as old as chess programs, and the early history is program practice that we have not checked in a primary source. Zobrist (1970) gave the hash that books and [transposition tables](/transposition-table/) use as their key. Hyatt (1999) described book learning in Crafty, and Buro (1999) described a book with negamax backup and automatic extension for the Othello program Logistello.

## References
