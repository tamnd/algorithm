---
tag: S3HYPD
kind: problem
slug: phrase-query
name: Phrase query
aliases:
- exact phrase search
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: intro
summary: Find the documents in which the query terms occur next to each other in the given order.
model: word-ram
complexity:
  vars: {r: the number of words in the phrase, M: the total length of the document lists of the phrase words, P: the number of positions of the phrase words in the documents that hold all of them, T: the number of tokens in the collection}
  time: {positional_index: O(M + r P), scan: O(T)}
prereqs: [posting-list-intersection, string-matching]
see_also: [positional-index, positional-intersection, inverted-index, naive-string-matching, knuth-morris-pratt, suffix-array, wildcard-query, boolean-retrieval-model]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 2, Section 2.4 (positional postings and phrase queries), Section 2.4.1 (biword indexes) and Section 2.4.2 (positional indexes)
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 2, Section 2.1 (phrase search on an inverted index of term positions)
  - paper: doi:10.1145/1132956.1132959
    title: Justin Zobel and Alistair Moffat, Inverted files for text search engines, ACM Computing Surveys 38(2), Article 6, 2006
    locator: the evaluation of phrase queries on inverted lists with word positions
---

A phrase query asks for the documents that contain a given sequence of words, next to each other and in the given order, such as "posting list" or "sorted array". Web search engines offer it as a query in quotes. It is stronger than the AND query of [posting list intersection](/posting-list-intersection/): a document can hold all the words of the phrase in other places and in another order, and still not match. Over the token sequence of one document, it is [string matching](/string-matching/) with words as the symbols. With an index, the usual solutions are a [positional index](/positional-index/) with [positional intersection](/positional-intersection/), and indexes of word pairs or phrases.

## In plain words

You give a few words in a fixed order. The answer is every document in which these words stand side by side, in exactly that order.

A document that holds all the words is not enough. "List sorted" and "sorted list" use the same two words, but only one of them is a phrase of a given document.

To answer fast, an index can keep, for each word, the places where it stands in each document. Then a document matches if the first word stands at some place, the second word at the next place, the third word one place after that, and so on. A slower way reads the text of every document and looks for the words one after the other.

## Definition

A document $d$ is a sequence of tokens $t^d_0, \ldots, t^d_{L_d - 1}$, made by the same tokenizer as the query. A phrase is a sequence of terms $q_0, \ldots, q_{r-1}$ with $r \ge 1$. An *occurrence* of the phrase is a pair $(d, x)$ with
$$t^d_{x + j} = q_j \quad \text{for } j = 0, \ldots, r - 1.$$
The phrase query returns the set of documents $d$ that have at least one occurrence, in increasing order of id. The occurrence form returns all pairs $(d, x)$. For $r = 1$, the answer is the posting list of $q_0$.

## Variants

- **Occurrences or documents.** Return all positions of the phrase, to highlight them in a result page, or only the documents, for a Boolean answer.
- **Proximity.** The words must stand within $k$ positions of each other, with or without a fixed order. A phrase of two words is the ordered case with distance exactly 1.
- **Phrases with gaps.** Some systems allow a fixed number of any words between two phrase words, or a [wildcard](/wildcard-query/) inside a word.
- **Phrases in a larger query.** A phrase can be one operand of a Boolean query, such as "posting list" AND merge, or one feature of a ranked query.

## Examples

On the toy collection, with tokens split on spaces and no stemming:

| phrase | AND of the words | phrase result | reason |
|---|---|---|---|
| posting list | 3, 4 | 3, 4 | both documents have "posting" right before "list"; document 5 has "posting lists", another token |
| sorted array | 1, 2, 8 | 1, 2, 8 | each document has "sorted array" |
| sorted list | 4 | 4 | positions 5 and 6 of document 4 |
| list sorted | 4 | none | "list" stands at 2 and 6 and "sorted" at 5 |
| merge sort | 2 | 2 | positions 0 and 1 of document 2 |

The row "list sorted" shows the gap between the two queries: the AND query returns document 4, and the phrase query returns nothing. The row "posting list" shows that the result depends on the tokenizer: with stemming, "lists" would become "list", and document 5 would match.

## Known algorithms

- **Scan the text.** Read every document and run a [naive matcher](/naive-string-matching/) or [Knuth-Morris-Pratt](/knuth-morris-pratt/) with words as symbols. No index is needed, but each query reads the whole collection.
- **Positional index.** Intersect the document lists of the words, then, in each common document, intersect the position lists after shifting word $j$ back by $j$. This is the method of [positional intersection](/positional-intersection/). Starting from the rarest word keeps the candidates few.
- **Biword index.** Index each pair of consecutive words as one term. A two-word phrase is then one lookup. A longer phrase becomes an AND of its pairs, which can return documents where the pairs do not line up, so the candidates must be checked against the text or a positional index.
- **Phrase indexes and combined schemes.** Index frequent phrases directly, and fall back on the positional index for the rest.
- **Index of collection positions.** Buettcher, Clarke and Cormack number all tokens of the collection in one sequence and find phrases with the methods next and prev of their inverted index, which jump from one candidate occurrence to the next.
- **Suffix arrays.** A [suffix array](/suffix-array/) of the token sequence finds all occurrences of a phrase by binary search, and [document listing](/document-listing/) turns the occurrences into distinct documents.

## Bounds

- **Scan.** One pass of a linear-time matcher costs $O(T)$ for $T$ tokens, for every query, rare or not.
- **Positional index.** With $M$ ids in the document lists of the phrase words and $P$ positions of these words in their common documents, the merge of the ids and the shifted merges of the positions cost $O(M + rP)$, by the proof on the positional intersection page.
- **Biword index.** For $r = 2$, the cost is one dictionary lookup plus the length of one list, at the price of one dictionary entry for each distinct pair of consecutive words.
- **Suffix array.** A binary search compares the phrase with $O(\log T)$ suffixes, each comparison at most $r$ symbols, so $O(r \log T)$ plus the number of occurrences.
- **The AND query as a filter.** Every document of the phrase result is in the result of the AND query of its words, so the cost of the [posting list intersection](/posting-list-intersection/) of the words is a part of the positional method.

## Reductions

- **To an AND query.** The phrase result is a subset of the AND result of its words, so a phrase query is an AND query followed by a check in each candidate document.
- **To string matching.** Join the token sequences of all documents with a separator token that is never in a query, and search the phrase as a pattern with words as symbols. Each match gives a document and a position.
- **From proximity.** A proximity query with an ordered distance of exactly 1 between consecutive words is a phrase query, so an algorithm for ordered proximity also answers phrases.

## Applications

- Queries in quotes in web and site search, for names, titles and fixed expressions.
- Search in legal, patent and code collections, where the exact wording matters.
- Ranking: documents where the query words stand together or close are often scored higher, and the same positions give these features.
- Highlighting the matched words in a result page, from the occurrence form.

## References
