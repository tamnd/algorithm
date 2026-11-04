---
tag: Y931HC
kind: concept
slug: polynomial-time
name: Polynomial time
aliases:
- O(n^k) time
area: foundations/asymptotic-analysis
level: intro
summary: Running time bounded by a polynomial in the input size, the standard formal notion of efficient computation and the class P.
prereqs: [asymptotic-notation, time-complexity, input-size]
see_also: [p, np, quadratic-time, cubic-time, pseudo-polynomial-time, quasi-polynomial-time, time-hierarchy-theorem, computational-tractability]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 7.2 (the class P)
  - book: isbn:9780521424264
    title: Arora and Barak, Computational Complexity, A Modern Approach
    locator: Chapter 1
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 34
  - paper: doi:10.4153/CJM-1965-045-4
    title: Jack Edmonds, Paths, trees, and flowers, Canadian Journal of Mathematics 17 (1965)
    locator: the digression on good algorithms
  - paper: "Alan Cobham, The intrinsic computational difficulty of functions, Proceedings of the 1964 International Congress for Logic, Methodology and Philosophy of Science (1965)"
    locator: the class of functions computable in polynomial time
  - paper: "Leonid G. Khachiyan, A polynomial algorithm in linear programming, Soviet Mathematics Doklady 20 (1979)"
    locator: the ellipsoid method for linear programming
  - paper: "Manindra Agrawal, Neeraj Kayal and Nitin Saxena, PRIMES is in P, Annals of Mathematics 160 (2004)"
    locator: the main theorem
---

An algorithm runs in polynomial time when its worst-case [time](/time-complexity/) is $O(n^k)$ for some constant $k$, where $n$ is the length of the input in bits (or symbols). The decision problems that a deterministic algorithm solves in polynomial time form the complexity class [P](/p/). Polynomial time is the usual formal meaning of "efficient": it contains the classes of [quadratic](/quadratic-time/) and [cubic](/cubic-time/) time, and it does not contain [exponential time](/exptime/).

## In plain words

A program passes the polynomial-time test when its running time is at most the input length raised to some fixed power, such as 2, 3 or 10. The power can be large, but it must not change when the input grows.

A program that fails the test grows much faster. A program that tries each subset of the items doubles its time each time one item is added. The test does not promise speed in practice: a power of 50 passes it and is useless. But a program built from parts that pass the test passes it too. This is why theory uses it.

The test counts the length of the input as written, not the value of a number. A program that counts up to a number in the input can be fast for the value and slow for the length.

## The idea

**Definition.** Fix an alphabet $\Sigma$ with at least two symbols and write $|x|$ for the length of a string $x \in \Sigma^*$. An algorithm $A$ on strings, in a stated machine model, runs in *polynomial time* when there are constants $c, k \ge 0$ such that for each $x \in \Sigma^*$ the algorithm stops on $x$ within $c\,(|x|+1)^k$ steps. This is the same as $T(n) = O(n^k)$ for the worst-case time $T$, for $n \ge 1$. The term $+1$ only handles the empty string. The class P is the set of languages (decision problems) $L \subseteq \Sigma^*$ for which some deterministic polynomial-time algorithm decides, for each $x$, whether $x \in L$.

$$\mathrm{P} = \bigcup_{k \ge 0} \mathrm{DTIME}(n^k).$$

Here $\mathrm{DTIME}(f(n))$ is the [complexity class](/complexity-class/) of the languages that a deterministic algorithm decides in time $O(f(n))$.

The class [FP](/fp/) is the same idea for functions: the functions $f : \Sigma^* \to \Sigma^*$ that a deterministic polynomial-time algorithm computes.

**The input length is in bits.** The size $n$ is the length of a standard encoding of the input. A graph given by its adjacency list has $n = \Theta((|V| + |E|) \log |V|)$ bits, and an integer $N$ has $\lfloor \lg N \rfloor + 1$ bits. Two reasonable encodings of the same object have lengths that are polynomially related, so the class does not depend on the choice. A number written in unary is not a reasonable encoding, because it is exponentially longer than the binary form. See [input size](/input-size/) and [unary encoding](/unary-encoding/).

**Model.** The class P is the same in the common models, because they simulate each other with a polynomial slowdown: the [Turing machine](/turing-machine/) (single or multi-tape), and the [word RAM](/word-ram/) with words of $O(\log n)$ bits. The exponent $k$ can change from one model to another, so a statement such as "cubic time" needs a model, and the statement "polynomial time" does not. A model with unit cost, unbounded integers and multiplication in one step is the exception. A RAM that multiplies integers of any size in one step can compute $2^{2^n}$ by $n$ squarings in $n$ steps, and the answer has $2^n$ bits. So this unit-cost model does not simulate the Turing machine with a polynomial slowdown. See [unit-cost model](/unit-cost-model/).

**Closure under composition.** The reason for the choice of polynomials is that the class is closed under the operations by which algorithms are built.

*Claim.* Let $f$ be computable in time $p(n)$ and $g$ in time $q(n)$ on a Turing machine, where $p$ and $q$ are polynomials that are non-decreasing. Then $g \circ f$ is computable in time $O(p(n) + q(p(n)))$, which is polynomial.

*Proof.* On input $x$ with $|x| = n$, run the machine for $f$. It stops after at most $p(n)$ steps. A Turing machine writes at most one symbol in each step, so the output $f(x)$ has length at most $p(n)$. Now run the machine for $g$ on $f(x)$. By the bound for $g$, this takes at most $q(|f(x)|) \le q(p(n))$ steps, because $q$ is non-decreasing. Copying $f(x)$ to the input tape of the machine for $g$ and moving the head back takes $O(p(n))$ more steps. So the total is $O(p(n) + q(p(n)))$. The composition of two polynomials is a polynomial, and the sum of two polynomials is a polynomial. $\square$

The same argument shows that an algorithm that makes at most $p(n)$ calls to a polynomial-time subroutine, with arguments of length at most $p(n)$, runs in polynomial time. The sum and the product of two polynomial running times are polynomial. This is the base of the [polynomial-time reductions](/polynomial-time-reduction/) of the theory of [NP-completeness](/np-complete/).

**The exponent matters.** Polynomial time is not one level. The deterministic [time hierarchy theorem](/time-hierarchy-theorem/) shows that, on multi-tape Turing machines, $\mathrm{DTIME}(n^k) \subsetneq \mathrm{DTIME}(n^{k+1})$ for each $k \ge 1$. So there are problems that are solvable in time $n^{k+1}$ and not in time $n^k$. Above polynomial time are [quasi-polynomial time](/quasi-polynomial-time/), the class $2^{(\log n)^{O(1)}}$, that is, $2^{O((\log n)^c)}$ for some constant $c$, then [subexponential](/subexponential-time/) time, then exponential time.

**Pseudo-polynomial time.** The test counts the length of the input, not the value of a number in the input. An algorithm with time polynomial in the value is *pseudo-polynomial*, and it is exponential in the length when the number is written in binary. Two examples:

- [Trial division](/trial-division/) tests whether $N$ is prime with about $\sqrt{N}$ divisions. The length is $b = \lfloor \lg N \rfloor + 1$ bits, and $\sqrt{N} \approx 2^{b/2}$, so the time is exponential in the length.
- The dynamic program for [subset sum](/subset-sum-problem/) and for the [knapsack problem](/knapsack-problem/) takes $O(nW)$ time for $n$ items and a target or capacity $W$. The input length is about $n \lg W$ bits plus the length of the items, so $W$ can be $2^{\Theta(n)}$, and the time is then exponential. The problem is NP-complete in the usual sense, and the dynamic program does not show that P equals NP.

See [pseudo-polynomial time](/pseudo-polynomial-time/) for the exact definition, and [weak and strong NP-hardness](/strong-np-hardness/).

**Strong and weak polynomial time.** For problems whose input is a list of numbers, a second test is used in the arithmetic model. An algorithm is *strongly polynomial* when the number of arithmetic operations and comparisons is polynomial in the count of the input numbers, whatever their values, and the sizes of the numbers during the run are polynomial in the input length. It is *weakly polynomial* when it is polynomial in the length in bits only. Sorting $n$ numbers by comparisons is strongly polynomial. The ellipsoid method for linear programming is weakly polynomial: its number of iterations grows with the bit length of the input, so it is not strongly polynomial. Whether linear programming has any strongly polynomial algorithm is a long-standing open question.

## Examples

- Sorting $n$ numbers with [merge sort](/merge-sort/) takes $O(n \log n)$ comparisons. This is $O(n^2)$, so it is in polynomial time.
- Shortest paths with non-negative weights, minimum spanning trees, maximum matching in graphs and maximum flow are in P.
- Linear programming is in P by the ellipsoid method (Khachiyan, 1979), and this method is slow in practice. The simplex method, which many practitioners prefer, has exponential worst-case time for several classical pivot rules.
- Primality testing is in P (Agrawal, Kayal and Saxena, 2004).
- Non-example: the usual algorithm for the [subset sum problem](/subset-sum-problem/) with numbers in binary tries $2^n$ subsets. The time $\Theta(2^n \cdot n)$ is exponential, and no polynomial-time algorithm is known. The problem is [NP-complete](/np-complete/), so a polynomial algorithm would prove $\mathrm{P} = \mathrm{NP}$ (see the [P versus NP problem](/p-versus-np-problem/)).
- Non-example: no polynomial-time algorithm is known on a classical computer for the factoring of an integer given in binary. It is not known to be NP-complete.
- Non-example: a function such as $n^{\lg n}$ grows faster than each polynomial. For $n = 2^{20}$ it is $2^{400}$, and $n^3 = 2^{60}$.

## Where it is used

Polynomial time is the standard meaning of "tractable" or "efficient" in complexity theory, and the class P is the base for the definitions of [NP](/np/), of [NP-hardness](/np-hard/) and of the polynomial-time reduction. The thesis that *feasible* means *polynomial time* is called the Cobham-Edmonds thesis. The thesis is named after Alan Cobham, who proposed the class of functions computable in polynomial time as a machine-independent class in 1965, and Jack Edmonds. In 1965 Edmonds called an algorithm "good" when its running time has a polynomial bound. The thesis is a rule, not a theorem, and it has known weak points. An algorithm with time $n^{100}$ or with a huge constant is polynomial and is not practical. An exponential algorithm can be fast on the inputs that occur, as the simplex method is. The thesis keeps its use for two reasons. The natural problems in P tend to have algorithms of low degree, and the class does not depend on the machine model. See [computational tractability](/computational-tractability/).

## References
