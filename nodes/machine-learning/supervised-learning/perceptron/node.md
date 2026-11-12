---
tag: 83YNZY
kind: algorithm
slug: perceptron
name: Perceptron
aliases:
- perceptron learning algorithm
- Rosenblatt perceptron
- perceptron learning rule
area: machine-learning/supervised-learning
level: intro
summary: Online learner for a linear classifier. On each mistake it adds y times x to the weights. On separable data it stops after at most (R/γ)^2 mistakes.
solves: [halfspace-learning]
model: real-ram
complexity:
  vars: {n: the number of examples, d: the number of features, m: "the number of mistakes, at most (R/γ)^2 on separable data"}
  time: {worst: "O((m + 1) n d)", best: "Θ(n d)"}
  space: {extra: Θ(d)}
properties: {deterministic: true, online: true, exact: true, recursive: false}
history:
  year: 1958
  people: [Frank Rosenblatt]
  note: Rosenblatt described the perceptron in Psychological Review in 1958. Novikoff and Block proved the mistake bound in 1962.
prereqs: [linear-separability]
see_also: [perceptron-convergence-theorem, winnow, support-vector-machine, kernel-trick, halfspace-learning, hinge-loss, stochastic-gradient-descent, logistic-regression]
sources:
  - paper: doi:10.1037/h0042519
    title: Frank Rosenblatt, The perceptron, a probabilistic model for information storage and organization in the brain, Psychological Review 65(6), 1958
    locator: pp. 386 to 408 (the perceptron and its reinforcement rule)
  - paper: "A. B. J. Novikoff, On convergence proofs on perceptrons, Proceedings of the Symposium on the Mathematical Theory of Automata, Volume 12, Polytechnic Institute of Brooklyn, 1962"
    locator: the bound (R/γ)^2 on the number of corrections
  - paper: doi:10.1023/A:1007662407062
    title: Yoav Freund and Robert E. Schapire, Large margin classification using the perceptron algorithm, Machine Learning 37(3), 1999
    locator: the voted perceptron, the averaged version, the kernel form and the bound for data that is not separable
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Section 9.1.2 (the perceptron for halfspaces and its mistake bound) and Chapter 21 (online learning)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 4.5.1, Rosenblatt's perceptron learning algorithm
---

The perceptron is an online algorithm that learns a linear classifier $x \mapsto \operatorname{sign}(w \cdot x + b)$ for labels $y \in \{-1, +1\}$. It looks at one example at a time, and when it makes a mistake it adds $y x$ to $w$ and $y$ to $b$. On [linearly separable](/linear-separability/) data it stops after a finite number of mistakes, at most $(R/\gamma)^2$ by the [perceptron convergence theorem](/perceptron-convergence-theorem/). On data that is not separable it never stops, and its weights cycle.

## In plain words

You want a straight line (in higher dimensions, a flat plane) that puts the positive points on one side and the negative points on the other. Start with a line that knows nothing. Go through the points one by one. If a point is on the correct side, do nothing. If it is on the wrong side, push the line toward that point: add the point to the weights when the point is positive, and subtract it when the point is negative. Go through the data again and again until a full pass makes no mistake.

When a separating line exists, this stops. The number of pushes depends only on how large the points are and how wide the gap between the two classes is, not on the number of points.

## The problem

The input is a training set $S = ((x_1, y_1), \ldots, (x_n, y_n))$ with $x_i \in \mathbb{R}^d$ and $y_i \in \{-1, +1\}$. The output is a weight vector $w \in \mathbb{R}^d$ and a bias $b \in \mathbb{R}$ with $y_i (w \cdot x_i + b) > 0$ for each $i$, when such a pair exists. This is the consistent case of [halfspace learning](/halfspace-learning/). The data model is the realizable online model: the examples come in any order, possibly chosen by an adversary, and some halfspace labels all of them correctly. The cost is the number of mistakes. In the batch setting, the algorithm passes over $S$ again and again.

We write $R = \max_i \lVert x_i \rVert$, and $\gamma$ for the margin of a separator, defined on the [convergence theorem](/perceptron-convergence-theorem/) page.

## The algorithm

```pseudo id=main
PERCEPTRON(S, T)                           ▷ S = ((x_1, y_1), ..., (x_n, y_n)), at most T epochs
L1  w ← 0 ∈ R^d, b ← 0
L2  for epoch ← 1 to T do
L3      errors ← 0
L4      for i ← 1 to n do
L5          if y_i (w · x_i + b) ≤ 0 then          ▷ a mistake; 0 counts as a mistake
L6              w ← w + y_i x_i
L7              b ← b + y_i                       ▷ the weight of a constant feature 1
L8              errors ← errors + 1
L9      if errors = 0 then return (w, b)          ▷ a full pass with no mistake
L10 return (w, b)                                 ▷ no separator found in T epochs
```

Line L5 tests the sign of the margin $y_i (w \cdot x_i + b)$. The test is $\le 0$, not $< 0$, so a point on the hyperplane is a mistake. With $w = 0$ at the start, the first example is always a mistake.

Lines L6 and L7 are one update of the augmented vector $(w, b)$ by $y_i (x_i, 1)$. So the bias is the weight of an extra feature that is always 1. If the extra feature is a constant $c$ instead of 1, the extra weight $w_0$ gives $b = c w_0$, and line L7 becomes $b \leftarrow b + y_i c^2$. The value of $c$ changes the mistake bound, because it changes the radius of the augmented points; see the [convergence theorem](/perceptron-convergence-theorem/).

Line L9 stops after a pass with no mistake. In such a pass $(w, b)$ does not change, so the returned pair classifies each example correctly.

## Example

Take six points in $\mathbb{R}^2$ with the bias feature 1, in this order: $x_1 = (2, 1)$ and $x_2 = (0, 2)$ with $y = +1$, $x_3 = (-1, 0)$, $x_4 = (1, -2)$ and $x_5 = (-2, 1)$ with $y = -1$, and $x_6 = (3, 3)$ with $y = +1$.

| epoch | $i$ | $x_i$ | $y_i$ | $w \cdot x_i + b$ | mistake | $w$ after | $b$ after |
|---|---|---|---|---|---|---|---|
| 1 | 1 | (2, 1) | +1 | 0 | yes | (2, 1) | 1 |
| 1 | 2 | (0, 2) | +1 | 3 | no | (2, 1) | 1 |
| 1 | 3 | (-1, 0) | -1 | -1 | no | (2, 1) | 1 |
| 1 | 4 | (1, -2) | -1 | 1 | yes | (1, 3) | 0 |
| 1 | 5 | (-2, 1) | -1 | 1 | yes | (3, 2) | -1 |
| 1 | 6 | (3, 3) | +1 | 14 | no | (3, 2) | -1 |
| 2 | 1 to 6 | | | 7, 3, -4, -2, -5, 14 | none | (3, 2) | -1 |

The second epoch has no mistake, so the output is $w = (3, 2)$ and $b = -1$, after 3 mistakes. For the bound: the augmented points $(x_i, 1)$ have $R'^2 = 18 + 1 = 19$, from $x_6$. The unit vector $(2, 2, -1)/3$ gives each example an augmented margin of at least $1$ (the examples 2 to 5 have exactly 1). So the theorem allows at most $19/1^2 = 19$ mistakes, and the run makes 3.

On XOR, the points $(0, 0)$ and $(1, 1)$ with $y = -1$ and $(1, 0)$ and $(0, 1)$ with $y = +1$, no separator exists. In this order, the first epoch makes 3 mistakes and each later epoch makes 4. Every epoch ends at the same state $w = (1, 1)$, $b = 1$, so the algorithm cycles forever. Line L10 is the only exit.

## Correctness

If PERCEPTRON returns at line L9, the output separates $S$: a pass with no mistake leaves $(w, b)$ fixed, and in that pass each example passed the test $y_i (w \cdot x_i + b) > 0$ with this fixed pair. If $S$ is linearly separable with margin $\gamma$ for the augmented points, the [perceptron convergence theorem](/perceptron-convergence-theorem/) bounds the total number of updates by $M = (R'/\gamma)^2$, where $R'$ is the largest norm of an augmented point. Each epoch that does not return makes at least one update, so at most $M$ epochs fail, and epoch $M + 1$ or an earlier one returns at line L9 when $T > M$. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/): each arithmetic operation on a real number costs 1.

- **One epoch.** Line L5 costs $\Theta(d)$ for the dot product, and an update costs $\Theta(d)$. So one epoch costs $\Theta(n d)$.
- **Separable data, worst case.** Let $m \le (R'/\gamma)^2$ be the number of mistakes. At most $m$ epochs have a mistake, and one more epoch confirms. So the time is $O((m + 1) n d)$. The bound on $m$ does not depend on $n$ or $d$.
- **Best case.** The first example is always a mistake, so at least two epochs run when $n \ge 1$, and the time is $\Theta(n d)$.
- **Data that is not separable.** The loop runs all $T$ epochs, in time $\Theta(T n d)$.
- **Space.** $\Theta(d)$ for $w$ and $b$, besides the input. The online form keeps only $w$ and $b$ and reads each example once.

The bound $(R/\gamma)^2$ is a worst case over all orders of the examples. On random data it is often loose. In the seeded test of the implementation (200 points in $[-1, 1]^5$, labelled by a random unit vector, kept at margin at least 0.1, seed 7), the five runs had bounds between 320 and 365 and made between 3 and 34 mistakes.

## Properties

- **Mistake driven.** The state changes only on a mistake. So $w = \sum_i a_i y_i x_i$, where $a_i$ is the number of mistakes on example $i$. This is the dual form that the kernel perceptron uses.
- **Scale free.** A learning rate $\eta > 0$ in lines L6 and L7 multiplies $w$ and $b$ by $\eta$ at every step, so it changes no prediction when $w$ starts at 0.
- **Not a maximum margin method.** The output is some separator, often close to a training point. The [support vector machine](/support-vector-machine/) finds the separator with the largest margin.
- **Order dependent.** Different orders of the examples give different outputs.
- **Bounded weights.** On any data, separable or not, the weights stay in a bounded set (the perceptron cycling theorem). The run does not diverge, but it does not settle either.

## Variants and improvements

- **Kernel (dual) perceptron.** Keep the counts $a_i$ instead of $w$, and predict with $f(x) = \sum_j a_j y_j (k(x_j, x) + 1)$. With a [kernel](/kernel-trick/) such as $k(x, z) = (x \cdot z + 1)^2$, this learns XOR. One prediction costs $n$ kernel evaluations.
- **Voted perceptron.** Freund and Schapire (1999) keep every intermediate vector $w_t$ with the number of examples $c_t$ that it survived, and predict by a vote of $\operatorname{sign}(w_t \cdot x)$ with weights $c_t$. They prove a generalization bound for it from the mistake bound.
- **Averaged perceptron.** Predict with the mean $\bar w = \frac{1}{N}\sum_t w_t$ of the vectors after each of the $N$ steps. It is a cheap approximation of the voted perceptron and is common in practice.
- **Margin perceptron.** Update when $y_i (w \cdot x_i + b) \le \tau$ for a $\tau > 0$. The output then has a positive margin on the training set.
- **The perceptron as a gradient method.** Line L5 to line L7 is a step of [stochastic gradient descent](/stochastic-gradient-descent/) with rate 1 on the loss $\max(0, -y (w \cdot x + b))$. The [hinge loss](/hinge-loss/) $\max(0, 1 - y(w \cdot x + b))$ gives the margin perceptron and, with a regularizer, the linear SVM.
- **Multiplicative updates.** [Winnow](/winnow/) multiplies weights instead of adding to them, and makes far fewer mistakes when only a few of many features matter.

## When to use it

Use the perceptron as a fast online baseline, as the inner step of structured prediction (the structured perceptron), or when the data arrives as a stream and the memory is small. Use the averaged form, not the last vector, for prediction. When the classes overlap, or when you need a probability or a large margin, use [logistic regression](/logistic-regression/) or a [support vector machine](/support-vector-machine/) instead.

## Pitfalls

- **The test $< 0$ in line L5.** With $w = 0$ at the start, $y_i (w \cdot x_i + b) = 0$ for each example, so the test $< 0$ never fires and the algorithm returns $w = 0$. Use $\le 0$.
- **No bias.** Without line L7 the hyperplane passes through the origin. Data that a hyperplane with an offset separates may then not be separable, and the run cycles.
- **The bias feature scale.** A constant feature $c$ much smaller than the data norm makes the bias learn slowly, and a large $c$ increases $R'$ and the mistake bound. The value $c = R$ gives the bound $(2R/\gamma)^2$.
- **Waiting for convergence on real data.** Overlapping classes make the loop run until $T$. Always set $T$, and keep the averaged vector.
- **Returning the last vector of a cycling run.** On data that is not separable, the last $w$ depends on where the cycle stops. The averaged or voted vector is more stable.

## Implementations

## History

Frank Rosenblatt introduced the perceptron in 1958 as a model of learning in the brain, and built the Mark I Perceptron machine. In 1962, Novikoff and Block independently proved that the error correction rule stops on separable data, with the bound $(R/\gamma)^2$. Minsky and Papert's book Perceptrons (1969) studied which functions single layer perceptrons can compute, with XOR and parity as examples that they cannot. Freund and Schapire (1999) brought the algorithm back with the voted perceptron and the kernel form.

## References
