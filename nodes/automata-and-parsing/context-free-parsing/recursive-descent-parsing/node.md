---
tag: FBHW41
kind: algorithm
slug: recursive-descent-parsing
name: Recursive descent parsing
aliases:
- recursive descent parser
- top-down recursive parsing
area: automata-and-parsing/context-free-parsing
level: core
summary: Top-down parser implemented as mutually recursive procedures, one per nonterminal.
solves: [cfg-parsing-problem]
model: word-ram
complexity:
  vars: {n: "the number of input tokens, for a fixed LL(1) grammar"}
  time: {worst: O(n), best: Θ(1)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: true, online: true}
history:
  year: 1968
  people: [Philip M. Lewis, Richard E. Stearns]
  note: Lewis and Stearns defined the LL(k) grammars in 1968, the class on which predictive recursive descent needs no backtracking.
prereqs: [top-down-parsing, context-free-grammar, recursion]
see_also: [ll1-parsing, first-and-follow-sets, left-recursion-elimination, left-factoring, pratt-parsing, backtracking-parsing, packrat-parsing, recursive-ascent-parsing]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 2.4.2, Predictive Parsing; Section 4.4.1, Recursive-Descent Parsing; Section 4.4.2, FIRST and FOLLOW; Section 4.4.3, LL(1) Grammars
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Chapter 6, General Directional Top-Down Parsing (recursive descent with backtracking); Chapter 8, Deterministic Top-Down Parsing (LL(1) parsing and its recursive form)
  - paper: doi:10.1145/321466.321477
    title: Philip M. Lewis II and Richard E. Stearns, Syntax-directed transduction, Journal of the ACM 15(3) (1968)
    locator: pp. 465 to 488 (the LL(k) grammars)
---

Recursive descent parsing is [top-down parsing](/top-down-parsing/) written as a set of procedures, one for each nonterminal of the grammar: the procedure for $A$ reads the part of the input that $A$ derives, calling the procedures of the nonterminals on the right side of the chosen production. In its predictive form it chooses the production from the next token, and for an LL(1) grammar it parses in linear time with no backtracking. It is the easiest parser to write by hand, gives good error messages, and is the method of many production compilers.

## In plain words

A grammar rule says, for example, that a term is a factor followed by more factors joined by times signs. A recursive descent parser turns each rule into a function with the same name. The function for "term" calls the function for "factor", then, while the next token is a times sign, it reads the sign and calls "factor" again.

When a rule has several forms, the function looks at the next token to choose one. If each form starts with different tokens, the choice is always right, and the parser never goes back. Parentheses and other nesting are handled by functions that call each other, so the call stack of the program remembers where each open part started. A rule that starts with its own name, such as "an expression is an expression plus a term", makes the function call itself forever, so such rules must be rewritten first.

## The problem

The input is a [context-free grammar](/context-free-grammar/) $G = (V, \Sigma, P, S)$ and a string $w = a_1 \cdots a_n$ of tokens. We use the notation of that page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size. The token after the input is the end marker $a_{n+1} = \$$. The output is a [parse tree](/parse-tree/) of $w$, or an error when $w \notin L(G)$ ([the parsing problem](/cfg-parsing-problem/)).

The predictive method needs two conditions on $G$. With the [FIRST and FOLLOW sets](/first-and-follow-sets/) and [nullable symbols](/nullable-symbol/), define for each production

$$\text{PREDICT}(A \to \alpha) = \text{FIRST}(\alpha) \cup \begin{cases} \text{FOLLOW}(A) & \text{if } \alpha \Rightarrow^* \varepsilon, \\ \emptyset & \text{otherwise.} \end{cases}$$

1. **LL(1).** Two different productions of the same nonterminal have disjoint PREDICT sets.
2. **No left recursion.** There is no derivation $A \Rightarrow^+ A\beta$. For a grammar that satisfies condition 1 and has no [useless symbols](/useless-symbol-elimination/), this holds by itself; the implementation tests it anyway, so that the parser always stops.

## The algorithm

```pseudo id=main
PARSE(G, w)
L1  for each production A → α, compute PREDICT(A → α)     ▷ once per grammar
L2  pos ← 1;  t ← PROC(S)
L3  if a_pos ≠ $ then error                               ▷ input left over
L4  return t

PROC(A)                                                   ▷ one procedure for each nonterminal
L5  choose A → X1 … Xk with a_pos ∈ PREDICT(A → X1 … Xk); if there is none, error
L6  children ← empty list
L7  for i ← 1 to k do
L8      if Xi is a terminal then
L9          if a_pos ≠ Xi then error
L10         append Xi to children;  pos ← pos + 1
L11     else append PROC(Xi) to children
L12 return the node A with children
```

The global variable pos is the position of the next token. Line L5 is the prediction: by the LL(1) condition at most one production fits the token $a_{pos}$. Lines L8 to L10 match a terminal of the right side against the input, and line L11 calls the procedure of a nonterminal, which reads exactly the part of the input that the nonterminal derives. A production $A \to \varepsilon$ has $k = 0$, so it reads nothing; it is chosen when the next token can follow $A$.

In a hand-written parser, PROC(A) is a real function `A()`, and the choice of line L5 is a `switch` on the next token. The implementation of this page keeps the grammar as data, so that it can be tested on many grammars, and it runs the procedures as Python generators on an explicit stack: a call of line L11 is a `yield`, and nesting depth does not hit the recursion limit of the language.

## Example

Take the expression grammar without left recursion:

$$E \to T E', \quad E' \to + T E' \mid \varepsilon, \quad T \to F T', \quad T' \to * F T' \mid \varepsilon, \quad F \to (\,E\,) \mid a.$$

The PREDICT sets are $\{(, a\}$ for $E \to TE'$, $T \to FT'$; $\{+\}$ for $E' \to +TE'$; $\{), \$\}$ for $E' \to \varepsilon$; $\{*\}$ for $T' \to *FT'$; $\{+, ), \$\}$ for $T' \to \varepsilon$; $\{(\}$ for $F \to (E)$ and $\{a\}$ for $F \to a$. They are disjoint for each nonterminal. On $a + a * a$ (positions 1 to 5, then $\$$ at position 6), the calls are, with indentation for the depth of the call:

| call | pos | token | production chosen |
|---|---|---|---|
| E | 1 | a | $E \to T E'$ |
| . T | 1 | a | $T \to F T'$ |
| . . F | 1 | a | $F \to a$, match $a$ |
| . . T' | 2 | + | $T' \to \varepsilon$ |
| . E' | 2 | + | $E' \to + T E'$, match $+$ |
| . . T | 3 | a | $T \to F T'$ |
| . . . F | 3 | a | $F \to a$, match $a$ |
| . . . T' | 4 | * | $T' \to * F T'$, match $*$ |
| . . . . F | 5 | a | $F \to a$, match $a$ |
| . . . . T' | 6 | \$ | $T' \to \varepsilon$ |
| . . E' | 6 | \$ | $E' \to \varepsilon$ |

There are 11 calls, one for each internal node of the parse tree, in preorder, and 5 matches. After the call of $E$ returns, pos is 6 and $a_6 = \$$, so line L3 accepts. On $a + * a$, the call of $T$ at position 3 sees $*$, which is in no PREDICT set of $T$, and line L5 reports the error at the exact token.

A hand-written parser for the same language usually replaces $E'$ and $T'$ by loops, in the extended form $E \to T \{ + T \}$, $T \to F \{ * F \}$:

```
E():  x ← T();  while next = "+" do  match "+";  x ← node("+", x, T())  od;  return x
T():  x ← F();  while next = "*" do  match "*";  x ← node("*", x, F())  od;  return x
F():  if next = "(" then match "(";  x ← E();  match ")";  return x  else return leaf(match "a")
```

The loop builds left-associative trees directly, which the grammar with $E'$ does not do.

## Correctness

**Claim.** If $G$ is LL(1) and not left recursive, then PARSE stops on every input. It returns a parse tree of $w$ if $w \in L(G)$, and it reports an error if $w \notin L(G)$.

Three facts give the claim. *Soundness:* by induction on the returns, a call PROC(A) that starts at position $p$ and returns at position $q$ returns a parse tree with root $A$ whose leaves spell $a_p \cdots a_{q-1}$. *Completeness:* if $w$ has a parse tree $T$, each node $A$ of $T$ with children $\alpha$ over $a_p \cdots a_{q-1}$ has $a_p \in \text{PREDICT}(A \to \alpha)$: the token is in $\text{FIRST}(\alpha)$ when $q > p$, and in $\text{FOLLOW}(A)$ when $\alpha$ derives $\varepsilon$. By the LL(1) condition, line L5 chooses exactly that production, and by induction on the height of the node the call returns at $q$. *Termination:* the active calls that start at the same position form a chain $A_1, A_2, \ldots$ in which each $A_{i+1}$ follows a nullable prefix in the chosen production of $A_i$; without left recursion such a chain has at most $|V|$ calls, so the call stack has depth at most $(n + 1)|V|$. The full proof is in [the correctness proof](proofs/correctness.md). Completeness also shows that the tree is unique: an LL(1) grammar is unambiguous.

## Complexity

**Preparation.** Line L1 computes the nullable symbols, FIRST and FOLLOW by fixpoint iteration. Each round of the iteration scans the grammar, and each round that does not stop adds at least one element to one of the $|V|$ sets of at most $|\Sigma| + 1$ tokens. So there are at most $|V|(|\Sigma| + 2) + 1$ rounds of $O(|G|)$ set operations each. This is independent of the input.

**Parsing.** Each call does $O(1)$ work for its choice and $O(1)$ work for each symbol of its right side, so the time is linear in the size of the call tree. Split the calls into those that read at least one token and those that read none. A call that reads a token starts at the position $p$ of its first token, and it is an ancestor of the leaf $a_p$ that starts at $p$; these ancestors form a chain as in the termination argument, so there are at most $|V|$ of them for each $p$, and at most $n|V|$ in all. A call that reads nothing has a subtree of calls that all read nothing, of depth at most $|V|$, so its subtree has at most $c_G = \sum_{d < |V|} r^d$ calls, where $r$ is the longest right side. The maximal such subtrees hang below the root or below the at most $n|V|$ reading calls, at most $r$ below each. So the number of calls is at most $n|V| + (rn|V| + 1)\,c_G$, which is $O(n)$ for a fixed grammar. The best case is $\Theta(1)$: an error on the first token.

**Space.** The call stack has depth at most $(n + 1)|V|$ and the tree has $O(n)$ nodes for a fixed grammar, so the extra space is $O(n)$.

## Properties

- **Deterministic and one pass.** For an LL(1) grammar each token is read once and never read again.
- **Online.** The parser detects an error at the first token that cannot continue a valid prefix, the correct-prefix property of LL parsers.
- **Recursive.** The call stack is the parse stack. In a language with a small stack, deep nesting must be handled with an explicit stack, as in the implementation.
- **Inherited information flows down.** A procedure can take arguments from its caller, which makes [syntax-directed translation](/syntax-directed-translation/) with inherited attributes natural.

## Variants and improvements

- **Table-driven LL(1).** The same choices, made from an [LL parse table](/ll-parse-table/) with an explicit stack of grammar symbols, give the nonrecursive [LL(1) parser](/ll1-parsing/).
- **Longer lookahead.** With $k$ tokens of lookahead, the method parses [LL(k) grammars](/ll-k-parsing/). [LL(*) parsing](/ll-star-parsing/) uses a finite automaton over the coming tokens to choose.
- **Backtracking.** Trying the productions in order and going back on failure handles more grammars ([backtracking parsing](/backtracking-parsing/)), in exponential time in the worst case. [Packrat parsing](/packrat-parsing/) memoizes each (procedure, position) pair and gives linear time for [parsing expression grammars](/parsing-expression-grammar/).
- **Precedence climbing.** For expressions with many precedence levels, [Pratt parsing](/pratt-parsing/) replaces one procedure per level by one loop with binding powers.
- **Recursive ascent.** The bottom-up analogue, with one procedure for each LR state, is [recursive ascent parsing](/recursive-ascent-parsing/).

## When to use it

Use recursive descent when you write a parser by hand for a language that you control: the code reads like the grammar, each procedure can build exactly the tree you want, and errors are easy to report at the right token. Use a parser generator with [LALR(1) parsing](/lalr-parsing/) when the grammar is large, changes often, or is naturally left recursive and you do not want to rewrite it. Use the [Earley parser](/earley-parser/) or [GLR parsing](/glr-parsing/) for ambiguous grammars.

## Pitfalls

- **Left recursion.** A production $E \to E + T$ makes PROC(E) call PROC(E) at line L11 without reading a token, forever. Remove left recursion first ([left recursion elimination](/left-recursion-elimination/)), or use a loop as in the hand-written form.
- **Wrong associativity after the rewrite.** In the grammar with $E \to T E'$, $E' \to - T E' \mid \varepsilon$, the tree of $a - b - c$ groups to the right. Evaluating that tree naively gives $a - (b - c)$. Pass the left operand down to $E'$ as an argument, or use the loop, which builds $(a - b) - c$.
- **Forgetting FOLLOW.** Choosing $A \to \varepsilon$ on any token that starts no other production accepts too much and moves errors to a later place. Line L5 must choose $A \to \varepsilon$ only when the token is in $\text{FOLLOW}(A)$.
- **Not checking the end.** Without line L3, the parser accepts $a\,a$ for the expression grammar, because PROC(E) returns after the first $a$.
- **Common prefixes.** For $S \to ab \mid ac$, one token cannot choose. [Left-factor](/left-factoring/) the grammar into $S \to aS'$, $S' \to b \mid c$.

## Implementations

## History

Recursive descent compilers were written for ALGOL 60 in the early 1960s, since the procedures of the parser follow the recursive syntax of the language. Lewis and Stearns defined the LL($k$) grammars in 1968 in their study of syntax-directed transduction, and these are the grammars on which a predictive parser with $k$ tokens of lookahead works without backtracking. Rosenkrantz and Stearns studied their properties in 1970.

## References
