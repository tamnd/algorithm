---
tag: ZPR256
kind: technique
slug: transfer-matrix-method
name: Transfer-matrix method
aliases:
- transfer matrix
- transfer-matrix counting
area: combinatorics/counting-algorithms
level: advanced
summary: Counts configurations on a chain by powers of a transition matrix.
prereqs: [generating-functions, adjacency-matrix, matrix-power]
see_also: [counting-fixed-length-paths, matrix-exponentiation, broken-profile-dp, linear-recurrence-nth-term, generating-functions, symbolic-method, kasteleyn-method, determinant]
sources:
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Chapter 4, Section 4.7, The transfer-matrix method
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter V, Applications of rational and meromorphic asymptotics (regular specifications, finite automata and transfer matrices)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 7.1, Domino Theory and Change (the 3 by n domino tilings)
---

The transfer-matrix method counts objects that are built one step at a time, when each step depends only on a finite state left by the step before. The states and the allowed steps form a directed graph with adjacency matrix $M$, and the number of objects of length $n$ is a sum of entries of the power $M^n$. The [generating function](/generating-functions/) of the counts is rational, with denominator $\det(I - zM)$, so the counts satisfy a linear recurrence. The method counts words that avoid a pattern, tilings and colorings of strips, and the states of lattice models in statistical physics.

## In plain words

Think of a machine with a few dials. You build an object piece by piece, and after each piece the dials show all that matters for the next piece. For strings that must avoid a bad pattern, the dials show how much of the pattern you have just written. For a tiling of a strip, they show which cells of the next column are already covered.

Write a table: for each dial setting and each next setting, how many pieces lead from one to the other. Then the number of objects of a given length is the number of ways to walk through this table for that many steps. Multiplying the table by itself does all the walks at once. The counts follow a fixed linear rule, so a program can find even a huge term fast.

## When it applies

- An object of length $n$ is a sequence of $n$ steps, and whether a step is allowed depends only on a bounded amount of history: the state.
- The number $d$ of states is small enough for a $d \times d$ matrix. For strips of width $k$ the state is often a subset of a column, so $d \le 2^k$, and only narrow strips are practical.
- Each object has exactly one walk through the states. The automaton is deterministic, or at least unambiguous.
- The question asks for a count for one large $n$, for all $n \le N$, for the rational generating function, or for the growth rate.

## The template

**Notation.** $V = \{1, \ldots, d\}$ is the set of states. $M$ is the $d \times d$ transfer matrix: $M_{ij}$ is the number (or total weight) of steps from state $i$ to state $j$. A *walk* of length $n$ is a sequence of $n$ steps, each from the state where the last one ended. $n$ is the length of the object.

**Theorem 1 (walks).** For every $n \ge 0$, the number of walks of length $n$ from state $i$ to state $j$ is $(M^n)_{ij}$.

*Proof.* By induction on $n$. For $n = 0$ the only walk is the empty walk from $i$ to $i$, and $(M^0)_{ij} = I_{ij}$. For $n \ge 1$, split the walks by the state $k$ after $n - 1$ steps. By the [rule of sum](/rule-of-sum/) and the [rule of product](/rule-of-product/), and the induction hypothesis, the count is $\sum_k (M^{n-1})_{ik} M_{kj} = (M^n)_{ij}$. $\square$

**Theorem 2 (rational series).** Let $F_{ij}(z) = \sum_{n \ge 0} (M^n)_{ij} z^n$. Then

$$F_{ij}(z) = \frac{(-1)^{i+j} \det\bigl((I - zM) \text{ without row } j \text{ and column } i\bigr)}{\det(I - zM)}.$$

The denominator is a polynomial of degree at most $d$ with constant term 1, and the numerator has degree at most $d - 1$.

*Proof.* As formal series with matrix coefficients, $(I - zM) \sum_{n \ge 0} z^n M^n = \sum_n z^n M^n - \sum_n z^{n+1} M^{n+1} = I$. So $\sum_n z^n M^n$ is the inverse of $I - zM$ over the ring of formal series. The determinant of $I - zM$ has constant term $\det I = 1$, so it is invertible as a series, and the adjugate formula $A^{-1} = \operatorname{adj}(A)/\det A$ holds over this ring. The $(i, j)$ entry of the adjugate is the signed minor given in the statement. Each entry of $I - zM$ has degree at most 1, so a minor of size $d - 1$ has degree at most $d - 1$, and the full [determinant](/determinant/) has degree at most $d$. $\square$

**Consequence.** By Theorem 2 or by the Cayley-Hamilton theorem, if $\det(xI - M) = x^d + c_1 x^{d-1} + \cdots + c_d$, then every entry sequence satisfies $a_n + c_1 a_{n-1} + \cdots + c_d a_{n-d} = 0$ for $n \ge d$. The same holds for any fixed combination $u^{\mathsf T} M^n v$, which is the usual form of a count: $u$ marks the start states and $v$ the accepting states.

```pseudo id=main
TRANSFER-COUNT(objects, n)
L1  choose the states: what a step must know about the past          ▷ hole: the state
L2  for each pair of states (s, t) do
L3      M[s, t] ← the number of steps that lead from s to t          ▷ hole: the steps
L4  u ← the start vector, v ← the end vector
L5  x ← u
L6  for i ← 1 to n do
L7      x ← x M                                                       ▷ x[t] = walks of length i that end in t
L8  return x · v
```

**Cost.** The loop of lines L6 and L7 makes $n$ products of a vector by a $d \times d$ matrix, so it takes $O(n d^2)$ operations, or $O(n e)$ with $e$ the number of nonzero entries, and it gives every count up to $n$ on the way. For one large $n$, compute $u^{\mathsf T} M^n v$ by [matrix exponentiation](/matrix-exponentiation/) in $O(d^3 \log n)$ operations, or find the recurrence of the consequence once and use the [Nth term of a linear recurrence](/linear-recurrence-nth-term/). Counts grow like $\lambda^n$, where $\lambda$ is the largest eigenvalue of $M$, so exact counts have $\Theta(n)$ bits when $\lambda > 1$, and each operation costs that much. Modulo a prime $p$, each operation is one word operation.

## Classic examples

**1. Strings that avoid a pattern.** Count the binary strings of length $n$ with no factor $101$. The state is the longest suffix of the string so far that is a prefix of $101$: $\varepsilon$, $1$ or $10$. The steps are $\varepsilon \xrightarrow{0} \varepsilon$, $\varepsilon \xrightarrow{1} 1$, $1 \xrightarrow{0} 10$, $1 \xrightarrow{1} 1$, $10 \xrightarrow{0} \varepsilon$, and $10 \xrightarrow{1}$ is forbidden. So

$$M = \begin{pmatrix} 1 & 1 & 0 \\ 0 & 1 & 1 \\ 1 & 0 & 0 \end{pmatrix}, \qquad u = (1, 0, 0), \qquad v = (1, 1, 1)^{\mathsf T}.$$

The vector $x$ of line L7 goes $(1,0,0)$, $(1,1,0)$, $(1,2,1)$, $(2,3,2)$, $(4,5,3)$, $(7,9,5)$, and the counts $x \cdot v$ for $n = 0$ to $11$ are $1, 2, 4, 7, 12, 21, 37, 65, 114, 200, 351, 616$ (OEIS A005251, shifted by 3). Here $\det(I - zM) = 1 - 2z + z^2 - z^3$, the generating function is $\frac{1 + z^2}{1 - 2z + z^2 - z^3}$, and $a_n = 2a_{n-1} - a_{n-2} + a_{n-3}$ for $n \ge 3$. The states are those of the [KMP automaton](/prefix-function/) of the pattern, which works for every pattern.

**2. Proper colorings of a cycle.** A proper $q$-coloring of the cycle $C_n$ with $n \ge 2$ is a closed walk of length $n$ in the complete graph $K_q$, whose adjacency matrix $J - I$ has the eigenvalue $q - 1$ once and $-1$ with multiplicity $q - 1$. So the count is $\operatorname{tr} (J - I)^n = (q - 1)^n + (-1)^n (q - 1)$. For $q = 3$ and $n = 3$ to $8$ this gives $6, 18, 30, 66, 126, 258$. The trace counts closed walks, so cyclic objects use $\operatorname{tr} M^n$ in place of $u^{\mathsf T} M^n v$.

**3. Domino tilings of a 3 by n strip (Concrete Mathematics, Section 7.1).** The state is the set of cells of the next column that horizontal dominoes already cover, a subset of 3 cells. The transfer matrix is $8 \times 8$, and the counts for $n = 0, 2, 4, \ldots, 12$ are $1, 3, 11, 41, 153, 571, 2131$ (OEIS A001835, shifted by 1); odd $n$ gives 0. The series is $\frac{1 - z^2}{1 - 4z^2 + z^4}$. This is the same computation as [broken profile dynamic programming](/broken-profile-dp/), which moves one cell at a time.

**4. Hard squares on a strip.** The independent sets of the $k \times n$ grid graph: the state is the set of chosen cells of a column, with no two adjacent, and two columns are compatible when they share no row. For $k = 2$ the counts for $n = 0$ to $8$ are $1, 3, 7, 17, 41, 99, 239, 577, 1393$ (OEIS A001333, shifted by 1). For $k = 3$ they are $1, 5, 17, 63, 227, 827, 2999$ (OEIS A051736). For width $k$ the number of states is $F_{k+2}$, a [Fibonacci number](/fibonacci-numbers/).

**5. Fibonacci numbers.** Strings with no two adjacent 1s have the states "last bit 0" and "last bit 1", and $M = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$. Its powers are $M^n = \begin{pmatrix} F_{n+1} & F_n \\ F_n & F_{n-1} \end{pmatrix}$, the [matrix form of the Fibonacci numbers](/matrix-fibonacci/).

## Variations

- **Steps of different lengths.** If a step from $s$ to $t$ adds $\ell$ to the size, put $z^\ell$ in the matrix entry. Theorem 2 still holds with $zM$ replaced by this matrix $M(z)$ of polynomials with no constant term.
- **Weights and parameters.** An entry may be a weight, or a polynomial in a second variable $u$ that marks a parameter, such as the number of 1s. Then $u^{\mathsf T} M^n v$ is the generating polynomial of that parameter.
- **Regular languages.** Every regular language has a deterministic automaton, so the transfer-matrix method shows that its counting series is rational. This is the regular part of the [symbolic method](/symbolic-method/).
- **Counting walks in a graph.** With $M$ the [adjacency matrix](/adjacency-matrix/) of a graph, Theorem 1 is the method of [counting fixed-length paths](/counting-fixed-length-paths/).
- **Profile methods.** For grids that are too wide for a full matrix, [broken profile DP](/broken-profile-dp/) adds one cell at a time and never forms $M$. For planar perfect matchings, the [Kasteleyn method](/kasteleyn-method/) replaces the matrix power by one Pfaffian.
- **Physics.** In the one-dimensional Ising model the transfer matrix is $2 \times 2$, and the partition function of a ring of $n$ spins is $\lambda_1^n + \lambda_2^n$.

## Pitfalls

- **A state that forgets too much.** For words that avoid $101$, the last letter alone is not a state: after $10$ the next $1$ is forbidden, but after $00$ it is allowed. Use the automaton of the pattern. Test: compare the counts with a brute force list of all $2^n$ strings for $n \le 12$.
- **An ambiguous automaton.** A nondeterministic automaton may accept one word along several walks, and $u^{\mathsf T} M^n v$ then counts walks, not words. Make the automaton deterministic first.
- **Paths and cycles.** $u^{\mathsf T} M^n v$ counts linear objects, and $\operatorname{tr} M^n$ counts objects on a cycle with a marked start. Using one for the other gives wrong counts: with 3 colors, the path with $n$ vertices has $3 \cdot 2^{n-1}$ proper colorings, but the cycle $C_n$ has only $2^n + 2(-1)^n$.
- **Too many states.** The number of profiles grows exponentially with the width of the strip. Reduce by symmetry, or move one cell at a time.
- **Overflow.** Counts grow like $\lambda^n$. Use big integers or a modulus.

## Exercises

1. Build the transfer matrix for binary strings with no factor $11$ and no factor $000$, and find their generating function.
2. Show that the number of 2-colorings of the vertices of a path with $n$ vertices, with no two adjacent vertices both black, is $F_{n+2}$, with a $2 \times 2$ transfer matrix.
3. Compute the number of domino tilings of a $4 \times n$ strip for $n \le 8$ with a $16 \times 16$ transfer matrix.
4. Prove that for any pattern of length $m$, the counts of the binary strings that avoid it satisfy a linear recurrence of order at most $m$.
5. Use $\operatorname{tr} M^n$ to count the binary necklaces with a marked start and no two adjacent 1s, and show that the count is the Lucas number $L_n$ for $n \ge 1$.

## References
