---
tag: ANER1G
kind: technique
slug: global-rebuilding
name: Global rebuilding
aliases:
- Overmars global rebuilding
area: foundations/amortized-analysis
level: advanced
summary: Converts amortized bounds to worst-case bounds by rebuilding the structure incrementally in the background.
prereqs: [amortized-cost, array-doubling, amortized-vs-worst-case]
see_also: [dynamic-table-contraction, lazy-rebuilding, real-time-queue, decomposable-searching-problem, lazy-deletion, scapegoat-tree, worst-case-update-time, kd-tree]
sources:
  - book: isbn:9783540123309
    title: Mark H. Overmars, The Design of Dynamic Data Structures, Lecture Notes in Computer Science 156, Springer (1983)
    locator: Chapter "Global rebuilding", pp. 67 to 77 (weak deletions, periodic rebuilding, and rebuilding in the background for worst-case bounds); the chapters on partial and local rebuilding for comparison
  - paper: doi:10.1016/0020-0190(81)90093-4
    title: Mark H. Overmars and Jan van Leeuwen, Worst-case optimal insertion and deletion methods for decomposable searching problems, Information Processing Letters 12(4), 1981
    locator: pp. 168 to 173
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press (1998)
    locator: Chapter 8, Lazy Rebuilding (batched rebuilding, global rebuilding, lazy rebuilding)
  - paper: doi:10.1016/0020-0190(81)90030-2
    title: Robert Hood and Robert Melville, Real-time queue operations in pure LISP, Information Processing Letters 13(2), 1981
    locator: pp. 50 to 54
---

Global rebuilding is a technique for dynamic data structures that keeps a structure efficient under updates by building a fresh copy of the whole structure from its current set of items. In its plain form, the structure is rebuilt from scratch after a constant fraction of updates, which gives [amortized](/amortized-cost/) bounds. In the form of Overmars (1983), the new copy is built in the background, a few steps at each update, while the old copy answers the queries; the updates made in the meantime are kept in a buffer and replayed on the new copy before the switch. This form turns the amortized bound into a [worst-case](/worst-case-update-time/) bound of the same order, and is the standard tool of de-amortization.

## In plain words

Some data structures get worse as you change them. Deleted items leave holes, and the shape drifts away from the ideal one. A simple fix is to throw the structure away now and then and build a new one from the items that are left. If you do this after a fixed fraction of changes, the cost of the rebuild, shared over those changes, is small. But the change that starts the rebuild is very slow. Global rebuilding removes that slow step. It starts to build the new copy early and does a small part of the work at each change. The old copy keeps working until the new one is ready. Changes made during the build are written down and copied to the new structure, a few at a time. Then the new copy takes over.

## When it applies

- The structure can be built from a list of $n$ items in time $P(n)$, for example $O(n)$ or $O(n \log n)$.
- It supports *weak updates*: an insertion or a deletion that keeps the answers correct but may let the quality decay. Overmars calls a deletion weak when the query and update times stay within a constant factor of their bounds as long as at most a constant fraction of the items have been deleted since the last build. Marking an item as deleted, as in [lazy deletion](/lazy-deletion/), is the typical weak deletion.
- You need a bound on each operation, not on the total: real-time systems, interactive programs, or a structure that is a part of a bigger worst-case bound. Or the structure is used [persistently](/persistent-data-structure/), where amortized bounds can fail.
- The build algorithm can be paused after a fixed number of steps and resumed, and there is memory for two copies.

## The template

**Assumptions.** A structure $D$ for a set $S$, with three properties.

1. BUILD on a list of $b$ items takes at most $P(b)$ steps, and $P$ is non-decreasing with polynomial growth: $P(2x) \le K\,P(x)$ for a constant $K$, and $P(x) \ge x$.
2. Each weak update takes at most $U$ steps (where $U$ may depend on $b$).
3. A structure built on $b$ items keeps its query and update bounds while at most $\alpha b$ weak updates have been applied to it since its build, for a constant $0 < \alpha \le 1$.

### The amortized form

Rebuild from scratch after each $L = \max(1, \lfloor \alpha b / 2 \rfloor)$ updates, where $b$ is the size at the last build.

**Theorem 1.** For $\alpha \le 1$, each update has amortized cost $O(U + P(n)/(\alpha n))$, where $n$ is the current size, and $D$ always stays within property 3.

*Proof.* Between two rebuilds, $L \le \alpha b$ updates are applied, so property 3 holds. The rebuild works on at most $b + L \le 2b$ items and costs at most $P(2b) \le K\,P(b)$. Charge it to the $L$ updates of the period. If $\alpha b \ge 2$, then $L \ge \alpha b / 4$ and each update pays at most $4K\,P(b)/(\alpha b)$. During the period the size $n$ is between $b - L \ge b/2$ and $2b$, so $P(b)/b \le$ a constant times $P(n)/n$ by the growth condition, and the charge is $O(P(n)/(\alpha n))$. If $\alpha b < 2$, then $b < 2/\alpha$ is a constant and each rebuild takes $O(1)$ time. $\square$

The update that triggers a rebuild still takes $\Theta(P(n))$ time. This is the step that the background form removes.

### The worst-case form (Overmars)

```pseudo id=main
EPOCH(D)                                ▷ D is current and up to date; S has n₀ items
L1  h ← max(1, ⌊α·n₀ / 8⌋)
L2  start SNAPSHOT-AND-BUILD(D′) on the set S as it is now
L3  B ← empty queue                      ▷ buffer of updates for D′
L4  for each of the next 2h updates u do
L5      apply u to D                     ▷ queries keep using D
L6      append u to B
L7      if this is one of the first h updates of the epoch then
L8          run ⌈(P(n₀) + c·n₀) / h⌉ steps of SNAPSHOT-AND-BUILD    ▷ D′ is ready after h updates
L9      else
L10         remove 2 updates from the front of B and apply them to D′
L11 switch: D ← D′, discard the old D, start the next EPOCH(D)
```

The work of the snapshot and the build is $P(n_0) + c\,n_0$ steps for a constant $c$, so line L8 finishes it in the first $h$ updates.

**Theorem 2.** Let $n_0 \ge 8/\alpha$. With EPOCH, each update takes $O(U + P(n)/(\alpha n))$ steps in the worst case, queries are answered by a structure that satisfies property 3, and the memory is at most about twice that of one structure plus the buffer.

*Proof.* *The buffer empties in time.* After the first $h$ updates, $B$ holds $h$ updates and the build of $D'$ is complete. In the second half, each update adds 1 to $B$ and removes 2, so after $j$ of them $B$ holds $h - j$; before each removal it holds $h - j + 2 \ge 2$ items, so line L10 never runs out. After $2h$ updates $B$ is empty. $D'$ was built on $S$ as it was at line L2 and has since received all $2h$ updates of the epoch in order, so at line L11 it represents the current set.

*Property 3 holds for each structure.* $D'$ is built on $n_0$ items. It receives $2h \le \alpha n_0/4$ updates during the epoch of $D$. In its own epoch it receives $2h'$ more, with $h' \le \alpha n_1/8$, where $n_1 \le n_0 + 2h \le \tfrac54 n_0$ is the size at its switch. So the total is at most $\alpha n_0 / 4 + \alpha \cdot \tfrac54 n_0 / 4 = \tfrac{9}{16} \alpha n_0 \le \alpha n_0$. The same count for $D$ (with the roles shifted by one epoch) shows that $D$ is within its bound while it answers queries.

*Work per update.* In the first half: one weak update on $D$ and $\lceil (P(n_0) + c n_0)/h \rceil$ build steps. Since $\alpha n_0 \ge 8$, $h \ge \alpha n_0 / 16$, so this is $O(U + P(n_0)/(\alpha n_0))$. In the second half: three weak updates, $O(U)$. During the epoch $n$ stays between $\tfrac34 n_0$ and $\tfrac54 n_0$, so by the growth condition $P(n_0)/n_0 = O(P(n)/n)$. $\square$

The constants $8$ and $2$ are one valid choice; Overmars states the result with general constants. When $n_0 < 8/\alpha$ the set has constant size and each operation can rebuild directly in $O(1)$ time.

**The snapshot.** Line L2 must give the build the set $S$ as it was at the start of the epoch, while the updates of lines L5 and L10 change $D$. One way: keep beside $D$ a linked list of item records, each with the time of its insertion and of its deletion. A deletion only writes its time; an insertion appends a record at the end. At line L2, remember the time $t_0$ and the last record. The snapshot walks the list up to that record, a few records per step, and passes to BUILD each record that was alive at $t_0$ (inserted before $t_0$, deleted after it or not at all). It unlinks the records of items deleted before $t_0$ as it passes them. The list then has $O(n)$ records at all times, and the walk is part of the $c\,n_0$ steps.

## Classic examples

- **Incremental array doubling.** When an [array](/array-doubling/) of capacity $c$ is full, allocate capacity $2c$; at each later append, write the new item and move 2 old items. All old items have moved after $\lceil c/2 \rceil$ appends, while the new array still has room. Each append does at most 3 units of work, and for $n = 1000$ appends the total is 2023, the same as plain doubling, which has one append of cost 513. This is global rebuilding with BUILD = copy and $P(n) = n$.
- **Incremental resizing of a hash table.** A [hash table](/hash-table/) keeps the old and the new table during a resize, moves a constant number of keys at each operation, and looks up in both tables. The same scheme handles [contraction](/dynamic-table-contraction/).
- **Lazy deletion in a perfectly balanced search tree.** Take a tree that supports searches and deletions only. Mark deleted keys and keep the shape. A tree built on $b$ keys has height $\lfloor \lg b \rfloor$, and while at most half of the keys are marked, $b \le 2n$, so the height is still $O(\log n)$. Rebuild from the unmarked keys, which an in-order walk gives in sorted order, in $O(n)$ steps. The background form gives $O(\log n)$ worst-case deletions. The same applies to a [k-d tree](/kd-tree/), which has no simple rebalancing.
- **Decomposable searching problems.** Overmars and van Leeuwen (1981) use background rebuilding to turn the amortized bounds of the logarithmic method for [decomposable searching problems](/decomposable-searching-problem/) into worst-case bounds for insertions and deletions.
- **The [real-time queue](/real-time-queue/).** Hood and Melville (1981) keep a functional queue with $O(1)$ worst-case operations by reversing the rear list step by step, a few steps per operation, before the front list runs out. Okasaki presents it as global rebuilding, and uses [lazy rebuilding](/lazy-rebuilding/) for a simpler variant.

## Variations

- **Batched rebuilding.** The amortized form above: rebuild after a fraction of updates. Okasaki calls it batched rebuilding. It is enough when only the total time matters.
- **Partial rebuilding.** Rebuild only the subtree that is out of balance, as in the [scapegoat tree](/scapegoat-tree/) and in the [weight-balanced tree](/weight-balanced-tree/). Overmars treats it in its own chapter. It gives amortized bounds, and the cost of a rebuild is proportional to the size of the subtree.
- **Lazy rebuilding.** In a lazy functional language, the rebuild is a suspended computation that later operations force step by step; Okasaki's [lazy rebuilding](/lazy-rebuilding/) gives amortized bounds that hold under persistence with simpler code.
- **Several structures in parallel.** The logarithmic method keeps one structure per 1 bit of $n$ (a [binary counter](/binary-counter-increment/)) and rebuilds each block in the background.

## Pitfalls

- **A buffer that grows.** The replay rate must exceed the arrival rate. With 1 replay for each new update, the buffer never shrinks and $D'$ never catches up. Line L10 uses 2.
- **A rebuild that starts too late.** If the background build starts only when $D$ has reached its limit of $\alpha b$ updates, $D$ is past its bound during the build. Start early enough that the build and the catch-up end within the limit, as in the count of Theorem 2.
- **The snapshot.** Reading the set from $D$ while $D$ changes can give a set that never existed, and the replay then applies an update twice or to an item that is not there. Use a time-stamped list or a frozen copy.
- **A build that cannot pause.** A recursive build with deep calls must be rewritten as an explicit state machine, or run as a coroutine, so that it can stop after a fixed number of steps.
- **Allocation.** Allocating the new structure in one step may cost $\Theta(n)$ if the memory is zeroed. Allocate in pieces, or count it in the background work.
- **Memory.** Two copies plus the buffer exist during each epoch. If memory is tight, this may cost more than the latency that it saves.
- **Amortized bounds hidden in the parts.** The weak updates must have worst-case bounds themselves. If a weak update has only an amortized bound, the result is amortized too.

## Exercises

1. Apply Theorem 1 to a binary search tree with lazy deletion, rebuilt when half of its keys are marked, and give the amortized cost of a deletion.
2. Design the incremental version of [dynamic table contraction](/dynamic-table-contraction/) and show that each operation moves $O(1)$ items in the worst case.
3. In EPOCH, replace the 2 of line L10 by 3 and the split of the epoch by $h$ build updates and $\lceil h/2 \rceil$ catch-up updates. Redo the count of property 3.

## References
