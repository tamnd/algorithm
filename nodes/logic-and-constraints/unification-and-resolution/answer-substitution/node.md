---
tag: 98NXYB
kind: concept
slug: answer-substitution
name: Answer substitution
aliases:
- computed answer
- computed answer substitution
- correct answer substitution
area: logic-and-constraints/unification-and-resolution
level: intro
summary: A computed answer is the composition of the mgus of an SLD refutation, restricted to the query variables. Computed answers are correct, and every correct answer is an instance of one.
prereqs: [sld-resolution, unification-problem]
see_also: [logic-programming, horn-clause, sldnf-resolution, robinson-unification, most-general-unifier, refutation, herbrand-universe, first-order-theorem-proving]
sources:
  - book: isbn:9783540181996
    title: John W. Lloyd, Foundations of Logic Programming, second edition, Springer (1987)
    locator: Chapter 1 (correct answer substitutions) and Chapter 2 (computed answer substitutions, soundness and completeness of SLD resolution)
  - paper: doi:10.1145/322326.322339
    title: Krzysztof R. Apt and Maarten H. van Emden, Contributions to the theory of logic programming, Journal of the ACM 29(3), 841 to 862 (1982)
    locator: the soundness and completeness of SLD resolution with respect to answers
  - paper: "Cordell Green, Application of theorem proving to problem solving, Proceedings of the First International Joint Conference on Artificial Intelligence (IJCAI), 219 to 239 (1969)"
    locator: the answer literal, which extracts values of existential variables from a resolution refutation
  - book: isbn:9780262691635
    title: Leon Sterling and Ehud Shapiro, The Art of Prolog, second edition, MIT Press (1994)
    locator: the chapters on the computation model of logic programs and of Prolog (answers to queries, substitutions and instances)
---

An answer substitution gives values to the variables of a query to a [logic program](/logic-programming/). There are two notions. A *correct answer* is defined by logic: a substitution $\theta$ for the query $\leftarrow Q$ is correct for the program $P$ if $\forall\, Q\theta$ follows from $P$. A *computed answer* is defined by the procedure: it is the composition of the most general unifiers used in an [SLD refutation](/sld-resolution/), restricted to the variables of the query. Soundness says that every computed answer is correct, and completeness says that every correct answer is an instance of a computed answer. So the computed answers are the most general correct ones, and a computed answer may still contain variables.

## In plain words

When you ask a logic program a question with unknowns, such as "who is reachable from $a$?", the answer is a list of values for the unknowns. The machine finds them as a side effect of its proof: each step matches a goal against a rule and records what the variables must be. At the end of a successful proof, the records for the variables of the question are the answer. If a variable is not fixed by the proof, it stays a variable, and the answer means "this holds for every value".

## The idea

**Substitutions.** A substitution $\theta = \{x_1/t_1, \ldots, x_n/t_n\}$ replaces each variable $x_i$ by the term $t_i$. Applying $\theta$ to an expression $E$ gives the instance $E\theta$. Composition $\theta\sigma$ applies $\theta$ first, then $\sigma$. The restriction $\theta|_V$ keeps only the bindings of the variables in $V$.

**Correct answers.** Let $P$ be a definite program and $\leftarrow Q$ a query, with $Q = A_1 \wedge \cdots \wedge A_k$. A substitution $\theta$ for the variables of $Q$ is a *correct answer* if $P \models \forall\, (A_1 \wedge \cdots \wedge A_k)\theta$. This definition uses only the program and logic, not any procedure. It is the declarative meaning of an answer.

**Computed answers.** Let $G_0 = \leftarrow Q, G_1, \ldots, G_n = \square$ be an SLD refutation, where step $i$ uses the most general unifier $\theta_i$. The *computed answer* is $(\theta_1 \theta_2 \cdots \theta_n)|_{\mathrm{vars}(Q)}$. The restriction removes the bindings of the renamed clause variables, which are internal to the proof. Different refutations of the same query can give different computed answers; the set of all computed answers does not depend on the [computation rule](/sld-resolution/), but the order in which a search finds them does.

**Soundness and completeness.** These two theorems link the procedure to the logic. They are proved on the [SLD resolution](/sld-resolution/) page, following Clark (1979) and Lloyd (1987).

- *Soundness.* Every computed answer is a correct answer.
- *Completeness.* For every correct answer $\theta$ there is a computed answer $\sigma$ and a substitution $\gamma$ with $\theta = \sigma\gamma$ on the variables of the query. That is, $\theta$ is an instance of $\sigma$.

Completeness is up to instances: the procedure gives the most general forms, and the correct answer itself may never appear. It also needs a fair search, such as breadth-first search of the SLD tree. Prolog's depth-first search may loop before it reaches a refutation, so in Prolog an answer that exists may never be printed.

**Answers in resolution theorem proving.** Green (1969) used the same idea for general clauses. To prove $\exists x\, F(x)$, add the clause for $\neg F(x) \vee \mathit{ans}(x)$, with a new predicate $\mathit{ans}$, and resolve until a clause with only $\mathit{ans}$ literals remains. Its arguments give the answer. For Horn clauses this clause is always a single literal $\mathit{ans}(t)$, so there is one answer per refutation. For general clauses it can be a disjunction $\mathit{ans}(t_1) \vee \mathit{ans}(t_2)$: the proof shows that one of the values works, but not which one.

**With negation.** In [SLDNF resolution](/sldnf-resolution/), computed answers are defined in the same way, and negative literals contribute no bindings, because they are only selected when ground. The computed answers are sound for the program's completion, but completeness fails in general.

## Examples

**Two answers from two refutations.** Take the facts $e(a, b)$, $e(b, c)$ and the rules

$$
\begin{aligned}
&\mathit{path}(X, Y) \leftarrow e(X, Y), \\
&\mathit{path}(X, Y) \leftarrow e(X, Z), \mathit{path}(Z, Y).
\end{aligned}
$$

For the query $\leftarrow \mathit{path}(a, W)$, the first refutation uses the first rule, renamed to $\mathit{path}(X_1, Y_1) \leftarrow e(X_1, Y_1)$, with mgu $\{X_1/a, Y_1/W\}$, and then the fact $e(a, b)$ with mgu $\{W/b\}$. The composition is $\{X_1/a, Y_1/b, W/b\}$, and the restriction to $\{W\}$ is the computed answer $\{W/b\}$. A second refutation uses the second rule, then $e(a, b)$, then the first rule and $e(b, c)$, and gives $\{W/c\}$. These are all the computed answers, and indeed the correct ground answers are exactly $W = b$ and $W = c$.

**An answer with a variable.** With the program for list joining,

```text
app([], L, L).
app([H | T], L, [H | R]) ← app(T, L, R).
```

the query $\leftarrow \mathit{app}([a], Y, Z)$ has one refutation. The second clause, renamed with $H_1, T_1, L_1, R_1$, unifies with mgu $\{H_1/a, T_1/[\,], L_1/Y, Z/[a \mid R_1]\}$. The new goal $\leftarrow \mathit{app}([\,], Y, R_1)$ unifies with the renamed first clause $\mathit{app}([\,], L_2, L_2)$ with mgu $\{L_2/Y, R_1/Y\}$. The computed answer is $\{Z/[a \mid Y]\}$. It leaves $Y$ free, so it stands for the infinitely many correct answers $\{Y/s, Z/[a \mid s]\}$, one for each term $s$.

**A correct answer that is never computed.** Let $P = \{p(X) \leftarrow\}$ and the query $\leftarrow p(Y)$. The only computed answer is the identity substitution $\varepsilon$ (the mgu binds the clause variable to $Y$, and the restriction removes it). The substitution $\{Y/a\}$ is a correct answer, since $P \models p(a)$, but it is not computed. It is an instance of $\varepsilon$, which is what completeness promises.

**Restriction matters.** Without the restriction, the first path answer would include $X_1/a$ and $Y_1/b$. These variables come from a renamed copy of a clause and have no meaning for the user, and their names change from run to run.

## Where it is used

- **Prolog and Datalog systems.** The printed answers to a query, such as `W = b ; W = c`, are the computed answers, found one at a time on [backtracking](/chronological-backtracking/). Datalog engines, which compute bottom-up, return the ground correct answers instead.
- **Program semantics.** Semantics based on computed answers, such as the s-semantics of Falaschi, Levi, Martelli and Palamidessi, model a program by its non-ground answers, which is finer than the least Herbrand model.
- **Question answering in theorem provers.** Green's answer literal is still used in resolution provers to extract witnesses, for example in program synthesis from proofs.
- **Abstract interpretation of logic programs.** Analyzers approximate the set of computed answers to find types, modes and sharing of variables.

## References
