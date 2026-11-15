---
tag: CHQP94
kind: data-structure
slug: posting-list
name: Posting list
aliases:
- postings list
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: intro
summary: The sorted list of document ids, with optional frequencies and positions, for one term of an inverted index.
model: word-ram
complexity:
  vars: {n: the number of postings in the list, g: the number of postings that one NEXT-GEQ call skips, T: the number of tokens in the collection}
  time: {append: O(1) amortized, access: O(1), next_geq: O(1 + log g), build: O(T) expected}
  space: {total: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [term-document-incidence-matrix, binary-search]
see_also: [inverted-index, posting-list-intersection, merge-based-list-intersection, skip-pointers, positional-index, exponential-search, postings-gap-encoding, elias-fano-encoding]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 1, Section 1.2 (building an inverted index, the dictionary and the postings sorted by document id), and Chapter 2, Section 2.3 (skip pointers)
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 2, Section 2.1 (the inverted index interface first, last, next and prev, and Section 2.1.2 on the implementation of these methods)
  - paper: doi:10.1145/1132956.1132959
    title: Justin Zobel and Alistair Moffat, Inverted files for text search engines, ACM Computing Surveys 38(2), Article 6, 2006
    locator: the layout of an inverted list as document ids with in-document frequencies and positions, and its compression
  - book: isbn:9781558605701
    title: Ian H. Witten, Alistair Moffat and Timothy C. Bell, Managing Gigabytes, second edition, Morgan Kaufmann, 1999
    locator: Chapter 3 (indexing) and Chapter 4 (querying)
---

A posting list is the list of documents that contain one term, kept in increasing order of document id, with an optional term frequency and list of positions for each document. One posting list for each term of the vocabulary, plus a dictionary that maps a term to its list, makes an [inverted index](/inverted-index/). The list is the row of the [term-document incidence matrix](/term-document-incidence-matrix/) for that term, stored without its zeros. Because the ids are sorted, two lists can be intersected by a [merge](/merge-based-list-intersection/), and a search for the first id at least some value takes $O(1 + \log g)$ comparisons when it skips $g$ entries.

## In plain words

Think of the index at the back of a book. For each word it gives the pages where the word appears, from the first page to the last. A posting list is the same thing for a search engine: for each word, the numbers of the documents that hold the word, from small to large. Each entry is called a posting. It can also say how many times the word occurs in that document, and where.

The order is the important part. Because the numbers go up, the engine can walk two lists side by side to find the documents that hold both words. It can also jump ahead in a list to the first number past some value, without a look at each entry on the way.

## The abstract type

A posting list for a term $t$ over a collection with document ids from a totally ordered set holds a sequence of postings $(d_0, f_0), (d_1, f_1), \ldots, (d_{n-1}, f_{n-1})$, where $d_0 < d_1 < \cdots < d_{n-1}$ are the ids of the documents that contain $t$ and $f_i \ge 1$ is the number of times $t$ occurs in $d_i$. The length $n$ is the document frequency $\mathrm{df}_t$ of the term. The operations are:

- APPEND$(P, d, f)$: add the posting $(d, f)$ at the end, if $d$ is greater than the last id.
- ACCESS$(P, i)$: return the posting at index $i$.
- NEXT-GEQ$(P, x, lo)$: return the least index $p \ge lo$ with $d_p \ge x$, or $n$ if there is none.

NEXT-GEQ is the operation that intersection algorithms need. It is called `next` in the interface of Buettcher, Clarke and Cormack, and `nextGEQ` in many engines. A [positional index](/positional-index/) adds the list of positions of $t$ in $d_i$ to each posting.

## Representation

The plain form is two arrays of length $n$: one for the ids and one for the frequencies. The arrays grow at the end, as a dynamic array does, so APPEND is amortized $O(1)$. An index is built in order of document id, so each new posting goes at the end of its list.

In a real engine the ids are stored as gaps $d_i - d_{i-1}$, which are small for long lists, and the gaps are compressed with a code such as [variable-byte encoding](/variable-byte-encoding/) or [PForDelta](/pfor-delta/). This is [postings gap encoding](/postings-gap-encoding/). A compressed list must be decoded from the start, so engines add [skip pointers](/skip-pointers/) or cut the list into blocks with the first id of each block in a small table. [Elias-Fano encoding](/elias-fano-encoding/) stores the ids in about $2 + \log_2(u/n)$ bits each, for ids below $u$, and still supports NEXT-GEQ directly. This page uses the plain arrays.

## Operations

The main operations are APPEND and NEXT-GEQ. NEXT-GEQ is a galloping search, the form of [exponential search](/exponential-search/) that starts at a given index. It probes the indices $lo, lo + 1, lo + 3, lo + 7, \ldots$, at offsets $2^i - 1$, until it finds an id at least $x$ or passes the end, then does a [binary search](/binary-search/) in the last gap.

```pseudo id=main
APPEND(P, d, f)                         ▷ P.ids is strictly increasing
L1  if |P| > 0 and not (P.ids[|P| - 1] < d) then error "out of order"
L2  add d at the end of P.ids, add f at the end of P.tf

NEXT-GEQ(P, x, lo)                      ▷ least p ≥ lo with P.ids[p] ≥ x, else |P|
L3  n ← |P|
L4  if lo ≥ n or not (P.ids[lo] < x) then return lo
L5  b ← 1                                ▷ P.ids[lo + b - 1] < x
L6  while lo + 2b - 1 < n and P.ids[lo + 2b - 1] < x do b ← 2b
L7  a ← lo + b, c ← min(lo + 2b - 1, n)
L8  while a < c do                       ▷ P.ids[a - 1] < x, and c = n or P.ids[c] ≥ x
L9      q ← ⌊(a + c) / 2⌋
L10     if P.ids[q] < x then a ← q + 1 else c ← q
L11 return a
```

ACCESS$(P, i)$ returns $(P.\mathit{ids}[i], P.\mathit{tf}[i])$. To build all lists of a collection, read the documents in increasing id order, count the terms of each document in a [hash table](/hash-table/), and call APPEND on the list of each distinct term.

## Example

The toy collection of the information retrieval pages has 8 documents, 79 tokens, 50 distinct terms and 74 postings. Of the 50 lists, 35 have only one posting. The longest lists are:

| term | ids | tf |
|---|---|---|
| a | 1, 3, 4, 6, 7 | 2, 1, 2, 2, 1 |
| sorted | 1, 2, 4, 8 | 1, 2, 1, 1 |
| array | 1, 2, 8 | 1, 1, 1 |
| posting | 3, 4, 5 | 1, 1, 1 |

Document 2 is "merge sort merges two sorted runs into one sorted array", so the posting of "sorted" for it is $(2, 2)$. The token "sort" is a different term from "sorted", because the collection has no [stemming](/stemming/).

Run NEXT-GEQ on the list of "sorted", with $x = 5$ and $lo = 0$:

| line | probe | id | result | state |
|---|---|---|---|---|
| L4 | 0 | 1 | $1 < 5$ | go on |
| L5 | | | | $b = 1$ |
| L6 | 1 | 2 | $2 < 5$ | $b = 2$ |
| L6 | 3 | 8 | $8 \ge 5$ | stop the loop |
| L7 | | | | $a = 2$, $c = 3$ |
| L9, L10 | 2 | 4 | $4 < 5$ | $a = 3$ |
| L11 | | | | return 3 |

The answer is index 3, the id 8. The call skips $g = 3$ postings and makes 4 comparisons, which is the bound $2 \lfloor \log_2 3 \rfloor + 2 = 4$ of the next section.

## Correctness

The invariant of the structure is that the ids are strictly increasing and each frequency is at least 1. Line L1 rejects an id that would break the order, so APPEND keeps the invariant. For NEXT-GEQ, the loop of line L6 keeps $P.\mathit{ids}[lo + b - 1] < x$ with $b$ a power of 2. When it stops, the answer lies between $lo + b$ and $\min(lo + 2b - 1, n)$, and the binary search of lines L8 to L10 keeps the condition in the comment of line L8 until the range has one index. Because the ids are sorted, the indices with an id below $x$ form a prefix, so the first index past that prefix is the answer. The full proof, with the count of comparisons, is in the proof file below.

## Complexity

- APPEND: $O(1)$ amortized time, and one comparison.
- ACCESS: $O(1)$ time.
- NEXT-GEQ: let $p$ be the answer and $g = p - lo$. The call makes 1 comparison when $g = 0$, and at most $2 \lfloor \log_2 g \rfloor + 2$ comparisons when $g \ge 1$, so the time is $O(1 + \log g)$. A plain binary search over the rest of the list would cost about $\log_2(n - lo)$ comparisons, even when the answer is near $lo$.
- A sequence of $r$ calls in which each call starts at the answer of the call before it skips at most $n$ postings in total, and makes at most $2r \log_2(1 + n/r) + 2r$ comparisons by the concavity of the logarithm. This is the bound that the galloping intersections, such as [small-versus-small](/small-versus-small-intersection/), rely on.
- Build: $O(T)$ expected time for $T$ tokens, with a hash table from terms to lists.
- Space: $\Theta(n)$ words for one list, and a number of words linear in the total number of postings for all lists. That total is at most $T$.

## Variants

- **Document ids only.** For Boolean queries alone, the frequencies are not needed, and the list is one sorted array of ids.
- **With positions.** Each posting holds the sorted list of the positions of the term in the document. This is the [positional index](/positional-index/), which answers [phrase queries](/phrase-query/).
- **Compressed lists.** Gaps with a variable-length code, or [Elias-Fano encoding](/elias-fano-encoding/), cut the space to a few bits for each posting.
- **Blocked lists with skips.** The list is cut into blocks of about 64 or 128 postings, and a table holds the first id of each block, so NEXT-GEQ decodes only one block. [Skip pointers](/skip-pointers/) are the textbook form of this idea.
- **Impact-ordered lists.** For ranked retrieval, some engines sort the postings by a score instead of by id, which helps early stop but breaks the merge.

## When to use it

Use a posting list for each term whenever a collection is searched by words: it is the core of every inverted index. Use the plain array form for small or in-memory indexes and for the results of an intersection, and a compressed form with blocks for large indexes. For a term that occurs in almost every document, a [bit vector](/bit-vector/) over all ids can be smaller and faster than a list of ids.

## Pitfalls

- **Ids out of order.** If documents are added in a random order, a plain append breaks the sort, and each merge then gives wrong answers. Line L1 must test the order; a list that is not built in id order must be sorted before use.
- **Duplicate ids.** A term that occurs twice in one document must give one posting with $f = 2$, not two postings with the same id. The test in line L1 is a strict $<$; with $\le$ it would accept a duplicate.
- **Binary search from index 0.** A call NEXT-GEQ$(P, x, 0)$ in each step of an intersection, in place of NEXT-GEQ$(P, x, p)$ from the last answer $p$, makes the cost of each step about $\log_2 n$ and loses the bound of $2r \log_2(1 + n/r) + 2r$.
- **Overshoot of the galloping probe.** Line L6 must test $lo + 2b - 1 < n$ before it reads the id. Line L7 must cap $c$ at $n$, else the binary search reads past the end.

## Implementations

## History

Inverted files with sorted lists of record numbers are among the oldest structures of text retrieval. The books of Witten, Moffat and Bell and the survey of Zobel and Moffat describe the modern layout: document ids in increasing order, gaps between ids compressed with a variable-length code, and in-document frequencies and positions stored next to the ids. Manning, Raghavan and Schuetze use the name "postings list" in their textbook, and Buettcher, Clarke and Cormack define the interface with first, last, next and prev.

## References
