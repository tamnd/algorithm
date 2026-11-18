---
tag: 4GVQ8M
kind: algorithm
slug: adaptive-merging
name: Adaptive merging
aliases:
- adaptive merging index
area: databases/storage-and-indexing
level: research
summary: "Build an index as a side effect of queries: sorted runs are created on the first scan and each range query merges its keys into the final index."
model: word-ram
complexity:
  vars: {N: the number of entries, s: the run size, m: "the number of runs, at most N/s rounded up", g: the number of uncovered key ranges of the query, t: the number of entries that the query merges, a: the size of the answer}
  time: {worst: "O(g m log s + t log m + log N + a)", average: "O(g m log s + t log m + log N + a)", best: "O(log N + a)"}
  space: {extra: "O(N)"}
properties: {deterministic: true, exact: true, external: false, online: true, in_place: false, recursive: false}
history:
  year: 2010
  people: [Goetz Graefe, Harumi Kuno]
  note: "Goetz Graefe and Harumi Kuno of HP Labs presented adaptive merging at EDBT 2010, as a way to build a B-tree index from the queries alone that needs far fewer queries than database cracking to become complete."
prereqs: [database-cracking, sorted-run, k-way-merge]
see_also: [external-merge-sort, replacement-selection, b-plus-tree, bulk-loading-b-tree, index-selection, log-structured-merge-tree, adaptive-sorting, zone-map]
sources:
  - paper: doi:10.1145/1739041.1739087
    title: "Goetz Graefe and Harumi Kuno, Self-selecting, self-tuning, incrementally optimized indexes, Proceedings of the 13th International Conference on Extending Database Technology (EDBT 2010)"
    locator: pp. 371 to 381, run generation by the first query, partitioned B-trees, the merge step of each query, and the comparison with database cracking
  - paper: doi:10.14778/2002938.2002944
    title: "Stratos Idreos, Stefan Manegold, Harumi Kuno and Goetz Graefe, Merging what's cracked, cracking what's merged: adaptive indexing in main-memory column-stores, PVLDB 4(9) (2011)"
    locator: pp. 586 to 597, the hybrids of cracking and adaptive merging and their measured comparison
---

Adaptive merging builds an index on a column as a side effect of range queries, with no index build up front. The first query reads the column in chunks that fit in memory, sorts each chunk, and keeps the results as *sorted runs*, as the first phase of an [external merge sort](/external-merge-sort/) would. Each query then takes the entries of its key range out of all runs, merges them, and puts them into a *final partition* that is fully sorted. A key range that one query has merged is answered from the final partition alone. The index thus grows where the queries go, like [database cracking](/database-cracking/), but because the runs are already sorted, one query is enough to finish its key range. The answers are always exact (a theorem); the speed of convergence is a measurement.

## In plain words

You have a big box of papers in random order. The first time somebody asks for "the papers from March to May", you take the papers out in stacks of 100, put each stack in order, and keep the stacks. Then you pull March to May out of every stack, which is quick because each stack is in order, and you put these papers in one big ordered binder.

The next person asks for "April to August". April and May are already in the binder. You pull only June to August out of the stacks and add them to the binder at the right place. Each paper goes into the binder once and stays there. After enough requests, the stacks are empty and the binder is a full index.

## The problem

The input is a column of $N$ entries (key, row id). Queries arrive one at a time; each asks for all entries with $lo \le key < hi$, in key order. Nothing is known about the queries in advance, and there is no time to build an index before the first one. The goal is to answer each query exactly, with a cost that falls quickly toward that of a complete index for the key ranges that the queries use, and to spend no work on key ranges that no query uses.

A full scan costs $\Theta(N)$ for every query. A complete sorted index costs $O(\log N + a)$ per query, for an answer of size $a$, but needs $\Theta(N \log N)$ work before the first query.

## The algorithm

```pseudo id=main
RANGE-QUERY(lo, hi)
L1  if there are no runs yet then
L2      cut the column into chunks of s entries
L3      sort each chunk in memory; these are the runs R_1, ..., R_m
L4  for each key range [a, b) of [lo, hi) that is not covered yet do
L5      for each run R_i do
L6          i ← the first index with a key ≥ a; j ← the first index with a key ≥ b   ▷ two binary searches
L7          move the slice R_i[i .. j - 1] out of R_i
L8      merge the moved slices into one sorted list L
L9      insert L into the final partition F at the first key ≥ a
L10 add [lo, hi) to the covered key ranges; drop the empty runs
L11 return the entries of F with lo ≤ key < hi
```

- **Covered ranges.** The code keeps the merged key ranges as a sorted list of disjoint ranges. Step L4 asks for the parts of $[lo, hi)$ that are not in this list; there can be several if earlier queries covered pieces of the range.
- **The final partition** holds exactly the entries whose keys are in the covered ranges. All other entries are still in the runs.
- **In the paper**, the runs and the final partition are all partitions of one partitioned B-tree, in which an artificial leading key column names the partition. The code on this page keeps each run and the final partition as a sorted Python list.
- **Run generation.** The paper makes the runs in the first query, with any in-memory sort; replacement selection gives runs about twice the memory size. The code sorts fixed chunks.

## Example

The column is 27, 3, 14, 8, 30, 19, 5, 22, 11 (row ids 0 to 8), and the run size is $s = 3$.

1. **Query [10, 20).** There are no runs, so L2 and L3 make the runs $R_1 = [3, 14, 27]$, $R_2 = [8, 19, 30]$ and $R_3 = [5, 11, 22]$. The whole range $[10, 20)$ is uncovered. The binary searches find 14 in $R_1$, 19 in $R_2$ and 11 in $R_3$. They are merged into $F = [11, 14, 19]$, and the runs are now $[3, 27]$, $[8, 30]$ and $[5, 22]$. The answer is 11, 14, 19.
2. **Query [15, 25).** The covered range is $[10, 20)$, so only $[20, 25)$ is new. Only 22, from $R_3$, moves. $F = [11, 14, 19, 22]$, the covered range becomes $[10, 25)$, and the answer, read from $F$, is 19, 22.
3. **Query [0, 12).** The new part is $[0, 10)$. The entries 3, 8 and 5 move and are merged into 3, 5, 8, which go to the front of $F$. Now $F = [3, 5, 8, 11, 14, 19, 22]$, the covered range is $[0, 25)$, the third run is empty and is dropped, and the runs left are $[27]$ and $[30]$. The answer is 3, 5, 8, 11.

After these three queries, 7 of the 9 entries were moved, each one once, and any query inside $[0, 25)$ now costs two binary searches in $F$.

**Measurement.** With $N = 100{,}000$ random keys in $[0, 10^6)$ (seed 7), runs of 1,000 entries, and queries over random ranges of width $10^4$ (1% of the domain), the first query moves 1,005 entries, its answer. After 100 queries, 62,784 entries are in the final partition; after 400 queries, 97,925 are, and a query that falls in a covered range moves nothing. A full scan would read 100,000 entries for each query.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). The main points:

- **Invariant.** Every entry is in exactly one of the runs and the final partition; all of them are sorted; and an entry is in the final partition if and only if its key is in a covered range.
- **Extraction.** Because a run is sorted, the entries with a key in $[a, b)$ form one contiguous slice, which two binary searches find.
- **Insertion.** All keys in the final partition are in covered ranges, so none lies in the new range $[a, b)$. The merged list therefore fits in one place of the final partition, and the partition stays sorted.
- **Answer (theorem).** After L10, $[lo, hi)$ is covered, so every entry of the answer is in the final partition, and L11 returns all of them in order.
- **Each entry moves once (theorem).** Entries only leave runs and only enter the final partition, so the total merge work over all queries is at most $N$ entries.

## Complexity

- **First query.** Run generation sorts $m$ chunks of $s$ entries, $O(N \log s)$ comparisons, plus the cost of a normal query.
- **Later query.** For each of the $g$ uncovered ranges, two binary searches in each of the $m$ runs, $O(g m \log s)$; a heap merge of the $t$ moved entries, $O(t \log m)$; and the answer from the final partition, $O(\log N + a)$. In a B-tree, inserting the merged list costs $O(t + \log N)$ per range. The Python list on this page shifts the tail instead, which costs $O(N)$ in the worst case.
- **Fully covered query.** $O(\log N + a)$, the cost of a complete index.
- **Total merge work** over any sequence of queries is $O(N \log m)$, since each entry is merged once.
- **Space.** One copy of the column, split among the runs and the final partition.

## Properties

- **Exact.** Every answer equals that of a full scan; the adaptivity changes only the cost.
- **Fast convergence.** A key range is complete after the first query that asks for it. Database cracking needs many queries over the same area before its pieces are small (a measurement of both papers on their workloads).
- **Expensive first query.** The first query sorts the whole column in runs, which costs more than the one partition pass of cracking.
- **Monotone.** No entry ever leaves the final partition, so the work per query only falls for repeated key ranges.

## Variants and improvements

- **Hybrids with cracking.** Idreos, Manegold, Kuno and Graefe (2011) combine the two methods: the initial partitions can be cracked instead of sorted, and the final partition can be cracked, sorted or radix-clustered. Some hybrids keep a first query nearly as cheap as cracking and still converge quickly (a measurement in main-memory column stores).
- **Merging more than the query asks.** A query can merge a wider key range than its own, to finish the index in fewer queries at the cost of more work now.
- **Updates.** New entries can go into a new run, or straight into the final partition if their key is covered. Deletions can mark entries in either place.
- **Replacement selection** gives longer runs and so fewer binary searches per query.

## When to use it

Adaptive merging fits a large table that is read mostly by range predicates on one attribute, when the workload is not known in advance, so [index selection](/index-selection/) before the queries is not possible, and when the key ranges of interest are queried more than once. It suits disk-based systems with B-trees, where sorted runs and merges are the natural tools. If the first query must be cheap, cracking or a hybrid is better; if the workload is known and there is idle time, a [bulk-loaded B-tree](/bulk-loading-b-tree/) is simpler.

## Pitfalls

- **Many runs.** Every uncovered range needs two binary searches in every run. With small runs and a large column, $m$ is large and the searches dominate. Use runs as large as the memory allows.
- **Fragmented coverage.** Many small covered ranges make $g$ large for a wide query. Join covered ranges that touch, as the code does.
- **Half-open bounds.** Mixing closed and half-open ranges in the covered list gives entries that are merged twice or never. Keep one convention.
- **Equal keys.** Search by key only (here by the tuple $(a,)$, which sorts before every entry with key $a$), not by a full entry, or a run is cut in the middle of equal keys.
- **The first query's latency.** Sorting all runs makes the first query much slower than a scan. A system that cannot accept this must make the runs in the background or use cracking for the start.

## Implementations

## History

Goetz Graefe had proposed partitioned B-trees in 2003, B-trees with an artificial leading key column that hold several sorted partitions at once. Graefe and Harumi Kuno used them for adaptive merging at EDBT 2010, as an answer to database cracking (Idreos, Kersten and Manegold, 2007): like cracking, it builds the index as a side effect of queries, but with sorted runs and merges in place of quicksort partitioning. In 2011, Stratos Idreos, Stefan Manegold, Kuno and Graefe studied hybrids of the two methods in main-memory column stores.

## References
