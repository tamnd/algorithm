---
tag: CAP0E5
kind: technique
slug: noise-contrastive-estimation
name: Noise-contrastive estimation
aliases:
- NCE
area: natural-language-and-speech/language-modeling
level: advanced
summary: "Fit an unnormalized model by logistic regression that tells data samples from noise samples. It avoids the full softmax over a large vocabulary."
prereqs: [logistic-regression, maximum-likelihood-estimation]
see_also: [negative-sampling, importance-sampling, hierarchical-softmax, neural-probabilistic-language-model, skip-gram-model, partition-function, contrastive-divergence, softmax-regression]
sources:
  - paper: "Michael Gutmann and Aapo Hyvärinen, Noise-contrastive estimation: a new estimation principle for unnormalized statistical models, Proceedings of AISTATS 2010, PMLR 9, pages 297 to 304"
    title: Gutmann and Hyvärinen 2010
    locator: the estimation principle, with the normalizing constant as a parameter
  - paper: "Michael U. Gutmann and Aapo Hyvärinen, Noise-contrastive estimation of unnormalized statistical models, with applications to natural image statistics, Journal of Machine Learning Research 13, 2012, pages 307 to 361"
    title: Gutmann and Hyvärinen 2012
    locator: "Section 2.1 (the objective, equations 3 to 7, with r_nu(u) = 1/(1 + nu exp(-u))), Section 2.2 (unnormalized models, ln p_m = ln p_m^0 + c), Section 2.3 (Theorem 1, the nonparametric optimum; Theorems 2 and 3, consistency and asymptotic normality), Section 2.4 (Corollaries 5 to 7 on the variance as nu grows and for p_n = p_d)"
  - paper: "Andriy Mnih and Yee Whye Teh, A fast and simple algorithm for training neural probabilistic language models, Proceedings of ICML 2012, pages 1751 to 1758, arXiv:1206.6426"
    title: Mnih and Teh 2012
    locator: "Section 3 (NCE for the log-bilinear language model; Section 3.1, the normalizers fixed to 1; Section 3.2, the speedup (cd + V)/(cd + k)), Tables 1 and 2 (Penn Treebank results for k = 1 to 100 and for unigram against uniform noise), and the MSR Sentence Completion Challenge"
  - paper: "Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado and Jeffrey Dean, Distributed representations of words and phrases and their compositionality, Advances in Neural Information Processing Systems 26 (NIPS 2013), arXiv:1310.4546"
    title: Mikolov, Sutskever, Chen, Corrado and Dean 2013
    locator: negative sampling, introduced as a simplification of NCE for the skip-gram model
---

Noise-contrastive estimation (NCE) fits a model whose probabilities are known only up to a normalizing constant. A [language model](/neural-probabilistic-language-model/) with a [softmax](/softmax-regression/) over a vocabulary of $|V|$ words is such a model: the score of one word is cheap, but its probability needs the sum of $|V|$ exponentials, the [partition function](/partition-function/), at every training step. NCE turns the fit into a binary classification. Mix the training data with $k$ times as many samples from a known noise distribution, and train the model, by [logistic regression](/logistic-regression/), to tell which samples are data. Gutmann and Hyvärinen (2010, 2012) proved that the best classifier gives the data density itself, normalized, with no sum over the space. Mnih and Teh (2012) used it to train neural language models over 10 times faster with the same perplexity.

## In plain words

You want a model that scores words, but turning scores into chances needs a sum over every word, which is slow.

So play a different game. Take a real next word from the text, and also draw a few fake words at random from a simple known list of chances, such as how common each word is. Ask the model to tell the real word from the fakes. It does this by comparing its own score of each word with how likely the word is as a fake.

A model that plays this game as well as possible must give each word its true chance in the text. And the game needs only the few words in hand, not the whole vocabulary.

## When it applies

Use it when a model has a cheap unnormalized score $\ln p_m^0(u; \theta)$ and an expensive normalizer, and you can sample from a noise distribution $p_n$ whose density you can evaluate. The noise must be positive wherever the data density is. The main uses are language models with a large output vocabulary, where the normalizer is a sum over $|V|$ words for each context, and models of continuous data whose normalizer is an integral with no closed form. When the output space is small, the plain softmax with maximum likelihood is simpler and as fast.

## The template

Let $x$ be a data sample, from the unknown density $p_d$, and let $\nu = k$ noise samples be drawn for each data sample from $p_n$. The model is $\ln p_m(u) = s_\theta(u)$, an unnormalized log density; it may include a learned constant $c$ in place of the normalizer, $\ln p_m = \ln p_m^0 + c$. The posterior probability that a sample $u$ came from the data, if the model were right, is

$$h(u) = \frac{p_m(u)}{p_m(u) + \nu\, p_n(u)} = \sigma\big(G(u) - \ln \nu\big), \qquad G(u) = \ln p_m(u) - \ln p_n(u),$$

with the logistic function $\sigma$. Gutmann and Hyvärinen write $h = r_\nu(G)$ with $r_\nu(u) = 1/(1 + \nu e^{-u})$. NCE maximizes the log-likelihood of the right labels,

$$J(\theta) = \mathbb{E}_{x \sim p_d} \ln h(x) + \nu\, \mathbb{E}_{y \sim p_n} \ln\big(1 - h(y)\big).$$

```pseudo id=main
NCE-TRAIN(score s_θ, data, noise p_n, k, rate η)
L1  repeat until the held-out loss stops falling:
L2      draw a data example u_0, with its context if the model has one
L3      draw k noise samples u_1, ..., u_k from p_n          ▷ hole: the noise distribution, positive where the data is
L4      Δ_j ← s_θ(u_j) - ln(k · p_n(u_j)) for j = 0, ..., k   ▷ hole: the model score, with or without a learned constant
L5      J ← ln σ(Δ_0) + Σ_{j=1..k} ln(1 - σ(Δ_j))
L6      θ ← θ + η ∇_θ J                                     ▷ hole: the optimizer
```

Line L4 is the log odds of "data" against "noise" for each sample. Line L5 needs $k + 1$ scores and no sum over the space. The gradient of line L5 is

$$\nabla_\theta J = \big(1 - \sigma(\Delta_0)\big) \nabla_\theta s_\theta(u_0) - \sum_{j=1}^{k} \sigma(\Delta_j)\, \nabla_\theta s_\theta(u_j).$$

**Why the optimum is the data density.** Treat $f(u) = \ln p_m(u)$ as free at each point, and write $q = e^{f(u)}$. The objective at $u$ is

$$p_d(u) \ln \frac{q}{q + \nu p_n(u)} + \nu p_n(u) \ln \frac{\nu p_n(u)}{q + \nu p_n(u)}.$$

Its derivative in $q$ is $\frac{\nu p_n}{q + \nu p_n} \big(\frac{p_d}{q} - 1\big)$, which is positive for $q < p_d$ and negative for $q > p_d$ when $p_n(u) > 0$. So the unique maximum is $q = p_d(u)$: the best model is the data density, and it is normalized although nothing forced it to be. This is Theorem 1 of Gutmann and Hyvärinen (2012). For a parametric family that contains $p_d$, they prove that the estimate is consistent and asymptotically normal (Theorems 2 and 3).

**A small check.** Let $p_d = (0.5, 0.25, 0.15, 0.1)$ on four symbols, $p_n$ uniform and $\nu = 2$. Gradient ascent on the exact objective with four free values $f(u)$ ends at $e^f = (0.5, 0.25, 0.15, 0.1)$, which sums to 1. Stochastic steps as in the template, with 200,000 data samples and seed 1, end near $(0.491, 0.272, 0.149, 0.088)$, with sum 1.001.

**The cost.** For a language model with a context of $c$ words of dimension $d$, Mnih and Teh count about $c d + |V|$ operations per word for the softmax and $c d + k$ for NCE, so the speedup is $(c d + |V|)/(c d + k)$. With $c = 2$, $d = 100$, $|V| = 10{,}000$ and $k = 25$ this is about 45.

## Classic examples

- **[Neural probabilistic language models](/neural-probabilistic-language-model/).** Mnih and Teh trained log-bilinear language models with NCE, with a unigram noise distribution, and fixed the normalizer of every context to 1 instead of learning one constant per context; this did not hurt. On the Penn Treebank, maximum likelihood gave a test perplexity of 163.5 in 21 hours. NCE gave 192.5, 172.6, 163.1 and 159.1 with $k = 1$, 5, 25 and 100, in about 1.5 hours each, about 14 times faster. Uniform noise was much worse than unigram noise. They also trained models on the 47 million word, 80,000 word vocabulary data of the MSR Sentence Completion Challenge.
- **[Negative sampling](/negative-sampling/) for the [skip-gram model](/skip-gram-model/).** Mikolov and colleagues (2013) simplified NCE for word vectors: they use $\sigma(s_\theta(u))$ in place of $\sigma(s_\theta(u) - \ln(k p_n(u)))$. The objective no longer gives probabilities, but it is enough to learn good [word embeddings](/word-embedding/).
- **Unnormalized density models.** Gutmann and Hyvärinen applied NCE to models of natural images, such as [independent component analysis](/independent-component-analysis/) models and their extensions, where the normalizer is an integral with no closed form; the normalizing constant is one more parameter.
- **[Recurrent language models](/recurrent-neural-network-language-model/).** The output softmax of a recurrent model has the same cost, and NCE with a unigram noise distribution trains it with $k$ output scores per word.

## Variations

- **The noise distribution.** The unigram distribution is the usual choice for words; a noise closer to the data gives a harder task and a better estimate per sample. Uniform noise is easy to sample but needs many more samples.
- **The number of noise samples.** As $\nu \to \infty$, the covariance of the estimate no longer depends on $p_n$ (Corollary 5 of Gutmann and Hyvärinen), and for a normalized model the estimate tends to the efficiency of maximum likelihood (Corollary 6). With $p_n = p_d$ the covariance is $(1 + 1/\nu)$ times that of maximum likelihood (Corollary 7): 2 times for $\nu = 1$ and about 1.1 times for $\nu = 10$.
- **The normalizer.** Learn one constant $c$ for a single model, as Gutmann and Hyvärinen do. For a conditional model with millions of contexts, fix it to 0, as Mnih and Teh do; the model learns to be nearly self-normalized.
- **[Negative sampling](/negative-sampling/).** Dropping $\ln(k p_n(u))$ from line L4 gives the objective of word2vec. Its optimum is $e^{s(u)} = p_d(u) / (k\, p_n(u))$, a scaled ratio of densities, not $p_d$.
- **[Importance sampling](/importance-sampling/).** Bengio and Senécal estimated the gradient of the normalizer from samples, which needs the samples to be weighted and was found to be unstable by Mnih and Teh. NCE does not estimate the normalizer at all.
- **Ranking forms.** A softmax over the data sample and the $k$ noise samples, which picks the data sample among $k + 1$, is the basis of later contrastive objectives. It is a different loss with a different optimum.
- **[Contrastive divergence](/contrastive-divergence/).** It also avoids the normalizer, but samples from the model by a short Markov chain instead of from a fixed noise distribution.

## Pitfalls

- **Noise with gaps.** If $p_n(u) = 0$ where $p_d(u) > 0$, the model is never told the right value there, and Theorem 1 fails. Give the noise full support, for example by smoothing the unigram.
- **Too few noise samples.** With $k = 1$ the language model of Mnih and Teh was much worse than maximum likelihood (192.5 against 163.5). Choose $k$ on held-out data; 25 already matched it.
- **Reporting perplexity without normalizing.** The trained model is only close to normalized. For a test perplexity, normalize each distribution over $V$ explicitly, which is affordable at test time.
- **Mixing up NCE and negative sampling.** Negative sampling has no $\ln(k p_n)$ term and does not estimate probabilities. Do not use its scores as a language model.
- **The wrong posterior.** The factor $k$ belongs in line L4. With $\ln p_n$ alone, the optimum is $p_d / k$, which is off by a constant factor.

## Exercises

1. Show that the maximum of $J$ over unnormalized densities is $p_m = p_d$ when $p_n > 0$ wherever $p_d > 0$. *Hint:* the derivative at each point is given in the template.
2. Show that the negative sampling objective $\mathbb{E}_{p_d} \ln \sigma(s(u)) + k\, \mathbb{E}_{p_n} \ln \sigma(-s(u))$ is maximized at $e^{s(u)} = p_d(u) / (k\, p_n(u))$. *Answer:* the same computation with $\nu p_n$ replaced by 1 gives $q (q + 1)^{-1}$ terms and the stationary point $q = p_d / (k p_n)$.
3. Show that for a fixed context, as $k \to \infty$, the expected NCE gradient tends to the gradient of the log-likelihood of a normalized model. *Hint:* $\sigma(\Delta_0) \to 0$ for the data sample, and $k\, \mathbb{E}_{p_n}[\sigma(\Delta) \nabla s] \to \sum_u p_m(u) \nabla s(u)$.
4. With $p_n = p_d$, how large must $\nu$ be for the covariance to be within 5 percent of that of maximum likelihood? *Answer:* $1 + 1/\nu \le 1.05$, so $\nu \ge 20$.

## References
