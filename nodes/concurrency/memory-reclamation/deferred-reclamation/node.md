---
tag: B9R4Q5
kind: concept
slug: deferred-reclamation
name: Deferred reclamation
aliases: [deferred destruction, retire list, limbo list, deferred free]
area: concurrency/memory-reclamation
level: intro
summary: A thread that removes a node does not free it. It puts the node on a retire list, and the node is freed later, in a batch, once a safety test says that no thread can still access it.
prereqs: [safe-memory-reclamation]
see_also: [hazard-pointers, epoch-based-reclamation, read-copy-update, grace-period, quiescent-state-based-reclamation, debra, use-after-free, treiber-stack]
sources:
  - paper: doi:10.1109/TPDS.2004.8
    title: Maged M. Michael, Hazard pointers, safe memory reclamation for lock-free objects, IEEE Transactions on Parallel and Distributed Systems 15(6), 2004, pages 491-504
    locator: the RetireNode and Scan routines, the private list of retired nodes, the threshold R and the amortized bound on the cost of a scan
  - url: https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-579.pdf
    title: Keir Fraser, Practical lock-freedom, PhD thesis, University of Cambridge, Technical Report UCAM-CL-TR-579, 2004
    locator: the section on epoch-based garbage collection, with the limbo lists that hold the nodes retired in each epoch
  - paper: "Paul E. McKenney, Exploiting deferred destruction: an analysis of read-copy-update techniques in operating system kernels, PhD thesis, OGI School of Science and Engineering at Oregon Health and Science University, 2004"
    locator: the description of deferred destruction and of the callbacks that run after a grace period
  - url: https://www.kernel.org/doc/html/latest/RCU/whatisRCU.html
    title: Paul E. McKenney, What is RCU?, the Linux kernel documentation
    locator: the call_rcu interface, which registers a callback that runs after a grace period, and the comparison with synchronize_rcu
  - paper: doi:10.1016/j.jpdc.2007.04.010
    title: Thomas E. Hart, Paul E. McKenney, Angela Demke Brown and Jonathan Walpole, Performance of memory reclamation for lockless synchronization, Journal of Parallel and Distributed Computing 67(12), 2007, pages 1270-1285
    locator: the common structure of the schemes, in which removed nodes wait on lists until they are safe to free, and the effect of the list size on cost
---

**Deferred reclamation** is the common pattern behind most [safe memory reclamation](/safe-memory-reclamation/) schemes. A thread that removes a node from a concurrent data structure does not free it at once, because another thread may have loaded a pointer to it and may still read it. Instead, the thread calls $retire(x)$, which puts the node on a **retire list** (also called a limbo list). Later, a reclamation step looks at the list and frees each node that a safety test allows. Schemes differ in the test: [hazard pointers](/hazard-pointers/) free the nodes that no hazard pointer names, and [epoch-based reclamation](/epoch-based-reclamation/) and [read-copy-update](/read-copy-update/) free the nodes retired before a [grace period](/grace-period/) ended. They share the list, the batching of the test, and the trade-off between the cost of a test and the number of nodes that wait to be freed.

## In plain words

In an office, people take old papers out of the files. They do not shred them at once, because a colleague may be reading a copy of the file list and may still come to look at them.

So they put the old papers in a tray. From time to time, when the tray is full, someone checks which papers nobody can still be looking for, and shreds only those. The rest stay in the tray until the next check.

Checking once per full tray is cheaper than checking for each paper. But the tray takes room, and if nobody can be sure about some papers, the tray keeps growing.

## The idea

**The interface.** The data structure calls $retire(x)$ once for each node $x$ it removes, after the step that made $x$ unreachable, for example after the CAS of a pop. From then on, the node belongs to the reclamation scheme. The scheme calls $free(x)$, or a callback given with $x$, at some later time when its test says that no thread can still access $x$.

**The list.** Each thread usually keeps its own retire list, so that a retire is a plain append with no synchronization. Some schemes keep one list per epoch or per batch; some move full lists to a shared pool so that other threads can help free them.

**The batch.** The test has a cost that does not depend much on the number of nodes tested at once. With hazard pointers, it reads the $H = nK$ hazard pointers of $n$ threads with $K$ each; with epochs, it reads the epoch of every thread. So a thread runs the test only when its list reaches a threshold $R$, and then tests all its nodes together. If the test keeps at most $H$ nodes and $R \ge H + \Omega(H)$, each test frees $\Omega(R)$ nodes, so the cost per retire is $O(1)$ on average. This is the bound of the scan of hazard pointers.

**The trade-off.** A larger $R$ makes the test rarer and cheaper per node, but more nodes wait: up to $R$ per thread in the best case. A smaller $R$ frees sooner, but tests more often. The [garbage](/safe-memory-reclamation/), the number of retired nodes that are not yet freed, is the measure of the trade-off.

**What can stop the list from draining.**

- *A stalled thread.* With grace periods, a thread that stops inside an operation stops all grace periods, so no list drains, and the garbage grows without bound. With hazard pointers, it keeps only the nodes it names.
- *An idle thread.* With per-thread lists, a thread that stops retiring never reaches $R$, so its list is never tested. Schemes test at thread exit, hand the list to another thread, or test on a timer.
- *A thread that exits.* Its list must go somewhere, to a shared pool or to another thread, or the nodes leak.

**Who frees.** The retiring thread itself (hazard pointers and EBR in their usual form), a helper that takes lists from a shared pool, or a background thread that runs callbacks (call_rcu in Linux). Freeing in the retiring thread keeps the cost local; freeing in another thread keeps the cost out of the operations, but moves memory across caches.

## Examples

- **Hazard pointers.** A thread appends to its private list. When the list has $R$ nodes, it reads all hazard pointers into a set $H$, frees the nodes not in $H$, and keeps the others. The tests of the [hazard pointers](/hazard-pointers/) page measure the garbage on the [Treiber stack](/treiber-stack/) and the queue, with and without a stalled thread, and check that it stays at most $n R$.
- **Epoch-based reclamation.** A thread keeps one limbo list for each of the last three epochs. A node retired in epoch $e$ goes on the list of $e$. When the global epoch reaches $e + 2$, every thread has left the operations it was in at epoch $e$, so the list of $e$ is freed as a whole. The tests of the [epoch-based reclamation](/epoch-based-reclamation/) page show that this list grows without bound when one thread stalls inside an operation.
- **call_rcu.** In [read-copy-update](/read-copy-update/), an updater can wait for a grace period with synchronize_rcu and then free, or it can call call_rcu with the node and a callback, and go on at once. The kernel queues the callbacks and runs them after a grace period, in batches.
- **Reference counting with deferral.** In [Hyaline](/hyaline/), a batch of retired nodes gets one counter for all the threads that were active when it was retired, and the last thread to leave frees the batch. The list is shared, and the freeing is done by whoever leaves last.
- **Non-example: immediate free.** A pop that frees the node right after its CAS can free a node that another pop has just loaded. The tests of the scheme pages run this case as the broken baseline, and find a [use-after-free](/use-after-free/) in it.

## Where it is used

- In every manual reclamation scheme for lock-free structures: [hazard pointers](/hazard-pointers/), [epoch-based reclamation](/epoch-based-reclamation/), [quiescent-state-based reclamation](/quiescent-state-based-reclamation/), [DEBRA](/debra/) and their relatives all have a retire call and some form of retire list.
- In the Linux kernel, where call_rcu and kfree_rcu defer the free of an object until after a grace period.
- In libraries: the retire function of hazard pointers in Folly, call_rcu in the user-space RCU library liburcu, and defer_destroy in the crossbeam-epoch crate in Rust.
- In databases and file systems, where old versions of pages or index nodes wait until no reader can still see them.

## References
