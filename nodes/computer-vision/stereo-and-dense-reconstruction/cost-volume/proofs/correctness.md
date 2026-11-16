---
title: Correctness of the cost volume operations
proves: [correctness]
status: full
---

Let $\mathcal I = \{0, \ldots, W - 1\} \times \{0, \ldots, H - 1\} \times \{0, \ldots, D - 1\}$ and $N = W H D$.

## Lemma 1. INDEX is a bijection from $\mathcal I$ onto $\{0, \ldots, N - 1\}$

For $(u, v, d) \in \mathcal I$, the value $k = (v W + u) D + d$ satisfies $0 \le k \le ((H - 1) W + W - 1) D + D - 1 = N - 1$. Conversely, given $k$ in this range, $d = k \bmod D$ and $q = \lfloor k / D \rfloor$, then $u = q \bmod W$ and $v = \lfloor q / W \rfloor$. Division with remainder is unique, so $k$ has exactly one preimage, and INDEX is one to one and onto. $\square$

So each triple has its own cell, and writing one entry never changes another.

## Lemma 2. BUILD writes each entry once with its value

The loops of lines L2 and L3 visit each triple of $\mathcal I$ exactly once. Line L4 writes $c(u, v, d)$ when $u - d \ge 0$ and $\infty$ otherwise into the cell of the triple, and by Lemma 1 no other visit writes that cell. After BUILD every cell holds the value of the definition. The code visits the triples in increasing order of INDEX, so it writes the array from position 0 to $N - 1$ with a running counter, which by Lemma 1 is the same as computing INDEX. $\square$

## Lemma 3. WTA returns the least disparity with the least cost

Fix a pixel. **Invariant.** After line L7 has handled the disparities up to $d$, $\textit{best} = \min_{d' \le d} C(u, v, d')$ and $\textit{disp}(u, v)$ is the least $d' \le d$ that reaches it. Line L6 makes it true for $d = 0$. If $C(u, v, d + 1) < \textit{best}$, it is the new least value and $d + 1$ is the only disparity that reaches it, and line L7 records it. Otherwise the least value and the least disparity that reaches it do not change. After $d = D - 1$, the claim is the definition of WTA. Invalid entries hold $\infty$, which is never less than a valid cost, so WTA picks an invalid disparity only when all the column is invalid, which cannot happen because $C(u, v, 0)$ is valid for every pixel. $\square$

## Lemma 4. RIGHT-VIEW is the volume of the right image

With the right image as reference, the right pixel $(x, v)$ at disparity $d$ is compared with the left pixel $(x + d, v)$: if the left pixel $(u, v)$ matches the right pixel $(u - d, v)$, then the right pixel $(x, v) = (u - d, v)$ matches the left pixel $(x + d, v)$. The left entry $(x + d, v, d)$ compares exactly this pair, and it exists in $\mathcal I$ if and only if $x + d \le W - 1$, the test of line L11. Its value is the cost of the pair for any cost that is symmetric in the two pixels compared, such as the absolute difference or the Hamming distance of census strings. When $x + d \ge W$ the left pixel is outside the image, and line L11 writes $\infty$, the invalid value. $\square$

For a cost that is not symmetric in the two images, such as the one-sided term of the Birchfield-Tomasi measure, the right view holds the cost of the same pair with the same roles, which is still the cost of that pair but not the cost the method would compute with the right image as the first argument.

## Slices

SLICE$(d)$ reads the cells of all triples with this $d$ in row-major order of the pixels, and SET-SLICE$(d, A)$ writes $A[v][u]$ into the cell of $(u, v, d)$. By Lemma 1 these cells are distinct and are not cells of other disparities, so a slice can be filtered and written back without changing the other slices. $\square$
