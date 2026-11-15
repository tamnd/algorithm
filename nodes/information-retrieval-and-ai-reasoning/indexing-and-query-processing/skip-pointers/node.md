---
tag: 3KK71T
kind: technique
slug: skip-pointers
name: Skip pointers
aliases:
- skip pointers in posting lists
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Adds about sqrt(n) forward pointers to a posting list so an intersection can jump over runs that cannot match.
prereqs: [merge-based-list-intersection, posting-list]
see_also: [skip-list, posting-list-intersection, small-versus-small-intersection, postings-gap-encoding, variable-byte-encoding, elias-fano-encoding, pfor-delta, block-max-wand]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 2, Section 2.3 (faster postings list intersection via skip pointers, the algorithm with skips, the placement of about sqrt(P) evenly spaced pointers, and the remark on static and updated indexes)
  - paper: doi:10.1145/237496.237497
    title: Alistair Moffat and Justin Zobel, Self-indexing inverted files for fast text retrieval, ACM Transactions on Information Systems 14(4), 1996, 349-379
    locator: the skips in compressed inverted lists, their cost in index size (under 20 percent) and the gain for Boolean queries of 5 to 10 terms (under one fifth of the time)
  - paper: doi:10.1145/1132956.1132959
    title: Justin Zobel and Alistair Moffat, Inverted files for text search engines, ACM Computing Surveys 38(2), Article 6, 2006
    locator: the sections on query evaluation with compressed lists and skipping
---

Skip pointers are extra forward links stored inside a [posting list](/posting-list/): every $s$-th entry also holds the id and the place of the entry $s$ positions further on. During an intersection, when the list is behind the other list, a skip can move it past a run of ids that cannot match without reading them one by one. The usual rule of thumb is about $\sqrt{n}$ pointers, evenly spaced, for a list of length $n$. Skip pointers are not a [skip list](/skip-list/): a skip list is a randomized dictionary of linked levels that supports search, insertion and deletion in expected $O(\log n)$ time, while skip pointers are one fixed level of shortcuts, placed when the index is built, on a list that is usually compressed and read forward only. Their main use is on lists coded with [gaps](/postings-gap-encoding/), where an entry cannot be reached by its index and a skip lets the reader jump over the gaps it does not need to decode.

## In plain words

Think of a long sorted list as a road with a sign every few steps. Each sign tells you which number is at the next sign and where it is.

When you compare two lists and the one you walk on is behind, look at the sign. If the number at the next sign is still not past the number you look for, nothing between here and that sign can match, so you go straight to the sign. If it is past, you walk the short way, one entry at a time.

Signs that are close together let you stop near the place you want, but you must read many signs. Signs far apart are cheap to keep, but each jump lands farther from the target, and you walk more. A common choice spaces the signs by about the square root of the list length.

## When it applies

- The query is an AND of terms, so the answer is a [posting list intersection](/posting-list-intersection/). For an OR query the result holds every entry of every list, so there is nothing to skip.
- One list is much longer than the other, so most entries of the long list cannot match.
- The list can be read only forward, as with [variable byte](/variable-byte-encoding/) codes or other codes of gaps. If the list is a plain array, a [galloping search](/exponential-search/) does the same job with no extra space.
- The index does not change often. Skips are placed when the list is built, and an insertion in the middle moves the places that they point to.

## The template

The merge of two sorted lists, with a skip test before each single step. The holes to fill are in capitals.

```pseudo id=main
INTERSECT-WITH-SKIPS(A, B)                 ▷ A and B strictly increasing
L1  i ← 0, j ← 0, R ← ()
L2  while i < |A| and j < |B| do
L3      if A[i] = B[j] then append A[i] to R, i ← i + 1, j ← j + 1
L4      else if A[i] < B[j] then
L5          if HAS-SKIP(A, i) and A[SKIP(A, i)] ≤ B[j] then
L6              while HAS-SKIP(A, i) and A[SKIP(A, i)] ≤ B[j] do i ← SKIP(A, i)
L7          else i ← i + 1
L8      else the same as lines L5 to L7, with A, i and B, j swapped
L9  return R
```

**The holes.** PLACE-SKIPS, at build time, chooses the entries that hold a skip and the spacing $s$. HAS-SKIP$(A, i)$ tells if entry $i$ holds one, and SKIP$(A, i)$ gives its target. In a compressed list, the skip stores the id at the target and the byte offset where the decoder must restart, so the test of line L5 reads only the skip and not the entries between.

**The invariant to prove.** Before each test of line L2, every common id that is not in $R$ is in $A[i..]$ and in $B[j..]$. A jump of line L6 from $i$ to $t$ keeps it, because the ids $A[i], \ldots, A[t-1]$ are less than $A[t] \le B[j]$, and every id left in $B$ is at least $B[j]$, so none of them is common. The test must be $A[t] \le B[j]$: a jump to an id greater than $B[j]$ can pass over $B[j]$ itself. Lines L3 and L7 are the steps of the [merge](/merge-based-list-intersection/), with the same proof.

**The cost.** Let $A$ have length $n$ with a skip at every $s$-th entry, pointing $s$ entries on, and let $B$ have length $m$. The jumps of line L6 move $i$ forward by $s$ each, so there are at most $n/s$ of them. While $j$ stays the same, $i$ makes at most $s - 1$ single steps to reach an entry with a skip, and after a skip test fails, at most $s$ more, because the target of that skip is already past $B[j]$. So $A$ makes at most $n/s + (2s - 1)m$ moves, against up to $n$ for the merge. With $s$ near $\sqrt{n/m}$, this is $O(\sqrt{nm})$. The rule of about $\sqrt{n}$ evenly spaced pointers does not depend on the query, which is not known when the index is built.

**A worked example.** Let $B = (2, 4, 6, \ldots, 32)$, the 16 even numbers from 2 to 32, with skips of length $\sqrt{16} = 4$ at the indices 0, 4 and 8, so that they point to $B[4] = 10$, $B[8] = 18$ and $B[12] = 26$. Intersect it with $A = (8, 30)$, which has no skips.

| state | test | move |
|---|---|---|
| $A[0] = 8$, $B[0] = 2$ | $B$ is behind; the skip target $B[4] = 10 > 8$ | single step, $j = 1$ |
| $B[1] = 4$, then $B[2] = 6$ | no skips at indices 1 and 2 | single steps, $j = 3$ |
| $B[3] = 8$ | $8 = 8$ | output 8, $i = 1$, $j = 4$ |
| $A[1] = 30$, $B[4] = 10$ | $B[8] = 18 \le 30$, then $B[12] = 26 \le 30$ | two jumps, $j = 12$ |
| $B[12] = 26$, then $B[13] = 28$ | no skips at indices 12 and 13 | single steps, $j = 14$ |
| $B[14] = 30$ | $30 = 30$ | output 30, $i = 2$, stop |

The result is $(8, 30)$. The scan reads 9 entries of $B$ (the indices 0 to 4, 8 and 12 to 14), where the merge reads 15. The skip at index 0 shows the pitfall of the test: a jump to $B[4] = 10$ with the target 8 would pass over the match.

On the toy collection the lists are too short to need skips: the longest one, for the word "a", has 5 entries.

## Classic examples

- **[Merge-based list intersection](/merge-based-list-intersection/)** with skips is the template above. Manning, Raghavan and Schuetze give it for two posting lists.
- **[Positional intersection](/positional-intersection/).** The document level of a positional list is a posting list, so skips move it to the next common document before any position is read.
- **[Document-at-a-time evaluation](/document-at-a-time-evaluation/).** Each term has a cursor with a forward seek to the first id at least $x$; skips make that seek cheap on compressed lists.
- **[WAND](/wand/) and [block-max WAND](/block-max-wand/).** These ranked methods move a cursor to a pivot id that may be far ahead, and use skips or a block index to get there. Block-max WAND also keeps the largest score of each block next to the skip data.
- **[Small-versus-small intersection](/small-versus-small-intersection/)** on compressed lists seeks in the long list with a block index, the array form of skips.

## Variations

- **A block index.** Keep the first id of each block of $s$ compressed entries in a separate small array, and find the block of a target with a binary or galloping search on that array. This is the usual layout for block codes such as [PForDelta](/pfor-delta/).
- **More than one level.** Skips at the spacings $s$, $s^2$, $s^3$, and so on give seeks in $O(\log n)$ steps. This is close to a deterministic skip list stored in a static array.
- **Spacing for the query.** If the lengths of the lists in typical queries are known, the cost $n/s + (2s-1)m$ suggests a spacing near $\sqrt{n/m}$ in place of $\sqrt{n}$.
- **Codes with built-in skips.** [Elias-Fano encoding](/elias-fano-encoding/) stores the high bits of the ids in a unary bit array, and a select structure on that array jumps to any part of the list with no extra pointers.
- **Skips in position lists.** A long list of positions in one document can carry its own skips, for proximity queries on long documents.

## Pitfalls

- **A jump past the target.** The skip test must check that the target id is at most the current id of the other list. In the example, a jump from $B[0]$ to $B[4] = 10$ when the other id is 8 loses the match 8, with no error.
- **The wrong spacing.** Many short skips cost space and many failed tests; a few long skips are rarely taken. Moffat and Zobel report an index growth of under 20 percent with their skips, so the space is not free.
- **Updates.** Skips that point a fixed number of entries ahead must be rebuilt when an id is inserted in the middle of a list. They suit a static index; a list that changes often needs a different layout, see [dynamic index maintenance](/dynamic-index-maintenance/).
- **Skips where they cannot help.** Skips do not speed up a union, and they do not help when the two lists have about the same length and interleave finely, because then almost every skip test fails.
- **The hardware.** The gain comes from not decoding the entries that are skipped. When the lists are in memory and decoding is fast, the extra tests can cost about as much as they save; measure before tuning.

## References
