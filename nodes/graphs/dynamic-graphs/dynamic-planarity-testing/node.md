---
tag: 10K97W
kind: problem
slug: dynamic-planarity-testing
name: Dynamic planarity testing
aliases:
- dynamic planarity
area: graphs/dynamic-graphs
level: research
summary: Maintain whether a graph remains planar under edge insertions and deletions.
prereqs: [dynamic-graph, planar-graph, planarity-testing, kuratowski-theorem]
see_also: [planar-embedding, hopcroft-tarjan-planarity-test, boyer-myrvold-planarity-test, dynamic-biconnectivity, sparsification, euler-formula, planar-separator-theorem]
sources:
  - paper: doi:10.1145/3357713.3384249
    title: Jacob Holm and Eva Rotenberg, Fully-dynamic planarity testing in polylogarithmic time, Proceedings of STOC 2020, 167 to 180
    locator: the main theorem (deterministic, O(log^3 n) amortized time per edge insertion or deletion)
  - paper: doi:10.1006/jcss.1996.0002
    title: David Eppstein, Zvi Galil, Giuseppe F. Italiano and Thomas H. Spencer, Separator based sparsification I, planarity testing and minimum spanning trees, Journal of Computer and System Sciences 52(1), 3 to 27 (1996)
    locator: the fully dynamic planarity testing result (O(n^(1/2)) amortized time per update or query)
  - paper: doi:10.1137/s0097539794280736
    title: Giuseppe Di Battista and Roberto Tamassia, On-line planarity testing, SIAM Journal on Computing 25(5), 956 to 997 (1996)
    locator: the main theorem (incremental planarity testing with SPQR-trees, O(log n) amortized time per operation)
  - paper: doi:10.1145/195058.195439
    title: Johannes A. La Poutré, Alpha-algorithms for incremental planarity testing, Proceedings of STOC 1994, 706 to 715
    locator: the main theorem (incremental planarity testing in inverse-Ackermann amortized time)
  - paper: doi:10.1007/s00224-017-9768-7
    title: Jacob Holm and Eva Rotenberg, Dynamic planar embeddings of dynamic graphs, Theory of Computing Systems 61(4), 1054 to 1083 (2017)
    locator: the main theorem (an embedded graph with flips, O(log^2 n) time per update and query)
---

Dynamic planarity testing is the problem of keeping the answer to "is the graph [planar](/planar-graph/)?" for an undirected [dynamic graph](/dynamic-graph/) under edge insertions and deletions. A static [planarity test](/planarity-testing/) takes linear time, so recomputation costs $O(n)$ per update, using that a planar graph has at most $3n - 6$ edges. In the fully dynamic setting the best bound was $O(n^{1/2})$ amortized from 1996 until Holm and Rotenberg (2020) gave a deterministic algorithm with $O(\log^3 n)$ amortized time per update. The hard part is that an insertion may need a different [embedding](/planar-embedding/), and the change can reach far from the new edge.

## In plain words

Draw a network on paper so that no two lines cross. Some networks allow this and some do not. As lines are added and removed, you want to know whether a drawing with no crossings still exists.

A new line may fit into the current drawing. If it does not, the drawing may still be redrawn so that it fits: you can flip a part of the drawing over, like turning a piece of paper. The hard question is whether some sequence of flips makes room. A removed line never makes things worse, but it can make room for a line that was refused earlier.

## Definition

**Input.** An undirected graph $G = (V, E)$ on $n$ vertices, at first with no edges, and an online sequence of $\mathrm{insert}(u, v)$ and $\mathrm{delete}(u, v)$ updates and queries.

**Queries.**

- $\mathrm{planar}()$ returns true if and only if $G$ has a planar embedding.
- $\mathrm{admissible}(u, v)$ returns true if and only if $G + \{u, v\}$ is planar.

**Output.** The answer to each query before the next operation is read. By [Kuratowski's theorem](/kuratowski-theorem/), $G$ is planar exactly when it has no subgraph that is a subdivision of $K_5$ or $K_{3,3}$.

**Cost.** Update and query time, worst case or [amortized](/amortized-update-time/). Updates are insertions only, deletions only, or both.

Two models differ in what may be inserted. In the **general** model, any edge may be inserted, and the structure must handle a non-planar graph and report it. In the **planar-preserving** model, only edges that keep the graph planar are inserted, and the question is how to find and keep an embedding.

## Variants

- **Insertions only.** Once the graph is non-planar, it stays so. Di Battista and Tamassia (1996) keep the SPQR-trees of the biconnected components and answer in $O(\log n)$ amortized time; La Poutré (1994) lowers this to inverse-Ackermann amortized time.
- **Deletions only.** Once the graph is planar, it stays so.
- **Fully dynamic.** Both.
- **Fixed embedding.** The graph comes with a planar embedding, and an edge may be inserted only across a face, between two vertices on the face boundary. The question is whether the two ends share a face.
- **Embedding with flips.** As above, but the structure may also flip parts of the embedding that are attached through at most two vertices.
- **Report an embedding.** Keep an actual planar embedding, not only the bit.

## Examples

Take $V = \{0, \ldots, 5\}$ and start from the complete bipartite graph $K_{3,3}$ with sides $\{0, 1, 2\}$ and $\{3, 4, 5\}$, minus the edge $25$. The bound $m \le 3n - 6 = 12$ holds in all rows, so edge counting alone never decides.

| update | edges | planar | reason |
|---|---|---|---|
| start | 8 | yes | $K_{3,3}$ minus an edge is planar |
| insert 01 | 9 | yes | |
| insert 34 | 10 | yes | |
| insert 25 | 11 | no | contains $K_{3,3}$ |
| delete 03 | 10 | yes | |
| insert 12 | 11 | yes | |

The insertion of $25$ completes $K_{3,3}$. The deletion of $03$ removes an edge of that $K_{3,3}$, and the result is planar again, although it has the same number of edges as the planar graph two rows before. So the answer depends on the structure, not on counts. A structure that keeps one fixed embedding can also fail: in a fixed drawing the two ends of an admissible edge need not share a face, and the drawing must change before the edge fits.

## Known algorithms

| setting | algorithm | update time | case |
|---|---|---|---|
| any | recompute with a linear-time test such as [Hopcroft-Tarjan](/hopcroft-tarjan-planarity-test/) or [Boyer-Myrvold](/boyer-myrvold-planarity-test/) | $O(n)$ | worst, deterministic |
| insertions only | Di Battista and Tamassia (1996), SPQR-trees | $O(\log n)$ | amortized, deterministic |
| insertions only | La Poutré (1994) | inverse Ackermann | amortized, deterministic |
| fixed embedding | Italiano, La Poutré and Rauch (1993) | $O(\log^2 n)$ | deterministic |
| embedding with flips | Holm and Rotenberg (2015, 2017) | $O(\log^2 n)$ | deterministic |
| fully dynamic | Eppstein, Galil, Italiano and Spencer (1996), separator-based [sparsification](/sparsification/) | $O(n^{1/2})$ | amortized, deterministic |
| fully dynamic | Holm and Rotenberg (2020) | $O(\log^3 n)$ | amortized, deterministic |

**Recompute.** A planar graph has at most $3n - 6$ edges by [Euler's formula](/euler-formula/). So the structure can keep a counter: while $m > 3n - 6$ the answer is no, and otherwise a linear-time test costs $O(n)$.

**Fixed embedding.** In a plane graph, the complement of a spanning tree is a spanning tree of the dual graph. Holm and Rotenberg (2017) store the primal and the dual tree with one shared Euler tour, so that "do $u$ and $v$ share a face?" becomes a query on dynamic trees.

**Fully dynamic with flips.** Holm and Rotenberg (2020) keep an embedding of a planar subgraph and, when an insertion does not fit, search for a short sequence of flips that makes room. Their analysis bounds the number of flips in an amortized sense, and each flip and each face query costs polylogarithmic time with the structure above, which gives $O(\log^3 n)$ amortized time per update.

## Bounds

**Upper bounds.** $O(\log^3 n)$ amortized per update, deterministic, fully dynamic; inverse Ackermann amortized for insertions only.

**Lower bounds.** We do not state a lower bound here. Since the upper bound is polylogarithmic, the open question is the exact power of $\log n$.

## Reductions

- **To biconnected and triconnected parts.** A graph is planar exactly when each [biconnected component](/dynamic-biconnectivity/) is planar, and the embeddings of a biconnected graph are described by the SPQR-tree of its triconnected parts. So dynamic algorithms keep these decompositions.
- **To dynamic trees.** In a fixed embedding, face queries reduce to queries on a primal and a dual spanning tree, as above.

## Applications

- **Graph drawing.** Interactive editors keep a drawing with no crossings while the user adds and removes edges, and need to know when this stops being possible.
- **Circuit and chip layout.** A single-layer wiring is a planar embedding; changes to the netlist insert and delete edges.
- **Subroutine.** Dynamic algorithms for planar graphs, such as the [planar separator](/planar-separator-theorem/) based ones, need to know that the graph is still planar.

## References
