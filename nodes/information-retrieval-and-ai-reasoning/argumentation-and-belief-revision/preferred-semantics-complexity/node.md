---
tag: 0A79JT
kind: theorem
slug: preferred-semantics-complexity
name: Complexity of preferred semantics
aliases:
- Dunne-Bench-Capon complexity of argumentation
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: For finite frameworks, credulous acceptance under preferred semantics is NP-complete, verification is coNP-complete, and sceptical acceptance is Pi2P-complete.
prereqs: [preferred-extension, argument-acceptance-problem, polynomial-hierarchy, qbf]
see_also: [stable-extension-argumentation, semi-stable-extension, argumentation-sat-encoding, sat, np-complete, co-np-complete, admissible-set]
sources:
  - book: isbn:9781848902756
    title: Wolfgang Dvořák and Paul E. Dunne, Computational problems in formal argumentation and their complexity, in Pietro Baroni, Dov Gabbay, Massimiliano Giacomin and Leendert van der Torre (eds), Handbook of Formal Argumentation, volume 1, College Publications (2018)
    locator: Section 3.3 (Table 1, Reduction 3.6 for the NP and coNP bounds and Reduction 3.7 for the Pi2P bound) and Section 3.4 (tractable classes and odd-cycle-free frameworks)
  - paper: doi:10.1016/S0004-3702(02)00261-8
    title: Paul E. Dunne and Trevor J. M. Bench-Capon, Coherence in finite argument systems, Artificial Intelligence 141(1-2), 187 to 203 (2002)
    locator: the whole paper (sceptical acceptance under preferred semantics is Pi2P-complete)
  - paper: "Yannis Dimopoulos and Alberto Torres, Graph theoretical structures in logic programs and default theories, Theoretical Computer Science 170(1-2), 209 to 244 (1996)"
    locator: the whole paper (the NP-completeness and coNP-completeness results for preferred semantics)
  - paper: doi:10.1016/0004-3702(94)00041-X
    title: Phan Minh Dung, On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games, Artificial Intelligence 77(2), 321 to 357 (1995)
    locator: Definition 7, Theorem 11, Corollary 12 and Theorem 25
  - paper: "Celia Wrathall, Complete sets and the polynomial-time hierarchy, Theoretical Computer Science 3(1), 23 to 33 (1976)"
    locator: the whole paper (QBF with k alternations is complete for the k-th level)
---

Preferred semantics is the most used credulous semantics of abstract argumentation, and its decision problems sit at two levels of the [polynomial hierarchy](/polynomial-hierarchy/). Asking whether an argument is in some preferred extension is NP-complete, like [SAT](/sat/). Asking whether it is in every preferred extension is $\Pi_2^P$-complete, like a [QBF](/qbf/) of the form $\forall \exists$. The jump comes from maximality: to refute sceptical acceptance one must show a preferred extension without the argument, and checking that a set is preferred is itself coNP-complete. The definitions are on [preferred extension](/preferred-extension/), and the full table for all semantics is on [argument acceptance](/argument-acceptance-problem/).

## Statement

Let $F = (A, R)$ be a finite argumentation framework, given as the list of its arguments and attacks, with $n = |A|$ and $m = |R|$. Let $\mathrm{prf}(F)$ be its set of preferred extensions, which is never empty (Dung 1995, Corollary 12). Consider the decision problems

- $\mathrm{Cred}_{prf}$: given $F$ and $a \in A$, is $a$ in some preferred extension?
- $\mathrm{Skept}_{prf}$: given $F$ and $a \in A$, is $a$ in every preferred extension?
- $\mathrm{Ver}_{prf}$: given $F$ and $S \subseteq A$, is $S$ a preferred extension?
- $\mathrm{Exists}^{\neg\emptyset}_{prf}$: given $F$, is there a nonempty preferred extension?

Hardness is under polynomial-time many-one reductions (the reductions below are also logspace). The complexity is combined: the whole framework is the input.

**Theorem.**

1. $\mathrm{Cred}_{prf}$ is NP-complete (Dimopoulos and Torres 1996).
2. $\mathrm{Ver}_{prf}$ is coNP-complete (Dimopoulos and Torres 1996).
3. $\mathrm{Exists}^{\neg\emptyset}_{prf}$ is NP-complete.
4. $\mathrm{Skept}_{prf}$ is $\Pi_2^P$-complete (Dunne and Bench-Capon 2002).

These are the preferred row of Table 1 in Dvořák and Dunne (2018), which also gives coNP-completeness of deciding whether the preferred extension is unique.

## In plain words

A preferred extension is a largest group of arguments that hangs together and answers every attack on it. Finding out whether a given argument can be in such a group is as hard as solving a satisfiability puzzle, but no harder: if someone shows you a group, you can check it fast. Checking that a given group is one of the largest ones is harder, because you must rule out every bigger group. Finding out whether an argument is in all of the largest groups is harder still. To say no, you must exhibit a largest group without it, and that claim of being largest cannot be checked fast. So the question has the shape "for all choices, there is a completion", which is the second level of the hierarchy.

## Proof

We use three facts from Dung (1995). A set is admissible when it is conflict-free and defends each member. Every admissible set is contained in a preferred extension (Theorem 11). Every preferred extension is admissible by definition and complete (Theorem 25).

**Membership.**

- *Credulous acceptance is in NP.* By Theorem 11, $a$ is in some preferred extension exactly when $a$ is in some admissible set. Guess $S$ and check in $O(n + m)$ time that it is admissible and holds $a$.
- *Verification is in coNP.* $S$ is not preferred exactly when $S$ is not admissible, or some admissible $T$ satisfies $S \subsetneq T$. Guess $T$ and check it in polynomial time.
- *Nonempty existence is in NP.* A nonempty preferred extension exists exactly when a nonempty admissible set exists, by Theorem 11.
- *Sceptical acceptance is in $\Pi_2^P$.* The complement asks for a preferred $S$ with $a \notin S$. Guess $S$ and verify that it is preferred with one call to an NP oracle (the complement of verification). So the complement is in $\Sigma_2^P = \mathrm{NP}^{\mathrm{NP}}$.

**The standard translation (Dvořák and Dunne, Reduction 3.6).** Let $\varphi$ be a CNF formula with clause set $C$ over variables $X$. The framework $F_\varphi$ has the arguments $\{\varphi\} \cup C \cup X \cup \bar{X}$, where $\bar{X} = \{\bar{x} : x \in X\}$ stands for the negative literals, and the attacks

- $(c, \varphi)$ for each clause $c$;
- $(x, \bar{x})$ and $(\bar{x}, x)$ for each variable $x$;
- $(l, c)$ for each literal $l$ that occurs in the clause $c$.

*Claim A.* $\varphi$ is in some admissible set of $F_\varphi$ if and only if $\varphi$ is satisfiable.

If $\tau$ is a model, let $S = \{\varphi\} \cup \{l : l \text{ true under } \tau\}$. $S$ has no clause and no complementary pair, so it is conflict-free. Each clause, an attacker of $\varphi$, has a true literal in $S$ that attacks it. Each literal $l \in S$ is attacked only by its complement, which $l$ attacks. So $S$ is admissible. Conversely, let $S$ be admissible with $\varphi \in S$. $S$ holds no clause, since each clause attacks $\varphi$. Each clause must be attacked by $S$, and only literals attack clauses, so $S$ holds a literal of each clause. $S$ holds no complementary pair. So "true when the positive literal is in $S$" is a model.

By Claim A and Theorem 11, $(F_\varphi, \varphi)$ is a yes-instance of $\mathrm{Cred}_{prf}$ exactly when $\varphi$ is satisfiable. This proves part 1.

**The construction for the second level (Dvořák and Dunne, Reduction 3.7).** Let $\Phi = \forall Y\, \exists Z\, \varphi$, where $\varphi$ is in CNF with clause set $C$ over $X = Y \cup Z$. The framework $H_\Phi$ is $F_\varphi$ plus one argument $\bar\varphi$ and the attacks

- $(\varphi, \bar\varphi)$ and $(\bar\varphi, \bar\varphi)$;
- $(\bar\varphi, z)$ and $(\bar\varphi, \bar{z})$ for each $z \in Z$.

For an admissible set $S$ of $H_\Phi$:

- **(F1)** $\bar\varphi \notin S$, because $\bar\varphi$ attacks itself.
- **(F2)** If $S$ holds a $Z$-literal, then $\varphi \in S$. The literal is attacked by $\bar\varphi$, so $S$ attacks $\bar\varphi$, and the only attackers of $\bar\varphi$ are $\varphi$ and $\bar\varphi$.
- **(F3)** If $\varphi \in S$, then as in Claim A, $S$ holds no clause and a literal of each clause, with no complementary pair.
- **(F4)** If a clause $c$ is in $S$, then $S$ attacks each literal $l$ of $c$. The attackers of $l$ are its complement and, for a $Z$-literal, $\bar\varphi$. By (F1), the complement of $l$ is in $S$. If $c$ has a $Z$-literal, this puts a $Z$-literal in $S$, so $\varphi \in S$ by (F2), and $c$ attacks $\varphi$, a conflict. So $c$ has only $Y$-literals, and $S$ holds the complement of each of them.

*Lemma B.* Each preferred extension $E$ of $H_\Phi$ holds exactly one of $y$, $\bar{y}$ for each $y \in Y$.

At most one, by conflict-freeness. Suppose it holds neither. The only attacker of $y$ is $\bar{y} \notin E$, and $y$ attacks $\bar{y}$. $y$ also attacks the clauses that contain $y$, but by (F4) such a clause in $E$ would force $\bar{y} \in E$. So $E \cup \{y\}$ is conflict-free, and it defends each member, which contradicts the maximality of $E$. $\square$

*Claim C.* $\varphi$ is in every preferred extension of $H_\Phi$ if and only if $\Phi$ is true.

($\Leftarrow$) Let $\Phi$ be true and let $E$ be preferred. By Lemma B, $E$ fixes an assignment $I$ of $Y$. Choose $I_Z$ such that $I \cup I_Z$ satisfies $\varphi$, and let $T$ be $\{\varphi\}$ plus the literals true under $I \cup I_Z$. $T$ is admissible: it is conflict-free, each clause is attacked by a true literal of $T$, each literal is defended against its complement by itself, and each $Z$-literal is defended against $\bar\varphi$ by $\varphi$. Suppose $\varphi \notin E$. By (F1) and (F2), $E$ holds no $\bar\varphi$ and no $Z$-literal. If $E$ held a clause $c$, then by (F4) $c$ would have only $Y$-literals, all false under $I$, so $I \cup I_Z$ would make $c$ false. So $E$ is exactly the set of the $Y$-literals true under $I$, and $E \subsetneq T$, which contradicts maximality. So $\varphi \in E$.

($\Rightarrow$) Let $\Phi$ be false, with an assignment $I$ of $Y$ that no $I_Z$ extends to a model. The set $S_I$ of the $Y$-literals true under $I$ is admissible: no $Z$-literal or $\bar\varphi$ is involved, and each literal defends itself. By Theorem 11 there is a preferred $E \supseteq S_I$, and by Lemma B its $Y$-literals are exactly $S_I$. If $\varphi \in E$, then (F3) gives a consistent set of literals that hits each clause and agrees with $I$ on $Y$, which is a model extending $I$. That is impossible, so $\varphi \notin E$. $\square$

Deciding the truth of $\forall Y \exists Z\, \varphi$ with $\varphi$ in CNF is $\Pi_2^P$-complete (Wrathall 1976). $H_\Phi$ has $|C| + 2|X| + 2$ arguments and is built in logspace. This proves part 4.

**Verification and nonempty existence.** Let $\varphi$ be a CNF formula with no empty clause (a formula with an empty clause is unsatisfiable and can be mapped to a fixed instance). Take $Y = \emptyset$ in the construction, so every variable is in $Z$ and $\bar\varphi$ attacks every literal. Then every nonempty admissible set holds $\varphi$: a literal brings in $\varphi$ by (F2), and a clause cannot be in an admissible set by (F4), because each clause has a $Z$-literal. So by (F3) and the first half of Claim A, a nonempty admissible set exists if and only if $\varphi$ is satisfiable. Hence $\emptyset$ is preferred exactly when $\varphi$ is unsatisfiable, which reduces UNSAT to $\mathrm{Ver}_{prf}$ (part 2), and a nonempty preferred extension exists exactly when $\varphi$ is satisfiable, which reduces SAT to $\mathrm{Exists}^{\neg\emptyset}_{prf}$ (part 3).

## Consequences

- **Same credulous problem for three semantics.** By Theorem 11 and Theorem 25, credulous acceptance under admissible, complete and preferred semantics is one problem, and one SAT call on the [argumentation SAT encoding](/argumentation-sat-encoding/) decides it.
- **Preferred is harder than stable for sceptical reasoning.** Sceptical acceptance under [stable semantics](/stable-extension-argumentation/) is coNP-complete. If sceptical preferred acceptance were in coNP, then $\Pi_2^P = \mathrm{coNP}$ and the polynomial hierarchy would collapse to its first level.
- **Solver design.** Unless the hierarchy collapses, no single SAT call can decide sceptical preferred acceptance. Practical solvers use a loop of SAT calls that look for an admissible set avoiding the query and then try to extend it.
- **Semi-stable semantics.** For [semi-stable](/semi-stable-extension/) semantics, credulous acceptance is already $\Sigma_2^P$-complete, so the maximality of the range costs one level more than the maximality of the set.

## Tightness

- **Odd-cycle-free frameworks.** If a finite framework has no directed cycle of odd length, its preferred and stable extensions coincide, so sceptical preferred acceptance falls to coNP-complete, and the $\Pi_2^P$ bound needs odd cycles. The construction $H_\Phi$ has one: the self-attack of $\bar\varphi$.
- **Polynomial classes.** On acyclic, bipartite and even-cycle-free frameworks, all four problems of the theorem are in polynomial time, and the same holds on symmetric frameworks (Dvořák and Dunne, Section 3.4).
- **The hypotheses matter.** The theorem is about combined complexity on finite frameworks given explicitly. It says nothing about frameworks given in a succinct form, where the bounds can be higher, or about structured formalisms that first have to build the framework.

## History

Dung defined preferred extensions in 1995 and proved that they always exist. Dimopoulos and Torres in 1996 studied kernels and related graph structures in logic programs and default theories and obtained the NP and coNP results for stable, admissible and preferred semantics. Dunne and Bench-Capon in 2002 studied coherence, the case where the preferred and stable extensions coincide, and proved that sceptical acceptance under preferred semantics is $\Pi_2^P$-complete. The construction above is the variant given in the survey of Dvořák and Dunne in the Handbook of Formal Argumentation (2018), whose Table 1 collects the complexity of all standard semantics.

## References
