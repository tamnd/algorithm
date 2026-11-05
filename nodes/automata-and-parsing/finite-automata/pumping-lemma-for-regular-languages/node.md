---
tag: X9RQNE
kind: theorem
slug: pumping-lemma-for-regular-languages
name: Pumping lemma for regular languages
aliases:
- regular pumping lemma
area: automata-and-parsing/finite-automata
level: intro
summary: Every sufficiently long string in a regular language splits into xyz with xy^iz in the language for all i.
prereqs: [regular-language, deterministic-finite-automaton, pigeonhole-principle]
see_also: [myhill-nerode-theorem, dfa-emptiness, dfa-finiteness, closure-properties-of-regular-languages, context-free-language, dyck-language]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.4, Nonregular Languages (Theorem 1.70, the pumping lemma, and Examples 1.73 to 1.77)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.1, Proving Languages Not to Be Regular (Theorem 4.1, the pumping lemma), and Section 4.3, Decision Properties of Regular Languages
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 11, Limitations of Finite Automata, and Lecture 12, Using the Pumping Lemma (the lemma as a game with a demon)
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: pp. 114 to 125
  - paper: doi:10.1137/0210039
    title: Andrzej Ehrenfeucht, Rohit Parikh and Grzegorz Rozenberg, Pumping lemmas for regular sets, SIAM Journal on Computing 10(3) (1981)
    locator: pp. 536 to 541 (a pumping condition that characterizes the regular sets)
  - url: "https://en.wikipedia.org/wiki/Pumping_lemma_for_regular_languages"
    locator: lead (Rabin and Scott 1959, and the rediscovery by Bar-Hillel, Perles and Shamir 1961), and section Invalidity of the lemma converse
---

The pumping lemma for regular languages says that each long enough string of a [regular language](/regular-language/) has a short non-empty piece near its start that can be repeated any number of times, or deleted, and the result stays in the language. The bound "long enough" is the number of states of any [DFA](/deterministic-finite-automaton/) for the language. The lemma is the standard tool to prove that a language is not regular, and it also bounds the length of the strings that a test for emptiness or finiteness must try. Its converse is false.

## Statement

**Theorem (pumping lemma).** Let $L \subseteq \Sigma^*$ be regular. Then there is an integer $p \ge 1$ such that each $w \in L$ with $|w| \ge p$ can be written as $w = xyz$ with

1. $|xy| \le p$,
2. $|y| \ge 1$, and
3. $x y^i z \in L$ for each $i \ge 0$.

If a complete DFA $M = (Q, \Sigma, \delta, q_0, F)$ accepts $L$, then $p = |Q|$ works.

Here $y^0 = \varepsilon$, so $i = 0$ deletes $y$, and $i \ge 2$ repeats it. The least $p$ for which the conclusion holds is the *minimal pumping length* of $L$.

**General form.** The proof gives more: for each $w \in L$ and each split $w = u v s$ with $|v| \ge p$, the middle part can be written $v = xyz$ with $|xy| \le p$, $|y| \ge 1$, and $u x y^i z s \in L$ for each $i \ge 0$. The theorem is the case $u = \varepsilon$.

## In plain words

A finite automaton has a fixed number of states. When it reads a string that is longer than this number, it must visit some state twice. The letters that it reads between the two visits take it around a loop, back to the same state. It can go around this loop again and again, or skip it, and it still ends in the same place. So if the long string is accepted, all the strings made by repeating or removing that piece are accepted too.

To show that a language is not regular, find a long string in it for which every such repetition breaks the language.

## Proof

Let $M = (Q, \Sigma, \delta, q_0, F)$ be a complete DFA with $L(M) = L$, and let $p = |Q| \ge 1$. Take $w = a_1 a_2 \cdots a_n \in L$ with $n \ge p$, and let $r_0, r_1, \ldots, r_n$ be the run of $M$ on $w$: $r_0 = q_0$ and $r_t = \delta(r_{t-1}, a_t)$. Since $w \in L$, $r_n \in F$.

The $p + 1$ states $r_0, \ldots, r_p$ lie in a set of $p$ states, so by the [pigeonhole principle](/pigeonhole-principle/) there are indices $0 \le j < k \le p$ with $r_j = r_k$. Set $x = a_1 \cdots a_j$, $y = a_{j+1} \cdots a_k$ and $z = a_{k+1} \cdots a_n$. Then $|xy| = k \le p$ and $|y| = k - j \ge 1$.

Write $q = r_j$. By the definition of the run, $\delta^*(q_0, x) = q$, $\delta^*(q, y) = r_k = q$, and $\delta^*(q, z) = r_n$. By induction on $i$, $\delta^*(q_0, x y^i) = q$ for each $i \ge 0$: for $i = 0$ this is $\delta^*(q_0, x) = q$, and $\delta^*(q_0, x y^{i+1}) = \delta^*(\delta^*(q_0, x y^i), y) = \delta^*(q, y) = q$, by the rule $\delta^*(s, uv) = \delta^*(\delta^*(s, u), v)$ of the DFA page. So $\delta^*(q_0, x y^i z) = \delta^*(q, z) = r_n \in F$, and $x y^i z \in L$.

For the general form, apply the same argument to the states $r_{|u|}, \ldots, r_{|u| + p}$, which the run visits while it reads the first $p$ symbols of $v$. $\blacksquare$

## Consequences

### Proofs that a language is not regular

The lemma is used in the contrapositive: if for every $p \ge 1$ some $w \in L$ with $|w| \ge p$ has no split with properties 1 to 3, then $L$ is not regular.

- **$\{a^n b^n : n \ge 0\}$.** Given $p$, take $w = a^p b^p$. Since $|xy| \le p$, the part $y$ is $a^t$ with $t \ge 1$. Then $x y^0 z = a^{p-t} b^p$ is not in the language.
- **Equal numbers.** The strings over $\{a, b\}$ with as many $a$s as $b$s are not regular. The same $w = a^p b^p$ works. Another proof: if this language were regular, its intersection with the regular $a^* b^*$ would be regular by the [closure properties](/closure-properties-of-regular-languages/), but the intersection is $\{a^n b^n\}$.
- **Powers of two in unary.** $\{a^{2^k} : k \ge 0\}$ is not regular. Given $p$, take $w = a^{2^p}$. Then $1 \le |y| \le p < 2^p$, so $2^p < |x y^2 z| = 2^p + |y| < 2^{p+1}$, and $x y^2 z$ is not in the language.
- **Balanced parentheses.** The [Dyck language](/dyck-language/) is not regular: with $w = (^p )^p$, the part $y$ is $(^t$, and deleting it unbalances the string.

### Bounds for decision procedures

Let $M$ have $p$ states.

**Corollary 1 (emptiness).** $L(M) \ne \emptyset$ if and only if $M$ accepts a string of length less than $p$.

*Proof.* If $L(M) \ne \emptyset$, let $w$ be a shortest string of $L(M)$. If $|w| \ge p$, the lemma gives $w = xyz$ with $xz \in L(M)$ and $|xz| < |w|$, a contradiction. So $|w| < p$. The other direction is clear from the definition. $\square$

**Corollary 2 (finiteness).** $L(M)$ is infinite if and only if $M$ accepts a string $w$ with $p \le |w| < 2p$.

*Proof.* If such a $w$ exists, the lemma gives $x y^i z \in L(M)$ for each $i$, and these strings have the distinct lengths $|w| + (i - 1)|y|$, so $L(M)$ is infinite. Conversely, let $L(M)$ be infinite. Then it has strings of length at least $p$; let $w$ be a shortest one. Suppose $|w| \ge 2p$. The lemma gives $w = xyz$ with $1 \le |y| \le p$ and $xz \in L(M)$. Then $|xz| = |w| - |y| \ge 2p - p = p$ and $|xz| < |w|$, which contradicts the choice of $w$. So $p \le |w| < 2p$. $\square$

These corollaries show that emptiness and finiteness are decidable by trying finitely many strings. The graph searches of [DFA emptiness](/dfa-emptiness/) and [DFA finiteness](/dfa-finiteness/) decide the same questions in time linear in the size of $M$, instead of trying up to $|\Sigma|^{2p}$ strings.

## Tightness

**The bound $p = |Q|$ cannot be lowered in general.** For $p \ge 1$ let $L_p = \{ a^k : k \ge p - 1 \}$. Its smallest DFA has $p$ states, $0, 1, \ldots, p - 1$, with $k \to k + 1$ for $k < p - 1$, a loop on $p - 1$, and $F = \{p - 1\}$. The minimal pumping length of $L_p$ is exactly $p$: the string $a^{p-1}$ is in $L_p$, and deleting any non-empty $y$ from it gives a string that is too short, so no bound below $p$ works.

**The converse is false.** A language can satisfy the conclusion of the lemma and still not be regular. Let

$$L = \{ a^i b^j c^k : i = 0 \text{ or } j = k \}.$$

The conclusion holds with $p = 1$, taking $x = \varepsilon$ and $y$ equal to the first symbol of $w$. If $w = a^i b^j c^j$ with $i \ge 1$, then $y = a$, and $x y^t z = a^{i - 1 + t} b^j c^j$ is in $L$ for each $t \ge 0$: when the number of $a$s is 0 the first condition holds, and otherwise $j = k$ holds. If $w = b^j c^k$, then $y$ is $b$ or $c$, and the result still has no $a$. But $L$ is not regular. If it were, $L \cap a b^* c^* = \{ a b^j c^j : j \ge 0 \}$ would be regular, and the strings $a b^j$ for $j \ge 0$ are pairwise distinguishable for it: the suffix $c^j$ puts $a b^j$ in and $a b^{j'}$ out for $j' \ne j$. So it has infinitely many [Myhill-Nerode](/myhill-nerode-theorem/) classes.

Stronger pumping conditions exist that are also sufficient for regularity. Ehrenfeucht, Parikh and Rozenberg (1981) gave such a condition, which asks that pumping keep membership in both directions for every long enough block. The [Myhill-Nerode theorem](/myhill-nerode-theorem/) is the more practical exact test.

## History

Rabin and Scott proved the lemma in 1959, in the paper that introduced nondeterministic finite automata and their decision problems. Bar-Hillel, Perles and Shamir found it again in 1961, next to their pumping lemma for context-free languages.

## References
