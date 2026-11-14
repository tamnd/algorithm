---
tag: 60ZARY
kind: algorithm
slug: path-based-scheduling
name: Path-based scheduling
aliases:
- as fast as possible scheduling
- AFAP scheduling
- Camposano scheduling
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: Camposano's scheduler that takes every path of the control flow graph, cuts each path into the fewest states by interval covering and merges the cuts into one FSM.
solves: [resource-constrained-scheduling]
model: word-ram
complexity:
  vars: {V: the number of operations, E: the number of control flow edges, P: the number of paths, R: the number of distinct constraints}
  time: {worst: O(P V^2 log V + R (R V + E log E))}
  space: {extra: O(P V + R V)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1991
  people: [Raul Camposano]
  note: Camposano scheduled every path of the control flow graph as fast as possible and merged the paths into one controller, in IEEE TCAD in 1991, with earlier versions in 1990 at HICSS and, with Reinaldo Bergamaschi, at DAC.
prereqs: [control-data-flow-graph, activity-selection, hitting-set]
see_also: [finite-state-machine-with-datapath, operation-chaining, speculative-code-motion, sdc-scheduling, greedy-set-cover, vertex-cover, trace-scheduling, list-scheduling]
sources:
  - paper: doi:10.1109/43.62794
    title: Raul Camposano, Path-based scheduling for synthesis, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 10(1), 85 to 93, 1991
    locator: the scheduling of each path as fast as possible, the constraints as intervals on a path and the merge of all paths into one finite state machine
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 5, Schedule Optimization (scheduling with control flow)
---

Path-based scheduling, also called as fast as possible (AFAP) scheduling, schedules a design that has branches by looking at each path through its control flow graph one at a time. Raul Camposano (1991) keeps the order of the operations on a path fixed and asks only where the controller must start a new state, that is, where to cut the path. A cut is needed between two operations that share the one unit of their type, and inside every run of chained operations whose delays exceed the clock period. On one path, every such rule is an interval of possible cut positions, and the fewest cuts that meet all intervals come from a greedy scan by right ends, which is exact. A cut sits on a control flow edge that many paths may share, so the cuts of all paths must then be merged into one set of edges, and one finite state machine. This merge is a hitting set problem on subpaths, and it is [NP-hard](/np-hard/) in the model of this page. The version here merges by a greedy choice and reports the per-path optimum as a lower bound.

## In plain words

Think of each way the program can run, from start to end, as a row of tasks in a fixed order. You must split each row into clock ticks. Two tasks that need the one multiplier cannot share a tick, and a run of tasks that is too slow for one tick must be split. For one row, the fewest splits come from walking along it and splitting as late as you can each time a rule forces you. But rows share their first tasks before a branch, and one split there serves every row that passes through it. Picking the splits so that all rows are served with as few as possible is the hard part, so the method picks the split that serves the most rules, again and again.

## The problem

The control flow graph is a DAG whose nodes are operations; loops are cut at their back edges first. Each operation $v$ has a type $k(v)$ and a combinational delay $d(v) \le T$, the clock period. Some types are limited to one unit. A path is a sequence $p_0, p_1, \ldots, p_{m-1}$ from the entry to an exit, and cut position $t$ on it is the edge $(p_t, p_{t+1})$. The operations between two cuts form one state, which must

- hold at most one operation of each limited type, and
- have a total delay of at most $T$, since the operations of a path are chained in their order.

A set $H$ of cut edges is valid when every state of every path meets both rules. The goal is a valid $H$ with the fewest edges, so the controller has few states and every path runs in few cycles. Each rule becomes a constraint $[lo, hi]$ on a path, a set of consecutive positions that must hold a cut:

- for $i < j$ with $k(p_i) = k(p_j)$ limited, the interval $[i, j - 1]$;
- for each $i$, if $j$ is the least index with $d(p_i) + \cdots + d(p_j) > T$, the interval $[i, j - 1]$.

On the graph, the constraint is the set of its edges, a subpath, and $H$ is valid exactly when it meets every such subpath.

## The algorithm

```pseudo id=main
PATH-BASED-SCHEDULE(G, k, d, T)
L1  P ← every path of G from the entry to an exit
L2  for each path p in P do
L3      I_p ← the constraint intervals of p
L4      c_p ← cuts by the right end greedy on I_p: scan by right end, cut at hi when the interval holds no cut yet
L5      add the edge set of each interval of I_p to the family R
L6  order ← an empty list; U ← R
L7  while U is not empty do
L8      e ← the edge in the most sets of U, ties to the first in a fixed order
L9      append e to order; remove from U every set that holds e
L10 H ← the edges of order; for e in order, last first: drop e from H if H − {e} still meets every set of R
L11 return H, and for each p the states 1 + |c_p| alone and 1 + |H ∩ p| under H
```

Line L4 gives the fewest states that path $p$ could have on its own, a lower bound for any merge. Lines L6 to L9 are the [greedy set cover](/greedy-set-cover/) method on the dual of the [hitting set](/hitting-set/) instance: the edges are the sets and the constraints are the elements. Line L10 removes cuts that later choices made redundant. Camposano's paper merges the paths in its own way; this page does not reproduce that step.

## Example

Take $a = x \cdot y$ with delay 2, then $b = a + 1$ with delay 1, then a branch to $c = b + u$ or $d = b - u$, each with delay 1, and $T = 3$. There are two paths, $a, b, c$ and $a, b, d$. On the first, $d(a) + d(b) = 3$ fits but $d(a) + d(b) + d(c) = 4$ does not, so a cut must fall on $(a, b)$ or $(b, c)$. The second path gives the interval $\{(a, b), (b, d)\}$ in the same way, and no other run is too slow.

The right end greedy of line L4 cuts each path on its last allowed edge, $(b, c)$ and $(b, d)$. Each path then has 2 states, which is the least possible for it alone, but the union has two cut edges and the controller three states: $\{a, b\}$, then $\{c\}$ or $\{d\}$. Lines L7 to L9 see that $(a, b)$ is in both constraints and take it alone. The controller then has two states, $\{a\}$ and $\{b, c\}$ or $\{b, d\}$, where the branch is decided inside the second state, and each path still takes 2 cycles. The merge, not the per-path step, finds the shared cut.

## Correctness

What is proved, in the [full proof](proofs/correctness.md):

- **The intervals are exact.** A set of cut edges gives valid states on every path exactly when it meets every constraint of line L5.
- **One path is exact.** The right end greedy of line L4 meets every interval with the fewest cuts, by an exchange argument. So $\max_p |c_p|$ is a lower bound for the size of any valid $H$, and $1 + |c_p|$ is the fewest states path $p$ can have.
- **Valid output.** Line L9 ends only when every constraint holds an edge of the list, and line L10 drops an edge only when the rest still meets every constraint.
- **The merge is NP-hard.** Choosing the fewest edges of a DAG that meet given subpaths is NP-hard, by a reduction from [vertex cover](/vertex-cover/): each vertex $i$ becomes an edge $x_i$, each graph edge $\{i, k\}$ becomes a private connector edge from the head of $x_i$ to the tail of $x_k$, and the constraint is the subpath $x_i$, connector, $x_k$. A cut on a connector can be moved to $x_i$, so the fewest cuts equal the least vertex cover.

The greedy merge has the ratio $H_D \le \ln D + 1$ of greedy set cover, where $D$ is the largest number of constraints that one edge meets; this is proved on the [greedy set cover](/greedy-set-cover/) page and is not repeated. Measured, not proved: on 150 random graphs with at most 8 operations and if/else branches, the greedy merge used more cuts than an exhaustive search on 4, and without line L10 on 18.

## Complexity

The number of paths $P$ can grow as $2^b$ for $b$ branches in sequence, which is the main cost and the reason the method enumerates paths only of loop-free bodies. Each path has at most $V$ operations and $O(V^2)$ constraints, built in $O(V^2)$ time and stabbed in $O(V^2 \log V)$ time. The merge picks at most $R$ edges, each pick counts the edges of the open constraints in $O(R V)$ time and sorts at most $E$ candidates, and line L10 makes at most $R$ checks of $O(R V)$ each. So the time is $O(P V^2 \log V + R (R V + E \log E))$, and the space is $O(P V + R V)$ for the paths and the constraints.

## Properties

- **Fixed order.** The operations keep their order on each path. The method chooses only where states begin, which is why it is fast on one path and why it may miss a reordering that a list scheduler would find.
- **Every path is short.** Each path gets a schedule close to its own optimum, rather than the common path only.
- **Valid output, not the fewest cuts.** The merge is a heuristic in general.
- **Deterministic.** The order of paths and the tie rule of line L8 are fixed.

## Variants and improvements

- **Exact merge for small designs.** Search over subsets of edges by size, or an [integer program](/binary-integer-programming/) with one variable per edge and one covering row per constraint. The tests use the subset search as the reference.
- **Area.** Bergamaschi and Camposano also weighed the number of units and registers against the number of states.
- **Code motion first.** The fixed order is a weakness, so [speculative code motion](/speculative-code-motion/) and similar moves are often applied before the path step.
- **Several units per type.** With $a_k > 1$ units, a rule involves $a_k + 1$ operations of one type, and the constraint is still an interval: the positions between the first and the last of any $a_k + 1$ such operations in a row.

## When to use it

Use it for control-heavy designs with many short branches, where a scheduler that looks at one basic block or one trace at a time leaves cycles on the less common paths. It suits bodies with few branches in sequence, since the paths are listed one by one. For data flow with few branches, or for loops that must be pipelined, use [list scheduling](/list-scheduling/), [SDC scheduling](/sdc-scheduling/) or a modulo scheduler instead.

## Pitfalls

- **Path explosion.** With $b$ if/else blocks in sequence there are $2^b$ paths. Bound the depth or schedule regions of the body separately.
- **Right ends are not shared ends.** The per-path greedy puts cuts as late as possible, often after a branch, where no other path can use them. The example shows that merging these cuts directly gives a larger controller.
- **States are not cuts.** Two cuts on edges into the same operation may start the same state, so the number of cut edges is an upper bound on the extra states, not always their number.
- **Long operations.** An operation with $d(v) > T$ has no valid cut set. It must be spread over several cycles, which is the opposite case to chaining on the [operation chaining](/operation-chaining/) page.

## Implementations

## History

Camposano described the method at HICSS and, with Bergamaschi, at DAC in 1990, and in full in IEEE TCAD in 1991. Bergamaschi and Camposano extended it to trade area against the number of states at EURO-DAC 1991. Later work in HLS combined it with code motion over branches, since the fixed order of operations limits what it can find.

## References
