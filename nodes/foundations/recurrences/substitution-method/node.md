---
tag: 0X7N0X
kind: technique
slug: substitution-method
name: Substitution method
aliases:
- guess-and-verify
- induction for recurrences
area: foundations/recurrences
level: intro
summary: Guess a closed-form bound for a recurrence and prove it by induction, choosing constants to fit the base case.
prereqs: [recurrence-relation, induction, asymptotic-notation]
see_also: [recursion-tree-method, iteration-method, master-theorem, closed-form-solution, divide-and-conquer-recurrence, merge-sort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 4.3, The substitution method for solving recurrences
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 5.1, A First Recurrence, The Mergesort Algorithm (substituting a solution into the recurrence); Section 5.2, Further Recurrence Relations
  - book: isbn:9780321905758
    title: Robert Sedgewick and Philippe Flajolet, An Introduction to the Analysis of Algorithms, second edition
    locator: Section 2.5, Methods for Solving Recurrences
---

The substitution method solves a [recurrence relation](/recurrence-relation/) in two steps: guess the form of the solution, then prove the guess by [induction](/induction/) on $n$, choosing the constants so that both the inductive step and the base cases hold. It proves upper and lower bounds in [asymptotic notation](/asymptotic-notation/) and exact [closed forms](/closed-form-solution/) alike. It is the only general method that handles floors, ceilings and inequalities directly, and the other methods, such as the [recursion-tree method](/recursion-tree-method/), are often used only to find the guess.

## In plain words

You want to show that the cost of a recursive program is at most some formula. Pick the formula, with a constant that you leave open for now. Then assume that the formula is true for all smaller inputs, put it into the right side of the recurrence, and do the algebra. If the result is at most the formula for the current input, the step works. You also check the few smallest inputs directly. Then you choose the constant large enough for both parts.

The method needs a good guess. If the guess is too low, the algebra fails. If it is too high, the proof works but the bound is weak. A failed step often shows how to fix the guess, for example by subtracting a smaller term.

## When it applies

- The recurrence is given as an equation or an inequality, with any kind of arguments on the right side: fractions with floors and ceilings, $n - 1$, $\sqrt n$, unequal parts.
- You have a candidate solution, from a [recursion tree](/recursion-tree-method/), from the [master theorem](/master-theorem/) applied to a simpler recurrence, from a similar known recurrence, or from computed values.
- You want a proof that holds for each $n$ above a threshold, not only for powers of $b$.
- It does not apply when you have no guess. It finds no answer by itself.

## The template

To prove $T(n) \le g(n)$ for each $n \ge n_0$, where $g$ has open constants $c, d, \ldots$:

1. **Guess.** Choose the form of $g$, for example $g(n) = c \, n \lg n$ or $g(n) = cn - d$.
2. **Hypothesis.** State it with explicit constants and an explicit range: "for each $m$ with $n_0 \le m < n$, $T(m) \le g(m)$". Do not use $O$ here. A hypothesis "$T(m) = O(m)$" has no fixed constant, and induction with it proves nothing.
3. **Step.** For $n$ large enough that each argument $m$ on the right side satisfies $n_0 \le m < n$, substitute $T(m) \le g(m)$ and show that the right side is at most $g(n)$. This step gives conditions on the constants, such as $c \ge 1$ or $d \ge 1$.
4. **Base cases.** The step needs each argument to be at least $n_0$. List the $n \ge n_0$ for which some argument falls below $n_0$, or for which the recurrence does not apply. For a recurrence with argument $\lfloor n/b \rfloor$, these are the finitely many $n$ with $n_0 \le n < b \, n_0$. Check $T(n) \le g(n)$ for each of them. This gives more conditions on the constants.
5. **Constants.** Choose constants that meet all conditions of steps 3 and 4 at the same time. Then the claim holds for each $n \ge n_0$ by strong induction.

For a lower bound $T(n) \ge g(n)$ the template is the same with $\ge$. For $\Theta$ prove both bounds.

## Classic examples

### Merge sort: $T(n) = 2T(\lfloor n/2 \rfloor) + n$

Let $T(1) = 1$ and $T(n) = 2T(\lfloor n/2 \rfloor) + n$ for $n \ge 2$. We show $\frac12 n \lg n \le T(n) \le 2 n \lg n$ for each $n \ge 2$.

*Upper bound, guess $T(n) \le c \, n\lg n$.* The guess fails at $n = 1$, where $c \cdot 1 \cdot \lg 1 = 0 < T(1)$. So take $n_0 = 2$. The arguments $\lfloor n/2 \rfloor$ fall below 2 only for $n \in \{2, 3\}$, so these are the base cases. For $n \ge 4$, $\lfloor n/2 \rfloor \ge 2$, and the hypothesis gives

$$T(n) \le 2c \lfloor n/2 \rfloor \lg \lfloor n/2 \rfloor + n \le c \, n \lg(n/2) + n = c \, n \lg n - cn + n \le c \, n \lg n \quad \text{when } c \ge 1.$$

Base cases: $T(2) = 4 \le 2c$ needs $c \ge 2$, and $T(3) = 5 \le 3c\lg 3 \approx 4.75c$ needs $c \ge 1.06$. So $c = 2$ works, and $T(n) \le 2n\lg n$ for each $n \ge 2$. The bound is tight at $n = 2$.

*Lower bound, guess $T(n) \ge c \, n\lg n$.* The guess $c = 1$ is false: $T(7) = 17 < 7\lg 7 \approx 19.65$. Take $c = \frac12$ and $n_0 = 1$, where $T(1) = 1 \ge 0$. For $n \ge 2$ even, $T(n) \ge n \cdot \frac12 \lg(n/2) + n = \frac12 n\lg n + \frac n2$. For $n \ge 3$ odd, $\lfloor n/2 \rfloor = (n-1)/2$ and

$$T(n) \ge \tfrac12 (n - 1)\lg\tfrac{n-1}{2} + n = \tfrac12 (n-1)\lg(n-1) + \tfrac{n+1}{2}.$$

This is at least $\frac12 n\lg n$ when $n\lg n - (n-1)\lg(n-1) \le n + 1$. The left side equals $\lg n + (n-1)\lg\frac{n}{n-1}$, and $(n-1)\lg(1 + \frac{1}{n-1}) \le \lg e$ because $\ln(1 + x) \le x$. So the left side is at most $\lg n + \lg e$, which is at most $n + 1$ for each $n \ge 1$. Hence $T(n) = \Theta(n \log n)$.

### Subtract a lower-order term: $T(n) = T(\lfloor n/2 \rfloor) + T(\lceil n/2 \rceil) + 1$

Let $T(1) = 1$. The guess $T(n) \le cn$ fails in the step: the right side is $c\lfloor n/2 \rfloor + c\lceil n/2 \rceil + 1 = cn + 1$, which is not at most $cn$ for any $c$. The guess is right in order but too weak to carry the induction. Strengthen it to $T(n) \le cn - d$. The step gives $cn - 2d + 1 \le cn - d$, which holds when $d \ge 1$. The base case $T(1) = 1 \le c - d$ holds for $c = 2$, $d = 1$. So $T(n) \le 2n - 1$, and in fact $T(n) = 2n - 1$ for each $n \ge 1$: the same induction with equalities proves it, since $2\lfloor n/2 \rfloor - 1 + 2\lceil n/2 \rceil - 1 + 1 = 2n - 1$.

### An exact solution: $T(n) = T(\lceil n/2 \rceil) + 1$

Let $T(1) = 0$. Guess $T(n) = \lceil \lg n \rceil$. For $n \ge 2$ let $k = \lceil \lg n \rceil \ge 1$, so $2^{k-1} < n \le 2^k$. Then $2^{k-2} < n/2 \le \lceil n/2 \rceil \le 2^{k-1}$, where the last step holds because $2^{k-1}$ is an integer at least $n/2$. So $\lceil \lg \lceil n/2 \rceil \rceil = k - 1$, and the hypothesis gives $T(n) = (k - 1) + 1 = k$. This counts the comparisons of a binary search that halves with a ceiling.

### Unequal parts: $T(n) = T(n/3) + T(2n/3) + cn$

Take $T$ on the reals, with $T(n) = \Theta(1)$ for $n < 3$. The [recursion tree](/recursion-tree-method/) suggests $\Theta(n\log n)$. Guess $T(n) \le d \, n\lg n$ for $n \ge 3$. The step for $n \ge 9$, where both arguments are at least 3, gives

$$d\frac n3\lg\frac n3 + d\frac{2n}{3}\lg\frac{2n}{3} + cn = d\,n\lg n - d\,n\left(\lg 3 - \tfrac23\right) + cn,$$

which is at most $d \, n \lg n$ when $d \ge c/(\lg 3 - \frac23) \approx 1.089c$. The base region $3 \le n < 9$ is bounded, so a large $d$ covers it. The constant $\lg 3 - \frac23 = \frac13\lg 3 + \frac23\lg\frac32$ is the entropy of the split, and it is the reason why an unbalanced split still costs only $\Theta(n\log n)$.

## Variations

- **Exact solutions.** Guess an exact closed form and prove equality, as in the last two examples. With a computer, compute 20 values from the recurrence first and fit the guess to them.
- **A stronger hypothesis.** When the step almost works, prove something stronger: subtract a lower-order term ($cn - d$, $cn\lg n - dn$), or add a factor that shrinks, as in Leighton's proof of the [Akra-Bazzi theorem](/akra-bazzi-theorem/), which carries a factor $1 + 1/\log^{\varepsilon/2} x$ through the induction to absorb floors and ceilings.
- **Recurrences on the reals.** Induct on the interval that contains $n$: if each argument on the right side is at most $n - 1$ or at most $n/b$, the intervals $[n_0 + j - 1, n_0 + j)$ give a well-founded order.
- **Recurrence inequalities.** If the algorithm gives only $T(n) \le 2T(\lfloor n/2 \rfloor) + cn$, the same proof gives the upper bound. A lower bound needs a lower inequality.
- **Change of variables first.** A recurrence such as $T(n) = 2T(\sqrt n) + \lg n$ is easier after the [change of variables](/change-of-variables/) $n = 2^m$.

## Pitfalls

- **Asymptotic notation inside the induction.** "Assume $T(m) = O(m)$ for $m < n$. Then $T(n) = 2T(n/2) + n = 2 \cdot O(n/2) + n = O(n)$." This "proves" a false bound for merge sort. The constant must be fixed before the induction and the step must give back exactly the same constant: here it gives $cn + n$, which is not at most $cn$.
- **The base case $n = 1$ with $\lg$.** $c \cdot 1 \cdot \lg 1 = 0$, so a bound $T(n) \le c\,n\lg n$ is false at $n = 1$ for each $c$. Start the claim at $n_0 = 2$ and check $n = 2$ and $n = 3$ as base cases.
- **Arguments below the threshold.** The step must not use the hypothesis on an argument below $n_0$. With $n_0 = 2$ and argument $\lfloor n/2 \rfloor$, the step is valid only for $n \ge 4$.
- **A guess that is right in order but fails the step.** As in $T(n) = 2T(n/2) + 1$ with guess $cn$, a failed step does not mean the order is wrong. Try subtracting a lower-order term before trying a larger order.
- **Floors and ceilings dropped without care.** $\lceil n/2 \rceil$ can exceed $n/2$, and $\lg\lceil n/2 \rceil$ can exceed $\lg n - 1$. Bound them explicitly, as in the examples, or use the [smoothness rules](/smoothness-rules/).

## Exercises

1. Prove that $T(n) = T(n-1) + n$, $T(0) = 0$, satisfies $T(n) = n(n+1)/2$. (Exact induction.)
2. Prove $T(n) = O(n^2)$ for $T(n) = 4T(\lfloor n/2 \rfloor) + n$, $T(1) = 1$. (The guess $cn^2$ fails in the step. Use $cn^2 - dn$, bound $-4d\lfloor n/2 \rfloor \le -2dn + 2d$, and choose $d$ and the threshold large enough.)
3. Prove $T(n) = \Theta(\log n)$ for $T(n) = T(\lfloor n/2 \rfloor) + 1$, $T(1) = 1$, and show $T(n) = \lfloor \lg n \rfloor + 1$ exactly.
4. Show that $T(n) = 2T(\lfloor n/2 \rfloor + 17) + n$ is $O(n\log n)$. (Use $n_0$ large enough that $n/2 + 17 \le 3n/4$.)
5. Find the error in the proof "$T(n) = 2T(\lfloor n/2 \rfloor) + n \le 2c\lfloor n/2 \rfloor + n \le cn + n = O(n)$".

## References
