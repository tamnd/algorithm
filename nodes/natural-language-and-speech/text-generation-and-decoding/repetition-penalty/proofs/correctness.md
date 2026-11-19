---
title: What the scaled and the additive repetition penalties do to the next-token distribution
proves: [correctness]
status: full
---

We use the notation of the page. The logits are $z_1, \ldots, z_n$, the softmax is $p_j = e^{z_j} / \sum_i e^{z_i}$, the history is a list of tokens, $c_j$ is the number of times token $j$ occurs in it, and $S = \{j : c_j > 0\}$ is the set of seen tokens. The three forms are:

- division (CTRL as written): $z'_j = z_j / \theta$ for $j \in S$;
- sign-aware scaling: $z'_j = z_j / \theta$ if $z_j > 0$ and $z'_j = z_j \theta$ otherwise, for $j \in S$;
- additive: $z'_j = z_j - c_j \alpha_f - [c_j > 0] \alpha_p$ for all $j$.

Unseen logits do not change. Let $q$ be the softmax of $z'$.

**Lemma 1 (no change at the neutral settings).** With $\theta = 1$, or with $\alpha_f = \alpha_p = 0$, or with an empty history, $z' = z$.

*Proof.* Each formula reduces to $z'_j = z_j$. $\square$

**Lemma 2 (division can reward a repeated token).** Let $\theta > 1$, $S = \{j\}$ and $z_j < 0$. Then $q_j > p_j$.

*Proof.* $z_j / \theta > z_j$ when $z_j < 0$ and $\theta > 1$. Raising one logit while the others stay fixed raises its probability, since $p_j = 1 / (1 + \sum_{i \ne j} e^{z_i - z_j})$ grows with $z_j$. $\square$

For the logits $(2, -1, 0)$ and the history $\{1\}$, division by $\theta = 2$ raises the probability of token 1 from 0.0420 to 0.0674, while the sign-aware form lowers it to 0.0159.

**Lemma 3 (the sign-aware form).** Let $\theta \ge 1$. Then (a) $z'_j \le z_j$ for every $j \in S$; (b) $q_i \ge p_i$ for every unseen token $i$; (c) if $S = \{j\}$, then $q_j \le p_j$.

*Proof.* (a) For $z_j > 0$, $z_j / \theta \le z_j$; for $z_j \le 0$, $z_j \theta \le z_j$. (b) The numerator $e^{z_i}$ of an unseen token is unchanged, and by (a) the denominator does not grow. (c) Only $z_j$ changes, and it does not go up, so $p_j$ does not go up, as in the proof of Lemma 2. $\square$

Part (c) needs a single seen token. With two or more, a seen token can gain probability, because the other seen tokens can lose more. For the logits $(4, 0.5, 0)$, the history $\{0, 1\}$ and $\theta = 2$, the new logits are $(2, 0.25, 0)$, and the probability of token 1 rises from 0.0288 to 0.1327.

**Lemma 4 (the additive form changes the odds by a fixed factor).** For any two tokens $i$ and $j$,

$$\log \frac{q_j}{q_i} = \log \frac{p_j}{p_i} - (c_j \alpha_f + [c_j > 0] \alpha_p) + (c_i \alpha_f + [c_i > 0] \alpha_p).$$

*Proof.* $\log (q_j / q_i) = z'_j - z'_i$, and $z_j - z_i = \log (p_j / p_i)$. $\square$

So with $\alpha_f, \alpha_p \ge 0$, every occurrence of $j$ in the history multiplies its odds against an unseen token by $e^{-\alpha_f}$, and its first occurrence by a further $e^{-\alpha_p}$, whatever the logits are.

**Lemma 5 (shifts).** Adding a constant $a$ to every logit does not change $q$ under the additive form. It can change $q$ under both scaling forms.

*Proof.* Under the additive form every $z'_j$ also moves by $a$, and the softmax ignores a common shift. For the scaling forms, take the logits $(2, 1, 0)$ and $(-1, -2, -3)$, which give the same $p$, the history $\{0\}$ and $\theta = 1.5$. The first gives $z'_0 = 4/3$ and $q_0 = 0.5050$; the second gives $z'_0 = -1.5$ and $q_0 = 0.5465$. $\square$

The logits of a model are defined only up to such a shift, so the strength of a scaling penalty depends on an arbitrary choice of the network, while the additive penalty does not. The tests check Lemmas 1 to 5 on random logits and on the examples above.
