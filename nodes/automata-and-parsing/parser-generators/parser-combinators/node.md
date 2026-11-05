---
tag: 622VZM
kind: technique
slug: parser-combinators
name: Parser combinators
aliases:
- monadic parsing
area: automata-and-parsing/parser-generators
level: advanced
summary: Builds parsers by composing small parser functions with higher-order operators.
prereqs: [recursive-descent-parsing, context-free-grammar]
see_also: [parser-generator, parsing-expression-grammar, packrat-parsing, left-recursion-elimination, backtracking-parsing, pratt-parsing, gll-parsing, ll1-parsing]
sources:
  - paper: doi:10.1017/S0956796800000411
    title: Graham Hutton, Higher-order functions for parsing, Journal of Functional Programming 2(3) (1992)
    locator: pp. 323 to 343 (parsers as functions returning lists of results, and the combinators for sequence, choice, repetition and semantic actions)
  - paper: doi:10.1017/S0956796898003050
    title: Graham Hutton and Erik Meijer, Monadic parsing in Haskell, Journal of Functional Programming 8(4) (1998)
    locator: pp. 437 to 444 (the parser monad, deterministic choice, and chainl1 for left-associative operators)
  - paper: "Philip Wadler, How to replace failure by a list of successes, Functional Programming Languages and Computer Architecture (FPCA 1985), Lecture Notes in Computer Science 201, Springer"
    locator: pp. 113 to 128 (the list of successes representation of backtracking)
  - paper: "Daan Leijen and Erik Meijer, Parsec: Direct style monadic parser combinators for the real world, technical report, Department of Computer Science, Universiteit Utrecht, 2001"
    locator: the sections on the choice combinator that commits after consuming input and on try
  - paper: "Richard A. Frost, Rahmatullah Hafiz and Paul Callaghan, Parser combinators for ambiguous left-recursive grammars, Practical Aspects of Declarative Languages (PADL 2008), Lecture Notes in Computer Science 4902, Springer"
    locator: the curtailment of left-recursive calls and the memoization that gives polynomial time
  - paper: "S. Doaitse Swierstra and Luc Duponcheel, Deterministic, error-correcting combinator parsers, Advanced Functional Programming, Lecture Notes in Computer Science 1129, Springer, 1996"
    locator: the combinators that compute first sets and emptiness alongside the parser, and the error correction
---

## In plain words

A parser combinator library treats a parser as an ordinary function: it takes the input and a position and says how far it can read. A few tiny parsers recognise single tokens, and a few operators glue parsers together: "this, then that", "this or that", "this, repeated", "this, with its result transformed". A whole grammar is then written as a program that looks almost like the grammar, in the host language, with no separate generator step.

Because the pieces are just functions, they can be tested one by one, given parameters, and mixed with ordinary code. The price is that the parser does exactly what the code says: it explores choices in the order written, it can take a very long time on some grammars, and a rule that calls itself before reading anything never stops.

## When it applies

Use combinators when the grammar is small or medium, changes often, or lives inside a program in a language with first-class functions: configuration formats, query languages, protocol messages, and the front ends of interpreters. They fit well when the parse must build values directly and when parts of the grammar are computed at run time.

The grammar must suit top-down parsing, as for [recursive descent](/recursive-descent-parsing/): no left recursion, and alternatives ordered or factored so that backtracking stays cheap. For large, stable grammars where linear time and conflict reports matter, a [parser generator](/parser-generator/) is usually the better tool.

## The template

**Notation.** A grammar is $G = (V, \Sigma, P, S)$ with productions written $A \to \alpha \mid \beta$, the empty string $\varepsilon$, start symbol $S$, input length $n$ and size $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$. The input is $w = a_1 \cdots a_n$, and a position $i$ means that $a_1 \cdots a_i$ has been read.

**Parsers.** A parser for values of type $T$ is a function $p$ from a position $i$ to a list of pairs $(v, j)$ with $i \le j$, each meaning "$a_{i+1} \cdots a_j$ can be read as the value $v$". The empty list is failure. This is Wadler's *list of successes*; a deterministic library returns at most one pair instead.

**Basic parsers and combinators.**

- $\mathrm{pure}(v)$ returns $[(v, i)]$ and reads nothing; $\mathrm{fail}$ returns $[\,]$.
- $\mathrm{sym}(a)$ returns $[(a, i + 1)]$ if $a_{i+1} = a$, else $[\,]$.
- $p \cdot q$ (sequence) runs $q$ from every end position of $p$ and pairs the values: all $((v, u), k)$ with $(v, j) \in p(i)$ and $(u, k) \in q(j)$. The monadic form $p \mathbin{>\!\!>\!\!=} f$ lets the second parser depend on the first value.
- $p \mid q$ (choice) returns the results of $p$ followed by those of $q$.
- $\mathrm{map}(f, p)$ applies $f$ to each value: semantic actions.
- $\mathrm{many}(p)$ is $\mathrm{pure}([\,]) \mid \mathrm{map}(\mathrm{cons}, p \cdot \mathrm{many}(p))$, zero or more repetitions, best written as a loop and restricted to iterations that read something.
- $\mathrm{chainl1}(p, \mathit{op})$ parses $p\ (\mathit{op}\ p)^*$ and combines the values from the left, the replacement for left-recursive rules such as $E \to E - T$.

**From grammar to program.** For each nonterminal $A$ with productions $A \to \alpha_1 \mid \cdots \mid \alpha_m$, define the parser $A = \alpha_1 \mid \cdots \mid \alpha_m$, where each $\alpha_k = X_1 \cdots X_r$ becomes $X_1 \cdot \cdots \cdot X_r$, terminals become $\mathrm{sym}$, nonterminals become references to their parsers, and $\varepsilon$ becomes $\mathrm{pure}$. The input is accepted when $S(0)$ contains a pair with $j = n$.

**What the program recognises.** With list-of-successes semantics, and for a grammar without left recursion (no derivation $A \Rightarrow^+ A \beta$, counting nullable prefixes), the program terminates and $A(i)$ contains a pair with end $j$ exactly when $A \Rightarrow^* a_{i+1} \cdots a_j$; so it accepts exactly $L(G)$, ambiguous grammars and ε-productions included. A script checked this against the language of the grammar on 1335 random grammars without left recursion, 771 of them with ε-productions, for all inputs over $\{a, b\}$ up to length 5.

**Deterministic choice.** Libraries for practical use usually make choice deterministic: $p \mid q$ returns the first success of $p$ and runs $q$ only if $p$ fails. This is the ordered choice of [parsing expression grammars](/parsing-expression-grammar/), and it recognises a different language from the grammar whenever an earlier alternative succeeds on a prefix that the rest of the input cannot extend. Parsec goes one step further: $p \mid q$ tries $q$ only if $p$ failed *without consuming input*, and the combinator $\mathrm{try}(p)$ makes a failure of $p$ count as consuming nothing, so the author chooses where backtracking is allowed (Leijen and Meijer).

## Classic examples

**All parses of a prefix.** For $S \to a\,S \mid a$ on the input $aaa$, the list of successes for $S$ from position 0 has the end positions 1, 2 and 3: every prefix that $S$ can read. Only the last is a full parse; the others are what make sequencing work, since a following parser starts from each of them.

**Ordered choice loses a parse.** The grammar $S \to (a \mid a\,b)\,c$ generates $ac$ and $abc$. With lists of successes, $S$ accepts $abc$: the second alternative of the choice ends at 2 and $c$ follows. With deterministic choice, the first alternative $a$ succeeds, so $a\,b$ is never tried, $c$ fails on $b$, and $abc$ is rejected, while $ac$ is still accepted. Writing the longer alternative first, or factoring it as $a\,(b \mid \varepsilon)\,c$, fixes it.

**Left-associative operators.** A rule $E \to E - n \mid n$ cannot be written directly, since $E$ would call itself at the same position forever; the script's version ran out of stack at once. The right-recursive rewrite $E \to n - E \mid n$ terminates but groups to the right, giving $1 - (2 - 3) = 2$ on $1 - 2 - 3$. $\mathrm{chainl1}(\mathit{num}, \mathit{minus})$ reads the same tokens with a loop and folds from the left, giving $(1 - 2) - 3 = -4$.

**Exponential time.** For $P \to a\,P\,b \mid a\,P\,c \mid \varepsilon$ on $a^k c^k$, the list-of-successes program explores both alternatives at every level and each one recurses again, so the number of terminal tests grows like $2^k$: the script counted 106 for $k = 4$, 1786 for $k = 8$ and 28666 for $k = 12$. Memoizing each nonterminal's result per position, as [packrat parsing](/packrat-parsing/) does, makes the count $6k$: 24, 48 and 72 for the same inputs.

## Variations

- **Monadic and applicative.** Monadic combinators let a later parser depend on an earlier value, which handles context-sensitive formats such as a length field followed by that many bytes. Applicative combinators forbid this, so the library can inspect the whole grammar before running it, compute first sets, and build a deterministic [LL(1)](/ll1-parsing/)-style parser with error correction, as Swierstra and Duponcheel did.
- **Memoization.** Caching results per (parser, position) turns deterministic combinators into a packrat parser with linear time for the PEG semantics, and bounds the number of calls of a list-of-successes parser by a polynomial in $n$, although for an ambiguous grammar the lists of values can still grow exponentially.
- **Left recursion.** Frost, Hafiz and Callaghan curtail a left-recursive call once it has been entered more times at a position than there are input tokens left, and with memoization they parse ambiguous left-recursive grammars in polynomial time. Libraries based on [GLL parsing](/gll-parsing/) handle all context-free grammars, with shared parse forests.
- **Operator tables.** Instead of one rule per precedence level, a combinator builds an expression parser from a table of operators, precedences and associativities, in the manner of [Pratt parsing](/pratt-parsing/).
- **Error messages.** Deterministic libraries record the farthest position reached and the tokens expected there, and let rules be labelled so that messages name a construct instead of a token.

## Pitfalls

- **Left recursion.** A rule that can call itself before reading input recurses forever, or until the stack is exhausted. Hidden left recursion through a nullable prefix, as in $A \to B\,A\,c$ with $B \Rightarrow^* \varepsilon$, is just as bad. Rewrite with $\mathrm{chainl1}$ or [left recursion elimination](/left-recursion-elimination/).
- **Repetition of an empty match.** $\mathrm{many}(p)$ with a $p$ that can succeed without reading anything loops; libraries either reject such iterations or stop when no input was consumed.
- **Order of alternatives.** With deterministic choice, an alternative that is a prefix of a later one hides it, as in the $(a \mid a\,b)\,c$ example; keywords and identifiers, or $\le$ and $<$, are the usual victims.
- **Exponential backtracking.** Unrestricted backtracking can take exponential time on inputs that a table-driven parser reads in linear time; add memoization, factor common prefixes, or make choices commit.
- **Recursion depth.** Each nonterminal call is a call of the host language, so deeply nested input can exhaust the stack, as in any [recursive descent](/recursive-descent-parsing/) parser.
- **No ambiguity report.** A combinator parser never tells you that the grammar is ambiguous or not LL(k): the list of successes silently returns several results, and deterministic choice silently picks one.

## Exercises

1. Write $\mathrm{many}(p)$ without recursion, as a loop over the frontier of end positions, and show that it terminates when every success of $p$ reads at least one token. *Hint: positions strictly increase along each chain, and there are $n + 1$ of them.*
2. Show that with lists of successes, $(p \mid q) \cdot r$ and $p \cdot r \mid q \cdot r$ return the same list, but with deterministic choice they can differ. *Hint: use $p = a$, $q = a\,b$, $r = c$ on $abc$.*
3. Define $\mathrm{chainr1}(p, \mathit{op})$ for right-associative operators, and use it for exponentiation so that $2 \wedge 3 \wedge 2$ means $2 \wedge (3 \wedge 2)$.
4. Prove that for a grammar without left recursion the list-of-successes program terminates on every input. *Hint: order the calls by (position, the depth of the nonterminal in a left-call graph that is acyclic).*
5. For $P \to a\,P\,b \mid a\,P\,c \mid \varepsilon$, find the number of terminal tests on $a^k c^k$ with and without memoization, and compare with the counts in the example.

## References
