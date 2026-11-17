---
title: The R-CNN context box puts the proposal at p pixels from the patch border, the warp is the affine map of the box, decoding inverts the encoding, the label rules are consistent, and NMS keeps a non-overlapping cover
proves: [correctness]
status: full
---

The CNN, the SVM weights and the regressors are learned, and nothing is claimed about them. The claims below are about the steps of the page that are not learned, as the Python code does them. A box is $(x_1, y_1, x_2, y_2)$ with $x_1 < x_2$ and $y_1 < y_2$.

**Claim 1 (context).** Let $S > 2p \ge 0$, and let line L2 grow the box $b$ about its center by the factor $f = S / (S - 2p)$ to the box $c$. Under the map $x \mapsto S (x - c_{x_1}) / (c_{x_2} - c_{x_1})$ from $c$ to $[0, S]$, the left and right edges of $b$ go to $p$ and $S - p$, and the same holds for the rows.

*Proof.* Let $m = (b_{x_1} + b_{x_2})/2$ and $w = b_{x_2} - b_{x_1}$. Then $c_{x_1} = m - fw/2$ and $c_{x_2} = m + fw/2$, so the width of $c$ is $fw$. The left edge of $b$ is $m - w/2$, and it maps to $S (fw/2 - w/2) / (fw) = S (f - 1) / (2f)$. Since $f - 1 = 2p / (S - 2p)$ and $1/f = (S - 2p)/S$, this is $S \cdot \frac{2p}{S - 2p} \cdot \frac{S - 2p}{2S} = p$. The right edge maps to $S (fw/2 + w/2)/(fw) = S (f + 1)/(2f) = S - p$ by the same algebra, since $(f - 1) + (f + 1) = 2f$. The rows are the same with $y$ and the height. $\square$

So, for $S = 227$ and $p = 16$, a proposal of side 195 at the origin has the context box $(-16, -16, 211, 211)$.

**Claim 2 (warp).** Let the image be $I(u, v) = \alpha u + \beta v + \gamma$ at pixel $(u, v)$. If the sample point $(x, y)$ of an output pixel satisfies $0.5 \le x \le W - 0.5$ and $0.5 \le y \le H - 0.5$, the warp returns exactly $\alpha (x - 0.5) + \beta (y - 0.5) + \gamma$. Outside the image it returns the fill value.

*Proof.* The code samples output pixel $(u, v)$ of a box $c$ at $x = c_{x_1} + (u + 0.5)(c_{x_2} - c_{x_1})/S$ and the same for $y$, which is the image of the output pixel center under the affine map from $[0, S]^2$ to $c$. Inside the stated range the clamping does nothing, $f_x = x - 0.5 \in [0, W - 1]$, and with $u_0 = \lfloor f_x \rfloor$ and $a = f_x - u_0$ the bilinear formula is $(1 - a) I(u_0, \cdot) + a I(u_0 + 1, \cdot)$, which for a function that is affine in $u$ equals its value at $u_0 + a = f_x$. When $u_0 = W - 1$ then $a = 0$ and only one column is used. The same holds for $v$, and bilinear interpolation of a function that is affine in each variable on its own is exact. A point outside $[0, W) \times [0, H)$ takes the fill by the first test of the code. $\square$

**Claim 3 (decoding).** For a proposal $P$ with center form $(P_x, P_y, P_w, P_h)$ and a box $G$, let $t = ((G_x - P_x)/P_w, (G_y - P_y)/P_h, \log(G_w/P_w), \log(G_h/P_h))$. Then $\operatorname{DECODE}(P, t) = G$, and $\operatorname{DECODE}(P, 0) = P$.

*Proof.* Decoding gives the center $P_x + P_w (G_x - P_x)/P_w = G_x$, the width $P_w e^{\log(G_w/P_w)} = G_w$, and the same for $y$ and $h$; a box is fixed by its center form. With $t = 0$ the center is $P_x$ and the width $P_w e^0 = P_w$. $\square$

**Claim 4 (labels).** With the thresholds 0.5 for fine-tuning, 0.3 for the SVM negatives and 0.6 for regression:

1. if $(i, j)$ is a regression pair, the fine-tuning label of proposal $i$ is the class of ground truth box $j$;
2. if proposal $i$ is an SVM negative of class $c$, its fine-tuning label is not $c$.

*Proof.* (1) Both rules pick the ground truth box of largest IoU, with ties going to the first box. For a regression pair this IoU is above $0.6 \ge 0.5$, so fine-tuning labels the proposal with the class of that same box. (2) A negative of class $c$ has IoU below 0.3 with every box of class $c$. If its fine-tuning label were $c$, its best box would be of class $c$ with IoU at least 0.5, which is a contradiction. $\square$

The rules do not agree the other way round. A proposal with IoU 0.5 is a fine-tuning positive but neither an SVM example nor a regression pair, which is the example of the page.

**Claim 5 (NMS).** For one class, let $K$ be the indices kept by greedy NMS with threshold $\tau$. Then any two boxes of $K$ have IoU at most $\tau$, and every index not in $K$ has a box in $K$ with a score at least as high and an IoU above $\tau$.

*Proof.* The code visits the boxes by score, best first, and adds a box to $K$ only if its IoU with every box already in $K$ is at most $\tau$. Two kept boxes were compared when the later of them was added, so their IoU is at most $\tau$. A box that is not kept was rejected because some box already in $K$ overlapped it by more than $\tau$, and that box was visited earlier, so its score is at least as high. $\square$

[Box non-maximum suppression](/box-non-maximum-suppression/) proves more about this procedure; R-CNN runs it once for each class, so a box of one class never removes a box of another class.
