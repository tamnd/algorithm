---
tag: DS6M6D
kind: algorithm
slug: positional-intersection
name: Positional intersection
aliases:
- positional merge for phrase queries
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Intersects two positional posting lists and, inside each common document, merges the position lists to find occurrences within distance k.
solves: [phrase-query]
model: word-ram
complexity:
  vars: {m: the number of documents in the first list, n: the number of documents in the second list, P: the number of positions of the two terms in their common documents, z: the number of output triples, k: the largest distance}
  time: {worst: O(m + n + P + z)}
  space: {extra: O(k)}
properties: {deterministic: true, comparison: false, recursive: false}
prereqs: [positional-index, merge-based-list-intersection]
see_also: [phrase-query, posting-list-intersection, skip-pointers, sliding-window, k-way-merge, adaptive-set-intersection, naive-string-matching, suffix-array]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 2, Section 2.4.2 (positional indexes, the algorithm PositionalIntersect for two terms within k words, and phrase queries as the case of adjacent positions), and Section 2.4.1 (biword indexes)
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 2, Section 2.1 (phrase search on an index of positions with the methods next and prev)
  - paper: doi:10.1145/1132956.1132959
    title: Justin Zobel and Alistair Moffat, Inverted files for text search engines, ACM Computing Surveys 38(2), Article 6, 2006
    locator: the evaluation of phrase and proximity queries on lists with word positions
---

Positional intersection answers a proximity query "$w_1$ within $k$ words of $w_2$" from a [positional index](/positional-index/). It merges the two document lists like the [merge-based list intersection](/merge-based-list-intersection/), and inside each common document it merges the two position lists with a small window of the positions of $w_2$ that are close to the current position of $w_1$. The output is every triple $(d, x, y)$ with $w_1$ at position $x$ and $w_2$ at position $y$ of document $d$ and $|x - y| \le k$. Manning, Raghavan and Schuetze give it as PositionalIntersect. A [phrase query](/phrase-query/) is the case where the second word must stand exactly one place after the first, and a phrase of $r$ words checks the offsets $0, 1, \ldots, r - 1$. The time is linear in the lengths of the lists, the positions in the common documents, and the output.

## In plain words

First find the documents that hold both words, by walking the two sorted lists of document numbers side by side.

In each such document, both words come with a sorted list of places. Walk through the places of the first word in order. For each one, move a second finger along the places of the second word, and keep in a small queue every place of the second word that is close enough. Places that are now too far behind fall out of the front of the queue. Every place left in the queue gives one answer.

The second finger never moves back. Since the first word only moves forward, a place of the second word that is too far behind for this place is too far behind for all later ones.

## The problem

The input is two positional lists, each a sequence of pairs (document id, positions) with strictly increasing ids and strictly increasing positions, and an integer $k \ge 0$. The output is the list of triples $(d, x, y)$ such that $d$ is in both lists, $x$ is a position of the first term in $d$, $y$ is a position of the second term in $d$, and $|x - y| \le k$, in increasing order. The distance is symmetric: the second term may stand before or after the first.

## The algorithm

```pseudo id=main
POSITIONAL-INTERSECT(p1, p2, k)
L1  i ← 0, j ← 0, R ← ()
L2  while i < |p1| and j < |p2| do
L3      if doc(p1[i]) = doc(p2[j]) then
L4          W ← an empty queue, X ← pos(p1[i]), Y ← pos(p2[j]), b ← 0
L5          for each x in X, in increasing order do
L6              while b < |Y| do
L7                  if |x - Y[b]| ≤ k then add Y[b] at the end of W
L8                  else if Y[b] > x then break             ▷ Y[b] > x + k
L9                  b ← b + 1
L10             while W is not empty and |front(W) - x| > k do remove front(W)
L11             for each y in W do append (doc(p1[i]), x, y) to R
L12         i ← i + 1, j ← j + 1
L13     else if doc(p1[i]) < doc(p2[j]) then i ← i + 1
L14     else j ← j + 1
L15 return R
```

Lines L2, L3, L13 and L14 are the merge of the document ids. Lines L6 to L9 move the index $b$ of $Y$ forward until $Y[b] > x + k$, add the close positions to $W$ and skip the positions less than $x - k$. Line L10 drops from the front of $W$ the positions that were close to an earlier $x$ but are now more than $k$ before $x$.

## Example

Take the toy collection and the query "list within 2 words of a". The lists are list: $\langle 3: 9 \rangle$, $\langle 4: 2, 6 \rangle$ and a: $\langle 1: 3, 6 \rangle$, $\langle 3: 7 \rangle$, $\langle 4: 0, 4 \rangle$, $\langle 6: 0, 4 \rangle$, $\langle 7: 5 \rangle$. The merge of the ids takes 3 passes of line L2: 3 against 1, then 3, then 4. Document 4 is "a posting list is a sorted list of document ids".

| document | $x$ | lines L6 to L9 | $W$ after line L10 | output |
|---|---|---|---|---|
| 3 | 9 | $|9 - 7| \le 2$: add 7; end of $Y$ | $(7)$ | $(3, 9, 7)$ |
| 4 | 2 | $|2 - 0| \le 2$: add 0; $|2 - 4| \le 2$: add 4; end of $Y$ | $(0, 4)$ | $(4, 2, 0)$, $(4, 2, 4)$ |
| 4 | 6 | end of $Y$ | $|0 - 6| > 2$: drop 0; $(4)$ | $(4, 6, 4)$ |

The inner loop makes 3 passes in total. With $k = 1$, the query "list within 1 word of sorted" returns $(4, 6, 5)$: "sorted list" stands at positions 5 and 6 of document 4. The distance has no direction, so this triple is not a match of the phrase "list sorted", which needs $y = x + 1$.

For phrases, keep only the triples with $y = x + 1$. The phrase "posting list" gives $(3, 8, 9)$ and $(4, 1, 2)$, so documents 3 and 4. Document 5 holds "posting" and "lists", which is another token, so it is not a match. The phrase "a sorted list" of three words matches only at position 4 of document 4.

## Correctness

The merge of the ids handles each common document once, in increasing order, as in the [merge](/merge-based-list-intersection/). Inside a document, the proof keeps three facts after line L10 for the current $x$: every position of $Y$ before $b$ is at most $x + k$; the position at $b$, if any, is greater than $x + k$; and $W$ holds, in increasing order, exactly the positions before $b$ that are at least $x - k$. These facts pass from one $x$ to the next because $x$ increases: a position that is less than $x - k$ is less than every later $x$ minus $k$. Since every position from $b$ on is greater than $x + k$, $W$ holds exactly the positions within distance $k$ of $x$. The full proof, with the phrase form, is in the proof file below.

## Complexity

- **Ids.** At most $m + n - 1$ passes of line L2, as in the merge.
- **Positions.** In a common document with position lists $X$ and $Y$, each pass of line L6 moves $b$ forward or stops for one $x$, so there are at most $|X| + |Y|$ passes. Each position of $Y$ enters and leaves $W$ at most once. In total, $O(P)$ for the positions of the two terms in the common documents.
- **Output.** Line L11 does one step for each triple, so $O(z)$. The output can be as large as $|X| \cdot \min(2k + 1, |Y|)$ in one document.
- **Total.** $O(m + n + P + z)$ time. The queue holds distinct positions in $[x - k, x + k]$, so at most $\min(2k + 1, |Y|)$ of them.
- **Phrases.** For a phrase of $r$ words, the code intersects the $r$ document lists, then the position lists after subtracting the offset $j$ from the positions of word $j$. Each round is a merge of two increasing lists, so a common document costs at most $\sum_j |X_j| + (r - 1)|X_0|$ steps.

## Properties

- **Exact.** It finds every pair within distance $k$, not only the closest one.
- **Forward only.** Both levels read each list once from left to right, so it works on compressed lists that are decoded in order, and [skip pointers](/skip-pointers/) can speed up the document level.
- **Output order.** The triples come out in increasing order of document, then $x$, then $y$.
- **Not a comparison algorithm.** The test $|x - y| \le k$ uses the difference of two positions, which needs integer positions.

## Variants and improvements

- **Phrases of $r$ words.** Word $j$ of the phrase must stand at $x + j$. Subtract $j$ from the positions of word $j$ and intersect the shifted lists, as the code does. Starting from the rarest word makes the candidate list small early.
- **Ordered proximity.** For "$w_2$ within $k$ words after $w_1$", keep only $0 < y - x \le k$; the window is then the range $(x, x + k]$.
- **Only the documents.** If only the documents are needed, stop each document at its first match.
- **Biword index.** An index of pairs of consecutive words answers two-word phrases with one lookup and longer phrases with candidate checks; Manning, Raghavan and Schuetze compare it with the positional index.
- **Index of collection positions.** Buettcher, Clarke and Cormack number the tokens of the whole collection and find phrases with the methods next and prev, which jump from one candidate to the next with no merge of document ids.
- **Ranked proximity.** Scores that reward close query words use the same merge to find the smallest window that holds all of them.

## When to use it

Use it to answer phrase and proximity queries from a positional index. For common words, the position lists are long, and a biword or phrase index for the frequent pairs can save work. For phrases of any length on raw text, a [suffix array](/suffix-array/) avoids the merge.

## Pitfalls

- **Resetting the second finger.** The index $b$ of $Y$ must not go back to 0 for each $x$. With the reset, the inner loop costs $|X| \cdot |Y|$ in a document. It must go back to 0 for each new document, at line L4.
- **The break condition.** Line L8 stops only when $Y[b] > x + k$. A stop at the first far position, also when it is less than $x - k$, misses the close positions after it.
- **Direction.** $|x - y| \le k$ has no direction, so $k = 1$ also matches "list sorted" for the query "sorted list". A phrase needs $y = x + 1$.
- **Stop words and tokenizing.** If the index drops stop words, the positions of the words around them shift or have gaps, and the offsets of a phrase with a stop word in the middle are wrong unless the positions keep the gaps.
- **One word twice.** For a query such as "a within 2 of a", each position is within distance 0 of itself. Exclude $x = y$ if a pair of two different occurrences is wanted.

## Implementations

## History

Manning, Raghavan and Schuetze give the algorithm for two terms within $k$ words, and the phrase case, in their textbook of 2008, together with the biword index as the other way to answer phrases. Buettcher, Clarke and Cormack give phrase search on an index of collection positions in 2010.

## References
