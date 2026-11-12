---
tag: 1ZSBS6
kind: concept
slug: precision-and-recall
name: Precision and recall
aliases:
- F1 score
- F-measure
- average precision
area: machine-learning/supervised-learning
level: intro
summary: "Precision TP/(TP+FP) and recall TP/(TP+FN), their F-beta mean, micro, macro and weighted averages, and the precision-recall curve with average precision."
prereqs: [confusion-matrix]
see_also: [confusion-matrix, roc-auc, classification, multiclass-classification, learning-to-rank, cross-validation]
sources:
  - book: "C. J. van Rijsbergen, Information Retrieval, second edition, Butterworths, 1979"
    locator: Chapter 7 (evaluation, and the effectiveness measure E built from precision and recall)
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schutze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 8 (Section 8.3, precision, recall and the F measure; Section 8.4, interpolated precision and 11-point interpolated average precision)
  - paper: doi:10.1145/1143844.1143874
    title: Jesse Davis and Mark Goadrich, The relationship between precision-recall and ROC curves, Proceedings of the 23rd International Conference on Machine Learning, 233-240, 2006
    locator: linear interpolation between points in PR space is incorrect; a curve dominates in ROC space iff it dominates in PR space
  - paper: "Marina Sokolova and Guy Lapalme, A systematic analysis of performance measures for classification tasks, Information Processing and Management 45(4), 427-437, 2009"
    locator: micro and macro averaging of precision, recall and F-score for multiclass and multilabel tasks
---

Precision is the fraction of the examples predicted positive that are positive, $\mathrm{TP}/(\mathrm{TP} + \mathrm{FP})$, and recall is the fraction of the positive examples that are predicted positive, $\mathrm{TP}/(\mathrm{TP} + \mathrm{FN})$. Both are read from the [confusion matrix](/confusion-matrix/), and neither uses the true negatives, which makes them the usual pair when positives are rare. The $F_\beta$ score of van Rijsbergen (1979) combines them in a weighted harmonic mean. For more than two classes they are averaged in a micro, macro or weighted way, and for a real-valued score they trace the precision-recall curve, which average precision summarizes.

## In plain words

A search engine returns twenty pages for your question. Precision asks how many of those twenty are useful. Recall asks how many of all the useful pages on the web are among the twenty. A short list of very good pages has high precision and low recall. A list of every page has full recall and very low precision.

There is a trade-off. To find more of the good items, you must accept more bad ones. A single score that weighs both is the F score. If the classifier gives a score instead of a yes or no, you can move the cut-off and draw how precision changes as recall grows. One number for the whole curve is the average precision.

## The idea

**Precision, recall and $F_\beta$.** For one positive class with counts TP, FP and FN,

$$P = \frac{\mathrm{TP}}{\mathrm{TP} + \mathrm{FP}}, \qquad R = \frac{\mathrm{TP}}{\mathrm{TP} + \mathrm{FN}}, \qquad F_\beta = \frac{(1 + \beta^2)\, P R}{\beta^2 P + R} = \frac{(1 + \beta^2)\,\mathrm{TP}}{(1 + \beta^2)\,\mathrm{TP} + \beta^2\, \mathrm{FN} + \mathrm{FP}}.$$

Recall is also called sensitivity or the true positive rate. $F_1 = 2PR/(P + R)$ is the harmonic mean. $F_\beta$ is the harmonic mean with weight $\frac{1}{1 + \beta^2}$ on $\frac1P$ and $\frac{\beta^2}{1 + \beta^2}$ on $\frac1R$, so $\beta > 1$ favors recall. van Rijsbergen defines the effectiveness measure $E = 1 - \big(\frac{\alpha}{P} + \frac{1 - \alpha}{R}\big)^{-1}$; with $\alpha = 1/(1 + \beta^2)$, $F_\beta = 1 - E$. The count form on the right shows that $F_\beta$ ignores TN.

**The convention for $0/0$.** Precision is $0/0$ when the classifier predicts no positives, recall is $0/0$ when there are no positive examples, and $F_\beta$ is $0/0$ when $\mathrm{TP} = \mathrm{FP} = \mathrm{FN} = 0$. This page sets each such value to 0, as scikit-learn does by default (with a warning, and a `zero_division` argument to choose 0 or 1 instead). The choice changes macro averages, so report it.

**Averaging over $k$ classes.** Treat each class $j$ in turn as positive, with $\mathrm{TP}_j$, $\mathrm{FP}_j$, $\mathrm{FN}_j$ from the confusion matrix and support $t_j = \mathrm{TP}_j + \mathrm{FN}_j$.

- *Micro:* add the counts over the classes first, then compute $P$, $R$, $F$ once. In single-label multiclass classification every error is one FP (for the predicted class) and one FN (for the true class), so $\sum_j \mathrm{FP}_j = \sum_j \mathrm{FN}_j = n - \sum_j \mathrm{TP}_j$, and micro-$P$ = micro-$R$ = micro-$F_1$ = accuracy.
- *Macro:* compute $P_j$, $R_j$, $F_j$ for each class and take the plain mean. Every class counts the same, so rare classes count more than their share. Macro recall is the balanced accuracy. Macro-$F_1$ here is the mean of the $F_j$; some papers instead take $F_1$ of macro-$P$ and macro-$R$, which is a different number.
- *Weighted:* the mean of the per-class values with weights $t_j / n$. Weighted recall is $\sum_j \frac{t_j}{n}\frac{\mathrm{TP}_j}{t_j}$ = accuracy.

**The precision-recall curve.** A scorer $s(x)$ predicts positive when $s(x) \ge \tau$. Sort the examples by decreasing score, and at each distinct score value $\tau_1 > \tau_2 > \cdots$ take all examples with score at least $\tau_n$. Examples with equal scores must enter together, since no threshold separates them. This gives points $(R_n, P_n)$. Recall never decreases as $\tau$ falls, but precision can go up and down. The curve of a random scorer lies near the horizontal line $P = \pi$, where $\pi$ is the fraction of positives, so the baseline depends on the class balance (for [ROC](/roc-auc/) it is always the diagonal).

**Average precision, and what this page computes.** Three different numbers are all called the area under the PR curve:

1. *Average precision (AP), the step sum.* $\mathrm{AP} = \sum_n (R_n - R_{n-1})\, P_n$ with $R_0 = 0$. Without ties it equals the mean, over the positive examples, of the precision at the rank of that example. It uses no interpolation. This is what this page and scikit-learn's `average_precision_score` compute.
2. *The trapezoid area.* Join the points by straight lines and integrate. Davis and Goadrich (2006) show that straight lines in PR space are wrong: between two achievable points the achievable precision follows a curve that is not linear in recall. So the trapezoid area is not the area of an achievable curve. It can be too high, for example when it joins two points far apart, as Davis and Goadrich show. It can also be too low: on the example below it is less than AP.
3. *Interpolated AP.* Replace precision by the interpolated precision $P_{\mathrm{interp}}(r) = \max_{r' \ge r} P(r')$ and average it at fixed recall levels, for example the 11 levels $0, 0.1, \ldots, 1$ used in information retrieval (Manning, Raghavan and Schutze, Section 8.4). Interpolation never lowers a value.

They are not interchangeable; state which one a table reports.

**Cost.** One pass over a confusion matrix gives all the counts in $O(k^2)$. The PR curve and AP need a sort of the scores, $O(n \log n)$, then one linear scan that groups ties.

## Examples

**One class.** With $\mathrm{TP} = 40$, $\mathrm{FP} = 5$, $\mathrm{FN} = 10$: $P = 40/45 = 0.889$, $R = 40/50 = 0.8$, $F_1 = 80/95 = 0.842$. With $\beta = 2$, $F_2 = 200/(200 + 40 + 5) = 0.816$, closer to $R$.

**Three classes.** For the cat, dog and bird matrix of the [confusion matrix](/confusion-matrix/) page (rows true, columns predicted: $(8, 1, 1)$, $(2, 3, 1)$, $(0, 1, 3)$):

| class | TP | FP | FN | $P_j$ | $R_j$ | $F_{1,j}$ |
|---|---|---|---|---|---|---|
| cat | 8 | 2 | 2 | 0.800 | 0.800 | 0.800 |
| dog | 3 | 2 | 3 | 0.600 | 0.500 | 0.545 |
| bird | 3 | 2 | 1 | 0.600 | 0.750 | 0.667 |

- Micro: $P = R = F_1 = 14/20 = 0.7$, the accuracy.
- Macro: $P = 0.667$, $R = 41/60 = 0.683$, $F_1 = 0.671$. The $F_1$ of macro-$P$ and macro-$R$ is $0.675$ instead.
- Weighted (supports 10, 6, 4): $R = 0.7$, $F_1 = 23/33 = 0.697$.

**A PR curve and three areas.** Eight examples with scores $0.9, 0.8, 0.7, 0.6, 0.55, 0.5, 0.4, 0.3$ and labels $+, +, -, +, -, +, -, -$ (four positives).

| threshold | 0.9 | 0.8 | 0.7 | 0.6 | 0.55 | 0.5 | 0.4 | 0.3 |
|---|---|---|---|---|---|---|---|---|
| recall | 1/4 | 2/4 | 2/4 | 3/4 | 3/4 | 1 | 1 | 1 |
| precision | 1 | 1 | 2/3 | 3/4 | 3/5 | 4/6 | 4/7 | 4/8 |

- AP $= \frac14(1 + 1 + \frac34 + \frac46) = 41/48 = 0.854$.
- The trapezoid area from $(0, 1)$ is $401/480 = 0.835$.
- The 11-point interpolated AP is $(6 \cdot 1 + 2 \cdot \frac34 + 3 \cdot \frac23)/11 = 19/22 = 0.864$.

The same curve gives three values that differ in the second digit.

**Ties.** If the scores were $0.9, 0.9, 0.7, \ldots$ with the first two labels $+$ and $-$, the first point is $(R, P) = (1/4, 1/2)$; there is no point with precision 1, because no threshold takes one of the two tied examples without the other.

## Where it is used

- Information retrieval and search, where the collection is large and the relevant items are few.
- Detection tasks with rare positives: fraud, disease screening, defects, and object detection (where the mean of AP over classes, mAP, is the standard score).
- Multiclass and multilabel text classification, reported with micro and macro $F_1$.
- Choosing a threshold: the point on the PR curve that meets a required recall, or that maximizes $F_\beta$. Pick it on validation data or inside [cross-validation](/cross-validation/), not on the test set.

### Pitfalls

- **Which class is positive.** Precision and recall of class 1 and of class 0 are different numbers. Swapping the axes of the confusion matrix also swaps precision and recall.
- **Precision depends on the prevalence.** With the same true and false positive rates, precision falls when positives become rarer. A PR curve from a balanced test set does not transfer to a deployment with 1 percent positives; [ROC](/roc-auc/) rates do.
- **$F_1$ ignores true negatives** and weights precision and recall equally. If the costs of FP and FN are known, use them.
- **Averaged $F_1$ is not unique.** Micro, macro, weighted, the mean of per-class $F_1$ and $F_1$ of the means all differ, and so does the choice of 0 or 1 for $0/0$.
- **Linear interpolation of PR points** does not give an achievable curve, and its area can be too high or too low; see above.

## References
