---
tag: BE4V9Z
kind: definition
slug: well-founded-reduction-ordering
name: Reduction ordering
aliases:
- simplification ordering
- monotone well-founded ordering
area: automata-and-parsing/term-rewriting
level: advanced
summary: A well-founded ordering closed under contexts and substitutions, used to prove termination.
prereqs: [termination, well-founded-relation, term-context, substitution]
see_also: [lexicographic-path-ordering, recursive-path-ordering, knuth-bendix-ordering, polynomial-interpretation, matrix-interpretation, multiset-ordering, dependency-pairs, knuth-bendix-completion]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 5.2, Reduction orders (p. 101 onwards); Section 5.4, Simplification orders (p. 111 onwards)
  - paper: doi:10.1016/0304-3975(82)90026-3
    title: Nachum Dershowitz, Orderings for term-rewriting systems, Theoretical Computer Science 17(3) (1982)
    locator: pp. 279 to 301 (simplification orderings are well-founded, the recursive path ordering)
  - paper: doi:10.1090/S0002-9947-1960-0111704-1
    title: Joseph B. Kruskal, Well-quasi-ordering, the tree theorem, and Vazsonyi's conjecture, Transactions of the American Mathematical Society 95(2) (1960)
    locator: pp. 210 to 225 (the tree theorem)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 6, Termination (reduction orders, simplification orders and Kruskal's theorem)
---

A **reduction ordering** is a well-founded strict order on terms that is closed under contexts and under substitutions. If it puts the left side of each rule above the right side, then every [rewrite step](/rewrite-step/) goes down in the order, so the system is [terminating](/termination/); conversely every terminating system has such an order. A **simplification ordering** also puts each term above its proper subterms; by Kruskal's tree theorem it is then well-founded for free, which is why the [path orderings](/recursive-path-ordering/) and the [Knuth-Bendix ordering](/knuth-bendix-ordering/) need no separate proof of well-foundedness.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions with root $\varepsilon$, contexts $C[\,]$, substitutions $\sigma$ applied as $t\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure.

A strict order $>$ on $T(\Sigma, V)$ (irreflexive and transitive) is

- **closed under contexts** (monotone) if $s > t$ implies $C[s] > C[t]$ for every [context](/term-context/) $C$; it suffices to check $f(\ldots, s, \ldots) > f(\ldots, t, \ldots)$ for each symbol and argument place;
- **closed under substitutions** (stable) if $s > t$ implies $s\sigma > t\sigma$ for every [substitution](/substitution/) $\sigma$;
- a **rewrite ordering** if it has both properties;
- a **reduction ordering** if it is a [well-founded](/well-founded-relation/) rewrite ordering;
- a **simplification ordering** if it is a rewrite ordering with the **subterm property** $f(t_1, \ldots, t_n) > t_i$ for all $f$ and $i$.

A system $R$ is **compatible** with $>$ if $l > r$ for every rule $l \to r \in R$. Then $s \to_R t$ implies $s > t$, and $R$ terminates when $>$ is a reduction ordering; the converse, with $>$ taken as $\to_R^+$, is on the [termination](/termination/) page. Since a finite system needs only finitely many comparisons $l > r$, this turns termination into a check of finitely many pairs, once the order is fixed.

**Variables on the right.** If $l > r$ in a reduction ordering, then $\mathrm{Var}(r) \subseteq \mathrm{Var}(l)$. *Proof.* Let $x$ occur in $r$ at position $p$ but not in $l$, and let $\sigma = \{x \mapsto l\}$. Then $l\sigma = l$, and $r\sigma = C[l]$ for the context $C = (r\sigma)[\square]_p$. Stability gives $l > C[l]$, and monotonicity applied again and again gives $l > C[l] > C[C[l]] > \cdots$, an infinite descending chain. $\blacksquare$ So rules with extra variables on the right side never terminate, which is one reason [rewrite rules](/rewrite-rule/) forbid them.

**No total order on open terms.** A rewrite ordering cannot compare two distinct variables: if $x > y$, the substitution that swaps $x$ and $y$ gives $y > x$, and transitivity gives $x > x$. Likewise it cannot compare $f(x, y)$ with $f(y, x)$. A reduction ordering can be total on ground terms, which [unfailing completion](/unfailing-completion/) uses.

**Simplification orderings are well-founded.** For a finite signature, every simplification ordering $>$ is well-founded. *Proof sketch.* A simplification ordering contains the **homeomorphic embedding** $\trianglerighteq_{\mathrm{emb}}$: $s$ embeds $t$ if $t$ arises from $s$ by deleting nodes, each deleted node replaced by one of its subterms. This follows from the subterm property and monotonicity, by induction on $s$. Suppose $t_1 > t_2 > \cdots$ is infinite. Each $t_j$ has only variables of $t_1$: if $x$ occurs in $t_j$ but not in $t_1$, then $\sigma = \{x \mapsto t_1\}$ gives $t_1 = t_1\sigma > t_j\sigma$, and $t_j\sigma$ contains $t_1$, so $t_j\sigma \ge t_1$ by the subterm property, a contradiction. So all terms lie in $T(\Sigma, X)$ for a finite $X$. Kruskal's tree theorem says that the embedding is a well-quasi-order on $T(\Sigma, X)$ when $\Sigma \cup X$ is finite, so $t_i \trianglelefteq_{\mathrm{emb}} t_j$ for some $i < j$. Then $t_j \ge t_i$, which contradicts $t_i > t_j$ and irreflexivity. $\blacksquare$ Dershowitz (1982) proved this result and built the recursive path ordering on it.

**Weaker notions used by modern tools.** A **reduction pair** $(\gtrsim, >)$ consists of a stable and monotone quasi-order $\gtrsim$ and a stable well-founded order $>$ that need not be monotone, with $\gtrsim \cdot > \subseteq >$. The [dependency pair](/dependency-pairs/) framework proves termination with reduction pairs, and so handles systems that no simplification ordering orients.

## Examples and non-examples

**A size order.** Let $s > t$ iff $|s| > |t|$ and each variable occurs in $s$ at least as often as in $t$. This is a reduction ordering. It is well-founded since sizes are natural numbers. It is closed under contexts since a context adds the same size to both sides and keeps the variable counts. It is closed under substitutions since $|s\sigma| = |s| + \sum_x |s|_x (|x\sigma| - 1)$, where $|s|_x$ is the number of occurrences of $x$, and $|s|_x \ge |t|_x$ for each $x$. It orients $f(x, a) \to x$ and $g(g(x)) \to g(x)$.

**The variable condition is needed.** Drop the variable counts and compare sizes only: $s = h(x, a, a)$ has size 4 and $t = g(x, x)$ has size 3. With $\sigma = \{x \mapsto g(g(a))\}$, $|s\sigma| = 6$ and $|t\sigma| = 7$, so the order is not stable.

**Orders from interpretations.** Map each symbol to a function on natural numbers that is strictly increasing in each argument, and let $s > t$ iff the value of $s$ is greater than the value of $t$ for every assignment to the variables. This is a reduction ordering: monotone because the functions are increasing, stable because the comparison covers all assignments, well-founded because the values are natural numbers. [Polynomial interpretations](/polynomial-interpretation/) and [matrix interpretations](/matrix-interpretation/) are of this kind. They are not simplification orders in general unless each function is at least as large as its arguments.

**Path orders and the Knuth-Bendix order.** The [recursive path ordering](/recursive-path-ordering/), the [lexicographic path ordering](/lexicographic-path-ordering/) and the [Knuth-Bendix ordering](/knuth-bendix-ordering/) are simplification orderings for finite signatures. With a total precedence, the lexicographic path ordering and the Knuth-Bendix ordering are total on ground terms.

**Non-examples.**

- The proper subterm order, $s > t$ iff $t$ is a proper subterm of $s$, is well-founded and stable but not monotone: $g(a) > a$, but $f(a)$ is not a subterm of $f(g(a))$. So it is not a reduction ordering.
- The strict order "$|s| > |t|$" is monotone and well-founded but not stable, as shown above.
- A rewrite ordering that orients $f(f(x)) \to f(g(f(x)))$ exists, since this system terminates, but no simplification ordering does: $f(f(x))$ embeds in $f(g(f(x)))$, so a simplification ordering gives $f(g(f(x))) \ge f(f(x))$. See [termination](/termination/).
- The lexicographic order on the pre-order strings of terms is a strict total order on ground terms, but it is not well-founded when a unary symbol is smaller than a constant: with $f < a$, $a > f(a) > f(f(a)) > \cdots$.

## Related definitions

- [Termination](/termination/): what a compatible reduction ordering proves.
- [Multiset ordering](/multiset-ordering/): lifts a well-founded order to multisets; used inside the recursive path ordering.
- [Lexicographic path ordering](/lexicographic-path-ordering/), [recursive path ordering](/recursive-path-ordering/) and [Knuth-Bendix ordering](/knuth-bendix-ordering/): the standard simplification orderings.
- [Polynomial interpretation](/polynomial-interpretation/) and [matrix interpretation](/matrix-interpretation/): reduction orderings from monotone algebras.
- [Dependency pairs](/dependency-pairs/): replace reduction orderings by reduction pairs.
- [Knuth-Bendix completion](/knuth-bendix-completion/): orients each new equation with a fixed reduction ordering.

## References
