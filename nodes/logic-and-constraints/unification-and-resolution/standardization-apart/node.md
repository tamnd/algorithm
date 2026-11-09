---
tag: BRDJWG
kind: concept
slug: standardization-apart
name: Standardization apart
aliases:
- variable renaming apart
area: logic-and-constraints/unification-and-resolution
level: intro
summary: Renaming variables so that distinct clauses share no variables before unification.
prereqs: [substitution, clause, unifier]
see_also: [binary-resolution, sld-resolution, most-general-unifier, lifting-lemma, factoring, knuth-bendix-completion, warren-abstract-machine, term-indexing]
sources:
  - paper: doi:10.1145/321250.321253
    title: J. A. Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965, pages 23 to 41
    locator: the definition of resolvents, which is stated for clauses whose variables have been renamed apart
  - book: isbn:9783540181997
    title: John W. Lloyd, Foundations of Logic Programming, second edition, Springer, 1987
    locator: Chapter 2, the definition of SLD-derivation (each step uses a variant of a program clause with variables that have not appeared before)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 6, the definition of critical pairs (the two rules are renamed so that they have no common variables)
---

**Standardization apart** is the renaming of the variables of two clauses, or of two rules, so that they share no variable before they are unified. A variable of a clause is universally quantified in that clause only, so the $x$ of one clause and the $x$ of another clause are unrelated. If both keep the name $x$, a [unifier](/unifier/) must give them the same value, and unification can fail where the logic allows a step. Resolution, [SLD resolution](/sld-resolution/) and critical pair computation all rename apart before each step. The renaming is sound, because a clause and its variant are logically equivalent.

## In plain words

Each clause is a separate rule, and its letters are its own private placeholders. Two rules can use the same letter for unrelated things, just as two recipes can both say "the first ingredient" for different foods.

Before a prover combines two rules, it gives the placeholders of one rule new names that the other rule does not use. Otherwise the prover would think that the two rules talk about the same unknown thing, and it would try to give one value to both. That can make a valid step look impossible, so the prover would miss proofs. The same holds when a program uses one rule several times in a row: each use gets fresh names. Renaming never changes what a rule means, so it is always safe.

## The idea

Notation, as in the rest of this area: $\sigma, \theta$ are substitutions, $t\sigma$ is the application of $\sigma$ to $t$, and a renaming $\rho$ is a substitution that maps the variables one to one onto variables.

**Definition.** Two clauses $C$ and $D$ are **standardized apart** when $\mathrm{Var}(C) \cap \mathrm{Var}(D) = \emptyset$. To standardize $D$ apart from $C$, choose a renaming $\rho$ such that $\mathrm{Var}(D\rho) \cap \mathrm{Var}(C) = \emptyset$, and use the variant $D\rho$ in place of $D$.

**Soundness.** A clause stands for the universal closure of its disjunction, $\forall x_1 \cdots \forall x_k\, (L_1 \lor \cdots \lor L_r)$. Renaming bound variables does not change a formula, so $D$ and $D\rho$ have the same models.

**Why it is needed.** Resolution of $C = \{L\} \cup C'$ and $D = \{\neg L'\} \cup D'$ uses a single substitution $\sigma$ with $L\sigma = L'\sigma$. With shared variables, $\sigma$ must treat a variable of $C$ and the variable with the same name in $D$ alike. This adds a constraint that the logic does not have. After renaming, a unifier of $L$ and $L'\rho$ can choose the values for the two clauses independently, which is exactly what the [lifting lemma](/lifting-lemma/) needs. The lemma lifts a ground step between instances $C\theta_1$ and $D\theta_2$ with independent $\theta_1$ and $\theta_2$. When $C$ and $D$ share no variables, $\theta_1$ and $\theta_2$ combine into one substitution $\theta$ that acts as $\theta_1$ on $C$ and as $\theta_2$ on $D$.

**Each use needs fresh names.** A derivation can use one clause many times. Each use must get its own variant, with variables that are new to the whole derivation so far. A clause resolved with itself must also be renamed, so the two copies are independent. [Factoring](/factoring/) works inside one clause, so it does not rename.

**Implementation.** A prover can copy the clause with fresh variable names from a counter. Some provers number the variables of each stored clause from zero and keep two separate banks of variables during one unification, or add an offset to the numbers of one clause, so that no copy is made. The [Warren abstract machine](/warren-abstract-machine/) renames as a side effect of a call: it allocates new variable cells for each activation of a clause.

## Examples

**Resolution fails without renaming.** Take

$$C_1 = \{P(x)\}, \qquad C_2 = \{\neg P(f(x))\}.$$

The set is unsatisfiable: $C_1$ says that $P$ holds everywhere, and $C_2$ says that $P(f(x))$ fails for each $x$. With the shared name, resolution needs a unifier of $P(x)$ and $P(f(x))$, and the [occurs check](/occurs-check/) rejects $x \doteq f(x)$. So no resolvent exists, and the prover finds no refutation.

After renaming $C_2$ to $\{\neg P(f(x'))\}$, the mgu of $P(x)$ and $P(f(x'))$ is $\{x \mapsto f(x')\}$, and the resolvent is the empty clause. The refutation exists.

**SLD resolution uses a clause twice.** Take the program

```
nat(0).
nat(s(X)) :- nat(X).
```

and the query `?- nat(s(s(0))).` The first step uses the variant `nat(s(X1)) :- nat(X1)` and binds `X1 = s(0)`, which leaves the goal `nat(s(0))`. The second step uses a fresh variant `nat(s(X2)) :- nat(X2)` and binds `X2 = 0`, which leaves `nat(0)`, solved by the fact. Without fresh names, the second step would need `X = s(0)` and `X = 0` at once, and the query would fail although it is true.

**A shared variable that does not matter.** Resolving $\{P(x), Q(x)\}$ with $\{\neg P(a)\}$ works without renaming, since the second clause has no variables. Renaming apart is still the safe default, because a prover cannot know in advance which shared names will matter.

**Critical pairs.** In [Knuth-Bendix completion](/knuth-bendix-completion/), the rule $f(f(x)) \to g(x)$ overlaps with itself. A renamed copy $f(f(y)) \to g(y)$ unifies its left side with the subterm $f(x)$ of the original, by $\{x \mapsto f(y)\}$, and gives the critical pair $\langle g(f(y)),\ f(g(y)) \rangle$. Without renaming, $f(f(x))$ and $f(x)$ would not unify, and the overlap would be missed.

## Where it is used

- [Binary resolution](/binary-resolution/), [paramodulation](/paramodulation/) and [superposition](/superposition/) rename the two premises apart before each inference.
- [SLD resolution](/sld-resolution/) and Prolog use a fresh variant of a program clause at each step.
- Critical pairs in [Knuth-Bendix completion](/knuth-bendix-completion/) and in confluence checks rename the two rules apart.
- [Term indexing](/term-indexing/) stores terms with normalized variable names. A query for unifiable terms must treat the variables of the query and of the stored terms as distinct, which is standardization apart done inside the index.

## References
