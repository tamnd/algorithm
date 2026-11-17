---
title: The box formula for IoU gives the area of the intersection over the area of the union
proves: [correctness]
status: full
---

We use the notation of the page. A box is $a = (a_{x1}, a_{y1}, a_{x2}, a_{y2})$ with $a_{x1} \le a_{x2}$ and $a_{y1} \le a_{y2}$, and it is the closed set $[a_{x1}, a_{x2}] \times [a_{y1}, a_{y2}]$ of the plane. Its area is $|a| = (a_{x2} - a_{x1})(a_{y2} - a_{y1})$. The procedure IOU of the page computes $w$ and $h$ in lines L1 and L2, $I$ in line L3, $U$ in line L4 and returns $I / U$ in line L5.

**Claim.** If $|a \cup b| > 0$, IOU returns $|a \cap b| / |a \cup b|$, where $|\cdot|$ is the area (the Lebesgue measure of the set).

**Lemma 1 (the intersection of two boxes).** $a \cap b = [\max(a_{x1}, b_{x1}), \min(a_{x2}, b_{x2})] \times [\max(a_{y1}, b_{y1}), \min(a_{y2}, b_{y2})]$, and this set is empty when one of the two intervals is empty.

*Proof.* A point $(x, y)$ is in $a \cap b$ exactly when $a_{x1} \le x \le a_{x2}$, $b_{x1} \le x \le b_{x2}$, $a_{y1} \le y \le a_{y2}$ and $b_{y1} \le y \le b_{y2}$. The two conditions on $x$ together say $\max(a_{x1}, b_{x1}) \le x \le \min(a_{x2}, b_{x2})$, and the same holds for $y$. A product of two intervals is empty exactly when one of them is empty. $\square$

**Lemma 2 (the area of the intersection).** After line L3, $I = |a \cap b|$.

*Proof.* Lines L1 and L2 compute the lengths $w$ and $h$ of the two intervals of Lemma 1. If $w > 0$ and $h > 0$, the intersection is a box with sides $w$ and $h$, so its area is $w h$. If $w \le 0$ or $h \le 0$, the interval is empty or a single point, so the intersection is empty or lies on a line segment, and its area is 0. Line L3 returns exactly these two values. $\square$

**Lemma 3 (the area of the union).** After line L4, $U = |a \cup b|$.

*Proof.* Area is additive on disjoint measurable sets, and $a \cup b$ is the disjoint union of $a$ and $b \setminus a$. Also $b$ is the disjoint union of $b \setminus a$ and $a \cap b$. So $|a \cup b| = |a| + |b| - |a \cap b|$, which is the value of line L4 by Lemma 2. $\square$

**Proof of the claim.** By Lemmas 2 and 3, line L5 returns $|a \cap b| / |a \cup b|$ when $U > 0$. $\square$

**Corollary (range and symmetry).** $0 \le \mathrm{IoU}(a, b) \le 1$ and $\mathrm{IoU}(a, b) = \mathrm{IoU}(b, a)$. If $|a| > 0$ and $|b| > 0$, then $\mathrm{IoU}(a, b) = 1$ exactly when $a = b$.

*Proof.* $a \cap b \subseteq a \cup b$ gives the range, and the formulas of lines L1 to L4 do not change when $a$ and $b$ swap. If the value is 1, then $|a \cap b| = |a \cup b|$, so $|a| = |a \cap b| = |b|$. The intersection is a box inside $a$ with the same positive area, and a box inside a box with the same area has the same sides, so $a \cap b = a$. In the same way $a \cap b = b$, so $a = b$. $\square$

**Corollary (invariance).** For a map $\phi(x, y) = (s x + t_x, s y + t_y)$ with $s > 0$, $\mathrm{IoU}(\phi(a), \phi(b)) = \mathrm{IoU}(a, b)$.

*Proof.* $\phi$ maps boxes to boxes, keeps the order of coordinates, and maps $a \cap b$ to $\phi(a) \cap \phi(b)$. It multiplies every area by $s^2$, so the ratio does not change. $\square$

**Corollary (pixel sets).** For a box with integer corners, let $P(a)$ be the set of unit cells $[u, u + 1) \times [v, v + 1)$ inside $a$. Then $|P(a)| = |a|$, $P(a \cap b) = P(a) \cap P(b)$, and the box IoU equals $|P(a) \cap P(b)| / |P(a) \cup P(b)|$.

*Proof.* The cells inside $a$ are those with $a_{x1} \le u < a_{x2}$ and $a_{y1} \le v < a_{y2}$, so there are $(a_{x2} - a_{x1})(a_{y2} - a_{y1})$ of them. A cell is inside both boxes exactly when it is inside their intersection, which is a box with integer corners by Lemma 1. Counting with inclusion and exclusion as in Lemma 3 gives the union. $\square$

**The inclusive pixel form.** The PASCAL VOC development kit stores the first and the last pixel of each side, so a side from index $x_1$ to index $x_2$ has $x_2 - x_1 + 1$ pixels. This is the continuous box $(x_1, y_1, x_2 + 1, y_2 + 1)$, and the claim applies to that box. The two forms give different values on the same four numbers, for example $1/7$ and $2/7$ for $(0, 0, 2, 2)$ and $(1, 1, 3, 3)$.

**The metric.** The Jaccard distance $1 - |A \cap B| / |A \cup B|$ satisfies the triangle inequality on finite sets (Kosub 2019 gives two short proofs). By the pixel-set corollary, $1 - \mathrm{IoU}$ is then a metric on boxes with integer corners and positive area. A box with rational corners becomes a box with integer corners after a scaling, which does not change IoU by the invariance corollary, and continuity extends the inequality to real corners. We do not repeat the proof of the set inequality here; the tests check it on random boxes.
