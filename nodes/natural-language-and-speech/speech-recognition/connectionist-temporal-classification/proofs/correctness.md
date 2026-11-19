---
title: The CTC forward-backward pass computes p(l | x) and the gradient of the loss
proves: [correctness]
status: full
---

We use the notation of the page, with frames $t = 1, \ldots, T$ and states $s = 1, \ldots, S$ (the code counts both from 0). The blank is $\varnothing$. The label sequence is $l = l_1 \ldots l_U$ with no blank in it, and the extended sequence is $l' = \varnothing\, l_1\, \varnothing\, l_2 \ldots l_U\, \varnothing$, so $S = 2U + 1$, $l'_s = \varnothing$ for odd $s$ and $l'_{2j} = l_j$. The output of frame $t$ is $y_t = \mathrm{softmax}(u_t)$. The proofs work with probabilities; the code stores their natural logs, and $\oplus$ (log_add) in log space is $+$ on probabilities, so the same statements hold for the stored values.

A *path* is a sequence $\pi = \pi_1 \ldots \pi_T$ of symbols, with probability $\prod_t y_t(\pi_t)$. The map $\mathcal{B}$ merges each run of equal symbols into one symbol and then deletes the blanks. By definition $p(l \mid x) = \sum_{\pi : \mathcal{B}(\pi) = l} \prod_t y_t(\pi_t)$.

## Paths and state sequences

Call a state $s$ *skippable to* if $s \ge 3$, $l'_s \neq \varnothing$ and $l'_s \neq l'_{s-2}$. An *admissible state sequence* is $\sigma = \sigma_1 \ldots \sigma_T$ with $\sigma_1 \in \{1, 2\}$, $\sigma_T \in \{S-1, S\}$ (only $\{1\}$ at both ends when $S = 1$), and each step $\sigma_t - \sigma_{t-1}$ equal to 0 or 1, or equal to 2 when $\sigma_t$ is skippable to.

**Lemma 1.** The map $\sigma \mapsto \pi$ with $\pi_t = l'_{\sigma_t}$ is a bijection from the admissible state sequences onto the paths $\pi$ with $\mathcal{B}(\pi) = l$.

*Proof.* Take an admissible $\sigma$ and set $\pi_t = l'_{\sigma_t}$. A step of 2 always lands on an even state $s$ and skips the odd state $s - 1$, so no even state is skipped. Since $\sigma$ starts at 1 or 2 and ends at $S - 1$ or $S$, it visits each even state $2, 4, \ldots, 2U$, each on a block of consecutive frames, in this order. The path $\pi$ is a run of $l_1$, a run of $l_2$, and so on, with blank runs between some of them. Two label runs with no blank run between them come from a step of 2, so their symbols differ, and the runs do not merge. So $\mathcal{B}$ maps each label run to one symbol, deletes the blank runs, and gives $l$.

Conversely, take $\pi$ with $\mathcal{B}(\pi) = l$ and cut it into maximal runs of equal symbols. Merging gives one symbol per run, and deleting the blank runs leaves $l$, so the non-blank runs are, in order, runs of $l_1, \ldots, l_U$. Map the frames of the $j$-th label run to state $2j$, the frames of a blank run between label runs $j$ and $j+1$ to state $2j + 1$, a leading blank run to state 1 and a trailing blank run to state $2U + 1$. The result is admissible: the steps inside a run are 0, a step into or out of a blank run is 1, and two adjacent label runs $j$ and $j + 1$ give a step of 2, where $l_{j+1} \neq l_j$ because two adjacent maximal runs hold different symbols. This construction is the inverse of the first map, because the state of each frame is fixed by the run that holds the frame. $\square$

So $p(l \mid x) = \sum_\sigma \prod_t y_t(l'_{\sigma_t})$, summed over the admissible state sequences. In particular, a path exists if and only if an admissible $\sigma$ exists, which needs one frame for each label and one more frame for each blank state between two equal labels, that is $T \ge U + r$, where $r$ is the number of indices $j$ with $l_j = l_{j+1}$.

## The forward and backward variables

**Lemma 2 (forward).** After lines L2 to L5, $\alpha_t(s)$ equals the sum, over the prefixes $\sigma_1 \ldots \sigma_t$ that satisfy the start rule and the step rule and end with $\sigma_t = s$, of $\prod_{\tau = 1}^{t} y_\tau(l'_{\sigma_\tau})$.

*Proof.* By induction on $t$. For $t = 1$ the prefixes are $\sigma_1 = 1$ and $\sigma_1 = 2$, which line L2 sets, and every other state gets 0. For $t > 1$, the last step of a prefix that ends in $s$ comes from $s$, from $s - 1$, or from $s - 2$ when $s$ is skippable to. These sets of prefixes are disjoint, and every prefix of each set is the extension of a prefix that ends at frame $t - 1$. The weight is a product, so the sum factors as $(\alpha_{t-1}(s) + \alpha_{t-1}(s-1) + [\text{$s$ skippable to}]\,\alpha_{t-1}(s-2))\, y_t(l'_s)$, which is lines L4 and L5. $\square$

**Lemma 3 (backward).** After line L7 and its loop, $\beta_t(s)$ equals the sum, over the suffixes $\sigma_{t+1} \ldots \sigma_T$ such that $\sigma_t = s$ followed by the suffix satisfies the step rule and ends in $\{S-1, S\}$, of $\prod_{\tau = t+1}^{T} y_\tau(l'_{\sigma_\tau})$. The factor $y_t$ is not included.

*Proof.* By induction on $t$ downward. For $t = T$ the suffix is empty, its product is 1, and it is valid exactly when $s \in \{S - 1, S\}$, which line L7 sets. For $t < T$, split by $\sigma_{t+1} \in \{s, s+1, s+2\}$, where $s + 2$ is allowed only when it is skippable to. This gives $\beta_t(s) = \sum_{s'} y_{t+1}(l'_{s'})\, \beta_{t+1}(s')$ over the allowed $s'$, which is the code. $\square$

**Theorem 1.** $p(l \mid x) = \alpha_T(S) + \alpha_T(S-1)$ (only $\alpha_T(1)$ when $S = 1$), so line L6 gives $\log p(l \mid x)$. Moreover, for every frame $t$ and state $s$, $\alpha_t(s)\beta_t(s)$ is the total probability of the paths of $l$ that are in state $s$ at frame $t$, and $\sum_s \alpha_t(s) \beta_t(s) = p(l \mid x)$.

*Proof.* The first claim is Lemma 2 at $t = T$ with the end rule, and Lemma 1. For the second, an admissible $\sigma$ with $\sigma_t = s$ is a valid prefix ending in $s$ followed by a valid suffix from $s$, and every such pair gives an admissible $\sigma$. The product over frames splits into the prefix part, which includes $y_t$, and the suffix part, which does not, so the sum is $\alpha_t(s)\beta_t(s)$. Each admissible $\sigma$ is in exactly one state at frame $t$, so summing over $s$ gives $p$. $\square$

## The gradient

**Theorem 2.** Let $\gamma_t(k) = \sum_{s : l'_s = k} \alpha_t(s)\beta_t(s)$. Then
$$\frac{\partial(-\ln p(l \mid x))}{\partial u_t(k)} = y_t(k) - \frac{\gamma_t(k)}{p(l \mid x)},$$
which is line L8. The log is the natural log.

*Proof.* By Theorem 1 and Lemma 1, $\gamma_t(k)$ is the sum of $\prod_\tau y_\tau(\pi_\tau)$ over the paths of $l$ with $\pi_t = k$. Each such product holds the factor $y_t(k)$ exactly once, and the products of the other paths of $l$ do not depend on $y_t(k)$. Treating the $y_t(j)$ as free variables, $\partial p / \partial y_t(j) = \gamma_t(j) / y_t(j)$. The softmax gives $\partial y_t(j) / \partial u_t(k) = y_t(j)(\delta_{jk} - y_t(k))$, and $u_t$ affects no other frame. By the chain rule,
$$\frac{\partial \ln p}{\partial u_t(k)} = \sum_j \frac{\gamma_t(j)}{p\, y_t(j)}\, y_t(j)\big(\delta_{jk} - y_t(k)\big) = \frac{\gamma_t(k)}{p} - y_t(k) \frac{\sum_j \gamma_t(j)}{p} = \frac{\gamma_t(k)}{p} - y_t(k),$$
because $\sum_j \gamma_t(j) = \sum_s \alpha_t(s)\beta_t(s) = p$ by Theorem 1. Change the sign. $\square$

**Remark (the convention of Graves et al. 2006).** Their backward variable $\hat\beta_t(s)$ includes the factor $y_t(l'_s)$, so $\hat\alpha_t(s)\hat\beta_t(s) = \alpha_t(s)\beta_t(s)\, y_t(l'_s)$. Their eq. (16) therefore reads $y_t(k) - \frac{1}{y_t(k) Z_t} \sum_{s : l'_s = k} \hat\alpha_t(s)\hat\beta_t(s)$ with $Z_t = \sum_s \hat\alpha_t(s)\hat\beta_t(s) / y_t(l'_s) = p$. It is the same quantity as Theorem 2.

**Corollary.** For each frame, $\sum_k \partial(-\ln p)/\partial u_t(k) = 1 - \sum_k \gamma_t(k)/p = 0$. The tests check this, and they check Theorem 2 against central finite differences of the loss.

## Log space and rounding

The code stores $\ln \alpha$ and $\ln \beta$ and adds probabilities with log_add, which computes $\max(a, b) + \ln(1 + e^{-|a - b|})$. No exponential of a large number is formed, and every stored value is a log of a sum of path probabilities, which is at least the log of one path probability. If each output satisfies $y_t(k) \ge e^{-c}$, a stored value is at least $-cT$, so for any realistic $T$ it is far inside the range of a double, while the product of the probabilities itself would underflow. We do not give a bound on the rounding error of the log-space sums. The tests compare the code with exact enumeration and with exact path counts.
