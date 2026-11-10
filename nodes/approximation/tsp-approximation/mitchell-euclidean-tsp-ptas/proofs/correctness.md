---
title: Bridges make cuts m-perfect, the conversion is m-guillotine, and a sketch of Mitchell's length bound and dynamic program
proves: [correctness]
status: sketch
---

A *graph* here is a finite set $E$ of line segments in the plane, and $L(E)$ is their total length. A *window* is a closed axis-parallel rectangle $W$. A *cut* of $W$ is a horizontal or vertical line $\ell$ through the inside of $W$. The set $\ell \cap W \cap \bigcup E$ is a union of $k$ disjoint *components* $\xi_1, \ldots, \xi_k$, in order along $\ell$; each is a point or a segment. For an integer $m \ge 1$, the *m-span* $\sigma_m(\ell)$ is empty if $k \le 2(m - 1)$, and otherwise it is the segment of $\ell$ from the low end of $\xi_m$ to the high end of $\xi_{k-m+1}$. The cut is *m-perfect* if $\sigma_m(\ell) \subseteq \bigcup E$. $E$ is *m-guillotine* in $W$ if no vertex of $E$ lies strictly inside $W$, or if some m-perfect cut $\ell$ through a vertex coordinate splits $W$ into two windows in which $E$ is m-guillotine. The checker of the code uses this definition.

Lemmas 1 to 3 have full proofs and are what the code relies on. Part B is a sketch of Mitchell's theorems, after Mitchell (1999); its constants are not checked here.

## Part A. Bridges and the conversion

**Lemma 1 (a bridge makes a cut m-perfect).** Add the segment $\sigma_m(\ell)$, the *bridge*, to $E$. Then $\ell$ is m-perfect for the new graph, and the cost is $|\sigma_m(\ell)|$ minus the part already covered.

*Proof.* If the span is empty there is nothing to do. Otherwise the bridge runs from the low end of $\xi_m$ to the high end of $\xi_{k-m+1}$, so the components $\xi_m, \ldots, \xi_{k-m+1}$ merge into one component $\xi^*$. The new components are $\xi_1, \ldots, \xi_{m-1}, \xi^*, \xi_{k-m+2}, \ldots, \xi_k$, which are $2m - 1$ components. The $m$-th from each end is $\xi^*$, so the new span is $\xi^*$, which lies in the new graph. $\square$

**Lemma 2 (bridges meet other cut lines only at old points).** The two ends of a bridge are points of $E$ before the bridge was added.

*Proof.* The ends are the low end of $\xi_m$ and the high end of $\xi_{k-m+1}$, and components are subsets of $\bigcup E$. $\square$

The conversion works on a stack of windows, starting with the bounding box. For a window with a vertex strictly inside, it picks a cut through such a vertex, adds the bridge of Lemma 1, and pushes the two halves.

**Lemma 3 (the conversion stops, and its result is m-guillotine).** The conversion stops, the final graph $E_G \supseteq E$ is m-guillotine in the bounding box, and $L(E_G) - L(E)$ is at most the sum of the spans it used.

*Proof.* *Stopping.* A bridge made in window $W$ lies on the cut of $W$, so its ends are on the boundary of both halves, not strictly inside. A bridge made later in another window lies in that window, whose inside does not meet the inside of $W$, so its ends are not strictly inside $W$. Thus the set of vertices strictly inside a window never grows after the window is made. The vertex on the cut is not strictly inside either half, so each half has fewer of them than its parent, and every branch ends.

*m-guillotine.* By induction from the windows with no inner vertex, which are m-guillotine by definition. Take a window $W$ with its cut $\ell$. Right after its bridge is added, $\ell$ is m-perfect by Lemma 1. A later bridge made inside $W$ that is parallel to $\ell$ lies on a different line and does not meet $\ell$. A later bridge across $\ell$, or one made in a window outside $W$, meets $\ell \cap W$ at most at one end, which by Lemma 2 was already a point of the graph. So later bridges do not change $\ell \cap W \cap \bigcup E$, and $\ell$ stays m-perfect in $E_G$. The halves are m-guillotine by induction, so $W$ is.

*Length.* Each bridge costs at most its span. $\square$

The test file checks Lemma 3 on 60 seeded random tours for $m = 1, 2, 3$ with the exhaustive checker, and checks the classic pinwheel of five rectangles, which is not 1-guillotine.

**The guarantee of the code.** The code returns the order $A$ whose length plus bridge length is least. For an optimal order $H$, this gives $L(A) \le L(A) + \text{bridges}(A) \le \text{OPT} + \text{bridges}(H)$. So the ratio is at most $1 + \text{bridges}(H) / \text{OPT}$. The code does not prove a bound on bridges; it measures that $\text{bridges}(H) \le \frac{\sqrt{2}}{m}\,\text{OPT}$ on its test instances, which is the bound of Part B.

## Part B. Mitchell's theorems (sketch)

**A favorable cut.** In a window $W$, let $R_V$ be the set of points that lie in the m-span of their vertical line, and $R_H$ the same for horizontal lines. Then $\text{area}(R_V) = \int |\sigma_m(x)|\,dx$ over the vertical cuts and $\text{area}(R_H) = \int |\sigma_m(y)|\,dy$. Suppose $\text{area}(R_V) \le \text{area}(R_H)$. Since $\text{area}(R_H)$ is also the integral over $x$ of the length of $R_H$ on the vertical line at $x$, some vertical cut has $|\sigma_m(x)|$ at most the length of $R_H$ on it. This step is a full proof by Fubini's theorem. Each point of $R_H$ on that line has at least $m$ edges to its left and $m$ to its right on its horizontal line. So the span can be paid by charging $1/m$ of its length to the vertical extent of the $m$ edges nearest on one side.

**Length theorem (Mitchell 1999).** For each graph $E$ in a box and each $m \ge 1$ there is an m-guillotine graph $E_G \supseteq E$ with $L(E_G) \le (1 + \frac{\sqrt{2}}{m}) L(E)$. *Idea.* Use favorable cuts recursively. A piece of edge is charged at most once from each side in each direction, because after a cut it is within $m$ components of the new window boundary. So the total charge is at most $\frac{1}{m}$ times the sum of the $x$ and $y$ extents of the edges, and that sum is at most $\sqrt{2}\, L(E)$. The full proof deals with cuts that are not at vertex coordinates.

**The TSP.** Let $E$ be an optimal tour and $E_G$ the graph of the length theorem. Doubling each bridge gives a connected graph with even degrees at every point, of length at most $(1 + \frac{2\sqrt{2}}{m})\,\text{OPT}$ in this sketch, and its Euler circuit shortcuts to a tour. So it is enough to find a least-length m-guillotine graph of this kind, which has ratio $1 + O(1/m)$.

**The dynamic program.** A subproblem is a window whose sides lie on the $O(n)$ lines $x = x_i$ and $y = y_i$ through the points, so there are $O(n^4)$ windows. Its boundary state lists, for each side, the bridge on it and at most $2m$ edges that cross it outside the bridge, each given by its two end points, and a pattern that says which of these boundary pieces are joined inside. There are $n^{O(m)}$ states. The value of a state is the least length of a graph inside the window that has that boundary, visits the points inside, and has even degrees. It is computed from the $O(n)$ cuts and the states of the two halves that agree on the cut. The total time is $n^{O(m)}$, so a ratio $1 + \varepsilon$ costs $n^{O(1/\varepsilon)}$.
