---
title: The closed form of Stolcke gives the relative entropy caused by removing one explicit n-gram, and the pruned model with recomputed backoff weights is again a proper positive distribution after every history
proves: [correctness]
status: full
---

We use the notation of the page. The backoff model has a set $E(h)$ of explicit words for each history $h$ of length 1 to $n - 1$, and

$$p(w \mid h) = p^*(w \mid h) = \frac{c(h w) - d}{c(h)} \text{ if } w \in E(h), \qquad p(w \mid h) = \alpha(h)\, p(w \mid h') \text{ otherwise},$$

with $0 < d < 1$, $p(w) = c(w)/N$ at the empty history, and $\alpha(h) = 1$ when $E(h)$ is empty. Here $h'$ is $h$ without its first token. Every $w \in E(h)$ has $c(h w) \ge 1$. Write $S_1(h) = \sum_{v \in E(h)} p^*(v \mid h)$ and $S_2(h) = \sum_{v \in E(h)} p(v \mid h')$. The backoff weight is

$$\alpha(h) = \frac{1 - S_1(h)}{1 - S_2(h)}.$$

The model is defined only if $E(h) \ne V$ for the full model; the code raises an error otherwise.

**Theorem 1 (a proper distribution).** For every set of explicit n-grams with $E(h) \subseteq \{w : c(h w) > 0\}$ and $E(h) \ne V$, every row $p(\cdot \mid h)$ is positive on $V$ and sums to 1. In particular this holds for the full model and for every pruned model.

*Proof.* Induction on the length of $h$. At the empty history $p(w) = c(w)/N > 0$ and the sum is 1. Let $h$ be longer. If $E(h)$ is empty, the row equals the row of $h'$. Otherwise $S_1(h) = \sum_{v \in E(h)} (c(h v) - d)/c(h) \le 1 - d |E(h)| / c(h) < 1$, because $\sum_{v \in E(h)} c(h v) \le c(h)$. Since $E(h) \ne V$ there is a word outside $E(h)$, and its lower probability is positive by the induction hypothesis, so $S_2(h) < 1$. Hence $\alpha(h) > 0$. Each explicit word gets $p^*(w \mid h) \ge (1 - d)/c(h) > 0$ and each other word gets $\alpha(h) p(w \mid h') > 0$. The sum is $S_1(h) + \alpha(h)(1 - S_2(h)) = S_1(h) + 1 - S_1(h) = 1$, using that the lower row sums to 1. A pruned model has $E'(h) \subseteq E(h)$, so $E'(h) \ne V$ again. $\square$

**Lemma 2 (what one removal changes).** Remove the explicit n-gram $h w$ and recompute $\alpha(h)$. Then the rows of all histories of length at most $|h|$ do not change, except the row of $h$. If $h w$ has the top order $n$, no other row of length $n - 1$ changes either.

*Proof.* The row of a history $g$ depends on $E(g)$ and on the rows of the suffixes of $g$. Only $E(h)$ changes. A history of length at most $|h|$ other than $h$ does not have $h$ as a suffix. A history of length $n - 1$ other than $h$ has the same length as $h$, so it does not have $h$ as a suffix either. $\square$

So for a top order n-gram the relative entropy between the two joint models $p(h) p(w \mid h)$ is $p(h)$ times the relative entropy of the row of $h$. For a lower order n-gram the rows of the longer histories that back off to $h$ also change. Stolcke counts only the row of $h$, and so does the code; this is the approximation of the method.

**Theorem 3 (the closed form).** Let $p'$ be the model after removing $h w$. Then

$$\alpha'(h) = \frac{1 - S_1(h) + p^*(w \mid h)}{1 - S_2(h) + p(w \mid h')},$$

and

$$p(h) \sum_{v \in V} p(v \mid h) \ln \frac{p(v \mid h)}{p'(v \mid h)} = p(h) \left[ p^*(w \mid h) \ln \frac{p^*(w \mid h)}{\alpha'(h)\, p(w \mid h')} + \big(1 - S_1(h)\big) \ln \frac{\alpha(h)}{\alpha'(h)} \right].$$

*Proof.* The new explicit set is $E(h) \setminus \{w\}$, so the sums lose the term of $w$, which gives $\alpha'(h)$. By Lemma 2 the lower rows do not change, so $p(w \mid h')$ has the same value in both models. Split the sum over $v$ in three. For $v \in E(h)$ with $v \ne w$, $p'(v \mid h) = p^*(v \mid h) = p(v \mid h)$, and the term is 0. For $v = w$, $p(w \mid h) = p^*(w \mid h)$ and $p'(w \mid h) = \alpha'(h) p(w \mid h')$, which is the first term. For $v \notin E(h)$, $p(v \mid h) = \alpha(h) p(v \mid h')$ and $p'(v \mid h) = \alpha'(h) p(v \mid h')$, so the ratio is $\alpha(h)/\alpha'(h)$ for each such $v$, and their total weight is $\sum_{v \notin E(h)} p(v \mid h) = 1 - S_1(h)$ by Theorem 1. $\square$

Line L4 of the page computes this weight as $\alpha(h)(1 - S_2(h))$, which is the same number. The value is a relative entropy of two distributions, so it is at least 0 by Gibbs' inequality; the code clamps a float rounding error below 0 to 0.

**Theorem 4 (the threshold).** With the costs $D(g)$ computed once on the original model:

1. $\theta = 0$ prunes nothing;
2. if $\theta_1 \le \theta_2$, every n-gram pruned at $\theta_1$ is pruned at $\theta_2$;
3. if the pruned top order n-grams have pairwise different histories, the relative entropy of the pruned model is the sum of their costs. With two removed words after the same history it is not, in general.

*Proof.* (1) $D(g) \ge 0$, so $e^{D(g)} - 1 \ge 0$ is never below 0. (2) The test $e^{D(g)} - 1 < \theta$ compares a fixed number with $\theta$. (3) By Lemma 2 each removal changes only its own row, and the rows of different histories enter the relative entropy as separate terms. Two removals from the same row change $\alpha(h)$ together, and the new weight is not the one of either single removal. The test file has an example where the joint value differs from the sum by more than $10^{-6}$. $\square$

**Why the threshold is a perplexity ratio.** If text is drawn from $p$, the cross entropy of $p'$ on it is $H(p) + D(p \parallel p')$ per token, so the perplexity ratio is $\mathrm{PP}'/\mathrm{PP} = e^{D}$ and the relative increase is $e^D - 1$. The threshold $\theta$ bounds this increase for each removed n-gram alone.
