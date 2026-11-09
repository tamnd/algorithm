---
tag: PHN425
kind: technique
slug: demodulation
name: Demodulation
aliases:
- rewriting simplification
- simplification by rewriting
- demodulator
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Rewrite subterms of a clause with unit equations, each used from its larger to its smaller side in a reduction ordering, and delete the old clause. It terminates and keeps the clause set equivalent.
prereqs: [paramodulation, rewrite-rule, well-founded-reduction-ordering]
see_also: [paramodulation, superposition, knuth-bendix-completion, unfailing-completion, knuth-bendix-ordering, normal-form, congruence-closure, subsumption]
sources:
  - paper: "Lawrence Wos, George A. Robinson, Daniel F. Carson and Leon Shalla, The concept of demodulation in theorem proving, Journal of the ACM 14(4), 1967"
    locator: the definition of demodulators, unit equalities used to rewrite clauses into a canonical form, and their use to cut down the number of retained clauses
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 7, Robert Nieuwenhuis and Albert Rubio, Paramodulation-based theorem proving (simplification by rewriting, redundancy, and the ordering conditions that keep completeness)
  - paper: "William McCune, Otter 3.0 Reference Manual and Guide, Technical Report ANL-94/6, Argonne National Laboratory, 1994"
    locator: demodulation of new clauses, back demodulation of stored clauses, and the orientation of demodulators by term ordering
---

**Demodulation** is the simplification rule that rewrites a subterm $l\theta$ of a [clause](/clause/) to $r\theta$, using a unit equation $l = r$ (a **demodulator**) and a matching substitution $\theta$, and then replaces the clause by the rewritten one. Each step must make the term smaller in a [reduction ordering](/well-founded-reduction-ordering/) $\succ$, that is $l\theta \succ r\theta$, so rewriting always stops, at a [normal form](/normal-form/). Demodulation is to [paramodulation](/paramodulation/) what deletion is to inference: paramodulation adds a new clause and keeps the old one, while demodulation uses only matching, not unification, and removes the old clause. In [superposition](/superposition/) provers, demodulation with an extra guard is the main simplification, and it keeps the calculus complete.

## In plain words

If a prover knows that "zero plus anything is that thing", then every clause that mentions "zero plus five" can say "five" instead. The new clause is shorter and says the same thing, given the rule. So the prover rewrites it and throws the long version away.

The rule must always be used in the direction that makes things simpler, measured by a fixed ordering of terms. Then rewriting cannot go on forever, and every clause is cut down to a simplest form. Most clauses that a prover derives become much shorter this way, or turn into copies of clauses it already has, which it can then drop.

## When it applies

- **Unit equations are present.** The demodulators are positive unit clauses $l = r$, in the input or derived. Conditional equations, clauses with more literals, are not used for rewriting.
- **A reduction ordering is fixed.** A well-founded order $\succ$ on terms, closed under contexts and substitutions, such as the [Knuth-Bendix ordering](/knuth-bendix-ordering/) or a path ordering. An equation is used only in a direction that decreases it.
- **The goal is a smaller clause set, not new consequences.** Demodulation does not derive new facts; it replaces clauses by simpler equivalent ones. New consequences come from [paramodulation](/paramodulation/) or [superposition](/superposition/).

## The template

```pseudo id=main
DEMODULATE(C, U, ≻)
L1  repeat
L2      find L in C, a position p, l = r in U and θ with L|p = lθ    ▷ hole: indexing and choice of position
L3      if lθ ≻ rθ and REDUNDANT-GUARD(L, p, l = r, θ) then             ▷ hole: the ordering and the guard
L4          C ← C with L|p replaced by rθ
L5  until no step applies
L6  return C                                                          ▷ hole: then tautology and subsumption tests
```

**The holes.**

- *Finding redexes.* Either side of a unit may play the role of $l$, and $\theta$ binds only variables of the unit. A prover finds candidates for $l\theta$ with [term indexing](/term-indexing/), and visits positions in a fixed order, for example leftmost-outermost. The result can depend on this order (see the pitfalls).
- *The ordering.* With a total ground order, such as KBO with a total precedence, every ground instance of an equation can be oriented, and an unorientable equation such as $x + y = y + x$ is still used on the instances where $l\theta \succ r\theta$.
- *The guard.* In a prover that only wants an equivalent clause set, the guard is true. In a superposition prover, the old clause must be redundant: it must follow from the unit and the new clause, which are both smaller than it. This is the condition $L \succ (l = r)\theta$ in the literal ordering, explained below.
- *After rewriting.* The rewritten clause may be a tautology, such as $t = t$, or subsumed by a stored clause, and is then deleted. Stored clauses that a new unit can rewrite are taken out and simplified again (**back demodulation**).

**Correctness.** Let $C'$ be $C$ with $L|_p = l\theta$ replaced by $r\theta$.

- *The set stays equivalent.* In every model of $l = r$, the terms $l\theta$ and $r\theta$ have the same value under every assignment, so by induction on the context, $L$ and the rewritten literal have the same truth value. Hence $\{l = r, C\} \models C'$ and $\{l = r, C'\} \models C$. Replacing $C$ by $C'$ while the unit is kept changes no model.
- *It terminates.* A reduction ordering is closed under contexts, so $l\theta \succ r\theta$ gives $t[l\theta]_p \succ t[r\theta]_p$ for every term $t$. Each step therefore replaces one side of one literal by a smaller term and leaves the others unchanged, so the multiset of all sides of $C$ decreases in the multiset extension of $\succ$, which is well-founded. So there is no infinite chain of steps.
- *The guard in superposition.* Compare literals as multisets of sides, with $s = t$ as $\{s, t\}$ and $s \ne t$ as $\{s, s, t, t\}$. If $l\theta$ is a proper subterm of a side $s$, then $s \succ l\theta \succ r\theta$ by the subterm property of the ordering, so $L \succ (l = r)\theta$. If $L$ is $s \ne t$ with $s = l\theta$, then $\{s, s, t, t\} \succ \{s, r\theta\}$ because $s \succ r\theta$. If $L$ is $s = t$ with $s = l\theta$, then $\{s, t\} \succ \{s, r\theta\}$ holds if and only if $t \succ r\theta$. So the guard only forbids rewriting the whole larger side of a positive equation by a unit that is as large as that equation.

**Example.** With $0 + y = y$ and $s(x) + y = s(x + y)$, oriented from left to right by KBO with precedence $+ \succ s \succ 0$:

$$s(s(0)) + s(0) \;\to\; s(s(0) + s(0)) \;\to\; s(s(0 + s(0))) \;\to\; s(s(s(0))).$$

Three steps reach the normal form, and every clause that contained the left term now contains $s(s(s(0)))$ instead. The implementation on the [superposition](/superposition/) page follows this template in its functions `demodulate` and `demodulate_clause`, with KBO as the ordering and the guard above.

## Classic examples

- [Superposition](/superposition/): demodulation with the guard above runs on every new clause before it is stored, and it is a case of redundancy, so the calculus stays complete.
- [Knuth-Bendix completion](/knuth-bendix-completion/): the simplification of the sides of rules and equations by the other rules is demodulation in a setting with only unit equations.
- [Unfailing completion](/unfailing-completion/): ordered rewriting, in which an unorientable equation is used only on instances that decrease, is demodulation with a total ground ordering.
- [Paramodulation](/paramodulation/) provers since the late 1960s: resolution and paramodulation provers in the line of Otter run demodulation on each new clause and back demodulation on stored clauses.
- [Congruence closure](/congruence-closure/): for ground unit equations, the same normal forms can be computed in near-linear time by a union-find structure, with no ordering on terms needed.

## Variations

- **Unconditional versus guarded.** A plain resolution prover may rewrite with any oriented unit. A superposition prover adds the redundancy guard, which matters only at the top of the larger side of a positive equation.
- **Ordered rewriting.** Use equations that cannot be oriented, such as commutativity, on the instances that decrease: $b + a \to a + b$ when $b \succ a$ in the precedence, and $a + b$ stays. The order of arguments then works as a normal form for sums.
- **Contextual rewriting and conditional demodulation.** Use a non-unit clause $l = r \vee D$ to rewrite a clause that already contains the complement of $D$. This is stronger and needs its own redundancy argument.
- **Unit deletion modulo equations.** If both sides of a literal $s \ne t$ rewrite to the same term, the literal is false in every model of the units, so delete it from its clause.

## Pitfalls

- **Rewriting a unit with itself.** Without the guard, $f(x) = a$ rewrites itself to $a = a$, which is a tautology and is deleted, and the unit is lost. On $\{f(x) = a, f(b) \ne a\}$ the prover is then left with $\{f(b) \ne a\}$, which is satisfiable, and it answers SATURATED on an unsatisfiable set. The guard forbids this step, since $(f(x) = a)$ is not larger than itself, while it allows rewriting $f(b) \ne a$ to $a \ne a$, which equality resolution turns into $\square$.
- **No ordering.** An equation used in both directions, such as $f(x) = f(f(x))$ read from left to right, gives an infinite rewrite chain. Always check $l\theta \succ r\theta$ for the instance used.
- **Normal forms are not unique.** With the units $f(a) = b$ and $f(a) = c$, both oriented away from $f(a)$, the term $f(a)$ rewrites to $b$ or to $c$, depending on which unit is tried first. Demodulation alone is not confluent; a superposition step between the two units derives $b = c$, after which the normal forms agree. See [Knuth-Bendix completion](/knuth-bendix-completion/).
- **Using unification instead of matching.** Demodulation must not instantiate the clause being rewritten. If $f(a) = b$ "rewrote" $P(f(y))$ to $P(b)$ by binding $y \mapsto a$, the result would only be about an instance, and deleting $P(f(y))$ would lose information. Only the variables of the demodulator are bound.
- **Rewriting is not all of equational reasoning.** Demodulation keeps the clause set equivalent but cannot by itself find all consequences: from $f(a) = b$ and $P(f(x))$ it derives nothing, while paramodulation derives $P(b)$. A prover needs both.

## Exercises

1. Prove that $\{l = r, C\} \models C'$ and $\{l = r, C'\} \models C$, where $C'$ is $C$ with one occurrence of $l\theta$ replaced by $r\theta$.
2. Rewrite $s(0) + (0 + s(s(0)))$ to normal form with the two Peano units of the example, and count the steps.
3. Give a unit equation $l = r$ and a term ordering that is total on ground terms such that $l$ and $r$ are not comparable, but some instances are. Which instances can be used for rewriting?
4. Show that the guard condition $L \succ (l = r)\theta$ fails exactly when $L$ is a positive equation $l\theta = t$ and $t \succ r\theta$ does not hold.
5. With the units $f(a) = b$, $f(a) = c$ and $g(b) = d$, find a term whose normal form depends on the order in which units are tried. Which superposition steps make the normal forms unique?

## References
