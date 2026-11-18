---
tag: 510HA2
kind: technique
slug: subword-regularization
name: Subword regularization
aliases:
- stochastic subword segmentation
area: natural-language-and-speech/tokenization-and-text-normalization
level: advanced
summary: Sample a different segmentation of each training sentence from a unigram tokenization model, so the network sees many splits and grows robust.
prereqs: [unigram-language-model-tokenization, subword-tokenization, word-lattice]
see_also: [bpe-dropout, data-augmentation, dropout, regularization, machine-translation, forward-backward-algorithm, k-shortest-paths, ancestral-sampling]
sources:
  - paper: doi:10.18653/v1/P18-1007
    title: Taku Kudo, Subword regularization, Improving neural network translation models with multiple subword candidates, ACL 2018, pages 66 to 75
    locator: Section 2.1 (on-the-fly sampling, Equations 3 and 4), Section 2.2 (one-best and n-best decoding), Section 3.3 (l-best sampling with the smoothing value alpha, and forward filtering backward sampling), Section 4 (the relation to data augmentation), Section 5.1 (the settings l = 64 with alpha = 0.1, and l = infinity with alpha = 0.2 or 0.5) and Section 5.2 (the BLEU gains)
  - paper: doi:10.18653/v1/2020.acl-main.170
    title: Ivan Provilkov, Dmitrii Emelianenko and Elena Voita, BPE-dropout, Simple and effective subword regularization, ACL 2020, pages 1882 to 1892
    locator: the abstract and Section 4 (subword regularization with the BPE merge table, compared with Kudo's method)
  - paper: doi:10.18653/v1/D18-2012
    title: Taku Kudo and John Richardson, SentencePiece, A simple and language independent subword tokenizer and detokenizer for neural text processing, EMNLP 2018 System Demonstrations, pages 66 to 71
    locator: the library that implements the unigram model used for sampling
---

Subword regularization trains a model on random segmentations of its input instead of one fixed segmentation. Each time a sentence is used in training, its words are split into subword pieces by sampling from a probabilistic tokenizer, so the same word reaches the model as different rows of pieces. Kudo (2018) introduced it with the [unigram language model tokenizer](/unigram-language-model-tokenization/) and showed gains in [machine translation](/machine-translation/). At test time the model gets the single most probable segmentation, or a few of them.

## In plain words

A tokenizer that always cuts a word the same way hides the fact that the word could be cut in other ways. A model trained on one cut never learns that "un" + "related" and "unrel" + "ated" spell the same word, so it is fragile when a rare or misspelled word is cut in an unusual way.

Subword regularization picks a fresh cut for each word every time the model sees it during training. Likely cuts come up often, unlikely ones less often, and a dial sets how adventurous the picks are. The model learns from many cuts of the same text, which acts like extra training data. When the model is used, the picking stops and the best cut is used.

## When it applies

It needs a tokenizer that defines a probability for every segmentation of a word, such as the unigram language model, or a random procedure that gives many segmentations, such as [BPE-dropout](/bpe-dropout/). It needs a model that is trained by many passes over the data, so that each sentence is segmented many times. It helps most when the data is small or the test text differs from the training text. Kudo applies it to both the source and the target side of a translation model, and it needs no change to the model, only to the data it reads.

## The template

Let a model give each piece $w$ a probability $p(w)$, and let $P(s) = \prod_{w \in s} p(w)$ for a segmentation $s$ of a word $x$. For a smoothing value $a > 0$, sample $s$ with probability

$$Q(s) = \frac{P(s)^a}{\sum_t P(t)^a},$$

where the sum runs over the candidates $t$. A small $a$ makes the law flatter, and a large $a$ moves it to the [Viterbi](/viterbi-algorithm/) segmentation. Kudo uses one sample per sentence per update ($k = 1$ in his Equation 4); over many updates this approximates training on the marginal likelihood over all segmentations.

There are two ways to draw $s$. The first takes the $l$ best segmentations and draws one of them:

```pseudo id=nbest
SAMPLE-NBEST(x, p, a, l)
N1  T ← the l best segmentations of x, with their log probabilities
N2  Z ← the log-add over t in T of a · log P(t)
N3  draw r uniform in [0, 1)
N4  return the first t of T where the running sum of exp(a · log P(t) - Z) exceeds r
```

The second draws from all segmentations, exactly, by forward filtering and backward sampling on the [word lattice](/word-lattice/). Positions are fenceposts $0, \ldots, n$, and the piece $x[i{:}j]$ is the edge from $i$ to $j$. The forward pass runs in the LOG semiring (log probabilities, plus = log-add, times = +) with the edge weights $a \log p(w)$, natural logs:

```pseudo id=main
SAMPLE-LATTICE(x, p, a)
S1  alpha ← the forward values of x with the edge weights a · log p(w)
S2  if alpha[n] = -∞ then fail: x has no segmentation
S3  pieces ← empty; j ← n
S4  while j > 0
S5      give each start i of a piece x[i:j] the weight exp(alpha[i] + a · log p(x[i:j]) - alpha[j])
S6      draw a start i with these weights
S7      put x[i:j] in front of pieces; j ← i
S8  return pieces
```

The weights of line S5 sum to 1, and the product of the weights along the drawn path telescopes to $P(s)^a / \sum_t P(t)^a$; proofs/correctness.md gives the proof. One sample costs as much as one forward pass, linear in the size of the lattice.

Kudo decodes either from the best segmentation (one-best decoding) or from the $n$ best, and then keeps the translation $y$ with the best score $\log P(y \mid x) / |y|^{\lambda}$, where $\lambda$ is a length penalty tuned on development data (n-best decoding).

## Classic examples

**The word "hugs".** Take the model h 0.1, u 0.1, g 0.1, s 0.15, hu 0.1, ug 0.15, hug 0.2, gs 0.05 and ugs 0.05 of the unigram page. The word has 7 segmentations. The law $Q$ for three values of $a$:

| segmentation | a = 1 | a = 0.5 | a = 2 |
|---|---|---|---|
| hug s | 0.6757 | 0.3978 | 0.9399 |
| h ugs | 0.1126 | 0.1624 | 0.0261 |
| hu gs | 0.1126 | 0.1624 | 0.0261 |
| h ug s | 0.0507 | 0.1089 | 0.0053 |
| hu g s | 0.0338 | 0.0890 | 0.0023 |
| h u gs | 0.0113 | 0.0514 | 0.0003 |
| h u g s | 0.0034 | 0.0281 | 0.00002 |

With $a = 1$ the law is the posterior $P(s) / P(x)$, and $P(\text{hugs}) = 0.0444$. With $l = 3$ and $a = 1$, the three best are hug s, h ugs and hu gs, with the probabilities 0.75, 0.125 and 0.125: the rest of the law is cut off. In a measurement with 10,000 draws by the lattice sampler at $a = 0.5$ and the seed 0, hug s came up 3,999 times, close to the 3,978 that the law predicts.

**Translation.** In Kudo's experiments (Section 5.1), the samplers used $l = 64$ with $a = 0.1$, and $l = \infty$ (the lattice sampler) with $a = 0.2$ on the IWSLT data and $0.5$ on the others. Subword regularization raised BLEU by 1 to 2 points on all language pairs but one (Section 5.2), and by about 2 points on out-of-domain data (Section 5.3). These are measurements on those tasks.

## Variations

- **BPE-dropout.** Provilkov, Emelianenko and Voita (2020) get random segmentations from a BPE merge table by skipping merges at random. It needs no unigram model, and they report better BLEU than Kudo's sampling on their tasks.
- **l-best against the lattice.** The $l$-best list needs a [k-shortest-paths](/k-shortest-paths/) search; Kudo uses the Forward-DP Backward-A* algorithm of Nagata (1994). The lattice sampler needs only the forward values and is exact.
- **n-best decoding.** Kudo found that n-best decoding helps only for models trained with subword regularization (Section 5.2).
- **Other noise.** It is a form of [data augmentation](/data-augmentation/) and is related in spirit to [dropout](/dropout/): the noise is in the input, not in the network.

## Pitfalls

- **Sampling at test time.** Inference should use the best segmentation, or n-best decoding; a random segmentation at test time makes the output random.
- **Underflow.** For a long sentence, $P(s)$ underflows in floating point. Work in log space, with log-add for the sums, as the code does through nlslog.
- **The l-best list is not the full law.** Sampling from the $l$ best renormalizes over the list, so segmentations outside the list are never drawn.
- **The value of a.** With $a$ too small, implausible segmentations such as single characters become frequent; with $a$ too large, the method is plain Viterbi segmentation.
- **The cost per epoch.** Segmentation must be done again at each update, so it cannot be cached as for a fixed tokenizer.

## Exercises

1. Show that with $a = 1$ the lattice sampler draws $s$ with the posterior probability $P(s) / P(x)$ of the unigram model.
2. Show that as $a$ grows without bound, $Q$ puts all its mass on the Viterbi segmentations (spread over them if there are ties).
3. For the word "hugs" above, compute the forward values with $a = 0.5$, shown as $\exp(\alpha[j])$, and check that they are 1, 0.316228, 0.416228, 0.701311 and 0.435399.
4. Explain why the weights of line S5 sum to 1 at every position $j$ with $\alpha[j] > -\infty$.
5. Give a model and a word for which the 2-best sampler can never return the segmentation of largest probability among those with three pieces.

## References
