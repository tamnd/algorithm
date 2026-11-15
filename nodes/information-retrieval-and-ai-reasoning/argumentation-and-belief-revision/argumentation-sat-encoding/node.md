---
tag: RCX19M
kind: technique
slug: argumentation-sat-encoding
name: SAT encoding of argumentation semantics
aliases:
- Besnard-Doutre encoding
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: research
summary: Encodes conflict-freeness, admissibility and stability as propositional formulas so SAT solvers enumerate extensions.
prereqs: [abstract-argumentation-framework, admissible-set, sat]
see_also: [argument-labelling, dpll, cdcl, tseitin-transformation, stable-extension-argumentation, preferred-extension, preferred-semantics-complexity, argument-acceptance-problem]
sources:
  - paper: "Philippe Besnard and Sylvie Doutre, Checking the acceptability of a set of arguments, in James P. Delgrande and Torsten Schaub (eds), 10th International Workshop on Non-Monotonic Reasoning (NMR 2004), 59 to 64 (2004)"
    locator: the whole paper (propositional formulas whose models are the conflict-free sets and the stable, admissible and complete extensions of a framework)
  - paper: doi:10.1016/0004-3702(94)00041-X
    title: Phan Minh Dung, On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games, Artificial Intelligence 77(2), 321 to 357 (1995)
    locator: Section 2 (conflict-free, admissible, complete and stable sets)
  - paper: "Yannis Dimopoulos and Alberto Torres, Graph theoretical structures in logic programs and default theories, Theoretical Computer Science 170(1-2), 209 to 244 (1996)"
    locator: the whole paper (credulous acceptance under stable and preferred semantics is NP-complete)
  - paper: doi:10.1016/S0004-3702(02)00261-8
    title: Paul E. Dunne and Trevor J. M. Bench-Capon, Coherence in finite argument systems, Artificial Intelligence 141(1-2), 187 to 203 (2002)
    locator: the whole paper (sceptical acceptance under preferred semantics is Pi2P-complete)
  - paper: "Wolfgang Dvořák, Matti Järvisalo, Johannes Peter Wallner and Stefan Woltran, Complexity-sensitive decision procedures for abstract argumentation, Artificial Intelligence 206, 53 to 78 (2014)"
    locator: the whole paper (iterated SAT calls for the problems on the second level of the polynomial hierarchy)
  - book: isbn:9781848902756
    title: Wolfgang Dvořák and Paul E. Dunne, Computational problems in formal argumentation and their complexity, in Pietro Baroni, Dov Gabbay, Massimiliano Giacomin and Leendert van der Torre (eds), Handbook of Formal Argumentation, volume 1, College Publications (2018)
    locator: Section 3.3 (Table 1, the complexity of the reasoning problems that the encodings solve)
---

The SAT encoding of argumentation semantics turns the question "which sets of arguments does this semantics accept?" into a propositional formula. Each argument gets a variable, the formula states the conditions of the semantics, and the models of the formula are exactly the extensions. Philippe Besnard and Sylvie Doutre (2004) gave such formulas for conflict-free sets and for stable, admissible and complete extensions. A [SAT](/sat/) solver then finds one extension, decides whether an argument is credulously or sceptically accepted, or enumerates all extensions with blocking clauses. Many solvers for abstract argumentation work this way, and for preferred semantics they call the solver many times.

## In plain words

Give every argument a switch: on means accepted, off means rejected. Each rule of a semantics is a rule about switches. "Two arguments that attack each other are not both on" is one rule. "If an argument is on, each of its attackers is attacked by something that is on" is another. Write all these rules as one long logical formula. A SAT solver finds switch settings that obey every rule, and each such setting is an acceptable set of arguments.

To list all the sets, ask the solver for one, then add a rule that forbids exactly that setting, and ask again. To check whether an argument can be accepted, add the rule "this switch is on" and ask once.

## When it applies

The technique applies to a finite [abstract argumentation framework](/abstract-argumentation-framework/) $F = (A, R)$ and to any semantics whose sets can be described by conditions on each argument and its attackers. Use it when:

- the problem is NP-hard or coNP-hard, for example credulous acceptance under stable or preferred semantics, which is NP-complete (Dimopoulos and Torres 1996);
- the frameworks are large and a modern [CDCL](/cdcl/) solver will beat a hand-written search;
- all extensions are wanted, or a witness extension is wanted for an answer.

It is not needed for grounded semantics, which a [linear-time propagation](/grounded-extension-algorithm/) computes. For problems on the second level of the [polynomial hierarchy](/polynomial-hierarchy/), such as sceptical acceptance under preferred semantics, which is $\Pi_2^P$-complete (Dunne and Bench-Capon 2002), one SAT call is not enough unless the hierarchy collapses. Then the encoding is used inside a loop of calls.

## The template

**Step 1: variables.** For each argument $a$ take a variable $\mathit{in}_a$, true when $a \in S$. For clauses of small size, also take $\mathit{out}_a$, true when $a \in S^+$, that is, when some attacker of $a$ is in $S$. Write $a^-$ for the set of the attackers of $a$.

**Step 2: define the out variables.** For each argument $a$:

$$\mathit{out}_a \leftrightarrow \bigvee_{b \in a^-} \mathit{in}_b,$$

which is the clause $\neg \mathit{out}_a \vee \bigvee_{b \in a^-} \mathit{in}_b$ and the clauses $\mathit{out}_a \vee \neg \mathit{in}_b$ for each $b \in a^-$. These are the clauses of the [Tseitin transformation](/tseitin-transformation/). In every model, $\mathit{out}_a$ is fixed by the in variables, so each set $S$ has at most one model.

**Step 3: the conditions of the semantics.** Add, for each argument $a$:

| semantics | clauses for argument $a$ | meaning |
|---|---|---|
| conflict-free | $\neg \mathit{in}_a \vee \neg \mathit{in}_b$ for each $b \in a^-$ | no attack inside $S$ |
| [admissible](/admissible-set/) | conflict-free, and $\neg \mathit{in}_a \vee \mathit{out}_b$ for each $b \in a^-$ | $S$ attacks each attacker of its members |
| [complete](/complete-extension/) | admissible, and $\mathit{in}_a \vee \bigvee_{b \in a^-} \neg \mathit{out}_b$ | $S$ also contains each argument it defends |
| [stable](/stable-extension-argumentation/) | conflict-free, and $\mathit{in}_a \vee \mathit{out}_a$ | each argument is in $S$ or attacked by $S$ |

A self-attack $(a, a)$ gives the unit clause $\neg \mathit{in}_a$. An argument with no attacker gets the unit clause $\neg \mathit{out}_a$, and under complete semantics the unit clause $\mathit{in}_a$.

**Step 4: the size.** With $n = |A|$ and $m = |R|$, there are $2n$ variables and $O(n + m)$ clauses with $O(n + m)$ literals in total. The encoding is built in linear time.

**Step 5: ask the solver.** One call finds an extension or shows that none exists. Read $S = \{a : \mathit{in}_a\}$ from the model. Any complete solver works. The code of this page uses a small [DPLL](/dpll/) solver with unit propagation, and a CDCL solver is the choice for large frameworks.

**Step 6: enumerate.** After each model with set $S$, add the blocking clause $\bigvee_{a \in S} \neg \mathit{in}_a \vee \bigvee_{a \notin S} \mathit{in}_a$ and call again. By step 2 the models and the sets are one to one, so each extension is found once.

Without the out variables, the conditions are the formulas that Besnard and Doutre (2004) use, over the in variables only. Stable: $\bigwedge_a \big(\mathit{in}_a \leftrightarrow \bigwedge_{b \in a^-} \neg \mathit{in}_b\big)$. Admissible: $\bigwedge_a \big(\mathit{in}_a \rightarrow \bigwedge_{b \in a^-} (\neg \mathit{in}_b \wedge \bigvee_{c \in b^-} \mathit{in}_c)\big)$. Complete: the admissible formula with $\leftrightarrow$ in place of $\rightarrow$ for the defence part. The stable and admissible formulas are already short clauses. The complete one is not: its "if defended then in" direction becomes a [CNF](/conjunctive-normal-form/) of exponential size when the "or" is distributed, which is why the out variables are used.

## Classic examples

**A worked case.** Take $A = \{a, b, c, d\}$ with $a \leftrightarrow b$, $b \to c$ and $c \to d$. The stable encoding has $8$ variables and $16$ clauses: four clauses that bound each out variable from above, four of the form $\mathit{out}_x \vee \neg \mathit{in}_y$, four conflict clauses and four clauses $\mathit{in}_x \vee \mathit{out}_x$. Since $a$ and $b$ attack each other, $\mathit{in}_a \vee \mathit{out}_a$ forces $\mathit{in}_a$ or $\mathit{in}_b$.

- If $\mathit{in}_a$, then $\neg \mathit{in}_b$ by the conflict clause, $c$ has no attacker in $S$, so $\neg \mathit{out}_c$ and then $\mathit{in}_c$, and so $\neg \mathit{in}_d$. The set is $\{a, c\}$.
- If $\mathit{in}_b$, then $\mathit{out}_a$ and $\mathit{out}_c$, so $d$ has no attacker in $S$, and $\mathit{in}_d$. The set is $\{b, d\}$.

So the stable extensions are $\{a, c\}$ and $\{b, d\}$. With the complete encoding the solver also finds $\emptyset$, the grounded extension, and with the admissible encoding it finds $\emptyset$, $\{a\}$, $\{b\}$, $\{a, c\}$ and $\{b, d\}$. The page's tests check this case and compare the enumeration with brute force on random frameworks.

**Credulous acceptance.** Is $a$ in some preferred extension? Every admissible set lies in a preferred one, so the question is whether the admissible encoding plus the unit clause $\mathit{in}_a$ is satisfiable. That is one SAT call for an NP-complete problem.

**Sceptical acceptance under stable semantics.** $a$ is in every stable extension exactly when the stable encoding plus $\neg \mathit{in}_a$ is unsatisfiable. Note that with no stable extension at all, every argument is sceptically accepted under this definition.

**Preferred extensions by iterated calls.** Find an admissible set $S$. Then ask for an admissible set that contains $S$ and at least one more argument: add the unit clauses $\mathit{in}_a$ for $a \in S$ and the clause $\bigvee_{a \notin S} \mathit{in}_a$. Repeat until the answer is "no": $S$ is then a [preferred extension](/preferred-extension/). Add the clause $\bigvee_{a \notin S} \mathit{in}_a$ to the main formula, so that no subset of $S$ is found again, and start over. This is how the iterated SAT solvers enumerate preferred extensions, and Dvořák, Järvisalo, Wallner and Woltran (2014) use loops of this kind for sceptical preferred acceptance.

## Variations

- **Labelling encodings.** With the [labelling](/argument-labelling/) view, the in and out variables are the labels in and out, and undec is "neither". The clauses of step 3 are then the rules of complete labellings, one argument at a time.
- **Answer set programming.** The same conditions are a short logic program, and an ASP solver can handle the maximality of preferred semantics with its own optimization. See [answer set programming](/answer-set-programming/).
- **Quantified Boolean formulas.** Preferred and semi-stable semantics need "no larger admissible set exists", which is a universal quantifier. A [QBF](/qbf/) with one more alternation states it directly.
- **Incremental solving.** The loops above add clauses and call again on almost the same formula. An [incremental SAT](/incremental-sat/) solver keeps the learned clauses between calls, which saves much of the work.
- **Range variables.** For semi-stable and stage semantics, $\mathit{in}_a \vee \mathit{out}_a$ says that $a$ is in the range $S \cup S^+$, and maximizing the range becomes a loop of the same kind.

## Pitfalls

- **Missing out definitions.** If the clause $\neg \mathit{out}_a \vee \bigvee_{b \in a^-} \mathit{in}_b$ is left out, a model can set $\mathit{out}_a$ to true with no attacker of $a$ in $S$. The admissible encoding then accepts sets that are not admissible, and the blocking clauses of step 6 can find the same set more than once.
- **Distributing the defence.** Writing "defended implies in" directly in CNF without auxiliary variables multiplies the clause sizes and can blow up the formula.
- **Blocking on all variables.** Block on the in variables only. With auxiliary variables that are not fixed by the in variables, blocking whole models lists the same extension many times.
- **Preferred is not one call.** Maximality is not a property of one model. A single SAT call gives an admissible set, not a preferred one.
- **Empty extension.** The empty set is admissible in every framework, and it is the grounded extension whenever every argument has an attacker. A solver that returns $\emptyset$ has not failed.
- **Unconstrained variables.** An argument that attacks nothing and is not attacked appears in no clause of the admissible encoding. Its in variable is free, and the enumeration must give it both values.

## Exercises

1. Write the complete encoding for the 3-cycle $a \to b \to c \to a$, and show that its only model has all in variables false.
2. Show that for the stable encoding, the clauses $\mathit{out}_a \vee \neg \mathit{in}_b$ can be dropped without changing the set of the in parts of the models, but the clauses $\neg \mathit{out}_a \vee \bigvee_{b \in a^-} \mathit{in}_b$ cannot. Is the same true for the admissible encoding?
3. Prove that the stable encoding with the out variables has exactly one model for each stable extension.
4. Give an encoding whose models are the sets $S$ that are admissible and contain a given set $T$. Use it to decide whether $T$ is inside some preferred extension.
5. Count the clauses of each encoding as a function of $n$ and $m$, and give a framework where the complete encoding without out variables has a clause count exponential in $n$ after distribution.

## References
