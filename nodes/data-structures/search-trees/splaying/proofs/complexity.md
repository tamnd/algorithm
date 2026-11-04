---
title: The Access Lemma, an amortized bound of 3(r(t) - r(x)) + 1 for splaying
proves: [amortized-time]
status: full
---

Give each node $i$ a weight $w(i) > 0$, which does not change during the splay. For a node $x$, let $s(x)$ be the total weight of the subtree rooted at $x$, and $r(x) = \lg s(x)$. The potential of the tree is $\Phi = \sum_x r(x)$. The cost of a splay is the number of rotations, or 1 if there are none. For a step, write $r$ and $s$ for the values before and $r'$ and $s'$ for the values after.

**Fact.** For $a, b > 0$, $\lg a + \lg b \le 2 \lg(a + b) - 2$.

*Proof.* $ab \le ((a + b)/2)^2$ by the inequality of the arithmetic and geometric means, and taking $\lg$ gives $\lg a + \lg b \le 2 \lg(a + b) - 2$. $\square$

In each step, only $x$, its parent $y$ and (for a double step) its grandparent $z$ change their subtrees, so only their ranks change. After the step $x$ roots the subtree that $y$ (zig) or $z$ (double step) rooted, so $r'(x) = r(y)$ or $r'(x) = r(z)$. Also $r(x) \le r(y) \le r(z)$ before the step, since each subtree contains the one below it, and $r'(x) \ge r'(v)$ for each $v$ below $x$ after it.

**Zig.** The cost is 1, and $\Delta \Phi = r'(x) + r'(y) - r(x) - r(y) = r'(y) - r(x) \le r'(x) - r(x)$, since $r'(x) = r(y)$ and $r'(y) \le r'(x)$. So the amortized cost is at most $1 + (r'(x) - r(x)) \le 1 + 3(r'(x) - r(x))$.

**Zig-zig.** The cost is 2. With $r'(x) = r(z)$,
$$\Delta\Phi = r'(y) + r'(z) - r(x) - r(y) \le r'(x) + r'(z) - 2 r(x),$$
using $r'(y) \le r'(x)$ and $r(y) \ge r(x)$. Before the step, the subtree of $x$ holds $x$ and its two subtrees $A, B$; after it, $z$ holds $z$, the old sibling subtree of $y$ and the old other subtree of $z$. These two node sets are disjoint and lie inside the new subtree of $x$, so $s(x) + s'(z) \le s'(x)$. By the fact, $r(x) + r'(z) \le 2 r'(x) - 2$, that is $r'(z) \le 2 r'(x) - r(x) - 2$. So
$$2 + \Delta\Phi \le 2 + r'(x) + 2r'(x) - r(x) - 2 - 2r(x) = 3(r'(x) - r(x)).$$

**Zig-zag.** The cost is 2. With $r'(x) = r(z)$,
$$\Delta\Phi = r'(y) + r'(z) - r(x) - r(y) \le r'(y) + r'(z) - 2r(x),$$
using $r(y) \ge r(x)$. After the step $y$ and $z$ are the two children of $x$, so $s'(y) + s'(z) \le s'(x)$ and, by the fact, $r'(y) + r'(z) \le 2 r'(x) - 2$. So
$$2 + \Delta\Phi \le 2 r'(x) - 2 r(x) \le 3(r'(x) - r(x)),$$
since $r'(x) \ge r(x)$.

**The whole splay.** Let the steps be $1, \ldots, m$, with $r_0(x) = r(x)$ before the first and $r_m(x) = r(t)$ after the last, where $t$ is the root before the splay ($x$ ends with the subtree of the whole tree, whose weight is $s(t)$). Only the last step can be a zig. Adding the bounds of the steps, the sum telescopes:
$$\text{amortized cost} \le \sum_{j=1}^{m} 3\,(r_j(x) - r_{j-1}(x)) + 1 = 3\,(r(t) - r(x)) + 1.$$
If $x$ is already the root, the cost is 1 and $\Delta\Phi = 0$, which also meets the bound. $\blacksquare$

**Consequences.** With $w(i) = 1$ for all $n$ nodes, $r(t) = \lg n$ and $r(x) \ge 0$, so the amortized cost is at most $3 \lg n + 1$. For a sequence of $m$ splays, the actual cost is the amortized cost plus $\Phi_0 - \Phi_m$; with unit weights each rank lies between 0 and $\lg n$, so $\Phi_0 - \Phi_m \le n \lg n$, and the total is at most $m(3 \lg n + 1) + n \lg n$. In general $\lg w(i) \le r(i) \le \lg W$ with $W = \sum_i w(i)$, so the net drop of potential is at most $\sum_i \lg(W/w(i))$.
