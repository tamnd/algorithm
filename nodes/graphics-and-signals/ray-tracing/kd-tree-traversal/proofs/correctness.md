---
title: Front-to-back kd-tree traversal visits the cells along the ray in order and returns the closest hit
proves: [correctness]
status: full
---

Let the tree have closed cells: the root cell is the scene box, and an inner node $v$ with axis $a$ and plane $p$ has the children $\mathrm{left}(v) = C(v) \cap \{x_a \le p\}$ and $\mathrm{right}(v) = C(v) \cap \{x_a \ge p\}$. Let the ray be $r(t) = o + t d$ with $d \ne 0$, and $t_{max} \ge 0$ or $t_{max} = \infty$. For a node $v$, let $J(v) = \{t \in [0, t_{max}] : r(t) \in C(v)\}$, an interval since $C(v)$ is convex.

**Lemma 1 (the build).** Each leaf holds every triangle that meets its cell.

*Proof.* A triangle that meets a cell has a box that meets the cell. The build gives a triangle to a child when its box meets the closed half-space of the child on the split axis. On every axis, the box of the triangle then meets the cell of each node on the path: on the axes cut by the path, by this rule, and on the others, since the root cell is the scene box, which contains every triangle. So every triangle whose box meets a leaf cell is in that leaf, and in particular every triangle that meets it. $\square$

**Lemma 2 (one step).** Let an inner node $v$ be reached with an interval $[t_n, t_f] \subseteq J(v)$, $t_n \le t_f$. Lines L5 to L10 either go on with one child $c$ and $[t_n, t_f] \subseteq J(c)$, or go on with near and $[t_n, t_s] \subseteq J(\mathrm{near})$ and push far with $[t_s, t_f] \subseteq J(\mathrm{far})$.

*Proof.* Let $f(t) = o_a + t d_a - p$, a linear function with $f(0) = o_a - p$. Line L5 picks near as the left child when $o_a < p$, or $o_a = p$ and $d_a \le 0$; then $f(t) \le 0$ for all $t \in [0, t_s]$ when $d_a > 0$ (with $t_s = (p - o_a)/d_a$), and for all $t \ge 0$ when $d_a \le 0$. In the other case, near is the right child and $f(t) \ge 0$ on the same sets with the signs exchanged. So $r(t)$ is in the closed cell of near for $0 \le t \le t_s$ (for all $t \ge 0$ if $d_a = 0$ or $t_s \le 0$), and in the cell of far for $t \ge t_s$ when $t_s > 0$. Line L6: $d_a = 0$, near holds $r(t)$ for all $t$. Line L8: if $t_s > t_f$, near holds $r(t)$ on $[t_n, t_f]$; if $t_s \le 0$, the ray at $t > 0$ moves away from the plane on the side of near, and near holds it on $[t_n, t_f]$ too. Line L9: $0 < t_s < t_n$, so far holds $r(t)$ on $[t_n, t_f]$. Line L10: $t_n \le t_s \le t_f$ and $t_s > 0$, so near holds $[t_n, t_s]$ and far holds $[t_s, t_f]$. In each case the cell of $v$ also holds these points, so they are in the cell of the child. $\square$

**Lemma 3 (the order).** Without the return of line L12, the walk visits leaves $\ell_1, \ldots, \ell_k$ with intervals $[s_0, s_1], [s_1, s_2], \ldots, [s_{k-1}, s_k]$, where $[s_0, s_k] = J(\mathrm{root})$, and $[s_{j-1}, s_j] \subseteq J(\ell_j)$.

*Proof.* By induction on the height of a subtree: a node reached with $[t_n, t_f]$ produces leaves whose intervals follow each other and cover $[t_n, t_f]$. For a leaf this is clear. For an inner node, Lemma 2 gives one child with the whole interval, or the near child with $[t_n, t_s]$ followed by the far child with $[t_s, t_f]$. The far child is pushed and the walk goes down the near child at once; the stack is last in, first out, so all of the near subtree is done before the far child is popped. Line L1 gives the root $J(\mathrm{root})$ by the exact slab method. The containment comes from Lemma 2. $\square$

**Theorem.** KD-CLOSEST returns the least $t \in [0, t_{max}]$ at which the ray meets a triangle, with that triangle, or none if there is no such $t$.

*Proof.* Every returned value is a real hit with $t \le t_{max}$. Let $t^*$ be the least hit, on the triangle $q$. The point $r(t^*)$ lies on $q$, which lies in the scene box, so $t^* \in J(\mathrm{root}) = [s_0, s_k]$, and $t^* \in [s_{i-1}, s_i]$ for some least $i$. By Lemma 3, $r(t^*) \in C(\ell_i)$, so $q$ meets the cell of $\ell_i$ and is in $\ell_i$ by Lemma 1. So if the walk reaches $\ell_i$, its least hit is at most $t^* \le s_i$, which is the $t_f$ of $\ell_i$, and line L12 returns. Now suppose the walk returns at a leaf $\ell_j$ with $j \le i$ and the hit $t_b$. Then $t_b \ge t^*$, since $t^*$ is the least hit. If $j < i$, then $t_b \le s_j \le s_{i-1} \le t^*$, so $t_b = t^*$. If $j = i$, the least hit in $\ell_i$ is at most $t^*$ since $q$ is there, so $t_b = t^*$. If there is no hit, line L12 never returns and line L13 returns none. The walk ends, since each node is reached once. $\blacksquare$

**Remark.** A hit in $\ell_j$ with $t > s_j$ is a point outside the cell of $\ell_j$, on a triangle that is in $\ell_j$ only because it also meets that cell elsewhere. A nearer hit on another triangle can lie in a later cell, so the test $t \le t_f$ of line L12 is what makes the early return correct. The proof also shows that hits with $t < t_n$ in a leaf may be accepted: such a hit would have been found in an earlier leaf.
