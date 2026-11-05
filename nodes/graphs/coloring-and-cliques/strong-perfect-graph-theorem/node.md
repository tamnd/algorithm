---
tag: 8X5RV6
kind: theorem
slug: strong-perfect-graph-theorem
name: Strong perfect graph theorem
aliases:
- SPGT
area: graphs/coloring-and-cliques
level: research
summary: A graph is perfect if and only if it has no odd hole and no odd antihole.
prereqs: [perfect-graph, induced-subgraph, complement-graph]
see_also: [perfect-graph-theorem, lovasz-theta-function, chordal-graph, line-graph, bipartite-graph, konig-theorem, mycielski-graph, ellipsoid-method]
sources:
  - paper: doi:10.4007/annals.2006.164.51
    title: Maria Chudnovsky, Neil Robertson, Paul Seymour and Robin Thomas, The strong perfect graph theorem, Annals of Mathematics 164(1), 51 to 229 (2006)
    locator: the main theorem and the decomposition theorem for Berge graphs
  - paper: doi:10.1007/s00493-005-0012-8
    title: Maria Chudnovsky, Gérard Cornuéjols, Xinming Liu, Paul Seymour and Kristina Vušković, Recognizing Berge graphs, Combinatorica 25(2), 143 to 186 (2005)
    locator: the polynomial-time algorithm that tests for odd holes and odd antiholes
  - paper: "C. Berge, Färbung von Graphen, deren sämtliche bzw. deren ungerade Kreise starr sind, Wissenschaftliche Zeitschrift der Martin-Luther-Universität Halle-Wittenberg, Mathematisch-Naturwissenschaftliche Reihe 10, 114 (1961)"
    locator: the statement of the strong perfect graph conjecture
  - paper: doi:10.1016/0095-8956(72)90045-7
    title: L. Lovász, A characterization of perfect graphs, Journal of Combinatorial Theory, Series B 13(2), 95 to 98 (1972)
    locator: the characterization by ω(H) α(H) ≥ |V(H)|, which gives |V| = αω + 1 for minimally imperfect graphs
  - paper: "M. Chudnovsky, Berge trigraphs, Journal of Graph Theory 53(1), 1 to 55 (2006)"
    locator: the decomposition theorem without homogeneous pairs
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition, Elsevier, 2004
    locator: Chapter 3, Perfect graphs (minimally imperfect graphs and the strong conjecture)
---

The strong perfect graph theorem says that a graph is [perfect](/perfect-graph/) if and only if it contains no odd hole (an induced cycle of odd length at least 5) and no odd antihole (an induced [complement](/complement-graph/) of such a cycle). Berge conjectured it in 1961, and Chudnovsky, Robertson, Seymour and Thomas proved it in a paper of about 180 pages, announced in 2002 and published in 2006. It turns perfection, a condition about coloring every [induced subgraph](/induced-subgraph/), into a list of forbidden induced subgraphs, and together with the 2005 recognition algorithm it shows that perfect graphs can be recognized in polynomial time.

## Statement

A **hole** is an induced cycle of length at least 4, and an **antihole** is an induced subgraph whose complement is a hole. A graph is **Berge** if it has no odd hole and no odd antihole, that is, no induced $C_{2k+1}$ and no induced $\overline{C_{2k+1}}$ for any $k \ge 2$.

**Theorem (Chudnovsky, Robertson, Seymour and Thomas 2006).** A finite simple graph is perfect if and only if it is Berge.

Equivalently: the minimally imperfect graphs, the imperfect graphs all of whose proper induced subgraphs are perfect, are exactly the odd holes $C_5, C_7, C_9, \ldots$ and the odd antiholes $\overline{C_7}, \overline{C_9}, \ldots$ (note $\overline{C_5} \cong C_5$).

## In plain words

A network is called perfect when the number of colors it needs is always the size of its largest group of mutually linked points, also after deleting any points. Checking this directly means looking at every way of deleting points.

The theorem says there are only two kinds of obstacle. One is a ring of an odd number of points, at least five, with no shortcuts. The other is the mirror image of such a ring, where linked and unlinked are swapped. A network is perfect exactly when neither appears inside it. Showing that these obstacles are bad is easy; showing that nothing else is bad took forty years and a very long proof.

## Proof

**Perfect implies Berge.** Induced subgraphs of a perfect graph are perfect, so it suffices to show that odd holes and odd antiholes are not perfect.

- An odd hole $C_{2k+1}$, $k \ge 2$, has $\omega = 2$, since it has no triangle, and $\chi = 3$, since an odd cycle is not bipartite.
- An odd antihole $\overline{C_{2k+1}}$, $k \ge 2$, has $\omega = \alpha(C_{2k+1}) = k$ and $\alpha = \omega(C_{2k+1}) = 2$. Each color class is independent, so it has at most 2 vertices, and $\chi \ge \lceil (2k + 1)/2 \rceil = k + 1 > \omega$.

**Berge implies perfect: structure of the proof.** The converse is the content of the 2006 paper. Its plan is as follows.

1. *Minimal counterexample.* Suppose some Berge graph is imperfect, and take $G$ with the fewest vertices. Every proper induced subgraph of $G$ is Berge and so perfect, hence $G$ is minimally imperfect. The class of Berge graphs is closed under complement, because the complement of an odd hole is an odd antihole and conversely, and by the [perfect graph theorem](/perfect-graph-theorem/) so is the class of minimally imperfect graphs. Lovász's characterization adds that $|V(G)| = \alpha(G)\,\omega(G) + 1$.
2. *Basic classes are perfect.* Five classes of Berge graphs are shown to be perfect directly: [bipartite graphs](/bipartite-graph/); their complements, by [König's theorem](/konig-theorem/); [line graphs](/line-graph/) of bipartite graphs, by König's edge coloring theorem; their complements, by König's matching theorem; and double split graphs, a specific family checked by hand.
3. *Decomposition theorem.* Every Berge graph either belongs to a basic class or admits one of these decompositions: a proper 2-join in $G$ or in $\overline{G}$, a proper homogeneous pair, or a balanced skew partition. This is the main theorem of the paper and takes most of its length. It is proved by studying how a Berge graph can contain line graphs of bipartite subdivisions of $K_4$, prisms, and wheels, and by showing that each such configuration forces a decomposition unless the graph is basic. Chudnovsky later showed that homogeneous pairs are not needed.
4. *Minimally imperfect graphs do not decompose.* A minimally imperfect graph has no proper 2-join, in itself or in its complement (Cornuéjols and Cunningham 1985), no homogeneous pair (Chvátal and Sbihi 1987), and no balanced skew partition. The last statement is new in the 2006 paper; it strengthens Chvátal's star cutset lemma (1985) and uses step 1 and the parity condition in the word "balanced".
5. *Conclusion.* By step 2, $G$ is not basic, so by step 3 it decomposes, which contradicts step 4. Hence no Berge graph is imperfect. $\blacksquare$

The full arguments for steps 3 and 4 are in the Annals paper and are not reproduced here.

**Check on small graphs.** For all $2^{15} = 32768$ labeled graphs on 6 vertices, an exhaustive computation of $\chi$ and $\omega$ on every induced subgraph agrees with the theorem: exactly 1944 of them are imperfect, and these are exactly the ones with an induced $C_5$, the only odd hole or antihole that fits in 6 vertices. On 5 vertices the imperfect graphs are the 12 labeled copies of $C_5$.

## Consequences

- **The perfect graph theorem.** The Berge condition is symmetric under complement, so the theorem gives Lovász's [perfect graph theorem](/perfect-graph-theorem/) at once.
- **Recognition in polynomial time.** Chudnovsky, Cornuéjols, Liu, Seymour and Vušković (2005) test whether a graph is Berge in $O(n^9)$ time. With the theorem, this decides perfection in polynomial time, although perfection itself refers to all $2^n$ induced subgraphs. Testing for an odd hole alone was later shown to be polynomial too, by a separate algorithm (Chudnovsky, Scott, Seymour and Spirkl 2020).
- **Optimization.** Since perfect graphs satisfy $\alpha = \vartheta = \chi(\overline{G})$, the [Lovász theta function](/lovasz-theta-function/) computed by the [ellipsoid method](/ellipsoid-method/) yields maximum cliques, maximum independent sets and optimal colorings of Berge graphs in polynomial time. A purely combinatorial polynomial coloring algorithm for all Berge graphs is still not known.
- **Known perfect classes, uniformly.** [Chordal graphs](/chordal-graph/) have no holes at all and their complements have no antiholes of length at least 5, so they are Berge. The same quick check covers bipartite graphs, comparability graphs and many other classes that were first shown perfect one by one.
- **Structure theory.** The decomposition method, with 2-joins and skew partitions, became a main tool for graph classes defined by forbidden induced subgraphs, such as even-hole-free graphs and $\chi$-bounded classes.

## Tightness

Both kinds of forbidden subgraph are needed, and none can be dropped from the list, since every odd hole and odd antihole is minimally imperfect.

- $C_5$ has no odd antihole other than itself, and $C_7$ has none at all, but they are imperfect.
- $\overline{C_7}$ has no odd hole: an induced $C_5$ in $\overline{C_7}$ would be an induced $\overline{C_5} \cong C_5$ in $C_7$ on 5 vertices, but 5 vertices of $C_7$ induce a union of paths. Yet $\omega(\overline{C_7}) = 3$ and $\chi(\overline{C_7}) = 4$, so the antihole condition cannot be dropped.
- The condition is about induced subgraphs. The [Mycielski graphs](/mycielski-graph/) contain $C_5$ as an induced subgraph and are imperfect; a graph can contain $C_5$ as a non-induced subgraph, such as $K_5$, and still be perfect.
- Even holes are allowed: $C_4$, $C_6$ and every bipartite graph with long cycles are perfect.

## History

Claude Berge introduced perfect graphs in 1961, motivated by Shannon's zero-error capacity, and conjectured both the perfect graph theorem and this strong form. Lovász proved the weak form in 1972. For thirty years the strong conjecture was proved for many special classes, including planar graphs, claw-free graphs (Parthasarathy and Ravindra 1976), $K_4$-free graphs and bull-free graphs, and decomposition ideas such as Chvátal's star cutsets were developed. Chudnovsky, Robertson, Seymour and Thomas announced the proof in May 2002; it appeared in the Annals of Mathematics in 2006. The polynomial recognition algorithm followed in 2005.

## References
