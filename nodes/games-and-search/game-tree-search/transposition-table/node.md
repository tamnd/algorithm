---
tag: 25X300
kind: data-structure
slug: transposition-table
name: Transposition table
aliases:
- transposition cache
area: games-and-search/game-tree-search
level: core
summary: Hash table of earlier search results keyed by position, so a position reached by another move order is not searched again. Each entry keeps a depth, a bound flag and a best move.
model: word-ram
complexity:
  vars: {k: the number of index bits (the table has 2^k slots)}
  time: {worst: O(1)}
  space: {extra: Θ(2^k)}
prereqs: [alpha-beta-pruning, zobrist-hashing, hash-table]
see_also: [mtdf, principal-variation-search, iterative-deepening-search, move-ordering, memoization, hash-collision, parallel-alpha-beta, proof-number-search]
sources:
  - url: http://digital.library.wisc.edu/1793/57624
    title: Albert L. Zobrist, A new hashing method with application for game playing, Technical Report 88, Computer Sciences Department, University of Wisconsin, April 1970
    locator: the whole report (the hash of a position by XOR of random numbers, and its use as the key of a table of positions)
  - paper: "Richard D. Greenblatt, Donald E. Eastlake and Stephen D. Crocker, The Greenblatt chess program, AFIPS Fall Joint Computer Conference 31 (1967), pp. 801 to 810"
    title: Greenblatt, Eastlake and Crocker 1967
    locator: the description of the hash table of positions in the search
  - book: isbn:9780387908151
    title: David J. Slate and Lawrence R. Atkin, CHESS 4.5, the Northwestern University chess program, in Peter W. Frey (ed.), Chess Skill in Man and Machine, Springer
    locator: pp. 82 to 118 (the transposition table of CHESS 4.5 and its use with iterative deepening)
  - paper: "Dennis M. Breuker, Jos W. H. M. Uiterwijk and H. Jaap van den Herik, Replacement schemes for transposition tables, ICCA Journal 17(4) (1994), pp. 183 to 193"
    title: Breuker, Uiterwijk and van den Herik 1994
    locator: the whole paper (replacement by depth, by size of the subtree and always, measured in chess)
  - paper: "Akihiro Kishimoto and Martin Müller, A general solution to the graph history interaction problem, Proceedings of AAAI 2004, pp. 644 to 649"
    title: Kishimoto and Müller 2004
    locator: Sections 1 and 2 (why a value stored for a position can be wrong when the value depends on the path)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition, Pearson (2020)
    locator: Chapter 5 (transpositions and the transposition table in alpha-beta search)
---

A transposition table is a hash table that a game-tree search uses to remember what it has found about positions. In most games the same position can come from different move orders, for example 1. e4 e5 2. Nf3 and 1. Nf3 e5 2. e4 in chess, so the [game tree](/game-tree/) contains many copies of the same subtree. The table is keyed by a [Zobrist hash](/zobrist-hashing/) of the position. Each entry stores the remaining depth of the search, the value, a flag that tells whether the value is exact or only a lower or upper bound, and the best move. Before [alpha-beta](/alpha-beta-pruning/) searches a position, it looks up the entry. A deep enough entry can give the result at once, and otherwise its best move is tried first. The flag is not optional: after a cutoff, alpha-beta knows only a bound, and a bound stored as an exact value gives wrong results.

## In plain words

When you search a game, you meet the same position many times, because the players can reach it in different orders. So you keep a notebook. After you study a position, you write down what you learned and which move looked best.

Next time you meet the position, you open the notebook first. Often the note tells you enough, and you skip the work.

Be careful what you write. Many times the search stops early, because it already knows that the position is good enough or bad enough. Then you know only "at least this much" or "at most this much". If you write such a result as the true score, a later look at the notebook trusts a wrong number.

The notebook has a fixed number of pages, so new notes push out old ones.

## The abstract type

A transposition table is a lossy map from positions to search results. For a position $p$, the result of a search of $p$ to remaining depth $d$ is a tuple (depth $d$, flag, value $v$, move). With $V_d(p)$ the [negamax](/negamax/) value of $p$ searched to depth $d$, the flag says that $V_d(p) = v$ (EXACT), $V_d(p) \ge v$ (LOWER) or $V_d(p) \le v$ (UPPER). The operations are:
- `probe(T, p)`: return a stored result for $p$, or NIL.
- `store(T, p, d, flag, v, move)`: record a result for $p$.

Unlike a [dictionary](/dictionary/), the table may forget a result at any time. A probe after a store can return NIL. The search must stay correct when this happens, and it does, since a missing entry only costs work.

## Representation

The table is an array of $2^k$ slots. A position $p$ has a key $Z(p)$ of 64 bits, made by [Zobrist hashing](/zobrist-hashing/), and its slot is $Z(p) \bmod 2^k$, which is the low $k$ bits of the key. A slot holds one entry $(z, d, f, v, x)$: the full key $z$, the depth $d$, the flag $f$, the value $v$ and the best move $x$. There is no list per slot and no probing of other slots: when two positions share a slot, one of them loses its entry. The full key in the entry tells the two positions apart, so a probe never returns the entry of the other position. Many programs store only the high bits of the key, since the low $k$ bits are already given by the slot.

The table keeps this invariant:
- **(T1) Placement.** An entry with key $z$ is in slot $z \bmod 2^k$.
- **(T2) Truth.** An entry $(z, d, f, v, x)$ is about the position $p$ with $Z(p) = z$, and $V_d(p) = v$ if $f$ is EXACT, $V_d(p) \ge v$ if $f$ is LOWER, and $V_d(p) \le v$ if $f$ is UPPER.

## Operations

TT-PROBE reads one slot. TT-STORE writes one slot, here with the *depth-preferred* policy: it keeps an entry of another position that holds a deeper search. SEARCH is fail-soft [alpha-beta](/alpha-beta-pruning/) in negamax form with the table.

```pseudo id=main
TT-PROBE(T, z)
L1  e ← T.slot[z mod 2^k]
L2  if e ≠ NIL and e.key = z then return e
L3  return NIL

TT-STORE(T, z, d, f, v, x)
L4  e ← T.slot[z mod 2^k]
L5  if e ≠ NIL and e.key ≠ z and e.depth > d then return   ▷ keep the deeper entry
L6  T.slot[z mod 2^k] ← (z, d, f, v, x)

SEARCH(p, d, α, β)
L7  e ← TT-PROBE(T, Z(p))
L8  if e ≠ NIL and e.depth ≥ d then
L9      if e.flag = EXACT, or e.flag = LOWER and e.value ≥ β, or e.flag = UPPER and e.value ≤ α, then return e.value
L10 if d = 0 or p is terminal then
L11     v ← EVALUATE(p); TT-STORE(T, Z(p), d, EXACT, v, NIL); return v
L12 if e ≠ NIL then put the move e.move first
L13 m ← −∞; best ← NIL
L14 for each move x of p, giving the child c, in order, do
L15     t ← −SEARCH(c, d − 1, −β, −max(m, α))
L16     if t > m then m ← t; best ← x
L17     if m ≥ β then break
L18 if m ≤ α then f ← UPPER else if m ≥ β then f ← LOWER else f ← EXACT
L19 TT-STORE(T, Z(p), d, f, m, best)
L20 return m
```

Line L9 uses an entry only when it decides the result: an exact value, a lower bound that already reaches $\beta$, or an upper bound that is already at most $\alpha$. A bound that does not decide the result still gives the best move in line L12. Line L18 is where the flag comes from. A result at most $\alpha$ means that every move failed low, so the true value is at most $m$. A result at least $\beta$ came from a cutoff, so the true value is at least $m$. Only a result strictly inside the window is exact. The *always-replace* policy drops line L5 and writes every new entry.

## Example

The game graph has 10 positions. In the MAX view, MAX moves at R, P and Q, and MIN moves at Y and C. R has the moves to Y and to a terminal position worth 3. Y has the moves to P and Q. P has the moves to a terminal worth 5 and to C. Q has the moves to C and to a terminal worth 2. C has the moves to terminals worth 4 and 1. So C is reached by two move orders, through P and through Q. The values are $C = 1$, $P = 5$, $Q = 2$, $Y = \min(5, 2) = 2$ and $R = \max(2, 3) = 3$.

The search goes R, Y, P. At P the first move gives 5, so MAX at P has $\alpha = 5$. At C the first move gives 4, which is not more than 5, so MIN has a cutoff, and C returns 4. This 4 says only that C is worth at most 4 to MAX. In negamax form C returns $-4$ with the window $(-\infty, -5)$, so line L18 stores it as LOWER: C is worth at least $-4$ to MIN, the side to move.

Then the search goes to Q, with the window $(-\infty, 5)$ for MAX, and the first move of Q goes to C again. The probe finds the entry. For C the window is $(-5, +\infty)$, and a LOWER bound of $-4$ does not reach $+\infty$, so line L9 does not use it. The search of C runs again with its stored move first, finds both moves, and stores C as EXACT with the value 1, or $-1$ for MIN. Q is worth $\max(1, 2) = 2$, Y is worth 2, and R is worth 3, which is correct.

If line L18 always set EXACT, the probe at Q would return 4 for C. Then Q would be worth $\max(4, 2) = 4$, Y would be worth $\min(5, 4) = 4$, and R would be worth $\max(4, 3) = 4$, which is wrong. The test file checks both results, and also checks that the entry for C after the search of P alone is the LOWER bound $-4$.

On tic-tac-toe from the empty board, fail-soft alpha-beta without a table visits 18297 nodes. With a table of $2^{16}$ slots and the keys of the test, it visits 4858 nodes, and both give the value 0, a draw. The tests check these counts.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). It shows that every call keeps (T2), and that SEARCH returns a fail-soft result for its window, as on the [alpha-beta](/alpha-beta-pruning/) page: a result $r \le \alpha$ is an upper bound on the true value, a result $r \ge \beta$ is a lower bound, and a result inside the window is exact. So the full window gives the exact value. Lines L7 to L9 are correct because a deciding entry satisfies the same three cases, by (T2). Lines L18 and L19 keep (T2) because the flag records the case of the result. Dropping entries does not break the proof, so the replacement policy affects only the work.

The proof needs three conditions. The key must be one-to-one on the positions that the search meets. The value of a position must not depend on the path to it. And line L8 uses an entry of depth $e \ge d$ as if it were of depth $d$, so $V_e(p)$ and $V_d(p)$ must be equal. This last condition holds when every path to a position has the same length, or when the search goes to the end of the game. Programs that search to a fixed depth break it on purpose, because a deeper result is better information. The result is then a mix of depths and not exactly $V_d$ of the root.

## Complexity

| operation | time | space |
|---|---|---|
| TT-PROBE | $O(1)$ | |
| TT-STORE | $O(1)$ | |
| table | | $\Theta(2^k)$ entries of $O(1)$ words |

These bounds are on the [word RAM](/word-ram/) with a key of one word. The key of a child costs $O(1)$ from the key of its parent, by the update rule of [Zobrist hashing](/zobrist-hashing/).

The effect on the search depends on the game. With the full window and no lost entries, every result is exact, and each position is expanded at most once, as in [memoization](/memoization/). So the work is linear in the number of positions and moves of the game graph, not in the size of the tree. With the narrow windows of alpha-beta, a position can be searched again when its stored bound does not decide the new window. The best move from the table often gives the [move ordering](/move-ordering/) that alpha-beta needs, and with [iterative deepening](/iterative-deepening-search/) the moves from the last iteration order the next one.

## Variants

- **Replacement policies.** Always replace, depth-preferred, or prefer the entry whose subtree had more nodes. Breuker, Uiterwijk and van den Herik compared such policies in chess.
- **Two-level tables and buckets.** Each slot has two entries, one kept by depth and one always replaced. Or the slot is a bucket of 4 entries that share a cache line, and the store replaces the least useful one.
- **Aging.** An entry from an earlier move of the game is replaced first, because its position is less likely to come back.
- **Partial keys.** The entry stores only the bits of the key that are not used for the index, to save space. This makes false matches more likely.
- **Tables for other searches.** [MTD(f)](/mtdf/) keeps both a lower and an upper bound per position. [Proof-number search](/proof-number-search/) stores proof and disproof numbers. [Monte Carlo tree search](/monte-carlo-tree-search/) on a graph merges the statistics of transpositions.
- **Shared tables.** In [parallel alpha-beta](/parallel-alpha-beta/) the threads share one table. In a lockless form, the entry stores the XOR of its key and its data, so a write that another thread interrupts fails the key check.

## When to use it

Use a transposition table in every alpha-beta search of a game where transpositions are common, such as chess, checkers, Go or Connect Four. With iterative deepening it pays even in games with few transpositions, because of the stored best move. It does not help in a tree without transpositions and without iterative deepening, where each probe is a miss.

## Pitfalls

- **Storing a bound as exact.** This is the error of the example. Store the flag from line L18, and use an entry only as line L9 does.
- **Using the entry at the wrong depth.** An entry from a shallower search, with depth less than $d$, must not decide the result. Its move can still be tried first.
- **Path dependence.** If the value depends on the history, as with a draw by repetition or the fifty-move rule in chess, the same key can need different values. This is the graph history interaction problem. Kishimoto and Müller give a general fix for it.
- **Hash collisions.** Two positions with the same 64-bit key look like one. The chance is small but not zero, so a program must check that the stored move is legal before it plays it. See [hash collision](/hash-collision/) and the [birthday paradox](/birthday-paradox/).
- **Mate scores.** A score such as "mate in $k$ moves" counts from the root. Store it as a distance from the position and convert it back at the probe, or the score is wrong when the position is reached at another ply.
- **Missing state in the key.** The key must include the side to move, castling rights and the en passant square, or two different positions get the same entry.

## Implementations

The Python version takes the moves, the evaluation and the key as functions. `use_flags=False` stores every result as exact, so the tests can show the error of the example. The tests compare the result with plain negamax on tic-tac-toe, on Nim and on random layered game graphs, with tables from 4 to 65536 slots and both policies.

## History

Greenblatt, Eastlake and Crocker described a hash table of positions in the chess program Mac Hack VI in 1967. Zobrist (1970) gave the hashing method that made such tables cheap and safe, and proposed the table of positions for game playing. Slate and Atkin (1977) described the table of CHESS 4.5 together with iterative deepening, and the use of the stored best move to order the next iteration. Breuker, Uiterwijk and van den Herik studied replacement schemes in the 1990s. Later work, such as that of Kishimoto and Müller (2004), treated the graph history interaction problem.

## References
