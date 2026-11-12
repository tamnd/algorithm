---
tag: GZK9TB
kind: algorithm
slug: quadratic-discriminant-analysis
name: Quadratic discriminant analysis
aliases:
- QDA
- quadratic discriminant classifier
- Gaussian quadratic classifier
area: machine-learning/supervised-learning
level: intro
summary: "Fit one Gaussian per class, each with its own covariance, and predict the class of largest posterior. The decision boundaries are quadratic."
solves: [classification]
model: real-ram
complexity:
  vars: {n: the number of training examples, d: the number of features, k: the number of classes}
  time: {worst: "O(n d^2 + k d^3)", best: "Θ(n d^2 + k d^3)"}
  space: {extra: "Θ(k d^2)"}
properties: {deterministic: true, online: false, exact: true, recursive: false}
history:
  year: 1947
  people: [Cedric A. B. Smith]
  note: Fisher's 1936 linear discriminant assumes a common covariance. The quadratic rule for normal classes with unequal covariances appears in Smith 1947. Friedman added regularized discriminant analysis in 1989.
prereqs: [bayes-optimal-classifier, covariance-matrix, maximum-likelihood-estimation]
see_also: [linear-discriminant-analysis, naive-bayes-classifier, gaussian-mixture-model, cholesky-decomposition, logistic-regression, generative-vs-discriminative-models, positive-definite-matrix, bias-variance-tradeoff]
sources:
  - paper: doi:10.1080/01621459.1989.10478752
    title: Jerome H. Friedman, Regularized discriminant analysis, Journal of the American Statistical Association 84(405), 1989
    locator: pp. 165 to 175 (the two parameters λ and γ, the shrinkage toward the pooled covariance and toward a multiple of the identity)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 4.3 (linear and quadratic discriminant functions, eq. 4.12) and Section 4.3.1 (regularized discriminant analysis)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 4.2.1 (Gaussian class conditionals; a shared covariance gives linear boundaries, separate covariances give quadratic ones)
  - paper: "C. A. B. Smith, Some examples of discrimination, Annals of Eugenics 13, 1947"
    locator: pp. 272 to 282 (a quadratic discriminant for normal classes with unequal covariances)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 4.2 (the Cholesky factorization of a symmetric positive definite matrix)
---

Quadratic discriminant analysis (QDA) is a generative classifier. It models each class $c$ as a Gaussian $\mathcal{N}(\mu_c, \Sigma_c)$ with its own mean and its own [covariance matrix](/covariance-matrix/), estimates the prior $\pi_c$, the means and the covariances by [maximum likelihood](/maximum-likelihood-estimation/), and predicts the class with the largest posterior probability. Because each class has its own covariance, the boundary between two classes is the zero set of a quadratic function of $x$. When all classes share one covariance, the quadratic terms cancel and QDA becomes [linear discriminant analysis](/linear-discriminant-analysis/). Training costs $O(n d^2 + k d^3)$ and one prediction costs $O(k d^2)$ after a [Cholesky decomposition](/cholesky-decomposition/) of each covariance.

## In plain words

You have measurements of items from a few groups. For each group, you draw an oval cloud that fits its points: the center of the cloud is the group average, and the size, the stretch and the tilt of the cloud come from the spread of the points. Each group gets a cloud of its own shape. For a new item, you ask which cloud makes the item most likely, after you also count how common each group is. The item goes to that group.

Because the clouds can have different shapes, the line between two groups can bend. It can be a curve, a closed ring around a tight group, or two separate pieces. A tight group wins only near its center, and a wide group can win again far away on the other side.

## The problem

The data model is supervised [classification](/classification/): the training set $S = ((x_1, y_1), \ldots, (x_n, y_n))$ has $x_i \in \mathbb{R}^d$ and $y_i$ in a finite set of $k$ classes. The model assumes that the class $y$ has prior $\pi_c = P(y = c)$ and that $x$ given $y = c$ is Gaussian:
$$ p(x \mid c) = (2\pi)^{-d/2} |\Sigma_c|^{-1/2} \exp\!\big(-\tfrac12 (x - \mu_c)^{\top} \Sigma_c^{-1} (x - \mu_c)\big). $$
The output is a rule that maps a query $x$ to a class. Under the 0-1 loss, the [Bayes optimal classifier](/bayes-optimal-classifier/) for this model picks the class with the largest $\pi_c\, p(x \mid c)$. Taking logarithms and dropping the constant $-\frac d2 \log 2\pi$ gives the quadratic discriminant function (ESL eq. 4.12):
$$ \delta_c(x) = -\tfrac12 \log|\Sigma_c| - \tfrac12 (x - \mu_c)^{\top} \Sigma_c^{-1} (x - \mu_c) + \log \pi_c . $$

## The algorithm

QDA estimates the parameters and then evaluates $\delta_c$. Let $n_c$ be the number of training points of class $c$, $\mu_c$ their mean, $W_c = \sum_{y_i = c} (x_i - \mu_c)(x_i - \mu_c)^{\top}$ their scatter matrix and $W = \sum_c W_c$ the pooled scatter. Friedman's regularized discriminant analysis (RDA) uses two parameters $\lambda, \gamma \in [0, 1]$:
$$ S_c(\lambda) = \frac{(1 - \lambda) W_c + \lambda W}{(1 - \lambda) n_c + \lambda n}, \qquad \Sigma_c(\lambda, \gamma) = (1 - \gamma) S_c(\lambda) + \gamma\, \frac{\operatorname{tr} S_c(\lambda)}{d}\, I . $$
With $\lambda = \gamma = 0$ this is plain QDA with the maximum likelihood covariance $W_c / n_c$. With $\lambda = 1$ and $\gamma = 0$ every class gets the pooled covariance $W / n$, which is LDA.

```pseudo id=main
QDA-FIT(S, λ, γ)
L1  for each class c do
L2      π_c ← n_c / n
L3      μ_c ← (1/n_c) Σ_{i: y_i = c} x_i
L4      W_c ← Σ_{i: y_i = c} (x_i − μ_c)(x_i − μ_c)ᵀ
L5  for each class c do Σ_c ← Σ_c(λ, γ), as defined above
L6      L_c ← the Cholesky factor of Σ_c, with L_c L_cᵀ = Σ_c
L7      ℓ_c ← 2 Σ_{j=1..d} log L_c[j, j]
QDA-PREDICT(x)
L8  for each class c do
L9      solve L_c z = x − μ_c by forward substitution
L10     δ_c ← −ℓ_c / 2 − zᵀz / 2 + log π_c
L11 return the first class c, in a fixed order, with the largest δ_c
```

Line L6 fails when $\Sigma_c$ is not [positive definite](/positive-definite-matrix/), for example when $n_c \le d$ and $\lambda = \gamma = 0$. Lines L9 and L10 never form $\Sigma_c^{-1}$: since $\Sigma_c^{-1} = L_c^{-\top} L_c^{-1}$, the quadratic form equals $\lVert L_c^{-1}(x - \mu_c) \rVert^2 = z^{\top} z$, and $\log|\Sigma_c| = \log |L_c|^2 = 2 \sum_j \log L_c[j,j]$. The posterior probabilities are $P(c \mid x) = e^{\delta_c} / \sum_{c'} e^{\delta_{c'}}$, computed with the [log-sum-exp trick](/log-sum-exp-trick/).

## Example

Eight points in $\mathbb{R}^2$, four in each class:

| class | points | $\mu_c$ | $\Sigma_c$ (maximum likelihood) |
| --- | --- | --- | --- |
| A | (0, 0), (2, 0), (0, 2), (2, 2) | (1, 1) | $I$ |
| B | (4, 1), (6, 1), (5, 0), (5, 2) | (5, 1) | $\frac12 I$ |

Both priors are $\frac12$. Here $\log|\Sigma_A| = 0$ and $\log|\Sigma_B| = -2\ln 2$, so
$$ \delta_A(x) = -\tfrac12 \lVert x - \mu_A \rVert^2 - \ln 2, \qquad \delta_B(x) = \ln 2 - \lVert x - \mu_B \rVert^2 - \ln 2 . $$
For the query $(3, 1)$: $\delta_A = -2 - \ln 2 \approx -2.693$ and $\delta_B = -4$, so QDA predicts A with posterior $0.787$. The boundary $\delta_A = \delta_B$ is $2\lVert x - \mu_B\rVert^2 - \lVert x - \mu_A \rVert^2 = 2 \ln 2$. Expand it with $2\mu_B - \mu_A = (9, 1)$ and $2\lVert\mu_B\rVert^2 - \lVert\mu_A\rVert^2 = 50$:
$$ (x_1 - 9)^2 + (x_2 - 1)^2 = 32 + 2 \ln 2 \approx 33.386 . $$
The boundary is a circle with center $(9, 1)$ and radius about $5.778$. Class B, the tight class, wins inside it. On the line $x_2 = 1$ the boundary points are $x_1 = 9 \pm \sqrt{32 + 2\ln 2}$, that is $3.222$ and $14.778$.

| query | $\delta_A$ | $\delta_B$ | QDA | posterior of the winner | LDA |
| --- | --- | --- | --- | --- | --- |
| (3, 1) | −2.693 | −4 | A | 0.787 | tie (on the line $x_1 = 3$) |
| (3.5, 1) | −3.818 | −2.25 | B | 0.828 | B |
| (14, 1) | −85.193 | −81 | B | 0.985 | B |
| (16, 1) | −113.193 | −121 | A | 0.9996 | B |

LDA pools the covariances into $\frac34 I$, and its discriminant is $\delta_B - \delta_A = \frac{16}{3} x_1 - 16$, so its boundary is the line $x_1 = 3$. The two rules disagree far to the right: at $(16, 1)$ the point is 11 units from $\mu_B$, and a class with variance $\frac12$ makes that much less likely than the wider class A does.

**A case LDA cannot handle.** In one dimension, let class 1 be $\mathcal{N}(0, 1)$ and class 2 be $\mathcal{N}(0, 4)$, with equal priors. The means are equal, so every linear rule has error at least $\frac12$. The QDA rule picks class 1 when $|x| < t$ with $\frac38 t^2 = \ln 2$, so $t = \sqrt{(8/3) \ln 2} \approx 1.360$, and its error is $(1 - \Phi(t)) + \Phi(t/2) - \frac12 \approx 0.339$, the Bayes error.

## Correctness

There are two claims. First, with $\lambda = \gamma = 0$, lines L1 to L5 compute the maximum likelihood estimates of the priors, means and covariances of the Gaussian class model. The log likelihood separates into one term for the prior, maximized by the class frequencies, and one term for each class, maximized by the sample mean and the scatter divided by $n_c$. Second, lines L6 to L10 compute $\delta_c(x) = \log\big(\pi_c\, p(x \mid c)\big) + \frac d2 \log 2\pi$, by the two Cholesky identities above, so line L11 returns a class with the largest posterior under the fitted model. If the data really come from the Gaussian model, this is the Bayes optimal rule for the fitted parameters, and it converges to the Bayes rule as $n \to \infty$ because the estimates are consistent. The full proof is below, together with the proof that equal class covariances give the linear LDA boundary.

## Complexity

The model is the [real RAM](/real-ram/).

- **Training.** The means cost $\Theta(n d)$ and the scatter matrices cost $\Theta(n d^2)$ (each point adds one outer product of size $d \times d$). Each Cholesky factorization costs about $d^3/3$ operations, so $\Theta(k d^3)$ for all classes. The total is $\Theta(n d^2 + k d^3)$, with $\Theta(k d^2)$ space for the factors.
- **One prediction.** Forward substitution costs $\Theta(d^2)$ per class, so a query costs $\Theta(k d^2)$.
- **Parameters.** QDA has $k\big(d + d(d+1)/2\big) + k - 1$ free parameters, against $k d + d(d+1)/2 + k - 1$ for LDA. With $d = 100$ and $k = 3$, QDA has 15,452 and LDA has 5,352.

## Properties

- **Quadratic boundaries.** The boundary between classes $a$ and $b$ is $\{x : \delta_a(x) = \delta_b(x)\}$, a quadric surface with quadratic part $-\frac12 x^{\top}(\Sigma_a^{-1} - \Sigma_b^{-1}) x$. In the plane it is a conic: an ellipse, a parabola, a hyperbola, or a pair of lines. In one dimension it gives up to two thresholds, so a class region can have two pieces.
- **Equal covariances give LDA.** If $\Sigma_a = \Sigma_b = \Sigma$, the terms $x^{\top} \Sigma^{-1} x$ and $\log|\Sigma|$ cancel in $\delta_a - \delta_b$, which is linear in $x$. If two classes have equal sample covariances $W_a / n_a = W_b / n_b$, the pooled covariance is the same matrix, so plain QDA gives exactly the [linear discriminant analysis](/linear-discriminant-analysis/) boundary.
- **Posterior form.** For two classes, $\log\frac{P(a \mid x)}{P(b \mid x)} = \delta_a(x) - \delta_b(x)$ is a quadratic function of $x$. So QDA fits the same family of posteriors as [logistic regression](/logistic-regression/) on the features $x_j$ and $x_j x_l$, but by maximizing the joint likelihood, not the conditional one. See [generative vs discriminative models](/generative-vs-discriminative-models/).
- **Invariance.** The predictions do not change under an invertible affine change of the features, $x \mapsto A x + b$, when $\gamma = 0$: the means move with the map, each covariance becomes $A \Sigma_c A^{\top}$, the quadratic forms do not change, and every $\log|\Sigma_c|$ grows by the same $2 \log|\det A|$. The term $\gamma\, \operatorname{tr}(S)/d \cdot I$ is not invariant: scale the features before RDA.
- **Variance.** The covariance estimates are the weak part. With $n_c$ close to $d$, $W_c / n_c$ has small eigenvalues that are much too small, and $\Sigma_c^{-1}$ blows up along their directions. This is the [bias-variance tradeoff](/bias-variance-tradeoff/) that RDA controls.

## Variants and improvements

- **Regularized discriminant analysis** (Friedman 1989). $\lambda$ moves each class covariance toward the pooled covariance, from QDA ($\lambda = 0$) to LDA ($\lambda = 1$). $\gamma$ moves it toward a multiple of the identity, which also fixes a singular pooled covariance. Both are chosen by [cross-validation](/cross-validation/) on a grid. ESL writes the first step as $\Sigma_c(\alpha) = \alpha \Sigma_c + (1 - \alpha) \Sigma$, with the pooled covariance $\Sigma$, which is the same family when the class sizes are equal, with $\alpha = (1 - \lambda) n_c / \big((1 - \lambda) n_c + \lambda n\big)$.
- **Diagonal QDA.** Restrict each $\Sigma_c$ to be diagonal. This is Gaussian [naive Bayes](/naive-bayes-classifier/): $O(k d)$ parameters, and boundaries that are quadratic without cross terms.
- **Mixture discriminant analysis.** Model each class as a [Gaussian mixture](/gaussian-mixture-model/) fitted by EM, for classes with several clusters (ESL Section 12.7).
- **Unbiased covariances.** Some libraries divide $W_c$ by $n_c - 1$. This changes $\log|\Sigma_c|$ and the quadratic form by class dependent amounts, so the predictions can differ slightly from the maximum likelihood version.

## When to use it

Use QDA when the classes have clearly different spreads or orientations, the number of features is small, and each class has many more points than features. It is fast, it has no learning rate or iterations, and it returns calibrated posteriors when the Gaussian assumption holds. Use LDA, RDA or diagonal QDA when $n_c$ is not much larger than $d$; use logistic regression, kernel methods or trees when the classes are far from Gaussian, for example when they have heavy tails or several clusters.

## Pitfalls

- **Singular covariance.** With $n_c \le d$, or with a feature that is constant within a class, $W_c$ is singular and line L6 fails. Do not "fix" this with a pseudo-inverse; regularize with $\lambda$ or $\gamma$.
- **Explicit inverse and determinant.** Computing $\Sigma_c^{-1}$ and $|\Sigma_c|$ directly is slower and less stable, and $|\Sigma_c|$ underflows or overflows in high dimensions. Use the Cholesky factor and its log-diagonal.
- **Exponentiating the discriminants.** $\delta_c$ is often below $-700$, where $e^{\delta_c}$ is 0 in double precision. Normalize the posteriors in log space.
- **Outliers.** One far point changes a covariance estimate a lot, and so changes the boundary. Robust estimates of the means and covariances help.

## Implementations

## History

Ronald Fisher introduced the linear discriminant in 1936 for two classes with a common covariance. The likelihood ratio rule for two normal classes with unequal covariances, which gives a quadratic boundary, was described by C. A. B. Smith in 1947, and became standard in the statistical theory of discrimination (Anderson's multivariate analysis texts, McLachlan's 1992 monograph). Jerome Friedman proposed regularized discriminant analysis in 1989 to make QDA usable when the classes have few points compared with the number of features. The Elements of Statistical Learning presents LDA, QDA and RDA as one family.

## References
