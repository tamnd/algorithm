---
tag: ZG8A1R
kind: algorithm
slug: unicode-normalization-algorithm
name: Unicode normalization algorithm
aliases:
- UAX 15 normalization
area: strings/text-processing-and-typesetting
level: core
summary: "Normalize a string by full decomposition, a stable sort by combining class inside each run of combining marks, and, for NFC and NFKC, a left-to-right canonical composition."
model: word-ram
complexity:
  vars: {n: the number of code points of the input}
  time: {worst: Θ(n^2), best: Θ(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: true, online: false}
prereqs: [unicode-normalization-forms, canonical-equivalence, insertion-sort]
see_also: [unicode-normalization-forms, canonical-equivalence, hangul-syllable-composition, stable-sort, counting-sort, unicode-case-folding, unicode-collation-algorithm, hash-table]
sources:
  - book: isbn:9781936213344
    title: The Unicode Consortium, The Unicode Standard, Version 16.0.0, 2024
    locator: "Chapter 3: Section 3.7 Decomposition (D65, D68), Section 3.11 Normalization Forms (3.11.5 Canonical Ordering Algorithm, D108 and D109; 3.11.6 Canonical Composition Algorithm, D110 to D117; 3.11.7 Definition of Normalization Forms, D118 to D121) and Section 3.12 Conjoining Jamo Behavior"
  - url: https://www.unicode.org/reports/tr15/
    title: Mark Davis and Ken Whistler, Unicode Standard Annex 15, Unicode Normalization Forms, revision 56
    locator: "Section 1.3 (canonical ordering and composition), Section 4 (conformance, UAX15-C1 to C5), Section 5 (composition exclusion, 5.1 and its four types), Section 9 (detecting normalization forms) and Section 13 (Stream-Safe Text Format)"
  - url: https://www.unicode.org/Public/16.0.0/ucd/CompositionExclusions.txt
    title: Unicode Character Database 16.0.0, CompositionExclusions.txt (2024-02-02)
    locator: Sections 1 to 4 (67 script-specific exclusions, 14 post composition version exclusions, 1035 singletons, 4 non-starter decompositions)
  - url: https://www.unicode.org/Public/16.0.0/ucd/NormalizationTest.txt
    title: Unicode Character Database 16.0.0, NormalizationTest.txt (2024-04-30)
    locator: The conformance test lines c1 to c5 and their invariants
---

The Unicode normalization algorithm computes the four [normalization forms](/unicode-normalization-forms/) of a string in three passes. It first replaces every code point by its full decomposition, then sorts each run of combining marks by canonical combining class with a stable sort that never moves a starter, and, for NFC and NFKC, it then composes pairs of a starter and a later mark back into precomposed characters from left to right. The data are a decomposition mapping and a combining class for each code point, a list of composition exclusions, and the arithmetic of [Hangul syllables](/hangul-syllable-composition/). Section 3.11 of the core specification defines the steps, and Unicode Standard Annex 15 explains them.

## In plain words

A letter with accents can be stored in several ways: as one ready-made letter, or as a plain letter followed by accent marks, and the marks can come in different orders. Normalization picks one of these ways, so that the same text is always stored the same way.

First, take every ready-made letter apart, all the way down to the plain letter and its marks. Second, put the marks after each letter in a fixed order. Marks that sit in different places, such as one below the letter and one above, are put in order by a number that each mark has. Marks in the same place keep their order, because there the order changes what the reader sees.

For the composed form, go through the result once more and join each letter with its marks into a ready-made letter wherever such a letter exists.

## The problem

The input is a string $X$ of $n$ code points and a form: NFD, NFC, NFKD or NFKC. The output is the string of that form that is equivalent to $X$, as D118 to D121 define it.

The data come from the Unicode Character Database:

- $\mathrm{ccc}(c)$, the canonical combining class, a number in 0..254. A *starter* has class 0.
- The decomposition mapping of $c$. It is canonical unless it starts with a tag such as `<compat>`, and the forms NFKD and NFKC also use the tagged mappings.
- The full composition exclusions (D113): the 67 script-specific and 14 post composition version exclusions that CompositionExclusions.txt lists, plus the 1,035 singletons and the 4 non-starter decompositions, which can be derived from the mappings. A primary composite (D114) is a character with a canonical mapping that is not in this set.
- PAIR$(a, b)$: the primary composite whose canonical mapping is $a\,b$, or none. For Hangul it is computed. The implementation builds a [hash table](/hash-table/) with the 1,360 other pairs.

## The algorithm

```pseudo id=main
NORMALIZE(form, X)
L1  d <- empty list
L2  for each code point c of X do append FULL-DECOMPOSE(c, form is NFKD or NFKC) to d
L3  CANONICAL-ORDER(d)
L4  if form is NFC or NFKC then d <- COMPOSE(d)
L5  return d

FULL-DECOMPOSE(c, compat)
L6  if c is a Hangul syllable then return its jamo, by the arithmetic of section 3.12.2
L7  m <- the canonical decomposition mapping of c, or its compatibility mapping if compat and it has one
L8  if c has no such mapping then return [c]
L9  return the concatenation of FULL-DECOMPOSE(x, compat) for each x of m

CANONICAL-ORDER(d)
L10 for i <- 1 to |d| - 1 do
L11     j <- i
L12     while j > 0 and ccc(d[j - 1]) > ccc(d[j]) > 0 do
L13         swap d[j - 1] and d[j]; j <- j - 1

COMPOSE(d)
L14 out <- empty list; starter <- -1; last <- -1
L15 for each c of d, in order do
L16     k <- ccc(c)
L17     if starter >= 0 and (last = -1 or 0 < last < k) and PAIR(out[starter], c) exists then
L18         out[starter] <- PAIR(out[starter], c); continue with the next c
L19     if k = 0 then starter <- |out|; last <- -1
L20     else last <- k
L21     append c to out
L22 return out
```

**Decomposition (lines L6 to L9).** The mappings in the data are one level deep. U+1E69 maps to U+1E63 U+0307, and U+1E63 maps again to U+0073 U+0323, so line L9 must recurse. The recursion always stops, because the mappings have no cycle.

**Canonical ordering (lines L10 to L13).** The swap condition of line L12 is the reorderable pair of D108. Because both characters must have a class above 0, a starter never moves and a mark never crosses a starter, and because the condition is a strict $>$, marks of the same class keep their order. So this is an [insertion sort](/insertion-sort/) inside each run of non-starters, and it is [stable](/stable-sort/).

**Composition (lines L14 to L22).** $starter$ is the index of the last starter in $out$, and $last$ is the class of the last mark after it, or $-1$ if there is none. By D115, a character $C$ is blocked from the starter when some character between them is a starter or has a class at least $\mathrm{ccc}(C)$. After canonical ordering, the classes of the marks after the starter do not decrease, so the largest of them is $last$, and the test of line L17 is exactly "not blocked". A starter $C$ can compose only when it comes right after the last starter, with $last = -1$. That case covers the Hangul pairs $L + V$ and $LV + T$, and vowel signs of Indic scripts, such as U+0B47 U+0B3E, which compose to U+0B4B ORIYA VOWEL SIGN O. The composite always has class 0, so line L18 keeps the invariant.

## Example

NFC of U+1E61 U+0323, the letter ṡ followed by a dot below.

| step | sequence | reason |
|---|---|---|
| L2 | 0073 0307 0323 | U+1E61 maps to s and U+0307 DOT ABOVE |
| L3 | 0073 0323 0307 | ccc(0307) = 230 > ccc(0323) = 220 > 0, so line L13 swaps them |
| L17, L18 | 1E63 0307 | PAIR(0073, 0323) is U+1E63 ṣ, and nothing lies between |
| L17, L18 | 1E69 | PAIR(1E63, 0307) is U+1E69 ṩ, and $last = -1$ |

The NFD is 0073 0323 0307, the line L3 row. The input U+1E63 U+0307 and the input s U+0307 U+0323 give the same results, because all three strings are [canonically equivalent](/canonical-equivalence/).

Two cases where composition stops:

- a U+0301 U+0301: the first acute composes to U+00E1. PAIR(00E1, 0301) does not exist, so the second acute is appended, and the NFC is 00E1 0301.
- a U+0305 U+0301: there is no a with overline, so U+0305 is appended with $last = 230$. The acute also has class 230, so it is blocked, and the NFC is 0061 0305 0301, although U+00E1 exists.

A singleton is never composed back. U+212B ANGSTROM SIGN decomposes to U+00C5 and then to 0041 030A, and NFC gives U+00C5, not U+212B.

## Correctness

The proof in proofs/correctness.md shows that the three parts compute D68 (or D65), D109 and D117. Line L9 applies the mappings until none is left, which is the full decomposition. CANONICAL-ORDER removes all reorderable pairs and only swaps such pairs, and since each swap keeps the starters and the order of equal classes, the result is the unique sequence with each run sorted stably, which is what D109 produces. COMPOSE keeps the invariant on $starter$ and $last$ described above, so its test is the blocking condition of D115, and PAIR finds exactly the primary composites. The proof relies on three facts about the data that the definitions do not imply: the mappings have no cycle, every primary composite is a starter, and the composite of a pair is found by its two-part mapping. The tests compare the whole procedure with `unicodedata.normalize` on every decomposable character of Unicode 3.2 in the Basic Multilingual Plane and on random strings, so an error in one of these facts would show up there.

## Complexity

In the [word-RAM model](/word-ram/), with the data in tables of constant access time, line L2 takes $O(n)$ time, because one code point expands to at most 18 code points (under NFKD) and the recursion has constant depth. Canonical ordering takes $O(\sum_r k_r^2)$ time for runs of $k_r$ non-starters, and composition takes $O(|d|)$ time.

| claim | value |
|---|---|
| decomposition | $O(n)$, at most 18 code points per input code point |
| canonical ordering | $O(\sum_r k_r^2)$, which is $\Theta(n^2)$ for one long run in decreasing class order |
| composition | $O(n)$ |
| text in Stream-Safe Text Format | $O(n)$ in total, since every run has at most 30 non-starters |

The worst case is a string of many marks with decreasing classes. Real text has short runs, so the time is linear in practice, and the Stream-Safe Text Format of section 13 of UAX 15 makes the bound linear for every input that follows it.

## Properties

- **Idempotent.** NORMALIZE(form, NORMALIZE(form, X)) = NORMALIZE(form, X).
- **Decides the equivalences.** Two strings are canonically equivalent exactly when their NFD outputs are equal, and the test `test_canonical_equivalence` checks this.
- **Starters stay in place.** The test `test_starters_never_move_and_order_is_stable` checks that canonical ordering moves only marks and keeps the order of equal classes.
- **Not closed under concatenation.** NFC("a") NFC(U+0301) is not in NFC. The test `test_not_closed_under_concatenation` checks this.
- **Recursive.** FULL-DECOMPOSE calls itself on the parts of a mapping. An implementation can store the full decompositions instead and avoid the recursion.

## Variants and improvements

- **Quick check.** Section 9 of UAX 15 gives the properties NFC_Quick_Check and the like. A string whose characters all have the value Yes and whose marks are in order is already normalized, so most text needs no work. A value No means that the string is not normalized, and Maybe means that the algorithm must run.
- **Incremental normalization.** The work can be split at characters that start a new segment, such as starters with the quick check value Yes, and each segment normalized alone. This keeps the buffer small for streams.
- **Counting sort for ordering.** The classes are in 0..254, so a run of marks can also be sorted with a stable [counting sort](/counting-sort/) in $O(k + 255)$ time. For the usual runs of one to three marks, insertion sort is faster.
- **Precomputed tables.** Libraries such as ICU store the full decompositions and the pair table in compact tables, which removes the recursion of line L9 and the search of PAIR.
- **Stream-Safe Text Format.** Insert U+034F COMBINING GRAPHEME JOINER after every 30 non-starters, as section 13 of UAX 15 describes, to bound the buffer and the time.

## When to use it

Normalize text before you compare, hash, index or search it, so that equivalent strings give the same result. NFC is the usual form for storing and exchanging text, and it is what the web and most file formats expect. NFD is convenient for processing that looks at the marks, such as removing accents. Use NFKC or NFKD only for matching, as in identifiers and search, because they change the meaning of text such as ½ and superscripts. For comparison without case, combine normalization with [case folding](/unicode-case-folding/). For sorting, the [collation algorithm](/unicode-collation-algorithm/) handles equivalent strings by itself.

## Pitfalls

- **Sorting across starters.** A sort of all the marks of a string, or a sort that is not stable, gives wrong results. The test `test_starters_never_move_and_order_is_stable` checks this.
- **Missing exclusions.** The derived exclusions, the 1,035 singletons such as U+212B and the 4 non-starter decompositions such as U+0344, are not in the list that CompositionExclusions.txt gives as data. The test `test_exclusion_table` checks the 81 listed exclusions and that the implementation derives exactly the 1,035 singletons and the 4 non-starter decompositions.
- **Composing with the wrong starter.** The composition must use the last starter in the output, which can be a composite that line L18 made, not the last starter in the input.
- **One level of decomposition.** Applying the mappings once leaves characters such as U+1E69 half decomposed.
- **Different Unicode versions.** A code point that is unassigned in one version can be assigned with a mapping or a class in a later one, so two systems with different data can give different results for it. The tests pin the data to version 16.0.0 and check the 35 lines of NormalizationTest.txt that `test_conformance_lines` includes.
- **Long runs of marks.** A string of thousands of marks makes the sort quadratic and the buffer large. Limit runs as the Stream-Safe Text Format does.

## Implementations

## History

The normalization forms were defined in UAX 15 in the years around Unicode 3.0, and the composition step was then fixed by a stability policy: when a new character is added whose decomposition uses existing characters, it is excluded from composition, so that the NFC of existing text does not change. The 14 post composition version exclusions in CompositionExclusions.txt are such characters. NormalizationTest.txt gives conformance test data for every version, and the clauses UAX15-C1 to UAX15-C5 state what an implementation must do.

## References
