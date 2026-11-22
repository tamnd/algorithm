---
tag: NXW2EA
kind: problem
slug: neural-network-verification-problem
name: Neural network verification
aliases:
- robustness verification
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: "Decide whether a network's output satisfies a property, such as a fixed label, for every input in a given region."
history:
  year: 2017
  people: [Guy Katz, Clark Barrett, David Dill, Kyle Julian, Mykel Kochenderfer]
  note: Katz et al. (CAV 2017) proved that the problem is NP-complete for ReLU networks with linear constraints and gave Reluplex, which checked properties of the ACAS Xu collision avoidance networks.
prereqs: [relu, adversarial-example, simplex-method]
see_also: [reluplex, interval-bound-propagation, linear-bound-propagation, randomized-smoothing, mixed-integer-programming, smt-problem, pgd-attack, abstract-interpretation]
sources:
  - url: https://arxiv.org/abs/1702.01135
    title: Guy Katz, Clark Barrett, David Dill, Kyle Julian and Mykel Kochenderfer, Reluplex, an efficient SMT solver for verifying deep neural networks, CAV 2017, LNCS 10426, pages 97 to 117
    locator: the statement of the verification problem, the proof that it is NP-complete, and the ACAS Xu case study
  - url: https://proceedings.mlr.press/v80/weng18a.html
    title: Tsui-Wei Weng, Huan Zhang, Hongge Chen, Zhao Song, Cho-Jui Hsieh, Duane Boning, Inderjit Dhillon and Luca Daniel, Towards fast computation of certified robustness for ReLU networks, ICML 2018, PMLR 80, pages 5276 to 5285
    locator: the result that no polynomial algorithm approximates the minimum l1 adversarial distortion within a 0.99 ln n factor unless P = NP, and the Fast-Lin bounds
  - url: https://proceedings.mlr.press/v80/wong18a.html
    title: Eric Wong and J. Zico Kolter, Provable defenses against adversarial examples via the convex outer adversarial polytope, ICML 2018, PMLR 80, pages 5286 to 5295
    locator: the linear relaxation of the ReLU and the dual bound on the worst-case margin
  - url: https://arxiv.org/abs/1810.12715
    title: Sven Gowal, Krishnamurthy Dvijotham, Robert Stanforth, Rudy Bunel, Chongli Qin, Jonathan Uesato, Relja Arandjelovic, Timothy Mann and Pushmeet Kohli, On the effectiveness of interval bound propagation for training verifiably robust models, arXiv 2018
    locator: interval bounds as a verifier and as a training loss
  - url: https://proceedings.mlr.press/v97/cohen19c.html
    title: Jeremy Cohen, Elan Rosenfeld and J. Zico Kolter, Certified adversarial robustness via randomized smoothing, ICML 2019, PMLR 97, pages 1310 to 1320
    locator: a probabilistic certificate for a smoothed classifier in place of a certificate for the network itself
  - url: https://arxiv.org/abs/1902.06705
    title: Nicholas Carlini, Anish Athalye, Nicolas Papernot, Wieland Brendel, Jonas Rauber, Dimitris Tsipras, Ian Goodfellow, Aleksander Madry and Alexey Kurakin, On evaluating adversarial robustness, arXiv 2019
    locator: verified accuracy as a lower bound and attack accuracy as an upper bound on robust accuracy
---

The neural network verification problem asks whether a trained network $f$ maps every input of a region $X$ into a set $Y$ of allowed outputs. The usual instance is local robustness: $X = B_\infty(x, \epsilon) \cap [0, 1]^d$ around a test input $x$ with label $y$, and $Y$ is the set of logit vectors whose largest entry is $z_y$. A "yes" answer is a certificate: no [adversarial example](/adversarial-example/) exists in $X$. A "no" answer comes with a counterexample, an input in $X$ whose output is outside $Y$. Katz et al. (2017) proved that the problem is NP-complete for networks with ReLU activations and properties given by linear constraints. Methods are therefore exact but exponential in the worst case, such as [Reluplex](/reluplex/) and [mixed integer programming](/mixed-integer-programming/), or fast but incomplete, such as [interval bound propagation](/interval-bound-propagation/) and [linear bound propagation](/linear-bound-propagation/), which may answer "unknown".

**Notation.** The network has $L$ affine layers $W_\ell v + b_\ell$ with a ReLU after every layer except the last, and the output is the logit vector $z(x) \in \mathbb{R}^K$. $R$ is the number of ReLU units, the margin is $m(x) = \min_{j \ne y} (z_y(x) - z_j(x))$, and $\epsilon$ is the radius of the input region.

## In plain words

A test can show that a network gives the right answer on many inputs. Verification asks for more: a proof that the answer is right on every input in a whole region, such as all images that differ from a given image by at most a small amount in each pixel.

There are infinitely many inputs in the region, so the proof cannot try them one by one. It must reason about the network as a formula. For ReLU networks, the hard part is that each unit can be on or off, and the number of on and off patterns grows exponentially. Exact methods search these patterns. Fast methods replace each unit by a simple shape that contains it, and may then fail to prove a true property.

## Definition

**Input.** A network $f : \mathbb{R}^d \to \mathbb{R}^K$ made of affine layers and ReLU units, an input region $X$ given by linear constraints (a box or a polytope), and an output property $Y$ given by linear constraints on $z$.

**Output.** "Holds" if $f(x) \in Y$ for every $x \in X$; otherwise "violated", with a witness $x \in X$ such that $f(x) \notin Y$.

**Adversary.** The property is a statement about the worst case: the region $X$ is the set of inputs that an adversary can reach, for example a test-time change $\eta$ with $\lVert \eta \rVert_\infty \le \epsilon$ that keeps $x + \eta$ in $[0, 1]^d$. The verifier has the full network, so the answer holds against any adversary with that capability, whatever it knows.

**Optimization form.** For local robustness the property holds if and only if $\min_{x' \in X} m(x') > 0$. An exact method computes this minimum or decides its sign; a sound but incomplete method computes a lower bound $\underline m \le \min_{x' \in X} m(x')$ and answers "holds" only if $\underline m > 0$.

The answer of a sound verifier on a test set gives a lower bound on the robust accuracy, and the answer of an attack such as [PGD](/pgd-attack/) gives an upper bound; the true robust accuracy lies between them.

## Variants

- **Local robustness in other norms.** $X = B_2(x, \epsilon)$ or $B_1(x, \epsilon)$ intersected with $[0,1]^d$. The $\ell_2$ ball is not a polytope, so exact methods need quadratic constraints or a polytope that contains it.
- **Certified radius.** Find the largest $\epsilon$ for which the property holds. Bisection over $\epsilon$ with a sound verifier gives a lower bound on it, and an attack gives an upper bound.
- **Safety properties.** $X$ and $Y$ describe a region of operation and an unsafe output, such as the ACAS Xu properties that Katz et al. checked: for inputs in a region of sensor values, the network never advises a given manoeuvre.
- **Other activations.** Max pooling and other piecewise linear units fit the same framework. Sigmoid and tanh units need bounds by linear functions, and exact answers are then much harder.
- **Probabilistic versions.** Ask that the property holds for a random input with high probability, or certify a [smoothed classifier](/randomized-smoothing/) built from the network in place of the network itself.
- **Global properties.** Ask for a property for every input $x$, not only near one point, such as a bound on how fast the output can change. These need different methods.

## Examples

Take the network with two inputs, two ReLU units and two logits, $W_1 = \begin{pmatrix} 2 & -1 \\ 1 & -2 \end{pmatrix}$, $b_1 = (0, 0.5)$, $W_2 = \begin{pmatrix} 1 & -1 \\ -2 & 2 \end{pmatrix}$, $b_2 = (1, 0)$. At $x = (0.5, 0.5)$ the hidden layer is $(0.5, 0)$, the logits are $z = (1.5, -1)$, and the label is $y = 0$. The margin is $m(x') = z_0 - z_1 = 3 h_1 - 3 h_2 + 1$, where $h_1, h_2$ are the outputs of the two ReLU units.

| question at $\epsilon = 1/4$ | answer |
|---|---|
| exact minimum of $m$ over $B_\infty(x, 1/4)$ | $1$, so the property holds |
| lower bound by interval bound propagation | $-1.25$, so the answer is "unknown" |
| lower bound by linear bound propagation (CROWN) | $0.25$, so the property is proved |
| exact search by Reluplex over the four on and off patterns | all four are infeasible, so the property holds |

The certified radius tells the methods apart in the same way: intervals certify $\epsilon = 5/36$, linear bounds $5/18$, and the exact radius is $5/12$. At $\epsilon = 5/12$ the corner $x' = (1/12, 1/12)$ gives the logits $(2/3, 2/3)$, a tie, which is the counterexample that an exact method returns for any $\epsilon \ge 5/12$.

## Known algorithms

- **Exact by SMT.** [Reluplex](/reluplex/) extends the [simplex method](/simplex-method/) with ReLU constraints and splits a unit only when needed (Katz et al. 2017). Later solvers of the same family add bound tightening and parallel search.
- **Exact by mixed integer programming.** Encode each unstable ReLU with one binary variable and big-M constraints, and solve with a [mixed integer programming](/mixed-integer-programming/) solver. Tight bounds on each unit, found first by a cheap method, make the encoding much faster.
- **Interval bound propagation.** Propagate a box through each layer with [interval arithmetic](/interval-arithmetic/). It costs about two forward passes but loses precision fast in deep networks. Gowal et al. (2018) showed it works well when the network is trained for it.
- **Linear bound propagation.** Bound each ReLU between two linear functions and propagate linear bounds backward (Wong and Kolter 2018, Weng et al. 2018, Zhang et al. 2018). Tighter than intervals at a cost of about one backward pass per layer.
- **Branch and bound.** Split unstable units into their two cases and bound each case with linear bounds; this is complete in the limit and is the basis of the strongest current verifiers.
- **Abstract interpretation.** Push an abstract domain, such as boxes, zonotopes or polyhedra, through the network; this is the framework of [abstract interpretation](/abstract-interpretation/), and the methods above are instances of it.
- **Randomized smoothing.** Certify a smoothed version of the network with high probability, at any scale (Cohen et al. 2019). This answers a different question.

## Bounds

- **NP-complete.** The problem with ReLU units and linear constraints on input and output is NP-complete (Katz et al. 2017). It is in NP: a witness $x$ is checked by one forward pass. It is NP-hard by a reduction from [3-SAT](/3-sat/).
- **Exact cost.** If $R$ units are unstable on $X$, an exact method can try all $2^R$ on and off patterns, each one a linear program solved in polynomial time, so the cost is $O(2^R \mathrm{poly}(s))$ for a network of size $s$. A polynomial algorithm exists only if P = NP.
- **Hard to approximate.** No polynomial algorithm can approximate the minimum $\ell_1$ adversarial distortion of a ReLU network within a factor $0.99 \ln n$, where $n$ is the number of neurons, unless P = NP (Weng et al. 2018).
- **Incomplete methods.** Interval and linear bounds run in polynomial time, so by the result above they must fail to prove some true properties. The gap between their bound and the exact minimum can grow with the depth.

## Reductions

- **From 3-SAT.** Katz et al. encode each Boolean variable as an input in $[0, 1]$, use ReLU units to force the values to 0 or 1 at a counterexample and to compute the clauses, and ask for an input whose output shows that all clauses hold. A formula is satisfiable if and only if the property is violated.
- **To linear programming with case splits.** Fixing the on and off state of each ReLU makes every unit linear, so the problem is a union of $2^R$ linear programs; this is the basis of Reluplex and of branch and bound.
- **To mixed integer programming.** With a known bound $|v| \le M$ on each pre-activation, the constraint $h = \max(v, 0)$ is equivalent to linear constraints with one binary variable.
- **To satisfiability modulo theories.** The negated property, the network and the region together form a formula of linear real arithmetic with ReLU constraints, an instance of the [SMT problem](/smt-problem/).

## Applications

- **Certified robust accuracy.** Reporting the fraction of test inputs whose robustness is verified gives a guaranteed lower bound on robust accuracy, which is the standard of evidence for a defense (Carlini et al. 2019).
- **Certified training.** Training with the bound of a fast verifier as the loss, as with interval bound propagation, gives networks that are easy to verify.
- **Safety of control networks.** Proving input and output properties of networks used in control, such as the ACAS Xu collision avoidance networks.
- **Evaluating defenses.** An exact verifier can find the true minimum distortion on small networks and so check whether an attack used in an evaluation is strong enough.

## References
