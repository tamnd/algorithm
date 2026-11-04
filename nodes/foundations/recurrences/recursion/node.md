---
tag: 9SPG7H
kind: concept
slug: recursion
name: Recursion
aliases:
- recursive definition
- recursive procedure
area: foundations/recurrences
level: intro
summary: A definition or procedure that refers to itself on smaller inputs until it reaches base cases.
prereqs: [induction]
see_also: [recurrence-relation, divide-and-conquer-paradigm, well-founded-relation, termination-proof, structural-induction, memoization, stack, recursion-tree-method]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.3.1, The divide-and-conquer method; Chapter 4, Divide-and-Conquer
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 1, Recurrent Problems (Sections 1.1 to 1.3)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.1, Mathematical Induction; Section 2.3, Trees (recursive definitions)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.1, Basic Programming Model (recursion)
---

Recursion is a way to define a function, a set or a procedure in terms of itself on smaller inputs, with one or more base cases that need no self-reference. A recursive definition is correct when each chain of self-references reaches a base case, which is a statement about a [well-founded relation](/well-founded-relation/), and its properties are proved by [induction](/induction/) along the same order. The cost of a recursive procedure is described by a [recurrence relation](/recurrence-relation/), and most of the methods in this area of the site exist to solve those recurrences.

## In plain words

A recursive procedure solves a problem by asking itself to solve smaller copies of the same problem. It then builds the answer for the big problem from the answers for the small copies. A problem that is small enough has a direct answer, and the procedure stops there. This small case is the base case.

Two things must be true. First, each self-call must get a strictly smaller problem, by some measure that cannot go down forever. Second, each small enough problem must be a base case. When both are true, the procedure always stops. To trust the answer, you assume that the self-calls return correct answers and check that the step that combines them is correct. This is a proof by induction in disguise.

## The idea

### Recursive definitions

A recursive definition of a function $f$ on a set $D$ has two parts.

- **Base cases.** For each $x$ in a set $B \subseteq D$, the value $f(x)$ is given directly.
- **Recursive case.** For each $x \in D \setminus B$, the value $f(x) = \Phi(x, f(y_1), \ldots, f(y_k))$ for some elements $y_1, \ldots, y_k$ of $D$ that are determined by $x$, and a known function $\Phi$.

Let $y \prec x$ mean that $y$ is one of the $y_i$ in the rule for $x$. The definition gives exactly one function $f$ when $\prec$ is [well-founded](/well-founded-relation/), that is, when there is no infinite chain $x_0 \succ x_1 \succ x_2 \succ \cdots$. The proof is by well-founded induction: if two functions $f$ and $g$ both satisfy the definition and differ somewhere, take an $x$ that is minimal among the points where they differ. Then $f(y_i) = g(y_i)$ for each $y_i \prec x$, so the rule gives $f(x) = g(x)$, a contradiction. Existence is proved by the same induction. The usual way to show that $\prec$ is well-founded is a measure $\mu : D \to \mathbb{N}$ with $\mu(y) < \mu(x)$ whenever $y \prec x$, such as the length of an array or the value of an integer argument. This is a [variant function](/variant-function/).

The factorial is the standard example: $0! = 1$ and $n! = n \cdot (n-1)!$ for $n \ge 1$. The measure is $n$ itself. A recursive definition of a set works in the same way: a binary tree is either empty, or a root with a left and a right binary tree. Proofs about such sets use [structural induction](/structural-induction/).

### Recursive procedures

A recursive procedure is a program that calls itself. Each call has its own copy of the parameters and the local variables, kept in an activation record on the call [stack](/stack/). The call returns to the point after the self-call, with its local state intact. So the extra space of a recursive procedure is at least proportional to the largest depth of the calls, times the size of one record.

Three facts make a recursive procedure correct.

1. **Termination.** A measure of the arguments drops by at least a fixed amount, or to a strictly smaller natural number, at each self-call, and the base case covers each argument whose measure is below a threshold. See [termination proof](/termination-proof/).
2. **Base cases.** The procedure is correct on each base case.
3. **Recursive step.** If each self-call returns the correct result for its smaller argument (the induction hypothesis), then the procedure returns the correct result for the current argument.

These are the three parts of a proof by strong induction on the measure. The proof of [merge sort](/merge-sort/) on its own page is a full example: the measure is the length $hi - lo$ of the range, the base case is a range of length at most 1, and the step uses the correctness of the merge.

### Cost of a recursive procedure

Let $T(n)$ be the cost of a call on an input of size $n$. The cost of a call is the cost of its own work plus the cost of its self-calls, so $T$ satisfies a [recurrence relation](/recurrence-relation/). For example, MERGE-SORT gives $T(n) = T(\lceil n/2 \rceil) + T(\lfloor n/2 \rfloor) + \Theta(n)$. The calls form a tree, the recursion tree, with one node for each call. The [recursion-tree method](/recursion-tree-method/) adds the work of the nodes level by level. The total work is the sum over all nodes, the time is that sum on one processor, and the stack space is the height of the tree times the size of a record.

### Recursion and iteration

Each recursive procedure can be turned into a loop with an explicit stack that holds the pending calls. A procedure whose only self-call is its last action (tail recursion) needs no stack at all: the call can reuse the current record, and it becomes a loop. The [Euclidean algorithm](/euclidean-algorithm/) $\gcd(a, b) = \gcd(b, a \bmod b)$ is tail recursive. Factorial in the form $n \cdot (n-1)!$ is not, because the multiplication happens after the self-call returns.

## Examples

- **Factorial.** FACT$(n)$ returns 1 if $n = 0$, and $n \cdot$ FACT$(n - 1)$ otherwise. It makes $n + 1$ calls and the stack depth is $n + 1$. The cost is $T(n) = T(n - 1) + \Theta(1)$, so $T(n) = \Theta(n)$.
- **Fibonacci, the slow way.** FIB$(n)$ returns $n$ if $n \le 1$, and FIB$(n-1) +$ FIB$(n-2)$ otherwise. The number of calls $C(n)$ satisfies $C(0) = C(1) = 1$ and $C(n) = 1 + C(n-1) + C(n-2)$. By induction, $C(n) = 2F_{n+1} - 1$, where $F_k$ is the $k$-th [Fibonacci number](/fibonacci-numbers/): the base cases hold because $F_1 = F_2 = 1$, and $1 + (2F_n - 1) + (2F_{n-1} - 1) = 2F_{n+1} - 1$. For $n = 30$ the procedure makes $2F_{31} - 1 = 2{,}692{,}537$ calls to compute $F_{30} = 832{,}040$. The calls grow like $\varphi^n$ with $\varphi \approx 1.618$, because the same subproblems are solved many times. [Memoization](/memoization/) stores each value once and brings the cost down to $\Theta(n)$ additions.
- **Binary search.** [Binary search](/binary-search/) compares the key with the middle item and calls itself on one half. Its cost is $T(n) = T(\lfloor n/2 \rfloor) + \Theta(1)$, so $T(n) = \Theta(\log n)$. It is tail recursive, so it is usually written as a loop.
- **Tower of Hanoi.** To move $n$ disks, move $n-1$ disks to the spare peg, move the largest disk, then move the $n-1$ disks on top of it. The number of moves satisfies $M(0) = 0$ and $M(n) = 2M(n-1) + 1$, so $M(n) = 2^n - 1$. For 64 disks this is $18{,}446{,}744{,}073{,}709{,}551{,}615$ moves. See [Tower of Hanoi](/tower-of-hanoi/).
- **Ackermann's function.** $A(0, n) = n + 1$, $A(m, 0) = A(m - 1, 1)$, and $A(m, n) = A(m - 1, A(m, n - 1))$. The pair $(m, n)$ drops in the lexicographic order at each call: either $m$ drops, or $m$ stays and $n$ drops. This order on $\mathbb{N} \times \mathbb{N}$ is well-founded, so each call terminates, although the second argument of the outer call can be very large. The [Ackermann function](/ackermann-function/) grows faster than each [primitive recursive function](/primitive-recursive-function/), so its number of calls has no primitive recursive bound. Small values are $A(2, 3) = 9$ and $A(3, 3) = 61$.
- **McCarthy's 91 function.** $M(n) = n - 10$ if $n > 100$, and $M(n) = M(M(n + 11))$ otherwise. Here the argument grows at some calls, so the plain size is not a measure. Still, $M(n) = 91$ for each integer $n \le 100$, and $M(n) = n - 10$ for $n > 100$. A termination proof is an induction on $101 - n$ that also uses the value of the inner call, not only its argument.
- **Non-example: a missing base case.** The definition $f(n) = f(n - 1) + 1$ for each integer $n$ defines no unique function on $\mathbb{Z}$: each $f(n) = n + c$ satisfies it. The relation "$n - 1 \prec n$" on $\mathbb{Z}$ has the infinite chain $0 \succ -1 \succ -2 \succ \cdots$, so it is not well-founded.
- **Non-example: an unknown measure.** The procedure that maps $n$ to $n/2$ when $n$ is even, and to $3n + 1$ when $n$ is odd, and stops at 1, has no known termination proof. Whether it stops for each positive integer is the open Collatz problem. A recursive definition is only as good as its proof of termination.

## Where it is used

- **Divide and conquer.** The [divide-and-conquer paradigm](/divide-and-conquer-paradigm/) is recursion where each call splits its input into parts of a fixed fraction of the size. Merge sort, quicksort, [Karatsuba multiplication](/karatsuba-multiplication/) and the [Strassen algorithm](/strassen-algorithm/) are of this kind, and their costs are [divide-and-conquer recurrences](/divide-and-conquer-recurrence/).
- **Recursive data structures.** Lists, trees and expressions are defined recursively, and the natural programs on them follow the definition: one case for each constructor. [Recursive descent parsing](/recursive-descent-parsing/) follows the grammar in the same way.
- **Dynamic programming.** A dynamic program starts from a recursive definition of the optimal value and stores the values of the subproblems, either top-down with memoization or bottom-up in a table.
- **Search and enumeration.** Backtracking and the generation of subsets, permutations and combinations explore a tree of choices recursively.
- **Theory of computation.** The [primitive recursive functions](/primitive-recursive-function/) and the [partial recursive functions](/partial-recursive-function/) define computability by recursion, and the [Kleene recursion theorem](/kleene-recursion-theorem/) shows that programs can refer to their own text.
- **Analysis of algorithms.** The cost of each recursive algorithm is a [recurrence relation](/recurrence-relation/). The [substitution method](/substitution-method/), the [recursion-tree method](/recursion-tree-method/) and the [master theorem](/master-theorem/) solve these recurrences.

### Pitfalls

- **Stack depth.** A recursion of depth $n$ uses $\Theta(n)$ stack space. A recursive quicksort that recurses on the larger part first can reach depth $n$; recursing on the smaller part and looping on the larger one keeps the depth at most $\lg n$. See [quicksort stack depth](/quicksort-stack-depth/).
- **Repeated subproblems.** Two self-calls that share subproblems can make the cost exponential, as in the slow Fibonacci above.
- **A base case that is not reached.** A self-call on $\lfloor n/2 \rfloor$ with only the base case $n = 1$ loops forever on $n = 0$. Test each base case against each argument the recursive case can produce.

## References
