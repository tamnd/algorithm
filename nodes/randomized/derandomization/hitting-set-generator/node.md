---
tag: A5Y8J7
kind: definition
slug: hitting-set-generator
name: Hitting set generator
aliases:
- HSG
- hitting set
- epsilon-hitting set generator
area: randomized/derandomization
level: advanced
summary: A generator whose output hits every set of inputs that a fixed class of tests accepts with non-negligible probability.
prereqs: [pseudorandom-generator, rp, one-sided-error]
see_also: [disperser, expander-walk-sampler, polynomial-identity-testing, small-bias-sample-space, randomness-amplification, hardness-versus-randomness, schwartz-zippel-lemma, hitting-set]
sources:
  - paper: doi:10.1145/273865.273933
    title: Alexander E. Andreev, Andrea E. F. Clementi and José D. P. Rolim, A new general derandomization method, Journal of the ACM 45(1), 1998
    locator: pages 179 to 213 (hitting set generators for circuits and the result that they give BPP = P)
  - paper: doi:10.1109/sfcs.1989.63449
    title: Aviad Cohen and Avi Wigderson, Dispersers, deterministic amplification, and weak random sources, FOCS 1989
    locator: pages 14 to 19 (dispersers and one-sided amplification)
  - paper: doi:10.1016/0022-0000(88)90035-9
    title: Michael Sipser, Expanders, randomness, or time versus space, Journal of Computer and System Sciences 36(3), 1988
    locator: pages 379 to 383 (one-sided derandomization of RP with dispersers)
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1-3), 2012
    locator: Chapter 7, Section 7.1 (the definition of pseudorandom generators, of which hitting set generators are the one-sided form) and Chapter 6, Section 6.2 (dispersers)
---

A **hitting set generator** maps short seeds to strings so that every test from a fixed class that accepts a large fraction of all strings also accepts at least one output of the generator. It is the one-sided form of a [pseudorandom generator](/pseudorandom-generator/): a pseudorandom generator must make each test accept with about the right probability, while a hitting set generator must only make each test accept at least once. This is what an algorithm with [one-sided error](/one-sided-error/) needs: if a polynomial time hitting set generator with logarithmic seed length exists for polynomial size circuits, then $\mathrm{RP} = \mathrm{P}$. Andreev, Clementi and Rolim (1998) proved that such a generator also gives $\mathrm{BPP} = \mathrm{P}$.

## Definition

Notation. $m$ is the output length and $\ell$ the seed length. A *test* is a function $T : \{0,1\}^m \to \{0,1\}$; it *accepts* $x$ if $T(x) = 1$. $U_m$ is the uniform distribution on $\{0,1\}^m$, and $\mathcal{C}$ is a class of tests, such as the Boolean circuits of size at most $m$. $\varepsilon \in (0, 1)$.

**Definition.** A function $H : \{0,1\}^\ell \to \{0,1\}^m$ is an *$\varepsilon$-hitting set generator* for $\mathcal{C}$ if for every $T \in \mathcal{C}$,

$$\Pr_{x \sim U_m}[T(x) = 1] \ge \varepsilon \quad \Longrightarrow \quad \exists s \in \{0,1\}^\ell : T(H(s)) = 1.$$

The image $\{H(s) : s \in \{0,1\}^\ell\}$ is an *$\varepsilon$-hitting set* for $\mathcal{C}$: it meets the accepting set of every test of density at least $\varepsilon$. Seen as a set system, it is a [hitting set](/hitting-set/) for the family of accepting sets of the tests in $\mathcal{C}$ that have density at least $\varepsilon$. The generator is *efficient* if $H$ (or the whole list of outputs) can be computed in time polynomial in $2^\ell$ and $m$.

Compare the definition of a pseudorandom generator $G$ with error $\varepsilon$: $|\Pr[T(G(U_\ell)) = 1] - \Pr[T(U_m) = 1]| \le \varepsilon$ for every $T \in \mathcal{C}$. That condition is two-sided and controls the probability; the hitting condition is one-sided and asks only for one accepting seed.

**Facts.**

1. **A pseudorandom generator is a hitting set generator.** If $G$ fools $\mathcal{C}$ with error $\varepsilon$, then $G$ is an $\varepsilon'$-hitting set generator for every $\varepsilon' > \varepsilon$: a test with $\Pr[T(U_m) = 1] \ge \varepsilon'$ has $\Pr[T(G(U_\ell)) = 1] \ge \varepsilon' - \varepsilon > 0$. The converse fails, see the examples.
2. **Hitting sets exist.** If $\mathcal{C}$ is finite, a multiset of $K$ independent uniform strings misses a fixed test of density at least $\varepsilon$ with probability at most $(1 - \varepsilon)^K < e^{-\varepsilon K}$. With $K > \ln|\mathcal{C}|/\varepsilon$, the [union bound](/union-bound/) shows that some multiset hits every test. For circuits of size $m$, $\ln|\mathcal{C}| = O(m \log m)$, so a hitting set with seed length $\log_2 m + \log_2(1/\varepsilon) + O(\log \log m)$ exists. The problem is to compute one.
3. **Hitting sets derandomize RP.** Let $\mathcal{A}$ be an [RP](/rp/) algorithm whose run on inputs of length $n$ uses $m = \mathrm{poly}(n)$ random bits and is a circuit $T_w(r) = \mathcal{A}(w, r)$ of size $\mathrm{poly}(n)$. Run $\mathcal{A}(w, H(s))$ for every seed $s$, and accept if some run accepts. If $w$ is not in the language, no run accepts, since $\mathcal{A}$ has one-sided error. If $w$ is in the language, $T_w$ has density at least $1/2$ and the hitting set contains an accepting string. With $\ell = O(\log n)$ and $H$ efficient, the time is polynomial, so $\mathrm{RP} = \mathrm{P}$.
4. **Hitting sets derandomize BPP (Andreev, Clementi and Rolim 1998).** An efficient $1/2$-hitting set generator with logarithmic seed length for circuits also gives $\mathrm{BPP} = \mathrm{P}$. The proof does not simply run the BPP algorithm on the hitting set; it uses the hitting set to find, deterministically, approximations of the acceptance probability of circuits. Goldreich, Vadhan and Wigderson later gave a simpler proof.

## Examples and non-examples

- **Nonconstant affine tests.** Let $\mathcal{C}$ be the tests $T(x) = \langle a, x \rangle \oplus c$ with $a \ne 0$, each of density exactly $1/2$. The $m + 1$ strings $0, e_1, \ldots, e_m$ (zero and the unit vectors) form a $1/2$-hitting set: for $a \ne 0$, $\langle a, 0 \rangle = 0$ and $\langle a, e_i \rangle = 1$ for any $i$ with $a_i = 1$, so both values of the parity appear. This set is not pseudorandom for the same class: the test $x_1$ accepts only $e_1$, with probability $1/(m+1)$ in place of $1/2$. Any [small-bias sample space](/small-bias-sample-space/) with bias below 1 is also a hitting set for this class.
- **A non-example for the affine class.** The even-weight strings $\{000, 011, 101, 110\}$ do not hit the test $x_1 \oplus x_2 \oplus x_3$, which is 1 on half of $\{0,1\}^3$ but 0 on all four strings.
- **Polynomials.** Let $\mathcal{C}$ be the tests "$p(x) \ne 0$" for nonzero polynomials $p$ of total degree at most $d$ in $n$ variables over a field, with $x$ uniform on $S^n$ for a set $S$ of size $|S| \ge 2d$. By the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) each test has density at least $1 - d/|S| \ge 1/2$. A hitting set for this class is exactly a deterministic black-box [polynomial identity test](/polynomial-identity-testing/). The grid $T^n$ with $|T| = d + 1$ is a hitting set of size $(d+1)^n$; explicit hitting sets of polynomial size are known only for restricted classes of polynomials, such as sparse polynomials.
- **Expander walks.** For the class of all tests of density at least $1 - \mu$, no small hitting set exists, since a test can reject any $\mu 2^m$ strings. But an [expander walk](/expander-walk-sampler/) hits every such test with probability $1 - \mu(\mu + \lambda(1 - \mu))^{t-1}$ over a short seed, and a [disperser](/disperser/) hits every such test from almost every value of a weak random source. These are the "seeded" versions of hitting sets.
- **All tests.** If $\mathcal{C}$ contains every function, an $\varepsilon$-hitting set must have more than $(1 - \varepsilon)2^m$ points, because the test that rejects exactly the hitting set has density at least $\varepsilon$ otherwise. So hitting set generators are useful only for restricted classes.

## Related definitions

- [Pseudorandom generator](/pseudorandom-generator/): the two-sided notion. Every pseudorandom generator is a hitting set generator, with a slightly larger $\varepsilon$.
- [Disperser](/disperser/): a function of a weak random source and a short seed whose outputs hit every large set; the one-sided relative of an extractor, as a hitting set generator is of a pseudorandom generator.
- [Hardness versus randomness](/hardness-versus-randomness/): hard functions give pseudorandom generators and hence hitting set generators.
- [Randomness amplification](/randomness-amplification/): reducing the error of an RP algorithm with few random bits, the "seeded" form of a hitting set.
- **Hitting sets for restricted models.** Hitting sets for read-once branching programs and for combinatorial rectangles have in some cases been built with seeds shorter than those of the pseudorandom generators known at the time for the same classes.

## References
