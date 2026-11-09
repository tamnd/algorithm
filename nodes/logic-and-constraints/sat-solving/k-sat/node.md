---
tag: 8FQX22
kind: problem
slug: k-sat
name: k-SAT
aliases:
- k-satisfiability
- k-CNF satisfiability
area: logic-and-constraints/sat-solving
level: core
summary: SAT restricted to clauses of at most k literals. Linear for k = 2 and NP-complete for k >= 3; the best known algorithms take 2^((1 - c/k)n) time, and ETH and SETH say how far this can improve.
prereqs: [sat, conjunctive-normal-form, 3-sat]
see_also: [2-sat, schoning-algorithm, ppsz-algorithm, strong-exponential-time-hypothesis, satisfiability-threshold, lovasz-local-lemma, exact-exponential-algorithms, max-sat]
sources:
  - paper: doi:10.1006/jcss.2000.1727
    title: Russell Impagliazzo and Ramamohan Paturi, On the complexity of k-SAT, Journal of Computer and System Sciences 62(2), 367 to 375 (2001)
    locator: the definitions of ETH and of the constants s_k, and the result that s_k increases infinitely often under ETH
  - paper: doi:10.1006/jcss.2001.1774
    title: Russell Impagliazzo, Ramamohan Paturi and Francis Zane, Which problems have strongly exponential complexity?, Journal of Computer and System Sciences 63(4), 512 to 530 (2001)
    locator: the sparsification lemma
  - paper: doi:10.1007/s00453-001-0094-7
    title: Uwe Schöning, A probabilistic algorithm for k-SAT based on limited local search and restart, Algorithmica 32(4), 615 to 623 (2002)
    locator: the bound (2(k - 1)/k)^n
  - paper: doi:10.1145/1066100.1066101
    title: Ramamohan Paturi, Pavel Pudlák, Michael E. Saks and Francis Zane, An improved exponential-time algorithm for k-SAT, Journal of the ACM 52(3), 337 to 364 (2005)
    locator: the PPSZ algorithm and its bound with the constants mu_k
  - paper: doi:10.1137/120868177
    title: Timon Hertli, 3-SAT faster and simpler, unique-SAT bounds for PPSZ hold in general, SIAM Journal on Computing 43(2), 718 to 729 (2014)
    locator: the PPSZ bounds for formulas with many models
  - paper: doi:10.1145/800133.804350
    title: Thomas J. Schaefer, The complexity of satisfiability problems, Proceedings of the 10th ACM Symposium on Theory of Computing (STOC 1978), 216 to 226
    locator: the dichotomy theorem for Boolean constraints
  - paper: "Burkhard Monien and Ewald Speckenmeyer, Solving satisfiability in less than 2^n steps, Discrete Applied Mathematics 10(3), 287 to 295 (1985)"
    locator: the branching algorithm on a shortest clause
  - paper: "Ramamohan Paturi, Pavel Pudlák and Francis Zane, Satisfiability coding lemma, Proceedings of the 38th IEEE Symposium on Foundations of Computer Science (FOCS 1997), 566 to 574"
    locator: the PPZ algorithm and the bound 2^((1 - 1/k) n)
  - paper: "Robin A. Moser and Gábor Tardos, A constructive proof of the general Lovász Local Lemma, Journal of the ACM 57(2), article 11 (2010)"
    locator: the algorithm that finds a model of a k-CNF formula under the local lemma condition
---

$k$-SAT is the [satisfiability problem](/sat/) for CNF formulas where each clause has at most $k$ literals. For $k = 2$ it is [2-SAT](/2-sat/), which is solvable in linear time. For each $k \ge 3$ it is NP-complete, since it contains [3-SAT](/3-sat/). The best known algorithms for $k \ge 3$ take time $2^{(1 - c/k) n}$ for a constant $c$, for example [Schöning's random walk](/schoning-algorithm/) and [PPSZ](/ppsz-algorithm/). Two hypotheses describe what to expect: the exponential time hypothesis (ETH) says that 3-SAT needs $2^{\delta n}$ time for some $\delta > 0$, and the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) (SETH) says that the base of the exponent tends to 2 as $k$ grows.

## In plain words

You have many yes-or-no choices, and rules that each name at most $k$ of them and say that at least one must go a certain way. For $k = 2$ there is a fast method. For $k = 3$ or more, no method is known that avoids an exponential search, but the search can be much faster than trying all choices: for $k = 3$, the best methods try about $1.31^n$ cases instead of $2^n$.

As $k$ grows, each rule is easier to satisfy alone, but the known methods gain less over trying everything. Many researchers believe that this is not a weakness of the methods, and that for large $k$ nothing much faster than trying everything is possible. This belief is a hypothesis, not a theorem.

## Definition

We use the notation of the area: $n$ variables, $m$ clauses, and $|F|$ literal occurrences. Fix an integer $k \ge 1$.

**Input.** A CNF formula $F$ over $x_1, \ldots, x_n$ where each clause has at most $k$ literals.

**Output.** Whether $F$ has a model, and if so, one model.

**Exactly $k$ literals.** Some authors ask for exactly $k$ distinct literals in each clause (E$k$-SAT). A shorter clause $C$ is padded with a new variable $z$ as $(C \vee z) \wedge (C \vee \neg z)$, and this is repeated until the length is $k$. So the two versions are equally hard.

## Variants

- **Small $k$.** 1-SAT is solved by checking that no variable occurs with both signs. 2-SAT is solved in $\Theta(n + m)$ time by the [2-SAT algorithm](/two-sat-algorithm/).
- **Unique $k$-SAT.** The formula is promised to have at most one model. By the [Valiant and Vazirani theorem](/valiant-vazirani-theorem/), this promise does not make the problem easier for randomized polynomial algorithms. The first PPSZ analysis was for this case.
- **Random $k$-SAT.** $m = \alpha n$ random clauses of exactly $k$ literals. The probability of a model drops sharply at a threshold ratio, which is about $2^k \ln 2$ for large $k$. See [the satisfiability threshold](/satisfiability-threshold/).
- **MAX-$k$-SAT.** Satisfy as many clauses as possible. See [MAX-SAT](/max-sat/).
- **Bounded occurrence.** The local lemma below gives satisfiable classes where each clause meets few other clauses.

## Examples

**Few clauses mean a model exists.** A formula with clauses of exactly $k$ literals and fewer than $2^k$ clauses has a model. *Proof.* Take a uniformly random assignment. A clause with $k$ distinct literals is false with probability $2^{-k}$, so by [linearity of expectation](/linearity-of-expectation/) the expected number of false clauses is $m 2^{-k} < 1$. So some assignment has no false clause. The bound is tight: the $2^k$ clauses with all sign patterns over $k$ variables have no model.

**Few overlaps mean a model exists.** If each clause has exactly $k$ literals and shares a variable with at most $d$ other clauses, where $e \cdot 2^{-k} (d + 1) \le 1$, then the formula has a model. This is the symmetric [Lovász local lemma](/lovasz-local-lemma/) with the bad events "clause $j$ is false", each of probability $2^{-k}$. The algorithm of Moser and Tardos (2010) finds a model in expected polynomial time: while some clause is false, pick one and give its variables new random values.

**The hardest small case.** For $k = 3$, the formula of the 8 clauses with all sign patterns over $x_1, x_2, x_3$ has no model, and each 7 of them have exactly one. This shows the first bound above is tight for $k = 3$.

## Known algorithms

Here $O^*$ hides factors polynomial in $n$ and $|F|$. The bounds are for the worst case; the randomized ones are expected time with one-sided error.

| algorithm | bound for $k$-SAT | for 3-SAT |
|---|---|---|
| Brute force | $O^*(2^n)$ | $2^n$ |
| Monien and Speckenmeyer (1985) | $O^*(\beta_k^n)$, where $\beta_k$ is the largest root of $x^k = 2x^{k-1} - 1$ | $1.619^n$ |
| Paturi, Pudlák and Zane (PPZ, 1997) | $O^*(2^{(1 - 1/k) n})$ | $1.588^n$ |
| [Schöning](/schoning-algorithm/) (1999) | $O^*((2 (k - 1)/k)^n)$ | $1.334^n$ |
| [PPSZ](/ppsz-algorithm/) (2005), general case by Hertli (2014) | $O^*(2^{(1 - \mu_k/(k-1)) n})$ | $1.3071^n$ |

The constant of PPSZ is $\mu_k = \sum_{j \ge 1} \frac{1}{j (j + 1/(k-1))}$. It increases with $k$ toward $\pi^2/6$, so the exponent is $1 - \Theta(1/k)$. For $k = 3$, $\mu_3 / 2 = 2 - 2 \ln 2$, and the bound is $2^{(2 \ln 2 - 1) n} \approx 1.3071^n$. Small improvements for $k = 3$ and $k = 4$ exist, such as biased PPSZ (Hansen, Kaplan, Zamir and Zwick 2019). In practice, [CDCL](/cdcl/) solvers decide large industrial instances, and their worst case is exponential.

## Bounds

Let $s_k$ be the infimum of the numbers $\delta$ such that $k$-SAT has a randomized algorithm with time $O(2^{\delta n})$. The table gives $s_k \le 1 - \Theta(1/k)$, and $s_k \le s_{k+1}$ since a $k$-CNF is a $(k+1)$-CNF.

- **ETH (Impagliazzo and Paturi 2001).** The hypothesis $s_3 > 0$. It implies P $\ne$ NP, and it is not proved.
- **Sparsification lemma (Impagliazzo, Paturi and Zane 2001).** For each $\varepsilon > 0$, a $k$-CNF formula is the OR of at most $2^{\varepsilon n}$ $k$-CNF formulas, each with $O(n)$ clauses, where the constant depends on $k$ and $\varepsilon$, and the list is found in $O^*(2^{\varepsilon n})$ time. So under ETH, 3-SAT also needs $2^{\Omega(m)}$ time, and through reductions of linear size many graph problems need $2^{\Omega(n)}$ time.
- **The constants grow (Impagliazzo and Paturi 2001).** Under ETH, $s_k < s_\infty$ for each $k$, where $s_\infty = \lim s_k$, and $s_k$ increases infinitely often.
- **SETH.** The hypothesis $s_\infty = 1$: for each $\varepsilon > 0$, some $k$ has no $O(2^{(1-\varepsilon) n})$ algorithm for $k$-SAT. It implies ETH. The known algorithms match its form, with $1 - s_k = O(1/k)$ from above. Many conditional lower bounds in [fine-grained complexity](/strong-exponential-time-hypothesis/) start from SETH.
- **Dichotomy.** [Schaefer's theorem](/schaefer-dichotomy-theorem/) says that a Boolean constraint language is in P (2-CNF, Horn, dual Horn, affine, or trivially satisfiable by all 0 or all 1) or NP-complete. $k$-SAT for $k \ge 3$ is on the hard side.

## Reductions

- **$k$-SAT to 3-SAT.** [Karp's clause split](/3-sat/) turns a clause of $k$ literals into $k - 2$ clauses of 3 literals with $k - 3$ new variables. This keeps satisfiability but multiplies the number of variables by up to about $m (k - 3) / n + 1$, so a $c^n$ algorithm for 3-SAT does not give one for $k$-SAT with the same $n$.
- **SAT to $k$-SAT.** For each $k \ge 3$, by the same split, so $k$-SAT is NP-complete for $k \ge 3$.
- **Unique $k$-SAT.** Valiant and Vazirani give a randomized reduction from SAT to unique SAT, and Calabro, Impagliazzo, Kabanets and Paturi (2008) show that unique $k$-SAT has the same limit constant as $k$-SAT, under randomized reductions.

## Applications

- **Fine-grained hardness.** SETH gives conditional lower bounds such as $n^{2 - o(1)}$ for edit distance and orthogonal vectors, and ETH gives $2^{\Omega(n)}$ bounds for many NP-hard graph problems.
- **Algorithm design.** The methods for $k$-SAT, random walks, random orders with forced values, and branching on short clauses, are used for other constraint problems.
- **Random structures.** Random $k$-SAT is a model for phase transitions in combinatorics and statistical physics.

## References
