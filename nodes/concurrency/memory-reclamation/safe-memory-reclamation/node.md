---
tag: 10QYW7
kind: problem
slug: safe-memory-reclamation
name: Safe memory reclamation
aliases: [safe memory reclamation problem, memory reclamation problem]
area: concurrency/memory-reclamation
level: core
summary: Free the nodes that a concurrent data structure has removed, but only when no thread can still access them, with low cost per read and a bound on the unfreed nodes.
prereqs: [use-after-free, lock-freedom]
see_also: [hazard-pointers, epoch-based-reclamation, read-copy-update, deferred-reclamation, aba-problem, treiber-stack, michael-scott-queue, harris-linked-list]
sources:
  - paper: doi:10.1109/TPDS.2004.8
    title: Maged M. Michael, Hazard pointers, safe memory reclamation for lock-free objects, IEEE Transactions on Parallel and Distributed Systems 15(6), 2004, pages 491-504
    locator: the statement of the problem for lock-free objects, the conditions on a reclamation method, and the bound on the retired nodes that are not yet freed
  - paper: doi:10.1016/j.jpdc.2007.04.010
    title: Thomas E. Hart, Paul E. McKenney, Angela Demke Brown and Jonathan Walpole, Performance of memory reclamation for lockless synchronization, Journal of Parallel and Distributed Computing 67(12), 2007
    locator: the description and the measured costs of quiescent-state-based reclamation, epoch-based reclamation, hazard pointers and lock-free reference counting
  - paper: doi:10.1145/2767386.2767436
    title: Trevor Brown, Reclaiming memory for lock-free data structures, there has to be a better way, PODC 2015
    locator: the survey of reclamation schemes and their trade-offs, and the definition of DEBRA and DEBRA+
  - paper: doi:10.1145/3583668.3594564
    title: Gali Sheffi and Erez Petrank, The ERA theorem for safe memory reclamation, PODC 2023, pages 102-112
    locator: the definitions of ease of integration, robustness and applicability, and the theorem that no scheme has all three
  - paper: "Keir Fraser, Practical lock-freedom, PhD thesis, University of Cambridge, Technical Report UCAM-CL-TR-579, 2004"
    locator: the chapter on the implementation of the lock-free structures, with the epoch-based garbage collector
  - paper: doi:10.1145/3178487.3178488
    title: Haosen Wen, Joseph Izraelevitz, Wentao Cai, H. Alan Beadle and Michael L. Scott, Interval-based memory reclamation, PPoPP 2018, pages 1-13
    locator: the survey of the robustness of reclamation schemes and the bound on unfreed nodes for interval-based reclamation
---

**Safe memory reclamation** (SMR) is the problem of freeing the nodes that a concurrent data structure has removed, without a [use-after-free](/use-after-free/) by any thread. In a lock-free structure such as the [Treiber stack](/treiber-stack/), a thread can load a pointer to a node and then be delayed; meanwhile another thread removes the node. The remover cannot know, without help, whether some thread still holds the pointer. Freeing at once is unsafe, and never freeing leaks memory. An SMR scheme gives the structure a small interface (protect a pointer, retire a removed node) and decides when each retired node can be freed. Good schemes keep the cost of a read low, keep the number of retired but unfreed nodes bounded even when threads stop, and need few changes to the data structure. No known scheme has all three, and for a precise form of these goals none can.

## In plain words

Many people read from a shared set of folders. Some people also take folders out of the set when they are no longer needed.

A person who takes a folder out cannot shred it at once, because someone may have just picked it up and still be reading it. But if nobody ever shreds old folders, the office fills up.

So there must be a rule that tells when an old folder is surely not in anybody's hands. The rule should not slow down the readers much. It should still work if one reader falls asleep with a folder in hand. And it should be easy to add to the office as it is.

## Definition

**Setting.** $n$ threads run operations of a concurrent data structure on a shared memory. A node is **reachable** while it can be found from the roots of the structure. An operation that unlinks a node $x$ calls $retire(x)$ once, after which $x$ is not reachable. The scheme also gives the operations a way to announce what they read: for example $protect(p)$ before a node is used, or $begin$ and $end$ around an operation. The scheme frees retired nodes at times it chooses.

**Input.** The data structure code with its calls to the interface, and any schedule of the threads, including schedules in which threads stop for good.

**Output.** For each retired node $x$, a free time $f_x \in (r_x, \infty]$, where $r_x$ is the time of $retire(x)$ and $\infty$ means never.

**Requirements.**

1. *Safety.* No thread accesses $x$ at a time $\tau \ge f_x$ through a pointer it obtained before $f_x$. Equivalently, there is no use-after-free on a node of the structure.
2. *Free only what was retired, and only once.* A node is freed only after its retire, and at most once.
3. *No leak when all threads progress.* If after some time every thread that is inside an operation takes steps and finishes it, then every retired node is freed after a finite number of further steps.

**Measures.** The **garbage** at time $\tau$ is the number of nodes $x$ with $r_x \le \tau < f_x$. A scheme is **robust** if the garbage stays bounded by a function of $n$ and the scheme's parameters, even when some threads stop for good. The other measures are the cost per read of a node (writes, fences, checks), the cost per retire, the progress of the reclamation code (blocking, lock-free or wait-free), and how much the data structure must change.

## Variants

- **Robust or not.** Robust schemes bound the garbage under stopped threads; non-robust schemes, such as epoch-based reclamation, only bound it when all threads progress.
- **Manual or automatic.** In a manual scheme, the programmer places the calls to protect and retire. In an automatic scheme, such as reference counting or a tracing garbage collector, the system finds the unreachable nodes.
- **With or without reuse.** A weaker goal only prevents the [ABA problem](/aba-problem/): nodes go to a [type-stable](/type-stable-memory/) free list and never back to the system, and [tagged pointers](/tagged-pointers/) make the CAS steps safe. Stale reads are then allowed, but memory cannot shrink.
- **Applicability.** Some schemes need every data structure to allow a restart at any read, or need the structure to give the nodes near an anchor; others work with any structure.

## Examples

- **The Treiber stack with two threads.** Thread $p$ reads $top = A$ and then reads $A.next$. Thread $q$ pops $A$ between the two reads and retires it. A safe scheme must not free $A$ before $p$'s read of $A.next$. With [hazard pointers](/hazard-pointers/), $p$ has published $A$ and checked it, so $q$'s scan sees $A$ and keeps it. With [epoch-based reclamation](/epoch-based-reclamation/), $p$ is inside an operation in an epoch that is too old, so the epoch cannot advance far enough to free $A$.
- **A stopped thread.** If $p$ stops for good after reading $top = A$, then a robust scheme still frees all other retired nodes. With hazard pointers, only $A$ (and the nodes in $p$'s other hazard pointers) stay; with epochs, no node retired after $p$ stopped is ever freed. The test files of the scheme pages measure this: on the stack and the queue with three threads, the garbage of epoch-based reclamation grows with the run, while that of hazard pointers stays under its bound.
- **The Michael and Scott queue.** A dequeue reads $head$, then $head.next$, then the value in $head.next$. Both nodes need protection, and the second only after a check that $head$ did not change, or the protection comes too late.

## Known algorithms

- **Grace periods.** [Epoch-based reclamation](/epoch-based-reclamation/), [quiescent-state-based reclamation](/quiescent-state-based-reclamation/), [read-copy-update](/read-copy-update/) and [DEBRA](/debra/): almost free reads, garbage unbounded when a thread stops.
- **Pointer protection.** [Hazard pointers](/hazard-pointers/) and [pass the buck](/pass-the-buck/): a write and a fence per protected node, garbage $O(n R)$ with a scan every $R$ retires.
- **Anchors and eras.** [Drop the anchor](/drop-the-anchor/), [hazard eras](/hazard-eras/) and [interval-based reclamation](/interval-based-reclamation/): fewer writes than hazard pointers, garbage bounded under stalls.
- **Restarts.** [DEBRA+](/debra/), [neutralization-based reclamation](/neutralization-based-reclamation/) and [optimistic access](/optimistic-access/): epochs or unprotected reads, with a restart of a delayed thread, which makes them robust.
- **Reference counting.** [Lock-free reference counting](/lock-free-reference-counting/) and [Hyaline](/hyaline/): counts per node or per batch of retired nodes.

## Bounds

The model is the asynchronous shared-memory model: $n$ threads, any schedule, and threads that may stop for good at any step.

- **A stopped thread keeps what it holds.** Suppose a thread may still access the nodes it loaded, and it stops while it holds pointers to $K$ nodes that are then retired. Any safe scheme must keep these nodes, because the thread could take its next step at any time. So in the worst case, any safe scheme keeps at least $n K$ retired nodes for $n$ threads that hold $K$ each. Hazard pointers match this up to the batch size: they keep at most $n K$ protected nodes plus the batches of at most $R$ nodes per thread.
- **Robustness costs something.** Sheffi and Petrank define three goals: a scheme is easy to integrate (it needs only simple calls and no changes to the structure's algorithm), robust (bounded garbage under stopped threads), and widely applicable (it works for all common structures). Their ERA theorem says that no scheme has all three. Epoch-based reclamation gives up robustness, hazard pointers give up applicability (some traversals cannot validate their pointers), and restart schemes give up ease of integration.
- **Without reuse.** If nodes are never freed to the system, there is no use-after-free at all, and the garbage is unbounded. Type-stable memory is this case with reuse inside the pool.

## Reductions

- **To garbage collection.** A tracing garbage collector solves the problem: a node is freed only when no thread holds a pointer to it. This is why lock-free structures in Java need no SMR scheme. The cost moves to the collector.
- **To reference counting.** Count the pointers to each node, both in the structure and in threads. The difficulty is to increment the count of a node that may be freed at the same moment, which [lock-free reference counting](/lock-free-reference-counting/) solves with a CAS on two words or with a scheme such as pass the buck.
- **The ABA problem reduces to SMR.** A scheme that keeps a node from being freed while a thread holds a pointer to it also keeps the address from being reused, so a CAS that compares against that pointer cannot be misled by reuse.

## Applications

- Lock-free stacks, queues, lists, skip lists and hash tables in C, C++ and Rust, which have no garbage collector.
- The Linux kernel, where RCU protects read-mostly structures such as routing tables and lists of modules.
- Libraries: the hazard pointers and RCU of the Folly library, the user-space RCU library liburcu, and the crossbeam-epoch crate in Rust.
- Database engines and memory allocators that keep lock-free indexes.

## References
