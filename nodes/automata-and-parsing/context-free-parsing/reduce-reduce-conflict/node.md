---
tag: GD98NX
kind: concept
slug: reduce-reduce-conflict
name: Reduce-reduce conflict
aliases:
- R/R conflict
area: automata-and-parsing/context-free-parsing
level: core
summary: A parser state where two different productions can both be reduced on the same lookahead.
prereqs: [shift-reduce-parsing]
see_also: [shift-reduce-conflict, lalr-parsing, canonical-lr-parsing, slr-grammar, lalr-grammar, ambiguity, lr-parse-table, yacc]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.5.4, Conflicts During Shift-Reduce Parsing; Section 4.7.4, Constructing LALR Parsing Tables (merging states with a common core, and the reduce-reduce conflicts it can create)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Chapter 9, Deterministic Bottom-Up Parsing (LR(0), SLR(1), LR(1) and LALR(1) conflicts)
  - url: https://www.gnu.org/software/bison/manual/html_node/Reduce_002fReduce.html
    title: GNU Bison manual, Reduce/Reduce Conflicts
    locator: the default choice of the rule that appears first in the grammar
---

A reduce-reduce conflict is a state of a [shift-reduce parser](/shift-reduce-parsing/) in which, for the same next token, two different productions are complete on top of the stack and the parsing method allows reducing either. The parser cannot tell which nonterminal the symbols on top of the stack stand for. Like a [shift-reduce conflict](/shift-reduce-conflict/), it shows that the grammar is not in the class of the method. It comes from [ambiguity](/ambiguity/), from a lookahead that is too coarse, or, specific to [LALR(1) parsing](/lalr-parsing/), from merging LR(1) states that have the same items but different lookaheads.

## In plain words

A bottom-up parser combines the pieces on top of its stack into a larger piece named by a grammar rule. Sometimes two rules have the same right side, or one right side ends with another, and both fit the top of the stack. The parser must name the new piece, and the two rules give two different names.

Often the next token tells them apart: a name followed by `(` is a function, a name followed by `=` is a variable. A reduce-reduce conflict is a place where the next token is not enough, for the method in use, to decide which name is right. Tools such as yacc then pick the rule written first in the grammar and print a warning, which is rarely what the grammar writer meant.

## The idea

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size.

**Definition.** A state $I$ of an LR automaton has a reduce-reduce conflict on the lookahead $a$ if it contains two complete [items](/lr-item/) $[A \to \beta \cdot]$ and $[B \to \gamma \cdot]$ for different productions, and the method allows both reductions on $a$. Since both right sides end at the top of the stack, one of $\beta$ and $\gamma$ is a suffix of the other. The methods allow a reduction on $a$ as for shift-reduce conflicts: always in [LR(0)](/lr0-parsing/), when $a \in \text{FOLLOW}(A)$ in [SLR(1)](/slr-parsing/), when $a$ is in the merged lookahead set in LALR(1), and when the item carries $a$ in [canonical LR(1)](/canonical-lr-parsing/).

**Where they come from.**

1. **Ambiguity.** If two productions derive the same string in the same context, as in $S \to A \mid B$, $A \to x$, $B \to x$, every LR($k$) table has the conflict.
2. **Coarse lookahead.** SLR(1) uses $\text{FOLLOW}(A)$, which collects the tokens after $A$ in every context. Two nonterminals that are followed by different tokens in each context can still have overlapping FOLLOW sets.
3. **LALR merging.** LALR(1) merges the canonical LR(1) states with the same LR(0) items and takes the union of their lookaheads. This can create a reduce-reduce conflict that no LR(1) state has. It cannot create a new shift-reduce conflict: the shift moves depend only on the LR(0) items, so a shift-reduce conflict after merging was already present in one of the merged states.

**Resolution.** Yacc and Bison resolve a reduce-reduce conflict by reducing with the production that appears first in the grammar, and they report it. Precedence declarations do not apply. Since the choice by order silently makes one production unreachable in that context, a reduce-reduce conflict is usually fixed in the grammar, by merging the two nonterminals there and telling them apart later in semantic analysis, or by a stronger method.

## Examples

All tables and state counts below were computed by a script that builds the LR(0), SLR(1), LALR(1) and canonical LR(1) tables, with the augmented start item counted as a state.

**Resolved by FOLLOW.** $S \to A\, a \mid B\, b$, $A \to c$, $B \to c$. After $c$ the LR(0) state is $\{[A \to c \cdot], [B \to c \cdot]\}$, a reduce-reduce conflict on every token in LR(0). Since $\text{FOLLOW}(A) = \{a\}$ and $\text{FOLLOW}(B) = \{b\}$, the SLR(1) table reduces by $A \to c$ on $a$ and by $B \to c$ on $b$, with no conflict.

**Resolved by LALR but not SLR.** $S \to A\, a \mid B\, b \mid d\, A\, b \mid e\, B\, a$, $A \to c$, $B \to c$. Now $\text{FOLLOW}(A) = \text{FOLLOW}(B) = \{a, b\}$, so the SLR(1) table has a reduce-reduce conflict on $a$ and on $b$ in the state reached by $c$ at the start. But that state is reached only at the start, where $A$ is followed by $a$ and $B$ by $b$; after $d$ or $e$ the parser reaches other states with one complete item each. The LALR(1) and LR(1) tables, with 15 states, have no conflict.

**Created by LALR merging.** $S \to a\, A\, d \mid b\, B\, d \mid a\, B\, e \mid b\, A\, e$, $A \to c$, $B \to c$. The canonical LR(1) automaton has 14 states, among them

$$\{[A \to c \cdot, d],\ [B \to c \cdot, e]\} \text{ after } a\,c, \qquad \{[A \to c \cdot, e],\ [B \to c \cdot, d]\} \text{ after } b\,c,$$

and no conflict: the grammar is LR(1). The two states have the same core, so LALR(1) merges them into $\{[A \to c \cdot, \{d, e\}],\ [B \to c \cdot, \{d, e\}]\}$, with 13 states and a reduce-reduce conflict on $d$ and on $e$. The grammar is LR(1) but not LALR(1).

**Ambiguous.** $S \to A \mid B$, $A \to x$, $B \to x$ has the conflict on $\$$ in the state $\{[A \to x \cdot], [B \to x \cdot]\}$ in all four tables, since $x$ has two parse trees.

## Where it is used

- **Grammar debugging.** In a [yacc](/yacc/) or Bison grammar, a reduce-reduce conflict usually means that two nonterminals cover the same phrase, for example a type name and an expression that are both a plain identifier. The common fix merges them and decides later, with a symbol table.
- **Comparing LALR and LR.** The merging example is the standard proof that the [LALR(1) grammars](/lalr-grammar/) are a proper subclass of the LR(1) grammars, and that the difference consists only of reduce-reduce conflicts.
- **SLR versus LALR.** The FOLLOW examples show why LALR(1) accepts more grammars than [SLR(1)](/slr-grammar/).
- **Generalized parsing.** [GLR parsing](/glr-parsing/) follows both reductions of a conflict at once, which handles ambiguous and non-LR grammars.

## References
