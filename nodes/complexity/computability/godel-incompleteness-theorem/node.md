---
tag: TX5KQW
kind: theorem
slug: godel-incompleteness-theorem
name: Gödel's incompleteness theorems
aliases:
- incompleteness theorems
area: complexity/computability
level: advanced
summary: A consistent, effectively axiomatized theory that contains basic arithmetic leaves some arithmetic sentences undecided, and if it is strong enough it cannot prove its own consistency.
prereqs: [halting-problem, godel-numbering, recursively-enumerable-language]
see_also: [godel-numbering, church-theorem, halting-problem, entscheidungsproblem, hilberts-tenth-problem, busy-beaver-function, kleene-recursion-theorem, presburger-arithmetic]
sources:
  - paper: doi:10.1007/BF01700692
    title: Kurt Gödel, Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I, Monatshefte für Mathematik und Physik 38 (1931)
    locator: pp. 173 to 198, Theorem VI (the first theorem) and Theorem XI (the second theorem)
  - paper: doi:10.2307/2269028
    title: J. Barkley Rosser, Extensions of some theorems of Gödel and Church, Journal of Symbolic Logic 1(3) (1936)
    locator: pp. 87 to 91
  - book: isbn:9780521701464
    title: George S. Boolos, John P. Burgess and Richard C. Jeffrey, Computability and Logic, fifth edition, Cambridge University Press, 2007
    locator: Chapter 15, Arithmetization; Chapter 16, Representability of recursive functions (Section 16.4, Robinson arithmetic); Chapter 17, Indefinability, undecidability, incompleteness; Chapter 18, The unprovability of consistency
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 6.2, Decidability of logical theories
  - paper: doi:10.1145/3427361.3427369
    title: Scott Aaronson, The busy beaver frontier, SIGACT News 51(3) (2020)
    locator: pp. 32 to 54
---

Gödel's incompleteness theorems are two results about formal theories of arithmetic, published by Kurt Gödel in 1931. The first says that a consistent theory whose axioms can be listed by a program, and which can express and prove some basic facts about the natural numbers, is *incomplete*: some sentence of arithmetic is neither provable nor refutable in it. The second says that such a theory, if it is strong enough, cannot prove the sentence that expresses its own consistency. Gödel's own proof of the first theorem needed a stronger hypothesis, $\omega$-consistency; Rosser showed in 1936 that plain consistency is enough. From the side of computation, the first theorem is a close relative of the undecidability of the [halting problem](/halting-problem/), and the proof given here comes from that link.

## Statement

Let $T$ be a first-order theory in the language of arithmetic, with $0$, successor, $+$, $\times$ and $<$. Robinson arithmetic $Q$ is the theory with a few simple axioms about these symbols and no induction.

**First incompleteness theorem (Gödel 1931, in Rosser's form of 1936).** Suppose $T$ is consistent, its set of axioms is c.e. (computably enumerable), and $T$ contains $Q$, or more generally interprets $Q$. Then there is a sentence $\theta$ such that $T$ proves neither $\theta$ nor $\neg\theta$.

**Second incompleteness theorem (Gödel 1931).** Suppose in addition that $T$ proves the basic properties of its own provability predicate, as Peano arithmetic does. Let $\mathrm{Con}_T$ be the arithmetic sentence that says "there is no proof of $0 = 1$ from the axioms of $T$". Then $T$ does not prove $\mathrm{Con}_T$.

A theory with a c.e. set of axioms has a c.e. set of theorems, since proofs can be listed and checked. Such a theory is often called *effectively axiomatized*.

## In plain words

A formal theory is a list of starting facts and fixed rules for deriving new facts. Mathematicians hoped to find one theory of whole numbers that could settle every question about them, a theory that never contradicts itself and whose starting facts a computer could list.

Gödel showed that this is impossible. Any such theory that knows a little arithmetic leaves some questions open: it can neither prove nor disprove them.

A computer view makes this plausible. If a theory settled every question, a computer could answer any question by searching its proofs until one side is proved. Since statements about numbers can describe programs, this would tell whether any program stops, and no computer can do that.

The second theorem says that such a theory cannot even prove that it never contradicts itself.

## Proof

We prove the first theorem through computation, following the method of Boolos, Burgess and Jeffrey, Chapter 17. Let $\varphi_e$ be the $e$-th partial computable function, and let
$$A = \{ e : \varphi_e(e) = 0 \}, \qquad B = \{ e : \varphi_e(e) = 1 \}.$$
These sets are disjoint and c.e.

**Lemma 1 (no computable separation).** There is no total computable function $D$ with $D(e) = 0$ for all $e \in A$ and $D(e) = 1$ for all $e \in B$.

*Proof.* Suppose $D$ is one. Then $g(e) = 1 - D(e)$ is total computable, so $g = \varphi_d$ for some $d$. If $D(d) = 0$, then $\varphi_d(d) = 1$, so $d \in B$ and $D(d) = 1$. If $D(d) = 1$, then $\varphi_d(d) = 0$, so $d \in A$ and $D(d) = 0$. Both cases are impossible. $\square$

**Lemma 2 ($Q$ separates $A$ and $B$).** There is a formula $\theta(x)$ such that $Q \vdash \theta(\bar e)$ for every $e \in A$ and $Q \vdash \neg\theta(\bar e)$ for every $e \in B$, where $\bar e$ is the numeral for $e$.

*Proof sketch.* Through the [Gödel numbering](/godel-numbering/) of machines, there are formulas $\alpha(x, s)$ and $\beta(x, s)$ with only bounded quantifiers that say "$\varphi_x(x)$ halts within $s$ steps with output $0$", and the same with output $1$. Two facts about $Q$ are proved in Boolos, Burgess and Jeffrey, Chapter 16: $Q$ proves every true sentence with only bounded quantifiers and every true sentence of the form $\exists s\, \psi$ with $\psi$ bounded; and for each numeral $\bar n$, $Q$ proves $\forall s\, (s \le \bar n \vee \bar n \le s)$ and $\forall s\, (s \le \bar n \to s = \bar 0 \vee \cdots \vee s = \bar n)$. Let
$$\theta(x) = \exists s\, \big( \alpha(x, s) \wedge \forall t \le s\ \neg\beta(x, t) \big).$$
If $e \in A$, then $\theta(\bar e)$ is a true sentence of the form $\exists s\, \psi$ with $\psi$ bounded, so $Q$ proves it. If $e \in B$, say $\varphi_e(e)$ halts at step $n$ with output $1$, then $Q$ proves $\beta(\bar e, \bar n)$ and $\neg\alpha(\bar e, \bar m)$ for each $m \le n$. Reason in $Q$ about any $s$. If $s \le \bar n$, then $s$ is one of $\bar 0, \ldots, \bar n$, so $\neg\alpha(\bar e, s)$. If $\bar n \le s$, then $t = \bar n$ is a $t \le s$ with $\beta(\bar e, t)$. In both cases the body of $\theta$ fails, so $Q \vdash \neg\theta(\bar e)$. $\square$

**Theorem.** If $T$ is consistent, has a c.e. set of axioms and contains $Q$, then for some $e$, $T$ proves neither $\theta(\bar e)$ nor $\neg\theta(\bar e)$.

*Proof.* Suppose that for every $e$, $T$ proves $\theta(\bar e)$ or $\neg\theta(\bar e)$. Define $D(e)$ as follows: list the theorems of $T$, stop at the first one that is $\theta(\bar e)$ or $\neg\theta(\bar e)$, and output $0$ in the first case and $1$ in the second. By assumption the search always stops, so $D$ is total computable. If $e \in A$, then $T \vdash \theta(\bar e)$ by Lemma 2, and $T \nvdash \neg\theta(\bar e)$ by consistency, so $D(e) = 0$. In the same way $D(e) = 1$ for $e \in B$. This contradicts Lemma 1. $\blacksquare$

**Gödel's sentence.** Gödel's own proof builds a sentence $G$ that says of itself "I am not provable in $T$". By the diagonal lemma, a form of [Kleene's recursion theorem](/kleene-recursion-theorem/) for formulas, there is a sentence $G$ with $T \vdash G \leftrightarrow \neg \mathrm{Prov}_T(\ulcorner G \urcorner)$, where $\mathrm{Prov}_T(y)$ says "$y$ is the code of a theorem of $T$". If $T \vdash G$, then $T$ proves the true statement $\mathrm{Prov}_T(\ulcorner G \urcorner)$, and so $\neg G$, which makes $T$ inconsistent. So a consistent $T$ does not prove $G$, and $G$ is true. To show that $T$ does not prove $\neg G$ either, Gödel used $\omega$-consistency. Rosser's sentence, "for every proof of me there is a shorter proof of my negation", needs only consistency, just as $\theta$ above uses the race between $\alpha$ and $\beta$.

**The second theorem.** The argument "if $T$ is consistent, then $T$ does not prove $G$" uses only elementary reasoning about proofs, so it can be carried out inside $T$ when $T$ is strong enough. This gives $T \vdash \mathrm{Con}_T \to \neg \mathrm{Prov}_T(\ulcorner G \urcorner)$, and so $T \vdash \mathrm{Con}_T \to G$. If $T$ proved $\mathrm{Con}_T$, it would prove $G$, which the first part rules out. The conditions that make this work were stated by Hilbert and Bernays and by Löb; Boolos, Burgess and Jeffrey, Chapter 18, give the details.

## Consequences

- **Hilbert's program.** Hilbert hoped to prove the consistency of all of mathematics by finite, elementary means. The second theorem shows that no theory of this kind proves even its own consistency, let alone that of stronger theories.
- **Truth is not c.e.** The set of true sentences of arithmetic is not c.e. Otherwise it would be a consistent, complete theory with a c.e. set of axioms that contains $Q$.
- **Undecidability.** Every consistent theory that contains $Q$ is undecidable. With Lemma 2, a decision procedure for $T$ would give a computable separation of $A$ and $B$. Since $Q$ has finitely many axioms, this gives another proof of [Church's theorem](/church-theorem/).
- **Concrete undecided sentences.** By the MRDP theorem behind [Hilbert's tenth problem](/hilberts-tenth-problem/), for each such theory there is a polynomial equation with no solution in natural numbers for which the theory cannot prove that there is none. In the same way, a theory of this kind that proves only true sentences of arithmetic proves the value of the [busy beaver function](/busy-beaver-function/) for only finitely many $n$. Yedidia and Aaronson built a Turing machine with $7918$ states that halts if and only if ZFC set theory is inconsistent; if ZFC is consistent, it cannot prove that this machine runs forever, and so it cannot determine the busy beaver value for $7918$ states (Aaronson 2020).

## Tightness

Each hypothesis is needed.

- **Consistency.** An inconsistent theory proves every sentence, so it is complete.
- **Listable axioms.** True arithmetic, the set of all true sentences, is consistent and complete, and it contains $Q$. Its axioms are not c.e.
- **Enough arithmetic.** [Presburger arithmetic](/presburger-arithmetic/), the theory of $(\mathbb{N}, 0, 1, +)$ without multiplication, is consistent, complete and decidable. So is the theory of real closed fields, by [Tarski's theorem](/tarski-decidability-theorem/). These theories cannot express the run of a machine.
- **$\omega$-consistency versus consistency.** Gödel's sentence $G$ needs $\omega$-consistency to be undecided, but Rosser's sentence, and $\theta$ above, need only consistency.
- **The second theorem needs more than $Q$.** The derivability conditions on $\mathrm{Prov}_T$ require some induction; Peano arithmetic, and much weaker theories, satisfy them.

## History

Gödel announced the first theorem in September 1930 at a conference in Königsberg, and published both theorems in 1931, in a paper whose method of coding formulas by numbers became the [Gödel numbering](/godel-numbering/) of computability theory. He proved the first theorem for $\omega$-consistent theories and sketched the second. Rosser (1936) removed $\omega$-consistency. Church and Turing's work of 1936 on the [Entscheidungsproblem](/entscheidungsproblem/) gave the notion of computation that makes "c.e. set of axioms" precise, and with it the general form of the theorems stated above. The detailed proof of the second theorem appeared in the second volume of Hilbert and Bernays (1939).

## References
