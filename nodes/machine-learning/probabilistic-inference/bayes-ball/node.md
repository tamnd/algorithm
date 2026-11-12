---
tag: FBZXXF
kind: algorithm
slug: bayes-ball
name: Bayes-Ball algorithm
aliases:
- Bayes ball
- Shachter's Bayes-Ball
area: machine-learning/probabilistic-inference
level: core
summary: "Shachter's ball-passing search in a DAG. It finds the nodes d-separated from a query set given evidence, and the tables and observations the query needs, in O(n + m) time."
solves: [d-separation-query]
model: word-ram
complexity:
  vars: {n: the number of nodes, m: the number of edges}
  time: {worst: "Θ(n + m)"}
  space: {extra: "Θ(n + m)"}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1998
  people: [Ross D. Shachter]
  note: Shachter presented Bayes-Ball at UAI 1998 as a simple linear-time way to find irrelevant nodes and requisite information in belief networks and influence diagrams.
prereqs: [d-separation, d-separation-query, breadth-first-search]
see_also: [bayesian-network, markov-blanket, variable-elimination, backdoor-criterion, conditional-independence, graph-reachability]
sources:
  - paper: "Ross D. Shachter, Bayes-Ball: the rational pastime (for determining irrelevance and requisite information in belief networks and influence diagrams), Proceedings of the 14th Conference on Uncertainty in Artificial Intelligence (UAI 1998), pages 480 to 487"
    title: Shachter 1998
    locator: the Bayes-Ball algorithm (visits from a parent and from a child, top and bottom marks), its outputs and its linear running time
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 3, Section 3.3.3 (Algorithm 3.1, the reachable set algorithm, and its correctness)"
  - paper: doi:10.1002/net.3230200504
    title: Dan Geiger, Thomas Verma and Judea Pearl, Identifying independence in Bayesian networks, Networks 20(5), 1990, pages 507 to 534
    locator: the earlier linear-time algorithm for the set of nodes d-separated from a given set
  - book: isbn:9781558604797
    title: Judea Pearl, Probabilistic Reasoning in Intelligent Systems, Morgan Kaufmann, 1988
    locator: "Chapter 3, the definition of d-separation"
---

Bayes-Ball is a graph search by Ross Shachter (1998) that answers [d-separation queries](/d-separation-query/) in a [Bayesian network](/bayesian-network/). A ball starts at the query nodes $J$ and moves along the edges by local rules that depend on whether the current node is in the evidence set $K$ and on whether the ball came from a parent or from a child. The nodes that the ball reaches through their bottom are exactly the nodes [d-connected](/d-separation/) to $J$ given $K$, and the same run also gives the conditional tables and the observations that the query $P(J \mid K)$ needs. It runs in $O(n + m)$ time on a DAG with $n$ nodes and $m$ edges.

## In plain words

Think of each variable as a room and each arrow as a pipe. You drop a ball into the rooms you ask about and let it bounce. An unobserved room passes the ball on: a ball that comes up from below can go anywhere, and a ball that comes down from above keeps going down. An observed room blocks a ball that comes from below, and bounces a ball that comes from above back up to all the rooms above it. Every room you can reach this way can still change your answer. Every other room is irrelevant. Each room keeps two flags, one for each way it can send the ball, so no room sends the ball the same way twice and the search ends quickly.

## The problem

The input is a DAG $G = (V, E)$ with adjacency lists of parents and children, a set $J$ of query nodes and a disjoint set $K$ of observed nodes. In this page $n = |V|$ and $m = |E|$; they count nodes and edges, not training examples. The main output is the set of nodes $y \notin K$ joined to $J$ by an active trail given $K$, which decides the [d-separation query](/d-separation-query/) for every $Y$ at once. Shachter also defines two by-products for the query $P(J \mid K)$:

- the *requisite probability nodes* $N_p$, the nodes whose conditional tables may be needed;
- the *requisite observation nodes* $N_e$, the observed nodes whose values may be needed.

## The algorithm

```pseudo id=main
BAYES-BALL(G, J, K)
L1  no node is visited or marked ;  Q ← the visits (j, from child) for j ∈ J
L2  while Q is not empty do
L3      remove a visit (v, from) from the front of Q ;  mark v visited
L4      if from = child and v ∉ K then
L5          if v is not marked on top then mark its top ; add (p, from child) to Q for each p ∈ Pa(v)
L6          if v is not marked on bottom then mark its bottom ; add (c, from parent) to Q for each c ∈ Ch(v)
L7      else if from = parent then
L8          if v ∈ K and v is not marked on top then mark its top ; add (p, from child) to Q for each p ∈ Pa(v)
L9          if v ∉ K and v is not marked on bottom then mark its bottom ; add (c, from parent) to Q for each c ∈ Ch(v)
L10 return the visited nodes, the top marks and the bottom marks
```

The outputs are read from the marks:

- the nodes not marked on the bottom are *irrelevant*: each of them is in $K$ or d-separated from $J$ given $K$;
- $N_p$ is the set of nodes marked on top;
- $N_e$ is the set of nodes of $K$ that were visited.

The four cases of lines L4 to L9 are the local rules of d-separation. An unobserved node reached from a child is a chain or a fork, so the ball goes on to its parents and its children. An unobserved node reached from a parent is a chain, so the ball goes on down. An observed node reached from a child blocks the ball. An observed node reached from a parent is a collider in the evidence, so the ball bounces up to all its parents. A collider with an observed descendant needs no separate rule: the ball goes down to the observed descendant, bounces, and climbs back up to the collider from a child.

## Example

Take the DAG with the edges $A \to B$, $A \to C$, $B \to D$, $C \to D$, $D \to E$, the query $J = \{B\}$ and the evidence $K = \{A, E\}$. In the queue, $X{\uparrow}$ is a visit to $X$ from a child and $X{\downarrow}$ a visit from a parent.

| step | visit | action | queue after |
|---|---|---|---|
| 1 | $B$ from child | top: send to $A$; bottom: send to $D$ | $A{\uparrow}$, $D{\downarrow}$ |
| 2 | $A$ from child | $A \in K$: blocked | $D{\downarrow}$ |
| 3 | $D$ from parent | bottom: send to $E$ | $E{\downarrow}$ |
| 4 | $E$ from parent | $E \in K$: top, bounce to $D$ | $D{\uparrow}$ |
| 5 | $D$ from child | top: send to $B$ and $C$; bottom already marked | $B{\uparrow}$, $C{\uparrow}$ |
| 6 | $B$ from child | both marks already set | $C{\uparrow}$ |
| 7 | $C$ from child | top: send to $A$; bottom: send to $D$ | $A{\uparrow}$, $D{\downarrow}$ |
| 8 | $A$ from child | $A \in K$: blocked | $D{\downarrow}$ |
| 9 | $D$ from parent | bottom already marked | empty |

The bottom marks are $\{B, C, D\}$, so $C$ and $D$ are d-connected to $B$ given $\{A, E\}$: the collider $D$ is open because its child $E$ is observed. The top marks are $N_p = \{B, C, D, E\}$, and $N_e = \{A, E\}$. With $K = \{A\}$ instead, the ball goes down from $D$ to $E$ and out of the graph, never bounces, and the bottom marks are $\{B, D, E\}$, so $B$ and $C$ are d-separated given $\{A\}$. The only top mark is then $B$: to compute $P(B \mid A)$ you need the table of $B$ and the value of $A$, and nothing else.

## Correctness

**Theorem.** A node $y \notin K$ is marked on the bottom if and only if $y \in J$ or an active trail given $K$ joins $J$ to $y$.

The proof has two steps. First, the marks only stop a node from sending the same set of balls twice, so the visits that occur are exactly the states reachable from the start visits in a fixed state graph $H$ with $2n$ states. Second, $H$ reaches the same nodes as the state graph of the reachable set algorithm of Koller and Friedman, which they prove correct: the only arc that $H$ lacks, from a collider in $\mathrm{An}(K) \setminus K$ straight up to its parents, is replaced in $H$ by the trip down to the first observed descendant and back up. The full proof is below.

Shachter also proves that $P(J \mid K)$ depends only on the tables of the nodes in $N_p$ and on the values of the nodes in $N_e$. The tests change every table outside $N_p$ at random and check that $P(J \mid K)$ stays the same, in exact rational arithmetic.

## Complexity

- **Time.** Each node gets its top mark at most once, which schedules one visit per parent, and its bottom mark at most once, which schedules one visit per child. So there are at most $|J| + 2m$ visits, each with $O(1)$ work, and the time is $O(n + m)$ in the word RAM with adjacency lists, with $\Theta(n + m)$ in the worst case.
- **Memory.** Three flags per node, and a queue that can hold $O(n + m)$ visits.
- **No preprocessing.** The reachable set algorithm first computes the ancestors of $K$. Bayes-Ball does not, because the bounce at an observed node does that work on the fly.

## Properties

- **Exact.** It decides d-separation exactly; there is no approximation and no randomness.
- **Any order of the queue.** The proof does not depend on the order in which visits leave the queue, so a stack works too. The trace above uses a first in, first out queue.
- **All targets at once.** One run gives the answer for every $Y$, like one run of [breadth-first search](/breadth-first-search/) gives every reachable vertex.
- **Uses only the graph.** The tables of the network are never read.

## Variants and improvements

- **Functional nodes.** If a node is a deterministic function of its parents, Shachter skips its bottom mark in line L6: a ball that comes from a child does not pass down through it. This finds the extra independences that come from determinism.
- **Influence diagrams.** With decision and utility nodes, the same rules find the requisite observations for a decision, which Shachter uses to simplify influence diagrams.
- **Reachable set algorithm.** Koller and Friedman's procedure keeps the same two directions as states, and handles colliders by a precomputed ancestor set. See the [d-separation query](/d-separation-query/) page.
- **Pruning for inference.** Before [variable elimination](/variable-elimination/), keep only the tables of the nodes in $N_p$ and the observed values of the nodes in $N_e$. The parents of a node in $N_p$ are in $N_p$ or in $N_e$, so the smaller model is well defined, and it gives the same $P(J \mid K)$ at a lower cost.

## When to use it

Use Bayes-Ball when you need the d-separation answer for many targets at once, or when you want to prune a network before inference, because it also returns the requisite tables. For a single yes or no answer it costs the same as the reachable set algorithm. The moral ancestral graph test is simpler to state but can add $\Theta(n^2)$ moral edges. Enumerating the paths of the [d-separation](/d-separation/) definition is only for tiny graphs and for tests.

## Pitfalls

- **One visited flag per node.** If the search stops at any node it has seen before, it loses the second direction. In the example, $D$ is first visited from a parent at step 3 and sends the ball only down. The visit from a child at step 5 is the one that reaches $C$; a search that skips it answers that $B$ and $C$ are d-separated given $\{A, E\}$, which is wrong. Keep the two marks of lines L5, L6, L8 and L9.
- **Reading the answer from the visited set.** Observed nodes are visited (the node $A$ in the example) but they are not d-connected to $J$. Read the answer from the bottom marks.
- **Passing a ball up through an observed node.** An observed node visited from a child must block the ball (line L4 tests $v \notin K$). Passing it on treats an observed chain or fork as open.
- **No bounce at an observed node.** Without line L8, a collider in $K$ or with a descendant in $K$ stays closed, and the search misses the explaining away dependence.
- **Overlapping sets.** The proof assumes that $J$ and $K$ are disjoint. A query on an observed node is trivial and should be handled before the search.

## Implementations

## History

Pearl defined d-separation in the 1980s, and Geiger, Verma and Pearl (1990) gave a linear-time algorithm for the set of nodes d-separated from a given set, as a search over legal pairs of consecutive edges. Shachter (1998) recast the search as a ball that bounces through the network, with the two marks per node, and added the requisite tables and observations for inference in belief networks and influence diagrams.

## References
