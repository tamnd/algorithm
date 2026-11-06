---
tag: 8TFPRS
kind: algorithm
slug: fermat-primality-test
name: Fermat primality test
aliases:
- Fermat test
area: number-theory/primality
level: intro
summary: Randomized test that checks a^(n-1) ≡ 1 (mod n) for random bases a; a failed check proves n composite, but Carmichael numbers pass for every base coprime to n.
solves: [primality-testing]
model: multitape-turing-machine
complexity:
  vars: {n: the number tested, k: the number of rounds}
  time: {worst: O(k (log n)^3), best: O(1)}
  space: {extra: O(log n)}
properties: {deterministic: false, recursive: false, certifying: false}
history:
  year: 1640
  people: [Pierre de Fermat]
  note: The test uses the converse of Fermat's little theorem, which Fermat stated in a letter of 1640. The bounds on its error are from the 1970s and 1980s.
prereqs: [fermat-little-theorem, modular-exponentiation, binary-exponentiation, prime-number]
see_also: [fermat-pseudoprime, carmichael-number, miller-rabin, solovay-strassen, baillie-psw, compositeness-witness, probable-prime, one-sided-error]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.8, Primality testing (pseudoprimality testing with the procedure PSEUDOPRIME, and Carmichael numbers)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 3.4, Pseudoprimes (3.4.1 Fermat pseudoprimes, 3.4.2 Carmichael numbers)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.4, Factoring into primes (the Fermat test as a first check for primality)
  - paper: doi:10.1016/0304-3975(80)90007-9
    title: Louis Monier, Evaluation and comparison of two efficient probabilistic primality testing algorithms, Theoretical Computer Science 12 (1980)
    locator: pages 97 to 108 (the number of bases for which a composite number passes the Fermat test)
  - paper: doi:10.1090/S0025-5718-1980-0583518-6
    title: Robert Baillie and Samuel S. Wagstaff Jr., Lucas pseudoprimes, Mathematics of Computation 35 (1980)
    locator: pages 1391 to 1417 (Section 1, the count of bases to which n is a pseudoprime)
---

The Fermat primality test decides whether an integer $n$ is probably [prime](/prime-number/) by checking the congruence $a^{n-1} \equiv 1 \pmod n$ of [Fermat's little theorem](/fermat-little-theorem/) for a few random bases $a$. If one base fails the congruence, $n$ is certainly composite and the base is a [compositeness witness](/compositeness-witness/). If all bases pass, $n$ is a [probable prime](/probable-prime/): the answer can be wrong, but only on the side of "prime". For most composite numbers each round catches the error with probability more than $1/2$, but the [Carmichael numbers](/carmichael-number/) pass for every base coprime to $n$, so the test has no error bound that holds for all inputs. [Miller-Rabin](/miller-rabin/) repairs this flaw at the same cost.

## In plain words

For a prime number, a certain remainder computation always gives one, whatever base you start from. So pick a random base, compute that remainder for your number, and look at the result. If it is not one, your number cannot be prime, and the base is a proof of that. If it is one, the number may be prime, so you try more random bases. Each base that passes makes you more confident.

The weak point is a small family of composite numbers that give one for almost every base. A number from this family passes nearly every round, so more rounds do not help. For random numbers this almost never happens, but an adversary can choose such a number on purpose.

## The problem

The input is an integer $n \ge 0$ and a number of rounds $k \ge 1$. The output is false, which means "$n$ is not prime", or true, which means "$n$ is probably prime". This is a [Monte Carlo](/monte-carlo-algorithm/) solution of the [primality testing](/primality-testing/) problem with [one-sided error](/one-sided-error/): the answer false is always right, and the answer true is right for each prime $n$.

**Cost model.** The integers are of arbitrary precision. Let $\ell = \lfloor \lg n \rfloor + 1$ be the number of binary digits of $n$, so $\ell = \Theta(\log n)$. Costs are in bit operations, as on a [multitape Turing machine](/multitape-turing-machine/), and $M(\ell)$ is the cost of one product of two $\ell$-digit integers: $O(\ell^2)$ for [schoolbook multiplication](/schoolbook-multiplication/), $O(\ell \log \ell)$ for [Harvey and van der Hoeven](/harvey-van-der-hoeven-multiplication/). When $n$ fits in a machine word of $w$ binary digits and a product modulo $n$ costs one step, the [word RAM](/word-ram/) bounds are given too.

## The algorithm

A base $a$ with $\gcd(a, n) = 1$ and $a^{n-1} \not\equiv 1 \pmod n$ is a *Fermat witness* for $n$. A base $a$ with $a^{n-1} \equiv 1 \pmod n$ for a composite $n$ is a *Fermat liar*, and $n$ is then a [Fermat pseudoprime](/fermat-pseudoprime/) to the base $a$. A base that shares a factor with $n$ also fails the congruence, so it proves $n$ composite as well.

```pseudo id=main
FERMAT-PRIMALITY-TEST(n, k)                ▷ true means "probably prime"
L1  if n < 4 then return n ≥ 2              ▷ 0 and 1 are not prime; 2 and 3 are prime
L2  if n is even then return false
L3  for i ← 1 to k do
L4      a ← a uniform random integer in [2, n − 2]
L5      if a^(n−1) mod n ≠ 1 then return false    ▷ a proves n composite
L6  return true
```

Lines L1 and L2 handle the small and the even inputs, so the loop runs only for odd $n \ge 5$, where the range $[2, n-2]$ is not empty. The bases $1$ and $n - 1$ are left out: $1^{n-1} = 1$, and $(n-1)^{n-1} \equiv (-1)^{n-1} = 1$ for odd $n$, so these two bases pass for every odd $n$ and test nothing. Line L5 computes the power by [binary exponentiation](/binary-exponentiation/), with a reduction modulo $n$ after each product. The rounds are independent, so a run of $k$ rounds is the same as $k$ runs of one round.

## Example

Test $n = 341 = 11 \cdot 31$. The exponent is $n - 1 = 340 = 101010100_2$.

With the base $a = 2$: $2^{10} = 1024 = 3 \cdot 341 + 1$, so $2^{10} \equiv 1$ and $2^{340} = (2^{10})^{34} \equiv 1 \pmod{341}$. The base 2 is a liar, and 341 is the smallest Fermat pseudoprime to the base 2.

With the base $a = 3$, the left-to-right binary method reads the digits of $340$ from the top. At each digit it squares the running value, and for a digit 1 it also multiplies by 3. All values are modulo 341.

| digit | after squaring | after multiplying | power of 3 |
|---|---|---|---|
| 1 | $1$ | $3$ | $3^{1}$ |
| 0 | $9$ | $9$ | $3^{2}$ |
| 1 | $81$ | $243$ | $3^{5}$ |
| 0 | $56$ | $56$ | $3^{10}$ |
| 1 | $67$ | $201$ | $3^{21}$ |
| 0 | $163$ | $163$ | $3^{42}$ |
| 1 | $312$ | $254$ | $3^{85}$ |
| 0 | $67$ | $67$ | $3^{170}$ |
| 0 | $56$ | $56$ | $3^{340}$ |

So $3^{340} \equiv 56 \not\equiv 1 \pmod{341}$, line L5 returns false, and 3 is a Fermat witness. Of the 300 bases in $[1, 340]$ that are coprime to 341, exactly 100 are liars, so one random round from line L4 misses with probability $98/338 \approx 0.29$.

For the [Carmichael number](/carmichael-number/) $561 = 3 \cdot 11 \cdot 17$, every base coprime to 561 is a liar. Of the 558 bases in $[2, 559]$, 318 are liars, so a round misses with probability $318/558 \approx 0.57$, and 20 rounds still miss with probability about $1.3 \cdot 10^{-5}$. For a Carmichael number with three prime factors of about 30 decimal digits each, such as $(6t + 1)(12t + 1)(18t + 1)$ with $t = 10^{29} + 18555$, a round misses with probability more than $1 - 10^{-29}$.

## Correctness

The answer false is always right. Line L1 is right by inspection, line L2 is right because an even number above 2 is composite, and line L5 is right because a prime $n$ and a base $2 \le a \le n - 2$ give $a^{n-1} \equiv 1 \pmod n$ by Fermat's little theorem. So a prime $n$ always gets the answer true.

For an odd composite $n$, the liars that are coprime to $n$ form a subgroup of the [multiplicative group](/multiplicative-group-modulo-n/) $(\mathbb{Z}/n\mathbb{Z})^*$, since $a^{n-1} \equiv 1$ and $b^{n-1} \equiv 1$ give $(ab)^{n-1} \equiv 1$. If $n$ has at least one Fermat witness coprime to $n$, the subgroup is proper, so by [Lagrange's theorem](/lagranges-theorem-group-theory/) it holds at most half of the group. Then each round answers true with probability less than $1/2$, and $k$ rounds with probability less than $2^{-k}$. The exact number of liars for odd $n = \prod p_i^{e_i}$ is

$$\#\{a \in [1, n-1] : a^{n-1} \equiv 1 \pmod n\} = \prod_i \gcd(n - 1, p_i - 1).$$

The full proof of these claims is in the proofs.

## Complexity

**One round.** Line L5 is one [modular exponentiation](/modular-exponentiation/) with an exponent of $\ell$ binary digits. Binary exponentiation does at most $\ell - 1$ squarings and $\ell - 1$ other products, each followed by a reduction modulo $n$. With schoolbook arithmetic each step costs $O(\ell^2)$ bit operations, so a round costs $O(\ell^3) = O((\log n)^3)$. With fast multiplication and division a round costs $O(\ell \, M(\ell))$, which is $O((\log n)^2 \log \log n)$ with the Harvey and van der Hoeven bound.

**All rounds.** The worst case is a prime or a Carmichael number with large factors: all $k$ rounds run, for $O(k (\log n)^3)$ bit operations with schoolbook arithmetic. The best case is $O(1)$: $n < 4$ or $n$ even. Line L4 needs $O(\log n)$ random binary digits per round.

**Word RAM.** For $n < 2^w$ with a product modulo $n$ in $O(1)$ steps, a round costs $O(\log n)$ steps and the test costs $O(k \log n)$.

**Space.** The running power and the base need $O(\log n)$ binary digits, so the extra space is $O(\log n)$, or $O(1)$ words on the word RAM.

**Error.** The error is one-sided: only a composite $n$ can get a wrong answer, and the wrong answer is always true. For an odd composite $n$ the probability of the answer true is exactly $q^k$ with $q = (F(n) - 2)/(n - 3)$, where $F(n) = \prod_i \gcd(n - 1, p_i - 1)$ is the number of liars above. It depends only on $n$ and $k$, not on any assumption about the input. If $n$ is not a Carmichael number, then $q < 1/2$. If $n$ is a Carmichael number, then $F(n) = \varphi(n)$, and $q$ tends to 1 as the smallest prime factor of $n$ grows.

## Properties

- **Monte Carlo with one-sided error.** The answer false is a proof; the answer true is not. See [one-sided error](/one-sided-error/).
- **Not uniform in its error.** No number of rounds gives an error bound that holds for every input, because of the Carmichael numbers. This is the difference from [Miller-Rabin](/miller-rabin/), whose error is at most $4^{-k}$ on each input.
- **Certifying only for composites.** A witness $a$ is a short proof of compositeness that anyone can check with one exponentiation. A pass gives no proof of primality; for that see [primality certificates](/primality-certificate/).
- **No factor found.** A witness shows that $n$ is composite but in general gives no factor of $n$.

## Variants and improvements

- **Fixed base.** Test only the base 2. This is the deterministic test of a [probable prime](/probable-prime/) to the base 2, used as a fast filter. Below $10^5$ it accepts 78 composites, the first being 341, 561 and 645.
- **[Miller-Rabin](/miller-rabin/).** Write $n - 1 = 2^s d$ with $d$ odd and look at the whole sequence $a^d, a^{2d}, \ldots, a^{2^s d}$, not only its last term. A [nontrivial square root of 1](/nontrivial-square-root-of-one/) in the sequence also proves $n$ composite. This costs the same, and each round catches each odd composite with probability at least $3/4$.
- **[Solovay-Strassen](/solovay-strassen/).** Compare $a^{(n-1)/2}$ with the [Jacobi symbol](/jacobi-symbol/) $(a/n)$. Each round catches each odd composite with probability at least $1/2$; see [Euler-Jacobi pseudoprime](/euler-jacobi-pseudoprime/).
- **[Baillie-PSW](/baillie-psw/).** Combine the base-2 strong test with a Lucas test. No composite that passes it is known.
- **Trial division first.** Dividing by the primes up to a small bound before line L3 removes most composites more cheaply than an exponentiation.

## When to use it

Use the Fermat test with the base 2 as a cheap filter, for example when you search for a random prime and most candidates are composite, and confirm the survivors with a stronger test. Do not use it alone when the input may come from an adversary, because a Carmichael number passes. In nearly all uses [Miller-Rabin](/miller-rabin/) is better: it has the same cost and a bound on its error for every input. When you need a proof of primality, use a proving method such as [ECPP](/ecpp/) or the [AKS test](/aks-primality-test/).

## Pitfalls

- **Bases 1 and n − 1.** If line L4 draws from $[1, n-1]$, the bases $1$ and $n - 1$ always pass for odd $n$ and waste rounds. Draw from $[2, n-2]$.
- **Trusting more rounds against Carmichael numbers.** On a Carmichael number with large prime factors, almost every base is a liar, so the error does not drop like $2^{-k}$. The bound $2^{-k}$ holds only for composites that have a witness coprime to $n$.
- **Even and small inputs.** Without line L1 the range $[2, n-2]$ is empty for $n \le 3$, and without line L2 the even number 2 needs a special case. Handle $n < 4$ and even $n$ before the loop.
- **Computing the full power.** Computing $a^{n-1}$ as an integer and then reducing it needs about $n \lg a$ binary digits of memory. Reduce modulo $n$ after each product in line L5.
- **Overflow on a word.** For $n$ near $2^{64}$, a product of two residues needs 128 binary digits. Use a double-width product or a [modular multiplication](/modular-multiplication/) routine.

## Implementations

## History

Fermat stated the theorem behind the test in a letter of 1640. The use of its converse to detect composite numbers is old, and the fact that some composites pass it was known in the nineteenth century: $341 = 11 \cdot 31$ passes the base 2. Korselt gave in 1899 the criterion for a composite number to pass every coprime base, and Carmichael found the first such numbers in 1910. In 1980 Monier, and independently Baillie and Wagstaff, gave the exact number of bases for which a composite number passes. The Carmichael numbers, infinitely many by the theorem of Alford, Granville and Pomerance of 1994, are the reason that the [Miller-Rabin](/miller-rabin/) test replaced the Fermat test.

## References
