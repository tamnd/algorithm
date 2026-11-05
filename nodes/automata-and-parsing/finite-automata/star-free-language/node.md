---
tag: FCCC24
kind: definition
slug: star-free-language
name: Star-free language
aliases:
- aperiodic language
- counter-free language
area: automata-and-parsing/finite-automata
level: advanced
summary: Regular language definable without the Kleene star, using only union, concatenation and complement.
prereqs: [regular-language, kleene-star]
see_also: [schutzenberger-theorem, syntactic-monoid, star-free-expressions, linear-temporal-logic, krohn-rhodes-theorem, regular-expression, pumping-lemma-for-regular-languages, cyclic-group]
sources:
  - paper: "Marcel-Paul Schützenberger, On finite monoids having only trivial subgroups, Information and Control 8(2) (1965)"
    locator: pp. 190 to 194 (star-free languages are exactly the languages with an aperiodic syntactic monoid)
  - book: "Robert McNaughton and Seymour Papert, Counter-Free Automata, MIT Press, 1971"
    locator: the chapters on counter-free automata, star-free sets and first-order definable sets
  - paper: "Sang Cho and Dung T. Huynh, Finite-automaton aperiodicity is PSPACE-complete, Theoretical Computer Science 88(1) (1991)"
    locator: pp. 99 to 116 (deciding whether the language of a DFA is star-free is PSPACE-complete)
  - paper: "Rina S. Cohen and Janusz A. Brzozowski, Dot-depth of star-free events, Journal of Computer and System Sciences 5(1) (1971)"
    locator: pp. 1 to 16 (the dot-depth hierarchy of star-free languages)
---

A star-free language is a language that can be built from the empty set and the single letters with union, concatenation and complement, without the [Kleene star](/kleene-star/). Complement makes up for the missing star in many cases: $\Sigma^*$ is the complement of $\emptyset$, and $(ab)^*$ is star-free. Every star-free language is [regular](/regular-language/), but not every regular language is star-free: $(aa)^*$ is not. [Schützenberger's theorem](/schutzenberger-theorem/) gives a test: a regular language is star-free if and only if its [syntactic monoid](/syntactic-monoid/) is aperiodic, that is, contains no non-trivial group.

## Definition

Let $\Sigma$ be a finite alphabet. The class $\mathrm{SF}(\Sigma)$ of *star-free languages* over $\Sigma$ is the smallest class of languages $L \subseteq \Sigma^*$ such that

1. $\emptyset$ and $\{a\}$, for each $a \in \Sigma$, are in $\mathrm{SF}(\Sigma)$;
2. if $K, L \in \mathrm{SF}(\Sigma)$, then $K \cup L$, $KL = \{ uv : u \in K, v \in L \}$ and $\overline{L} = \Sigma^* \setminus L$ are in $\mathrm{SF}(\Sigma)$.

An expression built from $\emptyset$, letters, $\cup$, concatenation and complement is a [star-free expression](/star-free-expressions/). By De Morgan's laws, $\mathrm{SF}(\Sigma)$ is closed under intersection and difference. The complement is taken with respect to $\Sigma^*$, so the class depends on the alphabet: a language over $\Sigma$ that is star-free over a larger alphabet $\Gamma$ is star-free over $\Sigma$ too, but the expressions differ.

Useful star-free languages:

- $\Sigma^* = \overline{\emptyset}$, and $\{\varepsilon\} = \overline{\bigcup_{a \in \Sigma} \{a\} \Sigma^*}$.
- $\Sigma^* w \Sigma^*$, the strings that contain $w$ as a factor, and $w \Sigma^*$, $\Sigma^* w$.
- $B^*$ for $B \subseteq \Sigma$, which is $\overline{\Sigma^* (\Sigma \setminus B) \Sigma^*}$, a union over the letters of $\Sigma \setminus B$.

**Equivalent definitions.** For a regular language $L$ with minimal complete DFA $(Q, \Sigma, \delta, q_0, F)$, without $\varepsilon$-moves, the following are equivalent:

1. $L$ is star-free.
2. The syntactic monoid $M(L)$ is *aperiodic*: there is $k$ with $m^k = m^{k + 1}$ for all $m \in M(L)$ (Schützenberger, 1965).
3. There is $k$ such that for all strings $x, u, y$: $x u^k y \in L$ if and only if $x u^{k + 1} y \in L$.
4. The minimal DFA is *counter-free*: no string $u$ and states $p_0, \ldots, p_{j - 1}$, all different with $j \ge 2$, satisfy $\delta^*(p_i, u) = p_{i + 1 \bmod j}$ for all $i$ (McNaughton and Papert, 1971).
5. $L$ is defined by a sentence of first-order logic over the positions of the string, with the order $<$ and a predicate for each letter (McNaughton and Papert, 1971).
6. $L$ is defined by a formula of [linear temporal logic](/linear-temporal-logic/) on finite strings (Kamp, 1968).

The equivalence of 1 and 2 is Schützenberger's theorem, with a full proof on its page. Items 2 and 3 are the same statement, written in the monoid and in the strings. Items 2 and 4 are the same statement for the transition monoid of the minimal DFA, since a map $f : Q \to Q$ satisfies $f^k = f^{k + 1}$ for some $k$ if and only if it has no cycle of length at least 2.

**Deciding star-freeness.** Given a DFA, test whether its minimal DFA is counter-free. The problem is PSPACE-complete (Cho and Huynh, 1991): the syntactic monoid can have exponentially many elements, so one cannot list it in general.

## Examples and non-examples

- **Finite and cofinite languages.** A single string is a concatenation of letters, a finite language is a finite union of strings, and a cofinite language is the complement of a finite one.
- **$(ab)^*$ over $\{a, b\}$.** A string is in $(ab)^*$ if and only if it does not start with $b$, does not end with $a$, and contains neither $aa$ nor $bb$. So
  $$(ab)^* = \overline{b \Sigma^* \cup \Sigma^* a \cup \Sigma^* aa \Sigma^* \cup \Sigma^* bb \Sigma^*}.$$
  If a non-empty string satisfies the four conditions, its letters alternate, it starts with $a$ and ends with $b$, so it is $(ab)^k$; the empty string satisfies them too. Its syntactic monoid has six elements and is aperiodic.
- **$a^*$ over $\{a, b\}$** is star-free, as $\overline{\Sigma^* b \Sigma^*}$. Over $\{a\}$ alone, $a^* = \overline{\emptyset}$.
- **Non-example: $(aa)^*$.** For every $k$, take $x = y = \varepsilon$ and $u = a$: exactly one of $a^k$ and $a^{k + 1}$ has even length, so condition 3 fails. The syntactic monoid is the [cyclic group](/cyclic-group/) of order 2. The same argument shows that "the number of $a$s is divisible by $p$" is not star-free for any $p \ge 2$, over any alphabet that contains $a$.
- **Non-example: $(aa)^* b$.** The language $(aa)^* b$ over $\{a, b\}$ is not star-free: $a^k b$ and $a^{k + 1} b$ differ in membership for every $k$.
- **Unary alphabets.** Over $\{a\}$, a language is star-free if and only if it is finite or cofinite. If condition 3 holds with $k$, then all $a^j$ with $j \ge k$ are in $L$ or all are outside, so $L$ is finite or cofinite; the converse is the first example.

## Related definitions

- [Star-free expressions](/star-free-expressions/) are the expressions of the definition, studied as a form of [regular expression](/regular-expression/).
- **Aperiodic monoid.** A finite monoid with $m^k = m^{k + 1}$ for some $k$ and all $m$; equivalently, every subgroup is trivial. See [syntactic monoid](/syntactic-monoid/).
- **Counter-free automaton.** A DFA as in condition 4. A DFA that is not minimal can have a counter even when its language is star-free, for example a cycle of two accepting states for $a^*$ over $\{a\}$; the test applies to the minimal DFA.
- **Dot-depth.** Star-free languages are graded by the number of alternations of concatenation and Boolean operations needed; this dot-depth hierarchy is infinite (Cohen and Brzozowski, 1971, defined it; Brzozowski and Knast, 1978, proved it strict).
- **Generalized star height.** With complement allowed, the star height of $L$ is the least nesting of stars in an expression for $L$. The star-free languages are those of generalized star height 0. Whether some regular language has generalized star height 2 or more is an open problem.
- **Piecewise testable and locally testable languages** are subclasses of the star-free languages, also characterized by their syntactic monoids.
- The [Krohn-Rhodes theorem](/krohn-rhodes-theorem/) implies that the transition monoids of counter-free automata are exactly the monoids that divide cascades of two-state reset automata.

## References
