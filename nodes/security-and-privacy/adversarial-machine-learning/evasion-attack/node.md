---
tag: 3BJ34P
kind: concept
slug: evasion-attack
name: Evasion attack
aliases:
- test-time attack
area: security-and-privacy/adversarial-machine-learning
level: intro
summary: "An attack that changes inputs at test time so that a trained classifier misclassifies them, in a white-box or black-box setting."
history:
  year: 2013
  people: [Battista Biggio, Fabio Roli, Christian Szegedy]
  note: Biggio et al. (ECML PKDD 2013) stated evasion at test time as an optimization problem with an explicit adversary model; Szegedy et al. found the same effect in deep networks.
prereqs: [adversarial-example]
see_also: [adversarial-example, fast-gradient-sign-method, pgd-attack, boundary-attack, zeroth-order-optimization-attack, adversarial-transferability, data-poisoning, adversarial-training]
sources:
  - url: https://arxiv.org/abs/1708.06131
    title: Battista Biggio, Igino Corona, Davide Maiorca, Blaine Nelson, Nedim Srndic, Pavel Laskov, Giorgio Giacinto and Fabio Roli, Evasion attacks against machine learning at test time, ECML PKDD 2013, LNCS 8190, pages 387 to 402
    locator: the adversary model (goal, knowledge, capability), the gradient descent evasion with a mimicry term, and the experiments on handwritten digits and PDF malware
  - paper: "Battista Biggio and Fabio Roli, Wild patterns: Ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317 to 331, 2018"
    locator: the threat model in three parts, the taxonomy of attacks at training and test time, and the history
  - url: https://arxiv.org/abs/1312.6199
    title: Christian Szegedy, Wojciech Zaremba, Ilya Sutskever, Joan Bruna, Dumitru Erhan, Ian Goodfellow and Rob Fergus, Intriguing properties of neural networks, ICLR 2014
    locator: Section 4 (adversarial examples of deep networks and their transfer)
  - url: https://arxiv.org/abs/1602.02697
    title: Nicolas Papernot, Patrick McDaniel, Ian Goodfellow, Somesh Jha, Z. Berkay Celik and Ananthram Swami, Practical black-box attacks against machine learning, AsiaCCS 2017, pages 506 to 519
    locator: the substitute model trained on labels from queries, and the transfer of its adversarial examples
  - url: https://arxiv.org/abs/1712.04248
    title: Wieland Brendel, Jonas Rauber and Matthias Bethge, Decision-based adversarial attacks, reliable attacks against black-box machine learning models, ICLR 2018
    locator: the taxonomy of gradient-based, score-based, transfer-based and decision-based attacks
  - url: https://arxiv.org/abs/1902.06705
    title: Nicholas Carlini, Anish Athalye, Nicolas Papernot, Wieland Brendel, Jonas Rauber, Dimitris Tsipras, Ian Goodfellow, Aleksander Madry and Alexey Kurakin, On evaluating adversarial robustness, arXiv 2019
    locator: the threat model of an evaluation, adaptive attacks, and the checklist of common flaws
  - url: https://arxiv.org/abs/1802.00420
    title: Anish Athalye, Nicholas Carlini and David Wagner, Obfuscated gradients give a false sense of security, circumventing defenses to adversarial examples, ICML 2018
    locator: the three kinds of obfuscated gradients and the attacks that break defenses based on them
---

An evasion attack changes an input at test time so that a trained model gives it a wrong label, without any change to the model or its training data. The output of the attack is an [adversarial example](/adversarial-example/). Biggio et al. (2013) stated evasion as an optimization problem against an explicit adversary, and Biggio and Roli (2018) describe every attack by three parts: the goal, the knowledge and the capability. The class covers attacks with full access to the gradients, attacks that see only the scores or only the labels, and attacks that use a second model. On the defense side, an evasion attack is the tool that measures robustness: it gives an upper bound on robust accuracy, while certificates give the lower bound. An attack on the training data instead is [data poisoning](/data-poisoning/).

## In plain words

A spam filter or an image classifier is trained once and then used on new inputs. An attacker who controls an input can change it a little, so that it still does its job for the attacker but the model now says "harmless" or names the wrong object. This is an evasion attack.

How the attacker searches depends on what the attacker can see. With a copy of the model, the attacker can ask which small change raises the error most. With only the answers of the model, the attacker must try many inputs and learn from the results. With nothing, the attacker can train a similar model and hope that its tricks work on the real one.

Defenders use these attacks to test their models. A model that resists strong attacks of every kind is more robust, but only a proof shows that no attack exists.

## The idea

**The threat model.** Let the model have logits $z(x) \in \mathbb{R}^K$ and label $f(x) = \arg\max_k z_k(x)$ on inputs $x \in [0,1]^d$, with a loss $L(\theta, x, y)$. Following Biggio and Roli (2018), an evasion attack fixes:

- **The goal.** Untargeted (any wrong label) or targeted (a chosen label $t$). The violation is of integrity: the model still works on other inputs.
- **The knowledge.** White box (the parameters $\theta$ and the gradients), gray box (the training data or the architecture, but not $\theta$), black box with scores (the vector of probabilities for each query), or black box with decisions (only the label for each query).
- **The capability.** Changes at test time only, within a set $S(x)$, usually $B_p(x, \epsilon) \cap [0,1]^d$ for a norm $p$ and a radius $\epsilon$. In some domains the set is different: a malware file can get new parts but cannot lose the parts it needs to run.

**Two forms of the problem.** With a fixed budget, the attacker solves
$$\max_{x' \in S(x)} L(\theta, x', y),$$
and succeeds if the maximizer has a wrong label. FGSM and the PGD attack work in this form. With a minimal budget, the attacker solves
$$\min_{x' \in [0,1]^d} \lVert x' - x \rVert_p \quad \text{subject to } f(x') \ne y,$$
and DeepFool and the Carlini-Wagner attack work in this form. Biggio et al. (2013) minimize the score of the classifier under a distance limit and add a term that keeps $x'$ near the dense regions of the data of the target class, so that the result looks like normal data.

**How the knowledge sets the method.**

| knowledge | what the attacker can compute | attacks |
|---|---|---|
| white box | $\nabla_x L$ and the Jacobian of $z$ | [FGSM](/fast-gradient-sign-method/), [PGD attack](/pgd-attack/), [Carlini-Wagner attack](/carlini-wagner-attack/), [DeepFool](/deepfool/), [JSMA](/jacobian-saliency-map-attack/) |
| black box with scores | finite differences of the scores | [ZOO attack](/zeroth-order-optimization-attack/) |
| black box with decisions | labels of chosen inputs | [boundary attack](/boundary-attack/) |
| gray box or none | a substitute model trained by the attacker | transfer, see [adversarial transferability](/adversarial-transferability/) |

Less knowledge costs queries, not always success. On a smooth model, a score-based or decision-based attack can reach nearly the same distance as a white-box attack, but it needs hundreds or thousands of queries where the white-box attack needs a few gradients.

**What an attack proves.** If the attack finds $x' \in S(x)$ with $f(x') \ne y$, then $x$ is not robust at radius $\epsilon$. So the fraction of test points that resist a given attack is an upper bound on the robust accuracy. If the attack fails, nothing is proved. A defense can make gradient attacks fail without making the model robust, for example by gradients that vanish or are noisy ("gradient masking"). Athalye, Carlini and Wagner (2018) found this in 7 of the 9 defenses of ICLR 2018 that they studied, and broke them. Carlini et al. (2019) ask for *adaptive* evaluations: attacks designed for the defense, with the threat model stated, many restarts, and a check that unbounded attacks reach 100 percent success.

**The defenses.**

- **Robust training.** [Adversarial training](/adversarial-training/) minimizes the loss at the worst point of $S(x)$ found by PGD. It is the empirical defense that has held up best.
- **Certified methods.** [Randomized smoothing](/randomized-smoothing/), [interval bound propagation](/interval-bound-propagation/) and [linear bound propagation](/linear-bound-propagation/) prove for each input that no change in $S(x)$ changes the label. Complete verification is the [neural network verification problem](/neural-network-verification-problem/).
- **Detection and input changes.** Many detectors and input transformations were broken by adaptive attacks, for example with [BPDA](/backward-pass-differentiable-approximation/) or [EOT](/expectation-over-transformation/). [Defensive distillation](/defensive-distillation/) is the classic case.
- **Limits on the attacker.** Fewer queries, labels without scores, or rate limits make black-box attacks slower. They do not stop transfer attacks.

## Examples

**One model, four kinds of knowledge.** Take the linear model of the page [adversarial example](/adversarial-example/): $K = 3$, $z(x) = Wx$ with rows $(1, 0)$, $(0, 1)$, $(-1, -1)$, and $x = (0.6, 0.4)$ with label $0$. The minimal $\ell_2$ distance to another label is $\rho_2 = 0.2/\sqrt2 = 0.14142$. The four attacks of this area, run with the code of their pages on this model:

| attack | knowledge | cost | distance found | ratio to $\rho_2$ |
|---|---|---|---|---|
| DeepFool, overshoot 0.02 | white box | 1 Jacobian, 2 logit calls | 0.14425 | 1.020 |
| Carlini-Wagner, 8 rounds of 100 Adam steps | white box | 800 gradients | 0.14143 | 1.00003 |
| ZOO, 400 steps, $c = 1$, $\kappa = 0.05$ | scores | 1200 queries | 0.14326 | 1.013 |
| boundary attack, 200 steps, start $(0, 1)$ | decisions | 297 queries | 0.14146 | 1.0002 |

All four find an adversarial example close to the minimum. The white-box attacks need almost no queries. The black-box attacks need hundreds, and on a model in thousands of dimensions they need many more. These are measurements on one tiny model with fixed seeds, not a general ranking.

**Capability: add only, or add and remove.** A made-up detector scores binary features with weights $w = (2, 1.5, -0.5, -0.8, -1.2)$ and bias $-1$, and flags an input when the score is above $0$. The input $x = (1, 1, 0, 0, 0)$ has score $2.5$ and is flagged. If the attacker may only add features (set a $0$ to $1$), the best order adds the most negative weights first: after feature 5 the score is $1.3$, after feature 4 it is $0.5$, and after feature 3 it is $0$, which is not above $0$. So three changes are needed. If the attacker may also remove features, removing feature 1 and adding feature 5 gives $-0.7$ with two changes. The same model is more or less robust depending on the capability. Biggio et al. (2013) used an add-only capability for PDF malware, where removing content can break the file.

**A transfer attack.** Two logistic models trained on different seeded samples of the same Gaussian blobs in 8 dimensions agree on the signs of all 8 weights. FGSM at $\epsilon = 0.1$ in $\ell_\infty$ against the first model changes the label of 79 of 198 test points on that model and of 90 on the second model, which the attacker never queried. The details are on the page [adversarial transferability](/adversarial-transferability/).

## Where it is used

- **Security evaluation of classifiers.** Spam filters, malware detectors and intrusion detectors face attackers who adapt their inputs. Biggio and Roli (2018) trace this work back to spam filtering in 2004 and 2005. An evaluation states the threat model and reports the success rate of the strongest attacks for it.
- **Robustness benchmarks.** Published robust accuracy numbers are upper bounds from a fixed set of attacks, so they can only go down when a stronger attack appears.
- **Robust training.** The inner step of [adversarial training](/adversarial-training/) is an evasion attack, usually PGD, run on each training batch.
- **Tests of a defense.** An adaptive attack that targets the specific defense is the standard check of a new defense (Carlini et al. 2019). [Defensive distillation](/defensive-distillation/) passed the attacks of its own paper and failed the Carlini-Wagner attack.
- **The physical world.** Changes that survive printing, cameras and viewpoints are found by averaging the attack over random transformations ([expectation over transformation](/expectation-over-transformation/)).

## References
