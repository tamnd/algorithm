---
tag: FBF4BY
kind: concept
slug: gini-impurity
name: Gini impurity
aliases:
- Gini index
- Gini index of diversity
area: machine-learning/supervised-learning
level: intro
summary: "The impurity 1 - Σ p_k^2 of a node's label distribution: the chance that a label drawn at random from the node is wrong. CART splits to reduce it."
prereqs: [discrete-probability-distribution, classification]
see_also: [information-gain, cart, decision-tree-learning, shannon-entropy, binary-entropy-function, mean-squared-error]
sources:
  - book: isbn:9780412048418
    title: Leo Breiman, Jerome H. Friedman, Richard A. Olshen and Charles J. Stone, Classification and Regression Trees, Wadsworth, 1984 (reprinted by Chapman and Hall/CRC)
    locator: Chapter 4 (splitting rules; the Gini index of diversity, its interpretations and the twoing rule)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 9.2.3 (node impurity measures, Figure 9.3, and the example of 400 and 400 observations where misclassification error cannot tell two splits apart)
  - paper: "Laura Elena Raileanu and Kilian Stoffel, Theoretical comparison between the Gini index and information gain criteria, Annals of Mathematics and Artificial Intelligence 41(1), 2004"
    locator: pages 77 to 93 (a formal and empirical comparison of the two split criteria)
---

The Gini impurity of a set of labeled examples is $G = 1 - \sum_{c=1}^{k} p_c^2$, where $p_c$ is the fraction of examples of class $c$ among $k$ classes. It is the probability that two labels drawn at random with replacement from the set differ, which is the error rate of a guess drawn at random from the set's own label distribution. [CART](/cart/) grows a classification tree by choosing at each node the split that most reduces the size-weighted Gini impurity. Like the [entropy](/shannon-entropy/) behind [information gain](/information-gain/), it is concave, zero exactly on pure nodes and largest at the uniform distribution.

## In plain words

Look at a box of labeled examples. Pick one example at random and look at its label. Then guess a label for a second random example by copying the first label. The Gini impurity is the chance that this guess is wrong.

If all examples in the box have the same label, the guess is always right and the impurity is zero. If two labels are each half of the box, the guess is wrong half of the time. The more mixed the box, the larger the impurity.

A tree learner tries each possible question, splits the box into smaller boxes, and adds up their impurities, each weighted by its share of the examples. It asks the question that makes this sum smallest.

## The idea

**Definition.** Let a node hold $n$ examples, $n_c$ of class $c$, and $p_c = n_c / n$. Then

$$ G(p) = 1 - \sum_{c=1}^{k} p_c^2 = \sum_{c=1}^{k} p_c (1 - p_c) = \sum_{c \ne c'} p_c\, p_{c'}. $$

The three forms are equal because $\sum_c p_c = 1$. The last one is the probability that two independent draws from $p$ give different classes. If you label a random example of the node by an independent draw from $p$, you are wrong with exactly this probability, which is Breiman et al.'s reading of it as a misclassification rate.

**The split criterion.** A split sends the $n$ examples to branches with $n_1, \ldots, n_r$ examples and label distributions $p^{(1)}, \ldots, p^{(r)}$. CART uses binary splits, $r = 2$, and maximizes the decrease

$$ \Delta G = G(p) - \sum_{v=1}^{r} \frac{n_v}{n} G(p^{(v)}). $$

Multiplying by $n$ gives the total form $n\,G = n - \sum_c n_c^2 / n$, which needs only the class counts, so a scan over sorted values can update it in $O(k)$ time per example, or $O(1)$ with a running sum of squares.

**Binary case.** With two classes and $p = p_1$,

$$ G = 2p(1 - p), \qquad H = h(p) = -p \log_2 p - (1 - p)\log_2 (1 - p), $$

where $h$ is the [binary entropy function](/binary-entropy-function/) in bits. Both are 0 at $p \in \{0, 1\}$ and largest at $p = 1/2$, with $G = 1/2$ and $h = 1$.

| $p$ | 0 | 0.1 | 0.2 | 0.3 | 0.5 |
|---|---|---|---|---|---|
| Gini $2p(1-p)$ | 0 | 0.18 | 0.32 | 0.42 | 0.5 |
| entropy $h(p)$ in bits | 0 | 0.4690 | 0.7219 | 0.8813 | 1 |
| entropy in nats | 0 | 0.3251 | 0.5004 | 0.6109 | 0.6931 |
| misclassification $\min(p, 1 - p)$ | 0 | 0.1 | 0.2 | 0.3 | 0.5 |

**How it relates to entropy.** The two measures have the same shape and differ in detail.

1. **Both are concave, zero exactly at the pure distributions, and largest at the uniform one.** $G = 1 - \lVert p \rVert^2$ is strictly concave because $\lVert p \rVert^2$ is strictly convex. Its largest value on $k$ classes is $1 - 1/k$, at $p_c = 1/k$, since $\sum_c p_c^2 \ge 1/k$ by the Cauchy-Schwarz inequality. The entropy is strictly concave with largest value $\log_2 k$. $G = 0$ if and only if $\sum_c p_c^2 = 1$, which with $\sum_c p_c = 1$ and $p_c \ge 0$ holds only when one $p_c$ is 1.
2. **Gini is a lower bound on the entropy in nats.** Since $-\ln t \ge 1 - t$ for $t > 0$, $H_{\text{nats}}(p) = \sum_c p_c(-\ln p_c) \ge \sum_c p_c (1 - p_c) = G(p)$, with equality only at pure nodes. The Gini impurity is the first-order term of the entropy, with $-\ln p_c$ replaced by its tangent at $p_c = 1$.
3. **Both bound the misclassification rate.** $\sum_c p_c^2 \le \max_c p_c \sum_c p_c = \max_c p_c$, so $G \ge 1 - \max_c p_c$, the error of predicting the majority class.
4. **Splits never raise the weighted impurity.** For either measure, by concavity and Jensen's inequality, $\sum_v \frac{n_v}{n} G(p^{(v)}) \le G(\sum_v \frac{n_v}{n} p^{(v)}) = G(p)$, so $\Delta G \ge 0$, with equality if and only if all branches have the parent's distribution. The same holds for the entropy.
5. **A variance.** Code the label as the one-hot vector $e_{y_i} \in \{0, 1\}^k$. The mean vector is $p$, and $\frac{1}{n} \sum_i \lVert e_{y_i} - p \rVert^2 = 1 - \lVert p \rVert^2 = G$. So the Gini decrease is the decrease of the squared error of the one-hot labels, the criterion of a CART regression tree applied to these vectors. For two classes, $G/2 = p(1-p)$ is the variance of the 0/1 label.

Neither measure is always better. They choose the same split on most data, and studies such as Raileanu and Stoffel (2004) find that they rarely disagree. Gini needs no logarithm, which makes it a little cheaper. The choice matters less than the stopping and pruning rules.

## Examples

**PlayTennis.** The 14 days of [ID3](/id3/)'s example have 9 positive and 5 negative labels, so $G = 1 - (9/14)^2 - (5/14)^2 = 45/98 = 0.4592$. The weighted Gini of the four attributes and the decrease:

| attribute | branch counts (positive, negative) | weighted $G$ | $\Delta G$ |
|---|---|---|---|
| outlook | (2, 3), (4, 0), (3, 2) | 12/35 = 0.3429 | 0.1163 |
| humidity | (3, 4), (6, 1) | 18/49 = 0.3673 | 0.0918 |
| windy | (6, 2), (3, 3) | 3/7 = 0.4286 | 0.0306 |
| temperature | (2, 2), (4, 2), (3, 1) | 37/84 = 0.4405 | 0.0187 |

The order is the same as with information gain (outlook 0.247, humidity 0.152, windy 0.048, temperature 0.029 bits). These are multiway splits; CART would split on a subset of the values.

**Why not the misclassification rate (Hastie, Tibshirani and Friedman, Section 9.2.3).** A node has 400 examples of each of two classes. Split 1 gives branches with counts (300, 100) and (100, 300). Split 2 gives (200, 400) and (200, 0). Both make 200 errors, a misclassification rate of 0.25, so that criterion cannot choose. The weighted Gini is $0.375$ for split 1 and $\frac{600}{800} \cdot 2 \cdot \frac13 \cdot \frac23 = 0.3333$ for split 2; the weighted entropy is $0.8113$ and $0.6887$ bits. Both concave measures prefer split 2, which makes a pure node that later splits need not touch. The misclassification rate is piecewise linear, not strictly concave, so many splits tie under it.

**Three classes.** Counts $(5, 3, 2)$ give $G = 1 - 0.25 - 0.09 - 0.04 = 0.62$. The uniform distribution on 3 classes gives the largest value, $2/3$.

## Where it is used

- [CART](/cart/) uses the Gini decrease to grow classification trees, and libraries use it as the default criterion of [random forests](/random-forest/). The same total form $n\,G$ gives the fast split scan of [decision tree learning](/decision-tree-learning/) and of the [decision stump](/decision-stump/).
- The mean decrease of Gini impurity over all nodes that split on a feature is a common feature importance score of tree ensembles. It is biased toward features with many distinct values, for the same reason as [information gain](/information-gain/).
- The identity with the squared error of one-hot labels links it to the [mean squared error](/mean-squared-error/), and so to regression trees.
- In ecology the same quantity, $\sum_c p_c^2$ or one minus it, is Simpson's diversity index. The Gini coefficient of income inequality is a different quantity.

## References
