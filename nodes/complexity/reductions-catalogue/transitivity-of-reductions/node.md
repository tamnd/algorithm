---
tag: E1AEJ5
kind: theorem
slug: transitivity-of-reductions
name: Transitivity of reductions
area: complexity/reductions-catalogue
level: intro
summary: If A reduces to B and B reduces to C, then A reduces to C, for Karp, Cook, logspace, Levin and parsimonious reductions. So NP-hardness proofs can chain.
prereqs: [polynomial-time-reduction]
see_also: [turing-reduction, levin-reduction, parsimonious-reduction, logspace, np-completeness-proof, fine-grained-reduction, reduction, np-hard]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: "Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (eds.), Complexity of Computer Computations, Plenum Press, 1972, 85-103"
    locator: the transitivity of polynomial-time reducibility, used to chain the reductions from satisfiability
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 2.5, Polynomial Transformations and NP-Completeness (transitivity of polynomial transformations)
  - paper: doi:10.1016/S0022-0000(75)80050-X
    title: "Neil D. Jones, Space-bounded reducibility among combinatorial problems, Journal of Computer and System Sciences 11(1) (1975), 68-85"
    locator: logspace reducibility and the proof that it is transitive
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, 3rd edition, Cengage Learning, 2013
    locator: Section 7.4 (polynomial time reducibility) and Section 8.5 (log space reducibility and its transitivity)
---

Reductions compose: if $A$ reduces to $B$ and $B$ reduces to $C$, then $A$ reduces to $C$, with the same kind of reduction. This holds for [Karp reductions](/polynomial-time-reduction/), [Cook reductions](/turing-reduction/), [logspace](/logspace/) reductions, [Levin reductions](/levin-reduction/) and [parsimonious reductions](/parsimonious-reduction/). The polynomial-time cases follow because a polynomial of a polynomial is a polynomial; the logspace case needs a recomputation trick, because the intermediate output is too long to store. Transitivity is why one NP-complete problem is enough to start an [NP-completeness proof](/np-completeness-proof/) for the next one.

## Statement

**Theorem.** Let $A$, $B$, $C \subseteq \{0,1\}^*$, and let $p$ and $q$ be polynomials, which we may take to be non-decreasing.

1. **(Karp.)** If $f$ is a Karp reduction from $A$ to $B$ computable in time $p(n)$, and $g$ is a Karp reduction from $B$ to $C$ computable in time $q(n)$, then $g \circ f$ is a Karp reduction from $A$ to $C$ computable in time $O(p(n) + q(p(n)))$, with $|g(f(x))| \le q(p(|x|))$.
2. **(Cook.)** If $A$ Cook-reduces to $B$ in time $p(n)$ and $B$ Cook-reduces to $C$ in time $q(n)$, then $A$ Cook-reduces to $C$ in time $O(p(n) \cdot (1 + q(p(n))))$.
3. **(Logspace.)** If $f$ and $g$ are logspace reductions from $A$ to $B$ and from $B$ to $C$, then $g \circ f$ is a logspace reduction from $A$ to $C$.
4. **(Levin and parsimonious.)** The composition of two Levin reductions is a Levin reduction, and the composition of two parsimonious reductions is parsimonious.

Time is measured on a multitape Turing machine. Every $O$ hides only a constant factor that depends on the machines, not on $x$.

## In plain words

To solve a problem, you may turn it into a second problem, and then turn that one into a third. Doing both steps in a row is again a fast way to turn the first problem into the third. So you never need to reduce straight from the first known hard problem; any hard problem already on the list will do. The only catch is that the costs multiply: two slow steps in a row can be much slower than either one.

## Proof

**Part 1 (Karp).** Let $M_f$ and $M_g$ be machines that compute $f$ in time $p$ and $g$ in time $q$. A machine $M$ for $g \circ f$ first runs $M_f$ on $x$ and writes $y = f(x)$ on a work tape. This takes at most $p(n)$ steps, where $n = |x|$, so $|y| \le p(n)$, since a machine writes at most one symbol per step. Then $M$ moves the head back to the start of $y$ in at most $p(n)$ steps and runs $M_g$ on $y$, which takes at most $q(|y|) \le q(p(n))$ steps, because $q$ is non-decreasing. The total is $O(p(n) + q(p(n)))$, a polynomial in $n$. Its output $g(y)$ has length at most $q(p(n))$. For correctness, for every $x$:

$$x \in A \iff f(x) \in B \iff g(f(x)) \in C,$$

where the first equivalence is the property of $f$ and the second is the property of $g$ applied to the string $f(x)$. The second step uses the fact that $g$ is correct on every string, also on strings that do not look like natural instances of $B$.

**Part 2 (Cook).** Let $M_1$ be an oracle machine that decides $A$ with oracle $B$ in time $p$, and $M_2$ one that decides $B$ with oracle $C$ in time $q$. Build $M$ with oracle $C$: it runs $M_1$, and whenever $M_1$ asks a question $y$, it runs $M_2^C$ on $y$ and gives its answer to $M_1$. Since $M_2^C$ decides $B$, every answer is the correct answer of a $B$-oracle, so $M^C$ accepts exactly the strings that $M_1^B$ accepts, which is $A$. For the time, $M_1$ makes at most $p(n)$ steps, so it asks at most $p(n)$ questions, each of length at most $p(n)$. Each run of $M_2^C$ takes at most $q(p(n))$ steps. Copying a question to a work tape and resetting the heads costs $O(p(n) + q(p(n)))$ per question. So the total time is $O(p(n) \cdot (1 + q(p(n))))$, a polynomial. Questions to $C$ come only from runs of $M_2$, and each has length at most $q(p(n))$.

**Part 3 (logspace).** A logspace transducer has a read-only input tape, a write-only output tape whose head only moves right, and work tapes with $O(\log n)$ cells. Let $M_f$ and $M_g$ be such transducers for $f$ and $g$. A logspace machine has at most $|x| \cdot 2^{O(\log |x|)}$ configurations that can occur, which is polynomial in $|x|$, and it halts, so it runs for polynomial time and $|f(x)| \le r(|x|)$ for a polynomial $r$.

The machine $M$ cannot write $f(x)$ down, since it may have polynomial length. Instead, $M$ simulates $M_g$ on the input $f(x)$ and keeps only a counter $i$, the position of the input head of $M_g$ on $f(x)$. When $M_g$ reads its input symbol, $M$ computes the $i$-th symbol of $f(x)$ from the start: it runs $M_f$ on $x$, does not write $M_f$'s output, counts the output symbols, and stops when it reaches symbol number $i$. When $M_g$ moves its input head, $M$ adds or subtracts $1$ from $i$. The output of $M$ is the output of $M_g$.

The space used is: the work tapes of $M_g$, which hold $O(\log |f(x)|) = O(\log r(n)) = O(\log n)$ cells; the counter $i \le r(n)$, with $O(\log n)$ bits; the work tapes of one run of $M_f$, with $O(\log n)$ cells; and a counter for the output symbols of $M_f$, with $O(\log n)$ bits. The total is $O(\log n)$. The output is $g(f(x))$, so correctness follows as in Part 1. The running time is polynomial, because $M_f$ is run again for each step of $M_g$, which is polynomial times polynomial.

**Part 4 (Levin and parsimonious).** Let $(f_1, g_1, h_1)$ be a Levin reduction from $R$ to $R'$ and $(f_2, g_2, h_2)$ one from $R'$ to $R''$. Put $f = f_2 \circ f_1$, $g(x, w'') = g_1(x, g_2(f_1(x), w''))$ and $h(x, w) = h_2(f_1(x), h_1(x, w))$. By Part 1, $f$ is a Karp reduction. If $w'' \in R''(f(x))$, then $g_2(f_1(x), w'') \in R'(f_1(x))$, so $g(x, w'') \in R(x)$. If $w \in R(x)$, then $h_1(x, w) \in R'(f_1(x))$, so $h(x, w) \in R''(f(x))$. Each map applies polynomial-time maps to strings of polynomial length, so it runs in polynomial time, as in Part 1. For parsimonious reductions, $\#R(x) = \#R'(f_1(x)) = \#R''(f_2(f_1(x)))$ for every $x$. $\square$

## Consequences

- **Hardness moves forward.** If $A$ is [NP-hard](/np-hard/) and $A \le_m^p B$, then $B$ is NP-hard: every $L \in$ NP has $L \le_m^p A$, and Part 1 gives $L \le_m^p B$. With $B \in$ NP, $B$ is [NP-complete](/np-complete/). This is step 2 of the [NP-completeness proof](/np-completeness-proof/) recipe.
- **Equivalence classes.** $\le_m^p$ and $\le_T^p$ are preorders, so $A \equiv B$ (each reduces to the other) is an equivalence relation. All NP-complete problems form one class under $\equiv_m^p$.
- **A chain, with numbers.** Take $\varphi = (x_1 \lor x_2 \lor \neg x_3) \land (\neg x_1 \lor x_2 \lor x_3) \land (\neg x_1 \lor \neg x_2 \lor \neg x_3)$. The standard reduction from [3-SAT](/3-sat/) to independent set gives a graph with $9$ vertices, $15$ edges and target $3$. Complementing the set gives [vertex cover](/vertex-cover/) with target $9 - 3 = 6$. Taking the $15$ edges as the universe and, for each vertex, the set of edges at that vertex gives [set cover](/set-cover/) with $9$ sets and target $6$. The composed map sends $\varphi$ straight to this set cover instance. There are $12$ independent sets of size $3$, $12$ vertex covers of size $6$ and $12$ set covers of size $6$, while $\varphi$ has $5$ satisfying assignments. The last two steps are parsimonious, and the first is not.
- **Closure of classes.** P, NP and coNP are closed under $\le_m^p$, and P is closed under $\le_T^p$. Together with transitivity, a problem $A \le_m^p B$ for a $B$ in a class inherits every upper bound that $B$ has, up to the polynomial in Part 1.

## Tightness

- **Exponents multiply.** The bound $q(p(n))$ in Part 1 can be reached. Let $\mathrm{pad}(x) = x\,1\,0^{|x|^2 - |x| - 1}$ for $|x| \ge 2$, a map from a language $A$ to its padded version, of output length $|x|^2$, computed in time $O(|x|^2)$. Applying it twice gives a string of length $|x|^4$, so the composition of two quadratic-time reductions can need quartic time just to write its output. A chain of $k$ such steps has output length $n^{2^k}$.
- **Only a fixed number of steps.** Transitivity applies to a constant number of reductions. Composing a number of reductions that grows with $n$ can leave polynomial time: $\log_2 n$ squarings give length $n^{n}$.
- **Exact exponents are lost.** Because of this growth, a Karp reduction says nothing about the exact exponent of an algorithm. Statements such as "an $O(n^{2-\varepsilon})$ algorithm for $B$ gives one for $A$" need [fine-grained reductions](/fine-grained-reduction/), which control the size of each step.
- **Logspace needs the trick.** Writing $f(x)$ to a work tape in Part 3 would use polynomial space, not logarithmic. Recomputing each symbol on demand trades time for space; the result is still polynomial time.

## History

Cook (1971) and Karp (1972) both used transitivity to pass hardness from one problem to the next; Karp chained his reductions from satisfiability into a tree of $21$ problems ([Karp's 21 NP-complete problems](/karps-21-np-complete-problems/)). Garey and Johnson (1979, Section 2.5) state transitivity of polynomial transformations as a lemma and use it to set up their method of proof. Jones (1975) studied logspace reducibility among combinatorial problems and proved its transitivity with the recomputation argument of Part 3; Sipser (Section 8.5) uses the same idea for NL-completeness.

## References
