---
tag: EN0RG5
kind: technique
slug: backward-pass-differentiable-approximation
name: Backward pass differentiable approximation
aliases:
- BPDA
- obfuscated gradients
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: Breaks defenses that hide gradients by using the true function on the forward pass and a differentiable stand-in on the backward pass.
prereqs: [pgd-attack, backpropagation, adversarial-example]
see_also: [expectation-over-transformation, pgd-attack, fast-gradient-sign-method, carlini-wagner-attack, defensive-distillation, adversarial-training, randomized-smoothing, interval-bound-propagation]
sources:
  - url: https://arxiv.org/abs/1802.00420
    title: Anish Athalye, Nicholas Carlini and David Wagner, Obfuscated gradients give a false sense of security, circumventing defenses to adversarial examples, ICML 2018, PMLR 80, pages 274 to 283
    locator: the three kinds of obfuscated gradients, BPDA, the reparameterization and EOT attacks, and the study of 9 defenses of ICLR 2018, of which 7 relied on obfuscated gradients (6 circumvented completely and 1 partially)
  - url: https://arxiv.org/abs/1902.06705
    title: Nicholas Carlini, Anish Athalye, Nicolas Papernot, Wieland Brendel, Jonas Rauber, Dimitris Tsipras, Ian Goodfellow, Aleksander Madry and Alexey Kurakin, On evaluating adversarial robustness, arXiv 2019
    locator: the checklist for an evaluation, including the signs of gradient masking
  - url: https://arxiv.org/abs/2002.08347
    title: Florian Tramer, Nicholas Carlini, Wieland Brendel and Aleksander Madry, On adaptive attacks to adversarial example defenses, NeurIPS 2020
    locator: thirteen defenses with an adaptive attack for each, and the lessons for evaluation
---

Backward pass differentiable approximation (BPDA) is a technique of Athalye, Carlini and Wagner (2018) for testing a defense that puts a step $g$ in front of a classifier $f$ and so makes the gradient of $f(g(x))$ useless: zero almost everywhere, undefined, or wrong. Such a step can be a quantization of the input, a non-differentiable image transformation or a projection onto a learned set. Gradient attacks such as [PGD](/pgd-attack/) then fail, and the defense looks robust. BPDA computes $g$ exactly on the forward pass but uses a differentiable function $h \approx g$ on the backward pass, often the identity when $g(x) \approx x$. The gradient is then $J_h(x)^\top \nabla_v L(f(v), y)$ at $v = g(x)$, which is good enough to find adversarial examples. In their study of 9 defenses accepted at ICLR 2018, 7 relied on such obfuscated gradients, and the new attacks circumvented 6 of them completely and 1 partially, in the threat model each paper claimed. The lesson is about evaluation: an attack that fails gives no evidence of robustness when its gradients are broken.

## In plain words

Many defenses add a step before the model, such as rounding the pixels. The rounding gives the attacker a flat gradient, a signal that says "nothing changes here", so the usual attack makes no progress, and the defense seems strong.

The model behind the rounding is still the same weak model. BPDA keeps the real rounding when it runs the input forward, but when it asks which way to move, it pretends the rounding was not there. That answer is close enough to the truth, and the attack works again.

So a defense must be tested by an attacker who knows the defense and adapts the attack to it. A failed attack with broken gradients proves nothing.

## When it applies

- The defended model has the form $f(g(x))$ with $f$ differentiable and $g$ a step whose gradient is zero, missing or misleading, and the attacker knows $g$ (white box).
- A differentiable $h$ with $h(x) \approx g(x)$ is known, or $g(x) \approx x$, so the identity is a good stand-in. A neural network trained to imitate $g$ also works.
- The threat model allows test-time changes of $x$ inside a set $S$, such as $B_\infty(x, \epsilon) \cap [0, 1]^d$.
- It does not help against a defense with a certificate, such as [randomized smoothing](/randomized-smoothing/) or [interval bound propagation](/interval-bound-propagation/), whose guarantee does not depend on gradients. Against random defenses, combine it with [expectation over transformation](/expectation-over-transformation/).

## The template

Notation: $f$ is the classifier, $g$ the defense step, $h$ the differentiable stand-in, $L$ the loss, $\Pi_S$ the projection onto the allowed set $S$. The holes in angle brackets are chosen for each evaluation.

```pseudo id=main
BPDA-EVALUATE(f, g, h, x, y, S)
L1  x' ← x
L2  for i ← 1 to ⟨number of steps⟩ do
L3      v ← g(x')                                  ▷ the true defense on the forward pass
L4      r ← ∇_v L(f(v), y)                         ▷ the gradient of the classifier at g(x')
L5      d ← J_h(x')^T r                            ▷ the stand-in on the backward pass; d = r if h is the identity
L6      x' ← Π_S(x' + ⟨step rule⟩(d))              ▷ a PGD step inside the allowed set
L7  return x'                                      ▷ check f(g(x')) on the true defense
```

Line L3 runs the defense exactly, so the final check at line L7 is on the real system and not on the stand-in. Line L5 is the only change to [PGD](/pgd-attack/). If $h$ is the identity, $d$ is the gradient of $f$ at the processed input $g(x')$; this is like the straight-through estimator used to train networks with quantized units. For defenses whose gradient vanishes or explodes because $g$ is a deep iterative procedure, Athalye et al. use a related idea, reparameterization: write $x = h(z)$ with $g(h(z)) \approx h(z)$ and attack in $z$.

**Cost.** Each step costs one call of $g$, one forward and backward pass of $f$, and one product with $J_h^\top$. With the identity stand-in the cost is that of PGD plus the cost of $g$.

**Why it works.** If $g(x') \approx x'$, then $f(g(x'))$ and $f(x')$ are close functions near the iterates, and so the gradient of $f$ at $g(x')$ points in a useful direction even though $g$ itself has zero gradient. This is a heuristic, not a theorem: a stand-in can fail when $h$ is far from $g$, and then the evaluation must try a better $h$.

## Classic examples

- **Input quantization against PGD.** Let $f$ be a linear score $s(v) = 2v - 1.2$ (label 1 if $s > 0$, label 0 otherwise) on one input, and let $g(x) = \lfloor 4x \rfloor / 4$. At $x = 0.8$, $g(x) = 0.75$ and $s = 0.3$, so the label is 1. The gradient of $s(g(x))$ is $0$ at every point where it exists, so a plain gradient attack does not move. With $h$ the identity, line L5 gives $d = 2$, and one step of $0.1$ down, inside the $\ell_\infty$ budget $0.1$, gives $x' = 0.7$, $g(x') = 0.5$ and $s = -0.2$: the label changes. The same pattern broke defenses based on thermometer encoding and on input transformations such as bit depth reduction.
- **Defensive distillation.** An earlier case of a masked gradient: [defensive distillation](/defensive-distillation/) made the softmax saturate, so gradients of the loss were tiny, but the [Carlini-Wagner attack](/carlini-wagner-attack/) on the logits found adversarial examples at the same distances as before.
- **Projection onto a learned set.** Defenses that move the input to a nearby point of a generative model before classifying it compute $g$ by an inner optimization. Its gradient explodes or vanishes, and BPDA with the identity, or reparameterization, attacks them.
- **Random transformations.** A defense that applies a random resize or padding has a random gradient; BPDA for the non-differentiable parts plus [expectation over transformation](/expectation-over-transformation/) for the randomness breaks it.
- **Training-time defenses are a contrast.** [Adversarial training](/adversarial-training/) changes $f$ itself and keeps true gradients, and it held up in the same study within its threat model.

## Variations

- **A learned stand-in.** When $g(x)$ is not close to $x$, train a small network $h$ to imitate $g$ and use it on the backward pass.
- **Reparameterization.** For an iterative $g$, attack in a latent space $z$ with $x = h(z)$ and $g(h(z)) \approx h(z)$.
- **Combined with EOT.** For random $g$, average the BPDA gradient over many draws of the randomness.
- **Gradient-free checks.** Black-box attacks such as the [boundary attack](/boundary-attack/) or the [zeroth-order attack](/zeroth-order-optimization-attack/) need no gradient at all, so if they beat a white-box gradient attack, the gradients are masked.
- **Adaptive attacks in general.** Tramer, Carlini, Brendel and Madry (2020) circumvented 13 recently published defenses, each with its own adapted attack, and showed that BPDA is one tool among several: the attack must be built for the defense.

## Pitfalls

- **Checking success on the stand-in.** Line L7 must evaluate $f(g(x'))$ with the true $g$; a success of $f(h(x'))$ says nothing about the defense.
- **A bad stand-in.** If $h$ is far from $g$ at line L5, the attack can fail, and the failure is about $h$, not about the defense. Try another $h$ before you report robustness.
- **Too few steps.** With a stand-in the direction is noisy, so line L2 often needs more steps than plain PGD. Report how the attack success changes with the number of steps.
- **Reading a failed attack as a lower bound.** An attack gives an upper bound on robust accuracy, never a lower bound. Only a verifier or a certificate gives a lower bound.
- **Signs of masked gradients.** Carlini et al. (2019) list them: one-step attacks beat iterative ones, black-box attacks beat white-box ones, a larger budget does not reach 100 percent success, or random search finds adversarial examples that gradients miss. If any holds, the gradients are broken somewhere.

## Exercises

1. Let $g(x) = \lfloor kx \rfloor / k$ on $[0, 1]$. Show that the derivative of $s(g(x))$ is $0$ at every point where it exists, for every differentiable $s$, and find the points where it does not exist.
2. In the quantization example, show that every budget $\epsilon > 0.05$ allows an $x'$ with $|x' - 0.8| \le \epsilon$ and the label 0, and that no budget $\epsilon \le 0.05$ does.
3. Suppose $\lVert g(x) - x \rVert_2 \le c$ for every $x$ and the score $s$ of $f$ is $\lambda$-Lipschitz. Show that $|s(g(x)) - s(x)| \le \lambda c$, and explain why an attack on $f$ alone with a margin larger than $\lambda c$ also succeeds against $f \circ g$.

## References
