---
tag: W88DHC
kind: problem
slug: wildcard-query
name: Wildcard query
aliases:
- wildcard term query
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Find the documents that contain any term matching a pattern with wildcards, such as mon*h.
model: word-ram
complexity:
  vars: {n: the number of terms in the dictionary, L: the total length of the terms, q: the length of the pattern, r: the number of matching terms, P: the total length of the posting lists of the matching terms}
  time: {dictionary_scan: O(L + n q + P log r), permuterm_one_star: O(q log(L + n) + r log r + P log r)}
prereqs: [trie, regular-expression]
see_also: [k-gram-index, permuterm-index, inverted-index, wildcard-matching-in-trie, prefix-matching, regex-matching, stemming, boolean-retrieval-model]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 3, Section 3.2 (the reasons for wildcard queries with S*dney, color and colour, judicia* and Universit* Stuttgart; trailing queries such as mon* with a search tree, leading queries such as *mon with a reverse B-tree, se*mon by the intersection of the two; the query re*d AND fe*ri as a conjunction of disjunctions), Section 3.2.1 (general wildcard queries and the permuterm index) and Section 3.2.2 (k-gram indexes and the postfilter)
  - book: isbn:9781558605701
    title: Ian H. Witten, Alistair Moffat and Timothy C. Bell, Managing Gigabytes, Compressing and Indexing Documents and Images, second edition, Morgan Kaufmann, 1999
    locator: Chapter 4, Section 4.2 (partially specified query terms, with a scan of the lexicon, an index of n-grams and rotated lexicons)
---

A wildcard query is a query term with one or more stars, such as "mon*h", where each star stands for any string, also the empty one; the answer is the set of documents that contain at least one term of the dictionary that matches the pattern. It is solved in two stages: find the matching terms in the dictionary of an [inverted index](/inverted-index/), then take the union of their [posting lists](/posting-list/). The first stage is the hard part, because the dictionary is sorted for lookups by prefix, and a star in front or in the middle breaks that order.

## In plain words

Sometimes a user knows only part of a word. They are not sure whether it is "Sydney" or "Sidney", whether the text says "color" or "colour", or they want "judicial" and "judiciary" at once. A star in the query fills the gap: "judicia*" means any word that starts with "judicia".

The search engine first finds all the words of its dictionary that fit the pattern. Then it returns every document that contains at least one of them. If the star is at the end, the words that fit sit next to each other in a sorted list, and the search is easy. If the star is at the start or in the middle, the words that fit are spread over the whole list, and the engine needs an extra index to find them fast.

## Definition

Let $\Sigma$ be an alphabet without the symbol *, let $V \subseteq \Sigma^+$ be the dictionary of a collection, and for each term $t \in V$ let $\mathrm{post}(t)$ be its posting list. A *pattern* is a string $q = X_0 * X_1 * \cdots * X_j$ with pieces $X_i \in \Sigma^*$ and $j \ge 1$ stars. A string $t$ *matches* $q$ when $t = X_0 S_1 X_1 S_2 \cdots S_j X_j$ for some strings $S_1, \ldots, S_j \in \Sigma^*$.

- **Input:** the dictionary $V$ with its posting lists, and a pattern $q$.
- **Output:** the set of matching terms $T(q) = \{t \in V : t \text{ matches } q\}$, and the documents $\bigcup_{t \in T(q)} \mathrm{post}(t)$.

The set of strings that match $q$ is the language of the [regular expression](/regular-expression/) in which each star is replaced by $\Sigma^*$, so a term can be tested by [regex matching](/regex-matching/). For stars only, a direct test suffices: $X_0$ must be a prefix of $t$, $X_j$ a suffix, the two must not overlap, and the middle pieces must occur in order between them; taking each middle piece at its leftmost possible place is correct, because an earlier end leaves more room for the pieces after it.

## Variants

- **Trailing, leading and infix queries.** A *trailing* query X* has its star at the end, a *leading* query *X at the start, and *X* asks for the terms that contain X.
- **One star or several.** The query X*Y has one star; queries such as "*mo*er" have more, and most index methods answer them in two steps: a superset from the outer pieces, then a check.
- **A single character.** In shells and in many engines, ? stands for exactly one character and [...] for one character of a set. These are still regular languages.
- **Boolean combinations.** A query such as "re*d AND fe*ri" combines wildcard terms. Each wildcard term becomes the OR of its matching terms, so the query is a conjunction of disjunctions, as Manning, Raghavan and Schuetze put it.
- **Terms only.** Some uses, such as completion of a query and spelling help, need only $T(q)$ and not the documents.

## Examples

All examples use the 50 terms and 8 documents of the toy collection.

| pattern | matching terms | documents |
|---|---|---|
| sort* | sort, sorted | $d_1, d_2, d_4, d_8$ |
| li* | list, lists | $d_3, d_4, d_5$ |
| li*t | list | $d_3, d_4$ |
| doc* | document, documents | $d_4, d_7$ |
| s*ed | sorted, speed | $d_1, d_2, d_4, d_5, d_8$ |
| *ing | encoding, posting | $d_3, d_4, d_5, d_8$ |
| m*e* | merge, merges | $d_2, d_5$ |
| mon*h | none | none |

The Boolean query "post* AND li* AND merge*" gives $d_5$, the document that the plain query "posting list merge" misses because $d_5$ says "lists"; a user can get with stars the effect that [stemming](/stemming/) gives automatically. The query "*s" matches 10 terms and all 8 documents, which shows that a short pattern can be as expensive as the whole collection.

## Known algorithms

- **A scan of the dictionary.** Test every term against the pattern, in $O(L + nq)$ time with a linear-time matcher for the pieces, then merge the posting lists of the $r$ matches in $O(P \log r)$ time with a heap. It needs no extra space and is the baseline for every other method.
- **Search trees.** A [B-tree](/b-tree/) or a [trie](/trie/) over the sorted dictionary lists the terms with a given prefix, which answers X*; this is [prefix matching](/prefix-matching/). A second tree over the reversed terms answers *X, and Manning, Raghavan and Schuetze answer X*Y by intersecting the two results, as in "se*mon". [Wildcard matching in a trie](/wildcard-matching-in-trie/) walks the trie and branches at each star.
- **The [permuterm index](/permuterm-index/).** Store every rotation of each term with an end mark \$; X*Y becomes the prefix lookup of Y\$X, exact and with no filter, at a cost of $\ell + 1$ keys per term of length $\ell$. Queries with more stars use the outer pieces, then a check.
- **The [k-gram index](/k-gram-index/).** Index the k-grams of each padded term, intersect the lists of the grams of the pattern, and check each candidate; the index is smaller, but every query needs the check, and a pattern with no gram falls back to a scan.
- **A suffix array of the dictionary.** Concatenate the terms with separators and build a [suffix array](/suffix-array/); the terms that contain X are found by a binary search for X, which answers *X* and gives candidates for any pattern.

## Bounds

- **Output.** Any method must report the $r$ matching terms and read the posting lists it returns, so it needs $\Omega(q + r)$ time for the terms, and the union of the lists costs at least its size.
- **The term test.** One term $t$ can be tested against a pattern in $O(|t| + q)$ time: search the pieces left to right with a linear-time [string matcher](/string-matching/), each from the end of the previous match, so that the scanned parts of $t$ do not overlap.
- **One star.** With a permuterm index in a sorted array of $K = L + n$ keys, the terms of X*Y are found in $O(q \log K + r)$ time, which is optimal up to the search for the range. The cost is space: Manning, Raghavan and Schuetze report an almost ten-fold increase for a dictionary of English terms.
- **Several stars.** The methods above find a superset from part of the pattern and check it, so their time also depends on the number of candidates, which can be as large as $n$ for patterns such as "*s".

## Reductions

- **To regular expression matching.** Replace each star with a pattern for any string; each term is then a [regex matching](/regex-matching/) instance, and the dictionary scan is a filter with this test.
- **From one star to prefix search.** X*Y is a prefix query on the rotations of the terms, which is the permuterm index, or the intersection of a prefix query on the terms and a prefix query on the reversed terms.
- **From the terms to the documents.** Once $T(q)$ is known, the documents are the OR of the posting lists of $T(q)$, and a conjunction of wildcard terms is a [posting list intersection](/posting-list-intersection/) of those unions.

## Applications

Manning, Raghavan and Schuetze list four reasons for wildcard queries: the user is unsure of the spelling, as in "S*dney"; the user wants all spelling variants, such as "color" and "colour"; the user wants the variants that stemming would catch but does not know whether the engine stems, as in "judicia*"; and the user is unsure how a foreign word is written, as in "Universit* Stuttgart". They also note that the processing can be expensive, and that engines most often offer it behind an advanced query interface. File name patterns in shells, such as "*.txt", are the same problem over a list of names, and [query completion](/query-auto-completion/) is close to the trailing case.

## References
