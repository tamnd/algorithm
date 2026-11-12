---
tag: 65EW3P
kind: model
slug: gaussian-graphical-model
name: Gaussian graphical model
aliases:
- Gaussian Markov random field
- covariance selection model
- concentration graph model
area: machine-learning/probabilistic-inference
level: advanced
summary: "A multivariate normal distribution with a graph: an edge is missing exactly when the precision matrix has a zero there, which means conditional independence given the rest."
prereqs: [markov-random-field, covariance-matrix, markov-property]
see_also: [lasso-regression, coordinate-descent, schur-complement, gaussian-belief-propagation, cholesky-decomposition, positive-definite-matrix, kalman-filter, factor-analysis]
sources:
  - paper: doi:10.2307/2528966
    title: Arthur P. Dempster, Covariance selection, Biometrics 28(1), 1972, pages 157 to 175
    locator: zeros in the inverse covariance matrix as the model, and the maximum likelihood fit that matches the sample covariance on the free entries
  - paper: doi:10.1093/biostatistics/kxm045
    title: Jerome Friedman, Trevor Hastie and Robert Tibshirani, Sparse inverse covariance estimation with the graphical lasso, Biostatistics 9(3), 2008, pages 432 to 441
    locator: the graphical lasso objective, block coordinate descent on W with a lasso for each column, and the diagonal W_jj = S_jj + rho
  - paper: doi:10.1214/009053606000000281
    title: Nicolai Meinshausen and Peter Bühlmann, High-dimensional graphs and variable selection with the Lasso, The Annals of Statistics 34(3), 2006, pages 1436 to 1462
    locator: neighbourhood selection by one lasso regression per variable, and its consistency
  - book: isbn:9780198522195
    title: Steffen L. Lauritzen, Graphical Models, Oxford University Press, 1996
    locator: "Chapter 5 (multivariate normal models): Gaussian graphical models and their maximum likelihood estimation"
  - book: isbn:9781584884323
    title: Håvard Rue and Leonhard Held, Gaussian Markov Random Fields, Theory and Applications, Chapman and Hall/CRC, 2005
    locator: "Chapter 2: the precision matrix, the conditional mean and variance of one variable given the rest, and sparse Cholesky methods"
---

A Gaussian graphical model is a multivariate normal distribution together with an undirected graph that records which pairs of variables are directly linked. The graph is read off the *precision matrix* $\Theta = \Sigma^{-1}$, the inverse of the [covariance matrix](/covariance-matrix/): there is no edge between $i$ and $j$ exactly when $\Theta_{ij} = 0$, and that zero means that $X_i$ and $X_j$ are independent given all the other variables. Dempster (1972) introduced the model as *covariance selection*. The standard estimator of a sparse $\Theta$ from data is the graphical lasso of Friedman, Hastie and Tibshirani (2008).

## The machine

**The distribution.** A random vector $X = (X_1, \dots, X_p)$ has the distribution $N(\mu, \Sigma)$ with a [positive definite](/positive-definite-matrix/) $\Sigma$. Its precision matrix is $\Theta = \Sigma^{-1}$, and its density is

$$f(x) \propto \exp\Big(-\tfrac12 (x - \mu)^\top \Theta (x - \mu)\Big) = \prod_{i} e^{-\frac12 \Theta_{ii} (x_i - \mu_i)^2} \prod_{i < j} e^{-\Theta_{ij} (x_i - \mu_i)(x_j - \mu_j)}.$$

The density is a product of factors on single variables and on pairs, so it is a pairwise [Markov random field](/markov-random-field/) on the graph $G = (V, E)$ with $V = \{1, \dots, p\}$ and $E = \{ij : \Theta_{ij} \ne 0\}$.

**The main fact.** For $i \ne j$, let $R = V \setminus \{i, j\}$. Then

$$X_i \perp X_j \mid X_R \iff \Theta_{ij} = 0.$$

*Proof.* Let $A = \{i, j\}$. The conditional distribution of $X_A$ given $X_R$ is normal with covariance equal to the [Schur complement](/schur-complement/) $\Sigma_{AA} - \Sigma_{AR} \Sigma_{RR}^{-1} \Sigma_{RA}$. The block inverse formula says that this Schur complement is $(\Theta_{AA})^{-1}$. The inverse of the $2 \times 2$ matrix $\Theta_{AA}$ has off-diagonal entry $-\Theta_{ij} / \det \Theta_{AA}$, which is zero exactly when $\Theta_{ij} = 0$. Two jointly normal variables are independent exactly when their covariance is zero, so the claim follows. $\blacksquare$

**Partial correlation.** The correlation of $X_i$ and $X_j$ given all the others is

$$\rho_{ij \cdot R} = -\frac{\Theta_{ij}}{\sqrt{\Theta_{ii} \Theta_{jj}}},$$

which is the correlation read from $(\Theta_{AA})^{-1}$. The sign is the opposite of the sign of $\Theta_{ij}$.

**One variable given the rest.** $X_i$ given $X_{V \setminus i} = x$ is normal with variance $1 / \Theta_{ii}$ and mean $\mu_i - \frac{1}{\Theta_{ii}} \sum_{j \ne i} \Theta_{ij} (x_j - \mu_j)$. So the regression of $X_i$ on the other variables has coefficient $-\Theta_{ij} / \Theta_{ii}$ on $X_j$, and the regression uses only the neighbours of $i$. This is the [Markov blanket](/markov-blanket/) of $i$.

**All Markov properties hold.** The density is positive everywhere, so the pairwise [Markov property](/markov-property/) given by the zeros of $\Theta$ implies the local and the global ones: if $S$ separates $A$ from $B$ in $G$, then $X_A \perp X_B \mid X_S$.

## What it counts

- **Parameters.** With the mean, the model has $p$ means, $p$ diagonal entries and one free entry of $\Theta$ per edge. A sparse graph has far fewer than the $p(p+1)/2$ entries of a full covariance matrix.
- **Likelihood.** For $N$ observations with sample covariance $S$ (around the sample mean), the log-likelihood is, up to a constant, $\frac{N}{2}\big(\log \det \Theta - \operatorname{tr}(S \Theta)\big)$. It is a concave function of $\Theta$.
- **Cost of inference.** Conditional means and variances need linear solves with blocks of $\Theta$. A dense [Cholesky decomposition](/cholesky-decomposition/) costs $O(p^3)$ operations. For a sparse $\Theta$, as in spatial models on grids, a sparse Cholesky factor after a fill-reducing order is much cheaper (Rue and Held 2005).
- **Cost of estimation.** One sweep of the graphical lasso solves $p$ lasso problems of size $p - 1$, which is $O(p^3)$ for dense problems and less when the solution is sparse.

## Relation to other models

- **Markov random fields.** It is the continuous case of a pairwise [Markov random field](/markov-random-field/), with quadratic log-potentials. The [Ising model](/ising-model/) and the [Potts model](/potts-model/) are discrete pairwise models.
- **Covariance graphs.** Zeros of $\Sigma$, not of $\Theta$, mean marginal independence. In the chain example below $\Theta_{13} = 0$ but $\Sigma_{13} \ne 0$.
- **Linear Gaussian networks.** A [Bayesian network](/bayesian-network/) in which each variable is a linear function of its parents plus Gaussian noise gives a normal joint. Its precision matrix has zeros outside the moral graph of the DAG.
- **State space models.** The [Kalman filter](/kalman-filter/) works with a chain-structured Gaussian model in time. [Factor analysis](/factor-analysis/) models $\Sigma$ as low rank plus diagonal, which is a different kind of structure.
- **Inference by messages.** [Gaussian belief propagation](/gaussian-belief-propagation/) passes means and precisions along the edges of $G$.

## Known results in the model

**Covariance selection.** Fix the graph $G$. Dempster (1972) showed that the maximum likelihood estimate $\hat\Theta$, under the constraint $\hat\Theta_{ij} = 0$ for $ij \notin E$, is the one whose inverse $\hat\Sigma$ agrees with $S$ on the diagonal and on the edges. The likelihood is concave, so the estimate is unique when it exists. It exists when $S$ is positive definite, which needs $N > p$, and it can exist for smaller $N$ when the graph is sparse.

**The graphical lasso.** When the graph is unknown, Friedman, Hastie and Tibshirani (2008) maximize

$$\log \det \Theta - \operatorname{tr}(S \Theta) - \rho \textstyle\sum_{i,j} |\Theta_{ij}|$$

over positive definite $\Theta$, with a penalty $\rho \ge 0$. The objective is strictly concave, so the maximizer is unique, and for $\rho > 0$ it is positive definite even when $N < p$. The method works on $W = \Theta^{-1}$. It sets $W = S + \rho I$, and then cycles over the columns. For column $j$, with $W_{11}$ the matrix $W$ without row and column $j$ and $s_{12}$ the column $j$ of $S$ without its diagonal entry, it solves the [lasso](/lasso-regression/) problem

$$\min_\beta \tfrac12 \beta^\top W_{11} \beta - \beta^\top s_{12} + \rho \|\beta\|_1$$

by [coordinate descent](/coordinate-descent/), and sets the column of $W$ to $W_{11} \beta$. At the end, $\Theta_{jj} = 1 / (W_{jj} - w_{12}^\top \beta)$ and the column of $\Theta$ is $-\beta\, \Theta_{jj}$. The optimality conditions are $W - S = \rho \Gamma$, where $\Gamma_{ij}$ is the sign of $\Theta_{ij}$ when it is not zero and lies in $[-1, 1]$ when it is zero; in particular $W_{jj} = S_{jj} + \rho$. If $\rho \ge \max_{i \ne j} |S_{ij}|$, the estimate is diagonal.

**Neighbourhood selection.** Meinshausen and Bühlmann (2006) regress each variable on all the others with the lasso and put an edge where a coefficient is not zero. Because the coefficients are $-\Theta_{ij} / \Theta_{ii}$, this estimates the same graph. They proved that it finds the true graph with probability tending to one, under conditions on the sparsity and on the correlations, even when $p$ grows faster than $N$.

**A worked example.** Take the chain $1 - 2 - 3$ with

$$\Theta = \begin{pmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 2 \end{pmatrix}, \qquad \Sigma = \frac14 \begin{pmatrix} 3 & 2 & 1 \\ 2 & 4 & 2 \\ 1 & 2 & 3 \end{pmatrix}.$$

$X_1$ and $X_3$ are correlated, with correlation $1/3$, since $\Sigma_{13} = 1/4$. Given $X_2$, their conditional covariance matrix is $\Sigma_{\{1,3\}} - \Sigma_{\{1,3\},2} \Sigma_{22}^{-1} \Sigma_{2,\{1,3\}} = \frac12 I$, so they are independent given $X_2$, as the zero $\Theta_{13}$ says. The partial correlation of $X_1$ and $X_2$ given $X_3$ is $1 / \sqrt{4} = 1/2$.

**Checks in code.** The tests compute $\Sigma = \Theta^{-1}$ in exact rational arithmetic for random sparse $\Theta$, and confirm that the Schur complement gives zero conditional covariance exactly at the zeros of $\Theta$, and for every separated triple of sets. They also check the graphical lasso: with $\rho = 0$ it returns $S^{-1}$, its output meets the optimality conditions, and on 3000 samples from a chain model it finds the chain.

## References
