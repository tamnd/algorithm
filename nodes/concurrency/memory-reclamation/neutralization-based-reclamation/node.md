---
tag: A696BX
kind: algorithm
slug: neutralization-based-reclamation
name: Neutralization-based reclamation
aliases: [NBR]
area: concurrency/memory-reclamation
level: research
summary: A thread reserves the nodes it will change before it writes. A reclaimer signals all threads; a thread that only reads restarts, so the reclaimer can free every node that no one reserved.
solves: [safe-memory-reclamation]
complexity:
  vars: {n: the number of processes, K: the number of reservations per process, R: the retire list size that starts a scan}
  space: {reservations: Θ(n K), unfreed_garbage: O(n R)}
  steps: {read: O(1), enter_write_phase: O(K), scan: O(n K + R)}
properties: {robust: true, bounded_garbage: true, per_read_cost: false, needs_signals: true, restartable_reads: true}
history:
  year: 2021
  people: [Ajay Singh, Trevor Brown, Ali Mashtizadeh]
  note: Singh, Brown and Mashtizadeh presented NBR at PPoPP 2021. It takes the signals of DEBRA+ (Brown, 2015) and replaces the recovery code with a restart of the read phase.
prereqs: [epoch-based-reclamation, hazard-pointers]
see_also: [debra, hazard-eras, interval-based-reclamation, quiescent-state-based-reclamation, harris-linked-list, optimistic-access, treiber-stack, michael-scott-queue]
sources:
  - paper: doi:10.1145/3437801.3441625
    title: "Ajay Singh, Trevor Brown and Ali Mashtizadeh, NBR: Neutralization based reclamation, PPoPP 2021"
    locator: Section 4.1 (the phases), Algorithm 1 (beginReadPhase, endReadPhase and retire with signalAll), Sections 4.2 to 4.4 (signals, the handshakes and the write phase rule), Algorithm 2 and Section 5.1 (NBR+), Appendix A (Assumption 4 and the proof)
  - paper: doi:10.1145/2767386.2767436
    title: Trevor Alexander Brown, Reclaiming memory for lock-free data structures, there has to be a better way, PODC 2015, pages 261-270
    locator: DEBRA+, which sends signals to neutralize a stalled thread in epoch-based reclamation
---

Neutralization-based reclamation, or NBR, is a [safe memory reclamation](/safe-memory-reclamation/) method by Ajay Singh, Trevor Brown and Ali Mashtizadeh. Each attempt of an operation has a read phase, which only reads, and a write phase, which changes memory. A thread can restart its read phase at any time. Before it starts to write, it publishes reservations for the few nodes that the write phase will use, as with [hazard pointers](/hazard-pointers/). A thread whose retire list is full sends a signal to every other thread. A thread in its read phase that gets the signal drops all its pointers and restarts. So after the signals, the reclaimer reads the reservations and frees every retired node that no one reserved. The reads cost nothing extra, and a stalled thread holds back at most its $K$ reserved nodes.

## In plain words

Workers look through a shared archive and sometimes change a file. Looking is cheap: a worker does not tell anyone what they look at.

Before a worker changes a file, they write the names of the few files they will touch on a board.

A clerk who wants to shred old files first rings a bell. Every worker who is only looking stops, forgets what they saw, and starts again from the archive door. Old files are no longer in the archive, so a worker who starts again cannot find them.

After the bell, the clerk reads the board and shreds every old file whose name is not on it.

A worker who falls asleep can only hold up the few files on the board, never the whole pile.

## The problem

[Safe memory reclamation](/safe-memory-reclamation/) for lock-free structures such as the [Treiber stack](/treiber-stack/), the [Michael and Scott queue](/michael-scott-queue/) and the [Harris list](/harris-linked-list/). [Epoch-based reclamation](/epoch-based-reclamation/) costs little per read, but one stalled thread stops all reclamation. [Hazard pointers](/hazard-pointers/) bound the garbage, but each read of a node costs a write and a fence. NBR wants the low read cost of epochs and the bounded garbage of hazard pointers.

The model: $n$ asynchronous processes on a sequentially consistent shared memory, with a way to interrupt a process, such as POSIX signals. Each process has $K$ reservation words that others can read, a local flag that says if it can restart now, and a local retire list. A signal is handled before the next shared step of its target. The data structure must split each attempt of an operation into a read phase that does not write shared nodes or allocate, and a write phase that uses only the nodes it reserved.

## The algorithm

```pseudo id=main
BEGIN_READ_PHASE()                   ▷ at the start of each attempt
L1  for i in 0..K−1: res[me][i] ← nil
L2  restartable ← true
END_READ_PHASE(p_0, ..., p_{K−1})    ▷ the nodes the write phase uses
L3  for i in 0..K−1: res[me][i] ← p_i
L4  restartable ← false
RETIRE(x)
L5  append x to list[me]; if |list[me]| < R then return
L6  for each process q ≠ me: send a signal to q
L7  S ← the set of all non-nil res[q][i]
L8  for each y in list[me]: if y ∉ S then free y and remove it from list[me]
ON_SIGNAL()                          ▷ the handler of a process
    if restartable then drop all local pointers and go back to L1
```

The order in L1 and L2 and in L3 and L4 is the whole point. A thread clears its old reservations before it can be restarted, and it publishes its new reservations before it can no longer be restarted. So at every moment, each node a thread may use is either reserved, or the thread will drop it when a signal comes. In the paper, L2 and L4 are compare-and-swap steps on a word that the signal handler reads, which also acts as a fence.

A signal does not wait for an answer. It is enough that the target handles it before its next access to a shared node. A node retired before the signal is not reachable, so a thread that restarts cannot find it again.

## Example

A stack $top \to A \to B \to C$, two processes, $R = 1$. Process $p$ pops slowly; process $q$ pops twice.

| step | process | line | action | state after |
|---|---|---|---|---|
| 1 | $p$ | L1, L2 | starts a read phase | $p$ restartable |
| 2 | $p$ | pop | reads $top = A$ and $A.next = B$ | |
| 3 | $q$ | L3, L4 | reads $A$ and $B$, reserves both | $res[q] = (A, B)$ |
| 4 | $q$ | pop, L5 | CAS $top$ from $A$ to $B$; retires $A$ | $list[q] = (A)$ |
| 5 | $q$ | L6 to L8 | signals $p$; $A$ is reserved by $q$ itself, so it stays | $list[q] = (A)$ |
| 6 | $q$ | L1 to L4 | second pop: clears, reads $B$ and $C$, reserves both | $res[q] = (B, C)$ |
| 7 | $q$ | pop, L5 | CAS $top$ from $B$ to $C$; retires $B$ | $list[q] = (A, B)$ |
| 8 | $q$ | L6 to L8 | signals $p$; frees $A$, keeps $B$ | $list[q] = (B)$ |
| 9 | $p$ | handler | handles the signal: it is restartable, so it goes back to L1 | |
| 10 | $p$ | pop | reads $top = C$ and pops $C$ | stack empty |

If $p$ ignores the signal, its next step reads $A.val$ after step 8 freed $A$. The test finds this run.

## Correctness

The full proof is in proofs/correctness.md. It assumes the two phases described above, that a read phase accesses only nodes that were reachable at the read that returned them, that each node is retired once after its unlink and not linked again, and that a signal is handled before the next shared step of its target (Assumption 4 of the paper).

- **Key fact.** Between the signal and its handling, the target takes no step, so its flag and its reservations do not change. If it is restartable, it drops its pointers. If it is not, it is in a write phase whose nodes it reserved before the signal, and the reclaimer reads the reservations after the signal.
- **Safety.** A thread that restarts reads only from the roots after the unlink, so it cannot reach a retired node. A thread in its write phase uses only reserved nodes, and the scan keeps them.
- **Bound.** With $R > n K$, a scan keeps at most $n K$ nodes, so each list holds at most $R$ nodes, and at most $n R$ nodes are unfreed in total, whatever threads stop.

The test file checks every interleaving of a stack run and a queue run, seeded random runs, three broken versions (a thread that ignores signals, a thread that leaves the read phase before it writes its reservations, and a scan that reads the reservations before it sends the signals), an immediate free, and the garbage under a stall.

## Complexity

| measure | value |
|---|---|
| shared space | $n K$ reservation words |
| a read in the read phase | no extra step |
| entering the write phase | $K$ writes and one fence |
| a scan | $n - 1$ signals, $n K$ reads, one free per freed node |
| scan cost per freed node | $O(1)$ when $R \ge 2 n K$ |
| unfreed garbage | at most $n R$, even with stopped threads |

**Garbage under a stall.** The test runs three processes on a structure with four nodes, with $K = 2$ and $R = 2 n K = 12$. Process 0 stops inside its first pop or dequeue, and the others do 50 or 400 operations. The peak of unfreed retired nodes stays between 22 and 24 in all runs, under the proved bound $n R = 36$. With [epoch-based reclamation](/epoch-based-reclamation/) the same runs keep every retired node.

## Properties

- Robust: a stopped thread holds back at most its $K$ reserved nodes, and the total garbage is bounded.
- Reads in the read phase are plain loads, with no write and no fence per node.
- Needs a way to interrupt threads, and a data structure whose read phase can restart from the roots at any point.
- The restarts are caused only by scans, and each scan follows a successful unlink, so the scheme keeps the lock freedom of the structure.
- A signal costs a system call per target, so a scan is expensive; the cost is spread over $R$ retires.

## Variants and improvements

- **NBR+.** The paper adds a low and a high watermark for the retire list. A thread at the low watermark watches for a scan by another thread, detected with per-thread counters, and then frees its own unreserved nodes without sending signals. Only a thread at the high watermark sends signals. This cuts the number of signals.
- **[DEBRA+](/debra/).** The earlier method by Brown, in [epoch-based reclamation](/epoch-based-reclamation/). A thread that stalls in an epoch gets a signal and runs recovery code that the data structure supplies. NBR replaces the recovery code with a restart of the read phase, which is simpler to write.
- **Several phases per operation.** The paper lets an operation repeat the pair of phases. The Harris list does its search as a read phase and its CAS as a write phase, and starts a new read phase if the CAS fails.
- **[Optimistic access](/optimistic-access/).** Also lets reads run without protection and restarts them, but checks a per-thread warning bit after each read instead of using signals, and needs [type-stable memory](/type-stable-memory/).

This page implements plain NBR with $K = 2$. NBR+ is described but not implemented.

## When to use it

Use NBR when reads are much more common than writes, the threads may stall, and the garbage must stay bounded: for example in search trees and linked lists, where a search reads many nodes and a write uses only a few. It needs signals, or another way to interrupt threads, and a structure where the read phase has no side effects. Do not use it when the read phase must allocate, do I/O or take locks, since a restart could leave these half done, or when a thread may not be interrupted.

## Pitfalls

**Reserving after the phase change.** The wrong code sets the flag to false at L4 first and writes the reservations at L3 after it. A signal that comes between these steps does not restart the thread, and the scan does not see the reservation, so it frees a node the write phase will use. The test finds this with a queue run in which the old tail of a stalled enqueue is freed. The right code writes all reservations at L3 and then clears the flag at L4.

**Reading the reservations before the signals.** The wrong scan reads the reservations first and sends the signals after that. A reader can then reserve a node and enter its write phase between the two steps: the scan did not see the reservation, and the signal finds the reader not restartable, so the node is freed under it. The test finds this with a scripted queue run. The right scan signals at L6 and reads at L7.

**Ignoring the signal.** If the read phase is not restartable, or the handler does not drop the pointers, a reader keeps a pointer to a node that the scan frees. The test finds the run in the example. The right handler goes back to L1 whenever the flag is true.

**Side effects in the read phase.** A read phase that writes a shared node, allocates or takes a lock can be cut off by a restart in the middle. The paper forbids writes to shared records and allocation in the read phase. Do these in the write phase, on reserved nodes.

**A threshold that is too small.** If $R \le n K$, a scan can find all its nodes reserved and free nothing, so every retire sends $n - 1$ signals. Choose $R$ well above $n K$; the paper uses thousands of nodes.

## Implementations

## History

Trevor Brown proposed DEBRA+ in 2015: in [epoch-based reclamation](/epoch-based-reclamation/), a thread that holds up the epoch gets a signal and runs recovery code, so that one stalled thread cannot stop all reclamation. Writing that recovery code is hard for each data structure. Ajay Singh, Trevor Brown and Ali Mashtizadeh presented NBR at PPoPP 2021. It splits each operation into a read phase that can always restart and a write phase that uses [hazard-pointer](/hazard-pointers/) style reservations, so the recovery is just a restart. Their experiments on trees and lists showed throughput close to that of epoch-based methods, with bounded garbage.

## References
