---
tag: RMK6AM
kind: definition
slug: levi-identity
name: Levi identity
aliases:
- revision by contraction and expansion
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: core
summary: Defines revision by p as contraction by not p followed by expansion by p.
prereqs: [agm-postulates]
see_also: [partial-meet-contraction, agm-representation-theorem, epistemic-entrenchment, grove-spheres, belief-revision]
sources:
  - paper: "Peter Gärdenfors, Belief revision: an introduction, in Peter Gärdenfors (ed.), Belief Revision, Cambridge University Press (1992)"
    locator: Section 3 (Theorems 1 and 2, on the Levi and Harper identities)
  - paper: doi:10.2307/2274239
    title: "Carlos E. Alchourrón, Peter Gärdenfors and David Makinson, On the logic of theory change: partial meet contraction and revision functions, Journal of Symbolic Logic 50(2), 510 to 530 (1985)"
    locator: the whole paper (revision defined from partial meet contraction by the Levi identity)
  - book: isbn:9780262071093
    title: "Peter Gärdenfors, Knowledge in Flux: Modeling the Dynamics of Epistemic States, MIT Press (1988)"
    locator: Chapter 3 (revision and contraction and the identities that connect them)
---

The Levi identity defines revision from contraction: to revise a belief set $K$ by $p$, first give up $\neg p$, then add $p$. In symbols, $K * p = (K \div \neg p) + p$. It reduces the hard part of [belief revision](/belief-revision/), choosing what to give up, to contraction, and it carries the [AGM postulates](/agm-postulates/) for contraction over to revision. Its converse, the Harper identity, defines contraction from revision.

## Definition

Let $\mathrm{Cn}$ be a Tarskian, compact consequence operation that includes classical propositional logic and satisfies the deduction theorem. Let $K$ be a belief set, $+$ expansion, and $\div$ a contraction function. The **Levi identity** defines a revision function by

$$K * p = (K \div \neg p) + p = \mathrm{Cn}((K \div \neg p) \cup \{p\}).$$

Given a revision function $*$, the **Harper identity** defines a contraction function by

$$K \div p = K \cap (K * \neg p).$$

The first step of the Levi identity makes room for $p$: after the contraction, $\neg p$ is no longer believed, so adding $p$ does not make the set inconsistent. The second step adds $p$ and closes under $\mathrm{Cn}$. The Harper identity keeps what is in $K$ and would still be believed after learning $\neg p$.

### The basic postulates carry over

**Theorem** (Gärdenfors 1992, Theorem 1). If $\div$ satisfies K÷1 to K÷4 and K÷6, then the revision $*$ given by the Levi identity satisfies K*1 to K*6. If $\div$ also satisfies K÷7, then $*$ satisfies K*7, and if $\div$ also satisfies K÷8, then $*$ satisfies K*8.

*Proof of the basic part.* Write $C = K \div \neg p$, so $K * p = C + p$.

- K*1: $C + p$ is $\mathrm{Cn}$ of a set, so it is a belief set.
- K*2: $p \in \mathrm{Cn}(C \cup \{p\})$.
- K*3: $C \subseteq K$ by K÷2, and expansion is monotone, so $C + p \subseteq K + p$.
- K*4: if $\neg p \notin K$, then $C = K$ by K÷3, so $K * p = K + p$.
- K*5: if $\vdash \neg p$, then $p$ is inconsistent and $C + p = K_\bot$. If not $\vdash \neg p$, then $\neg p \notin C$ by K÷4. Suppose $C + p = K_\bot$. By the deduction theorem, $p \to \bot \in \mathrm{Cn}(C)$, and $C$ is closed by K÷1, so $\neg p \in C$, a contradiction. So $C + p$ is consistent.
- K*6: if $\vdash p \leftrightarrow q$, then $\vdash \neg p \leftrightarrow \neg q$, so $K \div \neg p = K \div \neg q$ by K÷6, and expansions by equivalent sentences are equal. $\square$

The proof never uses recovery, K÷5. So contractions that differ only in how much of $K$ they would give back by recovery give the same revision.

**Theorem** (Gärdenfors 1992, Theorem 2). If $*$ satisfies K*1 to K*6, then the contraction given by the Harper identity satisfies K÷1 to K÷6, with recovery. K*7 gives K÷7 and K*8 gives K÷8.

The two identities are inverse in one direction and nearly inverse in the other. Starting from a revision with K*1 to K*6, the Harper identity and then the Levi identity give back the same revision. Starting from a contraction with K÷1 to K÷6, the Levi identity and then the Harper identity give back the same contraction. A contraction without recovery comes back as a different contraction: the one with recovery that has the same revision.

## Examples and non-examples

Take two atoms $a, b$ and $K = \mathrm{Cn}(a \wedge b)$, and revise by $\neg a$. The Levi identity asks for $K \div \neg\neg a$, which is $K \div a$ by K÷6.

| contraction $K \div a$ | its models | $K * \neg a = (K \div a) + \neg a$ |
|---|---|---|
| keep $b$ (maxichoice) | $ab$, $\bar a b$ | $\mathrm{Cn}(\neg a \wedge b)$ |
| keep $a \leftrightarrow b$ (maxichoice) | $ab$, $\bar a \bar b$ | $\mathrm{Cn}(\neg a \wedge \neg b)$ |
| full meet | $ab$, $\bar a b$, $\bar a \bar b$ | $\mathrm{Cn}(\neg a)$ |
| give up everything, $\mathrm{Cn}(\emptyset)$ | all four worlds | $\mathrm{Cn}(\neg a)$ |

Here $\bar a$ means that $a$ is false. The first three rows are [partial meet contractions](/partial-meet-contraction/). The last row is not: it fails recovery, because $(K \div a) + a = \mathrm{Cn}(a)$ does not contain $b$. Yet it gives the same revision as full meet contraction. Apply the Harper identity to that revision: $K \cap \mathrm{Cn}(\neg a)$ has the models $ab$, $\bar a b$ and $\bar a \bar b$, which is $\mathrm{Cn}(a \to b)$, the full meet contraction. So the round trip from a contraction without recovery does not come back to where it started.

For this $K$ there are 189 partial meet contractions, counting sentences up to equivalence. For each of them, the Levi identity gives a revision that satisfies K*1 to K*6, and the Harper identity applied to that revision gives back the same contraction.

A non-example of the Levi pattern is revision by "contract by $p$, then add $p$". For $K = \mathrm{Cn}(a \wedge b)$ and $p = \neg a$, the sentence $\neg a$ is not in $K$, so $K \div \neg a = K$ and the result is $K + \neg a = K_\bot$. The identity must contract by the negation.

## Related definitions

- [AGM postulates](/agm-postulates/): the lists K*1 to K*8 and K÷1 to K÷8 that the identities translate.
- [Partial meet contraction](/partial-meet-contraction/): the AGM construction of contraction, which the Levi identity turns into partial meet revision.
- [Epistemic entrenchment](/epistemic-entrenchment/): another way to build the contraction, and with it the revision.
- [Grove's spheres](/grove-spheres/): a construction of revision on worlds, from which the Harper identity gives the contraction. In model terms, $\mathrm{Mod}(K \div p) = \mathrm{Mod}(K) \cup \mathrm{Mod}(K * \neg p)$.
- Expansion $K + p$, the operation that both identities use, is the unique operation that satisfies the expansion postulates of Gärdenfors (1988, Chapter 3).

## References
