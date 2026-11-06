---
tag: V9YQ4E
kind: definition
slug: string-rewriting-system
name: String rewriting system
aliases:
- semi-Thue system
- Thue system
- string rewriting
area: automata-and-parsing/term-rewriting
level: core
summary: A rewriting system over strings, where rules replace one substring by another.
prereqs: [term-rewriting-system, monoid]
see_also: [undecidability-of-word-problem, word-problem, post-canonical-system, markov-algorithm, knuth-bendix-completion, critical-pair, word-problem-for-groups, context-free-grammar]
sources:
  - book: isbn:9780387979656
    title: Ronald V. Book and Friedrich Otto, String-Rewriting Systems, Springer, 1993
    locator: the chapters String-rewriting systems (definitions, Thue congruences, confluence and completion) and Length as the basis for reduction (linear-time normal forms)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 3, Examples of TRSs and special rewriting formats (string rewriting systems)
  - paper: doi:10.1016/0304-3975(85)90023-4
    title: Deepak Kapur and Paliath Narendran, A finite Thue system with decidable word problem and without equivalent finite canonical system, Theoretical Computer Science 35(2-3) (1985)
    locator: pp. 337 to 344
  - paper: doi:10.1016/0022-4049(87)90129-0
    title: Craig C. Squier, Word problems and a homological finiteness condition for monoids, Journal of Pure and Applied Algebra 49(1-2) (1987)
    locator: pp. 201 to 217
---

A **string rewriting system** (semi-Thue system) is a set of rules $u \to v$ between words over an alphabet. A word $xuy$ rewrites in one step to $xvy$: some factor equal to a left side is replaced by the right side. Read in both directions, the rules generate a congruence on words, and the quotient is the [monoid](/monoid/) that the rules present. String rewriting is the special case of [term rewriting](/term-rewriting-system/) with only unary symbols; it is where the undecidability of the [word problem](/undecidability-of-word-problem/) was first proved, and it is the basis of [Knuth-Bendix completion](/knuth-bendix-completion/) for monoids and groups.

## Definition

We use the notation of the term rewriting pages where it applies: rules $l \to r$, $\to_R$ for one step and $\to_R^*$ for its reflexive transitive closure. Words are written by juxtaposition, and $\varepsilon$ is the empty word.

Let $\Sigma$ be a finite alphabet. A **string rewriting system** over $\Sigma$ is a set $R \subseteq \Sigma^* \times \Sigma^*$ of rules $u \to v$. On these pages we require $u \ne \varepsilon$. The **one-step relation** is

$$w \to_R w' \iff w = xuy \text{ and } w' = xvy \text{ for some } x, y \in \Sigma^* \text{ and } (u \to v) \in R.$$

The **Thue congruence** $\leftrightarrow_R^*$ is the reflexive, symmetric and transitive closure. It is a congruence on the free monoid $\Sigma^*$: $w_1 \leftrightarrow_R^* w_2$ implies $x w_1 y \leftrightarrow_R^* x w_2 y$. The monoid $M_R = \Sigma^* / {\leftrightarrow_R^*}$ is the monoid **presented** by $\langle \Sigma \mid R \rangle$. A **Thue system** is a string rewriting system used in both directions, that is, a set of equations $u \approx v$.

All notions of an [abstract reduction system](/abstract-reduction-system/) apply: $R$ is **terminating**, **confluent**, or **convergent** (both); $R$ is **length-reducing** if $|u| > |v|$ for each rule, **monadic** if moreover $|v| \le 1$, and **special** if $v = \varepsilon$ for each rule.

**As a term rewriting system.** Map each letter $a$ to a unary function symbol, and a word $w = a_1 \cdots a_n$ to the term $\varphi(w) = a_1(a_2(\cdots a_n(z) \cdots))$ with a variable $z$. A rule $u \to v$ becomes the term rule $\varphi(u) \to \varphi(v)$ in the variable $z$; the condition $u \ne \varepsilon$ is exactly the condition that the left side is not a variable. Every term over unary symbols is $\varphi(w)$ with $z$ renamed, and a term step at the position after the prefix $x$ is exactly the string step at the factor $u$ that starts after $x$. So $w \to_R w'$ iff $\varphi(w) \to \varphi(w')$, and $R$ is terminating, or confluent, iff the term system is.

**Critical pairs.** Two left sides $u_1, u_2$ overlap in two ways: a proper suffix of $u_1$ is a proper prefix of $u_2$ ($u_1 = xy$, $u_2 = yz$ with $x, y, z \ne \varepsilon$), which gives the word $xyz$ and the [critical pair](/critical-pair/) $\langle v_1 z, x v_2 \rangle$; or $u_2$ is a factor of $u_1$ ($u_1 = x u_2 y$), which gives $\langle v_1, x v_2 y \rangle$. A finite system has finitely many critical pairs. A terminating system is confluent iff all its critical pairs are joinable, so confluence is decidable for finite terminating systems.

**Decision problems.** For finite systems the word problem ($w \leftrightarrow_R^* w'$?) is undecidable in general (Post and Markov, 1947); see [undecidability of the word problem](/undecidability-of-word-problem/). Termination and confluence are undecidable for finite systems as well. Whether termination is decidable for systems with a single rule is an open problem. For a finite convergent system, $w \leftrightarrow_R^* w'$ iff the two normal forms are equal, and for a finite length-reducing confluent system the normal form of a word can be computed in linear time with a stack (Book and Otto, the chapter on length as the basis for reduction).

## Examples and non-examples

**Sorting letters.** $R = \{ba \to ab\}$ over $\{a, b\}$ is convergent. Each step removes one pair of positions with $b$ before $a$, so each reduction of $b^n a^n$ to its normal form $a^n b^n$ has exactly $n^2$ steps: 1, 4, 9, 16, 25 for $n = 1$ to 5. The normal forms are the words $a^i b^j$, and $R$ presents the free commutative monoid $\mathbb{N}^2$.

**The symmetric group $S_3$.** The group $\langle a, b \mid a^2 = b^2 = (ab)^3 = 1 \rangle$ is $S_3$, with $a$ and $b$ two transpositions. Completion with the shortlex order ($a < b$, shorter words first) turns $\{aa \to \varepsilon,\ bb \to \varepsilon,\ ababab \to \varepsilon\}$ into the convergent system

$$aa \to \varepsilon, \qquad bb \to \varepsilon, \qquad bab \to aba.$$

Its normal forms are $\varepsilon, a, b, ab, ba, aba$: six words for the six elements. For example, the overlap of $bb$ and $bab$ on the word $bbab$ gives the critical pair $\langle ab, baba \rangle$, and $baba \to abaa \to ab$ joins it.

**Free group of rank 1.** $\{aA \to \varepsilon,\ Aa \to \varepsilon\}$ is convergent and special; its normal forms $a^n$ and $A^n$ correspond to the integers, and it presents the group $\mathbb{Z}$.

**A monoid with no finite convergent system on its generators.** Kapur and Narendran (1985) showed that the monoid $\langle a, b \mid aba = bab \rangle$ has a decidable word problem but no finite convergent string rewriting system over $\{a, b\}$ that presents it. With a new letter $c$ for $ab$ such a system exists. Squier (1987) proved that a monoid with a finite convergent presentation satisfies the homological condition FP3, and used it to give finitely presented monoids with decidable word problem that have no finite convergent presentation over any finite alphabet.

**Grammars.** A Chomsky type-0 grammar is a string rewriting system with a start symbol and a set of terminal letters; its language is the set of terminal words $w$ with $S \to^* w$. A [context-free grammar](/context-free-grammar/) is the case where each left side is one nonterminal.

**Non-examples.**

- $\{ab \to bab\}$ is a string rewriting system, but not a terminating one: $ab \to bab \to bbab \to \cdots$, since each result contains $ab$ again.
- A system whose rules apply only at the start of a word, $uy \to vy$, is a prefix rewriting system, not a string rewriting system; its reachability sets are regular, which is false for string rewriting in general.
- A [Markov algorithm](/markov-algorithm/) is not a string rewriting system: it orders its rules, applies the first that matches at its leftmost place, and has stop rules.

## Related definitions

- [Term rewriting system](/term-rewriting-system/): the general case with symbols of any arity.
- [Word problem](/word-problem/) and [undecidability of the word problem](/undecidability-of-word-problem/): equality in the presented monoid.
- [Post canonical system](/post-canonical-system/): a more general string production system with variables.
- [Word problem for groups](/word-problem-for-groups/): the same question for group presentations.
- [Knuth-Bendix completion](/knuth-bendix-completion/): turns a presentation into a convergent system when it can.
- [Monoid](/monoid/): the structure that a Thue system presents.

## References
