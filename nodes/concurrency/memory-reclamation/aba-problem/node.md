---
tag: M62E1N
kind: concept
slug: aba-problem
name: ABA problem
aliases: [ABA, ABA hazard]
area: concurrency/memory-reclamation
level: intro
summary: A CAS succeeds although the location changed from A to B and back to A in the meantime, so the comparison is misled and the update uses facts that are no longer true.
prereqs: [compare-and-swap]
see_also: [tagged-pointers, hazard-pointers, treiber-stack, michael-scott-queue, load-linked-store-conditional, type-stable-memory, safe-memory-reclamation, use-after-free]
sources:
  - url: https://bitsavers.trailing-edge.com/pdf/ibm/370/princOps/GA22-7000-6_IBM_System_370_Principles_of_Operation_7th_ed_198003.pdf
    title: IBM System/370 Principles of Operation, GA22-7000-6, seventh edition, IBM, March 1980
    locator: Appendix A, the programming examples for COMPARE AND SWAP and COMPARE DOUBLE AND SWAP, Free-Pool Manipulation (the free list that fails if the head is removed and put back, and the counter that prevents it)
  - paper: doi:10.1145/248052.248106
    title: Maged M. Michael and Michael L. Scott, Simple, fast, and practical non-blocking and blocking concurrent queue algorithms, PODC 1996, pages 267-275
    locator: the discussion of the ABA problem in the non-blocking queue and of the modification counters next to the pointers
  - paper: doi:10.1109/TPDS.2004.8
    title: Maged M. Michael, Hazard pointers, safe memory reclamation for lock-free objects, IEEE Transactions on Parallel and Distributed Systems 15(6), 2004, pages 491-504
    locator: the description of the ABA problem and the use of hazard pointers to prevent it
  - paper: doi:10.1109/ISORC.2010.10
    title: Damian Dechev, Peter Pirkelbauer and Bjarne Stroustrup, Understanding and effectively preventing the ABA problem in descriptor-based lock-free designs, ISORC 2010, pages 185-192
    locator: the definition of the ABA problem and the survey of the ways to prevent it
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 10, the section on memory reclamation and the ABA problem
---

The **ABA problem** is a failure of [compare-and-swap](/compare-and-swap/) (CAS). A thread reads a shared word and finds the value $A$. It then computes a new value from facts it read at the same time, and it calls CAS to replace $A$ with the new value only if the word still holds $A$. Meanwhile other threads change the word from $A$ to $B$ and back to $A$. The CAS sees $A$ and succeeds, but the facts that the thread computed from are no longer true. The usual cause is the reuse of memory: a node at address $A$ is removed, freed, allocated again, and put back, so the pointer has the same bits but names a different node. The usual cures are [tagged pointers](/tagged-pointers/), which make the word differ after any change, and [safe memory reclamation](/safe-memory-reclamation/), which keeps an address from being reused while a thread may still compare against it.

## In plain words

You park your car in spot 12 and leave a note for a friend: "my car is in spot 12, the key is under the mat". While you are away, your car is towed, and another car of the same model is parked in spot 12.

Your friend comes, sees a car of the right model in spot 12, and looks under the mat. The check "is there such a car in spot 12" passed, but the car is a different one, and the note is wrong about it.

CAS checks only the value of one word. It cannot see that the word changed and came back.

## The idea

**The pattern.** A lock-free operation often has this form: read a word $X$ and get $a$, read other data that depends on $a$, compute a new value $n$, and call $CAS(X, a, n)$. The CAS makes the update atomic only if "$X$ still holds $a$" implies "the data I read is still valid". That implication holds when the value $a$ can never return to $X$ once it has left. ABA is the case in which $a$ returns.

**Why it happens.** The value can come back in two ways.

- *Reuse of memory.* The node at address $a$ is removed from the structure and freed. The allocator gives the same address to a new node, which is then put back into $X$. This is the common case in C and C++, and allocators that reuse the most recently freed block first make it likely.
- *The same node goes back.* With no free at all, a node that is removed and later inserted again also brings back its address. A free list that recycles nodes is the classic example.

**The Treiber stack.** A pop reads $top = A$, then reads $A.next = B$, and calls $CAS(top, A, B)$. Suppose that between the read and the CAS, another thread pops $A$, pops $B$, and pushes $A$ again (or pushes a new node that got the address of $A$). Now $top = A$ and $A.next = C$. The CAS of the first thread succeeds and sets $top = B$, a node that is no longer on the stack. $C$ is lost, and $B$, which may be freed, is now the top.

**What prevents it.**

- *Tags.* Put a counter next to the pointer and change both with one double-width CAS. Every successful change adds one to the counter, so a word that changed and came back has a different counter. A counter of $w$ bits can still wrap around after $2^w$ changes. See [tagged pointers](/tagged-pointers/).
- *LL/SC.* [Load-linked and store-conditional](/load-linked-store-conditional/) fails if any write to the word happened since the load-linked, even a write of the same value. Real hardware can also fail it for other reasons, so the code still loops.
- *Protection from reuse.* With [hazard pointers](/hazard-pointers/), a thread publishes $A$ before it reads $A.next$, and no node named by a hazard pointer is freed. So the address $A$ cannot come back as a new node while the thread can still make its CAS. Grace-period schemes such as [epoch-based reclamation](/epoch-based-reclamation/) give the same guarantee for every node read inside an operation. These cure ABA from reuse, not ABA from a node that is inserted again on purpose.
- *A garbage collector.* In Java, a node that a thread still points to is never freed, so its address does not come back while the thread can compare against it.
- *Descriptors and fresh objects.* Some designs never put the same value in a word twice, for example by installing a new descriptor object for each change, which is never reused while some thread may read it.

**ABA and use-after-free.** ABA is not itself a [use-after-free](/use-after-free/): the CAS compares bits, and the comparison is about a value, not an access to a freed block. But the stale read before the CAS, of $A.next$, is a use-after-free if $A$ was freed, and both come from the same cause. Tags alone fix the CAS, but not the stale read; that is why tags are used with a [type-stable](/type-stable-memory/) pool, in which a stale read returns a harmless value.

## Examples

- **A free list in the IBM System/370.** The programming examples for COMPARE AND SWAP show a free list whose head can be removed and put back between a read and a CAS. The fix in the same appendix puts a counter next to the head pointer and uses COMPARE DOUBLE AND SWAP.
- **The Michael and Scott queue.** The [queue](/michael-scott-queue/) in its 1996 form makes $head$, $tail$ and every $next$ field a counted pointer, because a dequeued node goes to a free list and may come back as a new node.
- **The Treiber stack with immediate free.** The tests of the [tagged pointers](/tagged-pointers/) page run every interleaving of two threads on a small [Treiber stack](/treiber-stack/) with an allocator that reuses the last freed address. With plain pointers, a run loses a value. With a tag of 16 bits, no run does. With a tag of one bit, the run in which the word changes twice between a read and a CAS loses a value again.
- **The work-stealing deque.** The [Arora, Blumofe and Plaxton deque](/arora-blumofe-plaxton-deque/) keeps the top index and a tag in one word, because an index, unlike a pointer, comes back quite often.

## Where it is used

- Every lock-free structure that uses CAS on pointers in a language with manual memory management must deal with ABA, either with tags or with a reclamation scheme.
- The ABA problem is one of the two main reasons for [safe memory reclamation](/safe-memory-reclamation/) schemes; the other is the stale read.
- Hardware support: double-width CAS instructions such as CMPXCHG16B on x86-64 and CASP on ARMv8.1 exist in part to make tagged pointers possible, and LL/SC on POWER, ARM and RISC-V avoids ABA on one word.
- Teaching: ABA is the standard example that a lock-free algorithm that is correct with a garbage collector can be wrong without one.

## References
