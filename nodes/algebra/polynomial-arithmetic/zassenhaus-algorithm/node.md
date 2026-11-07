---
tag: 0Y712F
kind: algorithm
slug: zassenhaus-algorithm
name: Zassenhaus algorithm
aliases:
- Berlekamp-Zassenhaus algorithm
- Zassenhaus factorization
- Zassenhaus recombination
area: algebra/polynomial-arithmetic
level: advanced
summary: Factors integer polynomials by factoring modulo a prime, Hensel lifting the factors, and trying products of subsets of them. Fast in practice, exponential in the worst case.
solves: [polynomial-factorization-over-integers]
model: multitape-turing-machine
complexity:
  vars: {n: the degree of f, r: the number of irreducible factors of f modulo the chosen prime p, L: the length in binary digits of the largest coefficient of f}
  time: {expected: O(r 2^r n^2 (n + L)^2 + r n^2 (n + L)^3)}
  space: {extra: O(n (n + L))}
  candidates: {worst: O(r 2^r)}
properties: {deterministic: false, recursive: false, in_place: false}
prereqs: [polynomial-factorization-over-integers, polynomial-factorization-over-finite-fields, hensel-lifting]
see_also: [polynomial-factorization-over-integers, hensel-lifting, polynomial-factorization-over-finite-fields, cantor-zassenhaus-algorithm, berlekamp-factorization, lll-algorithm, gauss-lemma, square-free-factorization]
sources:
  - paper: doi:10.1016/0022-314X(69)90047-X
    title: Hans Zassenhaus, On Hensel factorization I, Journal of Number Theory 1(3), 1969
    locator: pp. 291 to 311
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 15, Hensel lifting and factoring polynomials (Sections 15.4 to 15.6); Section 6.6 for Mignotte's factor bound
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.2, Factorization of Polynomials (factoring over the integers)
  - paper: doi:10.1002/j.1538-7305.1967.tb03174.x
    title: Elwyn R. Berlekamp, Factoring polynomials over finite fields, Bell System Technical Journal 46(8), 1967
    locator: pp. 1853 to 1859
  - paper: doi:10.1007/BF01457454
    title: Arjen K. Lenstra, Hendrik W. Lenstra Jr. and László Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261(4), 1982
    locator: pp. 515 to 534
  - paper: doi:10.1006/jnth.2001.2763
    title: Mark van Hoeij, Factoring polynomials and the knapsack problem, Journal of Number Theory 95(2), 2002
    locator: pp. 167 to 189
---

The Zassenhaus algorithm factors a polynomial $f \in \mathbb{Z}[x]$ into irreducible polynomials. It factors $f$ modulo a small prime $p$, lifts that factorization to one modulo a large power $p^k$ with [Hensel lifting](/hensel-lifting/), and then tests products of subsets of the lifted factors to find the true factors over $\mathbb{Z}$. The first two stages take polynomial time, but the last can try up to about $2^r$ subsets, where $r$ is the number of factors modulo $p$, so the worst case is exponential. In practice $r$ is usually small and the algorithm is fast; Zassenhaus published it in 1969, using [Berlekamp's](/berlekamp-factorization/) factoring modulo $p$.

## In plain words

Factoring with whole-number coefficients is hard to do directly, but factoring with coefficients modulo a small prime is easy. So the method first factors the polynomial modulo a prime. Every true factor breaks up modulo the prime into some of the small pieces, but a true factor can break into several pieces, so the pieces do not show the answer directly.

Next the method makes the pieces exact modulo a very large power of the prime, so large that every true factor can be read off from its remainder. Then it tries groups of pieces: one piece, then two pieces, and so on. For each group it multiplies the pieces and checks whether the product is a true factor. When it finds one, it removes those pieces and goes on. The number of groups can be very large when the polynomial has many pieces modulo the prime.

## The problem

Given $f \in \mathbb{Z}[x]$ of degree $n \ge 1$, [primitive](/primitive-polynomial/), square-free and with $\operatorname{lc}(f) > 0$, find the irreducible $g_1, \ldots, g_m \in \mathbb{Z}[x]$, primitive with positive leading coefficients, with $f = g_1 \cdots g_m$. A general $f \in \mathbb{Z}[x]$ is first reduced to this case: remove the content, and take a [square-free factorization](/square-free-factorization/). This is the [factorization problem over the integers](/polynomial-factorization-over-integers/).

**Cost model.** The algorithm works with integers of growing size, so we count bit operations, as on a [multitape Turing machine](/multitape-turing-machine/), with schoolbook integer arithmetic. $n = \deg f$, $L$ is the length of the largest coefficient of $f$ in binary digits, and $r$ is the number of irreducible factors of $f$ modulo the chosen prime $p$. The factorization modulo $p$ is randomized, so the bound is for the expected cost.

## The algorithm

The norms are $\|a\|_1 = \sum |a_i|$ and $\|a\|_2 = (\sum a_i^2)^{1/2}$. "$a$ mods $m$" is the representative of $a$ modulo $m$ with coefficients in $(-m/2, m/2]$, and $\operatorname{pp}$ is the primitive part.

```pseudo id=main
ZASSENHAUS(f)                        ▷ f primitive, square-free, lc(f) > 0, deg f = n ≥ 1
L1  p ← the least prime with p ∤ lc(f) and f mod p square-free
L2  u_1, …, u_r ← the monic irreducible factors of f mod p
L3  B ← 2^n · lc(f) · (⌊‖f‖₂⌋ + 1);  k ← least with p^k > 2B
L4  v_1, …, v_r ← Hensel lifts: v_i monic, v_i ≡ u_i (mod p), f ≡ lc(f) v_1 ⋯ v_r (mod p^k)
L5  T ← {v_1, …, v_r};  F ← f;  G ← [ ];  s ← 1
L6  while 2s ≤ |T| do
L7      find the first S ⊆ T with |S| = s and ‖g*‖₁ ‖h*‖₁ ≤ B, where g* ← lc(F) ∏_{v∈S} v mods p^k and h* ← lc(F) ∏_{v∈T∖S} v mods p^k
L8      if such S exists then G ← G + [pp(g*)];  F ← pp(h*);  T ← T ∖ S
L9      else s ← s + 1
L10 return G + [F]
```

Line L2 uses [distinct-degree factorization](/distinct-degree-factorization/) and the [Cantor-Zassenhaus](/cantor-zassenhaus-algorithm/) splitting in the implementation; Berlekamp's algorithm also works. Line L4 uses linear Hensel lifting, one power of $p$ at a time. The bound $B$ in line L3 is chosen so that every true factor, scaled by $\operatorname{lc}(F)$, has coefficients smaller than $p^k/2$; then it equals its symmetric remainder modulo $p^k$. The test in line L7 is the one of von zur Gathen and Gerhard, Chapter 15: if the two products are small enough, then $g^* h^* = \operatorname{lc}(F) F$ exactly, with no trial division.

## Example

Let $f = x^4 - x^2 - 2 = (x^2 - 2)(x^2 + 1)$.

- **L1.** $p = 2$ and $p = 3$ fail: $f \equiv x^2(x^2 + 1)$ modulo $2$ and $f \equiv (x^2 + 1)^2$ modulo $3$. So $p = 5$.
- **L2.** $f \equiv (x + 2)(x + 3)(x^2 + 3) \pmod 5$, so $r = 3$. The factor $x^2 + 1$ splits as $(x + 2)(x + 3)$, but $x^2 - 2 \equiv x^2 + 3$ stays irreducible, as $2$ is not a square modulo $5$.
- **L3.** $\|f\|_2 = \sqrt 6$, so $B = 16 \cdot 1 \cdot 3 = 48$, and $k = 3$: $5^3 = 125 > 96$.
- **L4.** The lifts modulo $125$ are $x + 57$, $x - 57$ and $x^2 - 2$; indeed $57^2 = 3249 \equiv -1 \pmod{125}$.

The recombination:

| $T$ | $S$ | $g^*$ | $h^*$ | $\|g^*\|_1 \|h^*\|_1$ | result |
|---|---|---|---|---|---|
| all three | $\{x + 57\}$ | $x + 57$ | $x^3 - 57x^2 - 2x - 11$ | $58 \cdot 71 = 4118$ | reject |
| all three | $\{x - 57\}$ | $x - 57$ | $x^3 + 57x^2 - 2x + 11$ | $4118$ | reject |
| all three | $\{x^2 - 2\}$ | $x^2 - 2$ | $x^2 + 1$ | $3 \cdot 2 = 6$ | accept |
| $\{x \pm 57\}$ | $\{x + 57\}$ | $x + 57$ | $x - 57$ | $3364$ | reject |
| $\{x \pm 57\}$ | $\{x - 57\}$ | $x - 57$ | $x + 57$ | $3364$ | reject |

After the accepted step, $G = [x^2 - 2]$ and $F = x^2 + 1$. Then $s$ becomes $2$, and $2s = 4 > |T| = 2$, so the loop stops. The output is $[x^2 - 2, x^2 + 1]$. The factor $x^2 + 1$ corresponds to two factors modulo $5$, so no single lifted factor could show it. The tests check every number in this trace.

## Correctness

Line L1 stops, because $s f + t f' = R$ for some $s, t \in \mathbb{Z}[x]$ and a nonzero integer $R$, and every prime that divides neither $R$ nor $\operatorname{lc}(f)$ is good. Hensel lifting gives monic lifts $v_i$, and they are unique: two lifts of the same factorization modulo $p$ agree modulo $p^k$. Every factor $h$ of the current $F$ reduces modulo $p$ to the product of a unique subset $S(h)$ of $T$. By uniqueness of the lifts, $g^*$ for that subset is exactly $\frac{\operatorname{lc}(F)}{\operatorname{lc}(h)} h$, because Mignotte's bound shows that its coefficients are below $p^k/2$; so true factors pass the test. Conversely, if the test passes, then $g^* h^*$ and $\operatorname{lc}(F) F$ are congruent and both small, so they are equal, and $\operatorname{pp}(g^*)$ is a true factor. Subsets are tried in order of size, so the first factor found for each size is irreducible. When $2s > |T|$, the remaining $F$ has no factor whose subset has fewer than $s$ elements, so it is irreducible. The full proof is below.

## Complexity

The costs are for the implementation, with schoolbook integer arithmetic. The numbers modulo $p^k$ have $O(\log B) = O(n + L)$ binary digits, since $\|f\|_2 \le (n + 1)^{1/2} 2^L$ and $\operatorname{lc}(f) \le 2^L$.

- **Line L1.** At most $\log_2 |R \operatorname{lc}(f)|$ primes are bad, so $p$ is small, with $O(\log(n + L))$ binary digits.
- **Line L2.** Expected $O(n^3 \log p)$ operations in $\mathbb{F}_p$ for the factorization modulo $p$; this is small next to the rest.
- **Line L4.** $k = O((n + L)/\log p)$ lifting steps for each of $r - 1$ splits, each step a few products of degree at most $n$ with coefficients of $O(n + L)$ binary digits. Total $O(r\, n^2 (n + L)^3)$. This is proved. Quadratic lifting and a factor tree, as in von zur Gathen and Gerhard, Chapter 15, reduce it.
- **Lines L6 to L9.** Each candidate $S$ costs two products modulo $p^k$, $O(n^2 (n + L)^2)$. For each size $s$ the subsets are listed at most once after each found factor, so there are at most $(r + 1) 2^r$ candidates in all. Total $O(r\, 2^r n^2 (n + L)^2)$ in the worst case. This is proved.
- **Space.** $O(n (n + L))$ binary digits for the lifted factors and the current products.

**Worst case and practice.** The exponential term is real. The Swinnerton-Dyer polynomials, such as $x^4 - 10x^2 + 1$, are irreducible over $\mathbb{Z}$ but split into factors of degree at most $2$ modulo every prime, so $r \ge n/2$ for every choice of $p$. Such inputs of degree $2^m$ make the recombination try exponentially many subsets. For random polynomials, $r$ is small, about $\ln n$ on average for a random polynomial modulo $p$, and the recombination is cheap. This is observed in practice and agrees with the average number of irreducible factors of random polynomials over finite fields.

## Properties

- **Output.** The irreducible factors, primitive with positive leading coefficients, whose product is $f$. Their order is the order in which they were found.
- **Randomized only in line L2.** The answer does not depend on the random choices; only the running time does. With Berlekamp's deterministic algorithm for small $p$, the whole algorithm is deterministic.
- **Exact.** All arithmetic is with integers; no floating point is used.
- **Early stop.** If $r = 1$, then $f$ is irreducible and the recombination is skipped. This makes the method a fast irreducibility test for most inputs.
- Not recursive; the implementation uses loops and a work list.

## Variants and improvements

- **Several primes.** Factor modulo a few good primes and keep the prime with the fewest factors. The factor degrees modulo different primes also limit the possible degrees of true factors, so many subsets can be skipped.
- **Degree and coefficient tests.** Before the full test, check cheap necessary conditions, such as whether the constant term of $g^*$ divides $\operatorname{lc}(F) F(0)$, which holds for every true factor because $g^* h^* = \operatorname{lc}(F) F$.
- **Complementary subsets.** When $2s = |T|$, a subset and its complement give the same split, so only subsets that contain a fixed element need to be tried.
- **Quadratic Hensel lifting.** Lifting from $p^{2^j}$ to $p^{2^{j+1}}$ needs $O(\log k)$ steps instead of $k - 1$; with a factor tree all $r$ factors are lifted together.
- **Lattice reduction.** Lenstra, Lenstra and Lovász (1982) replaced the subset search by finding a short vector in a lattice with the [LLL algorithm](/lll-algorithm/), which gives polynomial time in the worst case. Van Hoeij (2002) combined lattice reduction with the recombination, solving it as a [knapsack](/knapsack-problem/)-type problem with LLL. This is fast in practice also for inputs with large $r$, and modern systems use it.

## When to use it

Use the Zassenhaus algorithm to factor integer polynomials of moderate degree, when the number of factors modulo a prime is small, which is the common case. For inputs with many factors modulo every prime, such as Swinnerton-Dyer polynomials, use van Hoeij's method. For a polynomial over $\mathbb{Q}$, clear denominators first; for a polynomial with repeated factors, take the square-free factorization first.

## Pitfalls

- **Square-free input.** If $f$ is not square-free, no prime makes $f \bmod p$ square-free, and line L1 never stops. The implementation checks the input first and raises an error.
- **Bad primes.** A prime that divides $\operatorname{lc}(f)$ drops the degree, and a prime with a repeated factor modulo $p$ breaks Hensel lifting. Both must be skipped.
- **The bound.** If $p^k$ is not larger than twice the bound on the factors, a true factor can be missed, and the output may contain reducible polynomials. Use a proved bound such as Mignotte's, not a guess from the input coefficients.
- **Leading coefficients.** For non-monic $f$, multiply the candidate by $\operatorname{lc}(F)$ before reducing modulo $p^k$, and take the primitive part afterwards. Without this, the candidate is not an integer polynomial of small height.
- **Symmetric remainders.** Reduce modulo $p^k$ into $(-p^k/2, p^k/2]$, not into $[0, p^k)$; otherwise negative coefficients of true factors are not recovered.
- **Exponential blowup.** Do not use the plain subset search when $r$ can be large; the cost doubles with each extra modular factor.

## Implementations

## History

Zassenhaus (1969) proposed factoring over $\mathbb{Z}$ by Hensel lifting a factorization modulo a prime, which became practical with Berlekamp's algorithm (1967) for the modular step; the combination is often called the Berlekamp-Zassenhaus algorithm. Lenstra, Lenstra and Lovász (1982) gave the first polynomial-time algorithm by replacing the subset search with lattice reduction, and van Hoeij (2002) gave the lattice-based recombination used in current systems. Von zur Gathen and Gerhard, Chapter 15, present the algorithm with the factor bound and the test used here.

## References
