---
tag: JDPM64
kind: technique
slug: termination-proof
name: Termination proof
aliases:
- Proof of termination
- Termination argument
area: foundations/correctness-and-invariants
level: intro
summary: Showing a loop or recursion ends, usually by exhibiting a variant function that strictly decreases.
prereqs: [variant-function, well-founded-relation, loop-invariant]
see_also: [induction, total-correctness, partial-correctness, ackermann-function, structural-induction, multiset-ordering, lexicographic-order, halting-problem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.1 (the termination step of a loop invariant proof)
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10), 1969
    locator: the discussion of termination, which the rules of the paper do not prove
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.1, Algorithm E and its finiteness
  - paper: "Robert W. Floyd, Assigning meanings to programs, Proceedings of Symposia in Applied Mathematics 19 (1967)"
    locator: pages 19 to 32, the final section (termination by a map into a well-ordered set)
  - paper: "Nachum Dershowitz and Zohar Manna, Proving termination with multiset orderings, Communications of the ACM 22(8) (1979), doi:10.1145/359138.359142"
    locator: pages 465 to 476
---

A termination proof shows that a loop or a recursive function stops on every valid input. The usual method is to assign to each state a value in a well-founded set, and to show that each step makes this value strictly smaller. Because a well-founded set has no infinite descending chain, the execution is finite. A proof of correctness that has no termination proof shows only [partial correctness](/partial-correctness/), and with the termination proof it shows [total correctness](/total-correctness/).

## In plain words

A program that never stops is wrong, even if every answer that it gives is right. To show that a program stops, you find a measure of how much work is left. At each step the measure must go down. And it must not be able to go down forever.

The simplest measure is a whole number that is zero or more. A whole number cannot drop for ever, so the program must stop. Sometimes one number is not enough. A step may reduce one number but raise another. Then you use a pair of numbers, compared like words in a dictionary: the first number counts most, and the second number counts only when the first is equal. A pair of whole numbers compared this way also cannot drop for ever, even if the second number can jump up at the moment when the first one drops.

## When it applies

- A loop whose exit depends on a counter, a range or a size: for example `while lo < hi`.
- A recursive function. Each call must be on a smaller argument, by some measure.
- A rewrite system, a game or a protocol where each move changes a state.
- Any proof of [total correctness](/total-correctness/).

It does not apply when the loop is meant to run forever, such as the main loop of a server. For such a system, you prove properties of its states with an [invariant](/invariant/).

## The template

A *well-founded order* is a pair $(W, \prec)$, with $\prec$ a strict partial order on $W$, such that each non-empty subset of $W$ has a minimal element. See [well-founded relation](/well-founded-relation/).

**Principle.** Let a program have a set of states, and let each step go from a state $s$ to a state $s'$. Let $I$ be an inductive [invariant](/invariant/): $I(s)$ and $s \to s'$ imply $I(s')$. Let $(W, \prec)$ be a well-founded order and $v$ a function from the states that satisfy $I$ to $W$, such that $I(s)$ and $s \to s'$ imply $v(s') \prec v(s)$. Then no execution that starts in a state with $I$ has infinite length. Here a step of a loop is one whole pass, so the principle also needs each pass to stop. A body with an inner loop needs its own termination proof first.

*Proof.* Suppose that $s_0 \to s_1 \to s_2 \to \cdots$ is an infinite execution with $I(s_0)$. Since $I$ is inductive, $I(s_k)$ holds for each $k$, by induction on $k$. Let $X = \{ v(s_k) : k \ge 0 \}$. It is not empty, so it has a minimal element $v(s_j)$. But $v(s_{j+1}) \prec v(s_j)$ and $v(s_{j+1}) \in X$. This contradicts the minimality. $\blacksquare$

Use these steps.

1. **Name the step.** For a loop, one pass of the body. For a recursion, one call from a function to a callee.
2. **State the invariant or the precondition** that you need. A measure often makes sense only when some conditions hold, for example $b \ge 0$.
3. **Choose the measure** $v$ and the order $(W, \prec)$. Try, in this order: one natural number, such as a size, a length or a distance to the end; then a tuple of natural numbers in lexicographic order; then a multiset or a more general order.
4. **Prove that $v$ is in $W$** at each state that is needed. For $W = \mathbb{N}$ this means $v \ge 0$.
5. **Prove the strict decrease** at each step, in each case of the body, including the branches that look harmless.
6. **Conclude** with the principle above. If $W = \mathbb{N}$ and $v$ drops by at least 1, add the bound on the number of steps from the [variant function](/variant-function/) page.

**[Lexicographic order](/lexicographic-order/).** On $\mathbb{N} \times \mathbb{N}$, define $(a, b) \prec (c, d)$ when $a < c$, or when $a = c$ and $b < d$. This order is well-founded. *Proof.* Let $X \subseteq \mathbb{N} \times \mathbb{N}$ be non-empty. Let $a_0$ be the least first component of an element of $X$ (it exists, by the [well-ordering principle](/well-ordering-principle/)). Let $b_0$ be the least $b$ such that $(a_0, b) \in X$. Then $(a_0, b_0)$ is minimal in $X$: if $(c, d) \prec (a_0, b_0)$, then either $c < a_0$, and $(c, d) \notin X$ by the choice of $a_0$, or $c = a_0$ and $d < b_0$, and $(c, d) \notin X$ by the choice of $b_0$. $\blacksquare$ The same argument, applied to the first coordinate and then to the rest, shows that tuples of any fixed length are well-founded in this order. Note that no bound exists on how large the second component can become when the first one drops. This is the strength of the order.

## Classic examples

### Euclid's algorithm and binary search

For both, the measure is one natural number: $b$ for Euclid's algorithm, and $hi - lo$ for binary search. The checks are on the [variant function](/variant-function/) page.

### The Ackermann function

The two-argument [Ackermann function](/ackermann-function/) is defined for $m, n \in \mathbb{N}$ by

$$A(0, n) = n + 1, \qquad A(m+1, 0) = A(m, 1), \qquad A(m+1, n+1) = A(m, A(m+1, n)).$$

**Claim.** The recursion terminates for each pair $(m, n)$.

**Proof.** Use the measure $v(m, n) = (m, n)$ of the call, in the lexicographic order on $\mathbb{N} \times \mathbb{N}$. Each call of the third rule makes two calls, and the second call uses the value of the first as its argument. In each case the new call is smaller:

- $A(m+1, 0)$ calls $A(m, 1)$. Here $(m, 1) \prec (m+1, 0)$ since $m < m+1$.
- $A(m+1, n+1)$ calls $A(m+1, n)$ first. Here $(m+1, n) \prec (m+1, n+1)$ since the first components are equal and $n < n+1$.
- $A(m+1, n+1)$ then calls $A(m, k)$, where $k$ is the value returned by the first call. Here $(m, k) \prec (m+1, n+1)$ for each natural number $k$, since $m < m+1$.

The last case is the reason for the lexicographic order. The value $k$ can be huge, and no single natural-number measure of $(m, n)$ bounds it. Now prove, by well-founded induction on $(m, n)$, that the call terminates. Assume that each call on a pair that is smaller than $(m, n)$ terminates. If $m = 0$, the call returns at once. If $m > 0$ and $n = 0$, the call needs $A(m-1, 1)$, which terminates since $(m-1, 1) \prec (m, 0)$. If $m > 0$ and $n > 0$, the call first runs $A(m, n-1)$, which terminates with some value $k$ since $(m, n-1) \prec (m, n)$. Then it runs $A(m-1, k)$, which terminates since $(m-1, k) \prec (m, n)$. So the call on $(m, n)$ terminates. $\blacksquare$

The computation can still be long. $A(2, 3) = 9$ takes 44 calls, and $A(3, 3) = 61$ takes 2432 calls. For small $m$ there are closed forms: $A(1, n) = n + 2$, $A(2, n) = 2n + 3$ and $A(3, n) = 2^{n+3} - 3$. These are proved by induction on $n$.

### A loop that needs a pair

```pseudo id=pair
RESET-LOOP(x, y)                  ▷ x, y natural numbers
L1  while x > 0 or y > 0 do
L2      if y > 0 then y ← y − 1
L3      else x ← x − 1, y ← READ()   ▷ READ returns any natural number
```

Each pass either lowers $y$ by 1, or lowers $x$ by 1 and sets $y$ to a value that nobody knows in advance. The number of passes cannot be bounded by a function of the initial $(x, y)$: with $x = 3$ and $y = 0$, the loop takes 18 passes if `READ` always returns 5, and many more if it returns larger numbers. The loop does stop: take $v = (x, y)$ in the lexicographic order. In line L2 the pair goes from $(x, y)$ to $(x, y-1)$. In line L3 it goes from $(x, 0)$ to $(x-1, y')$ and $x - 1 < x$. Both are strict decreases in the lexicographic order.

### Recursion on a size

[Merge sort](/merge-sort/) calls itself on ranges of length $\lfloor k/2 \rfloor$ and $\lceil k/2 \rceil$ where $k = hi - lo \ge 2$. For $k \ge 2$ both are at least 1 and at most $k - 1$. So the length decreases at each call, and the length 1 or 0 is a base case.

### A loop with no known measure

```pseudo id=collatz
COLLATZ(n)                        ▷ n a positive integer
L1  while n ≠ 1 do
L2      if n is even then n ← n / 2
L3      else n ← 3n + 1
```

For $n = 27$ the loop stops after 111 passes. Nobody has proved that it stops for every $n$. This is the Collatz problem. No measure that works for all inputs is known, and the value of $n$ is not one: it grows at odd steps.

### A multiset measure

Take a bag of balls, each labelled with a natural number. A move takes out one ball with label $k \ge 1$ and puts in any finite number of balls with labels less than $k$. A ball with label 0 can only be taken out. Does every sequence of moves stop? The number of balls can grow, and so can the sum of the labels, so neither is a measure. The bag itself is: one move replaces an element of the multiset by finitely many smaller elements, and the [multiset ordering](/multiset-ordering/) over a well-founded order is well-founded (Dershowitz and Manna, 1979). For a bag with labels at most $m$, the tuple $(c_m, c_{m-1}, \ldots, c_0)$ of counts of each label also works, in the lexicographic order on $\mathbb{N}^{m+1}$: a move lowers $c_k$ by 1 and changes only counts of smaller labels. From the bag $\{2\}$, a player who always puts in two balls of the next lower label makes 7 moves: $\{2\} \to \{1, 1\} \to \{1, 0, 0\} \to \cdots$.

### The limits of the method

- **No algorithm decides termination.** Whether a program stops on a given input is the [halting problem](/halting-problem/), which is undecidable. So no tool finds a measure for every program that stops. See [undecidability of termination](/undecidability-of-termination/). Tools search for measures of a fixed form, such as linear functions of the variables or lexicographic tuples of them, and the [size-change termination](/size-change-termination/) method checks recursive calls without an explicit measure.
- **The method is complete.** If a program stops from every state that satisfies $I$, a measure exists. For a deterministic program, the number of steps that are left is a measure into $\mathbb{N}$. If a step can choose among infinitely many next states, as in RESET-LOOP above, no measure into $\mathbb{N}$ may exist, and a measure into the ordinals is needed. The proof for RESET-LOOP is on the [variant function](/variant-function/) page.

## Variations

- **Termination of recursion.** Show that the argument decreases in a well-founded order at each recursive call. In proof assistants, the same idea is a rule that accepts a recursive definition only when a decreasing measure is given.
- **Lexicographic measures.** Used for nested loops that reset an inner counter, and for functions of the Ackermann type.
- **Bounded steps.** When $W = \mathbb{N}$ and the decrease is at least 1, the initial value of the measure is an upper bound on the number of steps. A measure that halves gives a logarithmic bound.
- **Multiset orders.** If a step removes one item and adds any finite number of smaller items, the multiset of the items decreases in the multiset order, which is well-founded. It is used for rewrite systems.

## Pitfalls

- **A decrease that is not strict.** If the measure can stay equal at one branch of the body, the argument fails. In binary search with $lo \leftarrow mid$ instead of $lo \leftarrow mid + 1$, the measure $hi - lo$ stays 1 when $hi - lo = 1$.
- **A measure not bounded below.** A strictly decreasing integer does not give termination if it can become negative. Prove $v \ge 0$ under the invariant, and use the invariant: the bound may depend on it.
- **A decrease on a real number.** The sequence $1, 1/2, 1/4, \ldots$ decreases and never ends. The order must be well-founded. The order on the non-negative reals is not.
- **A measure that does not account for all the branches.** Check each branch, each early `continue` and each recursive call, not only the main one.
- **Forgotten edge values.** Check the empty range and the range with one item. A measure that works for a range of length 5 can fail for a range of length 1.
- **Confusing the bound with the cost.** The initial value of the measure bounds the number of passes only if each pass lowers it by at least 1. It says nothing about the cost of one pass.

## Exercises

1. Prove that the loop `while n > 1: n ← ⌊n / 2⌋` stops for each integer $n \ge 1$. Give the exact number of passes in terms of $n$. What is it for $n = 1000$?
2. Show that `while i != 0: i ← i − 2` does not stop for $i = 3$. Add a precondition to the loop and a measure that make the termination proof work.
3. Prove, with a lexicographic measure, that the loop `while x > 0 or y > 0: if y > 0 then (x, y) ← (x, y − 1) else (x, y) ← (x − 1, 2x)` stops. Compute the exact number of passes for $x = 3$ and $y = 0$.
4. A function $f$ on $\mathbb{N}$ is defined by $f(0) = 0$ and $f(n) = f(\lfloor n/3 \rfloor) + 1$ for $n \ge 1$. Prove that the recursion terminates and give a bound on the depth.
5. Prove that the lexicographic order on $\mathbb{N}^3$ is well-founded.
6. Give a loop for which $\mathbb{N}$ is not enough but $\mathbb{N} \times \mathbb{N}$ is, other than the ones on this page. Prove its termination.
7. Show that the order "$a \prec b$ when $a < b$" on the non-negative rational numbers is not well-founded. Give an infinite decreasing sequence.
8. In the Ackermann function, prove by induction on $n$ that $A(1, n) = n + 2$ and $A(2, n) = 2n + 3$.

## References
