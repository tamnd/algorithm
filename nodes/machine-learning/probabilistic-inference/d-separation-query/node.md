---
tag: W0ZM3T
kind: problem
slug: d-separation-query
name: d-separation query
aliases:
- conditional independence test in a Bayesian network
- d-separation test
area: machine-learning/probabilistic-inference
level: core
summary: "Given a DAG and disjoint node sets X, Y and Z, decide whether Z d-separates X from Y. A reachability search answers it in O(|V| + |E|) time."
prereqs: [d-separation, directed-acyclic-graph, graph-reachability]
see_also: [bayes-ball, bayesian-network, conditional-independence, markov-blanket, backdoor-criterion, do-calculus, bayesian-network-structure-learning, breadth-first-search]
sources:
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 3, Section 3.3.3 (an algorithm for d-separation, Algorithm 3.1, the procedure Reachable) and Section 3.3.2 (soundness and completeness)"
  - paper: doi:10.1002/net.3230200504
    title: Dan Geiger, Thomas Verma and Judea Pearl, Identifying independence in Bayesian networks, Networks 20(5), 1990, pages 507 to 534
    locator: the linear-time algorithm that finds all nodes d-separated from a set given another set, and its correctness
  - paper: "Ross D. Shachter, Bayes-Ball: the rational pastime (for determining irrelevance and requisite information in belief networks and influence diagrams), Proceedings of the 14th Conference on Uncertainty in Artificial Intelligence (UAI 1998), pages 480 to 487"
    title: Shachter 1998
    locator: the Bayes-Ball algorithm and its linear running time
  - book: isbn:9781558604797
    title: Judea Pearl, Probabilistic Reasoning in Intelligent Systems, Networks of Plausible Inference, Morgan Kaufmann, 1988
    locator: "Chapter 3 (Markov and Bayesian networks), the definition of d-separation"
---

A d-separation query asks whether a set of nodes $Z$ [d-separates](/d-separation/) a set $X$ from a set $Y$ in a [directed acyclic graph](/directed-acyclic-graph/). In a [Bayesian network](/bayesian-network/) a yes answer proves that $X$ and $Y$ are [conditionally independent](/conditional-independence/) given $Z$ in every distribution that the network can represent. The definition talks about all paths, and there can be exponentially many, but the query reduces to [graph reachability](/graph-reachability/) on $2|V|$ states and so takes $O(|V| + |E|)$ time.

## In plain words

A Bayesian network draws each variable as a dot and each direct influence as an arrow. You want to know if learning one group of variables can change your belief about a second group, once you already know a third group. The rule that answers it looks at every route between the two groups and checks whether the known variables block the route. There can be a huge number of routes. The trick is to walk the graph once, like a flood fill, and to remember for each dot whether you came in along an arrow or against one. That is enough to tell where the walk may go next, so each dot and each arrow is handled a fixed number of times.

## Definition

**Data model.** The input is a DAG $G = (V, E)$, given by adjacency lists of parents and children, and three pairwise disjoint sets $X, Y, Z \subseteq V$ with $X$ and $Y$ non-empty. We write $\mathrm{Pa}(v)$, $\mathrm{Ch}(v)$ and $\mathrm{De}(v)$ for the parents, the children and the descendants of $v$ (the node itself is not in $\mathrm{De}(v)$), and $\mathrm{An}(Z)$ for $Z$ together with all ancestors of nodes of $Z$.

**Active trail.** A trail is a sequence of distinct nodes $v_0, v_1, \ldots, v_k$ in which each consecutive pair is joined by an edge in either direction. The trail is *active given $Z$* if each interior node $v_i$, $0 < i < k$, meets this condition:

- if $v_{i-1} \to v_i \leftarrow v_{i+1}$ (a *collider* on the trail), then $v_i \in Z$ or $\mathrm{De}(v_i) \cap Z \ne \emptyset$;
- otherwise (a chain $\to v_i \to$, $\leftarrow v_i \leftarrow$, or a fork $\leftarrow v_i \to$), $v_i \notin Z$.

**The query.** Output YES if no active trail given $Z$ joins a node of $X$ to a node of $Y$. This is written $X \perp_G Y \mid Z$, and the [d-separation](/d-separation/) page explains why it is the right notion of independence for a DAG. The relation is symmetric in $X$ and $Y$. A node of $X$ adjacent to a node of $Y$ always gives NO, because the trail of length one has no interior node.

## Variants

- **The reachable set.** Given $X$ and $Z$, output all nodes $y \notin Z$ such that an active trail joins $X$ to $y$. One run of the algorithm below answers the query for every $Y$ at once.
- **Irrelevance and requisite information.** For the query $P(X \mid Z)$, list the nodes whose tables can change the answer and the observed nodes that can change it. [Bayes-Ball](/bayes-ball/) computes both in the same linear time.
- **Deterministic nodes.** If some nodes are functions of their parents, more independences hold than d-separation shows. Geiger, Verma and Pearl give a modified criterion (D-separation) with the same linear cost, and Bayes-Ball handles these nodes with one extra test.
- **Finding a separator.** Given two nodes $x$ and $y$, find a $Z$ that d-separates them, or report that none exists. Adjacent nodes are never d-separated. If they are not adjacent, one of them, say $y$, is not a descendant of the other, and then $Z = \mathrm{Pa}(x)$ works, by the local directed [Markov property](/markov-property/). In words: take the parents of the node that comes later in a topological order.
- **Causal queries.** The [backdoor criterion](/backdoor-criterion/) and the rules of the [do-calculus](/do-calculus/) are d-separation queries in a graph with some edges removed.

## Examples

Take the DAG with the five nodes $A, B, C, D, E$ and the edges $A \to B$, $A \to C$, $B \to D$, $C \to D$, $D \to E$. The node $D$ is a collider on the trail $B \to D \leftarrow C$, and $E$ is its only descendant.

| $X$ | $Y$ | $Z$ | answer | reason |
|---|---|---|---|---|
| $B$ | $C$ | $\emptyset$ | NO | the fork $B \leftarrow A \to C$ is active |
| $B$ | $C$ | $\{A\}$ | YES | $A$ blocks the fork, and the collider $D$ has nothing of $Z$ at or below it |
| $B$ | $C$ | $\{A, D\}$ | NO | the collider $D$ is in $Z$, so $B \to D \leftarrow C$ is active |
| $B$ | $C$ | $\{A, E\}$ | NO | the descendant $E$ of the collider is in $Z$ |
| $B$ | $C$ | $\{D\}$ | NO | both trails are active |
| $A$ | $E$ | $\{D\}$ | YES | $D$ blocks both chains $A \to B \to D \to E$ and $A \to C \to D \to E$ |
| $A$ | $E$ | $\{B\}$ | NO | the chain $A \to C \to D \to E$ is open |
| $A$ | $D$ | $\{B, C\}$ | YES | $Z = \mathrm{Pa}(D)$, as in the separator rule |

For $X = \{B\}$ and $Z = \{A, E\}$, the reachable set is $\{B, C, D\}$, so the same run answers NO for $Y = \{C\}$ and for $Y = \{D\}$.

## Known algorithms

**Path enumeration.** List all simple trails from $X$ to $Y$ and test each one against the definition. This is correct by definition, but the number of trails can grow exponentially in $|V|$, and the tests of this page use it only as a reference on graphs with at most 7 nodes.

**The reachable set algorithm** (Koller and Friedman, Algorithm 3.1). A state is a pair $(v, d)$: $d = {\uparrow}$ means the trail entered $v$ from a child, and $d = {\downarrow}$ means it entered $v$ from a parent.

```pseudo id=main
REACHABLE(G, X, Z)
L1  A ← An(Z)                               ▷ Z and its ancestors, by a search up the parent lists
L2  S ← the states (x, ↑) for x ∈ X ;  seen ← ∅ ;  R ← ∅
L3  while S is not empty do
L4      remove a state (v, d) from S
L5      if (v, d) ∈ seen then continue
L6      seen ← seen ∪ {(v, d)}
L7      if v ∉ Z then R ← R ∪ {v}
L8      if d = ↑ and v ∉ Z then                ▷ chain or fork at v: go anywhere
L9          add (p, ↑) for each p ∈ Pa(v), and (c, ↓) for each c ∈ Ch(v)
L10     else if d = ↓ then
L11         if v ∉ Z then add (c, ↓) for each c ∈ Ch(v)       ▷ chain at v
L12         if v ∈ A then add (p, ↑) for each p ∈ Pa(v)       ▷ open collider at v
L13 return R                                ▷ X ⊥ Y | Z exactly when R ∩ Y = ∅
```

Lines L8 to L12 are the definition of an active trail written as local moves. A trail that enters $v$ from a child and leaves it is a chain or a fork at $v$, so it needs $v \notin Z$. A trail that enters from a parent and leaves to a child is a chain, so it also needs $v \notin Z$. A trail that enters from a parent and leaves to a parent makes $v$ a collider, so it needs $v \in Z$ or a descendant in $Z$, which is the test $v \in \mathrm{An}(Z)$ of line L12. The search may follow a walk that repeats a node. Koller and Friedman (Section 3.3.3) prove that such a walk exists exactly when a simple active trail exists, so $R$ is the reachable set.

| algorithm | time | notes |
|---|---|---|
| path enumeration | exponential in $|V|$ in the worst case | the definition, a test oracle only |
| reachable set (Koller and Friedman) | $O(|V| + |E|)$ | one search on $2|V|$ states |
| [Bayes-Ball](/bayes-ball/) (Shachter 1998) | $O(|V| + |E|)$ | also gives the requisite nodes; no separate ancestor pass |
| Geiger, Verma and Pearl (1990) | $O(|V| + |E|)$ | a search over edges that follows only legal pairs of consecutive edges |
| moral ancestral graph | $O(|V|^2)$ in the worst case | separation in the moralized graph of $\mathrm{An}(X \cup Y \cup Z)$; see [d-separation](/d-separation/) |

## Bounds

**Upper bound.** Line L1 visits each node of $\mathrm{An}(Z)$ once and scans its parent list once, so it costs $O(|V| + |E|)$. In the loop, each of the $2|V|$ states passes line L5 once, and a state $(v, d)$ adds at most $|\mathrm{Pa}(v)| + |\mathrm{Ch}(v)|$ new states. The sum of these over all states is at most $2 \cdot 2|E|$. So the whole query takes $O(|V| + |E|)$ time in the word RAM with adjacency lists, with $O(|V|)$ memory for the marks and $O(|V| + |E|)$ in the worst case for the stack of states.

**Lower bound.** The bound is linear in the size of the input. A matching $\Omega(|V|)$ bound holds for each correct algorithm: on a directed path from $x$ to $y$ with $Z = \emptyset$, the answer is NO, and the removal of any one of the $|V| - 1$ edges changes it to YES. So the algorithm must read each edge of the path.

## Reductions

- **To reachability.** The query is reachability from the states $(x, \uparrow)$ in a directed graph on the $2|V|$ states, with the moves of lines L8 to L12 as arcs. The arcs are built in $O(|V| + |E|)$ time after $\mathrm{An}(Z)$ is known.
- **From reachability in a DAG.** To decide whether $y$ is reachable from $x$ in a DAG, delete the edges into $x$ and ask the query with $Z = \emptyset$. With $Z$ empty, an active trail has no collider, so it is a common ancestor with a directed path down to each end. The only ancestor of $x$ is now $x$ itself, so $x$ and $y$ are d-connected exactly when $y$ is reachable from $x$. The two problems therefore have the same time bound up to a constant.

## Applications

- **Pruning before inference.** Nodes d-separated from the query given the evidence, and barren nodes below them, can be removed before [variable elimination](/variable-elimination/) or the [junction tree algorithm](/junction-tree-algorithm/).
- **Constraint-based structure learning.** The PC algorithm of [Bayesian network structure learning](/bayesian-network-structure-learning/) asks an oracle of conditional independence; d-separation queries on a known graph give that oracle in tests and simulations.
- **Causal inference.** The checks of the [backdoor criterion](/backdoor-criterion/) and of each rule of the [do-calculus](/do-calculus/) are d-separation queries in mutilated graphs.
- **Markov blankets.** The [Markov blanket](/markov-blanket/) of a node is a set that d-separates it from all other nodes.

## References
