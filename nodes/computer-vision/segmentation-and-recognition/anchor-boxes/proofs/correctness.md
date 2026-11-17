---
title: The anchor grid has the stated shapes and centers, and the IoU of an object with its nearest anchor has closed forms for size, shape and position errors
proves: [correctness]
status: full
---

A box is $(x_1, y_1, x_2, y_2)$ with $x_1 < x_2$ and $y_1 < y_2$, and its area is $(x_2 - x_1)(y_2 - y_1)$. For two boxes $A$ and $B$ write $\operatorname{IoU}(A, B) = |A \cap B| / |A \cup B|$ with $|A \cup B| = |A| + |B| - |A \cap B|$.

**Claim 1 (the grid).** ANCHORS returns $W_f H_f |S| |R|$ boxes. The box for position $(u, v)$ and the shape of size $\sigma$ and ratio $r$ has center $((u + o)s, (v + o)s)$, width $\sigma / \sqrt r$, height $\sigma \sqrt r$, area $\sigma^2$ and ratio $h / w = r$.

*Proof.* Line L2 appends one shape for each pair $(\sigma, r)$, so $B$ has $|S||R|$ shapes. The loop of line L4 runs once for each of the $W_f H_f$ positions, and line L6 appends one box for each shape, so the count is $W_f H_f |S||R|$. The box of line L6 has $x_2 - x_1 = w$, $y_2 - y_1 = h$ and the midpoint $(c_x, c_y)$ of line L5. Its area is $(\sigma / \sqrt r)(\sigma \sqrt r) = \sigma^2$ and its ratio is $\sigma\sqrt r / (\sigma / \sqrt r) = r$. $\square$

In Claims 2 to 4 two boxes have the same center, so each box is fixed by its width and height. Two such boxes with sizes $(w_1, h_1)$ and $(w_2, h_2)$ overlap in a box of size $\min(w_1, w_2) \times \min(h_1, h_2)$, since along each axis the shorter interval lies inside the longer one.

**Claim 2 (size error).** Two centered boxes with the same ratio and sizes $\sigma_1 \le \sigma_2$ have IoU $(\sigma_1 / \sigma_2)^2$.

*Proof.* With the same ratio, box 1 has width and height $\sigma_1 / \sigma_2$ times those of box 2, so it lies inside box 2. The intersection is box 1 and the union is box 2, and the IoU is $\sigma_1^2 / \sigma_2^2$. $\square$

**Corollary (octave sizes).** Let the square sizes be $\sigma, 2\sigma, 4\sigma, \dots$ and let a centered square have side $x$ with $\sigma \le x \le 2^m \sigma$. Then its best IoU with the anchors is at least $1/2$.

*Proof.* Pick $j$ with $2^j \sigma \le x \le 2^{j+1} \sigma$. By Claim 2 the two anchors give $(2^j \sigma / x)^2$ and $(x / 2^{j+1} \sigma)^2$. The first falls and the second rises as $x$ grows, and they are equal at $x = 2^j \sigma \sqrt 2$, where both are $1/2$. So the larger of the two is at least $1/2$ for every $x$ in the interval. $\square$

**Claim 3 (shape error).** Two centered boxes of area $\sigma^2$ with ratios $r_1 \le r_2$ and $q = r_2 / r_1$ have IoU $1/(2\sqrt q - 1)$.

*Proof.* Box $i$ has width $\sigma / \sqrt{r_i}$ and height $\sigma \sqrt{r_i}$. Since $r_1 \le r_2$, box 2 is the narrower and box 1 is the shorter, so the intersection has width $\sigma / \sqrt{r_2}$ and height $\sigma \sqrt{r_1}$, and area $\sigma^2 \sqrt{r_1 / r_2} = \sigma^2 / \sqrt q$. The union is $2\sigma^2 - \sigma^2 / \sqrt q$. Dividing, the IoU is $(1/\sqrt q) / (2 - 1/\sqrt q) = 1/(2\sqrt q - 1)$. $\square$

For $q = 2$ the IoU is $1/(2\sqrt 2 - 1) \approx 0.547$, and for $q = 4$ it is $1/3$.

**Claim 4 (position error).** Let $G$ and $A$ be squares of side $\sigma$ whose centers differ by $d_x$ and $d_y$ with $0 \le d_x, d_y \le \sigma$. Then $\operatorname{IoU}(G, A) = p / (2\sigma^2 - p)$ with $p = (\sigma - d_x)(\sigma - d_y)$, and this value does not increase when $d_x$ or $d_y$ grows.

*Proof.* Along $x$ the two intervals have length $\sigma$ and start $d_x$ apart, so they overlap in a length $\sigma - d_x \ge 0$; the same holds along $y$. So $|G \cap A| = p$ and $|G \cup A| = 2\sigma^2 - p$. The function $p \mapsto p/(2\sigma^2 - p)$ has derivative $2\sigma^2/(2\sigma^2 - p)^2 > 0$ on $0 \le p \le \sigma^2$, so it grows with $p$, and $p$ does not grow when $d_x$ or $d_y$ grows. $\square$

**Corollary (stride).** Let the anchors be squares of side $\sigma$ centered at the points $((u + o)s, (v + o)s)$ for all integers $u$ and $v$, with $s \le 2\sigma$. Then every square $G$ of side $\sigma$ has an anchor with IoU at least $p^* / (2\sigma^2 - p^*)$, $p^* = (\sigma - s/2)^2$, and a square centered at $((u + o + 1/2)s, (v + o + 1/2)s)$ has no anchor with a higher IoU.

*Proof.* Rounding the center of $G$ to the nearest grid point in each axis gives an anchor with $d_x, d_y \le s/2$, and Claim 4 gives the bound. For the square at the middle of four grid points, every anchor has $d_x \ge s/2$ and $d_y \ge s/2$, so by Claim 4 none does better than $d_x = d_y = s/2$. $\square$

For $\sigma = 32$ this gives $24^2 / (2048 - 576) = 576/1472 \approx 0.391$ at $s = 16$ and $30^2/(2048 - 900) = 900/1148 \approx 0.784$ at $s = 4$.

**On the k-means of YOLOv2.** The assignment step puts each box in the cluster with the smallest distance $1 - \operatorname{IoU}$, so it does not raise the total distance for fixed centers. The update step replaces each center by the mean width and height of its members. For the squared Euclidean distance the mean is the minimizer, which is why plain k-means never raises its objective. For $1 - \operatorname{IoU}$ the mean is not always the minimizer, so the total distance can rise in an update step, and the loop has no proof of termination. The code stops at a fixed point of the assignment or after a set number of rounds, so it always stops; the tests check its result on planted clusters, not a general guarantee.
