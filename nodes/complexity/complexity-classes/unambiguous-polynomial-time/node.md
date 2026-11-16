---
tag: H6P7AN
kind: definition
slug: unambiguous-polynomial-time
name: UP
aliases:
- unambiguous NP
area: complexity/complexity-classes
level: advanced
summary: The languages accepted by polynomial-time nondeterministic machines that have at most one accepting path on every input. P is in UP and UP is in NP.
prereqs: [np, nondeterministic-turing-machine, certificate]
see_also: [np, valiant-vazirani-theorem, one-way-function, integer-factorization, parity-game, aks-primality-test, np-intermediate, co-np]
sources:
  - paper: doi:10.1016/0020-0190(76)90097-1
    title: Leslie G. Valiant, Relative complexity of checking and evaluating, Information Processing Letters 5(1), 20 to 23 (1976)
    locator: the definition of the class UP
  - paper: doi:10.1137/0217018
    title: Joachim Grollmann and Alan L. Selman, Complexity measures for public-key cryptosystems, SIAM Journal on Computing 17(2), 309 to 335 (1988)
    locator: the theorem that one-to-one one-way functions exist if and only if P is not UP
  - paper: doi:10.1016/S0020-0190(98)00150-1
    title: Marcin Jurdziński, Deciding the winner in parity games is in UP ∩ co-UP, Information Processing Letters 68(3), 119 to 124 (1998)
    locator: the main theorem
  - paper: doi:10.4007/annals.2004.160.781
    title: Manindra Agrawal, Neeraj Kayal and Nitin Saxena, PRIMES is in P, Annals of Mathematics 160(2), 781 to 793 (2004)
    locator: the main theorem
  - paper: doi:10.1016/0304-3975(86)90135-0
    title: Leslie G. Valiant and Vijay V. Vazirani, NP is as easy as detecting unique solutions, Theoretical Computer Science 47(1), 85 to 93 (1986)
    locator: the randomized reduction from SAT to unique SAT
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley (1994)
    locator: Chapter 12, Cryptography (one-way functions and the class UP)
---

UP (unambiguous polynomial time) is the class of languages accepted by a polynomial-time [nondeterministic Turing machine](/nondeterministic-turing-machine/) that has at most one accepting computation path on every input. Equivalently, it is the class of languages in [NP](/np/) with a verifier for which every yes-instance has exactly one [certificate](/certificate/). Valiant defined the class in 1976. $\mathsf{P} \subseteq \mathsf{UP} \subseteq \mathsf{NP}$, and neither inclusion is known to be strict. UP is closely tied to cryptography: one-to-one one-way functions exist if and only if $\mathsf{P} \ne \mathsf{UP}$.

## Definition

**Model.** A nondeterministic [multitape Turing machine](/multitape-turing-machine/) $M$ runs in polynomial time on every computation path. An input is accepted if at least one path accepts.

**Definition (Valiant 1976).** A language $L$ is in $\mathsf{UP}$ if there is such a machine $M$ with $L(M) = L$ and, for every input $x$, at most one accepting path of $M$ on $x$.

**Verifier form.** $L \in \mathsf{UP}$ if and only if there are a polynomial $p$ and a deterministic polynomial-time verifier $V$ such that for every $x$:

- $x \in L$ if and only if $V(x, u) = 1$ for some $u \in \{0,1\}^{p(|x|)}$, and
- for every $x$ there is at most one such $u$.

To go from a machine to a verifier, let $u$ be the sequence of nondeterministic choices; to go back, let the machine guess $u$. Each direction keeps the number of accepting paths equal to the number of certificates.

**Points to note.**

- The condition is on the machine and must hold on every input. So a yes-instance has exactly one accepting path and a no-instance has none. A language is in UP if some unambiguous machine accepts it, even if other natural machines for it are ambiguous.
- For NP, a clock on a nondeterministic machine gives a list of machines that covers exactly the class. No such rule is known for the unambiguous machines, and no UP-complete problem is known.
- $\mathsf{coUP}$ is the class of complements of UP languages, and $\mathsf{UP} \cap \mathsf{coUP}$ is the class of languages where both yes-instances and no-instances have unique certificates.

**Basic properties.**

- $\mathsf{P} \subseteq \mathsf{UP}$: a deterministic machine has at most one path.
- $\mathsf{UP} \subseteq \mathsf{NP}$ by definition, and $\mathsf{UP} \cap \mathsf{coUP} \subseteq \mathsf{NP} \cap \mathsf{coNP}$.
- UP is closed under intersection (run both machines one after the other; the pair of accepting paths is unique) and under polynomial-time many-one reductions.

## Examples and non-examples

**Factoring is in UP ∩ coUP.** Let $\mathrm{FACT} = \{(N, k) : N$ has a prime factor at most $k\}$. A certificate is the list of prime factors of $N$ in nondecreasing order. The verifier checks that each entry is prime with the [AKS test](/aks-primality-test/), that the list is sorted, and that the product is $N$. The prime factorization is unique, so every $N$ has exactly one valid list. For $(N, k) \in \mathrm{FACT}$ the verifier also checks that the first entry is at most $k$; for $(N, k) \notin \mathrm{FACT}$ the same list, with first entry above $k$, is the unique certificate of the complement. For example, $N = 1001$ has the unique list $(7, 11, 13)$, so $(1001, 10) \in \mathrm{FACT}$ and $(1001, 5) \notin \mathrm{FACT}$. So $\mathrm{FACT} \in \mathsf{UP} \cap \mathsf{coUP}$. By binary search on $k$, an algorithm for FACT finds a prime factor. If [integer factorization](/integer-factorization/) were NP-hard under polynomial-time Turing reductions, then $\mathsf{NP} \subseteq \mathsf{P}^{\mathsf{NP} \cap \mathsf{coNP}} = \mathsf{NP} \cap \mathsf{coNP}$, and so $\mathsf{NP} = \mathsf{coNP}$.

**An ambiguous verifier.** The verifier for composite numbers that takes a divisor $d$ with $1 < d < N$ as certificate is ambiguous: $N = 1001$ has the $6$ certificates $7$, $11$, $13$, $77$, $91$ and $143$, and $N = 360$ has $22$. This verifier does not show that the language is in UP. The language of composite numbers is still in UP, because it is in P by the AKS test, and also because the sorted list of prime factors is a unique certificate.

**Parity games.** Deciding the winner of a [parity game](/parity-game/) is in $\mathsf{UP} \cap \mathsf{coUP}$ (Jurdziński 1998). No polynomial-time algorithm for the problem is known.

**Non-examples and open cases.**

- *NP-complete problems.* No NP-complete problem is known to be in UP. The natural verifier for SAT is ambiguous, since a formula can have many satisfying assignments. If some NP-complete problem were in UP, then $\mathsf{UP} = \mathsf{NP}$, since UP is closed under many-one reductions.
- *Unique solutions as a promise.* The [Valiant-Vazirani theorem](/valiant-vazirani-theorem/) reduces SAT to SAT on formulas with at most one solution by randomized reductions. This does not put SAT in UP: the reduction is randomized, and on a satisfiable input it gives a formula with exactly one solution only with probability about $1/(8n)$.
- *Counting the certificates.* A machine with exactly two accepting paths on some input is not unambiguous, even if it has at most one on every other input.

## Related definitions

- **One-way functions.** A function $f$ is one-way in the worst-case sense if it is computable in polynomial time, $|x|$ and $|f(x)|$ are polynomially related, and no polynomial-time algorithm inverts it on every input in its range. Grollmann and Selman (1988) proved that a one-to-one function of this kind exists if and only if $\mathsf{P} \ne \mathsf{UP}$. If $f$ is one-to-one, the language $\{(y, i, b) :$ the $i$-th bit of $f^{-1}(y)$ is $b\}$ is in UP, with $f^{-1}(y)$ as the unique certificate. This is worst-case hardness; [one-way functions](/one-way-function/) for cryptography need hardness on average.
- [NP](/np/): at least one certificate, with no bound on their number.
- $\oplus\mathsf{P}$ is the class of languages where a nondeterministic polynomial-time machine accepts when its number of accepting paths is odd. A UP machine has $0$ or $1$ accepting paths, so $\mathsf{UP} \subseteq \oplus\mathsf{P}$. The class appears in [Toda's theorem](/toda-theorem/).
- [NP-intermediate](/np-intermediate/): FACT is a candidate for a problem in NP that is neither in P nor NP-complete.

## References
