---
tag: 0AQA6S
kind: technique
slug: read-copy-update
name: Read-copy-update
aliases: [RCU]
area: concurrency/memory-reclamation
level: core
summary: Readers run with no locks and no waits. A writer copies the data, changes the copy, publishes it with one pointer write, and frees the old version after a grace period.
prereqs: [grace-period, readers-writers-problem]
see_also: [quiescent-state-based-reclamation, epoch-based-reclamation, quiescent-state, deferred-reclamation, readers-writer-lock, hazard-pointers, debra, safe-memory-reclamation]
sources:
  - paper: "Paul E. McKenney and John D. Slingwine, Read-copy update: using execution history to solve concurrency problems, Parallel and Distributed Computing and Systems (PDCS) 1998"
    locator: the description of the method, the quiescent states and the grace period, and the uses in the DYNIX/ptx kernel
  - paper: "Paul E. McKenney, Exploiting deferred destruction: an analysis of read-copy-update techniques in operating system kernels, PhD thesis, OGI School of Science and Engineering at Oregon Health and Science University, 2004"
    locator: the chapters on the RCU interface, the implementations of grace-period detection, and the design patterns for RCU
  - paper: doi:10.1109/TPDS.2011.159
    title: Mathieu Desnoyers, Paul E. McKenney, Alan S. Stern, Michel R. Dagenais and Jonathan Walpole, User-level implementations of read-copy update, IEEE Transactions on Parallel and Distributed Systems 23(2), 2012, pages 375-382
    locator: the general-purpose user-space RCU with a global counter and a per-thread counter, and the proof sketch of the grace-period guarantee
  - url: https://lwn.net/Articles/262464/
    title: Paul E. McKenney and Jonathan Walpole, What is RCU, fundamentally?, LWN.net, December 2007
    locator: the publish-subscribe mechanism, the wait for pre-existing readers, and the multiple versions that readers can see
  - url: https://www.kernel.org/doc/html/latest/RCU/whatisRCU.html
    title: Paul E. McKenney, What is RCU?, the Linux kernel documentation
    locator: the core API (rcu_read_lock, rcu_read_unlock, synchronize_rcu, call_rcu, rcu_assign_pointer, rcu_dereference) and the toy implementations
  - paper: doi:10.1016/j.jpdc.2007.04.010
    title: Thomas E. Hart, Paul E. McKenney, Angela Demke Brown and Jonathan Walpole, Performance of memory reclamation for lockless synchronization, Journal of Parallel and Distributed Computing 67(12), 2007
    locator: the comparison of quiescent-state-based reclamation, epoch-based reclamation, hazard pointers and reference counting
---

**Read-copy-update** (RCU) is a way to share read-mostly data between threads. Readers take no lock and never wait. A writer that wants to change a node does not change it in place. It makes a copy, changes the copy, and publishes the copy with one pointer write. Readers that start after the write see the new version; readers that started before may still see the old one. The writer then waits for a [grace period](/grace-period/), a time after which every reader that was running at the write has finished, and only then frees the old version. RCU came from the DYNIX/ptx kernel and is a core part of the Linux kernel. Its reclamation half is [quiescent-state-based reclamation](/quiescent-state-based-reclamation/) or a close relative, so RCU is also a [safe memory reclamation](/safe-memory-reclamation/) method.

## In plain words

A notice board shows the train times. Many people read it all day, and once a week the times change.

The clerk does not scrape the old paper off while people read it. The clerk prints a new sheet, pins it over the old one in one move, and waits.

People who walked up after the new sheet went up read the new times. People who were already reading still read the old sheet in their hand, and that is fine for a short time.

When every person who was reading at the moment of the change has walked away, the clerk throws the old sheet away. Readers never have to wait for the clerk, and the clerk never pulls a sheet from someone's hand.

## When it applies

- **Many reads, few writes.** The cost moves from the readers to the writers. A read-side section costs almost nothing, while an update costs a copy and a wait.
- **Readers can live with a slightly old version.** A reader that started before an update may finish with the old data. That is fine for routing tables, configuration, lists of modules and other data where each read only needs one consistent version.
- **The change can be made by one pointer write.** The new version is built off to the side and then made visible with one store, so that a reader sees either all of the old version or all of the new one.
- **Readers do not block inside a read-side section, or block only briefly.** The grace period waits for every reader that is inside a section. A reader that sleeps or stops there holds back every grace period, and with it all reclamation.
- **There is a cheap way to see that a reader has finished.** In a kernel, a context switch is a natural [quiescent state](/quiescent-state/). In user space, each reader keeps a counter, as in the template below.

## The template

The shared word $cfg$ points to the current version. $G$ is a global counter that starts at 1. $R[t]$ is the word of reader $t$; it is 0 when $t$ is outside a read-side section.

```pseudo id=main
READ-LOCK(t)
L1  g ← G
L2  R[t] ← g                           ▷ t is in a section that began in period g
READ-UNLOCK(t)
L3  R[t] ← 0
READER(t)
    READ-LOCK(t)
L4  p ← cfg                             ▷ subscribe: read the current version
L5  use p                               ▷ hole: the read-side work, which must not block
    READ-UNLOCK(t)
SYNCHRONIZE()
L6  g ← FETCH-AND-ADD(G, 1) + 1
L7  for each reader q: wait until R[q] = 0 or R[q] ≥ g
UPDATE()                                ▷ updaters hold a lock among themselves
    old ← cfg
L8  new ← a copy of old, changed        ▷ hole: the change
L9  cfg ← new                           ▷ publish with one write
    SYNCHRONIZE()
L10 free old                            ▷ hole: or hand old to a callback (call_rcu)
```

The holes are the read-side work at L5, the change at L8, and what happens to the old version at L10. The grace-period detection in L1 to L3, L6 and L7 is the user-space form with a global counter; a kernel replaces it with its own detection of quiescent states.

**Walk-through.** A reader marks itself at L1 and L2 with the period it saw, reads the pointer at L4, uses the version at L5, and clears its mark at L3. It never waits and never writes a word that another reader writes. The updater builds the new version at L8 and publishes it at L9; from then on, a reader that reads $cfg$ gets the new version. At L6 the updater starts a new period $g$, and at L7 it waits for each reader that is still in a section that began before $g$. A reader that shows 0 is outside any section, and a reader that shows a value of at least $g$ began its section after L6 and so after L9. When L7 ends, no reader can still hold the old version, and L10 frees it.

**Why it is safe.** Let reader $q$ read the old version at L4. Then that read came before L9, so $q$ read $G$ at L1 before L6 and wrote a value $s \le g - 1$ at L2. When the updater looks at $R[q]$ at L7, after L9, it sees $s$ while $q$ is still in that section. It sees 0 only before L2 or after L3; before L2 is not possible, because then $q$'s read at L4 would come after L9. It sees a value of at least $g$ only from a later section. So the wait ends only after $q$ left the section in which it read the old version. The full proof is in proofs/correctness.md.

**Cost.** READ-LOCK and READ-UNLOCK are one read and two writes of a word that only $t$ writes. In a kernel with non-preemptible sections they compile to nothing at all. SYNCHRONIZE is one fetch-and-add and one read per reader, plus the wait, which lasts as long as the longest read-side section that was running at L6. Memory: one word per reader, and the old versions that wait for their grace period.

**Example.** Reader $r$ and updater $u$. The version $A$ holds $v_0$, and $u$ replaces it by $B$ with $v_1$.

| step | process | line | action | state after |
|---|---|---|---|---|
| 1 | $r$ | L1, L2 | reads $G = 1$, writes $R[r] = 1$ | $r$ in a section |
| 2 | $r$ | L4 | reads $cfg = A$ | |
| 3 | $u$ | L8 | makes $B$, a copy of $A$ with $v_1$ | |
| 4 | $u$ | L9 | writes $cfg = B$ | new readers see $B$ |
| 5 | $u$ | L6 | $G = 2$, so $g = 2$ | |
| 6 | $u$ | L7 | $R[r] = 1$: not 0 and less than 2, so waits | |
| 7 | $r$ | L5 | reads $A.val = v_0$, safe | |
| 8 | $r$ | L3 | writes $R[r] = 0$ | |
| 9 | $u$ | L7 | $R[r] = 0$, the wait ends | |
| 10 | $u$ | L10 | frees $A$ | |

If $u$ freed $A$ at step 5 without the wait, then step 7 would read freed memory. The test file finds this run.

## Classic examples

- [Readers-writer locks](/readers-writer-lock/) for read-mostly data: RCU replaces the reader side of the lock by L1 to L3, so readers no longer write a counter that all of them share. This is the most common use in the Linux kernel.
- [Treiber stack](/treiber-stack/) and [Michael and Scott queue](/michael-scott-queue/): each operation is a read-side section, and after it the process waits for a grace period and frees the node it removed. The implementation on this page runs both on the simulator.
- [Harris linked list](/harris-linked-list/) and other linked structures: readers walk the list inside a read-side section with no protection per node, and a removed node is freed after a grace period. In the kernel the updaters of an RCU list usually take a lock among themselves.
- [Quiescent-state-based reclamation](/quiescent-state-based-reclamation/): the same grace-period idea, with the end of an operation as the quiescent state and no wait in the updater.

## Variations

- **Deferred freeing (call_rcu).** The updater does not wait at L7. It hands the old version to a callback that runs after the grace period. Updates no longer block, but a reader that stops inside a section lets the waiting versions grow without bound. The implementation has this mode, and the test measures it.
- **Kernel RCU.** With non-preemptible read-side sections, a context switch, the idle loop or user mode is a quiescent state for the CPU, so READ-LOCK and READ-UNLOCK need no code. A grace period ends when every CPU has passed a quiescent state.
- **Preemptible RCU and SRCU.** For real-time kernels, a reader can be preempted inside its section, so the section must be counted. Sleepable RCU (SRCU) lets readers sleep and keeps grace periods separate for each domain.
- **User-space RCU.** The template above is close to the general form of the liburcu library: a global counter and a per-thread counter, with memory barriers on both sides. Other forms of liburcu use signals or quiescent states to move the barriers away from the readers.
- **[Epoch-based reclamation](/epoch-based-reclamation/).** The same idea with a global epoch that advances when all active threads have seen it, used in lock-free structures in place of a kernel grace period.

## Pitfalls

- **Freeing before the grace period.** The wrong code frees the old version right after L9. A reader that read $cfg$ just before L9 still uses it. The right code runs SYNCHRONIZE between L9 and L10. The test finds this run.
- **A pointer kept after the section.** A reader that saves $p$ from L4 and uses it after L3 is not protected. The rule is that pointers read in a section are only used in that section.
- **Blocking in a read-side section.** A reader that sleeps, or that calls SYNCHRONIZE itself, inside its section blocks every grace period. If the reader calls SYNCHRONIZE inside its own section, it waits for itself forever.
- **A stopped reader.** In synchronous mode, all updaters stop at L7; in deferred mode, the garbage grows. The test shows both, on the stack and on the queue with three processes. When process 0 stops inside its section, the two others block at L7 after one removal each. In deferred mode they go on, but they free nothing: when each of them runs 50 or 400 operations, 50 or 400 removed nodes stay unfreed.
- **Publishing a node that is not ready.** On a weak memory model, the writes that fill in $new$ at L8 must be visible before the pointer write at L9. The kernel uses rcu_assign_pointer, a store with release order, and readers use rcu_dereference.
- **Several updaters at once.** The template assumes that updaters exclude each other. Two updaters that both copy $old$ and publish lose one of the two changes.
- **An update that needs two pointer writes.** If a reader can see the first write and not the second, it can see a state that never existed. Build the whole new version off to the side, and publish it with one write.

## References
