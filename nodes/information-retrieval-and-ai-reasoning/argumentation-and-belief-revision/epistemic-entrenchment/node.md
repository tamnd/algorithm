---
tag: K4FQGQ
kind: definition
slug: epistemic-entrenchment
name: Epistemic entrenchment
aliases:
- Gardenfors-Makinson entrenchment
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: An ordering of beliefs by how firmly they are held, from which an AGM contraction gives up the least entrenched beliefs first.
prereqs: [agm-postulates, partial-meet-contraction]
see_also: [agm-representation-theorem, levi-identity, grove-spheres, ordinal-conditional-functions, katsuno-mendelzon-revision, belief-revision]
sources:
  - paper: "Peter Gärdenfors and David Makinson, Revisions of knowledge systems using epistemic entrenchment, in Moshe Y. Vardi (ed.), Proceedings of the Second Conference on Theoretical Aspects of Reasoning about Knowledge (TARK 1988), Morgan Kaufmann, 83 to 95 (1988)"
    locator: the whole paper (the postulates EE1 to EE5 and the two-way translation between entrenchment and contraction)
  - paper: "Peter Gärdenfors, Belief revision: an introduction, in Peter Gärdenfors (ed.), Belief Revision, Cambridge University Press (1992)"
    locator: Section 4.1 (EE1 to EE5, the conditions (C≤) and (C-), and Theorems 9 to 12)
  - book: isbn:9780262071093
    title: "Peter Gärdenfors, Knowledge in Flux: Modeling the Dynamics of Epistemic States, MIT Press (1988)"
    locator: the chapter on epistemic entrenchment
---

Epistemic entrenchment is an order on sentences by how firmly they are believed. When a belief set must lose $p$, it gives up the sentences that are least entrenched, and keeps a belief $q$ when the disjunction $p \vee q$ is more entrenched than $p$. Peter Gärdenfors and David Makinson (1988) gave five postulates for the order and showed that the orders that satisfy them correspond one to one to the contractions that satisfy all eight [AGM postulates](/agm-postulates/). So entrenchment is a third way, beside [partial meet contraction](/partial-meet-contraction/) and [systems of spheres](/grove-spheres/), to build the same operators.

## Definition

Let $\mathrm{Cn}$ be a Tarskian, compact consequence operation that includes classical propositional logic and satisfies the deduction theorem, let $\vdash p$ mean $p \in \mathrm{Cn}(\emptyset)$, and let $K$ be a belief set. An **epistemic entrenchment** related to $K$ is a relation $\le$ on sentences, where $p \le q$ reads "$q$ is at least as entrenched as $p$", such that for all $p, q, r$:

| | name | postulate |
|---|---|---|
| EE1 | transitivity | if $p \le q$ and $q \le r$, then $p \le r$ |
| EE2 | dominance | if $p \vdash q$, then $p \le q$ |
| EE3 | conjunctiveness | $p \le p \wedge q$ or $q \le p \wedge q$ |
| EE4 | minimality | if $K \ne K_\bot$, then $p \notin K$ if and only if $p \le q$ for all $q$ |
| EE5 | maximality | if $q \le p$ for all $q$, then $\vdash p$ |

Write $p < q$ for $p \le q$ and not $q \le p$. Some consequences follow at once. The order is connected: $p \le q$ or $q \le p$, by EE2 and EE3 applied to $p \wedge q$. A conjunction is as entrenched as its weaker part. Sentences outside $K$ are the least entrenched, and tautologies are the most entrenched.

**From entrenchment to contraction.** The condition

$$\text{(C÷)} \qquad q \in K \div p \text{ if and only if } q \in K \text{ and } (p < p \vee q \text{ or } \vdash p)$$

defines a contraction function. The test is on $p \vee q$, not on $q$: $q$ survives when the belief "$p$ or $q$" is firmer than $p$, so that it does not have to go with $p$.

**From contraction to entrenchment.** Given a contraction function, the condition

$$\text{(C}\le\text{)} \qquad p \le q \text{ if and only if } p \notin K \div (p \wedge q) \text{ or } \vdash p \wedge q$$

defines a relation: when forced to give up $p$ or $q$, one gives up $p$ (or both).

**Theorems** (Gärdenfors 1992, Theorems 9 and 10, after Gärdenfors and Makinson 1988). If $\le$ satisfies EE1 to EE5, then the contraction defined by (C÷) satisfies K÷1 to K÷8, and (C≤) applied to it gives back $\le$. If $\div$ satisfies K÷1 to K÷8, then the relation defined by (C≤) satisfies EE1 to EE5, and (C÷) applied to it gives back $\div$.

**The finite propositional case.** Over finitely many atoms, let $r$ be a rank function on worlds with $r(w) = 0$ exactly for the models of $K$. Then

$$E(p) = \min \{ r(w) : w \text{ is a world where } p \text{ is false} \},$$

with $E(p) = \infty$ for a tautology, gives the entrenchment $p \le q$ if and only if $E(p) \le E(q)$. A sentence is as firm as the most plausible world that refutes it. Every entrenchment over a finite language has this form, and the ranks are the spheres of [Grove's model](/grove-spheres/) read from the inside out.

## Examples and non-examples

Take two atoms $a, b$, the belief set $K = \mathrm{Cn}(a \wedge b)$ and the ranks $r(ab) = 0$, $r(\bar a b) = 1$, $r(\bar a \bar b) = r(a \bar b) = 2$, where $\bar a$ means that $a$ is false.

| sentence | $a \wedge b$ | $a$ | $b \to a$ | $b$ | $a \vee b$ | $a \to b$ | $a \vee \neg a$ |
|---|---|---|---|---|---|---|---|
| entrenchment $E$ | 1 | 1 | 1 | 2 | 2 | 2 | $\infty$ |

This order satisfies EE1 to EE5: the order is given by numbers, so EE1 holds; EE2 and EE3 follow from the minimum in the definition of $E$; and $E(p) = 0$ exactly for the sentences that are false in $ab$, which are the sentences outside $K$.

Contract by $a$ with (C÷). Then $E(a) = 1$, and

- $b$ stays, since $E(a \vee b) = 2 > 1$;
- $a \to b$ stays, since $a \vee (a \to b)$ is a tautology;
- $b \to a$ goes, since $a \vee (b \to a)$ is $b \to a$, with $E = 1$.

So $K \div a = \mathrm{Cn}(b)$, whose models are $ab$ and $\bar a b$, and by the [Levi identity](/levi-identity/) $K * \neg a = \mathrm{Cn}(\neg a \wedge b)$. This is also what the spheres $\{ab\} \subset \{ab, \bar a b\} \subset$ all worlds give, and (C≤) applied to this contraction returns the table above for all 16 sentences up to equivalence.

Non-examples:

- **A partial order.** If $a$ and $b$ are not comparable, EE3 fails for $a \wedge b$, since $a \wedge b$ cannot be at least as firm as either.
- **Equal firmness for all beliefs.** Put the sentences outside $K$ at level 0, the other non-tautologies at level 1 and the tautologies at level 2. For a consistent $K$ this satisfies EE1 to EE5, and (C÷) then gives full meet contraction. So EE1 to EE5 allow this crude choice. Without the separate top level for tautologies, EE5 fails.
- **Testing $q$ instead of $p \vee q$.** Rott's condition, $q \in K \div p$ if and only if $q \in K$ and ($p < q$ or $\vdash p$), gives a contraction that satisfies K÷1 to K÷4 and K÷6 to K÷8 but not recovery, and that gives the same revision through the Levi identity (Gärdenfors 1992, Theorems 11 and 12). In the example, contract by $b$, with $E(b) = 2$. Condition (C÷) gives $\mathrm{Cn}(b \to a)$, with the models $ab$, $\bar a \bar b$ and $a \bar b$. Rott's condition keeps only the sentences with $E > 2$, the tautologies, so it gives $\mathrm{Cn}(\emptyset)$, and $\mathrm{Cn}(\emptyset) + b$ does not contain $a$. Both give $K * \neg b = \mathrm{Cn}(\neg b)$.

## Related definitions

- [Partial meet contraction](/partial-meet-contraction/) and the [AGM representation theorem](/agm-representation-theorem/): the contractions from entrenchments are exactly the transitively relational partial meet contractions.
- [Grove's spheres](/grove-spheres/) and faithful preorders in the [Katsuno and Mendelzon theorem](/katsuno-mendelzon-revision/): the same information on worlds instead of sentences.
- [Ordinal conditional functions](/ordinal-conditional-functions/): numerical ranks on worlds, whose induced order on sentences is an entrenchment, with the numbers used for iterated revision.
- Safe contraction (Alchourrón and Makinson 1985) uses a relation on sentences too, but removes the least elements of each minimal subset that implies $p$.

## References
