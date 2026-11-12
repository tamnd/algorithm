---
tag: 4044MK
kind: technique
slug: kernel-trick
name: Kernel trick
aliases:
- kernel substitution
area: machine-learning/supervised-learning
level: core
summary: Write a linear method so that the data enter only through inner products, then replace each inner product by a PSD kernel k(x, z) = φ(x)·φ(z) without forming φ.
prereqs: [positive-definite-matrix]
see_also: [mercer-theorem, representer-theorem, support-vector-machine, kernel-ridge-regression, perceptron, kernel-pca, gaussian-process, linear-separability]
sources:
  - paper: "M. A. Aizerman, E. M. Braverman and L. I. Rozonoer, Theoretical foundations of the potential function method in pattern recognition learning, Automation and Remote Control 25, 1964"
    locator: pp. 821 to 837 (the potential function as an inner product in a feature space, and the kernelized perceptron)
  - paper: doi:10.1145/130385.130401
    title: Bernhard E. Boser, Isabelle M. Guyon and Vladimir N. Vapnik, A training algorithm for optimal margin classifiers, COLT 1992
    locator: pp. 144 to 152 (the maximum margin classifier with a kernel in place of the inner product)
  - paper: "Ali Rahimi and Benjamin Recht, Random features for large-scale kernel machines, Advances in Neural Information Processing Systems 20, 2007"
    locator: random Fourier features for shift-invariant kernels
  - paper: "Charles A. Micchelli, Interpolation of scattered data: distance matrices and conditionally positive definite functions, Constructive Approximation 2, 1986"
    locator: pp. 11 to 22 (the Gaussian Gram matrix of distinct points is positive definite)
  - book: isbn:9780262194754
    title: Bernhard Schölkopf and Alexander J. Smola, Learning with Kernels, MIT Press, 2002
    locator: Chapter 2 (kernels, feature spaces and the kernel trick) and Chapter 13 (designing kernels)
  - book: isbn:9780521813976
    title: John Shawe-Taylor and Nello Cristianini, Kernel Methods for Pattern Analysis, Cambridge University Press, 2004
    locator: Chapter 2 (the kernel approach) and Chapter 3 (properties of kernels, closure properties)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 6.1 (dual representations) and Section 6.2 (constructing kernels)
---

The kernel trick turns a linear method into a nonlinear one without computing a feature map. If a learning method uses the data only through inner products $x_i \cdot x_j$, replace each of them by a kernel $k(x_i, x_j)$. When $k$ is symmetric and positive semidefinite, it equals an inner product $\varphi(x_i) \cdot \varphi(x_j)$ in some feature space, so the method runs as if on the points $\varphi(x_i)$, even when that space has a very large or infinite dimension. The [support vector machine](/support-vector-machine/), [kernel ridge regression](/kernel-ridge-regression/), the kernel [perceptron](/perceptron/) and [kernel PCA](/kernel-pca/) are all built this way.

## In plain words

A straight line cannot split some data, such as the XOR pattern. If you add new features, for example the product of two coordinates, a straight line in the larger space may split it. But the larger space can be huge.

Many methods never look at a single point on its own. They only ask how similar two points are, by their inner product. So you only need the inner products in the larger space, not the points there. A kernel is a function that gives these inner products directly from the original points, often at the cost of one inner product in the original space. Replace every inner product by the kernel, and the method works in the larger space for free.

## When it applies

The trick needs two things.

1. **A dual form.** The method must use the inputs only through inner products, in training and in prediction. This is true when the weight vector is a combination $w = \sum_i a_i x_i$ of the training points, so that $w \cdot x = \sum_i a_i\, x_i \cdot x$. The [representer theorem](/representer-theorem/) says when a regularized method has such a solution.
2. **A positive semidefinite kernel.** The function $k : \mathcal{X} \times \mathcal{X} \to \mathbb{R}$ must be symmetric, and every Gram matrix $K_{ij} = k(x_i, x_j)$ on a finite set of points must be [positive semidefinite](/positive-definite-matrix/). Then a feature map exists: the Moore-Aronszajn theorem gives a Hilbert space $\mathcal{H}$ with $\varphi(x) = k(x, \cdot)$ and $k(x, z) = \langle \varphi(x), \varphi(z) \rangle_{\mathcal{H}}$. [Mercer's theorem](/mercer-theorem/) gives a concrete feature map with eigenfunctions when $k$ is continuous on a compact domain.

The inputs need not be vectors. Any set with a PSD kernel works, such as strings, trees or graphs.

## The template

```pseudo id=main
KERNELIZE(A, k, S)                              ▷ A: a linear method, k: a PSD kernel, S = (x_1, ..., x_n)
L1  write A with w = Σ_i a_i φ(x_i)              ▷ hole: the dual form of A, with coefficients a
L2  so that each x_i · x_j and each x_i · x appears only as an inner product   ▷ hole: the rewrite
L3  K[i][j] ← k(x_i, x_j) for i, j ← 1 to n      ▷ hole: the kernel
L4  a ← run A on K instead of on the vectors x_i ▷ hole: the solver of A
L5  return f(x) = Σ_i a_i k(x_i, x)              ▷ prediction needs only kernel values
```

Line L1 is the step that needs thought. Line L3 costs $\Theta(n^2)$ kernel evaluations and $\Theta(n^2)$ memory. Line L5 costs $n$ kernel evaluations per prediction, or as many as there are nonzero $a_i$.

**Explicit feature maps.** For the polynomial kernel $k(x, z) = (x \cdot z + c)^p$ with $c \ge 0$, the multinomial theorem gives

$$(c + \textstyle\sum_{j} x_j z_j)^p = \sum_{k_0 + k_1 + \cdots + k_d = p} \binom{p}{k_0, k_1, \ldots, k_d} c^{k_0} \prod_{j} (x_j z_j)^{k_j},$$

so $\varphi(x)$ has one coordinate $\sqrt{\binom{p}{k_0, \ldots, k_d} c^{k_0}}\, \prod_j x_j^{k_j}$ for each exponent vector. There are $\binom{d + p}{p}$ coordinates when $c > 0$, and $\binom{d + p - 1}{p}$ when $c = 0$. For $d = 2$ and $p = 2$, $c = 1$:

$$\varphi(x) = (1, \sqrt 2 x_1, \sqrt 2 x_2, x_1^2, \sqrt 2 x_1 x_2, x_2^2).$$

The kernel costs $O(d)$, while $\varphi$ has $\Theta(d^p)$ coordinates for fixed $p$.

**The Gaussian kernel has an infinite feature space.** For $k(x, z) = \exp(-\lVert x - z \rVert^2 / 2\sigma^2)$ in one dimension,

$$k(x, z) = e^{-x^2/2\sigma^2} e^{-z^2/2\sigma^2} e^{xz/\sigma^2} = \sum_{m=0}^{\infty} \varphi_m(x) \varphi_m(z), \qquad \varphi_m(x) = e^{-x^2/2\sigma^2} \frac{x^m}{\sigma^m \sqrt{m!}}.$$

No finite map works. The Gram matrix of $n$ distinct points is positive definite for every $n$ (Micchelli 1986), so its rank is $n$, while a feature map of dimension $D$ gives a Gram matrix of rank at most $D$.

**Closure rules.** If $k_1$ and $k_2$ are PSD kernels, then so are:

- $k_1 + k_2$, because a sum of PSD matrices is PSD;
- $a k_1$ for $a \ge 0$;
- $k_1 k_2$, because the elementwise (Schur) product of PSD matrices is PSD, with the feature map $\varphi_1 \otimes \varphi_2$;
- $f(x) k_1(x, z) f(z)$ for any function $f$, because $D K D$ is PSD for a diagonal $D$;
- $\exp(k_1)$, the limit of the partial sums $\sum_{m \le M} k_1^m / m!$, each PSD by the rules above, and the PSD matrices form a closed set;
- $k_1(\psi(x), \psi(z))$ for any map $\psi$.

The Gaussian kernel follows: $\exp(x \cdot z/\sigma^2)$ is PSD by the exp rule, and the rule for $f(x) = e^{-\lVert x \rVert^2/2\sigma^2}$ gives $k$. A difference $k_1 - k_2$ is not PSD in general.

## Classic examples

- **The kernel [perceptron](/perceptron/).** The perceptron's weights are $w = \sum_i a_i y_i x_i$, where $a_i$ counts the mistakes on $x_i$. The test $y_i\, w \cdot x_i \le 0$ becomes $y_i \sum_j a_j y_j k(x_j, x_i) \le 0$. Aizerman, Braverman and Rozonoer used this in 1964. With $k(x, z) = (x \cdot z + 1)^2$, the kernel perceptron learns XOR on $\{0, 1\}^2$: the eighth pass makes no mistake, and the mistake counts are $a = (7, 5, 5, 4)$ in the order $(0,0), (0,1), (1,0), (1,1)$. With the linear kernel $x \cdot z + 1$, it never stops.
- **The [support vector machine](/support-vector-machine/).** Its dual problem uses the data only through $y_i y_j x_i \cdot x_j$. Boser, Guyon and Vapnik (1992) replaced these by $k(x_i, x_j)$.
- **[Kernel ridge regression](/kernel-ridge-regression/).** Ridge regression in feature space has the solution $f(x) = \sum_i \alpha_i k(x_i, x)$ with $\alpha = (K + \lambda I)^{-1} y$.
- **[Kernel PCA](/kernel-pca/) and [kernel k-means](/kernel-k-means/).** Principal components and cluster distances need only inner products, after centering in feature space.
- **[Gaussian processes](/gaussian-process/).** The kernel is the covariance function, and the posterior mean has the same form as kernel ridge regression.

## Variations

- **Random features.** Rahimi and Recht (2007) approximate a shift-invariant kernel by $k(x, z) \approx z(x) \cdot z(z)$ with $D$ random cosine features drawn from the Fourier transform of the kernel. Then a linear method on $D$ features avoids the $n \times n$ Gram matrix.
- **The Nyström method.** It approximates $K$ by a low-rank matrix built from $m \ll n$ columns.
- **Kernels on structures.** String kernels, tree kernels and graph kernels compare discrete objects by counting shared substructures, often by dynamic programming.
- **Learned and limiting kernels.** The [neural tangent kernel](/neural-tangent-kernel/) describes very wide neural networks trained by gradient descent.
- **Conditionally positive definite kernels.** Some methods, such as those that are invariant to a shift of the origin, need $c^\top K c \ge 0$ only for $c$ with $\sum_i c_i = 0$. The kernel $-\lVert x - z \rVert$ is of this type.

## Pitfalls

- **A similarity function is not always a kernel.** The function $\lvert x - z \rvert$ has the Gram matrix $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ on the points 0 and 1, with eigenvalue $-1$. The sigmoid $\tanh(x \cdot z - 1)$ is negative at $x = z = 0$, so it cannot be an inner product $\varphi(x) \cdot \varphi(x) \ge 0$. With such a function, a convex method such as the SVM can lose its convexity.
- **The Gram matrix grows as $n^2$.** For $n = 10^6$ points it has $10^{12}$ entries. Exact kernel methods suit small and medium $n$; random features or the Nyström method suit large $n$.
- **Prediction costs grow with $n$.** Each prediction needs one kernel value per training point with a nonzero coefficient. The SVM helps here, because most coefficients are zero.
- **The bandwidth matters.** A Gaussian kernel with a very small $\sigma$ gives a Gram matrix close to $I$, which memorizes the data. A very large $\sigma$ gives a matrix close to the all-ones matrix, which is close to a constant model. Choose $\sigma$ by validation, after scaling the features.
- **Floating point Gram matrices can lose PSD.** Rounding can give tiny negative eigenvalues. Add a small multiple of $I$ (a jitter) before a Cholesky factorization.
- **The feature map is not unique.** Different maps can give the same kernel, so a statement about "the" feature space means the reproducing kernel Hilbert space.

## Exercises

1. Show that $\varphi$ above for $d = 2$, $p = 2$, $c = 1$ satisfies $\varphi(x) \cdot \varphi(z) = (x \cdot z + 1)^2$ by expanding both sides.
2. Show that the Gram matrix of $(x \cdot z + 1)^2$ on any $n \ge 4$ points of $\mathbb{R}$ has rank at most 3. Check it on the points $-3, -1, 0, 2, 5, 7$, where the rank is exactly 3.
3. Prove that $\min(x, z)$ is a PSD kernel on $[0, \infty)$ by writing it as $\int_0^\infty \mathbf{1}[t \le x] \mathbf{1}[t \le z]\, dt$.
4. Find two points that show that $k_1 - k_2$ is not PSD for $k_1(x, z) = xz$ and $k_2(x, z) = 2xz$.

## References
