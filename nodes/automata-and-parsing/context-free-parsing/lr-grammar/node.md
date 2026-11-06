---
tag: 801CWY
kind: definition
slug: lr-grammar
name: LR(k) grammar
aliases:
- LR(1) grammar
area: automata-and-parsing/context-free-parsing
level: core
summary: A grammar parsable deterministically bottom-up with k symbols of lookahead.
prereqs: [context-free-grammar, handle, lr-item]
see_also: [lr-k-grammar, ll-grammar, lr-parsing, canonical-lr-parsing, lr0-parsing, deterministic-context-free-language, lookahead-parsing, ambiguity]
sources:
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (the definition of LR(k) grammars, the test for fixed k, the equivalence with deterministic languages, and the undecidability of the LR(k) property for unknown k)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.6, Introduction to LR Parsing; Section 4.7, More Powerful LR Parsers
  - paper: doi:10.1145/361227.361232
    title: Harry B. Hunt III, Thomas G. Szymanski and Jeffrey D. Ullman, On the complexity of LR(k) testing, Communications of the ACM 18(12) (1975)
    locator: pp. 707 to 716 (an O(n^(k+2)) test for the LR(k) property, for each fixed k)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 9, Deterministic Bottom-Up Parsing
---

An LR(k) grammar is a [context-free grammar](/context-free-grammar/) whose rightmost derivations can be undone one step at a time, from left to right, by looking at the part of the input already reduced and at the next $k$ tokens. Knuth (1965) defined the class and showed that its grammars are exactly those for which a deterministic [LR parser](/lr-parsing/) exists, running in linear time. Every LR(k) grammar is unambiguous, every [LL(k) grammar](/ll-grammar/) is LR(k), and the languages of LR(k) grammars are exactly the [deterministic context-free languages](/deterministic-context-free-language/).

## Definition

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area. The augmented grammar adds a new start symbol $S'$ with the production $S' \to S$. For a string $w$, $\mathrm{FIRST}_k(w)$ is the prefix of length $k$ of $w \$^k$, where $\$ \notin \Sigma$ is an end marker.

**LR(k).** Let $k \ge 0$. The grammar $G$ is *LR(k)* if, for all rightmost derivations in the augmented grammar

$$S' \Rightarrow_{rm}^* \alpha A w \Rightarrow_{rm} \alpha \beta w \qquad \text{and} \qquad S' \Rightarrow_{rm}^* \gamma B x \Rightarrow_{rm} \alpha \beta y,$$

with $w, x, y \in \Sigma^*$, the condition $\mathrm{FIRST}_k(w) = \mathrm{FIRST}_k(y)$ implies $\alpha = \gamma$, $A = B$ and $x = y$. A grammar is *LR* if it is LR(k) for some $k$.

In words: in the right-sentential form $\alpha \beta w$, the [handle](/handle/) is $\beta$, reduced by $A \to \beta$. If another right-sentential form $\alpha \beta y$ starts with the same $\alpha\beta$ and has the same next $k$ terminals, then its handle must be the same production at the same place. So a parser that holds $\alpha\beta$ on its stack and sees $k$ tokens never needs more information to decide whether to reduce, and by which production.

**Equivalent form.** $G$ is LR(k) if and only if the canonical LR(k) automaton, built from the [LR(k) items](/lr-item/), has no state with a conflict: no two complete items $[A \to \beta \cdot, u]$ and $[B \to \delta \cdot, u]$ with different productions, and no complete item $[A \to \beta \cdot, u]$ together with an item $[C \to \mu \cdot a \nu, v]$ such that $u \in \mathrm{FIRST}_k(a \nu v)$. This gives a test for each fixed $k$; Hunt, Szymanski and Ullman (1975) do it in $O(|G|^{k+2})$ time without building the automaton, which can be exponentially large.

**LR(0) and the end marker.** For $k = 0$ the condition also covers the production $S' \to S$, so a grammar whose language has a word that is a proper prefix of another word, such as $L \to L , x \mid x$, is not LR(0): after $x$ the parser cannot tell whether to stop. Many textbooks and tools augment with $S' \to S \, \$$ instead and shift $\$$ like a token; then $L \to L , x \mid x$ passes the LR(0) test. The [LR(0) parsing](/lr0-parsing/) page uses this convention.

**Subclasses.** The parsers that build smaller automata accept fewer grammars:

$$\text{LR(0)} \subset \text{SLR(1)} \subset \text{LALR(1)} \subset \text{LR(1)}$$

as classes of grammars, each inclusion strict. [LR(0) parsing](/lr0-parsing/) uses no lookahead, [SLR](/slr-parsing/) uses FOLLOW sets for the complete items, [LALR](/lalr-parsing/) merges the LR(1) states that have the same items, and [canonical LR(1)](/canonical-lr-parsing/) keeps them all.

## Examples and non-examples

The table gives the smallest $k$ for which the canonical LR(k) automaton has no conflict, checked for $k \le 3$.

| grammar | LR(0) | LR(1) | LR(2) | note |
|---|---|---|---|---|
| $L \to L , x \mid x$ | no | yes | yes | LR(0) with an end marker, see below |
| $L \to x , L \mid x$ | no | yes | yes | after $x$, reduce on $\$$, shift on $,$ |
| $S \to a S b \mid a b$ | yes | yes | yes | |
| $S \to A a$, $A \to \varepsilon$ | yes | yes | yes | reduce $\varepsilon$ to $A$ first |
| $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to ( E ) \mid id$ | no | yes | yes | the expression grammar |
| $S \to A a \mid B b$, $A \to c$, $B \to c$ | no | yes | yes | after $c$, the next token picks $A$ or $B$ |
| $S \to A a b \mid B a c$, $A \to c$, $B \to c$ | no | no | yes | the token after $a$ decides |
| $S \to A b \mid A c$, $A \to a A \mid a$ | no | yes | yes | not LL(k) for any $k$ |
| $S \to a S a \mid a$ | no | no | no | not LR(k) for any $k$ |
| $E \to E + E \mid a$ | no | no | no | ambiguous |

**Why $S \to A a b \mid B a c$ needs two tokens.** After $c$, the parser must reduce $c$ to $A$ or to $B$. The right-sentential forms $c\,a\,b$ and $c\,a\,c$ have the handles $A \to c$ and $B \to c$ at the same place, and both continue with $a$. So $\mathrm{FIRST}_1$ does not separate them and $\mathrm{FIRST}_2$, which is $a b$ or $a c$, does.

**Why $S \to a S a \mid a$ is not LR.** Its language is the strings $a^{2m+1}$, which is regular, but the handle of $a^{2m+1}$ is the middle $a$. Take $\alpha\beta = a^{m+1}$ with $\beta = a$, the handle of $a^{2m+1}$, and $\alpha \beta y$ with $y = a^{m+2}$, the form $a^{2m+3}$, whose handle is further right; for $m \ge k$ the next $k$ tokens are $a^k$ in both. So the LR condition fails for every $k$. The equivalent grammar $S \to S a a \mid a$ is LR(1).

**Ambiguous grammars are never LR.** If $w$ had two rightmost derivations, follow both backwards from $w$: at the first right-sentential form where they choose different handles, the two choices have the same left part and the same remaining input, so the LR condition is violated for every $k$. So every LR(k) grammar is unambiguous, and an ambiguous grammar such as $E \to E + E \mid a$ is LR(k) for no $k$.

**Languages without LR grammars.** The even palindromes $\{ u u^R : u \in \{a, b\}^* \}$ have no LR(k) grammar for any $k$, because they are not a deterministic context-free language: a parser reading from left to right cannot know where the middle is.

## Related definitions

- **LR(k) languages.** Knuth (1965) showed that a language has an LR(k) grammar for some $k$ if and only if it is accepted by a deterministic pushdown automaton, and that every such language already has an LR(1) grammar. So for languages the hierarchy collapses at $k = 1$, while for grammars it is strict: $S \to A a b \mid B a c$, $A \to c$, $B \to c$ is LR(2) and not LR(1). The languages of LR(0) grammars are the deterministic context-free languages with the prefix property, in which no word is a proper prefix of another.
- **Undecidability.** For fixed $k$ the LR(k) property is decidable, but whether a grammar is LR(k) for some $k$ is undecidable (Knuth 1965).
- **LL(k).** Every LL(k) grammar is LR(k), and the inclusion is strict: $S \to A b \mid A c$, $A \to a A \mid a$ is LR(1) but LL(k) for no $k$. An LR parser decides after seeing the whole right side and $k$ more tokens, an LL parser before seeing any of it. See [lookahead parsing](/lookahead-parsing/).
- **The parser-generator view.** The page [LR(k) grammar](/lr-k-grammar/) in the parser-generator area treats the same class from the side of table construction.

## References
