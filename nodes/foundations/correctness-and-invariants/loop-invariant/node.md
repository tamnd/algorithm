---
tag: 7NVRNT
kind: concept
slug: loop-invariant
name: Loop invariant
aliases: [loop invariant property]
area: foundations/correctness-and-invariants
level: intro
summary: A statement about the variables of a loop that is true before each test of the loop condition. It is the main tool to prove that a loop is correct.
prereqs: [induction, invariant]
see_also: [variant-function, termination-proof, inductive-invariant, hoare-logic, partial-correctness, total-correctness]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.1, Insertion sort (loop invariants, with initialization, maintenance and termination)
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10), 1969
    locator: the rule of iteration for the while statement
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.1, Mathematical induction (the proof of Algorithm E by assertions)
---

A loop invariant is a statement about the variables of a loop that is true before each test of the loop condition. To prove that a loop is correct, you show three facts: the statement is true at the start (initialization), each pass keeps it true (maintenance), and the statement together with the exit condition gives the result (termination). It is the main tool to prove iterative algorithms such as [binary search](/binary-search/) and [insertion sort](/insertion-sort/).

## In plain words

A loop changes its variables at each pass. A loop invariant is a fact about these variables that stays true through all the changes. It is true before the first pass. Each pass keeps it true. When the loop stops, the invariant and the reason for the stop together tell you that the result is correct.

Think of a worker who sorts cards by taking one card at a time. After each card, the worker can say: "the cards I have already taken are in order". This sentence is the invariant. It is true at the start, when the worker holds no card. It stays true after each card. When no card is left, the sentence says that all the cards are in order.

## The idea

Let $I$ be a statement about the variables of a loop

$$\textbf{while } C \textbf{ do } B.$$

$I$ is a loop invariant when these hold:

1. **Initialization.** $I$ is true before the first test of $C$.
2. **Maintenance.** If $I$ and $C$ are true before a pass of the body $B$, then $I$ is true after that pass, which is before the next test of $C$.
3. **Termination.** When the loop stops, $C$ is false and $I$ is true. The conjunction $I \wedge \neg C$ must imply the postcondition that you want.

Initialization and maintenance prove, by [induction](/induction/) on the number of passes, that $I$ is true before each test of $C$. The base case is the first test, and the step is maintenance. Termination uses the last test. A `for` loop is a `while` loop with a counter, and the exit condition is that the counter has passed its last value.

These three facts prove only that the result is right when the loop stops. They give [partial correctness](/partial-correctness/). To prove that the loop does stop, find a [variant function](/variant-function/) and write a [termination proof](/termination-proof/). Both together give [total correctness](/total-correctness/).

The same idea is a rule of [Hoare logic](/hoare-logic/): from $\{I \wedge C\}\ B\ \{I\}$ you derive $\{I\}\ \textbf{while } C \textbf{ do } B\ \{I \wedge \neg C\}$.

## Examples

### Insertion sort on a concrete array

This is the code of [insertion sort](/insertion-sort/). The array has the indices 0 to $n - 1$.

```pseudo id=main
INSERTION-SORT(A)
L1  for i ← 1 to n − 1 do
L2      key ← A[i]
L3      j ← i − 1
L4      while j ≥ 0 and A[j] > key do
L5          A[j + 1] ← A[j]
L6          j ← j − 1
L7      A[j + 1] ← key
```

The invariant of the outer loop, at the test before the pass for $i$:

> $A[0 \ldots i-1]$ holds the items that were in $A[0 \ldots i-1]$ at the start, in non-decreasing order, and $A[i \ldots n-1]$ is unchanged from the start.

Take $A = [5, 2, 4, 6, 1, 3]$ with $n = 6$. The table shows the invariant at the test for each value of $i$.

| $i$ | $A[0 \ldots i-1]$ | the whole array |
|---|---|---|
| 1 | 5 | 5 2 4 6 1 3 |
| 2 | 2 5 | 2 5 4 6 1 3 |
| 3 | 2 4 5 | 2 4 5 6 1 3 |
| 4 | 2 4 5 6 | 2 4 5 6 1 3 |
| 5 | 1 2 4 5 6 | 1 2 4 5 6 3 |
| 6 | 1 2 3 4 5 6 | 1 2 3 4 5 6 |

- **Initialization.** For $i = 1$, the part $A[0 \ldots 0]$ has one item, so it is sorted, and it is the original first item. In the example it is $[5]$.
- **Maintenance.** Assume the invariant for $i$, and call the sorted prefix $s_0 \le \cdots \le s_{i-1}$. Let $key = A[i]$. By the second part of the invariant, $key$ is the original item at position $i$. The inner loop needs its own invariant, at the test of line L4:
  > $A[0 \ldots j] = s_0 \ldots s_j$, and $A[j+2 \ldots i] = s_{j+1} \ldots s_{i-1}$, and each of $s_{j+1}, \ldots, s_{i-1}$ is greater than $key$.

  At the first test, $j = i - 1$. The second part is empty, so the invariant is true. If the test is true, line L5 copies $A[j]$ to $A[j+1]$, and line L6 decreases $j$. After the pass, $A[j+1]$ holds $s_j$, and the new value of $j$ is $j - 1$. So the second part now starts with $s_j$, and $s_j > key$ by the test. The first part is shorter by one item and is unchanged. So the inner invariant is kept. The inner loop stops: $j$ drops by 1 at each pass, and the test fails at $j = -1$, so $j + 1$ is a variant. The `and` in line L4 is short-circuit, so $A[-1]$ is never read. The inner loop stops when $j = -1$ or $A[j] \le key$. In both cases, $s_0, \ldots, s_j$ are at most $key$, since the prefix is sorted, and $s_{j+1}, \ldots, s_{i-1}$ are greater than $key$. Line L7 puts $key$ at $A[j+1]$. Now $A[0 \ldots i]$ is $s_0 \ldots s_j, key, s_{j+1} \ldots s_{i-1}$, which is sorted and holds the original first $i + 1$ items. The inner loop and line L7 write only to $A[0 \ldots i]$, so $A[i+1 \ldots n-1]$ is still unchanged. This is the invariant for $i + 1$. For $i = 4$ in the example, $key = 1$, the inner loop moves 6, 5, 4 and 2 one place right, $j$ ends at $-1$, and line L7 gives $[1, 2, 4, 5, 6, 3]$.
- **Termination.** The `for` loop ends when $i = n$. The invariant for $i = n$ says that $A[0 \ldots n-1]$ holds the original items in order. That is the postcondition: the whole array is sorted and it is a permutation of the input.

### Other loops

- In the [binary search](/binary-search/) that returns as soon as $A[mid] = key$ (the version on the [variant function](/variant-function/) page), the invariant is: $0 \le lo \le hi \le n$, and if the key is in the array, it is in $A[lo \ldots hi-1]$. If the loop exits with $lo \ge hi$, the range is empty and the key is not in the array. The variant is $hi - lo$. The lower-bound version, which runs until $lo = hi$ and returns $lo$, needs a different invariant: each item before $lo$ is less than the key, and each item from $hi$ on is at least the key.
- In [merge sort](/merge-sort/), the merge loop has the invariant: the output part holds the smallest items of the two inputs, in sorted order, and each read position points to the smallest item of its input that is not yet placed.
- In the [Euclidean algorithm](/euclidean-algorithm/), with the loop `while b ≠ 0: (a, b) ← (b, a mod b)`, the invariant is $\gcd(a, b) = \gcd(a_0, b_0)$, where $a_0, b_0$ are the input. The variant is $b$. At exit, $b = 0$, so $\gcd(a, 0) = a$ is the answer.

### Statements that are not good loop invariants

A candidate can fail in three ways: at initialization, at maintenance or at termination. Each case below is for the outer loop of insertion sort.

- **Fails initialization.** "$A[0 \ldots i-1]$ holds the $i$ smallest items of the whole array." At the start it is true only if the first item is the smallest, which is false for the example (5 is not the smallest). Initialization must hold on every valid input, not only on some.
- **True, but maintenance cannot be proved.** "$A[0 \ldots i-1]$ holds the original first $i$ items, in order", without the clause about $A[i \ldots n-1]$. This statement is true at every test, because it follows from the full invariant. But from it alone, the maintenance step cannot show that $A[0 \ldots i]$ holds the original first $i + 1$ items: nothing says that $A[i]$ still holds the original item. A statement that is true but cannot carry its own maintenance step must be strengthened. The inner invariant above is also a strengthened one: its third clause, that the shifted items are greater than $key$, is what makes the exit argument work.
- **Maintained, but too weak for termination.** "$A[0 \ldots i-1]$ is sorted" holds at the start and each pass keeps it. At exit it gives a sorted array, but not that the array is a permutation of the input. The statement "true" is the extreme case: it passes initialization and maintenance, and gives nothing at exit.

A useful invariant is strong enough to give the postcondition at exit and to carry its own maintenance step, and weak enough to hold at the start. The [Hoare logic](/hoare-logic/) page shows an invariant that is too weak for the integer square root.

## Where it is used

Loop invariants are the base of [Hoare logic](/hoare-logic/) and of the proofs on this site. Tools that check programs, such as Dafny and Why3, ask the user to write them. Programmers also write them as [assertions](/assertion/), so that a test fails when the invariant is false. A statement that is kept by every operation of a data structure is a related object: see [representation invariant](/representation-invariant/) and [inductive invariant](/inductive-invariant/). The general notion is the [invariant](/invariant/).

## References
