---
tag: H3Q7BT
kind: definition
slug: many-one-reducibility
name: Many-one reducibility
aliases:
- computable reduction
- m-reduction
- mapping reduction
area: complexity/computability
level: core
summary: A reduces to B by a many-one reduction if a total computable f has x in A exactly when f(x) is in B. Decidability and c.e. pass from B down to A.
prereqs: [decidable-language, recursively-enumerable-language, computable-function]
see_also: [halting-problem, acceptance-problem, rice-theorem, polynomial-time-reduction, turing-reduction, turing-degrees, oracle-turing-machine, reduction]
sources:
  - paper: doi:10.1090/S0002-9904-1944-08111-1
    title: Emil L. Post, Recursively enumerable sets of positive integers and their decision problems, Bulletin of the American Mathematical Society 50(5) (1944)
    locator: pp. 284 to 316 (many-one and one-one reducibility, creative sets, and Turing reducibility)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 5.3, Mapping reducibility
  - book: isbn:9780262680523
    title: Hartley Rogers Jr., Theory of Recursive Functions and Effective Computability, MIT Press (reprint of the McGraw-Hill edition of 1967)
    locator: Chapter 7 (one-one and many-one reducibility, creative sets, and the isomorphism theorem)
  - paper: doi:10.1002/malq.19550010205
    title: John Myhill, Creative sets, Zeitschrift für mathematische Logik und Grundlagen der Mathematik 1(2) (1955)
    locator: pp. 97 to 108
---

A *many-one reduction* from a language $A$ to a language $B$ is a total [computable function](/computable-function/) $f$ such that $x \in A$ if and only if $f(x) \in B$, for every $x$. If one exists, $A$ is *many-one reducible* to $B$, written $A \le_m B$. The reduction turns each question about $A$ into one question about $B$ with the same answer, so $A$ is no harder than $B$: if $B$ is [decidable](/decidable-language/) or [computably enumerable](/recursively-enumerable-language/), so is $A$. Read the other way, it is the main tool for proving [undecidability](/undecidability/). Post introduced it in 1944, together with the stricter one-one reducibility and the weaker Turing reducibility. Sipser calls it a *mapping reduction*. The [polynomial-time reductions](/polynomial-time-reduction/) of complexity theory are its resource-bounded form.

## Definition

Let $A \subseteq \Sigma^*$ and $B \subseteq \Gamma^*$. Then $A \le_m B$ if there is a total computable function $f : \Sigma^* \to \Gamma^*$ with
$$x \in A \iff f(x) \in B \quad \text{for all } x \in \Sigma^*.$$
The function $f$ must be defined on every input, including the words outside $A$, and it must send those words outside $B$. The same definition applies to sets of natural numbers.

- $A \equiv_m B$ if $A \le_m B$ and $B \le_m A$. The classes of $\equiv_m$ are the *m-degrees*.
- $A \le_1 B$, *one-one reducibility*, if such an $f$ exists that is also injective.
- $B$ is *m-complete* for a class $\mathcal{C}$ if $B \in \mathcal{C}$ and $A \le_m B$ for every $A \in \mathcal{C}$. For the class of c.e. sets, the complete sets are the c.e. sets to which the [halting problem](/halting-problem/) reduces.

**Basic properties.**

1. *Preorder.* $A \le_m A$ by the identity. If $A \le_m B$ by $f$ and $B \le_m C$ by $g$, then $A \le_m C$ by $g \circ f$, which is total computable.
2. *Decidability and c.e. pass down.* Let $A \le_m B$ by $f$. If $M$ decides $B$, the machine that computes $f(x)$ and runs $M$ on it decides $A$. If $M$ only recognizes $B$, the same machine recognizes $A$. So if $B$ is decidable, so is $A$, and if $B$ is c.e., so is $A$.
3. *Undecidability passes up.* By (2), if $A$ is undecidable and $A \le_m B$, then $B$ is undecidable; and if $A$ is not c.e., neither is $B$.
4. *Complements.* $A \le_m B$ if and only if $\overline{A} \le_m \overline{B}$, by the same $f$, since $x \notin A \iff f(x) \notin B$. So a reduction from $\overline{\mathrm{HALT}}$ to $B$ shows that $B$ is not c.e.
5. *The trivial sets.* $A \le_m \emptyset$ if and only if $A = \emptyset$, since no $f(x)$ can be in $\emptyset$; in the same way $A \le_m \Gamma^*$ if and only if $A = \Sigma^*$. If $B$ is neither empty nor everything, then every decidable $A$ reduces to $B$: fix $b_1 \in B$ and $b_0 \notin B$, and let $f(x) = b_1$ if $x \in A$ and $f(x) = b_0$ otherwise. So all decidable sets other than $\emptyset$ and $\Sigma^*$ form the lowest nontrivial m-degree.

**Complete sets.** $K = \{ e : \varphi_e(e) \text{ is defined} \}$, $\mathrm{HALT}$ and $A_{\mathrm{TM}}$ are m-complete for the c.e. sets: if $A = L(M)$, then $x \mapsto \langle M, x \rangle$ reduces $A$ to $A_{\mathrm{TM}}$. Post called a c.e. set *creative* if its complement fails, in an effective way, to be c.e.; $K$ is the standard example. Myhill (1955) showed that the creative sets are exactly the m-complete c.e. sets, that they are even 1-complete, and that for any two sets that are one-one reducible to each other, some computable permutation of $\mathbb{N}$ maps one onto the other. So all the m-complete c.e. sets are copies of $K$.

**Comparison with Turing reducibility.** $A$ is *Turing reducible* to $B$, $A \le_T B$, if an [oracle Turing machine](/oracle-turing-machine/) with oracle $B$ decides $A$. Such a machine may ask many questions, adaptively, and may negate the answers. Every many-one reduction is a Turing reduction with one question and no change to the answer, so $A \le_m B$ implies $A \le_T B$. The converse fails: $\overline{K} \le_T K$ (ask whether $e \in K$ and negate the answer), but $\overline{K} \not\le_m K$, since $K$ is c.e. and $\overline{K}$ is not. The classes of $\le_T$ are the [Turing degrees](/turing-degrees/). Many-one reductions see the difference between c.e. and co-c.e., and Turing reductions do not.

## Examples and non-examples

**Small examples.**

- $\{ x \in \mathbb{N} : x \text{ even} \} \le_m \{0\}$ by $f(x) = x \bmod 2$.
- The multiples of $3$ reduce to the multiples of $6$ by $f(x) = 2x$, since $3 \mid x$ if and only if $6 \mid 2x$. This $f$ is injective, so it is also a one-one reduction.
- $\mathbb{N} \le_m \{0\}$ by the constant function $0$, but $\mathbb{N} \not\le_1 \{0\}$: an injective $f$ cannot map an infinite set into a set with one element. So $\le_1$ is a stricter relation than $\le_m$.

**Reductions between undecidable problems.**

- $\mathrm{HALT} \le_m A_{\mathrm{TM}}$: map $\langle M, w \rangle$ to $\langle M_1, w \rangle$, where $M_1$ is $M$ with its reject moves redirected to the accept state.
- $A_{\mathrm{TM}} \le_m \mathrm{HALT}$: map $\langle M, w \rangle$ to $\langle M_2, w \rangle$, where $M_2$ is $M$ with its reject moves redirected to a state that loops forever.
- $K \le_m \mathrm{HALT}$: map $e$ to $\langle M_e, e \rangle$. Conversely, $\mathrm{HALT} \le_m K$: map $\langle M, w \rangle$ to an index of the machine that ignores its input and runs $M$ on $w$, computed by the [s-m-n theorem](/s-m-n-theorem/).
- $A_{\mathrm{TM}} \le_m \{ \langle N \rangle : L(N) \ne \emptyset \}$: map $\langle M, w \rangle$ to a machine that ignores its input $x$ and accepts if $M$ accepts $w$. By property 4, $\overline{A_{\mathrm{TM}}} \le_m E_{\mathrm{TM}}$, so the emptiness problem $E_{\mathrm{TM}}$ is not c.e.
- $\overline{\mathrm{HALT}} \le_m \mathrm{TOT}$: map $\langle M, w \rangle$ to a machine that on input $x$ runs $M$ on $w$ for $|x|$ steps, loops forever if $M$ has halted, and halts otherwise. So the totality problem is not c.e.

**Non-examples.**

- $\overline{K} \not\le_m K$, as above, though $\overline{K} \le_T K$.
- A reduction that answers the question itself is not a reduction. For example, "if $M$ halts on $w$, output $\langle M_1 \rangle$, else output $\langle M_2 \rangle$" is a well-defined map, but it is not computable, since it needs to know whether $M$ halts. A reduction may only build the new instance from the old one.
- A partial computable map is not enough. If $f(x)$ is undefined for some $x \notin A$, then a decider for $B$ composed with $f$ runs forever on $x$.

## Related definitions

- [Polynomial-time reduction](/polynomial-time-reduction/) (Karp reduction): a many-one reduction computable in polynomial time. It defines NP-completeness. Every polynomial-time reduction is a many-one reduction, but a many-one reduction may take any computable amount of time.
- [Turing reduction](/turing-reduction/) (Cook reduction): the polynomial-time form of Turing reducibility, with many oracle questions.
- [Oracle Turing machine](/oracle-turing-machine/) and [Turing degrees](/turing-degrees/): the computable Turing reducibility $\le_T$ and its degrees.
- [Rice's theorem](/rice-theorem/): a general many-one reduction from $A_{\mathrm{TM}}$ to every nontrivial semantic property.
- [Reduction](/reduction/): the general idea of solving one problem with a solver for another, in algorithms as well as in lower bounds.
- [Arithmetical hierarchy](/arithmetical-hierarchy/): each level $\Sigma_n$ and $\Pi_n$ has m-complete sets, such as $K$ for $\Sigma_1$ and $\mathrm{TOT}$ for $\Pi_2$.

## References
