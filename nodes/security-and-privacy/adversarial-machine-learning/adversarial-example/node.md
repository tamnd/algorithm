---
tag: ZJAKP2
kind: definition
slug: adversarial-example
name: Adversarial example
aliases:
- adversarial perturbation
area: security-and-privacy/adversarial-machine-learning
level: intro
summary: "An input in an allowed small set around a correctly classified input, such as an l_p ball, to which the model gives a wrong label. The set is part of the threat model."
history:
  year: 2013
  people: [Battista Biggio, Christian Szegedy, Ian Goodfellow]
  note: Biggio et al. (ECML PKDD 2013) and Szegedy et al. (posted in 2013, ICLR 2014) found that small, gradient-guided changes of an input fool trained classifiers. Goodfellow, Shlens and Szegedy (2015) explained it by linearity.
prereqs: [logistic-regression]
see_also: [evasion-attack, fast-gradient-sign-method, deepfool, adversarial-transferability, universal-adversarial-perturbation, adversarial-training, randomized-smoothing, neural-network-verification-problem]
sources:
  - url: https://arxiv.org/abs/1312.6199
    title: Christian Szegedy, Wojciech Zaremba, Ilya Sutskever, Joan Bruna, Dumitru Erhan, Ian Goodfellow and Rob Fergus, Intriguing properties of neural networks, ICLR 2014
    locator: Section 4 (the box-constrained minimal perturbation that changes the label, found with L-BFGS)
  - url: https://arxiv.org/abs/1708.06131
    title: Battista Biggio, Igino Corona, Davide Maiorca, Blaine Nelson, Nedim Srndic, Pavel Laskov, Giorgio Giacinto and Fabio Roli, Evasion attacks against machine learning at test time, ECML PKDD 2013, LNCS 8190, pages 387 to 402
    locator: the adversary model (goal, knowledge, capability) and the gradient-based evasion of a classifier at test time
  - url: https://arxiv.org/abs/1412.6572
    title: Ian J. Goodfellow, Jonathon Shlens and Christian Szegedy, Explaining and harnessing adversarial examples, ICLR 2015
    locator: Section 3 (the linear explanation, with the perturbation eta of l_infinity norm at most epsilon)
  - paper: "Battista Biggio and Fabio Roli, Wild patterns: Ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317 to 331, 2018"
    locator: the threat model in three parts and the history of evasion attacks since the work on spam filters
  - url: https://arxiv.org/abs/1608.04644
    title: Nicholas Carlini and David Wagner, Towards evaluating the robustness of neural networks, IEEE Symposium on Security and Privacy 2017, pages 39 to 57
    locator: the l_0, l_2 and l_infinity distance metrics and the targeted definition
  - url: https://arxiv.org/abs/1706.06083
    title: Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt, Dimitris Tsipras and Adrian Vladu, Towards deep learning models resistant to adversarial attacks, ICLR 2018
    locator: Section 2 (the set of allowed perturbations and the robust objective)
---

An adversarial example is an input $x'$ that is close to a correctly classified input $x$, in a set of allowed changes fixed in advance, and that the model labels wrongly. The changes are often too small for a person to see, yet they move the input across the decision boundary of the model. Biggio et al. (2013) and Szegedy et al. (2014) found such inputs for trained classifiers with gradient steps, and Goodfellow, Shlens and Szegedy (2015) explained them by the near-linear behavior of the models in high dimension. An [evasion attack](/evasion-attack/) is a method that finds them; [adversarial training](/adversarial-training/) and certified methods are the defenses. "Close" has no meaning without a threat model, so the definition below names the set of allowed changes explicitly.

## Definition

A classifier with $K$ classes has logits $z(x) \in \mathbb{R}^K$ and predicts $f(x) = \arg\max_k z_k(x)$, with ties going to the smallest index. Inputs are in $[0,1]^d$. For $p \in \{0, 1, 2, \infty\}$ and a radius $\epsilon \ge 0$, the set of allowed inputs around $x$ is

$$S_p(x, \epsilon) = B_p(x, \epsilon) \cap [0,1]^d, \qquad B_p(x, \epsilon) = \{x' : \lVert x' - x \rVert_p \le \epsilon\}.$$

Here $\lVert v \rVert_0$ counts the nonzero coordinates of $v$; it is not a norm, since $\lVert 2v \rVert_0 = \lVert v \rVert_0$.

**Definition (untargeted).** Let $x \in [0,1]^d$ have the true label $y$ and let $f(x) = y$. An input $x'$ is an *adversarial example for $x$ at radius $\epsilon$ in $\ell_p$* if $x' \in S_p(x, \epsilon)$ and $f(x') \ne y$. The vector $\eta = x' - x$ is its perturbation.

**Definition (targeted).** For a target class $t \ne y$, $x'$ is a *targeted* adversarial example if $x' \in S_p(x, \epsilon)$ and $f(x') = t$.

**Definition (robustness).** The point $x$ is *robust at radius $\epsilon$ in $\ell_p$* if no adversarial example for $x$ exists in $S_p(x, \epsilon)$. The *minimal adversarial distance* is $\rho_p(x) = \inf\{\lVert x' - x \rVert_p : x' \in [0,1]^d,\ f(x') \ne y\}$. If $\epsilon < \rho_p(x)$, then $x$ is robust at radius $\epsilon$. The *robust accuracy* of $f$ at radius $\epsilon$ on a test set is the fraction of test points $(x, y)$ with $f(x') = y$ for every $x' \in S_p(x, \epsilon)$.

Three remarks fix the reading of the definition:

- **The threat model is part of the definition.** The norm $p$, the radius $\epsilon$ and the box $[0,1]^d$ define what counts. An input is an adversarial example only relative to a stated set. Biggio and Roli (2018) put this set in the capability of the attacker, next to the goal (untargeted or targeted) and the knowledge (white box, gray box, black box with scores, black box with decisions).
- **The true label is assumed to stay $y$ in the set.** The set is chosen small enough that a person would give $x'$ the same label as $x$. This is a modeling assumption, not a theorem. A change that turns a "3" into a real "8" is not an adversarial example, even though the model changes its label.
- **The start must be correct.** If $f(x) \ne y$ already, the model is simply wrong at $x$. Some papers, such as Szegedy et al., define the condition as $f(x') \ne f(x)$ instead of $f(x') \ne y$. The two agree when $f(x) = y$. Say which one a number uses.

**Bounds.** An attack that finds an adversarial example proves that $x$ is not robust, so attacks give an *upper bound* on robust accuracy. A verifier or a certificate, such as [randomized smoothing](/randomized-smoothing/) or [interval bound propagation](/interval-bound-propagation/), proves that no adversarial example exists, so it gives a *lower bound*. A failed attack proves nothing.

**Proposition (linear models).** Let $K = 2$ with $f(x) = 1$ when $w^\top x + b > 0$ and $f(x) = 0$ otherwise, $w \ne 0$, and ignore the box. Then $\rho_2(x) = |w^\top x + b| / \lVert w \rVert_2$ and $\rho_\infty(x) = |w^\top x + b| / \lVert w \rVert_1$.

*Proof.* Changing the label needs $w^\top \eta$ to reach $-(w^\top x + b)$ when the label is $1$, or to pass it when the label is $0$. So $|w^\top \eta| \ge |w^\top x + b|$ is needed, and by Hölder's inequality $|w^\top \eta| \le \lVert w \rVert_q \lVert \eta \rVert_p$ with $1/p + 1/q = 1$. So $\lVert \eta \rVert_p \ge |w^\top x + b| / \lVert w \rVert_q$. The vectors $\eta = \tau\, w / \lVert w \rVert_2$ and $\eta = \tau \operatorname{sign}(w)$, with the sign of $\tau$ chosen to move toward the boundary, attain equality in the two cases, and a slightly longer step crosses the boundary. $\blacksquare$

The $\ell_\infty$ case shows the linear explanation of Goodfellow, Shlens and Szegedy. The change of the logit is $\epsilon \lVert w \rVert_1$, which grows with the number of coordinates: if every $|w_i|$ is about $m$, it is about $\epsilon\, m\, d$. In high dimension, many changes that are each too small to see add up to a large change of the output.

## Examples and non-examples

**A linear model in the plane, three norms.** Take $K = 3$, $z(x) = Wx$ with rows $(1, 0)$, $(0, 1)$ and $(-1, -1)$, and $x = (0.6, 0.4)$ with $y = 0$. Then $z(x) = (0.6, 0.4, -1)$. The label becomes $1$ once $x_2 > x_1$. Class $2$ is far away.

| norm | $\rho_p(x)$ | a perturbation that reaches it |
|---|---|---|
| $\ell_2$ | $0.2/\sqrt2 = 0.1414$ | $\tau(-1, 1)/\sqrt2$ with $\tau$ just above $0.1414$ |
| $\ell_\infty$ | $0.1$ | $\tau(-1, 1)$ with $\tau$ just above $0.1$ |
| $\ell_0$ | $1$ | change one coordinate, for example $x_2$ to $0.61$ |

The point $x' = (0.498, 0.502)$, found by one step of [DeepFool](/deepfool/), is an adversarial example in $\ell_2$ at every radius $\epsilon \ge 0.1443$. At $\epsilon = 0.14$ in $\ell_2$, no adversarial example exists, because $0.14 < \rho_2(x)$. The same pair is far apart in $\ell_0$ (two changed coordinates) and close in $\ell_\infty$ ($0.102$). So the norm decides which inputs count.

**A logistic model in six dimensions, with the box.** Let $w = (1.5, -2, 0.5, 1, -0.5, 3)$, $b = 1$, $x = (0.2, 0.9, 0.5, 0, 1, 0.4)$ and $y = 1$. The logit is $z = 0.45$. The [fast gradient sign method](/fast-gradient-sign-method/) at $\epsilon = 0.1$ in $\ell_\infty$ gives $x' = (0.1, 1, 0.4, 0, 1, 0.3)$ with $z' = -0.25$, so $x'$ is an adversarial example. Coordinates 4 and 5 cannot move, because the box stops them at $0$ and $1$. So the box matters: without it, $\rho_\infty(x) = 0.45 / 8.5 = 0.0529$; with it, only the other four coordinates can move, and $\rho_\infty(x) = 0.45 / 7 = 0.0643$.

**A non-example: a radius that is too small.** In the same model at $\epsilon = 0.05$, the smallest logit in $S_\infty(x, 0.05)$ is $0.45 - 7 \cdot 0.05 = 0.1 > 0$. FGSM is exact for a linear model (see its page), so this is a proof: no adversarial example exists, and $x$ is robust at this radius.

**A non-example: a change outside the set.** The input $(0.2, 0.9, 0.5, 0, 1, 0)$ changes one coordinate by $0.4$ and has logit $-0.75$, a wrong label. At $\epsilon = 0.1$ in $\ell_\infty$ it is not an adversarial example, because it is not in $S_\infty(x, 0.1)$. In $\ell_0$ with $\epsilon = 1$ it is one.

**A non-example: random noise.** A change of the same size in a random direction rarely changes the label. On two logistic models in 8 dimensions trained on seeded Gaussian blobs (the measurement on the page [adversarial transferability](/adversarial-transferability/)), random sign noise of size $0.1$ in $\ell_\infty$ changed the label of 5 of 198 test points, while the FGSM change of the same size changed 90. Adversarial examples are rare in volume but easy to find with the gradient.

**A non-example: a point that is already wrong.** If $f(x) \ne y$, then $x$ itself has the wrong label, and no search is needed. It counts against clean accuracy, not as an adversarial example.

**An example in $\ell_0$.** The [Jacobian saliency map attack](/jacobian-saliency-map-attack/) changes few coordinates by a large amount. On the six-feature model of its page it reaches the target class with four changed features, so $\lVert \eta \rVert_0 = 4$ while $\lVert \eta \rVert_\infty = 0.8$.

## Related definitions

- **[Evasion attack](/evasion-attack/).** The class of methods that find adversarial examples at test time. Each one fixes the goal, the knowledge and the set $S_p(x, \epsilon)$.
- **Minimal perturbation.** The attacks [DeepFool](/deepfool/) and the [Carlini-Wagner attack](/carlini-wagner-attack/) estimate $\rho_2(x)$ from above. The attacks with a fixed radius, [FGSM](/fast-gradient-sign-method/) and the [PGD attack](/pgd-attack/), test membership of a set instead.
- **[Universal adversarial perturbation](/universal-adversarial-perturbation/).** One vector $\eta$ that changes the label of many inputs at once, in contrast to an $\eta$ chosen for each $x$.
- **[Adversarial transferability](/adversarial-transferability/).** An adversarial example for one model is often one for another model trained on similar data.
- **Certified radius.** A lower bound on $\rho_p(x)$ with a proof, from [randomized smoothing](/randomized-smoothing/) (with a stated probability), [interval bound propagation](/interval-bound-propagation/) or [linear bound propagation](/linear-bound-propagation/). The exact question is the [neural network verification problem](/neural-network-verification-problem/).
- **Training-time attacks.** [Data poisoning](/data-poisoning/) and [backdoor attacks](/backdoor-attack/) change the training data, not the test input. A backdoor trigger is a test-time change too, but it works because the training was changed.
- **Robust training.** [Adversarial training](/adversarial-training/) minimizes the loss at the worst point of $S_p(x, \epsilon)$, which lowers the number of adversarial examples for the training distribution.

## References
