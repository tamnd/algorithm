---
tag: DQ5FW8
kind: data-structure
slug: blink-tree
name: B-link tree
aliases:
- Lehman-Yao B-link tree
area: data-structures/concurrent-structures
level: advanced
summary: B+-tree whose nodes have right-sibling links, so readers never need to lock while a split is in progress.
prereqs: [b-plus-tree, lock-coupling, linearizability]
see_also: [b-tree, readers-writer-lock, optimistic-concurrency-control, deadlock, mutex, concurrent-hash-table, lock-striping]
sources:
  - paper: doi:10.1145/319628.319663
    title: Philip L. Lehman and S. Bing Yao, Efficient locking for concurrent operations on B-trees, ACM Transactions on Database Systems 6(4), 1981
    locator: pages 650 to 670, the B-link tree, the search, insertion and move-right procedures, and the proofs of correctness and freedom from deadlock
  - paper: doi:10.1016/0022-0000(86)90021-8
    title: Yehoshua Sagiv, Concurrent operations on B*-trees with overtaking, Journal of Computer and System Sciences 33(2), 1986
    locator: pages 275 to 296, updates that hold fewer locks, and compression of nodes after deletions
  - paper: doi:10.1145/1806907.1806908
    title: Goetz Graefe, A survey of B-tree locking techniques, ACM Transactions on Database Systems 35(3), 2010
    locator: the sections on latches and locks, and on B-link trees
  - url: https://github.com/postgres/postgres/blob/master/src/backend/access/nbtree/README
    title: PostgreSQL source tree, the README of the nbtree access method
    locator: the opening sections, which describe the B-tree index as an implementation of Lehman and Yao's algorithm
---

A B-link tree is a [B+-tree](/b-plus-tree/) in which every node also stores a *high key*, the largest key it may hold, and a link to its right sibling on the same level. The links let a split happen in two steps that are each safe to see: first the node gives its upper half to a new right sibling and points to it, and only later the parent learns about the new node. A search that reaches a node after a split simply follows the right link when its key is above the high key. So searches take no locks at all, and an update locks only a few nodes, from the bottom up, never the whole path. Lehman and Yao introduced the structure in 1981, and many database systems build their indexes on it.

## In plain words

Think of a long row of filing drawers, each with a label that says which names it holds, such as "up to Miller". A clerk who must split a full drawer moves its second half into a new drawer, puts the new drawer to the right, and writes on the old drawer "up to Jones; for later names, look in the next drawer to the right". Only after that does the clerk update the index cards at the front desk.

A visitor who uses an old index card may come to the old drawer and not find "Smith". But the label says "up to Jones", so the visitor goes one drawer to the right and finds it there. Nobody has to stop the visitors while the clerk works. Clerks lock a drawer only while they change it.

## The abstract type

The B-link tree implements an ordered map, with the usual [B-tree](/b-tree/) operations:

- search$(k)$ returns the value of key $k$, or NIL.
- insert$(k, v)$ maps $k$ to $v$ and returns the old value of $k$, or NIL.
- delete$(k)$ removes $k$ and returns its value, or NIL.

Each operation is [linearizable](/linearizability/): it seems to happen at one instant between its call and its return. Range scans follow the right links of the leaf level, as in a B+-tree.

## Representation

- Each node is a page that is read and written as one unit. It has a level (0 for leaves), a sorted list of keys, a high key $high$ ($+\infty$ for the rightmost node of a level), and a right link $link$ (NIL for the rightmost node).
- A leaf holds pairs (key, value). An internal node holds pairs $(m_i, c_i)$: child $c_i$ is the subtree for keys above $m_{i-1}$ and at most $m_i$, and the last separator equals the node's high key.
- Each node has a lock, which only updates use. A node is changed only by the holder of its lock, except a new node before anyone can reach it.
- An anchor holds the root and the height of the tree.
- Every node $n$ covers a key range $(low(n), high(n)]$. The low bound is fixed when the node is created; a split only lowers the high key. On each level, the right links run through the nodes in key order, and their ranges cover all keys without overlap.

A node can be read while it is locked. All that is needed is that a reader sees either the whole page before a write or the whole page after it, which is true of a disk page and is easy to get in memory by writing a fresh copy of the page and switching a pointer.

## Operations

```pseudo id=main
SEARCH(T, k)
L1  n ← T.root
L2  A ← READ(n)
L3  while A is not a leaf or k > A.high do
L4      if k > A.high then n ← A.link else n ← the child c_i of A with m_{i−1} < k ≤ m_i
L5      A ← READ(n)
L6  return the value of k in A, or NIL

INSERT(T, k, v)
L7  descend as in SEARCH to the leaf n for k; push the last node visited at each level on a stack
L8  LOCK(n); A ← READ(n); MOVE-RIGHT(k)
L9  if k is in A then set its value to v; WRITE(n, A); UNLOCK(n); return the old value
L10 (y, w) ← (k, v)
L11 loop
L12     insert the entry (y, w) into A
L13     if A has at most C entries then WRITE(n, A); UNLOCK(n); return NIL
L14     split A into a left half A′ and a right half B; u ← a new node; WRITE(u, B); WRITE(n, A′)
            ▷ B gets A's old high key and link; A′ gets the high key max(A′) and the link u
L15     y ← A′.high; w ← u; old ← n
L16     n ← POP(stack), or, if the stack is empty: if old is the root, make a new root with the entries (y, old) and (+∞, u), UNLOCK(old), return NIL; otherwise find the node one level up by a descent for y
L17     LOCK(n); A ← READ(n); MOVE-RIGHT(y); UNLOCK(old)

MOVE-RIGHT(key)                                 ▷ n is locked and A = READ(n)
L18 while key > A.high do LOCK(A.link); UNLOCK(n); n ← A.link; A ← READ(n)

DELETE(T, k)
L19 descend to the leaf n for k; LOCK(n); A ← READ(n); MOVE-RIGHT(k)
L20 remove k from A if it is there; WRITE(n, A); UNLOCK(n); return its value, or NIL
```

**Search.** At each node the search either goes right, if its key is above the high key (a split moved the key away), or goes down. It never locks and never waits.

**Insert.** The insert walks down without locks, keeping a stack of the nodes where it went down. Only at the leaf does it take a lock, and then it may have to move right, because the leaf may have split since the parent was read. Line L18 locks the right sibling before it releases the current node, so no split can slip in between. A full node splits at line L14: the new right node is written first, while nobody can reach it, and the old node is written second, with its new high key and its link to the new node. From that moment every key is reachable again. The insert then adds the separator $y$ and the pointer $u$ to the parent (lines L15 to L17), locking the parent before it unlocks the child. The new entry is placed by key: the parent entry $(m, c)$ with the smallest $m \ge y$ becomes $(y, c)$ and $(m, u)$.

**Root.** When the root splits, the splitter makes a new root above the two halves. A thread that splits another node of the top level before the new root exists waits until it does.

**Delete.** Lehman and Yao let leaves become underfull, and so does this delete: it only removes the key. Nodes never merge.

## Example

Capacity $C = 3$. The tree holds 10, 20, 30, 40 and 50, in leaves $L = [10, 20]$ with high key 20 and $R = [30, 40, 50]$ with high key $+\infty$, under the root $[(20, L), (+\infty, R)]$.

| step | thread | what it does | result |
|---|---|---|---|
| 1 | search(50) | L1, L2: reads the root; 50 is above 20, so the next node is $R$ | |
| 2 | insert(45) | L7, L8: descends to $R$ and locks it; L12: $[30, 40, 45, 50]$ is too full | |
| 3 | insert(45) | L14: writes the new node $u = [45, 50]$, high $+\infty$, no link | |
| 4 | insert(45) | L14: writes $R = [30, 40]$, high 40, link $u$ | 45 is in the map |
| 5 | insert(45) | L16, L17: locks the root, unlocks $R$; adds the separator 40 | root $[(20, L), (40, R), (+\infty, u)]$ |
| 6 | search(50) | L5: reads $R$; 50 is above its high key 40, so L4 follows the link | |
| 7 | search(50) | L5: reads $u$, a leaf with 50 in its range | returns the value of 50 |

The search read the root before the split, so it went to $R$, which no longer holds 50. Without the high key and the link it would have returned NIL. With them, it moves right and finds 50. It never waited for the insert, even though $R$ and then the root were locked.

## Correctness

The proof keeps one invariant: on each level, the nodes in the order of the right links cover the key space in consecutive ranges $(low, high]$, the low bound of each node never changes, and each separator in an internal node is the low bound of the child to its right. A split keeps this, because the write of the new node changes nothing that anyone can reach, and the single write of the old node replaces the range $(low, high]$ by $(low, y]$ and $(y, high]$ in one step. From the invariant, a search that has reached a node with $k$ above its low bound can only go right or down to another such node, so the leaf it ends at covers $k$ at the moment it reads it. That read is the linearization point of the search, and each update is linearized at its write of the leaf page, or at the read of the locked leaf if it changes nothing. Updates take locks in an order that only goes up a level or to the right on one level, by the fixed low bound, so there is no deadlock; searches take no locks. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| quantity | value |
|---|---|
| page reads of a search, no contention | $O(\log_C n)$, one per level |
| locks held by an update at one time | at most 3 (the child, the parent and its right sibling) |
| locks taken by an update without splits | 1, plus 1 for each move right |
| extra reads due to concurrent splits | one per split that the operation must move right past |
| space | $O(n)$; deleted keys leave underfull nodes |

The cost of concurrency is small: a search may follow some extra right links, one for each split that happened between the read of a parent and the read of its child, and an update locks the nodes it changes and no others. In [lock coupling](/lock-coupling/), by contrast, every operation locks each node on its path, and every operation passes the root, so the root lock becomes a bottleneck.

## Variants

- **Sagiv's B-link tree.** Sagiv refines the scheme so that updates hold fewer locks at a time, and adds a compression process that merges underfull nodes in the background while other operations continue.
- **Latches and locks.** Database systems separate short-term *latches* on pages, which protect the structure, from long-term transaction locks on keys. Graefe's survey describes how B-link trees fit into this.
- **Optimistic latch coupling.** In-memory B-trees often let readers check a version number on each node instead of taking a latch, and retry if the node changed: an [optimistic](/optimistic-concurrency-control/) form of the same idea.
- **Lock-free B-link trees.** Later designs replace the node locks by compare-and-swap on node pointers, so that no thread ever waits.

## When to use it

Use a B-link tree for an index on disk or in memory that many threads search and update at the same time, especially when searches outnumber updates. PostgreSQL's B-tree indexes are an implementation of the Lehman and Yao algorithm. For a tree that only one thread changes at a time, or with very few concurrent users, a plain B+-tree with one [readers-writer lock](/readers-writer-lock/) is simpler.

## Pitfalls

- **Writing the old node first.** If the old node gets its new high key before the new node exists on disk or in memory, the link points to garbage. Write the new node first.
- **Unlocking before the next lock.** Line L18 must lock the right sibling before it unlocks the current node, and line L17 must lock the parent before it unlocks the child; otherwise a concurrent split can move the key range away in between.
- **Locking in the wrong direction.** Updates must never wait for a lock to the left or below a lock they hold. Locking left to right and bottom up is what rules out deadlock.
- **Deleting nodes.** A search may hold a pointer to any node it read. A node cannot simply be freed or merged away; deletion of nodes needs a separate scheme, such as Sagiv's, plus safe reclamation of memory.
- **Forgetting the move right after the descent.** The leaf found by a lock-free descent may have split. Always move right after taking the lock, at every level.

## Implementations

The Python module keeps each node as an immutable page that is replaced in one step, with a lock for updates, and models every page read, page write and lock attempt as one step of a generator. The tests replay the example step by step, show that searches finish while every node is locked, compare thousands of sequential operations with a dictionary, check random interleavings of three threads, with splits at every level and races at the root, against a sequential map with a linearizability search, check the invariant of the tree after each run, and run the plain methods under real threads.

## History

Bayer and McCreight's B-tree of 1972 became the standard index of databases, and the first concurrent versions, by Bayer and Schkolnick in 1977 and others, locked the path from the root, which made the root a bottleneck. Lehman and Yao added the high key and the right link in 1981, proved that searches need no locks, and showed that updates need only a small number of locks at a time, without deadlock. Sagiv in 1986 reduced the locks further and handled deletion. The design became the basis of B-tree indexes in systems such as PostgreSQL.

## References
