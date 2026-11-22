---
tag: VZRNHS
kind: algorithm
slug: svm-poisoning-attack
name: Poisoning attack on support vector machines
aliases:
- Biggio poisoning attack
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: Finds a training point that most increases an SVM's validation error by gradient ascent through the incremental SVM solution.
model: real-ram
complexity:
  vars: {n: the number of training points, d: the dimension, v: the number of validation points, s: the number of margin support vectors, p: the number of ascent steps, k: the number of SMO iterations per training}
  time: {worst: "O(p (n^2 d + k n + d s^3 + v d^2))"}
  space: {extra: "O(n^2 + v)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2012
  people: [Battista Biggio, Blaine Nelson, Pavel Laskov]
  note: Biggio, Nelson and Laskov gave the attack at ICML 2012, using the incremental SVM of Cauwenberghs and Poggio (2000) to differentiate the solution. It started the line of work on optimal poisoning as a bilevel problem.
prereqs: [support-vector-machine, hinge-loss, kkt-conditions, data-poisoning]
see_also: [sequential-minimal-optimization, svm-training, quadratic-programming, projected-gradient-descent, clean-label-poisoning, spectral-signatures-defense, backdoor-attack, gaussian-elimination]
sources:
  - paper: "Battista Biggio, Blaine Nelson and Pavel Laskov, Poisoning attacks against support vector machines, Proceedings of the 29th International Conference on Machine Learning (ICML) 2012, arXiv:1206.6389"
    locator: "the attack objective (the hinge loss on a validation set), Algorithm 1 (gradient ascent with a fixed step), equation (10) (the gradient through the KKT conditions of the incremental SVM), and the experiments on artificial data (means (+-1.5, 0), covariance 0.6 I, 25 points per class, 500 validation points) and on MNIST"
  - paper: "Shike Mei and Xiaojin Zhu, Using machine teaching to identify optimal training-set attacks on machine learners, Proceedings of the 29th AAAI Conference on Artificial Intelligence (AAAI) 2015"
    locator: optimal training set attacks as a bilevel program, solved through the KKT conditions of the learner
  - paper: "Luis Munoz-Gonzalez, Battista Biggio, Ambra Demontis, Andrea Paudice, Vasin Wongrassamee, Emil C. Lupu and Fabio Roli, Towards poisoning of deep learning algorithms with back-gradient optimization, Proceedings of the 10th ACM Workshop on Artificial Intelligence and Security (AISec) 2017"
    locator: the poisoning gradient by differentiation through the steps of the learning algorithm
  - paper: "Gert Cauwenberghs and Tomaso Poggio, Incremental and decremental support vector machine learning, Advances in Neural Information Processing Systems 13 (NIPS) 2000"
    locator: the update of the dual solution that keeps the KKT conditions while one point is added or changed, with the sets S, E and R
  - paper: "Marco Barreno, Blaine Nelson, Anthony D. Joseph and J. D. Tygar, The security of machine learning, Machine Learning 81, 2010"
    locator: the taxonomy of attacks, with causative attacks that change the training data
  - paper: "Battista Biggio and Fabio Roli, Wild patterns, ten years after the rise of adversarial machine learning, Pattern Recognition 84, 2018"
    locator: the threat model in three parts, goal, knowledge and capability
  - paper: "Jacob Steinhardt, Pang Wei Koh and Percy Liang, Certified defenses for data poisoning attacks, Advances in Neural Information Processing Systems 30 (NeurIPS) 2017"
    locator: upper bounds on the loss that a poisoning attacker can cause against defenses that remove outliers, for linear models such as the SVM
---

The poisoning attack of Biggio, Nelson and Laskov (2012) is the first optimization attack on the training data of a [support vector machine](/support-vector-machine/). The attacker adds one point $(x_c, y_c)$ to the training set and chooses $x_c$ to maximize the [hinge loss](/hinge-loss/) of the trained SVM on a validation set, by gradient ascent. The gradient goes through the training: when $x_c$ moves a little and no training point changes its role (margin support vector, error vector, or neither), the dual solution changes smoothly, and the [KKT conditions](/kkt-conditions/) give its derivative by a linear solve. On this page the kernel is linear, so the SVM solution is an affine function of $x_c$ on each region where the roles stay fixed. The attack is a local search with no guarantee of a global maximum; its effect is a measurement.

## In plain words

An SVM learns a line that separates two classes. An attacker who can add one training point wants to put it where it hurts the line the most.

Start with a copy of a point of one class and give it the other label. Train the SVM, check how badly it does on some held out points, and work out which way to move the bad point to make that worse. Move it a step that way and repeat.

The hard part is the "which way". Moving the point changes the training, and the line moves in turn. While the same points stay on the margin, the line moves in a simple, predictable way, so the direction comes from one small system of equations. When the points on the margin change, the attack retrains and starts again from there.

## The problem

**The threat model**, in the three parts of Biggio and Roli:

- *Goal of the attacker.* Raise the error of the SVM on clean test data. The attack is not targeted at one test point.
- *Knowledge.* Full: the training set, the learning algorithm, the parameter $C$ and the kernel, and a validation set from the same distribution. This is a worst case for the defender.
- *Capability.* Add one point with a label of the attacker's choice (in Algorithm 1, the flipped label of a cloned point), inside a box of feasible values; several points are added one at a time.

**Input.** Training points $(x_i, y_i)$ with $y_i \in \{+1, -1\}$, a validation set $V = \{(x_k, y_k)\}$, the SVM parameter $C$, a label $y_c$, a start $x_c^{(0)}$, a step $t$, a box $[l, h]^d$, a step limit and a tolerance $\epsilon$.

**Output.** A point $x_c$ in the box with a large value of

$$L(x_c) = \sum_{k \in V} \max\big(0,\ 1 - y_k f_{x_c}(x_k)\big),$$

where $f_{x_c}(x) = \langle w, x \rangle + b$ is the SVM trained on the training set plus $(x_c, y_c)$.

**The SVM.** The dual is $\min_\alpha \tfrac{1}{2}\alpha^\top Q \alpha - \mathbf{1}^\top \alpha$ subject to $0 \le \alpha_i \le C$ and $\sum_i y_i \alpha_i = 0$, with $Q_{ij} = y_i y_j \langle x_i, x_j \rangle$ and $w = \sum_i \alpha_i y_i x_i$. The solution splits the points into the margin support vectors $S$ ($0 < \alpha_i < C$, $y_i f(x_i) = 1$), the error vectors $E$ ($\alpha_i = C$, $y_i f(x_i) \le 1$) and the rest $R$ ($\alpha_i = 0$, $y_i f(x_i) \ge 1$).

## The algorithm

```pseudo id=main
SVM-POISON(training set, V, C, y_c, x_c0, t, box, steps, epsilon)
L1  x_c <- x_c0
L2  for p = 1 to steps do
L3      train the SVM on the training set plus (x_c, y_c); this gives alpha, b, S, E, R
L4      u <- gradient of L at x_c, from the KKT system on S with S, E, R held fixed
L5      x_c <- the projection onto the box of x_c + t u / ||u||
L6      stop if L rose by less than epsilon since the last step
L7  return x_c
```

**Line L4.** Write $K = \begin{pmatrix} Q_{SS} & y_S \\ y_S^\top & 0 \end{pmatrix}$. If the attack point is not in $S$, its $\alpha_c$ is $0$ or $C$ and does not move, and only the column $Q_{Sc}$, with entries $y_s y_c \langle x_s, x_c \rangle$, depends on $x_c$. The derivative of the KKT equations gives, for each coordinate $j$,

$$\frac{\partial (\alpha_S, b)}{\partial x_{c,j}} = -K^{-1} \begin{pmatrix} \alpha_c y_c y_S \odot x_{S,j} \\ 0 \end{pmatrix}, \qquad \frac{\partial w}{\partial x_c} = \sum_{s \in S} y_s x_s \Big(\frac{\partial \alpha_s}{\partial x_c}\Big)^{\!\top} + \alpha_c y_c I,$$

and then $\nabla L = -\sum_{k : y_k f(x_k) < 1} y_k \big( (\partial w / \partial x_c)^\top x_k + \nabla b \big)$. This is the linear kernel case of equation (10) of Biggio et al. In the code, line L3 runs [SMO](/sequential-minimal-optimization/) and then solves the KKT equations exactly on the sets it found, by [Gaussian elimination](/gaussian-elimination/).

## Example

Two classes in the plane, $C = 0.1$: training points $(-2, 0), (-2, 1)$ with label $-1$ and $(2, 0), (2, 1)$ with label $+1$, and validation points $(\pm 1, 0), (\pm 1, 1)$ with the sign of the first coordinate as label. The clean SVM is $w = (0.5, 0)$, $b = 0$: every validation point has margin $0.5$, so $L = 4 \cdot 0.5 = 2$ and the error is $0$.

The attacker adds $x_c = (a, 0.5)$ with label $+1$, starting at $a = -2$. The solution has $\alpha_c = C$, the two points with label $+1$ in $S$ and the other three in $E$. The constraint $\sum y_i \alpha_i = 0$ and the two margin equations give

$$w = (0.6 + 0.1 a,\ 0), \qquad b = -0.2 - 0.2 a, \qquad L(a) = 2.4 - 0.4 (a + 2),$$

so the gradient is $(-0.4, 0)$: move left. With $t = 0.5$ in the box $[-5, 5]^2$ the losses are $2.4, 2.6, \ldots, 3.6$, and the attack stops at $x_c = (-5, 0.5)$, where $L$ no longer rises. The clean points with label $-1$ at first coordinate $-1$ have margin $0.8 + 0.3 a$, which is negative for $a < -8/3$, so from the third step on, half of the validation set is misclassified.

## Correctness

**Theorem (the gradient, proved on this page).** Fix a solution with sets $S, E, R$, the attack point not in $S$, $S \neq \emptyset$, and $K$ nonsingular. On the region of $x_c$ where these sets give a solution of the KKT conditions, $(\alpha_S, b)$ and $w$ are affine functions of $x_c$; where also no validation point has $y_k f(x_k) = 1$, $L$ is differentiable and its gradient is the formula of line L4. The proof differentiates the KKT equations; the KKT conditions are sufficient for the convex dual, so the solution of the equations is the SVM.

**Theorem (flat regions, proved on this page).** With a linear kernel, if $\lvert S \rvert = d + 1$ and the points of $S$ are affinely independent, the $d + 1$ equations $y_s(\langle w, x_s \rangle + b) = 1$ fix $w$ and $b$, so the gradient of $L$ is $0$ on the region. Algorithm 1 then stops.

**What is not proved.** $L$ is not concave in $x_c$, so gradient ascent finds a local maximum at best, and a fixed step may overshoot. Biggio et al. report that the attack finds good local maxima in their experiments; this is a measurement.

## Complexity

- **Time per step.** Training costs $O(n^2 d)$ for $Q$ and $O(k n)$ for $k$ SMO iterations; the exact solve on $S$ costs $O(s^3)$. The gradient solves $K$ for $d$ right sides, $O(d s^3)$ (or $O(s^3 + d s^2)$ with one factorization), and the validation sum costs $O(v d^2)$. The incremental SVM of Cauwenberghs and Poggio updates the solution in place of a full retraining.
- **Total.** $p$ steps, so $O(p (n^2 d + k n + d s^3 + v d^2))$.
- **Space.** $O(n^2)$ for $Q$ and $O(v)$ for the validation set.

## Properties

- **One point at a time.** Several attack points are found one after another, each with the previous ones in the training set.
- **Needs full knowledge.** The gradient needs the training set and the validation set. An attacker with less knowledge must estimate them, for example from a substitute data set.
- **Kernels.** Equation (10) of Biggio et al. holds for any differentiable kernel, so the attack works in input space with a nonlinear kernel. The code covers the linear kernel only.

## Variants and improvements

- **Bilevel poisoning.** Mei and Zhu (2015) wrote optimal training set attacks as a bilevel program, with the learner as the inner problem, and solved it through its KKT conditions for several convex learners.
- **Back-gradient poisoning.** Munoz-Gonzalez et al. (2017) replaced the KKT solve by differentiation through the steps of gradient descent, which reaches neural networks.
- **Certified bounds.** Steinhardt, Koh and Liang (2017) bound the loss that any poisoning of a fixed fraction can cause against an outlier removal defense, for linear models.
- **Targeted poisoning.** [Clean-label poisoning](/clean-label-poisoning/) aims at one test point, and a [backdoor](/backdoor-attack/) at inputs with a trigger.

## When to use it

Use it to measure the worst case robustness of an SVM, or of another convex learner, to a few added points, in a setting where the attacker could know the training data. It is a tool for evaluation on synthetic or owned data, not a defense. For deep networks use back-gradient methods; for a guarantee in place of a measurement use certified bounds. Defenses that remove outliers, such as [spectral signatures](/spectral-signatures-defense/) for a group of poisoned points, do not target this attack.

## Pitfalls

- **Flat regions with a linear kernel.** In low dimension the margin set often has $d + 1$ points, the gradient is $0$, and the attack does not move. The example of the tests in $d = 2$ shows this; in $d = 8$ with 15 points per class the attack moves.
- **The attack point on the margin.** If $x_c$ is a margin support vector, $\alpha_c$ moves too, and the formula of line L4 does not apply. Start from a point deep in the other class, where $\alpha_c = C$.
- **Sets that change.** The gradient holds only while $S$, $E$ and $R$ stay fixed. A large step crosses into another region, and $L$ may fall; line L6 stops there.
- **An inexact solver.** SMO stops at a tolerance, so $\alpha$ is close but not exact, and $K^{-1}$ amplifies the error. The code solves the KKT equations exactly on the sets that SMO finds and checks them.

## Implementations

The code runs only on a linear SVM and on data that the tests build from a fixed seed, two Gaussian blobs in at most 8 dimensions; it never reads a real data set or a deployed model. The tests check the SVM on 500 random problems by a duality certificate (a feasible $\alpha$ whose dual value equals the primal value of $(w, b)$ is optimal, by weak duality), check the gradient against central finite differences where the sets do not change, check the example and the flat region, and measure the attack: on four seeds with the means and covariance of Biggio et al. but $d = 8$ and 15 points per class, one point raises the validation error from 5.0, 5.75, 4.5 and 7.0 percent to 21.0, 12.0, 11.5 and 7.75 percent.

## History

Barreno et al. (2006, 2010) named causative attacks on the training data. Biggio, Nelson and Laskov (2012) gave the first gradient attack on SVM training, using the incremental SVM of Cauwenberghs and Poggio (2000) and experiments on artificial data and MNIST. Mei and Zhu (2015) generalized it to bilevel optimization, Steinhardt, Koh and Liang (2017) gave certified bounds, and Munoz-Gonzalez et al. (2017) extended gradient poisoning to deep networks.

## References
