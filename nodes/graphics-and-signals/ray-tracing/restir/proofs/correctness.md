---
title: Unbiased contribution weights in ReSTIR, and the bias of the 1/M weighting
proves: [correctness]
status: full
---

**Setting.** The lights form a finite set $\mathcal Y$ (for an area light, replace each sum over $\mathcal Y$ by an integral). Pixel $q$ has the integrand $f_q(y) = \hat p_q(y) V_q(y) \ge 0$, where $\hat p_q \ge 0$ is the target and $V_q \in \{0, 1\}$ is the visibility, and the value $I_q = \sum_y f_q(y)$. The source density $p$ is positive on every light with $\hat p_q(y) > 0$. Write $S_q = \{y : \hat p_q(y) V_q(y) > 0\}$.

**Definition.** A random pair $(y, W)$, with $W = 0$ when $y$ is empty, is an *unbiased contribution weight* (UCW) for a set $S$ if $E[g(y) W] = \sum_{y \in S} g(y)$ for every function $g$ on $\mathcal Y$. Then $E[f_q(y) W] = I_q$ for a UCW for any $S \supseteq S_q$ whose extra lights have $f_q = 0$, in particular for $S = S_q$.

**Lemma 1 (the reservoir).** After UPDATE with the weights $w_1, \dots, w_n \ge 0$ and $w = \sum_i w_i > 0$, the reservoir holds item $i$ with probability $w_i / w$.

*Proof.* By induction on $n$. Item $n$ is taken with probability $w_n / \sum_{l \le n} w_l$. An earlier item $i$ is held after step $n - 1$ with probability $w_i / \sum_{l < n} w_l$ and survives step $n$ with probability $\sum_{l < n} w_l / \sum_{l \le n} w_l$; the product is $w_i / \sum_{l \le n} w_l$. $\square$

**Lemma 2 (RIS, lines L2 and L3).** Let $x_1, \dots, x_M$ be independent with density $p$, $w_i = \hat p_q(x_i) / p(x_i)$, $y$ chosen by Lemma 1, and $W = \frac{1}{M \hat p_q(y)} \sum_i w_i$. Then $(y, W)$ is a UCW for $\{\hat p_q > 0\}$.

*Proof.* Given the candidates, Lemma 1 gives

$$E[g(y) W \mid x_1, \dots, x_M] = \sum_{i : w_i > 0} \frac{w_i}{\sum_l w_l}\, g(x_i)\, \frac{\sum_l w_l}{M \hat p_q(x_i)} = \frac1M \sum_{i : \hat p_q(x_i) > 0} \frac{g(x_i)}{p(x_i)},$$

also when all $w_i$ are $0$. Each term has the mean $\sum_{y : \hat p_q(y) > 0} g(y)$, because $p > 0$ there. $\square$

**Lemma 3 (visibility, line L4 and the end of L12).** If $(y, W)$ is a UCW for $S$, then $(y, W V_q(y))$ is a UCW for $S \cap \{V_q = 1\}$.

*Proof.* Apply the definition to the function $g V_q$. $\square$

**Lemma 4 (COMBINE).** Let $(y_i, W_i)$ for $i = 1, \dots, m$ be UCWs for the sets $S_{o_i}$ of the pixels $o_i$, with any dependence between them and with $W_i = 0$ whenever $y_i \notin S_{o_i}$, and let $M_1, \dots, M_m > 0$ be constants. Let $h_i(y) = \hat p_{o_i}(y) V_{o_i}(y)$, so that $S_{o_i} = \{h_i > 0\}$. COMBINE at pixel $q$ takes $y = y_r$ with probability $w_r / \sum_i w_i$, where $w_i = \hat p_q(y_i) W_i M_i$. With the weighting of line L11,

$$W = \frac{\sum_i w_i}{Z(y)\, \hat p_q(y)}, \qquad Z(y) = \sum_{i : h_i(y) > 0} M_i,$$

and with the balance heuristic,

$$W = \frac{h_r(y)}{H(y)} \cdot \frac{\sum_i w_i}{\hat p_q(y)}, \qquad H(y) = \sum_i M_i h_i(y).$$

In both cases $(y, W)$ is a UCW for $\big(\bigcup_i S_{o_i}\big) \cap \{\hat p_q > 0\}$.

*Proof.* Write $\mu_r(y) = M_r / Z(y)$ for the first weighting and $\mu_r(y) = M_r h_r(y) / H(y)$ for the second. For each $y$ in $\bigcup_i S_{o_i}$, the sum of $\mu_r(y)$ over the $r$ with $y \in S_{o_r}$ is $1$; this is the statement that the MIS weights sum to one. In both cases the value $W$ for the choice $r$ is $\mu_r(y_r)\, \frac{\sum_i w_i}{M_r \hat p_q(y_r)}$. Given the inputs,

$$E[g(y) W \mid \text{inputs}] = \sum_{r : w_r > 0} \frac{w_r}{\sum_i w_i}\, g(y_r)\, \mu_r(y_r) \frac{\sum_i w_i}{M_r \hat p_q(y_r)} = \sum_r g(y_r)\, \mu_r(y_r)\, \mathbf 1[\hat p_q(y_r) > 0]\, W_r.$$

Term $r$ is $G_r(y_r) W_r$ for the fixed function $G_r = g\, \mu_r\, \mathbf 1[\hat p_q > 0]$, so its mean is $\sum_{y \in S_{o_r}} G_r(y)$ because $(y_r, W_r)$ is a UCW. Only linearity of the expected value is used, so the inputs may depend on each other. Summing over $r$ and exchanging the sums,

$$E[g(y) W] = \sum_{y : \hat p_q(y) > 0} g(y) \sum_{r : y \in S_{o_r}} \mu_r(y) = \sum_{y \in (\bigcup_r S_{o_r}) \cap \{\hat p_q > 0\}} g(y). \qquad \square$$

**Lemma 5 (the 1/M weighting is biased).** With $W = \sum_i w_i / (\sum_i M_i \cdot \hat p_q(y))$ in place of $Z(y)$, the same computation with $\mu_r = M_r / \sum_i M_i$ gives

$$E[g(y) W] = \sum_{y : \hat p_q(y) > 0} g(y)\, c(y), \qquad c(y) = \frac{\sum_{r : y \in S_{o_r}} M_r}{\sum_i M_i} \le 1.$$

So $E[f_q(y) W] = \sum_y f_q(y) c(y) \le I_q$, with equality only if every light that pixel $q$ sees is in every $S_{o_r}$. The image is too dark where the combined pixels see different lights. In the table scene of the tests, light 0 is seen by pixel 0 but not by pixel 1, $M = (2, 1)$, so $c(0) = \tfrac23$ and the mean is $\tfrac23 \cdot 1 + 2 = \tfrac83$ in place of $3$. $\square$

**Claim.** In every frame, each reservoir $R_q$ after line L5 and each reservoir $S_q$ after line L7 is a UCW for $S_q$. So the value $f_q(S_q.y)\, S_q.W$ of line L8 has the mean $I_q$, in every frame and for both unbiased weightings.

**Proof.** By induction over the steps of the frames. The counts $M$ are fixed numbers: $M$ candidates, and sums and minimums of fixed numbers. The neighbors are chosen independently of the reservoirs, so the proof holds given the choice.

- Line L3 gives a UCW for $\{\hat p_q > 0\}$ by Lemma 2, and line L4 makes it a UCW for $S_q$ by Lemma 3.
- Line L5 combines this with the stored $S_q$ of the last frame, a UCW for $S_q$ by the induction hypothesis; capping its $M$ only changes a constant. By Lemma 4 the result is a UCW for $S_q \cap \{\hat p_q > 0\} = S_q$, and Lemma 3 at the end of line L12 keeps it.
- Line L7 combines $R_q$ with the $R_n$ of neighbors, UCWs for $S_q$ and the $S_n$. By Lemma 4 the result is a UCW for $(S_q \cup \bigcup_n S_n) \cap \{\hat p_q > 0\}$, and Lemma 3 cuts this to $S_q$.

The last step is why line L12 sets $W = 0$ when $q$ cannot see $y$: then the support of every stored reservoir is exactly $S_q$, which is what the tests $h_i(y) > 0$ in the next COMBINE assume. $\square$

**Remark.** The proof needs $\hat p_q > 0$ wherever $f_q > 0$. A target with a zero where $f_q > 0$ loses those lights; the tests check the exact loss for one such target.
