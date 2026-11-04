---
tag: X5FKYE
kind: technique
slug: slope-trick
name: Slope trick
area: techniques/dynamic-programming
level: advanced
summary: Keeps a convex piecewise linear DP function as a set of slope change points in a heap, updating it with cheap operations.
prereqs: [convex-function, priority-queue, binary-heap]
see_also: [isotonic-regression, convex-function, priority-queue, convex-hull-trick, aliens-trick, median]
sources:
  - paper: doi:10.4230/OASIcs.SOSA.2019.1
    title: Günter Rote, Isotonic regression by dynamic programming, 2nd Symposium on Simplicity in Algorithms (SOSA 2019), OASIcs 69, 1:1-1:18, 2019
    locator: the dynamic program over convex piecewise linear functions and its O(n log n) implementation for the L1 norm with a priority queue
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 3.2, Operations that preserve convexity (sums, and partial minimization in Section 3.2.5)
---

The slope trick is a way to run a dynamic program whose state is a real or integer value $y$ and whose table $f_i(y)$ is a convex piecewise linear function of $y$. Instead of storing $f_i$ at every $y$, it stores the points where the slope of $f_i$ changes, each with its change, in one or two [priority queues](/priority-queue/), plus the minimum value. Typical DP steps, such as adding $|y - x|$, taking a prefix minimum $\min_{z \le y} f(z)$, or shifting by a constant, become a few heap operations. A DP that would take $O(n \cdot V)$ time over a value range of size $V$ then takes $O(n \log n)$. The classic use is $L_1$ [isotonic regression](/isotonic-regression/): make a sequence nondecreasing with the least total change.

## In plain words

Some DP tables are indexed by a number that can be huge, such as the value you give to the current element. But the table, drawn as a curve, is often a bowl made of straight pieces. A bowl of straight pieces is fixed by its lowest value and the places where it bends.

So you keep only the bend points, in a heap, and the lowest value. Each DP step changes the curve in a simple way: it adds a new bowl, or it flattens the right side. Each such change adds or removes a few bend points. A heap gives you the largest bend point fast, which is exactly the one these changes touch.

## When it applies

- The DP has the form $f_{i}(y) = \text{(operations on } f_{i-1}) $ for a state value $y$ that ranges over a large or continuous set.
- Each $f_i$ is convex and piecewise linear with integer slopes. Convexity is kept by the operations below, so it is enough that $f_0$ is convex.
- The operations are among these:

| operation | effect on the function | effect on the stored points |
|---|---|---|
| add $\max(0, y - x)$ | slope $+1$ right of $x$ | insert $x$ |
| add $\max(0, x - y)$ | slope $-1$ left of $x$ | insert $x$ |
| add $\lvert y - x \rvert$ | both | insert $x$ twice |
| prefix minimum $\min_{z \le y} f(z)$ | remove the part with positive slope | delete all points right of the minimum |
| suffix minimum $\min_{z \ge y} f(z)$ | remove the part with negative slope | delete all points left of the minimum |
| shift: $f(y - c)$ | move right by $c$ | add $c$ to all points, with a lazy offset |
| add a constant | change the minimum value | none |

Here a "point" means one unit of slope change, so a point with change 2 is stored twice. When the function has both sides, it is kept in two heaps: a max-heap $L$ of the points left of the minimum and a min-heap $R$ of the points right of it.

## The template

$L_1$ isotonic regression: given $a_1, \ldots, a_n$, find a nondecreasing $b_1 \le \cdots \le b_n$ that minimizes $\sum_i |a_i - b_i|$. Let $f_i(y)$ be the least cost of the first $i$ elements with $b_i \le y$. Then

$$f_i(y) = \min_{z \le y} \bigl( f_{i-1}(z) + |a_i - z| \bigr), \qquad f_0 \equiv 0.$$

Each $f_i$ is nonincreasing, so it has only a left side, and one max-heap $L$ is enough. The hole is the cost added per element.

```pseudo id=main
SLOPE-TRICK-ISOTONIC(a, n)
L1  L ← empty max-heap; ans ← 0                ▷ ans is the minimum value of f
L2  for i ← 1 to n do
L3      x ← a_i
L4      push x into L                          ▷ hole: the points of the added cost
L5      if top(L) > x then
L6          ans ← ans + top(L) − x
L7          pop L
L8          push x into L
L9  return ans
```

### Why it works

**Invariant.** After step $i$, $f_i$ is convex, piecewise linear and nonincreasing; its slope is 0 to the right of the largest point of $L$; each point of $L$ is a place where the slope grows by 1; and the minimum value of $f_i$ is $ans$. So $L$ has $i$ points and the slope left of all of them is $-i$.

**Step.** Let $t = \max L$ before the step, and let $g(y) = f_{i-1}(y) + |y - x|$.

- If $x \ge t$: on $y \ge t$, $f_{i-1}$ is constant at $ans$, so $g$ is smallest at $y = x$, with value $ans$. The prefix minimum of $g$ is $f_{i-1}$ plus $|y - x|$ for $y < x$ and $ans$ for $y \ge x$; it bends at the old points and once more at $x$. The template pushes $x$ once and line L5 is false. This matches.
- If $x < t$: on $[x, t]$, the slope of $f_{i-1}$ is at most $-1$ and the slope of $|y - x|$ is $+1$, so $g$ does not increase there; on $y \ge t$, $g$ increases with slope 1. So $\min g = g(t) = ans + (t - x)$, which is line L6. The prefix minimum of $g$ equals $g$ left of $t$ and is constant right of $t$. Compared with $f_{i-1}$, it has two new points at $x$ (from $|y - x|$) and loses the point at $t$ (where the slope now stays 0). Lines L4, L7 and L8 do exactly this.

**Cost.** Each step does at most three heap operations, so the time is $O(n \log n)$ and the space is $O(n)$. A table over all values would take $O(n V)$ time.

## Classic examples

### Make a sequence nondecreasing

For $a = (3, 1, 4, 1, 5, 9, 2, 6)$:

| $i$ | $a_i$ | top before | $L$ after the step | $ans$ |
|---|---|---|---|---|
| 1 | 3 | | 3 | 0 |
| 2 | 1 | 3 | 1, 1 | 2 |
| 3 | 4 | 1 | 1, 1, 4 | 2 |
| 4 | 1 | 4 | 1, 1, 1, 1 | 5 |
| 5 | 5 | 1 | 1, 1, 1, 1, 5 | 5 |
| 6 | 9 | 5 | 1, 1, 1, 1, 5, 9 | 5 |
| 7 | 2 | 9 | 1, 1, 1, 1, 2, 2, 5 | 12 |
| 8 | 6 | 5 | 1, 1, 1, 1, 2, 2, 5, 6 | 12 |

The least total change is 12, for example with $b = (1, 1, 1, 1, 5, 5, 5, 6)$, which costs $2 + 0 + 3 + 0 + 0 + 4 + 3 + 0 = 12$. A DP over all values agrees, also on 500 random inputs.

### Other uses

- **Strictly increasing.** Replace $a_i$ by $a_i - i$ and solve the nondecreasing problem.
- **Moving tokens on a line.** Problems where items move between neighboring positions at a cost per unit of distance, and the state is the net flow across a boundary, give $f_i(y) = \min(\ldots) + |y|$ steps with shifts.
- **Bounded changes.** "Each $b_i$ is within $d$ of $b_{i-1}$" is a minimum over a window, which splits the function at its minimum and shifts the two sides by $-d$ and $+d$. This needs both heaps $L$ and $R$ with lazy offsets.
- **Recovering the solution.** Store the top of $L$ after each step; then set $b_n$ to the last stored value and go backward with $b_i = \min(b_{i+1}, \text{stored value of step } i)$.

## Variations

- **Two heaps.** For functions that are not monotone, keep $L$ for the left side and $R$ for the right side, so that the minimum is between $\max L$ and $\min R$. Adding $\max(0, y - x)$ inserts $x$ into $R$ if $x \ge \max L$, and otherwise inserts $x$ into $L$ and moves $\max L$ to $R$, with the matching update of the minimum value.
- **Weighted points.** Store pairs (position, slope change) when the slope changes by large amounts, as for weighted $|y - x|$.
- **Mergeable heaps.** On trees, the functions of the children are added, which merges their point sets; use mergeable heaps or small to large merging.
- **Other norms.** For the squared error, the functions are piecewise quadratic, and Rote's method stores the pieces in a different structure. The $L_1$ case is the one with the simple heap.

## Pitfalls

- **The function must stay convex.** A step such as "add $-|y - x|$" or a maximum of two functions breaks convexity, and the stored points no longer describe the function.
- **Prefix minimum versus suffix minimum.** Isotonic regression for a nondecreasing $b$ takes the prefix minimum, which removes the right side. Taking the suffix minimum solves the nonincreasing problem.
- **Lazy offsets.** With shifts, each heap needs its own offset, and every comparison between the two heaps must add the offsets first.
- **Reading the solution from the heap.** The final heap does not hold $b$. Use the backward pass of the examples.

## Exercises

1. Prove that the prefix minimum of a convex function is convex.
2. Solve the strictly increasing version of the example: find the least $\sum |a_i - b_i|$ with $b_1 < b_2 < \cdots < b_n$ in the integers.
   <details><summary>Hint</summary>Apply the template to $a_i - i$.</details>
3. Show that the values $b_i$ produced by the backward pass are nondecreasing and reach the cost $ans$.
4. Extend the template to the constraint $|b_i - b_{i-1}| \le d$, and describe the effect on $L$ and $R$.

## References
