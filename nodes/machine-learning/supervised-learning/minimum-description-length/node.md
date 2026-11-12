---
tag: 71J32F
kind: concept
slug: minimum-description-length
name: Minimum description length
aliases:
- MDL principle
- two-part code MDL
area: machine-learning/supervised-learning
level: advanced
summary: "Choose the model that gives the shortest code for the data: the bits to describe the model plus the bits to describe the data with the help of the model."
prereqs: [kraft-inequality, occams-razor, shannon-entropy]
see_also: [marginal-likelihood, kolmogorov-complexity, universal-code, structural-risk-minimization, bayesian-inference, source-coding-theorem, overfitting, regularization]
sources:
  - paper: doi:10.1016/0005-1098(78)90005-5
    title: Jorma Rissanen, Modeling by shortest data description, Automatica 14(5), 1978
    locator: the principle, and the two-part code length with about (k/2) log n bits for k parameters
  - book: isbn:9780262072816
    title: Peter D. Grünwald, The Minimum Description Length Principle, MIT Press, 2007
    locator: Chapter 1 (the idea and crude two-part MDL), Part II (universal codes, two-part, Bayesian, normalized maximum likelihood and prequential) and Part III (refined MDL)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 5 (Kraft inequality and the code length of a distribution) and Chapter 14 (Kolmogorov complexity)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Section 7.3 (minimum description length and Occam's razor)
  - paper: "Andrew Barron, Jorma Rissanen and Bin Yu, The minimum description length principle in coding and modeling, IEEE Transactions on Information Theory 44(6), 1998"
    locator: survey of two-part, mixture and normalized maximum likelihood codes, and their (k/2) log n redundancy
---

The minimum description length (MDL) principle, due to Rissanen (1978), chooses among models by data compression. Each model gives a way to encode the data. MDL picks the model for which the bits to describe the model, plus the bits to describe the data with the help of the model, are fewest. A model that is too simple fits the data badly, so the second part is long. A model that is too complex needs many bits for itself, so the first part is long. Because code lengths and probabilities are linked by the [Kraft inequality](/kraft-inequality/), the principle is close to Bayesian model selection by [marginal likelihood](/marginal-likelihood/), and it is the model selection form of [Occam's razor](/occams-razor/).

## In plain words

Imagine that you must send a data set to a friend over a slow line, and you both agree on a set of possible models in advance. You may first send a model and then send the data in a code that the model makes short. A good model makes the data cheap to send, but the model itself also costs bits. Choose the model that makes the whole message shortest. Regularities in the data are exactly what lets you compress it, so the shortest message is the one that captures the regularities and leaves only noise. Random noise cannot be compressed, so a model that tries to describe the noise only adds bits.

## The idea

**Codes are probabilities.** A prefix-free code assigns lengths $L(x)$ with $\sum_x 2^{-L(x)} \le 1$ (Kraft). Conversely, for every probability distribution $P$ there is a prefix-free code with $L(x) = \lceil -\log_2 P(x) \rceil$ (Cover and Thomas, Chapter 5). So "a short code for the data" and "a high probability for the data" are the same thing, up to rounding. MDL works with the ideal lengths $-\log_2 P(x)$; a real code, for example an arithmetic code, is within 2 bits of them.

**Two-part MDL.** Let $\mathcal{H}$ be a set of models, each a probability distribution on data sets, and let $L(H)$ be a prefix-free code for $\mathcal{H}$. Choose

$$\hat H = \arg\min_{H \in \mathcal{H}} \Big( L(H) + L(D \mid H) \Big), \qquad L(D \mid H) = -\log_2 H(D).$$

For a model class with continuous parameters, the parameter $\theta$ must itself be sent with finite precision. Sending each of $k$ parameters to precision about $1/\sqrt{n}$ costs about $\frac12 \log_2 n$ bits per parameter, and a coarser precision costs more in the second part than it saves in the first. This gives Rissanen's *crude* MDL criterion for a class with $k$ free parameters:

$$-\log_2 P(D \mid \hat\theta) + \frac{k}{2} \log_2 n,$$

where $\hat\theta$ is the maximum likelihood estimate. Up to a constant factor this is the Bayesian information criterion (BIC) of Schwarz, found at the same time on Bayesian grounds.

**Refined MDL.** Grünwald (2007) calls the version above crude because the code for the parameter is somewhat arbitrary. Refined MDL replaces the two parts by one *[universal code](/universal-code/)* for the whole model class, a code whose length for every data set is close to $-\log_2 P(D \mid \hat\theta(D))$, the best fit in hindsight. Four universal codes are standard: the two-part code, the Bayes mixture $\int P(D \mid \theta) w(\theta)\, d\theta$, the normalized maximum likelihood code of Shtarkov, and the prequential code that predicts each point from the points before it. For smooth $k$-parameter families all four exceed the best fit by $\frac{k}{2} \log_2 n + O(1)$ bits (Barron, Rissanen and Yu 1998). The model class with the shortest universal code length is chosen.

**The link to Bayes.** If the code for the model part is $-\log_2$ of a prior, a Bayes mixture code is exactly minus the log of the Bayes *evidence*. Then MDL with a mixture code and Bayesian model selection with that prior pick the same model. The example below shows this as an exact identity. The two views differ in what they claim: Bayes treats the prior as a belief, MDL treats it as a code and judges it by the code length it gives, with no claim that any model is true.

**The link to learning bounds.** If the hypothesis $h$ is coded with $|h|$ bits by a prefix-free code, the [Occam bound](/occams-razor/) says that with probability $1 - \delta$, for all $h$ at once, $L_D(h) \le L_S(h) + \sqrt{(|h| \ln 2 + \ln(2/\delta))/(2n)}$. Minimizing the right side is the MDL rule of Shalev-Shwartz and Ben-David (Section 7.3), a kind of [structural risk minimization](/structural-risk-minimization/).

**The link to Kolmogorov complexity.** The shortest program that prints the data, its [Kolmogorov complexity](/kolmogorov-complexity/), would be the ideal description length, but it is not computable. MDL replaces the set of all programs by a model class whose codes can be computed.

### Pitfalls

- **The code must be fixed before the data are seen.** A code chosen after looking at the data can make any model look short; the Kraft inequality only protects a code that was fixed in advance.
- **Crude penalties are asymptotic.** The $\frac{k}{2} \log_2 n$ term assumes that $k$ is small compared with $n$. In the histogram example below, the crude criterion charges 2312 bits for 256 bins on 200 points, while the exact code needs only 1591.
- **Small samples give small differences.** When two totals differ by a fraction of a bit, the data do not prefer either model. In the example, with 50 uniform points, 1 bin and 256 bins differ by 0.1 bits.
- **The model class is a choice.** MDL finds the best compressor in the class you gave it. If the class misses the regularity in the data, MDL cannot find it.
- **Ideal lengths are not integers.** Real codes round up, which adds at most a few bits in total, but it matters when two models are within a few bits of each other.

## Examples

**Choosing the number of bins of a histogram.** The data are $n$ integers in $\{0, \ldots, N - 1\}$, with $N = 2^B$. The model with $K = 2^j$ equal bins ($j = 0, \ldots, B$) codes the data in four parts:

1. the index $j$, uniform over $B + 1$ choices: $\log_2(B + 1)$ bits;
2. the bin counts $(n_1, \ldots, n_K)$, uniform over the $\binom{n + K - 1}{K - 1}$ ways to write $n$ as a sum of $K$ counts;
3. the sequence of bin labels, given the counts: $\log_2 \frac{n!}{n_1! \cdots n_K!}$ bits;
4. the position of each point inside its bin: $n \log_2 (N/K)$ bits.

Parts 1 and 2 describe the model, parts 3 and 4 the data given the model. Multiply out the four probabilities:

$$2^{-L_K(D)} = \frac{1}{B + 1} \cdot \frac{(K - 1)!\, n_1! \cdots n_K!}{(n + K - 1)!} \cdot \Big(\frac{K}{N}\Big)^n.$$

The middle factor is the Bayes marginal likelihood of the bin labels under a uniform Dirichlet prior on the bin probabilities, the same as Laplace's rule of succession applied point by point. So here two-part MDL and Bayesian model selection are the same rule. The tests for this page check this identity exactly with fractions, and check that for each $K$ the probabilities of all $N^n$ data sets sum to exactly $1/(B + 1)$, so the code wastes no bits.

The code for this page uses $B = 8$ ($N = 256$), $n = 200$ and seed 1. "Steps" draws from a density with masses $0.45, 0.05, 0.1, 0.4$ on the four quarters of the range; its bin counts with $K = 4$ are $97, 11, 23, 69$.

| data | $K = 1$ | $K = 2$ | $K = 4$ | $K = 8$ | $K = 16$ | $K = 256$ | MDL choice |
|---|---|---|---|---|---|---|---|
| uniform | **1603.2** | 1606.5 | 1611.5 | 1614.7 | 1624.0 | 1614.5 | $K = 1$ |
| steps | 1603.2 | 1605.8 | **1538.0** | 1541.6 | 1550.2 | 1590.7 | $K = 4$ |

For the steps data with $K = 4$, the four parts are 3.2, 20.4, 314.5 and 1200.0 bits. A code that knew the true density would need 1526.9 bits, so the cost of learning the density from the data is 11.1 bits. With $n = 1000$ MDL again picks $K = 1$ and $K = 4$, and the crude criterion $n \hat H + \frac{K - 1}{2} \log_2 n + n \log_2 (N/K)$ picks the same.

**Why the penalty is about $\frac{K - 1}{2} \log_2 n$.** By Stirling's formula, part 3 is $n \hat H - \frac{K - 1}{2} \log_2 n + O(1)$, where $\hat H$ is the [entropy](/shannon-entropy/) of the empirical bin frequencies, and part 2 is $(K - 1) \log_2 n + O(1)$ for fixed $K$. The sum is the crude MDL formula with $k = K - 1$ free parameters.

**Polynomial degree.** For regression with Gaussian noise, the code length of the residuals is $\frac{n}{2} \log_2 \hat\sigma^2$ plus a constant, and a degree $p$ polynomial adds about $\frac{p + 1}{2} \log_2 n$ bits. This gives a penalized fit, like the ones on [overfitting](/overfitting/) and [regularization](/regularization/), with a penalty that comes from counting bits.

## Where it is used

- **Model selection.** Choosing the order of autoregressive models, the number of components of a mixture, the degree of a polynomial, or the structure of a [Bayesian network](/bayesian-network-structure-learning/), where MDL scores are standard.
- **Decision tree pruning and rule learning.** Several pruning methods compare the bits for a subtree with the bits for the errors it removes.
- **Clustering and segmentation.** The number of clusters or change points is chosen by the code length of the segmentation plus the data in each segment.
- **Learning theory.** Occam bounds and PAC-Bayes bounds have the form "training error plus description length over sample size", which MDL turns into a selection rule.

## References
