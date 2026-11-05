---
tag: E6NAK1
kind: concept
slug: parser-generator
name: Parser generator
aliases:
- compiler-compiler
- parser generator tool
area: automata-and-parsing/parser-generators
level: intro
summary: A tool that takes a grammar as input and produces a parser for its language.
prereqs: [context-free-grammar]
see_also: [yacc, parser-table-construction, parsing-table, lalr-parsing, ll1-parsing, parser-combinators, packrat-parsing, parser-error-recovery]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 3.5, The Lexical-Analyzer Generator Lex; Section 4.8, Using Ambiguous Grammars; Section 4.9, Parser Generators
  - paper: "Stephen C. Johnson, Yacc: Yet Another Compiler-Compiler, Computing Science Technical Report No. 32, Bell Laboratories, Murray Hill, New Jersey, 1975"
    locator: the sections on the basic specification, actions, ambiguity and conflicts, precedence, and error handling
  - url: https://www.gnu.org/software/bison/manual/
    title: GNU Bison manual
    locator: chapter The Bison Parser Algorithm (sections Shift/Reduce Conflicts, Operator Precedence, Reduce/Reduce Conflicts, Tuning LR) and chapter Error Recovery
  - book: isbn:9781934356999
    title: Terence Parr, The Definitive ANTLR 4 Reference, Pragmatic Bookshelf, 2013
    locator: Chapter 1 (the ANTLR tool and the parse trees it builds) and Chapter 5 (Designing Grammars, left-recursive rules)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 17, Practical Parser Writing and Usage
---

A parser generator is a program that reads a [context-free grammar](/context-free-grammar/), usually with a piece of code attached to each production, and writes a parser for the language of that grammar. The output is either a [parsing table](/parsing-table/) plus a fixed driver, as in [yacc](/yacc/) and Bison, or ordinary code with one routine for each nonterminal, as in ANTLR. The generator checks the grammar while it works: when the grammar is outside the class that its method handles, it reports each conflict, so the author learns about an ambiguity before a user does.

## In plain words

Writing a parser by hand is slow and easy to get wrong. A parser generator turns the job around. You write down the rules of the language, such as "an expression is an expression, a plus sign and a term". The tool studies the rules and writes the parser for you.

The tool does more than copy the rules. It works out, for every situation the parser can be in, what the parser must do when it sees the next word. If two different moves fit the same situation, the rules are unclear, and the tool tells you where. If no situation is unclear, the parser it writes reads any input in one pass from left to right and never guesses. The code you attach to the rules runs at the moment each rule is recognized, so the parser can build a tree or compute a value as it goes.

## The idea

**Notation.** The parsing pages of this site use one notation. A grammar is $G = (V, \Sigma, P, S)$ with productions written $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, $S$ is the start symbol, $n$ is the length of the input and $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$ is the size of the grammar. The end of the input is the marker $\$ \notin \Sigma$.

**Input and output.** A parser generator for a parsing method $\mathcal{M}$ (LL(1), LALR(1), and so on) maps a grammar specification to a program. The specification holds the productions, the declarations of the terminals (the tokens), and optional extras: the code to run when a production is used, the precedence and associativity of operators, and rules for [error recovery](/parser-error-recovery/). The program it writes has a contract:

- If $G$ belongs to the class of $\mathcal{M}$ (for example, $G$ is an [LALR(1) grammar](/lalr-grammar/)), the generator reports no conflict, and the parser accepts a token string $w$ exactly when $w \in L(G)$. For the LL and LR methods it does so in $O(n)$ time, with one pass from left to right and no backtracking.
- If $G$ is outside the class, the generator reports each place where two moves compete. Many tools then pick one move by a fixed rule and still write a parser. That parser is deterministic, but it may accept a different language from $L(G)$, and the report is the only warning.

**The pipeline.** Most table-driven generators follow the same steps, which the [parser table construction](/parser-table-construction/) page states as a problem:

1. Read the grammar and check it: undefined symbols, nonterminals that derive no terminal string, symbols that the start symbol cannot reach.
2. Compute the [nullable symbols](/nullable-symbol/) and the [FIRST and FOLLOW sets](/first-and-follow-sets/).
3. Build the automaton of the method: for LR methods the [LR item sets](/lr-item-sets/) with their [lookahead symbols](/lookahead-symbols/), for LL(1) one row for each nonterminal.
4. Fill the table and find the conflicts. Resolve the ones that the precedence declarations cover, and report the rest.
5. [Compress the table](/parse-table-compression/), then write it out together with the driver and the user's code.

A scanner generator such as lex works the same way one level lower: it turns [regular expressions](/regular-expression/) into an automaton by the [Thompson construction](/thompson-construction/) and the [subset construction](/subset-construction/), and writes the scanner that splits the characters of the input into the tokens that the parser reads.

**Other designs.** Not every generator writes a table.

- *Recursive descent code.* ANTLR writes one function for each rule. ANTLR 4 decides between alternatives at run time with its ALL(*) prediction, an extension of [LL(*) parsing](/ll-star-parsing/), and it accepts directly left-recursive rules by rewriting them (Parr, Chapter 5).
- *Generalized parsers.* Bison can write a [GLR parser](/glr-parsing/) instead of an LALR(1) one (the `%glr-parser` declaration). It forks at each conflict, so it handles every context-free grammar, but its time is no longer linear when many alternatives stay alive.
- *PEG tools.* A generator for [parsing expression grammars](/parsing-expression-grammar/) writes a [packrat parser](/packrat-parsing/). Its choice operator is ordered, so it never reports a conflict: the first alternative that succeeds wins.
- *No generator at all.* [Parser combinators](/parser-combinators/) build the parser inside the host language from small functions, and give up the grammar analysis and the conflict report.

## Examples

**A specification.** This is a yacc input for sums and products of numbers. The part before the first `%%` declares the tokens and the operator precedence, the part after it lists the productions with their actions. `$$` is the value of the left side and `$1`, `$3` are the values of the first and the third symbol of the right side.

```
%token NUM
%left '+'
%left '*'
%%
expr : expr '+' expr   { $$ = $1 + $3; }
     | expr '*' expr   { $$ = $1 * $3; }
     | '(' expr ')'    { $$ = $2; }
     | NUM
     ;
```

The grammar $E \to E + E \mid E * E \mid (\,E\,) \mid \mathit{num}$ is [ambiguous](/ambiguity/). Its LR(0) automaton has 10 states, and the LALR(1) table has 4 cells with a [shift-reduce conflict](/shift-reduce-conflict/): in the state with the item $E \to E + E \,\cdot$ and in the state with $E \to E * E \,\cdot$, each on the lookaheads $+$ and $*$. The two `%left` lines settle all four. A later line has a higher precedence, so $*$ binds more tightly than $+$, and `%left` makes each operator group to the left. The generator then reports no conflict, and the parser evaluates `2+3*4` to 14.

**The same language without precedence.** The unambiguous grammar $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to (\,E\,) \mid \mathit{num}$ needs no declarations. Its LR(0) automaton has 12 states, the canonical LR(1) automaton has 22, and the LALR(1) table, with 12 states, has no conflict. This is why LALR(1) generators use the smaller automaton: on grammars like this one it loses nothing.

**A conflict that changes the language.** Take $S \to A\, b$, $A \to a \mid a\, b$. Its language is $\{ab, abb\}$. After reading $a$ with the lookahead $b$, the parser can reduce $a$ to $A$ or shift $b$, and one token cannot tell which: the grammar is LR(2) but not LR(1). A yacc-style generator reports one shift-reduce conflict and resolves it by shifting. The parser it writes accepts $abb$ and rejects $ab$, a sentence of the grammar. The conflict report is the only sign of this.

**A scanner specification.** A lex input pairs regular expressions with actions, such as `[0-9]+ { return NUM; }` and `[ \t\n] ;` to skip blanks. Lex and flex follow two rules when several patterns match: the scanner takes the longest match, and among patterns with a match of the same length it takes the one listed first.

## Where it is used

- **Compilers and interpreters.** Many language implementations have used yacc or Bison grammars. The [yacc](/yacc/) page describes its algorithm: LALR(1) tables, precedence, the default resolution of conflicts, and the `error` token.
- **Tools for data formats and query languages.** Configuration languages, SQL dialects and domain-specific languages are often defined by a grammar from which a generator writes the parser.
- **Teaching.** The steps of a generator are the standard sequence of a compiler course: [FIRST and FOLLOW sets](/first-and-follow-sets/), [LL(1) grammars](/ll-1-grammar/), [LR item sets](/lr-item-sets/), [LALR lookahead computation](/lalr-lookahead-computation/), and [table compression](/parse-table-compression/).
- **Grammar checking.** Because the generator lists every conflict, running it is a cheap test that a grammar is deterministic. A grammar without conflicts in an [LR(k)](/lr-k-grammar/) method is unambiguous. Deciding [ambiguity](/cfg-ambiguity-problem/) for an arbitrary grammar is [undecidable](/cfg-ambiguity-undecidable/), so this test is one-sided: a conflict does not prove ambiguity.
- **Editors.** Incremental generators write parsers that can reuse the old tree after an edit, the problem of [incremental reparsing](/incremental-reparsing/).

## References
