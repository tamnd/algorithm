---
tag: SJSRTS
kind: concept
slug: adversarial-transferability
name: Transferability of adversarial examples
aliases:
- transfer attack
- substitute model attack
area: security-and-privacy/adversarial-machine-learning
level: core
summary: "Adversarial examples made for one model often fool other models trained for the same task. This allows black-box attacks through a substitute model, and it limits defenses that hide gradients."
history:
  year: 2013
  people: [Christian Szegedy, Nicolas Papernot, Patrick McDaniel, Ian Goodfellow, Florian Tramer]
  note: Szegedy et al. observed in 2013 that adversarial examples fool networks trained on other data. Papernot, McDaniel and Goodfellow studied it across model classes in 2016 and built black-box attacks on it.
prereqs: [adversarial-example, fast-gradient-sign-method]
see_also: [evasion-attack, fast-gradient-sign-method, universal-adversarial-perturbation, boundary-attack, zeroth-order-optimization-attack, defensive-distillation, adversarial-training, pgd-attack]
sources:
  - url: https://arxiv.org/abs/1312.6199
    title: Christian Szegedy, Wojciech Zaremba, Ilya Sutskever, Joan Bruna, Dumitru Erhan, Ian Goodfellow and Rob Fergus, Intriguing properties of neural networks, ICLR 2014
    locator: the experiments on cross-model generalization of adversarial examples, for networks with other hyperparameters and other training sets
  - url: https://arxiv.org/abs/1605.07277
    title: Nicolas Papernot, Patrick McDaniel and Ian Goodfellow, Transferability in machine learning, from phenomena to black-box attacks using adversarial samples, arXiv 1605.07277, 2016
    locator: the transfer within and across classes of models (networks, logistic regression, support vector machines, decision trees, nearest neighbors), and the substitute training
  - url: https://arxiv.org/abs/1602.02697
    title: Nicolas Papernot, Patrick McDaniel, Ian Goodfellow, Somesh Jha, Z. Berkay Celik and Ananthram Swami, Practical black-box attacks against machine learning, AsiaCCS 2017, pages 506 to 519
    locator: the substitute model trained on labels from queries, with Jacobian-based data augmentation
  - url: https://arxiv.org/abs/1704.03453
    title: Florian Tramer, Nicolas Papernot, Ian Goodfellow, Dan Boneh and Patrick McDaniel, The space of transferable adversarial examples, arXiv 1704.03453, 2017
    locator: the dimension of the space of adversarial directions, and the distance between the decision boundaries of two models
  - url: https://arxiv.org/abs/1611.02770
    title: Yanpei Liu, Xinyun Chen, Chang Liu and Dawn Song, Delving into transferable adversarial examples and black-box attacks, ICLR 2017
    locator: untargeted and targeted transfer between large models, and attacks on an ensemble of models
  - url: https://arxiv.org/abs/1412.6572
    title: Ian Goodfellow, Jonathon Shlens and Christian Szegedy, Explaining and harnessing adversarial examples, ICLR 2015
    locator: the linear explanation of adversarial examples and of their transfer
  - url: https://arxiv.org/abs/1705.07204
    title: Florian Tramer, Alexey Kurakin, Nicolas Papernot, Ian Goodfellow, Dan Boneh and Patrick McDaniel, Ensemble adversarial training, attacks and defenses, ICLR 2018
    locator: adversarial training with examples transferred from other models
---

Transferability is the observation that an [adversarial example](/adversarial-example/) made for one model often fools a second model trained for the same task, even when the second model has another architecture or was trained on other data. Szegedy et al. (2014) first reported it for neural networks. Papernot, McDaniel and Goodfellow (2016) measured it across classes of models, such as networks, logistic regression and decision trees. It matters for security in two ways. An attacker without access to a model can train a substitute model, attack the substitute with a white-box method, and send the result to the real model. And a defense that only hides or breaks the gradients of the model does not stop such an attack, since the attack never uses those gradients.

## In plain words

Two models trained for the same task learn similar rules, because they see similar data. A change that pushes an input across the border of one model often pushes it across the border of the other, since the borders are close and point in similar directions.

So an attacker who cannot look inside the target can build a stand-in. They train their own model on similar data, or on answers from the target. They attack their own model, where they can see everything, and then use the result on the target.

The transfer is not perfect. Some changes that fool the stand-in do not fool the target. A change in a random direction of the same size fools far fewer inputs, so transfer is not luck: it shows that the two models share their weak directions.

## The idea

Let $f_S$ be the source model, which the attacker can attack in the white box, and $f_T$ the target. For a set of inputs that both models classify correctly, the transfer rate of an attack $A$ at radius $\epsilon$ is the fraction of inputs $x$ for which $f_T(A(f_S, x)) \ne y$. One can also count the fraction of the successful source examples that also fool the target.

**Why it happens, in the linear case.** For linear models $f(x) = \operatorname{sign}(w^\top x + b)$, the [FGSM](/fast-gradient-sign-method/) step for the source is $\eta = -\epsilon\, s \operatorname{sign}(w_S)$, with $s = \pm 1$ the sign of the label. It moves the target score by $-\epsilon\, s\, w_T^\top \operatorname{sign}(w_S)$. If the two weight vectors have the same signs, this is $-\epsilon\, s \lVert w_T \rVert_1$, the largest move that any change in the $\ell_\infty$ ball can make on the target. Then the transferred example is exactly the FGSM example of the target. Goodfellow, Shlens and Szegedy (2015) argued that networks behave much like linear models in these directions, which explains much of the transfer between them.

**Shared space of adversarial directions.** Tramer et al. (2017) found that adversarial directions of a model span a space of many dimensions, and that the decision boundaries of two models trained for the same task are close to each other along these directions. Two models whose spaces overlap share adversarial examples.

**What makes it stronger or weaker.**

- Untargeted examples transfer far more often than targeted ones. Liu et al. (2017) found that examples aimed at one class rarely transfer between large networks, and that attacking an ensemble of several source models helps.
- A larger $\epsilon$ and a perturbation that goes well past the boundary of the source (a high confidence $\kappa$ in the [Carlini-Wagner attack](/carlini-wagner-attack/)) transfer better. Minimal examples, which lie just past the boundary of the source, often do not.
- Single-step attacks often transfer better than many steps of [PGD](/pgd-attack/), which can overfit the source model.
- Models of the same class, trained on similar data, share more. Papernot, McDaniel and Goodfellow report transfer also across model classes, with different rates.

**The substitute model attack.** Papernot et al. (AsiaCCS 2017) train a substitute without access to the training data of the target. They start from a small set of inputs, label them with queries to the target, train the substitute, and add new inputs in the directions where the substitute changes most (Jacobian-based data augmentation). Then they attack the substitute and transfer the result. This uses only labels, like the [boundary attack](/boundary-attack/), but with far fewer queries, and the attack is done off line.

## Examples

**Two logistic models in 8 dimensions.** Draw two training sets of 40 points each from the same two Gaussian blobs in $[0,1]^8$, with centers $(0.4, \dots, 0.4)$ and $(0.6, \dots, 0.6)$ and $\sigma = 0.1$, using `mlkit.make_blobs` with seeds 1 and 2. Train a logistic regression on each with `mlkit.train_logistic` (300 steps, step size 1, no penalty). Draw 200 test points with seed 3 and clip them to the box. Both models reach accuracy $0.995$, and 198 test points are correct for both.

| | source model $S$ | target model $T$ |
|---|---|---|
| weights | $(1.01, 2.56, 4.45, 2.63, 0.95, 1.78, 1.53, 3.18)$ | $(1.56, 2.52, 3.28, 3.65, 2.72, 2.61, 1.66, 0.60)$ |
| bias | $-9.11$ | $-9.03$ |

The two weight vectors differ a lot, with cosine $0.869$, but all 8 signs agree. Run FGSM on the source and send the result to the target:

| $\epsilon$ in $\ell_\infty$ | labels changed on $S$ | labels changed on $T$ | changed on both | random signs, changed on $T$ |
|---|---|---|---|---|
| 0.02 | 1 of 198 | 1 | 0 | 0 |
| 0.05 | 14 | 16 | 6 | 0 |
| 0.1 | 79 | 90 | 61 | 5 |

At $\epsilon = 0.1$ the target, which the attacker never queried, loses 90 of 198 points, more than the source itself. The linear argument above explains this: the signs agree, so the source FGSM change is exactly the FGSM change of the target, and the target has a slightly larger $\lVert w \rVert_1$ ($18.60$ against $18.10$). The points it loses are not the same as those of the source: 61 points are lost by both.

**A non-example: random noise.** A change of the same size with random signs, drawn with seed 4, changes the label of only 5 of the 198 points on the target at $\epsilon = 0.1$. So the effect of the transferred change comes from its direction, not from its size.

**A non-example: a model that uses other directions.** If the target had the opposite sign on some weights of the source, the source FGSM step would push its score the wrong way along those features, and the transfer would drop. In the linear case the move on the target is $-\epsilon\, s\, w_T^\top \operatorname{sign}(w_S)$, and when most signs disagree this moves the target score toward the correct label.

## Where it is used

- **Black-box attacks.** A substitute model and a white-box attack on it, as in Papernot et al. (2017), or a pretrained model for the same task. Transfer is also a good start for a query-based attack, such as the [boundary attack](/boundary-attack/), which then needs fewer queries.
- **Evaluating defenses.** A defense that stops white-box attacks but not transferred ones is a sign of gradient masking. This is how [defensive distillation](/defensive-distillation/) and many later defenses were shown to be weak. A strong evaluation includes a transfer attack from an undefended model.
- **Universal perturbations.** One [universal perturbation](/universal-adversarial-perturbation/) often fools other networks as well, which is transfer across both inputs and models.
- **Defenses.** Ensemble adversarial training (Tramer et al., 2018) trains on examples transferred from other fixed models, to defend against transfer attacks. Certified methods, such as [randomized smoothing](/randomized-smoothing/), hold against any attack, transferred or not, within their radius.
- **Understanding models.** Transfer rates measure how much two models share their decision boundaries.

## References
