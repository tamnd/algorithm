---
tag: D427XN
kind: concept
slug: roc-auc
name: ROC curve and AUC
aliases:
- receiver operating characteristic
- AUROC
- ROC AUC
area: machine-learning/supervised-learning
level: intro
summary: "The ROC curve plots true positive rate against false positive rate over all thresholds. Its area equals U/(n+ n-), the rate of correctly ordered pairs."
prereqs: [confusion-matrix]
see_also: [precision-and-recall, confusion-matrix, classification, learning-to-rank, sorting-problem, merge-sort, logistic-regression]
sources:
  - paper: doi:10.1016/j.patrec.2005.10.010
    title: Tom Fawcett, An introduction to ROC analysis, Pattern Recognition Letters 27(8), 861-874, 2006
    locator: Section 5 (efficient generation of ROC curves), Section 6 (the ROC convex hull), Section 7 (area under the curve, and Algorithm 2), Section 10 (more than two classes)
  - paper: doi:10.1148/radiology.143.1.7063747
    title: James A. Hanley and Barbara J. McNeil, The meaning and use of the area under a receiver operating characteristic (ROC) curve, Radiology 143(1), 29-36, 1982
    locator: the area equals the Wilcoxon statistic, and its approximate standard error
  - paper: doi:10.1214/aoms/1177730491
    title: H. B. Mann and D. R. Whitney, On a test of whether one of two random variables is stochastically larger than the other, Annals of Mathematical Statistics 18(1), 50-60, 1947
    locator: the statistic U
  - paper: "Donald Bamber, The area above the ordinal dominance graph and the area below the receiver operating characteristic graph, Journal of Mathematical Psychology 12(4), 1975"
    locator: the area below the ROC graph as P(X < Y) + P(X = Y) / 2
  - paper: "David J. Hand and Robert J. Till, A simple generalisation of the area under the ROC curve for multiple class classification problems, Machine Learning 45(2), 171-186, 2001"
    locator: the multiclass measure M and the relation Gini = 2 AUC - 1
---

The ROC (receiver operating characteristic) curve of a real-valued score plots the true positive rate against the false positive rate as the decision threshold moves from $+\infty$ to $-\infty$ (Fawcett 2006). The area under it, the AUC, is the probability that a random positive example gets a higher score than a random negative one, with ties counted as one half. This equals the Mann-Whitney statistic $U$ divided by $n_+ n_-$ (Hanley and McNeil 1982). One sort of the scores computes the curve and the area in $O(n \log n)$ time, against $O(n_+ n_-)$ for the count over all pairs.

## In plain words

A test gives each patient a number, and a higher number means "more likely sick". To make a decision you pick a cut-off. A low cut-off catches almost every sick patient but also alarms many healthy ones. A high cut-off does the reverse. The ROC curve shows all these choices at once: how many sick patients you catch against how many healthy patients you alarm.

The area under the curve is one number for the whole curve. It has a simple meaning. Take one sick and one healthy patient at random. The area is the chance that the sick one has the higher number. A test that guesses gets one half, and a perfect test gets one.

## The idea

**The curve.** Let $s(x)$ be a score and predict positive when $s(x) \ge \tau$. With $n_+$ positive and $n_-$ negative examples, each threshold gives a binary [confusion matrix](/confusion-matrix/) and the point

$$\mathrm{FPR}(\tau) = \frac{\mathrm{FP}(\tau)}{n_-}, \qquad \mathrm{TPR}(\tau) = \frac{\mathrm{TP}(\tau)}{n_+}.$$

As $\tau$ falls both rates grow, from $(0, 0)$ to $(1, 1)$. The point $(0, 1)$ is a perfect classifier, and the diagonal $\mathrm{TPR} = \mathrm{FPR}$ is what a random guess achieves at any rate. Both rates are computed within one class, so the curve does not change when the class proportions change; this is the main difference from the [precision-recall curve](/precision-and-recall/).

**The area as a pair count.** Define

$$\mathrm{AUC} = \frac{1}{n_+ n_-} \sum_{i : y_i = 1} \sum_{j : y_j = 0} \Big( \mathbb{1}[s_i > s_j] + \tfrac12\, \mathbb{1}[s_i = s_j] \Big).$$

For a random positive $X_+$ and a random negative $X_-$ from the data, this is $P(s(X_+) > s(X_-)) + \frac12 P(s(X_+) = s(X_-))$ (Bamber 1975).

**The area under the curve is that count.** Sort the examples by decreasing score and group equal scores. A group with $a$ positives and $b$ negatives, reached after $T$ positives with higher scores, moves the curve right by $b/n_-$ and up by $a/n_+$, and adds the trapezoid

$$\frac{b}{n_-} \cdot \frac{1}{2}\Big(\frac{T}{n_+} + \frac{T + a}{n_+}\Big) = \frac{b\,(T + a/2)}{n_+ n_-}.$$

Each of the $b$ negatives in the group is beaten by the $T$ positives above it (1 each), ties with the $a$ positives in its group ($\frac12$ each), and beats the rest (0). Summing over the groups gives the pair count. $\blacksquare$ The tie group is the diagonal segment of the curve, and the trapezoid rule is exactly what gives a tie the value $\frac12$.

**The Mann-Whitney form.** Rank all $n$ scores from 1 (smallest) to $n$, giving each tie group the mean of its ranks (mid-ranks). Let $R_+$ be the sum of the ranks of the positives. Then

$$U = R_+ - \frac{n_+(n_+ + 1)}{2}, \qquad \mathrm{AUC} = \frac{U}{n_+ n_-}.$$

The mid-rank of a positive is 1 plus the number of examples below it plus half the number of others tied with it. Summed over the positives, the pairs of two positives contribute exactly $n_+(n_+ + 1)/2$, and the rest is the pair count above. This is the identity of Hanley and McNeil (1982) between the AUC and the Wilcoxon-Mann-Whitney statistic.

**The algorithm.** Sort the indices by decreasing score in $O(n \log n)$. Scan once, keep $T$ and $F$ (positives and negatives seen so far), and at the end of each tie group add $b\,(2T + a)$ to an integer accumulator. Divide by $2 n_+ n_-$ at the end. This is Fawcett's Algorithm 2 with exact integer arithmetic. The same scan outputs the ROC points. The pair count needs $O(n_+ n_-)$ time; counting the correctly ordered pairs during a [merge sort](/merge-sort/), as in inversion counting, also takes $O(n \log n)$. If the scores are already [sorted](/sorting-problem/), the scan alone is $O(n)$.

**Facts that follow.**

- AUC does not change under any strictly increasing transformation of the score. It measures ranking only, not the calibration of probabilities.
- Reversing the score gives $1 - \mathrm{AUC}$. A constant score gives exactly $\frac12$ because every pair is a tie.
- For a hard 0/1 prediction the curve has one inner point, and $\mathrm{AUC} = \frac12(\mathrm{TPR} + 1 - \mathrm{FPR})$, the balanced accuracy.
- The Gini coefficient used in credit scoring is $2\,\mathrm{AUC} - 1$ (Hand and Till 2001).

**The convex hull.** Choosing at random between two classifiers reaches every point on the segment between their ROC points. Lines of equal expected cost have slope $\frac{c_{\mathrm{FP}}\, \pi_-}{c_{\mathrm{FN}}\, \pi_+}$, where $\pi_\pm$ are the class proportions and $c$ the error costs, so for any costs and proportions the best threshold is a vertex of the upper convex hull of the curve (Fawcett, Section 6).

**Uncertainty.** Hanley and McNeil give the approximate standard error

$$\mathrm{SE}^2 = \frac{A(1 - A) + (n_+ - 1)(Q_1 - A^2) + (n_- - 1)(Q_2 - A^2)}{n_+ n_-}, \qquad Q_1 = \frac{A}{2 - A},\ Q_2 = \frac{2A^2}{1 + A}.$$

**More than two classes.** Either average the one-vs-rest AUCs, or use the measure $M$ of Hand and Till (2001): the mean over all pairs of classes $i < j$ of $\frac12(\hat A(i \mid j) + \hat A(j \mid i))$, where $\hat A(i \mid j)$ is the AUC of the score for class $i$ on the examples of classes $i$ and $j$ only.

## Examples

**Eight examples, no ties.** Scores $0.9, 0.8, 0.7, 0.6, 0.55, 0.5, 0.4, 0.3$ with labels $+, +, -, +, -, +, -, -$.

- The ROC points, threshold by threshold: $(0, \frac14), (0, \frac12), (\frac14, \frac12), (\frac14, \frac34), (\frac12, \frac34), (\frac12, 1), (\frac34, 1), (1, 1)$.
- The area is $\frac14 \cdot \frac12 + \frac14 \cdot \frac34 + \frac12 \cdot 1 = \frac{13}{16} = 0.8125$.
- Pairs: the four negatives are beaten by 2, 3, 4 and 4 positives, so the count is $13/16$.
- Mid-ranks of the positives (ascending): $8, 7, 5, 3$, so $U = 23 - 10 = 13$.

The average precision of the same data is $0.854$ (see [precision and recall](/precision-and-recall/)); it is a different number on a different scale. With only four examples of each class, the Hanley-McNeil standard error is about $0.16$.

**Seven examples with ties.** Positives score $3, 2, 2, 1$ and negatives $2, 1, 0$.

| group (score) | positives | negatives | point after the group | trapezoid |
|---|---|---|---|---|
| 3 | 1 | 0 | $(0, \frac14)$ | 0 |
| 2 | 2 | 1 | $(\frac13, \frac34)$ | $\frac13 \cdot \frac12(\frac14 + \frac34) = \frac16$ |
| 1 | 1 | 1 | $(\frac23, 1)$ | $\frac13 \cdot \frac12(\frac34 + 1) = \frac{7}{24}$ |
| 0 | 0 | 1 | $(1, 1)$ | $\frac13$ |

The area is $\frac{19}{24} = 0.7917$. The pair count agrees: the positive with score 3 beats all 3 negatives; each positive with score 2 ties one negative and beats two, $2.5$ each; the positive with score 1 ties one and beats one, $1.5$. The total is $9.5$ out of 12. Mid-ranks: score 0 has rank 1, the two 1s share $2.5$, the three 2s share 5, and 3 has rank 7, so $R_+ = 7 + 5 + 5 + 2.5 = 19.5$ and $U = 19.5 - 10 = 9.5$.

## Where it is used

- Medical diagnosis and radiology, where ROC analysis began for tests with a continuous reading and the threshold is set later.
- Comparing scoring models in credit risk, fraud detection and information retrieval before a threshold is chosen.
- Model selection in [classification](/classification/) when the class proportions at deployment are unknown or change.
- As a ranking objective: maximizing AUC is a pairwise [learning to rank](/learning-to-rank/) problem.

### Pitfalls

- **Ties counted as 0 or 1.** An implementation that sorts and walks one example at a time, without grouping ties, gives a result that depends on the input order. With a constant score it can return anything from 0 to 1 instead of $\frac12$.
- **High AUC with rare positives.** With 10 positives among $10^5$ examples, an AUC of $0.99$ can still mean that most predicted positives are false. Look at [precision](/precision-and-recall/) at the threshold you will use.
- **AUC averages over all thresholds**, including ones you will never use. Partial AUC restricts the false positive rate to a range.
- **AUC says nothing about probabilities.** Two models with the same AUC can give very different probabilities. Use a proper loss such as the [logistic loss](/logistic-loss/) for that.
- **Area under the PR curve is not AUC.** Both are "the area under the curve"; name the curve.

## References
