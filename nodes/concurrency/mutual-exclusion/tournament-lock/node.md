---
tag: RBPQNE
kind: algorithm
slug: tournament-lock
name: Tournament lock
aliases: [arbitration tree lock]
area: concurrency/mutual-exclusion
level: core
summary: N-process mutual exclusion from a binary tree of two-process locks. A process wins one lock at each level up to the root, so it takes O(log n) steps. Starvation free with Peterson nodes.
solves: [mutual-exclusion-problem]
complexity:
  vars: {n: the number of processes}
  space: {shared: Θ(n)}
  steps: {solo: Θ(log n)}
  rmr: {cc: Θ(log n), dsm: ∞}
  bypass: {worst: ∞}
properties: {deterministic: true, deadlock_free: true, starvation_free: true, fcfs: false, bounded_bypass: false, single_writer: false, bounded_registers: true, local_spinning: false}
history:
  year: 1977
  people: [Gary L. Peterson, Michael J. Fischer]
  note: Peterson and Fischer built n-process locks from a tree of two-process locks at STOC 1977. Yang and Anderson (1995) used a tree of local-spin locks to get O(log n) remote references.
prereqs: [mutual-exclusion-problem, peterson-algorithm]
see_also: [filter-lock, kessels-algorithm, lamport-bakery-algorithm, mcs-lock, rmr-complexity, mutual-exclusion-lower-bounds, starvation-freedom]
sources:
  - paper: doi:10.1145/800105.803398
    title: Gary L. Peterson and Michael J. Fischer, Economical solutions for the critical section problem in a distributed system (extended abstract), STOC 1977, pages 91-97
    locator: the tree of two-process solutions for n processes
  - paper: doi:10.1016/0020-0190(81)90106-X
    title: Gary L. Peterson, Myths about the mutual exclusion problem, Information Processing Letters 12(3), 1981, pages 115-116
    locator: the two-process algorithm that this page uses at each node
  - paper: doi:10.1007/BF01784242
    title: Jae-Heon Yang and James H. Anderson, A fast, scalable mutual exclusion algorithm, Distributed Computing 9(1), 1995, pages 51-60
    locator: the arbitration tree of local-spin two-process locks with O(log n) remote memory references in the CC and DSM models
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 10, Mutual Exclusion with Read/Write Shared Memory (the tournament algorithm)
  - paper: doi:10.1145/945526.945527
    title: K. Alagarsamy, Some myths about famous mutual exclusion algorithms, ACM SIGACT News 34(3), 2003, pages 94-103
    locator: the remarks on unbounded bypass in Peterson's algorithms, including the tournament with Peterson's two-process algorithm
---

The tournament lock solves the [mutual exclusion problem](/mutual-exclusion-problem/) for $n$ processes with a binary tree of two-process locks. Each process starts at a leaf and must win the two-process lock at each node on its way up. The winner at the root enters the critical section, and on the way out it releases the locks from the root down. Peterson and Fischer (1977) introduced the tree. This page uses [Peterson's two-process algorithm](/peterson-algorithm/) at each node, as textbooks do; Peterson and Fischer used a two-process algorithm of their own. A process takes $O(\log n)$ steps when it runs alone, the lock is starvation free, and it makes $O(\log n)$ remote memory references per passage on a cache-coherent machine. It is not first come, first served, and a slow process can be passed any number of times.

## In plain words

Think of a sports tournament. Players meet in pairs, the winner of each match goes to the next round, and the winner of the final gets the prize. Here the prize is the critical section, and each match is a small lock for two players.

A process that wants to enter plays the match at the lowest node of its path, then the match at the node above, and so on up to the root. At each node it meets at most one other process: the winner from the other half of that part of the tree.

When it leaves, it frees the root first and then the nodes below it. The order is important.

## The problem

There are $n \ge 2$ asynchronous processes $0, \ldots, n-1$. Each one repeats a remainder section, an entry section, a critical section and an exit section. The entry and exit sections must give mutual exclusion and starvation freedom, as the [mutual exclusion problem](/mutual-exclusion-problem/) defines. The shared memory has atomic read/write registers and is sequentially consistent. A process stays in its critical section for a finite time.

## The algorithm

Let $size$ be the smallest power of two with $size \ge n$. The tree is a complete binary tree with $size$ leaves, stored as a heap: node 1 is the root and node $x$ has the children $2x$ and $2x + 1$. Process $i$ starts at leaf $i + size$. When a process comes to node $x$ from child $2x + s$, it plays side $s \in \{0, 1\}$ of a Peterson lock at $x$, with registers $flag[x][0]$, $flag[x][1]$ (false at the start) and $turn[x]$.

```pseudo id=main
LOCK(i)
L1  for each node x on the path from the leaf of i up to the root, with i on side s of x
L2      flag[x][s] ← true
L3      turn[x] ← 1 − s
L4      loop
L5          if flag[x][1 − s] = false then exit the loop
L6          if turn[x] ≠ 1 − s then exit the loop
                                       ▷ critical section
UNLOCK(i)
L7  for each node x on the path from the root down to the leaf of i, with i on side s of x
L8      flag[x][s] ← false
```

The *doorway* is L2 and L3 at the lowest node. Lines L2 to L6 are Peterson's entry section at node $x$, and L8 is its exit section. A process holds node $x$ from the time it leaves the loop at $x$ until it lowers $flag[x][s]$.

Why must the exit go from the root down? Each side of a node is used by one process at a time only because the process holds the child on that side. If a process released its lowest node first, another process could win that node, come up and raise the same flag at the next node, and then the first process would lower that flag and erase it. The test file finds this run, and it ends with two processes in the critical section.

## Example

Four processes: 0 and 1 meet at node 2, 2 and 3 meet at node 3, and the winners meet at the root, node 1. Process 3 does not try. Each row is one or more shared steps; the test file runs this schedule step by step.

| step | process | action |
|---|---|---|
| 1 | 0 | at node 2: $flag[2][0] \leftarrow true$, $turn[2] \leftarrow 1$ |
| 2 | 1 | at node 2: $flag[2][1] \leftarrow true$, $turn[2] \leftarrow 0$ |
| 3 | 2 | at node 3: $flag[3][0] \leftarrow true$, $turn[3] \leftarrow 1$ |
| 4 | 0 | reads $flag[2][1] = true$, $turn[2] = 0 \ne 1$: wins node 2; at the root: $flag[1][0] \leftarrow true$, $turn[1] \leftarrow 1$ |
| 5 | 1 | reads $flag[2][0] = true$, $turn[2] = 0$: waits |
| 6 | 2 | reads $flag[3][1] = false$: wins node 3; at the root: $flag[1][1] \leftarrow true$, $turn[1] \leftarrow 0$ |
| 7 | 0 | reads $flag[1][1] = true$, $turn[1] = 0 \ne 1$: enters |
| 8 | 2 | reads $flag[1][0] = true$, $turn[1] = 0$: waits |
| 9 | 0 | leaves: $flag[1][0] \leftarrow false$, then $flag[2][0] \leftarrow false$ |
| 10 | 2 | reads $flag[1][0] = false$: enters |
| 11 | 1 | reads $flag[2][0] = false$: wins node 2; at the root: $flag[1][0] \leftarrow true$, $turn[1] \leftarrow 1$; reads $flag[1][1] = true$, $turn[1] = 1$: waits |
| 12 | 2 | leaves: $flag[1][1] \leftarrow false$, then $flag[3][0] \leftarrow false$ |
| 13 | 1 | reads $flag[1][1] = false$: enters |

## Correctness

The full proof is in proofs/correctness.md. It reduces the tree to Peterson's algorithm at each node.

- **Each side of a node has one user at a time.** By induction from the leaves up: a process runs the code of node $x$ only while it holds the child of $x$ on its side, because it starts at $x$ just after it wins the child and, in the exit section, it releases $x$ before the child. At most one process holds the child, so the passages on one side of $x$ come one after the other and never overlap. They act like one *virtual process* that runs Peterson's code again and again.
- **Mutual exclusion.** So each node runs Peterson's algorithm for two virtual processes, and at most one process holds it. The process in the critical section holds the root.
- **Starvation freedom.** By induction from the root down: a process that holds a node goes on up, holds the root, enters, and releases the nodes in finite time. So the "critical section" of each node is finite, and Peterson's starvation freedom at that node lets every waiting process win it.
- **No bound on bypass.** For $n \ge 3$, process 0 can finish its doorway at its lowest node and then be slow. Process 2 does not pass through that node, and at every node of its path the other flag is down, so it can enter again and again. Process 2 starts after process 0 finished its doorway and enters first, so the lock is not FCFS. Alagarsamy (2003) also notes unbounded bypass for this tree.

The test file checks mutual exclusion, deadlock freedom and starvation freedom by exhaustive search of all interleavings for 2 processes forever (117 states, the same as Peterson's algorithm, with bypass 1 and FCFS), for 3 processes with one passage each (3262 states) and forever (6466 states, with no FCFS order and no bound on bypass), and mutual exclusion and deadlock freedom for 4 processes with one passage each (58387 states). It runs the example above, and a run in which process 2 enters 20 times while process 0 waits after its doorway. It also runs seeded random schedules for 4 and 7 processes.

## Complexity

| measure | value |
|---|---|
| shared registers | $3(size - 1) < 6n$: two single-writer flags per side and one $turn$ per node |
| entry and exit without contention | $3\lceil \log_2 n \rceil$ steps to enter, $\lceil \log_2 n \rceil$ writes to leave |
| bypass after the doorway | 1 for $n = 2$; no bound for $n \ge 3$ |
| RMRs per passage, CC model | $\Theta(\log n)$ |
| RMRs per passage, DSM model | unbounded |

A process that runs alone writes the flag and the turn at each of the $\lceil \log_2 n \rceil$ nodes of its path and reads the other flag as false. The test file counts these steps for $n = 2$ to $8$.

In the cache coherent (CC) model, a read misses the cache only if the register was written since the last read by the same process. While a process waits at node $x$, it reads only $flag[x][1-s]$ and $turn[x]$, and Peterson's bypass 1 for the virtual processes means that the other side writes them only a bounded number of times before the process wins $x$. So each node costs $O(1)$ misses, and the passage costs $O(\log n)$. Each node of the path also costs at least its two writes, which count as remote references in this model, so the bound is tight. The test finds at most 5 RMRs in one entry section for 2 processes, and 10 for 3 processes run forever.

In the distributed shared memory (DSM) model, each register lives in the memory module of one process, and $turn[x]$ is remote for at least one of the processes that use node $x$. While another process holds the root for a long time, a process that waits at $x$ can read $turn[x]$ remotely any number of times. So the count is unbounded. Yang and Anderson (1995) fixed this with a two-process lock at each node in which a process spins only on a register in its own module. Their tree makes $O(\log n)$ remote references per passage in both the CC and the DSM model. Attiya, Hendler and Woelfel (2008) proved that $\Omega(\log n)$ is a lower bound for algorithms with reads and writes, so the tree is optimal in this sense. See [RMR complexity](/rmr-complexity/) and [lower bounds for mutual exclusion](/mutual-exclusion-lower-bounds/).

## Properties

- Uses atomic read/write registers only, with small values.
- Deadlock free and starvation free, because each node is.
- Not FCFS, and for $n \ge 3$ the bypass has no bound.
- The $turn$ registers have two writers each; the flags have one writer at a time, but different processes write the same flag over time.
- With Peterson nodes, busy waiting is not local in the DSM model.
- Any correct two-process lock can be put at the nodes. The tree keeps mutual exclusion and deadlock freedom, and starvation freedom if the node lock has it.

## Variants and improvements

- **Yang and Anderson's tree.** A local-spin two-process lock at each node gives $\Theta(\log n)$ RMRs in both models. With a fast path in front, a process that runs alone takes $O(1)$ steps. This was the first $O(\log n)$ RMR lock that uses only reads and writes.
- **Kessels' tree.** [Kessels' algorithm](/kessels-algorithm/) (1982) replaces the shared $turn$ at each node by two single-writer registers, so that every register in the tree has one writer.
- **Filter lock.** Peterson's other generalization, the [filter lock](/filter-lock/), lets every process pass all $n - 1$ levels and costs $\Theta(n^2)$ steps without contention.
- **Queue locks.** With an atomic instruction, queue locks such as the [MCS lock](/mcs-lock/) make $O(1)$ RMRs per passage and are FCFS.

## When to use it

Use it to build an $n$-process lock from a two-process lock, with a cost that grows with $\log n$ instead of $n$. The idea of a tree of small locks also appears in combining trees and in hierarchical locks for machines with many sockets. For a real lock on current hardware, a lock built on an atomic instruction, such as the [MCS lock](/mcs-lock/), is simpler and faster. The read/write tree matters when there is no such instruction, and in the theory of RMR complexity.

## Pitfalls

**Exit in the wrong order.** The locks must be released from the root down. If a process releases its lowest node first, a second process can win it and raise a flag at the next node while the first process still has to lower that same flag. The first process then erases the flag of the second one. The test file finds this run with 3 processes: two processes end up in the critical section.

**Fixed ids.** Each process must use its own leaf. Two threads with the same id break mutual exclusion at the lowest node.

**TSO and x86.** At each node, the write of $turn[x]$ can wait in a store buffer while the process reads the other flag. The test file finds a run with two processes in the critical section on the TSO model, and none when a full fence follows each write of $turn[x]$. Under TSO it checks only safety.

**Bypass.** The tree is starvation free, but a process that is slow after its doorway can be passed any number of times, so it gives no bound on the wait in terms of entries of others.

## Implementations

## History

Dijkstra (1965) posed the problem, and the first $n$-process solutions, by Dijkstra, Knuth (1966), de Bruijn (1967) and Eisenberg and McGuire (1972), let each process scan all the others. Peterson and Fischer (1977), at STOC, showed how to build $n$-process solutions from two-process ones by a binary tree, so that a process meets only $O(\log n)$ others. Peterson's 1981 note gave the short two-process algorithm that most textbooks now put at the nodes. Kessels (1982) built a tree in which each register has a single writer. Yang and Anderson (1995) used the tree with local-spin nodes and got $O(\log n)$ remote memory references, and Attiya, Hendler and Woelfel (2008) proved that no read/write algorithm can do better.

## References
