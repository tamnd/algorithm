---
tag: B01V2J
kind: algorithm
slug: ticket-lock
name: Ticket lock
area: concurrency/mutual-exclusion
level: core
summary: A FIFO spin lock with two counters. A process takes a ticket with fetch-and-add and waits until the now-serving counter shows its ticket; the holder advances the counter.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes}
  space: {shared: Θ(1)}
  steps: {solo: Θ(1)}
  rmr: {cc: O(n), dsm: ∞}
properties: {deterministic: true, deadlock_free: true, starvation_free: true, fcfs: true, local_spinning: false}
history:
  year: 1991
  people: [David P. Reed, Rajendra K. Kanodia, John M. Mellor-Crummey, Michael L. Scott]
  note: Reed and Kanodia (1979) built synchronization from eventcounts and sequencers. Mellor-Crummey and Scott (1991) gave the ticket lock with proportional backoff in this form and measured it.
prereqs: [spin-lock]
see_also: [fetch-and-add, spin-lock, anderson-lock, mcs-lock, clh-lock, lamport-bakery-algorithm, rmr-complexity, fairness]
sources:
  - paper: doi:10.1145/103727.103729
    title: John M. Mellor-Crummey and Michael L. Scott, Algorithms for scalable synchronization on shared-memory multiprocessors, ACM Transactions on Computer Systems 9(1), 1991, pages 21-65
    locator: Section 2.2, the ticket lock with proportional backoff (Algorithm 2), and the measurements in Section 4
  - paper: doi:10.1145/359060.359076
    title: David P. Reed and Rajendra K. Kanodia, Synchronization with eventcounts and sequencers, Communications of the ACM 22(2), 1979, pages 115-123
    locator: the sequencer (a ticket dispenser) and the eventcount with await
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 7, Spin Locks and Contention, and the exercises on the ticket lock
  - paper: doi:10.1145/361082.361093
    title: Leslie Lamport, A new solution of Dijkstra's concurrent programming problem, Communications of the ACM 17(8), 1974, pages 453-455
    locator: the bakery algorithm, which takes numbers with reads and writes only
  - url: "https://lwn.net/Articles/267968/"
    title: Jonathan Corbet, Ticket spinlocks, LWN.net, February 2008
    locator: the ticket spin locks of Nick Piggin in Linux 2.6.25 and the unfairness of the old x86 spin lock
---

The ticket lock is a [spin lock](/spin-lock/) that serves processes in first come, first served order. It uses two counters, $next$ and $serving$, both 0 at the start. A process takes the value of $next$ as its ticket and increments $next$ with one [fetch-and-add](/fetch-and-add/). It then waits until $serving$ equals its ticket. To leave, it writes its ticket plus 1 to $serving$. It is the lock of a bakery or a deli counter, made atomic by hardware; the [bakery algorithm](/lamport-bakery-algorithm/) gets the same order with reads and writes only.

## In plain words

At a deli counter you pull a numbered paper ticket from a machine. A screen shows the number that is being served now. You wait until the screen shows your number. When you are done, the screen moves on to the next number.

The machine never gives the same number twice, so nobody can push ahead of you. Everybody who came before you is served first, and then you.

The weak point is the screen. All people who wait look at the same screen, so each change of it must reach all of them. With many people, every change costs a lot of messages.

## The problem

The [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes, with first come, first served (FCFS) order. The model is $n$ asynchronous processes on a sequentially consistent shared memory, with atomic registers (consensus number 1) and one [fetch-and-add](/fetch-and-add/) counter (consensus number 2). The doorway of a process is its fetch-and-add. FCFS means: if $p$ finishes its doorway before $q$ starts its doorway, then $q$ does not enter before $p$. The cost measure is the number of remote memory references (RMRs); see [RMR complexity](/rmr-complexity/).

## The algorithm

$next$ and $serving$ are shared counters, both 0 at the start; $my$ is a local variable that the process keeps until it leaves. $BASE$ is the backoff unit, and $BASE = 0$ turns backoff off.

```pseudo id=main
LOCK()
L1  my ← FETCH-AND-ADD(next, 1)        ▷ the doorway: take a ticket
L2  loop
L3      s ← serving
L4      if s = my then return
L5      wait BASE · (my − s) time units  ▷ proportional backoff
UNLOCK()
L6  serving ← my + 1
```

Only the holder writes $serving$, so L6 can be a plain write. L5 is the *proportional backoff* of Mellor-Crummey and Scott: $my - s$ is the number of processes ahead, and each of them needs at least a critical section, so a waiter can wait that long times a typical length without delay to itself.

With hardware counters of fixed width, the counters wrap around. The implementation has a parameter $M$ that makes L1 count modulo $M$, and L5 and L6 use $(my - s) \bmod M$ and $(my + 1) \bmod M$. This is correct when $M \ge n$, because at most $n$ tickets are out at a time.

## Example

Three processes take tickets at once, with $BASE = 1$.

| step | process | line | action | $next$ | $serving$ |
|---|---|---|---|---|---|
| start | | | | 0 | 0 |
| 1 | 0 | L1 | ticket 0 | 1 | 0 |
| 2 | 1 | L1 | ticket 1 | 2 | 0 |
| 3 | 2 | L1 | ticket 2 | 3 | 0 |
| 4 | 0 | L3, L4 | reads 0, enters | 3 | 0 |
| 5 | 1 | L3, L5 | reads 0, waits 1 unit | 3 | 0 |
| 6 | 2 | L3, L5 | reads 0, waits 2 units | 3 | 0 |
| 7 | 0 | L6 | leaves | 3 | 1 |
| 8 | 1 | L3, L4 | reads 1, enters | 3 | 1 |
| 9 | 2 | L3, L5 | reads 1, waits 1 unit | 3 | 1 |
| 10 | 1 | L6 | leaves | 3 | 2 |
| 11 | 2 | L3, L4 | reads 2, enters | 3 | 2 |

The processes enter in the order of their tickets. In the CC model, process 2 misses on its reads at steps 6, 9 and 11, because $serving$ changed before each of them except the first. With its fetch-and-add and its write at L6 it makes 5 remote references, which is $n + 2$ for $n = 3$.

## Correctness

The full proof is in proofs/correctness.md. The main facts:

- **Distinct tickets.** Fetch-and-add is atomic, so the tickets are $0, 1, 2, \ldots$ in the order of the L1 steps, each given once.
- **Invariant.** $serving$ is the ticket of the holder, if there is a holder, and otherwise the smallest ticket not yet used to enter. It changes only at L6, by 1.
- **Mutual exclusion and FIFO.** A process enters only when $serving$ equals its ticket, and $serving$ passes through the tickets one by one. So the processes enter one at a time, in ticket order, which is the order of their doorways.
- **Starvation freedom.** A process with ticket $t$ waits for at most $t - serving < n$ passages of others, each finite.
- **Remote references.** In the CC model, one passage makes at most $n + 2$ RMRs, and the last of $n$ processes in line makes exactly $n + 2$.

The test file checks mutual exclusion and FIFO order over all interleavings for two processes with two passages each and for three processes with one passage, finds the maximum CC cost of a passage to be 4 and 5, checks that proportional backoff keeps safety, checks starvation freedom with counters modulo 3 for two processes, and shows that counters modulo 2 with three processes break mutual exclusion. It also checks the bound $n + 2$ for $n$ from 2 to 8.

## Complexity

| measure | value |
|---|---|
| shared words | 2 |
| steps without contention | 3: L1, one read at L3, L6 |
| RMRs per passage, CC model | at most $n + 2$, and $n + 2$ is reached |
| RMRs per passage, DSM model | unbounded |
| traffic for one handover with $k$ waiters, CC | $\Theta(k)$ misses |
| bypass after the doorway | 0 |

**Why $n + 2$.** The fetch-and-add of L1 is one RMR, and the write of L6 is one. A waiter's first read of $serving$ misses. After that, a read misses only if $serving$ was written since the last read, and $serving$ is written once per handover. While a process with ticket $t$ waits, $serving$ moves from its first value $s_0$ to $t$, and $t - s_0 \le n - 1$ because at most $n$ tickets are out. So the reads cost at most $1 + (n - 1) = n$ RMRs, and the passage at most $n + 2$.

So a passage is $O(n)$ in the CC model, not $O(1)$ like the queue locks. The bigger cost is the traffic of a handover: all $k$ waiters spin on the one word $serving$, so each write at L6 invalidates $k$ copies and causes $k$ misses. Proportional backoff reduces the number of reads, but not the invalidations. In the DSM model, $serving$ lives in one memory module, and every read of L3 is remote for the other processes.

## Properties

- Uses one fetch-and-add per passage, plus reads and one write.
- Deadlock free, starvation free and FCFS, with bypass 0 after the doorway of one step.
- Deterministic, also with proportional backoff.
- No local spinning: all waiters read the same word.
- No owner is recorded, and $my$ must be kept by the holder for L6. A variant that does L6 as $serving \leftarrow serving + 1$ needs no $my$ in the exit section.

## Variants and improvements

- **The bakery algorithm.** Lamport (1974) takes numbers with reads and writes only, so two processes may get the same number, and ties are broken by process id. See [bakery algorithm](/lamport-bakery-algorithm/).
- **Eventcounts and sequencers.** Reed and Kanodia (1979) described a *sequencer*, which hands out numbers with $\mathrm{ticket}()$, and an *eventcount* with $\mathrm{await}(e, v)$ and $\mathrm{advance}(e)$. A ticket lock is a sequencer for $next$ and an eventcount for $serving$.
- **Array-based queue lock.** Anderson (1990) gives each ticket its own slot, so each waiter spins on a different word and a handover costs $O(1)$ RMRs. See [Anderson's lock](/anderson-lock/).
- **Partitioned ticket lock.** Dice (2011) spreads $serving$ over several words, indexed by the ticket, to reduce the invalidations of each handover.
- **Linux ticket spin locks.** Linux used ticket spin locks on x86 from 2.6.25 (2008), with the two counters in one word, until queued spin locks based on [MCS](/mcs-lock/) replaced them.
- **Fair readers-writer lock.** A ticket lock that readers pass on at once gives a fair [readers-writer lock](/readers-writer-lock/).

## When to use it

Use the ticket lock when you want a simple FIFO spin lock with little code, for a moderate number of processors on one socket. It beats test-and-set locks on fairness. For many processors, or on NUMA machines, use a queue lock such as [MCS](/mcs-lock/) or [CLH](/clh-lock/), or a [cohort lock](/cohort-lock/). Avoid it, like every FIFO spin lock, when there are more threads than processors.

## Pitfalls

**Counters that wrap too soon.** If the counters count modulo $M < n$, two waiting processes can hold the same ticket. With $M = 2$ and three processes, processes 0 and 2 both get ticket 0 and enter together; the test file finds this run. The wrong choice is an 8 bit ticket for up to 256 or more threads. The right choice is a counter of at least $\lceil \log_2 n \rceil$ binary digits, so that $M \ge n$.

**Skipping waiters on release.** The wrong line is `serving ← next`: it jumps over everyone who is waiting, and later tickets can never enter. The right line is L6: `serving ← my + 1`.

**Backoff that is not proportional.** The wrong line is `wait BASE · my`, which grows forever with the ticket number. The right line is L5: `wait BASE · (my − s)`, the distance to the front.

**Preemption of a waiter.** If the next process in line is descheduled, the lock stays free and nobody else may take it, because the order is fixed. With more threads than processors, every FIFO spin lock forms such convoys. Use a lock that blocks, or a lock that lets a waiter leave the queue.

**Memory order.** L3 must be an acquire read and L6 a release write, or the critical section may see stale data on weak memory models.

## Implementations

## History

Reed and Kanodia (1979) proposed eventcounts and sequencers as a synchronization primitive, and a ticket lock is their simplest use. Mellor-Crummey and Scott (1991) gave the ticket lock with proportional backoff as a spin lock and measured it against the test-and-set lock, Anderson's lock and the MCS lock. Linux adopted ticket spin locks for x86 in 2008, because the old test-and-set lock was very unfair on large machines, and replaced them with queued spin locks in 2015.

## References
