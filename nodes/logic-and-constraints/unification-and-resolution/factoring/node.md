---
tag: TM79C1
kind: technique
slug: factoring
name: Factoring
aliases:
- factoring rule
- factor of a clause
area: logic-and-constraints/unification-and-resolution
level: core
summary: The unary inference rule that applies a most general unifier of two literals of the same sign in a clause, so they merge into one. Binary resolution needs it to be refutation complete.
prereqs: [most-general-unifier, clause]
see_also: [binary-resolution, resolvent, robinson-resolution, robinson-completeness-theorem, lifting-lemma, subsumption, ordered-resolution, superposition]
sources:
  - paper: doi:10.1145/321250.321253
    title: John Alan Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965
    locator: the resolution principle, which unifies a set of literals in each parent at once and so builds factoring into the rule
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 5, The resolution principle (factors and unit factors of a clause, and resolvents as binary resolvents of factors)
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 2, Leo Bachmair and Harald Ganzinger, Resolution theorem proving (the factoring rule, its restriction to maximal positive literals, and equality factoring)
---

**Factoring** is the inference rule that takes a [clause](/clause/) $C$ with two literals $L$ and $L'$ of the same sign whose atoms unify, applies a [most general unifier](/most-general-unifier/) $\sigma$ of the atoms, and derives the **factor** $C\sigma$, in which $L\sigma$ and $L'\sigma$ have become one literal. Together with [binary resolution](/binary-resolution/) it makes a refutation complete calculus, and without it binary resolution is not complete for first-order clauses. Ground clauses need no factoring, because a clause is a set and equal literals merge by themselves. Robinson's original rule unifies several literals of each parent at once, so it does factoring and resolution in one step.

## In plain words

A clause lists options, at least one of which holds. Sometimes two options say almost the same thing, such as "something is red" and "a ball is red". Choosing to read the first as the second turns the two options into one, and the shorter statement is still a safe consequence.

Resolution removes one option from each of two statements at a time. If both statements carry two options that could be read as the same one, resolution alone keeps leaving two options behind, and it never reaches the empty statement that shows a contradiction. Merging options first fixes this.

## When it applies

- **First-order clauses with variables.** Two literals of the same sign merge after unification. In ground clauses, equal literals are already one element of the set.
- **Literals of the same sign.** Two positive literals or two negative literals. Unifying a positive and a negative literal of one clause makes a tautology, not a factor.
- **Refutation search.** The factor is an instance of $C$, so it is a sound consequence, but it is weaker than $C$ in general. It is added to the clause set, next to $C$.

## The template

```pseudo id=main
FACTORS(C)
L1  for each pair L ≠ L' in C do                         ▷ hole: which pairs are eligible
L2      if L and L' have the same sign then
L3          σ ← MGU(atom(L), atom(L'))
L4          if σ ≠ FAIL then
L5              output Cσ                                ▷ hole: keep, use once, or condense
L6              FACTORS(Cσ)                              ▷ hole: iterate, or factor sets at once
```

**The holes.**

- *Eligible pairs.* Unrestricted factoring tries every pair. [Ordered resolution](/ordered-resolution/) factors only on a maximal positive literal, and calculi with a selected negative literal need no negative factoring at all.
- *What to do with the factor.* Store it as a new clause, or use it only as a parent of the next resolution step, as in Robinson's combined rule.
- *Iterate or factor a set.* A factor in the sense of Chang and Lee applies an mgu of any set of two or more literals of the same sign. Repeated binary factoring gives the same factors up to renaming, by the lemma below.

**Lemma (factoring a set in steps).** Let $A_1, \ldots, A_k$ be unifiable atoms. Let $\sigma_1$ be an mgu of $A_1$ and $A_2$, and for $i \ge 2$ let $\sigma_i$ be an mgu of $A_1 \sigma_1 \cdots \sigma_{i-1}$ and $A_{i+1} \sigma_1 \cdots \sigma_{i-1}$. Then each $\sigma_i$ exists, and $\sigma_1 \cdots \sigma_{k-1}$ is an mgu of $\{A_1, \ldots, A_k\}$.

*Proof.* Write $\tau_i = \sigma_1 \cdots \sigma_i$, with composition read left to right, so that $A\tau_i$ means: apply $\sigma_1$ first. Let $\theta$ be any unifier of all the $A_j$. We show by induction on $i$ that $\sigma_i$ exists, that $\tau_i$ unifies $A_1, \ldots, A_{i+1}$, and that $\theta = \tau_i \theta_i$ for some $\theta_i$. For $i = 1$, $\theta$ unifies $A_1$ and $A_2$, so $\sigma_1$ exists and $\theta = \sigma_1 \theta_1$. For the step, $\theta_{i}$ unifies $A_1 \tau_i$ and $A_{i+2} \tau_i$, since both are mapped to $A_1 \theta = A_{i+2} \theta$. So $\sigma_{i+1}$ exists, and $\theta_i = \sigma_{i+1} \theta_{i+1}$ for some $\theta_{i+1}$, which gives $\theta = \tau_{i+1} \theta_{i+1}$. The atoms $A_1, \ldots, A_{i+1}$ are equal under $\tau_i$, so they stay equal under $\tau_{i+1}$, and $\sigma_{i+1}$ makes $A_{i+2}$ equal to them. So $\tau_{k-1}$ unifies all the $A_j$, and every unifier $\theta$ is an instance of it. $\square$

If the $k$ literals are in $C$, the binary factors in the order of the lemma end in $C\tau_{k-1}$, which is the factor of $C$ on the whole set.

**Theorem (factoring is needed).** The set $S = \{P(x) \vee P(y), \; \lnot P(u) \vee \lnot P(v)\}$ is unsatisfiable, and binary resolution without factoring does not derive $\square$ from it.

*Proof.* $S$ is unsatisfiable: the first clause says that $P$ holds for every element, and the second that $P$ fails for every element, in a nonempty domain. Call a clause *good* if it has exactly two literals, each of the form $P(z)$ or $\lnot P(z)$ for a variable $z$, with different variables. Both clauses of $S$ are good. Let $C = \{L_1, L_2\}$ and $D = \{M_1, M_2\}$ be good and renamed apart, and resolve on $L_2$ and $M_1$, with variables $z_2$ and $w_1$. The mgu is a single binding between $z_2$ and $w_1$. The other variables, $z_1$ of $L_1$ and $w_2$ of $M_2$, are different from $z_2$ and $w_1$ and from each other, so the resolvent is $\{L_1, M_2\}$ with its two variables unchanged, which is good. By induction every derived clause is good, and $\square$ has no literals. $\square$

With factoring, $P(x) \vee P(y)$ has the factor $P(x)$, the other clause has the factor $\lnot P(u)$, and these two resolve to $\square$.

**Why factors are sound.** A factor $C\sigma$ is an instance of $C$, and every instance of a clause is true in every model of the clause, because the variables of a clause are universally quantified.

**Example.** The clause $P(x) \vee P(f(y)) \vee Q(x)$ has one factor: $P(x)$ and $P(f(y))$ unify with $x \mapsto f(y)$, which gives $P(f(y)) \vee Q(f(y))$. The clause $P(x, y) \vee P(y, x) \vee P(a, b)$ has two factors up to renaming: $P(x, x) \vee P(a, b)$ from the first two literals, and $P(a, b) \vee P(b, a)$ from either of the first two with the third. All three literals do not unify, since that would need $a = b$.

## Classic examples

- [Robinson's resolution](/robinson-resolution/): factors of each new clause are added to the clause set, next to the clause.
- [Ordered resolution](/ordered-resolution/): factoring only on maximal positive literals, which keeps refutation completeness and cuts the number of factors.
- [Hyperresolution](/hyperresolution/): factors of positive clauses, before they take part in a hyperresolution step.
- [Superposition](/superposition/): equality factoring, the analogue for positive equations, which is needed for completeness with equality.
- [Input resolution](/input-resolution/) and [unit resolution](/unit-resolution/): defined with factors of input clauses, as in Chang 1970.
- [SLD resolution](/sld-resolution/): a Horn clause has at most one positive literal, and SLD resolution on Horn clauses is complete with no factoring.

## Variations

- **Robinson's combined rule.** Unify a set of literals of $C$ and a set of complementary literals of $D$ in one mgu. This equals binary resolution of a factor of $C$ with a factor of $D$.
- **Positive factoring only.** In calculi with selection or with an ordering, only positive literals need to be merged; a negative literal can be selected, and selection never needs two negative literals to be one.
- **Condensation.** If a factor $C\sigma$ is a proper subset of $C$, as $P(a)$ is of $P(x) \vee P(a)$, then $C\sigma$ is equivalent to $C$: it is an instance of $C$, and as a subset it implies $C$. The prover can replace $C$ by $C\sigma$. This is the only case in which a factor may replace its clause.
- **Equality factoring.** In [superposition](/superposition/), two positive equations $s = t$ and $s' = t'$ with $s\sigma = s'\sigma$ give a clause with the new literal $t \ne t'$, which is needed when the two right sides differ.
- **Unit factors.** A factor with one literal. Unit factors feed [unit resolution](/unit-resolution/).

## Pitfalls

- **Replacing the clause by its factor.** The factor is weaker. The set $\{P(x) \vee P(f(y)) \vee Q(x), \lnot P(f(z)), \lnot P(a), \lnot Q(a)\}$ is unsatisfiable, since the instance with $x = a$ and $y = a$ has all three literals false. With the first clause replaced by its factor $P(f(y)) \vee Q(f(y))$, the set is satisfiable: make $Q$ true on all terms $f(t)$ and $P$ false everywhere. Keep $C$ and add the factor.
- **Deleting the factor by subsumption.** $C$ subsumes $C\sigma$ in the sense $C\sigma' \subseteq C\sigma$ for $\sigma' = \sigma$. A prover that deletes clauses by this test, without a length test, deletes each new factor, and then $\{P(x) \vee P(y), \lnot P(u) \vee \lnot P(v)\}$ saturates without $\square$. The test on the [subsumption](/subsumption/) page adds $|C| \le |D|$.
- **Factoring literals of opposite signs.** Unifying $P(x)$ and $\lnot P(a)$ in one clause makes the tautology $P(a) \vee \lnot P(a) \vee \ldots$, which is useless and is not a factor.
- **Forgetting renaming.** The two literals of a factor are in the same clause and share variables; do not rename one of them apart, or the factor is a different clause. Renaming apart is only for the two parents of a resolvent.

## Exercises

1. List all factors of $P(x) \vee P(y) \vee P(z)$ up to renaming. *Answer:* $P(x) \vee P(z)$ and $P(x)$.
2. Show that a factor of a clause $C$ that is a proper subset of $C$ is logically equivalent to $C$.
3. Prove that the clause set of the theorem above has a refutation with 3 steps: two factors and one resolvent.
4. A clause has $n$ positive literals that pairwise unify. How many factors does unrestricted iterated binary factoring produce, counted with repetition? Why does a prover want factoring of sets in one step instead?
5. Show that for Horn clauses, factoring of negative literals is never needed for [SLD resolution](/sld-resolution/) to reach the empty goal.

## References
