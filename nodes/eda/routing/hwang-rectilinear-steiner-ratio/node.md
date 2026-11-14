---
tag: G78JW0
kind: theorem
slug: hwang-rectilinear-steiner-ratio
name: Hwang's rectilinear Steiner ratio
aliases:
- rectilinear Steiner ratio three halves
area: eda/routing
level: advanced
summary: The rectilinear minimum spanning tree of a point set is at most 3/2 times the length of its rectilinear Steiner minimal tree, and the bound is tight.
prereqs: [rectilinear-steiner-tree-problem, hanan-theorem, rectilinear-minimum-spanning-tree]
see_also: [steiner-ratio, rectilinear-steiner-tree-problem, hanan-theorem, rectilinear-minimum-spanning-tree, iterated-one-steiner, approximation-ratio, steiner-tree-problem, kou-markowsky-berman]
sources:
  - paper: doi:10.1137/0130013
    title: F. K. Hwang, On Steiner minimal trees with rectilinear distance, SIAM Journal on Applied Mathematics 30(1), 104 to 114, 1976
    locator: the shape of full rectilinear Steiner minimal trees with at least five terminals, and the proof of the bound 3/2 from it
  - paper: doi:10.1007/BF02067241
    title: Dana S. Richards and Jeffrey S. Salowe, A simple proof of Hwang's theorem for rectilinear Steiner minimal trees, Annals of Operations Research 33, 549 to 556, 1991
    locator: the short proof of the shape of full minimal trees with at least five terminals
  - paper: "Jeffrey S. Salowe, A simple proof of the planar rectilinear Steiner ratio, Operations Research Letters 12(4), 271 to 274, 1992"
    locator: the bound 3/2 derived from the shape of full trees (general locator)
  - paper: doi:10.1137/0114025
    title: M. Hanan, On Steiner's problem with rectilinear distance, SIAM Journal on Applied Mathematics 14(2), 255 to 265, 1966
    locator: the existence of a minimal tree on the grid of lines through the points
---

Hwang's theorem on the rectilinear Steiner ratio says that joining a set of points directly, by a minimum spanning tree in the L1 metric, costs at most 3/2 times the best network of horizontal and vertical wires with extra junction points. F. K. Hwang proved it in 1976. The constant is tight: for the four points of a plus sign, the spanning tree has length 6 and the best Steiner tree has length 4. In electronic design automation (EDA) the theorem is why the [rectilinear minimum spanning tree](/rectilinear-minimum-spanning-tree/) is a safe first estimate of the wire of a net, and why Steiner heuristics that start from it and never make it longer, such as [iterated 1-Steiner](/iterated-one-steiner/), are within 3/2 of the optimum. In the language of the [Steiner ratio](/steiner-ratio/), the ratio of the L1 plane is exactly 2/3.

## Statement

Let $P$ be a finite set of $n \ge 2$ points in the plane and $d$ the L1 distance. Let $\mathrm{RMST}(P)$ be the length of a minimum spanning tree of the complete graph on $P$ with lengths $d$, and $\mathrm{RSMT}(P)$ the length of a rectilinear Steiner minimal tree of $P$, a shortest connected union of horizontal and vertical segments that contains $P$. It exists by [Hanan's theorem](/hanan-theorem/).

**Theorem (Hwang 1976).** For every such $P$,
$$\mathrm{RMST}(P) \le \tfrac{3}{2}\, \mathrm{RSMT}(P).$$
The constant $3/2$ cannot be replaced by a smaller one.

Since every rectilinear Steiner tree $T$ of $P$ has $|T| \ge \mathrm{RSMT}(P)$, the theorem also gives $\mathrm{RMST}(P) \le \frac{3}{2} |T|$ for every such tree.

## In plain words

You want to join some pins with horizontal and vertical wire. The best network may use extra branch points that are not pins. The simple method joins pins directly to pins, which is the minimum spanning tree.

How much can the branch points save? At most a third of the simple length. Said the other way, the simple method is never more than one and a half times the best.

For the plus sign, four pins around a center, the branch point in the center saves exactly a third: each pin needs one unit of wire to the center, 4 in total, while joining pins to pins needs three wires of length 2, which is 6.

For three pins the saving is at most a quarter. The hard part of the proof is the case of five or more pins, where Hwang first showed what the best trees look like.

## Proof

The proof is by induction on $n$. It splits a minimal tree at pins of degree two or more, proves the small cases directly, and uses Hwang's description of the shape of minimal trees for the large case. Write $\mathrm{dist}_T(u, v)$ for the length of the path between $u$ and $v$ inside a tree $T$, so $d(u, v) \le \mathrm{dist}_T(u, v)$, because the path is a rectilinear curve from $u$ to $v$.

**Lemma 1 (leaves are terminals).** In a rectilinear Steiner minimal tree of $P$, viewed as a graph whose vertices are the points of $P$, the junctions and the bends, every leaf is a point of $P$.

*Proof.* A leaf that is not in $P$ can be removed with its edge, which has positive length, and the rest still contains $P$. This gives a shorter tree, a contradiction. $\square$

**Lemma 2 (splitting at a terminal).** Suppose some rectilinear Steiner minimal tree $T$ of $P$ has a point $p \in P$ of degree at least 2. Then there are sets $P', P''$ with $P' \cup P'' = P$, $P' \cap P'' = \{p\}$ and $2 \le |P'|, |P''| \le n - 1$, and trees $T', T''$ of these sets with $|T'| + |T''| = |T|$. Moreover $\mathrm{RMST}(P) \le \mathrm{RMST}(P') + \mathrm{RMST}(P'')$.

*Proof.* Split the branches of $T$ at $p$ into two non-empty groups. Each group, together with $p$, is a tree. By Lemma 1 each branch contains a leaf, which is a point of $P$ other than $p$. So each part contains $p$ and at least one more point, and misses the points of the other part, which gives the bounds on the sizes. The two parts share only $p$, so their lengths add up to $|T|$. The union of a spanning tree of $P'$ and a spanning tree of $P''$ is connected, since both contain $p$, and it has $(|P'| - 1) + (|P''| - 1) = n - 1$ edges, so it is a spanning tree of $P$. $\square$

**Lemma 3 (at most four terminals, all leaves).** Let $T$ be a rectilinear Steiner tree of $P$ with $n \in \{2, 3, 4\}$ in which every point of $P$ is a leaf. Then $\mathrm{RMST}(P) \le \frac{3}{2} |T|$.

*Proof.* Remove the vertices of degree 2 that are not in $P$ by joining their two edges into one path, so the tree has leaves $P$ and inner vertices of degree at least 3. For $n = 2$ the tree is a path, and $\mathrm{RMST}(P) = d(a, b) \le |T|$.

For $n = 3$ the tree has one inner vertex $s$, with paths of lengths $\alpha \le \beta \le \gamma$ to the leaves $a, b, c$. The spanning tree $\{ab, ac\}$ has length at most $(\alpha + \beta) + (\alpha + \gamma) = |T| + \alpha \le |T| + |T|/3 = \frac{4}{3}|T|$.

For $n = 4$ the tree is either a star with one inner vertex and paths $\alpha, \beta, \gamma, \delta$ to the leaves, or it has two inner vertices $s_1, s_2$ joined by a path of length $\mu$, with leaves $a, b$ at $s_1$ by paths $\alpha, \beta$ and leaves $c, e$ at $s_2$ by paths $\gamma, \delta$. Treat the star as the second case with $\mu = 0$ and any pairing of the leaves. Let $x$ be the one of $a, b$ with the shorter path to $s_1$, and $y$ the one of $c, e$ with the shorter path to $s_2$. The spanning tree $\{ab, ce, xy\}$ has length at most
$$(\alpha + \beta) + (\gamma + \delta) + \big(\min(\alpha, \beta) + \mu + \min(\gamma, \delta)\big) \le |T| + \frac{\alpha + \beta}{2} + \frac{\gamma + \delta}{2} \le \frac{3}{2} |T|. \qquad \square$$

**Lemma 4 (Hwang's shape theorem, cited).** Let $|P| \ge 5$, and suppose that no rectilinear Steiner minimal tree of $P$ has a point of $P$ of degree 2 or more. Then some rectilinear Steiner minimal tree of $P$ has all its Steiner points, except at most one, on one straight line $\ell$, and the edges at the Steiner points on $\ell$ that leave $\ell$ go to the two sides of $\ell$ in alternation.

This is the theorem of Hwang (1976). Richards and Salowe (1991) gave a short direct proof. We do not repeat it here.

**Lemma 5 (the bound for these shapes, cited).** For a tree of the shape of Lemma 4, $\mathrm{RMST}(P) \le \frac{3}{2} |T|$.

*Sketch.* The terminals hang from the line $\ell$ by legs that alternate between the two sides. A spanning tree is built from edges between terminals of nearby legs, and its length is compared with the tree segment by segment, with a separate count for the one Steiner point off $\ell$. Hwang (1976) does this computation, and Salowe (1992) gives a shorter one. This page does not give the computation in full. $\square$

**Proof of the theorem.** By induction on $n$. For $n = 2$, $\mathrm{RMST}(P) = d(a, b) = \mathrm{RSMT}(P)$. Let $n \ge 3$ and let $T$ be a rectilinear Steiner minimal tree of $P$.

If some minimal tree $T$ has a point of $P$ of degree at least 2, Lemma 2 gives $P', P''$ and $T', T''$. The tree $T'$ joins $P'$, so $\mathrm{RSMT}(P') \le |T'|$, and the same holds for $T''$. By induction,
$$\mathrm{RMST}(P) \le \mathrm{RMST}(P') + \mathrm{RMST}(P'') \le \tfrac{3}{2}\big(|T'| + |T''|\big) = \tfrac{3}{2}\, \mathrm{RSMT}(P).$$

Otherwise every point of $P$ is a leaf of every minimal tree. For $n \le 4$ Lemma 3 gives the bound. For $n \ge 5$ Lemmas 4 and 5 give it. $\square$

**Tightness.** For $P = \{(1, 0), (0, 1), (2, 1), (1, 2)\}$, every two points are at distance 2, so every spanning tree has length 6. The star from $(1, 1)$ has length 4, and no tree is shorter, since every tree must reach from $x = 0$ to $x = 2$ and from $y = 0$ to $y = 2$, which needs $2 + 2 = 4$. So $\mathrm{RMST}(P) / \mathrm{RSMT}(P) = 6/4 = 3/2$. $\square$

What is proved on this page in full: the reduction to trees whose terminals are all leaves, the bound for at most four terminals, and the tightness. The case of five or more terminals rests on Lemmas 4 and 5, which are cited from Hwang (1976), Richards and Salowe (1991) and Salowe (1992).

## Consequences

- **A 3/2 approximation.** The [rectilinear minimum spanning tree](/rectilinear-minimum-spanning-tree/), found in $O(n \log n)$ time, is a 3/2-approximation of the [rectilinear Steiner tree problem](/rectilinear-steiner-tree-problem/), in the sense of the [approximation ratio](/approximation-ratio/).
- **Heuristics that start from the MST.** Any method that starts from the spanning tree and never makes it longer is within 3/2 of the optimum. This covers [iterated 1-Steiner](/iterated-one-steiner/) and edge-based Steiner heuristics, and it is often the only worst-case guarantee they have.
- **The Steiner ratio of the L1 plane.** The [Steiner ratio](/steiner-ratio/) $\inf_P \mathrm{RSMT}(P)/\mathrm{RMST}(P)$ of the L1 plane is exactly 2/3. For graphs the same ratio is only 1/2, which is why the spanning tree method of [Kou, Markowsky and Berman](/kou-markowsky-berman/) for the [Steiner tree problem](/steiner-tree-problem/) in graphs only promises a factor 2.
- **Wire estimates.** In placement, the spanning tree length of a net is at most 3/2 times its best Steiner length, so it can be used as a pessimistic estimate with a known error.

## Tightness

- **The plus sign.** The four points around $(1, 1)$ reach the ratio 3/2 exactly, as shown in the proof.
- **Three points.** For $n = 3$ the ratio is at most 4/3, by Lemma 3. It is reached by $(0, 0)$, $(2, 0)$ and $(1, 1)$: the spanning tree has length $2 + 2 = 4$ and the best tree has length 3, the half perimeter of the bounding box.
- **Two points.** For $n = 2$ the ratio is 1.
- **Which small sets are tight.** Let $n \le 4$. If a minimal tree has a terminal of degree 2 or more, Lemma 2 splits $P$ into parts of at most 3 points, and the ratio is at most 4/3. Otherwise the bound of Lemma 3 is reached only if $\mu = 0$ and, for every pairing of the leaves, the two legs of each pair are equal. So the ratio 3/2 needs a minimal tree that is a star with four legs of equal length, as in the plus sign. This is a necessary condition, not a sufficient one.

## History

M. Hanan studied the rectilinear Steiner problem in 1966 and showed that a minimal tree can be found on the grid of lines through the points. E. N. Gilbert and H. O. Pollak defined the Steiner ratio in 1968 for the Euclidean plane. F. K. Hwang proved in 1976 that the ratio of the L1 plane is 2/3, by first describing the shape of full minimal trees with five or more terminals. Dana Richards and Jeffrey Salowe gave a short proof of the shape theorem in 1991, and Salowe gave a short proof of the ratio in 1992. In VLSI routing the result became the standard justification for spanning tree estimates and for Steiner heuristics that improve on the spanning tree.

## References
