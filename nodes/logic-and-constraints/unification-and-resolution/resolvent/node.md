---
tag: E96AMX
kind: definition
slug: resolvent
name: Resolvent
aliases:
- binary resolvent
area: logic-and-constraints/unification-and-resolution
level: intro
summary: The clause made from two clauses by deleting a complementary pair of literals, after applying a most general unifier of their atoms, and joining what is left. It follows from its two parents.
prereqs: [clause, literal, most-general-unifier]
see_also: [binary-resolution, factoring, refutation, robinson-resolution, standardization-apart, davis-putnam-elimination, hyperresolution, paramodulation]
sources:
  - paper: doi:10.1145/321250.321253
    title: John Alan Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965
    locator: the definition of resolvents, in which a set of literals of each clause is unified and removed
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 5, The resolution principle (binary resolvents, factors, and resolvents of clauses as binary resolvents of their factors)
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 2, Leo Bachmair and Harald Ganzinger, Resolution theorem proving (the binary resolution and factoring rules)
---

A **resolvent** of two [clauses](/clause/) is the clause made by deleting one literal $L$ from the first and one literal of opposite sign from the second, after a [most general unifier](/most-general-unifier/) has made the two atoms equal, and joining the rest. For ground clauses it is the familiar rule: from $C \vee A$ and $D \vee \lnot A$ get $C \vee D$. The resolvent is a consequence of its two parents, and it is the single step from which [refutations](/refutation/) are built. This page defines the clause; [binary resolution](/binary-resolution/) is the inference rule that produces it, and [Robinson's resolution](/robinson-resolution/) is the procedure that uses it with [factoring](/factoring/).

## Definition

A literal is an atom $A$ or its negation $\lnot A$. The complement $\bar L$ of $L$ is $\lnot A$ if $L = A$, and $A$ if $L = \lnot A$. A clause is a finite set of literals, read as their disjunction with its variables universally quantified. Unions of clauses are unions of sets, so equal literals merge.

**Ground resolvent.** Let $C$ and $D$ be ground clauses with $L \in C$ and $\bar L \in D$. The resolvent of $C$ and $D$ on $L$ is

$$\mathrm{res}_L(C, D) = (C \setminus \{L\}) \cup (D \setminus \{\bar L\}).$$

**Binary resolvent.** Let $C$ and $D$ be clauses with no variable in common; rename one of them first if needed ([standardization apart](/standardization-apart/)). Let $L \in C$ and $M \in D$ be literals of opposite sign whose atoms $A$ and $B$ are unifiable, and let $\sigma$ be a most general unifier of $A$ and $B$. The binary resolvent of $C$ and $D$ on $L$ and $M$ is

$$((C \setminus \{L\}) \cup (D \setminus \{M\}))\sigma.$$

The literals $L$ and $M$ are the **literals resolved upon**, and $C$ and $D$ are the **parents**. Two most general unifiers differ by a renaming, so the resolvent is unique up to a renaming of variables.

**Resolvent in the sense of Robinson.** A **factor** of $C$ is $C\tau$, where $\tau$ is a most general unifier of two or more literals of $C$ with the same sign. A resolvent of $C$ and $D$ is a binary resolvent of $C$ or a factor of $C$ with $D$ or a factor of $D$. Robinson's 1965 paper defines it in one step: unify a set of literals of $C$ with the complements of a set of literals of $D$, and remove them all. Both definitions give the same clauses up to renaming.

**Soundness.** Every binary resolvent $R$ of $C$ and $D$ is true in every model of $C$ and $D$.

*Proof.* Let $M$ be a model of $C$ and $D$, and $\beta$ an assignment of the variables of $R$. Every instance of a true clause is true, so $C\sigma$ and $D\sigma$ are true under $\beta$. The atoms $A\sigma$ and $B\sigma$ are equal, so $L\sigma$ and $M\sigma$ are complementary, and exactly one of them is true. If $L\sigma$ is false, some other literal of $C\sigma$ is true, and it is in $R$. If $M\sigma$ is false, the same holds for $D\sigma$. So $R$ is true under $\beta$. $\square$

A factor is an instance of its clause, so it is sound too.

## Examples and non-examples

**Ground.** $P \vee Q$ and $\lnot Q \vee R$ have the resolvent $P \vee R$ on $Q$. $P \vee Q$ and $\lnot Q \vee P$ have the resolvent $P$: the two copies of $P$ merge, since a clause is a set.

**With a unifier.** $P(x) \vee Q(f(x))$ and $\lnot Q(y) \vee R(y)$ have no common variable. The atoms $Q(f(x))$ and $Q(y)$ have the most general unifier $y \mapsto f(x)$, and the resolvent is $P(x) \vee R(f(x))$.

**Two unifier bindings.** $P(x, a) \vee Q(x)$ and $\lnot P(b, y) \vee R(y)$ resolve with $\sigma = \{x \mapsto b, y \mapsto a\}$, which gives $Q(b) \vee R(a)$.

**Renaming is needed.** $P(x)$ and $\lnot P(f(x))$ seem to have no resolvent, since $x$ and $f(x)$ do not unify. But the clauses are $\forall x P(x)$ and $\forall x \lnot P(f(x))$, two separate quantifiers. After renaming the second to $\lnot P(f(x'))$, the unifier $x \mapsto f(x')$ gives the resolvent $\square$.

**Two pairs, two resolvents.** $P \vee Q$ and $\lnot P \vee \lnot Q$ have two resolvents, $Q \vee \lnot Q$ on $P$ and $P \vee \lnot P$ on $Q$. Both are tautologies. Removing both pairs at once to get $\square$ is not a resolvent, and it would be unsound: $P$ true and $Q$ false satisfies both parents.

**No resolvent.** $P(x)$ and $P(a)$ have the same sign. $P(a)$ and $\lnot P(b)$ have atoms that do not unify. $P(x)$ and $\lnot Q(x)$ have different predicates.

**A consequence that is not a resolvent.** From $P(x) \vee Q(x)$ and $\lnot P(y)$, the unifier $\{x \mapsto a, y \mapsto a\}$ gives $Q(a)$, which follows from the parents. It is not a binary resolvent, because that unifier is not most general. The resolvent is $Q(x)$, and $Q(a)$ is its instance.

**Merging needs factors.** The binary resolvents of $P(x) \vee P(y)$ and $\lnot P(u) \vee \lnot P(v)$ are all of the form $P(x) \vee \lnot P(v)$, with two literals. The factor $P(x)$ of the first clause and the factor $\lnot P(u)$ of the second have the resolvent $\square$. See [factoring](/factoring/).

## Related definitions

- [Binary resolution](/binary-resolution/): the rule that adds a resolvent to a clause set, with its strategies.
- [Factoring](/factoring/): the unary rule that merges unifiable literals; together with resolvents it gives a refutation complete system.
- [Refutation](/refutation/): a derivation of $\square$ by resolvents and factors.
- [Hyperresolution](/hyperresolution/): a hyperresolvent is the result of a chain of binary resolvents with positive clauses, taken as one step.
- [Paramodulation](/paramodulation/): the analogue of a resolvent for equality, which replaces a term by an equal one.
- [Davis-Putnam elimination](/davis-putnam-elimination/): replaces all clauses on a propositional variable by all their resolvents on it.
- [Unit clause](/unit-clause/): a resolvent with a unit parent is shorter than the other parent, as in [unit resolution](/unit-resolution/).

## References
