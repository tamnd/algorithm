---
title: The two passes compute the weighted 8-neighbor path distance, which equals a(M − m) + bm, and the 3-4 transform is within a factor of √10/3 and 2√2/3 of the Euclidean distance
proves: [correctness, closed-form, error-bound]
status: full
---

**Setting.** The image is the rectangle $R = \{0, \dots, W-1\} \times \{0, \dots, H-1\}$ with a nonempty set $S \subseteq R$ of feature pixels. The weights are integers with $0 < a \le b \le 2a$. A step is a move from a pixel to one of its 8 neighbors inside $R$; an axial step (to an edge neighbor) costs $a$ and a diagonal step (to a corner neighbor) costs $b$. For a displacement $(\Delta x, \Delta y)$ let $M = \max(|\Delta x|, |\Delta y|)$, $m = \min(|\Delta x|, |\Delta y|)$ and

$$g(\Delta x, \Delta y) = a(M - m) + bm.$$

The claim is that the algorithm returns $d(p) = \min_{q \in S} g(p - q)$ at every pixel $p$.

**Lemma 1 (no path is cheaper than g).** Every sequence of steps from $q$ to $p$, inside $R$ or not, costs at least $g(p - q)$.

*Proof.* Let the path have $\alpha$ axial and $\delta$ diagonal steps. Each step changes each coordinate by at most 1, so $\alpha + \delta \ge M$. An axial step changes $|\Delta x| + |\Delta y|$ by at most 1 and a diagonal step by at most 2, so $\alpha + 2\delta \ge M + m$. Then

$$a\alpha + b\delta = (2a - b)(\alpha + \delta) + (b - a)(\alpha + 2\delta) \ge (2a - b)M + (b - a)(M + m) = a(M - m) + bm,$$

where the inequality uses $2a - b \ge 0$ and $b - a \ge 0$. $\square$

**Lemma 2 (every value is the cost of a path).** At every moment of the algorithm, each finite value $d(p)$ is the cost of some path of steps inside $R$ from a feature pixel to $p$. Hence $d(p) \ge \min_{q \in S} g(p - q)$ at every moment.

*Proof.* Line L1 sets $d = 0$ on $S$, the cost of the empty path, and $\infty$ elsewhere. Lines L4 and L7 replace $d(p)$ only by $d(r) + w$, where $r$ is a neighbor of $p$ inside $R$ and $w$ is the cost of the step from $r$ to $p$; a path to $r$ followed by this step is a path to $p$. The second claim follows from Lemma 1. $\square$

**Lemma 3 (a monotone path of cost g).** For $q, p \in R$ there is a path from $q$ to $p$ of cost $g(p - q)$ that stays in the bounding box of $q$ and $p$, and whose steps are all forward steps followed by all backward steps, where the forward steps are the displacements $(1, 0), (1, 1), (0, 1), (-1, 1)$ and the backward steps are their negatives.

*Proof.* Let $s_x = \operatorname{sign}(\Delta x)$ and $s_y = \operatorname{sign}(\Delta y)$. Take $m$ diagonal steps $(s_x, s_y)$ and $M - m$ axial steps along the longer axis, $(s_x, 0)$ if $|\Delta x| \ge |\Delta y|$ and $(0, s_y)$ otherwise. They add up to $(\Delta x, \Delta y)$ and cost $g$. Every step moves each coordinate toward $p$ or leaves it, so every prefix of the sequence, in any order, ends in the bounding box, which lies in $R$ because $R$ is a rectangle. Each of the 8 step directions is either forward or backward, since the forward set and its negative partition the 8 directions. So put the forward steps first. $\square$

**Lemma 4 (what each pass propagates).** (a) After the forward pass, $d(p) \le d_0(r) + c$ for every path from $r$ to $p$ inside $R$ of forward steps with cost $c$, where $d_0$ is the value after line L1. (b) After the backward pass, $d(p) \le d_1(r) + c$ for every path from $r$ to $p$ inside $R$ of backward steps with cost $c$, where $d_1$ is the value after the forward pass.

*Proof.* (a) A forward step from $u$ to $u'$ means $u = u' - s$ with $s$ a forward displacement, so $u$ is the left, upper left, upper or upper right neighbor of $u'$, which comes before $u'$ in raster order. Line L4 at $u'$ reads the final forward pass value of $u$ and so sets $d(u') \le d(u) + w$. By induction along the path, $d(p) \le d_0(r) + c$; values only decrease, so this stays true to the end of the pass. (b) The same with the reverse raster order: a backward step from $u$ to $u'$ comes from the right, lower right, lower or lower left neighbor of $u'$, which line L7 has already finished. $\square$

**Theorem 5 (the algorithm is correct).** The returned $d(p)$ equals $\min_{q \in S} g(p - q)$, which is also the shortest path distance from $S$ to $p$ in the weighted 8-neighbor graph on $R$.

*Proof.* Let $q \in S$ and take the path of Lemma 3, with the forward part from $q$ to an intermediate pixel $r$ of cost $c_1$ and the backward part from $r$ to $p$ of cost $c_2$, with $c_1 + c_2 = g(p - q)$. By Lemma 4(a), $d_1(r) \le 0 + c_1$, and by Lemma 4(b), the final $d(p) \le d_1(r) + c_2 \le g(p - q)$. So $d(p) \le \min_q g(p - q)$, and Lemma 2 gives the reverse inequality. Lemmas 1 and 3 show that $\min_q g(p - q)$ is the graph distance. $\square$

With $(a, b) = (1, 2)$, $g = M + m = |\Delta x| + |\Delta y|$, the city block distance. With $(a, b) = (1, 1)$, $g = M$, the chessboard distance.

**Theorem 6 (the error of the 3-4 transform).** Let $(a, b) = (3, 4)$, let $c$ be the result at a pixel $p$, and let $E = \min_{q \in S} |p - q|^2$ be the exact squared Euclidean distance. Then

$$8E \le c^2 \le 10E,$$

so $c/3$ lies between $\tfrac{2\sqrt{2}}{3} e \approx 0.9428\,e$ and $\tfrac{\sqrt{10}}{3} e \approx 1.0541\,e$, with $e = \sqrt{E}$. Both bounds are reached.

*Proof.* For one displacement, $g = 3(M - m) + 4m = 3M + m$ and $|p - q|^2 = M^2 + m^2$. Then

$$g^2 - 8(M^2 + m^2) = M^2 + 6Mm - 7m^2 = (M - m)(M + 7m) \ge 0,$$

$$10(M^2 + m^2) - g^2 = M^2 - 6Mm + 9m^2 = (M - 3m)^2 \ge 0.$$

For the minimum over $S$: $c^2 = \min_q g_q^2 \ge \min_q 8E_q = 8E$, and with $q^*$ a feature at squared distance $E$, $c^2 \le g_{q^*}^2 \le 10E$. Equality in the first holds for $M = m$, as at $(1, 1)$, where $c = 4$ and $E = 2$; in the second for $M = 3m$, as at $(3, 1)$, where $c = 10$ and $E = 10$. $\blacksquare$
