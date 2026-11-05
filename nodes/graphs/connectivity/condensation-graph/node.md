---
tag: MFY06B
kind: definition
slug: condensation-graph
name: Condensation graph
aliases:
- SCC DAG
- Component graph
area: graphs/connectivity
level: core
summary: The DAG obtained by contracting each strongly connected component to a single vertex.
prereqs: [strongly-connected-components, directed-acyclic-graph]
see_also: [topological-sort, kosaraju-sharir, tarjan-scc, gabow-path-based-scc, graph-transpose, transitive-closure, 2-sat, reachability]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.5, Strongly connected components (the component graph and the lemma that it is acyclic)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Section 3.4, Strongly connected components (every directed graph is a dag of its strongly connected components)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.2, Directed graphs (strong connectivity and the kernel DAG)
  - paper: "Kapali P. Eswaran and Robert E. Tarjan, Augmentation problems, SIAM Journal on Computing 5(4), 653 to 665 (1976)"
    locator: the strong connectivity augmentation theorem (max of the numbers of sources and sinks)
---

The condensation of a [directed graph](/directed-graph/) $G$ is the graph with one vertex for each [strongly connected component](/strongly-connected-components/) of $G$, and an edge from one component to another when $G$ has an edge from a vertex of the first to a vertex of the second. It is always a [directed acyclic graph](/directed-acyclic-graph/), so each directed graph is a DAG of strongly connected pieces. Many questions about $G$, such as [reachability](/reachability/), the [transitive closure](/transitive-closure/) and [2-SAT](/2-sat/), become questions about this DAG, which is often much smaller and can be handled in [topological order](/topological-sort/).

## Definition

Let $G = (V, E)$ be a directed graph. Parallel edges and [self-loops](/self-loop/) are allowed. Write $u \leadsto v$ when $G$ has a directed path from $u$ to $v$ (a path of length 0 is allowed, so $u \leadsto u$). The relation "$u \leadsto v$ and $v \leadsto u$" is an equivalence relation, and its classes $C_1, \ldots, C_k$ are the strongly connected components. Let $\mathrm{comp}(v)$ be the class of $v$.

The condensation is the graph $G^{\mathrm{SCC}} = (V^{\mathrm{SCC}}, E^{\mathrm{SCC}})$ with

$$V^{\mathrm{SCC}} = \{C_1, \ldots, C_k\}, \qquad E^{\mathrm{SCC}} = \{\, (C_i, C_j) : i \neq j, \ \exists (u, v) \in E \text{ with } u \in C_i, \ v \in C_j \,\}.$$

So it is a simple directed graph: the edges inside one component disappear, and many edges between the same two components become one edge. Some programs keep the multiplicity, or keep one edge of $G$ as a witness for each edge of $G^{\mathrm{SCC}}$; the theorems below hold for both forms. The map $v \mapsto \mathrm{comp}(v)$ *contracts* each component to one vertex.

**Theorem 1 (acyclic).** $G^{\mathrm{SCC}}$ has no directed cycle.

*Proof.* It has no loops by definition. Suppose it has a directed cycle $D_0 \to D_1 \to \cdots \to D_{\ell} = D_0$ with $\ell \ge 2$ and $D_0 \neq D_1$. For each step $D_{i} \to D_{i+1}$ pick an edge $(u_i, v_i)$ of $G$ with $u_i \in D_i$ and $v_{i} \in D_{i+1}$. Inside $D_{i+1}$, $v_i \leadsto u_{i+1}$ (indices mod $\ell$). Joining these pieces gives $u_0 \leadsto v_0 \leadsto u_1 \leadsto \cdots \leadsto u_0$, so $u_0 \leadsto v_0$ and $v_0 \leadsto u_0$. Then $u_0$ and $v_0$ are in the same component, so $D_0 = D_1$, a contradiction. $\square$

**Theorem 2 (reachability).** For $u, v \in V$: $u \leadsto v$ in $G$ if and only if $\mathrm{comp}(u) \leadsto \mathrm{comp}(v)$ in $G^{\mathrm{SCC}}$.

*Proof.* A path in $G$ maps to a walk in $G^{\mathrm{SCC}}$ when we drop the steps inside one component, since each other step is an edge of $G^{\mathrm{SCC}}$. Conversely, take a path $\mathrm{comp}(u) = D_0 \to D_1 \to \cdots \to D_\ell = \mathrm{comp}(v)$ and edges $(u_i, v_i)$ as in Theorem 1. Inside each component every vertex reaches every other, so $u \leadsto u_0 \to v_0 \leadsto u_1 \to \cdots \to v_{\ell-1} \leadsto v$. $\square$

**Consequences.**

- $G$ is [strongly connected](/strongly-connected-graph/) if and only if $G^{\mathrm{SCC}}$ has exactly one vertex.
- $G$ is acyclic if and only if each component is a single vertex without a loop. Then $G^{\mathrm{SCC}}$ is $G$ with parallel edges merged.
- Since $G^{\mathrm{SCC}}$ is a DAG, it has a [topological order](/topological-ordering/), at least one *source* component (in-degree 0) and at least one *sink* component (out-degree 0). [Tarjan's algorithm](/tarjan-scc/) outputs the components in reverse topological order, and the form of the [Kosaraju-Sharir algorithm](/kosaraju-sharir/) in CLRS, which searches the transpose second, outputs them in topological order.
- The [transpose](/graph-transpose/) has the same components, and its condensation is the transpose of $G^{\mathrm{SCC}}$.
- The [transitive closure](/transitive-closure/) of $G$ follows from the closure of $G^{\mathrm{SCC}}$ by Theorem 2: $u$ reaches $v$ exactly when $\mathrm{comp}(u)$ reaches $\mathrm{comp}(v)$.

**Making a graph strongly connected.** Let $G^{\mathrm{SCC}}$ have $k \ge 2$ vertices, $s$ sources and $t$ sinks, where an isolated component counts as both. Then the least number of new edges that make $G$ strongly connected is $\max(s, t)$ (Eswaran and Tarjan, 1976). The lower bound is short: in a strongly connected graph each component has an edge that enters it and an edge that leaves it, so each source component needs a new edge that enters it and each sink component needs a new edge that leaves it, and one new edge enters only one component and leaves only one. The matching construction is in the paper.

**Cost.** Given the label $\mathrm{comp}$, the condensation is built in $O(n + m)$ time: scan each edge $(u, v)$ with $\mathrm{comp}(u) \neq \mathrm{comp}(v)$ and add the pair, removing repeated pairs with a mark array per component or with a [counting sort](/counting-sort/) of the pairs. The labels themselves cost $O(n + m)$ with any linear strong components algorithm.

## Examples and non-examples

The graph $G$ has the vertices 0 to 7 and 13 edges: $0 \to 1$, $1 \to 2$, $2 \to 0$, $2 \to 3$, $1 \to 3$, $3 \to 4$, $4 \to 3$, $4 \to 5$, $0 \to 5$, $5 \to 6$, $6 \to 5$, $6 \to 7$, and the loop $7 \to 7$.

| component | vertices | edges of $G$ inside it |
|---|---|---|
| $A$ | 0, 1, 2 | $0 \to 1$, $1 \to 2$, $2 \to 0$ |
| $B$ | 3, 4 | $3 \to 4$, $4 \to 3$ |
| $C$ | 5, 6 | $5 \to 6$, $6 \to 5$ |
| $D$ | 7 | the loop $7 \to 7$ |

| edge of $G^{\mathrm{SCC}}$ | edges of $G$ that give it |
|---|---|
| $A \to B$ | $2 \to 3$ and $1 \to 3$ |
| $A \to C$ | $0 \to 5$ |
| $B \to C$ | $4 \to 5$ |
| $C \to D$ | $6 \to 7$ |

The condensation has 4 vertices and 4 edges, and no cycle. Its only topological order is $A, B, C, D$. The source is $A$ and the sink is $D$, so one new edge makes $G$ strongly connected, for example $7 \to 0$. By Theorem 2, the vertex 1 reaches 6 because $A \leadsto C$, and 5 does not reach 3 because $C \not\leadsto B$.

More cases:

| graph | condensation |
|---|---|
| a directed cycle | one vertex |
| a DAG | the DAG itself, with parallel edges merged |
| $n$ vertices and no edges | $n$ isolated vertices; $s = t = n$, so $n$ new edges are needed for $n \ge 2$ |
| the edges $0 \to 1$ and $1 \to 0$ twice each | one vertex |
| an undirected graph stored as edges in both directions | its [connected components](/connected-components/), with no edges |

**Non-example.** Contracting the [biconnected components](/biconnected-components/) or the weak components of a directed graph does not give the condensation: the weak component of $0 \to 1$ is $\{0, 1\}$, but the condensation has two vertices and the edge $\{0\} \to \{1\}$.

## Related definitions

- [Strongly connected components](/strongly-connected-components/): the vertices of the condensation.
- [Directed acyclic graph](/directed-acyclic-graph/) and [topological sort](/topological-sort/): the shape of the condensation and the order in which algorithms process it.
- [Graph transpose](/graph-transpose/): same components, reversed condensation.
- [Transitive closure](/transitive-closure/) and [transitive reduction](/transitive-reduction/): both are usually computed on the condensation.
- [2-SAT](/2-sat/): a formula is satisfiable if and only if no variable is in the same component as its negation in the implication graph, and an order of the condensation gives a satisfying assignment.
- [Block-cut tree](/block-cut-tree/): the analogue for undirected graphs, with blocks in place of strong components.

## References
