---
tag: F0CXA1
kind: algorithm
slug: kessels-algorithm
name: Kessels' algorithm
aliases: [Kessels mutual exclusion]
area: concurrency/mutual-exclusion
level: advanced
summary: Peterson's lock with the shared turn split into two registers, one per process, so that no register has two writers. A binary tree of these locks serves n processes.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes}
  space: {shared: Θ(n)}
  steps: {solo: Θ(log n)}
  rmr: {cc: Θ(log n), dsm: ∞}
  bypass: {worst: ∞}
properties: {deterministic: true, deadlock_free: true, starvation_free: true, fcfs: false, bounded_bypass: false, single_writer: true, bounded_registers: true, local_spinning: false}
history:
  year: 1982
  people: [J. L. W. Kessels]
  note: Kessels gave a two-process solution without common modifiable variables in Acta Informatica in 1982, and built an n-process solution from a binary tree of it.
prereqs: [mutual-exclusion-problem, peterson-algorithm, tournament-lock]
see_also: [filter-lock, lamport-bakery-algorithm, burns-lamport-algorithm, rmr-complexity, mutual-exclusion-lower-bounds, starvation-freedom]
sources:
  - paper: doi:10.1007/BF00288966
    title: J. L. W. Kessels, Arbitration without common modifiable variables, Acta Informatica 17(2), 1982, pages 135-141
    locator: the two-process solution with single-writer variables, and its generalization by a binary arbitration tree
  - paper: doi:10.1016/0020-0190(81)90106-X
    title: Gary L. Peterson, Myths about the mutual exclusion problem, Information Processing Letters 12(3), 1981, pages 115-116
    locator: the two-process algorithm with a shared turn register, which Kessels' algorithm changes
  - paper: doi:10.1145/800105.803398
    title: Gary L. Peterson and Michael J. Fischer, Economical solutions for the critical section problem in a distributed system (extended abstract), STOC 1977, pages 91-97
    locator: the tree of two-process solutions for n processes
  - paper: arxiv:2507.13198
    title: Rob van Glabbeek, Bas Luttik and Myrthe Spronck, Just verification of mutual exclusion algorithms, 2025 (a short version is in CONCUR 2025)
    locator: Table 1, the results for Kessels' algorithm with atomic, regular and safe registers
---

Kessels' algorithm solves the [mutual exclusion problem](/mutual-exclusion-problem/) for two processes with registers that each have only one writer. It is [Peterson's algorithm](/peterson-algorithm/) with one change: the shared register $turn$, which both processes write, is split into two registers $t_0$ and $t_1$, and the turn is their exclusive or. Kessels (1982) also put this two-process lock at the nodes of a binary tree, as in the [tournament lock](/tournament-lock/), to get a lock for $n$ processes. The two-process lock is starvation free and first come, first served with bypass 1. The tree is starvation free, takes $O(\log n)$ steps without contention, and has no bound on bypass for $n \ge 3$.

## In plain words

In Peterson's lock, two people share one sign that says whose turn it is to wait. Both of them write on the same sign.

In Kessels' lock, each person has a sign of their own and writes only on it. Each sign shows 0 or 1. If the two signs show the same value, it is person 0's turn to wait; if they differ, it is person 1's turn.

When person 0 wants to enter, it copies the sign of person 1, so the signs agree and person 0 waits. Person 1 does the opposite: it sets its sign to differ from the sign of person 0. So the one who wrote last waits, as in Peterson's lock.

## The problem

There are $n \ge 2$ asynchronous processes $0, \ldots, n - 1$. Each one repeats a remainder section, an entry section, a critical section and an exit section. The entry and exit sections must give mutual exclusion and starvation freedom, as the [mutual exclusion problem](/mutual-exclusion-problem/) defines. The shared memory has atomic read/write registers and is sequentially consistent. A process stays in its critical section for a finite time. Kessels added one more wish: no shared register may be written by two processes, so that each register can live in the memory of its writer and no two writes ever compete for it.

## The algorithm

For two processes there is one node. Process $s \in \{0, 1\}$ has a flag $b[s]$ (false at the start) and a register $t[s] \in \{0, 1\}$ (0 at the start). Let $T = t[0] \oplus t[1]$. Process $s$ waits while the other flag is up and $T = s$.

For $n$ processes, let $size$ be the smallest power of two with $size \ge n$. The tree is a complete binary tree with $size$ leaves, stored as a heap: node 1 is the root and node $x$ has the children $2x$ and $2x + 1$. Process $i$ starts at leaf $i + size$. When it comes to node $x$ from child $2x + s$, it plays side $s$ of the two-process lock at $x$, with the registers $b[x][s]$ and $t[x][s]$. For $n = 2$ the tree is one node.

```pseudo id=main
LOCK(i)
L1  for each node x on the path from the leaf of i up to the root, with i on side s of x
L2      b[x][s] ← true
L3      o ← t[x][1 − s]
L4      if s = 0 then mine ← o else mine ← 1 − o
L5      t[x][s] ← mine
L6      loop
L7          if b[x][1 − s] = false then exit the loop
L8          o ← t[x][1 − s]
L9          if (s = 0 and mine ≠ o) or (s = 1 and mine = o) then exit the loop
                                       ▷ critical section
UNLOCK(i)
L10 for each node x on the path from the root down to the leaf of i, with i on side s of x
L11     b[x][s] ← false
```

Line L4 picks $mine$ so that $mine \oplus o = s$. So after the write at L5, $T = s$, unless the other side changed its $t$ since the read at L3. The test at L9 succeeds exactly when $T \ne s$. The local variable $mine$ is always equal to $t[x][s]$, so a process never needs to read its own register.

The *doorway* is L2 to L5 at the lowest node. A process holds node $x$ from the time it leaves the loop at $x$ until it lowers $b[x][s]$. As in the tournament lock, the exit goes from the root down, so that each side of a node is used by one process at a time.

## Example

Two processes, one node; write $b_s$ and $t_s$ for $b[1][s]$ and $t[1][s]$. The test file runs this schedule step by step.

| step | process | action | $t_0, t_1$ | $T$ |
|---|---|---|---|---|
| 1 | 0 | $b_0 \leftarrow true$; reads $t_1 = 0$, so $mine = 0$; $t_0 \leftarrow 0$ | 0, 0 | 0 |
| 2 | 1 | $b_1 \leftarrow true$; reads $t_0 = 0$, so $mine = 1$; $t_1 \leftarrow 1$ | 0, 1 | 1 |
| 3 | 1 | reads $b_0 = true$ and $t_0 = 0 \ne mine$: $T = 1$, so it waits | 0, 1 | 1 |
| 4 | 0 | reads $b_1 = true$ and $t_1 = 1 \ne mine$: $T = 1 \ne 0$, so it enters | 0, 1 | 1 |
| 5 | 1 | reads $b_0 = true$ and $t_0 = 0$: still waits | 0, 1 | 1 |
| 6 | 0 | leaves: $b_0 \leftarrow false$ | 0, 1 | 1 |
| 7 | 1 | reads $b_0 = false$: enters | 0, 1 | 1 |

Process 1 wrote its $t$ last, so it gave way, just as the process that writes $turn$ last gives way in Peterson's algorithm.

## Correctness

The full proof is in proofs/correctness.md.

- **Mutual exclusion, two processes.** The proof uses four invariants. The main one says: if process $i$ is in the critical section and process $j$ has finished its doorway, then $T = j$. The others say that a value of $t$ that a process read at L3 is still current when that matters. Together they are kept by every step, and two processes in the critical section would need $T = 0$ and $T = 1$ at once.
- **Bypass 1 and FCFS.** After process $i$ finishes its doorway, $t[i]$ and $b[i]$ do not change until it leaves. A passage of $j$ that starts after that reads the current $t[i]$, writes $T = j$, and waits until $i$ leaves.
- **Starvation freedom.** If both processes waited forever, $T$ would be constant, and one of them would see $T$ different from its own index.
- **The tree.** The proof is the same as for the [tournament lock](/tournament-lock/): each side of a node is used by one process at a time, so the processes on one side act as one virtual process, and each node runs the two-process algorithm. For $n \ge 3$ a process that is slow after its doorway can be passed any number of times by a process from the other half of the tree.

The test file checks mutual exclusion, deadlock freedom and starvation freedom by exhaustive search of all interleavings. The two-process algorithm has only two processes, so it is checked with 2: 101 states with one passage each and 234 states forever, with bypass 1 and FCFS. The tree for 3 processes is checked with one passage each (3385 states) and forever (20436 states, with no FCFS order and no bound on bypass). The tests also run the example above, a run in which process 2 enters 20 times while process 0 waits after its doorway, and seeded random schedules for 4 and 7 processes.

## Complexity

| measure | value |
|---|---|
| shared registers | $4(size - 1) < 8n$: one $b$ and one $t$ per side of each node |
| entry and exit without contention | $4\lceil \log_2 n \rceil$ accesses to enter, $\lceil \log_2 n \rceil$ writes to leave |
| bypass after the doorway | 1 for $n = 2$; no bound for $n \ge 3$ |
| RMRs per passage, CC model | $\Theta(\log n)$ |
| RMRs per passage, DSM model | unbounded |

A process that runs alone does at each node of its path two writes and two reads: it writes $b$, reads the other $t$, writes its own $t$, and reads the other $b$ as false. The test file counts these steps for $n = 2$ to $8$.

In the cache coherent (CC) model, a waiting process reads only the other side's $b$ and $t$, and they change only a bounded number of times before it wins the node, because of bypass 1 at the node. So each node costs $O(1)$ remote references and a passage costs $\Theta(\log n)$. This is an argument, not a full proof. The test finds at most 7 RMRs in one entry section for 2 processes run forever, and 11 for 3 processes with one passage each.

In the distributed shared memory (DSM) model, each register can live in the module of its writer, but a waiting process spins on the registers of the other side, which are remote. So the count is unbounded, as for Peterson's algorithm. Yang and Anderson (1995) built a tree with local-spin nodes for $O(\log n)$ in both models; see [RMR complexity](/rmr-complexity/).

## Properties

- Uses atomic read/write registers only. Each register holds one of two values.
- In the two-process algorithm each register has one writer: $b[s]$ and $t[s]$ are written only by process $s$. In the tree, the registers of side $s$ of node $x$ are written only by the processes below that side, and by Lemma 4 of the proof only one of them at a time.
- Deadlock free and starvation free. The two-process algorithm is FCFS with bypass 1; the tree for $n \ge 3$ is not FCFS and has no bound on bypass.
- A process never reads its own registers; it keeps $mine$ in a local variable.
- Not correct when the registers are not atomic. With safe registers, a read that overlaps a write may return any value, even when the write does not change the value. The test file finds a run in which process 1 reads $t_0 = 1$ while process 0 writes 0 over 0, and both processes enter. Van Glabbeek, Luttik and Spronck (2025) list Kessels' algorithm as not correct with safe or with regular registers.

## Variants and improvements

- **Peterson's algorithm.** The same algorithm with one shared $turn$ register that both processes write. [Peterson's algorithm](/peterson-algorithm/) is shorter, but its $turn$ register has two writers.
- **Tournament lock.** The same tree with Peterson's lock at each node is the [tournament lock](/tournament-lock/).
- **Local-spin trees.** Yang and Anderson (1995) put a two-process lock at each node in which a process spins only on a register in its own memory module, and got $O(\log n)$ RMRs in the DSM model too.
- **One-bit algorithms.** The [Burns and Lamport algorithm](/burns-lamport-algorithm/) uses one single-writer flag per process for $n$ processes, but it is not starvation free.
- **Bakery.** [Lamport's bakery algorithm](/lamport-bakery-algorithm/) is another solution with only single-writer registers. It is FCFS, but its registers have no bound and a process scans all others.

## When to use it

Use it in a system in which a register can only be written by its owner, for example when each process may write only to its own memory or its own message slot, and the others may only read it. It also shows that the shared $turn$ of Peterson's algorithm is not needed. On real hardware with atomic instructions, a lock such as the [MCS lock](/mcs-lock/) is simpler and faster.

## Pitfalls

**TSO and x86.** The algorithm needs two fences on TSO hardware. Without a fence after L2, the read of $t$ at L3 can pass the write of $b$, and without a fence after L5, the reads in the loop can pass the write of $t$. The test file finds a run with two processes in the critical section on the TSO model, and none when a full fence follows each of the two writes. Under TSO it checks only safety.

**Non-atomic registers.** The algorithm is not correct with safe or regular registers; see Properties. Use atomic registers.

**Exit in the wrong order.** In the tree, the exit must go from the root down, as in the [tournament lock](/tournament-lock/).

**The two codes differ.** Process 0 copies the other value and process 1 writes its opposite. If both copied the other value, every write would make $T = 0$. Then process 1 would never wait, and it could enter while process 0 is in the critical section.

## Implementations

## History

Dijkstra (1965) posed the problem. Peterson (1981) gave the short two-process algorithm with flags and one $turn$ register. Kessels, at Philips Research in Eindhoven, published "Arbitration without common modifiable variables" in Acta Informatica in 1982. He removed the register with two writers from Peterson's algorithm and generalized the solution to $n$ processes by a binary arbitration tree, the idea that Peterson and Fischer (1977) had used. In 2025, van Glabbeek, Luttik and Spronck checked the algorithm with a model checker under several memory models. In their usual model it has mutual exclusion, deadlock freedom and starvation freedom with atomic registers, and none of the three with safe or regular registers.

## References
