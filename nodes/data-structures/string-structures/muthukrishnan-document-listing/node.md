---
tag: QK2HK3
kind: algorithm
slug: muthukrishnan-document-listing
name: Muthukrishnan's document listing algorithm
area: data-structures/string-structures
level: research
summary: Report all documents containing a pattern in time proportional to the output size, using the document array and range-minimum queries.
solves: [document-listing]
model: word-ram
complexity:
  vars: {n: the total length of the collection, m: the length of the pattern, d: the number of documents reported}
  time: {worst: O(m + d)}
  space: {extra: O(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 2002
  people: [S. Muthukrishnan]
  note: Muthukrishnan reduced document listing to range-minimum queries on an array of previous occurrences, giving a query time linear in the pattern length and the number of documents reported.
prereqs: [suffix-array, generalized-suffix-tree, range-minimum-query]
see_also: [document-listing, top-k-document-retrieval, range-minimum-query, sparse-table, suffix-array-search, inverted-index, wavelet-tree, cartesian-tree]
sources:
  - paper: S. Muthukrishnan, Efficient algorithms for document retrieval problems, Proceedings of the 13th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 2002)
    locator: pages 657 to 666, the document listing problem, the array of previous occurrences and the listing procedure by range-minimum queries
  - paper: Kunihiko Sadakane, Succinct data structures for flexible text retrieval systems, Journal of Discrete Algorithms 5(1), 2007, doi:10.1016/j.jda.2006.03.011
    locator: pages 12 to 22, document listing with a range-minimum structure on the document array and a bit vector of reported documents instead of the array of previous occurrences
  - paper: Gonzalo Navarro, Spaces, trees, and colors, the algorithmic landscape of document retrieval on sequences, ACM Computing Surveys 46(4), 2014, doi:10.1145/2535933
    locator: article 52, the section on document listing, which presents Muthukrishnan's algorithm and its compressed variants
---

Muthukrishnan's algorithm lists the documents of a collection that contain a pattern in time $O(m + d)$, where $m$ is the length of the pattern and $d$ the number of documents reported, independent of the number of occurrences. It finds the range of the pattern in a suffix tree or suffix array of the whole collection, and then lists the distinct documents of that range with range-minimum queries on an array $C$ that points from each suffix to the previous suffix of the same document. This page covers this algorithm; the problem and other solutions are on the page of [document listing](/document-listing/).

## In plain words

Put all documents into one suffix array. The suffixes that start with the pattern form one block of it, and each suffix belongs to a document. Reading the block one by one lists every document, but a document with a million occurrences is seen a million times.

The trick is to mark, for each row of the suffix array, where the previous row of the same document is. In the block, the first row of each document points to a row before the block; every other row points inside it. So we want exactly the rows that point before the block. A range-minimum query finds the row of the block that points farthest back. If even that row points inside the block, we are done; otherwise it is a new document, and we search the two sides of it the same way.

## The problem

A collection of documents $S_0, \ldots, S_{k-1}$ of total length $n$ is given in advance and can be preprocessed. A query gives a pattern $p$ of length $m \ge 1$ and asks for the set $\{\, j : p \text{ occurs in } S_j \,\}$, each document once ([document listing](/document-listing/)). The number of occurrences $occ$ can be much larger than the number $d$ of documents in the answer, and the goal is a time that depends on $d$ only.

## The algorithm

**Preprocessing.** Concatenate the documents into $T = S_0 \$ S_1 \$ \cdots S_{k-1} \$$, with a separator $\$$ that occurs in no document and no pattern, and build its suffix array $SA$ (or a generalized suffix tree). Then build:

- the *document array* $D$, where $D[r]$ is the document that contains position $SA[r]$;
- the array $C$, where $C[r]$ is the largest $r' < r$ with $D[r'] = D[r]$, or $-1$ if there is none;
- a range-minimum structure on $C$, which returns in $O(1)$ the position of a minimum of $C[a \ldots b]$.

**Query.** Find the range $[lo, hi)$ of rows whose suffixes start with $p$, and run:

```pseudo id=main
PREPROCESS(S_0, …, S_{k−1})
L1  build SA of T = S_0 $ ⋯ S_{k−1} $;  D[r] ← the document of SA[r]
L2  for r ← 0 to |T| − 1:  C[r] ← last[D[r]] (or −1);  last[D[r]] ← r
L3  build a range-minimum structure RMQ on C

LIST(p)
L4  [lo, hi) ← the rows of SA whose suffixes start with p
L5  push [lo, hi − 1];  while the stack is not empty: pop [a, b];  if a > b, continue
L6      r ← RMQ(a, b)
L7      if C[r] ≥ lo: continue                  ▷ no first occurrence in [a, b]
L8      report D[r];  push [r + 1, b];  push [a, r − 1]
```

Line L7 is the test that makes the work proportional to $d$. The row $r$ is the *first* row of its document within $[lo, hi)$ exactly when $C[r] < lo$, so each document of the answer has exactly one such row. The minimum of $C$ over $[a, b]$ is below $lo$ if and only if $[a, b]$ contains such a row; if it does not, the whole interval is dropped with one query.

## Example

Take the documents $S_0 = $ banana, $S_1 = $ ananas and $S_2 = $ cabana, and the pattern $p = $ an. In the suffix array of $T$, the rows $6$ to $10$ start with an:

| row r | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|
| suffix | ana\$ | ana\$ananas\$⋯ | anana\$⋯ | ananas\$⋯ | anas\$⋯ |
| D[r] | 2 | 0 | 0 | 1 | 1 |
| C[r] | 5 | 4 | 7 | 2 | 9 |

So $lo = 6$. The first query on $[6, 10]$ returns $r = 9$ with $C[9] = 2 < 6$: report document 1, the first row of $S_1$ in the range (row 10 points back to it). The query on $[6, 8]$ returns $r = 7$ with $C[7] = 4 < 6$: report document 0. The query on $[6, 6]$ returns $C[6] = 5 < 6$: report document 2. The queries on $[8, 8]$ and $[10, 10]$ give $C = 7$ and $C = 9$, both at least 6, and stop. The answer is $\{1, 0, 2\}$ after 5 range-minimum queries, within the bound $2d + 1 = 7$. Here the scan of the 5 occurrences would be as fast; the gain appears when a pattern has many occurrences in few documents, since the number of queries depends on $d$ only.

## Correctness

The rows of $[lo, hi)$ with $C[r] < lo$ are the first row of each document in the range, one per document. Each popped interval is a part of $[lo, hi)$ not yet examined, the intervals on the stack are disjoint, and the minimum test at line L7 decides whether an interval contains one of these rows. So each document is reported once and none is missed. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Finding the range takes $O(m)$ time with a generalized suffix tree and $O(m \log n)$ with binary search in the suffix array. In the listing phase, each query that reports splits its interval into two, and each query that does not report ends a branch. The queries form a binary tree with $d$ internal nodes, so at most $d + 1$ queries fail, and there are at most $2d + 1$ queries in total, each $O(1)$. The query time is $O(m + d)$ with the suffix tree.

The data structures take $O(n)$ words: $SA$, $D$, $C$ and a linear-space range-minimum structure, besides the suffix tree if one is used. The preprocessing takes $O(n)$ time for an integer alphabet with a linear-time suffix array construction.

## Properties

- **Output-sensitive.** The time of the listing phase does not depend on the number of occurrences, only on $d$.
- **Unordered output.** The documents come out in the order of their first rows in the suffix array, not by document number; sorting the answer costs extra.
- **Static.** Inserting a document changes $SA$, $D$ and $C$ globally; the structure is built once for a fixed collection.
- **Constant-time step.** Each step is one range-minimum query and one comparison, so the time per document is a small constant.

## Variants and improvements

- **No array $C$.** Sadakane (2007) keeps a range-minimum structure for $C$ that answers queries without access to $C$ itself, and replaces the test $C[r] < lo$ by a bit vector that marks the documents already reported in the current query; the marks are cleared at the end. The array $D$ is also not stored, since the document of a row is computed from the compressed suffix array.
- **Compressed indexes.** With a [compressed suffix array](/compressed-suffix-array/) for the range, and a [wavelet tree](/wavelet-tree/) on $D$ instead of the explicit arrays, document listing takes space close to the compressed text; Navarro's survey describes these trade-offs.
- **Top-k retrieval.** Listing only the $k$ documents with the most occurrences of $p$ is [top-k document retrieval](/top-k-document-retrieval/), which needs different structures.

## When to use it

Use this algorithm when patterns are arbitrary substrings, not whole words, and patterns can occur many times in few documents, so that scanning the occurrences is too slow. For word queries on natural-language text, an [inverted index](/inverted-index/) answers the same question with less space. For few documents, scanning the occurrences and deduplicating them is simpler.

## Pitfalls

- **Comparing with $lo$, not $a$.** The test of line L7 uses the left end of the whole range. Comparing with the left end of the current interval reports a document again in each part where it appears.
- **Separators.** Without a separator after each document, a pattern can match across two documents, and the suffix belongs to the first while the occurrence does not exist.
- **Recursion depth.** The recursion on the two sides can be $d$ deep; an explicit stack avoids a deep call stack.
- **Ties in the minimum.** Any minimum works; a minimum with $C[r] < lo$ is always a first row, whichever is returned.

## Implementations

The Python module concatenates the documents with a separator, builds the suffix array by sorting (enough for tests), the arrays $D$ and $C$, and a sparse table for range minima, and lists the documents with an explicit stack. It counts the range-minimum queries. The tests replay the example, check empty documents and patterns that occur nowhere, and compare 600 random collections against a scan of each document, checking that the queries never exceed $2d + 1$.

## History

Before this algorithm, the usual way was to scan all $occ$ occurrences and remove duplicates. Muthukrishnan (2002) gave the reduction to range-minimum queries on the array of previous occurrences and the $O(m + d)$ bound. Sadakane (2007) adapted it to succinct data structures, and later work on compressed document retrieval, surveyed by Navarro (2014), builds on the same idea.

## References
