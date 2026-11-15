---
tag: 1J9WQT
kind: definition
slug: agm-postulates
name: AGM postulates
aliases:
- Alchourron-Gardenfors-Makinson postulates
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: core
summary: Rationality postulates for expansion, contraction and revision of a logically closed belief set, such as success and minimal change.
prereqs: [belief-revision]
see_also: [levi-identity, partial-meet-contraction, agm-representation-theorem, epistemic-entrenchment, grove-spheres, katsuno-mendelzon-revision, gardenfors-impossibility-theorem, darwiche-pearl-postulates]
sources:
  - paper: doi:10.2307/2274239
    title: "Carlos E. Alchourrón, Peter Gärdenfors and David Makinson, On the logic of theory change: partial meet contraction and revision functions, Journal of Symbolic Logic 50(2), 510 to 530 (1985)"
    locator: the whole paper (the basic and supplementary postulates for contraction and revision)
  - book: isbn:9780262071093
    title: "Peter Gärdenfors, Knowledge in Flux: Modeling the Dynamics of Epistemic States, MIT Press (1988)"
    locator: Chapter 3 (the postulates for expansion, revision and contraction, with K*7 on p. 57)
  - paper: "Peter Gärdenfors, Belief revision: an introduction, in Peter Gärdenfors (ed.), Belief Revision, Cambridge University Press (1992)"
    locator: Section 2.1 (the assumptions on Cn) and Sections 3.1 and 3.2 (the postulates K*1 to K*8 and K-1 to K-8, and Theorems 1 and 2)
  - paper: doi:10.1016/0004-3702(91)90069-V
    title: Hirofumi Katsuno and Alberto O. Mendelzon, Propositional knowledge base revision and minimal change, Artificial Intelligence 52(3), 263 to 294 (1991)
    locator: Section 3 (the postulates R1 to R6 for formulas of a finite propositional language)
---

The AGM postulates are the rules that a rational change of a logically closed belief set should obey. Carlos Alchourrón, Peter Gärdenfors and David Makinson stated them in 1985 for contraction and revision. There are eight for each operation: six basic ones and two supplementary ones, which tie the change by a conjunction to the changes by its parts. They do not pick one operator. They mark out a family, and the representation theorems show which constructions give exactly that family. The problem itself is on [belief revision](/belief-revision/).

## Definition

The language $L$ has a consequence operation $\mathrm{Cn}$ that is Tarskian, includes classical propositional logic, is compact and satisfies the deduction theorem (Gärdenfors 1992, Section 2.1). We write $\vdash p$ when $p \in \mathrm{Cn}(\emptyset)$. A belief set is a set $K$ with $K = \mathrm{Cn}(K)$, and $K_\bot$ is the set of all sentences. Expansion is $K + p = \mathrm{Cn}(K \cup \{p\})$.

**Revision.** A function $*$ that maps each belief set $K$ and sentence $p$ to a set $K * p$ is an AGM revision when it satisfies:

| | name | postulate |
|---|---|---|
| K*1 | closure | $K * p$ is a belief set |
| K*2 | success | $p \in K * p$ |
| K*3 | inclusion | $K * p \subseteq K + p$ |
| K*4 | vacuity | if $\neg p \notin K$, then $K + p \subseteq K * p$ |
| K*5 | consistency | $K * p = K_\bot$ if and only if $\vdash \neg p$ |
| K*6 | extensionality | if $\vdash p \leftrightarrow q$, then $K * p = K * q$ |
| K*7 | superexpansion | $K * (p \wedge q) \subseteq (K * p) + q$ |
| K*8 | subexpansion | if $\neg q \notin K * p$, then $(K * p) + q \subseteq K * (p \wedge q)$ |

**Contraction.** A function $\div$ is an AGM contraction when it satisfies:

| | name | postulate |
|---|---|---|
| K÷1 | closure | $K \div p$ is a belief set |
| K÷2 | inclusion | $K \div p \subseteq K$ |
| K÷3 | vacuity | if $p \notin K$, then $K \div p = K$ |
| K÷4 | success | if not $\vdash p$, then $p \notin K \div p$ |
| K÷5 | recovery | if $p \in K$, then $K \subseteq (K \div p) + p$ |
| K÷6 | extensionality | if $\vdash p \leftrightarrow q$, then $K \div p = K \div q$ |
| K÷7 | conjunctive overlap | $(K \div p) \cap (K \div q) \subseteq K \div (p \wedge q)$ |
| K÷8 | conjunctive inclusion | if $p \notin K \div (p \wedge q)$, then $K \div (p \wedge q) \subseteq K \div p$ |

Postulates 1 to 6 are the basic ones and 7 and 8 the supplementary ones. Gärdenfors (1992) writes K-1 to K-8 for the contraction postulates.

**Useful equivalent forms.** Under K*1 to K*6, postulate K*7 is equivalent to $(K * p) \cap (K * q) \subseteq K * (p \vee q)$, and K*7 with K*8 is equivalent to the factoring condition: $K * (p \vee q)$ is $K * p$, or $K * q$, or $(K * p) \cap (K * q)$. Under K÷1 to K÷6, K÷7 with K÷8 is equivalent to: $K \div (p \wedge q)$ is $K \div p$, or $K \div q$, or $(K \div p) \cap (K \div q)$.

**The finite propositional form.** Over $n$ atoms a belief set is $\mathrm{Cn}(\psi)$ for one formula $\psi$, and $\mathrm{Mod}(\psi)$ determines it. Katsuno and Mendelzon (1991) restate K*1 to K*8 for an operator $\psi \circ \mu$ on formulas:

| | postulate |
|---|---|
| R1 | $\psi \circ \mu$ implies $\mu$ |
| R2 | if $\psi \wedge \mu$ is satisfiable, then $\psi \circ \mu \leftrightarrow \psi \wedge \mu$ |
| R3 | if $\mu$ is satisfiable, then $\psi \circ \mu$ is satisfiable |
| R4 | if $\psi_1 \leftrightarrow \psi_2$ and $\mu_1 \leftrightarrow \mu_2$, then $\psi_1 \circ \mu_1 \leftrightarrow \psi_2 \circ \mu_2$ |
| R5 | $(\psi \circ \mu) \wedge \varphi$ implies $\psi \circ (\mu \wedge \varphi)$ |
| R6 | if $(\psi \circ \mu) \wedge \varphi$ is satisfiable, then $\psi \circ (\mu \wedge \varphi)$ implies $(\psi \circ \mu) \wedge \varphi$ |

R1 is K*2, R2 joins K*3 and K*4, R3 is the hard half of K*5, R4 is K*6 together with the fact that only $\mathrm{Cn}(\psi)$ matters, R5 is K*7 and R6 is K*8. K*1 holds by construction, because the result is a formula.

## Examples and non-examples

Most examples use two atoms $a, b$. Then each belief set is given by a set of the four worlds, and sentences are counted up to logical equivalence.

- **Full meet revision** sets $K * p = K + p$ when $\neg p \notin K$ and $K * p = \mathrm{Cn}(p)$ otherwise. It satisfies all eight revision postulates.
- **[Dalal's operator](/dalal-revision/)**, which keeps the models of $p$ that are closest in Hamming distance to the models of $K$, satisfies all eight.
- **Forgetting all of $K$.** The operator $K * p = \mathrm{Cn}(p)$ satisfies every postulate except K*4. For $K = \mathrm{Cn}(a)$ and $p = b$ it gives $\mathrm{Cn}(b)$, which has lost $a$.
- **Contraction without recovery.** For $K = \mathrm{Cn}(a \wedge b)$, let $K \div p = \mathrm{Cn}(\emptyset)$ when $p \in K$ is not a tautology, and $K \div p = K$ otherwise. This satisfies every contraction postulate except K÷5: $(K \div a) + a = \mathrm{Cn}(a)$ does not contain $b$.
- **Basic but not supplementary.** For $K = \mathrm{Cn}(a \wedge b)$ there are 189 [partial meet contractions](/partial-meet-contraction/). All of them satisfy K÷1 to K÷6. Only 49 satisfy K÷7, only 45 satisfy K÷8, and 13 satisfy both. The 13 are the transitively relational ones, one for each total preorder on the three worlds outside $\mathrm{Mod}(K)$.
- **A natural operator that fails K*8.** Satoh's operator keeps the models of $\mu$ whose set of changed atoms is minimal under inclusion. Over three atoms, take $\psi = \neg a \wedge \neg b \wedge \neg c$, $\mu$ with the models $\{a\}$, $\{b\}$ and $\{b, c\}$ (each model written as its set of true atoms), and $\varphi$ with the models $\{a\}$ and $\{b, c\}$. Then $\psi \circ \mu$ has the models $\{a\}$ and $\{b\}$, so $(\psi \circ \mu) \wedge \varphi$ has the one model $\{a\}$. But $\psi \circ (\mu \wedge \varphi)$ has the models $\{a\}$ and $\{b, c\}$, because $\{b\}$ is gone and $\{b, c\}$ becomes minimal. So R6 fails. Over two atoms Satoh's operator satisfies all six.

## Related definitions

- The [Levi identity](/levi-identity/) $K * p = (K \div \neg p) + p$ and the Harper identity $K \div p = K \cap (K * \neg p)$ translate between the two lists: basic contraction postulates give basic revision postulates and back, and the supplementary ones match too (Gärdenfors 1992, Theorems 1 and 2). Recovery is not needed for the step from contraction to revision.
- [Partial meet contraction](/partial-meet-contraction/) gives exactly the contractions with K÷1 to K÷6, and transitively relational partial meet contraction gives exactly those with K÷1 to K÷8; see the [AGM representation theorem](/agm-representation-theorem/).
- An [epistemic entrenchment](/epistemic-entrenchment/) order on sentences and a [system of spheres](/grove-spheres/) on worlds each give exactly the operators with all eight postulates.
- The [Katsuno and Mendelzon theorem](/katsuno-mendelzon-revision/) characterizes R1 to R6 by faithful total preorders on worlds.
- The [Darwiche and Pearl postulates](/darwiche-pearl-postulates/) add rules for sequences of revisions, which the AGM postulates leave free.
- The [Gärdenfors impossibility theorem](/gardenfors-impossibility-theorem/) shows that the Ramsey test for conditionals cannot be added to a weak form of these postulates.

## References
