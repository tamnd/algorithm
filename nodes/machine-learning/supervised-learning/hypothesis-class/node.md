---
tag: 52QMHE
kind: definition
slug: hypothesis-class
name: Hypothesis class
aliases:
- concept class
- hypothesis space
- hypothesis set
area: machine-learning/supervised-learning
level: intro
summary: "The set H of functions from inputs to labels that a learner may output. Its choice before the data is seen is the inductive bias, and its size or VC dimension sets the data a learner needs."
prereqs: [probability-distribution]
see_also: [empirical-risk-minimization, pac-learning, vc-dimension, bias-variance-tradeoff, no-free-lunch-theorem-learning, halfspace-learning, range-space, loss-function]
sources:
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, From Theory to Algorithms, Cambridge University Press, 2014
    locator: Section 2.3 (ERM with inductive bias), Section 5.2 (error decomposition), Section 9.1.3 (Theorems 9.2 and 9.3, the VC dimension of halfspaces)
  - book: isbn:9780262111935
    title: Michael J. Kearns and Umesh V. Vazirani, An Introduction to Computational Learning Theory, MIT Press, 1994
    locator: Chapter 1 (concept classes, representation classes and the hypothesis class of the learner)
  - book: isbn:9780262039406
    title: Mehryar Mohri, Afshin Rostamizadeh and Ameet Talwalkar, Foundations of Machine Learning, second edition, MIT Press, 2018
    locator: Chapter 2 (the hypothesis set in the PAC framework)
  - paper: doi:10.1145/1968.1972
    title: L. G. Valiant, A theory of the learnable, Communications of the ACM 27(11), 1984
    locator: pp. 1134 to 1142 (concepts, and the classes of Boolean functions that are learnable)
---

A hypothesis class is the set $H$ of functions from an input domain $X$ to a label set $Y$ from which a learning algorithm picks its output. The learner fixes $H$ before it sees the data, so $H$ is its *inductive bias*: it can only fit patterns that some member of $H$ expresses. The size of $H$, or its [VC dimension](/vc-dimension/) when $H$ is infinite, sets how many examples [empirical risk minimization](/empirical-risk-minimization/) needs to choose well. A small class needs few examples but may contain no good function; a large class contains good functions but needs many examples.

## Definition

Notation on this page: $X$ is the domain, $Y$ the label set ($Y = \{0, 1\}$ for binary classification), $D$ an unknown [probability distribution](/probability-distribution/) on $X \times Y$, and $S = ((x_1, y_1), \ldots, (x_n, y_n))$ a sample of $n$ examples drawn i.i.d. from $D$.

- A **hypothesis** is a function $h : X \to Y$.
- A **hypothesis class** is a set $H \subseteq Y^X$ of hypotheses.
- For a [loss function](/loss-function/) $\ell : Y \times Y \to \mathbb{R}_{\ge 0}$, the **true risk** of $h$ is $L_D(h) = \mathbb{E}_{(x, y) \sim D}[\ell(h(x), y)]$ and the **empirical risk** is $L_S(h) = \frac{1}{n} \sum_{i=1}^{n} \ell(h(x_i), y_i)$. Under the 0-1 loss, $\ell(\hat y, y) = 1[\hat y \ne y]$, so $L_D(h) = \Pr_D[h(x) \ne y]$.
- $D$ is **realizable** by $H$ when some $h^\star \in H$ has $L_D(h^\star) = 0$. Otherwise the setting is **agnostic**: the learner competes with $\min_{h \in H} L_D(h)$, see [agnostic PAC learning](/agnostic-pac-learning/).
- For points $C = (c_1, \ldots, c_k)$ of $X$, the **restriction** of $H$ to $C$ is the set of label vectors $H_C = \{(h(c_1), \ldots, h(c_k)) : h \in H\}$. All capacity measures of a binary class look at $H$ only through these restrictions.

A learner is **proper** when its output always lies in $H$, and **improper** when it may output a function outside $H$ while it is judged against $H$. In the model of Valiant and of Kearns and Vazirani, the target belongs to a **concept class** $C$, and the learner outputs from a class $H$ that may be larger than $C$. When $H = C$, the two words name the same set, and most texts then say "hypothesis class" for both.

A class is often given by parameters: $H = \{h_\theta : \theta \in \Theta\}$. The class is the set of functions, not the set of parameters. Two parameters can give the same function, and one real parameter can give a class of infinite VC dimension.

**Error decomposition.** For an output $h_S \in H$, with $L_D^\star$ the least risk of any function (the [Bayes optimal classifier](/bayes-optimal-classifier/)),

$$L_D(h_S) - L_D^\star = \underbrace{\Big(\min_{h \in H} L_D(h) - L_D^\star\Big)}_{\text{approximation error}} + \underbrace{\Big(L_D(h_S) - \min_{h \in H} L_D(h)\Big)}_{\text{estimation error}}.$$

The identity holds because the two middle terms cancel. A larger class can only lower the approximation error, and for a fixed $n$ it usually raises the estimation error. This is the bias-complexity tradeoff of Shalev-Shwartz and Ben-David, Section 5.2, which the page on the [bias-variance tradeoff](/bias-variance-tradeoff/) treats for the squared loss.

## Examples and non-examples

| Class | Domain | Size | VC dimension |
|---|---|---|---|
| thresholds $h_t(x) = 1[x \ge t]$ | $\mathbb{R}$ | infinite | 1 |
| intervals $1[a \le x \le b]$ | $\mathbb{R}$ | infinite | 2 |
| axis aligned rectangles | $\mathbb{R}^2$ | infinite | 4 |
| halfspaces $1[\langle w, x \rangle + b \ge 0]$ | $\mathbb{R}^d$ | infinite | $d + 1$ |
| conjunctions of literals | $\{0, 1\}^d$ | $3^d + 1$ | $d$ |
| all functions | infinite $X$ | infinite | infinite |

The VC dimensions are proved on the [VC dimension](/vc-dimension/) page; the class of halfspaces is the subject of [halfspace learning](/halfspace-learning/).

**Restriction of thresholds.** Take $C = (1, 2, 3)$. A threshold labels a prefix of the sorted points 0 and the rest 1, so $H_C = \{(1,1,1), (0,1,1), (0,0,1), (0,0,0)\}$. This is 4 of the $2^3 = 8$ label vectors. The vector $(1, 0, 1)$ is missing, so no threshold fits a sample with those labels, whatever the sample size.

**Conjunctions.** Over $d$ Boolean variables, a conjunction such as $x_1 \wedge \neg x_3$ says for each variable whether it appears positive, negative or not at all. These $3^d$ conjunctions are different functions, because each one is true exactly on a different subcube of $\{0, 1\}^d$. A conjunction with both $x_i$ and $\neg x_i$ is the constant 0, which adds one more function, so $|H| = 3^d + 1$. For $d = 3$ this is 28 functions. In the realizable case, the [PAC learning](/pac-learning/) bound for finite classes then asks for $\lceil \ln(28/0.05)/0.1 \rceil = 64$ examples for error $\varepsilon = 0.1$ with confidence $1 - \delta = 0.95$.

**The class of all functions.** If $X$ is infinite and $H = \{0, 1\}^X$, then every sample is fit by some $h \in H$, and the fit says nothing about new points. The [no-free-lunch theorem](/no-free-lunch-theorem-learning/) makes this exact: no learner can PAC learn this class.

Non-examples:

- **A trained model.** One network with fixed weights is a hypothesis, not a class. The class is the set of all functions that the architecture computes for some weights.
- **A set of parameter vectors.** For homogeneous halfspaces, $w$ and $2w$ give the same function $x \mapsto 1[\langle w, x \rangle \ge 0]$. Counting parameters, or counting parameter vectors on a grid, can overstate the size of the class. The other way also fails: the one-parameter class $x \mapsto 1[\sin(\theta x) > 0]$ has infinite VC dimension.
- **A class chosen after the data.** The bounds of [PAC learning](/pac-learning/) hold for a class fixed before the sample is drawn. If a family of classes is searched with the same sample, the bound must pay for the search, as in [structural risk minimization](/structural-risk-minimization/).
- **A distribution or a loss.** These define the risk of each hypothesis; they are not part of $H$.

## Related definitions

- [Empirical risk minimization](/empirical-risk-minimization/) returns a member of $H$ with the least empirical risk.
- [PAC learning](/pac-learning/) and [agnostic PAC learning](/agnostic-pac-learning/) define when a class is learnable from a number of examples that does not depend on $D$.
- The [VC dimension](/vc-dimension/), the growth function of the [Sauer-Shelah lemma](/sauer-shelah-lemma/), the [Rademacher complexity](/rademacher-complexity/) and the fat-shattering dimension of the [margin bound](/margin-generalization-bound/) measure the capacity of $H$.
- A binary hypothesis is the indicator function of a subset of $X$. So a binary class is a [range space](/range-space/) $(X, \{h^{-1}(1) : h \in H\})$ in the language of computational geometry, and the two notions of VC dimension agree.
- A sequence of nested classes $H_1 \subseteq H_2 \subseteq \cdots$ is the input of [structural risk minimization](/structural-risk-minimization/). A class weighted by a prefix code is the input of [minimum description length](/minimum-description-length/).
- The [generalization error](/generalization-error/) of a hypothesis is its true risk, or the gap between its true and empirical risk; texts use both meanings.

## References
