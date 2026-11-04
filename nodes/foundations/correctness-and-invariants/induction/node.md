---
tag: R0YK57
kind: technique
slug: induction
name: Mathematical induction
aliases:
- Induction
- Simple induction
- Strong induction
area: foundations/correctness-and-invariants
level: intro
summary: Proves a statement for all natural numbers by proving a base case and that each case implies the next (strong form uses all earlier cases).
prereqs: []
see_also: [well-ordering-principle, structural-induction, loop-invariant, well-founded-relation, proof-by-contradiction, termination-proof, substitution-method, tower-of-hanoi]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.1, Mathematical induction
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 1.1, The Tower of Hanoi
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 0.4, Types of proof (proof by induction)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.1 (loop invariants, which are proved by induction) and Section 4.3 (the substitution method for solving recurrences)
  - url: https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/mit6_042js15_textbook2.pdf
    title: Eric Lehman, F. Thomson Leighton and Albert R. Meyer, Mathematics for Computer Science (2015 version)
    locator: Chapter 5, Induction (ordinary and strong induction, and their equivalence)
---

Mathematical induction is a proof technique for a statement $P(n)$ about all natural numbers $n$. You prove a base case, and you prove that each case follows from the cases before it. The technique is the basis of every proof about a [loop invariant](/loop-invariant/), a recursive algorithm or a recurrence. It has two forms, weak induction and strong induction, and they prove the same statements.

## In plain words

Think of a row of dominoes that has no end. You want all of them to fall. It is enough to show two things. First, the first domino falls. Second, whenever one domino falls, the next one falls too. The second fact covers all of them at once.

A proof by induction has the same two parts. The base case shows that the statement is true for the smallest value. The step shows that if the statement is true for one value, it is true for the next. In the strong form, the step may use all the smaller values, not only the last one. This is the right tool when a problem breaks into two smaller problems of different sizes, as in merge sort.

A loop is a row of dominoes too. The state before the first pass is the base case, and each pass is one step.

## When it applies

Use induction when you have these signs.

- The claim is "for all $n$" with $n$ a natural number, a length, a size or a number of steps.
- The object for $n+1$ is built from the object for $n$, or from smaller objects. Examples are a recursive call, a loop pass, a recurrence and a closed form that you guess.
- You can state the claim as a predicate $P(n)$ that is true or false for each single $n$.

If the objects are trees, lists or terms defined by rules, use [structural induction](/structural-induction/). If the order is not the order of the natural numbers, use induction on a [well-founded relation](/well-founded-relation/).

## The template

**Weak induction.** Let $P(n)$ be a predicate on the natural numbers, and let $n_0$ be a natural number. The principle is

$$\big(P(n_0) \ \wedge\ \forall n \ge n_0 : (P(n) \Rightarrow P(n+1))\big) \ \Rightarrow\ \forall n \ge n_0 : P(n).$$

**Strong induction.** The principle is

$$\big(\forall n \ge n_0 : (\forall k \in [n_0, n) : P(k)) \Rightarrow P(n)\big) \ \Rightarrow\ \forall n \ge n_0 : P(n).$$

For $n = n_0$ the set $[n_0, n)$ is empty, so the step for $n_0$ must prove $P(n_0)$ with no hypothesis. This is the base case. A strong step often needs more than one base case in practice, because the argument for small $n$ may use fewer smaller values than the general argument needs. See the postage example below.

Write each proof in these parts.

1. **Predicate.** State $P(n)$ in full. Say which variable the induction is on, and the range of $n$.
2. **Base case.** Prove $P(n_0)$, or the first few cases that the step cannot cover.
3. **Step.** Fix an arbitrary $n$. Assume the induction hypothesis: $P(n)$ for weak induction, or $P(k)$ for all $k$ with $n_0 \le k < n$ for strong induction. Prove $P(n+1)$, or $P(n)$ in the strong form. Say where you use the hypothesis.
4. **Conclusion.** Say that $P(n)$ holds for all $n \ge n_0$ by induction.

The two forms prove the same statements. Weak induction is the special case of strong induction where the step uses only $P(n-1)$. Strong induction follows from weak induction applied to the predicate $Q(n) = \forall k \in [n_0, n] : P(k)$. Weak induction, strong induction and the [well-ordering principle](/well-ordering-principle/) are equivalent: each one proves the other two. That page gives the three proofs.

**Induction on a loop counter.** Let a loop have the test $C$ and the body $B$. Let $P(i)$ say: "if the loop runs at least $i$ passes, then after $i$ passes the state satisfies $I$". The base case $P(0)$ is the claim that $I$ holds before the loop. The step is the claim that one pass of $B$ keeps $I$ when $C$ is true. Then $I$ holds after every pass, whatever the number of passes. This is the proof of a [loop invariant](/loop-invariant/) in its basic form. It shows nothing about the number of passes: a separate [termination proof](/termination-proof/) shows that the loop stops.

## Classic examples

**The sum of the first $n$ positive integers.** Claim: $P(n)$ is $\sum_{k=1}^{n} k = n(n+1)/2$, for $n \ge 0$ (the empty sum is 0). Base case: for $n = 0$ both sides are 0. Step: assume $P(n)$. Then $\sum_{k=1}^{n+1} k = n(n+1)/2 + (n+1) = (n+1)(n+2)/2$, which is $P(n+1)$. For example, $n = 10$ gives 55.

**Induction on a loop counter.** This is the basic proof of a [loop invariant](/loop-invariant/). Take this loop, with the precondition that $n$ is an integer and $n \ge 0$.

```pseudo id=main
SUM-OF-ODD(n)                     ▷ n an integer, n ≥ 0
L1  s ← 0, i ← 0
L2  while i < n do
L3      i ← i + 1
L4      s ← s + (2i − 1)
L5  return s
```

Claim: before each test of line L2, $s = i^2$ and $0 \le i \le n$. Base case: before the first test, $i = 0$ and $s = 0 = 0^2$, and $0 \le 0 \le n$ by the precondition. Step: assume $s = i^2$ and $0 \le i \le n$, and assume that the test $i < n$ is true. The pass sets $i' = i + 1$ and $s' = i^2 + 2(i+1) - 1 = (i+1)^2$. From $i < n$ and integers, $i' = i + 1 \le n$, and $i' \ge 1 \ge 0$. So the claim holds at the next test. Exit: the test is false, so $i \ge n$. Together with $i \le n$ this gives $i = n$, so the result is $s = n^2$. Termination: the value $n - i$ is a natural number by the claim, and each pass lowers it by 1, so the loop makes exactly $n$ passes. For $n = 5$ the values of $s$ are $0, 1, 4, 9, 16, 25$. Without the precondition the proof fails: for $n = -3$ the loop makes no pass and returns $0$, not $9$.

**The Fibonacci bound.** Let $F_0 = 0$, $F_1 = 1$ and $F_n = F_{n-1} + F_{n-2}$ for $n \ge 2$ (the [Fibonacci numbers](/fibonacci-numbers/)). Claim: $F_n < 2^n$ for all $n \ge 1$. A step from $P(n-1)$ alone does not work, because $F_n$ uses the two values before it. Strong induction, or weak induction on $P(n-1) \wedge P(n)$, fixes this. Here we use strong induction. Base cases: $F_1 = 1 < 2$ and $F_2 = 1 < 4$. Step: let $n \ge 3$ and assume the claim for $n-1$ and $n-2$, both at least 1. Then $F_n = F_{n-1} + F_{n-2} < 2^{n-1} + 2^{n-2} < 2^{n-1} + 2^{n-1} = 2^n$. The two base cases are needed: the step for $n = 3$ uses $F_2$ and $F_1$.

**Postage with 4 and 5 cent stamps.** Claim: each integer $n \ge 12$ is $4a + 5b$ for some integers $a, b \ge 0$. The integers 1, 2, 3, 6, 7 and 11 below 12 are not of this form, so 12 is the best start. Use strong induction with four base cases: $12 = 4 \cdot 3$, $13 = 4 \cdot 2 + 5$, $14 = 4 + 5 \cdot 2$ and $15 = 5 \cdot 3$. Step: let $n \ge 16$ and assume the claim for all $k$ with $12 \le k < n$. Since $n - 4 \ge 12$, the hypothesis gives $n - 4 = 4a + 5b$, so $n = 4(a+1) + 5b$. The step uses $P(n-4)$, which is why four base cases are needed: $n - 4 \ge 12$ only when $n \ge 16$.

**A recurrence by the substitution method.** The [substitution method](/substitution-method/) solves a recurrence in two steps: guess a bound, then prove it by strong induction. Let $T(1) = 1$ and $T(n) = 2T(\lfloor n/2 \rfloor) + n$ for $n \ge 2$. Claim: $T(n) \le n \lg n + n$ for all $n \ge 1$. Base case: $T(1) = 1 = 1 \cdot 0 + 1$. Step: let $n \ge 2$ and assume the claim for all $k$ with $1 \le k < n$. Let $m = \lfloor n/2 \rfloor$. Then $1 \le m < n$, so the hypothesis gives $T(m) \le m \lg m + m$. Since $0 \le \lg m \le \lg(n/2)$ and $2m \le n$,
$$T(n) \le 2m \lg m + 2m + n \le n \lg(n/2) + n + n = n \lg n + n.$$
The first values are $T(1), \ldots, T(8) = 1, 4, 5, 12, 13, 16, 17, 32$, and $T(8) = 32 = 8 \lg 8 + 8$, so the bound is exact at powers of 2. The guess must be strong enough to pass the base case: the bound $T(n) \le n \lg n$ is false at $n = 1$, where it says $1 \le 0$. The extra term $+n$ fixes this. See [recurrence relation](/recurrence-relation/) and the [master theorem](/master-theorem/) for other methods.

**The Tower of Hanoi.** The [Tower of Hanoi](/tower-of-hanoi/) with $n$ disks takes $T_n = 2T_{n-1} + 1$ moves, with $T_0 = 0$. Weak induction proves the closed form $T_n = 2^n - 1$ (Exercise 6). A second induction shows that no method uses fewer moves: the largest disk must move at least once, and at its first move the other $n - 1$ disks must all be on the one peg that is neither its source nor its target. To get there takes at least $T_{n-1}$ moves, and to bring them back on top of it after its last move takes at least $T_{n-1}$ more. So each method uses at least $2T_{n-1} + 1$ moves (Graham, Knuth and Patashnik, Section 1.1).

**Merge sort.** The proof that [merge sort](/merge-sort/) is correct is a strong induction on the length of the range: the two recursive calls get shorter ranges, so the hypothesis applies to both.

## Variations

- **Start above 0.** Use a base case $n_0$. This is the same principle with the range shifted.
- **Several base cases.** Needed when the step reaches back $m$ values. Prove $P(n_0), \ldots, P(n_0+m-1)$ first.
- **Induction on a different measure.** Induct on the size, the height, the number of edges or the length of a string. Define the measure, and check that each use of the hypothesis is on a smaller value of it.
- **Stronger hypothesis.** Sometimes $P(n)$ cannot be proved from $P(n-1)$, but a stronger claim $Q(n)$ can. This is called strengthening the induction hypothesis. A loop invariant is often a strengthened form of the claim that you want.
- **Structural induction and well-founded induction.** These generalise the principle to trees, lists and to any [well-founded relation](/well-founded-relation/). See [structural induction](/structural-induction/).
- **Descent.** Induction in reverse: assume a counterexample, take the least one, and find a smaller one. This is a [proof by contradiction](/proof-by-contradiction/) that uses the [well-ordering principle](/well-ordering-principle/).

## Pitfalls

- **A missing base case.** A true step proves nothing without a base case. Take $P(n)$: "$n = n + 1$". The step is true, because adding 1 on both sides turns $P(n)$ into $P(n+1)$. But $P(0)$ is false, and so is each $P(n)$.
- **A step that fails for small $n$.** The false proof that all horses in a set of $n$ horses have the same color uses a step that needs two sets of $n$ horses that share a horse. For $n = 1$, to $n+1 = 2$, the two sets of one horse do not share a horse. So the step fails at the first value, and the base case $n = 1$ does not help.
- **Using the claim for $n+1$ in the proof of $P(n+1)$.** Use only the hypothesis. A circular argument is not an induction.
- **Using the hypothesis out of range.** In strong induction, check that each smaller value that you use is in the range $[n_0, n)$. In the postage example, $n - 4 \ge 12$ must hold.
- **Two variables.** If the claim has two variables, say which one carries the induction. Fix the other as an arbitrary value before the step, and do not change it.
- **Induction on a loop without termination.** The induction on the loop counter shows that the invariant holds after each pass that happens. It does not show that the loop ends. For that, see the [termination proof](/termination-proof/).

## Exercises

1. Prove by induction that $\sum_{k=1}^{n} (2k - 1) = n^2$ for all $n \ge 0$.
2. Prove by induction that $4^n - 1$ is divisible by 3 for all $n \ge 0$.
3. Prove that $2^n \ge n^2$ for all $n \ge 4$. Show that the claim fails for $n = 3$. Show that the step from $n$ to $n+1$ is correct for all $n \ge 3$, and say why this does not prove the claim for $n = 3$.
4. Prove with strong induction that each integer $n \ge 2$ is a product of one or more primes. Which base cases do you need?
5. Let $T(1) = 0$ and $T(n) = T(\lceil n/2 \rceil) + T(\lfloor n/2 \rfloor) + n - 1$ for $n \ge 2$ (the worst-case number of comparisons of merge sort is bounded by this recurrence). Prove that $T(n) \le n \lg n$ for all $n \ge 1$. Why is weak induction not enough?
6. Tower of Hanoi: let $T_n$ be the least number of moves to move $n$ disks, with $T_0 = 0$ and $T_n = 2T_{n-1} + 1$. Prove that $T_n = 2^n - 1$.
7. Find the error in this proof that $n^2 + n$ is odd for all $n \ge 1$: "Assume that $n^2 + n$ is odd. Then $(n+1)^2 + (n+1) = (n^2 + n) + 2(n+1)$ is an odd number plus an even number, so it is odd." Is the claim true for any $n$?
8. For the loop `s ← 0; for i ← 1 to n do s ← s + i * i`, state an invariant for the sum of squares and prove it by induction on the loop counter. The closed form is $n(n+1)(2n+1)/6$.

## References
