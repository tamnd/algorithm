---
tag: S9WMZP
kind: definition
slug: deterministic-context-free-language
name: Deterministic context-free language
aliases:
- DCFL
area: automata-and-parsing/context-free-parsing
level: advanced
summary: A context-free language accepted by a deterministic pushdown automaton, equal to the LR(k) languages.
prereqs: [pushdown-automaton, context-free-language]
see_also: [knuth-lr-theorem, lr-grammar, lr-parsing, cfl-closure-properties, cfl-pumping-lemma, inherent-ambiguity, ll-grammar, dyck-language]
sources:
  - paper: doi:10.1016/S0019-9958(66)80019-0
    title: Seymour Ginsburg and Sheila Greibach, Deterministic context free languages, Information and Control 9(6) (1966)
    locator: pp. 620 to 648
  - book: isbn:9780201029888
    title: John E. Hopcroft and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, Addison-Wesley, 1979
    locator: Chapter 10, Deterministic Context-Free Languages
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 2.4, Deterministic Context-Free Languages
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639
  - paper: doi:10.1016/S0304-3975(00)00285-1
    title: Géraud Sénizergues, L(A)=L(B)? decidability results from complete formal systems, Theoretical Computer Science 251(1-2) (2001)
    locator: pp. 1 to 166 (equivalence of deterministic pushdown automata is decidable)
  - paper: doi:10.1145/800135.804426
    title: Stephen A. Cook, Deterministic CFL's are accepted simultaneously in polynomial time and log squared space, Proceedings of the 11th Annual ACM Symposium on Theory of Computing (1979)
    locator: pp. 338 to 345
---

A deterministic context-free language (DCFL) is a language that a deterministic [pushdown automaton](/pushdown-automaton/) accepts by final state. These are the languages that a parser can read from left to right with a stack and without guesses: by [Knuth's LR theorem](/knuth-lr-theorem/) they are exactly the languages of [LR(1) grammars](/lr-grammar/), and also of LR(k) grammars for any $k$. The class lies strictly between the [regular languages](/regular-language/) and the [context-free languages](/context-free-language/).

## Definition

We use the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol, $n$ the input length, and the grammar size $|G| = \sum_{A \to \alpha} (|\alpha| + 1)$. For automata we use the notation of the [pushdown automaton](/pushdown-automaton/) page: $M = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$, configurations $(q, w, \gamma)$ with the top of the stack on the left, and the move relation $\vdash$.

A pushdown automaton $M$ is **deterministic** (a DPDA) if for every state $q$, input symbol $a \in \Sigma$ and stack symbol $X \in \Gamma$:

- $\delta(q, a, X)$ has at most one element and $\delta(q, \varepsilon, X)$ has at most one element;
- if $\delta(q, \varepsilon, X)$ is nonempty, then $\delta(q, b, X)$ is empty for every $b \in \Sigma$.

Then every configuration has at most one move. A language $L \subseteq \Sigma^*$ is a **deterministic context-free language** if $L = L(M)$ for some DPDA $M$, where

$$L(M) = \{\, w \in \Sigma^* : (q_0, w, Z_0) \vdash^* (q, \varepsilon, \gamma) \text{ for some } q \in F \text{ and } \gamma \in \Gamma^* \,\}.$$

**The run on a word.** Because each configuration has at most one move, the input $w$ gives one sequence of configurations, the *run* of $M$ on $w$. It stops when there is no move, or when the next move must read a symbol that is not there; it can also go on for ever with $\varepsilon$-moves. The word $w$ is accepted when some configuration of the run, reached after all of $w$ is read, has a state in $F$. Since a move that reads is never possible where an $\varepsilon$-move is possible, the run on a prefix $x$ of $xy$ is a prefix of the run on $xy$, up to the first move that reads a symbol of $y$. This is the property that all proofs about DCFLs use.

**Normal forms.** Every DPDA has an equivalent DPDA that reads its whole input on every word and never makes an infinite sequence of $\varepsilon$-moves. Ginsburg and Greibach proved this in 1966, and used it to show that the DCFLs are closed under complement: swap accepting and non-accepting states, with care for the states that the run passes through after the last input symbol.

## Examples and non-examples

**Regular languages.** A deterministic finite automaton is a DPDA that never changes its stack, so every regular language is a DCFL.

**$\{a^m b^m : m \ge 0\}$.** Take states $p, q, r, f$ with start $p$, $F = \{p, f\}$, stack symbols $Z_0, A$, and the moves

$$\delta(p, a, Z_0) = (q, A Z_0), \quad \delta(q, a, A) = (q, A A), \quad \delta(q, b, A) = (r, \varepsilon), \quad \delta(r, b, A) = (r, \varepsilon), \quad \delta(r, \varepsilon, Z_0) = (f, Z_0).$$

The automaton pushes one $A$ for each $a$, pops one for each $b$, and goes to $f$ when the bottom symbol shows again. A $b$ before any $a$, an $a$ after a $b$, or too many $b$'s leave it with no move, and too few $b$'s leave it in $r$.

**The Dyck language.** The [Dyck language](/dyck-language/) of balanced brackets on one pair is accepted by the DPDA with states $f, q$, start $f$, $F = \{f\}$ and the moves

$$\delta(f, (, Z_0) = (q, A Z_0), \quad \delta(q, (, A) = (q, A A), \quad \delta(q, ), A) = (q, \varepsilon), \quad \delta(q, \varepsilon, Z_0) = (f, Z_0).$$

The number of $A$'s on the stack is the depth of the open brackets. In $q$ with $Z_0$ on top only the $\varepsilon$-move exists, and in $q$ with $A$ on top only reading moves exist, so the automaton is deterministic.

**Programming languages.** The languages of [LR(1) grammars](/lr-grammar/), such as arithmetic expressions with the usual precedence, are DCFLs, because an [LR parser](/lr-parsing/) is a DPDA.

**Marked palindromes.** $\{ w c w^R : w \in \{a, b\}^* \}$ is a DCFL: push symbols until $c$, then pop and compare. The marker $c$ tells the automaton where the middle is.

**Non-example: $L_2 = \{a^m b^m : m \ge 1\} \cup \{a^m b^{2m} : m \ge 1\}$.** This language is context-free and has an unambiguous grammar, $S \to A \mid B$, $A \to a A b \mid a b$, $B \to a B b b \mid a b b$, but it is not a DCFL.

*Proof.* Suppose that a DPDA $M$ accepts $L_2$. Build a (nondeterministic) pushdown automaton $M''$ from two copies of $M$. Copy 1 is $M$ itself. Copy 2 is $M$ with every move that reads $b$ changed to a move that reads $c$. $M''$ starts in copy 1. In every state $q \in F$ of copy 1 it may also make an $\varepsilon$-move to the twin of $q$ in copy 2, with the stack unchanged. The accepting states of $M''$ are the states of $F$ in copy 2. We show that

$$L(M'') \cap a^* b^* c^+ = \{a^m b^m c^m : m \ge 1\}.$$

($\supseteq$) Let $m \ge 1$. The run of $M$ on $a^m b^{2m}$ accepts. By determinism it starts with the run on $a^m b^m$, which accepts, so it passes through a configuration $C$ with a state in $F$ after all of $a^m b^m$ is read; the rest of the run reads $b^m$ from $C$ and reaches a state in $F$ after the last $b$. $M''$ follows the run in copy 1 up to $C$, moves to copy 2, and follows the rest of the run, reading $c^m$ in place of $b^m$. So $M''$ accepts $a^m b^m c^m$.

($\subseteq$) Let $M''$ accept $w \in a^* b^* c^+$. An accepting computation ends in copy 2, so it moves to copy 2 once, at a configuration $C$ with a state in $F$. Let $x$ be the part of $w$ read before $C$ and $z$ the rest. Copy 1 never reads $c$ and copy 2 never reads $b$, so $x \in a^* b^*$, and $z$ is not empty because $w$ has a $c$. The computation up to $C$ is a run of $M$ that accepts $x$, so $x \in L_2$, and $x$ ends with $b$. Then $z \in c^+$, say $z = c^j$ with $j \ge 1$, and the whole computation is a computation of $M$ that accepts $x b^j$, so $x b^j \in L_2$. If $x = a^m b^m$, then $a^m b^{m + j} \in L_2$ gives $j = m$. If $x = a^m b^{2m}$, then $a^m b^{2m + j} \in L_2$ is false for all $j \ge 1$. So $w = a^m b^m c^m$.

A pushdown automaton accepts a [context-free language](/context-free-language/), and the intersection of a context-free language with a regular language is context-free ([closure properties](/cfl-closure-properties/)). So $\{a^m b^m c^m : m \ge 1\}$ would be context-free. It is not, by the [pumping lemma](/cfl-pumping-lemma/). This contradiction shows that $L_2$ is not a DCFL. $\blacksquare$

**Non-example: even palindromes.** $L_P = \{ w w^R : w \in \{a, b\}^* \}$ is not a DCFL, although it has the unambiguous grammar $S \to a S a \mid b S b \mid \varepsilon$. The same method works. If a DPDA $M$ accepts $L_P$, build $M''$ as above, with copy 2 reading $c$ in place of $a$ and $d$ in place of $b$. Then

$$L(M'') \cap a^* b b a^* d d c^* = \{ a^i b b a^i d d c^i : i \text{ even} \}.$$

The part read in copy 1 is $x = a^i b b a^m$, and it must be in $L_P$, so $m = i$. The part read in copy 2 is $d d c^k$, and $a^i b b a^i b b a^k$ must be in $L_P$; it is a palindrome only for $k = i$, and its length $3i + 4$ is even only for even $i$. Conversely, for even $i$ both $a^i b b a^i$ and $a^i b b a^i b b a^i$ are in $L_P$, and determinism gives the accepting computation of $M''$ as before. The language on the right is not context-free: for the pumping length $p$ take $a^{2p} b b a^{2p} d d c^{2p}$. A part $v x y$ of length at most $p$ meets at most two of the three blocks $a^{2p}$, $a^{2p}$, $c^{2p}$. Pumping down either removes a $b$ or a $d$, or shortens one or two of the blocks but not all three, and in both cases the word leaves the language. $\blacksquare$

**Non-example: languages that are not context-free.** $\{a^m b^m c^m\}$ and every other language that is not context-free are not DCFLs, since a DPDA is a pushdown automaton.

## Related definitions

- **LR languages.** By [Knuth's LR theorem](/knuth-lr-theorem/), a language is a DCFL if and only if it has an [LR(k) grammar](/lr-grammar/) for some $k$, if and only if it has an LR(1) grammar. So the DCFLs are the languages that an [LR parser](/lr-parsing/) can parse, and they are recognized in $O(n)$ time.
- **Prefix property and LR(0).** A language has the *prefix property* if no word in it is a proper prefix of another word in it. The languages that a DPDA accepts by empty stack are exactly the DCFLs with the prefix property, and these are also the languages of LR(0) grammars. For any DCFL $L$ and a new end marker $\dashv$, the language $L \dashv$ has the prefix property, which is why parsers add an end marker.
- **LL languages.** The languages of [LL(k) grammars](/ll-grammar/) are DCFLs, because an LL(k) parser is also a DPDA. The inclusion is strict: there are DCFLs with no LL(k) grammar for any $k$.
- **Unambiguity.** Every LR(k) grammar is unambiguous, so every DCFL has an unambiguous grammar and is not [inherently ambiguous](/inherent-ambiguity/). The converse is false: $L_2$ and $L_P$ above are unambiguous but not deterministic.
- **Closure.** The DCFLs are closed under complement, under intersection with a regular language (run a DPDA and a deterministic finite automaton side by side) and under inverse homomorphism. They are not closed under union: $\{a^m b^m : m \ge 1\}$ and $\{a^m b^{2m} : m \ge 1\}$ are DCFLs, but their union $L_2$ is not. They are not closed under intersection either: $\{a^m b^m c^k : m, k \ge 0\}$ and $\{a^k b^m c^m : m, k \ge 0\}$ are DCFLs, and their intersection $\{a^m b^m c^m : m \ge 0\}$ is not context-free. The context-free languages are not closed under complement, so closure under complement gives a second way to separate the classes: a context-free language whose complement is not context-free is not a DCFL.
- **Decision problems.** Sénizergues proved that it is decidable whether two DPDAs accept the same language; for general pushdown automata the question is undecidable. It is also undecidable whether a given context-free grammar generates a DCFL.
- **Space and parallel complexity.** Cook proved that a DCFL can be recognized by one algorithm in polynomial time and $O(\log^2 n)$ space at the same time.

## References
