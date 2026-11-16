---
title: Correctness of the SuperPoint decoder
proves: [correctness]
status: full
---

This proof covers the decoding step only: lines L1 to L11 of the main page, on given network outputs. The detector output $X$ has $H_c \times W_c$ cells of 65 real logits, and the descriptor output $F$ has $H_c \times W_c$ vectors in $\mathbb{R}^{m}$. Nothing here says that the network finds good points; that is a measured property.

**Lemma 1 (the heat map is a probability per cell).** For each cell $(c_x, c_y)$, the 64 values that line L3 writes into the pixels $(8 c_x + a, 8 c_y + b)$, $0 \le a, b \le 7$, are in $(0, 1)$, and their sum plus the dropped dustbin value $p_{64}$ is 1.

*Proof.* Line L2 computes $p_c = e^{z_c - M} / \sum_{c'} e^{z_{c'} - M}$ with $M = \max_c z_c$. Each term $e^{z_c - M}$ is positive and finite, so each $p_c$ is in $(0, 1)$ when there are at least two channels, and $\sum_{c=0}^{64} p_c = 1$. Subtracting $M$ multiplies the numerator and the denominator by the same factor $e^{-M}$, so $p_c$ equals the softmax $e^{z_c} / \sum e^{z_{c'}}$. $\square$

**Lemma 2 (each pixel gets exactly one channel).** The map $c \mapsto (8 c_x + (c \bmod 8), 8 c_y + \lfloor c / 8 \rfloor)$ is a bijection from the channels $0, \dots, 63$ of cell $(c_x, c_y)$ to the 64 pixels of that cell, and the cells partition the $8 H_c \times 8 W_c$ image.

*Proof.* Division with remainder writes each $c \in \{0, \dots, 63\}$ uniquely as $c = 8 b + a$ with $0 \le a, b \le 7$, and each pair $(a, b)$ comes from $c = 8 b + a$. The pixel $(u, v)$ is in exactly the cell $(\lfloor u/8 \rfloor, \lfloor v/8 \rfloor)$. So line L3 writes each pixel exactly once. $\square$

**Lemma 3 (invariance to a shift of the logits).** Adding the same constant to the 65 logits of a cell does not change its heat values.

*Proof.* The softmax of $z + t \mathbf{1}$ has terms $e^{z_c + t} / \sum e^{z_{c'} + t} = e^{z_c} / \sum e^{z_{c'}}$. $\square$

Let $C$ be the list of line L4 in the order of line L5: decreasing score, then increasing row, then increasing column. Write $\lVert (u, v) - (u', v') \rVert_\infty = \max(|u - u'|, |v - v'|)$.

**Lemma 4 (the grid test equals the distance test).** When line L8 tests a pixel $p$ of $C$, $p$ is marked "not free" if and only if some pixel kept before it is within Chebyshev distance $r$ of $p$.

*Proof.* Line L6 starts with all pixels free. A pixel becomes not free only at line L8, when a kept pixel $k$ marks the square $\{p : \lVert p - k \rVert_\infty \le r\}$, clipped to the image. Pixels are never marked free again. So at the time of the test, $p$ is not free exactly when it is in the square of some earlier kept pixel, that is, within distance $r$ of it. $\square$

**Theorem 1 (the result of NMS).** Let $K$ be the list of kept pixels. Then:

1. $K$ is the greedy list: a pixel of $C$ is in $K$ if and only if no pixel of $K$ that comes before it in the order of $C$ is within Chebyshev distance $r$.
2. Any two pixels of $K$ are at Chebyshev distance more than $r$.
3. Each pixel of $C$ that is not in $K$ is within distance $r$ of a pixel of $K$ whose score is at least its own.
4. Each pixel of $K$ has score at least $\tau$ and lies at least $\beta$ pixels from each border.

*Proof.* Part 1 is Lemma 4 applied to each pixel in the order of line L7. For part 2, take $k, k'$ in $K$ with $k$ before $k'$. When line L8 tested $k'$, it was free, so by Lemma 4 it was at distance more than $r$ from $k$. For part 3, a pixel $p$ of $C$ that is not kept was not free at its test, so by Lemma 4 an earlier kept pixel $k$ is within distance $r$. The order of line L5 puts $k$ before $p$ only if its score is at least the score of $p$. Part 4 follows from line L4. $\square$

**Lemma 5 (the descriptor).** Let $f$ be the vector that line L10 computes for a pixel $(u, v)$, with $f_x = (u - 3.5)/8$ and $f_y = (v - 3.5)/8$ clamped to $[0, W_c - 1] \times [0, H_c - 1]$. Then $f$ is a convex combination of the four vectors of $F$ around $(f_x, f_y)$. If $F$ is an affine function of the cell index, $F[c_y][c_x] = A (c_x, c_y)^T + b$, then $f = A (f_x, f_y)^T + b$ exactly. If $f \ne 0$, line L11 returns a vector of Euclidean norm 1.

*Proof.* With $x_0 = \lfloor f_x \rfloor$, $\alpha = f_x - x_0 \in [0, 1)$, and $y_0, \beta'$ the same for $f_y$, the weights $(1-\alpha)(1-\beta')$, $\alpha(1-\beta')$, $(1-\alpha)\beta'$ and $\alpha\beta'$ are non-negative and sum to 1. At the last column or row the code uses $x_1 = x_0$ or $y_1 = y_0$, and then $\alpha = 0$ or $\beta' = 0$ because the clamp makes $f_x = W_c - 1$ or $f_y = H_c - 1$ an integer. For an affine $F$, interpolation along $x$ gives $(1 - \alpha) F[\cdot][x_0] + \alpha F[\cdot][x_0 + 1] = A (x_0 + \alpha, \cdot)^T + b$, because an affine function is affine along each line, and the same holds along $y$. Division by the norm $\lVert f \rVert > 0$ gives a vector of norm 1. $\square$

Lemmas 1 to 5 together show that the decoder returns the greedy non-maximum suppression of the heat map defined by the per-cell softmax, with a unit descriptor for each kept pixel. $\blacksquare$
