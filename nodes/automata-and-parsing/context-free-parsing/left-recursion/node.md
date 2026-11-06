---
tag: Y501YC
kind: concept
slug: left-recursion
name: Left recursion
area: automata-and-parsing/context-free-parsing
level: core
summary: A nonterminal that can derive a sentential form beginning with itself, which breaks naive top-down parsers.
prereqs: [context-free-grammar, derivation, nullable-symbol]
see_also: [left-recursion-elimination, left-recursion-removal, recursive-descent-parsing, ll1-parsing, left-factoring, greibach-normal-form, packrat-parsing, earley-parser]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.3.3, Elimination of Left Recursion; Section 4.4.3, LL(1) Grammars (no left-recursive grammar is LL(1))
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 6.4, Eliminating Left Recursion; Section 11.1.3, Hidden Left Recursion and Loops
  - paper: doi:10.1145/1328408.1328424
    title: Alessandro Warth, James R. Douglass and Todd Millstein, Packrat parsers can support left recursion, PEPM 2008
    locator: pp. 103 to 110
  - paper: doi:10.1145/321250.321254
    title: Sheila A. Greibach, A new normal-form theorem for context-free phrase structure grammars, Journal of the ACM 12(1) (1965)
    locator: pp. 42 to 52 (every context-free language without the empty string has a grammar in which every right side starts with a terminal)
---

A nonterminal $A$ is left-recursive when it derives, in one or more steps, a sentential form that begins with $A$ itself: $A \Rightarrow^+ A \alpha$. A grammar is left-recursive when it has a left-recursive nonterminal. Left recursion is the natural way to write left-associative operators and lists, and bottom-up parsers handle it well, but a naive top-down parser on such a grammar calls itself forever without reading input.

## In plain words

Some rules say "an A is an A followed by something". A list of numbers is a list, then a comma, then a number. That is a fine description, but a parser that works from the top down reads it as an order: to find an A, first find an A. It then asks the same question again before it has read any word, and it never stops.

Rules can hide this loop. A rule can start with B, and B can start with A. A rule can also start with a name that can be empty, and only then with A. In each case the parser can return to A without reading a word. Parsers that work from the bottom up do not have this problem, because they recognize the inner A first.

## The idea

We use the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol, $n$ the input length. Let $G = (V, \Sigma, P, S)$ be a [context-free grammar](/context-free-grammar/) and $A \in V$.

**Definition.** $A$ is **left-recursive** if $A \Rightarrow^+ A \alpha$ for some $\alpha \in (V \cup \Sigma)^*$. Three kinds are usually named:

- **immediate** (or direct) left recursion: a production $A \to A \alpha$;
- **indirect** left recursion: a cycle through other nonterminals, as in $A \to B \beta$ and $B \to A \gamma$;
- **hidden** left recursion: $A$ comes after a [nullable](/nullable-symbol/) prefix, as in $A \to B A \gamma$ with $B \Rightarrow^* \varepsilon$.

The case $\alpha = \varepsilon$, that is $A \Rightarrow^+ A$, is a **cycle**; a grammar with a useful cycle is ambiguous.

**Detection.** Draw the *left-corner graph*: an edge from $A$ to $B$ whenever some production $A \to X_1 \cdots X_k$ has $X_i = B$ and $X_1, \ldots, X_{i-1}$ all nullable. Then $A$ is left-recursive if and only if $A$ lies on a cycle of this graph.

*Proof.* If there is an edge $A \to B$, then $A \Rightarrow X_1 \cdots X_{i-1} B \cdots \Rightarrow^* B \cdots$, by erasing the nullable prefix. Following a cycle from $A$ back to $A$ gives $A \Rightarrow^+ A \alpha$. Conversely, let $A \Rightarrow^m A \alpha$ with $m \ge 1$, and take the [parse tree](/parse-tree/) of this derivation. The leftmost leaf of the frontier is labeled $A$; follow the path from the root to it. At each node $C$ on the path with production $C \to X_1 \cdots X_k$, the path goes to some $X_i$ such that all the subtrees of $X_1, \ldots, X_{i-1}$ have empty frontier, so these symbols are nullable, and $C \to X_i$ is an edge. The path has at least one edge because $m \ge 1$. So the path is a closed walk from $A$ to $A$ in the graph. $\square$

The nullable set and the graph take $O(|G|)$ time to build, and a strongly connected components search finds all left-recursive nonterminals in $O(|G|)$ time: a nonterminal is left-recursive exactly when its component has an edge inside it.

**Why top-down parsers fail.** A [recursive descent](/recursive-descent-parsing/) parser has one procedure for each nonterminal. With $A \to A \alpha \mid \beta$, the procedure for $A$ that tries the first alternative calls the procedure for $A$ again at the same input position, so it recurses without end. A predictive parser does not loop, but it cannot choose: if $A \to A \alpha \mid \beta$ and $\beta$ derives a nonempty terminal string, every terminal in FIRST($\beta$) is also in FIRST($A \alpha$), so the grammar is not [LL(1)](/ll1-parsing/). In fact no left-recursive grammar is LL(1) when its left-recursive nonterminal is useful.

**Why bottom-up parsers like it.** A shift-reduce parser builds the inner $A$ first and reduces as soon as it can. For a list $E \to E + T \mid T$, an LR parser reduces after each item, and its stack stays short. For the right-recursive $E \to T + E \mid T$, it must shift the whole list before the first reduction.

## Examples

**Left-associative operators.** The expression grammar

$$E \to E + T \mid T, \qquad T \to T * F \mid F, \qquad F \to (\,E\,) \mid a$$

has immediate left recursion in $E$ and in $T$. Its parse tree for $a + a + a$ groups as $(a + a) + a$, which is the meaning of left-associative $+$. On $a + a + \cdots + a$ with $k$ plus signs, an LALR(1) parser for $E \to E + T \mid T$, $T \to a$ never has more than 4 states on its stack, while for $E \to T + E \mid T$ its stack grows to $2k + 2$ states (measured for $k = 1, 10, 100$).

**Indirect.** In $S \to A a \mid b$, $A \to S c \mid d$, neither production is immediately left-recursive, but $S \Rightarrow A a \Rightarrow S c a$. Both $S$ and $A$ are on the cycle $S \to A \to S$ of the left-corner graph.

**Hidden.** In $A \to B A c \mid a$, $B \to \varepsilon \mid b$, the derivation $A \Rightarrow B A c \Rightarrow A c$ shows that $A$ is left-recursive, though $A$ is not first on any right side. Hidden left recursion escapes a test that only looks at the first symbol, and some parsing methods that handle ordinary left recursion fail on it.

**A cycle.** In $A \to A \mid a$, $A \Rightarrow A$, and the string $a$ has infinitely many parse trees: $A \Rightarrow a$, $A \Rightarrow A \Rightarrow a$, and so on.

**Not left-recursive.** $E \to T + E \mid T$, $T \to a$ is right-recursive: $E$ derives forms that end with $E$, but none that begin with it.

## Where it is used

- **Removing it for top-down parsing.** [Left recursion removal](/left-recursion-removal/) rewrites immediate left recursion $A \to A \alpha \mid \beta$ as $A \to \beta A'$, $A' \to \alpha A' \mid \varepsilon$, and [left recursion elimination](/left-recursion-elimination/) removes indirect left recursion by ordering the nonterminals and substituting. The result describes the same language but gives right-leaning trees, so associativity has to be restored in the semantic actions. [Left factoring](/left-factoring/) is usually applied after it.
- **Normal forms.** In [Greibach normal form](/greibach-normal-form/) every right side starts with a terminal, so no nonterminal is left-recursive; the conversion to it removes left recursion as one of its steps.
- **General parsers.** The [Earley parser](/earley-parser/), CYK and [GLR](/glr-parsing/) parsers accept left-recursive grammars directly. Earley's parser is even faster on left recursion than on right recursion, which needs Leo's improvement to run in linear time. GLR parsers based on LR(0) tables can fail to terminate on hidden left recursion unless they are built with care.
- **Packrat and PEG parsers.** A [packrat parser](/packrat-parsing/) runs a [parsing expression grammar](/parsing-expression-grammar/) by recursive descent and also loops on left recursion. Warth, Douglass and Millstein grow the memoized result of a left-recursive rule step by step until it stops getting longer, and this lets such parsers accept many left-recursive rules.
- **Parser generators.** LR generators such as yacc prefer left recursion for lists. Top-down generators such as ANTLR rewrite immediate left recursion in a rule automatically, but reject indirect left recursion.
- **Left-corner parsing.** [Left-corner parsing](/left-corner-parsing/) predicts top-down but recognizes the left corner of each rule bottom-up, so it handles direct and indirect left recursion without changing the grammar; hidden left recursion through empty rules needs extra care.

## References
