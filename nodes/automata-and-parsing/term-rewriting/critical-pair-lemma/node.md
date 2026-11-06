---
tag: EVYM1C
kind: theorem
slug: critical-pair-lemma
name: Critical pair lemma
aliases:
- Knuth-Bendix critical pair lemma
area: automata-and-parsing/term-rewriting
level: core
summary: A terminating system is locally confluent iff all its critical pairs are joinable.
prereqs: [critical-pair, local-confluence, joinability, newman-lemma]
see_also: [knuth-bendix-completion, confluence, confluence-decision-problem, orthogonal-confluence-theorem, termination, linearity]
sources:
  - paper: "Donald E. Knuth and Peter B. Bendix, Simple word problems in universal algebras, in J. Leech (editor), Computational Problems in Abstract Algebra, Pergamon Press, 1970"
    locator: pp. 263 to 297 (the test of all superpositions for a well-founded set of reductions)
  - paper: doi:10.1145/322217.322230
    title: Gérard Huet, Confluent reductions, abstract properties and applications to term rewriting systems, Journal of the ACM 27(4) (1980)
    locator: pp. 797 to 821, Section 3 (the critical pair lemma for arbitrary term rewriting systems)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 6, Section 6.2, Critical pairs (the critical pair lemma and the decidability of confluence for finite terminating systems)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 2, First-order term rewriting systems (the critical pair lemma)
---

The **critical pair lemma** says that a term rewriting system is [locally confluent](/local-confluence/) if and only if all its [critical pairs](/critical-pair/) are [joinable](/joinability/). Local confluence speaks of infinitely many peaks, one for each term and each pair of redexes in it, while a finite system has only finitely many critical pairs. Together with [Newman's lemma](/newman-lemma/) the lemma gives the Knuth-Bendix criterion: a terminating system is confluent iff all its critical pairs are joinable, which makes confluence decidable for finite terminating systems and is the engine of [Knuth-Bendix completion](/knuth-bendix-completion/).

## Statement

We use the notation of the term rewriting pages: terms $T(\Sigma, V)$, positions as sequences of positive integers, $t|_p$ and $t[s]_p$, substitutions $\sigma$, rules $l \to r$, the rewrite relation $\to_R$ and its reflexive transitive closure $\to_R^*$. $\mathrm{CP}(R)$ is the set of critical pairs of $R$.

**Theorem (critical pair lemma).** For every term rewriting system $R$,

$$R \text{ is locally confluent} \iff s \downarrow_R t \text{ for every } \langle s, t \rangle \in \mathrm{CP}(R).$$

**Corollary (Knuth and Bendix, 1970).** If $R$ is terminating, then $R$ is confluent iff all its critical pairs are joinable. If $R$ is finite and terminating, this is decidable: compute the finitely many critical pairs, compute a [normal form](/normal-form/) of each side by any strategy, and compare. The pair $\langle s, t \rangle$ is joinable iff the normal forms are equal, because a terminating confluent system has unique normal forms; and if some pair has two different normal forms, $R$ is not confluent.

The lemma needs no hypothesis of termination or of [left-linearity](/linearity/). Only the corollary needs termination.

## In plain words

When two rules can both rewrite a term, three things can happen. They can act on separate parts of the term, and then doing both, in either order, gives the same result. One rule can act inside a part that the other rule only copies or moves around, and then the other copies can be fixed up afterwards, so again the results meet. Or the two rules can really compete for the same symbols. Only this last case can break agreement.

Each competing case is a copy, with some parts filled in, of one most general conflict between two rules. There are only finitely many such general conflicts. So to know that every small disagreement can be resolved, it is enough to resolve this finite list.

## Proof

Two properties of $\to_R$ are used, both direct from the definition of a rewrite step $u[l\sigma]_p \to_R u[r\sigma]_p$:

- **Closure under substitution:** if $s \to_R t$ then $s\tau \to_R t\tau$ for every substitution $\tau$, because $(l\sigma)\tau = l(\sigma\tau)$. By induction on length, $s \to_R^* t$ implies $s\tau \to_R^* t\tau$.
- **Closure under context:** if $s \to_R t$ then $u[s]_p \to_R u[t]_p$ for every term $u$ and position $p$. Again this extends to $\to_R^*$.

**($\Rightarrow$)** Let $\langle s, t \rangle$ come from the overlap $l_1\theta$, so $s = (l_1\theta)[r_2\theta]_p \leftarrow_R l_1\theta \to_R r_1\theta = t$. This is a local peak, and local confluence makes it joinable.

**($\Leftarrow$)** Assume all critical pairs are joinable, and take a peak

$$t_1 = t[r_1\sigma_1]_{p_1} \ \leftarrow_R\ t \ \to_R\ t[r_2\sigma_2]_{p_2} = t_2, \qquad t|_{p_1} = l_1\sigma_1,\ t|_{p_2} = l_2\sigma_2,$$

with the rules $l_1 \to r_1$ and $l_2 \to r_2$ renamed apart. There are three cases.

1. **Disjoint positions.** If neither of $p_1, p_2$ is a prefix of the other, the two redexes do not overlap. Then $t_1|_{p_2} = l_2\sigma_2$ and $t_2|_{p_1} = l_1\sigma_1$, and both $t_1$ and $t_2$ rewrite in one step to $t[r_1\sigma_1]_{p_1}[r_2\sigma_2]_{p_2}$.
2. **Nested positions, critical overlap.** Up to swapping the two steps, $p_2 = p_1 q$ for some position $q$. By closure under context it is enough to join $r_1\sigma_1 \leftarrow l_1\sigma_1 \to (l_1\sigma_1)[r_2\sigma_2]_q$, the peak at $t|_{p_1}$. Suppose $q \in \mathrm{Pos}_\Sigma(l_1)$, a function-symbol position of $l_1$. Then $(l_1|_q)\sigma_1 = l_2\sigma_2$. Since the rules share no variable, $\sigma = \sigma_1 \cup \sigma_2$ is a well-defined substitution with $(l_1|_q)\sigma = l_2\sigma$, so $l_1|_q$ and $l_2$ are unifiable. If $q = \varepsilon$ and the two rules are copies of the same rule, then $\sigma_1$ and $\sigma_2$ agree on the copied variables, so $r_1\sigma_1 = r_2\sigma_2$ and the peak is trivial. Otherwise, with $\theta$ the most general unifier, $\sigma = \theta\tau$ for some $\tau$, and $\langle (l_1\theta)[r_2\theta]_q, r_1\theta \rangle$ is a critical pair. By assumption its two sides reduce to a common $u$. Applying $\tau$ gives $(l_1\sigma)[r_2\sigma]_q \to_R^* u\tau$ and $r_1\sigma \to_R^* u\tau$, and these are exactly the two sides of the peak.
3. **Nested positions, variable overlap.** Now $p_2 = p_1 q$ and $q$ is not in $\mathrm{Pos}_\Sigma(l_1)$. Then $q = q_1 q_2$ where $l_1|_{q_1} = x$ is a variable and $(x\sigma_1)|_{q_2} = l_2\sigma_2$. Let $x\sigma_1 \to_R w$ be the step $x\sigma_1 \to_R (x\sigma_1)[r_2\sigma_2]_{q_2}$, and let $\sigma_1'$ agree with $\sigma_1$ except that $x\sigma_1' = w$. For any term $u$, $u\sigma_1 \to_R^* u\sigma_1'$, by rewriting each occurrence of $x\sigma_1$ that comes from an occurrence of $x$ in $u$. On the left of the peak, $r_1\sigma_1 \to_R^* r_1\sigma_1'$. On the right, $(l_1\sigma_1)[r_2\sigma_2]_q$ is $l_1\sigma_1$ with the occurrence of $x$ at $q_1$ already rewritten; rewriting the other occurrences of $x$ gives $l_1\sigma_1'$, and one step at the root gives $r_1\sigma_1'$. So both sides reach $r_1\sigma_1'$.

In each case the peak is joinable, so $R$ is locally confluent. The corollary follows from Newman's lemma, which turns local confluence of a terminating system into confluence, and from the fact that confluence implies local confluence. $\blacksquare$

## Consequences

- **Deciding confluence of terminating systems.** For a finite terminating $R$, confluence is decided by joining the critical pairs; see [deciding confluence](/confluence-decision-problem/). For the group axioms $e \cdot x \to x$, $i(x) \cdot x \to e$ and $(x \cdot y) \cdot z \to x \cdot (y \cdot z)$, the critical pair $\langle e \cdot z,\ i(y) \cdot (y \cdot z) \rangle$ from the overlap $(i(y) \cdot y) \cdot z$ has the distinct normal forms $z$ and $i(y) \cdot (y \cdot z)$, so the system is not confluent. For the ten-rule convergent system of groups that completion produces, each of its 55 critical pairs (counting a root overlap of two different rules once for each order) has equal normal forms on both sides.
- **[Knuth-Bendix completion](/knuth-bendix-completion/)** computes critical pairs, normalizes them and turns each non-joinable pair into a new rule oriented by a reduction ordering. When no non-joinable pair is left, the lemma and Newman's lemma give a convergent system.
- **Orthogonal systems.** A left-linear system without critical pairs is locally confluent by the lemma. Confluence without termination needs the stronger argument of the [orthogonal confluence theorem](/orthogonal-confluence-theorem/).
- **Theorem proving.** Superposition calculi for first-order logic with equality, such as [superposition](/superposition/), compute the same overlaps between clauses.

## Tightness

- **Local confluence, not confluence.** Without termination, joinable critical pairs give only local confluence. Huet's system $f(x, x) \to a$, $f(x, g(x)) \to b$, $c \to g(c)$ has no critical pairs, since $x = g(x)$ has no unifier, so it is locally confluent. Yet $f(c, c) \to a$ and $f(c, c) \to f(c, g(c)) \to b$, with $a \ne b$ normal forms. So the termination hypothesis of the corollary cannot be dropped.
- **Joinable, not trivial.** The lemma cannot ask for trivial critical pairs. In $\{f(a) \to b,\ a \to c,\ f(c) \to b\}$ the critical pair $\langle f(c), b \rangle$ is not trivial, but it joins at $b$, and the system is confluent.
- **All pairs are needed.** Leaving out the overlaps of a rule with itself is wrong: $f(f(x)) \to g(x)$ alone has only the self-overlap $f(f(f(x)))$, its critical pair $\langle f(g(x)), g(f(x)) \rangle$ is not joinable, and the system is not confluent even though it terminates.
- **Only one direction of reduction.** The corollary asks for $s \downarrow t$, not for $s \leftrightarrow^* t$, which always holds for a critical pair.

## History

Knuth and Bendix stated the criterion for terminating systems in their 1970 paper, where they used it to decide when a set of reductions is complete and to build the completion procedure. Huet in 1980 separated the two ingredients: the critical pair lemma, valid for every term rewriting system and giving local confluence, and Newman's lemma, which adds termination. His paper also introduced the analysis of variable overlaps for non-terminating systems.

## References
