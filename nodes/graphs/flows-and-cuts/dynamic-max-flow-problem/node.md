---
tag: 5JJE0G
kind: problem
slug: dynamic-max-flow-problem
name: Dynamic maximum flow problem
aliases:
- incremental max flow
- fully dynamic maximum flow
area: graphs/flows-and-cuts
level: research
summary: Maintain a maximum flow under edge insertions, deletions, or capacity changes.
prereqs: [max-flow-problem, augmenting-path-flow, residual-graph]
see_also: [almost-linear-max-flow, ford-fulkerson, max-flow-min-cut-theorem, min-cut-problem, dynamic-connectivity, image-segmentation-graph-cuts, push-relabel]
sources:
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, third edition
    locator: Problem 26-4, Updating maximum flow (raising or lowering the capacity of one edge by 1 in O(V + E) time)
  - paper: doi:10.1145/2746539.2746609
    title: Monika Henzinger, Sebastian Krinninger, Danupon Nanongkai and Thatchaphol Saranurak, Unifying and strengthening hardness for dynamic problems via the online matrix-vector multiplication conjecture, STOC 2015
    locator: the results on dynamic s-t reachability, of which dynamic maximum flow is a generalization
  - paper: url:https://arxiv.org/abs/2203.00671
    title: Li Chen, Rasmus Kyng, Yang P. Liu, Richard Peng, Maximilian Probst Gutenberg and Sushant Sachdeva, Maximum flow and minimum-cost flow in almost-linear time, FOCS 2022
    locator: the main theorem (the recomputation baseline of m^(1+o(1)) log U time per update)
---

The dynamic maximum flow problem asks to keep the value of a [maximum flow](/max-flow-problem/), and often the flow itself or a minimum cut, while the network changes by edge insertions, deletions and capacity changes. Recomputing from scratch costs one maximum flow per update, and the question is how much of the old flow can be reused. A change of one capacity by $\delta$ changes the maximum flow value by at most $\delta$, so with integer capacities a few augmenting paths in the [residual graph](/residual-graph/) repair the flow. The fully dynamic problem with polynomially fast updates, however, is ruled out under standard conjectures, while incremental and decremental versions have almost-linear total time algorithms.

## In plain words

A network of pipes is already carrying as much water as it can, from a source to a drain. Now one pipe gets wider, a new pipe is laid, or a pipe is closed. Do you have to plan everything again? If a pipe gets wider by a little, the best total can grow by at most that little, so you look for a few new routes and add them. If a pipe is closed, you first take its water away along the routes that used it, and then look for detours. The hard question is whether this can always be done much faster than planning again from the start, after every one of a long list of changes.

## Definition

**Input.** A directed graph with $n$ vertices, a source $s$ and a sink $t \ne s$, capacities $c(e) \ge 0$, and a sequence of updates, each of which inserts an edge, deletes an edge or changes one capacity. Capacities are integers in most results, real numbers in some. Parallel and antiparallel edges are separate edges; antiparallel edges are not merged, and inserting the reverse of an existing edge adds a new edge. An undirected edge is two antiparallel arcs.

**Output.** After each update, or on request between updates, the value $F$ of a maximum s-t flow. Stronger versions also keep a maximum flow $f$, so that $f(e)$ can be read, or a minimum s-t cut.

**Kinds of update sequence.**
- *Incremental*: only insertions and capacity increases.
- *Decremental*: only deletions and capacity decreases.
- *Fully dynamic*: both.

**The basic fact.** Raising $c(e)$ by $\delta \ge 0$ raises the capacity of every cut by at most $\delta$ and lowers none, so by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) the value $F$ grows by at most $\delta$; likewise lowering $c(e)$ by $\delta$ lowers $F$ by at most $\delta$. An edge of capacity 0 is the same as no edge, so insertion and deletion are capacity changes from or to 0.

## Variants

- **Value only or flow too.** Keeping the value is easier; keeping the flow means the flow on many edges may change after one update.
- **Exact or approximate.** For undirected graphs, approximate maximum flow values under updates can be kept in subpolynomial time per update, up to subpolynomial factors in the approximation, by expander hierarchies (Goranci, Racke, Saranurak and Tan, 2021).
- **All pairs.** Keep the min cut value for every pair, for example by maintaining a [Gomory-Hu tree](/gomory-hu-tree/).
- **Changing source and sink.** Keep the flow while $s$ or $t$ moves; this is what the [Hao-Orlin algorithm](/hao-orlin/) does inside one computation, with the sink changing $n - 1$ times.
- **Flows over time.** In operations research, *dynamic flow* also means a flow over time: edges have transit times, and the goal is to send as much as possible from $s$ to $t$ by a deadline $T$. Ford and Fulkerson (1958) solved this with one min-cost flow and temporally repeated paths. That is a different problem from the one on this page.

## Examples

Take the running network $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10, with maximum flow 19 and minimum cut $\{s, c\}$ of capacity $c(s, a) + c(c, d) = 10 + 9 = 19$. Apply these updates in order.

| update | new value | why |
|---|---|---|
| raise $b t$ to 12 | 19 | the cut $\{s, c\}$ does not use $b t$; no augmenting path appears |
| raise $c d$ to 10 | 20 | the cut $\{s, c\}$ grows to 20, the capacity of $\{s\}$; one augmenting path of 1 |
| insert $a t$ with capacity 0 | 20 | a zero-capacity edge changes nothing |
| insert $d c$ with capacity 5 | 20 | an antiparallel edge to $c d$, kept separate; no cut leaving $\{s, c\}$ grows |
| delete $s a$ | 10 | only $s c$ leaves $s$; the 10 units through $s a$ are removed and no detour exists |
| lower $s c$ to 0 | 0 | no s-t path remains |

**Repairing after an increase.** Raising $c(e)$ by $\delta$ keeps the old flow feasible; with integer capacities at most $\delta$ augmenting paths are needed, each found in $O(n + m)$ time by breadth-first search, so the update costs $O(\delta (n + m))$, which is the bound of CLRS Problem 26-4 for $\delta = 1$.

**Repairing after a decrease.** Lowering $c(u, v)$ by $\delta$ to below $f(u, v)$ leaves an overflow of $k = f(u, v) - c'(u, v)$ units. Lower $f(u, v)$ by $k$, which leaves an excess of $k$ at $u$ and a deficit of $k$ at $v$. First push as much as possible from $u$ to $v$ in the residual graph; then return the rest from $u$ back to $s$ and from $t$ back to $v$, along flow paths, which lowers the value; finally look for new augmenting paths. With integer capacities this costs $O(\delta (n + m))$ too.

## Known algorithms

- **Recompute.** Run the [almost-linear algorithm](/almost-linear-max-flow/) after each update: $m^{1 + o(1)} \log U$ per update.
- **Repair by augmenting paths.** As in the examples, $O(\delta (n + m))$ per capacity change of $\delta$ with integer capacities. For unit capacities this is $O(n + m)$ per update.
- **Warm-started solvers in practice.** In computer vision, Kohli and Torr (2005) reuse the flow and the search trees of the Boykov-Kolmogorov solver when the edge weights of an [image segmentation](/image-segmentation-graph-cuts/) graph change between video frames, and report large speedups over recomputation. Push-relabel codes can be restarted from the old preflow with the labels recomputed.
- **Incremental, almost-linear total time.** Chen, Kyng, Liu, Meierhans and Probst Gutenberg (2024) give algorithms for incremental graphs, among them min-cost flow, whose total time over all insertions is almost linear; van den Brand and others (2024) give decremental counterparts.
- **Approximate fully dynamic on undirected graphs.** Expander hierarchy methods keep approximate maximum flow values with subpolynomial update time.

## Bounds

- **Per update, the trivial bounds.** $\Omega(1)$ per update, and $O(m^{1 + o(1)} \log U)$ by recomputation.
- **Conditional lower bound.** With capacity 1 on all edges, the maximum flow is positive if and only if $t$ is reachable from $s$. Henzinger, Krinninger, Nanongkai and Saranurak (2015) show, under the online matrix-vector multiplication conjecture, that fully dynamic s-t reachability has no algorithm with polynomial preprocessing whose update and query times are both polynomially smaller than the trivial ones in a precise sense, and so the same holds for dynamic maximum flow. Abboud and Vassilevska Williams (2014) gave related bounds under other conjectures.
- **Amortized over a sequence.** For incremental and decremental sequences the total time can be almost linear in the number of updates plus $m$, as listed above.

## Reductions

- **From dynamic s-t reachability**, with unit capacities, as in the lower bound.
- **To dynamic min cut.** A maximum flow certifies a minimum cut, the set of vertices reachable from $s$ in the residual graph, so keeping a maximum flow also keeps a minimum cut at an extra $O(n + m)$ per query.
- **Dynamic bipartite matching** is dynamic maximum flow on the unit-capacity network of [bipartite matching](/bipartite-matching/), so its conditional lower bounds and algorithms carry over.

## Applications

Video segmentation by graph cuts, where consecutive frames give nearly the same graph; network design and what-if analysis, where one link at a time is added or removed; sensitivity analysis of a flow model; and subroutines in algorithms that solve a sequence of related flow problems, such as parametric flow and the [Gomory-Hu algorithm](/gomory-hu-algorithm/).

## References
