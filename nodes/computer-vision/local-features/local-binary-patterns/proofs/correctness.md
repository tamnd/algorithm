---
title: Correctness of local binary patterns
proves: [correctness]
status: full
---

Fix $P \ge 1$ and $R > 0$. For a center $c$ let $g_c$ be its value and $g_0, \dots, g_{P-1}$ the values of its neighbors, taken from pixels or by bilinear interpolation. Write $b_p = s(g_p - g_c)$, with $s(x) = 1$ for $x \ge 0$ and $0$ otherwise, so the code is $\sum_p b_p 2^p$. Indices of bits are taken modulo $P$. A rotation of a code by $k$ is the code with bits $b'_p = b_{p - k}$.

**Lemma 1 (the algorithm computes the defined histogram).** LBP returns, for each label $\ell$, the number of pixels $c$ with the circle inside the image and $\mathrm{map}(\mathrm{LBP}_{P,R}(c)) = \ell$.

*Proof.* Line L1 computes the offsets of the definition. For a fixed $c$, line L4 sets the code to 0, and after the iteration $p$ of lines L5 to L7 the code equals $\sum_{q \le p} b_q 2^q$, since line L7 adds $2^p$ exactly when $g_p - g_c \ge 0$. After the loop the code is $\mathrm{LBP}_{P,R}(c)$. Line L8 adds 1 to the bin of its label. Line L3 visits each pixel with its circle inside the image once, so each such pixel adds 1 to exactly one bin, the bin of its label. $\square$

**Lemma 2 (gray-scale invariance).** Let $f$ be strictly increasing. If all neighbors are pixel centers, the image $f(I)$ has the same codes as $I$. With interpolation, the same holds for $f(x) = a x + b$ with $a > 0$.

*Proof.* If $g_p$ and $g_c$ are pixel values, $f(g_p) \ge f(g_c)$ holds exactly when $g_p \ge g_c$, since $f$ is strictly increasing. So each bit is the same. Bilinear interpolation is a weighted sum $\sum_k w_k x_k$ with weights $w_k \ge 0$ and $\sum_k w_k = 1$. So the interpolated value of $a I + b$ is $a g_p + b$, and $a g_p + b - (a g_c + b) = a (g_p - g_c)$ has the sign of $g_p - g_c$ for $a > 0$. So each bit is the same. $\square$

**Lemma 3 (uniform codes).** For $P \ge 2$ there are exactly $P(P - 1) + 2$ codes with $U \le 2$. The u2 mapping has $P(P - 1) + 3$ labels.

*Proof.* $U$ counts the positions $p$ with $b_p \ne b_{p-1}$ on a circle, so $U$ is even. The codes with $U = 0$ are the two constant codes. A code with $U = 2$ has exactly one run of ones and one run of zeros on the circle. It is fixed by the start of the run of ones ($P$ choices) and the length of the run, from 1 to $P - 1$ ($P - 1$ choices), and different choices give different codes. So there are $P(P - 1)$ such codes, and $P(P - 1) + 2$ uniform codes. The u2 mapping gives each one its own label and adds one shared label. $\square$

**Lemma 4 (riu2).** $U$ and the number of ones do not change under rotation of the code. Two uniform codes with the same number $k$ of ones are rotations of each other. So riu2 is constant on rotation classes, and it has exactly $P + 2$ labels.

*Proof.* A rotation moves the bits around the circle and keeps both the multiset of bits and the set of adjacent pairs, so it keeps the number of ones and $U$. So the riu2 label, which depends only on these two numbers, is constant on a rotation class. A uniform code with $0 < k < P$ ones is one run of $k$ ones, and any two runs of the same length differ by a rotation. The constant codes are the only codes with $k = 0$ and $k = P$. So the uniform codes give the labels $0, \dots, P$, each one used, and the other codes give the label $P + 1$, which is used for $P \ge 4$ (the code $0101\dots$ restricted to the first four bits, with the other bits 0, has $U = 4$). This gives $P + 2$ labels. $\square$

**Lemma 5 (rotation by 90 degrees).** Let $4$ divide $P$ and let $J$ be the image $I$ turned by 90 degrees, so that the pixel at the offset $(\Delta u, \Delta v)$ from a center goes to the offset $(\Delta v, -\Delta u)$ from the new center. Then the code of each center in $J$ is the rotation by $P/4$ of the code of the same center in $I$.

*Proof.* Neighbor $p$ is at the angle $\alpha_p = 2\pi p / P$, at the offset $(R\cos\alpha_p, -R\sin\alpha_p)$. The turn maps it to $(-R\sin\alpha_p, -R\cos\alpha_p) = (R\cos(\alpha_p + \pi/2), -R\sin(\alpha_p + \pi/2))$, which is the offset of neighbor $p + P/4$. The turn maps the grid to itself and each unit cell to a unit cell. Bilinear interpolation in a cell is the unique function of the form $\alpha + \beta x + \gamma y + \delta x y$ that takes the four corner values, and this form is kept by the map $(x, y) \mapsto (y, -x)$. So the interpolated value of $J$ at the new position equals the interpolated value of $I$ at the old position. So bit $p + P/4$ of the new code equals bit $p$ of the old code. $\square$

**Theorem.** LBP returns the histogram of the labels of the codes. The codes are invariant under the changes of Lemma 2. For $P = 8$ the u2, riu2 and ri mappings have 59, 10 and 36 labels. If $4$ divides $P$, the riu2 and ri histograms do not change when the image turns by 90 degrees.

*Proof.* Lemma 1 gives the histogram and Lemma 2 the invariance. Lemma 3 gives $8 \cdot 7 + 3 = 59$ and Lemma 4 gives $8 + 2 = 10$. The ri labels are the rotation classes of 8-bit strings, the binary necklaces of length 8. By Burnside's lemma their number is $\frac{1}{8}\sum_{d \mid 8} \varphi(d) 2^{8/d} = \frac{1}{8}(256 + 16 + 2 \cdot 4 + 4 \cdot 2) = 36$. By Lemma 5 each code of the turned image is a rotation of a code of the original image, and the turned image has the same set of centers with the circle inside. By Lemma 4, riu2 is constant on rotation classes, and so is ri by its definition. So each pixel adds 1 to the same bin in both histograms. $\square$

The code rounds $g_p - g_c$ to 9 decimals before the sign test. In exact arithmetic Lemma 5 is exact. In floating point the two interpolations can round differently, and the rounding keeps a difference that is zero in exact arithmetic at zero in both images.
