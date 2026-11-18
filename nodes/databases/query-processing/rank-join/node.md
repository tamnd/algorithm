---
tag: TEN8RX
kind: algorithm
slug: rank-join
name: Rank join
aliases:
- HRJN
- hash rank join
area: databases/query-processing
level: advanced
summary: "Join two inputs sorted by score and output the results in order of a monotone combined score. Stop when a threshold shows that no pair not yet formed can enter the top k."
solves: [top-k-query]
model: word-ram
complexity:
  vars: {n: the number of tuples of L, m: the number of tuples of R, k: the number of results asked for, d: the number of tuples read, j: the number of join pairs formed from the tuples read}
  time: {worst: "O(n + m + n m log(n + m))", average: "O(d + (j + k) log(j + 2))"}
  space: {extra: "O(d + j)"}
properties: {deterministic: true, exact: true, external: false, online: true, in_place: false, recursive: false}
history:
  year: 2003
  people: [Ihab F. Ilyas, Walid G. Aref, Ahmed K. Elmagarmid]
  note: "Ilyas, Aref and Elmagarmid gave the hash rank join operator HRJN at VLDB 2003 and the journal version with the adaptive form HRJN* in 2004."
prereqs: [hash-join, top-k-query, priority-queue]
see_also: [threshold-algorithm, no-random-access-algorithm, fagin-algorithm, symmetric-hash-join, pipelining-and-materialization, iterator-model, query-optimization, binary-heap]
sources:
  - paper: doi:10.1007/s00778-004-0128-2
    title: "Ihab F. Ilyas, Walid G. Aref and Ahmed K. Elmagarmid, Supporting top-k join queries in relational databases, The VLDB Journal 13(3), 2004, pages 207 to 221"
    locator: Section 4 (the HRJN operator, its threshold, Theorem 4.2.1 on correctness and the adaptive pulling strategy HRJN*)
  - paper: "Ihab F. Ilyas, Walid G. Aref and Ahmed K. Elmagarmid, Supporting top-k join queries in relational databases, Proceedings of the 29th International Conference on Very Large Data Bases (VLDB), 2003, pages 754 to 765"
    title: Supporting top-k join queries in relational databases
    locator: the conference version of the HRJN operator
  - paper: doi:10.1145/1007568.1007593
    title: "Ihab F. Ilyas, Rahul Shah, Walid G. Aref, Jeffrey S. Vitter and Ahmed K. Elmagarmid, Rank-aware query optimization, SIGMOD 2004, pages 203 to 214"
    locator: the estimate of the input depth of a rank join and its use in plan enumeration
  - paper: doi:10.1145/1391729.1391730
    title: "Ihab F. Ilyas, George Beskales and Mohamed A. Soliman, A survey of top-k query processing techniques in relational database systems, ACM Computing Surveys 40(4), Article 11, 2008"
    locator: the sections on rank join and on top-k over sorted lists
  - paper: doi:10.1016/S0022-0000(03)00026-6
    title: "Ronald Fagin, Amnon Lotem and Moni Naor, Optimal aggregation algorithms for middleware, Journal of Computer and System Sciences 66(4), 2003, pages 614 to 656"
    locator: the threshold algorithm TA, which uses random access, and NRA, which uses sorted access only
  - paper: doi:10.1145/1376916.1376924
    title: "Karl Schnaitter and Neoklis Polyzotis, Evaluating rank joins with optimal cost, PODS 2008, pages 43 to 52"
    locator: the analysis of the HRJN threshold and a tighter bound for rank join
---

A rank join is a join operator that reads two inputs, each sorted by a score from high to low, and outputs the join results in order of a combined score $f$ such as the sum. It stops as soon as it has $k$ results and a threshold shows that no pair it has not yet formed can score higher. It answers a [top-k query](/top-k-query/) whose objects are the results of a join, not objects that occur once in every list. The [threshold algorithm](/threshold-algorithm/) solves the case where every list holds the same objects and it needs random access to look up an object in the other lists. The hash rank join (HRJN) uses only sorted access and a [hash join](/hash-join/) on what it has read, like the [no-random-access algorithm](/no-random-access-algorithm/).

## In plain words

Two shops each list their products from the most to the least popular. You want the 2 best pairs of products, one from each shop, that fit together, where the score of a pair is the sum of the two popularity scores.

You read the two lists a little at a time, and you keep every product you read. Each time you read a product, you check it against the products of the other shop that you already read, and you put each pair that fits in a ranked list.

You stop when your best pairs score at least as much as any pair you could still build. A pair that is not built yet needs a product that you have not read. Such a product scores no more than the last product read from its shop, so you can compute the best score that any such pair can have.

## The problem

The input is two lists $L$ and $R$ of $n$ and $m$ tuples. Each tuple has a join key and a score, and each list is sorted by score from high to low. The join condition is equality of keys, and a NULL key never matches. The score of a join result $(l, r)$ is $f(\mathit{score}(l), \mathit{score}(r))$, where $f$ is *monotone*: $f(x, y) \le f(x', y')$ whenever $x \le x'$ and $y \le y'$. Sum, weighted sum, minimum, maximum and the product of scores that are not negative are monotone. The output is $k$ join results with the largest scores, in order of score, with ties broken in any way, under bag semantics.

**Cost model.** The main measure is the *depth*: the number of tuples read from each input, $d_L$ and $d_R$, with $d = d_L + d_R$. In a pipelined plan each read pulls a tuple from a child operator, so the depth is the work that the operator causes below it. The second measure is the work in the [word RAM](/word-ram/), with hash tables and a binary heap.

## The algorithm

```pseudo id=main
HRJN(L, R, f, k)                     ▷ L and R sorted by score, highest first
L1  H_L, H_R ← empty hash tables on the join key; Q ← an empty max-priority queue on the score
L2  if L or R is empty or k = 0 then return the empty list
L3  while fewer than k results are output and L or R is not exhausted do
L4      choose an input I that is not exhausted       ▷ in turn, or by the HRJN* rule
L5      t ← the next tuple of I; bottom_I ← score(t); insert t in H_I
L6      for each tuple u of the other table with the key of t do insert the pair of t and u in Q
L7      T ← the largest of f(top_L, bottom_R) if R is not exhausted and f(bottom_L, top_R) if L is not exhausted; T ← −∞ if both are exhausted
L8      while Q is not empty, the top score of Q is at least T and fewer than k results are output do output the top of Q
L9  while Q is not empty and fewer than k results are output do output the top of Q
L10 return the output
```

Here $\mathit{top}_I$ is the score of the first tuple of $I$ and $\mathit{bottom}_I$ is the score of the last tuple read from $I$. Before the first read from an input, the implementation uses $f(\mathit{top}_L, \mathit{top}_R)$ as the threshold. An input is *exhausted* when all its tuples have been read, and then its term leaves the threshold, because no pair can use an unread tuple of it.

The threshold is the *corner bound*. A pair that is not formed has a tuple $l$ of $L$ that is not read, or a tuple $r$ of $R$ that is not read. In the first case $\mathit{score}(l) \le \mathit{bottom}_L$ and the other score is at most $\mathit{top}_R$, so the pair scores at most $f(\mathit{bottom}_L, \mathit{top}_R)$. The second case is symmetric.

**Which input to read (line L4).** HRJN reads the inputs in turn. HRJN* reads $R$ when $f(\mathit{top}_L, \mathit{bottom}_R) > f(\mathit{bottom}_L, \mathit{top}_R)$, and $L$ otherwise, because only a read from $R$ can lower the first term. The choice changes the depth, not the result.

## Example

Let $f$ be the sum, $k = 2$, $L = (a, 10), (b, 8), (c, 5), (a, 3), (b, 1)$ and $R = (b, 9), (a, 7), (c, 6), (b, 2)$, each written as (key, score). HRJN reads the inputs in turn.

| read | tuple | new pairs in Q | threshold T | output |
|---|---|---|---|---|
| 1 | $L$: $(a, 10)$ |  | $f(10, 9) = 19$ |  |
| 2 | $R$: $(b, 9)$ |  | $\max(10 + 9, 10 + 9) = 19$ |  |
| 3 | $L$: $(b, 8)$ | $(b, 8)(b, 9)$: 17 | $\max(10 + 9, 8 + 9) = 19$ |  |
| 4 | $R$: $(a, 7)$ | $(a, 10)(a, 7)$: 17 | $\max(10 + 7, 8 + 9) = 17$ | both pairs with 17 |

The operator stops after 4 of the 9 tuples. For $k = 3$ it continues. The third pair $(c, 5)(c, 6)$ with score 11 is formed at read 6, but the threshold falls only to 16, 16 and then 12 at read 8, when $R$ is exhausted and $T = f(3, 9)$. The bound $f(3, 9)$ assumes that the next tuple of $L$ has score 3 and joins with $(b, 9)$. Only read 9 exhausts $L$ and lets the operator output 11. So a loose corner bound can force the operator to read all the input.

**The pull rule.** Ilyas et al. compare the two rules on the scores $L = 100, 50, 25, 10, \dots$ and $R = 10, 9, 8, 5, \dots$ with the sum. After 3 reads from each input, $T = \max(100 + 8, 25 + 10) = 108$. HRJN* reads $L$ twice and $R$ four times in the same 6 reads, and gets $T = \max(100 + 5, 50 + 10) = 105$. A lower threshold lets the operator output its results sooner.

## Correctness

Each pair of the join is put in the queue exactly once, when the later of its two tuples is read, because the earlier tuple is then in its hash table. A pair that is not yet formed has an unread tuple, so by monotonicity it scores at most $T$. When line L8 outputs a pair, its score is at least $T$ and at least every score in the queue, so no pair that is not output yet has a higher score. The outputs therefore come in order of score, and the first $k$ of them are a top-k answer. The full proof is in [the proof page](proofs/correctness.md).

The proof needs $f$ to be monotone. If $f$ is not monotone, a tuple with a low score can still give a high combined score, and no bound from the scores read so far is safe.

## Complexity

- **Work.** Each read costs one insert and one probe of a hash table, in expected $O(1)$ time. Each formed pair costs one push into a [binary heap](/binary-heap/), $O(\log(j + 2))$, and each output costs one pop. The total is expected $O(d + (j + k) \log(j + 2))$, where $j$ is the number of pairs formed (a theorem in the word RAM). In the worst case $d = n + m$ and $j = n m$.
- **Space.** The operator keeps every tuple read and every pair formed but not output: $O(d + j)$. This is the main practical cost, because nothing read can be dropped while a later tuple of the other input might join with it.
- **Depth.** The depth depends on the data. When the tuples with high scores join, the depth is small: for two inputs of 200 tuples with scores $200, 199, \dots, 1$ and keys $0, 1, 2, 3, 0, 1, \dots$, so that tuples of equal rank join, $k = 3$ reads 5 tuples from each input. When they do not join, the operator can read both inputs to the end even for $k = 1$. Neither rule for line L4 is optimal on every instance.

## Properties

- **Pipelined.** The operator outputs each result as soon as it is safe, so a parent operator, such as another rank join, can pull results one at a time.
- **Sorted access only.** It never looks up a key in an input that it has not read, unlike the threshold algorithm.
- **Bag semantics.** Each pair of tuples with equal keys is a separate result, so duplicates in the inputs give duplicate results.
- **Ties.** Results with equal scores come in the order in which they were formed. The order of the scores does not depend on the pull rule, but which of several tied pairs is output first can.

## Variants and improvements

- **Multiway rank join.** A plan for several inputs is a tree of binary rank joins. The output of a child rank join is sorted by its combined score, so it can be the input of the parent, with the score of a partial result as its score.
- **Rank join in the optimizer.** Ilyas, Shah, Aref, Vitter and Elmagarmid (2004) estimate the depth of each input, so that the [query optimizer](/query-optimization/) can compare a plan with rank joins against a plan that joins everything and then sorts.
- **Tighter bounds.** Schnaitter and Polyzotis (2008) showed that the corner bound can be far from the best possible bound, and gave a tighter bound computed from the tuples already read, with an analysis of the cost of reading.
- **Nested-loops rank join.** When one input is small or has an index on the key, a rank join can scan the other input in order and look up matches, at the cost of random access.
- **The top-k aggregation case.** When both lists hold the same objects and the key is the object, a rank join solves the top-k aggregation problem for two lists with sorted access only, as the [no-random-access algorithm](/no-random-access-algorithm/) does.

## When to use it

Use a rank join when a query asks for the $k$ best results of a join under a monotone score, the inputs can be read in order of score (from an index or from a ranked child operator), and $k$ is small compared with the size of the join. The early stop pays off when the high scores of the two inputs tend to join. When the join result is small, a plain [hash join](/hash-join/) followed by a sort or a heap of size $k$ is simpler and reads the same input.

## Pitfalls

- **A score that is not monotone.** For example, $f(x, y) = x - y$ breaks the threshold, and the operator returns wrong results without any error.
- **Threshold terms of exhausted inputs.** If a term of an exhausted input stays in $T$, the operator cannot output its last results until both inputs end. If the term of an input that is not exhausted is dropped, results come out too early.
- **Unsorted input.** An input that is not sorted by score breaks the bound $\mathit{score}(l) \le \mathit{bottom}_L$. The implementation checks the order.
- **Memory.** In the worst case the operator keeps both inputs in memory, like a [symmetric hash join](/symmetric-hash-join/).
- **NULL keys.** A tuple with a NULL key must not be put in a hash table under a NULL entry, because NULL never equals NULL in a join.

## Implementations

## History

Ilyas, Aref and Elmagarmid presented the hash rank join operator HRJN at VLDB 2003, as a physical operator that a relational engine can place in a query plan, and the journal version of 2004 described the adaptive pull rule HRJN*. Ilyas, Shah, Aref, Vitter and Elmagarmid (SIGMOD 2004) added rank joins to a cost-based optimizer with an estimate of the depth. Their work built on the top-k algorithms of Fagin, Lotem and Naor for lists of the same objects, which use sorted and random access. Schnaitter and Polyzotis (2008) studied the cost of rank join algorithms and showed that the corner bound is not tight in general. Ilyas, Beskales and Soliman (2008) surveyed rank join among the top-k techniques in relational systems.

## References
