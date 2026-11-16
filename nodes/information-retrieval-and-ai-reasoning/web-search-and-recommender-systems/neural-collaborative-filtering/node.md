---
tag: 9XDZVT
kind: algorithm
slug: neural-collaborative-filtering
name: Neural collaborative filtering
aliases:
- NCF
- NeuMF
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: research
summary: Replaces the dot product of matrix factorization by a neural network over user and item embeddings, trained on implicit feedback.
solves: [recommendation-problem]
model: word-ram
complexity:
  vars: {m: the number of users, n: the number of items, s: the number of positive pairs, q: the number of negatives per positive, E: the number of epochs, k: the embedding size, P: the number of weights of the hidden layers}
  time: {worst: O(E s (q + 1) (k + P))}
  space: {extra: O((m + n) k + P)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2017
  people: [Xiangnan He, Lizi Liao, Hanwang Zhang, Liqiang Nie, Xia Hu, Tat-Seng Chua]
  note: He, Liao, Zhang, Nie, Hu and Chua (WWW 2017) proposed GMF, an MLP over concatenated embeddings, and NeuMF, which joins them; Rendle, Krichene, Zhang and Anderson (RecSys 2020) measured a tuned dot product doing better on the same data.
prereqs: [matrix-factorization-recommendation, implicit-feedback, backpropagation]
see_also: [bayesian-personalized-ranking, implicit-feedback-als, logistic-loss, relu, gradient-checking, adam, maximum-inner-product-search, sasrec]
sources:
  - paper: doi:10.1145/3038912.3052569
    title: Xiangnan He, Lizi Liao, Hanwang Zhang, Liqiang Nie, Xia Hu and Tat-Seng Chua, Neural collaborative filtering, Proceedings of the 26th International Conference on World Wide Web (WWW 2017), 173-182
    locator: Section 3.1 (the general framework and the log loss with negative sampling, Equation 7), Section 3.2 (GMF, Equations 8 and 9), Section 3.3 (MLP, Equation 10), Section 3.4 (NeuMF, Equation 12, and pre-training in 3.4.1), Section 4 (MovieLens and Pinterest, leave-one-out with HR@10 and NDCG@10)
  - paper: doi:10.1145/3383313.3412488
    title: Steffen Rendle, Walid Krichene, Li Zhang and John Anderson, Neural collaborative filtering vs. matrix factorization revisited, Proceedings of the 14th ACM Conference on Recommender Systems (RecSys 2020), 240-248
    locator: Section 3 (the NCF experiments rerun with a tuned dot product, Figure 2), Section 3.4 (test-set selection of the NCF numbers), Section 4 (learning a dot product with an MLP is hard, Figure 3), Section 5 (the cost of serving MLP scores)
  - paper: arxiv:2005.09683
    title: Steffen Rendle, Walid Krichene, Li Zhang and John Anderson, Neural collaborative filtering vs. matrix factorization revisited, arXiv version
    locator: Sections 3.2 and 3.3 and Appendix A (the setup of the dot product baseline and the embedding sizes 16 to 192)
---

Neural collaborative filtering (NCF) is a family of models of He, Liao, Zhang, Nie, Hu and Chua (2017) that score a user and an item with a neural network over their embeddings in place of the dot product of [matrix factorization](/matrix-factorization-recommendation/). GMF multiplies the two embeddings entry by entry and applies learned weights; the MLP part feeds the concatenated embeddings through layers of [ReLU](/relu/) units; and NeuMF adds the two, each with its own embeddings. The models are trained on [implicit feedback](/implicit-feedback/) with the log loss, with sampled unused items as negatives. The paper reported that NeuMF ranked better than the baselines it tested. Rendle, Krichene, Zhang and Anderson (2020) reran the same experiments and measured a different result: a well-tuned dot product did better than the learned MLP similarity in their experiments.

## In plain words

Matrix factorization scores a user and an item by multiplying their profiles number by number and adding up. NCF asks whether a small neural network could learn a better way to combine the two profiles. It keeps the multiply-and-add path, adds a second path that runs the profiles through a network, and learns how much to trust each.

A network can in theory represent the dot product and much more. Whether it learns something better from real data is a question of experiment, and the experiments disagree with the original claim when the simple baseline is tuned with care.

## The problem

The input is a set $S$ of positive pairs of $m$ users and $n$ items, an embedding size $k$, the widths of the hidden layers, and a number $q$ of negatives per positive. NeuMF (Section 3.4, Equation 12) computes

$$\varphi^{G} = p_u^G \odot q_i^G, \qquad z_0 = [p_u^M ; q_i^M], \qquad z_l = \mathrm{ReLU}(W_l z_{l-1} + b_l) \;\; (l = 1, \dots, L),$$

$$\hat y_{ui} = \sigma\bigl(h^\top [\varphi^{G} ; z_L]\bigr),$$

with separate embeddings $p^G, q^G$ for the GMF part and $p^M, q^M$ for the MLP part. The training set has label $y = 1$ for each pair of $S$, and label $y = 0$ for $q$ items drawn uniformly from the items the user has not used. The loss is the [log loss](/logistic-loss/) of Equation 7,

$$L = -\sum_{(u, i) \in S} \ln \hat y_{ui} - \sum_{(u, j) \in S^-} \ln(1 - \hat y_{uj}).$$

The output is a score for each user and item, and the recommendation is the unused items in order of score.

## The algorithm

```pseudo id=main
NCF-TRAIN(S, k, widths, q, E, η)
L1  draw all embeddings and weights from a Gaussian with a small spread
L2  repeat E times
L3      D ← {(u, i, 1) : (u, i) ∈ S} ∪ {(u, j, 0) : q random unused j for each (u, i) ∈ S}
L4      for each (u, i, y) in D, in random order do
L5          s ← SCORE(u, i)
L6          step every parameter used in L5 against the gradient of -y ln σ(s) - (1 - y) ln σ(-s)
L7  return the parameters

SCORE(u, i)
L8  g ← p_u^G ⊙ q_i^G                          ▷ GMF part
L9  z ← [p_u^M ; q_i^M]                        ▷ MLP part
L10 for each hidden layer l do z ← ReLU(W_l z + b_l)
L11 return hᵀ[g ; z]                           ▷ the logit; the prediction is σ of it
```

The gradient of line L6 comes from [backpropagation](/backpropagation/): the derivative of the loss in the logit is $\sigma(s) - y$, the top layer passes $(\sigma(s) - y) h$ down, and each ReLU layer passes $W_l^\top$ times the derivative of its active units. The code writes all of it by hand and checks every entry against finite differences. The paper uses Adam, and for NeuMF it first trains GMF and the MLP alone and then joins them with weight $\alpha = 0.5$ on each part (Section 3.4.1). The code uses plain stochastic gradient steps and no pre-training.

## Example

Take $k = 2$ and one hidden layer of width 2. Let $p_u^G = (1, 2)$, $q_i^G = (0.5, -1)$, $p_u^M = (1, 0)$, $q_i^M = (0, 1)$,

$$W_1 = \begin{pmatrix} 1 & -1 & 1 & 0 \\ 0 & 1 & 1 & 1 \end{pmatrix}, \qquad b_1 = (0, -0.5), \qquad h = (1, 0.5, 2, -1).$$

- Line L8: $g = (0.5, -2)$.
- Line L9: $z_0 = (1, 0, 0, 1)$.
- Line L10: $W_1 z_0 + b_1 = (1, 1 - 0.5) = (1, 0.5)$, and both units are active, so $z_1 = (1, 0.5)$.
- Line L11: $s = 1 \cdot 0.5 + 0.5 \cdot (-2) + 2 \cdot 1 + (-1) \cdot 0.5 = 1$, so $\hat y = \sigma(1) \approx 0.7311$.

For a positive example, $\partial L / \partial s = \sigma(1) - 1 \approx -0.2689$. The gradient for the third entry of $h$ is that times $z_{1,1} = 1$, and the gradient for $W_1$ in row 2, column 4 is that times $h_4 = -1$ times $z_{0,4} = 1$, about $0.2689$. A step against these gradients raises $s$. The test file checks these values.

With $h = (1, 1, 0, 0)$ the MLP part is switched off and the score is $p_u^{G\top} q_i^G = 0.5 - 2 = -1.5$, the plain dot product.

## Correctness

The proof in `proofs/correctness.md` shows that the hand-written backward pass is the exact gradient of the log loss at every point where no hidden unit is exactly at 0, by the chain rule applied layer by layer from the top. It also shows that matrix factorization is the special case $h^G = \mathbf{1}$, $h^M = 0$, so NeuMF can represent every score that matrix factorization can. That does not mean that training finds a better model: the loss is not convex, and which model ranks better on held-out data is measured, not proved.

## Complexity

- **One example.** The forward and backward passes cost $O(k + P)$, where $P$ is the number of weights in the hidden layers.
- **One epoch.** $s (q + 1)$ examples, so $O(s (q + 1)(k + P))$. The paper uses $q = 4$.
- **Training.** $O(E s (q + 1)(k + P))$ for $E$ epochs.
- **Space.** $O((m + n) k)$ for the four embedding tables and $O(P)$ for the weights; a step touches only the four rows of $u$ and $i$.
- **Serving.** Ranking all $n$ items for one user costs $n$ forward passes, $O(n (k + P))$. A dot product model can use [maximum inner product search](/maximum-inner-product-search/) instead, which is the cost argument of Section 5 of Rendle et al. (2020).

## Properties

- **Contains matrix factorization.** With the MLP weights of $h$ at 0 and the GMF weights at 1, the score is the dot product.
- **Not convex.** The products of embeddings and the hidden layers make the loss non-convex.
- **Pointwise loss.** Each example is scored alone, unlike the pairwise loss of [BPR](/bayesian-personalized-ranking/).
- **Costly to serve.** The score is not an inner product of a user vector and an item vector, so standard fast retrieval does not apply.

## Variants and improvements

- **GMF.** Only the product part, $\sigma(h^\top (p_u \odot q_i))$; with $h = \mathbf{1}$ and no output nonlinearity it is matrix factorization.
- **MLP only.** Only the concatenation part. The paper used a tower of layers that halve in width.
- **Pre-training.** Train GMF and the MLP alone, then start NeuMF from both with $\alpha = 0.5$ on each part.
- **Other losses.** The pairwise loss of [BPR](/bayesian-personalized-ranking/) can replace the log loss.
- **Sequence models.** [SASRec](/sasrec/) and [GRU4Rec](/gru4rec/) use neural networks over the item history in place of a user embedding.

## When to use it

He et al. evaluated on MovieLens 1M (6,040 users, 3,706 items) and Pinterest (55,187 users, 9,916 items) with one held-out item per user ranked against 100 sampled items, measuring HR@10 and NDCG@10, and reported that NeuMF did better than their baselines.

Rendle, Krichene, Zhang and Anderson (2020) reran these experiments on the same splits and metrics, with a dot product model with biases trained by the same log loss and negative sampling, and with the hyperparameters chosen on a validation set. In their experiments the dot product beat the MLP on all data sets, metrics and embedding sizes they tried ($d$ from 16 to 192), and beat NeuMF except at one point, HR on MovieLens with $d = 192$, where the pre-trained NeuMF was ahead. They also reported that the NCF numbers had been selected at the best iteration on the test set, as found by Ferrari Dacrema, Boglio, Cremonesi and Jannach (2019), and that an MLP trained only to fit a dot product still had a large error, which grew with the embedding size (their Section 4 and Figure 3). These are measurements on two data sets with one protocol. They do not prove that a dot product is always better, but they show that a tuned dot product is the baseline to beat. Use NCF when there is a reason to expect that the plain dot product is the wrong form, and compare it with a well-tuned matrix factorization.

## Pitfalls

- **A weak baseline.** The main lesson of the 2020 rerun: a matrix factorization baseline with poorly chosen hyperparameters makes any new model look good.
- **Selecting on the test set.** Picking the best epoch by the test metric inflates the result. Use a validation split.
- **Sampled metrics.** Ranking a held-out item among 100 sampled items is a different measure from ranking it among all items, so results under the two protocols are not comparable.
- **L2 on GMF.** The weights $h$ can grow while the embeddings shrink, so an L2 penalty on the embeddings alone does not limit the model; Rendle et al. (2020, Section 3.3.3) make this point.
- **Serving cost.** A model that needs a forward pass per item does not scale to large catalogs without a candidate generation stage.
- **ReLU at zero.** A finite-difference gradient check fails near a unit that is exactly at 0. Check at random points, as the tests do.

## Implementations

## History

He et al. presented NCF at WWW 2017, and it became a common baseline for neural recommenders. In 2019, Ferrari Dacrema, Cremonesi, Jannach and coauthors studied the reproducibility of neural recommendation papers, including NCF, and compared them with simple, well-tuned baselines. Rendle, Krichene, Zhang and Anderson revisited the NCF experiments at RecSys 2020 and found that a tuned dot product beat the learned similarity in their experiments, that an MLP has difficulty learning a dot product, and that MLP scores are costly to serve.

## References
