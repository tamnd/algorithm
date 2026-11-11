---
tag: F7GS7Y
kind: data-structure
slug: lock-free-priority-queue
name: Lock-free priority queue
aliases:
- Sundell-Tsigas priority queue
- skip-list priority queue
- Lindén-Jonsson priority queue
- skiplist-based concurrent priority queue
area: concurrency/lock-free-structures
level: advanced
summary: Concurrent priority queue where delete-min is performed by logically marking the first node of a skip list.
implements: [priority-queue]
complexity:
  vars: {n: "the number of keys", L: "the number of levels of the skip list", B: "the bound on the deleted prefix before it is cut off"}
  space: {extra: Θ(n + B + L)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [priority-queue, lock-free-skip-list, logical-deletion, linearizability]
see_also: [spraylist, multiqueue, relaxed-priority-queue, fine-grained-concurrent-heap, lock-free-skip-list, binary-heap, epoch-based-reclamation, read-modify-write]
sources:
  - paper: doi:10.1007/978-3-319-03850-6_15
    title: Jonatan Lindén and Bengt Jonsson, A skiplist-based concurrent priority queue with minimal memory contention, OPODIS 2013, LNCS 8304, pages 206 to 220
    locator: the deletion mark in the predecessor's pointer, DeleteMin with fetch-and-or, the deleted prefix, the batch cut of the prefix with BoundOffset, Restructure, the inserting flag, and the linearizability argument
  - paper: doi:10.1016/j.jpdc.2004.12.005
    title: Håkan Sundell and Philippas Tsigas, Fast and lock-free concurrent priority queues for multi-thread systems, Journal of Parallel and Distributed Computing 65(5), 2005, pages 609 to 627
    locator: the first lock-free skip list priority queue from CAS, where delete-min marks the first node and then removes it from every level (conference version IPDPS 2003)
  - paper: doi:10.1109/IPDPS.2000.845994
    title: Nir Shavit and Itay Lotan, Skiplist-based concurrent priority queues, IPDPS 2000, pages 263 to 268
    locator: the first skip list priority queue, with locks, whose delete-min takes the first node that is not yet taken; it is quiescently consistent, not linearizable
  - paper: doi:10.1145/2688500.2688523
    title: Dan Alistarh, Justin Kopinsky, Jerry Li and Nir Shavit, The SprayList, a scalable relaxed priority queue, PPoPP 2015, pages 11 to 20
    locator: the contention at the head of a skip list priority queue, and the relaxed delete-min that sprays to one of the first few keys
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: the chapter on priority queues, the section on a skiplist-based unbounded priority queue, and its remark that this queue is quiescently consistent but not linearizable
---

A lock-free priority queue keeps its keys in a [lock-free skip list](/lock-free-skip-list/) sorted by key, so the minimum is always the first node that is still in the queue. Insert is a skip list insert. Delete-min takes the first node by [logical deletion](/logical-deletion/). The name covers a family: Sundell and Tsigas (2003) gave the first lock-free one, and Lindén and Jonsson (2013) gave the version on this page, which cuts the work of delete-min to one [fetch-and-or](/read-modify-write/) on one word in the common case. The deleted nodes always form a prefix of the bottom level. A delete-min walks that prefix and marks the first pointer that is not yet marked, and the node behind that pointer is its result. Nobody unlinks single nodes: when the prefix gets long, one CAS on the head cuts it off. The queue is [linearizable](/linearizability/) and [lock-free](/lock-freedom/).

## In plain words

Think of a line of people sorted by ticket number. A clerk serves the person with the lowest number. Here there are many clerks at once.

Each person holds the hand of the next person. To serve someone, a clerk does not tap that person: the clerk ties a ribbon on the hand that holds them, from the person in front. A hand with a ribbon means "the one behind me is served". The first clerk who ties a ribbon on a bare hand gets the person behind it.

A newcomer joins by taking a free hand. A hand with a ribbon cannot take a newcomer, so nobody can slip in among the people who were already served.

The served people stay in line for a while. Now and then a clerk sends the whole served group away at once.

## The abstract type

The queue implements a [priority queue](/priority-queue/) of keys; equal keys are allowed.

- insert(k): add $k$.
- delete_min(): remove a least key and return it, or return EMPTY if the queue is empty.

## Representation

### Model and notation

We use the asynchronous shared memory model with processes that may crash, atomic read, write, CAS and fetch-and-or on single words, and [sequential consistency](/sequential-consistency/). The bottom pointer of a node and its mark bit share one word. Nodes are not freed in the code (the model has a garbage collector); see the section on memory reclamation.

| Symbol | Meaning |
|---|---|
| $x.\mathit{next}[0]$ | the bottom level word of node $x$: a pair (pointer, mark) |
| $x.\mathit{next}[i]$, $i > 0$ | an upper level pointer, with no mark: a hint for insert |
| deleted | a node is deleted when the bottom pointer *into* it is marked |
| prefix | the deleted nodes that are still reachable at the bottom level |
| $B$ | the bound: a delete-min that walked more than $B$ nodes tries to cut the prefix |
| $x.\mathit{inserting}$ | true while the insert of $x$ is still linking upper levels |
| FAO | fetch-and-or: set the mark bit of a word and return its old value |

### Fields

- A node has a key, a top level, the inserting flag, and its next words.
- head and tail sentinels with keys $-\infty$ and $+\infty$.

**Invariant.** (1) Along the bottom level from head, the marked pointers form a prefix of the chain: the pointers into the deleted nodes come first and all later pointers are unmarked. (2) The nodes that are not deleted are sorted by key. (3) A marked word never changes, except the head's word, which moves forward to another deleted node. The abstract queue is the multiset of keys of the nodes after the prefix.

So "the first pointer that is not marked" is the pointer into the least key, and an insert, which needs an unmarked pointer for its CAS, can never link a node inside the prefix.

## Operations

```pseudo id=main
LOCATE_PREDS(k)                               ▷ returns (last deleted node seen, preds, succs)
L1  pred ← head; del ← null
L2  for i ← L − 1 down to 0 do
L3      (cur, d) ← pred.next[i]               ▷ d is the mark, at level 0 only
L4      while cur.key < k or cur.next[0] is marked or (i = 0 and d) do
L5          if i = 0 and d then del ← cur     ▷ cur is deleted
L6          pred ← cur; (cur, d) ← pred.next[i]
L7      preds[i] ← pred; succs[i] ← cur
L8  return (del, preds, succs)

INSERT(k)                                     ▷ t is the random top level
L9  node ← new node with key k, top t, inserting = true
    loop
L10     (del, preds, succs) ← LOCATE_PREDS(k)
L11     node.next[0] ← (succs[0], 0)
L12     if CAS(preds[0].next[0], (succs[0], 0), (node, 0)) then exit loop
    i ← 1
L13 while i ≤ t do
L14     node.next[i] ← succs[i]
L15     if node.next[0] is marked or succs[i].next[0] is marked or del = succs[i] then exit
L16     if CAS(preds[i].next[i], succs[i], node) then i ← i + 1
L17     else (del, preds, succs) ← LOCATE_PREDS(k); if succs[0] ≠ node then exit
L18 node.inserting ← false

DELETE_MIN()
L19 x ← head; offset ← 0; newhead ← null; obshead ← head.next[0]
    repeat
L20     nxt ← x.next[0]
L21     if pointer of nxt = tail then return EMPTY
L22     if newhead = null and x.inserting then newhead ← x
L23     nxt ← FAO(x.next[0]); offset ← offset + 1
L24     x ← pointer of nxt
    until nxt was not marked                  ▷ this FAO deleted x
L25 v ← x.key; if newhead = null then newhead ← x
L26 if offset ≤ B then return v
L27 if CAS(head.next[0], obshead, (newhead, 1)) then  ▷ cut the prefix before newhead
L28     RESTRUCTURE()
L29 return v

RESTRUCTURE()                                 ▷ move the head's upper pointers past deleted nodes
L30 pred ← head; for i ← L − 1 down to 1 do loop
L31     h ← head.next[i]
L32     if h.next[0] is not marked then exit loop
L33     cur ← pred.next[i]
L34     while cur.next[0] is marked do pred ← cur; cur ← pred.next[i]
L35     if CAS(head.next[i], h, cur) then exit loop
```

A node $x$ with a marked $x.\mathit{next}[0]$ is deleted and is not the last deleted node, since the node after it is deleted too; the last deleted node is the one whose incoming pointer is marked. LOCATE_PREDS skips both kinds (L4), so an insert lands after the prefix.

**Linearization points.** An insert at its CAS at L12. A delete-min that returns a key at its FAO at L23 whose old value was not marked. A delete-min that returns EMPTY at its read at L20 that saw the tail. The cut at L27 and RESTRUCTURE do not change the abstract queue.

**Why the mark goes into the predecessor's pointer.** An insert can only link behind a pointer that is not marked, and the FAO that deletes a node marks exactly the pointer an insert would need to link a node in front of the remaining queue. So an insert and a delete-min that race for the same spot race on one word, and one of them fails. If the mark were a flag in the deleted node, as in queues that mark the node itself, an insert could link a new node behind a deleted node, inside the prefix, and the cut at L27 would throw it away. The test `test_a_deletion_flag_in_the_node_loses_an_insert` finds this run with the explorer and replays it: insert(0) returns, and a later delete-min returns a larger key while 0 is lost.

**Why newhead stops at a node that is still being inserted.** The cut at L27 makes the nodes before newhead unreachable at the bottom level. A node whose insert is still at L13 to L17 may still be linked at an upper level by its inserter, and the inserter reads its fields. Keeping it reachable lets a reclamation scheme treat "cut off" as "no longer used by inserts".

### Memory reclamation

The cut at L27 makes up to $B$ nodes unreachable at once, but slow processes can still be inside them: a delete-min that read an old head walks through them, and a LOCATE_PREDS may start from one of them at level 0 through an upper level hint that RESTRUCTURE has not moved yet. So the process that wins the CAS at L27 must not free the cut nodes at once. It should retire them to a scheme such as [epoch-based reclamation](/epoch-based-reclamation/), which frees them when every process has left the operation it was in; batch retirement fits that scheme well. [Hazard pointers](/hazard-pointers/) are awkward here, because a delete-min walks a prefix of unbounded length. Without a scheme, a slow walker reads a freed node, and if the address is reused as a new node, an FAO can mark a live pointer by mistake and delete a key that nobody returns.

### Weak memory

The CAS at L12 must be a release, so that a delete-min that reads the new pointer sees the key. The FAO at L23 and the CAS at L27 are read-modify-writes on one word; the FAO must be at least an acquire, so that the key read at L25 is the key of the node it deleted. The write at L18 and the read at L22 are only a hint for reclamation and can be relaxed in the model of this page.

## Example

Take $L = 1$ (one level), $B = 0$, and the queue $\{1, 2, 3\}$: head, 1, 2, 3, tail with no marks.

1. $p$: delete_min. FAO(head.next[0]) returns (1, 0). Node 1 is deleted: head's pointer is marked. $p$ returns 1. Its CAS at L27 fails, because head's word changed from (1, 0) to (1, 1).
2. $q$: insert(0). LOCATE_PREDS skips node 1, whose incoming pointer is marked, and stops at node 2 with key $2 \ge 0$. So preds[0] = node 1 and succs[0] = node 2. $q$ stops before its CAS.
3. $p$: delete_min. obshead is (1, 1). FAO(head.next[0]) returns (1, 1): node 1 was taken. FAO(node 1.next[0]) returns (2, 0): $p$ has deleted node 2. offset is 2 > 0, so $p$ will try the cut.
4. $q$: CAS(node 1.next[0], (2, 0), (0, 0)) fails, because the word is (2, 1). $q$ runs LOCATE_PREDS again, which skips node 1 and node 2 and stops at node 3, and links node 0 after node 2: head, 1, 2, 0, 3. The queue is $\{0, 3\}$.
5. $p$: CAS(head.next[0], (1, 1), (2, 1)) succeeds. Node 1 is cut off. The list is head, 2, 0, 3, and a third delete_min returns 0.

With the flag in the node instead, the CAS in step 4 succeeds (node 1's pointer is not marked), node 0 goes between node 1 and node 2, and the cut in step 5 removes it with node 1.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) is a sketch. Its parts are as follows.

- *Safety.* Invariant (1), the marked prefix, holds because an insert links only behind an unmarked pointer, an FAO marks the first unmarked pointer it meets after a marked one, and the cut moves head to a deleted node with a marked pointer. A node with an unmarked bottom pointer is never cut off, so the FAO that deletes a node acts on the boundary of the prefix in the current list. By (2), the node behind the boundary has a least key. With the linearization points above, each history is linearizable to a priority queue. The insert of a key below the current minimum goes right after the prefix and is the next node that a delete-min takes.
- *Progress.* Insert retries only after a failed CAS, which means that another process changed the word. A delete-min does one FAO per node it passes, and each FAO either deletes a node, which ends it, or passes a node that is already deleted; the prefix it walks grows only when other delete-min operations finish. So the queue is lock-free. It is not wait-free: a delete-min can be kept walking by others that delete in front of it.

The tests check all interleavings of six small cases with two processes, including two delete-min operations that both try to cut the prefix and an insert of a key below the minimum while the prefix is cut; 60 seeded runs with three processes and bounds 0, 1 and 2; that each delete-min alone changes exactly one word outside the head; and the bug above.

## Complexity

| quantity | bound | status |
|---|---|---|
| successful writes outside the head per delete-min | exactly one FAO (none if EMPTY) | proved, and tested alone |
| steps of a delete-min alone | at most $3(B + 2) + 2 + 5L$ | measured for $L \le 8$, $B \le 8$ |
| steps of an insert alone | $O(\log n)$ expected with random levels | cited (as for a skip list, Pugh) |
| deleted nodes still reachable | at most $B + 1$ when no process runs, plus those kept for inserts in progress | measured in the sequential tests |
| with contention | unbounded (lock-free, not wait-free) | |

Under contention all delete-min operations meet at the boundary of the prefix: their FAO steps hit the same few words. Lindén and Jonsson report that this design improves on earlier skip list priority queues by 30 to 80 percent in their experiments, because each delete-min writes to one word instead of unlinking a node from every level. Space: one node per key, about two words of pointers on average, plus up to $B + 1$ deleted nodes and the sentinels.

## Variants

- **Sundell and Tsigas.** Delete-min marks the first node and then removes it from every level like a skip list remove, with helping for the unlinks. It is linearizable and lock-free, but every delete-min writes to the head at several levels, which is the contention that Lindén and Jonsson remove.
- **Shavit and Lotan, and the textbook queue.** Delete-min walks the bottom level and takes the first node whose own flag it can set, then removes it. A key inserted behind the walker is missed, so the queue is [quiescently consistent](/quiescent-consistency/) but not linearizable.
- **Relaxed queues.** The [SprayList](/spraylist/) lets delete-min take one of the first $O(p \log^3 p)$ keys, for $p$ processes, chosen by a random walk, so the processes do not all meet at the head. The [MultiQueue](/multiqueue/) uses many sequential heaps. Both are [relaxed priority queues](/relaxed-priority-queue/).
- **Heaps.** A [fine-grained concurrent heap](/fine-grained-concurrent-heap/) uses locks on the nodes of a [binary heap](/binary-heap/) instead of a skip list.

## When to use it

Use it when you need a strict, linearizable concurrent priority queue without locks, for example for a shared event queue in a simulation or a scheduler that must not skip the least key. It scales to a few threads; past that, all delete-min operations fight over the head, and a relaxed queue such as the SprayList or a MultiQueue is faster if the application can accept keys that are close to the minimum. With one consumer and many producers, the delete-min side has no contention and the insert side scales like a skip list.

## Pitfalls

- **A deletion flag in the node.** It lets an insert land inside the prefix, and the batch cut loses it; see above.
- **Cutting the prefix while a node in it is still being inserted.** The inserter may still link it at upper levels and read it; keep it, as newhead does at L22.
- **Assuming delete-min writes once.** Most delete-min calls do one FAO, but a call that cuts the prefix also runs RESTRUCTURE, which writes the head at every level.
- **Treating the FAO as a CAS loop.** The FAO never fails. Replacing it with a read and a CAS adds failed CAS steps under contention, and that is the cost the design avoids.
- **Duplicates.** An insert goes in front of equal keys, so equal keys come out in reverse order of insertion; the queue is not stable.

## Implementations

## History

Shavit and Lotan built the first skip list priority queue in 2000, with locks, and showed that it is quiescently consistent. Sundell and Tsigas gave a lock-free skip list priority queue from CAS at IPDPS 2003, with a journal version in 2005. Herlihy and Shavit's textbook (2008) presents a lock-free skip list priority queue that is quiescently consistent. Lindén and Jonsson observed in 2013 that the cost of these queues is in the memory traffic at the head, and moved the deletion mark into the predecessor's pointer so that a delete-min writes one word; they verified a model of the algorithm with the SPIN model checker. In 2015 Alistarh, Kopinsky, Li and Shavit gave up strict order to remove the head as a point of contention, with the SprayList.

## References
