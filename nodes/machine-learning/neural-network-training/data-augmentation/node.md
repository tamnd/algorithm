---
tag: B4MG5J
kind: technique
slug: data-augmentation
name: Data augmentation
area: machine-learning/neural-network-training
level: intro
summary: "Train on randomly transformed copies of the examples, such as flips, crops, cutout or mixup. It acts as a regularizer and teaches the model invariances that the task has."
prereqs: [overfitting, empirical-risk-minimization, regularization]
see_also: [dropout, label-smoothing, adversarial-training, weight-decay, jensens-inequality, finite-group, variance, cross-entropy-loss]
sources:
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 7.4 (dataset augmentation)
  - url: https://arxiv.org/abs/1710.09412
    title: Hongyi Zhang, Moustapha Cisse, Yann N. Dauphin and David Lopez-Paz, mixup, beyond empirical risk minimization, ICLR 2018
    locator: Section 2 (mixup as vicinal risk minimization, λ drawn from Beta(α, α))
  - url: https://arxiv.org/abs/1708.04552
    title: Terrance DeVries and Graham W. Taylor, Improved regularization of convolutional neural networks with cutout, arXiv:1708.04552, 2017
    locator: the cutout method, a square patch with a random center that may extend past the border
  - url: https://jmlr.org/papers/v21/20-163.html
    title: Shuxiao Chen, Edgar Dobriban and Jane H. Lee, A group-theoretic framework for data augmentation, JMLR 21(245), 1 to 71, 2020
    locator: augmentation as averaging over the orbits of a group that leaves the data distribution unchanged, and the variance reduction of augmented empirical risk minimization
---

Data augmentation trains a model on randomly transformed copies of the training examples instead of on the examples alone. For images the classic transforms are horizontal flips, random crops after padding, small rotations and changes of color, all chosen so that the label stays correct. Cutout (DeVries and Taylor, 2017) also blanks a random square of the image. Mixup (Zhang, Cisse, Dauphin and Lopez-Paz, 2018) goes further: it trains on convex combinations $\lambda x_i + (1 - \lambda) x_j$ of two inputs, with the same combination of their labels. Augmentation can be seen in two ways. It is a [regularizer](/regularization/): it adds a data-dependent penalty to the training loss and reduces [overfitting](/overfitting/). And when the transforms form a group that leaves the data distribution unchanged, it teaches the model an invariance the task already has; averaging a model over the group then never increases a convex risk (Chen, Dobriban and Lee, 2020).

## In plain words

A model learns only from the examples it sees. If a picture of a cat, turned left to right, is still a picture of a cat, then each training picture gives a second, free example. Data augmentation makes such changed copies at random during training: turned pictures, shifted pictures, pictures with a small part covered, or two pictures blended together with a blended label. The model sees a new copy at each pass, so it cannot learn the training pictures by heart, and it learns that these changes do not matter for the answer. The changes must keep the answer correct: a turned 6 is a 9, so not every change is safe.

## When it applies

- **Data.** Any domain with transforms that keep the label: images (flips, crops, color), audio (time shifts, noise, changes of speed), text (word swaps, back-translation), and inputs with a known symmetry.
- **Part of the training loop.** The input pipeline. A fresh transform is drawn each time an example is used, so the model does not see the same copy twice.
- **Problem.** Overfitting when labelled data is scarce, and a need for invariance to transforms that the test data will contain.
- **Not for test time,** except as test-time augmentation, which averages the predictions over several transforms of one input.

## The template

Notation: $T$ is a family of label-preserving transforms with a probability distribution on it, and LOSS($\theta$; $x$, $y$) is the training loss of one example.

```pseudo id=template
AUGMENTED-TRAINING(θ, data, T, epochs)
L1  for epoch ← 1 to epochs:
L2      for each mini-batch B of data:
L3          for each (x, y) in B: draw t from T; replace (x, y) by (t(x), y)
L4          (optional mixup) draw λ ~ Beta(α, α) and a permutation π of B;
                replace (x_i, y_i) by (λ x_i + (1 − λ) x_π(i), λ y_i + (1 − λ) y_π(i))
L5          θ ← θ − η ∇_θ mean of LOSS(θ; x, y) over B
```

For mixup the labels $y$ are probability vectors over the $K$ classes, such as one-hot vectors, and the loss is the [cross-entropy](/cross-entropy-loss/) with a soft target.

**Cost.** One transform per example and step, which is cheap next to the forward and backward pass. The data set is not stored in augmented form, so the memory does not grow.

### Augmentation as a regularizer

Augmented training minimizes, in expectation over the transforms, $\frac1n\sum_i \mathbb{E}_t\, \mathrm{LOSS}(\theta; t(x_i), y_i)$.

**Claim 1.** For a linear model $w$, the squared loss and a finite set $G$ of transforms drawn uniformly, the augmented loss of one example is

$$\frac{1}{|G|}\sum_{g \in G} (w \cdot g x - y)^2 = (w \cdot \bar x - y)^2 + w^\top C_x w, \qquad \bar x = \frac{1}{|G|}\sum_g g x, \quad C_x = \frac{1}{|G|}\sum_g (g x - \bar x)(g x - \bar x)^\top .$$

*Proof.* For a uniform $g$, the prediction $z = w \cdot g x$ has mean $w \cdot \bar x$ and [variance](/variance/) $w^\top C_x w$, and $\mathbb{E}(z - y)^2 = (\mathbb{E}z - y)^2 + \operatorname{Var} z$. $\blacksquare$

So augmentation fits the orbit means and adds the penalty $\frac1n\sum_i w^\top C_{x_i} w$, which punishes the weights in the directions in which the transforms move the inputs. [Dropout](/dropout/) of the inputs is the same construction with random masks as the transforms, which gives its adaptive L2 penalty.

### Augmentation and invariance

Let a finite group $G$ act on the inputs (a [finite group](/finite-group/), such as the rotations of a signal or the flips of an image), and suppose that the pair $(gX, Y)$ has the same distribution as $(X, Y)$ for every $g \in G$. The orbit average of a predictor $f$ is $\bar f(x) = \frac{1}{|G|}\sum_{g} f(g x)$; it is invariant, $\bar f(g x) = \bar f(x)$.

**Claim 2.** If the loss $\ell(\hat y, y)$ is convex in $\hat y$, the risk $R(f) = \mathbb{E}\,\ell(f(X), Y)$ satisfies $R(\bar f) \le R(f)$. For the squared loss, $R(f) - R(\bar f) = \mathbb{E}\big[\operatorname{Var}_g f(gX)\big]$, with $g$ uniform on $G$.

*Proof.* By [Jensen's inequality](/jensens-inequality/) for each fixed $(X, Y)$, $\ell(\bar f(X), Y) \le \frac{1}{|G|}\sum_g \ell(f(gX), Y)$. Take expectations; by the invariance of the distribution, $\mathbb{E}\,\ell(f(gX), Y) = \mathbb{E}\,\ell(f(X), Y) = R(f)$ for each $g$. For the squared loss, the gap in Jensen's inequality for $u \mapsto (u - y)^2$ is exactly the variance of $f(gX)$ over $g$, whatever $y$ is, as in the proof of Claim 1. $\blacksquare$

Chen, Dobriban and Lee (2020) build a theory of augmentation on this group view. Augmented [empirical risk minimization](/empirical-risk-minimization/) averages the loss over orbits, and under exact invariance this reduces the variance of the fitted model without adding bias. When the transforms do not leave the distribution unchanged, augmentation can add bias, which is the formal side of "a turned 6 is a 9".

## Classic examples

**Flips and crops for images.** Krizhevsky, Sutskever and Hinton (2012) trained on random crops of the training images and their mirror images. The usual recipe for 32 by 32 images pads by 4 pixels with zeros, cuts a random 32 by 32 window, and flips it with probability one half.

**Cutout.** Choose a center uniformly over the image and set to zero a square of fixed size around it; the square may stick out of the image, and only the part inside is zeroed. On a 6 by 7 image of ones with a 3 by 3 square, the number of zeros is 9 for a center away from the border, 6 for a center on an edge, and 4 for a corner.

**Mixup.** Take $\lambda = 0.7$, inputs $x_i = (1, 0)$ and $x_j = (0, 1)$ with labels class 1 and class 3 of $K = 3$. The mixed example is $\tilde x = (0.7, 0.3)$ with target $\tilde y = (0.7, 0, 0.3)$. The cross-entropy is linear in the target, so for any predicted probabilities $p$,

$$H(\tilde y, p) = 0.7\,(-\log p_1) + 0.3\,(-\log p_3),$$

the same mix of the two losses. Zhang et al. draw $\lambda \sim \mathrm{Beta}(\alpha, \alpha)$. On ImageNet they use a small $\alpha$, from 0.1 to 0.4, so most $\lambda$ are near 0 or 1. On CIFAR-10 they use $\alpha = 1$, so $\lambda$ is uniform on $[0, 1]$.

**The regularizer on one example.** For cyclic rotations of $x = (1, 0, 0, 2)$, $w = (1, 0, 0, 0)$ and $y = 1$, the four rotations give the predictions $1, 2, 0, 0$ and the squared errors $0, 1, 1, 1$, with mean $3/4$. In Claim 1, $w \cdot \bar x = 3/4$, so the fit term is $1/16$, and the penalty is the variance of $\{1, 2, 0, 0\}$, which is $11/16$.

**Invariance by averaging.** Let $X$ be uniform on $\{0, 1\}^4$, $Y = X_1 + X_2 + X_3 + X_4 \pm 1/2$ with a fair sign, and $G$ the cyclic rotations, which leave $(X, Y)$ unchanged. The predictor $f(x) = x_1 + 2x_2 - x_4 + 1/3$ has squared risk $79/36$. Its orbit average $\bar f(x) = \frac12\sum_j x_j + 1/3$ has risk $17/18$, and the gap $5/4$ is the mean variance of $f$ over the orbits.

## Variations

- **Learned or searched policies,** which choose the kinds and strengths of transforms by a search on validation error, and random combinations of a few strong transforms.
- **CutMix** pastes a patch of one image into another and mixes the labels in proportion to the area.
- **Noise injection.** Adding Gaussian noise to the inputs is augmentation by random translations; for a linear model with squared loss it gives exactly the penalty of [ridge regression](/ridge-regression/), by the argument of Claim 1.
- **[Adversarial training](/adversarial-training/)** uses the worst transform in a small ball instead of a random one.
- **Test-time augmentation** averages the predictions over several transforms of each test input, which is a sample of the orbit average $\bar f$.
- **Consistency training** in semi-supervised learning asks that the predictions on two transforms of the same unlabelled input agree.

## Pitfalls

- **Transforms that change the label.** A vertical flip of a digit, a crop that removes the object, or a color change when color is the class, all teach wrong labels. Claim 2 needs the invariance to hold.
- **Augmenting the validation or test set by mistake.** The validation set must look like the real test data, or [early stopping](/early-stopping/) and model selection use a wrong error.
- **Leakage.** Augmented copies of one example must stay on the same side of a train and validation split.
- **Mixup with a wrong loss.** The mixed label is a soft target; a loss that takes a class index, or a one-hot label taken by rounding, loses the mix. Mixup also changes the calibration of the predicted probabilities, which matters if they are used as such.
- **Too strong a policy for a small model.** Strong augmentation makes the training task harder and can underfit; the strength is a hyperparameter like any penalty.

## Exercises

1. Show that the orbit average $\bar f$ is invariant, $\bar f(h x) = \bar f(x)$ for every $h \in G$, using that $g \mapsto g h$ is a bijection of $G$.
2. Show that for a linear model with squared loss and additive noise $x \mapsto x + \epsilon$, $\epsilon \sim N(0, \sigma^2 I)$, the expected augmented loss is the squared loss plus $\sigma^2\|w\|^2$.
3. In the mixup template with one-hot labels, show that the expected mixed target is not the label of $x_i$, and compute the expected weight of the label of $x_i$ when $\lambda \sim \mathrm{Beta}(\alpha, \alpha)$.
4. Give a distribution and a group for which $(gX, Y)$ does not have the distribution of $(X, Y)$, and a predictor $f$ with $R(\bar f) > R(f)$.
5. For cutout with a square of side $s$ on an $h \times w$ image, compute the expected number of zeroed pixels when the center is uniform.

## References
