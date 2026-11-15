---
tag: J3EW3B
kind: data-structure
slug: permuterm-index
name: Permuterm index
aliases:
- permuterm vocabulary
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Indexes every rotation of each term with an end marker, so a wildcard query becomes a prefix lookup in a search tree.
model: word-ram
complexity:
  vars: {n: the number of terms, L: the total length of the terms, K: the number of keys (L + n), l: the length of the longest term, q: the length of the query, r: the number of keys in the range of the query}
  time: {insert: O(l (l log K + K)), delete: O(l (l log K + K)), wildcard_one_star: O(q log K + r log r), wildcard_more_stars: O(q log K + r log r + r l q)}
  space: {total: O(K l)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [wildcard-query, binary-search]
see_also: [k-gram-index, trie, b-tree, prefix-matching, inverted-index, suffix-array, burrows-wheeler-transform, fm-index]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 3, Section 3.2.1 (permuterm indexes, the end mark $ and the rotations of hello$, the query m*n rotated to n$m*, and the query *mo*er, answered by the range of er$ and a filter that keeps fishmonger and removes filibuster), Section 3.2.2 (the almost ten-fold space increase for a dictionary of English terms), and Section 3.5 (Garfield 1976 and Ferragina and Venturini 2007)
  - book: isbn:9781558605701
    title: Ian H. Witten, Alistair Moffat and Timothy C. Bell, Managing Gigabytes, Compressing and Indexing Documents and Images, second edition, Morgan Kaufmann, 1999
    locator: Chapter 4, Section 4.2 (partially specified query terms, with rotated lexicons compared with an index of n-grams and with a scan of the lexicon)
---

A permuterm index is a search tree, or a sorted array, over all the rotations of the terms of a dictionary, where each term $t$ gets an end mark and becomes \$-terminated: "hello" gives the keys "hello\$", "ello\$h", "llo\$he", "lo\$hel", "o\$hell" and "\$hello", each pointing back to "hello". A [wildcard query](/wildcard-query/) X*Y matches exactly the terms that have a rotation starting with Y\$X, so it becomes one prefix lookup. The price is space: a term of length $\ell$ has $\ell + 1$ keys, and Manning, Raghavan and Schuetze report an almost ten-fold space increase for a dictionary of English terms.

## In plain words

A search tree over sorted words finds all words that start with "mo" quickly, but not all words that end with "on" or that start with "m" and end with "n". The permuterm index fixes this by turning every word around in all possible ways. Add a mark at the end of the word, then move letters one at a time from the front to the back, and store each result.

Now "m*n" asks for the words that end with "n" and start with "m". Rotate the query in the same way so that the star is at the end: "n, mark, m". Every word that matches has a stored form that starts with exactly these letters, and no other word has one. So one search for a prefix answers the query, with no check afterwards.

## The abstract type

The structure holds a set $V$ of terms, strings over an alphabet without the end mark \$ and the wildcard *. The operations are:

- INSERT$(I, t)$ and DELETE$(I, t)$: add or remove the term $t$.
- MEMBER$(I, t)$: tell if $t$ is in $V$.
- WILDCARD$(I, q)$: return the sorted list of the terms of $V$ that match $q$, where each * stands for any string, also the empty one.

## Representation

For each term $t$, the $|t| + 1$ rotations $\rho_0, \ldots, \rho_{|t|}$ of the string $t$\$ are its keys, with $\rho_i = (t\$)[i..] \, (t\$)[..i]$. All keys of all terms are kept in one sorted array, each with a pointer to its term; since the \$ marks where the term ends, a key names its term, and two terms never share a key. A balanced [search tree](/b-tree/) or a [trie](/trie/) of the keys does the same with cheaper updates. The array has $K = L + n$ keys, and stored as strings they take $\sum_t (|t| + 1)^2$ characters; stored as a pointer to the term and a rotation offset, they take $O(K)$ words.

## Operations

A prefix range is found by two [binary searches](/binary-search/): the first key at least $p$, and the first key at least $p$ followed by a character TOP that sorts after every character of a key.

```pseudo id=main
WILDCARD(I, q)
L1  if q has no * then return (q) if q$ is a key of I, else ()
L2  X ← the part of q before its first *; Y ← the part after its last *
L3  p ← Y $ X                                       ▷ the rotation of X*Y with the star last
L4  [lo, hi) ← the range of the keys that start with p
L5  if q has exactly one * then return the sorted terms of the keys in [lo, hi)
L6  return the sorted terms t of the keys in [lo, hi) with MATCHES(t, q)   ▷ the middle pieces

INSERT(I, t)
L9  if t$ is a key of I then return
L10 for each rotation r of t$ do insert (r, t) into the sorted array of keys
```

DELETE removes the $|t| + 1$ keys of $t$ in the same way. MATCHES is the check of the [k-gram index](/k-gram-index/) page: the first piece as a prefix, the last as a suffix, and the middle pieces in order between them.

The simple forms are cases of line L3: X* gives the prefix \$X, *X gives the prefix X\$, and "m*n" gives "n\$m", as in Manning, Raghavan and Schuetze. In their query "*mo*er", line L3 gives the prefix "er\$"; its range holds "fishmonger" and "filibuster", and line L6 keeps "fishmonger". The code treats *X* as X*Y with empty X and Y, so its range is every key that starts with \$, and line L6 checks every term; the variant below gives the direct lookup.

## Example

Start empty and apply these operations.

| operation | terms | keys | notes |
|---|---|---|---|
| INSERT list | 1 | 5 | \$list, ist\$l, list\$, st\$li, t\$lis |
| INSERT lists | 2 | 11 | adds the 6 rotations of lists\$ |
| INSERT sort | 3 | 16 | adds \$sort, ort\$s, rt\$so, sort\$, t\$sor |
| WILDCARD li*t | 3 | 16 | p = t\$li, range (t\$lis), answer (list) |
| WILDCARD *t | 3 | 16 | p = t\$, range (t\$lis, t\$sor), answer (list, sort) |
| WILDCARD l*s*s | 3 | 16 | p = s\$l, range (s\$list), MATCHES keeps lists |
| DELETE lists | 2 | 10 | its 6 keys are removed |

The query "li*t" shows the difference from the k-gram index: the range holds only the rotation of "list", and "lists" is never a candidate.

On the 50 terms of the toy collection the index has 284 keys with 1,834 characters in all, against 234 characters for the terms, a factor of 7.8. The query "s*ed" becomes the prefix "ed\$s", whose range is the two keys "ed\$sort" and "ed\$spe", so the answer is sorted and speed. The query "s*t*d" becomes the prefix "d\$s"; its range gives sorted and speed, and line L6 keeps sorted alone, because "speed" has no t between its s and its final d.

## Correctness

The invariant is that the array is sorted, has no repeats, and holds exactly the rotations of $t$\$ for the terms $t$ of $V$, each with its term; lines L9 and L10 and DELETE keep it. The key fact is that a term $t$ has a rotation starting with Y\$X exactly when $t = XSY$ for some string $S$, and then exactly one of its rotations starts with Y\$X, because \$ occurs once in each key. So for one star the range of line L4 holds one key for each answer and nothing else, and line L5 needs no filter. For more stars, X*Y is implied by the query, so the range holds every answer, and line L6 keeps exactly the answers. The full proof is in the proof file of this page.

## Complexity

| operation | time | notes |
|---|---|---|
| MEMBER | $O(\ell \log K)$ | one binary search with string comparisons |
| INSERT, DELETE | $O(\ell(\ell \log K + K))$ | $\ell + 1$ keys, each placed by binary search and an array shift |
| WILDCARD, one star | $O(q \log K + r \log r)$ | two binary searches, then sort the $r$ terms found |
| WILDCARD, more stars | $O(q \log K + r \log r + r \ell q)$ | plus one MATCHES for each of the $r$ terms |
| space | $O(K\ell)$ characters | $O(K)$ words if a key is a term and an offset |

With a balanced tree in place of the array, an insertion costs $O(\ell^2 \log K)$. The query cost does not depend on the number of terms that do not match, which is the main gain over a scan of the dictionary.

## Variants

- **Infix queries.** For *X*, take the keys that start with X: a term contains X exactly when some rotation of $t$\$ starts with X. A term can have several such keys, so remove repeats. On the toy vocabulary, "*or*" gives the four keys "or\$f", "ore\$sc", "ort\$s" and "orted\$s", which are the answer.
- **Keys as offsets.** Store each key as a pointer to the term and a rotation offset, and compare by reading the term from that offset. This cuts the space to $O(K)$ words and makes each comparison a little slower.
- **Compressed permuterm index.** Ferragina and Venturini (2007), as cited by Manning, Raghavan and Schuetze, give an approach to the space blowup of the permuterm index. Sorted rotations are also the base of the [Burrows-Wheeler transform](/burrows-wheeler-transform/) and the [FM-index](/fm-index/), which store them in compressed form.
- **Search tree and reverse search tree.** For queries with one star only, a [B-tree](/b-tree/) of the terms and one of the reversed terms answer X* and *Y; X*Y is the intersection of the two results. This takes two copies of the dictionary, not $\ell + 1$, but needs an intersection.

## When to use it

Use it when queries have one star, anywhere in the term, and must be fast and exact, and when the dictionary is small enough to store about ten times over. For long dictionaries with frequent updates or tight memory, the [k-gram index](/k-gram-index/) is smaller, at the cost of a postfilter for every query. For queries with only a trailing star, a plain search tree is enough.

## Pitfalls

- **Rotating the query the wrong way.** The prefix is the part after the last star, then \$, then the part before the first star: "m*n" becomes "n\$m", not "m\$n".
- **The end of the range.** The range must end at the first key at least the prefix followed by a character above every key character. With a TOP that can occur in a term, keys are lost at the end of the range.
- **The end mark in a term.** A term that contains \$ has two marks in its keys, and a key no longer names its term. Reject such terms.
- **More than one star.** The range of the outer pieces is a superset of the answer; skip line L6 and "s*t*d" returns "speed".
- **Space.** Each term is stored $\ell + 1$ times, and as strings the keys of a term take $(\ell + 1)^2$ characters. On the toy vocabulary the strings take 7.8 times the space of the terms.

## Implementations

## History

Manning, Raghavan and Schuetze credit Garfield (1976) with one of the first complete descriptions of the permuterm index. Witten, Moffat and Bell describe the same idea as a rotated lexicon and compare it with an index of n-grams of the lexicon.

## References
