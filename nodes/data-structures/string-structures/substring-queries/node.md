---
tag: ZXH7VG
kind: problem
slug: substring-queries
name: Substring queries
aliases:
- substring search in an index
area: data-structures/string-structures
level: core
summary: Preprocess a text so that occurrences of any query pattern can be found quickly.
prereqs: [prefix-matching, suffix-array, suffix-tree]
see_also: [full-text-index, suffix-tree, suffix-array-search, fm-index, prefix-matching, string-matching, document-listing, inverted-index]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences
    locator: Chapter 7 (First applications of suffix trees), Section 7.1, exact string matching with a suffix tree of the text
  - paper: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5), 1993, doi:10.1137/0222058
    locator: pages 935 to 948, the search in O(m + log n) time with LCP information
  - paper: Gonzalo Navarro and Veli Mäkinen, Compressed full-text indexes, ACM Computing Surveys 39(1), 2007, doi:10.1145/1216370.1216372
    locator: Section 3 (basic concepts, the count, locate and extract queries) and the tables comparing compressed indexes
  - paper: Paolo Ferragina and Giovanni Manzini, Opportunistic data structures with applications, Proceedings of the 41st Annual Symposium on Foundations of Computer Science (FOCS 2000), doi:10.1109/SFCS.2000.892127
    locator: pages 390 to 398, counting occurrences in O(m) time with a compressed index
---

Substring queries are the indexed form of [string matching](/string-matching/): a text $T$ of length $n$ is given once, and then many patterns $P$ arrive, each of length $m$, and for each one the task is to count or list the positions where $P$ occurs in $T$. Because a pattern occurs at position $i$ exactly when it is a prefix of the suffix $T[i ..]$, the problem is [prefix matching](/prefix-matching/) on the set of suffixes of $T$. A [suffix tree](/suffix-tree/) answers a query in $O(m + occ)$ time, a [suffix array](/suffix-array/) in $O(m \log n + occ)$ or $O(m + \log n + occ)$ time, and compressed indexes such as the [FM-index](/fm-index/) in space close to that of the compressed text. The data type that supports these queries is the [full-text index](/full-text-index/); this page is about the query problem and its bounds.

## In plain words

You have a long text, such as a book, a genome or a log file, and you will search it many times for different words or pieces of words. Scanning the whole text for each search is slow when the text is long and the searches are many.

The trick is to look at the text as the list of all its endings: the text from position 0, from position 1, and so on. A pattern occurs at a position exactly when the ending there starts with the pattern. If the endings are sorted, all endings that start with the pattern sit next to each other, and a search finds that block quickly. The positions in the block are the answers.

## Definition

**Input.** A text $T \in \Sigma^n$ over an alphabet of size $\sigma$, given for preprocessing. Then queries $P \in \Sigma^m$.

**Output.** One of the three standard queries.

- **Count.** The number $occ$ of positions $i$ with $T[i .. i+m-1] = P$.
- **Locate.** The set of these positions, in any order.
- **Exists.** Whether $occ > 0$.

Indexes that do not keep $T$ also support **extract**: given $i$ and $\ell$, return $T[i .. i+\ell-1]$. An index that supports extract replaces the text and is called a *self-index*.

The occurrences may overlap. In "banana", the pattern "ana" occurs at positions 1 and 3, counting from 0, and the two occurrences share the symbol at position 3.

## Variants

- **Online, or no preprocessing.** If each text is searched once, the right tools are scanning algorithms such as [Knuth-Morris-Pratt](/knuth-morris-pratt/) and [Boyer-Moore](/boyer-moore/), in $O(n + m)$ time per query.
- **Many documents.** The text is a collection of documents and the output is the set of documents that contain $P$, each reported once. This is [document listing](/document-listing/), solved by Muthukrishnan's method in $O(m + d)$ time for $d$ documents.
- **Word queries.** If queries are whole words, an [inverted index](/inverted-index/) from words to positions is smaller and faster. It cannot find a pattern that starts in the middle of a word.
- **Dynamic text.** The text changes by insertions and deletions between queries, which needs dynamic indexes.
- **Approximate queries.** Occurrences with up to $k$ mismatches or edits, a harder problem with indexes whose size or time grows exponentially with $k$.
- **Longest repeat and similar.** Many questions about $T$ alone, such as the longest repeated substring or the number of distinct substrings, are solved on the same structures; see [distinct substrings counting](/distinct-substrings-counting/).

## Examples

Let $T$ = banana, with positions 0 to 5. Its suffixes in sorted order give the suffix array $SA = [5, 3, 1, 0, 4, 2]$:

| rank | $SA$ | suffix |
|---|---|---|
| 0 | 5 | a |
| 1 | 3 | ana |
| 2 | 1 | anana |
| 3 | 0 | banana |
| 4 | 4 | na |
| 5 | 2 | nana |

| pattern | rank interval | count | positions |
|---|---|---|---|
| a | 0 to 2 | 3 | 1, 3, 5 |
| ana | 1 to 2 | 2 | 1, 3 |
| na | 4 to 5 | 2 | 2, 4 |
| ban | 3 to 3 | 1 | 0 |
| nab | empty | 0 | none |

For "ana", a binary search finds the first suffix not smaller than "ana", which is rank 1, and the last suffix that starts with "ana", which is rank 2. The count is the length of the interval and the positions are $SA[1] = 3$ and $SA[2] = 1$.

## Known algorithms

| index | space | count | locate |
|---|---|---|---|
| none, scan with KMP | the text | $O(n + m)$ | $O(n + m)$ |
| [suffix tree](/suffix-tree/) | $O(n)$ words | $O(m)$ with constant time child access | $O(m + occ)$ |
| [suffix array](/suffix-array/) and [binary search](/suffix-array-search/) | $n$ words plus the text | $O(m \log n)$ | $O(m \log n + occ)$ |
| suffix array with LCP arrays (Manber and Myers) | about $3n$ words plus the text | $O(m + \log n)$ | $O(m + \log n + occ)$ |
| [FM-index](/fm-index/) | about $n H_k$ bits plus lower order terms | $O(m)$ for small alphabets | $O(m + occ \cdot s)$ with a sample of one position in $s$ |
| [compressed suffix array](/compressed-suffix-array/) | $O(n \log \sigma)$ bits or entropy bounded | $O(m \log n)$ or better | a polylogarithmic cost per occurrence |

Here $H_k$ is the empirical entropy of order $k$ of $T$, and the space of the compressed indexes includes the text, which they can extract. The suffix tree and the suffix array are built in $O(n)$ time for integer alphabets.

**From an interval to positions.** All indexes in the table first find the rank interval $[l, r]$ of the suffixes that start with $P$, which gives the count $r - l + 1$. Locating then reads $SA[l .. r]$. In a suffix array this costs $O(1)$ per position. In an FM-index, $SA$ is kept only at sampled ranks, and each other position is found by walking backward with the LF mapping until a sample is reached.

## Bounds

**Lower bound $\Omega(m + occ)$ for locate.** Each symbol of $P$ must be read, by the same argument as for [prefix matching](/prefix-matching/), and each of the $occ$ positions must be reported. The suffix tree with constant time child access meets this bound, so the problem is solved optimally in time with $O(n)$ words of space.

**Space.** An index that can extract the text must store at least $\lg \sigma^n = n \lg \sigma$ bits in the worst case, since it determines $T$. The FM-index and related self-indexes use $n H_k(T) + o(n \log \sigma)$ bits for small $k$, which is close to the size of the text compressed with a model of order $k$ (Navarro and Mäkinen 2007).

**Time and space together.** Compressed indexes pay for locate: with a sampling step $s$, the space for the samples is $O((n/s) \log n)$ bits and each position costs $O(s)$ steps. Reaching $O(m + occ)$ locate time in compressed space needs further structures.

## Reductions

- **To prefix matching on suffixes.** $P$ occurs at $i$ if and only if $P$ is a prefix of $T[i ..]$. So the occurrences are the answer of [prefix matching](/prefix-matching/) on the $n$ suffixes, and the [suffix trie](/suffix-trie/) and [suffix tree](/suffix-tree/) are the trie and the [radix tree](/radix-tree/) of these suffixes.
- **Count to an interval.** In the sorted order of the suffixes, the suffixes with prefix $P$ form one interval, by the interval property of the [string symbol table](/string-symbol-table/). Counting is finding the two ends.
- **From string matching.** Each instance of single-pattern string matching is a substring query with one query, so the indexed problem cannot be easier than reading the text once at preprocessing.
- **To document listing.** With a separator between documents and an array that maps each position to its document, the documents of the positions in the interval are the answer to [document listing](/document-listing/), with repeats.

## Applications

- **Genomics.** Read aligners map millions of short DNA reads against a reference genome by substring queries on an FM-index of the genome.
- **Code and log search.** Tools that search large code bases or logs for arbitrary substrings use suffix arrays or indexes of short substrings.
- **Data compression.** Finding the longest earlier match at each position, as in [LZ77](/lz77/), is a series of substring queries on the text read so far.
- **Text processing.** Finding repeats, the longest common substring of two texts, and the number of distinct substrings all start from the structures that answer substring queries.

## References
