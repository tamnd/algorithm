---
tag: BGPJ7S
kind: theorem
slug: posts-theorem
name: Post's theorem
aliases:
- Post's theorem on the arithmetical hierarchy
area: complexity/computability
level: research
summary: "A set is Sigma_(n+1) exactly when it is c.e. relative to the n-th jump of the empty set, and Delta_(n+1) exactly when it is computable from that jump. Quantifier levels match Turing degrees."
prereqs: [arithmetical-hierarchy, turing-jump]
see_also: [arithmetical-hierarchy, turing-jump, turing-degrees, oracle-turing-machine, halting-problem, polynomial-hierarchy, post-problem, relativization]
sources:
  - title: "Emil L. Post, Degrees of recursive unsolvability, preliminary report (abstract), Bulletin of the American Mathematical Society 54(7) (1948)"
    locator: pp. 641 to 642
  - paper: doi:10.1090/S0002-9947-1943-0007371-8
    title: "Stephen C. Kleene, Recursive predicates and quantifiers, Transactions of the American Mathematical Society 53(1) (1943)"
    locator: "pp. 41 to 73 (the quantifier forms and the hierarchy theorem)"
  - book: isbn:9783642319327
    title: "Robert I. Soare, Turing Computability, Theory and Applications, Springer, 2016"
    locator: "Chapter 4, The Arithmetical Hierarchy"
---

Post's theorem connects two ways of measuring how undecidable a set is. The [arithmetical hierarchy](/arithmetical-hierarchy/) counts the alternating quantifiers in a definition, and the [Turing jump](/turing-jump/) builds the chain $\emptyset, \emptyset', \emptyset'', \ldots$ of harder and harder halting problems. The theorem says that a set is $\Sigma_{n+1}$ exactly when it is computably enumerable (c.e.) relative to $\emptyset^{(n)}$, and $\Delta_{n+1}$ exactly when it is computable from $\emptyset^{(n)}$. So each extra quantifier costs exactly one jump. For $n = 0$ this is the familiar fact that $\Sigma_1$ is the class of c.e. sets and $\Delta_1$ the class of decidable sets. Post announced the theorem in 1948. The same pattern, with polynomial bounds, defines the [polynomial hierarchy](/polynomial-hierarchy/) by oracles.

## Statement

Fix a computable numbering of [oracle machines](/oracle-turing-machine/), with the encoding fixed and computable. Let $\emptyset^{(0)} = \emptyset$ and $\emptyset^{(n+1)} = (\emptyset^{(n)})'$, where $A' = \{ e : \Phi_e^A(e)\!\downarrow \}$. "$A$ is c.e. in $B$" means that $A = W_e^B$ for some $e$.

**Theorem (Post).** For every $n \ge 0$ and every set $A \subseteq \mathbb{N}$:

1. $A \in \Sigma_{n+1}$ if and only if $A$ is c.e. in some $\Pi_n$ set, if and only if $A$ is c.e. in $\emptyset^{(n)}$.
2. For $n \ge 1$, $\emptyset^{(n)}$ is $\Sigma_n$-complete: it is $\Sigma_n$, and every $\Sigma_n$ set reduces to it by a one-one reduction.
3. $A \in \Delta_{n+1}$ if and only if $A \le_T \emptyset^{(n)}$.

## In plain words

Some questions about numbers need one search ("is there a step at which this program halts?"), some need a search inside a check over all numbers ("for every input, is there a step?"), and so on. Separately, imagine a magic box that answers the halting question, then a stronger box that answers the halting question for programs that use the first box, and so on.

The theorem says these two ladders are the same ladder. A question with one more layer of "there is" and "for all" is exactly a question that one more box lets you answer by a search. With the boxes up to a level, you can settle every question whose yes and no answers both need at most that many layers.

## Proof

The proof is by induction on $n$. For $n = 0$, part 1 says that $\Sigma_1$ is the class of c.e. sets, since every set is c.e. in a decidable set exactly when it is c.e., and part 3 says that $\Delta_1$ is the class of decidable sets, since a set and its complement are both c.e. exactly when the set is decidable.

**Lemma.** $A$ is $\Sigma_{n+1}$ if and only if $A$ is c.e. in some $\Pi_n$ set.

*If $A$ is $\Sigma_{n+1}$.* Then $A = \{ x : \exists y\, C(x, y) \}$ for a $\Pi_n$ relation $C$, after merging the leading $\exists$ quantifiers with a pairing function. An oracle machine with oracle $C$ searches $y = 0, 1, 2, \ldots$ and asks whether $(x, y) \in C$; it halts exactly when $x \in A$. So $A$ is c.e. in $C$.

*If $A = W_e^C$ with $C$ in $\Pi_n$.* By the use principle, $x \in A$ if and only if there are a stage $s$ and a finite binary string $\sigma$ such that

- $\Phi_e^\sigma(x)$ halts within $s$ steps and queries only numbers below $|\sigma|$, which is a decidable condition on $(x, s, \sigma)$, and
- $\sigma$ is an initial segment of $C$: for each $i < |\sigma|$, $\sigma(i) = 1$ implies $i \in C$, and $\sigma(i) = 0$ implies $i \notin C$.

In the second condition, $i \in C$ is $\Pi_n$ and $i \notin C$ is $\Sigma_n$. A bounded conjunction of such conditions is $\Delta_{n+1}$, so the whole condition is $\Sigma_{n+1}$ after the quantifier $\exists \langle s, \sigma \rangle$. So $A$ is $\Sigma_{n+1}$.

**Part 1.** Assume part 2 for $n$ (for $n = 0$ use $\emptyset$). If $A$ is c.e. in a $\Pi_n$ set $C$, then $C \le_T \emptyset^{(n)}$, since the complement of $C$ is $\Sigma_n$ and reduces to $\emptyset^{(n)}$ by part 2. So $A$ is c.e. in $\emptyset^{(n)}$. Conversely, $\emptyset^{(n)}$ is $\Sigma_n$, so its complement $C$ is $\Pi_n$, and a set c.e. in $\emptyset^{(n)}$ is c.e. in $C$, since each set computes the other. With the lemma, the three conditions of part 1 are equivalent.

**Part 2 for $n + 1$.** $\emptyset^{(n+1)} = (\emptyset^{(n)})'$ is c.e. in $\emptyset^{(n)}$, so it is $\Sigma_{n+1}$ by part 1. If $A$ is $\Sigma_{n+1}$, it is c.e. in $\emptyset^{(n)}$ by part 1, and the jump theorem of the [Turing jump](/turing-jump/) page gives $A \le_1 (\emptyset^{(n)})'$.

**Part 3.** $A$ is $\Delta_{n+1}$ if and only if $A$ and its complement are both $\Sigma_{n+1}$, if and only if both are c.e. in $\emptyset^{(n)}$ by part 1, if and only if $A \le_T \emptyset^{(n)}$, by the relativized form of the fact that a set is decidable when it and its complement are c.e. $\blacksquare$

**Worked example.** Take $\mathrm{FIN} = \{ e : W_e \text{ is finite} \}$, which has the $\Sigma_2$ form $\exists n\, \forall x\, \forall s\, [x > n \Rightarrow x \notin W_{e,s}]$. Part 1 says it is c.e. in $\emptyset'$. The machine is direct: for $n = 0, 1, 2, \ldots$, ask the oracle whether the machine that searches for an element of $W_e$ above $n$ ever halts. The question is an instance of the halting problem, which reduces to $\emptyset'$. The first "no" proves that $W_e$ has no element above $n$, so $W_e$ is finite, and the machine halts. If $W_e$ is infinite, every answer is "yes" and the machine runs forever. By part 2, $\mathrm{FIN}$ reduces to $\emptyset''$, and since $\mathrm{FIN}$ is $\Sigma_2$-complete, the two are Turing equivalent.

## Consequences

- **The hierarchy is proper.** $\emptyset^{(n+1)}$ is $\Sigma_{n+1}$. If it were also $\Pi_{n+1}$, it would be $\Delta_{n+1}$ and so computable from $\emptyset^{(n)}$ by part 3, which the jump theorem forbids. So $\Sigma_{n+1} \ne \Pi_{n+1}$ for every $n$, a second proof of Kleene's hierarchy theorem.
- **Arithmetical sets.** A set is arithmetical if and only if it is computable from $\emptyset^{(n)}$ for some $n$. All arithmetical sets are computable from $\emptyset^{(\omega)}$, the set that collects all the iterated jumps, which is not arithmetical.
- **Degrees of natural problems.** Every $\Sigma_{n+1}$-complete or $\Pi_{n+1}$-complete set has the [Turing degree](/turing-degrees/) $\mathbf{0}^{(n+1)}$. So $\mathrm{TOT}$ and $\mathrm{FIN}$ have degree $\mathbf{0}''$, and $\mathrm{COF}$ has degree $\mathbf{0}'''$.
- **Limit computability.** For $n = 1$, part 3 says that $\Delta_2$ is the class of sets computable from the [halting problem](/halting-problem/). With Shoenfield's limit lemma, $\Delta_2$ is also the class of sets with a computable approximation that changes its value finitely often at each input.
- **Relativization.** The theorem relativizes: for every set $B$, a set is $\Sigma_{n+1}^B$ (with a matrix decidable in $B$) if and only if it is c.e. in $B^{(n)}$.
- **Complexity theory.** In the [polynomial hierarchy](/polynomial-hierarchy/), $\Sigma_{k+1}^{\mathrm{P}} = \mathrm{NP}^{\Sigma_k^{\mathrm{P}}}$: one more polynomially bounded quantifier is one more $\mathrm{NP}$ oracle. This is the analog of part 1, with $\mathrm{NP}$ in the role of "c.e.". It does not imply that the levels are different, because no analog of the jump theorem is known in polynomial time, and [relativization](/relativization/) results show that the usual diagonal proof cannot give one.

## Tightness

- **$\Delta_{n+1}$ is larger than $\Sigma_n \cup \Pi_n$.** The set $K \oplus \overline{K} = \{ 2x : x \in K \} \cup \{ 2x + 1 : x \notin K \}$ is computable from $\emptyset'$, so it is $\Delta_2$. It is not $\Sigma_1$, since $\overline{K}$ reduces to it, and not $\Pi_1$, since $K$ reduces to it. So "computable from $\emptyset^{(n)}$" in part 3 cannot be replaced by "$\Sigma_n$ or $\Pi_n$".
- **"c.e. in" cannot be replaced by "computable in".** $K$ is $\Sigma_1$ but is not computable from $\emptyset$. In general a $\Sigma_{n+1}$ set need not be computable from $\emptyset^{(n)}$.
- **Not every $\Sigma_{n+1}$ set is complete.** Part 2 gives completeness for $\emptyset^{(n+1)}$ only. By the relativized solution of [Post's problem](/post-problem/), there are $\Sigma_{n+1}$ sets that are not computable from $\emptyset^{(n)}$ and not complete, so a set at level $n + 1$ need not have degree $\mathbf{0}^{(n+1)}$.

## History

Kleene introduced the quantifier forms and proved the hierarchy theorem in 1943, and Mostowski found the hierarchy independently in 1947. Post connected it with degrees: his abstract of 1948, a preliminary report on degrees of recursive unsolvability, announced that the levels of the hierarchy are given by the iterated jumps of the empty set. A full proof is in Soare's textbook, in the chapter on the arithmetical hierarchy.

## References
