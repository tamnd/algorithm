---
tag: G04W13
kind: algorithm
slug: operator-precedence-parsing
name: Operator-precedence parsing
aliases:
- Floyd operator precedence parsing
- Operator precedence parsing
- precedence parsing
area: automata-and-parsing/context-free-parsing
level: core
summary: Shift-reduce parser that decides reductions by precedence relations between adjacent terminals.
solves: [cfg-parsing-problem]
model: word-ram
complexity:
  vars: {n: the number of input tokens, g: the grammar size, v: the number of nonterminals, σ: the number of terminals}
  time: {worst: O(n g), build: O(v g σ)}
  space: {extra: O(n g), table: O(σ^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 1963
  people: [Robert W. Floyd]
  note: Floyd defined operator grammars and precedence grammars and parsed them with a matrix of relations between pairs of terminals.
prereqs: [operator-grammar, shift-reduce-parsing, handle]
see_also: [shunting-yard-algorithm, pratt-parsing, lr0-parsing, lr-parse-table, bottom-up-parsing, recursive-descent-parsing, ambiguity, parse-tree]
sources:
  - paper: doi:10.1145/321172.321179
    title: Robert W. Floyd, Syntactic analysis and operator precedence, Journal of the ACM 10(3) (1963)
    locator: pp. 316 to 333
  - book: isbn:9780201100884
    title: Alfred V. Aho, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, first edition
    locator: Section 4.6, Operator-Precedence Parsing (the parsing algorithm, precedence functions and error recovery)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Section 9.2, Precedence Parsing
---

Operator-precedence parsing is a [shift-reduce](/shift-reduce-parsing/) method for [operator grammars](/operator-grammar/), the grammars with no empty right sides and no two adjacent nonterminals. It compares the topmost terminal on the stack with the next input token by one of three relations: $\lessdot$ and $\doteq$ say shift, and $\gtrdot$ says that the end of a [handle](/handle/) has been reached, whose start is the last $\lessdot$ below it. Floyd (1963) introduced it, and it parses expressions with any number of precedence levels in linear time from a small table indexed by terminals only.

## In plain words

When you read $2 + 3 * 4$ from left to right and reach the $*$, you cannot add yet, because $*$ binds more tightly than $+$. When you then reach the end, you multiply first and then add. An operator-precedence parser makes exactly these decisions, for every pair of tokens, from a table.

The parser keeps a stack of what it has read. It looks at the last token on the stack and the next token of the input. If the table says the new token "binds more tightly" or "belongs with" the old one, it reads it. If the old one "binds more tightly", the group at the top of the stack is complete, and the parser replaces it by one grammar symbol. Only tokens are compared, so the table is small and easy to write by hand.

## The problem

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area. The end marker $\$ \notin \Sigma$ is placed at both ends of the input.

Given an [operator precedence grammar](/operator-grammar/), an operator grammar in which at most one of the relations $\lessdot$, $\doteq$, $\gtrdot$ holds between any two terminals, and a token string $w = a_1 \cdots a_n$, return a [parse tree](/parse-tree/) of $w$ or report an error. This is the [parsing problem](/cfg-parsing-problem/) for a subclass of grammars. The relations are those of the [operator grammar](/operator-grammar/) page: $a \doteq b$ if $a$ and $b$ occur in one right side with at most a nonterminal between them, $a \lessdot b$ if $a B$ occurs in a right side and $b$ is a leading terminal of $B$, and $a \gtrdot b$ if $B b$ occurs and $a$ is a trailing terminal of $B$; the end markers are treated as the production $\$ S \$$.

## The algorithm

The stack holds $\$$ at the bottom, then terminals and nonterminal entries; since the grammar is an operator grammar, no two nonterminal entries are adjacent. The parser ignores nonterminal entries when it looks for the topmost terminal. Classic descriptions push a single placeholder for every nonterminal and do not check the reduced handle against the grammar. The version here keeps in each nonterminal entry the set of all nonterminals that can derive that part of the input, each with a tree, and a reduction looks up the productions whose right sides have the shape of the handle. This handles unit productions such as $E \to T$, which the precedence relations cannot see, and it makes the parser accept exactly $L(G)$.

```pseudo id=main
OP-PARSE(w)                                     ▷ the relations ⋖, ≐, ⋗ have no conflict
L1  push $; let a1 ... an $ be the input and point at a1
L2  loop: t ← the topmost terminal on the stack; b ← the current input token
L3      if t = $ and b = $ then accept if the stack is $ N with S ∈ N, else error
L4      if t ⋖ b or t ≐ b then push b and advance the input
L5      else if t ⋗ b then
L6          repeat pop the topmost terminal x, until the topmost terminal y has y ⋖ x
L7          the handle is everything above y, including the nonterminal entries
L8          push N, the set of all A with a production A → handle shape, closed under unit productions; error if N = ∅
L9      else report an error at b
```

At L8, the handle has the form $[N_0] \, a_i \, [N_1] \cdots a_j \, [N_k]$ with optional nonterminal entries. A production $A \to X_1 \cdots X_m$ matches it when its terminals are $a_i, \ldots, a_j$ in order, its nonterminals are where the entries are, and each of its nonterminals is in the corresponding entry. Then $A \in N$, and any $B$ with $B \to A$ is added too, and so on.

## Example

Take the expression grammar $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to ( E ) \mid id$, whose precedence matrix is computed on the [operator grammar](/operator-grammar/) page. The parse of $id * id + id$:

| stack | input | relation | action |
|---|---|---|---|
| $\$$ | $id * id + id \$$ | $\$ \lessdot id$ | shift |
| $\$ \ id$ | $* id + id \$$ | $id \gtrdot *$ | reduce $id$ to $\{F, T, E\}$ |
| $\$ \ \{E, F, T\}$ | $* id + id \$$ | $\$ \lessdot *$ | shift |
| $\$ \ \{E, F, T\} *$ | $id + id \$$ | $* \lessdot id$ | shift |
| $\$ \ \{E, F, T\} * id$ | $+ id \$$ | $id \gtrdot +$ | reduce $id$ to $\{F, T, E\}$ |
| $\$ \ \{E, F, T\} * \{E, F, T\}$ | $+ id \$$ | $* \gtrdot +$ | reduce by $T \to T * F$ to $\{T, E\}$ |
| $\$ \ \{E, T\}$ | $+ id \$$ | $\$ \lessdot +$ | shift |
| $\$ \ \{E, T\} +$ | $id \$$ | $+ \lessdot id$ | shift |
| $\$ \ \{E, T\} + id$ | $\$$ | $id \gtrdot \$$ | reduce $id$ to $\{F, T, E\}$ |
| $\$ \ \{E, T\} + \{E, F, T\}$ | $\$$ | $+ \gtrdot \$$ | reduce by $E \to E + T$ to $\{E\}$ |
| $\$ \ \{E\}$ | $\$$ | | accept |

At the sixth row, the pop of L6 removes $*$ and stops at $\$$, because $\$ \lessdot *$; the handle is $\{E, F, T\} * \{E, F, T\}$, which matches $T \to T * F$ with $T$ from the first entry and $F$ from the second. Then $E \to T$ adds $E$. The resulting tree is the usual one, with $id * id$ grouped under $T$.

The input $id \, id$ stops at once: there is no relation between $id$ and $id$. The input $+ \, id$ shows that errors can be found late: the parser shifts $+$ (since $\$ \lessdot +$) and $id$, reduces $id$, and only at the end finds the handle $+ \{E, F, T\}$, which matches no production.

## Correctness

Take a parse tree of a sentence and merge each chain of unit productions into one node. Every remaining inner node has at least one terminal child. Reverse the rightmost derivation of this tree: the next node to reduce is the leftmost one whose children are all ready. Its terminal children are consecutive terminals of the current string, related by $\doteq$; the terminal to its left is related by $\lessdot$ to its first terminal, and its last terminal is related by $\gtrdot$ to the terminal to its right; and each terminal on the stack to its left is related by $\lessdot$ or $\doteq$ to the next one. These facts come from the definitions of LEADING and TRAILING and from the operator form, which makes every nonterminal next to the handle belong to it. Since each pair of terminals has at most one relation, the parser shifts exactly until the end of this node and pops exactly its children, so it follows the tree. Its sets contain the labels of the tree's nodes, and every set entry comes with a real tree, so it accepts exactly the sentences. The full proof is below.

## Complexity

- **Steps.** Each shift reads one token, and each reduction removes at least one terminal from the stack, because every handle contains a terminal. So there are at most $n + 1$ shifts and $n$ reductions, and OP-PARSE stops after $O(n)$ steps.
- **Time.** A reduction pops its handle and tries the productions with the same shape, at most $O(|G|)$ work, then closes the set under unit productions in $O(|G|)$. The total is $O(n |G|)$, which is $O(n)$ for a fixed grammar. Without the label sets, as in the classic form, each step costs $O(1)$ amortized.
- **Building the table.** LEADING and TRAILING are computed by a fixed-point iteration in $O(|V| \cdot |G| \cdot |\Sigma|)$ time, and the relations by one pass over the right sides, $O(|G| \cdot |\Sigma|)$. The matrix has $(|\Sigma| + 1)^2$ cells.
- **Space.** The stack holds $O(n)$ entries; the trees in the sets share their subtrees, $O(n |G|)$ nodes in all.

## Properties

- **Deterministic and nonrecursive.** No backtracking, and the stack is explicit, so deep nesting needs no recursion.
- **No valid prefix property.** The parser can shift tokens that no sentence allows at that place, as $+ \, id$ above shows. LR parsers find every error at the first wrong token; operator-precedence parsers find it later, at a reduction.
- **Nonterminals are invisible to the relations.** The relations depend only on terminals, so unit productions and the names of nonterminals do not influence shifts and reductions. The classic form, which does not check the handle, accepts the language of the grammar with all nonterminals merged, which can be larger than $L(G)$.
- **Small grammar class.** Operator precedence grammars cannot have unary and binary uses of one operator, such as minus, without a conflict, and they cannot have empty productions. Their languages are deterministic.

## Variants and improvements

- **Precedence functions.** Instead of the matrix, store two integer functions $f$ and $g$ with $f(a) < g(b)$, $f(a) = g(b)$ or $f(a) > g(b)$ when $a \lessdot b$, $a \doteq b$ or $a \gtrdot b$. They exist when a graph built from the relations has no cycle, and the longest paths in it give the values. For the expression grammar, $f(id) = f(*) = f()) = 4$, $f(+) = 2$, $f(() = f(\$) = 0$, and $g(id) = g(() = 5$, $g(*) = 3$, $g(+) = 1$, $g()) = g(\$) = 0$. Two arrays replace the matrix, but the empty cells, which signal errors, are lost.
- **Declared precedence.** For an ambiguous grammar like $E \to E + E \mid E * E \mid id$, the matrix is written from declared precedence levels and associativities: $a \lessdot b$ if $b$ binds more tightly than $a$, or equally tightly and is right associative. The [shunting yard algorithm](/shunting-yard-algorithm/) and [Pratt parsing](/pratt-parsing/) are the same idea specialized to expressions.
- **Unary operators.** The lexer can give a unary minus its own token, using the previous token to decide, which removes the conflict.
- **Simple precedence.** Wirth and Weber (1966) defined the relations between all grammar symbols, so that the handle is found without the operator form.
- **Error recovery.** Errors are detected at two places, an empty cell (L9) and a handle that matches no production (L8); classic parsers attach a recovery routine to each empty cell, such as inserting a missing operand or operator, and can also use [panic-mode error recovery](/panic-mode-error-recovery/).

## When to use it

Use operator precedence for the expression part of a language, often inside a [recursive descent](/recursive-descent-parsing/) parser for the statements, when the operator table may change at run time, as with user-defined operators. For a whole language, or when precise error positions matter, an [LR parse table](/lr-parse-table/) handles a much larger class of grammars with the valid prefix property.

## Pitfalls

- **Pop until $\lessdot$, not until any relation.** L6 stops at the first terminal $y$ with $y \lessdot x$, where $x$ was popped last; stopping on $\doteq$ would cut a handle like $( E )$ in half.
- **Include the nonterminal below the handle.** The nonterminal entry between $y$ and the first popped terminal belongs to the handle, as the $E$ in $E + T$.
- **Ignoring unit productions.** A parser that reduces only by the shapes of the handles never builds the nodes of $E \to T$ or $T \to F$. It must close the label sets under unit productions, as here, or accept a skeletal tree.
- **The empty input.** An operator grammar has no empty productions, so $\varepsilon$ is never a sentence; OP-PARSE stops at L3 with a stack holding only $\$$ and reports an error.

## Implementations

## History

Floyd (1963) defined operator grammars and operator precedence grammars, and showed how a matrix of relations between terminals parses them. Precedence-based expression parsing was already in use in early compilers, and Dijkstra's shunting yard algorithm (1961) is a precursor. Wirth and Weber (1966) extended the relations to all symbols in simple precedence parsing. Operator-precedence parsing was a standard textbook method in the 1970s and 1980s, until LR parser generators, which also resolve expression grammars by declared precedence, took its place for complete languages.

## References
