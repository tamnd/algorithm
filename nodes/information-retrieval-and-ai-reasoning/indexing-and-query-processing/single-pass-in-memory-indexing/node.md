---
tag: 8P8GD3
kind: algorithm
slug: single-pass-in-memory-indexing
name: Single-pass in-memory indexing
aliases:
- SPIMI
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Builds a separate dictionary and posting lists for each block in one pass with no global term ids, then merges the blocks.
solves: [inverted-index]
model: external-memory-model
complexity:
  vars: {T: the number of tokens, M: the number of tokens that one block takes in, W: the number of terms summed over all blocks, k: the number of blocks (the ceiling of T/M), B: the number of words in a disk block}
  time: {average: O(T + W log T), worst: O(T log T)}
  space: {memory: O(M), disk: O(T)}
  io:
    worst: "O((T/B) (1 + log_(M/B) k))"
    best: "O(T/B)"
properties: {deterministic: true, comparison: false, recursive: false, online: false, in_place: false, stable: true}
prereqs: [inverted-index, hash-table, blocked-sort-based-indexing, k-way-merge]
see_also: [posting-list, logarithmic-merging, geometric-partitioning, dynamic-index-maintenance, index-partitioning, postings-gap-encoding, external-merge-sort, array-doubling]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 4, Section 4.3 (single-pass in-memory indexing, the SPIMI-INVERT pseudocode), with Section 4.2 for the merge of the blocks
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 4, Section 4.5.1 (in-memory index construction) and Section 4.5.3 (merge-based index construction)
  - paper: "Steffen Heinz and Justin Zobel, Efficient single-pass index construction for text databases, Journal of the American Society for Information Science and Technology 54(8), pages 713 to 729, 2003"
    title: Efficient single-pass index construction for text databases
    locator: the single-pass construction with in-memory partial indexes and a final merge
  - paper: doi:10.1145/1132956.1132959
    title: Justin Zobel and Alistair Moffat, Inverted files for text search engines, ACM Computing Surveys 38(2), Article 6, 2006
    locator: the section on index construction
---

Single-pass in-memory indexing (SPIMI) builds an [inverted index](/inverted-index/) for a collection larger than memory. It reads tokens into a [hash table](/hash-table/) from terms to growing [posting lists](/posting-list/), and when memory is full it sorts the terms of the table, writes the table to disk as one block, and starts a new, empty table. A final [k-way merge](/k-way-merge/) joins the blocks by term. It differs from [blocked sort-based indexing](/blocked-sort-based-indexing/) in two ways. It has no global map from terms to integer ids, so the dictionary of the whole vocabulary never has to fit in memory. And it never sorts the (term, document) pairs: the postings of a term arrive in document order and are appended in place, so only the distinct terms of each block are sorted.

## In plain words

Read the documents one by one. Keep a notebook in memory with one page for each word you have seen. When you meet a word, open its page and write the number of the current document at the end, or add one to its count if that number is already the last entry. The numbers on each page are in order without any extra work, because you read the documents in order. When the notebook is full, put its pages in alphabetical order, store it on a shelf, and take a new empty notebook. At the end, read all the notebooks on the shelf together, alphabet order in each, and join the pages of each word into one list.

## The problem

The input is a collection of $N$ documents $d_1 < d_2 < \cdots < d_N$ with $T$ tokens in total. The output is, for each term $t$, the list of pairs $(d, \mathrm{tf}_{t,d})$ for the documents that contain $t$, in increasing order of $d$. Memory holds a block of $M$ tokens with its dictionary, much less than $T$. The model is the [external memory model](/external-memory-model/), with disk blocks of $B$ words.

## The algorithm

```pseudo id=main
SPIMI(D, M)                            ▷ D: documents in increasing id order, M ≥ 1
L1  blocks ← empty list, dict ← empty hash map, used ← 0
L2  for each document d of D, for each token w of d do
L3      if w is not in dict then dict[w] ← empty list
L4      P ← dict[w]
L5      if P is not empty and its last posting has id d then add 1 to its count
L6      else append (d, 1) to P
L7      used ← used + 1
L8      if used = M then add WRITE-BLOCK(dict) to blocks, dict ← empty hash map, used ← 0
L9  if dict is not empty then add WRITE-BLOCK(dict) to blocks
L10 return MERGE-BLOCKS(blocks)

WRITE-BLOCK(dict)
L11 return the pairs (w, dict[w]) in increasing order of w     ▷ one block, written to disk

MERGE-BLOCKS(blocks)
L12 put the first entry of each block in a min-heap H, keyed by (term, block number)
L13 while H is not empty do
L14     remove the least entry (w, P) of H, and put the next entry of its block in H
L15     if the output ends with term w then join P to its list, adding counts if the first id of P equals the last id
L16     else output (w, P)
L17 return the output
```

Line L1 starts with an empty table. For each token, lines L3 and L4 find or create the posting list of its term. Because the documents come in increasing id order, the new posting is either for the same document as the last posting of the list, and line L5 adds 1 to the count, or for a later document, and line L6 appends it. In a real engine the list is a dynamic array that doubles when full, as in [array doubling](/array-doubling/). Line L7 counts the memory used, here in tokens. When the block is full, line L8 writes it and starts a new one, and line L9 writes the last block.

WRITE-BLOCK sorts only the terms of the block, so the block on disk is in term order. This is the one sort of SPIMI. It is needed for the merge.

MERGE-BLOCKS takes the block entries in order of term, and for one term in order of block number, which is also the order of the documents. Line L15 joins the lists of one term. A block can end in the middle of a document, so the first posting of a later list can have the same id as the last posting of the list so far. Then the two counts are added.

## Example

Take the toy collection of the information retrieval pages: 8 documents, 79 tokens, 50 distinct terms and 74 postings. With $M = 16$ tokens per block, line L8 writes a block after tokens 16, 32, 48 and 64, and line L9 writes a fifth block with the last 15 tokens.

| block | tokens | documents | terms | postings | list of "sorted" | list of "list" |
|---|---|---|---|---|---|---|
| 1 | 1 to 16 | 1, 2 | 14 | 15 | (1, 1), (2, 1) | |
| 2 | 17 to 32 | 2, 3, 4 | 13 | 16 | (2, 1) | (3, 1), (4, 1) |
| 3 | 33 to 48 | 4, 5 | 15 | 16 | (4, 1) | (4, 1) |
| 4 | 49 to 64 | 5, 6, 7 | 15 | 15 | | |
| 5 | 65 to 79 | 7, 8 | 14 | 15 | (8, 1) | |

Document 2 has "sorted" at its tokens 5 and 9, which are tokens 14 and 18 of the stream, so the boundary after token 16 cuts it. The merge takes the lists of "sorted" from blocks 1, 2, 3 and 5 in that order. Line L16 starts the output with $(1, 1), (2, 1)$. Block 2 gives $(2, 1)$, whose id equals the last id, so line L15 makes the last pair $(2, 2)$. Blocks 3 and 5 append $(4, 1)$ and $(8, 1)$. The list is $(1, 1), (2, 2), (4, 1), (8, 1)$. In the same way, "list" in document 4 is cut between blocks 2 and 3 and ends as $(3, 1), (4, 2)$.

The five blocks hold 71 terms, against 50 distinct terms in the collection, because common words such as "a" and "array" are in several blocks. They hold 77 postings, and the merge joins 3 of them, which leaves the 74 postings of the index. Blocked sort-based indexing with the same block size writes the same 77 entries, but it sorts 79 pairs in its blocks, while SPIMI sorts only the 71 block terms.

## Correctness

Inside one block, the list of each term holds the documents of the block that contain the term, with their counts, in increasing order of id. This holds because the documents are read in increasing order and the tokens of one document are consecutive, so a new posting is either for the last document of the list or for a later one. Each block on disk is sorted by term. The merge takes the lists of one term in block order, so the ids keep increasing from one list to the next, and the only possible repeat is the one document that a block boundary cuts, where line L15 adds the counts. The sum over the blocks is the term frequency. The full proof is in the proof file below.

## Complexity

- **Inversion.** Lines L2 to L8 do $O(1)$ expected work for each token with a hash table, so $O(T)$ expected time in total. Manning, Raghavan and Schuetze give $\Theta(T)$ for SPIMI for this reason.
- **Sort of the block terms.** A block with $v$ distinct terms costs $O(v \log v)$ to sort, with $v \le M$. Over all blocks this is $O(W \log M)$, where $W$ is the number of terms summed over the blocks.
- **Merge.** The heap has at most $k$ entries, so the merge costs $O(W \log k)$ for the heap and $O(T)$ to join the lists. With $\log M + \log k = O(\log T)$, the total is $O(T + W \log T)$ expected, and $W \le T$ gives $O(T \log T)$ in the worst case.
- **Disk transfers.** Each block is written once and read once by the merge, so $O(T/B)$ transfers when the $k$ blocks fit one merge pass, that is $k \le M/B$. With more blocks the merge takes several passes, as in [external merge sort](/external-merge-sort/).
- **Memory.** One block: the table and its lists, $O(M)$ words.

## Properties

- **No global dictionary.** Each block has its own dictionary, and the merge compares term strings. Memory does not depend on the size of the vocabulary of the whole collection.
- **Postings stay in document order.** No sort of postings is needed, inside a block or in the merge.
- **One pass over the collection.** The collection is read once. The merge then reads each block once.
- **Deterministic.** The index does not depend on $M$; only the blocks do.

## Variants and improvements

- **Compressed blocks.** The terms of a block can be stored with [front coding](/front-coding/) and the lists as gaps with a variable-length code, which makes each block smaller and lets more tokens fit in memory. See [postings gap encoding](/postings-gap-encoding/).
- **Memory in bytes.** Real engines stop a block when the bytes used reach a limit, not after a fixed number of tokens. This changes the block boundaries but not the result.
- **Merge-based construction.** Buettcher, Clarke and Cormack describe the same idea as in-memory construction for each part of the collection followed by a merge of the partial indexes. Heinz and Zobel describe a single-pass method of this kind with a careful in-memory structure.
- **Distributed indexing.** The parsers of a MapReduce job can each run SPIMI on their part of the collection, and the inverters merge by term range. See [index partitioning](/index-partitioning/).
- **Dynamic indexes.** The in-memory block of SPIMI is also the auxiliary index of [logarithmic merging](/logarithmic-merging/) and [geometric partitioning](/geometric-partitioning/), which merge the blocks while new documents arrive.

## When to use it

Use SPIMI to build an index for a static collection that does not fit in memory, in particular when the vocabulary is large or unbounded, as in web text with many rare tokens. Use blocked sort-based indexing when a global integer id per term is needed for other reasons and the vocabulary fits in memory. For a collection that grows, use SPIMI for each in-memory block and a merge policy from [dynamic index maintenance](/dynamic-index-maintenance/).

## Pitfalls

- **Documents out of order.** Lines L5 and L6 assume that the documents arrive in increasing id order. With documents in any other order, line L6 appends ids out of order and the lists are not sorted. Feed the documents in id order, or give them ids in the order they are read.
- **Merge order of equal terms.** The heap of line L12 must break ties between equal terms by block number. If it takes the lists of one term in any other order, the ids of the joined list are not increasing.
- **No join for a cut document.** If line L15 appends the list without the test on the first id, a document cut by a block boundary gets two postings. In the example, "sorted" would hold $(2, 1)$ twice in place of $(2, 2)$.
- **Writing the block without sorting.** If WRITE-BLOCK writes the terms in hash table order in place of line L11, the merge cannot work in one pass, because the blocks are no longer sorted by the merge key.
- **Counting memory in postings only.** A block with many new terms uses memory for the dictionary entries too. An engine that limits only the number of postings can run out of memory on a block with many rare terms.

## Implementations

## History

Manning, Raghavan and Schuetze presented SPIMI in their 2008 textbook as the scalable alternative to blocked sort-based indexing. They credit the method to Heinz and Zobel, whose 2003 paper describes single-pass construction with in-memory partial indexes and a final merge. Buettcher, Clarke and Cormack describe the same scheme as merge-based index construction.

## References
