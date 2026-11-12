---
tag: ETYSJD
kind: algorithm
slug: winnow
name: Winnow algorithm
aliases:
- Winnow
- WINNOW1
- WINNOW2
- Littlestone's Winnow
area: machine-learning/supervised-learning
level: advanced
summary: Online learner of a linear threshold over Boolean features with multiplicative updates. It learns a k-literal monotone disjunction with O(k log n) mistakes.
solves: [halfspace-learning]
model: real-ram
complexity:
  vars: {n: the number of Boolean features, k: the number of relevant variables of the target disjunction, t: the number of examples}
  time: {worst: Θ(t n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: true, exact: true, recursive: false}
history:
  year: 1988
  people: [Nick Littlestone]
  note: Littlestone introduced WINNOW1 and WINNOW2 and the mistake bound model in Machine Learning in 1988.
prereqs: [perceptron, multiplicative-weights-update]
see_also: [perceptron, perceptron-convergence-theorem, weighted-majority, multiplicative-weights-update, halfspace-learning, vc-dimension, regret]
sources:
  - paper: doi:10.1007/BF00116827
    title: Nick Littlestone, Learning quickly when irrelevant attributes abound, a new linear-threshold algorithm, Machine Learning 2(4), 1988
    locator: pp. 285 to 318; Section 5 (WINNOW1, its Theorem 7 bound for k-literal monotone disjunctions, and the Theorem 8 lower bound) and the sections on WINNOW2
  - paper: "Jyrki Kivinen, Manfred K. Warmuth and Peter Auer, The perceptron algorithm versus Winnow, linear versus logarithmic mistake bounds when few input variables are relevant, Artificial Intelligence 97(1-2), 1997"
    locator: the comparison of additive and multiplicative updates on sparse targets
  - book: isbn:9780262039406
    title: Mehryar Mohri, Afshin Rostamizadeh and Ameet Talwalkar, Foundations of Machine Learning, second edition, MIT Press, 2018
    locator: Chapter 8, On-line learning (the Winnow algorithm and its mistake bound)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Chapter 21 (online learning, mistake bounds and the Littlestone dimension)
---

Winnow is an online algorithm of Littlestone (1988) that learns a linear threshold function over Boolean features with multiplicative weight updates. On a mistake it multiplies the weights of the active features by a factor $\alpha > 1$, or sets them to zero (WINNOW1) or divides them by $\alpha$ (WINNOW2). For a target that is a disjunction of $k$ of the $n$ variables, WINNOW1 makes at most $\alpha k(\log_\alpha \theta + 1) + n/\theta$ mistakes, which is $2k\log_2 n + 2$ for $\alpha = 2$ and $\theta = n/2$. The bound grows only with the logarithm of $n$, so Winnow learns well when most features are irrelevant.

## In plain words

Each feature has a weight, and all weights start at one. The learner says yes when the total weight of the features that are on is above a threshold. When it says no but the answer was yes, it doubles the weights of the features that are on: some of them must matter. When it says yes but the answer was no, the features that are on cannot be in the target, so their weights become zero.

A useful feature only needs to be doubled a few times before its weight alone passes the threshold. So the learner makes few mistakes on the yes examples. Each wrong yes throws away a lot of weight, and the total weight was small at the start, so wrong yes answers are few too.

## The problem

Examples are $x \in \{0, 1\}^n$ with labels $y \in \{0, 1\}$. The target is a monotone disjunction $f(x) = x_{i_1} \lor \cdots \lor x_{i_k}$ of $k$ of the $n$ variables, unknown to the learner, and $y = f(x)$. The examples come one at a time in any order, possibly chosen by an adversary. The learner predicts $\hat y$, then sees $y$. The cost is the number of mistakes, $\hat y \ne y$. This is the realizable mistake bound model, a special case of online [halfspace learning](/halfspace-learning/): $f(x) = 1$ exactly when $\sum_{j} x_{i_j} \ge 1$.

## The algorithm

The parameters are the update factor $\alpha > 1$ and the threshold $\theta > 0$. This is WINNOW1.

```pseudo id=main
WINNOW1(n, α, θ)                         ▷ examples arrive one at a time
L1  w_i ← 1 for i = 1, ..., n
L2  for each example x ∈ {0,1}^n do
L3      ŷ ← 1 if Σ_i w_i x_i > θ, else ŷ ← 0      ▷ predict, then see y
L4      if ŷ = 0 and y = 1 then                      ▷ false negative
L5          w_i ← α w_i for each i with x_i = 1      ▷ promotion
L6      else if ŷ = 1 and y = 0 then                 ▷ false positive
L7          w_i ← 0 for each i with x_i = 1          ▷ elimination
L8      count a mistake if line L5 or L7 ran
```

Line L3 is a linear threshold with nonnegative weights. Line L5 multiplies only the weights of the active features. Line L7 uses the fact that the target is monotone: on a negative example every relevant variable is 0, so each active variable is irrelevant, and its weight can go to 0 for good.

**WINNOW2** replaces line L7 by a demotion $w_i \leftarrow w_i / \alpha$. It never sets a weight to zero, so it tolerates noise and it learns more general targets, for example "at least $r$ of these $k$ variables are 1". Littlestone proves a mistake bound for WINNOW2 on these threshold functions in terms of their separation margin. The constants on this page are those of WINNOW1.

## Example

Let $n = 8$, the target $f = x_1 \lor x_3$ (so $k = 2$), $\alpha = 2$ and $\theta = n/2 = 4$. The weights are written as $(w_1, \ldots, w_8)$.

| step | $x$ | $y$ | $\sum w_i x_i$ | $\hat y$ | action | weights after |
|---|---|---|---|---|---|---|
| 1 | 11001100 | 1 | 4 | 0 | promote 1, 2, 5, 6 | (2, 2, 1, 1, 2, 2, 1, 1) |
| 2 | 00011011 | 0 | 5 | 1 | eliminate 4, 5, 7, 8 | (2, 2, 1, 0, 0, 2, 0, 0) |
| 3 | 01100000 | 1 | 3 | 0 | promote 2, 3 | (2, 4, 2, 0, 0, 2, 0, 0) |
| 4 | 01010100 | 0 | 6 | 1 | eliminate 2, 4, 6 | (2, 0, 2, 0, 0, 0, 0, 0) |
| 5 | 10000000 | 1 | 2 | 0 | promote 1 | (4, 0, 2, 0, 0, 0, 0, 0) |
| 6 | 00100001 | 1 | 2 | 0 | promote 3, 8 | (4, 0, 4, 0, 0, 0, 0, 0) |
| 7 | 01001010 | 0 | 0 | 0 | none | same |
| 8 | 10000001 | 1 | 4 | 0 | promote 1, 8 | (8, 0, 4, 0, 0, 0, 0, 0) |

The run makes 7 mistakes in 8 steps. The bound is $2 \cdot 2 \cdot (\log_2 4 + 1) + 8/4 = 14$. The weight $w_8 = 0$ stays 0 when it is "promoted" at steps 6 and 8, because it was eliminated at step 2. At most one more mistake can follow: $w_3 = 4$ is not above $\theta$, and one promotion lifts it to 8.

## Correctness

**Theorem (Littlestone 1988, Theorem 7).** If the target is a monotone disjunction of $k$ variables, $\alpha > 1$ and $\theta \ge 1/\alpha$, then on any sequence of examples WINNOW1 makes at most $\alpha k (\log_\alpha \theta + 1) + n/\theta$ mistakes.

The proof counts the two kinds of mistakes. A relevant weight is never eliminated, and it is promoted only while it is at most $\theta$, so each of the $k$ relevant weights is promoted at most $\log_\alpha \theta + 1$ times, and each promotion mistake promotes at least one of them. The total weight starts at $n$, grows by less than $(\alpha - 1)\theta$ per promotion and drops by more than $\theta$ per elimination, and it never becomes negative. The full proof is below.

**Lower bound.** Littlestone also shows (Theorem 8) that every deterministic online learner can be forced to make at least $k \lfloor \log_2(n/k) \rfloor$ mistakes on this class. So WINNOW1 with $\alpha = 2$ is optimal up to a constant factor.

## Complexity

The model is the [real RAM](/real-ram/).

- **Per example.** Line L3 and the update each touch the $n$ weights, so $\Theta(n)$ time. With a sparse example that has $s$ ones, both cost $O(s)$.
- **Total.** $\Theta(t n)$ time for $t$ examples, and $\Theta(n)$ memory for the weights.
- **Mistakes.** At most $\alpha k(\log_\alpha \theta + 1) + n/\theta$ in the worst case over all sequences. With $\alpha = 2$ and $\theta = n/2$ it is $2k\log_2 n + 2$, and with $\theta = n$ it is $2k(\log_2 n + 1) + 1$.
- **Weights.** Each weight is 0 or a power of $\alpha$ at most $\alpha\theta$, so the numbers stay small. With $\alpha = 2$ they are exact integers.

In the seeded tests (3000 random examples per target, $\alpha = 2$, $\theta = n/2$), the runs made 6 mistakes for $n = 16, k = 1$ (bound 10), 11 for $n = 64, k = 2$ (bound 26), 27 for $n = 128, k = 4$ (bound 58) and 8 for $n = 256, k = 1$ (bound 18).

## Properties

- **Attribute efficient.** The number of mistakes grows with $k \log n$, not with $n$. The [perceptron](/perceptron/) on the same targets can be forced into a number of mistakes that grows linearly in $n$ (Kivinen, Warmuth and Auer 1997).
- **Mistake driven and online.** The state changes only on a mistake, and each example is read once.
- **Nonnegative weights.** Winnow represents only targets with nonnegative weights. A non-monotone disjunction is handled by doubling the features to $(x, 1 - x)$, which doubles $n$. With $\alpha = 2$ and $\theta = n/2$ the bound $2k\log_2 n + 2$ grows by $2k$.
- **Multiplicative.** The update is a step of the [multiplicative weights update](/multiplicative-weights-update/) method, the same family as [weighted majority](/weighted-majority/). Additive updates such as the perceptron's fit dense targets, and multiplicative updates fit sparse ones.

## Variants and improvements

- **WINNOW2.** Demote by $\alpha$ instead of eliminating. It learns $r$-of-$k$ threshold functions and, more generally, linear threshold functions with a positive margin, and it degrades gracefully with noisy labels.
- **Balanced Winnow.** Keep two weight vectors $w^+$ and $w^-$ and predict with $w^+ - w^-$. This allows negative weights.
- **Exponentiated gradient.** Kivinen and Warmuth's EG algorithm uses the same multiplicative idea for regression with a normalized weight vector.
- **Learning other classes.** By a change of features, Winnow learns $k$-term DNF and other classes with a bound that depends on the logarithm of the number of features.

## When to use it

Use Winnow when the examples are sparse Boolean vectors with very many features, of which only a few matter, as in text classification with word features. Use the [perceptron](/perceptron/) or a [support vector machine](/support-vector-machine/) when many features carry a little weight each. Use WINNOW2 rather than WINNOW1 on real data, because a single wrong negative label can eliminate a relevant weight in WINNOW1 forever.

## Pitfalls

- **Elimination on noisy data.** In line L7 a mislabelled negative example sets relevant weights to 0, and no later promotion can lift them. The example has no noise, but it shows the mechanism: $w_8$ stays at 0 through the promotions of steps 6 and 8. There $x_8$ is irrelevant, so no harm is done; a relevant variable would be lost in the same way. Use WINNOW2 if labels can be wrong.
- **A threshold that is too small.** With $\theta < 1/\alpha$ the theorem does not apply. With $\theta = 1$, each single active feature already passes the threshold, and the $n/\theta$ term of the bound becomes $n$. Use $\theta$ of order $n$.
- **Non-monotone targets.** Line L7 is sound only when the target is monotone. For a target with negated literals, add the complemented features first.
- **Comparing $\ge$ and $>$ in line L3.** Both conventions give the same bound, but the traces differ. The test with $>$ is Littlestone's.

## Implementations

## History

Nick Littlestone introduced Winnow in 1988, in the same paper that defined the mistake bound model and what is now called the Littlestone dimension. He gave WINNOW1 for monotone disjunctions with the bound of Theorem 7, the lower bound of Theorem 8, and WINNOW2 for linearly separable Boolean functions with a margin. Kivinen, Warmuth and Auer (1997) compared the additive perceptron and the multiplicative Winnow and showed the gap between linear and logarithmic dependence on the number of irrelevant features.

## References
