---
tag: 84BFXG
kind: algorithm
slug: static-timing-analysis
name: Static timing analysis
aliases:
- STA
- block-based timing analysis
area: cad/timing-and-verification
level: core
summary: Computes arrival times by a forward pass and required times by a backward pass over the timing graph in topological order, in linear time with no input vectors.
solves: [longest-path-problem]
model: word-ram
complexity:
  vars: {V: the number of vertices (pins) of the timing graph, E: the number of edges (cell arcs and net arcs)}
  time: {worst: Θ(V + E), average: Θ(V + E), best: Θ(V + E)}
  space: {extra: Θ(V)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1982
  people: [Robert B. Hitchcock, Gordon L. Smith, David D. Cheng]
  note: Hitchcock and his colleagues at IBM described the Timing Analysis (TA) program in 1982. It computed arrival times, required times and slacks block by block, with no simulation vectors, and was used on the IBM 3081.
prereqs: [timing-graph, arrival-and-required-time, topological-sort]
see_also: [dag-longest-path, critical-path-method, critical-path, setup-and-hold-constraints, false-path, statistical-static-timing-analysis, k-shortest-paths, kahns-algorithm]
sources:
  - paper: doi:10.1147/rd.261.0100
    title: Robert B. Hitchcock, Gordon L. Smith and David D. Cheng, Timing analysis of computer hardware, IBM Journal of Research and Development 26(1), 100 to 105, 1982
    locator: the block-oriented analysis, the arrival times, required times and slacks, and the use on the IBM 3081
  - paper: "Robert B. Hitchcock, Timing verification and the timing analysis program, Proceedings of the 19th Design Automation Conference, 594 to 604, 1982"
    locator: the TA program, the slack report and the comparison of block-oriented and path-oriented analysis
  - paper: "T. I. Kirkpatrick and N. R. Clark, PERT as an aid to logic design, IBM Journal of Research and Development 10(2), 135 to 141, 1966"
    locator: the use of PERT longest path computations on logic networks
  - book: doi:10.1007/978-0-387-93820-2
    title: J. Bhasker and Rakesh Chadha, Static Timing Analysis for Nanometer Designs, A Practical Approach, Springer, 2009
    locator: Chapter 2, STA Concepts, Chapter 8, Timing Verification, and Chapter 10, Robust Verification (common path pessimism and on-chip variation)
  - book: isbn:9789048195909
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, Springer, 1st edition, 2011
    locator: Chapter 8, Timing Closure, Section 8.2.1, Static Timing Analysis
---

Static timing analysis (STA) checks that every path of a digital circuit is fast enough, and that no path is too fast, without simulating any input vectors. It works on the [timing graph](/timing-graph/), a DAG with a vertex per pin and a delay per edge. One forward pass in [topological order](/topological-sort/) computes the latest [arrival time](/arrival-and-required-time/) at each pin, one backward pass computes the required time, and their difference is the slack, all in $\Theta(V + E)$ time. The result is exact for the graph, but it ignores the logic of the gates, so it is pessimistic when the longest path can never be excited (a [false path](/false-path/)).

## In plain words

Think of each pin as a place, and each wire or gate as a road that takes a known time. The inputs start at known times. Visit the pins so that each pin comes after all pins that feed it. At each pin, write down the latest time a signal can get there: the largest "time at the pin before it plus the time of the road". This is the arrival time.

Then go backward from the outputs, which have deadlines. At each pin, write down the latest time a signal may be there and still reach every output on time. This is the required time.

The required time minus the arrival time is the slack. A negative slack means a signal can be late. The pins with the least slack form the critical path, the one to fix first.

## The problem

The input is a timing graph $G = (V, E)$ that is a [directed acyclic graph](/directed-acyclic-graph/), a delay $d(e)$ for each edge, an arrival time $AT_0(s)$ for each start point $s$ (a vertex with no in-edge) and a required time $RT_0(t)$ for each endpoint $t$ (a vertex with no out-edge). The output is, for each vertex $v$, the arrival time $AT(v)$, the required time $RT(v)$ and the slack $RT(v) - AT(v)$ as defined on [arrival time and required time](/arrival-and-required-time/):
$$ AT(v) = \max_{P : s \leadsto v} \big(AT_0(s) + d(P)\big), \qquad RT(v) = \min_{P : v \leadsto t} \big(RT_0(t) - d(P)\big). $$
This is the [longest path problem](/longest-path-problem/) on a DAG, with many sources and given offsets, solved forward from the start points and backward from the endpoints. Each pass is the [DAG longest path](/dag-longest-path/) algorithm. In the *early* mode, used for the hold check, max and min swap places and the delays are the minimum delays.

## The algorithm

```pseudo id=main
STATIC-TIMING-ANALYSIS(G, d, AT0, RT0)
L1  order ← a topological order of G (stop with an error if G has a cycle)
L2  for each vertex v in order do
L3      if v has no in-edge then AT(v) ← AT0(v)
L4      else AT(v) ← max over edges (u, v) of AT(u) + d(u, v)
L5  for each vertex u in the reverse of order do
L6      if u has no out-edge then RT(u) ← RT0(u)
L7      else RT(u) ← min over edges (u, v) of RT(v) − d(u, v)
L8  for each vertex v do slack(v) ← RT(v) − AT(v)
L9  return AT, RT, slack
```

Line L1 can use [Kahn's algorithm](/kahns-algorithm/) or a depth-first search. In line L4 every predecessor $u$ comes before $v$ in the order, so $AT(u)$ is already known, and in line L7 every successor $v$ comes after $u$, so it has been visited first in the reverse order. The early mode takes the minimum in line L4, the maximum in line L7, and $AT(v) - RT(v)$ in line L8.

To report a *critical path*, start at an endpoint of least slack and walk back along an in-edge $(u, v)$ with $AT(u) + d(u, v) = AT(v)$ until a start point is reached. Every vertex on this path has the least slack.

## Example

Take the three-gate circuit of the [timing graph](/timing-graph/) page: inputs $a, b, c$ with $AT_0 = 0, 1, 0$, gates $G1(a, b)$, $G2(b, c)$, $G3(G1, G2)$ and the output $y$ with $RT_0(y) = 9$. The net arcs have delay 1, except $b \to G2/A$ with delay 2, and the cell arcs have delays $G1$: $A \to Y$ 3, $B \to Y$ 1; $G2$: $A \to Y$ 2, $B \to Y$ 3; $G3$: $A \to Y$ 2, $B \to Y$ 3.

The forward pass, in the order $a, b, c, G1/A, G1/B, G2/A, G2/B, G1/Y, G2/Y, G3/A, G3/B, G3/Y, y$:

| vertex | line | computation | $AT$ |
| --- | --- | --- | --- |
| $a$, $b$, $c$ | L3 | given | 0, 1, 0 |
| $G1/A$, $G1/B$ | L4 | $0 + 1$, $1 + 1$ | 1, 2 |
| $G2/A$, $G2/B$ | L4 | $1 + 2$, $0 + 1$ | 3, 1 |
| $G1/Y$ | L4 | $\max(1 + 3, 2 + 1)$ | 4 |
| $G2/Y$ | L4 | $\max(3 + 2, 1 + 3)$ | 5 |
| $G3/A$, $G3/B$ | L4 | $4 + 1$, $5 + 1$ | 5, 6 |
| $G3/Y$ | L4 | $\max(5 + 2, 6 + 3)$ | 9 |
| $y$ | L4 | $9 + 1$ | 10 |

The backward pass gives $RT(y) = 9$, $RT(G3/Y) = 8$, $RT(G3/A) = 6$, $RT(G3/B) = 5$, $RT(G1/Y) = 5$, $RT(G2/Y) = 4$, $RT(G1/A) = 2$, $RT(G1/B) = 4$, $RT(G2/A) = 2$, $RT(G2/B) = 1$, $RT(a) = 1$, $RT(c) = 0$ and $RT(b) = \min(4 - 1, 2 - 2) = 0$. The slacks are $-1$ on $b, G2/A, G2/Y, G3/B, G3/Y, y$, 0 on $c$ and $G2/B$, 1 on $a, G1/A, G1/Y, G3/A$, and 2 on $G1/B$. The output is one unit late. The backtrace from $y$ follows $G3/B$ (since $6 + 3 = 9$), $G2/Y$, $G2/A$ (since $3 + 2 = 5$) and $b$, which is the critical path $b \to G2/A \to G2/Y \to G3/B \to G3/Y \to y$ with delay 9 and path slack $9 - 1 - 9 = -1$.

In early mode with $RT_0^{e}(y) = 4$, the forward pass with minima gives $AT^{e}(y) = 7$, by the path $b \to G1/B \to G1/Y \to G3/A \to G3/Y \to y$, and the early slack $7 - 4 = 3$.

## Correctness

The [proof](proofs/correctness.md) shows the following, by induction along the topological order.

- **Arrival times.** After line L4 for $v$, $AT(v)$ is the largest value of $AT_0(s) + d(P)$ over all paths $P$ from a start point $s$ to $v$.
- **Required times.** After line L7 for $u$, $RT(u)$ is the smallest value of $RT_0(t) - d(P)$ over all paths $P$ from $u$ to an endpoint $t$.
- **Slack.** $\mathrm{slack}(v)$ is the least path slack $RT_0(t) - AT_0(s) - d(P)$ over all start-to-end paths through $v$, so the least vertex slack is the least slack over all paths.
- **Critical path.** The backtrace always finds an in-edge that sets the arrival time, and it returns a start-to-end path whose slack is the least slack.

The proof uses no sign condition on the delays. Negative delays, which appear in some models of cell arcs, are allowed.

## Complexity

- **Time.** Line L1 takes $\Theta(V + E)$ time. Lines L2 to L4 look at each edge once as an in-edge, and lines L5 to L7 once as an out-edge, so they take $\Theta(V + E)$ time with unit-cost additions and comparisons. Line L8 takes $\Theta(V)$. In total $\Theta(V + E)$ in every case, which is $O(P)$ for a netlist with $P$ pins.
- **Space.** Three numbers per vertex and the order, so $\Theta(V)$ extra space when the graph is given as in-lists and out-lists.
- **Comparison with path enumeration.** The number of start-to-end paths can grow exponentially with the depth of the circuit; a chain of $k$ reconvergent pairs of paths has $2^k$ paths. STA finds the worst slack of all of them in linear time, because the max and the min distribute over the concatenation of path prefixes and suffixes.

## Properties

- **Exact for the graph, pessimistic for the circuit.** The arrival time is the largest delay of any path in the graph. If the logic of the gates makes that path impossible to excite, the real circuit is faster. STA never reports a time that is too early, so it is safe, but it can report violations that cannot happen.
- **No input vectors.** STA does not depend on the values of the signals. This is the difference from timing simulation, which needs vectors and covers only the paths they excite.
- **Block-based.** Each vertex keeps one arrival time per mode and transition. The cost does not depend on the number of paths. A *path-based* analysis keeps paths explicitly and can apply rules per path, at a higher cost.
- **Monotone.** If a delay grows, no arrival time falls and no required time rises, so no slack grows. This is what makes incremental timing after a small change possible.

## Variants and improvements

- **Rise and fall, and unateness.** Each pin keeps a rising and a falling arrival time. A negative unate arc maps the input rising time to the output falling time, and a non-unate arc maps each input transition to both.
- **Slew propagation.** With the [nonlinear delay model](/nonlinear-delay-model/), the delay of an arc depends on the input slew. Tools propagate the worst slew together with the latest arrival time. The two can come from different in-edges, which adds pessimism; some tools propagate several candidates.
- **Early and late, and on-chip variation.** The setup check uses late data times and early capture clock times, and the hold check the opposite. Derating factors scale the delays of each mode to model variation across the chip.
- **Common path pessimism removal.** The launch and capture clock paths often share a part of the clock tree. Using a late delay on that part for one and an early delay for the other is impossible in reality, and CPPR adds the difference back to the slack.
- **Exceptions.** Designers declare false paths and multicycle paths in the constraints file (for example the SDC commands `set_false_path` and `set_multicycle_path`). The tool then removes or relaxes those paths, which needs some path tracking.
- **Path enumeration.** To report the $k$ worst paths, the tool runs a [k shortest paths](/k-shortest-paths/) style search on the DAG with the slacks as guides.
- **Incremental timing.** After a change, only the forward cone of the change needs new arrival times and only the backward cone new required times. Timing-driven optimizers call this many times.
- **Statistical timing.** [Statistical static timing analysis](/statistical-static-timing-analysis/) replaces the numbers by random variables and the max by an approximate statistical max.

## When to use it

- To sign off that a synchronous design meets its clock period and hold constraints, for every input. This is the standard method for digital chips.
- Inside optimization loops such as [gate sizing](/gate-sizing/), buffer insertion and [timing-driven placement](/timing-driven-placement/), where slacks must be recomputed after each change.
- When the circuit has no combinational loops and its timing is given by delays per arc. For a circuit with loops, latches with time borrowing, or analog behavior, other methods are needed.

## Pitfalls

- **Late arrival for the hold check.** The hold check must use the earliest arrival. Using the late times hides every hold violation; see [setup and hold constraints](/setup-and-hold-constraints/).
- **Combinational loops.** A cycle in the timing graph has no topological order. The tool must cut the loop at some arc, and the result depends on the cut.
- **Reading slack as path slack.** The slack at a vertex is the least slack of all paths through it, not the slack of one particular path.
- **False violations.** A negative slack on a false path is not a real violation. Declaring it a false path without proof is also a mistake, because then a real path may go unchecked.
- **Clock pessimism.** Without CPPR, the shared part of the clock tree counts twice and the slack is too small.

## Implementations

## History

Timing analysis by longest path began with the PERT method of project planning. Kirkpatrick and Clark (1966) at IBM applied PERT to logic design. Robert Hitchcock, Gordon Smith and David Cheng described the IBM Timing Analysis program in 1982, in the IBM Journal of Research and Development, and Hitchcock gave an account of it at the 19th Design Automation Conference the same year. TA analyzed the circuit block by block, computed arrival times, required times and slacks with no simulation, and found almost all timing problems of the IBM 3081 before hardware debugging. Since then block-based STA has been the sign-off method of digital design, extended with slews, on-chip variation, CPPR and [statistical timing](/statistical-static-timing-analysis/). Research on false paths in the late 1980s, such as the work of Du, Yen and Ghanta (1989) and of McGeer and Brayton (1989), addressed the pessimism of the purely structural analysis.

## References
