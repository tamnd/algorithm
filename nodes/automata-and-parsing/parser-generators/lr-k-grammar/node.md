---
tag: XXHNT1
kind: definition
slug: lr-k-grammar
name: LR(k) grammar
aliases:
- LR(k)
- LR(1) grammar
area: automata-and-parsing/parser-generators
level: core
summary: A grammar that can be parsed bottom-up deterministically with k tokens of lookahead; the languages of LR(k) grammars are exactly the deterministic context-free languages.
prereqs: [lr-item-sets, first-and-follow-sets]
see_also: [lr-grammar, canonical-lr-parsing, lalr-parsing, slr-parsing, lr-parse-table, lookahead-symbols, ll-k-grammar, deterministic-context-free-language]
sources:
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (LR(k) grammars, the item sets with lookahead strings, the test for a fixed k, and the equivalence with deterministic languages)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.7.1, Canonical LR(1) Items; Section 4.7.2, Constructing LR(1) Sets of Items; Section 4.7.3, Canonical LR(1) Parsing Tables
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 9, Deterministic Bottom-Up Parsing (LR(1) and LR(k) parsing)
---

An LR(k) grammar is a [context-free grammar](/context-free-grammar/) for which a deterministic bottom-up parser, reading the input from left to right with $k$ tokens of lookahead, can always tell whether to shift or which production to reduce. Knuth (1965) defined the class by a condition on rightmost derivations and proved it equal to a test that a parser generator can run: build the canonical collection of LR(k) item sets and check that no state has a conflict. This page states the class from the side of that construction; the derivation form of the definition is on the [LR(k) grammar](/lr-grammar/) page of the context-free parsing area.

## Definition

**Notation.** A grammar is $G = (V, \Sigma, P, S)$ with productions written $A \to \alpha \mid \beta$, the empty string $\varepsilon$, start symbol $S$, input length $n$ and size $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$. The augmented grammar adds a new start symbol $S'$ and the production $S' \to S$. Lowercase $u, v, w$ are terminal strings and Greek letters are strings over $V \cup \Sigma$. For a terminal string $w$, $\mathrm{FIRST}_k(w)$ is the prefix of length $k$ of $w\,\$^k$, and for a string $\alpha$ of grammar symbols $\mathrm{FIRST}_k(\alpha)$ is the set of $\mathrm{FIRST}_k(w)$ over the terminal strings $w$ derived from $\alpha$.

**The derivation condition.** $G$ is *LR(k)* if, for any two rightmost derivations in the augmented grammar
$$S' \Rightarrow_{rm}^* \alpha A w \Rightarrow_{rm} \alpha \beta w \quad \text{and} \quad S' \Rightarrow_{rm}^* \gamma B x \Rightarrow_{rm} \alpha \beta y$$
with $\mathrm{FIRST}_k(w) = \mathrm{FIRST}_k(y)$, we have $\alpha = \gamma$, $A = B$ and $x = y$. The parser holds $\alpha\beta$ on its stack and sees $\mathrm{FIRST}_k$ of the rest; the condition says that this is enough to locate the [handle](/handle/) and name its production.

**LR(k) items.** An LR(k) item is a pair $[A \to \alpha \cdot \beta,\ u]$ of a dotted production, as in an [LR(0) item](/lr-item/), and a lookahead string $u$ of length $k$ over $\Sigma \cup \{\$\}$. The item is *valid* for a string $\gamma$ if there is a rightmost derivation $S' \Rightarrow_{rm}^* \delta A w \Rightarrow_{rm} \delta \alpha \beta w$ with $\gamma = \delta\alpha$ and $u = \mathrm{FIRST}_k(w)$. The canonical collection is built as for [LR(0) item sets](/lr-item-sets/), from the start item $[S' \to \cdot S,\ \$^k]$, with this closure rule:
$$[A \to \alpha \cdot B \beta,\ u] \in I,\quad B \to \eta \in P,\quad v \in \mathrm{FIRST}_k(\beta u) \implies [B \to \cdot \eta,\ v] \in I .$$
The goto on a symbol $X$ moves the dot over $X$ in every item that has $X$ after the dot and keeps the lookahead. The state reached from the start on a viable prefix $\gamma$ is exactly the set of LR(k) items valid for $\gamma$; this is Knuth's main lemma, proved for $k = 0$ on the [LR item sets](/lr-item-sets/) page, and the proof carries the lookahead along unchanged.

**Consistency.** A set $I$ of LR(k) items is *consistent* if

- no two complete items $[A \to \beta \cdot,\ u]$ and $[B \to \delta \cdot,\ u]$ with different productions share a lookahead (no reduce-reduce conflict), and
- no complete item $[A \to \beta \cdot,\ u]$ has $u \in \mathrm{FIRST}_k(a \nu v)$ for an item $[C \to \mu \cdot a \nu,\ v] \in I$ with $a$ a terminal (no shift-reduce conflict).

**Theorem (Knuth 1965).** $G$ is LR(k) if and only if every state of its canonical LR(k) collection is consistent. When it is, the states, their goto function and their consistent actions form the [canonical LR(k) parsing table](/canonical-lr-parsing/), and the parser runs in $O(n)$ steps.

The idea of the proof: by the main lemma, the items of the state for $\alpha\beta$ are exactly the handles that the derivation condition talks about. A conflict on $u$ in that state means two rightmost derivations whose sentential forms begin with $\alpha\beta$, continue with strings that agree on $\mathrm{FIRST}_k$, and have different handles at that point, which is a violation of the condition; and every violation shows up as such a pair of valid items.

**Sizes.** There are at most $|G| \cdot (|\Sigma| + 1)^k$ LR(k) items, and the number of states can be exponential in $|G|$ already for $k = 0$, as the family on the [LR item sets](/lr-item-sets/) page shows. Raising $k$ by one multiplies the possible lookaheads by $|\Sigma| + 1$ and usually splits states further, which is why tools stop at $k = 1$ and then merge states: [LALR(1)](/lalr-parsing/) keeps one state per LR(0) core.

## Examples and non-examples

State counts of the canonical LR(k) collection, with the number of states that are not consistent in brackets when there are any.

| grammar | $k = 0$ | $k = 1$ | $k = 2$ | $k = 3$ |
|---|---|---|---|---|
| $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to (\,E\,) \mid \mathit{id}$ | 12 (3) | 22 | 32 | 42 |
| $S \to L = R \mid R$, $L \to * R \mid \mathit{id}$, $R \to L$ | 10 (1) | 14 | 14 | 14 |
| $S \to A\,a\,b \mid B\,a\,c$, $A \to c$, $B \to c$ | 9 (1) | 9 (1) | 9 | 9 |
| $S \to a\,S\,a \mid a$ | 5 (1) | 8 (1) | 11 (1) | 14 (1) |
| $S \to S\,a\,a \mid a$ | 5 (1) | 5 | 5 | 5 |

**The expression grammar.** It is LR(1) and not LR(0). The three inconsistent LR(0) states are the ones with $E \to E \cdot + T$ beside $S' \to E \cdot$, with $E \to T \cdot$ beside $T \to T \cdot * F$, and with $E \to E + T \cdot$ beside $T \to T \cdot * F$; one token decides each. Each extra token of lookahead adds 10 states here, for $k \le 3$, because the lookaheads of the deeper items reach further into the right context while no state becomes inconsistent.

**One more token for each $a$.** In $S \to A\,a\,b \mid B\,a\,c$, $A \to c$, $B \to c$, the state reached on $c$ holds $[A \to c \cdot,\ a]$ and $[B \to c \cdot,\ a]$ for $k = 1$, a reduce-reduce conflict, and $[A \to c \cdot,\ a\,b]$ and $[B \to c \cdot,\ a\,c]$ for $k = 2$, which is consistent. Putting $m$ copies of $a$ in both right sides gives a grammar that is LR(m+1) and not LR(m), checked for $m \le 3$, so the classes of LR(k) grammars grow strictly with $k$.

**Not LR(k) for any k.** In $S \to a\,S\,a \mid a$ the parser must reduce the middle $a$ of $a^{2m+1}$, and with $m \ge k$ the next $k$ tokens are $a^k$ either way. For every $k$ the state reached on $a$, which holds $S \to a \cdot S\,a$, $S \to a \cdot$ and the closure items $S \to \cdot\, a\,S\,a$ and $S \to \cdot\, a$, is inconsistent on the lookahead $a^k$. The same language has the grammar $S \to S\,a\,a \mid a$, which is LR(1): being LR(k) is a property of the grammar, not of the language.

**Ambiguous grammars.** An ambiguous grammar is LR(k) for no $k$. For $E \to E + E \mid \mathit{id}$ the state reached on $E + E$ holds the complete item $E \to E + E \cdot$ and the item $E \to E \cdot + E$, and for every $k$ they conflict on a lookahead that starts with $+$: on $+\,\mathit{id}$ for $k = 2$ and on $+\,\mathit{id}\,+$ for $k = 3$. A generator such as [yacc](/yacc/) still builds a table for it by resolving the conflict with declared precedence; the table then picks one parse tree for each sentence, and the grammar is still not LR(k).

## Related definitions

- **Subclasses.** [SLR(1)](/slr-parsing/) and [LALR(1)](/lalr-parsing/) grammars are those whose LR(0) automaton becomes conflict-free with FOLLOW sets or with LALR lookaheads; every SLR(1) grammar is LALR(1) and every LALR(1) grammar is LR(1). The grammar $S \to L = R \mid R$ above is LALR(1) but not SLR(1).
- **Languages.** Knuth showed that the languages with an LR(k) grammar for some $k$ are exactly the [deterministic context-free languages](/deterministic-context-free-language/), and that each such language has an LR(1) grammar; see the [LR(k) grammar](/lr-grammar/) page for these results and for the undecidability of being LR(k) for some unknown $k$.
- **LL(k).** Every [LL(k) grammar](/ll-k-grammar/) without useless symbols is LR(k); the converse fails, since an LR parser decides after it has read the whole right side. See [lookahead symbols](/lookahead-symbols/).
- **Tables.** The [LR parse table](/lr-parse-table/) is the data structure, and [parser table construction](/parser-table-construction/) compares the ways of building it.

## References
