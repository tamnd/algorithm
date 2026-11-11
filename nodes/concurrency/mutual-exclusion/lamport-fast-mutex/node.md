---
tag: HZ54V5
kind: algorithm
slug: lamport-fast-mutex
name: Lamport's fast mutual exclusion algorithm
aliases:
- Lamport fast mutex
area: concurrency/mutual-exclusion
level: advanced
summary: A deadlock free mutual exclusion algorithm from read/write registers in which a process without contention makes only 5 writes and 2 reads per passage, for any number of processes.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes}
  space: {shared: Θ(n)}
  steps: {solo: Θ(1)}
  rmr: {cc: ∞, dsm: ∞}
  bypass: {worst: ∞}
properties: {deterministic: true, deadlock_free: true, starvation_free: false, fcfs: false, bounded_bypass: false, single_writer: false, bounded_registers: true, local_spinning: false}
history:
  year: 1987
  people: [Leslie Lamport]
  note: Published in ACM Transactions on Computer Systems, with the remark that contention for a lock is rare in well designed systems, so the case without contention should be fast.
prereqs: [mutual-exclusion-problem, burns-lamport-algorithm]
see_also: [fischer-algorithm, mutual-exclusion-lower-bounds, lamport-bakery-algorithm, rmr-complexity, test-and-set, deadlock-freedom, starvation-freedom]
sources:
  - paper: doi:10.1145/7351.7352
    title: Leslie Lamport, A fast mutual exclusion algorithm, ACM Transactions on Computer Systems 5(1), 1987, pages 1-11
    locator: the algorithm with the registers x, y and b, and the count of five writes and two reads without contention
  - paper: doi:10.1109/REAL.1992.242680
    title: Rajeev Alur and Gadi Taubenfeld, Results about fast mutual exclusion, Proceedings of the 13th IEEE Real-Time Systems Symposium, 1992, pages 12-21
    locator: the result that no algorithm bounds the number of shared memory accesses of the winning process when there is contention
  - paper: doi:10.1006/inco.1993.1065
    title: James E. Burns and Nancy A. Lynch, Bounds on shared memory for mutual exclusion, Information and Computation 107(2), 1993, pages 171-184
    locator: the lower bound of n shared registers; this algorithm uses n + 2
---

Lamport's fast mutual exclusion algorithm solves the deadlock free form of the [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes with atomic read/write registers, and it is fast when there is no contention. A process that runs alone makes 5 writes and 2 reads in one passage, whatever the number of processes. Earlier algorithms from reads and writes, such as the [Burns-Lamport algorithm](/burns-lamport-algorithm/) or the [bakery](/lamport-bakery-algorithm/), read the registers of all $n$ processes in each passage. The fast path uses two shared registers $x$ and $y$; a process falls back to a slow path with one flag per process only when it meets contention. Lamport published it in 1987. The algorithm is deadlock free, but a process can starve.

## In plain words

There is a door $y$ and a name board $x$. To enter, you write your name on the board, then look at the door. If the door is taken, you step back and wait until it is free. If it is free, you write your name on the door and look at the board again. If your name is still on the board, no one came after you, and you go in. This is the fast path: two writes, two reads, and one more write to say that you want to enter.

If another name is on the board, someone came in at the same time. Then you take the slow path: you lower your flag and wait until all flags are down. After that, the one whose name is still on the door goes in, and the others wait until the door is free and start again.

## The problem

There are $n \ge 2$ asynchronous processes with the names $1, \ldots, n$. Each one repeats a remainder section, an entry section, a critical section and an exit section. The entry and exit sections must give mutual exclusion and deadlock freedom, as the [mutual exclusion problem](/mutual-exclusion-problem/) defines. The shared memory has atomic read/write registers and is sequentially consistent. A process stays in its critical section for a finite time. The goal is a constant number of steps when a process runs alone.

## The algorithm

The shared registers are $x$ and $y$, which hold a name or 0, and one boolean $b[j]$ for each process $j$. At the start $y = 0$, which means "free", and all $b[j]$ are false.

```pseudo id=main
LOCK(i)
L1  loop
L2      b[i] ← true
L3      x ← i
L4      if y ≠ 0 then
L5          b[i] ← false
L6          await y = 0
L7          start the next round of the loop at L2
L8      y ← i
L9      if x ≠ i then
L10         b[i] ← false
L11         for each j: await not b[j]
L12         if y ≠ i then
L13             await y = 0
L14             start the next round of the loop at L2
L15     exit the loop
UNLOCK(i)
L16 y ← 0
L17 b[i] ← false
```

L2 to L9 with a successful test at L9 is the fast path. A process that reads $x \ne i$ at L9 knows that another process wrote $x$ after it, so two processes may be between L8 and the critical section. On the slow path it lowers its flag and waits at L11 until every process has left the region between L2 and L10. Then the value of $y$ names the last process that wrote $y$, and only that process goes in. The others wait for $y = 0$, that is, for the exit of the process inside, and start again. The wait at L11 reads the flag of every process, its own too, which is false.

The implementation gives process $i$ the name $i + 1$, so that its processes are numbered from 0 and the name 0 stays free.

## Example

Two processes with the names 1 and 2 meet. All registers are 0 or false at the start. The test file runs this schedule step by step; there the processes are numbered 0 and 1.

| step | process | action | $x$ | $y$ |
|---|---|---|---|---|
| 1 | 1 | $b[1] \leftarrow$ true; $x \leftarrow 1$; reads $y = 0$ | 1 | 0 |
| 2 | 2 | $b[2] \leftarrow$ true; $x \leftarrow 2$; reads $y = 0$ | 2 | 0 |
| 3 | 1 | $y \leftarrow 1$ | 2 | 1 |
| 4 | 2 | $y \leftarrow 2$ | 2 | 2 |
| 5 | 1 | reads $x = 2$, not its name: slow path | 2 | 2 |
| 6 | 2 | reads $x = 2$: enters by the fast path | 2 | 2 |
| 7 | 1 | $b[1] \leftarrow$ false; reads $b[1]$ = false; reads $b[2]$ = true and waits | 2 | 2 |
| 8 | 2 | leaves: $y \leftarrow 0$; $b[2] \leftarrow$ false | 2 | 0 |
| 9 | 1 | reads $b[2]$ = false; reads $y = 0$ at L12, not its name; reads $y = 0$ at L13 and starts again | 2 | 0 |
| 10 | 1 | $b[1] \leftarrow$ true; $x \leftarrow 1$; reads $y = 0$; $y \leftarrow 1$; reads $x = 1$: enters | 1 | 1 |

In step 6, process 2 wrote $x$ last, so it is the one that sees its own name and goes in. Process 1 waits on the slow path until process 2 has left, and then enters by the fast path.

## Correctness

The full proof is in proofs/correctness.md.

- **The key invariant.** While a process is in the critical section, $y \ne 0$. Only the exit writes 0 to $y$, and the proof shows that no exit can come between the write of $y$ by a fast path process and its entry.
- **Mutual exclusion.** Two fast path processes cannot both see their own name in $x$, because the later writer of $x$ wrote it inside the window of the other. A slow path process waits until the flag of every process is down, so it cannot pass while a fast path process is between L2 and its exit. Two slow path processes cannot both read their own name in $y$, because the later writer of $y$ still had its flag up when the other one checked the flags.
- **Deadlock freedom.** If no process enters and $y \ne 0$, then $y$ settles on the name of the last writer, every other process lowers its flag, and the last writer passes L11 and L12. If $y = 0$ forever, no process can be in the middle of a round, which is not possible.
- **No starvation freedom.** A process can be overtaken again and again: each time it comes back to L4, another process has already written $y$. The proof file gives such a run for two processes.

The test file checks mutual exclusion and deadlock freedom by exhaustive search of all interleavings: for 2 processes with one passage each (342 states) and forever (992 states), and for 3 processes with one passage each (23951 states). For 2 processes forever it finds starvation runs for both processes, and it runs the starvation cycle of the proof file. It checks that a process alone makes exactly the 5 writes and 2 reads of the fast path, for 2, 3 and 8 processes, and it runs the slow path example above.

## Complexity

| measure | value |
|---|---|
| shared registers | $n + 2$: $x$ and $y$ with $n + 1$ values, and $n$ booleans $b[j]$ |
| passage without contention | 7 accesses: the writes of $b[i]$, $x$ and $y$ and the reads of $y$ and $x$ in the entry, and the writes of $y$ and $b[i]$ in the exit |
| slow path | $n$ reads at L11 plus the waits; no bound under contention |
| bypass | no bound |
| RMRs per passage | unbounded in both the CC and the DSM model |

Without contention, the entry is $b[i] \leftarrow$ true, $x \leftarrow i$, read $y$, $y \leftarrow i$, read $x$: 3 writes and 2 reads. The exit is $y \leftarrow 0$ and $b[i] \leftarrow$ false: 2 writes. So the passage has 5 writes and 2 reads, and this does not depend on $n$.

Under contention there is no bound, and this is not a weakness of this algorithm only. Alur and Taubenfeld (1992) proved that for two or more processes, no mutual exclusion algorithm bounds the number of shared memory accesses that the winning process needs to enter when there is contention.

## Properties

- Uses atomic read/write registers only. $x$ and $y$ have $n$ writers each, and each $b[i]$ has one writer.
- Mutual exclusion and deadlock freedom; not starvation free and not FCFS.
- A process alone enters in a constant number of steps, for any $n$.
- Symmetric up to the names: all processes run the same code.
- On a search of 2 processes with one passage each, where a read that overlaps a write can return any value of the register, the test file finds no violation. This is a small check only; the page makes no claim for safe registers in general.

## Variants and improvements

- **Fischer's algorithm.** Lamport's paper also gives [Fischer's algorithm](/fischer-algorithm/), which uses one register and a known bound on the time of a step, instead of the slow path.
- **Faster slow paths.** Merritt and Taubenfeld (1993) changed the slow path so that it is faster when few processes compete. Later adaptive algorithms make the cost depend on the number of processes that compete, not on $n$.
- **The splitter.** The first part of the fast path, write $x$, read $y$, write $y$, read $x$, is the idea behind the splitter of Moir and Anderson, which is a building block for renaming and adaptive algorithms.
- **Hardware locks.** With a [test-and-set](/test-and-set/) or compare-and-swap instruction, a lock without contention takes one atomic step. Lamport's algorithm shows that reads and writes alone can also give a constant cost in that case.

## When to use it

Use it to teach the idea of a fast path: optimize the case without contention, and keep a correct but slow path for the rare case of contention. The same idea is in many real locks, such as the futex based mutexes of Linux, which take one atomic instruction when the lock is free. Do not use this algorithm itself as a real lock: real machines have atomic instructions and weak memory, and the algorithm is not fair.

## Pitfalls

**Starvation.** A process can wait forever while others keep entering by the fast path. The proof file gives a run.

**The value 0.** The value 0 in $y$ means "free", so no process may have the name 0. The implementation gives process $i$ the name $i + 1$.

**The order of the steps.** The write of $x$ must come before the read of $y$, and the write of $y$ before the read of $x$. If a compiler or the hardware reorders them, the algorithm breaks. On TSO hardware such as x86, the write of $x$ can wait in a store buffer while the process reads $y$; the test file finds a run on the TSO model with two processes in the critical section.

**Hot spots.** Under contention, all waiting processes read $y$ again and again. On a machine without caches this makes much traffic on one register.

## Implementations

## History

Lamport published the algorithm in 1987 in ACM Transactions on Computer Systems. He wrote that in a well designed system, contention for a critical section is rare, so the cost without contention matters most, and he noted that earlier algorithms from reads and writes need a number of steps that grows with $n$ even without contention. The paper also gave Fischer's timing based algorithm. Alur and Taubenfeld (1992) proved that a bound on the steps of the winner under contention is not possible, and Merritt and Taubenfeld (1993) gave a faster slow path. Moir and Anderson later used the fast path as the splitter for renaming.

## References
