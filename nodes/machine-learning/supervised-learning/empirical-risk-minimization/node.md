---
tag: CNMDNK
kind: technique
slug: empirical-risk-minimization
name: Empirical risk minimization
aliases:
- ERM
- minimizing average training loss
- ERM rule
area: machine-learning/supervised-learning
level: core
summary: "Choose a hypothesis from a fixed class with the least mean loss on the training sample. It learns well when the class has uniform convergence, but the search can be NP-hard."
prereqs: [hypothesis-class]
see_also: [pac-learning, agnostic-pac-learning, structural-risk-minimization, regularization, overfitting, halfspace-learning, fundamental-theorem-of-statistical-learning, stochastic-gradient-descent]
sources:
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, From Theory to Algorithms, Cambridge University Press, 2014
    locator: Sections 2.2 and 2.3 (the ERM rule, overfitting, inductive bias), Lemma 4.2 (an epsilon/2-representative sample makes ERM good), Chapter 8 (Sections 8.2 to 8.4, the runtime of ERM)
  - book: isbn:9780387987804
    title: Vladimir N. Vapnik, The Nature of Statistical Learning Theory, second edition, Springer, 2000
    locator: Chapter 2 (consistency of the empirical risk minimization principle)
  - paper: doi:10.1145/1968.1972
    title: L. G. Valiant, A theory of the learnable, Communications of the ACM 27(11), 1984
    locator: pp. 1134 to 1142 (the elimination algorithm for conjunctions, which is an ERM rule in the realizable case)
  - paper: "S. Ben-David, N. Eiron and P. M. Long, On the difficulty of approximately maximizing agreements, Journal of Computer and System Sciences 66(3), 2003"
    locator: pp. 496 to 514 (NP-hardness of approximate agnostic ERM for halfspaces, axis aligned rectangles and other classes)
  - paper: "D. S. Johnson and F. P. Preparata, The densest hemisphere problem, Theoretical Computer Science 6(1), 1978"
    locator: pp. 93 to 107 (NP-hardness of finding a halfspace with the fewest disagreements)
---

Empirical risk minimization (ERM) is the rule that returns a hypothesis of a fixed [hypothesis class](/hypothesis-class/) $H$ with the least mean loss on the training sample. It is the basic learner of statistical learning theory: when $H$ has uniform convergence, for example a finite class or a binary class of finite [VC dimension](/vc-dimension/), ERM is a [PAC learner](/pac-learning/) and an [agnostic PAC learner](/agnostic-pac-learning/). Without a restriction on $H$ it fits the sample and fails on new points. Its statistical cost is set by $H$; its running time depends on how hard the minimization over $H$ is, and for halfspaces in the agnostic case it is NP-hard when the dimension is part of the input.

## In plain words

You have a list of candidate rules, chosen before you see any data. You also have a set of labeled examples. For each rule, count how often it is wrong on the examples. Return a rule with the smallest count. That is the whole method.

It works when the list is not too rich. Then a rule that does well on enough random examples also does well on new examples from the same source. It fails when the list is so rich that some rule fits any set of examples, for instance the rule that only remembers the examples. Such a rule is right on every example it saw and says nothing useful about the rest. The art is in the choice of the list and in a fast way to find its best member.

## When it applies

The setting is statistical learning. Examples $(x_i, y_i)$, $i = 1, \ldots, n$, are drawn i.i.d. from an unknown distribution $D$ on $X \times Y$. The class $H$ and the [loss](/loss-function/) $\ell$ are fixed before the sample. The true risk is $L_D(h) = \mathbb{E}_{D}[\ell(h(x), y)]$ and the empirical risk is $L_S(h) = \frac{1}{n} \sum_{i=1}^n \ell(h(x_i), y_i)$. ERM returns some $h_S \in \arg\min_{h \in H} L_S(h)$.

ERM is a good learner when $H$ has the **uniform convergence** property: for each $\varepsilon, \delta$ there is a sample size beyond which, with probability at least $1 - \delta$, $|L_S(h) - L_D(h)| \le \varepsilon$ for all $h \in H$ at the same time. Finite classes with a bounded loss have it, by [Hoeffding's inequality](/hoeffding-inequality/) and the [union bound](/union-bound/). For binary classification with the 0-1 loss, the [fundamental theorem of statistical learning](/fundamental-theorem-of-statistical-learning/) shows that uniform convergence holds exactly when the VC dimension is finite, and that then every ERM rule learns.

ERM is a practical algorithm only when the minimization over $H$ can be done: by enumeration for a small finite class, by a sweep for thresholds and intervals, by linear programming for halfspaces on separable data, and by convex optimization when the loss is convex in the parameters.

## The template

```pseudo id=main
ERM(H, S, ℓ)                                  ▷ H finite, S = ((x_1, y_1), …, (x_n, y_n))
L1  best ← none, r⋆ ← +∞
L2  for each h in H do
L3      r ← (1/n) · Σ_{i=1..n} ℓ(h(x_i), y_i)  ▷ the empirical risk L_S(h)
L4      if r < r⋆ then best ← h, r⋆ ← r       ▷ ties keep the first minimizer
L5  return best
```

This loop makes $|H| \cdot n$ loss evaluations. For a structured class, the loop over $H$ is replaced by a search that uses the structure. For thresholds $h_t(x) = 1[x \ge t]$ on the line under the 0-1 loss, only $n + 1$ thresholds give different label vectors on the sample, and a sweep finds the best one:

```pseudo id=sweep
ERM-THRESHOLD(S)                              ▷ h_t(x) = 1 when x ≥ t
L6  sort S by x
L7  e ← the number of i with y_i = 0          ▷ t ≤ min x: every point gets label 1
L8  e⋆ ← e, t⋆ ← the smallest x
L9  for each distinct value v of x, in increasing order do
L10     for each i with x_i = v do e ← e + (1 if y_i = 1 else −1)   ▷ now x_i gets label 0
L11     t ← the next distinct value after v, or +∞
L12     if e < e⋆ then e⋆ ← e, t⋆ ← t
L13 return t⋆, e⋆
```

Line L10 moves the points with value $v$ below the cut. A point with label 1 becomes an error and a point with label 0 stops being one. The sort costs $O(n \log n)$ comparisons and the sweep $O(n)$, with $O(n)$ memory. Points with the same $x$ move together, which is why line L9 runs over distinct values.

**Trace.** Take the sample $(1, 0), (2, 1), (3, 0), (4, 0), (5, 1), (6, 1)$, already sorted. Line L7 gives $e = 3$ for $t = 1$.

| cut below | $t$ | errors $e$ | best so far |
|---|---|---|---|
| none | 1 | 3 | $t = 1$, 3 |
| 1 | 2 | 2 | $t = 2$, 2 |
| 1, 2 | 3 | 3 | $t = 2$, 2 |
| 1, 2, 3 | 4 | 2 | $t = 2$, 2 |
| 1 to 4 | 5 | 1 | $t = 5$, 1 |
| 1 to 5 | 6 | 2 | $t = 5$, 1 |
| 1 to 6 | $+\infty$ | 3 | $t = 5$, 1 |

The output is $t = 5$ with one error, the point $(2, 1)$, so $L_S(h_5) = 1/6$.

**Why ERM learns under uniform convergence.** Call $S$ $\tfrac{\varepsilon}{2}$-representative when $|L_S(h) - L_D(h)| \le \varepsilon/2$ for every $h \in H$. Then for every $h \in H$,

$$L_D(h_S) \le L_S(h_S) + \tfrac{\varepsilon}{2} \le L_S(h) + \tfrac{\varepsilon}{2} \le L_D(h) + \varepsilon.$$

The first and third steps use the representative property, and the middle step holds because $h_S$ minimizes $L_S$. Take $h$ a minimizer of $L_D$ over $H$ (or a near minimizer, if none exists) to get $L_D(h_S) \le \min_{h \in H} L_D(h) + \varepsilon$. This is Lemma 4.2 of Shalev-Shwartz and Ben-David. It holds for every ERM output, so the rule for ties does not matter.

**Sample sizes for a finite class** (natural logarithms, 0-1 loss):

- Realizable case: $n \ge \ln(|H|/\delta)/\varepsilon$ examples make every ERM output have $L_D(h_S) \le \varepsilon$ with probability at least $1 - \delta$. The proof is on the [PAC learning](/pac-learning/) page.
- Agnostic case: $n \ge 2\ln(2|H|/\delta)/\varepsilon^2$ examples make $L_D(h_S) \le \min_{h \in H} L_D(h) + \varepsilon$ with probability at least $1 - \delta$. The proof is on the [agnostic PAC learning](/agnostic-pac-learning/) page.

## Classic examples

- **Conjunctions, realizable.** Valiant's elimination algorithm starts with the conjunction of all $2d$ literals and deletes each literal that a positive example makes false. The result is consistent with the sample, so it is an ERM output, in $O(nd)$ time.
- **Axis aligned rectangles, realizable.** The smallest rectangle that contains the positive examples is consistent, and takes $O(n)$ time to find (Shalev-Shwartz and Ben-David, Section 8.2.2).
- **Halfspaces, realizable.** A halfspace with zero training error is a feasible point of a linear program, see [linear programming](/linear-programming-problem/), or the limit of the [perceptron](/perceptron/) on separable data. Both are polynomial or finite on separable samples. The class is the topic of [halfspace learning](/halfspace-learning/).
- **Least squares.** ERM with the squared loss over linear functions is [ordinary least squares](/ordinary-least-squares/), solved by the normal equations.
- **Log loss.** ERM with the [logistic loss](/logistic-loss/) over linear scores is [logistic regression](/logistic-regression/). ERM with the negative log-likelihood is [maximum likelihood estimation](/maximum-likelihood-estimation/).

## Variations

- **Regularized loss minimization.** Return $\arg\min_h L_S(h) + \lambda R(h)$ for a penalty $R$ such as $\|w\|^2$. The [support vector machine](/support-vector-machine/) and [ridge regression](/ridge-regression/) are of this form. See [regularization](/regularization/).
- **Structural risk minimization.** Over nested classes $H_1 \subseteq H_2 \subseteq \cdots$, minimize the empirical risk plus a penalty that grows with the class, see [structural risk minimization](/structural-risk-minimization/).
- **Surrogate losses.** Minimize a convex upper bound on the 0-1 loss, such as the [hinge loss](/hinge-loss/) or the logistic loss, so that the search is a convex program. The guarantee is then on the surrogate risk.
- **Approximate ERM.** If the output only has $L_S(h_S) \le \min_h L_S(h) + \eta$, the chain of inequalities above gives $L_D(h_S) \le \min_h L_D(h) + \varepsilon + \eta$.
- **Improper ERM.** Run ERM over a larger class that is easy to search. Shalev-Shwartz and Ben-David, Section 8.3, learn 3-term DNF formulas this way with 3-CNF formulas, while proper learning of 3-term DNF is hard unless RP = NP.
- **Iterative methods.** [Stochastic gradient descent](/stochastic-gradient-descent/) approximately minimizes a convex empirical risk with one pass or a few passes over the data.

## Pitfalls

- **No inductive bias.** Over the class of all functions, the memorizer that returns $y_i$ on a seen $x_i$ and 0 elsewhere is an ERM output. With $D$ uniform on $\{0, \ldots, 999\}$, target $1[x < 500]$ and 50 examples (48 distinct points with seed 4), the memorizer has $L_S = 0$ and $L_D = 473/1000$. ERM over the thresholds $1[x \le t]$ on the same sample returns $1[x \le 490]$, which is consistent and has $L_D = 9/1000$. The difference is the class, not the rule. See [overfitting](/overfitting/).
- **Training error is optimistic.** For a fixed $h^\star \in H$, $\mathbb{E}[L_S(h_S)] \le \mathbb{E}[L_S(h^\star)] = L_D(h^\star)$. With $h^\star$ a minimizer of $L_D$, this gives $\mathbb{E}[L_S(h_S)] \le \min_{h \in H} L_D(h) \le \mathbb{E}[L_D(h_S)]$. So the training error of the ERM output is a biased estimate of its true error; use a held out set or [cross-validation](/cross-validation/).
- **Choosing the class with the same data.** Trying many classes on one sample and reporting the best is ERM over the union of the classes. The bounds must use the union, or the penalty of structural risk minimization.
- **Hard search in the agnostic case.** Finding a halfspace with the fewest training errors is NP-hard (Johnson and Preparata 1978). Ben-David, Eiron and Long (2003) show that even approximate agreement maximization is NP-hard for halfspaces, axis aligned rectangles and other classes. These results take the dimension $d$ of the points as part of the input. So agnostic ERM for these classes has no algorithm polynomial in $d$ and $n$ unless P = NP. For a fixed $d$ the search is polynomial in $n$: at most $O(n^d)$ halfspaces give all the different labelings of the sample. Practical systems minimize a convex surrogate instead.
- **ERM is not always the best learner.** For binary classes it learns at the optimal agnostic rate, but in the realizable case some ERM rules need a factor $\log(1/\varepsilon)$ more examples than the best learner; see the [fundamental theorem](/fundamental-theorem-of-statistical-learning/).

## Exercises

1. Run ERM-THRESHOLD on $(1, 1), (2, 0), (3, 1), (4, 1)$. Give the output and its empirical risk.
2. Write an $O(n \log n)$ ERM for intervals $1[a \le x \le b]$ under the 0-1 loss. (Hint: it is a maximum sum subarray problem with weight $+1$ for a label 1 and $-1$ for a label 0.)
3. Show that ERM over a finite class with ties broken at random is still an agnostic PAC learner with the same sample size.
4. Show that the elimination algorithm for conjunctions returns the most specific conjunction that is consistent with the positive examples, and that it never errs on a negative example in the realizable case.

## References
