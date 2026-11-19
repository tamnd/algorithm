---
title: The graphone lattice gives the exact joint probability, the exact expected counts and the best graphone sequence
proves: [correctness]
status: full
---

Fix the order $M$, the chunk limits $L_g \ge 1$ and $L_p \ge 0$, and a model $p(q \mid h)$ over graphones $q$ and the end symbol $\langle/s\rangle$. A history $h$ is the tuple of the last $M - 1$ symbols, padded at the start with $\langle s\rangle$; write $h \oplus q$ for the history after $q$ (drop the oldest symbol, append $q$). For $M = 1$ every history is the empty tuple. The weight of a graphone sequence $Q = q_1 \ldots q_K$ is

$$P(Q) = \prod_{k=1}^{K} p(q_k \mid h_{k-1}) \cdot p(\langle/s\rangle \mid h_K), \qquad h_0 = \langle s\rangle^{M-1},\ h_k = h_{k-1} \oplus q_k.$$

A joint segmentation of the pair $(g, \varphi)$ is a sequence $Q$ whose letter sides concatenate to $g$ and whose phoneme sides concatenate to $\varphi$, with $1 \le |q_k^g| \le L_g$ and $0 \le |q_k^\varphi| \le L_p$. Let $S(g, \varphi)$ be the set of joint segmentations and $Z = \sum_{Q \in S(g,\varphi)} P(Q)$.

## The lattice

The states are the triples $(i, j, h)$ with $0 \le i \le |g|$ and $0 \le j \le |\varphi|$. There is an arc from $(i, j, h)$ to $(i + a, j + b, h \oplus q)$ with weight $p(q \mid h)$ for each $q = (g[i..i+a), \varphi[j..j+b))$ with $1 \le a \le L_g$ and $0 \le b \le L_p$ that fits. Every arc increases $i$ by at least 1, because every graphone has a letter, so the lattice is acyclic and the order of increasing $i$ is a topological order.

**Lemma 1 (bijection).** The map that sends $Q \in S(g, \varphi)$ to the path that starts at $(0, 0, h_0)$ and follows the arcs of $q_1, \ldots, q_K$ is a bijection between $S(g, \varphi)$ and the paths from $(0, 0, h_0)$ to a state $(|g|, |\varphi|, h)$. The product of the arc weights of the path, times $p(\langle/s\rangle \mid h)$, is $P(Q)$.

*Proof.* After $k$ graphones of $Q$ the path is at $(|q_1^g \cdots q_k^g|, |q_1^\varphi \cdots q_k^\varphi|, h_k)$, and the arc for $q_{k+1}$ exists because $q_{k+1}$ is the next chunk of both strings. The path ends at $(|g|, |\varphi|, h_K)$. Conversely, a path reads off a sequence of graphones whose sides are consecutive chunks that start at 0 and end at the full lengths, so it is a joint segmentation. The two maps are inverse because the arc out of a state is fixed by its graphone. The weight claim is the definition of $P(Q)$. $\square$

## Forward and log Z (log semiring)

Let $\alpha(i, j, h)$ be the sum, over the paths from $(0, 0, h_0)$ to $(i, j, h)$, of the product of their arc weights. Lines L10 to L14 work in the log semiring $(\mathbb{R} \cup \{-\infty\}, \text{log\_add}, +, -\infty, 0)$, which is isomorphic to the probability semiring by $x \mapsto e^x$.

**Lemma 2.** When the loop of line L11 reaches letter position $i$, every state $(i, j, h)$ holds $\log \alpha(i, j, h)$.

*Proof.* By induction on $i$. For $i = 0$ the only state with a path is $(0, 0, h_0)$, reached by the empty path of weight 1, and line L10 stores $\log 1 = 0$. No arc enters a state with $i = 0$. Let $i > 0$. Every path into $(i, j, h)$ ends with an arc from some state $(i', j', h')$ with $i' < i$. By the induction hypothesis that state held its final value when line L11 processed $i'$, and line L14 then added (log_add) its value plus the log weight of the arc. Every such arc is processed once, because line L11 visits $i' < i$ before $i$ and line L12 lists each fitting graphone once. By distributivity, the sum over paths into $(i, j, h)$ is the sum over the last arc of $\alpha(\text{source}) \cdot p(q \mid h')$. Arcs with weight 0 are skipped, which changes no sum. $\square$

**Theorem 1.** Line L15 returns $\log Z$.

*Proof.* By Lemma 2 at $i = |g|$ and Lemma 1, $\sum_h \alpha(|g|, |\varphi|, h)\, p(\langle/s\rangle \mid h) = \sum_{Q \in S(g, \varphi)} P(Q) = Z$. $\square$

## Expected counts

Define $\beta(i, j, h)$ as the sum over the paths from $(i, j, h)$ to an end state of the product of the arc weights times $p(\langle/s\rangle \mid h_{\text{end}})$. The function `backward` computes $\log \beta$ by the mirror of Lemma 2, in the order of decreasing $i$.

**Theorem 2.** For each history $h$ and graphone $q$, line L7 accumulates

$$c(h, q) = \sum_{(g, \varphi)} \sum_{Q \in S(g, \varphi)} \frac{P(Q)}{Z_{g,\varphi}}\, n_{h,q}(Q),$$

where $n_{h,q}(Q)$ is the number of positions $k$ with $h_{k-1} = h$ and $q_k = q$. The count of $\langle/s\rangle$ after $h$ is the same with $n_{h,\langle/s\rangle}(Q) = [h_K = h]$.

*Proof.* By Lemma 1, $\sum_Q P(Q)\, n_{h,q}(Q)$ is the sum over the pairs (path, arc of the path with label $q$ out of a state with history $h$) of the path weight. Split each such path at the arc: the weight is the weight of the prefix, times $p(q \mid h)$, times the weight of the suffix with the end factor. Summing over prefixes and suffixes gives $\alpha(i, j, h)\, p(q \mid h)\, \beta(i + a, j + b, h \oplus q)$, summed over the arcs with label $q$ out of a state with history $h$. Dividing by $Z$ and adding over the lexicon gives line L7. The end symbol is the same argument with the empty suffix. $\square$

## EM

The M step of line L8 sets $p'(q \mid h) = c(h, q) / \sum_{q'} c(h, q')$. For a fixed $h$ this is the unique maximizer of $\sum_q c(h, q) \log p'(q \mid h)$ over the probability vectors (Gibbs' inequality), so it maximizes the expected complete-data log likelihood $\sum_{h,q} c(h, q) \log p'(q \mid h)$. This is the M step of the [expectation-maximization](/expectation-maximization/) algorithm with the joint segmentation as the hidden variable, so the standard EM argument (Dempster, Laird and Rubin 1977) gives $\sum \log Z'_{g,\varphi} \ge \sum \log Z_{g,\varphi}$: the log likelihood of the lexicon never decreases. A graphone with count 0 gets probability 0 and stays at 0 in every later iteration.

## Decoding (Viterbi semiring)

`decode` works on the lattice of states $(i, h)$ for the letters alone: an arc from $(i, h)$ to $(i + a, h \oplus q)$ with weight $p(q \mid h)$ for each graphone $q$ of the model with $q^g = g[i..i+a)$. As in Lemma 1, the paths from $(0, h_0)$ to a state $(|g|, h)$ are in bijection with the graphone sequences whose letter sides concatenate to $g$.

**Theorem 3.** If some graphone sequence of positive weight spells $g$, lines L16 to L21 return one of largest weight $P(Q)$, and the log of that weight.

*Proof.* The argument of Lemma 2 in the Viterbi semiring $(\mathbb{R} \cup \{-\infty\}, \max, +, -\infty, 0)$ shows that when line L17 reaches $i$, each $\delta(i, h)$ is the largest log weight of a path into $(i, h)$, and the stored back pointer names the last arc of one such path: line L19 replaces the stored value only by a strictly larger one, so the stored pointer always belongs to the stored value. Line L20 takes the end state that maximizes $\delta(|g|, h) + \log p(\langle/s\rangle \mid h)$, which is the largest $\log P(Q)$. Following the pointers from it rebuilds a path whose log weight is that value, by induction on the number of arcs, and line L21 reads its graphones and phonemes. $\square$

The decoder maximizes over graphone sequences, not over pronunciations: the probability of a pronunciation $\varphi$ is the sum over all its joint segmentations with $g$, and the $\varphi$ of the best single sequence need not be the $\varphi$ of the largest sum. This is the maximum approximation of Bisani and Ney.
