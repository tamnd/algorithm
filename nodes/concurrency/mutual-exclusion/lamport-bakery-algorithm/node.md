---
tag: XJ2MAW
kind: algorithm
slug: lamport-bakery-algorithm
name: Lamport's bakery algorithm
aliases: [bakery algorithm]
area: concurrency/mutual-exclusion
level: core
summary: N-process mutual exclusion in which each process takes a ticket larger than all it sees. FCFS and starvation free, it even works with safe registers, but tickets are unbounded.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes}
  space: {shared: Θ(n)}
  steps: {solo: Θ(n)}
  rmr: {cc: Θ(n), dsm: ∞}
  bypass: {worst: n - 1}
properties: {deterministic: true, deadlock_free: true, starvation_free: true, fcfs: true, single_writer: true, bounded_registers: false, local_spinning: false}
history:
  year: 1974
  people: [Leslie Lamport]
  note: Lamport published the bakery algorithm in 1974. It was the first FCFS solution, the first that needs no register written by two processes, and it works when a read that overlaps a write returns any value.
prereqs: [mutual-exclusion-problem]
see_also: [peterson-algorithm, filter-lock, eisenberg-mcguire-algorithm, ticket-lock, szymanski-algorithm, starvation-freedom, rmr-complexity, mutual-exclusion-lower-bounds]
sources:
  - paper: doi:10.1145/361082.361093
    title: Leslie Lamport, A new solution of Dijkstra's concurrent programming problem, Communications of the ACM 17(8), 1974, pages 453-455
    locator: the algorithm, Assertions 1 to 3 with their proofs, the remark that a read overlapping a write may return any value, and the remarks on unbounded numbers
  - paper: doi:10.1007/978-3-540-30186-8_5
    title: Gadi Taubenfeld, The black-white bakery algorithm and related bounded-space, adaptive, local-spinning and FIFO algorithms, DISC 2004, LNCS 3274, pages 56-70
    locator: the black-white bakery algorithm (bounded tickets with one extra shared bit)
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 2, Mutual Exclusion (Lamport's bakery algorithm, its proofs, and bounded timestamps)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 10, Mutual Exclusion with Read/Write Shared Memory (the bakery algorithm)
---

Lamport's bakery algorithm solves the [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes with read/write registers, in the way that customers are served in a bakery: each process that wants to enter takes a ticket that is larger than every ticket it sees, and the process with the smallest ticket goes first, with ties broken by process number. It is first come, first served (FCFS) after a doorway of $O(n)$ steps, and so starvation free with bypass at most $n - 1$. Each register has one writer, and the algorithm stays correct even if a read that overlaps a write returns an arbitrary value. Its weak point is that tickets can grow without bound.

## In plain words

In a busy bakery you take a numbered ticket when you come in, and the smallest number is served next. This algorithm does the same, but there is no machine that gives out tickets. Each person looks at the tickets that the others hold and writes down a number one larger than the largest one.

Two people who look at the same time can write the same number. Then the one with the smaller name goes first.

There is one more rule. While you are choosing your number, you hold up a sign that says "choosing". Before you compare your ticket with someone's, you wait until their sign is down. Without this rule, a person who is still choosing could be passed and then pick a smaller number than yours.

## The problem

There are $n$ asynchronous processes $0, \ldots, n-1$. Each repeats a remainder section, an entry section, a critical section and an exit section, as in the [mutual exclusion problem](/mutual-exclusion-problem/). The goals are mutual exclusion, starvation freedom, and FCFS order: if process $i$ finishes its *doorway* (a part of the entry section with a bounded number of its own steps) before process $k$ starts its doorway, then $k$ does not enter before $i$. The shared memory has read/write registers, and each register is written by one process only. The registers may be *safe* in Lamport's sense: a read that overlaps a write of the same register may return any value. Processes may stay in their remainder sections forever.

## The algorithm

Process $i$ owns two registers: $choosing[i]$, false at the start, and $number[i]$, an integer that is 0 at the start. A ticket is the pair $(number[i], i)$, and pairs are compared in lexicographic order.

```pseudo id=main
LOCK(i)                                    ▷ entry section of process i
L1  choosing[i] ← true
L2  m ← max of number[j] over all j ≠ i    ▷ n − 1 reads, in any order
L3  number[i] ← m + 1
L4  choosing[i] ← false                    ▷ end of the doorway
L5  for each j ≠ i do
L6      wait until choosing[j] = false
L7      wait until number[j] = 0 or (number[j], j) > (number[i], i)
                                           ▷ critical section
UNLOCK(i)
L8  number[i] ← 0
```

The doorway is L1 to L4, with $n + 2$ shared steps and no waiting. Each wait is a loop of reads. A process with $number[j] = 0$ is not competing. Lamport numbers the processes from 1 and takes the maximum over all $n$ numbers, its own included; its own number is 0 at that point, so this is the same.

**Why $choosing$ is needed.** Without L1, L4 and L6, mutual exclusion fails. Process 0 reads $number[1] = 0$ and stops before it writes its ticket. Process 1 reads $number[0] = 0$, writes $number[1] = 1$, sees $number[0] = 0$ at L7 and enters. Process 0 now writes $number[0] = 1$, and at L7 it sees $(1, 1) > (1, 0)$, so it enters too. The test file finds exactly this run in a search of 51 states. With $choosing$, process 1 would wait at L6 until process 0 has written its ticket, and then it would see $(1, 0) < (1, 1)$ and wait.

## Example

Three processes. Process 2 has entered the critical section alone with ticket 1. Then process 0 and process 1 start at the same time while process 2 is inside.

| step | event | $number[0]$ | $number[1]$ | $number[2]$ |
|---|---|---|---|---|
| 1 | process 2 is in the critical section | 0 | 0 | 1 |
| 2 | processes 0 and 1 both read the numbers and see the maximum 1 | 0 | 0 | 1 |
| 3 | both write the ticket 2 and lower $choosing$ | 2 | 2 | 1 |
| 4 | process 0 passes process 1, since $(2, 1) > (2, 0)$, and waits for process 2, since $(1, 2) < (2, 0)$; process 1 waits for process 0, since $(2, 0) < (2, 1)$ | 2 | 2 | 1 |
| 5 | process 2 leaves and writes $number[2] = 0$ | 2 | 2 | 0 |
| 6 | process 0 reads $number[2] = 0$ and enters; process 1 still waits | 2 | 2 | 0 |
| 7 | process 2 starts again, reads the maximum 2 and takes ticket 3 | 2 | 2 | 3 |
| 8 | process 0 leaves; process 1 enters, since $(3, 2) > (2, 1)$, and process 2 waits for it | 0 | 2 | 3 |

Process 1 tied with process 0 and lost the tie on its number, but process 2, which came later, could not pass it. That is the FCFS property. The test file runs this schedule step by step.

## Correctness

The full proof is in proofs/correctness.md. It follows Lamport's three assertions, and it does not use the value of any read that overlaps a write.

- **Lemma 1.** If process $i$ is in the bakery (after its doorway) during the whole of process $k$'s read of $number[i]$ in a doorway, then $k$ chooses a ticket larger than $i$'s.
- **Lemma 2.** If $i$ is in the critical section and $k$ is in the bakery, then $(N_i, i) < (N_k, k)$, where $N$ denotes the tickets. The proof looks at the last read of $choosing[k]$ by $i$, which returned false. Either that read began before $k$ raised $choosing[k]$, and then Lemma 1 applies, or it ended after $k$ began to lower it, and then $i$'s later read of $number[k]$ saw $k$'s final ticket.
- **Mutual exclusion** follows from Lemma 2, applied in both directions.
- **FCFS.** If $i$ finished its doorway before $k$ started its doorway, then by Lemma 1, $N_k > N_i$, so $k$ cannot enter while $i$ waits.
- **Bypass at most $n - 1$.** Each other process enters at most once while $i$ waits, because its next doorway starts after $i$'s doorway.
- **Deadlock and starvation freedom.** If nobody entered, the waiting process with the smallest pair would pass all the checks. With bypass at most $n - 1$, this gives starvation freedom.

The test file explores all interleavings with atomic registers for two processes with one, two and three passages each (169, 1025 and 3241 states) and for three processes with one passage each (11035 states). It finds no state with two processes inside, no fair run in which a process waits forever, FCFS order for every process, and bypass 1 for two processes over three passages, and 2 for three processes. It also checks safe registers, the run without $choosing$, the growth of tickets, TSO, the step count, and random schedules of 4 and 6 processes.

**Safe registers.** In the safe mode of the explorer, a write takes two steps, and any read of the register between them may return any value of a finite domain: $\{0, \ldots, 4\}$ for two processes with two passages each (8666 states), and $\{0, \ldots, 3\}$ for three processes with one passage each (171093 states). No state has two processes inside. A real safe register may return any integer, so the test is a finite check, not a proof; the proof above covers all values.

## Complexity

| measure | value |
|---|---|
| shared registers | $2n$: one boolean and one unbounded integer per process, each with a single writer |
| entry without contention | $3n$ shared steps: L1, $n - 1$ reads at L2, L3, L4, and two reads for each $j \ne i$ |
| exit | 1 write |
| bypass after the doorway | at most $n - 1$ |
| RMRs per passage, CC model | $O(n)$ |
| RMRs per passage, DSM model | unbounded |

The test file counts the solo entry section: exactly $3n$ shared steps for $n = 2, 3, 4$. In the cache coherent model, a waiting process rereads $choosing[j]$ or $number[j]$ from its cache, and each other process writes its registers only a constant number of times while $i$ waits, because it enters at most once. So a passage makes $O(n)$ remote references. The test file finds at most 8 per entry section for two processes, the same for two and for three passages, and at most 12 for three processes. In the DSM model, process $i$ spins on registers in the memory modules of other processes, so the number of remote references is unbounded. Even without contention, the entry section takes $\Theta(n)$ steps, because a process reads all $n - 1$ other tickets twice. [Lamport's fast mutex](/lamport-fast-mutex/) (1987) avoids this with a constant number of steps when there is no contention.

## Properties

- Each register is written by one process only, and the algorithm needs only safe registers.
- FCFS after a doorway of $n + 2$ steps, starvation free, bypass at most $n - 1$.
- Symmetric: all processes run the same code; ties are broken by number.
- Tickets are unbounded: they can grow forever when the critical section is never empty.
- Busy waiting, not local spinning.

## Variants and improvements

- **Bounded tickets.** Lamport (1974) showed that the numbers grow without bound if there is always a process in the bakery, and he noted that a simple cyclic scheme over a finite set of integers does not fix it. Taubenfeld's *black-white bakery algorithm* (2004) bounds the tickets by $n$ with one extra shared bit, a color: a process takes the current color together with its ticket, a process that leaves sets the shared color to the color that is not its own, and processes that hold the older color go first. It keeps FCFS order and uses bounded registers. Herlihy and Shavit give a bounded timestamp scheme for the same purpose.
- **Fewer steps.** Eisenberg and McGuire (1972) bound the bypass by $n - 1$ with $n + 1$ registers, but they need a multi-writer register and are not FCFS; see [Eisenberg and McGuire's algorithm](/eisenberg-mcguire-algorithm/). [Szymański's algorithm](/szymanski-algorithm/) uses a constant number of bits per process and has linear waiting.
- **Atomic instructions.** With fetch-and-add, the [ticket lock](/ticket-lock/) gives tickets from one shared counter: $O(1)$ steps without contention, the same FCFS order, and a counter that can wrap around safely.
- **Two processes.** For $n = 2$, [Peterson's algorithm](/peterson-algorithm/) is simpler and needs only bounded registers.

## When to use it

Use it to see how FCFS order and single-writer registers can be had with reads and writes only, and as the base of many later algorithms. It is a good choice in a distributed shared memory in which each process can write only its own memory, or in which a read may return garbage when it races with a write, which was the setting of Lamport's paper. In a normal program, a [ticket lock](/ticket-lock/) or a queue lock gives the same order with $O(1)$ steps, and the system [mutex](/mutex/) is better still.

## Pitfalls

**Forgetting $choosing$.** The run in the section The algorithm shows that the wait at L6 is needed for mutual exclusion, not only for speed.

**Comparing tickets only.** Two processes can choose the same number, so the comparison must use the pair $(number[j], j)$, not $number[j]$ alone; with numbers alone, two processes with equal tickets would both wait forever.

**Overflow.** Tickets grow with the number of overlapping passages. The test file runs two processes that always overlap, and their tickets go $1, 2, 3, \ldots, 9$. Lamport estimated that, at one doorway per millisecond, the numbers stay below $2^{35}$ for a year, if no read returns a value larger than one that was written. With a 32-bit integer that can be too small, and a wrapped ticket breaks mutual exclusion.

**Memory order.** On x86, the write of $choosing[i]$ can stay in the store buffer while the reads of L2 go to memory, and the write of $number[i]$ can stay there while another process reads it. The test file finds a run of the TSO explorer with both processes inside. A full fence after L1 and another after L4 fix it: the test file finds no bad state with these two fences for two processes with one and two passages, and neither fence alone is enough (both checked by search). Under TSO the test checks only safety.

**Process failure.** Lamport allows a process to fail by going to its remainder section, after which reads of its registers may give arbitrary values for a while and then 0. A process that fails and restarts again and again can make another process wait at L6 forever, as Lamport notes.

## Implementations

## History

Leslie Lamport published the bakery algorithm in 1974 in Communications of the ACM, as a new solution of the problem that Dijkstra (1965) had posed and that Knuth (1966), de Bruijn (1967) and Eisenberg and McGuire (1972) had refined. Unlike those solutions, it is first come, first served, it does not need a register that two processes write, and it tolerates reads that return arbitrary values when they overlap a write; Lamport presented it for a system of $n$ computers, each with its own memory, that may fail. The paper calls the tolerance of overlapping reads a remarkable property, and it asks whether an FCFS algorithm with bounded registers, in which no process writes another's memory, exists. Its unbounded tickets led to many bounded variants, among them Taubenfeld's black-white bakery algorithm (2004).

## References
