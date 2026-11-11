---
tag: XQXAGT
kind: algorithm
slug: burns-lamport-algorithm
name: Burns-Lamport algorithm
aliases:
- one-bit mutual exclusion
area: concurrency/mutual-exclusion
level: advanced
summary: An n-process mutual exclusion algorithm that uses one boolean single-writer register per process; it is deadlock free but not starvation free, and n registers is the least possible.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes}
  space: {shared: Θ(n)}
  steps: {solo: Θ(n)}
  rmr: {cc: ∞, dsm: ∞}
  bypass: {worst: ∞}
properties: {deterministic: true, deadlock_free: true, starvation_free: false, fcfs: false, bounded_bypass: false, single_writer: true, bounded_registers: true, local_spinning: false}
history:
  year: 1981
  people: [James E. Burns, Leslie Lamport]
  note: Burns found it in his 1981 thesis, and Lamport found it on his own and published it in 1986 as the one-bit algorithm. Burns and Lynch showed that n registers are needed.
prereqs: [mutual-exclusion-problem]
see_also: [mutual-exclusion-lower-bounds, lamport-fast-mutex, dijkstra-mutex-algorithm, lamport-bakery-algorithm, szymanski-algorithm, deadlock-freedom, starvation-freedom]
sources:
  - paper: doi:10.1145/5383.5385
    title: Leslie Lamport, The mutual exclusion problem, part II, statement and solutions, Journal of the ACM 33(2), 1986, pages 327-348
    locator: the one-bit algorithm, with one boolean variable per process
  - paper: doi:10.1006/inco.1993.1065
    title: James E. Burns and Nancy A. Lynch, Bounds on shared memory for mutual exclusion, Information and Computation 107(2), 1993, pages 171-184
    locator: the result that n binary shared variables are necessary and sufficient for deadlock free mutual exclusion of n processes
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 10, Mutual Exclusion, the section on Burns' algorithm with single-writer binary registers
---

The Burns-Lamport algorithm solves the deadlock free form of the [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes with one boolean register per process, and only its owner writes it. A process gives way to every process with a lower number, and waits for every process with a higher number. This is the least shared memory possible: Burns and Lynch proved that any deadlock free algorithm for $n$ processes from read/write registers needs $n$ registers. The price is fairness. A process with a high number can wait forever while lower processes enter again and again. Burns found the algorithm in his 1981 thesis, and Lamport found it on his own and published it in 1986.

## In plain words

Each process has one flag. To enter, you raise your flag. Then you look at the flags of all processes with a lower number. If one of them is up, you lower your flag, wait until that flag is down, and start again. If all of them are down, you keep your flag up and look at the processes with a higher number: you wait until each of their flags is down. Then you enter. When you leave, you lower your flag.

So lower numbers have priority. A lower process never lowers its flag for a higher one, and a higher process always steps back for a lower one. This rule makes sure that someone gets in, but it does not make sure that you get in.

## The problem

There are $n \ge 2$ asynchronous processes $0, \ldots, n - 1$. Each one repeats a remainder section, an entry section, a critical section and an exit section. The entry and exit sections must give mutual exclusion and deadlock freedom, as the [mutual exclusion problem](/mutual-exclusion-problem/) defines. The shared memory has atomic read/write registers and is sequentially consistent. A process stays in its critical section for a finite time. Each process knows its own number $i$. Starvation freedom is not asked for.

## The algorithm

Each process $i$ has one boolean register $x[i]$, false at the start.

```pseudo id=main
LOCK(i)
L1  loop
L2      x[i] ← true
L3      for j ← 0 to i − 1
L4          if x[j] then
L5              x[i] ← false
L6              await not x[j]
L7              start the next round of the loop at L2
L8  for j ← i + 1 to n − 1
L9      await not x[j]
UNLOCK(i)
L10 x[i] ← false
```

L2 to L7 are the *lower check*: the process goes on only when it has seen every lower flag down while its own flag is up. L8 and L9 are the *higher wait*: the process keeps its flag up and waits for each higher flag in turn. A process that is past the lower check never lowers its flag before it enters, so every higher process steps back for it.

This is the form in Lamport's paper. Burns' form, as Lynch gives it, differs in small details of the order of the checks. This page and its code use Lamport's form.

## Example

Two processes, both flags false at the start. The test file runs this schedule step by step.

| step | process | action | $x[0]$, $x[1]$ |
|---|---|---|---|
| 1 | 1 | $x[1] \leftarrow$ true; reads $x[0]$ = false; no higher process; enters | false, true |
| 2 | 0 | $x[0] \leftarrow$ true; reads $x[1]$ = true and waits at L9 | true, true |
| 3 | 1 | leaves: $x[1] \leftarrow$ false | true, false |
| 4 | 1 | $x[1] \leftarrow$ true; reads $x[0]$ = true; $x[1] \leftarrow$ false; waits at L6 | true, false |
| 5 | 0 | reads $x[1]$ = false; enters | true, false |
| 6 | 0 | leaves: $x[0] \leftarrow$ false | false, false |
| 7 | 1 | reads $x[0]$ = false; goes back to L2 | false, false |
| 8 | 0 | $x[0] \leftarrow$ true | true, false |
| 9 | 1 | $x[1] \leftarrow$ true; reads $x[0]$ = true; $x[1] \leftarrow$ false; waits at L6 | true, false |
| 10 | 0 | reads $x[1]$ = false; enters | true, false |

After step 10 the state is the same as after step 5. So steps 6 to 10 can repeat forever: process 1 takes steps in each round, but it never enters. This is the starvation run.

## Correctness

The full proof is in proofs/correctness.md.

- **Mutual exclusion.** Suppose $p < q$ are both inside. Each one wrote its flag true for the last time before it entered and kept it up. Process $q$ read $x[p]$ false at L4 after its own last write, so that read came before the last write of $p$. Then $p$ read $x[q]$ at L9 after that, when $x[q]$ was up. This is a contradiction.
- **Deadlock freedom.** Suppose no process enters from some time on. The lowest waiting process $m$ then passes the lower check and keeps its flag up forever. Take the highest process $h$ that is past the lower check. Each process above $h$ that still tries meets the flag of $m$ first in its lower check, so it lowers its own flag and waits on $m$ forever. So $h$ sees all higher flags down and enters, which is a contradiction.
- **Process 0 cannot starve.** Its flag stays up from its first write, so each other process enters at most once more before process 0 does.
- **Other processes can starve.** The example above is a fair run in which process 1 never enters.

The test file checks mutual exclusion and deadlock freedom by exhaustive search of all interleavings: for 2 processes with one passage each (48 states) and forever (60 states), and for 3 processes with one passage each (675 states) and forever (1039 states). For 3 processes forever, it finds starvation runs for processes 1 and 2 and none for process 0, and it finds that the number of entries of others before a waiting process enters has no bound for processes 1 and 2. It also runs the starvation cycle above and checks that it comes back to the same state.

## Complexity

| measure | value |
|---|---|
| shared registers | $n$ boolean single-writer registers, which is the least possible |
| entry without contention | $n$ steps: 1 write and $n - 1$ reads |
| exit | 1 write |
| bypass | no bound for processes $1, \ldots, n - 1$ |
| RMRs per passage | unbounded in both the CC and the DSM model |

In the CC model, a process that waits at L9 on a higher flag can see that flag go up and down again and again, as the higher process starts its lower check and steps back. Each change costs one remote read. The test file finds runs with no bound for processes 1 and 2, and a bound of 7 for process 0, with 3 processes.

## Properties

- Uses atomic read/write registers only; each register has one writer and two values.
- Mutual exclusion and deadlock freedom; not starvation free and not FCFS.
- Process 0 is starvation free; the other processes are not.
- The number of registers, $n$, meets the lower bound of Burns and Lynch.
- Not symmetric: the lower numbers have priority.
- The exhaustive checks for 2 processes forever and 3 processes with one passage each also pass when each register is only *safe*, so that a read that overlaps a write can return true or false.

## Variants and improvements

- **Burns' form.** The same idea with a slightly different order of checks, as Lynch (1996) gives it.
- **Fast paths.** [Lamport's fast mutual exclusion algorithm](/lamport-fast-mutex/) adds two multi-writer registers so that a process without contention enters in a constant number of steps.
- **Starvation freedom.** The [bakery algorithm](/lamport-bakery-algorithm/) and [Szymański's algorithm](/szymanski-algorithm/) are starvation free, but they use more values per register.
- **Dijkstra (1965).** [Dijkstra's algorithm](/dijkstra-mutex-algorithm/) is also only deadlock free, and uses a multi-writer register $k$ in addition to two flags per process.

## When to use it

Use it to teach the space lower bound: it shows that $n$ boolean registers are enough for deadlock freedom, and the [lower bound](/mutual-exclusion-lower-bounds/) shows that fewer are not. Some papers use it as a building block and add fairness on top, for example the FCFS algorithm of Lycklama and Hadzilacos (1991). Do not use it as a real lock: it is not fair, it does not work on weak memory without fences, and it spins on shared flags.

## Pitfalls

**Starvation is real.** A process with a high number can wait forever while lower processes keep entering. The example above is such a run for 2 processes. Use it only where some other part of the system gives fairness.

**The order of the checks matters.** The lower check must test the flags while the process's own flag is up, and a process that finds a lower flag up must lower its own flag before it waits. If it waits with its flag up, two processes can wait for each other forever: the lower one waits at L9 for the higher flag to go down, and the higher one waits at L6 for the lower flag to go down. The test file builds this naive form and finds such a deadlock for 2 processes.

**Weak memory.** On TSO hardware such as x86, the write of true can wait in a store buffer while the process reads the other flags. The test file finds a run on the TSO model with two processes in the critical section. A fence after the write at L2 is the usual fix; the test file does not check it.

**Fixed numbers.** Each process must know a fixed number from 0 to $n - 1$, and the priority follows these numbers.

## Implementations

## History

Burns found the algorithm in his 1981 PhD thesis at the Georgia Institute of Technology, where he also showed, with Lynch, that $n$ binary shared variables are necessary and sufficient for deadlock free mutual exclusion. The journal paper of Burns and Lynch appeared in 1993. Lamport found the same algorithm on his own and published it in 1986 as the one-bit algorithm in part II of his paper on the mutual exclusion problem, where he also proved it correct.

## References
