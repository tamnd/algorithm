---
tag: KR24FX
kind: algorithm
slug: cohort-lock
name: Cohort lock
aliases: [lock cohorting]
area: concurrency/mutual-exclusion
level: research
summary: A NUMA lock made of one global lock and one local lock per NUMA node. The holder passes the global lock to a waiter on its own node, up to a bound, before it lets another node in.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes, d: the number of NUMA nodes}
  space: {shared: Θ(n + d)}
  steps: {solo: Θ(1)}
  rmr: {cc: ∞, dsm: ∞}
properties: {deterministic: false, deadlock_free: true, starvation_free: false, fcfs: false, local_spinning: false}
history:
  year: 2012
  people: [David Dice, Virendra J. Marathe, Nir Shavit]
  note: Dice, Marathe and Shavit introduced lock cohorting at PPoPP 2012, as a way to turn any pair of suitable locks into a NUMA lock, and gave C-BO-MCS, C-TKT-TKT and other cohort locks.
prereqs: [mcs-lock]
see_also: [mcs-lock, clh-lock, spin-lock, ticket-lock, anderson-lock, rmr-complexity, starvation-freedom, fairness]
sources:
  - paper: doi:10.1145/2145816.2145848
    title: David Dice, Virendra J. Marathe and Nir Shavit, Lock cohorting, a general technique for designing NUMA locks, Proceedings of the 17th ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming (PPoPP), 2012, pages 247-256
    locator: the cohorting transformation, thread-oblivious global locks, cohort detection, the may-pass-local bound, and the C-BO-MCS lock
  - paper: doi:10.1145/2686884
    title: David Dice, Virendra J. Marathe and Nir Shavit, Lock cohorting, a general technique for designing NUMA locks, ACM Transactions on Parallel Computing 1(2), 2015
    locator: the journal version, with the proofs and the abortable cohort locks
  - paper: "Zoran Radović and Erik Hagersten, Hierarchical backoff locks for nonuniform communication architectures, Proceedings of the 9th International Symposium on High-Performance Computer Architecture (HPCA), 2003"
    locator: the HBO lock, an earlier NUMA lock that uses shorter backoff for waiters on the node of the holder
  - paper: "Victor Luchangco, Dan Nussbaum and Nir Shavit, A hierarchical CLH queue lock, Proceedings of Euro-Par 2006"
    locator: the HCLH lock, which splices local CLH queues into a global queue
  - paper: doi:10.1145/103727.103729
    title: John M. Mellor-Crummey and Michael L. Scott, Algorithms for scalable synchronization on shared-memory multiprocessors, ACM Transactions on Computer Systems 9(1), 1991, pages 21-65
    locator: Section 2.4, the MCS lock used as the local lock
---

A cohort lock is a lock for a NUMA machine, on which a processor reaches the memory of its own node much faster than the memory of another node. It combines one *global* lock with one *local* lock for each NUMA node. A process first takes the local lock of its node. If the previous holder on the same node passed the global lock along with the local lock, the process is done; otherwise it takes the global lock too. On release, a holder that sees a waiter on its own node (a *cohort* member) hands both locks to it, but only a bounded number of times in a row; then it releases the global lock so that other nodes get a turn. This keeps the lock and the data it guards on one node for several passages. The implementation here is the C-BO-MCS lock of Dice, Marathe and Shavit: a test-and-test-and-set lock with backoff as the global lock, and an MCS lock per node.

## In plain words

A company has one meeting room and several floors. On each floor people line up for the room. The first person in a floor's line goes to fetch the room key from the lobby. When that person is done, and somebody from the same floor is next in line, the key goes straight to that colleague, without a trip to the lobby. This is fast, because the key stays upstairs.

But if the key never went back, people from other floors would wait forever. So after a fixed number of handovers on one floor, the key goes back to the lobby, and any floor may take it.

## The problem

The [mutual exclusion problem](/mutual-exclusion-problem/) on a machine with $d$ NUMA nodes (clusters) and $n$ processes, each fixed to one node. The goal beyond safety is *locality*: consecutive holders should mostly be on the same node, so that the lock word and the protected data stay in the caches of that node. The model is $n$ asynchronous processes on a sequentially consistent memory with atomic registers (consensus number 1), test-and-set and swap (consensus number 2) and compare-and-swap (consensus number $\infty$).

The construction needs two properties. The global lock must be *thread-oblivious*: a process may release it even if another process acquired it. The local lock must support *cohort detection*: the holder can tell whether another process of its node waits. A test-and-set lock is thread-oblivious, and an MCS lock supports cohort detection.

## The algorithm

$G$ is the global lock word, false when free. Node $c$ has the MCS tail $tail[c]$ and a pass counter $count[c]$. Process $p$ owns an MCS node $I$ with the fields $I.next$ and $I.state$, where $state$ is $WAIT$, $GLOBAL$ (the global lock was passed with the local lock) or $ACQ$ (the process must take the global lock). $B$ is the may-pass-local bound.

```pseudo id=main
LOCK(I, c)                                ▷ c is the NUMA node of the caller
L1  I.next ← nil;  I.state ← WAIT
L2  pred ← FETCH-AND-STORE(tail[c], I)     ▷ join the local MCS queue
L3  if pred ≠ nil then
        pred.next ← I
        while I.state = WAIT do nothing     ▷ local spinning
        if I.state = GLOBAL then return     ▷ the global lock came with the local lock
L4  GLOBAL-ACQUIRE(G)                       ▷ test-and-test-and-set with backoff
L5  count[c] ← 0
UNLOCK(I, c)
L6  succ ← I.next
    if succ = nil and tail[c] ≠ I then      ▷ cohort detection: someone has joined
        repeat succ ← I.next until succ ≠ nil
L7  if succ ≠ nil and count[c] < B then     ▷ may pass locally
        count[c] ← count[c] + 1
        succ.state ← GLOBAL
        return
L8  G ← false                               ▷ release the global lock
L9  if succ = nil then
        if COMPARE-AND-SWAP(tail[c], I, nil) then return
        repeat succ ← I.next until succ ≠ nil
    succ.state ← ACQ                        ▷ the successor must take G itself
```

L1 to L3 are the MCS entry section, with a state instead of a flag. L4 is the global lock; `GLOBAL-ACQUIRE` is the TTAS-BO loop of the [spin lock](/spin-lock/) page. L5 starts a new batch. L6 is cohort detection: if $next$ is empty but $tail[c]$ is not the caller, a process of the same node has swapped itself in and will link shortly. L7 passes both locks inside the node while the batch is shorter than $B + 1$ passages. L8 and L9 release the global lock and then the local lock, and tell the local successor, if any, to compete for the global lock.

## Example

Processes $a$ and $b$ on node 0, process $e$ on node 1, and $B = 1$.

| step | process | line | action | $G$ | $count[0]$ |
|---|---|---|---|---|---|
| 1 | $a$ | L1, L2 | joins queue 0, $pred = nil$ | false | 0 |
| 2 | $a$ | L4, L5 | wins the TAS on $G$, enters | true | 0 |
| 3 | $b$ | L1 to L3 | joins queue 0 behind $a$, links, spins on its state | true | 0 |
| 4 | $e$ | L1, L2, L4 | joins queue 1 alone, spins on $G$ | true | 0 |
| 5 | $a$ | L6, L7 | sees $b$, $count[0] = 0 < 1$: passes, $b.state \leftarrow GLOBAL$ | true | 1 |
| 6 | $b$ | L3 | sees $GLOBAL$, enters without touching $G$ | true | 1 |
| 7 | $a$ | L1 to L3 | joins queue 0 again behind $b$, spins | true | 1 |
| 8 | $b$ | L6, L7 | sees $a$, but $count[0] = 1$: no pass | true | 1 |
| 9 | $b$ | L8, L9 | $G \leftarrow$ false, $a.state \leftarrow ACQ$ | false | 1 |
| 10 | $e$ | L4 | wins the TAS on $G$, enters | true | 1 |
| 11 | $a$ | L4 | spins on $G$ | true | 1 |

Node 0 had a batch of $B + 1 = 2$ passages with one acquisition of $G$. Then the bound sent $G$ back, and node 1 got it.

## Correctness

The full proof is in proofs/correctness.md. Call a process the *owner* of $G$ from its winning TAS at L4, or from the step that sets its state to $GLOBAL$, until it writes $GLOBAL$ to a successor at L7 or writes $G \leftarrow$ false at L8.

- **One owner.** $G$ is true exactly when there is an owner, and there is at most one: a TAS succeeds only on a free $G$, and a pass at L7 moves ownership from one process to the next in one step.
- **Mutual exclusion.** Every process in its critical section is the owner of $G$.
- **Bounded passing.** Between two successful TAS steps on $G$, at most $B$ passes happen, so at most $B + 1$ critical sections.
- **Deadlock freedom.** The local queues behave like MCS queues, and the head of each local queue either owns $G$ or competes for it with a deadlock-free lock.
- **No starvation freedom.** The global lock is a backoff lock, which is not starvation free; a process on one node can lose the TAS on $G$ forever to processes on another node.

The test file checks mutual exclusion over all interleavings for two processes on one node with two passages each, and for three processes on two nodes with $B = 0$ and $B = 1$. With one process on each of two nodes running forever, it finds no deadlock and finds a starvation cycle; with two processes on one node, it finds no starvation. On random runs with three processes on each of two nodes, it checks that each batch between two acquisitions of $G$ has at most $B + 1$ critical sections and that the bound is reached, for $B$ from 0 to 4.

## Complexity

| measure | value |
|---|---|
| shared space | one global word, $d$ local tails and counters, one node per process |
| steps without contention | the MCS entry and exit plus one TAS and one write on $G$ |
| RMRs per passage | unbounded, from the spinning on $G$ at L4 |
| global lock acquisitions | at least one per $B + 1$ critical sections under contention on one node |

The cost model that matters here is not RMRs but the number of handovers that cross NUMA nodes, since each one moves the lock and the protected data between nodes. With $B$ large and all nodes busy, about one in $B + 1$ handovers crosses nodes. Waiters inside a node spin locally on their MCS nodes; only the heads of the local queues spin on $G$, at most one per node, so at most $d$ processes contend for $G$.

## Properties

- Uses swap and compare-and-swap for the local MCS locks, and test-and-set for the global lock.
- Deadlock free. Not starvation free with a backoff global lock. With a fair global lock, such as a ticket lock, and a finite $B$, every process enters.
- Not FIFO: processes of one node pass processes of other nodes that waited longer, up to $B$ times.
- Randomized, through the backoff of the global lock.
- Most waiters spin on their own MCS nodes; the heads of the local queues spin on $G$.

## Variants and improvements

Dice, Marathe and Shavit combine many pairs of locks:

- **C-BO-BO.** Backoff locks for both levels. The local BO lock needs an extra field in which waiters tell the holder that they exist.
- **C-TKT-TKT.** Ticket locks for both levels; cohort detection compares the two counters of the local ticket lock. The global ticket lock must release with $serving \leftarrow serving + 1$, since the releasing process may not know the ticket of the acquiring one.
- **C-BO-MCS.** This page.
- **C-PTL-TKT and C-MCS-MCS.** With a partitioned ticket lock or an MCS lock as the global lock; an MCS global lock needs a thread-oblivious form in which the node is not tied to the process that enqueued it.
- **Abortable cohort locks.** The journal version adds locks in which a waiter may give up.

Earlier NUMA locks include the hierarchical backoff lock of Radović and Hagersten (2003), which gives waiters on the node of the holder a shorter backoff, and the HCLH lock of Luchangco, Nussbaum and Shavit (2006). Later NUMA locks include compact NUMA-aware locks (CNA), which keep one MCS queue and move remote waiters to a secondary queue.

## When to use it

Use a cohort lock for a heavily contended lock on a machine with two or more NUMA nodes, when the protected data is large enough that moving it between nodes costs more than the lock itself. Pick $B$ to trade throughput (large $B$) against fairness between nodes (small $B$). For one socket, a plain [MCS lock](/mcs-lock/) or [CLH lock](/clh-lock/) is simpler and as fast.

## Pitfalls

**Passing without a bound.** The wrong line is `if succ ≠ nil then pass locally`. A busy node then keeps the global lock forever, and every other node starves. The right line is L7: `if succ ≠ nil and count[c] < B then pass locally`.

**Resetting the counter at each pass.** The wrong code writes `count[c] ← 0` at the pass. Then the bound never takes effect. The right place is L5, only after a successful acquisition of $G$.

**A global lock that is not thread-oblivious.** The process that releases $G$ is often not the one that took it. The wrong global ticket release is `serving ← my + 1`, with the ticket of the releaser, who never took a ticket. The right release is `serving ← serving + 1`. A global lock that records an owner, such as an error-checking POSIX mutex, cannot be used.

**Cohort detection that waits for nobody.** The wrong test is `if tail[c] ≠ I then pass` with $succ$ still $nil$: the holder would write the state of a node it does not know. The right code waits at L6 for the link before it passes.

## Implementations

## History

NUMA machines made the place of the lock matter: Radović and Hagersten (2003) gave hierarchical backoff locks, and Luchangco, Nussbaum and Shavit (2006) gave a hierarchical CLH lock, both tied to one kind of lock. Dice, Marathe and Shavit (2012) showed that a NUMA lock can be built from almost any pair of locks, if the global lock is thread-oblivious and the local lock detects cohorts. Their cohort locks beat the earlier NUMA locks on a four-socket machine, and the journal version (2015) added proofs and abortable locks.

## References
