---
tag: KCSG4C
kind: definition
slug: term-context
name: Context (term with a hole)
aliases:
- term with a hole
- multihole context
area: automata-and-parsing/term-rewriting
level: core
summary: A term containing one distinguished hole, used to state where a rewrite step occurs.
prereqs: [term, subterm]
see_also: [rewrite-step, parallel-rewriting, well-founded-reduction-ordering, equational-theory, congruence-closure, critical-pair-lemma]
sources:
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 2, First-order term rewriting systems (contexts, one-hole and multi-hole)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 3.1, Terms, substitutions, and identities; Section 4.2, Term rewriting systems (closure of the rewrite relation under contexts)
  - paper: doi:10.1017/S0956796897002864
    title: Gérard Huet, Functional pearl, The zipper, Journal of Functional Programming 7(5) (1997)
    locator: pp. 549 to 554 (a term with a hole as a data structure for local edits)
---

A **context** is a [term](/term/) with one hole $\square$ in it. Filling the hole with a term $t$ gives the term $C[t]$. Contexts give a short way to say "the same term around a different subterm": a [rewrite step](/rewrite-step/) is $C[l\sigma] \to C[r\sigma]$, and a relation is closed under contexts when $s \to t$ implies $C[s] \to C[t]$ for every $C$. A context with several holes, a **multihole context**, describes several places at once.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers with root $\varepsilon$, $t|_p$ and $t[s]_p$, substitutions $\sigma$, rules $l \to r$.

Let $\square$ be a new constant, not in $\Sigma \cup V$. A **context** is a term $C \in T(\Sigma \cup \{\square\}, V)$ in which $\square$ occurs exactly once. For a term $t$, $C[t]$ is the result of replacing $\square$ by $t$. If the hole is at position $p$, then $C[t] = C[t]_p$ in the replacement notation. The **empty context** is $\square$ itself, with $\square[t] = t$.

A **multihole context** is a term $C \in T(\Sigma \cup \{\square\}, V)$ with $n \ge 0$ occurrences of $\square$. $C[t_1, \ldots, t_n]$ fills the holes from left to right, that is, in the order of their positions in the pre-order walk.

**Contexts and positions.** One-hole contexts and positions carry the same information:

1. For every term $s$ and $p \in \mathrm{Pos}(s)$, $s[\square]_p$ is a context with its hole at $p$, and $s = (s[\square]_p)[s|_p]$.
2. Each context $C$ has its hole at exactly one position $p_C$, and $C = C[\square]$ is $(C[u])[\square]_{p_C}$ for every $u$.
3. Composition: $C[D]$ is a context with hole position $p_C\, p_D$, and $(C[D])[t] = C[D[t]]$.
4. Cancellation: $C[s] = C[t]$ implies $s = t$.

Items 1 to 3 follow from the facts on [subterms](/subterm/): $(s[\square]_p)[s|_p]_p = s[s|_p]_p = s$, and $C[D]|_{p_C} = D$. For item 4, $s = C[s]|_{p_C} = C[t]|_{p_C} = t$.

**Closure under contexts.** A relation $\to$ on terms is **closed under contexts** (also **compatible**, or **monotone**) iff $s \to t$ implies $C[s] \to C[t]$ for all contexts $C$. It is enough to check the contexts of depth one:

$$s \to t \implies f(u_1, \ldots, u_{i-1}, s, u_{i+1}, \ldots, u_n) \to f(u_1, \ldots, u_{i-1}, t, u_{i+1}, \ldots, u_n)$$

for every $f \in \Sigma_n$, every $i$ and all terms $u_j$. *Proof.* By induction on the length of $p_C$. For $p_C = \varepsilon$, $C[s] = s \to t = C[t]$. For $p_C = i\,q$, $C = f(u_1, \ldots, D, \ldots, u_n)$ with $D$ in argument $i$ and $p_D = q$. By the induction hypothesis $D[s] \to D[t]$, and the depth-one condition gives $C[s] \to C[t]$. $\blacksquare$

A **rewrite relation** is closed under contexts and under substitutions. A rewrite relation that is also an equivalence is a **congruence** on terms that is closed under substitutions; $\leftrightarrow_E^*$ for a set of equations $E$ is the smallest one that contains $E$. A [reduction ordering](/well-founded-reduction-ordering/) is a well-founded order that is closed under contexts and substitutions.

## Examples and non-examples

**Filling a hole.** Let $C = f(g(\square), a)$. Its hole is at position 1.1. Then $C[h(x)] = f(g(h(x)), a)$, and $C[\square] = C$. With $D = h(\square, b)$, $C[D] = f(g(h(\square, b)), a)$, with the hole at $1.1.1$, and $C[D][c] = f(g(h(c, b)), a)$.

**All contexts of a term.** The term $t = f(g(x), f(a, x))$ has 6 positions, so 6 ways to write $t = C[u]$ with a one-hole context: $C = \square$ with $u = t$, $C = f(\square, f(a, x))$ with $u = g(x)$, $C = f(g(\square), f(a, x))$ with $u = x$, and three more for positions 2, 2.1 and 2.2. The contexts for 1.1 and 2.2 are different, though both fill to $t$ with $u = x$.

**A rewrite step.** With the rule $0 + y \to y$, the step $s(0) \times (0 + x) \to s(0) \times x$ is $C[(0 + y)\sigma] \to C[y\sigma]$ for $C = s(0) \times \square$ and $\sigma = \{y \mapsto x\}$.

**A multihole context.** $C = g(\square, \square)$ has two holes, and $C[0 + s(0), 0 + s(0)] = g(0 + s(0), 0 + s(0))$. Contracting both redexes at once, $C[0 + s(0), 0 + s(0)] \to C[s(0), s(0)]$, is a [parallel rewriting](/parallel-rewriting/) step.

**The zipper.** A program that edits a large term in many nearby places can store the term as a pair of a context and a subterm, with the context kept as the list of nodes on the path from the hole to the root. Moving the hole one step up or down, or replacing the subterm, then takes $O(1)$ time plus the arity of the node, in a purely functional way. This is Huet's zipper.

**Non-examples.**

- $f(\square, \square)$ is not a one-hole context; it is a multihole context with two holes.
- $g(x)$ is not a context, since it has no hole; a multihole context with zero holes is just a term.
- Filling a hole is not substitution: $f(x, \square)[y]$ is $f(x, y)$, and only the hole is replaced, never a variable. In the [lambda calculus](/lambda-calculus/), filling a context can capture a free variable of the filler, so there a context is not the same as a substitution even up to renaming.

## Related definitions

- [Subterm](/subterm/): the term that fills the hole, $t|_p$ for $t = C[t|_p]$.
- [Rewrite step](/rewrite-step/): $C[l\sigma] \to C[r\sigma]$.
- [Parallel rewriting](/parallel-rewriting/): steps in a multihole context.
- [Reduction ordering](/well-founded-reduction-ordering/): an order closed under contexts.
- [Equational theory](/equational-theory/) and [congruence closure](/congruence-closure/): equivalences closed under contexts.
- [Critical pair lemma](/critical-pair-lemma/): its proof splits two steps $C[l_1\sigma_1]$ and $D[l_2\sigma_2]$ by the relative position of their holes.

## References
