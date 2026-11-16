---
title: Correctness of the census transform and the census cost
proves: [correctness]
status: full
---

Fix a radius $r \ge 1$ and let $o_1, \ldots, o_n$ be the offsets of the window without $(0, 0)$ in row-major order, $n = (2r + 1)^2 - 1$. Write $\xi(a, b) = 1$ if $b < a$ and $0$ otherwise. For a pixel $p$ of an image $I$, the census string is the bit string $T(p) = \xi(I(p), I(p + o_1)) \ldots \xi(I(p), I(p + o_n))$, the first bit most significant, where a position outside the image takes the value of the nearest border pixel. We identify a bit string $b_1 \ldots b_k$ with the integer $\sum_{i=1}^{k} b_i 2^{k - i}$.

## Lemma 1. Lines L2 to L5 compute $T(p)$

**Invariant.** After the loop of line L3 has handled the offsets $o_1, \ldots, o_k$, the integer $c$ equals the string $\beta_1 \ldots \beta_k$ with $\beta_i = \xi(I(p), I(p + o_i))$.

**Start.** Before the loop, $k = 0$ and $c = 0$, the empty string.

**Step.** If $c = \beta_1 \ldots \beta_k = \sum_{i \le k} \beta_i 2^{k - i}$, line L4 sets $c$ to $2c + \beta_{k+1} = \sum_{i \le k} \beta_i 2^{k + 1 - i} + \beta_{k + 1} 2^0$, which is the string $\beta_1 \ldots \beta_{k+1}$.

**End.** After $k = n$ steps, $c = T(p)$, and line L5 stores it. Each value is less than $2^n$, so it fits a word of $w \ge n$ bits. $\square$

## Lemma 2. Line L7 returns the number of differing bits

Let $a = a_1 \ldots a_n$ and $b = b_1 \ldots b_n$. Bit $i$ of $a \oplus b$ is $a_i \oplus b_i$, which is 1 exactly when $a_i \ne b_i$. Popcount counts the 1 bits. So line L7 returns $\lvert \{ i : a_i \ne b_i \} \rvert$, the Hamming distance of $a$ and $b$. $\square$

The Hamming distance is a metric on strings of $n$ bits: it is zero exactly for equal strings, it is symmetric, and it satisfies the triangle inequality because a position where $a$ and $c$ differ is a position where $a$ and $b$ differ or $b$ and $c$ differ. So the census cost satisfies $0 \le C(p, d) \le n$.

## Theorem 1. Invariance to strictly increasing changes

Let $g$ be a strictly increasing function on the values of the image, and $I' = g \circ I$. Then $T'(p) = T(p)$ for every pixel $p$.

*Proof.* For any two values $a$ and $b$, $g(b) < g(a)$ holds exactly when $b < a$: if $b < a$ then $g(b) < g(a)$ because $g$ is strictly increasing, and if $b \ge a$ then $g(b) \ge g(a)$ for the same reason. So $\xi(g(a), g(b)) = \xi(a, b)$. The border rule picks the same source pixel in $I$ and $I'$, so every bit of $T'(p)$ equals the bit of $T(p)$ at the same offset. $\square$

**Corollary.** If $I'_L = g_L \circ I_L$ and $I'_R = g_R \circ I_R$ with two strictly increasing functions $g_L$ and $g_R$, possibly different, then the census cost $C'(p, d)$ of the new pair equals $C(p, d)$ of the old pair for every pixel and disparity, by Theorem 1 and Lemma 2. Any method that depends only on the costs, such as winner-takes-all on box sums of costs, then gives the same disparity map.

The theorem needs one function for the whole image. A change of brightness that varies across the window, such as a strong vignetting edge, can change the order of values inside it, and then the strings change.

## Theorem 2. Shifts and turns permute nothing or permute bits

*Shift.* Let $I'(u, v) = I(u - s, v)$ for an integer $s$. For a pixel $p = (u, v)$ such that the windows of $p$ in $I'$ and of $(u - s, v)$ in $I$ lie inside the images, every term $\xi(I'(p), I'(p + o))$ equals $\xi(I(p - (s, 0)), I(p - (s, 0) + o))$, so $T'(p) = T(p - (s, 0))$. This is why a disparity $s$ between two images of the same flat textured surface gives the cost 0 at disparity $s$.

*Turn by 90 degrees.* Let $I$ have $H$ rows and put $I'(x, y) = I(y, H - 1 - x)$. The pixel $(x, y)$ of $I'$ is the pixel $(u, v) = (y, H - 1 - x)$ of $I$, and the offset $(du', dv')$ in $I'$ moves to $(u + dv', v - du')$ in $I$, the offset $(dv', -du')$. The map $(du', dv') \mapsto (dv', -du')$ is a bijection of the window offsets without $(0, 0)$. So, for a pixel whose window lies inside the image, the bit of $T'$ at offset $o'$ equals the bit of $T$ at the image of $o'$: the string of the turned image is a fixed permutation of the bits of the string of the original. $\square$

## The rank transform

The rank of $p$ is $\lvert \{ i : I(p + o_i) < I(p) \} \rvert = \sum_i \beta_i$, which is $\operatorname{popcount}(T(p))$ by the definition of $T(p)$. So the rank is a function of the census, and two pixels with equal census strings have equal ranks. The converse is false: the strings $10$ and $01$ have the same rank 1.

## The code

The function `census` follows lines L1 to L6 with the bits in the order of `window_offsets`, and Lemma 1 applies. The function `hamming` is line L7, and Lemma 2 applies; `popcount` counts the characters `1` in the binary form of the integer, which is the number of 1 bits. The function `census_cost_volume` gives $C(p, d)$ for $u - d \ge 0$ and the value $n + 1 > C$ otherwise, so an invalid entry is never smaller than a valid one. The function `census_disparity` sums these costs over a box clamped to the image and keeps the smallest disparity with the least sum, which is winner-takes-all with ties to the smallest $d$.
