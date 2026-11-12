---
tag: 8TYE96
kind: theorem
slug: perceptron-convergence-theorem
name: Perceptron convergence theorem
aliases:
- Novikoff's theorem
- Block-Novikoff theorem
- perceptron mistake bound
area: machine-learning/supervised-learning
level: core
summary: "If each example has norm at most R and a unit vector separates them with margin γ, the perceptron makes at most (R/γ)^2 mistakes, in any order."
prereqs: [perceptron, linear-separability]
see_also: [perceptron, winnow, margin-generalization-bound, support-vector-machine, kernel-trick, halfspace-learning]
sources:
  - paper: "A. B. J. Novikoff, On convergence proofs on perceptrons, Proceedings of the Symposium on the Mathematical Theory of Automata, Volume 12, Polytechnic Institute of Brooklyn, 1962"
    locator: the theorem that the number of corrections is at most (R/γ)^2, and its proof
  - paper: doi:10.1103/RevModPhys.34.123
    title: H. D. Block, The perceptron, a model for brain functioning. I, Reviews of Modern Physics 34(1), 1962
    locator: pp. 123 to 135 (the convergence theorem for the error correction procedure)
  - paper: doi:10.1023/A:1007662407062
    title: Yoav Freund and Robert E. Schapire, Large margin classification using the perceptron algorithm, Machine Learning 37(3), 1999
    locator: the statement of the Block-Novikoff bound and its extension to data that is not separable
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Section 9.1.2 (the perceptron for halfspaces and its mistake bound)
  - book: isbn:9780262039406
    title: Mehryar Mohri, Afshin Rostamizadeh and Ameet Talwalkar, Foundations of Machine Learning, second edition, MIT Press, 2018
    locator: Chapter 8, On-line learning (the perceptron algorithm, its mistake bound and the dual form)
---

The perceptron convergence theorem bounds the number of mistakes of the [perceptron](/perceptron/). If every example has norm at most $R$, and some unit vector puts every example on its correct side with margin at least $\gamma > 0$, then the perceptron makes at most $(R/\gamma)^2$ mistakes, whatever the order of the examples and however long the sequence. Novikoff and Block proved it in 1962. The bound is the best possible for any deterministic online learner.

## Statement

Let $(x_1, y_1), (x_2, y_2), \ldots$ be a finite or infinite sequence with $x_t \in \mathbb{R}^d$ and $y_t \in \{-1, +1\}$. The perceptron through the origin starts with $w_1 = 0$. At step $t$ it makes a mistake if $y_t\, w_t \cdot x_t \le 0$, and then sets $w_{t+1} = w_t + y_t x_t$; otherwise $w_{t+1} = w_t$.

**Theorem (Block 1962, Novikoff 1962).** Assume that

1. $\lVert x_t \rVert \le R$ for each $t$, and
2. there are a vector $u \in \mathbb{R}^d$ with $\lVert u \rVert = 1$ and a number $\gamma > 0$ such that $y_t\, u \cdot x_t \ge \gamma$ for each $t$.

Then the number of mistakes is at most $(R/\gamma)^2$.

The data model is the realizable online model: no distribution is assumed, the sequence may be chosen by an adversary, and the bound is a worst case over all such sequences. The norm is the Euclidean norm.

**With a bias.** Suppose instead that $y_t (u \cdot x_t + b) \ge \gamma$ with $\lVert u \rVert = 1$, and the perceptron learns $(w, b)$ by the augmentation $x \mapsto (x, c)$ with a constant $c > 0$. The augmented points have norm at most $\sqrt{R^2 + c^2}$, and the unit vector $(u, b/c)/\sqrt{1 + b^2/c^2}$ has margin at least $\gamma / \sqrt{1 + b^2/c^2}$ on them. So the theorem gives at most

$$\frac{(R^2 + c^2)(1 + b^2/c^2)}{\gamma^2}$$

mistakes. With $c = 1$ this is $(R^2 + 1)(1 + b^2)/\gamma^2$. The choice $c^2 = R\lvert b \rvert$ minimizes it, to $(R + \lvert b \rvert)^2/\gamma^2$. When both labels occur, $\lvert b \rvert < R$, because the hyperplane $u \cdot x + b = 0$ must cut the ball of radius $R$ that holds the points, so $c = R$ gives at most $2(R^2 + b^2)/\gamma^2 \le (2R/\gamma)^2$.

## In plain words

Picture a separating direction that gives every example a clear gap. Each mistake of the perceptron does two things. It moves the weight vector a fixed amount further along the good direction, because the gap is at least some fixed size. It also makes the weight vector longer, but only slowly, because the example was on the wrong side, so the update does not point along the old weights. The progress along the good direction grows like the number of mistakes, while the length grows only like its square root. The progress can never be larger than the length, so the number of mistakes must stop. Large examples allow more mistakes, and a wide gap allows fewer.

## Proof

Let $w^{(k)}$ be the weight vector after the $k$-th mistake, with $w^{(0)} = 0$. The weights change only at a mistake, so it suffices to study $w^{(0)}, w^{(1)}, \ldots$. Let the $k$-th mistake be on the example $(x, y)$. Then $y\, w^{(k-1)} \cdot x \le 0$ and $w^{(k)} = w^{(k-1)} + y x$.

**Step 1: progress along $u$.** By hypothesis 2,

$$u \cdot w^{(k)} = u \cdot w^{(k-1)} + y\, u \cdot x \ge u \cdot w^{(k-1)} + \gamma.$$

From $u \cdot w^{(0)} = 0$, induction on $k$ gives $u \cdot w^{(k)} \ge k\gamma$.

**Step 2: slow growth of the norm.** Expand the square:

$$\lVert w^{(k)} \rVert^2 = \lVert w^{(k-1)} \rVert^2 + 2 y\, w^{(k-1)} \cdot x + y^2 \lVert x \rVert^2 \le \lVert w^{(k-1)} \rVert^2 + R^2.$$

The middle term is at most 0 because the step is a mistake, $y^2 = 1$, and $\lVert x \rVert \le R$ by hypothesis 1. From $\lVert w^{(0)} \rVert = 0$, induction gives $\lVert w^{(k)} \rVert^2 \le k R^2$.

**Step 3: combine.** By the Cauchy-Schwarz inequality and $\lVert u \rVert = 1$,

$$k\gamma \le u \cdot w^{(k)} \le \lVert u \rVert\, \lVert w^{(k)} \rVert \le \sqrt{k}\, R.$$

For $k \ge 1$, divide by $\sqrt{k}\,\gamma > 0$ and square: $k \le R^2/\gamma^2$. So a $k$-th mistake can exist only for $k \le (R/\gamma)^2$, and the number of mistakes is at most $(R/\gamma)^2$. $\blacksquare$

The proof uses neither the order of the examples nor their number. It also holds for any learning rate $\eta > 0$ in the update $w \leftarrow w + \eta y x$ from $w = 0$, because then every $w^{(k)}$ is $\eta$ times the vector of the rate 1 run, and the signs of all tests are the same.

## Consequences

- **Termination of the batch perceptron.** On a finite [linearly separable](/linear-separability/) training set, the [perceptron](/perceptron/) passes over the data until a pass has no mistake. Each failed pass has a mistake, so it stops after at most $(R/\gamma)^2 + 1$ passes, and its output separates the data.
- **Dimension free.** The bound does not contain $d$ or $n$. So it also holds in a feature space of very large or infinite dimension. The kernel perceptron with a [kernel](/kernel-trick/) $k$ makes at most $(R/\gamma)^2$ mistakes, with $R^2 = \max_t k(x_t, x_t)$ and $\gamma$ the margin in the feature space.
- **Generalization.** Freund and Schapire (1999) turn the mistake bound into a bound on the expected error of the voted perceptron on i.i.d. data. The [margin generalization bound](/margin-generalization-bound/) is the batch counterpart: the quantity $(R/\gamma)^2$ there plays the role of the VC dimension.
- **Data that is not separable.** Freund and Schapire (1999) also bound the mistakes when no separator exists, by $\left((R + D)/\gamma\right)^2$, where $D$ is the Euclidean norm of the vector of hinge deviations $\max(0, \gamma - y_t\, u \cdot x_t)$ for a fixed $u$ and $\gamma$.
- **Linear feasibility.** A system $A z > 0$ is a separable data set with $y = +1$. The perceptron finds a solution with at most $(R/\gamma)^2$ updates, which is fast when the system is well conditioned and slow when $\gamma$ is tiny.

The seeded test of the implementation runs the perceptron on 10 random streams of 20000 examples drawn from 100 separable points in $[-1, 1]^6$ (seed 2024). The bounds were between 895 and 1643, and the runs made between 14 and 88 mistakes. On random data the bound is far from tight.

## Tightness

The bound is exact for the perceptron, and no deterministic online learner can do better in the worst case.

**The perceptron.** Let $m \ge 1$ and $d = m$, and feed the unit vectors $e_1, \ldots, e_m$, each with label $+1$. Then $R = 1$, and $u = (1, \ldots, 1)/\sqrt{m}$ has margin $\gamma = 1/\sqrt{m}$, so $(R/\gamma)^2 = m$. Before the $i$-th example the weights are $e_1 + \cdots + e_{i-1}$, which is orthogonal to $e_i$, so the test $y\, w \cdot x \le 0$ fires. The perceptron makes exactly $m$ mistakes.

**Any deterministic learner.** Feed $e_1, \ldots, e_m$ again, but let the adversary choose each label $y_i$ as the opposite of the learner's prediction on $e_i$. The learner then makes $m$ mistakes. The labels are separable by $u = (y_1, \ldots, y_m)/\sqrt{m}$, with margin $1/\sqrt{m}$ and $R = 1$. So for each integer $m \le d$, some sequence with $(R/\gamma)^2 = m$ forces $m$ mistakes on every deterministic learner.

## History

Rosenblatt (1958) proposed the perceptron and its error correction rule. In 1962 H. D. Block, in Reviews of Modern Physics, and A. B. J. Novikoff, at a symposium on the theory of automata, proved that the rule stops on separable data. Novikoff's short proof by the two inequalities of Steps 1 and 2 is the one in today's textbooks. Freund and Schapire (1999) used the bound to analyze the voted and the kernel perceptron and extended it to data that is not separable.

## References
