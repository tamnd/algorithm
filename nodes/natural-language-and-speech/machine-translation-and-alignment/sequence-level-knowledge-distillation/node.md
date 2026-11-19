---
tag: 6KDR4C
kind: technique
slug: sequence-level-knowledge-distillation
name: Sequence-level knowledge distillation
aliases:
- sequence-level distillation
area: natural-language-and-speech/machine-translation-and-alignment
level: advanced
summary: Train a small translation model on the beam search outputs of a large one, rather than on the gold targets.
history:
  year: 2016
  people: [Yoon Kim, Alexander M. Rush]
  note: Kim and Rush adapted knowledge distillation to sequence models at EMNLP 2016. Their student models ran 10 times faster than the teacher with little loss in BLEU, and the method later became the standard data preparation for non-autoregressive translation.
prereqs: [knowledge-distillation, encoder-decoder-model, beam-search]
see_also: [non-autoregressive-translation, back-translation, minimum-risk-training, cross-entropy-loss, greedy-decoding, bleu, transformer, teacher-forcing]
sources:
  - paper: doi:10.18653/v1/D16-1139
    title: Yoon Kim and Alexander M. Rush, Sequence-Level Knowledge Distillation, EMNLP 2016, pages 1317 to 1327
    locator: "word-level distillation, sequence-level distillation on the beam output of the teacher, and sequence-level interpolation; the abstract gives the speed-up of 10, the gains of 4.2 and 1.7 BLEU with greedy decoding and beam search, and 13 times fewer parameters with pruning at a cost of 0.4 BLEU"
  - paper: arxiv:1711.02281
    title: Jiatao Gu, James Bradbury, Caiming Xiong, Victor O. K. Li and Richard Socher, Non-Autoregressive Neural Machine Translation, ICLR 2018
    locator: "abstract (knowledge distillation as one of the three parts of the training of a non-autoregressive model)"
---

Sequence-level knowledge distillation trains a student translation model on the translations that a teacher model produces, instead of on the human references. First a large teacher is trained as usual. Then the teacher translates every source sentence of the training set with [beam search](/beam-search/), and the student trains by maximum likelihood on these pairs of source and teacher output. It is the sequence form of [knowledge distillation](/knowledge-distillation/), which matches the student to the teacher's distribution one prediction at a time. Kim and Rush (2016) introduced it, and it is now the usual way to prepare data for [non-autoregressive translation](/non-autoregressive-translation/).

## In plain words

A big translation model is accurate but slow. A small model is fast but learns less well from the raw data.

Human translations of the same kind of sentence vary a lot. One translator writes one thing, another writes something else. A small model wastes its capacity trying to cover all of that variety.

So let the big model translate the training data first. Its outputs are more regular: similar sentences get similar translations. Train the small model to copy these outputs. The small model now learns one consistent way to translate, which is easier to learn, and it gets close to the big model's quality.

## When it applies

- You have a trained teacher model and want a smaller or faster student for the same task, such as a model with fewer layers or a [non-autoregressive](/non-autoregressive-translation/) model.
- The output is a sequence, and the teacher can produce a good output by beam search.
- You can afford one pass of beam search over the training set with the teacher.
- The student is trained by maximum likelihood, so changing the targets is all it takes; the student's architecture and loss stay the same.

## The template

Let $q(y \mid x)$ be the teacher and $p(y \mid x; \theta)$ the student, both autoregressive over target tokens from a vocabulary $\mathcal{V}$.

**Word-level distillation.** At each target position $j$, with the reference prefix $y_{<j}$, the student matches the teacher's next-token distribution:

$$\mathcal{L}_{\mathrm{word}} = -\sum_{j=1}^{J} \sum_{k \in \mathcal{V}} q(y_j = k \mid y_{<j}, x) \log p(y_j = k \mid y_{<j}, x; \theta).$$

**Sequence-level distillation.** The ideal target is the teacher's whole sequence distribution:

$$\mathcal{L}_{\mathrm{seq}} = -\sum_{y} q(y \mid x) \log p(y \mid x; \theta) \approx -\log p(\hat y \mid x; \theta), \qquad \hat y = \mathrm{BEAM}(q, x).$$

The sum is over all target sequences, which is exponential in the length. The approximation replaces $q$ by a point mass on the beam output $\hat y$ of the teacher. In practice:

1. Train the teacher on the parallel data $D = \{(x, y^*)\}$.
2. For each $(x, y^*) \in D$, run beam search with the teacher to get $\hat y$.
3. Train the student by maximum likelihood on $\{(x, \hat y)\}$, optionally mixed with $D$ or with the word-level loss.

**Sequence-level interpolation.** Kim and Rush also choose, among the $K$ beam outputs of the teacher, the one closest to the reference by a similarity such as sentence [BLEU](/bleu/), and train on it. This keeps the target near both the teacher's mode and the reference.

The exact $\mathcal{L}_{\mathrm{seq}}$ is the cross-entropy from the teacher's sequence distribution to the student's, so minimizing it over all students minimizes $\mathrm{KL}(q \,\|\, p)$ (a theorem, since the entropy of $q$ does not depend on $\theta$). The point-mass approximation with the beam output is a heuristic: it assumes that the teacher's distribution is concentrated near its mode.

## Classic examples

- **Smaller translation models.** Kim and Rush (2016) distilled a large LSTM teacher into a smaller student. Their best student ran 10 times faster than the teacher with little loss in BLEU, and it beat a baseline of the same size trained without distillation by 4.2 BLEU with greedy decoding and 1.7 BLEU with beam search. Weight pruning on top gave a student with 13 times fewer parameters than the teacher for a loss of 0.4 BLEU (measurements, from the abstract).
- **Greedy decoding is enough.** The same paper found that the distilled students, and even the teacher trained on its own outputs, need beam search much less: [greedy decoding](/greedy-decoding/) gets close to the beam result (a measurement). The student has learned a sharper distribution around one output.
- **Non-autoregressive translation.** Gu et al. (2018) trained their parallel decoder on the outputs of an autoregressive teacher and named distillation as one of the three parts of their method. Most later [non-autoregressive](/non-autoregressive-translation/) models do the same.

## Variations

- **Word-level distillation** keeps the reference prefix and matches the teacher's soft distribution at each step. It needs the teacher's distributions at training time, which are large ($|\mathcal{V}|$ numbers per token).
- **Mixed losses.** Combine the distillation loss with the loss on the references with a weight, or combine word-level and sequence-level distillation.
- **Several teachers.** Use an ensemble as the teacher, or the outputs of several teachers, to give more varied targets.
- **Forward translation of monolingual text.** Run the teacher on extra source text that has no reference. This is self-training, the mirror of [back-translation](/back-translation/), which makes synthetic sources instead of synthetic targets.
- **Sampling instead of beam search.** Train on samples from the teacher to approximate the full sum better. This trades the regularity of the targets for coverage.

## Pitfalls

- **Teacher errors become targets.** The student copies the teacher's mistakes, and it cannot be better than its targets on the cases where the teacher is wrong. Check the student against the references, not against the teacher.
- **Loss of diversity.** Distilled data has less lexical variety than real data, so rare words and constructions appear less often. This is part of why it helps small models and part of why it can hurt on rare phenomena.
- **Cost of decoding.** Step 2 runs beam search over the full training set, which can take as long as several epochs of training. Do it once and store the result.
- **Evaluation with the same metric.** Sequence-level interpolation selects targets by sentence BLEU. Gains measured with BLEU alone can overstate the improvement; check with a second metric such as [chrF](/chrf/) or [COMET](/comet-metric/).
- **Comparing with an undistilled baseline.** Distillation also changes the data. When comparing two architectures, train both on the same distilled data, or the comparison mixes two effects.

## Exercises

1. Show that $-\sum_y q(y \mid x) \log p(y \mid x) = H(q) + \mathrm{KL}(q \,\|\, p)$, and conclude that the exact sequence-level loss is minimized by $p = q$. *Hint:* add and subtract $\sum_y q \log q$.
2. Why does word-level distillation not give the sequence-level loss? *Answer:* it conditions on the reference prefix at each step, so it matches $q(y_j \mid y^*_{<j}, x)$, not the teacher's distribution over its own prefixes.
3. A teacher gives two translations of a source the probabilities 0.4 and 0.35, and the rest is spread thin. What does the beam approximation keep, and what does it lose? *Answer:* it keeps the first translation as the target and drops the second, so the student learns one mode instead of two.

## References
