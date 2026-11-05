---
tag: D61K9B
kind: concept
slug: syntactic-monoid
name: Syntactic monoid
aliases:
- syntactic semigroup
- Myhill monoid
- syntactic congruence
area: automata-and-parsing/finite-automata
level: advanced
summary: Finite monoid of transformations induced by a language's Myhill-Nerode classes; it characterizes regularity.
prereqs: [monoid, myhill-nerode-theorem, deterministic-finite-automaton]
see_also: [schutzenberger-theorem, star-free-language, krohn-rhodes-theorem, myhill-nerode-relation, congruence, dfa-minimization, finite-group, regular-language]
sources:
  - paper: "Marcel-Paul Schützenberger, On finite monoids having only trivial subgroups, Information and Control 8(2) (1965)"
    locator: pp. 190 to 194 (the syntactic monoid of a star-free language is aperiodic, and the converse)
  - paper: "Imre Simon, Piecewise testable events, Automata Theory and Formal Languages, 2nd GI Conference, Lecture Notes in Computer Science 33 (1975)"
    locator: pp. 214 to 222 (a language is piecewise testable if and only if its syntactic monoid is J-trivial)
  - book: "Samuel Eilenberg, Automata, Languages, and Machines, Volume B, Academic Press, 1976"
    locator: Chapter VII, on varieties of finite monoids and the correspondence with varieties of languages
  - book: "Robert McNaughton and Seymour Papert, Counter-Free Automata, MIT Press, 1971"
    locator: the chapters on counter-free automata and the equivalence with star-free sets and first-order logic
---

The syntactic monoid of a language $L \subseteq \Sigma^*$ is the set of classes of the *syntactic congruence*, which puts two strings $u$ and $v$ in one class when no context tells them apart: $xuy \in L$ if and only if $xvy \in L$, for all strings $x$ and $y$. The classes multiply by concatenation. The syntactic monoid is finite exactly when $L$ is [regular](/regular-language/), it is the transition monoid of the minimal [DFA](/deterministic-finite-automaton/) of $L$, and it is the smallest monoid that recognizes $L$. Algebraic properties of the monoid classify languages: it has no non-trivial groups exactly when $L$ is [star-free](/star-free-language/) ([Schützenberger's theorem](/schutzenberger-theorem/)).

## In plain words

Two pieces of text behave the same in a language if you can always swap one for the other, anywhere in a string, without changing whether the string is in the language. Grouping pieces that behave the same gives a small set of "kinds" of text. Gluing two pieces together gives a piece whose kind depends only on the kinds of the parts, so the kinds have a multiplication table.

This table is the syntactic monoid. It is finite exactly when a finite machine can recognize the language, and you can read it from the smallest such machine: each kind is the effect of a piece of text on the states of the machine. The table tells you much about the language. For example, if no kind repeats in a cycle, the language has a description without repetition loops.

## The idea

**Notation.** $\Sigma$ is a finite alphabet. A DFA is $D = (Q, \Sigma, \delta, q_0, F)$, complete, without $\varepsilon$-moves, and $\delta^*(q, u)$ is the state after reading $u$ from $q$. A [monoid](/monoid/) is a set with an associative product and an identity $1$; a *morphism* $\varphi : \Sigma^* \to M$ satisfies $\varphi(uv) = \varphi(u) \varphi(v)$ and $\varphi(\varepsilon) = 1$, and it is fixed by the values $\varphi(a)$ on letters.

**Syntactic congruence.** For $L \subseteq \Sigma^*$ define

$$u \equiv_L v \iff \text{for all } x, y \in \Sigma^* : \ xuy \in L \Leftrightarrow xvy \in L.$$

This is an equivalence relation, and a [congruence](/congruence/): if $u \equiv_L v$ then $xuy \equiv_L xvy$. So the classes form a monoid $M(L) = \Sigma^* / {\equiv_L}$ with $[u][v] = [uv]$ and identity $[\varepsilon]$, the *syntactic monoid*, and $\eta_L : u \mapsto [u]$ is the *syntactic morphism*. Taking $x = y = \varepsilon$ shows that $L$ is a union of classes: $L = \eta_L^{-1}(\eta_L(L))$. The syntactic congruence is finer than the [Myhill-Nerode relation](/myhill-nerode-relation/), which uses only contexts on the right ($x = \varepsilon$).

**Recognition.** A monoid $M$ *recognizes* $L$ if $L = \varphi^{-1}(P)$ for a morphism $\varphi : \Sigma^* \to M$ and a subset $P \subseteq M$. If $\varphi$ is onto and recognizes $L$, then $M(L)$ is a quotient of $M$: the map $\psi(\varphi(u)) = \eta_L(u)$ is a well-defined onto morphism. *Proof.* If $\varphi(u) = \varphi(v)$, then $\varphi(xuy) = \varphi(xvy)$ for all $x, y$, so $xuy$ and $xvy$ are both in $L = \varphi^{-1}(P)$ or both outside it, and $u \equiv_L v$. $\square$ So $M(L)$ is the smallest monoid that recognizes $L$, in a strong sense: it is the image of every monoid that recognizes $L$ by an onto morphism.

**Transition monoid.** Each string $u$ acts on the states of $D$ by the map $\delta_u : q \mapsto \delta^*(q, u)$, and $\delta_{uv}$ is $\delta_u$ followed by $\delta_v$. The set $T(D) = \{ \delta_u : u \in \Sigma^* \}$, with this composition, is the *transition monoid* of $D$. It recognizes $L(D)$, with $P = \{ f : f(q_0) \in F \}$, and it has at most $|Q|^{|Q|}$ elements.

**Theorem.** If $D$ is the minimal complete DFA of $L$, then $\delta_u = \delta_v$ if and only if $u \equiv_L v$, so $M(L)$ is isomorphic to $T(D)$.

*Proof.* If $\delta_u = \delta_v$ then $u \equiv_L v$, by the recognition argument above. Conversely, let $u \equiv_L v$ and let $q \in Q$. Every state of the minimal DFA is reachable, so $q = \delta^*(q_0, x)$ for some $x$. For every $y$, $\delta^*(\delta_u(q), y) \in F$ if and only if $xuy \in L$, if and only if $xvy \in L$, if and only if $\delta^*(\delta_v(q), y) \in F$. So $\delta_u(q)$ and $\delta_v(q)$ are not distinguishable, and in the minimal DFA they are equal. $\square$

**Consequences.**

- $L$ is regular if and only if $M(L)$ is finite. If $L$ is regular, $M(L) \cong T(D)$ is finite. If $M(L)$ is finite, the DFA with states $M(L)$, start $1$, moves $m \xrightarrow{a} m \, \eta_L(a)$ and accepting set $\eta_L(L)$ accepts $L$.
- If the minimal DFA has $n$ states, then $n \le |M(L)| \le n^n$. The upper bound is reached for $n \ge 2$ over three letters, by a DFA whose letters act as an $n$-cycle, a transposition of two states, and a map that merges two states; these maps generate all $n^n$ maps from $Q$ to $Q$.
- **Computing $M(L)$.** Start from the identity map, and search over the letters: from each map $f$ found, form $f$ followed by $\delta_a$ for each $a \in \Sigma$, and keep the new maps in a hash table. Each element is a tuple of $n$ states, so the search takes $O(|M(L)| \, \sigma \, n)$ time for $\sigma = |\Sigma|$, which can be exponential in $n$.

**Properties and classes of languages.** The following correspondences hold for regular $L$.

| property of $M(L)$ | class of languages | source |
|---|---|---|
| finite | [regular languages](/regular-language/) | the theorem above |
| a [finite group](/finite-group/) | every letter permutes the states of the minimal DFA | direct |
| commutative | membership depends only on the number of each letter | direct |
| aperiodic: $m^k = m^{k + 1}$ for some $k$ and all $m$ | [star-free languages](/star-free-language/), and the languages of first-order logic over $<$ | Schützenberger (1965); McNaughton and Papert (1971) |
| $\mathcal{J}$-trivial: $MsM = MtM$ implies $s = t$ | piecewise testable languages | Simon (1975) |

Eilenberg's variety theorem (1976) makes this systematic: classes of finite monoids closed under submonoids, quotients and finite direct products correspond one to one to classes of regular languages closed under Boolean operations, left and right quotients, and inverse morphisms. The [Krohn-Rhodes theorem](/krohn-rhodes-theorem/) decomposes the transition monoid of any automaton into groups and aperiodic pieces.

## Examples

**$(ab)^*$ over $\{a, b\}$.** The minimal DFA has three states: $0$ (start, accepting), $1$ (after an $a$), and a dead state. The transition monoid has six elements, named by shortest strings: $1, a, b, ab, ba$, and $0 = [aa]$, the class of all strings that contain $aa$ or $bb$. The product table, row times column:

| | $1$ | $a$ | $b$ | $ab$ | $ba$ | $0$ |
|---|---|---|---|---|---|---|
| $1$ | $1$ | $a$ | $b$ | $ab$ | $ba$ | $0$ |
| $a$ | $a$ | $0$ | $ab$ | $0$ | $a$ | $0$ |
| $b$ | $b$ | $ba$ | $0$ | $b$ | $0$ | $0$ |
| $ab$ | $ab$ | $a$ | $0$ | $ab$ | $0$ | $0$ |
| $ba$ | $ba$ | $0$ | $b$ | $0$ | $ba$ | $0$ |
| $0$ | $0$ | $0$ | $0$ | $0$ | $0$ | $0$ |

Every element satisfies $m^2 = m^3$: $1, ab, ba$ and $0$ are idempotent, and $a^2 = b^2 = 0$. So $M((ab)^*)$ is aperiodic, and $(ab)^*$ is star-free. The Myhill-Nerode relation has only three classes, the classes of $\varepsilon$, $a$ and $aa$, against six classes of $\equiv_L$. For example, $ab$ and $\varepsilon$ are in one Myhill-Nerode class, but not in one class of $\equiv_L$: with $x = a$ and $y = b$, the string $a \cdot ab \cdot b = aabb$ is not in $L$, while $a \cdot b = ab$ is.

**$(aa)^*$ over $\{a\}$.** The minimal DFA is a cycle of two states, and $M(L) = \{1, a\}$ with $a^2 = 1$, the [cyclic group](/cyclic-group/) of order 2. It is not aperiodic, since $a^k \ne a^{k + 1}$ for all $k$, so $(aa)^*$ is not star-free. Over $\{a, b\}$ the same language has the monoid $\{1, a, 0\}$ with $b \mapsto 0$, which still contains the group $\{1, a\}$.

**Full transformation monoid.** For the DFA with $n$ states $\{0, \ldots, n - 1\}$, letters $a : q \mapsto q + 1 \bmod n$, $b$ swapping $0$ and $1$, $c : n - 1 \mapsto 0$ (other states fixed), and $F = \{0\}$, the DFA is minimal and its transition monoid has $n^n$ elements: 4, 27 and 256 for $n = 2, 3, 4$.

## Where it is used

- **Deciding membership in a class.** To decide whether a regular language is star-free, piecewise testable, or definable in a fragment of logic, compute $M(L)$ from the minimal DFA and test an equation in the monoid.
- **Lower bounds.** Since $M(L)$ is a quotient of a submonoid of every monoid that recognizes $L$, its size and structure bound the size of any monoid or automaton model that recognizes $L$.
- **Logic and verification.** Through [Schützenberger's theorem](/schutzenberger-theorem/) and its logical form, the syntactic monoid decides whether a property of words is expressible in first-order logic or in [linear temporal logic](/linear-temporal-logic/).
- **Decomposition.** The [Krohn-Rhodes theorem](/krohn-rhodes-theorem/) applies to $M(L)$ to split an automaton into a cascade of simple pieces.

## References
