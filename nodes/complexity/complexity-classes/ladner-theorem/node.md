---
tag: S9RN5J
kind: theorem
slug: ladner-theorem
name: Ladner's theorem
aliases:
- NP-intermediate existence
area: complexity/complexity-classes
level: advanced
summary: "If P is not equal to NP, then NP contains problems that are neither in P nor NP-complete. The proof pads SAT by a slowly growing amount chosen by delayed diagonalization."
prereqs: [np-intermediate, np-complete, polynomial-time-reduction, sat]
see_also: [np-intermediate, ladners-theorem, p-versus-np-problem, np-complete, mahaneys-theorem, time-hierarchy-theorem, diagonalization-argument, relativization]
sources:
  - paper: doi:10.1145/321864.321877
    title: Richard E. Ladner, On the structure of polynomial time reducibility, Journal of the ACM 22(1) (1975), 155 to 171
    locator: the existence theorem for NP and the density of the polynomial-time degrees
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Section 3.3, Ladner's theorem (the proof by padding SAT), and the chapter notes of Chapter 3
  - paper: "Uwe Schöning, A uniform approach to obtain diagonal sets in complexity classes, Theoretical Computer Science 18 (1982), 95 to 103"
    locator: the uniform diagonalization theorem
---

Ladner's theorem says that if $\mathsf{P} \ne \mathsf{NP}$, then [NP](/np/) contains languages that are neither in [P](/p/) nor [NP-complete](/np-complete/). Such languages are called [NP-intermediate](/np-intermediate/). Ladner proved it in 1975. The language that the proof builds is SAT padded by a slowly growing amount, where the growth is chosen by diagonalization against all polynomial-time machines. This page proves the form for NP. The page on [Ladner's theorem in general form](/ladners-theorem/) covers the version between any two degrees.

## Statement

**Theorem (Ladner, 1975).** If $\mathsf{P} \ne \mathsf{NP}$, then there is a language $L \in \mathsf{NP} \setminus \mathsf{P}$ that is not NP-complete under polynomial-time many-one reductions.

The statement is an implication. It does not say that NP-intermediate languages exist, because that would imply $\mathsf{P} \ne \mathsf{NP}$. The converse is also true: if $\mathsf{P} = \mathsf{NP}$, every language in NP is in P, so none is NP-intermediate. So NP-intermediate languages exist if and only if $\mathsf{P} \ne \mathsf{NP}$.

## In plain words

Assume that the hardest problems in NP really cannot be solved fast. The theorem says that some problem then sits strictly between the fast problems and the hardest ones.

The proof takes a hardest problem and adds a long block of filler symbols to each input. The filler makes the problem easier, because the time allowed grows with the input length. Too little filler leaves the problem among the hardest, and too much filler makes it fast to solve. The proof picks the amount of filler step by step, with a rule that checks all fast programs on small inputs. If some fast program solves the problem, the filler stays small, which would make the hardest problem fast too. If no fast program solves it, the filler grows, but so slowly that the problem never becomes one of the hardest.

## Proof

The full proof is in [the proof of Ladner's theorem](proofs/main.md). It follows the proof in the textbook of Arora and Barak (Section 3.3).

**The language.** Let $M_1, M_2, \ldots$ list all deterministic Turing machines so that every machine appears infinitely often in the list. Define a function $H$ on the natural numbers by

$H(n) =$ the smallest $i < \log \log n$ such that, for every string $x$ with $|x| \le \log n$, the machine $M_i$ on input $x$ outputs the right answer for membership of $x$ in $\text{SAT}_H$ within $i (|x| + 1)^i$ steps; and $H(n) = \lfloor \log \log n \rfloor$ if there is no such $i$.

Let

$$\text{SAT}_H = \{ \psi \, 0 \, 1^{n^{H(n)}} : \psi \in \text{SAT}, \ n = |\psi| \}.$$

The two definitions refer to each other, but $H(n)$ only needs membership of strings of length at most $\log n$, so the recursion is well founded.

**Four facts.**

1. $H$ is computable in time polynomial in $n$, by brute force on the strings of length at most $\log n$, which are fewer than $2n$.
2. $\text{SAT}_H \in \mathsf{NP}$: check the padding by computing $H(|\psi|)$, then guess an assignment for $\psi$.
3. If $\text{SAT}_H \in \mathsf{P}$, then $H$ is bounded: the fast machine for $\text{SAT}_H$ appears as some $M_i$ and is found by the minimum for every large $n$.
4. If $\text{SAT}_H \notin \mathsf{P}$, then $H(n) \to \infty$: if $H(n) = i$ for infinitely many $n$, then $M_i$ is right on all strings and $\text{SAT}_H \in \mathsf{P}$.

**Not in P.** If $\text{SAT}_H \in \mathsf{P}$, then $H(n) \le C$, the padding has polynomial length at most $n^C$, and $\psi \mapsto \psi \, 0 \, 1^{n^{H(n)}}$ reduces SAT to $\text{SAT}_H$ in polynomial time. Then $\text{SAT} \in \mathsf{P}$ and $\mathsf{P} = \mathsf{NP}$.

**Not NP-complete.** If SAT reduces to $\text{SAT}_H$ by a map that runs in time $n^i$, then the image of a formula $\psi$ of length $n$ is a padded formula $\psi'$ of length $m$ with $m^{H(m)} \le n^i$. Since $H(m) \to \infty$, $H(m) > 2i$ for all large $m$, and then $m < \sqrt{n}$. Applying the reduction again and again shrinks the formula to a constant size in $O(\log \log n)$ rounds, which decides SAT in polynomial time. Again $\mathsf{P} = \mathsf{NP}$. $\square$

## Consequences

- NP-intermediate languages exist if and only if $\mathsf{P} \ne \mathsf{NP}$. A proof that a specific language is NP-intermediate would prove $\mathsf{P} \ne \mathsf{NP}$.
- Applied repeatedly, the method gives an infinite chain of NP-intermediate languages, each strictly easier than the one before under polynomial-time reductions. Ladner also proved that the polynomial-time degrees of decidable languages are dense: if $A <_p B$, there is a language $C$ with $A <_p C <_p B$ ([general form](/ladners-theorem/)).
- The proof only simulates machines and uses no special property of SAT except its membership in NP and its completeness. The same method works for other classes with complete problems and an effective list of their machines. Schöning (1982) gave a uniform theorem of this kind.
- The proof relativizes: it stays true for machines with any oracle. So it cannot say anything about the P versus NP problem itself ([relativization](/relativization/)).

## Tightness

- The hypothesis cannot be dropped: if $\mathsf{P} = \mathsf{NP}$, there are no NP-intermediate languages.
- The language $\text{SAT}_H$ is artificial. The theorem gives no natural problem. For factoring, the discrete logarithm and graph isomorphism there is evidence of intermediate status, but no proof, even under the assumption $\mathsf{P} \ne \mathsf{NP}$ ([NP-intermediate](/np-intermediate/)).
- Some natural families have no intermediate members at all. By the [CSP dichotomy theorem](/csp-dichotomy-theorem/), every constraint satisfaction problem over a fixed finite template is in P or NP-complete. So Ladner's construction cannot be carried out inside such a family.
- The padding function grows extremely slowly: $H(n) \le \log \log n$, which is 6 at $n = 2^{64}$. Natural problems do not behave like this, which is one reason why the constructed language does not answer the question for natural problems.

## History

Ladner (1975) proved the theorem in his paper on the structure of polynomial-time reducibility. His construction "blows holes" in SAT: it removes from SAT all formulas whose lengths lie in certain long intervals, and it decides the intervals by delayed diagonalization, so that the remaining language differs from every polynomial-time language and no polynomial-time reduction from SAT works. The same paper proves the density of the polynomial-time degrees. The proof by padding on this page is the one in the textbook of Arora and Barak, whose chapter notes attribute it to an unpublished manuscript of Impagliazzo. Schöning (1982) turned the method into a uniform diagonalization theorem for many complexity classes.

## References
