---
tag: 3AW3WK
kind: algorithm
slug: naive-bayes-classifier
name: Naive Bayes classifier
aliases:
- naive Bayes
- simple Bayesian classifier
- idiot's Bayes
- multinomial naive Bayes
- Bernoulli naive Bayes
- Gaussian naive Bayes
area: machine-learning/supervised-learning
level: intro
summary: A generative classifier that assumes the features are independent given the class. It counts in one pass and predicts with argmax of log P(c) + Σ log P(x_j | c).
solves: [classification]
model: real-ram
complexity:
  vars: {n: the number of training examples, d: the number of features (the vocabulary size for text), k: the number of classes}
  time: {worst: "Θ(n d + k d)", best: "Θ(n d + k d)"}
  space: {extra: Θ(k d)}
properties: {deterministic: true, online: true, exact: true, recursive: false}
history:
  year: 1961
  people: [M. E. Maron]
  note: Maron used the independence model to classify documents in 1961. Domingos and Pazzani explained in 1997 why it works when the assumption fails.
prereqs: [bayes-theorem, conditional-independence, maximum-likelihood-estimation, bayes-optimal-classifier]
see_also: [generative-vs-discriminative-models, logistic-regression, quadratic-discriminant-analysis, linear-discriminant-analysis, log-sum-exp-trick, bayesian-network, classification, softmax-regression]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 13, Sections 13.2 to 13.4 (multinomial and Bernoulli naive Bayes, add-one smoothing, Table 13.1 and Examples 13.1 and 13.2)
  - paper: doi:10.1023/A:1007413511361
    title: Pedro Domingos and Michael Pazzani, On the optimality of the simple Bayesian classifier under zero-one loss, Machine Learning 29(2-3), 1997
    locator: pp. 103 to 130 (conditions for optimality under zero-one loss with dependent features)
  - paper: "Andrew Y. Ng and Michael I. Jordan, On discriminative vs. generative classifiers: A comparison of logistic regression and naive Bayes, Advances in Neural Information Processing Systems 14 (NIPS 2001), MIT Press, 2002"
    locator: pp. 841 to 848 (the generative-discriminative pair and the two regimes of learning curves)
  - paper: "Andrew McCallum and Kamal Nigam, A comparison of event models for naive Bayes text classification, AAAI-98 Workshop on Learning for Text Categorization, 1998"
    locator: the multivariate Bernoulli and the multinomial event models
  - paper: doi:10.1145/321075.321084
    title: M. E. Maron, Automatic indexing, an experimental inquiry, Journal of the ACM 8(3), 1961
    locator: pp. 404 to 417 (probabilistic classification of documents from independent clue words)
  - book: isbn:9780070428072
    title: Tom M. Mitchell, Machine Learning, McGraw-Hill, 1997
    locator: Section 6.9 (the naive Bayes classifier) and Section 6.10 (learning to classify text)
---

A naive Bayes classifier is a generative classifier that assumes the features are [conditionally independent](/conditional-independence/) given the class. With this assumption the joint probability factors as $p(x, c) = \pi_c \prod_{j=1}^d p(x_j \mid c)$, so training is one pass of counting and prediction is $\arg\max_c \big(\log \pi_c + \sum_j \log p(x_j \mid c)\big)$. The multinomial and Bernoulli variants count words in text, and the Gaussian variant fits one normal density per feature and class. The assumption is almost never true, but the rule often classifies well, because the 0-1 loss needs only the right ranking of the classes, not the right probabilities (Domingos and Pazzani 1997).

## In plain words

To guess the topic of an email, look at its words. For each topic, you learned how often each word appears in emails of that topic. Pretend that the words appear independently of each other once the topic is known. Then the chance of seeing this email under a topic is the product of the chances of its words, times how common the topic is. Choose the topic with the largest product.

Two practical tricks make it work. A word that never appeared with a topic would make the product zero, so you add one to every count before you divide. And a product of thousands of small numbers becomes too small for a computer, so you add logarithms instead of multiplying.

## The problem

The data model is supervised [classification](/classification/): $n$ examples $(x_i, y_i)$ drawn i.i.d. from an unknown distribution, with $y_i$ in a set of $k$ classes ($k$ is the number of classes on this page) and the 0-1 loss. The method fits a model of $p(x, y)$ in a fixed family and predicts with the [Bayes optimal rule](/bayes-optimal-classifier/) of the fitted model. The three common families differ in what a feature is.

- **Multinomial.** A document is a sequence of tokens from a vocabulary $V$ of size $d$. Given class $c$, each token is drawn independently from a distribution $\theta_c$ on $V$. With $n_t$ the count of token $t$ in the document, $p(x \mid c) \propto \prod_{t \in V} \theta_{c,t}^{\,n_t}$, where the multinomial coefficient does not depend on $c$.
- **Bernoulli.** A document is the binary vector $b \in \{0, 1\}^d$ that says which tokens of $V$ occur. Given $c$, $b_t$ is 1 with probability $p_{c,t}$, independently, so $p(b \mid c) = \prod_{t} p_{c,t}^{b_t}(1 - p_{c,t})^{1 - b_t}$. Absent words count as evidence.
- **Gaussian.** $x \in \mathbb{R}^d$, and given $c$ each $x_j$ is $N(\mu_{c,j}, \sigma^2_{c,j})$ independently. This is [quadratic discriminant analysis](/quadratic-discriminant-analysis/) with diagonal covariance matrices.

## The algorithm

The multinomial variant, with smoothing parameter $\alpha \ge 0$ ($\alpha = 1$ is Laplace or add-one smoothing):

```pseudo id=main
TRAIN-MULTINOMIAL-NB(docs, labels, α)
L1  V ← the set of tokens in the training documents
L2  for each class c do
L3      log π_c ← log(n_c / n)                 ▷ n_c documents have label c
L4      N_{c,t} ← the number of times token t occurs in the documents of class c
L5      log θ_{c,t} ← log((N_{c,t} + α) / (Σ_{t'} N_{c,t'} + α |V|))   for each t ∈ V

PREDICT-MULTINOMIAL-NB(doc)
L6  for each class c do s_c ← log π_c + Σ_{tokens t of doc with t ∈ V} log θ_{c,t}
L7  Z ← LOG-SUM-EXP(s_1, …, s_k);  P(c | doc) ← exp(s_c − Z)
L8  return the class c with the largest s_c
```

Line L6 skips tokens outside $V$, which the model gives no probability. Line L7 computes $Z = m + \log \sum_c e^{s_c - m}$ with $m = \max_c s_c$, the [log-sum-exp trick](/log-sum-exp-trick/), so the largest term is $e^0 = 1$ and nothing underflows. Line L8 needs no normalization at all, because $\log$ is increasing and $Z$ is the same for each class. Ties go to the first class in a fixed order.

The other variants change lines L4 to L6 only.

- **Bernoulli.** $p_{c,t} = (D_{c,t} + \alpha)/(n_c + 2\alpha)$, where $D_{c,t}$ is the number of documents of class $c$ that contain $t$, and $s_c = \log \pi_c + \sum_{t \in V} \big(b_t \log p_{c,t} + (1 - b_t)\log(1 - p_{c,t})\big)$. The sum runs over all of $V$, not only the words of the document.
- **Gaussian.** $\mu_{c,j}$ and $\sigma^2_{c,j}$ are the mean and the variance of feature $j$ in class $c$, and $s_c = \log \pi_c - \sum_j \big(\tfrac12 \log(2\pi\sigma^2_{c,j}) + (x_j - \mu_{c,j})^2/(2\sigma^2_{c,j})\big)$. A small constant added to each variance keeps a feature that is constant within a class from giving a zero variance.

**Why the smoothing.** With $\alpha = 0$, line L5 gives the [maximum likelihood estimate](/maximum-likelihood-estimation/) $N_{c,t}/N_c$. If a token never occurs in class $c$ in training, its estimate is 0, $\log \theta_{c,t} = -\infty$, and one occurrence of that token rules out class $c$ whatever the other evidence. With $\alpha > 0$, $(N_{c,t} + \alpha)/(N_c + \alpha|V|)$ is the posterior mean of $\theta_c$ under a symmetric Dirichlet prior with parameter $\alpha$, which is never 0.

## Example

This is the example of Manning, Raghavan and Schütze (Table 13.1). Training documents: "Chinese Beijing Chinese", "Chinese Chinese Shanghai" and "Chinese Macao" in class china, and "Tokyo Japan Chinese" in class other. The test document is "Chinese Chinese Chinese Tokyo Japan". The vocabulary has 6 words.

**Multinomial, $\alpha = 1$.** Class china has 8 tokens, 5 of them "Chinese", so $\theta_{\text{china},\text{Chinese}} = (5 + 1)/(8 + 6) = 3/7$ and $\theta_{\text{china},\text{Tokyo}} = \theta_{\text{china},\text{Japan}} = 1/14$. Class other has 3 tokens, one of each, so each of the three words has $(1 + 1)/(3 + 6) = 2/9$. The priors are $3/4$ and $1/4$.

$$ \tfrac34 \cdot \left(\tfrac37\right)^3 \cdot \tfrac1{14} \cdot \tfrac1{14} \approx 0.000301, \qquad \tfrac14 \cdot \left(\tfrac29\right)^3 \cdot \tfrac29 \cdot \tfrac29 \approx 0.000135. $$

The classifier predicts china, with posterior $4782969/6934265 \approx 0.6898$. Three occurrences of "Chinese" outweigh one each of "Tokyo" and "Japan".

**Bernoulli, $\alpha = 1$.** Now each document counts once per word. In class china (3 documents), $p(\text{Chinese}) = (3 + 1)/(3 + 2) = 4/5$, $p(\text{Tokyo}) = p(\text{Japan}) = 1/5$, and $p = 2/5$ for each of Beijing, Shanghai and Macao. In class other (1 document), $p = 2/3$ for Chinese, Tokyo and Japan, and $1/3$ for the other three. The three absent words contribute factors $1 - p$:

$$ \tfrac34 \cdot \tfrac45 \cdot \tfrac15 \cdot \tfrac15 \cdot \left(\tfrac35\right)^3 \approx 0.00518, \qquad \tfrac14 \cdot \left(\tfrac23\right)^3 \cdot \left(\tfrac23\right)^3 \approx 0.02195. $$

The Bernoulli model predicts other, with posterior $250000/309049 \approx 0.8089$. It ignores how often "Chinese" occurs, and it counts the absence of Beijing, Shanghai and Macao against class china.

**The same Bernoulli model as a linear classifier.** Taking the log ratio of the two joint probabilities gives $\log \frac{P(\text{china} \mid b)}{P(\text{other} \mid b)} = w_0 + \sum_t w_t b_t$, with $w_t = \log \frac{p_{1,t}(1 - p_{0,t})}{p_{0,t}(1 - p_{1,t})}$ and $w_0 = \log\frac{\pi_1}{\pi_0} + \sum_t \log\frac{1 - p_{1,t}}{1 - p_{0,t}}$. Here $w_{\text{Chinese}} = \ln 2 \approx 0.693$, $w_{\text{Tokyo}} = w_{\text{Japan}} = -\ln 8 \approx -2.079$, $w = \ln(4/3) \approx 0.288$ for the other three words, and $w_0 \approx 2.023$. For the test document the log ratio is $2.023 + 0.693 - 2 \cdot 2.079 \approx -1.443$, and the sigmoid of that is $0.1911$, the posterior of china above.

## Correctness

The claim is that, for the model family on this page, the trained parameters are the smoothed estimates of line L5 (the maximum likelihood estimates when $\alpha = 0$), and that PREDICT returns the class with the largest posterior under the fitted model and the exact posteriors of that model. Under the multinomial model $p(c \mid x) = \pi_c \prod_t \theta_{c,t}^{n_t} / \sum_{c'} \pi_{c'} \prod_t \theta_{c',t}^{n_t}$ by [Bayes' theorem](/bayes-theorem/), because the multinomial coefficient cancels. Its logarithm is $s_c - Z$, and $\log$ is increasing, so line L8 returns an $\arg\max$ of the posterior. The maximum likelihood estimate of a categorical distribution from counts is the vector of relative frequencies, by Gibbs' inequality. The full proof is below. The claim is about the fitted model only: if the features are dependent, the posteriors of the model are not the true posteriors.

## Complexity

The model is the [real RAM](/real-ram/), with one unit for each arithmetic operation and each logarithm.

- **Training.** Counting reads each feature of each example once: $\Theta(n d)$ for dense features, or $\Theta(T)$ for $T$ tokens in total with sparse counts. Line L5 costs $\Theta(k d)$ logarithms. So the time is $\Theta(n d + k d)$, in one pass over the data.
- **Prediction.** $\Theta(k L)$ for a multinomial document of $L$ tokens, $\Theta(k d)$ for the Bernoulli and Gaussian variants, and $\Theta(k)$ for line L7.
- **Space.** $\Theta(k d)$ parameters.
- **Online updates.** New examples change only counts (or the running sums for the Gaussian means and variances), so the model can be updated in $\Theta(d)$ per example without a new pass.

## Properties

- **A linear classifier in disguise.** For two classes, the multinomial and the Bernoulli variants have log odds that are linear in the counts or the bits, as the example shows. Gaussian naive Bayes with a variance that does not depend on the class is linear too; with class dependent variances its boundary is quadratic, but only along the axes.
- **The generative-discriminative pair.** Logistic regression fits the same linear form by maximizing the conditional likelihood $\prod_i p(y_i \mid x_i)$, and naive Bayes fits it through $p(x, y)$. Ng and Jordan (2001) call them a generative-discriminative pair. Logistic regression has the lower or equal asymptotic error. Under their assumptions, naive Bayes comes close to its own, possibly higher, asymptotic error after $O(\log d)$ examples, while logistic regression may need a number of examples linear in $d$. See [generative versus discriminative models](/generative-vs-discriminative-models/).
- **Optimal under 0-1 loss beyond its assumption.** Domingos and Pazzani (1997) show that naive Bayes is the Bayes optimal classifier for a distribution whenever, at every $x$, its estimate puts the true most probable class first, even if the estimated probabilities are far off. They show that this region of 0-1 optimality is much larger than the region where the probabilities are right, and that naive Bayes is optimal for learning conjunctions and disjunctions of literals, which break the independence assumption.
- **Poor probabilities.** Repeated or correlated features are counted many times, which pushes the posteriors toward 0 and 1. Use the class ranking, and calibrate the probabilities if you need them.
- **Not universal.** The Bernoulli variant cannot learn XOR of two bits. With the four inputs equally likely and $y = b_1 \oplus b_2$, each bit alone is independent of the class, so every estimate of $p_{c,t}$ is $1/2$ and every posterior is $1/2$.

## Variants and improvements

- **Lidstone smoothing.** Any $\alpha > 0$, chosen by [cross-validation](/cross-validation/); $\alpha < 1$ often works better for text than add-one.
- **Complement naive Bayes.** Estimate each $\theta_c$ from the documents of all the other classes, which helps with unbalanced classes in text.
- **Transformed counts.** Use $\log(1 + n_t)$ or TF-IDF weights in place of raw counts; the model is then no longer a likelihood, but the linear rule often classifies better.
- **Semi-naive Bayes.** Allow some dependencies: tree augmented naive Bayes gives each feature one more parent feature in a [Bayesian network](/bayesian-network/), and averaged one-dependence estimators average such models.
- **Kernel densities.** Replace the normal density of a real feature by a kernel density estimate.
- **Expectation maximization with unlabeled data.** Treat the class of an unlabeled document as hidden and fit the mixture with EM.

## When to use it

Use naive Bayes for text classification, spam filtering and other problems with many sparse features, when training must be fast, when the training set is small, or as a baseline. It needs no iterative optimization and handles thousands of classes and millions of features. Prefer [logistic regression](/logistic-regression/) or a linear SVM when there is enough data, because they do not pay for the wrong independence assumption in their asymptotic error. Do not use its probabilities as calibrated risks without calibration.

## Pitfalls

- **No smoothing.** One unseen word sets a class probability to 0. Always use $\alpha > 0$.
- **Multiplying probabilities.** A product of 3000 factors near $0.5$ is about $10^{-900}$ and underflows to 0 in double precision, so all classes tie. Add logarithms, and normalize with log-sum-exp.
- **Mixing the event models.** The multinomial model uses token counts and ignores absent words. The Bernoulli model uses presence bits and must include the factors $1 - p_{c,t}$ for absent words. Code that mixes them, for example Bernoulli estimates with a sum over present words only, computes neither model.
- **Zero variance in the Gaussian variant.** A feature that is constant in one class gives $\sigma^2 = 0$ and an infinite density. Add a small constant to each variance.
- **Leaking the vocabulary.** Build $V$ from the training set only; words seen only in test data must be skipped, not given a smoothed probability that depends on the test set.
- **Trusting the probabilities.** Duplicated features double their evidence. A posterior of 0.999 from naive Bayes is often far from the true frequency.

## Implementations

## History

M. E. Maron used the independence model to assign index terms to documents in 1961. The rule appears under the names "simple Bayes" and "idiot's Bayes" in the pattern recognition literature of the following decades. McCallum and Nigam (1998) compared the multivariate Bernoulli and the multinomial event models for text. Domingos and Pazzani (1997) gave the analysis under 0-1 loss that explains its good accuracy, and Ng and Jordan (2001) used it with logistic regression as the standard example of a generative-discriminative pair.

## References
