---
tag: HFHFEB
kind: definition
slug: strongest-postcondition
name: Strongest postcondition
aliases:
- strongest post-condition
area: compilers-and-program-analysis/verification-and-synthesis
level: core
summary: The most precise condition that holds after a command runs from a state satisfying a given precondition, the forward dual of wp.
prereqs: [weakest-precondition, hoare-triple]
see_also: [verification-condition-generation, symbolic-execution, path-condition, abstract-interpretation, collecting-semantics, floyd-inductive-assertions, loop-invariant-synthesis, galois-connection]
sources:
  - paper: "Robert W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, American Mathematical Society, 1967"
    locator: pp. 19 to 32, the verification condition for an assignment operator, which introduces the existential quantifier over the old value
  - paper: doi:10.1007/978-1-4612-3228-5_12
    title: Edsger W. Dijkstra and Carel S. Scholten, The strongest postcondition, chapter of Predicate Calculus and Program Semantics, Springer, 1990
    locator: pp. 209 to 215, and the chapter on converse predicate transformers before it, pp. 201 to 208
  - paper: doi:10.1137/0207005
    title: Stephen A. Cook, Soundness and completeness of an axiom system for program verification, SIAM Journal on Computing 7(1), 1978
    locator: pp. 70 to 90, the definition of expressiveness by the strongest postcondition
  - paper: doi:10.1145/360204.360220
    title: Cormac Flanagan and James B. Saxe, Avoiding exponential explosion, generating compact verification conditions, Proceedings of POPL 2001
    locator: pp. 193 to 205, Section 1, which notes that strongest postconditions and symbolic execution can also blow up
---

The strongest postcondition $\mathrm{sp}(S, P)$ of a command $S$ and a precondition $P$ is the set of all states in which a run of $S$ can stop when it starts in a state of $P$. Every true postcondition of $S$ from $P$ contains it, so it is the most precise one. It is computed forwards through the code, and it is the dual of the [weakest liberal precondition](/weakest-precondition/): $\mathrm{sp}(S, P) \subseteq Q$ holds exactly when $P \subseteq \mathrm{wlp}(S, Q)$. [Symbolic execution](/symbolic-execution/), forward [verification condition generation](/verification-condition-generation/) and [abstract interpretation](/abstract-interpretation/) all compute it or approximate it.

## Definition

Use the notation of the [weakest precondition](/weakest-precondition/) page. A *state* $\sigma$ gives an integer to each variable. A *predicate* is a set of states, written as a formula; $P \wedge Q$ is the intersection, $P \vee Q$ the union, and $P \implies Q$ means $P \subseteq Q$. The commands are

$$S ::= \mathbf{skip} \mid x := e \mid \mathbf{havoc}\ x \mid \mathbf{assume}\ b \mid S_1; S_2 \mid \mathbf{if}\ b\ \mathbf{then}\ S_1\ \mathbf{else}\ S_2 \mid \mathbf{while}\ b\ \mathbf{do}\ S.$$

$\mathbf{havoc}\ x$ gives $x$ any value, and $\mathbf{assume}\ b$ stops the run with no final state when $b$ is false. The meaning $[\![S]\!]$ of $S$ is the set of pairs $(\sigma, \sigma')$ such that some run of $S$ from $\sigma$ stops in $\sigma'$.

**Definition.** For a command $S$ and a predicate $P$,

$$\mathrm{sp}(S, P) = \{\sigma' \mid \text{there is } \sigma \in P \text{ with } (\sigma, \sigma') \in [\![S]\!]\}.$$

So $\mathrm{sp}(S, P)$ is the image of $P$ under the relation $[\![S]\!]$. The partial correctness triple $\{P\}\ S\ \{Q\}$ holds exactly when $\mathrm{sp}(S, P) \implies Q$. It follows that $\mathrm{sp}(S, P)$ is the strongest $Q$ for which the triple holds, which gives the name. Runs that do not stop add nothing, so sp, like wlp, is about [partial correctness](/partial-correctness/) only.

**Duality with wlp.** For all $S$, $P$ and $Q$,

$$\mathrm{sp}(S, P) \implies Q \quad\text{if and only if}\quad P \implies \mathrm{wlp}(S, Q).$$

*Proof.* Both sides say the same thing: for every $\sigma \in P$ and every $\sigma'$ with $(\sigma, \sigma') \in [\![S]\!]$, $\sigma' \in Q$. The left side says it because $\mathrm{sp}(S, P)$ is the set of such $\sigma'$. The right side says it because $\mathrm{wlp}(S, Q)$ is the set of $\sigma$ all of whose final states are in $Q$. $\square$

In the words of order theory, $\mathrm{sp}(S, \cdot)$ and $\mathrm{wlp}(S, \cdot)$ form a [Galois connection](/galois-connection/) on the lattice of predicates, with sp as the lower adjoint. Three facts follow at once. First, sp is monotone. Second, sp preserves every union: $\mathrm{sp}(S, \bigvee_i P_i) = \bigvee_i \mathrm{sp}(S, P_i)$, and $\mathrm{sp}(S, \mathit{false}) = \mathit{false}$. Third, $\mathrm{sp}(S, \mathrm{wlp}(S, Q)) \implies Q$ and $P \implies \mathrm{wlp}(S, \mathrm{sp}(S, P))$.

**Assignment.** Let $P[x_0/x]$ be $P$ with every free $x$ replaced by a fresh variable $x_0$. Then

$$\mathrm{sp}(x := e, P) = \exists x_0 .\ P[x_0/x] \wedge x = e[x_0/x].$$

*Proof.* The command maps $\sigma$ to $\sigma' = \sigma[x \mapsto e(\sigma)]$. Suppose $\sigma' = \sigma[x \mapsto e(\sigma)]$ for some $\sigma \in P$. Take $x_0 = \sigma(x)$. The other variables agree in $\sigma$ and $\sigma'$, so $\sigma'$ with $x_0$ set to $\sigma(x)$ satisfies $P[x_0/x]$, because that formula reads the old value of $x$ from $x_0$. For the same reason $e[x_0/x]$ has the value $e(\sigma)$, which is $\sigma'(x)$. So $\sigma'$ satisfies the right side. Conversely, suppose $\sigma'$ and a value $v$ for $x_0$ satisfy $P[x_0/x] \wedge x = e[x_0/x]$. Let $\sigma = \sigma'[x \mapsto v]$. Then $\sigma \in P$, and $e(\sigma)$ equals the value of $e[x_0/x]$, which is $\sigma'(x)$. So $\sigma' = \sigma[x \mapsto e(\sigma)]$ is a final state from $P$. $\square$

The duality makes this the mirror of the rule $\mathrm{wlp}(x := e, Q) = Q[e/x]$. The forward rule needs the quantifier, because the old value of $x$ is lost. When the assignment can be undone, the quantifier goes away: for $x := x + c$, the only possible old value is $x - c$, so $\mathrm{sp}(x := x + c, P) = P[x - c/x]$.

**The other commands.** Each rule follows from the definition of $[\![S]\!]$.

- $\mathrm{sp}(\mathbf{skip}, P) = P$ and $\mathrm{sp}(\mathbf{assume}\ b, P) = P \wedge b$.
- $\mathrm{sp}(\mathbf{havoc}\ x, P) = \exists x .\ P$.
- $\mathrm{sp}(S_1; S_2, P) = \mathrm{sp}(S_2, \mathrm{sp}(S_1, P))$, since the meaning of a sequence is the composition of relations.
- $\mathrm{sp}(\mathbf{if}\ b\ \mathbf{then}\ S_1\ \mathbf{else}\ S_2, P) = \mathrm{sp}(S_1, P \wedge b) \vee \mathrm{sp}(S_2, P \wedge \neg b)$. With this rule the formula of a program with $n$ branches in sequence can have $2^n$ disjuncts, one for each path.
- $\mathrm{sp}(\mathbf{while}\ b\ \mathbf{do}\ S, P) = \neg b \wedge H$, where $H$ is the least [fixed point](/fixed-point/) of $F(X) = P \vee \mathrm{sp}(S, X \wedge b)$.

*Proof of the loop rule.* Let $H_k$ be the set of states at the loop head after exactly $k$ iterations of a run from $P$. Then $H_0 = P$ and $H_{k+1} = \mathrm{sp}(S, H_k \wedge b)$. The loop stops in $\sigma'$ exactly when $\sigma'$ is in some $H_k$ and fails $b$, so the result is $\neg b \wedge \bigvee_k H_k$. Because sp preserves unions, $F$ preserves the union of every increasing chain, and by the [Kleene fixed-point theorem](/kleene-fixed-point-theorem/) its least fixed point is $\bigvee_k F^k(\mathit{false})$. By induction, $F^{k+1}(\mathit{false}) = H_0 \vee \dots \vee H_k$, so the least fixed point is $\bigvee_k H_k$. $\square$

The set $H$ is the strongest [loop invariant](/loop-invariant/) at the head: every [inductive invariant](/inductive-invariant/) $I$ with $P \implies I$ and $\mathrm{sp}(S, I \wedge b) \implies I$ is a prefixed point of $F$, so $H \implies I$. This is why loop invariants are needed. The fixed point is a set of states, but in general no formula of the assertion language describes it.

**What is decidable.** For a loop-free command over linear integer arithmetic, $\mathrm{sp}(S, P)$ is a formula of [Presburger arithmetic](/presburger-arithmetic/), with one existential quantifier for each assignment and havoc. Presburger arithmetic is decidable, so the triple $\{P\}\ S\ \{Q\}$ is decidable for such commands; real tools give $\mathrm{sp}(S, P) \wedge \neg Q$ to an [SMT](/smt-problem/) solver, which treats the quantified variables as fresh constants. With products of variables, validity is undecidable by [Hilbert's tenth problem](/hilberts-tenth-problem/). With loops, the triple is undecidable even over linear arithmetic, by [Rice's theorem](/rice-theorem/), since it can express that a program never reaches a given point.

## Examples and non-examples

- **An assignment that can be undone.** From $P$: $x = 2$, the command $x := x + 1$ gives $\exists x_0 .\ x_0 = 2 \wedge x = x_0 + 1$, which is $x = 3$. The short rule $P[x - 1/x]$ gives $x - 1 = 2$, the same set.
- **An assignment that forgets.** From $x > 0 \wedge y = x$, the command $x := 5$ gives $\exists x_0 .\ x_0 > 0 \wedge y = x_0 \wedge x = 5$, which is $y > 0 \wedge x = 5$. The fact about the old $x$ survives through $y$.
- **A quantifier that does not go away.** From $\mathit{true}$, the command $x := 2x$ gives $\exists x_0 .\ x = 2x_0$: "$x$ is even". Presburger arithmetic eliminates the quantifier only with a divisibility predicate, $2 \mid x$; no formula built from linear inequalities alone describes the even numbers.
- **A loop.** From $n \ge 0$, the program $x := 0;\ \mathbf{while}\ x < n\ \mathbf{do}\ x := x + 1$ has the head states $H = 0 \le x \le n$. This $H$ satisfies $F(H) = H$: from $0 \le x \le n \wedge x < n$, the step $x := x + 1$ gives $1 \le x \le n$, and the initial states add $x = 0$. The strongest postcondition is $x \ge n \wedge 0 \le x \le n$, which is $x = n \wedge n \ge 0$.
- **A run that does not stop.** $\mathrm{sp}(\mathbf{while}\ \mathit{true}\ \mathbf{do}\ \mathbf{skip}, P) = \mathit{false}$ for every $P$. So $\mathrm{sp}(S, P) \implies Q$ never proves termination.
- **Non-example: conjoining without renaming.** The formula $P \wedge x = e$ is not the strongest postcondition. From $x = 2$, the command $x := x + 1$ would give $x = 2 \wedge x = x + 1$, which is false, and the triple with postcondition $\mathit{false}$ does not hold.
- **Non-example: wp run forwards.** The backward rule used forwards, $Q = P[e/x]$, is wrong too. From $x = 2$, the command $x := x + 1$ would give $x + 1 = 2$, that is $x = 1$.
- **Non-example: sp does not preserve intersections.** For $S = (x := 0)$, $P_1 = (x = 1)$ and $P_2 = (x = 2)$: $\mathrm{sp}(S, P_1 \wedge P_2) = \mathrm{sp}(S, \mathit{false}) = \mathit{false}$, but $\mathrm{sp}(S, P_1) \wedge \mathrm{sp}(S, P_2) = (x = 0)$. Only unions are preserved, as for every lower adjoint.
- **Non-example: going forwards and back does not return.** For $S = (x := 0)$ and $Q = (x \ge 0)$, $\mathrm{wlp}(S, Q) = \mathit{true}$, but $\mathrm{sp}(S, \mathit{true}) = (x = 0)$, which is strictly stronger than $Q$.

## Related definitions

- **Weakest precondition.** The [weakest precondition](/weakest-precondition/) works backwards from the postcondition, and its liberal form wlp is the upper adjoint of sp. A backward [VC generator](/verification-condition-generation/) uses wp, since its assignment rule is a substitution with no quantifier. A forward one uses sp.
- **Symbolic execution.** [Symbolic execution](/symbolic-execution/) computes sp one path at a time. The [path condition](/path-condition/) of a path, together with its symbolic store, is the sp of the path with the old values named by input symbols in place of $\exists$.
- **Collecting semantics and abstract interpretation.** The [collecting semantics](/collecting-semantics/) at a program point is the sp of the code that leads there. [Abstract interpretation](/abstract-interpretation/) computes an over-approximation of it in an [abstract domain](/abstract-domain/), and [predicate abstraction](/predicate-abstraction/) computes the best one over a fixed set of predicates.
- **Inductive assertions.** Floyd's method of [inductive assertions](/floyd-inductive-assertions/) used the forward assignment rule with the existential quantifier. A [loop invariant](/loop-invariant/) is a predicate that contains the head states $H$ of the loop rule, and [loop invariant synthesis](/loop-invariant-synthesis/) searches for one that a solver can handle.
- **Expressiveness.** Cook called an assertion language expressive when it can describe $\mathrm{sp}(S, P)$ for every $S$ and $P$, and proved [Hoare logic](/hoare-logic/) complete relative to such a language.

## References
