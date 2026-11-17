---
title: The confusion matrix gives the Jaccard index of each class, and properties of the mean
proves: [correctness]
status: full
---

We use the notation of the page. There are $K$ classes, a data set of image pairs $(g, p)$, and a void index. Index the pixels of the data set by $(e, u, v)$, where $e$ is the number of the image. Let $V$ be the set of pixels whose true label is not void. For a class $i$ let
$$G_i = \{x \in V : g(x) = i\}, \qquad P_i = \{x \in V : p(x) = i\}.$$
The procedure MEAN-IOU builds the matrix $n$ in lines L1 to L4 and averages in lines L5 to L9.

**Lemma 1 (the confusion matrix).** After line L4, $n_{ij} = |G_i \cap P_j|$ for all classes $i$ and $j$.

*Proof.* Line L3 skips exactly the pixels outside $V$. Each pixel of $V$ is visited once, in its image, and line L4 adds 1 to the entry $(g(x), p(x))$ and to no other entry. So $n_{ij}$ counts the pixels of $V$ with $g(x) = i$ and $p(x) = j$. $\square$

The matrix does not depend on the order of the images or on the predicted labels at void pixels, since each pixel adds 1 to one entry and void pixels add nothing.

**Theorem 1 (each class score is a Jaccard index).** For each class $i$, the value $t_i$ of line L7 is $|G_i \cup P_i|$, and if $t_i > 0$ then $n_{ii} / t_i = |G_i \cap P_i| / |G_i \cup P_i|$.

*Proof.* The sets $G_i$ for $i = 0, \ldots, K - 1$ partition $V$, and so do the sets $P_j$. So $\sum_j n_{ij} = \sum_j |G_i \cap P_j| = |G_i|$ and $\sum_j n_{ji} = |P_i|$. Line L7 gives $t_i = |G_i| + |P_i| - |G_i \cap P_i| = |G_i \cup P_i|$, by inclusion and exclusion, and $n_{ii} = |G_i \cap P_i|$ by Lemma 1. $\square$

So the score of class $i$ is the [intersection over union](/intersection-over-union/) of the true and the predicted region of class $i$, both taken over the whole data set as one pixel set. Line L8 counts the class only if $t_i > 0$. A class with $t_i = 0$ appears neither in the truth nor in the prediction, and its ratio would be $0/0$. A class that is predicted but never true has $t_i = |P_i| > 0$ and $n_{ii} = 0$, so it counts with the value 0. Line L9 returns the mean of the $c$ counted values, and the procedure returns no value when $c = 0$.

**Corollary 1 (range and the perfect score).** If at least one class is counted, then $0 \le \mathrm{mIoU} \le 1$, and $\mathrm{mIoU} = 1$ if and only if $p(x) = g(x)$ for every $x \in V$.

*Proof.* Each counted value is in $[0, 1]$, since $G_i \cap P_i \subseteq G_i \cup P_i$, so their mean is too. If $p = g$ on $V$, then $P_i = G_i$ for all $i$ and every counted value is 1. Conversely, if the mean is 1, every counted value is 1. If some $x \in V$ had $g(x) = i \ne j = p(x)$, then $x \in G_i \setminus P_i$, so $t_i > 0$ and $|G_i \cap P_i| < |G_i \cup P_i|$, and the value of class $i$ would be below 1. $\square$

**Corollary 2 (relabeling).** If a permutation $\pi$ of the classes is applied to both $g$ and $p$, the mIoU does not change.

*Proof.* The new sets are $G'_{\pi(i)} = G_i$ and $P'_{\pi(i)} = P_i$, so the new values are the old ones in another order. The mean of a set of numbers does not depend on the order. $\square$

**Corollary 3 (Dice).** For a class with $t_i > 0$, the Dice score $D_i = 2 |G_i \cap P_i| / (|G_i| + |P_i|)$ equals $2 J_i / (1 + J_i)$, where $J_i$ is the class IoU. So $D_i$ is an increasing function of $J_i$.

*Proof.* Write $a = |G_i \cap P_i|$ and $t = |G_i \cup P_i|$. Then $|G_i| + |P_i| = t + a$, and $2 J / (1 + J) = 2 (a / t) / ((t + a)/t) = 2a / (t + a)$. The function $J \mapsto 2J/(1 + J)$ has derivative $2/(1 + J)^2 > 0$. $\square$

The mean of the $D_i$ and the mean of the $J_i$ need not rank two predictions in the same order, because the map is not linear. The tests check Corollary 3 per class.

**Proposition 4 (the data set score is not the mean of the image scores).** In general, the mIoU of the confusion matrix summed over the images differs from the mean of the mIoU of each image.

*Proof.* The example of the page is a counterexample: two images with the scores $3/8$ and $1$ have the mean $11/16$, while the summed matrix gives $31/40$. $\square$

**Proposition 5 (pixel accuracy and mIoU).** Pixel accuracy, the trace of $n$ over the sum of $n$, can be close to 1 while the mIoU is close to $\tfrac12$.

*Proof.* Let $V$ have $N$ pixels, all of class 0 but one of class 1, and let $p$ be 0 everywhere. The accuracy is $(N - 1)/N$. Class 0 has IoU $(N - 1)/N$, class 1 has IoU $0/1 = 0$, so the mIoU is $(N - 1)/(2N)$. $\square$

**Cost.** Lines L1 to L4 take $O(K^2 + N)$ time for $N$ pixels in total. Lines L5 to L9 take $O(K^2)$ time as written, or $O(K)$ with the row and column sums kept during the count. The extra space is $O(K^2)$ for the matrix, independent of the number of images.
