---
tag: MFR8P0
kind: problem
slug: feature-selection
name: Feature selection
aliases:
- variable selection
- attribute selection
- variable subset selection
area: machine-learning/dimensionality-reduction
level: core
summary: "Choose k of the d input features so that a model on them predicts well. Best subset selection for least squares is NP-hard, so filters, greedy wrappers and the lasso are used."
prereqs: [linear-regression, overfitting]
see_also: [lasso-regression, cross-validation, information-gain, orthogonal-matching-pursuit, principal-component-analysis, curse-of-dimensionality, np-hard, random-forest]
sources:
  - paper: "Isabelle Guyon and André Elisseeff, An introduction to variable and feature selection, Journal of Machine Learning Research 3, 2003"
    locator: pp. 1157 to 1182 (filters, wrappers and embedded methods, the examples of features that are useless alone but useful together)
  - paper: doi:10.1137/S0097539792240406
    title: B. K. Natarajan, Sparse approximate solutions to linear systems, SIAM Journal on Computing 24(2), 1995
    locator: pp. 227 to 234 (NP-hardness by reduction from exact cover by 3-sets, and a bound for greedy selection)
  - paper: doi:10.1016/S0004-3702(97)00043-X
    title: Ron Kohavi and George H. John, Wrappers for feature subset selection, Artificial Intelligence 97(1-2), 1997
    locator: pp. 273 to 324 (the wrapper approach, relevance and usefulness, search strategies)
  - paper: doi:10.1109/TPAMI.2005.159
    title: Hanchuan Peng, Fuhui Long and Chris Ding, Feature selection based on mutual information, criteria of max-dependency, max-relevance, and min-redundancy, IEEE Transactions on Pattern Analysis and Machine Intelligence 27(8), 2005
    locator: pp. 1226 to 1238 (the mRMR criterion, its link to maximum dependency, incremental search)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, 2nd edition, Springer, 2009
    locator: Section 3.3 (best subset, forward and backward stepwise selection) and Section 3.4 (shrinkage, the lasso)
  - paper: doi:10.1109/TC.1977.1674939
    title: Patrenahalli M. Narendra and Keinosuke Fukunaga, A branch and bound algorithm for feature subset selection, IEEE Transactions on Computers C-26(9), 1977
    locator: pp. 917 to 922 (exact search for a monotone criterion)
  - paper: doi:10.1111/j.2517-6161.1996.tb02080.x
    title: Robert Tibshirani, Regression shrinkage and selection via the lasso, Journal of the Royal Statistical Society Series B 58(1), 1996
    locator: pp. 267 to 288 (the l1 penalty sets coefficients to zero)
  - paper: "Abhimanyu Das and David Kempe, Submodular meets spectral, greedy algorithms for subset selection, sparse approximation and dictionary selection, Proceedings of the 28th International Conference on Machine Learning (ICML), 2011"
    locator: pp. 1057 to 1064 (approximation bounds for forward selection through the submodularity ratio)
---

Feature selection is the problem of choosing a subset $S$ of the $d$ input features, usually of a given size $k$, so that a model that sees only the features in $S$ predicts the target well. It differs from feature extraction, such as [principal component analysis](/principal-component-analysis/), because the result is a subset of the original measurements, not new combinations of them. Fewer features give models that are cheaper to measure and run, easier to read and less prone to [overfitting](/overfitting/). The exact problem for least squares, best subset selection, is [NP-hard](/np-hard/) (Natarajan 1995). Practical methods fall into three groups (Guyon and Elisseeff 2003): filters, which score features without a model; wrappers, which search over subsets using a model; and embedded methods, which select while they fit.

## In plain words

You want to predict something from many measurements, but many of them are useless or repeat each other. Feature selection keeps a few measurements and drops the rest.

Trying every possible group is the exact answer, but the number of groups grows too fast. So people use shortcuts. A filter gives each measurement a score, for example how much it tells about the target, and keeps the best ones. A wrapper adds or removes one measurement at a time and keeps the change that helps the model most. An embedded method trains a model that switches some measurements off by itself.

The shortcuts can fail. Two measurements can be useless alone and perfect together. A measurement can look best alone and still not belong to the best group.

## Definition

**Input.** A data matrix $X \in \mathbb{R}^{n \times d}$ with columns $x_1, \ldots, x_d$ (the features), a target $y$ of length $n$, and a budget $k \le d$.

**Output.** A subset $S \subseteq \{1, \ldots, d\}$ with $|S| = k$ that minimizes a criterion $J(S)$. For least squares, the standard criterion is the residual sum of squares
$$ J(S) = \mathrm{RSS}(S) = \min_{\beta \in \mathbb{R}^{|S|}} \lVert y - X_S \beta \rVert_2^2 , $$
where $X_S$ keeps the columns in $S$. This is **best subset selection**. Its penalized form is $\min_\beta \lVert y - X \beta \rVert_2^2 + \lambda \lVert \beta \rVert_0$, where $\lVert \beta \rVert_0$ counts the nonzero entries. In general $J(S)$ is the estimated error of a chosen learner trained on $X_S$, for example its [cross-validation](/cross-validation/) error.

**Decision version.** Given $X$, $y$, $k$ and $\varepsilon \ge 0$, is there an $S$ with $|S| \le k$ and $\mathrm{RSS}(S) \le \varepsilon$? This is also called the sparse approximate solution problem for the linear system $X \beta = y$.

## Variants

- **Filter methods** score each feature, or each small group, with a statistic that does not depend on the final model: correlation with the target, [information gain](/information-gain/) or mutual information, a $\chi^2$ test, or the Relief weight. They are fast but blind to interactions.
- **Wrapper methods** search over subsets and score each subset by training the model (Kohavi and John 1997). Forward stepwise selection, backward elimination, floating search and genetic search are wrappers.
- **Embedded methods** select during training: the [lasso](/lasso-regression/) sets coefficients to exactly zero, decision trees use only the features on which they split, and recursive feature elimination drops the features with the smallest weights.
- **Fixed size or penalized.** Either $k$ is given, or a penalty such as AIC, BIC or Mallows' $C_p$ trades fit for size, or $k$ is chosen by cross-validation.
- **Unsupervised selection** keeps features that preserve structure such as variance or cluster separation, with no target.
- **Supervised versus unsupervised relevance.** Kohavi and John separate strongly relevant features (removing one alone changes the conditional distribution of the target), weakly relevant features (they can help in some subsets) and irrelevant ones, and point out that the optimal subset for a given learner need not contain all relevant features.

## Examples

**Greedy is not optimal.** Take least squares with no intercept on three samples:

| sample | $x_1$ | $x_2$ | $x_3$ | $y$ |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 0 | 1 | 1 | 1 |
| 3 | 0 | 0 | 1 | 0 |

Here $y = x_1 + x_2$ exactly. Alone, $\mathrm{RSS}(\{1\}) = \mathrm{RSS}(\{2\}) = 1$ but $\mathrm{RSS}(\{3\}) = 2/3$, because $x_3$ points closer to $y$. Forward stepwise selection with $k = 2$ takes $x_3$ first and then $x_1$, with $\mathrm{RSS}(\{1, 3\}) = 1/2$. The best pair is $\{1, 2\}$ with $\mathrm{RSS} = 0$. Backward elimination from all three features drops $x_3$ and finds the optimum here, but it fails on other instances.

**Useless alone, useful together.** Let $x_1$ and $x_2$ be independent fair bits and $y = x_1 \oplus x_2$. Each feature alone has mutual information 0 with $y$, so every filter that scores single features ranks them as noise. Together they determine $y$ (1 bit).

**Redundancy.** Let $a$ and $b$ be independent fair bits on 16 samples, $y = 2a + b$ (four classes), and offer four features: $a$, an exact copy of $a$, a noisy copy of $b$ with a quarter of its values flipped, and pure noise. Their mutual information with $y$ is 1, 1, 0.189 and 0 bits. Ranking by relevance alone keeps $a$ and its copy, which together still carry 1 bit. The mRMR rule picks $a$, then scores the copy $1 - 1 = 0$ and the noisy $b$ $0.189 - 0 = 0.189$, so it takes the noisy $b$. That pair carries 1.189 bits about $y$.

## Known algorithms

| algorithm | type | cost (model fits) | guarantee |
| --- | --- | --- | --- |
| Exhaustive best subset | wrapper, exact | $\binom{d}{k}$, or $2^d$ for all sizes | optimal |
| Branch and bound (Narendra and Fukunaga 1977), leaps and bounds | exact | exponential in the worst case, often much less | optimal for a monotone criterion such as RSS |
| Mixed-integer optimization | exact | exponential in the worst case | optimal, with a certificate |
| Forward stepwise selection | wrapper, greedy | $O(k d)$ | optimal for orthogonal columns; approximation bounds from the submodularity ratio (Das and Kempe 2011) |
| Backward elimination | wrapper, greedy | $O(d^2)$ | none in general |
| [Orthogonal matching pursuit](/orthogonal-matching-pursuit/) | greedy | $k$ steps | recovers the true support under coherence or RIP conditions |
| Lasso | embedded, convex | one convex program per $\lambda$ | recovers the true support under irrepresentability conditions |
| mRMR (Peng, Long and Ding 2005) | filter, greedy | $O(k d)$ mutual information estimates | none in general |
| Univariate filters (correlation, information gain, $\chi^2$) | filter | $d$ scores | none; misses interactions |
| Impurity or permutation importance of a [random forest](/random-forest/) | embedded | one forest | none in general |

Forward stepwise selection starts from $S = \emptyset$ and, for $t = 1, \ldots, k$, adds the feature $j \notin S$ that minimizes $\mathrm{RSS}(S \cup \{j\})$. With a QR factorization of $X_S$ updated one column at a time, one step costs $O(n d)$, so the whole path costs $O(n d k)$. It is a [greedy algorithm](/greedy-algorithm/) and the first example above shows that it can miss the optimum.

mRMR with the difference criterion picks the most relevant feature first, and then the feature $j$ that maximizes
$$ I(x_j; y) - \frac{1}{|S|} \sum_{s \in S} I(x_j; x_s) , $$
relevance minus mean redundancy with the features already chosen. Peng, Long and Ding show that, for first-order incremental search, this is equivalent to maximizing the dependency $I(x_S; y)$, which is too hard to estimate directly.

## Bounds

- **Hardness.** Best subset selection for least squares is NP-hard (Natarajan 1995). The proof is the reduction below. The hardness holds even for $\varepsilon = 0$, so it does not come from numerical issues.
- **Exhaustive search** needs $\binom{d}{k}$ least squares fits of cost $O(n k^2)$ each. This is practical up to about $d = 30$ to $40$ with branch and bound or leaps and bounds, and much further with modern mixed-integer solvers on well-conditioned data.
- **Greedy guarantees.** For orthogonal columns, $\mathrm{RSS}(S) = \lVert y \rVert^2 - \sum_{j \in S} (x_j^{\top} y)^2 / \lVert x_j \rVert^2$ is additive in the features, so forward selection is optimal. Natarajan bounds the size of the subset found by greedy selection in terms of the conditioning of the matrix. Das and Kempe bound the $R^2$ of the forward selection subset by a factor $1 - e^{-\gamma}$ of the optimum, where $\gamma$ is the submodularity ratio of the data.
- **Statistics.** With many candidate subsets, the best training error is biased down. Selection must be validated on data not used for the search, or the model error is underestimated.

## Reductions

**From exact cover by 3-sets.** An instance of [exact cover by 3-sets](/exact-cover-by-3-sets/) has a universe of $3q$ elements and a family of 3-element subsets $C_1, \ldots, C_d$. Build $X \in \{0, 1\}^{3q \times d}$ whose column $j$ is the indicator vector of $C_j$, and let $y$ be the all-ones vector. If $q$ sets form an exact cover, the sum of their columns is $y$, so $\mathrm{RSS} = 0$ with $k = q$ features. Conversely, if $X_S \beta = y$ with $|S| \le q$, the columns in $S$ have at most $3|S| \le 3q$ nonzero rows between them, and all $3q$ rows of $y$ are nonzero. So $|S| = q$, the sets in $S$ are pairwise disjoint and cover the universe, and they form an exact cover. Hence deciding whether $\mathrm{RSS}(S) = 0$ for some $|S| \le k$ is NP-hard.

**To sparse recovery.** Best subset selection with the $\ell_0$ penalty is the noisy form of finding the sparsest solution of a linear system, the problem of [compressed sensing](/compressed-sensing/). Results there say when convex relaxation (the lasso, basis pursuit) or greedy pursuit recovers the same support.

**Relation to extraction.** Feature selection restricts the linear map of feature extraction to a coordinate projection. Any selection method gives an extraction method, but PCA and its relatives cannot report which original measurements matter.

## Applications

- **Genomics and proteomics.** Expression data have tens of thousands of genes and a few hundred samples. Selection gives small marker panels that can be measured cheaply.
- **Text classification.** Vocabularies are large, and filters such as information gain or $\chi^2$ cut them to the useful terms before training.
- **Interpretable models** in credit scoring, medicine and science, where a short list of inputs must be explained.
- **Reducing measurement cost** when each feature needs a sensor or a laboratory test.
- **Fighting the [curse of dimensionality](/curse-of-dimensionality/)** for distance-based learners such as [k-nearest neighbors](/k-nearest-neighbors/), whose accuracy drops when many irrelevant features dilute the distances.

## References
