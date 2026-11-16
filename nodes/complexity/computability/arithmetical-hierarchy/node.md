---
tag: W7YDBF
kind: concept
slug: arithmetical-hierarchy
name: Arithmetical hierarchy
aliases:
- Kleene-Mostowski hierarchy
area: complexity/computability
level: advanced
summary: "A classification of sets of numbers by the number of alternating unbounded quantifiers in front of a decidable relation. Level 1 is the c.e. sets; totality of programs is complete for Pi_2."
prereqs: [recursively-enumerable-language, many-one-reducibility]
see_also: [posts-theorem, turing-jump, turing-degrees, polynomial-hierarchy, halting-problem, rice-theorem, godel-incompleteness-theorem, s-m-n-theorem]
sources:
  - paper: doi:10.1090/S0002-9947-1943-0007371-8
    title: "Stephen C. Kleene, Recursive predicates and quantifiers, Transactions of the American Mathematical Society 53(1) (1943)"
    locator: "pp. 41 to 73 (the quantifier forms and the hierarchy theorem)"
  - paper: doi:10.4064/fm-34-1-81-112
    title: "Andrzej Mostowski, On definable sets of positive integers, Fundamenta Mathematicae 34 (1947)"
    locator: pp. 81 to 112
  - book: isbn:9783642319327
    title: "Robert I. Soare, Turing Computability, Theory and Applications, Springer, 2016"
    locator: "Chapter 4, The Arithmetical Hierarchy, Section 4.1, Levels in the Arithmetical Hierarchy"
---

The arithmetical hierarchy sorts sets of natural numbers by how many alternating unbounded quantifiers their definition needs. A set is $\Sigma_n$ if it can be written as "there is a $y_1$ such that for all $y_2$ there is a $y_3$ ..." with $n$ alternating quantifiers in front of a [decidable](/decidable-language/) relation, and $\Pi_n$ if the first quantifier is "for all". The $\Sigma_1$ sets are the computably enumerable (c.e.) sets, such as the [halting](/halting-problem/) set $K$. The set of programs that halt on every input needs two quantifiers and is complete for $\Pi_2$. Kleene (1943) and Mostowski (1947) introduced the hierarchy independently, and Kleene proved that each level contains new sets. By [Post's theorem](/posts-theorem/), the levels match the iterates of the [Turing jump](/turing-jump/): $\Sigma_{n+1}$ is the class of sets that are c.e. relative to $\emptyset^{(n)}$. The [polynomial hierarchy](/polynomial-hierarchy/) of complexity theory is defined in the same way with quantifiers bounded by a polynomial.

## In plain words

Some questions about numbers can be settled by a search that stops when it finds an answer: "does this program ever halt?" A yes answer can be confirmed by waiting long enough, but a no answer cannot. Other questions need two searches inside each other: "does this program halt on every input?" For each input you must search for the halting step, and there are infinitely many inputs.

The hierarchy counts these nested searches, and how they alternate between "there is" and "for all". Each extra level allows strictly harder questions. Many famous open problems in mathematics sit on the first or second level.

## The idea

**Definition.** Let $R$ range over decidable relations on $\mathbb{N}$. A set $A \subseteq \mathbb{N}$ (or a relation) is

- $\Sigma_0 = \Pi_0$ if it is decidable;
- $\Sigma_n$, for $n \ge 1$, if there is a decidable $R$ with
$$x \in A \iff \exists y_1\, \forall y_2\, \exists y_3 \cdots Q y_n\; R(x, y_1, \ldots, y_n),$$
where the quantifiers alternate and $Q$ is $\exists$ for odd $n$ and $\forall$ for even $n$;
- $\Pi_n$ if its complement is $\Sigma_n$, which means a form that starts with $\forall$;
- $\Delta_n$ if it is both $\Sigma_n$ and $\Pi_n$.

A set is *arithmetical* if it is $\Sigma_n$ for some $n$. Equivalently, the arithmetical sets are the sets definable by a formula of first-order arithmetic in the language $0, 1, +, \times, <$; the class does not change if the matrix $R$ is required to be primitive recursive, or to use only bounded quantifiers.

**Rules for counting quantifiers.**

- Two quantifiers of the same kind in a row count as one: $\exists y\, \exists z\, R(x, y, z)$ is $\exists w\, R(x, \pi_1(w), \pi_2(w))$ with a computable pairing function $\pi$.
- Bounded quantifiers $\exists z < y$ and $\forall z < y$ do not count, when they stand next to an unbounded quantifier.
- $\Sigma_n$ and $\Pi_n$ are closed under $\wedge$, $\vee$, bounded quantifiers and [many-one reductions](/many-one-reducibility/). $\Sigma_n$ is closed under $\exists$, and $\Pi_n$ under $\forall$.
- Both $\Sigma_n$ and $\Pi_n$ are contained in $\Delta_{n+1}$, by adding a dummy quantifier.

**The first levels.**

- $\Delta_1$ is the class of decidable sets, and $\Sigma_1$ is the class of c.e. sets. A c.e. set is $\{ x : \exists s\, [x \text{ is listed by stage } s] \}$, and this is a $\Sigma_1$ form. The fact that a set is decidable when both it and its complement are c.e. is the statement $\Delta_1 = \Sigma_1 \cap \Pi_1$.
- $\Delta_2$ is the class of sets computable from $\emptyset'$, by Post's theorem and the limit lemma of the [Turing jump](/turing-jump/) page.

**Hierarchy theorem.** For every $n \ge 1$ there is a set in $\Sigma_n$ that is not in $\Pi_n$, so
$$\Delta_n \subsetneq \Sigma_n \subsetneq \Delta_{n+1} \quad \text{and} \quad \Sigma_n \ne \Pi_n.$$
The proof is a diagonal argument. There is a universal $\Sigma_n$ relation $U_n(e, x)$, one $\Sigma_n$ form with an index parameter $e$ that lists all $\Sigma_n$ sets. The set $D = \{ x : U_n(x, x) \}$ is $\Sigma_n$. If its complement were $\Sigma_n$, it would equal $\{ x : U_n(e, x) \}$ for some $e$, and then $e \in D$ if and only if $e \notin D$.

**Complete sets.** A set is $\Sigma_n$-complete if it is $\Sigma_n$ and every $\Sigma_n$ set reduces to it by a many-one reduction. Writing $W_{e,s}$ for the finite part of $W_e$ listed within $s$ steps, a decidable relation of $e$, $x$ and $s$:

| set | quantifier form | complete for |
| --- | --- | --- |
| $K = \{ e : \varphi_e(e) \text{ halts} \}$ | $\exists s\, [e \in W_{e,s}]$ | $\Sigma_1$ |
| $\mathrm{EMP} = \{ e : W_e = \emptyset \}$ | $\forall x\, \forall s\, [x \notin W_{e,s}]$ | $\Pi_1$ |
| $\mathrm{FIN} = \{ e : W_e \text{ finite} \}$ | $\exists n\, \forall x\, \forall s\, [x > n \Rightarrow x \notin W_{e,s}]$ | $\Sigma_2$ |
| $\mathrm{TOT} = \{ e : \varphi_e \text{ total} \}$ | $\forall x\, \exists s\, [x \in W_{e,s}]$ | $\Pi_2$ |
| $\mathrm{INF} = \{ e : W_e \text{ infinite} \}$ | $\forall n\, \exists x\, \exists s\, [x > n \wedge x \in W_{e,s}]$ | $\Pi_2$ |
| $\mathrm{COF} = \{ e : W_e \text{ cofinite} \}$ | $\exists n\, \forall x\, \exists s\, [x > n \Rightarrow x \in W_{e,s}]$ | $\Sigma_3$ |

The quantifier form gives the upper bound. The lower bound needs a reduction. For TOT, let $A = \{ x : \forall y\, \exists z\, R(x, y, z) \}$ be any $\Pi_2$ set. By the [s-m-n theorem](/s-m-n-theorem/) there is a total computable $f$ such that $\varphi_{f(x)}(y)$ searches, for each $y' \le y$ in turn, for a $z$ with $R(x, y', z)$, and halts when it has found one for every $y' \le y$. Then $\varphi_{f(x)}$ is total if and only if $x \in A$, so $A \le_m \mathrm{TOT}$.

## Examples

**The halting set.** $K$ has the form $\exists s\, [\varphi_e(e) \text{ halts within } s \text{ steps}]$, so it is $\Sigma_1$. It is $\Sigma_1$-complete and not $\Pi_1$, so its complement is $\Pi_1$ and not $\Sigma_1$, which is the statement that the complement of $K$ is not c.e.

**Open problems as sentences.** A sentence is a formula with no free variable, and its level is the level of its quantifier form. The level says what kind of evidence could refute it.

- Goldbach's conjecture is $\Pi_1$: for all even $n > 2$ there are primes $p, q \le n$ with $p + q = n$, where the inner quantifiers are bounded. If it is false, a search finds a counterexample.
- The twin prime conjecture is $\Pi_2$: for all $n$ there is a $p > n$ with $p$ and $p + 2$ prime.
- The Collatz conjecture is $\Pi_2$: for all $n \ge 1$ there is an $s$ such that $s$ steps of the map ($n \mapsto n/2$ for even $n$, $n \mapsto 3n + 1$ for odd $n$) reach $1$. A run of the map for every $n < 1000$ finds the largest step count $178$, at $n = 871$; below $10000$ it is $261$, at $n = 6171$. Such runs confirm instances of the inner $\exists s$ one $n$ at a time, but no finite run can confirm the outer $\forall n$.
- The statement $\mathrm{P} \ne \mathrm{NP}$ is $\Pi_2$: for every machine $M$ and every exponent $k$, there is an input on which $M$ either gives the wrong answer to SAT or runs longer than $|x|^k + k$ steps, and this inner check is decidable.

**Index sets.** By [Rice's theorem](/rice-theorem/), nontrivial properties of the function computed by a program are undecidable; the hierarchy says how undecidable. "$W_e$ is nonempty" is $\Sigma_1$-complete, "$W_e$ is finite" is $\Sigma_2$-complete, "$\varphi_e$ is total" is $\Pi_2$-complete, and "$W_e$ is decidable" is $\Sigma_3$-complete.

**Above the hierarchy.** The set of true sentences of first-order arithmetic is not arithmetical. Every $\Sigma_{n+1}$ set reduces to it by a many-one reduction (map $x$ to the sentence that says $x$ is in the set), so if it were $\Sigma_n$, every $\Sigma_{n+1}$ set would be $\Sigma_n$, which the hierarchy theorem forbids. Its degree is that of $\emptyset^{(\omega)}$ on the [Turing jump](/turing-jump/) page. This is a computability form of Tarski's theorem on the undefinability of truth, and it is close to [Gödel's incompleteness theorem](/godel-incompleteness-theorem/).

## Where it is used

- **Classifying undecidable problems.** The level of a problem, together with a completeness proof, is a precise statement of how undecidable it is. Termination of a program on one input is $\Sigma_1$; termination on all inputs and equivalence of two programs are $\Pi_2$.
- **Degrees.** By [Post's theorem](/posts-theorem/), the $\Sigma_{n+1}$-complete sets have the [Turing degree](/turing-degrees/) $\mathbf{0}^{(n+1)}$, so the levels give the natural landmarks of the degree order.
- **Logic.** The level of a sentence of arithmetic tells which methods can refute or confirm it. A false $\Pi_1$ sentence is refuted by one finite computation that finds a counterexample, while a true one is never confirmed by a finite computation. The consistency of a theory with a computable set of axioms is a $\Pi_1$ sentence: no number codes a proof of a contradiction.
- **Complexity theory.** The [polynomial hierarchy](/polynomial-hierarchy/) uses the same alternation of quantifiers, with each quantifier bounded by a polynomial in the input length, and $\mathrm{NP}$ in the role of $\Sigma_1$. The oracle characterization $\Sigma_{k+1}^{\mathrm{P}} = \mathrm{NP}^{\Sigma_k^{\mathrm{P}}}$ is the analog of Post's theorem.

## References
