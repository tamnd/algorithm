---
tag: 5Q6Q0N
kind: concept
slug: generative-vs-discriminative-models
name: Generative versus discriminative models
aliases:
- generative versus discriminative classifiers
- generative-discriminative pair
- informative versus discriminative learning
area: machine-learning/supervised-learning
level: intro
summary: "A generative model fits the joint p(x, y) and classifies by Bayes' rule; a discriminative model fits p(y | x) or the boundary directly. Each wins in a different regime."
prereqs: [bayes-optimal-classifier, logistic-regression, naive-bayes-classifier]
see_also: [quadratic-discriminant-analysis, linear-discriminant-analysis, conditional-random-field, hidden-markov-model, support-vector-machine, gaussian-mixture-model, structured-prediction, exponential-family-distribution]
sources:
  - paper: "Andrew Y. Ng and Michael I. Jordan, On discriminative vs. generative classifiers: a comparison of logistic regression and naive Bayes, Advances in Neural Information Processing Systems 14, MIT Press, 2002"
    locator: pp. 841 to 848 (the asymptotic errors of the pair, and the O(log n) versus O(n) sample sizes to approach them)
  - paper: "Y. Dan Rubinstein and Trevor Hastie, Discriminative vs informative learning, Proceedings of the Third International Conference on Knowledge Discovery and Data Mining (KDD-97), AAAI Press, 1997"
    locator: pp. 49 to 53 (the terms informative and discriminative, and when each is more efficient)
  - paper: doi:10.1080/01621459.1975.10480319
    title: Bradley Efron, The efficiency of logistic regression compared to normal discriminant analysis, Journal of the American Statistical Association 70(352), 1975
    locator: pp. 892 to 898 (the asymptotic relative efficiency of logistic regression when the normal model is true)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 1.5.4 (generative models, discriminative models and discriminant functions), Sections 4.2 and 4.3 (probabilistic generative and discriminative models)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 4.4.5 (logistic regression or LDA?)
  - paper: doi:10.1561/2200000013
    title: Charles Sutton and Andrew McCallum, An introduction to conditional random fields, Foundations and Trends in Machine Learning 4(4), 2012
    locator: Section 2.2 (generative versus discriminative models; naive Bayes and logistic regression, HMMs and linear-chain CRFs)
  - paper: "Julia A. Lasserre, Christopher M. Bishop and Thomas P. Minka, Principled hybrids of generative and discriminative models, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2006"
    locator: the hybrid model that interpolates between the generative and the discriminative fit
---

A generative model of classification describes how the data are produced: it fits the joint distribution $p(x, y) = p(y)\, p(x \mid y)$ and classifies a new $x$ by computing $p(y \mid x)$ with [Bayes' theorem](/bayes-theorem/). A discriminative model fits the conditional distribution $p(y \mid x)$ directly, or, in its non-probabilistic form, only a decision function $f(x)$. [Naive Bayes](/naive-bayes-classifier/), [linear](/linear-discriminant-analysis/) and [quadratic discriminant analysis](/quadratic-discriminant-analysis/) and [hidden Markov models](/hidden-markov-model/) are generative. [Logistic regression](/logistic-regression/), [conditional random fields](/conditional-random-field/) and [support vector machines](/support-vector-machine/) are discriminative. A generative model uses more assumptions; when they hold it learns faster, and when they fail the discriminative model usually has the lower error with enough data.

## In plain words

There are two ways to learn to tell cats from dogs. The first way is to learn what cats look like and what dogs look like, well enough that you could draw a new one of each. To sort a new animal, you ask which of the two descriptions fits it better. The second way is to learn only the differences that matter for the choice, such as the shape of the ears.

The first way, the generative way, learns more than the task needs. If its picture of each animal is right, it learns quickly from few examples, and it can also fill in missing details. If its picture is wrong, its mistakes go into the choice. The second way, the discriminative way, spends all its effort on the choice. It usually needs more examples, but it is more robust when the picture is wrong.

## The idea

### Three ways to build a classifier

Bishop (Section 1.5.4) separates three approaches, in decreasing order of what they model:

1. **Generative.** Model $p(x \mid y)$ and $p(y)$, so the joint $p(x, y)$. Get $p(y \mid x) = p(x \mid y) p(y) / \sum_{y'} p(x \mid y') p(y')$, then apply the [Bayes optimal](/bayes-optimal-classifier/) rule to the fitted posterior.
2. **Discriminative, probabilistic.** Model $p(y \mid x)$ directly with a parametric family, for example $p(y = 1 \mid x) = \sigma(w^{\top} x + b)$, and fit it by conditional [maximum likelihood](/maximum-likelihood-estimation/).
3. **Discriminant function.** Learn a map $f$ from inputs to labels with no probabilities, for example the [perceptron](/perceptron/) or the support vector machine, by minimizing a [loss](/loss-function/) on the training set.

Rubinstein and Hastie (1997) call the first approach informative learning and the second discriminative learning. Many authors put the second and third under one name, discriminative.

### The objectives differ by one term

For a generative model with parameters $\theta$, the log likelihood of the training set splits as
$$ \sum_{i=1}^n \log p_\theta(x_i, y_i) = \underbrace{\sum_{i=1}^n \log p_\theta(y_i \mid x_i)}_{\text{conditional}} + \underbrace{\sum_{i=1}^n \log p_\theta(x_i)}_{\text{marginal}} . $$
A discriminative fit of the same family maximizes only the conditional term. The generative fit also has to explain the distribution of the inputs, so it gives up some conditional fit when the model of $p(x \mid y)$ is wrong. When the model is right, the marginal term is extra information about $\theta$, and the generative estimate has a smaller variance.

### Generative-discriminative pairs

Several generative models induce a posterior that is a known discriminative family. Ng and Jordan (2001) call such a generative model and the discriminative model that fits the same family directly a generative-discriminative pair.

| generative model | posterior family | discriminative partner |
| --- | --- | --- |
| Bernoulli or multinomial naive Bayes | $\sigma(w^{\top} x + b)$ (softmax for $k$ classes) | logistic regression |
| Gaussian classes, shared covariance (LDA) | $\sigma(w^{\top} x + b)$ | logistic regression |
| Gaussian classes, separate covariances (QDA) | $\sigma$ of a quadratic in $x$ | logistic regression on $x_j$ and $x_j x_l$ |
| Gaussian naive Bayes with a shared variance per feature | $\sigma(w^{\top} x + b)$ | logistic regression |
| hidden Markov model | linear-chain Gibbs distribution | linear-chain CRF |

The linear cases follow from one fact: if every class conditional is in the same [exponential family](/exponential-family-distribution/) with a shared dispersion, then $\log \frac{p(y = a \mid x)}{p(y = b \mid x)}$ is linear in the sufficient statistics (Bishop Section 4.2). So the two members of a pair can represent the same classifiers. They differ only in how they choose the parameters.

### What theory says

- **Correct model, efficiency.** Efron (1975) took two normal classes with a shared covariance, where LDA is the maximum likelihood fit and logistic regression is also consistent. He computed the asymptotic relative efficiency of logistic regression for the excess error rate. It is between about one half and two thirds for the class separations of practical interest, and it decreases as the classes move apart. So when the generative model is right, logistic regression needs up to about twice as many examples for the same error.
- **Wrong model, asymptotic error.** For a pair, the discriminative fit converges to the classifier in the family with the best conditional likelihood (or, for empirical risk minimization, the best 0-1 error), and the generative fit converges to the classifier induced by the best joint fit. Ng and Jordan show that, for naive Bayes and its partner, the asymptotic 0-1 error of the discriminative classifier is at most that of the generative one, when the discriminative classifier is chosen to minimize the training error.
- **Wrong model, speed.** Ng and Jordan also compare how many examples each needs to come within a fixed $\epsilon$ of its own asymptotic error, with $d$ features. For the discriminative classifier, the standard VC bound gives $O(d)$ examples, and for linear classifiers in general $\Omega(d)$ can be necessary. For naive Bayes, all $O(d)$ parameter estimates are within $\epsilon$ of their limits, with high probability, after $O(\log d)$ examples. They then show that the error of naive Bayes comes within $\epsilon$ of its asymptotic error after $O(\log d)$ examples, under an extra assumption: few points lie close to the asymptotic decision boundary. Their experiments on UCI data often show naive Bayes ahead for small $n$ and logistic regression ahead for large $n$. This is a statement about each method reaching its own limit, not a claim that naive Bayes always wins on small samples, and later work showed data sets where the predicted crossover does not happen.

### What only a generative model gives

- **Missing features.** With $p(x \mid y)$ you can marginalize over a missing feature. A discriminative model needs a separate model or imputation.
- **Unlabeled data and new data.** The marginal $p(x)$ uses unlabeled examples (semi-supervised learning with EM on a [Gaussian mixture](/gaussian-mixture-model/)) and gives a score for detecting inputs unlike the training data.
- **Sampling and modular training.** You can sample new pairs $(x, y)$, and you can add a class by fitting one more $p(x \mid c)$ without refitting the others.
- **Closed-form fits.** Naive Bayes, LDA and QDA are fitted by counting and averaging, with no iterative optimization, and their estimates stay finite on separable data, where the logistic regression maximum likelihood estimate does not exist.

## Examples

**Duplicated feature: same decisions, worse probabilities.** Let $y$ be 0 or 1 with probability $\frac12$ each, and let one bit $b$ have $P(b = 1 \mid y = 1) = 0.8$ and $P(b = 1 \mid y = 0) = 0.2$. Give the classifier two features $x_1 = x_2 = b$, a copy of the same bit. The true posterior is $P(y = 1 \mid x = (1, 1)) = 0.8$. Naive Bayes, in the limit of infinite data, estimates the same marginals and multiplies the evidence twice:
$$ P_{\text{NB}}(y = 1 \mid x = (1, 1)) = \frac{0.8^2}{0.8^2 + 0.2^2} = \frac{16}{17} \approx 0.941 . $$
Logistic regression on $(x_1, x_2)$ can represent the true posterior ($b_0 = -\ln 4$ and $w_1 + w_2 = 2 \ln 4$), and conditional maximum likelihood finds it. Both rules predict $y = b$ and have the Bayes error 0.2. But the expected [log loss](/cross-entropy-loss/) is $0.500$ nats for logistic regression and $0.8 \ln\frac{17}{16} + 0.2 \ln 17 \approx 0.615$ nats for naive Bayes. The wrong independence assumption made the generative probabilities overconfident.

**An outlier moves the generative boundary.** One feature, two classes, five points each:

| class | points |
| --- | --- |
| 0 | 0, 1, 2, 3, 4.5 |
| 1 | 3.5, 5, 6, 7, 60 |

LDA fits $\mu_0 = 2.1$, $\mu_1 = 16.3$ and a pooled variance $240.6$, and with equal priors its threshold is the midpoint $9.2$. It misclassifies the four class 1 points 3.5, 5, 6 and 7. Without the point at 60, the LDA threshold is $3.88$ and it makes two errors. Logistic regression puts its threshold at about $4.002$ with or without the point at 60, and makes two errors: the far point already has $p(y = 1 \mid x) \approx 1$, so it adds almost nothing to the gradient. The Gaussian model is wrong for class 1, and the generative fit spends its parameters on explaining the outlier.

**Generative wins when the model is right and $n$ is small.** With two Gaussian classes with a shared covariance in $d$ dimensions and $n$ close to $d$, logistic regression can separate the training set perfectly and its weights diverge, while LDA (with a shrunk covariance, as in regularized discriminant analysis) stays stable. This is the regime of Efron's efficiency result and of the small-$n$ side of the Ng and Jordan experiments.

## Where it is used

- **Text classification.** Naive Bayes is a standard first model for short texts and small labeled sets, and logistic regression or linear SVMs usually win on large ones.
- **Sequence labeling.** Hidden Markov models were replaced by linear-chain [conditional random fields](/conditional-random-field/) and structured perceptrons for tagging and segmentation, because a discriminative model can use many overlapping features of the whole input without modeling their joint distribution (see [structured prediction](/structured-prediction/)).
- **Choosing between LDA, QDA and logistic regression.** ESL Section 4.4.5 states the trade: LDA relies on the Gaussian assumption and gains efficiency, and logistic regression is safer for outliers and non-Gaussian features. In practice the two often give similar results.
- **Hybrid models.** Lasserre, Bishop and Minka (2006) fit a model whose parameters interpolate between the generative and the discriminative fit, to use unlabeled data and still keep a good conditional fit. Deep generative models are also used as feature extractors for discriminative heads.

## References
