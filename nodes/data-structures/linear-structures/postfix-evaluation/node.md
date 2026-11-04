---
tag: XVTXFV
kind: algorithm
slug: postfix-evaluation
name: Postfix expression evaluation
area: data-structures/linear-structures
level: intro
summary: Evaluates an expression in postfix notation by scanning left to right and using a stack to hold operands.
model: word-ram
complexity:
  vars: {m: the number of tokens}
  time: {worst: Θ(m), best: Θ(m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, online: true, recursive: false, in_place: false}
prereqs: [stack, reverse-polish-notation, loop-invariant]
see_also: [reverse-polish-notation, infix-to-postfix, shunting-yard-algorithm, dijkstra-two-stack-evaluation, expression-tree, balanced-parentheses]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3, Bags, queues, and stacks (Exercise 1.3.11, evaluation of a postfix expression with a stack)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.1, Stacks, queues, and deques, and Section 2.3.3, Other representations of trees (postorder with degrees)
  - paper: doi:10.1093/comjnl/5.3.210
    title: C. L. Hamblin, Translation to and from Polish notation, The Computer Journal 5(3) (1962)
    locator: pp. 210 to 213
  - paper: "Arthur W. Burks, Don W. Warren and Jesse B. Wright, An analysis of a logical machine using parenthesis-free notation, Mathematical Tables and Other Aids to Computation 8(46) (1954)"
    locator: pp. 53 to 57
---

Postfix evaluation computes the value of an expression in [reverse Polish notation](/reverse-polish-notation/) with one left-to-right scan and a [stack](/stack/) of values: an operand is pushed, and an operator pops its operands and pushes its result. For $m$ tokens it takes $\Theta(m)$ time when each operator costs $O(1)$, and $\Theta(m)$ extra space in the worst case. It also decides whether the string is a well-formed postfix expression, with no extra work. It is how stack machines, calculators that use RPN, and the second half of the classic infix pipeline ([infix to postfix](/infix-to-postfix/), then evaluate) work.

## In plain words

Read the expression from left to right and keep a pile of numbers. When you read a number, put it on top of the pile. When you read an operator such as plus, take the top two numbers off the pile, add them, and put the sum back on top. The number that was on top is the right-hand operand, and the one below it is the left-hand operand. This matters for minus and for division.

When the input ends, exactly one number should be on the pile, and that number is the answer. If an operator finds too few numbers on the pile, or if more than one number is left at the end, the expression was not written correctly.

## The problem

**Input.** A string $s_1 \cdots s_m$ of tokens. Each token is an operand with a value in a set $D$, or an operator $\omega$ with a known arity $\operatorname{ar}(\omega) \ge 1$ and a function $f_\omega : D^{\operatorname{ar}(\omega)} \to D$.

**Output.** If the string is a postfix expression (the set $\mathcal{P}$ of the [reverse Polish notation](/reverse-polish-notation/) page), its value, defined by $\operatorname{val}(v) = v$ for an operand and

$$\operatorname{val}(E_1 \cdots E_k\, \omega) = f_\omega(\operatorname{val}(E_1), \ldots, \operatorname{val}(E_k)).$$

The value is well defined, because each postfix expression splits into $E_1, \ldots, E_k, \omega$ in exactly one way. If the string is not in $\mathcal{P}$, the output is an error.

## The algorithm

```pseudo id=main
POSTFIX-EVAL(s, m)                         ▷ tokens s[1 .. m]
L1  S ← an empty stack
L2  for j ← 1 to m do
L3      if s[j] is an operand then PUSH(S, s[j])
L4      else ω ← s[j]; k ← ar(ω)
L5          if |S| < k then error "too few operands"
L6          pop y[k], y[k − 1], ..., y[1] from S      ▷ the top is the last operand
L7          PUSH(S, f_ω(y[1], ..., y[k]))
L8  if |S| ≠ 1 then error "not one expression"
L9  return POP(S)
```

Line L3 handles an operand. Lines L4 to L7 handle an operator of arity $k$: the top of the stack is its last operand, so the pops of line L6 fill $y$ from the right. For a binary operator, line L6 pops $b = y[2]$ first and then $a = y[1]$, and line L7 pushes $f_\omega(a, b)$, for example $a - b$. Line L5 catches an operator with too few operands, and line L8 catches a string that leaves zero or several values.

## Example

Evaluate `5 1 2 + 4 × + 3 −`, the postfix form of $5 + (1 + 2) \times 4 - 3$.

| $j$ | token | action | stack after (bottom to top) |
|---|---|---|---|
| 1 | 5 | push | 5 |
| 2 | 1 | push | 5, 1 |
| 3 | 2 | push | 5, 1, 2 |
| 4 | + | pop 2 and 1, push $1 + 2 = 3$ | 5, 3 |
| 5 | 4 | push | 5, 3, 4 |
| 6 | × | pop 4 and 3, push $3 \times 4 = 12$ | 5, 12 |
| 7 | + | pop 12 and 5, push $5 + 12 = 17$ | 17 |
| 8 | 3 | push | 17, 3 |
| 9 | − | pop 3 and 17, push $17 - 3 = 14$ | 14 |

Line L8 finds one value, and the result is 14. The height of the stack after each token is $1, 2, 3, 2, 3, 2, 1, 2, 1$, the prefix sums of the counting test of the [reverse Polish notation](/reverse-polish-notation/) page. On `3 4 + +`, the stack is $[7]$ when the second `+` arrives, and line L5 reports too few operands. On `3 4`, line L8 finds two values.

## Correctness

The key [loop invariant](/loop-invariant/) is about the prefix $s_1 \cdots s_j$ that has been read: if no error has occurred, this prefix is a concatenation $F_1 \cdots F_p$ of $p$ postfix expressions, and the stack holds $\operatorname{val}(F_1), \ldots, \operatorname{val}(F_p)$ from the bottom to the top. An operand adds a new $F_{p+1}$. An operator of arity $k \le p$ joins the last $k$ of them into one postfix expression by rule 2 of the definition, and line L7 pushes its value. The algorithm reports an error exactly when some prefix has fewer values than its operator needs, or when the final count is not 1, which by the counting test is exactly when the string is not a postfix expression. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Each token causes one push. Each pop of line L6 or line L9 removes a value that a push put there, so the total number of pops is at most $m$. With a stack on an array or a linked list, each push and pop costs $O(1)$. If each $f_\omega$ costs $O(1)$, as for fixed-width integers on the [word RAM](/word-ram/), the time is $\Theta(m)$ in every case: each token is read once, which gives the lower bound, and the work per token is $O(1)$ amortized. Operators of large arity are covered by the same count, because their pops are paid by earlier pushes.

The extra space is the largest height of the stack. It is at most the number of operands, so $O(m)$. It is $\Theta(m)$ in the worst case: the string `1 2 3 ⋯ n + + ⋯ +` with $n$ operands and $n - 1$ plus signs has $m = 2n - 1$ tokens and reaches the height $n = (m + 1)/2$. A string whose tree leans to the left, such as `1 2 + 3 + 4 +`, never has more than 2 values on the stack.

With numbers of unbounded size, the cost of the arithmetic is added: the stack work stays $\Theta(m)$, and each $f_\omega$ costs what the number type costs.

## Properties

- **One pass, online.** Each token is used when it is read, so the algorithm can run on a stream and needs no look-ahead.
- **No recursion.** The stack replaces the recursion of an evaluator on the expression tree, so deep expressions do not overflow the call stack.
- **Validation for free.** The same scan decides membership in $\mathcal{P}$.
- **Order of operands kept.** The algorithm never reorders operands, so it is correct for non-commutative operators.

## Variants and improvements

- **Prefix (Polish) notation.** Scan from right to left with the same stack. Then the top of the stack is the *first* operand, so line L6 fills $y$ from the left.
- **Build a tree instead of a value.** Push leaf nodes in line L3, and in line L7 push a new node with the popped nodes as children. This builds the [expression tree](/expression-tree/) in $\Theta(m)$ time.
- **Code generation.** Emit "load" for an operand and the operator instruction for an operator. The result is code for a stack machine, and the evaluation is the run of that code.
- **From infix.** Convert first with the [shunting-yard algorithm](/shunting-yard-algorithm/), or evaluate infix directly with [Dijkstra's two-stack algorithm](/dijkstra-two-stack-evaluation/), which merges the two scans.
- **Variadic operators.** An operator such as "sum of all" with a count in the token pops that many values. The counting test then uses the count of each token as its arity.

## When to use it

Use postfix evaluation when the expression is already in postfix form: the output of a parser or of the shunting-yard algorithm, an RPN calculator, or stack machine code. It is simpler and faster than a recursive evaluator on a tree, and it needs no parentheses. For infix input given once, the two-stack method avoids the intermediate string. When the same expression is evaluated many times with different variable values, keep the postfix string (or the code) and run the scan each time.

## Pitfalls

- **Operand order.** Line L6 pops the right operand first. Writing line L7 for a binary operator as $f_\omega(\text{first pop}, \text{second pop})$ computes $b - a$ for `a b −`. The test `7 2 −` must give 5, not $-5$, and `8 2 /` must give 4.
- **No check of the stack height.** Without line L5, `3 +` pops an empty stack. Without line L8, `3 4` returns 4 and hides the error. Test both.
- **A unary minus that uses the binary symbol.** If `−` can mean both negation and subtraction, the arity of a token is not known, and `3 4 −` has two readings. Use a distinct token such as `neg`, and tokenize a negative number such as `-3` as one operand.
- **Division.** A division by zero must be reported, not left to crash the program. Integer division must be defined for negative operands (truncation or floor), because languages differ.
- **Tokenizing.** `12 3 +` and `1 23 +` differ only in a space. Split on white space, or a multi-digit number becomes several operands.

## Implementations

## History

Burks, Warren and Wright analysed a logical machine for a parenthesis-free notation in 1954. Hamblin used the reverse form for computer code in Australia, and his 1962 paper in The Computer Journal treats translation to and from both the prefix and the postfix form. Sedgewick and Wayne give the stack evaluation as an exercise next to Dijkstra's two-stack algorithm.

## References
