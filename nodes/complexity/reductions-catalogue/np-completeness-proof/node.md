---
tag: W1RSQ7
kind: technique
slug: np-completeness-proof
name: NP-completeness proof
aliases:
- reduction-based hardness proof
area: complexity/reductions-catalogue
level: core
summary: The recipe for proving a problem NP-complete. Show it is in NP, then give a polynomial-time reduction from a known NP-complete problem and prove both directions.
prereqs: [np-complete, polynomial-time-reduction, transitivity-of-reductions]
see_also: [gadget-reduction, np-hardness-reductions, cook-levin-theorem, karps-21-np-complete-problems, garey-johnson-compendium, strong-np-hardness, co-np-complete, np-hard]
sources:
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 4th edition, MIT Press, 2022
    locator: Section 34.4, NP-completeness proofs (the five-step method)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 2.5, Polynomial Transformations and NP-Completeness, and Chapter 3, Proving NP-Completeness Results
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, 3rd edition, Cengage Learning, 2013
    locator: Sections 7.4 and 7.5, NP-completeness and additional NP-complete problems
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: "Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (eds.), Complexity of Computer Computations, Plenum Press, 1972, 85-103"
    locator: the first large set of NP-completeness proofs by reduction from satisfiability
---

An NP-completeness proof shows that a decision problem $L$ is [NP-complete](/np-complete/) in two parts: $L$ is in NP, and a known NP-complete problem $K$ has a [polynomial-time reduction](/polynomial-time-reduction/) to $L$. By [transitivity](/transitivity-of-reductions/), every problem in NP then reduces to $L$. The reduction part has four obligations: define the map, bound its cost, show that yes-instances go to yes-instances, and show that an arbitrary yes-instance in the image comes from a yes-instance. Cormen, Leiserson, Rivest and Stein give the recipe as five steps (Section 34.4), and Garey and Johnson (Section 2.5 and Chapter 3) use the same method.

## In plain words

To show that a new problem is as hard as the hardest problems with easily checked answers, you do two things. First, show that a proposed answer to your problem can be checked quickly. Second, take a problem already known to be that hard and show how to rewrite any of its questions, quickly, as a question about your problem with the same answer. If your problem had a fast method, the known hard problem would have one too. The rewriting must be correct both ways: a yes must turn into a yes, and a yes on your side must come only from a yes on the other side. Most mistakes are in that second part, or in rewriting in the wrong direction.

## When it applies

Use the recipe when $L$ is a decision problem, a set of strings, and you believe that it is in NP and that no polynomial-time algorithm exists. If $L$ is an optimization or search problem, state its decision version first ("is there a solution of value at least $k$?") and prove that version NP-complete; the original problem is then [NP-hard](/np-hard/). If you cannot show membership in NP, stop after the reduction: the result is NP-hardness. The recipe needs at least one problem already known to be NP-complete. The first one, SAT, comes from the [Cook-Levin theorem](/cook-levin-theorem/), which reduces every NP problem to SAT directly.

## The template

```pseudo id=template
PROVE-NP-COMPLETE(L)
L1  give a certificate c and a verifier V(x, c) for L    ▷ hole: membership in NP
L2  choose a known NP-complete problem K                 ▷ hole: the source
L3  define f from instances of K to instances of L       ▷ hole: the construction
L4  bound the time to compute f, and so |f(x)|
L5  prove: x ∈ K ⇒ f(x) ∈ L                              ▷ map a witness of x forward
L6  prove: f(x) ∈ L ⇒ x ∈ K                              ▷ from an arbitrary witness of f(x)
L7  conclude: K ≤ L and L ∈ NP, so L is NP-complete
```

The holes are the certificate and verifier, the source $K$, and the map $f$.

**Line L1 (membership).** Give the certificate, bound its length by a polynomial in $|x|$, and describe a deterministic verifier that runs in polynomial time and accepts some certificate exactly for the yes-instances.

**Line L2 (the source).** Pick $K$ close in structure to $L$: [3-SAT](/3-sat/) for problems with binary choices and local constraints, [3-dimensional matching](/three-dimensional-matching/) or [exact cover by 3-sets](/exact-cover-by-3-sets/) for packing and partition, [vertex cover](/vertex-cover/) or [clique](/clique-problem/) for graph selection, [Hamiltonian cycle](/hamiltonian-cycle-problem/) for orderings, and [partition](/partition-problem/) or [subset sum](/subset-sum-problem/) for numbers. The [Garey and Johnson compendium](/garey-johnson-compendium/) lists sources by problem type.

**Line L3 (the construction).** The three common methods are restriction, local replacement and component design; see [elementary NP-hardness reductions](/np-hardness-reductions/) and [gadget reduction](/gadget-reduction/).

**Lines L5 and L6 (the two directions).** L5 maps a witness of $x$ to a witness of $f(x)$. L6 must start from *any* witness of $f(x)$, not only from those produced by L5, and build a witness of $x$. When both maps are polynomial-time, the reduction is also a [Levin reduction](/levin-reduction/).

**Why it works.** For any $A \in$ NP, $A \le_m^p K$ since $K$ is NP-complete, and $K \le_m^p L$ by L3 to L6. Transitivity gives $A \le_m^p L$, so $L$ is NP-hard, and L1 puts it in NP.

## Classic examples

### A worked proof: DOUBLE-SAT

Let DOUBLE-SAT be the set of CNF formulas with at least two satisfying assignments.

- **L1.** The certificate is a pair of distinct assignments. Its length is twice the number of variables, and the verifier checks that they differ and that each satisfies every clause, in time linear in the size of the formula.
- **L2.** Take $K = $ SAT.
- **L3.** Map $\varphi$ over variables $x_1, \ldots, x_n$ to $f(\varphi) = \varphi \land (z \lor \neg z)$, where $z$ is a new variable.
- **L4.** $f$ copies $\varphi$ and appends one clause, so it runs in linear time and $|f(\varphi)| = |\varphi| + O(\log n)$ (the name of $z$).
- **L5.** If $a$ satisfies $\varphi$, then $(a, z = 0)$ and $(a, z = 1)$ are two distinct satisfying assignments of $f(\varphi)$, because $z$ appears in no clause of $\varphi$ and the clause $(z \lor \neg z)$ is always true.
- **L6.** If $f(\varphi)$ has at least two satisfying assignments, take any one of them, $b$. Every clause of $\varphi$ is a clause of $f(\varphi)$, so $b$ restricted to $x_1, \ldots, x_n$ satisfies $\varphi$.

For $\varphi = (x_1 \lor x_2 \lor \neg x_3) \land (\neg x_1 \lor x_2 \lor x_3) \land (\neg x_1 \lor \neg x_2 \lor \neg x_3)$: the witness $x_1 x_2 x_3 = 110$ maps forward to the two assignments $110$ with $z = 0$ and $110$ with $z = 1$. In the other direction, the witness pair ($011$ with $z = 1$, $000$ with $z = 0$) of $f(\varphi)$ maps back to $011$, which satisfies $\varphi$. The formula has $5$ satisfying assignments and its image has $10$. On all $2951$ formulas made of $1$ to $3$ distinct clauses of width $1$ to $3$ over three variables, $\varphi$ is satisfiable exactly when $f(\varphi)$ has at least two satisfying assignments.

### Other classic proofs

- **[Clique](/clique-problem/)** from 3-SAT: one vertex per literal occurrence, edges between compatible occurrences in different clauses, and $k = m$. This is the complement of the independent set graph on [polynomial-time reduction](/polynomial-time-reduction/).
- **[Vertex cover](/vertex-cover/)** from 3-SAT by component design, worked with numbers on [gadget reduction](/gadget-reduction/).
- **[Traveling salesman (decision)](/traveling-salesman-decision/)** from Hamiltonian cycle by restriction: edges cost $1$, non-edges cost $2$, and the bound is $n$. On a $5$-vertex house graph the cheapest tour costs $5$, so the answer is yes; on the $5$-vertex bowtie graph (two triangles sharing a vertex) it costs $6$, so the answer is no.
- The full list from Karp's paper is on [Karp's 21 NP-complete problems](/karps-21-np-complete-problems/).

## Variations

- **NP-hardness only.** For problems not known to be in NP, or not decision problems, prove L2 to L6 and skip L1. Garey and Johnson (Chapter 5) use [Cook reductions](/turing-reduction/) for this.
- **Strong NP-completeness.** For problems with numbers, reduce from a [strongly NP-hard](/strong-np-hardness/) source such as [3-partition](/three-partition/) and keep all numbers bounded by a polynomial in the input size. This rules out pseudo-polynomial algorithms unless P = NP.
- **Restricted inputs.** To show that $L$ stays hard on planar graphs, cubic graphs or other special inputs, check that $f$ produces only such inputs, or add a gadget step that converts to them.
- **coNP-completeness.** Reduce from a [coNP-complete](/co-np-complete/) problem such as TAUT and show membership in coNP. By the complement property of Karp reductions, the same $f$ shows the complement of $L$ NP-complete.
- **Other classes.** The same recipe with other reductions gives completeness for other classes, for example [logspace](/logspace/) reductions for NL and P, and parsimonious reductions for counting classes.

## Pitfalls

- **The wrong direction.** Reducing $L$ to SAT shows that $L$ is in NP, not that it is hard. The reduction must go *from* the known hard problem *to* $L$.
- **One direction only.** Showing L5 without L6 proves nothing. Every map sends yes to yes if it sends everything to one fixed yes-instance.
- **L6 from a special witness.** A proof of L6 that assumes the witness of $f(x)$ has the shape built in L5 is incomplete. Start from an arbitrary witness and show that it has, or can be put into, a useful shape.
- **Exponential output.** A map that writes numbers in unary, or that lists all subsets, all assignments or all paths, is not polynomial. Bound $|f(x)|$ in L4 with the numbers in binary.
- **Membership forgotten or wrong.** Optimization problems are not in NP as stated, and some decision problems are not known to be in NP (for example, "is this the shortest tour?"). Then the result is NP-hardness, not NP-completeness.
- **Overclaiming.** NP-completeness does not show that no polynomial-time algorithm exists. It shows that one exists only if P = NP. Whether P equals NP is open ([P versus NP](/p-versus-np-problem/)).

## Exercises

1. Prove that the set of graphs with a clique of size at least half the number of vertices is NP-complete. Hint: pad the graph from CLIQUE with isolated or universal vertices.
2. Let SAT-DIFF be the set of pairs of CNF formulas $(\varphi, \psi)$ on the same variables for which some assignment satisfies $\varphi$ but not $\psi$. Show that it is NP-complete.
3. Show that HAMILTONIAN PATH is NP-complete by a reduction from [Hamiltonian cycle](/hamiltonian-cycle-problem/). Check L6 from an arbitrary path.
4. Find the error: "To prove that SUBSET SUM is NP-complete, reduce it to 3-SAT by writing the sum as a Boolean circuit."

## References
