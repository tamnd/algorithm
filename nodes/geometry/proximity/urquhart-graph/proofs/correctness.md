---
title: BUILD computes the Urquhart graph, which lies between the relative neighborhood graph and the Delaunay triangulation
proves: [correctness, termination]
status: full
---

**Setting.** $P$ is a set of $n$ distinct points in the plane with no four on a common circle. Then the Delaunay triangulation $DT$ of $P$ is unique, and a triangle with vertices in $P$ belongs to it if and only if its circumcircle has no point of $P$ in its interior (the empty-circle characterization, de Berg, Cheong, van Kreveld and Overmars, Chapter 9). Since no fourth point lies on any circumcircle, this is the same as asking that no other point lies inside or on it. If all points are on one line there are no triangles, and the triangulation is the path through the points in sorted order. The Urquhart graph $UG$ is $DT$ minus, for each triangle of $DT$ whose longest side is unique, that side.

**Lemma 1 (BUILD is correct).** After BUILD, $adj$ holds exactly the edges of $UG$, each at both ends.

*Proof.* Line L1 computes the set $T$ of triangles with an empty circumcircle, which by the setting are the triangles of $DT$. Line L2 collects their sides, which are the edges of $DT$: every edge of a triangulation of a set that is not collinear is a side of at least one triangle, and in the collinear case line L2 takes the path. Lines L3 to L5 go through each triangle once, sort its three sides by squared length, and remove the longest side exactly when it is strictly longer than the second, that is, when the longest side is unique. Squared lengths order the sides like lengths. Removing an edge that was already removed by the other triangle on it changes nothing. Line L6 stores the remaining edges in both directions, and lines L7 and L8 only read them. $\square$

**Termination.** Line L1 tests $\binom{n}{3}$ triples against at most $n - 3$ points each, and lines L2 to L6 loop over the at most $2n$ triangles and $3n$ edges, so BUILD stops.

**Lemma 2 (UG lies in DT).** Every edge of $UG$ is an edge of $DT$.

*Proof.* Lines L3 to L5 only remove edges from the edge set of $DT$. $\square$

**Lemma 3 (the RNG lies in UG).** Every edge of the [relative neighborhood graph](/relative-neighborhood-graph/) of $P$ is an edge of $UG$.

*Proof.* Every RNG edge is a Gabriel edge and hence an edge of $DT$ (shown on the [Gabriel graph](/gabriel-graph/) page). Let $pq$ be an edge of $DT$ that is removed by lines L3 to L5. Then $pq$ is the unique longest side of some Delaunay triangle $pqr$, so $\|p - r\| < \|p - q\|$ and $\|q - r\| < \|p - q\|$. Thus $r$ lies in the open lune of $p$ and $q$, and $pq$ is not an RNG edge. So no RNG edge is removed. $\square$

**Conclusion.** By Lemma 1, BUILD stores exactly the Urquhart graph, and it terminates. By Lemmas 2 and 3, $RNG \subseteq UG \subseteq DT$. Every Euclidean minimum spanning tree lies in the RNG, so $UG$ is connected, and as a subgraph of $DT$ it is planar. $\blacksquare$
