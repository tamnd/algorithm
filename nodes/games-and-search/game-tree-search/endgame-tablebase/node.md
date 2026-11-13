---
tag: Q9YYTV
kind: data-structure
slug: endgame-tablebase
name: Endgame tablebase
aliases:
- tablebase
- endgame database
area: games-and-search/game-tree-search
level: advanced
summary: Precomputed table giving the exact outcome of every position with few remaining pieces.
model: word-ram
complexity:
  vars: {v: the number of positions of the endgame up to symmetry, e: the number of moves between them}
  time: {worst: O(1), build: O(v + e)}
  space: {extra: O(v)}
prereqs: [retrograde-analysis, winning-losing-states, perfect-hashing]
see_also: [endgame-solving, solved-game, opening-book, transposition-table, zobrist-hashing, minimal-perfect-hashing, huffman-coding, alpha-beta-pruning]
sources:
  - paper: doi:10.3233/ICG-2000-23304
    title: Eugene V. Nalimov, Guy McC. Haworth and Ernst A. Heinz, Space-efficient indexing of chess endgame tables, ICGA Journal 23(3) (2000)
    locator: pp. 148 to 162 (index functions that use the symmetries of the board, the 462 placements of the two kings in pawnless endgames, and the index of the Nalimov tables)
  - paper: doi:10.3233/ICG-1986-9302
    title: Ken Thompson, Retrograde analysis of certain endgames, ICCA Journal 9(3) (1986)
    locator: pp. 131 to 139 (tables of chess endgames with up to five pieces built by retrograde analysis)
  - url: https://www.chessprogramming.org/Syzygy_Bases
    title: Chess Programming Wiki, Syzygy Bases
    locator: the introduction and the table of sizes (WDL and DTZ tables by Ronald de Man from 2013; the 7-piece tables by Bojun Guo in 2018, 8.5 TiB of WDL and 8.3 TiB of DTZ, 16.7 TiB in all; 149.2 GiB for 6 pieces and 939.0 MiB for 3 to 5 pieces)
  - url: https://www.chessprogramming.org/Lomonosov_Tablebases
    title: Chess Programming Wiki, Lomonosov Tablebases
    locator: the introduction (DTM tables by Vladimir Makhnychev and Victor Zakharov at Lomonosov Moscow State University; the 4+3 tables completed in July 2012 and the 5+2 tables in August 2012)
---

An endgame tablebase is a table that stores the exact value of every position of one endgame, for example all positions with a white king, a white rook and a black king. A program *probes* it during play: it turns the position into an index, reads one entry and gets the result with perfect play, win, draw or loss, and often the distance to the end, such as the distance to mate. The table is built once, offline, by [retrograde analysis](/retrograde-analysis/). The data structure has three parts. An *index function* maps each position to a number, and it uses the symmetries of the board so that positions that are mirror images share one entry. An *encoding* packs the value and the distance into a few bits. A *compression* scheme makes the table small enough to store, and it keeps blocks that can be read on their own. The tables of chess are large: the Syzygy tables for all endgames with up to 7 pieces take 16.7 TiB, according to the Chess Programming Wiki.

## In plain words

In an endgame with only a few pieces left, a computer can work out every possible position once, and write the answer for each in a big table. During a game, the program does not need to think: it looks up the position and reads off "White wins in 13 moves" or "draw".

Two ideas make the table small. A position and its mirror image have the same answer, so only one of them is stored. And the table is packed tightly, with each answer in a few bits, and the whole table compressed in blocks.

The answer is exact, not a guess. That is the main difference from an [opening book](/opening-book/), which only stores the moves that have been played before.

## The abstract type

A tablebase $T$ for an endgame $S$ supports two operations:

- TB-BUILD$(S)$: compute the value and the distance of every position of $S$, and store them.
- TB-PROBE$(T, p)$: for a legal position $p$ of $S$, return its value for the side to move and its distance.

The values are those of the game with perfect play by both sides. The distance depends on the *metric* of the table: distance to mate (DTM), to conversion into another endgame (DTC), or to the next capture or pawn move (DTZ), or no distance at all (WDL, only the value).

## Representation

**The index.** A position is mapped to a number in $[0, M)$. The plain index lists the square of each piece and the side to move, $64^k \cdot 2$ entries for $k$ pieces on a chess board. A better index removes what cannot happen and what is repeated:

- **Symmetry.** Without pawns, the 8 maps of the board onto itself (rotations and reflections) keep the rules, so each position has up to 8 images with the same value. With pawns, which move in one direction, only the left-right mirror keeps the rules. Castling is left out of the tables.
- **The two kings.** The kings are placed first, as a pair, and the pair is reduced by symmetry. The kings may not stand on one square or next to each other. On the 8 by 8 board this leaves 462 classes of king placements without pawns (Nalimov, Haworth and Heinz, 2000), and 1,806 with only the mirror. The tests count these classes.
- **The other pieces.** Each other piece adds a factor for its square, and equal pieces can be counted as a set rather than in order.

The best indexes are close to a [perfect hash](/perfect-hashing/) of the legal positions, but they stay simple enough to compute in a few steps.

**The entries.** Each entry packs the value and the distance. A WDL entry needs 2 bits or less; a DTM entry needs a byte or more.

**Compression.** Tables are split into blocks, each block is compressed on its own, and a small directory gives the start of each block. A probe decompresses one block. Entries that do not matter, such as illegal positions or positions with a capture that a program would find anyway, can be set to whatever value compresses best. The real schemes differ between the table formats, and we do not describe them here.

The implementation here is a toy: king and rook against king on a 4 by 4 board, with no other pieces, no castling and no move counter. It is not chess. A stalemate and the capture of the rook are draws.

## Operations

```pseudo id=main
TB-INDEX(p)
L1  p' ← the least of the 8 images of p, comparing the pair of kings first, then the rook
L2  return (CLASS(king pair of p') · 16 + rook square of p') · 2 + side to move

TB-BUILD(S)
L3  run RETROGRADE on the classes of S: the children of a class are the classes of the children of its representative
L4  for each class c with value x and distance d: T[TB-INDEX(c)] ← CODE(x, d)

TB-PROBE(T, p)
L5  b ← T[TB-INDEX(p)]
L6  return DECODE(b)
```

CLASS numbers the classes of the legal king pairs, here the 21 classes on the 4 by 4 board. CODE stores a draw as 1 and a win or loss in $d$ plies as $2 + 2d$ plus 1 for a win, so one byte holds every entry of the toy; 0 marks an unused entry. Line L3 is the [retrograde analysis](/retrograde-analysis/) of the class graph. Its counter counts the distinct child classes of a class, and the predecessors of a class are found from all positions in its orbit, since a move into any of them is a move into the class.

## Example

The toy has 3,496 legal positions. They fall into 443 classes under the 8 symmetries, about 7.9 positions per class. The table has $21 \cdot 16 \cdot 2 = 672$ bytes, against $16 \cdot 16 \cdot 16 \cdot 2 = 8{,}192$ for the plain index, and 443 of its entries are used. Of the classes, 167 are won for the side to move, 198 lost and 78 drawn.

A probe of White Ka1, Rd2 against Black Kc3, White to move, returns "win in 13 plies". The 7 other images of this position, for example White Kd4, Ra3 against Black Kb2, return the same entry, because they have the same index.

The tests also build the table for a variant in which the white king may not move. Then White cannot always force a mate. With White to move, 368 positions are won and 944 are draws, and none of these draws has a move out of the endgame, so they are draws by endless play: neither side can force a mate, and the play can go on for ever.

## Correctness

The [proof](proofs/correctness/) has four steps:

- **The rules are symmetric.** The 8 maps keep king steps, rook lines and the first piece on each line, so they keep legality, moves and mate.
- **So are the values.** A map takes the sets of positions won or lost within $n$ plies onto themselves.
- **The index is well defined.** The least image of a position is the same for all its images, so all images share one index, and different classes get different indexes.
- **Probes are exact.** Retrograde analysis on the classes gives the same values and distances as on the positions, and the code is one to one.

The tests compare every probe with a forward computation of the won and lost sets on all 3,496 positions, with no use of symmetry, for the toy and for the variant. They check that the 8 images of every position get the same index and entry, that UNMOVES inverts MOVES, and that the distances are exact: a win is one more than the shortest loss among its moves, and a loss one more than the longest win.

## Complexity

**Probe.** TB-INDEX tries the 8 maps and does a few arithmetic steps, so TB-PROBE takes $O(1)$ time for a fixed number of pieces, plus the time to decompress one block in a compressed table.

**Build.** TB-BUILD takes $O(v + e)$ steps for $v$ classes and $e$ moves between them, as retrograde analysis does, with $O(1)$ work per step for the symmetries.

**Space.** One entry per index value, $O(v)$, before compression. The index of the toy wastes the entries of 229 of its 672 values.

**Real sizes.** The Chess Programming Wiki gives these sizes for the Syzygy tables: 939.0 MiB for 3 to 5 pieces, 149.2 GiB for 6 pieces, and for 7 pieces 8.5 TiB of WDL tables and 8.3 TiB of DTZ tables, 16.7 TiB in all. The tests build only the toy table of 672 bytes.

## Variants

- **Nalimov tables.** DTM tables with the index of Nalimov, Haworth and Heinz (2000), long used by chess programs for endgames with up to 6 pieces.
- **Syzygy tables.** Tables by Ronald de Man, from 2013, in two parts: WDL tables, small and fast, for the probes in the search, and DTZ tables for the moves at the root. They take the fifty-move rule into account. Bojun Guo built the 7-piece tables in 2018.
- **Lomonosov tables.** DTM tables by Vladimir Makhnychev and Victor Zakharov at Lomonosov Moscow State University. The Chess Programming Wiki dates the 4+3 tables to July 2012 and the 5+2 tables to August 2012.
- **Bit bases.** Tables with only one bit per position, such as "won for White or not", for use deep in the search.
- **Other games.** The same structure holds the endgame databases of checkers and the full table of awari; see [solved game](/solved-game/).

## When to use it

Use a tablebase when an endgame is small enough to store and is reached often, in play or in the search. In the search, a WDL probe replaces a whole subtree of [alpha-beta](/alpha-beta-pruning/) by an exact value. At the root, a DTM or DTZ probe gives a move that makes progress. For an endgame too large to store, solve single positions with a forward search instead; see [endgame solving](/endgame-solving/).

## Pitfalls

- **Wrong symmetry.** With pawns, only the left-right mirror is a symmetry. Using all 8 maps gives wrong values.
- **Metric and rules.** A DTM table ignores the fifty-move rule, so a "win" in it may be a draw under the rule. A DTZ table respects the rule, but its distance is not the distance to mate.
- **Playing by WDL alone.** Moves that keep a won position won do not always make progress. A program that plays by WDL alone can go round in circles; it needs a distance.
- **Castling and en passant.** Tables leave out castling rights, and en passant needs care in the index. A position with castling rights is not in the table.
- **Disk and memory.** A probe deep in the search can cost a disk read. Programs probe only some nodes, or keep the small WDL tables in memory.

## Implementations

## History

Ströhlein's 1970 doctoral thesis built the first chess endgame tables, as described on the page on [retrograde analysis](/retrograde-analysis/). Thompson (1986) built tables of chess endgames with up to five pieces. Nalimov, Haworth and Heinz (2000) gave the index functions of the Nalimov tables. The Lomonosov DTM tables for seven pieces were finished in 2012, and the Syzygy tables of Ronald de Man, first released in 2013, reached seven pieces in 2018, according to the Chess Programming Wiki.

## References
