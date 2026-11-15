---
tag: XH65PN
kind: model
slug: probabilistic-matrix-factorization
name: Probabilistic matrix factorization
aliases:
- PMF
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: Models ratings as Gaussian noise around the dot product of user and item factors with Gaussian priors, so MAP estimation is regularized MF.
prereqs: [matrix-factorization-recommendation, maximum-a-posteriori-estimation]
see_also: [matrix-completion, rating-matrix, alternating-least-squares, ridge-regression, bayesian-inference, gibbs-sampling, svd-plus-plus, singular-value-decomposition]
sources:
  - url: https://papers.nips.cc/paper/2007/hash/d7322ed717dedf1eb4e6e52a37ea7bcd-Abstract.html
    title: Ruslan Salakhutdinov and Andriy Mnih, Probabilistic matrix factorization, Advances in Neural Information Processing Systems 20 (NIPS 2007)
    locator: Section 2, Equations 1 to 5 (the likelihood, the priors, the log posterior and the regularized objective with lambda_U = sigma^2 / sigma_U^2); Section 3, Equation 6 (adaptive priors); Section 4, Equation 7 (constrained PMF); Section 5 (Netflix results)
---

Probabilistic matrix factorization (PMF) is a statistical model for a partly observed table of ratings. Each user $i$ and each item $j$ has a hidden vector of $D$ factors, $U_i$ and $V_j$. Each observed rating is the dot product $U_i^\top V_j$ plus Gaussian noise, and the factor vectors have zero-mean Gaussian priors. Salakhutdinov and Mnih (2007) introduced it to give [matrix factorization](/matrix-factorization-recommendation/) for ratings a probabilistic reading. The main fact about the model is that its [maximum a posteriori](/maximum-a-posteriori-estimation/) estimate is the minimizer of squared error on the observed ratings plus Frobenius norm penalties on the factors, which is the usual regularized matrix factorization. So the model explains the penalty weights as ratios of variances, and it opens the way to choosing them from data and to fully Bayesian treatments. How well a fitted model predicts ratings is measured on held-out data, never proved.

## The machine

Let there be $N$ users, $M$ items and ratings in $\{1, \dots, K\}$. Let $R$ be the $N \times M$ [rating matrix](/rating-matrix/), with $I_{ij} = 1$ if user $i$ rated item $j$ and $I_{ij} = 0$ otherwise. The parameters are a $D \times N$ matrix $U$ and a $D \times M$ matrix $V$, with columns $U_i$ and $V_j$. The model is (Salakhutdinov and Mnih 2007, Section 2):

**Likelihood (Equation 1).** The observed ratings are independent given the factors, with

$$p(R \mid U, V, \sigma^2) = \prod_{i=1}^{N} \prod_{j=1}^{M} \bigl[\mathcal N(R_{ij} \mid U_i^\top V_j, \sigma^2)\bigr]^{I_{ij}} .$$

Missing entries contribute nothing, which is the same as assuming that they are missing at random.

**Priors (Equation 2).** The factor vectors are independent with spherical Gaussian priors, $p(U \mid \sigma_U^2) = \prod_i \mathcal N(U_i \mid 0, \sigma_U^2 I)$ and $p(V \mid \sigma_V^2) = \prod_j \mathcal N(V_j \mid 0, \sigma_V^2 I)$.

**Posterior (Equation 3).** By [Bayes' theorem](/bayes-theorem/), $\ln p(U, V \mid R, \sigma^2, \sigma_U^2, \sigma_V^2)$ equals

$$-\frac{1}{2\sigma^2} \sum_{i,j} I_{ij} (R_{ij} - U_i^\top V_j)^2 - \frac{1}{2\sigma_U^2} \sum_i \lVert U_i \rVert^2 - \frac{1}{2\sigma_V^2} \sum_j \lVert V_j \rVert^2$$

plus terms that depend on the variances and the counts but not on $U$ or $V$.

**Bounded variant (Equation 5).** In their experiments the authors pass the dot product through the logistic function $g(x) = 1 / (1 + e^{-x})$, so the mean is $g(U_i^\top V_j)$, and they map the ratings to $[0, 1]$ by $t(x) = (x - 1) / (K - 1)$. This keeps predictions in the range of valid ratings.

## What it counts

**MAP estimation is regularized matrix factorization.** Multiply the log posterior by $-\sigma^2$. Maximizing it over $U$ and $V$, with the variances fixed, is the same as minimizing (Equation 4)

$$E(U, V) = \frac12 \sum_{i=1}^{N} \sum_{j=1}^{M} I_{ij} (R_{ij} - U_i^\top V_j)^2 + \frac{\lambda_U}{2} \sum_{i=1}^{N} \lVert U_i \rVert^2 + \frac{\lambda_V}{2} \sum_{j=1}^{M} \lVert V_j \rVert^2, \qquad \lambda_U = \frac{\sigma^2}{\sigma_U^2}, \ \lambda_V = \frac{\sigma^2}{\sigma_V^2} .$$

A strong prior (small $\sigma_U^2$) or noisy ratings (large $\sigma^2$) give a large penalty. The step is exact: the two objectives differ by a positive factor and a constant.

**Cost.** One evaluation of $E$ or of its gradient takes $O(D)$ work per observed rating plus $O(D)$ per user and per item, so $O(D (|\Omega| + N + M))$ in total, where $|\Omega| = \sum_{i,j} I_{ij}$. The authors note that steepest descent takes time linear in the number of observations, and that one sweep through the Netflix data with 30 factors took under an hour in Matlab (Section 2). In Section 5 they train with mini-batches of 100,000 ratings and momentum.

**What it does not give.** $E$ is not convex in $(U, V)$ jointly, so gradient descent and [alternating least squares](/alternating-least-squares/) find a local minimum, not a guaranteed global one. The MAP estimate is a point estimate; it does not use the posterior spread.

**A small example.** Take $D = 1$, one item with $V_1 = 2$ held fixed, and one user who rated it $R_{11} = 4$. The terms of $E$ that involve $U_1$ are $\tfrac12 (4 - 2 U_1)^2 + \tfrac{\lambda_U}{2} U_1^2$. The derivative is $-2(4 - 2 U_1) + \lambda_U U_1$, which is zero at $U_1 = 8 / (4 + \lambda_U)$. With $\lambda_U = 0$ (a flat prior) the prediction $2 U_1$ is $4$, the observed rating. With $\lambda_U = 4$ it is $U_1 = 1$ and the prediction is $2$: the prior pulls the factor toward 0. This one-user step is [ridge regression](/ridge-regression/), which is why alternating least squares on $E$ solves a ridge problem per user and per item.

## Relation to other models

- **Singular value decomposition.** If every rating is observed and $\sigma_U^2, \sigma_V^2 \to \infty$, the penalties vanish and $E$ is the squared error of a rank-$D$ approximation, which the truncated [singular value decomposition](/singular-value-decomposition/) minimizes (Section 2). With missing entries, no such closed form is known, and the problem is hard in general (see [matrix completion](/matrix-completion/)).
- **Adaptive priors (Section 3, Equation 6).** Put priors on the hyperparameters and maximize the log posterior over parameters and hyperparameters together. For Gaussian priors the best hyperparameters have a closed form when the factors are fixed, so the method alternates between the two. This chooses $\lambda_U$ and $\lambda_V$ from the training data instead of by a grid search.
- **Constrained PMF (Section 4, Equation 7).** Each user vector is $U_i = Y_i + \sum_k I_{ik} W_k / \sum_k I_{ik}$, an offset plus the mean of vectors $W_k$ of the items the user rated. Users who rated similar sets of items get similar priors, which helps users with few ratings. The same idea, items rated as evidence about the user, appears in [SVD++](/svd-plus-plus/).
- **Bayesian PMF.** Instead of a MAP point, put hyperpriors on the hyperparameters and average over the posterior of $U$ and $V$, by sampling methods such as [Gibbs sampling](/gibbs-sampling/) or by [variational inference](/variational-inference/). The 2007 paper names a fully Bayesian treatment with Markov chain Monte Carlo only as future work (Section 6); it is not part of PMF as defined there.
- **Implicit feedback.** For clicks and purchases instead of ratings, the Gaussian likelihood on observed entries is replaced by a weighted loss on all entries; see [implicit feedback](/implicit-feedback/) and [ALS for implicit feedback](/implicit-feedback-als/).
- **Pairwise ranking.** [Bayesian personalized ranking](/bayesian-personalized-ranking/) keeps the factor model and the Gaussian prior but replaces the rating likelihood by a likelihood of pairwise preferences.

## Known results in the model

These are reported measurements on one data set, not theorems.

- **Netflix Prize data (Section 5).** The training set has 100,480,507 ratings from 480,189 users on 17,770 movies. Netflix's own system, Cinematch, had a test RMSE of 0.9514. A linear combination of several PMF models reached 0.8970, and a combination of PMF models with restricted Boltzmann machine models reached 0.8861, which the authors describe as nearly 7% better than Cinematch.
- **Users with few ratings.** On the full data, constrained PMF reached a validation RMSE of 0.9016, and the authors report that it generalizes considerably better than plain PMF for users with very few ratings, with the gap closing as the number of ratings grows (Section 5.4, Figure 4).
- **Capacity control.** On a smaller and harder subset (50,000 users, 1,850 movies) with 10 factors, PMF with adaptive priors reached a validation RMSE of 0.9197, against 0.9253 and 0.9430 for two fixed-penalty PMF models and 0.9258 for an unregularized factorization that then overfit (Section 5.3).

## References
