---
tag: Y50GY4
kind: algorithm
slug: eisenberg-mcguire-algorithm
name: Eisenberg-McGuire algorithm
area: concurrency/mutual-exclusion
level: advanced
summary: An n-process mutual exclusion algorithm from read/write registers in which a leaving process gives the turn to the next waiting process, so a waiting process is passed at most n - 1 times.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes}
  space: {shared: Θ(n)}
  steps: {solo: Θ(n)}
  rmr: {cc: ∞, dsm: ∞}
  bypass: {worst: n - 1}
properties: {deterministic: true, deadlock_free: true, starvation_free: true, fcfs: false, bounded_bypass: true, single_writer: false, bounded_registers: true, local_spinning: false}
history:
  year: 1972
  people: [Murray A. Eisenberg, Michael R. McGuire]
  note: A one-page letter to Communications of the ACM that lowered the worst wait of the Knuth and de Bruijn solutions to n - 1 turns.
prereqs: [mutual-exclusion-problem, knuth-mutex-algorithm]
see_also: [dijkstra-mutex-algorithm, lamport-bakery-algorithm, szymanski-algorithm, starvation-freedom, deadlock-freedom, ticket-lock]
sources:
  - paper: doi:10.1145/355606.361895
    title: Murray A. Eisenberg and Michael R. McGuire, Further comments on Dijkstra's concurrent programming control problem, Communications of the ACM 15(11), 1972, page 999
    locator: the algorithm with the flags IDLE, WAITING and ACTIVE and the shared turn, and the claim that a process waits at most n - 1 turns
  - paper: doi:10.1145/355592.365595
    title: Donald E. Knuth, Additional comments on a problem in concurrent programming control, Communications of the ACM 9(5), 1966, pages 321-322
    locator: the earlier starvation free solution that this algorithm improves
  - paper: doi:10.1145/363162.363167
    title: N. G. de Bruijn, Additional comments on a problem in concurrent programming control, Communications of the ACM 10(3), 1967, pages 137-138
    locator: the earlier bound of n(n - 1)/2 turns
  - paper: doi:10.1145/365559.365617
    title: E. W. Dijkstra, Solution of a problem in concurrent programming control, Communications of the ACM 8(9), 1965, page 569
    locator: the statement of the problem
---

The Eisenberg-McGuire algorithm solves the [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes with atomic read/write registers. It is a refinement of [Knuth's algorithm](/knuth-mutex-algorithm/): each process has a three-valued flag, and a shared register $turn$ gives one process the highest priority. The new step is in the exit section: a leaving process scans forward from its own number and gives $turn$ to the first process that is not idle. So the turn always moves toward a waiting process, and a process that has made its first write waits for at most $n - 1$ entries of others. Eisenberg and McGuire published it in 1972 as a one-page letter.

## In plain words

The processes sit around a table, and a token $turn$ points at one seat. A process that wants to enter raises its flag to WAITING. It then looks at the seats from the token forward to its own seat. If any of them is not idle, it starts this look again from the token. If all are idle, it raises its flag to ACTIVE and checks that no other flag is ACTIVE, and that the token is at its own seat or at an idle seat. If all is well, it takes the token and enters. If not, it goes back to WAITING and tries again.

When it leaves, it walks forward from its seat and puts the token on the first seat whose flag is up. So the token always moves to someone who waits, and no one is passed more than once per seat.

## The problem

There are $n \ge 2$ asynchronous processes $0, \ldots, n - 1$. Each one repeats a remainder section, an entry section, a critical section and an exit section. The entry and exit sections must give mutual exclusion and starvation freedom, as the [mutual exclusion problem](/mutual-exclusion-problem/) defines. The shared memory has atomic read/write registers and is sequentially consistent. A process stays in its critical section for a finite time. All processes run the same code.

## The algorithm

Each process $i$ has a register $flag[i] \in \{\text{IDLE}, \text{WAITING}, \text{ACTIVE}\}$, IDLE at the start. The shared register $turn$ holds a process number. Process numbers are taken mod $n$.

```pseudo id=main
LOCK(i)
L1  loop
L2      flag[i] ← WAITING
L3      j ← turn                           ▷ phase 1: scan turn, turn + 1, ..., i − 1
L4      while j ≠ i
L5          if flag[j] ≠ IDLE then j ← turn else j ← j + 1
L6      flag[i] ← ACTIVE                   ▷ phase 2
L7      for each j ≠ i
L8          if flag[j] = ACTIVE then start the next round of the loop at L2
L9      t ← turn
L10     if t = i or flag[t] = IDLE then exit the loop
L11 turn ← i
                                           ▷ critical section
UNLOCK(i)
L12 j ← turn + 1
L13 while flag[j] = IDLE: j ← j + 1
L14 turn ← j
L15 flag[i] ← IDLE
```

The *doorway* is the first write at L2. Phase 1 lets a process go on only when every process from $turn$ forward to it is idle. Phase 2 is the test of [Dijkstra's algorithm](/dijkstra-mutex-algorithm/): no other process may be ACTIVE. The test at L10 is new: the holder of the turn must be idle, or be the process itself. The paper writes L9 and L10 as one condition; here $turn$ is read once into $t$.

## Example

Three processes, $turn = 0$ at the start. The test file runs this schedule step by step.

| step | process | action | $turn$ |
|---|---|---|---|
| 1 | 0 | WAITING; $turn = 0$ is itself; ACTIVE; no other flag is ACTIVE; $t = 0$ is itself; $turn \leftarrow 0$; enters | 0 |
| 2 | 2 | WAITING; reads $turn = 0$ and $flag[0] = $ ACTIVE; reads $turn = 0$ again | 0 |
| 3 | 1 | WAITING; reads $turn = 0$ and $flag[0] = $ ACTIVE; reads $turn = 0$ again | 0 |
| 4 | 0 | leaves: reads $turn = 0$, then $flag[1] = $ WAITING, so $turn \leftarrow 1$; $flag[0] \leftarrow$ IDLE | 1 |
| 5 | 2 | reads $flag[0] = $ IDLE and $flag[1] = $ WAITING; reads $turn = 1$ | 1 |
| 6 | 1 | reads $flag[0] = $ IDLE, so it comes to itself; ACTIVE; no other flag is ACTIVE; $t = 1$ is itself; enters | 1 |
| 7 | 2 | reads $flag[1] = $ ACTIVE; reads $turn = 1$ again | 1 |
| 8 | 1 | leaves: reads $turn = 1$, then $flag[2] = $ WAITING, so $turn \leftarrow 2$; $flag[1] \leftarrow$ IDLE | 2 |
| 9 | 2 | reads $flag[1] = $ IDLE, so it comes to itself; ACTIVE; no other flag is ACTIVE; $t = 2$ is itself; enters | 2 |

In step 4, process 0 gives the turn to process 1, the first process after it that is not idle. In step 8, process 1 gives it to process 2. Each waiting process is served in the cyclic order from the leaving process.

## Correctness

The full proof is in proofs/correctness.md.

- **Mutual exclusion.** A process keeps its flag ACTIVE from L6 of the round in which it enters until the end of its exit. If $q$ enters before $j$, then $j$ must read $flag[q] \ne$ ACTIVE in phase 2; the proof shows that this read comes after $q$ has finished its exit. So at most one process is in the critical or exit section at a time.
- **Bypass at most $n - 1$.** Fix a waiting process $i$ after its doorway, and measure the distance $d(x)$ from $x$ forward to $i$. A leaving process $j$ gives the turn to the first process $z$ after it that is not idle; since $i$ is not idle, $d(z) < d(j)$. The next process to enter must read $turn = z$ at L9, and $flag[z]$ is still not idle, so the next process to enter is $z$ itself. So the distances of the processes that enter before $i$ go down strictly, from at most $n - 1$, and there are at most $n - 1$ of them.
- **Deadlock freedom.** If no process enters, $turn$ is constant. The first trying process in the forward order from $turn$ passes phase 1, and all the others stay in phase 1, with flag WAITING. So the first one passes phase 2 and L10, and enters.
- **Starvation freedom** follows from the two points before.

The test file checks mutual exclusion, deadlock freedom and starvation freedom by exhaustive search of all interleavings: for 2 processes with one passage each (693 states) and forever (1829 states), and for 3 processes with one passage each (40273 states). The largest number of entries of others after the doorway is $n - 1$: 1 for $n = 2$ and 2 for $n = 3$. From the start of the entry section, before the first write, there is no bound, and the algorithm is not FCFS. The test file also runs the example above and seeded random schedules for 4 and 6 processes, in which the bypass reaches $n - 1$ and no more. A single run outside the test file searched 3 processes forever (225494 states, about 30 seconds) and found no violation; it is too slow for the test file.

## Complexity

| measure | value |
|---|---|
| shared registers | $n + 1$: $flag[0..n-1]$ with three values each, and $turn$ |
| entry without contention | $n + 4$ steps for the holder of the turn; one more read per idle process from $turn$ to $i$, and one read at L10 |
| exit | 1 read of $turn$, up to $n$ reads of flags, 2 writes |
| bypass after the doorway | at most $n - 1$, and this is reached |
| RMRs per passage | unbounded in both the CC and the DSM model |

Without contention, the process that holds the turn writes WAITING, reads $turn$, writes ACTIVE, reads $n - 1$ flags, reads $turn$ and writes $turn$. The exit is wait free but takes $\Theta(n)$ steps, since the leaving process scans until it finds a flag that is not IDLE, and its own flag stops the scan.

## Properties

- Uses atomic read/write registers only; each $flag[i]$ has three values and one writer; $turn$ has $n$ writers.
- Mutual exclusion, deadlock freedom, starvation freedom and bypass at most $n - 1$ after the doorway.
- Not FCFS: a process that starts later but sits closer to the turn can enter first.
- The exit section is wait free.
- Symmetric: all processes run the same code.

## Variants and improvements

- **Knuth (1966) and de Bruijn (1967).** The same flags and turn, with the bounds $2^{n-1} - 1$ and $n(n - 1)/2$. The [Knuth algorithm](/knuth-mutex-algorithm/) page has the details.
- **The bakery.** [Lamport's bakery algorithm](/lamport-bakery-algorithm/) (1974) is FCFS, needs only single-writer registers, and still works when a read that overlaps a write returns any value. Its numbers have no bound.
- **Szymański (1988).** [Szymański's algorithm](/szymanski-algorithm/) has linear wait and a constant number of single-writer flags per process.

## When to use it

Use it as the textbook n-process solution with a tight bound on waiting from read/write registers only. It is a good example of a proof by a measure that goes down. For a real lock, use a lock built on an atomic instruction: a [ticket lock](/ticket-lock/) gives FCFS order, and an MCS lock also spins locally.

## Pitfalls

**Do not drop the test at L10 without a new proof.** The proof of the bound $n - 1$ uses it to show that the next process to enter is the one that got the turn. An exhaustive search with the test removed, for 2 processes forever and 3 processes with one passage each, found no run that breaks the bound. So this page does not claim that the test is needed, only that the proof here needs it.

**The exit scan starts at $turn + 1$.** It must go forward from the leaving process and stop at the first flag that is not IDLE. A scan from another place can give the turn to a process far from the waiting one.

**Weak memory.** On TSO hardware such as x86, the write of ACTIVE can wait in a store buffer while the process reads the other flags. The test file finds a run on the TSO model with two processes in the critical section. With a fence after each write of $flag[i]$ in the entry section (after L2 and L6), the test file finds no such run for 2 and 3 processes with one passage each. [Dekker's algorithm](/dekker-algorithm/) has the same problem.

**Busy waiting.** A waiting process reads shared registers in a loop, and each round of the outer loop writes its flag. On a cache coherent machine this makes much traffic.

## Implementations

## History

Dijkstra (1965) stated the problem. Knuth (1966) gave the first solution in which no process can wait forever, and de Bruijn (1967) lowered its worst wait to $n(n - 1)/2$ turns. Eisenberg and McGuire (1972), in a one-page letter to Communications of the ACM, changed the exit section so that the turn goes to the next process that is not idle, and got $n - 1$ turns. Lamport's bakery algorithm (1974) then gave FCFS order with single-writer registers.

## References
