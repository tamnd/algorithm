---
title: Ward's method merges by the exact increase of the sum of squares
proves: [correctness]
status: full
---

For a finite set $S$ of points of $\mathbb{R}^d$, let $c_S = \frac{1}{|S|}\sum_{p \in S} p$ and $\text{SSE}(S) = \sum_{p \in S} \lVert p - c_S \rVert^2$. For disjoint $A$ and $B$, let $\Delta(A, B) = \text{SSE}(A \cup B) - \text{SSE}(A) - \text{SSE}(B)$.

**Lemma 1 (parallel axis).** For each point $z$, $\sum_{p \in S} \lVert p - z \rVert^2 = \text{SSE}(S) + |S| \lVert c_S - z \rVert^2$.

*Proof.* Write $p - z = (p - c_S) + (c_S - z)$ and expand. The cross term is $2 \langle \sum_{p \in S} (p - c_S),\ c_S - z \rangle = 0$, because $\sum_{p \in S} (p - c_S) = 0$. $\square$

**Lemma 2 (the increase).** $\Delta(A, B) = \dfrac{n_A n_B}{n_A + n_B} \lVert c_A - c_B \rVert^2$, where $n_A = |A|$ and $n_B = |B|$.

*Proof.* Let $s = n_A + n_B$ and $c = c_{A \cup B} = (n_A c_A + n_B c_B)/s$. Split the sum of $\text{SSE}(A \cup B)$ into the points of $A$ and of $B$, and apply Lemma 1 to each part with $z = c$:

$$\text{SSE}(A \cup B) = \text{SSE}(A) + n_A \lVert c_A - c \rVert^2 + \text{SSE}(B) + n_B \lVert c_B - c \rVert^2.$$

Now $c_A - c = \frac{n_B}{s}(c_A - c_B)$ and $c_B - c = \frac{n_A}{s}(c_B - c_A)$. So the extra terms are $\bigl(\frac{n_A n_B^2}{s^2} + \frac{n_B n_A^2}{s^2}\bigr) \lVert c_A - c_B \rVert^2 = \frac{n_A n_B}{s} \lVert c_A - c_B \rVert^2$. $\square$

**Theorem.** WARD$(P)$ returns $n - 1$ merges. Merge $t$ joins two current clusters $A$, $B$ with the smallest $\Delta(A, B)$ over all pairs of current clusters, and records $h_t = \Delta(A, B)$. Also $\sum_t h_t = \text{SSE}(P)$, and after the first $m$ merges the current clusters have total sum of squares $h_1 + \cdots + h_m$.

*Proof.* We show this invariant for the loop of line L2: for each active slot $i$, $c[i]$ is the centroid of the cluster $C_i$ in slot $i$, and $\text{size}[i] = |C_i|$. It holds at line L1, where each cluster is one point. In a round, lines L3 and L4 compute, for each pair, the value $\frac{\text{size}[i]\,\text{size}[j]}{\text{size}[i] + \text{size}[j]} \lVert c[i] - c[j] \rVert^2$, which is $\Delta(C_i, C_j)$ by the invariant and Lemma 2. So the pair kept is a pair with the least increase, as the greedy rule asks. Line L5 sets $c[i]$ to $(n_i c_i + n_j c_j)/(n_i + n_j)$, which is the centroid of $C_i \cup C_j$, and line L7 sets the size. So the invariant holds again. Each round drops one slot, so there are $n - 1$ rounds.

Let $T_m$ be the total sum of squares of the clusters after $m$ merges. Then $T_0 = 0$, since each single point has $\text{SSE} = 0$, and $T_m = T_{m-1} + h_m$ by the definition of $\Delta$. After $n - 1$ merges, one cluster holds $P$, so $\text{SSE}(P) = T_{n-1} = \sum_t h_t$. $\square$

**Lemma 3 (the Lance-Williams row).** For disjoint clusters $I$, $J$, $K$ with sizes $n_i$, $n_j$, $n_k$ and $t = n_i + n_j + n_k$,

$$\Delta(K, I \cup J) = \frac{n_i + n_k}{t} \Delta(K, I) + \frac{n_j + n_k}{t} \Delta(K, J) - \frac{n_k}{t} \Delta(I, J).$$

*Proof.* With $s = n_i + n_j$ and $c = (n_i c_I + n_j c_J)/s$, the identity $\lVert u - c \rVert^2 = \frac{n_i}{s}\lVert u - c_I \rVert^2 + \frac{n_j}{s}\lVert u - c_J \rVert^2 - \frac{n_i n_j}{s^2}\lVert c_I - c_J \rVert^2$ holds for each point $u$. It follows by expansion, as in the proof of the [Lance-Williams formula](/agglomerative-clustering/). Put $u = c_K$, multiply by $n_k s / t$, and replace each squared centroid distance by Lemma 2: $\lVert c_K - c_I \rVert^2 = \frac{n_k + n_i}{n_k n_i}\Delta(K, I)$, and so on. $\square$

**Lemma 4 (reducibility and monotone heights).** If $\Delta(I, J) \le \min(\Delta(I, K), \Delta(J, K))$, then $\Delta(I \cup J, K) \ge \min(\Delta(I, K), \Delta(J, K))$. So $h_1 \le h_2 \le \cdots \le h_{n-1}$.

*Proof.* Let $m = \min(\Delta(I, K), \Delta(J, K))$. In Lemma 3 the first two coefficients are positive, the third is negative, and the three add up to $1$. So $\Delta(I \cup J, K) \ge \frac{n_i + n_k}{t} m + \frac{n_j + n_k}{t} m - \frac{n_k}{t} \Delta(I, J) \ge \frac{n_i + n_j + n_k}{t} m = m$, using $\Delta(I, J) \le m$. At step $t$, the merged pair $I, J$ has the least increase, so every value after the merge is at least $\Delta(I, J) = h_t$, and $h_{t+1} \ge h_t$. $\square$

**The cut is not an optimal k-means partition.** On the points $0, 1, 2, 3, 5$ of the line, the merges are $\{0, 1\}$ at $1/2$, then $\{2, 3\}$ at $1/2$, then $\{0, 1, 2, 3\}$ at $4$ (against $\frac{2}{3} \cdot (5 - 5/2)^2 = 25/6$ for $\{2, 3\}$ with $5$), then all at $\frac{4}{5}(5 - 3/2)^2 = 49/5$. The cut at $k = 2$ has sum of squares $1/2 + 1/2 + 4 = 5$, while $\{0, 1, 2\}$, $\{3, 5\}$ has $2 + 2 = 4$.

**Running time.** The round with $m$ active slots computes $m(m - 1)/2$ values at $O(d)$ time each, so the total is $\Theta(n^3 d)$. The centroids and sizes take $\Theta(n d)$ memory.
