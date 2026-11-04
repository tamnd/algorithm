---
title: The MX-CIF quadtree stores each rectangle at its smallest enclosing cell and reports exactly the rectangles that meet a window
proves: [correctness, termination]
status: full
---

We use the names of the pseudocode. Cells are half-open squares, the root cell is $[0, 2^D)^2$, and rectangles are half-open with integer corners. For a cell $Z$ of side $s \ge 2$ and a rectangle $r \subseteq Z$, write $\text{quad}(Z, r)$ for the quadrant of $Z$ that holds $r$, or none if no quadrant does; for $s = 1$ it is none. The invariant (M) asks: (1) each stored rectangle is stored once, at a node $u$ whose cell holds it, with $\text{quad}(u, r)$ none; (2) the children of a node are its quadrants; (3) each node other than the root stores a rectangle or has a child.

**Lemma 1 (the quadrant test).** For $r \subseteq Z$, the test of the representation returns the quadrant that holds $r$ if there is one, and none otherwise. *Proof.* On the $x$ axis, $[x_1, x_2) \subseteq [c, c_x)$ if and only if $x_2 \le c_x$, and $[x_1, x_2) \subseteq [c_x, c + s)$ if and only if $x_1 \ge c_x$, since $r \subseteq Z$. The same holds on the $y$ axis, and a quadrant is the product of one half on each axis. $\square$

**Lemma 2 (the path of a rectangle).** Let $Z_0$ be the root cell and $Z_{i+1} = \text{quad}(Z_i, r)$ while this is not none, ending at $Z_t$. Then $Z_t$ is the smallest cell of the quadtree that holds $r$, and every cell of the quadtree that holds $r$ is one of $Z_0, \ldots, Z_t$. *Proof.* Cells of the quadtree are nested or disjoint. A cell $W$ that holds $r$ meets $Z_0$, so $W \subseteq Z_0$; if $W \subseteq Z_i$ and $W \ne Z_i$, then $W$ lies in one quadrant of $Z_i$, which holds $r$, so it is $Z_{i+1}$ by Lemma 1 and $W \subseteq Z_{i+1}$. Since the sides halve, $W = Z_i$ for some $i \le t$. Also no quadrant of $Z_t$ holds $r$, so no cell smaller than $Z_t$ does. $\square$

**INSERT.** Lines L1 to L4 follow the path of Lemma 2, making the missing nodes as quadrants of their parents, so part 2 holds. They stop at $Z_t$, after at most $D$ steps. Line L5 stores $r$ at $Z_t$, which holds $r$ and has no quadrant that holds it, so part 1 holds; the code first checks that $r$ is not already there, and by Lemma 2 this is the only node where it could be. Each node made on the path now has $r$ below it, so part 3 holds.

**DELETE.** By Lemma 2 and part 1, if $r$ is stored, it is at the node of $Z_t$, and all nodes on the path to it exist; so line L11 returns false only if $r$ is not stored, and line L12 finds $r$ if it is. After removing $r$, parts 1 and 2 still hold, and part 3 can fail only at nodes of the path, since only their sets of rectangles below them changed. Lines L13 and L14 go up the path and remove each node with no rectangle and no child. When the loop stops at a node $u$ that stores a rectangle or has a child, every node above $u$ has $u$ below it, so part 3 holds there. The loop goes up one level each pass, so it stops after at most $D$ passes.

**Uniqueness.** By part 1 and Lemma 2, each rectangle is at the node of its own $Z_t$, which depends only on the rectangle. By part 3, a node exists if and only if its cell is on the path of a stored rectangle. So the tree depends only on the set of rectangles.

**WINDOW.** Each node is pushed once, by its parent, so the loop stops after visiting each node at most once, and by part 1 no rectangle is reported twice. Each reported rectangle is stored and meets $q$, by line L9. Let $r$ be stored at $u$ and meet $q$. For each node $w$ on the path from the root to $u$, the cell of $w$ holds the cell of $u$, which holds $r$, so it meets $q$, and line L7 does not skip $w$. Line L10 pushes all children, so $u$ is visited, and line L9 reports $r$.

**STAB.** If $r$ holds $p$ and is stored at $u$, then the cell of $u$ holds $p$, so it is one of the cells of the quadtree that hold $p$, which form the single path from the root to the cell of side 1 at $p$. The stab walk visits the existing nodes of that path, and each rectangle it reports holds $p$ by its test. $\blacksquare$
