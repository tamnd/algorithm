---
tag: 798KD6
kind: technique
slug: divide-and-conquer-on-queries
name: Divide and conquer on queries
area: techniques/divide-and-conquer
level: advanced
summary: Solves offline query problems by recursing over a time or index range, applying updates on the way down and rolling them back with an undoable structure.
prereqs: [divide-and-conquer-paradigm, segment-tree, union-find-with-rollback, offline-algorithm]
see_also: [offline-dynamic-connectivity, rollback-technique, offline-deletion, offline-query-processing, parallel-binary-search, dominance-counting, fenwick-tree, dynamic-connectivity]
sources:
  - url: https://cp-algorithms.com/data_structures/deleting_in_log_n.html
    title: cp-algorithms, Deleting from a data structure in O(T(n) log n)
    locator: sections Algorithm, Notes and Implementation (segment tree over time, union-find with rollbacks, offline dynamic connectivity)
  - paper: "David Eppstein, Offline algorithms for dynamic minimum spanning tree problems, Journal of Algorithms 17(2) (1994), doi:10.1006/jagm.1994.1033"
    locator: pages 237 to 250 (the update sequence is split into blocks recursively; O(k log n) total time for k updates)
  - paper: "Richard Peng, Bryce Sandlund and Daniel D. Sleator, Optimal offline dynamic 2,3-edge/vertex connectivity, Algorithms and Data Structures (WADS 2019), Lecture Notes in Computer Science, doi:10.1007/978-3-030-24766-9_40"
    locator: pages 553 to 565 (offline 2- and 3-edge and vertex connectivity by divide and conquer over the operation sequence, O(log n) time per operation)
  - url: https://www.cs.princeton.edu/~danqic/papers/divide-and-conquer.pdf
    title: Chen Danqi, 从《Cash》谈一类分治算法的应用 (Applications of a class of divide-and-conquer algorithms, starting from the problem Cash), 2008 Chinese national olympiad training team paper, Yali High School
    locator: whole paper (the first half of the operations updates the second half, then the recursion continues)
  - paper: "Jon Louis Bentley, Multidimensional divide-and-conquer, Communications of the ACM 23(4) (1980), doi:10.1145/358841.358850"
    locator: pages 214 to 229 (dominance counting and related problems by divide and conquer on one coordinate)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 19, Data Structures for Disjoint Sets (union by rank, path compression)
---

Divide and conquer on queries is a family of [offline](/offline-algorithm/) methods that recurse over the time line of a known sequence of updates and queries, rather than over the input items. This page describes two members that are often confused. The first, divide and conquer over time, stores each update on the nodes of a [segment tree](/segment-tree/) over time, walks the tree with a structure that can undo its last change, and answers each query at a leaf; it turns a structure that supports insertions only into one that also supports deletions, at a cost of a $\log q$ factor. The second, CDQ divide and conquer, splits the operation sequence into halves and counts the effect of the updates in the left half on the queries in the right half by a sweep; it removes the time dimension from a problem at a cost of a $\log n$ factor.

## In plain words

Some problems give you the whole list of changes and questions in advance, so you can choose a better order of work.

In the first method, each change is valid during a stretch of time. Draw the time line as a tree of nested stretches. Hang each change on the few big stretches that make up its own stretch. Walk the tree from the top: when you go down, make the changes that hang there; when you come back up, undo them. When you reach a single moment, exactly the changes valid at that moment are in effect, so you answer its question there.

In the second method, cut the list of operations in the middle. Solve each half on its own. What is missing is the effect of the early changes on the late questions, which is one simple pass with no time order in it.

## When it applies

- **The whole sequence is known in advance.** All updates and queries are given before the first answer is due. This is the main condition; an online problem, where the next operation depends on the last answer, does not fit.
- **Deletions are hard, insertions are easy (divide and conquer over time).** The structure supports "add an item" in time $T(n)$ and can undo the last addition in the same time, but it has no good delete. [Union-find](/disjoint-set-forest/) is the classic case: it merges sets but cannot split them. Each item is present on an interval of time.
- **Updates add up and do not interact (CDQ).** The answer to a query is a sum (or a minimum, or any combination that can be built in pieces) over the earlier updates of a contribution that depends only on the update and the query. With time as one coordinate, the problem becomes a static problem with one more dimension, such as [dominance counting](/dominance-counting/).
- **A simpler static problem is easy.** Each method calls a static or incremental routine many times on parts of the input, so that routine must be fast.

## The template

### Divide and conquer over time

Number the operations $1, \dots, q$. Each item $e$ (an edge, a point, a number) is present on a closed interval of times $[s_e, t_e]$: from its insertion to just before its deletion, or to $q$ if it is never deleted. Build a segment tree over $[1, q]$.

```pseudo id=main
OFFLINE-OVER-TIME(ops[1 .. q])
L1  for each item e with lifetime [s_e, t_e] do              ▷ hole: what an item is
L2      INSERT-INTERVAL(root, 1, q, s_e, t_e, e)
L3  D ← an empty undoable structure                          ▷ hole: the structure D
L4  VISIT(root, 1, q)

INSERT-INTERVAL(v, lo, hi, s, t, e)
L5  if t < lo or hi < s then return
L6  if s ≤ lo and hi ≤ t then append e to items(v); return
L7  mid ← ⌊(lo + hi) / 2⌋
L8  INSERT-INTERVAL(left(v), lo, mid, s, t, e)
L9  INSERT-INTERVAL(right(v), mid + 1, hi, s, t, e)

VISIT(v, lo, hi)
L10 mark ← CHECKPOINT(D)                                     ▷ the size of the undo stack
L11 for each e in items(v) do ADD(D, e)                      ▷ hole: ADD, with an undo record
L12 if lo = hi then
L13     if ops[lo] is a query then answer[lo] ← QUERY(D, ops[lo])   ▷ hole: QUERY
L14 else
L15     mid ← ⌊(lo + hi) / 2⌋
L16     VISIT(left(v), lo, mid)
L17     VISIT(right(v), mid + 1, hi)
L18 ROLLBACK(D, mark)                                        ▷ undo the changes of line L11
```

The holes are the kind of item, the structure $D$ with its operations ADD and QUERY, and an undo record for each ADD. Lines L5 to L9 are the usual range update of a segment tree: an interval is stored at the nodes whose ranges lie inside it and whose parents' ranges do not. Lines L10 and L18 make each visit leave $D$ as it found it.

**Why it is correct.** The nodes chosen for $[s_e, t_e]$ by lines L5 to L9 have disjoint ranges whose union is $[s_e, t_e]$. The nodes on the path from the root to leaf $\tau$ are exactly the nodes whose range contains $\tau$. So $e$ is stored on that path at most once, and it is stored there if and only if $\tau \in [s_e, t_e]$. By induction on the depth, at the start of line L12 in VISIT of a node $v$, $D$ holds exactly the items stored on the path from the root to $v$, because each child visit ends with $D$ restored (line L18). At the leaf $\tau$, $D$ therefore holds exactly the items present at time $\tau$, and line L13 answers the query on the right set.

**Cost.** A range $[s, t]$ is stored at no more than 2 nodes on each level, so at $O(\log q)$ nodes. With $m$ items, the total number of ADD calls is $O(m \log q)$, and each is undone once. If ADD and its undo cost $T(n)$ in the worst case, the total time is $O(q + m \, T(n) \log q)$ plus the queries, and the memory is $O(m \log q)$. This is the "deletion in $O(T(n) \log n)$ offline" of cp-algorithms.

**Offline dynamic connectivity.** The items are edges, $D$ is [union-find with rollback](/union-find-with-rollback/), and a query asks whether two vertices are in the same component. ADD$(D, \{u, v\})$ finds the two roots; if they differ, it links the root of smaller rank below the other ([union by rank](/union-by-rank/)) and pushes the changed parent pointer and rank on a stack. ROLLBACK pops these records. There is no [path compression](/path-compression/): with union by rank alone each tree has height at most $\lfloor \log_2 n \rfloor$ (CLRS, Chapter 19), so FIND costs $O(\log n)$ in the worst case and each union changes $O(1)$ fields. With $q$ operations on $n$ vertices the total time is $O(q \log q \log n)$. This is the algorithm of the page [offline dynamic connectivity](/offline-dynamic-connectivity/).

### CDQ divide and conquer

```pseudo id=cdq
CDQ(l, r)                                     ▷ ops[l .. r], in time order
C1  if l = r then return
C2  m ← ⌊(l + r) / 2⌋
C3  CDQ(l, m)
C4  CROSS(l, m, r)                            ▷ hole: add the effect of the updates in ops[l .. m] to the queries in ops[m+1 .. r]
C5  CDQ(m + 1, r)
```

The hole is CROSS. In it, every update is earlier than every query, so time no longer matters, and CROSS is a static problem: sort both groups by one coordinate and sweep, keeping the updates seen so far in a simple structure such as a [Fenwick tree](/fenwick-tree/).

**Why it is correct.** Take an update $i$ and a later query $j$, so $i < j$. Among the calls of CDQ, exactly one has $l \le i \le m < j \le r$: the smallest range that holds both. So the contribution of $i$ to $j$ is added once, in line C4 of that call, and no pair with $i > j$ is ever added. If the answer is a sum of such contributions, each query gets its full answer. The order "left, cross, right" also covers the case where an update depends on the answer to an earlier query, as in the dynamic program of Chen Danqi's paper: when line C4 runs, every query in $ops[l..m]$ is already final, and every query $j$ has received all the contributions from the left before the recursion reaches it.

**Cost.** If CROSS on a range of length $k$ costs $O(k \log n)$ (a sort and a Fenwick tree sweep), the total is $T(n) = 2T(n/2) + O(n \log n) = O(n \log^2 n)$ for $n$ operations. If CROSS needs only a merge of lists already sorted by the recursion, the total is $O(n \log n)$.

## Classic examples

### A trace of divide and conquer over time

Four vertices $1, 2, 3, 4$ and eight operations, numbered by time:

| time | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| operation | add 1-2 | add 2-3 | is 1 ~ 3? | add 3-4 | remove 2-3 | is 1 ~ 4? | add 1-4 | is 2 ~ 4? |

There are five edge events and three queries. The lifetimes are $1\text{-}2: [1, 8]$, $2\text{-}3: [2, 4]$, $3\text{-}4: [4, 8]$ and $1\text{-}4: [7, 8]$. Lines L5 to L9 store them at these nodes of the segment tree over $[1, 8]$:

| node | $[1, 8]$ | $[2, 2]$ | $[3, 4]$ | $[4, 4]$ | $[5, 8]$ | $[7, 8]$ |
|---|---|---|---|---|---|---|
| edges | 1-2 | 2-3 | 2-3 | 3-4 | 3-4 | 1-4 |

The walk with union by rank (on a tie of ranks, the root of the first vertex becomes the parent):

| step | node | action | parent pointers changed | rank change |
|---|---|---|---|---|
| 1 | $[1, 8]$ | union 1-2 | $2 \to 1$ | rank of 1 becomes 1 |
| 2 | $[2, 2]$ | union 2-3 | $3 \to 1$ | none |
| 3 | leave $[2, 2]$ | rollback | $3 \to 3$ | none |
| 4 | $[3, 4]$ | union 2-3 | $3 \to 1$ | none |
| 5 | leaf 3 | query 1 ~ 3 | roots 1 and 1: **yes** | |
| 6 | $[4, 4]$ | union 3-4, then rollback on leaving | $4 \to 1$, then $4 \to 4$ | none |
| 7 | leave $[3, 4]$ | rollback | $3 \to 3$ | none |
| 8 | $[5, 8]$ | union 3-4 | $4 \to 3$ | rank of 3 becomes 1 |
| 9 | leaf 6 | query 1 ~ 4 | roots 1 and 3: **no** | |
| 10 | $[7, 8]$ | union 1-4 | $3 \to 1$ | rank of 1 becomes 2 |
| 11 | leaf 8 | query 2 ~ 4 | roots 1 and 1 (path $4 \to 3 \to 1$): **yes** | |

The answers are yes, no, yes. At step 5 the path from the root holds 1-2 and 2-3, the edges present at time 3; at step 9 it holds 1-2 and 3-4, the edges present at time 6; at step 11 it holds 1-2, 3-4 and 1-4.

### A trace of CDQ

Operations on a line: "add $x$" puts a point at $x$; "count $\le X$" asks how many points added before it are at most $X$. The sequence is: 1 add 3, 2 add 7, 3 count $\le 5$, 4 add 1, 5 count $\le 4$, 6 add 5, 7 add 2, 8 count $\le 5$. CROSS sorts the left adds and the right queries by coordinate and sweeps, with an add before a query at the same coordinate.

| call | adds on the left | queries on the right | added to the answers |
|---|---|---|---|
| $[1, 4]$ | 3, 7 | op 3 ($\le 5$) | op 3: 1 |
| $[7, 8]$ | 2 | op 8 ($\le 5$) | op 8: 1 |
| $[5, 8]$ | 5 | op 8 ($\le 5$) | op 8: 1 |
| $[1, 8]$ | 1, 3, 7 | op 5 ($\le 4$), op 8 ($\le 5$) | op 5: 2, op 8: 2 |

The other calls have no add on the left or no query on the right. The answers are 1, 2 and 4. The pair (op 6, op 8) is counted in $[5, 8]$ and the pair (op 7, op 8) in $[7, 8]$, as the correctness argument says.

### Other examples

- **[Offline dynamic connectivity](/offline-dynamic-connectivity/).** The main example above, in $O(q \log q \log n)$ time.
- **Offline [dynamic bipartiteness](/dynamic-bipartiteness/).** The same walk with a union-find that stores the parity of the path to the root; an edge that closes an odd cycle marks the graph as non-bipartite until it is rolled back.
- **[Offline deletion](/offline-deletion/) in general.** Any structure with an add and an undo in $T(n)$ worst-case time, such as a set of linear equations kept in echelon form or a knapsack table that grows by one item, gets deletions in $O(T(n) \log q)$ per item.
- **Three-dimensional [dominance counting](/dominance-counting/).** For each point $p_i = (a_i, b_i, c_i)$, count the points with $a_j \le a_i$, $b_j \le b_i$ and $c_j \le c_i$. Sort by $a$ so that $a$ plays the part of time, run CDQ on the sorted order, and in CROSS sort by $b$ and keep a Fenwick tree over $c$: $O(n \log^2 n)$ time. Bentley's multidimensional divide and conquer (1980) solves dominance problems by the same kind of split on one coordinate. See also [offline orthogonal range counting](/offline-orthogonal-range-counting/).
- **Point updates and range queries, offline.** "Add $w$ at position $x$" and "sum over $[x_1, x_2]$" become dominance counting in (time, position), solved by CDQ in $O(n \log n)$ or $O(n \log^2 n)$ time without a two-dimensional structure.
- **Offline dynamic minimum spanning tree.** Eppstein (1994) splits the sequence of edge weight changes into blocks recursively and shrinks the graph for each block, by removing edges that no minimum spanning tree in the block can use and contracting edges that all of them use. The total time is $O(k \log n)$ for $k$ updates on $n$ vertices.

## Variations

- **Over the queries only.** The segment tree can be built over the query times alone, with each lifetime cut down to the queries that it covers. Then the tree has one leaf per query.
- **Divide and conquer without the explicit tree.** Recurse on $[lo, hi]$ with the list of items whose lifetime meets it; an item that covers the whole range is applied and dropped, the others go to the halves. This is the same walk without stored lists.
- **[Parallel binary search](/parallel-binary-search/).** A related offline method for queries whose answer is the first time (or the smallest value) at which a monotone condition becomes true. All binary searches advance together: in each of $O(\log q)$ rounds, replay the updates once in order and test each query at the middle of its current range. It does not need an undo, but it needs the condition to be monotone in time.
- **CDQ with a dependence between halves.** When the updates of the right half depend on answers in the left half, the order of lines C3, C4 and C5 must be left, cross, right. When the updates do not depend on any answer, the cross step can run before or after both recursive calls.
- **The name.** In the Chinese olympiad community the method is called CDQ divide and conquer, after the initials of Chen Danqi. Her 2008 national training team paper applies it to a dynamic program, the olympiad problem Cash: the decisions of the first half of the days update the values of the second half, and then the recursion continues on the second half.
- **Several dimensions.** CDQ can be nested: a CROSS step that is itself a dominance problem in one fewer dimension can be solved by CDQ again, at one more $\log n$ factor per dimension.
- **Online alternatives.** If the operations are not known in advance, [dynamic connectivity](/dynamic-connectivity/) needs a fully dynamic structure such as a [link-cut tree](/link-cut-tree/) for forests or the polylogarithmic amortized structures for general graphs. The offline methods here are simpler and have worst-case bounds.

## Pitfalls

- **Path compression with rollback.** The $O(\alpha(n))$ bound of union-find with path compression is amortized. After a rollback the structure returns to an older state, and the same costly find can be repeated many times, so the amortized bound fails. Use union by rank or by size alone, which gives $O(\log n)$ per find in the worst case.
- **Amortized structures in general.** Rollback breaks amortized bounds, as cp-algorithms says. ADD must have a worst-case bound, or the total cost is not $O(T(n) \log q)$.
- **Rollback of a union that did nothing.** An ADD that finds both ends in the same set changes nothing. The template rolls back to the stack size saved in line L10, so this case needs no record. Code that instead pops one record for each edge stored at the node must push an empty record for such a union; otherwise it pops a record that belongs to an ancestor.
- **Off-by-one lifetimes.** An edge removed at time $t$ is present up to $t - 1$, not $t$. An item never removed lives to $q$. If the same edge is added twice before it is removed, decide whether the graph is a multigraph and give each copy its own lifetime.
- **CDQ on contributions that interact.** CDQ needs the answer to be a combination of independent pair contributions. Updates that overwrite each other (such as "set position $x$ to $w$") must first be turned into additive ones ("add $w - w_{\text{old}}$").
- **Ties in CDQ.** In dominance counting with equal coordinates, the split by index can separate equal points and count a pair in one direction only. Merge equal points first, or break ties so that the order matches "$\le$" in every coordinate. In the cross sweep, process an update before a query with the same key when the query asks for "$\le$".
- **Online input.** Neither method works when a query must be answered before the next operation is read, for example when the next operation is encoded with the last answer.

## Exercises

1. Prove that INSERT-INTERVAL stores a range $[s, t] \subseteq [1, q]$ at no more than 2 nodes on each level of the segment tree, and that the ranges of the chosen nodes are disjoint with union $[s, t]$.
2. Extend the walk to report, at each query time, the number of connected components. Which fields must the undo record hold?
3. Show that union by rank without path compression keeps the height of each tree at most $\lfloor \log_2 n \rfloor$, and that this bound still holds after any sequence of unions and rollbacks.
4. Give a CDQ algorithm for this offline problem: a sequence of "insert the number $x$ into a multiset" and "how many numbers in the multiset are smaller than $y$" operations, $n$ in all. Prove an $O(n \log n)$ bound when the cross step uses a merge.
5. Solve the three-dimensional dominance problem for the points $(1, 2, 3)$, $(2, 1, 1)$, $(2, 3, 2)$, $(3, 3, 3)$ by hand with CDQ, and check each count against the definition.

## References
