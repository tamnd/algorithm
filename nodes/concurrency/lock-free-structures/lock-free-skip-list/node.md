---
tag: BMT1MG
kind: data-structure
slug: lock-free-skip-list
name: Lock-free skip list
aliases:
- Fraser skip list
- Herlihy-Shavit lock-free skip list
- lock-free skip list
- LockFreeSkipList
area: concurrency/lock-free-structures
level: advanced
summary: Concurrent ordered dictionary built from a skip list whose levels are lock-free linked lists.
implements: [ordered-set]
complexity:
  vars: {n: "the number of keys", L: "the number of levels, about log2 n", R: "the size of the key range when keys are integers"}
  space: {extra: Θ(n + L)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [skip-list, harris-linked-list, linearizability, lock-freedom]
see_also: [skip-list, harris-linked-list, logical-deletion, split-ordered-list, lock-free-priority-queue, non-blocking-bst, epoch-based-reclamation, spraylist]
sources:
  - url: "https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-579.html"
    title: Keir Fraser, Practical lock-freedom, PhD thesis, University of Cambridge, 2003, published as Computer Laboratory Technical Report UCAM-CL-TR-579, 2004
    locator: the chapter on lock-free search structures, the skip list built from single-word CAS with a mark bit in each level's pointer, and the chapter on epoch-based memory reclamation
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: the chapter on skiplists and balanced search, the section on a lock-free concurrent skiplist (the LockFreeSkipList class, its find, add, remove and wait-free contains, and the linearization points)
  - paper: doi:10.1007/978-3-540-72951-8_11
    title: Maurice Herlihy, Yossi Lev, Victor Luchangco and Nir Shavit, A simple optimistic skiplist algorithm, SIROCCO 2007, LNCS 4474, pages 124 to 138
    locator: the lock-based lazy skip list with optimistic search and short validation, the lock-based companion of the lock-free list
  - paper: doi:10.1145/78973.78977
    title: William Pugh, Skip lists, a probabilistic alternative to balanced trees, Communications of the ACM 33(6), 1990, pages 668 to 676
    locator: the sequential skip list, random levels and the expected logarithmic search cost
---

A lock-free skip list is a [skip list](/skip-list/) in which every level is a lock-free sorted list in the style of the [Harris list](/harris-linked-list/): each level of a node has its own next pointer with a mark bit in the same word, and a node is deleted by [logical deletion](/logical-deletion/) before it is unlinked. The bottom level is the set; the upper levels are only shortcuts, so they may be out of date for a moment without harm. The design is due to Fraser (2003, 2004); the version on this page is the LockFreeSkipList of Herlihy and Shavit's textbook. Add, remove and contains are [linearizable](/linearizability/); add and remove are [lock-free](/lock-freedom/), and contains never writes and is wait-free when keys come from a finite range. It differs from the plain [skip list](/skip-list/) only in how it changes the levels: one CAS at a time, in an order that keeps the bottom level correct after every step.

## In plain words

Think of a subway with a local line and express lines above it. The local line decides which stations exist. The express lines only help you get there faster.

To open a station, you first connect it to the local line. From that moment it exists. Then you connect it to the express lines one at a time; if a rider takes an older express route meanwhile, the local line still gets the rider there.

To close a station, you first put a "closed" sign on each of its express platforms, from the top down, and last on its local platform. The person whose sign closes the local platform has closed the station. Anyone who passes a closed platform may unhook it from the line. Riders who only look never touch anything: they step past closed platforms.

## The abstract type

The list implements an [ordered set](/ordered-set/); the code keeps only the keys.

- add(k): add $k$; return true if $k$ was not present, false otherwise.
- remove(k): remove $k$; return true if $k$ was present, false otherwise.
- contains(k): return whether $k$ is present.

The ordered queries (min, successor, a range scan) can walk the bottom level, but such a walk is not an atomic snapshot of the set; this page covers the three operations above.

## Representation

### Model and notation

We use the asynchronous shared memory model with processes that may crash, atomic read, write and [CAS](/compare-and-swap/) on single words, and [sequential consistency](/sequential-consistency/). A word holds a pointer and a mark bit together, so one CAS can test and change both. Nodes are not freed in the code (the model has a garbage collector); see the section on memory reclamation.

| Symbol | Meaning |
|---|---|
| $L$ | the number of levels, numbered $0$ (bottom) to $L - 1$ |
| $x.\mathit{top}$ | the top level of node $x$, fixed when $x$ is made |
| $x.\mathit{next}[i]$ | the word of $x$ at level $i \le x.\mathit{top}$: a pair (pointer, mark) |
| marked at level $i$ | the mark bit of $x.\mathit{next}[i]$ is 1 |
| head, tail | sentinels with keys $-\infty$ and $+\infty$ and top level $L - 1$ |
| present | $x$ is reachable at level 0 and not marked at level 0 |
| $n$ | the number of keys in the set |

### Fields

- A node has a key, a top level and $x.\mathit{top} + 1$ marked next words. The key and the top level never change.
- head and tail. At the start, head points to tail at every level.

**Invariant.** (1) Every pointer stored at level $i$ goes from a node to a node with a strictly larger key. (2) A word that is marked never changes again. (3) A node that is not marked at level 0 and was linked at level 0 is reachable at level 0. (4) At level 0, at most one node with a given key is unmarked and reachable. The abstract set is the set of keys of the present nodes.

The upper levels have weaker rules: a node can be reachable at level $i > 0$ while it is not yet linked at a lower level, or after it was removed at level 0 (a late link, shown below). Searches only use the upper levels to choose where to start on the level below, so this is safe.

## Operations

```pseudo id=main
FIND(k)                                       ▷ returns (found, preds, succs); unlinks marked nodes
L1  retry: pred ← head
L2  for i ← L − 1 down to 0 do
L3      curr ← pointer of pred.next[i]
        loop
L4          (succ, m) ← curr.next[i]
L5          while m do                        ▷ curr is marked at level i: unlink it
L6              if not CAS(pred.next[i], (curr, 0), (succ, 0)) then goto retry
L7              curr ← succ; (succ, m) ← curr.next[i]
L8          if curr.key < k then pred ← curr; curr ← succ else exit loop
L9      preds[i] ← pred; succs[i] ← curr
L10 return (succs[0].key = k, preds, succs)

ADD(k)                                        ▷ t is the random top level of the new node
L11 loop (found, preds, succs) ← FIND(k)
L12     if found then return false
L13     node ← new node with key k, top t, node.next[i] = (succs[i], 0) for i ≤ t
L14     if CAS(preds[0].next[0], (succs[0], 0), (node, 0)) then exit loop
L15 for i ← 1 to t do
        loop
L16         (s, m) ← node.next[i]; if m then return true     ▷ node is being removed
            if s ≠ succs[i] and not CAS(node.next[i], (s, 0), (succs[i], 0)) then continue
L17         if CAS(preds[i].next[i], (succs[i], 0), (node, 0)) then exit loop
L18         (found, preds, succs) ← FIND(k); if not found or succs[0] ≠ node then return true
L19 return true

REMOVE(k)
L20 (found, preds, succs) ← FIND(k); node ← succs[0]
L21 if not found then return false
L22 for i ← node.top down to 1 do
L23     repeat (succ, m) ← node.next[i]; if not m then CAS(node.next[i], (succ, 0), (succ, 1)) until m
L24 (succ, m) ← node.next[0]
    loop
L25     if CAS(node.next[0], (succ, 0), (succ, 1)) then
L26         FIND(k); return true              ▷ the winner unlinks node at every level
        (succ, m) ← node.next[0]
L27     if m then return false                ▷ another remove marked level 0 first

CONTAINS(k)                                   ▷ reads only
L28 pred ← head; for i ← L − 1 down to 0 do curr ← pointer of pred.next[i]; loop
L29     (succ, m) ← curr.next[i]; while m do curr ← succ; (succ, m) ← curr.next[i]
        if curr.key < k then pred ← curr; curr ← succ else exit loop
L30 return curr.key = k
```

**Linearization points.** A successful add at its CAS at L14, which makes the node present. A successful remove at its CAS at L25, which marks level 0. An add that returns false at the read in FIND that saw the node with key $k$ unmarked at level 0. A remove that returns false either at the point in FIND where no node with key $k$ was present, or, at L27, just after the other remove's mark. A contains that returns true at the read of the unmarked level 0 word of the node it returns; one that returns false at its start if no node with key $k$ was present then, and otherwise just after that node was marked (the proof shows that it was marked during the call).

**Why level 0 decides a remove.** Several removes of one key can mark the upper levels; each upper mark succeeds for one of them, and they help each other finish. Only the CAS at L25 has a single winner per node, since a marked word never changes. If a remove also returned true when its own CAS marked the top level, two removes of one key could both return true. The test `test_deciding_at_the_top_level_lets_two_removes_win` finds this run with the explorer and replays it.

**Why add resets its own next.** A failed CAS at L17 makes add call FIND again, and the new successor at level $i$ can differ from the one stored in the node. Before the next try, add sets node.next[i] to the new successor with a CAS, so that it never links the node in front of a stale successor; that CAS fails if a remove has marked the word, and then add stops building the node. Fraser's design does this reset. The textbook's code sets the field once, when the node is made.

**A late link.** An add can pass L16, then a remove can mark and unlink the node at every level, and then the add's CAS at L17 can still succeed: the removed node is linked again at level $i$. It is marked there, so searches step over it and the next FIND that passes unlinks it. The set is not affected. The test `test_a_late_add_can_link_a_removed_node` shows the run.

### Memory reclamation

Because of late links, a node is not garbage when its remover returns, which is where most attempts to free skip list nodes go wrong: a node freed after it is unlinked at level 0 can be linked again at an upper level and then read by a later search. A safe rule in the model of this page is to retire the node only when both its add and its winning remove have returned, and after one more FIND(k) that starts after both, which unlinks every marked node with key $k$ at every level, since a search for $k$ passes the place of $k$ at each level. This rule is our own observation; check it before you rely on it. Fraser's thesis frees nodes with [epoch-based reclamation](/epoch-based-reclamation/), which it introduced; [hazard pointers](/hazard-pointers/) also work but need about $2L$ hazards per process, one for each predecessor and successor. Without any scheme, a search can follow a pointer into a freed node, and a CAS that expects (curr, 0) can succeed on a reused address (the [ABA problem](/aba-problem/)).

### Weak memory

The CAS at L14 must be a release, so that a process that reads the pointer to the new node also sees its key, its top level and its next words; reads of next words must be acquire loads, or loads with a data dependency on the pointer, which most hardware orders. The marks and the unlink CAS steps are read-modify-writes on one word and need no extra fence on most hardware.

## Example

Take $L = 2$ and the set $\{1, 3\}$, with node 1 and node 3 at top level 1. Level 1 is head, 1, 3, tail and level 0 is head, 1, 3, tail.

Process $p$ runs remove(1) and process $q$ runs add(2) with top level 0.

1. $p$: FIND(1) returns preds = (head, head) and succs = (node 1, node 1). $p$ marks node 1 at level 1 (L23).
2. $q$: FIND(2) at level 1 reads node 1's level 1 word, sees the mark, and unlinks node 1 at level 1 (L6): head now points to 3 at level 1. At level 0 it moves past node 1, which is not yet marked there, and returns preds[0] = node 1, succs[0] = node 3.
3. $q$: CAS(node 1.next[0], (3, 0), (2, 0)) succeeds (L14). Now level 0 is head, 1, 2, 3. The set is $\{1, 2, 3\}$; this is the linearization point of add(2).
4. $p$: CAS(node 1.next[0], (3, 0), (3, 1)) fails, because the word is now (2, 0). $p$ reads it again and retries; CAS(node 1.next[0], (2, 0), (2, 1)) succeeds (L25). The set is $\{2, 3\}$; this is the linearization point of remove(1).
5. $p$: FIND(1) unlinks node 1 at level 0. Level 0 is head, 2, 3, tail.

If $q$'s CAS in step 3 had come after $p$'s mark, it would have failed, because a marked word never matches (3, 0); $q$ would have searched again and linked node 2 after head. That is why the mark must share the word with the pointer.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) is a sketch. Its parts are as follows.

- *Safety.* Every pointer that is ever written at level $i$ goes to a larger key, because each CAS writes either the successor that FIND saw after the predecessor, or the successor of a node that was just unlinked. So each level is sorted, from any node, reachable or not. Marked words never change, because every CAS expects an unmarked old value. At level 0, add links a node only between two adjacent unmarked nodes with keys below and above $k$, so no two present nodes share a key. With the linearization points above, the set of present keys changes exactly at the points of successful adds and removes, so each history is linearizable to a set. The hard case is a contains that returns false while a node with key $k$ was present when it started: by the sorted pointers, contains would reach that node at level 0 unless it was marked, so it was marked during the call. This is proved in the textbook; the proof file gives the outline.
- *Progress.* A CAS fails only if another process changed the word with a successful CAS. Each add links its node at most once per level, each node is marked at most once per level, and each unlink removes a link, so if no operation finished, only finitely many CAS steps could succeed, and after them every search would finish. So the list is lock-free. Contains moves to a strictly larger key at each read at a level, so with integer keys in a range of size $R$ it reads at most $L(R + 2)$ words: it is wait-free.

The tests check all interleavings of five small cases with two processes, including two removes of one key and an add next to a node that is being removed; 60 seeded runs with three processes and three levels, with the check that every level is sorted and that every unmarked node at a level is in the level below; a remove that stops after its mark at level 0 while the others go on; the late link; the bug above; and that contains only reads.

## Complexity

| quantity | bound | status |
|---|---|---|
| expected steps of an operation alone, random levels | $O(\log n)$ | cited (Pugh) |
| contains alone in a perfect list of $2^L - 1$ keys | at most $3L - 1$ reads | measured for $L \le 10$ |
| reads of a contains, integer keys in a range of size $R$ | at most $L(R + 2)$ | proved (sketch file) |
| add or remove with contention | unbounded: lock-free, not wait-free | |
| CAS steps of a remove alone | $t + 1$ marks plus at most $t + 1$ unlinks, $t$ the top level | proved by counting |
| space | $\Theta(n + L)$ words when the expected top level is a constant | |

With random levels and promotion probability $1/2$, a node has two next words on average, so the space is about $2n$ words plus the sentinels. Under contention, every failed CAS costs a new FIND from the head, which is the main cost of the structure in practice.

## Variants

- **Lock-based lazy skip list.** Herlihy, Lev, Luchangco and Shavit search without locks and lock only the predecessors to add or remove, then validate. It is simpler to reason about and has a wait-free contains as well, but it blocks.
- **Marker nodes.** Java's ConcurrentSkipListMap, by Doug Lea, works with references, which cannot carry a mark bit. It marks a node by putting a special marker node after it, and its upper levels are separate index nodes; the idea is the same.
- **Restart from the predecessor.** On a failed CAS, FIND can restart from the last good node on the level above instead of from the head. This is a common optimization.
- **Priority queues.** A skip list whose removes always take the first node gives a [lock-free priority queue](/lock-free-priority-queue/); the [SprayList](/spraylist/) relaxes that removal to spread contention.
- **Trees.** A [non-blocking binary search tree](/non-blocking-bst/) gives the same set with a worst case that depends on its shape instead of on random levels.

## When to use it

Use it when you need a concurrent ordered set or map with scalable reads and writes and no locks, and when range scans that are not atomic are acceptable. Java's standard library uses a skip list of this kind for its concurrent ordered map. Compared with a lock-free hash table such as the [split-ordered list](/split-ordered-list/), it gives order but costs $O(\log n)$ pointer reads per search. Compared with balanced trees, it has no rebalancing, which is what makes it simple to make lock-free.

## Pitfalls

- **Deciding a remove at an upper level.** Only the mark at level 0 has a single winner; see above.
- **Linking upper levels before level 0.** Then a key can be reached from an upper level while it is not in the set, and a remove can mark a node that add has not finished linking at the bottom; always link level 0 first and mark level 0 last.
- **A stale next in the new node.** Retrying the CAS at L17 with a next field from an older search can link the node in front of a node that is no longer its successor. Reset it as at L16.
- **Freeing a node when its remover returns.** Late links make that unsafe; see memory reclamation.
- **Contains that unlinks.** Contains could unlink marked nodes like FIND, but then it writes and is no longer wait-free; the version here only steps past them.

## Implementations

## History

Pugh introduced skip lists in 1990 and also gave a version with locks. Fraser's PhD thesis at Cambridge (2003, published as a technical report in 2004) gave a lock-free skip list from single-word CAS, using the mark bit of the Harris list at every level, and the epoch-based reclamation that frees its nodes; Fraser and Harris later built skip lists from multi-word CAS and from software transactional memory as well. Sundell and Tsigas gave another lock-free skip list in 2003, used for priority queues. Doug Lea's ConcurrentSkipListMap in Java 6 (2006) brought the idea into a standard library. Herlihy, Lev, Luchangco and Shavit published the lock-based lazy skip list in 2007, and the lock-free version of this page, with its linearization argument, became a chapter of Herlihy and Shavit's textbook in 2008.

## References
