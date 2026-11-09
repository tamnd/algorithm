---
title: BUILD computes the Gabriel graph, which lies between the minimum spanning tree and the Delaunay graph
proves: [correctness, termination]
status: full
---

**Setting.** $P = \{p_0, \ldots, p_{n-1}\}$ is a set of distinct points in the plane. For $i \ne j$ let $D_{ij}$ be the closed disk with diameter $p_i p_j$: its center is $m = (p_i + p_j)/2$ and its squared radius is $\rho^2 = \|p_i - p_j\|^2 / 4$. The pair $\{i, j\}$ is a Gabriel edge when no $p_k$ with $k \ne i, j$ lies in $D_{ij}$.

**Lemma 1 (the dot test).** For every point $r$, $(p_i - r) \cdot (p_j - r) = \|m - r\|^2 - \rho^2$. So $r \in D_{ij}$ if and only if $(p_i - r) \cdot (p_j - r) \le 0$.

*Proof.* Put $u = (p_i - p_j)/2$. Then $p_i - r = (m - r) + u$ and $p_j - r = (m - r) - u$, so $(p_i - r) \cdot (p_j - r) = \|m - r\|^2 - \|u\|^2$, and $\|u\|^2 = \rho^2$. The point $r$ is in the closed disk exactly when $\|m - r\|^2 \le \rho^2$. $\square$

**Lemma 2 (BUILD is correct).** After BUILD, $j \in adj[i]$ and $i \in adj[j]$ hold exactly for the Gabriel edges $\{i, j\}$, and no other entries exist.

*Proof.* Lines L1 to L6 consider each unordered pair $\{i, j\}$ once, with $i < j$, and only those lines write to $adj$. For a fixed pair, line L2 sets $empty$ to true, and line L5 sets it to false exactly when line L4 finds some $k \ne i, j$ with $(p_i - p_k) \cdot (p_j - p_k) \le 0$, which by Lemma 1 means $p_k \in D_{ij}$. Stopping the loop of line L3 early at that point does not change the outcome, because $empty$ is never set back to true. So at line L6, $empty$ is true exactly when no other point is in $D_{ij}$, and line L6 adds the edge in both directions exactly in that case. Lines L7 and L8 read $adj$ without changing it. $\square$

**Termination.** The loops of lines L1 and L3 run over finite index ranges, so BUILD makes at most $\binom{n}{2}(n-2)$ dot tests and stops.

The following two lemmas give the properties used on the page. Write $GG$, $RNG$ and $DG$ for the Gabriel graph, the [relative neighborhood graph](/relative-neighborhood-graph/) and the Delaunay graph of $P$.

**Lemma 3 (any minimum spanning tree is in the RNG, and the RNG is in the GG).** Let $T$ be any minimum spanning tree of the complete graph on $P$ with Euclidean weights. Then $T \subseteq RNG \subseteq GG$.

*Proof.* Recall that $\{p, q\} \in RNG$ when no third point $r$ has $\max(\|p - r\|^2, \|q - r\|^2) < \|p - q\|^2$. If $pq \in T$ and such an $r$ existed, removing $pq$ from $T$ splits it into two parts, one with $p$ and one with $q$; $r$ is in one of them, so one of the edges $pr$ or $qr$ joins the two parts, and adding it gives a spanning tree of smaller weight, a contradiction. So $T \subseteq RNG$. For the second inclusion, suppose $\{p, q\} \notin GG$, so some third point $r$ has $(p - r) \cdot (q - r) \le 0$. Then
$$\|p - q\|^2 = \|(p - r) - (q - r)\|^2 = \|p - r\|^2 + \|q - r\|^2 - 2 (p - r) \cdot (q - r) \ge \|p - r\|^2 + \|q - r\|^2.$$
Both terms on the right are positive because the points are distinct, so each of them is strictly less than $\|p - q\|^2$, and $\{p, q\} \notin RNG$. $\square$

**Lemma 4 (the GG is in the Delaunay graph).** Every Gabriel edge is an edge of the Delaunay graph of $P$, and therefore of every Delaunay triangulation of $P$.

*Proof.* Two points $p, q \in P$ are adjacent in the Delaunay graph if and only if some closed disk has $p$ and $q$ on its boundary and contains no other point of $P$ (de Berg, Cheong, van Kreveld and Overmars, the characterization of Delaunay edges in Chapter 9). For a Gabriel edge, $D_{pq}$ is such a disk. A Delaunay triangulation is obtained from the Delaunay graph by adding diagonals inside faces that are not triangles, so it contains every edge of the Delaunay graph. $\square$

**Conclusion.** By Lemma 2 the structure stores exactly the Gabriel graph, by termination it is built in finite time, and by Lemmas 3 and 4, for every minimum spanning tree $T$ and every Delaunay triangulation $DT$ of $P$, $T \subseteq RNG \subseteq GG \subseteq DT$. In particular the Gabriel graph is planar, since it is a subgraph of a planar straight-line graph, and it is connected, since it contains a spanning tree. $\blacksquare$
