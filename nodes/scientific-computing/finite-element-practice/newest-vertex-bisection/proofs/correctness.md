---
title: The marked-edge form of newest vertex bisection gives the coarsest conforming refinement
proves: [correctness]
status: full
---

**Setting.** $\mathcal{T}$ is a conforming triangulation of a polygon: two triangles meet in a common vertex, a common edge or not at all. Each triangle is stored as an ordered triple $[z_1, z_2, z_3]$. The edge $z_1z_2$ is its refinement edge, and $z_3$ is its newest vertex. One bisection of $[z_1, z_2, z_3]$ adds the midpoint $m$ of $z_1z_2$ and gives the two children $[z_3, z_1, m]$ and $[z_2, z_3, m]$. So the new vertex $m$ is the newest vertex of both children, and the two old edges $z_3z_1$ and $z_2z_3$ become their refinement edges. A refinement of $\mathcal{T}$ by newest vertex bisection is any triangulation that we get from $\mathcal{T}$ by a finite number of such bisections. The input is a set $\mathcal{M}$ of marked triangles. REFINE is the procedure of the main page, lines L1 to L10.

We prove four claims.

1. *(Termination.)* REFINE stops after at most $|\mathcal{E}|$ passes of the loop at line L2, where $\mathcal{E}$ is the set of edges of $\mathcal{T}$.
2. *(Closure.)* At line L5, for every triangle $T$, if any edge of $T$ is in the set $S$ of split edges, then the refinement edge of $T$ is in $S$.
3. *(Conformity.)* The output is a conforming triangulation of the same polygon, every marked triangle is bisected at least once, and the output is a refinement of $\mathcal{T}$ by newest vertex bisection.
4. *(Minimality.)* Every conforming refinement of $\mathcal{T}$ by newest vertex bisection in which every marked triangle is bisected is equal to the output of REFINE or is a refinement of it.

**Proof of 1.** An edge enters the stack only when it enters $S$ (lines L1 and L4), and it never leaves $S$. So every edge enters the stack at most once, and each pass of line L2 removes one edge from the stack. The loop at line L3 visits the at most two triangles that contain the edge. So the number of passes is at most $|\mathcal{E}|$, and the total work of lines L2 to L4 is $O(|\mathcal{E}|)$.

**Proof of 2.** Let $e \in S$ be an edge of $T$. The edge $e$ entered the stack when it entered $S$, and the loop at line L2 runs until the stack is empty, so $e$ was popped once. At that pass, line L3 visited every triangle that contains $e$, and $T$ is one of them. Line L4 then put the refinement edge of $T$ into $S$, or it was there already.

**Proof of 3.** By claim 2, each triangle $T = [z_1, z_2, z_3]$ falls into one of four cases at line L6: no edge of $T$ is in $S$; only $z_1z_2$ is in $S$; $z_1z_2$ and one other edge are in $S$; all three edges are in $S$. In the first case $T$ is kept. In the second case line L6 bisects $T$ once. If the left edge $z_3z_1$ is in $S$, line L8 bisects the child $[z_3, z_1, m]$, whose refinement edge is $z_3z_1$. If the right edge $z_2z_3$ is in $S$, line L9 bisects the child $[z_2, z_3, m]$, whose refinement edge is $z_2z_3$. So in every case the children of $T$ come from bisections by the rule of the setting, and the output is a refinement by newest vertex bisection. A marked triangle has its refinement edge in $S$ by line L1, so it is bisected at least once.

Now look at the edges of the children inside $T$. A direct check of the four cases shows:

- an edge of $T$ that is not in $S$ is a whole edge of exactly one child;
- an edge of $T$ that is in $S$, with midpoint $p$ from line L5, is the union of two edges of children, which meet at $p$;
- every other edge of a child lies inside $T$ (apart from its end points) and is shared by exactly two children of $T$.

For example, in the case with all three edges split, the children are $[m, z_3, l]$, $[z_1, m, l]$, $[m, z_2, r]$ and $[z_3, m, r]$, where $l$ and $r$ are the midpoints of $z_3z_1$ and $z_2z_3$. The edge $z_1z_2$ becomes $z_1m$ and $mz_2$, the edge $z_3z_1$ becomes $z_3l$ and $lz_1$, the edge $z_2z_3$ becomes $z_2r$ and $rz_3$, and the inner edges $mz_3$, $ml$ and $mr$ each lie in two children.

The children of $T$ tile $T$, because a bisection cuts a triangle into two triangles along a segment. So the output tiles the polygon. For conformity, take an edge $e$ of $\mathcal{T}$ that lies in two triangles $T$ and $T'$. The decision whether $e$ is in $S$ does not depend on the side, and line L5 gives $e$ one midpoint. If $e \notin S$, then $e$ is a whole edge of one child on each side. If $e \in S$, then both sides have the two halves of $e$ as edges, with the same midpoint. In both cases no vertex lies inside an edge of a child on the other side. Inner edges of $T$ meet only children of $T$. So no hanging node appears, and the output is conforming. The boundary loop after line L9 splits a boundary edge exactly when it is in $S$, so the boundary list matches the boundary of the new mesh.

**Proof of 4.** Let $\mathcal{T}^*$ be a conforming refinement by newest vertex bisection in which every marked triangle is bisected. Say that $\mathcal{T}^*$ splits an edge $e$ of $\mathcal{T}$ if the midpoint of $e$ is a vertex of $\mathcal{T}^*$. We show by induction over the order in which edges enter $S$ that $\mathcal{T}^*$ splits every edge in $S$.

An edge that enters at line L1 is the refinement edge of a marked triangle $T$. The first bisection of $T$ always cuts its refinement edge, and $T$ is bisected in $\mathcal{T}^*$. So $\mathcal{T}^*$ splits it.

An edge $r$ that enters at line L4 is the refinement edge of a triangle $T$ that contains an edge $e$ which entered $S$ before $r$. By the induction hypothesis, the midpoint $p$ of $e$ is a vertex of $\mathcal{T}^*$. Because $\mathcal{T}^*$ is conforming, $p$ cannot lie inside an edge of a triangle of $\mathcal{T}^*$. If $T$ were not bisected in $\mathcal{T}^*$, then $T$ would be a triangle of $\mathcal{T}^*$ with $p$ inside its edge $e$, which is a hanging node. So $T$ is bisected, and its first bisection cuts $r$. So $\mathcal{T}^*$ splits $r$.

So $\mathcal{T}^*$ splits every edge of $S$. Fix a triangle $T$ of $\mathcal{T}$. The descendants of $T$ in $\mathcal{T}^*$ form a refinement of $T$ by bisection that contains the midpoint of every edge of $T$ in $S$. The bisection of a triangle is fixed by its labels, so the refinements of $T$ form a binary tree of bisections. The children that REFINE gives to $T$ are the smallest subtree that splits exactly the edges of $T$ in $S$: one bisection for the refinement edge, and one more bisection of a child for each of the other two edges, as no other bisection adds the midpoint of that edge. So the descendants of $T$ in $\mathcal{T}^*$ are the REFINE children of $T$ or refinements of them. This holds for every $T$, which proves claim 4. $\square$

**What the proof does not cover.** The claims above hold for every labeling of the initial triangles, and one call of REFINE always stops. Two further facts are cited, not proved here. First, all descendants of one initial triangle fall into at most four similarity classes (Sewell 1972; Mitchell 1989), so the minimum angle stays bounded below by a constant that depends only on $\mathcal{T}$. The test file checks this on a scalene triangle. Second, the closure estimate of Binev, Dahmen and DeVore (2004), $\#\mathcal{T}_k - \#\mathcal{T}_0 \le C\sum_{j<k}\#\mathcal{M}_j$, needs a compatible labeling of $\mathcal{T}_0$ in their proof. Karkulik, Pavlicek and Praetorius (2013) proved it in 2D for every labeling.
