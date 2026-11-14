---
title: The packing of a sequence pair has no overlap and is the least packing that obeys its relations
proves: [correctness, complexity]
status: full
---

We use the pseudocode and the convention of the page. Let $(\Gamma_+, \Gamma_-)$ be two orders of the same $n$ blocks, and write $a <_+ b$ and $a <_- b$ for "a comes before b" in the two orders. For blocks $a \ne b$:

- $a$ is *left of* $b$ if $a <_+ b$ and $a <_- b$;
- $a$ is *below* $b$ if $b <_+ a$ and $a <_- b$.

Let $G_h$ be the directed graph with an edge $a \to b$ of weight $w_a$ for each pair with $a$ left of $b$, and $G_v$ the graph with an edge $a \to b$ of weight $h_a$ for each pair with $a$ below $b$. These are the [constraint graphs](/floorplan-constraint-graphs/) of the pair.

**Lemma 1 (one relation per pair).** For each pair of distinct blocks $a, b$, exactly one of these holds: $a$ left of $b$, $b$ left of $a$, $a$ below $b$, $b$ below $a$.

*Proof.* The two orders give the two bits $[a <_+ b]$ and $[a <_- b]$. The four values of the two bits are the four cases: $(1, 1)$ is $a$ left of $b$, $(0, 0)$ is $b$ left of $a$, $(0, 1)$ is $a$ below $b$, and $(1, 0)$ is $b$ below $a$. $\square$

**Lemma 2 (the graphs are acyclic).** Every edge $a \to b$ of $G_h$ has $a <_+ b$, and every edge of $G_v$ has $a <_- b$. So $\Gamma_+$ is a topological order of $G_h$ and $\Gamma_-$ is a topological order of $G_v$, and both graphs are DAGs.

*Proof.* This is the definition of the two relations. $\square$

**Lemma 3 (longest paths).** Lines L10 to L15 set $x_b$ to the length of the longest path into $b$ in $G_h$ and $y_b$ to the length of the longest path into $b$ in $G_v$. These are the least values that satisfy $x_b \ge x_a + w_a$ for each edge of $G_h$, $y_b \ge y_a + h_a$ for each edge of $G_v$, and $x, y \ge 0$.

*Proof.* Line L11 visits the blocks in the order $\Gamma_+$, which is topological by Lemma 2, so every predecessor $a$ of $b$ has its final value when $b$ is visited. Line L12 then takes the maximum of $x_a + w_a$ over all edges into $b$, which is the recurrence of the [longest path in a DAG](/dag-longest-path/). The same holds for lines L13 and L14 with $\Gamma_-$. By induction along the topological order, any solution of the inequalities has $x_b$ at least the longest path value, and the longest path values satisfy all of them. $\square$

**Lemma 4 (the Fenwick pass).** Lines L1 to L4 compute the same $x$ as Lemma 3, and lines L5 to L8 the same $y$.

*Proof.* Consider line L3 for the block $b$ with position $p$ in $\Gamma_-$. The blocks already in the tree are exactly the blocks $a$ with $a <_+ b$, because line L2 follows $\Gamma_+$. The tree stores at position $q$ the value $x_a + w_a$ of the block $a$ at position $q$ of $\Gamma_-$, if $a$ has been seen, and 0 otherwise, and a query returns the maximum over positions $1, \ldots, p - 1$, that is over the blocks with $a <_- b$. So the query returns the maximum of $x_a + w_a$ over the blocks with $a <_+ b$ and $a <_- b$, which are the blocks left of $b$, or 0 if there is none. This is the recurrence of Lemma 3, evaluated in the same order. For $y$, line L6 visits the blocks in the reverse of $\Gamma_+$, so the blocks seen before $b$ are those with $b <_+ a$, and the query selects those with $a <_- b$: the blocks below $b$. $\square$

**Theorem 1 (no overlap).** In the packing, no two blocks overlap, and for every pair the relation of Lemma 1 holds in the geometry: if $a$ is left of $b$ then $x_a + w_a \le x_b$, and if $a$ is below $b$ then $y_a + h_a \le y_b$. Line L9 returns the width and the height of the bounding box.

*Proof.* By Lemma 3 every edge constraint holds. By Lemma 1 every pair has an edge in one of the graphs, so the two blocks are separated by a vertical line or by a horizontal line, and their interiors do not meet. The query over all $n$ positions in line L9 returns the largest $x_a + w_a$, which is the right side of the bounding box, and the same for the top. $\square$

**Theorem 2 (the least packing).** Let $P$ be any placement of the blocks without overlap in which, for each pair, the relation of the sequence pair holds ($a$ left of $b$ implies $x^P_a + w_a \le x^P_b$, and the same for below). Then $x_b \le x^P_b$ and $y_b \le y^P_b$ for all $b$, and the packing is not wider and not higher than $P$.

*Proof.* The coordinates of $P$ satisfy the inequalities of Lemma 3, so they are at least the least solution. $\square$

**Cited theorem (every packing has a sequence pair).** For every placement $P$ of the blocks without overlap there is a sequence pair whose packing is not wider and not higher than $P$. In particular, some sequence pair gives a packing of least area. This is the main theorem of Murata, Fujiyoshi, Nakatake and Kajitani (IEEE TCAD 15(12), 1996, the section on the gridding procedure). *Proof sketch:* from the centre of each block draw two monotone staircase lines, one up and to the right and one down and to the left, that go around the other blocks and do not cross the lines of other blocks; this gives the positive locus of the block. The positive loci of different blocks do not cross, so they are ordered from the upper left to the lower right, and this order is $\Gamma_+$. The negative loci, which go up and to the left and down and to the right, give $\Gamma_-$ in the same way. For each pair, the relation that the two loci give is true in $P$, so Theorem 2 applies. The tests check the consequence for $n \le 4$: the least area over all $(n!)^2$ pairs equals the least area of a packing, found by a search over all positions.

**Complexity.** The Fenwick tree has $n$ cells, and each of the $2n$ updates and $2n + 2$ queries takes $O(\log n)$ time, so PACK takes $O(n \log n)$ time and $O(n)$ space. PACK-BY-GRAPHS looks at each ordered pair one time in each pass, so it takes $\Theta(n^2)$ time. A relation query reads two positions, and a swap updates two entries of each order and of the position maps, in $O(1)$ time. $\blacksquare$
