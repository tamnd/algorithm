---
tag: GDMYGR
kind: algorithm
slug: dense-passage-retrieval
name: Dense passage retrieval
aliases:
- DPR
area: information-retrieval-and-ai-reasoning/ranking-models
level: research
summary: Trains a question encoder and a passage encoder with in-batch negatives so that relevant passages are nearest neighbors by inner product.
solves: [learning-to-rank]
model: word-ram
complexity:
  vars: {B: the number of questions in a batch, m: the number of passages in a batch, k: the vector dimension, N: the number of passages in the collection}
  time: {per_batch: O(B m k), per_query: O(N k + N log N)}
  space: {extra: O(B m + N k)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2020
  people: [Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, Wen-tau Yih]
  note: Karpukhin and colleagues showed in 2020 that a dual encoder trained only on question-passage pairs, with in-batch negatives and one BM25 hard negative, retrieves passages for open-domain questions better than BM25 on several benchmarks (a measured result).
prereqs: [dual-encoder-retrieval, cross-entropy-loss]
see_also: [maximum-inner-product-search, hnsw, bm25, colbert, cross-encoder-reranking, retrieval-augmented-generation, listnet, softmax-regression]
sources:
  - paper: doi:10.18653/v1/2020.emnlp-main.550
    title: Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen and Wen-tau Yih, Dense passage retrieval for open-domain question answering, Proceedings of EMNLP 2020
    locator: pp. 6769-6781; Section 3.1 and Equation (1) (the similarity of the [CLS] vectors of two BERT encoders, dimension 768), Section 3.2 and Equation (2) (the negative log-likelihood of the positive passage, with in-batch negatives and BM25 hard negatives), Section 5.4 (indexing with FAISS HNSW), Table 2 (retrieval accuracy)
---

Dense passage retrieval (DPR) trains the two encoders of a [dual encoder](/dual-encoder-retrieval/) for open-domain question answering, so that the passage that answers a question has the largest inner product with it among millions of passages. The training loss is a softmax [cross-entropy](/cross-entropy-loss/) over one positive passage and many negatives, and its main trick is to reuse the positive passages of the other questions in a batch as negatives, which costs no extra encoding. The dual-encoder page describes the scoring model and its limits; this page gives the training objective, its gradient, the in-batch construction, and the exact top-$k$ step that the index approximates. Search over the vectors is the topic of [maximum inner product search](/maximum-inner-product-search/) and [HNSW](/hnsw/). The two BERT encoders and the quality of the retrieval they learn are outside the code and the proofs here.

## In plain words

We want a search system that turns every question and every passage into a list of numbers, so that a good answer passage lands close to its question. We train it on questions with known answer passages. A training batch holds many questions and their answer passages. For each question, its own passage is the right one, and the passages of all the other questions serve as wrong ones, for free. We also add one hard wrong passage per question, a passage that shares many words with the question but does not answer it. Training pushes each question toward its right passage and away from the wrong ones. Later, search is just finding the closest stored passages.

## The problem

A batch has $B$ questions with vectors $q_1, \ldots, q_B$ and $m \ge B$ passages with vectors $c_1, \ldots, c_m \in \mathbb R^k$, produced by the question encoder $E_Q$ and the passage encoder $E_P$. Passage $c_i$ is the positive of question $i$ for $i \le B$; the other passages are negatives for it: the positives of the other questions and any extra hard negatives, such as the top BM25 passage that does not contain the answer. With $S_{ij} = q_i \cdot c_j$, the loss is

$$L = \frac{1}{B} \sum_{i=1}^{B} -\log \frac{e^{S_{ii}}}{\sum_{j=1}^{m} e^{S_{ij}}}.$$

This is Equation (2) of Karpukhin et al. (2020), averaged over the batch. After training, a question $q$ is answered by the $K$ passages of the collection with the largest $q \cdot c$.

## The algorithm

```pseudo id=main
DPR-BATCH(Q, C, B)              -- Q: B × k question vectors, C: m × k passage vectors
L1  S ← Q Cᵀ
L2  p_i ← softmax(S_i) for each row i
L3  L ← (1/B) Σ_i -log p_ii
L4  G ← (P - [I | 0]) / B        -- P has the rows p_i, [I | 0] marks the positives
L5  ∇_Q ← G C,  ∇_C ← Gᵀ Q
L6  return ∇_Q and ∇_C, to be back-propagated into E_Q and E_P
L7  SEARCH(q, K): return the K passages with the largest q · c, ties to the smaller id
```

Lines L1 to L6 are the code. The back-propagation into the encoders after line L6, and the update of their weights, are outside it. The paper trains with batch size 128 and one BM25 negative per question, so each question sees 255 negatives. Line L7 is exact search; the paper builds a FAISS HNSW index over the passage vectors to answer faster.

## Example

Take $B = 2$ questions $q_1 = (1, 0)$ and $q_2 = (0, 1)$, their positives $c_1 = (2, 0)$ and $c_2 = (1, 1)$, and one hard negative each: $c_3 = (0, -1)$ for $q_1$ and $c_4 = (1, 2)$ for $q_2$. All four passages are shared negatives for both questions.

| | $c_1$ | $c_2$ | $c_3$ | $c_4$ |
|---|---|---|---|---|
| $S_{1j}$ | 2 | 1 | 0 | 1 |
| $p_{1j}$ | **0.5344** | 0.1966 | 0.0723 | 0.1966 |
| $S_{2j}$ | 0 | 1 | -1 | 2 |
| $p_{2j}$ | 0.0871 | **0.2369** | 0.0321 | 0.6439 |

The loss is $\frac{1}{2}(-\ln 0.5344 - \ln 0.2369) = 1.0334$. Without the hard negatives, with only $c_1$ and $c_2$, it is $0.3133$: the hard negative $c_4$ outscores the positive of $q_2$ and dominates the loss. The gradients are

$$\nabla_{q_1} = (-0.2689, 0.2588), \quad \nabla_{q_2} = (0.0275, 0.2463),$$

$$\nabla_{c_1} = (-0.2328, 0.0436), \quad \nabla_{c_2} = (0.0983, -0.3816), \quad \nabla_{c_3} = (0.0362, 0.0160), \quad \nabla_{c_4} = (0.0983, 0.3220).$$

A step against them moves $q_2$ and $c_2$ toward each other and $c_4$ away from $q_2$. At search time, $q_2$ would retrieve $c_4$ first with these vectors, which is what the loss penalizes.

## Correctness

The proof in proofs/correctness.md shows:

- **Gradient.** $\partial L / \partial q_i = \frac{1}{B} \sum_j (p_{ij} - [j = i]) c_j$ and $\partial L / \partial c_j = \frac{1}{B} \sum_i (p_{ij} - [j = i]) q_i$, which is line L5. The tests check every coordinate against central finite differences on random batches.
- **Bounds.** $L > 0$, each row term is $\log m$ when its scores are equal, and it tends to 0 only when the positive's margin over every negative grows without bound. With $m = B$, each question has $B - 1$ negatives; with one hard negative each, $2B - 1$.
- **Exact search.** Line L7 returns the $K$ passages of largest inner product, ties to the smaller id. Approximate indexes are compared against this.

Nothing here shows that training makes the answer passage of a new question its nearest neighbor; that is measured. Karpukhin et al. (2020), Table 2, report a top-20 retrieval accuracy of 78.4 for DPR against 59.1 for BM25 on the Natural Questions test set, as a measurement.

## Complexity

One batch costs $O(B m k)$ for $S$ and the same for the two gradients, plus the encoder passes for $B + m$ inputs, which dominate in practice. The in-batch negatives add $B - 1$ negatives per question for no extra encoder pass, since their vectors are already computed. The extra space is $O(B m)$ for the scores. Search by exact scan costs $O(N k)$ per query, plus $O(N \log K)$ to keep the top $K$ with a heap, and the index stores $N k$ numbers; for 21 million passages of dimension 768 that is about 16 billion numbers, which is why the index uses compression or graph search.

## Properties

- **Shift invariant per row.** Adding a constant to all scores of one question does not change the loss.
- **Hard negatives matter.** In the example, one hard negative raises the loss from 0.3133 to 1.0334, because it is the strongest competitor of the positive. The paper's main training setting adds one BM25 negative per question to the in-batch negatives.
- **Batch size is the number of negatives.** Larger batches give more negatives per question at the same encoding cost per question, which ties the quality of training to the memory of the hardware.
- **Same similarity at training and search.** The loss uses the inner product, so the search must use the inner product, not the cosine.
- **Passages are fixed once encoded.** A change of $E_P$ requires re-encoding the whole collection.

## Variants and improvements

- **Mined hard negatives.** Use negatives retrieved by the current model, refreshed during training.
- **Distillation from a reranker.** Train the dual encoder to match the scores of a [cross-encoder](/cross-encoder-reranking/) instead of hard labels.
- **Multi-vector scoring.** [ColBERT](/colbert/) keeps one vector per token and scores by late interaction.
- **Joint training with a reader or generator.** [Retrieval-augmented generation](/retrieval-augmented-generation/) fine-tunes the question encoder of DPR through the generator's likelihood, with the passage encoder frozen.
- **Hybrid with BM25.** Combine dense and lexical scores, for example by a linear combination or [reciprocal rank fusion](/reciprocal-rank-fusion/).

## When to use it

Use DPR as the first stage when queries are questions in natural language and the answers are in passages that may not share the question's words. It needs training pairs of questions and positive passages, and a GPU to encode the collection. When the queries are keyword-like or the domain has no training data, BM25 is a strong baseline that the paper itself uses for hard negatives. For the final order of a short list, a cross-encoder is more accurate, at a cost per pair.

## Pitfalls

- **Positives counted as negatives.** If two questions in a batch share a positive passage, line L4 treats it as a negative for one of them. Remove such duplicates when building batches.
- **Softmax over the wrong axis.** Line L2 normalizes each question's row over the passages. Normalizing over questions gives a different loss and, in line L5, different gradients.
- **Overflow.** Line L2 must subtract the row maximum before exponentiating.
- **Approximate search mistaken for the model.** Recall measured with an approximate index in place of line L7 mixes the errors of the index with those of the encoders. Report the exact-search result when comparing models.
- **False hard negatives.** A BM25 passage that does not contain the answer string may still answer the question. Such negatives push the model away from correct passages.

## Implementations

## History

Neural dual encoders for retrieval go back at least to DSSM by Huang et al. (2013), trained on click data. Karpukhin et al. (2020) showed that two BERT encoders, fine-tuned only on question and passage pairs with in-batch negatives and one BM25 negative, beat BM25 on several open-domain question answering benchmarks in their measurements. DPR became the standard dense retriever of the following years and the retriever of the original retrieval-augmented generation model.

## References
