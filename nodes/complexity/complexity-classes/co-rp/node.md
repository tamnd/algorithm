---
tag: D5QS25
kind: definition
slug: co-rp
name: coRP
aliases:
- coRP
area: complexity/complexity-classes
level: advanced
summary: "The complements of the languages in RP. A coRP machine runs in polynomial time, always accepts a yes-instance and rejects a no-instance with probability at least 1/2."
prereqs: [rp, co-np, one-sided-error]
see_also: [rp, zpp, bpp, polynomial-identity-testing, miller-rabin-primality-test, freivalds-algorithm, schwartz-zippel-lemma, aks-primality-test]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 7, Randomized computation (one-sided error, coRP and polynomial identity testing)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley (1994)
    locator: Chapter 11, Randomized computation
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press (1995)
    locator: Chapter 1, Introduction (complexity classes and the Freivalds technique)
  - paper: doi:10.1007/s00037-004-0182-6
    title: Valentine Kabanets and Russell Impagliazzo, Derandomizing polynomial identity tests means proving circuit lower bounds, Computational Complexity 13(1-2), 1 to 46 (2004)
    locator: the main theorem (a deterministic identity test gives NEXP not in P/poly or the permanent without polynomial-size arithmetic circuits)
  - paper: doi:10.4007/annals.2004.160.781
    title: Manindra Agrawal, Neeraj Kayal and Nitin Saxena, PRIMES is in P, Annals of Mathematics 160(2), 781 to 793 (2004)
    locator: the main theorem
---

coRP is the class of decision problems whose complements are in [RP](/rp/): a [probabilistic Turing machine](/probabilistic-turing-machine/) decides them in polynomial time, always accepts a yes-instance, and rejects a no-instance with probability at least $1/2$. So a reject answer is always right, and only an accept answer can be wrong. The standard examples are [polynomial identity testing](/polynomial-identity-testing/) and, before 2002, primality. Whether $\mathsf{RP} = \mathsf{coRP}$ is open.

## Definition

**Model.** The machine is a probabilistic [multitape Turing machine](/multitape-turing-machine/), or equivalently a deterministic machine $M$ that reads an input $x$ and a string $r$ of coin flips and runs in time polynomial in $|x|$ for every $r$.

**Definition.** A language $L$ is in $\mathsf{coRP}$ if its complement $\overline{L}$ is in $\mathsf{RP}$. Equivalently, there are a polynomial $p$ and a machine $M$ as above such that, with $r$ uniform on $\{0,1\}^{p(|x|)}$, for every input $x$:

$$x \in L \Rightarrow \Pr_r[M(x, r) = 1] = 1, \qquad x \notin L \Rightarrow \Pr_r[M(x, r) = 1] \le 1/2.$$

To get this form from an RP machine for $\overline{L}$, swap its answers. The class $\mathsf{coRP}$ is the set of complements of RP languages, not the complement of the set $\mathsf{RP}$. In prose the class is written coRP, the same way as [coNP](/co-np/).

**Amplification.** Run $M$ for $k$ times with independent coins and accept only if every run accepts. A yes-instance is still always accepted, and a no-instance is accepted with probability at most $2^{-k}$. The same holds if the rejection probability on no-instances is only $1/q(|x|)$ for a polynomial $q$, with $k = q(n)\, s(n)$ runs for error $e^{-s(n)}$. See [error amplification](/error-amplification/).

**Basic properties.** Each property is the mirror of a property of RP.

- $\mathsf{P} \subseteq \mathsf{coRP} \subseteq \mathsf{coNP}$. For a no-instance, a coin string $r$ with $M(x, r) = 0$ is a short certificate that $x \notin L$.
- $\mathsf{coRP} \subseteq \mathsf{BPP}$.
- $\mathsf{RP} \cap \mathsf{coRP} = \mathsf{ZPP}$. If a language has both machines, run them in turn until the RP machine accepts (then the answer is yes) or the coRP machine rejects (then the answer is no). Each round ends the loop with probability at least $1/2$, so the expected number of rounds is at most $2$ and the answer is never wrong. The full proof is on the page of [ZPP](/zpp/).
- coRP is closed under union, intersection and polynomial-time many-one reductions. It is not known to be closed under complement.

## Examples and non-examples

**Polynomial identity testing.** The input is an arithmetic circuit $C$ with integer constants and inputs $x_1, \ldots, x_n$, and the question is whether $C$ computes the zero polynomial. A circuit of size $s$ computes a polynomial of degree at most $2^s$, and repeated squaring can make its values have a number of bits exponential in $s$. So the test picks each $x_i$ uniformly from $\{1, \ldots, 4 \cdot 2^s\}$, picks a random modulus $m$ of polynomial bit length, and evaluates $C$ modulo $m$. If $C$ is the zero polynomial, every evaluation gives $0$, so the test accepts. If not, the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) gives a nonzero integer value with probability at least $3/4$, and a random modulus of the right size does not divide that value with probability at least an inverse polynomial. So the language of zero circuits is in coRP. No deterministic polynomial-time algorithm is known. Kabanets and Impagliazzo (2004) showed that one would imply a circuit lower bound that is also not known: either NEXP is not in P/poly, or the permanent has no arithmetic circuits of polynomial size. For a formula given as a list of monomials the problem is easy, so the hard case is a compact circuit. See [polynomial identity testing](/polynomial-identity-testing/).

**Primality.** The language PRIMES is in coRP by the [Miller-Rabin test](/miller-rabin-primality-test/). Write $n - 1 = 2^s d$ with $d$ odd. A base $a$ is a strong liar for $n$ if $a^d \equiv 1$ or $a^{2^j d} \equiv -1 \pmod n$ for some $0 \le j < s$. Every base is a strong liar for a prime, so the test never rejects a prime. For every odd composite $n$, at most $1/4$ of the bases in $\{1, \ldots, n - 1\}$ are strong liars. The exact counts for some composites are:

| $n$ | factors | strong liars in $\{1, \ldots, n-1\}$ | fraction |
|---|---|---|---|
| 9 | $3^2$ | 2 of 8 | 0.25 |
| 15 | $3 \cdot 5$ | 2 of 14 | 0.143 |
| 25 | $5^2$ | 4 of 24 | 0.167 |
| 65 | $5 \cdot 13$ | 6 of 64 | 0.0938 |
| 91 | $7 \cdot 13$ | 18 of 90 | 0.2 |
| 341 | $11 \cdot 31$ | 50 of 340 | 0.147 |
| 561 | $3 \cdot 11 \cdot 17$ | 10 of 560 | 0.0179 |
| 2047 | $23 \cdot 89$ | 242 of 2046 | 0.118 |

Among the 340 odd composites below 1024, the worst fraction is $1/4$, at $n = 9$. The number 561 is a Carmichael number, so every base coprime to it passes the plain [Fermat test](/fermat-primality-test/), but only 10 bases pass the strong test. In 2002 Agrawal, Kayal and Saxena put PRIMES in P ([AKS test](/aks-primality-test/)), so this example no longer separates coRP from P.

**Matrix product checking.** Given $n \times n$ matrices $A$, $B$ and $C$, is $AB = C$? [Freivalds' algorithm](/freivalds-algorithm/) picks a random vector $v \in \{0,1\}^n$ and tests $A(Bv) = Cv$ in time $O(n^2)$. If $AB = C$ it always accepts; if not, it rejects with probability at least $1/2$. This problem is in P by matrix multiplication, so the example is about speed, not about the class.

**Non-examples.**

- *Two-sided error.* A machine that sometimes rejects a yes-instance does not give a coRP algorithm.
- *coNP-complete problems.* $\mathsf{coRP} \subseteq \mathsf{coNP}$, but no coNP-complete problem, such as the tautology problem, is known to be in coRP. If one were, then $\mathsf{coNP} = \mathsf{coRP}$ and so $\mathsf{NP} = \mathsf{RP}$.

## Related definitions

- [RP](/rp/): the error is on yes-instances instead.
- [ZPP](/zpp/) $= \mathsf{RP} \cap \mathsf{coRP}$.
- [BPP](/bpp/) contains both RP and coRP.
- [coNP](/co-np/) has the same form as coRP with "at least one coin string rejects" in place of "at least half of the coin strings reject" on the no side.
- [One-sided error](/one-sided-error/) and [Monte Carlo algorithms](/monte-carlo-algorithm/).

## References
