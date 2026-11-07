---
tag: YF5DJV
kind: algorithm
slug: coppersmith-winograd-algorithm
name: Coppersmith-Winograd algorithm
aliases:
- Coppersmith-Winograd
- Coppersmith and Winograd's algorithm
- CW algorithm
area: algebra/matrix-multiplication
level: research
summary: The 1990 bound ω < 2.375477 (about 2.376 originally) from a tensor of border rank q+2 and the laser method; its algorithms are galactic and never used in practice.
model: algebraic-computation-tree
complexity:
  vars: {n: the order of the matrices}
  time: {worst: O(n^2.375477), average: O(n^2.375477), best: O(n^2.375477)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: true, in_place: false}
history:
  year: 1990
  people: [Don Coppersmith, Shmuel Winograd]
  note: Announced at STOC 1987 and published in the Journal of Symbolic Computation in 1990. The bound stood until 2010.
prereqs: [laser-method, schonhage-asymptotic-sum-inequality]
see_also: [matrix-multiplication-exponent, border-rank, matrix-multiplication-tensor, tensor-rank, strassen-algorithm, bilinear-complexity, alphatensor]
sources:
  - paper: doi:10.1016/S0747-7171(08)80013-2
    title: Don Coppersmith and Shmuel Winograd, Matrix multiplication via arithmetic progressions, Journal of Symbolic Computation 9(3) (1990)
    locator: pp. 251 to 280 (the tensor, its border rank q+2, the easy and complete constructions, the square of the tensor and ω < 2.375477)
  - paper: doi:10.1145/28395.28396
    title: Don Coppersmith and Shmuel Winograd, Matrix multiplication via arithmetic progressions, 19th ACM Symposium on Theory of Computing (STOC 1987)
    locator: pp. 1 to 6 (the conference version and ω < 2.376)
  - paper: doi:10.1137/0211038
    title: Don Coppersmith and Shmuel Winograd, On the asymptotic complexity of matrix multiplication, SIAM Journal on Computing 11(3) (1982)
    locator: pp. 472 to 492 (the earlier bound ω < 2.496)
  - paper: "Volker Strassen, Relative bilinear complexity and matrix multiplication, Journal für die reine und angewandte Mathematik 375/376 (1987)"
    locator: pp. 406 to 443 (the laser method and ω < 2.479)
  - paper: "Raphaël Salem and Donald C. Spencer, On sets of integers which contain no three terms in arithmetical progression, Proceedings of the National Academy of Sciences of the USA 28(12) (1942)"
    locator: pp. 561 to 563 (large subsets of 1..M with no three-term progression)
  - paper: doi:10.4086/toc.gs.2013.005
    title: Markus Bläser, Fast Matrix Multiplication, Theory of Computing Graduate Surveys 5 (2013)
    locator: the sections on the Coppersmith and Winograd tensor (proofs of the easy and complete bounds)
  - book: isbn:9783540605829
    title: Peter Bürgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory, Springer (1997)
    locator: Chapter 15 (the laser method and the Coppersmith and Winograd bounds)
  - paper: doi:10.1145/2213977.2214056
    title: Virginia Vassilevska Williams, Multiplying matrices faster than Coppersmith-Winograd, STOC 2012
    locator: pp. 887 to 898 (the eighth power of the CW tensor and ω < 2.3729)
  - paper: "Andris Ambainis, Yuval Filmus and François Le Gall, Fast matrix multiplication: limitations of the Coppersmith-Winograd method, 47th ACM Symposium on Theory of Computing (STOC 2015)"
    locator: the main theorem (this form of the laser method on powers of the CW tensor cannot give ω < 2.3078)
---

The Coppersmith-Winograd algorithm is the construction behind the bound $\omega < 2.375477$ on the [exponent of matrix multiplication](/matrix-multiplication-exponent/), published in 1990 and the best bound for twenty years. Its core is a small tensor $T_q$ with $3q + 3$ terms whose [border rank](/border-rank/) is only $q + 2$: an approximate algorithm computes it with $q + 2$ multiplications. Its pieces are tiny matrix products that share variables. The [laser method](/laser-method/), with a hash into a set with no three-term arithmetic progression, cuts a high tensor power of $T_q$ down to many independent matrix products. [Schönhage's asymptotic sum inequality](/schonhage-asymptotic-sum-inequality/) then turns these into the bound on ω. The matrix multiplication algorithms that come out of this are galactic: the bound is proved, but the hidden constants are so large that no one runs them.

## In plain words

The page has two layers. The small layer is a concrete trick. It takes two short vectors and computes a handful of sums of products, $3q + 3$ products in all, with only $q + 2$ multiplications. It cheats a little: it works with a tiny number ε and reads the answer off the ε³ part of the result.

The big layer is a proof. The handful of sums contains small matrix products, but they overlap. Repeat the trick on itself many times. Then zero out inputs, chosen by a hash, until the pieces that survive no longer overlap. Each surviving piece is a separate matrix product, and all of them are computed cheaply together. Counting them shows that $n \times n$ matrices can be multiplied with $O(n^{2.375477})$ operations. The counting is proved, but the matrices would have to be astronomically large for this to pay off.

## The problem

The final goal is the product $C = AB$ of $n \times n$ matrices over a field $F$, with the cost $MM(n)$ counted in field operations in the [algebraic model](/algebraic-computation-tree/), and in particular the exponent ω with $MM(n) = O(n^{\omega + \epsilon})$ for every $\epsilon > 0$. The construction works over any field. The bilinear algorithms it produces use no commutativity of the matrix entries, so they also apply to blocks.

The small problem computed on this page is the bilinear map of the Coppersmith-Winograd tensor. For an integer $q \ge 0$, the tensor in $F^{q+2} \otimes F^{q+2} \otimes F^{q+2}$ is the trilinear form
$$T_q = \sum_{i=1}^{q} \big(x_0 y_i z_i + x_i y_0 z_i + x_i y_i z_0\big) + x_0 y_0 z_{q+1} + x_0 y_{q+1} z_0 + x_{q+1} y_0 z_0.$$
Read the coefficient of $z_k$ as an output. Then $T_q$ is the bilinear map $\varphi(x, y) = (\varphi_0, \ldots, \varphi_{q+1})$ with
$$\varphi_0 = \sum_{i=1}^{q} x_i y_i + x_0 y_{q+1} + x_{q+1} y_0, \qquad \varphi_i = x_0 y_i + x_i y_0 \ (1 \le i \le q), \qquad \varphi_{q+1} = x_0 y_0.$$
Computed directly, φ takes $3q + 3$ multiplications. The [tensor rank](/tensor-rank/) of $T_q$ is larger than $q + 2$, but its border rank is exactly $q + 2$, the least possible for a tensor whose $x$ part has $q + 2$ variables. The approximate algorithm below shows the upper bound. It needs a ring $R$ that allows subtraction, with an indeterminate ε that commutes with everything; the $x$ factor stays on the left in each product.

## The algorithm

The approximate algorithm works in $R[\varepsilon]$:

```pseudo id=main
CW-APPROX(x, y, q)                ▷ x, y ∈ R^(q+2), indices 0..q+1
L1  for i ← 1 to q do P_i ← (x_0 + ε x_i)(y_0 + ε y_i)
L2  X ← x_1 + … + x_q;  Y ← y_1 + … + y_q
L3  P_(q+1) ← (x_0 + ε² X)(y_0 + ε² Y)
L4  P_(q+2) ← (x_0 + ε³ x_(q+1))(y_0 + ε³ y_(q+1))
L5  c_0 ← ε (P_1 + … + P_q) − P_(q+1) + (1 − qε) P_(q+2)
L6  for i ← 1 to q do c_i ← ε² (P_i − P_(q+1))
L7  c_(q+1) ← ε³ P_(q+2)
L8  return the coefficient of ε³ in each of c_0, …, c_(q+1)
```

Lines L1, L3 and L4 are the only multiplications of a linear form in $x$ by a linear form in $y$: there are $q + 2$ of them. Lines L5 to L7 multiply products by fixed polynomials in ε, which are not counted as multiplications in the bilinear model. Line L8 discards the higher powers of ε; this is the step that makes the algorithm approximate. In trilinear form, the identity behind it is
$$\varepsilon^3 T_q = \sum_{i=1}^{q} \varepsilon (x_0 + \varepsilon x_i)(y_0 + \varepsilon y_i)(z_0 + \varepsilon z_i) - (x_0 + \varepsilon^2 X)(y_0 + \varepsilon^2 Y)(z_0 + \varepsilon^2 Z) + (1 - q\varepsilon)(x_0 + \varepsilon^3 x_{q+1})(y_0 + \varepsilon^3 y_{q+1})(z_0 + \varepsilon^3 z_{q+1}) + O(\varepsilon^4),$$
with $Z = z_1 + \cdots + z_q$. So $\underline{R}(T_q) \le q + 2$ with error degree $3$.

The matrix multiplication algorithm is then built in four steps. This is a proof, not a program, and none of the steps below is implemented here.

1. **Blocks.** Split the variables into blocks $X^{[0]} = \{x_0\}$, $X^{[1]} = \{x_1, \ldots, x_q\}$ and $X^{[2]} = \{x_{q+1}\}$, and the same for $y$ and $z$. The terms of $T_q$ fall into six blocks $T^{IJK}$ with $I + J + K = 2$. Three of them, $T^{011} = \sum_i x_0 y_i z_i$, $T^{101}$ and $T^{110}$, are matrix products of shapes $\langle 1, 1, q \rangle$, $\langle q, 1, 1 \rangle$ and $\langle 1, q, 1 \rangle$. The other three, such as $x_0 y_0 z_{q+1}$, are $\langle 1, 1, 1 \rangle$. They share variables, so $T_q$ is not a direct sum of them.
2. **Power and zero out by type.** Take the Kronecker power $T_q^{\otimes N}$, which has border rank at most $(q + 2)^N$. Its blocks are indexed by sequences in $\{0, 1, 2\}^N$. Keep only the $X$, $Y$ and $Z$ blocks whose sequences have a chosen number of 0s, 1s and 2s, and set the rest to zero.
3. **Hash.** Choose a prime $M$ and a set $B \subset \mathbb{Z}/M\mathbb{Z}$ with no three-term arithmetic progression and $|B| = M^{1 - o(1)}$ (Salem and Spencer 1942, Behrend 1946). Map each block sequence to $\mathbb{Z}/M\mathbb{Z}$ by a random linear hash. The hashes of the three blocks of any surviving term form an arithmetic progression, so if all three lie in $B$, the three hashes are equal. Zero out every block whose hash is not in $B$. Then, inside each hash class, remove the remaining overlaps greedily. For a good choice of the hash, the number of independent matrix products left is at least the number of $X$ blocks times $|B| / (12 M)$, where $M$ is about six times the number of terms that share one $X$ block. Since $|B| = M^{1 - o(1)}$ and $M = 2^{O(N)}$, the loss is a factor $2^{o(N)}$. The details are on the [laser method page](/laser-method/).
4. **Count.** What is left is a direct sum of $2^{N H - o(N)}$ matrix products, each with volume $q^{3 \alpha N}$, all computed by an approximate bilinear algorithm with $(q + 2)^N$ products. Here α and $H$ come from the chosen type in step 2. The asymptotic sum inequality gives $2^{N H - o(N)} q^{\alpha N \omega} \le (q + 2)^N$. Take $N$-th roots and let $N \to \infty$.

The square $T_q \otimes T_q$ treated the same way, with blocks regrouped by the sum of their two indices, gives the bound $2.375477$. Some of its blocks are not matrix products, and their worth is bounded by a laser analysis of their own.

## Example

Take $q = 2$, $x = (1, 2, 3, 4)$ and $y = (5, 6, 7, 8)$. The direct values are $\varphi_0 = 2 \cdot 6 + 3 \cdot 7 + 1 \cdot 8 + 4 \cdot 5 = 61$, $\varphi_1 = 6 + 10 = 16$, $\varphi_2 = 7 + 15 = 22$ and $\varphi_3 = 5$, with $9$ multiplications.

The algorithm makes $4$ products. Here $X = 5$ and $Y = 13$:

| product | factors | value in $\mathbb{Z}[\varepsilon]$ |
|---|---|---|
| $P_1$ | $(1 + 2\varepsilon)(5 + 6\varepsilon)$ | $5 + 16\varepsilon + 12\varepsilon^2$ |
| $P_2$ | $(1 + 3\varepsilon)(5 + 7\varepsilon)$ | $5 + 22\varepsilon + 21\varepsilon^2$ |
| $P_3$ | $(1 + 5\varepsilon^2)(5 + 13\varepsilon^2)$ | $5 + 38\varepsilon^2 + 65\varepsilon^4$ |
| $P_4$ | $(1 + 4\varepsilon^3)(5 + 8\varepsilon^3)$ | $5 + 28\varepsilon^3 + 32\varepsilon^6$ |

Then
$$\begin{aligned}
c_0 &= \varepsilon(P_1 + P_2) - P_3 + (1 - 2\varepsilon) P_4 = 61\varepsilon^3 - 121\varepsilon^4 + 32\varepsilon^6 - 64\varepsilon^7, \\
c_1 &= \varepsilon^2 (P_1 - P_3) = 16\varepsilon^3 - 26\varepsilon^4 - 65\varepsilon^6, \\
c_2 &= \varepsilon^2 (P_2 - P_3) = 22\varepsilon^3 - 17\varepsilon^4 - 65\varepsilon^6, \\
c_3 &= \varepsilon^3 P_4 = 5\varepsilon^3 + 28\varepsilon^6 + 32\varepsilon^9.
\end{aligned}$$
The coefficients of $\varepsilon^3$ are $61, 16, 22, 5$, as required. In $c_0$ the constant terms $-5 + 5$, the $\varepsilon$ terms $10 - 10$ and the $\varepsilon^2$ terms $38 - 38$ cancel. In floating point at $\varepsilon = 0.01$, dividing by $\varepsilon^3$ instead of extracting a coefficient gives $59.79, 15.74, 21.83, 5.00003$, off by $O(\varepsilon)$; at $\varepsilon = 0.001$ the first value is $60.879$. A script checks all of these numbers.

The bounds on ω, computed by the same script:

- **Easy construction.** Drop the three $\langle 1,1,1 \rangle$ terms; the border rank stays at most $q + 2$. With the three remaining types equally likely, the $X$ block index is $0$ with probability $1/3$ and $1$ with probability $2/3$. Step 4 gives $\omega \le \log_q \big(4 (q+2)^3 / 27\big)$. This is $2.5$ at $q = 4$, $2.4159$ at $q = 6$ and smallest at $q = 8$, where it is $2.4036$.
- **Complete construction.** Give each of the three product types weight α and each of the three unit types weight $1/3 - \alpha$. The $X$ index is then $0$, $1$ or $2$ with probabilities $2/3 - \alpha$, $2\alpha$ and $1/3 - \alpha$, and
$$\omega \le \frac{\log_2 (q + 2) - H(2/3 - \alpha,\, 2\alpha,\, 1/3 - \alpha)}{\alpha \log_2 q}.$$
Minimized over α this is $2.69856$ at $q = 2$, $2.4141$ at $q = 4$, $2.38719$ at $q = 6$ with $\alpha \approx 0.31733$, $2.38743$ at $q = 7$ and $2.39081$ at $q = 8$. Coppersmith and Winograd state it as $\omega < 2.388$.
- **Square of the tensor.** Their analysis of $T_q^{\otimes 2}$ gives $\omega < 2.375477$. This number is quoted from the paper and not recomputed here.

## Correctness

Each $P_i$ is a polynomial in ε. Expand $P_i = x_0 y_0 + \varepsilon (x_0 y_i + x_i y_0) + \varepsilon^2 x_i y_i$ for $i \le q$, $P_{q+1} = x_0 y_0 + \varepsilon^2 (x_0 Y + X y_0) + \varepsilon^4 X Y$ and $P_{q+2} = x_0 y_0 + \varepsilon^3 (x_0 y_{q+1} + x_{q+1} y_0) + \varepsilon^6 x_{q+1} y_{q+1}$.

- **Output 0.** In $c_0$ the constant term is $-x_0 y_0 + x_0 y_0 = 0$. The ε term is $q x_0 y_0 - q x_0 y_0 = 0$. The ε² term is $\sum_i (x_0 y_i + x_i y_0) - (x_0 Y + X y_0) = 0$. The ε³ term is $\sum_i x_i y_i + (x_0 y_{q+1} + x_{q+1} y_0) = \varphi_0$, since $-q\varepsilon P_{q+2}$ has no ε² term to lift.
- **Outputs 1 to q.** $P_i - P_{q+1}$ has no constant term, and its ε term is $x_0 y_i + x_i y_0$, so the ε³ coefficient of $c_i$ is $\varphi_i$.
- **Output q+1.** The constant term of $P_{q+2}$ is $x_0 y_0 = \varphi_{q+1}$.

Every step uses only distributivity and the fact that ε commutes, so the identity holds over any ring with subtraction, and for matrices as entries. The algorithm makes a fixed number of steps, so it terminates. The full proof is in the proofs section.

For the matrix multiplication bound, correctness is the chain of proved theorems in steps 1 to 4. The power $T_q^{\otimes N}$ has border rank at most $(q+2)^N$ because border rank is submultiplicative. Zeroing out variables never raises border rank. The arithmetic progression argument makes the surviving products independent. The asymptotic sum inequality, which also absorbs the conversion from border rank to rank, turns the count into a bound on ω.

## Complexity

- **The small algorithm.** $q + 2$ multiplications of polynomials in ε of degree at most $3$, against $3q + 3$ for the direct formula; $\Theta(q)$ additions. Exactly, this is the bound $\underline{R}(T_q) \le q + 2$. Lower bounds on the $x$ flattening show it is optimal.
- **Making it exact.** Over a field with more than $7$ elements, $c_k(\varepsilon) / \varepsilon^3$ with the higher terms of the $z$ factors dropped is a polynomial of degree at most $6$. So $7$ evaluations at nonzero ε and Lagrange interpolation at $0$ give φ exactly with $7(q+2)$ multiplications, and division only by constants. Without division, multiplying out the polynomials in ε gives at most $10(q+2)$, that is $\binom{h+2}{2}$ times the border rank with $h = 3$.
- **The exponent.** The constructions give the proved bounds $\omega \le 2.4036$ (easy), $\omega < 2.388$ (complete) and $\omega < 2.375477$ (square). So for every $\tau > 2.375477$, and also for some $\tau < 2.375477$ since the inequality is strict, there is a fixed bilinear algorithm for $\langle K, K, K \rangle$ with at most $K^{\tau}$ products. Used recursively on blocks, it gives $MM(n) = O(n^{2.375477})$.
- **Space.** Any fixed bilinear algorithm run recursively, one product at a time, uses $O(n^2)$ extra space, with a constant that depends on $K$.
- **The constants.** $K$ is a power of $q + 2$ with an exponent $N$ large enough for the $o(N)$ terms of step 4 to be small, and the border rank to rank step adds a factor polynomial in $N$. The resulting $K$ is astronomically large. There is no known size of matrix that could be stored at which it beats Strassen's algorithm. The method is galactic.

All the exponent bounds above are proved. No running time for the matrix algorithm has been observed, because it has never been run on matrices.

## Properties

- **Approximate, then exact.** The small algorithm is exact only in the coefficient of ε³; the exact algorithms come from interpolation or from expanding in ε.
- **Deterministic.** The hash in step 3 is chosen at random in the proof, but only its existence is used. The final algorithm is a fixed bilinear algorithm with no randomness.
- **Bilinear and noncommutative.** Every product is a linear form in $A$ times a linear form in $B$, so the algorithm recurses on blocks over any ring with subtraction. The exact version by interpolation divides by small integers; the version that expands in ε does not divide.
- **Tight support.** The block indices of every term of $T_q$ add up to $2$. This is what makes the arithmetic progression hash work.
- **Choice of q.** The easy bound tends to $3$ as $q \to \infty$ and is about $3.245$ at $q = 2$; only middle values of $q$, from about $5$ to $8$, give good bounds.

## Variants and improvements

- **Higher powers.** Stothers (2010) analyzed $T_q^{\otimes 4}$ and got $\omega < 2.3737$. Vassilevska Williams (2012) automated the analysis of the eighth power and got $2.372873$. Le Gall (2014) used convex optimization on the thirty-second power for $2.3728639$. All use the same tensor.
- **Refined laser method.** Alman and Vassilevska Williams (2021) kept some of the blocks that the earlier analyses threw away, and got $2.3728596$.
- **Asymmetric hashing.** Duan, Wu and Zhou (2023) hashed the three sides differently, which gave $2.371866$. Later papers improved this to $2.371552$ (2024) and $2.371339$ (2025). The 2025 value is taken from the [exponent page](/matrix-multiplication-exponent/) and not checked here.
- **Barriers.** Ambainis, Filmus and Le Gall (2015) proved that the laser method in this form, applied to any power of $T_q$, cannot give $\omega < 2.3078$. So getting near $\omega = 2$ needs a new tensor or a new method.
- **Rectangular products.** The same tensor and method bound the exponents of rectangular matrix products and the dual exponent α (Coppersmith 1997, Le Gall and Urrutia 2018).
- **Practical fast algorithms.** For real matrices the competitors are [Strassen's algorithm](/strassen-algorithm/) and schemes found by computer search such as [AlphaTensor](/alphatensor/), which are exact, small and recursive.

## When to use it

Not for computing. The algorithm is used as a theorem: it is why papers can write $O(n^{2.376})$, or now $O(n^{2.372})$, for problems that reduce to matrix multiplication, such as inversion, determinants and triangle detection. For any matrix that fits in a computer, a [blocked classical product](/blocked-matrix-multiplication/) or Strassen's algorithm is faster by a huge margin. The small approximate algorithm is a good example of border rank and of how cheap approximate computations can be.

## Pitfalls

- **Reading O(n^2.376) as a speedup.** The bound hides a constant that has never been made explicit for any useful size. Do not cite it as an improvement for a real implementation.
- **Dropping the ε correction.** Without the factor $1 - q\varepsilon$ in front of $P_{q+2}$, the ε³ coefficient of $c_0$ is still right, but $c_0$ keeps the stray term $q \varepsilon x_0 y_0$. Then the sum is no longer $\varepsilon^3 T_q + O(\varepsilon^4)$, so the border rank statement fails, dividing by ε³ blows up as ε tends to $0$, and the interpolation step gives a wrong answer.
- **Dividing by ε³ in floating point.** This gives φ only up to $O(\varepsilon)$, and small ε loses precision through cancellation. Use exact arithmetic or interpolation.
- **Interpolation in small characteristic.** The $7$-point interpolation needs $7$ distinct nonzero field elements and division by their differences. Over $\mathbb{F}_2$ or $\mathbb{F}_7$ it fails. Expanding in ε works over any ring.
- **Confusing the tensor with matrix multiplication.** $T_q$ is not a matrix product; its pieces are. The bound needs the laser method, not just the border rank of $T_q$.

## Implementations

## History

Strassen's 1969 algorithm gave $\omega \le \log_2 7 \approx 2.807$. Bini, Capovani, Romani and Lotti introduced approximate algorithms in 1979, and Schönhage's asymptotic sum inequality of 1981 gave $2.522$. Coppersmith and Winograd reached $2.496$ in 1982 with sums of products. Strassen's laser method (announced in 1986, published in 1987) gave $2.479$. Coppersmith and Winograd added the hash into sets without three-term arithmetic progressions, which explains the title of their paper, and their new tensor $T_q$. They presented $\omega < 2.376$ at STOC 1987 and published the full paper, with $2.375477$ from the square of the tensor, in 1990. No better bound was found until Stothers (2010) and Vassilevska Williams (2012) analyzed higher powers of the same tensor.

## References
