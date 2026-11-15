---
tag: 4TB81W
kind: algorithm
slug: perfectref-rewriting
name: PerfectRef query rewriting
aliases:
- DL-Lite query rewriting
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: research
summary: Rewrites a conjunctive query under a DL-Lite TBox into a union of conjunctive queries that gives the certain answers when it is run on the data alone.
solves: [ontology-mediated-query-answering]
model: word-ram
complexity:
  vars: {n: the number of atoms of the query, t: the size of the TBox}
  time: {worst: "(t n)^O(n)"}
  space: {extra: "(t n)^O(n)"}
properties: {deterministic: true, exact: true, saturation: true, data_independent: true}
history:
  year: 2007
  people: [Diego Calvanese, Giuseppe De Giacomo, Domenico Lembo, Maurizio Lenzerini, Riccardo Rosati]
  note: The DL-Lite family was introduced in 2005. The journal paper of 2007 gave PerfectRef for DL-Lite_R, proved it correct, and showed that query answering is in AC0 in data complexity.
prereqs: [dl-lite, tbox-and-abox, open-world-assumption]
see_also: [ontology-mediated-query-answering, chase-algorithm, query-containment-problem, chandra-merlin-theorem, most-general-unifier, el-classification, instance-checking, datalog]
sources:
  - paper: doi:10.1007/s10817-007-9078-x
    title: Diego Calvanese, Giuseppe De Giacomo, Domenico Lembo, Maurizio Lenzerini and Riccardo Rosati, Tractable reasoning and efficient query answering in description logics, the DL-Lite family, Journal of Automated Reasoning 39(3), 2007
    locator: pages 385 to 429 (the section on query answering in DL-Lite_R, with the algorithm PerfectRef, its termination and correctness, and the AC0 data complexity bound; general locator)
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: the chapter on query answering in DL-Lite (general locator)
---

PerfectRef is a query rewriting algorithm for DL-Lite$_R$: it turns a conjunctive query $q$ and a TBox $T$ into a finite union of conjunctive queries whose answers over any ABox, read as a plain database, are the certain answers of $q$ over $T$ and that ABox. It works by two steps applied until nothing new appears: it replaces one atom by an atom that implies it under an inclusion of $T$, and it merges two atoms that unify. The TBox is used only once, at rewriting time, so the data can stay in a relational database and the rewritten query runs there as SQL.

## In plain words

A company keeps its data in tables, and a small list of rules says how the terms are related, for example "every professor teaches something" and "whatever is taught is a course". A user asks "who teaches a course?". The table of teachers may be empty for a person who is only listed as a professor, yet by the rules that person teaches a course. Instead of adding the missing rows to the tables, the method changes the question. It writes down every other question whose answers must also be answers of the first one, such as "who is a professor?" and "who teaches anything?". All these questions together are asked of the plain tables, and the union of their answers is exactly what follows from the tables and the rules.

## The problem

A DL-Lite$_R$ TBox $T$ has concept inclusions $B_1 \sqsubseteq B_2$ and $B_1 \sqsubseteq \neg B_2$ between basic concepts $B ::= A \mid \exists P \mid \exists P^-$, and role inclusions $R_1 \sqsubseteq R_2$ and $R_1 \sqsubseteq \neg R_2$ between roles $R ::= P \mid P^-$ ([DL-Lite](/dl-lite/)). An ABox $A$ is a finite set of facts $A(a)$ and $P(a, b)$ ([TBox and ABox](/tbox-and-abox/)). A conjunctive query $q(\vec x) = \exists \vec y.\, \varphi$ is a conjunction of atoms $A(t)$ and $P(t_1, t_2)$ over the answer variables $\vec x$ and the bound variables $\vec y$. A tuple $\vec a$ of individuals is a certain answer if it is an answer of $q$ in every model of $(T, A)$. This is [ontology-mediated query answering](/ontology-mediated-query-answering/) under the [open world assumption](/open-world-assumption/).

The task of PerfectRef is to compute, from $q$ and $T$ alone, a union of conjunctive queries $Q$ with $\mathrm{cert}(q, T, A) = Q(A)$ for every ABox $A$ for which $(T, A)$ is consistent. Negative inclusions do not change the rewriting; they are used only for the consistency test.

## The algorithm

Every query is kept in a normal form $\tau(q)$: a variable that occurs once in the body and not in the head is written $\_$. An inclusion $I$ is applicable to an atom $g$ in these cases, and $\mathrm{gr}(g, I)$ is the new atom:

| atom $g$ | inclusion $I$ | $\mathrm{gr}(g, I)$ |
|---|---|---|
| $A(t)$ | $B \sqsubseteq A$ | $B(t)$ |
| $P(t, \_)$ | $B \sqsubseteq \exists P$ | $B(t)$ |
| $P(\_, t)$ | $B \sqsubseteq \exists P^-$ | $B(t)$ |
| $P(t_1, t_2)$ | $Q \sqsubseteq P$ or $Q^- \sqsubseteq P$ | $Q(t_1, t_2)$ or $Q(t_2, t_1)$ |

Here $B(t)$ stands for $A'(t)$, $Q(t, \_)$ or $Q(\_, t)$ when $B$ is $A'$, $\exists Q$ or $\exists Q^-$. The role inclusion row also covers $P^-$ on the right, with the two terms swapped.

```pseudo id=main
PERFECTREF(q, T)                      ▷ q and every new query are in the normal form τ
L1  PR ← {q}; TODO ← [q]
L2  while TODO is not empty do
L3      take q′ from TODO; for each atom g of q′ do
L4          for each inclusion I of T applicable to g do
L5              add τ(q′ with g replaced by gr(g, I)) to NEW
L6      for each pair of atoms g1, g2 of q′ with the same predicate do
L7          if g1 and g2 unify: add τ(reduce(q′, g1, g2)) to NEW
L8      for each q″ in NEW that is not in PR: add q″ to PR and to TODO
L9  return PR                         ▷ evaluate the union of PR over the ABox
```

Lines L3 to L5 go backwards through one inclusion: if $\mathrm{gr}(g, I)$ holds, then $g$ holds in every model of $T$. The condition $\_$ in the table matters. The inclusion $B \sqsubseteq \exists P$ only says that some $P$-successor exists, so it can stand in for $P(t, \_)$, where the successor is not used anywhere else, but not for $P(t, y)$ with $y$ shared by another atom. Lines L6 and L7 make such a shared variable unshared: unifying $P(x, y)$ with $P(\_, y)$ gives one atom $P(x, y)$, and after $\tau$ it is $P(x, \_)$, to which the existential inclusion applies. The reduction is what lets the algorithm see the anonymous elements that the TBox forces. Line L8 keeps the set of queries without repeats. No step makes new variables, so the set is finite and the loop stops.

## Example

The TBox is $\mathit{Professor} \sqsubseteq \exists \mathit{teaches}$ and $\exists \mathit{teaches}^- \sqsubseteq \mathit{Course}$, and the query is $q(x) = \exists y.\, \mathit{teaches}(x, y) \wedge \mathit{Course}(y)$. The run makes four queries:

| query | made at | from | step | body |
|---|---|---|---|---|
| $q_0$ | L1 | input | | $\mathit{teaches}(x, y) \wedge \mathit{Course}(y)$ |
| $q_1$ | L4, L5 | $q_0$ | $\mathit{Course}(y)$ with $\exists \mathit{teaches}^- \sqsubseteq \mathit{Course}$ | $\mathit{teaches}(x, y) \wedge \mathit{teaches}(\_, y)$ |
| $q_2$ | L6, L7 | $q_1$ | unify the two atoms, then $\tau$ | $\mathit{teaches}(x, \_)$ |
| $q_3$ | L4, L5 | $q_2$ | $\mathit{teaches}(x, \_)$ with $\mathit{Professor} \sqsubseteq \exists \mathit{teaches}$ | $\mathit{Professor}(x)$ |

The atom $\mathit{teaches}(x, y)$ of $q_0$ cannot use $\mathit{Professor} \sqsubseteq \exists \mathit{teaches}$, because $y$ is shared with $\mathit{Course}(y)$. Over the ABox $\{\mathit{Professor}(\mathit{ann}), \mathit{teaches}(\mathit{bob}, c_1)\}$ the query $q_0$ alone has no answer. The rewriting gives $\mathit{bob}$ from $q_1$ and $q_2$ and $\mathit{ann}$ from $q_3$, and $\{\mathit{ann}, \mathit{bob}\}$ is the set of certain answers. If the TBox also has $\mathit{AssocProf} \sqsubseteq \mathit{Professor}$ and the role inclusion $\mathit{lectures} \sqsubseteq \mathit{teaches}$, the rewriting has 10 queries.

## Correctness

Each step is sound: if a query added at line L5 or line L7 has a match in a model of $T$, the query it came from has a match with the same answer. So every tuple found over the ABox is a certain answer. For the other direction, the chase of $(T, A)$ is a model that maps into every model, so the certain answers are its answers on individuals. A match into the chase can be moved back one chase step at a time: the atoms that hit the newest fact are first merged by line L7, and the single atom left is then replaced at line L5 by the atom that hit the fact the step used. A new anonymous element occurs in only one fact when it is made, which is why the variable mapped to it is $\_$ after the merges. After as many moves as chase steps, some query of PR matches the ABox itself. The full proof, with termination and the exponential lower bound, is in proofs/correctness.md.

## Complexity

Let $q$ have $n$ atoms and $v$ variables, and let $m$ be the number of names in $T$ and $q$. Every query in PR has at most $n$ atoms over the $v$ variables and $\_$, so PR has at most $(m(v + 1)^2 + 1)^n$ queries, and the time is that bound times a polynomial in $n$ and $|T|$. For a fixed query this is polynomial in $|T|$; in $n$ it is exponential.

The exponential size can occur. For $T_n = \{B_i \sqsubseteq A_i : 1 \le i \le n\}$ and $q_n(x) = A_1(x) \wedge \dots \wedge A_n(x)$, PR has exactly $2^n$ queries, one for each choice of $A_i$ or $B_i$ at each position, and no union of conjunctive queries with fewer members is a correct rewriting. A positive existential query $\bigwedge_i (A_i(x) \vee B_i(x))$ has linear size here, so the blow-up belongs to the target language, not to the problem.

The rewriting does not look at the ABox. With $q$ and $T$ fixed, evaluating the union over the ABox is a fixed first-order query, so the data complexity of query answering in DL-Lite$_R$ is in AC$^0$ ([AC0](/ac0/)).

## Properties

- **Data independent.** The output depends only on $q$ and $T$. One rewriting serves every ABox, and the ABox is never changed.
- **Exact.** The union gives the certain answers, no more and no fewer, when $(T, A)$ is consistent.
- **Syntactic.** Every query of PR uses only the variables of $q$ and the names of $T$ and $q$; nothing anonymous is made.
- **Redundant.** PR often contains queries that are contained in others, such as $q_1$ and $q_2$ of the example. They give no new answers.

## Variants and improvements

- **Removing contained queries.** A query of PR that is contained in another one can be dropped; containment of conjunctive queries is decided by a homomorphism test ([query containment problem](/query-containment-problem/), [Chandra and Merlin](/chandra-merlin-theorem/)). This keeps the union smaller but does not avoid the exponential size in the example above.
- **Other target languages.** Rewriting into positive existential queries or into non-recursive [Datalog](/datalog/) can be much smaller than a union of conjunctive queries, and several later systems do this.
- **Functional roles.** For DL-Lite$_F$ the same algorithm works with the role inclusions left out; functionality, like negative inclusions, only takes part in the consistency test.
- **Consistency.** Each negative inclusion becomes a boolean query that asks for a violation, for example $\exists y.\, B_1(y) \wedge B_2(y)$, and it is rewritten and evaluated in the same way.
- **The chase.** The opposite approach adds the consequences to the data with the [chase](/chase-algorithm/). For DL-Lite the chase can be infinite, so it must be cut or folded, and the data must be changed when the TBox changes.

## When to use it

Use it when the data is large, kept in a relational database, and the ontology fits in DL-Lite, which is the basis of the OWL 2 QL profile. The database engine does all the work on the data, and the TBox only changes the SQL. Do not use it when the TBox has qualified existentials on the left, such as $\exists P.A \sqsubseteq A$, or disjunction: then certain answers are not first-order rewritable in general, and methods for [EL](/el-classification/) or for more expressive logics are needed. For long queries over deep hierarchies, the union can be too large to send to a database; a rewriting into a smaller target language fits better there.

## Pitfalls

- **Rewriting an atom with a shared variable.** Line L4 must apply $B \sqsubseteq \exists P$ only to an atom $P(t, \_)$. Applying it to $P(x, y)$ with $y$ used elsewhere is unsound. With only $\mathit{Professor} \sqsubseteq \exists \mathit{teaches}$ and the query $q_0$ of the example, the wrong step gives $\mathit{Professor}(x) \wedge \mathit{Course}(y)$, which returns $\mathit{ann}$ over $\{\mathit{Professor}(\mathit{ann}), \mathit{Course}(\mathit{db})\}$. But $\mathit{ann}$ is not a certain answer, because what she teaches need not be a course.
- **Skipping $\tau$ after a merge.** Line L7 must apply $\tau$ to the result of the reduction. Without it, $q_2$ of the example stays $\mathit{teaches}(x, y)$, line L4 does not see that $y$ is unbound, $q_3$ is never made, and $\mathit{ann}$ is missed.
- **Building the merged atom from one side.** At line L7, a position where one atom has $\_$ must take the term of the other atom. Keeping the $\_$ of the first atom loses a shared variable, and the result is wrong for some inputs; the random tests of the implementation found such cases in an early version.
- **Making fresh variables.** Line L8 compares queries by their syntax. If each step renamed the $\_$ variables into new names, no query would repeat and the loop would not stop on a cyclic TBox such as $\exists P \sqsubseteq \exists P^-$ and $\exists P^- \sqsubseteq \exists P$. Keeping all unbound variables as $\_$ is what bounds PR.
- **Ignoring consistency.** Line L9 gives the certain answers only for a consistent knowledge base. If the ABox violates a negative inclusion, every tuple is a certain answer, so the consistency test must run first.

## Implementations

## History

Calvanese, De Giacomo, Lembo, Lenzerini and Rosati introduced the DL-Lite family in 2005 as description logics in which query answering can be done by a relational database. Their journal paper of 2007 gave PerfectRef for DL-Lite$_R$ and DL-Lite$_F$, proved that it returns exactly the certain answers, and showed that conjunctive query answering is in AC$^0$ in data complexity. The OWL 2 QL profile of the Web Ontology Language is based on DL-Lite$_R$. Later work studied smaller rewritings, other target languages and lower bounds on the size of rewritings.

## References
