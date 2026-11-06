---
tag: H9NDC7
kind: concept
slug: factor-base
name: Factor base
aliases:
- factor base
- factorization base
area: number-theory/discrete-logarithm
level: advanced
summary: The fixed set of small elements, like the primes up to a bound B or the irreducible polynomials of small degree, over which index calculus and sieve methods factor numbers to collect linear relations.
prereqs: [smooth-number, prime-number]
see_also: [index-calculus, relation-collection, quadratic-sieve, dixon-random-squares, general-number-field-sieve, dickman-function, function-field-sieve, subexponential-time]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 3, Section 3.2.5 (the factor base of the random square methods), Section 3.2.6 (the factor base of the quadratic sieve, with -1 and the primes with Legendre symbol 1), Section 3.6.5 (Algorithm 3.68 and Examples 3.69 and 3.70)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 15, Sections 15.1 (smooth integers), 15.2 (Dixon's factor base), 15.5.1 (Exercises 15.5.6 and 15.5.7, the choice B = L_p(1/2, 1/2)), 15.5.2 (the factor base of Coppersmith, Odlyzko and Schroeppel), 15.5.3 and 15.6 (factor bases of polynomials and of divisors)
  - paper: "Carl Pomerance, A tale of two sieves, Notices of the American Mathematical Society 43(12), 1996"
    locator: pages 1473 to 1485 (the balance between the size of the factor base and the chance of smoothness)
---

A factor base is a fixed set of "small" elements, such as the primes up to a bound $B$, over which the index calculus and sieve algorithms try to factor many group elements or integers. Each element that factors completely over the base, a [smooth](/smooth-number/) element, gives a linear relation among the logarithms or the exponent vectors of the base elements, and once there are a few more relations than base elements, linear algebra finishes the job. The size of the base is the central tuning parameter: a larger base makes smooth elements more common but needs more relations and a larger linear system. Balancing the two gives the subexponential running times $L[1/2, c]$ and, with two factor bases, $L[1/3, c]$.

## In plain words

Think of a small toolbox of building blocks, for example all prime numbers below one thousand. Many numbers can be built by multiplying blocks from this box, and many cannot. The methods that use a factor base test lots of numbers, keep the ones that can be built from the box, and write down how each was built.

Each such record is one equation. When you have a few more equations than blocks, you can combine them to learn something about every block, and then about the number you really care about.

A bigger box means more numbers can be built, so equations come faster, but you need more of them and they take longer to combine. A smaller box means fewer equations to combine but long waits for each one. The best size sits in between.

## The idea

**Definition.** In a group $G$ (or a ring), a factor base is a finite set $\mathcal{B} = \{b_1, \dots, b_s\} \subseteq G$ such that a noticeable fraction of the elements met by the algorithm can be written as $\prod b_i^{e_i}$, and such that this decomposition is easy to find when it exists. An element with such a decomposition is $\mathcal{B}$-smooth. In $(\mathbb{Z}/p\mathbb{Z})^*$ the standard choice is the primes up to $B$, with elements represented by integers in $[1, p - 1]$ and smoothness tested by [trial division](/trial-division/) or by sieving.

**Relations.** In [index calculus](/index-calculus/) for a generator $g$ of order $n$, a smooth power gives

$$g^k = \prod_i b_i^{e_i} \quad\Longrightarrow\quad k \equiv \sum_i e_i \log_g b_i \pmod n,$$

a linear equation in the unknown logarithms of the base elements. In the factoring methods, such as [Dixon's](/dixon-random-squares/) and the [quadratic sieve](/quadratic-sieve/), the relations are $x^2 \equiv \prod b_i^{e_i} \pmod N$, and linear algebra over $\mathbb{F}_2$ finds a [congruence of squares](/congruence-of-squares/). In both cases the base elements are the unknowns of the linear system, so about $s$ relations are needed. See [relation collection](/relation-collection/).

**The balance.** Let elements be integers of size about $p$, take the base to be the primes up to $B$, and let $u = \ln p / \ln B$. Then $s = \pi(B) \approx B / \ln B$, and a random integer below $p$ is $B$-smooth with probability about $u^{-u}$ (the [Dickman function](/dickman-function/) estimate, $\rho(u) = u^{-u(1 + o(1))}$ in the range that matters). Collecting $s$ relations needs about $s \, u^u$ trials. With the bound

$$B = L_p[1/2, c] = \exp\big((c + o(1)) (\ln p)^{1/2} (\ln \ln p)^{1/2}\big),$$

one finds $u^u = L_p[1/2, 1/(2c)]$. So:

- with trial division, each trial costs about $s$ divisions, the relations cost $s^2 u^u = L_p[1/2, 2c + 1/(2c)]$, and the minimum is at $c = 1/2$, giving $L_p[1/2, 2]$ (Galbraith, Exercise 15.5.7);
- with a smoothness test of cost $L_p[1/2, o(1)]$ per trial, the relations cost $L_p[1/2, c + 1/(2c)]$ and sparse linear algebra costs $s^{2 + o(1)} = L_p[1/2, 2c]$; at $c = 1/\sqrt 2$ both are $L_p[1/2, \sqrt 2]$.

Faster methods make the elements to be factored smaller, so that smoothness is more likely for the same base. The sieve of Coppersmith, Odlyzko and Schroeppel factors numbers of size about $p^{1/2}$ and reaches $L_p[1/2, 1]$. The number field sieve and the function field sieve factor numbers of size $L[2/3]$ over two factor bases, one on each side of a commutative diagram of rings, and reach $L[1/3, c]$.

**Extra members.** A factor base often contains elements besides small primes: $-1$ when the numbers to be factored can be negative, the prime ideals of small norm in a number ring, the leading coefficient of a defining polynomial, or a few large elements chosen to make relations easier.

## Examples

- **Discrete logarithm modulo $229$.** HAC's Example 3.69 takes $p = 229$, $g = 6$ and the base $\{2, 3, 5, 7, 11\}$. Six smooth powers, such as $6^{100} \equiv 180 = 2^2 \cdot 3^2 \cdot 5$ and $6^{18} \equiv 176 = 2^4 \cdot 11$, give six equations modulo $228$, whose solution is $\log_6 2 = 21$, $\log_6 3 = 208$, $\log_6 5 = 98$, $\log_6 7 = 107$ and $\log_6 11 = 162$. Then $13 \cdot 6^{77} \equiv 147 = 3 \cdot 7^2$ gives $\log_6 13 = 208 + 2 \cdot 107 - 77 \bmod 228 = 117$.
- **A subgroup of prime order.** Galbraith's Example 15.5.4 takes $p = 223$, $g = 15$ of prime order $37$, and the base $\{2, 3, 5, 7\}$. The base primes do not lie in $\langle g \rangle$; the method multiplies by elements of the complementary subgroup of order $6$ and works modulo $37$.
- **Polynomials over $\mathbb{F}_2$.** In $\mathbb{F}_{2^7} = \mathbb{F}_2[x]/(x^7 + x + 1)$, HAC's Example 3.70 uses the irreducible polynomials of degree at most $3$: $\{x, x + 1, x^2 + x + 1, x^3 + x + 1, x^3 + x^2 + 1\}$. A polynomial of degree $m$ is smooth with respect to degree $b$ with probability about $u^{-u}$ for $u = m/b$, as for integers.
- **Quadratic sieve.** The base is $-1$ and the primes $q \le B$ with Legendre symbol $(N/q) = 1$, since only these can divide $x^2 - N$ (HAC, Section 3.2.6).
- **Number field sieve.** One base is the rational primes up to $B$; the other is the prime ideals of norm up to $B$ in $\mathbb{Z}[\theta]$, for a root $\theta$ of the chosen polynomial.
- **Curves.** For the Jacobian of a hyperelliptic curve over $\mathbb{F}_q$, the base is the prime divisors of degree one, that is, the points of the curve; for an elliptic curve over $\mathbb{F}_{q^n}$, Gaudry and Diem use the points whose $x$-coordinate lies in $\mathbb{F}_q$. No good factor base is known for elliptic curves over prime fields, which is why [index calculus](/index-calculus/) does not apply to them.

## Where it is used

- **Discrete logarithms in finite fields.** [Index calculus](/index-calculus/), [Coppersmith's algorithm](/coppersmith-discrete-logarithm/), the [function field sieve](/function-field-sieve/), the [number field sieve for discrete logarithms](/number-field-sieve-discrete-logarithm/) and the [quasi-polynomial algorithms](/quasi-polynomial-discrete-logarithm/).
- **Factoring.** [Dixon's random squares](/dixon-random-squares/), the [quadratic sieve](/quadratic-sieve/) and the [general number field sieve](/general-number-field-sieve/).
- **Curves.** Index calculus in Jacobians of hyperelliptic curves of large genus, the [summation polynomial](/semaev-summation-polynomial-index-calculus/) method for elliptic curves over extension fields, and the [Weil descent](/weil-descent-attack/) attack, which moves an elliptic curve problem to a Jacobian where a factor base exists.
- **Class groups.** Computations of class groups and regulators of number fields collect relations among prime ideals of small norm in the same way.

## References
