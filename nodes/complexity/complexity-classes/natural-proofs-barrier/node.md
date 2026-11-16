---
tag: 4R6J5Y
kind: concept
slug: natural-proofs-barrier
name: Natural proofs barrier
aliases:
- Razborov-Rudich barrier
area: complexity/complexity-classes
level: research
summary: "Razborov and Rudich: a lower bound proof through a property that is easy to test and true of many functions would break strong pseudorandom functions, so it cannot put NP outside P/poly."
prereqs: [circuit-complexity, p-poly, pseudorandom-function]
see_also: [relativization, algebrization-barrier, baker-gill-solovay-theorem, one-way-function, ac0, parity-problem, algorithmic-method, counting-argument]
sources:
  - paper: doi:10.1006/jcss.1997.1494
    title: Alexander A. Razborov and Steven Rudich, Natural proofs, Journal of Computer and System Sciences 55(1) (1997)
    locator: pp. 24 to 35 (natural properties, the examples from known lower bounds, and the theorem that strong pseudorandom functions rule out natural proofs against P/poly); conference version in STOC 1994
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 23, Why are circuit lower bounds so difficult? (natural properties, the parity and AC0[3] examples, and the proof of the main theorem)
  - paper: doi:10.1145/2559903
    title: Ryan Williams, Nonuniform ACC circuit lower bounds, Journal of the ACM 61(1) (2014), Article 2
    locator: the section "How do we avoid the barriers?"
---

The natural proofs barrier is a result of Razborov and Rudich (1994, journal version 1997) about the methods used to prove circuit lower bounds. Most known lower bounds, such as the proof that parity is not in [AC0](/ac0/), work through a property of Boolean functions. The property is easy to test from the truth table, it holds for many functions, and it fails for every function with small circuits. Razborov and Rudich called such a proof *natural*. They showed that if strong [pseudorandom functions](/pseudorandom-function/) exist, then no natural proof can show that a function in NP has no polynomial-size circuits, which would separate NP from [P/poly](/p-poly/). The barrier is the second of three, after [relativization](/relativization/) and before [algebrization](/algebrization-barrier/).

## In plain words

To show that a problem needs large circuits, one usually finds a feature that the problem has and that every small circuit lacks. In known proofs the feature is easy to check from the full table of answers, and a random table has it with good probability. Now suppose that a secret-key scheme exists whose outputs look random to every fast test. Each output of the scheme comes from a small circuit, so it lacks the feature. A random table often has it. So checking the feature would be a fast test that tells the scheme from true randomness, which the scheme does not allow. Hence, if such secure schemes exist, a proof of this common kind cannot show that hard search problems need large circuits. Cryptography and lower bounds pull in opposite directions here.

## The idea

**Properties of Boolean functions.** Let $F_n$ be the set of all Boolean functions $f : \{0, 1\}^n \to \{0, 1\}$. A function is given by its truth table, a string of length $N = 2^n$. A *property* is a sequence $C = (C_n)$ with $C_n \subseteq F_n$. For a circuit class $\Lambda$ such as P/poly, a property is defined to be:

- **constructive** if membership $f \in C_n$ is decidable in time polynomial in $N$, that is $2^{O(n)}$, given the truth table of $f$;
- **large** if $|C_n| \ge 2^{-O(n)} |F_n|$, so that a random function has the property with probability at least $2^{-O(n)}$, which is $1/\mathrm{poly}(N)$;
- **useful against $\Lambda$** if every sequence of functions $f_n$ with $f_n \in C_n$ for infinitely many $n$ is outside $\Lambda$. For P/poly this means that such functions need circuits of size larger than every polynomial in $n$.

A property that is constructive and large is *natural*. Razborov and Rudich also allow constructivity in other classes: a property decidable in time polynomial in $N$ is P-natural, and one whose test is itself an AC0 or an NC2 circuit on the truth table is AC0-natural or NC2-natural. Arora and Barak (Chapter 23) state largeness with the bound $2^{-n}$. A *natural proof* of a lower bound against $\Lambda$ is a proof that defines, perhaps implicitly, a natural property useful against $\Lambda$.

**Strong pseudorandom functions.** A pseudorandom function family gives, for each key $s$ of $k$ bits, a function $f_s : \{0, 1\}^m \to \{0, 1\}$, such that no efficient test can tell $f_s$ for a random key from a truly random function when it may query the function. Razborov and Rudich use a strong form: the family is computable by circuits of size polynomial in $k$, and no test that runs in time $2^{k^\varepsilon}$ tells the two apart with advantage $2^{-k^\varepsilon}$, for some $\varepsilon > 0$. Such families follow from a [pseudorandom generator](/pseudorandom-generator/) by the construction of Goldreich, Goldwasser and Micali. A sufficient hardness assumption is that factoring or the [discrete logarithm](/discrete-logarithm-problem/) needs time $2^{n^\varepsilon}$ for some $\varepsilon > 0$.

**The theorem.** *If a P-natural property useful against P/poly exists, then strong pseudorandom functions do not exist.* Equivalently, if they exist, no P-natural proof shows that a function needs superpolynomial circuits.

*Proof sketch.* Let $C$ be such a property, with test time $2^{cm}$ on functions of $m$ bits and largeness $2^{-cm}$. Take a strong pseudorandom family with keys of $k$ bits, and use it with input length $m = k^\delta$ for a small $\delta > 0$. Each $f_s$ has circuits of size polynomial in $k$, which is $m^{O(1/\delta)}$, a polynomial in $m$. Since $C$ is useful against P/poly, $f_s \notin C_m$ for every key $s$ once $m$ is large. A random function $g$ has $g \in C_m$ with probability at least $2^{-cm}$. The test "query the function on all $2^m$ inputs and check membership in $C_m$" runs in time $2^{O(m)} = 2^{O(k^\delta)}$, and it tells $f_s$ from $g$ with advantage at least $2^{-cm}$. With $\delta < \varepsilon$, this breaks the security of the family. The full proof, with exact parameters, is in Razborov and Rudich and in Arora and Barak, Chapter 23.

**What the barrier does not cover.**

- *Classes without pseudorandom functions.* The argument needs pseudorandom functions inside the class $\Lambda$. AC0 does not contain them, which is why natural proofs against AC0 exist. Candidate pseudorandom functions are known in [TC0](/tc0/), so a natural proof is not expected to give lower bounds against TC0.
- *Proofs that are not constructive or not large.* Diagonalization uses a property that holds for one specially built function, not for many. The [counting argument](/counting-argument/) of Shannon shows that most functions need large circuits, but it does not exhibit a property of an explicit function in NP.
- *Weaker statements.* The barrier is about lower bounds against P/poly and classes like it. It says nothing about uniform separations proved by other means.

## Examples

**Parity is not in AC0, as a natural proof.** The proof by random restrictions uses the property "no restriction that fixes all but $n^\varepsilon$ variables makes $f$ constant". Parity has it, since fixing variables leaves a parity or its negation of the free variables. Every AC0 function family fails it for large $n$, by the switching lemma, so the property is useful against AC0. It is constructive: there are $3^n = N^{\log_2 3}$ restrictions, and each one is checked on the truth table. Arora and Barak note that it is even AC0-natural. It is large by a union bound, since one restriction with $k$ free variables gives a constant function with probability $2 \cdot 2^{-2^k}$.

To see the numbers, take $n = 4$ and the property "no restriction that leaves $k$ variables free makes $f$ constant". An exhaustive count over all $2^{16} = 65{,}536$ functions on 4 variables gives:

| $k$ | restrictions | union bound on the bad fraction | functions with the property |
|---|---|---|---|
| 3 | $\binom{4}{3} \cdot 2^1 = 8$ | $8 \cdot 2/256 = 1/16$ | 62,022 (about 94.6%) |
| 2 | $\binom{4}{2} \cdot 2^2 = 24$ | $24 \cdot 2/16 = 3$, no information | 7,842 (about 12.0%) |

Parity on 4 variables has both properties, and AND has neither. With $k = 3$ the union bound already shows that at least 15/16 of all functions have the property, and the exact count, 0.946, is just above it. With fewer free variables the property gets stronger and rarer. In the AC0 proof, $k = n^\varepsilon$ grows, $2^{-2^k}$ falls much faster than the number of restrictions grows, and the property holds for almost all functions.

**The AC0[3] lower bound.** Razborov and Smolensky proved that parity has no polynomial-size constant-depth circuits with MOD 3 gates. Arora and Barak show that the proof is natural: it uses a property based on the rank over $\mathrm{GF}(3)$ of a matrix built from the truth table, which is NC2-natural.

**A lower bound that is not natural.** Williams (2014) proved that NEXP does not have polynomial-size ACC circuits. He writes that the proof circumvents natural proofs because of its use of diagonalization, and that there is little evidence that ACC contains pseudorandom functions, so natural proofs may not be a barrier for ACC after all. See [algorithmic method](/algorithmic-method/).

**A pitfall.** The barrier is conditional. It does not show that NP has small circuits, and it does not show that $\mathsf{P} \ne \mathsf{NP}$ is unprovable. It says that one family of methods would, if it succeeded against P/poly, also refute a cryptographic assumption that most researchers believe.

## Where it is used

- **Circuit complexity research.** The barrier is one explanation of why the methods that gave lower bounds for [AC0](/ac0/) and AC0[p] in the 1980s have not given lower bounds for TC0 or P/poly. A new lower bound method against a class that is believed to contain pseudorandom functions must be non-constructive or not large. See [circuit complexity](/circuit-complexity/).
- **The P versus NP problem.** Together with [relativization](/relativization/) and [algebrization](/algebrization-barrier/), it is one of the three known obstacles, summarized on the [P versus NP problem](/p-versus-np-problem/) page.
- **Cryptography.** The proof reads a lower bound method as an attack. A natural property useful against a class gives a test that breaks every pseudorandom function family computed in that class. See [one-way function](/one-way-function/) and [pseudorandom function](/pseudorandom-function/).
- **The algorithmic method.** Lower bounds from faster satisfiability algorithms, such as the ACC lower bound of Williams, are designed to avoid this barrier through diagonalization. See [algorithmic method](/algorithmic-method/).

## References
