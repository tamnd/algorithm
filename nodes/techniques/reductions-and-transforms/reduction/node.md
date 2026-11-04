---
tag: X0KSM7
kind: technique
slug: reduction
name: Reduction
aliases:
- problem reduction
- reducing one problem to another
area: techniques/reductions-and-transforms
level: intro
summary: Solving a problem by transforming its instances into instances of a problem already solved, then mapping the answer back.
prereqs: [decision-problem, polynomial-time]
see_also: [polynomial-time-reduction, many-one-reducibility, turing-reduction, transitivity-of-reductions, reductions-for-algorithms, reduction-lower-bound, np-hardness-reductions, polynomial-time-equivalence]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 34.3, NP-completeness and reducibility (reductions, the lemma that A reducible to B and B in P gives A in P)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 8.1, Polynomial-time reductions (reductions with a black box for the other problem, the two uses, transitivity)
  - paper: doi:10.1145/800157.805047
    title: "Stephen A. Cook, The complexity of theorem-proving procedures, Proceedings of the 3rd Annual ACM Symposium on Theory of Computing (STOC 1971), 151-158"
    locator: the reducibility defined with a query machine (a Turing reduction)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: "Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum, 1972, 85-103"
    locator: the definition of polynomial-time (many-one) reducibility and the chain of reductions from satisfiability
  - paper: doi:10.1016/0304-3975(75)90016-X
    title: "Richard E. Ladner, Nancy A. Lynch and Alan L. Selman, A comparison of polynomial time reducibilities, Theoretical Computer Science 1(2) (1975), 103-123"
    locator: the definitions of many-one and Turing reducibility in polynomial time and their comparison
---

A reduction from a problem $A$ to a problem $B$ is a method that solves $A$ with the help of any algorithm for $B$: it transforms an instance of $A$ into one or more instances of $B$, and maps the answers back to an answer for $A$. A reduction is used in two directions. Read forward, it turns an algorithm for $B$ into an algorithm for $A$ ([reductions for algorithms](/reductions-for-algorithms/)). Read backward, it shows that $B$ is hard when $A$ is known or believed to be hard ([NP-hardness reductions](/np-hardness-reductions/), [lower bounds by reduction](/reduction-lower-bound/)).

## In plain words

You have a new task, and you already own a machine that does some other task. A reduction is a recipe that rewrites your task as a job for the machine, runs the machine, and reads your answer off its output. If the rewriting and the reading are cheap, your task is at most as hard as the machine's task.

The recipe works in both directions. If the machine is fast, you now have a fast way to do your task. If your task is known to be hard, the machine's task must be hard as well, since otherwise the recipe would make your task easy.

Two kinds of recipe are common. In the strict kind, the machine runs once and its yes or no answer is your answer. In the free kind, you may run the machine many times and do any cheap work between the runs.

## When it applies

- A new problem looks like a known problem after a change of view: a graph built from the input, a sorted copy of the input, a negation of the weights, a complement of a set.
- You need an algorithm and a well-studied problem (sorting, shortest paths, maximum flow, linear programming, satisfiability) has a fast solver.
- You need evidence that a problem has no fast algorithm. Then reduce a problem that is believed hard, such as [3-SAT](/3-sat/), to it.
- You want to compare two problems. Reductions in both directions show that they have the same complexity ([polynomial-time equivalence](/polynomial-time-equivalence/)).

## The template

Let $A$ and $B$ be problems. An instance $x$ has a size $|x|$, the length of its encoding. A reduction of $A$ to $B$ is an algorithm SOLVE-A that may call a procedure SOLVE-B as a black box. The black box returns a correct answer for each instance of $B$ that it gets.

```pseudo id=main
SOLVE-A(x)                        ▷ x an instance of A
L1  y ← TRANSFORM(x)                ▷ an instance of B
L2  z ← SOLVE-B(y)                  ▷ the black box for B
L3  return RECOVER(x, y, z)         ▷ an answer for x
```

The holes are TRANSFORM, which builds the instance $y$, and RECOVER, which turns the answer $z$ for $y$ into an answer for $x$. The reduction is correct when, for every instance $x$ of $A$ and every correct answer $z$ for $y$, RECOVER returns a correct answer for $x$. The cost of the reduction is the cost of TRANSFORM and RECOVER, without the cost of the call. The template has one call; the general form below allows several.

### Many-one and Turing reductions

For decision problems the two standard forms have exact definitions. A [decision problem](/decision-problem/) is a set $A \subseteq \{0,1\}^*$ of yes-instances.

*Many-one reduction* ([polynomial-time reduction](/polynomial-time-reduction/), also Karp reduction). $A \le_m^p B$ when a function $f : \{0,1\}^* \to \{0,1\}^*$, computable in time polynomial in $|x|$, satisfies

$$x \in A \iff f(x) \in B \qquad \text{for every } x \in \{0,1\}^*.$$

This is the template with TRANSFORM $= f$, one call, and RECOVER returns $z$ unchanged. Karp (1972) used this form for his list of NP-complete problems.

*Turing reduction* ([Turing reduction](/turing-reduction/), also Cook reduction). $A \le_T^p B$ when an [oracle Turing machine](/oracle-turing-machine/) $M$ decides $A$ in time polynomial in $|x|$ when it has an oracle for $B$. The machine may ask any number of questions "is $q \in B$?", may choose each question after it sees the earlier answers, and may combine the answers in any way. Writing a question of length $\ell$ costs $\ell$ steps, and the answer comes in one step. Cook (1971) defined his reducibility in this way.

A many-one reduction is a Turing reduction that asks exactly one question and returns its answer: the machine computes $f(x)$, asks the oracle, and copies the answer. So $A \le_m^p B$ implies $A \le_T^p B$.

### What a reduction transfers

**Lemma 1.** If $A \le_m^p B$ and $B \in$ [P](/p/), then $A \in$ P. The same holds for $\le_T^p$.

*Proof.* Let $f$ run in time at most $p(n)$ and let an algorithm decide $B$ in time at most $q(m)$, with $p$ and $q$ non-decreasing polynomials. A machine writes at most one output symbol in each step, so $|f(x)| \le p(|x|)$. To decide $x$, compute $f(x)$ and run the algorithm for $B$ on it. The time is at most $p(n) + q(p(n))$, a polynomial in $n$. For a Turing reduction that runs in time $p(n)$, there are at most $p(n)$ questions, each of length at most $p(n)$. Replace each answer of the oracle by a run of the algorithm for $B$. The time is at most $p(n) + p(n)\, q(p(n))$, again a polynomial. $\square$

The contrapositive is the hardness direction: if $A \le_m^p B$ and $A \notin$ P, then $B \notin$ P. This is how [NP-hardness reductions](/np-hardness-reductions/) are used. A problem $B$ is [NP-hard](/np-hard/) when $A \le_m^p B$ for every $A \in$ [NP](/np/), and to show it for a new $B$ it is enough to reduce one known NP-hard problem to $B$, by Lemma 2.

**Lemma 2 (transitivity).** If $A \le_m^p B$ and $B \le_m^p C$, then $A \le_m^p C$. The same holds for $\le_T^p$.

*Proof.* Let $f$ reduce $A$ to $B$ in time $p(n)$ and $g$ reduce $B$ to $C$ in time $q(m)$. Then $x \in A \iff f(x) \in B \iff g(f(x)) \in C$, and $g \circ f$ runs in time at most $p(n) + q(p(n))$, since $|f(x)| \le p(n)$. For Turing reductions, run the machine for $A$ and answer each of its questions to $B$ by a run of the machine for $B$, which asks its own questions to $C$. The proof of Lemma 1 bounds the time by $p(n) + p(n)\, q(p(n))$. $\square$

The page [transitivity of reductions](/transitivity-of-reductions/) states this as a theorem. Lemma 2 is why one reduction from a known NP-complete problem is enough: the chain of reductions from all of NP passes through it.

### The two forms are different in power

Every problem $A$ Turing reduces to its complement $\bar{A}$: ask whether $x \in \bar{A}$ and return the opposite answer. So $\overline{\mathrm{SAT}} \le_T^p \mathrm{SAT}$. A many-one reduction cannot flip the answer, and $\overline{\mathrm{SAT}} \le_m^p \mathrm{SAT}$ would give NP $=$ [co-NP](/co-np/).

*Proof.* Suppose $\overline{\mathrm{SAT}} \le_m^p \mathrm{SAT}$ by $g$. Let $L \in$ co-NP. Then $\bar{L} \in$ NP, so $\bar{L} \le_m^p \mathrm{SAT}$ by some $f$ ([Cook-Levin theorem](/cook-levin-theorem/)). The same $f$ gives $x \in L \iff f(x) \in \overline{\mathrm{SAT}}$, so $L \le_m^p \overline{\mathrm{SAT}} \le_m^p \mathrm{SAT}$. A problem that many-one reduces to a problem in NP is in NP: the certificate for $g(f(x))$ is a certificate for $x$. So co-NP $\subseteq$ NP. If $L \in$ NP, then $\bar{L} \in$ co-NP $\subseteq$ NP, so $L \in$ co-NP. Hence NP $=$ co-NP. $\square$

Turing reductions do not separate a problem from its complement, so NP and co-NP look the same under them. This is one reason why NP-completeness is defined with many-one reductions. Ladner, Lynch and Selman (1975) compare these and other polynomial-time reducibilities.

## Classic examples

### Cyclic rotation to substring search

A string $x$ is a rotation of a string $y$ when $y = uv$ and $x = vu$ for some strings $u, v$. Claim: $x$ is a rotation of $y$ if and only if $|x| = |y|$ and $x$ occurs in $yy$.

*Proof.* If $y = uv$ and $x = vu$, then $yy = u\,vu\,v$ holds $x$ at position $|u|$. Conversely, let $|x| = |y| = n$ and let $x$ occur in $yy$ at position $i$. Since $|yy| = 2n$, $0 \le i \le n$. Put $u = y[0..i)$ and $v = y[i..n)$. Then $yy[i..i+n) = v\,u$, so $x = vu$. $\square$

TRANSFORM builds $yy$ in $O(n)$ time, SOLVE-B is [string matching](/string-matching/), for example [Knuth-Morris-Pratt](/knuth-morris-pratt/) in $O(n)$ time, and RECOVER returns the answer. For $y = \texttt{abcde}$ and $x = \texttt{cdeab}$, $yy = \texttt{abcdeabcde}$ holds $x$ at position $2$ (counted from $0$), so $u = \texttt{ab}$ and $v = \texttt{cde}$. This is a many-one reduction with total time $O(n)$.

### Element distinctness to sorting

Sort the items, then compare each item with the next one. The items are distinct if and only if no two neighbours are equal. The page [presorting](/presorting/) gives this example in full, [reduction to sorting](/reduction-to-sorting/) gives reductions that sort a transformed input, and [reductions for algorithms](/reductions-for-algorithms/) gives more reductions used to design algorithms, with their costs.

### Search to decision

To find a satisfying assignment of a formula with $n$ variables from a black box that only answers "satisfiable or not", fix the variables one at a time and keep each value for which the black box still says yes. This makes at most $n + 1$ calls, each on a formula no longer than the input. It is a Turing reduction from the search problem to the decision problem: it makes many calls and chooses each call from the earlier answers. See [search-to-decision reduction](/search-to-decision-reduction/) and [self-reducibility](/self-reducibility/).

### 3-SAT to independent set (hardness)

A formula with $k$ clauses of three literals becomes a graph with one triangle for each clause and an edge between each pair of opposite literals $x_i$ and $\neg x_i$. The formula is satisfiable if and only if the graph has an [independent set](/independent-set/) of size $k$ (Kleinberg and Tardos, Section 8.2). This is a many-one reduction, used backward: since 3-SAT is NP-complete, independent set is NP-hard. See [NP-hardness reductions](/np-hardness-reductions/).

### Sorting to convex hull (lower bound)

The points $(x_i, x_i^2)$ lie on a parabola, and their hull in order lists the $x_i$ in sorted order. Read backward inside the algebraic computation tree model, this gives an $\Omega(n \log n)$ lower bound for the hull. The page [lower bounds by reduction](/reduction-lower-bound/) has the proof and the model conditions.

## Variations

- **Polynomial-time reductions** are the standard in complexity theory, in the many-one form ([many-one reducibility](/many-one-reducibility/)) or the Turing form.
- **Fine-grained reductions** keep track of exact exponents, such as $n^{2 - \delta}$, instead of "any polynomial". See [fine-grained reduction](/fine-grained-reduction/).
- **Reductions that keep more structure.** A [parsimonious reduction](/parsimonious-reduction/) keeps the number of solutions. A [Levin reduction](/levin-reduction/) also maps solutions back and forth. An [approximation-preserving reduction](/approximation-preserving-reduction/) keeps the quality of approximate answers.
- **Reductions with a weak machine.** Inside P, polynomial-time reductions are too strong to tell problems apart: every problem in P many-one reduces to every problem that has at least one yes-instance and one no-instance (see [polynomial-time equivalence](/polynomial-time-equivalence/)). Logarithmic-space reductions are used there instead.
- **Reductions to a general solver.** Many problems reduce to one general problem with a strong solver, such as [linear programming](/reduction-to-linear-programming/) or SAT.

## Pitfalls

- **The wrong direction.** "$A$ reduces to $B$" means $A$ is solved with $B$. To prove that $B$ is hard, reduce a hard problem to $B$, not $B$ to a hard problem. Reducing [2-SAT](/2-sat/) to SAT proves nothing about 2-SAT.
- **A one-way correctness proof.** A many-one reduction needs both $x \in A \Rightarrow f(x) \in B$ and $f(x) \in B \Rightarrow x \in A$. Most wrong NP-hardness proofs check only the first.
- **A reduction that does the work.** If TRANSFORM or RECOVER already costs as much as solving $A$ directly, the reduction says nothing about $B$ and gives no speed-up for $A$.
- **Size blow-up.** The cost of the call depends on the size of $y$, not of $x$. A transform from size $n$ to size $n^2$ turns an $O(m)$ solver for $B$ into an $O(n^2)$ algorithm for $A$.
- **Numbers in unary.** A transform that writes a number $W$ in unary, or builds a table of $W$ entries, is not polynomial in the input size, which counts the $\log W$ bits of $W$.
- **Many-one and Turing mixed up.** A Turing reduction does not show NP-hardness in the sense of many-one reductions, and it cannot tell NP from co-NP, as shown above.

## Exercises

1. Give a many-one reduction from "does the graph $G$ have a [clique](/clique/) of size $k$" to "does the graph $H$ have an independent set of size $k$", and prove both directions.
2. Prove that $A \le_m^p B$ if and only if $\bar{A} \le_m^p \bar{B}$, where the bar is the complement.
3. Reduce "is the string $x$ a palindrome" to string equality, and give the cost of the reduction.
4. A transform runs in time $O(n^2)$ and builds an instance of size $O(n^{1.5})$ for a problem solved in time $O(m^2)$. Give the time of the combined algorithm.
5. Write the search-to-decision reduction for SAT in full, and prove that it makes at most $n + 1$ calls.

## References
