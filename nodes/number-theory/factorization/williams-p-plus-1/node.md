---
tag: XKCQGC
kind: algorithm
slug: williams-p-plus-1
name: Williams' p+1 algorithm
aliases:
- Williams p+1
area: number-theory/factorization
level: advanced
summary: Computes g = gcd(V_M(A) - 2, N) for a Lucas sequence V and a smooth exponent M. It finds a prime p of N when p + 1 or p - 1, chosen by the seed A, has only small prime power factors.
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, B: the smoothness bound}
  time: {worst: O(B log log B)}
  space: {extra: O(B)}
  multiplications_mod_N: {worst: O(B)}
  bit_operations: {worst: O(B n^2 + B log log B)}
properties: {deterministic: true, recursive: false}
prereqs: [pollard-p-minus-1, legendre-symbol, smooth-number, greatest-common-divisor]
see_also: [elliptic-curve-factorization, lucas-primality-test, pollard-rho, multiplicative-order, dickman-function, integer-factorization]
sources:
  - paper: "H. C. Williams, A p + 1 method of factoring, Mathematics of Computation 39(159), 1982"
    locator: pages 225 to 234 (the method, the choice of several seeds, and the second stage)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 3.6.3, Implementing the Lucas and quadratic Frobenius tests, pages 146 to 148 (the rules V_2j = V_j^2 - 2 and V_2j+1 = V_j V_j+1 - a, and Algorithm 3.6.7, Lucas chain); Section 5.4, pages 236 to 238, for the p - 1 method that this one parallels
  - paper: "Eric Bach and Jeffrey Shallit, Factoring with cyclotomic polynomials, Mathematics of Computation 52(185), 1989"
    locator: pages 201 to 219 (the generalization to the values of cyclotomic polynomials at p)
---

Williams' $p + 1$ method is the twin of [Pollard's $p - 1$ method](/pollard-p-minus-1/). It finds a prime factor $p$ of $N$ when $p + 1$ is [smooth](/smooth-number/), so it covers primes that the $p - 1$ method misses. Instead of powers of a number modulo $N$, it computes the term $V_M(A)$ of a Lucas sequence for a seed $A$ and a highly divisible exponent $M$, and takes $\gcd(V_M(A) - 2, N)$. With seed $A$ the method uses $p + 1$ when $A^2 - 4$ is a non-residue modulo $p$ and $p - 1$ otherwise, so in practice one runs it with three or four seeds.

## In plain words

The $p - 1$ method works because, modulo a prime $p$, raising a number to a power that is a multiple of $p - 1$ gives one. It succeeds when $p - 1$ breaks into small pieces.

The $p + 1$ method uses a different sequence of numbers, defined by a simple rule from a starting value. Modulo $p$, this sequence comes back to two after $p + 1$ steps or after $p - 1$ steps, depending on the start. Which one applies cannot be seen without knowing $p$, so you try a few starting values.

To jump far ahead in the sequence, the method uses a rule that doubles the position with one multiplication. Then it compares the term at a huge, very divisible position with two, through a gcd with the number to factor. If $p + 1$ breaks into small pieces, the gcd shows $p$.

## The problem

**Input.** An integer $N \ge 3$, a smoothness bound $B \ge 1$, and a seed $A$ with $0 \le A < N$. In practice $N$ is odd, composite and free of small factors.

**Output.** A divisor $g$ of $N$. It is a proper factor when one prime of $N$ has $p - (D/p)$ dividing $M$ and another prime does not, where $D = A^2 - 4$, $(D/p)$ is the [Legendre symbol](/legendre-symbol/), and
$$M = \prod_{q \le B,\ q \text{ prime}} q^{\lfloor \log_q B \rfloor},$$
the product of the largest powers of the primes $q \le B$ that are at most $B$. A number divides $M$ exactly when all of its prime power factors are at most $B$.

**The Lucas sequence.** For a seed $A$, let $V_0 = 2$, $V_1 = A$ and $V_{j+1} = A V_j - V_{j-1}$. Write $V_j(A)$ when the seed matters. For example $V(6)$ is $2, 6, 34, 198, 1154, \dots$.

**Cost model.** On the [word RAM](/word-ram/) with $N < 2^w$, one multiplication modulo $N$ and one gcd step cost $O(1)$. For an arbitrary-precision $N$ with $n$ binary digits, a multiplication modulo $N$ costs $O(n^2)$ bit operations with schoolbook arithmetic. The list of primes up to $B$ costs $O(B \log \log B)$ word operations with the [sieve of Eratosthenes](/sieve-of-eratosthenes/).

## The algorithm

The main block runs over the primes $q \le B$ and replaces $v$ by $V_Q(v)$, where $Q$ is the largest power of $q$ that is at most $B$. Because $V_Q(V_k(A)) = V_{Qk}(A)$, at the end $v = V_M(A) \bmod N$.

```pseudo id=main
WILLIAMS-P-PLUS-1(N, B, A)                 ▷ N ≥ 3, B ≥ 1, 0 ≤ A < N; returns a divisor of N
L1  v ← A
L2  for each prime q ≤ B, in increasing order do
L3      Q ← the largest power of q with Q ≤ B
L4      v ← LUCAS-V(v, Q, N)                ▷ now v = V_(product of the powers so far)(A) mod N
L5  g ← gcd(v − 2, N)
L6  return g
```

LUCAS-V computes $V_m(v) \bmod N$ with a binary Lucas chain. It keeps the pair $(x, y) = (V_j, V_{j+1})$ and reads the binary digits of $m$ from the top. Each digit maps $j$ to $2j$ or to $2j + 1$ with the rules $V_{2j} = V_j^2 - 2$ and $V_{2j+1} = V_j V_{j+1} - v$.

```pseudo id=lucas
LUCAS-V(v, m, N)                            ▷ m ≥ 1; returns V_m(v) mod N
K1  (x, y) ← (v, v² − 2)                    ▷ (V_1, V_2), so j = 1
K2  for each binary digit b of m after the leading 1, from high to low do
K3      if b = 1 then (x, y) ← (x · y − v, y² − 2)       ▷ j ← 2j + 1
K4      else (x, y) ← (x² − 2, x · y − v)                 ▷ j ← 2j
K5  return x
```

All arithmetic is modulo $N$. Each pass of line K2 costs two multiplications, so line L4 costs about $2 \lg Q$ multiplications.

## Example

Let $N = 5959 = 59 \cdot 101$ and $B = 5$, so $M = 4 \cdot 3 \cdot 5 = 60$. Here $59 + 1 = 60$ divides $M$, but $59 - 1 = 2 \cdot 29$ and $101 \pm 1$ do not. So the $p - 1$ method fails: $2^{60} \equiv 5137 \pmod{5959}$ and $\gcd(5136, 5959) = 1$.

Take the seed $A = 6$. Then $D = 32$, and $(32/59) = (2/59) = -1$ because $59 \equiv 3 \pmod 8$; so modulo $59$ the method uses $p + 1 = 60$.

| $q$ | $Q$ | $v$ after line L4 | as a Lucas term |
|---|---|---|---|
| | | 6 | $V_1(6)$ |
| 2 | 4 | 1154 | $V_4(6)$ |
| 3 | 3 | 497 | $V_{12}(6)$ |
| 5 | 5 | 5607 | $V_{60}(6)$ |

For the first row, LUCAS-V$(6, 4, N)$ starts with $(x, y) = (6, 34)$, reads the digits $0, 0$ of $4 = 100_2$, and gives $(34, 198)$ and then $(34^2 - 2, \cdot) = (1154, \cdot)$. Line L5 gives $\gcd(5605, 5959) = 59$, since $5605 = 5 \cdot 19 \cdot 59$.

Other seeds show the other cases. With $A = 3$, $D = 5$ is a square modulo $59$, so the method uses $p - 1 = 58$, and $\gcd(V_{60}(3) - 2, N) = 1$. With $A = 5$, $D = 21$ is a square modulo $101$, the order of the root modulo $101$ divides $20$, and the gcd is $101$. With $A = 9$, both primes are found in the same run and the gcd is $N$.

## Correctness

Let $\alpha$ and $\beta$ be the roots of $t^2 - At + 1$, so $\alpha + \beta = A$, $\alpha\beta = 1$ and $V_j = \alpha^j + \beta^j$. The rules of lines K3 and K4 follow from $(\alpha^j + \beta^j)^2 = \alpha^{2j} + \beta^{2j} + 2$ and a similar product, and they keep $(x, y) = (V_j, V_{j+1})$ where $j$ is the number formed by the digits of $m$ read so far, so LUCAS-V returns $V_m$. The rule $V_Q(V_k(A)) = V_{Qk}(A)$, which holds since $\alpha^k\beta^k = 1$, shows that line L5 sees $V_M(A)$. For an odd prime $p \mid N$ with $p \nmid D$, put $\varepsilon = (D/p)$. If $\varepsilon = 1$, then $\alpha \in \mathbb F_p^*$ and $\alpha^{p-1} = 1$. If $\varepsilon = -1$, then $\alpha$ lies in $\mathbb F_{p^2}$ but not in $\mathbb F_p$, the Frobenius map sends $\alpha$ to the other root, and $\alpha^{p+1} = \alpha\beta = 1$. So if $p - \varepsilon$ divides $M$, then $\alpha^M = \beta^M = 1$ in characteristic $p$, $V_M(A) \equiv 2 \pmod p$, and $p$ divides $g$. The full proof is below.

## Complexity

- **Multiplications.** Line L4 costs $2\lceil \lg Q \rceil$ multiplications modulo $N$, at most $2 \lg B + 2$. Summed over the primes $q \le B$, this is $2 \lg M + 2\pi(B)$, and $\ln M = \psi(B) \sim B$ by the [prime number theorem](/prime-number-theorem/), so about $2B/\ln 2 \approx 2.9B$ multiplications. This is twice the cost of the $p - 1$ method with the same $B$.
- **Time.** $O(B)$ multiplications and one gcd, plus $O(B \log \log B)$ for the primes. On the word RAM this is $O(B \log \log B)$. For an arbitrary-precision $N$, it is $O(B n^2 + B \log \log B)$ bit operations.
- **Space.** $O(B)$ for the list of primes, or $O(\sqrt B)$ with a [segmented sieve](/segmented-sieve/); the Lucas chain itself needs $O(1)$ numbers.
- **Chance of success.** These bounds are proved for one run. Whether the run splits $N$ depends on the factorization of $p + 1$ or $p - 1$, which the method cannot control. For a random seed, $(D/p) = -1$ with probability close to $1/2$, so $r$ seeds miss the $p + 1$ case with probability about $2^{-r}$. Heuristically $p + 1$ is $B$-smooth with probability about $\rho(u)$ for $u = \ln p / \ln B$, where $\rho$ is the [Dickman function](/dickman-function/), as for $p - 1$.

## Properties

- **Deterministic for a fixed seed.** The output depends only on $N$, $B$ and $A$.
- **Seed-dependent group.** Modulo $p$, the root $\alpha$ lives in a cyclic group of order $p + 1$ (the norm-one elements of $\mathbb F_{p^2}$) or of order $p - 1$ (the group $\mathbb F_p^*$), selected by $(D/p)$. This is the only difference from the $p - 1$ method, and it is why a run of $p + 1$ includes, for some seeds, a run of $p - 1$.
- **No inverses.** Unlike the [elliptic curve method](/elliptic-curve-factorization/), the chain needs only multiplications and subtractions modulo $N$.
- **The gcd is monotone in $M$.** If $p \mid V_M(A) - 2$, then $p \mid V_{Mk}(A) - 2$ for every $k \ge 1$, because $\alpha^M = 1$ implies $\alpha^{Mk} = 1$. So a gcd taken after each prime, as in the driver of the implementation, can only grow.

## Variants and improvements

- **Several seeds.** Williams suggests running stage 1 with a few seeds. The seed $A$ with $A^2 - 4$ a non-residue is needed for $p + 1$, and no seed choice works for all $p$ without knowing $p$.
- **A second stage.** As for $p - 1$, a second stage allows one prime factor $q$ of $p + 1$ between $B$ and a second bound $B_2$. It uses the identity $V_{j+k} = V_j V_k - V_{j-k}$ to step through the primes $q$ with a few multiplications each (Williams 1982).
- **Shorter Lucas chains.** The binary chain uses two multiplications per binary digit. Montgomery's PRAC chains, and chains that handle several primes at once, reduce the constant.
- **Cyclotomic generalization.** Bach and Shallit show how to find $p$ when $\Phi_k(p)$ is smooth, where $\Phi_k$ is the $k$-th cyclotomic polynomial: $k = 1$ gives $p - 1$ and $k = 2$ gives $p + 1$.
- **ECM.** The [elliptic curve method](/elliptic-curve-factorization/) replaces the two fixed groups of order $p \pm 1$ with groups of many orders near $p$, one per curve, which removes the dependence on one special number.

## When to use it

Run $p + 1$ with three seeds after [trial division](/trial-division/) and [Pollard's $p - 1$](/pollard-p-minus-1/), when the factors of $N$ may have a special form, for example factors of numbers $b^k + 1$ or of Lucas numbers, where $p + 1$ often has known factors. For general $N$ it finds a factor less often than one ECM curve with the same bound, so programs such as GMP-ECM offer it as a cheap extra stage, not as the main method.

## Pitfalls

- **Only one seed.** If $(D/p) = 1$, the run is a $p - 1$ run in disguise, and a $p$ with smooth $p + 1$ is missed. In the example, the seed $3$ fails while $6$ succeeds.
- **The seeds $A = 0, 1, 2$ and $A \equiv \pm 2$.** For $A = 2$ the sequence is constant $2$, so the gcd is $N$. For $A = 0$ and $A = 1$ the sequence has period $4$ and $6$. Use $A \ge 3$, and check $\gcd(A^2 - 4, N)$ first: it can be a factor.
- **The ladder order.** In line K3 the new pair is $(V_{2j+1}, V_{2j+2})$: $x$ is updated from the old $x$ and $y$, and $y$ from the old $y$. Updating $x$ first and then using it for $y$ gives wrong values.
- **The power of $q$.** Line L3 must use the largest power of $q$ up to $B$. With $Q = q$ only, $M$ is squarefree, and a prime $p$ with $(D/p) = -1$ and $4 \mid p + 1$ is missed.
- **A gcd equal to $N$.** It means that all primes were found at the same step. Repeat with a smaller $B$, or keep the intermediate values and take a gcd after each prime.

## Implementations

## History

Hugh C. Williams published the $p + 1$ method in 1982, eight years after Pollard's $p - 1$ method of 1974 with a second stage. The Lucas sequences it uses go back to Édouard Lucas in the 1870s, who used them for primality tests of Mersenne numbers. Eric Bach and Jeffrey Shallit generalized the idea to cyclotomic polynomials in 1989. The [elliptic curve method](/elliptic-curve-factorization/) of Hendrik Lenstra (1985, published 1987) took the next step and replaced the two groups by a family of groups.

## References
