---
title: Contrastive search maximizes its score over the top-k candidates and reduces to greedy decoding
proves: [correctness]
status: full
---

We use the notation of the page. At each step the model gives the next-token distribution $p$ for the prefix $y$ and the hidden states $h_1, \ldots, h_{|y|}$ of its positions; for a candidate $v$, $h_v$ is the state of the last position of $y v$. The cosine similarity is $s(a, b) = a \cdot b / (\lVert a \rVert \lVert b \rVert)$, and we set $s(a, b) = 0$ when $a$ or $b$ is the zero vector. The score of a candidate is

$$\text{score}(v) = (1 - \alpha) \, p(v) - \alpha \max_{1 \le j \le |y|} s(h_v, h_j),$$

with $0 \le \alpha \le 1$, and the maximum over an empty context is 0.

**Lemma 1 (termination and cost).** CONTRASTIVE-SEARCH runs at most $N$ steps. Each step makes $k' + 1$ calls of the model, where $k' = \min(k, |V|)$, and appends one token.

*Proof.* The loop of line L2 runs at most $N$ times. Line L3 makes one call, and line L6 makes one call per candidate. $\square$

**Lemma 2 (the step).** Let $K$ be the list of line L4: the $k'$ most probable tokens, sorted by probability from high to low, with the smaller index first on ties. The token $w$ of line L8 has the largest score among the tokens of $K$, and among the tokens of largest score it is the first one in $K$.

*Proof.* That $K$ holds $k'$ tokens of largest probability is the exchange argument of [top-k sampling](/top-k-sampling/). Line L7 computes the score of each candidate. Line L8 scans the scores in the order of $K$ and replaces the best only on a strictly larger score, so it ends at the first candidate of largest score. $\square$

**Theorem 3 (greedy limits).** If $\alpha = 0$, or if $k = 1$, CONTRASTIVE-SEARCH returns the output of [greedy decoding](/greedy-decoding/) with the tie rule "first index of the largest probability".

*Proof.* With $k = 1$, $K$ holds one token, the first index of the largest probability, and line L8 must return it. With $\alpha = 0$, the score is $p(v)$. The first token of $K$ has the largest probability, and among the tokens of largest probability it has the smallest index; every later token of $K$ has a smaller probability, or the same probability and a larger index. So by Lemma 2 the step returns the first token of $K$, which is the greedy choice. By induction on the steps, the two decoders build the same prefix, and they stop at the same time. $\square$

**Lemma 4 (scale of the states).** Multiplying every hidden state by the same number $c > 0$, or each state by its own positive number, does not change any score or the output.

*Proof.* $s(c a, d b) = cd \, (a \cdot b) / (|c| \lVert a \rVert \, |d| \lVert b \rVert) = s(a, b)$ for $c, d > 0$. $\square$

So only the directions of the states matter. A model that changes the length of its states from layer to layer or from token to token gives the same search.

**Proposition 5 (when probability wins).** The penalty $\max_j s(h_v, h_j)$ lies in $[-1, 1]$. So for two candidates $v, w \in K$,

$$\text{score}(v) - \text{score}(w) \ge (1 - \alpha)(p(v) - p(w)) - 2 \alpha,$$

and $v$ has the larger score, whatever the states, when $(1 - \alpha)(p(v) - p(w)) > 2 \alpha$. For $\alpha = 1$, the score is minus the penalty, and the step returns the first candidate of smallest largest similarity to the context.

*Proof.* The cosine of two vectors lies in $[-1, 1]$ by the Cauchy-Schwarz inequality, and it is 0 by definition for a zero vector, so the maximum lies in $[-1, 1]$ too. The difference of the penalties of $v$ and $w$ is at most 2, which gives the bound. For $\alpha = 1$ the probability term is 0. $\square$

For example, with $\alpha = 0.6$, the bound requires $0.4 (p(v) - p(w)) > 1.2$, which no pair of probabilities satisfies; at that setting the states can always overrule the probabilities among the candidates. With $\alpha = 0.2$, the bound holds when $p(v) - p(w) > 0.5$.

**Remark (what is not claimed).** Contrastive search is deterministic and makes no claim about the probability of its output, which is in general neither the mode nor a sample from the model. Lemma 2 and Theorem 3 say that the code computes the rule of Su et al. 2022. The tests check Lemma 2 against a direct enumeration of the scores on random toy models, Theorem 3 against a greedy decoder, and Lemma 4 by scaling the states.
