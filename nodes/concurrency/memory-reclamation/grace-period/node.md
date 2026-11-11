---
tag: JJSRTK
kind: concept
slug: grace-period
name: Grace period
aliases: [quiescent period, RCU grace period]
area: concurrency/memory-reclamation
level: core
summary: An interval in which every thread passes through a quiescent state. Every reader that was active at its start has finished by its end, so a node removed before the start can be freed.
prereqs: [quiescent-state, deferred-reclamation]
see_also: [read-copy-update, epoch-based-reclamation, quiescent-state-based-reclamation, debra, safe-memory-reclamation, hazard-pointers, readers-writer-lock, hyaline]
sources:
  - paper: "Paul E. McKenney and John D. Slingwine, Read-copy update, using execution history to solve concurrency problems, Parallel and Distributed Computing and Systems (PDCS) 1998, pages 509-518"
    locator: the definition of a grace period as a period in which every thread passes through a quiescent state, and its use to free removed data
  - paper: "Paul E. McKenney, Exploiting deferred destruction: an analysis of read-copy-update techniques in operating system kernels, PhD thesis, OGI School of Science and Engineering at Oregon Health and Science University, 2004"
    locator: the implementations of grace-period detection and the batching of callbacks over one grace period
  - paper: doi:10.1109/TPDS.2011.159
    title: Mathieu Desnoyers, Paul E. McKenney, Alan S. Stern, Michel R. Dagenais and Jonathan Walpole, User-level implementations of read-copy update, IEEE Transactions on Parallel and Distributed Systems 23(2), 2012, pages 375-382
    locator: the grace-period guarantee, the user-space detection of grace periods with a global counter and per-thread counters, and the proof sketch
  - url: https://lwn.net/Articles/262464/
    title: Paul E. McKenney and Jonathan Walpole, What is RCU, fundamentally?, LWN.net, December 2007
    locator: the section on waiting for pre-existing RCU readers to complete, and the figure of the grace period
  - url: https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-579.pdf
    title: Keir Fraser, Practical lock-freedom, PhD thesis, University of Cambridge, Technical Report UCAM-CL-TR-579, 2004
    locator: the section on epoch-based garbage collection, in which two advances of the global epoch give the guarantee of a grace period
  - paper: doi:10.1016/j.jpdc.2007.04.010
    title: Thomas E. Hart, Paul E. McKenney, Angela Demke Brown and Jonathan Walpole, Performance of memory reclamation for lockless synchronization, Journal of Parallel and Distributed Computing 67(12), 2007, pages 1270-1285
    locator: the description of the schemes based on grace periods (quiescent-state-based and epoch-based reclamation) and the cost of a preempted thread
---

A **grace period** is an interval of time in which every thread passes through at least one [quiescent state](/quiescent-state/), a point at which it holds no reference to a shared node. Its key property is that every read-side critical section that was running when the grace period started has ended by the time it ends. A node that was removed from a data structure before the grace period started can only be held by such a section, so after the grace period it is safe to free. Grace periods are how [read-copy-update](/read-copy-update/), [quiescent-state-based reclamation](/quiescent-state-based-reclamation/) and [epoch-based reclamation](/epoch-based-reclamation/) decide when a retired node can be freed. They make reads almost free, because a reader only marks the start and the end of its section; the price is that one thread that stops inside a section stops every grace period, so the retired nodes pile up.

## In plain words

A museum wants to remove a painting. Some visitors are already in the room and may still be looking at it. New visitors are sent another way and will not see it.

So the museum does not wait for every visitor to leave the building. It waits only until each visitor who was in the room when the painting was taken down has left the room at least once. After that, nobody can still be looking at the painting, and it can be stored away.

The waiting time is the grace period. It does not matter who comes in later. But one visitor who falls asleep in the room keeps the museum waiting forever.

## The idea

**The definition.** Let $n$ threads run, and let each thread mark its read-side critical sections, the intervals in which it may hold references to shared nodes. An interval $[s, e]$ is a **grace period** if every thread that was inside a critical section at time $s$ has left that section by time $e$. Equivalently, every thread has a quiescent state in $[s, e]$, or is idle for the whole interval.

**Why it is enough.** A node $x$ is removed at time $r_x \le s$: from then on, it cannot be reached from the roots. A thread that starts a section after $s$ starts from the roots, so it never finds $x$. A thread whose section was running at $s$ may hold $x$, but by $e$ it has left that section and dropped its references. So after $e$, no thread holds $x$, and $x$ can be freed. This is the whole proof of safety for every grace-period scheme; the schemes differ only in how they detect that a grace period has passed.

**Waiting only for the old readers.** A grace period does not wait for all readers to be absent at once. New sections can start at any time and do not delay it. This is why a grace period always ends if every thread keeps making progress, even under a constant flow of readers.

**Detection.** The schemes find grace periods in different ways.

- *Counters per thread.* Each thread increments a private counter at each quiescent state. The reclaimer copies all counters at $s$ and waits until each has changed, or until the thread is offline. This is quiescent-state-based reclamation.
- *A global counter.* A reader copies a global counter $G$ into its own slot when it enters a section and clears the slot when it leaves. The reclaimer increments $G$ to a new value $g$ and waits until each slot is clear or at least $g$. This is the user-space RCU of Desnoyers and others, and the synchronous mode of the [read-copy-update](/read-copy-update/) page.
- *Epochs.* A reader announces the global epoch when it starts an operation. The epoch advances only when every active reader has announced the current one. Two advances after a removal form a grace period, because a reader that announced epoch $e$ blocks the move from $e + 1$ to $e + 2$. This is [epoch-based reclamation](/epoch-based-reclamation/) and [DEBRA](/debra/).
- *Scheduler events.* In a kernel in which RCU readers cannot be preempted, a context switch on every CPU is a grace period.

**Batching.** One grace period serves all the nodes removed before it started. So the reclaimer collects removed nodes on a [retire list](/deferred-reclamation/), and frees the whole list after one grace period. The cost of the detection, which reads the state of all $n$ threads, is then shared by many nodes.

**Synchronous or asynchronous.** An updater can wait for a grace period before it goes on (synchronize_rcu), which is simple and keeps the garbage small, but blocks the updater. Or it can register a callback that runs after a grace period (call_rcu), which never blocks, but lets the garbage grow while the grace period lasts.

**The weakness.** A thread that stops inside a section, by a crash, a page fault or preemption, holds back every grace period that starts after it entered. A synchronous updater then waits forever, and an asynchronous one keeps retiring nodes that are never freed. No bound on the garbage holds. Schemes such as [hazard pointers](/hazard-pointers/), the robust form of [Hyaline](/hyaline/) and DEBRA+ exist to avoid this.

## Examples

- **A removal from a list.** A reader enters a section at time 1 and reads node $B$. An updater unlinks $B$ at time 2 and starts a grace period at time 3. Another reader enters at time 4; it cannot find $B$. The first reader leaves at time 5. The grace period can end at 5, and $B$ is freed. The second reader may still be running; it does not matter.
- **Read-copy-update.** The tests of the [read-copy-update](/read-copy-update/) page run every interleaving of small runs with readers and an updater that replaces a shared value and frees the old one after a grace period. With the wait, no run has a use-after-free. Without the wait, a run is found in which a reader reads the freed old value.
- **A stalled reader.** The same tests stall one reader inside its section. The synchronous updaters block, and in the deferred mode, the garbage grows with the length of the run: 50 and 400 retired nodes, none freed. The tests of the [epoch-based reclamation](/epoch-based-reclamation/) and [quiescent-state-based reclamation](/quiescent-state-based-reclamation/) pages show the same growth on the stack and the queue.
- **Two epochs, not one.** A node retired in epoch $r$ may be held by a reader that announced $r$ and is still running in epoch $r + 1$. Freeing at $r + 1$ is too early; the move to $r + 2$ needs that reader to leave. So one epoch step is not a grace period, and two are.

## Where it is used

- The Linux kernel, where RCU protects read-mostly data such as routing tables, the list of tasks and many other lists, and grace periods are detected from context switches and other events.
- The user-space RCU library liburcu, with several ways to detect grace periods, and the RCU of the Folly library.
- Epoch-based reclamation in lock-free libraries such as the crossbeam-epoch crate in Rust.
- Databases and storage engines that keep old versions of pages or index nodes until all readers that started before a change have finished.
- As a building block in other schemes: [Hyaline](/hyaline/) and [interval-based reclamation](/interval-based-reclamation/) use per-batch or per-interval forms of the same guarantee.

## References
