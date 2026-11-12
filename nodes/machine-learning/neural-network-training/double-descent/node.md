---
tag: E223P3
kind: concept
slug: double-descent
name: Double descent
aliases:
- model-wise double descent
- double descent risk curve
- epoch-wise double descent
- sample-wise double descent
area: machine-learning/neural-network-training
level: research
summary: "Test error can fall, rise to a peak near the interpolation threshold, and fall again as model size grows. For minimum norm least squares the peak is at p = n and is explained exactly."
prereqs: [bias-variance-tradeoff, overfitting, ordinary-least-squares, pseudoinverse]
see_also: [ridge-regression, least-squares-problem, kernel-ridge-regression, neural-tangent-kernel, early-stopping, regularization, generalization-error, gradient-descent]
sources:
  - paper: doi:10.1073/pnas.1903070116
    title: Mikhail Belkin, Daniel Hsu, Siyuan Ma and Soumik Mandal, Reconciling modern machine-learning practice and the classical bias-variance trade-off, PNAS 116(32), 2019
    locator: the double descent risk curve (Figure 1) and the experiments with random Fourier features, fully connected networks and random forests
  - url: https://arxiv.org/abs/1912.02292
    title: Preetum Nakkiran, Gal Kaplun, Yamini Bansal, Tristan Yang, Boaz Barak and Ilya Sutskever, Deep double descent, where bigger models and more data hurt, ICLR 2020
    locator: the effective model complexity, the generalized double descent hypothesis, and the model-wise, epoch-wise and sample-wise experiments
  - paper: doi:10.1214/21-AOS2133
    title: Trevor Hastie, Andrea Montanari, Saharon Rosset and Ryan J. Tibshirani, Surprises in high-dimensional ridgeless least squares interpolation, Annals of Statistics 50(2), 2022
    locator: pp. 949 to 986 (the limiting risk of the minimum norm interpolator for isotropic features as a function of gamma = p/n, and optimally tuned ridge)
  - paper: doi:10.1137/20M1336072
    title: Mikhail Belkin, Daniel Hsu and Ji Xu, Two models of double descent for weak features, SIAM Journal on Mathematics of Data Science 2(4), 2020
    locator: the exact finite sample risk of the minimum norm least squares fit with Gaussian features
  - paper: doi:10.1073/pnas.2001875117
    title: Marco Loog, Tom Viering, Alexander Mey, Jesse H. Krijthe and David M. J. Tax, A brief prehistory of double descent, PNAS 117(20), 2020
    locator: earlier observations of a peak in the learning curve at the interpolation threshold
---

Double descent is the shape of a test error curve that falls, rises to a peak, and falls again as the capacity of a model grows. The peak sits near the *interpolation threshold*, the smallest capacity at which the model can fit the training set exactly. Belkin, Hsu, Ma and Mandal (2019) named the curve, and Nakkiran et al. (2020) showed it for deep networks as a function of width, of training time and of the number of examples. For most models it is an observed curve; for [minimum norm least squares](/pseudoinverse/) with Gaussian features the peak at $p = n$ follows from an exact formula.

## In plain words

The classic advice says that a model with too many parameters [overfits](/overfitting/): the test error falls as the model grows, then rises again. Modern networks have far more parameters than training examples, and they still predict well. Double descent puts the two facts on one curve. As the model grows, the test error first follows the classic U. It is worst at the point where the model has just enough freedom to pass through every training example. There, the only fit that does so must bend hard to reach each noisy label. When the model grows further, many fits pass through every example, and the training method picks a smooth one among them. So the test error falls a second time.

## The idea

**Setting and notation.** There are $n$ training examples $(x_i, y_i)$, drawn i.i.d. from an unknown distribution $D$, and the loss is squared error. A model family is indexed by a capacity, for example the number $p$ of features of a linear model or the width of a network. The *interpolation threshold* is the smallest capacity at which the training procedure reaches zero training error. For a linear model on $p$ features in general position, it is $p = n$.

**The three forms.** Nakkiran et al. (2020) observed the peak in three ways for convolutional networks, ResNets and transformers trained by [stochastic gradient descent](/stochastic-gradient-descent/) or Adam:

- *Model-wise*: test error against width, at a fixed number of training steps.
- *Epoch-wise*: test error against the number of training steps, for a large model. A large model can pass the threshold during training, so [early stopping](/early-stopping/) at the first minimum is not always best.
- *Sample-wise*: test error against $n$, for a fixed model. Near the threshold, more data can make the test error larger, because the threshold moves with $n$.

They define the *effective model complexity* of a training procedure as the largest $n$ for which it reaches a training error of at most $\varepsilon$ on average, and state the *generalized double descent hypothesis*: the test error peaks when this complexity is close to $n$. It is a hypothesis drawn from experiments, not a theorem. In their experiments the peak is much stronger with label noise.

**The linear case, exactly.** Let $X$ be the $n \times p$ matrix of features and $y = X\beta + \epsilon$. The learner is the minimum norm least squares fit

$$\hat w = X^{+} y = \begin{cases} (X^\top X)^{-1} X^\top y, & p \le n, \\ X^\top (X X^\top)^{-1} y, & p > n, \end{cases}$$

for $X$ of full rank. For $p \le n$ it is [ordinary least squares](/ordinary-least-squares/). For $p > n$ it is the interpolant $X w = y$ with the smallest $\lVert w \rVert_2$. Each branch solves a linear system on the smaller side of $X$.

Take the isotropic model: the rows of $X$ are i.i.d. $N(0, I_p)$, the noise $\epsilon$ is $N(0, \sigma^2 I_n)$ and independent of $X$, and $\beta$ has norm $r$ and a uniformly random direction. For a test point $x \sim N(0, I_p)$, the excess risk of $\hat w$ is $\mathbb{E}_x[(x^\top(\hat w - \beta))^2] = \lVert \hat w - \beta \rVert^2$.

**Proposition.** In the isotropic model,

$$\mathbb{E}\,\lVert \hat w - \beta \rVert^2 = \begin{cases} \dfrac{\sigma^2 p}{n - p - 1}, & p \le n - 2, \\[2mm] r^2\Big(1 - \dfrac{n}{p}\Big) + \dfrac{\sigma^2 n}{p - n - 1}, & p \ge n + 2, \end{cases}$$

and the expectation is infinite for $n - 1 \le p \le n + 1$.

*Proof.* For $p \le n$, $\hat w - \beta = (X^\top X)^{-1} X^\top \epsilon$. Its squared norm has conditional mean $\sigma^2 \operatorname{tr}((X^\top X)^{-1})$ given $X$. The matrix $X^\top X$ is Wishart with $n$ degrees of freedom and scale $I_p$, and the mean of its inverse is $I_p/(n - p - 1)$ when $n \ge p + 2$, and does not exist otherwise. So the mean is $\sigma^2 p/(n - p - 1)$. For $p > n$, let $P = X^\top (X X^\top)^{-1} X$, the orthogonal projection onto the row space of $X$. Then $\hat w - \beta = -(I - P)\beta + X^\top (X X^\top)^{-1} \epsilon$. The second term has mean 0 given $X$, so the cross term vanishes. The row space is a uniformly random $n$-dimensional subspace, independent of the direction of $\beta$, so $\mathbb{E}\lVert (I - P)\beta \rVert^2 = r^2 (p - n)/p$. The second term has mean square $\sigma^2 \mathbb{E}\operatorname{tr}((X X^\top)^{-1})$, and $X X^\top$ is Wishart of size $n$ with $p$ degrees of freedom, so this is $\sigma^2 n/(p - n - 1)$ for $p \ge n + 2$. $\blacksquare$

Let $n, p \to \infty$ with $p/n \to \gamma$. The formulas tend to the limit risk of Hastie, Montanari, Rosset and Tibshirani (2022) for isotropic features:

$$R(\gamma) = \begin{cases} \sigma^2 \dfrac{\gamma}{1 - \gamma}, & \gamma < 1, \\[2mm] r^2\Big(1 - \dfrac{1}{\gamma}\Big) + \dfrac{\sigma^2}{\gamma - 1}, & \gamma > 1. \end{cases}$$

Both branches tend to infinity at $\gamma = 1$. The variance term is $\sigma^2$ times the sum of $1/s_k^2$ over the singular values $s_k$ of $X$. When $p$ is close to $n$, the smallest singular value is close to 0, and the noise is amplified without bound. Away from the threshold the singular values are bounded away from 0, and past it the bias term $r^2(1 - 1/\gamma)$ grows slowly while the variance term falls. This is the whole mechanism of the peak in the linear case.

**Why the minimum norm fit.** [Gradient descent](/gradient-descent/) on $\tfrac12 \lVert X w - y \rVert^2$ from $w_0 = 0$ with a step size below $2/s_{\max}^2$ converges to $X^{+} y$. Each step adds a multiple of $X^\top(Xw - y)$, so every iterate lies in the row space of $X$. The limit is an interpolant (for $p > n$) in the row space, and the only such interpolant is $X^{+} y$. So "train to zero training error with gradient descent" and "take the minimum norm interpolant" give the same model here. For networks, the implicit bias of the training method is not known in this exact form.

**What changes the peak.** The [bias-variance decomposition](/bias-variance-tradeoff/) still holds at every $p$; only the shape of the variance curve differs from the classic picture. Hastie et al. (2022) show that [ridge regression](/ridge-regression/) with the best penalty has no peak in the isotropic model. In the isotropic model the second descent need not go below the first minimum: with $r = 1$ and $\sigma = 0.5$, the best risk for $\gamma > 1$ is $0.75$ at $\gamma = 2$, while the risk tends to 0 as $\gamma \to 0$. In models where $\beta$ is fixed and the learner sees only the first $p$ of many features, the overparameterized side can win (Belkin, Hsu and Xu 2020).

## Examples

**The linear peak, by simulation.** Take $n = 20$, $r = 1$, $\sigma = 0.5$, and for each $p$ draw 200 independent data sets from the isotropic model with `random.Random(2024)`. The table gives the mean and the median of $\lVert \hat w - \beta \rVert^2$ over the 200 fits, the exact expectation from the proposition, and the limit $R(p/n)$.

| $p$ | mean | median | exact expectation | $R(p/n)$ |
|---|---|---|---|---|
| 5 | 0.098 | 0.074 | 0.089 | 0.083 |
| 10 | 0.285 | 0.241 | 0.278 | 0.250 |
| 15 | 1.054 | 0.732 | 0.938 | 0.750 |
| 18 | 3.071 | 1.868 | 4.500 | 2.250 |
| 19 | 20.27 | 3.188 | infinite | 4.750 |
| 20 | 2929.9 | 10.16 | infinite | infinite |
| 21 | 11.19 | 3.659 | infinite | 5.048 |
| 22 | 4.046 | 2.182 | 5.091 | 2.591 |
| 25 | 1.526 | 1.118 | 1.450 | 1.200 |
| 40 | 0.778 | 0.760 | 0.763 | 0.750 |
| 80 | 0.836 | 0.838 | 0.835 | 0.833 |
| 160 | 0.912 | 0.912 | 0.911 | 0.911 |

The peak is at $p = n = 20$. The mean there is dominated by a few data sets with a very small singular value, which is what an infinite expectation looks like in a finite sample; the median shows the same peak without the heavy tail. Far from the threshold the simulated means agree with the exact expectations. As $p \to \infty$ the risk tends to $r^2 = 1$, the risk of the zero predictor, because the fit sees a smaller and smaller part of $\beta$.

**Deep networks.** Nakkiran et al. (2020) trained ResNet18 models of growing width on CIFAR-10 with some labels replaced at random. The test error rose to a peak near the width at which the training error first reached zero, then fell for wider models. The same paper shows the epoch-wise peak for a fixed wide model. These are measured curves; their height and position depend on the label noise, the data augmentation and the optimizer.

**Non-example.** With a well tuned [regularization](/regularization/) penalty, or with early stopping chosen on validation data, the peak in the linear model shrinks or disappears. A U-shaped curve that never reaches zero training error, for example ridge with a large fixed penalty, has no interpolation threshold and shows no double descent.

## Where it is used

- **Choosing model size.** Past the threshold, a larger model is often not worse, so practitioners do not stop growing a network at the size that first fits the data. The worst size is the one that just interpolates.
- **Theory of interpolation.** Minimum norm least squares, random features models and [kernel ridge regression](/kernel-ridge-regression/) with a vanishing penalty are the test beds for the question why fits with zero training error can generalize. The [neural tangent kernel](/neural-tangent-kernel/) links wide networks to such kernel fits.
- **Regularization and early stopping.** The epoch-wise and model-wise peaks are reasons to tune the penalty or the stopping time on a validation set rather than by a rule of thumb.
- **Pitfalls.** The peak is not universal: it needs a training method that reaches zero training error and it grows with label noise. The location is the threshold of the training procedure, not a parameter count, so "more parameters than examples" is only a rough guide. A mean over a few seeds near the threshold can be dominated by one bad run; report medians too. The second descent is not always below the first minimum.

## References
