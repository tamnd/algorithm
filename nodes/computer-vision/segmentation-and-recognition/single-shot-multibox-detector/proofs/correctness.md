---
title: The default boxes have the stated shapes and count, the matching gives each truth its own box when it can and makes every box of IoU above the threshold positive, the mining keeps the hardest negatives, and the output is sorted and suppressed per class
proves: [correctness]
status: full
---

The network is learned and outside the claims. The claims are about the steps of the page that are not learned, as the Python code does them. A corner box is $(x_1, y_1, x_2, y_2)$ and a default box is $(c_x, c_y, w, h)$.

**Claim 1 (default boxes).** Let map $k$ have $f_k \times f_k$ cells, scale $s_k$ and ratio list $R_k$. Every box of map $k$ made from a ratio $a \in R_k$ has area $s_k^2$ and $w/h = a$. The extra box has side $\sqrt{s_k s_{k+1}}$. The number of boxes is $\sum_k f_k^2 n_k$, with $n_k = |R_k| + [1 \in R_k]$.

*Proof.* $w h = s_k\sqrt{a} \cdot s_k/\sqrt{a} = s_k^2$ and $w/h = a$. The code makes $n_k$ shapes for map $k$ and places all of them at each of the $f_k^2$ cell centers. $\square$

For SSD300, $n_k = 4, 6, 6, 6, 4, 4$ and the count is $8732$.

**Claim 2 (matching).** Let $m(i)$ be the truth of box $i$, or $-1$. Then:

1. the boxes matched in step 1 are distinct, and so are their truths;
2. a truth $g$ has no box only if every box with positive IoU with $g$ was matched in step 1 to another truth;
3. a box whose best IoU is above the threshold $t$ is positive;
4. a negative box has IoU at most $t$ with every truth;
5. a matched box has positive IoU with its truth, and a box matched in step 2 has a truth of largest IoU.

*Proof.* Step 1 removes the chosen box and the chosen truth from the free sets after each pair, so no box or truth is chosen twice. This gives item 1. Step 1 stops when no free truth or no free box is left, or when the largest IoU over the free pairs is 0. Suppose truth $g$ is still free at the end. Then either no box is free, or every free box has IoU 0 with $g$. In both cases, every box with positive IoU with $g$ is not free, so it was matched in step 1, and to a truth other than $g$, since $g$ is free. This gives item 2. In step 2 every free box $i$ takes a truth $j$ of largest IoU, and is matched when that IoU is above $t$. A box of best IoU above $t$ is thus matched in step 1 or in step 2, which gives item 3. A box that stays negative was free in step 2 with best IoU at most $t$, which gives item 4. Step 1 only takes pairs of positive IoU, and step 2 only matches IoU above $t \geq 0$, which gives item 5. $\square$

Item 2 shows when the first rule of the paper, the best box for each truth, can fail. If two truths have the same best box, only one can have it. The greedy step gives the other truth its best free box, as the bipartite matching of MultiBox does.

**Claim 3 (hard negatives).** With $N$ positives and $n_-$ negatives, the kept negatives are $\min(3N, n_-)$ negatives, and no negative that is left out has a larger background loss than a kept one. So negatives and positives are at most 3:1.

*Proof.* The code sorts the negatives by non-increasing loss, with ties by index, and takes a prefix of that length. An element after the prefix has a loss at most that of every element in it. $\square$

**Claim 4 (loss).** The code returns $\frac{1}{N}(L_{conf} + \alpha L_{loc})$, with $L_{conf}$ the sum of $-\log p_{i, c(i)}$ over the positives and of $-\log p_{i,0}$ over the kept negatives, and $L_{loc}$ the sum of $\operatorname{smooth}_{L_1}$ over the four offsets of the positives against the encoded truth. It returns 0 when $N = 0$.

*Proof.* This is the code line by line, with the softmax of the scores as $p$. $\square$

**Claim 5 (output).** The detection returns at most $K$ triples (score, class, box), in order of non-increasing score. Each score is above $\tau_{conf}$, and two boxes of the same class have IoU at most $\tau$.

*Proof.* For each class, the candidates are the boxes with a probability above $\tau_{conf}$. Greedy NMS keeps a candidate only if its IoU with every box kept so far for the class is at most $\tau$. The candidates of other classes are never compared, so the statement holds only inside a class. The merged list is sorted by non-increasing score, and its first $K$ items are returned. A prefix of a list keeps both the order and the pairwise property. $\square$
