---
tag: 7P2CSB
kind: algorithm
slug: sorted-neighborhood-method
name: Sorted neighborhood method
aliases:
- SNM
- merge/purge sorted neighborhood
area: databases/data-integration-and-cleaning
level: core
summary: "Sort the records by a key and compare each record only with the w - 1 records before it. Several passes with different keys and a transitive closure give the duplicate clusters."
solves: [entity-resolution]
model: word-ram
complexity:
  vars: {n: the number of records, w: the window size, p: the number of passes}
  time: {worst: "O(p (n log n + w n))", average: "O(p (n log n + w n))", best: "O(p (n log n + w n))"}
  space: {extra: "O(n + p w n)"}
properties: {deterministic: true, exact: false, external: false, online: false, in_place: false, recursive: false}
history:
  year: 1995
  people: [Mauricio A. Hernández, Salvatore J. Stolfo]
  note: "Introduced for the merge/purge of large mailing lists. The journal version of 1998 adds more experiments and an incremental version."
prereqs: [entity-resolution, external-merge-sort]
see_also: [entity-resolution-blocking, r-swoosh, fellegi-sunter-model, weighted-union-find, edit-distance, soundex, jaro-winkler-distance, sliding-window-model]
sources:
  - paper: "Mauricio A. Hernández and Salvatore J. Stolfo, The merge/purge problem for large databases, Proceedings of the 1995 ACM SIGMOD International Conference on Management of Data, pages 127 to 138"
    locator: the sorted neighborhood method (create keys, sort, merge with a window of fixed size), the multi-pass approach with the transitive closure of the matched pairs, and the experiments on generated mailing list data
  - paper: "Mauricio A. Hernández and Salvatore J. Stolfo, Real-world data is dirty: data cleansing and the merge/purge problem, Data Mining and Knowledge Discovery 2(1), 1998, pages 9 to 37"
    locator: the journal version, with the equational theory of the match rules and the incremental merge/purge
  - book: isbn:9783642311635
    title: "Peter Christen, Data Matching: Concepts and Techniques for Record Linkage, Entity Resolution, and Duplicate Detection, Springer, 2012"
    locator: the chapter on indexing, the section on sorted neighbourhood indexing
---

The sorted neighborhood method (SNM) is a way to cut the number of comparisons in [entity resolution](/entity-resolution/). It sorts the records by a key, slides a window of $w$ records over the sorted list, and runs the match rule only on pairs inside the window, which gives $(w - 1) n - w(w-1)/2$ comparisons per pass instead of $n(n-1)/2$. Several passes with different keys are joined by a transitive closure. Standard [blocking](/entity-resolution-blocking/) compares the records whose keys are *equal*; SNM compares the records whose keys are *near* in sort order, so a typo late in a key still leaves the record close to its duplicates. Key functions such as [Soundex](/soundex/) and match rules based on [edit distance](/edit-distance/) are inputs to SNM, not part of it.

## In plain words

You have a long list of customer records with many duplicates that are spelled a little differently. Comparing every record with every other one takes too long. So you sort the list by a key, for example the first letters of the last name and the year of birth. Duplicates now sit close together. You walk down the list and compare each record only with the few records just before it. A typo near the start of the key can move a duplicate far away, so you sort again by another key and walk again. At the end, if A matched B and B matched C, you put A, B and C into one group.

## The problem

The input is a set $D$ of $n$ records, keys $K_1, \ldots, K_p$ (functions from records to sortable values), a window size $w \ge 2$, and a pairwise rule $\mathit{match}(r, s)$. Hernández and Stolfo call the rules the *equational theory*: for example, "same year of birth and at most two edits between the names". The output is a partition of $D$ into clusters, one for each entity found. The aim is the result of comparing all pairs with $\mathit{match}$ and taking the closure, at a fraction of the cost. How close it comes is a matter of the keys and the data, so SNM is a heuristic for the problem [entity resolution](/entity-resolution/).

## The algorithm

```pseudo id=main
SNM(D, K_1 ... K_p, w, match)
L1  P ← ∅                                            ▷ the matched pairs
L2  for each key K in K_1, ..., K_p do                ▷ one pass for each key
L3      L ← the records of D sorted by K
L4      for i ← 1 to |L| do
L5          for j ← max(1, i - w + 1) to i - 1 do     ▷ the w - 1 records before L[i]
L6              if match(L[j], L[i]) then add {L[j], L[i]} to P
L7  C ← the connected components of the graph (D, P), found with union-find
L8  return C
```

Line L3 is the *sort* phase. A key usually joins parts of several fields, such as the first consonants of the last name and the first letters of the first name, with the most stable characters first. On disk the sort is an [external merge sort](/external-merge-sort/). Lines L4 to L6 are the *merge* phase: the window moves down by one record at a time, as in the [sliding window model](/sliding-window-model/), and the new record is compared with the $w - 1$ records already in it. Line L7 is the multi-pass closure. A [weighted union-find](/weighted-union-find/) does it in near linear time.

## Example

Six records with a last name and a year of birth. The rule is: same year and at most one edit between the names.

| record | name | year |
|---|---|---|
| r1 | smith | 1970 |
| r2 | smyth | 1970 |
| r3 | jones | 1962 |
| r4 | smith | 1985 |
| r5 | jonas | 1962 |
| r6 | brown | 1970 |

**Pass 1, key = name, $w = 2$.** The order is r6 brown, r5 jonas, r3 jones, r1 smith, r4 smith, r2 smyth. The 5 calls compare neighbours only. Only r5 and r3 match. The duplicate pair r1 and r2 is missed, because r4 (another person, born in 1985) sits between them.

**The same pass with $w = 3$** makes $(3 - 1) \cdot 6 - 3 = 9$ calls and also finds r1 and r2.

**Pass 2, key = (year, name), $w = 2$.** The order is r5, r3, r6, r1, r2, r4. Neighbours r5 and r3 match, and so do r1 and r2. With both passes at $w = 2$ the method makes 10 calls and returns the clusters {r1, r2}, {r3, r5}, {r4} and {r6}, the same result as all 15 pairs.

**A larger run.** On generated data with 60 people and 144 records (141 true duplicate pairs, Python seed 42, typos in the names and a changed first letter of the last name in 15% of the copies), comparing all 10296 pairs with a rule like the one above gives pairwise precision 1.0 and recall 0.922. One pass with $w = 4$ (426 calls) gives recall 0.681, 0.624 or 0.901 for the three keys used. Three passes with $w = 4$ (1278 calls, 12% of all pairs) give recall 0.922, the same as all pairs. These numbers are measurements on that data only.

## Correctness

One pass calls $\mathit{match}$ exactly once on each pair of records that are less than $w$ positions apart in its sort order, and on no other pair. So $P$ is the set of matching pairs that some pass placed in its window, and line L7 returns the components of the graph of these pairs. With $w \ge n$ this is the transitive closure of the match rule over all pairs. With smaller $w$ it is a refinement of that closure: SNM can miss merges, but it never makes a merge that the full comparison would not make. There is no guarantee about the true entities; that depends on the keys and the rule. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **Sort.** $O(n \log n)$ key comparisons per pass. For data on disk, this is the cost of an external sort.
- **Merge.** $(w - 1) n - w (w - 1)/2$ match calls per pass for $n \ge w$, so $O(w n)$. The match rule is often the most expensive step, so this term counts most in practice.
- **Closure.** At most $p (w - 1) n$ unions, near linear with union-find.
- **Total.** $O(p (n \log n + w n))$ time and $O(n)$ memory besides the pairs; the window itself needs only $w$ records in memory.

## Properties

- **Not exact.** It returns a subset of the merges of the all-pairs closure, and its quality depends on the keys. Its window size and keys are heuristics, not results of a proof.
- **Fixed cost.** The number of comparisons depends only on $n$, $w$ and $p$, not on the data. Blocking, by contrast, can blow up when one key value is frequent.
- **Order dependent.** Ties in the sort order and the choice of the first characters of the key change which pairs are compared.
- **Closure can chain.** The transitive closure can join two different entities through a chain of near matches.

## Variants and improvements

- **Multi-pass.** The main form of the method, as above. Hernández and Stolfo measured on their generated data that several passes with small windows found more duplicates than one pass with a large window at a similar cost.
- **Clustering method.** The paper also partitions the records by a coarse key and runs the window inside each part, which suits parallel machines.
- **Incremental merge/purge.** The journal version keeps a representative of each cluster, so that a new batch of records is compared with the representatives instead of the full old data.
- **Adaptive windows.** Later work grows or shrinks the window by the similarity of the keys at its edge, so that runs of similar keys get a larger window.
- **A window over key values.** Another variant slides the window over the sorted list of distinct key values instead of records, so that all records with the same key are always compared.

## When to use it

Use SNM when you have a reasonable sort key and want a predictable number of comparisons, for example to deduplicate a large list of names and addresses. Use two or three passes with keys built from different fields. If many records share one key value and must all be compared with each other, standard [blocking](/entity-resolution-blocking/) on that key is simpler. If you can afford to compare all pairs with an expensive rule, [R-Swoosh](/r-swoosh/) also merges the records and compares the merged results.

## Pitfalls

- **A typo in the first character.** A different first character moves a record far away in the order. Only another pass with another key can find it.
- **Window too small for large clusters.** An entity with more than $w$ records cannot have all its records in one window, so its pairs are found only through the closure, and a missing link splits the cluster.
- **Frequent keys.** If more than $w$ records share a key value, the window sees only some of them, and the result depends on the tie order. Break ties by a second field, not by input position, if the order of input is not random.
- **Closure without checks.** Line L7 joins chains, so one wrong match can merge two large clusters. Check large clusters or use a stricter rule for merges through the closure.

## Implementations

## History

Hernández and Stolfo described the method in 1995 for the merge/purge problem: the deduplication of mailing lists and other large files that come from many sources. They wrote the match rules as an equational theory in a rule language, ran the method on generated data with known duplicates and on real data, and showed the multi-pass approach with a transitive closure. The 1998 journal version adds the incremental algorithm and more experiments. Christen's book (2012) treats it as one of the main indexing methods for record linkage.

## References
