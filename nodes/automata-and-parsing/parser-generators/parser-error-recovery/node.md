---
tag: 5NTR4T
kind: technique
slug: parser-error-recovery
name: Parser error recovery
aliases:
- syntax error recovery
- panic mode recovery
- phrase-level recovery
area: automata-and-parsing/parser-generators
level: intro
summary: Strategies such as panic mode and phrase-level repair that let a parser continue and report several syntax errors.
prereqs: [lr-parsing, ll1-parsing, first-and-follow-sets]
see_also: [panic-mode-error-recovery, yacc, parsing-table, ll-parse-table, lr-parse-table, edit-distance, earley-parser, parser-generator]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.1.3, Syntax Error Handling; Section 4.1.4, Error-Recovery Strategies; Section 4.4.5, Error Recovery in Predictive Parsing; Section 4.8.3, Error Recovery in LR Parsing
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 16, Error Handling
  - url: https://www.gnu.org/software/bison/manual/html_node/Error-Recovery.html
    title: GNU Bison manual, Error Recovery
    locator: the error token, the discarding of states and tokens, the suppression of messages, yyerrok and yyclearin
  - paper: "Alfred V. Aho and Thomas G. Peterson, A minimum distance error-correcting parser for context-free languages, SIAM Journal on Computing 1(4) (1972)"
    locator: the whole paper (the least number of insertions, deletions and replacements that turn the input into a sentence, in time cubic in the input length)
  - paper: "Michael G. Burke and Gerald A. Fisher, A practical method for LR and LL syntactic error diagnosis and recovery, ACM Transactions on Programming Languages and Systems 9(2) (1987)"
    locator: the whole paper (deferred parsing, simple and scope recovery tried on a window of tokens)
---

Parser error recovery is the set of methods that let a parser go on after a syntax error, so that one run reports many errors instead of stopping at the first. A deterministic parser such as an [LL(1)](/ll1-parsing/) or [LR](/lr-parsing/) parser detects an error at the first token where its [parsing table](/parsing-table/) has an empty entry; recovery then changes the parser's stack, the remaining input, or both, until the table again has an entry. The main methods are panic mode, phrase-level repair, error productions such as the `error` token of [yacc](/yacc/), and global minimum-distance correction.

## In plain words

A parser reads tokens one at a time and knows, at each step, which tokens may come next. When the next token is not one of them, the input has an error. Stopping there is easy but unhelpful: a programmer wants to see all the mistakes in a file at once.

So the parser makes a guess about what went wrong and patches its own state to get going again. The crudest guess throws away tokens until it reaches one that usually starts or ends a statement, such as a semicolon or a closing brace. A finer guess pretends that one token was missing or extra. The art is to patch so that the parser does not trip over the same mistake again and print a flood of false errors.

## When it applies

- A table-driven or recursive descent parser with the *valid prefix property*: it reports an error at the first token $a_i$ such that $a_1 \cdots a_i$ is not a prefix of any sentence. Canonical LR(1) and LL(1) parsers have it. LALR(1) and SLR(1) parsers may first make some reductions on the bad token, but they never shift it, so the error is still found before the token is consumed.
- The language has *synchronizing tokens*: tokens that end or start a construct, such as `;`, `}` or `end`, which the parser can use as safe places to restart.
- The goal is diagnosis, not a guess at the program's meaning. A compiler that has recovered from an error still refuses to produce code.

## The template

The parser calls RECOVER when the entry of its table for the current state and the current token $a$ is empty. The names in capitals after the word "hole" are the choices that make a concrete method.

```pseudo id=main
RECOVER(stack, input)                     ▷ called on an empty table entry
L1  if not SUPPRESSED then REPORT(the current token)
L2  choose a method:                        ▷ hole: the METHOD
L3      panic mode: skip input tokens until a token in SYNC(top of stack); pop the stack until its top can continue on that token
L4      phrase level: among the local edits (insert, delete or replace one token) choose the edit of least COST after which the parser can shift K more tokens; apply it
L5      error production: pop states until one can shift the token error; shift it; skip input tokens until one has a table entry
L6  SUPPRESSED ← true until K tokens have been shifted   ▷ hole: K
L7  continue the normal parse loop
```

The holes are the set $\mathrm{SYNC}$ of synchronizing tokens for each stack top, the cost of an edit, the number $K$ of tokens that must be shifted before the parser trusts itself again, and the choice of method. Line L6 is what stops one real error from producing a cascade of reports.

**Termination.** Each pass through RECOVER must make progress, or the parser loops. Panic mode must pop at least one stack symbol or skip at least one token in each step. An insertion repair consumes nothing, so a phrase-level method must refuse a second insertion at the same input position. Exercise 2 asks for a measure that proves termination for the LL(1) rules below.

## Classic examples

**Panic mode in an LL(1) parser.** Take the LL(1) expression grammar $E \to T E'$, $E' \to + T E' \mid \varepsilon$, $T \to F T'$, $T' \to * F T' \mid \varepsilon$, $F \to (\,E\,) \mid \mathit{id}$ and let $\mathrm{SYNC}(A) = \mathrm{FOLLOW}(A)$, the [FOLLOW set](/first-and-follow-sets/) of each nonterminal. The rules are: if $M[A, a]$ is empty and $a \in \mathrm{SYNC}(A)$, pop $A$; if it is empty and $a \notin \mathrm{SYNC}(A)$, skip $a$; if a terminal on top does not match $a$, pop it. On the input $\mathit{id} * + \mathit{id}$, with a missing operand:

| stack (top first) | input | action |
|---|---|---|
| $E$ | $\mathit{id} * + \mathit{id}\ \$$ | $E \to T E'$ |
| $T\ E'$ | $\mathit{id} * + \mathit{id}\ \$$ | $T \to F T'$ |
| $F\ T'\ E'$ | $\mathit{id} * + \mathit{id}\ \$$ | $F \to \mathit{id}$ |
| $\mathit{id}\ T'\ E'$ | $\mathit{id} * + \mathit{id}\ \$$ | match $\mathit{id}$ |
| $T'\ E'$ | $* + \mathit{id}\ \$$ | $T' \to * F T'$ |
| $*\ F\ T'\ E'$ | $* + \mathit{id}\ \$$ | match $*$ |
| $F\ T'\ E'$ | $+ \mathit{id}\ \$$ | error; $+ \in \mathrm{FOLLOW}(F)$, pop $F$ |
| $T'\ E'$ | $+ \mathit{id}\ \$$ | $T' \to \varepsilon$ |
| $E'$ | $+ \mathit{id}\ \$$ | $E' \to + T E'$ |
| $+\ T\ E'$ | $+ \mathit{id}\ \$$ | match $+$ |
| $T\ E'$ | $\mathit{id}\ \$$ | $T \to F T'$, then $F \to \mathit{id}$, match, $T' \to \varepsilon$, $E' \to \varepsilon$ |
| (empty) | $\$$ | accept |

The parser reports one error and acts as if the missing operand were there. On $(\,\mathit{id}\ \mathit{id}\,) * \mathit{id}$ it reports one error at the second $\mathit{id}$, which is in no SYNC set of $T'$, skips it, and finishes. The [panic-mode error recovery](/panic-mode-error-recovery/) page studies the choice of SYNC sets.

**A cascade.** On $\mathit{id} + )\ \mathit{id}$ the same rules report three errors: the parser pops $T$ on $)$, which is in $\mathrm{FOLLOW}(T)$, and then the stack is empty, so it skips $)$ and then $\mathit{id}$. The input has one mistake, a stray $)$ that one deletion removes, but the recovery left the parser out of step with the input. Rule L6 hides the second and third reports.

**The error token of yacc and Bison.** A grammar for a statement list can contain the production $\mathit{stmt} \to \mathtt{error}\ ;$. On a syntax error, the Bison parser pops states until it reaches a state that can shift the special token `error`, shifts it, and then discards input tokens until it finds one that it can shift, here `;`. It reports no new error until three tokens have been shifted, and the action `yyerrok` ends this quiet period at once (GNU Bison manual, Error Recovery). The [yacc](/yacc/) page gives the full algorithm.

**Phrase-level repair in an LR parser.** On an empty entry, try each single-token insertion, deletion and replacement at the error point, run the parser forward on a copy of the stack for a few tokens, and keep the first edit, in a fixed order of cost, with which the parser gets furthest. Burke and Fisher defer the shifts of a small window of tokens so that the repair can also be made a few tokens before the point where the error was detected.

**Global minimum-distance correction.** Find a sentence $y \in L(G)$ that minimizes the [edit distance](/edit-distance/) between the input and $y$, counting insertions, deletions and replacements of tokens. Aho and Peterson (1972) solve this exactly for every context-free grammar with a variant of the [Earley parser](/earley-parser/) on a grammar extended with error productions, in time cubic in the input length. On $\mathit{id} * + \mathit{id}$ the distance is 1: deleting $+$ gives $\mathit{id} * \mathit{id}$, and the input itself is not a sentence. The method is exact but too slow for routine use; it is the yardstick for the heuristics above.

## Variations

- **SYNC sets from the grammar.** FOLLOW sets alone are too small in practice: a missing `;` after an expression makes the parser skip the keyword that starts the next statement. Adding the FIRST sets of higher constructs, or the keywords that start statements, gives better restart points.
- **Error productions.** The grammar author adds productions for common mistakes, such as a missing `;`, and the action prints a precise message. Yacc's `error` token is the general form of this idea.
- **Lookahead correction.** In an LALR(1) parser, default reductions can make the parser reduce on a bad token before it finds the error, which changes the state from which recovery starts. Bison's LAC option (`%define parse.lac full`) first checks, on a copy of the stack, that the token can be shifted after these reductions, and treats it as an error at once when it cannot.
- **Recovery in recursive descent.** Each parsing function receives the set of tokens that its callers can accept, and on an error skips to a token in the union of that set and its own FIRST set. This is panic mode with SYNC sets passed as arguments.
- **Repair for tools.** An editor wants a tree for every input. Error-tolerant parsers insert "missing" nodes and wrap skipped tokens in "error" nodes, so that later passes still run; this is phrase-level repair whose edits are recorded in the tree.

## Pitfalls

- **Infinite loops.** A recovery step that neither consumes a token nor pops the stack can repeat forever. In the LL(1) rules above, when the top of the stack is the bottom marker the parser must skip the token, not pop the marker.
- **Cascades of false errors.** Without line L6, a single missing token can produce many reports, as in the cascade example. Suppress reports until $K$ tokens have been shifted; Bison uses $K = 3$.
- **Recovery that changes the result silently.** After recovery the tree or the computed value is a guess. A compiler must mark the run as failed even if every later token parses.
- **Synchronizing on a token that the stack cannot use.** If the skipped-to token has no entry for any state left on the stack, panic mode empties the stack and the rest of the input is lost. Keep the start symbol, or a statement-level state, on the stack as a floor.
- **Default reductions hide the error point.** In an SLR or LALR table compressed with default reductions, the error is found after some reductions, so the stack at the error no longer shows the construct the user was writing, and the message names the wrong construct.

## Exercises

1. For the LL(1) expression grammar above, give the actions of panic mode with $\mathrm{SYNC}(A) = \mathrm{FOLLOW}(A)$ on the input $)\ \mathit{id} * \mathit{id}$. How many errors does it report?
2. Show that the LL(1) panic-mode rules above always terminate: find a quantity that drops by at least 1 at each error step and does not grow at the other steps by more than the number of tokens consumed.
3. Give a grammar and an input for which phrase-level repair by single-token insertion, without the rule against a second insertion at the same place, loops forever.
4. Compute by brute force the minimum edit distance from $(\,(\,\mathit{id} + )$ to a sentence of the expression grammar. Which repairs reach it?
5. Write the production with the `error` token that lets a yacc parser for a list of statements $L \to L\ S \mid S$, $S \to \mathit{id} = E\ ;$ skip a bad statement up to the next `;`.

## References
