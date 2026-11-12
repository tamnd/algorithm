---
tag: WPW65B
kind: definition
slug: confusion-matrix
name: Confusion matrix
aliases:
- error matrix
area: machine-learning/supervised-learning
level: intro
summary: "A k by k table whose entry (i, j) counts the examples of true class i predicted as class j. Accuracy, balanced accuracy, kappa and MCC are read from it."
prereqs: [classification]
see_also: [precision-and-recall, roc-auc, classification, multiclass-classification, cross-validation, normalized-mutual-information, adjusted-rand-index]
sources:
  - paper: doi:10.1177/001316446002000104
    title: Jacob Cohen, A coefficient of agreement for nominal scales, Educational and Psychological Measurement 20(1), 37-46, 1960
    locator: the coefficient kappa = (p_o - p_c) / (1 - p_c)
  - paper: doi:10.1016/0005-2795(75)90109-9
    title: B. W. Matthews, Comparison of the predicted and observed secondary structure of T4 phage lysozyme, Biochimica et Biophysica Acta 405(2), 442-451, 1975
    locator: the correlation coefficient C between predicted and observed binary assignments
  - paper: "Jan Gorodkin, Comparing two K-category assignments by a K-category correlation coefficient, Computational Biology and Chemistry 28(5-6), 367-374, 2004"
    locator: the K-category correlation coefficient R_K computed from a K by K confusion matrix
  - paper: "Kay H. Brodersen, Cheng Soon Ong, Klaas E. Stephan and Joachim M. Buhmann, The balanced accuracy and its posterior distribution, Proceedings of the 20th International Conference on Pattern Recognition, 3121-3124, 2010"
    locator: balanced accuracy as the mean of the per-class accuracies
  - paper: doi:10.1016/j.patrec.2005.10.010
    title: Tom Fawcett, An introduction to ROC analysis, Pattern Recognition Letters 27(8), 861-874, 2006
    locator: Figure 1 (the binary confusion matrix with the predicted class in rows and the true class in columns)
---

A confusion matrix of a classifier on a labeled set is the $k \times k$ table $C$ whose entry $C_{ij}$ counts the examples whose true class is $i$ and whose predicted class is $j$. The diagonal holds the correct predictions and each off-diagonal cell is one kind of error. The layout is a convention: this page and scikit-learn put the true labels in rows and the predicted labels in columns, but Fawcett (2006) and many texts use the transpose, so read the axis labels before you read the numbers. Accuracy, balanced accuracy, Cohen's kappa, the Matthews correlation coefficient and [precision and recall](/precision-and-recall/) are all functions of $C$.

## Definition

**The matrix.** Let the classes be $1, \ldots, k$ and let $(y_1, \hat y_1), \ldots, (y_n, \hat y_n)$ be true and predicted labels. Then

$$C_{ij} = \#\{\, t : y_t = i,\ \hat y_t = j \,\}, \qquad \sum_{i, j} C_{ij} = n.$$

Write $t_i = \sum_j C_{ij}$ for the number of true examples of class $i$ (the row sum, or support) and $p_j = \sum_i C_{ij}$ for the number of predictions of class $j$ (the column sum). scikit-learn's `confusion_matrix(y_true, y_pred)` uses this layout, with the classes in sorted order.

**The binary case.** With class 0 negative and class 1 positive, in this layout

$$C = \begin{pmatrix} \mathrm{TN} & \mathrm{FP} \\ \mathrm{FN} & \mathrm{TP} \end{pmatrix}.$$

A false positive (FP) is a negative predicted positive (a type I error); a false negative (FN) is a positive predicted negative (a type II error). For one class $j$ of a multiclass matrix, the one-vs-rest counts are $\mathrm{TP}_j = C_{jj}$, $\mathrm{FP}_j = p_j - C_{jj}$, $\mathrm{FN}_j = t_j - C_{jj}$ and $\mathrm{TN}_j = n - \mathrm{TP}_j - \mathrm{FP}_j - \mathrm{FN}_j$.

**Accuracy.** $\mathrm{acc} = \frac1n \sum_i C_{ii}$. It is 1 minus the empirical 0-1 risk.

**Balanced accuracy.** The mean of the per-class recalls,

$$\mathrm{bacc} = \frac{1}{\lvert K \rvert} \sum_{i \in K} \frac{C_{ii}}{t_i}, \qquad K = \{ i : t_i > 0 \}.$$

In the binary case it is $\frac12\big(\frac{\mathrm{TP}}{\mathrm{TP} + \mathrm{FN}} + \frac{\mathrm{TN}}{\mathrm{TN} + \mathrm{FP}}\big)$, the mean of sensitivity and specificity. A constant classifier scores $1/\lvert K \rvert$, whatever the class sizes.

**Cohen's kappa (Cohen 1960).** Let $p_o = \mathrm{acc}$ be the observed agreement and $p_e = \frac{1}{n^2}\sum_i t_i\, p_i$ the agreement expected if the true and the predicted labels were independent with the same margins. Then

$$\kappa = \frac{p_o - p_e}{1 - p_e}.$$

$\kappa = 1$ for perfect agreement, $\kappa = 0$ when the agreement equals the chance level, and $\kappa < 0$ below it. It is undefined when $p_e = 1$, which happens only when both labelings put every example in the same single class.

**Matthews correlation coefficient (Matthews 1975).** In the binary case

$$\mathrm{MCC} = \frac{\mathrm{TP}\cdot\mathrm{TN} - \mathrm{FP}\cdot\mathrm{FN}}{\sqrt{(\mathrm{TP} + \mathrm{FP})(\mathrm{TP} + \mathrm{FN})(\mathrm{TN} + \mathrm{FP})(\mathrm{TN} + \mathrm{FN})}},$$

the Pearson correlation of the true and the predicted 0/1 indicators. It lies in $[-1, 1]$. The multiclass form of Gorodkin (2004), with $c = \sum_i C_{ii}$ and $s = n$, is

$$\mathrm{MCC} = \frac{c\, s - \sum_j p_j t_j}{\sqrt{\big(s^2 - \sum_j p_j^2\big)\big(s^2 - \sum_j t_j^2\big)}}.$$

For $k = 2$ the numerator is $2(\mathrm{TP}\cdot\mathrm{TN} - \mathrm{FP}\cdot\mathrm{FN})$ and each factor under the root is twice a product of two margins, for example $s^2 - p_0^2 - p_1^2 = 2 p_0 p_1$ because $s = p_0 + p_1$. So the two forms agree. When a factor is 0 (all true labels equal, or all predictions equal) the ratio is $0/0$; scikit-learn returns 0 in that case, and this page does too.

**Symmetry.** Accuracy, $\kappa$ and MCC do not change when $C$ is transposed, so they do not depend on the layout. Balanced accuracy, precision and recall do: transposing $C$ turns the per-class recalls into the per-class precisions.

## Examples and non-examples

**Ninety-five negatives and five positives, all predicted negative.**

$$C = \begin{pmatrix} 95 & 0 \\ 5 & 0 \end{pmatrix}.$$

Accuracy is $0.95$, but balanced accuracy is $\frac12(1 + 0) = 0.5$. For kappa, $p_o = 0.95$ and $p_e = (95 \cdot 100 + 5 \cdot 0)/100^2 = 0.95$, so $\kappa = 0$. For MCC the factor $\mathrm{TP} + \mathrm{FP} = 0$, so the ratio is $0/0$ and the convention gives 0. Three of the four numbers say the classifier has learned nothing; accuracy does not.

**A useful binary classifier.** $\mathrm{TN} = 45$, $\mathrm{FP} = 5$, $\mathrm{FN} = 10$, $\mathrm{TP} = 40$. Then accuracy is $0.85$. The margins are $t = (50, 50)$ and $p = (55, 45)$, so $p_e = (50 \cdot 55 + 50 \cdot 45)/10^4 = 0.5$ and $\kappa = 0.35 / 0.5 = 0.7$. And $\mathrm{MCC} = (40 \cdot 45 - 5 \cdot 10)/\sqrt{45 \cdot 50 \cdot 50 \cdot 55} = 1750/2487.47 = 0.7035$.

**Three classes.** With classes cat, dog and bird,

| true \ predicted | cat | dog | bird | $t_i$ |
|---|---|---|---|---|
| cat | 8 | 1 | 1 | 10 |
| dog | 2 | 3 | 1 | 6 |
| bird | 0 | 1 | 3 | 4 |
| $p_j$ | 10 | 5 | 5 | 20 |

- Accuracy $= 14/20 = 0.7$.
- Recalls $0.8, 0.5, 0.75$, so balanced accuracy $= 41/60 = 0.6833$.
- $p_e = (10 \cdot 10 + 6 \cdot 5 + 4 \cdot 5)/400 = 0.375$, so $\kappa = (0.7 - 0.375)/0.625 = 0.52$.
- MCC $= (14 \cdot 20 - 150)/\sqrt{(400 - 150)(400 - 152)} = 130/\sqrt{62000} = 0.5221$.
- For dog against the rest: $\mathrm{TP} = 3$, $\mathrm{FP} = 5 - 3 = 2$, $\mathrm{FN} = 6 - 3 = 3$, $\mathrm{TN} = 12$.

**Non-example: the transposed table read with the wrong convention.** If the 2 by 2 table of the second example is printed in Fawcett's layout (predicted in rows), the cell in row 1, column 2 is $\mathrm{FN} = 10$, not $\mathrm{FP}$. Reading it with the scikit-learn convention swaps the false positives and the false negatives, and so swaps precision ($40/45$) and recall ($40/50$). Accuracy, $\kappa$ and MCC come out right by the symmetry above, which hides the mistake.

**Non-example: a contingency table between two clusterings.** A table that cross-counts two partitions of the same points has the same shape, but its rows and columns are not matched: cluster 3 of one partition has no reason to correspond to cluster 3 of the other. Its diagonal means nothing, and it is scored with permutation-invariant measures such as [normalized mutual information](/normalized-mutual-information/) and the [adjusted Rand index](/adjusted-rand-index/).

**Non-example: a multilabel prediction.** When each example can have several labels, a single $k \times k$ table cannot place an example with two true labels. Use one 2 by 2 matrix for each label instead.

## Related definitions

- [Precision and recall](/precision-and-recall/): $\mathrm{TP}/(\mathrm{TP} + \mathrm{FP})$ and $\mathrm{TP}/(\mathrm{TP} + \mathrm{FN})$, and their averages over the classes of a multiclass matrix.
- [ROC curve and AUC](/roc-auc/): the true positive rate $\mathrm{TP}/(\mathrm{TP} + \mathrm{FN})$ against the false positive rate $\mathrm{FP}/(\mathrm{FP} + \mathrm{TN})$ as the threshold of a score moves, one binary confusion matrix per threshold.
- [Classification](/classification/) and [multiclass classification](/multiclass-classification/): the tasks whose outputs the matrix summarizes.
- Specificity is $\mathrm{TN}/(\mathrm{TN} + \mathrm{FP})$, the recall of the negative class. Sensitivity is the recall of the positive class.
- [Cross-validation](/cross-validation/): summing the confusion matrices of the folds gives one matrix for the whole data set.

## References
