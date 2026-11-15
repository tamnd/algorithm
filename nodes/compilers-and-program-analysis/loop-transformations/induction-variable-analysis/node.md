---
tag: TMQVV2
kind: problem
slug: induction-variable-analysis
name: Induction variable analysis
aliases:
- induction variable detection
area: compilers-and-program-analysis/loop-transformations
level: core
summary: Find the variables of a loop that change by a fixed amount each iteration, or are affine in such variables.
prereqs: [natural-loop, static-single-assignment-form, phi-function]
see_also: [chains-of-recurrences, strength-reduction, operator-strength-reduction, tarjan-scc, dependence-testing, loop-invariant-code-motion, integer-overflow, rice-theorem]
sources:
  - paper: "Michael P. Gerlek, Eric Stoltz and Michael Wolfe, Beyond induction variables: detecting and classifying sequences using a demand-driven SSA form, ACM Transactions on Programming Languages and Systems 17(1), 1995"
    locator: the strongly connected regions of the SSA graph, and the classes of linear, polynomial, geometric, wrap-around, periodic and monotonic sequences
  - paper: "Keith D. Cooper, L. Taylor Simpson and Christopher A. Vick, Operator strength reduction, ACM Transactions on Programming Languages and Systems 23(5), 2001"
    locator: the detection of induction variables as strongly connected components of the SSA graph, found with Tarjan's algorithm, and their use for strength reduction
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Chapter 9 (induction variables and reduction in strength among the machine-independent optimizations)
  - book: isbn:9781558602861
    title: Randy Allen and Ken Kennedy, Optimizing Compilers for Modern Architectures, a Dependence-Based Approach, Morgan Kaufmann, 2002 (copyright 2001)
    locator: Chapter 4 (preliminary transformations, induction-variable substitution so that subscripts become affine in the loop indices)
  - book: isbn:1558603204
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: the chapter on loop optimizations (identifying basic and dependent induction variables, strength reduction and linear-function test replacement)
---

## In plain words

Inside a loop, some variables move in a regular way: a counter goes up by one each time, a pointer moves by the size of an element, an address is "four times the counter plus eight". Induction variable analysis finds these variables and writes down how each one depends on the number of the current iteration. With that, a compiler can replace a multiplication by a cheaper addition, remove variables that only shadow the counter, compute how many times the loop runs, and turn array accesses into the simple form that dependence tests need. Some variables move in less regular ways, by a growing step or by doubling, or they take turns between two values, and good analyses recognize these too. A variable that changes only under a condition, or that overflows, needs care.

## Definition

Let $L$ be a loop (a [natural loop](/natural-loop/)) with header $h$, in [SSA form](/static-single-assignment-form/). Number the visits of the header $n = 0, 1, 2, \dots$: visit $n$ is the start of iteration $n$. A name $v$ defined in $L$ has the value $v(n)$ in iteration $n$ (for a name defined in the body, the value it gets in that iteration). An expression is **loop invariant** if its value does not change during the execution of the loop.

- A **basic induction variable** is a name $v$ defined by a [φ-function](/phi-function/) at the header, $v = \varphi(v_{init}, v_{next})$, where every path around the loop computes $v_{next} = v + s$ for one loop invariant $s$, the **step**. Then $v(n) = v_{init} + n s$.
- A **derived induction variable** (also *dependent* induction variable) is a name $w$ with $w(n) = a \cdot v(n) + b$ for a basic induction variable $v$ and loop invariant $a$, $b$. Then $w(n) = (a v_{init} + b) + n \cdot a s$.
- An **induction variable** is a basic or derived one: a name whose value is an affine function $\alpha + n \beta$ of the iteration number with loop invariant $\alpha$ and $\beta$.

**The problem.** Given the loop, find every induction variable and its closed form $\alpha + n\beta$, as an expression in loop-invariant values. The extended problem also finds names whose values follow other closed forms of $n$ (see Variants).

Before SSA, the classic definition is: $v$ is a basic induction variable if its only assignments in the loop have the form $v = v \pm s$ with loop-invariant $s$, and the analysis finds *families* of derived variables of the form $a \cdot v + b$ that belong to each basic variable.

## Variants

**Classes of sequences.** Gerlek, Stoltz and Wolfe classify the names of a loop by the sequence $v(0), v(1), \dots$:

| class | closed form or behavior | typical source |
|---|---|---|
| linear | $\alpha + \beta n$ | `i = i + 1`, `p = p + 4` |
| polynomial | a polynomial in $n$ of degree $d \ge 2$ | `j = j + i` with $i$ linear |
| geometric | $\alpha \cdot r^n$, or $\alpha r^n$ plus a polynomial | `k = 2 * k` |
| wrap-around | one special first value, then an induction variable shifted by one iteration | `w = i` at the end of the body, used at the top |
| periodic | repeats with a fixed period | `f = 1 - f`, `t = a; a = b; b = t` |
| monotonic | only known to grow (or fall) | `if (c) x = x + 1` |

Linear, polynomial and geometric sequences have closed forms, which [chains of recurrences](/chains-of-recurrences/) compute; LLVM's scalar evolution analysis represents them in that form.

**Unknown or symbolic steps.** The step can be a loop-invariant name, such as $s$ in `i = i + s`; the closed form is then symbolic, and it matters whether $s$ is positive.

**Machine integers.** On $w$-bit integers, `i = i + 1` wraps around at $2^w$. The closed form is then $\alpha + n\beta \bmod 2^w$ (or undefined behavior for signed overflow in C), and many uses of the closed form, such as trip counts and dependence tests, need a proof that no wrap happens.

**Trip count.** A related question asks for the number of iterations, the least $n$ for which the exit test fails, from the closed form of the variable in the test.

## Examples

### A loop in SSA form

```
B0:  i0 = 0;  j0 = 5;  k0 = 1;  w0 = 99;  f0 = 0
B1:  i1 = φ(i0, i2)
     j1 = φ(j0, j2)
     k1 = φ(k0, k2)
     w1 = φ(w0, i1)
     f1 = φ(f0, f2)
     t  = 4 * i1 + 8
     A[t] = j1 + k1 + w1 + f1
     j2 = j1 + i1
     k2 = 2 * k1
     f2 = 1 - f1
     i2 = i1 + 1
     if i2 < N goto B1
```

The values at the start of iteration $n$:

| name | class | closed form | $n = 0, 1, 2, 3, 4$ |
|---|---|---|---|
| `i1` | basic, step 1 | $n$ | $0, 1, 2, 3, 4$ |
| `t` | derived from `i1` | $4n + 8$ | $8, 12, 16, 20, 24$ |
| `j1` | polynomial | $5 + n(n-1)/2$ | $5, 5, 6, 8, 11$ |
| `k1` | geometric | $2^n$ | $1, 2, 4, 8, 16$ |
| `w1` | wrap-around | $99$ for $n = 0$, then $n - 1$ | $99, 0, 1, 2, 3$ |
| `f1` | periodic, period 2 | $n \bmod 2$ | $0, 1, 0, 1, 0$ |

The cycle of `i1` in the SSA graph is `i1 → i2 → i1`, with one addition of the constant 1. The cycle of `j1` adds `i1`, which is not loop invariant, so `j1` is not linear; its increments are the linear sequence $0, 1, 2, \dots$, so `j1` is a polynomial of degree 2. The name `w1` takes `i1` around the back edge, so it holds the value of `i1` from the previous iteration. A simple pass that only looks for `v = v + c` finds `i1` and `t` and treats the other four as unknown.

### Strength reduction

The derived variable `t` is $4n + 8$, so it can be computed as its own basic variable, `t1 = φ(8, t2)` and `t2 = t1 + 4`, which replaces a multiplication by an addition ([strength reduction](/strength-reduction/)). If `i1` has no other use than the exit test, the test `i2 < N` can be rewritten as `t2 < 4*N + 8`, and `i` disappears (linear-function test replacement), provided $4N + 8$ does not overflow.

### Non-examples

- `if (A[i] > 0) c = c + 1`: the step depends on the data. `c` is monotonic, not linear, and has no closed form.
- `x = x + y` where `y` is changed in the loop by a non-inductive assignment: not an induction variable.
- `i = i + 1` on an 8-bit unsigned integer starting at 250 with step 3: the values are $250, 253, 0, 3, \dots$; the closed form $250 + 3n$ holds only modulo 256.

## Known algorithms

- **Classic dataflow detection.** With reaching definitions and loop-invariance information, find the names whose only definitions in the loop are `v = v ± s`, then grow families of derived variables `a*v + b` one assignment at a time. This is the method of the dragon book and of early optimizing compilers.
- **SCCs of the SSA graph.** In SSA form, a basic induction variable is a [strongly connected component](/strongly-connected-components/) of the def-use graph of the loop that contains one header φ and otherwise only additions and subtractions of loop-invariant values. [Tarjan's algorithm](/tarjan-scc/) finds the components in one pass, in an order where each component comes after the components it uses, so derived variables can be classified in the same pass. Cooper, Simpson and Vick use this for [operator strength reduction](/operator-strength-reduction/).
- **Classification of sequences.** Gerlek, Stoltz and Wolfe extend the SCC method to the classes above: a component whose increments are themselves linear gives a polynomial, a multiplication on the cycle gives a geometric sequence, a φ whose back-edge argument is an induction variable gives a wrap-around sequence, and a cycle of φ-functions gives a periodic one.
- **Chains of recurrences.** Represent each name by a [chain of recurrences](/chains-of-recurrences/) such as $\{0, +, 1\}$ for `i1`, and compute with the rules of the algebra: $4 \cdot \{0, +, 1\} + 8 = \{8, +, 4\}$, $\{5, +, \{0, +, 1\}\} = \{5, +, 0, +, 1\}$. The closed form follows from the chain. LLVM's scalar evolution works this way.
- **Abstract interpretation.** A numeric [abstract interpretation](/abstract-interpretation/) with relational domains finds affine relations between variables, including ones that the syntactic methods miss, at a higher cost.

## Bounds

**Linear time for the syntactic problem.** Over the SSA graph of a loop with $V$ names and $E$ def-use edges, the SCC method runs in $O(V + E)$ time: Tarjan's algorithm is linear, and classifying a component reads each of its operations once. The classic dataflow method needs reaching definitions first, which costs more in the worst case.

**The semantic problem is undecidable.** Whether the values of a name form an affine sequence is a property of what the program computes, so by [Rice's theorem](/rice-theorem/) no algorithm decides it for all loops. A direct reduction from the halting problem: given a program $P$, build the loop whose iteration $n$ simulates one more step of $P$ and then runs `v = v + 1`, plus one more `v = v + 1` in the iteration in which $P$ halts. If $P$ never halts, $v(n) = n$, an induction variable. If $P$ halts in step $s$, then $v(n) = n$ up to step $s$ and $n + 1$ after it, which is not affine. So every practical analysis is conservative: it recognizes sufficient syntactic patterns, and treats every other name as unknown.

## Reductions

- **To strongly connected components.** Basic induction variables are SCCs of the SSA def-use graph with a special shape ([Tarjan](/tarjan-scc/)).
- **To recurrence solving.** A name defined by a cycle with additions and multiplications is a linear recurrence in $n$. [Chains of recurrences](/chains-of-recurrences/) give the closed forms for the classes that have one.
- **Dependence testing needs it.** A subscript `A[k]` where `k = k + 2` is not affine in the loop index as written; replacing `k` by its closed form $k_0 + 2n$ (induction-variable substitution) makes it affine, and the [dependence tests](/dependence-testing/) apply.

## Applications

- **[Strength reduction](/strength-reduction/)** of multiplications in derived variables, mainly address computations, and its SSA version, [operator strength reduction](/operator-strength-reduction/).
- **Induction variable elimination** and linear-function test replacement, which remove counters that are only used to control the loop.
- **Induction variable substitution** before dependence analysis, so that subscripts become affine functions of the loop indices, and loop normalization.
- **Trip counts** for loop unrolling, vectorization and loop-invariant code motion with known iteration counts ([loop-invariant code motion](/loop-invariant-code-motion/), [vectorization](/vectorization/)).
- **Bounds check elimination**: a check `0 <= i < len` on a linear `i` can be moved out of the loop and tested once at the ends of the range.

## References
