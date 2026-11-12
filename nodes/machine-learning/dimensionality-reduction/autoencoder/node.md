---
tag: GR8CEC
kind: model
slug: autoencoder
name: Autoencoder
aliases:
- auto-encoder
- autoassociative neural network
- undercomplete autoencoder
area: machine-learning/dimensionality-reduction
level: core
summary: "A neural network trained to copy its input through a narrow code layer. With linear layers and squared loss its code spans the PCA subspace, but its weights need not be orthogonal."
prereqs: [backpropagation, activation-function, principal-component-analysis]
see_also: [variational-autoencoder, reconstruction-error, probabilistic-pca, kernel-pca, singular-value-decomposition, principal-curves, dropout, weight-decay]
sources:
  - paper: doi:10.1016/0893-6080(89)90014-2
    title: "Pierre Baldi and Kurt Hornik, Neural networks and principal component analysis: learning from examples without local minima, Neural Networks 2(1):53-58, 1989"
    locator: the linear autoencoder with squared loss; its global minimum is the projection onto the top principal subspace, the weights are fixed only up to an invertible matrix, and all other critical points are saddle points
  - paper: doi:10.1007/BF00332918
    title: "Hervé Bourlard and Yves Kamp, Auto-association by multilayer perceptrons and singular value decomposition, Biological Cybernetics 59(4-5):291-294, 1988"
    locator: for one hidden layer and linear outputs, the optimal weights follow from the SVD of the data, and nonlinear hidden units do not lower the optimal error
  - book: isbn:9780262035613
    title: "Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016"
    locator: "Chapter 14 (autoencoders): 14.1 undercomplete autoencoders, 14.2 regularized autoencoders (sparse and denoising), 14.7 contractive autoencoders"
  - paper: doi:10.1126/science.1127647
    title: "Geoffrey E. Hinton and Ruslan R. Salakhutdinov, Reducing the dimensionality of data with neural networks, Science 313(5786):504-507, 2006"
    locator: deep autoencoders with a 30-unit code, pretrained layer by layer, give lower reconstruction error than PCA on images and documents
  - paper: "Pascal Vincent, Hugo Larochelle, Yoshua Bengio and Pierre-Antoine Manzagol, Extracting and composing robust features with denoising autoencoders, Proceedings of ICML 2008, pp. 1096-1103"
    title: Vincent, Larochelle, Bengio and Manzagol 2008
    locator: the denoising autoencoder, trained to rebuild the clean input from a corrupted copy
  - paper: "Salah Rifai, Pascal Vincent, Xavier Muller, Xavier Glorot and Yoshua Bengio, Contractive auto-encoders: explicit invariance during feature extraction, Proceedings of ICML 2011"
    title: Rifai, Vincent, Muller, Glorot and Bengio 2011
    locator: the contractive penalty on the Frobenius norm of the Jacobian of the encoder
  - paper: "Carl Eckart and Gale Young, The approximation of one matrix by another of lower rank, Psychometrika 1(3):211-218, 1936"
    title: Eckart and Young 1936
    locator: the best approximation of a matrix of a given rank in the Frobenius norm comes from the truncated singular value decomposition
  - paper: "Simon S. Du, Wei Hu and Jason D. Lee, Algorithmic regularization in learning deep homogeneous models: layers are automatically balanced, Advances in Neural Information Processing Systems 31 (NeurIPS 2018)"
    title: Du, Hu and Lee 2018
    locator: under gradient flow, the difference of W_l W_l^T and W_(l+1)^T W_(l+1) between adjacent layers stays constant
---

An autoencoder is a neural network that is trained to output its own input. It has two parts: an *encoder* $f$ that maps an input $x \in \mathbb{R}^d$ to a code $z = f(x) \in \mathbb{R}^k$, and a *decoder* $g$ that maps the code back to a reconstruction $\hat x = g(z)$. When the code is narrower than the input ($k < d$, the *bottleneck*), the network cannot learn the identity, so it must keep the directions of the data that matter most for the [reconstruction error](/reconstruction-error/). The code is then a nonlinear reduction of the dimension. In the linear case with squared loss the autoencoder learns exactly the subspace of [principal component analysis](/principal-component-analysis/) (Bourlard and Kamp 1988; Baldi and Hornik 1989), but not the principal directions themselves: its weights are fixed only up to an invertible $k \times k$ matrix and need not be orthogonal.

## The machine

An autoencoder with code size $k$ is a pair of parametrized maps

$$f_\theta : \mathbb{R}^d \to \mathbb{R}^k, \qquad g_\phi : \mathbb{R}^k \to \mathbb{R}^d,$$

each a feed-forward network of affine layers and [activation functions](/activation-function/), for example $f_\theta(x) = \sigma(W_1 x + b_1)$ and $g_\phi(z) = W_2 z + b_2$ for one hidden layer. Given data $x_1, \ldots, x_n$, it is trained to minimize

$$L(\theta, \phi) = \frac{1}{n} \sum_{i=1}^{n} \ell\big(x_i,\ g_\phi(f_\theta(x_i))\big),$$

with the squared error $\ell(x, \hat x) = \|x - \hat x\|^2$ for real data, or the cross entropy for data in $[0, 1]$. The gradients come from [backpropagation](/backpropagation/), and the training is by stochastic gradient descent or one of its variants. No labels are used.

The **linear autoencoder** has no activation functions and no biases, and works on centered data:

$$z = W_1 x, \qquad \hat x = W_2 z, \qquad W_1 \in \mathbb{R}^{k \times d},\ W_2 \in \mathbb{R}^{d \times k}.$$

With $S = \frac{1}{n} \sum_i x_i x_i^\top$ and $P = W_2 W_1$, its loss and gradients depend on the data only through $S$:

$$L = \operatorname{tr} S - 2 \operatorname{tr}(P S) + \operatorname{tr}(P S P^\top), \qquad \frac{\partial L}{\partial W_1} = -2 W_2^\top R, \qquad \frac{\partial L}{\partial W_2} = -2 R\, W_1^\top,$$

where $R = S - P S$. The implementation trains this model by full-batch gradient descent from a random start.

Three variants keep the code useful when the bottleneck alone is not enough, for example when $k \ge d$:

- **Denoising** (Vincent, Larochelle, Bengio and Manzagol 2008). Corrupt each input to $\tilde x$, for example by setting a random part of it to zero or by adding noise, and minimize $\ell(x, g(f(\tilde x)))$: the network must rebuild the clean input.
- **Sparse.** Add a penalty on the code, such as $\lambda \sum_j |z_j|$, or a KL penalty that keeps the mean activation of each code unit near a small target.
- **Contractive** (Rifai et al. 2011). Add $\lambda \|J_f(x)\|_F^2$, the squared Frobenius norm of the Jacobian of the encoder, so that the code changes little when the input moves a little.

## What it counts

The model gives three things:

- **The code** $z_i = f(x_i)$ of each point, which is the reduced representation. It is used for plots (with $k = 2$), as features for a later model, or for search.
- **The reconstruction error** $\|x - g(f(x))\|^2$ of each point. A large error marks a point that is unlike the training data, which makes autoencoders a common tool for anomaly detection.
- **The training loss** $L$, the mean reconstruction error. For the linear autoencoder its smallest value is $\sum_{j > k} \lambda_j$, the sum of the eigenvalues of $S$ that PCA leaves out.

An example. Take $d = 2$, $k = 1$ and $S = \operatorname{diag}(4, 1)$. The weights $W_2 = (2, 0)^\top$ and $W_1 = (0.5, 0)$ give $P = \operatorname{diag}(1, 0)$ and $L = 5 - 2 \cdot 4 + 4 = 1$, the left-out eigenvalue. So do $W_2 = (c, 0)^\top$ and $W_1 = (1/c, 0)$ for every $c \ne 0$, and only $c = \pm 1$ makes $W_1$ a unit vector.

On a seeded set of 200 centered points in $\mathbb{R}^5$ with sample eigenvalues $7.010$, $2.790$, $2.227$, $1.404$ and $0.430$, a linear autoencoder with $k = 2$ trained for 4000 steps of gradient descent (step size $0.02$) goes from $L = 13.97$ to $L = 4.0609$, which equals $2.227 + 1.404 + 0.430$. The principal angles between the column space of $W_2$ and the top two eigenvectors are below $10^{-4}$. When the start makes the encoder ten times larger than the decoder, the end has the same subspace and the same loss, but $W_1 W_1^\top = \begin{pmatrix} 5.68 & -1.68 \\ -1.68 & 3.21 \end{pmatrix}$, far from the identity.

## Relation to other models

- **PCA.** The linear autoencoder with squared loss has the same optimal subspace as PCA, and its optimal reconstruction $P x$ is the PCA reconstruction. PCA gives an orthonormal basis ordered by variance; the autoencoder gives some basis of the same subspace.
- **Probabilistic PCA.** [Probabilistic PCA](/probabilistic-pca/) is a latent variable model whose maximum likelihood solution spans the same subspace. It adds a noise variance and a density, which the plain autoencoder does not have.
- **Variational autoencoder.** The [variational autoencoder](/variational-autoencoder/) makes the encoder output a distribution over codes and the decoder a likelihood, and trains both on the [evidence lower bound](/evidence-lower-bound/). It is a generative model; the autoencoder is not, since points drawn in the code space need not decode to plausible inputs.
- **Kernel PCA and manifold methods.** [Kernel PCA](/kernel-pca/), [Isomap](/isomap/) and similar methods also give nonlinear codes, but they have no decoder and no map for new points without extra work. An autoencoder gives both maps.
- **Principal curves.** A [principal curve](/principal-curves/) is a one-dimensional nonlinear decoder, with the projection index as the encoder.

## Known results in the model

### The linear autoencoder spans the PCA subspace

Let the eigenvalues of $S$ be $\lambda_1 \ge \cdots \ge \lambda_d$ with $\lambda_k > \lambda_{k+1}$, let $V_k$ hold the top $k$ unit eigenvectors as columns, and let $S$ be invertible.

**Theorem** (Bourlard and Kamp 1988; Baldi and Hornik 1989). The smallest value of $L$ is $\sum_{j > k} \lambda_j$. It is reached exactly when $W_2 = V_k C$ and $W_1 = C^{-1} V_k^\top$ for some invertible $k \times k$ matrix $C$.

*Proof.* Put the centered data in the columns of $X \in \mathbb{R}^{d \times n}$, so $L = \frac{1}{n} \|X - P X\|_F^2$ with $P = W_2 W_1$ of rank at most $k$. The matrix $P X$ has rank at most $k$, so by the Eckart-Young theorem $\|X - P X\|_F^2 \ge \sum_{j > k} \sigma_j^2$, where the $\sigma_j$ are the singular values of $X$ and $\sigma_j^2 = n \lambda_j$. Equality holds only for the truncated SVD, $P X = V_k V_k^\top X$, which is unique because $\lambda_k > \lambda_{k+1}$. Since $S$ is invertible, $X$ has full row rank, so $P = V_k V_k^\top$. Then $P$ has rank $k$, the range of $W_2$ is the range of $P$, so $W_2 = V_k C$ with $C$ invertible, and $V_k C W_1 = V_k V_k^\top$ gives $W_1 = C^{-1} V_k^\top$. Conversely, every such pair gives $P = V_k V_k^\top$. $\square$

So only the subspace is fixed. The encoder rows and decoder columns span the top-$k$ eigenspace, but $W_1 W_1^\top = C^{-1} C^{-\top}$ is the identity only when $C$ is orthogonal. To read off the principal directions, orthonormalize the columns of $W_2$ and diagonalize the $k \times k$ matrix $W_2^\top S W_2$ in that basis.

### No bad local minima

Baldi and Hornik (1989) also showed that, when the eigenvalues of $S$ are distinct, every critical point of $L$ with $P$ of full rank $k$ is of the form $P = V_I V_I^\top$, for a set $I$ of $k$ eigenvectors. Every choice of $I$ other than the top $k$ gives a saddle point. So gradient descent from a generic start does not get stuck in a local minimum, which is what the tests see.

### Gradient flow keeps the layers balanced

**Proposition** (a case of Du, Hu and Lee 2018). Under gradient flow $\dot W_1 = -\partial L/\partial W_1$, $\dot W_2 = -\partial L/\partial W_2$, the matrix $W_1 W_1^\top - W_2^\top W_2$ is constant.

*Proof.* With the gradients above, $\frac{d}{dt}(W_1 W_1^\top) = 2 W_2^\top R W_1^\top + 2 W_1 R^\top W_2$ and $\frac{d}{dt}(W_2^\top W_2) = 2 W_1 R^\top W_2 + 2 W_2^\top R W_1^\top$, which are equal. $\square$

At a minimum, $W_1 W_1^\top - W_2^\top W_2 = C^{-1} C^{-\top} - C^\top C$. From a small random start this difference is near 0, so $C^\top C \approx I$, and the weights come out nearly orthonormal. From an unbalanced start they do not, as in the example above. The orthogonality seen in practice is a property of the training, not of the model.

### Nonlinear units do not help in one hidden layer

Bourlard and Kamp (1988) showed that with one hidden layer and linear outputs, nonlinear hidden units cannot give a lower squared error than the linear optimum: the best the network can do is the truncated SVD. A nonlinear autoencoder can beat PCA only with more layers. Hinton and Salakhutdinov (2006) trained deep autoencoders with a 30-unit code, pretrained layer by layer, and got lower reconstruction errors than PCA with 30 components on images of digits and faces.

### Without a bottleneck or a penalty, the identity is optimal

If $k \ge d$, then $W_2 W_1 = I$ gives $L = 0$, and the code need not show any structure of the data. The same holds for a nonlinear network with enough capacity, even with $k < d$: in principle it can map each training point to its own code and back. This is why the denoising, sparse and contractive penalties, or a small $k$ together with a limited network, are needed for a useful code.

## References
