---
title: The fit step of variational shape approximation is optimal, the guarded loop never increases the L^(2,1) energy and stops, and a box gives its six sides
proves: [correctness, termination]
status: full
---

**Setup.** The mesh is connected and each face $T$ has an area $a_T > 0$ and a unit normal $n_T$. A partition $R = (R_1, \ldots, R_p)$ puts each face in one region, and each region $R_i$ has a unit proxy normal $N_i$. The energy is

$$E(R, N) = \sum_{i=1}^{p}\sum_{T \in R_i} a_T\,|n_T - N_i|^2.$$

For a set $S$ of faces write $A(S) = \sum_{T \in S} a_T$ and $m(S) = \sum_{T \in S} a_T n_T$. The fit step sets $N_i = m(R_i)/|m(R_i)|$ when $m(R_i) \ne 0$ and keeps $N_i$ otherwise. The flood step takes, in each region, the face $T$ of least error $a_T|n_T - N_i|^2$ as the seed of that region, and then grows the regions from the seeds with a priority queue: it pops the entry of least error, and if the face of the entry is still free, it gives the face the region of the entry and pushes each free neighbour with its error to the proxy of that region.

**Lemma 1 (the best normal).** For a set $S$ of faces and a unit vector $N$,

$$\sum_{T \in S} a_T\,|n_T - N|^2 = 2A(S) - 2\,m(S) \cdot N \ \ge\ 2A(S) - 2|m(S)|.$$

If $m(S) \ne 0$, equality holds exactly for $N = m(S)/|m(S)|$. If $m(S) = 0$, every unit $N$ gives $2A(S)$.

*Proof.* For unit vectors, $|n_T - N|^2 = 2 - 2\,n_T \cdot N$. Multiply by $a_T$ and add. By the Cauchy-Schwarz inequality $m \cdot N \le |m|\,|N| = |m|$, with equality for unit $N$ exactly when $N = m/|m|$. $\square$

**Lemma 2 (the fit step does not increase the energy).** If $N'$ is the result of the fit step on $(R, N)$, then $E(R, N') \le E(R, N)$.

*Proof.* $E$ is a sum of one term for each region, and the term of $R_i$ depends only on $N_i$. By Lemma 1, the new $N_i$ minimizes its term, or the term does not depend on $N_i$ and $N_i$ is kept. $\square$

**Lemma 3 (the best assignment, without connectivity).** For fixed proxies $N$, the partition that gives each face to a proxy of least error minimizes $E(\cdot, N)$ over all partitions.

*Proof.* With $N$ fixed, $E$ is a sum of one term for each face, and each term depends only on the region of that face. $\square$

So the two steps of Lloyd's algorithm, the fit of Lemma 2 and the assignment of Lemma 3, never increase $E$. Variational shape approximation does not use the assignment of Lemma 3, because it can give regions that are not connected. The flood step gives each face to the first region that reaches it in the order of the queue, which need not be a region of least error for that face. It is not proved to decrease the energy, and it can increase it: in 30 runs from random seeds on perturbed icospheres with 320 faces, 119 of the 337 flood steps increased the energy, by up to 16%. For this reason the algorithm keeps the new partition only if its energy is not larger (line L7).

**Lemma 4 (the flood).** On a connected mesh, the flood gives a region to every face. Each region of the result holds the seed of that region and is connected through shared edges. Distinct regions have distinct seeds, so no region is empty.

*Proof.* A face gets the region $i$ only when an entry for it, pushed by a neighbour that has region $i$, is popped. By induction on the order of the pops, each face of region $i$ is joined to the seed of $i$ by a path of faces of region $i$. Suppose a face is free at the end. The mesh is connected and the seeds are not free, so there are adjacent faces $T$ and $U$ with $T$ not free and $U$ free at the end. When $T$ got its region, $U$ was free, so an entry for $U$ was pushed. That entry was popped before the queue was empty, and $U$ was free then, so $U$ got a region, a contradiction. Each face is in one region, so the seeds of distinct regions are distinct faces. $\square$

**Theorem 1 (the energy never increases).** Let $E_0, E_1, \ldots$ be the energies after each step of the algorithm: each fit, each accepted flood, and each insertion of a proxy. Then $E_0 \ge E_1 \ge \cdots$.

*Proof.* A fit step does not increase the energy by Lemma 2. A flood is accepted only if its energy with the same proxies is not larger (line L7), and a rejected flood changes nothing. An insertion moves one face $T$ to a new region with the proxy normal $n_T$. The error of $T$ becomes $a_T|n_T - n_T|^2 = 0$, and the region and the proxy of every other face do not change. So no step increases $E$. $\square$

**Theorem 2 (termination and the number of regions).** Let $1 \le k \le$ the number of faces. The algorithm stops, and it returns a partition with $k$ nonempty regions, or fewer regions and energy 0.

*Proof.* The rounds of line L3 stop after at most $s$ rounds. Each pass of the outer loop either stops at line L8 or adds one proxy, so there are at most $k - 1$ passes. It remains to show that every region stays nonempty. A flood keeps all regions nonempty by Lemma 4. An insertion happens only when $E > 0$, right after a fit. It takes a face $T$ of largest error from a region $R_w$ of largest total error, so the total error of $R_w$ is positive. If $R_w$ were the single face $T$, the fit would have set $N_w = n_T$, and its error would be 0. So $R_w$ has at least two faces and is not empty after $T$ leaves. $\square$

The algorithm finds a local optimum in this sense: no single step of it decreases $E$ further. It is not proved to find the partition of least energy for the given $k$, and the energy it reaches depends on the order of the insertions.

**Theorem 3 (a box).** Let the mesh be the surface of a box, each of the six sides cut into triangles, and let $k = 6$.

1. A partition into 6 regions has energy 0, for some proxies, if and only if its regions are the six sides.
2. If the 6 proxy normals are the 6 outward side normals and each region has its seed on its own side, the flood returns the six sides.
3. For the six sides with their fitted proxies, the coarse mesh has the 8 corners of the box as its anchors and the 6 rectangles of the sides as its polygons.

*Proof.* (1) By Lemma 1 the least energy of a region is $2A - 2|m|$. Since $|m| \le \sum a_T|n_T| = A$, with equality only if all $n_T$ in the region are equal, the energy is 0 only if each region lies in one side. Six nonempty regions cover the six sides, and each side needs a region of its own, so there is one region for each side. Conversely, each side has $m = A\,n$ and energy 0.

(2) For a face of a side with normal $n$, the error to the proxy of its own side is 0, to the proxy of an adjacent side $2a_T$, and to the proxy of the opposite side $4a_T$. An entry with error 0 is pushed only by the region of the same side. We show by induction on the pops that, while some side still has a free face, there is an entry of error 0 for a free face in the queue, and that every face labelled so far has the region of its own side. Take a side $S$ with a free face. The faces of $S$ that are labelled carry region $S$, by the induction, and they include the seed. The triangles of a side are connected through shared edges, so a free face $U$ of $S$ is adjacent to a labelled face $T$ of $S$. When $T$ got region $S$, $U$ was free, so an entry $(0, U, S)$ was pushed, and it is still in the queue or it has been popped. If it was popped while $U$ was free, $U$ would have region $S$. So it is in the queue. Every entry with positive error is popped only after all entries with error 0, so the next face that gets a region gets it with error 0, which means from its own side. So every face gets the region of its own side.

(3) A vertex inside a side touches 1 region, a vertex inside an edge of the box touches 2, and a corner touches 3. So the anchors are the 8 corners. The proxy point $X_i$ of a side is the area-weighted mean of the centroids of its faces, which lies on the plane of the side, and a corner lies on the planes of its 3 sides, so each projection, and so the mean, is the corner itself. The border of a side is the rectangle around it, which passes through its 4 corners in order, so each polygon is the rectangle of a side. $\square$

That the full algorithm, which starts from one proxy and adds the others one at a time, reaches the six sides on every subdivision of every box is not proved here. The tests check it on the box of size $2 \times 3 \times 5$ with two subdivisions.
