---
tag: KFPNHK
kind: problem
slug: transitive-closure
name: Transitive closure
aliases:
- Reachability matrix
area: graphs/connectivity
level: core
summary: Compute, for every pair of vertices, whether a path exists between them.
prereqs: [reachability, directed-graph, adjacency-matrix]
see_also: [warshall-algorithm, transitive-reduction, boolean-matrix-multiplication, floyd-warshall, condensation-graph, dynamic-transitive-closure, strongly-connected-components, datalog]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 23.2, The Floyd-Warshall algorithm (the part on the transitive closure of a directed graph)
  - paper: doi:10.1145/321105.321107
    title: Stephen Warshall, A theorem on Boolean matrices, Journal of the ACM 9(1), 11 to 12 (1962)
    locator: the whole paper
  - paper: doi:10.1109/swat.1971.4
    title: Michael J. Fischer and Albert R. Meyer, Boolean matrix multiplication and transitive closure, 12th Annual Symposium on Switching and Automata Theory, 129 to 131 (1971)
    locator: the whole paper (transitive closure costs at most a constant factor more than Boolean matrix multiplication)
  - paper: doi:10.1016/0020-0190(71)90006-8
    title: Ian Munro, Efficient determination of the transitive closure of a directed graph, Information Processing Letters 1(2), 56 to 58 (1971)
    locator: the whole paper (closure in the time of matrix multiplication, through strong components and a block recursion)
  - paper: doi:10.1007/bf01940892
    title: Paul Purdom Jr., A transitive closure algorithm, BIT Numerical Mathematics 10(1), 76 to 94 (1970)
    locator: the whole paper (closure through the strong components and a topological order)
---

The transitive closure of a [directed graph](/directed-graph/) records, for every ordered pair of vertices $(u, v)$, whether some path leads from $u$ to $v$. It is the all-pairs form of [reachability](/reachability/), and its output is an $n \times n$ Boolean matrix, the *reachability matrix*. It can be computed by $n$ graph searches in $O(nm)$ time, by [Warshall's algorithm](/warshall-algorithm/) in $\Theta(n^3)$ time, or in the time of [Boolean matrix multiplication](/boolean-matrix-multiplication/), with which it is equivalent up to a constant factor.

## In plain words

Draw a map of one-way streets. For every pair of places, ask: can I drive from the first to the second? Write the answers in a table with a row and a column for each place. That table is the transitive closure.

It adds an arrow from one place to another whenever some chain of arrows already leads there. If you could go from a to b and from b to c, the closure has an arrow straight from a to c. Nothing else is added. A place gets an arrow to itself only if a round trip through it exists.

## Definition

**Input.** A directed graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$ and $m$ arcs, given as [adjacency lists](/adjacency-list/) or as an [adjacency matrix](/adjacency-matrix/). [Parallel arcs](/multigraph/) and [self-loops](/self-loop/) are allowed. Parallel arcs change nothing. A loop at $v$ puts $(v, v)$ in the closure.

**Output.** The *transitive closure* $G^+ = (V, E^+)$, where $(u, v) \in E^+$ exactly when $G$ has a [walk](/walk/) of length at least 1 from $u$ to $v$. As a matrix, $R[u][v] = 1$ exactly when $(u, v) \in E^+$.

**Reflexive form.** The *reflexive-transitive closure* $G^*$ also allows walks of length 0, so it adds $(v, v)$ for every $v$. Many texts call $G^*$ the transitive closure, including CLRS, so the convention must be checked. The two differ only on the diagonal: $(v, v) \in E^+$ exactly when $v$ lies on a directed cycle, a loop included.

Equivalently, $E^+$ is the smallest transitive relation on $V$ that contains $E$. *Proof.* The set $E^+$ contains $E$ and is transitive, as two walks can be joined. If $T \supseteq E$ is transitive, induction on the length shows that the ends of every walk of length at least 1 are in $T$. $\square$ In matrix terms, with $A$ the adjacency matrix and Boolean sums and products, $R = A + A^2 + \cdots + A^n$, because a walk that is longer than $n$ repeats a vertex and has a shorter walk with the same ends, of length at least 1.

**Undirected graphs.** If $G$ is undirected, given with both arcs of each edge, $R[u][v] = 1$ for $u \ne v$ exactly when $u$ and $v$ are in the same [connected component](/connected-components/), so the closure is a union of complete graphs, one for each component. Also $R[v][v] = 1$ exactly when $v$ has at least one edge, as $v \to w \to v$ is then a closed walk. The problem is then solved by finding the components, in $\Theta(n + m)$ time plus the output.

## Variants

- **Single source.** Only the row of one vertex: this is [reachability](/reachability/) from a source, one search in $\Theta(n + m)$ time.
- **Queries instead of a matrix.** Build a data structure that answers "does $u$ reach $v$" fast, with less than $n^2$ bits. These are reachability oracles and labeling schemes; see [reachability](/reachability/).
- **Dynamic closure.** Keep the closure, or answer reachability queries, while arcs are inserted and deleted. See [dynamic transitive closure](/dynamic-transitive-closure/).
- **Closure of a relation.** The same problem stated for a binary relation on a finite set, as in databases and logic programs, where the recursive query of a [Datalog](/datalog/) program such as `path(x, y) :- edge(x, z), path(z, y)` computes it.
- **Witnesses.** Return, with each 1 entry, an intermediate vertex or a path that proves it.

## Examples

**The running example.** Take the graph of the [depth-first search](/depth-first-search/) page, with the lists $0: 1, 3, 2$; $1: 2$; $2: 0$; $3: 2, 4$; $4$: none; $5: 4, 6$; $6: 5$. Its strong components are $\{0, 1, 2, 3\}$, $\{4\}$ and $\{5, 6\}$, and the arcs between them go into $\{4\}$. So

| from \\ to | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| 0, 1, 2, 3 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5, 6 | 0 | 0 | 0 | 0 | 1 | 1 | 1 |

The closure has $4 \cdot 5 + 0 + 2 \cdot 3 = 26$ arcs. The row of 4 is empty because 4 has no arcs out, and $R[4][4] = 0$ because 4 lies on no cycle; the reflexive closure would set it to 1.

**A path.** For the path $0 \to 1 \to \cdots \to n-1$, $R[u][v] = 1$ exactly when $u < v$: the closure is a transitive tournament with $n(n-1)/2$ arcs, from $n - 1$ input arcs. So the output can be quadratic in the input.

**A loop.** One vertex with a loop has $R = [1]$; without the loop, $R = [0]$.

## Known algorithms

| Algorithm | Time | Notes |
|---|---|---|
| A search from every vertex | $O(n(n + m))$ | Best for sparse graphs; BFS or DFS |
| [Warshall's algorithm](/warshall-algorithm/) | $\Theta(n^3)$, or $\Theta(n^3 / w)$ with $w$-bit words | Three nested loops on the matrix |
| Strong components, then a DAG in reverse topological order | $O(n + m + n' m' / w)$ | $n'$ and $m'$ are the sizes of the condensation |
| Repeated squaring of $I + A$ | $O(n^\omega \log n)$ | $\lceil \log_2 n \rceil$ Boolean products |
| Block recursion (Fischer and Meyer, Munro) | $O(n^\omega)$ | Same time as one Boolean product |

Here $\omega < 2.372$ is the [matrix multiplication exponent](/matrix-multiplication-exponent/).

**Searches.** A [depth-first search](/depth-first-search/) or breadth-first search from $u$ marks exactly the vertices $v$ with a walk from $u$ of length at least 0; to get $G^+$, start it from the successors of $u$ instead. $n$ searches take $O(n(n + m))$ time and are the best simple choice when $m$ is small.

**Through the condensation.** Vertices in one [strong component](/strongly-connected-components/) have equal rows, so it is enough to compute the closure of the [condensation](/condensation-graph/), which is a DAG. Process its nodes in reverse [topological order](/topological-sort/), and let the row of $C$ be the union over its arcs $(C, D)$ of $\{D\}$ and the row of $D$. With rows stored as bit vectors this costs $O(m' \cdot n' / w)$ word operations. This is the approach of Purdom.

**Matrix methods.** With $B = I + A$, $B^{2^k}$ records the walks of length at most $2^k$, so $\lceil \log_2 n \rceil$ squarings give $G^*$. Fischer and Meyer, and Munro, removed the $\log n$ factor: split the vertices into two halves, write the matrix as four blocks, and compute the closure from the closures of two half-size matrices and a constant number of half-size products.

## Bounds

- **Output.** The output has $n^2$ bits, and as the path example shows it can have $\Theta(n^2)$ ones from $\Theta(n)$ input arcs, so $\Omega(n^2)$ time is needed for the matrix output.
- **Equivalence with Boolean matrix multiplication.** Closure is at least as hard as one Boolean product. *Proof.* Given $n \times n$ Boolean matrices $X$ and $Y$, build a graph on $3n$ vertices $a_i, b_k, c_j$ with an arc $a_i \to b_k$ when $X[i][k] = 1$ and an arc $b_k \to c_j$ when $Y[k][j] = 1$. Every walk from an $a$ to a $c$ has length 2, so $R[a_i][c_j] = \bigvee_k X[i][k] Y[k][j] = (XY)[i][j]$. $\square$ The block recursion of Fischer and Meyer and of Munro gives the other direction. So the closure takes $\Theta(n^\omega)$ time up to constant factors, and a faster closure algorithm would give a faster Boolean product.
- **Combinatorial algorithms.** Without fast matrix multiplication, the [Four Russians method](/four-russians-method/), which was first used for this very problem, computes the closure in $O(n^3 / \log n)$ time.
- **Space.** $\Theta(n^2)$ bits for the output; the searches need only $O(n)$ extra words besides it.
- **Complexity class.** Each entry is an instance of directed reachability, which is complete for [NL](/nondeterministic-logspace/); see [reachability](/reachability/).

## Reductions

- **From reachability:** one entry of the closure answers one reachability query.
- **To and from Boolean matrix multiplication:** shown under Bounds.
- **To all-pairs shortest paths.** The closure is the pattern of finite entries of the distance matrix, so [Floyd-Warshall](/floyd-warshall/) computes it; Warshall's algorithm is Floyd-Warshall with Boolean "or" and "and" in place of "min" and "+".
- **Strong components from the closure.** $u$ and $v$ are in one strong component exactly when $u = v$ or $R[u][v] = R[v][u] = 1$.
- **Transitive reduction.** For DAGs, the [transitive reduction](/transitive-reduction/) and the transitive closure have the same complexity, by Aho, Garey and Ullman.

## Applications

- **Databases and logic programming.** Recursive queries such as "all ancestors" or "all parts of a part" are closures of a relation, and [Datalog](/datalog/) engines compute them.
- **Compilers and build systems.** Which functions may call which, which modules depend on which, and which definitions may reach which uses are closure questions on program graphs.
- **Type hierarchies and ontologies.** Subtype and "is-a" tests are reachability in a DAG; many systems precompute the closure or a compressed form of it.
- **Deadlock and model checking.** Wait-for graphs and state graphs are checked through reachability between many pairs.

## References
