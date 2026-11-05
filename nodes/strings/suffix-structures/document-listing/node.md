---
tag: X1V9RZ
kind: problem
slug: document-listing
name: Document listing
aliases:
- document retrieval
area: strings/suffix-structures
level: research
summary: Report every document in a collection that contains a given pattern.
model: word-ram
complexity:
  vars: {n: the total length of the documents, m: the length of the pattern, D: the number of documents, d: the number of documents that contain the pattern}
  time: {worst: O(m + d)}
  space: {extra: O(n)}
prereqs: [generalized-suffix-tree, suffix-array, range-minimum-query]
see_also: [top-k-document-retrieval, generalized-suffix-tree, full-text-index, wavelet-tree, compressed-suffix-array, range-minimum-query, inverted-file-index, suffix-array-search]
sources:
  - paper: "S. Muthukrishnan, Efficient algorithms for document retrieval problems, Proceedings of the 13th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 2002), 657-666"
  - paper: doi:10.1016/j.jda.2006.03.011
    title: Kunihiko Sadakane, Succinct data structures for flexible text retrieval systems, Journal of Discrete Algorithms 5(1), 2007
    locator: pages 12 to 22, document listing and document counting with a compressed suffix array and a succinct range minimum structure
  - paper: doi:10.1007/978-3-540-73437-6_22
    title: Niko Välimäki and Veli Mäkinen, Space-efficient algorithms for document retrieval, CPM 2007, LNCS 4580
    locator: pages 205 to 215, document listing with a wavelet tree on the document array
  - paper: doi:10.1145/2535933
    title: Gonzalo Navarro, Spaces, trees, and colors, the algorithmic landscape of document retrieval on sequences, ACM Computing Surveys 46(4), 2014
    locator: pages 1 to 47, the survey of document listing, document counting and top-k retrieval
---

Document listing asks, for a collection of $D$ documents of total length $n$ and a pattern $P$ of length $m$, for the set of the documents that contain $P$, each reported once. A plain [full-text index](/full-text-index/) reports all $z$ occurrences of $P$, and $z$ can be much larger than the number $d$ of documents in the answer, for example when a short pattern occurs thousands of times in a few documents. Muthukrishnan solved the problem in 2002 in $O(m + d)$ time and $O(n)$ words, with a [generalized suffix tree](/generalized-suffix-tree/) or suffix array, a document array and [range minimum queries](/range-minimum-query/) on an array of previous occurrences. Later work brought the space down to that of a compressed index.

## In plain words

You have many documents and a word. You want the list of documents that contain the word, and you want each document only once.

An index of all the text finds every place where the word occurs. But a common word can occur a thousand times in the same few documents, and going through all those places to find a short list is a waste.

The trick is to look only at the first place of each document. All places where the word occurs form one block of a sorted list. For each entry of the list, remember where the previous entry of the same document is. An entry is the first of its document in the block if that previous entry lies before the block. A range minimum query finds such an entry at once, and you split the block there and go on.

## Definition

**Input.** A collection of documents $S_0, \ldots, S_{D-1}$ over an ordered alphabet, of total length $n$, given once for preprocessing. Then queries, each a nonempty pattern $P$ of length $m$.

**Output.** For each query, the set $\{ j : P \text{ occurs in } S_j \}$, each document once, in any order. Its size is $d$, and $d \le \min(D, z)$, where $z$ is the number of occurrences of $P$ in all documents.

**The standard setting.** Concatenate the documents into $T = S_0 \$_0 S_1 \$_1 \cdots S_{D-1} \$_{D-1}$, where the separators $\$_j$ are distinct and smaller than every symbol, and indices are 0-based. Let $SA$ be the suffix array of $T$. The occurrences of $P$ are the suffixes in one range $SA[sp \ldots ep]$, found by the suffix tree or by [suffix array search](/suffix-array-search/), and none of them crosses a separator, since $P$ has no separator. Two arrays describe the documents:

- the *document array* $DA[i]$: the document that contains the position $SA[i]$;
- the *previous array* $C[i] = \max\{ j < i : DA[j] = DA[i] \}$, or $-1$ if there is none.

**The key fact.** A rank $i$ in $[sp..ep]$ holds the leftmost occurrence of its document in the range if and only if $C[i] < sp$. So the answer is $\{ DA[i] : sp \le i \le ep, \ C[i] < sp \}$, and each document of the answer comes from exactly one such $i$.

**Muthukrishnan's listing.** Take $k = \mathrm{RMQ}_C(sp, ep)$, the position of a minimum. If $C[k] \ge sp$, no rank in the range has $C < sp$, so stop. Otherwise report $DA[k]$ and repeat on $[sp..k-1]$ and $[k+1..ep]$. Each query that reports a document creates at most two more queries, so there are at most $2d + 1$ range minimum queries, and the listing takes $O(d)$ time after the range is found.

## Variants

- **Document counting.** Report only $d$. Sadakane gives $d$ in $O(1)$ time after the range is found, with a structure of $2n + o(n)$ binary digits.
- **Top-$k$ retrieval.** Report the $k$ documents in which $P$ occurs most often, or that score highest by another measure; see [top-$k$ document retrieval](/top-k-document-retrieval/).
- **Document listing with frequencies.** Report each document with the number of occurrences of $P$ in it.
- **Several patterns.** Report the documents that contain all of the patterns, or any of them. These need more than range minima, and the known bounds are weaker.
- **Dynamic collections.** Documents are added and deleted between the queries.

## Examples

The collection is $S_0 = \texttt{banana}$, $S_1 = \texttt{ananas}$ and $S_2 = \texttt{nab}$, so $D = 3$ and $T = \texttt{banana}\$_0\texttt{ananas}\$_1\texttt{nab}\$_2$, of length 18, with $\$_0 < \$_1 < \$_2$ smaller than the letters.

| $i$ | $SA[i]$ | suffix (start) | $DA[i]$ | $C[i]$ |
|---|---|---|---|---|
| 0 | 6 | `$0ananas` | 0 | -1 |
| 1 | 13 | `$1nab` | 1 | -1 |
| 2 | 17 | `$2` | 2 | -1 |
| 3 | 5 | `a$0` | 0 | 0 |
| 4 | 15 | `ab$2` | 2 | 2 |
| 5 | 3 | `ana$0` | 0 | 3 |
| 6 | 1 | `anana$0` | 0 | 5 |
| 7 | 7 | `ananas$1` | 1 | 1 |
| 8 | 9 | `anas$1` | 1 | 7 |
| 9 | 11 | `as$1` | 1 | 8 |
| 10 | 16 | `b$2` | 2 | 4 |
| 11 | 0 | `banana$0` | 0 | 6 |
| 12 | 4 | `na$0` | 0 | 11 |
| 13 | 14 | `nab$2` | 2 | 10 |
| 14 | 2 | `nana$0` | 0 | 12 |
| 15 | 8 | `nanas$1` | 1 | 9 |
| 16 | 10 | `nas$1` | 1 | 15 |
| 17 | 12 | `s$1` | 1 | 16 |

**Query `ana`.** The range is $[5..8]$, with $z = 4$ occurrences and $C[5 \ldots 8] = [3, 5, 1, 7]$. The minimum is $C[7] = 1 < 5$: report document 1. On $[5..6]$ the minimum is $C[5] = 3 < 5$: report document 0. On $[6..6]$, $C[6] = 5 \ge 5$, and on $[8..8]$, $C[8] = 7 \ge 5$: stop. The answer is $\{0, 1\}$ after 4 range minimum queries, and the ranks 6 and 8, which are second occurrences, are never reported.

**Query `na`.** The range is $[12..16]$, with $z = 5$. The minima are $C[15] = 9$ (document 1), then on $[12..14]$, $C[13] = 10$ (document 2), then on $[12..12]$, $C[12] = 11$ (document 0), all below 12. The ranks 14 and 16 have $C = 12$ and $C = 15$ and stop the search. The answer is all three documents.

**Query `a`.** The range is $[3..9]$, with $z = 7$ and $d = 3$: the ranks 3, 7 and 4 have $C = 0, 1, 2$, below 3, and give the documents 0, 1 and 2.

## Known algorithms

| method | space | query time | notes |
|---|---|---|---|
| list all occurrences and remove repeats | $O(n)$ words | $O(m + z)$ | a mark per document, cleared after the query |
| Matias, Muthukrishnan, Sahinalp and Ziv, 1998 | $O(n)$ words | $O(m \log D + d)$ | a suffix tree augmented with document information |
| Muthukrishnan, 2002 | $O(n)$ words | $O(m + d)$ | suffix tree, $DA$, $C$ and $O(1)$ range minima; optimal |
| Sadakane, 2007 | a compressed suffix array plus $O(n)$ binary digits | $O(t_{\mathrm{search}}(m) + d \cdot t_{SA})$ | $C$ is not stored, see below |
| Välimäki and Mäkinen, 2007 | a compressed suffix array plus a [wavelet tree](/wavelet-tree/) on $DA$, about $n \log D$ binary digits | $O(t_{\mathrm{search}}(m) + d \log D)$ | lists the distinct values of $DA[sp \ldots ep]$ with the wavelet tree |
| an [inverted index](/inverted-file-index/) | compressed lists of documents per word | fast, but only for whole words | the usual method for natural language text |

**Sadakane's method.** A range minimum structure of $2n + o(n)$ binary digits answers $\mathrm{RMQ}_C$ without $C$. The test $C[k] < sp$ is replaced by a mark per document: the listing visits $k$, then its left part, then its right part, so all leftmost occurrences before a rank are reported before it. A rank whose document is already marked is therefore not a leftmost occurrence, and the recursion stops there. $DA[k]$ comes from $SA[k]$ by a rank query on a bit vector that marks the starts of the documents.

## Bounds

- **Upper bound.** $O(m + d)$ time with $O(n)$ words (Muthukrishnan), for an alphabet in which the child of a suffix tree node is found in $O(1)$ time, for example with perfect hashing.
- **Lower bound.** $\Omega(m + d)$: the query must read the pattern and write the answer. So Muthukrishnan's bound is optimal in time.
- **Space.** In compressed space, the known solutions pay a factor such as $t_{SA}$ or $\log D$ for each reported document; the survey of Navarro compares them.

## Reductions

- **To range minimum.** Listing the distinct values in a range of $DA$ reduces to range minima on $C$, by the key fact. This is the *colored range listing* problem: report the distinct colors in a range of an array.
- **To two-dimensional range queries.** The ranks $i$ with $sp \le i \le ep$ and $C[i] < sp$ are the points $(i, C[i])$ in a three-sided range, so a structure for three-sided range reporting also solves the problem.

## Applications

- **Genome and protein collections.** Find the genomes or the proteins that contain a motif, where the texts have no words and an inverted index does not apply.
- **Source code and logs.** Find the files that contain a string, such as an identifier, in a large code base.
- **Text in East Asian languages.** In languages written without spaces, words are hard to find, and a full-text index over the characters is a common choice.
- **Version collections.** Find the versions of a document, or the snapshots of a web page, that contain a string; there, the collection is highly repetitive, and indexes such as the [r-index](/r-index/) are used.

## References
