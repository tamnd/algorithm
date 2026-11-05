---
tag: JAH419
kind: technique
slug: parallel-binary-search
name: Parallel binary search
aliases:
- simultaneous binary search
- overall binary search
area: searching/search-on-answers
level: advanced
summary: Answers many binary-search queries together by sweeping all candidate midpoints in rounds, reusing one shared data structure instead of searching each query separately.
prereqs: [binary-search-on-answer, monotone-predicate, offline-query-processing]
see_also: [binary-search-on-answer, offline-query-processing, fenwick-tree, disjoint-set, range-kth-smallest-query, persistent-segment-tree, range-update-point-query, parametric-search]
sources:
  - url: https://cp-algorithms.com/num_methods/binary_search.html
    title: cp-algorithms, Binary search
    note: the section Parallel Binary Search, with the Meteors problem
  - book: isbn:9783319725468
    title: Antti Laaksonen, Guide to Competitive Programming, first edition, Springer, 2017
    locator: Section 15.5.3, Parallel Binary Search
---

Parallel binary search answers $Q$ queries of the form "after how many of the updates $u_1, \ldots, u_T$ does the condition of query $q$ first hold?" when each condition is monotone in the number of updates. A separate [binary search on the answer](/binary-search-on-answer/) for each query would rebuild the state of the updates $\lceil \lg(T+1) \rceil$ times per query. Parallel binary search instead runs all the searches in lockstep: in each round it sorts the queries by their current midpoint, applies the updates once from the start, and checks each query when the sweep reaches its midpoint. So $\lceil \lg(T+1) \rceil$ sweeps answer all queries, in $O((T \cdot c_u + Q \cdot c_q) \log T)$ time for update cost $c_u$ and check cost $c_q$. It is an [offline](/offline-query-processing/) technique: all queries must be known in advance.

## In plain words

Many people each wait for something to happen, such as their savings reaching a target, while a long list of events changes everything. Each person could find their moment alone, by replaying the events up to the middle, checking, and replaying again. But replaying is slow, and doing it for every person is very slow.

Instead, give everyone a guess at once. Replay the events a single time from the start, and whenever the replay reaches someone's guess, check that person and tell them whether their moment came earlier or later. Everyone halves their range in this one replay. After a few replays, as many as a binary search would need, everyone knows their moment.

## When it applies

- **A shared sequence of updates.** There is a state $S_0$ and updates $u_1, \ldots, u_T$; let $S_t$ be the state after the first $t$ updates. A data structure can apply an update in time $c_u$ and can be reset to $S_0$ cheaply.
- **Many queries with a monotone condition.** Each query $q$ has a predicate $P_q(t)$ that is computed from $S_t$ in time $c_q$, and it is a [monotone predicate](/monotone-predicate/) in $t$: $t \le t'$ and $P_q(t)$ imply $P_q(t')$. The answer to $q$ is the smallest $t \in \{1, \ldots, T\}$ with $P_q(t)$, or "never". Monotonicity usually holds because the updates only add: adding amounts to counters, adding edges to a graph, inserting elements into a set.
- **Offline.** All queries are known before the first round.
- **No cheap access to old states.** If the structure is persistent, so that $S_t$ can be queried for any $t$ directly, each query can run its own binary search with no rounds; parallel binary search is the method when the structure is not persistent.

## The template

Each query keeps a range $[lo_q, hi_q]$ that holds its answer, where $T + 1$ stands for "never".

```pseudo id=main
PARALLEL-BINARY-SEARCH(queries, u_1..u_T)
L1  for each query q do lo[q] ← 1;  hi[q] ← T + 1
L2  repeat ⌈lg(T + 1)⌉ times
L3      bucket[t] ← the queries q with lo[q] < hi[q] and ⌊(lo[q] + hi[q]) / 2⌋ = t
L4      reset the structure to S_0
L5      for t ← 1 to T do
L6          apply u_t                                 ▷ the structure now holds S_t
L7          for each q in bucket[t] do
L8              if P_q(t) then hi[q] ← t else lo[q] ← t + 1
L9  return lo                                     ▷ lo[q] = T + 1 means never
```

Line L3 is a [counting sort](/counting-sort/) of the active queries by midpoint, in $O(Q + T)$ time.

**Correctness.** Fix a query $q$ and let $a_q$ be its answer, the smallest $t \le T$ with $P_q(t)$, or $T + 1$ if there is none. The invariant is $lo_q \le a_q \le hi_q$. It holds at the start. In a round, if $lo_q < hi_q$, then $m = \lfloor (lo_q + hi_q)/2 \rfloor$ satisfies $lo_q \le m < hi_q \le T + 1$, so $1 \le m \le T$ and $q$ is in a bucket. When the sweep reaches $m$, the structure holds exactly $S_m$, because the updates are applied in order from $S_0$. If $P_q(m)$ holds, then $a_q \le m$ by the definition of $a_q$. If not, monotonicity gives $\neg P_q(t)$ for every $t \le m$, so $a_q \ge m + 1$. So the invariant holds after the round. This is exactly the step of SMALLEST-FEASIBLE on the page [binary search on the answer](/binary-search-on-answer/); the rounds only change the order in which the steps of different queries are done.

**Number of rounds.** A range of $\ell + 1$ values, with $\ell = hi_q - lo_q \ge 1$, becomes a range of at most $\lceil (\ell + 1)/2 \rceil$ values. Starting from $T + 1$ values, $\lceil \lg(T + 1) \rceil$ rounds leave one value, so $lo_q = hi_q = a_q$ at the end.

**Cost.** Each round makes $T$ updates, $O(Q)$ checks, a reset and a counting sort. The total is $O\big((T c_u + Q c_q + Q + T + R) \log T\big)$, where $R$ is the cost of a reset. Separate searches would cost $O(Q (T c_u + c_q) \log T)$, because each step of each search rebuilds the state.

## Classic examples

### Range additions and thresholds

Four cells start at $0$. The updates are: $u_1$ adds $2$ to cells $1$ to $2$, $u_2$ adds $1$ to cells $2$ to $4$, $u_3$ adds $3$ to cell $1$, $u_4$ adds $2$ to cells $3$ to $4$. The states are $S_1 = (2, 2, 0, 0)$, $S_2 = (2, 3, 1, 1)$, $S_3 = (5, 3, 1, 1)$, $S_4 = (5, 3, 3, 3)$. The queries ask when a cell first reaches a target: $q_1$: cell $1 \ge 4$; $q_2$: cell $2 \ge 3$; $q_3$: cell $4 \ge 3$; $q_4$: cell $3 \ge 5$. A [Fenwick tree](/fenwick-tree/) with range additions and point queries holds the state, with $c_u = c_q = O(\log n)$; see [range update, point query](/range-update-point-query/).

| round | $q_1$ | $q_2$ | $q_3$ | $q_4$ |
|---|---|---|---|---|
| 1 | $[1,5]$, mid 3: 5, yes | $[1,5]$, mid 3: 3, yes | $[1,5]$, mid 3: 1, no | $[1,5]$, mid 3: 1, no |
| 2 | $[1,3]$, mid 2: 2, no | $[1,3]$, mid 2: 3, yes | $[4,5]$, mid 4: 3, yes | $[4,5]$, mid 4: 3, no |
| 3 | $[3,3]$, done | $[1,2]$, mid 1: 2, no | $[4,4]$, done | $[5,5]$, done |

The answers are $3$, $2$, $4$ and never, after $\lceil \lg 5 \rceil = 3$ sweeps.

### Meteors

In the problem Meteors from the Polish Olympiad in Informatics of 2011, a circle of $m$ sectors is owned by $n$ states, $k$ meteor showers each add an amount to a circular range of sectors, and each state asks after which shower its sectors have collected its target. The check of a state sums the point values of its sectors, so the checks of one round take $O(m \log m)$ in total, and the showers $O(k \log m)$. With $\lceil \lg(k + 1) \rceil$ rounds the total is $O((m + k) \log m \log k)$, while separate searches would cost a factor of about $n$ more.

### Connectivity over time

Edges $e_1, \ldots, e_T$ are added to a graph one at a time, and each query asks when two given vertices first become connected. The state is a [disjoint-set](/disjoint-set/) structure; adding an edge is a union, and a check is two finds. Connectivity only grows, so the predicate is monotone. Each round resets the structure and adds the edges in order, for $O((T + Q)\,\alpha(n) \log T)$ in total.

### The k-th smallest in a range

For [range k-th smallest queries](/range-kth-smallest-query/), sort the array values and search on the value: the updates insert the array positions in increasing order of value into a Fenwick tree, and the query "is the $k$-th smallest of $A[l..r]$ at most the $t$-th smallest value?" is "are at least $k$ positions of $[l, r]$ inserted after $t$ updates?", which is monotone in $t$. This gives $O((n + Q) \log^2 n)$ offline.

## Variations

- **Recursive form.** Process a value range $[lo, hi]$ together with the queries whose answers lie in it: apply the updates of the left half, split the queries by their check, recurse on the left half with the "yes" queries, undo the updates, and recurse on the right half with the "no" queries. Each update and query is handled $O(\log T)$ times, and no full reset is needed. In Chinese contest literature this is called overall binary search.
- **Persistent structures.** A [persistent segment tree](/persistent-segment-tree/) keeps every $S_t$, so each query can run its own binary search online, at the price of $O(T \log n)$ memory.
- **A search over values.** The "time" axis can be any sorted list of candidate values, as in the k-th smallest example: the updates are the candidates in order.
- **Other structures.** Any structure with cheap updates and a cheap reset works: Fenwick and [segment trees](/segment-tree/), disjoint sets, counters, bitsets.

## Pitfalls

- **Updates that undo progress.** If an update can make a predicate false again, such as a subtraction in a sum or the removal of an edge, the predicate is not monotone in $t$, and the search returns a wrong time. Check monotonicity for each query, not only for the structure.
- **Forgetting the reset.** Each round must start from $S_0$. A structure that keeps the state of the last round gives checks on $S_{T + t}$.
- **Overflow.** In Meteors, the sum of a state can exceed 64 bits when many showers hit many sectors. Stop adding once the sum reaches the target.
- **Rounds by a fixed count with "never".** Use $T + 1$ as the upper end so that queries without an answer converge to $T + 1$, and make sure the midpoint is never $T + 1$; the invariant $lo < hi \le T + 1$ ensures this.
- **Sorting the queries in each round by comparison.** A comparison sort adds a factor $\log Q$ per round; the bucket array of line L3 avoids it.

## Exercises

1. Prove that the recursive form handles each update $O(\log T)$ times and each query $O(\log T)$ times.
2. In the connectivity example, why can a disjoint-set structure without undo be used in the round form but not directly in the recursive form? How does union by rank without path compression help?
3. Give an example of updates and a query for which the predicate is not monotone, and show the wrong answer that the template returns.
4. Queries ask for the first time when the sum of a whole array reaches a target, with only point additions. Show that no binary search is needed, and find a direct $O(T + Q \log Q)$ method.

## References
