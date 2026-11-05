---
tag: ZSM42R
kind: technique
slug: zobrist-hashing
name: Zobrist hashing
aliases:
- Zobrist keys
area: searching/hashing-search
level: core
summary: Incrementally updatable hash of a board position using XOR of random keys.
prereqs: [hash-function, hash-table, game-tree]
see_also: [transposition-table, tabulation-hashing, alpha-beta-pruning, minimax, monte-carlo-tree-search, birthday-paradox, universal-hash-family, endgame-tablebase]
sources:
  - url: http://digital.library.wisc.edu/1793/57624
    title: Albert L. Zobrist, A new hashing method with application for game playing, Technical Report 88, Computer Sciences Department, University of Wisconsin, April 1970
    locator: the whole report (the XOR of random numbers per piece and square, its incremental update, and its use for a table of positions)
  - paper: doi:10.3233/ICG-1990-13203
    title: Albert L. Zobrist, A new hashing method with application for game playing, ICCA Journal 13(2) (1990)
    locator: pages 69 to 73 (reprint of the 1970 report, with a note of the editors)
  - paper: doi:10.1145/2220357.2220361
    title: Mihai Patrascu and Mikkel Thorup, The power of simple tabulation hashing, Journal of the ACM 59(3) (2012)
    locator: Section 1 (simple tabulation, its origin in the method of Zobrist, and its 3-independence)
---

Zobrist hashing is a technique for hashing a state that is a set of features, such as a board position seen as the set of (piece, square) pairs, by giving each possible feature a random $b$-bit word and taking the XOR of the words of the features present. Because XOR is its own inverse, a move that adds or removes a few features changes the hash by a few XORs, so the hash of each new position costs $O(1)$ time instead of a scan of the board. Two different positions get the same hash with probability $2^{-b}$, which makes the hash a safe key for a [transposition table](/transposition-table/) in game-tree search. Albert Zobrist described the method in a 1970 technical report, and it is the origin of [tabulation hashing](/tabulation-hashing/).

## In plain words

Give every possible "fact" about a board its own random number: "white knight on g1" gets one, "black pawn on e5" gets another, "white to move" gets another. The fingerprint of a position is all the numbers of its true facts combined with exclusive or.

Exclusive or has a handy property: doing it twice with the same number undoes it. So when a knight moves from g1 to f3, you remove "knight on g1" and add "knight on f3" by two quick operations on the old fingerprint. You never look at the rest of the board. Two different positions almost never get the same fingerprint, because their facts differ in at least one random number. Positions reached by different move orders get the same fingerprint, which is exactly what a search wants to notice.

## When it applies

- The state is a set of features from a fixed finite list, and two states are equal exactly when they have the same features. Board positions, sets of flags and sets of items fit this.
- States change by small steps that add or remove a few features, and the hash of each new state is needed: game-tree search, local search, and simulations that revisit states.
- A table keyed by states must detect repeats, and a rare false match is acceptable, or is checked by a cheap test of the move or of the full state.
- It does not apply directly when the order of the features matters, as in a string; there the position is part of the feature, or a [rolling hash](/rabin-karp/) is the better tool.

## The template

```pseudo id=main
ZOBRIST-INIT(F, b)                      ▷ F: the list of all features; hole: what a feature is
L1  for each feature f in F do
L2      Z[f] ← a random b-bit word        ▷ hole: the source of randomness and b, often 64

ZOBRIST-HASH(P)                         ▷ from scratch, once
L3  H ← 0
L4  for each feature f present in P do
L5      H ← H ⊕ Z[f]
L6  return H

ZOBRIST-UPDATE(H, removed, added)       ▷ after each move
L7  for each f in removed ∪ added do
L8      H ← H ⊕ Z[f]
L9  return H

TABLE-INDEX(H, k)                       ▷ hole: how the hash is split
L10 return the low k bits of H as the slot, and the other b − k bits as the check stored in the slot
```

**The holes.** The feature list decides what counts as equal. For chess it is the 768 pairs of 12 piece kinds and 64 squares, plus features for the side to move, each castling right and each en passant file. Leave out a feature, such as the side to move, and two different positions get the same hash for sure. The word size $b$ sets the collision rate. The split of line L10 uses the low bits as an index into a table of $2^k$ slots and keeps the rest to check a hit.

**Why the update is right.** XOR is associative and commutative, and $Z[f] \oplus Z[f] = 0$. The hash of a position is $\bigoplus_{f \in P} Z[f]$. If the move turns $P$ into $P' = (P \setminus R) \cup A$ with $R \subseteq P$ and $A \cap (P \setminus R) = \emptyset$, then XOR with the words of $R$ cancels them, and XOR with the words of $A$ adds them, so lines L7 and L8 give $\bigoplus_{f \in P'} Z[f]$, the value that ZOBRIST-HASH computes from scratch. The order of the moves does not matter, so positions reached by different move orders get the same hash.

**Why collisions are rare.** Let the words $Z[f]$ be independent and uniform on $\{0,1\}^b$. For two different positions $P \ne Q$, $H(P) \oplus H(Q) = \bigoplus_{f \in P \triangle Q} Z[f]$, the XOR over the features in exactly one of them. This set is not empty, and the XOR of a nonempty set of independent uniform words is uniform. So $\Pr[H(P) = H(Q)] = 2^{-b}$. Among $N$ distinct positions met in a search, the expected number of colliding pairs is $\binom{N}{2} 2^{-b}$, by [linearity of expectation](/linearity-of-expectation/); this is the [birthday paradox](/birthday-paradox/) bound.

**Cost.** Initialization stores $|F|$ words. A hash from scratch takes $O(|P|)$ XORs; an update takes $O(|R| + |A|)$, which is $O(1)$ for a chess move (2 features for a quiet move, up to about 6 with a capture, castling rights and the side to move).

## Classic examples

- **[Transposition tables](/transposition-table/) in chess programs.** The search of a [game tree](/game-tree/) by [alpha-beta pruning](/alpha-beta-pruning/) or [negamax](/negamax/) meets the same position along many move orders. A table indexed by the Zobrist hash stores the value, depth and best move of each searched position, and the 64-bit hash is updated with each move made and unmade in the search. This is the use Zobrist designed the method for.
- **Go and Monte Carlo tree search.** In [Monte Carlo tree search](/monte-carlo-tree-search/) for Go, the nodes of the search tree are shared through a hash table on Zobrist keys, and the same keys detect the repetition of a whole-board position, which the superko rule forbids.
- **Repetition detection.** A chess program keeps the hashes of the positions on the current path and since the last capture or pawn move, and checks a new hash against them to detect a draw by repetition, without comparing boards.
- **[Endgame tablebases](/endgame-tablebase/) and [retrograde analysis](/retrograde-analysis/).** Programs that enumerate positions use Zobrist keys to index or to check positions when a perfect index is not used.
- **Simple tabulation hashing.** Hashing a key of $c$ characters as $T_1[x_1] \oplus \cdots \oplus T_c[x_c]$, with one random table per character position, is Zobrist hashing with the features "character $a$ at position $i$". Patrascu and Thorup analyze it under the name [tabulation hashing](/tabulation-hashing/) and show that it is 3-independent and strong enough for linear probing and cuckoo hashing.

## Variations

- **Word size.** 32-bit keys collide too often for searches of $10^8$ positions; 64-bit keys are the standard; some programs use 128 bits or store extra check bits in each table entry.
- **Feature sets for parts of the board.** Programs keep separate Zobrist keys for the pawn structure only, or for the material only, to cache evaluations that depend only on that part. These keys are updated with the same XORs, restricted to the features of the part.
- **Additive variant.** Addition modulo $2^b$ instead of XOR also allows updates, with subtraction for a removed feature. It keeps the same counting argument, but it needs a subtraction for each removal and has no advantage in practice.
- **Hashing multisets.** If a feature can occur twice, XOR cancels the pair, so two copies hash like none. Use a feature per count ("two pawns of this kind on this file"), or the additive variant, which counts multiplicities.
- **Fixed keys.** Some programs, such as those that share opening books, use a fixed published table of keys so that hashes agree between programs. The keys are random once and then constant, so the guarantee holds for positions that do not depend on the table.

## Pitfalls

- **Missing features.** If the side to move, castling rights or the en passant file are not features, positions that differ only in them get the same hash with certainty, and the search reuses wrong values.
- **Bad random words.** A word of 0, two equal words, or words from a weak generator with few independent bits make the XOR of some small set of features vanish, which gives systematic collisions. Use a good generator. Note also that more than $b$ words are always linearly dependent over $\mathbb{F}_2$ (chess uses about 780 words of 64 bits), so some nonempty sets of features have XOR 0. The guarantee is only that a fixed pair of positions collides with probability $2^{-b}$, not that no pair does.
- **Index bits are not check bits.** If a table of $2^k$ slots uses the low $k$ bits as the index and stores only those same bits as a check, the check adds nothing. Store the other bits, or the whole key.
- **Trusting a hit blindly.** With 64-bit keys and $10^9$ positions, the expected number of colliding pairs is about $\binom{10^9}{2} 2^{-64} \approx 0.027$, but a program that probes a table a billion times with fewer check bits sees false hits. Check that the stored best move is legal before playing it.
- **Forgetting to unmake.** In a search that makes and unmakes moves, the hash must be updated in both directions. Applying the same XORs again undoes the move, so the unmake is the same code as the make.

## Exercises

1. Tic-tac-toe has the 18 features "X on cell $i$" and "O on cell $i$" for $i = 0, \ldots, 8$ (cells in reading order), plus "O to move", whose word is XORed in after each move. With the 8-bit words $Z[X_4] = \mathtt{1c}$, $Z[O_0] = \mathtt{3f}$, $Z[X_8] = \mathtt{c7}$ and $Z[\text{O to move}] = \mathtt{13}$ (in hexadecimal), and the empty board with X to move hashed as 0, compute the hash after the moves X on 4, O on 0, X on 8 by updates, and check that it equals the hash from scratch, $\mathtt{f7}$. Show that the order X on 8, O on 0, X on 4 gives the same value.
2. Prove that if the words $Z[f]$ are only pairwise independent, then two distinct positions that differ in exactly one feature still collide with probability $2^{-b}$, and find a family of words that is pairwise independent in which two positions that differ in three features always collide.
3. A table has $2^{20}$ slots and stores in each slot the high 16 bits of a 64-bit Zobrist key as a check. A search probes the table $10^9$ times, each time for a position that is not in the slot. Estimate the expected number of false hits, assuming each check matches with probability $2^{-16}$.

## References
