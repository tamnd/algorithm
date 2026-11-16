---
tag: GZ9EHE
kind: problem
slug: acceptance-problem
name: Acceptance problem (A_TM)
aliases:
- universal language
- membership problem for Turing machines
area: complexity/computability
level: intro
summary: "Given a Turing machine M and a word w, decide whether M accepts w. The language A_TM is the language of a universal machine: it is c.e., undecidable and not co-c.e."
prereqs: [universal-turing-machine, recursively-enumerable-language, diagonalization-argument]
see_also: [halting-problem, universal-turing-machine, rice-theorem, post-correspondence-problem, many-one-reducibility, recursively-enumerable-language, undecidability, decidable-language]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 4.1, Decidable languages (acceptance problems for DFAs and CFGs); Section 4.2, Undecidability (the acceptance problem for Turing machines); Chapter 5, Reducibility
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.2 (the universal language and its undecidability)
  - paper: doi:10.1112/plms/s2-42.1.230
    title: Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society (2) 42 (1936)
    locator: pp. 230 to 265, Section 6, The universal computing machine, and Section 8, Application of the diagonal process
  - book: isbn:9783642319327
    title: Robert I. Soare, Turing Computability, Theory and Applications, Springer, 2016
    locator: Chapter 2, Computably Enumerable Sets
---

The acceptance problem asks, for a [Turing machine](/turing-machine/) $M$ and a word $w$, whether $M$ accepts $w$. Its language,
$$A_{\mathrm{TM}} = \{ \langle M, w \rangle : M \text{ accepts } w \},$$
is the language of a [universal Turing machine](/universal-turing-machine/), and so it is also called the *universal language* $L_u$. It is [computably enumerable](/recursively-enumerable-language/), since the universal machine accepts exactly its members, but it is not [decidable](/decidable-language/), and its complement is not c.e. It differs from the [halting problem](/halting-problem/) only in that a machine may halt by rejecting; the two problems reduce to each other. Textbooks often prove $A_{\mathrm{TM}}$ undecidable first and use it as the source of later reductions.

## In plain words

You are given a program that answers yes or no, and an input for it. Will the program answer yes on this input?

Running the program helps only partly. If it answers yes, you know. If it answers no, you know. But if it is still running, you cannot tell whether it will answer later or never.

No method avoids this problem for all programs. If some checker could always tell whether a program answers yes, you could build a program that asks the checker about itself and then answers the opposite. The checker would be wrong about that program. So the question has no general solution, even though it is easy to confirm every yes.

## Definition

**Instance.** A Turing machine $M$, given by its code $\langle M \rangle$, and a word $w$ over the input alphabet of $M$.

**Question.** Does $M$ accept $w$, that is, does it halt in its accept state?

A word that is not a valid pair $\langle M, w \rangle$ is a no-instance.

**Theorem.** $A_{\mathrm{TM}}$ is c.e. and undecidable. Its complement $\overline{A_{\mathrm{TM}}}$ is not c.e.

*Proof that it is c.e.* The universal machine $U$ simulates $M$ on $w$ and accepts if $M$ accepts. So $L(U) = A_{\mathrm{TM}}$. On a pair where $M$ rejects, $U$ rejects; where $M$ runs forever, so does $U$.

*Proof that it is undecidable.* Suppose a machine $H$ decides $A_{\mathrm{TM}}$. Let $D$ be the machine that, on input $\langle M \rangle$, runs $H$ on $\langle M, \langle M \rangle \rangle$, accepts if $H$ rejects, and rejects if $H$ accepts. Since $H$ always halts, so does $D$. Then
$$D \text{ accepts } \langle D \rangle \iff H \text{ rejects } \langle D, \langle D \rangle \rangle \iff D \text{ does not accept } \langle D \rangle,$$
a contradiction. So $H$ does not exist. $\blacksquare$

*Proof that the complement is not c.e.* A language that is c.e. and co-c.e. is decidable (Post's theorem, on the [decidable language](/decidable-language/) page). $A_{\mathrm{TM}}$ is c.e. and undecidable, so it is not co-c.e.

**Completeness.** Every c.e. language $A = L(M_A)$ reduces to $A_{\mathrm{TM}}$ by the [many-one reduction](/many-one-reducibility/) $x \mapsto \langle M_A, x \rangle$. So $A_{\mathrm{TM}}$, like $\mathrm{HALT}$, is complete for the c.e. languages.

**Acceptance against halting.** A machine can halt in two ways, by accepting or by rejecting. $\mathrm{HALT}$ asks whether it halts in either way, and $A_{\mathrm{TM}}$ asks whether it halts by accepting. For a machine whose only halting state is the accept state, the two questions are the same. In general, each problem reduces to the other by a change to the machine (see Reductions).

## Variants

- **Restricted machines.** The acceptance problem is decidable for weaker models, because their runs can be bounded:
  - $A_{\mathrm{DFA}} = \{ \langle B, w \rangle : B \text{ is a DFA that accepts } w \}$: simulate $B$ for $|w|$ steps. The same holds for NFAs and regular expressions, after conversion to a [DFA](/deterministic-finite-automaton/).
  - $A_{\mathrm{CFG}} = \{ \langle G, w \rangle : G \text{ generates } w \}$: the [CYK algorithm](/cyk-algorithm/) on $G$ in Chomsky normal form.
  - $A_{\mathrm{LBA}}$, for linear bounded automata, which use only the cells of the input: on input length $n$, such a machine with $q$ states and $g$ tape symbols has at most $q \cdot n \cdot g^n$ configurations, so a run longer than that loops forever. With $q = 4$, $g = 5$ and $n = 4$ this bound is $10000$.
- **Nondeterministic machines.** $A_{\mathrm{NTM}}$, for a [nondeterministic Turing machine](/nondeterministic-turing-machine/), is undecidable as well; it contains $A_{\mathrm{TM}}$ as a special case. It is still c.e.: search the computation tree breadth first.
- **Bounded acceptance.** "Does $M$ accept $w$ within $t$ steps?" is decidable. With $t$ written in unary, it takes time polynomial in the input length for deterministic $M$; for nondeterministic $M$ it is [NP](/np/)-complete.
- **A fixed machine.** For one fixed machine $M$, the question "does $M$ accept $w$" is the language $L(M)$. It is decidable for some $M$ and not for others; for $M = U$ it is $A_{\mathrm{TM}}$ itself.

## Examples

Let $M$ be the decider for $\{0^k 1^k\}$ of the [Turing machine](/turing-machine/) page, and $M'$ the same machine with its reject moves replaced by moves that run right forever. Both accept the same language; they differ on the other words.

| pair | in $A_{\mathrm{TM}}$ | in $\mathrm{HALT}$ | run |
|---|---|---|---|
| $\langle M, 0011 \rangle$ | yes | yes | accepts after 13 steps |
| $\langle M, 001 \rangle$ | no | yes | rejects after 8 steps |
| $\langle M', 0011 \rangle$ | yes | yes | accepts after 13 steps |
| $\langle M', 001 \rangle$ | no | no | runs forever |

The second row shows the difference between the two problems: $M$ halts on $001$ but does not accept it.

**A machine whose acceptance hides an open problem.** Let $G$ accept the empty input if it finds an even number $n \ge 4$ that is not a sum of two primes, searching $n = 4, 6, 8, \ldots$ in order. Then $\langle G, \varepsilon \rangle \in A_{\mathrm{TM}}$ if and only if Goldbach's conjecture is false.

## Known algorithms

- **Simulation.** A universal machine confirms every yes-instance: if $M$ accepts $w$ after $T$ steps, a multitape universal machine accepts after $O(c_M T \log T)$ steps. No algorithm confirms every no-instance.
- **Restricted classes.** For DFAs, simulation takes $O(|w|)$ steps after the automaton is read. For context-free grammars in Chomsky normal form, CYK takes $O(|w|^3 \cdot |G|)$ time. For linear bounded automata, simulation with a step counter takes time exponential in $|w|$.

## Bounds

- $A_{\mathrm{TM}}$ is undecidable, by the theorem above.
- $\overline{A_{\mathrm{TM}}}$ is not c.e., so no machine can confirm every no-instance, even without a time bound.
- $A_{\mathrm{TM}}$ is complete for the c.e. languages under many-one reductions, and has [Turing degree](/turing-degrees/) $\mathbf{0}'$.

## Reductions

All reductions here are many-one reductions by total computable maps.

- **$\mathrm{HALT} \le_m A_{\mathrm{TM}}$.** Map $\langle M, w \rangle$ to $\langle M_1, w \rangle$, where $M_1$ is $M$ with every move into the reject state redirected to the accept state. $M_1$ accepts $w$ if and only if $M$ halts on $w$.
- **$A_{\mathrm{TM}} \le_m \mathrm{HALT}$.** Map $\langle M, w \rangle$ to $\langle M_2, w \rangle$, where $M_2$ is $M$ with every move into the reject state redirected to a state that loops forever. $M_2$ halts on $w$ if and only if $M$ accepts $w$.
- **$A_{\mathrm{TM}}$ to non-emptiness.** Map $\langle M, w \rangle$ to the code of a machine $M_w$ that ignores its input $x$ and runs $M$ on $w$, accepting if $M$ accepts. Then $L(M_w) = \Sigma^*$ if $M$ accepts $w$, and $L(M_w) = \emptyset$ otherwise. So $A_{\mathrm{TM}} \le_m \{ \langle N \rangle : L(N) \ne \emptyset \}$, and $\overline{A_{\mathrm{TM}}} \le_m E_{\mathrm{TM}} = \{ \langle N \rangle : L(N) = \emptyset \}$, which is therefore not c.e.
- **$A_{\mathrm{TM}}$ to regularity.** Map $\langle M, w \rangle$ to a machine that accepts $x$ if $x$ has the form $0^k 1^k$, and otherwise runs $M$ on $w$ and accepts $x$ if $M$ accepts. Its language is $\Sigma^*$, which is regular, if $M$ accepts $w$, and the non-regular $\{0^k 1^k\}$ otherwise. So $A_{\mathrm{TM}} \le_m \{ \langle N \rangle : L(N) \text{ is regular} \}$.
- **$A_{\mathrm{TM}}$ to the Post correspondence problem.** The tiles of the [Post correspondence problem](/post-correspondence-problem/) can be built from $\langle M, w \rangle$ so that a match spells out an accepting computation of $M$ on $w$. From there the reductions go on to [ambiguity of context-free grammars](/cfg-ambiguity-undecidable/).
- **[Rice's theorem](/rice-theorem/)** generalizes the last three items: $A_{\mathrm{TM}}$ reduces to every nontrivial property of the languages of machines.

## Applications

- **The source of reductions.** Proofs that a problem is undecidable usually reduce $A_{\mathrm{TM}}$ or [HALT](/halting-problem/) to it; see [undecidability](/undecidability/).
- **Stored programs.** That $A_{\mathrm{TM}}$ is c.e. is the existence of a universal machine, the basis of interpreters and stored-program computers. That it is undecidable says that no interpreter can also predict, for every program, whether the program will say yes.
- **Complexity theory.** Its bounded forms give complete problems: the bounded acceptance problem for nondeterministic machines is NP-complete, and the same idea with time or space bounds gives complete problems for other classes.

## References
