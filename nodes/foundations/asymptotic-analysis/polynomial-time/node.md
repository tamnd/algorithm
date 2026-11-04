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
    locator: Section 7.1 (measuring complexity, the relation between models) and Section 7.2 (the class P)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 1 (the class P and the robustness of the model) and Chapter 3 (the time hierarchy theorem)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 34.1, Polynomial time (encodings and pseudo-polynomial algorithms)
  - paper: doi:10.4153/CJM-1965-045-4
    title: Jack Edmonds, Paths, trees, and flowers, Canadian Journal of Mathematics 17, 449 to 467 (1965)
    locator: Section 2, the digression on good algorithms
  - paper: "Alan Cobham, The intrinsic computational difficulty of functions, in Logic, Methodology and Philosophy of Science, Proceedings of the 1964 International Congress, North-Holland (1965), 24 to 30"
    locator: the class of functions computable in polynomial time
  - paper: doi:10.1109/SWAT.1974.20
    title: Juris Hartmanis and Janos Simon, On the power of multiplication in random access machines, 15th Annual Symposium on Switching and Automata Theory (1974), 13 to 23
    locator: the main theorem on RAMs with unit-cost multiplication
  - paper: doi:10.4007/annals.2004.160.781
    title: Manindra Agrawal, Neeraj Kayal and Nitin Saxena, PRIMES is in P, Annals of Mathematics 160(2), 781 to 793 (2004)
    locator: the main theorem
---

An algorithm runs in polynomial time when its worst-case [time](/time-complexity/) is $O(n^k)$ for some constant $k$, where $n$ is the length of the input in bits or symbols. The decision problems that a deterministic algorithm solves in polynomial time form the complexity class [P](/p/). Polynomial time is the usual formal meaning of "efficient": it contains [quadratic](/quadratic-time/) and [cubic](/cubic-time/) time, it does not depend on the choice among the usual machine models, and it does not contain [exponential time](/exptime/). The definition counts the length of the input, not the values of the numbers in it, and this is the difference between polynomial and [pseudo-polynomial](/pseudo-polynomial-time/) time.

## In plain words

A program passes the polynomial-time test when its running time is at most the input length raised to some fixed power, such as 2, 3 or 10. The power can be large, but it must stay fixed.

A program that fails the test grows much faster. A program that tries each subset of the items doubles its time each time one item is added. The test does not promise speed in practice: a power of 50 passes it and is useless. But a program built from parts that pass the test passes it too, and the test gives the same answer on each reasonable kind of machine. So theory uses it.

The test counts the length of the input as written, not the size of a number. A program that counts up to a number in the input is fast for short numbers and slow for long ones.

## The idea

### Definition

Fix an alphabet $\Sigma$ with at least two symbols and write $|x|$ for the length of a string $x \in \Sigma^*$. An algorithm on strings, in a stated machine model, runs in *polynomial time* when there are constants $c, k \ge 0$ such that, for each $x \in \Sigma^*$, the algorithm stops on $x$ within $c\,(|x|+1)^k$ steps. This is $T(n) = O(n^k)$ for the worst-case time $T$; the term $+1$ only handles the empty string. The class P is the set of languages $L \subseteq \Sigma^*$ that some deterministic polynomial-time algorithm decides:

$$\mathrm{P} = \bigcup_{k \ge 0} \mathrm{DTIME}(n^k),$$

where $\mathrm{DTIME}(f(n))$ is the [complexity class](/complexity-class/) of the languages that a deterministic multi-tape [Turing machine](/turing-machine/) decides in time $O(f(n))$. The class [FP](/fp/) is the same idea for functions $f : \Sigma^* \to \Sigma^*$.

### The input length is in bits

The size $n$ is the length of a standard encoding of the input. An integer $N \ge 1$ has $\lfloor \lg N \rfloor + 1$ bits. A graph with $V \ge 2$ vertices and $E$ edges in adjacency lists has $\Theta((V + E) \log V)$ bits. Two reasonable encodings of the same objects have lengths that are polynomially related, so the class does not depend on the choice. A number written in unary is not a reasonable encoding, because it is exponentially longer than the binary form (CLRS, Section 34.1). See [input size](/input-size/).

### The model of computation

The class P is the same on the single-tape and the multi-tape Turing machine, and on the [word RAM](/word-ram/) with words of $O(\log n)$ bits, because each simulates the others with a polynomial slowdown. A multi-tape machine that runs in time $t(n) \ge n$ is simulated by a single-tape machine in time $O(t(n)^2)$ (Sipser, Section 7.1). The exponent $k$ can change from one model to another: a statement such as "cubic time" needs a model, and the statement "polynomial time" does not.

The exception is a RAM with unbounded registers and unit-cost multiplication. Starting from 2, it computes $2^{2^n}$ with $n$ squarings, a number of $2^n + 1$ bits, so it does not simulate the Turing machine with a polynomial slowdown. Hartmanis and Simon (1974) showed that such machines, with bitwise Boolean operations on registers as well, decide in polynomial time exactly the languages of PSPACE. So a "polynomial" bound in that model is not a polynomial bound in the usual sense. See [unit-cost model](/unit-cost-model/) and [logarithmic-cost model](/logarithmic-cost-model/).

### Closure under composition

*Claim.* Let $f$ be computable in time $p(n)$ and $g$ in time $q(n)$ on multi-tape Turing machines, where $p$ and $q$ are non-decreasing polynomials. Then $g \circ f$ is computable in time $O(p(n) + q(p(n)))$, which is polynomial.

*Proof.* On input $x$ with $|x| = n$, run the machine for $f$. It stops within $p(n)$ steps. It writes at most one symbol in each step, so $|f(x)| \le p(n)$. Copying $f(x)$ to the input tape of the machine for $g$ and moving the head back takes $O(p(n))$ steps. Then the machine for $g$ runs on $f(x)$ for at most $q(|f(x)|) \le q(p(n))$ steps, because $q$ is non-decreasing. The total is $O(p(n) + q(p(n)))$. A composition and a sum of polynomials are polynomials. $\square$

In the same way, an algorithm that makes at most $p(n)$ calls to a polynomial-time subroutine, each on an argument of length at most $p(n)$, runs in polynomial time. This closure is the base of the [polynomial-time reductions](/polynomial-time-reduction/) of the theory of [NP-completeness](/np-complete/). The condition on the length of the arguments is essential, see the pitfalls.

### The exponent matters

Polynomial time is not one level. The deterministic [time hierarchy theorem](/time-hierarchy-theorem/) gives $\mathrm{DTIME}(n^k) \subsetneq \mathrm{DTIME}(n^{k+1})$ for each $k \ge 1$, because $n^k \log n^k = o(n^{k+1})$ (Arora and Barak, Chapter 3). Above polynomial time lie [quasi-polynomial time](/quasi-polynomial-time/), $2^{(\log n)^{O(1)}}$, then [subexponential time](/subexponential-time/), then exponential time.

### Strongly and weakly polynomial

For problems whose input is a list of numbers, a second test is used. An algorithm is *strongly polynomial* when the number of arithmetic operations and comparisons is bounded by a polynomial in the count of the input numbers, whatever their values, and the numbers that it creates have bit lengths bounded by a polynomial in the input length. It is *weakly polynomial* when it is polynomial in the bit length but not in this stronger sense. Sorting $n$ numbers by comparisons is strongly polynomial. The [ellipsoid method](/ellipsoid-method/) for linear programming is weakly polynomial: its number of iterations grows with the bit length of the input. Whether linear programming has a strongly polynomial algorithm is open.

### Pitfalls

- **Pseudo-polynomial is not polynomial.** The dynamic program for the [subset sum problem](/subset-sum-problem/) and for the [knapsack problem](/knapsack-problem/) fills a table of $(n+1)(W+1)$ cells for $n$ items and a target or capacity $W$. The input length is about $n \lg W$ bits plus the lengths of the items. For $n = 40$ items of 41 bits and $W = 2^{40}$, the input has about 1640 bits, and the table has about $4.5 \times 10^{13}$ cells. The time is polynomial in the value $W$ and exponential in its length. Subset sum is NP-complete, and this dynamic program does not show $\mathrm{P} = \mathrm{NP}$. See [pseudo-polynomial time](/pseudo-polynomial-time/) and [strong NP-hardness](/strong-np-hardness/).
- **A loop up to the value.** [Trial division](/trial-division/) tests whether $N$ is prime with up to $\lfloor \sqrt N \rfloor$ divisions. For the prime $N = 2^{61} - 1$, an input of 61 bits, that is 1518500249 divisions. The time is about $2^{\beta/2}$ for $\beta$ bits, exponential in the input length. The [AKS primality test](/aks-primality-test/) shows that primality is in P (Agrawal, Kayal and Saxena, 2004).
- **Composition without a length bound.** Calling a polynomial-time subroutine $n$ times on its own output can take exponential time. Squaring a number is polynomial, but $n$ squarings of 2 give $2^{2^n}$, with $2^n + 1$ bits: 1025 bits after 10 squarings. The closure claim needs a polynomial bound on the length of every argument.
- **Unit cost on unbounded numbers.** A bound that counts arithmetic operations on numbers of any size is polynomial in the usual sense only when the bit lengths of the numbers also stay polynomial. See the model section above.
- **The encoding.** A problem on a number $N$ written in unary has input length $N$, so a time of $O(N)$ is then polynomial. Changing the encoding to make an algorithm "polynomial" changes the problem.
- **Polynomial is not practical.** A time of $n^{100}$, or $n^2$ with a constant of $10^{30}$, is polynomial and useless. An exponential algorithm can be fast on the inputs that occur, as the [simplex method](/simplex-method/) is, although several classical pivot rules take exponential time in the worst case.

## Examples

- Sorting $n$ numbers with [merge sort](/merge-sort/) takes $O(n \log n)$ comparisons, which is $O(n^2)$.
- Shortest paths with non-negative weights, minimum spanning trees, maximum matching in general graphs and maximum flow are in P. Edmonds's 1965 paper on matching is the source of the term "good algorithm".
- Linear programming is in P by the ellipsoid method (Khachiyan, 1979), which is slow in practice.
- Primality testing is in P (Agrawal, Kayal and Saxena, 2004).
- Subset sum with the target 9 and the numbers 3, 34, 4, 12, 5, 2: the dynamic program fills $7 \times 10 = 70$ cells and finds $4 + 5 = 9$. This is cheap because $W = 9$ is small, not because the method is polynomial.
- Non-example: the brute-force algorithm for [subset sum](/subset-sum-problem/) tries all $2^n$ subsets, in $\Theta(2^n n)$ time. No polynomial-time algorithm is known, and one would prove $\mathrm{P} = \mathrm{NP}$, see the [P versus NP problem](/p-versus-np-problem/).
- Non-example: no polynomial-time algorithm is known on a classical computer for the factoring of an integer given in binary. Factoring is not known to be NP-complete.
- Non-example: $n^{\lg n} = 2^{\lg^2 n}$ grows faster than each polynomial. For $n = 2^{20}$ it is $2^{400}$, while $n^3 = 2^{60}$.

## Where it is used

Polynomial time is the standard meaning of "tractable" in complexity theory, and the class P is the base for the definitions of [NP](/np/), of [NP-hardness](/np-hard/) and of the polynomial-time reduction. The thesis that *feasible* means *polynomial time* is called the Cobham-Edmonds thesis. Cobham (1965) proposed the functions computable in polynomial time as a class that does not depend on the machine, and Edmonds (1965) called an algorithm "good" when its running time has a polynomial bound. The thesis is a convention, not a theorem, and it has the weak points listed above. It stays in use for two reasons: the natural problems in P tend to have algorithms of low degree, and the class does not depend on the machine model. See [computational tractability](/computational-tractability/).

## References
