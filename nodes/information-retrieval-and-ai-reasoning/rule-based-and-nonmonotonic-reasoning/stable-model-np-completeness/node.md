---
tag: 5555AX
kind: theorem
slug: stable-model-np-completeness
name: NP-completeness of stable model existence
aliases:
- Marek-Truszczynski theorem
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: Deciding whether a finite propositional normal logic program has a stable model is NP-complete.
prereqs: [stable-model-semantics, np-complete, 3-sat]
see_also: [disjunctive-asp-sigma2-completeness, answer-set-programming, smodels-algorithm, conflict-driven-answer-set-solving, fages-theorem, well-founded-semantics, default-logic-complexity, autoepistemic-logic]
sources:
  - paper: doi:10.1145/116825.116836
    title: Victor W. Marek and Mirosław Truszczyński, Autoepistemic logic, Journal of the ACM 38(3) (1991)
    locator: the complexity results for stable expansions and for stable models of logic programs, including the NP-completeness of the existence of a stable model
  - paper: "Nicole Bidoit and Christine Froidevaux, Negation by default and unstratifiable logic programs, Theoretical Computer Science 78(1), 85 to 112 (1991)"
    locator: the complexity of the default semantics of logic programs, which coincides with the stable model semantics
  - paper: doi:10.1007/978-3-642-60085-2_17
    title: "Victor W. Marek and Mirosław Truszczyński, Stable models and an alternative logic programming paradigm, in Krzysztof R. Apt, Victor W. Marek, Mirosław Truszczyński and David S. Warren (eds.), The Logic Programming Paradigm: a 25-Year Perspective, Springer, 375 to 398 (1999)"
    locator: the section on the complexity of stable model existence
  - paper: doi:10.1145/502807.502810
    title: Evgeny Dantsin, Thomas Eiter, Georg Gottlob and Andrei Voronkov, Complexity and expressive power of logic programming, ACM Computing Surveys 33(3), 374 to 425 (2001)
    locator: the propositional complexity of normal programs under the stable model semantics, for existence, brave and cautious reasoning
  - paper: "Michael Gelfond and Vladimir Lifschitz, The stable model semantics for logic programming, in Robert A. Kowalski and Kenneth A. Bowen (eds.), Logic Programming: Proceedings of the Fifth International Conference and Symposium, MIT Press, 1070 to 1080 (1988)"
    locator: the definition of stable models
  - paper: "William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 267 to 284 (1984)"
    locator: the linear-time least model computation used in the membership proof
  - paper: doi:10.1023/a:1018930122475
    title: Ilkka Niemelä, Logic programs with stable model semantics as a constraint programming paradigm, Annals of Mathematics and Artificial Intelligence 25(3-4), 241 to 273 (1999)
    locator: the discussion of stable models as a language for NP search problems
---

This theorem places the main reasoning task of [answer set programming](/answer-set-programming/) exactly in the complexity landscape. A [stable model](/stable-model-semantics/) can be checked in linear time, so the existence question is in NP, and the even cycles of negation in a program can encode any [3-SAT](/3-sat/) instance, so it is NP-hard. The result is due to Marek and Truszczyński (1991), and Bidoit and Froidevaux (1991) proved it in an equivalent setting. It explains why stable model solvers search like SAT solvers, and why programs with disjunction, which reach one level higher, need [a different theorem](/disjunctive-asp-sigma2-completeness/).

## Statement

A *finite propositional normal program* $P$ is a finite set of rules $h \leftarrow b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_n$, where $h$, the $b_i$ and the $c_j$ are atoms from a finite set $A$ and $m, n \geq 0$. The program has no variables and no disjunction in the heads. For $M \subseteq A$, the reduct $P^M$ deletes each rule with some $c_j \in M$ and deletes the negative literals of the other rules. $M$ is a *stable model* if $M$ is the least model of $P^M$ (Gelfond and Lifschitz 1988). The size of $P$ is the number of rules plus the number of literals.

**Theorem** (Marek and Truszczyński 1991; Bidoit and Froidevaux 1991). The problem "given a finite propositional normal program $P$, does $P$ have a stable model?" is NP-complete.

The same holds when constraints $\leftarrow b_1, \ldots, \mathit{not}\ c_n$ are allowed, and NP-hardness holds already for programs in which each rule has at most three positive body atoms and at most one negative body literal.

## In plain words

To check a proposed answer, you only have to follow the rules forward once, which is fast. So the question is no harder than the problems where a good guess can be checked quickly. It is also no easier than any of them. A pair of rules that say "this is true unless that is true" and "that is true unless this is true" acts like a free choice between two values, one pair for each variable of a logic formula. One more rule for each clause of the formula rejects every choice that makes the clause false. So the program has an answer exactly when the formula can be satisfied, and a fast method for answers would give a fast method for every problem in NP.

## Proof

*Membership in NP.* A certificate is a set $M \subseteq A$. The reduct $P^M$ is computed in linear time, and its least model in linear time by the counter method of Dowling and Gallier (1984). Comparing it with $M$ takes linear time. With constraints, also check that $M$ satisfies no constraint body.

*NP-hardness.* We reduce [3-SAT](/3-sat/). Let $\varphi = C_1 \wedge \cdots \wedge C_k$ be a CNF formula over the variables $x_1, \ldots, x_n$. Use the atoms $x_i$ and $\bar{x}_i$ for each variable and one more atom $f$. For a literal $l$, let $\sigma(l)$ be the atom that says that $l$ is false: $\sigma(x_i) = \bar{x}_i$ and $\sigma(\neg x_i) = x_i$. The program $P_\varphi$ has the rules

$$x_i \leftarrow \mathit{not}\ \bar{x}_i, \qquad \bar{x}_i \leftarrow \mathit{not}\ x_i \qquad (1 \leq i \leq n),$$

$$f \leftarrow \sigma(l_1), \ldots, \sigma(l_r), \mathit{not}\ f \qquad \text{for each clause } C = l_1 \vee \cdots \vee l_r.$$

It has $2n + k$ rules and is built in linear time. For an assignment $\tau$, let $M_\tau = \{x_i : \tau(x_i) = 1\} \cup \{\bar{x}_i : \tau(x_i) = 0\}$.

(a) *Every stable model $M$ is $M_\tau$ for some $\tau$ and does not contain $f$.* If $f \in M$, the reduct deletes every rule with head $f$, so $f$ is not in the least model, a contradiction. If neither $x_i$ nor $\bar{x}_i$ is in $M$, the reduct keeps the fact $x_i \leftarrow$, so $x_i$ is in the least model, a contradiction. If both are in $M$, the reduct deletes both rules, and no other rule has $x_i$ as its head, a contradiction.

(b) *$M_\tau$ is a stable model if and only if $\tau$ satisfies $\varphi$.* The reduct by $M_\tau$ keeps exactly the facts $x_i \leftarrow$ with $\tau(x_i) = 1$, the facts $\bar{x}_i \leftarrow$ with $\tau(x_i) = 0$, and the rules $f \leftarrow \sigma(l_1), \ldots, \sigma(l_r)$, since $f \notin M_\tau$. Its least model is $M_\tau$, plus $f$ if the body of some clause rule lies in $M_\tau$. That body lies in $M_\tau$ exactly when every literal of the clause is false under $\tau$. So the least model equals $M_\tau$ exactly when $\tau$ satisfies every clause.

By (a) and (b), $\tau \mapsto M_\tau$ is a bijection between the satisfying assignments of $\varphi$ and the stable models of $P_\varphi$. In particular, $P_\varphi$ has a stable model if and only if $\varphi$ is satisfiable. Each clause rule has at most three positive atoms and one negative literal. With constraints, the clause rules can be written $\leftarrow \sigma(l_1), \ldots, \sigma(l_r)$ without $f$. $\square$

*Example.* For $\varphi = (x_1 \vee x_2) \wedge (\neg x_1 \vee x_3) \wedge (\neg x_2 \vee \neg x_3)$, the constraint version of $P_\varphi$ has the six choice rules and the constraints $\leftarrow \bar{x}_1, \bar{x}_2$, $\leftarrow x_1, \bar{x}_3$ and $\leftarrow x_2, x_3$. Its stable models are $\{\bar{x}_1, x_2, \bar{x}_3\}$ and $\{x_1, \bar{x}_2, x_3\}$, and the satisfying assignments of $\varphi$ are $(0, 1, 0)$ and $(1, 0, 1)$.

## Consequences

- **Brave and cautious reasoning.** Deciding whether an atom $a$ is in some stable model is NP-complete: add the constraint $\leftarrow \mathit{not}\ a$. Deciding whether $a$ is in every stable model is coNP-complete: it fails exactly when the program with $\leftarrow a$ added has a stable model (Dantsin, Eiter, Gottlob and Voronkov 2001).
- **Search is needed.** Unless P = NP, no polynomial algorithm finds stable models. Solvers such as the [smodels search](/smodels-algorithm/) and [conflict-driven answer set solving](/conflict-driven-answer-set-solving/) use the methods of SAT solvers for this reason.
- **ASP solves exactly NP.** Every problem in NP can be written as a program whose stable models are the certificates, by the construction above applied to a SAT encoding obtained from the [Cook-Levin theorem](/cook-levin-theorem/). This is the basis of the claim that ASP captures NP search problems.
- **Polynomial approximations.** The [well-founded model](/well-founded-semantics/) is computed in polynomial time and is contained in every stable model, so it can prune the search but cannot decide existence.

## Tightness

- **Hard even for tight programs.** The program $P_\varphi$ has no positive cycle: the atoms $x_i$ and $\bar{x}_i$ have no positive body, and $f$ depends positively only on these atoms. So the problem stays NP-complete on [tight programs](/fages-theorem/), where stable models are the models of the completion.
- **Polynomial cases.** For a program without negation the unique stable model is the least model, found in linear time. For a [stratified program](/stratified-logic-program/) the unique stable model is the perfect model, also found in polynomial time. So some negation through a cycle is necessary for hardness, and $P_\varphi$ uses even cycles of length two.
- **Disjunction goes higher.** For disjunctive programs, existence is $\Sigma_2^p$-complete ([Eiter and Gottlob 1995](/disjunctive-asp-sigma2-completeness/)); for head-cycle-free disjunctive programs it stays in NP.
- **Variables go higher.** For programs with variables and no function symbols, the problem is NEXPTIME-complete when the program is part of the input, and NP-complete when the program is fixed and only the facts vary (Dantsin, Eiter, Gottlob and Voronkov 2001).

## History

Gelfond and Lifschitz defined stable models in 1988. Marek and Truszczyński (1991) studied autoepistemic logic, whose stable expansions correspond to stable models through Gelfond's translation, and proved among other results that the existence of a stable model of a finite propositional program is NP-complete. Bidoit and Froidevaux (1991) obtained the same bound for their default semantics of logic programs, which coincides with the stable model semantics. Marek and Truszczyński (1999) and Niemelä (1999) later used the result to argue that logic programs with stable models are a language for NP search problems, which started answer set programming as a programming method.

## References
