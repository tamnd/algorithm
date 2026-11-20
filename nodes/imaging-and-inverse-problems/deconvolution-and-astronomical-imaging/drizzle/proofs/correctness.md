---
title: Drizzle is a weighted mean of the drops, it keeps the weighted flux, and its special cases are shift-and-add and interlacing
proves: [correctness]
status: full
---

**Setting.** Input pixel $i$ (of any frame) has the value $d_i$ (counts per input pixel), the weight $w_i \ge 0$ and, after the geometric transform, the drop $\Delta_i$: a square of side $p$ around the transformed pixel center. Here the transform is a shift, so $\Delta_i$ is an axis-aligned square of area $p^2$. Output pixel $o$ is the square $Q_o$ of side $s$. Lines L1 to L8 compute

$$a_{io} = |\Delta_i \cap Q_o|, \qquad W_o = \sum_i a_{io} w_i, \qquad I_o = \begin{cases} s^2 \dfrac{\sum_i a_{io} w_i d_i}{W_o} & W_o > 0, \\ 0 & W_o = 0. \end{cases}$$

The code adds the drops one at a time, so after all drops the two sums are the ones above; the order of the additions does not change them.

**Claim 1 (overlap areas).** For axis-aligned squares, $a_{io} = \ell_x \ell_y$, where $\ell_x$ and $\ell_y$ are the lengths of the intersections of the projections on the two axes, and $\ell(a_0, a_1, b_0, b_1) = \max(0, \min(a_1, b_1) - \max(a_0, b_0))$. The loop of line L4 visits every $o$ with $a_{io} > 0$.

*Proof.* The intersection of two axis-aligned rectangles is the product of the intersections of their sides, which are intervals; the length of $[a_0, a_1] \cap [b_0, b_1]$ is the formula. Output column $J$ covers $[Js, (J+1)s]$, and it meets $[x_0, x_1]$ in a set of positive length only if $Js < x_1$ and $(J+1)s > x_0$, that is $\lfloor x_0/s \rfloor \le J \le \lceil x_1/s \rceil - 1$; the same holds for the rows. $\square$

The test compares the areas with a brute force count of lattice cells of side $1/20$, which is exact when all edges lie on the lattice.

**Claim 2 (weighted mean).** If $W_o > 0$, $I_o/s^2$ is a convex combination of the values $d_i$ of the drops that overlap $Q_o$ with $w_i > 0$. In particular, if all such $d_i$ equal $c$, then $I_o = c s^2$.

*Proof.* The coefficients $a_{io}w_i/W_o$ are nonnegative and sum to $1$. $\square$

So a flat input of $c$ counts per input pixel gives $c s^2$ counts per output pixel: the surface brightness is kept, for any shifts, any $p$ and any weights.

**Claim 3 (weighted flux).** If every drop lies inside the output grid, then

$$\sum_o W_o I_o = s^2 p^2 \sum_i w_i d_i, \qquad \sum_o W_o = p^2 \sum_i w_i.$$

*Proof.* For $W_o > 0$, $W_o I_o = s^2 \sum_i a_{io}w_i d_i$, and for $W_o = 0$ both sides are $0$ because then $a_{io}w_i = 0$ for all $i$. Sum over $o$ and swap the sums: $\sum_o a_{io} = |\Delta_i| = p^2$, because the output pixels tile the plane and the drop lies inside the grid. The second identity is the same with $d_i = 1$. $\square$

With equal weights, $\sum_o W_o I_o / \sum_o W_o = s^2 \cdot$ the mean input value: the flux of the input, measured in counts per output pixel, is kept in the weighted sense. The plain sum $\sum_o I_o$ is the total flux only where the output pixels are covered with a uniform weight.

**Claim 4 (linearity).** For fixed shifts, $p$, $s$ and weights, $I$ is a linear function of the data $d$, and $W$ does not depend on $d$.

*Proof.* $a_{io}$ and $w_i$ do not depend on $d$, and $I_o$ is a fixed linear combination of the $d_i$. $\square$

**Claim 5 (shift-and-add).** With $s = p = 1$, integer shifts and unit weights, $I_o$ is the mean of the input values whose pixels land exactly on $Q_o$.

*Proof.* A drop of side $1$ shifted by integers is exactly one output pixel, so $a_{io} \in \{0, 1\}$ and $I_o = \sum_{i \to o} d_i / \#\{i \to o\}$. $\square$

**Claim 6 (interlacing).** Let $s = p = 1/2$ and use four frames with the shifts $(b/2 - 1/4 + c, a/2 - 1/4 + c)$ for $a, b \in \{0, 1\}$ and a fixed $c$. Then the drop of pixel $(i, j)$ of frame $(a, b)$ is exactly one output pixel, and $I = \frac14 d$ on the interlaced grid.

*Proof.* The center of the drop is at $x = j + 1/2 + b/2 - 1/4 + c$, so the drop covers $[j + b/2 + c, j + b/2 + c + 1/2]$, which is the output column $J = 2j + b + 2c$ when $2c$ is an integer. The same holds for the rows. So $a_{io} = 1/4$ for exactly one $o$, and $I_o = s^2 d_i = d_i/4$. $\square$

So drizzle with a small pixfrac and a complete set of half-pixel dithers puts each input sample on its own output pixel, with no smoothing by the input pixel shape beyond what the detector already did. With $p = 1$ the same frames give a smoother output, because each input pixel covers several output pixels. $\blacksquare$
