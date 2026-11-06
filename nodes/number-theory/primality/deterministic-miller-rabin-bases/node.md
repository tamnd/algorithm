---
tag: D499H8
kind: concept
slug: deterministic-miller-rabin-bases
name: Deterministic Miller-Rabin bases
aliases:
- fixed base sets for Miller-Rabin
- deterministic Miller-Rabin
area: number-theory/primality
level: advanced
summary: Small fixed sets of bases that make Miller-Rabin exact below a bound, such as the first 12 primes or 7 chosen bases below 2^64. The bounds come from computer searches for strong pseudoprimes.
prereqs: [miller-rabin, strong-pseudoprime]
see_also: [miller-rabin, strong-pseudoprime, compositeness-witness, miller-rabin-error-bound, baillie-psw, pseudoprime, primality-testing, fermat-primality-test]
sources:
  - paper: doi:10.1090/S0025-5718-1980-0572872-7
    title: Carl Pomerance, J. L. Selfridge and Samuel S. Wagstaff Jr., The pseudoprimes to 25·10^9, Mathematics of Computation 35 (1980)
    locator: pages 1003 to 1026 (the smallest strong pseudoprimes to the bases 2 and 3, to 2 3 and 5, and to 2 3 5 and 7)
  - paper: doi:10.1090/S0025-5718-1993-1192971-8
    title: Gerhard Jaeschke, On strong pseudoprimes to several bases, Mathematics of Computation 61 (1993)
    locator: pages 915 to 926 (the values for the first five to eight prime bases and the sets 2 7 61 and 31 73)
  - paper: doi:10.1090/S0025-5718-2014-02830-5
    title: Yupeng Jiang and Yingpu Deng, Strong pseudoprimes to the first eight prime bases, Mathematics of Computation 83 (2014)
    locator: pages 2915 to 2924 (the smallest strong pseudoprime to the first 9 10 and 11 prime bases)
  - paper: doi:10.1090/mcom/3134
    title: Jonathan Sorenson and Jonathan Webster, Strong pseudoprimes to twelve prime bases, Mathematics of Computation 86 (2017)
    locator: pages 985 to 1003 (the smallest strong pseudoprimes to the first 12 and 13 prime bases)
  - paper: doi:10.1090/S0025-5718-1990-1023756-8
    title: Eric Bach, Explicit bounds for primality testing and related problems, Mathematics of Computation 55 (1990)
    locator: pages 355 to 380 (under GRH, each odd composite n has a witness below 2 (ln n)^2)
  - paper: doi:10.1016/S0022-0000(76)80043-8
    title: Gary L. Miller, Riemann's hypothesis and tests for primality, Journal of Computer and System Sciences 13 (1976)
    locator: pages 300 to 317 (the deterministic test under the extended Riemann hypothesis)
  - url: https://miller-rabin.appspot.com/
    title: Deterministic variants of the Miller-Rabin primality test, the table of best known SPRP base sets
    locator: the table of best solutions for 1 to 7 bases (Worley, Izykowski and Panasiuk, Sinclair)
  - url: https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    title: Miller-Rabin primality test, Wikipedia
    locator: section Testing against small sets of bases
---

A deterministic set of [Miller-Rabin](/miller-rabin/) bases is a fixed list of bases $a_1, \ldots, a_m$ together with a bound $B$, such that every odd composite $n < B$ fails the strong test for at least one $a_i$. With such a set, Miller-Rabin gives the exact answer for every $n < B$, with no randomness and no error. The sets are found and checked by computer searches for [strong pseudoprimes](/strong-pseudoprime/); the best known are the first 12 primes and a set of 7 chosen bases, each valid for all $n < 2^{64}$.

## In plain words

The Miller-Rabin test checks a number against a helper number called a base. A prime always passes, but a few composite numbers pass for some bases. Researchers have used computers to list the composite numbers that pass for given bases, up to very large limits. From those lists, they know small groups of bases that no composite number below the limit can pass all together.

So a program that only handles numbers below the limit can test with exactly those bases and always give the right answer. For all numbers that fit in 64 binary digits, twelve fixed bases are enough, or seven well-chosen ones.

## The idea

**Strong pseudoprimes and witnesses.** Write $n - 1 = 2^s d$ with $d$ odd. An odd composite $n$ is a strong pseudoprime to the base $a$ if $a^d \equiv 1$ or $a^{2^r d} \equiv -1 \pmod n$ for some $0 \le r < s$. A base for which this fails is a [compositeness witness](/compositeness-witness/). By the [Miller-Rabin error bound](/miller-rabin-error-bound/), each odd composite $n > 9$ has at most $\varphi(n)/4$ non-witnesses, so witnesses are plentiful; the question here is whether a *fixed* short list contains one for every composite below a bound.

**The numbers $\psi_m$.** Let $\psi_m$ be the smallest odd composite that is a strong pseudoprime to each of the first $m$ primes $2, 3, 5, \ldots, p_m$. Then the first $m$ primes are a deterministic set for all $n < \psi_m$, and $\psi_m$ itself is the first failure. The known values are below; each row was computed by a search, and the work behind the larger rows uses the structure of strong pseudoprimes to prune the search.

| $m$ | bases | $\psi_m$ | factors | source |
|---|---|---|---|---|
| 1 | 2 | $2047$ | $23 \cdot 89$ | classical |
| 2 | 2, 3 | $1373653$ | $829 \cdot 1657$ | Pomerance, Selfridge, Wagstaff 1980 |
| 3 | 2 to 5 | $25326001$ | $2251 \cdot 11251$ | Pomerance, Selfridge, Wagstaff 1980 |
| 4 | 2 to 7 | $3215031751$ | $151 \cdot 751 \cdot 28351$ | Pomerance, Selfridge, Wagstaff 1980 |
| 5 | 2 to 11 | $2152302898747$ | $6763 \cdot 10627 \cdot 29947$ | Jaeschke 1993 |
| 6 | 2 to 13 | $3474749660383$ | $1303 \cdot 16927 \cdot 157543$ | Jaeschke 1993 |
| 7, 8 | 2 to 19 | $341550071728321$ | $10670053 \cdot 32010157$ | Jaeschke 1993 |
| 9, 10, 11 | 2 to 31 | $3825123056546413051$ | $149491 \cdot 747451 \cdot 34233211$ | Jiang and Deng 2014 |
| 12 | 2 to 37 | $318665857834031151167461$ | $399165290221 \cdot 798330580441$ | Sorenson and Webster 2017 |
| 13 | 2 to 41 | $3317044064679887385961981$ | | Sorenson and Webster 2017 |

The repeated rows mean that adding the base 19, or the bases 29 and 31, does not raise the bound. Since $\psi_{11} < 2^{64} < \psi_{12}$, the first 12 primes, $2, 3, \ldots, 37$, are the smallest prefix of the primes that works for all 64-digit binary numbers; the first 11 do not.

**Chosen bases.** The bases need not be small primes. A search over many candidate bases, checked against a list of all base-2 [pseudoprimes](/pseudoprime/) below a bound, finds shorter sets. The best known sets, from a public search table, are:

| bases | bound $B$ | found by |
|---|---|---|
| $9345883071009581737$ | $341531$ | Worley 2013 |
| $336781006125,\ 9639812373923155$ | $1050535501$ | Izykowski and Panasiuk 2013 |
| $4230279247111683200,\ 14694767155120705706,\ 16641139526367750375$ | $350269456337$ | Worley 2013 |
| $2,\ 141889084524735,\ 1199124725622454117,\ 11096072698276303650$ | $55245642489451$ | Worley 2013 |
| $2,\ 4130806001517,\ 149795463772692060,\ 186635894390467037,\ 3967304179347715805$ | $7999252175582851$ | Worley 2013 |
| $2,\ 123635709730000,\ 9233062284813009,\ 43835965440333360,\ 761179012939631437,\ 1263739024124850375$ | $585226005592931977$ | Worley 2013 |
| $2,\ 325,\ 9375,\ 28178,\ 450775,\ 9780504,\ 1795265022$ | at least $2^{64}$ | Sinclair 2011 |

Older sets of this kind, with small bases, are Jaeschke's $\{2, 7, 61\}$ for $n < 4759123141 = 48781 \cdot 97561$, which covers every 32-digit binary number, $\{31, 73\}$ for $n < 9080191$, and $\{2, 13, 23, 1662803\}$ for $n < 1122004669633$.

**What the bound means.** In each table, $B$ is the first odd composite that passes all the bases, so the set is valid for $n < B$, not $n \le B$. In particular $\psi_m$ itself passes the first $m$ prime bases.

**Bases larger than $n$.** A chosen base $a$ may be larger than $n$, or a multiple of it. Reduce $a$ modulo $n$, and if the result is 0, skip that base: $n$ then divides $a$, and the other bases decide. For example $325 = 5^2 \cdot 13$, so with Sinclair's set the base 325 is skipped for $n = 5$, $13$, $25$ and $65$; a test that rejected these would call the primes 5 and 13 composite.

**Under the generalized Riemann hypothesis.** Miller showed in 1976 that if the extended Riemann hypothesis holds, every odd composite $n$ has a witness $a = O((\log n)^2)$. Bach made the constant explicit in 1990: under GRH, some witness satisfies $a \le 2 (\ln n)^2$. So testing all bases up to $2(\ln n)^2$ is a deterministic primality test in polynomial time, but only if GRH is true; for $n$ near $2^{64}$ this is about 3936 bases, far more than the 7 or 12 above, which are proved by computation with no hypothesis. Without GRH, no bound on the least witness that is polynomial in $\log n$ is known.

**How the checks are done.** Every composite that passes a set containing the base 2 is a strong pseudoprime to the base 2, and so a Fermat pseudoprime to the base 2. So it is enough to test the set on a list of all base-2 Fermat pseudoprimes below the bound. Such a list for all $n < 2^{64}$ was computed by Jan Feitsma and William Galway, and the sets valid up to $2^{64}$ were checked with it. For sets without the base 2, and for bounds above $2^{64}$, as in Jiang and Deng or Sorenson and Webster, the search builds candidate strong pseudoprimes from their prime factors instead.

## Examples

**$n = 2047$ and the bases 2 and 3.** $2047 - 1 = 2 \cdot 1023$. Then $2^{1023} = (2^{11})^{93} \equiv 1^{93} = 1 \pmod{2047}$, so 2047 passes the base 2. But $3^{1023} \equiv 1565 \pmod{2047}$, which is neither $1$ nor $-1$, and $s = 1$ allows no squaring, so 3 is a witness. The set $\{2, 3\}$ is correct up to $1373653$, and this number fails it: it is a strong pseudoprime to both 2 and 3, and the base 5 exposes it.

**A 32-digit binary routine.** For $n < 2^{32}$, test $n$ against the bases 2, 7 and 61, after trial division by these three primes. Every $n < 4759123141$ gets the right answer, and $4759123141 > 2^{32}$.

**A 64-digit binary routine.** For $n < 2^{64}$, use the 12 bases $2, 3, 5, \ldots, 37$, or Sinclair's 7 bases with the reduction rule above. Each costs at most 12 or 7 modular exponentiations with 64-digit binary numbers, so a few microseconds.

**Checks run for this page.** A program listed all 2314 odd composites below $2^{32}$ that are strong pseudoprimes to the base 2, and tested the sets above on them. The first failures of the first $m$ primes below $2^{32}$ are $2047$, $1373653$, $25326001$ and $3215031751$ for $m = 1$ to 4, and none for $m = 5$; the sets $\{2, 7, 61\}$, Jaeschke's four-base set, Worley's sets with 4 to 6 bases and Sinclair's set have no failure below $2^{32}$. Direct searches over all odd composites found the first failures $341531$ for Worley's single base, $9080191$ for $\{31, 73\}$ and $1050535501$ for the Izykowski and Panasiuk pair, and no failure below $2^{32}$ for Worley's three-base set. The values $\psi_5$ to $\psi_{13}$, their factorizations and the bounds $B$ of the chosen sets were checked to pass the stated bases, and each $\psi_m$ to fail the next prime base after the repeated rows.

**Non-example.** The first 11 primes are not enough below $2^{64}$: $3825123056546413051 < 2^{64}$ passes the strong test for every prime base up to 31, and only the base 37 among the first 12 primes exposes it.

## Where it is used

- **Library primality functions for machine integers.** Many libraries test 32-digit and 64-digit binary integers with one of the sets above, after trial division by small primes, so the answer is exact and fast. The [Miller-Rabin](/miller-rabin/) page has an implementation with the first 12 primes.
- **Combined with a Lucas test.** For larger $n$, a fixed set gives only a probable prime, and the [Baillie-PSW](/baillie-psw/) test, a base-2 strong test plus a strong Lucas test, is the common choice; it has no known counterexample and is proved correct below $2^{64}$.
- **Hashed bases.** Some fast routines go further: they split the integers below $2^{32}$ or $2^{64}$ into buckets by a [hash function](/hash-function/) of $n$, and store for each bucket one or two bases that work for all of it. Then one or two strong tests suffice.
- **Factoring and sieving programs.** These test very many small numbers for primality, and a fixed set avoids a random number generator and makes runs repeatable.
- **Why the bound is needed.** No finite set of bases works for all $n$: Alford, Granville and Pomerance proved in 1994 that for every finite set of bases there are infinitely many composites that are strong pseudoprimes to all of them. So each fixed set comes with a bound, and above it one needs random bases, a Lucas test, or a proof of primality such as [ECPP](/ecpp/).

## References
