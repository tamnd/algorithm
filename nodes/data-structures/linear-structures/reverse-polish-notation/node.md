---
tag: 6TF3TJ
kind: definition
slug: reverse-polish-notation
name: Reverse Polish notation
aliases:
- postfix notation
- RPN
area: data-structures/linear-structures
level: intro
summary: Notation that writes operators after their operands, so no parentheses are needed.
prereqs: [structural-induction]
see_also: [postfix-evaluation, infix-to-postfix, shunting-yard-algorithm, expression-tree, dijkstra-two-stack-evaluation, stack, abstract-syntax-tree]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.3, Other representations of trees (sequential postorder with degrees)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3, Bags, queues, and stacks (Dijkstra's two-stack algorithm and the exercises on infix to postfix and postfix evaluation)
  - paper: "Arthur W. Burks, Don W. Warren and Jesse B. Wright, An analysis of a logical machine using parenthesis-free notation, Mathematical Tables and Other Aids to Computation 8(46) (1954)"
    locator: pp. 53 to 57
  - paper: doi:10.1093/comjnl/5.3.210
    title: C. L. Hamblin, Translation to and from Polish notation, The Computer Journal 5(3) (1962)
    locator: pp. 210 to 213
---

Reverse Polish notation, or postfix notation, writes each operator after its operands: the infix expression $(3 + 4) \times 2$ becomes `3 4 + 2 ×`. It is the reverse of the prefix notation that Jan Łukasiewicz used for logic in the 1920s, from which it takes its name. Burks, Warren and Wright analysed a logical machine that reads a parenthesis-free notation in 1954, and Hamblin used both the prefix and the reverse form for computer code. A well-formed postfix string has exactly one reading, so it needs no parentheses and no precedence rules, and a single left-to-right scan with a [stack](/stack/) evaluates it, as in [postfix evaluation](/postfix-evaluation/). The postfix string of an expression is the postorder of its [expression tree](/expression-tree/).

## Definition

Fix a set $V$ of *operands* (numbers or names) and a set $\Omega$ of *operators*, where each operator $\omega \in \Omega$ has an *arity* $\operatorname{ar}(\omega) \ge 1$. Operands and operators are *tokens*, and $V \cap \Omega = \emptyset$. An operator of arity 0, such as a constant, is treated as an operand.

**Postfix expressions.** The set $\mathcal{P}$ of postfix expressions is the smallest set of finite token strings such that:

1. each operand $v \in V$, as a string of length one, is in $\mathcal{P}$;
2. if $\omega \in \Omega$ has arity $k$ and $E_1, \ldots, E_k \in \mathcal{P}$, then the concatenation $E_1 E_2 \cdots E_k\, \omega$ is in $\mathcal{P}$.

**From trees.** For an expression tree $e$, with operands at the leaves and an operator of arity $k$ at each node with $k$ ordered children, the postfix form is defined by structural recursion:

$$\operatorname{post}(v) = v, \qquad \operatorname{post}(\omega(e_1, \ldots, e_k)) = \operatorname{post}(e_1) \cdots \operatorname{post}(e_k)\, \omega.$$

This is the postorder of the tree. The prefix (Polish) form puts $\omega$ first instead: $\omega\, \operatorname{pre}(e_1) \cdots \operatorname{pre}(e_k)$.

**The counting test.** Give each token a weight: $w(v) = 1$ for an operand and $w(\omega) = 1 - \operatorname{ar}(\omega)$ for an operator. For a token string $s = s_1 \cdots s_m$, let $P_j = \sum_{i = 1}^{j} w(s_i)$, with $P_0 = 0$.

**Theorem.** (a) A string $s$ of $m \ge 1$ tokens is in $\mathcal{P}$ if and only if $P_j \ge 1$ for each $j$ with $1 \le j \le m$, and $P_m = 1$. (b) Each $s \in \mathcal{P}$ arises from rule 2 or rule 1 in exactly one way: the operator, the number $k$ and the parts $E_1, \ldots, E_k$ are determined by $s$. So $\operatorname{post}$ is a one-to-one map from expression trees onto $\mathcal{P}$.

The number $P_j$ is the height of the evaluation stack after the first $j$ tokens: an operand pushes one value, and an operator of arity $k$ pops $k$ values and pushes one. Part (a) says that the stack never runs short and ends with one value.

*Proof of (a), only if.* By induction on the rules. For an operand, $m = 1$ and $P_1 = 1$. For $s = E_1 \cdots E_k\, \omega$, assume the claim for each $E_r$. A prefix of $s$ that ends inside $E_r$ has the sum $(r - 1) + P'$, where $P' \ge 1$ is a prefix sum of $E_r$, since each complete $E_q$ adds exactly 1. So it is at least 1. The prefix that ends with $E_k$ has the sum $k$, and the last token adds $1 - k$, which gives $P_m = 1$.

*Proof of (a), if.* By strong induction on $m$. Assume the conditions. If $m = 1$, then $w(s_1) = 1$, so $s_1$ is an operand, which is in $\mathcal{P}$. Let $m \ge 2$. Then $P_{m-1} \ge 1$ and $P_m = 1$, so $w(s_m) \le 0$, and $s_m$ is an operator $\omega$ with arity $k = P_{m-1} \ge 1$. Each token changes the prefix sum by at most $+1$. For $r = 1, \ldots, k$ let $c_r$ be the last $j \le m - 1$ with $P_j = r$, and let $c_0 = 0$. Such a $j$ exists, because the sums start at $P_0 = 0$, reach $P_{m-1} = k$, and rise by at most one per step. After $c_r$, every sum up to $m - 1$ is at least $r + 1$: a later sum below $r$ would have to pass $r$ again on its way up to $k$, after $c_r$. Hence $c_0 < c_1 < \cdots < c_k = m - 1$. Let $E_r = s_{c_{r-1} + 1} \cdots s_{c_r}$. For $c_{r-1} < j \le c_r$, its prefix sums are $P_j - (r - 1) \ge 1$ (for $r = 1$ by the hypothesis, for $r \ge 2$ by the property of $c_{r-1}$), and its total is $r - (r - 1) = 1$. Each $E_r$ is shorter than $s$, so $E_r \in \mathcal{P}$ by the induction hypothesis, and $s = E_1 \cdots E_k\, \omega \in \mathcal{P}$ by rule 2. $\square$

*Proof of (b).* A string of length one is an operand and comes only from rule 1. If $s = E_1 \cdots E_k\, \omega$ by rule 2, then $\omega$ is the last token and $k = \operatorname{ar}(\omega)$. By the computation in the only-if proof, the end of $E_r$ is a position with prefix sum $r$, and all later prefix sums before $\omega$ are at least $r + 1$. So the end of $E_r$ is the last position $c_r$ with $P_j = r$, and it depends only on $s$. So the parts are unique, and by induction the whole tree is unique. $\square$

## Examples and non-examples

| infix | postfix | prefix sums $P_1, \ldots, P_m$ | value |
|---|---|---|---|
| $(3 + 4) \times 2$ | `3 4 + 2 ×` | 1, 2, 1, 2, 1 | 14 |
| $3 + 4 \times 2$ | `3 4 2 × +` | 1, 2, 3, 2, 1 | 11 |
| $5 + (1 + 2) \times 4 - 3$ | `5 1 2 + 4 × + 3 −` | 1, 2, 3, 2, 3, 2, 1, 2, 1 | 14 |
| $(a - b) - c$ | `a b − c −` | 1, 2, 1, 2, 1 | |
| $a - (b - c)$ | `a b c − −` | 1, 2, 3, 2, 1 | |

The first two rows show that the order of the operators replaces the parentheses and the precedence rules. The last two rows show that the order of the operands of a non-commutative operator is kept, and that the two groupings of $a - b - c$ give different strings.

Non-examples:

- `3 + 4` is infix, not postfix: $P_2 = 0$ after `3 +`, so the operator lacks an operand.
- `3 4` has $P_2 = 2$: two values are left, and the string is two expressions, not one.
- `3 4 + +` has $P_4 = 0$: the second `+` has only one operand.
- `3 −` with a binary `−` has $P_2 = 0$. With a unary minus it is well-formed. A postfix language must give the two operators different symbols (for example `neg` for the unary one), because the arity of each token must be known from the token alone. Otherwise `3 4 −` could be $3 - 4$ or the two values $3$ and $-4$.

## Related definitions

- **Polish notation (prefix notation).** The operator comes first: `× + 3 4 2` for $(3 + 4) \times 2$. The same counting test works on the reversed string. Hamblin's 1962 paper treats translation to and from both forms.
- **Infix notation** needs parentheses or precedence and associativity rules. The [infix to postfix](/infix-to-postfix/) problem converts it, for example with the [shunting-yard algorithm](/shunting-yard-algorithm/). [Dijkstra's two-stack evaluation](/dijkstra-two-stack-evaluation/) evaluates a fully parenthesised infix expression without building the postfix string.
- **Postorder of a tree.** The postfix form of an [expression tree](/expression-tree/) or an [abstract syntax tree](/abstract-syntax-tree/) is its postorder with each node written as its label. Knuth calls the general form, with the degree of each node written in place of the arity of an operator, postorder with degrees, and the counting test above shows that it determines the tree.
- **Stack machine code.** The code of a stack machine, such as the bytecode of the Java virtual machine or the language Forth, is postfix: each instruction pops its operands and pushes its result.

## References
