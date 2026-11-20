---
title: Witten-Bell smoothing gives every history a distribution over the vocabulary with no zeros
proves: [correctness]
status: full
---

Fix the training text and the vocabulary $V$, with $|V| \ge 1$. Assume that every token predicted in training is in $V$. For a history $h$ (a tuple of at most $n - 1$ tokens), $c(h w)$ is the number of times $h$ is followed by $w$ in the padded text, $c(h) = \sum_w c(h w)$, and $T(h) = |\{w : c(h w) > 0\}|$. For $h \ne \epsilon$, $h'$ is $h$ without its first token.

**Theorem.** For every history $h$, the values $P_{WB}(w \mid h)$ of P-WB for $w \in V$ satisfy $P_{WB}(w \mid h) > 0$ and $\sum_{w \in V} P_{WB}(w \mid h) = 1$.

*Proof.* By induction on the length $\ell$ of $h$. Write $L(w)$ for the value of *lower* in line L1: $L(w) = 1/|V|$ if $h = \epsilon$, and $L(w) = P_{WB}(w \mid h')$ otherwise.

*The values of lower.* If $\ell = 0$, then $L(w) = 1/|V| > 0$ and $\sum_{w \in V} L(w) = 1$. If $\ell \ge 1$, then $h'$ has length $\ell - 1$, and by the induction hypothesis $L(w) > 0$ and $\sum_{w \in V} L(w) = 1$. So in both cases $L$ is a distribution on $V$ with no zeros.

*Case $c(h) = 0$.* Line L2 returns $L(w)$, which has both properties.

*Case $c(h) > 0$.* Some token follows $h$, so $T(h) \ge 1$. Line L3 gives $\lambda = c(h)/(c(h) + T(h))$ with $0 < \lambda < 1$. Line L4 returns $\lambda \, c(h w)/c(h) + (1 - \lambda) L(w)$. The first term is at least 0 and the second is positive, so the value is positive. Every $w$ with $c(h w) > 0$ is a token predicted in training, so it is in $V$, and therefore $\sum_{w \in V} c(h w) = c(h)$. Summing over $V$,

$$\sum_{w \in V} P_{WB}(w \mid h) = \lambda \cdot \frac{c(h)}{c(h)} + (1 - \lambda) \sum_{w \in V} L(w) = \lambda + (1 - \lambda) = 1. \qquad \blacksquare$$

**The closed form.** In the case $c(h) > 0$, $\lambda c(h w)/c(h) = c(h w)/(c(h) + T(h))$ and $1 - \lambda = T(h)/(c(h) + T(h))$, so line L4 equals $\bigl(c(h w) + T(h) P_{WB}(w \mid h')\bigr)/\bigl(c(h) + T(h)\bigr)$, the formula on the page.

**Sentences.** A sentence $w_1 \ldots w_k$ gets $\prod_{i=1}^{k+1} P_{WB}(w_i \mid h_i)$ with $w_{k+1} = $ `</s>` and $h_i$ the $n - 1$ tokens before $w_i$ in the padded sentence. Since every row is a distribution with `</s>` in it, the probabilities of all finite sentences sum to at most 1. There are finitely many histories of $n - 1$ tokens over $V$ and `<s>`, and by the theorem each gives `</s>` a positive probability, so $P_{WB}(\text{</s>} \mid h) \ge \delta$ for one $\delta > 0$ and all of them. The total probability of the sentences with more than $k$ tokens is then at most $(1 - \delta)^k$, which tends to 0, so the probabilities of all finite sentences sum to exactly 1.
