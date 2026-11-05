---
tag: XY0H37
kind: problem
slug: keyword-in-context-search
name: Keyword-in-context search
area: strings/suffix-structures
level: core
summary: Problem of listing every occurrence of a query string in a text along with surrounding context, solved with a suffix array.
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the query, k: the number of occurrences, w: the context width}
  time: {worst: O(m log n + k (m + w))}
prereqs: [suffix-array, suffix-array-search, full-text-index]
see_also: [full-text-index, suffix-array-search, inverted-index, longest-repeated-substring, string-matching, fm-index]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Chapter 6 (Context), the section on suffix arrays, with the KWIC client and the suffix array API
  - paper: doi:10.1137/0222058
    title: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5), 1993
    locator: pages 935 to 948, the search for all occurrences of a pattern as one interval of the suffix array
  - paper: Hans Peter Luhn, Key word-in-context index for technical literature (KWIC index), American Documentation 11(4), 1960
    locator: pages 288 to 295, the KWIC index of titles
---

Keyword-in-context (KWIC) search is the problem of listing every occurrence of a query string $P$ in a text $T$, each one with the $w$ symbols of text before it and after it. It is a client of a [full-text index](/full-text-index/): with the [suffix array](/suffix-array/) of $T$, all occurrences form one interval of ranks, found by two [binary searches](/suffix-array-search/), and each occurrence is printed from its text position. The listing comes out sorted by the text that follows the query, which is the order of a concordance. The cost is $O(m \log n)$ for the search plus the size of the output.

## In plain words

A concordance is an old tool of scholars: for a word, it lists each place in a book where the word appears, with a few words before and after it, so you can see how the word is used. A search engine shows the same thing when it prints a short piece of text around each match.

To build this for any query, sort all endings of the text once. Every ending that starts with the query is in one block of the sorted list, and two binary searches find the edges of that block. Each ending in the block gives one match. For each one, print a little of the text before the start, the query, and a little of the text after it. Because the list is sorted, the matches come out in the order of what follows the query.

## Definition

**Input.** A text $T = T[0 \ldots n-1]$ over an ordered alphabet, a query $P = P[0 \ldots m-1]$ with $m \ge 1$, and a context width $w \ge 0$. Indices are 0-based.

**Output.** For each $i \in \mathrm{Occ}(T, P) = \{ i : T[i \ldots i+m-1] = P \}$, the triple

$$\bigl(\, T[\max(0, i-w) \ldots i-1],\ P,\ T[i+m \ldots \min(n, i+m+w) - 1] \,\bigr),$$

the left context, the keyword and the right context. The order of the output is part of the specification. The usual order is the lexicographic order of the suffixes $T[i \ldots n-1]$, which is the order of the suffix array. Another common order is by position $i$.

**The method.** Let $SA$ be the suffix array of $T$, without a sentinel. The suffixes that start with $P$ are those of the ranks $lo \le r < hi$, where $lo$ is the first rank whose suffix is not smaller than $P$, and $hi$ is the first rank whose suffix is larger than $P$ and does not start with $P$. Both are found by [binary search on the suffix array](/suffix-array-search/), and the occurrences are $SA[lo], \ldots, SA[hi-1]$, in suffix order.

## Variants

- **Word boundaries.** Report only occurrences that start and end at word boundaries, so that "the" does not match inside "other". Filter the interval, or index only the suffixes that start a word (a sparse suffix array).
- **Context in words.** The context is $w$ words, not $w$ symbols, as in a printed concordance.
- **Case folding and normalization.** Search on a normalized copy of the text and print from the original.
- **Counting only.** Return $hi - lo$, the number of occurrences, in $O(m \log n)$ time without listing them.
- **Many documents.** For a collection, report each document once: that is [document listing](/document-listing/).
- **The KWIC index.** The original KWIC index of Luhn lists every significant word of every title, in alphabetical order of the keyword, with the rest of the title around it. This is the same output for all keywords at once.

## Examples

The text $T$ = `it was the best of times it was the worst of times` has $n = 50$ symbols, with positions starting at 0. The query is `the`, with $w = 6$.

| rank in $SA$ | position | left context | keyword | right context |
|---|---|---|---|---|
| 43 | 7 | `t was ` | `the` | ` best ` |
| 44 | 32 | `t was ` | `the` | ` worst` |

The two occurrences are adjacent in the suffix array, at ranks 43 and 44, and they come out in the order of the right context: ` best ` before ` worst`. For the query `of` the suffix order is positions 42 and 16, because `of times` at 42 ends the text and so is a prefix of `of times it was ...` at 16, which makes it the smaller suffix. For `times` the order is 45 then 19, for the same reason. In position order they would be 16, 42 and 19, 45.

A query that does not occur, such as `age`, gives an empty interval, $lo = hi$, after the two binary searches.

## Known algorithms

| method | preprocessing | query time | notes |
|---|---|---|---|
| scan the text with [KMP](/knuth-morris-pratt/) or another [string matching](/string-matching/) algorithm | none | $O(n + m + occ \cdot w)$ | for one query, or a small text |
| [suffix array](/suffix-array/) with binary search | a [suffix array construction](/suffix-array-construction/), $O(n)$ for an integer alphabet | $O(m \log n + occ(m + w))$ | the method of Sedgewick and Wayne; the output is in suffix order |
| suffix array with LCP information (Manber and Myers) | $O(n)$ more for the LCP values | $O(m + \log n + occ(m + w))$ | the search no longer compares the pattern from its start each time |
| [suffix tree](/suffix-tree/) | $O(n)$ for an integer alphabet | $O(m \log \sigma + occ(m + w))$ | the leaves below the locus of $P$, in sorted order if the children are sorted |
| [FM-index](/fm-index/) | $O(n)$ for an integer alphabet | $O(m \log \sigma)$ to find the interval, then a locate and an extract of $m + 2w$ symbols for each occurrence | compressed, keeps no plain text |
| word-based [inverted index](/inverted-index/) | linear in the text | the posting list of the word | only for whole words |

## Bounds

- **Output.** Each reported triple has up to $m + 2w$ symbols, so a query needs $\Omega(m + occ)$ time at least, and $\Omega(occ (m + w))$ when the triples are written out in full. The suffix tree and the suffix array with LCP information reach this up to the search term.
- **Search.** With the plain suffix array, the search makes $O(\log n)$ suffix comparisons of up to $m$ symbols each, so $O(m \log n)$ time in the worst case. On typical text the comparisons stop after a few symbols.

## Reductions

- **To pattern search in a full-text index.** The problem is a `locate` query of a [full-text index](/full-text-index/) plus random access to the text, so any index that supports `locate` and `extract` solves it.
- **To the suffix array interval.** Counting the occurrences reduces to finding the interval $[lo, hi)$; the listing then costs only the output.

## Applications

- **Concordances and corpus linguistics.** Tools that study how words are used print each occurrence of a word or phrase with its context, sorted by the following words.
- **Search result snippets.** A search engine shows a short window of text around each match.
- **Code search.** Tools that search large code bases for any substring show each hit with its surrounding lines.
- **Library catalogs.** The KWIC index of titles, introduced by Luhn at IBM, was printed for technical literature from the 1960s.

## References
