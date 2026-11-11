---
tag: K7CR9Y
kind: algorithm
slug: debra
name: DEBRA
aliases: [distributed epoch-based reclamation, DEBRA+]
area: concurrency/memory-reclamation
level: research
summary: Epoch-based reclamation in which each operation checks one other thread instead of all of them, with three limbo bags per thread. DEBRA+ adds signals that make the garbage bounded.
solves: [safe-memory-reclamation]
complexity:
  vars: {n: the number of processes, K: the reservations per process in DEBRA+, T: the bag size that starts neutralization}
  space: {announcements: Θ(n), debra_plus_garbage: O(n (T + n K))}
  steps: {operation_overhead: O(1), rotation: O(n K)}
properties: {robust: false, robust_with_signals: true, bounded_garbage: false, per_node_cost: false}
history:
  year: 2015
  people: [Trevor Brown]
  note: Brown presented DEBRA and DEBRA+ at PODC 2015 together with a record manager interface that separates allocation, reclamation and data structure code.
prereqs: [epoch-based-reclamation]
see_also: [quiescent-state-based-reclamation, neutralization-based-reclamation, hazard-pointers, interval-based-reclamation, hazard-eras, read-copy-update]
sources:
  - paper: doi:10.1145/2767386.2767436
    title: Trevor Brown, Reclaiming memory for lock-free data structures, there has to be a better way, PODC 2015, pages 261-270
    locator: the sections on DEBRA (leaveQstate, enterQstate, the three limbo bags and the incremental check of one process per operation) and on DEBRA+ (neutralizing signals, recovery code and the bound on garbage)
  - url: https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-579.pdf
    title: Keir Fraser, Practical lock-freedom, PhD thesis, University of Cambridge, Technical Report UCAM-CL-TR-579, 2004
    locator: the epoch-based reclamation with three limbo lists that DEBRA distributes
  - paper: doi:10.1145/3437801.3441625
    title: Ajay Singh, Trevor Brown and Ali Mashtizadeh, NBR, neutralization based reclamation, PPoPP 2021, pages 175-190
    locator: the comparison with DEBRA+ and the simpler use of signals without recovery code in the write phase
---

DEBRA is a variant of [epoch-based reclamation](/epoch-based-reclamation/) by Trevor Brown in which no operation ever scans all threads. Each operation reads the global epoch, announces it, and checks just one other thread. When a thread has checked all $n$ threads in the current epoch, it tries to advance the epoch. Each thread keeps three limbo bags and frees the oldest one whenever it sees the epoch change. The cost per operation is a constant number of steps. Like any epoch scheme, plain DEBRA stops reclaiming when a thread stops inside an operation. DEBRA+ fixes this: a thread whose bags grow too large sends a signal to the slow thread, which then restarts its operation, so the garbage of each thread stays bounded.

## In plain words

A team works in shifts that are numbered on a board. When you start a task, you read the shift number and write it next to your name. Then you look at one teammate's name, the next one on your list. If they are on this shift or on a break, you tick them off.

When you have ticked off the whole team, you move the board to the next shift.

You keep three bins of old parts. Each time you see the shift number change, you empty your oldest bin and start filling it again. A part is only destroyed after three changes, so nobody can still hold it.

In the plus version, if your bins get too full, you tap the slow teammate on the shoulder. They drop what they hold and start their task again.

## The problem

[Safe memory reclamation](/safe-memory-reclamation/) for lock-free structures such as the [Treiber stack](/treiber-stack/) and the [Michael and Scott queue](/michael-scott-queue/), with as little work per operation as possible. Plain [epoch-based reclamation](/epoch-based-reclamation/) reads all $n$ announcements in each attempt to advance, and it has no bound on garbage when a thread stalls.

The model: $n$ asynchronous processes on a sequentially consistent shared memory with reads, writes and [compare-and-swap](/compare-and-swap/). $G$ is the global epoch. $A[p]$ is the announcement of $p$, a pair (epoch, quiescent). Each process has a private $seen$ epoch, a counter $checked$, and three bags. DEBRA+ also needs a way to interrupt a process, such as a POSIX signal, and $K$ reservation slots per process; $T$ is the bag size at which a process starts to send signals.

## The algorithm

```pseudo id=main
LEAVE_QSTATE()                        ▷ at the start of each operation
L1  e ← G
L2  if e ≠ seen then seen ← e; checked ← 0; rotate the three bags
L3      FREE every node of the new current bag, except reserved ones (DEBRA+)
L4  A[me] ← (e, false)
L5  (f, quiet) ← A[checked]; ok ← quiet or f = e
L6  if not ok and DEBRA+ and |bags| ≥ T then SIGNAL(checked); ok ← true
    if ok then checked ← checked + 1
L7      if checked = n then
L8          CAS(G, e, e + 1); checked ← 0
RETIRE(x)                             ▷ x is already unlinked
L9  current bag ← current bag ∪ {x}
ENTER_QSTATE()                        ▷ at the end of each operation
L10 A[me] ← (seen, true)
```

The check at L5 looks at one process per operation, in a fixed round-robin order. A round is the $n$ checks that a process makes while it sees one epoch $e$. If all of them pass, every process was quiescent or had announced $e$ at some time after $G$ became $e$, so the compare-and-swap at L8 is safe. A round that fails on process $q$ stays at $q$ and tries it again at the next operation.

There is no re-read of $G$ after L4, unlike in EBR, so an announcement can be stale. That is why DEBRA keeps three bags and not two. A node retired by $p$ goes into the bag of the epoch that $p$ last saw, but the real epoch at the retire can be one higher. Three rotations of $p$ mean that the epoch has moved at least twice after the retire, and an operation that could hold the node keeps the epoch at most one above its announcement.

**DEBRA+.** An operation has a read phase, in which it only reads shared memory, and a write phase, in which it changes it. When a process holds at least $T$ nodes and its check of $q$ fails, it signals $q$ at L6 and counts $q$ as passed. If $q$ is in its read phase, the signal handler jumps back to the start of the operation, and $q$ announces again before it reads anything. If $q$ is in its write phase, it goes on; before it entered that phase, it wrote the nodes it will use into its reservation slots, and L3 does not free reserved nodes. Brown's version runs recovery code in the handler that may help the interrupted operation; the version here restarts it.

## Example

Two processes. Process 1 pops five nodes; process 0 pops once and pauses just before it reads $top.next$. This is the run that the test uses to show why two bags are not enough.

| step | process | line | action | state after |
|---|---|---|---|---|
| 1 | 1 | L1 to L8, pop | first pop: checks process 0 (quiescent), retires $X_1$ | $checked_1 = 1$ |
| 2 | 1 | L1 to L8 | second pop: checks itself, $checked_1 = 2 = n$, CAS $G$ from 0 to 1 | $G = 1$, $seen_1 = 0$ |
| 3 | 0 | L1 to L5 | sees $G = 1$, announces $(1, \text{false})$; reads $top = X_2$ | |
| 4 | 1 | pop, L9 | pops $X_2$ and puts it in the bag of $seen_1 = 0$ | bags: $\{X_1, X_2\}, \{\}, \{\}$ |
| 5 | 1 | L1 to L3 | third pop: sees 1, rotates, frees the empty oldest bag | $seen_1 = 1$ |
| 6 | 1 | L5 | checks process 0: $(1, \text{false})$ is current, passes | $checked_1 = 1$ |
| 7 | 1 | L5 to L8 | fourth pop: checks itself, CAS $G$ from 1 to 2 | $G = 2$ |
| 8 | 1 | L1 to L3 | fifth pop: sees 2, rotates; the bag with $X_2$ is the oldest of three, not yet freed | |
| 9 | 0 | pop | reads $X_2.next$ and $X_2.val$ safely | |

With two bags, step 8 rotates back to the bag that holds $X_2$ and frees it, while process 0, which announced epoch 1, is about to read it; the test finds the use after free at step 9. The node was retired when $G$ was 1, but it went into the bag of epoch 0, and only one more epoch had passed.

## Correctness

The full proof is in proofs/correctness.md.

- **Key fact.** An operation whose announcement was written when $G = g_0$ keeps $G \le g_0 + 1$ until it ends, because the round that would move $G$ to $g_0 + 2$ checks it after $G$ became $g_0 + 1$ and sees a smaller epoch.
- **Three rotations.** A node retired when $G = g_r$ is freed only after its owner has seen three new epochs since then, so $G \ge g_r + 2$; an operation that can hold the node had $g_0 \le g_r$, so it has ended.
- **DEBRA+.** A signalled process takes no step between the signal and its handling, so its accesses before the signal come before the free. In the read phase it restarts; in the write phase it uses only reserved nodes, and their reservations were written before the signal and are seen by the free.
- **Bound.** With DEBRA+, if each operation retires at most one node, each process holds at most $T + 3(n + 1) + 3nK$ nodes.

The test file checks every interleaving of small stack and queue runs with two and three processes for DEBRA, and with two processes for DEBRA+ with $T = 1$, where every failed check sends a signal. It runs 60 seeded random schedules of each kind for DEBRA and DEBRA+, and two scripted runs that break wrong versions: two bags instead of three, and a DEBRA+ process that ignores the signal and reads a node that was freed after it was counted as quiescent.

## Complexity

| measure | value |
|---|---|
| shared space | $G$ and $n$ announcements; DEBRA+ adds $nK$ reservations and $n$ signal flags |
| overhead per operation | $O(1)$ steps: one read of $G$, one announcement, one check, at most one CAS |
| rotation | frees one bag; DEBRA+ reads $nK$ reservations first |
| unfreed nodes, DEBRA | not bounded if a process stops inside an operation |
| unfreed nodes, DEBRA+ | at most $n (T + 3(n + 1) + 3nK)$ |

**Cost per operation.** EBR reads all $n$ announcements in each attempt to advance. DEBRA spreads this work: one announcement per operation, so a round of $n$ checks costs $n$ operations of the checker. An advance therefore needs at least $n$ operations, which makes epochs longer, but every operation pays the same small cost and no scan is ever needed.

**Garbage under a stall.** With three processes, 400 operations each, and process 0 stopped inside its first pop, plain DEBRA keeps every node that the two others retire: the peak is 400. DEBRA+ with $T = 8$ keeps a peak of 20, below the bound $3 (8 + 12 + 18) = 114$.

## Properties

- Plain DEBRA is not robust: a stalled operation holds the epoch.
- DEBRA+ is robust if the operating system delivers signals, and if the data structure can restart an operation in its read phase.
- No cost per node read, and $O(1)$ steps per operation.
- Bags are freed in whole batches, which suits a pool allocator: Brown's record manager moves a full bag to a shared pool in $O(1)$ steps.
- DEBRA+ adds a write per reserved pointer to the start of each write phase.

## Variants and improvements

- **[Epoch-based reclamation](/epoch-based-reclamation/).** The original scheme scans all announcements and has no per-operation check.
- **[Quiescent-state-based reclamation](/quiescent-state-based-reclamation/).** No announcement at the start of an operation, only reports of quiescence.
- **[Neutralization-based reclamation](/neutralization-based-reclamation/).** Singh, Brown and Mashtizadeh (2021) keep the signals of DEBRA+ but publish reservations in the style of hazard pointers and need no recovery code, which makes the scheme easy to apply to many structures.
- **[Interval-based reclamation](/interval-based-reclamation/) and [hazard eras](/hazard-eras/).** These bound the garbage without signals, at the cost of a per-node check of a birth epoch.

## When to use it

Use DEBRA where you would use EBR and the number of threads is large, so that a full scan of announcements is costly. Use DEBRA+ when the garbage must stay bounded under stalls and the operations of the data structure split cleanly into a read phase and a write phase, and when your platform can deliver signals to threads.

## Pitfalls

**Two bags instead of three.** The wrong code rotates over two bags at L2 and L3, so a node is freed one epoch change after the bag stops being current. The node may have been retired when $G$ was already one above $seen$, and then only one epoch has passed. The right code keeps three bags. The test shows the use after free with a scripted schedule.

**Ignoring the signal.** The wrong code counts a process as passed at L6 but lets it go on in its read phase with the pointers it had. The right code makes it drop all pointers and start the operation again from L1.

**No reservations in the write phase.** A process that is signalled in its write phase keeps using its pointers. Without the reservations that L3 respects, the nodes it writes through can be freed under it.

**Retiring many nodes per operation.** The bound of DEBRA+ grows with the number of retires between rotations. A structure that retires a whole chain of nodes in one operation needs a larger bound or a scan per retire.

## Implementations

## History

Trevor Brown presented DEBRA and DEBRA+ at PODC 2015, in a paper that also introduced a record manager abstraction separating allocation, reclamation and data structure code, and measured both schemes against hazard pointers and EBR on several lock-free trees and lists. DEBRA was among the fastest schemes in those benchmarks. NBR (Singh, Brown and Mashtizadeh, PPoPP 2021) later reused the idea of neutralizing signals in a form that needs no per-structure recovery code.

## References
