---
title: The split gains of a phonetic decision tree are exact and never negative
proves: [correctness]
status: full
---

We use the notation of the page. A pool is the set of triphone states of one base phone and one state position. Each state $s$ has an occupancy $N_s > 0$, a mean $\mu_s \in \mathbb{R}^d$ and a diagonal variance $\sigma^2_s \in \mathbb{R}^d$, computed from the frames $F_s$ that are assigned to it: $N_s = |F_s|$, $\mu_{sk} = \frac{1}{N_s} \sum_{o \in F_s} o_k$ and $\sigma^2_{sk} = \frac{1}{N_s} \sum_{o \in F_s} (o_k - \mu_{sk})^2$. All logs are natural logs. We prove the statements for these hard assignments. With soft occupancies the same algebra holds for the weighted sums, and $L(S)$ is then the auxiliary function of EM with the state posteriors held fixed, which is the approximation that Young, Odell and Woodland make.

**Lemma 1 (pooled statistics).** For a set $S$ of states with the frames $F(S) = \bigcup_{s \in S} F_s$, the statistics of $F(S)$ are

$$N(S) = \sum_{s \in S} N_s, \qquad \mu_k(S) = \frac{1}{N(S)} \sum_{s \in S} N_s \mu_{sk}, \qquad \sigma^2_k(S) = \frac{1}{N(S)} \sum_{s \in S} N_s (\sigma^2_{sk} + \mu_{sk}^2) - \mu_k(S)^2.$$

*Proof.* The frame sets are disjoint. The sum of $o_k$ over $F_s$ is $N_s \mu_{sk}$, and the sum of $o_k^2$ over $F_s$ is $N_s(\sigma^2_{sk} + \mu^2_{sk})$, because the variance is the mean square minus the square of the mean. Add over $s$, divide by $N(S)$, and use the same identity for $F(S)$. $\square$

**Lemma 2 (closed form of $L$).** Let $L(S)$ be the largest log likelihood of the frames $F(S)$ under one Gaussian with a diagonal covariance. If every $\sigma^2_k(S) > 0$, then

$$L(S) = -\tfrac{1}{2} N(S) \Big( d \log(2\pi) + \sum_{k=1}^{d} \log \sigma^2_k(S) + d \Big).$$

*Proof.* With a diagonal covariance, the log density is a sum over the dimensions, so the log likelihood is $\sum_k \ell_k(m_k, v_k)$ with $\ell_k = -\frac{1}{2} \sum_{o \in F(S)} \big( \log(2\pi v_k) + (o_k - m_k)^2 / v_k \big)$. Each $\ell_k$ is maximized at the sample mean $m_k = \mu_k(S)$ and the sample variance $v_k = \sigma^2_k(S)$ (the usual maximum likelihood estimate; see maximum-likelihood-estimation). At this point $\sum_{o} (o_k - m_k)^2 / v_k = N(S)$, which gives the formula. $\square$

By Lemmas 1 and 2, $L(S)$ needs only $N_s$, $\mu_s$ and $\sigma^2_s$ of the states in $S$, not the frames. The code computes it in $O(|S| d)$ time.

**Theorem 1 (gains are never negative).** For every set $S$ and every split of $S$ into non-empty parts $S_y$ and $S_n$, the gain $\Delta = L(S_y) + L(S_n) - L(S)$ is at least 0.

*Proof.* Let $g$ be the Gaussian that attains $L(S)$. The log likelihood of $F(S)$ under $g$ is the sum of the log likelihoods of $F(S_y)$ and of $F(S_n)$ under $g$. Each part is at most the largest log likelihood of that part, which is $L(S_y)$ or $L(S_n)$. $\square$

**Theorem 2 (what the greedy tree computes).** Let BUILD-TREE run with a threshold $\theta$ and a minimum occupancy $m$, and without a limit on the number of leaves. Then:

1. For each leaf that it splits, the question is one with the largest gain among the allowed questions of that leaf (both sides with occupancy at least $m$).
2. A leaf is split if and only if its largest allowed gain is at least $\theta$. So the final tree does not depend on the order in which the leaves are taken.
3. The leaves partition the pool, and $\sum_{\text{leaves } S} L(S) = L(\text{pool}) + \sum_{\text{splits}} \Delta$.
4. Every context $(l, r)$, seen in training or not, reaches exactly one leaf.

*Proof.* (1) Line L3 computes the gain of every allowed question of a leaf by Lemmas 1 and 2, and keeps the largest. (2) The best allowed split of a leaf depends only on the states of the leaf. Lines L4 and L5 split some leaf whose best gain is at least $\theta$ as long as one exists, and splitting a leaf does not change the candidates of the other leaves. When the loop stops, no leaf has an allowed gain of at least $\theta$, and every split that was made had a gain of at least $\theta$ when it was made. So the set of splits is determined by the leaves alone, whatever the order. (3) Each split replaces one block $S$ of a partition by $S_y$ and $S_n$, so the sum of $L$ over the blocks grows by exactly $\Delta$. (4) A question is a test on $l$ or $r$ with the answer yes or no for every phone, so the walk from the root is defined for every context and ends at one leaf. $\square$

**Remark (no global optimum).** Theorem 2 is about the greedy procedure. It does not say that the tree has the largest likelihood among all trees with the same number of leaves. The test test_greedy_misses_an_xor_context builds a pool in which the mean depends on "the left phone is a vowel" exclusive-or "the right phone is a nasal". No single question changes the mean, so every first split has a small gain, and with a threshold above it the tree stays one leaf, although a tree of depth two has a gain more than four times as large.

**Proposition (merge stage).** Each merge of lines L8 to L11 joins the two clusters $a, b$ with the smallest loss $L(a) + L(b) - L(a \cup b) \ge 0$ (by Theorem 1), and only while this loss is below $\theta$. So the total log likelihood drops by less than $\theta$ per merge, and the number of clusters drops by one per merge, so the stage stops after fewer merges than there are leaves.
