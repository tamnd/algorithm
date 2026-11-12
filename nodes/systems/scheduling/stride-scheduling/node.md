---
tag: RJMX01
kind: algorithm
slug: stride-scheduling
name: Stride scheduling
area: systems/scheduling
level: advanced
summary: The deterministic form of lottery scheduling. Each client has a stride inverse to its tickets; the client with the smallest pass runs and adds its stride, so pairwise errors stay under one quantum.
solves: [cpu-scheduling]
model: word-ram
complexity:
  vars: {n: the number of quanta, c: the number of clients}
  time: {worst: O(n log c + c)}
  space: {extra: O(c)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1995
  people: [Carl A. Waldspurger, William E. Weihl]
  note: Waldspurger and Weihl gave stride scheduling, the deterministic counterpart of lottery scheduling, in an MIT technical report of June 1995.
prereqs: [lottery-scheduling, priority-queue]
see_also: [completely-fair-scheduler, weighted-fair-queueing, generalized-processor-sharing, weighted-round-robin, virtual-time, binary-heap, multilevel-queue-scheduling, round-robin]
sources:
  - paper: "Carl A. Waldspurger and William E. Weihl, Stride Scheduling: Deterministic Proportional-Share Resource Management, technical memorandum MIT/LCS/TM-528, MIT Laboratory for Computer Science, June 1995"
    title: "Stride Scheduling: Deterministic Proportional-Share Resource Management"
    locator: the basic algorithm (stride1, stride, pass and the priority queue), the dynamic version with the global pass, and the error analysis against lottery scheduling
  - paper: "Carl A. Waldspurger, Lottery and Stride Scheduling: Flexible Proportional-Share Resource Management, PhD thesis, MIT, 1995, technical report MIT/LCS/TR-667"
    title: "Lottery and Stride Scheduling: Flexible Proportional-Share Resource Management"
    locator: the chapter on stride scheduling, including hierarchical stride scheduling
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces
    locator: Chapter 9, Scheduling, Proportional Share, Section 9.6 (stride scheduling, the trace of Figure 9.3 with strides 100, 200 and 40)
---

Stride scheduling is a deterministic proportional-share [CPU scheduling](/cpu-scheduling/) policy. Client $c$ holds $t_c$ tickets, as in [lottery scheduling](/lottery-scheduling/), and it gets a *stride* $s_c = \mathit{stride1} / t_c$, where $\mathit{stride1}$ is a large constant. Each client also has a *pass* value. Each quantum goes to the client with the smallest pass, and that client's pass grows by its stride. A client with twice the tickets has half the stride, so it runs twice as often. Unlike the lottery, whose error grows like $\sqrt{n}$ after $n$ quanta, stride scheduling keeps the error between any two clients below one quantum.

## In plain words

Think of each program as a runner on a track. A program with many tickets takes short steps, and a program with few tickets takes long steps. At each moment, the runner who is furthest behind gets to take one step, and that step is one time slot of processor time.

The runners stay close together, because whoever falls behind moves next. A runner with short steps needs many steps to cover the same distance, so it gets many time slots. Nothing is random, so the parts are almost exact even over short times: no program is ever more than about one time slot ahead of its fair part, compared with any other program.

## The problem

The model is one CPU, time in quanta, and $c$ clients that are always ready. Client $i$ holds $t_i \ge 1$ tickets, and $T = \sum_i t_i$. After $n$ quanta, client $i$ has run $a_i(n)$ quanta, and its fair share is $n t_i / T$. The goal is a deterministic schedule in which the error $a_i(n) - n t_i / T$ stays small for every $n$, and in which the shares can change at run time.

## The algorithm

```pseudo id=main
STRIDE-SCHEDULE(C, n, stride1)         ▷ C: clients with tickets t_c; n quanta
L1  for each client c do s_c ← stride1 / t_c; pass_c ← 0
L2  build a min-priority queue Q of the clients, keyed by (pass_c, the join order of c)
L3  for r ← 1 to n do
L4      c ← EXTRACT-MIN(Q)
L5      run c for one quantum
L6      pass_c ← pass_c + s_c
L7      INSERT(Q, c)
```

The key of line L2 breaks ties by the order in which the clients joined, so the schedule is a function of the input. Some versions start the pass of a client at its stride; this page follows the trace in OSTEP and starts at 0. Both choices give error bounds of the same size, with the two sides of each bound swapped.

**Clients that join and leave.** The paper keeps a *global pass* that grows by $\mathit{stride1} / T$ in each quantum, which is the pass of an imagined client that holds all $T$ tickets. A client that leaves saves $\mathit{remain} = \mathit{pass}_c - \mathit{global\_pass}$. A client that joins gets $\mathit{pass}_c = \mathit{global\_pass} + \mathit{remain}$, so a new client neither takes over the CPU (as with a pass of 0) nor waits for a long time. When the tickets of a client change, its remain is scaled by the ratio of the new stride to the old stride.

## Example

This is the trace of OSTEP Chapter 9. A, B and C hold 100, 50 and 250 tickets, and $\mathit{stride1} = 10000$, so the strides are 100, 200 and 40.

| pass A | pass B | pass C | runs |
|---|---|---|---|
| 0 | 0 | 0 | A |
| 100 | 0 | 0 | B |
| 100 | 200 | 0 | C |
| 100 | 200 | 40 | C |
| 100 | 200 | 80 | C |
| 100 | 200 | 120 | A |
| 200 | 200 | 120 | C |
| 200 | 200 | 160 | C |
| 200 | 200 | 200 | A, and the cycle repeats |

In the first 8 quanta, C runs 5 times, A twice and B once, exactly in the ratio $250 : 100 : 50$. A lottery with the same tickets gives these counts only on average.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). Let $m$ be the smallest pass at the end of a quantum, and let all strides be exact rationals.

1. **The pass invariant.** At the end of each quantum, $m \le \mathit{pass}_k \le m + s_k$ for every client $k$. The client that runs has the smallest pass, and after it runs its pass is $m + s_k$; every other pass is unchanged.
2. **Pairwise error.** For any two clients $i$ and $j$ and any $n$, $-t_i \le a_i t_j - a_j t_i \le t_j$. So the error of $i$ against the pair, $a_i - (a_i + a_j) t_i / (t_i + t_j)$, lies in $[-t_i / (t_i + t_j),\ t_j / (t_i + t_j)]$, which is strictly less than one quantum in absolute value.
3. **Error against the total.** For each client, $-c\, t_i / T \le a_i(n) - n t_i / T \le 1$. So the absolute error is at most $c$ quanta for every $n$, while the error of lottery scheduling has standard deviation $\sqrt{n p (1 - p)}$.

The tests check the two bounds in integer arithmetic after every quantum, and compare the schedule with a heap-free reference that picks the smallest $a_c / t_c$.

## Complexity

Line L2 builds a [binary heap](/binary-heap/) in $O(c)$. Each quantum does one EXTRACT-MIN and one INSERT, so $n$ quanta take $O(n \log c + c)$ time. The space is $O(c)$. Join, leave and a change of tickets take $O(\log c)$ with an indexed heap (the implementation rebuilds the heap on a leave, in $O(c)$). If the passes are kept as integers, choose $\mathit{stride1}$ as a multiple of every ticket count, for example their least common multiple; otherwise use exact fractions, because rounded strides add an error that grows with $n$.

## Properties

- **Deterministic.** The schedule depends only on the tickets, the order of joins and the tie rule.
- **Bounded error.** The pairwise error is below one quantum and the error against the total is at most $c$ quanta, for every $n$, not only on average.
- **Periodic.** With fixed tickets, all passes are equal again after $T / g$ quanta, where $g$ is the greatest common divisor of the tickets, and the schedule repeats. In the example, every 8 quanta.
- **Global state.** Each client needs a pass value that is consistent with the others. This is the price of the bounded error; a lottery needs no state per client except the tickets.

## Variants and improvements

- **Hierarchical stride scheduling.** Waldspurger's thesis arranges the clients as the leaves of a binary tree and runs stride scheduling at each node. The error against the total falls from $O(c)$ to $O(\log c)$.
- **Virtual time in networks.** The same idea, with the pass as a virtual finish time, is [weighted fair queueing](/weighted-fair-queueing/); stride scheduling is close to the virtual clock and to self-clocked fair queueing. The ideal that all of them approach is [generalized processor sharing](/generalized-processor-sharing/).
- **Linux CFS.** The [Completely Fair Scheduler](/completely-fair-scheduler/) keeps a virtual runtime that grows by the run time divided by the weight, which is a pass with a stride proportional to $1 / w$, and it places a new task near the smallest virtual runtime, much like the global pass.
- **Weighted round robin.** A cycle that runs client $i$ for $t_i$ quanta in a row gives the same long-run shares, but its error inside a cycle grows with $t_i$. Stride scheduling spreads the runs out. See [weighted round robin](/weighted-round-robin/).

## When to use it

Use stride scheduling when the shares must be accurate over short times as well as long ones, for example to divide a CPU or a link between a few clients with known weights, or to give a stable rate to a media task. Use a lottery instead when clients join and leave very often and the global pass is hard to keep consistent, for example across many processors. When the clients block and wake often, use a scheduler with a global virtual time, such as CFS, which handles waking tasks by its placement rule.

## Pitfalls

- **Starting a new client at pass 0.** A client that joins late with pass 0 has the smallest pass by far, and it runs alone until it catches up. Join at the global pass, as the dynamic version does.
- **Integer division in the stride.** If $\mathit{stride1}$ is not a multiple of $t_c$, then the integer quotient at line L1 rounds the stride down, and the shares drift by a fixed fraction. Use a common multiple, or keep exact fractions.
- **Overflow of the pass.** The pass grows without bound. With fixed-width integers, compare passes by their difference, or subtract the minimum pass from all passes from time to time.
- **No tie rule.** If ties at line L4 are broken by a hash or by the heap layout, two runs of the same input can give different schedules. Put a join order in the key, as line L2 does.

## Implementations

## History

Waldspurger and Weihl introduced lottery scheduling in 1994 and gave stride scheduling, its deterministic counterpart, in an MIT technical report in June 1995. The report shows the basic pass and stride rule, the global pass for dynamic changes, and hierarchical stride scheduling. Waldspurger's PhD thesis of the same year covers both methods in full. The same virtual-time idea was found at about the same time for packet scheduling in networks, and later in the virtual runtime of the Linux CFS.

## References
