---
tag: 0XYD33
kind: problem
slug: mutual-exclusion-problem
name: Mutual exclusion problem
aliases: [critical section problem]
area: concurrency/mutual-exclusion
level: intro
summary: Design entry and exit code so that at most one of n asynchronous processes is in its critical section at a time, and a process that wants to enter eventually does.
history:
  year: 1965
  people: [Edsger W. Dijkstra, Th. J. Dekker, Leslie Lamport]
  note: Dijkstra stated the problem for n processes in 1965 and solved it with reads and writes. Dekker had solved it for two processes earlier. Lamport gave the precise fairness conditions and the doorway in 1974 and 1986.
prereqs: [critical-section]
see_also: [mutex, peterson-algorithm, lamport-bakery-algorithm, mutual-exclusion-lower-bounds, deadlock-freedom, starvation-freedom, rmr-complexity, test-and-set]
sources:
  - paper: doi:10.1145/365559.365617
    title: Edsger W. Dijkstra, Solution of a problem in concurrent programming control, Communications of the ACM 8(9), 1965, page 569
    locator: the statement of the problem and its requirements (a) to (d)
  - paper: doi:10.1145/5383.5384
    title: Leslie Lamport, The mutual exclusion problem, Part I, A theory of interprocess communication, Journal of the ACM 33(2), 1986
    locator: the formal model of processes, system executions and registers
  - paper: doi:10.1145/5383.5385
    title: Leslie Lamport, The mutual exclusion problem, Part II, Statement and solutions, Journal of the ACM 33(2), 1986, pages 327 to 348
    locator: Section 2.1 (the basic requirements), Section 2.2 (fairness, the doorway and first come first served, and Theorem 1)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 10, Mutual Exclusion (the problem, Dijkstra's algorithm, stronger conditions, lockout freedom, and the lower bound on shared memory)
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 2, Mutual Exclusion (two-thread solutions, the filter lock, fairness, the bakery algorithm, and the lower bound)
  - paper: doi:10.1006/inco.1993.1065
    title: James E. Burns and Nancy A. Lynch, Bounds on shared memory for mutual exclusion, Information and Computation 107(2), 1993, pages 171 to 184
    locator: the lower bound of n read/write registers
  - paper: "Hagit Attiya, Danny Hendler and Philipp Woelfel, Tight RMR lower bounds for mutual exclusion and other problems, STOC 2008, pages 217 to 226"
    locator: the Omega(n log n) lower bound on total RMRs
---

The mutual exclusion problem asks for an entry section and an exit section around the [critical section](/critical-section/) of each of $n$ processes, so that at most one process is in its critical section at any time and a process that wants to enter is not blocked forever. Dijkstra stated it in 1965 and solved it with atomic reads and writes of shared variables. It is the base problem of lock design: every [mutex](/mutex/) and spin lock is a solution, and the algorithms of this area differ in the primitives they use, the fairness they give, and their cost.

## In plain words

Several workers share one tool that only one of them can use at a time. They cannot talk to each other. They can only write notes on a board and read the notes of the others. Each worker follows the same kind of plan: do private work, then follow a protocol to get the tool, use it, and follow a protocol to give it back.

The task is to write the protocol. It must never let two workers use the tool together. It must also not get stuck: if workers want the tool, one of them must get it. A better protocol also makes sure that each worker who asks gets the tool in the end, and that nobody is passed too many times.

## Definition

**Model.** There are $n \ge 2$ processes, named $p, q, \ldots$ or $0, \ldots, n - 1$ (indices $i, j$). They are asynchronous: each takes steps at its own speed, and nothing bounds the time between two steps of one process. They share memory. In the basic problem the only shared operations are atomic reads and writes of registers: each read or write is one indivisible step, and a read returns the value of the last write before it. The memory is sequentially consistent. A run is an interleaving of the steps of all processes. Variants use stronger primitives such as [test-and-set](/test-and-set/) or [compare-and-swap](/compare-and-swap/), weaker registers, or known timing, and each page says which.

The code of process $i$ is a loop with four sections, as on the [critical section](/critical-section/) page:

```pseudo
loop forever
    remainder section
    entry section
    critical section
    exit section
```

The problem is to write the entry and exit sections. The *doorway* is a prefix of the entry section that a process completes in a bounded number of its own steps, whatever the other processes do; the rest of the entry section is the *waiting* part (Lamport 1986, Part II, Section 2.2).

**Assumptions.**

1. A process may stay in its remainder section forever, and it may stop (crash) there.
2. A process does not stop in its entry, critical or exit section, and it leaves the critical section after a finite number of its own steps.
3. A run is fair: each process that is not in its remainder section takes infinitely many steps. Nothing else is assumed about speed.
4. Reads and writes of shared registers are atomic, unless the page states a weaker register.
5. The processes run the same code, up to their index, and they do not share local variables.

**Requirements.** The first is a safety property. The others are progress properties, from the weakest to the strongest:

- *Mutual exclusion.* In no reachable state are two processes in their critical sections.
- *Deadlock freedom* (also called *progress*). In every fair run, if some process is in its entry section, then some process later enters its critical section. A process in its exit section also reaches its remainder section. The page [deadlock freedom](/deadlock-freedom/) treats the property in general.
- *Starvation freedom* (Lynch: *lockout freedom*). In every fair run, every process in its entry section later enters its critical section. See [starvation freedom](/starvation-freedom/).
- *Bounded bypass $b$* (also $b$-bounded waiting). While process $p$ waits after its doorway, the other processes together enter the critical section at most $b$ times before $p$ does. Bounded bypass with any finite $b$ implies starvation freedom, given deadlock freedom.
- *First come first served* (FCFS, Lamport 1986). If $p$ completes its doorway before $q$ begins its doorway, then $q$ does not enter its critical section before $p$. FCFS is $0$-bounded waiting with respect to later arrivals.

Lamport (1986, Part II, Theorem 1) proves that FCFS together with deadlock freedom implies starvation freedom. Dijkstra's (1965) own conditions were mutual exclusion, symmetry, no assumption on speeds, a process stopped in its remainder section must not block the others, and the deadlock freedom stated above. The starvation-free and bounded versions came with Knuth (1966) and later papers.

**Costs.** A solution is measured by the number of shared registers and their size, the number of steps a process makes in its entry and exit sections when it runs alone, and the number of remote memory references (RMRs) per passage in the cache coherent (CC) or the distributed shared memory (DSM) model. The page [RMR complexity](/rmr-complexity/) defines the RMR models.

## Variants

- *Strong primitives.* With [test-and-set](/test-and-set/), swap, [fetch-and-add](/fetch-and-add/) or [compare-and-swap](/compare-and-swap/), one shared word is enough. The [ticket lock](/ticket-lock/) is FCFS with fetch-and-add, and the queue locks ([Anderson](/anderson-lock/), [MCS](/mcs-lock/), [CLH](/clh-lock/)) also make $O(1)$ RMRs per passage.
- *Weak registers.* Lamport's [bakery algorithm](/lamport-bakery-algorithm/) still works when each register is only *safe*: a read that overlaps a write may return any value of the domain.
- *Single-writer registers.* Each register has one writer, as in the bakery, [Kessels' algorithm](/kessels-algorithm/) and [Szymański's algorithm](/szymanski-algorithm/).
- *Small registers.* The [one-bit algorithm](/burns-lamport-algorithm/) uses one bit per process.
- *Fast mutual exclusion.* Lamport's [fast mutex](/lamport-fast-mutex/) enters in a constant number of steps when there is no contention.
- *Known timing.* [Fischer's algorithm](/fischer-algorithm/) uses one register and a delay, and it is correct only if the delay is longer than any write.
- *Other relaxations and extensions* include k-exclusion (at most $k$ processes inside), the [readers-writers problem](/readers-writers-problem/) (many readers or one writer), group mutual exclusion, mutual exclusion in a message passing system, and recoverable mutual exclusion, where a process may crash in its critical section and restart.

## Examples

Three short attempts for two processes show why each requirement matters. The test file checks each one over every interleaving, with two clients that loop forever.

**One flag.** Process $i$ waits until `busy` is false, then writes `busy := true`, and the exit section writes `busy := false`. The read and the write are two steps. The explorer finds this run of 6 steps, out of 27 reachable states: process 0 leaves its remainder section and reads `busy = false`, process 1 does the same, process 0 writes `true` and enters, and process 1 writes `true` and enters. Mutual exclusion fails.

**Strict alternation.** Process $i$ waits until `turn = i`, and the exit section writes `turn := 1 − i`. Mutual exclusion holds in all 39 states. Deadlock freedom fails: if process 1 stays in its remainder section, as assumption 1 allows, process 0 enters once, gives the turn to process 1, and then waits forever.

**Two flags.** Process $i$ writes `flag[i] := true` and waits until `flag[1 − i]` is false; the exit section writes `flag[i] := false`. Mutual exclusion holds in all 43 states, because a process enters only after it saw the other flag down after it raised its own. Deadlock freedom fails on the schedule: process 0 writes its flag, process 1 writes its flag, and then both read the other flag as true forever.

| attempt | states | mutual exclusion | deadlock free | failing schedule |
|---|---|---|---|---|
| one flag | 27 | no | | 0 reads, 1 reads, 0 writes, 1 writes |
| strict alternation | 39 | yes | no | 1 stays in its remainder section |
| two flags | 43 | yes | no | 0 and 1 raise their flags, then both wait |
| [Peterson](/peterson-algorithm/) | 117 | yes | yes | none; starvation free with bypass 1 |

[Peterson's algorithm](/peterson-algorithm/) combines the two-flag attempt with a `turn` variable that breaks the tie, and it meets every requirement.

## Known algorithms

The table lists the solutions on this site. Registers are counted for $n$ processes. "Bypass" is the bypass bound from the end of the doorway; "unbounded" means that the other processes can enter any number of times while one process waits, even though each waiting process does enter in the end.

| algorithm | year | processes | shared registers | primitives | progress | bypass |
|---|---|---|---|---|---|---|
| [Dekker](/dekker-algorithm/) | 1959 (Dijkstra 1965) | 2 | 3 | read, write | starvation free | unbounded |
| [Dijkstra](/dijkstra-mutex-algorithm/) | 1965 | $n$ | $2n + 1$ | read, write | deadlock free | none |
| [Knuth](/knuth-mutex-algorithm/) | 1966 | $n$ | $n + 1$ | read, write | starvation free | $2^{n-1} - 1$ |
| de Bruijn | 1967 | $n$ | $n + 1$ | read, write | starvation free | $n(n-1)/2$ |
| [Eisenberg and McGuire](/eisenberg-mcguire-algorithm/) | 1972 | $n$ | $n + 1$ | read, write | starvation free | $n - 1$ |
| [Lamport bakery](/lamport-bakery-algorithm/) | 1974 | $n$ | $2n$, unbounded values | safe single-writer registers | FCFS | $n - 1$ |
| [Peterson and Fischer tournament](/tournament-lock/) | 1977 | $n$ | $O(n)$ | read, write | starvation free | unbounded |
| [Peterson](/peterson-algorithm/) | 1981 | 2 | 3 | read, write | FCFS | 1 |
| [filter lock](/filter-lock/) | 1981 | $n$ | $2n - 1$ | read, write | starvation free | unbounded |
| [Burns and Lamport one-bit](/burns-lamport-algorithm/) | 1981, 1986 | $n$ | $n$ bits | single-writer bits | deadlock free | none |
| [Kessels](/kessels-algorithm/) | 1982 | 2 | 4 single-writer bits | read, write | FCFS | 1 |
| [Lamport fast mutex](/lamport-fast-mutex/) | 1987 | $n$ | $n + 2$ | read, write | deadlock free | none |
| [Fischer](/fischer-algorithm/) | 1987 (Lamport) | $n$ | 1 | read, write, known delay | deadlock free | none |
| [Szymański](/szymanski-algorithm/) | 1988 | $n$ | $n$ (5 values each) | single-writer registers | starvation free | $n - 1$ |
| [test-and-set lock](/test-and-set/) | | $n$ | 1 | test-and-set | deadlock free | none |
| [ticket lock](/ticket-lock/) | | $n$ | 2 | fetch-and-add | FCFS | $n - 1$ |

"None" means that the algorithm is not starvation free. The Peterson and Kessels bounds and the measured bounds of the other algorithms are checked on their pages by exhaustive search for 2 and 3 processes. The bounds of Knuth, de Bruijn and Eisenberg and McGuire are the published ones.

## Bounds

- *Space.* Burns and Lynch (1980, 1993) prove that any deadlock-free solution for $n$ processes that uses only read/write registers needs at least $n$ registers. The one-bit algorithm meets the bound with $n$ single bits. See [mutual exclusion lower bounds](/mutual-exclusion-lower-bounds/).
- *RMRs.* With reads, writes and conditional primitives such as compare-and-swap, Attiya, Hendler and Woelfel (2008) prove that some run has $\Omega(n \log n)$ RMRs in total for $n$ entries, in both the CC and the DSM models, so some passage makes $\Omega(\log n)$ RMRs. Yang and Anderson (1995) give a matching $O(\log n)$ algorithm with reads and writes. With fetch-and-add or swap, the queue locks make $O(1)$ RMRs per passage.
- *Fast paths.* With reads and writes alone, a process that runs alone can enter in a constant number of steps (Lamport 1987), but Alur and Taubenfeld (1992) show that under contention the first process to enter may have to make an unbounded number of steps, so a bound on all steps needs stronger primitives or timing.
- *FCFS with bounded registers.* The bakery algorithm needs unbounded ticket values. Bounded FCFS solutions exist, for example Taubenfeld's black-white bakery algorithm (2004).

## Reductions

- *From n processes to 2.* Any two-process solution gives an $n$-process solution by a binary tree of two-process locks: the [tournament lock](/tournament-lock/) of Peterson and Fischer (1977). The tree keeps starvation freedom if each node lock is starvation free, and it costs $\lceil \log_2 n \rceil$ node passages.
- *From FCFS to starvation freedom.* FCFS plus deadlock freedom gives starvation freedom (Lamport 1986, Part II, Theorem 1).
- *From a lock to any shared object.* Put every operation of a sequential object in one critical section. The result is linearizable, but it is blocking: a process that stops inside blocks all others. This is the reason for the non-blocking objects of the [lock-free structures](/non-blocking-algorithm/) area.
- *From a strong primitive.* A [test-and-set](/test-and-set/) register solves the problem with one word: enter when test-and-set returns 0, and reset it to leave.

## Applications

Every lock in an operating system kernel, a database engine, a language runtime or a lock-based data structure solves this problem, usually with an atomic instruction and a sleep queue (see [mutex](/mutex/)). The read/write algorithms matter today in three places: as a base for theory (the lower bounds and the RMR results), in settings without atomic read-modify-write instructions, and as small, checkable examples for model checkers and proof tools. On real multiprocessors, they need memory fences, because hardware memory is not sequentially consistent; [Peterson's algorithm](/peterson-algorithm/) shows the failure under TSO.

## References
