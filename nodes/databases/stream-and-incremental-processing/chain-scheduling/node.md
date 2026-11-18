---
tag: XJAPP3
kind: algorithm
slug: chain-scheduling
name: Chain scheduling
aliases:
- chain operator scheduling
area: databases/stream-and-incremental-processing
level: advanced
summary: "Schedule stream operators by the slopes of the lower envelopes of their progress charts, so that tuples shrink as fast as possible and the queues between operators use little memory."
solves: [scheduling-problem]
model: word-ram
complexity:
  vars: {k: the total number of operators of all queries, n: the number of waiting tuples}
  time: {worst: "O(log k)", build: "O(k)"}
  space: {extra: "O(n + k)"}
properties: {deterministic: true, exact: true, online: true, external: false, in_place: false, recursive: false}
history:
  year: 2003
  people: [Brian Babcock, Shivnath Babu, Mayur Datar, Rajeev Motwani]
  note: "Chain was part of the STREAM project at Stanford. The journal version of 2004, with Dilys Thomas as a further author, adds Chain-Flush, a variant for latency."
prereqs: [convex-hull, greedy-algorithm, continuous-query]
see_also: [exchange-argument, single-machine-scheduling, list-scheduling, backpressure, eddies, pipelining-and-materialization, symmetric-hash-join, graham-scan]
sources:
  - paper: doi:10.1145/872757.872789
    title: "Brian Babcock, Shivnath Babu, Mayur Datar and Rajeev Motwani, Chain: operator scheduling for memory minimization in data stream systems, Proceedings of ACM SIGMOD 2003, pages 253 to 264"
    locator: "the progress chart of an operator chain, its lower envelope, the Chain rule with the earliest arrival on a tie, and the claim of the abstract that Chain is near-optimal for single-stream queries with selections, projections and foreign-key joins with stored relations (the exact form of the bound is not repeated here)"
  - paper: doi:10.1007/s00778-004-0132-6
    title: Brian Babcock, Shivnath Babu, Mayur Datar, Rajeev Motwani and Dilys Thomas, Operator scheduling in data stream systems, The VLDB Journal 13(4), 2004, pages 333 to 353
    locator: the journal version, which adds Chain-Flush for latency (general locator)
---

Chain is a rule of Babcock, Babu, Datar and Motwani (2003) for deciding which operator a data stream system runs next when tuples wait in queues between operators. Each query is a chain of operators, and each operator changes the size of a tuple, for example a filter that drops most tuples or a projection that removes columns. Chain draws the size of a tuple against the processing time it has had, takes the lower convex envelope of this *progress chart*, and always runs the waiting tuple that sits on the steepest segment of its envelope. The goal is little memory in the queues during bursts of input, and the paper claims that Chain is near-optimal for single-stream queries with selections, projections and foreign-key joins with stored relations.

## In plain words

Tuples arrive in bursts, faster than the system can process them, and they wait in queues. Each step of work makes a tuple smaller or removes it, but some steps help a lot and some help almost nothing. To keep the queues small, you should spend your time on the work that frees the most memory per unit of time. The catch is that a step that frees nothing can be the gate to a step that frees a lot. Chain looks ahead along each query: it groups such a step with the later steps that make it worth while, and it gives the whole group the average rate of the group. Then it always works on the best group, the oldest tuple first.

## The problem

A query is a chain of operators $o_1, \dots, o_k$ that every tuple of the query passes through in order. A tuple enters with size $s_0$, and after $o_j$ its size is $s_j$; a filter with selectivity $p$ turns size $s$ into the expected size $p s$, and a projection makes a tuple smaller. The output leaves the system after $o_k$, so $s_k = 0$. Operator $o_j$ takes the time $t_j$ per tuple. One processor runs one operator on one tuple at a time, and tuples arrive at times that the system does not control. The memory at a time is the total size of the tuples that wait in the system. The scheduling problem is to choose, at each step, the next operator to run so that the memory stays low at all times, and in particular at the peak of a burst.

The *progress chart* of a query is the polyline through the points $P_j = (T_j, s_j)$ with $T_0 = 0$ and $T_j = t_1 + \cdots + t_j$. Its lower envelope is its lower convex hull. The slope of a segment, with the sign changed, is the size that a tuple loses per unit of processing time on that segment.

## The algorithm

```pseudo id=main
ENVELOPE(s_0, ..., s_k; t_1, ..., t_k)      ▷ the chart of one query; T_0 = 0 and T_j = t_1 + ... + t_j
L1  i ← 0
L2  while i < k do
L3      j* ← the j > i with the largest (s_i - s_j) / (T_j - T_i); the largest such j on a tie
L4      the priority of o_{i+1}, ..., o_{j*} ← (s_i - s_{j*}) / (T_{j*} - T_i)
L5      i ← j*

CHAIN(arrivals)                              ▷ one operator step per time unit
    for each time unit do
L6      add the tuples that arrive now to the set of waiting tuples
L7      if some tuple waits then
L8          x ← the waiting tuple whose next operator has the highest priority; the oldest tuple on a tie
L9          run the next operator o_j on x; the memory falls by s_{j-1} - s_j
L10         if o_j is the last operator of its query then x leaves the system
```

The envelope depends only on the chart, so it is computed once per query, when the query is registered or when the statistics change. Lines L1 to L5 find each segment as the steepest descent from the current vertex, which is $O(k^2)$ for a chain of $k$ operators; a monotone hull scan, as in the [Graham scan](/graham-scan/), finds the same envelope in $O(k)$, because the points are already sorted by time.

In a system, the tuples that wait before an operator form a queue in arrival order, so the oldest tuple of an operator is the head of its queue. Line L8 then needs only the queue heads: keep the non-empty operator queues in a heap keyed by the priority and the arrival time of the head.

## Example

Two queries have unit-time operators. Query A has the chart $1, 1, 1/5, 0$: a first operator that keeps every tuple, such as a costly test that passes all of them, then a filter that keeps a fifth of the size, then the output. Query B has the chart $1, 2/5, 0$.

The envelope of A goes from $(0, 1)$ to $(2, 1/5)$ with slope $2/5$, because that is steeper than the slope 0 to $(1, 1)$ and the slope $1/3$ to $(3, 0)$. Then it goes on to $(3, 0)$ with slope $1/5$. So the priorities of A are $2/5, 2/5, 1/5$: the first operator frees nothing, but it shares the priority of the filter after it. The chart of B is convex, and its priorities are its drops, $3/5$ and $2/5$.

A tuple of A and a tuple of B arrive at time 0, a second tuple of B at time 1, and a second tuple of A at time 2. The table gives the memory after each step, in units of $1/5$.

| step | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| Chain | 7 | 9 | 14 | 10 | 8 | 6 | 6 | 2 | 1 | 0 |
| FIFO | 10 | 11 | 15 | 12 | 10 | 7 | 5 | 5 | 1 | 0 |
| best for this step | 7 | 9 | 12 | 10 | 8 | 6 | 4 | 2 | 1 | 0 |

At step 0, Chain runs the first tuple of B (priority $3/5$) and FIFO runs the first operator of A, which frees nothing. At step 2, all four candidates have priority $2/5$, and Chain takes the oldest, the first tuple of A, whose next step frees nothing; the step after it frees $4/5$. The last row is the least memory over all schedules for each step on its own, found by search. Chain has the lower peak (14 against 15) and the lower total (63 against 76) than FIFO here, but it is not optimal at steps 2 and 6, because the chart of A is not convex. These numbers are the output of the code on this page, so they are measurements on one input.

## Correctness

Chain is a rule, so the question is how good its schedules are. The proofs are in [the correctness proof](proofs/correctness.md), for the model of the code: one processor and operators of unit time.

- **Theorem.** Lines L1 to L5 compute the lower convex hull of the chart. Each operator gets the rate at which the hull falls over it, and the priorities do not increase along the chain.
- **Theorem.** If the chart of every query is convex, so that the drops do not increase along each chain, then Chain gives the least possible memory at every step at once, over all schedules. The proof writes the memory as the arrived size minus the total drop of the steps run so far. It relaxes the problem by dropping the order of the operators inside a chain, and shows by an [exchange argument](/exchange-argument/) that the greedy rule "the heaviest released job first" is optimal for unit jobs with release times. With convex charts, this greedy rule runs the steps in chain order, so it is Chain.
- **A counterexample** for charts that are not convex: with the charts $1, 1, 0$ and $1, 2/5, 0$ and one tuple of each at time 0, Chain has memory $7/5$ after two steps, and running query A first gives 1.

For charts that are not convex, the envelope is a heuristic in this model: it replaces a chain by the convex chart that it could follow if it ran each segment without a break. Babcock et al. prove a near-optimality result for this case in their own model. This page does not state the form of that bound, because it could not confirm it.

## Complexity

- **Per scheduling step.** With a heap of the non-empty operator queues, line L8 costs $O(\log k)$ in the worst case per step, and line L9 and the queue update cost $O(1)$, so the scheduler adds $O(\log k)$ per operator step and $O(k \log k)$ per tuple of a query with $k$ operators. These are worst-case bounds. The code on this page scans all waiting tuples, which is $O(n)$ per step and is meant for tests only.
- **The envelope.** $O(k)$ per query with a hull scan, $O(k^2)$ with lines L1 to L5, once per change of the statistics.
- **Memory.** The scheduler stores the priorities, $O(k)$, and the queues hold the $n$ waiting tuples. Chain does not change the size of a tuple; it changes how many tuples wait at each size.

## Properties

- **Deterministic** with the tie rule, and **online**: it decides each step from the tuples that have arrived.
- **Starvation.** A query with low priorities waits as long as tuples of a query with higher priorities keep arriving, so its latency can grow without bound during a long burst. This follows from the rule, and it is the reason for the latency variant below.
- **Late data.** Chain orders work by priority and arrival time, not by event time. A late tuple is ordinary work for it; the windows and the [watermarks](/event-time-watermark/) of the operators decide what a late tuple means. A long delay in a queue can make a tuple late for a downstream window, so a system that uses Chain must set its allowed lateness with the queueing delay in mind.

## Variants and improvements

- **Chain-Flush.** The journal version (2004) adds Chain-Flush, a variant that aims at low output latency. This page does not give its rule, because it could not confirm the details.
- **Operator times.** With different times $t_j$, the priority is the drop per unit of time, and the envelope uses the times on its horizontal axis. The function on this page accepts such times, but the theorem above is only for unit times.
- **Queries over several streams.** The paper's claim is for single-stream queries with selections, projections and foreign-key joins with stored relations. Joins of two streams, where one input tuple can make many output tuples, do not fit the model of a chart whose size only falls, and this page does not cover them.
- **Other schedulers.** FIFO, round robin and a greedy rule that looks only at the next operator are simpler. In the example above the greedy rule gives the memory 7, 9, 12, 10, 10, 6, 5, 5, 1, 0: a lower peak than Chain (12 against 14), because it does not run the step that frees nothing early, but a higher total (65 against 63). Neither rule is better on all inputs.

## When to use it

Use Chain when memory is the limit during bursts, the queries are chains of operators that make tuples smaller, and the system has good estimates of selectivities and costs. When the output latency matters more than memory, use Chain-Flush, FIFO, or a scheduler with deadlines. When the arrival rate stays above the processing rate, no scheduler helps, and the system needs [backpressure](/backpressure/) or load shedding.

## Pitfalls

- **Bad statistics.** The priorities come from estimated selectivities and costs. If the estimates are wrong, the schedule is wrong too, and the statistics must be watched and the envelopes recomputed.
- **Reading the slope as a greedy drop.** The priority of an operator is the slope of its envelope segment, not its own drop. An operator that frees nothing can have a high priority because of the operators after it, as in the example.
- **Breaking a segment.** The envelope assumes that the tuple goes on along its segment. If other tuples with the same priority interleave, as at step 2 of the example, the memory can rise before it falls.
- **Starvation.** Without a bound on waiting time, tuples of low-priority queries can wait for a long time.

## Implementations

This page did not confirm the details of the implementation in the papers. The Python code on this page computes the envelope with exact fractions, simulates Chain, FIFO and the greedy rule with unit operator times, and finds the least memory at each step by a search over all schedules. Its tests compare the envelope with a brute-force hull, check the theorem for convex charts against the search on random inputs, and check the counterexample.

## History

Babcock, Babu, Datar and Motwani introduced the progress chart and Chain at SIGMOD 2003, as part of the work on adaptive query processing over data streams in the STREAM project. The journal version of 2004, with Dilys Thomas, added Chain-Flush.

## References
