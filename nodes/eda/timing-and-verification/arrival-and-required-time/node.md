---
tag: 8XDHXD
kind: definition
slug: arrival-and-required-time
name: Arrival time and required time
aliases:
- required arrival time
- actual arrival time
area: eda/timing-and-verification
level: intro
summary: The latest time a signal settles at a pin, from the inputs forward, and the latest time it may settle, from the outputs backward. Their difference is the slack.
prereqs: [timing-graph, dag-longest-path]
see_also: [static-timing-analysis, setup-and-hold-constraints, timing-graph, false-path, critical-path-method, statistical-static-timing-analysis]
sources:
  - paper: doi:10.1147/rd.261.0100
    title: Robert B. Hitchcock, Gordon L. Smith and David D. Cheng, Timing analysis of computer hardware, IBM Journal of Research and Development 26(1), 100 to 105, 1982
    locator: the arrival times, required times and slacks that the TA program computes for each block
  - book: isbn:9789048195909
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, Springer, 1st edition, 2011
    locator: Chapter 8, Timing Closure, Section 8.2.1, Static Timing Analysis (actual arrival time, required arrival time and slack)
  - book: doi:10.1007/978-0-387-93820-2
    title: J. Bhasker and Rakesh Chadha, Static Timing Analysis for Nanometer Designs, A Practical Approach, Springer, 2009
    locator: Chapter 2, STA Concepts, and Chapter 8, Timing Verification (arrival, required time and slack in setup and hold checks)
---

The arrival time of a pin is the latest time at which the signal at that pin can settle, computed forward from the times at which the inputs settle. The required time of a pin is the latest time at which the signal there may settle so that every output and register downstream still meets its deadline, computed backward from those deadlines. The difference, required time minus arrival time, is the *slack*: a negative slack is a timing violation. These three numbers are what [static timing analysis](/static-timing-analysis/) computes for each vertex of the [timing graph](/timing-graph/). Some books call them the actual arrival time and the required arrival time.

## Definition

Let $G = (V, E)$ be a timing graph, a [directed acyclic graph](/directed-acyclic-graph/) with a delay $d(e)$ on each edge. For a path $P$ let $d(P)$ be the sum of the delays of its edges. The *start points* are the vertices with no in-edge, and each start point $s$ has a given arrival time $AT_0(s)$. The *endpoints* are the vertices with no out-edge, and each endpoint $t$ has a given required time $RT_0(t)$.

**Arrival time.** For a vertex $v$,
$$ AT(v) = \max \{\, AT_0(s) + d(P) \;:\; P \text{ a path from a start point } s \text{ to } v \,\}. $$
Every vertex of a finite DAG is reached from some start point (walk back along in-edges until none is left), so the set is not empty. Splitting each path at its last edge gives the recurrence $AT(v) = \max_{(u, v) \in E} (AT(u) + d(u, v))$ for $v$ not a start point, and $AT(s) = AT_0(s)$ for a start point. The arrival time is a [longest path](/dag-longest-path/) value.

**Required time.** For a vertex $v$,
$$ RT(v) = \min \{\, RT_0(t) - d(P) \;:\; P \text{ a path from } v \text{ to an endpoint } t \,\}, $$
with the recurrence $RT(u) = \min_{(u, v) \in E} (RT(v) - d(u, v))$, and $RT(t) = RT_0(t)$ for an endpoint. If the signal at $v$ settles by $RT(v)$, then along every path from $v$ it reaches the endpoint by its deadline, and $RT(v)$ is the latest time with this property.

**Slack.** The slack of a vertex is $\mathrm{slack}(v) = RT(v) - AT(v)$. The slack of a start-to-end path $P$ from $s$ to $t$ is $\mathrm{slack}(P) = RT_0(t) - AT_0(s) - d(P)$. Every path through $v$ is a path from a start point to $v$ followed by a path from $v$ to an endpoint, and the two parts can be chosen independently. So
$$ \mathrm{slack}(v) = \min \{\, \mathrm{slack}(P) : P \text{ a start-to-end path through } v \,\}. $$
In particular the least slack over all vertices equals the least slack over all paths. Tools report the *worst negative slack* (WNS), the least endpoint slack when it is negative, and the *total negative slack* (TNS), the sum of the negative endpoint slacks. A path whose slack equals the WNS is a *critical path*.

**Late and early times.** The definitions above are the *late* times, used for the setup check. The *early* times use the shortest delays: $AT^{e}(v)$ is the minimum of $AT_0(s) + d_{\min}(P)$, $RT^{e}(v)$ is the maximum of $RT_0^{e}(t) - d_{\min}(P)$, and the early slack is $AT^{e}(v) - RT^{e}(v)$, so that it is again negative on a violation. The early times are used for the hold check.

**Where the boundary times come from.** For a primary input, $AT_0$ is the input delay given by the designer. For a register clock pin, $AT_0$ is the time at which the clock edge reaches it. For a register data pin, $RT_0$ comes from the [setup and hold constraints](/setup-and-hold-constraints/): $c_{\text{capture}} + T - t_{\text{setup}}$ in late mode and $c_{\text{capture}} + t_{\text{hold}}$ in early mode, where $T$ is the clock period.

## Examples and non-examples

**The three-gate circuit.** Take the 13-vertex timing graph of the [timing graph](/timing-graph/) page, with $AT_0(a) = 0$, $AT_0(b) = 1$, $AT_0(c) = 0$ and $RT_0(y) = 9$.

| vertex | $a$ | $b$ | $c$ | $G1/A$ | $G1/B$ | $G1/Y$ | $G2/A$ | $G2/B$ | $G2/Y$ | $G3/A$ | $G3/B$ | $G3/Y$ | $y$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $AT$ | 0 | 1 | 0 | 1 | 2 | 4 | 3 | 1 | 5 | 5 | 6 | 9 | 10 |
| $RT$ | 1 | 0 | 0 | 2 | 4 | 5 | 2 | 1 | 4 | 6 | 5 | 8 | 9 |
| slack | 1 | $-1$ | 0 | 1 | 2 | 1 | $-1$ | 0 | $-1$ | 1 | $-1$ | $-1$ | $-1$ |

For example, $AT(G1/Y) = \max(1 + 3, 2 + 1) = 4$ and $RT(b) = \min(RT(G1/B) - 1, RT(G2/A) - 2) = \min(3, 0) = 0$. The vertices with slack $-1$ are exactly the vertices of the path $b \to G2/A \to G2/Y \to G3/B \to G3/Y \to y$, whose path slack is $9 - 1 - 9 = -1$. Two paths pass through $G1/Y$: the one from $a$, with slack $9 - 0 - 8 = 1$, and the one from $b$ through $G1/B$, with slack $9 - 1 - 6 = 2$. The vertex slack $1$ is the smaller one. The path from $c$ has delay 9 too, but it starts at time 0, so its slack is 0.

**Early times on the same graph.** With early required time $RT_0^{e}(y) = 4$, the earliest arrival at $y$ is $7$, by the path $b \to G1/B \to G1/Y \to G3/A \to G3/Y \to y$ with delay 6. The early slack is $7 - 4 = 3$, so this output meets a hold requirement of 4.

**Non-example: the time for one input vector.** The arrival time is a bound over all paths. It is not the time at which $y$ settles for a given change of the inputs. If no input change can make a signal travel along the longest path, the circuit is faster than $AT$ says. Such a path is a [false path](/false-path/).

**Non-example: slack is not a path property summed along edges.** One cannot get the slack of a path by adding the slacks of its vertices, or by taking the slack of its last vertex. In the example, $\mathrm{slack}(y) = -1$, but the path from $a$ to $y$ has slack $1$. The vertex slack is the least slack of all paths through the vertex.

## Related definitions

- **Slew.** Timing tools also carry a *slew* (transition time) at each pin, the time the signal takes to move between two thresholds, usually 10 and 90 percent or 20 and 80 percent of the supply. Arrival times are measured at the 50 percent point. The slew of the input sets the delay of the next cell in the [nonlinear delay model](/nonlinear-delay-model/).
- **Rise and fall times.** With unate cell arcs, each pin has a rising and a falling arrival time. A negative unate arc maps the rising input time to the falling output time and back.
- **Float in project scheduling.** The [critical path method](/critical-path-method/) has the earliest start, the latest start and the total float of an activity. They are the arrival time, the required time and the slack of the same longest path computation on a project network.
- **Statistical times.** In [statistical static timing analysis](/statistical-static-timing-analysis/), the delays are random variables, and so are the arrival time, the required time and the slack.
- **Setup and hold slacks.** At a register data pin the late slack is the setup slack and the early slack is the hold slack; see [setup and hold constraints](/setup-and-hold-constraints/).

## References
