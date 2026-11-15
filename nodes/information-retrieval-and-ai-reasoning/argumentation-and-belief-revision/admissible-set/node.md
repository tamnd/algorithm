---
tag: 809Q84
kind: definition
slug: admissible-set
name: Admissible set of arguments
aliases:
- admissible extension
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: core
summary: A set of arguments with no attack inside it that defends each of its members, which means that it attacks every attacker of each member.
prereqs: [abstract-argumentation-framework]
see_also: [complete-extension, preferred-extension, grounded-extension, stable-extension-argumentation, argument-labelling, argument-acceptance-problem, argumentation-sat-encoding]
sources:
  - paper: doi:10.1016/0004-3702(94)00041-X
    title: Phan Minh Dung, On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games, Artificial Intelligence 77(2), 321 to 357 (1995)
    locator: Definitions 5 and 6 (p. 326), Lemma 10 and Theorem 11 (p. 327), and Lemma 18 (p. 329)
  - paper: "Pietro Baroni, Martin Caminada and Massimiliano Giacomin, An introduction to argumentation semantics, The Knowledge Engineering Review 26(4), 365 to 410 (2011)"
    locator: the whole paper (conflict-free and admissible sets and labellings)
  - book: isbn:9781848902756
    title: Wolfgang Dvořák and Paul E. Dunne, Computational problems in formal argumentation and their complexity, in Pietro Baroni, Dov Gabbay, Massimiliano Giacomin and Leendert van der Torre (eds), Handbook of Formal Argumentation, volume 1, College Publications (2018)
    locator: Section 3.3, Table 1 (the rows for conflict-free and admissible sets) and Reduction 3.6
---

An admissible set is a set of arguments that can be held together and that can answer every attack on it. It is the basic notion of Dung's theory of argumentation: complete, grounded, preferred and stable extensions are all admissible sets with an extra condition. The framework and its notation are on [abstract argumentation framework](/abstract-argumentation-framework/).

## Definition

Let $(A, R)$ be an argumentation framework and $S \subseteq A$.

**Conflict-free (Dung 1995, Definition 5).** $S$ is conflict-free when there are no $a, b \in S$ with $(a, b) \in R$. A self-attacking argument is in no conflict-free set.

**Defence (Definition 6).** $S$ defends an argument $a$ when for each $b$ with $(b, a) \in R$ there is a $c \in S$ with $(c, b) \in R$. Dung says that $a$ is acceptable with respect to $S$. An argument with no attacker is defended by every set, also by $\emptyset$.

**Admissible (Definition 6).** $S$ is admissible when $S$ is conflict-free and $S$ defends each of its members.

With the characteristic function $F(S) = \{a : S \text{ defends } a\}$, the second condition is $S \subseteq F(S)$. So a conflict-free set is admissible exactly when $S \subseteq F(S)$ (Lemma 18).

The two conditions are local and easy to check. Conflict-freeness looks at the attacks inside $S$. Defence looks, for each member, at its attackers and at the attackers of those. With adjacency lists both take $O(n + m)$ time for $n$ arguments and $m$ attacks.

## Examples and non-examples

Take the framework with $a \to b \to c \to d \to e$, the 2-cycle $e \leftrightarrow f$, and an argument $g$ that attacks itself and $d$.

```
a --> b --> c --> d --> e <--> f
                  ^
                  |
             g ---+   (g also attacks g)
```

A check of all 128 subsets gives exactly seven admissible sets:

$$\emptyset,\ \{a\},\ \{f\},\ \{a, c\},\ \{a, f\},\ \{a, c, e\},\ \{a, c, f\}.$$

- $\{a\}$ is admissible: $a$ has no attacker.
- $\{f\}$ is admissible: the only attacker of $f$ is $e$, and $f$ attacks $e$. A set can defend itself.
- $\{a, c\}$ is admissible: $b$ attacks $c$, and $a$ attacks $b$.
- $\{a, c, e\}$ is admissible: $e$ has the attackers $d$ and $f$. $c$ attacks $d$, and $e$ attacks $f$.

Non-examples:

- $\{c\}$ is conflict-free but not admissible. It is attacked by $b$ and does not attack $b$.
- $\{e\}$ is conflict-free but not admissible. It answers $f$ but not $d$.
- $\{e, f\}$ is not conflict-free, since $e$ and $f$ attack each other.
- $\{g\}$ is not conflict-free, since $g$ attacks itself. No admissible set contains $g$.
- $\{a, c, e, f\}$ is not conflict-free, so the union of the admissible sets $\{a, c, e\}$ and $\{a, c, f\}$ is not admissible.

In the Nixon framework, two arguments $a \leftrightarrow b$, the admissible sets are $\emptyset$, $\{a\}$ and $\{b\}$. In a 3-cycle $a \to b \to c \to a$, the only admissible set is $\emptyset$: a single argument does not attack its attacker, and two arguments of the cycle attack each other.

## Related definitions

- **Basic facts.** $\emptyset$ is always admissible. The union of two admissible sets need not be admissible, as the examples show, but the union of a chain of admissible sets is admissible. Dung's Fundamental Lemma (Lemma 10): if $S$ is admissible and defends $a$ and $a'$, then $S \cup \{a\}$ is admissible and defends $a'$. So an admissible set can grow one defended argument at a time.
- **[Complete extension](/complete-extension/).** An admissible set that contains every argument it defends: $S = F(S)$.
- **[Grounded extension](/grounded-extension/).** The least complete extension.
- **[Preferred extension](/preferred-extension/).** A maximal admissible set. Each admissible set is contained in one (Theorem 11).
- **[Stable extension](/stable-extension-argumentation/).** A conflict-free set that attacks every argument outside it. Every stable extension is admissible.
- **Naive extension.** A maximal conflict-free set. It need not be admissible: in $a \to b$, the set $\{b\}$ is a naive extension.
- **[Admissible labelling](/argument-labelling/).** The same notion with labels: each in argument has all its attackers out, and each out argument has an attacker that is in.
- **Complexity.** Checking that $S$ is admissible is easy (in logspace). Deciding whether an argument is in some admissible set is NP-complete, and so is deciding whether a nonempty admissible set exists. Sceptical acceptance is trivial, because $\emptyset$ is admissible (Dvořák and Dunne, Table 1). See [argument acceptance](/argument-acceptance-problem/).
- **[SAT encoding](/argumentation-sat-encoding/).** With one variable for each argument, conflict-freeness is a 2-clause $\neg x_a \vee \neg x_b$ for each attack, and defence is a clause for each attack on a member.

## References
