---
tag: 9G5GMD
kind: technique
slug: model-extraction-attack
name: Model extraction attack
aliases:
- model stealing
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: "Rebuilds a model served behind an API from its answers to chosen queries, exactly for linear models by solving equations."
prereqs: [logistic-regression, gaussian-elimination, adversarial-example]
see_also: [knowledge-distillation, logistic-regression, adversarial-transferability, membership-inference-attack, zeroth-order-optimization-attack, language-model-watermarking, token-bucket, differential-privacy-definition]
sources:
  - url: https://arxiv.org/abs/1609.02943
    title: Florian Tramer, Fan Zhang, Ari Juels, Michael K. Reiter and Thomas Ristenpart, Stealing machine learning models via prediction APIs, USENIX Security 2016, pages 601 to 618
    locator: the threat model of prediction APIs, equation-solving extraction of models that return confidence values, extraction of decision trees, attacks with labels only, and the countermeasures discussed
  - url: https://arxiv.org/abs/1909.01838
    title: Matthew Jagielski, Nicholas Carlini, David Berthelot, Alex Kurakin and Nicolas Papernot, High accuracy and high fidelity extraction of neural networks, USENIX Security 2020
    locator: the distinction between accuracy and fidelity as goals, and functionally equivalent extraction of small ReLU networks
  - url: https://arxiv.org/abs/1805.02628
    title: Mika Juuti, Sebastian Szyller, Samuel Marchal and N. Asokan, PRADA, protecting against DNN model stealing attacks, IEEE EuroS&P 2019
    locator: detection from the distribution of successive queries of a client, and the report that it detected all prior extraction attacks with no false positives in their experiments
---

A model extraction attack builds a copy of a machine learning model that is served behind a prediction interface, using only the answers of the interface to queries that the attacker chooses. Tramer, Zhang, Juels, Reiter and Ristenpart (2016) showed it on commercial prediction services of the time: models that return confidence values, such as [logistic regression](/logistic-regression/), can be recovered exactly by solving a system of equations, because the confidence determines the value of a linear function of the input; decision trees can be recovered from the paths their answers reveal; and models that return only labels can still be approximated with more queries. The copy can then be used without paying, can leak information about the training data, and helps to craft [adversarial examples](/adversarial-example/) by [transfer](/adversarial-transferability/). This page describes the attack at the level of the papers' abstracts and on an abstract model with symbols. It gives no queries or code for any real service, and most of it is on the threat model, the conditions the attack needs and the defenses.

**Threat model.** The goal is a copy with high accuracy on the task (it is as useful as the original) or with high fidelity (it agrees with the original, even on its mistakes), the distinction of Jagielski et al. (2020). The knowledge is black box: the attacker knows the kind of model and the format of the input, and maybe a little data of the task, but not the weights or the training set. The capability is to send queries and read the answers, within the limits of the interface. The defender controls what the interface returns and how many queries it accepts.

## In plain words

A company trains a model and lets people ask it questions for a fee. A customer who asks enough well-chosen questions can learn enough about the answers to build a model that behaves the same way, and then no longer needs the company.

For simple models this is easy: if the answer includes a confidence score, each answer is an equation in the unknown weights, and a few answers are enough equations to solve for all of them. For complex models, the attacker trains a new model on the answers, which needs many more questions.

Defenses return less information with each answer, limit and watch the questions, and mark the model so that a stolen copy can be recognized.

## When it applies

- **Rich answers.** Confidence values or probabilities reveal much more per query than labels. A model that returns its logit, or a probability from which the logit can be computed, gives one exact equation per query.
- **Chosen inputs.** The attacker must be able to choose the inputs, including unusual ones far from normal data, which are often the most informative.
- **A known model class.** Exact recovery needs the class of the model, such as linear or a tree of a known depth. Without it, the attacker trains a substitute, as in [knowledge distillation](/knowledge-distillation/), and gets an approximation.
- **Enough queries.** The cost of the attack is the number of queries. It is small for linear models (about the number of parameters) and large for deep networks.
- **Price and limits.** The attack is worth it when a query is cheap compared with training the model, and when the interface does not limit or watch queries.

## The template

The stages of the published methods at the level of their abstracts, with the point where each defense acts. None of the holes is a query, a parameter or a threshold of a real attack.

```pseudo id=main
EXTRACTION-THREAT-MODEL(interface A of a model f, model class C)
L1  choose ⟨query inputs⟩                                ▷ defense: query monitoring (PRADA), rate limits
L2  send them to A and record ⟨the answers⟩              ▷ defense: labels only, rounded confidences, noise
L3  if C is simple then solve ⟨equations in the parameters⟩ from the answers
L4  else train ⟨a substitute model⟩ on the pairs           ▷ cost grows with the information per answer
L5  compare the copy with A on ⟨fresh inputs⟩             ▷ accuracy or fidelity; defense: watermarks to prove theft
```

The defender acts at lines L1, L2 and L5. Lines L3 and L4 run on the attacker's side, after the answers are known.

**The defense points.**
- **Return less (line L2).** Return only the label, or round the confidence to a few digits. Tramer et al. found that rounding raises the cost of equation solving and that attacks with labels only need many more queries; it does not stop extraction.
- **Add noise to answers (line L2).** Randomize the answers, in the extreme with [differential privacy](/differential-privacy-definition/) for the parameters; this costs accuracy for honest clients.
- **Watch the queries (line L1).** PRADA (Juuti et al. 2019) analyzes the distribution of the successive queries of a client and raises an alarm when it differs from that of benign clients. The authors report that it detected all prior extraction attacks with no false positives in their experiments, a measurement; an attacker who knows the detector can try to make queries look normal.
- **Limit and price queries (line L1).** Rate limits, for example with a [token bucket](/token-bucket/), and accounts bound to identities raise the cost of the many queries of line L4.
- **Mark the model (line L5).** Embed a watermark or a set of secret inputs with chosen answers, so that the owner can show that a suspect model is a copy. This does not prevent theft; it helps to prove it. [Watermarks for text](/language-model-watermarking/) are the same idea for the outputs of language models.

## Classic examples

- **Equations for a logistic model, on an abstract model.** Let $f(x) = \sigma(w^\top x + b)$ with unknown $w \in \mathbb{R}^d$ and $b$, and suppose the interface returns $p = f(x)$ exactly. Then $\ell(x) = \ln(p / (1 - p)) = w^\top x + b$ is a known linear function of the unknowns, so $d + 1$ answers at inputs in general position give a linear system with a unique solution, solved by [Gaussian elimination](/gaussian-elimination/). For example, with symbols: at the inputs $0, e_1, \dots, e_d$ the values are $\ell_0 = b$ and $\ell_i = w_i + b$, so $b = \ell_0$ and $w_i = \ell_i - \ell_0$. If the interface rounds $p$, each $\ell$ is known only within an interval, and the system gives a set of possible parameters, not one; that is why rounding helps the defender.
- **Substitute models.** For deep networks, the attacker trains a model on the answers to its queries, which is [knowledge distillation](/knowledge-distillation/) with the interface as the teacher. The copy is approximate and is useful for transfer attacks.
- **Functionally equivalent copies.** Jagielski et al. (2020) showed that for small ReLU networks with exact outputs, the weights can in principle be recovered up to the symmetries of the network, by locating the points where units switch on and off; this needs exact answers, which rounding removes.
- **Gradient-free attacks.** [Zeroth-order attacks](/zeroth-order-optimization-attack/) use the same kind of access to find adversarial examples directly, without building a copy.
- **Privacy.** A copy can be used for [membership inference](/membership-inference-attack/) offline, so extraction can turn a commercial loss into a privacy loss.

## Variations

- **Labels only.** Learning the model from labels alone is an active learning problem; the number of queries grows with the complexity of the decision boundary.
- **Fidelity against accuracy.** A copy that matches the original's mistakes is better for transfer attacks; a copy that is merely accurate is better for free use. The two goals need different queries.
- **Extraction of hyperparameters and architecture.** Related work recovers the training settings or the structure of a model, not only its weights.
- **Language models.** The same economics apply to large models served by interfaces: training a smaller model on a larger model's answers transfers much of its behavior, which is why many providers restrict that use in their terms and in their interfaces.

## Pitfalls

These are pitfalls for defenders.
- **Returning full precision without need.** A confidence with many digits at line L2 gives exact equations. Return what the application needs and no more.
- **Assuming labels only is enough.** Labels make extraction costlier, not impossible; combine them with limits at line L1.
- **A detector without an adaptive test.** A query monitor at line L1 should be tested against an attacker who knows it, as with every defense in adversarial machine learning.
- **Ignoring the training data.** A copy of the model can leak its training data; extraction is also a privacy problem, and defenses for it include training with differential privacy.
- **Watermarks that do not survive training.** A mark at line L5 must still be detectable after the copy is fine-tuned or distilled; test this before you rely on it.

## Exercises

1. In the abstract logistic model with $d = 2$, the interface returns the exact logits $\ell(0, 0) = c_0$, $\ell(1, 0) = c_1$ and $\ell(0, 1) = c_2$ for made-up numbers $c_i$. Write $w$ and $b$ in terms of the $c_i$, and show that a fourth query cannot change the answer.
2. Suppose the interface rounds every probability to the nearest multiple of $10^{-k}$, and the true probabilities lie in $[0.1, 0.9]$. Bound the error of each logit $\ell$ in terms of $k$, and then the error of each recovered $w_i$ in the scheme of the first exercise.
3. Explain why a copy with high fidelity is more useful for crafting adversarial examples against the original than a copy with the same accuracy but low fidelity.

## References
