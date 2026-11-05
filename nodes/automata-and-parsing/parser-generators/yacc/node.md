---
tag: NSTRHE
kind: algorithm
slug: yacc
name: Yacc
aliases:
- Yet Another Compiler-Compiler
- bison
area: automata-and-parsing/parser-generators
level: core
summary: The classic LALR(1) parser generator tool whose input grammars carry semantic actions.
solves: [parser-table-construction]
model: word-ram
complexity:
  vars: {n: the number of input tokens, Q: the number of LR(0) states, g: the grammar size, σ: the number of terminals}
  time: {build: O(Q g^3 σ^2), parse: O(n)}
  space: {table: O(Q g), parse: O(n)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1975
  people: [Stephen C. Johnson]
  note: Johnson's Bell Laboratories report describes yacc, which reads a grammar with actions, builds an LALR(1) table, settles ambiguities with precedence declarations and recovers from errors with the error token; GNU Bison is a later yacc-compatible generator.
prereqs: [lalr-parsing, shift-reduce-conflict, parsing-table]
see_also: [parser-generator, lalr-lookahead-computation, parser-error-recovery, reduce-reduce-conflict, operator-precedence-parsing, glr-parsing, parse-table-compression, syntax-directed-translation]
sources:
  - paper: "Stephen C. Johnson, Yacc: Yet Another Compiler-Compiler, Computing Science Technical Report No. 32, Bell Laboratories, Murray Hill, New Jersey, 1975"
    locator: sections Ambiguity and Conflicts, Precedence, and Error Handling (the default rules for conflicts, the precedence declarations, and the error token)
  - url: https://www.gnu.org/software/bison/manual/
    title: GNU Bison manual
    locator: chapter The Bison Parser Algorithm (sections Shift/Reduce Conflicts, Operator Precedence, Reduce/Reduce Conflicts, Tuning LR, Default Reductions) and chapter Error Recovery
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.7.5, Efficient Construction of LALR Parsing Tables (spontaneous and propagated lookaheads); Section 4.8, Using Ambiguous Grammars; Section 4.9, Parser Generators (Yacc, ambiguous grammars and error recovery in Yacc)
---

Yacc is the parser generator that reads a [context-free grammar](/context-free-grammar/) whose productions carry actions, builds an [LALR(1)](/lalr-parsing/) [parsing table](/parsing-table/) for it, and writes a parser that runs the table and computes a value for each phrase with those actions. Its algorithm has three parts: the LALR(1) construction by lookahead propagation, the resolution of conflicts by declared operator precedence and two default rules, and a driver that recovers from syntax errors through a special `error` token. Johnson wrote it at Bell Laboratories in the 1970s, and GNU Bison follows the same design.

## In plain words

You give yacc a grammar and, beside each rule, a short piece of code that says what the rule computes, such as "the value of a sum is the left value plus the right value". Yacc turns the grammar into a table and wraps it in a small program that reads tokens, keeps a stack, and runs your code each time it recognises a rule.

Some grammars leave the table two choices in one place, for example whether `1 + 2 * 3` means `(1 + 2) * 3`. Instead of rejecting such a grammar, yacc lets you say which operators bind tighter and in which direction they group, and settles the choice for you. It reports every choice it had to make without your help. When the input has a mistake, the parser can skip to a safe point, such as the next semicolon, and go on.

## The problem

**Notation.** A grammar is $G = (V, \Sigma, P, S)$ with productions written $A \to \alpha \mid \beta$, the empty string $\varepsilon$, start symbol $S$, input length $n$ and size $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$. The end marker is $\$$, and the augmented grammar adds $S' \to S$ as production 0. $Q$ is the set of states of the LR(0) automaton.

**Input.** A grammar in which each production $A \to X_1 \cdots X_k$ has an action $f$ that maps the values of $X_1, \ldots, X_k$ to the value of $A$ (by default the value of $X_1$), and a list of precedence declarations: lines `%left`, `%right` and `%nonassoc`, each naming terminals, from the lowest precedence to the highest. A production may name a terminal with `%prec` to take that terminal's precedence. A terminal `error` may appear in right sides.

**Output.** A deterministic table over the states of the LR(0) automaton, the report of the conflicts that precedence did not settle, and a driver that, on a token sequence, either accepts and returns the value of $S$, or reports syntax errors and recovers or stops.

When $G$ is LALR(1) and declares no precedence, the parser accepts exactly $L(G)$ and its value is the action applied bottom-up over the unique parse tree. When $G$ has conflicts, the table chooses one action per cell, and the parser accepts a subset of $L(G)$ with one tree for each accepted sentence.

## The algorithm

```pseudo id=main
YACC(G, precedence)
L1  build the LR(0) automaton of the augmented grammar: kernels, closure, GOTO
L2  for each kernel item i of each state s: close {[i, #]}; a lookahead a ≠ # after X is spontaneous for the kernel item of GOTO(s, X), and # links i to it
L3  start from $ on [S' → ·S] and the spontaneous lookaheads; copy along the links until no set grows
L4  for each state, add shift on terminal transitions and reduce A → α on each lookahead of a completed item; reduce by S' → S on $ is accept
L5  for each cell with a shift and a reduce by a rule p where the token and p both have precedence: the higher wins; on equal precedence, left keeps the reduce, right keeps the shift, nonassoc keeps neither
L6  if a shift and a reduce are still left: keep the shift and report a shift-reduce conflict
L7  if several reduces are left: keep the rule that comes first in the grammar and report a reduce-reduce conflict
PARSE(tokens)
L8  repeat: x ← the default reduction of the top state if it has one, else ACTION[top state, next token]
L9      shift q: push q with the token's value; if errors are being suppressed, count one shifted token
L10     reduce A → X1 … Xk: pop k states and values, push GOTO[exposed state, A] with f(values)
L11     accept: return the value on top of the stack
L12     error: report it unless fewer than 3 tokens were shifted since the last recovery (if none was, discard the token, or stop at $); pop states until one can shift error, shift it
```

**The lookaheads (L1 to L3).** The table has one state per LR(0) state, as in [LALR(1) parsing](/lalr-parsing/), and the reduce lookaheads are those that the canonical LR(1) items with the same core would have. Line L2 finds them without building the LR(1) collection: closing a kernel item with a dummy lookahead $\#$ shows, for each successor kernel item, which lookaheads arise inside the state (spontaneous) and whether the lookaheads of the item itself are passed on (a link). Line L3 is a fixed point over the links. This is the propagation method of the Dragon book, Section 4.7.5; the relations of DeRemer and Pennello compute the same sets faster, see [LALR lookahead computation](/lalr-lookahead-computation/).

**Precedence (L5).** Each rule takes the precedence of the last terminal in its right side, or the terminal named by `%prec`. In a cell where the table could shift the token $a$ or reduce by the rule $p$, the one with higher precedence wins: if $a$ is higher, shift; if $p$ is higher, reduce. On equal precedence, `%left` means reduce, `%right` means shift and `%nonassoc` means a syntax error. If $a$ or $p$ has no precedence, the cell is left to the default rules. A conflict settled this way is not reported as a conflict (Bison manual, How Precedence Works).

**Default rules (L6, L7).** A remaining shift-reduce conflict is settled for the shift, a reduce-reduce conflict for the rule that appears first in the grammar. Both are reported (Bison manual, Shift/Reduce Conflicts and Reduce/Reduce Conflicts). When a cell has a shift and several reductions, this implementation applies L5 to each reduction in grammar order and then L6.

**The driver (L8 to L11).** It is the shift-reduce loop of the [LR parser](/lr-parsing/) with a value stack beside the state stack. A state whose only action is one reduction reduces without looking at the next token, a *default reduction*; Bison uses default reductions too, and its `lr.default-reduction` setting chooses in which states (Bison manual, Default Reductions).

**Error recovery (L12).** When the table has no action, the parser reports a syntax error, then pops states until the top state has a shift on `error`, shifts `error`, and tries the same token again. If that token still cannot be used, it is discarded and the parser pops back to the state after `error` for the next token, so tokens are skipped until one can follow `error`. No new message is printed until three tokens have been shifted after a recovery; a stack with no state that shifts `error` ends the parse. This is the procedure in the Bison manual, Error Recovery; its `yyerrok` action, which ends the quiet period at once, is not modelled.

## Example

**Spec.** The grammar $E \to E + E \mid E * E \mid (\,E\,) \mid \mathit{num}$, productions 1 to 4, with actions for the sum and the product and the declarations `%left '+'` then `%left '*'`, so $*$ has the higher precedence. The LR(0) automaton has 10 states.

**Lookaheads.** Closing $[E' \to \cdot E,\ \#]$ in state 0 gives the items $[E \to \cdot E + E]$ and $[E \to \cdot E * E]$ with the lookaheads $+$, $*$ and $\#$. So in state 1, the GOTO on $E$, the kernel items $E \to E \cdot + E$ and $E \to E \cdot * E$ get $+$ and $*$ spontaneously and $\$$ by propagation from $E' \to \cdot E$. After L3, every completed item has the lookaheads $\{+, *, ), \$\}$.

**Conflicts.** Four cells hold a shift and a reduce, all settled by L5:

| state | kernel items | token | candidates | kept | why |
|---|---|---|---|---|---|
| 7 | $E \to E + E \cdot$, $E \to E \cdot + E$, $E \to E \cdot * E$ | $+$ | shift 4, reduce 1 | reduce 1 | equal precedence, `%left` |
| 7 | the same | $*$ | shift 5, reduce 1 | shift 5 | $*$ is higher than rule 1 |
| 8 | $E \to E * E \cdot$, $E \to E \cdot + E$, $E \to E \cdot * E$ | $+$ | shift 4, reduce 2 | reduce 2 | rule 2 is higher than $+$ |
| 8 | the same | $*$ | shift 5, reduce 2 | reduce 2 | equal precedence, `%left` |

No conflict is reported. After resolution state 8 reduces on every token, so it, state 3 ($E \to \mathit{num} \cdot$) and state 9 ($E \to (\,E\,) \cdot$) get default reductions.

**Trace of $2 + 3 * 4$.**

| state stack | values | next token | action |
|---|---|---|---|
| 0 | | 2 | shift 3 |
| 0 3 | 2 | $+$ | default reduce 4, GOTO 1 |
| 0 1 | 2 | $+$ | shift 4 |
| 0 1 4 | 2 + | 3 | shift 3 |
| 0 1 4 3 | 2 + 3 | $*$ | default reduce 4, GOTO 7 |
| 0 1 4 7 | 2 + 3 | $*$ | shift 5 |
| 0 1 4 7 5 | 2 + 3 * | 4 | shift 3 |
| 0 1 4 7 5 3 | 2 + 3 * 4 | $\$$ | default reduce 4, GOTO 8 |
| 0 1 4 7 5 8 | 2 + 3 * 4 | $\$$ | default reduce 2: $3 \cdot 4 = 12$, GOTO 7 |
| 0 1 4 7 | 2 + 12 | $\$$ | reduce 1: $2 + 12 = 14$, GOTO 1 |
| 0 1 | 14 | $\$$ | accept, value 14 |

**Recovery.** Add $L \to L\,S \mid \varepsilon$, $S \to E\ ; \mid \mathtt{error}\ ;$ above the expressions, with $L$ collecting the values of its statements and $S \to \mathtt{error}\ ;$ giving the value ERR. On $1 + ;\ 2\ ;$ the parser finds no action for $;$ after $1 +$ and reports an error at token 2. It pops the states of $+$ and of $E$, reaches the state after $L$, which shifts `error`, and then shifts the $;$, reduces $S \to \mathtt{error}\ ;$ and goes on. The result is the list [ERR, 2].

## Correctness

The proof in [correctness](proofs/correctness.md) shows that lines L1 to L4 give each completed item of each LR(0) state exactly the lookaheads that the canonical LR(1) items with the same core have, so the table before resolution is the LALR(1) table. It shows that L5 to L7 keep one action per cell by the stated rules, and that for an LALR(1) grammar the parser with default reductions accepts exactly $L(G)$ and never shifts a token $a_j$ for which $a_1 \cdots a_j$ is not a prefix of a sentence, so its first error is reported at that token. The tests compare the table with canonical LR(1) states merged by core on random grammars, the parser with the language up to length 5, the values of operator expressions with the unique parse tree that obeys the precedence rules, and the recovery with a statement-by-statement reference.

## Complexity

- **Construction.** The LR(0) automaton can have exponentially many states in $|G|$ (see [LR item sets](/lr-item-sets/)), so the cost is stated per state. The implementation here closes each kernel item with a set of lookaheads: at most $|G|$ items, each processed at most $|\Sigma| + 2$ times, each time at cost $O(|G| \cdot |\Sigma|)$, so $O(|G|^2 |\Sigma|^2)$ per kernel item and $O(|Q| \cdot |G|^3 \cdot |\Sigma|^2)$ overall. The propagation fixpoint costs $O(|\Sigma|)$ per link and per growth, and is dominated by the closures. The DeRemer and Pennello method computes the same lookaheads in time linear in the size of its relations times $|\Sigma|$.
- **Resolution.** One pass over the cells: $O(|Q| \cdot (|\Sigma| + 1))$ cells, each with at most one shift and $|P|$ reductions.
- **Parsing.** $O(n)$ time and stack space on a conflict-free LALR(1) table: each token is shifted once, and each reduction builds one internal node of the parse tree, which has $O(n)$ nodes because a reduced LALR(1) grammar is unambiguous and so has no derivation $A \Rightarrow^+ A$. Recovery adds at most one discarded token per error and pops at most the current stack.

## Properties

- **Deterministic and online.** The parser reads each token once, from left to right, and decides with one token of lookahead; with default reductions it sometimes decides with none.
- **Correct prefix.** For an LALR(1) grammar the parser never shifts a token that makes the input read so far a non-prefix of $L(G)$: errors are found at the earliest token, though some reductions may be done first.
- **No recursion.** The parser uses an explicit stack, so deeply nested input does not exhaust a call stack.
- **Values bottom-up.** Each action runs when its rule is reduced, after the actions of all symbols of its right side: a synthesized attribute evaluation, as in [syntax-directed translation](/syntax-directed-translation/).

## Variants and improvements

- **Bison table types.** Bison builds LALR(1) by default and, through `%define lr.type`, IELR(1) or canonical LR(1) tables, which remove the extra reduce-reduce conflicts that merging can create (Bison manual, LR Table Construction).
- **GLR.** With `%glr-parser`, Bison keeps the conflicting actions and runs them in parallel, a [GLR parser](/glr-parsing/).
- **Lookahead correction.** Bison's `%define parse.lac full` checks on a copy of the stack that the token can be shifted before it does default reductions, which keeps the stack intact for recovery and error messages; see [parser error recovery](/parser-error-recovery/).
- **Table compression.** Real generators store the table with default reductions and packed rows; see [parse table compression](/parse-table-compression/).
- **Faster lookaheads.** The DeRemer and Pennello relations replace the propagation of L2 and L3; see [LALR lookahead computation](/lalr-lookahead-computation/).

## When to use it

Use yacc or Bison when the language has a stable grammar that is LALR(1) or close to it, and operator expressions are a large part of it: precedence declarations keep the grammar short, and the conflict report is a check on every change. Prefer a hand-written [recursive descent](/recursive-descent-parsing/) or [Pratt](/pratt-parsing/) parser when error messages and recovery must be precise, and a [GLR](/glr-parsing/) or [Earley](/earley-parser/) parser when the grammar is far from LALR(1).

## Pitfalls

- **Ignoring the conflict report.** The default shift and the earlier-rule choice silently change the language. In $S \to A\,b$, $A \to a \mid a\,b$ the shift makes the sentence $a\,b$ unparsable; see [parser generator](/parser-generator/). Bison's `%expect n` declares how many shift-reduce conflicts the author expects, so that a new one is noticed.
- **Precedence on the wrong rule.** A rule takes the precedence of its last terminal. Unary minus written $E \to -\,E$ gets the precedence of binary minus unless `%prec` gives it a higher one, and then $-2 \wedge 3$ or $-2 * 3$ groups in a way the author did not mean.
- **Precedence hides real ambiguity.** Declarations settle every shift-reduce conflict that involves a declared token, including ones unrelated to operators, so a broad declaration can hide a mistake in the grammar.
- **Error rules that create conflicts.** An `error` production in the wrong place adds conflicts, and a recovery that resumes at a token that occurs everywhere can produce cascades of messages.
- **Actions with side effects.** Default reductions and lookahead mean that an action may run before or after the parser reads the next token, so actions that talk to the lexer must not depend on exactly when they run.

## Implementations

## History

Johnson developed yacc at Bell Laboratories in the early 1970s and described it in Computing Science Technical Report 32 (1975); it was distributed with Unix and made LALR(1), precedence declarations and the `error` token the standard toolkit of parser generators. The LALR method itself is due to DeRemer (1969), and the propagation method of computing its lookaheads is the one presented in the Dragon book. GNU Bison, written later, is upward compatible with yacc and adds the other table types, GLR parsing and lookahead correction described in its manual.

## References
