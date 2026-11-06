---
tag: SRGWMG
kind: problem
slug: all-pairs-gcd
name: All-pairs GCD
aliases:
- pairwise gcd problem
- batch GCD problem
area: number-theory/divisibility-and-gcd
level: advanced
summary: Find gcd(a_i, a_j) for every pair among n integers, or detect pairs with a nontrivial gcd.
prereqs: [greatest-common-divisor, euclidean-algorithm, coprime-integers]
see_also: [batch-gcd, subproduct-tree, scaled-remainder-tree, rsa-cryptosystem, integer-factorization, euler-totient, binary-gcd, mobius-inversion-formula]
sources:
  - paper: "Daniel J. Bernstein, Fast multiplication and its applications, in Algorithmic Number Theory, MSRI Publications 44, Cambridge University Press, 2008"
    locator: pages 325 to 384 (product trees, remainder trees and their use for many gcds at once)
  - paper: "Nadia Heninger, Zakir Durumeric, Eric Wustrow and J. Alex Halderman, Mining your Ps and Qs: detection of widespread weak keys in network devices, Proceedings of the 21st USENIX Security Symposium, 2012"
    locator: pages 205 to 220 (all-pairs gcd of 11 million RSA moduli, factoring keys of 0.50% of TLS hosts)
  - paper: "Arjen K. Lenstra, James P. Hughes, Maxime Augier, Joppe W. Bos, Thorsten Kleinjung and Christophe Wachter, Ron was wrong, Whit is right, Advances in Cryptology (CRYPTO 2012), Lecture Notes in Computer Science 7417"
    locator: pages 626 to 642
  - paper: "H. J. S. Smith, On the value of a certain arithmetical determinant, Proceedings of the London Mathematical Society 7, 1875"
    locator: pages 208 to 212
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The greatest common divisor (gcds of many numbers, and the probability 6/pi^2 that two random integers are coprime)
---

The all-pairs GCD problem takes $n$ integers $a_1, \ldots, a_n$ and asks for $\gcd(a_i, a_j)$ for every pair $i < j$, or, in its most used form, for the pairs that share a factor greater than $1$. Running the [Euclidean algorithm](/euclidean-algorithm/) on all $\binom n2$ pairs is quadratic in $n$, which is too slow for millions of large numbers. Bernstein's [batch GCD](/batch-gcd/) computes $\gcd(a_i, \prod_{j \ne i} a_j)$ for every $i$ in time quasi-linear in the total input size, using a [product tree](/subproduct-tree/) and a remainder tree, and this reveals every $a_i$ that shares a factor with some other input. In 2012 two research groups ran it on millions of RSA public keys collected from the internet and factored tens of thousands of them, because badly seeded generators had produced moduli with a common prime.

## In plain words

You have a long list of whole numbers, and you want to know which pairs have a common factor bigger than one. Checking every pair works, but the number of pairs grows with the square of the list, so a list of a million numbers has half a trillion pairs.

A faster way multiplies everything together first. If a number shares a factor with any other number in the list, it shares that factor with the product of all the others. Multiplying in a balanced tree and then reducing back down the tree gives, for each number, its common factor with the rest of the list, all at once. Only the few numbers that turn out to have a common factor need a closer look to find their partners.

## Definition

**Input.** Integers $a_1, \ldots, a_n$, each of at most $\beta$ binary digits. Signs do not matter, since $\gcd(a, b) = \gcd(|a|, |b|)$; a zero entry has $\gcd(0, a_j) = |a_j|$, so it shares a factor with every entry other than $\pm 1$, and inputs usually exclude it.

**Output, in one of three forms.**

1. **Full table.** All $\binom n2$ values $\gcd(a_i, a_j)$ for $i < j$.
2. **Detection.** For each $i$, the value $g_i = \gcd\bigl(a_i, \prod_{j \ne i} a_j\bigr)$. Then $g_i > 1$ if and only if $a_i$ shares a factor with some other $a_j$.
3. **Pairs.** All pairs $(i, j)$ with $\gcd(a_i, a_j) > 1$, together with these gcds.

**Cost model.** Numbers are in arbitrary precision. $M(k)$ is the cost of multiplying two $k$-digit integers, $O(k \log k)$ with the Harvey and van der Hoeven algorithm and $O(k^{1.585})$ with Karatsuba; one gcd of $\beta$-digit numbers costs $O(\beta^2)$ with the Euclidean algorithm or $O(M(\beta) \log \beta)$ with a half-gcd. The input size is $N = n\beta$.

## Variants

- **Shared factors in a fixed set of moduli.** The RSA case: each $a_i = p_i q_i$ is a product of two primes of about $\beta/2$ digits, and the task is to find all moduli with a prime in common with another modulus.
- **Coprime base.** Replace the list by a set of pairwise coprime numbers such that each $a_i$ is a product of powers of them, Bernstein's factoring into coprimes, which also runs in essentially linear time.
- **Small values.** All $a_i \le V$ for a bound $V$ that fits in memory: count, for each $g$, the pairs with $\gcd(a_i, a_j) = g$. Let $c(d)$ be the number of $a_i$ divisible by $d$; then the number of pairs with $d \mid \gcd$ is $\binom{c(d)}{2}$, and the exact counts $e(d) = \binom{c(d)}{2} - \sum_{k \ge 2} e(kd)$ follow by going down from $d = V$. This takes $O(V \log V)$ steps, a sieve over multiples, independent of the number of pairs.
- **The gcd matrix.** The $n \times n$ matrix $(\gcd(i, j))$ for $1 \le i, j \le n$. Since $\gcd(i, j) = \sum_{d \mid i, d \mid j} \varphi(d)$, it factors as $E \Phi E^{T}$ with $E$ the divisibility matrix and $\Phi$ the diagonal of the [totient](/euler-totient/) values, so its determinant is $\varphi(1) \varphi(2) \cdots \varphi(n)$ (Smith, 1875).
- **Gcd sums.** $\sum_{i, j \le n} \gcd(i, j) = \sum_{d \le n} \varphi(d) \lfloor n/d \rfloor^2$, computable without forming the pairs.

## Examples

**Full table.** For $(12, 18, 35, 49, 10)$:

| | 12 | 18 | 35 | 49 | 10 |
|---|---|---|---|---|---|
| 12 | | 6 | 1 | 1 | 2 |
| 18 | 6 | | 1 | 1 | 2 |
| 35 | 1 | 1 | | 7 | 5 |
| 49 | 1 | 1 | 7 | | 1 |
| 10 | 2 | 2 | 5 | 1 | |

The detection values $g_i = \gcd(a_i, P/a_i)$ with $P = 12 \cdot 18 \cdot 35 \cdot 49 \cdot 10$ are $(12, 6, 35, 7, 10)$. Every entry has $g_i > 1$, so each shares a factor with another one. But $g_i$ is the gcd with the product of all the others, not a gcd of a pair: $g_1 = 12$, although no single pair has gcd $12$, because the factor $4$ comes from $18 \cdot 10$ and the $3$ from $18$.

**RSA-style moduli.** Take $a = (101 \cdot 103, \; 101 \cdot 107, \; 109 \cdot 113, \; 113 \cdot 127) = (10403, 10807, 12317, 14351)$. The detection values are $(101, 101, 113, 113)$: each modulus is factored by one gcd. If both primes of a modulus were shared with others, $g_i$ would be the modulus itself, and pairwise gcds among the flagged moduli would be needed to split it.

**Small values.** For $(12, 18, 35, 49, 10, 6, 14, 21)$ the 28 pairs have gcd $1$ eight times, $2$ seven times, $3$ three times, $5$ once, $6$ three times and $7$ six times, as the sieve over multiples finds without forming the pairs.

**Gcd matrix.** For $n = 6$ the determinant of $(\gcd(i, j))_{i, j \le 6}$ is $\varphi(1) \cdots \varphi(6) = 1 \cdot 1 \cdot 2 \cdot 2 \cdot 4 \cdot 2 = 32$, and $\sum_{i, j \le 6} \gcd(i, j) = 61$.

## Known algorithms

| algorithm | output | cost |
|---|---|---|
| all pairs with the Euclidean algorithm | full table | $\binom n2$ gcds, $O(n^2 \beta^2)$ |
| all pairs with a half-gcd | full table | $O(n^2 M(\beta) \log \beta)$ |
| [batch GCD](/batch-gcd/) | detection | $O(M(N) \log n)$ for the trees, plus $n$ gcds |
| batch GCD, then pairwise gcds among the flagged inputs | pairs | as above, plus $\binom{f}{2}$ gcds for $f$ flagged inputs |
| sieve over multiples | counts by gcd value, all $a_i \le V$ | $O(V \log V + n)$ |

**Pairwise.** The direct method needs no extra memory and is right for small $n$, or when the full table is the output. [Binary GCD](/binary-gcd/) on word-sized inputs gives $O(n^2 \beta)$ word operations.

**Batch GCD.** Build the product tree of the $a_i$ with root $P = \prod a_i$. Push $P$ down a remainder tree, reducing modulo the square of each node, so that each leaf receives $P \bmod a_i^2$. Then $(P \bmod a_i^2)/a_i = (P/a_i) \bmod a_i$, and $g_i = \gcd(a_i, (P/a_i) \bmod a_i)$. Both trees have $\lceil \lg n \rceil$ levels, each level multiplies or divides numbers of total size $O(N)$, so the cost is $O(M(N) \log n)$, which is $O(N \log N \log n)$ with fast multiplication. See [batch GCD](/batch-gcd/) and [scaled remainder trees](/scaled-remainder-tree/) for a constant-factor faster form.

**Recovering pairs.** After detection, only the inputs with $g_i > 1$ remain. Usually they are few, and pairwise gcds among them, or a second batch run on groups, finish the job. If $g_i = a_i$, all prime factors of $a_i$ appear elsewhere, and pairwise gcds with the other flagged inputs split it.

## Bounds

- **Output size.** The full table has $\binom n2$ entries, so it needs $\Omega(n^2)$ time; the pairwise method meets this up to the cost of one gcd.
- **Detection.** Reading the input takes $\Omega(N)$, and batch GCD is within a factor $O(\log N \log n)$ of that. No better lower bound is known.
- **Memory.** The product tree holds $O(N)$ digits per level and $O(N \log n)$ in total if all levels are kept; for 11 million RSA moduli of 1024 binary digits the levels are gigabytes, so large runs split the input into groups and combine the results.
- **How many pairs share a factor.** For random integers, $\gcd(a_i, a_j) = 1$ with probability tending to $6/\pi^2 \approx 0.608$; for random RSA moduli of distinct primes, a shared factor is so unlikely that every hit indicates a broken generator.

## Reductions

- **Detection reduces to one gcd per input** with the product of the others, $g_i = \gcd(a_i, P/a_i)$, which is what makes the problem quasi-linear.
- **Product of the others without division.** $(P/a_i) \bmod a_i = (P \bmod a_i^2)/a_i$, since $P = a_i \cdot (P/a_i)$; this avoids $n$ divisions of the huge $P$.
- **To multipoint evaluation.** Computing $P \bmod a_i$ for all $i$ is the integer form of evaluating a polynomial at many points, solved by the same [subproduct tree](/subproduct-tree/).
- **Factoring.** A nontrivial $g_i$ is a factor of $a_i$; for products of two primes, it is a complete [factorization](/integer-factorization/). So all-pairs gcd is a way to factor many weak keys at once, with no general factoring algorithm involved.
- **Gcd sums to Dirichlet convolution.** $\gcd(i, j) = \sum_{d \mid \gcd(i, j)} \varphi(d)$ turns gcd sums over boxes into sums of $\varphi(d)$ times counts of multiples, the same device as [Möbius inversion](/mobius-inversion-formula/).

## Applications

- **Weak RSA keys.** Heninger, Durumeric, Wustrow and Halderman collected 11 million distinct RSA moduli from TLS and SSH hosts, ran batch GCD, and obtained private keys for $0.50\%$ of the TLS hosts and $0.03\%$ of the SSH hosts. Lenstra, Hughes, Augier, Bos, Kleinjung and Wachter found the same problem independently in a set of public keys. The cause was low entropy at boot time in embedded devices, which made different devices pick the same first prime. See [RSA](/rsa-cryptosystem/).
- **Auditing key generators.** Certificate authorities and researchers rerun batch GCD on new key collections.
- **Coprime bases.** Factoring a set of numbers into coprimes is used in algebraic number theory and in simplifying products of many integers.
- **Gcd matrices and sums.** Smith's determinant and the sums $\sum \gcd(i, j)$ appear in number theory exercises and contest problems, where the sieve over multiples is the standard method.

## References
