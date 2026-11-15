---
tag: SZNC8Y
kind: theorem
slug: mahaneys-theorem
name: Mahaney's theorem
aliases:
- sparse NP-complete sets theorem
area: complexity/np-completeness
level: research
summary: If a sparse set, one with polynomially many strings up to each length, is NP-hard under Karp reductions, then P = NP. This settled a conjecture of Berman and Hartmanis.
prereqs: [np-complete, polynomial-time-reduction, sat]
see_also: [ladners-theorem, self-reducibility, p-poly, karp-lipton-theorem, unary-encoding, turing-reduction, np-intermediate, cook-levin-theorem]
sources:
  - paper: doi:10.1016/0022-0000(82)90002-2
    title: Stephen R. Mahaney, Sparse complete sets for NP, Solution of a conjecture of Berman and Hartmanis, Journal of Computer and System Sciences 25(2), 130 to 143 (1982)
    locator: the main theorem (if a sparse set is NP-complete under many-one reductions, then P = NP); preliminary version in FOCS 1980, 54 to 60
  - paper: doi:10.1137/0206023
    title: Leonard Berman and Juris Hartmanis, On isomorphisms and density of NP and other complete sets, SIAM Journal on Computing 6(2), 305 to 322 (1977)
    locator: the isomorphism conjecture and the conjecture that no NP-complete set is sparse
  - paper: doi:10.1137/0220030
    title: Mitsunori Ogiwara and Osamu Watanabe, On polynomial-time bounded truth-table reducibility of NP sets to sparse sets, SIAM Journal on Computing 20(3), 471 to 483 (1991)
    locator: the left-set technique and the extension to bounded truth-table reductions
  - book: isbn:9783540674191
    title: Lane A. Hemaspaandra and Mitsunori Ogihara, The Complexity Theory Companion, Springer (2002)
    locator: Chapter 1 (the self-reducibility technique), Section 1.1 (no sparse NP-complete sets unless P = NP)
---

Mahaney's theorem says that an [NP-complete](/np-complete/) problem cannot be sparse unless P = NP. A set is sparse when it has only polynomially many strings of each length, so it holds very little information. [SAT](/sat/) has exponentially many yes-instances of each length. Mahaney proved in 1980 that if SAT reduces to a sparse set by a [polynomial-time reduction](/polynomial-time-reduction/) (a Karp reduction), then SAT is in P. This proved, under the hypothesis P ≠ NP, a conjecture of Berman and Hartmanis. The short proof given here, by the left set, is due to Ogiwara and Watanabe (1991).

## Statement

The model is the deterministic multitape Turing machine, and $\le_m^p$ is the Karp reduction.

**Definition.** A language $S \subseteq \{0,1\}^*$ is sparse when there is a polynomial $p$ with $|S \cap \{0,1\}^{\le \ell}| \le p(\ell)$ for every $\ell$. A tally set, a subset of $\{1\}^*$, is a special case. The function $\ell \mapsto |S \cap \{0,1\}^{\le \ell}|$ is the census of $S$.

**Theorem (Mahaney 1982).** If some sparse set $S$ is NP-hard under Karp reductions, that is, $\mathrm{SAT} \le_m^p S$, then $\mathsf{P} = \mathsf{NP}$.

**Corollary.** There is a sparse NP-complete set if and only if P = NP. (For the converse: if P = NP, then the one-string set $\{1\}$ is in NP, and SAT reduces to it by deciding SAT and mapping to $1$ or to $0$.)

**Examples.** A script counted strings of length $n$ for $n = 5, 10, 20$:

| $n$ | all strings | at most two 1s | palindromes | in $\{1\}^*$ |
|---|---|---|---|---|
| 5 | 32 | 16 | 8 | 1 |
| 10 | 1024 | 56 | 32 | 1 |
| 20 | 1048576 | 211 | 1024 | 1 |

The strings with at most two 1s have $1 + n + \binom{n}{2}$ members of length $n$, a polynomial, so this set is sparse. The palindromes have $2^{\lceil n/2 \rceil}$ members of length $n$, so they are not sparse, though they are a tiny part of all strings. Every tally set is sparse, with at most one string of each length.

## In plain words

Some sets of strings are thin: for each length they contain only a few strings, a number that grows like a polynomial in the length. A thin set can still be hard to decide, but it cannot hold much information. Mahaney asked whether a problem in the hardest group of easy-to-check problems can be thin. He showed that it cannot, unless all those problems are easy. The idea of the short proof is this: if satisfiability translates into a thin set, then a search for the first satisfying setting of the variables can throw away all but a few partial settings at each step, because the thin set has room for only a few different answers. So the search ends quickly, and satisfiability becomes easy.

## Proof

The full proof and a run of the algorithm are on [the proof page](proofs/main.md). Here is the plan.

**The left set.** For a CNF formula $\varphi$ with $n$ variables and $w \in \{0,1\}^n$, let $\langle \varphi, w\rangle \in \mathrm{LSAT}$ when some satisfying assignment $z$ of $\varphi$ has $z \le w$ in lexicographic order. LSAT is in NP, so it reduces to SAT and then to $S$, by a reduction $h$ with polynomially long outputs.

**The search.** Build the satisfying assignments bit by bit, keeping a list of prefixes. At level $i$, extend each prefix by 0 and by 1, and represent each prefix $u$ by the largest assignment $u1 \cdots 1$ that starts with it. If $z^*$ is the smallest satisfying assignment, then the prefixes below the prefix of $z^*$ give no-instances of LSAT, and the prefix of $z^*$ and all larger ones give yes-instances. So:

- among prefixes with the same image under $h$, keep only the smallest; the prefix of $z^*$ survives, because all smaller prefixes are no-instances and $h$ separates yes from no;
- after that, the surviving prefixes from $z^*$ on have different images, all in $S$ and all of polynomial length, so there are at most $q = p(r(N))$ of them; keep only the $q$ largest prefixes, and the prefix of $z^*$ survives again.

**The cost.** The list never has more than $q$ prefixes, so after $n$ levels the algorithm checks at most $q$ full assignments, in polynomial time. It finds $z^*$ whenever $\varphi$ is satisfiable. So SAT is in P.

**A run.** On $\varphi = (x_1 \lor x_2) \land (\lnot x_1 \lor x_3) \land (x_2 \lor x_4) \land (\lnot x_3 \lor \lnot x_4)$, with satisfying assignments $0100, 0101, 0110, 1110$, a script ran the search with a stand-in for $h$ and $q = 4$. The prefixes of $z^* = 0100$ survived at every level. At the last level, five prefixes survived the first rule, and the second rule dropped $0000$, which does not satisfy $\varphi$.

## Consequences

- **Density of NP-complete sets.** If P ≠ NP, every NP-complete set has a census that grows faster than every polynomial. In this sense NP-complete sets are dense.
- **The isomorphism conjecture.** Berman and Hartmanis (1977) conjectured that all NP-complete sets are polynomial-time isomorphic, that is, related by polynomial-time bijections whose inverses are also polynomial-time. Such a bijection changes the census by at most a polynomial in the length, and SAT is not sparse, so the conjecture implies that no NP-complete set is sparse. Mahaney's theorem proves this weaker statement from P ≠ NP alone. The isomorphism conjecture itself is still open.
- **Tally sets and unary encodings.** Every tally set is sparse. So a problem in NP whose instances are single numbers written in [unary](/unary-encoding/), that is, strings $1^n$, is not NP-complete unless P = NP.
- **Stronger reductions.** Ogiwara and Watanabe (1991) extended the theorem to bounded truth-table reductions: if SAT reduces to a sparse set by a polynomial-time reduction that asks a fixed number of questions in advance, then P = NP.

## Tightness

- **The hypothesis is needed.** If P = NP, the sparse set $\{1\}$ is NP-complete, as in the Corollary.
- **Density.** Sparse means polynomial census. Sets of slightly larger census can be NP-complete. Pad SAT: map $x$ to $x\,1\,0^{|x|^2}$. The set of padded formulas is NP-complete, and a string of length $n = \ell^2 + \ell + 1$ in it comes from a string of length $\ell$, so there are at most $2^{\ell} \le 2^{\sqrt{n}}$ of them. A script counted the possible padded strings for $\ell = 3, 4, 5$: lengths 13, 21 and 31 carry at most 8, 16 and 32 strings, against $2^{13}$, $2^{21}$ and $2^{31}$ strings in all. Padding by $0^{|x|^c}$ gives NP-complete sets with census about $2^{n^{1/c}}$. So the theorem rules out polynomial census, padding allows census $2^{n^{\varepsilon}}$ for every fixed $\varepsilon > 0$, and this theorem does not settle the census functions in between, such as $2^{(\log n)^2}$.
- **Turing reductions.** For polynomial-time Turing ([Cook](/turing-reduction/)) reductions the theorem is not known. A language Cook-reduces to some sparse set exactly when it is in [P/poly](/p-poly/). So "SAT Cook-reduces to a sparse set" means $\mathsf{NP} \subseteq \mathsf{P/poly}$, which by the [Karp-Lipton theorem](/karp-lipton-theorem/) collapses the polynomial hierarchy to its second level, but is not known to give P = NP.
- **Complete sets for other classes.** The theorem is about NP. Other classes behave differently: under polynomial-time Karp reductions every nontrivial set in P is complete for P, sparse ones included. This is one reason why P-completeness uses log-space reductions.

## History

In 1977 Berman and Hartmanis observed that all the NP-complete problems known then were polynomial-time isomorphic, conjectured that this holds for all of them, and conjectured as a consequence that no sparse set is NP-complete. Piotr Berman (1978) proved that no tally set is NP-complete unless P = NP, and Steven Fortune (1979) proved that no sparse set is coNP-complete unless P = NP. Mahaney settled the sparse case for NP at FOCS 1980 (journal version 1982). His proof guesses the census of the sparse set up to the relevant length, a number of polynomial size, and uses it to recognize the strings outside the set as well as the strings in it. Ogiwara and Watanabe (1991) found the left-set proof given here and used it to extend the theorem to bounded truth-table reductions. Hemaspaandra and Ogihara present it as the first example of the self-reducibility technique.

## References
