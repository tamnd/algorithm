---
title: The RankBoost ranking loss is at most the product of the normalizers, and each normalizer is at most the square root of 1 minus r squared
proves: [correctness]
status: full
---

The input is a list of $N$ crucial pairs $(x_0, x_1)$, each saying that $x_1$ must rank above $x_0$, and a distribution $D_1$ over them; the code uses the uniform $D_1$. Round $t$ picks a weak ranker $h_t : X \to [0, 1]$ and a real $\alpha_t$, and sets

$$D_{t+1}(x_0, x_1) = \frac{D_t(x_0, x_1)\, e^{\alpha_t (h_t(x_0) - h_t(x_1))}}{Z_t}, \qquad Z_t = \sum_{(x_0, x_1)} D_t(x_0, x_1)\, e^{\alpha_t (h_t(x_0) - h_t(x_1))}.$$

The final ranker is $H = \sum_{t \le T} \alpha_t h_t$, and its ranking loss is $\mathrm{rloss}(H) = \sum D_1(x_0, x_1)\, [H(x_0) \ge H(x_1)]$, so a tie counts as an error. This is the RankBoost of Freund et al. (2003), Figure 1.

**Theorem 1 (the bound).** $\mathrm{rloss}(H) \le \prod_{t=1}^{T} Z_t$.

*Proof.* Unroll the update. By induction on $T$,

$$D_{T+1}(x_0, x_1) = \frac{D_1(x_0, x_1)\, e^{H(x_0) - H(x_1)}}{\prod_{t \le T} Z_t}.$$

$D_{T+1}$ sums to 1, so $\prod_t Z_t = \sum D_1(x_0, x_1)\, e^{H(x_0) - H(x_1)}$. Each term is at least $D_1(x_0, x_1)\, [H(x_0) \ge H(x_1)]$, because $e^u \ge 1$ for $u \ge 0$ and $e^u > 0$ always. $\square$

The same argument holds for every prefix $H_T = \sum_{t \le T} \alpha_t h_t$, so the bound holds after each round. It is the theorem of Freund et al. (2003), Section 3.

**Lemma 2 (method 3).** Let $h$ take values in $[0, 1]$ and let $r = \sum D(x_0, x_1)(h(x_1) - h(x_0))$, so $|r| \le 1$. For every $\alpha$,

$$Z(\alpha) \le \frac{1 - r}{2} e^{\alpha} + \frac{1 + r}{2} e^{-\alpha},$$

and for $|r| < 1$ the right side is smallest at $\alpha = \frac{1}{2} \ln \frac{1 + r}{1 - r}$, where it equals $\sqrt{1 - r^2}$. So with this $\alpha$, $Z \le \sqrt{1 - r^2}$.

*Proof.* Put $u = h(x_0) - h(x_1) \in [-1, 1]$. By convexity of $u \mapsto e^{\alpha u}$, $e^{\alpha u} \le \frac{1 + u}{2} e^{\alpha} + \frac{1 - u}{2} e^{-\alpha}$. Take the $D$-weighted sum and use $\sum D u = -r$. The right side $a e^{\alpha} + b e^{-\alpha}$ with $a = (1 - r)/2$ and $b = (1 + r)/2$ is smallest at $e^{2\alpha} = b/a$, with the value $2\sqrt{ab} = \sqrt{1 - r^2}$. $\square$

Line L4 of the code uses this $\alpha$, and line L5 computes $Z$ exactly. Since $\sqrt{1 - r^2} \le e^{-r^2/2}$, Theorem 1 gives $\mathrm{rloss}(H) \le \exp(-\frac{1}{2} \sum_t r_t^2)$: if every round has $|r_t| \ge \gamma > 0$, the ranking loss on the training pairs falls at least as fast as $e^{-\gamma^2 T / 2}$.

**Lemma 3 (method 2 for $\{0, 1\}$ rankers).** For $h$ with values in $\{0, 1\}$, let $W_b = \sum D(x_0, x_1)\, [h(x_0) - h(x_1) = b]$ for $b \in \{-1, 0, 1\}$. Then $Z(\alpha) = W_{-1} e^{-\alpha} + W_0 + W_{1} e^{\alpha}$, and when $W_{-1}, W_1 > 0$ its minimum is at $\alpha = \frac{1}{2} \ln (W_{-1} / W_1)$, with the value $W_0 + 2\sqrt{W_{-1} W_1}$. Also $r = W_{-1} - W_1$.

*Proof.* The value of $e^{\alpha u}$ depends only on $u \in \{-1, 0, 1\}$; group the pairs by $u$. The minimum of $a e^{-\alpha} + b e^{\alpha}$ is $2\sqrt{ab}$ at $e^{2\alpha} = a/b$. For $r$, $h(x_1) - h(x_0) = -u$. $\square$

Method 2 gives the exact minimum of $Z$ for a $\{0, 1\}$ ranker, and method 3 a bound on it. The code uses method 3, with $\alpha$ from $r$, as do the experiments of the paper. For the same ranker, method 2 can give a smaller $Z$ than method 3, since $W_0 + 2\sqrt{W_{-1} W_1} \le \sqrt{1 - r^2}$ always.

**Lemma 4 (the weak learner).** Line L3 returns a threshold ranker $h(x) = [x_f > \theta]$ with the largest $|r|$ over all features $f$ and all real $\theta$.

*Proof.* For a fixed $f$, $h$ depends on $\theta$ only through the set of values of $x_f$ above $\theta$. Below the smallest value or at or above the largest, $h$ is constant and $r = 0$. Between two consecutive distinct values, every $\theta$ gives the same $h$, and the code tries the midpoint of each such interval. So it tries every distinct nonconstant threshold ranker, and keeps the one of largest $|r|$. $\square$

Maximizing $|r|$ minimizes the bound $\sqrt{1 - r^2}$ of Lemma 2, which is the choice of Freund et al. (2003), Section 4. A negative $r$ gives a negative $\alpha$, which reverses the ranker.

**Remark (clipping).** If $|r| = 1$, the chosen ranker orders every pair of positive weight the right way (or every pair the wrong way), and $\alpha$ would be infinite. The code clips $|r|$ to $1 - 10^{-10}$, which gives $\alpha \approx 11.9$ and $Z \le \sqrt{1 - r^2} \approx 1.4 \cdot 10^{-5}$. Theorem 1 does not depend on how $\alpha$ is chosen, so it still holds.

**What is not proved.** Theorem 1 bounds the loss on the training pairs. The paper also studies generalization under assumptions on how the data are drawn; that analysis is not used here, and the quality on new queries is a matter of measurement.

The tests in `impl/python/test_rankboost.py` check the choice of each weak ranker against a brute force over all features and all observed values, the formula for $\alpha$, $Z_t$ against a direct sum and against $\sqrt{1 - r_t^2}$, $r = W_{-1} - W_1$, Theorem 1 after every round on random data, Lemma 3 by a grid search over $\alpha$, the clipping, the rule that ties are errors, and the worked example of the page.
