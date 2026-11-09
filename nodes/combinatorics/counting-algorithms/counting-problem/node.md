---
tag: MV23GB
kind: concept
slug: counting-problem
name: Counting problem
aliases:
- enumeration problem
- '#-problem'
- '#P problem'
area: combinatorics/counting-algorithms
level: intro
summary: Computing how many objects satisfy a given property.
prereqs: [rule-of-sum, rule-of-product]
see_also: [enumeration-problem, decision-problem, search-problem, permanent-computation, counting-perfect-matchings, counting-spanning-trees, fpras, model-counting]
sources:
  - paper: doi:10.1016/0304-3975(79)90044-6
    title: Leslie G. Valiant, The complexity of computing the permanent, Theoretical Computer Science 8(2), 189 to 201 (1979)
    locator: the definition of the class #P and the #P-completeness of the permanent of a 0-1 matrix
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 17, Complexity of counting (#P, #P-completeness of the permanent, Toda's theorem)
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 1, Section 1.1, How to count (what it means to count, and the forms an answer can take)
  - paper: doi:10.1145/1008731.1008738
    title: Mark Jerrum, Alistair Sinclair and Eric Vigoda, A polynomial-time approximation algorithm for the permanent of a matrix with nonnegative entries, Journal of the ACM 51(4), 671 to 697 (2004)
    locator: the main theorem (an FPRAS for the permanent of a nonnegative matrix)
---

A counting problem asks for the number of solutions of an instance, not for one solution: how many subsets of a set have size $k$, how many perfect matchings a graph has, how many assignments satisfy a formula. Formally, it is a function $x \mapsto |S(x)|$, where $S(x)$ is a finite set of solutions defined by the input $x$. Counting is at least as hard as deciding whether a solution exists, and sometimes much harder: deciding whether a bipartite graph has a perfect matching takes polynomial time, but counting its perfect matchings is #P-complete. The pages of this area solve counting problems with closed forms, recurrences and [dynamic programming](/dp-on-dag/), [inclusion-exclusion](/inclusion-exclusion-principle/), [generating functions](/generating-functions/) and determinants.

## In plain words

Some questions ask "is there one?", for example "can this set of coins pay exactly 50 cents?". A counting question asks "how many are there?", for example "in how many ways can these coins pay 50 cents?". The answer is a number, and it can be very large even for a small input.

To count, you rarely list all the solutions. A list can be far too long. Instead, you find a formula, or you split the solutions into groups and count each group, or you count the wrong objects and subtract them. Some counting questions have fast methods. For others, no fast exact method is known, and the best practical answer is a good estimate.

## The idea

**Definition.** Let $\Sigma^*$ be the set of finite strings. A counting problem is given by a relation $R \subseteq \Sigma^* \times \Sigma^*$ with finite sets $S_R(x) = \{y : (x, y) \in R\}$. The problem is to compute the function

$$\#R(x) = |S_R(x)|.$$

The class #P (Valiant, 1979) holds the functions $\#R$ for the relations $R$ that are checkable in polynomial time and have solutions of length polynomial in $|x|$. These are the counting versions of the problems in [NP](/np/). A function $f$ is #P-complete if $f \in$ #P and every function in #P reduces to $f$ in polynomial time, usually by a [parsimonious reduction](/parsimonious-reduction/) that keeps the number of solutions.

**Related problems on the same set $S(x)$.**

| problem | output | example for "$k$-subsets of $[n]$" |
|---|---|---|
| [decision](/decision-problem/) | whether $S(x) \ne \emptyset$ | yes when $0 \le k \le n$ |
| [search](/search-problem/) | one element of $S(x)$ | $\{1, \ldots, k\}$ |
| counting | $\lvert S(x) \rvert$ | $\binom{n}{k}$ |
| [enumeration](/enumeration-problem/) | all of $S(x)$, each once | the $\binom{n}{k}$ subsets |
| sampling | a uniform random element of $S(x)$ | a random $k$-subset |

Counting gives decision for free: $S(x) \ne \emptyset$ if and only if $\#R(x) \ge 1$. Enumeration gives counting in time $\Omega(|S(x)|)$, which is exponential for most problems, so a good counting algorithm must count without listing. For self-reducible problems, counting and uniform sampling are equivalent up to polynomial factors, even in their approximate forms (Jerrum, Valiant and Vazirani; see the [JVV theorem](/jerrum-valiant-vazirani-theorem/)).

**The output and its cost.** The answer can have many digits. For the subsets of size $n/2$ of an $n$-set, the count $\binom{n}{n/2}$ has about $n$ bits. So "polynomial time" for a counting problem means polynomial in the input length, with arithmetic on numbers of polynomial bit length. A program then works in one of three regimes:

- **exact big integers**, with a bit cost for each operation (see [arbitrary-precision arithmetic](/arbitrary-precision-arithmetic/));
- **residues modulo a prime $p$**, with $O(1)$ cost per operation on a word RAM when $p$ fits in a word, which is the usual setting of programming contests (see [modular inverse](/modular-inverse/) and [Lucas's theorem](/lucas-theorem/));
- **approximate counts**, with a relative error $\varepsilon$ and a failure probability $\delta$. A fully polynomial randomized approximation scheme ([FPRAS](/fpras/)) runs in time polynomial in $|x|$, $1/\varepsilon$ and $\log(1/\delta)$.

**The main methods.**

- A **closed form** from a bijection or from the [rule of product](/rule-of-product/): $\binom{n}{k}$, $n^{n-2}$ labeled trees, the [Catalan numbers](/catalan-numbers/).
- A **recurrence** from a case split by the [rule of sum](/rule-of-sum/), evaluated by dynamic programming: [Pascal's triangle](/pascal-triangle-dp/), [counting subset sums](/counting-subset-sum/), paths in a DAG.
- **[Inclusion-exclusion](/inclusion-exclusion-principle/)** and **[Möbius inversion](/mobius-inversion/)**, when it is easier to count objects that break some conditions.
- **[Generating functions](/generating-functions/)** and the **[transfer matrix method](/transfer-matrix-method/)**, for families with a recursive or a finite-state structure.
- **Determinants**, which take polynomial time: the [matrix-tree theorem](/matrix-tree-theorem/) for spanning trees, the [Kasteleyn method](/kasteleyn-method/) for perfect matchings of planar graphs, the [Lindström, Gessel and Viennot lemma](/lindstrom-gessel-viennot-lemma/) for non-crossing paths.

## Examples

**1. A closed form.** The number of $k$-subsets of $[n]$ is $\binom{n}{k}$. For $n = 10$, $k = 5$ it is 252, and a program computes it with $O(k)$ arithmetic operations; see [computing binomial coefficients](/binomial-coefficient-computation/).

**2. Easy decision, hard counting.** A bipartite graph with parts $\{u_1, \ldots, u_n\}$ and $\{v_1, \ldots, v_n\}$ has the 0-1 matrix $M$ with $M_{ij} = 1$ if $u_i v_j$ is an edge. Its perfect matchings correspond to the permutations $\pi$ with $M_{i\pi(i)} = 1$ for all $i$, so their number is the permanent $\sum_\pi \prod_i M_{i\pi(i)}$. For the ladder graph of the 2 by 4 grid, with

$$M = \begin{pmatrix} 1 & 1 & 0 & 0 \\ 1 & 1 & 1 & 0 \\ 0 & 1 & 1 & 1 \\ 0 & 0 & 1 & 1 \end{pmatrix},$$

the permanent is 5, the number of domino tilings of a 2 by 4 board. [Hopcroft and Karp](/hopcroft-karp/) decides whether a perfect matching exists in polynomial time, but computing the permanent of a 0-1 matrix is #P-complete (Valiant, 1979). The best known exact method, [Ryser's formula](/ryser-formula/), takes $O(2^n n)$ time. Jerrum, Sinclair and Vigoda (2004) gave an FPRAS for the permanent of a nonnegative matrix. See [permanent computation](/permanent-computation/) and [counting perfect matchings](/counting-perfect-matchings/).

**3. Easy for a determinant.** The complete graph $K_4$ has $4^{4-2} = 16$ spanning trees. For a general graph, the [matrix-tree theorem](/matrix-tree-theorem/) gives the count as a determinant of the reduced Laplacian, in $O(n^3)$ arithmetic operations. See [counting spanning trees](/counting-spanning-trees/).

**4. Pseudo-polynomial counting.** The number of subsets of a list of $n$ positive integers with sum $t$ is computed by a table of $O(nt)$ entries. This is polynomial in $n$ and in the value $t$, but not in the number of bits of $t$; see [counting subset sums](/counting-subset-sum/).

**5. Counting satisfying assignments.** Counting the satisfying assignments of a CNF formula ([model counting](/model-counting/), #SAT) is #P-complete. For a DNF formula, the decision is easy and the exact count is still #P-complete, but the [Karp and Luby algorithm](/karp-luby-algorithm/) gives an FPRAS; see [DNF counting](/dnf-counting/).

## Where it is used

- **Analysis of algorithms.** The average cost of an algorithm over all inputs of size $n$ is a sum divided by a count, for example the number of [inversions](/counting-inversions/) over the $n!$ permutations.
- **Probability.** On a finite space with uniform outcomes, a probability is a count divided by a count, as in the [ballot theorem](/ballot-theorem/) and the [birthday paradox](/birthday-paradox/).
- **Lower bounds.** The [counting argument](/counting-argument/) compares the number of inputs with the number of behaviors of an algorithm.
- **Generation.** A counting algorithm for a family gives [ranking and unranking](/combinatorial-ranking-and-unranking/) and uniform random generation of its members.
- **Complexity theory.** #P sits above the polynomial hierarchy: [Toda's theorem](/toda-theorem/) says that $\mathrm{PH} \subseteq \mathrm{P}^{\#\mathrm{P}}$.
- **Statistical physics and reliability.** Partition functions, network reliability and the number of colorings are weighted counting problems, often #P-hard, and are attacked with [approximate counting](/approximate-counting/).

## References
