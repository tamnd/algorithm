---
tag: D9FWRC
kind: algorithm
slug: work-stealing
name: Work stealing
aliases:
- work-stealing scheduler
- randomized work stealing
area: parallel/work-span-models
level: core
summary: Each processor works at the bottom of its own deque, and an idle processor steals the top item of a random victim's deque. Expected time T_1/p + O(T_infinity).
solves: [precedence-constrained-scheduling]
model: work-span-model
complexity:
  vars: {w: the work T_1, s: the span T_infinity, p: the number of processors, m: the stack space of a serial run}
  time: {expected: w/p + O(s)}
  space: {worst: p m}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1994
  people: [Robert D. Blumofe, Charles E. Leiserson]
  note: Blumofe and Leiserson gave the randomized work-stealing scheduler and its time, space and communication bounds at FOCS 1994. The journal version appeared in 1999.
prereqs: [fork-join-model, computation-dag, deque, greedy-scheduling]
see_also: [blumofe-leiserson-bound, greedy-scheduling, brent-theorem, parallel-slackness, chase-lev-deque, arora-blumofe-plaxton-deque, fork-join-parallelism, parallel-fibonacci]
sources:
  - paper: doi:10.1145/324133.324234
    title: "Robert D. Blumofe and Charles E. Leiserson, Scheduling multithreaded computations by work stealing, Journal of the ACM 46(5), 1999"
    locator: Section 4 (the algorithm and its space bound), Sections 5 and 6 (the atomic-access model and the analysis of time, steal attempts and communication)
  - paper: doi:10.1145/277651.277678
    title: "Nimar S. Arora, Robert D. Blumofe and C. Greg Plaxton, Thread scheduling for multiprogrammed multiprocessors, SPAA 1998"
    locator: Section 3 (the non-blocking work stealer at the level of DAG nodes, and the structural lemma) and Section 4 (the analysis with a potential function)
  - paper: doi:10.1145/277650.277725
    title: "Matteo Frigo, Charles E. Leiserson and Keith H. Randall, The implementation of the Cilk-5 multithreaded language, PLDI 1998"
    locator: the work-first principle, the two clones of each procedure, and the THE protocol for the deque
  - paper: "Robert D. Blumofe, Christopher F. Joerg, Bradley C. Kuszmaul, Charles E. Leiserson, Keith H. Randall and Yuli Zhou, Cilk: an efficient multithreaded runtime system, PPoPP 1995"
    locator: pp. 207-216, the Cilk runtime and its work-stealing scheduler
---

Work stealing is an online [scheduler](/precedence-constrained-scheduling/) for [fork-join](/fork-join-model/) programs on $p$ processors. Each processor keeps a [deque](/deque/) of ready work and uses its bottom end as a call stack, and a processor with no work steals the top item of the deque of another processor, chosen uniformly at random. Blumofe and Leiserson proved that the expected running time is $T_1/p + O(T_\infty)$, which is within a constant factor of the best possible time, and that the space is at most $p$ times the space of a serial run. The Cilk language is built on it, and many later task-parallel runtimes use a form of it.

## In plain words

A group of cooks shares a large job that splits into smaller jobs. Each cook has a personal pile of jobs to do later. When a cook splits a job, the cook starts the first part at once and puts the rest on top of the pile. When the current job is done, the cook takes the job most recently put on the pile.

A cook with an empty pile does not wait for orders. The cook picks another cook at random and takes the job at the bottom of that cook's pile, the oldest job there. Old jobs are usually large, so one theft gives the thief a lot of work, and thefts are rare. When every cook is busy, no cook talks to any other cook, so the cost of the coordination is paid only when some cook has nothing to do.

## The problem

The input is a [computation DAG](/computation-dag/) $G$ that a fork-join program makes as it runs. Each node is a unit-time strand. A node has at most two successors, and a node with two successors is a *spawn* node: one successor is the first node of the spawned child, and the other is the *continuation* in the parent. The root is the only node with no predecessor. The scheduler does not know $G$ in advance. It sees a node only when the node becomes *enabled*, at the moment its last predecessor finishes.

The output is a schedule: a step number and a processor for each node. Each step runs at most $p$ nodes, and each node runs in a later step than all of its predecessors. The goal is a small number of steps $T_p$, with little communication between processors and little space. We use the notation of the [work-span model](/work-span-model/).

| Symbol | Meaning |
|---|---|
| $n$ | the input size of the program |
| $p$ | the number of processors |
| $W = T_1$ | the work: the number of nodes of $G$ |
| $S = T_\infty$ | the span: the number of nodes on a longest path of $G$ |
| $T_p$ | the number of steps on $p$ processors |
| $W/S$ | the [parallelism](/parallelism/) |
| $S_1$ | the stack space of a serial run |

## The algorithm

Each processor $q$ has a deque $D_q$ and at most one *assigned* node. The owner of $D_q$ pushes and pops at the bottom, and thieves remove from the top. At the start, processor 0 has the root assigned, and all deques are empty. In each step, every processor runs one pass of the loop body. This is the node-level form of the scheduler, as in Arora, Blumofe and Plaxton.

```pseudo id=main
WORK-STEAL(G, p)                ▷ the code for processor q; all p processors run it in steps
L1  loop until all nodes of G are executed
L2      if q has an assigned node u then
L3          execute u
L4          if u enables two nodes then                       ▷ u is a spawn node
L5              push the continuation on the bottom of D_q, and assign the child to q
L6          else if u enables one node v then assign v to q
L7          else if D_q is not empty then pop the bottom node of D_q and assign it to q
L8          else q has no assigned node
L9      else                                                   ▷ q is a thief
L10         choose a victim r uniformly at random from the other p − 1 processors
L11         if D_r is not empty then remove the top node of D_r and assign it to q
```

Line L5 is the *work-first* rule: the processor runs the child at once, as a serial program does, and leaves the rest of the parent for thieves. So a processor that never meets a thief runs its nodes in the order of the serial program. Line L6 also covers the case in which $u$ is the last child to finish before a sync: the sync node becomes enabled, and $u$'s processor goes on with it. A node that $u$ makes ready but that still waits for another predecessor is not enabled, and line L7 or L8 runs. In one step, the owners act first and the thieves after them, one at a time, so two thieves never get the same node. A steal attempt at an empty deque fails, and the thief tries again in the next step.

## Example

Take the divide-and-conquer sum of 4 items: SUM$[lo, hi)$ spawns SUM$[lo, mid)$, calls SUM$[mid, hi)$, syncs and adds. Each call has an entry node and an exit node, a leaf does one addition, and an inner call has a spawn node, a sync node and one addition. The DAG has $T_1 = 27$ nodes and span $T_\infty = 13$. The nodes are numbered in the order of the serial run: 0 is the entry of SUM$[0,4)$, 1 is its spawn node, 2 to 12 are SUM$[0,2)$, 13 to 23 are SUM$[2,4)$, and 24 to 26 are the sync, the addition and the exit of the root. Here is one run on $p = 2$ processors.

| step | processor 0 | processor 1 | deques after the step |
|---|---|---|---|
| 1 | runs 0 | steal attempt, $D_0$ is empty | both empty |
| 2 | runs spawn node 1: pushes 13, takes child 2 | steals 13 from the top of $D_0$ | both empty |
| 3 | runs 2, the entry of SUM$[0,2)$ | runs 13, the entry of SUM$[2,4)$ | both empty |
| 4 | runs spawn node 3: pushes 7, takes 4 | runs spawn node 14: pushes 18, takes 15 | $D_0 = [7]$, $D_1 = [18]$ |
| 5 to 7 | runs 4, 5, 6 (SUM$[0,1)$), then pops 7 | runs 15, 16, 17 (SUM$[2,3)$), then pops 18 | both empty |
| 8 to 10 | runs 7, 8, 9 (SUM$[1,2)$) | runs 18, 19, 20 (SUM$[3,4)$) | both empty |
| 11 to 13 | runs 10, 11, 12: sync, add, exit | runs 21, 22, 23: sync, add, exit | both empty |
| 14 to 16 | three failed steal attempts | runs 24, 25, 26: sync, add, exit | both empty |

At step 7, node 6 finishes SUM$[0,1)$, but the sync node 10 still waits for node 9, so processor 0 pops node 7 from its own deque. At step 13, node 12 finishes SUM$[0,2)$ while node 23 finishes SUM$[2,4)$ on processor 1, so processor 1 enables the root sync node 24 and goes on with it. The run takes $T_2 = 16$ steps with 5 steal attempts and 1 successful steal. Each processor step runs a node or makes an attempt, and $2 \cdot 16 = 27 + 5$. The lower bounds give $T_2 \ge \max(\lceil 27/2 \rceil, 13) = 14$.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows three facts. First, at the end of each step, each node that is enabled and not yet executed is in exactly one place: assigned to one processor or in one deque. A node enters a place once, when it becomes enabled, and it leaves its deque only to become assigned. So each node runs at most once, and only after all its predecessors. Second, a processor whose deque is not empty always has an assigned node, because line L8 runs only when the deque is empty and a thief never takes the assigned node. Third, while nodes remain, a minimal node that is not executed is enabled, so by the first two facts some processor has an assigned node and the next step executes at least one node. So the run ends, each node runs exactly once, and $T_p \le T_1$.

## Complexity

In each step, each processor either executes one node or makes one steal attempt. If $A$ is the number of steal attempts in the run, then

$$p \cdot T_p = T_1 + A, \qquad\text{so}\qquad T_p = \frac{T_1}{p} + \frac{A}{p}.$$

All the cost of the scheduling is in $A$, and the analysis bounds $A$. The bounds below are proved by Blumofe and Leiserson for fully strict computations (each join edge goes from a child to its parent, as in the fork-join model) in their atomic-access model, in which concurrent steal requests to one deque wait in a queue. The theorem page [Blumofe-Leiserson bound](/blumofe-leiserson-bound/) gives the exact statements and a proof sketch.

- **Steal attempts.** $\mathrm{E}[A] = O(p \, T_\infty)$, and $A = O(p\,(T_\infty + \lg(1/\varepsilon)))$ with probability at least $1 - \varepsilon$.
- **Time.** $\mathrm{E}[T_p] = T_1/p + O(T_\infty)$. With probability at least $1 - \varepsilon$, $T_p = T_1/p + O(T_\infty + \lg p + \lg(1/\varepsilon))$. The $\lg p$ term comes from the queues of contending thieves.
- **Space.** At most $S_1 \, p$, for each run, where $S_1$ is the stack space of the serial run.
- **Communication.** The expected number of bytes sent is $O(p \, T_\infty (1 + n_d) S_{max})$, where $S_{max}$ is the size of the largest activation frame and $n_d$ is the largest number of join edges from one thread to its parent.

Every schedule needs $T_p \ge T_1/p$ by the [work law](/work-law/) and $T_p \ge T_\infty$ by the [span law](/span-law/). So the expected time is within a constant factor of the optimum. When the [parallel slackness](/parallel-slackness/) $T_1/(p\,T_\infty)$ is large, the term $T_1/p$ dominates and the [speedup](/speedup/) is nearly $p$.

## Properties

- **Online and distributed.** The scheduler needs no knowledge of the DAG, and it has no central queue. A processor touches the deque of another processor only when it has no work.
- **Serial order on each processor.** Between steals, a processor runs its nodes in the serial order of the program. This keeps the cache behaviour and the stack discipline of the serial program.
- **Few migrations.** Only stolen nodes move between processors. When the slackness is large, almost all nodes run where they became enabled.
- **Deque shape.** By the structural lemma of Blumofe and Leiserson (Lemma 4), the threads in a deque, from the top down, form a chain in which each thread is the parent of the next, and the bottom thread is the parent of the thread that the processor runs. So the top item is the oldest and usually the largest piece of work.
- **Randomized.** The schedule depends on the random choices of the thieves. Only the time is random; the result of a program without [determinacy races](/determinacy-race/) is the same in every run.
- **Not greedy.** A step can have idle processors while nodes wait in deques, because a thief can pick an empty deque. So the bound of a [greedy scheduler](/greedy-scheduling/), $T_1/p + T_\infty$, does not apply directly. Randomization replaces it with the same bound in expectation, up to the constant factor.

## Variants and improvements

- **Non-blocking deques.** Arora, Blumofe and Plaxton gave a deque in which the owner and the thieves need no locks, and proved the bound in multiprogrammed systems, where the operating system can take processors away. See the [Arora-Blumofe-Plaxton deque](/arora-blumofe-plaxton-deque/) and the growable [Chase-Lev deque](/chase-lev-deque/).
- **The THE protocol.** Cilk-5 uses a deque in which the owner takes a lock only when a thief may want the same item. The common path costs a few memory operations.
- **Child stealing.** Some runtimes push the child task and go on with the parent. Thieves then steal children, not continuations. This is easier to build as a library, but the serial order of the work-first rule is lost, and so is the space bound: a loop that spawns many children puts all of them in the deque before any of them runs.
- **Steal half.** A thief takes half of the victim's deque. This helps when many small tasks wait in one deque.
- **Locality-aware stealing.** A thief first tries victims that share a cache or a memory node with it.

## When to use it

Use work stealing to run nested, dynamic parallelism, such as recursive divide and conquer, parallel loops of uneven cost and tree searches. It needs a computation whose parallelism $T_1/T_\infty$ is much larger than $p$, so that steals are rare. For a parallel loop of equal iterations on a fixed number of threads, a static split is simpler and costs less. For a computation with a known DAG and known costs, an offline schedule can be better.

## Pitfalls

- **Steal from the wrong end.** A thief must take the top (oldest) node. If thieves take the bottom, they get small pieces of work, steals become frequent, and the deque shape that the analysis needs is lost.
- **Race between the owner and a thief.** When one item is left in a deque, the owner's pop and a thief's steal can both take it. The deque must resolve this case with a lock, an atomic compare-and-swap or a protocol such as THE.
- **Too fine a grain.** Each spawn pushes and pops a deque item. A spawn in an inner loop of tiny work makes this overhead dominate $T_1$. Coarsen the base case of the recursion.
- **Not enough parallelism.** The bound has the term $O(T_\infty)$ with a constant. If $T_1/T_\infty$ is close to $p$, the steal overhead is a large part of the time, and the speedup is far below $p$.
- **Blocking inside a task.** The analysis assumes that a node never waits, except at a sync. A task that blocks on a lock or on I/O holds its processor, and the bound does not hold.
- **The high-probability bound.** The bound $T_1/p + O(T_\infty)$ is in expectation. The bound with probability $1 - \varepsilon$ in the atomic-access model has the extra term $O(\lg p + \lg(1/\varepsilon))$.

## Implementations

## History

Blumofe and Leiserson say that the idea of work stealing goes back at least to the work of Burton and Sleep on the parallel run of functional programs (1981) and to Halstead's Multilisp (1984). Blumofe and Leiserson gave the randomized work-stealing scheduler for fully strict computations and proved its time, space and communication bounds. The conference version appeared at FOCS 1994 and the journal version in 1999. The Cilk runtime system of Blumofe and others (1995) used the scheduler, and Frigo, Leiserson and Randall described the work-first principle and the THE protocol of Cilk-5 in 1998. Arora, Blumofe and Plaxton gave the non-blocking version and its analysis for multiprogrammed systems in 1998.

## References
