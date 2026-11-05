---
tag: QGCV7H
kind: theorem
slug: dynamic-connectivity-lower-bound
name: Dynamic connectivity lower bounds
aliases:
- Dynamic connectivity lower bound
- Patrascu-Demaine connectivity bound
- Patrascu-Demaine lower bounds
- logarithmic lower bounds for dynamic connectivity
area: graphs/dynamic-graphs
level: research
summary: Logarithmic lower bounds in the cell-probe model for dynamic connectivity-type problems.
prereqs: [dynamic-connectivity, cell-probe-model, amortized-update-time]
see_also: [dynamic-tree, dynamic-tree-path-queries, holm-de-lichtenberg-thorup, link-cut-tree, dynamic-minimum-spanning-tree, dynamic-biconnectivity, omv-conjecture]
sources:
  - paper: doi:10.1137/S0097539705447256
    title: Mihai Patrascu and Erik D. Demaine, Logarithmic lower bounds in the cell-probe model, SIAM Journal on Computing 35(4), 932 to 963 (2006)
    locator: Section 1 (the statement of the trade-offs for partial sums and dynamic connectivity, and the list of consequences), the hard instance with permutations on a grid, and the information transfer method
  - paper: doi:10.1007/PL00009228
    title: Michael L. Fredman and Monika R. Henzinger, Lower bounds for fully dynamic connectivity problems in graphs, Algorithmica 22(3), 351 to 362 (1998)
    locator: the main theorem (Omega(log n / log log n) per operation in the cell-probe model)
  - paper: doi:10.1145/73007.73040
    title: Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of STOC 1989, 345 to 354
    locator: the chronogram method for dynamic lower bounds
  - paper: doi:10.1145/502090.502095
    title: Jacob Holm, Kristian de Lichtenberg and Mikkel Thorup, Poly-logarithmic deterministic fully-dynamic algorithms for connectivity, minimum spanning tree, 2-edge, and biconnectivity, Journal of the ACM 48(4), 723 to 760 (2001)
    locator: the main theorem for connectivity (the matching upper bounds up to a logarithmic factor)
---

The dynamic connectivity lower bound of Pătraşcu and Demaine (2004, journal 2006) states that every data structure for [dynamic connectivity](/dynamic-connectivity/) in the [cell-probe model](/cell-probe-model/) needs $\Omega(\log n)$ amortized time per operation, for the larger of the update time and the query time. The bound holds even when the graph is always a union of disjoint paths, and also for randomized structures. It comes as a trade-off curve between update and query time, which is tight for forests and nearly tight for general graphs. It replaced the earlier bound of $\Omega(\log n / \log\log n)$ by Fredman and Henzinger.

## Statement

**Theorem (Pătraşcu and Demaine).** Consider a data structure in the cell-probe model, with cells of $\Theta(\log n)$ size, that keeps an undirected graph on $n$ vertices under edge insertions and deletions and answers queries "are $u$ and $v$ connected?". Let $t_u$ be its amortized update time and $t_q$ its amortized query time, both counted in cell probes. Then

$$t_q \log\frac{t_u}{t_q} = \Omega(\log n) \qquad \text{and} \qquad t_u \log\frac{t_q}{t_u} = \Omega(\log n),$$

where each logarithm is taken as at least 1. In particular, $\max(t_u, t_q) = \Omega(\log n)$. The bounds hold for graphs that are disjoint unions of paths, and also for randomized structures.

## In plain words

A program keeps a network whose links change, and it must answer whether two points are joined. This theorem says that no program can do every change and every answer in a constant number of steps as the network grows. It always needs about as many steps as the number of digits in the size of the network, when you count only the reads and writes of memory and nothing else.

The bound also shows a trade. A program can make changes cheaper only by making answers dearer, and the other way around. Known programs for networks with no loops reach this bound, and programs for general networks come close.

## Proof

The following is a sketch. The full proof is in Pătraşcu and Demaine (2006), in the sections on the permutation problem and on the information transfer method.

**Hard instance.** Arrange the $n$ vertices in a grid of $\sqrt n$ columns of $\sqrt n$ vertices each. Between column $i$ and column $i + 1$, put a perfect matching, which is a permutation $\pi_i$ of $\{1, \ldots, \sqrt n\}$. The graph is a union of $\sqrt n$ disjoint paths from the first column to the last. The path that starts at row $j$ ends at row $(\pi_{\sqrt n - 1} \circ \cdots \circ \pi_1)(j)$. Two operations act on this graph:

- **update**$(i, \pi)$: replace $\pi_i$ by $\pi$. This takes $O(\sqrt n)$ edge deletions and insertions.
- **verify**$(k, \sigma)$: is $\pi_k \circ \cdots \circ \pi_1 = \sigma$? Each path meets column $k + 1$ exactly once, so this holds exactly when, for each row $j$, the vertex in row $j$ of the first column is connected to the vertex in row $\sigma(j)$ of column $k + 1$. This takes $\sqrt n$ connectivity queries.

So a connectivity structure with times $t_u$ and $t_q$ solves this permutation problem with $O(\sqrt n\, t_u)$ time per update and $O(\sqrt n\, t_q)$ per verification. It suffices to show that the permutation problem needs $\Omega(\sqrt n \log n)$ cell probes per operation in the balanced case.

**Information transfer.** Take a long random sequence of $m$ operations, alternating between random updates and verifications of the true prefix composition. Build a balanced binary tree over the time line, with the operations as leaves. Charge each cell probe that reads a cell to the lowest common ancestor of the time when the cell was last written and the time when it is read. Each read is charged to exactly one node. At a node with left subtree $L$ and right subtree $R$ of $k$ operations each, the verifications in $R$ depend on the updates in $L$. Each random permutation carries $\log_2 (\sqrt n)! = \Theta(\sqrt n \log n)$ units of information. An encoding argument shows that the cells written in $L$ and read in $R$ must carry $\Omega(k \sqrt n \log n)$ units, so there are $\Omega(k \sqrt n)$ such cells, as each cell holds $O(\log n)$ units.

The step that needs care is that a verification answers only yes or no, so it reveals very little information by itself. Pătraşcu and Demaine handle this by an encoding in which the decoder tries candidate permutations and uses the probes of the verification as a certificate that separates the right answer from the wrong ones.

**Summing.** Each level of the tree has nodes whose subtrees together cover the time line, so each level receives $\Omega(m \sqrt n)$ probes. With $\Theta(\log m)$ levels and $m$ polynomial in $n$, the total is $\Omega(m \sqrt n \log n)$ probes, which is $\Omega(\sqrt n \log n)$ per operation of the permutation problem, and so $\Omega(\log n)$ per edge update or connectivity query. The unbalanced trade-offs come from a tree with a higher branching factor, chosen from the ratio of $t_u$ and $t_q$. $\square$

## Consequences

- **Problems that contain connectivity.** By reductions, the same $\Omega(\log n)$ bound holds for [dynamic minimum spanning trees](/dynamic-minimum-spanning-tree/), [dynamic biconnectivity](/dynamic-biconnectivity/) and 2-edge connectivity, [dynamic bipartiteness](/dynamic-bipartiteness/), [dynamic reachability](/dynamic-reachability/) in directed graphs, and the [dynamic tree](/dynamic-tree/) type.
- **Forests and paths.** Since the hard instance is a union of paths, connectivity in [dynamic trees](/dynamic-tree/) and the [path queries](/dynamic-tree-path-queries/) on them also need $\Omega(\log n)$.
- **Partial sums.** The same paper proves the matching bound for prefix sums over an array under point updates.
- **No constant-time structure.** Unlike [incremental connectivity](/incremental-connectivity/), which takes $O(\alpha(n))$ amortized time per operation, the fully dynamic problem cannot be solved in nearly constant time per operation.

## Tightness

- **Forests.** [Link-cut trees](/link-cut-tree/) and Euler tour trees answer connectivity in a dynamic forest in $O(\log n)$ time per operation, so the bound is tight for forests.
- **General graphs.** The algorithm of [Holm, de Lichtenberg and Thorup](/holm-de-lichtenberg-thorup/) takes $O(\log^2 n)$ amortized time per update and $O(\log n / \log\log n)$ per query, and later work lowered the update time further. So for general graphs the gap to the lower bound is at most a factor near $\log n$ for amortized bounds, and larger for worst-case bounds.
- **Model.** The bound is for the cell-probe model, so it holds for every algorithm on a word RAM with words of $\Theta(\log n)$ size, whatever instructions it uses.

## History

Fredman and Saks (1989) introduced the chronogram method for dynamic cell-probe lower bounds. Fredman and Henzinger (1998) used it to prove $\Omega(\log n / \log\log n)$ for dynamic connectivity. For many years no dynamic problem had a larger cell-probe lower bound, and Pătraşcu and Demaine describe this as a long-standing barrier. Pătraşcu and Demaine broke it at STOC 2004 with the information transfer method, and the journal version appeared in 2006. The method has since been used for many other dynamic problems.

## References
