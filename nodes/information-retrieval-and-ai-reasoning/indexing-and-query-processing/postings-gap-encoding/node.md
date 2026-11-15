---
tag: NG3066
kind: technique
slug: postings-gap-encoding
name: Postings gap encoding
aliases:
- d-gaps
- docid gaps
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Stores the differences between consecutive document ids of a posting list, which are small and compress well with integer codes.
prereqs: [posting-list, delta-encoding]
see_also: [variable-byte-encoding, elias-gamma-coding, golomb-coding, simple-9, pfor-delta, interpolative-coding, elias-fano-encoding, document-identifier-reassignment]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 5, Section 5.3 (postings file compression, with the gaps of a posting list), Section 5.3.1 (variable byte codes) and Section 5.3.2 (gamma codes)
  - book: isbn:9781558605701
    title: Ian H. Witten, Alistair Moffat and Timothy C. Bell, Managing Gigabytes, Compressing and Indexing Documents and Images, second edition, Morgan Kaufmann, 1999
    locator: the chapter on indexing, the compression of inverted files by coding the gaps between document numbers with Elias and Golomb codes, and the global and local models for the gaps
  - paper: doi:10.1145/1132956.1132959
    title: Justin Zobel and Alistair Moffat, Inverted files for text search engines, ACM Computing Surveys 38(2), 2006
    locator: the section on index compression, with the d-gaps of document numbers, the choice of codes and the cost of decoding
  - paper: "Giulio Ermanno Pibiri and Rossano Venturini, Techniques for inverted index compression, ACM Computing Surveys, 2021, arXiv 1908.10598"
    title: Techniques for inverted index compression
    locator: the sections on integer codes and on list codes, which take the gaps of a sorted list as their input
---

Postings gap encoding stores a [posting list](/posting-list/) $d_1 < d_2 < \cdots < d_k$ of document ids as the first id and then the gaps $d_2 - d_1, \ldots, d_k - d_{k-1}$. It codes each gap with a code that gives short words to small integers. The gaps of a list for a term in $k$ of $N$ documents add up to at most $N$, so on average they are about $N/k$. That is much smaller than $N$ for common terms, and a code for small integers then spends far fewer bits than a fixed width of $\lceil \lg N \rceil$. This page is the technique as it is used in an inverted index: the gaps, the choice of code, and the skips that make up for the loss of random access. The general transform of a sequence into its differences, also for signed data, is [delta encoding](/delta-encoding/). The codes themselves each have a page, such as [variable-byte encoding](/variable-byte-encoding/), [Elias gamma coding](/elias-gamma-coding/) and [Simple-9](/simple-9/).

## In plain words

A posting list holds the numbers of the documents that contain a word, in increasing order. When a word is common, the numbers in its list are close to each other. So do not write the numbers. Write the first number, and then how far each number is from the one before it. These steps are small, often 1 or 2, even when the numbers are large. Small numbers can be written with few bits if the code gives short forms to small numbers. To read the list, add the steps back up from the start. The cost is that you can no longer jump into the middle of the list, so a few full numbers are kept at fixed places as starting points.

## When it applies

- The ids of each list are distinct and sorted, so every gap is at least 1. This is how [posting lists](/posting-list/) are built.
- Lists are read from the start, as in the merge of a [list intersection](/merge-based-list-intersection/) or a term-at-a-time pass. Jumps into a list are rare or go through [skip pointers](/skip-pointers/).
- The ids of related documents are close, or the list is long. The gaps are then small. If a term is in only a few documents of a large collection, the gaps are large and the gain is small.
- The same idea applies inside a [positional index](/positional-index/) to the word positions in one document, which are also sorted.

The gain has a simple bound. If the $k$ gaps $g_1, \ldots, g_k$ add up to at most $N$, then by the concavity of the logarithm $\sum_i \lg g_i \le k \lg(N/k)$. So the Elias gamma code, with $2 \lfloor \lg g \rfloor + 1$ bits for a gap $g$, spends at most $k(2 \lg(N/k) + 1)$ bits on the list. The least number of bits for any code of $k$ ids out of $N$ is $\lg \binom{N}{k} \approx k \lg(N/k) + 1.44k$ for $k \ll N$, the [information-theoretic bound](/information-theoretic-bound/).

## The template

The template has two holes. CODE is a code for integers at least 1, with its decoder DECODE. B is the number of ids between two skip entries.

```pseudo id=main
GAP-ENCODE(d[1..k], CODE, B)              ▷ d[1] < d[2] < ... < d[k], ids from 1
L1  prev ← 0, out ← empty, skips ← empty
L2  for i ← 1 to k do
L3      if (i - 1) mod B = 0 then append (prev, the bit position of out) to skips    ▷ hole B
L4      append CODE(d[i] - prev) to out                                            ▷ hole CODE
L5      prev ← d[i]
L6  return out, skips

GAP-DECODE(out, k, DECODE)
L7  prev ← 0
L8  for i ← 1 to k do
L9      g ← DECODE(the next code word of out)
L10     prev ← prev + g, and emit prev
```

The first gap is $d_1 - 0 = d_1$, so the list needs no separate first value, and ids start from 1 so that every gap is at least 1. Decoding is a running sum, a [prefix sum](/prefix-sums/) of the gaps. To find the first id at least $x$, search the skip entries for the last one whose id is below $x$, start the running sum there with prev set to its id, and decode at most $B$ gaps.

## Classic examples

Take the list of 10 ids $3, 7, 21, 22, 60, 150, 151, 400, 420, 999$ in a collection of $N = 1000$ documents. A fixed width of $\lceil \lg 1000 \rceil = 10$ bits gives 100 bits. The gaps are $3, 4, 14, 1, 38, 90, 1, 249, 20, 579$.

- **[Variable-byte encoding](/variable-byte-encoding/).** Seven data bits and a flag bit in each byte. Eight gaps fit in one byte and two need two, so the list takes 12 bytes, 96 bits. The code is byte-aligned and fast to decode.
- **[Elias gamma coding](/elias-gamma-coding/).** A gap $g$ takes $2 \lfloor \lg g \rfloor + 1$ bits: 3, 5, 7, 1, 11, 13, 1, 15, 9 and 19, which is 84 bits. The bound above gives at most 143.
- **[Elias delta coding](/elias-delta-coding/).** The length of the gap is itself coded in gamma, which gives 79 bits. It wins over gamma on large gaps.
- **[Golomb coding](/golomb-coding/).** If each document holds the term with the same chance $k/N$, the gaps follow a geometric law, and a Golomb code with parameter $b \approx 0.69 N/k$ is close to the best prefix code for them. Here $b = 69$, and the list takes 82 bits. The power of 2 nearest to $b$ gives a [Rice code](/rice-coding/), which is faster to decode.
- **[Simple-9](/simple-9/) and [PForDelta](/pfor-delta/).** These pack the gaps of several ids into one machine word or one block of 128 values with one width, so that the decoder does no bit-by-bit work.

The least possible size for any 10 ids out of 1000 is $\lg \binom{1000}{10} \approx 77.8$ bits, so on this list gamma, delta and Golomb are all within 7 bits of it.

## Variations

- **Local and global models.** A global Golomb parameter uses one value of $b$ for all lists, and a local one uses $b \approx 0.69 N/k$ for each list. The local model fits each term better at the cost of one stored parameter per list.
- **No gaps at all.** [Interpolative coding](/interpolative-coding/) codes the middle id of a list within the range its neighbors allow, and recurses, so it codes ids, not gaps. [Elias-Fano encoding](/elias-fano-encoding/) stores the ids with no running sum and gives random access in constant time. [Partitioned Elias-Fano](/partitioned-elias-fano/) cuts the list into chunks that each fit their local density.
- **Smaller gaps.** [Document identifier reassignment](/document-identifier-reassignment/) renumbers the documents so that similar ones get close ids, which makes the gaps of many lists smaller at once.
- **Other fields.** Term frequencies are at least 1 and are often coded as $f - 1$ or with gamma. Word positions inside a document are gap-coded like ids, with the gaps starting again in each document.

## Pitfalls

- **A gap of 0.** If the ids start at 0, or a list has a repeated id, a gap can be 0, and codes such as gamma and Golomb have no word for 0. Number the ids from 1, or code $g - 1$ with a code for integers at least 0.
- **No random access.** The id at position $i$ needs the sum of the first $i$ gaps. Without skips, a jump into a long list decodes the whole prefix.
- **The skip entries must store the id, not the gap.** A skip entry that only holds a bit position gives no id to start the running sum from.
- **Bit codes are slow to decode.** Gamma and Golomb read the list one bit at a time and branch a lot. For fast query processing, byte-aligned and word-aligned codes often win even when they take more space.
- **Short lists.** For a term in a few documents, the first gap is about as large as an id, and a per-list parameter or header can cost more than it saves.

## References
