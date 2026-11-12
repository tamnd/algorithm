---
tag: BSBWN0
kind: concept
slug: bias-variance-tradeoff
name: Bias-variance tradeoff
aliases:
- bias-variance decomposition
- bias-variance dilemma
area: machine-learning/supervised-learning
level: core
summary: "For squared loss, the expected error of a learned predictor at a point is exactly noise plus squared bias plus variance. More capacity often lowers bias and raises variance."
prereqs: [generalization-error, variance, mean-squared-error]
see_also: [overfitting, regularization, double-descent, k-nearest-neighbors, bagging, ridge-regression, cross-validation, bayes-optimal-classifier]
sources:
  - paper: doi:10.1162/neco.1992.4.1.1
    title: Stuart Geman, Elie Bienenstock and René Doursat, Neural networks and the bias/variance dilemma, Neural Computation 4(1), 1992
    locator: Section 2 (the decomposition of the mean squared error into bias and variance) and the experiments on k-nearest-neighbor and kernel regression
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 2.9 (model complexity and the bias-variance tradeoff) and Section 7.3 (the bias-variance decomposition, with the k-nearest-neighbor and linear model cases)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 3.2 (the bias-variance decomposition)
  - paper: "Pedro Domingos, A unified bias-variance decomposition and its applications, Proceedings of the 17th International Conference on Machine Learning (ICML), 2000"
    locator: the decomposition for general losses and the zero-one loss case
  - paper: "Gareth M. James, Variance and bias for general loss functions, Machine Learning 51(2), 2003"
    locator: the systematic effect and the variance effect for general losses
  - paper: doi:10.1073/pnas.1903070116
    title: Mikhail Belkin, Daniel Hsu, Siyuan Ma and Soumik Mandal, Reconciling modern machine-learning practice and the classical bias-variance trade-off, PNAS 116(32), 2019
    locator: the double descent curve beyond the interpolation threshold
---

The bias-variance decomposition splits the expected [squared error](/mean-squared-error/) of a learned predictor at a fixed input into three parts: the noise in the label, the squared bias of the average prediction, and the [variance](/variance/) of the prediction over training sets. It is an exact identity for squared loss. The *tradeoff* is the common observation that a richer model class lowers the bias and raises the variance, so that the [generalization error](/generalization-error/) is smallest at a middle capacity. The identity always holds; the tradeoff is a tendency, and it fails in some modern settings (see [double descent](/double-descent/)).

## In plain words

Train the same kind of model many times, each time on a fresh sample of data, and look at its predictions for one fixed input. Three things make these predictions miss the true label. First, the label itself is noisy, and no model can predict the noise. Second, the average prediction may be off target, because the model is too simple to follow the true curve. This is the bias. Third, the predictions jump around from one sample to the next, because the model follows the accidents of each sample. This is the variance. A very flexible model has a small bias and a large variance. A very rigid model has the opposite. For squared error, the three parts add up exactly to the expected error.

## The idea

**Setting.** This is regression with squared loss. Examples $(x, y)$ are drawn i.i.d. from an unknown distribution $D$. Write

$$f(x) = \mathbb{E}[y \mid x], \qquad \sigma^2(x) = \mathbb{E}[(y - f(x))^2 \mid x],$$

so $y = f(x) + \varepsilon$ with $\mathbb{E}[\varepsilon \mid x] = 0$. The function $f$ is the regression function; for squared loss it is the best possible predictor (the [Bayes optimal](/bayes-optimal-classifier/) predictor), and $\sigma^2(x)$ is the smallest possible error at $x$. A learner takes a training set $S$ of $n$ examples and returns a predictor $\hat g_S$. Fix a test input $x_0$, and let $y_0$ be its label, drawn from $D$ given $x_0$ and independent of $S$. Define the average prediction $\bar g(x_0) = \mathbb{E}_S[\hat g_S(x_0)]$.

**Theorem (bias-variance decomposition).** If $y_0$ and $\hat g_S(x_0)$ have finite second moments, then

$$\mathbb{E}_{S, y_0}\big[(y_0 - \hat g_S(x_0))^2\big] = \underbrace{\sigma^2(x_0)}_{\text{noise}} + \underbrace{\big(f(x_0) - \bar g(x_0)\big)^2}_{\text{bias}^2} + \underbrace{\mathbb{E}_S\big[(\hat g_S(x_0) - \bar g(x_0))^2\big]}_{\text{variance}}.$$

*Proof.* Write $y_0 - \hat g_S(x_0) = a + b + c$ with $a = y_0 - f(x_0)$, $b = f(x_0) - \bar g(x_0)$ and $c = \bar g(x_0) - \hat g_S(x_0)$. Then $(a + b + c)^2 = a^2 + b^2 + c^2 + 2ab + 2ac + 2bc$. Take the expectation over $S$ and $y_0$, term by term.

1. $\mathbb{E}[a^2] = \sigma^2(x_0)$ by the definition of $\sigma^2$.
2. $b$ is a constant, so $\mathbb{E}[b^2] = b^2$, the squared bias.
3. $\mathbb{E}[c^2]$ is the variance of $\hat g_S(x_0)$, by definition.
4. $\mathbb{E}[ab] = b\, \mathbb{E}[a] = 0$, because $\mathbb{E}[y_0 \mid x_0] = f(x_0)$.
5. $a$ depends only on $y_0$ and $c$ depends only on $S$, and these are independent. So $\mathbb{E}[ac] = \mathbb{E}[a]\,\mathbb{E}[c] = 0 \cdot 0 = 0$.
6. $\mathbb{E}[bc] = b\, \mathbb{E}[c] = b\,(\bar g(x_0) - \bar g(x_0)) = 0$.

The sum of the three surviving terms is the claim. $\blacksquare$

Average both sides over $x_0 \sim D$ to get the same split for the expected test error of the learner, $\mathbb{E}_S[L_D(\hat g_S)]$. The three terms are then the mean noise (the Bayes risk), the mean squared bias and the mean variance.

**Why it is a tradeoff.** Bias and variance usually pull in opposite directions as the capacity of the [hypothesis class](/hypothesis-class/) grows. A class that holds functions close to $f$ can have a small bias; but a class that can fit many functions can also fit the noise of each sample, so its fits differ more from sample to sample. Geman, Bienenstock and Doursat (1992) named this the bias/variance dilemma for neural networks and nonparametric estimators. A [regularization](/regularization/) parameter, the degree of a polynomial, the number $k$ in [$k$-nearest neighbors](/k-nearest-neighbors/) or the width of a kernel moves a model along this axis. The classic picture is a U-shaped test error curve against capacity, with [overfitting](/overfitting/) on its right side.

**The U curve is not universal.** The identity says nothing about the shape of the curve. Belkin, Hsu, Ma and Mandal (2019) showed curves where the test error rises to a peak near the interpolation threshold (the capacity at which the model first fits the training set exactly) and then falls again as the capacity grows further. This is [double descent](/double-descent/). It does not contradict the decomposition, which holds at every capacity; only the shapes of the bias and variance curves differ from the classic picture.

**Other losses.** The exact additive split is a property of squared loss. For the zero-one loss of [classification](/classification/), there is no decomposition with these three nonnegative terms that always adds up. Domingos (2000) defines the bias through the *main prediction* (the most frequent prediction over training sets) and shows that the zero-one error is a weighted sum of noise, bias and variance in which variance adds to the error at unbiased points and subtracts from it at biased points. James (2003) separates, for a general loss, the *systematic effect* and the *variance effect* on the error from the bias and the variance themselves. These are analogues, not the same identity.

## Examples

**Polynomial regression.** Let $f(x) = \sin(2\pi x)$ on $[0, 1]$, with $x$ uniform and Gaussian noise of standard deviation $0.3$, so $\sigma^2 = 0.09$. Each training set has $n = 30$ examples, and the learner is the least squares polynomial of degree $p$. The table averages each term over 20 test inputs $x_0 = (j + 0.5)/20$, $j = 0, \ldots, 19$, and over 2000 training sets drawn with `random.Random(1)`. The column "sum" is noise plus bias$^2$ plus variance. The last column is a separate estimate of the test error: for each training set and each $x_0$, it draws a fresh noisy label $y_0$ and averages $(y_0 - \hat g_S(x_0))^2$.

| degree $p$ | bias$^2$ | variance | sum | measured test error |
|---|---|---|---|---|
| 0 | 0.5000 | 0.0196 | 0.6096 | 0.6102 |
| 1 | 0.1929 | 0.0219 | 0.3048 | 0.3058 |
| 3 | 0.0040 | 0.0169 | 0.1109 | 0.1110 |
| 5 | 0.0000 | 0.0560 | 0.1461 | 0.1461 |
| 6 | 0.0002 | 0.1510 | 0.2412 | 0.2430 |
| 7 | 0.0001 | 0.5181 | 0.6082 | 0.6116 |

With the empirical mean and variance over the 2000 sets, the sum equals the mean of $\sigma^2 + (f(x_0) - \hat g_S(x_0))^2$ to rounding error, as the proof says. The measured error differs from the sum only by the Monte Carlo error of the fresh labels. The bias falls with the degree and the variance rises; the error is lowest at $p = 3$ here. At degree 9 on 30 points the variance is about 96, because a few training sets leave a gap near an end of the interval and the polynomial swings far there. Degree 2 (not shown) has almost the same bias as degree 1 (0.1939), because $\sin(2\pi x)$ is odd around $x = 1/2$ and an even term does not help.

**$k$-nearest neighbors with fixed inputs.** Fix the training inputs $x_1, \ldots, x_n$ and let only the labels be random. The $k$-NN prediction at $x_0$ is the mean label of the $k$ nearest inputs $x_{(1)}, \ldots, x_{(k)}$, so its variance is $\sigma^2/k$ and its bias is $f(x_0) - \frac1k \sum_{l} f(x_{(l)})$:

$$\mathrm{Err}(x_0) = \sigma^2 + \Big(f(x_0) - \frac1k \sum_{l=1}^{k} f(x_{(l)})\Big)^2 + \frac{\sigma^2}{k}.$$

With $n = 20$ inputs $i/19$, the same $f$ and $\sigma^2 = 0.09$, averaged over the same 20 test inputs, the exact values are: $k = 1$ gives $0.09 + 0.0055 + 0.0900 = 0.1855$; $k = 3$ gives $0.09 + 0.0068 + 0.0300 = 0.1268$; $k = 8$ gives $0.09 + 0.0715 + 0.01125 = 0.1728$; $k = 20$ gives $0.09 + 0.5000 + 0.0045 = 0.5945$. Here capacity falls as $k$ grows: $k = 1$ has the smallest bias and the largest variance.

**Non-example: zero-one loss.** Take a classifier that is wrong at $x_0$ with probability 0.6 over training sets, with no label noise. Its main prediction is the wrong label, so it is biased at $x_0$, and its error there is 0.6. A classifier that always predicts the wrong label has the same bias, no variance and error 1. So at a biased point, more variance gave a smaller error; a squared loss decomposition can never do that.

## Where it is used

- **Model selection.** The choice of a degree, of $k$, of a tree depth or of a penalty weight is the choice of a point on the bias-variance axis. In practice it is made with a validation set or [cross-validation](/cross-validation/), because the terms need many training sets and the true $f$.
- **Regularization.** [Ridge regression](/ridge-regression/) adds bias to the least squares estimate and lowers its variance; for a well chosen penalty the sum is smaller. See [regularization](/regularization/).
- **Ensembles.** [Bagging](/bagging/) averages models fitted on bootstrap samples. The average has about the same bias and a smaller variance, which is why bagging helps most for unstable learners such as deep trees.
- **Theory of learning.** The split is close in spirit to the split of the excess risk into an approximation error and an estimation error, but it is not the same: bias and variance are taken at each input and over training sets, and only for squared loss. See [generalization error](/generalization-error/).

### Pitfalls

- **One data set does not give the terms.** Bias and variance are expectations over training sets. A single fit shows neither. Simulation (as above) or the bootstrap gives estimates.
- **The variance is over training sets,** not over the inputs $x$ and not over the noise of the test label.
- **The decomposition is for squared loss.** Do not add up "bias" and "variance" of a classifier as if they gave its zero-one error.
- **The noise term depends on the features.** $\sigma^2(x)$ is irreducible only for the given inputs. A new feature can lower it.
- **The U curve is an observation, not a theorem.** Test error can fall again past the interpolation threshold.

## References
