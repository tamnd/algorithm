---
tag: 8T0DN0
kind: definition
slug: offline-dynamic-graph
name: Offline dynamic graph
aliases:
- offline dynamic model
area: graphs/dynamic-graphs
level: core
summary: The whole sequence of updates is known in advance, which permits divide-and-conquer over time.
prereqs: [dynamic-graph, fully-dynamic-graph]
see_also: [offline-dynamic-connectivity, rollback-technique, union-find-with-rollback, divide-and-conquer-on-queries, incremental-graph, decremental-graph, temporal-graph]
sources:
  - paper: "David Eppstein, Offline algorithms for dynamic minimum spanning tree problems, Journal of Algorithms 17(2), 237 to 250 (1994)"
    locator: Section 1 (the offline model, where the whole sequence of updates is known in advance)
  - paper: doi:10.1145/265910.265914
    title: David Eppstein, Zvi Galil, Giuseppe F. Italiano and Amnon Nissenzweig, Sparsification, a technique for speeding up dynamic graph algorithms, Journal of the ACM 44(5), 669 to 696 (1997)
    locator: Section 1 (online dynamic problems, for contrast)
  - url: https://cp-algorithms.com/data_structures/deleting_in_log_n.html
    title: cp-algorithms, Deleting from a data structure in O(T(n) log n)
    locator: the whole article (the segment tree over time and the offline connectivity example)
---

An offline dynamic graph is a [dynamic graph](/dynamic-graph/) problem in which the algorithm receives the whole sequence of updates and queries at the start, and may answer the queries in any order, as long as each answer is about the graph at the time of its query. Knowing the future lets the algorithm give each edge its lifetime, an interval of time, and then process time by divide and conquer instead of step by step. Many offline problems are much easier than their online versions: offline [fully dynamic](/fully-dynamic-graph/) connectivity needs only a [disjoint-set forest](/disjoint-set-forest/) that can undo its last unions.

## Definition

Fix a vertex set $V$ with $n = |V|$. An **instance** of an offline dynamic graph problem is a finite sequence $\sigma = (o_1, o_2, \ldots, o_k)$ of operations, where each $o_t$ is an update (for example $\mathrm{insert}(u, v)$ or $\mathrm{delete}(u, v)$) or a query (for example $\mathrm{connected}(u, v)$). Let $G_t$ be the graph after the updates among $o_1, \ldots, o_t$. An **offline algorithm** reads all of $\sigma$ and outputs, for each query $o_t$, the value $q(G_t, o_t)$. It does not need to answer $o_t$ before it reads $o_{t+1}$.

An **online algorithm**, in contrast, must output the answer to $o_t$ before it reads $o_{t+1}$. Each online algorithm is also an offline algorithm, with the same cost, so the offline model can only be easier.

**Lifetimes.** In an offline sequence of edge insertions and deletions, each insertion of an edge $e$ at time $l$ is matched with the next deletion of $e$ at time $r$, or with $r = k + 1$ if $e$ is never deleted again. The interval $[l, r)$ is a **lifetime** of $e$, and

$$E_t = \{\, e : t \in [l, r) \text{ for some lifetime } [l, r) \text{ of } e \,\}.$$

So an offline fully dynamic edge sequence is the same as a set of edges with time intervals, which is a [temporal graph](/temporal-graph/) with interval labels. Computing the lifetimes takes $O(k)$ expected time with a hash table of open insertions, or $O(k \log k)$ time with a balanced search tree.

**Cost.** The cost is the total time for all of $\sigma$, often stated as an amortized time per operation. A bound such as $O(\log^2 n)$ per operation means $O(k \log^2 n)$ in total, and says nothing about the delay before any one answer.

## Examples and non-examples

**Example: lifetimes and answers.** Take $V = \{0, 1, 2, 3\}$ and the sequence

| time | operation | edges after it | answer |
|---|---|---|---|
| 1 | insert(0, 1) | 01 | |
| 2 | insert(1, 2) | 01, 12 | |
| 3 | connected(0, 2) | 01, 12 | true |
| 4 | delete(0, 1) | 12 | |
| 5 | insert(2, 3) | 12, 23 | |
| 6 | connected(0, 3) | 12, 23 | false |
| 7 | connected(1, 3) | 12, 23 | true |
| 8 | delete(1, 2) | 23 | |
| 9 | connected(1, 3) | 23 | false |

The lifetimes are $[1, 4)$ for $01$, $[2, 8)$ for $12$ and $[5, 10)$ for $23$, with $k = 9$. The query at time 7 sees exactly the edges whose interval contains 7, which are $12$ and $23$. [Offline dynamic connectivity](/offline-dynamic-connectivity/) places each interval on $O(\log k)$ nodes of a segment tree over the times $1$ to $k$, walks the tree with a [union-find with rollback](/union-find-with-rollback/), and answers all queries in $O(k \log k \log n)$ time.

**Example: decremental by reversal.** If all updates are deletions and they are known in advance, read the sequence backwards. The deletions become insertions, so the problem becomes [incremental](/incremental-graph/). For connectivity, a disjoint-set forest then answers all queries in $O(\alpha(n))$ amortized time per operation, while online [decremental connectivity](/decremental-connectivity/) of general graphs needs more complex structures.

**Example: offline minimum spanning forest.** Eppstein (1994) maintains the weight of the minimum spanning forest of a graph under an offline sequence of edge updates in $O(\log n)$ amortized time per update, while the best online bounds are polylogarithmic of higher degree.

**Non-example: answers needed at once.** A network monitor must report a disconnection when it happens. Its sequence is online, even if the operator could later replay it offline.

**Non-example: a static graph with many queries.** If no update occurs, the problem is static, and one pass over the graph answers every query.

**Non-example: a known insertion time only.** If each edge reveals its deletion time when it is inserted, but future insertions are unknown, the setting lies between online and offline. It is sometimes called semi-online. A lifetime is known as soon as the edge exists, but the segment tree over time cannot be built in advance.

## Related definitions

- **[Rollback technique](/rollback-technique/).** Offline algorithms walk a recursion over time, add edges on the way down and undo them on the way back up. They need a structure whose undo is cheap in the worst case, such as [union-find with rollback](/union-find-with-rollback/).
- **[Divide and conquer on queries](/divide-and-conquer-on-queries/).** The general method of splitting the time range of an offline sequence and recursing on both halves.
- **[Temporal graph](/temporal-graph/).** A graph whose edges carry time labels. An offline edge sequence turned into lifetimes is a temporal graph, but temporal graph problems also ask about paths that move forward in time.
- **[Incremental graph](/incremental-graph/) and [decremental graph](/decremental-graph/).** Offline, the two classes are the same up to reversal of the sequence.
- **[Fully dynamic graph](/fully-dynamic-graph/).** The online setting with insertions and deletions, which offline algorithms avoid.

## References
