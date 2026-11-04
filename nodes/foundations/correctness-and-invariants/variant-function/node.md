---
tag: E88TBX
kind: definition
slug: variant-function
name: Variant function
aliases:
- Loop variant
- Ranking function
- Bound function
- Decreasing measure
area: foundations/correctness-and-invariants
level: intro
summary: A quantity that is non-negative (or bounded below) and strictly decreases each iteration, forcing termination.
prereqs: [loop-invariant, induction]
see_also: [termination-proof, well-founded-relation, total-correctness, invariant, well-ordering-principle]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.1, Algorithm E (Euclid's algorithm) and its finiteness
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.3, the analysis of Euclid's algorithm
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.2, Greatest common divisor (Euclid's algorithm and Lamé's theorem)
  - book: isbn:9780387964805
    title: David Gries, The Science of Programming
    locator: Part II, the chapter on the iterative construct (the invariant and the bound function of a loop)
  - paper: "Robert W. Floyd, Assigning meanings to programs, Proceedings of Symposia in Applied Mathematics 19 (1967)"
    locator: pages 19 to 32, the final section (termination by a map into a well-ordered set)
---

A variant function of a loop is a function from the program state to the natural numbers (or to another well-founded set) that is non-negative whenever the loop runs and that gets smaller at each pass. Because a natural number cannot get smaller forever, the loop must stop. A variant is the standard tool for the termination half of a proof of [total correctness](/total-correctness/). Its role is the opposite of an [invariant](/invariant/): an invariant stays the same, and a variant must change.

## Definition

Let $L$ be the loop $\textbf{while } C \textbf{ do } B$. Let $I$ be a [loop invariant](/loop-invariant/) of $L$. A *variant function* (also called a ranking function or a bound function) for $L$ with respect to $I$ is a function $v$ from program states to $\mathbb{Z}$ such that, for each state $s$ with $I(s) \wedge C(s)$:

1. **Bounded below.** $v(s) \ge 0$.
2. **Decrease.** If one pass of $B$ takes $s$ to $s'$, then $v(s') \le v(s) - 1$.

More generally, $v$ may map into a set $W$ with a [well-founded relation](/well-founded-relation/) $\prec$, and condition 2 becomes $v(s') \prec v(s)$. Then condition 1 is replaced by the fact that $\prec$ has no infinite descending chain. The case $W = \mathbb{N}$ with the usual order is the one that this page treats. See the [termination proof](/termination-proof/) page for other choices of $W$.

**Theorem.** Let $I$ be a loop invariant of $L$ (it holds before the first test, and each pass that starts in a state with $I \wedge C$ ends in a state with $I$), and let $v$ be a variant for $L$ with respect to $I$. Assume that each pass of $B$ stops. If the loop starts in a state $s_0$ with $I(s_0)$, then the loop stops. If $C(s_0)$ holds, it makes at most $v(s_0) + 1$ passes, and at most $v(s_0)$ passes when $v(s) \ge 1$ whenever $I(s) \wedge C(s)$.

*Proof.* Suppose the loop makes at least $K \ge 1$ passes, and let $s_0, s_1, \ldots, s_{K-1}$ be the states before the first $K$ passes. Each $s_k$ satisfies $C$, because a pass starts from it, and satisfies $I$, by initialization and maintenance. By induction on $k$, condition 2 gives $v(s_k) \le v(s_0) - k$ for $0 \le k \le K-1$. Condition 1 gives $v(s_{K-1}) \ge 0$. So $0 \le v(s_0) - (K - 1)$, that is, $K \le v(s_0) + 1$. Hence the loop cannot make $v(s_0) + 2$ passes, and since each pass stops, the loop stops. If $v \ge 1$ on each state with $I \wedge C$, then $1 \le v(s_{K-1}) \le v(s_0) - (K-1)$, so $K \le v(s_0)$. $\blacksquare$

In the proof, the key point is that $v$ drops by at least 1 at each pass, so the number of passes is bounded by a fixed number. A decrease by a smaller and smaller amount is not enough (see the non-examples).

## Examples and non-examples

### Euclid's algorithm

```pseudo id=euclid
EUCLID(a, b)                      ▷ a, b integers, a ≥ 0, b ≥ 0
L1  while b ≠ 0 do
L2      (a, b) ← (b, a mod b)
L3  return a
```

Take $I$ to be: $a$ and $b$ are integers with $a \ge 0$ and $b \ge 0$. The variant is $v = b$.

- **I is an invariant.** It holds at the start by the precondition. If $b \ne 0$, the new pair is $(b, a \bmod b)$, and $b \ge 0$ and $0 \le a \bmod b$.
- **Bounded below.** On $I \wedge (b \ne 0)$ we have $b \ge 1$, so $v \ge 1 \ge 0$.
- **Decrease.** The new value of $b$ is $a \bmod b$. For integers $a \ge 0$ and $b \ge 1$, $0 \le a \bmod b \le b - 1$. So $v' \le v - 1$.

By the theorem, the loop makes at most $b_0$ passes, where $b_0$ is the input value of $b$. For $(a, b) = (1071, 462)$ the values of $b$ are $462, 147, 21, 0$: three passes, and the result is $\gcd = 21$. The bound $b_0 = 462$ is far from tight. The variant $b$ gives only a linear bound. A second variant gives a logarithmic one.

*Claim.* Let $b_0, b_1, \ldots$ be the values of $b$ before each test, so that $b_{k+1} = b_{k-1} \bmod b_k$ for $k \ge 1$. If $b_{k+1} \ne 0$, then $b_{k+2} < b_k / 2$. *Proof.* We have $1 \le b_{k+1} < b_k$, since each value is a remainder modulo the one before it. If $b_{k+1} \le b_k/2$, then $b_{k+2} = b_k \bmod b_{k+1} < b_{k+1} \le b_k/2$. If $b_{k+1} > b_k/2$, then $b_k < 2b_{k+1}$, so the quotient of $b_k$ by $b_{k+1}$ is 1 and $b_{k+2} = b_k - b_{k+1} < b_k/2$. $\square$

So $b$ at least halves every two passes, and $\lfloor \lg b \rfloor$ drops by at least 1 every two passes. For $b_0 \ge 1$ the loop makes at most $2 \lg b_0 + 2$ passes. The exact worst case is known: Lamé's theorem says that if the loop makes $k$ passes on $a > b \ge 1$, then $b \ge F_{k+1}$, the $(k+1)$st [Fibonacci number](/fibonacci-numbers/), so the number of passes is at most about $\log_\phi b_0$ with $\phi = (1 + \sqrt{5})/2$ (CLRS, Section 31.2; Knuth, Volume 2, Section 4.5.3). For $(a, b) = (13, 8)$ the values of $b$ are $8, 5, 3, 2, 1, 0$: five passes, and $8 = F_6$.

### Binary search

```pseudo id=binary-search
BINARY-SEARCH(A, x)               ▷ A[0 .. n − 1] sorted
L1  lo ← 0, hi ← n
L2  while lo < hi do
L3      mid ← lo + ⌊(hi − lo) / 2⌋
L4      if A[mid] < x then lo ← mid + 1
L5      else if A[mid] > x then hi ← mid
L6      else return mid
L7  return NIL
```

Take $I$ to be $0 \le lo \le hi \le n$ and the variant $v = hi - lo$.

- **I is an invariant.** At the start $lo = 0$ and $hi = n$. In a pass, $lo < hi$ and $lo \le mid < hi$, because $mid = lo + \lfloor (hi - lo)/2 \rfloor$ and $0 \le \lfloor (hi-lo)/2 \rfloor < hi - lo$ when $hi - lo \ge 1$. So $lo' = mid + 1 \le hi$ and $hi' = mid \ge lo$ keep $I$.
- **Bounded below.** On $I \wedge (lo < hi)$, $v = hi - lo \ge 1$.
- **Decrease.** Write $d = hi - lo \ge 1$, so $mid - lo = \lfloor d/2 \rfloor$. If line L4 runs, the new value is $hi - (mid + 1) = d - \lfloor d/2 \rfloor - 1 = \lceil d/2 \rceil - 1 \le \lfloor d/2 \rfloor$. If line L5 runs, it is $mid - lo = \lfloor d/2 \rfloor$. Line L6 leaves the loop. In both cases $v' \le \lfloor d/2 \rfloor \le d - 1$ because $d \ge 1$.

The decrease is more than 1: the variant at least halves. After $k$ passes, $v \le \lfloor n/2^k \rfloor$. A pass happens only if $v \ge 1$ before it, so the number $K$ of passes satisfies $\lfloor n/2^{K-1} \rfloor \ge 1$, that is $K \le \lfloor \lg n \rfloor + 1$ for $n \ge 1$. The bound is reached: for $n = 1000$ some search makes 10 passes, and $\lfloor \lg 1000 \rfloor + 1 = 10$.

For $A = [2, 4, 6, 8, 10, 12, 14]$ and $x = 13$, the values of $hi - lo$ before each pass are $7, 3, 1$.

### Non-examples

- **No decrease.** Change line L4 of binary search to $lo \leftarrow mid$. For $A = [10]$ and $x = 20$, the state is $lo = 0$, $hi = 1$, $mid = 0$ and $A[0] < x$, so $lo$ stays 0 and $hi - lo$ stays 1 at every pass. The variant does not decrease, and the loop does not stop.
- **Not bounded below.** The loop `while true: n ← n − 1` decreases $n$ at each pass, but $n$ has no lower bound, and the loop never stops. Condition 1 fails.
- **Decreases by less and less.** Let $x$ be a real number and run `while x > 0: x ← x / 2`. The value of $x$ decreases at each pass and stays above 0. This loop does not stop in exact arithmetic. Here $x$ is not a natural number and does not drop by a fixed amount, so $x$ is not a variant. In floating-point arithmetic the loop does stop, when $x$ underflows to 0, but the proof of that is about the number format, not about this variant.
- **An invariant is not a variant.** The quantity $\gcd(a, b)$ in Euclid's algorithm does not change. It is useful as an invariant, and useless as a variant.

### Every terminating loop has a variant, with one limit

The method is complete for deterministic loops. Suppose that the body is deterministic and stops, and that from each state with $I$ the loop stops. Let $v(s)$ be the number of passes that the loop makes when it starts in state $s$. On a state with $I \wedge C$, $v(s) \ge 1$, and one pass leads to a state $s'$ with $v(s') = v(s) - 1$. So $v$ is a variant. In practice the work is to find a variant that has a simple formula.

The limit is a body that can choose among infinitely many next states. Take `while x > 0 or y > 0: if y > 0 then y ← y − 1 else (x ← x − 1; y ← any natural number)`. Each run stops (see the [termination proof](/termination-proof/) page), but no variant into $\mathbb{N}$ exists. Suppose $v$ were one, and let $c = v(1, 0)$. From $(1, 0)$ the body may go to $(0, c + 1)$. From there the loop makes $c + 1$ passes through $(0, c+1), (0, c), \ldots, (0, 1)$, and $v \ge 0$ on $(0, 1)$, so by condition 2, $v(0, c+1) \ge c$. Then $v(1, 0) \ge v(0, c+1) + 1 \ge c + 1$, which contradicts $v(1, 0) = c$. The pair $(x, y)$ in the lexicographic order is a variant into a [well-founded relation](/well-founded-relation/), and in that order the state $(1, 0)$ has rank $\omega$.

## Related definitions

- [Loop invariant](/loop-invariant/): the statement that makes the variant meaningful. The variant needs only to be bounded below and to decrease on states that satisfy the invariant.
- [Termination proof](/termination-proof/): the technique of choosing a variant, including variants into well-founded sets other than $\mathbb{N}$, such as pairs ordered lexicographically.
- [Well-founded relation](/well-founded-relation/): the general setting. A relation is well-founded when it has no infinite descending chain, and a variant into such a set forces termination.
- [Well-ordering principle](/well-ordering-principle/): the fact that every non-empty set of natural numbers has a least element, which is why a variant in $\mathbb{N}$ cannot decrease forever.
- [Total correctness](/total-correctness/): partial correctness plus termination.

## References
