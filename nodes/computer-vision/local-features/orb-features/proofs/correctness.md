---
title: Correctness of ORB
proves: [correctness]
status: full
---

Pixels are $(u, v)$ with $u$ the column and $v$ the row. The turn by $90°$ is $R(x, y) = (-y, x)$; it maps the angle $\theta$ of a vector to $\theta + \pi/2$. For an image $I$ of size $n \times n$, the turned image is $I'(u', v') = I(v', n - 1 - u')$, so the pixel $(u, v)$ of $I$ is the pixel $(n - 1 - v, u)$ of $I'$, and the offset $(x, y)$ from a pixel becomes the offset $R(x, y)$.

**Lemma 1 (segment test).** Let $s_0, \dots, s_{15}$ be the states of the circle pixels in order, each brighter, darker or similar. The code returns true if and only if there are 9 cyclically contiguous indices $j, j + 1, \dots, j + 8 \pmod{16}$ with the same state, brighter or darker.

*Proof.* The code scans the sequence $s_0, \dots, s_{15}, s_0, \dots, s_{15}$ and counts the length of the current run of the wanted state. A cyclic run of 9 starting at $j$ appears in the doubled sequence at the positions $j, \dots, j + 8 \le 23$, so the count reaches 9. Conversely, a run of 9 in the doubled sequence covers 9 consecutive positions, which are 9 cyclically consecutive indices since $9 \le 16$. $\square$

**Lemma 2 (centroid angle).** Let $\theta$ be the centroid angle of $I$ at $k$ over the disk $D$ of radius $r$, and $\theta'$ that of $I'$ at the turned point $k'$. If $(m_{10}, m_{01}) \ne (0, 0)$, then $\theta' \equiv \theta + \pi/2 \pmod{2\pi}$. Adding a constant $a$ to $I$ does not change $\theta$, and multiplying $I$ by $c > 0$ does not change it either.

*Proof.* $D$ is symmetric under $R$. The pixel $k' + R(x, y)$ of $I'$ has the value $I(k + (x, y))$. So $(m'_{10}, m'_{01}) = \sum_{(x, y) \in D} R(x, y) I(k + (x, y)) = R(m_{10}, m_{01})$, whose angle is $\theta + \pi/2$. For the offset, $\sum_{(x, y) \in D} x = \sum y = 0$ since $D$ is symmetric under $(x, y) \mapsto (-x, -y)$, so $a$ adds 0 to both moments. A factor $c > 0$ multiplies both moments and does not change $\operatorname{atan2}$. The moments are sums of integers, so all of this holds exactly in the code; the angles agree up to the rounding of $\operatorname{atan2}$. $\square$

**Lemma 3 (turned tables).** If the number of bins $B$ is a multiple of 4, the tables satisfy $T_{b + B/4} = R(T_b)$ for all $b$, indices modulo $B$, where $R$ acts on both points of each test.

*Proof.* For $b \ge B/4$ the code defines $T_b = R(T_{b - B/4})$, which is the claim for $b < 3B/4$. For $b \ge 3B/4$, $T_{b + B/4 - B} = T_{b - 3B/4}$, and applying the definition three times gives $T_b = R^3(T_{b - 3B/4})$, so $R(T_b) = R^4(T_{b - 3B/4}) = T_{b - 3B/4}$, since $R^4$ is the identity. $\square$

**Lemma 4 (descriptor under a quarter turn).** Let $k$ be a keypoint of $I$ and $k'$ the turned point in $I'$, both at least 17 pixels from the border, and let $b$ and $b'$ be their bins. If $b' = b + B/4 \pmod B$ and $B$ is a multiple of 4, the descriptors are equal.

*Proof.* The $5 \times 5$ window centered at $k' + R(p)$ in $I'$ holds the same pixels as the window centered at $k + p$ in $I$, since the window is symmetric under $R$. So $S'(k' + R(p)) = S(k + p)$ for every point $p$ of a test. By Lemma 3 the test $i$ of $T_{b'}$ is $(R(p_i), R(q_i))$ when $(p_i, q_i)$ is the test $i$ of $T_b$. So each bit of the descriptor of $k'$ compares the same two sums as the bit of $k$. $\square$

By Lemma 2 the turned angle is $\theta + \pi/2$, so the bins shift by exactly $B/4$ unless the rounding of $\operatorname{atan2}$ moves an angle that lies on a bin border; the tests check that the shift holds for the keypoints used.

**Lemma 5 (greedy search).** `learn_tests` ends. Every two tests it returns have an absolute correlation on the training patches below the returned threshold, and it returns $n$ tests unless the threshold has reached 1.

*Proof.* Each round runs over a finite list. A round ends with $n$ tests, or raises the threshold by a fixed step; after finitely many rounds the threshold is at least 1, and the search returns. In a round, a test enters the result only if its absolute correlation with each test already in the result is below the threshold of the round, so every pair in the result satisfies the bound. The returned threshold is that of the last round. $\square$

When the threshold is above 1, every correlation is below it, so the last round takes the first $n$ tests of the order; if there are fewer than $n$ candidates, the result is shorter.

**Theorem.** ORB returns the FAST-9 corners that are local maxima of the Harris measure, the best $N$ by that measure, each with its centroid angle and the descriptor of the definition. With $B$ a multiple of 4, turning the image by $90°$ about its center turns the angles by $\pi/2$ and keeps the descriptors whenever the bins shift by $B/4$. Adding a constant to the image does not change the output.

*Proof.* Line L1 is the segment test by Lemma 1, and line L2 keeps and sorts as defined. Line L3 computes the angle, line L4 the bin, and lines L5 and L6 the bits with the table of the bin. Lemmas 2 and 4 give the claim on the turned image. For the offset: the segment test compares differences of pixels, the Harris measure uses differences, the angle does not change by Lemma 2, and each test compares two sums of 25 pixels, which both grow by $25 a$. So every step gives the same result. $\square$
