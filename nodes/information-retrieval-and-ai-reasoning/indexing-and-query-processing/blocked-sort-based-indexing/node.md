---
tag: 7YJRVM
kind: algorithm
slug: blocked-sort-based-indexing
name: Blocked sort-based indexing
aliases:
- BSBI
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Builds an inverted index on disk by sorting blocks of termid-docid pairs in memory and merging the sorted runs.
solves: [inverted-index]
model: external-memory-model
complexity:
  vars: {T: the number of tokens (one term id and document id pair for each), M: the number of pairs that fit in memory, B: the number of pairs in a disk block, k: the number of runs (the ceiling of T/M), V: the number of distinct terms}
  time: {worst: O(T log T), average: O(T log T), best: O(T log T)}
  space: {memory: O(M + V), disk: O(T)}
  io:
    worst: "O((T/B) (1 + log_(M/B) k))"
    best: "O(T/B)"
properties: {deterministic: true, comparison: false, recursive: false, online: false, in_place: false, stable: true}
prereqs: [inverted-index, external-merge-sort, k-way-merge]
see_also: [single-pass-in-memory-indexing, posting-list, logarithmic-merging, dynamic-index-maintenance, index-partitioning, postings-gap-encoding, external-memory-model, hash-table]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 4, Section 4.1 (hardware basics) and Section 4.2 (blocked sort-based indexing, the BSBI pseudocode and the merge of the block files)
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 4, Section 4.5 (index construction), Section 4.5.2 (sort-based index construction)
  - book: isbn:9781558605701
    title: Ian H. Witten, Alistair Moffat and Timothy C. Bell, Managing Gigabytes, second edition, Morgan Kaufmann, 1999
    locator: Chapter 5 (index construction, sort-based inversion)
  - paper: doi:10.1145/1132956.1132959
    title: Justin Zobel and Alistair Moffat, Inverted files for text search engines, ACM Computing Surveys 38(2), Article 6, 2006
    locator: the section on index construction
---

Blocked sort-based indexing (BSBI) builds an [inverted index](/inverted-index/) for a collection that is too large for memory. It maps each term to an integer term id, reads the collection as a stream of (term id, document id) pairs, sorts the pairs one memory-sized block at a time, writes each sorted block to disk as a run, and then merges all runs into the final [posting lists](/posting-list/). It is [external merge sort](/external-merge-sort/) applied to term and document pairs, with two additions: a dictionary from terms to ids that stays in memory during the whole pass, and a merge that joins equal pairs into one posting with a term frequency. [Single-pass in-memory indexing](/single-pass-in-memory-indexing/) removes the global term ids and the sort of pairs; this page keeps both.

## In plain words

A search engine must find, for each word, the list of documents that contain it. For a large collection this list of lists does not fit in memory. BSBI solves this with a method that most people use to sort a big pile of cards. First give each word a number. Then read the documents and write down, for each word you see, its number and the document number. When your memory is full, sort what you have, put the sorted stack on disk, and start a new stack. At the end, read all sorted stacks at the same time and always take the smallest card on top. The cards come out in order of word, and for each word in order of document. That is the index.

## The problem

The input is a collection of $N$ documents $d_1 < d_2 < \cdots < d_N$, each a sequence of tokens, with $T$ tokens in total. The output is, for each distinct term $t$, its posting list: the pairs $(d, \mathrm{tf}_{t,d})$ for the documents $d$ that contain $t$, in increasing order of $d$, where $\mathrm{tf}_{t,d}$ is the number of times $t$ occurs in $d$. Memory holds $M$ pairs, with $M$ much smaller than $T$, and the disk transfers blocks of $B$ pairs. The machine is the [external memory model](/external-memory-model/). The dictionary of the $V$ distinct terms must fit in memory next to one block.

## The algorithm

```pseudo id=main
BSBI(D, M)                             ▷ D: documents in increasing id order, M ≥ 1
L1  termid ← empty map, runs ← empty list, block ← empty list
L2  for each document d of D, for each token w of d do
L3      if w is not in termid then termid[w] ← |termid|
L4      add (termid[w], d) to block
L5      if |block| = M then add INVERT(block) to runs, block ← empty list
L6  if block is not empty then add INVERT(block) to runs
L7  return MERGE-RUNS(runs)

INVERT(block)
L8  sort block by (term id, document id)
L9  replace each group of equal pairs (t, d) by one triple (t, d, f), f the size of the group
L10 return the triples, in sorted order        ▷ one run, written to disk

MERGE-RUNS(runs)
L11 put the first triple of each run in a min-heap H, keyed by (t, d)
L12 while H is not empty do
L13     remove the least triple (t, d, f) of H, and put the next triple of its run in H
L14     if the last output triple has the key (t, d) then add f to its count
L15     else output (t, d, f)
L16 group the output by t, and map each term id back to its term
```

Line L1 starts an empty dictionary from terms to ids. The loop of line L2 reads the tokens in the order of the collection. Line L3 gives a new term the next free id. Line L4 adds one pair for each token. When the block holds $M$ pairs, line L5 sorts it and writes it out as one run, and line L6 does the same for the last, shorter block.

INVERT sorts a block by term id first and document id second (line L8). After the sort, the copies of one pair are next to each other, so line L9 can count them in one scan. The run holds one triple for each distinct pair of the block.

MERGE-RUNS is a [k-way merge](/k-way-merge/) of the runs. The heap of line L11 holds the next triple of each run, so line L13 takes the triples of all runs in order of $(t, d)$. A block can end in the middle of a document, so the same pair can appear in two runs. Line L14 joins such copies by adding their counts. Line L16 cuts the sorted output into one posting list for each term. In a real engine, the merge reads each run through a small buffer of a few disk blocks and writes each posting list to the index file as soon as its term is complete.

## Example

The toy collection of the information retrieval pages has 8 documents of 9 or 10 tokens, 79 tokens in total, 50 distinct terms and 74 postings. Take $M = 16$. The term ids follow the order of first use: "binary" is 0, "search" is 1, "finds" is 2, "a" is 3, and "sorted" is 6. Line L5 cuts the stream after tokens 16, 32, 48 and 64, so there are $\lceil 79/16 \rceil = 5$ runs.

| run | tokens | documents | triples | triples for "a" (id 3) and "sorted" (id 6) |
|---|---|---|---|---|
| 1 | 1 to 16 | 1, 2 | 15 | (3, 1, 2), (6, 1, 1), (6, 2, 1) |
| 2 | 17 to 32 | 2, 3, 4 | 16 | (3, 3, 1), (3, 4, 1), (6, 2, 1) |
| 3 | 33 to 48 | 4, 5 | 16 | (3, 4, 1), (6, 4, 1) |
| 4 | 49 to 64 | 5, 6, 7 | 15 | (3, 6, 2) |
| 5 | 65 to 79 | 7, 8 | 15 | (3, 7, 1), (6, 8, 1) |

Document 2 is "merge sort merges two sorted runs into one sorted array". Its first "sorted" is token 14 and goes to run 1, and its second "sorted" is token 18 and goes to run 2. The same happens to "a" in document 4, which runs 2 and 3 share. The merge reads these triples in this order:

| line L13 takes | from run | line | output |
|---|---|---|---|
| (3, 1, 2) | 1 | L15 | (3, 1, 2) |
| (3, 3, 1) | 2 | L15 | (3, 3, 1) |
| (3, 4, 1) | 2 | L15 | (3, 4, 1) |
| (3, 4, 1) | 3 | L14 | (3, 4, 2) |
| (3, 6, 2) | 4 | L15 | (3, 6, 2) |
| (3, 7, 1) | 5 | L15 | (3, 7, 1) |
| (6, 1, 1) | 1 | L15 | (6, 1, 1) |
| (6, 2, 1) | 1 | L15 | (6, 2, 1) |
| (6, 2, 1) | 2 | L14 | (6, 2, 2) |
| (6, 4, 1) | 3 | L15 | (6, 4, 1) |
| (6, 8, 1) | 5 | L15 | (6, 8, 1) |

The posting list of "a" is $(1, 2), (3, 1), (4, 2), (6, 2), (7, 1)$, and the list of "sorted" is $(1, 1), (2, 2), (4, 1), (8, 1)$. The five runs hold 77 triples. Line L14 joins three pairs that a block boundary cut: "sorted" in document 2, and "a" and "list" in document 4. So the index has $77 - 3 = 74$ postings, the same as a direct build in memory.

## Correctness

The dictionary of line L3 gives each term one id for the whole pass, so equal terms in different blocks have equal ids. The blocks are consecutive pieces of the pair stream. In each run, line L9 outputs one triple for each distinct pair of the block, with the number of copies of that pair in the block. The heap merge outputs all triples in nondecreasing order of $(t, d)$, so the copies of one pair from different runs come out one after the other, and line L14 adds their counts. The sum over the runs is the number of copies of $(t, d)$ in the whole stream, which is $\mathrm{tf}_{t,d}$. Sorted by $t$ and then $d$, the output is the posting lists in the required order. The full proof is in the proof file below.

## Complexity

- **CPU time.** The $k = \lceil T/M \rceil$ blocks cost $O(M \log M)$ each to sort, so $O(T \log M)$ in total. The merge does $O(\log k)$ work for each of at most $T$ triples. With $\log M + \log k = O(\log T)$, the total is $O(T \log T)$, the cost of a sort of all pairs. This is the bound that Manning, Raghavan and Schuetze give for BSBI. The dictionary adds $O(T)$ expected time with a [hash table](/hash-table/).
- **Disk transfers.** Reading the collection and writing the runs costs $O(T/B)$ block transfers. If $k \le M/B$, one merge pass reads each run through a buffer of one block, so the merge also costs $O(T/B)$. If there are more runs than buffers, the runs are merged in passes of $M/B$ runs, as in external merge sort, and the merge costs $O((T/B) \log_{M/B} k)$.
- **Memory.** One block of $M$ pairs, plus the dictionary of $V$ terms, plus $k$ merge buffers.
- **Disk.** The runs hold at most $T$ triples. The final index replaces them.

## Properties

- **Two passes over the pairs.** One pass writes the runs, and one merge pass reads them, when $k \le M/B$.
- **Global term ids.** The term to id map is built during the first pass and must stay in memory to the end. For a very large vocabulary this map can be the limit, not the block.
- **Deterministic.** The output does not depend on $M$; only the number and the content of the runs do.
- **Sequential disk access.** Each run is written once from start to end, and the merge reads each run from start to end.

## Variants and improvements

- **Two passes with a known vocabulary.** If the vocabulary is collected in an earlier pass, the term ids can be the ranks of the terms in sorted order, so a merge by id is also a merge in term order.
- **Compressed runs.** The triples of a run are sorted, so the document ids of one term can be stored as gaps with a variable-length code. This cuts the disk space and the transfer time of the runs. See [postings gap encoding](/postings-gap-encoding/).
- **Merge-based construction.** Buettcher, Clarke and Cormack describe sort-based construction with the same two phases, and compare it with merge-based construction, which builds a full in-memory index for each block and merges the partial indexes. That second method is close to SPIMI.
- **Without global term ids.** [Single-pass in-memory indexing](/single-pass-in-memory-indexing/) builds a dictionary and posting lists for each block, sorts only the terms of the block, and merges blocks by term string. It does not need the global map.
- **Distributed construction.** The same sort and merge steps run as the map and reduce phases of a MapReduce job, with term ranges as the partitions. See [index partitioning](/index-partitioning/).

## When to use it

Use BSBI for a static collection that is larger than memory, when the dictionary of the whole vocabulary fits in memory and the sort of fixed-size records is the fastest tool at hand. For a collection that changes, BSBI builds the main index, and a scheme such as [logarithmic merging](/logarithmic-merging/) adds new documents later. If the vocabulary is too large to keep a term to id map, use single-pass in-memory indexing.

## Pitfalls

- **Term ids for each block.** If the map of line L1 is reset for each block, one term gets different ids in different runs, and the merge makes two posting lists for it. The map must live for the whole pass, as in line L1, or the merge must compare terms, as SPIMI does.
- **No join of cut documents.** If line L14 is left out and each triple goes to the output by line L15, the list of "sorted" in the example holds $(2, 1)$ twice in place of $(2, 2)$. A block boundary can cut a document, so the merge must add the counts of equal pairs.
- **Sort by term id only.** An unstable sort by term id alone, in place of line L8, can put the documents of a term out of order inside a run, and the merged posting lists are then not sorted. The key must be the pair (term id, document id).
- **Too many runs for one pass.** The merge needs one buffer of at least one block for each run. If $k$ is larger than $M/B$, a one-pass merge reads from disk with tiny buffers and becomes slow. Merge in several passes, as in external merge sort, or make the blocks larger.
- **Pairs in place of postings.** The block holds one pair for each token, not one for each distinct pair, so a block of $M$ pairs gives fewer than $M$ postings. The disk space for the runs is in tokens, not in postings.

## Implementations

## History

Sort-based inversion of a text file is the classic method for building an inverted file, and Witten, Moffat and Bell describe it with the cost of the disk sort in their book on index construction. Manning, Raghavan and Schuetze gave the method the name blocked sort-based indexing in their 2008 textbook, where it is the first of the construction algorithms, next to single-pass in-memory indexing and distributed indexing. Buettcher, Clarke and Cormack treat it as sort-based index construction.

## References
