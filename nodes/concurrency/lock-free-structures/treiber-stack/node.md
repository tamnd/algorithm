---
tag: YJWGPQ
kind: data-structure
slug: treiber-stack
name: Treiber stack
aliases:
- Treiber's stack
- lock-free stack
area: concurrency/lock-free-structures
level: core
summary: Lock-free linearizable stack on a linked list. Push and pop are CAS loops on the top pointer. It needs tags or safe memory reclamation against the ABA problem.
implements: [stack]
complexity:
  vars: {n: the number of processes, k: the largest number of operations that run at the same time}
  space: {extra: Θ(1)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [stack, singly-linked-list, compare-and-swap, linearizability, lock-freedom]
see_also: [elimination-backoff-stack, aba-problem, tagged-pointers, hazard-pointers, epoch-based-reclamation, michael-scott-queue, linearization-point, flat-combining]
sources:
  - paper: "R. Kent Treiber, Systems programming: coping with parallelism, Research Report RJ 5118, IBM Almaden Research Center, April 1986"
    locator: the lock-free LIFO list of the report (push and pop with compare-and-swap on the top word)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, 2020
    locator: Chapter 11 (Concurrent stacks and elimination), the unbounded lock-free stack; Chapter 10 for the ABA problem
  - paper: doi:10.1145/78969.78972
    title: "Maurice P. Herlihy and Jeannette M. Wing, Linearizability: a correctness condition for concurrent objects, ACM TOPLAS 12(3), 1990"
    locator: Sections 2 and 3 (the definition of linearizability that the correctness proof uses)
  - paper: doi:10.1109/TPDS.2004.8
    title: "Maged M. Michael, Hazard pointers: safe memory reclamation for lock-free objects, IEEE Transactions on Parallel and Distributed Systems 15(6), 2004"
    locator: the LIFO stack example, which uses hazard pointers in place of tags
---

The Treiber stack is a [lock-free](/lock-freedom/) [stack](/stack/) on a [singly linked list](/singly-linked-list/). A shared word `top` points to the first node, and both push and pop change `top` with one [compare-and-swap](/compare-and-swap/) (CAS) in a retry loop. R. Kent Treiber described it in an IBM research report in 1986. It is [linearizable](/linearizability/), it takes a constant number of steps when no other process interferes, and it is the standard first example of a non-blocking data structure. When popped nodes are freed and their addresses are used again, the plain version suffers from the [ABA problem](/aba-problem/), so a real implementation adds a tag to `top` or uses safe memory reclamation.

## In plain words

Picture a pile of plates and many cooks who add and take plates. There is no lock on the pile. A cook who wants to add a plate first looks at the plate on top, puts the new plate on it, and then says "if the top is still the plate I saw, make my plate the new top". The hardware does this check and the change as one action. If another cook changed the top in the meantime, the check fails, and the cook looks again and tries again. Taking a plate works the same way: look at the top plate and the plate under it, and make the plate under it the new top, only if the top did not change.

A failed try means that some other cook succeeded. So the pile as a whole always makes progress, even if one unlucky cook can keep failing.

## The abstract type

The Treiber stack implements the [stack](/stack/): push$(x)$ adds $x$ on top, and pop() removes and returns the top item, or returns EMPTY when the stack has no items. Both operations are total: pop on an empty stack returns at once and does not wait.

Several processes call the operations at the same time. The safety condition is [linearizability](/linearizability/): each operation seems to take effect at one moment between its call and its return, and the results are those of a sequential stack that applies the operations in the order of these moments. The progress condition is [lock-freedom](/lock-freedom/): in each infinite run in which processes keep taking steps, operations keep completing.

## Representation

### Model and notation

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names |
| $k$ | the largest number of operations that are in progress at the same time (the point contention) |

The processes are asynchronous: each one runs at its own speed, and each one can stop forever between two steps. They share memory words with atomic read, write and CAS. CAS$(w, a, b)$ sets $w$ to $b$ and returns true if $w = a$; otherwise it changes nothing and returns false. CAS has [consensus number](/consensus-number/) $\infty$, while plain registers have consensus number 1, so registers alone could not give a lock-free stack for $n \ge 2$ processes. The memory is sequentially consistent unless a paragraph says otherwise.

### Fields

- A node has two fields: `val`, the item, and `next`, a pointer to the node below it, or NULL.
- The shared word `top` points to the top node, or is NULL for the empty stack. In the tagged version, `top` holds a pair (pointer, tag) in one word, and each successful CAS on `top` adds 1 to the tag.

**Invariant.**

- **(T1)** The nodes that can be reached from `top` by `next` pointers form a finite list with no cycle. The abstract stack is the sequence of their `val` fields, with the item of `top` first.
- **(T2)** Once a node is in the list, its fields do not change until a pop removes it.
- **(T3)** A node that a push has allocated but not yet published (its CAS at L5 has not yet succeeded) cannot be reached from `top`, and only its owner writes to it.

## Operations

```pseudo id=main
PUSH(v)
L1  n ← new node with n.val = v
L2  repeat
L3      t ← top
L4      n.next ← t
L5  until CAS(top, t, n)          ▷ linearization point when it succeeds

POP()
L6  repeat
L7      t ← top
L8      if t = NULL then return EMPTY   ▷ linearization point: the read at L7
L9      nx ← t.next
L10 until CAS(top, t, nx)         ▷ linearization point when it succeeds
L11 v ← t.val
L12 retire(t)                     ▷ free t, now or later (see below)
L13 return v
```

**Push.** The new node is private until the CAS at L5 succeeds, so the write at L4 cannot disturb anyone. The CAS succeeds only if `top` still holds the pointer $t$ that L3 read. Then $n$ becomes the top and $n.next = t$ is the old top, so the item is pushed. If the CAS fails, some other operation changed `top` between L3 and L5, and the loop reads `top` again.

**Pop.** L7 reads the top node $t$ and L9 reads the node $nx$ below it. The CAS at L10 makes $nx$ the top only if `top` still holds $t$. After the CAS, $t$ is out of the list and belongs to this process, so L11 can read its value at leisure. A pop that reads NULL at L7 returns EMPTY: at that moment the stack was empty.

**Linearization points.** A push takes effect at its successful CAS. A pop that returns an item takes effect at its successful CAS. A pop that returns EMPTY takes effect at the read of L7 that returned NULL. The [linearization points](/linearization-point/) are fixed steps of the operation itself, which makes the proof short.

**The tagged version.** Replace `top` by a pair $(t, c)$. L5 becomes CAS$(top, (t, c), (n, c+1))$ and L10 becomes CAS$(top, (t, c), (nx, c+1))$. A CAS now fails if any successful CAS hit `top` since the read, even if the pointer is the same again. This needs a double-width CAS (or a pointer with spare bits), and it assumes the tag does not wrap around during one operation.

**Cost of one operation.** Alone, a push takes 4 shared steps (allocation, L3, L4, L5) and a pop takes 5 (L7, L9, L10, L11, and the free). Each failed CAS costs 2 or 3 more steps.

### Memory reclamation

After L10, other pops may still hold $t$: they read it at L7 and are about to read $t.next$ at L9. If $t$ is freed at once and the memory goes back to the system, their read at L9 is a use-after-free. If the allocator gives the same address to a new node that is pushed again, a stale CAS at L10 can succeed: this is the [ABA problem](/aba-problem/), and the example below shows that it corrupts the stack. The stack is safe in three ways: with a garbage collector (an address is not reused while a process holds it); with the tag of the tagged version and [type-stable memory](/type-stable-memory/) (freed nodes go to a free list of nodes and never back to the system, so the stale read at L9 reads a node, and the tagged CAS then fails); or with [hazard pointers](/hazard-pointers/) or [epoch-based reclamation](/epoch-based-reclamation/), which delay the free until no process holds $t$. Tags alone do not stop the stale read; they only make it harmless.

### Weak memory

On a machine with a weaker memory model, the writes of L1 and L4 must be visible before `top` points to $n$. In C++11 terms, the CAS at L5 needs release order, and the read at L7 needs acquire order, so that a pop that sees $n$ also sees $n.val$ and $n.next$. On x86 a locked CAS is a full fence, so the hardware gives this, but the compiler must still not move the writes past the CAS.

## Example

**A push and a pop that race.** The stack holds one item, 1, in node $A$. Process $p$ pushes 2 while $q$ pops.

| step | process | line | action | result |
|---|---|---|---|---|
| 1 | $q$ | L7 | read `top` | $A$ |
| 2 | $q$ | L9 | read $A.next$ | NULL |
| 3 | $p$ | L1 | allocate $B$ with val 2 | $B$ |
| 4 | $p$ | L3 | read `top` | $A$ |
| 5 | $p$ | L4 | $B.next \leftarrow A$ | |
| 6 | $p$ | L5 | CAS(`top`, $A$, $B$) | true: push(2) takes effect |
| 7 | $q$ | L10 | CAS(`top`, $A$, NULL) | false: `top` is $B$ |
| 8 | $q$ | L7 | read `top` | $B$ |
| 9 | $q$ | L9 | read $B.next$ | $A$ |
| 10 | $q$ | L10 | CAS(`top`, $B$, $A$) | true: pop takes effect |
| 11 | $q$ | L11 | read $B.val$ | 2 |

The pop returns 2 and the stack holds 1 again. The order of the linearization points is push(2) at step 6, then pop at step 10, and a sequential stack gives the same results.

**The ABA run.** Now the plain version frees popped nodes, and the allocator reuses the oldest freed address. The stack is $a, b, c$ from top to bottom, in nodes $A$, $B$, $C$. Process $p$ calls one pop; process $q$ pops twice, pushes $x$, and pops again.

| step | process | action | state after it |
|---|---|---|---|
| 1 | $p$ | L7 reads `top` $= A$, L9 reads $A.next = B$ | $p$ is about to run CAS(`top`, $A$, $B$) |
| 2 | $q$ | pop returns $a$ and frees $A$ | `top` $= B$ |
| 3 | $q$ | pop returns $b$ and frees $B$ | `top` $= C$ |
| 4 | $q$ | push($x$) gets the reused address $A$, with $A.next = C$ | `top` $= A$, the stack is $x, c$ |
| 5 | $p$ | CAS(`top`, $A$, $B$) succeeds, because `top` is $A$ again | `top` $= B$, a freed node |
| 6 | $p$ | L11 reads $A.val = x$ and returns $x$ | |
| 7 | $q$ | pop reads the freed node $B$ | returns garbage |

After step 6 the stack should hold only $c$, but `top` points to freed memory, and $c$ is lost. No order of these operations gives these results, so the run is not linearizable. With the tag, the tag of `top` grew by 3 in steps 2 to 4, so the CAS of step 5 fails, $p$ reads `top` again and pops $x$, and $q$ then pops $c$.

## Correctness

The invariants (T1) to (T3) hold in each state, and each successful CAS changes the abstract stack exactly as the operation at that point requires: a push puts its item on top, a pop removes the top item and returns it. A failed CAS and all other steps do not change the list. The key fact for pop is that when CAS(`top`, $t$, $nx$) succeeds, $nx$ is still $t.next$; this holds when an address is not reused during the operation (garbage collection, hazard pointers, epochs), or when the tag shows that `top` did not change at all. The full proof is in the proof file below.

## Complexity

| operation | alone | one operation, under contention | amortized over a run |
|---|---|---|---|
| push | 4 steps | unbounded | $O(k)$ steps |
| pop | 5 steps (1 if empty) | unbounded | $O(k)$ steps |

The space is one node for each item and one shared word.

**Not wait-free.** An operation can fail its CAS forever: if, between each read of `top` by $p$ and its CAS, another process completes a push, then each CAS of $p$ fails. So no bound on the steps of one operation exists, and the stack is lock-free but not [wait-free](/wait-freedom/).

**Amortized bound.** An iteration of a loop fails only if a successful CAS on `top` happened between its read at L3 or L7 and its CAS. One successful CAS can make at most one iteration fail in each other operation that is in progress at that time, so at most $k - 1$ iterations. Each operation has exactly one successful CAS (or ends at L8). So in a finite run with $m$ completed operations, the number of failed iterations is at most $(k - 1) m$ plus one for each operation still in progress, and each iteration takes $O(1)$ steps. The total is $O(k m)$ steps, that is $O(k)$ amortized for each operation.

**The contention problem.** All processes CAS the same word. On a cache-coherent machine each CAS moves the cache line of `top`, so the throughput does not grow with the number of processes. Exponential back-off after a failed CAS helps, and the [elimination back-off stack](/elimination-backoff-stack/) goes further.

## Variants

- **Back-off.** After a failed CAS, wait a random time that doubles after each failure. This lowers the contention but does not change the progress guarantee.
- **[Elimination back-off stack](/elimination-backoff-stack/).** Hendler, Shavit and Yerushalmi (2004) let a push and a pop that both fail their CAS meet in a side array and cancel, with no access to `top`. It keeps linearizability and scales much better.
- **LL/SC.** With [load-linked/store-conditional](/load-linked-store-conditional/), L10 becomes SC$(top, nx)$ after LL$(top)$ at L7. An SC fails if `top` was written at all, so this version has no ABA problem, but real LL/SC can fail for other reasons.
- **[Flat combining](/flat-combining/).** One process applies a batch of pushes and pops for the others under a lock. It is blocking, but it can be faster at high contention.
- **Michael and Scott queue.** The [Michael and Scott queue](/michael-scott-queue/) uses the same CAS-loop idea for a FIFO queue, with two pointers in place of one.

## When to use it

Use the Treiber stack when you need a stack, or a free list, that is shared by threads and must not block when a thread is preempted or stops. It is short and well understood. With a garbage collector (Java, Go, C#), the plain version is correct as it is. In C or C++, add tags or a reclamation scheme. At high contention a single `top` word is a hot spot, so prefer the elimination version, a per-thread pool, or a lock with combining.

## Pitfalls

- **Freeing at L12 without a scheme.** Another pop may still read $t.next$ at L9. Use a tag with type-stable memory, hazard pointers or epochs, as above.
- **ABA with reused nodes.** A plain CAS at L10 succeeds when `top` holds the same address again, even though the list changed. The example shows the lost item. Add the tag, or make sure that no address is reused while a process holds it.
- **Writing $n.next$ after the CAS.** If L4 comes after L5, a pop can see $n$ with a wrong `next` field. The node must be complete before it is published.
- **Tag wrap-around.** A tag of 16 bits wraps after 65536 changes, and a process stopped for that long can still suffer ABA. Use a wide tag.
- **Weak memory.** Without release order on the CAS at L5 and acquire order on the read at L7, a pop on ARM or POWER can read an old value of $n.val$.

## Implementations

## History

Treiber gave the stack in his 1986 IBM research report on concurrent programming. The report is the usual citation for the non-blocking LIFO list. The idea of a counter next to the top pointer, to make a reused address visible to CAS, was already in use for free lists on IBM System/370 machines. Herlihy and Wing (1990) defined linearizability, the condition under which the stack is now proved correct. Michael (2004) showed the stack with hazard pointers in place of tags, and Hendler, Shavit and Yerushalmi (2004) added elimination. The stack is the first lock-free structure in the textbook of Herlihy and Shavit.

## References
