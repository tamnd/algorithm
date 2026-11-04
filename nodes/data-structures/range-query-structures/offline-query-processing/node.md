---
tag: R1WX72
kind: technique
slug: offline-query-processing
name: Offline query processing
aliases:
- offline algorithm
- offline queries
area: data-structures/range-query-structures
level: intro
summary: Read all queries first and reorder them, for example by endpoint, to exploit structure.
prereqs: [offline-algorithm, prefix-sums]
see_also: [mo-algorithm, sweep-line-technique, offline-deletion, divide-and-conquer-on-queries, parallel-binary-search, arpa-offline-rmq, tarjan-offline-lca, range-distinct-count-query]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 18, Tree queries, Section 18.4 Offline algorithms (merging data structures, and lowest common ancestors offline)
  - url: https://cp-algorithms.com/data_structures/disjoint_set_union.html
    title: cp-algorithms, Disjoint Set Union
    locator: the section on range minimum queries offline (Arpa's trick), and the section on the offline lowest common ancestor
  - paper: doi:10.1145/322154.322161
    title: "Robert E. Tarjan, Applications of path compression on balanced trees, Journal of the ACM 26(4) (1979), 690-715"
    locator: the offline lowest common ancestor problem solved with disjoint set union
---

Offline query processing is the technique of reading all queries before answering any of them, and then answering them in an order that suits the data, such as by right endpoint, by threshold, or by time. The answers are stored at the original index of each query and printed in the input order at the end. Reordering turns a hard online problem into an easier one: a range query becomes a prefix query on a structure that grows during a sweep, a deletion becomes an undo, and a batch of queries can share one pass over the data. It applies only when the queries do not depend on earlier answers, which is the [offline](/offline-algorithm/) setting.

## In plain words

Suppose a teacher gets a stack of questions like "how many pupils born before 2010 scored above 80?". Answering them one by one means a new search each time. The teacher can instead read all the questions first, sort them by year, and walk once through the pupils sorted by birth year. When the walk reaches the year of a question, the answer is ready in a running count.

The trick is that the order of the questions is free. The teacher writes each answer next to the number of its question, so the answers can be handed back in the original order.

## When it applies

- **All queries are known in advance.** No query depends on the answer to an earlier one. A problem that encodes each query with the last answer ("xor the input with the previous output") forbids the technique on purpose.
- **A sweep makes one side of the query free.** If the queries have a coordinate that only grows during a sweep (a right endpoint, a time, a threshold), then sorting by it leaves a query with one fewer free parameter: a range $[l, r]$ becomes "all positions $\ge l$ in the structure of the prefix $A[1 \ldots r]$".
- **Insertions are easy, deletions are hard.** Union-find merges sets but cannot split them. Processing the queries in reverse turns deletions into insertions, and a segment tree on time turns them into undo steps, see [offline deletion](/offline-deletion/).
- **The cost of moving between queries is small in a good order.** [Mo's algorithm](/mo-algorithm/) sorts range queries so that a window moves $O(n \sqrt q)$ steps in total.
- **Many queries ask a binary search over the same sequence of events.** [Parallel binary search](/parallel-binary-search/) runs all the searches together, one sweep per round.

## The template

The common form is one sorted sweep over data events and queries, with a structure that answers the reduced query.

```pseudo id=main
OFFLINE(D, Q)                           ▷ D: data events with keys; Q[0 .. q − 1]: queries
L1  for j ← 0 to q − 1 do key_j ← KEY(Q[j])            ▷ the coordinate of the sweep
L2  E ← the events of D and the pairs (key_j, j), sorted by key
L3      (at equal keys, the data events come first)
L4  S ← an empty structure
L5  for each item x of E in order do
L6      if x is a data event then APPLY(S, x)
L7      else ans[j] ← ASK(S, Q[j])          ▷ x = (key_j, j)
L8  return ans
```

The sweep visits each event and each query once, so the cost is the sort, $O((m + q) \log (m + q))$ for $m$ events, plus $m$ calls of APPLY and $q$ calls of ASK. The method is correct when the invariant "before an item with key $k$, the structure $S$ holds exactly the events with key $\le k$, or $< k$ for the item itself if it is a data event" is enough for ASK to answer the query. The tie rule on line L3 decides between $\le$ and $<$, and it must match the query.

## Classic examples

**Distinct values in ranges, by right endpoint.** Given $A[0 \ldots n-1]$ and queries $[l, r)$, count the distinct values of $A[l \ldots r-1]$. Sweep $r$ from 1 to $n$. Keep a mark at the last position $p < r$ of each value, and no mark at the earlier positions of it. Then the number of distinct values in $[l, r)$ is the number of marks in $[l, r)$, because each value that occurs in $[l, r)$ has its last occurrence before $r$ in $[l, r)$. The marks live in a [Fenwick tree](/fenwick-tree/): step $r$ moves the mark of $A[r-1]$ from its old position to $r - 1$, which is two point updates, and a query is one range sum. The cost is $O((n + q) \log n)$. For $A = [1, 2, 1, 3, 2, 2, 4, 1]$:

| after the prefix $A[0 \ldots r-1]$ | marks at positions 0 to 7 | query answered | answer |
|---|---|---|---|
| $r = 3$ | $0, 1, 1, 0, 0, 0, 0, 0$ | $[1, 3)$ | 2 |
| $r = 4$ | $0, 1, 1, 1, 0, 0, 0, 0$ | $[0, 4)$ | 3 |
| $r = 6$ | $0, 0, 1, 1, 0, 1, 0, 0$ | $[3, 6)$ | 2 |
| $r = 7$ | $0, 0, 1, 1, 0, 1, 1, 0$ | $[2, 7)$ | 4 |
| $r = 8$ | $0, 0, 0, 1, 0, 1, 1, 1$ | $[5, 8)$ | 3 |

The same queries take 17 window moves with [Mo's algorithm](/mo-algorithm/), which gives the same answers without a tree but with a worse bound, $O(n \sqrt q)$.

**Range minimum by right endpoint.** [Arpa's trick](/arpa-offline-rmq/) sorts the queries by right end, sweeps the array with a [monotonic stack](/monotonic-stack/), and links each popped position to the new one in a union-find forest. The root of $l$ is then the position of the minimum of $[l, r]$.

**Lowest common ancestors.** [Tarjan's offline LCA algorithm](/tarjan-offline-lca/) attaches each query $(u, v)$ to both nodes, walks the tree in depth-first order, and merges each finished subtree into its parent in a union-find structure. When the walk is at $v$ and $u$ is finished, the representative of $u$ is the lowest common ancestor.

**Thresholds with union-find.** Queries "are $u$ and $v$ connected by edges of weight at most $w$?" are sorted by $w$ and merged with the edges sorted by weight, as in [Kruskal's algorithm](/kruskal/). Each query is one find after all the edges of weight $\le w$ are in.

**Counting inversions and dominance.** Points $(x, y)$ and queries "how many points have $x' \le x$ and $y' \le y$" are sorted by $x$, and the $y$ values go into a Fenwick tree. This is offline [dominance counting](/dominance-counting/), and [counting inversions](/counting-inversions/) is its special case.

## Variations

- **Reverse time.** If the operations only delete, answer them from the last to the first, so that each deletion becomes an insertion. The classic case is union-find under edge deletions.
- **Time as a segment tree.** If each item lives during an interval of time, put it on the $O(\log T)$ nodes of a segment tree over time and walk the tree with an undo stack, see [offline deletion](/offline-deletion/) and [offline dynamic connectivity](/offline-dynamic-connectivity/).
- **Square-root order.** [Mo's algorithm](/mo-algorithm/) sorts by blocks, for queries that a window can answer but a sweep cannot; [Mo's algorithm with updates](/mo-algorithm-with-updates/) adds time as a third key.
- **Divide and conquer on the queries.** Split the sequence of operations in half, let the updates of the first half answer the queries of the second half, and recurse, see [divide and conquer on queries](/divide-and-conquer-on-queries/).
- **Parallel binary search.** Each query keeps a range of candidate answers; each round sorts all midpoints and sweeps once, see [parallel binary search](/parallel-binary-search/).

## Pitfalls

- **Losing the original order.** Each query must carry its index $j$, and the answer must go to $\mathrm{ans}[j]$. Printing in sorted order is the most common bug.
- **The tie rule.** When a data event and a query have the same key, the order of line L3 decides whether the event counts. For "at most $w$" the events go first; for "less than $w$" the queries go first.
- **Forced online input.** If a query is given in a form that needs the previous answer, the queries cannot be sorted, and an online structure such as a [persistent segment tree](/persistent-segment-tree/) is needed.
- **Unstable sorts with equal keys.** Two queries with the same key can be answered in either order only if ASK does not change $S$. If it does, such as a query that also pops a stack, fix the order by a second key.

## Exercises

1. Show that with the marks at the *first* occurrence of each value in the suffix $A[l \ldots n-1]$, a sweep by left endpoint from right to left also counts distinct values in ranges.
2. Given an array and queries "how many items of $A[l \ldots r]$ are at most $x$?", design an offline method with $O((n + q) \log n)$ time.
3. Edges of a graph are deleted one by one, and after each deletion you must report the number of connected components. Solve it with union-find by reversing time.
4. Explain why Tarjan's offline LCA algorithm needs the queries attached to both endpoints.
5. Queries ask for the sum of $A[l \ldots r]$ after the first $t$ of a list of point updates. Answer them offline by sorting on $t$.

## References
