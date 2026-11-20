---
title: Reranking and the stopping bound of length normalized beam search
proves: [correctness]
status: full
---

We use the notation of the page. A model gives $\log p(w \mid y) \le 0$ for every prefix $y$ and token $w$, the score of a sequence is the sum of these terms, and a penalty lp maps a length $m \ge 1$ to a number $\text{lp}(m) > 0$. We assume exact arithmetic.

**Lemma 1 (raw scores only go down).** If $y'$ extends $y$, then $\log p(y') \le \log p(y)$.

*Proof.* $\log p(y')$ is $\log p(y)$ plus one term $\log p(w \mid \cdot) \le 0$ per added token. $\square$

So among outputs whose tokens all have the same probability $\pi < 1$, the raw score $|Y| \log \pi$ is largest for the shortest output. This is the bias that the technique corrects.

**Theorem 2 (RERANK).** RERANK returns a pair $(Y, v)$ with $v = \log p(Y) / \text{lp}(|Y|)$ maximal over the input list, and $Y$ is the first hypothesis in the list that attains it.

*Proof.* After the pass of line L2 for the $i$-th hypothesis, best holds the first of the hypotheses $1 \ldots i$ with the largest normalized score, and that score. This holds after the first pass, where line L4 sets best because it is none. Line L3 computes the normalized score, and line L4 replaces best only on a strict increase, so an equal later score keeps the earlier hypothesis. After the last pass, line L5 returns it. $\square$

**Lemma 3 (the bound).** Let lp be non-decreasing. Let $y$ be an open hypothesis of length $m$ with raw score $s \le 0$, and let $Y$ be a finished extension of $y$ with $|Y| \le n_{\max}$. Then $\log p(Y) / \text{lp}(|Y|) \le s / \text{lp}(n_{\max})$.

*Proof.* By Lemma 1, $\log p(Y) \le s \le 0$. Since $\text{lp}(|Y|) \le \text{lp}(n_{\max})$ and both are positive, $1 / \text{lp}(|Y|) \ge 1 / \text{lp}(n_{\max})$, and multiplying by the non-positive number $\log p(Y)$ reverses the order: $\log p(Y) / \text{lp}(|Y|) \le \log p(Y) / \text{lp}(n_{\max}) \le s / \text{lp}(n_{\max})$. $\square$

Both the power penalty with $\alpha \ge 0$ and the GNMT penalty with $\alpha \ge 0$ are positive and non-decreasing, so the lemma applies to them.

**Theorem 4 (an unbounded beam is exact).** Let the beam width be at least the number of open hypotheses at every step, and let lp be positive and non-decreasing. Then the beam search of the code returns a finished output $Y$ with $|Y| \le n_{\max}$ that maximizes $\log p(Y) / \text{lp}(|Y|)$ over all such outputs of positive probability.

*Proof.* With an unbounded width, no open hypothesis is ever dropped by the width, so every prefix of positive probability is expanded until it either ends with `</s>`, where it is scored by its normalized score and compared with the best so far, or reaches the length limit. The only other way to drop hypotheses is the early stop. The search stops early only when every open hypothesis $y$ satisfies $s(y) / \text{lp}(n_{\max}) \le$ the best normalized score found so far. By Lemma 3, no finished extension of any open hypothesis can then beat the best found, so stopping loses no better output. Hence the best normalized score over all finished outputs is found. $\square$

With a bounded width the beam drops hypotheses, and the result is only a heuristic, as for plain beam search.

**Lemma 5 (normalized scores are not monotone).** With the power penalty and $\alpha = 1$, the normalized score of a prefix can increase when a token is added.

*Proof.* A prefix of one token with $\log p = -1$ has normalized score $-1$. Add a token of probability $0.9$: the new score is $(-1 + \log 0.9) / 2 \approx -0.553 > -1$. $\square$

So the normalized score of an open hypothesis is not an upper bound on the normalized scores of its extensions, and Lemma 3 uses the raw score instead.

**Word reward.** For two outputs of lengths $m_1 < m_2$ and log probabilities $s_1 > s_2$, the score $s + r m$ prefers the longer one exactly when $r > (s_1 - s_2) / (m_2 - m_1)$. For the example of the page, $(-2.0 + 3.2) / (8 - 3) = 0.24$.
