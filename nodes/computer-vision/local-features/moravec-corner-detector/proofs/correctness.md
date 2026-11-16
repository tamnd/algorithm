---
title: Correctness of the Moravec corner detector
proves: [correctness]
status: full
---

We prove that MORAVEC returns exactly the set defined in The problem, and we prove the three facts about the response that the page states.

**Setting.** $I$ is a $W \times H$ image with integer values, $r \ge 0$, $m \ge 1$ and $\tau \ge 0$. Let $D$ be the set of pixels with $r + 1 \le u \le W - r - 2$ and $r + 1 \le v \le H - r - 2$. The target output is

$$T = \{(u, v) \in D : C(u, v) > \tau \text{ and } C(u, v) \ge C(u', v') \text{ for each } (u', v') \in D \text{ with } |u' - u| \le m, |v' - v| \le m\}.$$

**Lemma 1 (the reads are in the image).** For $(u, v) \in D$, $(a, b) \in S$ and $|i|, |j| \le r$, both $(u + i, v + j)$ and $(u + i + a, v + j + b)$ are pixels of $I$.

*Proof.* Each of $a$ and $b$ is in $\{-1, 0, 1\}$. So $u + i + a \ge (r + 1) - r - 1 = 0$ and $u + i + a \le (W - r - 2) + r + 1 = W - 1$. The same bounds hold for $u + i$, and the same argument with $H$ holds for the row. $\square$

**Lemma 2 (the table $C$).** After lines L1 to L3, $C$ is defined exactly on $D$, and for each $(u, v) \in D$ it holds $\min_{(a, b) \in S} E_{ab}(u, v)$.

*Proof.* Line L2 visits each pixel of $D$ once and no other pixel. By Lemma 1, each sum $E_{ab}(u, v)$ reads only pixels of $I$, so it is a well defined integer. Line L3 stores the minimum of the four sums for the set $S$ of line L1, and no later line writes to $C$. $\square$

**Theorem (output).** MORAVEC returns $T$.

*Proof.* By Lemma 2, line L5 visits exactly the pixels $(u, v) \in D$ with $C(u, v) > \tau$, each once. For such a pixel, line L6 tests $C(u, v) \ge C(u', v')$ for each defined $(u', v')$ in the square of radius $m$. The pixel $(u', v') = (u, v)$ passes this test trivially, so the test is true exactly when the second condition in the definition of $T$ holds. Line L7 adds the pixel exactly when the test is true. Lines L4 to L7 only add to the set, so after the loop the set holds each pixel of $T$ and no other pixel, and line L8 returns it. $\square$

**Proposition 1 (an edge along a direction of $S$).** Let $(u, v) \in D$ and $(a, b) \in S$. If $I(p + (a, b)) = I(p)$ for each pixel $p$ of the window at $(u, v)$, then $C(u, v) = 0$. In particular, a window that lies in a region where $I$ is constant gives $C = 0$.

*Proof.* Each term of $E_{ab}(u, v)$ is $(I(p + (a, b)) - I(p))^2 = 0$, so $E_{ab}(u, v) = 0$. Each $E$ is a sum of squares and so is at least $0$. The minimum of four numbers that are at least $0$, one of which is $0$, is $0$. If $I$ is constant on the window and its shifted copies, the hypothesis holds for each shift. $\square$

**Proposition 2 (offset and gain).** For an integer $c$ and an integer $g$, let $C'$ be the response of $gI + c$. Then $C'(u, v) = g^2 C(u, v)$ for each $(u, v) \in D$. If $g \ne 0$ and $\tau = 0$, MORAVEC returns the same set for $gI + c$ as for $I$.

*Proof.* Each difference becomes $(gI(q) + c) - (gI(p) + c) = g(I(q) - I(p))$, so each squared difference, each sum $E_{ab}$ and so the minimum $C$ is multiplied by $g^2 \ge 0$. Multiplying by $g^2 > 0$ keeps every inequality $C(u, v) \ge C(u', v')$ and keeps $C(u, v) > 0$, and the set $D$ depends only on $W$, $H$ and $r$. So by the Theorem the two outputs are the same set. $\square$

**Proposition 3 (the opposite shift).** For a shift $s = (a, b)$ and a pixel $p$ such that both sides read only pixels of $I$, $E_{-a,-b}(p) = E_{ab}(p - s)$.

*Proof.* Write $N$ for the set of offsets $(i, j)$ with $|i|, |j| \le r$. Then $E_{-a,-b}(p) = \sum_{n \in N} (I(p + n - s) - I(p + n))^2$. Put $q = p - s$. The term for $n$ is $(I(q + n) - I(q + n + s))^2 = (I(q + n + s) - I(q + n))^2$, which is the term for $n$ of $E_{ab}(q)$. Summing over $N$ gives the claim. $\square$

So the minimum over the eight unit shifts at $p$ is the minimum of the four sums at $p$ and of the four sums $E_{ab}(p - (a, b))$ at the neighbours, which is the statement on the page about the eight-shift variant. $\blacksquare$
