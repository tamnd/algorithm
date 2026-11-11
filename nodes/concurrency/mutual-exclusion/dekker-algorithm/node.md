---
tag: D4K719
kind: algorithm
slug: dekker-algorithm
name: Dekker's algorithm
aliases: [Dekker's mutual exclusion]
area: concurrency/mutual-exclusion
level: intro
summary: The first correct two-process mutual exclusion with reads and writes only (Dekker 1959, reported by Dijkstra). Two flags and a turn give starvation freedom, but no bound on bypass.
solves: [mutual-exclusion-problem]
complexity:
  space: {shared: Θ(1)}
  steps: {solo: Θ(1)}
  rmr: {cc: Θ(1), dsm: ∞}
  bypass: {worst: ∞}
properties: {deterministic: true, deadlock_free: true, starvation_free: true, fcfs: false, bounded_bypass: false, local_spinning: false}
history:
  year: 1959
  people: [Theodorus J. Dekker, Edsger W. Dijkstra]
  note: Dekker found the algorithm in 1959. Dijkstra reported it in EWD 35 (about 1962) and gave it with a proof in EWD 123, Cooperating Sequential Processes (1965).
prereqs: [mutual-exclusion-problem]
see_also: [peterson-algorithm, dijkstra-mutex-algorithm, knuth-mutex-algorithm, burns-lamport-algorithm, starvation-freedom, livelock, deadlock-freedom, rmr-complexity]
sources:
  - url: "https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD123.html"
    title: Edsger W. Dijkstra, Cooperating sequential processes, EWD 123, 1965
    locator: Section 2.1, A Simple Example (the rejected attempts, then Dekker's solution and its proof)
  - url: "https://www.cs.utexas.edu/~EWD/ewd00xx/EWD35.PDF"
    title: Edsger W. Dijkstra, Over de sequentialiteit van procesbeschrijvingen, EWD 35, in Dutch, about 1962
    locator: the report of Dekker's 1959 solution
  - url: "https://lamport.azurewebsites.net/pubs/dijkstra.pdf"
    title: Leslie Lamport, Chapter on concurrent algorithms, for a book on Dijkstra, 18 December 2021
    locator: Section 2.2, Dekker's Algorithm, and Figure 2 (the gap in Dijkstra's argument for deadlock freedom, and starvation freedom)
  - paper: doi:10.1145/365559.365617
    title: Edsger W. Dijkstra, Solution of a problem in concurrent programming control, Communications of the ACM 8(9), 1965
    locator: the n-process problem, which uses Dekker's idea of a turn variable
  - paper: doi:10.1145/1785414.1785443
    title: Peter Sewell, Susmit Sarkar, Scott Owens, Francesco Zappa Nardelli and Magnus O. Myreen, x86-TSO, a rigorous and usable programmer's model for x86 multiprocessors, Communications of the ACM 53(7), 2010, pages 89-97
    locator: the store buffer model of x86 and the store-load reordering
---

Dekker's algorithm is the first correct solution of the [mutual exclusion problem](/mutual-exclusion-problem/) for two processes that use only atomic reads and writes of shared memory. Th. J. Dekker found it in 1959, and Edsger Dijkstra reported it and proved it in his notes. Each process has a flag that says "I want to enter", and a shared variable $turn$ says which process has priority when both want to enter. A process that does not have priority lowers its flag and waits for its turn. The algorithm gives mutual exclusion and starvation freedom, but a slow process can be passed any number of times, so it has no bound on bypass.

## In plain words

Two people share one room. Each has a flag, and there is one sign that names whose turn it is. To enter, you raise your flag and look at the other flag. If it is down, you go in.

If both flags are up, you look at the sign. If the sign names you, you keep your flag up and wait for the other flag to go down. If the sign names the other person, you are polite: you lower your flag, wait until the sign names you, and then raise your flag again and look once more.

When you leave the room, you set the sign to the other person and lower your flag. So after a tie, the person who just left has to yield next time.

## The problem

There are $n = 2$ asynchronous processes, 0 and 1. Each one repeats a remainder section, an entry section, a critical section and an exit section, as in the [mutual exclusion problem](/mutual-exclusion-problem/). The goal is mutual exclusion (never both in the critical section) and a progress property: deadlock freedom (if a process tries, some process enters) or, stronger, starvation freedom (every process that tries enters). The shared memory has atomic read/write registers only, and it is sequentially consistent. A process stays in its critical section for a finite time and may stay in its remainder section forever.

Two simpler ideas fail. *Strict alternation* (enter only when $turn$ names you) is safe, but a process that stays in its remainder section blocks the other one forever. *Two flags* (raise your flag and wait while the other flag is up) is safe, but if both raise their flags at the same time, both wait forever: a deadlock. The test file finds this deadlock. Dekker's idea is to use the flags in the normal case and the turn only to break the tie.

## The algorithm

Process $i \in \{0, 1\}$ uses $j = 1 - i$. The registers are $flag[0]$ and $flag[1]$, false at the start, and $turn \in \{0, 1\}$, with any start value. Only process $i$ writes $flag[i]$. This is the modern form with "flag true means I want to enter"; Dijkstra's text uses variables $c_1$ and $c_2$ with the opposite meaning and jumps, and it runs the same steps.

```pseudo id=main
LOCK(i)                                ▷ entry section, j = 1 − i
L1  flag[i] ← true
    loop
L2      if flag[j] = false then exit the loop
L3      if turn = j then               ▷ the other process has priority
L4          flag[i] ← false            ▷ step back
L5          wait until turn ≠ j
L6          flag[i] ← true             ▷ try again
                                       ▷ critical section
UNLOCK(i)                              ▷ exit section
L7  turn ← j
L8  flag[i] ← false
```

If $turn = i$ at L3, process $i$ has priority, so it keeps its flag up and goes back to L2 to read the other flag again. Each numbered line is one shared step, and the line L5 is a loop of reads of $turn$.

## Example

Both processes try at once, with $turn = 0$ at the start.

| step | process | line | action | $flag[0]$ | $flag[1]$ | $turn$ |
|---|---|---|---|---|---|---|
| start | | | | false | false | 0 |
| 1 | 0 | L1 | $flag[0] \leftarrow true$ | true | false | 0 |
| 2 | 1 | L1 | $flag[1] \leftarrow true$ | true | true | 0 |
| 3 | 0 | L2 | reads $flag[1] = true$ | true | true | 0 |
| 4 | 1 | L2 | reads $flag[0] = true$ | true | true | 0 |
| 5 | 0 | L3 | reads $turn = 0$: it has priority, back to L2 | true | true | 0 |
| 6 | 1 | L3 | reads $turn = 0 = j$: it must yield | true | true | 0 |
| 7 | 1 | L4 | $flag[1] \leftarrow false$ | true | false | 0 |
| 8 | 0 | L2 | reads $flag[1] = false$, enters | true | false | 0 |
| 9 | 1 | L5 | reads $turn = 0$, waits | true | false | 0 |
| 10 | 0 | L7 | leaves, $turn \leftarrow 1$ | true | false | 1 |
| 11 | 0 | L8 | $flag[0] \leftarrow false$ | false | false | 1 |
| 12 | 1 | L5 | reads $turn = 1$, stops waiting | false | false | 1 |
| 13 | 1 | L6 | $flag[1] \leftarrow true$ | false | true | 1 |
| 14 | 1 | L2 | reads $flag[0] = false$, enters | false | true | 1 |

Now $turn = 1$, so in the next tie process 1 has priority.

**A bad run for bypass.** Let $turn = 1$, and let process 0 run L1 to L4, so that it waits with its flag down. If process 0 now stops for a while, process 1 can enter, leave and enter again any number of times, because each time it reads $flag[0] = false$ at L2. Process 0 is still in its entry section. When it runs again, it reads $turn = 0$ (each exit of process 1 wrote it), raises its flag for good, and enters. The test file runs this schedule with 10 entries of process 1.

## Correctness

The full proof is in proofs/correctness.md. In outline:

- **Mutual exclusion.** A process enters only right after it reads the other flag as false, and its own flag is true from its last raise until it leaves. If both were inside, look at the process whose last read of L2 came first. Its flag was already true when the other process made its read, so the other read could not return false. This is the "safe sluice" argument of Dijkstra.
- **Starvation freedom.** Suppose that process $i$ tries forever. If $j$ enters even once more, its exit sets $turn = i$ for good, so from then on $i$ keeps its flag up, $j$ can enter at most once more, and then $j$ either stays in its remainder section or yields at L4 and waits at L5 forever. In both cases $flag[j]$ stays false, and $i$ enters. If $j$ never enters again but tries forever, $turn$ is constant. The process that $turn$ does not name yields at L4 and waits at L5, and then the named process enters. That process cannot be $j$, so it is $i$. If $j$ stays in its remainder section, its flag is down and $i$ enters.
- **No bound on bypass.** The run above, in which process 0 waits with its flag down, lets process 1 enter any number of times first. So the algorithm is starvation free, but not $k$-bounded for any $k$, and not FCFS.

The test file explores all interleavings for two processes: 86 states for one passage each, 451 for two, and 187 when both run forever. It finds no state with both processes inside, no fair run in which a process waits forever, and no deadlock. The bypass search reaches its cap of 64, which stands for unbounded. The algorithm is for two processes only, so it can only be checked with 2.

## Complexity

| measure | value |
|---|---|
| shared registers | 3: two single-writer flags and one multi-writer $turn$ |
| entry and exit without contention | 4 shared steps: L1 and L2 to enter, L7 and L8 to leave |
| bypass | unbounded |
| RMRs per passage, CC model | $O(1)$; the test finds at most 10 for process 0 and 11 for process 1 in one entry section |
| RMRs per passage, DSM model | unbounded |

In the cache coherent (CC) model, a process that waits at L5 or loops at L2 and L3 rereads cached copies, and a cache miss needs a write of the other process. The test finds a bound for each process by search over all states. In the distributed shared memory (DSM) model, a waiting process reads $turn$ or the other flag in a loop, and at least one of them is in the other process's memory module, so the number of remote references is unbounded. See [RMR complexity](/rmr-complexity/).

## Properties

- Atomic read/write registers only.
- Deadlock free and starvation free, but no bounded bypass and no FCFS order.
- Busy waiting.
- Symmetric up to the names 0 and 1: the code is the same for both processes, unlike the one-bit algorithm, which gives process 0 a fixed priority.
- Needs sequential consistency. On x86 it fails without a fence, exactly as [Peterson's algorithm](/peterson-algorithm/) does.

## Variants and improvements

- **Peterson's algorithm** (1981) also uses two flags and a turn, but each process gives the turn away *before* it waits, so the last process to write the turn yields. It has no inner loop, it has bypass 1, and it is FCFS. See [Peterson's algorithm](/peterson-algorithm/).
- **Dijkstra's $n$-process algorithm** (1965) uses Dekker's idea of a turn variable for $n$ processes. It is deadlock free but not starvation free. See [Dijkstra's algorithm](/dijkstra-mutex-algorithm/).
- **Knuth's algorithm** (1966) extends Dekker's idea, with a turn that passes in a fixed order, to the first starvation-free $n$-process solution. See [Knuth's algorithm](/knuth-mutex-algorithm/).
- **The one-bit algorithm** of Burns and Lamport uses only the flags, with a fixed priority, and is deadlock free but not starvation free. See [Burns and Lamport's algorithm](/burns-lamport-algorithm/).

## When to use it

Dekker's algorithm is mainly of historical and teaching value: it shows that mutual exclusion is possible with reads and writes only, and it shows how hard it is to get the details right. For two processes, Peterson's algorithm is shorter, has bypass 1, and is easier to prove. On real hardware, use a lock built on an atomic instruction or the system [mutex](/mutex/).

## Pitfalls

**Memory order.** On x86 the write of L1 can wait in the store buffer while the read of L2 goes to memory. Then both processes read the other flag as false and both enter. The test file finds this run in the TSO mode of the explorer, in six steps. A full fence after L1 and after L6, before the next read of L2, fixes it: the test file adds the two fences and finds no bad state under TSO for one passage, two passages and forever (it checks only safety under TSO). In C11 and C++11, make the three variables atomic with `memory_order_seq_cst`.

**The order of the exit section.** The exit writes $turn$ before it lowers the flag, as in Dijkstra's text.

**A wrong proof.** Dijkstra's own argument for deadlock freedom misses a case, as Lamport (2021) points out: a process that waits at L5 while the other one stays in its remainder section. The algorithm is still correct, but the gap shows how easy it is to miss a run when one reasons about all behaviors by hand.

**Spinning.** A waiting process spins, and if the other process is preempted, it spins for a whole time slice.

## Implementations

## History

Dekker, a Dutch mathematician, found the algorithm in 1959. Dijkstra wrote about it in EWD 35, apparently written in 1962, and, according to that note, the solution was seen as a curiosity until the THE operating system made the problem real. In EWD 123, Cooperating Sequential Processes (1965), Dijkstra develops the solution step by step: he shows several wrong attempts, and then gives Dekker's solution with a proof of safety and of deadlock freedom. In his 1965 paper in Communications of the ACM he solved the problem for $n$ processes with Dekker's idea of a turn. Lamport (2021) notes that Dijkstra did not claim starvation freedom for Dekker's algorithm, although it holds, and that the first starvation-free $n$-process algorithm is Knuth's (1966).

## References
