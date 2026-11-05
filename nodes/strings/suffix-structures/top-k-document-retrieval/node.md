---
tag: NF2VJ4
kind: problem
slug: top-k-document-retrieval
name: Top-k document retrieval
aliases:
- top-k string retrieval
area: strings/suffix-structures
level: research
summary: Report the k documents most relevant to a pattern, ranked by a frequency measure.
model: word-ram
complexity:
  vars: {n: the total length of the documents, m: the length of the pattern, k: the number of documents asked for}
  time: {query: O(m + k)}
  space: {extra: O(n)}
prereqs: [document-listing, generalized-suffix-tree]
see_also: [document-listing, generalized-suffix-tree, suffix-array, range-minimum-query, wavelet-tree, inverted-index, top-k-selection, r-index]
sources:
  - paper: doi:10.1109/FOCS.2009.19
    title: Wing-Kai Hon, Rahul Shah and Jeffrey Scott Vitter, Space-efficient framework for top-k string retrieval problems, FOCS 2009
    locator: pages 713 to 722; the first linear-space index, with O(m + k log k) query time, by storing weighted pointers between generalized suffix tree nodes
  - paper: doi:10.1137/1.9781611973099.84
    title: Gonzalo Navarro and Yakov Nekrich, Top-k document retrieval in optimal time and linear space, SODA 2012
    locator: pages 1066 to 1077; O(m + k) query time in O(n) words, by a reduction to top-k range queries on the pointers
  - paper: doi:10.1137/140998949
    title: Gonzalo Navarro and Yakov Nekrich, Time-optimal top-k document retrieval, SIAM Journal on Computing 46(1), 2017
    locator: pages 80 to 113; the journal version, also with the optimal time when the pattern is given packed in words
  - paper: doi:10.1145/2535933
    title: Gonzalo Navarro, Spaces, trees, and colors, the algorithmic landscape of document retrieval on sequences, ACM Computing Surveys 46(4), 2014
    locator: the survey of document listing and top-k retrieval, with the relevance measures, the compressed solutions and the lower bounds
---

A collection of documents $D_0, \ldots, D_{d-1}$ of total length $n$ is given in advance. A *top-k document retrieval* query gives a pattern $P$ of length $m$ and a number $k$, and asks for the $k$ documents with the highest relevance to $P$. The usual relevance is the *term frequency*, the number of occurrences of $P$ in the document. Unlike an [inverted index](/inverted-index/), the pattern is any string, not a word from a fixed vocabulary, so this is the basic query of a search engine for DNA, source code, or languages without word breaks. It extends [document listing](/document-listing/), and Navarro and Nekrich (2012) solved it in the optimal $O(m + k)$ time with $O(n)$ words.

## In plain words

You have many documents, and someone gives you a short piece of text. You must return the few documents where that piece appears most often, best first.

You could find every place where the piece appears and count per document. But a common piece can appear millions of times in only a few documents, and you want just the top ten. The aim is to answer in time that depends only on the length of the piece and on how many documents you return, not on how many times the piece appears.

The trick is to do most of the counting in advance. Index all endings of all documents in one tree. For each branch of the tree and each document, store how many times the document appears below that branch. A query then only has to pick the largest stored counts in one place.

## Definition

Let $D_0, \ldots, D_{d-1}$ be strings over an ordered alphabet $\Sigma$ of size $\sigma$, with total length $n$; positions are 0-based. For a pattern $P \in \Sigma^m$ with $m \ge 1$, let $tf(P, D_j)$ be the number of positions $i$ with $D_j[i \ldots i + m - 1] = P$. A query $(P, k)$ asks for a list of $\min(k, d_P)$ documents, where $d_P$ is the number of documents with $tf(P, D_j) > 0$, such that every listed document has a term frequency at least that of every document not listed. Ties are broken in any way; the list may or may not be sorted by relevance, and sorting $k$ items costs $O(k \log k)$ more unless the method outputs them in order.

Indexes for the problem are usually built on the concatenation $T = D_0 \$_0 D_1 \$_1 \cdots D_{d-1} \$_{d-1}$ with distinct [sentinels](/sentinel-character/) $\$_0 < \$_1 < \cdots$, all smaller than the symbols of $\Sigma$. The [suffix array](/suffix-array/) of $T$ is the generalized suffix array of the collection, and the *document array* $DA[i]$ is the document that contains the suffix $SA[i]$. The rows whose suffixes start with $P$ form one interval $[sp, ep)$, and $tf(P, D_j)$ is the number of $j$ in $DA[sp \ldots ep-1]$.

## Variants

- **Other relevance measures.** Any measure that depends on the document and on the set of occurrences in it can be used: term frequency, the position of the first occurrence, the smallest distance between two occurrences, or a fixed score of the document (such as PageRank) among those that contain $P$. Hon, Shah and Vitter handle a general class of such measures.
- **Document listing.** Report every document that contains $P$; this is top-k with $k = d$ when the order does not matter. See [document listing](/document-listing/).
- **Document counting.** Report only the number $d_P$ of documents containing $P$; Sadakane solved it in $O(m)$ time with $2n + o(n)$ bits beyond a compressed suffix array.
- **Several patterns.** For two patterns, report the documents containing both, or neither; these queries are much harder, with conditional lower bounds based on set intersection.
- **Tf-idf.** Rank by a combination of the frequencies of several patterns, weighted by their rarity across the collection; exact solutions are again harder.
- **Compressed and repetitive collections.** Solutions in space close to that of a compressed full-text index, or close to the [r-index](/r-index/) for highly repetitive collections, with higher query time.

## Examples

Take $D_0 = \texttt{banana}$, $D_1 = \texttt{anna}$ and $D_2 = \texttt{nab}$, so $n = 13$ and $|T| = 16$. The rows of the generalized suffix array that start with $\texttt{a}$ are:

| row $i$ | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|
| $SA[i]$ | 5 | 10 | 13 | 3 | 1 | 7 |
| suffix (to its sentinel) | `a$0` | `a$1` | `ab$2` | `ana$0` | `anana$0` | `anna$1` |
| $DA[i]$ | 0 | 1 | 2 | 0 | 0 | 1 |

For $P = \texttt{a}$, the interval is $[3, 9)$ and the counts in $DA[3 \ldots 8]$ are 3 for $D_0$, 2 for $D_1$ and 1 for $D_2$. So the query $(\texttt{a}, 2)$ returns $D_0$ and $D_1$. For $P = \texttt{an}$ the interval is $[6, 9)$, with term frequencies 2, 1 and 0, and $(\texttt{an}, 1)$ returns $D_0$.

| pattern | $tf$ in $D_0, D_1, D_2$ | top 2 |
|---|---|---|
| a | 3, 2, 1 | $D_0$, $D_1$ |
| an | 2, 1, 0 | $D_0$, $D_1$ |
| na | 2, 1, 1 | $D_0$, then $D_1$ or $D_2$ |
| n | 2, 2, 1 | $D_0$, $D_1$ |
| ana | 2, 0, 0 | $D_0$ |
| b | 1, 0, 1 | $D_0$, $D_2$ |

A script checks these counts against a direct count in each document, and checks on random collections over alphabets of size 1, 2 and 4 that the counts in the $DA$ interval equal the term frequencies.

## Known algorithms

| method | query time | space | notes |
|---|---|---|---|
| Count in the $DA$ interval, then select | $O(m + occ + k \log k)$ | $O(n)$ words | $occ$ is the number of occurrences, which may be far larger than $k$ |
| Inverted index | fast for whole words | $O(n)$ | only for patterns that are words of a fixed vocabulary |
| Muthukrishnan (2002), chain array | $O(m + d_P)$ for listing | $O(n)$ words | lists the distinct documents with [range minimum queries](/range-minimum-query/); does not rank them |
| Hon, Shah and Vitter (2009) | $O(m + k \log k)$ | $O(n)$ words | the first linear-space top-k index |
| Navarro and Nekrich (2012) | $O(m + k)$ | $O(n)$ words | optimal time, output in no fixed order |
| Compressed indexes | $O(m)$ plus polylogarithmic time per document | close to compressed text size | [wavelet trees](/wavelet-tree/) on $DA$ and sampled frequencies; see the Navarro survey |

The idea of Hon, Shah and Vitter: in the [generalized suffix tree](/generalized-suffix-tree/), mark for each document $j$ the leaves of $D_j$ and the lowest common ancestors of consecutive marked leaves. From each marked node, a pointer goes to the nearest marked ancestor for the same document, with a weight equal to the number of leaves of $D_j$ in the subtree of the node where it starts. The documents relevant to the locus $v$ of $P$ are the pointers that start inside the subtree of $v$ and end above $v$, there is at most one per document, and their weights are the term frequencies. With nodes numbered in preorder, this is a 3-sided range query that asks for the $k$ largest weights. Navarro and Nekrich solve that range query in $O(k)$ time after the locus is found.

## Bounds

Any algorithm must read the pattern and output the answer, so $\Omega(m + k)$ time, and the Navarro and Nekrich index matches this in $O(n)$ words. When $P$ is given packed, $\Theta(m \log \sigma / w)$ words, the journal version also reaches the matching bound with $w$ the word size. For compressed space, the survey describes trade-offs between the size of the index and the time per reported document; whether $O(m + k)$ time is possible within compressed space is open.

## Reductions

- **Document listing to 3-sided range reporting.** Muthukrishnan's chain array $C[i]$ is the largest $i' < i$ with $DA[i'] = DA[i]$, or $-1$. Inside $[sp, ep)$, the first row of each document is the row with $C[i] < sp$, so the distinct documents are the rows $i$ in $[sp, ep)$ with $C[i] < sp$, found by repeated range minimum queries. In the example for $\texttt{a}$, $C[3 \ldots 8] = 0, 1, 2, 3, 6, 4$ and the rows 3, 4 and 5 have $C < 3$, giving $D_0$, $D_1$ and $D_2$.
- **Top-k to top-k range queries.** The pointer framework above turns the query into: among the points in a rectangle that is unbounded on one side, report the $k$ with the largest weights.
- **From set intersection.** Two-pattern queries are at least as hard as set intersection queries, which gives conditional lower bounds for them; the single-pattern problem has no such barrier.

## Applications

- Search in collections of DNA or protein sequences, where there are no words and any substring may be a query.
- Search in East Asian text, and in source code and log files, where word breaks are not reliable.
- Ranking versions of documents in repositories and archives, with compressed indexes that use the repetition between versions.
- Autocompletion and query suggestion, where the pattern is a prefix and documents are ranked by a fixed score.

## References
