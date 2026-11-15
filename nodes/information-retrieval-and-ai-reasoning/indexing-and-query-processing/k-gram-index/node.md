---
tag: HHWFE5
kind: data-structure
slug: k-gram-index
name: k-gram index
aliases:
- character n-gram index
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Maps each character k-gram to the dictionary terms that contain it, for wildcard queries and spelling correction.
model: word-ram
complexity:
  vars: {n: the number of terms, L: the total length of the terms, k: the gram length, P: the length of the longest list of the index, C: the total length of the lists of the query grams, c: the number of candidate terms, l: the length of the longest term, q: the length of the query}
  time: {insert: O(k l + l P), delete: O(k l + l P), wildcard: O(k q + C + c l q)}
  space: {total: O(L + n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [wildcard-query, posting-list, merge-based-list-intersection]
see_also: [permuterm-index, inverted-index, trie, q-gram-filtering, q-gram-lemma, edit-distance, jaccard-similarity, noisy-channel-spelling-correction]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 3, Section 3.2.2 (k-gram indexes for wildcard queries, the end mark $, the 3-grams of castle, the list of the 3-gram etr, the query re*ve, the false match of retired for red* and the postfilter), Section 3.3.4 (k-gram indexes for spelling correction), and Section 3.5 (the study of Zobel and Dart 1995)
  - book: isbn:9781558605701
    title: Ian H. Witten, Alistair Moffat and Timothy C. Bell, Managing Gigabytes, Compressing and Indexing Documents and Images, second edition, Morgan Kaufmann, 1999
    locator: Chapter 4, Section 4.2 (partially specified query terms, answered with an index of the n-grams of the lexicon, compared with rotated lexicons and with a scan of the lexicon)
---

A k-gram index is a second index over the dictionary of an [inverted index](/inverted-index/): for every string of $k$ consecutive characters, it lists the terms that contain that string. Each term is padded with an end mark, so "castle" becomes "\$castle\$" and has the 3-grams "\$ca", "cas", "ast", "stl", "tle" and "le\$". A [wildcard query](/wildcard-query/) such as "re*ve" is answered by intersecting the lists of the grams it must contain, then by a postfilter that removes the terms that contain all the grams and still do not match.

## In plain words

Cut every word of the dictionary into short overlapping pieces of three letters, with a mark for the start and the end. For each piece, keep the list of words that contain it. To find the words that match "re*ve", take the pieces the query says a match must have: it starts with "re" and ends with "ve". Words in all those lists are the candidates.

The pieces do not keep their order or their distance, so a candidate can have all of them and still not match. The query "red*" needs the pieces "start re" and "red", and "retired" has both, but it does not start with "red". So every candidate is checked against the query at the end. The index finds a short list of words to check, and the check gives the exact answer.

## The abstract type

The structure holds a set $V$ of terms, each a nonempty string over an alphabet without the end mark \$ and the wildcard *, for a fixed $k \ge 1$. The operations are:

- INSERT$(I, t)$ and DELETE$(I, t)$: add or remove the term $t$.
- WILDCARD$(I, q)$: return the sorted list of the terms of $V$ that match $q$, where each * in $q$ stands for any string, also the empty one.
- CANDIDATES$(I, q)$: return the terms that contain every k-gram of the query, a superset of the answer. Used by itself for [spelling correction](/noisy-channel-spelling-correction/), where a word is close to a term that shares many of its grams.

## Representation

A sorted array of the terms, and a map from each k-gram to its *list*: the sorted array of the terms $t$ such that the gram occurs in the padded term \$$t$\$. A term is in a list once, even if the gram occurs twice in it, and no list is empty. This is an inverted index whose documents are the terms and whose words are the grams, so the lists can be stored, compressed and intersected like [posting lists](/posting-list/). A term of length $\ell$ has at most $\ell + 3 - k \le \ell + 2$ distinct grams, so the lists hold at most $L + 2n$ entries.

## Operations

The query cuts \$$q$\$ at each * and takes the k-grams of the pieces. Grams that would cross a * are not known, so they are not used.

```pseudo id=main
WILDCARD(I, q)
L1  G ← the distinct k-grams of the pieces of $q$, cut at each *
L2  if G is empty then C ← all the terms of I                  ▷ no gram: scan the dictionary
L3  else C ← the intersection of the lists of the grams of G, shortest list first
L4  R ← ()
L5  for each term t of C, in sorted order do
L6      if MATCHES(t, q) then append t to R                     ▷ the postfilter
L7  return R

INSERT(I, t)
L8  if t is in I.terms then return
L9  insert t into the sorted array I.terms
L10 for each distinct k-gram g of $t$ do insert t into the sorted list of g
```

MATCHES checks the first piece of $q$ as a prefix of $t$, the last piece as a suffix, and the middle pieces in order between them, each at its leftmost place. DELETE undoes line L10 for each gram and removes a list when it becomes empty. The intersection on line L3 is a [merge](/merge-based-list-intersection/) of sorted lists, so its cost is the total length of the lists.

## Example

Start empty with $k = 3$ and apply these operations.

| operation | terms | grams | entries | notes |
|---|---|---|---|---|
| INSERT list | 1 | 4 | 4 | \$li, lis, ist, st\$ |
| INSERT lists | 2 | 6 | 9 | \$li, lis and ist now hold two terms |
| INSERT sort | 3 | 10 | 13 | |
| INSERT sorted | 4 | 13 | 19 | |
| INSERT speed | 5 | 17 | 24 | ed\$ holds sorted and speed |
| WILDCARD li*t | 5 | 17 | 24 | G = {\$li}, C = (list, lists), R = (list) |
| WILDCARD s*ed | 5 | 17 | 24 | G = {ed\$}, C = R = (sorted, speed) |
| DELETE lists | 4 | 15 | 19 | the lists of ts\$ and sts are removed |
| WILDCARD li* | 4 | 15 | 19 | R = (list) |

The query "li*t" shows why line L6 is needed: "t\$" has only two characters, so the only gram is "\$li", and "lists" is a candidate that does not end with t.

On the 50 terms of the toy collection, the index with $k = 3$ has 192 grams and 234 entries. The query "s*ed" gives the 5 candidates compressed, expected, inverted, sorted and speed, and the postfilter keeps sorted and speed, so the [inverted index](/inverted-index/) returns the documents of either: $d_1$, $d_2$, $d_4$, $d_5$ and $d_8$. The query "se*ch" uses the grams "\$se" and "ch\$", and their intersection is "search" alone. The query "*or*" has no gram of length 3, so line L2 checks all 50 terms and keeps for, score, sort and sorted.

## Correctness

The invariant is that the list of each gram $g$ holds exactly the terms of $V$ in which $g$ occurs, sorted, and that no list is empty; lines L8 to L10 and DELETE keep it. If $t$ matches $q$, every piece of \$$q$\$ is a substring of \$$t$\$, so every gram of $G$ occurs in \$$t$\$ and $t$ is in each list. So $C$ contains every answer, and line L6 keeps exactly the answers because MATCHES is correct. The inclusion can be strict, as "retired" for "red*" shows, so the postfilter cannot be dropped. The full proof is in the proof file of this page.

## Complexity

| operation | time | notes |
|---|---|---|
| INSERT, DELETE | $O(k\ell + \ell P)$ | at most $\ell + 2$ grams; each insertion into a sorted array of length at most $P$ |
| CANDIDATES | $O(kq + C)$ | $C$ is the total length of the lists of the grams of the query |
| WILDCARD | $O(kq + C + c\,\ell q)$ | plus one MATCHES for each of the $c$ candidates |
| WILDCARD, no gram | $O(n \ell q)$ | a scan of the dictionary |
| space | $O(L + n)$ entries | plus one key for each distinct gram |

With lists in balanced trees or with a rebuild in batches, insertion costs $O(k\ell + \ell \log P)$ per term. The work of a query is in the lists, and the lists of common grams such as "\$s" or "ing" are long; the shortest-first order of line L3 bounds the size of each intermediate result by the shortest list.

## Variants

- **Choice of k.** Smaller $k$ gives fewer and longer lists, and more queries with at least one gram. On the toy vocabulary, $k = 2$ gives 138 grams and 284 entries, $k = 3$ gives 192 and 234, and $k = 4$ gives 167 and 184.
- **Grams for spelling correction.** For a misspelled word, take the terms that share many of its grams, rank them by the [Jaccard coefficient](/jaccard-similarity/) of the gram sets, then by [edit distance](/edit-distance/). The [q-gram lemma](/q-gram-lemma/) bounds how many grams two strings within edit distance $e$ must share, and [q-gram filtering](/q-gram-filtering/) uses it.
- **Positional grams.** Store the offset of the gram in the term, so that the query can require two grams at a fixed distance; this removes some candidates before the postfilter.
- **Grams over the text.** Index the k-grams of the documents themselves, not of the terms. This supports substring search in languages without spaces between words.

## When to use it

Use it to answer wildcard queries with a * anywhere, and to find candidates for spelling correction, with one index for both. It is smaller than a [permuterm index](/permuterm-index/), which stores every rotation of every term, but every query needs a postfilter, and a query with no gram falls back to a scan. For queries with only a trailing *, a [trie](/trie/) or a search tree over the sorted dictionary is simpler and needs no filter.

## Pitfalls

- **Dropping the postfilter.** The candidates of "red*" include "retired", and those of "li*t" include "lists". Always check each candidate against the query.
- **Grams across a star.** "s*ed" must not produce the gram "sed" or "s*e"; take grams only inside the pieces between the stars.
- **Short pieces.** A piece shorter than $k$, such as "t\$" for $k = 3$, gives no gram; a query such as "*or*" or "*s" then gives no gram at all and a full scan. Fall back on purpose and keep the scan cost in mind.
- **The end mark in terms.** A term that contains the mark breaks the invariant and the prefix checks. Reject such terms or choose a mark outside the alphabet.
- **Repeated grams.** A term such as "banana" has the gram "ana" twice. Insert the term into the list once, or the merge on line L3 gets duplicates.

## Implementations

## History

Manning, Raghavan and Schuetze present the k-gram index for wildcard queries in Section 3.2.2 with the end mark, the intersection of the lists and the postfilter, and they use the same index again for spelling correction. They cite the study of Zobel and Dart (1995), which shows that k-gram indexing is very effective for finding candidates for a misspelled word but should be combined with a finer method such as edit distance. Witten, Moffat and Bell describe the same index of n-grams of the lexicon for partially specified query terms and compare it with rotated lexicons.

## References
