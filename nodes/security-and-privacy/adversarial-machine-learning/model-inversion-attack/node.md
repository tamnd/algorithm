---
tag: PV1E6J
kind: algorithm
slug: model-inversion-attack
name: Model inversion attack
aliases:
- model inversion
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: Recovers a sensitive input feature, or an input typical of one class, from a trained model and its confidence scores; MI-FACE does gradient descent on one minus the confidence.
model: real-ram
complexity:
  vars: {a: the largest number of steps (alpha), q: the window of the stopping rule (beta), d: the dimension, k: the number of classes}
  time: {worst: "O(a (k d + q))"}
  space: {extra: "O(a + d)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2014
  people: [Matt Fredrikson, Eric Lantz, Somesh Jha, Simon Lin, David Page, Thomas Ristenpart]
  note: Fredrikson et al. introduced model inversion at USENIX Security 2014 on a model for warfarin dosing. Fredrikson, Jha and Ristenpart (CCS 2015) gave attacks that use confidence scores, among them MI-FACE on face recognition models.
prereqs: [logistic-regression, softmax-regression, projected-gradient-descent, maximum-a-posteriori-estimation]
see_also: [gradient-inversion-attack, membership-inference-attack, training-data-extraction, model-extraction-attack, differential-privacy-definition, dp-sgd, linkage-attack, secure-multiparty-computation]
sources:
  - paper: "Matt Fredrikson, Somesh Jha and Thomas Ristenpart, Model inversion attacks that exploit confidence information and basic countermeasures, ACM Conference on Computer and Communications Security (CCS) 2015, pages 1322-1333, doi:10.1145/2810103.2813677"
    locator: "Section 3 and Figure 2 (the estimator of Fredrikson et al. 2014), Section 4 and equation (1) (the white-box estimator with counts for decision trees), Algorithm 1 (MI-FACE) and Section 5.2 (the reconstruction attack, with alpha = 5000, beta = 100 and lambda = 0.1), Section 5.3 (black box with numeric gradients), Section 6 and Figure 12 (rounded confidence scores as a countermeasure)"
  - paper: "Matt Fredrikson, Eric Lantz, Somesh Jha, Simon Lin, David Page and Thomas Ristenpart, Privacy in pharmacogenetics: an end-to-end case study of personalized warfarin dosing, USENIX Security Symposium 2014, pages 17-32"
    locator: the first model inversion attack, which estimates a genetic marker of a patient from a linear dosing model and other attributes of the patient, and the study of differential privacy as a defense
  - paper: "Yuheng Zhang, Ruoxi Jia, Hengzhi Pei, Wenxiao Wang, Bo Li and Dawn Song, The secret revealer: generative model-inversion attacks against deep neural networks, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2020"
    locator: a generative model trained on public data as a prior that keeps the inversion close to natural inputs
  - paper: "Battista Biggio and Fabio Roli, Wild patterns, ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317-331, 2018"
    locator: the threat model in three parts, goal, knowledge and capability
---

A model inversion attack uses a trained model to learn something about the data it was trained on: a sensitive feature of a person whose other features are known, or an input that the model links strongly to one class. Fredrikson et al. (2014) introduced it on a model that predicts the dose of the drug warfarin and showed that the model, with some demographic data of a patient, gives a good estimate of the patient's genetic marker. Fredrikson, Jha and Ristenpart (2015) showed that the confidence scores that many prediction services return make the attack much stronger. Their algorithm MI-FACE searches by gradient descent for the input with the highest confidence for a class; on a face recognition model whose classes are people, the result can look like the person. This page describes MI-FACE. The theorems on this page are about the optimization on small models; whether the result reveals a person is a measurement.

## In plain words

A model that names the person in a photo has learned, for each name, what that person's face looks like. If the model also says how sure it is, you can use that number as a guide.

Start from a blank image. Change it a little in the direction that makes the model more sure that the image shows a given name. Repeat until the model stops getting more sure. What is left is the picture that the model connects most strongly with that name, and it can look like the real person.

The same idea works for a table of records: if you know all of a person's answers but one, try each value of the missing answer and keep the one that best fits what the model says.

## The problem

**The threat model**, in the three parts of Biggio and Roli:

- *Goal of the attacker.* Learn private information about the training data. Two forms: a typical input of one class (a face, when each class is one person), or the value of one sensitive feature of a known person. This is a privacy goal.
- *Knowledge.* White box (the weights, so the attacker can compute the gradient) or black box with confidence scores. Fredrikson et al. also give the attacker auxiliary information, for example the marginal distribution of each feature. The attacker does not have the training data.
- *Capability.* Query the model on inputs of its choice, adaptively, at test time. The attacker does not change the model or its training data.

**Input.** A model that maps $x \in [0, 1]^d$ to class confidences $p_1(x), \ldots, p_k(x)$ that sum to $1$; a class $\ell$; a step size $\lambda > 0$; a step limit $\alpha$; a window $\beta \ge 1$; a cost target $\gamma$.

**Output.** A point $\hat{x} \in [0, 1]^d$ with a low cost $c(\hat{x}) = 1 - p_\ell(\hat{x})$, that is, an input on which the model is very sure of class $\ell$, and its cost.

## The algorithm

```pseudo id=main
MI-FACE(c, alpha, beta, gamma, lambda)
L1  x_0 <- 0
L2  for i = 1 to alpha do
L3      x_i <- PROCESS(x_{i-1} - lambda grad c(x_{i-1}))
L4      if c(x_i) >= max(c(x_{i-1}), ..., c(x_{i-beta})) then break
L5      if c(x_i) <= gamma then break
L6  return the x_i of least cost c(x_i), and that cost
```

The cost is $c(x) = 1 - p_\ell(x)$. Line L4 stops when the cost has not gone below the largest of the last $\beta$ costs, and line L5 stops when the cost is low enough. In Algorithm 1 of Fredrikson et al. the cost can have an extra term with auxiliary information, and PROCESS is an image filter (identity for two of their models; denoise and sharpen for the third). On this page PROCESS is the projection onto the box $[0, 1]^d$, that is, a clip of each coordinate, and there is no extra term. When fewer than $\beta$ costs exist, line L4 uses all of them, including $c(x_0)$.

The gradient of the cost comes from the model:

- binary logistic model $p_1(x) = \sigma(w \cdot x + b)$: $\nabla c(x) = -\sigma'(z)\, w$ with $z = w \cdot x + b$ and $\sigma' = \sigma(1 - \sigma)$;
- [softmax regression](/softmax-regression/) $p = \operatorname{softmax}(W x + b)$: $\nabla c(x) = -p_\ell(x)\big(W_\ell - \sum_j p_j(x) W_j\big)$;
- any network: $\nabla c(x) = p_\ell(x)\, \nabla_x \text{CE}(x, \ell)$, since $p_\ell = e^{-\text{CE}}$ for the cross-entropy loss CE;
- black box: $2d$ queries per step for a central difference, as in Section 5.3 of Fredrikson et al.

## Example

A binary logistic model with $w = (2, -1)$ and $b = 0$, class $\ell = 1$, $\lambda = 1$, $\beta = 1$, $\gamma = 0$.

| $i$ | $x_i$ | $z = w \cdot x_i$ | $c(x_i) = 1 - \sigma(z)$ |
|---|---|---|---|
| 0 | $(0, 0)$ | $0$ | $0.5$ |
| 1 | $(0.5, 0)$ | $1$ | $0.2689$ |
| 2 | $(0.8932, 0)$ | $1.7864$ | $0.1435$ |
| 3 | $(1, 0)$ | $2$ | $0.1192$ |
| 4 | $(1, 0)$ | $2$ | $0.1192$ |

At $x_0$ the gradient is $-\sigma'(0) w = (-0.5, 0.25)$, so the step gives $(0.5, -0.25)$, and the clip gives $(0.5, 0)$. The second coordinate stays at $0$ because $w_2 < 0$ pushes it down. At step 3 the first coordinate passes $1$ and is clipped. At step 4 nothing moves, the cost does not go down, and line L4 stops. The result is $(1, 0)$, the corner of the box where $w \cdot x$ is largest, with cost $1 - \sigma(2) = 0.1192$.

## Correctness

The attack has no right answer in general: on a neural network it finds a local minimum of a nonconvex cost, and how much the result tells about a person is a measurement. What is proved, in the proof file, is the following.

**Theorem (the gradients).** The three gradient formulas above are the gradients of $c$; for the network, at every point where no hidden pre-activation is $0$.

**Theorem (binary logistic model).** Let $w$ have no zero entry, let $M = \lVert w \rVert_1 + |b|$, $s = \sigma'(M)$ and $m = \min_j |w_j|$. The minimizer of $c$ on $[0, 1]^d$ is the corner $x^*_j = [w_j > 0]$. With $\gamma < c(x^*)$ and $\alpha \ge N$, where $N = \lceil 1/(\lambda s m) \rceil$, MI-FACE returns $x^*$, in exact arithmetic, and with $\alpha \ge N + \beta$ line L4 ends the run. The reason: every coordinate moves toward its end of $[0, 1]$ by at least $\lambda s m$ per step until it gets there, so the cost goes down at every step before $x^*$, and line L4 cannot stop the run early.

**Theorem (softmax regression).** The function $\ln p_\ell(x) = (W x + b)_\ell - \ln \sum_j e^{(W x + b)_j}$ is concave. So a point that line L3 does not move is a global minimizer of $c$ on the box, and for every $x$ in the box the gap $\max_{u \in [0, 1]^d} \nabla \ln p_\ell(x) \cdot (u - x)$, which is a sum of $d$ easy terms, bounds $\ln p_\ell(x^*) - \ln p_\ell(x)$ from above.

**Heuristic (networks).** For a network with hidden layers the cost is not convex in $x$, and MI-FACE can stop at a local minimum or at an input that no human would recognize. Fredrikson et al. report that their reconstructions from a multilayer network were much less clear than from softmax regression.

## Complexity

- **One step.** One gradient and one cost: $O(k d)$ for softmax regression, $O(h d + k h)$ for a network with $h$ hidden units, and $2d$ queries for a black box gradient. Line L4 reads up to $\beta$ costs.
- **Whole run.** At most $\alpha$ steps: $O(\alpha (k d + \beta))$ for softmax regression.
- **Space.** The code keeps all costs, $O(\alpha + d)$; a ring buffer of the last $\beta$ costs gives $O(\beta + d)$.

## Properties

- **Needs only scores.** With numeric gradients the attack needs only the confidence scores, at $2d$ queries per step.
- **A prototype, not a record.** For a class with many training records the result is the input the model is most sure of. In the tests it is at distance more than $0.5$ from every training record of its class, while the records lie within $0.39$ of their class mean, at $0.25$ on average (a measurement).
- **More sure than the data.** In the tests the cost at the result is below $0.01$, and the cost at the mean of the class is above $0.08$ (a measurement).
- **Local.** On a nonconvex model the result depends on $x_0$ and $\lambda$.

## Variants and improvements

- **Inversion of one feature.** The attack of Fredrikson et al. (2014), as given in Section 3 of the 2015 paper, knows all features of a person but one sensitive feature $x_1$ with few values, and the label $y$. It tries each value $v$ and returns the $v$ that maximizes $\text{err}(y, f(v, x_2, \ldots, x_t)) \prod_i p_i(x_i)$, a [maximum a posteriori](/maximum-a-posteriori-estimation/) estimate with the marginal priors $p_i$ and an error model err.
- **Decision trees with counts.** A white-box [decision tree](/decision-tree/) can report how many training records reach each leaf. Fredrikson et al. (2015, Section 4) use these counts in a better estimate and report no false positives on two survey models.
- **A generative prior.** Zhang et al. (2020) search in the input space of a generative model trained on public data, so that the result stays close to natural inputs.
- **Inversion of gradients.** In federated training a client sends gradients, not a model, and the gradients of one batch can be inverted to its inputs. See [gradient-inversion-attack](/gradient-inversion-attack/); secure aggregation by [secure multiparty computation](/secure-multiparty-computation/) is a defense there.
- **Defenses.** Rounding of the reported confidence (Fredrikson et al. 2015, Section 6) breaks numeric gradients for small difference steps. Differential privacy in training, for example [DP-SGD](/dp-sgd/), bounds what one record can change in the model; Fredrikson et al. (2014) report that budgets small enough to stop their attack made the dosing model worse for patients in simulation.

## When to use it

Use it to measure what a model that you own, or a model trained on synthetic data, leaks about its classes or about one sensitive feature, before you release it or put it behind an interface that returns scores. It is most meaningful when each class is one person or one small group, as in face recognition. For a test of whether a given record was in the training set, use a [membership inference attack](/membership-inference-attack/) instead. For a guarantee about each record, use [differential privacy](/differential-privacy-definition/), since a failed inversion does not show that a model is safe.

## Pitfalls

- **Inference is not always a leak.** If a model learns that one feature predicts another in the whole population, an estimate of that feature for any person, in the training set or not, follows. Compare the attack on training members with the same attack on nonmembers; Fredrikson et al. (2015, Figure 5c) found members at higher risk on their tree models.
- **Rounding is not a guarantee.** In the tests, rounding the scores to multiples of $0.05$ stops a black box attack with difference step $0.001$ (it identifies $1$ class of $6$, the rate of a guess), but a step of $0.1$ gets back $4$ of $6$. Rounding hides small changes, not large ones. Rounding does nothing against a white-box attacker.
- **Judge the result fairly.** Success of a face reconstruction needs a human or a separate model to judge it. Fredrikson et al. asked workers to pick the person from a line up of five; a line up from a much larger set is harder.
- **Step size and box.** With a step that is too large the cost goes up and line L4 stops at once; without the clip, the result leaves the valid input range.

## Implementations

The code runs only on models and data that the tests build from a fixed seed: binary logistic models, softmax regressions and tiny ReLU networks from the shared helper mlkit, in at most $8$ dimensions. It never queries a real model or reads a real data set. The tests check the example; check on $500$ random binary logistic models that MI-FACE returns the best corner within the step bound of the theorem; check the analytic gradients against central differences on $500$ points for each model type; and check on $500$ random softmax regressions that the concavity gap at the result is below $10^{-3}$. A measurement with seed 7604 trains a softmax regression on $6$ synthetic classes of $10$ records in $8$ dimensions. For each class, the white-box and the black-box result is nearest to the mean of the right class ($6$ of $6$ both times), at distance $0.72$ to $0.88$ from every record of the class. With scores rounded to $0.05$, black box differences of step $0.001$ identify $1$ class of $6$, and of step $0.1$, $4$ of $6$.

## History

Fredrikson, Lantz, Jha, Lin, Page and Ristenpart (2014) introduced model inversion on a linear model for warfarin dosing and found that it estimates a patient's genetic marker about as well as a model trained to predict it. Fredrikson, Jha and Ristenpart (2015) turned to services that return confidence scores: they inverted decision trees on lifestyle surveys and recovered recognizable faces from face recognition models with MI-FACE, where human workers picked the right person from a line up in up to $87$ percent of the cases for softmax regression. They also tried rounding of the scores and a tree training method that places the sensitive feature carefully. Later work, for example Zhang et al. (2020), added priors from generative models to invert deep networks.

## References
