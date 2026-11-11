---
tag: YTPF2R
kind: algorithm
slug: knuth-mutex-algorithm
name: Knuth's mutual exclusion algorithm
aliases: [Knuth 1966 mutex]
area: concurrency/mutual-exclusion
level: advanced
summary: The first starvation free mutual exclusion for n processes (1966). A leaving process passes the turn on, so a waiting process is passed at most 2^(n-1) - 1 times.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes}
  space: {shared: Θ(n)}
  steps: {solo: Θ(n)}
  rmr: {cc: ∞, dsm: ∞}
  bypass: {worst: 2^(n-1) - 1}
properties: {deterministic: true, deadlock_free: true, starvation_free: true, fcfs: false, bounded_bypass: true, single_writer: false, bounded_registers: true, local_spinning: false}
history:
  year: 1966
  people: [Donald E. Knuth, N. G. de Bruijn]
  note: Knuth pointed out that Dijkstra's 1965 solution lets a process wait forever and gave a solution without this flaw. De Bruijn (1967) changed it to lower the worst wait.
prereqs: [mutual-exclusion-problem, dijkstra-mutex-algorithm]
see_also: [eisenberg-mcguire-algorithm, lamport-bakery-algorithm, dekker-algorithm, starvation-freedom, starvation, deadlock-freedom]
sources:
  - paper: doi:10.1145/355592.365595
    title: Donald E. Knuth, Additional comments on a problem in concurrent programming control, Communications of the ACM 9(5), 1966, pages 321-322
    locator: the algorithm with control[i] in {0, 1, 2} and the turn k, and the remark that Dijkstra's solution allows a process to wait forever
  - paper: doi:10.1145/363162.363167
    title: N. G. de Bruijn, Additional comments on a problem in concurrent programming control, Communications of the ACM 10(3), 1967, pages 137-138
    locator: the change to Knuth's exit section that lowers the worst wait to n(n-1)/2 turns
  - paper: doi:10.1145/365559.365617
    title: E. W. Dijkstra, Solution of a problem in concurrent programming control, Communications of the ACM 8(9), 1965, page 569
    locator: the problem and the solution that Knuth's algorithm improves
  - url: "https://lamport.azurewebsites.net/pubs/dijkstra.pdf"
    title: Leslie Lamport, Dijkstra Book, Chapter on Concurrent Algorithms, 2021
    locator: Section 2.5, the remark that Knuth's algorithm was the first starvation free and symmetric n-process solution
---

Knuth's algorithm is the first solution to the [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes that is starvation free. Knuth published it in 1966, eight months after [Dijkstra's algorithm](/dijkstra-mutex-algorithm/), and pointed out that Dijkstra's solution lets a process wait forever. Knuth kept the shared turn $k$ but changed how it moves: a process that leaves the critical section gives the turn to the next process in a fixed cyclic order. Each process has one register with three values. A process that has made its first write is passed at most $2^{n-1} - 1$ times; de Bruijn (1967) changed the algorithm to lower this to $n(n - 1)/2$.

## In plain words

The processes sit around a table, and a token $k$ points at one seat. Seats are ranked from the token downward: the seat of the token first, then the seat below it, and so on around the table.

A process that wants to enter first raises a flag (value 1). It then looks at all the seats ranked above its own. If any of them has a flag up, it starts over. If none has, it raises its flag higher (value 2) and checks that no one else has a flag at 2. If someone has, it goes back to 1 and starts over. If no one has, it enters.

When it leaves, it moves the token to the seat below its own. So the processes after it in the order get a better rank, and no process can be skipped forever.

## The problem

There are $n \ge 2$ asynchronous processes $0, \ldots, n - 1$. Each one repeats a remainder section, an entry section, a critical section and an exit section. The entry and exit sections must give mutual exclusion and starvation freedom, as the [mutual exclusion problem](/mutual-exclusion-problem/) defines. The shared memory has atomic read/write registers and is sequentially consistent. A process stays in its critical section for a finite time. As in Dijkstra's paper, all processes run the same code.

## The algorithm

Each process $i$ has a register $control[i] \in \{0, 1, 2\}$, 0 at the start. The shared register $k$ holds a process number. Process numbers are taken mod $n$. Knuth numbers the processes from 1 to $N$; here they go from 0 to $n - 1$.

```pseudo id=main
LOCK(i)
L1  loop
L2      control[i] ← 1
L3      j ← k                              ▷ phase 1: scan k, k − 1, ..., i + 1
L4      while j ≠ i: if control[j] = 0 then j ← j − 1
L5          else go back to L3
L6      control[i] ← 2                     ▷ phase 2
L7      for each j ≠ i
L8          if control[j] = 2 then start the next round of the loop at L2
L9      exit the loop
L10 k ← i
                                           ▷ critical section
UNLOCK(i)
L11 k ← i − 1
L12 control[i] ← 0
```

The *doorway* is the first write at L2. Phase 1 lets a process go on only if every process ranked above it, from $k$ down to $i + 1$, is idle. Phase 2 is the same test as in Dijkstra's algorithm: a process enters only if no other process has $control = 2$. The order of the scan in phase 1 matters; the order in phase 2 does not.

## Example

Two processes, $k = 0$ at the start. The test file runs this schedule step by step.

| step | process | action | $k$ |
|---|---|---|---|
| 1 | 1 | $control[1] \leftarrow 1$; reads $k = 0$ and $control[0] = 0$: phase 1 done | 0 |
| 2 | 0 | $control[0] \leftarrow 1$; reads $k = 0$, which is itself, so phase 1 is empty; $control[0] \leftarrow 2$; reads $control[1] = 1$; $k \leftarrow 0$; enters | 0 |
| 3 | 1 | $control[1] \leftarrow 2$; reads $control[0] = 2$, so back to L2: $control[1] \leftarrow 1$; reads $k = 0$ and $control[0] = 2$: back to L3 | 0 |
| 4 | 0 | leaves: $k \leftarrow 1$, $control[0] \leftarrow 0$ | 1 |
| 5 | 0 | starts again: $control[0] \leftarrow 1$; reads $k = 1$ and $control[1] = 1$: back to L3 | 1 |
| 6 | 1 | reads $k = 1$, which is itself; $control[1] \leftarrow 2$; reads $control[0] = 1$; $k \leftarrow 1$; enters | 1 |

In step 4 process 0 hands the turn to process 1. In step 5 process 0 comes back at once, but now process 1 is ranked above it, so process 0 waits. In Dijkstra's algorithm, process 0 could have entered again.

## Correctness

The full proof is in proofs/correctness.md.

- **Mutual exclusion.** As in Dijkstra's algorithm: a process enters only after it wrote $control[i] \leftarrow 2$ and then read no other 2, and it keeps the value 2 until it leaves. Of two processes in the critical section, the one that wrote 2 later would have read the 2 of the other.
- **Deadlock freedom.** If processes loop forever and no one enters, $k$ does not change. The trying process ranked highest from $k$ passes phase 1 every time, and every other trying process fails phase 1, because its scan meets the highest one. So the others stay at 1, and the highest one passes phase 2.
- **Starvation freedom.** Fix a waiting process $i$ and rank the process numbers by their distance $d$ from $i$ going down: $d(i) = 0$, $d(i + 1) = 1$, and so on. A process that passes phase 1 while $i$ waits is never farther from $i$ than the value of $k$ that it read, because otherwise its scan would meet $i$. The largest distance among $k$ and the values of $k$ that processes have read never grows, and it shrinks in the end: the process at the largest distance can enter at most once more, and then its leaving hands $k$ to a smaller distance. When the largest distance is 0, no other process can enter. Since others enter as long as $i$ waits, $i$ cannot wait forever.
- **Bounded waiting.** The bound $2^{n-1} - 1$ is not proved on this page. The test file checks it by exhaustive search for $n = 2$ and $n = 3$, and finds that it is reached.

The test file checks mutual exclusion, deadlock freedom and starvation freedom by exhaustive search of all interleavings: for 2 processes with one passage each (256 states) and forever (622 states), and for 3 processes with one passage each (11504 states) and forever (52250 states). The largest number of entries of others after the doorway is 1 for $n = 2$ and 3 for $n = 3$. The algorithm is not FCFS. The test file also runs the example above and seeded random schedules for 4 and 6 processes.

## Complexity

| measure | value |
|---|---|
| shared registers | $n + 1$: $control[0..n-1]$ with three values each, and $k$ |
| entry without contention | phase 1 reads up to $n - 1$ registers and phase 2 reads $n - 1$: $\Theta(n)$ steps |
| exit | 2 writes |
| bypass after the doorway | at most $2^{n-1} - 1$ (Knuth); $n(n - 1)/2$ with de Bruijn's change |
| RMRs per passage | unbounded in both the CC and the DSM model |

A process that runs alone with $k = 0$ takes $n + 3$ steps to enter if it is process 0, and $2n + 2$ steps if it is process 1, which scans $n - 1$ idle processes in phase 1. A process that fails phase 2 writes $control[i]$ again in the next round, so the remote references in one wait have no bound.

## Properties

- Uses atomic read/write registers only; each $control[i]$ has three values and one writer; $k$ has $n$ writers.
- Mutual exclusion, deadlock freedom and starvation freedom.
- Bounded bypass, but the bound grows exponentially in $n$. Not FCFS.
- Symmetric: all processes run the same code, and the priority moves around with $k$.

## Variants and improvements

- **de Bruijn (1967).** A change to the exit section lowers the worst wait to $n(n - 1)/2$ turns.
- **Eisenberg and McGuire (1972).** The [Eisenberg and McGuire algorithm](/eisenberg-mcguire-algorithm/) lowers it to $n - 1$: a leaving process passes the turn to the next process that is not idle.
- **The bakery.** [Lamport's bakery algorithm](/lamport-bakery-algorithm/) (1974) is FCFS and needs no register with $n$ writers, but its numbers have no bound.

## When to use it

Read it as the step from [Dijkstra's algorithm](/dijkstra-mutex-algorithm/) to starvation freedom, and as an example of a rotating priority. For a real lock, use a lock built on an atomic instruction, such as a [ticket lock](/ticket-lock/) or an MCS lock.

## Pitfalls

**The scan order.** Phase 1 must scan from $k$ down to $i + 1$ in the cyclic order. A process that scans all others, or scans in another order, can lose the starvation freedom.

**Two values are not enough.** The values 1 and 2 mean different things: 1 blocks phase 1 of lower ranked processes, and 2 blocks phase 2 of everyone. With only one nonzero value, the algorithm becomes Dijkstra-like and can deadlock or starve.

**Weak memory.** On TSO hardware such as x86, the write $control[i] \leftarrow 2$ can wait in a store buffer while the process reads the others. The test file finds a run on the TSO model with two processes in the critical section.

**Exponential wait.** Starvation free does not mean a short wait. With many processes, the bound $2^{n-1} - 1$ is large.

## Implementations

## History

Dijkstra (1965) stated the problem and gave a deadlock free solution. In 1966 Knuth, then at Caltech, wrote a letter to Communications of the ACM that showed a run of Dijkstra's algorithm in which one process waits forever, and gave this algorithm, which is starvation free and still symmetric. De Bruijn (1967) improved the bound on the wait, and Eisenberg and McGuire (1972) brought it down to $n - 1$. Lamport (2021) calls Knuth's algorithm the first starvation free $n$-process solution. Almost all solutions published after it are starvation free.

## References
