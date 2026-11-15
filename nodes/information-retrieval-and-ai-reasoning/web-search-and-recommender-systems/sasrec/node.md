---
tag: QW5Y7Z
kind: algorithm
slug: sasrec
name: SASRec
aliases:
- self-attentive sequential recommendation
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: research
summary: Applies causal self-attention over a user's item sequence to predict the next item, attending to the relevant past items.
solves: [session-based-recommendation]
model: word-ram
complexity:
  vars: {n: the length of a sequence, d: the embedding size, m: the number of items, U: the number of sequences, E: the number of epochs}
  time: {worst: O(E U (n^2 d + n d^2 + m d))}
  space: {extra: O(m d + n d + d^2 + n^2)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2018
  people: [Wang-Cheng Kang, Julian McAuley]
  note: Kang and McAuley (ICDM 2018) applied causal self-attention blocks with a shared item embedding to next-item prediction from a user's sequence of actions.
prereqs: [session-based-recommendation, layer-normalization, backpropagation]
see_also: [gru4rec, neural-collaborative-filtering, bayesian-personalized-ranking, matrix-factorization-recommendation, markov-chain, adam, dropout, normalized-discounted-cumulative-gain]
sources:
  - paper: arxiv:1808.09781
    title: Wang-Cheng Kang and Julian McAuley, Self-attentive sequential recommendation, IEEE International Conference on Data Mining (ICDM 2018)
    locator: Section III-A (item and position embeddings, Equation 1), Section III-B (scaled dot-product attention, Equations 2 and 3, causality, the feed-forward network of Equation 4), Section III-C (stacking, residual connections, layer normalization, dropout), Section III-D (the shared item embedding, Equation 6), Section III-E (the binary cross entropy loss with one negative per step, Adam), Section III-F (complexity O(n^2 d + n d^2)), Section IV (four data sets, Hit@10 and NDCG@10 over 100 sampled negatives, Table III, the ablation in Table IV)
---

SASRec is the sequential recommender of Kang and McAuley (2018). It reads the sequence of items a user has acted on and, at each position, predicts the next item. In place of the recurrent state of [GRU4Rec](/gru4rec/), it uses causal self-attention: the output at position $t$ is a weighted mix of the items at positions $0, \dots, t$, with weights computed from the items themselves, so the model can look at the last item on sparse data and at a longer past on dense data. Each block has a self-attention layer and a small feed-forward network, each with layer normalization and a residual connection, and the score of an item is the inner product of the output with the same item embedding used at the input. The paper measured better ranking than its baselines on four data sets. That is a measurement, made with a sampled evaluation protocol, not a proof.

## In plain words

To guess what a user will pick next, look back over what they picked before, but not all past items matter equally. SASRec learns how much to look at each past item. Each item asks a question (its query), every earlier item offers an answer key, and the better a key matches the question, the more that earlier item counts.

The model may only look back, never ahead, because at prediction time the future is unknown. A mask removes the links to later positions. A position vector added to each item tells the model where the item is in the sequence.

## The problem

The input is a set of user sequences $S^u = (S^u_1, \dots, S^u_{|S^u|})$ over $m$ items, ordered by time. For each prefix the task is to rank the items so that the next one is near the top, the sequential form of [session-based recommendation](/session-based-recommendation/). SASRec keeps the most recent $n$ actions, and the paper pads shorter sequences on the left with a padding item whose embedding is 0.

With one block and one head, as in the code, the model is

$$E_t = M_{s_t} + P_t, \qquad X = \mathrm{LN}_1(E), \qquad A_t = \mathrm{softmax}_{u \le t}\Bigl(\frac{(X_t W^Q) \cdot (X_u W^K)}{\sqrt d}\Bigr),$$

$$S_t = E_t + \sum_{u \le t} A_{t,u}\, X_u W^V, \qquad F_t = S_t + \mathrm{ReLU}\bigl(\mathrm{LN}_2(S_t) W^{(1)} + b^{(1)}\bigr) W^{(2)} + b^{(2)}, \qquad r_{i,t} = F_t \cdot M_i.$$

$M \in \mathbb R^{m \times d}$ is the item embedding, shared by the input and the prediction (Equation 6), $P \in \mathbb R^{n \times d}$ is a learned position embedding, and [layer normalization](/layer-normalization/) is $\mathrm{LN}(x) = \alpha \odot (x - \mu)/\sqrt{\sigma^2 + \epsilon} + \beta$. With the target $o_t = s_{t+1}$ and one negative $j$ per step, drawn from the items not in the user's sequence, the loss of Section III-E is

$$-\sum_u \sum_t \Bigl[\ln \sigma(r_{o_t, t}) + \ln\bigl(1 - \sigma(r_{j, t})\bigr)\Bigr],$$

the [log loss](/logistic-loss/) on one positive and one negative per position.

## The algorithm

```pseudo id=main
SASREC-TRAIN(sequences, d, E, η)
L1  draw M, P and the block weights at random; gains 1, biases 0
L2  repeat E times
L3      for each sequence s, in random order do
L4          for each position t: target o_t ← s_{t+1}, and a random negative j_t not in s
L5          F ← FORWARD(s); loss and gradient of -Σ_t [ln σ(F_t·M[o_t]) + ln σ(-F_t·M[j_t])] by backpropagation
L6          for each weight w do
L7              w ← w - η · ∂loss/∂w
L8  return the weights

FORWARD(s)
L9  E_t ← M[s_t] + P_t for each position t
L10 X ← LN₁(E);  Q, K, V ← X W^Q, X W^K, X W^V
L11 A_{t,u} ← softmax over u ≤ t of Q_t·K_u / √d     ▷ the causal mask: no u > t
L12 S_t ← E_t + Σ_{u ≤ t} A_{t,u} V_u
L13 F_t ← S_t + ReLU(LN₂(S_t) W¹ + b¹) W² + b²
L14 return F
```

The [backpropagation](/backpropagation/) of line L5 runs through the prediction layer, the feed-forward network, the second layer normalization, the softmax attention, the projections and the first layer normalization; the code writes every part by hand and checks each gradient entry against finite differences. The paper stacks two blocks, applies [dropout](/dropout/) to the embeddings and to the output of each sublayer, and trains with [Adam](/adam/) at learning rate 0.001 and batch size 128. The code uses one block, no dropout, plain gradient steps and no padding.

## Example

Take $d = 2$, items $M_0 = (2, 0)$, $M_1 = (0, 3)$, $M_2 = (1, 1)$, positions $P_0 = (0, 0)$, $P_1 = (0, 1)$, layer normalizations with gain 1 and bias 0, $W^Q = W^K = 0$, $W^V = I$, and a feed-forward network with zero weights. The sequence is $(0, 1)$.

- Line L9: $E_0 = (2, 0)$ and $E_1 = (0, 4)$.
- Line L10: each row is normalized to mean 0 and variance 1: $X_0 = (1, -1)$ and $X_1 = (-1, 1)$, up to the tiny $\epsilon$. So $V = X$.
- Line L11: with zero queries and keys all scores are 0. Position 0 may look only at itself, $A_0 = (1)$. Position 1 looks at both, with equal weight, $A_1 = (1/2, 1/2)$.
- Line L12: $S_0 = (2, 0) + (1, -1) = (3, -1)$ and $S_1 = (0, 4) + \tfrac12 (1, -1) + \tfrac12 (-1, 1) = (0, 4)$.
- Line L13: the feed-forward network adds 0, so $F = S$.

The score of item 2 as the next item after the whole sequence is $F_1 \cdot M_2 = 0 + 4 = 4$. $F_0 = (3, -1)$ does not depend on item 1; whatever item is put at position 1, the first row stays the same. The test file checks these values, and it checks the second claim in general by changing each later item and comparing the earlier outputs as floats.

## Correctness

The proof in `proofs/correctness.md` shows two things. First, causality: $F_t$ depends only on $s_0, \dots, s_t$, because the attention sums run over $u \le t$ and all other operations act on one position at a time; in the code this holds exactly in floating point. Second, the backward pass is the exact gradient of the loss, by lemmas for the output, for layer normalization and for softmax attention, put together in reverse order of the forward graph. Whether the trained model ranks well is measured, not proved.

## Complexity

- **One sequence.** The attention scores and the weighted sums cost $O(n^2 d)$, and the projections and the feed-forward network cost $O(n d^2)$, so the forward and backward passes cost $O(n^2 d + n d^2)$, as in Section III-F. The paper notes that the $n^2 d$ term usually dominates.
- **Training.** $O(E U (n^2 d + n d^2))$ for $E$ epochs over $U$ sequences. The code also updates the whole item table at each step, which adds $O(m d)$ per step; an update of the used rows only would remove it.
- **Space.** $O(m d + n d + d^2)$ parameters, which do not grow with the number of users, plus $O(n^2 + n d)$ for the attention weights and the cache of one sequence.
- **Prediction.** After the forward pass, scoring an item costs $O(d)$, as for [matrix factorization](/matrix-factorization-recommendation/).
- **Parallel time.** The positions of one layer can be computed at the same time, unlike a recurrent network, which must finish step $t - 1$ before step $t$. The paper reported SASRec over ten times faster than the RNN and CNN baselines on a GPU.

## Properties

- **Causal.** The output at position $t$ uses only positions $0, \dots, t$, so training on all positions at once does not leak the targets.
- **Adaptive range.** The attention weights decide how far back to look. The paper reported that the model attended mostly to recent items on sparse data and further back on dense data.
- **Order through positions only.** Without $P$, the attention weights do not depend on the order of the past items. The paper's ablation found removing $P$ better on its sparsest data set and worse on the others.
- **Shared embedding.** One matrix $M$ serves the input and the prediction. The paper reported that this improved the results; the nonlinear block still allows asymmetric transitions.
- **Not convex.** The loss is not convex in the weights.

## Variants and improvements

- **More blocks and heads.** The paper's default stacks two blocks with one head. In its ablation (Table IV, NDCG@10), one block did reasonably well, two blocks did better mainly on the dense data sets, three blocks were about the same as two, and two heads were slightly worse than one.
- **User embedding.** Adding a user vector to $F_t$ is possible; the paper found it did not help.
- **Long sequences.** The quadratic cost limits $n$. The paper suggests attention restricted to recent actions, or splitting long sequences.
- **Bidirectional models.** Later models train with masked items in both directions in place of next-item prediction. There is no page for these yet.
- **Recurrent models.** [GRU4Rec](/gru4rec/) keeps a recurrent state in place of attention. Recurrent network, attention and transformer pages do not yet exist on the site.

## When to use it

Kang and McAuley evaluated on Amazon Beauty, Amazon Games, Steam and MovieLens-1M, with the last action of each user held out for testing and the one before it for validation. They ranked the held-out item against 100 sampled negative items and measured Hit@10 and [NDCG](/normalized-discounted-cumulative-gain/)@10. In Table III SASRec was best on all four data sets, and they reported average gains of 6.9% in Hit Rate and 9.6% in NDCG over the strongest baseline. They also observed that non-neural methods did better among the baselines on the sparse data sets and neural ones on the dense data sets.

These are measurements with one protocol, and ranking among 100 sampled items is a different measure from ranking among all items. Use SASRec when users have long ordered histories and the order matters, and compare it on full rankings with simple sequential baselines, such as a first-order [Markov chain](/markov-chain/) over items, and with tuned non-sequential ones.

## Pitfalls

- **A leaky mask.** If position $t$ can see position $t + 1$, the model learns to copy the target and the training loss falls while real accuracy does not. Test it by changing a later item and checking that earlier outputs do not change.
- **Padding.** With left padding, the loss terms whose target is the padding item must be dropped, and the padding embedding must stay 0.
- **Negatives from the history.** The paper draws negatives from items not in the user's sequence, so items already seen are never pushed down. Recommend among unseen items, as the code does, or the model may suggest an item the user just took.
- **Sampled metrics.** Results with 100 sampled negatives are not comparable with results over the full catalog.
- **Layer normalization at a constant row.** If all entries of a row are equal, the variance is 0 and only $\epsilon$ keeps the division finite; gradients there are large.
- **Softmax overflow.** Subtract the largest score before taking exponentials, as the code does.

## Implementations

## History

Kang and McAuley presented SASRec at ICDM 2018. It brought the self-attention design of the transformer, from machine translation, to next-item recommendation, and compared it with Markov chain models, GRU4Rec and the convolutional model Caser. It became a standard baseline for sequential recommendation, and later models built on it with more layers, bidirectional training and other objectives.

## References
