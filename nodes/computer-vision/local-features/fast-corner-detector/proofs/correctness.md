---
title: Correctness of the FAST corner detector
proves: [correctness]
status: full
---

Fix an integer image $I$, a pixel $p$ that is at least 3 pixels from each border, and an arc length $n$ with $1 \le n \le 16$. Number the circle pixels $x_0, \dots, x_{15}$ in the order of the page, and let an arc be a set $A_s = \{x_{(s + k) \bmod 16} : 0 \le k < n\}$ for $0 \le s < 16$. For a threshold $t \ge 1$, $p$ passes the segment test when some arc has all its pixels brighter ($I(x) \ge I_p + t$) or all darker ($I(x) \le I_p - t$).

**Lemma 1 (the score).** Let $b(A) = \min_{x \in A} (I(x) - I_p)$, $d(A) = \min_{x \in A} (I_p - I(x))$ and $V = \max_s \max(b(A_s), d(A_s))$. For each integer $t$, $p$ passes the segment test with threshold $t$ if and only if $V \ge t$. So $V$ is the largest threshold for which $p$ passes, and the set of thresholds for which it passes is $\{t : t \le V\}$.

*Proof.* All pixels of $A$ are brighter for $t$ exactly when $I(x) - I_p \ge t$ for each $x \in A$, that is when $b(A) \ge t$. In the same way all are darker exactly when $d(A) \ge t$. So $p$ passes exactly when $b(A_s) \ge t$ or $d(A_s) \ge t$ for some $s$, which is when the largest of these $32$ numbers, $V$, is at least $t$. Since $V$ is an integer, the passing thresholds are the integers up to $V$, and the largest is $V$. $\square$

**Lemma 2 (the high-speed test for $n = 12$).** If $n = 12$ and $p$ passes the segment test for $t$, then at least 3 of $x_0, x_4, x_8, x_{12}$ are brighter, or at least 3 are darker.

*Proof.* Let $A_s$ be an arc of 12 pixels that are all brighter (the darker case is the same). Its complement on the circle is the arc of the 4 positions $s + 12, s + 13, s + 14, s + 15$ modulo 16. Four consecutive integers hold exactly one multiple of 4, so the complement holds exactly one of the positions $0, 4, 8, 12$, and $A_s$ holds the other three. All pixels of $A_s$ are brighter. $\square$

So line L2 skips only pixels that would fail the test of line L4, and the set of candidates is the same with or without it. For $n < 12$ the complement has $16 - n \ge 5$ positions and can hold two of the four, so the lemma fails; the page gives an example with $n = 9$.

**Theorem.** FAST returns the set of pixels $p$ that pass the segment test for $t$ and whose score $V(p)$ is not smaller than the score of any passing pixel among their eight neighbours.

*Proof.* Line L1 visits each testable pixel once. By Lemma 2, line L2 skips only pixels that fail the segment test. Line L3 computes $V(p)$ as in Lemma 1, and by Lemma 1 line L4 adds $p$ to $C$ exactly when $p$ passes. So after the first loop $C$ is the set of passing pixels, each with its score. Lines L6 to L8 add $p \in C$ to the output exactly when $V(p) \ge V(q)$ for each $q \in C$ among its eight neighbours, and no line removes a pixel. Line L9 returns this set. $\square$

**Remark (rotation by $90°$).** The map $(du, dv) \mapsto (-dv, du)$, which is the rotation that sends pixel $(u, v)$ of a $W \times H$ image to pixel $(H - 1 - v, u)$ of the rotated image, sends $x_i$ to $x_{(i + 4) \bmod 16}$; this can be checked on the 16 offsets. A cyclic shift maps arcs to arcs, so the score of each pixel is the same as the score of its image, and the output of the rotated image is the rotated output. $\blacksquare$
