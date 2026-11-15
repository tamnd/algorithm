---
tag: DWCXP8
kind: problem
slug: posting-list-intersection
name: Posting list intersection
aliases:
- conjunctive query processing
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: intro
summary: Given the sorted posting lists of the terms of an AND query, output the documents that appear in all of them.
model: comparison-model
complexity:
  vars: {k: the number of lists, m: the length of the shortest list, n: the length of the longest list}
  time: {lower: Ω(m log(n/m + 1)), merge: O(m + n), galloping: O(m log(n/m + 1))}
prereqs: [posting-list, sorted-array-intersection]
see_also: [merge-based-list-intersection, small-versus-small-intersection, baeza-yates-intersection, adaptive-set-intersection, skip-pointers, phrase-query, merging-lower-bound, leapfrog-triejoin]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 1, Section 1.3 (processing Boolean queries, the merge of two postings lists, and query optimization by increasing document frequency)
  - paper: "Erik D. Demaine, Alejandro López-Ortiz and J. Ian Munro, Adaptive set intersections, unions, and differences, SODA 2000"
    title: Erik D. Demaine, Alejandro López-Ortiz and J. Ian Munro, Adaptive set intersections, unions, and differences, Proceedings of the 11th ACM-SIAM Symposium on Discrete Algorithms (SODA 2000), 743-752
    locator: Section 3 (proofs of the result and their gap cost) and Section 5 (the intersection algorithm and its bound)
  - paper: doi:10.1145/1498698.1564507
    title: Jérémy Barbay, Alejandro López-Ortiz, Tyler Lu and Alejandro Salinger, An experimental investigation of set intersection algorithms for text searching, ACM Journal of Experimental Algorithmics 14, Article 3.7, 2009
    locator: the description of the algorithms SvS, Adaptive, Small Adaptive, Sequential and Baeza-Yates, and their comparison on web query logs
  - paper: doi:10.1145/1877766.1877767
    title: J. Shane Culpepper and Alistair Moffat, Efficient set intersection for inverted indexing, ACM Transactions on Information Systems 29(1), Article 1, 2010
    locator: the intersection methods for uncompressed and compressed posting lists, and the hybrid of bit vectors and lists
---

Posting list intersection is the problem of computing the set of documents that appear in every one of $k$ sorted [posting lists](/posting-list/), which is how a search engine answers a query of terms joined by AND. It is the core step of the [Boolean retrieval model](/boolean-retrieval-model/), of [phrase queries](/phrase-query/), and of most ranked engines, which score only the documents that hold all or most query terms. For two lists of lengths $m \le n$, a merge solves it with $m + n - 1$ comparisons, and every algorithm in the [comparison model](/comparison-model/) needs $\log_2 \binom{m+n}{m}$ comparisons in the worst case. That lower bound is about $m \log_2(n/m)$ when $m$ is much smaller than $n$, so a fast method must search instead of scan when the lists differ a lot in length.

## In plain words

A search engine keeps, for each word, the list of documents that hold it, sorted by document number. To answer "sorted AND array", it must find the numbers that are on both lists.

If the two lists have about the same length, the best way is to walk them side by side, like a merge of two sorted piles. If one list is short and the other is very long, the walk wastes time on the long list. It is then better to take each number of the short list and jump forward in the long list to find it. With many words, the engine starts with the shortest lists, so that the set of candidates becomes small fast.

## Definition

**Input.** An integer $k \ge 2$ and $k$ sorted lists $L_1, \ldots, L_k$ of document ids from a totally ordered set. Each list is strictly increasing, so no id is twice in one list. Write $n_i = |L_i|$, and when $k = 2$ write $m = \min(n_1, n_2)$ and $n = \max(n_1, n_2)$.

**Output.** The list of all ids $x$ with $x \in L_i$ for each $i$, in increasing order.

**Cost.** In the [comparison model](/comparison-model/), an algorithm may compare two ids, with the answer $<$, $=$ or $>$, and the cost is the number of comparisons. On the word RAM, the ids are integers below some $u$, and the cost is time.

## Variants

- **Two lists or many.** Most algorithms for $k$ lists intersect two at a time. The order matters: the result of two lists is at most as long as the shorter one, so engines start with the two shortest lists.
- **Adaptive analysis.** The cost is measured by a property of the instance, not only by the list lengths. Demaine, López-Ortiz and Munro measure the size of a proof that the result is correct; Barbay and Kenyon measure the alternation of the instance. See [adaptive set intersection](/adaptive-set-intersection/).
- **Compressed lists.** The lists are stored as compressed gaps, so access is sequential. Then random jumps need [skip pointers](/skip-pointers/), blocks with a table of first ids, or [Elias-Fano encoding](/elias-fano-encoding/).
- **Bit vectors.** For a term in a large part of the collection, a [bit vector](/bit-vector/) over all ids answers AND with word operations. Culpepper and Moffat mix bit vectors for long lists with lists of ids for short ones.
- **Other operators.** OR is a union, which is a merge with duplicates removed. AND NOT is a difference. A threshold query asks for the ids in at least $t$ of the $k$ lists.
- **Positions.** A phrase query or a proximity query intersects the lists and then checks the positions in each common document. See [positional intersection](/positional-intersection/).
- **Arrays in memory.** The same problem on general sorted arrays is [sorted array intersection](/sorted-array-intersection/), where the input need not come from an index.

## Examples

The lists below are from the toy collection of the information retrieval pages.

| query | lists | result |
|---|---|---|
| sorted AND array | sorted: 1, 2, 4, 8; array: 1, 2, 8 | 1, 2, 8 |
| sorted AND array AND search | the two above and search: 1, 7 | 1 |
| posting AND list | posting: 3, 4, 5; list: 3, 4 | 3, 4 |
| posting AND list AND merge | the two above and merge: 2, 5 | empty |
| a AND key | a: 1, 3, 4, 6, 7; key: 1, 6 | 1, 6 |

For the query posting AND list AND merge, the order by increasing length is list (2), merge (2), posting (3). The first step, list AND merge, gives the empty list, and the work stops there with no look at the list of "posting".

The gap between the scan and the lower bound grows with the ratio of the lengths. For $m = n = 1000$, the merge makes at most 1999 comparisons and the lower bound is $\log_2 \binom{2000}{1000} \approx 1994.2$. For $m = 10$ and $n = 10000$, the merge can make 10009 comparisons, and the lower bound is only about 111.1.

## Known algorithms

| algorithm | idea | comparisons for two lists |
|---|---|---|
| [Merge-based list intersection](/merge-based-list-intersection/) | one pointer in each list, advance the smaller | at most $m + n - 1$ |
| [Skip pointers](/skip-pointers/) | the merge, with forward pointers that skip blocks | no better worst case, faster in practice |
| [Small-versus-small](/small-versus-small-intersection/) | search each candidate of the short list in the next list by galloping | at most $2m \log_2(1 + n/m) + 2m$ |
| [Baeza-Yates intersection](/baeza-yates-intersection/) | search the median of the short list in the long list, then recurse on both sides | $O(m \log(1 + n/m))$ |
| [Adaptive intersection](/adaptive-set-intersection/) | gallop through all $k$ lists in turn, with one candidate | proportional to the size of a proof of the result |
| Hash probes | put the long list in a [hash table](/hash-table/), probe each id of the short list | $O(m)$ expected time after an $O(n)$ build, not in the comparison model |

The doubling search that the galloping methods use is [exponential search](/exponential-search/). The two-pointer merge and the Hwang and Lin merge for general arrays are on the page [sorted array intersection](/sorted-array-intersection/).

## Bounds

**Lower bound.** Let $k = 2$. Every algorithm in the comparison model that computes $L_1 \cap L_2$ makes at least $\lceil \log_2 \binom{m+n}{m} \rceil$ comparisons in the worst case, for each $m$ and $n$. The argument uses only inputs where the two lists have no common id. On such an input, each two ids from different lists that are next to each other in the merged order must have been compared directly: if they were not, an adversary can make them equal without a change to any other answer, and the result is then wrong. Those comparisons fix the merged order, so the $\binom{m+n}{m}$ ways to interleave the two lists reach different leaves of the decision tree. No comparison gives "$=$" on these inputs, so the tree is binary there, and its depth is at least $\log_2 \binom{m+n}{m}$. The full proof is in the correctness proof of [adaptive set intersection](/adaptive-set-intersection/). The same count gives the lower bound for merging, see [merging lower bound](/merging-lower-bound/).

**Size of the bound.** From $\left(\frac{m+n}{m}\right)^m \le \binom{m+n}{m} \le \left(\frac{e(m+n)}{m}\right)^m$,

$$m \log_2\left(1 + \frac{n}{m}\right) \le \log_2 \binom{m+n}{m} \le m \log_2\left(1 + \frac{n}{m}\right) + m \log_2 e.$$

So the lower bound is $\Theta(m \log(1 + n/m))$. When $m = n$ it is $2n - O(\log n)$. The same adversary does better on the input $a_1 < b_1 < a_2 < \cdots < a_n < b_n$, where all $2n - 1$ pairs of neighbours come from different lists and each must be compared, so the merge with its $2n - 1$ comparisons is exactly optimal for equal lengths. When $m = o(n)$, the merge is far from optimal, and the galloping methods match the bound up to a constant factor.

**Many lists.** For $k$ lists with $n_1 \le \cdots \le n_k$, small-versus-small makes $O(\sum_{i \ge 2} n_1 \log(1 + n_i/n_1))$ comparisons. Demaine, López-Ortiz and Munro show that their adaptive method makes at most $8kG$ comparisons, where $G$ is the gap cost of a proof of the result, a sum of the logarithms of the gaps that the proof jumps over. This can be much less than any bound in terms of the lengths alone, for example when the lists are far apart in value.

## Reductions

- **To merging.** Merge the two lists into one sorted list and report each id that appears twice in a row. This gives the upper bound $m + n - 1$ from any optimal merge.
- **From merging, on disjoint inputs.** The lower bound argument shows that an algorithm that decides that two lists have no common id must learn their full merged order. So intersection is at least as hard as merging, in the comparison model.
- **Phrase queries to intersection.** A [phrase query](/phrase-query/) first intersects the posting lists of its terms, then checks positions only in the common documents.
- **Joins.** A natural join of relations on one attribute is an intersection of sorted lists of keys, and [leapfrog triejoin](/leapfrog-triejoin/) uses galloping intersection of many lists as its inner loop.

## Applications

- **Boolean search.** Each AND of a Boolean query is one intersection. Engines choose the order of the terms by document frequency.
- **Ranked search.** [Document-at-a-time evaluation](/document-at-a-time-evaluation/) and methods such as WAND move through the lists with the NEXT-GEQ operation, the same step that galloping intersection uses.
- **Phrase and proximity search.** The common documents of the terms are the only ones whose positions need a check.
- **Databases.** The intersection of sorted lists of row ids answers a conjunction of conditions on several indexed columns.

## References
