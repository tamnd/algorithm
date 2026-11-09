---
tag: Q4GN21
kind: problem
slug: binomial-coefficient-computation
name: Computing binomial coefficients
aliases:
- binomial coefficient evaluation
- computing n choose k
- nCr computation
area: combinatorics/counting-algorithms
level: intro
summary: Evaluating C(n,k) exactly or modulo a number.
model: word-ram
complexity:
  vars: {n: the upper index, k: the lower index, L: the number of bits of the answer, w: the word size in bits}
  time: {worst: Ω(L/w)}
prereqs: [binomial-coefficient, factorial]
see_also: [pascal-triangle-dp, binomial-coefficient-bounds, lucas-theorem, factorial-modulo-prime, modular-inverse, legendre-formula, chinese-remainder-theorem, integer-overflow]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.6, Binomial Coefficients (the factorial and product formulas, Pascal's rule, and the exercises on binomial coefficients modulo a prime)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 4.4, Factorial factors (the exponent of a prime in n!), and Section 5.1, Basic identities
  - paper: doi:10.2307/2369308
    title: Édouard Lucas, Théorie des fonctions numériques simplement périodiques, American Journal of Mathematics 1(2), 184 to 240 (1878)
    locator: the section on binomial coefficients modulo a prime (the theorem now called Lucas's theorem)
  - paper: doi:10.1016/0196-6774(85)90006-9
    title: Peter B. Borwein, On the complexity of calculating factorials, Journal of Algorithms 6(3), 376 to 380 (1985)
    locator: the main result (n! from its prime factorization in O(M(n log n) log log n) bit operations)
  - paper: doi:10.1145/820127.820168
    title: Yannis Manolopoulos, Binomial coefficient computation, recursion or iteration?, ACM SIGCSE Bulletin 34(4), 65 to 67 (2002)
    locator: the comparison of the recursive, the table and the multiplicative methods
---

Computing binomial coefficients is the problem of finding the number $\binom{n}{k}$ for given integers $n$ and $k$, either as an exact integer or as a residue modulo a number $m$. The exact value has $L = \lg \binom{n}{k}$ bits, which is about $n$ bits for $k = n/2$, so the cost depends on the arithmetic model as much as on the method. The usual methods are the product formula with $k$ exact divisions, the table of [Pascal's triangle](/pascal-triangle-dp/), tables of factorials and [modular inverses](/modular-inverse/) for a prime modulus, and [Lucas's theorem](/lucas-theorem/) for a small prime.

## In plain words

You want the number of ways to choose some items from a set, as a number a program can use. The number grows very fast. For one hundred items and a choice of fifty, it is too large for a normal machine number, so a program must either keep it as a long number or keep only its remainder after division by a fixed number.

The textbook formula divides one huge product by two other huge products. That is slow and overflows early. Better methods build the answer step by step, so that each step stays small, or they work with remainders from the start. The right method depends on how large the inputs are, how many answers you need, and whether you need the full number or only a remainder.

## Definition

Notation: $[n] = \{1, \ldots, n\}$, $\binom{n}{k}$ or $C(n, k)$ is the number of $k$-element subsets of $[n]$, $L = \lceil \lg(\binom{n}{k} + 1) \rceil$ is its number of bits, $p$ is a prime, $m \ge 2$ is a modulus, and $w$ is the word size of the [word RAM](/word-ram/), with $w \ge \lg n$.

**Input.** Integers $n \ge 0$ and $k$, and in the modular version a modulus $m \ge 2$.

**Output.** The integer $\binom{n}{k}$, which is $0$ when $k < 0$ or $k > n$; or, in the modular version, the residue $\binom{n}{k} \bmod m$ in $\{0, \ldots, m - 1\}$.

**Cost model.** In the exact version, the numbers are big integers stored in $\lceil L/w \rceil$ words, and an operation on them costs time proportional to the number of words it reads and writes; the multiplication of two $L$-bit numbers costs $M(L)$ bit operations, with $M(L) = O(L^2)$ for [schoolbook multiplication](/schoolbook-multiplication/) and $O(L \log L)$ with [FFT](/fast-fourier-transform/) methods. In the modular version with $m < 2^{w/2}$, every addition and multiplication of residues costs $O(1)$.

By symmetry, $\binom{n}{k} = \binom{n}{n-k}$, so all methods first replace $k$ by $\min(k, n - k)$.

## Variants

- **One exact value.** Return the big integer $\binom{n}{k}$.
- **One value modulo a prime $p > n$.** The common case in programming contests, with $p = 10^9 + 7$ or $p = 998244353$.
- **Many values modulo a prime, with $n \le N$.** Answer $q$ queries after a precomputation that depends on $N$.
- **A small prime $p \le n$.** Factorials up to $n$ are $0$ modulo $p$, so the table method fails, and Lucas's theorem is needed.
- **A prime power or a composite modulus.** No inverses exist for the multiples of the prime factors. Solve modulo each prime power and combine by the [Chinese remainder theorem](/chinese-remainder-theorem/).
- **A whole row or a whole table.** Output $\binom{n}{0}, \ldots, \binom{n}{n}$, or all $\binom{i}{j}$ with $i \le n$ and $j \le k$.
- **The logarithm or a floating-point value.** Compute $\ln \binom{n}{k} = \ln n! - \ln k! - \ln (n-k)!$ with the log-gamma function, for probabilities, when an exact value is not needed.
- **The generalized coefficient** $\binom{r}{k} = r(r-1)\cdots(r-k+1)/k!$ for a rational or real $r$, by the same product.

## Examples

**1. The product formula, step by step.** For $\binom{10}{3}$, start with $r = 1$, and for $i = 1, 2, 3$ set $r \leftarrow r \cdot (n - k + i) / i$:

| $i$ | $r \cdot (n - k + i)$ | $/\, i$ | $r$ |
|---|---|---|---|
| 1 | $1 \cdot 8 = 8$ | $/1$ | $8 = \binom{8}{1}$ |
| 2 | $8 \cdot 9 = 72$ | $/2$ | $36 = \binom{9}{2}$ |
| 3 | $36 \cdot 10 = 360$ | $/3$ | $120 = \binom{10}{3}$ |

After step $i$, $r = \binom{n - k + i}{i}$, which is an integer, so each division is exact.

**2. Overflow.** $\binom{100}{50} = 100891344545564193334812497256$ has 97 bits. $20!$ is the largest factorial below $2^{64}$, so the formula $n!/(k!(n-k)!)$ in 64-bit arithmetic is wrong already for $\binom{21}{1} = 21$. The values $\binom{n}{\lfloor n/2 \rfloor}$ fit in an unsigned 64-bit word for $n \le 67$, and the product formula with the order of example 1 keeps every intermediate product below $2^{64}$ for all $k$ when $n \le 62$. See [integer overflow](/integer-overflow/).

**3. A prime modulus with tables.** For $p = 13$, the factorials $0!, \ldots, 10!$ modulo 13 are $1, 1, 2, 6, 11, 3, 5, 9, 7, 11, 6$. Then $\binom{10}{3} \equiv 10! \cdot (3!)^{-1} \cdot (7!)^{-1} \equiv 6 \cdot 11 \cdot 3 \equiv 3 \pmod{13}$, using the inverses $6^{-1} \equiv 11$ and $9^{-1} \equiv 3$ from [Fermat's little theorem](/fermat-little-theorem/). Indeed $120 = 9 \cdot 13 + 3$. For a larger case, $\binom{10^6}{5 \cdot 10^5} \bmod (10^9 + 7) = 996692777$, while the exact value has 999990 bits.

**4. A small prime (Lucas).** In base 7, $1000 = (2626)_7$ and $549 = (1413)_7$. Lucas's theorem gives $\binom{1000}{549} \equiv \binom{2}{1}\binom{6}{4}\binom{2}{1}\binom{6}{3} \equiv 2 \cdot 1 \cdot 2 \cdot 6 \equiv 3 \pmod 7$, from four binomials with entries below 7, while the exact value has 988 bits.

**5. A composite modulus.** For $\binom{20}{10} = 184756$ modulo $12 = 4 \cdot 3$: modulo 3, Lucas with $20 = (202)_3$ and $10 = (101)_3$ gives $\binom{2}{1}\binom{0}{0}\binom{2}{1} = 4 \equiv 1$; modulo 4, the value is $0$, since by Kummer's theorem (example 6) the exponent of 2 in $\binom{20}{10}$ is 2: adding $10 = (1010)_2$ to itself gives two carries. The Chinese remainder theorem gives the unique $x \in \{0, \ldots, 11\}$ with $x \equiv 0 \pmod 4$ and $x \equiv 1 \pmod 3$, so $x = 4$, and indeed $184756 = 15396 \cdot 12 + 4$.

**6. The exponent of a prime (Kummer).** The exponent of $p$ in $\binom{n}{k}$ equals the number of carries when $k$ and $n - k$ are added in base $p$. For $\binom{100}{50}$ and $p = 2$, adding $50 = (110010)_2$ to itself gives one carry for each of its three 1 bits, so $2^3$ divides $\binom{100}{50}$ and $2^4$ does not.

## Known algorithms

| method | exact or modular | cost | notes |
|---|---|---|---|
| factorial formula $n!/(k!(n-k)!)$ | exact | big integers of $\Theta(n \log n)$ bits | wasteful; overflows first |
| product formula, $k$ steps | exact | $k$ multiplications and divisions of an $L$-bit number by an $O(\log n)$-bit number, $O(kL/w)$ word operations | simple and good for one value |
| [Pascal's triangle](/pascal-triangle-dp/) | both | $O(nk)$ additions; $O(k)$ space for one row | works modulo any $m$, no division |
| prime factorization and a product tree | exact | a sieve up to $n$, then $O(M(L) \log n)$ bit operations | the method of choice for large exact values |
| factorial tables modulo $p > n$ | modular | $O(n + \log p)$ to build, $O(1)$ per query | needs a prime $p > n$ |
| [Lucas's theorem](/lucas-theorem/) | modulo a prime $p$ | $O(\log_p n)$ small binomials, each $O(1)$ with tables of size $p$ | for $p \le n$ |
| prime powers and CRT | modulo any $m$ | depends on the factorization of $m$ | combine with the [CRT](/chinese-remainder-theorem/) |

**Product formula.** Set $r \leftarrow 1$, and for $i = 1, \ldots, k$ set $r \leftarrow r \cdot (n - k + i) / i$. After step $i$, $r = \binom{n-k+i}{i}$, because $\binom{n-k+i}{i} = \binom{n-k+i-1}{i-1} \cdot \frac{n-k+i}{i}$. So every division is exact. The partial values increase with $i$, since $(n-k+i+1)/(i+1) \ge 1$, so none exceeds the answer, and each intermediate product is at most $n$ times the answer. Multiply first, then divide: $r \cdot ((n-k+i)/i)$ is not exact in integer arithmetic. Each step multiplies and divides a number of at most $L + \lg n$ bits by a single word, which takes $O(L/w + 1)$ word operations, so the total is $O(k L / w + k)$. For $k = n/2$ this is $O(n^2 / w)$. Knuth (Section 1.2.6) and Manolopoulos (2002) discuss this method against the recursive one.

**Prime factorization.** By [Legendre's formula](/legendre-formula/), the exponent of a prime $p$ in $n!$ is $\sum_{j \ge 1} \lfloor n / p^j \rfloor$, so the exponent of $p$ in $\binom{n}{k}$ is $\sum_{j \ge 1} \bigl(\lfloor n/p^j \rfloor - \lfloor k/p^j \rfloor - \lfloor (n-k)/p^j \rfloor\bigr)$ (Concrete Mathematics, Section 4.4). List the primes up to $n$ with a [sieve](/sieve-of-eratosthenes/), compute each exponent, and multiply the prime powers in a balanced binary tree, so that the large multiplications are between numbers of equal size and can use fast multiplication. Borwein (1985) analyzed this method for $n!$, and the same argument applies to $\binom{n}{k}$, whose factorization has only primes up to $n$ with exponents at most $\log_p n$.

**Factorial tables modulo a prime.** For a prime $p > n$, precompute $i! \bmod p$ for $i \le n$, then $(n!)^{-1} \bmod p$ by one [modular exponentiation](/modular-exponentiation/), and then $(i!)^{-1} = ((i+1)!)^{-1} \cdot (i + 1)$ for $i = n - 1, \ldots, 0$. A query is $n! \cdot (k!)^{-1} \cdot ((n-k)!)^{-1}$. When $p \le n$, all factorials from $p!$ on are $0$ modulo $p$, so this method breaks; see [factorial modulo a prime](/factorial-modulo-prime/).

**Lucas's theorem.** Write $n = \sum n_i p^i$ and $k = \sum k_i p^i$ in base $p$. Then $\binom{n}{k} \equiv \prod_i \binom{n_i}{k_i} \pmod p$, with $\binom{n_i}{k_i} = 0$ when $k_i > n_i$ (Lucas, 1878). With factorial tables of size $p$, a query costs $O(\log_p n)$.

**Prime powers and composite moduli.** For $m = \prod p_j^{e_j}$, compute $\binom{n}{k} \bmod p_j^{e_j}$ for each $j$ and combine with the CRT. Modulo $p^e$, write each factorial as $p^{v} \cdot u$ with $u$ coprime to $p$; the exponent $v$ comes from Legendre's formula, and $u \bmod p^e$ is computed from the product of the numbers coprime to $p$ in one block of $p^e$ consecutive integers, raised to the number of full blocks, times the partial block, times the same quantity for $\lfloor n/p \rfloor$. The answer is $0$ when the exponent of $p$ in $\binom{n}{k}$ is at least $e$.

## Bounds

- **Output size.** An exact algorithm must write $L$ bits, so it needs $\Omega(L/w)$ word operations. By the [binomial coefficient bounds](/binomial-coefficient-bounds/), $k \lg(n/k) \le L \le k \lg(en/k) + 1$ for $1 \le k \le n$, and $L = n - \tfrac12 \lg n + O(1)$ for $k = n/2$.
- **Product formula.** $\Theta(kL/w)$ word operations when $k$ and $L$ are large, because each of the $k$ steps touches all words of the partial result. This is quadratic in the output size for $k = \Theta(n)$.
- **Factorization method.** The sieve takes $O(n \log \log n)$ word operations. The product tree has $O(\log n)$ levels, since there are fewer than $n$ primes, and the numbers on one level have at most $L$ bits in total, so the products cost $O(M(L) \log n)$ bit operations. This is within a logarithmic factor of one multiplication of two $L$-bit numbers.
- **Modular, prime $p > n$.** $\Theta(n)$ precomputation and $O(1)$ per query; without tables, one query takes $O(k + \log p)$ operations by the product formula with a single inverse at the end.
- **Overflow limits in 64 bits.** All $\binom{n}{k}$ fit in an unsigned 64-bit word exactly for $n \le 67$. The direct factorial formula is safe only for $n \le 20$.

## Reductions

- **To factorials.** $\binom{n}{k} = n!/(k!\,(n-k)!)$, so an algorithm for $n! \bmod p$ gives one for $\binom{n}{k} \bmod p$ with two inverses. Conversely, $n! = \binom{n}{\lfloor n/2 \rfloor} \cdot \lfloor n/2 \rfloor! \cdot \lceil n/2 \rceil!$, so recursive halving computes $n!$ from central binomial coefficients.
- **From multinomials.** The [multinomial coefficient](/multinomial-coefficient/) $\binom{n}{k_1, \ldots, k_m}$ is a product of $m - 1$ binomial coefficients, so it reduces to this problem.
- **From path and multiset counts.** The number of monotone lattice paths from $(0,0)$ to $(a, b)$ is $\binom{a+b}{a}$ ([counting lattice paths](/counting-lattice-paths/)), the number of multisets of size $k$ from $n$ kinds is $\binom{n+k-1}{k}$ ([stars and bars](/stars-and-bars/)), and the [Catalan number](/catalan-numbers/) $C_n$ is $\binom{2n}{n}/(n+1)$.
- **Composite to prime powers.** By the CRT, the problem modulo $m$ reduces to the problem modulo each prime power that divides $m$.

## Applications

- **Counting.** Closed forms in [stars and bars](/stars-and-bars/), the [inclusion-exclusion principle](/inclusion-exclusion-principle/), [derangements](/derangement/) and lattice paths are sums of binomial coefficients, usually modulo a prime.
- **Ranking.** The [combinatorial number system](/combinatorial-number-system/) ranks $k$-subsets with a sum of binomial coefficients, and needs them exactly.
- **Probability and statistics.** The [binomial distribution](/binomial-distribution/) and the hypergeometric distribution need $\binom{n}{k}$, usually through its logarithm.
- **Analysis of algorithms.** Lower bounds such as $\lg \binom{2m}{m}$ comparisons to merge two sorted lists of length $m$.

## References
