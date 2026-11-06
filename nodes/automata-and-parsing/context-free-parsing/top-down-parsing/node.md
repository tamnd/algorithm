---
tag: GTD5N2
kind: concept
slug: top-down-parsing
name: Top-down parsing
area: automata-and-parsing/context-free-parsing
level: core
summary: Builds the parse tree from the root, expanding nonterminals predictively.
prereqs: [context-free-grammar, leftmost-derivation, parse-tree]
see_also: [bottom-up-parsing, recursive-descent-parsing, ll1-parsing, ll-grammar, backtracking-parsing, left-recursion-elimination, left-factoring, first-and-follow-sets]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.4, Top-Down Parsing (4.4.1 Recursive-Descent Parsing, 4.4.2 FIRST and FOLLOW, 4.4.3 LL(1) Grammars, 4.4.4 Nonrecursive Predictive Parsing); Section 4.3.3, Elimination of Left Recursion
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 3.2, Two Ways to Parse a Sentence; Chapter 6, General Directional Top-Down Parsing; Chapter 8, Deterministic Top-Down Parsing
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 6.3.1, From Grammars to Pushdown Automata (the PDA that simulates leftmost derivations)
  - paper: "Daniel J. Rosenkrantz and Richard E. Stearns, Properties of deterministic top-down grammars, Information and Control 17(3) (1970)"
    locator: pp. 226 to 256 (LL(k) grammars, and languages with no LL(k) grammar)
---

Top-down parsing builds the [parse tree](/parse-tree/) of an input from the root down: it starts with the start symbol and repeatedly replaces the leftmost nonterminal that is not yet expanded by the right side of one of its productions, so it constructs a [leftmost derivation](/leftmost-derivation/) of the input in order. The hard part is to choose the production. A predictive parser chooses it from the next input tokens, which works for the [LL grammars](/ll-grammar/); a [backtracking parser](/backtracking-parsing/) tries the choices in turn. [Recursive descent](/recursive-descent-parsing/), [LL(1) parsing](/ll1-parsing/) and the hand-written parsers of most compilers are top-down.

## In plain words

A grammar says how a sentence is built: a program is a list of statements, a statement is an assignment or a loop, and so on. A top-down parser starts from the top goal, "this is a program", and breaks it into smaller goals, from left to right, until each goal is a single token that it can compare with the input.

At each goal with several possible forms, the parser must pick one. It looks at the next token of the input. If the next token is the keyword "while", the statement must be a loop. When one token is always enough to decide, the parser never needs to go back, and it reads the input in one pass. When it is not enough, the parser must guess, and undo the guess if it fails later.

## The idea

We use the notation of the [context-free grammar](/context-free-grammar/) page: a grammar $G = (V, \Sigma, P, S)$, productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size. The input is $w = a_1 \cdots a_n$, followed by an end marker $\$$.

**The state of a top-down parser.** At each moment the parser has matched a prefix $u$ of the input and holds a string $\gamma \in (V \cup \Sigma)^*$ of goals, such that $S \Rightarrow_{lm}^* u\gamma$: the string $u\gamma$ is a left-sentential [sentential form](/sentential-form/). It has two moves.

- **Match.** If $\gamma = a\gamma'$ and the next input token is $a$, then consume $a$: the state becomes $(ua, \gamma')$.
- **Expand.** If $\gamma = A\gamma'$ and $A \to \alpha$ is a production, the state becomes $(u, \alpha\gamma')$. This is one step $uA\gamma' \Rightarrow_{lm} u\alpha\gamma'$ of a leftmost derivation.

The parser starts in $(\varepsilon, S)$ and accepts in $(w, \varepsilon)$. Since each expand step is a leftmost step, an accepting run is a leftmost derivation of $w$, read off in order, and so it gives the parse tree in preorder. With the goals on a stack, this is the nondeterministic [pushdown automaton](/pushdown-automaton/) with one state that expands and matches. A top-down parser is a deterministic way to run it.

**Choosing the production.** A *predictive* parser decides the expansion of $A$ from the next $k$ tokens, the lookahead. For $k = 1$ it uses the sets

$$\text{FIRST}(\alpha) = \{ a \in \Sigma : \alpha \Rightarrow^* a\beta \}, \qquad \text{FOLLOW}(A) = \{ a \in \Sigma \cup \{\$\} : S\$ \Rightarrow^* \beta A a \gamma \}$$

([FIRST and FOLLOW sets](/first-and-follow-sets/)). The production $A \to \alpha$ is chosen on the token $a$ if $a \in \text{FIRST}(\alpha)$, or if $\alpha$ is [nullable](/nullable-symbol/) and $a \in \text{FOLLOW}(A)$. A grammar is LL(1) when no nonterminal has two productions that are chosen on the same token. Then every expansion is forced, the parser never backtracks, and it runs in $O(n)$ time for a fixed grammar: the parse tree has $O(n)$ nodes when the grammar has no cycles $A \Rightarrow^+ A$, and each move adds one node or consumes one token.

**What stops a predictive parser.**

- **Left recursion.** If $A \Rightarrow^+ A\alpha$, then a parser that expands $A$ without consuming input can expand $A$ again in the same state, forever. A predictive parser always picks the same production on the same token, so it loops, and a backtracking one also loops. [Left recursion](/left-recursion/) must be removed first ([left recursion elimination](/left-recursion-elimination/)).
- **Common prefixes.** For $S \to ab \mid ac$, one token of lookahead cannot choose. [Left factoring](/left-factoring/) rewrites it as $S \to aS'$, $S' \to b \mid c$, which delays the choice until after the $a$.
- **Ambiguity.** An [ambiguous](/ambiguity/) grammar is not LL($k$) for any $k$, since two leftmost derivations of the same string must at some point choose differently on the same lookahead.

**General top-down methods.** Without the LL condition, a top-down parser can still work. A [backtracking parser](/backtracking-parsing/) tries the productions in order and may take exponential time. [Packrat parsing](/packrat-parsing/) memoizes the results of an ordered-choice parser and runs in linear time, at the price of a different semantics ([parsing expression grammars](/parsing-expression-grammar/)). The [Earley parser](/earley-parser/) predicts top-down and completes bottom-up, and handles every grammar in $O(n^3)$ time.

## Examples

**An LL(1) parse.** The expression grammar $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to (\,E\,) \mid a$ is left recursive. Removing the left recursion gives

$$E \to T E', \quad E' \to + T E' \mid \varepsilon, \quad T \to F T', \quad T' \to * F T' \mid \varepsilon, \quad F \to (\,E\,) \mid a.$$

Its sets are $\text{FIRST}(E) = \text{FIRST}(T) = \text{FIRST}(F) = \{(, a\}$, $\text{FIRST}(E') = \{+\}$, $\text{FIRST}(T') = \{*\}$, and $\text{FOLLOW}(E) = \text{FOLLOW}(E') = \{), \$\}$, $\text{FOLLOW}(T) = \text{FOLLOW}(T') = \{+, ), \$\}$, $\text{FOLLOW}(F) = \{+, *, ), \$\}$. So $E' \to \varepsilon$ is chosen on $)$ and $\$$, and $T' \to \varepsilon$ on $+$, $)$ and $\$$. No two productions of one nonterminal share a token, so the grammar is LL(1). The run on $a + a * a$, with the top of the goal stack on the left:

| goals | input | move |
|---|---|---|
| $E\ \$$ | $a + a * a\ \$$ | expand $E \to T E'$ |
| $T\ E'\ \$$ | $a + a * a\ \$$ | expand $T \to F T'$ |
| $F\ T'\ E'\ \$$ | $a + a * a\ \$$ | expand $F \to a$ |
| $a\ T'\ E'\ \$$ | $a + a * a\ \$$ | match $a$ |
| $T'\ E'\ \$$ | $+ a * a\ \$$ | expand $T' \to \varepsilon$, since $+ \in \text{FOLLOW}(T')$ |
| $E'\ \$$ | $+ a * a\ \$$ | expand $E' \to + T E'$ |
| $+\ T\ E'\ \$$ | $+ a * a\ \$$ | match $+$ |
| $T\ E'\ \$$ | $a * a\ \$$ | expand $T \to F T'$ |
| $F\ T'\ E'\ \$$ | $a * a\ \$$ | expand $F \to a$ |
| $a\ T'\ E'\ \$$ | $a * a\ \$$ | match $a$ |
| $T'\ E'\ \$$ | $* a\ \$$ | expand $T' \to * F T'$ |
| $*\ F\ T'\ E'\ \$$ | $* a\ \$$ | match $*$ |
| $F\ T'\ E'\ \$$ | $a\ \$$ | expand $F \to a$ |
| $a\ T'\ E'\ \$$ | $a\ \$$ | match $a$ |
| $T'\ E'\ \$$ | $\$$ | expand $T' \to \varepsilon$ |
| $E'\ \$$ | $\$$ | expand $E' \to \varepsilon$ |
| $\$$ | $\$$ | accept |

The 11 expansions are the 11 steps of the leftmost derivation of $a + a * a$ in the new grammar, and the 5 matches consume the 5 tokens. The tree is built in preorder: the root $E$ first, then its first child $T$, and so on.

**Left recursion loops.** With the original production $E \to E + T$, a top-down parser in the state $(\varepsilon, E\ \$)$ on the input $a$ that tries $E \to E + T$ first reaches $(\varepsilon, E + T\ \$)$, with the same input and $E$ on top again. It can repeat this forever without consuming a token.

**Backtracking needed.** For $S \to aB \mid aC$, $B \to b$, $C \to c$ and the input $ac$, the token $a$ is in $\text{FIRST}(aB)$ and in $\text{FIRST}(aC)$. A backtracking parser tries $S \to aB$, matches $a$, fails on $c \ne b$, goes back to the start and tries $S \to aC$. A parser with two tokens of lookahead decides at once: the grammar is LL(2) but not LL(1).

**A language that has no LL grammar.** The language $\{a^k b^k : k \ge 1\} \cup \{a^k c^k : k \ge 1\}$ is accepted by a deterministic pushdown automaton, which pushes the $a$'s and decides at the first $b$ or $c$. Rosenkrantz and Stearns give it as a language that no LL($k$) grammar generates, for any $k$. The intuition is that a top-down parser must decide how to expand the start symbol, that is, which of the two kinds of string it builds, while the next $k$ tokens are still $a$'s. So the LL languages are fewer than the deterministic context-free ones, which [bottom-up parsing](/bottom-up-parsing/) handles.

## Where it is used

- [Recursive descent parsing](/recursive-descent-parsing/) writes one procedure for each nonterminal, and the call stack holds the goals. It is the method of the hand-written parsers of many production compilers, such as Clang and GCC.
- [LL(1) parsing](/ll1-parsing/) drives the same moves from an [LL parse table](/ll-parse-table/) and an explicit stack; [LL(k) parsing](/ll-k-parsing/) and [LL(*) parsing](/ll-star-parsing/) use longer lookahead.
- [Pratt parsing](/pratt-parsing/) adds binding powers to recursive descent to parse expressions without the long chain of precedence levels.
- [Backtracking parsing](/backtracking-parsing/), [packrat parsing](/packrat-parsing/) and [parser combinators](/parser-combinators/) are top-down methods that allow more grammars at a cost in time or semantics.
- [Syntax-directed translation](/syntax-directed-translation/) with inherited attributes fits top-down parsing well, because a procedure can pass values down to the procedures it calls.
- The opposite strategy is [bottom-up parsing](/bottom-up-parsing/), which builds the tree from the leaves and finds a rightmost derivation in reverse.

## References
