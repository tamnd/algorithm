---
tag: RHC19E
kind: algorithm
slug: defensive-distillation
name: Defensive distillation
aliases:
- distillation defense
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: "An empirical defense that retrains a network on its own soft labels at a high temperature. It makes softmax gradients tiny but leaves the boundaries in place, and Carlini and Wagner broke it."
model: real-ram
complexity:
  vars: {n: the number of training points, d: the input dimension, K: the number of classes, S: the number of training steps}
  time: {worst: O(S n K d)}
  space: {extra: Θ(n K + K d)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2015
  people: [Nicolas Papernot, Patrick McDaniel, Xi Wu, Somesh Jha, Ananthram Swami]
  note: Papernot and coauthors posted defensive distillation in November 2015 (IEEE S&P 2016). Carlini and Wagner showed in 2016 and 2017 that it does not make networks robust.
prereqs: [knowledge-distillation, cross-entropy-loss]
see_also: [carlini-wagner-attack, jacobian-saliency-map-attack, fast-gradient-sign-method, adversarial-training, backward-pass-differentiable-approximation, randomized-smoothing, evasion-attack, pgd-attack]
sources:
  - url: https://arxiv.org/abs/1511.04508
    title: Nicolas Papernot, Patrick McDaniel, Xi Wu, Somesh Jha and Ananthram Swami, Distillation as a defense to adversarial perturbations against deep neural networks, IEEE Symposium on Security and Privacy 2016, pages 582 to 597
    locator: the procedure with a teacher and a student at temperature T, the analysis of the gradients, and the evaluation with JSMA on MNIST and CIFAR10
  - url: https://arxiv.org/abs/1607.04311
    title: Nicholas Carlini and David Wagner, Defensive distillation is not robust to adversarial examples, arXiv 1607.04311, 2016
    locator: the explanation by logits that grow with T, and the changed attacks that succeed on distilled networks
  - url: https://arxiv.org/abs/1608.04644
    title: Nicholas Carlini and David Wagner, Towards evaluating the robustness of neural networks, IEEE Symposium on Security and Privacy 2017, pages 39 to 57
    locator: the attacks on the logits that succeed on distilled networks at the same distances as on undefended ones
  - url: https://arxiv.org/abs/1503.02531
    title: Geoffrey Hinton, Oriol Vinyals and Jeff Dean, Distilling the knowledge in a neural network, NIPS 2014 Deep Learning Workshop
    locator: distillation with a temperature in the softmax, which the defense reuses
  - url: https://arxiv.org/abs/1802.00420
    title: Anish Athalye, Nicholas Carlini and David Wagner, Obfuscated gradients give a false sense of security, ICML 2018
    locator: gradient masking and obfuscated gradients as a general cause of broken defenses
---

Defensive distillation is an empirical defense against adversarial examples, and it is broken. It trains a teacher network with the softmax at a high temperature $T$, labels the training data with the soft outputs of the teacher at that temperature, trains a student on those soft labels at the same $T$, and then uses the student at temperature $1$. Papernot, McDaniel, Wu, Jha and Swami (2016) proposed it. Their abstract reports that it cut the success rate of their attack on an MNIST network from 95 percent to below 0.5 percent. Carlini and Wagner (2016, 2017) then showed that the defense does not make the model more robust. Distillation makes the logits about $T$ times larger, so the softmax saturates and its gradient becomes tiny. Attacks that work on the logits, or that divide the logits by $T$, succeed on the distilled model at the same distances as on an undefended one. The defense is the classic example of gradient masking.

## In plain words

A softmax with temperature $T$ divides the logits by $T$ before the exponentials. A large $T$ gives soft outputs, close to uniform, that show how much the network hesitates between classes.

The defense trains the network twice at a large $T$. The second network learns from the soft outputs of the first. Then it is used at $T = 1$, without the division. Its logits are now large, so its output probabilities are almost exactly $0$ or $1$.

An attacker who follows the gradient of the loss on those probabilities sees an almost flat surface and gets no useful direction. But the borders between the classes have not moved. An attacker who looks at the logits, or divides them by $T$ again, finds adversarial examples as easily as before.

## The problem

Given training data $(x^i, y^i)$, $i = 1, \dots, n$, with $K$ classes, the defense wants a classifier with the same accuracy and fewer adversarial examples. The method works through the softmax with temperature,
$$\operatorname{softmax}_T(z)_k = \frac{e^{z_k / T}}{\sum_j e^{z_j / T}}.$$
It does not change the threat model or the norm of the attack. It changes only how the model is trained. Since no certificate comes with it, it can only be judged by attacks, which is why it is called empirical.

## The algorithm

```pseudo id=main
DEFENSIVE-DISTILLATION(data, K, T, S, lr)
L1  X ← the inputs; Y ← the one-hot labels
L2  teacher ← train with loss H(Y, softmax_T(z(X))) for S steps
L3  Q ← softmax_T(z_teacher(X))                ▷ the soft labels
L4  student ← train with loss H(Q, softmax_T(z(X))) for S steps
L5  return (teacher, student)                  ▷ deploy the student with softmax_1
```

$H(q, p) = -\sum_k q_k \ln p_k$ is the cross-entropy. The paper uses the same architecture for the teacher and the student, and temperatures up to $T = 100$. The code of this page uses softmax regression, $z(u) = Wu + b$, trained from zero by full-batch gradient descent, so that the effect of $T$ has a closed form.

## Example

Take three seeded Gaussian blobs in the plane with centers $(0.3, 0.3)$, $(0.7, 0.3)$ and $(0.5, 0.7)$, $\sigma = 0.08$, 10 points each, from `mlkit.make_blobs` with seed 3. Run the procedure twice for 100 steps: at $T = 1$ with step size $2$ (the baseline), and at $T = 20$ with step size $2 \cdot 20^2$. Both students classify all 30 points correctly.

| | baseline, $T = 1$ | distilled, $T = 20$ |
|---|---|---|
| logits at the first point $(0.3076, 0.4)$ | $(0.6328, -0.7257, 0.0929)$ | $(12.6559, -14.5138, 1.8579)$ |
| probabilities there | $(0.5435, 0.1397, 0.3168)$ | $(0.99998, 1.6 \cdot 10^{-12}, 2.0 \cdot 10^{-5})$ |
| median input gradient of the loss | $2.03$ | $1.0 \cdot 10^{-10}$ |
| median distance to the nearest boundary | $0.17165$ | $0.17165$ |
| FGSM at $\epsilon = 0.1$ in $\ell_\infty$, labels changed | 7 of 30 | 7 of 30 |

The distilled logits are exactly $20$ times the baseline logits, at every input. So the labels and the boundaries are the same, and every point has the same distance to the nearest boundary. Only the softmax changes: the median gradient of the cross-entropy at temperature $1$ drops by a factor of about $2 \cdot 10^{10}$. An attack that uses the size of that gradient, or that computes in low precision where the gradient rounds to $0$, stalls. FGSM uses only the sign, and in float64 the sign survives, so it changes the same 7 labels on both models. On the soft labels of line L3, the first point gets $(0.6349, 0.0918, 0.2733)$ from the teacher at $T = 20$.

## Correctness

The claims here are about what the defense does, and they show why it fails. For softmax regression trained from zero by full-batch gradient descent:

**Theorem 1 (temperature only scales).** Training at temperature $T$ with step size $T^2\eta$ gives weights exactly $T$ times those of training at temperature $1$ with step size $\eta$, at every step.

**Corollary 1.** The distilled student has logits $T$ times those of the student trained at $T = 1$, at every input. So it has the same labels, the same decision boundaries and the same $\ell_2$ distance from every input to the nearest boundary.

**Corollary 2 (the gradient vanishes).** If $u$ has label $y$ with logit margin $\mu > 0$ in the student trained at $T = 1$, the input gradient of the cross-entropy of the distilled student at temperature $1$ has norm at most $2(K - 1)\, T\, e^{-T\mu} \max_k \lVert w_k \rVert_2$.

Theorem 1 is an induction: if the weights are $T$ times larger, $\operatorname{softmax}(z/T)$ is the same, and the gradient in the logits is $1/T$ times larger, so a step of size $T^2\eta$ keeps the factor $T$. Corollary 2 bounds $1 - P_y \le (K - 1)e^{-T\mu}$. The proofs are in `proofs/correctness.md`. Together they show that the defense changes the gradient, not the boundary. A minimal-distance attack, such as [DeepFool](/deepfool/) or the [Carlini-Wagner attack](/carlini-wagner-attack/), has the same optimum on both models. For deep networks this is an explanation that Carlini and Wagner give, not a theorem.

## Complexity

- **Time.** Two trainings of $S$ steps, each $O(n K d)$ for softmax regression, plus $O(n K d)$ for the soft labels. The total is $O(S n K d)$. For a network, the cost is twice the cost of normal training.
- **Space.** $\Theta(n K)$ for the soft labels and $\Theta(K d)$ for the weights.
- **At test time.** No extra cost. The student has the same size as the original model.

## Properties

- **Empirical, and broken.** No certificate. Attacks on the logits defeat it.
- **No change to the boundaries.** In the linear case, exactly (Corollary 1). For networks, Carlini and Wagner find the same distances with their attacks.
- **Gradient masking.** It makes the gradient of the softmax output small, which defeats attacks that rely on that gradient.
- **Keeps accuracy.** The paper reports a small change in accuracy on MNIST and CIFAR10.
- **Cheap.** It costs one extra training run.

## Variants and improvements

- **Changed attacks.** Carlini and Wagner (2016) divide the logits by $T$ before the softmax, or attack the logits directly, and both succeed on distilled networks. Their 2017 attacks use the logits by design.
- **Extended distillation.** Papernot and McDaniel (2017) proposed a version that also uses the uncertainty of the teacher. It is also an empirical defense, with no certificate.
- **Better defenses.** [Adversarial training](/adversarial-training/) with PGD gives real empirical robustness against strong attacks. [Randomized smoothing](/randomized-smoothing/) and bound propagation give certificates.
- **Knowledge distillation itself.** [Knowledge distillation](/knowledge-distillation/) for model compression is a sound method. The problem is only the claim of robustness.

## When to use it

Do not use defensive distillation as a defense. Use it as a study case: to see gradient masking on a small model, to test whether an evaluation would catch a weak defense, or to teach why a defense must be tested with adaptive attacks. For a real defense, use [adversarial training](/adversarial-training/) and test it with strong attacks, or use a certified method.

## Pitfalls

- **Judging a defense by one attack.** The paper evaluated the defense mainly with JSMA on the softmax outputs, the kind of attack that the defense defeats. An adaptive attack must be part of every evaluation.
- **Small gradients are not robustness.** A tiny gradient of the loss says nothing about the distance to the boundary, as the example shows: the gradient falls by $10^{10}$ and the distance is the same.
- **Precision.** In float32, the probabilities round to exactly $0$ and $1$ and the gradient becomes exactly $0$. In float64 the sign often survives. An evaluation that works in one precision can fail in another.
- **Transfer attacks.** Adversarial examples made on an undefended model transfer to the distilled model, since the boundaries are close. See [adversarial transferability](/adversarial-transferability/).
- **Using the student at temperature $T$.** Then the gradients are normal again, and the defense does nothing even against simple attacks.

## Implementations

The code of this page is an abstract model on synthetic data. It trains softmax regression models only on Gaussian blobs that the tests build from a fixed seed with `mlkit.make_blobs`, and it never reads real data or touches a real system. The FGSM step in the tests runs on the same seeded models and data. The tests check the example of the page, edge cases, the gradient of the tempered loss against finite differences on 500 random logit vectors, that training at $T$ with step size $T^2\eta$ gives $T$ times the weights of training at $T = 1$ on seeded data, and that the student agrees with the teacher.

## History

Hinton, Vinyals and Dean (2015) introduced distillation with a temperature to compress large networks. Papernot, McDaniel, Wu, Jha and Swami posted defensive distillation in November 2015 and published it at IEEE S&P 2016, with an evaluation based on JSMA. Carlini and Wagner showed in July 2016 that changed attacks succeed against it, and in their 2017 paper their attacks on the logits found adversarial examples on distilled networks as close as on undefended ones. Athalye, Carlini and Wagner (2018) later named the general problem obfuscated gradients and showed that many other defenses fail in the same way.

## References
