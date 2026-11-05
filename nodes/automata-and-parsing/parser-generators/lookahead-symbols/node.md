---
tag: 4H70F6
kind: concept
slug: lookahead-symbols
name: Lookahead symbols
aliases:
- lookahead set
- lookahead token
area: automata-and-parsing/parser-generators
level: core
summary: The next input token(s) a parser inspects to choose its next action without consuming them.
prereqs: [first-and-follow-sets, shift-reduce-parsing]
see_also: [ll-1-grammar, ll-k-grammar, lr-k-grammar, lalr-lookahead-computation, slr-parsing, ll-star-parsing, parsing-expression-grammar, glr-parsing]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 3.5.4, The Lookahead Operator; Section 4.4.3, LL(1) Grammars; Section 4.6.4, Constructing SLR-Parsing Tables; Section 4.7, More Powerful LR Parsers
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: the definition of LR(k) grammars with k symbols of lookahead and the construction of the parser from item sets with lookahead strings
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 8, Deterministic Top-Down Parsing, and Chapter 9, Deterministic Bottom-Up Parsing
  - paper: doi:10.1145/964001.964011
    title: Bryan Ford, Parsing expression grammars, a recognition-based syntactic foundation, POPL 2004
    locator: the and-predicate and not-predicate operators, which look ahead without consuming input
  - paper: "Terence Parr and Kathleen Fisher, LL(*): the foundation of the ANTLR parser generator, PLDI 2011"
    locator: the lookahead automaton built for each parsing decision
---

A lookahead symbol is an input token that a parser examines to choose its next move without consuming it. A parser with $k$ tokens of lookahead sees the next $k$ tokens, padded with the end marker $\$$ near the end of the input, and its table maps each stack configuration and each such string to one action. The *lookahead set* of a parsing decision is the set of strings on which that decision is taken; computing these sets, as [FIRST and FOLLOW](/first-and-follow-sets/) sets, LALR lookaheads or LR(1) item lookaheads, is most of the work of a [parser generator](/parser-generator/).

## In plain words

When you read a sentence aloud you sometimes glance at the next word before you decide how to say the current one. A parser does the same. It peeks at the next token, and sometimes the next few, to decide which grammar rule it is in, without moving past them.

How far a parser must peek depends on the grammar and on the parsing method. A top-down parser must pick a rule as soon as the rule's text starts, so it needs to see enough of that text to tell the rules apart. A bottom-up parser waits until the whole rule has been read, so one token beyond it is usually enough. Peeking further makes the parser stronger, but its tables grow quickly, so most tools peek at one token.

## The idea

**Notation.** A grammar is $G = (V, \Sigma, P, S)$ with productions $A \to \alpha \mid \beta$, the empty string $\varepsilon$, start symbol $S$, input length $n$ and size $|G|$, the total length of the productions. The input is followed by the end marker $\$$. For a terminal string $w$, $w{:}k$ is its prefix of length $k$, or $w$ itself if it is shorter. $\mathrm{FIRST}_k(\alpha) = \{\, w{:}k : \alpha \Rightarrow^* w,\ w \in \Sigma^* \,\}$, and $\mathrm{FIRST}_1$ is the FIRST set with $\varepsilon$ standing for "nullable".

**When the decision is made.** A top-down parser such as an [LL(k)](/ll-k-grammar/) parser chooses the production $A \to \alpha$ when $A$ is on top of its stack, before it has read anything that $\alpha$ derives. Its lookahead must separate the alternatives of $A$ from their first $k$ tokens, plus what follows $A$ if an alternative can be empty. A bottom-up parser in the [LR(k)](/lr-k-grammar/) family reduces by $A \to \alpha$ only after it has read all of $\alpha$, so its $k$ tokens of lookahead come after the right side. Every LL(k) grammar without useless symbols is LR(k), and the converse fails, as the examples show.

**Lookahead sets in LR parsers.** For a completed item $A \to \alpha \cdot$ in a state $q$ of the [LR(0) automaton](/lr-item-sets/), the methods differ only in the set of terminals on which they reduce:

- [SLR(1)](/slr-parsing/) uses $\mathrm{FOLLOW}(A)$, which depends on $A$ alone;
- [LALR(1)](/lalr-parsing/) uses $\mathrm{LA}(q, A \to \alpha)$, the terminals that can follow $A$ when the parser reaches $q$ by any path, computed by [LALR lookahead computation](/lalr-lookahead-computation/);
- [canonical LR(1)](/canonical-lr-parsing/) splits $q$ into one state per context, so each copy has its own lookahead set.

The sets shrink down this list: $\mathrm{LA}(q, A \to \alpha) \subseteq \mathrm{FOLLOW}(A)$, and $\mathrm{LA}$ is the union of the sets of the LR(1) copies of $q$. Smaller sets mean fewer conflicts, so every SLR(1) grammar is LALR(1) and every LALR(1) grammar is LR(1).

**The cost of more lookahead.** A table indexed by $k$ tokens has up to $(|\Sigma| + 1)^k$ columns, and canonical LR(k) item sets also multiply with the number of lookahead strings. For languages the gain stops at $k = 1$: Knuth showed that the LR(k) grammars generate exactly the deterministic context-free languages, and that each of them has an LR(1) grammar. For grammars the gain is real at every $k$, which is why authors rewrite grammars rather than raise $k$.

**Unbounded lookahead.** Some methods give up a fixed $k$. A backtracking parser tries an alternative and returns to the saved input position if it fails, which in effect looks ahead as far as the failed attempt went. A [parsing expression grammar](/parsing-expression-grammar/) has explicit predicates: $\&e$ succeeds when $e$ matches at the current position and $!e$ when it does not, and neither consumes input. [LL(*) parsing](/ll-star-parsing/) builds a finite automaton per decision that scans as far ahead as needed. Generalized parsers such as [GLR](/glr-parsing/) avoid the question by following all actions at once.

## Examples

**Delaying the decision.** $S \to a\,b \mid a\,c$ is not LL(1): both alternatives begin with $a$. It is LL(2), since the second token separates them, and it is LR(0): the LR(0) automaton has 5 states and none of them has a choice, because the parser shifts $a$ and then $b$ or $c$ before it reduces. Left factoring, $S \to a\,S'$, $S' \to b \mid c$, makes the grammar LL(1).

**One token after the right side.** $E \to T + E \mid T$, $T \to \mathit{id}$. After the parser has shifted $T$ it is in the state $\{E \to T \cdot + E,\ E \to T \cdot\}$. It must reduce at the end of the input and shift on $+$, so it needs one token of lookahead: the grammar is not LR(0) but is SLR(1), with $\mathrm{FOLLOW}(E) = \{\$\}$. It is not LL(1), since both alternatives start with $T$, which derives $\mathit{id}$. It is LL(2): the first alternative is chosen on $\mathit{id}\,{+}$ and the second on $\mathit{id}\,\$$.

**A grammar with no finite top-down lookahead.** $S \to A \mid B$, $A \to a\,A\,b \mid a\,b$, $B \to a\,B\,c \mid a\,c$ generates $\{a^m b^m\} \cup \{a^m c^m\}$ for $m \ge 1$. A top-down parser must choose between $A$ and $B$ at the first token, and for every $k$ both choose-$A$ and choose-$B$ inputs begin with $a^k$, so the grammar is not LL(k) for any $k$. It is LR(0): its LR(0) automaton has 11 states without a conflict, because the parser shifts all the $a$ tokens and decides when it sees the first $b$ or $c$.

**A grammar that is not LR(k) for any k.** $S \to a\,S\,a \mid a$ generates the strings of odd length over $\{a\}$. To parse $a^{2m+1}$ the parser must reduce the middle $a$ by $S \to a$ when exactly $m$ tokens remain, and with $m \ge k$ the next $k$ tokens are $a^k$ whether or not it is the middle. The canonical LR(k) automaton has a shift-reduce conflict on $a^k$ for every $k$ from 1 to 4 (8, 11, 14 and 17 states). The same language has the SLR(1) grammar $S \to S\,a\,a \mid a$: lookahead is a property of the grammar, not of the language.

**Lookahead sets that merging spoils.** $S \to a\,A\,d \mid b\,B\,d \mid a\,B\,e \mid b\,A\,e$, $A \to c$, $B \to c$. The canonical LR(1) automaton has 14 states. After $a\,c$ the parser is in a state that reduces $A \to c$ on $d$ and $B \to c$ on $e$; after $b\,c$ it is in a state that reduces $A \to c$ on $e$ and $B \to c$ on $d$. The two states have the same LR(0) core, and the LALR(1) construction merges them into one of its 13 states, whose lookahead sets $\{d, e\}$ for both reductions collide: two reduce-reduce conflicts. The grammar is LR(1) but not LALR(1).

## Where it is used

- **Parser generators.** The LL(1) table puts $A \to \alpha$ in the cells of $\mathrm{FIRST}(\alpha)$ and, for nullable $\alpha$, of $\mathrm{FOLLOW}(A)$; see [LL(1) grammars](/ll-1-grammar/). [Yacc](/yacc/) and Bison compute LALR(1) lookahead sets for the reductions of each state; see [parser table construction](/parser-table-construction/).
- **Lexical analysis.** A scanner that takes the longest matching token reads characters beyond the end of a token before it accepts the token, and returns them to the input afterwards; Lex states this explicitly with its lookahead operator: the pattern `r/s` matches $r$ only when $s$ follows, and leaves $s$ in the input.
- **Error detection.** The lookahead token is the point at which a deterministic parser detects an error, and the lookahead sets of the states on the stack are the candidate repairs; see [parser error recovery](/parser-error-recovery/).
- **Grammar design.** Conflict reports name a state and a lookahead token, and the usual fix is to rewrite the grammar so that one token suffices, by [left factoring](/left-factoring/), by removing [left recursion](/left-recursion/) for LL, or by declaring precedence for LR.

## References
