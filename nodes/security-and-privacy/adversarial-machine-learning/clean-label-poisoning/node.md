---
tag: 9VQR2S
kind: algorithm
slug: clean-label-poisoning
name: Clean-label poisoning
aliases:
- feature collision attack
- poison frogs
area: security-and-privacy/adversarial-machine-learning
level: research
summary: Adds correctly labeled training points, crafted so that a model trained on them misclassifies one chosen target input; Poison Frogs makes their features match the target's.
model: real-ram
complexity:
  vars: {p: the number of iterations, d: the input dimension, h: the feature dimension}
  time: {worst: "O(p h d)"}
  space: {extra: "O(d + h)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2018
  people: [Ali Shafahi, W. Ronny Huang, Mahyar Najibi, Octavian Suciu, Christoph Studer, Tudor Dumitras, Tom Goldstein]
  note: Shafahi et al. gave the attack at NeurIPS 2018 under the title Poison frogs, with targeted poisons that a human labeler would label correctly.
prereqs: [data-poisoning, logistic-regression, proximal-gradient-method, projected-gradient-descent]
see_also: [svm-poisoning-attack, backdoor-attack, spectral-signatures-defense, dp-sgd, adversarial-example, evasion-attack, membership-inference-attack, krum-aggregation]
sources:
  - paper: "Ali Shafahi, W. Ronny Huang, Mahyar Najibi, Octavian Suciu, Christoph Studer, Tudor Dumitras and Tom Goldstein, Poison frogs! Targeted clean-label poisoning attacks on neural networks, Advances in Neural Information Processing Systems 31 (NeurIPS) 2018"
    locator: "the objective (feature distance to the target plus beta times the input distance to the base), the forward-backward splitting procedure, the transfer learning experiments with a frozen feature extractor, and the end-to-end experiments with several poisons and a faint blend of the target into the base"
  - paper: "Pang Wei Koh and Percy Liang, Understanding black-box predictions via influence functions, Proceedings of the 34th International Conference on Machine Learning (ICML) 2017"
    locator: training set attacks that change a few training inputs to flip the prediction on a test input
  - paper: "Chen Zhu, W. Ronny Huang, Ali Shafahi, Hengduo Li, Gavin Taylor, Christoph Studer and Tom Goldstein, Transferable clean-label poisoning attacks on deep neural nets, Proceedings of the 36th International Conference on Machine Learning (ICML) 2019"
    locator: the convex polytope attack, with poisons whose features surround the target, for transfer to unknown feature extractors
  - paper: "Jonas Geiping, Liam Fowl, W. Ronny Huang, Wojciech Czaja, Gavin Taylor, Michael Moeller and Tom Goldstein, Witches' brew: industrial scale data poisoning via gradient matching, International Conference on Learning Representations (ICLR) 2021"
    locator: clean-label poisons whose training gradient matches the gradient of the adversarial loss on the target, for training from scratch
  - paper: "Neehar Peri, Neal Gupta, W. Ronny Huang, Liam Fowl, Chen Zhu, Soheil Feizi, Tom Goldstein and John P. Dickerson, Deep k-NN defense against clean-label data poisoning attacks, ECCV 2020 Workshops"
    locator: removal of training points whose label differs from most of their nearest neighbors in feature space
  - paper: "Battista Biggio and Fabio Roli, Wild patterns, ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317-331, 2018"
    locator: the threat model in three parts, goal, knowledge and capability
---

Clean-label poisoning makes a model misclassify one chosen target input by adding training points that carry their correct labels. The attacker does not control the labels: a human or a pipeline labels the points honestly, and each poison still looks like an ordinary member of its class. In the method of Shafahi et al. (2018), called Poison Frogs, the attacker starts from a *base* input $b$ of the class it wants the target $t$ to fall into, and moves it to a poison $x$ whose features $f(x)$ are close to $f(t)$ while $x$ stays close to $b$. A model trained on the poison with the label of $b$ learns that this region of feature space belongs to the base class, and the target goes with it. The optimization is a forward-backward splitting, that is, a [proximal gradient method](/proximal-gradient-method/); its convergence is a theorem for linear features, and the success of the attack is a measurement.

## In plain words

You want a model to get one particular input wrong, but you can only add training examples, and someone else labels them correctly.

Take an example of the class you want the target to be confused with. Change it a little, so that a person still sees the same class, but so that the model "sees" it like the target. Its label is still correct, so nothing looks wrong.

When the model trains on it, it learns that inputs that look like this to the model belong to the base class. The target looks the same to the model, so it is now put in the base class too.

## The problem

**The threat model**, in the three parts of Biggio and Roli:

- *Goal of the attacker.* A targeted integrity attack: one chosen test input $t$ is classified as the base class, while the accuracy on other inputs stays the same, so that the attack is hard to notice.
- *Knowledge.* The feature map $f$ of the model (white box), as in transfer learning where a public feature extractor is frozen and only the last layer is trained; or a substitute of it. The target input.
- *Capability.* Add a few training points. Their labels are assigned honestly, and each poison must stay close to a real member of its class.

**Input.** A feature map $f : [0, 1]^d \to \mathbb{R}^h$, a target $t$, a base $b \in [0, 1]^d$, a weight $\beta > 0$, a step $\lambda > 0$ and a number of iterations.

**Output.** A poison $x \in [0, 1]^d$ with a small value of

$$F(x) = \lVert f(x) - f(t) \rVert^2 + \beta \lVert x - b \rVert^2 .$$

The first term pulls the features to the target; the second keeps the input near the base, so that its correct label is the label of $b$.

## The algorithm

```pseudo id=main
POISON(f, t, b, beta, lambda, steps)
L1  x <- b
L2  repeat steps times
L3      x_hat <- x - lambda * gradient of ||f(x) - f(t)||^2 at x          (forward step)
L4      x <- clip to [0, 1]^d of (x_hat + 2 lambda beta b) / (1 + 2 lambda beta)   (backward step)
L5  return x
```

Line L3 is a gradient step on the term with the features, which is hard and nonconvex for a network. Line L4 is the exact proximal step of the simple term $\beta \lVert x - b \rVert^2$ together with the box: it minimizes $\beta \lVert x - b \rVert^2 + \frac{1}{2\lambda}\lVert x - \hat{x} \rVert^2$ over $[0, 1]^d$, which is coordinatewise, and so is the clip of the unconstrained minimizer. Shafahi et al. also take a forward step on the feature term and a backward step on the distance term; the formula of line L4 is the exact backward step for $F$ as written on this page, and the box is added here so that the poison is a valid input. The code stops early when no coordinate moves by more than a tolerance.

The poison is then given the label of $b$ and added to the training set; the victim trains as usual.

## Example

Take $d = 2$, the linear feature map $f(x) = x_1 + x_2$ (so $h = 1$), the target $t = (1, 1)$, the base $b = (0, 0)$, $\beta = 1$ and $\lambda = 0.25$. At the base, $F(b) = (0 - 2)^2 + 0 = 4$.

The gradient of $(x_1 + x_2 - 2)^2$ at $b$ is $2(0 - 2)(1, 1) = (-4, -4)$, so line L3 gives $\hat{x} = (1, 1)$, and line L4 gives $x = (1, 1) / 1.5 = (2/3, 2/3)$. The next iteration gives $\hat{x} = (2/3, 2/3) - 0.5(4/3 - 2)(1, 1) = (1, 1)$ again, so $(2/3, 2/3)$ is the fixed point, and it is the minimizer: $F = (4/3 - 2)^2 + 2 \cdot (2/3)^2 = 4/3$.

The poison moves only along $(1, 1)$, the direction that the feature map sees; along $(1, -1)$, which $f$ cannot see, it stays at the base. In high dimension most directions are of this kind, which is why a poison can look like its base and still have the features of the target.

## Correctness

The attack has no correct output; whether the target flips is a measurement. What is proved is about the optimization.

**Theorem (convergence for linear features, proved on this page).** If $f(x) = A x$ and $0 < \lambda \le 1 / (2 \lVert A \rVert_2^2)$, then $F$ has a unique minimizer $x^*$ over $[0, 1]^d$, and the iterates of lines L3 and L4 satisfy $\lVert x_p - x^* \rVert \le (1 + 2\lambda\beta)^{-p} \lVert b - x^* \rVert$. The proof shows that one iteration is a contraction whose fixed points are the minimizers.

**Theorem (the backward step, proved on this page).** Line L4 is the exact minimizer of $\beta \lVert x - b \rVert^2 + \frac{1}{2\lambda} \lVert x - \hat{x} \rVert^2$ over the box.

**Heuristic (ReLU features).** For a network, $\lVert f(x) - f(t) \rVert^2$ is not convex, so the method finds a point with a lower objective, not a global minimum. On each region where the ReLU pattern is fixed the term is a convex quadratic; the tests check that the poison lowers $F$ and stays in the box.

**Heuristic (why the target flips).** A model that fits the poison with the label of $b$ must give the base class to a region of feature space that contains $f(t)$. Shafahi et al. report that one poison was enough in most of their transfer learning trials with a frozen feature extractor, and that end-to-end training needed many poisons and a faint blend of the target into each base. Both are measurements, not theorems.

## Complexity

- **One iteration.** One gradient of the feature term, $O(h d)$ for a linear map or for one ReLU layer, plus $O(d)$ for line L4.
- **Total.** $O(p h d)$ for $p$ iterations; for a deep network replace $h d$ by the cost of one backward pass.
- **Space.** $O(d + h)$.

## Properties

- **Clean labels.** Every poison has the label a human would give it, so label checks do not find it.
- **Targeted and quiet.** Only the target is meant to change; the accuracy on other inputs barely moves, so a drop in test accuracy does not reveal the attack.
- **Needs the features.** The method uses $f$; against an unknown model it must use a substitute, and the poison may not transfer.
- **Depends on dimension.** The poison stays near its base only when many input directions are invisible to $f$, as in images. In the 8-dimensional model of the tests it does not stay near (see Pitfalls).

## Variants and improvements

- **Several poisons and blending.** For end-to-end training, Shafahi et al. use many poisons and blend a faint copy of the target into each base, so that the features cannot separate them again during training.
- **Convex polytope.** Zhu et al. (2019) craft poisons whose features surround the target, which transfers better to feature extractors the attacker does not know.
- **Gradient matching.** Geiping et al. (2021) choose poisons whose training gradient matches the gradient that would flip the target, for models trained from scratch.
- **Backdoors with clean labels.** Poisons with correct labels can also plant a trigger; see [backdoor-attack](/backdoor-attack/).
- **Defenses.** Deep k-NN (Peri et al. 2020) removes training points whose label disagrees with their neighbors in feature space, where a poison sits among target-class points. Filtering by [spectral signatures](/spectral-signatures-defense/) looks for a group of poisons that share a direction. Training with [DP-SGD](/dp-sgd/) limits the effect of any few points on the model. Checking the provenance of training data removes the capability itself.

## When to use it

Use it to measure how much one or a few correctly labeled points can change a model that you own, on synthetic data or on data you control, and to test a defense that filters training data. It shows that label checks are not enough. For untargeted damage to accuracy use [SVM poisoning](/svm-poisoning-attack/) or its relatives; for test-time attacks see [evasion attacks](/evasion-attack/).

## Pitfalls

- **Low dimension.** In the tests, with 8 inputs and 4 features, the poison moves about 65 percent of the way from its base to the target: there are too few invisible directions to hide the change. The method needs high-dimensional inputs, and a small model shows only the mechanism.
- **One poison may not flip a linear head.** In the tests one poison lowers the score of the target but flips none of the 10 targets, because a linear head on 4 features cannot give one point its own region. The paper reports flips with the much wider features of an image network.
- **The weight beta.** A large $\beta$ keeps the poison at the base and does nothing; a small one lets it become the target, which a human would then label as the target's class. The useful value depends on the scales of the input and of the features.
- **The step.** A step $\lambda$ above $1/L$, where $L$ bounds the curvature of the feature term, can make the iterates oscillate.
- **Retraining the features.** If the victim also trains the feature extractor, the features move and the collision of one poison is lost.

## Implementations

The code runs only on feature maps and data that the tests build from a fixed seed: a random linear map, and the hidden layer of a seeded tiny_relu_net from the shared helper mlkit, on inputs in $[0, 1]^d$ with $d \le 8$; it never reads a real data set or touches a real model. The tests check the example, check on 500 random linear problems that the poison satisfies the optimality conditions of the box-constrained problem and equals the closed-form solution of $(A^\top A + \beta I) x = A^\top A t + \beta b$ (by Gaussian elimination) whenever that solution is in the box, check the gradient of the ReLU features against finite differences on 500 points, and check that the poison lowers $F$ on 100 random networks. They then measure a tiny transfer learning model with seed 7501: frozen ReLU features of width 4 on 8 inputs, a logistic head retrained on 40 points plus one poison, and 10 correctly classified targets with mean score $2.0$. One poison lowers the score of its target by $0.44$ on average, and the unmodified base by $0.03$; no target flips.

## History

Barreno et al. (2006, 2010) named causative attacks, and Biggio, Nelson and Laskov (2012) gave the first optimized poisoning of an SVM. Koh and Liang (2017) used influence functions to change a few training inputs and flip a test prediction. Shafahi et al. (2018) gave clean-label poisoning by forward-backward splitting, Zhu et al. (2019) made it transfer with convex polytopes, and Geiping et al. (2021) scaled it to training from scratch by gradient matching. Peri et al. (2020) gave the Deep k-NN defense.

## References
