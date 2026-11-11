---
tag: PMKEEH
kind: algorithm
slug: szymanski-algorithm
name: Szymański's algorithm
aliases:
- Szymanski mutual exclusion
area: concurrency/mutual-exclusion
level: advanced
summary: An n-process mutual exclusion algorithm with a waiting room and a door, which uses one five-valued single-writer flag per process and claims a linear bound on waiting.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes}
  space: {shared: Θ(n)}
  steps: {solo: Θ(n)}
  rmr: {cc: O(n), dsm: ∞}
  bypass: {worst: O(n)}
properties: {deterministic: true, deadlock_free: true, starvation_free: true, fcfs: false, bounded_bypass: true, single_writer: true, bounded_registers: true, local_spinning: false}
history:
  year: 1988
  people: [Bolesław K. Szymański]
  note: Published at the 1988 International Conference on Supercomputing as a simple answer to the concurrent programming problem that Lamport stated in 1986.
prereqs: [mutual-exclusion-problem, lamport-bakery-algorithm]
see_also: [eisenberg-mcguire-algorithm, filter-lock, burns-lamport-algorithm, starvation-freedom, deadlock-freedom, rmr-complexity]
sources:
  - paper: doi:10.1145/55364.55425
    title: Bolesław K. Szymański, A simple solution to Lamport's concurrent programming problem with linear wait, Proceedings of the 2nd International Conference on Supercomputing (ICS '88), 1988, pages 621-626
    locator: the algorithm with the flag values 0 to 4, and the claims of mutual exclusion, deadlock freedom and linear wait
  - paper: arxiv:2507.13198
    title: Rob van Glabbeek, Bas Luttik and Myrthe Spronck, Just verification of mutual exclusion algorithms, 2025 (a short version is in CONCUR 2025)
    locator: Table 1 and Appendix I.10, the model checking results for Szymański's algorithm
  - paper: doi:10.1145/5383.5385
    title: Leslie Lamport, The mutual exclusion problem, part II, statement and solutions, Journal of the ACM 33(2), 1986, pages 327-348
    locator: the statement of the concurrent programming problem that the title of Szymański's paper refers to
---

Szymański's algorithm solves the [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes with atomic read/write registers. Each process has one flag with five values, and only that process writes it. The processes go through a *waiting room* with a *door*. A group of processes comes into the room while the door is open. The last one in closes the door, and then the group goes into the critical section one at a time, in the order of their numbers. No new process comes in until the whole group has left. Szymański published it in 1988 and claimed that a process waits for at most a linear number of entries of others.

## In plain words

Think of a waiting room with one door. When you want to enter, you raise your hand and wait until the door is open, that is, until no one is in the room with the door closed. Then you step into the doorway. If you see that someone else still has a hand up, you wait inside the room for that person, until someone closes the door. If no one else has a hand up, you close the door yourself.

When the door is closed, the people in the room go in by number: you wait until all people with a lower number are gone. When you leave, you wait until each person with a higher number is in the room with the door closed, or is out of the game. The last person out opens the door again.

## The problem

There are $n \ge 2$ asynchronous processes $0, \ldots, n - 1$. Each one repeats a remainder section, an entry section, a critical section and an exit section. The entry and exit sections must give mutual exclusion and starvation freedom, as the [mutual exclusion problem](/mutual-exclusion-problem/) defines. The shared memory has atomic read/write registers and is sequentially consistent. A process stays in its critical section for a finite time. Each process knows its own number $i$.

## The algorithm

Each process $i$ has one register $flag[i] \in \{0, 1, 2, 3, 4\}$, 0 at the start. Only process $i$ writes it. The values mean:

| value | meaning |
|---|---|
| 0 | in the remainder section |
| 1 | wants to enter, waits for the door to open |
| 3 | in the doorway |
| 2 | in the waiting room, waits for the door to close |
| 4 | the door is closed; on the way to the critical section, or in it |

```pseudo id=main
LOCK(i)
L1  flag[i] ← 1
L2  for each j: await flag[j] < 3
L3  flag[i] ← 3
L4  if flag[j] = 1 for some j then
L5      flag[i] ← 2
L6      await flag[j] = 4 for some j
L7  flag[i] ← 4
L8  for each j < i: await flag[j] < 2
UNLOCK(i)
L9  for each j > i: await flag[j] < 2 or flag[j] = 4
L10 flag[i] ← 0
```

In all lines $j$ runs over the other processes. L2 waits until the door is open: no process is in the doorway or behind a closed door. L4 asks if some process still wants to come in. If so, the process waits in the room at L5 and L6 until some process closes the door with the value 4. The process that sees no 1 at L4 closes the door itself at L7. L8 lets the processes in the room enter by number. L9 keeps the door closed until every higher process in the room has passed L7, so that none of them is left behind in the room. The *doorway* here is the write at L1.

The implementation reads the flags one at a time. Each "for each $j$" waits on one flag at a time, in increasing order of $j$, and each "for some $j$" reads the flags in increasing order.

## Example

Two processes, both flags 0 at the start. The test file runs this schedule step by step.

| step | process | action | flags |
|---|---|---|---|
| 1 | 1 | $flag[1] \leftarrow 1$; reads $flag[0] = 0$, so the door is open | 0, 1 |
| 2 | 0 | $flag[0] \leftarrow 1$; reads $flag[1] = 1$, so the door is open | 1, 1 |
| 3 | 1 | $flag[1] \leftarrow 3$; reads $flag[0] = 1$, so it waits in the room: $flag[1] \leftarrow 2$ | 1, 2 |
| 4 | 0 | $flag[0] \leftarrow 3$; reads $flag[1] = 2$, no 1, so it closes the door: $flag[0] \leftarrow 4$; no lower process, so it enters | 4, 2 |
| 5 | 1 | reads $flag[0] = 4$; $flag[1] \leftarrow 4$; reads $flag[0] = 4$ at L8 and waits | 4, 4 |
| 6 | 0 | leaves: reads $flag[1] = 4$ at L9; $flag[0] \leftarrow 0$ | 0, 4 |
| 7 | 0 | $flag[0] \leftarrow 1$; reads $flag[1] = 4$, so the door is closed and it waits at L2 | 1, 4 |
| 8 | 1 | reads $flag[0] = 1 < 2$ at L8 and enters | 1, 4 |
| 9 | 1 | leaves: $flag[1] \leftarrow 0$ | 1, 0 |
| 10 | 0 | reads $flag[1] = 0$; $flag[0] \leftarrow 3$; no 1; $flag[0] \leftarrow 4$; enters | 4, 0 |

In step 7, process 0 comes back at once, but the door is closed, so process 1, which was already in the room, enters first.

## Correctness

The full proof of mutual exclusion is in proofs/correctness.md. It assumes that the wait at L2 ends with one atomic test of all the other flags at one instant. The implementation reads the flags one at a time, as the model of van Glabbeek, Luttik and Spronck does; for that form there is no proof on this page, only the exhaustive checks below.

- **The door lemma.** No process writes 3 at a time when another process holds 4. Take the first time this fails. Some process wrote 4 after the late process passed L2. That process either saw no 1 at L4, which is not possible while the late process has flag 1, or it saw a 4 at L6. A holder of a 4 that some process in the room has seen keeps it until that process has written 4 too, because of the waits at L8 and L9. So a 4 was present at the time the late process passed L2, which is not possible.
- **Mutual exclusion.** If $p < q$ are both in the critical section, $q$ read $flag[p] < 2$ at L8 after it wrote 4. Then $p$ wrote 3 while $q$ held 4, against the door lemma.
- **Deadlock freedom, starvation freedom and linear wait.** This page does not prove them. Szymański (1988) claims all three. van Glabbeek, Luttik and Spronck (2025) model check the algorithm and report that mutual exclusion, deadlock freedom and starvation freedom hold with atomic registers for small numbers of processes.

The test file checks mutual exclusion, deadlock freedom and starvation freedom by exhaustive search of all interleavings, with the flags read one at a time: for 2 processes with one passage each (210 states) and forever (240 states), and for 3 processes with one passage each (11565 states) and forever (14441 states). It also checks the door lemma in every reachable state for 2 and 3 processes. Counted from the write at L1, the largest number of entries of others before a process enters is 1 and 2 for $n = 2$, and 2, 3 and 4 for $n = 3$, so the worst case is $2(n - 1)$ for these sizes. From the start of the entry section, before the write at L1, there is no bound, and the algorithm is not FCFS. Seeded random schedules for 4 and 6 processes stay in the bound $2(n - 1)$.

## Complexity

| measure | value |
|---|---|
| shared registers | $n$ single-writer registers with 5 values each |
| entry without contention | $2n + 1 + i$ steps for process $i$: 3 writes, $2(n - 1)$ reads at L2 and L4, and $i$ reads at L8 |
| exit without contention | $n - i$ steps: $n - 1 - i$ reads at L9 and 1 write |
| bypass after the doorway | $O(n)$ as Szymański claims; measured $2(n - 1)$ for $n \le 3$ |
| RMRs per passage | $O(n)$ in the CC model if the linear wait bound holds (a sketch); unbounded in the DSM model |

*Sketch of the CC bound.* In the CC model, a read is remote only if another process wrote the register after the last read of this process. A process writes its flag at most 5 times per passage. While process $i$ is in its entry section, the others complete at most $B$ passages, where $B$ is the bypass bound, plus one passage each that is not complete. So $i$ makes at most $n - 1 + 5(B + n)$ remote reads, which is $O(n)$ if $B = O(n)$. The exit is similar, since the door stays closed while $i$ holds 4. The tests measure 10 and 11 RMRs for $n = 2$, and 16 to 19 for $n = 3$. In the DSM model, process $i$ waits on flags in the memory of other processes, and the tests find runs with no bound.

## Properties

- Uses atomic read/write registers only; each flag has one writer and five values.
- Mutual exclusion (proved here with Assumption A, and checked for $n \le 3$ without it); deadlock freedom and starvation freedom (claimed by Szymański, model checked by others, and checked here for $n \le 3$).
- Not FCFS: a process that writes 1 while the door is open can enter before a process that wrote 1 earlier but has a higher number.
- The processes in one batch enter in the order of their numbers.
- Not symmetric: the waits at L8 and L9 use the order of the numbers.

## Variants and improvements

- **Three boolean variables.** The literature also gives the flag as three boolean variables per process, called intent, door_in and door_out, written in a fixed order. This form is meant for weaker registers. This page does not check it.
- **The bakery.** [Lamport's bakery algorithm](/lamport-bakery-algorithm/) is FCFS and works with safe registers, but its numbers have no bound. Szymański keeps the registers bounded and gives up FCFS.
- **Eisenberg and McGuire.** The [Eisenberg-McGuire algorithm](/eisenberg-mcguire-algorithm/) has the bound $n - 1$ on waiting, but it needs a multi-writer register $turn$.
- **The filter lock.** The [filter lock](/filter-lock/) has $n - 1$ levels instead of one waiting room, and does not bound the bypass.

## When to use it

Use it to teach the waiting room idea: a batch of processes is let in at once, and the batch is served before the next one. It is a good test case for model checkers, and many tools use it as a benchmark. For a real lock, use a lock built on an atomic instruction, such as a [ticket lock](/ticket-lock/), or an MCS lock if the processes must spin on local memory.

## Pitfalls

**The wait at L2 is not one atomic test.** The proof on this page treats L2 as one test at one instant. Real code reads the flags one at a time, and a flag can change between two reads. The exhaustive checks for 2 and 3 processes find no problem with the reads one at a time, but this page has no proof for that form.

**Weak memory.** On TSO hardware such as x86, the write of 3 or 4 can wait in a store buffer while the process reads the other flags. The test file finds a run on the TSO model with two processes in the critical section.

**Safe registers.** With one five-valued flag per process, a read that overlaps a write can return any of the five values. The test file finds a run with two processes in the critical section when the flags are safe registers in this sense. The boolean form above is the one meant for weak registers.

**No bound from the start.** The bound on waiting counts from the write at L1. Before that write, other processes cannot see the process, and they can enter again and again.

**Busy waiting.** The wait at L6 scans all the flags in a loop. On a machine without caches, or in the DSM model, this makes much traffic.

## Implementations

## History

Lamport (1986) stated a hard form of the mutual exclusion problem, and asked for solutions that also tolerate weak registers and the failure of processes. Szymański (1988) gave this algorithm at the International Conference on Supercomputing as a simple solution with linear wait and a bounded number of values per register. The algorithm became a standard benchmark for model checkers, and van Glabbeek, Luttik and Spronck (2025) checked it with atomic, regular and safe registers.

## References
