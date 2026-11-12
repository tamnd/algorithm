---
tag: 3J0J4Q
kind: concept
slug: overfitting
name: Overfitting
aliases:
- overfit
- overtraining
area: machine-learning/supervised-learning
level: intro
summary: "A learned model fits its training examples, noise included, much better than new data, so its training error is low and its true error is high. A validation set detects it."
prereqs: [generalization-error]
see_also: [bias-variance-tradeoff, regularization, cross-validation, early-stopping, empirical-risk-minimization, structural-risk-minimization, double-descent, cost-complexity-pruning]
sources:
  - book: isbn:9780070428072
    title: Tom M. Mitchell, Machine Learning, McGraw-Hill, 1997
    locator: Section 3.6.1 (the definition of overfitting, with the decision tree example)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Section 2.2.1 (overfitting of empirical risk minimization) and Section 11.2 (validation)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 7.2 (training error and test error against model complexity) and Section 7.10 (cross-validation)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 5.2 (capacity, overfitting and underfitting) and Section 7.8 (early stopping)
  - paper: doi:10.1073/pnas.1907378117
    title: Peter L. Bartlett, Philip M. Long, Gábor Lugosi and Alexander Tsigler, Benign overfitting in linear regression, PNAS 117(48), 2020
    locator: the conditions under which the minimum norm interpolant of noisy data has a small excess risk
---

Overfitting is what happens when a learner fits its training sample better than the sample deserves: it follows the noise and the accidents of the sample, so its training error is small and its [generalization error](/generalization-error/) is much larger. A learner overfits more easily when its hypothesis class has a large capacity compared with the number of training examples. A held-out validation set, or [cross-validation](/cross-validation/), detects it, and [regularization](/regularization/), [early stopping](/early-stopping/), a smaller class or more data reduce it.

## In plain words

A student who learns the answers to last year's exam by heart can score full marks on that exam and still fail a new one. A model can do the same. If it has enough freedom, it can pass exactly through every training example, including the ones whose labels are wrong or noisy. Then it looks perfect on the data it has seen and does badly on new data. The cure is to check the model on data it did not see during training, and to limit its freedom: give it fewer parameters, punish complex models, stop training sooner, or give it more examples. The opposite problem, a model too simple to follow the real pattern, is called underfitting.

## The idea

**Setting.** Examples are drawn i.i.d. from an unknown distribution $D$. A learner picks $h_S$ from a [hypothesis class](/hypothesis-class/) $H$ using a training sample $S$ of $n$ examples. $L_S(h)$ is the training error and $L_D(h)$ the true risk, for a stated loss.

**Definition.** Mitchell (1997, Section 3.6.1) gives the standard definition: a hypothesis $h \in H$ *overfits* the training data if some other $h' \in H$ has

$$L_S(h) < L_S(h') \quad \text{and} \quad L_D(h) > L_D(h').$$

So overfitting is a relation between hypotheses, not a property of a number. In practice one says that a learner overfits when the gap $L_D(h_S) - L_S(h_S)$ is large and a less flexible choice would have a smaller $L_D$. *Underfitting* is the other side: both errors are high, because $H$ has no hypothesis close to the target.

**Why capacity matters.** If $H$ can fit any labeling of $n$ points (it shatters them, in the sense of the [VC dimension](/vc-dimension/)), then a training error of zero says nothing about $D$: the [no free lunch theorem](/no-free-lunch-theorem-learning/) builds distributions where such a learner has a large true error. [Empirical risk minimization](/empirical-risk-minimization/) over a class that is too rich for $n$ is the textbook way to overfit. Shalev-Shwartz and Ben-David (Section 2.2.1) give the extreme case: a predictor that returns the stored label on a training point and 0 elsewhere has training error 0, and when the positive region has probability $1/2$ and the domain is continuous, its true error is $1/2$. The bounds of [generalization error](/generalization-error/) theory say how large $n$ must be for a given capacity to keep the gap small.

**Capacity is not only the parameter count.** The effective capacity depends on the class, the algorithm and its stopping rule. A penalty on the weights, or a gradient method stopped early, explores only part of a large class. Very large models trained to fit their data exactly sometimes generalize well; this is studied as [double descent](/double-descent/) and as *benign overfitting* (Bartlett, Long, Lugosi and Tsigler 2020 give exact conditions for linear regression). These results do not remove the problem: they say when interpolation of noise is harmless, and in many settings it is not.

**Detection.** The training error cannot detect overfitting, because it falls as capacity rises. Set aside a validation sample $V$ that the learner does not use, and compare $L_S(h_S)$ with $L_V(h_S)$. Because $h_S$ does not depend on $V$, $L_V(h_S)$ is an unbiased estimate of $L_D(h_S)$, with Hoeffding error about $\sqrt{\ln(2/\delta)/(2|V|)}$ for a loss in $[0, 1]$. Plot both errors against a capacity knob (degree, depth, number of training epochs, inverse penalty). Overfitting shows as a training error that keeps falling while the validation error rises. [Cross-validation](/cross-validation/) does the same with less waste of data. A learning curve (the errors against $n$) shows whether more data would help: a large gap that shrinks with $n$ points to variance.

**Remedies.**

- More training data, which shrinks the gap for a fixed class.
- A smaller class: fewer features, a lower degree, a shallower tree, or [pruning](/cost-complexity-pruning/).
- [Regularization](/regularization/): a penalty such as $\lambda \|w\|_2^2$ or $\lambda \|w\|_1$, or a constraint on the norm.
- [Early stopping](/early-stopping/) of an iterative method, chosen by the validation error.
- Averaging, as in [bagging](/bagging/), which lowers the variance part of the error ([bias-variance tradeoff](/bias-variance-tradeoff/)).
- For neural networks, [dropout](/dropout/), [weight decay](/weight-decay/) and [data augmentation](/data-augmentation/).

## Examples

**Polynomials on 12 points.** Draw 12 training points with $x$ uniform on $[0, 1]$ and $y = \sin(2\pi x)$ plus Gaussian noise of standard deviation 0.3, and 50 validation points from the same source, with `random.Random(4)`. Fit the least squares polynomial of each degree $p$. The true risk is $0.09 + \int_0^1 (\sin 2\pi x - \hat g(x))^2 dx$, computed on a grid of 2000 points.

| degree $p$ | training MSE | validation MSE | true risk |
|---|---|---|---|
| 0 | 0.7341 | 0.5910 | 0.6789 |
| 1 | 0.1914 | 0.3185 | 0.3366 |
| 3 | 0.0693 | 0.1498 | 0.1277 |
| 4 | 0.0689 | 0.1511 | 0.1245 |
| 5 | 0.0581 | 0.2452 | 0.2358 |
| 7 | 0.0549 | 0.6211 | 0.5676 |
| 9 | 0.0218 | 144.9 | 129.3 |
| 11 | 0.0000 | $2.1 \times 10^{7}$ | $1.8 \times 10^{7}$ |

The training error never rises with the degree, because each class contains the one before it. At degree 11 the polynomial passes through all 12 points, noise included. The validation error picks degree 3, whose true risk 0.1277 is within 0.004 of the best one in the table (0.1245 at degree 4). Below degree 3 the model underfits; above degree 4 it overfits, and from degree 8 on it swings wildly between the training points.

**Memorizing a table.** A learner that stores the training pairs and answers 0 elsewhere has training error 0 on every sample with distinct inputs. If the labels are fair coins independent of $x$, every classifier has true risk $1/2$, so this learner has the largest possible gap of $1/2$; see [generalization error](/generalization-error/).

**Non-example: a high training error.** A linear fit to $\sin(2\pi x)$ has a training error near 0.19 and a similar validation error. Its true error is high, but it does not overfit: no simpler model does better on new data. It underfits.

## Where it is used

- **Model selection.** The choice of degree, depth, $k$ in [$k$-nearest neighbors](/k-nearest-neighbors/), the penalty weight or the number of boosting rounds is a choice against overfitting, made on validation data or by [cross-validation](/cross-validation/).
- **Learning theory.** [Structural risk minimization](/structural-risk-minimization/) and [minimum description length](/minimum-description-length/) add a capacity term to the training error, to choose a class that does not overfit.
- **Decision trees.** A fully grown tree fits its training set exactly. [Cost-complexity pruning](/cost-complexity-pruning/) and [reduced-error pruning](/reduced-error-pruning/) cut it back.
- **Neural network training.** Training is stopped, or the weights are penalized, when the validation loss stops falling.

### Pitfalls

- **Overfitting the validation set.** If many models are compared on one validation set, the best validation score is optimistic. Keep a final test set that is used once.
- **Leakage.** A preprocessing step (scaling, feature selection) fitted on all the data before the split lets information from the validation set into training, and hides overfitting.
- **Reading a small gap as success.** A small gap with a large error is underfitting.
- **Reading interpolation as failure.** A model with zero training error can still generalize well in some regimes; judge it on held-out data, not by its training error.

## References
