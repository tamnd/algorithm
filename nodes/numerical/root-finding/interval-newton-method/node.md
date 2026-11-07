---
tag: MES2VT
kind: algorithm
slug: interval-newton-method
name: Interval Newton method
aliases:
- interval Newton
- Moore's interval Newton method
- interval Newton operator
- verified Newton method
area: numerical/root-finding
level: research
summary: Newton iteration on intervals that gives guaranteed enclosures of all roots in a box. A box that maps into itself provably holds exactly one root, and widths then shrink quadratically.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {r: "the number of zeros in the start interval", w: "the width of the start interval", s: "the smallest distance between two zeros", δ: "the tolerance", K: "the cap on the iterations"}
  time: {worst: "O(K)", average: "O(r (log(w/s) + log(log(1/δ))))"}
  space: {extra: "O(log(w/δ))"}
  evaluations: {worst: "3 K", step: "3"}
properties: {deterministic: true, recursive: false, bracketing: true, derivative_free: false, global: true, verified: true}
prereqs: [interval-arithmetic, newton-raphson-method, bisection-method]
see_also: [interval-branch-and-bound, bracketing-method, kantorovich-theorem, multiplicity-of-roots, stopping-criteria, newton-method-for-systems, homotopy-continuation, brent-method]
sources:
  - book: isbn:9780898716696
    title: Ramon E. Moore, R. Baker Kearfott and Michael J. Cloud, Introduction to Interval Analysis, SIAM, 2009
    locator: the chapter on interval Newton methods (the operator N(X), the inclusion of all zeros, the existence and uniqueness test, and quadratic convergence)
  - book: "Ramon E. Moore, Interval Analysis, Prentice-Hall, 1966"
    locator: the first statement of the interval Newton method
  - book: "Arnold Neumaier, Interval Methods for Systems of Equations, Cambridge University Press, 1990"
    locator: the chapters on interval Newton operators, the Krawczyk and Hansen-Sengupta operators, and existence and uniqueness tests
  - paper: "Eldon R. Hansen, Interval forms of Newton's method, Computing 20, 153-163, 1978"
    locator: the extended division when the derivative enclosure contains zero, and the splitting into two intervals
  - paper: "Siegfried M. Rump, Verification methods: rigorous results using floating-point arithmetic, Acta Numerica 19, 287-449, 2010"
    locator: verified solution of nonlinear equations with directed rounding, and epsilon inflation
---

The interval Newton method finds every zero of a function $f$ in an interval $X_0 = [a, b]$ with mathematical certainty, even though it computes in floating point. It works with intervals instead of numbers. For a box $X$ with midpoint $m$, it computes the interval Newton operator
$$N(X) = m - \frac{f(m)}{F'(X)},$$
where $F'(X)$ is an interval that contains $f'(x)$ for every $x \in X$. Every zero of $f$ in $X$ lies in $N(X)$, so $X$ can be replaced by $X \cap N(X)$ without losing a zero. If $N(X) \subseteq X$ and $0 \notin F'(X)$, then $X$ contains exactly one zero: this is a proof of existence and uniqueness. When $F'(X)$ contains 0, extended division splits $X$ into at most two parts. Boxes where $f$ provably does not vanish are discarded. The result is a list of tiny intervals, each one either proved to hold exactly one zero or reported as a possible zero (a multiple root, for instance), with a guarantee that no zero outside them was missed. Near a simple zero the widths shrink quadratically, as for [Newton's method](/newton-raphson-method/).

## In plain words

Ordinary Newton's method gives a number that is probably close to a root. The interval version gives an interval that certainly contains a root, or certainly contains none. The mean value theorem says that a root $x^*$ satisfies $x^* = m - f(m)/f'(\xi)$ for some $\xi$ between $m$ and $x^*$. Interval arithmetic lets you evaluate this for all possible $\xi$ at once, which gives a range that the root cannot escape. When that range fits inside the box you started from, a root is trapped, and it is the only one there.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Here $f$ is continuously differentiable on $X_0 = [a, b]$. The user supplies interval extensions $F$ and $F'$: functions of an interval $X$ that return intervals containing $\{f(x) : x \in X\}$ and $\{f'(x) : x \in X\}$. Writing $f$ and $f'$ with [interval arithmetic](/interval-arithmetic/) operators that round outward gives these automatically. The error $e_k$ is replaced by the width $w(X_k)$ of the current box, which bounds it. Each step costs 3 interval evaluations: $F(X)$, $F([m, m])$ and $F'(X)$. With order $q = 2$, the efficiency index is $2^{1/3} \approx 1.26$ in interval evaluations. A box is finished when its width is at most $\delta\max(1, |x|)$ or when a Newton step no longer shrinks it. The whole run stops when the work list is empty or after $K$ iterations.

## The algorithm

```pseudo id=main
INTERVAL-NEWTON(F, F', [a, b], delta, K):
L1   stack <- [ [a, b] ];  found <- []
L2   while stack is not empty:
L3       X <- pop(stack)
L4       if 0 is not in F(X) then discard X;  continue
L5       m <- mid(X);  pieces <- N(X) ∩ X with N(X) = m - F([m, m]) / F'(X)  (extended division if 0 in F'(X));  unique <- (0 not in F'(X) and N(X) ⊆ X)
L6       if unique:
L7           if X is small or the step did not shrink it then add (N(X) ∩ X, "unique") to found  else push N(X) ∩ X
L8       else if X is small then add (X, "possible") to found
L9       else if pieces is one interval at most half as wide as X then push it
L10      else push the pieces, bisecting each piece wider than half of X
L11      if K iterations have been done then return found and the stack as "possible" boxes, status "max-iter"
L12  merge overlapping boxes in found, recheck each for uniqueness, and return them
```

Line L4 is the exclusion test: if the enclosure of $f$ on $X$ does not contain 0, then $f$ has no zero in $X$. Line L5 is the Newton step. When $0 \in F'(X)$ and $0 \notin F([m, m])$, the quotient is a union of two half-lines, and $N(X) \cap X$ is the union of at most two intervals, with a gap around $m$ that provably holds no zero. If both contain 0, $N(X)$ is the whole line, and only bisection helps. Lines L6 and L7 handle a box proved to hold one zero. Newton's steps then contract it quadratically until the width stops shrinking, which happens at a few ulps. Lines L9 and L10 ensure progress: a box is either shrunk by half by the Newton step or bisected. Line L12 joins boxes that share a zero lying exactly on a split point. A zero on the edge of a box cannot pass the test $N(X) \subseteq X$, so the recheck also tries a slightly inflated box (epsilon inflation).

## Example

Take $f(x) = x^2 - 2$ on $X_0 = [1, 2]$ with $F'(X) = 2X$. Then $m = 1.5$, $f(m) = 0.25$ and $F'(X_0) = [2, 4]$, so
$$N(X_0) = 1.5 - \frac{0.25}{[2, 4]} = 1.5 - [0.0625, 0.125] = [1.375, 1.4375] \subseteq [1, 2].$$
This proves that $[1, 2]$ holds exactly one zero, and that it lies in $[1.375, 1.4375]$. The next step has $m = 1.40625$, $f(m) = -0.0224609375$ and $F'(X) = [2.75, 2.875]$, and it gives a box of width $3.6 \times 10^{-4}$. The widths go
$$1,\ 0.0625,\ 3.6 \times 10^{-4},\ 6.7 \times 10^{-9},\ 8.9 \times 10^{-16},$$
each roughly the square of the previous one, until the box is 4 ulps wide around $\sqrt2$. Run from $[0, 3]$, the method needs 7 iterations and 21 interval evaluations. From $[-3, 3]$, the derivative enclosure $[-6, 6]$ contains 0, extended division splits the box, and both $\pm\sqrt2$ are found and verified. For $(x - 1)(x - 2)(x - 3)$ on $[-10, 10]$, it takes 41 iterations and 101 evaluations to return three boxes, each proved to hold exactly one zero. For $x^2 + 1$ on $[-5, 5]$, a single evaluation proves that there is no zero. For $(x - 1)^2$ the result is one box of width $6 \times 10^{-13}$ labelled "possible": a double zero can never be proved unique by this test, because $f'$ vanishes there.

## Correctness

Two facts carry the method. First, if $x^* \in X$ is a zero, the mean value theorem gives $0 = f(m) + f'(\xi)(x^* - m)$ for some $\xi \in X$. If $f'(\xi) \ne 0$, this means $x^* = m - f(m)/f'(\xi) \in N(X)$. If $f'(\xi) = 0$, then $f(m) = 0$, so $0 \in F([m, m])$, and the code uses the whole line. So no step loses a zero, and no discarded box contained one. Second, if $0 \notin F'(X)$ and $N(X) \subseteq X$, then $f$ is strictly monotone on $X$, and the inclusion forces $f$ to change sign between an endpoint of $X$ and $m$. So $X$ holds exactly one zero. Outward rounding makes every computed interval contain the exact one, so both facts survive floating point. Termination comes from the bisection and the size test, and in any case from the cap $K$. The full proofs, including the quadratic convergence of the widths, are in [the correctness proof](proofs/correctness.md).

## Complexity

For a simple zero $x^*$ and boxes small enough that $0 \notin F'(X)$, the widths satisfy $w(N(X)) \le C\,w(X)^2$, with $C$ depending on bounds for $|f'|$ from below and on the Lipschitz constant of $F'$. So once a zero is isolated, $O(\log\log(1/\delta))$ steps suffice. Before that, bisection and the exclusion test do the work, and they need about $\log_2(w/s)$ levels to separate zeros at distance $s$. Each step costs 3 interval evaluations, each 2 to 4 times as costly as a floating point evaluation. The work list is processed depth first and holds $O(\log(w/\delta))$ boxes. Overestimation in $F$ and $F'$ (the dependency problem of interval arithmetic) can make the exclusion test fail on boxes without zeros and slow the early phase. Centred forms and slopes reduce it.

## Properties

- Verified: every reported "unique" box provably contains exactly one zero, and the union of the boxes provably contains every zero in $[a, b]$, including any zeros on the boundary.
- A proof that there is no zero is a by-product, when the box list comes back empty.
- Local order 2 in the width of the box, proved for $f'$ Lipschitz and an interval extension of $F'$ whose width is linear in $w(X)$.
- Multiple zeros, and clusters of zeros closer than the tolerance, end up in "possible" boxes. The method never claims uniqueness wrongly, but it cannot always prove it.
- The cost depends on how tight the interval extensions are, and not only on $f$ itself.

## Variants and improvements

- **Krawczyk operator.** $K(X) = m - Yf(m) + (I - YF'(X))(X - m)$ with $Y \approx f'(m)^{-1}$ avoids interval division altogether and is the usual choice for systems.
- **Hansen-Sengupta operator.** For systems, it solves the interval linear system by an interval Gauss-Seidel sweep, preconditioned by the inverse of the midpoint Jacobian. It is usually sharper than Krawczyk's operator.
- **Systems.** With $F'(X)$ an interval Jacobian, the same inclusion and uniqueness theorems hold in $\mathbb{R}^n$. Combined with bisection, they give verified solvers for nonlinear systems and the core of [interval branch and bound](/interval-branch-and-bound/).
- **Slopes and centred forms.** Replacing $F'(X)$ by an interval slope at $m$ gives narrower enclosures and faster isolation.
- **Epsilon inflation.** Starting from an approximate root found by ordinary Newton, inflate a tiny box around it and verify it in one or two steps. This is how verification libraries certify floating point solutions.

## When to use it

Use it when you need a guarantee: all zeros in an interval and none missed, proofs that a zero exists, or proofs that none does. Typical uses are computer-assisted proofs, safety-critical computation, global optimization and robust geometric predicates. When you only need one root fast, use [Brent's method](/brent-method/) or Newton. For polynomials with many close roots, expect many "possible" boxes unless you raise the precision.

## Pitfalls

- L4: an interval extension that is not a true enclosure breaks everything. Rounding must be outward, and library functions such as exp must be enclosed with their error bound. The reference code widens by one ulp after every operation and assumes that math.exp is within one ulp.
- L5: a zero exactly on a split point lies on the edge of two boxes, where the test $N(X) \subseteq X$ cannot succeed. L12 merges such boxes and verifies a slightly inflated box. The reported box can then reach a few ulps outside $[a, b]$ when the zero sits on the endpoint.
- L5: when $0 \in F([m, m])$ and $0 \in F'(X)$, the operator gives no information. Only the bisection of L10 makes progress.
- L8: a "possible" box is not a zero. It may hold a multiple zero, several close zeros, or none, if overestimation hid the sign of $f$.
- L11: with a small cap the output can contain large unprocessed boxes. They are reported as "possible", so the no-zero-lost guarantee still holds, but nothing is resolved.
- Writing $f$ in a form with many occurrences of $x$ (the dependency problem) makes $F(X)$ much wider than the true range and slows the early phase.

## Implementations

## History

Ramon Moore introduced interval analysis and the interval Newton method in his 1962 thesis and his 1966 book. Krawczyk (1969) proposed the operator that bears his name and avoids interval division. Nickel and Hansen extended the method to derivative enclosures containing zero by extended division, Hansen's 1978 paper giving the form used here, and Kahan's arithmetic for division by intervals containing zero underlies it. Hansen and Sengupta (1981) gave the Gauss-Seidel form for systems. Neumaier's book (1990) organized the theory, and Rump's INTLAB and the epsilon inflation technique made verified Newton steps a routine tool. Tucker's proof of the existence of the Lorenz attractor (1999) is a famous application of interval methods.

## References
