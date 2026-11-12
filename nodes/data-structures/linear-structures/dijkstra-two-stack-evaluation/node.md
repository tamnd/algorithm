---
tag: 9KN9AK
kind: algorithm
slug: dijkstra-two-stack-evaluation
name: Dijkstra's two-stack expression evaluation
aliases:
- Dijkstra's two-stack algorithm for expression evaluation
area: data-structures/linear-structures
level: intro
summary: Evaluates a fully parenthesized arithmetic expression using one stack for operands and another for operators.
prereqs: [stack]
see_also: [shunting-yard-algorithm, postfix-evaluation, infix-to-postfix, reverse-polish-notation, expression-tree, balanced-parentheses, recursive-descent-parsing, pushdown-automaton]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3, Arithmetic expression evaluation, the program Evaluate (Dijkstra's two-stack algorithm for expression evaluation) and the trace of ( 1 + ( ( 2 + 3 ) * ( 4 * 5 ) ) ); exercise 1.3.9 on the missing left parentheses
  - paper: "Edsger W. Dijkstra, Algol 60 translation: an Algol 60 translator for the X1 and making a translator for Algol 60, Report MR 35/61, Mathematisch Centrum, Amsterdam (1961)"
    locator: the translation of expressions with a stack of operators
  - paper: "Klaus Samelson and Friedrich L. Bauer, Sequential formula translation, Communications of the ACM 3(2) (1960)"
    locator: the stack principle (cellar) for the translation and evaluation of formulas
---

Dijkstra's two-stack algorithm evaluates a fully parenthesized arithmetic expression, such as `( 1 + ( ( 2 + 3 ) * ( 4 * 5 ) ) )`, in one left-to-right pass with two [stacks](/stack/): one for values and one for operators. It pushes each number on the value stack and each operator on the operator stack, ignores each left parenthesis, and at each right parenthesis pops one operator and two values, applies the operator and pushes the result. At the end, the value stack holds the value of the expression. It runs in $\Theta(n)$ time for $n$ tokens, with stacks no deeper than the nesting of the expression. It is the simplest case of the stack method of Samelson, Bauer and Dijkstra, and Sedgewick and Wayne use it to introduce stacks.

## In plain words

Write a sum with a pair of brackets around every operation, like `( 1 + ( 2 * 3 ) )`. Keep two piles of cards: one for numbers and one for the signs `+`, `-`, `*` and `/`. Read the sum from left to right. Put each number on the number pile and each sign on the sign pile. Skip each opening bracket.

Each closing bracket means "the operation inside these brackets is complete". So take the top sign and the top two numbers, work out the answer, and put it back on the number pile. When you reach the end, one number is left, and that is the value of the whole sum.

## The problem

**Input.** A sequence of $n$ tokens that forms a fully parenthesized expression, by the grammar

$$E \to \textit{number} \mid (\; E \;\textit{op}\; E \;),$$

where $\textit{op}$ is one of `+`, `-`, `*`, `/`. Every operator, with its two operands, is inside its own pair of parentheses, so the input needs no precedence rules.

**Output.** The value $\text{val}(E)$, defined by $\text{val}(\textit{number}) = \text{the number}$ and $\text{val}((E_1 \textit{ op } E_2)) = \text{val}(E_1) \textit{ op } \text{val}(E_2)$.

## The algorithm

```pseudo id=main
EVALUATE(t₁, …, tₙ)
L1  vals ← an empty stack, ops ← an empty stack
L2  for each token t in order
L3      if t = "(" then do nothing
L4      else if t is an operator then PUSH(ops, t)
L5      else if t = ")" then
L6          op ← POP(ops), b ← POP(vals), a ← POP(vals)
L7          PUSH(vals, a op b)
L8      else PUSH(vals, the number t)
L9  return POP(vals)
```

Line L6 pops the right operand $b$ first, because it was pushed last. For `-` and `/`, the result is $a - b$ and $a / b$, not the other order. Line L3 ignores the left parentheses: the right parentheses alone mark where each operation ends, and the operator stack remembers which operator it is.

## Example

The input is `( 1 + ( ( 2 + 3 ) * ( 4 * 5 ) ) )`, 17 tokens. The stacks are written from the bottom to the top.

| token | action | vals | ops |
|---|---|---|---|
| `(` | ignore | | |
| `1` | push 1 | 1 | |
| `+` | push + | 1 | + |
| `(` `(` | ignore | 1 | + |
| `2` | push 2 | 1 2 | + |
| `+` | push + | 1 2 | + + |
| `3` | push 3 | 1 2 3 | + + |
| `)` | $2 + 3 = 5$ | 1 5 | + |
| `*` | push * | 1 5 | + * |
| `(` | ignore | 1 5 | + * |
| `4` | push 4 | 1 5 4 | + * |
| `*` | push * | 1 5 4 | + * * |
| `5` | push 5 | 1 5 4 5 | + * * |
| `)` | $4 \cdot 5 = 20$ | 1 5 20 | + * |
| `)` | $5 \cdot 20 = 100$ | 1 100 | + |
| `)` | $1 + 100 = 101$ | 101 | |

Line L9 returns 101. The deepest point has 4 values and 3 operators, which is the nesting depth of the expression.

## Correctness

The proof is by structural induction on the grammar. The claim is: if the algorithm starts to read a complete subexpression $E$ with stacks $V$ and $O$, then after reading it the stacks are $V$ with $\text{val}(E)$ pushed on top, and $O$ unchanged. For a number, line L8 pushes it. For $(E_1 \textit{ op } E_2)$, the `(` changes nothing, $E_1$ leaves $\text{val}(E_1)$ on $V$, line L4 pushes $\textit{op}$, $E_2$ leaves $\text{val}(E_2)$ above it, and the `)` pops exactly these three and pushes $\text{val}(E_1) \textit{ op } \text{val}(E_2)$. Applied to the whole input with empty stacks, the claim gives a value stack holding only $\text{val}(E)$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| measure | bound |
|---|---|
| time | $\Theta(n)$: one step per token and one operation per `)` |
| pushes and pops | each number and each result is pushed once and popped at most once |
| space | $O(d)$ for nesting depth $d$; at most $d + 1$ values and $d$ operators |

An expression with $m$ operators has $m + 1$ numbers and $2m$ parentheses, so $n = 4m + 1$. Each operator is applied exactly once. The depth $d$ is at most $m$, reached by expressions such as `( 1 + ( 1 + ( 1 + 1 ) ) )`.

## Properties

- **One pass, no lookahead.** Each token is read once, and the action depends only on the token and the stack tops.
- **Left parentheses are not needed.** Line L3 ignores them, so the algorithm also evaluates the expression with all `(` removed, such as `1 + 2 + 3 ) * 4 * 5 ) ) )`. The right parentheses carry all the structure.
- **No precedence table.** The parentheses fix the order of the operations. On input without full parentheses, the algorithm gives wrong results; see Pitfalls.
- **It is postfix evaluation in disguise.** The operators are applied in the order in which [infix-to-postfix conversion](/infix-to-postfix/) of the same input would output them, so the algorithm is the shunting-yard conversion and [postfix evaluation](/postfix-evaluation/) run together.

## Variants and improvements

- **Unary operators.** For an operator such as `sqrt`, written `( sqrt E )`, line L6 pops one value instead of two. Sedgewick and Wayne's version includes `sqrt`.
- **Precedence and associativity.** To accept input such as `1 + 2 * 3`, apply operators also when a new operator arrives: before pushing operator $o$, pop and apply each operator on top with a higher precedence, or an equal precedence when $o$ is left associative, and push `(` as a marker that stops this. This is the [shunting-yard algorithm](/shunting-yard-algorithm/) with evaluation in place of output.
- **Build a tree instead of a value.** Push trees on the value stack, and at `)` push a node with the operator and the two popped trees. This builds the [expression tree](/expression-tree/).
- **Error checks.** Report an error when a pop finds an empty stack, or when the stacks at the end are not one value and no operator. This also checks that the right parentheses are balanced against the operators.
- **Recursive form.** A recursive procedure for the grammar rule $E \to (E \textit{ op } E)$ does the same work with the call stack in place of the two explicit stacks. This is [recursive descent](/recursive-descent-parsing/).

## When to use it

Use the two-stack algorithm when the input is fully parenthesized, as in a teaching example or in data written by a program, or as the first step toward a full expression evaluator. For input written by people, with precedence rules, use the shunting-yard form or a recursive descent parser. If the expression is evaluated many times with different variable values, build a tree or a postfix program once and evaluate that.

## Pitfalls

- **Operands in the wrong order.** Popping $a$ before $b$ in line L6 computes $b - a$ and $b / a$. The first pop is the right operand.
- **Input without full parentheses.** On `( 1 + 2 * 3 )`, the one `)` applies `*` and pushes 6, and line L9 returns 6, while 1 and `+` stay on the stacks. The value by the rules of precedence is 7. Check that the input is fully parenthesized, or check at the end that exactly one value and no operator remain.
- **Integer division.** In languages with integer `/`, `( 7 / 2 )` gives 3. Use the number type that the problem asks for.
- **Multi-character tokens.** A scanner that reads one character at a time splits `12` into `1` and `2`. Split the input into tokens first.

## Implementations

## History

Samelson and Bauer described the use of a stack, which they called a cellar, for translating and evaluating formulas in 1959 and 1960, and they had filed a patent on it in 1957. Dijkstra's 1961 report on the ALGOL 60 translator for the X1 computer used a stack of operators to translate expressions with precedence, the method later called the shunting-yard algorithm. Sedgewick and Wayne present the version for fully parenthesized input under the name "Dijkstra's two-stack algorithm" as the first application of stacks in their book.

## References
