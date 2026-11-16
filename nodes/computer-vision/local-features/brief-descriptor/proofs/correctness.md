---
title: Correctness of the BRIEF descriptor
proves: [correctness]
status: full
---

Fix the tests $(x_i, y_i)$ for $i = 1, \dots, n_d$, the smoothing kernel $G$ with weights $G(\delta) \ge 0$ and $\sum_\delta G(\delta) = Z > 0$, and an image $I$. Let $J = G * I$, so $J(p) = \sum_\delta G(\delta) I(p + \delta)$, and let $\tau_i(k) = 1$ if $J(k + x_i) < J(k + y_i)$ and $0$ otherwise. All keypoints $k$ below have their patch and the smoothing window inside the image, so no border rule is used.

**Lemma 1 (the descriptor).** For each keypoint $k$, lines L4 to L7 output $f(k) = \sum_{i=1}^{n_d} 2^{i-1} \tau_i(k)$.

*Proof.* We show by induction on $i$ that after the iteration $i$ of line L5, $d = \sum_{j \le i} 2^{j-1} \tau_j(k)$. Before the loop $d = 0$ by line L4, the empty sum. In iteration $i$, line L6 adds $2^{i-1}$ exactly when $\tau_i(k) = 1$. So the claim holds after iteration $i$. After iteration $n_d$, $d = f(k)$, and line L7 outputs it. $\square$

**Lemma 2 (the Hamming distance).** Line L8 returns the number of positions in which $a$ and $b$ differ.

*Proof.* Bit $j$ of $a \oplus b$ is 1 exactly when bit $j$ of $a$ differs from bit $j$ of $b$. The words of $a \oplus b$ split its bits into disjoint groups, and the popcount of each word counts the ones in its group. So the sum over the words counts all positions where $a$ and $b$ differ. $\square$

**Lemma 3 (affine change of intensity).** Let $I' = a I + b$ with $a > 0$. Then $f'(k) = f(k)$ for each keypoint $k$.

*Proof.* $J'(p) = \sum_\delta G(\delta)(a I(p + \delta) + b) = a J(p) + b Z$. So $J'(k + x_i) - J'(k + y_i) = a (J(k + x_i) - J(k + y_i))$. Since $a > 0$ this difference is negative exactly when $J(k + x_i) - J(k + y_i)$ is negative, so $\tau'_i(k) = \tau_i(k)$ for each $i$, and by Lemma 1 $f'(k) = f(k)$. $\square$

With integer weights, integer images, integer $a > 0$ and integer $b$, every quantity in this proof is an integer, so the implementation follows the lemma exactly.

**Lemma 4 (shift).** Let $I'(p) = I(p + t)$ for a fixed integer vector $t$. Then the descriptor of $I'$ at $k$ equals the descriptor of $I$ at $k + t$.

*Proof.* $J'(p) = \sum_\delta G(\delta) I(p + t + \delta) = J(p + t)$. So $J'(k + x_i) = J(k + t + x_i)$ and $J'(k + y_i) = J(k + t + y_i)$, and each test of $I'$ at $k$ equals the same test of $I$ at $k + t$. By Lemma 1 the descriptors are equal. $\square$

**Lemma 5 (random strings).** Let $a$ be a fixed string of $n_d$ bits and $b$ a string with independent bits, each 1 with probability $1/2$. Then the Hamming distance of $a$ and $b$ has the binomial distribution with $n_d$ trials and probability $1/2$, with mean $n_d / 2$ and variance $n_d / 4$.

*Proof.* Bit $j$ of $a \oplus b$ is 1 exactly when bit $j$ of $b$ differs from bit $j$ of $a$, which has probability $1/2$ whatever bit $j$ of $a$ is. The bits of $b$ are independent, so the bits of $a \oplus b$ are independent with probability $1/2$ each, and their sum is binomial. $\square$

Lemma 5 is a model for unrelated keypoints, not a fact about images. The tests of BRIEF on real patches are correlated and do not have probability exactly $1/2$, so the distances of unrelated keypoints spread more widely than the binomial; Section 3.3 of Calonder et al. shows measured distributions.

**Theorem.** BRIEF returns $f(k)$ for each keypoint whose patch is inside the image, and HAMMING returns the Hamming distance. The descriptor does not change under $I \mapsto a I + b$ with $a > 0$, and it moves with the keypoints under a shift by whole pixels.

*Proof.* Lemmas 1 to 4. $\square$
