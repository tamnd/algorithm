---
tag: PBR52S
kind: problem
slug: constrained-clustering
name: Constrained clustering
aliases:
- must-link and cannot-link clustering
- clustering with instance-level constraints
area: machine-learning/clustering
level: advanced
summary: Clustering subject to pairwise must-link and cannot-link constraints.
prereqs: [clustering-problem, transitive-closure, graph-coloring]
see_also: [cop-k-means, k-means-problem, k-coloring, disjoint-set, bipartiteness-testing, connected-components, np-complete, hard-and-soft-clustering]
sources:
  - paper: "K. Wagstaff and C. Cardie, Clustering with instance-level constraints, Proceedings of ICML 2000, pp. 1103-1110"
    title: Wagstaff and Cardie 2000
    locator: must-link and cannot-link constraints, their transitive consequences, and constrained COBWEB
  - paper: "K. Wagstaff, C. Cardie, S. Rogers and S. Schrödl, Constrained k-means clustering with background knowledge, Proceedings of ICML 2001, pp. 577-584"
    title: Wagstaff et al. 2001
    locator: the COP-KMEANS algorithm and the lane-finding application
  - paper: "I. Davidson and S. S. Ravi, Clustering with constraints: feasibility issues and the k-means algorithm, Proceedings of the 2005 SIAM International Conference on Data Mining (SDM), pp. 138-149"
    title: Davidson and Ravi 2005
    locator: the feasibility problem for must-link, cannot-link, δ and ε constraints; cannot-link feasibility is NP-complete, must-link feasibility is polynomial
  - paper: "S. Basu, A. Banerjee and R. J. Mooney, Active semi-supervision for pairwise constrained clustering, Proceedings of the 2004 SIAM International Conference on Data Mining (SDM), pp. 333-344"
    title: Basu, Banerjee and Mooney 2004
    locator: PCKMeans, soft pairwise constraints with penalties, and active selection of constraints
  - paper: "M. Bilenko, S. Basu and R. J. Mooney, Integrating constraints and metric learning in semi-supervised clustering, Proceedings of ICML 2004"
    title: Bilenko, Basu and Mooney 2004
    locator: MPCKMeans, which learns a distance from the constraints
  - book: isbn:9781584889960
    title: "Sugato Basu, Ian Davidson and Kiri L. Wagstaff (editors), Constrained Clustering: Advances in Algorithms, Theory, and Applications"
    locator: Chapter 1 (introduction and the types of constraints)
---

Constrained clustering is clustering with side information in the form of pairwise constraints. A must-link constraint says that two points must be in the same cluster, and a cannot-link constraint says that two points must be in different clusters. The task is to find $k$ clusters that satisfy all constraints and are good for a usual objective, such as the sum of squared distances of the [k-means problem](/k-means-problem/). The constraints were introduced by Wagstaff and Cardie in 2000. Davidson and Ravi showed in 2005 that already the question whether any clustering satisfies the constraints is NP-complete when cannot-link constraints are present, while must-link constraints alone are easy.

## In plain words

Sometimes a user knows a little about the answer before clustering. She may know that two documents are about the same topic, or that two cars on a road are in different lanes. Constrained clustering takes this knowledge as pairs: "these two go together" and "these two stay apart".

"Go together" is easy to handle. If $a$ goes with $b$ and $b$ goes with $c$, then $a$ goes with $c$, so the points fall into fixed groups that always stay together. "Stay apart" is harder. If $a$, $b$ and $c$ must all stay apart, two clusters are not enough. Deciding whether $k$ clusters are enough is the same as coloring a map with $k$ colors so that neighbors differ, and that is a hard problem.

## Definition

The input is a set $X$ of $n$ points with a distance or a feature space, an integer $k$, a set $\mathrm{ML}$ of must-link pairs and a set $\mathrm{CL}$ of cannot-link pairs. A clustering is a map $\ell: X \to \{1, \ldots, k\}$ whose $k$ clusters are nonempty. It is feasible if $\ell(a) = \ell(b)$ for each $\{a, b\} \in \mathrm{ML}$ and $\ell(a) \ne \ell(b)$ for each $\{a, b\} \in \mathrm{CL}$.

- **Feasibility problem.** Given $X$, $k$, $\mathrm{ML}$ and $\mathrm{CL}$, is there a feasible clustering?
- **Optimization problem.** Among the feasible clusterings, find one with the least value of an objective, for example $\sum_{j} \sum_{x \in C_j}\|x - \mu_j\|^2$.

The must-link constraints generate an equivalence relation: its classes, the ML components, are the [connected components](/connected-components/) of the graph with the ML pairs as edges, that is, the [transitive closure](/transitive-closure/) of ML. Every feasible clustering is constant on each ML component. A cannot-link pair inside one ML component makes the instance infeasible. One more consequence follows: if $a$ and $b$ are must-linked and $b$ and $c$ cannot-linked, then $a$ and $c$ are cannot-linked.

## Variants

- **Hard and soft constraints.** Hard constraints must hold, as above. Soft constraints have penalties $w_{ab}$ for each violated pair that are added to the objective, as in PCKMeans of Basu, Banerjee and Mooney (2004). Then each clustering is feasible.
- **Learned distance.** MPCKMeans of Bilenko, Basu and Mooney (2004) changes the distance so that must-linked points come closer and cannot-linked points move apart.
- **Cluster-level constraints.** Davidson and Ravi also study the $\delta$-constraint (two points in different clusters are at distance at least $\delta$) and the $\varepsilon$-constraint (each point of a cluster with two or more points has another point of its cluster within distance $\varepsilon$). The $\delta$-constraint is the same as must-link constraints on all pairs closer than $\delta$; the $\varepsilon$-constraint is a disjunction of must-link constraints for each point.
- **Size constraints.** Lower or upper bounds on the cluster sizes, often solved by flows or integer programs.
- **At most $k$ clusters.** If empty clusters are allowed, feasibility asks for a coloring with at most $k$ colors; this changes only the case with fewer than $k$ ML components.
- **Constraints on a hierarchy.** For [hierarchical clustering](/hierarchical-clustering-problem/), constraints say which pairs must join below or above a level.

## Examples

Take six points with $\mathrm{ML} = \{01, 12, 34\}$ and $\mathrm{CL} = \{23, 05, 45\}$. The ML components are $A = \{0, 1, 2\}$, $B = \{3, 4\}$ and $C = \{5\}$. The CL pairs connect $A$ and $B$ (by $23$), $A$ and $C$ (by $05$) and $B$ and $C$ (by $45$).

| $k$ | feasible? | reason |
|---|---|---|
| 1 | no | the CL pairs need two clusters at least |
| 2 | no | $A$, $B$, $C$ are a triangle in the CL graph, which needs 3 colors |
| 3 | yes | $A$, $B$ and $C$ each form one cluster |
| 4 | no | there are only 3 ML components, so a fourth cluster would split one |

If the must-link pair $03$ is added, $A$ and $B$ join into one component, and the cannot-link pair $23$ is now inside it: no $k$ works.

A second example shows that greedy assignment can fail on a feasible instance. Take points $a$, $b$, $c$, $k = 2$ and $\mathrm{CL} = \{ac, bc\}$. The clustering $\{a, b\}, \{c\}$ is feasible. But a method that first puts $a$ in cluster 1 and $b$ in cluster 2, for example because each is near that center, then has no cluster left for $c$. This happens in [COP-k-means](/cop-k-means/).

## Known algorithms

- **Feasibility with ML only.** Compute the ML components with a [disjoint-set forest](/disjoint-set/) in near-linear time. A feasible clustering exists if and only if there are at least $k$ components.
- **Feasibility with ML and CL.** Contract the ML components, reject if a CL pair lies inside a component, and color the graph of CL pairs between components with $k$ colors. For $k = 2$ this is a [bipartiteness test](/bipartiteness-testing/) in linear time. For $k \ge 3$ use backtracking or a SAT or integer programming solver; small instances are easy in practice. The steps are:

```pseudo id=main
FEASIBLE(X, ML, CL, k)
L1  comp ← the ML components (union of each ML pair in a disjoint-set forest); m ← their number
L2  if m < k then return "infeasible"
L3  if some CL pair has both points in one component then return "infeasible"
L4  color the graph of CL pairs between components with at most k colors
        (2-coloring by breadth-first search if k = 2, backtracking otherwise); if impossible return "infeasible"
L5  while some color c is unused do move one component of a class with two or more components to c
    return the label of each point = the color of its component
```
- **[COP-k-means](/cop-k-means/)** (Wagstaff et al. 2001) runs k-means and assigns each point to the nearest center that violates no constraint. It is fast, but it can fail on feasible instances.
- **PCKMeans and MPCKMeans** treat the constraints as soft, with penalties, and so always return a clustering.
- **Exact methods.** Integer linear programming, constraint programming and column generation find optimal constrained clusterings for moderate $n$.
- **Spectral methods.** The constraints change the affinity matrix, for example by setting must-linked affinities to 1 and cannot-linked affinities to 0.

## Bounds

- **Cannot-link feasibility is NP-complete** for each fixed $k \ge 3$ (Davidson and Ravi 2005), by the reduction from [k-coloring](/k-coloring/) below. So, unless P = NP, no polynomial algorithm finds a feasible clustering whenever one exists, and no polynomial algorithm has any approximation ratio for the constrained objective with hard cannot-link constraints.
- **Must-link feasibility is in P,** and so is cannot-link feasibility with $k = 2$, by 2-coloring.
- **The objective.** Even without constraints, the k-means and [k-median](/k-median-problem/) objectives are NP-hard, so the constrained versions are too.
- **Davidson and Ravi** also study the $\delta$ and $\varepsilon$ constraints and their combinations with ML and CL. The $\delta$ constraint alone reduces to ML and is in P; the combinations with cannot-link constraints contain the CL case and are NP-complete in general.

## Reductions

**From k-coloring to cannot-link feasibility.** Let $G = (V, E)$ be a graph with $|V| \ge k$. Take $X = V$, no ML pairs, $\mathrm{CL} = E$, and the same $k$. A feasible clustering is a proper coloring with $k$ colors, all used. Conversely, take a proper coloring with at most $k$ colors. While fewer than $k$ colors are used, some color class has two or more vertices, because $|V| \ge k$; give one of them a new color. This keeps the coloring proper, because the new color class has only one vertex, and it uses one color more. So $G$ is $k$-colorable if and only if the instance is feasible. The map is computed in linear time.

**From constrained feasibility to k-coloring.** Contract each ML component to one vertex and connect two components when a CL pair joins them. The instance is feasible if and only if no CL pair lies inside a component, there are at least $k$ components, and the contracted graph is $k$-colorable; the argument is the same as above. So feasibility is in NP and has the same complexity as $k$-coloring.

## Applications

- **Lane finding.** Wagstaff et al. (2001) clustered GPS traces of cars into road lanes: points from the same trace in a short time are must-linked, and points too far apart across the road are cannot-linked.
- **Text and documents.** A user marks a few pairs of documents as related or not, and the clustering follows these choices.
- **Image segmentation and video.** Pixels or frames known to belong to the same object are must-linked.
- **Entity resolution.** Records with the same key must link, and records with conflicting fields cannot link.
- **Active learning.** The algorithm chooses which pairs to ask a user about, to get the most information from few constraints.

## References
