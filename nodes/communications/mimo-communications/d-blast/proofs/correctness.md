---
title: D-BLAST visits every antenna with every layer, is exact without noise, and its middle layers see the full log-det rate with MMSE nulling
proves: [correctness]
status: full
---

The channel is $y_t = H x_t + w_t$ with $H \in \mathbb{C}^{m \times n}$ fixed over the frame, columns $h_0, \ldots, h_{n-1}$, and $w_t \sim \mathcal{CN}(0, N_0 I)$ independent over $t$. Block $k$ of layer $l$ is on antenna $k$ at block time $l + k$, for $0 \le l < L$ and $0 \le k < n$. Write $a = 0$ for ZF and $a = N_0 / E_s$ for MMSE. For a set $A$ of antennas, $H_A$ is the matrix of their columns and $P^A = (H_A^H H_A + a I)^{-1}$.

**Lemma 1 (the layer map).** At block time $t$, antenna $k$ carries at most one block, namely block $k$ of layer $t - k$ when $0 \le t - k < L$. Each layer has exactly one block on each antenna. The frame uses the block times $0, \ldots, L + n - 2$, so it has $L + n - 1$ of them and carries $L n$ blocks in $(L + n - 1) n$ antenna slots.

*Proof.* Block $k$ of layer $l$ is at $(t, k) = (l + k, k)$. The map $(l, k) \mapsto (l + k, k)$ is one to one, and its inverse is $(t, k) \mapsto (t - k, k)$, so each slot holds at most one block. For a fixed $l$ the antennas $k = 0, \ldots, n - 1$ each occur once. The smallest time is $0 + 0$ and the largest is $(L - 1) + (n - 1)$. $\square$

So the rate is $L n / ((L + n - 1) n) = L / (L + n - 1)$ of the rate of $n$ full streams.

**Lemma 2 (who is cancelled and who is nulled).** At the step for block $k$ of layer $l$, at time $t = l + k$, an active antenna $k' > k$ carries the layer $t - k' < l$, and an active antenna $k' < k$ carries the layer $t - k' > l$.

*Proof.* $t - k' = l + (k - k')$, which is less than $l$ when $k' > k$ and more than $l$ when $k' < k$. $\square$

Lines L1 and L2 decode the layers in increasing order, so when the receiver reaches layer $l$, every layer $t - k' < l$ is decided. Line L4 subtracts exactly these, and line L5 nulls exactly the active antennas that carry later layers. If the earlier decisions are right, after line L4

$$r = H_A x_{t, A} + w_t, \qquad A = \{k' < k : 0 \le t - k' < L\} \cup \{k\}. \tag{1}$$

**Theorem 3 (exact without noise).** With ZF nulling ($a = 0$, $H$ of full column rank) and $w_t = 0$ for all $t$, the receiver returns every symbol of every layer, with either decoder of line L8.

*Proof.* By induction over the layers. Suppose that the layers $0, \ldots, l - 1$ are decided correctly. By Lemma 2 and equation (1), $r = H_A x_{t, A}$ for each block $k$ of layer $l$. The ZF filter $P^A H_A^H$ satisfies $P^A H_A^H H_A = I$, so its row for antenna $k$ gives $z_k = x_{t, k}$, the transmitted symbol. Slicing returns it at distance 0. With the repetition decoder, every $z_k$ equals the same symbol $s$, so the weighted mean is $s$ too. So layer $l$ is decided correctly. $\square$

**Lemma 4 (the SNR or SINR of a block).** Assume correct earlier decisions. The output $z_k$ of line L6 has the SNR $(E_s / N_0) / P^A_{kk}$ for ZF and the unbiased SINR $1 / (a P^A_{kk}) - 1$ for MMSE, where $A$ is the set of equation (1).

*Proof.* By equation (1), this is one step of nulling on the channel $H_A$, so Lemma 2 of the [V-BLAST proof](/v-blast/) applies with $K = A$. $\square$

**Theorem 5 (block 0 is maximal ratio combining).** For every layer, block 0 has $A = \{0\}$, and its SNR or SINR is $\|h_0\|^2 E_s / N_0$.

*Proof.* For $k = 0$ there is no antenna $k' < 0$, so $A = \{0\}$ and $P^A = 1 / (\|h_0\|^2 + a)$. For ZF, $(E_s / N_0) / P^A = \|h_0\|^2 E_s / N_0$. For MMSE, $1 / (a P^A) - 1 = (\|h_0\|^2 + a) / a - 1 = \|h_0\|^2 / a = \|h_0\|^2 E_s / N_0$. $\square$

**Theorem 6 (the middle layers see the full rate).** With MMSE nulling and correct earlier decisions, every layer $l \le L - n$ has

$$\sum_{k = 0}^{n - 1} \log_2(1 + \gamma_k) = \log_2 \det\left(I + \frac{E_s}{N_0} H^H H\right),$$

and every layer $l > L - n$ has a sum at least this large.

*Proof.* For $l \le L - n$ and $k' < k$, $t - k' = l + k - k' \le l + n - 1 \le L - 1$, so every antenna $k' < k$ is active and $A = \{0, \ldots, k\}$. These sets grow by one antenna from $k = 0$ to $k = n - 1$. Read in the order $k = n - 1, n - 2, \ldots, 0$, they are the sets $K_t$ of an MMSE-SIC run on $H$ with the order $(n - 1, n - 2, \ldots, 0)$: stream $k$ is detected when the remaining set is $\{0, \ldots, k\}$. Theorem 6 of the [V-BLAST proof](/v-blast/) holds for every order, so the sum of $\log_2(1 + \gamma_k)$ is $\log_2 \det(I + (E_s / N_0) H^H H)$.

For $l > L - n$, some antennas $k' < k$ are silent, so $A$ is a subset of $\{0, \ldots, k\}$ that contains $k$. By Lemma 3 of the V-BLAST proof, removing interferers never lowers the SINR, so each $\gamma_k$ is at least its value for a middle layer, and so is the sum. $\square$

**Theorem 7 (combining the blocks).** Suppose that the $n$ unbiased outputs of a layer are $z_k = s + e_k$, where $s$ is a symbol of energy $E_s$ repeated in all blocks, $E[e_k] = 0$, $E|e_k|^2 = E_s / \gamma_k$, and the $e_k$ are uncorrelated. Then the weighted mean $\bar z = \sum_k \gamma_k z_k / \sum_k \gamma_k$ is unbiased with SINR $\sum_k \gamma_k$, and no other unbiased linear combination has a larger SINR.

*Proof.* A combination $\sum_k c_k z_k$ with $\sum_k c_k = 1$ is unbiased and has error variance $\sum_k |c_k|^2 E_s / \gamma_k$. By the Cauchy-Schwarz inequality,

$$1 = \left|\sum_k c_k\right|^2 = \left|\sum_k \frac{c_k}{\sqrt{\gamma_k}} \sqrt{\gamma_k}\right|^2 \le \left(\sum_k \frac{|c_k|^2}{\gamma_k}\right)\left(\sum_k \gamma_k\right),$$

so the error variance is at least $E_s / \sum_k \gamma_k$, with equality when $c_k$ is proportional to $\gamma_k$. The SINR is $E_s$ divided by the error variance. $\square$

The noise terms of different blocks are independent, because the blocks of a layer are at different block times. With ZF there is no residual interference, so the condition of Theorem 7 always holds. With MMSE, the residual interference of block $k$ comes from the later layers that block $k$ nulls; it is uncorrelated between blocks when the symbols in different blocks are independent, as for $n = 2$ or for coded symbols. For a capacity-achieving code over the $n$ blocks, the layer can be decoded when its rate is below $\sum_k \log_2(1 + \gamma_k)$, which by Theorem 6 is the log-det rate of $H$. A layer then fails only when this rate is below the target rate, which is the outage event of the channel. This is the outage optimality of D-BLAST in Tse and Viswanath, Section 8.5.
