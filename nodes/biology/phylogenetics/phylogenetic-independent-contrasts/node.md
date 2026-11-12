---
tag: VXSG4E
kind: technique
slug: phylogenetic-independent-contrasts
name: Phylogenetic independent contrasts
aliases:
- independent contrasts
- PIC
- Felsenstein's contrasts
area: biology/phylogenetics
level: advanced
summary: Turn the trait values of n species on a tree into n - 1 contrasts that are independent under Brownian motion, so standard statistics apply.
prereqs: [phylogenetic-tree, variance, postorder-traversal]
see_also: [ordinary-least-squares, least-squares-problem, covariance-matrix, maximum-likelihood-estimation, stochastic-differential-equation, phylogenetic-likelihood, phylogenetic-diversity, felsenstein-pruning]
sources:
  - paper: doi:10.1086/284325
    title: Joseph Felsenstein, Phylogenies and the comparative method, American Naturalist 125(1), 1985
    locator: pp. 1-15 (the contrast algorithm, the lengthening of branches, and the problem of non-independent species)
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 23 (Brownian motion) and Chapter 25 (comparative methods)
  - paper: doi:10.1093/sysbio/41.1.18
    title: Theodore Garland Jr., Paul H. Harvey and Anthony R. Ives, Procedures for the analysis of comparative data using phylogenetically independent contrasts, Systematic Biology 41(1), 1992
    locator: pp. 18-32 (standardization checks, branch length transforms, and regression through the origin)
  - paper: doi:10.1086/303327
    title: Theodore Garland Jr. and Anthony R. Ives, Using the past to predict the present, confidence intervals for regression equations in phylogenetic comparative methods, American Naturalist 155(3), 2000
    locator: pp. 346-364 (the equivalence of contrasts and generalized least squares)
  - paper: doi:10.1093/sysbio/42.4.569
    title: Andy Purvis and Theodore Garland Jr., Polytomies in comparative analyses of continuous characters, Systematic Biology 42(4), 1993
    locator: pp. 569-575 (contrasts on trees with polytomies)
---

Phylogenetic independent contrasts (PIC) is Felsenstein's 1985 method for the statistics of trait values measured on related species. Species are not independent data points, because close relatives share much of their history. Under a Brownian motion model of trait evolution on a known rooted binary [phylogenetic tree](/phylogenetic-tree/), the method turns the $n$ tip values into $n - 1$ differences between sister nodes, the *contrasts*, which are independent normal variables with known [variances](/variance/). After division by their standard deviations they are independent and identically distributed, so correlation and regression through the origin apply to them. One [postorder traversal](/postorder-traversal/) computes them in $O(n)$ time.

## In plain words

Suppose we want to know if larger mammals have larger home ranges. We measure 40 species and plot one trait against the other. But 20 of the species may be close relatives of one large ancestor, and 20 of one small ancestor. Then the plot shows a strong trend even if only one real change happened, at the split between the two groups.

The contrast method looks at changes, not at species. For each pair of sister groups on the tree, it takes the difference of their trait values. Each difference comes from evolution after their split, separate from the other differences. Long branches give room for larger differences, so the method scales each difference by the time since the split.

The scaled differences behave like independent samples, and the usual tests can use them.

## When it applies

- The traits are continuous, such as log body mass, and the question is about how traits change together across species.
- A rooted tree with branch lengths is known, and it is binary or its polytomies are handled as described below.
- Each trait evolves as Brownian motion on the tree: along a branch of length $v$ the change is normal with mean 0 and variance $\sigma^2 v$, independent of other branches. Then the tip values are multivariate normal with covariance $\sigma^2 C$, where $C_{st}$ is the length of the shared part of the root paths of tips $s$ and $t$.
- The analysis is a correlation, a regression, or an estimate of the rate $\sigma^2$ or of the root value. For other models of evolution, such as Ornstein-Uhlenbeck, use generalized least squares with the model covariance instead.

## The template

Each node $k$ carries a value $x_k$ and a branch length $v_k$ above it. Tips start with their measured values and their branch lengths.

```pseudo id=main
CONTRASTS(T, x)
L1  for each internal node k, in postorder, with children i and j do
L2      c_k ← x_i − x_j                                  ▷ the raw contrast
L3      s_k ← c_k / sqrt(v_i + v_j)                      ▷ the standardized contrast
L4      x_k ← (x_i / v_i + x_j / v_j) / (1 / v_i + 1 / v_j)
L5      v_k ← v_k + v_i v_j / (v_i + v_j)                ▷ lengthen the branch above k
L6  return s for the n − 1 internal nodes, and x at the root
```

**Why the contrasts are independent.** Take two sister tips $i$ and $j$ below node $k$, with true value $X_k$ at $k$. Then $x_i = X_k + e_i$ and $x_j = X_k + e_j$ with independent errors of variances $\sigma^2 v_i$ and $\sigma^2 v_j$.

- The contrast $c_k = e_i - e_j$ does not depend on $X_k$, and it has variance $\sigma^2 (v_i + v_j)$.
- The weighted mean $x_k = X_k + (e_i/v_i + e_j/v_j)/(1/v_i + 1/v_j)$ has error variance $\sigma^2 v_i v_j/(v_i + v_j)$.
- The covariance of $e_i - e_j$ with $e_i/v_i + e_j/v_j$ is $\sigma^2 (v_i / v_i - v_j / v_j) = 0$, and the variables are jointly normal, so $c_k$ is independent of $x_k$.

So, for everything above $k$, the pair $i, j$ acts like one tip with value $x_k$ at the end of a branch lengthened by $v_i v_j/(v_i + v_j)$. Removing $i$ and $j$ and repeating gives $n - 1$ contrasts, each independent of all later ones, by induction on the number of tips.

**What the outputs are.**

- The root value $x_{\text{root}}$ is the generalized least squares (and maximum likelihood) estimate of the root state, $\hat{x}_0 = \mathbf{1}^\top C^{-1} x \,/\, \mathbf{1}^\top C^{-1} \mathbf{1}$, and its variance is $\sigma^2 v_i v_j/(v_i + v_j)$ for the two children of the root.
- $\sum_k s_k^2 = (x - \hat{x}_0 \mathbf{1})^\top C^{-1} (x - \hat{x}_0 \mathbf{1})$, so $\hat\sigma^2 = \frac{1}{n-1}\sum_k s_k^2$ is the restricted maximum likelihood estimate of the rate.
- For two traits, the slope of the standardized contrasts of $y$ on those of $x$, fitted through the origin, equals the generalized least squares slope of $y$ on $x$ with covariance $C$ (Garland and Ives 2000).

The work is $O(1)$ per node, so $O(n)$ in total, against $O(n^3)$ for a direct [least squares](/least-squares-problem/) solve with the $n \times n$ matrix $C$.

## Classic examples

**A worked tree.** Take $((A{:}1, B{:}3){:}1, (C{:}1, D{:}1){:}2)$ with trait values $A = 10$, $B = 14$, $C = 6$, $D = 8$.

| node | children | raw contrast | variance $v_i + v_j$ | standardized | node value | lengthened branch |
|---|---|---|---|---|---|---|
| $AB$ | $A, B$ | $10 - 14 = -4$ | $1 + 3 = 4$ | $-2$ | $\frac{10/1 + 14/3}{1 + 1/3} = 11$ | $1 + \frac{3}{4} = 1.75$ |
| $CD$ | $C, D$ | $6 - 8 = -2$ | $1 + 1 = 2$ | $-1.414$ | $7$ | $2 + \frac12 = 2.5$ |
| root | $AB, CD$ | $11 - 7 = 4$ | $1.75 + 2.5 = 4.25$ | $1.940$ | $\frac{159}{17} \approx 9.353$ | |

The root estimate has variance $1.75 \cdot 2.5 / 4.25 = 35/34 \approx 1.029$ (per unit of $\sigma^2$). The value at $AB$ is closer to $A$ than to $B$, because $A$ sits on the shorter branch. The estimate of the rate is $\hat\sigma^2 = (4 + 2 + 3.765)/3 \approx 3.255$.

**Two traits.** A second trait with values $3, 5, 1, 2$ on the same tips gives the contrasts $-2$, $-1$ and $2$, exactly half of those of the first trait, so the slope through the origin is $0.5$.

**Two clades.** Felsenstein's 1985 example: two clades, each with many species on short branches below a long stem. A plot of the tip values can show a strong correlation, but the tree holds only one contrast between the clades, at the root. The contrasts inside the clades carry the evidence on whether the traits change together, and a tip-based test that ignores the tree gives far too many false positives.

## Variations

- **Polytomies.** A node with more than two children can be resolved into a binary tree with zero-length branches, and the test then uses fewer degrees of freedom (Purvis and Garland 1993).
- **Branch length transforms.** When the standardized contrasts still depend on their standard deviations, transforms of the branch lengths (for example a logarithm or a power) can make the Brownian model fit better (Garland, Harvey and Ives 1992).
- **Several traits.** Each trait gets its own contrasts on the same tree. Correlations and multiple regressions through the origin then use the contrasts as the data.
- **Fast likelihood.** The same pass computes the likelihood of the tips under Brownian motion, since it is a product of normal densities of the contrasts and of the root term. Related linear-time algorithms evaluate likelihoods for other Gaussian models on trees.
- **Generalized least squares.** Phylogenetic generalized least squares uses $C$, or a model covariance, directly. It gives the same estimates as contrasts under Brownian motion and extends to other models and to designs with an intercept.

## Pitfalls

- **The sign of a contrast is arbitrary.** Swapping the two children flips $c_k$. So a regression of contrasts must pass through the origin. For plots, the usual choice is to make each contrast of $x$ positive and flip the matching contrast of $y$ with it.
- **Branch lengths matter.** Wrong lengths give contrasts with unequal variances. A check: the absolute standardized contrasts should not correlate with their standard deviations.
- **Zero branch lengths.** Two sister tips on zero-length branches divide by zero. Give such branches a small positive length, or merge the tips.
- **Node values are not full reconstructions.** The value $x_k$ at an internal node uses only the tips below $k$. Only the root value uses all the data. For ancestral states at other nodes, reroot or use the full model.
- **The model is an assumption.** Selection toward an optimum, trends, or jumps break the Brownian model, and the contrasts are then not independent.
- **Errors in the tree.** A wrong topology also changes the contrasts, so a result that depends on one uncertain split is weak.

## Exercises

1. For two sister tips with branch lengths $v_i$ and $v_j$, show that the weight on $x_i$ in the node value is $v_j / (v_i + v_j)$, and explain why the shorter branch gets the larger weight.
2. On a star tree with $n$ tips on branches of length 1, resolved into any binary tree with zero-length internal branches, compute the root estimate and show that it is the mean of the tips.
3. Show that the slope of the standardized contrasts of $y$ on those of $x$ through the origin does not change when each pair $(c^x_k, c^y_k)$ is multiplied by $-1$, and explain why an intercept would change.
4. Show that the root estimate does not depend on the order in which the postorder pass visits the children of each node.

## References
