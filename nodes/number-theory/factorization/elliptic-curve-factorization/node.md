---
tag: FMGN8V
kind: algorithm
slug: elliptic-curve-factorization
name: Elliptic curve factorization method
aliases:
- ECM
- Lenstra elliptic curve method
area: number-theory/factorization
level: advanced
summary: Lenstra's method computes [k]P on random elliptic curves mod N and finds a prime factor p when a point order mod p is smooth. Its cost depends on p, about L_p[1/2, 2^(1/2)] heuristically.
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, p: the smallest prime factor of N, B: the stage one bound B_1, D: the stage two bound B_2, C: the number of curves, G: the largest gap between consecutive primes in the stage two range}
  time: {worst: O(C (B + D/log D + G) n^2 + D log log D), heuristic: exp((2^(1/2) + o(1)) (ln p ln ln p)^(1/2)) n^2}
  space: {extra: O((G + D/log D) n)}
  point_additions: {worst: O(C (B + D/log D + G))}
properties: {deterministic: false, recursive: false}
prereqs: [pollard-p-minus-1, elliptic-curve-cryptography, extended-euclidean-algorithm, smooth-number]
see_also: [pollard-p-minus-1, williams-p-plus-1, pollard-rho, quadratic-sieve, general-number-field-sieve, ecpp, dickman-function, integer-factorization]
sources:
  - paper: "H. W. Lenstra, Jr., Factoring integers with elliptic curves, Annals of Mathematics 126(3), 1987"
    locator: pages 649 to 673 (the method, its analysis, and the bound conditional on smooth numbers in short intervals)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 7.3, Theorem 7.3.2, pages 334 to 335 (Lenstra's bound on curve orders in a set); Section 7.4.1, Definition 7.4.1 and Algorithm 7.4.2, pages 336 to 337; the heuristic complexity, pages 338 to 339; Section 7.4.2, Optimization of ECM, pages 339 to 347 (stage two, Montgomery curves, Suyama's observation, the F15 factor)
  - paper: "Peter L. Montgomery, Speeding the Pollard and elliptic curve methods of factorization, Mathematics of Computation 48(177), 1987"
    locator: pages 243 to 264 (curves By^2 = x^3 + Ax^2 + x, arithmetic without y, and the second stage)
---

The elliptic curve method, ECM, of Hendrik Lenstra finds a prime factor $p$ of an integer $N$ by computing a multiple $[k]P$ of a point $P$ on a random elliptic curve modulo $N$, where $k$ is the product of all prime powers up to a bound $B_1$. The point addition needs inverses modulo $N$, and when the order of $P$ modulo $p$ divides $k$ but its order modulo another prime factor does not, some inverse fails and the gcd of the bad denominator with $N$ is a proper factor. It is [Pollard's $p - 1$ method](/pollard-p-minus-1/) with the fixed group $(\mathbb{Z}/p\mathbb{Z})^\times$ of order $p - 1$ replaced by a curve group of order near $p$ that changes with each curve, so a bad $p$ is no obstacle: one tries another curve. The heuristic cost is $L_p[1/2, \sqrt 2]$ operations modulo $N$, which depends on the size of $p$ and only weakly on $N$, so ECM is the method of choice for factors of moderate size of very large numbers.

## In plain words

On a curve of a fixed kind, two points can be added to give a third, by a rule that needs one division. Work with remainders modulo the number to factor. Then a division can fail, and this failure is good news: the number we tried to divide by shares a factor with the number to factor, and one gcd shows it.

Choose a random curve and a point on it. Add the point to itself many times, a count made of all small primes. For one hidden prime factor, the points of the curve form a group whose size is near that factor. If this size has only small primes in it, the count lands on a multiple of the size, and a division fails. If not, choose a new curve. Each curve gives a new size, so sooner or later one has only small primes.

## The problem

**Input.** An integer $N > 1$ with $\gcd(N, 6) = 1$ that is not a prime power, bounds $2 \le B_1 \le B_2$, and a number $C$ of curves. The work also uses a source of random numbers.

**Output.** A proper factor $g$ of $N$ (with $1 < g < N$), or $1$ if no curve finds one. A prime $N$ always gives $1$.

**Curves modulo $N$.** For $a, b \in \mathbb{Z}/N\mathbb{Z}$ with $\gcd(4a^3 + 27b^2, N) = 1$, the curve $E_{a,b}$ is $y^2 = x^3 + ax + b$, and its points modulo $N$ are the pairs $(x, y)$ that satisfy the equation modulo $N$, with one more point $O$. Crandall and Pomerance call it a pseudocurve. Points are added by the chord and tangent rules of [elliptic curve](/elliptic-curve-cryptography/) groups, with $O$ as zero and $-(x, y) = (x, -y)$. For $P_1 = (x_1, y_1)$ and $P_2 = (x_2, y_2)$:

- if $x_1 \not\equiv x_2$, then $\lambda = (y_2 - y_1)(x_2 - x_1)^{-1}$;
- if $x_1 \equiv x_2$ and $y_1 + y_2 \equiv 0$, then $P_1 + P_2 = O$;
- otherwise $\lambda = (3x_1^2 + a)(y_1 + y_2)^{-1}$, the tangent slope, as $y_1 \equiv y_2$ in this case for every prime factor;

and then $x_3 = \lambda^2 - x_1 - x_2$, $y_3 = \lambda(x_1 - x_3) - y_1$, all modulo $N$. For a prime $N$ this is the usual group $E(\mathbb{F}_p)$. For composite $N$ the points modulo $N$ do not form a group: an inverse may not exist, and then the sum is undefined. ECM is built on this failure. The order of $E(\mathbb{F}_p)$ lies in $(p + 1 - 2\sqrt p,\ p + 1 + 2\sqrt p)$ by Hasse's theorem.

**Cost model.** A point addition costs $O(1)$ multiplications and one inverse modulo $N$, each $O(n^2)$ bit operations for an $N$ of $n$ binary digits with schoolbook arithmetic, or $O(1)$ word operations when $N < 2^w$ on the [word RAM](/word-ram/). The bound for given $B_1$, $B_2$ and $C$ is proved. The subexponential bound is a heuristic, and is a theorem of Lenstra under one assumption on smooth numbers in short intervals.

## The algorithm

Let $k = \prod_{q \le B_1} q^{e_q}$, where $q$ runs over the primes and $q^{e_q} \le B_1 < q^{e_q + 1}$, and let $q_1 < q_2 < \dots$ be the primes in $(B_1, B_2]$.

```pseudo id=main
ECM(N, B1, B2, C)                ▷ gcd(N, 6) = 1, N not a prime power; returns a proper factor of N or 1
L1  repeat C times
L2      choose x, y, a at random in [0, N); b ← (y² − x³ − ax) mod N; g ← gcd(4a³ + 27b², N)
L3      if g = N then go to the next curve; if g > 1 then return g
L4      Q ← [k](x, y), one prime q ≤ B1 at a time, e_q times each; if Q = O then go to the next curve
L5      stage two: R ← [q_1]Q, then R ← R + [q_(i+1) − q_i]Q for i = 1, 2, …, with a table of the [2j]Q, until R = O or the primes end
L6      on a failed inverse of d in any addition of L4 or L5: g ← gcd(d, N); if g < N then return g, else go to the next curve
L7  return 1
```

Line L2 makes a random curve through a random point, so no square root modulo $N$ is needed. Line L3 rejects a singular curve, and a discriminant with a common factor is already a success. Line L4 is stage one: it multiplies the point by each prime power, using double and add. If $Q$ becomes $O$ modulo $N$, the order of the point divides $k$ modulo every prime factor at once, and the curve is useless. Line L5 is stage two: it catches a point whose order modulo $p$ is a divisor of $k$ times one prime $q \in (B_1, B_2]$. It steps from $[q_i]Q$ to $[q_{i+1}]Q$ with one addition of a stored point $[q_{i+1} - q_i]Q$; the gaps are even, so the table needs only $[2]Q, [4]Q, \dots, [G]Q$. Line L6 is the exit for a failed inverse: the denominator $d$ has $\gcd(d, N) > 1$, and since $d \not\equiv 0 \pmod N$ in both cases of the rule that divide, the gcd is a proper factor. The test $g < N$ is a safeguard.

## Example

Let $N = 2290741 = 1129 \cdot 2029$, $B_1 = 20$, and take the curve $y^2 = x^3 + x - 1$ through $P = (2, 3)$, so $a = 1$ and $b = 9 - 8 - 2 = -1$. The discriminant term is $4 + 27 = 31$, and $\gcd(31, N) = 1$. Here $k = 2^4 \cdot 3^2 \cdot 5 \cdot 7 \cdot 11 \cdot 13 \cdot 17 \cdot 19$.

Hidden from the algorithm, $\#E(\mathbb{F}_{1129}) = 1120 = 2^5 \cdot 5 \cdot 7$, and $P$ has order $560 = 2^4 \cdot 5 \cdot 7$ modulo $1129$, which divides $k$. Modulo $2029$ the group has the prime order $2083$, so $P$ has order $2083$ there, which does not divide $k$.

| step | multiplier so far | point modulo $N$ |
|---|---|---|
| start | $1$ | $(2, 3)$ |
| $\times 2$ four times | $16$ | $(929285, 1878321)$ |
| $\times 3$ twice | $144$ | $(2283801, 421186)$ |
| $\times 5$ | $720$ | $Q = (1115156, 449422)$ |
| $\times 7$ | fails | |

Modulo $1129$, the point $Q$ has order $560/80 = 7$. To compute $[7]Q$, double and add forms $[2]Q$, $[3]Q$ and $[6]Q = (2200125, 2229695)$, and then needs $[6]Q + Q$. Modulo $1129$, $[6]Q = -Q$, so the two $x$ coordinates agree modulo $1129$ but not modulo $2029$. The slope needs the inverse of $x_Q - x_{[6]Q} \equiv 1205772 \pmod N$, and $\gcd(1205772, 2290741) = 1129$. So $N = 1129 \cdot 2029$.

With Pollard's $p - 1$ method and the same bound $20$, neither factor would be found: $1128 = 2^3 \cdot 3 \cdot 47$ and $2028 = 2^2 \cdot 3 \cdot 13^2$.

## Correctness

The output is a proper factor or $1$ by inspection: line L3 returns $g = \gcd(4a^3 + 27b^2, N)$ only if $1 < g < N$, and line L6 returns $g = \gcd(d, N)$ only if $1 < g < N$. The real content is why failures happen. Let $p$ be a prime factor of $N$. As long as every inverse exists, the computed points reduce modulo $p$ to the true multiples in the group $E(\mathbb{F}_p)$, because each case of the rule above modulo $N$ is the same case modulo $p$. A point $(x, y)$ modulo $N$ never reduces to $O$ modulo $p$. So if the order of $P$ modulo $p$ divides a multiplier that the algorithm computes, then some inverse fails before the end, or the result is $O$ modulo $N$. Since the cases are decided modulo $N$, a failed denominator is never $0$ modulo $N$, so every failure gives $1 < g < N$. Termination is clear: $C$ curves, each with finitely many additions. The full proof is below.

## Complexity

- **Per curve, proved.** Stage one multiplies by $\sum_q e_q$ primes, with at most $2\log_2 q$ additions for each, so about $2\log_2 k \approx 2.9 B_1$ additions, since $\ln k \approx B_1$. Stage two costs $G/2$ additions for the table and one addition per prime in $(B_1, B_2]$, about $B_2/\ln B_2$. Each addition costs $O(n^2)$ bit operations. Making the primes up to $B_2$ costs $O(B_2 \log \log B_2)$ once.
- **Success chance per curve.** By Lenstra's Theorem 7.3.2 in Crandall and Pomerance, the order of a random curve modulo $p$ is spread over the Hasse interval nearly as a random integer is, up to a factor $1/\ln p$. So the chance of success is about the chance $\rho(u)$ that a random number near $p$ is $B_1$ smooth, where $u = \ln p / \ln B_1$ and $\rho$ is the [Dickman function](/dickman-function/).
- **Heuristic total.** Minimizing $B_1/\text{prob}(B_1)$ gives $B_1 = \exp((\sqrt 2/2 + o(1))\sqrt{\ln p \ln \ln p})$ and an expected $L_p[1/2, \sqrt 2] = \exp((\sqrt 2 + o(1))\sqrt{\ln p \ln \ln p})$ operations modulo $N$ to find $p$. Lenstra proved this bound under the one assumption that numbers in the Hasse interval are smooth as often as random numbers of their size.
- **Worst case.** For $N$ a product of two primes near $\sqrt N$, this becomes $L_N[1/2, 1]$, the same as the [quadratic sieve](/quadratic-sieve/), but the sieve uses cheaper steps and wins in practice.
- **Space.** $O(1)$ points in stage one, and $O(G)$ points plus the list of primes in stage two.

## Properties

- **Depends on the smallest factor.** The cost is set by $p$, not by $N$; the size of $N$ enters only through the cost of arithmetic modulo $N$.
- **Many groups.** Each curve gives a new group order in the Hasse interval, unlike the single order $p - 1$ of the $p - 1$ method or $p + 1$ of the [$p + 1$ method](/williams-p-plus-1/).
- **Randomized, with large variance.** One success is enough, and its time varies a lot from run to run.
- **Parallel.** Curves are independent, so many machines can run different curves with no communication.
- **Small memory.** Stage one keeps $O(1)$ numbers modulo $N$.

## Variants and improvements

- **Projective and Montgomery coordinates.** Peter Montgomery's curves $By^2 = x^3 + Ax^2 + x$ allow the multiple $[k]P$ to be computed from $x$ and $z$ coordinates only, with no inverses, by a ladder; one gcd at the end of each stage replaces all the inverses. This is the form used in practice (Crandall and Pomerance, Algorithm 7.4.4).
- **Curves with known torsion.** Suyama's family of Montgomery curves has group orders divisible by $12$, which makes the order more likely to be smooth (Crandall and Pomerance, Theorem 7.4.3).
- **Faster stage two.** Baby step giant step pairings and fast polynomial arithmetic, due to Montgomery, cut stage two to a few multiplications per prime, and allow $B_2$ about $100$ times $B_1$.
- **Edwards curves.** Later work uses twisted Edwards curves, whose addition is cheaper still.
- **Primality proving.** The same curve arithmetic underlies [ECPP](/ecpp/).

## When to use it

Use ECM after [trial division](/trial-division/) and [Pollard's rho](/pollard-rho/), to find factors of medium size, roughly 15 to 40 digits, of any $N$, and especially of numbers far too large for the [quadratic sieve](/quadratic-sieve/) or the [number field sieve](/general-number-field-sieve/). Run it with growing $B_1$ before starting a sieve, since a sieve cannot exploit a small factor. For $N$ a product of two primes of equal size, use a sieve instead. First check that $N$ is not prime and not a perfect power; ECM cannot split a prime power, since all its prime factors are equal.

## Pitfalls

- **Prime powers.** For $N = p^e$, every failure has $\gcd(d, N)$ a power of $p$, which is a factor, but the analysis above is for distinct primes and the method is wasteful there. Detect perfect powers with integer roots first.
- **Factors $2$ and $3$.** The short form $y^2 = x^3 + ax + b$ needs $\gcd(N, 6) = 1$. Remove $2$ and $3$ first.
- **The tangent denominator.** Invert $y_1 + y_2$ in the tangent case, not $2y_1$. When $x_1 \equiv x_2$ modulo $N$ but $y_1 \equiv -y_2$ only modulo one prime $p$, the sum is $O$ modulo $p$, and $y_1 + y_2$ then shares the factor $p$ with $N$, while $2y_1$ may be invertible and give a wrong point, so the factor is lost.
- **All primes at once.** If $B_1$ is large compared with the prime factors, the orders modulo all primes divide $k$, and the result is $O$ modulo $N$. Then retry with a smaller $B_1$ or a new curve; one gcd after each prime, as here, makes this rare.
- **Random curve, random point.** Choosing $a$ and $b$ first and then a point needs a square root modulo $N$, which is as hard as factoring. Choose the point first and solve for $b$.

## Implementations

## History

Hendrik Lenstra found the method in 1985, and published it in the Annals of Mathematics in 1987. In the same year Peter Montgomery gave the curves and the inversion free arithmetic still in use, and a fast second stage. ECM has found many factors of Fermat and Mersenne numbers; for example, Richard Crandall and C. van Halewyn found a 33 digit factor of $F_{15}$ in 1997 with $B_1 = 10^7$ (Crandall and Pomerance).

## References
