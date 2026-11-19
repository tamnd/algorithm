---
title: Stupid backoff computes its recursive score, every score of a seen word lies in (0, 1], and the scores after a history of length m - 1 sum to at least 1 when the history was seen and to at most 1 + alpha + ... + alpha^(m-1)
proves: [correctness]
status: full
---

We use the notation of the page. Each sentence is padded with $n - 1$ copies of <s> and one </s>. For an m-gram $g$ with $1 \le m \le n$, $c(g)$ is the number of predicted positions where $g$ ends, and for a history $h$ of length $m - 1$ we write $c(h) = \sum_x c(h x)$. The vocabulary $V$ is the set of predicted tokens, so $c(w) \ge 1$ for every $w \in V$. The score is

$$S(w \mid h) = \frac{c(h w)}{c(h)} \text{ if } c(h w) > 0, \qquad S(w \mid h) = \alpha\, S(w \mid h') \text{ otherwise}, \qquad S(w \mid ()) = \frac{c(w)}{N} \text{ or } 0,$$

with $h'$ the history $h$ without its first token, $N = c(())$ the number of predicted tokens and $0 \le \alpha \le 1$.

**Lemma 1 (the counts).** The training loop gives $c(g)$ and $c(h)$ as defined.

*Proof.* The loop visits each predicted position $i$ once and adds one to every suffix $g$ of length $m = 1, \ldots, n$ of the tokens that end at $i$; these suffixes exist because of the $n - 1$ pads. So $c(g)$ counts the predicted positions where $g$ ends. In the same step it adds one to $c(g[{:}-1])$, the history of $g$. A history $h$ of length $m - 1$ gets one for each position $i$ where some $h x$ ends, which is $\sum_x c(h x)$. $\square$

**Theorem 2 (the score).** Lines L1 to L4 return $S(w \mid h)$.

*Proof.* Induction on the length of $h$. Line L1 tests $c(h w) > 0$ and line L2 returns $c(h w)/c(h)$; here $c(h) \ge c(h w) > 0$, so the division is defined. If $c(h w) = 0$ and $h$ is empty, $w$ was never predicted, and line L3 returns 0. Otherwise line L4 returns $\alpha$ times the score of the shorter history, which is correct by the induction hypothesis. $\square$

**Theorem 3 (range).** For $w \in V$ and every $h$, $0 < S(w \mid h) \le 1$ when $\alpha > 0$, and $0 \le S(w \mid h) \le 1$ when $\alpha = 0$. For $w \notin V$, $S(w \mid h) = 0$.

*Proof.* A ratio from line L2 is in $(0, 1]$ because $0 < c(h w) \le c(h)$. Line L4 multiplies a value in $[0, 1]$ by $\alpha \in [0, 1]$. The recursion ends at the empty history at the latest, where $S(w \mid ()) = c(w)/N > 0$ for $w \in V$. So every score of a word of $V$ is a product of a positive ratio and some powers of $\alpha$. A word not in $V$ has $c(h w) = 0$ for every $h$, so it reaches line L3. $\square$

**Theorem 4 (the sum is not 1).** Let $h$ have length $m - 1$ and let $B_m = 1 + \alpha + \cdots + \alpha^{m-1}$. Then

1. if $c(h) > 0$, then $\sum_{w \in V} S(w \mid h) \ge 1$, with equality exactly when $\alpha = 0$ or every word of $V$ was seen after $h$;
2. for every $h$, $\sum_{w \in V} S(w \mid h) \le B_m < 1 / (1 - \alpha)$ when $\alpha < 1$.

*Proof.* Split $V$ into the set $A$ of words with $c(h w) > 0$ and the rest. The words of $A$ give $\sum_{w \in A} c(h w)/c(h) = 1$ by the definition of $c(h)$, when $c(h) > 0$. The rest give $\alpha \sum_{w \notin A} S(w \mid h') \ge 0$, and by Theorem 3 this is positive exactly when $\alpha > 0$ and $A \ne V$. This proves part 1.

For part 2 use induction on $m$. For $m = 1$ the sum is $\sum_w c(w)/N = 1 = B_1$. For $m \ge 2$ the words of $A$ give at most 1 (exactly 1 if $A$ is not empty, 0 if it is), and the rest give at most $\alpha \sum_{w \in V} S(w \mid h') \le \alpha B_{m-1}$ by the induction hypothesis. So the sum is at most $1 + \alpha B_{m-1} = B_m$. $\square$

The bound is reached only in the limit, but the sum is often above 1. On the three sentences "a b", "a c" and "b c" with $n = 2$ and $\alpha = 2/5$, the scores after <s> are 2/3, 1/3, 4/45 and 2/15, which sum to 11/9. After a history that was never seen the sum can be below 1: with $n = 3$ on the same text, the scores after <s> c sum to 38/75. So no choice of a constant $\alpha > 0$ makes all rows sum to 1, and the scores are not a probability distribution. This is why stupid backoff has no [perplexity](/perplexity/).
