---
tag: YM4G39
kind: algorithm
slug: lock-free-reference-counting
name: Lock-free reference counting
aliases: [LFRC, Detlefs-Martin-Moir-Steele reference counting, Valois reference counting]
area: concurrency/memory-reclamation
level: advanced
summary: Each node counts the links and threads that point to it. A thread adds to the count before it uses a node and frees it when the count drops to zero, with a pool or a DCAS to keep the increment safe.
solves: [safe-memory-reclamation]
complexity:
  vars: {n: the number of processes, L: the number of nodes that one release frees}
  space: {per_node: Θ(1)}
  steps: {safe_read: O(1), release: O(1 + L)}
properties: {robust: false, bounded_garbage: false, per_read_cost: true, needs_type_stable_memory: true}
history:
  year: 1995
  people: [John D. Valois, Maged M. Michael, Michael L. Scott, David L. Detlefs, Paul A. Martin, Mark Moir, Guy L. Steele Jr.]
  note: Valois gave lock-free reference counting with a type-stable pool at PODC 1995, and Michael and Scott corrected it the same year. Detlefs, Martin, Moir and Steele removed the pool with DCAS at PODC 2001.
prereqs: [reference-counting, compare-and-swap, safe-memory-reclamation]
see_also: [treiber-stack, michael-scott-queue, fetch-and-add, double-compare-and-swap, type-stable-memory, aba-problem, hazard-pointers, pass-the-buck]
sources:
  - paper: doi:10.1145/224964.224988
    title: John D. Valois, Lock-free linked lists using compare-and-swap, PODC 1995, pages 214-222
    locator: the section on memory management, with SafeRead, Release and the reference count in each node of a free list
  - paper: "Maged M. Michael and Michael L. Scott, Correction of a memory management method for lock-free data structures, Technical Report 599, Computer Science Department, University of Rochester, 1995"
  - paper: doi:10.1145/383962.384016
    title: David L. Detlefs, Paul A. Martin, Mark Moir and Guy L. Steele Jr., Lock-free reference counting, PODC 2001, pages 190-199
    locator: the LFRCLoad operation with DCAS, the rules for counted pointers, and the restriction to structures without cycles
  - paper: doi:10.1109/tpds.2008.167
    title: Anders Gidenstam, Marina Papatriantafilou, Hakan Sundell and Philippas Tsigas, Efficient and reliable lock-free memory reclamation based on reference counting, IEEE Transactions on Parallel and Distributed Systems 20(8), 2009, pages 1173-1187
    locator: the combination of reference counts with hazard pointers that bounds the garbage and handles cycles
  - paper: doi:10.1016/j.jpdc.2007.04.010
    title: Thomas E. Hart, Paul E. McKenney, Angela Demke Brown and Jonathan Walpole, Performance of memory reclamation for lockless synchronization, Journal of Parallel and Distributed Computing 67(12), 2007, pages 1270-1285
    locator: the measured cost of lock-free reference counting next to hazard pointers, EBR and QSBR
---

Lock-free reference counting is a [safe memory reclamation](/safe-memory-reclamation/) method that gives each node a count of the pointers to it: links from the structure and local references of threads. A thread that wants to use a node reads a pointer to it, adds to the count, and checks that the pointer has not changed. A thread that drops a pointer subtracts from the count, and the thread that brings the count to zero frees the node. John Valois gave the method in 1995 with nodes in a type-stable pool, Maged Michael and Michael Scott corrected a race in it, and David Detlefs, Paul Martin, Mark Moir and Guy Steele made the increment safe with a double compare-and-swap, so that freed memory can go back to the system.

## In plain words

Each box in a shared shelf has a tally sheet. Before you take a box, you add a mark to its sheet, then you check that the box is still where you saw it.

If it moved, you rub out your mark and look again.

When you put a box down, or take it off the shelf, you rub out a mark. The person who rubs out the last mark throws the box away.

The danger is the moment between seeing the box and adding the mark. Someone can throw the box away in that moment. Valois keeps thrown-away boxes in a store room, so a late mark on one does no harm. Detlefs and others add the mark and check the shelf in one action.

## The problem

[Safe memory reclamation](/safe-memory-reclamation/) for lock-free structures such as the [Treiber stack](/treiber-stack/) and the [Michael and Scott queue](/michael-scott-queue/). Plain [reference counting](/reference-counting/) is not enough here: a thread reads a pointer from a shared word and then adds to the count of the node, and between these two steps another thread can remove the node, bring its count to zero and free it. The increment then writes to freed memory.

The model: $n$ asynchronous processes on a sequentially consistent shared memory with reads, writes, [fetch-and-add](/fetch-and-add/) and [compare-and-swap](/compare-and-swap/). Nodes come from a [type-stable](/type-stable-memory/) pool: a freed node stays a node and its count field keeps its value, so an increment on a free node is allowed. The structure must have no cycles, and every pointer that a thread keeps or that a node holds must be counted.

## The algorithm

```pseudo id=main
SAFE_READ(a, f)                      ▷ read a.f and hold a reference to it
L1  q ← a.f; if q = nil then return nil
L2  FAA(q.rc, 2)
L3  if a.f = q then return q
L4  RELEASE(q); go to L1
RELEASE(q)                           ▷ drop one reference to q
L5  if FAA(q.rc, −2) ≠ 2 then return
L6  if not CAS(q.rc, 0, 1) then return
L7  n ← q.next; free q to the pool; RELEASE(n)
```

The count moves in steps of 2, and its low bit is a **claim bit**. A node in the pool, or a node that some thread has claimed, has an odd count; allocation from the pool adds 1. A thread whose decrement at L5 takes the count to 0 must also win the CAS at L6 before it frees the node. The CAS fails if a late increment at L2 came first; that increment fails its check at L3 and calls RELEASE, and its decrement then tries the claim again. So exactly one thread claims each node, and no thread frees it twice.

Freeing a node removes the link in its field $next$, so L7 releases the next node, and one release can free a chain.

The client counts links too. Before a CAS writes a pointer to $x$ into a shared word, the thread adds 2 to the count of $x$ or gives up a reference that it holds, and it releases that count if the CAS fails. After a CAS removes a link to $y$, it calls RELEASE($y$).

## Example

A stack $top \to A \to B$, and two processes $p$ and $q$. Each link counts 2, so $A.rc = 2$ and $B.rc = 2$ at the start.

| step | process | line | action | $A.rc$ | $B.rc$ |
|---|---|---|---|---|---|
| 1 | $p$ | L1 | reads $top = A$, then stops | 2 | 2 |
| 2 | $q$ | L1 to L3 | SAFE_READ($top$) returns $A$ | 4 | 2 |
| 3 | $q$ | L1 to L3 | SAFE_READ($A.next$) returns $B$ | 4 | 4 |
| 4 | $q$ | pop | CAS $top$ from $A$ to $B$; the own reference to $B$ becomes the link of $top$ | 4 | 4 |
| 5 | $q$ | L5 | releases the link of $top$ and its own reference to $A$; the second FAA returns 2 | 0 | 4 |
| 6 | $q$ | L6, L7 | claims $A$ (0 to 1), frees $A$ to the pool, releases $A.next = B$ | 1 | 2 |
| 7 | $p$ | L2 | FAA on the free node $A$: harmless in the pool | 3 | 2 |
| 8 | $p$ | L3, L4 | $top = B \ne A$, so releases $A$; FAA returns 3, not 2 | 1 | 2 |
| 9 | $p$ | L1 | reads $top = B$ and goes on | 1 | 2 |

Without the pool, step 7 writes to freed memory. Without the claim bit, in steps of 1, step 6 leaves $A.rc = 0$, step 7 makes it 1, and the decrement at step 8 returns 1 and frees $A$ a second time. The test finds both runs.

## Correctness

The full proof is in proofs/correctness.md. Let $c(x)$ count the links to $x$, the references that threads hold, and the increments at L2 whose SAFE_READ has not yet ended.

- **Invariant.** $rc(x) = 2 c(x)$ while $x$ is allocated and not claimed, and $rc(x) = 2 c(x) + 1$ while it is claimed or free.
- **A claim needs no references.** The CAS at L6 succeeds only at $rc = 0$, so $c(x) = 0$. After that, $x$ gets no new link, because a link needs a held reference, and every pending increment fails its check at L3.
- **Safety.** A thread that holds $x$ keeps $c(x) \ge 1$, so the count is at least 2 and no claim succeeds.
- **No double free.** After a claim the count stays odd until the node is allocated again, so a second claim cannot succeed.
- **No leak without holders.** A node with no links and no holders is claimed by the last thread that releases it, and the chain of nodes after it follows.

The test file checks every interleaving of a stack run with three pops and of a queue run with an enqueue and two dequeues, the queue run also with DCAS, seeded random runs on both structures, the broken versions without the pool and without the claim bit, an immediate free, and the garbage under a stall.

## Complexity

| measure | value |
|---|---|
| space | one count per node |
| SAFE_READ | 1 read, 1 FAA and 1 check read when the source does not change; lock free |
| RELEASE | 1 FAA and 1 CAS, plus 2 steps for each node of the chain that it frees |
| writes per read | 1 FAA on the node, so every read writes to a shared cache line |
| unfreed garbage | the nodes that held references can reach; no bound in general |

**Garbage under a stall.** The test runs three processes on a structure with four nodes. Process 0 stops inside its first pop or dequeue while it holds a node that another process then removes, and the others do 50 or 400 operations. On the stack, the field $next$ of a node never changes after its push, so the stopped process keeps alive only the nodes below its node: the peak of removed but unfreed nodes is 6 or 7 for both run lengths, and the test checks a limit of 8. On the queue, the held node links to every node enqueued after it, so no dequeued node is freed: the peak is exactly 50 and 400.

## Properties

- A node is freed at once when its last reference goes away; there is no batch and no scan.
- Not robust: a stopped thread that holds a node keeps alive everything reachable from that node.
- Cycles of links are never freed, as with all reference counting.
- Each protected read is a write to the node, which makes reads of popular nodes slow on many cores.
- The method with the pool needs [type-stable memory](/type-stable-memory/); the method with DCAS needs a [double compare-and-swap](/double-compare-and-swap/) on two words, which common processors do not have.

## Variants and improvements

- **Valois, 1995.** The first version, with the pool and steps of 1. Michael and Scott showed that two threads can both see the count fall to zero and free the node twice, and fixed it with the claim bit.
- **DCAS, Detlefs, Martin, Moir and Steele, 2001.** L2 and L3 become one DCAS that adds 1 to $q.rc$ only if $a.f = q$. A free node is never touched, so freed memory can go back to the system and no claim bit is needed.
- **Single-word version with pass the buck.** Herlihy, Luchangco, Martin and Moir replace the DCAS by a [pass the buck](/pass-the-buck/) guard on the node during the increment.
- **Hazard pointers with counts.** Gidenstam, Papatriantafilou, Sundell and Tsigas protect the increment with [hazard pointers](/hazard-pointers/) and break chains of deleted nodes, which bounds the garbage.
- **Split counts.** An external count kept in the pointer word and an internal count in the node, joined when the pointer is replaced, as in some implementations of an atomic shared pointer. The increment then is a CAS on the pointer word itself.

## When to use it

Use lock-free reference counting when nodes must be freed as soon as no one uses them, when nodes are shared across operations, or when a node can stay in use for a long time, so that an epoch method would hold too much. Avoid it on read-heavy paths and for structures with cycles. For queues and other structures where a removed node keeps linking to live nodes, a stopped thread keeps everything alive; [hazard pointers](/hazard-pointers/) or [hazard eras](/hazard-eras/) bound the garbage instead.

## Pitfalls

**Increment after the free.** The wrong code runs L2 on memory that goes back to the system. Between L1 and L2 the node can be freed, and the FAA writes to freed memory. The right code keeps freed nodes in a type-stable pool, or uses the DCAS form. The test finds this on the stack and on the queue.

**No claim bit.** The wrong code frees the node whenever its decrement returns the step size. A late increment and its release can then take the count from 0 to 1 and back, and a second thread frees the node again. The right code claims the node at L6 with a CAS from 0 to 1 and lets allocation clear the bit. The test finds the double free.

**A link that is not counted.** The wrong client writes a pointer into a shared word or a node field by CAS and does not add to the count first. The count can then reach 0 while the link still exists. The right client adds the count before the CAS, or hands over a reference it holds, and releases it if the CAS fails.

**Long chains under a stall.** A removed node keeps its field $next$. In a queue, that field points to the next node, which is later removed and points to the next one, so a stalled thread keeps the whole tail of the history alive. Clear or break the links of removed nodes where the structure allows it.

## Implementations

## History

John Valois presented lock-free linked lists with a reference-counted free list at PODC 1995. In the same year Maged Michael and Michael Scott published a technical report that showed a race in the count and gave the correction with a claim bit. In 2001 David Detlefs, Paul Martin, Mark Moir and Guy Steele published lock-free reference counting with DCAS, which removed the type-stable pool. Later work combined counts with pass the buck and with hazard pointers to drop the DCAS and to bound the garbage.

## References
