---
tag: CN34A8
kind: definition
slug: subterm
name: Subterm
aliases:
- position
area: automata-and-parsing/term-rewriting
level: intro
summary: A term occurring at a position inside another term.
prereqs: [term]
see_also: [term-context, rewrite-step, substitution, well-founded-reduction-ordering, tree-pattern-matching, knuth-morris-pratt]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 3.1, Terms, substitutions, and identities (positions, subterms and replacement)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 2, First-order term rewriting systems (positions and subterms)
  - book: isbn:9780444880741
    title: Nachum Dershowitz and Jean-Pierre Jouannaud, Rewrite Systems, in J. van Leeuwen (editor), Handbook of Theoretical Computer Science, Volume B, Elsevier, 1990
    locator: pp. 243 to 320, Section 2 (positions, subterms and the subterm ordering)
---

A **subterm** of a [term](/term/) $t$ is the term $t|_p$ found at a **position** $p$ of $t$, that is, the subtree rooted at the node that the path $p$ reaches. Positions say where a [rewrite step](/rewrite-step/) happens, and the subterm relation is the base of the termination orders of rewriting, which all contain it. A subterm is a whole subtree, not any connected piece of the tree.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers with root $\varepsilon$, substitutions $\sigma$ applied as $t\sigma$.

The **positions** of a term are $\mathrm{Pos}(x) = \{\varepsilon\}$ for $x \in V$ and $\mathrm{Pos}(f(t_1, \ldots, t_n)) = \{\varepsilon\} \cup \{ ip \mid 1 \le i \le n,\ p \in \mathrm{Pos}(t_i) \}$. For $p \in \mathrm{Pos}(t)$, the **subterm** of $t$ at $p$ and the **replacement** of it by a term $s$ are

$$t|_\varepsilon = t, \quad f(t_1, \ldots, t_n)|_{ip} = t_i|_p; \qquad t[s]_\varepsilon = s, \quad f(t_1, \ldots, t_n)[s]_{ip} = f(t_1, \ldots, t_i[s]_p, \ldots, t_n).$$

$t(p)$ is the symbol or variable at the root of $t|_p$. A position is a **variable position** if $t|_p \in V$, and a **function position** otherwise.

The **subterm relation** is $t \trianglerighteq s$ iff $s = t|_p$ for some $p \in \mathrm{Pos}(t)$. $s$ is a **proper subterm** of $t$, written $t \triangleright s$, iff $t \trianglerighteq s$ and $t \ne s$, which holds iff $s = t|_p$ for some $p \ne \varepsilon$.

On positions, $p \le q$ ($p$ is **above** $q$) iff $q = pp'$ for some $p'$, $p < q$ iff moreover $p' \ne \varepsilon$, and $p \parallel q$ (**parallel**) iff neither $p \le q$ nor $q \le p$. Two positions are parallel exactly when they first differ at some index, for example $1.2 \parallel 2$.

**Basic facts.** For $p, q$ such that the positions exist:

1. $(t|_p)|_q = t|_{pq}$.
2. $(t[s]_p)|_p = s$, and $(t[s]_p)|_{pq} = s|_q$.
3. If $p \parallel q$, then $(t[s]_p)|_q = t|_q$, and $(t[s]_p)[u]_q = (t[u]_q)[s]_p$.
4. $(t[s]_p)[u]_p = t[u]_p$, and $t[t|_p]_p = t$.
5. For each substitution $\sigma$ and $p \in \mathrm{Pos}(t)$: $(t\sigma)|_p = (t|_p)\sigma$ and $(t[s]_p)\sigma = (t\sigma)[s\sigma]_p$.
6. $|t|_p| < |t|$ when $p \ne \varepsilon$. So $\triangleright$ is a well-founded strict order, and $\trianglerighteq$ is a partial order.

*Proof.* Items 1, 2 and 4 follow by induction on the length of $p$: for $p = \varepsilon$ they are the defining equations, and for $p = ip'$ both sides unfold into the $i$-th argument, where the hypothesis for $p'$ applies. For item 3, write $p = r i p'$ and $q = r j q'$ with $i \ne j$; replacing inside the $i$-th argument of $t|_r$ leaves its $j$-th argument unchanged, which gives the first equation, and the two replacements change different arguments, which gives the second. For item 5, $p \in \mathrm{Pos}(t)$ means that the path $p$ never passes through a variable of $t$, so $t\sigma$ has the same symbols as $t$ along $p$, and induction on $p$ applies as for item 1. For item 6, $|f(t_1, \ldots, t_n)| = 1 + \sum_i |t_i|$, so a proper subterm has fewer nodes; a strict order in which each step lowers a natural number has no infinite descending chain. Transitivity of $\trianglerighteq$ is item 1, and antisymmetry follows from item 6. $\blacksquare$

Item 5 needs $p \in \mathrm{Pos}(t)$: $t\sigma$ has more positions than $t$ when $\sigma$ maps a variable to a non-variable term, and those new positions are inside some $x\sigma$.

## Examples and non-examples

**Positions and subterms.** For $t = f(g(x), f(a, x))$:

| $p$ | $\varepsilon$ | 1 | 1.1 | 2 | 2.1 | 2.2 |
|---|---|---|---|---|---|---|
| $t(p)$ | $f$ | $g$ | $x$ | $f$ | $a$ | $x$ |

The term has 6 positions but 5 distinct subterms, because $x$ is at 1.1 and at 2.2. The variable positions are 1.1 and 2.2; the others are function positions. With $\sigma = \{x \mapsto g(a)\}$, $t\sigma = f(g(g(a)), f(a, g(a)))$ has 8 positions, and $(t\sigma)|_2 = f(a, g(a)) = (t|_2)\sigma$, as item 5 says.

**Replacement at parallel positions.** $t[b]_{1.1} = f(g(b), f(a, x))$ and $t[b]_{1.1}[c]_{2.1} = f(g(b), f(c, x)) = t[c]_{2.1}[b]_{1.1}$, since $1.1 \parallel 2.1$. At positions that are not parallel the order matters: $t[b]_2[c]_{2.1}$ fails, since $b$ has no position 2.1, while $t[c]_{2.1}[b]_2 = f(g(x), b)$.

**Testing for a subterm in linear time.** Write a term in prefix (Polish) form, one symbol per node: $t$ becomes the word $f\,g\,x\,f\,a\,x$. Since each symbol has a fixed arity, the subterm at a node is the unique well-formed prefix of the suffix that starts at that node. So $s$ is a subterm of $t$ iff the prefix form of $s$ is a factor of the prefix form of $t$. String matching with [Knuth-Morris-Pratt](/knuth-morris-pratt/) then decides $t \trianglerighteq s$ in $O(|s| + |t|)$ time, while comparing $s$ with the subterm at each position costs $O(|s| \cdot |t|)$ in the worst case.

**Non-examples.**

- $x + y$ is a subterm of $(x + y) + z$ but not of $x + (y + z)$, although the two terms are equal under associativity. The subterm relation is syntactic. [Rewriting modulo equations](/rewriting-modulo-equations/) uses subterms modulo the theory.
- $f(a)$ is not a subterm of $f(g(a))$: deleting the inner node $g$ is a homeomorphic *embedding*, not a subterm. Embedding is the larger relation used by Kruskal's tree theorem and by simplification orders.
- A position of $t\sigma$ inside some $x\sigma$, such as 1.1.1 in $f(g(g(a)), f(a, g(a)))$ above, is not a position of $t$. A rewrite step there is a step inside the substitution, which matters in the proof of the [critical pair lemma](/critical-pair-lemma/).

## Related definitions

- [Term](/term/): the trees whose positions are defined here.
- [Context](/term-context/): $t[\square]_p$, the term with the subterm at $p$ cut out, so that $t = t[t|_p]_p$.
- [Rewrite step](/rewrite-step/): $s \to t$ at position $p$ with $s|_p = l\sigma$ and $t = s[r\sigma]_p$.
- [Reduction ordering](/well-founded-reduction-ordering/): a simplification ordering contains $\triangleright$; this is the subterm property.
- [Tree pattern matching](/tree-pattern-matching/): find all positions $p$ where $t|_p$ is an instance of a pattern.
- [Parallel rewriting](/parallel-rewriting/): contract redexes at pairwise parallel positions in one step.

## References
