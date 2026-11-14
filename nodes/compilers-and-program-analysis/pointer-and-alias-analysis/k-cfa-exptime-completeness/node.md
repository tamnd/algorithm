---
tag: QS1ZW0
kind: theorem
slug: k-cfa-exptime-completeness
name: EXPTIME-completeness of k-CFA
aliases:
- Van Horn-Mairson theorem
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: research
summary: For every fixed k at least 1, deciding whether a function flows to a program point under k-CFA is complete for exponential time.
prereqs: [k-cfa, exptime]
see_also: [zero-cfa, ml-typability-dexptime-completeness, time-hierarchy-theorem, circuit-value-problem, turing-machine, polynomial-time-reduction, object-sensitivity]
sources:
  - paper: doi:10.1145/1411204.1411243
    title: David Van Horn and Harry G. Mairson, Deciding kCFA is complete for EXPTIME, Proceedings of ICFP 2008, 275 to 282
    locator: the main theorem, the EXPTIME-completeness of the control flow problem of k-CFA for every k greater than 0
  - paper: "David Van Horn, The Complexity of Flow Analysis in Higher-Order Languages, PhD thesis, Brandeis University, 2009, arXiv:1311.4733"
    locator: chapter 5, Lemma 10 (membership), Theorems 8 and 9 (NP-hardness), Lemma 11 and Theorem 10 (EXPTIME-hardness), Proposition 1 (exact k-CFA is PTIME-complete); chapter 3, Theorem 3 (0-CFA is PTIME-complete)
  - paper: doi:10.1145/1291151.1291166
    title: David Van Horn and Harry G. Mairson, Relating complexity and precision in control flow analysis, Proceedings of ICFP 2007, 85 to 96
    locator: the PTIME-completeness of 0-CFA, by analysis of linear terms that code Boolean circuits
  - paper: doi:10.1145/1806596.1806631
    title: Matthew Might, Yannis Smaragdakis and David Van Horn, Resolving and exploiting the k-CFA paradox, Proceedings of PLDI 2010, 305 to 315
    locator: why k-CFA of object-oriented programs is polynomial, and the polynomial m-CFA hierarchy for functional programs
---

For each fixed $k \ge 1$, the control flow problem of [k-CFA](/k-cfa/) is complete for [EXPTIME](/exptime/). The problem asks whether, in the k-CFA result of a program, a given function flows to a given program point. Van Horn and Mairson proved this in 2008. It ended a long belief that k-CFA was polynomial for fixed $k$, and it shows a jump: [0-CFA](/zero-cfa/) is complete for polynomial time, while 1-CFA is already as hard as any problem that a Turing machine solves in exponential time. The cause is the environments of closures, which can take exponentially many abstract values. When environments are flat, as for objects that copy their fields when they are created, the same analysis is polynomial.

## Statement

Fix $k \ge 0$. The k-CFA of a closed labeled term $e$ is the least analysis $(\hat C, \hat r)$ of the [k-CFA](/k-cfa/) page, where $\hat C(\ell, \delta)$ is the set of abstract closures at label $\ell$ in contour $\delta$, a sequence of at most $k$ call sites. The *control flow problem* for k-CFA is: given $e$, a function $\lambda x.t$ of $e$ and a label $\ell$ of $e$, decide whether some closure of $\lambda x.t$ is in $\hat C(\ell, \delta)$ for some contour $\delta$. Write $n$ for the size of $e$.

**Theorem (Van Horn and Mairson 2008).** For every fixed $k \ge 1$:

1. *Membership.* The control flow problem for k-CFA can be decided in time $2^{O(n \log n)}$, so it is in EXPTIME.
2. *Hardness.* For every deterministic Turing machine $M$ that halts within $2^{p(|x|)}$ steps on every input $x$, for a polynomial $p$, there is a function computable in logarithmic space that maps $x$ to a closed term $e_x$, a function $\lambda$ of $e_x$ and a label $\ell$ of $e_x$, such that $M$ accepts $x$ exactly when $\lambda$ flows to $\ell$ in the k-CFA of $e_x$.

So the control flow problem for k-CFA is EXPTIME-complete under logarithmic space reductions.

**Corollary.** For every fixed $k \ge 1$, no algorithm decides the k-CFA control flow problem in polynomial time.

## In plain words

k-CFA looks at a program and works out which functions can show up where. For k equal to zero this takes polynomial time. For any larger fixed k, it can take exponential time, and the theorem says that this is not the fault of a poor algorithm. The analysis itself is powerful enough to run any program that needs exponential time. The trick uses the fact that the analysis is not exact. A function value remembers a context for each of its variables, and the analysis mixes these contexts freely. So one small function can stand for exponentially many different values at once, and two uses of the same variable can pick values independently. A clever program uses this to store a huge machine tape and to step the machine forward. The answer to one flow question then tells whether the machine accepts.

## Proof

**Membership (full proof).** Let $n$ be the number of nodes of $e$. A contour is a sequence of at most $k$ labels, so there are $N \le (n + 1)^k$ contours. An abstract closure is a function of $e$ with an environment that maps its at most $n$ free variables to contours, so there are at most $Q = n N^n$ closures. The cache has at most $n N$ entries and the binding table at most $n N$ more, and each holds a subset of the $Q$ closures. The [k-CFA](/k-cfa/) algorithm only adds closures to these sets and stops when a full pass adds nothing. So it makes at most $2 n N Q + 1$ passes, and each pass costs a polynomial in $n$, $N$ and $Q$ (the proof file of the k-CFA page gives the details). With $N \le (n+1)^k$ and $k$ fixed, $Q = 2^{O(n \log n)}$, so the whole run takes $2^{O(n \log n)}$ steps. The answer is read from the final cache. This is Lemma 10 of Van Horn's thesis. $\square$

**Hardness (sketch).** This follows Van Horn's thesis, Section 5.5, Lemma 11 and Theorem 10, and Van Horn and Mairson (2008). Take $M$, $p$ and an input $x$ of length $m$, and let $N = O(p(m))$.

*Step 1: Boolean logic by linear terms.* True and False are closed functions, and every gate of a Boolean circuit is a term that uses each variable exactly once. For such linear terms the analysis is exact: each function is applied to at most one argument, so the abstract flow equals the real flow. This is the construction behind the PTIME-hardness of 0-CFA, by reduction from the [circuit value problem](/circuit-value-problem/) (Van Horn and Mairson 2007).

*Step 2: exponentially many closures at one place.* Consider

```
(fun f1 -> f1 0; f1 1) (fun z1 ->
  (fun f2 -> f2 0; f2 1) (fun z2 ->
    ...
      (fun fN -> fN 0; fN 1) (fun zN ->
        (fun x -> x) (fun w -> w z1 z2 ... zN))))
```

Each $z_i$ is bound to 0 at one call site and to 1 at another, so in 1-CFA it has two contours. The tuple `fun w -> w z1 ... zN` is created in all $2^N$ combinations of these contours. The identity function applied at one fixed call site puts all of them in the same cache entry, under the same contour. So one entry holds $2^N$ closures, one for each bit vector of length $N$. A closure has polynomial size, but the set of closures in one entry can be exponential.

*Step 3: a machine configuration as a set of closures.* A closure codes a tuple $\langle T, S, H, C, b \rangle$ of bit blocks: at time $T$ the machine is in state $S$ with its head on cell $H$, and cell $C$ holds symbol $b$. One configuration of $M$ is the set of such tuples for all cells $C$. The blocks have $O(p(m))$ bits, so they count up to $2^{p(m)}$ steps and cells.

*Step 4: a transition by a cross product.* The step function is a term $\Phi = $ `fun p -> ...` that uses $p$ twice and is otherwise linear. In a real run, both uses of $p$ see the same tuple. In the analysis, $p$ ranges over all tuples in its cache entry, and the two uses are analysed independently, so the body sees every pair of tuples. On each pair, a linear Boolean circuit computes the next tuple. If both tuples have the same time $T$ and the first has $H = C$, it writes the new tuple for cell $H$ at time $T + 1$ with the new state, head and symbol. If the first has time $T + 1$ and the second has time $T$ with $H' \ne C'$, it copies cell $C'$ to time $T + 1$ with the new state and head. On all other pairs it returns a fixed null tuple.

*Step 5: iteration and the answer.* The term applies $\Phi$ again and again to its own output, starting from the initial configuration, with enough iterations for the analysis to reach a fixed point. Every tuple that flows is then a true fact about the run of $M$ on $x$, or the null tuple, by induction on $T$. Every true fact flows, by induction on $T$ and the two rules. A final linear term checks whether some tuple has the accepting state and, if so, sends a chosen function $\lambda$ to a chosen label $\ell$. So $\lambda$ flows to $\ell$ exactly when $M$ accepts $x$.

*Step 6: size and larger $k$.* The term $e_x$ has size polynomial in $m$, and its parts are written out by a log-space transducer. For $k > 1$, each place where the proof needs one shared contour gets $k - 1$ more applications of identity functions. These extra call sites fill the longer contours, so k-CFA of the padded term behaves as 1-CFA of the original.

The full construction, with the circuits for $\Phi$ and the iterator, is in the thesis and the 2008 paper. $\square$

**Corollary.** By the [time hierarchy theorem](/time-hierarchy-theorem/), some language in EXPTIME is not in P. If the control flow problem for some $k \ge 1$ were in P, then every EXPTIME language would be in P, through the log-space reduction of part 2. So it is not in P. $\blacksquare$

## Consequences

- **The k-CFA hierarchy has two levels of cost.** 0-CFA is complete for PTIME, and every fixed $k \ge 1$ gives an EXPTIME-complete problem. Larger fixed $k$ does not raise the class, because the bound of part 1 holds for every fixed $k$.
- **Flat environments are polynomial.** Call an analysis *flat* if every abstract closure has one contour for all its free variables. Then there are at most $n N \le n (n+1)^k$ abstract closures, the sets in the cache have polynomial size, and the same round-robin solver runs in polynomial time. In Java and similar languages, an object copies the values it needs into its fields when it is created, in the context of the creation. So k-call-site and [object-sensitive](/object-sensitivity/) points-to analyses of such languages are flat, and polynomial for fixed $k$. Might, Smaragdakis and Van Horn (2010) used this to explain the "k-CFA paradox", the gap between slow functional k-CFA and fast object-oriented k-CFA, and to design m-CFA, a flat and polynomial analysis for functional programs.
- **Approximation is the source of the hardness.** When the contours are never cut, k-CFA computes the exact run, and Van Horn shows that this exact problem is only PTIME-complete (Proposition 1 of the thesis). The power to reach EXPTIME comes from mixing the contours of different variables.
- **NP-hardness has a short proof.** With Step 2 and one Boolean formula applied to the tuple, True flows out exactly when the formula is satisfiable, so 1-CFA is NP-hard (Theorems 8 and 9 of the thesis). The theorem above makes this tight.

## Tightness

The upper bound of part 1 cannot be lowered to polynomial time, by the corollary. The jump from $k = 0$ to $k = 1$ is real: 0-CFA is in polynomial time. The bound uses fixed $k$. If the contour length grows with the program, the count of environments $(n^{k})^{n}$ grows too, and Van Horn notes that with exponential contour length the problem becomes doubly exponential. The hardness uses a nonlinear variable and closures with many free variables. Without free variables in closures, or with flat environments, the problem is polynomial.

## History

Shivers defined the k-CFA hierarchy in 1988 and 1991. Since the number of contours is polynomial for fixed $k$, k-CFA with small $k$ was often taken to be polynomial. Van Horn and Mairson showed in 2007 that 0-CFA is PTIME-complete, and in 2008 that k-CFA is EXPTIME-complete for every $k \ge 1$. Van Horn's 2009 thesis collects these results. In 2010, Might, Smaragdakis and Van Horn explained why k-CFA style analyses of Java are polynomial, and introduced m-CFA.

## References
