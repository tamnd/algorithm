---
tag: Q08Q0Y
kind: algorithm
slug: differential-dataflow
name: Differential dataflow
aliases:
- differential computation
area: databases/stream-and-incremental-processing
level: research
summary: "Incremental computation for iterative dataflow programs that keeps differences indexed by a partial order of versions and iterations."
solves: [view-maintenance]
model: word-ram
complexity:
  vars: {d: the number of differences that one epoch adds to all traces, n: the number of differences stored in all traces}
  time: {worst: "O(d n)", average: "O(d log n)", best: "O(d)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: true, online: true, external: false, in_place: false, recursive: false}
history:
  year: 2013
  people: [Frank McSherry, Derek G. Murray, Rebecca Isaacs, Michael Isard]
  note: "McSherry, Murray, Isaacs and Isard described differential computation at CIDR 2013, and it ran on the Naiad system of timely dataflow."
prereqs: [delta-rules, semi-naive-evaluation]
see_also: [timely-dataflow, dbsp, delta-rules, higher-order-ivm, semi-naive-evaluation, incremental-view-maintenance, connected-components, breadth-first-search]
sources:
  - paper: "Frank McSherry, Derek G. Murray, Rebecca Isaacs and Michael Isard, Differential dataflow, Proceedings of the Conference on Innovative Data Systems Research (CIDR), 2013"
    title: Differential dataflow
    locator: "the versions and iterations as a lattice, the differences indexed by its elements, the incremental operators and the loop with its feedback, and the experiments on graph computations (general locator)"
  - paper: "Derek G. Murray, Frank McSherry, Rebecca Isaacs, Michael Isard, Paul Barham and Martín Abadi, Naiad, a timely dataflow system, Proceedings of ACM SOSP 2013"
    title: "Naiad: a timely dataflow system"
    locator: "the timely dataflow runtime on which differential dataflow ran, with timestamps of an epoch and loop counters (the page numbers are not checked here)"
  - paper: doi:10.14778/3587136.3587137
    title: "Mihai Budiu, Tej Chajed, Frank McSherry, Leonid Ryzhyk and Val Tannen, DBSP: automatic incremental view maintenance for rich query languages, PVLDB 16(7), 2023, pages 1601 to 1614"
    locator: "Section 6, nested streams, which give the same two dimensions of time with one total order per level"
---

Differential dataflow is an algorithm for incremental computation of dataflow programs with loops, in which each collection is stored as *differences*, signed changes indexed by times that form a partial order, such as pairs of an input epoch and a loop iteration. A change to the input at a later epoch then reuses the work of every earlier epoch at the same iteration, so a small input change causes a small amount of work even inside an iteration. [Incremental view maintenance](/incremental-view-maintenance/) and [delta rules](/delta-rules/) handle one dimension of change, and [semi-naive evaluation](/semi-naive-evaluation/) handles only the iterations of one fixed input, while differential dataflow handles both at once. [DBSP](/dbsp/) restates the idea with nested streams in place of a partial order, and [timely dataflow](/timely-dataflow/) is the runtime model that it was built on.

## In plain words

Think of a computation that repeats a step until nothing changes, such as finding every place you can reach from a start point. Now the map changes a little, and you want the new answer.

Starting again from zero repeats almost all of the old work. Keeping only the old final answer is not enough, because the new run would redo the old steps.

So you keep, for each step of the old run, only what changed at that step. For the new run you record, for each step, only how it differs from the same step of the old run. Most of those records are empty, so most of the work is skipped. Each stored change is labeled with two numbers, the version of the input and the step, and a result is the sum of all labeled changes that are not later in either number.

## The problem

The input is a sequence of epochs. Each epoch $e$ brings a change to the input collections: here a set of roots and a bag of directed edges $(a, b)$. The program is an iterative dataflow: here graph reachability,

$$R_{e,0} = \mathrm{distinct}(\mathit{roots}_e), \qquad R_{e,i+1} = \mathrm{distinct}\big(\mathit{roots}_e + \mathrm{dst}(R_{e,i} \bowtie \mathit{edges}_e)\big),$$

where $\mathrm{dst}$ keeps the target of each joined edge. After each epoch the output is $R_{e,i}$ for every $i$, and in particular its limit, the set of nodes reachable from the roots, which [breadth-first search](/breadth-first-search/) also computes. A collection is a Z-set, a bag with integer weights. A set is a Z-set with weights 0 and 1, and distinct maps a Z-set to a set.

## The algorithm

Times are pairs $t = (e, i)$ with the product order: $(e_1, i_1) \le (e_2, i_2)$ when $e_1 \le e_2$ and $i_1 \le i_2$. This is a partial order: $(0, 3)$ and $(1, 2)$ are not comparable. Every two times have a least upper bound $s \vee u$, the pair of the maxima. A *trace* $X$ maps times to signed bags, and the collection at $t$ is the sum of $X[s]$ over all $s \le t$. By Möbius inversion on this order the difference at $t$ is unique: $X[e, i]$ is the collection at $(e, i)$ minus the collections at $(e - 1, i)$ and $(e, i - 1)$, plus the collection at $(e - 1, i - 1)$.

The dataflow has the inputs *roots* and *edges*, a feedback edge *fed* that holds R one iteration later, a join, a union and a distinct. An epoch is processed one iteration at a time.

```pseudo id=main
ADVANCE(e, Δroots, Δedges)
L1  roots[(e, 0)] ← Δroots;  edges[(e, 0)] ← Δedges        ▷ input changes enter at iteration 0
L2  for i ← 0, 1, 2, ... while i ≤ i_max or R[(e, i - 1)] ≠ 0 do      ▷ i_max: the largest iteration stored
        t ← (e, i)
L3      if i > 0 then fed[t] ← R[(e, i - 1)]                 ▷ the feedback edge adds 1 to the iteration
L4      J[t] ← the sum over all s, u with s ∨ u = t of dst(fed[s] ⋈ edges[u])
L5      U[t] ← roots[t] + J[t]
L6      if U[t] ≠ 0 then C ← C ∪ {t} ∪ {t ∨ c : c ∈ C}      ▷ the closure of the times at which U changes
L7      if t ∈ C then
L8          R[t] ← distinct(the collection U at t) - (the sum of R[s] over s ≤ t, s ≠ t)
```

Line L4 is the differential join. The join is bilinear, so the join of the collections at $t$ is the sum of the joins of all pairs of differences at times $s, u \le t$, and a pair contributes from time $s \vee u$ on. Line L8 is the differential version of a nonlinear operator: it compares the new output with the accumulated old output. Lines L6 and L7 evaluate it only at the times in the closure of its input times under $\vee$. At any other time its output difference is 0, so most times cost nothing. A real system keeps each trace as an *arrangement*, indexed by key, so that line L4 finds the matching differences by a lookup, and runs the dataflow on [timely dataflow](/timely-dataflow/), which tells each operator when a time is complete.

## Example

Epoch 0 has the root 1 and the edges $1 \to 2$ and $2 \to 3$. Epoch 1 removes $1 \to 2$ and adds $1 \to 3$ and $3 \to 4$. The differences of R are:

| time | difference of R | R at this time |
|---|---|---|
| $(0, 0)$ | $1$ +1 | $\{1\}$ |
| $(0, 1)$ | $2$ +1 | $\{1, 2\}$ |
| $(0, 2)$ | $3$ +1 | $\{1, 2, 3\}$ |
| $(1, 0)$ | none | $\{1\}$ |
| $(1, 1)$ | $3$ +1, $2$ -1 | $\{1, 3\}$ |
| $(1, 2)$ | $3$ -1, $4$ +1 | $\{1, 3, 4\}$ |

R at $(1, 1)$ is the sum of the differences at $(0, 0)$, $(0, 1)$, $(1, 0)$ and $(1, 1)$, which gives $\{1, 3\}$. The difference at $(1, 2)$ removes the 3 that epoch 0 found at iteration 2, since epoch 1 found it at iteration 1. Distinct was evaluated 5 times in all, at the 5 times of the closure. In a second example, a path $0 \to 1 \to \cdots \to 20$ is computed in epoch 0, and epoch 1 adds the edge $20 \to 21$. The only difference of epoch 1 is $21$ +1 at time $(1, 21)$, and distinct runs once.

## Correctness

The proof is by induction over the times in the order epoch first, then iteration, which lists every smaller time first. The input traces accumulate to the inputs of each epoch at every iteration, because their changes enter at iteration 0. The feedback trace accumulates at $(e, i)$ to R at $(e, i - 1)$. The join trace accumulates to the join of the accumulated inputs, because the join is bilinear and $s, u \le t$ holds exactly when $s \vee u \le t$. For distinct, line L8 computes the unique difference, and a short argument on the four terms of the Möbius formula shows that the difference of any function of $U$ is 0 outside the closure of the times of $U$. The loop of line L2 can stop once the iteration is past every stored iteration and R did not change at the last one. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

The costs are per epoch, in the [word RAM](/word-ram/) model, with $d$ the number of differences that the epoch adds to all traces and $n$ the number of differences stored.

- **Time.** With arrangements sorted or hashed by key, each new difference at an operator input is matched with the differences of the same key in the other trace, which costs $O(\log n)$ per lookup in a sorted index, or expected $O(1)$ in a hash index, plus the number of matches. So an epoch costs about $O(d \log n)$ when each key has few differences. In the worst case one key holds all $n$ differences and the cost is $O(d n)$. These bounds are per epoch, not amortized, and they count the differences, not the size of the collections.
- **Memory.** Every difference of every trace is kept, $O(n)$. Systems compact the traces: once no future time can tell two times apart, their differences are added together. This is safe for times below the frontier of [timely dataflow](/timely-dataflow/).
- **Nonlinear operators.** For each key, distinct and other nonlinear operators are evaluated at the times of the closure of that key's input times, which can be much larger than the number of input times.

## Properties

- **Exact.** The accumulated collections at every time equal the iterates of the program.
- **Incremental in both dimensions.** A change at a later epoch reuses all work of earlier epochs at every iteration, and inside an epoch only the changed differences are processed.
- **Late data.** The epochs are logical. A record that arrives after its epoch has been processed is entered in the current epoch, and the outputs of that epoch and later ones include it. To place records by event time, the input keeps an epoch open until the frontier of timely dataflow, or a watermark, says that it is complete.
- **Deterministic.** The differences do not depend on the order in which the operators run, only on the times.

## Variants and improvements

- **Arrangements.** Indexed traces shared by many operators and queries, so that a collection is indexed once and read by every join that needs it.
- **Compaction.** Times that are no longer distinguishable, because the frontier has passed them, are merged, which keeps memory bounded for long-running inputs.
- **Other lattices.** Any lattice of times works. Nested loops give longer tuples of iteration counters, and the times can be ordered by event time and processing time.
- **Nested streams.** [DBSP](/dbsp/) keeps the two dimensions as a stream of streams, with a total order on each level, and proves the same rules with simpler algebra.
- **Other operators.** Grouping and aggregation, top-k, and [connected components](/connected-components/) by label propagation follow the pattern of distinct: compute the output at the closure times, and subtract the accumulated old output.

## When to use it

Use it for iterative computations, such as graph reachability, connected components, shortest paths and recursive Datalog queries, over inputs that change in small steps, when each new answer is needed quickly. Prefer recomputation when most of the input changes at each epoch, and semi-naive evaluation when the input never changes.

## Pitfalls

- **Total order of times.** Indexing the differences by a total order, such as epoch first, loses the reuse: the difference at $(1, 2)$ would be taken against $(1, 1)$ only, and every iteration of epoch 1 would redo work. The product order is what lets $(1, 2)$ reuse $(0, 2)$.
- **Missing closure times.** Evaluating distinct only at the times at which its input changes is wrong. For example, a difference at $(0, 3)$ and one at $(1, 0)$ can change the output at $(1, 3)$, where the input has no difference.
- **Memory growth.** Without compaction, the traces keep every difference of every epoch.
- **Many closure times.** A key with differences at many incomparable times can have a closure of size quadratic in their number, which makes nonlinear operators slow.

## Implementations

## History

McSherry, Murray, Isaacs and Isard (2013) introduced differential dataflow at CIDR, with times that combine input versions and loop iterations in a lattice and differences indexed by them, and showed experiments on iterative graph computations over changing inputs. It ran on Naiad, the timely dataflow system of Murray, McSherry, Isaacs, Isard, Barham and Abadi (2013). Later work by McSherry and others added shared arrangements, and Budiu, Chajed, McSherry, Ryzhyk and Tannen gave [DBSP](/dbsp/) (2023), which restates the theory with nested streams.

## References
