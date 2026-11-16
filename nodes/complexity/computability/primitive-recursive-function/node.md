---
tag: DEKSBB
kind: definition
slug: primitive-recursive-function
name: Primitive recursive function
aliases:
- primitive recursive
area: complexity/computability
level: core
summary: "A function on the natural numbers built from zero, successor and projections by composition and primitive recursion. All are total and computable, but some total computable functions are not."
prereqs: [computable-function, structural-induction]
see_also: [partial-recursive-function, ackermann-function, computable-function, register-machine, godel-numbering, diagonalization-argument, universal-turing-machine, kleene-recursion-theorem]
sources:
  - paper: doi:10.1007/BF01565439
    title: "Stephen C. Kleene, General recursive functions of natural numbers, Mathematische Annalen 112 (1936)"
    locator: "pp. 727 to 742 (the name primitive recursive, and the normal form)"
  - paper: doi:10.1007/BF01700692
    title: "Kurt Gödel, Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I, Monatshefte für Mathematik und Physik 38 (1931)"
    locator: "pp. 173 to 198, Section 2 (the class of functions that Gödel calls recursive, now called primitive recursive)"
  - paper: doi:10.1007/BF01459088
    title: "Wilhelm Ackermann, Zum Hilbertschen Aufbau der reellen Zahlen, Mathematische Annalen 99 (1928)"
    locator: "pp. 118 to 133 (a computable function that is not primitive recursive)"
  - paper: doi:10.1145/800196.806014
    title: "Albert R. Meyer and Dennis M. Ritchie, The complexity of loop programs, Proceedings of the 22nd ACM National Conference (1967)"
    locator: pp. 465 to 469
  - book: isbn:9780521701464
    title: "George S. Boolos, John P. Burgess and Richard C. Jeffrey, Computability and Logic, fifth edition, Cambridge University Press, 2007"
    locator: "Chapter 6, Recursive Functions, Section 6.1, Primitive Recursive Functions"
  - book: isbn:9780262680523
    title: "Hartley Rogers Jr., Theory of Recursive Functions and Effective Computability, MIT Press (reprint of the McGraw-Hill edition of 1967)"
    locator: Chapter 1
---

A primitive recursive function is a function from tuples of natural numbers to natural numbers that is built from three kinds of basic functions (zero, successor and projections) by two operations: composition and primitive recursion. Primitive recursion defines $h(x, y+1)$ from $h(x, y)$, so the number of steps is known before the computation starts. For this reason every primitive recursive function is total, and it can be computed by a program whose only loops are `for` loops with a bound fixed on entry. Almost every function met in practice (addition, multiplication, powers, the $n$-th prime, the coding of sequences and the step function of a [Turing machine](/turing-machine/)) is primitive recursive. The class is still smaller than the class of total [computable functions](/computable-function/): Ackermann gave a total computable function that grows too fast to be primitive recursive. Gödel used the class in 1931 under the name "recursive", and Kleene gave it the name "primitive recursive" in 1936.

## Definition

All functions on this page take $k \ge 0$ arguments from $\mathbb{N} = \{0, 1, 2, \ldots\}$ and return a value in $\mathbb{N}$. Write $\vec{x}$ for $x_1, \ldots, x_k$.

**Basic functions.**

- The *zero functions* $Z_k(\vec{x}) = 0$, for each $k \ge 0$. $Z_0$ is the constant $0$.
- The *successor* $S(x) = x + 1$.
- The *projections* $P^k_i(x_1, \ldots, x_k) = x_i$, for $1 \le i \le k$.

**Composition.** From $f$ with $m$ arguments and $g_1, \ldots, g_m$ with $k$ arguments each, form
$$h(\vec{x}) = f(g_1(\vec{x}), \ldots, g_m(\vec{x})).$$

**Primitive recursion.** From $f$ with $k$ arguments and $g$ with $k + 2$ arguments, form the function $h$ with $k + 1$ arguments given by
$$h(\vec{x}, 0) = f(\vec{x}), \qquad h(\vec{x}, y + 1) = g(\vec{x}, y, h(\vec{x}, y)).$$

The *primitive recursive functions* form the smallest class that contains the basic functions and is closed under composition and primitive recursion. Equivalently, $h$ is primitive recursive if it has a *derivation*: a finite list of functions, each of which is basic or comes from earlier entries by one of the two operations, with $h$ as the last entry.

A set $A \subseteq \mathbb{N}^k$ (a relation) is primitive recursive if its characteristic function, with value $1$ on $A$ and $0$ off $A$, is primitive recursive.

**Totality.** Each primitive recursive function is defined on every input. The proof is by [structural induction](/structural-induction/) on the derivation: the basic functions are total, a composition of total functions is total, and if $f$ and $g$ are total, then $h(\vec{x}, y)$ is defined for every $y$ by ordinary induction on $y$.

**Closure properties.** The class is also closed under these operations, each of which can be written with the two operations above:

- definition by cases with primitive recursive conditions;
- bounded sums $\sum_{z < y} f(\vec{x}, z)$ and bounded products $\prod_{z < y} f(\vec{x}, z)$;
- bounded quantifiers $\exists z < y\, R(\vec{x}, z)$ and $\forall z < y\, R(\vec{x}, z)$, for a primitive recursive relation $R$;
- bounded minimization $\mu z < y\, [R(\vec{x}, z)]$, the least $z < y$ with $R(\vec{x}, z)$, and $y$ if there is none;
- course-of-values recursion, where $h(\vec{x}, y + 1)$ may use all earlier values $h(\vec{x}, 0), \ldots, h(\vec{x}, y)$.

The bound $y$ is what keeps these operations inside the class. Bounded minimization becomes the unbounded operator $\mu$ of the [partial recursive functions](/partial-recursive-function/) when the bound is removed.

**Programs with bounded loops.** Meyer and Ritchie (1967) defined LOOP programs: programs over natural-number [registers](/register-machine/) with the statements $x := 0$, $x := x + 1$, $x := y$ and `loop x do ... end`, which runs its body a number of times equal to the value of $x$ on entry. A function is primitive recursive if and only if a LOOP program computes it. The `loop` statement is primitive recursion, and a `while` loop, whose number of rounds is not known on entry, is what LOOP programs lack.

**Time bounds.** A function is primitive recursive if and only if some Turing machine computes it within a number of steps that is bounded by a primitive recursive function of the input. One direction holds because the step function of a machine is primitive recursive, so running it for $t(\vec{x})$ steps is a primitive recursion on the step count. The other direction holds because a derivation can be compiled into a machine whose running time is bounded by a function with a derivation of the same shape.

## Examples and non-examples

**Arithmetic.** These definitions follow the scheme exactly, with the recursion on the last argument.

- Addition: $\mathrm{add}(x, 0) = x$, $\mathrm{add}(x, y + 1) = S(\mathrm{add}(x, y))$. Here $f = P^1_1$ and $g = S \circ P^3_3$.
- Multiplication: $\mathrm{mult}(x, 0) = 0$, $\mathrm{mult}(x, y + 1) = \mathrm{add}(\mathrm{mult}(x, y), x)$.
- Power: $x^0 = 1$, $x^{y+1} = \mathrm{mult}(x^y, x)$.
- Predecessor: $\mathrm{pred}(0) = 0$, $\mathrm{pred}(y + 1) = y$.
- Truncated subtraction (monus): $x \mathbin{\dot{-}} 0 = x$, $x \mathbin{\dot{-}} (y + 1) = \mathrm{pred}(x \mathbin{\dot{-}} y)$. It gives $7 \mathbin{\dot{-}} 3 = 4$ and $3 \mathbin{\dot{-}} 7 = 0$, because the class has no negative numbers.

From monus come $|x - y| = (x \mathbin{\dot{-}} y) + (y \mathbin{\dot{-}} x)$, the relations $x = y$ and $x < y$, and with bounded quantifiers the relations "$d$ divides $x$" and "$x$ is prime".

**A worked derivation.** Evaluate $\mathrm{add}(3, 4)$. The recursion gives $\mathrm{add}(3, 0) = P^1_1(3) = 3$, and then each step applies $g(x, y, r) = S(P^3_3(x, y, r))$, so the values for $y = 0, 1, 2, 3, 4$ are $3, 4, 5, 6, 7$. The run uses 4 successor calls and 5 projection calls. With the derivations above, $\mathrm{mult}(3, 4) = 12$ uses 37 calls of basic functions and $2^5 = 32$ uses 171. The count grows with the values, because the class has only the successor to build numbers; the class is about what can be defined, not about speed.

**Number theory and coding.** The $n$-th prime $p_n$ is primitive recursive: $p_0 = 2$, and $p_{n+1}$ is the least prime above $p_n$, found by bounded minimization below the bound $p_n! + 1$, since some prime factor of $p_n! + 1$ is larger than $p_n$. The first ten values are $2, 3, 5, 7, 11, 13, 17, 19, 23, 29$. The Cantor pairing $\pi(x, y) = (x + y)(x + y + 1)/2 + y$ is primitive recursive, with $\pi(3, 4) = 32$ and $\pi(4, 3) = 31$, and so are its two inverses, by bounded minimization. Pairing and prime-power codes let one number stand for a finite sequence, so functions on lists, strings and machine configurations become functions on $\mathbb{N}$, as in the [Gödel numbering](/godel-numbering/).

**The machinery of computation.** For a fixed coding of Turing machines, the following are primitive recursive: the function that maps a configuration to the next one, the function that runs a machine for $t$ steps, and Kleene's predicate $T(e, x, y)$, which says that $y$ codes a halting computation of the machine with index $e$ on input $x$. Only the search for such a $y$, with no bound, leaves the class. This is the content of the Kleene normal form on the [partial recursive function](/partial-recursive-function/) page.

**Non-example: the Ackermann function.** The [Ackermann function](/ackermann-function/) in the two-argument form of Péter and Robinson is
$$A(0, n) = n + 1, \quad A(m + 1, 0) = A(m, 1), \quad A(m + 1, n + 1) = A(m, A(m + 1, n)).$$
It is total and computable, with $A(1, 3) = 5$, $A(2, 3) = 9$, $A(3, 3) = 61$ and $A(3, 5) = 253$. For every primitive recursive $f$ there is an $m$ with $f(\vec{x}) < A(m, \max \vec{x})$ for all $\vec{x}$, proved by induction on the derivation of $f$. So the diagonal $n \mapsto A(n, n)$ is not primitive recursive. Its first values are $1, 3, 7, 61$, and $A(4, 4)$ is far too large to write in decimal. The recursion on $m$ is a double recursion: the inner call $A(m + 1, n)$ is used as an argument, so no bound on the number of steps can be fixed in advance by a single primitive recursion.

**Non-example: the diagonal function.** Derivations are finite strings, so they can be listed as $f_0, f_1, f_2, \ldots$ (the unary ones) by a computable enumeration, and $f_n(x)$ is computable from $n$ and $x$. The function $d(n) = f_n(n) + 1$ is total and computable, but differs from each $f_n$ at the input $n$, so it is not primitive recursive. This is a [diagonalization argument](/diagonalization-argument/). It shows more: the *evaluation function* $(n, x) \mapsto f_n(x)$ is total computable but not primitive recursive, so the class has no universal function inside itself. Any class of total functions with a computable list of programs has the same gap, which is why the full class of [computable functions](/computable-function/) must contain partial functions.

**Non-example: partial functions.** The function that is undefined at every input is computable but not primitive recursive, since primitive recursive functions are total. So are the functions defined by an unbounded search, such as $x \mapsto \mu y\, [\varphi_x(x) \text{ halts within } y \text{ steps}]$, which is undefined off the [halting](/halting-problem/) set $K$.

## Related definitions

- [Partial recursive function](/partial-recursive-function/): adds the unbounded $\mu$ operator. The class equals the class of [computable functions](/computable-function/).
- [Ackermann function](/ackermann-function/): the standard total computable function that is not primitive recursive.
- [Register machine](/register-machine/): with `while` loops the model computes every computable function; with only bounded `loop` statements it computes exactly the primitive recursive functions.
- Grzegorczyk hierarchy: a division of the primitive recursive functions into levels $\mathcal{E}^0 \subset \mathcal{E}^1 \subset \cdots$ by growth rate; the elementary functions form $\mathcal{E}^3$. Meyer and Ritchie related these levels to the depth to which `loop` statements are nested.
- Primitive recursive arithmetic: the logical theory whose terms are the primitive recursive functions, often taken as the formal form of finitist reasoning.

## References
