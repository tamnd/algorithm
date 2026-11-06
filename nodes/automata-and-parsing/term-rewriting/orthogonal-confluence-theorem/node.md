---
tag: 0FCP7R
kind: theorem
slug: orthogonal-confluence-theorem
name: Orthogonal systems are confluent
aliases:
- Huet's orthogonality theorem
area: automata-and-parsing/term-rewriting
level: advanced
summary: Every orthogonal term rewriting system is confluent.
prereqs: [orthogonal-rewrite-system, confluence, linearity]
see_also: [church-rosser-theorem, critical-pair-lemma, newman-lemma, combinatory-logic, outermost-reduction, parallel-rewriting, hindley-rosen-lemma, normal-form]
sources:
  - paper: doi:10.1145/321738.321750
    title: Barry K. Rosen, Tree-manipulating systems and Church-Rosser theorems, Journal of the ACM 20(1) (1973)
    locator: pp. 160 to 187 (confluence of non-overlapping left-linear rule schemes)
  - paper: doi:10.1145/322217.322230
    title: Gérard Huet, Confluent reductions, abstract properties and applications to term rewriting systems, Journal of the ACM 27(4) (1980)
    locator: pp. 797 to 821, Section 3 (left-linear systems whose critical pairs are parallel closed are confluent, by parallel reduction)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 4, Orthogonality (confluence by the parallel moves lemma, by developments, and for weakly orthogonal systems)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 6, Confluence (orthogonal systems, proof by parallel reduction)
---

The **orthogonal confluence theorem** says that every [orthogonal](/orthogonal-rewrite-system/) [term rewriting system](/term-rewriting-system/), that is, every system whose rules are [left-linear](/linearity/) and do not overlap, is [confluent](/confluence/). It needs no termination, so it covers systems such as [combinatory logic](/combinatory-logic/), lazy functional programs and streams, where [Newman's lemma](/newman-lemma/) does not apply. It is the first-order form of the [Church-Rosser theorem](/church-rosser-theorem/), and it is proved the same way, with parallel or multi-step reduction.

## Statement

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, $t|_p$ and $t[s]_p$, substitutions $\sigma$, rules $l \to r$ with $l \notin V$ and $\mathrm{Var}(r) \subseteq \mathrm{Var}(l)$, and $\to_R^*$ for the reflexive transitive closure of $\to_R$.

**Theorem.** Let $R$ be a term rewriting system, finite or infinite, such that

1. every left side $l$ is linear, and
2. no two rules overlap: for rules $l_1 \to r_1$ and $l_2 \to r_2$ renamed apart and a non-variable position $p$ of $l_1$, the terms $l_1|_p$ and $l_2$ are not unifiable, except when the two rules are the same and $p = \varepsilon$.

Then $\to_R$ is confluent: if $s \to_R^* t_1$ and $s \to_R^* t_2$, there is a $u$ with $t_1 \to_R^* u$ and $t_2 \to_R^* u$.

The same conclusion holds for **weakly orthogonal** systems, which are left-linear and have only trivial [critical pairs](/critical-pair/) $\langle t, t \rangle$ (Huet, 1980).

## In plain words

Suppose that the rules never look at the same variable twice and never compete for the same part of an expression. Then doing one simplification never spoils another one that was possible before: the other one may be copied, moved or thrown away, but it is still there to do. So if two people simplify the same expression in different ways, each can catch up with the other. They end up with the same result, even if simplification can go on forever.

## Proof

The full proof is in [the proof by multi-step reduction](proofs/main.md). Its structure:

1. **Multi-step reduction.** Define $s \Rightarrow t$ to contract a set of redexes of $s$ at once, possibly nested, from the inside out: $x \Rightarrow x$; it is closed under function symbols; and $x\sigma \Rightarrow x\tau$ for all $x \in \mathrm{Var}(l)$ gives $l\sigma \Rightarrow r\tau$.
2. **Sandwich.** ${\to_R} \subseteq {\Rightarrow} \subseteq {\to_R^*}$, so $\Rightarrow^* = \to_R^*$.
3. **Complete development.** By the overlap condition, at most one rule matches at the root of a term. Let $s^*$ contract every redex of $s$, from the inside out: $(l\sigma)^* = r\sigma^*$ with $x\sigma^* = (x\sigma)^*$.
4. **Redexes survive.** If $s = l\sigma$ and a multi-step from $s$ does not contract at the root, then it does not touch the pattern of $l$, because a redex there would overlap $l$; and since $l$ is linear, the result is $l\tau$ for one substitution $\tau$.
5. **Triangle.** $s \Rightarrow t$ implies $t \Rightarrow s^*$, by induction on $s$, with step 4 for a root redex that was not contracted.
6. **Diamond and tiling.** Two multi-steps from $s$ meet at $s^*$, so $\Rightarrow$ has the diamond property, and so does $\Rightarrow^*$ by tiling. With step 2 this is confluence of $\to_R$. $\blacksquare$

**Why single steps do not have the diamond property.** With $f(x) \to g(x, x)$ and $a \to b$, the term $f(a)$ rewrites to $g(a, a)$ and to $f(b)$. From $f(b)$ one step gives $g(b, b)$, but from $g(a, a)$ two steps are needed, one for each copy of the redex $a$. One multi-step on each side closes the peak: $g(a, a) \Rightarrow g(b, b)$ and $f(b) \Rightarrow g(b, b)$, and $g(b, b) = f(a)^*$.

## Consequences

- **Unique normal forms.** In an orthogonal system every term has at most one [normal form](/normal-form/), so an orthogonal system defines a partial function on terms, whatever the order of evaluation.
- **Equality by joining.** $s \leftrightarrow_R^* t$ iff $s$ and $t$ have a common reduct. Two distinct normal forms are therefore not equal in the [equational theory](/equational-theory/), so [combinatory logic](/combinatory-logic/) is consistent: $K \ne S$.
- **Functional programs.** Definitions by left-linear, non-overlapping pattern matching on constructors are orthogonal, so their results do not depend on the evaluation order, and lazy and strict evaluation agree whenever both terminate.
- **Strategies.** Confluence lets strategies be compared by whether they reach the unique normal form: [outermost reduction](/outermost-reduction/) does for left-normal systems, parallel-outermost reduction for all orthogonal systems, and [innermost reduction](/innermost-reduction/) need not.
- **Parallel evaluation.** Disjoint redexes can be contracted in any order or at the same time, which justifies [parallel rewriting](/parallel-rewriting/) of orthogonal systems.

## Tightness

- **Left-linearity is needed.** $\{ f(x, x) \to a,\ f(x, g(x)) \to b,\ c \to g(c) \}$ has no overlaps, and $f(c, c)$ has the two normal forms $a$ and $b$ (Huet, 1980).
- **Non-overlap is needed.** $\{ f(g(x)) \to a,\ g(b) \to c \}$ is left-linear, and $f(g(b))$ has the two normal forms $a$ and $f(c)$.
- **Termination can replace left-linearity.** A terminating system whose critical pairs are joinable is confluent, by the [critical pair lemma](/critical-pair-lemma/) and [Newman's lemma](/newman-lemma/), even if it is not left-linear. Neither theorem contains the other.
- **Orthogonality is not necessary.** $\{ a \to b,\ a \to c,\ b \to c \}$ has the critical pair $\langle b, c \rangle$, so it is not weakly orthogonal, yet it is confluent.
- **Normalization is not implied.** Orthogonality gives at most one normal form, not that one exists, and not that every reduction finds it: with $f(x) \to a$ and $b \to b$, the term $f(b)$ has the normal form $a$ and also an infinite reduction.

## History

Church and Rosser proved confluence of the lambda calculus in 1936, and Curry and Feys extended the method of residuals to combinatory logic. Rosen in 1973 proved the first-order theorem for "subtree replacement systems" with non-overlapping left-linear rule schemes, and O'Donnell in 1977 studied the same class with its normalizing strategies. Huet in 1980 gave the proof by parallel reduction for left-linear systems with parallel closed critical pairs, which contains the weakly orthogonal case. Klop in 1980 carried the theory over to higher-order rewriting with combinatory reduction systems. The proof through complete developments follows the method that Takahashi gave for the lambda calculus in 1995.

## References
