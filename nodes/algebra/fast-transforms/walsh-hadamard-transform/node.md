---
tag: 93FVVX
kind: problem
slug: walsh-hadamard-transform
name: Walsh-Hadamard transform
aliases:
- WHT
- Hadamard transform
- Walsh transform
- discrete Walsh transform
area: algebra/fast-transforms
level: core
summary: Transform with +1/-1 kernel defined by a Hadamard matrix of order 2^k.
model: real-ram
complexity:
  vars: {n: the transform length (a power of two)}
  time: {worst: O(n log n)}
prereqs: [kronecker-product, bitwise-operations, discrete-fourier-transform]
see_also: [fast-walsh-hadamard-transform, multidimensional-fft, sum-over-subsets, fourier-analysis-of-boolean-functions, hadamard-code, reed-muller-code, hadamard-gate, gray-code]
sources:
  - paper: doi:10.1080/14786446708639914
    title: James Joseph Sylvester, Thoughts on inverse orthogonal matrices, simultaneous sign-successions, and tessellated pavements in two or more colours, Philosophical Magazine 34(232), 1867
    locator: pp. 461 to 475 (the doubling construction of matrices of signs with orthogonal rows)
  - paper: doi:10.2307/2387224
    title: Joseph L. Walsh, A closed set of normal orthogonal functions, American Journal of Mathematics 45(1), 1923
    locator: pp. 5 to 24 (the Walsh functions)
  - paper: doi:10.1109/TC.1976.1674569
    title: Bruce J. Fino and V. Ralph Algazi, Unified matrix treatment of the fast Walsh-Hadamard transform, IEEE Transactions on Computers C-25(11), 1976
    locator: pp. 1142 to 1146 (the natural, dyadic and sequency orderings as factorizations of the Hadamard matrix)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 23, Walsh transforms (the Walsh-Kronecker basis, the orderings and dyadic convolution)
  - book: isbn:9781107038325
    title: Ryan O'Donnell, Analysis of Boolean Functions, Cambridge University Press, 2014
    locator: Chapter 1, Boolean functions and the Fourier expansion (the Fourier coefficients of a function on the Boolean cube)
  - paper: doi:10.1145/321752.321761
    title: Jacques Morgenstern, Note on a lower bound on the linear complexity of the fast Fourier transform, Journal of the ACM 20(2), 1973
    locator: pp. 305 to 306 (the determinant argument for linear algorithms with bounded constants)
  - url: https://en.wikipedia.org/wiki/Hadamard_transform
    title: Hadamard transform, Wikipedia
    locator: the definition, the orderings and the history of the names
---

The Walsh-Hadamard transform (WHT) of a vector $x$ of length $n = 2^t$ is $y = H_n x$, where $H_n$ is the $n \times n$ matrix with entries $(H_n)_{kj} = (-1)^{\mathrm{popcount}(j \wedge k)}$, a sign $\pm 1$ that depends on how many binary digits $j$ and $k$ share. It is the discrete Fourier transform of the group $(\mathbb{Z}/2\mathbb{Z})^t$ of bit strings under XOR, with $-1$ in the role of the root of unity, so it needs no multiplications at all. It is its own inverse up to the factor $1/n$, it turns XOR convolution into a pointwise product, and it computes the Fourier coefficients of functions on the Boolean cube. The [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/) computes it with $n \lg n$ additions and subtractions.

## In plain words

Write each position of the input as a string of binary digits. For each output position, pick out the binary digits that are set in it, and add up the inputs, giving a minus sign to those inputs whose position shares an odd number of the picked digits. The first output is the plain sum. Each other output compares one half of the inputs against the other half, for some way of splitting them by their binary digits. Doing the transform twice gives back the input times its length.

## Definition

**Notation.** $n = 2^t$ is the transform length, and it must be a power of two. For $0 \le j, k < n$, $j \wedge k$ is the bitwise AND of the binary representations, $j \oplus k$ the bitwise XOR, and $\langle j, k \rangle = \mathrm{popcount}(j \wedge k)$, the number of positions where both have a $1$. The Hadamard matrix in natural (Sylvester) order is

$$H_1 = (1), \qquad H_{2m} = \begin{pmatrix} H_m & H_m \\ H_m & -H_m \end{pmatrix}, \qquad (H_n)_{kj} = (-1)^{\langle j, k \rangle},$$

so $H_n = H_2^{\otimes t}$, the $t$-fold [Kronecker product](/kronecker-product/) of $H_2 = \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$. The two descriptions agree because the top binary digit of $j$ and $k$ selects the block and contributes the sign of the lower right block.

**Input.** $x \in R^n$, for a commutative ring $R$: the integers, $\mathbb{Z}/p\mathbb{Z}$, $\mathbb{R}$ or $\mathbb{C}$.

**Output.** $y = H_n x$, that is

$$y_k = \sum_{j=0}^{n-1} (-1)^{\langle j, k \rangle} x_j, \qquad 0 \le k < n.$$

**Normalization.** This page uses the unnormalized transform above. Since the rows of $H_n$ are orthogonal and $H_n$ is symmetric, $H_n^2 = n I$, so the inverse is $x = \frac{1}{n} H_n y$. The inverse exists exactly when $n$ is a unit of $R$, which fails in characteristic $2$, where $H_n$ is the all-ones matrix. Two other scalings are common: the orthonormal one, $\frac{1}{\sqrt n} H_n$, which is symmetric, orthogonal and its own inverse; and the probabilistic one used in the analysis of Boolean functions, $\hat f(k) = \frac{1}{n} (H_n f)_k$, which is the average of $f(j) (-1)^{\langle j, k \rangle}$ over $j$.

**As a Fourier transform.** The characters of the group $G = (\mathbb{Z}/2\mathbb{Z})^t$, written as integers $0, \ldots, n - 1$ under $\oplus$, are the maps $\chi_k(j) = (-1)^{\langle j, k \rangle}$, and $\chi_k(i \oplus j) = \chi_k(i) \chi_k(j)$ because $\langle i \oplus j, k \rangle \equiv \langle i, k \rangle + \langle j, k \rangle \pmod 2$. The WHT is the Fourier transform of $G$. Equivalently, it is the $t$-dimensional DFT of size $2 \times 2 \times \cdots \times 2$, with $\omega_2 = -1$ on every axis, which is the case $n_a = 2$ of the [multidimensional FFT](/multidimensional-fft/).

**Names.** Sylvester (1867) gave the doubling construction $H_{2m} = \begin{pmatrix} H_m & H_m \\ H_m & -H_m \end{pmatrix}$ of sign matrices with orthogonal rows. Hadamard (1893) studied $\pm 1$ matrices of maximal determinant, and such matrices now carry his name. Walsh (1923) introduced the Walsh functions, a complete orthonormal system of $\pm 1$ step functions on the unit interval, whose samples are the rows of $H_n$ in sequency order. Fino and Algazi (1976) gave a unified treatment of the fast algorithms for the natural, dyadic and sequency orderings as factorizations of the Hadamard matrix.

**Cost model.** Additions and subtractions in $R$, counted together. The transform needs no multiplications; the inverse adds $n$ divisions by $n$, or one shift each in binary arithmetic when $R = \mathbb{Z}$ and the result is known to be integral.

## Variants

- **Orderings.** The rows of $H_n$ are the Walsh functions sampled at $n$ points. The natural (Hadamard or Sylvester) order above is the Kronecker order. The *sequency* (Walsh) order sorts the rows by their number of sign changes; for $n = 8$ the rows in natural order have $0, 7, 3, 4, 1, 6, 2, 5$ sign changes. The *dyadic* (Paley) order sits between them. They differ by a bit reversal and a [Gray code](/gray-code/) permutation of the outputs, and Fino and Algazi (1976) treat all three as factorizations of one matrix.
- **Normalizations.** Unnormalized ($H_n$ forward, $\frac1n H_n$ inverse), orthonormal ($\frac{1}{\sqrt n} H_n$ both ways), or probabilistic ($\frac1n H_n$ forward, $H_n$ inverse).
- **XOR (dyadic) convolution.** Given $a, b \in R^n$, compute $c_k = \sum_{i \oplus j = k} a_i b_j$. The transform diagonalizes it: $H_n c = (H_n a) \cdot (H_n b)$ entrywise.
- **Other finite abelian groups.** For $(\mathbb{Z}/m\mathbb{Z})^t$ the same construction with an $m$-th root of unity gives the generalized Walsh or Chrestenson transform, again a multidimensional DFT.
- **Other Hadamard matrices.** Hadamard matrices, $\pm 1$ matrices with $H H^{\mathsf T} = n I$, exist for other orders such as $12$ and $20$, but they are not Kronecker powers of $H_2$ and have no comparable fast algorithm in general; the WHT always means the Sylvester family.

## Examples

**Small sizes.** $H_1 x = x$. For $n = 2$, $(u, v) \mapsto (u + v, u - v)$; for example $(5, 7) \mapsto (12, -2)$. For $n = 4$,

$$H_4 = \begin{pmatrix} 1 & 1 & 1 & 1 \\ 1 & -1 & 1 & -1 \\ 1 & 1 & -1 & -1 \\ 1 & -1 & -1 & 1 \end{pmatrix}.$$

An impulse $(1, 0, 0, 0)$ maps to the constant $(1, 1, 1, 1)$, and the constant maps to $(4, 0, 0, 0)$.

**A length-8 vector.** For $x = (3, 1, 4, 1, 5, 9, 2, 6)$, $H_8 x = (31, -3, 5, -1, -13, 13, -7, -1)$. The entry $k = 0$ is the sum. The entry $k = 4 = 100_2$ puts a minus sign on positions $4$ to $7$, whose top digit is set: $3 + 1 + 4 + 1 - 5 - 9 - 2 - 6 = -13$. Applying $H_8$ again and dividing by $8$ returns $x$.

**XOR convolution.** For $a = (1, 2, 3, 4)$ and $b = (5, 6, 7, 8)$, $H_4 a = (10, -2, -4, 0)$ and $H_4 b = (26, -2, -4, 0)$; the products are $(260, 4, 16, 0)$, and $\frac14 H_4$ of them is $c = (70, 68, 62, 60)$. Directly, $c_0 = \sum_i a_i b_i = 70$ and $c_1 = a_0 b_1 + a_1 b_0 + a_2 b_3 + a_3 b_2 = 6 + 10 + 24 + 28 = 68$.

**A Boolean function.** Let $f(j) = -1$ if at least two of the three digits of $j$ are $1$ and $f(j) = 1$ otherwise, the majority of three bits in $\pm 1$ form. Indexed by $j = 0, \ldots, 7$, $f = (1, 1, 1, -1, 1, -1, -1, -1)$, and $\frac18 H_8 f = (0, \frac12, \frac12, 0, \frac12, 0, 0, -\frac12)$. So the majority has weight $\frac12$ on each single bit and $-\frac12$ on the parity of all three, the familiar expansion $\mathrm{Maj}_3 = \frac12 (x_1 + x_2 + x_3) - \frac12 x_1 x_2 x_3$ in $\pm 1$ variables. The squares sum to $1$, as Parseval's identity requires for a $\pm 1$ function.

All the numbers above were checked by a script.

## Known algorithms

| algorithm | additions | multiplications | notes |
|---|---|---|---|
| direct matrix-vector product | $n(n - 1)$ | $0$ | each output is a signed sum of $n$ inputs |
| [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/) | $n \lg n$ | $0$ | $H_n = \prod_{q} (I_{2^q} \otimes H_2 \otimes I_{n / 2^{q+1}})$; in place |
| [multidimensional FFT](/multidimensional-fft/) with all $n_a = 2$ | $n \lg n$ | $0$ after removing the factors $\omega^0 = 1$ | the same computation seen as a DFT |

The fast algorithm is the radix-2 FFT without twiddle factors: the factorization of $H_n$ into $t$ sparse factors has the same shape as the Cooley-Tukey factorization of the DFT matrix, but every factor is $\pm 1$, so each butterfly is $(u, v) \mapsto (u + v, u - v)$.

## Bounds

**Upper bound.** $n \lg n$ additions and subtractions and no multiplications, by the fast algorithm; $n \lg n + n$ operations for the inverse.

**Lower bound with bounded constants.** In the model of linear algorithms where each step forms $\alpha u + \beta v$ from two earlier values with $|\alpha|, |\beta| \le 1$, every algorithm for $H_n$ over $\mathbb{R}$ needs at least $\frac{n}{2} \lg n$ steps. This is Morgenstern's determinant argument (1973), stated there for the DFT, applied to $H_n$: the largest absolute determinant of $n$ of the linear forms built so far starts at $1$ (the inputs form the identity) and at most doubles in one step, since replacing a form by $\alpha u + \beta v$ splits the determinant into $\alpha$ times one and $\beta$ times another, while the outputs include the rows of $H_n$ and and $|\det H_n| = n^{n/2}$ because $H_n H_n^{\mathsf T} = n I$. So at least $\log_2 n^{n/2} = \frac{n}{2} \lg n$ steps are needed. The fast algorithm is within a factor $2$ of this bound. (We derive this case from the argument; Morgenstern's paper states the DFT case.)

**Without the restriction.** With unbounded constants no lower bound of order $n \log n$ is known for the WHT, as for the DFT; the trivial bound is $n - 1$ additions for the first output alone.

## Reductions

- **XOR convolution to the WHT.** $c = \frac{1}{n} H_n((H_n a) \cdot (H_n b))$, in $3 n \lg n$ additions, $n$ multiplications and $n$ divisions, against $n^2$ multiplications directly. The proof is the character identity: $(H_n c)_k = \sum_{i, j} a_i b_j \chi_k(i \oplus j) = (H_n a)_k (H_n b)_k$. This is the [convolution theorem](/convolution-theorem/) for the group $(\mathbb{Z}/2\mathbb{Z})^t$.
- **OR and AND convolution.** These use the zeta and Möbius transforms over subsets ([sum over subsets](/sum-over-subsets/) and [Möbius inversion](/mobius-inversion/)), with the butterfly $(u, v) \mapsto (u, u + v)$ and its inverse; the WHT is the analogous transform for XOR.
- **The WHT to the multidimensional DFT.** As above, it is the DFT on the group $(\mathbb{Z}/2\mathbb{Z})^t$, so any multidimensional FFT computes it.
- **Boolean Fourier coefficients to the WHT.** For $f : \{0, 1\}^t \to \mathbb{R}$ given by its truth table, $\hat f = \frac1n H_n f$ lists all $2^t$ Fourier coefficients ([Fourier analysis of Boolean functions](/fourier-analysis-of-boolean-functions/)) in $n \lg n$ additions.

## Applications

- **Analysis of Boolean functions and cryptography.** The Walsh spectrum of a Boolean function measures its correlation with every linear function; it is used in [linear cryptanalysis](/linear-cryptanalysis/) and in the design of S-boxes, and the Fourier coefficients appear in learning theory and property testing.
- **Coding theory.** The rows of $H_n$ and their negatives form the [Hadamard code](/hadamard-code/), the first-order [Reed-Muller code](/reed-muller-code/); maximum-likelihood decoding computes the correlation of the received word with every codeword, which is one WHT.
- **Quantum computing.** Applying the [Hadamard gate](/hadamard-gate/) to each of $t$ qubits applies $\frac{1}{\sqrt n} H_n$ to the $n = 2^t$ amplitudes, the first step of the [Deutsch-Jozsa](/deutsch-jozsa-algorithm/), [Bernstein-Vazirani](/bernstein-vazirani-algorithm/) and [Simon](/simon-algorithm/) algorithms.
- **Signal and image processing.** As a multiplication-free orthogonal transform, it is used for compression and for spreading codes.
- **Set-function algorithms.** XOR convolution of functions on subsets of a $t$-element set, for example in counting problems and games on bit masks.

## References
