---
tag: J6KFBT
kind: concept
slug: lookahead-parsing
name: Lookahead
aliases:
- k-token lookahead
area: automata-and-parsing/context-free-parsing
level: core
summary: Input tokens examined beyond the current position to choose the next parsing action.
prereqs: [context-free-grammar, top-down-parsing, bottom-up-parsing]
see_also: [ll-grammar, lr-grammar, ll-parse-table, lr-parse-table, ll-star-parsing, first-and-follow-sets, left-factoring, backtracking-parsing]
sources:
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (LR(k) grammars, and the result that LR(k) languages are the deterministic languages)
  - paper: doi:10.1016/S0019-9958(70)90446-8
    title: D. J. Rosenkrantz and R. E. Stearns, Properties of deterministic top-down grammars, Information and Control 17(3) (1970)
    locator: pp. 226 to 256 (lookahead in LL(k) grammars)
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.4, Top-Down Parsing; Section 4.7, More Powerful LR Parsers (LR(1) items and their lookaheads)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 8, Deterministic Top-Down Parsing; Chapter 9, Deterministic Bottom-Up Parsing
---

Lookahead is the part of the input that a parser examines beyond the tokens it has already consumed, in order to choose its next action. A parser with $k$ tokens of lookahead decides each step from its own state and the next $k$ tokens; the classes [LL(k)](/ll-grammar/) and [LR(k)](/lr-grammar/) are the grammars for which this is enough to make every decision without guessing. More lookahead accepts more grammars, but the tables that store the decisions grow quickly with $k$, so practical parsers use $k = 1$ or a lookahead that is computed per decision.

## In plain words

A parser reads the input one word at a time, and at some points it must choose between two ways to go on. If it may peek at the next word before it chooses, that word is its lookahead. Some choices need more than one word: in "the old man the boats", only the last words show that "man" is a verb.

A parser that may peek at a fixed number of words is fast and never takes back a choice, but some grammars need it to peek further than any fixed number. Then you can change the grammar so that the choice is made later, let the parser peek as far as it needs, or let it try one way and back up when it fails.

## The idea

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area. The end marker $\$$ follows the last token.

**What lookahead is.** Let the input be $a_1 \cdots a_n \$$ and let the parser have consumed $a_1 \cdots a_{i-1}$. Its lookahead of length $k$ is $a_i \cdots a_{i+k-1}$, cut at the end marker when fewer than $k$ tokens remain. A parser *uses $k$ tokens of lookahead* when each of its actions is a function of its internal state, such as its stack, and of this string. The lookahead is examined, not consumed: the next action may consume $a_i$ or leave it for later.

**Where the decisions are.** A [top-down parser](/top-down-parsing/) decides which production to apply to the nonterminal on top of its stack, before it has read any of the tokens that the production derives. A [bottom-up parser](/bottom-up-parsing/) decides whether to shift the next token or to reduce a [handle](/handle/), and by which production, after it has read the whole right side. So a bottom-up parser has seen more of the input at the time of its decision, and with the same $k$ it handles more grammars: every [LL(k) grammar](/ll-grammar/) is an [LR(k) grammar](/lr-grammar/), and not conversely.

**The sets that lookahead is compared with.** The decisions are precomputed from sets of possible lookahead strings. $\mathrm{FIRST}_k(\alpha)$ is the set of strings of length up to $k$ that begin terminal strings derived from $\alpha$, and $\mathrm{FOLLOW}_k(A)$ is the set of such strings that can come right after $A$ in a sentential form; for $k = 1$ these are the [FIRST and FOLLOW sets](/first-and-follow-sets/). An LL(1) parser applies $A \to \alpha$ when the lookahead is in $\mathrm{FIRST}(\alpha)$, or in $\mathrm{FOLLOW}(A)$ when $\alpha$ is nullable; an LR(1) parser reduces by $A \to \alpha$ when the lookahead is in the set carried by the item $[A \to \alpha \cdot]$. If two actions share a lookahead string, the grammar has a *conflict* for that $k$.

**The price of $k$.** A table indexed by lookahead strings has up to $|\Sigma|^k$ columns for each row, and the number of LR(k) states also grows with $k$. Most generators therefore fix $k = 1$, and approximate even the one-token sets: [SLR parsing](/slr-parsing/) uses $\mathrm{FOLLOW}(A)$ as the lookahead set of every reduction by $A$, and [LALR parsing](/lalr-parsing/) merges LR(1) states with the same items.

**How much lookahead languages need.** For bottom-up parsing, one token is enough: Knuth (1965) proved that the languages with an LR(k) grammar for some $k$ are exactly the [deterministic context-free languages](/deterministic-context-free-language/), and each of them has an LR(1) grammar. So more lookahead helps to write grammars, not to describe more languages. For top-down parsing, more lookahead does give more languages, and some deterministic languages, such as $\{a^m b^m : m \ge 1\} \cup \{a^m c^m : m \ge 1\}$, have no LL(k) grammar for any $k$.

**Unbounded lookahead.** Some decisions need a lookahead of unbounded length. [LL(*) parsing](/ll-star-parsing/) scans ahead with a finite automaton built for each decision, as far as the automaton needs. [Backtracking parsing](/backtracking-parsing/) and [packrat parsing](/packrat-parsing/) try one alternative, and fall back to the next when it fails; the cost of a failed attempt is lookahead paid in time. The [Earley parser](/earley-parser/) and [GLR parsing](/glr-parsing/) avoid the decision altogether by following all alternatives at once.

## Examples

**Top-down, $k = 2$.** In $S \to a S \mid a$, the first token is $a$ for both productions, so one token cannot choose. Two tokens can: $aa$ selects $S \to a S$ and $a\$$ selects $S \to a$. [Left factoring](/left-factoring/) moves the decision one token later, to $S \to a S'$, $S' \to S \mid \varepsilon$, which needs only one token.

**Bottom-up, $k = 1$.** In $S \to A a \mid B b$, $A \to c$, $B \to c$, after reading $c$ the parser must reduce, either by $A \to c$ or by $B \to c$. Without lookahead it cannot choose: the [LR(0)](/lr0-parsing/) state holds the two complete items $A \to c \cdot$ and $B \to c \cdot$, a reduce-reduce conflict. With one token, $a$ selects $A \to c$ and $b$ selects $B \to c$, and the grammar is LR(1).

**Bottom-up, $k = 2$.** In $S \to A a b \mid B a c$, $A \to c$, $B \to c$, the token after $c$ is $a$ in both cases, so the grammar is not LR(1). The two tokens $ab$ and $ac$ decide, so it is LR(2). The language $\{cab, cac\}$ itself has the LR(0) grammar $S \to c a b \mid c a c$.

**No fixed $k$ for top-down, $k = 1$ for bottom-up.** In $S \to A b \mid A c$, $A \to a A \mid a$, the choice between the two productions of $S$ depends on the token after the whole run of $a$'s, so the grammar is not LL(k) for any $k$. An LR(1) parser reads the $a$'s first, reduces them to $A$, and only then sees $b$ or $c$; it uses its one token to decide, at the last $a$, between shifting another $a$ and reducing by $A \to a$. An LL(*) parser handles the grammar too, by scanning $a^* (b \mid c)$ at the start.

## Where it is used

- **Parse tables.** The columns of the [LL parse table](/ll-parse-table/) and of the action part of the [LR parse table](/lr-parse-table/) are lookahead tokens.
- **Parser generators.** Yacc and Bison build LALR(1) tables, with one token of lookahead. ANTLR computes the lookahead of each decision, as in [LL(*) parsing](/ll-star-parsing/).
- **Error detection.** An empty table cell for the current lookahead is how a deterministic parser detects a syntax error, and the lookahead sets of the current state name the tokens that were expected.
- **Error recovery.** [Panic-mode error recovery](/panic-mode-error-recovery/) skips input until the lookahead is in a synchronizing set, often a FOLLOW set.
- **Lexers.** A lexer that returns the longest token uses lookahead over characters: on reading $<$ it must look at the next character to tell $<$ from $<=$.

## References
