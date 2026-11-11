---
tag: 6NM0K3
kind: technique
slug: tagged-pointers
name: Tagged pointers (version counters)
aliases: [counted pointers, version tags, version-tagged pointers]
area: concurrency/memory-reclamation
level: core
summary: Keep a counter next to a pointer in one double-width word and change both with one CAS, so that a CAS fails if the pointer changed and came back. A w-bit counter can still wrap around.
prereqs: [aba-problem, compare-and-swap]
see_also: [treiber-stack, michael-scott-queue, arora-blumofe-plaxton-deque, load-linked-store-conditional, free-list, type-stable-memory, hazard-pointers, double-compare-and-swap]
sources:
  - url: https://bitsavers.trailing-edge.com/pdf/ibm/370/princOps/GA22-7000-6_IBM_System_370_Principles_of_Operation_7th_ed_198003.pdf
    title: IBM System/370 Principles of Operation, GA22-7000-6, seventh edition, IBM, March 1980
    locator: Appendix A, the programming examples for COMPARE AND SWAP and COMPARE DOUBLE AND SWAP, Free-Pool Manipulation (a free list whose head word holds a pointer and a counter)
  - paper: "R. Kent Treiber, Systems programming: coping with parallelism, Research Report RJ 5118, IBM Almaden Research Center, April 1986"
    locator: the lock-free LIFO list with a counter next to the top pointer
  - paper: doi:10.1145/248052.248106
    title: Maged M. Michael and Michael L. Scott, Simple, fast, and practical non-blocking and blocking concurrent queue algorithms, PODC 1996, pages 267-275
    locator: the non-blocking queue, in which head, tail and every next field are counted pointers, and the discussion of the ABA problem and the counter wraparound
  - paper: doi:10.1145/277651.277678
    title: Nimar S. Arora, Robert D. Blumofe and C. Greg Plaxton, Thread scheduling for multiprogrammed multiprocessors, SPAA 1998, pages 119-129
    locator: the deque code with the age word, which holds the top index and a tag
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 10, the section on memory reclamation and the ABA problem (the queue with stamped references)
  - paper: doi:10.1109/TPDS.2004.8
    title: Maged M. Michael, Hazard pointers, safe memory reclamation for lock-free objects, IEEE Transactions on Parallel and Distributed Systems 15(6), 2004, pages 491-504
    locator: the discussion of the ABA problem and of tags as the usual remedy, which hazard pointers replace
---

A **tagged pointer** keeps a counter, the tag, next to a pointer in one word that is read and written as a unit, usually a double-width word of two machine words. Every successful [compare-and-swap](/compare-and-swap/) on the word writes the new pointer and the old tag plus one. A CAS that read $(A, c)$ succeeds only if the word still holds $(A, c)$, so a node $A$ that was removed, reused and put back in the meantime no longer matches: its tag is now different. This is the oldest remedy for the [ABA problem](/aba-problem/). It does not free memory safely by itself. It needs nodes that are only reused as nodes of the same kind, in a [free list](/free-list/) or [type-stable memory](/type-stable-memory/), so that a stale read of a removed node is harmless. With a tag of $w$ bits, the protection fails when the word changes a multiple of $2^w$ times between the read and the CAS of one operation.

## In plain words

A shared box holds the name of the first item in a pile. A worker looks in the box, sees "item A", and gets ready to replace it with "item B".

While the worker waits, someone else takes item A away, and later puts a new item back that happens to get the same name A. If the worker only compares names, it sees "A" again and goes on as if nothing changed. Its plan is now wrong.

So the box also holds a counter, and every change to the box adds one to it. The worker writes down the name and the counter, and it changes the box only if both are the same as before. Now the change is seen.

If the counter is small, it can come back to the same value after enough changes. Then the problem returns.

## When it applies

- **A CAS on a pointer to a node that can be reused.** The structure frees or recycles nodes, and an operation reads a pointer, does some work that depends on the node, and then makes a CAS on the same pointer. The [Treiber stack](/treiber-stack/) pop is the standard case.
- **The hardware has a double-width CAS, or the pointer has spare bits.** On x86-64 the CMPXCHG16B instruction compares and swaps 16 bytes; on IBM System/370 and its successors, COMPARE DOUBLE AND SWAP does the same for two words. Without it, the tag must fit into unused bits of a 64-bit pointer, or the pointer must be an index into an array.
- **Nodes are reused only as nodes.** A thread can still read a node after another thread removed it. The read must not fault and must not see a different type of object. A free list or a type-stable pool gives this; a general allocator that returns memory to the system does not.
- **The structure needs no traversal of removed nodes.** Tags make one CAS correct. They do not say when a node can go back to the system, so they are not a full [safe memory reclamation](/safe-memory-reclamation/) method.

## The template

The shared word $X$ holds a pair $(p, c)$ of a pointer and a $w$-bit tag. A load of $X$ reads both halves at once, and DWCAS compares and swaps both at once.

```pseudo id=main
TAGGED-UPDATE(X)                       ▷ X is a double-width word (pointer, tag)
L1  (p, c) ← X                          ▷ one double-width load
L2  if p = nil then return EMPTY        ▷ hole: the case with nothing to change
L3  q ← NEW-POINTER(p)                  ▷ hole: read node p, which may be stale
L4  c' ← (c + 1) mod 2^w
L5  if not DWCAS(X, (p, c), (q, c')) then go to L1
L6  RECYCLE(p)                          ▷ hole: put p on a type-stable free list
```

The holes are the empty case at L2, the new pointer at L3, and the recycling at L6. For the Treiber stack pop, $X$ is the root, NEW-POINTER reads $p.next$ and the value of $p$, and RECYCLE puts $p$ on the free list. For a push, the same loop runs with $q$ a new node whose $next$ is set to $p$ before L5.

**Walk-through.** L1 takes a snapshot of the pointer and its tag. L3 reads the node, and this read can be stale: by now another thread may have removed $p$ and given its memory to a new node. L5 is the only step that changes $X$. If any successful update of $X$ happened between L1 and L5, it changed the tag, so the DWCAS fails and the loop starts again with fresh values. Only if $X$ was not changed at all, or was changed a multiple of $2^w$ times, does the DWCAS succeed. In the first case the values read at L3 are still right, because $p$ stayed in the structure all the time. The second case is the wraparound in the pitfalls.

**Why a stale read is harmless.** If $p$ was removed between L1 and L3, the tag of $X$ changed, so L5 fails (unless the tag wrapped around) and the value read at L3 is never used. The read must only not crash, and type-stable memory gives that.

**Cost.** One double-width load and one double-width CAS per try, and no shared writes other than the CAS itself. A try fails only if another update of $X$ succeeded, so the loop is [lock-free](/lock-freedom/).

**Example.** A stack $A \to B$ with the root $(A, 0)$. Process $p$ pops, process $q$ pops and then pushes $x$. The free list is LIFO, so the push gets the memory of $A$ back.

| step | process | line | action | root after |
|---|---|---|---|---|
| 1 | $p$ | L1 | reads $(A, 0)$ | $(A, 0)$ |
| 2 | $p$ | L3 | reads $A.next = B$ | $(A, 0)$ |
| 3 | $q$ | pop | DWCAS $(A, 0) \to (B, 1)$, recycles $A$ | $(B, 1)$ |
| 4 | $q$ | push $x$ | gets node $A$, sets $A.next = B$, DWCAS $(B, 1) \to (A, 2)$ | $(A, 2)$ |
| 5 | $p$ | L5 | DWCAS expects $(A, 0)$ | |

With $w \ge 2$, the root holds $(A, 2)$ at step 5, so the DWCAS fails and $p$ tries again. It then pops $x$, which is right. With $w = 1$, the tag $2 \bmod 2 = 0$ and the root holds $(A, 0)$, so the DWCAS succeeds and writes $(B, 1)$. The value $x$ is lost. With no tag at all, the same happens. The test file finds both runs.

## Classic examples

- [Free lists](/free-list/) on IBM System/370: the examples in the Principles of Operation keep a counter next to the head of a free pool and change both with COMPARE DOUBLE AND SWAP. This is the origin of the technique.
- [Treiber stack](/treiber-stack/): the root is a counted pointer, and pop is the template with NEW-POINTER reading $p.next$.
- [Michael and Scott queue](/michael-scott-queue/): head, tail and the $next$ field of every node are counted pointers. The tag of a node's $next$ field must survive when the node is recycled, so that a stale CAS on the $next$ of a reused node fails.
- [Arora, Blumofe and Plaxton deque](/arora-blumofe-plaxton-deque/): the top index and a tag share one word, the age, and the owner adds one to the tag when it resets the deque. The pointer here is an array index, so a single-width CAS is enough.

## Variations

- **Tags in spare pointer bits.** On x86-64, user pointers use only the low 47 or 48 bits, and aligned nodes have zero low bits. A tag of up to 16 or 20 bits fits into the same 64-bit word, and a plain CAS works. The tag is then small, so wraparound is a real risk.
- **Indices instead of pointers.** If nodes live in an array of $2^k$ entries, a 32-bit index and a 32-bit tag fit into one 64-bit word.
- **A tag per node.** Some versions keep the counter in the node and increment it on every reuse, and keep a copy in each pointer to the node. The check is the same: a reused node has a new count.
- **[Load-linked and store-conditional](/load-linked-store-conditional/).** An SC fails if the word was written at all since the LL, even with the same value. This removes the ABA problem with no tag, but a real SC can also fail for other reasons, and on some processors other memory accesses between the two steps make it fail.
- **Hazard pointers and epochs.** [Hazard pointers](/hazard-pointers/) and [epoch-based reclamation](/epoch-based-reclamation/) prevent the reuse of a node while a thread can still compare against it, so the ABA problem cannot happen on that node. They also let memory go back to the system, which tags do not.

## Pitfalls

- **A tag that is too small.** The tag protects only against fewer than $2^w$ changes between L1 and L5. With $w = 1$ the example above already fails after two changes; with $w = 2$ the test finds a failure after four changes, and $w = 3$ fixes that run. A thread that is preempted for a long time between L1 and L5 can see any number of changes. Use at least 32 bits, and better 64.
- **A tag on the wrong word.** The tag must sit in the same word as the pointer that the CAS compares. A counter in the node, or in a separate global word, is not checked by the CAS on the pointer, so the ABA run still succeeds. The right L5 compares the pointer and its own tag in one DWCAS.
- **Two separate loads of the pointer and the tag.** If L1 reads the pointer and the tag with two loads, a change between them gives a pair that never was in $X$. Read both with one double-width load, or read the tag first and check it again after the pointer.
- **Memory that goes back to the system.** Tags make the CAS correct, but the read at L3 still touches a node that may have been freed. If the allocator returns the page to the operating system, the read faults. Recycle nodes only into a pool of the same type.
- **A recycled node that loses its tag.** In the Michael and Scott queue, the tag in a node's $next$ field must keep counting across reuse. If a new node starts with tag 0 again, a stale CAS on the $next$ of the old node can succeed.

## Exercises

1. In the example, give a schedule in which $w = 2$ is not enough. *Answer:* let $q$ pop $A$, push $x$ (which gets $A$), pop $x$ and push $y$ (which gets $A$ again) between steps 2 and 5. The root changes four times and holds $(A, 0)$ again, so $p$'s DWCAS succeeds and $y$ is lost. The test file runs this case.
2. Show that on the stack it is enough to change the tag only when a pop succeeds. *Answer:* suppose a pop read $(A, c)$ at L1 and the root holds $A$ again at L5. If no pop removed $A$ in between, then $A$ stayed in the stack, its $next$ field did not change, and the CAS is a correct pop. If a pop removed $A$, that pop changed the tag.
3. Explain why the queue needs a tag on each $next$ field and not only on head and tail.

## References
