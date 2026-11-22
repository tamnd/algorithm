---
tag: AMRY1H
kind: technique
slug: expectation-over-transformation
name: Expectation over transformation
aliases:
- EOT
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: "Optimizes an adversarial example for the expected loss over random transformations such as rotation and lighting, so it works in the physical world."
prereqs: [pgd-attack, stochastic-gradient-descent, adversarial-example]
see_also: [backward-pass-differentiable-approximation, pgd-attack, universal-adversarial-perturbation, adversarial-transferability, randomized-smoothing, adversarial-training, stochastic-gradient-descent, monte-carlo-integration]
sources:
  - url: https://proceedings.mlr.press/v80/athalye18b.html
    title: Anish Athalye, Logan Engstrom, Andrew Ilyas and Kevin Kwok, Synthesizing robust adversarial examples, ICML 2018, PMLR 80, pages 284 to 293
    locator: the EOT objective with a distance constraint in expectation, the 2D results under noise, distortion and affine transformations, and the 3D printed objects (arXiv:1707.07397)
  - url: https://arxiv.org/abs/1802.00420
    title: Anish Athalye, Nicholas Carlini and David Wagner, Obfuscated gradients give a false sense of security, circumventing defenses to adversarial examples, ICML 2018, PMLR 80, pages 274 to 283
    locator: EOT as the attack against defenses with random gradients
  - url: https://arxiv.org/abs/1902.06705
    title: Nicholas Carlini, Anish Athalye, Nicolas Papernot, Wieland Brendel, Jonas Rauber, Dimitris Tsipras, Ian Goodfellow, Aleksander Madry and Alexey Kurakin, On evaluating adversarial robustness, arXiv 2019
    locator: the advice to attack random defenses with EOT and to report the number of samples
  - url: https://arxiv.org/abs/2002.08347
    title: Florian Tramer, Nicholas Carlini, Wieland Brendel and Aleksander Madry, On adaptive attacks to adversarial example defenses, NeurIPS 2020
    locator: adaptive attacks on random defenses with enough EOT samples
---

Expectation over transformation (EOT) is a technique of Athalye, Engstrom, Ilyas and Kwok (2018) for finding an input change that fools a classifier not at one fixed view of the input but on average over a distribution $T$ of transformations $t$, such as rotation, scaling, lighting, noise or a random step of a defense. The adversary maximizes $E_{t \sim T}[\log P(y_{\text{target}} \mid t(x'))]$ under a bound on the expected distance $E_{t \sim T}[d(t(x'), t(x))]$, and estimates the gradient of the expectation by the mean gradient over a few sampled $t$, as in [stochastic gradient descent](/stochastic-gradient-descent/). With it, the authors made 2D images that stayed adversarial under noise, distortion and affine transformations, and 3D-printed objects that a classifier labelled as the target class from most viewpoints. In the evaluation of defenses, EOT is the standard answer to randomness: a defense that adds a random step to the input has a random gradient, and an attack that uses one sample of it is too weak.

## In plain words

An adversarial example usually works only for one exact picture. Turn it a little, change the light, or print it, and the trick stops working.

EOT asks for a change that works for many views at once. At each step it draws several random views of the current input, asks how to change the input to fool the model on all of them, and moves in the average direction. The result fools the model across the whole range of views.

The same idea tests defenses that use randomness. If a defense blurs or shifts the input at random, one gradient is noisy, but the average of many gradients still points the right way.

## When it applies

- The input reaches the model through a random transformation $t \sim T$, either from the world (camera angle, distance, light) or from a random defense (random resizing, padding, noise, dropout at test time).
- The attacker can sample from $T$, or from a model of it, and $t$ is differentiable or has a usable stand-in, as with [BPDA](/backward-pass-differentiable-approximation/).
- The goal is success on average or with high probability over $t$, not for one fixed $t$.
- For a defense with a certificate over the randomness, such as [randomized smoothing](/randomized-smoothing/), EOT cannot beat the certified radius; it can only find inputs outside it.

## The template

Notation: $f$ is the model, $L$ the loss of the adversary (for a target label, the negative log probability of the target), $T$ the distribution of transformations, $S$ the allowed set of inputs, and $\Pi_S$ the projection onto it. The holes in angle brackets are chosen for each evaluation.

```pseudo id=main
EOT-EVALUATE(f, x, T, S)
L1  x' ← x
L2  for i ← 1 to ⟨number of steps⟩ do
L3      draw t_1, ..., t_m from T                   ▷ m = ⟨samples per step⟩
L4      g ← (1/m) Σ_j ∇_{x'} L(f(t_j(x')))          ▷ an unbiased estimate of ∇ E_t[L(f(t(x')))]
L5      x' ← Π_S(x' - ⟨step rule⟩(g))               ▷ a step of projected gradient descent on the expected loss
L6  return x'                                      ▷ measure the success rate over fresh draws of t
```

Line L4 is the whole idea. Under mild conditions (for example a loss that is differentiable in $x'$ for each $t$, with a gradient bounded by an integrable function), the gradient of the expectation is the expectation of the gradient, so the mean over $m$ samples is an unbiased estimate with variance that falls like $1/m$. Line L5 is the same step as [PGD](/pgd-attack/) or as the Lagrangian form of the paper, which adds the distance term to the loss. Line L6 must use new samples of $t$, so that the reported success is not fitted to the samples used in the search.

**Cost.** Each step costs $m$ forward and backward passes. Evaluations of random defenses often need tens or hundreds of samples per step before the success rate stops growing.

**What it measures.** The result is an upper bound on the robust accuracy of the random system as a whole: the fraction of inputs for which the attack fails, averaged over the randomness. This is a measurement for one attack, not a guarantee.

## Classic examples

- **A toy random defense.** Let a defense add a random shift $u \in \{-0.2, 0, 0.2\}$, each with probability $1/3$, to a single input before the linear score $s(v) = v - 0.5$. At $x = 0.7$ the scores are $0$, $0.2$ and $0.4$, so the input is classified as positive (label 1 if $s > 0$) with probability $2/3$. One sampled gradient is always $1$ here, so this defense does not hide the direction; but with a nonlinear $f$ the sampled gradients disagree, and their mean at line L4 is the gradient of the expected loss. Moving $x$ down to $0.5$ makes the scores $-0.2$, $0$ and $0.2$, so the positive label survives with probability only $1/3$.
- **Physical objects.** Athalye et al. used a distribution over 3D poses, lighting and camera noise and changed the texture of 3D-printed objects so that an ImageNet classifier gave the target label from most viewpoints.
- **Random defenses of 2018.** In Athalye, Carlini and Wagner (2018), defenses based on random input transformations and random pruning of activations fell to EOT, often together with [BPDA](/backward-pass-differentiable-approximation/).
- **Universal perturbations.** A [universal adversarial perturbation](/universal-adversarial-perturbation/) is the same objective with $T$ the distribution of the data: one change for many inputs.
- **Adversarial training under transformations.** The defense side of the same objective trains the model on transformed adversarial inputs; see [adversarial training](/adversarial-training/).

## Variations

- **A distance constraint in expectation.** The paper bounds $E_t[d(t(x'), t(x))]$, for example the distance in a perceptual color space, so that the change stays small in every view.
- **More samples or more steps.** When the gradient variance is high, increase $m$ at line L3 or run more steps; both cost forward passes.
- **Stand-ins for non-differentiable transformations.** Use a differentiable renderer or BPDA for $t$ when it has no gradient.
- **Worst case over $T$.** Replace the expectation by a maximum over a finite set of transformations when the goal is success for every view, not on average.
- **Transfer across models.** Averaging over an ensemble of models in place of transformations improves [transferability](/adversarial-transferability/).

## Pitfalls

- **Too few samples.** With $m = 1$ at line L3, a random defense can look robust only because the gradient is noisy. Report the success rate as a function of $m$ and of the number of steps, and stop only when it stops growing.
- **A wrong model of $T$.** If the distribution used at line L3 differs from the real transformations, the result can fail in use. For defenses, sample from the exact randomness of the defense.
- **Evaluating on the search samples.** Line L6 must draw fresh transformations; success on the samples of line L3 overstates the rate.
- **Fixing the random seed of the defense.** Attacking one fixed draw of the defense's randomness gives a change that fits that draw only; the defense then appears robust to new draws for the wrong reason.
- **Reading the result as a lower bound.** Like every attack, EOT gives an upper bound on robust accuracy. Only a verifier or a certificate gives a lower bound.

## Exercises

1. In the toy random defense, find the set of inputs $x$ for which the positive label has probability exactly $2/3$, $1/3$ and $0$.
2. Let $L(x', t)$ be differentiable in $x'$ with $|\partial L / \partial x'| \le B$ for every $t$. Use the dominated convergence theorem to show that $\frac{d}{dx'} E_t[L(x', t)] = E_t[\partial L(x', t) / \partial x']$, and show that the mean of $m$ independent sampled gradients has variance at most $B^2 / m$.
3. Explain why EOT cannot produce an input with the wrong label of a smoothed classifier inside its certified radius, even with an unlimited number of samples.

## References
