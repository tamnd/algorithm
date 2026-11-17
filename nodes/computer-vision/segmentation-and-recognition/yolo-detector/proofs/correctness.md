---
title: The decoded centers lie in their cells, the output is sorted and suppressed per class, the version 1 loss vanishes exactly on the targets and weights small boxes more, and the converged clustering assigns each shape to a center of largest IoU
proves: [correctness]
status: full
---

The network is learned and outside the claims. The claims are about the steps of the page that are not learned, as the Python code does them. A box is $(x_1, y_1, x_2, y_2)$ in pixels on an image of $W \times H$, and the grid has $S \times S$ cells.

**Claim 1 (decoding).** In version 1, a box of cell $(i, j)$ with $0 \le x, y \le 1$ has its center in $[jW/S, (j+1)W/S] \times [iH/S, (i+1)H/S]$, the cell. In version 2, the center $(\sigma(t_x) + c_x, \sigma(t_y) + c_y)$ lies in the open cell $(c_x, c_x + 1) \times (c_y, c_y + 1)$ for every real $t$, and the objectness $\sigma(t_o)$ lies in $(0, 1)$.

*Proof.* The version 1 center is $((j + x)W/S, (i + y)H/S)$, and $j \le j + x \le j + 1$. The sigmoid takes values in $(0, 1)$. $\square$

In floating point the sigmoid can round to 0 or 1 for large $|t|$, so the test allows the closed cell.

**Claim 2 (output).** The detection returns a list in order of non-increasing score. Every score is above $\tau_{score}$, and two boxes of the same class have IoU at most $\tau$.

*Proof.* For a class $c$, line L5 keeps only the boxes with score above $\tau_{score}$. Greedy NMS visits them by non-increasing score and keeps a box only if its IoU with every box kept so far for $c$ is at most $\tau$. Any two kept boxes of $c$ were compared when the later one was kept. The merged list is then sorted by score. Boxes of different classes are never compared. $\square$

**Claim 3 (loss).** Let each cell hold at most one truth center, and let all widths and heights be non-negative. In a truth cell, let $r$ be the responsible predictor of the code: the first predictor of largest IoU with the truth. The version 1 loss of the code is non-negative. It is zero if and only if all of the following hold:

1. in each truth cell, $r$ gives the target $x, y, w, h$ and confidence 1;
2. every other predictor in the grid has confidence 0;
3. the class vector of each truth cell is one-hot on its class.

*Proof.* Every term is a square times a positive weight, so the loss is non-negative, and it is zero exactly when every term is zero. The no-object terms are zero exactly when item 2 holds, and the class terms are zero exactly when item 3 holds. It is left to show that the terms of $r$ are zero exactly when item 1 holds. If item 1 holds, the box of $r$ is the truth, its IoU is 1, and the confidence term is $(1 - 1)^2 = 0$, as are the coordinate terms. Conversely, if the coordinate terms of $r$ are zero, then $x$ and $y$ equal the targets and $\sqrt{w}, \sqrt{h}$ equal the square roots of the targets, so $w$ and $h$ equal the targets. Then the box of $r$ is the truth, its IoU is 1, and a zero confidence term gives confidence 1. $\square$

The test builds outputs of this kind. It puts the truth values at a random predictor index and sets all other values to zero. A predictor with all values zero has an empty box of IoU 0, so the predictor with the truth values is $r$.

**Claim 4 (small boxes).** For a fixed error $\delta > 0$ in the width, the term $(\sqrt{w + \delta} - \sqrt{w})^2$ falls as $w$ grows.

*Proof.* $\sqrt{w + \delta} - \sqrt{w} = \delta / (\sqrt{w + \delta} + \sqrt{w})$, which is positive and falls as $w$ grows, so its square falls too. $\square$

So an error of $0.05$ in $w$ costs more on a box of width $0.1$ than on a box of width $0.8$. With a plain square, the costs would be the same.

**Claim 5 (clusters).** If the clustering ends because the assignment did not change, then each shape is assigned to a center of largest IoU with it, with ties to the lower index. Also, each center that has shapes is the mean of its shapes.

*Proof.* In each round, the code first assigns every shape to the index of largest IoU with the current centers. If this assignment equals the one of the round before, the loop stops before it moves the centers. The current centers were computed as the means of that same assignment. So the assignment is the best one for the final centers, and the centers are its means. $\square$

If the loop ends at the iteration limit, the last step moved the centers, and the assignment may not match them. The test uses data that converges well before the limit. The mean does not minimize $\sum (1 - \text{IoU})$ in a cluster, unlike the squared Euclidean case. So there is no proof that the cost falls at each round, and the method is a heuristic, as in YOLO9000.
