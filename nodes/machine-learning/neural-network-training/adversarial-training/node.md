---
tag: SQBJ92
kind: technique
slug: adversarial-training
name: Adversarial training
aliases:
- adversarial example training
- PGD adversarial training
- Madry adversarial training
- FGSM adversarial training
area: machine-learning/neural-network-training
level: advanced
summary: "Train on inputs perturbed within a small ball to maximize the loss: a min max problem whose inner step is solved by FGSM or PGD. It buys robustness at some cost in clean accuracy."
prereqs: [logistic-loss, projected-gradient-descent, stochastic-gradient-descent, minimax]
see_also: [minimax-theorem, logistic-regression, weight-decay, data-augmentation, regularization, lasso-regression, sharpness-aware-minimization]
sources:
  - url: https://arxiv.org/abs/1312.6199
    title: Christian Szegedy, Wojciech Zaremba, Ilya Sutskever, Joan Bruna, Dumitru Erhan, Ian Goodfellow and Rob Fergus, Intriguing properties of neural networks, ICLR 2014
    locator: Section 4 (adversarial examples found by box-constrained L-BFGS, and their transfer between models)
  - url: https://arxiv.org/abs/1412.6572
    title: Ian J. Goodfellow, Jonathon Shlens and Christian Szegedy, Explaining and harnessing adversarial examples, ICLR 2015
    locator: Section 3 (the linear explanation), Section 4 (the fast gradient sign method), Section 5 (adversarial training of linear models versus weight decay), Section 6 (the adversarial objective for deep networks)
  - url: https://arxiv.org/abs/1706.06083
    title: Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt, Dimitris Tsipras and Adrian Vladu, Towards deep learning models resistant to adversarial attacks, ICLR 2018
    locator: Section 2 (the saddle point formulation and projected gradient descent with random starts), Appendix A (Danskin's theorem for the outer gradient)
  - url: https://arxiv.org/abs/1802.00420
    title: Anish Athalye, Nicholas Carlini and David Wagner, Obfuscated gradients give a false sense of security, ICML 2018
    locator: defenses that mask gradients, and attacks that break them
  - url: https://arxiv.org/abs/1805.12152
    title: Dimitris Tsipras, Shibani Santurkar, Logan Engstrom, Alexander Turner and Aleksander Madry, Robustness may be at odds with accuracy, ICLR 2019
    locator: a data distribution where any robust classifier has lower clean accuracy
  - url: https://arxiv.org/abs/2001.03994
    title: Eric Wong, Leslie Rice and J. Zico Kolter, Fast is better than free, revisiting adversarial training, ICLR 2020
    locator: FGSM training with a random start, and catastrophic overfitting
  - url: https://arxiv.org/abs/2002.11569
    title: Leslie Rice, Eric Wong and J. Zico Kolter, Overfitting in adversarially robust deep learning, ICML 2020
    locator: robust overfitting, and early stopping as the remedy
---

Adversarial training makes a classifier resistant to small worst case changes of its input by training it on such changes. Madry et al. (2018) write it as the min max problem $\min_\theta \mathbb{E}\, \max_{\lVert \delta \rVert_\infty \le \epsilon} L(\theta, x + \delta, y)$: an attacker picks the perturbation that most increases the loss, and the learner minimizes the loss at the attacked point. Goodfellow, Shlens and Szegedy (2015) proposed the one step attack FGSM, $\delta = \epsilon \operatorname{sign}(\nabla_x L)$, Kurakin, Goodfellow and Bengio (2017) repeated it in small steps, and Madry et al. used this multi step attack with a random start, PGD, projected gradient ascent with sign steps. For a linear model the inner maximum has a closed form, $\ell(y\, w^\top x - \epsilon \lVert w \rVert_1)$, which makes adversarial training a kind of $L_1$ penalty inside the loss.

## In plain words

A network that sorts images can often be fooled by a tiny change to the pixels that a person cannot see. Such a changed input is an adversarial example. Adversarial training makes the network learn from these examples. For each training example, an attacker first searches, within a small allowed change, for the version that the network gets most wrong. Then the network trains on that version, with the correct label. The network learns to rely on features that a small change cannot flip. The cost is more training time, since each step includes an attack, and usually a lower accuracy on normal inputs.

## When it applies

- **A threat model is fixed.** The allowed changes form a set $S$, usually a ball $\lVert \delta \rVert_p \le \epsilon$ in the $\ell_\infty$ or $\ell_2$ norm, intersected with the valid input range such as $[0, 1]^d$ for pixels. The robustness obtained is for this set only.
- **The loss is differentiable in the input,** so that gradient based attacks can find strong perturbations. The training architecture is any differentiable network.
- **Robustness is worth its price.** Training costs about $K + 1$ times more with a $K$ step attack, and clean accuracy usually drops.

## The template

The data model: examples $(x, y)$, a network $f_\theta$, a loss $L(\theta, x, y)$, a perturbation set $S = \{\delta : \lVert \delta \rVert_\infty \le \epsilon\}$. The robust objective is

$$\min_\theta\ \rho(\theta), \qquad \rho(\theta) = \mathbb{E}_{(x, y)} \Big[ \max_{\delta \in S} L(\theta, x + \delta, y) \Big].$$

This is a [minimax](/minimax/) problem, but the order matters: the attacker moves after the learner and separately for each example, so it is not a [saddle point](/minimax-theorem/) problem of the classic convex-concave kind.

For each minibatch:

1. **Inner maximization (attack).** For each example, start at $x^0 = x + u$ with $u$ uniform in $S$ (or $u = 0$), and run $K$ steps of projected sign ascent:
$$x^{t+1} = \Pi_{x + S}\Big( x^t + \alpha \operatorname{sign}\big(\nabla_x L(\theta, x^t, y)\big) \Big),$$
where $\Pi$ clips each coordinate to $[x_i - \epsilon, x_i + \epsilon]$ and to the valid range. This is PGD. With $K = 1$, $\alpha = \epsilon$ and $u = 0$ it is FGSM.
2. **Outer minimization.** Take a [stochastic gradient](/stochastic-gradient-descent/) step on $\theta$ with the gradient $\nabla_\theta L(\theta, x^K, y)$ at the attacked inputs. Goodfellow et al. mix the clean and the adversarial loss, $\beta L(\theta, x, y) + (1 - \beta) L(\theta, x^K, y)$; Madry et al. use the adversarial loss alone.

**Why the sign.** The step $\operatorname{sign}(g)$ maximizes $g^\top \delta$ over $\lVert \delta \rVert_\infty \le 1$: it is the steepest ascent direction for the $\ell_\infty$ norm. For an $\ell_2$ ball, the step is $g / \lVert g \rVert_2$ and the projection rescales onto the ball. PGD is [projected gradient descent](/projected-gradient-descent/) on $-L$ with this normalized step.

**Why the outer gradient is right (Danskin's theorem).** Let $\phi(\theta) = \max_{\delta \in S} L(\theta, x + \delta, y)$ with $S$ compact and $L$ continuously differentiable in $\theta$. If the maximizer $\delta^*$ is unique, then $\phi$ is differentiable and $\nabla \phi(\theta) = \nabla_\theta L(\theta, x + \delta^*, y)$. So the gradient at the attacked point is the gradient of the robust objective, provided the attack finds the maximizer. For a network the inner problem is not concave and PGD finds only a local maximizer; Madry et al. report that PGD from many random starts finds maxima with similar loss values, which is evidence, not proof, that PGD gets close.

**The linear case is exact.** Let $f(x) = w^\top x + b$, $y \in \{-1, +1\}$, and $L = \ell(y f(x))$ with a decreasing loss $\ell$, such as the [logistic loss](/logistic-loss/) $\ell(m) = \log(1 + e^{-m})$.

**Proposition.** $\displaystyle \max_{\lVert \delta \rVert_\infty \le \epsilon} \ell\big(y (w^\top (x + \delta) + b)\big) = \ell\big(y (w^\top x + b) - \epsilon \lVert w \rVert_1\big)$, attained at $\delta^* = -\epsilon\, y \operatorname{sign}(w)$.

*Proof.* Since $\ell$ is decreasing, the maximum of the loss is at the minimum of the margin $y (w^\top x + b) + y\, w^\top \delta$. By Hölder's inequality $y\, w^\top \delta \ge -\lVert w \rVert_1 \lVert \delta \rVert_\infty \ge -\epsilon \lVert w \rVert_1$, and $\delta^*$ attains it: $y\, w^\top \delta^* = -\epsilon \sum_j |w_j|$. $\blacksquare$

The input gradient is $\nabla_x L = \ell'(m)\, y\, w$ with $\ell' < 0$, so $\operatorname{sign}(\nabla_x L) = -y \operatorname{sign}(w)$ and FGSM finds $\delta^*$ in one step. PGD with $K \alpha \ge 2\epsilon$ reaches the same corner from any start. For an $\ell_p$ ball the same proof gives $-\epsilon \lVert w \rVert_q$ with $1/p + 1/q = 1$.

So for [logistic regression](/logistic-regression/), adversarial training minimizes $\mathbb{E}\, \ell(y (w^\top x + b) - \epsilon \lVert w \rVert_1)$. Goodfellow et al. compare this with $L_1$ [weight decay](/weight-decay/), $\mathbb{E}\, \ell(y(w^\top x + b)) + \epsilon \lVert w \rVert_1$: the adversarial penalty acts inside the loss, so it fades once the margin is large, while weight decay never stops.

**Cost.** A $K$ step PGD attack costs $K$ forward and backward passes per example, so a training step costs about $K + 1$ times a standard step. Common settings on images in $[0, 1]$: $\epsilon = 8/255$, $K = 7$ to 10, $\alpha = 2/255$.

## Classic examples

**One linear example.** Let $w = (2, -1, 0.5)$, $b = 0.25$, $x = (0.3, -0.2, 0.4)$, $y = 1$, $\epsilon = 0.1$. The margin is $0.6 + 0.2 + 0.2 + 0.25 = 1.25$ and $\lVert w \rVert_1 = 3.5$, so the worst case margin is $1.25 - 0.35 = 0.9$. The logistic loss rises from $0.2519$ to $0.3412$. FGSM moves to $x + \delta^* = (0.2, -0.1, 0.3)$, a corner of the box, and attains exactly this loss.

**Robustness against accuracy.** Two Gaussian classes in 20 dimensions: $x = y\,\mu + N(0, I)$ with $\mu = (1, 0.25, \ldots, 0.25)$, one strong feature and 19 weak ones. Train logistic regression on 200 examples by full batch gradient descent (step 0.5, 100 epochs, PGD with 5 steps of $\alpha = \epsilon/2$; seed `random.Random(11)`), and measure the accuracy under the exact worst case attack on 1000 test examples.

| training $\epsilon$ | $\lVert w \rVert_1$ | accuracy, $\epsilon = 0$ | accuracy, $\epsilon = 0.1$ | accuracy, $\epsilon = 0.25$ |
|---|---|---|---|---|
| 0 (standard) | 9.22 | 0.899 | 0.832 | 0.671 |
| 0.1 | 6.48 | 0.885 | 0.837 | 0.724 |
| 0.25 | 3.06 | 0.843 | 0.810 | 0.761 |

The standard model uses the many weak features, which each give a little evidence but which an $\ell_\infty$ attacker can all shift at once. Adversarial training shrinks their weights, gains robust accuracy and loses clean accuracy. Tsipras et al. (2019) build a distribution where this trade-off is unavoidable for any classifier.

**Image classifiers (Madry et al. 2018).** PGD adversarial training of a wide ResNet on CIFAR-10 with $\epsilon = 8/255$ gave a model that kept a substantial fraction of its accuracy under strong white box attacks, at a large cost in clean accuracy; on MNIST with $\epsilon = 0.3$ the robust accuracy was much higher. Many later defenses that claimed more robustness were broken (Athalye et al. 2018), while PGD training held up.

## Variations

- **FGSM training with a random start.** One step attacks from a random point, with a step a little larger than $\epsilon$, approach PGD training at the cost of about two standard steps (Wong, Rice and Kolter 2020).
- **TRADES.** Replace the adversarial loss by the clean loss plus a term that penalizes the change of the output distribution under attack, with a weight that sets the trade-off.
- **Other threat models.** $\ell_2$ and $\ell_1$ balls, rotations and translations, or perturbations of word embeddings in text models.
- **Certified training.** Bound the inner maximum from above (by interval bounds or a convex relaxation) instead of from below by an attack, and minimize the bound; the result comes with a proof of robustness on each certified input.
- **Adversarial examples as data augmentation.** With small $\epsilon$ the perturbed inputs act as a [regularization](/regularization/) and can improve clean accuracy, especially for language models.

## Pitfalls

- **Weak attacks give false robustness.** A model can learn to hide its gradients (gradient masking) so that FGSM and PGD fail while other attacks succeed. Evaluate with strong, varied attacks, many random restarts, and gradient-free or adaptive attacks (Athalye et al. 2018).
- **Catastrophic overfitting.** With FGSM training the robust accuracy against PGD can drop to near zero within a few epochs while FGSM accuracy stays high. Random starts and checks against PGD during training catch it.
- **Robust overfitting.** The robust test accuracy of PGD training peaks early in training and then falls while the robust training accuracy rises; [early stopping](/early-stopping/) on a robust validation set helps (Rice, Wong and Kolter 2020).
- **Clipping to the valid range.** Perturbed pixels outside $[0, 1]$ are not valid images; project onto the intersection of the ball and the box.
- **Batch normalization.** Mixing clean and attacked inputs in one batch mixes their statistics; some methods keep separate statistics.
- **The guarantee is only for $S$.** A model robust in $\ell_\infty$ with $\epsilon = 8/255$ can still be fooled by a slightly larger $\epsilon$, another norm, or a rotation.

## Exercises

1. Show that $\operatorname{sign}(g)$ maximizes $g^\top \delta$ over the unit $\ell_\infty$ ball, and find the maximizer over the unit $\ell_2$ ball.
2. For the linear model with an $\ell_2$ ball, find the worst case margin and the one step attack that attains it.
3. Show that PGD with $K$ steps of size $\alpha$ from a uniform random start reaches the worst case corner for a linear model when $K \alpha \ge 2\epsilon$.
4. Give a function $L(\theta, \delta)$ with two maximizers in $\delta$ for which $\max_\delta L$ is not differentiable in $\theta$, and explain what this means for Danskin's theorem.

## References
