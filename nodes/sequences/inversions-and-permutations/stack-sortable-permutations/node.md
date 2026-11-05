---
tag: WGKX10
kind: concept
slug: stack-sortable-permutations
name: Stack-sortable permutations
aliases:
- 231-avoiding permutations
- Knuth stack sorting
area: sequences/inversions-and-permutations
level: advanced
summary: Permutations sortable by a single stack; these are exactly the 231-avoiding permutations, counted by Catalan numbers.
prereqs: [stack-permutation-generability, permutation-pattern-avoidance]
see_also: [catalan-numbers, stack, permutation-inverse, cartesian-tree, presortedness, balanced-parentheses, permutation-pattern-matching, adaptive-sorting]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.1 (stacks, and the exercises on the permutations that a stack can produce and sort)
  - paper: "Julian West, Permutations with forbidden subsequences and stack-sortable permutations, PhD thesis, Massachusetts Institute of Technology, 1990"
    locator: the stack sorting map, two-stack-sortable permutations and their forbidden patterns
  - paper: "Doron Zeilberger, A proof of Julian West's conjecture that the number of two-stack-sortable permutations of length n is 2(3n)!/((n+1)!(2n+1)!), Discrete Mathematics 102(1) (1992) 85-93"
    locator: the enumeration of two-stack-sortable permutations
---

A permutation is stack-sortable if a single [stack](/stack/) can turn it into $1, 2, \ldots, n$: read it from left to right, push items, and pop them to the output at any time. Knuth showed that these are exactly the permutations that avoid the pattern $231$, with no $i < j < k$ and $p_k < p_i < p_j$, and that there are $C_n$ of them, the [Catalan numbers](/catalan-numbers/). A greedy rule, pop while the top is smaller than the next item, sorts every stack-sortable permutation, and applied to any permutation it defines West's stack sorting map $s$, whose iterates sort everything after at most $n - 1$ passes. The stack-sortable permutations are the [inverses](/permutation-inverse/) of the outputs a stack can produce from sorted input, the subject of [stack permutation generability](/stack-permutation-generability/).

## In plain words

Numbers arrive one by one and must leave in increasing order. You have one pile in which you can set numbers aside, but you can only take back the number on top. A good rule is: before putting a new number on the pile, send away every number on top that is smaller than it, since nothing smaller is still to come for them to wait for. At the end, empty the pile.

This rule works whenever any method works, and it fails in one kind of situation: a middle number arrives, then a larger one, then a smaller one. The middle number has to leave before the larger one is put on top of it, or it gets buried, but it cannot leave before the small one that comes last. Inputs without this shape are exactly the ones a single pile can sort.

## The idea

**Greedy stack sorting.**

```pseudo
STACK-SORT(p[1 .. n])                     ▷ returns s(p)
1  S ← empty stack, out ← empty list
2  for j ← 1 to n do
3      while S is not empty and top(S) < p[j] do append pop(S) to out
4      push p[j] on S
5  while S is not empty do append pop(S) to out
6  return out
```

Every item is pushed and popped once, so it runs in $\Theta(n)$ time. The output $s(p)$ is West's *stack sorting map*. The stack always decreases from bottom to top.

**Theorem (Knuth).** The following are equivalent for a permutation $p$:

1. some sequence of pushes and pops sorts $p$ with one stack;
2. STACK-SORT returns $1 2 \cdots n$;
3. $p$ avoids $231$.

*Sketch.* If $p_i\,p_j\,p_k$ is a $231$, with $p_k < p_i < p_j$, then when $p_j$ arrives, $p_i$ is either already in the output, which is wrong since $p_k < p_i$ is still to come, or in the stack, where $p_j$ will bury it, so $p_j$ leaves first, also wrong. So no stack sorts $p$. Conversely, if STACK-SORT outputs some $x$ before a smaller $y$, then $x$ was popped by a larger arrival $z$ when $y$ had not arrived yet, and $x\,z\,y$ is a $231$.

**The tree view.** Build the decreasing binary tree of $p$: the root is the largest item, the left subtree is built from the items to its left, and the right subtree from the items to its right. This is the [Cartesian tree](/cartesian-tree/) for the maximum. Reading the tree in order gives $p$, and $s(p)$ is the postorder. So $s(p)$ is sorted exactly when the postorder is increasing, that is, when at every node the items of the left subtree are smaller than those of the right subtree. A violation at a node $v$, with $x$ on the left larger than $y$ on the right, gives the $231$ formed by $x$, $v$ and $y$.

**Counting.** A $231$-avoiding permutation with $n$ at position $k$ has every item before $n$ smaller than every item after it, and both sides avoid $231$. So the number $a_n$ satisfies $a_n = \sum_{k=1}^{n} a_{k-1} a_{n-k}$ with $a_0 = 1$, the recurrence of the Catalan numbers, and $a_n = C_n = \frac{1}{n+1}\binom{2n}{n}$.

**Several passes.** A permutation is $t$-stack-sortable if $s^t(p)$ is sorted. Every permutation of $[n]$ is $(n-1)$-stack-sortable: in one pass the largest item among those not yet in the sorted tail is popped only when the stack is emptied or when a tail item arrives, so it lands just before the tail, and after $t$ passes the last $t$ positions hold $n - t + 1, \ldots, n$. For $n \ge 2$ exactly $(n-2)!$ permutations need all $n - 1$ passes, among them $2\,3 \cdots n\,1$. West characterized the 2-stack-sortable permutations by the pattern $2341$ and a barred pattern, and Zeilberger proved West's conjecture that there are $\frac{2(3n)!}{(n+1)!\,(2n+1)!}$ of them.

## Examples

**A sortable input.** $p = 4\,1\,3\,2$ avoids $231$. STACK-SORT pushes 4 and then 1, pops 1 when 3 arrives, pushes 3 and 2, and empties the stack: $1, 2, 3, 4$.

**A non-sortable input.** $p = 3\,1\,4\,5\,2$ contains $231$, for example $3\,4\,2$. One pass gives $s(p) = 1\,3\,4\,2\,5$, which still contains $342$. Two passes give $1\,3\,2\,4\,5$ and three give the identity, so $p$ is 3-stack-sortable but not 2-stack-sortable.

**The smallest obstruction.** $s(2\,3\,1) = 2\,1\,3$. When 3 arrives, 2 must leave to avoid being buried, but 1 has not arrived yet.

**Counts.** For $n = 1, \ldots, 7$ there are $1, 2, 5, 14, 42, 132, 429$ stack-sortable permutations and $1, 2, 6, 22, 91, 408, 1938$ two-stack-sortable ones. The largest number of passes needed for $n = 1, \ldots, 7$ is $0, 1, 2, 3, 4, 5, 6$, reached by $1, 1, 1, 2, 6, 24, 120$ permutations.

**Inverse relation.** $3\,1\,2$ cannot be produced by a stack from $1\,2\,3$, and its inverse $2\,3\,1$ cannot be sorted by a stack. In general $p$ is stack-sortable exactly when $p^{-1}$ is producible, since the same push and pop word does both jobs.

## Where it is used

- **Pattern avoidance.** Stack sorting is the historical origin of the theory of [permutation patterns](/permutation-pattern-avoidance/): Knuth's characterization by $231$ was the first result of the kind, and every pattern of length 3 is avoided by $C_n$ permutations.
- **Catalan bijections.** The push and pop word of a sortable permutation is a [balanced parentheses](/balanced-parentheses/) word, which links $231$-avoiding permutations with binary trees, triangulations and the other Catalan families.
- **Sorting networks of stacks.** Sorting with several stacks in series or in parallel, with queues, and with deques generalizes the question, and the stack sorting map is the standard model for stacks in series.
- **Measures of disorder.** The number of passes needed, or whether one pass suffices, is a coarse measure of [presortedness](/presortedness/). One pass of STACK-SORT is linear, so testing $231$-avoidance costs $\Theta(n)$.
- **Data structures.** The same greedy rule, popping while the top is smaller, is the monotonic-stack pattern used for "next greater element" and for building [Cartesian trees](/cartesian-tree/) in linear time.

## References
