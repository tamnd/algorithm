---
tag: E3XY86
kind: algorithm
slug: fast-walsh-hadamard-transform
name: Fast Walsh-Hadamard transform
aliases:
- FWHT
- fast Hadamard transform
- fast Walsh transform
area: algebra/fast-transforms
level: core
summary: In-place butterfly computation of the WHT in O(n log n) additions and subtractions.
solves: [walsh-hadamard-transform]
model: real-ram
complexity:
  vars: {n: the transform length (a power of two)}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: O(1)}
  additions: {worst: n lg n}
  multiplications: {worst: 0}
properties: {deterministic: true, recursive: false, in_place: true}
prereqs: [walsh-hadamard-transform, butterfly-operation, bitwise-operations]
see_also: [fast-fourier-transform, sum-over-subsets, fourier-analysis-of-boolean-functions, hadamard-code, reed-muller-code, kronecker-product, convolution-theorem, haar-wavelet-transform]
sources:
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 23, Walsh transforms, Section 23.1 (the Walsh-Kronecker basis and the radix-2 algorithm), Section 23.8 (dyadic or XOR convolution) and Section 23.12 (OR and AND convolution)
  - paper: doi:10.1109/TC.1976.1674569
    title: Bruce J. Fino and V. Ralph Algazi, Unified matrix treatment of the fast Walsh-Hadamard transform, IEEE Transactions on Computers C-25(11), 1976
    locator: pp. 1142 to 1146 (the fast algorithms for the natural, dyadic and sequency orderings as factorizations of the Hadamard matrix)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 1, Section 1.1 (Kronecker products), and Section 1.3, The Cooley-Tukey Factorization (the same factorization pattern with twiddle factors)
  - paper: doi:10.2307/2387224
    title: Joseph L. Walsh, A closed set of normal orthogonal functions, American Journal of Mathematics 45(1), 1923
    locator: pp. 5 to 24 (the Walsh functions)
  - paper: doi:10.1145/321752.321761
    title: Jacques Morgenstern, Note on a lower bound on the linear complexity of the fast Fourier transform, Journal of the ACM 20(2), 1973
    locator: pp. 305 to 306 (the determinant argument for linear algorithms with bounded constants)
---

The fast Walsh-Hadamard transform (FWHT) computes the [Walsh-Hadamard transform](/walsh-hadamard-transform/) $y = H_n x$, with $y_k = \sum_j (-1)^{\langle j, k \rangle} x_j$, in $n \lg n$ additions and subtractions and no multiplications, for $n$ a power of two. Here $\langle j, k \rangle$ is the number of binary positions where both $j$ and $k$ have a $1$. The algorithm is the radix-2 [FFT](/fast-fourier-transform/) with every twiddle factor equal to $1$: $\lg n$ stages of $n/2$ [butterflies](/butterfly-operation/) $(u, v) \mapsto (u + v, u - v)$, in place and with no bit reversal. It is the transform behind XOR convolution, the Fourier analysis of Boolean functions, and the decoding of Hadamard and first-order Reed-Muller codes.

## In plain words

Number the entries of a list from zero and write the numbers in binary. The transform asks, for each pattern of binary positions, how the entries add up when each entry gets a plus or a minus sign by a simple rule: count the positions of the pattern where the entry's number also has a one, and use a minus when that count is odd.

Done directly, each answer looks at every entry. The fast method treats one binary position at a time. For the lowest position it pairs each entry with its neighbour and replaces the pair by their sum and their difference. Then it does the same with pairs two apart, then four apart, and so on. Each round costs one addition or subtraction per entry, and after one round per binary position the answer is complete. It needs no multiplications at all.

## The problem

**Notation.** $n = 2^t$ is the transform length, and it must be a power of two. For $0 \le j, k < n$, $j \wedge k$ is the bitwise AND and $\langle j, k \rangle = \mathrm{popcount}(j \wedge k)$. The Hadamard matrix in natural (Sylvester) order is

$$H_1 = (1), \qquad H_{2m} = \begin{pmatrix} H_m & H_m \\ H_m & -H_m \end{pmatrix}, \qquad (H_n)_{kj} = (-1)^{\langle j, k \rangle},$$

so $H_n = H_2 \otimes H_2 \otimes \cdots \otimes H_2$ ($t$ factors), a [Kronecker product](/kronecker-product/). This is the DFT of the group $(\mathbb{Z}/2\mathbb{Z})^t$, whose characters are $j \mapsto (-1)^{\langle j, k \rangle}$; the role of $\omega$ is played by $-1$.

**Input.** $x \in R^n$, for a commutative ring $R$ (the integers, $\mathbb{Z}/p\mathbb{Z}$, $\mathbb{R}$ or $\mathbb{C}$).

**Output.** $y = H_n x$. The inverse is $x = \frac{1}{n} H_n y$, since $H_n^2 = nI$; it needs $n$ to be a unit, so $R$ must not have characteristic $2$. Some texts scale by $1/\sqrt n$ on both sides, which makes the transform orthogonal and its own inverse.

**Cost model.** Additions and subtractions in $R$, counted together as additions. The algorithm uses no multiplications; the inverse adds $n$ divisions by $n$.

## The algorithm

```pseudo id=main
FWHT(x)                 ▷ x[0 .. n − 1] with n = 2^t
L1  n ← |x|
L2  h ← 1                                  ▷ the binary position being treated is lg h
L3  while h < n do
L4      for s ← 0 to n − 1 step 2h do      ▷ the block x[s .. s + 2h − 1]
L5          for j ← s to s + h − 1 do
L6              u ← x[j], v ← x[j + h]
L7              x[j] ← u + v, x[j + h] ← u − v
L8      h ← 2h

INVERSE-FWHT(y)         ▷ n must be a unit of R
L9  FWHT(y)
L10 for j ← 0 to n − 1 do y[j] ← y[j] / n
```

The indices $j$ and $j + h$ differ exactly in the binary position $\lg h$, and the pass over $h$ applies $H_2$ along that position to every pair. Because the factors $I \otimes H_2 \otimes I$ for different positions commute, the order of the passes does not matter, and no bit reversal is needed. Over the integers the entries grow by at most a factor of $2$ per pass, so $|y_k| \le n \max_j |x_j|$: the output needs $\lg n$ more binary digits than the input.

## Example

Transform $x = (3, 1, 4, 1, 5, 9, 2, 6)$, with $n = 8$.

| step | pairs | the array |
|---|---|---|
| input | | 3 1 4 1 5 9 2 6 |
| h = 1 | (0,1) (2,3) (4,5) (6,7) | 4 2 5 3 14 −4 8 −4 |
| h = 2 | (0,2) (1,3) (4,6) (5,7) | 9 5 −1 −1 22 −8 6 0 |
| h = 4 | (0,4) (1,5) (2,6) (3,7) | 31 −3 5 −1 −13 13 −7 −1 |

So $H_8 x = (31, -3, 5, -1, -13, 13, -7, -1)$. The first entry is the sum $31$. The entry $k = 4 = 100_2$ gives a minus sign to the entries $4$ to $7$: $3 + 1 + 4 + 1 - 5 - 9 - 2 - 6 = -13$. Running FWHT again gives $8x$, and INVERSE-FWHT divides by $8$ and returns $x$.

**XOR convolution.** For $a = (1, 2, 3, 4)$ and $b = (5, 6, 7, 8)$: $H_4 a = (10, -2, -4, 0)$ and $H_4 b = (26, -2, -4, 0)$, with products $(260, 4, 16, 0)$. The inverse transform gives $(70, 68, 62, 60)$, and directly $c_0 = \sum_i a_i b_i = 5 + 12 + 21 + 32 = 70$.

## Correctness

The invariant of the loop of line L3 is: when line L3 tests $h = 2^q$, each entry is $x'_{j} = \sum_{i} (-1)^{\langle i, j \rangle} x_{i}$, summed over the $i < n$ that agree with $j$ in all binary positions $q$ and above. For $q = 0$ the sum has the single term $i = j$. A pass of lines L4 to L7 pairs $j$ (with digit $0$ at position $q$) and $j + h$ (with digit $1$) and replaces them by the sum and the difference, which extends the sum to position $q$ with the sign $(-1)^{i_q j_q}$. At $h = n$ every $i$ is included, so $x' = H_n x$. The inverse follows from $H_n^2 = nI$. The full proof is below.

## Complexity

**Operations.** There are $\lg n$ passes, each with $n/2$ butterflies of one addition and one subtraction. So FWHT uses exactly $n \lg n$ additions (half of them subtractions) and no multiplications. INVERSE-FWHT adds $n$ divisions by $n$, which are shifts when $n$ is a power of two and the entries are known to be divisible. The time is $\Theta(n \log n)$ in each case, and the extra space is $O(1)$.

**Lower bound.** Morgenstern's determinant argument for linear algorithms with constants of modulus at most $1$ applies to every matrix: such an algorithm needs at least $\lg |\det M|$ additions. Since $H_n H_n^{\mathsf T} = nI$, $|\det H_n| = n^{n/2}$, so at least $\frac{n}{2} \lg n$ additions are needed in that model. FWHT is within a factor of $2$ of this bound.

**Rounding errors (proved).** In floating point, each output $y_k$ is computed by a tree of $\lg n$ additions or subtractions over all inputs, with signs $\pm 1$ that are exact. The standard bound for summation in a tree of depth $d$ gives $|\hat y_k - y_k| \le \gamma_{\lg n} \sum_j |x_j|$ with $\gamma_d = du/(1 - du)$, for unit roundoff $u$. Over the integers and over $\mathbb{Z}/p\mathbb{Z}$ the result is exact.

## Properties

- **Exact.** Over the integers there is no rounding, only growth by up to $\lg n$ binary digits.
- **In place, with no bit reversal.** The passes write back into the cells they read.
- **Multiplication-free.** Only additions and subtractions, which makes it cheap in hardware.
- **Involutive up to scale.** $H_n H_n = nI$, so the same code computes the inverse.
- **Order of passes is free.** The passes commute, so they can run for $h = n/2, \ldots, 1$ as well.

## Variants and improvements

- **XOR (dyadic) convolution.** For $c_k = \sum_{i \oplus j = k} a_i b_j$, the transform satisfies $H_n c = H_n a \cdot H_n b$ entrywise, the [convolution theorem](/convolution-theorem/) for the group $(\mathbb{Z}/2\mathbb{Z})^t$. So $c = \frac{1}{n} H_n(H_n a \cdot H_n b)$ in $3 n \lg n + O(n)$ operations instead of $n^2$.
- **OR and AND convolution.** Replacing the butterfly by $(u, v) \mapsto (u, u + v)$ gives the zeta transform over subsets, the [sum over subsets](/sum-over-subsets/), with inverse $(u, v) \mapsto (u, v - u)$, the [Möbius inversion](/mobius-inversion/) on the subset lattice. They turn OR convolution, $\sum_{i \lor j = k} a_i b_j$, into a pointwise product. The butterfly $(u, v) \mapsto (u + v, v)$ does the same for AND convolution.
- **Sequency (Walsh) order.** Sorting the rows by the number of sign changes gives the Walsh order, used in signal processing. It differs from the natural order by a bit reversal and a [Gray code](/gray-code/) permutation of the outputs; Fino and Algazi treat all the orderings as factorizations of one matrix.
- **Orthonormal scaling.** Multiply by $1/\sqrt 2$ in each butterfly to make each pass orthogonal; then the transform is its own inverse.
- **Higher radix and vectorization.** Doing two or three passes in one sweep over the array reduces memory traffic, as for the FFT.

## When to use it

Use it for XOR, OR or AND convolutions over subsets of a set of $t$ elements, as in counting problems on bitmasks; to compute all Fourier coefficients of a Boolean function on $t$ variables in $O(t 2^t)$ ([Fourier analysis of Boolean functions](/fourier-analysis-of-boolean-functions/)); to decode a [Hadamard code](/hadamard-code/) or a first-order [Reed-Muller code](/reed-muller-code/) by maximum likelihood, since all correlations with codewords are the entries of $H_n x$; and as a fast random-looking orthogonal transform in randomized numerical linear algebra and in spread-spectrum signal processing. For ordinary (cyclic) convolution use the [FFT](/convolution-via-fft/) instead.

## Pitfalls

- **A length that is not a power of two.** The transform is defined only for $n = 2^t$; pad with zeros if the application allows it, which changes the problem to subsets of a larger set.
- **The inverse in characteristic 2.** Modulo an even number, or over $\mathbb{F}_2$, $n$ is not a unit and the transform cannot be inverted.
- **Overflow.** The entries grow by up to a factor of $n$, and the product of two transforms in XOR convolution by up to $n^2 \max|a| \max|b|$. Use a modulus or wide integers.
- **Mixing up the scalings.** With the $1/\sqrt n$ convention on both sides, the convolution identity gets a factor $\sqrt n$. Check which convention a library uses.
- **The wrong butterfly for OR convolution.** The OR convolution needs the subset-sum butterfly $(u, u + v)$, not $(u + v, u - v)$.

## Implementations

## History

The functions $(-1)^{\langle j, k \rangle}$, in the sequency order, were studied by Walsh in 1923 as a complete orthonormal system on the unit interval. The matrices $H_n$ carry the names of Sylvester, who gave the doubling construction, and Hadamard, who studied matrices of $\pm 1$ entries with maximal determinant. The fast algorithm is the factorization $H_n = \prod_q (I \otimes H_2 \otimes I)$, the same pattern as the Cooley-Tukey factorization of the DFT matrix without twiddle factors. Fino and Algazi (1976) gave a unified matrix treatment of the fast algorithms for all the usual orderings.

## References
