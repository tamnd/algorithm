---
title: The octree quantizer keeps exact counts and sums per cube, never holds more than k leaves or k(b + 1) nodes, and gives at most k palette colors with an error at least the optimum
proves: [correctness]
status: full
---

Fix $k \ge 1$ and the depth $b \ge 1$. For a node $v$ at level $\ell$, let $Q(v)$ be its cube: the colors whose first $\ell$ binary digits in each channel match the path from the root to $v$. The cubes of the 8 possible children of $v$ split $Q(v)$, and $Q(\text{root})$ is the whole cube. Write $S$ for the list of colors inserted so far.

**Invariant.** After each pass of lines L2 to L9:

- (a) the tree has at most $k$ leaves;
- (b) for each color $c \in S$, the descent of line L11 from the root reaches a leaf, and that leaf $v$ has $c \in Q(v)$;
- (c) each leaf $v$ has $\mathrm{count}(v) = |\{c \in S : c \in Q(v)\}|$ and $\mathrm{sum}(v) = \sum_{c \in S,\, c \in Q(v)} c$, counted with repetition;
- (d) each node that is not a leaf has at least one child.

*Proof.* Before any insertion, $S$ is empty and the root alone is not a leaf (for $b \ge 1$) with no children, which is the start; (a) to (c) hold with no leaves and no colors, and (d) is checked after the first pass. Suppose the invariant holds before a color $c$ is inserted.

*Lines L2 to L5.* The descent follows the children $i_\ell(c)$, which are the children whose cubes hold $c$. If it meets an existing leaf $v$, then $c \in Q(v)$. Otherwise it creates nodes down to level $b$, and the last one is a leaf with $Q = \{c\}$. In both cases line L5 adds $c$ to the leaf whose cube holds $c$, so (c) holds for the new $S$: no other leaf has $c$ in its cube, because two leaves are never ancestor and descendant, so their cubes are disjoint. Property (b) holds for $c$ by construction and for the earlier colors because their paths are unchanged. Property (d) holds because each new inner node has the next node of the path as a child.

*Lines L6 to L9.* Let $u$ be a node chosen by line L7, at the deepest level among the nodes with children. A child of $u$ with children of its own would be deeper, so every child of $u$ is a leaf. By (c) for these leaves, the sum of their counts and sums is the count and sum over the colors of $S$ in $\bigcup Q(\text{child}) \subseteq Q(u)$. Every color of $S$ in $Q(u)$ descends through $u$ and, by (b), to a leaf below $u$, which is one of these children. So the new values of $u$ satisfy (c). After line L9 the descent of a color that went through $u$ stops at $u$, which is now a leaf with that color in $Q(u)$, so (b) holds. Other leaves are unchanged, and (d) still holds for the other nodes.

Each merge deletes at least one node, so the inner loop stops. When it stops, the number of leaves is at most $k$, which is (a). The loop can always choose a node while there are more than $k \ge 1$ leaves: then the root is not a leaf, so a node with children exists. $\square$

**Claim 1 (size of the tree).** After each pass, the tree has at most $k(b + 1)$ nodes, and before the merges of a pass it has at most $k + 1$ leaves.

*Proof.* By (d) every inner node has a leaf below it, so every node lies on the path from the root to some leaf. A path from the root has at most $b + 1$ nodes, levels 0 to $b$. With at most $k$ leaves by (a), the union of the paths has at most $k(b + 1)$ nodes. One insertion creates at most one new leaf, so before the merges there are at most $k + 1$ leaves. $\square$

**Claim 2 (the palette).** The palette of line L10 has between 1 and $k$ colors, all with positive counts. Each pixel color $c$ is mapped to the mean $p$ of a leaf $v$ with $c \in Q(v)$ and $p \in \overline{Q(v)}$, the cube with real coordinates. If $S$ has at most $k$ distinct colors, the palette is exactly the set of distinct colors and the error is 0.

*Proof.* Every leaf was made by an insertion with a count of 1 or by a merge of leaves with positive counts, so all counts are positive and the means are defined. By (a) there are at most $k$ leaves, and for $n \ge 1$ there is at least one. By (b) the descent reaches a leaf $v$ with $c \in Q(v)$. By (c) the mean of $v$ is the mean of colors in $Q(v)$; this cube is the product of three integer intervals $[t 2^s, (t + 1) 2^s - 1]$ with $s = b - \ell$, which is convex, so the mean lies in its real box, and in each channel $\lfloor p_a / 2^s \rfloor = t = \lfloor c_a / 2^s \rfloor$.

If $S$ has $D \le k$ distinct colors, suppose no merge has run. Then an insertion creates a leaf only for a color seen for the first time, because a color seen before finds its own leaf at level $b$. So the tree has at most $D \le k$ leaves, line L6 never calls a merge, and the supposition holds throughout. Each leaf is then at level $b$ with a cube of one color, its mean is that color, and every pixel maps to its own color. $\square$

**Claim 3 (error).** The error of the octree palette is at least the least error $\mathrm{OPT}_k$ over all palettes of at most $k$ colors, and the palette can have fewer than $\min(k, D)$ colors.

*Proof.* The octree gives a palette of at most $k$ colors by Claim 2 and a map, so its error is one of the values in the minimum. For the second part, take $b = 8$, $k = 2$ and the colors $(0, 0, 0)$, $(255, 0, 0)$ and $(0, 255, 0)$. They lie in three different children of the root, because they differ in the first digit of red or green. After the third insertion there are 3 leaves. The only nodes with children are the chain nodes of each color at levels 1 to 7 and the root. A merge of a chain node at the deepest level lowers the leaf count by 0, so the count stays 3 until every chain is merged up to level 1, which leaves the root as the only node with children, with 3 leaf children. Merging it leaves one leaf. So the palette has 1 color while $\min(k, D) = 2$. $\square$

The examples on the page compute the error ratio $(2^{b-1} - 1)^2$ for the reds $0$, $2^{b-1} - 1$ and $2^{b-1}$ with $k = 2$: the root separates $2^{b-1} - 1$ from $2^{b-1}$, so 0 and $2^{b-1} - 1$ share a leaf with an error of $2 \cdot ((2^{b-1} - 1)/2)^2$, while the palette $\{0, 2^{b-1} - 1/2\}$ has an error of $1/2$. So for a fixed depth the ratio is finite, but it grows without a bound as the depth grows.
