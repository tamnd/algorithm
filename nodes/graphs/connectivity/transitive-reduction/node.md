---
tag: ESGDFK
kind: problem
slug: transitive-reduction
name: Transitive reduction
area: graphs/connectivity
level: core
summary: Finds the smallest subgraph of a directed graph that has the same reachability, removing edges implied by other paths.
prereqs: [transitive-closure, condensation-graph, directed-acyclic-graph]
see_also: [warshall-algorithm, strongly-connected-components, topological-sort, hamiltonian-cycle-problem, boolean-matrix-multiplication, reachability]
sources:
  - paper: doi:10.1137/0201008
    title: Alfred V. Aho, Michael R. Garey and Jeffrey D. Ullman, The transitive reduction of a directed graph, SIAM Journal on Computing 1(2), 131 to 137 (1972)
    locator: the whole paper (the definition, uniqueness for acyclic graphs, the construction for graphs with cycles, and the equivalence in complexity with the transitive closure)
  - paper: doi:10.1137/s0097539793256685
    title: Samir Khuller, Balaji Raghavachari and Neal Young, Approximating the minimum equivalent digraph, SIAM Journal on Computing 24(4), 859 to 872 (1995)
    locator: the whole paper (the subgraph version, its hardness, and approximation algorithms)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 23.2, The Floyd-Warshall algorithm (transitive closure, which the reduction algorithms use)
---

The transitive reduction of a [directed graph](/directed-graph/) is a graph with as few arcs as possible that has the same [transitive closure](/transitive-closure/): the same pairs $(u, v)$ with a path from $u$ to $v$. For an acyclic graph it is unique and is a subgraph: keep exactly the arcs $(u, v)$ for which no longer path leads from $u$ to $v$. For a partial order this is the Hasse diagram. Aho, Garey and Ullman showed in 1972 that it takes the same time as the transitive closure. If the answer must use only arcs of the input, the problem becomes the minimum equivalent subgraph, which is NP-hard.

## In plain words

A list of tasks says which must be done before which. Some rules are implied by others: if A comes before B and B before C, the rule "A before C" adds nothing. The transitive reduction throws out every rule that follows from the others, and keeps the fewest rules that still say the same thing.

When the rules have no loops, there is exactly one smallest set: keep a rule only if no chain of other rules leads from its start to its end. When some tasks form loops, where each can be reached from the others, any ring through those tasks does the job, so there are many smallest answers. Asking for the fewest rules among those already written down is a much harder puzzle.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n$ vertices and $m$ arcs. [Parallel arcs](/multigraph/) and [self-loops](/self-loop/) are allowed in the input. The output has no parallel arcs, as a second copy never changes reachability. Write $G^+$ for the transitive closure: $(u, v) \in G^+$ when $G$ has a walk of length at least 1 from $u$ to $v$.

**Transitive reduction (Aho, Garey, Ullman).** A graph $H$ on the same vertex set with $H^+ = G^+$ and with as few arcs as possible. $H$ need not be a subgraph of $G$.

**Minimum equivalent subgraph.** The same, but $H$ must be a subgraph of $G$. Also called the minimum equivalent digraph.

**Loops.** With the closure $G^+$ above, $(v, v) \in G^+$ exactly when $v$ lies on a cycle. A vertex that is a strong component by itself and has a loop keeps the loop in every reduction. With the reflexive closure instead, loops are never needed and are dropped. The two conventions differ only in these loops.

**Theorem 1 (acyclic graphs).** Let $G$ be acyclic. Call an arc $(u, v)$ *redundant* if $G$ has a path of length at least 2 from $u$ to $v$, and let $E_{\mathrm{red}}$ be the set of arcs that are not redundant, one copy each. Then $(V, E_{\mathrm{red}})$ is the unique transitive reduction of $G$, and it is a subgraph of $G$.

*Proof.* Let $L(u, v)$ be the largest length of a path from $u$ to $v$, defined when $(u, v) \in G^+$; it is finite as $G$ is acyclic.

*Same closure.* We show that each arc $(u, v)$ of $G$ is in $E_{\mathrm{red}}^+$, by induction on $L(u, v)$. If $(u, v)$ is not redundant it is in $E_{\mathrm{red}}$. Else take a path $u = x_0, \ldots, x_\ell = v$ with $\ell \ge 2$. For each of its arcs, $L(u, v) \ge L(x_t, x_{t+1}) + (\ell - 1) > L(x_t, x_{t+1})$, because a longest path from $x_t$ to $x_{t+1}$ can be extended along the rest of the path, and in an acyclic graph the result is still a path. By induction every arc of the path is in $E_{\mathrm{red}}^+$, so $(u, v)$ is too. Hence $E^+ \subseteq E_{\mathrm{red}}^+ \subseteq E^+$.

*Contained in every equivalent graph.* Let $H^+ = G^+$ and $(u, v) \in E_{\mathrm{red}}$. Then $(u, v) \in H^+$, so $H$ has a walk from $u$ to $v$. If it had length at least 2, through a vertex $w$, then $(u, w)$ and $(w, v)$ would be in $G^+$, and $w \ne u, v$ as $G$ is acyclic; joining the two paths of $G$ gives a walk, hence a path, from $u$ to $v$ through $w$, of length at least 2, so $(u, v)$ would be redundant. So $H$ has the arc $(u, v)$, and $E_{\mathrm{red}} \subseteq H$.

So $E_{\mathrm{red}}$ has the right closure and is contained in every graph with this closure. Any equivalent $H$ with $|H| \le |E_{\mathrm{red}}|$ equals it. $\square$

**Theorem 2 (general graphs).** Let $C_1, \ldots, C_r$ be the [strong components](/strongly-connected-components/) of $G$ and $K$ its [condensation](/condensation-graph/). Build $H$ as follows: for each component with $|C| \ge 2$, a directed cycle through its vertices in any order; for each component $\{v\}$ that has a loop, the loop; and for each arc $(C, D)$ of the transitive reduction of the acyclic graph $K$, one arc from any vertex of $C$ to any vertex of $D$. Then $H$ is a transitive reduction of $G$.

*Proof.* $H$ has the same strong components as $G$, the same loops on single vertices, and its condensation has the reduction of $K$ as its arcs, so $H^+ = G^+$. For the lower bound, let $H'$ be any graph with $H'^+ = G^+$. It has the same strong components, as these are read off the closure. A vertex $c$ of a component $C$ with $|C| \ge 2$ has a path in $H'$ to another vertex of $C$; the first arc of this path ends in a vertex that reaches $C$ and is reached from $c$, so it lies in $C$. So $H'$ has at least $|C|$ arcs inside $C$. A single vertex $v$ with $(v, v) \in G^+$ needs a closed walk in $H'$, which can only be a loop. For an arc $(C, D)$ of the reduction of $K$, a path of $H'$ from $C$ to $D$ visits a sequence of components that is a path of $K$ from $C$ to $D$; this path can only be the arc $(C, D)$, so $H'$ has an arc from $C$ to $D$. These arcs are all different, so $|H'| \ge |H|$. $\square$

So the size of a transitive reduction is unique, but for graphs with cycles the reduction itself is not, and it may use arcs that $G$ does not have.

## Variants

- **Minimum equivalent subgraph.** Require $H \subseteq E$. For acyclic graphs it coincides with the transitive reduction by Theorem 1. With cycles it is NP-hard (see Bounds); Khuller, Raghavachari and Young give polynomial approximations with a constant ratio.
- **Hasse diagram.** For a finite partial order, viewed as an acyclic graph, the reduction is the covering relation, drawn as the Hasse diagram.
- **Reflexive convention.** Use the reflexive closure, and drop all loops (see Definition).

## Examples

**A triangle.** With the arcs $a \to b$, $b \to c$, $a \to c$, the arc $a \to c$ is redundant, and the reduction is the path $a \to b \to c$.

**Divisibility.** On $\{1, 2, 3, 4, 6, 12\}$ with $x \to y$ when $x$ divides $y$ and $x \ne y$, the graph has 12 arcs. The reduction keeps the 7 arcs $1 \to 2$, $1 \to 3$, $2 \to 4$, $2 \to 6$, $3 \to 6$, $4 \to 12$, $6 \to 12$, the Hasse diagram.

**The running example.** Take the graph of the [depth-first search](/depth-first-search/) page, with 10 arcs and the lists $0: 1, 3, 2$; $1: 2$; $2: 0$; $3: 2, 4$; $4$: none; $5: 4, 6$; $6: 5$. Its components are $\{0, 1, 2, 3\}$, $\{4\}$ and $\{5, 6\}$, and the condensation has the two arcs $\{0, 1, 2, 3\} \to \{4\}$ and $\{5, 6\} \to \{4\}$, both needed. One transitive reduction is $0 \to 1 \to 2 \to 3 \to 0$, $5 \to 6 \to 5$, $3 \to 4$ and $5 \to 4$, with 8 arcs; the arc $2 \to 3$ is not in $G$. The minimum equivalent subgraph has 9 arcs, and is unique here: $0 \to 1$, $0 \to 3$, $1 \to 2$, $2 \to 0$, $3 \to 2$, $3 \to 4$, $5 \to 4$, $5 \to 6$, $6 \to 5$. It needs one more arc because $\{0, 1, 2, 3\}$ has no Hamiltonian cycle in $G$: both 1 and 3 have 2 as their only successor inside the component.

**A loop.** For one vertex with a loop, the reduction is the loop itself. For a vertex with a loop inside a larger component, the loop is redundant.

## Known algorithms

| Algorithm | Time | Notes |
|---|---|---|
| Closure, then filter | $O(n^\omega)$ or $O(n^3 / w)$ | For a DAG, $A_{\mathrm{red}} = A \wedge \lnot (A \cdot A^+)$ |
| Search from each vertex | $O(n m)$ | For each $u$, mark what is reachable in two or more steps |
| Through the condensation | linear time plus the cost on $K$ | Theorem 2 |

**Closure, then filter.** For a DAG with adjacency matrix $A$ and closure $R = A^+$, the arc $(u, v)$ is redundant exactly when some successor $w \ne v$ of $u$ has $R[w][v] = 1$; as $G$ is acyclic, $w = v$ cannot give $R[v][v] = 1$. So the redundant arcs are the 1 entries of the Boolean product $A \cdot R$, and $A_{\mathrm{red}} = A \wedge \lnot (A R)$. With [Warshall's algorithm](/warshall-algorithm/) and bit rows this is $O(n^3 / w)$; with fast [Boolean matrix multiplication](/boolean-matrix-multiplication/) it is $O(n^\omega)$.

**Search from each vertex.** For each $u$, run a search from the successors of the successors of $u$, and drop every arc $(u, v)$ whose $v$ is marked. Each search is $O(n + m)$.

**Topological order with bit vectors.** In a DAG, take the vertices $u$ in reverse [topological order](/topological-sort/), keeping a bit vector of the vertices each reaches. Take the successors of $u$ in topological order; keep the arc to $v$ when $v$ is not yet in the reach set of $u$, and then add the reach set of $v$.

**Graphs with cycles.** Compute the strong components in $\Theta(n + m)$ time, reduce the condensation with one of the methods above, and add a cycle per component as in Theorem 2.

## Bounds

- **Same complexity as the closure.** Aho, Garey and Ullman proved that, up to constant factors, the transitive reduction and the transitive closure take the same time. So, by the bounds of the closure, the reduction takes $O(n^\omega)$ time, and a much faster reduction algorithm would give a faster Boolean matrix product.
- **Output.** The reduction of a DAG can have $\Theta(n^2)$ arcs: in the complete bipartite DAG with all arcs from a set of $n/2$ sources to a set of $n/2$ sinks, no arc is redundant.
- **Minimum equivalent subgraph is NP-hard.** *Proof.* Let $G$ be strongly connected with $n \ge 2$ vertices. A strongly connected spanning subgraph gives each vertex at least one arc in and one arc out, so it has at least $n$ arcs, and if it has exactly $n$ arcs, every vertex has exactly one arc in and one out, so it is a union of disjoint cycles, which is strongly connected only if it is one cycle through all vertices. So $G$ has an equivalent subgraph with $n$ arcs exactly when it has a [Hamiltonian cycle](/hamiltonian-cycle-problem/), which is NP-complete to decide on directed graphs. $\square$

## Reductions

- **To transitive closure and one Boolean product,** for DAGs, as above.
- **To strong components,** for general graphs, by Theorem 2.
- **From Hamiltonian cycle,** for the subgraph version, as in Bounds.
- **To reachability queries.** Storing the reduction instead of the graph keeps all reachability information in the fewest arcs, which can speed up searches on dense DAGs.

## Applications

- **Hasse diagrams.** Drawing a partial order, such as a class hierarchy, a lattice or a version history, by its covering relation only.
- **Build and package systems.** Removing implied dependencies to simplify a dependency graph before showing it or scheduling it.
- **Graph drawing.** A layered drawing of a DAG is easier to read when the transitive arcs are left out.
- **Network design.** The minimum equivalent subgraph asks for the fewest one-way links that keep every existing connection, a basic sparse design problem.

## References
