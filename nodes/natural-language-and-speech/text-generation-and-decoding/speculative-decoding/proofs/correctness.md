---
title: Speculative decoding samples exactly from the target
proves: [correctness]
status: full
---

We use the notation of the page. For a prefix $y$, $p_y = p(\cdot \mid y)$ and $q_y = q(\cdot \mid y)$ are distributions over $V$, which contains "</s>". The decoder has a length limit $n$; the target law is the law of [ancestral sampling](/ancestral-sampling/) from $p$ stopped at "</s>" or after $n$ tokens. We assume exact arithmetic and an exact uniform generator.

**Lemma 1 (one position).** Let $p$ and $q$ be distributions on $V$ and $\alpha = \sum_x \min(p(x), q(x))$. Draw $X \sim q$ and $R$ uniform on $[0, 1)$. If $R \, q(X) < p(X)$, output $X$ and call the draw accepted; otherwise output a draw from $r = \max(0, p - q) / (1 - \alpha)$. Then the output has law $p$, and the draw is accepted with probability $\alpha$.

*Proof.* $X$ is drafted only when $q(X) > 0$, and then $P(R \, q(X) < p(X)) = \min(1, p(X) / q(X))$. So $x$ is output by acceptance with probability $q(x) \min(1, p(x) / q(x)) = \min(p(x), q(x))$, and the acceptance probability is $\alpha$. If $\alpha < 1$, a rejection happens with probability $1 - \alpha$, and since $\sum_x \max(0, p(x) - q(x)) = \sum_x (p(x) - \min(p(x), q(x))) = 1 - \alpha$, the residual $r$ is a distribution. The output is $x$ with probability $\min(p(x), q(x)) + (1 - \alpha) r(x) = \min(p(x), q(x)) + \max(0, p(x) - q(x)) = p(x)$. If $\alpha = 1$ then $p = q$, no rejection happens, and the output law is $q = p$. $\square$

**The emitted stream.** Run the decoder and list the tokens it emits in order, $z_1, z_2, \ldots$. Each $z_t$ is produced by one of three mechanisms:

1. an accepted draft at line L6, or a residual draw at line L7, at some position $i$ of a step: this is one run of Lemma 1 with $p = p_{z_{<t}}$ and $q = q_{z_{<t}}$, because the draft token $x_i$ was drawn from $q$ at the prefix $y x_1 \ldots x_{i-1}$, and $x_1 \ldots x_{i-1}$ were accepted, so that prefix is $z_{<t}$;
2. the bonus draw of line L9, from $p_{z_{<t}}$ directly;
3. a residual or bonus draw at the start of a new step, which is the same as case 1 or 2 with the step's prefix $y = z_{<t}$.

Let $\mathcal{F}_{t-1}$ be everything drawn before the mechanism that produces $z_t$ starts: all earlier uniforms, drafts and residual draws. Which mechanism produces $z_t$, and with which $\gamma$, is a function of $\mathcal{F}_{t-1}$ (whether the previous position was accepted, how many drafts the step has left, how much room is left). The draws of the mechanism itself are fresh: the draft $x_i$ and the uniform $R$ at position $i$ are drawn after $\mathcal{F}_{t-1}$ is fixed. One subtle point: the drafts $x_{i+1}, \ldots, x_\gamma$ of the same step are drawn before the test at position $i$. Each $x_{j}$ is drawn from $q$ at the prefix $y x_1 \ldots x_{j-1}$, and the test at position $i$ uses only $x_i$, $R$ and the two distributions at position $i$. So drawing $x_{i+1}, \ldots, x_\gamma$ lazily, after the test at position $i$, gives the same joint law of all draws, and we may assume that order. Then $x_{i+1}$ is the fresh draft of case 1 at the next position.

**Lemma 2 (the conditional law).** For every $t$, given $\mathcal{F}_{t-1}$, the token $z_t$ has law $p_{z_{<t}}$.

*Proof.* In case 2 this is the definition of the bonus draw. In cases 1 and 3, the draft $x$ at the position has law $q_{z_{<t}}$ given $\mathcal{F}_{t-1}$, the uniform $R$ and the residual draw are independent of $\mathcal{F}_{t-1}$, and Lemma 1 applies with $p = p_{z_{<t}}$ and $q = q_{z_{<t}}$. The prefix $z_{<t}$ is a function of $\mathcal{F}_{t-1}$, so the conditional law is $p_{z_{<t}}$. $\square$

**Theorem 3 (exactness).** The output of SPECULATIVE-DECODE has the target law: for every sequence $y = y_1 \ldots y_m$ that ends with "</s>" (with no earlier "</s>") and has $m \le n$, or that has $m = n$ tokens and no "</s>", $P(\text{output} = y) = \prod_{t=1}^{m} p(y_t \mid y_{<t})$.

*Proof.* The decoder stops exactly when the emitted stream ends with "</s>" or reaches $n$ tokens: line L8 returns after an accepted "</s>" draft without a bonus, line L1 stops drafting after "</s>", and the room argument keeps every step within $n$ tokens. So the output is $z_1 \ldots z_m$ with the same stopping rule as ancestral sampling. By Lemma 2 and the tower rule, $P(z_1 = y_1, \ldots, z_m = y_m) = \prod_t p(y_t \mid y_{<t})$, by induction on $m$: the event $\{z_{<t} = y_{<t}\}$ is a union of events in $\mathcal{F}_{t-1}$, and on each of them $P(z_t = y_t \mid \mathcal{F}_{t-1}) = p(y_t \mid y_{<t})$. $\square$

**Theorem 4 (tokens per step).** Suppose that at every position the draft token is accepted with probability $\alpha$, independently of everything before it, and that no "</s>" and no length limit interrupts the step. Then a step emits $(1 - \alpha^{\gamma + 1}) / (1 - \alpha)$ tokens on average, and $\gamma + 1$ if $\alpha = 1$.

*Proof.* Let $K$ be the number of accepted drafts. Then $P(K \ge i) = \alpha^i$ for $0 \le i \le \gamma$. The step emits $K + 1$ tokens: the $K$ accepted drafts and either the residual draw (if $K < \gamma$) or the bonus draw (if $K = \gamma$). So the mean is $1 + E[K] = 1 + \sum_{i=1}^{\gamma} P(K \ge i) = \sum_{i=0}^{\gamma} \alpha^i$. $\square$

The independence assumption holds in the test model, where both models give the same rows at every prefix. It fails for real models, where $\alpha$ depends on the prefix; then Theorem 4 is a model of the speed, while Theorem 3 still holds exactly.
