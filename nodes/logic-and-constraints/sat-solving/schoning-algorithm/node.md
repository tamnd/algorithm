---
tag: JNC89S
kind: algorithm
slug: schoning-algorithm
name: Schoning's algorithm
aliases:
- random walk for k-SAT
- Schöning's algorithm
- Schöning's random walk
area: logic-and-constraints/sat-solving
level: advanced
summary: Randomized k-SAT algorithm. Restart from a random assignment, and flip a random variable of a false clause up to 3n times. Expected time O*((2(k-1)/k)^n), which is (4/3)^n for 3-SAT.
solves: [k-sat, 3-sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of clauses, k: the largest clause size}
  time: {expected: "O((2(k-1)/k)^n n^2 m k)"}
  space: {extra: O(n + m k)}
properties: {deterministic: false, exact: false}
history:
  year: 1999
  people: [Uwe Schöning]
  note: Presented at FOCS 1999, after Papadimitriou's random walk for 2-SAT of 1991; short walks with restarts solve k-SAT in O*((2(k-1)/k)^n) expected time.
prereqs: [k-sat, markov-chain, binary-entropy-function]
see_also: [ppsz-algorithm, walksat, gsat, probsat, local-search, monte-carlo-algorithm, strong-exponential-time-hypothesis, exact-exponential-algorithms]
sources:
  - paper: doi:10.1007/s00453-001-0094-7
    title: Uwe Schöning, A probabilistic algorithm for k-SAT based on limited local search and restart, Algorithmica 32(4), 615 to 623 (2002)
    locator: the whole paper (the algorithm and its analysis)
  - paper: "Uwe Schöning, A probabilistic algorithm for k-SAT and constraint satisfaction problems, Proceedings of the 40th IEEE Symposium on Foundations of Computer Science (FOCS 1999), 410 to 414"
    locator: the conference version
  - paper: "Christos H. Papadimitriou, On selecting a satisfying truth assignment, Proceedings of the 32nd IEEE Symposium on Foundations of Computer Science (FOCS 1991), 163 to 169"
    locator: the random walk for 2-SAT
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, 2nd edition (2017)
    locator: Section 7.1 (the random walk algorithms for 2-SAT and 3-SAT)
  - paper: "Robin A. Moser and Dominik Scheder, A full derandomization of Schöning's k-SAT algorithm, Proceedings of the 43rd ACM Symposium on Theory of Computing (STOC 2011), 245 to 252"
    locator: the deterministic version
  - paper: "Evgeny Dantsin, Andreas Goerdt, Edward A. Hirsch, Ravi Kannan, Jon Kleinberg, Christos Papadimitriou, Prabhakar Raghavan and Uwe Schöning, A deterministic (2 - 2/(k+1))^n algorithm for k-SAT based on local search, Theoretical Computer Science 289(1), 69 to 83 (2002)"
    locator: the deterministic local search with covering codes
---

Schöning's algorithm is a randomized algorithm for [k-SAT](/k-sat/). It starts from a uniformly random assignment, and $3n$ times it picks a false clause and flips a random variable of that clause. If no model appears, it restarts. If the formula has a model, one try finds one with probability at least about $(k / (2(k-1)))^n$, so the expected time is $O^*((2(k-1)/k)^n)$, which is $O^*((4/3)^n)$ for [3-SAT](/3-sat/). It was the fastest known algorithm for 3-SAT when Schöning published it in 1999, and its proof is short. It has one-sided error: it never returns a wrong model, but it can miss a model with small probability, and it never proves that a formula has none.

## In plain words

You want to set many switches so that a list of rules all hold, where each rule says that at least one of its three switches must be in a given position. Set all switches at random. Then, while some rule fails, pick a failing rule and flip one of its three switches at random.

If some correct setting exists, each such flip has at least a one in three chance to move you one switch closer to it. That is not enough to get there from far away, because the walk tends to drift off. So you stop after a short walk and start again from a new random setting. Sometimes the start is close, and then the short walk has a fair chance to finish. Counting how often this happens shows that about $(4/3)^n$ restarts are enough, far fewer than the $2^n$ settings of $n$ switches.

## The problem

The input is a CNF formula $F$ over $x_1, \ldots, x_n$ with $m$ clauses of at most $k$ literals, and a number of tries $T$. The output is a model of $F$, or the answer "no model found". If $F$ has no model, the answer is always "no model found". If $F$ has a model, the answer is a model with probability at least $1 - \varepsilon$ when $T = \lceil \ln(1/\varepsilon) / p \rceil$, where $p$ is the bound on the success of one try given below.

## The algorithm

```pseudo id=main
SCHONING(F, n, T)
L1 for t ← 1 to T do                        ▷ independent tries
L2     x ← a uniformly random assignment in {0,1}^n
L3     for s ← 0 to 3n do
L4         if x satisfies F then return x
L5         C ← any clause of F that x makes false
L6         ℓ ← a uniformly random literal of C
L7         flip the variable of ℓ in x
L8 return "no model found"
```

Line L4 is the only place that returns an assignment, and it checks it first. The choice at line L5 may be arbitrary or random; the analysis holds for any rule, and the implementation picks a uniformly random false clause. The random choice of line L6 is the important one. The walk length $3n$ comes from the proof, which needs the walk to make $i$ wrong steps and $i + j$ right steps when the start is at distance $j$.

The implementation keeps, for each clause, the number of its true literals, and a list of the false clauses, so that lines L4 and L5 take constant time and a flip updates only the clauses of the flipped variable. With $T$ left open, it computes $T$ for $\varepsilon = 10^{-6}$. It also has Papadimitriou's walk for 2-SAT: one long walk of $2n^2$ flips, repeated a few times.

## Example

Take the seven clauses over $x_1, x_2, x_3$ with all sign patterns except $(\neg x_1 \vee x_2 \vee x_3)$. Each clause rules out one assignment, so the only model is $a^* = 100$. One try may go as follows, where $d$ is the distance to $a^*$.

| step | $x$ | $d$ | false clause | good literals (true under $a^*$) | flip | chance to move closer |
|---|---|---|---|---|---|---|
| 0 | 011 | 3 | $(x_1 \vee \neg x_2 \vee \neg x_3)$ | all three | $x_3$ | $3/3$ |
| 1 | 010 | 2 | $(x_1 \vee \neg x_2 \vee x_3)$ | $x_1$, $\neg x_2$ | $x_2$ | $2/3$ |
| 2 | 000 | 1 | $(x_1 \vee x_2 \vee x_3)$ | $x_1$ only | $x_1$ | $1/3$ |
| 3 | 100 | 0 | none | | | |

At step 3, line L4 returns $100$. The last row shows the worst case of the proof: only one literal of the false clause helps, so the walk moves closer with probability exactly $1/3$. At step 0 the walk cannot move away, because $x$ differs from $a^*$ in every variable. If line L6 had picked $x_3$ at step 1, the walk would have gone back to $011$.

## Correctness

Line L4 returns only models, so a returned assignment is always correct, and on a formula with no model the algorithm always reaches line L8. The work is to bound the chance of a miss. Fix a model $a^*$ and let $d$ be the distance from $x$ to $a^*$. A false clause has a literal that is true under $a^*$, and flipping its variable decreases $d$, so each flip decreases $d$ with probability at least $1/k$. Couple $d$ with a walk on the integers that goes down with probability exactly $1/k$: the walk stays above $d$. From distance $j$, the walk reaches 0 within $3n$ steps with probability at least about $(k-1)^{-j}$, by counting paths with $j/(k-2)$ up steps and an entropy bound on the binomial coefficient. A random start has distance $j$ with probability $\binom{n}{j} 2^{-n}$, and the binomial theorem gives

$$\Pr[\text{one try succeeds}] \ \ge\ p = \frac{c_k}{3n+1} \left( \frac{k}{2(k-1)} \right)^n, \qquad c_k = \left(\frac{k-1}{k}\right)^{k-3} \ge \frac{1}{e}.$$

The full proof is in the proof file of this page.

## Complexity

One try takes $O(nmk)$ time: $O(n + mk)$ for the start, and $3n$ flips that each update at most $m$ clauses of at most $k$ literals. The number of tries until the first success is geometric with mean at most $1/p$. So on a satisfiable formula the expected time is

$$O\left( \left( \frac{2(k-1)}{k} \right)^n n^2 m k \right),$$

which is $O(1.3334^n)$ for 3-SAT and $O(1.5^n)$ for 4-SAT. With $T = \lceil \ln(1/\varepsilon) / p \rceil$ tries the worst case time is this bound times $\ln(1/\varepsilon)$, on any formula. The extra space is $O(n + mk)$ for the assignment, the counts, and the lists of occurrences.

For 2-SAT the walk needs no restarts. Papadimitriou (1991) showed that it finds a model in at most $n^2$ expected flips: each flip moves closer with probability at least $1/2$, and a fair walk on $\{0, \ldots, n\}$ reaches 0 in at most $n^2$ expected steps. The proof is in the complexity proof file. The [2-SAT algorithm](/two-sat-algorithm/) is faster, with linear time, but the walk shows why $k = 2$ and $k = 3$ differ.

## Properties

- **One-sided error.** A [Monte Carlo algorithm](/monte-carlo-algorithm/) for the decision problem: "model found" is always right, and "no model found" is wrong with probability at most $\varepsilon$. Run without a limit on $T$, it is a [Las Vegas algorithm](/las-vegas-algorithm/) for satisfiable formulas, and it runs forever on formulas with no model.
- **Little memory.** It stores one assignment and the counts, polynomial space.
- **Any choice of clause.** The analysis does not depend on which false clause line L5 picks.
- **Analysis by one model.** The proof uses only one fixed model. Formulas with many models are easier in practice, but the bound does not improve.

## Variants and improvements

- **Better starts.** Hofmeister, Schöning, Schuler and Watanabe (2002) choose the start more cleverly for 3-SAT and get about $1.3302^n$. Combinations of Schöning's walk with [PPSZ](/ppsz-algorithm/) by Iwama and Tamaki (2004) and later authors gave further small gains.
- **PPSZ.** For 3-SAT, PPSZ with Hertli's analysis (2014) reaches about $1.3071^n$ alone, which is better than all combinations with the walk.
- **Derandomization.** Dantsin and others (2002) replace the random start by a covering code and the walk by a deterministic search of the ball of radius $r$, which gives $(2k/(k+1))^n$, so $1.5^n$ for 3-SAT. Moser and Scheder (2011) derandomize the walk fully and reach $(4/3 + \varepsilon)^n$ for 3-SAT.
- **Constraint satisfaction.** For constraints of arity $k$ over domains of size $d$, the same walk gives $(d (k-1) / k)^n$ up to polynomial factors (Schöning 1999).
- **Practical local search.** [WalkSAT](/walksat/) and [probSAT](/probsat/) keep the idea of flipping a variable of a false clause, but pick the variable by its effect on other clauses, and restart rarely. They are much faster on random formulas, but have no proved bound of this kind.

## When to use it

Use it in teaching and in theory, as the simplest algorithm with a proved bound below $2^n$ for $k$-SAT, and as a building block of better exponential algorithms. For real formulas, use a [CDCL](/cdcl/) solver, which also proves unsatisfiability, or a tuned local search such as [probSAT](/probsat/) for large random satisfiable formulas. For 2-SAT, use the linear [2-SAT algorithm](/two-sat-algorithm/).

## Pitfalls

- **Treating "no model found" as a proof.** The answer at line L8 is only probably right. To prove that a formula has no model, use a complete method.
- **Too few tries.** The number of tries must grow like $(2(k-1)/k)^n$ times $n$. A fixed number of tries, such as 100, gives no guarantee for large $n$.
- **Long walks without restarts.** For $k \ge 3$, a walk of $n^2$ or more flips without restarts has no good bound, since the comparison walk drifts away from the model. The length $3n$ and the restarts are what the proof needs.
- **The wrong $k$.** The bound uses the longest clause. One long clause in a 3-CNF formula raises $k$ and the base of the bound; split long clauses first if the bound matters.
- **Empty clauses.** A formula with an empty clause has no model, but line L5 would never find a literal to flip. Check for it first.

## Implementations

## History

Papadimitriou (1991) introduced the random walk for 2-SAT and showed that it needs $O(n^2)$ expected flips. Schöning (1999) observed that for $k$-SAT short walks with restarts give an exponential bound below $2^n$, namely $(2(k-1)/k)^n$ up to polynomial factors, and the journal version appeared in 2002. For several years it was the best bound for 3-SAT, and it led to a series of improvements, combinations with PPSZ, and derandomizations, up to the full derandomization by Moser and Scheder in 2011.

## References
