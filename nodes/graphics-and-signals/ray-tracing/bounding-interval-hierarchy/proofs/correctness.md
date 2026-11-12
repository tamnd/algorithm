---
title: The bounding interval hierarchy build ends, its implicit boxes contain their objects, and its traversal finds the closest hit
proves: [correctness]
status: full
---

Let the objects have closed boxes $b_r = [l_r, h_r]$ and box centers $c_r = (l_r + h_r)/2$. Let $S$ be the scene box, the union of all $b_r$. For a node $v$, let $O(v)$ be the set of objects in the leaves below $v$. The *implicit box* $I(v)$ is $S$ for the root, and for the children of a node $v$ with axis $a$ and clip planes $\lambda$ (left) and $\rho$ (right), $I(\mathrm{left}) = I(v) \cap \{x : x_a \le \lambda\}$ and $I(\mathrm{right}) = I(v) \cap \{x : x_a \ge \rho\}$.

**Lemma 1 (the build ends, and each object is in one leaf).** Each pass of lines L4 to L6 at a node either splits its range into two nonempty parts or halves the candidate box $V$ on one axis and keeps all centers of the range in $V$. The build ends, every object is in exactly one leaf, and there are at most $2n - 1$ nodes.

*Proof.* At the start, $V = S$ holds all centers. Line L5 puts the centers with $c_{r,a} < p$ on the left and the others on the right. If all are on the left, they lie in the lower half $\{x \in V : x_a \le p\}$; if all are on the right, in the upper half. So line L6 keeps every center in $V$. The children get the two halves of $V$, each with the centers that line L5 gave it, so the invariant holds at every node. Line L3 makes a leaf when all centers of the range are equal. Otherwise, two centers differ by some $\epsilon > 0$ on some axis $k$, so the width of $V$ on axis $k$ stays at least $\epsilon$. Each halving takes the axis of largest width, and after finitely many halvings every width is below $\epsilon$ unless a split happened, a contradiction; so the loop ends with two nonempty parts. Each split makes the range of the node a disjoint union of the two child ranges, both nonempty and smaller, so the recursion ends, the leaves partition the objects, and a binary tree with $n$ nonempty leaves has at most $2n - 1$ nodes. $\square$

**Lemma 2 (the implicit boxes).** For every node $v$ and every object $r \in O(v)$, $b_r \subseteq I(v)$.

*Proof.* By induction from the root, where $b_r \subseteq S = I(\mathrm{root})$. Let $v$ have axis $a$ and clip planes $\lambda = \max_{r \in O(\mathrm{left})} h_{r,a}$ and $\rho = \min_{r \in O(\mathrm{right})} l_{r,a}$, as line L7 sets them. For $r$ in the left child, $b_r \subseteq I(v)$ and every point of $b_r$ has $x_a \le h_{r,a} \le \lambda$, so $b_r \subseteq I(\mathrm{left})$. The right child is the same with $x_a \ge l_{r,a} \ge \rho$. $\square$

So the clip planes give each child a slab that contains its objects, and the slabs of the two children can overlap (when $\lambda > \rho$) or leave a gap (when $\lambda < \rho$).

**Lemma 3 (the intervals).** In the traversal, the interval $[t_n, t_f]$ with which a node $v$ is pushed is the set of $t$ in $[0, \tau]$ with $o + t d \in I(v)$, where $\tau$ is the bound of the walk at the time of the push ($\infty$ before any hit, and then the least hit so far).

*Proof.* Line L9 gives the root the set of $t \ge 0$ with $o + t d \in S$, by the slab method on the closed box $S$. Line L13 cuts the interval of $v$ by one half-space: for $d_a > 0$ the set $\{t : o_a + t d_a \le \lambda\}$ is $t \le (\lambda - o_a)/d_a$, for $d_a < 0$ it is $t \ge (\lambda - o_a)/d_a$, and for $d_a = 0$ it is all $t$ or none, by the sign of $\lambda - o_a$. The right child is the same with $\ge \rho$. The intersection of intervals is an interval, and line L11 cuts $t_f$ to the best hit. $\square$

**Theorem.** The closest-hit traversal returns the least $t \ge 0$ at which the ray meets an object, or none if there is no such $t$.

*Proof.* Every value that the walk returns is a real hit, found by an exact test of a triangle in a leaf. Suppose the least hit is at $t^*$ on an object $r$. Let $v_0, \ldots, v_m$ be the path from the root to the leaf of $r$. The point $o + t^* d$ lies in $b_r$, so by Lemma 2 in $I(v_k)$ for every $k$. At every time the best hit so far is $\ge t^*$, so by Lemma 3, $t^*$ lies in the interval of each $v_k$ when it is pushed, the interval is not empty, and the node is pushed. When $v_k$ is popped, line L11 skips it only if $t_n > $ the best hit, but $t_n \le t^* \le$ the best hit. So every $v_k$ is popped and expanded, the leaf $v_m$ tests $r$, and the best hit becomes $t^*$. The walk ends since each node is pushed at most once (once by its parent). If there is no hit, no value is returned. $\blacksquare$

**Remark.** The walk cannot stop at the first leaf with a hit. In a kd-tree the cells of the two children are disjoint, so a hit inside the near cell comes before every point of the far cell. Here the slabs of the children overlap when $\lambda > \rho$, and an object of the far child can be hit before a hit found in the near child, as in the example of the page. The test $t_n >$ best of line L11 is what replaces the early stop. The any-hit query needs no order and returns at the first hit with $t \le t_{max}$; its correctness follows from Lemma 2 and Lemma 3 with $\tau = t_{max}$.
