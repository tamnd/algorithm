---
tag: 86H5G1
kind: definition
slug: prenex-normal-form
name: Prenex normal form
aliases:
- prenex form
- prenex formula
area: logic-and-constraints/unification-and-resolution
level: intro
summary: A first-order formula with all its quantifiers in a prefix at the front and a quantifier-free matrix after them. Every formula has an equivalent prenex form.
prereqs: [term]
see_also: [skolemization, clausal-normal-form, herbrand-theorem, conjunctive-normal-form, first-order-theorem-proving]
sources:
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 3, The first-order logic (prenex normal forms and the laws used to move quantifiers), and Chapter 4, Section 4.2 (Skolem standard forms, built from a prenex form)
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 6, Andreas Nonnengart and Christoph Weidenbach, Computing small clause normal forms (prenex forms, miniscoping and their effect on Skolem functions)
---

A first-order formula is in **prenex normal form** when it has the shape $Q_1 x_1 \, Q_2 x_2 \cdots Q_k x_k \, M$, where each $Q_i$ is $\forall$ or $\exists$ and $M$ has no quantifiers. The quantifier string is the **prefix** and $M$ is the **matrix**. Every formula has a logically equivalent prenex form, which is the first step of the classic route to [Skolem form](/skolemization/) and [clausal form](/clausal-normal-form/). The prenex form is not unique, and the order of the prefix changes the [terms](/term/) that Skolemization later introduces.

## Definition

We use first-order formulas built from atoms with $\lnot$, $\wedge$, $\vee$, $\to$, $\leftrightarrow$, $\forall$ and $\exists$. A structure has a **nonempty** domain, as usual. Two formulas are **equivalent** if they have the same truth value in every structure under every assignment of the free variables.

**Definition.** A formula is in prenex normal form if it is $Q_1 x_1 \cdots Q_k x_k \, M$ with $k \ge 0$, $Q_i \in \{\forall, \exists\}$ and $M$ quantifier-free. A prenex form of $F$ is a prenex formula equivalent to $F$ with the same free variables.

**The quantifier laws.** For any formulas $F$ and $G$ such that $x$ is not free in $G$:

1. $\lnot \forall x F \equiv \exists x \lnot F$ and $\lnot \exists x F \equiv \forall x \lnot F$.
2. $\forall x F \wedge G \equiv \forall x (F \wedge G)$ and $\exists x F \vee G \equiv \exists x (F \vee G)$.
3. $\forall x F \vee G \equiv \forall x (F \vee G)$ and $\exists x F \wedge G \equiv \exists x (F \wedge G)$.

The same laws hold with $G$ on the left of $\wedge$ or $\vee$, since both connectives are commutative.

*Proof of the laws.* Fix a structure with domain $D \ne \emptyset$ and an assignment $\beta$. Write $\beta[x \mapsto d]$ for $\beta$ with $x$ sent to $d$. Since $x$ is not free in $G$, the truth value of $G$ under $\beta[x \mapsto d]$ is the truth value $g$ of $G$ under $\beta$, for every $d$. Law 1 is the definition of $\forall$ and $\exists$ with De Morgan's law. For law 3 with $\forall$: if $g$ is true, both sides are true; if $g$ is false, both sides say that $F$ holds for every $d$. For law 3 with $\exists$: if $g$ is false, both sides are false; if $g$ is true, both sides say that $F$ holds for some $d$. For law 2 with $\forall$: the right side says that for every $d \in D$, $F$ holds at $d$ and $g$ is true. If $g$ is true, this is the left side. If $g$ is false, the left side is false, and the right side is false because $D$ has an element $d$. The law for $\exists$ and $\vee$ is the dual: if $g$ is false, both sides say that $F$ holds for some $d$; if $g$ is true, the left side is true, and the right side is true because $D$ has an element. $\square$

The proof uses $D \ne \emptyset$ only in law 2. In the empty domain $\forall x \bot \wedge \bot$ is false and $\forall x (\bot \wedge \bot)$ is true.

**Theorem (existence).** Every formula $F$ has a prenex form. If $F$ has no $\leftrightarrow$, the matrix has at most as many connectives as $F$, and the prefix has one quantifier for each quantifier of $F$.

*Proof.* First rename bound variables so that each quantifier binds its own variable and no bound variable is also free in $F$. Renaming a bound variable to a fresh one gives an equivalent formula, because the truth value of $\forall x F$ under $\beta$ depends only on the values of $F$ under $\beta[x \mapsto d]$, and these do not change when $x$ and its bound occurrences are replaced by a variable that does not occur in $F$. Next replace $A \to B$ by $\lnot A \vee B$ and $A \leftrightarrow B$ by $(\lnot A \vee B) \wedge (A \vee \lnot B)$, and rename apart again the bound variables of the two copies.

Now prove by induction on $F$ that a formula with only $\lnot, \wedge, \vee, \forall, \exists$, whose bound variables are distinct and not free in $F$, has a prenex form with the same bound variables. Replacing a subformula by an equivalent one gives an equivalent formula, by induction on the context, and we use this at each step.

- An atom is prenex with $k = 0$.
- $F = \lnot F_1$. By induction $F_1 \equiv Q_1 x_1 \cdots Q_k x_k M$. Apply law 1 $k$ times, from the outside in: $F \equiv \bar Q_1 x_1 \cdots \bar Q_k x_k \lnot M$, where $\bar\forall = \exists$ and $\bar\exists = \forall$.
- $F = F_1 \circ F_2$ with $\circ \in \{\wedge, \vee\}$. By induction $F_1 \equiv Q_1 x_1 \cdots Q_k x_k M_1$ and $F_2 \equiv Q'_1 y_1 \cdots Q'_l y_l M_2$. The $x_i$ are bound in $F_1$, so they are not free in $F_2$ and are different from the $y_j$, and the same holds for the $y_j$. Apply law 2 or 3 to pull out $Q_1 x_1$, then $Q_2 x_2$, and so on, and then the $Q'_j y_j$. The result is $Q_1 x_1 \cdots Q_k x_k \, Q'_1 y_1 \cdots Q'_l y_l \, (M_1 \circ M_2)$.
- $F = Q x \, F_1$. By induction $F_1 \equiv$ a prenex $P$, so $F \equiv Q x \, P$, which is prenex.

In each case the matrix gets one connective for each connective of $F$, and the prefix gets one quantifier for each quantifier of $F$. $\square$

**Size.** Without $\leftrightarrow$ the prenex form has the size of $F$, up to renaming. Each $\leftrightarrow$ copies both sides, so a chain $A_1 \leftrightarrow (A_2 \leftrightarrow (\cdots \leftrightarrow A_d))$ whose parts have quantifiers grows by a factor of about $2$ for each level, that is, to size $2^{\Theta(d)}$. Provers avoid this with the structural clausal form of [clausal normal form](/clausal-normal-form/).

## Examples and non-examples

**Prenex.** $\forall x \exists y \, R(x, y)$, $\forall x (P(x) \to Q(x))$, and every quantifier-free formula, with $k = 0$.

**Not prenex.** $\forall x P(x) \vee \forall x Q(x)$: a quantifier lies under $\vee$. A prenex form needs two variables: $\forall x \forall y (P(x) \vee Q(y))$. The formula $\forall x (P(x) \vee Q(x))$ is prenex but **not** equivalent: in the domain $\{0, 1\}$ with $P = \{0\}$ and $Q = \{1\}$, every element is in $P$ or in $Q$, but neither set is the whole domain. This is why the proof renames bound variables apart first.

**The dual mistake.** $\exists x P(x) \wedge \exists x Q(x)$ is not equivalent to $\exists x (P(x) \wedge Q(x))$. The same structure is a counterexample: some element is in $P$ and some element is in $Q$, but no element is in both.

**A quantifier under an antecedent changes.** $(\forall x P(x)) \to Q(c)$ is $\lnot \forall x P(x) \vee Q(c)$, which is $\exists x (\lnot P(x) \vee Q(c))$, that is, $\exists x (P(x) \to Q(c))$. The formula $\forall x (P(x) \to Q(c))$ is not equivalent: with domain $\{0, 1\}$, $P = \{0\}$, $c = 0$ and $Q = \emptyset$, the first formula is true because $P$ is not the whole domain, and the second is false at $x = 0$.

**Two prenex forms of one formula.** Let

$$F = \forall x (P(x) \to \exists y \, R(x, y)) \wedge \lnot \forall x P(x).$$

Rename the second $x$ to $z$. Pulling out the left conjunct first gives $\forall x \exists y \exists z \, ((\lnot P(x) \vee R(x, y)) \wedge \lnot P(z))$. Pulling out the right conjunct first gives $\exists z \forall x \exists y \, ((\lnot P(x) \vee R(x, y)) \wedge \lnot P(z))$. Both are equivalent to $F$ by laws 2 and 3, since $x$ and $y$ are not free in $\lnot P(z)$ and $z$ is not free in the left conjunct. [Skolemization](/skolemization/) of the first form replaces $z$ by a term $g(x)$, while the second form gives a constant $c$. The second is better for a prover: $\lnot P(c)$ is ground, while $\lnot P(g(x))$ has a variable.

## Related definitions

- **Negation normal form.** Negation is only on atoms, and $\to$ and $\leftrightarrow$ are gone. The proof above produces it on the way, and it is the input form for the structural transformations.
- **Skolem normal form.** A prenex form with an all-$\forall$ prefix, made by [Skolemization](/skolemization/). It is equisatisfiable with the original formula, not equivalent.
- **Clausal normal form.** A Skolem form whose matrix is a [conjunctive normal form](/conjunctive-normal-form/), written as a set of [clauses](/clause/); see [clausal normal form](/clausal-normal-form/).
- **Miniscope form.** The opposite of prenex form: each quantifier is pushed in as far as the laws allow. Provers prefer it before Skolemization, because a Skolem function then takes fewer arguments.
- **Prefix classes.** Decidable fragments of [first-order theorem proving](/first-order-theorem-proving/) are often named by the prefix of the prenex form, for example the $\exists^* \forall^*$ class of Bernays and Schönfinkel. Its Skolem form has only constants, so its [Herbrand universe](/herbrand-universe/) is finite.

## References
