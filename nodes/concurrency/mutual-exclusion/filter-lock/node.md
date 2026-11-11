---
tag: 5JN2ZF
kind: algorithm
slug: filter-lock
name: Filter lock
aliases: [n-process Peterson lock, level lock]
area: concurrency/mutual-exclusion
level: core
summary: Peterson's algorithm for n processes. It has n - 1 levels, and each level holds back one process. Starvation free with reads and writes only, but not FCFS and with no bound on bypass.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes}
  space: {shared: Θ(n)}
  steps: {solo: Θ(n^2)}
  rmr: {cc: O(n^3), dsm: ∞}
  bypass: {worst: ∞}
properties: {deterministic: true, deadlock_free: true, starvation_free: true, fcfs: false, bounded_bypass: false, single_writer: false, bounded_registers: true, local_spinning: false}
history:
  year: 1981
  people: [Gary L. Peterson]
  note: Peterson gave the n-process algorithm in his 1981 note, next to the two-process one. Herlihy and Shavit later named it the filter lock.
prereqs: [mutual-exclusion-problem, peterson-algorithm]
see_also: [tournament-lock, lamport-bakery-algorithm, eisenberg-mcguire-algorithm, szymanski-algorithm, starvation-freedom, rmr-complexity]
sources:
  - paper: doi:10.1016/0020-0190(81)90106-X
    title: Gary L. Peterson, Myths about the mutual exclusion problem, Information Processing Letters 12(3), 1981, pages 115-116
    locator: the generalization of the two-process algorithm to n processes
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 2, Mutual Exclusion (the filter lock, its proofs, and the remark that it is not fair)
  - paper: doi:10.1145/945526.945527
    title: K. Alagarsamy, Some myths about famous mutual exclusion algorithms, ACM SIGACT News 34(3), 2003, pages 94-103
    locator: the section on Peterson's algorithm and unbounded bypass for n > 2
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 10, Mutual Exclusion with Read/Write Shared Memory (Peterson's n-process algorithm)
---

The filter lock is Peterson's solution of the [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes with atomic read/write registers. It puts $n - 1$ copies of [Peterson's two-process algorithm](/peterson-algorithm/) one after the other, as levels. At each level, the last process that came to the level waits while some other process is at the same level or higher. So each level holds back at least one process, and at most one process gets through all $n - 1$ levels. The lock is starvation free and uses $2n - 1$ registers with small values. But a process can be passed any number of times while it waits, so it is not first come, first served (FCFS), and its bypass has no bound in terms of $n$.

## In plain words

A room has $n - 1$ waiting areas in a row, and you must pass all of them. At each area you write your name on a board, which removes the name that was there. You can go on if your name is no longer on the board, because someone came after you. You can also go on if nobody else is in this area or further in.

The person whose name is on the board stays behind. So each area holds back at least one person, and after $n - 1$ areas, only one person is left. That one goes into the room.

Nobody waits forever: a new arrival or an empty area frees you. But a slow person can be passed again and again by fast people.

## The problem

There are $n \ge 2$ asynchronous processes $0, \ldots, n-1$. Each one repeats a remainder section, an entry section, a critical section and an exit section. The entry and exit sections must give mutual exclusion and starvation freedom, as the [mutual exclusion problem](/mutual-exclusion-problem/) defines. The shared memory has atomic read/write registers and is sequentially consistent. A process stays in its critical section for a finite time.

## The algorithm

The registers are $level[0..n-1]$, all 0 at the start, and $victim[1..n-1]$, with any start values. Only process $i$ writes $level[i]$, the highest level it has come to. All processes write $victim[\ell]$, the process that came to level $\ell$ last.

```pseudo id=main
LOCK(i)
L1  for ℓ ← 1 to n − 1
L2      level[i] ← ℓ
L3      victim[ℓ] ← i
L4      repeat
L5          if victim[ℓ] ≠ i then exit the loop
L6          read level[k] for each k ≠ i in turn; stop at the first k with level[k] ≥ ℓ
L7      until no such k was found
                                       ▷ critical section
UNLOCK(i)
L8  level[i] ← 0
```

At level $\ell$, process $i$ waits while $victim[\ell] = i$ and some other process has $level[k] \ge \ell$. Each read is one shared step, so the condition is not read at one instant: the loop reads $victim[\ell]$, then the levels one at a time, and starts again if it finds a process at level $\ell$ or higher. The proof allows this.

The *doorway* is L2 and L3 of level 1: two writes with no wait. For $n = 2$ there is one level, and the lock is [Peterson's algorithm](/peterson-algorithm/), with $level[i] \ge 1$ as the flag and $victim[1]$ as the turn, except that the loop reads the turn first.

## Example

Three processes come at the same time. Each row is one or more shared steps. The test file runs this schedule step by step.

| step | process | action | $level$ | $victim[1]$ | $victim[2]$ |
|---|---|---|---|---|---|
| start | | | 0, 0, 0 | 0 | 0 |
| 1 | 0 | L2, L3 at level 1 | 1, 0, 0 | 0 | 0 |
| 2 | 1 | L2, L3 at level 1 | 1, 1, 0 | 1 | 0 |
| 3 | 2 | L2, L3 at level 1 | 1, 1, 1 | 2 | 0 |
| 4 | 0 | reads $victim[1] = 2$, passes level 1; L2, L3 at level 2 | 2, 1, 1 | 2 | 0 |
| 5 | 1 | reads $victim[1] = 2$, passes level 1; L2, L3 at level 2 | 2, 2, 1 | 2 | 1 |
| 6 | 2 | reads $victim[1] = 2$ and $level[0] = 2 \ge 1$, waits | 2, 2, 1 | 2 | 1 |
| 7 | 0 | reads $victim[2] = 1$, passes level 2, enters | 2, 2, 1 | 2 | 1 |
| 8 | 1 | reads $victim[2] = 1$ and $level[0] = 2 \ge 2$, waits | 2, 2, 1 | 2 | 1 |
| 9 | 0 | leaves, $level[0] \leftarrow 0$ | 0, 2, 1 | 2 | 1 |
| 10 | 1 | reads $victim[2] = 1$, $level[0] = 0$, $level[2] = 1$, enters | 0, 2, 1 | 2 | 1 |
| 11 | 2 | reads $victim[1] = 2$, $level[0] = 0$, $level[1] = 2 \ge 1$, waits | 0, 2, 1 | 2 | 1 |
| 12 | 1 | leaves, $level[1] \leftarrow 0$ | 0, 0, 1 | 2 | 1 |
| 13 | 2 | finds no other level of 1 or more, passes level 1, then level 2, enters | 0, 0, 2 | 2 | 2 |

Level 1 held back process 2, the last to write $victim[1]$, and level 2 held back process 1. In this run the processes enter in the order in which they came, but this is not always so.

## Correctness

The full proof is in proofs/correctness.md. Say that a process is *above* level $\ell$ if it has passed the loop of level $\ell$ and has not yet left the critical section.

- **Mutual exclusion.** At most $n - \ell$ processes are above level $\ell$, by induction on $\ell$. Suppose that $n - \ell + 1$ processes are above $\ell$, and look at the last write of $victim[\ell]$, by some process $C$. After it, $victim[\ell] = C$, so $C$ can pass level $\ell$ only with a scan that finds all other levels below $\ell$. But at least one other process above $\ell$ wrote its level before that write and still has a level of $\ell$ or more. So $C$ did not pass level $\ell$. If $C$ is one of the processes above $\ell$, this is a contradiction. If not, $C$ still waits at level $\ell$, and then $n - \ell + 2$ processes are above $\ell - 1$, which contradicts the induction. For $\ell = n - 1$, at most one process is above the last level, and the critical section is above it.
- **Starvation freedom.** By induction on the level, from the top down: a process that waits at level $\ell$ is freed when some process writes $victim[\ell]$ after it. If nobody does, then all processes above $\ell$ go through, by induction, and no process can come to level $\ell$ again without writing $victim[\ell]$. So in the end all other levels are below $\ell$, and the waiting process passes.
- **No bound on bypass.** For $n \ge 3$, process 0 can finish its doorway and then be slow. Processes 1 and 2 then take turns: when one comes to level 1, it writes $victim[1]$ and so frees the other one, which goes through all levels, because process 0 and the new arrival have level 1. This repeats any number of times. Process 1 can start its doorway after process 0 finished its doorway and still enter first, so the lock is not FCFS. Process 0 still enters as soon as it runs, because it is not the victim of level 1 any more.

The test file checks mutual exclusion, deadlock freedom and starvation freedom by exhaustive search of all interleavings: for 2 processes (105 states for one passage each, 409 for two, 119 forever, where the bypass is 1 and the order is FCFS) and for 3 processes with one passage each (25633 states, not FCFS). It runs the bypass schedule above with 20 entries of processes 1 and 2 while process 0 waits after its doorway. It also runs 3 seeded random schedules of 4000 steps each for 4 and 5 processes.

## Complexity

| measure | value |
|---|---|
| shared registers | $2n - 1$: $n$ single-writer levels and $n - 1$ multi-writer victims, all with values below $n$ |
| entry and exit without contention | $(n - 1)(n + 2)$ steps to enter, 1 write to leave |
| bypass after the doorway | 1 for $n = 2$; no bound for $n \ge 3$ |
| RMRs per passage, CC model | $O(n^3)$ (sketch below) |
| RMRs per passage, DSM model | unbounded |

Without contention, each level costs two writes, one read of $victim[\ell]$ and a scan of the $n - 1$ other levels, so the entry section takes $(n - 1)(n + 2) = \Theta(n^2)$ steps even when no other process tries. The test file counts these steps for $n = 2$ to $5$.

*Sketch of the CC bound.* In the cache coherent model, a read misses the cache only if the register was written since the last read by the same process. Process $i$ waits at level $\ell$ only while $victim[\ell] = i$. In that time, no process can come to level $\ell$ again, since that needs a write of $victim[\ell]$. So each other process writes its level at most about $2n$ times: up to the top, $0$ at the exit, and up to $\ell - 1$ again. That makes $O(n^2)$ misses at one level and $O(n^3)$ for all levels. The test finds at most 5 RMRs in one entry section for 2 processes run forever, and 10 for 3 processes with one passage each. We do not know a tight bound. In the distributed shared memory (DSM) model, at least one of the registers that a waiting process reads is in another module, and it can read it any number of times while another process stays in the critical section. See [RMR complexity](/rmr-complexity/).

## Properties

- Uses atomic read/write registers only, with values in $\{0, \ldots, n-1\}$.
- Deadlock free and starvation free for any $n$.
- Not FCFS, and the bypass of a waiting process is not bounded by any function of $n$ when $n \ge 3$. Each waiting process enters in the end, but nobody can say after how many entries of others.
- The $victim$ registers are written by all processes; the $level$ registers have one writer each.
- Busy waiting on registers that other processes write, so no local spinning.
- The cost without contention is $\Theta(n^2)$ steps, much more than the $\Theta(n)$ of the [bakery algorithm](/lamport-bakery-algorithm/).

## Variants and improvements

- **Tournament lock.** Instead of $n - 1$ levels that every process passes, use a binary tree of two-process Peterson locks. A process passes only $\lceil \log_2 n \rceil$ of them. See [tournament lock](/tournament-lock/).
- **Bounded bypass.** The [Eisenberg-McGuire algorithm](/eisenberg-mcguire-algorithm/) has bypass $n - 1$ with $n + 1$ small registers, and the [bakery algorithm](/lamport-bakery-algorithm/) is FCFS. [Szymański's algorithm](/szymanski-algorithm/) gives linear wait with a constant number of single-writer flags per process.
- **Order of the loop.** The loop can read $victim[\ell]$ and the levels in any order. The proof still holds, because it uses only reads that come after the write of $victim[\ell]$ by the same process.

## When to use it

Use it to teach how a two-process lock generalizes to $n$ processes, and as a first example of a proof by induction over levels. It is short and needs only reads and writes with small values. Do not use it where fairness or speed matter: a process can be passed many times, and even a process that runs alone makes $\Theta(n^2)$ steps. On real machines, use a lock built on an atomic instruction, such as a [ticket lock](/ticket-lock/) or a queue lock.

## Pitfalls

**Wrong order of the two writes.** A process must write $level[i]$ before $victim[\ell]$. If it writes $victim[\ell]$ first, two processes can pass the same level together: the test file finds such a run that breaks mutual exclusion for 2 and for 3 processes.

**Bypass is not bounded.** Some texts say that this lock has bounded bypass. It does not for $n \ge 3$. Alagarsamy (2003) points this out, and the test file shows a run with 20 bypasses.

**TSO and x86.** As with Peterson's algorithm, the write of $victim[\ell]$ can wait in a store buffer while the process reads the levels of others. The test file finds a run with two processes in the critical section on the TSO model, and none when a full fence follows each write of $victim[\ell]$. Under TSO it checks only safety.

**Compilers.** The registers must be atomic variables with sequentially consistent accesses, or a compiler can keep a level in a register and never read it again.

## Implementations

## History

Dijkstra (1965) gave the first solution for $n$ processes, and Knuth (1966), de Bruijn (1967), Eisenberg and McGuire (1972) and Lamport (1974) followed with fairer ones. In 1981 Gary L. Peterson published a two-page note in Information Processing Letters with a very short two-process algorithm and its generalization to $n$ processes by levels. Herlihy and Shavit, in The Art of Multiprocessor Programming (2008), present this generalization as the filter lock, and they note that it is not fair. Alagarsamy (2003) showed that its bypass is unbounded for $n > 2$, which some textbooks had stated otherwise; he also notes that Peterson did not claim a bound.

## References
