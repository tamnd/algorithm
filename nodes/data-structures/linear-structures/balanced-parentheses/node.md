---
tag: 1YYTP9
kind: problem
slug: balanced-parentheses
name: Balanced parentheses
aliases:
- bracket matching
- well-formed brackets
area: data-structures/linear-structures
level: intro
summary: Decide whether every opening bracket is matched by a correctly nested closing bracket.
prereqs: [stack, dyck-word]
see_also: [parenthesis-matching, dyck-word, catalan-numbers, pushdown-automaton, context-free-grammar, dijkstra-two-stack-evaluation, infix-to-postfix, expression-tree]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3, exercise 1.3.4 (a stack client Parentheses that checks whether the brackets of a text are properly balanced)
  - paper: "Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage Learning (2013)"
    locator: Section 2.1, Example 2.3, the grammar S -> aSb | SS | empty for properly nested parentheses; Section 2.2 on pushdown automata
  - paper: "Frederic Magniez, Claire Mathieu and Ashwin Nayak, Recognizing well-parenthesized expressions in the streaming model, Proceedings of the 42nd ACM Symposium on Theory of Computing (STOC 2010); journal version SIAM Journal on Computing 43(6) (2014)"
    locator: the one-pass algorithm with O(sqrt(n log n)) space for two or more bracket types, and the matching lower bound for one pass
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.1, the stack operations used by the standard algorithm
---

The balanced parentheses problem asks whether a string of brackets is properly nested: each opening bracket has a closing bracket of the same type after it, and two matched pairs are either disjoint or one lies inside the other. With one type of bracket, a counter of the open brackets decides it in one pass; the string is balanced exactly when the counter never goes below zero and ends at zero. With two or more types, the counter is not enough, and the standard solution pushes each opening bracket on a [stack](/stack/) and pops it at the matching closing bracket, in $\Theta(n)$ time and $O(n)$ space. The balanced strings over one pair are the [Dyck words](/dyck-word/), and the problem is the basic example of a language that a [pushdown automaton](/pushdown-automaton/) recognizes but no finite automaton does.

## In plain words

You have a line of text with brackets in it, like `{[()()]}`, and you want to know if they close correctly. Every bracket that opens must be closed later by the same kind of bracket, and the one that opened last must close first. So `([])` is fine, but `([)]` is not: the round bracket closes while the square one inside it is still open.

You can check this with a pile. Read from left to right. When a bracket opens, put it on the pile. When a bracket closes, the top of the pile must be the same kind; take it off. At the end, the pile must be empty. With only one kind of bracket, you do not need the pile: a count of the open brackets is enough.

## Definition

**Input.** A string $s = s_1 s_2 \cdots s_n$ over an alphabet with $k \ge 1$ pairs of brackets $(o_1, c_1), \ldots, (o_k, c_k)$, such as `()`, `[]` and `{}`. In the general version, other characters may occur and are ignored.

**Balanced strings.** The set $D_k$ of balanced strings is the language of the [context-free grammar](/context-free-grammar/)

$$S \to \varepsilon \mid S\,S \mid o_1\,S\,c_1 \mid \cdots \mid o_k\,S\,c_k.$$

Equivalently, $s$ is balanced when it can be reduced to the empty string by deleting, again and again, an adjacent pair $o_j c_j$.

**For one type** ($k = 1$), let $d_i$ be the number of opening brackets minus the number of closing brackets among $s_1, \ldots, s_i$, the *depth* after $i$ symbols. Then $s$ is balanced if and only if $d_i \ge 0$ for all $i$ and $d_n = 0$.

**The question.** Decide whether $s \in D_k$. Many uses also ask for the position of the first error, or for the partner of each bracket.

## Variants

- **One type of bracket.** The depth test above, with one counter.
- **Several types.** The stack algorithm below. The depth test is necessary but not sufficient: `([)]` passes it and is not balanced.
- **[Parenthesis matching](/parenthesis-matching/).** For each bracket, output the position of its partner. The stack algorithm does this if it pushes positions instead of symbols.
- **Fewest insertions to balance.** For one type, the answer is the number of closing brackets that find the counter at zero plus the final counter. For several types, fewest insertions or edits is a harder problem, solved by dynamic programming in polynomial time.
- **Longest balanced substring.** One pass with a stack of positions of unmatched brackets.
- **Counting.** The number of balanced strings of length $2m$ with one type is the [Catalan number](/catalan-numbers/) $C_m = \binom{2m}{m}/(m + 1)$; with $k$ types it is $k^m C_m$.
- **Text with quotes and comments.** Brackets inside string literals and comments must be skipped, which needs a small state machine in front of the stack.
- **Streaming.** The input passes once and the memory is small; see Bounds.

## Examples

**The stack on `{[()()]}`.** The stack is written from the bottom to the top.

| step | symbol | action | stack after it |
|---|---|---|---|
| 1 | `{` | push | `{` |
| 2 | `[` | push | `{[` |
| 3 | `(` | push | `{[(` |
| 4 | `)` | top is `(`, pop | `{[` |
| 5 | `(` | push | `{[(` |
| 6 | `)` | top is `(`, pop | `{[` |
| 7 | `]` | top is `[`, pop | `{` |
| 8 | `}` | top is `{`, pop | empty |

The stack is empty at the end, so the string is balanced.

**Three ways to fail.**

- `([)]`: at step 3 the symbol is `)` and the top is `[`. Wrong type.
- `())(`: at step 3 the symbol is `)` and the stack is empty. A closing bracket with no partner.
- `(()`: the input ends with `(` on the stack. An opening bracket with no partner.

**Depths for one type.** For `(()())` the depths are $1, 2, 1, 2, 1, 0$: never negative and zero at the end, so it is balanced. For `())(()` they are $1, 0, -1, \ldots$, and the string fails at position 3. To balance `())(` takes two insertions: one `(` for the closing bracket at position 3 and one `)` for the final depth 1.

**All balanced strings of length 6 with one type.** There are $C_3 = 5$: `((()))`, `(()())`, `(())()`, `()(())` and `()()()`. With two types, there are $2^3 \cdot 5 = 40$.

## Known algorithms

- **Depth counter**, for one type. Read $s$ once, add 1 for `(` and subtract 1 for `)`. Reject if the counter goes negative, and accept if it ends at 0. It costs $\Theta(n)$ time and one counter of $O(\log n)$ bits.
- **Stack algorithm**, for any $k$. For each symbol: if it is an opening bracket, push it; if it is a closing bracket $c_j$, reject when the stack is empty or its top is not $o_j$, and pop otherwise. At the end, accept if and only if the stack is empty. Each symbol causes at most one push and one pop, so it costs $\Theta(n)$ time and $O(d)$ space, where $d \le n$ is the largest depth. *Correctness:* by induction on the length of the input, the stack holds exactly the unmatched opening brackets of the prefix read so far, in order, and the prefix can be extended to a balanced string if and only if no rejection has happened; the reduction by adjacent pairs in the definition does the same deletions in the same order.
- **Repeated deletion.** Delete adjacent pairs $o_j c_j$ until none is left. It is correct by the definition, but a direct implementation costs $\Theta(n^2)$ time; the stack algorithm is this method done in the right order.
- **Parallel prefix sums**, for one type. Compute all depths $d_i$ with a parallel prefix sum and their minimum with a parallel reduction, in $O(\log n)$ depth and $O(n)$ work.
- **Magniez, Mathieu and Nayak (2010)**, for $k \ge 2$ in the streaming model. A randomized one-pass algorithm with $O(\sqrt{n \log n})$ space, which errs with small probability.

## Bounds

**Time.** Every algorithm must read every symbol, since changing any one symbol of a balanced string makes it unbalanced. So $\Omega(n)$ time is needed, and both the counter and the stack algorithm are optimal.

**Space with one pass.** For one type, $O(\log n)$ bits are enough. For $k \ge 2$, a deterministic one-pass algorithm needs $\Omega(n)$ bits: after reading $o_{j_1} o_{j_2} \cdots o_{j_m}$ with $m = n/2$, it must remember the whole sequence of types, because the only closing string that balances it is $c_{j_m} \cdots c_{j_1}$. So two different prefixes of opening brackets must lead to different memory states, and there are $k^{m}$ of them. Randomized one-pass algorithms need $\Theta(\sqrt{n})$ space up to log factors, by the algorithm and the lower bound of Magniez, Mathieu and Nayak.

**Not regular.** For one type, the language is not recognized by any finite automaton: the strings $(^i$ for different $i$ need different states, since only $)^i$ completes $(^i$. This is the standard use of the pumping lemma. A deterministic [pushdown automaton](/pushdown-automaton/) recognizes $D_k$ for every $k$, with the stack algorithm as its run.

## Reductions

- **Dyck language.** $D_1$ is the set of [Dyck words](/dyck-word/). Its words of length $2m$ are in bijection with lattice paths that do not go below the axis, binary trees with $m$ internal nodes and plane trees with $m + 1$ nodes, which is why they are counted by the Catalan numbers.
- **Chomsky and Schützenberger.** Every context-free language is the image under a homomorphism of the intersection of some $D_k$ with a regular language. So $D_k$ is the core of all context-free languages.
- **Expression parsing.** The balance check is the part of [infix-to-postfix conversion](/infix-to-postfix/) and of [Dijkstra's two-stack evaluation](/dijkstra-two-stack-evaluation/) that handles the parentheses. A balanced string of one type is also the shape of an [expression tree](/expression-tree/) read in order.
- **Succinct trees.** A depth-first walk of an ordered tree that writes `(` on entering a node and `)` on leaving it gives a balanced string of $2n$ bits. With rank and select support on it, tree navigation takes constant time in $2n + o(n)$ bits.

## Applications

- **Compilers and editors** check the brackets of source code, and editors highlight the partner of the bracket under the cursor.
- **Markup languages.** An XML document is well formed only if its tags are balanced, with each tag name as a bracket type.
- **Expression evaluation.** Calculators and parsers check the parentheses of an arithmetic expression before or while they evaluate it.
- **Succinct data structures** store trees as balanced strings of bits, as in the reductions above.

## References
