---
title: The chronogram bound for dynamic partial sums
proves: [statement]
status: full
---

We prove Theorem 1. Fix a deterministic structure for partial sums over $\mathbb{Z}/2^\delta$ on positions $1, \ldots, n$ in the cell-probe model with $b$-bit cells and at most $2^b$ cells, $4 \le \delta \le b$, whose updates each probe at most $t_u \ge 1$ cells. Let $\beta$ be the least power of 2 with $\beta \ge 32 t_u b/\delta$; then $\beta \ge 32$, because $b \ge \delta$. Let $n = \beta^K$. The memory starts in a fixed state. A query `sum(x)` is a decision tree: the next cell it reads depends on the contents read so far.

**The random input.** The updates come in $K$ epochs, in the time order epoch $K$, epoch $K - 1$, ..., epoch 1. Epoch $i$ has $\beta^i$ updates, at the positions $p^{(i)}_l = l \cdot n/\beta^i$ for $l = 1, \ldots, \beta^i$, in increasing order of $l$, with values $\Delta^{(i)}_l$. All values of all epochs are independent and uniform in $\mathbb{Z}/2^\delta$. After epoch 1, one query `sum(x)` is made, with $x$ uniform in $\{1, \ldots, n\}$ and independent of the values.

For a cell $c$ read by the query, its *epoch* is the epoch of the last update that wrote it, or none if no update wrote it. Let $Q_i$ be the event that the query reads at least one cell whose epoch is $i$.

**Lemma.** For each $i \in \{1, \ldots, K\}$, $\Pr[Q_i] \ge \frac12$.

*Proof.* Write $x = p^{(i)}_J + y$ with $J \in \{0, \ldots, \beta^i - 1\}$ and $y \in \{1, \ldots, n/\beta^i\}$, with $p^{(i)}_0 = 0$. For $x$ uniform, $J$ and $y$ are independent and uniform. It is enough to prove $\Pr[Q_i] \ge \frac12$ conditioned on any fixed $y$ and any fixed values $V$ of all epochs other than $i$; then average. So fix $y$ and $V$. The only randomness left is $D = (\Delta^{(i)}_1, \ldots, \Delta^{(i)}_{\beta^i})$, uniform over $2^{\delta\beta^i}$ values, and $J$.

For $j \in \{0, \ldots, \beta^i - 1\}$ let $x_j = p^{(i)}_j + y$. The epoch-$i$ positions that are at most $x_j$ are exactly $p^{(i)}_1, \ldots, p^{(i)}_j$, because $p^{(i)}_{j+1} = p^{(i)}_j + n/\beta^i \ge x_j + 1$ when $y \le n/\beta^i - 1$, and for $y = n/\beta^i$, $x_j = p^{(i)}_{j+1}$, and then the positions are $p^{(i)}_1, \ldots, p^{(i)}_{j+1}$. In both cases the answer to `sum(x_j)` is $C_j + P_{j'}$, where $C_j$ is the sum of the values of the other epochs at positions at most $x_j$, which depends only on $V$, and $P_{j'} = \Delta^{(i)}_1 + \cdots + \Delta^{(i)}_{j'}$ with $j' = j$ or $j' = j + 1$, an index fixed by $y$. As $j$ runs over $0, \ldots, \beta^i - 1$, the index $j'$ runs over a set of $\beta^i$ consecutive integers that contains all of $1, \ldots, \beta^i - 1$ and one of $0$ or $\beta^i$.

Call $j$ *good* if `sum(x_j)`, run after all updates, reads no cell of epoch $i$, and *bad* otherwise. Let $G$ be the set of good $j$, a function of $D$.

*The message.* Given $D$ (and the fixed $y$, $V$), the encoder writes:

1. the mask of $G$, $\beta^i$ bits;
2. the number $s$ of cells written by the updates of epochs $1, \ldots, i - 1$, in $b$ bits, and then, for each such cell, its address and its contents after the last update, $2b$ bits each;
3. for each bad $j$, in increasing order, the value $P_{j'}$, $\delta$ bits each;
4. if $j' = j + 1$ (the case $y = n/\beta^i$), also $P_{\beta^i}$ is covered; if $j' = j$, the value $P_{\beta^i}$ is not an answer, and the encoder adds it, $\delta$ bits.

Each update probes at most $t_u$ cells, so $s \le t_u \sum_{j=1}^{i-1} \beta^j \le 2 t_u \beta^{i-1}$, because $\beta \ge 2$. A cell address fits in $b$ bits, because the model has at most $2^b$ cells, and so does $s$. So part 2 has at most $b + 4 t_u b\beta^{i-1}$ bits.

*The message is prefix-free.* The decoder reads the mask, which has a fixed length; then $s$; then $2bs$ bits; then $\delta$ bits for each bad $j$, a number it knows from the mask; then $\delta$ more bits or none, which it knows from $y$. So no message is a proper prefix of another one.

*Decoding.* The decoder knows $y$ and $V$. It runs the structure on the updates of epochs $K, \ldots, i + 1$, which it knows, and gets the memory $M$ just before epoch $i$. For a good $j$, it simulates `sum(x_j)`: when the query reads a cell, it takes the contents from part 2 if the cell is listed there, and from $M$ otherwise. Let us check that this gives the true contents of every cell that the true query reads. A cell listed in part 2 was last written in epochs $1, \ldots, i - 1$, and part 2 gives its final contents. A cell not listed was not written after epoch $i$; since $j$ is good, the cell was not last written in epoch $i$ either; so its contents are those of $M$. By induction over the reads of the decision tree, the simulation follows the true query and returns the true answer $C_j + P_{j'}$. The decoder knows $C_j$, so it gets $P_{j'}$. For bad $j$, part 3 gives $P_{j'}$. With part 4, the decoder knows $P_0 = 0$ and $P_1, \ldots, P_{\beta^i}$, so it knows $\Delta^{(i)}_l = P_l - P_{l-1}$ for all $l$, which is $D$.

The decoder does not know which simulations would be correct without the mask; that is why the mask is sent.

*Counting.* The map from $D$ to the message is injective and prefix-free, and $D$ is uniform over $2^{\delta\beta^i}$ values. By the source coding theorem (Kraft's inequality), the expected length of the message is at least $\delta\beta^i$. Let $B = \beta^i - |G|$ be the number of bad $j$. Then

$$\delta\beta^i \le \beta^i + b + 4 t_u b \beta^{i-1} + \delta\,\mathbb{E}[B] + \delta.$$

Divide by $\delta\beta^i$:

$$\frac{\mathbb{E}[B]}{\beta^i} \ge 1 - \frac1\delta - \frac{b + \delta}{\delta\beta^i} - \frac{4 t_u b}{\delta\beta}.$$

Now $1/\delta \le 1/4$. Next $4 t_u b/(\delta\beta) \le 4/32 = 1/8$ by the choice of $\beta$. And $(b + \delta)/(\delta\beta^i) \le 2b/(\delta\beta) \le 2/(32 t_u) \le 1/16$. So $\mathbb{E}[B]/\beta^i \ge 1 - \frac14 - \frac18 - \frac1{16} > \frac12$.

For fixed $y$, the event $Q_i$ happens exactly when $J$ is bad, and $J$ is uniform over $\{0, \ldots, \beta^i - 1\}$ and independent of $D$, so $\Pr[Q_i \mid y, V] = \mathbb{E}[B]/\beta^i > \frac12$. Averaging over $y$ and $V$ proves the lemma. $\square$

**The theorem.** Each cell that the query reads has at most one epoch, so the number of cells it reads is at least the number of $i$ for which $Q_i$ happens. By linearity of expectation and the lemma, the expected number of cells read is at least $\sum_{i=1}^K \Pr[Q_i] \ge K/2$. The expectation is over the values and over $x$. So some fixed choice of the values gives a sequence of updates after which the average over $x$ of the cost of `sum(x)` is at least $K/2 = \lg n/(2\lg\beta)$. Finally $\beta < 64 t_u b/\delta$, so $\lg\beta < 6 + \lg(t_u b/\delta)$. $\blacksquare$
