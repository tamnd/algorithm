---
tag: VTXVR8
kind: definition
slug: quiescent-state
name: Quiescent state
aliases: [quiescent point, extended quiescent state]
area: concurrency/memory-reclamation
level: core
summary: A point in the run of a thread at which it holds no reference to a shared node, so that every node it uses later is reached again from the roots of the structure.
prereqs: [safe-memory-reclamation]
see_also: [grace-period, quiescent-state-based-reclamation, read-copy-update, epoch-based-reclamation, deferred-reclamation, debra, critical-section, hazard-pointers]
sources:
  - paper: "Paul E. McKenney and John D. Slingwine, Read-copy update, using execution history to solve concurrency problems, Parallel and Distributed Computing and Systems (PDCS) 1998, pages 509-518"
    locator: the definitions of a quiescent state, a quiescent period and a grace period, and the examples of quiescent states in a kernel (a context switch, the idle loop, user mode)
  - paper: "Paul E. McKenney, Exploiting deferred destruction: an analysis of read-copy-update techniques in operating system kernels, PhD thesis, OGI School of Science and Engineering at Oregon Health and Science University, 2004"
    locator: the definitions of quiescent states and grace periods, and the ways to detect quiescent states
  - paper: doi:10.1109/TPDS.2011.159
    title: Mathieu Desnoyers, Paul E. McKenney, Alan S. Stern, Michel R. Dagenais and Jonathan Walpole, User-level implementations of read-copy update, IEEE Transactions on Parallel and Distributed Systems 23(2), 2012, pages 375-382
    locator: the quiescent-state-based user-space RCU, in which a thread announces its quiescent states and marks itself offline for an extended quiescent state
  - paper: doi:10.1016/j.jpdc.2007.04.010
    title: Thomas E. Hart, Paul E. McKenney, Angela Demke Brown and Jonathan Walpole, Performance of memory reclamation for lockless synchronization, Journal of Parallel and Distributed Computing 67(12), 2007, pages 1270-1285
    locator: the definitions of quiescent states and grace periods used for quiescent-state-based and epoch-based reclamation
---

A **quiescent state** of a thread is a point in its run at which it holds no reference to any shared node of a concurrent data structure. A pointer that the thread loaded before the point is not used after it; any node it uses later, it reaches again from the roots. A removed node cannot be reached from the roots, so after a quiescent state, the thread can never access a node that was removed before it. If every thread has passed a quiescent state since a node was removed, the node is safe to free; the interval in which this happens is a [grace period](/grace-period/). Quiescent states are the basis of [read-copy-update](/read-copy-update/), [quiescent-state-based reclamation](/quiescent-state-based-reclamation/) and, in the form of the time between operations, of [epoch-based reclamation](/epoch-based-reclamation/).

## Definition

Take a run of a program with threads that share a data structure, and a set of **roots**: the shared variables from which the structure is reached, such as $top$ of a stack. A thread holds a **reference** to a shared node at time $\tau$ if it has, in a local variable or a register, a pointer to the node that it obtained before $\tau$ and may still use after $\tau$.

A point $\tau$ in the run of thread $t$ is a **quiescent state** of $t$ if $t$ holds no reference to a shared node at $\tau$. Equivalently, every pointer to a shared node that $t$ uses after $\tau$ was obtained after $\tau$, by a chain of reads that starts at a root.

An interval $[\tau_1, \tau_2]$ is an **extended quiescent state** of $t$ if every point in it is a quiescent state, that is, $t$ makes no access to the structure in the interval. A thread that is idle, blocked or offline is in an extended quiescent state.

The complement is a **read-side critical section**: a maximal interval in which the thread may hold references. In a scheme, the code marks the bounds of these sections, and the points outside them are the quiescent states that the scheme can see.

A quiescent state is a property of the program, not of the time: whether $\tau$ is quiescent depends on what the thread does after $\tau$. A scheme cannot observe it directly, so the program must announce it, for example by a call at a known point, or by leaving a section that the scheme tracks.

## Examples and non-examples

- **Example: between two operations.** A thread that runs the operations of a [Treiber stack](/treiber-stack/) and keeps no pointer from one operation to the next is in a quiescent state after each operation ends and before the next begins. Each pop starts again at $top$.
- **Example: a context switch in a kernel.** In a kernel in which code that reads RCU-protected data cannot be preempted, a CPU that does a context switch holds no reference to such data. Linux and the DYNIX/ptx kernel count context switches, the idle loop and running in user mode as quiescent states of a CPU.
- **Example: an explicit call.** In the quiescent-state-based flavor of the user-space RCU library, a thread calls a function to announce a quiescent state, at a point that the programmer knows to be safe, such as the top of an event loop.
- **Example: an offline thread.** A thread that is about to block for a long time marks itself offline. The whole time it is offline is an extended quiescent state, so it does not hold up grace periods.
- **Non-example: in the middle of a pop.** A thread that has read $top = A$ and is about to read $A.next$ holds a reference to $A$. The point between the two reads is not quiescent.
- **Non-example: a pointer kept across operations.** A thread that saves a pointer to a node in a cache, and uses it in its next operation, is not in a quiescent state between the operations, even though no operation is running. A scheme that counts the end of each operation as quiescent would free the node too early.
- **Non-example: a stalled thread inside an operation.** A thread that stops inside an operation never reaches its next quiescent state. No grace period that started before it stopped can end, which is why grace-period schemes are not robust.

## Related definitions

- **[Grace period](/grace-period/).** An interval in which every thread passes through at least one quiescent state, or stays in an extended quiescent state. A node removed before a grace period starts can be freed after it ends.
- **Read-side critical section.** The interval in which a thread may hold references; quiescent states are the points outside such sections. It is the counterpart, for readers, of a [critical section](/critical-section/) under a lock, but it excludes only reclamation, not other threads.
- **Epoch.** In [epoch-based reclamation](/epoch-based-reclamation/) and [DEBRA](/debra/), a thread announces the global epoch at the start of each operation and the end of the operation is a quiescent state. The epoch advances only when every active thread has announced it, which is a way of detecting grace periods.
- **Hazard pointer.** [Hazard pointers](/hazard-pointers/) track references one node at a time instead of quiescent states. A thread with all hazard pointers clear and no unprotected pointers is in a quiescent state, but the scheme never needs to know this.
- **[Quiescent-state-based reclamation](/quiescent-state-based-reclamation/).** The scheme in which threads announce quiescent states and a node is freed after a grace period.

## References
