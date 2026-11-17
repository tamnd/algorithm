---
title: RoI pooling outputs bin maxima with the argmax rule as its gradient, smooth L1 has a bounded gradient, decoding inverts the encoding, and the RoI sampling and NMS follow their rules
proves: [correctness]
status: full
---

The convolutional layers and the head are learned and outside the claims. The claims are about the steps of the page that are not learned, as the Python code does them.

**Claim 1 (RoI pooling and its gradient).** Fix an RoI and let $R_{pq}$ be the cells of bin $(p, q)$ after rounding and clipping. For every channel, line L3 sets $Y_{pq} = \max_{(r, k) \in R_{pq}} F_{rk}$ when $R_{pq}$ is not empty, and 0 otherwise. If every nonempty bin has a unique maximum cell $a_{pq}$, then for any weights $w$ the gradient of $\sum_{pq} w_{pq} Y_{pq}$ with respect to $F_{rk}$ is $\sum_{pq : a_{pq} = (r, k)} w_{pq}$, which is what the backward pass returns.

*Proof.* The loop visits every cell of $R_{pq}$ and replaces the current value only when the new one is larger, or when the bin has no value yet, so it ends with the maximum and the first cell where it is reached. If the maximum is unique there is a gap $\delta > 0$ between $F_{a_{pq}}$ and every other cell of the bin. A change of the map smaller than $\delta / 2$ in every cell keeps the same argmax, so near $F$ the output $Y_{pq}$ equals $F_{a_{pq}}$, a linear function of the map with gradient 1 at $a_{pq}$ and 0 elsewhere. Summing over the bins with the weights gives the claim. The backward pass adds $w_{pq}$ to the cell $a_{pq}$ for every bin, which is the same sum. Empty bins are constant and add nothing. $\square$

When a maximum is not unique the function is not differentiable there, and the code sends the gradient to the first cell, as the original layer does. The bin layout itself is proved on the [RoI pooling](/roi-pooling/) page: the bins of a row cover the RoI with no gap, and next bins share at most one row or column.

**Claim 2 (smooth L1).** $\operatorname{smooth}_{L_1}(x) = x^2/2$ for $|x| < 1$ and $|x| - 1/2$ otherwise is continuous and has the continuous derivative $g(x) = x$ for $|x| < 1$ and $\operatorname{sign}(x)$ otherwise, with $|g(x)| \le 1$.

*Proof.* At $|x| = 1$ both pieces give $1/2$, and both derivatives give $\pm 1$, so the function and its derivative are continuous. Inside $(-1, 1)$, $|g(x)| = |x| < 1$, and outside $|g(x)| = 1$. $\square$

So the box term of the loss changes each offset gradient by at most $\lambda$, however far the target is, while the L2 loss $x^2/2$ has gradient $x$, which grows without bound. For $u = 0$ the factor $[u \ge 1]$ is zero and the loss is $-\log p_0$ alone, whatever the offsets.

**Claim 3 (decoding).** Let $\operatorname{enc}$ map an RoI $r$ and a box $g$ to $d = ((g_x - r_x)/r_w, (g_y - r_y)/r_h, \log(g_w / r_w), \log(g_h / r_h))$ and then to $t_i = (d_i - \mu_i)/\sigma_i$ with $\sigma_i > 0$. Then $\operatorname{DECODE}(r, \operatorname{enc}(r, g)) = g$.

*Proof.* Decoding first computes $t_i \sigma_i + \mu_i = d_i$. Then it puts the center at $r_x + r_w (g_x - r_x)/r_w = g_x$ and the width at $r_w e^{\log(g_w / r_w)} = g_w$, and the same for $y$ and $h$. The center and the size fix the box. $\square$

**Claim 4 (sampling).** Let a batch have size $b$. Each RoI $i$ gets the largest IoU $o_i$ over the ground truth boxes, and the first box $j_i$ that reaches it. The code returns at most $\operatorname{round}(b/4)$ foreground entries, each $(i, \text{class of } j_i, j_i)$ with $o_i \ge 0.5$, and background entries $(i, 0)$ with $0.1 \le o_i < 0.5$, all for distinct RoIs, at most $b$ in total.

*Proof.* The loop puts each RoI in at most one of the two lists, by $o_i$, with the class of $j_i$ for the foreground list. It then samples without replacement $\min(|\text{fg}|, \operatorname{round}(b/4))$ foreground entries and at most $b$ minus that number of background entries. Sampling without replacement from lists of distinct RoIs gives distinct RoIs. $\square$

RoIs with $o_i < 0.1$ are in neither list and are never used, which is the rule of the paper.

**Claim 5 (NMS).** For one class, the kept boxes have pairwise IoU at most $\tau$, and every candidate that is not kept has IoU above $\tau$ with a kept box of at least the same score.

*Proof.* The code visits the candidates by score, best first, and keeps a box only if its IoU with every box kept so far is at most $\tau$. Any two kept boxes were compared when the later one was visited. A box that was not kept failed that test against a box kept earlier, which has a score at least as high. $\square$

The detections of different classes are computed apart, so one class never removes a box of another.
