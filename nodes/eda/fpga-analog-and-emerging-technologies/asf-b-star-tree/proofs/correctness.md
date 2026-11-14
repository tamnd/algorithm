---
title: Every packing of an ASF-B*-tree is symmetric and free of overlap, and the moves keep the tree an ASF-B*-tree
proves: [correctness]
status: full
---

Notation. A symmetric set has pairs, each of two cells of size $w \times h$, and self-symmetric cells of size $w \times h$. The representative of a pair is its right cell, of size $w \times h$. The representative of a self-symmetric cell is its right half, of size $\frac{w}{2} \times h$. All sizes are positive. The tree is a B*-tree over the representatives: the root has $x = 0$, a left child $c$ of $b$ has $x_c = x_b + w_b$, and a right child has $x_c = x_b$. The representatives are placed in preorder, and each takes the least $y$ that is at or above the top of every representative placed before it whose $x$-range meets its own (line L3). The *rightmost branch* is the root and its chain of right children. The tree is an ASF-B*-tree if every self-symmetric representative is on the rightmost branch.

**Lemma 1 (the axis is the rightmost branch).** In the packing of a B*-tree, every representative has $x \ge 0$, and $x_b = 0$ if and only if $b$ is on the rightmost branch.

*Proof.* By induction along the path from the root. The root has $x = 0$. A right child has the $x$ of its parent. A left child has $x_b + w_b > x_b \ge 0$. So $x \ge 0$ for all, and $x = 0$ exactly when every step of the path from the root goes to a right child. $\square$

**Lemma 2 (no overlap among the representatives).** No two representatives overlap.

*Proof.* Let $b$ be placed after $c$. If their $x$-ranges meet, line L3 gives $y_b \ge y_c + h_c$, so $b$ is above $c$. If they do not meet, they do not overlap. $\square$

**Theorem 3 (symmetric and free of overlap).** Let the tree be an ASF-B*-tree. Lines L5 and L6 place the left cell of each pair at $(-x_b - w_b, y_b)$ and each self-symmetric cell at $(-\frac{w}{2}, y_b)$ with its full width. Then the placement is mirror-symmetric about $x = 0$, and no two cells overlap.

*Proof.* Symmetry. The two cells of a pair have the same $y$, and their $x$-ranges $[x_b, x_b + w_b]$ and $[-x_b - w_b, -x_b]$ are mirror images about $0$. A self-symmetric representative is on the rightmost branch, so $x_b = 0$ by Lemma 1, and the full cell $[-\frac{w}{2}, \frac{w}{2}]$ is centered on the axis.

No overlap. Cut each self-symmetric cell into its two halves; it is enough to show that no two of the pieces overlap. The pieces are the representatives, which lie in $x \ge 0$ by Lemma 1, and their mirror images, which lie in $x \le 0$. Two representatives do not overlap, by Lemma 2. Two mirror images do not overlap, because the mirror of an overlap would be an overlap of two representatives. A representative and a mirror image have $x$-ranges whose interiors are in $(0, \infty)$ and $(-\infty, 0)$, so they do not overlap. $\square$

**Theorem 4 (no loss of area).** For every placement of the group that is mirror-symmetric about a vertical axis, there is an ASF-B*-tree whose packing has a width and a height that are no larger.

*Proof.* Move the axis to $x = 0$. The two cells of a pair have the same $y$ and do not overlap, so they are on opposite sides of the axis; take the cell at $x \ge 0$ as the representative. Together with the right halves of the self-symmetric cells, which are at $x = 0$, this is a placement of the representatives in $x \ge 0$ without overlap. Compact it down and to the left, against $y = 0$ and $x = 0$, until no representative can move. This does not increase the width or the height, and the self-symmetric halves stay at $x = 0$, because they cannot move left of it. Chang, Chang, Wu and Wu prove that each placement that is compact to the left and down is the packing of a B*-tree (the B*-tree page cites this). In that tree, the self-symmetric halves are at $x = 0$, so they are on the rightmost branch by Lemma 1, and the tree is an ASF-B*-tree. Mirroring the packing gives back a symmetric placement of the group that is no wider and no higher. $\square$

So a search over ASF-B*-trees loses no symmetric placement of least area. The tests check this consequence on three small groups by a search over a grid.

**Theorem 5 (the moves keep the tree an ASF-B*-tree).** ROTATE, SWAP, DELETE and INSERT, as defined on the page, map an ASF-B*-tree (minus the deleted node, between DELETE and INSERT) to an ASF-B*-tree.

*Proof.* ROTATE changes no link. SWAP is refused when it would put a self-symmetric label on a node off the rightmost branch, and it changes no link. DELETE of a node $b$ with two children first exchanges $b$ with its left child until $b$ has at most one child. A left child is not on the rightmost branch, so the label that moves up is a pair label, and the labels of the rightmost branch other than $b$ stay on it. Then $b$ is replaced by its only child $c$, if any. If $b$ is on the rightmost branch and $c$ is its right child, the nodes below $c$ on the rightmost branch move up by one and stay on it. If $c$ is a left child, $b$ has no right child, so no self-symmetric label was below $b$ on the rightmost branch. If $b$ is off the rightmost branch, the rightmost branch does not change. INSERT of $b$ as the side child of $p$ makes the old child a child of $b$ on the same side, so every node keeps the kind of path from the root it had, except that $b$ is added on it; with $p$ empty, $b$ becomes the root and the old root its right child, which keeps the old rightmost branch below $b$. A self-symmetric $b$ is inserted only as the root or as the right child of a node on the rightmost branch, so it lands on the rightmost branch. $\square$

**What is not true: a packing need not be connected.** Take a self-symmetric cell $r$ of size $2 \times 3$, a pair $b$ of $2 \times 1$ and a pair $c$ of $1 \times 1$. The tree has the root $r$, the right child $b$ of $r$, and the left child $c$ of $b$. The packing puts the half of $r$ at $[0, 1] \times [0, 3]$, $b$ at $[0, 2] \times [3, 4]$ and $c$ at $x = 2$. The $x$-range $[2, 3]$ of $c$ meets no placed cell, so $y_c = 0$, and $c$ is at $[2, 3] \times [0, 1]$. It shares no boundary with any other cell, and neither does its mirror. So this packing of an ASF-B*-tree is symmetric but not one connected region. The tests check this tree, and they count 3 trees out of 80 with disconnected packings for a group of two pairs and two self-symmetric cells.

What is proved here: Lemmas 1 and 2 and Theorems 3 and 5, and Theorem 4 given the cited result on B*-trees. What is cited: the B*-tree theorem on compact placements, and the symmetry-island theorem of Lin, Chang and Lin, which the example above shows needs more than the plain contour packing. What is measured: that the least area over all ASF-B*-trees equals the least area of a grid search on three small groups, and the number of disconnected packings.
