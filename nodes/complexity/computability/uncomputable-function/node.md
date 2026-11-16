---
tag: XA8JAZ
kind: concept
slug: uncomputable-function
name: Uncomputable function
aliases:
- non-computable function
area: complexity/computability
level: core
summary: A function on the natural numbers that no Turing machine computes. Almost all functions are uncomputable; the halting function and the busy beaver function are explicit examples.
prereqs: [computable-function, halting-problem, countability]
see_also: [computable-function, partial-recursive-function, halting-problem, busy-beaver-function, kolmogorov-complexity, diagonalization-argument, turing-degrees, arithmetical-hierarchy]
sources:
  - paper: doi:10.1112/plms/s2-42.1.230
    title: Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society (2) 42 (1936)
    locator: pp. 230 to 265, Section 8, Application of the diagonal process
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 4.2, Undecidability (the diagonalization method and the existence of languages that are not Turing-recognizable)
  - paper: doi:10.1002/j.1538-7305.1962.tb00480.x
    title: Tibor Rado, On non-computable functions, Bell System Technical Journal 41(3) (1962)
    locator: pp. 877 to 884
  - title: Joseph R. Shoenfield, On degrees of unsolvability, Annals of Mathematics (2) 69 (1959)
    locator: pp. 644 to 653 (the limit lemma)
  - book: isbn:9783642319327
    title: Robert I. Soare, Turing Computability, Theory and Applications, Springer, 2016
    locator: Chapter 1, Defining Computability; Chapter 3, Turing Reducibility
---

An uncomputable function is a function on the natural numbers, or on finite words, that no [Turing machine](/turing-machine/) computes. A *total* function $f$ is uncomputable if no machine halts on every input $n$ with output $f(n)$. A *partial* function is uncomputable if no machine halts exactly on its domain with the right outputs. By the [Church-Turing thesis](/church-turing-thesis/), no algorithm in any programming language computes such a function. Counting shows that almost every function is uncomputable, because there are only countably many machines. The interesting examples are explicit ones: the characteristic function of the [halting problem](/halting-problem/), the [busy beaver function](/busy-beaver-function/) and [Kolmogorov complexity](/kolmogorov-complexity/). The opposite notion is a [computable function](/computable-function/), and the partial computable functions are the [partial recursive functions](/partial-recursive-function/).

## In plain words

A function is uncomputable when no program can produce its values for all inputs. This is not a matter of speed or memory. Even with unlimited time, every program gets some input wrong or never answers.

Most functions are like this. There are only as many programs as there are whole numbers, but there are far more ways to assign an answer to each whole number. So most rules for answers have no program at all.

Some uncomputable functions have short, clear definitions. "Does this program stop?" is one. "What is the largest number of marks a machine with this many states can print before it stops?" is another. Each answer is a definite number, but no single method finds all of them.

## The idea

**Definition.** Let $\varphi_0, \varphi_1, \ldots$ be the partial computable functions, numbered by a [Gödel numbering](/godel-numbering/) of Turing machines. A partial function $f : \mathbb{N} \to \mathbb{N}$ is computable if $f = \varphi_e$ for some $e$. Otherwise it is uncomputable. For a set $A$, the characteristic function $\chi_A$ is computable exactly when $A$ is decidable.

**Counting.** The machines can be listed, so the computable functions form a countable set. The total functions from $\mathbb{N}$ to $\{0, 1\}$ form an uncountable set, by Cantor's [diagonalization argument](/diagonalization-argument/). So all but countably many of them are uncomputable. See [countability](/countability/) and the [counting argument](/counting-argument/).

**The diagonal function.** An explicit total example is
$$d(e) = \begin{cases} \varphi_e(e) + 1 & \text{if } \varphi_e(e) \text{ is defined,} \\ 0 & \text{otherwise.} \end{cases}$$
If $d = \varphi_e$ for some $e$, then $d$ is total, so $\varphi_e(e)$ is defined and $d(e) = \varphi_e(e) + 1 \neq \varphi_e(e)$, which is a contradiction. The partial function $e \mapsto \varphi_e(e) + 1$ is computable; the uncomputable part is deciding which case holds, which is the set $K$.

**Uncomputable is not the same as unknown.** Let $g(n) = 1$ for all $n$ if Goldbach's conjecture is true, and $g(n) = 0$ for all $n$ otherwise. Then $g$ is computable, because it is one of two constant functions and both are computable. Nobody knows which program computes it, but one of the two does. A function is uncomputable only if no program at all computes it.

**Degrees of uncomputability.** Uncomputable functions differ in how far they are from computable ones.

- *Limit computable.* Some functions are limits of computable guesses: $f(n) = \lim_s g(n, s)$ for a computable $g$, where the guesses change only finitely often. The characteristic function of $K$ is one: guess $0$, and switch to $1$ if $\varphi_e(e)$ halts within $s$ steps. Shoenfield's limit lemma says that these are exactly the functions computable with an oracle for the halting problem, the functions of [Turing degree](/turing-degrees/) at most $\mathbf{0}'$.
- *Higher.* The function that tells whether $\varphi_e$ is total is not limit computable. It sits at level $\Pi_2$ of the [arithmetical hierarchy](/arithmetical-hierarchy/). Truth of sentences of arithmetic is not at any finite level.

**Growth.** A total function that grows faster than every computable function is uncomputable. The busy beaver function $\Sigma$ is the standard example: for every computable $f$, $\Sigma(n) > f(n)$ for all large $n$.

## Examples

- **Halting.** $h(e, x) = 1$ if $\varphi_e(x)$ is defined and $0$ otherwise. This is the characteristic function of the halting problem, and it is uncomputable.
- **Busy beaver.** $\Sigma(n)$ is the largest number of ones that a halting $n$-state, two-symbol machine leaves on a blank tape. The known values are $\Sigma(1) = 1$, $\Sigma(2) = 4$, $\Sigma(3) = 6$, $\Sigma(4) = 13$ and $\Sigma(5) = 4098$. Each value is a definite number, but $\Sigma$ grows faster than any computable function. It is a lower limit: the guess "most ones among the machines that have halted within $s$ steps" only goes up and reaches $\Sigma(n)$.
- **Kolmogorov complexity.** $K(x)$, the length of the shortest program that prints $x$, is uncomputable. It is an upper limit: the guess "shortest program that has printed $x$ within $s$ steps" only goes down and reaches $K(x)$.
- **Diophantine equations.** The function that tells whether a polynomial equation with integer coefficients has a solution in integers is uncomputable. This is [Hilbert's tenth problem](/hilberts-tenth-problem/).
- **Bits of a number.** The function $n \mapsto$ the $n$-th bit of [Chaitin's constant](/chaitins-constant/) is uncomputable, and so is the function that gives the $n$-th bit of the binary expansion of $\sum_{e \in K} 2^{-e-1}$.
- **Semantic properties.** By [Rice's theorem](/rice-theorem/), the characteristic function of every nontrivial property of the function $\varphi_e$ is uncomputable. Examples are "is $\varphi_e$ total?" and "is $\varphi_e$ the constant zero?".

## Where it is used

- **Limits of software.** An uncomputable function marks a task that no tool can do in full. Compilers, verifiers and compressors can only approximate termination, program equivalence or shortest descriptions.
- **Undecidability proofs.** Each [undecidable](/undecidability/) problem gives an uncomputable characteristic function, and reductions transfer uncomputability from one function to another.
- **Logic.** The uncomputability of the halting function gives the undecidability of first-order logic ([Church's theorem](/church-theorem/)) and the [incompleteness theorems](/godel-incompleteness-theorem/).
- **Growth bounds.** Since $\Sigma$ outgrows every computable function, no computable bound limits the running time of halting machines of a given size. This is why brute-force search for the busy beaver values needs proofs about each machine that does not halt.

## References
