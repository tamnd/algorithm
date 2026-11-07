---
tag: JGQ9GZ
kind: data-structure
slug: straight-line-program
name: Straight-line program
aliases: [SLP, straight-line computation, arithmetic circuit, algebraic circuit, straight-line program representation]
area: algebra/computer-algebra
level: advanced
summary: Compact sequence of arithmetic instructions that computes a polynomial or other object.
implements: [polynomial]
model: blum-shub-smale-machine
complexity:
  vars: {L: "the length (number of instructions) of the program", n: "the number of variables"}
  time: {worst: O(L)}
  space: {extra: O(L)}
prereqs: [polynomial, expression-dag]
see_also: [automatic-differentiation, horners-rule-optimality, polynomial-identity-testing, schwartz-zippel-lemma, sparse-polynomial-interpolation, straight-line-program-grammar, binary-exponentiation, sparse-polynomial]
sources:
  - book: isbn:9783540605829
    title: Peter Bürgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory, Grundlehren der mathematischen Wissenschaften 315, Springer, 1997
    locator: Chapter 4 (straight-line programs and their complexity), Chapter 7 (the Baur and Strassen theorem) and Chapter 8 (the degree bound)
  - paper: doi:10.1016/0304-3975(83)90110-X
    title: Walter Baur and Volker Strassen, The complexity of partial derivatives, Theoretical Computer Science 22(3), 1983
    locator: pp. 317 to 330 (all partial derivatives with a constant factor more operations)
  - paper: doi:10.1515/crll.1973.264.184
    title: Volker Strassen, Vermeidung von Divisionen, Journal für die reine und angewandte Mathematik 264, 1973
    locator: pp. 184 to 202 (removing divisions from a straight-line program)
  - paper: doi:10.1145/322358.322373
    title: Oscar H. Ibarra and Shlomo Moran, Probabilistic algorithms for deciding equivalence of straight-line programs, Journal of the ACM 30(1), 1983
    locator: pp. 217 to 228
  - paper: doi:10.1145/42267.45069
    title: Erich Kaltofen, Greatest common divisors of polynomials given by straight-line programs, Journal of the ACM 35(1), 1988
    locator: pp. 231 to 264 (the straight-line representation as a data structure for computer algebra)
  - paper: "Erich Kaltofen, Factorization of polynomials given by straight-line programs, in Randomness and Computation, Advances in Computing Research 5, JAI Press, 1989"
    title: Factorization of polynomials given by straight-line programs
    locator: pp. 375 to 412
  - paper: doi:10.1145/32439.32473
    title: Timothy S. Freeman, Gregory M. Imirzian and Erich Kaltofen, A system for manipulating polynomials given by straight-line programs, SYMSAC 1986
    locator: pp. 169 to 175 (the DAGWOOD system)
  - paper: doi:10.1016/S0747-7171(08)80015-6
    title: Erich Kaltofen and Barry M. Trager, Computing with polynomials given by black boxes for their evaluations, Journal of Symbolic Computation 9(3), 1990
    locator: pp. 301 to 320
---

A straight-line program is a list of arithmetic instructions without branches or loops. Each instruction adds, subtracts or multiplies two earlier results, or loads a variable or a constant. The last result is the value of the program. It is a representation of a polynomial, often much smaller than the list of its terms: $L$ instructions can compute a polynomial of degree $2^L$, or a determinant of an $n \times n$ matrix of variables, which has $n!$ terms, with $O(n^4)$ instructions and no division. Evaluation at a point costs $L$ operations, all partial derivatives cost at most $5L$, and a random evaluation tests whether the program computes zero. Expansion into terms can take exponential time, and that is the price of the compact form.

## In plain words

A straight-line program is a recipe that computes a polynomial step by step. Each step takes two earlier results and adds, subtracts or multiplies them. There are no tests and no loops, so the same steps run for every input. A short recipe can stand for a huge polynomial: squaring a number again and again gives very high powers after few steps. You can evaluate the polynomial cheaply by following the recipe, and you can find all its slopes for about five times that cost by running the recipe backwards. To check whether a recipe always gives zero, run it at a few random points. What you cannot do cheaply in general is write out all the terms, because there can be far too many.

## The abstract type

The abstract type is a polynomial $f \in R[x_1, \ldots, x_n]$ over a commutative ring $R$, often a field $K$. The operations are evaluation at a point of $R^n$, addition, subtraction, multiplication and composition of polynomials, a degree bound, the gradient at a point, a zero test, and conversion to the [sparse](/sparse-polynomial/) or dense form. With divisions allowed, the same structure represents rational functions in $K(x_1, \ldots, x_n)$; this page treats the division-free case.

## Representation

A program of length $L$ in $n$ variables is a list $\gamma_1, \ldots, \gamma_L$ of instructions. Instruction $\gamma_j$ is one of $x_i$ (load a variable), $c$ with $c \in R$ (load a constant), or $v_a \circ v_b$ with $\circ \in \{+, -, \times\}$ and $a, b < j$. The value $v_j$ is a polynomial, defined in the obvious way from earlier values, and the program computes $f = v_L$. The empty program computes $0$.

The instructions form a directed acyclic graph with one node per instruction and edges from each operand to its use. So a straight-line program is an [expression DAG](/expression-dag/) with a fixed topological order. Subexpressions are shared, which is why it is smaller than an expression tree. The *length* (or size) counts all instructions. Many authors count only the multiplications, or only the nonscalar multiplications, as in algebraic complexity theory.

In the code, instructions are tuples `("var", i)`, `("const", c)` and `(op, a, b)` in a Python list. The coefficient ring is that of the values passed in: Python integers, `Fraction` for $\mathbb{Q}$, or integers reduced modulo $p$ for $\mathbb{Z}/p\mathbb{Z}$.

## Operations

### Evaluation

```pseudo id=main
EVALUATE(γ_1..γ_L, ξ ∈ R^n)                ▷ value of the program at the point ξ
L1  v ← an empty array of length L
L2  for j ← 1 to L
L3    v_j ← ξ_i if γ_j is x_i; c if γ_j is c; v_a ∘ v_b if γ_j is v_a ∘ v_b
L4    over Z/pZ: reduce v_j modulo p; store v_j
L5  return v_L, or 0 if L = 0
```

One operation in $R$ per arithmetic instruction, so at most $L$ operations and $L$ stored values. Over $\mathbb{Z}$ the numbers can have about $2^L$ binary digits, so for large programs one evaluates modulo a prime.

### Gradient by the reverse mode

```pseudo id=grad
GRADIENT(γ_1..γ_L, ξ)                       ▷ ∂f/∂x_i at ξ for all i
G1  compute v_1..v_L by EVALUATE
G2  w_j ← 0 for all j; g_i ← 0 for all i; if L = 0: return g
G3  w_L ← 1                                 ▷ w_j = ∂f/∂v_j
G4  for j ← L down to 1
G5    if γ_j is x_i: g_i ← g_i + w_j
G6    if γ_j is v_a ± v_b: w_a ← w_a + w_j; w_b ← w_b ± w_j
G7    if γ_j is v_a × v_b: w_a ← w_a + w_j v_b; w_b ← w_b + w_j v_a
G8  return g
```

This is the reverse mode of [automatic differentiation](/automatic-differentiation/). The backward pass uses at most $4$ operations for each instruction (two products and two sums for a product), so the whole gradient costs at most $5L$ operations. Baur and Strassen (1983) proved that in this way all $n$ partial derivatives cost only a constant factor more than $f$ itself. A forward pass for each variable separately would cost $nL$.

### Other operations

- **Sum, difference and product of two programs.** Concatenate them, shift the indices of the second, and add one instruction. Length $L_1 + L_2 + 1$.
- **Composition** $f(g_1, \ldots, g_m)$. Concatenate the programs for the $g_i$ and replace each load of $x_i$ in the program for $f$ by the index of the result of $g_i$. Length at most $L_f + \sum L_{g_i} + 2$ in the code.
- **Degree bound.** Propagate $\deg(v_a \pm v_b) \le \max$ and $\deg(v_a v_b) \le \deg v_a + \deg v_b$, with $-1$ for the zero constant. $O(L)$ integer operations. The bound can be larger than the true degree because of cancellation, and it can reach $2^L$.
- **Zero test.** Evaluate at random points of $(\mathbb{Z}/p\mathbb{Z})^n$. If $f \ne 0$ has degree at most $D < p$, by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) one point gives $0$ with probability at most $D / p$. A zero program is always reported as zero. Over $\mathbb{Z}$, Ibarra and Moran (1983) evaluate at random points modulo random primes. No deterministic polynomial-time test is known; this is the [polynomial identity testing](/polynomial-identity-testing/) problem.
- **Expansion.** Expand each value into a sparse polynomial. The cost is polynomial in $L$ and in the number of terms of the intermediate values, which can be exponential in $L$. The code stops with an error when a value exceeds a set number of terms. For sparse $f$, [sparse interpolation](/sparse-polynomial-interpolation/) from evaluations of the program is often faster, since it does not expand the intermediate values.

## Example

Take $f = (x + y)^4 - x y$ in $\mathbb{Z}[x, y]$, with the program

| $j$ | $\gamma_j$ | value | degree bound | $v_j$ at $(2, 3)$ |
|---|---|---|---|---|
| 1 | $x$ | $x$ | 1 | 2 |
| 2 | $y$ | $y$ | 1 | 3 |
| 3 | $v_1 + v_2$ | $x + y$ | 1 | 5 |
| 4 | $v_3 \times v_3$ | $(x + y)^2$ | 2 | 25 |
| 5 | $v_4 \times v_4$ | $(x + y)^4$ | 4 | 625 |
| 6 | $v_1 \times v_2$ | $x y$ | 2 | 6 |
| 7 | $v_5 - v_6$ | $f$ | 4 | 619 |

The expansion $x^4 + 4x^3 y + 6x^2 y^2 + 4 x y^3 + y^4 - x y$ has $6$ terms. With $(x + y)^{2^k}$ in place of $(x + y)^4$ the program has $k + 5$ instructions and the expansion has $2^k + 2$ terms.

The reverse pass at $(2, 3)$ starts with $w_7 = 1$. Instruction 7 gives $w_5 = 1$ and $w_6 = -1$. Instruction 6 adds $-1 \cdot 3$ to $g_x$ and $-1 \cdot 2$ to $g_y$. Instruction 5 gives $w_4 = 1 \cdot 25 + 1 \cdot 25 = 50$, and instruction 4 gives $w_3 = 2 \cdot 50 \cdot 5 = 500$. Instruction 3 adds $500$ to $w_1$ and to $w_2$, which then pass to $g_x$ and $g_y$. So $\nabla f(2, 3) = (497, 498)$, which agrees with $\partial f / \partial x = 4(x + y)^3 - y = 500 - 3$ and $\partial f / \partial y = 4(x + y)^3 - x = 500 - 2$.

## Correctness

Evaluation is correct by induction on $j$: the evaluation map $R[x_1, \ldots, x_n] \to R$ at $\xi$ is a ring homomorphism, so the value of $v_a \circ v_b$ at $\xi$ is $v_a(\xi) \circ v_b(\xi)$. Reduction modulo $p$ is also a ring homomorphism, so reducing after each step gives $f(\xi) \bmod p$.

For the gradient, regard $f$ as a function of the values $v_j$, and let $w_j$ be the total derivative of $f$ with respect to $v_j$, through all later instructions that use it. By the chain rule, $w_j = \sum_{k} w_k \, \partial \gamma_k / \partial v_j$, summed over the instructions $k > j$ that use $v_j$. The backward loop adds these contributions in decreasing order of $k$, so $w_j$ is complete when $j$ is reached. The partial derivatives are $1$ and $\pm 1$ for sums and differences and $v_b, v_a$ for a product (both contributions when $a = b$, giving $2 v_a$). The derivative with respect to $x_i$ is the sum of $w_j$ over the loads of $x_i$. All rules are polynomial identities, so the method is correct over any commutative ring, not only over the reals.

The degree bound is correct because $\deg(g \pm h) \le \max(\deg g, \deg h)$ and $\deg(g h) \le \deg g + \deg h$ over any ring. The zero test is correct for zero programs by the evaluation argument, and for nonzero programs it errs with the probability given by the Schwartz-Zippel lemma.

## Complexity

All costs are in operations of the coefficient ring and are proved.

| operation | cost |
|---|---|
| evaluate | $\le L$ ring operations, $L$ stored values |
| gradient (reverse mode) | $\le 5L$ ring operations, $L$ stored values |
| degree bound | $O(L)$ integer operations |
| sum, product, composition | $O(L_1 + L_2)$ to copy the instructions |
| zero test, $s$ points | $s L$ operations in $\mathbb{Z}/p\mathbb{Z}$, error at most $(D / p)^s$ |
| expansion | polynomial in $L$ and in the number of terms of all $v_j$; exponential in $L$ in the worst case |

Over $\mathbb{Z}$ the values can grow to about $2^L$ binary digits, as in $2^{2^L}$ by repeated squaring of $2$, so exact evaluation is not polynomial in $L$ in the bit model. Modular evaluation keeps each operation at the size of $p$. The Baur and Strassen bound is tight up to the constant: computing all partials takes at least as long as computing $f$, up to the constant, so lower bounds for the gradient give lower bounds for $f$. Strassen's degree bound uses this to show that $x_1^d + \cdots + x_n^d$ needs $\Omega(n \log d)$ multiplications.

## Variants

- **Programs with division.** Allow $v_a / v_b$ to represent rational functions. Strassen (1973) showed that divisions can be removed from a program for a polynomial of degree $d$ with a cost factor polynomial in $d$, by computing in power series around a point where no denominator vanishes.
- **Nonscalar cost.** In algebraic complexity theory, additions and multiplications by constants are free, and only products of two nonconstant values count. [Horner's rule](/horners-rule-optimality/) is optimal for a polynomial of one variable with generic coefficients (Ostrowski for small degrees, Pan in general).
- **Black boxes.** Kaltofen and Trager (1990) replace the program by any procedure that evaluates $f$. Most algorithms for programs, such as GCD, factorization and sparse interpolation, need only evaluations and work for black boxes too.
- **Arithmetic circuits and formulas.** An arithmetic circuit is the same object seen as a graph. A formula is a circuit whose graph is a tree, so subresults are not shared. Valiant's classes VP and VNP are defined with circuits of polynomial size and degree.
- **Programs over words.** A [straight-line grammar](/straight-line-program-grammar/) uses concatenation instead of arithmetic and represents compressed strings in the same way.

## When to use it

Use a straight-line program when the polynomial is the result of a computation and its expanded form would be large, for example a determinant or resultant with symbolic entries, a high power, or a function evaluated many times in numerical code. It is the natural input for [sparse interpolation](/sparse-polynomial-interpolation/), for randomized identity tests and for Kaltofen's GCD and factorization algorithms, which return their answers again as programs. Use the [sparse representation](/sparse-polynomial/) when you need the terms themselves, need equality tests that are exact and deterministic, or need a normal form, for example in Gröbner basis computations.

## Pitfalls

- **No normal form.** Two different programs can compute the same polynomial. Deciding equality needs a zero test of the difference, which is randomized.
- **Degree bounds are not degrees.** Cancellation can make the true degree much smaller than the propagated bound. A small prime with $p \le D$ makes the Schwartz-Zippel bound useless.
- **Coefficient growth over Z.** Exact integer evaluation of a program of length $L$ can produce numbers with about $2^L$ digits. Evaluate modulo primes.
- **Expansion blowup.** Converting to the sparse form can take exponential time and space even when the result is small, because intermediate values can be large. Set a size limit, as the code does, or interpolate instead.
- **Counting conventions.** Lengths in papers count different things: all instructions, only multiplications, or only nonscalar multiplications. State which one you mean.

## Implementations

## History

Straight-line programs come from algebraic complexity theory. Ostrowski (1954) asked whether Horner's rule is optimal, and Pan (1966) proved that it is for generic coefficients. Strassen (1973) showed how to remove divisions, and proved the degree bound for lower bounds the same year. Baur and Strassen (1983) proved that all partial derivatives cost only a constant factor more than the function. Ibarra and Moran (1983) gave probabilistic equivalence tests. In computer algebra, Kaltofen made the program a data structure: his GCD algorithm for straight-line programs (Journal of the ACM 1988) and his factorization algorithm (1989) take and return programs in time polynomial in the length and the degree. Freeman, Imirzian and Kaltofen (1986) built the DAGWOOD system on this idea. Kaltofen and Trager (1990) generalized it to black boxes.

## References
