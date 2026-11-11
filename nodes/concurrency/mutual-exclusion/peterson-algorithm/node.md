---
tag: SA5BTH
kind: algorithm
slug: peterson-algorithm
name: Peterson's algorithm
aliases: [Peterson's lock]
area: concurrency/mutual-exclusion
level: intro
summary: Two-process mutual exclusion with three read/write registers. Raise your flag, give the turn away, and wait while the other flag is up and the turn is not yours.
solves: [mutual-exclusion-problem]
complexity:
  space: {shared: Θ(1)}
  steps: {solo: Θ(1)}
  rmr: {cc: Θ(1), dsm: ∞}
  bypass: {worst: Θ(1)}
properties: {deterministic: true, deadlock_free: true, starvation_free: true, fcfs: true, local_spinning: false}
history:
  year: 1981
  people: [Gary L. Peterson]
  note: Peterson published the algorithm in Information Processing Letters in 1981, as a much shorter solution than Dekker's, together with a generalization to n processes.
prereqs: [mutual-exclusion-problem]
see_also: [dekker-algorithm, filter-lock, tournament-lock, kessels-algorithm, lamport-bakery-algorithm, test-and-set, rmr-complexity, starvation-freedom]
sources:
  - paper: doi:10.1016/0020-0190(81)90106-X
    title: Gary L. Peterson, Myths about the mutual exclusion problem, Information Processing Letters 12(3), 1981, pages 115-116
    locator: the two-process algorithm and its generalization to n processes
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 2, Mutual Exclusion (the Peterson lock, its proofs of mutual exclusion and starvation freedom, and the filter lock)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 10, Mutual Exclusion with Read/Write Shared Memory (Peterson's two-process algorithm and the tournament algorithm)
  - paper: doi:10.1145/1785414.1785443
    title: Peter Sewell, Susmit Sarkar, Scott Owens, Francesco Zappa Nardelli and Magnus O. Myreen, x86-TSO, a rigorous and usable programmer's model for x86 multiprocessors, Communications of the ACM 53(7), 2010, pages 89-97
    locator: the store buffer model of x86 and the store-load reordering that breaks Dekker-style algorithms
  - paper: doi:10.1145/365559.365617
    title: Edsger W. Dijkstra, Solution of a problem in concurrent programming control, Communications of the ACM 8(9), 1965
    locator: the statement of the mutual exclusion problem
---

Peterson's algorithm solves the [mutual exclusion problem](/mutual-exclusion-problem/) for two processes with three shared atomic read/write registers: one flag for each process and one shared variable $turn$. A process raises its flag, gives the turn to the other process, and then waits while the other flag is up and the turn still belongs to the other process. It is the simplest correct two-process lock with reads and writes only. It is starvation free, first come first served after a doorway of two writes, and a waiting process lets the other one enter at most once. It assumes sequential consistency, and it fails on x86 unless a fence separates the doorway from the waiting loop.

## In plain words

Two people want to use one room. Each has a flag. To enter, you raise your flag and then say "you go first". After that, you wait only while the other person's flag is up and the last "you go first" was yours.

If only you want the room, the other flag is down and you go in. If both of you want it, both said "you go first", but one of you said it last. That polite person waits and the other one goes in. When the other one leaves, they lower their flag, and you go in.

Even if the other person comes back at once, they must say "you go first" again. Now they were last, so they must wait for you. So nobody can enter twice while you wait.

## The problem

There are $n = 2$ asynchronous processes, 0 and 1, and each one repeats a remainder section, an entry section, a critical section and an exit section. The task is to write the entry and exit sections so that at most one process is in the critical section at any time (mutual exclusion) and every process that tries to enter does enter (starvation freedom), as the [mutual exclusion problem](/mutual-exclusion-problem/) defines. The shared memory has atomic read/write registers only, and the memory is sequentially consistent: every run is one interleaving of the reads and writes of the two processes. A process stays in its critical section for a finite time, and it may stop for good in its remainder section.

## The algorithm

Process $i \in \{0, 1\}$ uses $j = 1 - i$ for the other process. The registers are $flag[0]$ and $flag[1]$, both false at the start, and $turn$, with any start value in $\{0, 1\}$. Only process $i$ writes $flag[i]$, and both processes write $turn$.

```pseudo id=main
LOCK(i)                                ▷ entry section, j = 1 − i
L1  flag[i] ← true
L2  turn ← j                           ▷ end of the doorway
L3  loop
L4      if flag[j] = false then exit the loop
L5      if turn ≠ j then exit the loop
                                       ▷ critical section
UNLOCK(i)                              ▷ exit section
L6  flag[i] ← false
```

The *doorway* is L1 and L2: two writes, with no wait. The loop of L3 to L5 waits while $flag[j] = true$ and $turn = j$. Each line is one shared step, so the two reads of the loop are separate steps, and the other process can write between them. The proof allows that.

The order of L1 and L2 matters. If a process writes $turn$ before it raises its flag, both processes can enter. Process 0 writes $turn \leftarrow 1$, and process 1 writes $turn \leftarrow 0$, raises its flag, reads $flag[0] = false$ and enters. Then process 0 raises its flag, reads $flag[1] = true$ and $turn = 0 \ne 1$, and enters too. The test file finds such a run.

## Example

Both processes try at the same time. The schedule is the one that the test file runs; each row is one shared step.

| step | process | line | action | $flag[0]$ | $flag[1]$ | $turn$ |
|---|---|---|---|---|---|---|
| start | | | | false | false | 0 |
| 1 | 0 | L1 | $flag[0] \leftarrow true$ | true | false | 0 |
| 2 | 1 | L1 | $flag[1] \leftarrow true$ | true | true | 0 |
| 3 | 0 | L2 | $turn \leftarrow 1$ | true | true | 1 |
| 4 | 1 | L2 | $turn \leftarrow 0$ | true | true | 0 |
| 5 | 0 | L4 | reads $flag[1] = true$, goes on | true | true | 0 |
| 6 | 1 | L4 | reads $flag[0] = true$, goes on | true | true | 0 |
| 7 | 0 | L5 | reads $turn = 0 \ne 1$, enters | true | true | 0 |
| 8 to 11 | 1 | L5, L4, L5, L4 | reads $turn = 0 = j$ and $flag[0] = true$, waits | true | true | 0 |
| 12 | 0 | L6 | leaves, $flag[0] \leftarrow false$ | false | true | 0 |
| 13 | 1 | L5 | reads $turn = 0 = j$, goes on | false | true | 0 |
| 14 | 1 | L4 | reads $flag[0] = false$, enters | false | true | 0 |

Process 1 wrote $turn$ last in step 4, so process 1 is the one that waits. If process 0 now came back and ran L1 and L2 again, it would write $turn \leftarrow 1$, and process 1 would read $turn = 1 \ne 0$ at L5 and enter first.

## Correctness

The full proof is in proofs/correctness.md. It has four claims, for sequentially consistent atomic registers and fair runs.

- **Mutual exclusion.** Suppose that both processes are in the critical section. Look at the last write to $turn$ before that time, say by process $i$, which wrote $turn = j$. After it, $turn$ stays $j$, because $j$ wrote earlier and neither process writes $turn$ again before it leaves. And $flag[j]$ stays true, because $j$ raised it before its own write to $turn$. But $i$ left its loop after its write, so it read $flag[j] = false$ or $turn \ne j$. Neither can happen.
- **Bypass 1.** Once process $i$ has finished its doorway, process $j$ enters at most once before $i$ does. To enter a second time, $j$ must run L2 again and write $turn = i$, and after that it waits until $i$ enters or lowers its flag.
- **Starvation freedom.** If $i$ waited forever, then by bypass 1 the other process would end up either in its remainder section, with its flag down, or waiting forever too. In the first case $i$ reads $flag[j] = false$. In the second case $turn$ no longer changes, and the process that it does not name leaves its loop. Both are contradictions.
- **First come, first served.** If $i$ finishes its doorway before $j$ starts its doorway, then $j$ writes $turn = i$ later and must wait for $i$. So the doorway of two writes gives FCFS order in Lamport's sense.

The test file checks these claims by exhaustive search of all interleavings: 101 states for one passage of each process, 401 for two passages, and 117 when both processes run forever. It finds no state with both processes in the critical section, no fair run in which a process waits forever, a bypass of exactly 1 counted from the end of the doorway, and FCFS order. It also checks the worked example above step by step, and runs 5 seeded random schedules of 3000 steps each. The algorithm is for two processes only, so it can only be checked with 2; the [filter lock](/filter-lock/) and the [tournament lock](/tournament-lock/) extend it to $n$ processes.

## Complexity

| measure | value |
|---|---|
| shared registers | 3: two single-writer flags and one multi-writer $turn$ |
| entry and exit without contention | 4 shared steps: L1, L2 and L4 to enter, L6 to leave |
| bypass after the doorway | 1 |
| RMRs per passage, CC model | $O(1)$; the test finds at most 5 in one entry section |
| RMRs per passage, DSM model | unbounded |

In the cache coherent (CC) model, a waiting process rereads $flag[j]$ and $turn$ from its cache, and it misses only when the other process writes one of them. The other process writes them only a bounded number of times while $i$ waits, by bypass 1, so the number of remote memory references is $O(1)$. In the distributed shared memory (DSM) model, each register lives in the memory module of one process. A waiting process reads $turn$ in each turn of its loop, and $turn$ is remote for at least one of the two processes, wherever it is placed. That process can make any number of remote references while it waits. See [RMR complexity](/rmr-complexity/) for the two models.

## Properties

- Uses atomic read/write registers only; no read-modify-write instruction.
- Deadlock free and starvation free, with bypass 1 and FCFS order after a doorway of two writes.
- Busy waiting: a waiting process takes steps, and it spins on registers that the other process writes.
- Needs sequential consistency, or at least an order of each write before the next read of the same process.
- Two processes only. The ids 0 and 1 are fixed in the code.

## Variants and improvements

- **Peterson's $n$-process algorithm.** The 1981 paper also gives a version for $n$ processes with $n - 1$ levels, each level a Peterson-like waiting room for one more process. Herlihy and Shavit call it the [filter lock](/filter-lock/). It is starvation free but not FCFS, and its bypass is not bounded by a function of $n$.
- **Tournament lock.** Peterson and Fischer (1977) put two-process locks at the nodes of a binary tree. A process climbs from its leaf to the root and takes $O(\log n)$ two-process locks. See [tournament lock](/tournament-lock/).
- **Kessels' algorithm.** Kessels (1982) replaces the multi-writer $turn$ by two single-writer bits, one written by each process, so that every register has a single writer. See [Kessels' algorithm](/kessels-algorithm/).
- **Dekker's algorithm.** The first correct two-process solution, reported by Dijkstra, also uses two flags and a turn, but a process lowers its flag while it waits for its turn. See [Dekker's algorithm](/dekker-algorithm/).
- **Many processes.** For $n$ processes with reads and writes, see the [bakery algorithm](/lamport-bakery-algorithm/). With an atomic instruction such as [test-and-set](/test-and-set/), one word is enough.

## When to use it

Use it to teach mutual exclusion and to see how a proof about interleavings works; the whole algorithm fits in five lines and the proof in a paragraph. Use it inside the nodes of a tournament lock, or in a system that has only plain loads and stores between two parties, for example two processors that share memory but no atomic instruction. In ordinary multithreaded code on current hardware, use a [mutex](/mutex/) from the system library or a lock built on an atomic instruction instead: such locks work for any number of threads, need no fences in user code, and can sleep instead of spin.

## Pitfalls

**TSO and x86.** On x86, each processor has a store buffer: a write goes into the buffer and reaches memory later, and a later read of another address can read memory before that. This is the store-load reordering of the x86-TSO model (Sewell et al. 2010). Peterson's algorithm then fails. The test file finds this run in the TSO mode of the explorer:

1. Process 0 writes $flag[0] \leftarrow true$ and $turn \leftarrow 1$. Both writes wait in its store buffer.
2. Process 0 reads $flag[1]$ from memory, gets false, and enters.
3. Process 1 writes $flag[1] \leftarrow true$ and $turn \leftarrow 0$ into its own buffer.
4. Process 1 reads $flag[0]$ from memory. The write of process 0 is still in its buffer, so it gets false and enters.

Both processes are in the critical section. The fix is a full fence after L2 and before L4: `MFENCE` on x86, or a locked instruction such as `XCHG` for the write of L2. The fence makes the process wait until its buffer is empty, so its flag is in memory before it reads the other flag. The test file adds the fence and finds no bad state for one passage, two passages and forever. Under TSO it checks only safety, because the explorer does not force a buffer to drain. On weaker hardware, such as ARM and POWER, more pairs of accesses can be reordered. In C11 and C++11, the portable fix is to make all three variables atomic and use `memory_order_seq_cst` for every access to them.

**Compilers.** Plain variables are not enough even on sequentially consistent hardware: a compiler may keep $flag[j]$ in a register and never read it again inside the loop, or move the reads before the writes. Use atomic types, or `volatile` in Java, which gives sequentially consistent accesses for these fields.

**Wrong order in the doorway.** The flag must be raised before $turn$ is written. With the opposite order, both processes can enter, as the section The algorithm shows; the test file finds this run.

**Spinning.** A waiting process spins and uses its processor. If the holder is preempted, the waiter spins for its whole time slice. Real locks spin for a short time and then sleep.

## Implementations

## History

Dijkstra (1965) stated the mutual exclusion problem and credited the first two-process solution to Dekker. Dekker's algorithm and the $n$-process solutions of Dijkstra (1965), Knuth (1966), de Bruijn (1967) and Eisenberg and McGuire (1972) have intricate entry sections and long proofs. Peterson and Fischer (1977) studied two-process locks inside a tree. Gary L. Peterson published the algorithm of this page in 1981 in a two-page note, "Myths about the mutual exclusion problem", in Information Processing Letters. His algorithm is a few lines long, and the same note generalizes it to $n$ processes. It became the standard first example in textbooks on operating systems and concurrent programming. Later work showed that it needs a fence on x86 and other machines with store buffers.

## References
