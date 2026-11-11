---
tag: 319C81
kind: algorithm
slug: hazard-pointers
name: Hazard pointers
aliases: [Michael's hazard pointers, hazard pointer, HP]
area: concurrency/memory-reclamation
level: core
summary: A reader publishes each pointer it will use in a hazard pointer slot and re-reads the source to validate it. A retired node is freed only when no slot names it, so garbage stays bounded.
solves: [safe-memory-reclamation]
complexity:
  vars: {n: the number of processes, K: the hazard pointers per process, R: the retire list length that starts a scan}
  space: {slots: Θ(n K), garbage: O(n R)}
  steps: {protect_try: O(1), retire_amortized: O(1)}
properties: {robust: true, bounded_garbage: true, wait_free_reclamation: true, needs_store_load_fence: true}
history:
  year: 2002
  people: [Maged M. Michael]
  note: Michael presented hazard pointers at PODC 2002 and gave the full method in IEEE TPDS in 2004. They are part of the C++26 standard library through P2530.
prereqs: [safe-memory-reclamation, treiber-stack]
see_also: [pass-the-buck, epoch-based-reclamation, hazard-eras, interval-based-reclamation, drop-the-anchor, optimistic-access, michael-scott-queue, aba-problem]
sources:
  - paper: doi:10.1109/TPDS.2004.8
    title: Maged M. Michael, Hazard pointers, safe memory reclamation for lock-free objects, IEEE Transactions on Parallel and Distributed Systems 15(6), 2004, pages 491-504
    locator: Section 3, the methodology (hazard pointer slots, RetireNode and Scan, and the bound on retired nodes not yet freed); Section 4, applying hazard pointers to stacks, queues and lists
  - paper: doi:10.1145/571825.571829
    title: Maged M. Michael, Safe memory reclamation for dynamic lock-free objects using atomic reads and writes, PODC 2002, pages 21-30
    locator: the first version of the method, with atomic reads and writes only
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition (2020)
    locator: Chapter 19, Optimism and manual memory management, the section on hazard pointers
  - paper: doi:10.1016/j.jpdc.2007.04.010
    title: Thomas E. Hart, Paul E. McKenney, Angela Demke Brown and Jonathan Walpole, Performance of memory reclamation for lockless synchronization, Journal of Parallel and Distributed Computing 67(12), 2007, pages 1270-1285
    locator: the description and measured cost of hazard pointers next to QSBR, EBR and lock-free reference counting
---

Hazard pointers are a [safe memory reclamation](/safe-memory-reclamation/) method for lock-free data structures. Before a process uses a node, it writes the address of the node into one of its own shared slots, a *hazard pointer*, and then reads the source pointer again to check that the node is still linked. When a process unlinks a node it does not free it; it puts it on a private retire list. When the list is long enough, the process reads all hazard pointers of all processes and frees every listed node that no hazard pointer names. A stopped process can hold back only the few nodes its own slots name, so the garbage stays bounded.

## In plain words

Many people work on one shared shelf of boxes. Before you open a box, you write its number on your own card on the wall. Then you look at the shelf again to check that the box is still there. If it is gone, you wipe your card and start again.

When somebody takes a box off the shelf, they do not throw it away at once. They put it in their own bin. When the bin is full, they read every card on the wall. Each box in the bin whose number is on no card goes to the trash. The others wait for the next round.

If one person falls asleep, their card holds back only one or two boxes. Everybody else can still empty their bins.

## The problem

[Safe memory reclamation](/safe-memory-reclamation/) for a lock-free structure such as the [Treiber stack](/treiber-stack/) or the [Michael and Scott queue](/michael-scott-queue/). A process that unlinks a node cannot know whether another process is about to read it, so freeing at once causes a [use after free](/use-after-free/) and, after reuse of the address, the [ABA problem](/aba-problem/). The task is to free each retired node eventually, never while a process may access it, and to keep the number of retired but unfreed nodes bounded even when processes stop.

The model: $n$ asynchronous processes that may stop forever between any two steps, on a sequentially consistent shared memory with atomic read/write registers (consensus number 1) and, in the client, [compare-and-swap](/compare-and-swap/) (consensus number $\infty$). Each process $p$ has $K$ hazard pointers $HP[p][0..K-1]$, single-writer registers that all processes read. $R$ is the length of the retire list that starts a scan, and $H = nK$ is the number of slots.

## The algorithm

```pseudo id=main
PROTECT(i, src)                     ▷ src is a root or a field of a protected node
L1  p ← src
L2  HP[me][i] ← p                   ▷ publish the hazard
L3  if src ≠ p then goto L1         ▷ validate: p is still linked
L4  return p                        ▷ p is safe until slot i is written again
RETIRE(x)                           ▷ x is already unlinked
L5  rlist ← rlist ∪ {x}
L6  if |rlist| ≥ R then SCAN()
SCAN()
L7  plist ← { HP[q][j] ≠ nil : 0 ≤ q < n, 0 ≤ j < K }
L8  for each x in rlist: if x ∈ plist then keep x in rlist
L9      else remove x from rlist and FREE(x)
CLEAR()                             ▷ at the end of each operation
L10 HP[me][j] ← nil for every j
```

L2 alone is not enough. Between L1 and L2 another process may unlink the node, retire it, scan, and free it, all before the hazard pointer is visible. L3 closes this gap: if the source still holds $p$ after the hazard pointer was published, then $p$ was still linked at that moment, so it can only be retired later, and any scan that frees it must read the slot after that and will see the hazard. If the source changed, the process does not know whether $p$ is safe, so it tries again.

A scan reads the $H$ slots once into a set and then checks each listed node against the set. Nodes that are still protected stay in the list for the next scan. The method does not need a special order of the reads in L7: a slot read too early can only miss a hazard that will fail its own validation at L3.

In the Treiber stack, `pop` protects $top$ with slot 0, then reads $top.next$ and $top.val$ and tries the compare-and-swap; the winner calls RETIRE($top$). In the Michael and Scott queue, `dequeue` protects $head$ with slot 0 and $head.next$ with slot 1, and then checks that $head$ did not change before it trusts $head.next$. `push` and `enqueue` need slot 0 only for the tail.

## Example

A stack $top \to A \to B$, with two processes, $K = 2$ and $R = 1$, so every RETIRE scans. Process $p$ pops once and process $q$ pops twice. The run below is the one that the test finds when L3 is removed.

| step | process | line | action | state after |
|---|---|---|---|---|
| 1 | $p$ | L1 | reads $top = A$ | |
| 2 | $q$ | L1 to L4 | protects $A$: $HP[q][0] = A$, $top$ is still $A$ | |
| 3 | $q$ | pop | reads $A.next = B$, CAS $top$ from $A$ to $B$ | $top \to B$ |
| 4 | $q$ | L5 to L9 | retires $A$; the scan sees $HP[q][0] = A$ and keeps $A$ | $rlist_q = \{A\}$ |
| 5 | $q$ | L10 | clears its slots | |
| 6 | $q$ | pop | protects $B$, CAS $top$ from $B$ to nil, retires $B$; the scan reads $HP[p][0] = $ nil | $top =$ nil |
| 7 | $p$ | L2 | writes $HP[p][0] = A$ | |
| 8 | $q$ | L7 to L9 | reads its own slots, $plist = \{B\}$; frees $A$, keeps $B$ | $A$ is freed |
| 9 | $p$ | L3 | reads $top =$ nil $\ne A$, goes back to L1 | |
| 10 | $p$ | L1 | reads $top =$ nil, the stack is empty | $p$ returns empty |

Without L3, process $p$ goes on to read $A.next$ and $A.val$ after step 8, which reads a freed node. The explorer finds such a run at once and reports a read after free. The scan in step 8 is allowed to free $A$ even though $p$ has just named it, because $p$ will not trust $A$: its validation fails.

## Correctness

The full proof is in proofs/correctness.md. It assumes the three client rules: a process accesses a node only after PROTECT returned it at L4 and before it overwrites the slot; a node is retired once, after it is unlinked; and an unlinked node is not linked again before it is freed.

- **Key fact.** If PROTECT returns $x$ at its L3 read at time $t_3$, then $x$ was linked at $t_3$, so it is retired after $t_3$. Every scan that could free $x$ reads all slots after the retire, which is after the hazard was written at L2 and before it is cleared. Such a scan sees the hazard and keeps $x$.
- **Safety.** No process accesses a freed node, and no node is freed twice.
- **Bound.** With $R > nK$, each retire list holds at most $R$ nodes, so at most $nR$ retired nodes are unfreed, even if processes stop at any steps.

The test file checks every interleaving of small stack and queue runs, many seeded random runs, the use after free without L3 or with an immediate free, and the bound $nR$ with a stopped process.

## Complexity

| measure | value |
|---|---|
| shared space | $H = nK$ slots |
| PROTECT | 3 steps per try; lock free |
| RETIRE | O(1) amortized expected steps with $R = 2nK$; the scan is wait free |
| retired but unfreed nodes | at most $nR$, whatever the other processes do |

**Scan cost.** After a scan the list holds at most $nK$ nodes, since each kept node is named by one of the $nK$ slots. So the next scan comes at least $R - nK$ retirements later and frees at least $R - nK$ nodes. With $plist$ in a hash set, a scan takes $O(nK + R)$ expected steps. With $R = 2nK$ this is $O(1)$ expected per retired node. A sorted array instead of a hash set gives $O(\log H)$ per node in the worst case.

**Garbage.** Each list holds at most $R$ nodes at any time, so the total is at most $nR = O(n^2 K)$ with $R = 2nK$. The test runs three processes with $K = 2$, $R = 12$ and process 0 stopped inside a pop: the peak over many seeds and run lengths of 50 and 400 operations is 24, below the bound $nR = 36$. Under [epoch-based reclamation](/epoch-based-reclamation/) the same run keeps all 400 nodes.

## Properties

- Robust: a stopped process holds back at most $K$ nodes through its slots and its own list of at most $R$.
- PROTECT is lock free, not wait free: it retries while the source keeps changing. RETIRE and SCAN are wait free.
- Needs only reads and writes for the method itself; compare-and-swap is used by the client.
- Each dereference costs a write and a read, and on real hardware a store-load fence between them, so traversals of long lists are slower than with epochs.
- The client must know which pointers it holds. A protected node cannot be used to reach a second node without protecting that one too.

## Variants and improvements

- **[Pass the buck](/pass-the-buck/).** Herlihy, Luchangco, Martin and Moir (2002) published the same idea with guards and a wait-free Liberate that hands trapped values to the guards.
- **Hazard pointers with ranges.** [Hazard eras](/hazard-eras/) publish an era instead of a pointer, and [interval-based reclamation](/interval-based-reclamation/) publishes an interval of epochs. Both drop the per-node validation write when the era did not change.
- **Fewer hazard pointers.** [Drop the anchor](/drop-the-anchor/) publishes one anchor every $K$ nodes of a list traversal, and [optimistic access](/optimistic-access/) reads without protection and protects only the nodes it writes.
- **Asymmetric fences.** The Folly library moves the cost of the fence from the reader to the scanner, with a process-wide barrier such as Linux `membarrier`.
- **Wait-free reads.** Nikolaev and Ravindran (PPoPP 2020, WFE) make the reads wait free with helping, on top of [hazard eras](/hazard-eras/).

## When to use it

Use hazard pointers when a stalled or preempted thread must not stop reclamation, for example in a library that cannot control its callers, and when operations touch a few nodes each, as in stacks, queues and hash tables. For long traversals or read-mostly data, [epoch-based reclamation](/epoch-based-reclamation/) or [RCU](/read-copy-update/) is faster but not robust. [Hazard eras](/hazard-eras/), [interval-based reclamation](/interval-based-reclamation/) and [Hyaline](/hyaline/) sit between the two.

## Pitfalls

**Skipping the validation.** The wrong code is L1 and L2 and then use $p$. A scan may have read the slot before L2 and freed $p$; the test finds this run at once. The right code re-reads the source at L3 and retries on a change.

**No store-load fence.** On x86 (TSO) the read at L3 can be performed before the write at L2 becomes visible, which brings back the same bug. The write at L2 must be a sequentially consistent store, or be followed by a full fence, or the scanner must use an asymmetric barrier.

**Validating against the wrong source.** In the queue, $head.next$ must be validated by checking that $head$ is unchanged. Checking only $head.next$ is not enough, because $head$ itself may have been retired and freed.

**Retiring before the unlink.** RETIRE must come after the step that removes the last link. Calling it from a process that lost the compare-and-swap, or twice for the same node, gives a double free.

**Too small an R.** With $R \le nK$ a scan may free nothing, and every RETIRE scans; the amortized cost is no longer constant.

## Implementations

## History

Maged Michael presented hazard pointers at PODC 2002, in a version that needs only atomic reads and writes for the reclamation itself, and published the full method with applications to many lock-free structures in IEEE TPDS in 2004. Herlihy, Luchangco and Moir presented the closely related pass the buck method at DISC 2002. Hart, McKenney, Demke Brown and Walpole compared hazard pointers with quiescent-state and epoch-based reclamation in 2007 and found them slower for traversals but robust to stalled threads. Facebook's Folly library has shipped a hazard pointer implementation for years, and the C++26 standard library includes `std::hazard_pointer` through proposal P2530.

## References
