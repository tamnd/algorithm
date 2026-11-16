---
tag: X5R2ZA
kind: definition
slug: decidable-language
name: Decidable language
aliases:
- recursive language
- decidable problem
area: complexity/computability
level: intro
summary: A language is decidable if a Turing machine halts on every input and accepts exactly the words of the language. It is decidable exactly when it and its complement are both c.e.
prereqs: [turing-machine]
see_also: [recursively-enumerable-language, computable-function, undecidability, halting-problem, acceptance-problem, rice-theorem, decision-procedure, time-hierarchy-theorem]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 3 (deciders and Turing-decidable languages); Section 4.1, Decidable languages; Section 4.2 (a language is decidable if and only if it and its complement are Turing-recognizable)
  - paper: doi:10.1090/S0002-9904-1944-08111-1
    title: Emil L. Post, Recursively enumerable sets of positive integers and their decision problems, Bulletin of the American Mathematical Society 50(5) (1944)
    locator: pp. 284 to 316 (a set is recursive if and only if it and its complement are recursively enumerable)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.2 (recursive languages and the complements of recursive and recursively enumerable languages)
  - book: isbn:9780262680523
    title: Hartley Rogers Jr., Theory of Recursive Functions and Effective Computability, MIT Press (reprint of the McGraw-Hill edition of 1967)
    locator: Chapter 5 (recursive and recursively enumerable sets)
---

A language $L \subseteq \Sigma^*$ is *decidable* if some [Turing machine](/turing-machine/) halts on every input, accepts every word of $L$ and rejects every word outside $L$. Such a machine is a *decider* for $L$. The older name is *recursive language*; this page uses "decidable". A decision problem is decidable when the language of its yes-instances, under a fixed computable encoding, is decidable. Decidability is the computability notion of "solvable by an algorithm". It says nothing about time: a decidable language can need more time than any fixed computable bound.

## Definition

Fix a finite alphabet $\Sigma$. A Turing machine $M$ is a *decider* if it halts on every input $w \in \Sigma^*$, in its accept state or its reject state. A decider $M$ *decides* the language
$$L(M) = \{ w \in \Sigma^* : M \text{ accepts } w \}.$$
A language $L$ is *decidable* if some decider decides it. Equivalently, the characteristic function $\chi_L$, with $\chi_L(w) = 1$ for $w \in L$ and $0$ otherwise, is a total [computable function](/computable-function/).

A language that is not decidable is *undecidable*; see [undecidability](/undecidability/).

The definition uses the single-tape deterministic machine, but the class does not change for the [multitape Turing machine](/multitape-turing-machine/), the random-access machine or any other general model; this is the robustness behind the [Church-Turing thesis](/church-turing-thesis/). For a [nondeterministic Turing machine](/nondeterministic-turing-machine/), a decider must halt on every branch for every input. Then the tree of computations on each input is finitely branching with no infinite path, so it is finite (König's lemma), and a deterministic machine can search all of it. So nondeterministic deciders decide the same languages.

**Problems and languages.** A *decision problem* is a set of instances with a yes or no answer. With a fixed computable encoding $\langle \cdot \rangle$ of instances by words, the problem becomes the language $\{ \langle x \rangle : x \text{ is a yes-instance} \}$. Different computable encodings give languages that are all decidable or all undecidable, since a machine can translate one encoding into the other. Words that are not valid encodings are treated as no-instances; a decider can recognize them.

**Decidable against computably enumerable.** A language is [computably enumerable](/recursively-enumerable-language/) (c.e.) if some machine accepts exactly its words, with no condition on the other inputs: on a word outside the language, the machine may reject or run forever. Every decidable language is c.e. The converse fails: the [halting problem](/halting-problem/) is c.e. and not decidable.

**Theorem (Post 1944).** A language $L$ is decidable if and only if both $L$ and its complement $\overline{L} = \Sigma^* \setminus L$ are c.e.

*Proof.* If $M$ decides $L$, then $M$ shows that $L$ is c.e., and $M$ with its accept and reject states exchanged decides $\overline{L}$, so $\overline{L}$ is c.e. too. Conversely, let $M_1$ accept exactly $L$ and $M_2$ accept exactly $\overline{L}$. On input $w$, a new machine runs one step of $M_1$ on $w$, then one step of $M_2$ on $w$, and repeats. It accepts if $M_1$ accepts and rejects if $M_2$ accepts. Every $w$ is in $L$ or in $\overline{L}$, so one of the two machines accepts $w$ after finitely many steps, and the new machine halts with the right answer. $\blacksquare$

So the decidable languages are the c.e. languages whose complements are also c.e. A c.e. language with a complement that is not c.e., such as the halting problem, is undecidable.

## Examples and non-examples

**Decidable languages.**

- Every finite language, and every cofinite one: the decider holds the list of words.
- Every [regular language](/regular-language/): simulate a [DFA](/deterministic-finite-automaton/), which halts after $|w|$ steps.
- Every [context-free language](/context-free-language/): the [CYK algorithm](/cyk-algorithm/) decides membership for a grammar in Chomsky normal form in $O(n^3)$ time.
- $\{0^k 1^k : k \ge 0\}$. The one-tape decider of the [Turing machine](/turing-machine/) page crosses off one $0$ and one $1$ in each pass. It accepts $0^k 1^k$ after $2k^2 + 2k + 1$ steps, and halts on every other word as well:

| input | $\varepsilon$ | $01$ | $0011$ | $000111$ | $0101$ | $001$ | $011$ | $10$ |
|---|---|---|---|---|---|---|---|---|
| result | accept | accept | accept | accept | reject | reject | reject | reject |
| steps | 1 | 5 | 13 | 25 | 5 | 8 | 5 | 1 |

- The binary representations of the primes: trial division by every $d$ with $2 \le d \le \sqrt{n}$ halts on every input. The [AKS test](/aks-primality-test/) decides the same language in polynomial time.
- The set of true sentences of [Presburger arithmetic](/presburger-arithmetic/), the first-order theory of $(\mathbb{N}, +)$, and of the first-order theory of the real field ([Tarski](/tarski-decidability-theorem/)). Such an algorithm for a theory is a [decision procedure](/decision-procedure/).
- $A_{\mathrm{DFA}} = \{ \langle B, w \rangle : B \text{ is a DFA that accepts } w \}$ and $A_{\mathrm{CFG}} = \{ \langle G, w \rangle : G \text{ is a CFG that generates } w \}$.
- The language of codes $\langle M \rangle$ of machines that halt on the empty input within $100$ steps: simulate $100$ steps.

**Decidable even when we cannot say which machine decides it.** Let $L_G = \{\varepsilon\}$ if every even number greater than $2$ is the sum of two primes, and $L_G = \emptyset$ otherwise. Both $\{\varepsilon\}$ and $\emptyset$ are decidable, so $L_G$ is decidable, though nobody knows which of the two machines decides it. In contrast, $\{ 1^n : n \text{ is even, } n \ge 4, n \text{ is the sum of two primes} \}$ is decidable by a search over all pairs of numbers below $n$, and here the decider is explicit.

**Undecidable languages.**

- The [halting problem](/halting-problem/) $\mathrm{HALT} = \{ \langle M, w \rangle : M \text{ halts on } w \}$ and the [acceptance problem](/acceptance-problem/) $A_{\mathrm{TM}} = \{ \langle M, w \rangle : M \text{ accepts } w \}$. Both are c.e. and not decidable.
- Their complements, which are not even c.e.
- $E_{\mathrm{TM}} = \{ \langle M \rangle : L(M) = \emptyset \}$ and every other nontrivial property of the language of a machine ([Rice's theorem](/rice-theorem/)).
- The [Post correspondence problem](/post-correspondence-problem/), [Hilbert's tenth problem](/hilberts-tenth-problem/) on integer roots of polynomial equations, the [word problem for groups](/word-problem-for-groups/), [Wang tiling](/wang-tiling-problem/), and [ambiguity](/cfg-ambiguity-undecidable/) and [equivalence](/cfg-equivalence-undecidable/) of context-free grammars.

**Decidable is not the same as feasible.** For every total computable function $t$ there is a decidable language that no machine decides within $t(n)$ steps on all inputs of length $n$. One such language: the set of codes $\langle M \rangle$ such that $M$ does not accept $\langle M \rangle$ within $t(|\langle M \rangle|)$ steps. A decider simulates $M$ for that many steps. If a machine $N$ decided this language within $t(n)$ steps, then $N$ on input $\langle N \rangle$ would halt within the bound, so $\langle N \rangle$ is in the language if and only if $N$ does not accept it, a contradiction. The [time hierarchy theorem](/time-hierarchy-theorem/) is the sharp form of this argument.

## Related definitions

- [Computably enumerable language](/recursively-enumerable-language/): accepted by a machine that may run forever on words outside the language. Decidable means c.e. and co-c.e.
- [Computable function](/computable-function/): $L$ is decidable if and only if $\chi_L$ is total computable. The partial and [primitive recursive](/primitive-recursive-function/) functions give the same decidable sets through characteristic functions, and the primitive recursive sets are a proper subclass.
- [Uncomputable function](/uncomputable-function/): the characteristic function of an undecidable language is one.
- **Closure.** The decidable languages are closed under complement, union, intersection, concatenation, Kleene star and inverse homomorphism. For concatenation, a decider tries every split of the input; for star, every split into nonempty pieces. They are not closed under projection: every c.e. language has the form $\{ x : \exists y\ \langle x, y \rangle \in D \}$ for a decidable $D$, where $y$ codes an accepting computation.
- [Many-one reducibility](/many-one-reducibility/): if $A \le_m B$ and $B$ is decidable, then $A$ is decidable. This is the main tool for proving [undecidability](/undecidability/).
- [Oracle Turing machine](/oracle-turing-machine/) and [Turing degrees](/turing-degrees/): the decidable languages form the lowest degree, $\mathbf{0}$.
- [Complexity class](/complexity-class/): classes such as [P](/p/) and [EXPTIME](/exptime/) are sets of decidable languages with a bound on the resources of the decider.

## References
