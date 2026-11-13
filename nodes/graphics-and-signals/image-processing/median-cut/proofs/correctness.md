---
title: Median cut returns min(k, D) distinct palette colors, its median split halves distinct values, and its error is at least the optimum with no bounded ratio
proves: [correctness]
status: full
---

Let the input be colors $c_1, \ldots, c_n \in \mathbb{R}^d$ with $D$ distinct values, and $k \ge 1$. A *box* is a nonempty list of input colors. Write $\mathrm{ext}_a(b) = \max_{c \in b} c_a - \min_{c \in b} c_a$.

**Invariant.** Before each test of line L2, (i) the boxes of $B$ are nonempty and together hold every input color exactly once, (ii) two equal colors are in the same box, and (iii) for any two boxes $b \ne b'$ there is an axis $a$ and a value $m$ such that one box has all $c_a < m$ and the other has all $c_a \ge m$, or one has all $c_a \le m$ and the other all $c_a > m$.

*Proof.* At the start, $B$ holds one box with all colors, and (i) to (iii) hold. Suppose they hold, and line L8 splits a box $b$ with $\mathrm{ext}_a(b) > 0$ (line L4 did not stop). Let $m$ be the value of line L6. The value $m$ is the coordinate of a color of $b$, so $\min_b c_a \le m \le \max_b c_a$.

- If some color of $b$ has $c_a < m$, then $L = \{c_a < m\}$ is nonempty and $R = \{c_a \ge m\}$ holds the color that gave $m$.
- Otherwise $m = \min_b c_a$; then $L = \{c_a \le m\}$ holds that color, and $R = \{c_a > m\}$ holds a color with $c_a = \max_b c_a > m$, which exists because the extent is positive.

In both cases $L$ and $R$ are nonempty and split $b$, which gives (i). The rule depends only on $c_a$, so equal colors go to the same side, which gives (ii). The new pair $L, R$ is separated by $(a, m)$, and a pair $L, b'$ or $R, b'$ is separated by the plane that separated $b$ and $b'$, because $L, R \subseteq b$. This gives (iii). $\square$

**Claim 1 (palette size).** The loop ends with $|B| = \min(k, D)$, and the means of the boxes are pairwise distinct, so the palette has $\min(k, D)$ colors.

*Proof.* Each pass of the loop that does not stop adds one box. By (i) and (ii), each distinct color is in exactly one box and each box holds at least one distinct color, so $|B| \le D$ at all times. A box with a positive extent on some axis holds two distinct colors. So line L4 stops only when every box holds one distinct color, that is when $|B| = D$ by (ii). The loop therefore ends either at line L2 with $|B| = k \le D$, or at line L4 with $|B| = D < k$. In both cases $|B| = \min(k, D)$.

For two boxes $b, b'$, take the plane $(a, m)$ of (iii). The mean of a box lies in the convex hull of its colors, so if all $c_a < m$ in $b$ then the mean of $b$ has coordinate $a$ less than $m$, and if all $c_a \ge m$ in $b'$ then the mean of $b'$ has coordinate $a$ at least $m$. The other form of (iii) works the same way with $\le$ and $>$. So the two means differ in coordinate $a$. $\square$

**Claim 2 (the split halves distinct values).** If the values $c_a$ in $b$ are pairwise distinct, then $|L| = \lfloor |b|/2 \rfloor$ and $|R| = \lceil |b|/2 \rceil$.

*Proof.* After the sort of line L5, the color at position $h = \lfloor |b|/2 \rfloor$ (counting from 0) has value $m$, and since the values are distinct, exactly the $h$ colors before it have $c_a < m$. If $h \ge 1$, $L$ is these $h$ colors. The case $h = 0$ needs $|b| = 1$, which has extent 0 and is never split. $\square$

**Claim 3 (lower bound and no bounded ratio).** Let $\mathrm{OPT}_k$ be the least error $\sum_i |c_i - p_{j(i)}|^2$ over all palettes of at most $k$ colors and all maps $j$. The error of median cut is at least $\mathrm{OPT}_k$, and there is no constant $C$ with error $\le C \cdot \mathrm{OPT}_k$ on all inputs with $\mathrm{OPT}_k > 0$.

*Proof.* Median cut outputs a palette of at most $k$ colors and a map, so its error is one of the values in the minimum, which proves the first part.

For the second part, take $d = 1$ (or colors with only the red channel nonzero), the colors $0, 1, 2, 3, M$ with $M \ge 12$, and $k = 2$. The red extent is $M > 0$; after the sort, position 2 has $m = 2$, so $L = \{0, 1\}$ and $R = \{2, 3, M\}$, with means $p_1 = 1/2$ and $p_2 = (M + 5)/3$. In line L10, the color 2 is at distance $3/2$ from $p_1$ and $(M - 1)/3 \ge 11/3$ from $p_2$; the color 3 is at $5/2$ from $p_1$ and $(M - 4)/3 \ge 8/3$ from $p_2$; the color $M$ is at $(2M - 5)/3$ from $p_2$, which is less than $M - 1/2$. So 0, 1, 2, 3 map to $p_1$ and $M$ to $p_2$, and the error is

$$
\tfrac{1}{4} + \tfrac{1}{4} + \tfrac{9}{4} + \tfrac{25}{4} + \Big( \frac{2M - 5}{3} \Big)^2 = 9 + \Big( \frac{2M - 5}{3} \Big)^2 .
$$

The palette $\{3/2, M\}$ with the groups $\{0, 1, 2, 3\}$ and $\{M\}$ has error $\frac{9}{4} + \frac{1}{4} + \frac{1}{4} + \frac{9}{4} = 5$, so $0 < \mathrm{OPT}_2 \le 5$. The ratio is at least $(9 + ((2M - 5)/3)^2) / 5$, which grows without a bound as $M \to \infty$. $\square$

**Remark (nearest mapping).** For a fixed palette, mapping every color to its nearest palette color minimizes the error over all maps, so line L10 is never worse than mapping each color to the mean of its own box. In the other direction, for a fixed partition into groups, the mean of each group minimizes the sum of squared distances within it. So $\mathrm{OPT}_k$ is also the least, over partitions of the colors into at most $k$ groups, of the sum of the squared distances to the group means, which is how the tests compute it by trying every partition.
