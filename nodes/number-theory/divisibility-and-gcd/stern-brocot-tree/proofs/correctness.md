---
title: The Stern-Brocot tree holds each positive rational once, and its operations are correct
proves: [correctness]
status: full
---

A node is a quadruple $(a, b, c, d)$ of nonnegative integers. The root is $(0, 1, 1, 0)$, the left child of $(a, b, c, d)$ is $(a, b, a + c, b + d)$ and the right child is $(a + c, b + d, c, d)$. The value of the node is $(a + c)/(b + d)$, and we read $a/b$ and $c/d$ as its **left bound** and **right bound**, with $1/0 = +\infty$. We write $\sigma = a + b + c + d$.

**Lemma 1 (invariant).** Every node satisfies $bc - ad = 1$, $b \ge 1$, $c \ge 1$, and $a/b < (a + c)/(b + d) < c/d$; its value is in lowest terms and positive.

*Proof.* The root has $1 \cdot 1 - 0 \cdot 0 = 1$. For the left child, $b(a + c) - a(b + d) = bc - ad = 1$, and for the right child, $(b + d)c - (a + c)d = bc - ad = 1$. The entries $b$ and $c$ never decrease and start at 1. Then $(a + c) b - a (b + d) = bc - ad = 1 > 0$ gives $a/b < (a + c)/(b + d)$, and similarly $c(b + d) - d(a + c) = 1 > 0$ gives the other inequality (for $d = 0$ the right bound is $+\infty$). The relation $b \cdot (a + c) - a \cdot (b + d) = 1$ shows that any common divisor of $a + c$ and $b + d$ divides 1. The value is positive because $a + c \ge c \ge 1$. $\square$

**Lemma 2 (search tree).** Every node in the subtree of a node $x = (a, b, c, d)$ has its value strictly between $a/b$ and $c/d$; those in the left subtree are below the value of $x$, and those in the right subtree are above it. In particular, all values are distinct.

*Proof.* By induction on the depth below $x$, every node of the subtree has bounds in the closed interval $[a/b, c/d]$, since a child replaces one bound by the value of its parent, which lies between the parent's bounds by Lemma 1. Its value lies strictly between its own bounds, hence strictly between $a/b$ and $c/d$. The left child of $x$ has the right bound equal to the value of $x$, so its whole subtree lies below it; symmetrically for the right child. Two distinct nodes either lie in different subtrees of their lowest common ancestor, or one is an ancestor of the other, and in both cases their values differ. $\square$

**Lemma 3 (completeness).** Let $p, q \ge 1$ be coprime. The walk from the root that goes left when $p/q$ is smaller than the value and right when it is larger reaches the node with value $p/q$ after at most $p + q - 2$ steps.

*Proof.* While the value differs from $p/q$, Lemma 2 keeps $a/b < p/q < c/d$, so $bp - aq \ge 1$ and $cq - dp \ge 1$ as integers. Using $bc - ad = 1$,
$$(c + d)(bp - aq) + (a + b)(cq - dp) = p(bc - ad) + q(bc - ad) = p + q,$$
so $p + q \ge a + b + c + d = \sigma$. Each step increases $\sigma$ by $a + c$ or $b + d$, at least 1, and $\sigma = 2$ at the root, so after at most $p + q - 2$ steps the walk is at a node whose value is $p/q$. $\square$

Lemmas 1 to 3 together say that the map from nodes to values is a bijection onto the positive rationals, with each value in lowest terms.

**Lemma 4 (runs).** From a node with bounds $(a, b, c, d)$, $k$ right moves lead to the bounds $(a + kc, b + kd, c, d)$, and $k$ left moves to $(a, b, c + ka, d + kb)$.

*Proof.* A right move keeps $c, d$ and replaces $(a, b)$ by $(a + c, b + d)$; after $k$ of them, $(a, b)$ has gained $k(c, d)$. Left moves are symmetric. $\square$

So DECODE (lines L8 to L11) returns the node at the end of the path.

**Lemma 5 (ENCODE).** For $p, q \ge 1$, ENCODE$(p, q)$ returns the path to the node with value $p/q$.

*Proof.* Let $p/q = [k_0; k_1, \ldots, k_m]$ be the continued fraction produced by Euclid's algorithm, so $k_0 \ge 0$, $k_i \ge 1$ for $0 < i < m$, and $k_m \ge 2$ when $m \ge 1$ (the last quotient of Euclid is at least 2 because the last two remainders satisfy $r_{m} = k_m r_{m+1}$ and $r_m > r_{m+1}$); if $m = 0$, then $p/q = k_0 \ge 1$. These quotients depend only on the value $p/q$. Lines L2 to L6 compute exactly $k_0, \ldots, k_m$, decrease $k_m$ by 1, and emit $(R, k_0), (L, k_1), (R, k_2), \ldots$, dropping runs of length 0.

It remains to show that the search walk for $x = p/q$ is $R^{k_0} L^{k_1} R^{k_2} \cdots$ with the last run of length $k_m - 1$. At a node with bounds $(a, b, c, d)$, the map $t \mapsto (a + ct)/(b + dt)$ is increasing on $t \ge 0$ (its derivative has the sign of $bc - ad = 1$), runs from $a/b$ to $c/d$, and takes the value of the node at $t = 1$. So every $x$ with $a/b < x < c/d$ is $(a + ct)/(b + dt)$ for exactly one real $t > 0$, the **coordinate** of $x$ at that node, and the walk goes right if $t > 1$, left if $t < 1$, and stops if $t = 1$. At the root, the coordinate of $x$ is $x$ itself.

- After a right move, the bounds are $(a + c, b + d, c, d)$ and $x = (a + c + ct')/(b + d + dt')$ with $t' = t - 1$.
- After a left move, the bounds are $(a, b, a + c, b + d)$ and $x = (a + (a + c)t')/(b + (b + d)t')$ with $t = t'/(1 + t')$, that is, $1/t' = 1/t - 1$.

So, writing $s = 1/t$ while the walk goes left, the walk is: go right and subtract 1 from $t$ while $t > 1$; go left and subtract 1 from $s$ while $s > 1$; stop when the current coordinate is 1. We prove by induction on $m$ that, for $t = [k_0; k_1, \ldots, k_m]$ with $k_m \ge 2$ when $m \ge 1$ and $t \ge 1$ when $m = 0$, this process makes $k_0$ moves in the first direction, then $k_1$ in the other, and so on, with $k_m - 1$ in the last run. If $m = 0$, then $t = k_0$ is an integer, and it makes $k_0 - 1$ moves before $t = 1$. If $m \ge 1$, then $k_0 < t < k_0 + 1$, so it makes exactly $k_0$ moves and reaches $t = [0; k_1, \ldots, k_m] < 1$, and from there it continues in the other direction with $s = 1/t = [k_1; k_2, \ldots, k_m] > 1$, where the induction hypothesis applies. With $t = x = p/q$ at the root and the first direction $R$, this is the output of ENCODE. Euclid's algorithm takes $O(1 + \log \min(p, q))$ steps by Lamé's theorem, so ENCODE is fast even when the depth is large. $\square$

**Lemma 6 (PARENT).** For a node $x \ne$ root with bounds $(a, b, c, d)$, line L13 returns the bounds of its parent.

*Proof.* If $x$ is the right child of $y = (a', b', c', d')$, then $(a, b) = (a' + c', b' + d')$ and $(c, d) = (c', d')$, so $a + b = a' + b' + c' + d' > c' + d' = c + d$ because $a' + b' \ge b' \ge 1$, and $y = (a - c, b - d, c, d)$. If $x$ is the left child, then $(c, d) = (a' + c', b' + d')$ and $(a, b) = (a', b')$, so $c + d > a + b$ because $c' + d' \ge c' \ge 1$, and $y = (a, b, c - a, d - b)$. The two cases are told apart by comparing $a + b$ with $c + d$, which is what line L13 does. Only the root has bounds $(0, 1, 1, 0)$, since every other node has $\sigma > 2$; line L12 handles it. $\square$

**Lemma 7 (BEST-APPROXIMATION).** For $x = u/v$ with $u \ge 0$, $v \ge 1$, and $N \ge 1$, BEST-APPROXIMATION returns a fraction $p/q$ in lowest terms with $1 \le q \le N$ that minimizes $|x - p/q|$, and the smaller of two such fractions on a tie.

*Proof.* **Invariant:** the current bounds satisfy $bc - ad = 1$, $b \le N$, $a/b \le x < c/d$ with $a/b < x$ unless $(a, b) = (0, 1)$, and $x$ is not the value of any node visited so far. It holds at the start since $0 \le x < 1/0$.

In an iteration, the value $m = (a + c)/(b + d)$ has $b + d \le N$. If $m = x$, line L16 returns $m$, which is in lowest terms by Lemma 1 and is at distance 0. If $m < x$, every $k$ with $(a + kc)/(b + kd) < x$ and $b + kd \le N$ is allowed, $k = 1$ among them. The fraction $(a + kc)/(b + kd)$ is increasing in $k$ (because $bc - ad = 1 > 0$), so these $k$ form an initial segment, and the condition $(a + kc) v < u (b + kd)$ is $k(cv - ud) < ub - av$, where $cv - ud > 0$ by $x < c/d$; this gives the largest $k$ as $\lfloor (ub - av - 1)/(cv - ud) \rfloor$, capped by $\lfloor (N - b)/d \rfloor$ if $d > 0$. By Lemma 4 the new bounds are those of a node of the tree, and the invariant holds, the new left bound being below $x$. If $m > x$, the argument is symmetric with $(c + ka)/(d + kb)$ decreasing in $k$ and the condition $k(ub - av) < cv - ud$, where $ub - av \ge 0$, with equality only when $(a, b) = (0, 1)$ and $x = 0$, in which case the condition holds for all $k$. The new right bound stays above $x$, and $d + kb \le N$.

The loop ends. A left move increases $d$ by $kb \ge 1$, and a right move increases $b$ by $kd \ge 1$ unless $d = 0$. A right move with $d = 0$ is not capped by $N$, so its $k$ is the largest one with $(a + kc)/(b + kd) < x$, and the next node is at least $x$: the next iteration returns or moves left. So $b + d$ grows at least every second iteration and eventually exceeds $N$. When it ends without returning, $b + d > N$ and $a/b \le x < c/d$.

Now suppose $p/q$ is a fraction with $a/b < p/q < c/d$. Then $bp - aq \ge 1$ and $cq - dp \ge 1$, and as in Lemma 3, $q = b(cq - dp) + d(bp - aq)$... precisely, $q(bc - ad) = b(cq - dp) + d(bp - aq) \ge b + d > N$. So no fraction with denominator at most $N$ lies strictly between $a/b$ and $c/d$. Every candidate $p/q \le a/b$ is at distance at least $x - a/b$ from $x$, and every candidate $p/q \ge c/d$ is at distance at least $c/d - x$; both bounds have denominators at most $N$ when finite ($b \le N$, and $d \le N$ when $d \ge 1$). So the nearest candidates are $a/b$ and $c/d$, and line L19 picks the nearer, comparing $(ub - av) d$ with $(cv - ud) b$, which are $bdv$ times the two distances. If $d = 0$, then $c/d = +\infty$ and $a/b$ is the answer. On a tie it returns $a/b$, the smaller one, and $a/b$ is in lowest terms because $bc - ad = 1$. $\blacksquare$
