---
tag: 9DRC8Z
kind: definition
slug: clausal-normal-form
name: Clausal normal form
aliases:
- clausal form
- clause normal form
- CNF transformation
area: logic-and-constraints/unification-and-resolution
level: core
summary: A finite set of universally closed clauses that is satisfiable exactly when a given formula is. Distribution can make it exponential; definitions with new predicates keep it linear.
prereqs: [skolemization, conjunctive-normal-form, clause]
see_also: [prenex-normal-form, tseitin-transformation, plaisted-greenbaum-transformation, herbrand-theorem, robinson-resolution, standardization-apart, horn-clause, first-order-theorem-proving]
sources:
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 4, Section 4.2, Skolem standard forms (clauses, the set of clauses of a standard form, and Theorem 4.1 on unsatisfiability)
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 6, Andreas Nonnengart and Christoph Weidenbach, Computing small clause normal forms (the standard pipeline, structural renaming of subformulas and its effect on the number of clauses)
  - paper: "David A. Plaisted and Steven Greenbaum, A structure-preserving clause form translation, Journal of Symbolic Computation 2(3), 1986"
    locator: definitions of subformulas by new predicates, with one direction of the definition chosen by polarity, and the linear size of the result
  - paper: "G. S. Tseitin, On the complexity of derivation in propositional calculus, in A. O. Slisenko (ed.), Studies in Constructive Mathematics and Mathematical Logic, Part II, 1968"
    locator: the extension rule, which names a subformula by a new variable and gives a clause form of linear size
---

A **clausal normal form** of a closed first-order formula $F$ is a finite set $S$ of [clauses](/clause/) such that $S$ is satisfiable exactly when $F$ is. Each clause is a disjunction of [literals](/literal/), its variables are read as universally quantified, and the set is read as the conjunction of its clauses. Resolution and superposition provers take their input in this form. The standard route is negation normal form, [Skolemization](/skolemization/), and then [conjunctive normal form](/conjunctive-normal-form/) of the matrix. Distribution of $\vee$ over $\wedge$ can make the clause set exponential, and naming subformulas with new predicates, as in the [Tseitin transformation](/tseitin-transformation/), keeps it linear.

## Definition

A **literal** is an atom $A$ or its negation $\lnot A$. A **clause** is a finite set of literals $\{L_1, \ldots, L_m\}$, written $L_1 \vee \cdots \vee L_m$; the empty clause is $\square$. A structure $M$ **satisfies** a clause $C$ if for every assignment of the variables of $C$ some literal of $C$ is true, that is, if $M \models \forall \vec x \, C$, where $\vec x$ are the variables of $C$. $M$ satisfies a set $S$ of clauses if it satisfies every clause of $S$.

Each clause is closed on its own. Since $\forall x (A \wedge B) \equiv \forall x A \wedge \forall x B$, a set of clauses means the same thing when the variables of one clause are renamed apart from those of the others. Provers do this all the time; see [standardization apart](/standardization-apart/).

**Definition.** A clausal normal form of a closed formula $F$ is a finite set $S$ of clauses, over the signature of $F$ plus new function and predicate symbols, such that $S$ is satisfiable if and only if $F$ is.

Equivalence is not required, and in general it is not possible: Skolem symbols and definitions add new symbols.

**The standard construction.**

1. **Negation normal form.** Remove $\to$ and $\leftrightarrow$, push $\lnot$ down to the atoms, and rename bound variables apart. The result is equivalent to $F$.
2. **Skolemization.** Replace each $\exists y \, G$ by $G[f(\vec z)/y]$ with a new $f$, as on the [Skolemization](/skolemization/) page. The result is equisatisfiable with $F$.
3. **Drop the quantifiers.** Only $\forall$ is left, and a closed universal formula $\forall \vec x \, G$ with $G$ quantifier-free is satisfied by the same structures as the matrix $G$ read with free variables.
4. **Clauses.** Turn the quantifier-free $G$ into a set of clauses, by distribution or by definitions, as below.

**Distribution.** Use $A \vee (B \wedge C) \equiv (A \vee B) \wedge (A \vee C)$ until no $\wedge$ is below a $\vee$. The result is equivalent to $G$. It can be exponential, and this cannot be avoided without new symbols:

**Theorem 1.** Let $F_k = (A_1 \wedge B_1) \vee \cdots \vee (A_k \wedge B_k)$ with $2k$ distinct atoms. Every set of clauses over these atoms that is equivalent to $F_k$ has at least $2^k$ clauses. Distribution gives exactly $2^k$.

*Proof.* Let $S$ be equivalent to $F_k$, and drop the tautologies, which are true under every assignment. Let $C \in S$. If, for some $i$, neither $A_i$ nor $B_i$ is a positive literal of $C$, make every literal of $C$ false, which is possible because $C$ is not a tautology, set $A_i$ and $B_i$ true, which does not clash because neither occurs positively in $C$, and set the other atoms in any way. This assignment makes $F_k$ true and $C$ false, a contradiction. So every clause of $S$ has $A_i$ or $B_i$ as a positive literal, for each $i$. Now fix a choice $c = (c_1, \ldots, c_k)$ with $c_i \in \{A_i, B_i\}$, and let $\alpha_c$ make each $c_i$ false and the other atom of each pair true. Then each $A_i \wedge B_i$ is false, so $F_k$ is false, and some $C_c \in S$ is false under $\alpha_c$. All positive literals of $C_c$ are false under $\alpha_c$, so for each $i$ the positive literal from $\{A_i, B_i\}$ in $C_c$ is $c_i$, and the other atom of the pair is not positive in $C_c$. So $C_c$ determines $c$, and the $2^k$ choices give $2^k$ different clauses. Distribution gives the $2^k$ clauses $c_1 \vee \cdots \vee c_k$. $\square$

**Definitions (structural form).** For each subformula $H$ of the negation normal form $G$ that is not a literal, with free variables $\vec z$, take a new predicate $d_H$ and write $\ell(H)$ for $d_H(\vec z)$, and $\ell(L) = L$ for a literal $L$. Add the clauses

- $\lnot d_H(\vec z) \vee \ell(H_1)$ and $\lnot d_H(\vec z) \vee \ell(H_2)$ if $H = H_1 \wedge H_2$,
- $\lnot d_H(\vec z) \vee \ell(H_1) \vee \ell(H_2)$ if $H = H_1 \vee H_2$,

and the unit clause $\ell(G)$. Each definition is only an implication $d_H \to H$. This is the polarity-based form of Plaisted and Greenbaum; the [Tseitin transformation](/tseitin-transformation/) adds the converse implications as well.

**Theorem 2.** The structural form $D(G)$ has at most $2b + 1$ clauses of at most 3 literals each, where $b$ is the number of binary connectives of $G$, and $D(G)$ is satisfiable if and only if $\forall \vec x \, G$ is.

*Proof.* The size is clear from the construction: one or two clauses per connective and one unit. Suppose $M \models \forall \vec x \, G$. Expand $M$ by letting $d_H(\vec z)$ be true exactly when $H$ is true under $\vec z$. Then each clause $\lnot d_H \vee \ldots$ holds, because $d_H$ true means $H$ true, and $H$ true means both conjuncts, or one disjunct, true, and each $\ell(H_i)$ is then true by the same definition. The unit $\ell(G)$ holds because $G$ is true under every assignment. Conversely, let $M' \models D(G)$. By induction on $H$ from the literals up, for every assignment: if $\ell(H)$ is true, then $H$ is true. For a literal this is trivial. For $H = H_1 \wedge H_2$, $d_H$ true and the two clauses give $\ell(H_1)$ and $\ell(H_2)$ true, so by induction $H_1$ and $H_2$ are true. The case of $\vee$ is the same with one disjunct. The unit $\ell(G)$ is true under every assignment, so $G$ is true under every assignment, and $M'$ without the $d_H$ is a model of $\forall \vec x \, G$. $\square$

Together with the Skolemization theorem, every closed formula has a clausal normal form of size linear in the size of its negation normal form.

## Examples and non-examples

**The full route.** To prove $\forall x (P(x) \to Q(x)) \to (\forall x P(x) \to \forall x Q(x))$, negate it. In negation normal form the negation is $\forall x (\lnot P(x) \vee Q(x)) \wedge \forall y \, P(y) \wedge \exists z \lnot Q(z)$. Skolemization replaces $z$ by a constant $c$, and the clauses are

$$\lnot P(x) \vee Q(x), \quad P(x), \quad \lnot Q(c).$$

The variable $x$ of the first two clauses is two different variables. Resolution refutes the set in two steps: $Q(x)$ from the first two, then $\square$ with $\lnot Q(c)$.

**Distribution against definitions.** For $F_k$ of Theorem 1 the counts are:

| $k$ | distribution | structural |
|---|---|---|
| 1 | 2 | 3 |
| 2 | 4 | 6 |
| 3 | 8 | 9 |
| 4 | 16 | 12 |
| 10 | 1024 | 30 |
| 20 | 1048576 | 60 |

The structural form has $3k$ clauses: two for each $\wedge$, one for each of the $k - 1$ connectives $\vee$, and the unit. For $k \le 3$ distribution is smaller, so provers name a subformula only when this lowers the count.

**A first-order definition.** For $\forall x ((P(x) \wedge Q(x)) \vee R(x))$ distribution gives $P(x) \vee R(x)$ and $Q(x) \vee R(x)$. The structural form names $P(x) \wedge Q(x)$ by $d_1(x)$, whose argument is the free variable $x$, and gives $\lnot d_1(x) \vee P(x)$, $\lnot d_1(x) \vee Q(x)$, $\lnot d_2(x) \vee R(x) \vee d_1(x)$ and $d_2(x)$.

**Non-example: a shared variable.** $\forall x P(x) \vee \forall x Q(x)$ is not the clause $P(x) \vee Q(x)$, which says $\forall x (P(x) \vee Q(x))$. Its clausal form is $P(x) \vee Q(y)$, with two variables. The bound variables must be renamed apart in step 1.

**Non-example: equivalence.** $\{R(x, f(x))\}$ is a clausal normal form of $\forall x \exists y \, R(x, y)$, but it is not equivalent to it; see [Skolemization](/skolemization/).

**Non-example: a definition with too few arguments.** Naming $P(x) \wedge Q(x)$ by a nullary $d_1$ gives $\lnot d_1 \vee P(x)$, which says that $d_1$ implies $P$ of everything. Add the units $\lnot P(a)$ and $\lnot R(b)$ to the example. The formula is then satisfiable, with domain $\{a, b\}$, $P = Q = \{b\}$ and $R = \{a\}$. The wrong clauses $\lnot d_1 \vee P(x)$, $\lnot d_1 \vee Q(x)$, $R(x) \vee d_1$, $\lnot P(a)$, $\lnot R(b)$ are unsatisfiable: resolve $R(x) \vee d_1$ with $\lnot R(b)$ to get $d_1$, then $P(x)$, then $\square$ with $\lnot P(a)$. The predicate must take all free variables of the subformula.

## Related definitions

- [Conjunctive normal form](/conjunctive-normal-form/): the propositional case, with no variables and no Skolem symbols.
- [Clause](/clause/), [literal](/literal/), [unit clause](/unit-clause/) and [Horn clause](/horn-clause/): the parts of a clausal form, and the special shape used by logic programming.
- [Prenex normal form](/prenex-normal-form/) and [Skolemization](/skolemization/): the earlier steps of the classic route.
- [Tseitin transformation](/tseitin-transformation/) and [Plaisted-Greenbaum transformation](/plaisted-greenbaum-transformation/): the propositional versions of the structural form.
- [Herbrand's theorem](/herbrand-theorem/): a set of clauses is unsatisfiable exactly when some finite set of its ground instances is.

## References
