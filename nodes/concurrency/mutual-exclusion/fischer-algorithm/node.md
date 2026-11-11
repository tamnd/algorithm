---
tag: DRQ896
kind: algorithm
slug: fischer-algorithm
name: Fischer's algorithm
aliases:
- timing-based mutual exclusion
- Fischer's timed mutual exclusion
area: concurrency/mutual-exclusion
level: advanced
summary: A mutual exclusion algorithm with one shared register. It is correct only if each step takes at most Δ time and the wait D after the write is longer than Δ.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes, Δ: the longest time between the read of x = 0 and the write of x, D: the length of the delay}
  space: {shared: Θ(1)}
  steps: {solo: Θ(1)}
  rmr: {cc: ∞, dsm: ∞}
  bypass: {worst: ∞}
properties: {deterministic: true, deadlock_free: true, starvation_free: false, fcfs: false, bounded_bypass: false, single_writer: false, bounded_registers: true, local_spinning: false}
history:
  year: 1987
  people: [Michael J. Fischer, Leslie Lamport]
  note: Lamport gave this one register algorithm in his 1987 paper on fast mutual exclusion and credited it to Michael Fischer.
prereqs: [mutual-exclusion-problem, lamport-fast-mutex]
see_also: [mutual-exclusion-lower-bounds, peterson-algorithm, test-and-set, spin-lock, deadlock-freedom, starvation-freedom]
sources:
  - paper: doi:10.1145/7351.7352
    title: Leslie Lamport, A fast mutual exclusion algorithm, ACM Transactions on Computer Systems 5(1), 1987, pages 1-11
    locator: the introduction, which gives the algorithm with one register and a delay, credits it to Michael Fischer, and notes that it needs a bound on the time of a step
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: the chapter on mutual exclusion with partial synchrony, which treats Fischer's algorithm
  - paper: doi:10.1109/REAL.1992.242680
    title: Rajeev Alur and Gadi Taubenfeld, Results about fast mutual exclusion, Proceedings of the 13th IEEE Real-Time Systems Symposium, 1992, pages 12-21
    locator: fast mutual exclusion with and without timing assumptions
---

Fischer's algorithm solves the deadlock free form of the [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes with only one shared read/write register $x$. It is not an asynchronous algorithm: it needs a known bound $\Delta$ on the time between the read and the write of a process, and it makes each process wait for a time $D > \Delta$ before it checks $x$. With this timing, a process that runs alone enters in 4 steps and one delay, for any $n$. Without it, the algorithm is wrong: if a step takes longer than the delay, two processes can be in the critical section at the same time. Lamport published the algorithm in 1987 and credited it to Michael Fischer.

## In plain words

There is one board, $x$. To enter, you wait until the board is empty, write your name on it, and then wait for a fixed time $D$. After that you look at the board again. If your name is still there, you go in. If another name is there, someone wrote after you, so you go back and wait until the board is empty again. When you leave, you clean the board.

The wait is the trick. Everyone who saw an empty board writes within the time $\Delta$. If you wait longer than that, all of those writes are done when you look again, and only the last writer sees its own name. If someone is slower than your wait, they can write after you look, see their own name, and go in while you are inside.

## The problem

There are $n \ge 2$ processes with the names $1, \ldots, n$. Each one repeats a remainder section, an entry section, a critical section and an exit section. The entry and exit sections must give mutual exclusion and deadlock freedom, as the [mutual exclusion problem](/mutual-exclusion-problem/) defines. The shared memory has one atomic read/write register $x$ with the values $0, 1, \ldots, n$.

The model is not asynchronous. There is a known time bound $\Delta$: a process that reads $x = 0$ writes $x$ at most $\Delta$ time units later. A process can delay itself for at least a given time $D$. The [lower bound of Burns and Lynch](/mutual-exclusion-lower-bounds/) says that an asynchronous algorithm from read/write registers needs $n$ registers, so one register is only possible because of the timing.

## The algorithm

The shared register $x$ is 0 at the start, which means "free".

```pseudo id=main
LOCK(i)
L1  loop
L2      await x = 0
L3      x ← i
L4      delay for D time units
L5      if x = i then exit the loop
UNLOCK(i)
L6  x ← 0
```

L2 is a loop of reads, and the read that sees $x = 0$ ends it. The time from that read to the write at L3 must be at most $\Delta$. The delay at L4 must be at least $D$, and the algorithm needs $D > \Delta$. If the check at L5 fails, the process goes back to L2.

The implementation is a small timed simulator. Time is an integer, and each process has a window for its next step: at most $\Delta$ after the read of $x = 0$, from $D$ to $D + \Delta$ after the write, and at most $\Delta$ after every other step of the entry and exit. A process can stay in the remainder or the critical section for any time. Several steps can happen at the same time, in any order. `search` tries all timed runs for small $n$, $\Delta$ and $D$, and `replay` checks one given run. Process $i$ of the code has the name $i + 1$.

## Example

Two processes with $\Delta = 2$ and $D = 3$. Both read $x = 0$ at time 0.

| time | process | action | $x$ |
|---|---|---|---|
| 0 | 1 | reads $x = 0$ | 0 |
| 0 | 2 | reads $x = 0$ | 0 |
| 1 | 1 | $x \leftarrow 1$ and starts the delay | 1 |
| 2 | 2 | $x \leftarrow 2$ and starts the delay | 2 |
| 4 | 1 | reads $x = 2$, not its name: back to L2 | 2 |
| 5 | 2 | reads $x = 2$: enters | 2 |
| 5 | 1 | reads $x = 2$ at L2 and waits | 2 |

Process 2 wrote last, so it sees its own name. Process 1 started its delay before the write of process 2, but the delay is longer than $\Delta$, so the write of process 2 is done when process 1 checks.

Now let $D = 1$, which is less than $\Delta$. Both read $x = 0$ at time 0, and process 1 writes $x \leftarrow 1$ at time 0. At time 1 it checks, sees $x = 1$ and enters. Process 2 is slow but still in its bound: it writes $x \leftarrow 2$ at time 2, checks at time 3, sees $x = 2$ and enters too. The test file replays both runs.

## Correctness

The full proof is in proofs/correctness.md.

- **Mutual exclusion, if $D > \Delta$.** Suppose $q$ enters while $p$ is inside. Then $q$ wrote $x$ after the check of $p$, because the write of each one must be the last write before its own check. But $q$ read $x = 0$ before the write of $p$, as $x \ne 0$ from that write on. So the write of $q$ is at most $\Delta$ after the write of $p$, and the check of $p$ is at least $D > \Delta$ after it. This is a contradiction.
- **The bound is tight in this model.** If $D = \Delta$, the write of $q$ can come at the same instant as the check of $p$, just after it. The simulator finds this run.
- **Deadlock freedom.** If no process enters, $x$ is never written 0 again. Once $x \ne 0$, each process writes at most once more, and the last writer sees its own name. This does not need $D > \Delta$.
- **No starvation freedom.** One process can write last in each round, so another process can lose forever. The proof file gives a timed run.

The test file checks all timed runs of the simulator for 2 and 3 processes and $\Delta = 1, 2, 3$. For each of these, two processes can be in the critical section at the same time if and only if $D \le \Delta$. For example, with 2 processes and $\Delta = 2$, the search covers 255 states for $D = 3$ and finds no violation, and with 3 processes it covers 6108 states. The test file also replays the run found for $D = \Delta$, the broken run with $D = 1$ above, the solo run, and the starvation cycle of the proof file.

## Complexity

| measure | value |
|---|---|
| shared registers | 1, with $n + 1$ values |
| passage without contention | 4 accesses: read $x = 0$, write $x$, read $x$ after the delay, write $x \leftarrow 0$ |
| time without contention | $D$ plus a constant number of steps |
| bypass | no bound |
| RMRs per passage | unbounded in both the CC and the DSM model |

The delay costs time even without contention, since $D$ must be larger than the worst time of a step, not its usual time. Under contention a process can wait at L2 for any time, and it can lose the check at L5 again and again.

## Properties

- Uses one atomic read/write register with $n$ writers.
- Mutual exclusion holds only if $D > \Delta$. Deadlock freedom holds for any $D$, as long as each process takes its steps.
- Not starvation free and not FCFS.
- A process alone enters after a constant number of steps, for any $n$.
- All processes run the same code, up to the names.

## Variants and improvements

- **Lamport's fast algorithm.** In the same paper, Lamport gave the [fast mutual exclusion algorithm](/lamport-fast-mutex/), which has the same kind of fast path but needs no timing, at the cost of $n + 2$ registers.
- **Resilience to timing faults.** If a step can sometimes take longer than $\Delta$, Fischer's algorithm loses mutual exclusion. Later work on timing based mutual exclusion asks for algorithms that stay safe when the timing fails and are only slower then, for example by a combination with an asynchronous algorithm.
- **Hardware locks.** With [test-and-set](/test-and-set/) or compare-and-swap, a [spin lock](/spin-lock/) needs one register and no timing.

## When to use it

Use it to study timing based algorithms and the proof methods for real time systems; it is a standard example for timed automata and model checkers. It can be used in a system where the time of each step has a hard bound, for example on some embedded hardware without interrupts. Do not use it on a normal operating system: a process can be stopped for any time by the scheduler, a page fault or an interrupt, and then mutual exclusion fails.

## Pitfalls

**The delay is too short.** The algorithm is only correct if $D > \Delta$, where $\Delta$ is the worst time from the read of $x = 0$ to the write, not the usual time. One slow write after a preemption can break it. The test file finds a run for each $D \le \Delta$.

**The read and the write are far apart.** The bound $\Delta$ covers the time from the read at L2 to the write at L3. Code between them, or an interrupt, makes this time longer.

**Weak memory.** The write at L3 must be visible to the others before the check at L5. On hardware with a store buffer, the time until a write is visible is part of $\Delta$.

**Starvation.** A process can lose at L5 forever. The proof file gives a run.

## Implementations

## History

Lamport published the algorithm in 1987, in his paper on fast mutual exclusion in ACM Transactions on Computer Systems, and credited it to Michael Fischer. The paper then gives an algorithm with a fast path that needs no timing. The algorithm became a standard example for the verification of real time systems. Lynch's book of 1996 treats it in the part on partially synchronous systems, and Alur and Taubenfeld (1992) studied fast mutual exclusion with and without timing.

## References
