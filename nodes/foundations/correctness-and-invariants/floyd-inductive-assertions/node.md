---
tag: 9PHVXQ
kind: technique
slug: floyd-inductive-assertions
name: Floyd's inductive assertion method
aliases:
- Inductive assertion method
- Floyd's method
area: foundations/correctness-and-invariants
level: advanced
summary: Annotates each program point with an assertion and verifies the assertions by local checks.
prereqs: [assertion, hoare-triple, inductive-invariant, well-founded-relation]
see_also: [hoare-logic, weakest-precondition, loop-invariant, variant-function, termination-proof, partial-correctness, total-correctness, guarded-commands]
sources:
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32, the sections on flowcharts, verification conditions and proofs of termination
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10), 1969
    locator: pp. 576 to 580, the rule of iteration
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.1, Mathematical induction (the proof of Algorithm E by assertions)
  - book: isbn:9780070399105
    title: Zohar Manna, Mathematical Theory of Computation, McGraw-Hill (1974)
    locator: Chapter 3, Verification of programs (flowchart programs, partial correctness by inductive assertions, termination by well-founded sets)
  - paper: doi:10.1007/BF01966091
    title: Peter Naur, Proof of algorithms by general snapshots, BIT 6(4), 1966
    locator: pp. 310 to 316
  - paper: doi:10.1109/MAHC.1984.10017
    title: F. L. Morris and C. B. Jones, An early program proof by Alan Turing, IEEE Annals of the History of Computing 6(2), 1984
    locator: pp. 139 to 143 (Turing's 1949 paper Checking a large routine, with commentary)
---

Floyd's inductive assertion method proves a program correct by attaching an assertion to a few points of its flowchart, the cut points, and by checking one logical formula for each path between two cut points. R. W. Floyd made the method systematic in 1967 and added proofs of termination by well-ordered sets. Similar ideas appear earlier, in a 1949 note by Alan Turing and in the "general snapshots" of Peter Naur (1966). If all the formulas hold, the program is partially correct. A second step, a map from the states at the cut points into a well-ordered set, proves that the program stops. The method is the base of [Hoare logic](/hoare-logic/) and of the verification condition generators of modern program verifiers.

## In plain words

A flowchart with loops has an unbounded number of paths, so you cannot check each path. Floyd's idea is to cut every loop at one point, and to write a true statement at each cut. The first statement says what the input must be, and the last says what the result must be.

Between two cuts the path has no loop. For each such path you ask a local question: if the statement at the first cut is true, and the program follows this path, is the statement at the next cut true? The answers are formulas, and you prove them one by one. If all hold, then each time the program reaches a cut, its statement is true. So the result is right when the program stops.

To show that the program stops, you give each loop a number that falls at every round and cannot fall for ever.

## When it applies

- The program has a control flow graph: assignments, tests and jumps. Structured loops are a special case.
- You can state, for each loop, a property that holds each time the loop test is reached. This is the [inductive invariant](/inductive-invariant/) of the loop, and finding it is the creative step.
- The assignments and tests belong to a theory in which the formulas can be proved: for example integer arithmetic, with unbounded integers.
- The method is for sequential programs.

## The template

**Input.** A flowchart with an entry point and an exit point, a precondition $P_{\mathrm{in}}$ and a postcondition $P_{\mathrm{out}}$.

1. *Choose the cut points.* The entry and the exit are cut points. Add cut points so that each cycle of the flowchart passes through at least one cut point. Usually one at the test of each loop is enough.
2. *Attach assertions.* Put $P_{\mathrm{in}}$ at the entry and $P_{\mathrm{out}}$ at the exit. Put an assertion $P_i$ at each other cut point $i$. It is a formula on the variables $x$ of the program.
3. *List the basic paths.* A basic path $\alpha$ goes from a cut point $i$ to a cut point $j$ and has no other cut point between. Because each cycle has a cut point, the number of basic paths is finite. Each path has a condition $R_\alpha(x)$, the conjunction of the tests that it takes, in terms of the variables at its start, and a transformation $f_\alpha$ that gives the variables at its end from the variables at its start.
4. *Write the verification condition.* For each basic path $\alpha$ from $i$ to $j$:
$$ \forall x : P_i(x) \wedge R_\alpha(x) \implies P_j(f_\alpha(x)). $$
The right side is obtained by substitution of the assignments, in reverse order, as in $Q[E/x]$. In other words it is $P_j$ evaluated after the path, which is $\mathrm{wp}(\alpha, P_j)$ for the path taken as a command. The variable $x$ ranges over all states, not only over the states that the program reaches.
5. *Prove the conditions.* If all hold, the program is partially correct: $\{P_{\mathrm{in}}\}\ \text{program}\ \{P_{\mathrm{out}}\}$.
6. *Prove termination (for total correctness).* Choose a set $L$ of cut points such that each cycle passes through a point of $L$, a well-ordered set $(W, <)$, and for each $i \in L$ a function $\rho_i$ from states to $W$. Show that $P_i(x)$ implies that $\rho_i(x)$ is defined in $W$. For each path $\alpha$ from a point $i \in L$ to the next point $j \in L$, show $P_i(x) \wedge R_\alpha(x) \implies \rho_j(f_\alpha(x)) < \rho_i(x)$.

**Lemma (the assertions hold at every visit).** Assume that all the conditions of step 4 hold. Take any finite prefix of a run that starts in a state that satisfies $P_{\mathrm{in}}$. Then at each visit of the prefix to a cut point $i$, the state satisfies $P_i$.

*Proof.* Let $c_0, c_1, \dots, c_m$ be the visits of the prefix to cut points, in order, with $c_0$ the entry. Between $c_{r}$ and $c_{r+1}$ the run passes no other cut point, so this piece follows a basic path $\alpha$, and the run took the tests of $\alpha$, so $R_\alpha$ holds at $c_r$ and the state at $c_{r+1}$ is $f_\alpha$ of the state at $c_r$. Induction on $r$: the state at $c_0$ satisfies $P_{\mathrm{in}}$ by assumption. If the state at $c_r$ satisfies the assertion of its point, then the verification condition of $\alpha$ gives the assertion of the point of $c_{r+1}$. $\square$

**Why step 5 is sound.** A run that stops reaches the exit, which is a cut point. Apply the lemma to the whole run: the final state satisfies $P_{\mathrm{out}}$.

**Why step 6 is sound.** Suppose that a run from a state that satisfies $P_{\mathrm{in}}$ does not stop. First, it visits $L$ infinitely often. If not, after its last visit to $L$ it takes infinitely many steps in a finite flowchart, so it visits some point twice, and the part between the two visits is a cycle with no point of $L$, against the choice of $L$. Let $v_0, v_1, \dots$ be its visits to $L$. Apply the lemma to the prefix that ends at $v_{r+1}$: at $v_r$ the assertion $P_i$ of its point holds, so $\rho_i$ is defined in $W$ there, and the piece from $v_r$ to $v_{r+1}$ follows a path from $L$ to the next point of $L$ whose condition holds. Step 6 then gives $\rho(v_{r+1}) < \rho(v_r)$. So $\rho(v_0) > \rho(v_1) > \cdots$ is an infinite strictly decreasing sequence in $W$. A well-ordered set has no such sequence, as in the page on [well-founded relations](/well-founded-relation/). So each run stops. This reduces the proof of termination to the choice of $\rho$, as in a [termination proof](/termination-proof/).

## Classic examples

From simple to hard. Each line names the cut point, the assertion there, and the measure.

- **A summing loop.** For $i, s \leftarrow 0, 0$ followed by $\mathbf{while}\ i < n\ \mathbf{do}\ i \leftarrow i + 1 ;\ s \leftarrow s + i$, with precondition $n \ge 0$ and postcondition $s = n(n+1)/2$: the cut is the loop test, the assertion is $s = i(i+1)/2 \wedge 0 \le i \le n$, and $\rho = n - i$. The loop condition is $i(i+1)/2 + i + 1 = (i+1)(i+2)/2$ together with $i < n \implies 0 \le i + 1 \le n$. At the exit, $i \ge n$ and $i \le n$ give $i = n$.
- **[Euclidean algorithm](/euclidean-algorithm/), remainder form.** This is Algorithm E, the example that Knuth proves by assertions in Section 1.2.1 of volume 1. For positive $M$ and $N$, run $m, n \leftarrow M, N$ and then $\mathbf{while}\ n \ne 0\ \mathbf{do}\ m, n \leftarrow n, m \bmod n$. The cut is the test, with the assertion $m > 0 \wedge n \ge 0 \wedge \gcd(m, n) = \gcd(M, N)$ and $\rho = n \in \mathbb{N}$. The loop path needs $\gcd(n, m \bmod n) = \gcd(m, n)$ and $0 \le m \bmod n < n$. At the exit, $\gcd(m, 0) = m$. For $(M, N) = (1071, 462)$ the pairs are $(1071, 462), (462, 147), (147, 21), (21, 0)$, so the result is 21 after 3 rounds.
- **[Integer square root](/integer-square-root/).** Worked out in full below: one cut at the loop test, four basic paths, and $\rho = hi - lo$.
- **[Binary search](/binary-search/).** For the least index $i$ with $a[i] \ge x$ in a sorted array $a[0 \ldots n-1]$, with $lo, hi \leftarrow 0, n$ and the loop $\mathbf{while}\ lo < hi$ that sets $lo \leftarrow mid + 1$ when $a[mid] < x$ and $hi \leftarrow mid$ otherwise: the assertion at the test is $0 \le lo \le hi \le n$, $a[j] < x$ for all $j < lo$, and $a[j] \ge x$ for all $j$ with $hi \le j < n$. The measure is $hi - lo$.
- **[Insertion sort](/insertion-sort/).** Two nested loops give two cut points. At the outer test: $1 \le i \le n$, $A[0 \ldots i-1]$ is sorted, and $A$ is a permutation of the input. At the inner test, where the variable $key$ holds the old value of $A[i]$: $-1 \le j < i$, the cells $A[0 \ldots j]$ and $A[j+2 \ldots i]$ hold the old $A[0 \ldots i-1]$ in order, and every cell of $A[j+2 \ldots i]$ is greater than $key$. With both tests in $L$, take $W = \mathbb{N} \times \mathbb{N}$ in [lexicographic order](/lexicographic-order/), with $\rho = (n - i, i + 1)$ at the outer test and $\rho = (n - i, j + 1)$ at the inner test. The pair falls on each of the three paths: outer to inner sets $j = i - 1$, inner to inner lowers $j$, and inner to outer raises $i$.

### ISQRT in full

The program is on the page for [correctness](/correctness/). Its precondition is $n \ge 0$, and its postcondition is $r^2 \le n < (r+1)^2$. The cut points are the entry A, the loop test B, and the exit C. The assertion at B is $I$: $0 \le lo < hi \wedge lo^2 \le n < hi^2$. Let $g = hi - lo$ and $mid = lo + \lfloor g/2 \rfloor$. There are four basic paths.

| path | condition | update | condition to prove |
|---|---|---|---|
| A to B | none | $lo, hi \leftarrow 0, n + 1$ | $n \ge 0 \implies I[0/lo, (n+1)/hi]$ |
| B to B, first branch | $g > 1 \wedge mid^2 \le n$ | $lo \leftarrow mid$ | $I \wedge g > 1 \wedge mid^2 \le n \implies I[mid/lo]$ |
| B to B, second branch | $g > 1 \wedge mid^2 > n$ | $hi \leftarrow mid$ | $I \wedge g > 1 \wedge mid^2 > n \implies I[mid/hi]$ |
| B to C | $g \le 1$ | $r \leftarrow lo$ | $I \wedge g \le 1 \implies lo^2 \le n < (lo+1)^2$ |

The proofs follow.

- *A to B.* $0 < n + 1$ is true. Also $0 \le n$, and $n < (n+1)^2 = n^2 + 2n + 1$ because $n^2 + n + 1 > 0$.
- *First branch.* Since $g \ge 2$, we have $\lfloor g/2 \rfloor \ge 1$, so $mid \ge lo + 1 > 0$. Also $hi - mid = g - \lfloor g/2 \rfloor \ge 1$, so $mid < hi$. The condition $mid^2 \le n$ is the test, and $n < hi^2$ is in $I$.
- *Second branch.* $mid > lo$ as above, and $lo \ge 0$ is in $I$. The condition $lo^2 \le n$ is in $I$, and $n < mid^2$ is the test.
- *B to C.* From $lo < hi$ and $hi - lo \le 1$ we get $hi = lo + 1$. Then $I$ gives $lo^2 \le n < (lo+1)^2$.

For termination take $W = \mathbb{N}$ and $\rho_B = hi - lo$. By $I$, $hi - lo \ge 1$, so the value is in $\mathbb{N}$. On the first branch the new value is $hi - mid = g - \lfloor g/2 \rfloor \le g - 1$, and on the second it is $mid - lo = \lfloor g/2 \rfloor \le g - 1$, since $g - \lfloor g/2 \rfloor \ge 1$. In both cases it is smaller than $g$. So ISQRT is totally correct: $[n \ge 0]\ \mathrm{ISQRT}\ [r^2 \le n < (r+1)^2]$.

## Variations

- **Lexicographic order.** Some loops need a pair of numbers. Take $\mathbf{while}\ x > 0\ \mathbf{do}$ with the body "if $y > 0$ then $y \leftarrow y - 1$ else $x \leftarrow x - 1 ;\ y \leftarrow$ any natural number" (the new $y$ is read from the input, or chosen without a bound), and the invariant $x \ge 0 \wedge y \ge 0$. Take $W = \mathbb{N} \times \mathbb{N}$ in lexicographic order and $\rho = (x, y)$. Each branch makes the pair smaller: $(x, y - 1) < (x, y)$ and $(x - 1, y') < (x, y)$ for every $y'$. The lexicographic order on pairs of naturals is well-ordered; as an ordinal it is $\omega^2$. No measure into $\mathbb{N}$ works here: if $\rho$ maps into $\mathbb{N}$ and falls by at least 1 in each round, a run from a state $s$ has at most $\rho(s)$ rounds, but from $(x, y) = (2, 0)$ the run has $y' + 2$ rounds when the reset chooses $y'$, and $y'$ has no bound. With a fixed reset value $K$ instead, the single number $(K+1)x + y$ also works.
- **Forward and backward conditions.** The formulas can be built backwards with $\mathrm{wp}$, as in step 4, or forwards with the strongest postcondition. Both give equivalent conditions. Most verifiers use the backward form, because substitution is simple.
- **Assertions at every point.** An assertion can be attached to every point of the flowchart. Then each basic path is a single edge. The cut point version keeps the number of formulas small.
- **Structured programs.** In [Hoare logic](/hoare-logic/) the assertions are attached to the parts of a structured program, and the cut points are implied by the loop rule. The set of formulas is the same.
- **Guarded commands.** For the [guarded command language](/guarded-commands/), the conditions for the loop are the conditions of the loop theorem.

## Pitfalls

- *A cycle without a cut point.* Then the number of paths is infinite and the argument for step 5 breaks. Check that each cycle has a cut point.
- *An assertion that is too weak.* The condition for a path can then fail even when the program is right. In ISQRT, if $lo < hi$ is dropped from $I$, the exit path cannot show $hi = lo + 1$.
- *An assertion that is too strong.* The condition for the path into the loop then fails, because the precondition does not imply the assertion.
- *Reachable states only.* Each condition must hold for all states that satisfy the assertion and the path condition. The argument "the program never reaches this state" is not valid, unless the assertion itself excludes the state.
- *Partial correctness only.* Steps 1 to 5 do not prove that the program stops. A loop such as ISQRT with the test $hi - lo \ge 1$ keeps $I$ and does not stop. See [partial correctness](/partial-correctness/) and [total correctness](/total-correctness/).
- *A measure that does not strictly fall.* It is not enough that $\rho$ does not grow. It must be strictly smaller after each round of the loop. In a well-ordered set a strict fall is enough. If $\rho$ takes real values, require a fall of at least a fixed $\varepsilon > 0$ and a lower bound, or the values can fall for ever, as $1, 1/2, 1/4, \dots$ do.
- *Machine integers.* The conditions above are about unbounded integers. With wrapping arithmetic, an expression such as $(lo + hi)/2$ can overflow. The form $lo + \lfloor (hi - lo)/2 \rfloor$ does not overflow when $0 \le lo \le hi$, and ISQRT already uses it. In ISQRT two other expressions overflow: the start value $n + 1$ when $n$ is the largest integer, and the product $mid \cdot mid$ when $mid$ is larger than the square root of the largest integer. Require $n$ below the largest integer, and test $mid \le \lfloor n / mid \rfloor$ instead of $mid \cdot mid \le n$. For an integer $mid \ge 1$ the two tests are equivalent, and on the loop paths $mid \ge lo + 1 \ge 1$. See [integer overflow](/integer-overflow/).

## Exercises

1. Euclid's subtraction loop starts with $x, y \leftarrow X, Y$ for positive integers $X$ and $Y$, and repeats while $x \ne y$: if $x > y$ then $x \leftarrow x - y$, else $y \leftarrow y - x$. Give the assertion at the test, and the measure. *Answer:* $x > 0 \wedge y > 0 \wedge \gcd(x, y) = \gcd(X, Y)$, and $\rho = x + y$. At the exit $x = y$, so $x = \gcd(X, Y)$.
2. In ISQRT, replace the test $hi - lo > 1$ by $hi - lo \ge 1$. Which formula fails? *Answer:* the termination condition. For $g = 1$ we get $mid = lo$ and the first branch leaves $(lo, hi)$ unchanged, so $\rho$ does not fall. The partial correctness conditions still hold.
3. Write the assertion and the measure of the summing loop in the examples, for the test $i < n$ replaced by $i \ne n$, and give the precondition that you need. *Answer:* the same assertion, with $\rho = n - i$, and the precondition $n \ge 0$. For $n < 0$ the loop does not stop.
4. For the inner loop of insertion sort, $\mathbf{while}\ j \ge 0 \wedge A[j] > key\ \mathbf{do}\ A[j+1] \leftarrow A[j] ;\ j \leftarrow j - 1$, write the verification condition of the path from the inner test back to itself, with the assertion of the examples. *Answer:* assume the assertion, $j \ge 0$ and $A[j] > key$. After the path, $j' = j - 1$ and $A'[j+1] = A[j]$. Then $A'[0 \ldots j']$ is $A[0 \ldots j-1]$, and $A'[j'+2 \ldots i]$ is $A[j]$ followed by $A[j+2 \ldots i]$. That block is in order because $A[j] \le A[j+2]$ in the old sorted prefix, and each of its cells is greater than $key$ because $A[j] > key$. Also $-1 \le j' < i$.
5. Show that the loop of the lexicographic variation, with the reset $y \leftarrow$ any natural number, has no measure into $\mathbb{N}$ that falls in each round, even though every run stops. *Answer:* every run stops because $(x, y)$ falls in the well-ordered set $\mathbb{N} \times \mathbb{N}$. A measure $\rho$ into $\mathbb{N}$ that falls by at least 1 in each round bounds the number of rounds from the state $(2, 0)$ by $\rho(2, 0)$. But the run that chooses $y' = \rho(2, 0)$ has $\rho(2, 0) + 2$ rounds.

## References
