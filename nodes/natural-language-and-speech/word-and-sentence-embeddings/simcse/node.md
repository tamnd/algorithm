---
tag: 355PND
kind: algorithm
slug: simcse
name: SimCSE
aliases:
- simple contrastive sentence embeddings
area: natural-language-and-speech/word-and-sentence-embeddings
level: research
summary: Train sentence encoders by a contrastive loss in which the positive for a sentence is the same sentence passed again under a new dropout mask.
solves: [sentence-embedding]
model: real-ram
complexity:
  vars: {n: the number of sentences in the batch, d: the width of the sentence vectors}
  time: {worst: "O(n^2 d)"}
  space: {extra: "O(n^2 + n d)"}
properties: {deterministic: false, exact: false, online: false, recursive: false, supervised: false}
history:
  year: 2021
  people: [Tianyu Gao, Xingcheng Yao, Danqi Chen]
  note: Gao, Yao and Chen showed that dropout noise alone is enough to make the positive pairs of a contrastive loss for sentence vectors, and added a supervised form that uses natural language inference pairs.
prereqs: [sentence-embedding, dropout, cosine-similarity]
see_also: [sentence-bert, cross-entropy-loss, log-sum-exp-trick, softmax-regression, bert, dense-passage-retrieval, negative-sampling, natural-language-inference]
sources:
  - paper: doi:10.18653/v1/2021.emnlp-main.552
    title: Tianyu Gao, Xingcheng Yao and Danqi Chen, SimCSE, simple contrastive learning of sentence embeddings, Proceedings of EMNLP 2021, pages 6894 to 6910
    locator: equation 1 (the unsupervised loss), equation 5 (the loss with hard negatives), the comparison of dropout with discrete augmentations, and the analysis by alignment and uniformity
  - paper: "Tongzhou Wang and Phillip Isola, Understanding contrastive representation learning through alignment and uniformity on the hypersphere, ICML 2020"
    title: Wang and Isola 2020
    locator: the definitions of the alignment and uniformity measures
  - paper: "Aaron van den Oord, Yazhe Li and Oriol Vinyals, Representation learning with contrastive predictive coding, arXiv:1807.03748, 2018"
    title: van den Oord, Li and Vinyals 2018
    locator: the InfoNCE loss
  - paper: doi:10.18653/v1/N19-1423
    title: Jacob Devlin, Ming-Wei Chang, Kenton Lee and Kristina Toutanova, BERT, pre-training of deep bidirectional transformers for language understanding, NAACL-HLT 2019
    locator: the encoder that SimCSE fine-tunes, and its dropout of 0.1
---

SimCSE fine-tunes a pretrained encoder such as [BERT](/bert/) so that its sentence vectors solve the [sentence embedding](/sentence-embedding/) problem well. It passes each sentence of a batch through the encoder twice. [Dropout](/dropout/) picks a new random mask each time, so the two vectors differ a little, and the loss asks each vector to be closer in [cosine similarity](/cosine-similarity/) to its own twin than to the vectors of the other sentences of the batch. The loss is a [cross-entropy](/cross-entropy-loss/) over a softmax of scaled cosines, known as InfoNCE; the value of the method for downstream tasks is a measurement, not a theorem.

## In plain words

A model that turns sentences into vectors should put sentences with the same meaning close together and spread all the other sentences apart. Labeled pairs of paraphrases are expensive, so SimCSE makes its own pairs. It reads the same sentence twice, and each time it switches off a different random tenth of the network. The two results are almost the same, but not quite, so they make a natural pair. Then it plays a matching game inside each batch: for each sentence it must find its twin among all the second copies. The training makes this game easy to win. To win, the model must keep twins close and push different sentences away from each other, which is what a good sentence vector needs.

## The problem

The input of one training step is a batch of $N$ sentences $x_1, \ldots, x_N$ and an encoder $f$ with dropout. Let $h_i = f(x_i)$ under one dropout mask and $h^+_i = f(x_i)$ under a second, independent mask. In the supervised form, $h^+_i$ is the vector of a sentence that the premise $x_i$ entails, and a hard negative $h^-_i$ is the vector of a sentence that contradicts it. The output is the loss and its gradient with respect to every vector, which backpropagation then passes into the encoder.

With the temperature $\tau > 0$, the loss for sentence $i$ is

$$\ell_i = -\log \frac{e^{\cos(h_i, h^+_i)/\tau}}{\sum_{j=1}^{N} e^{\cos(h_i, h^+_j)/\tau} + \sum_{j=1}^{N} e^{\cos(h_i, h^-_j)/\tau}},$$

and the batch loss is the mean of the $\ell_i$. The second sum is absent in the unsupervised form. The other sentences of the batch serve as the negatives of sentence $i$, so no negative sampling step is needed.

## The algorithm

```pseudo id=main
SIMCSE-LOSS(h_1 .. h_N, h+_1 .. h+_N, τ, optional h-_1 .. h-_N)
L1  N ← the number of sentences in the batch
L2  for i ← 1 to N do
L3      z_ij ← cos(h_i, h+_j) / τ   for j ← 1 to N
L4      if hard negatives are given then z'_ij ← cos(h_i, h-_j) / τ   for j ← 1 to N
L5      lz_i ← LOG-SUM-EXP(z_i1 .. z_iN, z'_i1 .. z'_iN);  ℓ_i ← lz_i - z_ii
L6  loss ← (ℓ_1 + ... + ℓ_N) / N
L7  for each pair i, j do  p_ij ← exp(z_ij - lz_i)
L8      g ← (p_ij - [i = j]) / (N τ)
L9      ∇h_i ← ∇h_i + g · ∂cos(h_i, h+_j) / ∂h_i
L10     ∇h+_j ← ∇h+_j + g · ∂cos(h_i, h+_j) / ∂h+_j
L11 return loss, ∇h, ∇h+, ∇h-
```

Each row $i$ is a softmax classification over $N$ (or $2N$) candidates whose correct class is $j = i$. Line L5 uses the [log-sum-exp trick](/log-sum-exp-trick/), so line L7 never takes the exponential of a positive number. A hard negative adds the same two updates with $g' = p'_{ij} / (N \tau)$, where $p'_{ij} = \exp(z'_{ij} - lz_i)$, and with no $[i = j]$ term, since it is never the correct class. The cosine gradient is $\partial \cos(a, b) / \partial a = b / (\|a\| \|b\|) - \cos(a, b)\, a / \|a\|^2$.

In training, line L1 runs on the encoder outputs of a batch that holds each sentence twice. The paper uses BERT or RoBERTa, the [CLS] vector with a small MLP on top during unsupervised training (the MLP is removed at test time), the standard dropout rate of 0.1 and $\tau = 0.05$.

## Example

Take $N = 2$ and vectors in two dimensions, written for this page: $h_1 = (1, 0)$, $h_2 = (0, 1)$, $h^+_1 = (1, 1)$ and $h^+_2 = (-1, 1)$, with $\tau = 0.5$ and no hard negatives. With $c = 1/\sqrt{2} = 0.7071$, the cosines are:

| | $h^+_1$ | $h^+_2$ |
| --- | --- | --- |
| $h_1$ | $c$ | $-c$ |
| $h_2$ | $c$ | $c$ |

Row 1 has the logits $(1.4142, -1.4142)$. The positive wins with $p_{11} = 0.9442$, and $\ell_1 = \log(1 + e^{-2.8284}) = 0.0574$. Row 2 has the logits $(1.4142, 1.4142)$: the twin is no closer than the other sentence, so $p_{21} = p_{22} = 0.5$ and $\ell_2 = \log 2 = 0.6931$. The batch loss is $0.3753$.

The gradient with respect to $h_2$ is $(0.7071, 0)$. A step against it moves $h_2$ toward negative $x$, which is toward its twin $h^+_2$ and away from $h^+_1$. The gradient with respect to $h_1$ is exactly 0 here: both cosine gradients at $h_1$ point along $(0, 1)$, and their weights $g_{11} = -0.0558$ and $g_{12} = 0.0558$ cancel. With $\tau = 0.05$ instead, $\ell_1$ falls to about $5 \times 10^{-13}$ while $\ell_2$ stays $\log 2$, so the loss is $0.3466$: a small temperature puts nearly all the weight on the rows that are still wrong.

## Correctness

Two exact statements hold, and the proof below gives both. First, lines L1 to L6 compute the loss of equations 1 and 5 of the paper: log-sum-exp is an identity, not an approximation. Second, lines L7 to L11 return its exact gradient. The derivative of $\ell_i$ with respect to the logit $z_{ij}$ is $p_{ij} - [i = j]$, as for any softmax cross-entropy, and the chain rule through $z_{ij} = \cos(h_i, h^+_j)/\tau$ gives lines L8 to L10. The tests compare this gradient with central differences.

Two more facts follow. Each $\ell_i$ is at least 0, and it is 0 only in the limit where the positive takes all the weight. Each gradient is orthogonal to its own vector, so the loss depends only on the directions of the vectors, not on their lengths.

That the trained vectors are good sentence vectors is not a theorem. It is a measurement, given below.

## Complexity

The model is the [real-RAM](/real-ram/). For the loss and the gradient, with the encoder outputs given:

- **Logits.** Lines L2 to L4 compute $N^2$ cosines (or $2N^2$), each in $O(d)$ time: $O(N^2 d)$.
- **Gradient.** Lines L7 to L10 do $O(d)$ work for each pair: $O(N^2 d)$.
- **Space.** $O(N^2)$ for the logits and $O(N d)$ for the gradients.

In training, the two forward passes of the encoder and the backward pass dominate this cost. Each sentence goes through the encoder twice, so a step of unsupervised SimCSE costs about twice a plain fine-tuning step on the same batch. The training time itself is a measurement on given hardware.

## Properties

- **Unsupervised form.** It needs only raw sentences. The paper trains on $10^6$ sentences from English Wikipedia.
- **In-batch negatives.** The number of negatives per sentence is $N - 1$ (or $2N - 1$ with hard negatives). It grows with the batch at no extra encoder cost.
- **Scale invariance.** The loss uses only cosines, so it ignores the length of each vector.
- **Temperature.** A small $\tau$ sharpens the softmax and puts the weight on the hardest negatives. The paper reports $\tau = 0.05$ as the best of the values it tried, a measurement.
- **Alignment and uniformity.** With the measures of Wang and Isola 2020, the alignment is the mean of $\|f(x) - f(x^+)\|^2$ over positive pairs, and the uniformity is $\log$ of the mean of $e^{-2\|f(x) - f(y)\|^2}$ over all pairs, both on unit vectors. The paper measures that dropout noise keeps the alignment good while training makes the uniformity better. It also argues, through a limit with many negatives, that the loss flattens the singular value spectrum of the embedding matrix and so works against [anisotropy](/contextual-word-embedding/).

## Variants and improvements

- **Supervised SimCSE.** The positive is an entailment hypothesis and the hard negative is a contradiction hypothesis of the same premise, taken from the SNLI and MultiNLI data sets of [natural language inference](/natural-language-inference/), about 314,000 triples. This is equation 5 of the paper.
- **Discrete augmentations.** Cropping, word deletion, synonym replacement and masked-word replacement make the second view instead of dropout. On the STS-B development set the paper measures all of them below dropout alone.
- **Symmetric loss.** SimCLR and many later papers add the same loss with the roles of $h$ and $h^+$ swapped. SimCSE uses one direction.
- **Later variants.** DiffCSE (Chuang et al. 2022) adds a replaced-token detection task, and ESimCSE (Wu et al. 2022) repeats words to change the length of the second view and keeps a queue of earlier batches as extra negatives.
- **Retrieval.** The same in-batch softmax trains the question and passage encoders of [dense passage retrieval](/dense-passage-retrieval/), with labeled pairs instead of dropout pairs.

## When to use it

Use unsupervised SimCSE to adapt a pretrained encoder to sentence similarity when only unlabeled text in the target domain is at hand. Use the supervised form when entailment pairs or other paraphrase pairs exist. In the measurements of the paper, with BERT-base, the average Spearman correlation over seven semantic textual similarity tasks is 76.25 for the unsupervised form and 81.57 for the supervised form. Like [Sentence-BERT](/sentence-bert/), it gives one vector per sentence, so a search over $n$ sentences needs $n$ encoder passes. For a quick baseline with no training, an average of word vectors or [SIF](/smooth-inverse-frequency-embedding/) is cheaper.

## Pitfalls

- **The same mask twice.** If both passes use the same dropout mask, or if the encoder is in evaluation mode, $h_i = h^+_i$, and the loss only pushes sentences apart. The paper measures a large drop in quality for this case and for no dropout at all. Run both passes in training mode, as one batch of $2N$ sentences or as two calls.
- **Duplicate sentences in a batch.** If $x_i = x_j$, the vector $h^+_j$ is a false negative for row $i$. Remove duplicates before batching.
- **Plain exponentials.** With cosines in $[-1, 1]$ and $\tau = 0.05$, the largest logit is 20, which double precision holds. For $\tau$ below about $1/709$, or with dot products instead of cosines, $e^{z}$ overflows. Use line L5.
- **Mean and sum.** Line L6 takes the mean over the batch. A sum makes the gradient grow with $N$, which changes the right learning rate.
- **Small batches.** With few negatives the task is too easy and the uniformity gains are small. The batch size is a tuned value; the paper reports it with the learning rate for each model.

## Implementations

The code takes the two encoder outputs (and the hard negatives, when given) as given and implements the loss, its exact gradient and the alignment and uniformity measures; it does not train an encoder. It uses the log-sum-exp of the shared log-space helper of this area.

## History

The InfoNCE loss comes from contrastive predictive coding (van den Oord, Li and Vinyals 2018). SimCLR (Chen et al. 2020) used it with in-batch negatives on two augmented views of each image. For sentences, earlier work made the second view by editing the text or took it from labeled pairs. Gao, Yao and Chen 2021 showed at EMNLP that the dropout noise already in the encoder is enough to make the two views, and that it beats the discrete edits they tried. The paper became a standard baseline for sentence vectors, and many later methods change only the way they build the positive and negative pairs.

## References
