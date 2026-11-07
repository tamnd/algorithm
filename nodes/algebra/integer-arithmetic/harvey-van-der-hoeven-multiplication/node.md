---
tag: H0NKE4
kind: algorithm
slug: harvey-van-der-hoeven-multiplication
name: Harvey-van der Hoeven multiplication
aliases:
- O(n log n) integer multiplication
- Harvey and van der Hoeven's algorithm
- Gaussian resampling multiplication
area: algebra/integer-arithmetic
level: research
summary: Integer multiplication in O(n log n) bit operations, matching the conjectured optimum.
solves: [integer-multiplication]
model: multitape-turing-machine
complexity:
  vars: {N: the length of each operand in binary digits}
  time: {worst: O(N log N), average: O(N log N), best: O(N log N)}
properties: {deterministic: true, recursive: true, in_place: false}
history:
  note: Harvey and van der Hoeven (2019; Annals of Mathematics 2021) proved the O(N log N) bound that Schönhage and Strassen had conjectured in 1971.
prereqs: [furer-multiplication, schonhage-strassen-multiplication, multidimensional-fft]
see_also: [integer-multiplication, furer-multiplication, schonhage-strassen-multiplication, chinese-remainder-theorem, rader-fft, bluestein-fft, kronecker-substitution, nonuniform-fft]
sources:
  - paper: doi:10.4007/annals.2021.193.2.4
    title: David Harvey and Joris van der Hoeven, Integer multiplication in time O(n log n), Annals of Mathematics 193(2), 2021
    locator: pp. 563 to 617 (Theorem 1.1; Section 1.2 for the overview, the Agarwal-Cooley reduction, the conditional variant with Rader's algorithm and the recurrence (1.3); Section 4 for Gaussian resampling; Section 5 for the main algorithm with d = 1729; Section 5.4 for K = 8 and d at least 9)
  - url: https://hal.science/hal-02070778
    title: David Harvey and Joris van der Hoeven, Integer multiplication in time O(n log n), preprint hal-02070778, 2019
    locator: the preprint version of March 2019, with the same sections
  - paper: doi:10.1109/TASSP.1977.1162981
    title: Ramesh C. Agarwal and James W. Cooley, New algorithms for digital convolution, IEEE Transactions on Acoustics, Speech, and Signal Processing 25(5), 1977
    locator: pp. 392 to 410 (the Chinese remainder map from a one-dimensional cyclic convolution of length s_1 s_2 ... s_d to a multidimensional one)
  - paper: doi:10.1109/PROC.1968.6477
    title: Charles M. Rader, Discrete Fourier transforms when the number of data samples is prime, Proceedings of the IEEE 56(6), 1968
    locator: pp. 1107 to 1108 (the DFT of prime length p as a cyclic convolution of length p - 1)
  - paper: doi:10.1137/070711761
    title: Martin Fürer, Faster integer multiplication, SIAM Journal on Computing 39(3), 2009
    locator: pp. 979 to 1005 (the bound N log N 2^(O(log* N)) that this algorithm improves)
---

Harvey-van der Hoeven multiplication multiplies two $N$-bit integers in $O(N \log N)$ bit operations on a multitape Turing machine. This is the bound that Schönhage and Strassen conjectured in 1971 to be the right order for [integer multiplication](/integer-multiplication/), and no faster algorithm is possible if that conjecture holds, though no lower bound better than linear is proved. David Harvey and Joris van der Hoeven announced it in 2019, and it appeared in the Annals of Mathematics in 2021. Earlier algorithms, from [Schönhage-Strassen](/schonhage-strassen-multiplication/) to [Fürer](/furer-multiplication/), lose a factor at each level of their recursion. This one turns the product into a $d$-dimensional Fourier transform with $d = 1729$, so that each recursive product has size about $N^{1/d}$, and the cost of the transforms shrinks from one level to the next. The algorithm only differs from simpler ones for $N \ge 2^{d^{12}}$, far beyond any computer, so it is of theoretical interest; this page gives an exact model of its first stage.

## In plain words

To multiply two long numbers fast, cut them into pieces, treat the pieces as the coefficients of polynomials, and multiply the polynomials with a Fourier transform. The products of the transformed pieces are themselves multiplications of smaller numbers, done the same way. All earlier methods of this kind lose a little at every level of that recursion, and the losses add up.

Harvey and van der Hoeven arrange the pieces in a cube of many dimensions instead of a line, 1729 dimensions in the paper. Each side of the cube is short, so the smaller multiplications are very much smaller, and the work per level drops geometrically instead of staying the same or growing. The hard part is a new trick, Gaussian resampling, that changes the awkward prime side lengths of the cube into powers of two without losing accuracy.

## The problem

The input is two integers $u, v \ge 0$ of at most $N$ binary digits each, and the output is $uv$. The digits are grouped into limbs of $b$ bits, $\beta = 2^b$; in the paper $b$ is about $\log_2 N$.

**Cost model.** The bound $O(N \log N)$ counts bit operations on a [multitape Turing machine](/multitape-turing-machine/), with integers in binary; it is proved in the paper (Theorem 1.1), and only sketched here. The code is a toy structural model of the first stage, with exact arithmetic modulo a prime $q$ in place of complex numbers to $O(\log N)$ bits. It counts prime-length DFTs, the cyclic convolutions that Rader's algorithm makes of them, and pointwise products. Its correctness and these counts are proved below. Gaussian resampling, the synthetic FFTs and the recursion are described, not modelled, and no timing is measured or claimed.

## The algorithm

The real algorithm has four steps. (1) Choose distinct primes $s_1, \dots, s_d$ of about $(N/\log N)^{1/d}$ each, and cut the inputs into about $N/\log N$ chunks, which reduces the problem to a product in $\mathbb{Z}[x]/(x^{s_1 \cdots s_d} - 1)$. (2) By the [Chinese remainder theorem](/chinese-remainder-theorem/), as Agarwal and Cooley observed, this ring is isomorphic to $\mathbb{Z}[x_1, \dots, x_d]/(x_1^{s_1} - 1, \dots, x_d^{s_d} - 1)$, so it suffices to compute [multidimensional DFTs](/multidimensional-fft/) of size $s_1 \times \cdots \times s_d$ over $\mathbb{C}$. (3) Gaussian resampling turns such a DFT into one of size $t_1 \times \cdots \times t_d$, where each $t_i$ is a power of two slightly larger than $s_i$ and $t_1 \cdots t_d = O(s_1 \cdots s_d)$. (4) A multivariate form of [Bluestein's algorithm](/bluestein-fft/) turns that DFT into a product in $\mathbb{C}[y]/(y^r + 1)[x_1, \dots, x_{d-1}]/(x_i^{t_i} - 1)$, which Nussbaumer's polynomial transforms evaluate using only additions and shifts by powers of the synthetic root $y$, leaving pointwise products in $\mathbb{C}[y]/(y^r + 1)$. These become integer products of size about $N^{1/d}$ by [Kronecker substitution](/kronecker-substitution/), done by recursion.

The toy below does steps (1) and (2) exactly, over $\mathbb{Z}_q$ with $q$ prime and $q \equiv 1 \pmod S$, $S = s_1 \cdots s_d$. In place of steps (3) and (4) it does each DFT of prime length $s$ with [Rader's algorithm](/rader-fft/), which turns it into a cyclic convolution of length $s - 1$. That is the first step of the paper's conditional variant (Section 1.2.1), which needs primes $s_i \equiv 1 \pmod r$ and a hypothesis on their size; the toy does these convolutions directly and counts them.

```pseudo id=main
HVDH-TOY-MULTIPLY(u, v)          ▷ distinct primes s_1..s_d, S = s_1⋯s_d, prime q ≡ 1 (mod S)
L1  cut u and v into (S + 1)/2 limbs f_j and g_j of b bits, so that f g has degree < S
L2  put f_j and g_j in the cell (j mod s_1, ..., j mod s_d) of s_1 × ⋯ × s_d arrays F and G
L3  F ← DFT_d(F, +1); G ← DFT_d(G, +1)
L4  H ← F · G, cell by cell                   ▷ in the real algorithm: after steps (3) and (4), recursive calls
L5  H ← DFT_d(H, −1)/S
L6  return Σ_j H[j mod s_1, ..., j mod s_d] · β^j

DFT_d(A, σ)                       ▷ ω_i a primitive s_i-th root of unity in Z_q
L7  for i ← 1 to d do
L8      for each line ℓ of A along dimension i do A_ℓ ← PRIME-DFT(A_ℓ, ω_i^σ)
L9  return A

PRIME-DFT(x, ω)                   ▷ length s prime, g a generator of (Z/s)^×   (Rader)
L10 X_0 ← x_0 + x_1 + ⋯ + x_(s−1)
L11 c ← cyclic convolution of (x_(g^k)) and (ω^(g^(−k))) for 0 ≤ k < s − 1
L12 for p ← 0 to s − 2 do X_(g^(−p)) ← x_0 + c_p; return X
```

For $s = 2$, PRIME-DFT is the butterfly $(x_0 + x_1, x_0 - x_1)$ and needs no convolution.

## Example

Take $d = 2$, $s = (3, 5)$, so $S = 15$, with limbs of $b = 4$ bits. Then the toy holds operands of $(15 + 1)/2 = 8$ limbs, and the smallest suitable prime is $q = 1831 = 122 \cdot 15 + 1$, which exceeds the largest possible product coefficient $8 \cdot 15^2 = 1800$. For $u = \mathtt{BEEF}$ and $v = \mathtt{CAFE}$, lines L1 and L2 place the limbs, lowest first, as follows, and after line L5 the cells hold the coefficients $h_j$ of the product of the limb polynomials.

| $j$ | cell $(j \bmod 3, j \bmod 5)$ | $f_j$ | $g_j$ | $h_j$ |
|---|---|---|---|---|
| 0 | (0, 0) | 15 | 14 | 210 |
| 1 | (1, 1) | 14 | 15 | 421 |
| 2 | (2, 2) | 14 | 10 | 556 |
| 3 | (0, 3) | 11 | 12 | 684 |
| 4 | (1, 4) | 0 | 0 | 473 |
| 5 | (2, 0) | 0 | 0 | 278 |
| 6 | (0, 1) | 0 | 0 | 132 |
| 7 to 14 | the other cells | 0 | 0 | 0 |

Line L6 reads the cells back in the order of $j$ and carries in base 16, giving $\mathtt{97660722} = 2540046114 = uv$. Each DFT$_2$ does $15/3 + 15/5 = 8$ prime DFTs, so the three transforms make 24 prime DFTs and 24 Rader convolutions, of lengths 2 and 4, and line L4 makes 15 products.

## Correctness

The proof file gives the full argument for the toy. Line L2 is a bijection between the indices $0 \le j < S$ and the cells, by the Chinese remainder theorem, and it is a ring isomorphism $\mathbb{Z}_q[x]/(x^S - 1) \to \mathbb{Z}_q[x_1, \dots, x_d]/(x_i^{s_i} - 1)$, because $x^j \mapsto \prod_i x_i^{j \bmod s_i}$ respects products. Rader's algorithm in lines L10 to L12 computes the DFT of prime length, since $n \mapsto g^n$ is a bijection from $\{0, \dots, s-2\}$ to the nonzero residues modulo $s$, and DFT$_d$ computes the $d$-dimensional DFT because the $d$-dimensional kernel $\prod_i \omega_i^{j_i k_i}$ is a product of one-dimensional kernels. The convolution theorem then gives the cyclic product, the degree bound of line L1 rules out a wrap, and the bound $\frac{S+1}{2}(\beta - 1)^2 < q$ rules out a reduction modulo $q$.

## Complexity

**The toy, proved.** One DFT$_d$ does $\sum_i S/s_i$ prime DFTs, one per line, and each prime DFT of length $s > 2$ does one cyclic convolution of length $s - 1$, which the toy does directly in $(s - 1)^2$ products. So a multiplication costs $3\sum_i (S/s_i)(s_i - 1)^2 + S$ products in $\mathbb{Z}_q$ plus lower-order additions, which is $O(d S^{1 + 1/d})$ when all $s_i$ are about $S^{1/d}$. That is not $O(S \log S)$: the toy shows the reduction to short convolutions, not the fast way to do them.

**The real algorithm, a sketch of the paper's analysis.** Steps (3) and (4) and the synthetic FFTs cost $O(N \log N)$ bit operations at the top level, and the pointwise products are integer products of size $N' = N^{1/d + o(1)}$. With $M(N)$ the cost of a product, the paper proves (Section 5, Corollary 5.5) a recurrence of the form

$$M(N) < \frac{K N}{N'} M(N') + O(N \log N), \qquad N' = N^{1/d + o(1)},$$

with the absolute constant $K = 1728$, which does not depend on $d$. Writing $M(N) = T(N) \cdot N \log N$, and since $\log N' \approx (\log N)/d$, this becomes $T(N) \lesssim \frac{K}{d} T(N') + C$. With $d = 1729 > K$, the factor $K/d$ is less than 1, so $T$ stays bounded and $M(N) = O(N \log N)$. In words: the total cost of the FFTs falls by the factor $d/K$ at each deeper level, while in Schönhage-Strassen it stays the same at each level, and in Fürer's algorithm it grows.

## Properties

- **Deterministic and unconditional.** The bound uses no randomness and no unproved hypothesis. The variant with Rader's algorithm of Section 1.2.1 needs a hypothesis on the least prime in an arithmetic progression.
- **Recursive.** The size drops from $N$ to about $N^{1/d}$ per level, so the depth is $O(\log \log N)$; the base case is any method, for $N < 2^{d^{12}}$.
- **Numerical.** The transforms are over $\mathbb{C}$ to $O(\log N)$ bits of precision, with a full error analysis; the toy is exact.
- **Optimal if the conjecture holds.** $\Omega(N \log N)$ is not proved in general. Afshani, Freksen, Kamma and Larsen (2019) showed it for Boolean circuits, conditional on a conjecture about network coding.

## Variants and improvements

- **Smaller dimension.** With the optimisations of Section 5.4, the constant $K$ drops to about 8, and $d \ge 9$ suffices.
- **Rader instead of resampling.** The conditional variant replaces Gaussian resampling by Rader's algorithm on primes $s_i \equiv 1 \pmod r$, which is what the toy models at its first step.
- **Polynomials over finite fields.** A companion paper of the same authors gives $O(n \log n)$ for multiplying polynomials of degree $n$ over a fixed finite field, conditional on a hypothesis about primes in arithmetic progressions.
- **Consequences.** Every problem with cost $O(M(N))$ or $O(M(N) \log N)$, such as division, square roots and radix conversion, inherits the bound with $M(N) = O(N \log N)$.

## When to use it

Not in practice. The algorithm only does something new for $N \ge 2^{d^{12}}$, and even with $d = 9$ the constants are far from those of Schönhage-Strassen and of [number-theoretic transforms](/number-theoretic-transform/) with small primes, which libraries such as GMP use for large operands. Its value is the theorem: integer multiplication has the same complexity, $O(N \log N)$, as the FFT of length $N$ on numbers of fixed size.

## Pitfalls

- **Sizes that are not coprime.** Line L2 is a bijection only if the $s_i$ are pairwise coprime; with $s = (3, 3)$, the indices $0$ and $3$ fall in the same cell $(0, 0)$, while the cell $(0, 1)$ is never used, and the product comes out wrong. The right line L2 uses distinct primes, as the code checks.
- **Zero-padding to powers of two.** Replacing each prime $s_i$ by the next power of two by padding, or Bluestein's algorithm with length at least $2s_i - 1$, multiplies the total size by up to $2^d$, which for $d = 1729$ destroys the gain. That is why step (3) uses Gaussian resampling, with $t_1 \cdots t_d = O(s_1 \cdots s_d)$.
- **Too few limbs of room.** If line L1 used $S$ limbs instead of $(S + 1)/2$, the product would have degree up to $2S - 2$, and the cyclic convolution of length $S$ would fold the top half onto the bottom. Line L1 must keep $\deg f + \deg g < S$.
- **A modulus that is too small.** Line L5 recovers each $h_j$ only modulo $q$. With $q \le \frac{S+1}{2}(\beta - 1)^2$, a large coefficient wraps and line L6 returns a wrong product; the code picks $q$ above that bound.

## Implementations

## History

Schönhage and Strassen (1971) gave $O(N \log N \log \log N)$ and conjectured that $O(N \log N)$ is the right order. Fürer (2007) reached $N \log N \cdot 2^{O(\log^* N)}$. Harvey, van der Hoeven and Lecerf (2016) made the constant explicit as $8^{\log^* N}$, and a sequence of papers lowered it to $4^{\log^* N}$, the last unconditional step being by Harvey and van der Hoeven (2018). In March 2019 Harvey and van der Hoeven posted the $O(N \log N)$ algorithm, built on Gaussian resampling, Agarwal and Cooley's reduction (1977) and Nussbaumer's polynomial transforms (late 1970s); it was published in the Annals of Mathematics in 2021.

## References
