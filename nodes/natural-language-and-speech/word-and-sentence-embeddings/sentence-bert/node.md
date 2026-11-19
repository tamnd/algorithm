---
tag: S38M6T
kind: model
slug: sentence-bert
name: "Sentence-BERT"
aliases:
- SBERT
area: natural-language-and-speech/word-and-sentence-embeddings
level: research
summary: A siamese BERT encoder with mean pooling, fine-tuned on sentence pairs so that the cosine of two pooled vectors scores semantic similarity.
history:
  year: 2019
  people: [Nils Reimers, Iryna Gurevych]
  note: Reimers and Gurevych at TU Darmstadt fine-tuned BERT in a siamese setup on natural language inference data, so that sentence vectors can be compared by cosine instead of running BERT on every pair.
prereqs: [bert, sentence-embedding]
see_also: [simcse, smooth-inverse-frequency-embedding, dense-passage-retrieval, natural-language-inference, cosine-similarity, hnsw, cross-entropy-loss, paragraph-vector]
sources:
  - paper: doi:10.18653/v1/D19-1410
    title: Nils Reimers and Iryna Gurevych, Sentence-BERT, Sentence embeddings using siamese BERT-networks, EMNLP-IJCNLP 2019, pages 3982 to 3992
    locator: Section 3 (pooling, the classification, regression and triplet objectives, the training setup), Section 4 (the STS results), Section 6 (the ablation of pooling and features), Section 7 (the speed of computation)
  - paper: doi:10.18653/v1/N19-1423
    title: Jacob Devlin, Ming-Wei Chang, Kenton Lee and Kristina Toutanova, BERT, Pre-training of deep bidirectional transformers for language understanding, NAACL-HLT 2019, pages 4171 to 4186
    locator: the sentence pair input with the separator token, used by the cross-encoder
  - paper: doi:10.18653/v1/D17-1070
    title: Alexis Conneau, Douwe Kiela, Holger Schwenk, Loïc Barrault and Antoine Bordes, Supervised learning of universal sentence representations from natural language inference data, EMNLP 2017, pages 670 to 680
    locator: the InferSent encoder and the classifier on (u, v, |u - v|, u * v) trained on SNLI
  - paper: doi:10.18653/v1/S17-2001
    title: Daniel Cer, Mona Diab, Eneko Agirre, Iñigo Lopez-Gazpio and Lucia Specia, SemEval-2017 Task 1, Semantic textual similarity multilingual and crosslingual focused evaluation, SemEval-2017, pages 1 to 14
    locator: the STS benchmark data set of sentence pairs with scores from 0 to 5
---

Sentence-BERT (SBERT) turns a [BERT](/bert/) encoder into a [sentence embedding](/sentence-embedding/) model. The same encoder reads each of two sentences on its own, the mean of its output token vectors is the sentence vector, and the encoder is fine-tuned on labeled pairs, first on [natural language inference](/natural-language-inference/) data, so that the [cosine](/cosine-similarity/) of two vectors scores how similar the sentences are. For $n$ sentences this needs $n$ encoder passes, where BERT as a cross-encoder needs one pass for each of the $n(n-1)/2$ pairs. Reimers and Gurevych 2019 measured that finding the most similar pair among 10,000 sentences falls from about 65 hours to about 5 seconds.

## The machine

**Encoder.** A pretrained BERT (or RoBERTa) encoder with $L$ layers and width $d$ ($L = 12$, $d = 768$ for the base model) reads the [WordPiece](/wordpiece/) tokens of one sentence, $T$ tokens with the special tokens, and returns $H \in \mathbb{R}^{T \times d}$.

**Pooling.** The sentence vector $u \in \mathbb{R}^d$ is one of: MEAN, the mean of the rows of $H$ over the real tokens (the default); MAX, the maximum of each coordinate over the tokens; or CLS, the row of the first token.

**Siamese setup.** Two sentences $a$ and $b$ go through the same encoder with the same weights, one at a time, and give $u$ and $v$. The pair is never put into one input.

**Classification objective.** For a task with $k$ labels, such as entailment, neutral and contradiction,

$$o = \operatorname{softmax}(W_t [u; v; |u - v|]), \qquad W_t \in \mathbb{R}^{k \times 3d},$$

trained with the [cross-entropy loss](/cross-entropy-loss/). The head $W_t$ is used only in training.

**Regression objective.** The score is $\cos(u, v)$, trained with the mean squared error against a gold similarity.

**Triplet objective.** For an anchor $a$, a positive $p$ and a negative $n$, the loss is $\max(\|s_a - s_p\| - \|s_a - s_n\| + \epsilon, 0)$ with the Euclidean norm and $\epsilon = 1$.

**Training.** The NLI models were trained on SNLI (570,000 pairs) and MultiNLI (430,000 pairs) with the 3-way classification objective, a batch size of 16, [Adam](/adam/) with the learning rate $2 \cdot 10^{-5}$, a linear warmup over 10% of the training data, and one epoch. A second stage on the STS benchmark with the regression objective gives the models fine-tuned on STS.

**Use.** At test time each text is encoded once, and two texts are compared by $\cos(u, v)$. For search, the vectors go into an index for [nearest neighbor search](/nearest-neighbor-search/), such as [HNSW](/hnsw/).

## What it counts

The network computes a function from a sentence to a vector in $\mathbb{R}^d$, and the model scores a pair by the cosine of two such vectors.

- **One encoding.** A transformer encoder of $L$ layers on $T$ tokens costs $O(L (T d^2 + T^2 d))$; the pooling costs $O(T d)$.
- **All pairs.** For $n$ sentences, SBERT needs $n$ encodings and $n(n-1)/2$ cosines of cost $O(d)$ each. A cross-encoder needs $n(n-1)/2$ encodings of length about $2T$. For $n = 10{,}000$ that is about 50 million BERT passes, which the paper estimates at about 65 hours on a V100 GPU, against about 5 seconds for SBERT.
- **Search.** With the vectors stored, a query costs one encoding plus a search over $n$ vectors, $O(n d)$ exactly or less with an approximate index.
- **Speed (measurement).** In sentences per second, average GloVe vectors ran at 6469 on a CPU. InferSent ran at 137 on a CPU and 1876 on a GPU, and SBERT-base at 44 and 1378. With batches of sentences of similar length, SBERT-base ran at 83 and 2042.

## Relation to other models

- **BERT as a cross-encoder.** [BERT](/bert/) reads the pair "[CLS] a [SEP] b [SEP]" and scores it with a head on the first token. The two sentences attend to each other in every layer, which usually gives better pair scores, but no vector exists for a single sentence.
- **Plain BERT vectors.** Mean pooling or the CLS vector of a BERT encoder that is not fine-tuned gives poor similarity scores (see below). The fine-tuning, not the pooling, makes the vectors useful.
- **InferSent.** Conneau et al. 2017 trained a BiLSTM encoder with max pooling on SNLI with a classifier on $(u, v, |u - v|, u * v)$. SBERT uses the same training idea with a pretrained transformer.
- **SimCSE.** [SimCSE](/simcse/) trains the same kind of encoder with a contrastive loss, either on two dropout copies of one sentence or on NLI pairs with contradictions as hard negatives.
- **Dense retrieval.** [Dense passage retrieval](/dense-passage-retrieval/) uses the same bi-encoder idea for questions and passages, with two separate encoders and the dot product.
- **Weighted averages.** [SIF](/smooth-inverse-frequency-embedding/) and averaged [GloVe](/glove/) vectors need no network pass and no labeled data, and are much faster on a CPU.

## Known results in the model

- **Embeddings make all-pairs scoring linear in the encoder passes (theorem).** Since the score of a pair is a fixed function of the two vectors, the $n$ vectors are computed once and reused in all $n(n-1)/2$ scores. With unit vectors, $\|u - v\|^2 = 2 - 2 \cos(u, v)$, so the most similar text by cosine is the nearest by Euclidean distance, and Euclidean and inner product indexes apply.
- **The score is symmetric (theorem).** $\cos(u, v) = \cos(v, u)$, so SBERT cannot model a direction in a pair; a cross-encoder can.
- **STS without STS training (measurement).** As the Spearman rank correlation times 100, averaged over seven STS data sets, average GloVe vectors gave 61.32, the BERT CLS vector 29.19, mean-pooled BERT vectors 54.81, and SBERT-NLI-base 74.89.
- **Pooling and features (measurement).** On the STS benchmark development set, MEAN pooling gave 80.78 when the model was trained on NLI with the classification objective and 87.44 when it was trained on the STS benchmark with the regression objective. MAX gave 79.07 and 69.92, and CLS gave 79.80 and 86.62. With MEAN pooling and the classification objective, the features $(u, v, |u - v|)$ gave 80.78, and adding $u * v$ gave 80.44. The term $|u - v|$ mattered most.
- **Transfer (measurement).** On the SentEval classification tasks, SBERT vectors with a logistic regression classifier did better than InferSent and the Universal Sentence Encoder on most tasks.

## References
