---
tag: 6CBA3Q
kind: algorithm
slug: gru4rec
name: GRU4Rec
aliases:
- recurrent session-based recommendation
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: research
summary: Feeds the items of a session to a gated recurrent network and trains it with ranking losses to score the next item.
solves: [session-based-recommendation]
model: word-ram
complexity:
  vars: {N: the number of events in the training sessions, E: the number of epochs, H: the number of hidden units, B: the number of sessions per mini-batch, n: the number of items}
  time: {worst: O(E N (H^2 + B H))}
  space: {extra: O(n H + H^2)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2016
  people: [Balázs Hidasi, Alexandros Karatzoglou, Linas Baltrunas, Domonkos Tikk]
  note: Hidasi, Karatzoglou, Baltrunas and Tikk (ICLR 2016) applied a GRU network to session-based recommendation with session-parallel mini-batches, in-batch negatives and the BPR and TOP1 losses.
prereqs: [session-based-recommendation, backpropagation-through-time, bayesian-personalized-ranking]
see_also: [sasrec, item-based-collaborative-filtering, vanishing-gradient-problem, adagrad, stochastic-gradient-descent, gradient-checking, cross-entropy-loss, mean-reciprocal-rank]
sources:
  - paper: arxiv:1511.06939
    title: Balázs Hidasi, Alexandros Karatzoglou, Linas Baltrunas and Domonkos Tikk, Session-based recommendations with recurrent neural networks, ICLR 2016
    locator: Section 3 (the GRU, Equations 2 to 5), Section 3.1 (1-of-N input and the network), Section 3.1.1 (session-parallel mini-batches, Figure 2), Section 3.1.2 (in-batch negatives as popularity-based sampling), Section 3.1.3 (the BPR and TOP1 losses), Section 4 (RSC15 and VIDEO, recall@20 and MRR@20, Tables 1 and 3)
  - paper: arxiv:1706.03847
    title: Balázs Hidasi and Alexandros Karatzoglou, Recurrent neural networks with top-k gains for session-based recommendations, CIKM 2018
    locator: Abstract (new ranking losses and extra negative samples, with reported gains in MRR and recall@20)
  - paper: arxiv:1803.09587
    title: Malte Ludewig and Dietmar Jannach, Evaluation of session-based recommendation algorithms
    locator: Abstract (simple nearest neighbor methods often did as well as or better than GRU4Rec in their comparison)
---

GRU4Rec is the session-based recommender of Hidasi, Karatzoglou, Baltrunas and Tikk (2016). It reads the items of a session one at a time with a gated recurrent unit (GRU) network, a kind of recurrent network, and after each item it scores every item as the next one. It trains with ranking losses on the items of the same mini-batch as negatives, and it builds mini-batches from many sessions in parallel, so that sessions of very different lengths can share one batch. It needs no user profile: the hidden state of the network is the state of the session. The paper reported large gains over item-to-item nearest neighbors on two data sets. That is a measurement, and later comparisons measured simple methods doing as well on other data.

## In plain words

A user clicks a few items in a row, with no login and no history. The model keeps a short memory, a vector, and updates it after each click. From the memory it gives each item a score for "this comes next".

The memory update has two gates. One decides how much of the old memory to keep, the other how much of it to use when making a new proposal. Training shows the model real sessions and moves the weights so that the true next item scores higher than the other items in the batch.

## The problem

The input is a set of sessions, each a sequence $s_1, s_2, \dots, s_\ell$ of items from $n$ items. The task of [session-based recommendation](/session-based-recommendation/) is, after each prefix $s_1, \dots, s_t$, to rank the items so that $s_{t+1}$ is near the top. The quality is measured by recall@20 and [MRR](/mean-reciprocal-rank/)@20 on held-out sessions.

The model has input weights $W_z, W_r, W_h$ (one column per item, since the input is one-hot), recurrent weights $U_z, U_r, U_h$ of size $H \times H$, and output vectors $O[k]$ and biases $c_k$. After step $t$ the score of item $k$ is $\hat r_{t,k} = O[k]^\top h_t + c_k$. With target $i$ and $N_S$ negatives $j$, the two losses of Section 3.1.3 are

$$L_{\mathrm{BPR}} = -\frac{1}{N_S} \sum_{j} \ln \sigma(\hat r_i - \hat r_j), \qquad L_{\mathrm{TOP1}} = \frac{1}{N_S} \sum_j \sigma(\hat r_j - \hat r_i) + \sigma(\hat r_j^2).$$

BPR is the loss of [Bayesian personalized ranking](/bayesian-personalized-ranking/) averaged over the negatives. TOP1 is a smooth form of the relative rank of the target, plus a term that pushes the scores of negatives toward 0.

## The algorithm

```pseudo id=main
GRU4REC-TRAIN(sessions, H, B, E, η)
L1  draw all weights at random
L2  repeat E times
L3      for each session-parallel mini-batch of B lanes do
L4          for each lane: h ← 0 if its session starts here, else the state the lane carried
L5          read the input item with GRU-STEP; score the target and the other targets of the batch; get the loss gradient by backpropagation
L6          add the gradients of all lanes
L7          step all weights against the summed gradient with rate η
L8  return the weights

GRU-STEP(x, h)
L9  z ← σ(W_z[x] + U_z h);  r ← σ(W_r[x] + U_r h)       ▷ update gate and reset gate
L10 ĥ ← tanh(W_h[x] + U_h (r ⊙ h))                      ▷ candidate state
L11 return (1 - z) ⊙ h + z ⊙ ĥ
```

Lines L9 to L11 are Equations 2 to 5 of the paper. Session-parallel mini-batches (Section 3.1.1, Figure 2) work as follows. Put the sessions in an order. The first batch holds the first event of each of the first $B$ sessions, with the second events as targets. The next batch holds the second events, and so on. When a session runs out, the next unused session takes its lane and the hidden state of that lane is reset to 0. The negatives of each event are the targets of the other events in the batch (Section 3.1.2). An item is in a batch about as often as it is clicked, so this is sampling in proportion to popularity, and it costs no separate draws.

The code writes the [backpropagation through time](/backpropagation-through-time/) by hand. The training loop carries each lane's hidden state into the next batch but treats it as a constant, so the gradient of a batch stops at the step boundary. That cut is a choice of this code; the paper does not say how far its gradient runs back. The paper trains with [Adagrad](/adagrad/) and puts tanh on the output scores (Section 4.2); the code uses plain [stochastic gradient](/stochastic-gradient-descent/) steps and linear scores.

## Example

Take $H = 1$ and an item $x$ with $W_z[x] = W_r[x] = 0$, $W_h[x] = \ln 3$, all recurrent weights 0, and $h_0 = 0$.

- Line L9: $z = r = \sigma(0) = 0.5$.
- Line L10: $\hat h = \tanh(\ln 3) = (9 - 1)/(9 + 1) = 0.8$.
- Line L11: $h_1 = 0.5 \cdot 0 + 0.5 \cdot 0.8 = 0.4$.

Let the target $i$ have $O[i] = 1$ and one negative $j$ have $O[j] = -1$, both with bias 0. The scores are $\hat r_i = 0.4$ and $\hat r_j = -0.4$.

- BPR: $-\ln \sigma(0.8) = \ln(1 + e^{-0.8}) \approx 0.3711$. Its derivative in $\hat r_i$ is $-\sigma(-0.8) \approx -0.3100$, so a step raises the target score.
- TOP1: $\sigma(-0.8) + \sigma(0.16) \approx 0.3100 + 0.5399 = 0.8499$. The second term is large even though the negative ranks below the target; it pushes $\hat r_j$ toward 0.

For the mini-batches, take sessions $(0, 1, 2, 3)$, $(4, 5)$, $(6)$, $(7, 8, 9)$, $(1, 3, 5, 7, 9)$, $(2, 4)$ and $B = 3$. Session $(6)$ has no target and is skipped. The first batch is the events $0 \to 1$, $4 \to 5$, $7 \to 8$. Session $(4, 5)$ is then done, so in the second batch its lane starts $(1, 3, 5, 7, 9)$ with a reset: $1 \to 2$, $1 \to 3$, $8 \to 9$. The test file checks these values.

## Correctness

The proof in `proofs/correctness.md` shows that the hand-written backward pass is the exact gradient of the summed loss over a sequence: the loss derivatives in the scores, the output layer, and one GRU step backward, then an induction from the last step to the first. It also shows that the session-parallel batches visit each event of each session of length at least 2 exactly once, in order, with a reset at the first event. The tests check every gradient entry against finite differences for both losses. Whether the trained model ranks well is a question of measurement, not of proof.

## Complexity

- **One step.** The GRU step costs $O(H^2)$ for the three recurrent products, and the scores and their gradients cost $O(H)$ per scored item. With in-batch negatives each event scores $B$ items, so one event costs $O(H^2 + B H)$.
- **One epoch.** $N$ events, so $O(N (H^2 + B H))$. The batching itself is $O(N)$.
- **Training.** $O(E N (H^2 + B H))$ for $E$ epochs.
- **Space.** $O(n H)$ for the input and output weights and $O(H^2)$ for the recurrent weights, plus the hidden states of the active lanes.
- **Prediction.** Reading a session of length $\ell$ costs $O(\ell H^2)$ and scoring all items costs $O(n H)$.

## Properties

- **No user model.** The state is built from the session alone, so a new or anonymous user can get recommendations after one click.
- **Order aware.** The state after $s_1, \dots, s_t$ depends on the order of the items, unlike a sum of item vectors.
- **Smooth loss.** Both losses are smooth in all weights, so the gradient exists everywhere.
- **Not convex.** The products in the GRU make the loss non-convex, and training finds a local solution.
- **Popularity bias in the negatives.** In-batch negatives are popular items more often, which changes what the loss pushes down.

## Variants and improvements

- **Loss functions.** The paper found pointwise cross-entropy often unstable and used BPR and TOP1 (Section 4.2). Hidasi and Karatzoglou (2018) added the BPR-max and TOP1-max losses and extra sampled negatives, and reported gains of up to 35% in MRR and recall@20 over the earlier RNN.
- **Larger layers.** The paper reported better results with 1000 hidden units than with 100 for the pairwise losses (Table 3).
- **Deeper networks.** The paper tried more GRU layers and found one layer best on its data.
- **Self-attention.** [SASRec](/sasrec/) replaces the recurrent state by causal self-attention over the past items. An attention or transformer page does not yet exist on the site.
- **Other units.** The paper reported that a plain recurrent unit and an LSTM did worse than the GRU in its experiments.

## When to use it

Hidasi et al. evaluated on RSC15, the RecSys Challenge 2015 clicks (7,966,257 training sessions with 31,637,239 clicks on 37,483 items), and VIDEO, a video service (about 3 million sessions). Their best baseline was session-based [item-to-item nearest neighbors](/item-based-collaborative-filtering/). In Table 3, a GRU with 1000 units and the TOP1 loss reached recall@20 of 0.6206 and MRR@20 of 0.2693 on RSC15, which they reported as 22.53% and 31.49% above item-KNN, and the BPR loss reached recall@20 of 0.6322. On VIDEO, TOP1 with 1000 units reported recall@20 of 0.6624 and MRR@20 of 0.3891.

These are measurements on two data sets with one protocol. Ludewig and Jannach (2018) compared session-based methods on more data sets and found that simple nearest neighbor methods often did as well as or better than GRU4Rec. Use GRU4Rec when sessions are anonymous and the order of the items matters, and compare it with a well-tuned session nearest neighbor baseline.

## Pitfalls

- **Weak baselines.** As with other neural recommenders, a poorly tuned nearest neighbor baseline makes the network look better than it is.
- **Unstable pointwise loss.** The paper reports that cross-entropy gave only 10 and 6 numerically stable networks out of 100 random runs on RSC15 and VIDEO.
- **The hidden state at session ends.** Forgetting to reset the state when a lane switches sessions leaks one session into the next.
- **Truncated gradients.** Stopping the gradient at the batch boundary, as this code does, means the weights never get a signal from more than one step back. It is cheap but it is not the full gradient.
- **Target in the negatives.** If two lanes have the same target, that item is a positive for one lane and a negative for the other. The code drops a lane's own target from its negatives.
- **Gradient checks.** Check the backward pass with finite differences on a nonzero start state, or the $U$ gradients of the first step are zero and the check proves less.

## Implementations

## History

Hidasi, Karatzoglou, Baltrunas and Tikk presented GRU4Rec at ICLR 2016. It was one of the first applications of a recurrent network to session-based recommendation, and it became a standard baseline. Hidasi and Karatzoglou improved the losses and the sampling at CIKM 2018. Ludewig and Jannach published a comparison in 2018 that found simple nearest neighbor methods competitive. Self-attention models such as SASRec (2018) followed.

## References
