---
tag: KKZS7D
kind: definition
slug: partial-recursive-function
name: Partial recursive function
aliases:
- mu-recursive function
- general recursive function
area: complexity/computability
level: advanced
summary: "The primitive recursive functions closed under the unbounded search operator mu. The class is exactly the class of partial functions that a Turing machine computes."
prereqs: [primitive-recursive-function, computable-function]
see_also: [primitive-recursive-function, computable-function, church-turing-thesis, lambda-calculus, universal-turing-machine, s-m-n-theorem, halting-problem, register-machine]
sources:
  - paper: doi:10.1007/BF01565439
    title: "Stephen C. Kleene, General recursive functions of natural numbers, Mathematische Annalen 112 (1936)"
    locator: "pp. 727 to 742 (the operator mu, and the equivalence with the general recursive functions of Herbrand and Gödel)"
  - paper: doi:10.1090/S0002-9947-1943-0007371-8
    title: "Stephen C. Kleene, Recursive predicates and quantifiers, Transactions of the American Mathematical Society 53(1) (1943)"
    locator: "pp. 41 to 73 (the predicate T and the normal form, pp. 52 to 53)"
  - book: isbn:9780521701464
    title: "George S. Boolos, John P. Burgess and Richard C. Jeffrey, Computability and Logic, fifth edition, Cambridge University Press, 2007"
    locator: "Chapter 6, Section 6.2, Minimization, and Chapter 8, Section 8.1, Coding Turing Computations"
  - book: isbn:9780262680523
    title: "Hartley Rogers Jr., Theory of Recursive Functions and Effective Computability, MIT Press (reprint of the McGraw-Hill edition of 1967)"
    locator: Chapter 1
---

The partial recursive functions are the functions obtained from the [primitive recursive functions](/primitive-recursive-function/) by adding one more operation, the unbounded search operator $\mu$. The value $\mu y\, [g(\vec{x}, y) = 0]$ is the first $y$ at which $g$ is zero, found by trying $y = 0, 1, 2, \ldots$ in order. If the search never stops, the value is undefined, so the class contains partial functions. Kleene introduced the operator in 1936 and showed that it gives the same total functions as the general recursive functions of Herbrand and Gödel. The class is the same as the class of [computable functions](/computable-function/) defined by [Turing machines](/turing-machine/), by the [lambda calculus](/lambda-calculus/) and by [register machines](/register-machine/), and this agreement is part of the evidence for the [Church-Turing thesis](/church-turing-thesis/). Kleene's normal form theorem shows that one use of $\mu$, applied to a fixed primitive recursive predicate, is enough for every function in the class.

## Definition

Functions on this page are partial: a function $f$ with $k$ arguments maps a subset $\mathrm{dom}(f)$ of $\mathbb{N}^k$ to $\mathbb{N}$. Write $f(\vec{x})\!\downarrow$ if $\vec{x} \in \mathrm{dom}(f)$ and $f(\vec{x})\!\uparrow$ otherwise.

**The operations on partial functions.** Composition and primitive recursion are those of the [primitive recursive](/primitive-recursive-function/) page, read strictly: $f(g_1(\vec{x}), \ldots, g_m(\vec{x}))$ is defined only if every $g_i(\vec{x})$ is defined and $f$ is defined at the values, and $h(\vec{x}, y + 1)$ is defined only if $h(\vec{x}, y)$ is.

**Minimization.** From $g$ with $k + 1$ arguments, form $h(\vec{x}) = \mu y\, [g(\vec{x}, y) = 0]$, where
$$h(\vec{x}) = y \iff g(\vec{x}, y) = 0 \text{ and } g(\vec{x}, z)\!\downarrow \ne 0 \text{ for all } z < y.$$
If no such $y$ exists, $h(\vec{x})$ is undefined. The condition on all $z < y$ makes $\mu$ the result of a search: test $z = 0$, then $z = 1$, and so on, and stop at the first zero.

The *partial recursive functions* (also *$\mu$-recursive* functions) form the smallest class that contains the zero functions, the successor and the projections, and is closed under composition, primitive recursion and minimization. A partial recursive function that is total is a *recursive function*. A set is *recursive* if its characteristic function is recursive, which is the same as [decidable](/decidable-language/).

**The term "general recursive".** Herbrand and Gödel (1934) defined the *general recursive* functions as the total functions that a system of equations defines. Kleene (1936) showed that these are the total $\mu$-recursive functions, so in the original sense a general recursive function is total. Many later texts use "general recursive" for every $\mu$-recursive function, partial or total. On this page, "partial recursive" means possibly partial, and "recursive" means total.

**Kleene normal form theorem.** There are a primitive recursive predicate $T(e, x, y)$ and a primitive recursive function $U(y)$ such that, for every partial recursive unary $f$, there is a number $e$ with
$$f(x) = U(\mu y\, T(e, x, y)) \quad \text{for all } x,$$
with both sides undefined together. Here $T(e, x, y)$ says that $y$ codes a halting computation of the machine with index $e$ on input $x$, and $U(y)$ reads the output from that code. The same holds for $k$ arguments with predicates $T_k$. The function $\varphi_e(x) = U(\mu y\, T(e, x, y))$ is the $e$-th partial recursive function in a fixed computable numbering, with $W_e = \mathrm{dom}(\varphi_e)$, as on the [Gödel numbering](/godel-numbering/) page.

**Equivalence with machines.** A partial function is partial recursive if and only if a Turing machine computes it. In one direction, the basic functions and the three operations can each be carried out by a machine; minimization is a loop that tries $y = 0, 1, \ldots$. In the other direction, the normal form writes the function a machine computes as one search over codes of computations, with every other step primitive recursive.

## Examples and non-examples

**Integer square root.** $\lfloor \sqrt{x} \rfloor = \mu y\, [(y + 1)^2 > x]$, where the test is a primitive recursive predicate turned into a function that is $0$ when the test holds. The search stops for every $x$, so the function is total. It gives $0, 1, 2, 3, 3, 9, 10$ at $x = 0, 1, 8, 9, 10, 99, 100$. Here $\mu$ is not needed, since the bound $y \le x$ makes bounded minimization enough, and the function is primitive recursive.

**Subtraction as a partial function.** $f(x, y) = \mu z\, [z + y = x]$ is $x - y$ when $x \ge y$ and undefined when $x < y$. So $f(7, 3) = 4$, while the search for $f(3, 7)$ runs forever.

**A zero that the search cannot reach.** Let $g(x, 0)$ be $0$ if $\varphi_x(x)\!\downarrow$ and undefined otherwise, and let $g(x, 1) = 0$. This $g$ is partial recursive: on $(x, 0)$ it runs $\varphi_x(x)$ and returns $0$ if the run halts. Then $\mu y\, [g(x, y) = 0]$ is $0$ for $x$ in the [halting](/halting-problem/) set $K = \{ x : \varphi_x(x)\!\downarrow \}$ and undefined for $x \notin K$, even though $g(x, 1) = 0$ for every $x$. If the operator returned instead "the least $y$ with $g(x, y) = 0$, ignoring undefined values", it would give the total function that is $0$ on $K$ and $1$ off $K$, which is not computable. The condition $g(\vec{x}, z)\!\downarrow$ for all $z < y$ is what keeps the class computable.

**Functions undefined somewhere.** The everywhere undefined function $\mu y\, [S(y) = 0]$; the function $x \mapsto \mu y\, T(x, x, y)$, which is defined exactly on $K$; and the function $\varphi_e$ for any index $e$ of a machine that does not halt on all inputs.

**Total functions that need $\mu$.** The [Ackermann function](/ackermann-function/) is recursive but not primitive recursive. One way to define it with $\mu$ is to search for a code of a finite table of values of $A$ that is closed under the three defining equations and contains the wanted entry; the check of a table is primitive recursive, and the search always stops because the evaluation of $A(m, n)$ is finite.

**Non-examples.** The halting function, $1$ on $K$ and $0$ off $K$, is total but not partial recursive. The [busy beaver function](/busy-beaver-function/) grows faster than every recursive function, so it is not recursive. Both are [uncomputable functions](/uncomputable-function/).

## Related definitions

- [Primitive recursive function](/primitive-recursive-function/): the same scheme without $\mu$. Every function there is total, and the class is a proper subclass of the recursive functions.
- [Computable function](/computable-function/): the same class defined by Turing machines. The equality of the two definitions is a theorem; the claim that both capture all mechanical computation is the [Church-Turing thesis](/church-turing-thesis/).
- [Universal Turing machine](/universal-turing-machine/): the normal form gives the universal function $(e, x) \mapsto \varphi_e(x)$ as one partial recursive function.
- [s-m-n theorem](/s-m-n-theorem/) and [Kleene's recursion theorem](/kleene-recursion-theorem/): results about the indices $e$ in $\varphi_e$.
- Recursive and recursively enumerable sets: a set is recursive if its characteristic function is recursive, and recursively enumerable if it is the domain $W_e$ of a partial recursive function. In current terms these are the [decidable](/decidable-language/) and [computably enumerable](/recursively-enumerable-language/) sets.

## References
