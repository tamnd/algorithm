---
tag: E43HJF
kind: definition
slug: recursively-enumerable-language
name: Recursively enumerable language
aliases:
- RE language
- semi-decidable language
- Turing-recognizable language
- computably enumerable language
area: complexity/computability
level: intro
summary: A language is computably enumerable if a Turing machine accepts exactly its words and may run forever on other words. Equivalently, some machine lists its words.
prereqs: [decidable-language]
see_also: [decidable-language, halting-problem, acceptance-problem, many-one-reducibility, arithmetical-hierarchy, computable-function, rice-theorem, post-problem]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 3 (Turing-recognizable languages and enumerators); Section 4.2 (a Turing-unrecognizable language)
  - paper: doi:10.1090/S0002-9904-1944-08111-1
    title: Emil L. Post, Recursively enumerable sets of positive integers and their decision problems, Bulletin of the American Mathematical Society 50(5) (1944)
    locator: pp. 284 to 316
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.2 (recursively enumerable languages and their complements)
  - book: isbn:9780262680523
    title: Hartley Rogers Jr., Theory of Recursive Functions and Effective Computability, MIT Press (reprint of the McGraw-Hill edition of 1967)
    locator: Chapter 5 (recursive and recursively enumerable sets)
  - book: isbn:9783642319327
    title: Robert I. Soare, Turing Computability, Theory and Applications, Springer, 2016
    locator: Chapter 2, Computably Enumerable Sets
---

A language $L \subseteq \Sigma^*$ is *recursively enumerable* if some [Turing machine](/turing-machine/) accepts every word of $L$ and accepts no other word; on a word outside $L$ the machine may reject or run forever. The modern name is *computably enumerable*, written c.e., and this page uses it from here on. Other names are *semi-decidable* and *Turing-recognizable*. The name comes from an equivalent form: a language is c.e. exactly when a machine can print a list of its words. Every [decidable language](/decidable-language/) is c.e., but the [halting problem](/halting-problem/) is c.e. and not decidable, so the two classes differ.

## Definition

A language $L \subseteq \Sigma^*$ is *c.e.* if $L = L(M)$ for some Turing machine $M$, where
$$L(M) = \{ w \in \Sigma^* : M \text{ accepts } w \}.$$
Such an $M$ *recognizes* $L$. Nothing is required on inputs outside $L$. A language is *co-c.e.* if its complement $\overline{L} = \Sigma^* \setminus L$ is c.e.

For subsets of $\mathbb{N}$, with the [Gödel numbering](/godel-numbering/) of machines, the c.e. sets are exactly the sets $W_e = \mathrm{dom}(\varphi_e)$, the domains of the partial [computable functions](/computable-function/). The list $W_0, W_1, W_2, \ldots$ contains every c.e. set.

**Equivalent forms.** For a language $L$ the following are equivalent.

1. $L = L(M)$ for a Turing machine $M$.
2. $L$ is the domain of a partial computable function.
3. *Enumerator.* Some machine with an output tape, started on an empty input, prints words one after the other, so that the words printed are exactly the words of $L$. Repetitions are allowed and the order is arbitrary.
4. $L = \emptyset$, or $L$ is the range of a total computable function $f : \mathbb{N} \to \Sigma^*$.
5. *Projection.* There is a decidable language $D$ with $L = \{ x : \exists y\ \langle x, y \rangle \in D \}$.

*Proof.* Let $w_0, w_1, w_2, \ldots$ be the words of $\Sigma^*$ in shortlex order.

- (1) implies (2): change every move into the reject state into a move to a state that loops forever. The new machine halts exactly on the words of $L$, so it computes a partial function with domain $L$.
- (2) implies (1): a machine that computes a partial function halts in its accept state exactly on the domain, so it recognizes the domain.
- (1) implies (3), by *dovetailing*: in stage $r = 0, 1, 2, \ldots$, run $M$ for $r$ steps on each of $w_0, \ldots, w_r$, and print each word that $M$ accepts within those steps. A word $w_i$ that $M$ accepts in $t$ steps is printed in stage $\max(i, t)$, and in every stage after it. Running $M$ on one word at a time would fail, since $M$ may run forever on a word outside $L$ and block the rest.
- (3) implies (1): on input $w$, run the enumerator and accept when it prints $w$.
- (1) implies (5): let $D = \{ \langle x, t \rangle : M \text{ accepts } x \text{ within } t \text{ steps} \}$. A machine decides $D$ by simulating $t$ steps.
- (5) implies (1): on input $x$, test $\langle x, y \rangle \in D$ for $y = w_0, w_1, \ldots$ and accept when a test succeeds.
- (1) implies (4): if $L$ is nonempty, fix $a \in L$ and let $f(\pi(i, t)) = w_i$ if $M$ accepts $w_i$ within $t$ steps, and $f(\pi(i, t)) = a$ otherwise, where $\pi$ is the Cantor pairing function. Then $f$ is total and its range is $L$.
- (4) implies (1): on input $w$, compute $f(0), f(1), \ldots$ and accept when a value equals $w$. $\blacksquare$

**Ordered listings.** An infinite language $L$ is decidable if and only if some enumerator lists it in strictly increasing shortlex order. If $L$ is decidable, test $w_0, w_1, \ldots$ in turn and print the members. Conversely, given such a listing, decide $w$ by running the enumerator until it prints $w$ (accept) or a word after $w$ in shortlex order (reject); since $L$ is infinite, one of the two happens.

**Decidable and c.e.** By Post's theorem on the [decidable language](/decidable-language/) page, $L$ is decidable if and only if $L$ is c.e. and co-c.e. In the [arithmetical hierarchy](/arithmetical-hierarchy/) the c.e. sets are the $\Sigma_1$ sets, the co-c.e. sets the $\Pi_1$ sets, and the decidable sets the $\Delta_1 = \Sigma_1 \cap \Pi_1$ sets.

## Examples and non-examples

**Dovetailing on a small machine.** Take the decider for $\{0^k 1^k\}$ of the [Turing machine](/turing-machine/) page and replace its reject moves by moves that run right forever. The new machine recognizes the same language and halts only on its members. It accepts $\varepsilon$ in $1$ step, $01$ in $5$ steps and $0011$ in $13$ steps. These words have shortlex indices $0$, $4$ and $18$. The enumerator above prints $\varepsilon$ first in stage $1$, $01$ in stage $5$ and $0011$ in stage $\max(18, 13) = 18$. It never waits on a word such as $10$, where the machine runs forever.

**C.e. languages that are not decidable.**

- The [halting problem](/halting-problem/) $\mathrm{HALT} = \{ \langle M, w \rangle : M \text{ halts on } w \}$, and its diagonal form $K = \{ e : \varphi_e(e) \text{ is defined} \}$. A [universal Turing machine](/universal-turing-machine/) recognizes them.
- The [acceptance problem](/acceptance-problem/) $A_{\mathrm{TM}} = \{ \langle M, w \rangle : M \text{ accepts } w \}$.
- $\{ \langle M \rangle : L(M) \neq \emptyset \}$: dovetail $M$ over all inputs and accept when one run accepts.
- The theorems of a first-order theory with a decidable set of axioms, such as Peano arithmetic: list all proofs and check each one. The set of valid first-order sentences is c.e. by the completeness theorem, and not decidable by [Church's theorem](/church-theorem/); see also [Gödel's incompleteness theorem](/godel-incompleteness-theorem/).
- The solvable instances of the [Post correspondence problem](/post-correspondence-problem/): try all sequences of indices.
- The polynomial equations with an integer solution ([Hilbert's tenth problem](/hilberts-tenth-problem/)): try all integer tuples.
- The [ambiguous context-free grammars](/cfg-ambiguity-undecidable/): search for a word with two parse trees.

**Languages that are not c.e.**

- The complements $\overline{\mathrm{HALT}}$, $\overline{K}$ and $\overline{A_{\mathrm{TM}}}$. Each is the complement of a c.e. language that is not decidable; if it were c.e., Post's theorem would make the original language decidable.
- $E_{\mathrm{TM}} = \{ \langle M \rangle : L(M) = \emptyset \}$, for the same reason: its complement is c.e. (above), and $E_{\mathrm{TM}}$ is undecidable by [Rice's theorem](/rice-theorem/).
- $\mathrm{TOT} = \{ \langle M \rangle : M \text{ halts on every input} \}$ is neither c.e. nor co-c.e. For the first claim, map $\langle M, w \rangle$ to a machine $M'$ that on input $x$ runs $M$ on $w$ for $|x|$ steps, runs forever if $M$ has halted, and halts otherwise. Then $M'$ halts on every input if and only if $M$ does not halt on $w$, so $\overline{\mathrm{HALT}} \le_m \mathrm{TOT}$. For the second, map $\langle M, w \rangle$ to a machine that ignores its input and runs $M$ on $w$; this gives $\mathrm{HALT} \le_m \mathrm{TOT}$, so $\overline{\mathrm{HALT}} \le_m \overline{\mathrm{TOT}}$. TOT is $\Pi_2$-complete in the [arithmetical hierarchy](/arithmetical-hierarchy/).
- $\mathrm{EQ}_{\mathrm{TM}} = \{ \langle M_1, M_2 \rangle : L(M_1) = L(M_2) \}$ is neither c.e. nor co-c.e.
- By a count, all but countably many languages: there are only countably many machines ([countability](/countability/)).

**Closure properties.** The c.e. languages are closed under union, intersection, concatenation, Kleene star, homomorphism and inverse homomorphism. For union, run the two recognizers in alternating steps and accept when either accepts; running one after the other would fail if the first runs forever. For intersection, run one after the other. For concatenation and star, dovetail over all splits of the input. The c.e. languages are *not* closed under complement: $\mathrm{HALT}$ is c.e. and $\overline{\mathrm{HALT}}$ is not.

## Related definitions

- [Decidable language](/decidable-language/): a c.e. language whose complement is also c.e. The two notions are easy to mix up, and many wrong proofs assume that a recognizer halts on every input.
- [Computable function](/computable-function/): the c.e. sets are the domains, and also the ranges, of the partial computable functions.
- [Many-one reducibility](/many-one-reducibility/): if $A \le_m B$ and $B$ is c.e., then $A$ is c.e. $\mathrm{HALT}$, $K$ and $A_{\mathrm{TM}}$ are complete for the c.e. sets under $\le_m$.
- [Post's problem](/post-problem/) and [Turing degrees](/turing-degrees/): the c.e. sets fall into Turing degrees between $\mathbf{0}$ (the decidable sets) and $\mathbf{0}'$ (the degree of $K$), and there are degrees strictly between.
- [Arithmetical hierarchy](/arithmetical-hierarchy/): c.e. is the level $\Sigma_1$.
- [Countability](/countability/): every language is countable, but only countably many languages are c.e. "Enumerable" in the name means listable by a machine, not just countable.

## References
