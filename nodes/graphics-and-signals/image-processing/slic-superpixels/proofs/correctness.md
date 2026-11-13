---
title: Each SLIC step does what it claims, and the superpixels are connected after the postprocessing
proves: [correctness]
status: full
---

Fix an image with pixels $i$ that have a color $c_i$ and a position $(x_i, y_i)$, centers $C_1, \ldots, C_K$ with $C_j = [c_j, x_j, y_j]$, a number $S > 0$ and a compactness $m > 0$. Write $D(i, j)^2 = \lVert c_i - c_j \rVert^2 + m^2 \bigl((x_i - x_j)^2 + (y_i - y_j)^2\bigr) / S^2$, and say that $C_j$ covers $i$ if $|x_i - x_j| \le S$ and $|y_i - y_j| \le S$. SLIC makes no claim of optimality; the statements below are the ones that hold.

**Lemma 1 (assignment).** After lines L4 to L6, every pixel $i$ covered by at least one center has $l(i) = j$, where $j$ is the least index among the covering centers with the least $D(i, j)$. A pixel covered by no center keeps its old label.

*Proof.* Line L4 sets $d(i) = \infty$. Line L5 visits each center once and, for it, exactly the pixels it covers. So pixel $i$ is tested once against each covering center, in increasing order of $j$, and never against another center. Line L6 replaces $l(i)$ only when $D < d(i)$, so after the loop $d(i)$ is the least $D$ over the covering centers, and $l(i)$ is the first index that reached it, since a later index with the same value fails the strict test. If no center covers $i$, line L6 never runs for $i$. $\square$

**Lemma 2 (update).** For fixed labels, line L7 sets each center with at least one pixel to the point that minimizes $\sum_{l(i) = j} D(i, j)^2$ over all $[c_j, x_j, y_j]$.

*Proof.* The sum splits into $\sum \lVert c_i - c_j \rVert^2$ plus $(m^2 / S^2) \sum \bigl((x_i - x_j)^2 + (y_i - y_j)^2\bigr)$, and each part is a sum of squared distances to a point, which is least at the mean of the points. Both parts are minimized by the mean of $[c_i, x_i, y_i]$, which line L7 computes. $\square$

So the update step never raises the energy $\sum_i D(i, l(i))^2$. The assignment step can raise it: when a center moves, a pixel can leave its window and must take a covering center that is farther than its old one. The tests show a case. This is why the loop is stopped after a fixed number of passes, and why it is not a descent method like k-means. If a pass leaves every center unchanged ($E = 0$), the next assignment sees the same centers and the same old labels, so by Lemma 1 it returns the same labels, and the state is a fixed point.

**Lemma 3 (postprocessing).** After line L9, every pixel has a label, and the pixels with each label form one 4-connected set.

*Proof.* Line L9 keeps, for each label, one connected piece, and removes the label from all other pixels. The kept pieces are disjoint and each one is connected. The other pixels are taken in breadth-first order from the pixels next to the kept pieces. When a pixel is taken, it has at least one labeled neighbor (it entered the queue as the neighbor of a labeled pixel, and labels are never removed), and it takes the label of one of its labeled neighbors. By induction on the order in which pixels get labels, every pixel with label $j$ is joined to the kept piece of $j$ by a path of pixels with label $j$: a kept pixel trivially, and a later pixel through the neighbor whose label it took, which got that label earlier. So the set with label $j$ is connected. The image grid is connected and at least one piece is kept, so the breadth-first search reaches every pixel. $\square$

**Theorem.** The output of the implementation labels every pixel, each label is a connected set, and the returned centers are the exact means of their superpixels. Every assignment step gives each covered pixel its nearest covering center under the stated tie rule.

*Proof.* The last claim is Lemma 1. The loop runs at most the iteration limit, and every pass ends. Lemma 3 gives the labeling and the connectivity. The labels are renumbered by first appearance in raster order, which keeps the partition, and the final centers are computed by line L7 on the final labels, which are the means by Lemma 2. $\square$
