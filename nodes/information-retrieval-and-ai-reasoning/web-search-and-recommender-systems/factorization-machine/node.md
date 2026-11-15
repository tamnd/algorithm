---
tag: WQQ5T1
kind: model
slug: factorization-machine
name: Factorization machine
aliases:
- FM model
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: A regression model whose pairwise feature interactions use dot products of learned factor vectors, computed in time linear in the features.
prereqs: [linear-regression, matrix-factorization-recommendation]
see_also: [support-vector-machine, svd-plus-plus, logistic-regression, stochastic-gradient-descent, bayesian-personalized-ranking, cold-start-problem, hybrid-recommender, matrix-completion]
sources:
  - paper: doi:10.1109/ICDM.2010.127
    title: Steffen Rendle, Factorization machines, Proceedings of the 10th IEEE International Conference on Data Mining (ICDM 2010)
    locator: Section III-A (Equations 1 to 3, the model; Lemma 3.1, the O(k n) form), Section III-C (Equation 4, the gradient), Section III-D (Equation 5, the d-way model), Section IV (comparison with polynomial SVMs under sparsity, Figure 2), Section V (matrix factorization, SVD++, PITF and FPMC as special cases, Figure 3)
---

A factorization machine (FM) is a predictor for real-valued feature vectors that adds to a linear model a weight for every pair of features, and gives that weight as the dot product of two learned vectors, one per feature. Rendle (2010) introduced it to bring the idea of [matrix factorization](/matrix-factorization-recommendation/) to general feature vectors. Because each feature has its own factor vector, the model can estimate the interaction of two features that never occur together in training, which a model with an independent weight per pair, such as an [SVM](/support-vector-machine/) with a polynomial kernel, cannot do. With one-hot user and item features it is exactly biased matrix factorization, and with other features it reproduces models such as [SVD++](/svd-plus-plus/). The pairwise term looks like it needs $O(k n^2)$ work, but an algebraic identity brings it to $O(k n)$, and to $O(k\, m(x))$ for a vector with $m(x)$ nonzero entries. How well it predicts is measured on data, never proved.

## The machine

**Model (Rendle 2010, Equations 1 to 3).** For a feature vector $x \in \mathbb R^n$, a factorization machine of degree 2 predicts

$$\hat y(x) = w_0 + \sum_{i=1}^{n} w_i x_i + \sum_{i=1}^{n} \sum_{j=i+1}^{n} \langle v_i, v_j \rangle\, x_i x_j, \qquad \langle v_i, v_j \rangle = \sum_{f=1}^{k} v_{i,f}\, v_{j,f},$$

with parameters $w_0 \in \mathbb R$, $w \in \mathbb R^n$ and $V \in \mathbb R^{n \times k}$, whose row $v_i$ is the factor vector of feature $i$. The number of factors $k$ is a hyperparameter. The prediction is used directly for regression, through its sign or a logistic link for classification, and as a score for ranking (Section III-B); the losses are squared error, hinge, logistic or a pairwise ranking loss, usually with L2 regularization.

**Expressiveness (Section III-A2).** Every positive semidefinite matrix $W$ is $V V^\top$ for some $V$ when $k$ is large enough, so with large $k$ the model can represent any such matrix of pair weights. The point of a small $k$ is the opposite: it forces the pair weights to share structure, which is what lets them be estimated from sparse data.

**Input encoding.** In the recommender setting a training case is a user, an item and perhaps other context, each written as a block of indicator features. Rendle's Figure 1 uses a block for the user, one for the item, one for the other items the user rated, one for the time, and one for the item rated last.

**Degree $d$ (Section III-D, Equation 5).** The model extends to interactions of up to $d$ features, with one factor matrix $V^{(l)} \in \mathbb R^{n \times k_l}$ per order $l$ and a weight for $\{i_1, \dots, i_l\}$ given by $\sum_f \prod_{t} v^{(l)}_{i_t, f}$. The direct cost is $O(k_d\, n^d)$, and the paper states that the same argument as for $d = 2$ gives linear time.

## What it counts

**The linear-time identity (Lemma 3.1).** For each factor $f$,

$$\sum_{i=1}^{n} \sum_{j=i+1}^{n} v_{i,f} v_{j,f}\, x_i x_j = \frac12 \Bigl[\Bigl(\sum_{i=1}^{n} v_{i,f} x_i\Bigr)^2 - \sum_{i=1}^{n} v_{i,f}^2 x_i^2\Bigr].$$

*Proof.* Expand the square: $(\sum_i a_i)^2 = \sum_i a_i^2 + 2 \sum_{i < j} a_i a_j$ with $a_i = v_{i,f} x_i$. Subtract $\sum_i a_i^2$ and halve. Summing over $f$ gives the pairwise term of the model. $\square$

The right side takes $O(n)$ operations per factor, so a prediction costs $O(k n)$ instead of $O(k n^2)$. Only nonzero $x_i$ contribute to either sum, so the cost is $O(k\, m(x))$ for a sparse vector; for user and item indicators alone, $m(x) = 2$. The identity is exact in real arithmetic; in floating point the subtraction can lose digits when the two terms are large and close.

**Gradient (Section III-C, Equation 4).** With $s_f = \sum_j v_{j,f} x_j$,

$$\frac{\partial \hat y}{\partial w_0} = 1, \qquad \frac{\partial \hat y}{\partial w_i} = x_i, \qquad \frac{\partial \hat y}{\partial v_{i,f}} = x_i s_f - v_{i,f} x_i^2 .$$

The sums $s_f$ are already computed for the prediction, so each partial derivative costs $O(1)$ and one [stochastic gradient](/stochastic-gradient-descent/) step on a case costs $O(k\, m(x))$. The objective is not convex in $V$, so gradient methods give no guarantee of a global optimum.

**Parameters.** $1 + n + k n$, linear in $n$, against $1 + n + n(n - 1)/2$ for independent pair weights.

**A small example.** Take $n = 3$, $k = 1$, $x = (1, 2, 3)$ and $v = (1, -1, 2)$. The double sum is $v_1 v_2 x_1 x_2 + v_1 v_3 x_1 x_3 + v_2 v_3 x_2 x_3 = -2 + 6 - 12 = -8$. With the identity, $s = 1 - 2 + 6 = 5$ and $\sum_i v_i^2 x_i^2 = 1 + 4 + 36 = 41$, so the term is $\tfrac12 (25 - 41) = -8$, the same value.

## Relation to other models

- **Linear and logistic regression.** With $k = 0$ the model is [linear regression](/linear-regression/), or [logistic regression](/logistic-regression/) with a logistic link and log loss.
- **Polynomial SVM (Section IV).** An SVM with kernel $(\langle x, z \rangle + 1)^2$ has the same form with an independent weight $w_{i,j}$ per pair. With one user and one item indicator per case, a pair $(u, i)$ in the test set usually has no training case, so its weight stays 0 and the polynomial SVM falls back to user and item biases (Section IV-B). The FM weight $\langle v_u, v_i \rangle$ is learned from other pairs that share $u$ or $i$. Rendle also notes that FMs are trained in the primal and their predictions do not depend on stored support vectors.
- **Biased matrix factorization (Section V-A, Equation 12).** With $x$ the indicators of user $u$ and item $i$, the prediction is $w_0 + w_u + w_i + \langle v_u, v_i \rangle$, which is biased matrix factorization. With more than two categorical variables it is a nested parallel factor analysis (PARAFAC) model.
- **SVD++ (Section V-B).** Adding the indicators of the set $N_u$ of items the user rated, each scaled by $1 / \sqrt{|N_u|}$, gives the SVD++ prediction plus extra terms: biases for the items in $N_u$, their interactions with the user, and interactions between pairs of them.
- **PITF and FPMC (Sections V-C and V-D).** With user, item and tag indicators and a pairwise ranking loss, the FM is the PITF tag model except for a tag bias and shared tag factors. With the user's previous basket as features it is close to factorized personalized Markov chains for next-basket prediction, a sequential model related to [session-based recommendation](/session-based-recommendation/).
- **Ranking.** For ranking, the paper trains on pairs of cases with a pairwise classification loss (Section III-B). The pairwise loss of [Bayesian personalized ranking](/bayesian-personalized-ranking/) is one such loss, and the PITF comparison uses pairwise ranking.
- **Side information.** Because user and item attributes are just more features, an FM can score users or items with few interactions from their attributes, which is one approach to the [cold-start problem](/cold-start-problem/) and a form of [hybrid recommender](/hybrid-recommender/).
- **Later variants.** Field-aware factorization machines give each feature one factor vector per field of the other feature. Models such as DeepFM combine an FM with a neural network. Higher-order FMs use the degree-$d$ form.

## Known results in the model

These are measurements reported in the paper, not theorems.

- **Netflix (Figure 2).** On the Netflix rating data with user and item indicators, the paper plots test RMSE against $k$ for FMs and SVMs and reports that FMs estimate the pairwise interactions where SVMs fail.
- **Tag recommendation (Figure 3).** On Task 2 of the ECML/PKDD Discovery Challenge 2009, an FM reached a quality (F1 at top 5) comparable to the winning PITF model at the same number of parameters.

The linear-time identity and the special cases above are exact algebra. Whether the factorized pair weights help on a given data set is measured, not proved.

## References
