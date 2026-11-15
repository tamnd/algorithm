---
tag: F109TQ
kind: data-structure
slug: positional-index
name: Positional index
aliases:
- positional inverted index
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: An inverted index whose postings store, for each document, the positions where the term occurs, so phrase and proximity queries can be answered.
model: word-ram
complexity:
  vars: {T: the number of tokens in the collection, L: the number of tokens in one document, f: the number of documents that hold the term, g: the number of times the term occurs in the document}
  time: {add_document: O(L) expected, positions: O(log f + g), build: O(T) expected}
  space: {total: Θ(T)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [posting-list, phrase-query]
see_also: [positional-intersection, inverted-index, skip-pointers, postings-gap-encoding, k-gram-index, suffix-array, document-listing, posting-list-intersection]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 2, Section 2.4.1 (biword indexes) and Section 2.4.2 (positional indexes, their postings of the form document and positions, and the positional intersection of two lists)
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 2, Section 2.1 (an inverted index of term positions with the methods first, last, next and prev, and phrase search with it)
  - paper: doi:10.1145/1132956.1132959
    title: Justin Zobel and Alistair Moffat, Inverted files for text search engines, ACM Computing Surveys 38(2), Article 6, 2006
    locator: the inverted list with in-document frequencies and word positions, and the compression of position gaps
  - book: isbn:9781558605701
    title: Ian H. Witten, Alistair Moffat and Timothy C. Bell, Managing Gigabytes, second edition, Morgan Kaufmann, 1999
    locator: Chapter 3 (inverted file indexing, the granularity of an index and word-level indexes)
---

A positional index is an [inverted index](/inverted-index/) whose [posting lists](/posting-list/) also record where each term occurs: for each document that holds the term, it stores the sorted list of the token positions of the term in that document. With these positions, a search engine can answer a [phrase query](/phrase-query/) such as "posting list", which needs the two words next to each other and in this order, and proximity queries such as "the two words within 3 words of each other". A plain index of document ids can only say that both words occur somewhere in the document. The cost is space: a positional index stores one entry for each token of the collection, so it grows with the length of the text, not with the number of distinct pairs of a term and a document.

## In plain words

A plain index keeps, for each word, the list of documents that hold it. A positional index keeps a bit more: for each of those documents, the places in the text where the word stands, counted as the first word, the second word, and so on.

To check if a document holds the phrase "posting list", look up the places of "posting" and of "list" in that document. The phrase is there if some place of "list" is just one after a place of "posting".

So the index answers two kinds of questions: which documents hold a word, and where in each document the word is. The price is one stored number for each word of the text.

## The abstract type

A positional index over a collection of documents, each a sequence of tokens, supports:

- ADD-DOCUMENT$(d, t_0, \ldots, t_{L-1})$: add a document with an id greater than all ids before.
- POSTINGS$(w)$: the increasing ids of the documents that hold term $w$.
- POSITIONS$(w, d)$: the increasing positions $i$ with $t_i = w$ in document $d$, or the empty list.
- ENTRIES$(w)$: the positional posting list of $w$, the pairs $(d, \mathrm{POSITIONS}(w, d))$ in increasing order of $d$, which is the input of [positional intersection](/positional-intersection/).
- The statistics $\mathrm{df}(w) = |\mathrm{POSTINGS}(w)|$, $\mathrm{tf}(w, d) = |\mathrm{POSITIONS}(w, d)|$ and $\mathrm{cf}(w)$, the sum of $\mathrm{tf}(w, d)$ over all $d$.

Positions count tokens from 0. They are word positions, not byte offsets.

## Representation

A dictionary, here a [hash table](/hash-table/), maps each term to its positional list. The list is two parallel arrays: the increasing document ids, and for each id, the increasing array of positions. In the notation of Manning, Raghavan and Schuetze, the list of a term is written as entries $\langle d: p_1, p_2, \ldots \rangle$. On disk, both levels are usually coded as gaps with a [gap code](/postings-gap-encoding/): the ids as gaps between ids, and the positions of each document as gaps that restart at the first position of the document.

## Operations

```pseudo id=main
ADD-DOCUMENT(I, d, t_0, ..., t_{L-1})     ▷ d greater than every id in I
L1  if I has a document and not (the last id < d) then error "out of order"
L2  for i ← 0 to L - 1 do
L3      P ← the positional list of t_i, made empty if t_i is new   ▷ hash table
L4      if P is empty or the last id of P ≠ d then append (d, ()) to P
L5      append i to the positions of the last entry of P

POSITIONS(I, w, d)
L6  if w has no list then return ()
L7  p ← the least index with p = |P.ids| or P.ids[p] ≥ d   ▷ binary search
L8  if p < |P.ids| and P.ids[p] = d then return P.pos[p]
L9  return ()
```

The tokens of one document come in order of position, so line L5 always appends a position greater than the ones already in the list. The documents come in order of id, so line L4 appends an id greater than the ones already there. POSTINGS and ENTRIES return the stored arrays.

## Example

On the toy collection, 8 documents with 79 tokens and 50 distinct terms, the positional lists of three terms are:

| term | df | positional list |
|---|---|---|
| sorted | 4 | $\langle 1: 7 \rangle$, $\langle 2: 4, 8 \rangle$, $\langle 4: 5 \rangle$, $\langle 8: 1 \rangle$ |
| posting | 3 | $\langle 3: 8 \rangle$, $\langle 4: 1 \rangle$, $\langle 5: 8 \rangle$ |
| list | 2 | $\langle 3: 9 \rangle$, $\langle 4: 2, 6 \rangle$ |

Document 2 is "merge sort merges two sorted runs into one sorted array", so "sorted" stands at positions 4 and 8, and $\mathrm{tf}(\text{sorted}, 2) = 2$.

The phrase "posting list" is in a document when a position of "list" is one more than a position of "posting". The common documents of the two lists are 3 and 4. In document 3, $8 + 1 = 9$ is a position of "list", and in document 4, $1 + 1 = 2$ is. Document 5 holds "posting" at position 8 but not "list": its word is "lists", a different token. So the phrase is in documents 3 and 4. The query "list sorted" shows what the positions add: both words are in document 4, at positions 2, 6 and 5, but no position of "sorted" is one more than a position of "list", so the phrase is in no document, while the AND query returns document 4.

The whole index holds 74 document ids and 79 positions, one for each token. The index without positions holds only the 74 ids.

## Correctness

The proof keeps one invariant after each document: for each term, the stored ids are exactly the documents so far that hold it, in increasing order, and the positions stored with each id are exactly its positions in that document, in increasing order. ADD-DOCUMENT keeps it, because the new id is greater than all ids before and the tokens come in order of position, so each append goes at the right end. POSITIONS is a binary search on the ids. The full proof is in the proof file below.

## Complexity

- **Space.** One position for each token and one id for each pair of a term and a document that holds it, so $\Theta(T)$ words for $T$ tokens. A plain index stores only the ids, which can be much fewer than $T$ when words repeat in a document.
- **Build.** ADD-DOCUMENT makes one hash lookup and $O(1)$ amortized appends for each token, so $O(L)$ expected time for a document of $L$ tokens and $O(T)$ for the collection.
- **Lookup.** POSITIONS makes $O(\log f)$ comparisons on the ids of a term with $f$ documents, then returns its $g$ positions.
- **Queries.** A phrase or proximity query of two terms costs the intersection of the document lists plus, in each common document, a merge of the two position lists; see [positional intersection](/positional-intersection/).

## Variants

- **Biword index.** Index each pair of consecutive words as one term. A two-word phrase is then one lookup, but longer phrases need several lookups and can give false matches, and the dictionary grows a lot.
- **A combined index.** Keep a biword or phrase index for frequent phrases, and the positional index for the rest.
- **Index of positions in the collection.** Number all tokens of the collection in one sequence, and store for each term the increasing list of its global positions. Buettcher, Clarke and Cormack build their index this way, with methods that find the next and the previous occurrence of a term from a given position.
- **Skips in position lists.** [Skip pointers](/skip-pointers/) on the document level let a query jump to the next common document before it reads any position.
- **Full-text indexes.** A [suffix array](/suffix-array/) answers phrase queries of any length with no tokenizing, at a higher cost in space, and [document listing](/document-listing/) reports the documents that hold a pattern.

## When to use it

Use it when the engine must support phrase queries or rank documents by how close the query words are. If only the presence of words matters, a plain index of ids and frequencies is smaller and faster to scan.

## Pitfalls

- **Positions that do not match the query tokens.** The positions must be counted after the same tokenizing as the query. If the index drops stop words but keeps their places, or keeps them and the query drops them, phrase queries miss or find the wrong text.
- **Positions in the wrong order.** Line L5 assumes the tokens come in order. An index built from several passes over a document must sort the positions of each entry.
- **Gaps across documents.** On disk, the gaps of positions restart in each document. A gap from the last position of one document to the first of the next has no meaning.
- **Space.** A positional index needs one entry per token. Plan the size by the length of the text, not by the number of distinct pairs of a term and a document.

## Implementations

## History

Manning, Raghavan and Schuetze present biword indexes and positional indexes as the two ways to support phrase queries, and give the positional intersection of two lists. Witten, Moffat and Bell treat word-level indexes with gap codes in Managing Gigabytes, and Zobel and Moffat describe the layout of document ids, frequencies and positions in their survey of inverted files in 2006.

## References
