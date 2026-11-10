---
tag: 1ACZ46
kind: concept
slug: barrier-synchronization
name: Barrier synchronization
aliases:
- global barrier
- bulk synchronization barrier
area: parallel/mapreduce-and-bsp
level: core
summary: A point where all processes wait until every process has reached it, separating BSP supersteps. The dissemination barrier needs ceil(lg p) rounds of messages.
prereqs: [fetch-and-add]
see_also: [bsp-model, superstep, combining-tree, spin-lock, test-and-set, synchronizer]
sources:
  - paper: doi:10.1007/BF01379320
    title: "Debra Hensgen, Raphael Finkel and Udi Manber, Two algorithms for barrier synchronization, International Journal of Parallel Programming 17(1), 1988"
    locator: pp. 1-17, the dissemination barrier and the tournament barrier
  - paper: "John M. Mellor-Crummey and Michael L. Scott, Algorithms for scalable synchronization on shared-memory multiprocessors, ACM Transactions on Computer Systems 9(1), 1991"
    locator: pp. 21-65, the barrier section (centralized sense-reversing, combining tree, dissemination, tournament and tree barriers, with measurements)
  - book: isbn:9780123705914
    title: "Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, Morgan Kaufmann, 2008"
    locator: Chapter 17, Barriers (the sense-reversing barrier, combining tree barriers and the dissemination barrier)
---

A barrier is a synchronization point for a group of $p$ processes: no process passes the barrier until every process in the group has reached it. Barriers separate the [supersteps](/superstep/) of a [BSP](/bsp-model/) program and the phases of many shared-memory programs. A barrier can be built from a shared counter, from a tree, or from messages; the dissemination barrier needs $\lceil \lg p \rceil$ rounds of messages and no shared counter.

## In plain words

A group of hikers agrees to wait at each bridge until the whole group is there. Nobody crosses until the last hiker arrives. That is a barrier. It is easy to say but harder to build well. If every hiker reports to one leader, the leader becomes a queue, and the group waits for the leader to count. If hikers report in pairs, then pairs of pairs, the news spreads like a tournament and the wait grows only slowly with the size of the group. There is also a trap: if the group uses the same signal at every bridge, a fast hiker can reset the signal for the next bridge before a slow hiker has seen it for this one. Then both wait forever. Good barriers flip the meaning of the signal at each bridge.

## The idea

A barrier is used many times; each use is an episode. The property it must have is this: for each episode $e$, no process returns from its call of episode $e$ before all $p$ processes have called episode $e$. A barrier must also be live: when all $p$ processes have called it, all of them return.

### Central counter with sense reversal

The processes share a counter `count`, set to $0$, and a flag `flag`. Each process keeps a local bit `sense`.

```pseudo
procedure BARRIER()
    sense ← 1 − sense                         ▷ local to the process
    if FETCH-AND-INCREMENT(count) = p − 1 then  ▷ the last process to arrive
        count ← 0
        flag ← sense                          ▷ release the others
    else
        wait until flag = sense
```

The last arriving process resets the counter before it writes the flag, so no process of the next episode sees a stale count. A waiting process waits for the flag to equal its sense of the current episode, and the flag keeps that value until the last process of the next episode writes the other value. That cannot happen before all $p$ processes have arrived at the next episode, which includes the waiting process itself. So a slow process never misses its release. The cost is contention: $p$ [fetch-and-increment](/fetch-and-add/) operations on one memory word take $\Theta(p)$ time when they are serialized, and $p - 1$ processes spin on one flag.

### Combining tree

Put the processes at the leaves of a tree of fan-in $k$. A node waits for its $k$ children, then reports to its parent; the root, once all have reported, sends the release down the same tree. Each phase has $\lceil \log_k p \rceil$ levels, so a barrier takes $2\lceil \log_k p \rceil$ rounds, and no node receives more than $k - 1$ reports in a round. The [combining tree](/combining-tree/) for counters uses the same idea.

### Dissemination barrier

Hensgen, Finkel and Manber (1988) gave the dissemination barrier. Number the processes $0$ to $p - 1$. In round $r = 0, 1, \ldots, \lceil \lg p \rceil - 1$, process $i$ sends a signal to process $(i + 2^r) \bmod p$ and waits for the signal of round $r$ from process $(i - 2^r) \bmod p$. After the last round it leaves the barrier.

**Lemma.** After rounds $0$ to $r$, process $i$ knows that the processes $i, i - 1, \ldots, i - (2^{r+1} - 1)$ (taken mod $p$) have arrived.

*Proof.* By induction on $r$. Before round $0$, process $i$ knows only of itself, which is the set for "$r = -1$", of size $2^0$. In round $r$, process $i$ waits for the signal of process $j = i - 2^r$. That process sent it only after it finished round $r - 1$, so by the induction hypothesis it knew of $j, j - 1, \ldots, j - (2^r - 1)$. Together with the $2^r$ processes $i, \ldots, i - (2^r - 1)$ that $i$ already knew of, process $i$ now knows of the $2^{r+1}$ consecutive processes $i, \ldots, i - (2^{r+1} - 1)$. $\square$

After $\lceil \lg p \rceil$ rounds, $2^{\lceil \lg p \rceil} \ge p$, so each process knows that all $p$ have arrived, and it may leave. The barrier sends $p \lceil \lg p \rceil$ messages in all and each process sends and receives one message per round, so there is no hot spot.

**Lower bound.** Assume that in each round a process receives at most one message, and that a message carries at most what its sender knows. Then the number of processes that a process knows of at most doubles in a round, from $1$ at the start. To know of all $p$ it needs $2^r \ge p$, so every such barrier takes at least $\lceil \lg p \rceil$ rounds, and the dissemination barrier is optimal in this sense.

**Timing.** Let process $i$ arrive at time $a_i$ and let each message take one time unit. Process $i$ finishes round $r$ at $t_i(r) = \max\left(t_i(r-1), t_{i - 2^r}(r-1)\right) + 1$, with $t_i(-1) = a_i$. By induction, $t_i(r) \ge a_j + 1$ for each $j$ that $i$ knows of after round $r$, and $t_i(r) \le \max_j a_j + r + 1$. So every process leaves after the last arrival and at most $\lceil \lg p \rceil$ time units after it.

### In the BSP model

The [BSP model](/bsp-model/) charges a barrier as the constant $L$ in the cost $w + gh + L$ of each superstep. The dissemination barrier shows why $L$ grows with $p$ on real machines: even with no other traffic, a barrier needs about $\lg p$ message latencies.

## Examples

**Dissemination with $p = 5$.** The rounds use the distances $1$, $2$ and $4$, so $\lceil \lg 5 \rceil = 3$ rounds. Process $0$ knows of $\{0\}$ at the start, of $\{0, 4\}$ after round $0$, of $\{0, 4, 3, 2\}$ after round $1$, and of all five after round $2$. If the processes arrive at the times $0, 5, 1, 2, 0$, all five leave at time $8 = 5 + 3$.

**Tree with $p = 64$.** With fan-in $k = 4$ the tree has $\lceil \log_4 64 \rceil = 3$ levels, so a barrier takes $6$ rounds. With $k = 2$ it takes $12$ rounds, but each node handles only one report per round.

**A non-example: reuse without sense reversal.** Change the counter barrier so that the first process to arrive sets `flag` to $0$, and the last one sets it to $1$; the others wait for `flag = 1`. One episode works. With $p = 2$ and two episodes: $A$ arrives, sets the flag to $0$ and waits. $B$ arrives last, sets the flag to $1$ and leaves. Before $A$ reads the flag, $B$ reaches the next episode, arrives first and sets the flag to $0$. Now $A$ waits for the flag of episode 1, which will never be $1$ again, and $B$ waits for $A$ in episode 2: a deadlock. In the simulator of this page, with three processes and three episodes, most random interleavings end in this deadlock, and the sense-reversing barrier never does.

## Where it is used

- BSP and its descendants. Each superstep of a [BSP](/bsp-model/) program, each superstep of [Pregel](/pregel-model/), and each round of a [MapReduce](/mapreduce-model/) job (where reduce tasks start only after the map phase) ends with a barrier.
- Shared-memory programming. OpenMP puts a barrier at the end of a parallel loop unless it is told not to, POSIX threads have `pthread_barrier_wait`, and Java has `CyclicBarrier`.
- Message passing. MPI has `MPI_Barrier`, which libraries often build as a dissemination barrier or a tree.
- GPUs. In CUDA, `__syncthreads()` is a barrier for the threads of one block; a barrier for the whole grid is usually the end of a kernel launch.

## References
