---
tag: Y2PKTQ
kind: problem
slug: infix-to-postfix
name: Infix to postfix conversion
aliases:
- infix to RPN
- expression conversion
area: data-structures/linear-structures
level: intro
summary: Rewrite an infix arithmetic expression in postfix order respecting precedence and associativity.
prereqs: [stack, reverse-polish-notation]
see_also: [shunting-yard-algorithm, postfix-evaluation, reverse-polish-notation, expression-tree, operator-precedence-parsing, recursive-descent-parsing, dijkstra-two-stack-evaluation, balanced-parentheses]
sources:
  - paper: "Edsger W. Dijkstra, Algol 60 translation: an Algol 60 translator for the X1 and making a translator for Algol 60, Report MR 35/61, Mathematisch Centrum, Amsterdam (1961)"
    locator: the description of the translator with a stack of operators, later called the shunting-yard algorithm
  - book: isbn:9780321486813
    title: Aho, Lam, Sethi and Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Chapter 2, Sections 2.3 (Syntax-directed translation) and 2.5 (A translator for simple expressions), which translate infix expressions into postfix notation
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3, exercise 1.3.10 (InfixToPostfix) and exercise 1.3.11 (EvaluatePostfix)
---

Infix to postfix conversion is the problem of rewriting an arithmetic expression written in the usual infix form, such as `a * (b + c) - d / e`, in [postfix form](/reverse-polish-notation/), where each operator comes after its operands: `a b c + * d e / -`. The output must denote the same expression tree that the precedence and associativity rules give the input, and it needs no parentheses. Dijkstra's [shunting-yard algorithm](/shunting-yard-algorithm/) solves it in one left-to-right pass with a [stack](/stack/) of operators, in $\Theta(n)$ time. The postfix form is then evaluated with one stack by [postfix evaluation](/postfix-evaluation/), which is how calculators, interpreters and stack-machine compilers handle expressions.

## In plain words

In school we write `2 + 3 * 4` and know that the multiplication happens first, because of the rules of precedence. A machine finds it easier if each operation comes right after the two numbers it works on: `2 3 4 * +`. Read it from left to right: take 3 and 4, multiply them, then add 2 to the result. No parentheses and no precedence rules are needed.

The conversion keeps the numbers and names in the same order and only moves the operators to later places. The usual method holds back the operators on a pile and lets one out each time a weaker operator or a closing parenthesis shows that its operands are complete.

## Definition

**Input.** A sequence of $n$ tokens that form a correct infix expression. The tokens are operands (numbers or names), binary operators, and the parentheses `(` and `)`. Each operator has a precedence, a small integer, and an associativity, left or right. The usual table is: `^` with precedence 3 and right associativity; `*` and `/` with 2, left; `+` and `-` with 1, left.

**The meaning of the input.** The precedence and associativity rules and the parentheses determine one expression tree $T$ for the input: a higher precedence binds tighter, and among operators of equal precedence without parentheses, left associativity groups from the left ($a - b - c = (a - b) - c$) and right associativity from the right ($a \mathbin{\hat{}} b \mathbin{\hat{}} c = a \mathbin{\hat{}} (b \mathbin{\hat{}} c)$).

**Output.** The postfix form of $T$: its tokens in postorder, that is, the postfix form of the left subtree, then of the right subtree, then the operator at the root. A postfix string determines its tree, so the output is unique. It has no parentheses.

**Properties of every solution.** The operands appear in the same order as in the input. The output has the same number of operators as the input, and no parentheses.

## Variants

- **Fully parenthesized input.** Every operator with its two operands is in parentheses, as in `( 1 + ( 2 * 3 ) )`. Then no precedence table is needed: output each operand at once, push each operator, and pop one operator at each `)`. This is the core of [Dijkstra's two-stack evaluation](/dijkstra-two-stack-evaluation/).
- **Unary operators.** A `-` at the start or after `(` or after another operator is a unary minus. It needs its own token, a high precedence and right associativity.
- **Function calls.** Tokens such as `max ( a , b )` are handled by pushing the function name and treating the comma as the end of an argument.
- **Infix to prefix.** Reverse the input, swap `(` and `)`, convert with the roles of left and right associativity exchanged, and reverse the output. Or build the tree and print it in preorder.
- **Error detection.** Report unmatched parentheses, two operands in a row or two binary operators in a row. The shunting-yard algorithm finds the parenthesis errors as a side effect; the others need a check of the token types.
- **Direct code generation.** For a stack machine, the postfix form is the code: each operand becomes a push and each operator an instruction that pops two values and pushes one.

## Examples

**A trace of the shunting-yard algorithm** on `a * ( b + c ) - d / e`. The operator stack is written from the bottom to the top.

| token | action | output so far | stack after it |
|---|---|---|---|
| `a` | output | `a` | |
| `*` | push | `a` | `*` |
| `(` | push | `a` | `* (` |
| `b` | output | `a b` | `* (` |
| `+` | top is `(`, push | `a b` | `* ( +` |
| `c` | output | `a b c` | `* ( +` |
| `)` | pop to `(` | `a b c +` | `*` |
| `-` | pop `*` (precedence 2 ≥ 1), push | `a b c + *` | `-` |
| `d` | output | `a b c + * d` | `-` |
| `/` | top `-` is weaker, push | `a b c + * d` | `- /` |
| `e` | output | `a b c + * d e` | `- /` |
| end | pop all | `a b c + * d e / -` | |

**Associativity.**

| infix | postfix | tree |
|---|---|---|
| `a - b - c` | `a b - c -` | $(a - b) - c$ |
| `2 ^ 3 ^ 2` | `2 3 2 ^ ^` | $2^{(3^2)} = 512$ |
| `(a + b) * c` | `a b + c *` | $(a + b) \cdot c$ |
| `a + b * c - d` | `a b c * + d -` | $(a + (b \cdot c)) - d$ |

**A longer input.** `3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3` becomes `3 4 2 * 1 5 - 2 3 ^ ^ / +`. Its value is $3 + 8 / (-4)^8 = 3 + 8/65536 = 3.0001220703125$.

## Known algorithms

- **[Shunting-yard algorithm](/shunting-yard-algorithm/)** (Dijkstra, 1961). Read the tokens from left to right. Output each operand. Push `(`. At `)`, pop operators to the output until `(`, and drop the `(`. At an operator $o$, first pop to the output each operator $t$ on the top of the stack while $t$ has a higher precedence than $o$, or the same precedence and $o$ is left associative; then push $o$. At the end, pop all operators. Each token is pushed and popped at most once, so it costs $\Theta(n)$ time and $O(n)$ space for the stack.
- **Build the [expression tree](/expression-tree/), then print it in postorder.** A parser builds the tree, by [recursive descent](/recursive-descent-parsing/) with one procedure per precedence level, or by precedence climbing. Both are $\Theta(n)$. This route also gives the prefix and the fully parenthesized forms.
- **Syntax-directed translation.** A grammar for expressions with a semantic action that prints each operator after its operands. Aho, Lam, Sethi and Ullman build their first translator in this way. It is recursive descent where the output is printed instead of a tree built.
- **[Operator-precedence parsing](/operator-precedence-parsing/).** The general method of which the shunting-yard algorithm is a case, driven by a table of precedence relations between pairs of operators.

## Bounds

Every algorithm reads all $n$ tokens and writes the output, so $\Omega(n)$ time is needed, and the methods above are optimal. The output is at most $n$ tokens: it drops the parentheses and keeps the rest. The operator stack can hold $\Theta(n)$ items, as in `a ^ b ^ c ^ ... ^ z` or in deeply nested parentheses, and a recursive descent parser has the same recursion depth. With deep nesting, as in `a - ( b * ( c - ( d * e ) ) )`, the operators `-`, `*`, `-`, `*` all wait until the end, and a one-pass method must remember their order, so it needs memory that grows with the nesting depth.

## Reductions

- **To and from expression trees.** The postfix form is the postorder of the [expression tree](/expression-tree/), and a postfix string gives back its tree with one stack. So the problem is the same as parsing the infix form into a tree.
- **[Postfix evaluation](/postfix-evaluation/).** Conversion followed by evaluation computes the value of an infix expression. [Dijkstra's two-stack evaluation](/dijkstra-two-stack-evaluation/) does both at once: it applies each operator when the shunting-yard algorithm would output it.
- **[Balanced parentheses](/balanced-parentheses/).** The conversion checks the balance of the parentheses as a side effect: a `)` with no `(` on the stack, or a `(` left at the end, is an error.

## Applications

- **Calculators and interpreters** convert expressions to postfix or to a tree before they evaluate them. Hewlett-Packard calculators take postfix input directly.
- **Compilers for stack machines.** The Java virtual machine, the .NET runtime, Forth and PostScript run code in postfix order, and the expression part of a compiler for them is this conversion.
- **Spreadsheets and formula engines** parse cell formulas with a precedence table and evaluate them in postfix order.

## References
