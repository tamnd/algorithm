---
tag: 3BR4GX
kind: concept
slug: bottom-up-parsing
name: Bottom-up parsing
area: automata-and-parsing/context-free-parsing
level: core
summary: Builds the parse tree from the leaves by reducing substrings to nonterminals.
prereqs: [context-free-grammar, parse-tree, derivation, pushdown-automaton]
see_also: [top-down-parsing, shift-reduce-parsing, handle, viable-prefix, lr-parsing, canonical-lr-parsing, operator-precedence-parsing, cyk-algorithm]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.5, Bottom-Up Parsing (4.5.1 Reductions, 4.5.2 Handle Pruning, 4.5.3 Shift-Reduce Parsing, 4.5.4 Conflicts During Shift-Reduce Parsing)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 3, Introduction to Parsing (top-down and bottom-up), Chapter 7, General Directional Bottom-Up Parsing, and Chapter 9, Deterministic Bottom-Up Parsing
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (handles, LR(k) grammars, and the deterministic bottom-up parser)
---

Bottom-up parsing builds the [parse tree](/parse-tree/) of a string from its leaves to its root: it repeatedly finds a substring that matches the right side of a production and replaces it by the left side, until only the start symbol is left. The replacements, read backwards, form a rightmost [derivation](/derivation/) of the input. The usual form is [shift-reduce parsing](/shift-reduce-parsing/), with a stack that holds the part of the tree built so far. The deterministic bottom-up methods, above all [LR parsing](/lr-parsing/), are the ones used by parser generators such as [yacc](/yacc/).

## In plain words

Think of the tokens of the input as the leaves of a tree that you must grow upwards. You read the tokens from left to right and put them on a stack. From time to time, the top of the stack is exactly the right side of a grammar rule, such as "expression plus term". Then you can take those pieces off and put one new piece, "expression", in their place. This is a reduction: it makes a new node of the tree with the old pieces as children.

The parser has two moves: shift the next token onto the stack, or reduce the top of the stack. The input is correct when, at the end, the stack holds one piece, the start symbol of the grammar. The hard part is to know which move to make. A reduction that fits now can be wrong later.

## The idea

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $n$ the length of the input and $|G|$ the grammar size. The relation $\Rightarrow_{rm}$ is one step of a rightmost derivation, which rewrites the rightmost nonterminal.

**Reductions and rightmost derivations.** A reduction replaces an occurrence of $\beta$ in a sentential form by $A$, for a production $A \to \beta$. A bottom-up parse of $w$ is a sequence of reductions that turns $w$ into $S$. When each reduction is the inverse of a rightmost step,

$$S = \gamma_0 \Rightarrow_{rm} \gamma_1 \Rightarrow_{rm} \cdots \Rightarrow_{rm} \gamma_k = w,$$

the parser meets the forms in the order $\gamma_k, \gamma_{k-1}, \ldots, \gamma_0$. So a bottom-up parser builds a rightmost derivation in reverse, while a [top-down parser](/top-down-parsing/) builds a leftmost derivation in order. Both build the same [parse tree](/parse-tree/): the reductions create the inner nodes in postorder.

**Handles.** Let $\gamma = \alpha \beta x$ be a right sentential form with $x \in \Sigma^*$, and assume $S \Rightarrow^*_{rm} \alpha A x \Rightarrow_{rm} \alpha \beta x$. The production $A \to \beta$ at the position right after $\alpha\beta$ is a [handle](/handle/) of $\gamma$. Reducing a handle gives the previous form of a rightmost derivation; this is *handle pruning*. Because everything right of a handle is terminal, the handle is always at the top of the stack in a shift-reduce parser, never inside it. If $G$ is unambiguous, each right sentential form has exactly one rightmost derivation and so exactly one handle.

**Shift-reduce parsing.** The parser keeps a stack of grammar symbols and the rest of the input. A *shift* moves the next token onto the stack. A *reduce* by $A \to \beta$ pops $\beta$ from the top and pushes $A$. *Accept* happens when the stack is $S$ and the input is empty. At each moment the stack followed by the rest of the input is a right sentential form, if the parse is on the right track. The prefixes of right sentential forms that can appear on the stack are the [viable prefixes](/viable-prefix/): the prefixes that do not extend past the right end of the handle. Knuth (1965) proved that the viable prefixes of each grammar form a regular language. This is why an LR parser can choose its move with a finite automaton that reads the stack.

**The decision.** A shift-reduce parser must answer two questions at each step: shift or reduce, and, if reduce, by which production. A wrong answer is a *conflict*: a [shift-reduce conflict](/shift-reduce-conflict/) or a [reduce-reduce conflict](/reduce-reduce-conflict/). The bottom-up methods differ in how they answer.

| method | how it decides | grammars it accepts |
|---|---|---|
| [operator precedence](/operator-precedence-parsing/) | precedence relations between terminals | operator grammars without conflicts |
| [LR(0)](/lr0-parsing/) | the state of the item automaton | LR(0) grammars |
| [SLR(1)](/slr-parsing/) | LR(0) states, FOLLOW sets as lookahead | SLR(1) grammars |
| [LALR(1)](/lalr-parsing/) | LR(0) states with exact merged lookaheads | LALR(1) grammars, the class of yacc |
| [canonical LR(1)](/canonical-lr-parsing/) | LR(1) item sets | all LR(1) grammars |
| [GLR](/glr-parsing/) | follows all actions of a conflict at once | all context-free grammars |

An LR(k) parser runs in $O(n)$ time, and the LR(k) languages for $k \ge 1$ are exactly the [deterministic context-free languages](/deterministic-context-free-language/). Each LL(k) grammar is LR(k), so the deterministic bottom-up methods accept more grammars than the deterministic top-down ones. In particular they accept left recursion, which top-down parsers cannot handle.

The [CYK algorithm](/cyk-algorithm/) is bottom-up too, in the sense that it builds the tree from the leaves. But it is not directional: it works on all substrings at once rather than from left to right, and it takes $O(n^3 |G|)$ time.

## Examples

**A shift-reduce trace.** Take the grammar

$$E \to E + T \mid T, \qquad T \to T * F \mid F, \qquad F \to ( E ) \mid \mathtt{id}$$

and the input $\mathtt{id} + \mathtt{id} * \mathtt{id}$. The moves below are those of the LR(1) parser for this grammar, with $\$$ for the end of the input.

| stack | rest of the input | move |
|---|---|---|
| (empty) | id + id * id \$ | shift |
| id | + id * id \$ | reduce F → id |
| F | + id * id \$ | reduce T → F |
| T | + id * id \$ | reduce E → T |
| E | + id * id \$ | shift |
| E + | id * id \$ | shift |
| E + id | * id \$ | reduce F → id |
| E + F | * id \$ | reduce T → F |
| E + T | * id \$ | shift |
| E + T * | id \$ | shift |
| E + T * id | \$ | reduce F → id |
| E + T * F | \$ | reduce T → T * F |
| E + T | \$ | reduce E → E + T |
| E | \$ | accept |

The 8 reductions, read from the last to the first, give the rightmost derivation

$$E \Rightarrow E + T \Rightarrow E + T * F \Rightarrow E + T * \mathtt{id} \Rightarrow E + F * \mathtt{id} \Rightarrow E + \mathtt{id} * \mathtt{id} \Rightarrow T + \mathtt{id} * \mathtt{id} \Rightarrow F + \mathtt{id} * \mathtt{id} \Rightarrow \mathtt{id} + \mathtt{id} * \mathtt{id}.$$

**A move that fits but is wrong.** In the row with stack $E + T$ and next token $*$, the top $E + T$ matches the right side of $E \to E + T$. Reducing would give the stack $E$ followed by $* \, \mathtt{id}$, and no right sentential form starts with $E *$. So the parser must shift. An LR parser knows this because $E + T$ followed by $*$ is not the end of a handle: the lookahead $*$ is not in the set of tokens that can follow a complete $E \to E + T$ in this context.

**A conflict.** For the ambiguous grammar $E \to E + E \mid \mathtt{id}$ and the stack $E + E$ with next token $+$, both moves lead to a parse: reduce gives $(\mathtt{id} + \mathtt{id}) + \mathtt{id}$ and shift gives $\mathtt{id} + (\mathtt{id} + \mathtt{id})$. Every LR parser generator reports a shift-reduce conflict here, and yacc resolves it by the associativity declaration `%left '+'`, which chooses reduce.

## Where it is used

- **Parser generators.** [Yacc](/yacc/), Bison and their descendants build [LALR(1)](/lalr-parsing/) or [canonical LR(1)](/canonical-lr-parsing/) tables. Most compilers of C-family languages were built with them.
- **Deterministic parsing in linear time.** The [LR parsing](/lr-parsing/) family runs in $O(n)$ time with a table of fixed size, and detects an error at the first token that cannot continue a valid prefix.
- **General parsing.** [GLR parsing](/glr-parsing/) extends the LR stack to a [graph-structured stack](/graph-structured-stack/) and parses every context-free grammar, ambiguous or not.
- **Expressions.** The [shunting-yard algorithm](/shunting-yard-algorithm/) and [operator precedence parsing](/operator-precedence-parsing/) are small bottom-up parsers for expressions with precedence levels.
- **Theory.** The equivalence of LR(k) grammars, deterministic context-free languages and [deterministic pushdown automata](/pushdown-automaton/) rests on the bottom-up view, as Knuth showed in 1965.

## References
