---
tag: TRVFAJ
kind: theorem
slug: rice-theorem
name: Rice's theorem
aliases:
- Rice's theorem on nontrivial semantic properties
area: complexity/computability
level: core
summary: Every nontrivial property of the language of a Turing machine is undecidable. Properties of the machine text, such as its number of states, are not covered and can be decidable.
prereqs: [halting-problem, many-one-reducibility]
see_also: [halting-problem, acceptance-problem, many-one-reducibility, undecidability, full-employment-theorem, may-alias-undecidability, abstract-interpretation, cfg-equivalence-undecidable]
sources:
  - paper: doi:10.1090/S0002-9947-1953-0053041-6
    title: Henry Gordon Rice, Classes of recursively enumerable sets and their decision problems, Transactions of the American Mathematical Society 74(2) (1953)
    locator: pp. 358 to 366
  - paper: doi:10.2307/2269105
    title: Henry Gordon Rice, On completely recursively enumerable classes and their key arrays, Journal of Symbolic Logic 21(3) (1956)
    locator: pp. 304 to 308
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 5, Reducibility (Rice's theorem is given as a problem in this chapter)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 9.3 (Rice's theorem and properties of the recursively enumerable languages)
---

Rice's theorem says that no algorithm can decide any nontrivial property of *what* a program computes. For a property $P$ of languages, the question "given a [Turing machine](/turing-machine/) $M$, does $L(M)$ have property $P$?" is [undecidable](/undecidability/) unless $P$ holds for all languages of machines or for none. So emptiness, finiteness, regularity, equality with a fixed language, and every other such property cannot be decided from the code. Rice proved it in 1953. The theorem is about the language, not about the machine text: "$M$ has five states" is a property of the code and is decidable.

## Statement

A *property of c.e. languages* is a set $P$ of [computably enumerable](/recursively-enumerable-language/) languages. It is *nontrivial* if some machine has a language in $P$ and some machine has a language not in $P$. Every word is taken to be the code of a machine: a word that is not a valid code stands for a fixed machine that rejects every input. Let
$$L_P = \{ \langle M \rangle : L(M) \in P \}.$$

**Theorem (Rice 1953).** If $P$ is a nontrivial property of c.e. languages, then $L_P$ is not [decidable](/decidable-language/). More precisely:

- if $\emptyset \notin P$, then $A_{\mathrm{TM}} \le_m L_P$, so $L_P$ is not co-c.e.;
- if $\emptyset \in P$, then $\overline{A_{\mathrm{TM}}} \le_m L_P$, so $L_P$ is not c.e.

**Index-set form.** For a set $\mathcal{F}$ of unary partial computable functions, the *index set* $\{ e : \varphi_e \in \mathcal{F} \}$ is decidable if and only if $\mathcal{F}$ is empty or contains every partial computable function. Here $\varphi_e$ is the function computed by the machine with index $e$ in a [Gödel numbering](/godel-numbering/). The proof is the same as below, with "computes the function" in place of "accepts the language".

A property in either sense is *semantic*: if two machines have the same language (or compute the same function), both have the property or neither has it. Rice's theorem is about semantic properties only.

## In plain words

Take any yes-or-no question about the behavior of a program, as opposed to its text: does it ever say yes, does it say yes to finitely many inputs, does it do the same as some other program. Rice's theorem says that if some programs give the answer yes and some give no, then no tool can answer the question correctly for every program.

The proof shows that a tool for such a question could be used to solve the halting problem. Given a program and an input, build a new program that first runs the given program on the given input, and only then behaves like a program known to have the property. The new program has the property exactly when the first run ends with yes.

Questions about the text, such as the number of lines, or about a fixed number of steps, are not covered.

## Proof

Let $P$ be a nontrivial property of c.e. languages.

**Case $\emptyset \notin P$.** Since $P$ is nontrivial, there is a machine $M_L$ with $L = L(M_L) \in P$. We give a [many-one reduction](/many-one-reducibility/) from the [acceptance problem](/acceptance-problem/) $A_{\mathrm{TM}} = \{ \langle M, w \rangle : M \text{ accepts } w \}$ to $L_P$.

*The map.* For a valid pair $\langle M, w \rangle$, let $f(\langle M, w \rangle) = \langle M' \rangle$, where $M'$ is the machine that on input $x$:

1. saves $x$ on a second track, writes $w$, and runs $M$ on $w$;
2. if $M$ rejects $w$, rejects;
3. if $M$ accepts $w$, runs $M_L$ on $x$ and accepts if $M_L$ accepts.

If $M$ runs forever on $w$, then $M'$ runs forever in step 1. For a word that is not a valid pair, let $f$ output the code of a fixed machine $M_\emptyset$ that rejects every input; then $f(\text{word}) \notin L_P$, since $L(M_\emptyset) = \emptyset \notin P$, and the word is not in $A_{\mathrm{TM}}$ either.

*The map is total computable.* $M'$ is built from the text of $M$, the word $w$ and the fixed text of $M_L$: a block of $|w|$ states that writes $w$, a copy of the rules of $M$ with its accept state renamed to the start state of the copy of $M_L$, and its reject state kept. Nothing is run. With the standard code of the [Gödel numbering](/godel-numbering/) page, where a state number is written in unary, $M'$ has $O(n)$ rules of length $O(n)$ for $n = |\langle M, w \rangle|$, so $|\langle M' \rangle| = O(n^2)$, and $f$ takes polynomial time.

*If $\langle M, w \rangle \in A_{\mathrm{TM}}$, then $f(\langle M, w \rangle) \in L_P$.* If $M$ accepts $w$, then on every input $x$, $M'$ reaches step 3 and accepts $x$ if and only if $M_L$ accepts $x$. So $L(M') = L \in P$.

*If $f(\langle M, w \rangle) \in L_P$, then $\langle M, w \rangle \in A_{\mathrm{TM}}$.* The input is a valid pair, since otherwise $f$ outputs $\langle M_\emptyset \rangle \notin L_P$. Suppose $M$ does not accept $w$. Then $M$ rejects $w$ or runs forever on it, and in both cases $M'$ accepts no input: it rejects in step 2 or never leaves step 1. So $L(M') = \emptyset$, which is not in $P$, and $\langle M' \rangle \notin L_P$, a contradiction. So $M$ accepts $w$.

Hence $A_{\mathrm{TM}} \le_m L_P$. Since $A_{\mathrm{TM}}$ is undecidable and its complement is not c.e., $L_P$ is undecidable and, by the complement property of $\le_m$, not co-c.e.

**Case $\emptyset \in P$.** Let $\overline{P}$ be the set of c.e. languages not in $P$. It is nontrivial and does not contain $\emptyset$, so the first case gives $A_{\mathrm{TM}} \le_m L_{\overline{P}}$. Since every word codes a machine, $L_{\overline{P}}$ is the complement of $L_P$, and so $\overline{A_{\mathrm{TM}}} \le_m L_P$. The complement of $A_{\mathrm{TM}}$ is not c.e., so $L_P$ is not c.e., and in particular not decidable. $\blacksquare$

**Worked example.** Let $P = \{ L : 01 \in L \}$, so $\emptyset \notin P$. Let $M_L$ be the decider for $\{0^k 1^k\}$ of the [Turing machine](/turing-machine/) page; its language contains $01$, so it is in $P$. Take the same machine as $M$.

- For $w = 0011$, $M$ accepts after 13 steps. Then $M'$, on any input $x$, gets past step 1 and behaves like $M_L$. On $x = 01$ it then accepts, after $5$ further steps of $M_L$. So $L(M') = \{0^k 1^k\} \in P$, and $f$ maps this yes-instance to a yes-instance.
- For $w = 001$, $M$ rejects after 8 steps. Then $M'$ rejects every input in step 2, so $L(M') = \emptyset \notin P$, and $f$ maps this no-instance to a no-instance.

## Consequences

**Undecidable properties of machines.** Each of these sets of codes is undecidable, since each property is semantic and nontrivial:

- $E_{\mathrm{TM}} = \{ \langle M \rangle : L(M) = \emptyset \}$. Here $\emptyset \in P$, so $E_{\mathrm{TM}}$ is not even c.e.
- $\{ \langle M \rangle : L(M) \ne \emptyset \}$, which is c.e. but not decidable.
- $\{ \langle M \rangle : L(M) \text{ is finite} \}$, $\{ \langle M \rangle : L(M) \text{ is regular} \}$, $\{ \langle M \rangle : L(M) \text{ is context-free} \}$ and $\{ \langle M \rangle : L(M) = \Sigma^* \}$.
- $\{ \langle M \rangle : L(M) = L(M_0) \}$ for any fixed machine $M_0$, and so the equivalence problem $\{ \langle M_1, M_2 \rangle : L(M_1) = L(M_2) \}$.
- In the index-set form, $\{ e : \varphi_e \text{ is total} \}$ and $\{ e : \varphi_e \text{ is a constant function} \}$.

**The Rice-Shapiro theorem.** Rice's theorem says when an index set is decidable. The Rice-Shapiro theorem says when the set $\{ e : W_e \in P \}$, for a property $P$ of c.e. sets, is c.e.: exactly when there is a c.e. list of finite sets $D_0, D_1, \ldots$ such that a c.e. set $W$ is in $P$ if and only if $D_i \subseteq W$ for some $i$. So a c.e. property is closed under supersets and is decided by finite parts. For example, "$W$ is nonempty" is c.e., while "$W$ is finite" and "$W = \mathbb{N}$" are not. Rice conjectured this characterization in 1953, and it was proved by Myhill, McNaughton and Shapiro; Rice (1956) studied the same classes.

**Program analysis.** By the [Church-Turing thesis](/church-turing-thesis/), the theorem holds for programs in every general programming language. Exact answers to questions such as "is this code reachable", "is this variable always constant", "can these two pointers alias" ([may-alias undecidability](/may-alias-undecidability/)) or "do these two programs compute the same function" are impossible in general. Practical analyzers answer a safe approximation, as in [abstract interpretation](/abstract-interpretation/), and the [full employment theorem](/full-employment-theorem/) is a related consequence for optimizing compilers.

## Tightness

**Trivial properties are decidable.** If $P$ contains every c.e. language, $L_P$ is the set of all codes; if $P$ is empty, $L_P = \emptyset$. Both are decidable, so the condition "nontrivial" cannot be dropped.

**The property must be semantic.** Properties of the machine text, or of its behavior within a bound, are outside the theorem, and many are decidable:

- "$M$ has exactly five states": read the code.
- "$M$ halts on the empty input within $100$ steps": simulate $100$ steps. Two machines with the same language can differ here, so the property is not semantic.
- "$M$ moves its head left at some time during its run on $w$": decidable. If $M$ makes no left move in its first $|w| + |Q| + 1$ steps, then after $|w|$ steps its head is past the input and reads only blanks, and within $|Q| + 1$ more steps a state repeats; from then on its moves repeat with a period, all to the right. So simulating $|w| + |Q| + 1$ steps decides the question.
- "$M$ accepts its own code $\langle M \rangle$" is undecidable, but Rice's theorem does not prove it, since the property depends on the code. A [diagonalization argument](/diagonalization-argument/) proves it.
- "$M$ runs in polynomial time" is a property of the running time, not of $L(M)$, so Rice's theorem says nothing about it.

**The model must be general.** Rice's theorem needs every Turing machine to be allowed. For weaker models, many semantic properties are decidable. For finite automata, emptiness, finiteness and equivalence are decidable. For context-free grammars, emptiness and finiteness are decidable, but equivalence is not ([undecidability of CFG equivalence](/cfg-equivalence-undecidable/)). So for each restricted model the line between decidable and undecidable properties must be found separately.

**The two cases are sharp.** When $\emptyset \notin P$, $L_P$ can be c.e., as for non-emptiness, so "not co-c.e." cannot be improved to "not c.e.". When $\emptyset \in P$, $L_P$ can be co-c.e., as for emptiness.

## History

Henry Gordon Rice proved the theorem in 1953, in his paper on classes of recursively enumerable sets and their decision problems, in the index-set form for classes of c.e. sets. In the same paper he conjectured the characterization of the classes with a c.e. index set, which is now called the Rice-Shapiro theorem. Rice returned to these classes in 1956. Textbooks such as Hopcroft, Motwani and Ullman (Section 9.3) state the theorem for languages of Turing machines and prove it by the reduction from $A_{\mathrm{TM}}$ above; Sipser gives it as a problem in Chapter 5.

## References
