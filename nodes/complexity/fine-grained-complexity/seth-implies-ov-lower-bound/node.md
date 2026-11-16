---
tag: CX4N6X
kind: theorem
slug: seth-implies-ov-lower-bound
name: SETH implies OV lower bound
aliases:
- Williams' OV reduction
area: complexity/fine-grained-complexity
level: advanced
summary: "Williams (2005): if Orthogonal Vectors with dimension c log n had an O(n^(2-e)) algorithm for every c, SETH would fail. The proof splits the variables of a CNF formula into two halves."
prereqs: [strong-exponential-time-hypothesis, orthogonal-vectors]
see_also: [orthogonal-vectors-hypothesis, fine-grained-reduction, conditional-lower-bound, edit-distance-seth-lower-bound, lcs-seth-lower-bound, quadratic-time-hardness, k-sat, sum-over-subsets]
sources:
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: "Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005, 357-365 (conference version in ICALP 2004)"
    locator: the section on cooperative subset queries and orthogonal vectors (the theorem that a k^(2-e) algorithm for the subset query problem gives CNF-SAT in time 2^((1-e/2)n), and its split-and-list proof); this page relies on the journal version
  - paper: doi:10.1006/jcss.2001.1774
    title: "Russell Impagliazzo, Ramamohan Paturi and Francis Zane, Which problems have strongly exponential complexity?, Journal of Computer and System Sciences 63(4), 2001, 512-530"
    locator: the sparsification lemma
  - paper: doi:10.1006/jcss.2000.1727
    title: "Russell Impagliazzo and Ramamohan Paturi, On the complexity of k-SAT, Journal of Computer and System Sciences 62(2), 2001, 367-375"
    locator: the definition of s_k and of the exponential time hypotheses
  - paper: doi:10.1007/978-3-642-11269-0_6
    title: "Chris Calabro, Russell Impagliazzo and Ramamohan Paturi, The complexity of satisfiability of small depth circuits, IWPEC 2009, Lecture Notes in Computer Science 5917, 75-85"
    locator: Section 1.1 (SETH with randomized algorithms)
  - paper: "Amir Abboud, Ryan Williams and Huacheng Yu, More applications of the polynomial method to algorithm design, Proceedings of the 26th ACM-SIAM Symposium on Discrete Algorithms (SODA 2015), 218-230"
    locator: the algorithm for orthogonal vectors with d = c log n in time n^(2 - 1/O(log c)), which shows that c must depend on e
  - paper: "Virginia Vassilevska Williams, On some fine-grained questions in algorithms and complexity, Proceedings of the International Congress of Mathematicians (ICM 2018), Vol. 3, 3447-3487"
    locator: the section on SETH and orthogonal vectors (the reduction with sparsification)
---

The theorem says that a strongly subquadratic algorithm for [Orthogonal Vectors](/orthogonal-vectors/) would refute the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/). Williams proved it in 2004 with a split-and-list reduction: cut the variables of a CNF formula into two halves, list all assignments of each half as vectors, and use one coordinate per clause. A pair of vectors is then orthogonal exactly when the two half assignments satisfy every clause together. With the sparsification lemma, the dimension is $O(\log n)$, and the theorem becomes SETH $\Rightarrow$ [OVH](/orthogonal-vectors-hypothesis/).

## Statement

The model is the [word RAM](/word-ram/) with words of $O(\log n)$ bits. OV has two lists $A$ and $B$ of $n$ vectors each in $\{0,1\}^d$, and asks for $a \in A$ and $b \in B$ with $a \cdot b = 0$. A CNF formula has $N$ variables and $m$ clauses, and its size $|F|$ is the total number of literals.

**Lemma (split and list).** There is a deterministic algorithm that maps a CNF formula $F$ with $N$ variables and $m$ clauses to an OV instance with $n = 2^{\lceil N/2 \rceil}$ vectors in each list and dimension $d = m$, in time $O(2^{N/2} |F|)$, such that $F$ is satisfiable if and only if the instance has an orthogonal pair. The witnesses map both ways: an orthogonal pair gives a satisfying assignment, and a satisfying assignment gives an orthogonal pair.

**Theorem (Williams 2005).**

1. If OV has an algorithm with time $O(n^{2-\varepsilon} d^{t})$ for constants $\varepsilon > 0$ and $t$, then CNF-SAT has an algorithm with time $2^{(1-\varepsilon/2) N} \mathrm{poly}(m)$, and SETH fails.
2. If there is an $\varepsilon > 0$ such that for every constant $c$, OV with $d = c \log_2 n$ has an algorithm with time $O(n^{2-\varepsilon})$, then SETH fails.

Part 2 is the contrapositive of SETH $\Rightarrow$ OVH: if SETH holds, then for every $\varepsilon > 0$ there is a $c$ such that OV with $d = c \log n$ has no $O(n^{2-\varepsilon})$ algorithm. Both parts are **conditional on SETH** as lower bounds; the lemma and the implications themselves are **unconditional**. If the OV algorithm is randomized with bounded error, the conclusion refutes the randomized form of SETH.

## In plain words

Take a logic formula with many yes-or-no variables. Cut the variables into two halves. For each way to set the first half, write down which clauses that half fails to make true. Do the same for the second half. A full setting makes the formula true exactly when no clause is missed by both halves. In vector terms, the two lists of missed clauses have no common entry.

So a fast way to find such a pair in two lists is a fast way to solve the formula. Each half has the square root of the number of full settings, so checking all pairs of halves costs as much as brute force. A method that beats the pair check by any fixed power would beat brute force on formulas by a fixed fraction of the exponent, and SETH says that is impossible.

## Proof

### The construction

Let $F = C_1 \land \cdots \land C_m$ have variables $x_1, \ldots, x_N$. Each clause is a set of literals.

```pseudo id=main
SAT-TO-OV(F, N)              ▷ F has clauses C_1, ..., C_m over x_1, ..., x_N
L1  if N is odd then N ← N + 1         ▷ x_N is a new variable in no clause
L2  h ← N / 2;  V1 ← {x_1, ..., x_h};  V2 ← {x_{h+1}, ..., x_N}
L3  for each assignment α : V1 → {0, 1} do
L4      add to A the vector a_α with a_α[j] = 1 if α makes no literal of C_j true, else 0
L5  for each assignment β : V2 → {0, 1} do
L6      add to B the vector b_β with b_β[j] = 1 if β makes no literal of C_j true, else 0
L7  return (A, B)
```

A literal over $V_2$ is never made true by $\alpha$, since $\alpha$ does not set its variable; so $a_\alpha[j] = 1$ means that every literal of $C_j$ over $V_1$ is false under $\alpha$. Line L1 does not change satisfiability: the new variable is in no clause.

### The key claim

**Claim.** For all $\alpha$ and $\beta$, $a_\alpha \cdot b_\beta$ equals the number of clauses that the full assignment $\alpha \cup \beta$ does not satisfy.

*Proof.* Fix a clause $C_j$. Every literal of $C_j$ is over $V_1$ or over $V_2$. A literal over $V_1$ is true under $\alpha \cup \beta$ if and only if it is true under $\alpha$, and the same for $V_2$ and $\beta$. So $\alpha \cup \beta$ fails to satisfy $C_j$ if and only if $\alpha$ makes no literal of $C_j$ true and $\beta$ makes no literal of $C_j$ true, that is, if and only if $a_\alpha[j] = b_\beta[j] = 1$, that is, $a_\alpha[j]\, b_\beta[j] = 1$. Summing over $j$ gives the claim. $\square$

### Correctness of the lemma

By the claim, $a_\alpha \cdot b_\beta = 0$ if and only if $\alpha \cup \beta$ satisfies every clause.

- *From a satisfying assignment to a pair.* If $\sigma$ satisfies $F$, let $\alpha = \sigma|_{V_1}$ and $\beta = \sigma|_{V_2}$, with the new variable of L1 set to 0. Then $\alpha \cup \beta = \sigma$, so $a_\alpha \cdot b_\beta = 0$.
- *From a pair to a satisfying assignment.* If $a_\alpha \cdot b_\beta = 0$, then $\alpha \cup \beta$ satisfies $F$; drop the new variable of L1 if there is one.

So $F$ is satisfiable if and only if the instance has an orthogonal pair. Each list has $2^{N/2}$ vectors (after L1), and each vector has $m$ coordinates. To compute one vector, go once through the literals of $F$, so one vector costs $O(|F|)$ time and all of them cost $O(2^{N/2} |F|)$. $\square$

### Part 1

Let an OV algorithm run in time $O(n^{2-\varepsilon} d^{t})$. On input $F$, build the instance of the lemma, with $n = 2^{N/2}$ (after L1) and $d = m$, and run the algorithm. The total time is

$$O(2^{N/2} |F|) + O\big((2^{N/2})^{2-\varepsilon} m^{t}\big) = 2^{(1-\varepsilon/2) N} \mathrm{poly}(m),$$

since $|F| \le m N$. For $k$-SAT with a fixed $k$, $m$ is at most a polynomial in $N$, so $k$-SAT has an algorithm with time $2^{(1-\varepsilon/2) N} \mathrm{poly}(N)$ for every $k$. Then $s_k \le 1 - \varepsilon/2$ for every $k$, so $s_\infty < 1$, and SETH fails. This part does not need sparsification; it also refutes the weaker CNF-SETH.

### Part 2

Suppose that $\varepsilon > 0$ is fixed and that, for each constant $c$, an algorithm $\mathcal{A}_c$ decides OV with $d = c \log_2 n$ in time $O(n^{2-\varepsilon})$, where the constant in the $O$ may depend on $c$. Fix $k \ge 3$. We show that $k$-SAT has an algorithm with time $O(2^{(1-\varepsilon/5) N})$.

1. *Sparsify.* Apply the sparsification lemma with parameter $\varepsilon/4$: in time $\mathrm{poly}(N)\, 2^{\varepsilon N/4}$, write $F$ as $F_1 \lor \cdots \lor F_t$ with $t \le 2^{\varepsilon N/4}$, where each $F_i$ is a $k$-CNF formula on the same $N$ variables with at most $C N$ clauses, for a constant $C = C(k, \varepsilon/4)$. Take $C$ to be an integer. $F$ is satisfiable if and only if some $F_i$ is.
2. *Split and list.* After L1 the number of variables is even; call it $N$ again (it grew by at most 1). For each $F_i$, build the OV instance of the lemma: $n = 2^{N/2}$ vectors per list and $d_i \le C N = 2C \log_2 n$ coordinates.
3. *Pad.* Append $2C \log_2 n - d_i$ zero coordinates to every vector. Zero coordinates add nothing to an inner product, so the answer does not change, and now $d = c \log_2 n$ with $c = 2C$, a constant that depends only on $k$ and $\varepsilon$.
4. *Solve.* Run $\mathcal{A}_{2C}$ on each of the $t$ instances, and accept if one of them has an orthogonal pair.

The time is $\mathrm{poly}(N)\, 2^{\varepsilon N/4}$ for step 1, plus $t$ times $O(2^{N/2}\, \mathrm{poly}(N)) + O((2^{N/2})^{2-\varepsilon})$ for steps 2 to 4. That is

$$2^{\varepsilon N/4} \cdot O\big(2^{(1-\varepsilon/2) N}\big)\, \mathrm{poly}(N) = 2^{(1-\varepsilon/4) N} \mathrm{poly}(N) = O\big(2^{(1-\varepsilon/5) N}\big).$$

So $s_k \le 1 - \varepsilon/5$ for every $k \ge 3$, hence $s_\infty \le 1 - \varepsilon/5 < 1$, and SETH fails. $\blacksquare$

*Randomized algorithms.* If each $\mathcal{A}_c$ errs with probability at most $1/3$, run it $r = O(N)$ times on each instance and take the majority answer. Each answer is then wrong with probability at most $2^{-N}$, so by the union bound all $t \le 2^{\varepsilon N/4}$ answers are right with probability at least $1 - 2^{-(1-\varepsilon/4) N}$. The cost grows by a factor $O(N)$ only, so the argument refutes the randomized form of SETH.

### A worked example

Let $N = 4$ and

$$F = (x_1 \lor x_3) \land (\lnot x_1 \lor x_2 \lor \lnot x_4) \land (\lnot x_2 \lor x_4) \land (x_2 \lor \lnot x_3).$$

The halves are $V_1 = \{x_1, x_2\}$ and $V_2 = \{x_3, x_4\}$, and $d = m = 4$. Coordinate $j$ of a vector is 1 when the half assignment makes no literal of clause $j$ true:

| $x_1 x_2$ | $a_\alpha$ | | $x_3 x_4$ | $b_\beta$ |
|---|---|---|---|---|
| 00 | 1001 | | 00 | 1010 |
| 01 | 1010 | | 01 | 1100 |
| 10 | 0101 | | 10 | 0011 |
| 11 | 0010 | | 11 | 0101 |

For example, $\alpha = 00$ makes $\lnot x_1$ true, so clause 2 is covered, and $\lnot x_2$ true, so clause 3 is covered; clauses 1 and 4 are not, which gives 1001. The orthogonal pairs are $(01, 11)$, $(10, 00)$, $(11, 01)$ and $(11, 11)$. They map to the assignments $x_1 x_2 x_3 x_4 = 0111$, $1000$, $1101$ and $1111$, and these are exactly the four satisfying assignments of $F$ found by brute force over all 16.

Add the clause $(\lnot x_2 \lor \lnot x_4)$. Each vector gets a fifth coordinate, and then $A = (10010, 10101, 01010, 00101)$ and $B = (10100, 11001, 00110, 01011)$. Only the pair $(10, 00)$ is still orthogonal, and $1000$ is the only satisfying assignment left.

### Implementation and tests

The Python file implements SAT-TO-OV and the two witness maps. The tests compare satisfiability by brute force with orthogonality by brute force on all 2,951 formulas over $x_1, x_2, x_3$ with one to three distinct clauses (each clause a nonempty set of literals on distinct variables), and on 400 random formulas with seed 20261116, up to 9 variables and 14 clauses. They also check both witness maps on every instance, and the two tables of the example above.

## Consequences

- **SETH implies OVH.** This is part 2. So every lower bound proved from OV, such as those for [edit distance](/edit-distance-seth-lower-bound/), [LCS](/lcs-seth-lower-bound/) and approximate graph diameter, holds under SETH. See [quadratic-time hardness](/quadratic-time-hardness/).
- **$k$-OV.** Split the variables into $k$ parts instead of 2. The same claim, with the product of $k$ coordinates, shows that, conditional on SETH, $k$-OV with $d = c \log n$ has no $O(n^{k-\varepsilon})$ algorithm for a suitable $c$. This is the source of the bounds for LCS of $k$ strings.
- **A weaker assumption is enough downstream.** Since OVH follows from SETH and is not known to imply it, a bound proved from OV is stronger than one proved from SETH directly.
- **The reduction is a [fine-grained reduction](/fine-grained-reduction/)** from CNF-SAT with time $2^N$ to OV with time $n^2$. Its overhead is $2^{N/2} \mathrm{poly}(N)$, which is $n^{1+o(1)}$, much below $n^{2}$.

## Tightness

- **The exponents match.** Brute force on OV, in time $n^2 d$, gives brute force on CNF-SAT, in time $2^N \mathrm{poly}(m)$. A saving of $\varepsilon$ in the OV exponent gives a saving of exactly $\varepsilon/2$ in the SAT exponent, and no more.
- **The constant $c$ must depend on $\varepsilon$.** For each fixed $c$, Abboud, Williams and Yu (2015) solve OV with $d = c \log n$ in time $n^{2 - 1/O(\log c)}$, randomized. So "OV with $d = c \log n$ needs $n^{2-o(1)}$ time" is false for every fixed $c$, and part 2 cannot be improved to a single $c$.
- **The dimension must be $\omega(\log n)$.** For $d = c \log_2 n$ with $c < 2$, the [sum over subsets](/sum-over-subsets/) table solves OV in time $O(n^{c} \log n)$.
- **The converse is open.** No reduction from SAT to OV in the other direction is known, so OVH may hold even if SETH fails.

## History

Williams gave the reduction at ICALP 2004, in the journal version in Theoretical Computer Science in 2005, as a side result of his work on 2-CSP. He stated it for a cooperative subset query problem and for orthogonal vectors, in the form of part 1, with a factor polynomial in $d$. The low-dimension form uses the sparsification lemma of Impagliazzo, Paturi and Zane (2001). The problem became the main bridge from SETH to polynomial-time problems with Bringmann's bound for the Fréchet distance (2014) and the bounds for edit distance (Backurs and Indyk 2015) and LCS (Abboud, Backurs and Vassilevska Williams 2015; Bringmann and Künnemann 2015). The survey of Vassilevska Williams (ICM 2018) states the theorem in the form used on this page.

## References
