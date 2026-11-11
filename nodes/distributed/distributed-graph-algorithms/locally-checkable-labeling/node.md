---
tag: FKA20W
kind: definition
slug: locally-checkable-labeling
name: Locally checkable labeling (LCL)
aliases:
- LCL problems
- locally checkable problems
area: distributed/distributed-graph-algorithms
level: advanced
summary: A problem on bounded-degree graphs with finite labels whose solutions can be checked in constant-radius balls. Naor and Stockmeyer defined it; its round complexities have gaps.
prereqs: [local-model, round-complexity]
see_also: [sinkless-orientation, distributed-mis, distributed-vertex-coloring, ruling-set, network-decomposition, linial-coloring-lower-bound, ring-coloring, round-elimination]
sources:
  - paper: doi:10.1137/S0097539793254571
    title: Moni Naor and Larry Stockmeyer, What can be computed locally?, SIAM Journal on Computing 24(6), 1995
    locator: pp. 1259 to 1277 (the definition of LCLs, order-invariant algorithms by a Ramsey argument, randomization does not help in constant time, undecidability of constant-time solvability; also STOC 1993, doi:10.1145/167088.167149)
  - paper: doi:10.1137/17M1117537
    title: Yi-Jun Chang, Tsvi Kopelowitz and Seth Pettie, An exponential separation between randomized and deterministic complexity in the LOCAL model, SIAM Journal on Computing 48(1), 2019
    locator: pp. 122 to 143 (the gap from o(log_Delta n) to O(log* n) for deterministic algorithms, and randomized complexity at n at least deterministic complexity at sqrt(log n))
  - paper: doi:10.1137/17M1157957
    title: Yi-Jun Chang and Seth Pettie, A time hierarchy theorem for the LOCAL model, SIAM Journal on Computing 48(1), 2019
    locator: pp. 33 to 69 (the omega(1) to o(log log* n) gap on general bounded-degree graphs, the speedup of sublogarithmic randomized algorithms to the LLL complexity, and the gaps on trees; also FOCS 2017, doi:10.1109/FOCS.2017.23)
  - paper: doi:10.1109/FOCS.2018.00069
    title: Mohsen Ghaffari, David G. Harris and Fabian Kuhn, On derandomizing local distributed algorithms, FOCS 2018
    locator: pp. 662 to 673 (network decomposition is complete for derandomizing poly(log n)-round algorithms for LCL-type problems)
  - paper: doi:10.1145/3357713.3384298
    title: Václav Rozhoň and Mohsen Ghaffari, Polylogarithmic-time deterministic network decomposition and distributed derandomization, STOC 2020
    locator: pp. 350 to 363 (the decomposition that completes the derandomization)
  - paper: doi:10.1145/3087801.3087833
    title: Sebastian Brandt, Juho Hirvonen, Janne H. Korhonen, Tuomo Lempiäinen, Patric R. J. Östergård, Christopher Purcell, Joel Rybicki, Jukka Suomela and Przemysław Uznański, LCL problems on grids, PODC 2017
    locator: pp. 101 to 110 (the classes O(1), Theta(log* n) and Theta(n) on paths and cycles, and grids)
---

A locally checkable labeling (LCL) problem asks each node of a bounded-degree graph to output a label from a finite set, so that a solution is correct exactly when every ball of a fixed constant radius looks correct. Proper colouring with a fixed number of colours, [maximal independent set](/distributed-mis/), maximal matching and [sinkless orientation](/sinkless-orientation/) are LCLs; approximating a minimum vertex cover is not. Naor and Stockmeyer (1995) introduced the class, and much of distributed complexity theory is about which round complexities LCLs can have in the [LOCAL model](/local-model/).

## Definition

Fix a constant $\Delta$ and consider graphs of maximum degree at most $\Delta$. An **LCL problem** is a tuple $\Pi = (\Sigma_{\mathrm{in}}, \Sigma_{\mathrm{out}}, r, \mathcal{C})$, where:

- $\Sigma_{\mathrm{in}}$ and $\Sigma_{\mathrm{out}}$ are finite sets of input and output labels;
- $r$ is a constant, the **checking radius**;
- $\mathcal{C}$ is a finite set of **allowed neighbourhoods**: graphs of radius at most $r$ around a marked centre, of maximum degree at most $\Delta$, whose nodes carry one input and one output label.

An output labelling $\lambda : V \to \Sigma_{\mathrm{out}}$ of a graph $G$ with input labels is **valid** if, for every node $v$, the ball of radius $r$ around $v$, with its labels and with $v$ marked as the centre, is isomorphic to a member of $\mathcal{C}$. Labels may also sit on edges or on half-edges (a node and one of its ports); the definition is the same with the labels of the ball.

The identifiers are not part of the check: a checker sees only the graph and the labels. Given an LCL, the **deterministic complexity** is the least $T(n)$ such that some LOCAL algorithm, on every graph of $n$ nodes with distinct identifiers from $\{1, \dots, \mathrm{poly}(n)\}$, outputs a valid labelling after $T(n)$ rounds. The **randomized complexity** asks for a valid labelling with probability at least $1 - 1/n$.

Three facts follow from the definition. First, the number of allowed neighbourhoods is finite, since $\Delta$, $r$ and the label sets are constants. Second, if an algorithm fails, some node can see it within distance $r$, so a failure is local. Third, a valid labelling may not exist for some graphs; most results only consider LCLs and graph classes where it always exists.

## Examples and non-examples

- **Proper $k$-colouring** for a constant $k$: $\Sigma_{\mathrm{out}} = \{1, \dots, k\}$, $r = 1$, and a ball is allowed if the centre's colour differs from its neighbours'. On cycles, 3-colouring takes $\Theta(\log^* n)$ rounds ([Cole-Vishkin](/cole-vishkin/) and [Linial's lower bound](/linial-coloring-lower-bound/)), while 2-colouring of even cycles takes $\Theta(n)$.
- **$(\Delta + 1)$-colouring and $\Delta$-colouring** with constant $\Delta$. They differ sharply: $(\Delta + 1)$-colouring takes $O(\log^* n)$ rounds on bounded-degree graphs, while $\Delta$-colouring of trees has the same exponential gap between randomness and determinism as sinkless orientation.
- **MIS**: one bit per node, $r = 1$; a node with bit 1 has no neighbour with bit 1, and a node with bit 0 has a neighbour with bit 1.
- **Maximal matching**: each node outputs the port of its partner or "none"; with $r = 1$ (or 2, depending on where the labels sit) one checks that the choices agree and that no edge has two unmatched ends.
- **$(\alpha, \beta)$-[ruling sets](/ruling-set/)** with constant $\alpha$ and $\beta$, with $r = \max(\alpha - 1, \beta)$.
- **Sinkless orientation**: labels on half-edges ("out" or "in"), checked at each node and each edge.
- **Weak 2-colouring**: every node has a neighbour of the other colour. Naor and Stockmeyer showed that it can be solved in a constant number of rounds on graphs where every degree is odd, which was one of the first non-trivial constant-time results.
- **Non-example: approximation.** "A vertex cover of size at most twice the minimum" is not locally checkable, because the minimum is a global quantity. The covering part is local, but the size bound is not.
- **Non-example: global structure.** A spanning tree, a leader, or the value of $n$ cannot be checked within a constant radius with finite labels.
- **Non-example: unbounded labels or degrees.** $(\Delta + 1)$-colouring of graphs with unbounded $\Delta$ is checkable in radius 1, but it is not an LCL in the strict sense, since the label set grows; many results still extend to it.

## Related definitions

- **Order-invariant algorithms.** An algorithm is order-invariant if its output depends only on the relative order of the identifiers in a node's view, not on their values. Naor and Stockmeyer showed by a Ramsey argument that a constant-time algorithm for an LCL can be made order-invariant, and deduced that **randomization does not help in constant time**: if an LCL has a constant-time randomized algorithm with small failure probability, it has a constant-time deterministic one. They also showed that it is undecidable in general whether an LCL can be solved in constant time.
- **Gaps on general bounded-degree graphs.** For deterministic algorithms, the complexity of an LCL is either $O(1)$, or between $\Omega(\log \log^* n)$ and $O(\log^* n)$, or $\Omega(\log n)$. The first gap, from $\omega(1)$ to $o(\log \log^* n)$, is from Chang and Pettie (2017), with the method of Naor and Stockmeyer. The second, from $\omega(\log^* n)$ to $o(\log n)$, is from Chang, Kopelowitz and Pettie (2016): a deterministic algorithm with $o(\log_\Delta n)$ rounds can be sped up to $O(\log^* n)$. For randomized algorithms, the complexity is either $O(\log^* n)$ or $\Omega(\log \log n)$, and Chang and Pettie showed that a randomized algorithm with $o(\log n)$ rounds can be sped up to the complexity of the distributed Lovász local lemma.
- **Paths, cycles and trees.** On paths and cycles, every LCL has complexity $O(1)$, $\Theta(\log^* n)$ or $\Theta(n)$, for both deterministic and randomized algorithms, and the class can be decided from the problem description. On bounded-degree trees, the deterministic complexities are $O(1)$, $\Theta(\log^* n)$, $\Theta(\log n)$ and $\Theta(n^{1/k})$ for integers $k \ge 1$, with gaps between them; the $\Theta(n^{1/k})$ classes are the time hierarchy of Chang and Pettie.
- **Randomized versus deterministic.** Chang, Kopelowitz and Pettie showed that for LCLs the randomized complexity on $n$ nodes is at least the deterministic complexity on $\sqrt{\log n}$ nodes, so a deterministic $\Omega(\log n)$ bound gives a randomized $\Omega(\log \log n)$ bound. Sinkless orientation and $\Delta$-colouring show that this exponential gap occurs.
- **Derandomization.** Ghaffari, Harris and Kuhn (2018) showed that a deterministic $\mathrm{poly}(\log n)$-round [network decomposition](/network-decomposition/) makes every LCL with a $\mathrm{poly}(\log n)$ randomized algorithm solvable deterministically in $\mathrm{poly}(\log n)$ rounds. Rozhoň and Ghaffari (2020) gave such a decomposition, so for LCLs, $\mathrm{poly}(\log n)$ randomized and deterministic complexity coincide.
- **SLOCAL.** In the SLOCAL model, nodes are processed one at a time in an adversarial order and each reads and writes within a radius. MIS and colouring have locality 1 there; sinkless orientation separates LOCAL from SLOCAL.
- **Round elimination.** For LCLs given on half-edges with node and edge constraints, [round elimination](/round-elimination/) maps a problem $\Pi$ to a problem whose complexity is exactly one round less, on high-girth regular graphs. It gives the lower bounds for sinkless orientation, maximal matching and ruling sets.
- **Locally checkable proofs.** A related idea: a global property, such as "this is a spanning tree", becomes locally checkable when nodes get extra certificate labels. This is the setting of proof labelling schemes, where the labels may grow with $n$.

## References
