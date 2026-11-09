---
tag: 4ASCK6
kind: definition
slug: bisimulation
name: Bisimulation
aliases:
- Bisimilarity
- Strong bisimulation
- Bisimulation equivalence
area: logic-and-constraints/model-checking
level: core
summary: A relation between states such that related states match each other's transitions into related states; bisimilarity, the largest one, is the greatest fixed point of this condition.
prereqs: [labelled-transition-system, kripke-structure, fixed-point]
see_also: [simulation-relation, stuttering-equivalence, trace-equivalence, equivalence-checking, partition-refinement, ctl-star, modal-mu-calculus, knaster-tarski-theorem]
sources:
  - book: isbn:9780131150072
    title: Robin Milner, Communication and Concurrency, Prentice Hall, 1989
    locator: Chapter 4, Strong bisimulation (the definition, bisimilarity as the largest bisimulation, proof by exhibiting a bisimulation, and the congruence properties)
  - paper: doi:10.1145/2455.2460
    title: Matthew Hennessy and Robin Milner, Algebraic laws for nondeterminism and concurrency, Journal of the ACM 32(1), 1985
    locator: pages 137 to 161 (Hennessy-Milner logic and the characterization of bisimilarity for image-finite processes)
  - paper: doi:10.1016/0304-3975(88)90098-9
    title: Michael C. Browne, Edmund M. Clarke and Orna Grumberg, Characterizing finite Kripke structures in propositional temporal logic, Theoretical Computer Science 59, 1988
    locator: pages 115 to 131 (bisimilar states satisfy the same CTL* formulas, and for finite structures states with the same CTL formulas are bisimilar)
  - paper: doi:10.1137/0216062
    title: Robert Paige and Robert E. Tarjan, Three partition refinement algorithms, SIAM Journal on Computing 16(6), 1987
    locator: pages 973 to 989 (the relational coarsest partition problem in O(m log n) time)
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Sections 7.1 to 7.3 (bisimulation for transition systems, bisimulation and CTL*, and the quotienting algorithm)
---

A bisimulation is a relation between the states of transition systems in which related states can match each other's steps forever: if $s$ is related to $t$ and $s$ can do an action $a$ to $s'$, then $t$ can do $a$ to some $t'$ related to $s'$, and the same with the roles of $s$ and $t$ swapped. Two states are *bisimilar*, written $s \sim t$, if some bisimulation relates them. Bisimilarity is the largest bisimulation and an equivalence relation. It is the greatest fixed point of the matching condition, so it is a coinductive notion: one proves $s \sim t$ by showing one bisimulation that contains the pair. Park (1981) introduced bisimulation, and Milner made it the central equivalence of his calculus CCS. Bisimilarity is finer than [trace equivalence](/trace-equivalence/) and than mutual [simulation](/simulation-relation/), and it ignores nothing, unlike [stuttering equivalence](/stuttering-equivalence/). For image-finite systems it coincides with equality of Hennessy-Milner logic formulas (Hennessy and Milner 1985), and for finite Kripke structures with equality of CTL* formulas (Browne, Clarke and Grumberg 1988). So a model checker may replace a structure by its quotient modulo $\sim$, which Paige and Tarjan's algorithm computes in $O(m \log n)$ time; see [equivalence checking](/equivalence-checking/).

## Definition

**Labelled transition systems.** Let $(S, \mathit{Act}, \to)$ be a [labelled transition system](/labelled-transition-system/), with $s \xrightarrow{a} s'$ for $(s, a, s') \in {\to}$. A relation $R \subseteq S \times S$ is a *bisimulation* if for every $(s, t) \in R$ and every action $a$:

1. if $s \xrightarrow{a} s'$, there is $t'$ with $t \xrightarrow{a} t'$ and $(s', t') \in R$;
2. if $t \xrightarrow{a} t'$, there is $s'$ with $s \xrightarrow{a} s'$ and $(s', t') \in R$.

States $s$ and $t$ are *bisimilar*, $s \sim t$, if $(s, t) \in R$ for some bisimulation $R$. To compare two systems, take their disjoint union and compare their initial states.

**Kripke structures.** For a [Kripke structure](/kripke-structure/) $(S, R_T, L)$ with labelling $L : S \to 2^{\mathit{AP}}$, a relation $R$ is a bisimulation if every $(s, t) \in R$ has $L(s) = L(t)$ and the two transfer conditions hold for the single unlabelled transition relation. Two structures with initial states are bisimilar if every initial state of each is related to some initial state of the other.

**The greatest fixed point.** Define on the complete lattice of relations $2^{S \times S}$ the function
$$F(R) = \{(s, t) : \text{conditions 1 and 2 hold for } (s, t) \text{ with } R\}.$$
$F$ is monotone. A relation $R$ is a bisimulation if and only if $R \subseteq F(R)$, that is, $R$ is a post-fixed point. By the [Knaster-Tarski theorem](/knaster-tarski-theorem/), the union of all post-fixed points is the greatest fixed point $\nu F$, so
$$\sim \;=\; \bigcup \{R : R \subseteq F(R)\} \;=\; \nu F.$$
This gives the *coinduction principle*: to prove $s \sim t$, it is enough to find any $R$ with $(s, t) \in R \subseteq F(R)$.

**Basic facts.** The identity is a bisimulation, the inverse of a bisimulation is one, the composition of two bisimulations is one, and a union of bisimulations is one. So $\sim$ is an equivalence relation, and it is itself a bisimulation, the largest one.

**Approximants.** Let $\sim_0 = S \times S$ (or, for Kripke structures, the pairs with equal labels) and $\sim_{k+1} = F(\sim_k)$. Then $\sim_0 \supseteq \sim_1 \supseteq \cdots \supseteq \sim$. If the system is *image-finite*, that is every state has finitely many $a$-successors for each $a$, then $\sim \,=\, \bigcap_k \sim_k$. On a finite system the sequence becomes constant after at most $|S|$ steps, which gives the naive refinement algorithm.

**Hennessy-Milner logic.** Its formulas are $\varphi ::= \mathit{true} \mid \neg \varphi \mid \varphi \wedge \varphi \mid \langle a \rangle \varphi$, where $s \models \langle a \rangle \varphi$ if some $a$-successor of $s$ satisfies $\varphi$.

**Theorem (Hennessy and Milner, 1985).** In an image-finite system, $s \sim t$ if and only if $s$ and $t$ satisfy the same Hennessy-Milner formulas.

*Proof sketch.* Bisimilar states satisfy the same formulas, by induction on the formula. Conversely, show that the relation $E$ of "same formulas" is a bisimulation. Let $(s, t) \in E$ and $s \xrightarrow{a} s'$. If no $a$-successor $t'$ of $t$ is in relation $E$ with $s'$, then for each of the finitely many $t'_1, \ldots, t'_k$ there is a formula $\varphi_i$ true at $s'$ and false at $t'_i$. Then $\langle a \rangle (\varphi_1 \wedge \cdots \wedge \varphi_k)$ holds at $s$ and fails at $t$, which contradicts $(s, t) \in E$. ∎

**Theorem (Browne, Clarke and Grumberg, 1988).** For Kripke structures with total transition relations, bisimilar states satisfy the same [CTL\*](/ctl-star/) formulas. For finite Kripke structures the converse holds, and already CTL distinguishes any two states that are not bisimilar. In the same way, bisimilar states satisfy the same formulas of the [modal mu-calculus](/modal-mu-calculus/).

## Examples and non-examples

**A loop and its unfolding.** Let $s \xrightarrow{a} s$, and $t_0 \xrightarrow{a} t_1 \xrightarrow{a} t_0$. The relation $\{(s, t_0), (s, t_1)\}$ is a bisimulation: each $a$-step from $s$ goes back to $s$, and is matched by the $a$-step of $t_0$ to $t_1$, or of $t_1$ to $t_0$. So $s \sim t_0$. The quotient of the second system by $\sim$ is the first.

**The vending machines.** Let $p_0 \xrightarrow{a} p_1$, $p_1 \xrightarrow{b} p_2$, $p_1 \xrightarrow{c} p_3$, which pays ($a$) and then lets the user choose tea ($b$) or coffee ($c$). Let $q_0 \xrightarrow{a} q_1 \xrightarrow{b} q_2$ and $q_0 \xrightarrow{a} q_4 \xrightarrow{c} q_5$, which decides the drink when it takes the money. Both have the traces $\varepsilon, a, ab, ac$, so they are [trace equivalent](/trace-equivalence/). They are not bisimilar. The step $p_0 \xrightarrow{a} p_1$ must be matched by $q_0 \xrightarrow{a} q_1$ or $q_0 \xrightarrow{a} q_4$; but $p_1$ can do $c$ and $q_1$ cannot, and $p_1$ can do $b$ and $q_4$ cannot. The formula $\langle a \rangle (\langle b \rangle \mathit{true} \wedge \langle c \rangle \mathit{true})$ holds at $p_0$ and not at $q_0$. In CTL, with $b$ and $c$ as propositions of the target states, $\mathbf{AX}(\mathbf{EX}\,b \wedge \mathbf{EX}\,c)$ holds at one machine and not the other.

**Image-finiteness is needed.** Let $s$ have, for each $n \ge 1$, an $a$-step to the start of a path of $n - 1$ further $a$-steps that ends in a dead state. Let $t$ have the same steps, plus one $a$-step to a state $u$ with $u \xrightarrow{a} u$. A Hennessy-Milner formula of depth $d$ cannot tell $t$ from $s$, because the paths with $n > d$ look like the loop up to depth $d$. So $s$ and $t$ satisfy the same formulas. But $s \not\sim t$: the step $t \xrightarrow{a} u$ must be matched by a step of $s$ to a state that dies after finitely many steps, while $u$ never dies.

**Bisimilar but not isomorphic.** Bisimilarity ignores the number of copies: $a.\mathbf{0} + a.\mathbf{0}$ and $a.\mathbf{0}$ are bisimilar. A structure and its unwinding into an infinite tree are bisimilar.

## Related definitions

- [Simulation relation](/simulation-relation/): only condition 1. Bisimilarity implies mutual similarity, but not conversely; simulation preserves the universal fragment ACTL\*.
- [Stuttering equivalence](/stuttering-equivalence/): a weaker relation that lets one step be matched by several steps that do not change the labels. It preserves CTL\* without the next operator.
- [Trace equivalence](/trace-equivalence/): equality of the sets of action sequences. Bisimilarity implies it, and for deterministic systems the two coincide.
- Weak and branching bisimulation: versions for labelled systems with an internal action $\tau$, which may be matched by zero or more $\tau$-steps.
- [Equivalence checking](/equivalence-checking/): the decision problem. Kanellakis and Smolka (1990) gave an $O(mn)$ refinement algorithm, Paige and Tarjan (1987) an $O(m \log n)$ one, and Balcázar, Gabarró and Sántha (1992) showed that bisimilarity of finite systems is P-complete.
- [Partition refinement](/partition-refinement/) and [Hopcroft minimization](/hopcroft-minimization/): the general method behind the algorithms, and its special case for deterministic automata.

## References
