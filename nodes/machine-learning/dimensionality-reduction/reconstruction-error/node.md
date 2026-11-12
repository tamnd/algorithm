---
tag: WXM4XT
kind: concept
slug: reconstruction-error
name: Reconstruction error
aliases:
- reconstruction loss
area: machine-learning/dimensionality-reduction
level: intro
summary: "The mean squared distance between data and their reconstruction from a low-dimensional code. For rank k PCA it equals the sum of the discarded covariance eigenvalues."
prereqs: [principal-component-analysis]
see_also: [explained-variance, singular-value-decomposition, autoencoder, k-means-problem, nonnegative-matrix-factorization, vector-quantization, robust-pca, scree-plot]
sources:
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 12.1.2 (the minimum-error formulation of PCA, with the distortion measure equal to the sum of the discarded eigenvalues)
  - paper: doi:10.1007/BF02288367
    title: Carl Eckart and Gale Young, The approximation of one matrix by another of lower rank, Psychometrika 1(3), 211-218, 1936
    locator: the best rank k approximation in the Frobenius norm is the truncated singular value decomposition
  - paper: doi:10.1016/0893-6080(89)90014-2
    title: Pierre Baldi and Kurt Hornik, Neural networks and principal component analysis, learning from examples without local minima, Neural Networks 2(1), 53-58, 1989
    locator: a linear autoencoder with squared reconstruction error has its global minimum at the projection on the principal subspace
  - paper: doi:10.1080/00401706.1979.10489779
    title: J. Edward Jackson and Govind S. Mudholkar, Control procedures for residuals associated with principal component analysis, Technometrics 21(3), 341-349, 1979
    locator: the residual sum of squares of a point after PCA (the Q statistic) and its control limit
  - book: isbn:9780387954424
    title: I. T. Jolliffe, Principal Component Analysis, second edition, Springer, 2002
    locator: Section 3.5 (the singular value decomposition and the best low-rank fit) and Section 10.1 (detection of outliers by the last components and by residuals)
---

The reconstruction error of a dimensionality reduction method is the mean squared distance between each data point and the point that the method rebuilds from its low-dimensional code. For [principal component analysis](/principal-component-analysis/) with $k$ components, it equals the sum of the $d - k$ smallest eigenvalues of the [covariance matrix](/covariance-matrix/) (with the divisor $n$), and no other $k$-dimensional affine subspace gives a smaller value. The same quantity is the training loss of an [autoencoder](/autoencoder/) and the cost of the [k-means problem](/k-means-problem/).

## In plain words

A method that shrinks data has two parts. The first part turns each point into a short code. The second part turns the code back into a point. The rebuilt point is usually not equal to the original one, because the code holds less information. The reconstruction error measures this loss: for each point, take the squared distance between the original and the rebuilt point, and then take the mean over all points.

A small error means that the short code keeps most of the data. For principal component analysis the error has an exact value: it is the total spread in the directions that you throw away. More components always give a smaller error on the training data, so the error alone does not tell you when to stop.

## The idea

**General form.** An encoder $f : \mathbb{R}^d \to \mathbb{R}^k$ and a decoder $g : \mathbb{R}^k \to \mathbb{R}^d$ give the reconstruction error

$$\operatorname{err}(f, g) = \frac{1}{n} \sum_{i=1}^{n} \|x_i - g(f(x_i))\|^2 .$$

Some authors use the sum instead of the mean, or divide also by $d$; the relative error divides by the total variance $\frac1n \sum_i \|x_i - \bar x\|^2$.

**PCA.** Let $C = \frac1n \sum_i (x_i - \bar x)(x_i - \bar x)^T$ have the eigenvalues $\lambda_1 \ge \cdots \ge \lambda_d$ and orthonormal eigenvectors $v_1, \ldots, v_d$. With $W_k = [v_1, \ldots, v_k]$, PCA encodes $f(x) = W_k^T (x - \bar x)$ and decodes $g(z) = \bar x + W_k z$. Then

$$\operatorname{err}_k = \frac1n \sum_{i=1}^{n} \|(I - W_k W_k^T)(x_i - \bar x)\|^2 = \sum_{j=k+1}^{d} \lambda_j .$$

*Proof.* Write $y_i = x_i - \bar x = \sum_j (v_j^T y_i) v_j$. The residual is $\sum_{j > k} (v_j^T y_i) v_j$, and since the $v_j$ are orthonormal its squared norm is $\sum_{j > k} (v_j^T y_i)^2$. The mean over $i$ of $(v_j^T y_i)^2$ is $v_j^T C v_j = \lambda_j$. $\square$

**Optimality.** For each $k$-dimensional affine subspace, the mean squared distance of the points to it is at least $\sum_{j > k} \lambda_j$. The [PCA](/principal-component-analysis/) page proves this with the Ky Fan inequality. In matrix form, with $X_c$ the centered $n \times d$ data and singular values $\sigma_j$, the PCA reconstruction is the truncated [SVD](/singular-value-decomposition/) of $X_c$, and $n \cdot \operatorname{err}_k = \|X_c - X_{c,k}\|_F^2 = \sum_{j > k} \sigma_j^2$. Eckart and Young (1936) proved that no matrix of rank at most $k$ is closer to $X_c$ in the Frobenius norm. So $\lambda_j = \sigma_j^2 / n$.

**Link to explained variance.** The total variance is $\operatorname{tr} C = \sum_j \lambda_j$, so $\operatorname{err}_k / \operatorname{tr} C = 1 - R_k$, where $R_k$ is the cumulative [explained variance](/explained-variance/) ratio.

**Training error and new data.** On the training data, $\operatorname{err}_k$ does not increase with $k$ and reaches 0 at $k = d$ (or at the rank of $X_c$). So it cannot choose $k$ by itself, and it is optimistic for new points. On held-out points the error is still $\frac1m \sum \|(I - W_k W_k^T)(x - \bar x)\|^2$, but it is no longer the sum of the discarded eigenvalues of the training covariance.

**Other codes.** The same error measures other methods, each with a different set of allowed encoders and decoders:

- a [linear autoencoder](/autoencoder/) with squared loss: its global minima span the same subspace as PCA (Baldi and Hornik 1989), though the learned weights need not be orthonormal;
- [k-means](/k-means-problem/) and [vector quantization](/vector-quantization/): the code is the index of the nearest center, the decoder returns the center, and the error is the k-means cost divided by $n$;
- [nonnegative matrix factorization](/nonnegative-matrix-factorization/): $\|X - WH\|_F^2$ with nonnegative factors;
- [kernel PCA](/kernel-pca/): the error is small in the feature space, but a point in the input space that maps to the reconstruction may not exist (the pre-image problem).

## Examples

**The PCA example.** The eight points of the [PCA](/principal-component-analysis/) page have the mean $(4, 5, 6)$ and the covariance eigenvalues $81, 36, 9$, with eigenvectors $v_1 = (1, 2, 2)/3$, $v_2 = (2, 1, -2)/3$, $v_3 = (2, -2, 1)/3$.

| $k$ | $\operatorname{err}_k$ | relative error |
|---|---|---|
| 0 | 126 | 1 |
| 1 | 45 | 0.357 |
| 2 | 9 | 0.071 |
| 3 | 0 | 0 |

Check one point. For $x = (13, 11, 9)$, $y = x - \bar x = (9, 6, 3)$ has the scores $v_1^T y = 9$, $v_2^T y = 6$ and $v_3^T y = 3$. With $k = 1$ the reconstruction is $\bar x + 9 v_1 = (7, 11, 12)$, and the squared error is $\|(6, 0, -3)\|^2 = 45 = 6^2 + 3^2$. With $k = 2$ it is $\bar x + 9 v_1 + 6 v_2 = (11, 13, 8)$, with squared error $\|(2, -2, 1)\|^2 = 9 = 3^2$. In this data set every point has the scores $\pm 9$, $\pm 6$ and $\pm 3$, so every point has the same error as the mean.

**A subspace that is not the best.** For the same data, project on the first coordinate axis $e_1$. The variance along $e_1$ is $C_{11} = 29$, so the error is $126 - 29 = 97$, far above the PCA error 45 for $k = 1$.

**Rank deficiency.** If the points lie on a $k$-dimensional affine subspace, then $\lambda_{k+1} = \cdots = \lambda_d = 0$ and PCA rebuilds them exactly. The [covariance matrix](/covariance-matrix/) page shows that this always happens for $k = n - 1$.

## Where it is used

- Choosing $k$ for PCA by a target relative error, which is the same as a cumulative [explained variance](/explained-variance/) threshold.
- Anomaly detection: a point far from the principal subspace has a large residual $\|(I - W_k W_k^T)(x - \bar x)\|^2$. In process monitoring this is the Q statistic, or squared prediction error, with control limits from Jackson and Mudholkar (1979).
- Training [autoencoders](/autoencoder/) and [variational autoencoders](/variational-autoencoder/), where the reconstruction term is one part of the loss.
- Measuring the quality of [randomized PCA](/randomized-pca/) and [incremental PCA](/incremental-pca/) against the exact value $\sum_{j > k} \lambda_j$.
- [Robust PCA](/robust-pca/) replaces the squared error, which large outliers dominate, by a low-rank plus sparse split.
- Lossy compression: [vector quantization](/vector-quantization/) and transform coding measure distortion as the mean squared reconstruction error.

## References
