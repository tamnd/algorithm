---
tag: AEEC82
kind: technique
slug: rollback-technique
name: Rollback (undo) technique
aliases:
- undo operations
- rollback data structures
area: graphs/dynamic-graphs
level: core
summary: Operations are undone in stack order, which lets offline dynamic algorithms revisit states cheaply.
prereqs: [stack, amortized-vs-worst-case]
see_also: [union-find-with-rollback, offline-dynamic-connectivity, divide-and-conquer-on-queries, offline-dynamic-graph, chronological-backtracking, dancing-links, persistent-data-structure, dsu-with-parity]
sources:
  - paper: "Heikki Mannila and Esko Ukkonen, The set union problem with backtracking, Proceedings of the 13th International Colloquium on Automata, Languages and Programming (ICALP 1986), Lecture Notes in Computer Science 226, 236 to 243"
    locator: the problem statement (undo of the most recent unions) and the solution without path compression
  - paper: "Jeffery Westbrook and Robert E. Tarjan, Amortized analysis of algorithms for set union with backtracking, SIAM Journal on Computing 18(1), 1 to 11 (1989)"
    locator: Section 1 (why path compression conflicts with backtracking) and the amortized bounds for compaction rules
  - url: https://arxiv.org/abs/cs/0011047
    title: Donald E. Knuth, Dancing links, in Millennial Perspectives in Computer Science (2000), arXiv cs/0011047
    locator: the opening section (a removed list element is restored by two writes, in the reverse order of removal)
  - url: https://cp-algorithms.com/data_structures/deleting_in_log_n.html
    title: cp-algorithms, Deleting from a data structure in O(T(n) log n)
    locator: the whole article (rollback of union-find inside a segment tree over time)
---

The rollback technique makes a data structure able to undo its most recent operations, in the reverse order in which they were done, by logging the old value of every field that an operation writes. To return to an earlier state, the structure pops the log and writes the old values back. The cost of an undo equals the cost of the writes that it reverses, so the method is exact and cheap, but it is safe only when every forward operation has a good *worst-case* bound. It is the engine of [offline dynamic connectivity](/offline-dynamic-connectivity/), of [backtracking](/chronological-backtracking/) search and of [dancing links](/dancing-links/).

## In plain words

Think of an editor with an undo button. Each time the program changes a value, it first writes down on a pile of notes what the value was before. To undo, it takes the top note and puts the old value back. Notes come off the pile in the reverse order in which they went on, so the program walks back through its own history, one step at a time, and lands on exactly the state it had before.

A bookmark is just the height of the pile. To go back to a bookmark, take notes off until the pile has that height again.

The catch is that undo must be cheap every time. A structure that sometimes does a large clean-up, and relies on the clean-up being rare, can be forced to redo it again and again.

## When it applies

- An algorithm visits states in a tree-shaped order: it moves forward by small changes and later returns to an earlier state, always the most recent one it has not left. Recursion and depth-first search have this shape.
- The changes come in last-in, first-out order. Undo in any other order needs a different tool.
- Each forward operation writes few fields, with a small worst-case bound. Then the log grows by that bound per operation, and an undo costs the same.
- Copying the whole state at each step is too expensive, and a fully [persistent](/persistent-data-structure/) structure is more than the problem needs.

Typical signals in a problem: "offline, with insertions and deletions"; "try a choice, recurse, then take it back"; "answer queries on many subsets that form a tree of nested sets".

## The template

The structure $D$ keeps its normal fields and one stack $H$ of records. Each record is a pair (a location, its old value).

```pseudo id=main
WRITE(D, a, x)                               ▷ every change of a field of D goes through here
L1  push (a, D[a]) on H                      ▷ save the old value first
L2  D[a] ← x

APPLY(D, op)                                 ▷ hole: a forward operation with a worst-case bound
L3  run op, using WRITE for each change of a field of D

CHECKPOINT(D)
L4  return |H|

ROLLBACK(D, t)                               ▷ precondition: t ≤ |H|
L5  while |H| > t do
L6      (a, x) ← pop H
L7      D[a] ← x                             ▷ a plain write, not WRITE
```

The holes are the forward operations in line L3 and the choice of which fields to log. Reads change nothing and leave no record. A structure may log a whole operation as one record instead of one record per field, if the record holds enough to reverse it; [union-find with rollback](/union-find-with-rollback/) logs one pair of roots per union.

**Why it is correct.** Let $S_j$ be the state of $D$ when $|H| = j$ for the last time on the way up, and let $t = $ CHECKPOINT$(D)$ in state $S_t$. Claim: after ROLLBACK$(D, t)$, the state is $S_t$. By induction on $|H| - t$. If it is 0, the loop of line L5 does not run. Otherwise the top record $(a, x)$ was pushed by line L1 in the step from $S_{|H|-1}$ to $S_{|H|}$, and that step changed only $D[a]$, from $x$ to its present value. Lines L6 and L7 write $x$ back and pop the record, so the state is $S_{|H|-1}$ and the hypothesis finishes the proof. The order matters: if one location was written twice, the later record holds the intermediate value and the earlier record holds the original; popping the later record first restores both correctly.

**Cost.** Line L1 adds $O(1)$ time to each write. ROLLBACK costs $O(1)$ per popped record. So a forward operation with worst-case cost $c$ and at most $w \le c$ writes costs $O(c)$ forward and $O(w)$ to undo. The log takes $O(w)$ space per operation that has not been undone.

**Why worst case.** Amortized bounds do not survive undo. An amortized analysis charges an expensive operation to cheap ones that came before it, through a [potential](/potential-method/) built up in the state. An undo restores that potential, so the same expensive operation can be repeated, each time at its full cost. Take an array with doubling, holding 8 items in capacity 8. A push copies 8 items and writes one, which is 9 writes. Undo it, and the old buffer of capacity 8 is back. Repeat the pair 100 times: the pushes do 900 writes, while the amortized bound of 3 writes per push promises 300. In general $k$ pairs cost $\Theta(kn)$, not $O(k)$.

## Classic examples

- **[Union-find with rollback](/union-find-with-rollback/).** Union by size without [path compression](/path-compression/): each union writes one parent pointer and one size, so each record has $O(1)$ size, and find takes $O(\log n)$ in the worst case. Mannila and Ukkonen (1986) posed this "set union with backtracking" problem. Path compression is left out because a find would write $\Theta(\log n)$ pointers that must all be logged, and because its bound is only amortized.
- **[Offline dynamic connectivity](/offline-dynamic-connectivity/).** Each edge is placed on the nodes of a segment tree over time. A depth-first walk of the tree applies the edges of a node on entry and rolls them back on exit, so each leaf sees exactly the edges alive at its time. With union-find with rollback the total time is $O(k \log k \log n)$ for $k$ operations; the general method is [divide and conquer on queries](/divide-and-conquer-on-queries/).
- **Offline dynamic bipartiteness.** The same walk with [union-find with parity](/dsu-with-parity/) answers whether the current graph is bipartite after each update; see [dynamic bipartiteness](/dynamic-bipartiteness/).
- **[Chronological backtracking](/chronological-backtracking/) and [DPLL](/dpll/).** A SAT solver keeps a trail of assigned variables. Backtracking to a decision level pops the trail to the size it had at that level and unassigns each popped variable. [CDCL](/cdcl/) solvers jump back many levels at once, which is still a rollback to a checkpoint.
- **[Dancing links](/dancing-links/).** Removing $x$ from a doubly linked list sets $x.left.right \leftarrow x.right$ and $x.right.left \leftarrow x.left$ but leaves the pointers of $x$ intact. Undoing the removals in reverse order restores each one with two writes and no log at all, because $x$ itself holds the old values.
- **[Mo's algorithm](/mo-algorithm/) with rollback.** When a window can grow cheaply but cannot shrink, each block of queries grows the window from a fixed start and rolls the left part back after each query.

## Variations

- **Operation-level records.** Log one record per operation (for example "root $a$ was linked below root $b$") instead of one record per field. The undo then runs the inverse operation. This saves memory when the inverse is easy to compute.
- **Snapshots by copying.** Save a full copy at each checkpoint. Undo is $O(1)$ to switch back, but each checkpoint costs the full size. Good when checkpoints are rare and the state is small.
- **Timestamped logging.** Log a field only on its first change after the latest checkpoint, by keeping in each field the checkpoint number of its last log. Constraint solvers use this to keep the log short when one field changes many times between checkpoints.
- **Persistence.** If the program needs old versions in arbitrary order, not only the latest, use a [persistent data structure](/persistent-data-structure/). A rollback structure is the special case in which only the newest version is ever changed and versions are left in stack order.
- **Undo in other orders.** If deletions do not come in stack order but the sequence is known in advance, [divide and conquer on queries](/divide-and-conquer-on-queries/) rearranges them into stack order at a cost of a logarithmic factor; see also [offline deletion](/offline-deletion/).

## Pitfalls

- **Amortized forward operations.** As shown above, an undo restores the potential, so an amortized bound can be broken by repeating "expensive operation, undo". Use only worst-case bounds, or prove an amortized bound for the specific pattern of operations and undos, as Westbrook and Tarjan (1989) did for some compaction rules in union-find.
- **A write that bypasses the log.** One field changed without line L1, such as a size, a counter of components or a cached answer, leaves the rollback silently wrong. Route every write through WRITE, including writes to global counters.
- **Rolling back with WRITE.** Line L7 must be a plain write. If the undo logs its own writes, the stack never shrinks.
- **No record for a no-op.** If some calls of an operation change nothing (a union of two elements already in one set), the caller may still count one undo per call. Either push an empty record, or make the caller undo by checkpoint height instead of by call count.
- **Undo out of order.** Undoing an operation that is not the most recent one restores a stale value. Rollback supports only stack order.

## Exercises

1. A union-find with rollback uses union by rank instead of union by size. Which fields must a record hold, and why can the rank of the new root change by at most one?
2. Show that a binary search tree without balancing does not break the rollback bounds, but a [splay tree](/splay-tree/) does: build a sequence of operations and undos on $n$ keys whose total cost is $\Theta(k n)$ for $k$ operations.
3. Design a stack of integers with push, pop, maximum and undo of the last push or pop, all in $O(1)$ worst-case time.

## References
