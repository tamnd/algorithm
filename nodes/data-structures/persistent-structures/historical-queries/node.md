---
tag: ATEQ93
kind: problem
slug: historical-queries
name: Historical queries
aliases:
- queries on past versions
- versioned range queries
area: data-structures/persistent-structures
level: advanced
summary: Answer a query such as a range sum or count against the state of the structure at an earlier time.
prereqs: [partial-persistence, range-query-problem]
see_also: [persistent-segment-tree, range-kth-smallest-query, dominance-counting, sarnak-tarjan-point-location, retroactive-data-structure, offline-orthogonal-range-counting, fat-node, node-copying]
sources:
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: pages 86 to 124, the introduction (queries on past versions as the purpose of partial persistence, and the applications)
  - paper: doi:10.1145/6138.6151
    title: Neil Sarnak and Robert E. Tarjan, Planar point location using persistent search trees, Communications of the ACM 29(7), 1986
    locator: pages 669 to 679 (point location as a historical search query on a sweep of the plane)
---

The historical query problem asks a data structure that is changed over time to answer queries about any earlier state, not only the current one: "how many keys between 10 and 20 were in the set after the 500th update?" When the updates arrive in time order and the queries may come at any moment, this is exactly what a [partially persistent](/partial-persistence/) structure provides. Many problems that do not mention time become historical queries once one coordinate is read as time: a count of the points dominated by a query point is a count of keys at a past moment of a sweep, and the [range k-th smallest query](/range-kth-smallest-query/) is a query on the difference of two versions of a [persistent segment tree](/persistent-segment-tree/).

## In plain words

A list of changes is applied, one after another, to some collection of data: numbers are added, removed or changed. Later, someone asks a question about the collection, but as it was at some past moment: what was the total, how many values fell in a range, which one was the third smallest. You do not want to replay all changes up to that moment for each question. So you keep the history in a form that can answer questions about any moment directly, while still taking new changes at the end.

## Definition

Fix an abstract data type with a set of states, updates $u : S \to S$ and queries $q : S \to R$. An input consists of an initial state $S_0$ and a sequence of updates $u_1, u_2, \ldots, u_m$, which define the versions $S_t = u_t(S_{t - 1})$ for $1 \le t \le m$. A **historical query** is a pair $(t, q)$ with $0 \le t \le m$, and its answer is $q(S_t)$.

- In the **online** form, the updates and the historical queries arrive interleaved. A query $(t, q)$ that arrives after $u_j$ has $t \le j$. This is the problem that partial persistence solves.
- In the **offline** form, all updates and queries are given at once, and the answers may be computed in any order.

The cost measures are the time per update, the time per query, and the space, as functions of $m$ and of the size $n$ of the states. A solution is compared with the best ephemeral structure for the same type, which answers queries only about $S_m$.

## Variants

- **Historical range counting and range sums.** The states are sets or arrays of numbers, and the query asks for the count or the sum of the values whose keys lie in a range $[a, b]$.
- **Prefix versions of an array.** The updates are the appends of $A[1], A[2], \ldots, A[n]$ to an empty multiset, so the version $t$ is the multiset of $A[1 .. t]$. A query on $A[l .. r]$ combines the versions $r$ and $l - 1$. This is how the [range k-th smallest query](/range-kth-smallest-query/) and range distinct counts are solved online.
- **Historical search.** The state is an ordered set and the query asks for the predecessor of a key at time $t$. Planar point location is of this kind.
- **Branching history.** If updates may also apply to old versions, the versions form a tree and the problem needs [full persistence](/full-persistence/).
- **Not this problem: changing the past.** An update inserted at time $t$ that changes all later versions is a retroactive update; see [retroactive data structure](/retroactive-data-structure/). Historical queries never change a version.

## Examples

Let $A = (3, 1, 4, 1, 5)$, and let version $t$ be the multiset $\{A[1], \ldots, A[t]\}$. The query "how many values of $A[2 .. 4]$ are at most 3" is the count of values at most 3 in version 4 minus the same count in version 1.

| version | multiset | values at most 3 |
|---|---|---|
| 1 | $\{3\}$ | 1 |
| 4 | $\{3, 1, 4, 1\}$ | 3 |

The answer is $3 - 1 = 2$, which matches $A[2 .. 4] = (1, 4, 1)$. A persistent segment tree over the values 1 to 5 holds all five versions in $O(n \log n)$ space, and answers each such query by walking down two versions at once in $O(\log n)$ time.

A second example with deletions: start with the empty set, insert 5, insert 2, delete 5, insert 7. The versions are $\emptyset$, $\{5\}$, $\{2, 5\}$, $\{2\}$ and $\{2, 7\}$. The historical query "the smallest key greater than 3 at time 2" has the answer 5, while the same query on the current set has the answer 7.

## Known algorithms

- **Replay.** Store the updates and, for a query $(t, q)$, rebuild $S_t$ from $S_0$. This uses $O(m)$ space but $\Omega(t)$ time per query.
- **Copy every version.** Store each $S_t$. Queries run at full speed, but the space is $\Theta(nm)$.
- **Path copying.** A balanced tree or a [segment tree](/segment-tree/) with [path copying](/path-copying/) keeps every version in $O(\log n)$ extra space per update, and answers a query on any version in the time of the ephemeral query, $O(\log n)$ for range counts and sums.
- **Node copying.** For linked structures of bounded in-degree, [node copying](/node-copying/) gives partial persistence with $O(1)$ amortized space per update step and $O(1)$ time per access step. With a [red-black tree](/red-black-tree/), this answers historical searches in $O(\log n)$ time, with $O(n + m)$ space in total.
- **Fat nodes.** The [fat node](/fat-node/) method uses $O(1)$ space per update step but adds a factor $O(\log m)$ to the query time.
- **Offline sweep.** In the offline form, sort the queries by time and apply the updates in order to an ephemeral structure, answering each query when its time is reached. With a [Fenwick tree](/fenwick-tree/) this gives historical range sums in $O((m + Q) \log n)$ time and $O(n)$ space for $Q$ queries.

## Bounds

A historical query with $t = m$ is a query on the current state, so every lower bound for the ephemeral problem applies to the historical one. The general methods above show that, for structures of bounded in-degree in the [pointer machine](/pointer-machine/) model, the historical problem costs at most a constant factor more in time and space than the ephemeral one, with $O(1)$ amortized space per update step. Space is the main cost in practice: path copying adds $\Theta(\log n)$ space per update to a balanced tree, and node copying removes it.

## Reductions

- **Historical counting and dominance counting.** For a set that only grows, the count of keys in $[a, b]$ at time $t$ equals the number of points $(\text{key}, \text{time})$ with $a \le \text{key} \le b$ and $\text{time} \le t$, which is a query of [orthogonal range counting](/orthogonal-range-counting/) on the points of insertion. Conversely, a [dominance counting](/dominance-counting/) query "how many points $(x', y')$ have $x' \le x$ and $y' \le y$" becomes a historical count: insert the $y$-coordinates in increasing order of $x$, and count the keys at most $y$ in the version after the last point with $x' \le x$. So the two problems have the same complexity up to a sort.
- **With deletions.** If a key is inserted at time $s$ and deleted at time $e$, it is present at time $t$ exactly when $s \le t < e$. A historical count then becomes a three-sided query on the points $(\text{key}, s, e)$.
- **Point location.** Sweeping a planar subdivision with a vertical line, with time as the $x$-coordinate, turns point location into a historical search in the set of edges that cross the line; see [Sarnak-Tarjan point location](/sarnak-tarjan-point-location/).

## Applications

- [Planar point location](/planar-point-location/) in linear space and logarithmic time.
- Range queries on subarrays by prefix versions: the range k-th smallest, the number of distinct values in a range, and range counts of values below a bound.
- Databases and file systems that answer queries "as of" a past time, and version control tools that show the state of a file at a past commit.
- [Offline orthogonal range counting](/offline-orthogonal-range-counting/), which is the offline form of the historical count.

## References
