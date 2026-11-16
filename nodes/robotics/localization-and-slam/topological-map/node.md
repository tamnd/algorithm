---
tag: KYBFGV
kind: data-structure
slug: topological-map
name: Topological map
aliases:
- place graph
area: robotics/localization-and-slam
level: core
summary: A graph whose vertices are distinct places and whose edges are the paths between them, labeled with the actions that follow them, without a global metric frame.
model: word-ram
complexity:
  vars: {V: the number of places, E: the number of edges, k: the number of steps of a localization query}
  time: {add_place: O(1), add_edge: O(1) expected, step: O(1) expected, route: O((V + E) log V), localize: O(V + k V) expected}
  space: {total: O(V + E)}
history:
  year: 1991
  people: [Benjamin Kuipers, Yung-Tai Byun]
  note: Kuipers and Byun built a robot map as a graph of distinctive places joined by travel edges that the robot learns by hill climbing to a place and following a control law between places, with metric detail added on top of the graph.
prereqs: [graph, occupancy-grid-map]
see_also: [adjacency-list, dijkstra, breadth-first-search, pose-graph, slam-problem, loop-closure-detection, voronoi-diagram, global-localization]
sources:
  - paper: doi:10.1016/0921-8890(91)90014-C
    title: "Benjamin Kuipers and Yung-Tai Byun, A robot exploration and mapping strategy based on a semantic hierarchy of spatial representations, Robotics and Autonomous Systems 8(1-2), 1991, pages 47 to 63"
    locator: the distinctive places, the travel edges between them, and the topological map as the level between control and metric maps
  - paper: doi:10.1016/S0004-3702(00)00017-5
    title: "Benjamin Kuipers, The spatial semantic hierarchy, Artificial Intelligence 119(1-2), 2000, pages 191 to 233"
    locator: the control, causal, topological and metric levels, and the topological map of places, paths and regions
  - paper: "Howie Choset and Keiji Nagatani, Topological simultaneous localization and mapping (SLAM): toward exact localization without explicit localization, IEEE Transactions on Robotics and Automation 17(2), 2001, pages 125 to 137"
    locator: the generalized Voronoi graph as a topological map whose nodes are meeting points, and localization by matching the graph
---

A topological map stores the environment of a robot as a [graph](/graph/). A vertex is a place that the robot can recognize, such as a junction of corridors or a door, and an edge is a path that the robot can follow from one place to the next. An edge has a label for the action that follows it, for example "go east along the corridor", and can have a length. There is no global coordinate frame: the map says what is connected to what and how to get there, not where things are. This makes the map small and robust to errors of odometry, and it suits planning routes and talking about places. It is weak when two places look the same, which is the problem of perceptual aliasing. This page describes the structure, the operations to build it, to plan a route and to localize by a sequence of actions and observations, and their costs. Kuipers and Byun (1991) made this the central level of a robot map, and the [occupancy grid map](/occupancy-grid-map/) is its metric counterpart.

## In plain words

Think of how you give directions in a building: "from the lift, go to the end of the corridor, turn left, and it is the second door". You do not use coordinates. A topological map is the same idea for a robot. It is a list of places that the robot can recognize, and for each place the ways out of it, each leading to another place. To plan a route, the robot finds a chain of ways out from where it is to where it wants to go. If it does not know where it is, it looks at the place, makes a move, looks again, and crosses out every place on the map that does not fit what it saw.

## The abstract type

A topological map holds places and edges, with these operations:

- `add_place(σ)`: add a place with the signature $\sigma$, what the robot senses there, and return its id.
- `add_edge(u, a, v, b, ℓ)`: join the places $u$ and $v$ with an edge of length $\ell \ge 0$. The action $a$ at $u$ leads to $v$, and the action $b$ at $v$ leads back to $u$.
- `step(v, a)`: the place that the action $a$ leads to from $v$, or none.
- `route(s, t)`: a shortest route from $s$ to $t$, as a list of places and a list of actions, or none if $t$ cannot be reached.
- `localize(σ_0, [(a_1, σ_1), ..., (a_k, σ_k)])`: the set of places where the robot can be after it sensed $\sigma_0$, took the action $a_1$, sensed $\sigma_1$, and so on.

## Representation

- An array `sig` of signatures, indexed by the place id $0, \dots, V - 1$.
- An array `out` of dictionaries: `out[v][a] = (w, ℓ)` means that the action $a$ at $v$ leads to $w$ along an edge of length $\ell$. This is an [adjacency list](/adjacency-list/) keyed by the action.

**Invariant (T).** (1) For each place $v$ and each action $a$, there is at most one entry `out[v][a]`. (2) Each edge appears twice, as `out[u][a] = (v, ℓ)` and `out[v][b] = (u, ℓ)`. (3) All lengths are $\ge 0$.

Part 1 says that actions are deterministic in the map: an action at a place has at most one outcome. A real robot may fail to follow an action; the map records the intended outcome.

## Operations

```pseudo id=main
ADD-PLACE(G, σ)
L1  v ← |V|;  sig[v] ← σ;  out[v] ← an empty dictionary;  return v

ADD-EDGE(G, u, a, v, b, ℓ)                ▷ a leads from u to v, b from v to u
L2  if a is a key of out[u], or b is a key of out[v], or (u = v and a = b) then error
L3  out[u][a] ← (v, ℓ);  out[v][b] ← (u, ℓ)

ROUTE(G, s, t)                            ▷ Dijkstra on the lengths
L4  d[s] ← 0;  Q ← a min-heap with (0, s)
L5  while Q is not empty do
L6      pop (δ, u) with the smallest δ;  if δ > d[u] then continue;  if u = t then stop
L7      for each action a with out[u][a] = (w, ℓ) do
L8          if δ + ℓ < d[w] then d[w] ← δ + ℓ;  prev[w] ← (u, a);  push (d[w], w)
L9  if t was reached, follow prev from t back to s and return d[t], the places and the actions

LOCALIZE(G, σ_0, [(a_1, σ_1), ..., (a_k, σ_k)])
L10 C ← {v : sig[v] = σ_0}
L11 for i ← 1 to k do
L12     C ← {w : v ∈ C, out[v][a_i] = (w, ℓ) for some ℓ, sig[w] = σ_i}
L13 return C
```

ROUTE is [Dijkstra's algorithm](/dijkstra/) on the directed graph of the actions, with the lazy deletion of old heap entries. With unit lengths, [breadth-first search](/breadth-first-search/) gives the routes with the fewest edges. LOCALIZE keeps the set of places that agree with all observations so far; because actions are deterministic in the map, $|C|$ never grows.

## Example

The map of one floor has seven places. The signature of a place is its kind: a corner, a T junction or a dead end. The actions are the compass directions, and each edge has its length in meters.

```text
A (corner) -E 5- B (T) -E 4- C (corner)
   |S 3            |S 3         |S 3
D (T) ----E 4---- E (T) -E 4- F (corner)
   |S 2
G (dead end)
```

**Route.** From A to F, three routes reach F: A, B, C, F of length $5 + 4 + 3 = 12$, A, B, E, F of length $12$, and A, D, E, F of length $3 + 4 + 4 = 11$. ROUTE returns the places A, D, E, F with the actions S, E, E and the length 11.

**Localization.** The robot wakes up at a T junction. LOCALIZE starts with $C = \{B, D, E\}$.

| step | action | sensed | candidates |
|---|---|---|---|
| 0 | | T | {B, D, E} |
| 1 | E | corner | {C, F}: B leads east to C, a corner; D leads east to E, a T, which is out; E leads east to F, a corner |
| 2 | S | corner | {F}: C leads south to F, a corner; F has no way south |

After two moves the robot knows that it is at F, so it started at E. The reading "T" after the action N from a T junction would give $\{B\}$, and "dead end" after N would give the empty set: the observations do not fit the map, which means a sensing error or a wrong map.

**Aliasing.** Four corners joined in a square, with the actions "left" and "right", cannot be told apart: every sequence of actions leaves all four places as candidates. Only a difference in signatures or in the structure of the graph lets the robot localize.

## Correctness

ADD-PLACE and ADD-EDGE keep the invariant (T): line L2 refuses an edge that would give a second outcome to an action at a place, and line L3 writes both directions. ROUTE is Dijkstra's algorithm with nonnegative lengths, so it returns a shortest route. The [correctness proof](proofs/correctness.md) shows that LOCALIZE returns exactly the set of places $w$ such that some place $v_0$ with the signature $\sigma_0$ leads by the actions $a_1, \dots, a_k$ through places with the signatures $\sigma_1, \dots, \sigma_k$ to $w$. So the true place is always in the set when the robot senses and acts without error, and every place in the set agrees with the data. The tests compare ROUTE with the Floyd-Warshall distances and LOCALIZE with a search from every start place, on random maps.

## Complexity

The model is the [word RAM](/word-ram/), with dictionary operations in $O(1)$ expected time by hashing.

| operation | time |
|---|---|
| add_place | $O(1)$ amortized |
| add_edge, step | $O(1)$ expected |
| route | $O((V + E) \log V)$ with a binary heap |
| localize | $O(V)$ for line L10, then $O(\lvert C \rvert) \le O(V)$ expected per step, so $O(V + k V)$ |

The space is $O(V + E)$. A topological map of a building has a few hundred places where an occupancy grid of the same building has millions of cells.

## Variants

- **Metric annotations.** Store at each edge the relative pose between its ends, and at each place a small local map. This is the topological and metric hybrid of the spatial semantic hierarchy (Kuipers, 2000), and close to a [pose graph](/pose-graph/).
- **Voronoi graphs.** Take the places as the meeting points of the [Voronoi diagram](/voronoi-diagram/) of the free space, where the robot is equally far from three or more obstacles. The edges are the paths along the diagram. Choset and Nagatani (2001) built and localized in such maps.
- **Probabilistic localization.** Replace the set of candidates by a probability for each place, updated by a Bayes filter over the graph with error models for actions and signatures. This handles sensing errors that the set version cannot.
- **Regions.** Group places into rooms or zones, as a hierarchy, to plan in large buildings.

## When to use it

Use a topological map for route planning over large spaces, for tasks given in terms of places ("go to the kitchen"), and when the metric error of odometry is too large for one consistent metric map. Use an [occupancy grid map](/occupancy-grid-map/) or a pose graph when the robot needs exact positions, for example to avoid obstacles or to align scans. Most systems use both: a topological map on top of local metric maps.

## Pitfalls

- **Perceptual aliasing.** Two places with the same signature and the same neighborhood cannot be told apart. LOCALIZE then keeps both, and a mapping system that merges them builds a wrong map. Rich signatures and checks of loop closures reduce the risk.
- **Errors of sensing.** One wrong signature removes the true place from the set of LOCALIZE, and the set can become empty. Treat an empty set as a sign of an error, and use a probabilistic version if errors are common.
- **Actions that fail.** The map assumes that an action leads to its recorded place. A robot that misses a junction is somewhere else. Detect this with the signature of the place where it arrives.
- **Two edges with one label.** If two exits of a place have the same action label, the map is not deterministic and the operations above are wrong. Line L2 refuses such an edge.

## Implementations

## History

Kuipers and Byun (1991) proposed a map built on distinctive places and travel edges, learned by exploration, with metric information added only on top of the graph. Kuipers (2000) developed this into the spatial semantic hierarchy, with control, causal, topological and metric levels. Choset and Nagatani (2001) used the generalized Voronoi graph as a topological map for SLAM. Later systems combine topological graphs of places with local metric maps.

## References
