---
tag: MG8Q5D
kind: concept
slug: shift-reduce-conflict
name: Shift-reduce conflict
aliases:
- S/R conflict
area: automata-and-parsing/context-free-parsing
level: core
summary: A parser state where both shifting and reducing are valid actions for the next token.
prereqs: [shift-reduce-parsing]
see_also: [reduce-reduce-conflict, slr-grammar, lalr-parsing, canonical-lr-parsing, ambiguity, lr-parse-table, yacc, operator-precedence-parsing]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.5.4, Conflicts During Shift-Reduce Parsing; Section 4.6.4, Constructing SLR-Parsing Tables (Example 4.48); Section 4.8.1, Precedence and Associativity to Resolve Conflicts; Section 4.8.2, The Dangling-Else Ambiguity
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Chapter 9, Deterministic Bottom-Up Parsing (LR(0), SLR(1), LR(1) and LALR(1) conflicts, and conflict resolvers)
  - url: https://www.gnu.org/software/bison/manual/html_node/Shift_002fReduce.html
    title: GNU Bison manual, Shift/Reduce Conflicts
    locator: the dangling else, and the default choice of shifting
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (LR(k) grammars and the test for them)
---

A shift-reduce conflict is a state of a [shift-reduce parser](/shift-reduce-parsing/) in which, for the same next token, the parsing method allows both moves: shift the token, or reduce a complete right side on top of the stack. A parser generator that builds an LR table reports one for each such pair (state, token). The conflict means that the grammar is not in the class of the method (LR(0), SLR(1), LALR(1) or LR(1)). It comes either from [ambiguity](/ambiguity/), as in the dangling else, or from a lookahead that is too short or too coarse for the grammar.

## In plain words

A bottom-up parser holds the pieces it has read on a stack. At some moments the top of the stack forms a complete grammar rule, and the parser may combine it now, or it may read the next token first in the hope of building something larger. Usually one token of lookahead settles the question.

A shift-reduce conflict is a place where it does not. In `if c then if d then x else y`, after `if d then x` the parser sees `else`. Combining now would give the `else` to the outer `if`; reading on gives it to the inner one. The grammar allows both, so no lookahead can decide. Tools such as yacc then pick "read on" and print a warning, or follow precedence rules that the grammar writer declares.

## The idea

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size. An [LR item](/lr-item/) $[A \to \alpha \cdot \beta]$ marks how much of a right side is on the stack.

**Definition.** Let $I$ be a state of an LR automaton, a set of items. $I$ has a shift-reduce conflict on the terminal $a$ if it contains

- a complete item $[A \to \beta \cdot]$ whose reduction is allowed on $a$, and
- an item $[B \to \alpha \cdot a \gamma]$, which calls for shifting $a$.

When the reduction is "allowed on $a$" depends on the method:

| method | reduce $A \to \beta$ on $a$ when |
|---|---|
| [LR(0)](/lr0-parsing/) | always (no lookahead) |
| [SLR(1)](/slr-parsing/) | $a \in \text{FOLLOW}(A)$ |
| [LALR(1)](/lalr-parsing/) | $a$ is in the LALR lookahead set of the item in $I$ |
| [canonical LR(1)](/canonical-lr-parsing/) | the item is $[A \to \beta \cdot, a]$ |

The lookahead sets shrink from top to bottom, so a conflict in LR(1) is a conflict in LALR(1), SLR(1) and LR(0). The reverse fails: each method removes some conflicts of the one above it. A grammar is LR(1), in the sense of Knuth, exactly when its canonical LR(1) table has no conflict of either kind ([reduce-reduce conflicts](/reduce-reduce-conflict/) are the other kind).

**Two sources.**

1. **Ambiguity.** An LR($k$) grammar is unambiguous, so an ambiguous grammar has a conflict, of this kind or the reduce-reduce kind, in the LR($k$) table for every $k$. If a sentence has two parse trees, then at the first point where the two reverse rightmost derivations differ, the parser sees the same stack and the same input, and one tree reduces while the other shifts or reduces differently.
2. **Not enough lookahead.** An unambiguous grammar can have conflicts too: for the method (SLR merges contexts that LR(1) keeps apart), or for every $k$ (the grammar is not LR($k$) at all, though its language may be).

**Resolution.** A conflict can be removed by rewriting the grammar, by using a stronger method, or by a rule that picks one action. Yacc and Bison pick **shift** by default and report the number of conflicts. With precedence declarations they compare the precedence of the production (that of its last terminal) with that of the token: the higher one wins (reduce if the production's is higher, shift if the token's is), and on a tie the associativity decides, `%left` reducing, `%right` shifting, and `%nonassoc` making the pair an error. This lets a short ambiguous expression grammar replace a long unambiguous one.

## Examples

**The dangling else.** $S \to i\, E\, t\, S \mid i\, E\, t\, S\, e\, S \mid a$, $E \to b$, where $i$, $t$, $e$ stand for `if`, `then`, `else`. The LR(0) automaton has 10 states, one of them

$$\{\, [S \to i E t S \cdot],\ [S \to i E t S \cdot e S] \,\}.$$

Since $e \in \text{FOLLOW}(S)$, it has a shift-reduce conflict on $e$ in the SLR(1) and LALR(1) tables, and the canonical LR(1) automaton, with 17 states, has the same conflict. This is unavoidable: $i\,b\,t\,i\,b\,t\,a\,e\,a$ has two parse trees. Choosing shift attaches the $e$ to the nearest $i$; an LR parser that resolves the conflict by shifting returns the tree in which the inner statement is $i\,b\,t\,a\,e\,a$, which is the rule of C, Java and Pascal.

**An ambiguous expression grammar.** $E \to E + E \mid E * E \mid \mathtt{id}$ has 7 LR(0) states, and the state after $E + E$ contains $[E \to E + E \cdot]$, $[E \to E \cdot + E]$ and $[E \to E \cdot * E]$. On $+$ and on $*$ both moves are possible, and the same holds after $E * E$: four conflicts in the SLR(1), LALR(1) and LR(1) tables. Declaring `%left '+'` and then `%left '*'` (later lines bind tighter) resolves them: after $E + E$, reduce on $+$ and shift on $*$; after $E * E$, reduce on both. The parser then reads $\mathtt{id} + \mathtt{id} * \mathtt{id} + \mathtt{id}$ as $(\mathtt{id} + (\mathtt{id} * \mathtt{id})) + \mathtt{id}$.

**A conflict of SLR only.** The grammar $S \to L = R \mid R$, $L \to * R \mid \mathtt{id}$, $R \to L$ (assignments with pointers) is unambiguous. Its LR(0) automaton has the state $\{[S \to L \cdot = R],\ [R \to L \cdot]\}$. Since $\text{FOLLOW}(R) = \{=, \$\}$, the SLR(1) table both shifts and reduces on $=$. But a stack $L$ at the start of a statement can only be followed by $=$ if it is the left side of an assignment, and the LR(1) item is $[R \to L \cdot, \$]$: the canonical LR(1) table (14 states) and the LALR(1) table (10 states) have no conflict.

**No $k$ is enough.** $S \to a\, S\, a \mid a$ generates the odd-length strings $a^{2m+1}$ and is unambiguous. After reading some $a$'s with more $a$'s ahead, the parser must reduce $S \to a$ exactly at the middle of the input, which it cannot locate by looking $k$ tokens ahead. So the state $\{[S \to a \cdot S a], [S \to a \cdot], [S \to \cdot a S a], [S \to \cdot a]\}$ has a shift-reduce conflict on $a$ for every $k$; the canonical LR(1) automaton has 8 states and this conflict. The same language has the SLR(1) grammar $S \to a\, a\, S \mid a$: the problem is the grammar, not the language.

The tables and state counts above were computed by a script that builds the LR(0), SLR(1), LALR(1) and LR(1) tables.

## Where it is used

- **Grammar checking.** Parser generators such as [yacc](/yacc/) and Bison report shift-reduce conflicts with the state and the items involved; the count of expected conflicts can be declared with `%expect`.
- **Precedence declarations.** The precedence and associativity rules of yacc exist to resolve shift-reduce conflicts in expression grammars, as [operator precedence parsing](/operator-precedence-parsing/) does with its relations.
- **Comparing methods.** The grammars that are [SLR(1)](/slr-grammar/), LALR(1) and LR(1) are defined as those without conflicts in the corresponding tables.
- **Generalized parsing.** [GLR parsing](/glr-parsing/) keeps the conflicts and follows both actions; this is how it parses ambiguous grammars.
- **Language design.** The dangling else is resolved by the shift rule in C and Java, and avoided by an explicit end keyword in other languages.

## References
