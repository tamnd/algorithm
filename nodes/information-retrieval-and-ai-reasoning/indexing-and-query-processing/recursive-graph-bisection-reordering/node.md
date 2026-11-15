---
tag: 7XKMDW
kind: algorithm
slug: recursive-graph-bisection-reordering
name: Recursive graph bisection for index reordering
aliases:
- BP reordering
- Dhulipala bisection ordering
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: research
summary: Orders documents by recursive balanced bisection of the term-document graph, moving documents to minimize a log-gap cost.
model: word-ram
complexity:
  vars: {n: the number of documents, m: the number of document-term pairs, I: the iteration limit of each bisection}
  time: {total: O(I (m + n log n) log n)}
  space: {extra: O(n + m)}
properties: {deterministic: true, online: false, recursive: true, comparison: false}
prereqs: [document-identifier-reassignment, kernighan-lin]
see_also: [graph-partitioning-problem, fiduccia-mattheyses, multilevel-graph-partitioning, minhash, np-hard, webgraph-compression, postings-gap-encoding, partitioned-elias-fano]
sources:
  - paper: doi:10.1145/2939672.2939862
    title: Laxman Dhulipala, Igor Kabiljo, Brian Karrer, Giuseppe Ottaviano, Sergey Pupyrev and Alon Shalita, Compressing graphs and indexes with recursive graph bisection, Proceedings of the 22nd ACM SIGKDD Conference (KDD 2016), arXiv 1602.08820
    locator: the log-gap cost model of the bipartite term-document graph, the recursive bisection with the swap of documents by gain, its running time, the NP-hardness of the ordering problem, and the experiments on Gov2 and ClueWeb09
  - paper: "Joel Mackenzie, Antonio Mallia, Matthias Petri, J. Shane Culpepper and Torsten Suel, Compressing inverted indexes with recursive graph bisection, a reproducibility study, ECIR 2019"
    title: Compressing inverted indexes with recursive graph bisection, a reproducibility study
    locator: the independent implementation of the method and the measured index sizes against other document orders
  - paper: doi:10.1002/j.1538-7305.1970.tb01770.x
    title: B. W. Kernighan and S. Lin, An efficient heuristic procedure for partitioning graphs, Bell System Technical Journal 49(2), 291 to 307, 1970
    locator: the balanced bisection improved by swapping pairs of vertices chosen by gain, which the swap step here follows
---

Recursive graph bisection orders the documents of a collection so that the gaps of the [posting lists](/postings-gap-encoding/) get small. It views the collection as a bipartite graph between terms and documents. It splits the documents into two halves of equal size, then improves the split in a few rounds. In each round it computes for each document the drop in an estimate of the log-gap cost if that document moved to the other half, sorts each half by this gain, and swaps the leading pairs while the sum of their gains is positive. Then it orders each half the same way, down to single documents. Dhulipala and others published it in 2016, and it is often called BP. The problem it attacks, and other ways to attack it, are on the page [document identifier reassignment](/document-identifier-reassignment/). The swap step is the idea of [Kernighan-Lin](/kernighan-lin/), but with a different cost: Kernighan-Lin counts the edges cut, while this method counts the bits of the gaps. It is a heuristic with no approximation guarantee, and its gains are measured on real collections, not proved.

## In plain words

An index stores, for each word, the numbers of the documents that contain it, as the gaps from one number to the next. Small gaps take few bits. So documents that share words should get numbers close to each other. This method finds such numbers by cutting. It cuts the documents into two equal piles, and then moves documents between the piles so that each word is, as much as possible, in only one pile. Then it cuts each pile in two and does the same again, and so on, until each pile has one document. The order of the piles gives the new numbers. Nothing promises that the result is good. It works well on real web pages, and it can lose on small or random sets.

## The problem

The input is a collection of $n$ documents, each a set of terms. A document order is a permutation that gives each document a new id from 1 to $n$. For a term $t$ whose documents get the ids $p_1 < p_2 < \cdots < p_k$, the gaps are $p_1, p_2 - p_1, \ldots, p_k - p_{k-1}$. The log-gap cost of the order is the sum, over all terms and all their gaps $g$, of the bit length $\lfloor \lg g \rfloor + 1$. The goal is an order of small cost. Dhulipala and others show that finding an order of least cost is [NP-hard](/np-hard/) for their objective, the sum of $\lg g$ over the gaps, so the method aims for a good order, not the best one.

## The algorithm

For one bisection of a list $D$ into halves $A$ and $B$, let $a_t$ and $b_t$ be the numbers of documents in $A$ and in $B$ that contain term $t$. The method estimates the cost of $t$ as if its documents were spread evenly in each half, so that the average gap in $A$ is $|A|/(a_t+1)$:

$$c(a_t, b_t) = a_t \lg \frac{|A|}{a_t + 1} + b_t \lg \frac{|B|}{b_t + 1}.$$

The gain of a document is the drop of $\sum_t c(a_t, b_t)$ if that document alone moves to the other half. A large gain means the document fits the other half better.

```pseudo id=main
BP(D, depth)                                    ▷ D: a list of documents, each a set of terms
L1  if |D| ≤ leaf size or depth = depth limit then return D
L2  A ← the first ⌈|D|/2⌉ documents of D, B ← the rest
L3  repeat at most I times
L4      for each term t: a_t ← number of documents of A with t, b_t ← number of documents of B with t
L5      for each v in A: gain(v) ← sum over t in v of c(a_t, b_t) - c(a_t - 1, b_t + 1)
L6      for each v in B: gain(v) ← sum over t in v of c(a_t, b_t) - c(a_t + 1, b_t - 1)
L7      sort A and B by decreasing gain
L8      k ← the largest k such that gain(A[i]) + gain(B[i]) > 0 for every i < k
L9      if k = 0 then stop the loop
L10     exchange A[i] and B[i] for every i < k
L11 return BP(A, depth + 1) followed by BP(B, depth + 1)
```

Document $v$ at position $p$ of the result gets the new id $p + 1$. The original paper uses $I = 20$ iterations, and the implementation uses the same default. Line L7 breaks ties by the original id, so the method is deterministic.

## Example

Take 8 documents on two topics, in an order that mixes them:

| id | terms | id | terms |
|---|---|---|---|
| 1 | sort merge | 5 | sort merge array |
| 2 | sort array | 6 | hash table |
| 3 | merge array | 7 | key table |
| 4 | hash key | 8 | hash key table |

In the input order the log-gap cost is 32 bits. For example, the term *hash* is in documents 4, 6 and 8, with gaps 4, 2 and 2 of 3, 2 and 2 bits.

**First level.** $A = \{1, 2, 3, 4\}$ and $B = \{5, 6, 7, 8\}$. In $A$ the degrees are 2 for *sort*, *merge* and *array*, and 1 for *hash* and *key*. In $B$ they are 1 for *sort*, *merge* and *array*, 2 for *hash* and *key*, and 3 for *table*. The gains are 0 for documents 1, 2 and 3, and 3.66 for document 4. In $B$ they are 5.49 for document 5 and $-1.83$ for documents 6, 7 and 8. After the sort, the first pair is $(4, 5)$ with sum 9.15, and the second pair $(1, 6)$ has sum $-1.83$, so $k = 1$ and documents 4 and 5 change sides. In the next round every gain is negative, and the loop stops. Now $A = \{1, 2, 3, 5\}$ holds one topic and $B = \{4, 6, 7, 8\}$ the other, and the cost of the order $1, 2, 3, 5, 4, 6, 7, 8$ is 29 bits.

**Second level.** In $\{1, 2, 3, 5\}$ the halves are $\{1, 2\}$ and $\{3, 5\}$. The gains are 1.83 for documents 1, 2 and 5, and 0 for document 3, so both pairs have a positive sum and the two halves trade all their documents. That leaves the same split, and it happens again in each round. After 20 rounds $\{1, 2\}$ is first, and the gain sort puts 5 before 3. The other half gives $4, 6, 8, 7$ in the same way.

The final order is $1, 2, 5, 3, 4, 6, 8, 7$, with a cost of 27 bits. A search over all $8! = 40320$ orders finds no order below 27, so here the method finds an optimal order, while the median order costs 32.

On the toy collection of the information retrieval pages the method does worse. The input order of its 8 documents costs 169 bits, the method gives 178, one round per level gives 164, and the best of all orders is 148. These are the measured results of this implementation, and they show that the cost can go up.

## Correctness

The [proof](proofs/correctness.md) shows that each round keeps $A$ and $B$ a split of $D$ with the same sizes, that the recursion ends because both halves are strictly smaller, and so that the output is a permutation of the documents. There is no claim about the cost. The gain of line L5 or L6 is exact for one move alone, but line L10 makes many moves at once, each of which changes the degrees that the other gains used. The estimate $c$ also ignores the order inside each half. So a round can make the estimate worse, and the final order can be worse than the input. The tests check that the output is a permutation, that the cost function agrees with a separate walk over the positions, that the method lowers the cost on collections with planted topics, and that it raises the cost on some random collections.

## Complexity

One round at a list of $s$ documents with $m_s$ document-term pairs counts the degrees and the gains in $O(m_s)$ time and sorts the two halves in $O(s \log s)$ time. The lists at one level of the recursion are disjoint, so a level costs $O(I(m + n \log n))$ in total. The recursion has $\lceil \lg n \rceil$ levels, which gives $O(I(m + n \log n)\log n)$ time. The degree tables and the gains take $O(n + m)$ space. The paper runs the method on collections of millions of documents, and the two halves at each level can be done in parallel.

## Properties

- **Deterministic.** With ties broken by id, the same input gives the same order.
- **Balanced.** Every split has halves whose sizes differ by at most one, so the recursion depth is $\lceil \lg n \rceil$.
- **Nested.** Once a level puts a document in a half, the levels below keep it in that half.
- **No guarantee.** Nothing bounds the cost of the result in terms of the best cost.

## Variants and improvements

- **Depth limit.** Stop the recursion at a fixed depth and keep the input order inside each leaf, which saves time when the leaves are small runs of similar documents.
- **Other orders first.** Start from a URL order or a [MinHash](/minhash/) order instead of the input order, so that the first split is already good.
- **Graph compression.** The paper applies the same method to the adjacency lists of social graphs, as in [web graph compression](/webgraph-compression/), with the vertices on both sides of the bipartite graph.
- **Other partitioners.** General tools for [graph partitioning](/graph-partitioning-problem/), such as [multilevel](/multilevel-graph-partitioning/) schemes, minimize the edges cut and do not model the gaps. Swaps of single vertices as in [Fiduccia-Mattheyses](/fiduccia-mattheyses/) are another option for the local step.

## When to use it

Use it to renumber the documents of a static collection before the index is built, when the size of the index matters and an offline pass over the collection is affordable. It suits codes that gain from small gaps or dense clusters, such as [partitioned Elias-Fano](/partitioned-elias-fano/). For a collection that grows all the time, the ids must stay stable, and the method only applies to new segments. On a small or random collection it may not help, so measure the cost before and after.

## Pitfalls

- **It can make the order worse.** On the toy collection the cost goes from 169 to 178 bits. Keep the input order if the measured cost does not drop.
- **The halves can trade places.** If the gains are all positive, line L10 exchanges every pair, which leaves the split the same and wastes the round. The result then depends on the number of rounds being odd or even.
- **Keep the gains exact.** If the sum of a gain depends on the order of a hash set, rounding can flip ties and the method stops being deterministic. Sum the terms in a fixed order, or use an exactly rounded sum.
- **Do not count the gain of the whole round as the sum of the gains.** The degrees change with each swap.
- **The model is an estimate.** It assumes that the documents of a term spread evenly in each half, which is not true for small halves.

## Implementations

## History

The question of how document ids affect index size goes back to work on document reordering by Blandford and Blelloch in 2002 and by Shieh and others in 2003, who used clustering and traveling salesman tours. Silvestri showed in 2007 that the URL order of web pages is a strong and cheap baseline. Dhulipala, Kabiljo, Karrer, Ottaviano, Pupyrev and Shalita gave recursive graph bisection at KDD in 2016, with a swap step that follows the idea of Kernighan and Lin from 1970, and they reported smaller indexes than the earlier orders on the Gov2 and ClueWeb09 collections. Mackenzie and others reproduced the method in 2019.

## References
