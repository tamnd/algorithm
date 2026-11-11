---
tag: SV4NZH
kind: algorithm
slug: anderson-lock
name: Anderson's lock
aliases: [array-based queue lock, Anderson's queuing lock]
area: concurrency/mutual-exclusion
level: advanced
summary: A FIFO queue lock with an array of n flags. Fetch-and-add gives each process its own slot to spin on, and the holder hands over by setting the next slot.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes}
  space: {shared: Θ(n)}
  steps: {solo: Θ(1)}
  rmr: {cc: O(1), dsm: ∞}
properties: {deterministic: true, deadlock_free: true, starvation_free: true, fcfs: true, local_spinning: true}
history:
  year: 1990
  people: [Thomas E. Anderson, Gary Graunke, Shreekant Thakkar]
  note: Anderson (1990) proposed the array-based queue lock in his study of spin locks. Graunke and Thakkar (1990) proposed a similar array lock built on swap in the same year.
prereqs: [ticket-lock, rmr-complexity]
see_also: [ticket-lock, mcs-lock, clh-lock, spin-lock, fetch-and-add, cohort-lock, rmr-complexity]
sources:
  - paper: doi:10.1109/71.80120
    title: Thomas E. Anderson, The performance of spin lock alternatives for shared-memory multiprocessors, IEEE Transactions on Parallel and Distributed Systems 1(1), 1990, pages 6-16
    locator: the queueing lock with an array of flags, one for each processor, and its measurements
  - paper: doi:10.1145/103727.103729
    title: John M. Mellor-Crummey and Michael L. Scott, Algorithms for scalable synchronization on shared-memory multiprocessors, ACM Transactions on Computer Systems 9(1), 1991, pages 21-65
    locator: Section 2.3, Anderson's array-based queuing lock, in the form with next_slot and the subtraction of numprocs
  - paper: "Gary Graunke and Shreekant Thakkar, Synchronization algorithms for shared-memory multiprocessors, IEEE Computer 23(6), 1990, pages 60-69"
    locator: the array lock in which each processor swaps its flag address into a tail word and spins on the flag of its predecessor
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 7, Spin Locks and Contention, Section 7.5.1, Array-Based Locks (the ALock, false sharing and padding)
---

Anderson's lock is a queue lock for $n$ processes. A shared array has one flag for each process, and a counter gives out places in the array with [fetch-and-add](/fetch-and-add/), as in the [ticket lock](/ticket-lock/). Each waiter spins on the flag of its own place, and the holder hands the lock over by setting the flag of the next place. So a handover touches one flag instead of a word that all waiters read. In the cache coherent (CC) model a passage makes $O(1)$ remote memory references if the flags lie on separate cache lines.

## In plain words

Think of a row of chairs around a table, one for each person, with a lamp in front of each chair. A ticket machine sends each person who arrives to the next chair in turn. You sit down and watch only your own lamp. When your lamp lights up, it is your turn. You switch your lamp off, do your work, and then light the lamp of the next chair.

Each person watches a different lamp, so a handover disturbs only the next person, not everybody. The catch is that the lamps must really be separate. If two lamps share one switch box, a change to one disturbs the watcher of the other.

## The problem

The [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes with first come, first served order, and with few remote memory references (RMRs). The model is $n$ asynchronous processes on a sequentially consistent shared memory with atomic registers (consensus number 1) and a [fetch-and-add](/fetch-and-add/) counter (consensus number 2). The number $n$ is known in advance. The cost is measured in the CC and the DSM models of [RMR complexity](/rmr-complexity/).

## The algorithm

$slot[0..n - 1]$ is an array of flags: $slot[0] = HAS\_LOCK$ and the others are $MUST\_WAIT$ at the start. $next\_slot$ is a counter, 0 at the start. $place$ is local, and $x \bmod n$ is the residue in $\{0, \ldots, n - 1\}$. This is the form that Mellor-Crummey and Scott (1991) give.

```pseudo id=main
LOCK()
L1  place ← FETCH-AND-ADD(next_slot, 1)          ▷ the doorway
L2  if place mod n = 0 then FETCH-AND-ADD(next_slot, −n)
L3  place ← place mod n
L4  while slot[place] = MUST_WAIT do nothing       ▷ spin on the own slot
L5  slot[place] ← MUST_WAIT                        ▷ reset it for its next user
UNLOCK()
L6  slot[(place + 1) mod n] ← HAS_LOCK
```

L1 is a ticket, and L3 maps it to a slot. L2 keeps the counter in a bounded range: whenever a process gets a multiple of $n$, it subtracts $n$, which does not change any residue. L4 spins on a flag that only one waiter reads. L5 resets the flag before the holder enters, so that the next user of the same slot, $n$ tickets later, waits. L6 is the handover.

**Padding.** In the CC model, each $slot[i]$ must lie on its own cache line. If several flags share a line, then the write of L5 or L6 to one flag invalidates the copies of the other waiters too. This is *false sharing*. The implementation has a `lines` map for both layouts, and the test file measures the difference.

## Example

Three processes, with the counter values in the last column. $H$ is $HAS\_LOCK$ and $W$ is $MUST\_WAIT$.

| step | process | line | action | $slot$ | $next\_slot$ |
|---|---|---|---|---|---|
| start | | | | H W W | 0 |
| 1 | 0 | L1 | gets 0 | H W W | 1 |
| 2 | 1 | L1 | gets 1, place 1 | H W W | 2 |
| 3 | 0 | L2 | 0 mod 3 = 0, subtracts 3 | H W W | −1 |
| 4 | 2 | L1 | gets −1, place 2 | H W W | 0 |
| 5 | 0 | L4 | reads $slot[0] = H$ | H W W | 0 |
| 6 | 0 | L5 | resets $slot[0]$, enters | W W W | 0 |
| 7 | 1 | L4 | reads $slot[1] = W$, spins | W W W | 0 |
| 8 | 2 | L4 | reads $slot[2] = W$, spins | W W W | 0 |
| 9 | 0 | L6 | sets $slot[1]$ | W H W | 0 |
| 10 | 1 | L4, L5 | reads $H$, resets $slot[1]$, enters | W W W | 0 |
| 11 | 1 | L6 | sets $slot[2]$ | W W H | 0 |
| 12 | 2 | L4, L5 | reads $H$, resets $slot[2]$, enters | W W W | 0 |

The handover at step 9 changes only $slot[1]$. Process 2 spins on $slot[2]$ in its cache and is not disturbed. The next process to arrive gets 0 and place 0, and it waits until process 2 sets $slot[0]$.

## Correctness

The full proof is in proofs/correctness.md. Number the L1 steps $0, 1, 2, \ldots$ and call the number the *ticket* of the process; L1 to L3 give a process with ticket $m$ the place $m \bmod n$. The proof shows:

- **Places.** At most $n$ tickets are out at a time, so the waiting processes have distinct places.
- **Invariant.** Let $r$ be the number of L6 steps so far. Either $slot[r \bmod n] = HAS\_LOCK$, every other slot is $MUST\_WAIT$ and no process is between L5 and L6; or every slot is $MUST\_WAIT$ and the process with ticket $r$ is between L5 and L6.
- **Mutual exclusion, FIFO and starvation freedom** follow as for the ticket lock: the lock passes through tickets $0, 1, 2, \ldots$ in order.
- **Remote references.** With padding, a passage makes at most 6 RMRs in the CC model, independent of $n$.

The test file checks mutual exclusion and FIFO order over all interleavings for two processes with two passages and three processes with one, finds the maximum CC cost of a passage to be 6 and 5, checks starvation freedom for two processes that run forever, and checks the costs on random runs.

## Complexity

| measure | value |
|---|---|
| shared words | $n + 1$; with padding, $n$ cache lines per lock |
| steps without contention | 4 or 5: L1, maybe L2, one read at L4, L5, L6 |
| RMRs per passage, CC model, padded | at most 6 |
| RMRs per passage, CC model, one line for all slots | $O(n)$; $2n + 2$ in the round robin run of the test |
| RMRs per passage, DSM model | unbounded |
| bypass after the doorway | 0 |

**Why at most 6 in the CC model.** L1 and L2 are at most two atomic steps. While a process with ticket $m$ waits, its slot is written only once: by the L6 of ticket $m - 1$. The previous user of the slot, with ticket $m - n$, reset it at L5 before it entered, and that was before the L1 of ticket $m$, since at most $n$ tickets are out. So the reads of L4 make at most two misses: the first read and the read after the handover. L5 and L6 are one write each. That is $2 + 2 + 1 + 1 = 6$.

**Why not in the DSM model.** In the DSM model each flag lives in one memory module. A process gets a different place in each passage, so it usually spins on a flag in the module of another process, and every read of L4 is remote. There is no bound.

**Space.** Each lock needs $\Theta(n)$ words, or $\Theta(n)$ cache lines with padding, even when few processes use it. With $L$ locks that is $\Theta(Ln)$ space. The [MCS lock](/mcs-lock/) and the [CLH lock](/clh-lock/) need $O(1)$ space per lock plus $O(1)$ per process.

## Properties

- Uses fetch-and-add (and a fetch-and-add of $-n$, or an atomic increment modulo $n$) plus reads and writes.
- Deadlock free, starvation free and FCFS, with bypass 0 after the doorway.
- Local spinning in the CC model, if padded. Not local in the DSM model.
- Needs $n$ in advance and $\Theta(n)$ space per lock.
- Deterministic.

## Variants and improvements

- **Graunke and Thakkar's lock** (1990). Each process owns a flag, and a shared word holds the address and the value of the last flag. A process swaps its own flag into that word, and spins until the flag of its predecessor changes from the value it saw. Spinning is on the predecessor's flag, as in the CLH lock.
- **MCS lock.** Replaces the array by a linked list of nodes, one per waiting process, so that a process spins on its own node, which can live in its own memory module. This gives $O(1)$ RMRs in the DSM model too. See [MCS lock](/mcs-lock/).
- **CLH lock.** A linked list in which each process spins on the node of its predecessor. See [CLH lock](/clh-lock/).
- **Increment modulo $n$.** With an atomic "fetch and increment modulo $n$", L2 and L3 are not needed.
- **Hierarchical locks.** For NUMA machines, see the [cohort lock](/cohort-lock/).

## When to use it

Use Anderson's lock when the number of processes is small and known, the machine is cache coherent, and you want a simple FIFO lock without a linked list. Pad the array to the cache line size. Prefer the MCS or CLH lock when there are many locks, many possible processes, or a DSM machine.

## Pitfalls

**False sharing.** The wrong layout is `slot: array of n booleans`, where all flags share one cache line: each handover then invalidates every waiter, and a passage costs $O(n)$ RMRs. The test file measures $2n + 2$ in a round robin run. The right layout puts each flag on its own line: `slot: array of n cache lines, each holding one flag`. The test measures 5 then.

**Forgetting the reset.** The wrong code leaves out L5. Then $slot[place]$ stays $HAS\_LOCK$ after the holder leaves, and the process that gets the same place $n$ tickets later enters at once, while the holder of an earlier place may still be inside. The right code has L5, `slot[place] ← MUST_WAIT`, before the critical section.

**Too few slots.** The array must have at least as many slots as processes that can wait at once. With $n$ slots and $n + 1$ processes, two processes get the same place and can enter together.

**Counter overflow.** Without L2, $next\_slot$ grows without bound and a fixed width counter wraps to a value that is not a multiple of $n$ unless $n$ is a power of two. Keep L2, or use a power of two for $n$.

## Implementations

## History

Anderson (1990) measured spin locks on a Sequent Symmetry and showed that test-and-set locks waste bus bandwidth with many processors. He proposed exponential backoff and this array lock, in which each processor spins on its own flag. Graunke and Thakkar (1990) published a similar lock built on swap. Mellor-Crummey and Scott (1991) gave the form on this page, compared it with their MCS lock, and pointed out that its space is $\Theta(n)$ per lock and that it does not spin locally on machines without coherent caches.

## References
