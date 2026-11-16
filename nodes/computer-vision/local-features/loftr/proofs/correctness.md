---
title: Correctness of the LoFTR matching steps
proves: [correctness]
status: full
---

This proof covers the matching steps only: lines L1 to L8 of the main page, on given coarse features $f^A_1, \dots, f^A_m$ and $f^B_1, \dots, f^B_n$ in $\mathbb{R}^d$, with $m, n \ge 1$, given fine feature maps, a temperature $\tau > 0$, a threshold $\theta$, a window size $w$ and a scale $s > 0$. Nothing here says that the networks give good features; that is a measured property.

Line L1 sets $S_{ij} = \langle f^A_i, f^B_j \rangle / \tau$. Line L2 sets $R_{ij} = e^{S_{ij}} / \sum_k e^{S_{ik}}$ and $C_{ij} = e^{S_{ij}} / \sum_k e^{S_{kj}}$, and line L3 sets $P_{ij} = R_{ij} C_{ij}$.

**Lemma 1 (bounds).** Each $P_{ij}$ is in $(0, 1]$, with $P_{ij} \le R_{ij}$ and $P_{ij} \le C_{ij}$. Each row sum and each column sum of $P$ is at most 1.

*Proof.* $R_{ij}$ and $C_{ij}$ are in $(0, 1]$, so their product is positive and at most each factor. A row of $R$ sums to 1, so a row of $P$ sums to $\sum_j R_{ij} C_{ij} \le \sum_j R_{ij} = 1$. Columns are the same with $C$. $\square$

**Lemma 2 (a value above one half is a mutual best).** If $P_{ij} > 1/2$, then $P_{ij}$ is the unique largest value in row $i$ and in column $j$. So with $\theta > 1/2$ the mutual check of line L4 removes nothing: the matches are exactly the pairs with $P_{ij} \ge \theta$.

*Proof.* By Lemma 1, the other entries of row $i$ sum to at most $1 - P_{ij} < 1/2 < P_{ij}$, so each is smaller than $P_{ij}$. Column $j$ is the same. $\square$

**Lemma 3 (invariance and symmetry).** Adding a constant $t$ to every $S_{ij}$ does not change $P$. Swapping the two images transposes $P$, and the set of pairs of line L4 is the same up to the swap.

*Proof.* The factor $e^t$ cancels in each softmax. Swapping the images replaces $S$ by $S^T$, which swaps the row and the column softmax, so $P$ becomes $P^T$. Line L4 keeps $(i, j)$ when $j$ is the first largest entry of row $i$ and $i$ is the first largest entry of column $j$; for $P^T$ the two conditions swap roles, so the same pairs are kept. $\square$

**Lemma 4 (the output of line L4 is a matching).** Each $i$ and each $j$ is in at most one pair, and each pair has $P_{ij} \ge \theta$.

*Proof.* Each row has one first best column and each column one first best row. A pair $(i, j)$ needs both, so two pairs with the same $i$ would have the same $j$, and two pairs with the same $j$ would have the same $i$. $\square$

Now the refinement. Let $c$ be the fine vector of A, let $K$ be the set of window positions inside the fine map of B, with positions $x_k \in \mathbb{R}^2$ and vectors $g_k$, and let $q_k = e^{s \langle c, g_k \rangle} / \sum_{l \in K} e^{s \langle c, g_l \rangle}$ be the weights of line L7. Line L8 returns $\hat x = \sum_k q_k x_k$.

**Lemma 5 (the refined position).** $\hat x$ is in the convex hull of the positions of $K$, so it is inside the window and inside the fine map. If one position $k^*$ has a score larger than every other by at least $\Delta$, that is $s \langle c, g_{k^*} \rangle \ge s \langle c, g_k \rangle + \Delta$ for all $k \ne k^*$, then

$$\lVert \hat x - x_{k^*} \rVert \le (|K| - 1) \, e^{-\Delta} \max_k \lVert x_k - x_{k^*} \rVert.$$

*Proof.* The weights are positive and sum to 1, so $\hat x$ is a convex combination of the $x_k$. For the bound, $\hat x - x_{k^*} = \sum_{k \ne k^*} q_k (x_k - x_{k^*})$, and $q_k \le e^{-\Delta} q_{k^*} \le e^{-\Delta}$ for $k \ne k^*$. The triangle inequality gives the bound. $\square$

For a $w \times w$ window, $|K| \le w^2$ and $\max_k \lVert x_k - x_{k^*} \rVert \le (w - 1)\sqrt{2}$, so the refined position tends to the best window position as the gap $\Delta$ grows.

**Theorem.** The coarse matches are a partial matching of the coarse cells with confidence at least $\theta$, they do not depend on a constant shift of the scores, and they are symmetric in the two images. For $\theta > 1/2$ they are exactly the pairs with $P_{ij} \ge \theta$. Each refined position is a convex combination of the window positions, and it is within $(w^2 - 1) e^{-\Delta} (w - 1) \sqrt{2}$ fine pixels of the best window position when that position leads the others by $\Delta$ in score.

*Proof.* Lemmas 1 to 5. $\blacksquare$
