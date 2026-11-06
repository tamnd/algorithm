---
tag: BN030M
kind: technique
slug: panic-mode-error-recovery
name: Panic-mode error recovery
area: automata-and-parsing/context-free-parsing
level: core
summary: Discards input tokens until a synchronizing token lets the parser resume after a syntax error.
prereqs: [first-and-follow-sets, ll1-parsing, lr-parse-table]
see_also: [parser-error-recovery, ll-parse-table, recursive-descent-parsing, yacc, shift-reduce-parsing, operator-precedence-parsing, top-down-parsing, bottom-up-parsing]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.1.4, Error-Recovery Strategies; Section 4.4.5, Error Recovery in Predictive Parsing (synch entries from FOLLOW sets and the trace of Figure 4.23); Section 4.8.3, Error Recovery in LR Parsing; Section 4.9.4, Error Recovery in Yacc
  - book: isbn:9780521820608
    title: Andrew W. Appel and Jens Palsberg, Modern Compiler Implementation in Java, second edition
    locator: Section 3.2, Predictive Parsing (error recovery by skipping tokens); Section 3.5, Error Recovery (recovery with the error symbol)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 16, Error Handling
---

Panic-mode error recovery lets a parser go on after a syntax error so that one run can report many errors. When the parser detects an error, it discards input tokens until it finds a *synchronizing token*, such as a semicolon or a closing keyword, and it removes or completes the part of its stack that the error made useless, so that the synchronizing token can be read in a known state. It is the simplest recovery scheme, it never loops if it is set up to make progress, and it is the default in most [LL](/ll1-parsing/) and [LR](/lr-parse-table/) parsers.

## In plain words

When a reader meets a garbled sentence, she does not give up on the whole page. She skips to the next full stop and starts reading again from there. Panic mode does the same for a parser. On an error, it throws away tokens until one that usually starts or ends a piece of the program, like a semicolon or the word "end". It also forgets the half-finished piece it was working on, and pretends that piece was complete. Then it continues normally.

The skipped text may hide more errors, and the parser may complain about things that are fine once it is confused. But it always moves on, and it finds most errors in one run, which is what a programmer wants from a compiler.

## When it applies

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area. $\$$ is the end marker.

Panic mode fits any parser that detects an error at a definite token and keeps an explicit or implicit stack of goals: table-driven [LL(1) parsers](/ll1-parsing/), [recursive descent](/recursive-descent-parsing/) parsers, LR parsers driven by an [LR parse table](/lr-parse-table/), and [operator-precedence](/operator-precedence-parsing/) parsers. It needs a set of synchronizing tokens for each place where the parser can resume. These sets come from the grammar, usually from [FOLLOW and FIRST sets](/first-and-follow-sets/), plus a few tokens chosen by hand. It works best in languages whose statements and declarations are separated or closed by distinctive tokens, such as `;`, `}` or `end`.

## The template

1. **Detect.** The parser finds an error at the current token $b$: an empty table cell, or a terminal on the stack that does not match $b$.
2. **Report.** Record the error and its position.
3. **Choose a goal.** Pick a nonterminal $A$ that the parser is working on, together with its synchronizing set $\mathrm{SYNC}(A)$, typically $\mathrm{FOLLOW}(A)$, possibly with $\mathrm{FIRST}(A)$ and with tokens of enclosing constructs.
4. **Skip.** Discard input tokens until the current token is in $\mathrm{SYNC}(A)$ or is $\$$.
5. **Repair the stack.** If the token can follow $A$, pretend that $A$ has just been parsed: pop $A$ in an LL parser, or push the GOTO on $A$ in an LR parser. If the token can start $A$, restart $A$.
6. **Resume** normal parsing, and suppress new error messages until a few tokens have been read without error.

The scheme terminates if every recovery consumes at least one token or removes at least one stack entry. Steps 4 and 5 of the classic LL and LR forms below satisfy this, with the exception noted in the pitfalls.

## Classic examples

**LL(1) with synch entries.** For the [LL(1)](/ll1-parsing/) expression grammar $E \to T E'$, $E' \to + T E' \mid \varepsilon$, $T \to F T'$, $T' \to * F T' \mid \varepsilon$, $F \to ( E ) \mid id$, mark the empty cells $(A, b)$ of the [LL parse table](/ll-parse-table/) with $b \in \mathrm{FOLLOW}(A)$ as *synch*. Here $\mathrm{FOLLOW}(E) = \mathrm{FOLLOW}(E') = \{), \$\}$, $\mathrm{FOLLOW}(T) = \mathrm{FOLLOW}(T') = \{+, ), \$\}$ and $\mathrm{FOLLOW}(F) = \{+, *, ), \$\}$. The rules are:

- if the top of the stack is a terminal that does not match $b$, pop it (report it as missing);
- if the cell $(A, b)$ is synch, pop $A$;
- if the cell is empty and not synch, skip $b$;
- if $A$ is the last symbol above $\$$, do not pop it while input remains; skip instead.

On the input $) \ id * + \ id$, the parser takes these steps (stack top on the left):

| stack | input | action |
|---|---|---|
| $E \ \$$ | $) \ id * + \ id \ \$$ | error, skip $)$ |
| $E \ \$$ | $id * + \ id \ \$$ | $E \to T E'$, then on as usual |
| $* \ F \ T' \ E' \ \$$ | $* + \ id \ \$$ | match $*$ |
| $F \ T' \ E' \ \$$ | $+ \ id \ \$$ | error, $(F, +)$ is synch, pop $F$ |
| $T' \ E' \ \$$ | $+ \ id \ \$$ | $T' \to \varepsilon$, then on as usual |
| $\$$ | $\$$ | stop, 2 errors |

The parser reports a stray $)$ at token 0 and a missing operand at token 3, and it parses the rest normally.

**LR with a goal nonterminal.** For the statement list $L \to L ; S \mid S$, $S \to id = E$, $E \to E + id \mid id$, with the SLR table, choose the goal $S$ and $\mathrm{SYNC}(S) = \mathrm{FOLLOW}(S) = \{;, \$\}$. On an error, pop states until the top state has a GOTO on $S$, skip input until $;$ or $\$$, and push that GOTO. On $id = id \ id ; id = = ; id = id$ the parser finds the error at token 3 (the second $id$), pops back to the start state, skips that token, and pretends that a statement $S$ was parsed; it finds a second error at token 7 (the second $=$), pops to the state after $L ;$, skips it, and finishes. Two errors are reported and the last statement is parsed normally.

**The error token of yacc.** [yacc](/yacc/) and Bison let the grammar say where to synchronize, with productions such as $\mathit{stmt} \to \mathbf{error} \ ;$. On an error, the parser pops states until one has a shift on $\mathbf{error}$, shifts it, and then discards tokens until one can follow, here $;$. It reports new errors only after three tokens have been shifted. This is panic mode with the goals and synchronizing tokens written in the grammar.

**Recursive descent with stopper sets.** In a hand-written recursive descent parser, each parsing procedure gets as an argument the set of tokens that its callers can continue with. On an error, it skips tokens until one in its own FIRST set or in this set and returns. This is the scheme of Wirth's Pascal and Oberon compilers.

## Variations

- **Choice of synchronizing sets.** FOLLOW alone may be too small: a missing $;$ before a keyword that starts the next statement makes the parser skip the whole statement. Adding $\mathrm{FIRST}$ of the statement nonterminal, or the keywords that start statements, to the sets of the inner nonterminals lets the parser resume earlier.
- **Default to an empty production.** In an LL parser, a nonterminal with an $\varepsilon$-production can take it on any token instead of signaling an error. This delays the detection but never loses it, and it shrinks the number of states where recovery is needed.
- **Phrase-level recovery.** Instead of skipping, the parser repairs the input locally, by inserting, deleting or replacing a token, for example by inserting a missing $;$. Each empty table cell can point to its own repair routine. See [parser error recovery](/parser-error-recovery/).
- **Error productions.** Add productions for common mistakes to the grammar, so that they are parsed and reported precisely.
- **Global correction.** Find the smallest number of insertions and deletions that turn the input into a sentence. This is precise but costs much more than linear time, so production compilers do not use it.

## Pitfalls

- **Infinite loops.** If a recovery neither consumes a token nor shortens the stack, the parser can detect the same error again and again. In the LR form above, pushing the GOTO on $S$ and finding an error at the same token makes the parser pop back to the same state. Force progress: if no token has been shifted since the last recovery, discard the current token first.
- **Cascades of spurious errors.** After skipping, the parser may be in a state that does not match the program, and every following token looks wrong. Suppress messages until a few tokens have been shifted, as yacc does with its three tokens.
- **Skipping too much.** A small synchronizing set can discard large parts of the program, which hides real errors. Include tokens of enclosing constructs, such as `}` and `end`, in every set below them, so that recovery never skips past the end of a block.
- **Popping the start symbol.** If the goal is the start symbol, popping it on a token in its FOLLOW set leaves the rest of the input unparsed. Treat the outermost goal specially, as in the LL rule above.
- **Semantic actions on fake phrases.** The pretended nonterminal has no real value; code that builds a syntax tree must create a placeholder node and not crash on it.

## Exercises

1. For the LL(1) expression grammar above, trace the recovery on $id + * \ id$ and on $( id$. Which errors are reported, and at which tokens?
2. Give a grammar and an input on which the LR rule "pop until a GOTO on $S$, skip until $\mathrm{FOLLOW}(S)$, push" detects an error at the same token after the push. Show that discarding one token in that case guarantees termination.

## References
