---
tag: Z5BN7W
kind: technique
slug: set-of-support
name: Set-of-support strategy
aliases:
- set-of-support
- set of support
- SOS strategy
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Resolution in which every step needs a parent from a chosen support set or derived from it. It is complete when the clauses outside the support are satisfiable (Wos, Robinson and Carson 1965).
prereqs: [robinson-resolution, binary-resolution]
see_also: [robinson-resolution, binary-resolution, linear-resolution, hyperresolution, robinson-completeness-theorem, lifting-lemma, subsumption, first-order-theorem-proving]
sources:
  - paper: "Lawrence Wos, George A. Robinson and Daniel F. Carson, Efficiency and completeness of the set of support strategy in theorem proving, Journal of the ACM 12(4), 536 to 541, 1965"
    locator: the definition of the set of support strategy and the theorem that it is complete when the complement of the support set is satisfiable
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 6, Semantic resolution and lock resolution (set-of-support as a special case of semantic resolution, with its completeness)
  - paper: "William McCune, Otter 3.0 Reference Manual and Guide, Technical Report ANL-94/6, Argonne National Laboratory, 1994"
    locator: the main loop with the lists usable and sos, in which the given clause is taken from sos and resolved with the clauses in usable
---

The **set-of-support strategy** restricts [binary resolution](/binary-resolution/) to steps in which at least one parent is in a chosen subset $T$ of the input clauses, the **set of support**, or has been derived from it. The usual choice of $T$ is the clauses of the negated goal, so the prover never combines axioms with each other and works backward from the goal. Wos, Robinson and Carson proved in 1965 that the strategy is refutation complete whenever the input clauses outside $T$ are satisfiable, which is the case when the axioms are consistent. It is a restriction of [Robinson's resolution](/robinson-resolution/), and it is the "sos" list of the given-clause loop of provers such as Otter.

## In plain words

A theorem prover has some background facts and one question. Most of what it could derive from the background facts alone is true but useless, and there is a lot of it. The strategy tells the prover: every step must use the question, or something that came from the question.

This is safe as long as the background facts do not contradict each other. Then any contradiction must involve the question, and the prover can always find one that starts from it. If the background facts already contradict each other, the strategy can miss the contradiction, because it is forbidden to look at the background facts alone.

## When it applies

- **A refutation search with a natural split.** The input is $N \cup T$, where $N$ is known to be satisfiable: consistent axioms, a theory with a known model, or a background that has been checked before.
- **The goal is the interesting part.** Steps between two clauses of $N$ derive consequences of the axioms that need not relate to the goal. The strategy cuts all of them.
- **A model of $N$ is available or guaranteed by the shape of $N$.** If every clause of $N$ has a positive literal, the interpretation with every atom true is a model, so $T$ can be the set of all-negative clauses. Dually, $T$ can be the set of all-positive clauses.

## The template

```pseudo id=main
SOS-SATURATE(N, T)
L1  usable ← N together with its factors                 ▷ hole: the split into N and T
L2  sos ← T
L3  while sos ≠ ∅ do
L4      G ← remove a clause from sos                      ▷ hole: fair choice, by age and weight
L5      if G = □ then return UNSAT
L6      usable ← usable ∪ {G}
L7      for each factor of G and each resolvent of G with a clause of usable, as R do
L8          if R is not redundant then sos ← sos ∪ {R}     ▷ hole: tautology and subsumption deletion
L9  return SATURATED
```

**The holes.**

- *The split.* Choose $T$ so that $N = S \setminus T$ is satisfiable: the negated goal, the all-negative clauses, or the all-positive clauses. If $N$ may be unsatisfiable, the answer SATURATED proves nothing.
- *Fair choice.* Every clause put into sos must be picked at some time, for example by taking the oldest clause every few picks. Otherwise a refutation may exist and never be found.
- *Redundancy.* Tautologies may be dropped, and clauses subsumed by stored clauses may be deleted; the [subsumption](/subsumption/) page shows that this keeps the strategy complete.

Clauses of $N$ meet each other only through a clause of sos, so line L7 never forms a resolvent of two clauses of $N$.

**Theorem (Wos, Robinson and Carson 1965).** Let $S$ be a finite unsatisfiable set of clauses and $T \subseteq S$ such that $N = S \setminus T$ is satisfiable. Then $S$ has a refutation by binary resolution and factoring in which every resolution step has a parent that is in $T$ or derived, and factors of clauses of $N$ count as clauses of $N$.

*Ground lemma.* Let $G$ be a finite unsatisfiable set of ground clauses and $I$ any truth assignment. Then $G$ has a ground resolution refutation in which every step has a parent that is false in $I$.

*Proof of the lemma.* Induction on the number $n$ of atoms in $G$. If $n = 0$, then $\square \in G$. Let $n \ge 1$, choose an atom $A$, and let $L$ be the literal of $A$ that is false in $I$. Let

$$G_1 = \{ C \setminus \{L\} : C \in G, \; \bar L \notin C \}, \qquad G_2 = \{ C \setminus \{\bar L\} : C \in G, \; L \notin C \}.$$

These are $G$ with $L$ set false and with $L$ set true. Both are unsatisfiable, since a model of either, with $L$ set accordingly, would satisfy $G$, and neither contains $A$. By induction, $G_1$ and $G_2$ have refutations of the required kind.

Replay the refutation of $G_1$ with each input $C \setminus \{L\}$ replaced by $C$. No step resolves on $A$, so each replayed clause is the old clause $E$ or $E \cup \{L\}$. Since $L$ is false in $I$, a clause that was false in $I$ is still false in $I$, so every step still has a parent false in $I$. The replay ends in $\square$, and we are done, or in $\{L\}$.

In the second case, derive each input $C \setminus \{\bar L\}$ of $G_2$ with $\bar L \in C$ by resolving $\{L\}$ with $C$; the parent $\{L\}$ is false in $I$. Then run the refutation of $G_2$ unchanged. Every step in the whole derivation has a parent false in $I$, and it ends in $\square$. $\square$

*Proof of the theorem.* By [Herbrand's theorem](/herbrand-theorem/), a finite set $G$ of ground instances of clauses of $S$ is unsatisfiable. Call a clause of $G$ an $N$-instance if it is an instance of a clause of $N$, and a $T$-instance otherwise. Let $M$ be a model of $N$, and let $I$ give each ground atom its truth value in $M$. Every $N$-instance is true in $M$, so true in $I$. By the ground lemma, $G$ has a refutation in which every step has a parent false in $I$; that parent is not an $N$-instance, so it is a $T$-instance or a derived clause. Now lift the refutation by the [lifting lemma](/lifting-lemma/): each ground clause $E$ becomes a clause $D$ with $E = D\lambda$, where $T$-instances lift to clauses of $T$, $N$-instances to clauses of $N$, and derived clauses to derived clauses. A lifted resolution step uses factors of the lifted parents, and a factor of a clause of $T$ or of a derived clause is derived. So each lifted step has a parent in $T$ or derived, and the lifted derivation ends in $\square$. $\blacksquare$

**Example.** Let $N = \{P(a), \lnot P(x) \vee P(f(x))\}$ and let $T$ be the negated goal $\{\lnot P(f(f(f(a))))\}$. The loop derives $\lnot P(f(f(a)))$, $\lnot P(f(a))$, $\lnot P(a)$ and $\square$, four clauses in all. Unrestricted resolution may also resolve the two axioms with each other and derive $P(f(a))$, $\lnot P(x) \vee P(f(f(x)))$, and so on, none of which the strategy ever forms.

## Classic examples

- [Robinson's resolution](/robinson-resolution/) with the split into usable and sos: Otter's given-clause loop is this template, and later provers keep the two lists.
- [Linear resolution](/linear-resolution/): a linear refutation whose top clause is in $T$ is also a set-of-support refutation. When $N$ is satisfiable such a top clause exists: a minimal unsatisfiable subset of $S$ contains some $C \in T$, and without $C$ it is satisfiable, which is the condition of the completeness theorem on that page.
- [SLD resolution](/sld-resolution/): the goal clause is the support, every step uses the current goal, and the program clauses, which have a model, never meet each other.
- [Hyperresolution](/hyperresolution/) and other semantic resolution: the support is the set of clauses false in a fixed interpretation, which is the semantic form of the ground lemma above.
- [First-order theorem proving](/first-order-theorem-proving/) in practice: the negated conjecture is the default support set in many provers.

## Variations

- **Semantic resolution.** Fix an interpretation $I$ and require one parent to be false in $I$. With $I$ a model of $N$ this contains the set-of-support strategy; the ground lemma above is its completeness proof.
- **Input and unit preference.** Combine the strategy with unit preference, which picks short clauses from sos first, or with weight-based choice. These change the order of search, not the set of derivable clauses.
- **Support for paramodulation.** In equational provers, the same restriction is applied to paramodulation steps. The completeness proof above does not cover the ordering restrictions of superposition, so provers use this combination as a heuristic.
- **Two-sided support.** Put the negated goal and some hypotheses of the conjecture into $T$, which keeps $N$ satisfiable and allows forward reasoning from the hypotheses.

## Pitfalls

- **The complement is unsatisfiable.** $S = \{P, \lnot P, Q\}$ with $T = \{Q\}$: $Q$ resolves with nothing, the loop saturates, and $S$ is unsatisfiable through $P$ and $\lnot P$, which the strategy may not combine. The condition on $N$ is needed.
- **Inconsistent axioms.** If the axioms are inconsistent, the strategy may answer SATURATED, while every goal follows from them. A run that saturates proves that $S$ is satisfiable only when $N$ is known to be satisfiable.
- **Forgetting the factors of $N$.** Resolution steps may use factors of clauses of $N$ as the second parent. The template adds them to usable at the start.
- **Unfair choice.** A loop that always picks the lightest clause can starve an old heavy clause that the refutation needs. Mix age and weight.
- **Ordering restrictions.** The theorem is for unrestricted binary resolution inside the support condition. It says nothing about the support condition together with [ordered resolution](/ordered-resolution/) or [superposition](/superposition/): the ground lemma picks the atom to resolve on by the interpretation, not by the order, so its refutations need not obey the order.

## Exercises

1. Show that if every clause of $N$ contains a positive literal, then $N$ is satisfiable, so the all-negative clauses form a valid support set.
2. Find all set-of-support refutations of $\{P \vee Q, \lnot P \vee Q, P \vee \lnot Q, \lnot P \vee \lnot Q\}$ with $T = \{\lnot P \vee \lnot Q\}$, up to the order of steps.
3. Prove that if $N$ is satisfiable and $T = \emptyset$, the strategy derives nothing, and explain why this is consistent with the theorem.
4. In the ground lemma, why must $L$ be the literal that is false in $I$, and not the one that is true?
5. Give an unsatisfiable set $S$ and a set $T$ with $S \setminus T$ unsatisfiable for which the strategy still finds a refutation. Why does this not contradict the pitfall above?

## References
