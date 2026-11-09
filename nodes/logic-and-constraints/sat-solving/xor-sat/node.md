---
tag: 6PSPAR
kind: problem
slug: xor-sat
name: XOR-SAT
aliases:
- parity SAT
- XORSAT
- linear equations over GF(2)
area: logic-and-constraints/sat-solving
level: core
summary: SAT where each clause is an XOR of variables with a fixed parity. It is a linear system over GF(2), so Gaussian elimination decides it and counts its models in polynomial time.
prereqs: [sat, literal, gaussian-elimination]
see_also: [xor-gaussian-elimination, 2-sat, horn-sat, schaefer-dichotomy-theorem, tseitin-transformation, learning-parity-with-noise, dsu-with-parity, model-counting]
sources:
  - paper: doi:10.1145/800133.804350
    title: Thomas J. Schaefer, The complexity of satisfiability problems, Proceedings of the 10th ACM Symposium on Theory of Computing (STOC 1978), 216 to 226
    locator: the affine case of the dichotomy theorem
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2 (2022)
    locator: Section 7.2.2.2, Satisfiability (XOR clauses and parity constraints)
  - paper: "Alasdair Urquhart, Hard examples for resolution, Journal of the ACM 34(1), 209 to 219 (1987)"
    locator: the exponential resolution lower bound for Tseitin formulas on expander graphs
  - paper: "Mate Soos, Karsten Nohl and Claude Castelluccia, Extending SAT solvers to cryptographic problems, Theory and Applications of Satisfiability Testing (SAT 2009), Lecture Notes in Computer Science 5584, 244 to 257"
    locator: the whole paper (CNF plus XOR clauses in cryptanalysis)
  - paper: doi:10.1145/502090.502098
    title: Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48(4), 798 to 859 (2001)
    locator: the result for MAX-E3-LIN-2 (no 1/2 + epsilon approximation unless P = NP)
  - paper: "Olivier Dubois and Jacques Mandler, The 3-XORSAT threshold, Proceedings of the 43rd IEEE Symposium on Foundations of Computer Science (FOCS 2002), 769 to 778"
    locator: the threshold of random 3-XOR-SAT
---

XOR-SAT is the [satisfiability problem](/sat/) for conjunctions of XOR clauses, where each clause says that the XOR of some variables equals 0 or equals 1. A set of XOR clauses is a system of linear equations over the field $\mathrm{GF}(2)$, so [Gaussian elimination](/xor-gaussian-elimination/) decides it in polynomial time and also counts its models: a satisfiable system with $n$ variables and rank $r$ has exactly $2^{n - r}$ models. XOR-SAT is the affine case of [Schaefer's dichotomy theorem](/schaefer-dichotomy-theorem/), next to [2-SAT](/2-sat/) and [Horn-SAT](/horn-sat/). This page covers the problem; the algorithm has its own page.

## In plain words

You have a row of switches. Each rule names some switches and says "an odd number of these are on", or "an even number of these are on". The question is whether some setting of the switches obeys every rule.

These rules behave like sums where $1 + 1 = 0$. Two rules can be added: a switch named in both drops out, and the odd or even parts add. So the rules can be simplified in the same way as a school system of equations, one switch at a time, until each rule controls one switch or a rule says "nothing is odd", which is a contradiction. This takes a number of steps that grows like a power of the size, not exponentially. A small change to the rules, such as "at least one of these is on", makes the problem hard again.

## Definition

We use the notation of the area: $n$ variables and $m$ clauses.

**XOR clause.** A pair $(S, b)$ with $S \subseteq \{1, \ldots, n\}$ and $b \in \{0, 1\}$. It is the constraint $\bigoplus_{v \in S} x_v = b$. A negated variable needs no special form, since $\neg x_v = x_v \oplus 1$ moves into $b$, and a variable that occurs twice cancels, since $x_v \oplus x_v = 0$.

**Input.** A system of $m$ XOR clauses. In matrix form it is $A x = b$ over $\mathrm{GF}(2)$, with $A \in \{0,1\}^{m \times n}$ and $b \in \{0,1\}^m$, where $A[i][v] = 1$ when $x_v$ is in clause $i$.

**Output.** The decision version asks whether some $x \in \{0,1\}^n$ satisfies all clauses. The search version also asks for one such $x$. The counting version asks for the number of models.

**Structure of the models.** If $x^0$ is a model, then the models are exactly the vectors $x^0 \oplus y$ with $A y = 0$. So the models form an affine subspace of $\{0,1\}^n$, a coset of the null space of $A$, and the number of models is 0 or $2^{n - \mathrm{rank}(A)}$. The models are also closed under the XOR of any three of them, which is the property that defines the affine case of Schaefer's theorem.

## Variants

- **$k$-XOR-SAT.** Each clause has exactly $k$ variables. 2-XOR-SAT says for each pair whether two variables are equal or different. It is the question whether a graph with "equal" and "different" edge labels is consistent, and [union-find with parity](/dsu-with-parity/) decides it in near-linear time.
- **Counting.** Unlike #2-SAT and #Horn-SAT, which are #P-complete, the number of models of an XOR system is found in polynomial time, as $0$ or $2^{n - r}$.
- **Maximization.** MAX-$k$-XOR-SAT, also called MAX-E$k$-LIN-2, asks for the most satisfied clauses. It is NP-hard. A random assignment satisfies each clause with probability $1/2$, and for $k = 3$ Håstad proved that no polynomial algorithm does better than $1/2 + \varepsilon$ for any fixed $\varepsilon > 0$, unless P = NP. The noisy version with random clauses is [learning parity with noise](/learning-parity-with-noise/), a basis of cryptography.
- **CNF plus XOR.** A formula with both ordinary clauses and XOR clauses is NP-complete, since CNF alone is. Solvers such as CryptoMiniSat handle the XOR part with elimination and the CNF part with [CDCL](/cdcl/).
- **Random $k$-XOR-SAT.** Take $m = \alpha n$ random clauses of $k$ variables with random parities. For $k = 3$ the probability of a model drops from near 1 to near 0 at $\alpha \approx 0.918$ (Dubois and Mandler 2002). Unlike random [3-SAT](/satisfiability-threshold/), here the location of the threshold is proved.

## Examples

**A satisfiable system.** The four clauses

$$x_1 \oplus x_2 \oplus x_3 = 1,\quad x_2 \oplus x_3 \oplus x_4 = 0,\quad x_1 \oplus x_4 \oplus x_5 = 1,\quad x_3 \oplus x_5 = 1$$

have rank 4 over 5 variables, so they have $2^{5 - 4} = 2$ models: $(1,1,1,0,0)$ and $(0,0,1,1,0)$. The page on [Gaussian elimination](/xor-gaussian-elimination/) shows the elimination step by step.

**An unsatisfiable system.** The three clauses $x_1 \oplus x_2 = 1$, $x_2 \oplus x_3 = 1$ and $x_1 \oplus x_3 = 1$ add up to $0 = 1$, because each variable occurs twice. In words, the three vertices of a triangle cannot each differ from both others with only two values. Each clause holds for 2 of the 4 values of its two variables, and no assignment of the 8 satisfies all three.

**A CNF needs many clauses for one XOR.** The clause $x_1 \oplus \cdots \oplus x_k = 1$ written as a CNF over the same variables needs $2^{k-1}$ clauses. *Proof.* Take a clause $C$ of such a CNF and an assignment $a$ that makes $C$ false. If some $x_v$ does not occur in $C$, flipping $x_v$ in $a$ keeps $C$ false but changes the parity, so one of the two assignments is a model of the XOR that falsifies the CNF. So each clause contains all $k$ variables and excludes exactly one assignment. The $2^{k-1}$ assignments of even parity must all be excluded, so at least $2^{k-1}$ clauses are needed, and these clauses suffice. With new variables the [Tseitin transformation](/tseitin-transformation/) gives $O(k)$ clauses, by a chain of XORs of three variables.

## Known algorithms

| algorithm | bound | notes |
|---|---|---|
| [Gaussian elimination over GF(2)](/xor-gaussian-elimination/) | $O(m n \min(m, n))$ worst case | gives a model and the count $2^{n - r}$ |
| [Bitset elimination](/bitset-gaussian-elimination/) | $O(m \min(m, n) \lceil n / w \rceil)$ word operations | rows packed into words of $w$ bits |
| Elimination by fast matrix multiplication | $O(n^\omega)$ for $m = n$ | $\omega$ is the [exponent of matrix multiplication](/matrix-multiplication-exponent/) |
| [Wiedemann algorithm](/wiedemann-algorithm/) | about $n$ products of $A$ with a vector, randomized | for large sparse systems |
| [Union-find with parity](/dsu-with-parity/) | near-linear time | only for 2-XOR-SAT |

## Bounds

- **Upper bound.** Polynomial time, by elimination. The time is $O(n^\omega)$ for a square system, with $\omega < 2.372$.
- **Lower bound.** Each algorithm must read the input in the worst case, so $\Omega(m + n)$ for a sparse input. No better lower bound is known for general systems.
- **Resolution.** XOR-SAT is easy for elimination but hard for resolution. Tseitin formulas, which encode an odd sum of charges on the vertices of a graph as XOR clauses, have no model, yet each resolution proof has exponential size when the graph is a bounded-degree expander (Urquhart 1987). So a plain [CDCL](/cdcl/) solver, whose runs are resolution proofs, takes exponential time on these formulas, while elimination takes polynomial time.
- **Where it sits.** XOR-SAT is one of the six tractable cases of [Schaefer's dichotomy theorem](/schaefer-dichotomy-theorem/) for Boolean constraints.

## Reductions

- **$k$-XOR-SAT to 3-XOR-SAT.** Replace $x_1 \oplus x_2 \oplus \cdots \oplus x_k = b$ by $x_1 \oplus x_2 \oplus y = 0$ and $y \oplus x_3 \oplus \cdots \oplus x_k = b$ with a new variable $y$, and repeat. The value of $y$ is forced, so the reduction keeps the count of models.
- **XOR-SAT to CNF.** Each XOR of $k \le 3$ variables becomes $2^{k-1}$ clauses, and longer XORs are first split as above. The result is a CNF that a SAT solver accepts, but, by the resolution bound above, it may be very hard for it.
- **2-coloring.** A graph is bipartite exactly when the system $x_u \oplus x_w = 1$ for each edge $uw$ has a model. The triangle above is the smallest odd cycle.

## Applications

- **Cryptanalysis.** The equations of stream ciphers and hash functions mix XORs with nonlinear parts. Solvers that keep XOR clauses as equations and run elimination during the search do much better on them than CNF solvers (Soos, Nohl and Castelluccia 2009).
- **Codes.** Decoding a [linear code](/linear-code/) with the [parity-check matrix](/parity-check-matrix/) asks for the words with a given syndrome, which is a system of XOR equations. Finding the one of least weight, [syndrome decoding](/syndrome-decoding/), is NP-hard.
- **Approximate model counting.** Random XOR constraints are a hash family. Adding about $\log_2 c$ of them to a formula with $c$ models leaves a small number of models with good probability, which is the base of approximate [model counting](/model-counting/).
- **Puzzles.** In "lights out" each button flips a set of lights, and each light gives one XOR equation over the buttons.

## References
