---
title: Correctness of the irradiance volume sample
proves: [correctness]
status: full
---

**Setting.** The volume has $X \times Y \times Z$ probes with $X, Y, Z \ge 2$, an origin $o$ and a spacing $h > 0$. Probe $(i, j, k)$ sits at $o + h (i, j, k)$ and holds a vector $c_{ijk} \in \mathbb{R}^9$ of irradiance coefficients. For a point $p$, let $g_a = \operatorname{clamp}((p_a - o_a)/h, 0, D_a - 1)$ for each axis $a$, where $D = (X, Y, Z)$. Define the hat function $\Lambda(u) = \max(0, 1 - |u|)$ and the reference blend

$$B(p) = \sum_{i, j, k} \Lambda(g_x - i)\, \Lambda(g_y - j)\, \Lambda(g_z - k)\, c_{ijk},$$

the sum over every probe. The claims are in exact arithmetic.

**Claim 1 (the cell).** Line L2 gives $i_a \in \{0, \dots, D_a - 2\}$ and $f_a = g_a - i_a \in [0, 1]$ for each axis.

*Proof.* Line L1 and the clamp give $g_a \in [0, D_a - 1]$. If $g_a < D_a - 1$, then $i_a = \lfloor g_a \rfloor \le D_a - 2$ and $0 \le f_a < 1$. If $g_a = D_a - 1$, the minimum gives $i_a = D_a - 2$ and $f_a = 1$. In both cases $i_a \ge 0$. $\square$

**Claim 2 (the blend is the reference blend).** Lines L3 to L6 return $B(p)$.

*Proof.* For one axis, $\Lambda(g_a - m)$ is nonzero only for $|g_a - m| < 1$. By Claim 1, $g_a \in [i_a, i_a + 1]$, so only $m = i_a$ and $m = i_a + 1$ can give a nonzero value, with $\Lambda(g_a - i_a) = 1 - f_a$ and $\Lambda(g_a - i_a - 1) = 1 - (1 - f_a) = f_a$. So the triple sum in $B(p)$ reduces to the 8 corners $(i_x + a, i_y + b, i_z + c)$ with $a, b, c \in \{0, 1\}$, and each corner has the weight $w_{abc} = \prod$ of $f$ or $1 - f$ per axis. Line L5 computes exactly these weights and line L6 adds $w_{abc}\, c$ of each corner to the output, which line L3 starts at 0. $\square$

**Claim 3 (partition of unity).** The 8 weights are nonnegative and add up to 1, so if every probe holds the same vector $c$, the sample is $c$ at every point, inside or outside the grid.

*Proof.* Each factor is in $[0, 1]$ by Claim 1, so each product is too. The sum is $\prod_a \big((1 - f_a) + f_a\big) = 1$. $\square$

**Claim 4 (interpolation and exactness).** At a probe position the sample equals that probe. If $c_{ijk} = \alpha + \beta_x x_i + \beta_y y_j + \beta_z z_k$ for fixed vectors $\alpha, \beta_a$ and the probe positions $(x_i, y_j, z_k)$, then the sample at any $p$ inside the grid box is $\alpha + \beta \cdot p$.

*Proof.* At a probe position, $g_a$ is an integer $m_a$, so $\Lambda(g_a - m) = 1$ for $m = m_a$ and 0 for every other integer $m$, and $B(p) = c_{m_x m_y m_z}$. For the affine case, inside the box $g_a = (p_a - o_a)/h$ with no clamping. By Claim 3 the constant $\alpha$ is kept. For the term $\beta_x x_i$, sum out $j$ and $k$ with Claim 3, which leaves $\sum_i \Lambda(g_x - i)\, \beta_x (o_x + h i) = \beta_x \big(o_x + h((1 - f_x) i_x + f_x (i_x + 1))\big) = \beta_x (o_x + h g_x) = \beta_x p_x$. The other two axes are the same. $\square$

**Claim 5 (the irradiance).** Line L7 returns $\sum_{ijk} w_{ijk}(p)\, E_{ijk}(n)$, where $E_{ijk}(n) = \sum_m c_{ijk, m} Y_m(n)$ is the irradiance that probe $(i, j, k)$ gives for the normal $n$, and the map from the probe data to the result is linear.

*Proof.* The evaluation $c \mapsto \sum_m c_m Y_m(n)$ is linear, so it commutes with the weighted sum of Claim 2. Each weight depends only on $p$, not on the data, so the whole map from the probe vectors to the result is linear. $\square$

So the sample is the trilinear interpolation of the probe irradiance functions, which is what the page defines. It makes no claim that this equals the true irradiance at $p$: that needs the irradiance field to be close to trilinear between probes, and it fails across occluders (the light leak of the page), which is a property of the field, not of the code.

**Cost.** Lines L1 and L2 do a constant number of operations per axis, lines L4 to L6 visit 8 corners with 9 coefficients each, and line L7 evaluates nine basis functions, so `sample` is $O(1)$, independent of the number of probes. `set_probe` writes 9 numbers, and the memory is $9 X Y Z$ numbers per color channel. $\blacksquare$
