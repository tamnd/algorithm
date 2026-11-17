---
title: The anchors tile the feature map with the stated shapes, the proposal step returns sorted, clipped, large enough and non-overlapping boxes, and the RPN labels and sampling follow their rules
proves: [correctness]
status: full
---

The backbone and the two heads are learned and outside the claims. The claims are about the steps of the page that are not learned, as the Python code does them. A box is $(x_1, y_1, x_2, y_2)$.

**Claim 1 (anchors).** For sizes $s$ and ratios $\rho = h/w$, the code makes the shape $w = s/\sqrt{\rho}$, $h = s\sqrt{\rho}$ at the center $((j + 0.5)\sigma, (i + 0.5)\sigma)$ of cell $(i, j)$. Each anchor has area $s^2$ and aspect ratio $\rho$. If $T$ shifts the plane by $(a\sigma, b\sigma)$ with integers $a$ and $b$, every anchor at a cell $(i, j)$ for which $(i + b, j + a)$ is a cell of the map is mapped by $T$ onto the anchor of the same shape at that cell.

*Proof.* $wh = (s/\sqrt{\rho})(s\sqrt{\rho}) = s^2$ and $h/w = \rho$. The anchors at a cell are the shapes placed at the cell center, and $T$ moves the center of cell $(i, j)$ to $((j + a + 0.5)\sigma, (i + b + 0.5)\sigma)$, the center of cell $(i + b, j + a)$, without changing the shape. $\square$

Since the head has the same weights at every cell, the scores and offsets of a shifted image are, away from the borders and up to the receptive field, the shifted scores and offsets, and the proposals shift with the image. This is the translation property of the paper; it is a property of the convolution, and the claim gives the part that the anchors add.

**Claim 2 (proposals).** The proposal step returns at most $N_{post}$ boxes, in order of non-increasing score, each inside $[0, W_I] \times [0, H_I]$ with both sides at least the minimum size $m$, and with pairwise IoU at most $\tau_{rpn}$.

*Proof.* Line L3 clips every coordinate to the image, so every box is inside. Line L4 keeps only boxes with both sides at least $m$, and the later steps only remove boxes. Line L5 sorts by score with ties by index. Line L6 visits the boxes in that order and adds a box only if its IoU with every box kept so far is at most $\tau_{rpn}$, and stops at $N_{post}$ boxes. So the output is a subsequence of a sorted list, its size is at most $N_{post}$, and any two kept boxes were compared when the later one was added. $\square$

Clipping happens after decoding: a box that crosses the border keeps its regressed inside part. If clipping came first the offsets would apply to a different box than the one the network was trained on.

**Claim 3 (labels).** Let the label of an anchor that crosses the image border be "ignored". For the other anchors, let the label be positive if the IoU with some ground truth box is at least $\tau_+ = 0.7$ or if the anchor reaches the largest IoU, when positive, among the inside anchors for some box; negative if it is not positive and every IoU is below $\tau_- = 0.3$; and ignored otherwise. The code gives these labels, and every ground truth box with an inside anchor of positive IoU has a positive anchor, one of largest IoU with it.

*Proof.* The code first sets, for each inside anchor, the label 0 when its best IoU is below $\tau_-$, and then 1 when it is at least $\tau_+$; since $\tau_- < \tau_+$ at most one of the two applies. Then for each ground truth box $j$ with a largest IoU $b_j > 0$ over the inside anchors, it sets every inside anchor with IoU $b_j$ to 1 and matches it to $j$. An anchor that reaches $b_j$ is positive by the rule, and the code may overwrite a 0 there, as the rule asks, since a forced positive is not negative. Anchors that cross the border are never touched and stay at $-1$. The last statement holds because the anchors that reach $b_j$ are set to 1 and nothing later sets a label back to 0 or $-1$. $\square$

The match is a fine point. If one anchor reaches the largest IoU for two boxes, it is positive for both but matched, for its regression target, to the later one in the code, so the earlier box can have a positive anchor that does not regress towards it. The rule of the paper does not say which box wins; this page keeps the later box.

**Claim 4 (sampling).** With $n_+$ positives and $n_-$ negatives, the sampled batch has $\min(n_+, \lfloor b/2 \rfloor)$ positives and $\min(n_-, b - \text{that number})$ negatives, all other anchors ignored. So it has at most $b$ anchors, at most half of them positive, and each sampled label equals the label of Claim 3.

*Proof.* The code samples without replacement from the list of positives and then from the list of negatives, with these counts, and keeps the labels of the sampled anchors. $\square$

**Claim 5 (RPN loss).** The loss of the code is $\frac{1}{N_{cls}} \sum_{i \text{ sampled}} -\log(\cdot) + \frac{\lambda}{N_{reg}} \sum_{i \text{ positive}} \sum_c \operatorname{smooth}_{L_1}(t_{ic} - t^*_{ic})$ with $N_{cls}$ the number of sampled anchors, which is the formula of the paper with $p^*_i$ as the indicator of a positive.

*Proof.* The code sums the log loss of $p_i$ for positives and of $1 - p_i$ for negatives over the sampled anchors, divides by their number, and adds $\lambda / N_{reg}$ times the smooth L1 terms of the positives only. $\square$
