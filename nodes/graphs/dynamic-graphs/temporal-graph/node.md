---
tag: DQ7KTK
kind: definition
slug: temporal-graph
name: Temporal graph
aliases:
- time-varying graph
- evolving graph
area: graphs/dynamic-graphs
level: core
summary: A graph whose edges carry time labels such as presence intervals or time stamps.
prereqs: [graph, walk, reachability]
see_also: [dynamic-graph, offline-dynamic-graph, time-dependent-shortest-paths, menger-theorem, breadth-first-search, network-motif]
sources:
  - paper: doi:10.1006/jcss.2002.1829
    title: David Kempe, Jon Kleinberg and Amit Kumar, Connectivity and inference problems for temporal networks, Journal of Computer and System Sciences 64(4), 820 to 842 (2002)
    locator: Section 2 (time-respecting paths) and the section on the failure of Menger's theorem for vertex-disjoint time-respecting paths
  - paper: doi:10.1016/j.physrep.2012.03.001
    title: Petter Holme and Jari Saramäki, Temporal networks, Physics Reports 519(3), 97 to 125 (2012)
    locator: Section 2 (contact sequences, interval graphs and time-respecting paths)
  - paper: doi:10.1080/17445760.2012.668546
    title: Arnaud Casteigts, Paola Flocchini, Walter Quattrociocchi and Nicola Santoro, Time-varying graphs and dynamic networks, International Journal of Parallel, Emergent and Distributed Systems 27(5), 387 to 408 (2012)
    locator: Section 2 (the time-varying graph formalism) and Section 3 (journeys)
  - paper: "Sandeep Bhadra and Afonso Ferreira, Complexity of connected components in evolving graphs and the computation of multicast trees in dynamic networks, ADHOC-NOW 2003, Lecture Notes in Computer Science 2865, 259 to 270"
    locator: the NP-completeness of computing a largest strongly connected temporal component
---

A temporal graph is a [graph](/graph/) whose edges carry time labels: each edge exists only at certain time stamps or during certain time intervals. Paths in a temporal graph must respect time, so a message can travel along an edge only when the edge is present and only after it has arrived at the start of that edge. Unlike a [dynamic graph](/dynamic-graph/), where an algorithm sees only the present graph, a temporal graph is one object that holds the whole history, and its questions are about that history. Contact networks, transport timetables and message logs are temporal graphs.

## Definition

A **temporal graph** is a pair $\mathcal{G} = (V, \mathcal{E})$ where $V$ is a finite set of vertices and $\mathcal{E}$ is a finite set of **temporal edges** $(u, v, t)$ with $u, v \in V$ and a time stamp $t$ in a totally ordered time domain, usually $\mathbb{N}$ or $\mathbb{R}$. An edge may carry a **traversal time** $\lambda \ge 0$: it is then written $(u, v, t, \lambda)$, leaves $u$ at time $t$ and reaches $v$ at time $t + \lambda$. The edges are directed or undirected; an undirected temporal edge can be used in both directions. The **lifetime** of $\mathcal{G}$ is the range of its time stamps. The static graph with the edge set $\{\{u, v\} : (u, v, t) \in \mathcal{E}\}$ is the **underlying graph**.

Two common equivalent forms exist when the time domain is discrete.

- **Snapshot sequence.** A sequence of graphs $G_1, G_2, \ldots, G_T$ on $V$, with $(u, v, t) \in \mathcal{E}$ if and only if $\{u, v\}$ is an edge of $G_t$.
- **Interval form.** Each edge has a set of presence intervals $[a, b)$. An offline [dynamic graph](/offline-dynamic-graph/) with insertions and deletions gives exactly this form, one interval per lifetime of an edge.

A **temporal walk** (also a **journey** or a time-respecting path) from $u$ to $v$ is a sequence of temporal edges $(x_0, x_1, t_1), (x_1, x_2, t_2), \ldots, (x_{k-1}, x_k, t_k)$ with $x_0 = u$, $x_k = v$ and

$$t_{i+1} \ge t_i + \lambda_i \quad \text{for } 1 \le i < k,$$

where $\lambda_i$ is the traversal time of the $i$-th edge. With $\lambda = 0$ and non-decreasing times the walk is **non-strict**; with the condition $t_{i+1} > t_i$ it is **strict**. It is a temporal path if the $x_i$ are distinct. Vertex $v$ is **temporally reachable** from $u$ if a temporal walk from $u$ to $v$ exists. The usual measures of a journey are its arrival time $t_k + \lambda_k$, its departure time $t_1$, its duration and its number of edges; they give the **earliest-arrival**, **latest-departure**, **fastest** and **shortest** journeys.

Temporal reachability is reflexive but **not transitive**: from $u \leadsto v$ and $v \leadsto w$ it does not follow that $u \leadsto w$, because the journey from $v$ may leave before the journey from $u$ arrives.

## Examples and non-examples

**Example: earliest arrival.** Take $V = \{a, b, c, d, e\}$ and the undirected temporal edges $(a,b,1)$, $(c,d,1)$, $(b,c,2)$, $(d,e,3)$, $(c,e,4)$, $(a,d,5)$, $(b,e,6)$, with strict journeys that start at $a$ at time 0. Scanning the edges in time order and using an edge when one end has already been reached at an earlier time gives these earliest arrival times.

| vertex | $a$ | $b$ | $c$ | $d$ | $e$ |
|---|---|---|---|---|---|
| earliest arrival | 0 | 1 | 2 | 5 | 4 |
| hops in the underlying graph | 0 | 1 | 2 | 1 | 2 |

The vertex $d$ is a neighbor of $a$ in the underlying graph, but the journey $a, b, c, d$ is not allowed: the edge $(c, d, 1)$ is present before $c$ is reached at time 2. So $d$ waits for the direct edge at time 5. The scan of the sorted edge list takes $O(|\mathcal{E}|)$ time after sorting, which is the standard method for earliest arrival from one source.

**Example: no transitivity.** Take $(x, y, 2)$ and $(y, z, 1)$. Then $y$ is reachable from $x$ (at time 2) and $z$ is reachable from $y$ (at time 1), but $z$ is not reachable from $x$: when the message reaches $y$, the edge to $z$ is gone. In a static graph, reachability is always transitive.

**Example: Menger's theorem fails.** Kempe, Kleinberg and Kumar (2002) showed that in temporal graphs the largest number of vertex-disjoint time-respecting paths from $u$ to $v$ can be smaller than the smallest number of vertices whose removal destroys all such paths. So the static [Menger theorem](/menger-theorem/) does not carry over.

**Example: hard components.** In a static graph, [connected components](/connected-components/) take linear time. A set of vertices in which every pair is temporally reachable in both directions is a temporal analogue, and Bhadra and Ferreira (2003) proved that finding a largest such set is NP-complete.

**Non-example: a dynamic graph.** A [dynamic graph](/dynamic-graph/) algorithm receives updates one by one and answers questions about the current graph only. It is not asked about journeys that cross several time steps.

**Non-example: a weighted graph.** A graph whose edges carry lengths that happen to be called "times", such as a road graph with travel times, is a static [weighted graph](/weighted-graph/). Its paths have no departure constraints. A road graph whose travel times depend on the departure time is a time-dependent graph; see [time-dependent shortest paths](/time-dependent-shortest-paths/).

## Related definitions

- **[Dynamic graph](/dynamic-graph/) and [offline dynamic graph](/offline-dynamic-graph/).** An offline update sequence is a temporal graph in interval form, but offline dynamic algorithms answer questions about single moments, not about journeys.
- **Time-expanded graph.** Make a copy $(v, t)$ of each vertex for each relevant time, add waiting arcs $(v, t) \to (v, t')$ for consecutive times $t < t'$, and an arc $(u, t) \to (v, t + \lambda)$ for each temporal edge. Journeys become ordinary directed paths, so [breadth-first search](/breadth-first-search/) and other static algorithms apply, at the cost of a larger graph.
- **[Time-dependent shortest paths](/time-dependent-shortest-paths/).** Edge travel times are functions of the departure time, a continuous form of the same idea used in route planning.
- **Temporal motifs.** Small patterns of temporal edges in a fixed time order, the temporal form of [network motifs](/network-motif/).

## References
