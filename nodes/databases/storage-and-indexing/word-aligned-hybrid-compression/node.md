---
tag: KZ8EQQ
kind: algorithm
slug: word-aligned-hybrid-compression
name: Word-aligned hybrid compression
aliases:
- WAH
- WAH bitmap compression
area: databases/storage-and-indexing
level: advanced
summary: "Compress a bitmap into literal and fill words of machine size, so that AND, OR and XOR run on the compressed form in time linear in the number of compressed words."
model: word-ram
complexity:
  vars: {N: the number of bits of a bitmap, w: "the word length in bits (32 on this page)", p: the number of words of the first operand, q: the number of words of the second operand, h: the number of set bits}
  time: {worst: "O(p + q)", average: "O(p + q)", best: "O(max(p, q))"}
  space: {extra: "O(p + q)"}
properties: {deterministic: true, exact: true, external: false, online: true, in_place: false, recursive: false}
history:
  year: 2002
  people: [Kesheng Wu, Ekow J. Otoo, Arie Shoshani]
  note: "Wu, Otoo and Shoshani introduced the word-aligned hybrid code at SSDBM 2002 as a faster alternative to byte-aligned codes. The TODS paper of 2006 gives its analysis."
prereqs: [bitmap-index, run-length-encoding, bitwise-operations]
see_also: [roaring-bitmap, bit-vector, population-count, zone-map, bit-packing, simd-within-a-register, delta-encoding, rank-select-dictionary]
sources:
  - paper: doi:10.1145/1132863.1132864
    title: "Kesheng Wu, Ekow J. Otoo and Arie Shoshani, Optimizing bitmap indices with efficient compression, ACM Transactions on Database Systems 31(1) (2006)"
    locator: "pp. 1 to 38: Section 3 (literal and fill words, the active word, Fig. 2), Section 4.1 (Lemmas 1 and 2, Theorem 3 on the number of words), Section 4.3 (Proposition 4 on the size of an index), Section 5.1 (Lemma 5, Theorem 7 on the time of the logical operations, Theorem 8 on in-place OR)"
  - paper: doi:10.1109/SSDM.2002.1029710
    title: "Kesheng Wu, Ekow J. Otoo and Arie Shoshani, Compressing bitmap indexes for faster search operations, Proceedings of the 14th International Conference on Scientific and Statistical Database Management (SSDBM 2002)"
    locator: pp. 99 to 108, the first description of WAH and its measured comparison with BBC
---

Word-aligned hybrid compression (WAH) is a form of [run-length encoding](/run-length-encoding/) for bitmaps that cuts the bitmap into groups of $w - 1$ bits and writes each group, or each run of identical groups, as one machine word. Because every word covers whole groups, a logical operation on two compressed bitmaps walks both word lists once and never decodes them bit by bit. The [bitmap index](/bitmap-index/) page shows where WAH is used and gives a short example; this page holds the full algorithm, the word count theorem and the cost proofs.

## In plain words

A long row of switches is mostly off, with a few short patches where some are on. Instead of writing every switch, cut the row into pieces of 31 switches. A piece that is all off, or all on, joins its neighbors of the same kind, and the whole stretch is written as one word that says "this many pieces, all off". A piece with a mix is written as it is, in one word.

To combine two such rows, you read both lists of words side by side. When both say "many pieces of the same kind", you can answer for all of those pieces in one step. When one of them is a mixed piece, you combine that one piece. So the work depends on how many words there are, not on how many switches.

## The problem

Input: a bitmap $X$ of $N$ bits, and for the logical operations a second bitmap $Y$ of the same length $N$ and an operation $\circ$ (AND, OR or XOR, applied bit by bit). Output: the compressed form of $X$, and the compressed form of $X \circ Y$ computed from the compressed forms of $X$ and $Y$.

The words have $w = 32$ bits; the 64-bit version uses $w = 64$ in the same way. Cut the bitmap into $M = \lfloor N / 31 \rfloor$ full *groups* of 31 bits, and a tail of $N - 31 M$ bits. On this page, as in Fig. 2 of the paper, the first bit of a group is the highest of its 31 bits.

- A *literal word* has top bit 0. Its low 31 bits are one group as it is.
- A *fill word* has top bit 1. The next bit is the *fill bit* $f$, and the low 30 bits are a count $k \ge 1$. It stands for $k$ groups of 31 copies of $f$, so $31 k$ bits.
- The *active word* holds the tail of $N - 31 M < 31$ bits, with its length. It is kept apart from the regular words.

## The algorithm

```pseudo id=main
COMPRESS(b, N)                     ▷ b is a sequence of N bits
L1  Z ← an empty list of words
L2  M ← ⌊N / 31⌋
L3  for i ← 0 to M - 1 do
L4      g ← bits 31i to 31i + 30 of b, the first bit highest
L5      APPEND-LITERAL(Z, g)
L6  active ← the last N - 31M bits of b; nbits ← N - 31M
L7  return (Z, active, nbits)

APPEND-LITERAL(Z, g)               ▷ g is one group of 31 bits
L8  if g = 0 then APPEND-FILL(Z, 0, 1)
L9  else if g = 2^31 - 1 then APPEND-FILL(Z, 1, 1)
L10 else append g to Z              ▷ a literal word
APPEND-FILL(Z, f, k)               ▷ k groups of the bit f
L11 if the last word of Z is a fill with bit f then
L12     add k to its count
L13 else append the fill word 2^31 + f · 2^30 + k to Z
```

A count has 30 bits, so it holds at most $2^{30} - 1$ groups. Lemma 1 of the paper shows that, for $w > 5$, any run of at most $2^w$ bits fits in one fill word, so a bitmap of at most $2^{32}$ bits never overflows a count. The code starts a new fill word when a count is full.

The logical operation reads both word lists from the left. RUN$(X, i)$ gives the 31-bit value of word $i$ of $X$ (31 copies of the fill bit for a fill word) and the number of groups it still covers.

```pseudo id=op
WAH-OP(X, Y, ∘)                    ▷ X and Y have the same N
L14 Z ← an empty list; i ← 0; j ← 0
L15 (x, nx) ← RUN(X, 0); (y, ny) ← RUN(Y, 0)
L16 while i < |X| and j < |Y| do
L17     k ← min(nx, ny)
L18     if word i of X and word j of Y are both fills then APPEND-FILL(Z, the bit of x ∘ y, k)
L19     else APPEND-LITERAL(Z, x ∘ y)   ▷ here k = 1
L20     nx ← nx - k; ny ← ny - k
L21     if nx = 0 then i ← i + 1; (x, nx) ← RUN(X, i)
L22     if ny = 0 then j ← j + 1; (y, ny) ← RUN(Y, j)
L23 active ← active(X) ∘ active(Y), masked to nbits
L24 return (Z, active, nbits)
```

Two fills give a fill of the shorter length in one step, whatever their counts are. A fill and a literal give one literal, and APPEND-LITERAL turns an all-0 or all-1 result back into a fill, so the output has the same form that COMPRESS would give.

## Example

**Fig. 2 of the paper.** The 128 bits are one 1, twenty 0s, three 1s, seventy-nine 0s and twenty-five 1s. So $M = 4$ groups and a tail of 4 bits.

| group | bits | word |
|---|---|---|
| 0 | 1, twenty 0s, three 1s, seven 0s | literal 0x40000380 |
| 1 and 2 | 62 zeros | fill 0x80000002 (bit 0, count 2) |
| 3 | ten 0s, twenty-one 1s | literal 0x001FFFFF |
| tail | four 1s | active word 0x0000000F, 4 bits |

The 128 bits need three regular words and the active word.

**An AND.** Let $N = 160$, so $M = 5$ and a tail of 5 bits. $X$ has the bits 70 to 159 set, and $Y$ has the bits 0 to 99 and 157 to 159 set.

- $X$ = 0x80000002 (two 0-groups), 0x007FFFFF (bits 62 to 69 are 0, bits 70 to 92 are 1), 0xC0000002 (two 1-groups), active 0x1F.
- $Y$ = 0xC0000003 (three 1-groups), 0x7F000000 (bits 93 to 99 are 1), 0x80000001 (one 0-group), active 0x07.

WAH-OP with AND takes 4 steps:

1. Fill 0 of count 2 with fill 1 of count 3: both fills, $k = 2$, append a 0-fill of 2. $X$ moves on; $Y$ has 1 group left.
2. The literal 0x007FFFFF with the rest of the 1-fill: $k = 1$, append the literal 0x007FFFFF. Both move on.
3. The 1-fill of count 2 with the literal 0x7F000000: $k = 1$, append 0x7F000000. $Y$ moves on; $X$ has 1 group left.
4. The rest of the 1-fill with the 0-fill of count 1: append a 0-fill of 1. Both lists end.

The active words give 0x1F AND 0x07 = 0x07. The result is 0x80000002, 0x007FFFFF, 0x7F000000, 0x80000001 with active word 0x07: the bits 70 to 99 and 157 to 159, 33 bits in all. OR takes 4 steps too and gives the single fill 0xC0000005 with active word 0x1F.

**Sizes.** For $N = 100\,000$ bits ($M = 3225$ groups), with bits set at random by `random.Random(1)`:

| density | set bits $h$ | counting groups that are fills $G$ | WAH words |
|---|---|---|---|
| 0.001 | 108 | 3014 | 211 |
| 0.05 | 4973 | 130 | 3095 |
| 0.5 | 49958 | 0 | 3225 |

The plain bitmap has $\lceil 100\,000 / 32 \rceil = 3125$ words. At density 0.5, WAH is about 3% larger, because each 32-bit word carries only 31 bits of data.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). In short:

- **COMPRESS is lossless.** Each full group is written exactly once, as a literal or as part of a fill with its own bit, in order, and the tail is the active word.
- **Theorem 3 of the paper (the word count).** A *counting group* is a pair of consecutive full groups, so a bitmap with $M$ groups has $M - 1$ of them. Let $G$ be the number of counting groups whose two groups are fills of the same bit. If no count overflows, COMPRESS writes exactly $M - G$ regular words. A run of $l$ fill groups of one bit gives $l - 1$ such pairs (Lemma 2) and costs one word instead of $l$.
- **WAH-OP is exact.** The loop keeps the invariant that $Z$ is the compressed form of $X \circ Y$ on all groups consumed so far, and that the words of $X$ and $Y$ in use start at the same group. Both lists cover $M$ groups, so they end together.

## Complexity

All counts are in the [word RAM](/word-ram/) with $w$-bit words.

- **COMPRESS** does $O(1)$ work per group, so $O(N / w)$ word operations if the bitmap is given in words, and the output has at most $M + 1$ words. The bound $M - G$ of Theorem 3 is exact.
- **Size and set bits.** A bitmap with $h$ set bits in its full groups has at most $2h + 1$ regular words: at most $h$ groups are not all 0, and the all-0 groups form at most $h + 1$ runs, one word each. Summed over the $c$ bitmaps of an equality-encoded [bitmap index](/bitmap-index/) on $N$ rows, this gives at most $2N + c$ regular words and $c$ active words, which is the bound of at most $4N$ words of Proposition 4 of the paper, and about $2N$ when $c$ is much smaller than $N$.
- **WAH-OP.** Each step finishes at least one word of $X$ or of $Y$, and the last step finishes both, so the loop runs at most $p + q - 1$ times. Each step covers at least one group, so it also runs at most $M$ times. Each step finishes at most one word of each operand, so it runs at least $\max(p, q)$ times. These are the bounds of Lemma 5 of the paper, and Theorem 7 follows: WAH-OP takes $O(p + q)$ time, and the result has at most $p + q$ words.
- **Against the plain bitmap.** A plain AND takes $\lceil N / w \rceil$ word operations. WAH-OP is faster when $p + q$ is well below $N / w$, which is the case for sparse bitmaps and for bitmaps with long runs, such as the bitmaps of a column that is sorted or clustered.

## Properties

- **Word-aligned.** Every word holds whole groups, so no operation shifts bits across word boundaries. This is the reason WAH is faster than byte-aligned codes, at the cost of some space.
- **Canonical form.** COMPRESS and WAH-OP give the same word list for the same bits (when no count overflows). Two compressed bitmaps are equal exactly when their word lists and active words are equal.
- **Streaming.** Both procedures read their inputs once from left to right, and an append of new bits touches only the last regular word and the active word.
- **No random access.** Testing bit $r$ needs a scan of the words up to the group of $r$, unless an extra table of offsets is kept.

## Variants and improvements

- **64-bit words.** With $w = 64$, groups have 63 bits and the count has 62 bits. Fewer words per bitmap, but a sparse bitmap gains less, because a literal now covers more bits that are mostly 0.
- **In-place OR with a sparse operand.** Theorem 8 of the paper: when $Y$ is very sparse, an OR that updates $X$ in place, with $X$ held uncompressed, takes time linear in the number of words of $Y$ only. This is how many bitmaps of a range are combined.
- **Range queries.** For one-dimensional range conditions on a WAH-compressed bitmap index, Propositions 9 and 10 of the paper argue that an OR of many sparse bitmaps with in-place OR takes time linear in the number of hits, which is optimal up to a constant. The argument assumes that the bitmaps involved are sparse, and the authors call these results propositions, not theorems, for that reason.
- **Byte-aligned codes.** The byte-aligned bitmap code (BBC) of Antoshenkov uses bytes instead of words. It compresses better, but its operations decode more cases.
- **Later word-aligned codes.** Several later codes keep the word alignment and pack a few literal bits into fill words, or store chunks in other ways. [Roaring bitmaps](/roaring-bitmap/) instead split row ids into chunks of $2^{16}$ and pick an array, a bitmap or runs per chunk, which also allows fast random access.

## When to use it

Use WAH for read-mostly bitmap indexes on columns with long runs or few set bits per bitmap, where queries combine many bitmaps with AND and OR: scientific data, star-schema dimensions and log data. If queries need random access to single bits, or if many bitmaps are dense and random, prefer an uncompressed [bit vector](/bit-vector/) or a roaring bitmap.

## Pitfalls

- **Bit order.** The paper and this page put the first bit of a group in the highest of its 31 bits. The [bitmap index](/bitmap-index/) page and many libraries put row 0 in the lowest bit. Both work, but the two sides of an operation must use the same order.
- **Forgetting the active word.** The tail of $N \bmod 31$ bits is not a regular word. An operation must combine the two active words and mask the result to the tail length, as line L23 does.
- **Operands of different lengths.** WAH-OP assumes that both bitmaps cover the same $M$ groups. Extend the shorter bitmap with a 0-fill first, or the loop stops early and drops the tail of the longer one.
- **Non-canonical output.** If APPEND-LITERAL does not turn an all-0 or all-1 group into a fill, or APPEND-FILL does not merge with the last word, the output grows. Equality tests on word lists then fail even when the bits are equal.
- **Dense random data.** At density near one half, nothing compresses, and WAH is $32/31$ times the size of the plain bitmap and slower to combine.
- **Count overflow.** A bitmap of more than $2^{30}$ groups needs more than one fill word for a long run. Then Theorem 3 counts one word less than COMPRESS writes for each extra fill word.

## Implementations

## History

Byte-aligned bitmap compression (BBC), due to Antoshenkov, was the usual code for compressed bitmap indexes in the 1990s. Kesheng Wu, Ekow Otoo and Arie Shoshani at Lawrence Berkeley National Laboratory introduced the word-aligned hybrid code at SSDBM 2002. They measured logical operations about 12 times faster than BBC, for about 60% more space, on their test data. Their TODS paper of 2006 gives the word count theorem, the size bound of a whole index and the linear time of the operations. WAH became the code of the FastBit software of that laboratory, and later codes such as roaring bitmaps were compared against it.

## References
