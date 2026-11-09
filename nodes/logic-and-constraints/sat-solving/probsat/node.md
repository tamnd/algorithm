---
tag: RPJ893
kind: algorithm
slug: probsat
name: ProbSAT
aliases:
- probSAT
area: logic-and-constraints/sat-solving
level: advanced
summary: Local search for SAT. Pick a random false clause and flip one of its variables at random, with probability that falls with the number of clauses the flip would break.
solves: [sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of clauses, k: the largest clause size, d: the largest number of clauses that contain one variable, t: MAX-TRIES, f: MAX-FLIPS}
  time: {worst: O(t (f k d + m k))}
  space: {extra: O(n + m k)}
properties: {deterministic: false, exact: false}
history:
  year: 2012
  people: [Adrian Balint, Uwe Schöning]
  note: Presented at SAT 2012 as a study of which probability distribution over the variables of a false clause works best, with the finding that the break count alone is enough.
prereqs: [sat, local-search, walksat]
see_also: [walksat, gsat, schoning-algorithm, satisfiability-threshold, survey-propagation, cdcl, max-sat, k-sat]
sources:
  - paper: doi:10.1007/978-3-642-31612-8_3
    title: "Adrian Balint and Uwe Schöning, Choosing probability distributions for stochastic local search and the role of make versus break, Theory and Applications of Satisfiability Testing (SAT 2012), LNCS 7317, 16 to 29"
    locator: the break-only rule, the polynomial and exponential forms, and the tuned values of cb and eps
  - paper: "Bart Selman, Henry A. Kautz and Bram Cohen, Noise strategies for improving local search, Proceedings of the 12th National Conference on Artificial Intelligence (AAAI-94), 337 to 343"
    locator: WalkSAT, the rule that probSAT simplifies
  - paper: doi:10.1007/s00453-001-0094-7
    title: "Uwe Schöning, A probabilistic algorithm for k-SAT based on limited local search and restart, Algorithmica 32 (2002), 615 to 623"
    locator: the uniform random walk, which is probSAT with cb = 0
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications (2004)
    locator: probabilistic approximate completeness
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, 2nd edition (2021)
    locator: the chapter on stochastic local search
---

probSAT is a [local search](/local-search/) method for the [satisfiability problem](/sat/), by Balint and Schöning (2012). Like [WalkSAT](/walksat/), it picks a random false clause and flips one of its variables. Unlike WalkSAT, it has no special cases: it picks each variable of the clause at random, with a weight $f(\mathrm{break})$ that falls as the number of clauses the flip would make false grows. Balint and Schöning found that this simple rule, with the make count left out, was faster than earlier local search methods on random $k$-CNF formulas in their experiments. probSAT is incomplete: it cannot prove that a formula has no model. With $c_b = 0$ it is [Schöning's](/schoning-algorithm/) uniform random walk.

## In plain words

You want to set many switches so that a list of rules all hold. Set them at random, then pick one broken rule at random. Each switch of this rule would fix it, but may break other rules. Count, for each of these switches, how many rules it would break.

Now draw one switch by lottery. A switch that breaks no other rule gets many tickets, a switch that breaks one rule gets fewer, and a switch that breaks many rules gets very few, but never none. Flip the switch that wins, and repeat. Good moves are likely, but any move can happen, so the search never gets stuck for good.

## The problem

The input is a CNF formula $F$ with $n$ variables and $m$ clauses, a weight function $f$, and two limits, MAX-TRIES and MAX-FLIPS. The output is a model of $F$, or "no model found". probSAT does not decide satisfiability: "no model found" is also the output on some satisfiable formulas.

## The algorithm

For an assignment $x$ and a variable $v$, $\mathrm{break}(v)$ is the number of true clauses that become false when $v$ is flipped. The weight function has one of two forms, with parameters $c_b$ and $\varepsilon$:

$$f(b) = (\varepsilon + b)^{-c_b} \quad \text{(polynomial)}, \qquad f(b) = c_b^{-b} \quad \text{(exponential)}.$$

```pseudo id=main
PROBSAT(F, n, f, MAX-TRIES, MAX-FLIPS)
L1 for t ← 1 to MAX-TRIES do
L2     x ← a uniformly random assignment
L3     for i ← 0 to MAX-FLIPS do
L4         if x satisfies F then return x
L5         C ← a uniformly random false clause
L6         for each variable v of C do w(v) ← f(break(v))
L7         v ← a variable of C, picked with probability w(v) / Σ_u w(u)
L8         flip v in x
L9 return "no model found"
```

Balint and Schöning studied weights that depend on both the make and the break counts and found that leaving out the make count did not hurt, so the rule above uses only break. They reported tuned values per clause size: for 3-SAT the polynomial form with $c_b = 2.38$ and $\varepsilon = 1$, and for larger $k$ the exponential form with larger $c_b$. These values come from experiments. The implementation uses the 3-SAT values by default, the same data structure as [WalkSAT](/walksat/), and MAX-FLIPS $= 100n$. The original solver usually runs one try with no flip limit.

## Example

Take the six clauses of the WalkSAT page,

$$(x_2 \vee x_3 \vee \neg x_4) \wedge (x_1 \vee x_3 \vee x_4) \wedge (x_1 \vee \neg x_3) \wedge (\neg x_1 \vee x_3) \wedge (\neg x_1 \vee x_2) \wedge (\neg x_3 \vee x_4),$$

with models $0101$ and $1111$, and use the polynomial form with $c_b = 2.38$ and $\varepsilon = 1$. Start from $x = 0000$. The only false clause is $(x_1 \vee x_3 \vee x_4)$.

| variable | break | weight $(1 + b)^{-2.38}$ | probability |
|---|---|---|---|
| $x_1$ | 2 | $3^{-2.38} \approx 0.0732$ | $0.2162$ |
| $x_3$ | 2 | $3^{-2.38} \approx 0.0732$ | $0.2162$ |
| $x_4$ | 1 | $2^{-2.38} \approx 0.1921$ | $0.5675$ |

Say $x_4$ wins. Now $x = 0001$ and the only false clause is $(x_2 \vee x_3 \vee \neg x_4)$, with breaks 0, 1 and 1 for $x_2$, $x_3$ and $x_4$. The weights are $1$, $0.1921$ and $0.1921$, so $x_2$ is flipped with probability $0.7224$, and then $x = 0101$ is a model. WalkSAT would flip $x_2$ here with probability 1, because its break is 0; probSAT also gives the other two a chance.

## Correctness

Line L4 returns only an assignment with no false clause, so each answer is a model, and the loops are bounded, so probSAT stops. Each flip is on a variable of a false clause, so it makes that clause true. The proof file shows these facts, that the probabilities of line L7 are as stated, and one more exact property: all weights are positive, so from any assignment there is a probability at least $q^n$, with $q = f(B)/(k f(0))$ and $B$ the largest number of occurrences of a variable, of walking straight to a fixed model in $n$ flips. Hence a single try with no flip limit finds a model of a satisfiable formula with probability 1. This bound is exponentially weak and is not a speed claim.

For $c_b = 0$ the choice is uniform, and the bound of [Schöning's algorithm](/schoning-algorithm/) holds: $O^*((2(k-1)/k)^n)$ expected time with restarts every $3n$ flips. For the tuned values, no better bound is proved, and the speed is measured.

## Complexity

The set-up of line L2 costs $O(mk)$. Each flip computes at most $k$ break counts, each by a scan of at most $d$ clauses, and the flip updates at most $d$ clauses, so a try costs $O(fkd + mk)$ and the worst case time is $O(t(fkd + mk))$. Solvers keep the break counts up to date and precompute the weights for each possible break value, which makes the choice $O(k)$ per flip. The space is $O(n + mk)$.

The number of flips needed is the real cost, and it is measured.

## Properties

- **Incomplete.** It cannot prove unsatisfiability, and it may miss models within its limits.
- **No special cases.** No freebie rule, no noise coin, no tie rule, and no tabu list: one distribution covers all moves.
- **Never trapped.** Every variable of the chosen clause has a positive probability, which gives completeness in the limit (Theorem 2 of the proof file).
- **Few parameters.** Only $c_b$ and, in the polynomial form, $\varepsilon$.

## Variants and improvements

- **Make and break.** The general rule of the 2012 paper uses $f(\mathrm{make}, \mathrm{break})$, such as $c_m^{\mathrm{make}} / c_b^{\mathrm{break}}$. The authors reported that $c_m = 1$, which removes make, was as good.
- **Schöning's walk.** With $c_b = 0$ every variable has the same weight.
- **Restarts and caching.** Solvers based on probSAT keep break values in arrays and add restarts.
- **Parallel and hybrid solvers.** probSAT was combined with other methods in later SAT competition solvers, and it is a common phase in hybrid solvers that alternate local search with [CDCL](/cdcl/).

## When to use it

Use probSAT on large satisfiable uniform random $k$-CNF formulas, where it was among the strongest methods in reported competitions, and as a simple baseline for local search. It is easy to code and has few parameters. For structured formulas from industry, and whenever "unsatisfiable" must be proved, use a [CDCL](/cdcl/) solver.

## Pitfalls

- **Treating "no model found" as UNSAT.** probSAT never proves unsatisfiability.
- **$\varepsilon = 0$ in the polynomial form.** Then a break of 0 gives an infinite weight. Use $\varepsilon > 0$, or treat break 0 as a freebie move on purpose.
- **$c_b < 1$ in the exponential form.** Then the weights grow with break, and the search favors bad moves.
- **Tuned values out of context.** The reported $c_b$ values were tuned for uniform random formulas of a given $k$; other formulas may need other values.
- **Repeated literals.** A clause such as $(x_1 \vee x_1 \vee x_2)$ must be reduced first, or the break counts are wrong.

## Implementations

## History

Selman, Kautz and Cohen's [WalkSAT](/walksat/) of 1994 fixed the idea of flipping only variables of a false clause, and Schöning's 1999 analysis showed that a uniform choice among them gives a proved exponential bound. Balint and Schöning asked, at SAT 2012, which distribution over the variables of the clause is best. They tested functions of make and break, found that break alone was enough, and reported that the resulting probSAT beat the solvers they compared against on random 3-SAT, 5-SAT and 7-SAT. These are measured results. probSAT and its variants did well in the random tracks of later SAT competitions.

## References
