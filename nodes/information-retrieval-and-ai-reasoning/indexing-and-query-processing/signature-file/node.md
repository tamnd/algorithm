---
tag: WA5X66
kind: data-structure
slug: signature-file
name: Signature file
aliases:
- superimposed coding index
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: advanced
summary: Stores for each document a bit signature made by OR-ing hashed term codes, so a scan rejects most documents without false negatives.
model: word-ram
complexity:
  vars: {N: the number of documents, F: the signature width in bits, m: the bits set per term, D: the number of distinct terms of a document, s: the number of query terms, w: the word size in bits, c: the number of candidates, V: the cost of checking one candidate against its document}
  time: {insert: O(m D + F/w), search: O(m s + N F/w + c V)}
  space: {total: O(N F/w)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [bloom-filter, hash-function, posting-list]
see_also: [inverted-index, bloom-filter-optimal-hash-count, bitmap-index, bit-vector, false-positive-rate, inclusion-exclusion-principle, hoeffding-inequality, boolean-retrieval-model]
sources:
  - paper: doi:10.1145/2275.357411
    title: Christos Faloutsos and Stavros Christodoulakis, Signature files, An access method for documents and its analytical performance evaluation, ACM Transactions on Office Information Systems 2(4), 267 to 288, 1984
    locator: the signature file with superimposed coding of the words of a document, the false drop probability, and the choice of the number of bits per word
  - paper: doi:10.1145/4078.4080
    title: Christos Faloutsos, Access methods for text, ACM Computing Surveys 17(1), 49 to 74, 1985
    locator: the survey of text access methods, with full text scanning, inversion, signature files and clustering
  - paper: doi:10.1145/296854.277632
    title: Justin Zobel, Alistair Moffat and Kotagiri Ramamohanarao, Inverted files versus signature files for text indexing, ACM Transactions on Database Systems 23(4), 453 to 490, 1998
    locator: the experimental comparison, with the conclusion that inverted files are distinctly superior to signature files, being faster, smaller and more functional
---

A signature file is an index that stores, for each document, one string of $F$ bits, its *signature*: each distinct term of the document is hashed to a code with $m$ bits set, and the signature is the OR of these codes, a method called superimposed coding. A query is coded in the same way, and a document can contain all the query terms only if its signature has a 1 wherever the query code has one. A sequential scan of the signatures rejects most documents with a few word operations each, never rejects a document that matches, and passes some *false drops*, which a check against the document removes. Each signature is a [Bloom filter](/bloom-filter/) of the terms of one document.

## In plain words

For every word, a fixed rule picks a few positions in a row of bits. A document gets one row: switch on the positions of every word it contains. To ask whether a document holds the word "sorted", look at the positions of "sorted" in its row. If one of them is off, the document cannot hold the word, and it is skipped.

If all of them are on, the document probably holds the word, but other words may have switched on the same positions by chance. So the documents that pass are read and checked. The rows are short and the test is fast, so a scan over all rows is cheap. A wider row with well chosen positions per word lets fewer wrong documents pass.

## The abstract type

The structure holds a sequence of documents, each an id and a set of terms. The operations are:

- INSERT$(S, d, T)$: append the document $d$ with the set of terms $T$.
- CANDIDATES$(S, Q)$: return the ids, in insertion order, of the documents whose signature covers the code of the query terms $Q$. This set contains every document whose terms include $Q$.
- SEARCH$(S, Q)$: return the ids of the documents whose terms include $Q$, in insertion order: the Boolean AND query of the [Boolean retrieval model](/boolean-retrieval-model/).

## Representation

A term $t$ has the code $\mathrm{sig}(t)$, an $F$-bit word with exactly $m$ bits set, at places chosen by a [hash function](/hash-function/) of $t$. The signature of a document with term set $T$ is $\mathrm{sig}(T) = \bigvee_{t \in T} \mathrm{sig}(t)$. The file is the array of the $N$ signatures, each $\lceil F/w \rceil$ machine words, in the order of the documents, next to the documents or their term sets, which the check reads. The code here takes the $m$ places from 16-bit pieces of a keyed BLAKE2b hash, with rejection of the pieces that would bias a place and of places already taken, so that under the model of an ideal hash every set of $m$ places is equally likely.

## Operations

```pseudo id=main
SEARCH(S, Q)
L1  q ← 0
L2  for each term t of Q do q ← q OR sig(t)            ▷ the query code
L3  R ← ()
L4  for each document d with signature s and terms T, in order do
L5      if s AND q = q then                           ▷ d is a candidate
L6          if Q ⊆ T then append d to R              ▷ the check removes false drops
L7  return R
```

INSERT computes $\mathrm{sig}(T)$ with one code for each distinct term and appends it. CANDIDATES is lines L1 to L5 without the check. The test of line L5 is one AND and one comparison per machine word of the signature.

## Example

Take $F = 32$ and $m = 2$ on the toy collection. The code of "sorted" sets the bits 18 and 27, that of "merge" the bits 3 and 29, and that of "list" the bits 0 and 29. Apply these operations.

| operation | bits set | CANDIDATES and SEARCH after it |
|---|---|---|
| INSERT $d_1$ (8 terms) | 11: 3, 4, 7, 12, 15, 16, 18, 19, 22, 27, 30 | sorted: $(d_1)$ and $(d_1)$ |
| INSERT $d_2$ (9 terms) | 14 | merge: $(d_2)$ and $(d_2)$ |
| INSERT $d_3$ (10 terms) | 14: 0, 2, 3, 7, 9, 12, 15, 18, 19, 24, 25, 26, 29, 31 | merge: $(d_2, d_3)$ and $(d_2)$; list: $(d_3)$ and $(d_3)$ |

After $d_3$, "merge" has a false drop: $d_3$ has bit 3 from "term" and bit 29 from "list", and it does not contain "merge".

With all 8 documents, the signatures have 11, 14, 14, 13, 16, 16, 14 and 12 bits set. The query "sorted" gives the candidates $d_1$, $d_2$, $d_4$, $d_6$ and $d_8$, and the check keeps $d_1$, $d_2$, $d_4$ and $d_8$. "quantum" occurs in no document and still has the candidate $d_5$. The query $q_2$, "posting list merge", has the candidates $d_3$ and $d_4$ and no answer. Over the 326 pairs of a term of the vocabulary and a document that does not contain it, 58 are false drops; the formula below predicts 63.8 on average.

## Correctness

The invariant is that each stored signature is the OR of the codes of the terms of its document. If $Q \subseteq T$, every bit of $q$ is a bit of some $\mathrm{sig}(t)$ with $t \in T$, so $s \text{ AND } q = q$: a matching document is always a candidate, and there are no false negatives. Line L6 is the exact test, so SEARCH returns exactly the documents of a direct scan, in the same order.

The rate of false drops depends on the hash. Model each term code as a uniform random set of $m$ of the $F$ places, independent across terms. For a one-term query whose term is not among the $D$ distinct terms of a document, the document is a false drop when each of the $m$ query places is set by some document term. By the [inclusion-exclusion principle](/inclusion-exclusion-principle/) over the query places that stay empty,

$$P_{\mathrm{fd}} = \sum_{j=0}^{m} (-1)^j \binom{m}{j} \left( \frac{\binom{F-j}{m}}{\binom{F}{m}} \right)^{D}.$$

The full proofs of both parts are in the proof file of this page.

## Complexity

| operation | time | notes |
|---|---|---|
| INSERT | $O(mD + F/w)$ | $m$ places for each of the $D$ distinct terms, in expectation over the rejections |
| CANDIDATES | $O(ms + NF/w)$ | the query code, then one pass over all signatures |
| SEARCH | $O(ms + NF/w + cV)$ | plus one check of each of the $c$ candidates |
| space | $O(NF/w)$ words | plus the documents for the check |

The scan reads every signature for every query, so the time grows with $N$ whatever the size of the answer. An [inverted index](/inverted-index/) reads only the [posting lists](/posting-list/) of the query terms.

## Variants

- **Choice of m.** For $F = 64$ and $D = 10$, the formula gives the false drop rates 0.1457, 0.0713, 0.0520, 0.0472, 0.0490, 0.0551, 0.0654 and 0.0800 for $m = 1$ to 8. The best is $m = 4$, near the value $(F/D)\ln 2 \approx 4.44$ of the approximation $P_{\mathrm{fd}} \approx (1 - e^{-mD/F})^m$, which gives 0.0466 at $m = 4$ against the exact 0.0472. This is the same optimum as for a Bloom filter, on the page about the [optimal number of hash functions](/bloom-filter-optimal-hash-count/). Doubling the width to $F = 128$ with $m = 4$ cuts the exact rate to 0.00489.
- **Bit-sliced storage.** Store the file by columns: one [bit vector](/bit-vector/) of length $N$ for each of the $F$ places. A query reads only the columns of its set bits and ANDs them, so the work per query is about $ms$ columns of $N$ bits, not all $NF$ bits. This is close to a [bitmap index](/bitmap-index/) over hashed places.
- **Signatures of blocks.** Cut long documents into blocks of a fixed number of distinct terms, and give each block its own signature, so that $D$ stays near the value the width was chosen for.
- **Several queries in one pass.** A sequential scan can test many query codes against each signature it reads.

## When to use it

Signature files suit conjunctive queries over many small records with a fixed upper bound on their terms, where appends are frequent, and where a scan of a compact file is acceptable. Zobel, Moffat and Ramamohanarao compared the two methods for text indexing and found inverted files distinctly superior: faster, smaller and more functional. A signature file keeps no term weights for ranking and no positions for phrase queries, and a NOT in a query cannot use the signatures at all, because a set bit does not prove that a term is present. For text search, use an inverted index; keep signatures for filters inside other structures.

## Pitfalls

- **Long documents.** A document with many distinct terms sets most of the bits and becomes a candidate for almost every query. With $F = 32$ and $m = 2$ the toy documents of 10 terms already have a false drop rate of 0.22 for one query term. Choose $F$ for the largest $D$, or split documents into blocks.
- **Dropping the check.** CANDIDATES is not the answer: "quantum" has a candidate on the toy collection. The check of line L6 needs access to the documents.
- **Codes with fewer than m bits.** Taking $m$ hash values modulo $F$ without removing repeats gives some terms fewer bits, and those terms pass more false drops. Choose distinct places.
- **Biased places.** Reducing a 16-bit value modulo an $F$ that does not divide $2^{16}$ makes small places more likely. Reject the values at or above the largest multiple of $F$ below $2^{16}$.
- **Testing the rate without a tolerance.** A measured false drop rate is random. Compare it with the formula within a bound such as [Hoeffding's inequality](/hoeffding-inequality/): with 150,000 trials, a gap of 0.00695 has probability at most about $10^{-6}$ under the model.

## Implementations

## History

Faloutsos and Christodoulakis (1984) presented signature files with superimposed coding as an access method for documents and analyzed their performance and their false drop probability, and Faloutsos (1985) surveyed them with full text scanning, inversion and clustering as the access methods for text. Zobel, Moffat and Ramamohanarao (1998) compared signature files with compressed inverted files and found the inverted files better on time, space and the range of queries, and inverted indexes became the standard for text search.

## References
