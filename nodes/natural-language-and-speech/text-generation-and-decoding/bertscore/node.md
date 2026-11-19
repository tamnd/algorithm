---
tag: T124HA
kind: algorithm
slug: bertscore
name: BERTScore
aliases:
- BERT score
area: natural-language-and-speech/text-generation-and-decoding
level: research
summary: Score a candidate text against a reference by greedy matching of their contextual token embeddings by cosine, as precision, recall and F1.
model: word-ram
complexity:
  vars: {n: the number of reference tokens, m: the number of candidate tokens, d: the embedding width}
  time: {worst: "O(n m d)"}
  space: {extra: "O(n m)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2020
  people: [Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Q. Weinberger, Yoav Artzi]
  note: The authors, at Cornell University, posted BERTScore on arXiv in 2019 and published it at ICLR 2020, with a Python package that became a common second metric next to BLEU and ROUGE.
prereqs: [bert, cosine-similarity, precision-and-recall]
see_also: [rouge, bleu, comet-metric, word-movers-distance, colbert, tf-idf, assignment-problem, sentence-bert]
sources:
  - paper: arxiv:1904.09675
    title: Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Q. Weinberger and Yoav Artzi, BERTScore, Evaluating Text Generation with BERT, ICLR 2020
    locator: "Section 3 (token representation, cosine similarity, the recall, precision and F1 formulas, importance weighting by idf, baseline rescaling), Section 4 and Section 5 (the experiments on WMT16 to WMT18, COCO 2015 and PAWS), Appendix C (greedy and optimal matching)"
---

BERTScore compares a candidate text with a reference text through their contextual token embeddings, the vectors that a pretrained network such as [BERT](/bert/) gives to each token in its sentence. Each reference token is matched to the most similar candidate token by [cosine similarity](/cosine-similarity/), and the mean of these best similarities is the recall. Each candidate token is matched to the most similar reference token, and the mean is the precision. F1 is their harmonic mean. Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Weinberger and Yoav Artzi published it at ICLR 2020. Higher is better. The raw scores lie in $[-1, 1]$, and in practice in a narrow band near the top; a rescaling with a baseline spreads them out. The score is computed per sentence pair, and a system score is the mean over the test set. The computation from the embeddings is exact; that the score agrees with human judgments is a measurement.

## In plain words

[BLEU](/bleu/) and [ROUGE](/rouge/) count words and n-grams that occur in both texts. They give no credit when the candidate says "the economy grew" and the reference says "the economy expanded".

BERTScore gives each word a vector that depends on the word and on the words around it. Similar meanings give vectors that point in similar directions. For each word of the reference, find the candidate word that is closest in meaning, and take how close it is. The mean over the reference words tells how much of the reference the candidate covers. Do the same the other way round to see how much of the candidate is supported by the reference.

Rare words carry more meaning than words like "the". An optional weight gives each token its idf, so that matching a rare word counts more.

## The problem

The input is a reference with token embeddings $x_1, \ldots, x_n$ and a candidate with token embeddings $\hat x_1, \ldots, \hat x_m$, all in $\mathbb{R}^d$, and optional token weights. Without weights (Section 3 of the paper),

$$R_{\mathrm{BERT}} = \frac{1}{n}\sum_{i=1}^{n} \max_{j} x_i^{\mathsf T} \hat x_j, \qquad P_{\mathrm{BERT}} = \frac{1}{m}\sum_{j=1}^{m} \max_{i} x_i^{\mathsf T} \hat x_j, \qquad F_{\mathrm{BERT}} = 2\,\frac{P_{\mathrm{BERT}} \cdot R_{\mathrm{BERT}}}{P_{\mathrm{BERT}} + R_{\mathrm{BERT}}},$$

where the vectors are normalized to length 1, so that each inner product is a cosine. With importance weights, recall is $\sum_i \mathrm{idf}(x_i) \max_j x_i^{\mathsf T}\hat x_j / \sum_i \mathrm{idf}(x_i)$, and precision uses the idf of the candidate tokens in the same way. The idf of a word piece $w$ is computed over the $M$ references of the test set,

$$\mathrm{idf}(w) = -\log \frac{1}{M}\sum_{k=1}^{M} \mathbb{I}[w \in x^{(k)}],$$

and the paper applies plus-one smoothing for word pieces that occur in no reference. Baseline rescaling replaces a score $s$ by $(s - b)/(1 - b)$, where $b$ is the mean score of random sentence pairs.

## The algorithm

```pseudo id=main
BERTSCORE(x, x̂, w, ŵ, b)      ▷ x: n reference vectors; x̂: m candidate vectors
L1  normalize every x_i and every x̂_j to length 1
L2  S_ij ← x_i · x̂_j for all i, j       ▷ the n by m cosine matrix
L3  r_i ← max_j S_ij for each i          ▷ best match of each reference token
L4  p_j ← max_i S_ij for each j          ▷ best match of each candidate token
L5  R ← Σ_i w_i r_i / Σ_i w_i
L6  P ← Σ_j ŵ_j p_j / Σ_j ŵ_j
L7  F ← 2 P R / (P + R)
L8  optionally s ← (s - b_s) / (1 - b_s) for s in P, R, F
L9  return P, R, F
```

The embeddings come from one layer of a pretrained network, run on the reference and on the candidate separately. With all weights equal to 1, lines L5 and L6 are plain means. Line L3 and line L4 are the greedy matching: each token takes its best partner, and one token can be the best partner of several tokens on the other side. The paper computes the baseline $b$ for each model and language from one million random pairs of Common Crawl sentences, and rescales $P$, $R$ and $F$ in the same way.

## Example

Take two reference tokens and three candidate tokens in $\mathbb{R}^2$, with the vectors already given by the network: $x_1 = (1, 0)$, $x_2 = (0, 2)$, and $\hat x_1 = (3, 0)$, $\hat x_2 = (0.6, 0.8)$, $\hat x_3 = (0.8, -0.6)$. After normalization, the cosine matrix is

| | $\hat x_1$ | $\hat x_2$ | $\hat x_3$ | best |
|---|---|---|---|---|
| $x_1$ | 1 | 0.6 | 0.8 | 1 |
| $x_2$ | 0 | 0.8 | -0.6 | 0.8 |
| best | 1 | 0.8 | 0.8 | |

Recall is $(1 + 0.8)/2 = 0.9$, precision is $(1 + 0.8 + 0.8)/3 = 0.8667$, and $F = 2 \cdot 0.9 \cdot 0.8667 / 1.7667 = 0.8830$. Both $\hat x_2$ and $\hat x_3$ take $x_1$ or $x_2$ as their best match, and $\hat x_3$ matches $x_1$ although $\hat x_1$ matches $x_1$ better: greedy matching does not use each token once. With idf weights 1 and 3 on the reference tokens, recall becomes $(1 \cdot 1 + 3 \cdot 0.8)/4 = 0.85$. With a recall baseline of 0.8, the rescaled recall is $(0.9 - 0.8)/0.2 = 0.5$.

## Correctness

The following are theorems, with full proofs in the proofs file. After normalization, each entry of $S$ is the cosine of two tokens, so lines L3 to L7 compute the formulas of the paper exactly, and $P$ and $R$ lie in $[-1, 1]$. A candidate equal to the reference scores $P = R = F = 1$. The scores do not change when a vector is scaled by a positive number or when the tokens are reordered, and exchanging candidate and reference exchanges $P$ and $R$. Greedy recall is never below the score of the best one-to-one matching, and the two are equal when the best partners are distinct. $F$ lies between $P$ and $R$ when both are positive. Rescaling is an increasing affine map, so it keeps the order of candidates and the correlation with human judgments.

Whether BERTScore measures quality is a question of measurement, not of proof. The paper reports higher correlation with human judgments than BLEU and other metrics on the WMT16 to WMT18 metric tasks and on image captions from COCO 2015, and more robustness on the adversarial paraphrases of PAWS.

## Complexity

Line L1 takes $O((n + m)d)$ time. Line L2 is a matrix product, with $O(nmd)$ time and $O(nm)$ space. Lines L3 to L7 read the matrix once, in $O(nm)$ time. So one pair takes $O(nmd)$ time. The idf table takes $O(L)$ expected time for $L$ reference tokens in total. In practice the forward pass of the network costs far more than the matching: for a transformer with $\ell$ layers, it is about $O(\ell (n^2 d + n d^2))$ per sentence.

## Properties

- **Direction and range.** Higher is better. Raw scores are in $[-1, 1]$; with BERT-like models most pairs score in a band near the top, which is why the paper adds rescaling.
- **Sentence level.** The score is defined for one candidate and one reference. A system score is the mean over the sentences.
- **Soft matching.** Paraphrases and synonyms get partial credit, which n-gram metrics do not give.
- **Order is seen only through the embeddings.** The matching itself ignores token order. Contextual embeddings encode some of it, so a shuffled candidate gets a lower score, but not as low as with n-gram metrics.
- **Depends on the model.** Scores from different networks, layers or versions are not comparable. The paper selects the layer for each model on WMT16 data.
- **Not symmetric in P and R.** Recall measures coverage of the reference, and precision measures support of the candidate.

## Variants and improvements

- **One-to-one matching.** Appendix C of the paper compares greedy matching with the best one-to-one (optimal transport) matching, as in [word mover's distance](/word-movers-distance/) and MoverScore. Greedy matching is faster and needs no solver for the [assignment problem](/assignment-problem/).
- **Idf weights.** The weights of the problem section. The paper treats them as optional.
- **Multilingual models.** The same algorithm with a multilingual encoder scores texts in other languages.
- **MaxSim in retrieval.** [ColBERT](/colbert/) scores a document for a query with the same sum of maximum similarities over the query tokens, which is the unnormalized recall.
- **Trained metrics.** [COMET](/comet-metric/) and BLEURT train a network on human judgments instead of using a fixed similarity.

## When to use it

Use BERTScore to compare generation systems where paraphrases are common, such as summarization, captioning and translation, next to an n-gram metric such as ROUGE or BLEU. Report the model, the layer, the use of idf, the rescaling and the package version, because each changes the numbers. Do not use it to compare scores computed with different models. For a check of factual consistency or of fluency it is not enough: a candidate with a wrong number or a negation can still score high.

## Pitfalls

- **Unnormalized vectors.** The inner product of raw vectors is not a cosine. Line L1 is required.
- **Narrow range.** Raw scores of 0.85 and 0.90 can be far apart in quality. Compare rescaled scores, or compare systems on the same data.
- **Special tokens.** Tokens such as [CLS] and [SEP] are in every sentence and match each other perfectly. Decide whether they take part in the matching, and say so.
- **Idf from the test set.** The idf weights are computed from the references being scored, so they change with the test set.
- **Division by zero.** If $P + R = 0$, $F$ is undefined. The code returns 0.
- **Word pieces, not words.** The tokens are the pieces of the tokenizer of the model, such as [WordPiece](/wordpiece/), so a long word adds several tokens to the means.

## Implementations

The code takes the token embeddings of the network as given (an $n \times d$ and an $m \times d$ list of vectors) and implements the normalization, the greedy matching, the idf weights and the rescaling; it does not run or train a network.

## History

Earlier metrics for text generation compared surface forms: BLEU (2002) and ROUGE (2004) count n-grams, and METEOR (2005) adds stems and synonyms from WordNet. Metrics based on word embeddings, such as the word mover's distance (2015) and the greedy matching of word vectors used in dialogue evaluation, used static vectors. BERTScore used the contextual vectors of BERT and its successors, which had appeared in 2018 and 2019. The paper tested 12 models; for English it recommended a large RoBERTa model. Trained metrics such as BLEURT (2020) and COMET (2020) followed in the same year.

## References
