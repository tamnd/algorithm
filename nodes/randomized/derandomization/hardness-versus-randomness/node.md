---
tag: 66131Q
kind: concept
slug: hardness-versus-randomness
name: Hardness versus randomness
aliases:
- hardness vs randomness paradigm
area: randomized/derandomization
level: advanced
summary: Hard functions give pseudorandom generators, and generators give hard functions. So derandomizing BPP and proving circuit lower bounds are close to the same problem.
prereqs: [pseudorandom-generator, bpp, circuit-complexity, p-poly]
see_also: [nisan-wigderson-generator, impagliazzo-wigderson-theorem, polynomial-identity-testing, nexptime, subexponential-time, natural-proofs-barrier, nisan-prg, pseudorandom-generation]
sources:
  - paper: doi:10.1016/S0022-0000(05)80043-1
    title: Noam Nisan and Avi Wigderson, Hardness vs randomness, Journal of Computer and System Sciences 49(2), 1994
    locator: the generator from an average-case hard function and its consequences for BPP at each level of hardness
  - paper: doi:10.1145/258533.258590
    title: Russell Impagliazzo and Avi Wigderson, P = BPP if E requires exponential circuits, derandomizing the XOR lemma, 29th ACM Symposium on Theory of Computing (STOC), 1997
    locator: the main theorem, from worst-case exponential circuit lower bounds to P = BPP
  - paper: doi:10.1007/s00037-004-0182-6
    title: Valentine Kabanets and Russell Impagliazzo, Derandomizing polynomial identity tests means proving circuit lower bounds, Computational Complexity 13(1 to 2), 2004
    locator: the main theorem, from a fast deterministic identity test to circuit lower bounds for NEXP or the permanent
  - paper: doi:10.1109/SFCS.1982.45
    title: Andrew C. Yao, Theory and applications of trapdoor functions, 23rd IEEE Symposium on Foundations of Computer Science (FOCS), 1982
    locator: the use of a cryptographic generator to simulate BPP in subexponential time
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 20 (derandomization, the Nisan-Wigderson construction, and the theorem of Kabanets and Impagliazzo)
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1 to 3), 2012
    locator: Chapter 7 (pseudorandom generators from average-case and worst-case hardness)
---

Hardness versus randomness is the idea that computational hardness can replace random bits. If some function in exponential time is hard for small circuits, its values on a few correlated inputs look random to small circuits, and a [pseudorandom generator](/pseudorandom-generator/) with a short seed follows. The generator lets a deterministic algorithm try all seeds, so [BPP](/bpp/) becomes P or close to it. The link also runs the other way: a good enough derandomization implies circuit lower bounds. So, up to the details, proving that randomness does not help and proving that some explicit function is hard are one research problem.

## In plain words

Random choices make many algorithms simple. The question is whether they are really needed. Hardness versus randomness says: if some problem is truly hard to solve with small circuits, then the answers of that problem look like random coin flips to any small circuit. An algorithm can then use these answers instead of real coins. It tries all short seeds, which is cheap, and takes the majority answer.

The link goes both ways. If someone could remove randomness from every fast algorithm, then some explicit problem would have to be hard. So progress on one side is progress on the other, and both sides are still open.

## The idea

**From hardness to generators.** Let $f$ be a Boolean function that no small circuit computes well. The [Nisan-Wigderson generator](/nisan-wigderson-generator/) evaluates $f$ on $m$ subsets of the seed that overlap little. A circuit that tells its output from uniform gives, through [Yao's next-bit argument](/yao-next-bit-unpredictability/), a small circuit that predicts $f$, which contradicts the hardness. The generator may run in time exponential in its seed, because the derandomization tries all seeds anyway. This is the difference from the cryptographic generators of [HILL](/hill-prg-from-one-way-functions/), which must run faster than the tests.

**From generators to derandomization.** Suppose $G : \{0,1\}^{d(m)} \to \{0,1\}^m$ fools circuits of size $m$ with error $\frac1{10}$ and runs in time $2^{O(d(m))}$. Let $A$ be a BPP algorithm with running time $T(n)$ and error at most $\frac13$. For a fixed input $x$, the map $r \mapsto A(x, r)$ is a circuit of size about $T(n)^2$. Take $m = T(n)^2$, run $A(x, G(s))$ for all $2^{d(m)}$ seeds, and output the majority. Each seed answer is correct with probability at least $\frac23 - \frac1{10} > \frac12$ over the seed, so the majority is correct. The time is $2^{O(d(m))} \cdot T(n)$. With $d(m) = O(\log m)$ this is polynomial, so BPP $=$ P.

**From generators to hardness.** This direction is short and unconditional.

*Claim.* Let $G : \{0,1\}^{d} \to \{0,1\}^{m}$ with $m \ge d + 1$ be computable in time $2^{O(d)}$ and fool circuits of size $s$ with error less than $\frac12$. Define $f$ on $d + 1$ bits by $f(z) = 1$ when $z$ is the prefix of length $d + 1$ of some $G(u)$. Then $f$ is computable in time $2^{O(d)}$, and no circuit of size $s$ computes $f$.

*Proof.* To compute $f(z)$, run $G$ on all $2^d$ seeds; this takes time $2^{O(d)}$. Suppose a circuit $C$ of size at most $s$ computes $f$. The test $D(y) = C(y_1, \ldots, y_{d+1})$ also has size at most $s$. It accepts $G(U_d)$ with probability 1. The prefixes of outputs of $G$ number at most $2^d$ among the $2^{d+1}$ strings of length $d+1$, so $D$ accepts $U_m$ with probability at most $\frac12$. The advantage is at least $\frac12$, a contradiction. $\square$

With $d = O(\log m)$ and $s = m$, the function $f$, extended to all input lengths, is in $\mathrm{E} = \mathrm{DTIME}(2^{O(n)})$ and needs circuits of size $2^{\Omega(n)}$. So a generator with logarithmic seed of this kind *exists if and only if* E has a function that needs circuits of size $2^{\Omega(n)}$; the reverse direction is the [Impagliazzo-Wigderson theorem](/impagliazzo-wigderson-theorem/).

**From derandomization to lower bounds.** Derandomizing one problem, not the whole of BPP, already gives lower bounds. Kabanets and Impagliazzo (2004) proved:

*Theorem (Kabanets and Impagliazzo 2004).* If [polynomial identity testing](/polynomial-identity-testing/) for arithmetic circuits is in P, or even in nondeterministic subexponential time, then NEXP is not in [P/poly](/p-poly/), or the [permanent](/permanent-computation/) has no arithmetic circuits of polynomial size.

Polynomial identity testing is in BPP by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), so BPP $=$ P would imply one of these two lower bounds. The proof goes through the result of Impagliazzo, Kabanets and Wigderson (2002) that NEXP $\subseteq$ P/poly implies NEXP $=$ MA, and through Toda's and Valiant's theorems on the permanent. Neither conclusion is known today, so this explains why unconditional derandomization of BPP is hard.

## Examples

The known implications, with the type of each result:

| assumption | conclusion | source | type |
|---|---|---|---|
| one-way functions secure against polynomial-size circuits | BPP $\subseteq \bigcap_{\varepsilon > 0} \mathrm{DTIME}(2^{n^\varepsilon})$ | Yao 1982, with HILL 1999 | conditional |
| some $f \in \mathrm{E}$ is hard on average for circuits of size $2^{\Omega(n)}$, with advantage $2^{-\Omega(n)}$ | BPP $=$ P | Nisan and Wigderson 1994 | conditional |
| some $f \in \mathrm{E}$ needs circuits of size $2^{\Omega(n)}$ in the worst case | BPP $=$ P | Impagliazzo and Wigderson 1997 | conditional |
| EXP $\not\subseteq$ P/poly | BPP $\subseteq \bigcap_{\varepsilon > 0}$ i.o.-$\mathrm{DTIME}(2^{n^\varepsilon})$ | Babai, Fortnow, Nisan and Wigderson 1993 | conditional |
| BPP $\ne$ EXP | BPP has subexponential simulations that look correct to efficient samplers, for infinitely many lengths | Impagliazzo and Wigderson 1998 | conditional, uniform |
| a generator with seed $O(\log m)$ fools size $m$ | some $f \in \mathrm{E}$ needs circuits of size $2^{\Omega(n)}$ | the claim above | unconditional implication |
| identity testing in NSUBEXP | NEXP $\not\subseteq$ P/poly, or the permanent has no polynomial-size arithmetic circuits | Kabanets and Impagliazzo 2004 | unconditional implication |

Here "i.o." means that the simulation is correct for infinitely many input lengths.

**Unconditional cases.** Where a lower bound is known, the paradigm gives an unconditional generator.

- *Constant-depth circuits.* Parity needs exponential size in [AC0](/ac0/), by Håstad's switching lemma. Nisan (1991) turned this into a generator with seed of polylogarithmic length that fools AC0 circuits.
- *Space-bounded machines.* A machine with little memory cannot remember its random bits. [Nisan's generator](/nisan-prg/) uses this to fool read-once branching programs with a seed of $O(\log^2 n)$ bits.
- *Single problems.* Some problems were derandomized directly, without a generator: [primality testing](/aks-primality-test/) is in P by the AKS algorithm, and undirected connectivity is in logspace by Reingold's algorithm.

## Where it is used

- **Complexity theory.** The paradigm frames the question BPP $=$ P? as a question about circuit lower bounds. Most researchers expect BPP $=$ P because they expect E to need exponential circuits.
- **Extractors.** Trevisan saw that the NW proof does not use the complexity of $f$, only its truth table. The result is [Trevisan's extractor](/trevisan-extractor/), an unconditional object built by the same method.
- **Arthur-Merlin games.** The same method, with circuits that may use an NP oracle, derandomizes [Arthur-Merlin](/arthur-merlin/) protocols under hardness assumptions for nondeterministic circuits.
- **Barriers.** The two-way link means that unconditional derandomization of BPP needs new lower bounds, and new lower bounds face barriers such as [natural proofs](/natural-proofs-barrier/).

## References
