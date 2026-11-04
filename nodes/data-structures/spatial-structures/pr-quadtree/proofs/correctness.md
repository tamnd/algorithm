---
title: The PR quadtree operations keep the compact invariant and report exactly the points in a box
proves: [correctness, termination]
status: full
---

We use the names of the pseudocode. The root cell is $[0, 2^D)^2$, cells are half-open squares, and points have integer coordinates. For a node $u$ let $S(u)$ be the set of points stored in the leaves below $u$. The invariant (R) asks: (1) each point of the tree lies in the cell of its leaf and is stored once; (2) each leaf holds at most $B$ points; (3) each internal node has $u.count = |S(u)| > B$, and each leaf has $u.count = |u.points|$; and (4) the children of an internal node of side $s$ are its four quadrants, of side $s/2$.

**Lemma 1 (quadrants).** For a cell $Z$ of side $s \ge 2$, the four quadrants are disjoint, their union is $Z$, and the quadrant chosen for $p \in Z$ is the one that holds $p$. *Proof.* On each axis, $[c, c + s)$ is the disjoint union of $[c, c + s/2)$ and $[c + s/2, c + s)$, and the test $p_i \ge c + s/2$ picks the half that holds $p_i$. The product of the halves gives the claim. $\square$

**Lemma 2 (unit cells).** A cell of side 1 holds at most one integer point. *Proof.* It is $[a, a+1) \times [b, b+1)$ with integers $a, b$, and the only integer point in it is $(a, b)$. $\square$

**Search.** By Lemma 1 and (R) part 4, at each internal node the point $p$ lies in exactly one child cell, so there is exactly one leaf whose cell holds $p$, and line L1 (and line L12) reaches it in at most $D$ steps, since the side halves at each step. By (R) part 1, $p$ is stored exactly when it is in that leaf's list.

**INSERT.** Let $p$ be a point of the root cell that is not stored. Lines L1 to L3 add $p$ to the only leaf whose cell holds it, and add 1 to the count of each node whose subtree now holds $p$; part 1 and part 3 hold. If $|u.points| \le B$, the loop does not run and (R) holds.

Otherwise the loop runs with a leaf $u$ that holds $B + 1 \ge 2$ points, all in its cell, while (R) holds at every other node. By Lemma 2, the side of $u$ is at least 2, so line L5 can make the four quadrants. Line L6 moves each point into the quadrant that holds it (Lemma 1), with counts equal to the list sizes; now $u$ is internal with $u.count = B + 1 > B$, so part 3 holds at $u$ and part 4 holds. The children's lists add up to $B + 1$ points, so at most one child holds more than $B$; if none does, (R) holds everywhere and the loop stops. If one does, it holds exactly $B + 1$ points, all in its cell, and the loop continues with it in the same situation. The side halves at each pass and is at least 2 at each pass, so the loop stops after at most $D$ passes.

**DELETE.** Let $p$ be stored, and let $u$ be its leaf, with path $v_1, \ldots, v_j$ from the root down to the parent of $u$. After line L13, $p$ is gone and each count on the path and at $u$ is one less, so the counts are correct, and parts 1, 2 and 4 hold. Part 3 can fail only at the nodes $v_i$, and only when $v_i.count = B$ now, since before it was more than $B$.

Line L14 treats $v_j, v_{j-1}, \ldots$ in turn. Claim: when it reaches $v_i$, (R) holds at every node except possibly $v_1, \ldots, v_i$, and the counts are correct. This holds for $i = j$. If $v_i.count > B$, then $v_{i'}.count \ge v_i.count > B$ for each $i' < i$, since the count of a node is at least that of its child, so (R) holds everywhere and the loop can stop. If $v_i.count \le B$, each child $c$ of $v_i$ has $c.count \le B$; by the claim (R) part 3 holds at $c$, so $c$ is a leaf. Line L14 gathers the lists of the four leaves, at most $B$ points in total, all in the cell of $v_i$ by part 1 and Lemma 1, into one leaf with the same count. Parts 1 to 4 then hold at $v_i$, and the claim holds for $i - 1$. The loop stops after at most $j \le D$ steps. If it ends at the root, (R) holds everywhere.

**Uniqueness.** Let $\mathcal{T}(Z, S)$ be the tree on a set $S$ of points of the cell $Z$ that satisfies (R). If $|S| \le B$, part 3 forces a leaf with list $S$. If $|S| > B$, the root is internal, part 4 fixes its children as the quadrants, and by part 1 and Lemma 1 the child for quadrant $Z_o$ is a tree on $S \cap Z_o$ that satisfies (R); by induction on the side, it is $\mathcal{T}(Z_o, S \cap Z_o)$. So the shape depends only on $S$, not on the order of the operations.

**RANGE-SEARCH.** Let $Q = [\ell_x, h_x] \times [\ell_y, h_y]$. Each reported point is stored and is in $Q$ by the test of line L10, and each leaf is reached at most once, since the calls follow the tree, so by part 1 no point is reported twice. Let $p \in S \cap Q$, with leaf $w$. For each node $v$ on the path from the root to $w$, $p$ lies in the cell of $v$ (by part 1 and Lemma 1, the cells along the path are nested) and in $Q$, so the cell of $v$ meets $Q$, and line L9 does not stop the search at $v$. Line L11 calls every child, so the search reaches $w$, and line L10 reports $p$. The calls follow a finite tree, so the search stops. $\blacksquare$
