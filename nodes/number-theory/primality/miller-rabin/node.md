---
tag: T1483D
kind: algorithm
slug: miller-rabin
name: Miller-Rabin primality test
aliases:
- Miller-Rabin test
- strong probable prime test
area: number-theory/primality
level: core
summary: Randomized test that checks the strong probable prime condition for random bases; it never rejects a prime, and it accepts a composite with probability below 1/4 per base.
solves: [primality-testing]
model: multitape-turing-machine
complexity:
  vars: {n: the number tested, k: the number of rounds}
  time: {worst: O(k (log n)^3), best: O(1)}
  space: {extra: O(log n)}
properties: {deterministic: false, recursive: false, certifying: false}
history:
  year: 1976
  people: [Gary L. Miller, Michael O. Rabin]
  note: Miller gave a deterministic version that is correct under the extended Riemann hypothesis; Rabin made it a randomized test with an unconditional error bound. Both papers on the bound appeared in 1980, with Monier's independent proof.
prereqs: [fermat-primality-test, nontrivial-square-root-of-one, modular-exponentiation, strong-pseudoprime]
see_also: [miller-rabin-error-bound, deterministic-miller-rabin-bases, strong-liar, compositeness-witness, baillie-psw, solovay-strassen, random-prime-generation, miller-rabin-primality-test]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.8, Primality testing (the procedures WITNESS and MILLER-RABIN, and the error bound 2^-s)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 3.5, Probable primes and witnesses (the strong probable prime test and Theorem 3.5.4)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.4, Factoring into primes (Algorithm P, probabilistic primality test)
  - paper: doi:10.1016/S0022-0000(76)80043-8
    title: Gary L. Miller, Riemann's hypothesis and tests for primality, Journal of Computer and System Sciences 13 (1976)
    locator: pages 300 to 317
  - paper: doi:10.1016/0022-314X(80)90084-0
    title: Michael O. Rabin, Probabilistic algorithm for testing primality, Journal of Number Theory 12 (1980)
    locator: pages 128 to 138
  - paper: doi:10.1016/0304-3975(80)90007-9
    title: Louis Monier, Evaluation and comparison of two efficient probabilistic primality testing algorithms, Theoretical Computer Science 12 (1980)
    locator: pages 97 to 108
  - paper: doi:10.1090/S0025-5718-1990-1023756-8
    title: Eric Bach, Explicit bounds for primality testing and related problems, Mathematics of Computation 55 (1990)
    locator: pages 355 to 380 (under GRH, every odd composite n has a strong witness below 2 (ln n)^2)
---

The Miller-Rabin test decides whether an odd integer $n$ is probably [prime](/prime-number/). It writes $n - 1 = 2^s d$ with $d$ odd and, for a random base $a$, looks at the sequence $a^d, a^{2d}, \ldots, a^{2^s d} \bmod n$. For a prime this sequence either starts with 1 or reaches $-1$ before it reaches 1; a sequence that breaks this rule proves that $n$ is composite, either by the Fermat condition or by a [nontrivial square root of 1](/nontrivial-square-root-of-one/). A prime is never rejected, and a composite passes one round with probability below $1/4$, so $k$ rounds err with probability below $4^{-k}$ on every input. It costs the same as the [Fermat test](/fermat-primality-test/) and has no exceptions like the [Carmichael numbers](/carmichael-number/), which is why it is the standard test in practice.

## In plain words

For a prime number there is a fixed rule about what you see when you take a random helper number, raise it to a certain odd power, and then square the result again and again, always keeping only the remainder. The values must end at one, and if they reach one only after a few squarings, the value just before must be minus one.

Pick a random helper and run this chain of squarings. If the rule breaks, the number is surely not prime, and the helper proves it. If the rule holds, the number may be prime. For every composite number, at most one helper in four obeys the rule, so ten random helpers leave a chance of about one in a million, and twenty leave about one in a trillion. Unlike the plain Fermat test, no composite number fools most helpers.

## The problem

The input is an integer $n \ge 0$ and a number of rounds $k \ge 1$. The output is false, which means "$n$ is not prime", or true, which means "$n$ is probably prime". This is a [Monte Carlo](/monte-carlo-algorithm/) solution of the [primality testing](/primality-testing/) problem with [one-sided error](/one-sided-error/): false is always right, each prime gets true, and an odd composite gets true with probability below $4^{-k}$.

**Cost model.** The integers are of arbitrary precision. Let $\ell = \lfloor \lg n \rfloor + 1$ be the number of binary digits of $n$, so $\ell = \Theta(\log n)$. Costs are in bit operations, as on a [multitape Turing machine](/multitape-turing-machine/), and $M(\ell)$ is the cost of one product of two $\ell$-digit integers: $O(\ell^2)$ for [schoolbook multiplication](/schoolbook-multiplication/), $O(\ell \log \ell)$ for [Harvey and van der Hoeven](/harvey-van-der-hoeven-multiplication/). For $n$ that fits in a machine word of $w$ binary digits, with a product modulo $n$ in one step, the [word RAM](/word-ram/) bounds are given too.

## The algorithm

Let $n$ be odd, $n - 1 = 2^s d$ with $d$ odd. A base $a$ is a *strong liar* for $n$, and $n$ is a [strong probable prime](/strong-pseudoprime/) to the base $a$, if

$$a^d \equiv 1 \pmod n \quad \text{or} \quad a^{2^j d} \equiv -1 \pmod n \text{ for some } 0 \le j < s.$$

A base for which neither holds is a *strong witness* (a [compositeness witness](/compositeness-witness/)). A composite $n$ that is a strong probable prime to the base $a$ is a strong pseudoprime to that base.

```pseudo id=main
MILLER-RABIN(n, k)                          ▷ true means "probably prime"
L1  if n < 4 then return n ≥ 2              ▷ 0 and 1 are not prime; 2 and 3 are prime
L2  if n is even then return false
L3  write n − 1 = 2^s · d with d odd
L4  for i ← 1 to k do
L5      a ← a uniform random integer in [2, n − 2]
L6      x ← a^d mod n
L7      if x = 1 or x = n − 1 then go to the next round
L8      for j ← 1 to s − 1 do
L9          x ← x² mod n                     ▷ now x = a^(2^j d) mod n
L10         if x = n − 1 then go to the next round
L11     return false                        ▷ a is a strong witness
L12 return true
```

Lines L1 and L2 handle the small and the even inputs, so the loop runs only for odd $n \ge 5$. Line L3 strips the factors 2 from $n - 1$; since $n$ is odd, $s \ge 1$. Line L6 computes $a^d$ by [binary exponentiation](/binary-exponentiation/). Lines L7 to L10 check the strong condition along the sequence $a^d, a^{2d}, \ldots, a^{2^{s-1} d}$: the round passes as soon as it sees $-1$, or if the sequence starts at 1. The last term $a^{2^s d} = a^{n-1}$ is not computed, because if none of the earlier terms is $-1$, the round fails whatever it is. Line L11 is reached when the round fails. If $x$ becomes 1 inside the loop of line L8, it stays 1, and line L11 will be reached; at that point the previous value of $x$ was a nontrivial square root of 1.

## Example

**The Carmichael number 561.** $n = 561 = 3 \cdot 11 \cdot 17$, $n - 1 = 560 = 2^4 \cdot 35$, so $s = 4$, $d = 35$. With the base $a = 2$:

| step | line | $x$ |
|---|---|---|
| $a^{35}$ | L6 | $263$ |
| $a^{70}$ | L9, $j = 1$ | $166$ |
| $a^{140}$ | L9, $j = 2$ | $67$ |
| $a^{280}$ | L9, $j = 3$ | $1$ |

No value is $560$, so line L11 returns false. The Fermat test with the same base passes, since $2^{560} \equiv 1$. Here $67^2 \equiv 1 \pmod{561}$ with $67 \not\equiv \pm 1$, and $\gcd(66, 561) = 33$ is a factor.

**A strong pseudoprime to the bases 2 and 3.** $n = 1373653 = 829 \cdot 1657$, $n - 1 = 2^2 \cdot 343413$, so $s = 2$ and line L8 does one squaring.

- $a = 2$: $2^{343413} \equiv 890592$, then $890592^2 \equiv 1373652 = n - 1$. The round passes at line L10.
- $a = 3$: $3^{343413} \equiv 1$. The round passes at line L7.
- $a = 5$: $5^{343413} \equiv 1199564$, then $1199564^2 \equiv 73782$, which is not $n - 1$. Line L11 returns false.

So 1373653 is a strong pseudoprime to the bases 2 and 3, the smallest one, and 5 is a strong witness for it.

## Correctness

A prime $n$ is never rejected. By [Fermat's little theorem](/fermat-little-theorem/), $a^{2^s d} = a^{n-1} \equiv 1 \pmod n$. Modulo a prime the only square roots of 1 are $\pm 1$. So in the sequence $a^d, a^{2d}, \ldots, a^{2^s d}$, either the first term is 1, or the term before the first 1 is $-1$; that term has index below $s$. In both cases the round passes at line L7 or L10. Hence the answer false is always right: lines L1 and L2 are right by inspection, and line L11 is reached only when $n$ is not prime.

For an odd composite $n > 9$ the number of strong liars in $[1, n - 1]$ is at most $\varphi(n)/4$, by the [Monier-Rabin theorem](/miller-rabin-error-bound/). The bases $1$ and $n - 1$ are always liars and are not drawn, so one round passes with probability at most $\frac{\varphi(n)/4 - 2}{n - 3} < \frac14$. For $n = 9$ the only liars are $1$ and $8$, so no base in $[2, 7]$ passes. The rounds are independent, so $k$ rounds pass with probability below $4^{-k}$. The full proof is in the proofs.

## Complexity

**One round.** Line L6 is one [modular exponentiation](/modular-exponentiation/) with an exponent $d < n$, at most $\ell - 1$ squarings and $\ell - 1$ other products. Lines L8 to L10 add at most $s - 1 \le \ell$ squarings. Together that is $O(\ell)$ products modulo $n$, the same as one Fermat round. With schoolbook arithmetic a round costs $O(\ell^3) = O((\log n)^3)$ bit operations; with fast multiplication and division, $O(\ell \, M(\ell))$, which is $O((\log n)^2 \log \log n)$ with the Harvey and van der Hoeven bound.

**All rounds.** The worst case is a prime, or a composite that passes many rounds: $k$ rounds, $O(k (\log n)^3)$ bit operations with schoolbook arithmetic. The best case is $O(1)$, for $n < 4$ or $n$ even. For a random composite the first round almost always fails, so the expected cost on composites is about one round. Line L5 uses $O(\log n)$ random binary digits per round.

**Word RAM.** For $n < 2^w$ with a product modulo $n$ in $O(1)$ steps, a round costs $O(\log n)$ steps and the test $O(k \log n)$.

**Space.** The values $a$, $d$ and $x$ need $O(\log n)$ binary digits, so the extra space is $O(\log n)$, or $O(1)$ words.

**Error.** The error is one-sided: a wrong answer is always true on a composite. For an odd composite $n$ the probability of true is exactly $\left(\frac{|S(n)| - 2}{n - 3}\right)^k < 4^{-k}$, where $|S(n)|$ is the number of strong liars. It depends only on $n$ and $k$; the probability is over the random bases, not over the inputs. For a random input the error is much smaller, since most composites have few strong liars; see the [error bound](/miller-rabin-error-bound/) page.

## Properties

- **Monte Carlo with one-sided error.** False is a proof of compositeness; true is not a proof of primality.
- **Uniform error bound.** The bound $4^{-k}$ holds for every composite input, including Carmichael numbers. This is the main gain over the [Fermat test](/fermat-primality-test/).
- **Stronger than Fermat and Solovay-Strassen base by base.** Each strong liar is an Euler liar, and each Euler liar is a Fermat liar. So with the same bases Miller-Rabin rejects every composite that [Solovay-Strassen](/solovay-strassen/) or the Fermat test rejects.
- **Sometimes finds a factor.** When a round fails after a value $x \not\equiv \pm 1$ with $x^2 \equiv 1$, $\gcd(x - 1, n)$ is a proper factor of $n$.

## Variants and improvements

- **Fixed bases for bounded inputs.** Testing a fixed set of bases makes the test deterministic below a known bound. The first twelve primes, $2, 3, \ldots, 37$, give a correct test for all $n < 2^{64}$, because the smallest strong pseudoprime to all of them is $318665857834031151167461 > 2^{64}$ (Sorenson and Webster 2017). Smaller sets are known; see [deterministic Miller-Rabin bases](/deterministic-miller-rabin-bases/).
- **Miller's test.** Test every base $a \le 2 (\ln n)^2$. By Bach (1990), this is correct for every $n$ if the generalized Riemann hypothesis holds; the result is conditional. It costs $O((\log n)^5)$ bit operations with schoolbook arithmetic.
- **[Baillie-PSW](/baillie-psw/).** One strong test with the base 2, followed by a strong Lucas test. No composite is known to pass, and none exists below $2^{64}$.
- **Early exit on 1.** If $x$ becomes 1 in line L9, return false at once; the sequence can no longer reach $-1$.
- **Trial division first.** Dividing by the small primes before line L4 removes most composites more cheaply, which matters in [random prime generation](/random-prime-generation/).
- **Number of rounds for random candidates.** For random candidates of hundreds of binary digits, the average-case bounds of Damgård, Landrock and Pomerance justify fewer rounds than $4^{-k}$ would suggest; standards such as FIPS 186 list the round counts.

## When to use it

Use Miller-Rabin as the default primality test for large integers: in key generation, in computer algebra, and as the inner test of factoring and sieving code. Use a fixed base set for 64-bit integers, where the answer is then exact. When the input may come from an adversary, draw the bases at random at run time, not from a fixed list, because composites that pass any fixed list of bases can be built. When you need a proof that $n$ is prime, use a proving method such as [ECPP](/ecpp/), the [APR-CL test](/apr-cl-primality-test/), or a [Pocklington](/pocklington-primality-test/) certificate.

## Pitfalls

- **Fixed bases against adversaries.** Arnault (1995) built a 397-digit composite that is a strong pseudoprime to every prime base below 307. A library that tests only fixed small bases accepts such a number. Random bases avoid this.
- **Bases 1 and n − 1.** These are always liars. Drawing from $[1, n - 1]$ wastes rounds; draw from $[2, n - 2]$.
- **Off by one in the squaring loop.** The loop must test $a^{2^j d}$ for $j < s$ only. Testing $j = s$ as well would also accept bases with $a^{n-1} \equiv -1$, which no prime has, so the test would accept more composites.
- **Small and even inputs.** For $n \le 3$ the range $[2, n - 2]$ is empty, and the even prime 2 needs a special case.
- **Overflow on a word.** For $n$ near $2^{64}$, the square in line L9 needs 128 binary digits. Use a double-width product or [Montgomery multiplication](/montgomery-multiplication/).
- **A weak random source.** The error bound assumes independent uniform bases. A generator seeded with a constant, or one an adversary can predict, gives no guarantee.

## Implementations

## History

Gary Miller described the test in 1976 as a deterministic algorithm that tries all bases up to $O((\log n)^2)$, and proved it correct under the extended Riemann hypothesis. Michael Rabin observed in 1976 that random bases give an unconditional test, and in his 1980 paper he proved that at most a quarter of the bases are strong liars. Louis Monier proved the same bound in 1980, with an exact count of the liars. The strong probable prime condition itself was used earlier in computations by Selfridge and others. Pomerance, Selfridge and Wagstaff (1980) computed the smallest strong pseudoprimes to the first few prime bases, the start of the deterministic base sets.

## References
