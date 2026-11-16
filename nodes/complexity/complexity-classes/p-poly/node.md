---
tag: ZQ7DZ5
kind: definition
slug: p-poly
name: P/poly
aliases:
- nonuniform polynomial time
area: complexity/complexity-classes
level: advanced
summary: The problems decided in polynomial time with a polynomial-length advice string that depends only on the input length. Equivalently, the problems with polynomial-size circuit families.
prereqs: [p, boolean-circuit, non-uniform-computation]
see_also: [non-uniform-computation, adleman-theorem, karp-lipton-theorem, circuit-complexity, mahaneys-theorem, kernel-lower-bounds, hardness-versus-randomness, one-way-function]
sources:
  - paper: doi:10.1145/800141.804678
    title: Richard M. Karp and Richard J. Lipton, Some connections between nonuniform and uniform complexity classes, 12th ACM Symposium on Theory of Computing, 302 to 309 (1980)
    locator: the definition of advice classes C/f and the equality of P/poly with polynomial-size circuits
  - paper: doi:10.1137/0206023
    title: Leonard Berman and Juris Hartmanis, On isomorphisms and density of NP and other complete sets, SIAM Journal on Computing 6(2), 305 to 322 (1977)
    locator: the characterization, credited to Albert Meyer, of polynomial-size circuits by reductions to sparse sets
  - paper: doi:10.1016/S0019-9958(82)90382-5
    title: Ravi Kannan, Circuit-size lower bounds and non-reducibility to sparse sets, Information and Control 55(1-3), 40 to 56 (1982)
    locator: the fixed-polynomial circuit lower bound for the second level of the polynomial hierarchy
  - paper: doi:10.1109/CCC.1998.694585
    title: Harry Buhrman, Lance Fortnow and Thomas Thierauf, Nonrelativizing separations, 13th IEEE Conference on Computational Complexity, 8 to 12 (1998)
    locator: the theorem that MA_EXP is not in P/poly
  - paper: doi:10.1016/0304-3975(83)90020-8
    title: Chee K. Yap, Some consequences of non-uniform conditions on uniform classes, Theoretical Computer Science 26(3), 287 to 300 (1983)
    locator: the collapse of the hierarchy if coNP is in NP/poly
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 6, Boolean circuits (the class P/poly and Turing machines that take advice)
---

P/poly is the class of decision problems that a polynomial-time machine decides when it also gets an advice string of polynomial length, where the advice may depend on the input length but not on the input itself. The same class is the set of languages with [Boolean circuit](/boolean-circuit/) families of polynomial size, one circuit for each input length, with no condition on how the circuits are found. P/poly contains [P](/p/) and [BPP](/bpp/), and it also contains undecidable languages, so it is not a class of algorithms in the usual sense. It is the class that circuit lower bounds aim at: a proof that some problem in [NP](/np/) is not in P/poly would separate P from NP. The [non-uniform computation](/non-uniform-computation/) page proves the equality of the two definitions and the main theorems about advice. This page gives the definition, the members and non-members, and the known bounds.

## Definition

**Advice.** Let $a : \mathbb{N} \to \{0,1\}^*$ be any function with $|a(n)| \le p(n)$ for a polynomial $p$. A language $L$ is in $\mathsf{P/poly}$ if there are such a function $a$ and a deterministic polynomial-time machine $M$ with

$$x \in L \iff M(x, a(|x|)) = 1 \quad \text{for every } x.$$

The advice $a(n)$ is the same for all inputs of length $n$. It need not be computable.

**Circuits.** Equivalently, $L \in \mathsf{P/poly}$ if and only if there are a polynomial $s$ and circuits $C_0, C_1, \ldots$ such that $C_n$ has $n$ inputs, fan-in 2 AND and OR gates and NOT gates, at most $s(n)$ gates, and $C_n(x) = L(x)$ for every $x \in \{0,1\}^n$. There is no bound on depth and no uniformity condition. The description of $C_n$ is the advice in one direction. In the other direction, the tableau of $M$ on inputs of length $n$, with the advice bits fixed, is a circuit of polynomial size.

**General advice classes.** Karp and Lipton (1980) defined $\mathcal{C}/f$ for a class $\mathcal{C}$ and a length function $f$: the languages decided by a $\mathcal{C}$-machine with advice of length $f(n)$. So $\mathsf{NP/poly}$, $\mathsf{L/poly}$ and $\mathsf{P}/\log$ are defined the same way. With $\mathcal{C}$ a class of machines, the machine must behave correctly only with the right advice.

## Examples and non-examples

**Members.**

- *P.* Use empty advice.
- *BPP.* By [Adleman's theorem](/adleman-theorem/), one random string per length, after amplification, works for all inputs of that length. So $\mathsf{BPP} \subseteq \mathsf{P/poly}$.
- *Every unary language.* If $L \subseteq \{1\}^*$, the advice $a(n)$ is the single bit $[1^n \in L]$. This includes undecidable languages, such as $\{1^n : $ the $n$-th Turing machine halts$\}$, so $\mathsf{P/poly}$ is not contained in any class of decidable languages.
- *Sparse languages.* A language $S$ is sparse if it has at most $q(n)$ strings of length $n$ for a polynomial $q$. Then $S \in \mathsf{P/poly}$: the advice lists the strings of $S$ of length $n$, and the machine compares $x$ with each of them.

**Sparse oracles: a second characterization.** A language is in $\mathsf{P/poly}$ if and only if it is decided by a polynomial-time machine with a sparse oracle, that is $\mathsf{P/poly} = \bigcup_{S \text{ sparse}} \mathsf{P}^S$, with polynomial-time [Turing reductions](/turing-reduction/) to $S$. Berman and Hartmanis (1977) credit this to Albert Meyer. The reduction from advice to a sparse set encodes the prefixes of each advice string:

$$S = \{\, 1^n 0 w : w \text{ is a prefix of } a(n) \,\}.$$

For example, with advice $a(1) = 1$, $a(2) = 01$, $a(3) = 110$ and $a(4) = 0111$, the set $S$ restricted to these lengths has $14$ strings, from $10$ to $111100111$, and at most $3$ of any one length. In general $S$ has at most $p(n) + 1$ strings for each $n$, so it is sparse. To find $a(n)$, the machine asks whether $1^n 0 w 0$ and $1^n 0 w 1$ are in $S$, starting from the empty $w$, and extends $w$ by the bit that gives a yes, until neither does. This takes $2p(n) + 2$ queries, each chosen after the previous answers. The other direction is short: a machine that runs in time $q(n)$ asks only about strings of length at most $q(n)$, and the strings of $S$ up to that length are polynomially many, so they can be the advice. For [many-one reductions](/polynomial-time-reduction/) the situation is different: a sparse set is NP-hard under many-one reductions only if $\mathsf{P} = \mathsf{NP}$ ([Mahaney's theorem](/mahaneys-theorem/)).

**Non-members.**

- *Most functions.* By the [counting argument](/counting-argument/) on the [Boolean circuit](/boolean-circuit/) page, almost all functions of $n$ bits need circuits of size $\Omega(2^n/n)$. A machine with space $2^{O(n)}$ can find, for each $n$, the first truth table in lexicographic order that has no circuit of size $n^{\log n}$, by trying all circuits. So the class $\mathsf{ESPACE} = \mathsf{DSPACE}(2^{O(n)})$ is not in $\mathsf{P/poly}$.
- *Fixed polynomial size.* For each fixed $k$, some language in $\Sigma_2^p \cap \Pi_2^p$ has no circuits of size $O(n^k)$ (Kannan 1982). The idea: in $\Sigma_4^p$ one can say "the first function with no circuit of size $n^k$", and the [Karp-Lipton theorem](/karp-lipton-theorem/) brings this down when NP has small circuits. Later work moved the bound into smaller classes, such as $\mathsf{ZPP}^{\mathsf{NP}}$ and PP.
- *Exponential classes.* Buhrman, Fortnow and Thierauf (1998) proved that $\mathsf{MA}_{\mathsf{EXP}}$, the exponential-time version of [Merlin-Arthur](/merlin-arthur/), is not in P/poly. Whether NEXP is in P/poly, and even whether $\mathsf{EXP}^{\mathsf{NP}}$ is, is open.

**What is open.** Whether $\mathsf{NP} \subseteq \mathsf{P/poly}$ is open. It is believed false for three reasons:

- If it holds, then the [polynomial hierarchy](/polynomial-hierarchy/) collapses to $\Sigma_2^p$ (Karp-Lipton theorem).
- If $\mathsf{coNP} \subseteq \mathsf{NP/poly}$, then the hierarchy collapses to $\Sigma_3^p$ (Yap 1983). This weaker consequence is the base of the [kernel lower bounds](/kernel-lower-bounds/) in parameterized complexity.
- Cryptography assumes the opposite: a [one-way function](/one-way-function/) must be hard to invert for circuits of polynomial size, and if $\mathsf{NP} \subseteq \mathsf{P/poly}$ then every polynomial-time function can be inverted by such circuits, so no one-way function of this kind exists.

**Why the "/poly" matters for derandomization.** If some language in $\mathsf{E} = \mathsf{DTIME}(2^{O(n)})$ needs circuits of size $2^{\Omega(n)}$, then $\mathsf{P} = \mathsf{BPP}$ ([hardness versus randomness](/hardness-versus-randomness/)). Here the hard function must be hard for P/poly, not only for P, because the proof uses the circuits that would break a generator.

## Related definitions

- [Non-uniform computation](/non-uniform-computation/): advice and circuits in general, with proofs.
- [Circuit complexity](/circuit-complexity/): the study of the size of circuits, of which P/poly is the polynomial case.
- [Karp-Lipton theorem](/karp-lipton-theorem/) and [Adleman's theorem](/adleman-theorem/): the main theorems that relate P/poly to uniform classes.
- $\mathsf{L/poly}$: logspace with polynomial advice, equal to polynomial-size [branching programs](/branching-program/).
- [AC0](/ac0/), [TC0](/tc0/) and [NC](/nc/) in their non-uniform form are subclasses of P/poly with depth restrictions.

## References
