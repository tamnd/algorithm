---
tag: YFEJH1
kind: algorithm
slug: mcs-lock
name: MCS lock
aliases: [Mellor-Crummey-Scott lock]
area: concurrency/mutual-exclusion
level: advanced
summary: A FIFO queue lock built as a linked list. A process joins with one swap on the tail and spins on a flag in its own node, so a passage makes O(1) remote references in both CC and DSM.
solves: [mutual-exclusion-problem]
complexity:
  space: {shared: Θ(1)}
  steps: {solo: Θ(1)}
  rmr: {cc: O(1), dsm: O(1)}
properties: {deterministic: true, deadlock_free: true, starvation_free: true, fcfs: true, local_spinning: true}
history:
  year: 1991
  people: [John M. Mellor-Crummey, Michael L. Scott]
  note: Mellor-Crummey and Scott published the list-based queue lock in ACM TOCS in 1991, with a version that needs only fetch-and-store. It won the Dijkstra Prize in 2006.
prereqs: [spin-lock, rmr-complexity]
see_also: [clh-lock, anderson-lock, ticket-lock, cohort-lock, compare-and-swap, rmr-complexity, readers-writer-lock, spin-lock]
sources:
  - paper: doi:10.1145/103727.103729
    title: John M. Mellor-Crummey and Michael L. Scott, Algorithms for scalable synchronization on shared-memory multiprocessors, ACM Transactions on Computer Systems 9(1), 1991, pages 21-65
    locator: Section 2.4, the list-based queuing lock with fetch-and-store and compare-and-swap, and the version with fetch-and-store only
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 7, Spin Locks and Contention, Section 7.5.3, the MCS queue lock
  - paper: doi:10.1007/s00446-003-0088-6
    title: James H. Anderson, Yong-Jik Kim and Ted Herman, Shared-memory mutual exclusion, major research trends since 1986, Distributed Computing 16(2-3), 2003, pages 75-110
    locator: the section on local-spin algorithms, the CC and DSM models, and the MCS lock as an O(1) RMR algorithm
---

The MCS lock is a queue lock in which the waiting processes form a linked list. Each process brings a node with a flag $locked$ and a pointer $next$. A shared pointer $tail$ points to the last node. To join, a process swaps its node into $tail$ with one fetch-and-store and links itself behind the old tail. It then spins on the flag in its own node, and its predecessor clears that flag when it leaves. Because each process spins on its own node, which can live in its own memory, a passage makes $O(1)$ remote memory references in both the cache coherent (CC) and the distributed shared memory (DSM) models.

## In plain words

People wait in a line, but nobody needs to see the front. When you arrive, you take the name of the last person in line and write your own name in its place on a board. Then you tell that person: "I am behind you". You sit at your own desk and watch your own lamp.

When the person in front of you is done, they turn on your lamp. So you are woken by the one person in front of you, and nobody else is disturbed.

If you are done and nobody stands behind you, you erase your name from the board. If somebody has just written a name there but has not told you yet, you wait a moment for them to say "I am behind you", and then you turn on their lamp.

## The problem

The [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes with first come, first served order, and with $O(1)$ remote memory references (RMRs) per passage in both models of [RMR complexity](/rmr-complexity/). The model is $n$ asynchronous processes on a sequentially consistent shared memory, with atomic registers (consensus number 1), fetch-and-store, which is swap (consensus number 2), and [compare-and-swap](/compare-and-swap/) (consensus number $\infty$). The number $n$ need not be known.

## The algorithm

$tail$ is a shared pointer, $nil$ at the start. The node $I$ of a process has the fields $I.locked$ and $I.next$; in the DSM model it lives in the memory module of its process.

```pseudo id=main
LOCK(I)                                    ▷ I is the node of the caller
L1  I.next ← nil
L2  pred ← FETCH-AND-STORE(tail, I)         ▷ the doorway: one swap
L3  if pred ≠ nil then
L4      I.locked ← true
L5      pred.next ← I                      ▷ link behind the predecessor
L6      while I.locked do nothing           ▷ spin on the own node
UNLOCK(I)
L7  succ ← I.next
L8  if succ = nil then
        if COMPARE-AND-SWAP(tail, I, nil) then return   ▷ nobody waits
L9      repeat succ ← I.next until succ ≠ nil          ▷ a successor is linking
L10 succ.locked ← false                     ▷ hand over
```

L2 puts the caller at the end of the queue in one atomic step. That is the doorway, and the order of L2 steps is the order of service. L4 must come before L5, because once the predecessor sees the link it may clear the flag at once. L6 spins on the caller's own node. In the exit section, L8 handles the race between a holder that thinks it is alone and a newcomer that has swapped itself into $tail$ but not yet linked: the compare-and-swap fails, and the holder waits at L9 for the link. Only L9 waits in the exit section, and it waits for a process that is in its doorway.

**The version without compare-and-swap.** Mellor-Crummey and Scott also give an exit section that uses only fetch-and-store. If $I.next = nil$, the holder swaps $nil$ into $tail$. If the old value was $I$, it is done. Otherwise it has removed processes from the queue by mistake, so it swaps the old tail back, and the processes that arrived in between (the "usurpers") are linked in front of the removed ones. This version is still correct and deadlock free, but it no longer keeps FIFO order, and the authors note that starvation becomes possible in theory. It is not implemented here.

## Example

Process 1 arrives while process 0 is inside, and the release of process 0 races with the link of process 1.

| step | process | line | action | $tail$ | note |
|---|---|---|---|---|---|
| start | | | | nil | |
| 1 | 0 | L1, L2 | swap returns nil | 0 | enters at once |
| 2 | 1 | L1, L2 | swap returns 0 | 1 | |
| 3 | 1 | L4 | $locked_1 \leftarrow$ true | 1 | |
| 4 | 0 | L7 | reads $next_0 = nil$ | 1 | |
| 5 | 0 | L8 | CAS($tail$, 0, nil) fails | 1 | someone has joined |
| 6 | 0 | L9 | reads $next_0 = nil$ | 1 | waits for the link |
| 7 | 1 | L5 | $next_0 \leftarrow 1$ | 1 | |
| 8 | 0 | L9 | reads $next_0 = 1$ | 1 | |
| 9 | 0 | L10 | $locked_1 \leftarrow$ false | 1 | hands over |
| 10 | 1 | L6 | reads false, enters | 1 | |
| 11 | 1 | L7, L8 | $next_1 = nil$, CAS($tail$, 1, nil) succeeds | nil | the queue is empty |

Process 1 read only its own node while it waited. Process 0 waited at step 6 only for a process that was between L2 and L5.

## Correctness

The full proof is in proofs/correctness.md. It uses the *queue* $Q$: the processes in the order of their L2 steps, from the L2 step of each process until its successful compare-and-swap at L8 or its handover at L10.

- **Invariant.** $tail$ is the last process of $Q$, or $nil$ if $Q$ is empty. For two neighbors $p, q$ in $Q$, either $p.next = q$, or $q$ has not done L5 yet and $p.next = nil$. Only the first process of $Q$ (the *head*) can be past L6.
- **Mutual exclusion.** A process enters only as the head of $Q$, and $Q$ has one head.
- **FIFO.** The order of $Q$ is the order of the L2 steps, and the head leaves $Q$ only by handing over to its successor in $Q$.
- **Starvation freedom.** The exit section waits only at L9, for a process that is between L2 and L5 and so finishes L5 in a bounded number of its own steps.
- **Remote references.** At most 8 per passage in the CC model and at most 4 in the DSM model.

The test file checks mutual exclusion and FIFO order over all interleavings for two processes with two passages and for three processes, checks starvation freedom for two processes that run forever, and measures the maximum cost of a passage: 8 in the CC model, and 2 or 4 in the DSM model (process 0 owns the module of $tail$, so its swap is local).

## Complexity

| measure | value |
|---|---|
| shared space | one pointer per lock, one node of two words per process for each lock it holds or waits for |
| steps without contention | 4: L1, L2, then L7 and a successful CAS at L8 |
| RMRs per passage, CC model | at most 8 |
| RMRs per passage, DSM model | at most 4 |
| bypass after the doorway | 0 |

**CC count.** In the CC model a write or an atomic step is at most one RMR, and a read is an RMR only if it misses. The entry section makes at most 5: L1, L2, L4 and L5, and one miss in L6, because $I.locked$ is written by the caller at L4 and then only once by the predecessor at L10. The exit section makes at most 3: either a miss at L7 (the successor has written $I.next$) and the write of L10; or a hit at L7, the CAS of L8, one miss in L9 when the successor writes $I.next$, and the write of L10.

**DSM count.** The node of a process is local, so L1, L4, L6, L7 and L9 are local. The remote steps are the swap of L2 and the write to the predecessor's node at L5 in the entry section, and the CAS of L8 and the write to the successor's node at L10 in the exit section: at most 4. This is optimal up to a constant. With fetch-and-store, $O(1)$ RMRs per passage is possible; with reads, writes and compare-and-swap alone, some passage must make $\Omega(\log n)$ RMRs (Attiya, Hendler and Woelfel 2008). See [RMR complexity](/rmr-complexity/).

## Properties

- Uses one fetch-and-store per entry, and one compare-and-swap in some exits.
- Deadlock free, starvation free and FCFS, with bypass 0 after a doorway of one swap.
- Local spinning in both the CC and the DSM model.
- $O(1)$ space per lock, plus one node per waiting process; $n$ need not be known.
- The exit section is not wait free: it can wait at L9 for a slow newcomer. The time is bounded by the newcomer's steps, not by the critical sections of others.
- The caller must pass the same node to lock and unlock, and must not reuse the node until unlock returns.

## Variants and improvements

- **CLH lock.** Craig, and Magnusson, Landin and Hagersten, keep the list implicit: a process spins on the node of its predecessor, and the exit section is one write with no wait. It spins locally in the CC model but not in DSM. See [CLH lock](/clh-lock/).
- **Without compare-and-swap.** The fetch-and-store only exit section above.
- **Time-out and abortable versions.** Scott and Scherer (2001) gave MCS-try and CLH-try locks in which a waiter may leave the queue.
- **K42 and Linux qspinlock.** The K42 variant lets the lock word itself serve as the node of the holder, so the caller needs no node outside the lock. Linux has used an MCS-based queued spin lock (qspinlock) since 2015, with the lock state and a tail code in one 32-bit word.
- **Readers and writers.** Mellor-Crummey and Scott (1991, PPoPP) built fair and preference [readers-writer locks](/readers-writer-lock/) on the same queue.
- **NUMA.** The [cohort lock](/cohort-lock/) uses an MCS lock per NUMA node and a global lock.

## When to use it

Use the MCS lock for a contended lock on a large shared-memory machine, especially without coherent caches or across sockets, and when FIFO order is wanted. It needs a node per waiting process; in a kernel these are per-processor nodes, and in user code they can live on the stack of the caller. For low contention, a [test-and-set](/test-and-set/) or [ticket lock](/ticket-lock/) is cheaper, and with more threads than processors a blocking lock is better.

## Pitfalls

**Setting the flag after the link.** The wrong order is `pred.next ← I` and then `I.locked ← true`. The predecessor may see the link and clear the flag between the two writes, and then the caller sets it to true and spins forever. The right order is L4 then L5.

**Releasing without the compare-and-swap.** The wrong exit is `if I.next = nil then tail ← nil`. A newcomer may have swapped itself into $tail$ just before, and it is then lost: it waits forever, and the next process starts a second queue and enters while the lost one is still in line. The right exit is L8: `COMPARE-AND-SWAP(tail, I, nil)`, and on failure the wait of L9.

**Reusing the node too early.** The node must stay valid until the successor has stopped writing to it (L5 of the successor) and the holder has read it (L7 or L9). Freeing or reusing it inside the critical section is a bug.

**Memory order.** L2 must be at least an acquire and release operation, the read of L6 an acquire, and the write of L10 a release, or the critical section may see stale data on weak memory models.

## Implementations

## History

Mellor-Crummey and Scott (1991) designed the lock to spin only on local memory, after Anderson (1990) and Graunke and Thakkar (1990) had shown that queue locks avoid the traffic of test-and-set. They compared all the main spin locks and barriers on a BBN Butterfly (no coherent caches) and a Sequent Symmetry (with caches). The paper received the Edsger W. Dijkstra Prize in Distributed Computing in 2006. Linux added an MCS-based queued spin lock for x86 in version 4.2 in 2015.

## References
