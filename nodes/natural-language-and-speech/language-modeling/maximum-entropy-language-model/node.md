---
tag: CNH4EZ
kind: model
slug: maximum-entropy-language-model
name: Maximum entropy language model
aliases:
- exponential language model
- Rosenfeld maxent model
area: natural-language-and-speech/language-modeling
level: advanced
summary: "A log-linear model of the next word given features of the history, such as n-grams and triggers, fit to match feature expectations."
history:
  year: 1996
  people: [Ronald Rosenfeld, Adam L. Berger, Stephen A. Della Pietra, Vincent J. Della Pietra]
  note: Rosenfeld combined n-gram and trigger constraints in one maximum entropy model of the next word in 1996. Berger and the Della Pietras described the maximum entropy approach to language processing in the same year.
prereqs: [n-gram-language-model, softmax-regression]
see_also: [softmax-regression, exponential-family-distribution, logistic-regression, conditional-random-field, maximum-entropy-markov-model, cache-language-model, limited-memory-bfgs, neural-probabilistic-language-model]
sources:
  - paper: doi:10.1006/csla.1996.0011
    title: Ronald Rosenfeld, A maximum entropy approach to adaptive statistical language modelling, Computer Speech and Language 10(3), 1996, pages 187 to 228
    locator: trigger pairs, the maximum entropy model with n-gram and trigger constraints, and the results on Wall Street Journal text and in the SPHINX-II recognizer
  - paper: "Adam L. Berger, Stephen A. Della Pietra and Vincent J. Della Pietra, A maximum entropy approach to natural language processing, Computational Linguistics 22(1), 1996, pages 39 to 71"
    title: Berger, Della Pietra and Della Pietra 1996
    locator: the conditional maximum entropy model, its duality with maximum likelihood in the exponential family, and feature selection
  - paper: doi:10.1214/aoms/1177692379
    title: J. N. Darroch and D. Ratcliff, Generalized iterative scaling for log-linear models, Annals of Mathematical Statistics 43(5), 1972, pages 1470 to 1480
    locator: the generalized iterative scaling algorithm and its convergence
  - paper: doi:10.1103/PhysRev.106.620
    title: E. T. Jaynes, Information theory and statistical mechanics, Physical Review 106(4), 1957, pages 620 to 630
    locator: the principle of maximum entropy
---

A maximum entropy language model gives the probability of the next word $w$ after a history $h$ as a [softmax](/softmax-regression/) of a weighted sum of features:

$$P_\lambda(w \mid h) = \frac{\exp\big(\sum_i \lambda_i f_i(h, w)\big)}{Z_\lambda(h)}, \qquad Z_\lambda(h) = \sum_{v \in V} \exp\Big(\sum_i \lambda_i f_i(h, v)\Big).$$

Each feature $f_i$ is a fact about the pair, such as "the last word is *stock* and $w$ is *market*" or "*stock* occurred earlier in the document and $w$ is *shares*". Any set of such facts can be put together in one model, which is the main appeal. The weights are fitted so that, on the training text, the expected value of each feature under the model equals its count. Among all models that meet these constraints, this is the one with the largest entropy, which is where the name comes from. Rosenfeld (1996) used it to combine n-gram features with long-distance trigger features and lowered the perplexity of a trigram model by 32 to 39 percent.

## The machine

**Features.** A feature is a function $f_i(h, w) \ge 0$, in practice almost always 0 or 1. Common kinds:

- *n-gram features*, $f(h, w) = 1$ if the last $k - 1$ words of $h$ and $w$ form a given $k$-gram, for $k = 1, \ldots, n$;
- *trigger features*, $f(h, w) = 1$ if a given word $a$ occurred in the document history and $w = b$, for a selected trigger pair $a \to b$; with $a = b$ this is a self-trigger, the effect that a [cache](/cache-language-model/) models;
- *class features*, the same as n-gram features over word classes;
- any other test of the history, such as the topic of the document.

**The model.** For a history $h$, the score of a word is the sum of the weights of its active features, and the softmax turns the scores into a distribution over the vocabulary $V$. The normalizer $Z_\lambda(h)$ depends on $h$, so it must be computed for every history.

**The fit.** Let $\tilde p(h, w)$ be the relative frequency of the pair in the training text and $\tilde p(h)$ that of the history. The weights maximize the conditional log-likelihood

$$L(\lambda) = \sum_{h, w} \tilde p(h, w) \ln P_\lambda(w \mid h).$$

Its gradient is the difference between the data count and the model expectation of each feature,

$$\frac{\partial L}{\partial \lambda_i} = \sum_{h, w} \tilde p(h, w) f_i(h, w) - \sum_h \tilde p(h) \sum_w P_\lambda(w \mid h) f_i(h, w),$$

so at the optimum the two are equal for every feature. The classic algorithms are generalized iterative scaling (Darroch and Ratcliff 1972) and improved iterative scaling; later practice uses gradient methods such as [L-BFGS](/limited-memory-bfgs/) or [stochastic gradient descent](/stochastic-gradient-descent/). A Gaussian prior on the weights, or a cutoff on rare features, is needed in practice: a feature that is never active in the data would otherwise get the weight $-\infty$.

**The maximum entropy view.** Consider all conditional models $P(w \mid h)$ whose feature expectations, with the history weights $\tilde p(h)$, equal the data counts. The one with the largest conditional entropy $-\sum_h \tilde p(h) \sum_w P(w \mid h) \ln P(w \mid h)$ has the log-linear form above, and its weights are the maximum likelihood weights. The weights are the Lagrange multipliers of the constraints. So the model assumes nothing beyond the constraints: where no feature says otherwise, it spreads the probability as evenly as it can.

**An example.** The training data has the history a 4 times and a second history x 6 times. After a come b 3 times and c once; after x come a twice, b once and c 3 times. Take the unigram features of a, b and c, and one bigram feature for "a then b". The constraints are the counts 2, 4 and 4 of a, b and c, and the count 3 of a b. The bigram feature forces $4 P(\text{b} \mid \text{a}) = 3$, so $P(\text{b} \mid \text{a}) = 3/4$, and then the count of b forces $6 P(\text{b} \mid \text{x}) = 1$. No feature separates a from c, so after both histories they keep the same ratio $r = e^{\lambda_a - \lambda_c}$, and the count of a gives $(4 \cdot \frac14 + 6 \cdot \frac56) \frac{r}{1 + r} = 2$, so $r = 1/2$. The fitted model is

| $h$ | a | b | c |
|---|---|---|---|
| a | 1/12 | 3/4 | 1/6 |
| x | 5/18 | 1/6 | 5/9 |

with $e^{\lambda_b - \lambda_c} = 3/10$ and the bigram weight $e^{\mu} = 15$. Every constraint holds; for c, $4 \cdot \frac16 + 6 \cdot \frac59 = 4$. The model gives a after a the probability 1/12, although a b and a c are the only pairs seen after a: nothing in the constraints forbids it. After x it does not reproduce the counts, because no feature is specific to x.

## What it counts

The model is measured by its [perplexity](/perplexity/) on test text, and in a recognizer by the word error rate. The cost is dominated by the normalizer. One probability needs $Z_\lambda(h)$, a sum over all $|V|$ words, each with its active features: $\Theta(|V| \cdot a)$ for $a$ active features per pair, against $O(n)$ lookups for a backoff n-gram model. One pass of training computes the model expectations for every distinct history in the data, $\Theta(H |V| a)$ for $H$ distinct histories, and the fit needs many passes. Large vocabularies made this the main limit of the method. Word classes help: with $P(w \mid h) = P(\text{class}(w) \mid h)\, P(w \mid h, \text{class}(w))$ each normalizer runs over the classes or over one class, about $\sqrt{|V|}$ terms each for a good split.

## Relation to other models

- **Softmax regression.** The model is [softmax regression](/softmax-regression/) with the words as classes and features that depend on both the history and the class. With two classes it is [logistic regression](/logistic-regression/).
- **Exponential family.** For each history it is an [exponential family](/exponential-family-distribution/) distribution over $V$ with sufficient statistics $f_i(h, \cdot)$, which explains the moment matching at the optimum.
- **n-gram models.** With one indicator feature for every n-gram of one order and no prior, the likelihood is maximized by the maximum likelihood [n-gram model](/n-gram-language-model/), in the limit where the weights of the unseen n-grams go to $-\infty$. With features of all orders up to $n$ it is a smoothed model in which each n-gram adds to the score of the shorter ones, in place of backoff.
- **Sequence models.** The [maximum entropy Markov model](/maximum-entropy-markov-model/) uses the same conditional form for tags, and the [conditional random field](/conditional-random-field/) normalizes over whole tag sequences.
- **Neural language models.** A [neural probabilistic language model](/neural-probabilistic-language-model/) has the same softmax output, but learns its features of the history with a hidden layer instead of using a fixed list.
- **Cache models.** A self-trigger feature does the work of a [cache](/cache-language-model/) inside one model, and trigger pairs extend it to related words.

## Known results in the model

- **Duality.** The maximum likelihood model in the log-linear family and the maximum entropy model under the expectation constraints are the same model (Berger, Della Pietra and Della Pietra 1996). The log-likelihood is concave in $\lambda$, so every local maximum is global, and the fitted distribution is unique when the constraints can be met.
- **Generalized iterative scaling converges.** Darroch and Ratcliff proved that GIS increases the likelihood at each step and converges to the solution, for non-negative features with a constant sum $\sum_i f_i(h, w) = C$; a slack feature makes any feature set meet this condition. Its steps shrink with $C$, so it is slow with many active features.
- **Triggers help.** Rosenfeld (1996) selected trigger pairs by their mutual information and combined them with n-gram constraints in one maximum entropy model. On Wall Street Journal text this lowered the perplexity by 32 to 39 percent against a trigram model, and in the SPHINX-II recognizer it lowered the word error rate by 10 to 14 percent.
- **Feature induction.** Since any feature can be added, the choice of features is part of the fit. Berger and the Della Pietras add features one at a time by their gain in likelihood, a form of [feature selection](/feature-selection/).
- **No explicit backoff.** Smoothing comes from the prior on the weights and from the features of shorter histories, not from a discount; an unseen n-gram simply has no feature.

## References
