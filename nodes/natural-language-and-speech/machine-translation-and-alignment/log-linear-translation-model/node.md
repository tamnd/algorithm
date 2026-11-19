---
tag: DK58JF
kind: model
slug: log-linear-translation-model
name: Log-linear translation model
aliases:
- Och-Ney log-linear model
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: Score a translation by a weighted sum of feature functions, such as language and phrase model log-probabilities and penalties.
history:
  year: 2002
  people: [Franz Josef Och, Hermann Ney]
  note: Och and Ney (2002) replaced the noisy channel decision rule by a direct maximum entropy model of the translation given the source, with the channel and language model log-probabilities as two of its features. Och (2003) then tuned the weights for the translation metric directly, and the model became the frame of almost all statistical translation systems.
prereqs: [machine-translation, softmax-regression]
see_also: [noisy-channel-translation-model, phrase-based-translation-model, minimum-error-rate-training, hierarchical-phrase-based-translation, logistic-regression, structured-perceptron, minimum-risk-training, maximum-likelihood-estimation]
sources:
  - paper: doi:10.3115/1073083.1073133
    title: Franz Josef Och and Hermann Ney, Discriminative training and maximum entropy models for statistical machine translation, ACL 2002, pages 295 to 302
    locator: the direct maximum entropy model of the translation, the noisy channel model as a special case, and the training of the weights on n-best lists
  - paper: "Franz Josef Och, Minimum error rate training in statistical machine translation, ACL 2003, pages 160 to 167, ACL Anthology P03-1021"
    title: Och 2003
    locator: the log-linear decision rule and the training of its weights for the error measure instead of the likelihood
  - paper: "Adam L. Berger, Stephen A. Della Pietra and Vincent J. Della Pietra, A maximum entropy approach to natural language processing, Computational Linguistics 22(1), 1996, pages 39 to 71"
    title: Berger, Della Pietra and Della Pietra 1996
    locator: the exponential form of the conditional maximum entropy model and its training
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 9 (discriminative training)"
---

The log-linear translation model scores a candidate translation $e$ of a source sentence $f$ by a weighted sum $\sum_q \lambda_q h_q(e, f)$ of feature functions, and outputs the candidate with the highest score. The features are usually log-probabilities of sub-models, such as an [n-gram language model](/n-gram-language-model/) and phrase translation tables in both directions, together with counts such as the number of words and phrases. Read as a probability, $p(e \mid f) \propto \exp \sum_q \lambda_q h_q(e, f)$ is a conditional maximum entropy model, the same form as [softmax regression](/softmax-regression/) over the candidate translations. The [noisy channel model](/noisy-channel-translation-model/) is the special case with two features and both weights equal to 1.

## The machine

**Direction and notation.** Translation runs from the source $f = f_1 \ldots f_m$ to the target $e = e_1 \ldots e_l$. Logs are natural.

**Features.** A feature function $h_q(e, d, f)$, $q = 1, \ldots, Q$, maps a source sentence, a target sentence and a hidden derivation $d$ (for example the segmentation into phrases and their order) to a real number. Typical features are $\ln p_{\mathrm{LM}}(e)$, the sum of the log phrase translation probabilities $\ln \phi(\bar f \mid \bar e)$ and $\ln \phi(\bar e \mid \bar f)$, the lexical weights, a distortion cost, the word count $l$ and the phrase count. Any function can be a feature; it need not be a probability.

**The model.** With weights $\lambda = (\lambda_1, \ldots, \lambda_Q)$,

$$p_\lambda(e, d \mid f) = \frac{\exp \sum_{q=1}^{Q} \lambda_q h_q(e, d, f)}{\sum_{e', d'} \exp \sum_{q=1}^{Q} \lambda_q h_q(e', d', f)},$$

and the decision rule, with the usual max over derivations, is

$$\hat e = e\Big(\arg\max_{e, d} \sum_{q=1}^{Q} \lambda_q h_q(e, d, f)\Big).$$

The normalizer is the same for all candidates of one source sentence, so the decoder never computes it.

**Training.** The sub-models behind the features are trained first, each on its own data: the language model on target text, the phrase tables on a word-aligned [parallel corpus](/parallel-corpus/). Then only the $Q$ weights, usually between 5 and 20 of them, are tuned on a small held-out set of sentence pairs. Och and Ney (2002) maximized the conditional likelihood of the reference translations on $n$-best lists, as in maximum entropy training. Och (2003) tuned the weights for the translation metric itself with [minimum error rate training](/minimum-error-rate-training/), which became the usual method.

**Example.** For f = das haus ist klein, take three candidates with the features $h_1 = \ln p_{\mathrm{LM}}(e)$, $h_2 = \ln p(f \mid e)$ and $h_3 = l$:

| candidate | $h_1$ | $h_2$ | $h_3$ | score with $\lambda = (1, 1, 0)$ | score with $\lambda = (1, 1, 0.5)$ |
|---|---|---|---|---|---|
| the house is small | $-4.0$ | $-2.0$ | 4 | $-6.0$ | $-4.0$ |
| the house is little | $-5.0$ | $-1.5$ | 4 | $-6.5$ | $-4.5$ |
| the house | $-2.0$ | $-3.5$ | 2 | $-5.5$ | $-4.5$ |

With the noisy channel weights $(1, 1, 0)$ the short candidate "the house" wins, because the language model gives a higher probability to fewer words. A word bonus $\lambda_3 = 0.5$ corrects this, and "the house is small" wins. As probabilities over these three candidates, the second weights give $e^{-4.0} / (e^{-4.0} + 2 e^{-4.5}) = 0.452$ for the winner and $0.274$ for each of the others. With $\lambda = (0.3, 1, 0.5)$ the language model counts less, and "the house is little" wins with the score $-1.0$ against $-1.2$.

## What it counts

The model counts a score per candidate and derivation, and it costs $Q$ multiplications and additions on top of the feature values. When every feature is a sum of local parts, for example one part per phrase or per target word, the score is also a sum of local parts, and a decoder can add it up step by step as it builds the derivation. This is what [stack decoding](/phrase-based-stack-decoding/) and chart decoding need. A feature that looks at the whole sentence at once can only be used to rescore an $n$-best list or a lattice.

Training the weights counts in passes over the held-out set. Each pass decodes every sentence to get an $n$-best list, which is the expensive part; the weight update on fixed $n$-best lists is cheap in comparison.

## Relation to other models

- **Noisy channel model.** With $h_1 = \ln p(e)$, $h_2 = \ln p(f \mid e)$ and $\lambda_1 = \lambda_2 = 1$, the decision rule is $\arg\max_e p(e) \, p(f \mid e)$, the [noisy channel](/noisy-channel-translation-model/) rule. The log-linear model frees the weights, which allows $p(e \mid f)$ in place of, or next to, $p(f \mid e)$, and allows features that are not probabilities.
- **Softmax regression.** Over a fixed candidate list, $p_\lambda(e \mid f)$ is [softmax regression](/softmax-regression/) in which each class, here each candidate, has its own feature vector and all classes share one weight vector. With two candidates it is [logistic regression](/logistic-regression/) on the difference of their feature vectors.
- **Phrase-based and hierarchical models.** The [phrase-based model](/phrase-based-translation-model/) and [Hiero](/hierarchical-phrase-based-translation/) are log-linear models with particular features and derivations.
- **Structured perceptron.** The [structured perceptron](/structured-perceptron/) and its relatives (MIRA, pairwise ranking) train the same weights with other loss functions and scale to many thousands of sparse features, where MERT does not.
- **Minimum risk training.** [Minimum risk training](/minimum-risk-training/) uses the probabilities of the model to minimize the expected loss, and it is used to train neural models as well.

## Known results in the model

- **The normalizer cancels (theorem).** The $\arg\max$ of $p_\lambda(e, d \mid f)$ over candidates equals the $\arg\max$ of the linear score, since $\exp$ is increasing and the normalizer does not depend on the candidate.
- **Scale does not matter (theorem).** Multiplying all weights by the same positive number does not change the output. So weight tuning can fix the scale, for example $\sum_q |\lambda_q| = 1$, and MERT searches only over directions.
- **Noisy channel inside the family (theorem).** Every noisy channel model is a log-linear model with two features and unit weights, so the best log-linear model on the training data is at least as good as the noisy channel model under the same criterion.
- **Convex training on n-best lists (theorem).** On fixed $n$-best lists, the conditional log-likelihood of the reference candidates is concave in $\lambda$, as for every maximum entropy model, so its maximum can be found by any convex method. The error count of MERT is not concave, and only local optima are guaranteed.
- **Better than the channel (measurement).** Och and Ney (2002) reported lower error rates than the noisy channel baseline on their test data, from the direct translation probability, from extra features, and from discriminative training of the weights.
- **Training for the metric (measurement).** Och (2003) found that weights tuned for the evaluation metric gave better scores on that metric than weights tuned for likelihood.

## References
