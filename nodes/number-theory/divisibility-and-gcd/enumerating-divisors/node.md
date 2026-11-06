---
tag: GDT3BX
kind: problem
slug: enumerating-divisors
name: Enumerating divisors
aliases:
- listing divisors
- divisor generation
area: number-theory/divisibility-and-gcd
level: core
summary: List all divisors of n, given n's prime factorization.
prereqs: [divisor, divisor-function, fundamental-theorem-of-arithmetic]
see_also: [trial-division, integer-factorization, pollard-rho, divisor-count-sieve, multiplicative-order, necklace-counting, gray-code, mobius-inversion-formula]
sources:
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 16 (the divisors of n from its factorization, the function d(n)) and Chapter 18 (the order of magnitude of d(n))
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.1, Generating all n-tuples (mixed-radix counting and reflected mixed-radix Gray codes)
  - paper: "Srinivasa Ramanujan, Highly composite numbers, Proceedings of the London Mathematical Society (2) 14, 1915"
    locator: pages 347 to 409
  - url: "https://oeis.org/A002182"
    locator: OEIS A002182, Highly composite numbers (the record values of the number of divisors)
---

Enumerating divisors is the problem of listing all positive [divisors](/divisor/) of an integer $n$. When the prime factorization $n = p_1^{e_1} \cdots p_r^{e_r}$ is known, every divisor is a product $p_1^{f_1} \cdots p_r^{f_r}$ with $0 \le f_i \le e_i$, and all $d(n) = \prod (e_i + 1)$ of them can be produced with $d(n) - 1$ multiplications, which is optimal up to a constant factor because the output has $d(n)$ entries. When only $n$ is given, the work is dominated by [factoring](/integer-factorization/) it; [trial division](/trial-division/) up to $\sqrt n$ lists the divisors directly in $O(\sqrt n)$ divisions. The output stays small in practice: no $n \le 10^{18}$ has more than $103680$ divisors.

## In plain words

You want every whole number that divides a given number evenly. If you already know how the number breaks into primes, each divisor is a choice of how many copies of each prime to take, from none up to all of them. Going through all these choices lists every divisor exactly once, and each new divisor costs one multiplication.

If you do not know the primes, you can test every candidate up to the square root of the number. Each divisor you find below the square root comes with a partner above it, the number divided by it, so this finds all divisors. It is simple but slow for very large numbers; breaking the number into primes first is then faster.

## Definition

**Input.** An integer $n \ge 1$, either as its prime factorization, a list of pairs $(p_i, e_i)$ with distinct primes $p_i$ and exponents $e_i \ge 1$, or as the number $n$ alone.

**Output.** The set $D(n) = \{ d \ge 1 : d \mid n \}$, as a list of its $d(n)$ elements, in any order or in increasing order, as the variant requires.

Negative $n$ have the same positive divisors as $|n|$, and the negative divisors are their negatives. The input $n = 0$ is excluded, because every positive integer divides $0$. For $n = 1$ the output is the single divisor $1$, and the empty factorization.

**Cost model.** For $n$ that fits in a machine word, a multiplication or a division costs one step on the [word RAM](/word-ram/). For large $n$ of $b$ binary digits, each divisor has at most $b$ digits, and the bounds below are multiplied by the cost of one multiplication of such numbers.

## Variants

- **Sorted or unsorted.** The product method produces the divisors in a mixed-radix order. Sorting adds $O(d(n) \log d(n))$ comparisons; merging the $e + 1$ sorted lists $L, pL, \ldots, p^e L$ at each prime step gives sorted output directly.
- **Only the count or the sum.** $d(n)$ and $\sigma(n)$ need only the factorization, by the formulas of the [divisor function](/divisor-function/), not the list.
- **Divisors in a range.** Only the divisors up to a bound $B$, or in an interval; the product method can prune a branch as soon as the partial product exceeds $B$.
- **One change at a time.** List the divisors so that consecutive ones differ by one multiplication or one division by a single prime. This is a reflected mixed-radix [Gray code](/gray-code/) on the exponent vectors.
- **Divisors of all $n \le N$.** For each $d \le N$, append $d$ to the lists of its multiples $d, 2d, 3d, \ldots$. This takes $\sum_{d \le N} \lfloor N/d \rfloor = N \ln N + O(N)$ steps and as much memory, by the [harmonic series](/harmonic-series/); see [divisor count sieve](/divisor-count-sieve/).
- **Unitary divisors.** Only the divisors $d$ with $\gcd(d, n/d) = 1$; there are $2^r$ of them, one for each subset of the prime powers $p_i^{e_i}$.

## Examples

**From the factorization.** Let $n = 360 = 2^3 \cdot 3^2 \cdot 5$, so $d(360) = 4 \cdot 3 \cdot 2 = 24$. Start from the list $[1]$. The prime $2$ with exponent $3$ extends it to $[1, 2, 4, 8]$. The prime $3$ with exponent $2$ appends the list times $3$ and times $9$: $[1, 2, 4, 8, 3, 6, 12, 24, 9, 18, 36, 72]$. The prime $5$ appends the list times $5$, for $24$ divisors in all. Each new entry costs one multiplication, so $23$ multiplications in total. Sorted, the divisors are $1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 60, 72, 90, 120, 180, 360$.

**By trial division.** For $n = 36$, test $i = 1, \ldots, 6$. The hits are $1, 2, 3, 4, 6$, with partners $36, 18, 12, 9$, and $6$ is its own partner, so it is listed once. Reading the small divisors forward and the partners backward gives the sorted list $1, 2, 3, 4, 6, 9, 12, 18, 36$, with $d(36) = 9$ odd because $36$ is a square.

**A Gray code order.** For $12 = 2^2 \cdot 3$, the exponent pairs in reflected order are $(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1)$, which list the divisors $1, 2, 4, 12, 6, 3$: multiply by $2$, by $2$, by $3$, then divide by $2$ twice.

**Large outputs.** The number below $10^9$ with the most divisors is $735134400 = 2^6 \cdot 3^3 \cdot 5^2 \cdot 7 \cdot 11 \cdot 13 \cdot 17$, with $7 \cdot 4 \cdot 3 \cdot 2^4 = 1344$ divisors. Below $10^{18}$ it is $897612484786617600 = 2^8 \cdot 3^4 \cdot 5^2 \cdot 7^2 \cdot 11 \cdot 13 \cdot 17 \cdot 19 \cdot 23 \cdot 29 \cdot 31 \cdot 37$, with $103680$ divisors.

## Known algorithms

**The product method (given the factorization).** Keep a list, initially $[1]$. For each prime power $p^e$ in the factorization, replace the list $L$ by $L \cup pL \cup p^2 L \cup \cdots \cup p^e L$, computing each new block from the previous one by one multiplication per entry. Each divisor is produced exactly once, by the uniqueness of the factorization, and each costs one multiplication, so the time is $\Theta(d(n))$ and the memory is the output. It can also be written as a mixed-radix counter over the exponent vectors $(f_1, \ldots, f_r)$, or as a depth-first search over the primes, which yields the divisors one at a time with $O(r)$ extra memory.

**Trial division up to $\sqrt n$.** For $i = 1, 2, \ldots, \lfloor \sqrt n \rfloor$, if $i \mid n$ output $i$ and, if $i \ne n/i$, also $n/i$. This takes $\lfloor \sqrt n \rfloor$ divisions and gives sorted output with one extra list. It needs no factorization, and it is the right choice for one $n$ up to about $10^{12}$.

**Factor, then generate.** Factor $n$ first, by [trial division](/trial-division/) in $O(\sqrt n)$ or, for large $n$, by [Pollard's rho](/pollard-rho/) in about $n^{1/4}$ steps for each prime factor found, then run the product method. For $n$ near $10^{18}$ this is far faster than $10^9$ trial divisions.

**Sieve for all $n \le N$.** Iterate $d = 1, \ldots, N$ and add $d$ to the list of each multiple. Time and memory $\Theta(N \log N)$. If only the factorizations are needed, a [smallest prime factor table](/smallest-prime-factor-table/) from a [linear sieve](/linear-sieve/) stores them in $O(N)$ memory, and the product method then lists the divisors of any $n \le N$ on demand.

| setting | method | time |
|---|---|---|
| factorization given | product method | $\Theta(d(n))$ |
| one $n$, small | trial division to $\sqrt n$ | $\Theta(\sqrt n)$ |
| one $n$, large | factor by Pollard's rho, then product method | about $n^{1/4}$ for factoring, plus $\Theta(d(n))$ |
| all $n \le N$ | sieve over multiples | $\Theta(N \log N)$ |

## Bounds

**Output size.** The output has $d(n)$ entries, so $\Omega(d(n))$ time is necessary, and the product method meets it. The size is small: $d(n) \le 2\sqrt n$ always, and $d(n) = n^{O(1 / \log \log n)}$, which is $n^{o(1)}$. The record values for $n \le 10^3$, $10^6$, $10^9$, $10^{12}$ and $10^{18}$ are $32$ (at $840$), $240$ (at $720720$), $1344$, $6720$ (at $963761198400$) and $103680$. These maxima are reached at *highly composite numbers*, whose exponents do not increase along the primes $2, 3, 5, \ldots$; Ramanujan studied their structure in 1915.

**Average output size.** The average of $d(n)$ over $n \le N$ is $\ln N + 2\gamma - 1 + O(N^{-1/2})$, about $21$ for $N = 10^9$; see the [divisor summatory function](/divisor-summatory-function/).

**Without the factorization.** Listing the divisors is at least as hard as factoring: the smallest divisor greater than $1$ is a prime, and dividing it out and repeating gives the factorization from the list. So no method much faster than the best [integer factorization](/integer-factorization/) algorithms is known for general large $n$.

## Reductions

- **Factoring reduces to enumerating.** From the list of divisors, the primes are the divisors greater than $1$ that have no other divisor greater than $1$ in the list, and their exponents follow by repeated division. So an enumeration algorithm for all $n$ would factor $n$.
- **Computing $\sigma(n)$ can be as hard as factoring.** For an RSA-style modulus $n = pq$, $\sigma(n) = 1 + p + q + n$ gives $p + q$, and $p$ and $q$ are then the roots of $z^2 - (p + q) z + n$. So computing $\sigma(n)$ alone, without listing, is as hard as factoring such $n$.
- **Enumerating reduces to factoring.** By the product method, given the factorization the list costs $\Theta(d(n))$ more.
- **Sums over divisors.** Many problems ask for $\sum_{d \mid n} f(d)$. For multiplicative $f$ this is a product over the primes and needs no enumeration; for other $f$, enumerate.

## Applications

- **Divisor sums.** [Möbius inversion](/mobius-inversion-formula/), [Dirichlet convolution](/dirichlet-convolution/) and the [divisor function](/divisor-function/) for non-multiplicative summands.
- **Orders in groups.** The [multiplicative order](/multiplicative-order/) of $a$ modulo $m$ divides the group order, so it can be found by testing divisors of that order; with the factorization, removing prime factors one at a time is faster.
- **Counting necklaces.** The number of necklaces of length $n$ over $k$ colours is $\frac1n \sum_{d \mid n} \varphi(d) k^{n/d}$, a sum over the divisors of $n$ ([necklace counting](/necklace-counting/)).
- **Cyclotomic factorization.** $x^n - 1 = \prod_{d \mid n} \Phi_d(x)$ factors over the divisors of $n$; FFT sizes and periodic structures are chosen among divisors.
- **Perfect and amicable numbers.** Searches compute the aliquot sum $\sigma(n) - n$ for many $n$.
- **Factor pairs.** All rectangles of area $n$ with integer sides, all ways to split $n$ items into equal groups, and all periods $p \mid n$ of a string of length $n$ come from the divisors of $n$.

## References
