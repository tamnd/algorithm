---
tag: 2TMV07
kind: algorithm
slug: shunting-yard-algorithm
name: Shunting-yard algorithm
aliases:
- Dijkstra's shunting yard
- Dijkstra's shunting-yard algorithm
area: automata-and-parsing/context-free-parsing
level: intro
summary: Converts infix expressions to postfix or builds expression trees using an operator stack.
solves: [infix-to-postfix]
model: word-ram
complexity:
  vars: {n: the number of tokens of the input}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1961
  people: [Edsger W. Dijkstra]
  note: Dijkstra described the operator stack in the 1961 report on his ALGOL 60 translator for the X1 computer.
prereqs: [stack, reverse-polish-notation]
see_also: [infix-to-postfix, pratt-parsing, operator-precedence-parsing, postfix-evaluation, expression-tree, shift-reduce-parsing, recursive-descent-parsing, operator-grammar]
sources:
  - url: https://www.cs.utexas.edu/~EWD/MCReps/MR35.PDF
    title: Edsger W. Dijkstra, Algol 60 translation, An Algol 60 translator for the X1 and making a translator for Algol 60, Report MR 35/61, Mathematisch Centrum, Amsterdam, 1961
    locator: the description of the translation of expressions with a stack of operators and their priorities
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 2.3, Syntax-Directed Translation (postfix notation); Section 4.8.1, Precedence and Associativity to Resolve Conflicts
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 9.2, Precedence Parsing (operator precedence)
---

The shunting-yard algorithm reads an infix expression from left to right and outputs it in [postfix form](/reverse-polish-notation/), with each operator after its two operands. It keeps the operators that are not yet complete on a [stack](/stack/), and it uses the precedence and the associativity of the operators to decide when an operator leaves the stack. It solves [infix to postfix conversion](/infix-to-postfix/) in $\Theta(n)$ time for $n$ tokens. Edsger Dijkstra described it in 1961 for his ALGOL 60 translator, and it is still the standard way to parse expressions in calculators and small interpreters.

## In plain words

Think of a railway yard. The numbers and names of the expression are wagons that go straight through to the exit track. The operators are wagons that must wait on a side track, because each one must leave after both of its operands.

When a new operator arrives, it looks at the operator at the end of the side track. If that one binds at least as tightly (for example a times sign when a plus arrives), both of its operands have now passed, so it goes to the exit. This repeats, and then the new operator waits on the side track. An open parenthesis waits too, and it acts as a wall. A closing parenthesis sends out all operators back to the wall, and both parentheses are dropped. At the end of the input, all waiting operators go out.

## The problem

The input is a sequence of $n$ tokens: operands, the parentheses `(` and `)`, and binary operators. Each operator $o$ has a precedence $\text{prec}(o)$, an integer where a larger value binds tighter, and each precedence level is either left associative or right associative. The usual table is `^` with precedence 3 and right associativity, `*` and `/` with 2, left, and `+` and `-` with 1, left.

The meaning of the input is the unique parse tree of the precedence grammar. For the usual table, in the notation of the [context-free grammar](/context-free-grammar/) page (productions $A \to \alpha \mid \beta$, start symbol $S$, here $E$), it is

$$E \to E + T \mid E - T \mid T, \qquad T \to T * F \mid T / F \mid F, \qquad F \to P \,\hat{}\, F \mid P, \qquad P \to (\,E\,) \mid \text{id}.$$

A left-recursive level groups from the left ($a - b - c = (a - b) - c$), and a right-recursive level groups from the right ($a \,\hat{}\, b \,\hat{}\, c = a \,\hat{}\, (b \,\hat{}\, c)$). The output is the [postfix form](/reverse-polish-notation/) of the [expression tree](/expression-tree/): the postfix form of the left operand, then of the right operand, then the operator. If the input is not an expression of the grammar, the output is an error.

## The algorithm

We write $o \sqsupset t$, "$o$ pops $t$", when the operator $o$ on the stack must be output before the new operator $t$ is pushed:

$$o \sqsupset t \iff \text{prec}(o) > \text{prec}(t) \ \text{ or } \ \bigl(\text{prec}(o) = \text{prec}(t) \text{ and } t \text{ is left associative}\bigr).$$

```pseudo id=main
SHUNTING-YARD(tokens)
L1  out ← empty list;  ops ← empty stack
L2  for each token t of tokens, from left to right do
L3      if t is an operand then append t to out
L4      else if t = "(" then push t on ops
L5      else if t = ")" then
L6          while top(ops) ≠ "(" do append pop(ops) to out      ▷ error if ops becomes empty
L7          pop(ops)                                             ▷ drop the "("
L8      else                                                     ▷ t is a binary operator
L9          while ops is not empty and top(ops) is an operator o with o ⊐ t do
L10             append pop(ops) to out
L11         push t on ops
L12 while ops is not empty do
L13     if top(ops) = "(" then error                             ▷ a "(" without its ")"
L14     append pop(ops) to out
L15 return out
```

An operand goes to the output at once (line L3), so the operands keep their order. An operator waits on the stack until the next operator that does not bind more tightly to the right (lines L9 and L10), until the `)` of its group (line L6), or until the end of the input (line L12). An open parenthesis on the stack stops the loop of line L9, because it is not an operator, so the operators inside a pair of parentheses never pop the ones outside.

The pseudocode assumes that operands and operators alternate. The implementation adds the check that makes the algorithm reject every malformed input: a flag says whether the next token must be an operand or `(`, or must be an operator or `)`. Without it, the input `a b +` is accepted and gives `a b +`.

## Example

Convert `a + b * ( c - d ) ^ e ^ f - g`. The table shows the output and the stack (bottom on the left) after each token.

| token | action | output | stack |
|---|---|---|---|
| a | output | a | |
| + | push | a | + |
| b | output | a b | + |
| * | + does not pop *, push | a b | + * |
| ( | push | a b | + * ( |
| c | output | a b c | + * ( |
| - | the ( stops the loop, push | a b c | + * ( - |
| d | output | a b c d | + * ( - |
| ) | pop - , drop ( | a b c d - | + * |
| ^ | * does not pop ^, push | a b c d - | + * ^ |
| e | output | a b c d - e | + * ^ |
| ^ | ^ is right associative, so ^ does not pop ^, push | a b c d - e | + * ^ ^ |
| f | output | a b c d - e f | + * ^ ^ |
| - | pop ^, ^, *, + (each binds at least as tightly), push | a b c d - e f ^ ^ * + | - |
| g | output | a b c d - e f ^ ^ * + g | - |
| end | pop - | a b c d - e f ^ ^ * + g - | |

The result `a b c d - e f ^ ^ * + g -` is the postfix form of $(a + b * ((c - d) \,\hat{}\, (e \,\hat{}\, f))) - g$. At the second `-`, the stack holds the right spine of the tree read so far, and all four operators on it have precedence at least 1, so all four complete their right operand there.

## Correctness

**Claim.** On an input that is an expression of the precedence grammar, SHUNTING-YARD returns the postfix form of its parse tree. On any other input, the implementation reports an error.

The key invariant is about the stack. Consider a part of the input without parentheses at the top level, $x_0\, o_1\, x_1 \cdots o_j\, x_j$, where each $x_i$ is an operand or a group in parentheses. After the algorithm reads it, the stack above the group's `(` (or above the bottom) holds exactly the operators on the right spine of the tree of $x_0 \cdots x_j$, from the root at the bottom to the deepest at the top. The output holds the postfix form of that tree without these spine operators. A new operator $t$ attaches its left operand to the highest spine node from which every operator below pops $t$, and these operators form the top part of the stack, which is exactly what lines L9 and L10 output. The full proof, with the lemma that defines the tree by its root and the case analysis on precedence and associativity, is in [the correctness proof](proofs/correctness.md).

## Complexity

**Time.** Each token is handled once by the loop of line L2. Each operator and each `(` is pushed once, at line L4 or L11, and popped at most once, at line L6, L7, L10 or L14. A loop test that does not pop happens at most once for each token at lines L6 and L9, and once at line L12. So the total work is at most a constant times $n$, and it is at least $n$ because each token is read. The time is $\Theta(n)$ on the [word RAM](/word-ram/) in the best and the worst case, with a precedence lookup in $O(1)$ time.

**Space.** The stack holds at most $n$ tokens and the output has at most $n$ tokens, so the extra space is $O(n)$. The stack can really grow that large: on `( ( ( … a … ) ) )` or on `a ^ a ^ … ^ a`, it holds about half of the input.

## Properties

- **One pass, online.** The algorithm reads each token once from left to right and outputs operands at once. An operator is output when the first token arrives that completes it.
- **No recursion.** The explicit stack replaces the recursion of a [recursive descent parser](/recursive-descent-parsing/), so deep nesting does not overflow the call stack.
- **Table driven.** Adding an operator only adds a row to the precedence table. The grammar is not written down.
- **It is a shift-reduce parser.** Pushing an operator is a shift, and popping one to the output is a reduction of the handle $E\, o\, E$. The test $o \sqsupset t$ is the operator precedence relation of [operator-precedence parsing](/operator-precedence-parsing/).

## Variants and improvements

- **Build a tree.** Keep a second stack of trees instead of the output list. An operand pushes a leaf, and each pop of an operator $o$ pops two trees $r$ and $l$ and pushes the node $o(l, r)$. If the trees are replaced by their values, the same loop evaluates the expression directly.
- **Unary operators.** A prefix `-` is detected by position: it appears where an operand is expected. Give it its own token and a precedence, and treat it as a right-associative operator with no left operand. A postfix operator such as `!` goes to the output at once after popping the operators that bind more tightly.
- **Function calls.** A name followed by `(` is pushed as a function token, commas pop the operators back to the `(`, and the `)` also pops the function token to the output. Counting the commas gives the number of arguments.
- **Mixed-associativity levels.** If one level mixes left and right associative operators, the grouping of `a o b p c` is not defined. Require one associativity per level, as the implementation does.
- **Pratt parsing.** [Pratt parsing](/pratt-parsing/) uses the same binding powers in a recursive top-down form, which makes prefix, postfix and mixfix operators easier to add.

## When to use it

Use the shunting-yard algorithm when you parse arithmetic or logic expressions with a fixed set of binary operators and you want a short loop with no recursion, for example in a calculator, a spreadsheet formula engine or a configuration language. For a full programming language, embed it in a [recursive descent parser](/recursive-descent-parsing/) for the statements, or use [Pratt parsing](/pratt-parsing/), which handles prefix and mixfix operators more cleanly. A generated LR parser with precedence declarations, as in yacc, does the same work for a general grammar.

## Pitfalls

- **Wrong test for associativity.** The test must pop on equal precedence only when the new operator is left associative. Writing `prec(top) ≥ prec(t)` for all operators in line L9 makes `a ^ b ^ c` into `a b ^ c ^`, which is $(a \,\hat{}\, b) \,\hat{}\, c$. Writing `prec(top) > prec(t)` for all operators makes `a - b - c` into `a b c - -`, which is $a - (b - c)$.
- **Popping past a parenthesis.** The loop of line L9 must stop at `(`. Without the test "top(ops) is an operator", `a * ( b + c )` pops the `*` when `+` arrives and gives a wrong tree.
- **Unchecked errors.** The plain algorithm accepts `a b +`, and on `a )` line L6 pops an empty stack. Check that operands and operators alternate, that line L6 never pops an empty stack, and that line L13 finds no `(` at the end.
- **Unary minus.** Treating the `-` of `- a + b` as binary makes the first operator miss its left operand. Decide unary or binary from the expected-token flag.

## Implementations

## History

Dijkstra described the method in the 1961 report of the Mathematisch Centrum in Amsterdam on the ALGOL 60 translator for the Electrologica X1 that he wrote with Jaap Zonneveld. The report translates expressions with a stack of operators. The name compares the stack with the side track of a railway yard where wagons are reordered.

## References
