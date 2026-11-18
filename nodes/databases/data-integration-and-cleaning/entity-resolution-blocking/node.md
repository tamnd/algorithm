---
tag: EEW6T2
kind: technique
slug: entity-resolution-blocking
name: Blocking for entity resolution
aliases:
- record blocking
- standard blocking
area: databases/data-integration-and-cleaning
level: core
summary: "Group records by cheap keys and compare only pairs within the same block. Several keys raise recall, and pair completeness and reduction ratio measure the result."
prereqs: [entity-resolution, hash-table]
see_also: [sorted-neighborhood-method, canopy-clustering, minhash, locality-sensitive-hashing, set-similarity-join, soundex, inverted-index, fellegi-sunter-model]
sources:
  - paper: "Peter Christen, A survey of indexing techniques for scalable record linkage and deduplication, IEEE Transactions on Knowledge and Data Engineering 24(9), 2012, pages 1537 to 1555"
    locator: the survey and the experimental comparison of standard blocking, the sorted neighbourhood method, q-gram, suffix array and canopy based indexing
  - paper: "Andrew McCallum, Kamal Nigam and Lyle H. Ungar, Efficient clustering of high-dimensional data sets with application to reference matching, Proceedings of the 6th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2000, pages 169 to 178"
    locator: canopies built with a cheap distance, so that the expensive comparison runs only on records that share a canopy
  - book: isbn:9783642311635
    title: "Peter Christen, Data Matching: Concepts and Techniques for Record Linkage, Entity Resolution, and Duplicate Detection, Springer, 2012"
    locator: the chapter on indexing, and the measures reduction ratio, pair completeness and pair quality
---

Blocking cuts the cost of [entity resolution](/entity-resolution/) by grouping the records by a cheap *blocking key*, such as the first three letters of the surname, and comparing only the pairs inside each group. With one key the candidate pairs are the pairs with *equal* keys, found with a [hash table](/hash-table/) in one pass. With several keys they are the union of the pairs of each key. The [sorted neighborhood method](/sorted-neighborhood-method/) instead compares records whose keys are *near* in sort order. [Canopy clustering](/canopy-clustering/) makes overlapping groups from a cheap distance and a threshold, [MinHash](/minhash/) with [locality-sensitive hashing](/locality-sensitive-hashing/) puts similar sets into the same bucket with a known probability, and a [set similarity join](/set-similarity-join/) returns exactly the pairs above a similarity threshold. Plain blocking needs only a key function and is exact only about its own rule: it returns all pairs with equal keys. Whether those pairs hold the true matches is a heuristic question about the key.

## In plain words

Comparing every record with every other record is too slow for a big file. So you sort the records into boxes by something simple, such as the first letters of the last name and the birth year, and you compare records only inside a box. Records in different boxes are taken to be different people without a check. If a duplicate has a typo in the part used for the box, it lands in the wrong box and is lost. To lose fewer, you box the records a second time by another key and compare inside those boxes too.

## When it applies

- The match rule is expensive, and most pairs are clearly not matches.
- There is a field, or a part of a field, that true matches almost always share: a postcode, a year of birth, a phonetic code of the surname such as [Soundex](/soundex/).
- The key values are spread out, so that no block is very large.

It does not apply well when every field can have errors in any position and no part is stable, or when one key value covers most records.

## The template

```pseudo id=main
Blocking(D, keys K_1 ... K_p)
L1  C ← ∅                                     ▷ the candidate pairs
L2  for each key K in K_1 ... K_p do
L3      H ← an empty hash table
L4      for each record r in D do append r to H[K(r)]
L5      for each list B in H do
L6          add every pair {r, s} of B to C
L7  return C                                  ▷ then run the match rule on C only
```

The cost of one key is $O(n)$ to build the blocks plus $\sum_B |B|(|B| - 1)/2$ pairs. If all blocks have size at most $b$, this is at most $n(b - 1)/2$ pairs. One block of size $n$ brings back all $n(n-1)/2$ pairs, so the worst case is quadratic. With several keys, the union in line L6 removes the pairs found twice.

Three measures describe a set $C$ of candidate pairs, against the set $T$ of true pairs and the set $P$ of all pairs:

- **Reduction ratio** $RR = 1 - |C|/|P|$: how much work is saved.
- **Pair completeness** $PC = |C \cap T|/|T|$: the recall of the candidates, an upper bound on the recall of the whole method.
- **Pair quality** $PQ = |C \cap T|/|C|$: the precision of the candidates.

All three need labels, so they are measurements on a labelled sample, not properties of the key.

## Classic examples

**Keys on generated data.** The generator of the [sorted neighborhood method](/sorted-neighborhood-method/) page (Python seed 42: 60 people, 144 records, 10296 pairs, 141 true pairs, with typos in the names, a changed first letter of the surname in 15% of the copies and a changed city in 10%) gives:

| key | blocks | largest | pairs | RR | PC | PQ |
|---|---|---|---|---|---|---|
| first 3 letters of surname | 37 | 20 | 548 | 0.947 | 0.730 | 0.188 |
| city | 8 | 38 | 1635 | 0.841 | 0.922 | 0.080 |
| surname prefix and year | 77 | 7 | 115 | 0.989 | 0.730 | 0.896 |
| city and year | 60 | 7 | 153 | 0.985 | 0.922 | 0.850 |
| union of the last two | | | 170 | 0.983 | 0.957 | 0.794 |

Adding the year to a key cuts the pairs by a factor of 5 to 10 and keeps the same completeness, because this generator never changes the year. Two keys built from different fields find more true pairs than either one alone. These numbers are measurements on that data only.

**Linkage of two files.** To link two population files, block both on a geographic code and a phonetic code of the surname, and score only the pairs in the same block with the [Fellegi-Sunter model](/fellegi-sunter-model/). A second pass on the birth date finds the pairs whose surname changed, for example by marriage.

**Token blocking.** Each word of each field is a key, so a record is in many blocks. This is an [inverted index](/inverted-index/) on the words, and it needs no choice of field, but frequent words make huge blocks that must be dropped.

## Variations

- **Phonetic and q-gram keys.** Use Soundex or other phonetic codes, or the [q-grams](/q-gram-filtering/) of a field, so that small spelling errors keep the key.
- **Sorted neighborhood.** Sort by the key and use a sliding window, so the number of pairs is fixed and keys that are close but not equal still meet.
- **Canopies.** Use a cheap similarity, such as the [Jaccard similarity](/jaccard-similarity/) of the tokens, with a loose and a tight threshold to make overlapping groups.
- **Hashing for similarity.** MinHash with locality-sensitive hashing makes a block of each band of signatures, so that records with high Jaccard similarity share a block with high probability.
- **Block filtering.** Drop blocks that are larger than a limit, or remove a record from its largest blocks, to cap the cost. This lowers completeness.
- **Learned keys.** With labels, choose the combination of keys that reaches a target completeness with the fewest pairs.

## Pitfalls

- **Errors in the key.** A typo in the part of a field used by the key puts a duplicate in another block, and no later step can find it. Use keys from different fields.
- **Large blocks.** A frequent value such as a common surname or an empty field makes one huge block. The cost is quadratic in the largest block, so empty or default values must not be keys.
- **Reading completeness as recall.** Pair completeness is a bound on the final recall; the match rule loses more.
- **Measuring on easy data.** A key looks perfect on data in which its fields never change, as the year in the example above. Test keys on data with realistic errors in all fields.
- **Duplicate pairs from several keys.** Without the union in line L6, a pair in many blocks is compared many times.

## Exercises

1. Show that with one key and blocks of sizes $b_1, \ldots, b_k$, the number of pairs is at least $n(n/k - 1)/2$, with equality when all blocks have the same size.
2. Two keys have pair completeness $0.73$ and $0.92$. Give an example where their union has completeness $0.92$, and one where it has completeness $1$.
3. Write blocking as an equi-join of the record table with itself on the key, and say which join algorithm fits.
4. A key is built from the first $q$ letters of the surname. Explain how $RR$ and $PC$ change as $q$ grows.

## References
