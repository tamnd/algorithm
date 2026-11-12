---
tag: 8V15DT
kind: technique
slug: dropout
name: Dropout
aliases:
- inverted dropout
area: machine-learning/neural-network-training
level: intro
summary: "During training, keep each unit with probability p and scale the kept units by 1/p, so test time needs no change. For linear regression it equals an adaptive L2 penalty."
prereqs: [backpropagation, regularization, expected-value]
see_also: [ridge-regression, overfitting, weight-decay, data-augmentation, ensemble-learning, bagging, variance, bayesian-inference]
sources:
  - url: https://jmlr.org/papers/v15/srivastava14a.html
    title: Nitish Srivastava, Geoffrey Hinton, Alex Krizhevsky, Ilya Sutskever and Ruslan Salakhutdinov, Dropout, a simple way to prevent neural networks from overfitting, JMLR 15, 1929 to 1958, 2014
    locator: Section 4 (the model and the test-time scaling of the weights by p), Section 5.1 (backpropagation with dropout and the max-norm constraint), Section 7.5 (Monte Carlo averaging against weight scaling), Section 9.1 (linear regression with dropout as ridge regression with a diagonal penalty)
  - url: https://arxiv.org/abs/1207.0580
    title: Geoffrey E. Hinton, Nitish Srivastava, Alex Krizhevsky, Ilya Sutskever and Ruslan R. Salakhutdinov, Improving neural networks by preventing co-adaptation of feature detectors, arXiv:1207.0580, 2012
    locator: the first description of dropout and of halving the outgoing weights at test time
  - url: https://arxiv.org/abs/1307.1493
    title: Stefan Wager, Sida Wang and Percy Liang, Dropout training as adaptive regularization, NIPS 2013
    locator: Section 2 (dropout for generalized linear models as an adaptive L2 penalty, exact for linear regression)
  - url: https://proceedings.mlr.press/v48/gal16.html
    title: Yarin Gal and Zoubin Ghahramani, Dropout as a Bayesian approximation, representing model uncertainty in deep learning, ICML 2016, PMLR 48
    locator: Monte Carlo dropout at test time
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 7.12 (dropout, the weight scaling inference rule)
---

Dropout (Hinton et al., 2012; Srivastava et al., 2014) is a [regularization](/regularization/) method for neural networks. At each training step it multiplies each unit of a layer by an independent random mask entry $m_i$, which is 1 with probability $p$ (the keep probability) and 0 otherwise, so a fresh random subnetwork is trained at every step. In the usual form, inverted dropout, the kept units are also divided by $p$, so that the [expected value](/expected-value/) of each unit is unchanged; at test time the network is then used as it is, with no mask and no scaling. For a linear model with squared loss, the expected training loss under dropout of the inputs is exactly the squared loss plus an L2 penalty whose weight for each feature is set by the data (Wager, Wang and Liang, 2013).

## In plain words

During training, dropout switches off a random part of the units of a layer at each step, a new random part each time. The units that stay on are made stronger by the right amount, so that on average each unit passes on the same value as without dropout. No unit can count on a given other unit being there, so each unit must learn something useful on its own, and the network cannot fit the training data with fragile teamwork. When the network is used after training, all units stay on and nothing else changes. For a simple straight-line model the method has an exact meaning: it adds a cost on large weights, with a larger cost on the weights of features with large values.

## When it applies

- **Architecture.** Fully connected layers, the inputs of a network, and the non-recurrent connections of recurrent networks. On convolutional feature maps whole channels are usually dropped instead of single units.
- **Part of the training loop.** A random layer in the forward pass during training, with the same mask reused in the backward pass. At test time it is the identity.
- **Problem.** [Overfitting](/overfitting/) of a large network on a limited training set.
- **Typical values.** Srivastava et al. use $p = 0.5$ for hidden units and a value near 0.8 for input units.

## The template

Notation: $h \in \mathbb{R}^d$ is the vector of activations of one layer for one example, and $p \in (0, 1]$ is the keep probability.

```pseudo id=template
DROPOUT-FORWARD(h, p, training)
L1  if not training: return h                    ▷ test time: no mask, no scaling
L2  for i ← 1 to d: draw m_i ← 1 with probability p, else 0
L3  return (m_1 h_1 / p, ..., m_d h_d / p), and keep m

DROPOUT-BACKWARD(g, m, p)                       ▷ g = ∂L/∂(output)
L4  return (m_1 g_1 / p, ..., m_d g_d / p)
```

**Cost.** $\Theta(d)$ random draws and multiplications per example, and $d$ bits of mask memory until the backward pass. This is small next to the $\Theta(d^2)$ cost of the dense layer that follows.

### The scaling

**Claim 1.** For a fixed $h$, the output $\tilde h_i = m_i h_i/p$ of line L3 has $\mathbb{E}[\tilde h_i] = h_i$ and $\operatorname{Var}[\tilde h_i] = \frac{1-p}{p} h_i^2$.

*Proof.* $m_i$ takes the value 1 with probability $p$, so $\mathbb{E}[m_i] = \mathbb{E}[m_i^2] = p$. Then $\mathbb{E}[\tilde h_i] = p h_i/p = h_i$ and $\mathbb{E}[\tilde h_i^2] = p h_i^2/p^2 = h_i^2/p$, so the [variance](/variance/) is $h_i^2/p - h_i^2$. $\blacksquare$

So the input of the next linear layer $W \tilde h$ has expectation $W h$, the input it gets at test time. The original form multiplies by $m_i$ only and scales the outgoing weights by $p$ at test time; it gives the same expected values. For a network with nonlinear units the expected output under random masks is not the output of the network without masks, so the test-time rule is an approximation of the average over all $2^d$ subnetworks (Srivastava et al., Section 7.5).

### Linear regression: an adaptive L2 penalty

**Claim 2.** For a linear model with weights $w \in \mathbb{R}^d$, an example $(x, y)$ and dropout with keep probability $p$ on the inputs,

$$\mathbb{E}_m\Big[\big(y - w \cdot (m \odot x)/p\big)^2\Big] = (y - w \cdot x)^2 + \frac{1-p}{p}\sum_{j=1}^d w_j^2 x_j^2 .$$

*Proof.* Let $z = \sum_j w_j m_j x_j/p$. By [linearity of expectation](/linearity-of-expectation/) and Claim 1, $\mathbb{E}[z] = w \cdot x$. The $m_j$ are independent, so $\operatorname{Var}[z] = \sum_j w_j^2 \operatorname{Var}[m_j x_j/p] = \frac{1-p}{p}\sum_j w_j^2 x_j^2$. For any random $z$, $\mathbb{E}[(y - z)^2] = (y - \mathbb{E}z)^2 + \operatorname{Var} z$. $\blacksquare$

Summed over the $n$ rows of the data matrix $X$,

$$\sum_{i} \mathbb{E}_m\big[(y_i - w \cdot (m \odot x_i)/p)^2\big] = \|y - X w\|^2 + \frac{1-p}{p}\, w^\top \operatorname{diag}(X^\top X)\, w,$$

which is [ridge regression](/ridge-regression/) with the penalty $\lambda_j = \frac{1-p}{p}\sum_i x_{ij}^2$ on $w_j$. Its minimizer is

$$w^\star = \Big(X^\top X + \tfrac{1-p}{p}\operatorname{diag}(X^\top X)\Big)^{-1} X^\top y .$$

Srivastava et al. (Section 9.1) give the same result for the original, non-inverted form. Wager, Wang and Liang (2013) show that for generalized linear models, such as logistic regression, a second-order expansion of the expected loss gives the same kind of penalty, with the diagonal of the Fisher information in place of $\operatorname{diag}(X^\top X)$. The penalty is adaptive: it depends on the data. Unlike ridge regression with one $\lambda$, it does not change when a feature is multiplied by a constant $c$, because $w_j$ is then divided by $c$ and $w_j^2 \sum_i x_{ij}^2$ stays the same.

## Classic examples

**One example by hand.** Take $x = (1, 2)$, $w = (1, 1)$, $y = 4$ and $p = 1/2$. The four masks, each with probability $1/4$, give the predictions $0, 2, 4, 6$ (inputs scaled by 2) and the squared errors $16, 4, 0, 4$, with mean 6. Claim 2 gives $(4 - 3)^2 + 1 \cdot (1 + 4) = 6$.

**Linear regression on five points.** Take the rows $(1, 0), (0, 1), (1, 1), (2, 1), (1, 3)$ with targets $1, 2, 2, 4, 5$. Then $X^\top X = \begin{pmatrix} 7 & 6 \\ 6 & 12 \end{pmatrix}$ and $X^\top y = (16, 23)$.

| keep probability $p$ | $w^\star$ |
|---|---|
| 1 (no dropout, least squares) | $(9/8, 65/48) \approx (1.125, 1.354)$ |
| 0.8 | $(136/127, 421/381) \approx (1.071, 1.105)$ |
| 0.5 | $(41/50, 113/150) = (0.82, 0.753)$ |

Stochastic gradient descent with inverted dropout on the inputs, step size 0.005 and 4000 passes over the data in random order (seeded with `random.Random(3)`), with the iterates averaged over the second half, ends near $(0.81, 0.75)$, the last row of the table.

## Variations

- **DropConnect** drops single weights instead of units.
- **Spatial dropout** drops whole channels of a convolutional feature map, since neighbouring pixels in a channel are strongly correlated and dropping single pixels has little effect.
- **Gaussian dropout** multiplies each unit by a Gaussian with mean 1 and variance $(1-p)/p$, which has the same first two moments as inverted dropout (Srivastava et al., Section 10).
- **Monte Carlo dropout** (Gal and Ghahramani, 2016) keeps dropout on at test time and averages several random forward passes, which estimates the predictive mean and gives a spread that is used as a measure of uncertainty.
- **Dropout as an ensemble.** Training with dropout trains an exponential number of subnetworks that share weights, which is related to [bagging](/bagging/) and [ensemble learning](/ensemble-learning/).

## Pitfalls

- **Keep probability or drop probability.** Papers use $p$ for the keep probability, while many libraries take the drop probability $1 - p$ as their argument.
- **Forgetting the training flag.** Dropout must be off in evaluation, or the predictions are random. Mixing the two forms is also wrong: masks without the $1/p$ scaling in training, with the network unchanged at test time, make each layer get inputs at test time that are larger by the factor $1/p$ on average than in training.
- **Different statistics in training and in use.** Claim 1 matches the means but not the variances, so a layer after dropout sees a larger variance in training than at test time. This can shift the running statistics of [batch normalization](/batch-normalization/) placed after dropout.
- **The same mask for the backward pass.** The gradient must use the mask of the forward pass; drawing a new mask is a different, wrong gradient.
- **The noise of the masks.** Claim 2 holds for the expected loss. With few training steps, the noise of the masks adds variance to the gradient, and the iterates of stochastic gradient descent need a small step or averaging to settle near $w^\star$.

## Exercises

1. Show that for any random $z$ with finite variance, $\mathbb{E}[(y - z)^2] = (y - \mathbb{E} z)^2 + \operatorname{Var} z$.
2. Derive the penalty for dropout with keep probability $p$ applied to the hidden layer of a model $y = v^\top \phi(W x)$ with the first layer fixed, and compare it with Claim 2.
3. For the original form, with $\tilde h_i = m_i h_i$ and weights scaled by $p$ at test time, show that the trained weights equal those of inverted dropout multiplied by $1/p$.
4. Show that the minimizer $w^\star$ of Claim 2 does not change when one column of $X$ is multiplied by $c \ne 0$ and $w_j^\star$ is divided by $c$, and give an example where ridge regression with one $\lambda$ does change.
5. For a single sigmoid unit with input dropout, give an example where the expected output under the masks differs from the output at test time.

## References
