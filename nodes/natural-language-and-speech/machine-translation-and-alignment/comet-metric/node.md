---
tag: MVK1Y2
kind: model
slug: comet-metric
name: COMET
aliases:
- crosslingual optimized metric for evaluation of translation
area: natural-language-and-speech/machine-translation-and-alignment
level: research
summary: A learned translation metric that predicts human scores from multilingual encoder embeddings of the source, hypothesis and reference.
history:
  year: 2020
  people: [Ricardo Rei, Craig Stewart, Ana C. Farinha, Alon Lavie]
  note: Rei, Stewart, Farinha and Lavie of Unbabel presented COMET at EMNLP 2020, with three models trained on HTER, MQM and WMT relative rankings. Later releases of the framework use other encoders and training data.
prereqs: [bleu, bert, sentence-embedding]
see_also: [chrf, translation-edit-rate, bertscore, transformer, mean-squared-error, minimum-bayes-risk-decoding, minimum-risk-training, rouge]
sources:
  - paper: doi:10.18653/v1/2020.emnlp-main.213
    title: Ricardo Rei, Craig Stewart, Ana C. Farinha and Alon Lavie, COMET - A Neural Framework for MT Evaluation, EMNLP 2020, pages 2685 to 2702
    locator: "Section 2 (the cross-lingual encoder, XLM-RoBERTa base, the layer-wise attention pooling, the Estimator model and the Translation Ranking model, equations 1 to 6), Section 3 (the QT21, DARR and MQM corpora), Section 4 (the training setup and the Kendall tau-like formulation of WMT 2019) and Table 1 (correlations with English as the source)"
---

COMET is a learned metric for machine translation. A pretrained multilingual [transformer](/transformer/) encoder turns the source sentence, the translation hypothesis and a human reference into sentence vectors, and a small network on top maps them to a quality score. The network is trained to predict human judgments of translation quality, so the score is learned, not defined by a formula such as [BLEU](/bleu/) or [chrF](/chrf/). Rei, Stewart, Farinha and Lavie (2020) introduced the framework with two architectures: an Estimator that regresses on a human score, and a Translation Ranking model that learns from pairs of a better and a worse hypothesis. This page describes the models of that paper, which use XLM-RoBERTa base as the encoder: COMET-HTER, COMET-MQM and COMET-RANK. Each released version of COMET is a different trained model, and its scores have no fixed scale shared with the other versions.

## The machine

**Inputs.** A source segment $s$, a hypothesis $h$ and a reference $r$, each a sequence of subword tokens. The segments are usually single sentences.

**Encoder.** A pretrained cross-lingual encoder, XLM-RoBERTa base in the 2020 paper. For a segment $x = x_0, \ldots, x_n$, it gives an embedding $e_j^{(\ell)} \in \mathbb{R}^d$ for each token $x_j$ and each layer $\ell = 0, 1, \ldots, k$. The same encoder, with the same weights, encodes $s$, $h$ and $r$ separately.

**Pooling.** A layer-wise attention mixes the layers into one vector per token,

$$e_{x_j} = \mu\, E_{x_j}^\top \alpha, \qquad E_{x_j} = [e_j^{(0)}, e_j^{(1)}, \ldots, e_j^{(k)}], \qquad \alpha = \mathrm{softmax}([\alpha^{(0)}, \ldots, \alpha^{(k)}]),$$

with a trainable scale $\mu$ and trainable layer weights $\alpha^{(\ell)}$. During training, layer dropout sets a weight $\alpha^{(\ell)}$ to $-\infty$ with some probability. An average over the tokens of the segment then gives one sentence vector in $\mathbb{R}^d$: $\mathbf{s}$, $\mathbf{h}$ and $\mathbf{r}$.

**Estimator model.** The features are

$$\mathbf{x} = [\mathbf{h};\, \mathbf{r};\, \mathbf{h} \odot \mathbf{s};\, \mathbf{h} \odot \mathbf{r};\, |\mathbf{h} - \mathbf{s}|;\, |\mathbf{h} - \mathbf{r}|] \in \mathbb{R}^{6d},$$

where $\odot$ is the product and $|\cdot|$ the absolute value, coordinate by coordinate. The source vector itself is left out; it enters only through the product and the difference with $\mathbf{h}$. A feed-forward regressor maps $\mathbf{x}$ to one real number $\hat y$. Training minimizes the [mean squared error](/mean-squared-error/) between $\hat y$ and the human score $y$ of the segment.

**Translation Ranking model.** The input is a tuple $(s, h^+, h^-, r)$ in which human judges preferred $h^+$ to $h^-$. With the Euclidean distance $d(\cdot, \cdot)$ between sentence vectors and a margin $\epsilon$, the loss is the triplet margin loss

$$L = \max\{0, d(\mathbf{s}, \mathbf{h}^+) - d(\mathbf{s}, \mathbf{h}^-) + \epsilon\} + \max\{0, d(\mathbf{r}, \mathbf{h}^+) - d(\mathbf{r}, \mathbf{h}^-) + \epsilon\}.$$

At test time the model gets one hypothesis $\hat h$ and returns

$$f = \frac{2\, d(\mathbf{r}, \hat{\mathbf{h}})\, d(\mathbf{s}, \hat{\mathbf{h}})}{d(\mathbf{r}, \hat{\mathbf{h}}) + d(\mathbf{s}, \hat{\mathbf{h}})}, \qquad \mathrm{score} = \frac{1}{1 + f},$$

the harmonic mean of the two distances, turned into a similarity.

**Training data of the 2020 models.** COMET-HTER: the QT21 corpus, about 173K tuples in four pairs with the [HTER](/translation-edit-rate/) of each hypothesis against its post-edit. COMET-MQM: an internal corpus of about 12K segments with MQM scores, from English into 12 languages. COMET-RANK: relative rankings (DARR) derived from the direct assessments of the WMT news tasks of 2017 and 2018.

Standing assumptions: the encoder covers the languages of the input; the score of a segment depends only on its own source, hypothesis and reference; and the human judgments in the training data define what "quality" means for the model.

## What it counts

COMET computes a segment-level score for each hypothesis. A system-level score is usually the mean of the segment scores over a test set, which is a convention of the tools, not part of the model.

The direction and the range depend on the model. For COMET-RANK, higher is better and the score lies in $(0, 1]$, with 1 only when the hypothesis vector equals the source or reference vector. For COMET-MQM, higher is better; its training targets are MQM scores divided by 100 and cut at 0, but the regressor output is not bounded. For COMET-HTER, the model predicts an edit rate, so lower is better. Later released models are trained on other data and have their own scales. A COMET score therefore means something only together with the name of the model that produced it, and only in comparison with other scores from the same model.

The cost of one evaluation is three passes of the encoder, one for each of $s$, $h$ and $r$, plus the pooling and the regressor. A transformer encoder with $k$ layers of size $d$ costs $\Theta(k (n^2 d + n d^2))$ for a segment of $n$ tokens, which dominates. When many hypotheses share a source and a reference, the vectors $\mathbf{s}$ and $\mathbf{r}$ can be computed once.

## Relation to other models

- **String metrics.** [BLEU](/bleu/), [chrF](/chrf/) and [TER](/translation-edit-rate/) compare the hypothesis with the reference by matching strings. They need no training, and their scores are defined by formulas, so they mean the same thing everywhere. COMET compares vectors, uses the source, and is trained.
- **BERTScore.** [BERTScore](/bertscore/) also uses contextual embeddings, but it matches tokens greedily by cosine similarity and is not trained on human judgments. COMET pools whole segments and learns the mapping to a score.
- **Quality estimation.** A model with the same structure but no reference input predicts quality from the source and the hypothesis alone. The 2020 paper keeps the reference.
- **Use in decoding and training.** A learned metric can serve as the utility in [minimum Bayes risk decoding](/minimum-bayes-risk-decoding/) or as the loss in [minimum risk training](/minimum-risk-training/). The model then optimizes toward what the metric rewards, including its errors.

## Known results in the model

- **Correlation with human rankings.** On the WMT 2019 DARR data with English as the source, the best of the three 2020 models had a higher Kendall tau-like correlation than BLEU, chrF, YiSi-1 and BERTScore on each of the eight language pairs, and COMET-RANK was the best of the three on seven of them. For English to German, the correlation was 0.248 for BLEU, 0.321 for chrF and 0.427 for COMET-RANK (Table 1, measurements). The tau-like value is $(\mathrm{Concordant} - \mathrm{Discordant}) / (\mathrm{Concordant} + \mathrm{Discordant})$ over the pairs of a better and a worse hypothesis.
- **Small training sets can work.** COMET-MQM, trained on only about 12K segments with English always as the source, was roughly on par with COMET-HTER on most pairs with English as the source (a measurement from the paper).
- **The source matters.** Rei et al. report gains in correlation from the features that use the source, $\mathbf{h} \odot \mathbf{s}$ and $|\mathbf{h} - \mathbf{s}|$ (a measurement).
- **No guarantee.** There is no theorem that relates a COMET score to translation quality. The score is a prediction from a trained network, and it can be wrong in ways that a string metric is not: for example, a fluent hypothesis with a wrong number or name may still get a high score. Its correlation with humans is a measurement on specific test sets.
- **No fixed scale.** Different versions of COMET use different encoders, data and targets, so their scores are not comparable. Report the model version with every score, and do not compare a COMET score with a BLEU score or with a score from another COMET model.

## References
