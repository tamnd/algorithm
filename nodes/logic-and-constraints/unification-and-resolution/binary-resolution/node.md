---
tag: 5EW8KM
kind: technique
slug: binary-resolution
name: Binary resolution rule
aliases:
- binary resolution
- binary resolution inference
area: logic-and-constraints/unification-and-resolution
level: core
summary: The inference rule that takes two clauses, renames them apart, unifies one literal of each with a complementary one by an mgu, and adds the resolvent. With factoring it is refutation complete.
prereqs: [resolvent, most-general-unifier, standardization-apart]
see_also: [resolvent, factoring, robinson-resolution, robinson-completeness-theorem, lifting-lemma, ordered-resolution, set-of-support, occurs-check]
sources:
  - paper: doi:10.1145/321250.321253
    title: John Alan Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965
    locator: the resolution principle and its completeness; the rule there removes a set of literals from each parent, which is binary resolution of factors
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 5, The resolution principle (binary resolvents, factors, the lifting lemma and the completeness of resolution), with Chapters 6 and 7 for the restricted forms
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 2, Leo Bachmair and Harald Ganzinger, Resolution theorem proving (binary resolution and factoring as inference rules, ordering and selection restrictions)
---

**Binary resolution** is the inference rule that, from two [clauses](/clause/) $C \vee L$ and $D \vee M$ with no common variables, where $L$ and $M$ have opposite signs and a [most general unifier](/most-general-unifier/) $\sigma$ makes their atoms equal, derives the [resolvent](/resolvent/) $(C \vee D)\sigma$. It is sound, and together with [factoring](/factoring/) it is refutation complete by the [Robinson completeness theorem](/robinson-completeness-theorem/), whose first-order step is the [lifting lemma](/lifting-lemma/). This page is about the rule as a technique: how to apply it, and how the strategies of resolution restrict it. [Robinson's resolution](/robinson-resolution/) is the full procedure that applies the rule and factoring until $\square$ appears or nothing new comes.

## In plain words

Two facts that each list some options, such as "it rains or it is cold" and "it does not rain or I stay in", can be combined. If it rains, I stay in; if it does not rain, it is cold. So "it is cold or I stay in" is true either way. The rule drops the one option that the two facts disagree on and keeps all the others.

When the facts talk about all things, as in "every bird flies", the rule first makes the two disputed options match by filling in their variables as little as possible. It never drops two options at once, because that is not safe. Applied over and over, the rule finds a contradiction in any set of facts that cannot all be true, if one more small rule that merges equal options is added.

## When it applies

- **The input is a set of clauses.** The formulas have been put into [clausal normal form](/clausal-normal-form/), so each fact is a disjunction of literals with its variables read universally.
- **The goal is a refutation.** The rule is used to show unsatisfiability, by deriving $\square$. It does not derive every consequence: from $P$ alone it derives nothing, although $P$ implies $P \vee Q$. See [refutation](/refutation/).
- **Unification is decidable for the terms.** The rule needs a most general unifier of two atoms. For ordinary first-order terms it exists whenever a unifier exists, by the [mgu existence theorem](/mgu-existence-theorem/). For terms modulo a theory, such as associativity and commutativity, a single mgu may not exist, and the rule uses a complete set of unifiers instead.
- **Equality is not built in.** The rule treats $=$ as an ordinary predicate. With equality, add the equality axioms or use [paramodulation](/paramodulation/) or [superposition](/superposition/).

## The template

```pseudo id=main
BINARY-RESOLVE(C, D)
L1  D ← a copy of D with variables disjoint from C       ▷ hole: renaming apart
L2  for each L in C and M in D do                         ▷ hole: which literals are eligible
L3      if L and M have opposite signs then
L4          σ ← MGU(atom(L), atom(M))                      ▷ hole: unification algorithm
L5          if σ ≠ FAIL then
L6              R ← ((C \ {L}) ∪ (D \ {M}))σ
L7              output R                                   ▷ hole: keep, simplify or delete R
```

**The holes.**

- *Renaming apart.* The variables of a clause are local to it, so a copy of $D$ with fresh variables means the same clause. Without the copy, $P(x)$ and $\lnot P(f(x))$ have no resolvent, although together they are unsatisfiable. See [standardization apart](/standardization-apart/).
- *Eligible literals.* Unrestricted resolution tries every pair. The strategies of resolution are restrictions here: an order on atoms ([ordered resolution](/ordered-resolution/)), a selected negative literal ([hyperresolution](/hyperresolution/), [SLD resolution](/sld-resolution/)), or a condition on the parents ([unit resolution](/unit-resolution/), [input resolution](/input-resolution/), [set of support](/set-of-support/)).
- *Unification.* Any algorithm that returns an mgu or reports failure, with the [occurs check](/occurs-check/): [Robinson unification](/robinson-unification/), [Martelli-Montanari unification](/martelli-montanari-unification/), or the linear-time [Paterson-Wegman unification](/paterson-wegman-unification/).
- *What to do with $R$.* A prover drops tautologies, drops $R$ if a stored clause [subsumes](/subsumption/) it, simplifies it by unit deletion or [demodulation](/demodulation/), and stops when $R = \square$.

**Why it is sound.** Let a structure satisfy $C$ and $D$, and fix an assignment of the variables of $R$. The instances $C\sigma$ and $D\sigma$ are true under it, and $L\sigma$ and $M\sigma$ are complementary, so one of them is false. The clause that contains the false one has another true literal, and that literal is in $R$. The full proof is on the [resolvent](/resolvent/) page.

**Why it is complete, with factoring.** For ground clauses, the rule alone is refutation complete, because a clause is a set and equal literals merge: this is Lemma 2 of the proof on the [Robinson's resolution](/robinson-resolution/) page. For first-order clauses, every ground resolvent of ground instances of $C$ and $D$ is an instance of a binary resolvent of factors of $C$ and $D$, by the [lifting lemma](/lifting-lemma/). With [Herbrand's theorem](/herbrand-theorem/), this lifts a ground refutation to a first-order one. Factoring cannot be dropped: see the pitfalls.

**Cost of one application.** The loop tries at most $|C| \cdot |D|$ pairs. Each unification is linear in the size of the two atoms with a DAG algorithm. Writing the resolvent out as trees can cost more: the parents

$$Q(x_n) \vee \lnot P(x_1, \ldots, x_n, f(x_0, x_0), \ldots, f(x_{n-1}, x_{n-1})), \qquad P(y_1, \ldots, y_n, y_1, \ldots, y_n)$$

have total size $6n + 4$, and their only resolvent is $Q(t_n)$, where $t_0 = x_0$ and $t_i = f(t_{i-1}, t_{i-1})$, a term with $2^{n+1} - 1$ symbols. Provers that share subterms, as in a [term DAG](/term-dag/), keep this linear.

**Example.** Prove that $a$ has a grandparent from $\mathit{Par}(b, a)$, $\mathit{Par}(c, b)$ and $\mathit{Gp}(x, z) \vee \lnot \mathit{Par}(x, y) \vee \lnot \mathit{Par}(y, z)$. The negated goal is $\lnot \mathit{Gp}(w, a)$.

1. Resolve $\lnot \mathit{Gp}(w, a)$ with the rule on $\mathit{Gp}(x, z)$, with $\sigma = \{x \mapsto w, z \mapsto a\}$: $\lnot \mathit{Par}(w, y) \vee \lnot \mathit{Par}(y, a)$.
2. Resolve with $\mathit{Par}(b, a)$ on the second literal, with $\{y \mapsto b\}$: $\lnot \mathit{Par}(w, b)$.
3. Resolve with $\mathit{Par}(c, b)$, with $\{w \mapsto c\}$: $\square$.

The binding $w \mapsto c$ is the grandparent.

## Classic examples

- [Robinson's resolution](/robinson-resolution/): binary resolution and factoring on all pairs, with deletion of subsumed clauses, as a complete first-order prover.
- [Davis-Putnam elimination](/davis-putnam-elimination/): ground binary resolution on all clauses that contain one variable, after which the variable is gone.
- [SLD resolution](/sld-resolution/): binary resolution between a goal clause and a program clause, on the selected goal literal, as in logic programming.
- [Unit resolution](/unit-resolution/) and [input resolution](/input-resolution/): binary resolution with one parent a unit clause, or an input clause; they refute the same sets, by Chang 1970, and are complete for Horn clauses.
- [Hyperresolution](/hyperresolution/): a chain of binary resolutions of one clause with positive clauses, done as one step.
- [CDCL](/cdcl/): each learned clause is the result of a chain of ground binary resolutions, so the [solver simulates resolution](/cdcl-simulates-resolution/).

## Variations

- **Robinson's form.** Unify a set of literals of $C$ and a set of literals of $D$ at once, and remove them all. This equals binary resolution of [factors](/factoring/) and needs no separate factoring rule.
- **Restricted resolution.** [Ordered resolution](/ordered-resolution/) resolves only on maximal literals; [set of support](/set-of-support/) needs one parent from the support set; [linear resolution](/linear-resolution/) needs one parent to be the last clause. Each keeps refutation completeness under its conditions.
- **Ground resolution.** With no variables, the mgu is empty and the rule is $C \vee A, D \vee \lnot A \vdash C \vee D$. This is the proof system of propositional resolution, in which the [Haken lower bound](/haken-resolution-lower-bound/) holds.
- **Resolution modulo a theory.** Replace syntactic unification by unification modulo the theory, for example [AC unification](/stickel-ac-unification/), and resolve once for each unifier in a complete set.
- **Equality.** [Paramodulation](/paramodulation/) is the equality analogue: it replaces a subterm by an equal term instead of removing a literal.

## Pitfalls

- **Two pairs at once.** From $P \vee Q$ and $\lnot P \vee \lnot Q$, removing both pairs gives $\square$, but $P$ true and $Q$ false satisfies both clauses. Only one pair is removed in each step.
- **No renaming apart.** $\{P(x), \lnot P(f(x))\}$ is unsatisfiable, but $x$ and $f(x)$ do not unify, so the rule without renaming finds nothing.
- **No occurs check.** $\{P(x, x), \lnot P(y, f(y))\}$ is satisfiable: take the natural numbers, $P$ as equality and $f$ as successor. The unifier would need $y = f(y)$, so the atoms do not unify, and the rule must find no resolvent. A unification that skips the [occurs check](/occurs-check/), as Prolog does by default, derives $\square$ here.
- **No factoring.** $\{P(x) \vee P(y), \lnot P(u) \vee \lnot P(v)\}$ is unsatisfiable, but every binary resolvent of two clauses with two literals each, and of their resolvents, has two literals. So $\square$ never appears. The proof is on the [factoring](/factoring/) page.
- **A unifier that is not most general.** Resolving with a less general unifier is sound, but the resolvent is an instance of the right one and can block later steps. The lifting lemma needs the mgu.
- **Exponential terms.** As above, a resolvent written as a tree can be exponentially larger than its parents; store terms as DAGs or bound the term depth.

## Exercises

1. Find all binary resolvents of $P(x) \vee Q(x)$ and $\lnot P(a) \vee \lnot Q(b)$. *Answer:* $Q(a) \vee \lnot Q(b)$ on $P$, and $P(b) \vee \lnot P(a)$ on $Q$.
2. Show that a binary resolvent of two Horn clauses is a Horn clause.
3. Give two ground clauses whose resolvent is longer than both of them. Show that a ground resolvent has fewer literals than its two parents together.
4. Refute $\{P(x) \vee P(y), \lnot P(u) \vee \lnot P(v)\}$ with binary resolution and factoring, and count the steps.
5. Prove that for ground clauses, without factoring, binary resolution derives $\square$ from every unsatisfiable set. Where does the proof use that a clause is a set?

## References
