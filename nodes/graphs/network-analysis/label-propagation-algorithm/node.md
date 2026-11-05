---
tag: GKHM2A
kind: algorithm
slug: label-propagation-algorithm
name: Label propagation algorithm
aliases:
- LPA
area: graphs/network-analysis
level: core
summary: Nodes repeatedly adopt the majority label among their neighbours until stable.
solves: [community-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {expected: O(m (n + m)), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: false, recursive: false}
history:
  year: 2007
  people: [Usha Nandini Raghavan, Réka Albert, Soundar Kumara]
  note: Published in Physical Review E as a near-linear-time method for community detection.
prereqs: [community-detection, graph, degree]
see_also: [louvain-method, leiden-algorithm, girvan-newman-algorithm, modularity, infomap, connected-components]
sources:
  - paper: doi:10.1103/PhysRevE.76.036106
    title: Usha Nandini Raghavan, Réka Albert and Soundar Kumara, Near linear time algorithm to detect community structures in large-scale networks, Physical Review E 76, 036106 (2007)
    locator: the algorithm (initial unique labels, asynchronous updates in random order, random tie breaking, the stopping rule), the oscillation of synchronous updates, and the aggregation of several runs
  - paper: doi:10.1103/PhysRevE.80.026129
    title: Michael J. Barber and John W. Clark, Detecting network communities by propagating labels under constraints, Physical Review E 80, 026129 (2009)
    locator: label propagation as a search for a local maximum of the number of edges inside communities, and the modularity-constrained variant LPAm
  - paper: doi:10.1103/PhysRevE.79.066107
    title: Ian X. Y. Leung, Pan Hui, Pietro Liò and Jon Crowcroft, Towards real-time community detection in large networks, Physical Review E 79, 066107 (2009)
    locator: the tendency to form one very large community, and the hop attenuation and node preference variants
  - paper: doi:10.1016/j.physrep.2009.11.002
    title: Santo Fortunato, Community detection in graphs, Physics Reports 486(3-5), 75 to 174 (2010)
    locator: the section on alternative methods that describes label propagation and its cost
---

The label propagation algorithm finds [communities](/community-detection/) by local voting. Every vertex starts with its own label. In rounds, the vertices are visited in random order, and each vertex takes the label that most of its neighbours carry, breaking ties at random. The process stops when every vertex has a label that is most frequent among its neighbours, and the groups of vertices with equal labels are the communities. Each round costs $O(n + m)$ time, and on real networks a few rounds are enough, which makes it one of the fastest community detection methods. It optimizes no global objective, and its result changes from run to run.

## In plain words

Think of a crowd where each person starts with a different flag. Again and again, each person looks at the flags of their friends and switches to the flag that most of them hold. If there is a draw, they pick one of the leaders at random.

Inside a tight group, one flag soon wins, because the members mostly look at each other. Between groups there are few friendships, so a flag has a hard time crossing over. The game ends when nobody wants to switch. Each flag that is left marks one community.

## The problem

The input is an undirected, unweighted graph $G = (V, E)$ with $n$ vertices and $m$ edges. It may be disconnected, and it may have isolated vertices. The output is a partition of $V$ into communities, the classes of a labelling $\ell : V \to V$. A labelling is *stable* when, for every vertex $v$ with at least one neighbour, the number of neighbours with label $\ell(v)$ is the largest count of any label among the neighbours of $v$. Label propagation returns a stable labelling. It is a heuristic for [community detection](/community-detection/): it does not maximize [modularity](/modularity/) or any other stated score.

## The algorithm

```pseudo id=main
LABEL-PROPAGATION(G, random source)
L1  for each vertex v do label[v] ← v
L2  repeat
L3      changed ← false
L4      for each vertex v, in a new uniform random order do
L5          count[x] ← the number of neighbours of v with label x, for each label x among them
L6          if v has a neighbour and count[label[v]] < max over x of count[x] then
L7              label[v] ← a uniform random choice among the labels x with maximum count[x]
L8              changed ← true
L9  until not changed
L10 return the classes of vertices with equal label
```

The updates are asynchronous: line L5 sees the labels that earlier vertices of the same round have just set. Raghavan, Albert and Kumara show why this matters: with synchronous updates, where all vertices use the labels of the previous round, the labels on a bipartite part of the graph can swap sides forever.

Line L6 keeps the current label when it is already among the most frequent. In the paper, a vertex picks uniformly among the most frequent labels even when its own label is one of them, and the run stops when every vertex holds a most frequent label. Both rules stop at exactly the stable labellings. The rule of line L6 makes every change strictly useful, which gives the bound on the number of rounds below.

**Ties, isolated vertices and disconnected graphs.** Ties between labels are broken at random in line L7. An isolated vertex has no neighbour, never changes, and forms a community alone. Labels never cross between [connected components](/connected-components/), so every community lies inside one component. A class of equal labels can still be disconnected inside a component, when two distant parts adopt the same label; many implementations split each class into its connected parts after line L10.

**Directed and weighted graphs.** The method ignores directions. With edge weights, line L5 sums the weights of the neighbours with each label instead of counting them.

## Example

Take the vertices 0 to 6 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$. Fix the visit order $6, 5, 4, 3, 2, 1, 0$, and, for a reproducible trace, break ties by the smallest label instead of at random. The counts list the labels of the neighbours at the moment of the visit.

| round | vertex | counts of neighbour labels | old label | new label |
|---|---|---|---|---|
| 1 | 6 | 4: 1, 5: 1 | 6 | 4 |
| 1 | 5 | 4: 2 | 5 | 4 |
| 1 | 4 | 3: 1, 4: 2 | 4 | 4, kept |
| 1 | 3 | 1: 1, 2: 1, 4: 1 | 3 | 1 |
| 1 | 2 | 0: 1, 1: 2 | 2 | 1 |
| 1 | 1 | 0: 1, 1: 2 | 1 | 1, kept |
| 1 | 0 | 1: 2 | 0 | 1 |
| 2 | all | | | no change |

The result is $\{0, 1, 2, 3\}$ with label 1 and $\{4, 5, 6\}$ with label 4, the partition of largest modularity of this graph. With the order $0, 1, \ldots, 6$ and the same tie rule, vertex 0 takes label 1 and the label 1 then spreads through vertex 3 to vertex 4 before the triangle $\{4, 5, 6\}$ agrees on its own label; the run ends with a single community. The order matters, which is why the method uses a new random order in every round.

## Correctness

Call an edge *agreeing* when its two ends have the same label, and let $\Phi$ be the number of agreeing edges. When line L7 changes the label of $v$ from $a$ to $b$, only the edges at $v$ change status: $\mathrm{count}[a]$ of them stop agreeing and $\mathrm{count}[b]$ start, and line L6 guarantees $\mathrm{count}[b] > \mathrm{count}[a]$. So $\Phi$ grows by at least 1 with every change. Since $0 \le \Phi \le m$, there are at most $m$ changes in the whole run, so at most $m$ rounds make a change, and the loop stops after at most $m + 1$ rounds. When it stops, a full round made no change, so line L6 failed at every vertex with neighbours, which means the labelling is stable. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **One round.** Counting the labels of the neighbours with a hash map, and a random permutation, take $O(n + \deg(v))$ in total over $v$, so $O(n + m)$ expected time per round.
- **Number of rounds.** By the argument above, at most $m + 1$ rounds, so the worst case is $O(m(n + m))$ expected time. In practice the number of rounds is small and grows slowly with $n$; Raghavan, Albert and Kumara report that most vertices are labelled after a few rounds, and call the method near linear.
- **Best case.** A graph that is already stable at the start, such as a graph with no edges, stops after one round, $\Theta(n + m)$.
- **Space.** The labels and a counter take $\Theta(n)$ words besides the graph.
- **Parallel form.** The work of a round splits over the vertices. Synchronous rounds parallelize best but can oscillate; colouring the graph and updating one colour class at a time, the semi-synchronous scheme, avoids the swaps.

## Properties

- **Randomized.** Different runs can return different partitions. Raghavan, Albert and Kumara combine several runs by intersecting their partitions.
- **No objective.** Barber and Clark show that the stable labellings are the local maxima of the number of agreeing edges, under single-vertex changes. The global maximum of that number is the useless labelling with one label for each component.
- **Local.** Each step reads only the labels of the neighbours, so the method runs on streaming and distributed graph systems.
- **No parameters.** It needs no number of communities and no resolution.
- **Respects components.** Communities never span two components of $G$.

## Variants and improvements

- **Modularity-constrained propagation (LPAm).** Barber and Clark add a penalty term so that each update increases modularity, which avoids the single giant community.
- **Hop attenuation and node preference.** Leung and co-authors let a label lose weight as it travels from its origin, and weight neighbours by degree, to stop one label from flooding the graph.
- **Semi-synchronous updates.** Update the classes of a proper colouring one after the other: as fast as synchronous rounds, but without oscillation.
- **Seeded labels.** Fix the labels of a few vertices and propagate the rest; this is semi-supervised classification on graphs.
- **Overlapping communities.** Let each vertex keep several labels with weights, as in the COPRA and SLPA methods.

## When to use it

Use it as a fast first look at the communities of a very large graph, where even the [Louvain method](/louvain-method/) is too slow, or in a vertex-centric distributed system. Run it several times and compare, since one run can be misleading. When the quality of the partition matters more than speed, or a stable answer is needed, use the [Leiden algorithm](/leiden-algorithm/) or the Louvain method, which optimize [modularity](/modularity/), or [Infomap](/infomap/).

## Pitfalls

- **One giant community.** On graphs with weak community structure, or with an unlucky order, one label can spread over everything, as the second order in the example shows.
- **Synchronous updates.** Computing all new labels from the old ones can oscillate forever on bipartite parts, for example on a single edge, where the two ends swap their labels in every round.
- **Counting the vertex itself.** The original method counts only the neighbours. Counting $v$ itself in line L5 changes the stable states and is a different algorithm.
- **Fixed tie rule.** Breaking ties by the smallest label in every run removes the randomness that helps the method find different structures, and favours small labels everywhere.
- **Disconnected label classes.** Two parts of a component can end with the same label without being joined; split the classes into connected parts when communities must be connected.

## Implementations

## History

Usha Nandini Raghavan, Réka Albert and Soundar Kumara published the method in 2007 as a near-linear-time alternative to methods based on modularity or betweenness. Barber and Clark in 2009 linked it to the maximization of agreeing edges and to modularity, and Leung, Hui, Liò and Crowcroft studied its use on large networks and its tendency to form one large community. Its simplicity made it a standard routine in graph libraries and in vertex-centric distributed systems.

## References
