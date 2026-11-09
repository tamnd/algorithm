---
tag: ECTVB1
kind: algorithm
slug: ppsz-algorithm
name: PPSZ algorithm
aliases:
- Paturi-Pudlak-Saks-Zane algorithm
- PPSZ
area: logic-and-constraints/sat-solving
level: research
summary: Randomized k-SAT algorithm. Add short resolvents, then set variables in random order, using a unit clause when one applies and a coin flip otherwise. About 1.3071^n for 3-SAT.
solves: [k-sat, 3-sat]
model: word-ram
complexity:
  vars: {n: the number of variables, k: the largest clause size, s: the bound on the size of resolvents, g: the number of clauses after resolution, c: "the PPSZ constant mu_k/(k-1), which is 2 - 2 ln 2 for k = 3"}
  time: {expected: "O(2^((1 - c) n + o(n)))"}
  space: {extra: O(g s)}
properties: {deterministic: false, exact: false}
history:
  year: 1998
  people: [Ramamohan Paturi, Pavel Pudlák, Michael E. Saks, Francis Zane]
  note: Presented at FOCS 1998, extending the PPZ algorithm of 1997 by bounded resolution; the journal version appeared in 2005, and Hertli extended the unique-SAT bound to all formulas in 2011.
prereqs: [k-sat, robinson-resolution, unit-propagation, linearity-of-expectation]
see_also: [schoning-algorithm, 3-sat, strong-exponential-time-hypothesis, exact-exponential-algorithms, monte-carlo-algorithm, davis-putnam-elimination, backbone]
sources:
  - paper: doi:10.1145/1066100.1066101
    title: Ramamohan Paturi, Pavel Pudlák, Michael E. Saks and Francis Zane, An improved exponential-time algorithm for k-SAT, Journal of the ACM 52(3), 337 to 364 (2005)
    locator: the algorithm, the constants mu_k, and the bounds for unique and general k-SAT
  - paper: "Ramamohan Paturi, Pavel Pudlák and Francis Zane, Satisfiability coding lemma, Proceedings of the 38th IEEE Symposium on Foundations of Computer Science (FOCS 1997), 566 to 574"
    locator: the PPZ algorithm and the critical clause argument
  - paper: doi:10.1137/120868177
    title: Timon Hertli, 3-SAT faster and simpler, unique-SAT bounds for PPSZ hold in general, SIAM Journal on Computing 43(2), 718 to 729 (2014)
    locator: the main theorem (the unique-SAT bounds of PPSZ hold for all satisfiable formulas)
  - paper: "Thomas Dueholm Hansen, Haim Kaplan, Or Zamir and Uri Zwick, Faster k-SAT algorithms using biased-PPSZ, Proceedings of the 51st ACM Symposium on Theory of Computing (STOC 2019), 578 to 589"
    locator: the improved bounds for 3-SAT and 4-SAT
  - paper: doi:10.1006/jcss.2000.1727
    title: Russell Impagliazzo and Ramamohan Paturi, On the complexity of k-SAT, Journal of Computer and System Sciences 62(2), 367 to 375 (2001)
    locator: the exponential time hypothesis and the constants s_k
---

PPSZ is a randomized algorithm for [k-SAT](/k-sat/) by Paturi, Pudlák, Saks and Zane. It first adds to the formula all [resolvents](/robinson-resolution/) with at most $s$ literals. Then, in each try, it goes through the variables in a random order: if the clauses and the values set so far force the next variable by a unit clause, it takes the forced value, and else it flips a coin. For [3-SAT](/3-sat/) a try succeeds with probability at least $2^{-(2 \ln 2 - 1) n - o(n)}$, so the expected time is about $1.3071^n$. This was proved first for formulas with one model, and Hertli (2014) proved it for all satisfiable formulas. With small later gains, it is still the base of the best known bounds for 3-SAT. Like [Schöning's algorithm](/schoning-algorithm/), it has one-sided error and cannot prove that a formula has no model.

## In plain words

You must set many switches so that a list of rules all hold. Go through the switches in a random order. For each one, look at the rules: if some rule now fails unless this switch goes a certain way, set it that way. If no rule says anything, flip a coin. At the end, check the result, and if it is wrong, start again with a new order.

The coin flips are the risky part, and the rules save some of them. If only one correct setting exists, each switch has a rule that depends on it, and that rule decides the switch whenever it comes last in the rule. Before the start, the method also derives extra short rules from pairs of rules, so that switches are decided more often. For three switches per rule this saves enough coin flips that about $1.31^n$ restarts suffice.

## The problem

The input is a CNF formula $F$ with $n$ variables and clauses of at most $k$ literals, a bound $s$ on the size of resolvents, and a number of tries $T$. The output is a model of $F$, or "no model found". If $F$ has no model, the answer is always "no model found". If $F$ has a model, the answer is a model with probability at least $1 - (1 - p)^T$, where $p$ is the success probability of one try.

## The algorithm

```pseudo id=main
PPSZ(F, n, s, T)
L1 G ← F plus all resolvents of at most s literals, repeated until none is new
L2 for t ← 1 to T do
L3     π ← a uniformly random order of x1, ..., xn
L4     for each variable v in the order π do
L5         if some clause of G is a unit clause (ℓ) on v under the values set so far then
L6             give v the value that makes ℓ true          ▷ forced
L7         else give v a uniformly random value            ▷ guessed
L8     if x satisfies F then return x
L9 return "no model found"
```

Line L1 is *$s$-bounded resolution*: for two clauses $C \ni x$ and $D \ni \neg x$ of $G$, the resolvent $(C \setminus \{x\}) \cup (D \setminus \{\neg x\})$ is added when it has at most $s$ literals, is not a tautology, and is new. Each resolvent is implied by $F$, so $G$ has the same models as $F$. With $s = 0$ no resolvent is added, and the algorithm is the earlier PPZ algorithm of Paturi, Pudlák and Zane (1997).

Line L5 is a test of one step of [unit propagation](/unit-propagation/): a clause of $G$ that contains a literal $\ell$ of $v$, whose other literals are all set and all false. The implementation keeps for each variable the list of clauses of $G$ that contain it, and checks these clauses when the variable comes up. Its default is $s = k$, which keeps $G$ small; the proved bound for PPSZ needs $s$ to grow slowly with $n$.

## Example

Take the seven clauses over $x_1, x_2, x_3$ with all sign patterns except $(\neg x_1 \vee x_2 \vee x_3)$. Each clause rules out one assignment, so the only model is $a = 100$.

**Without resolution ($s = 0$).** Take the order $x_2, x_3, x_1$, and suppose the coins give the values of $a$.

| step | variable | clauses that are unit on it | action | value |
|---|---|---|---|---|
| 1 | $x_2$ | none, since nothing is set | guess | 0 |
| 2 | $x_3$ | none, since each clause with $x_3$ also has $x_1$, which is not set | guess | 0 |
| 3 | $x_1$ | $(x_1 \vee x_2 \vee x_3)$, since $x_2 = x_3 = 0$ | forced | 1 |

The try returns $100$ if both guesses are right, with probability $1/4$. For this formula the last variable of each order is forced, whatever the order, because for each pair of values of the first two variables some clause has these two literals false. So one try succeeds with probability exactly $1/4$, which is the bound $2^{-(1 - 1/k) n} = 2^{-2}$ of the PPZ analysis for $k = n = 3$. The tests check this number by trying all 6 orders.

**With resolution ($s = 3$).** Resolving $(x_1 \vee x_2 \vee x_3)$ with $(x_1 \vee \neg x_2 \vee x_3)$ on $x_2$ gives $(x_1 \vee x_3)$. Resolving $(x_1 \vee x_2 \vee \neg x_3)$ with $(x_1 \vee \neg x_2 \vee \neg x_3)$ gives $(x_1 \vee \neg x_3)$. These two resolvents give the unit clause $(x_1)$. In the same way line L1 derives $(\neg x_2)$ and $(\neg x_3)$. Now every variable is forced at line L5 in every order, and one try succeeds with probability 1. This is the effect of resolution: it turns guesses into forced values.

## Correctness

Line L8 returns only models, so a returned assignment is always right, and on a formula with no model the algorithm reaches line L9.

The bound on the chance of success uses *critical clauses*. Suppose $F$ has exactly one model $a$. Flipping any variable $v$ in $a$ gives a non-model, so some clause $C_v$ is true under $a$ only because of its literal of $v$. In a try whose guesses agree with $a$, every forced value also agrees with $a$, since each clause of $G$ is implied by $F$. When $v$ comes after the other variables of $C_v$ in the order, $C_v$ is a unit clause and forces $v$. This happens with probability at least $1/k$, so on average at least $n/k$ variables are forced, and only the other variables need lucky coins. Jensen's inequality turns this into the PPZ bound

$$\Pr[\text{one try succeeds}] \ \ge\ 2^{-(1 - 1/k) n}.$$

The full proof of this bound and of the soundness of forced values is in the proof file of this page.

**The PPSZ bound (cited).** With bounded resolution and $s$ growing slowly with $n$, Paturi, Pudlák, Saks and Zane show that a variable is forced with probability at least $\mu_k / (k-1) - o(1)$, where

$$\mu_k = \sum_{j \ge 1} \frac{1}{j \, (j + \frac{1}{k-1})}.$$

The idea is a tree of critical clauses: $v$ has a critical clause, each other variable of that clause has its own critical clause, and so on. Place each variable at a uniformly random time in $[0, 1]$. If $v$ is at time $r$, and every path down the tree meets a variable placed before $r$, then resolution along the tree has derived a clause that forces $v$. For $k = 3$ the probability $Q(r)$ of such a cut in a deep tree is the smallest root of $Q = (r + (1 - r) Q)^2$, which is $r^2/(1-r)^2$ for $r \le 1/2$ and 1 above, and $\int_0^1 Q(r)\, dr = 2 - 2 \ln 2 \approx 0.6137$. So about $61\%$ of the variables are forced, against $1/3$ for PPZ, and one try succeeds with probability $2^{-(2 \ln 2 - 1) n - o(n)} \approx 1.3071^{-n}$. For formulas with many models, the original paper had a weaker bound for 3-SAT, about $1.362^n$; Hertli (2014) showed that the unique-SAT bound holds for all satisfiable formulas.

## Complexity

Line L1 adds at most $\sum_{i \le s} \binom{n}{i} 2^i \le (2n + 1)^s$ clauses, so it takes $n^{O(s)}$ time; this is polynomial for fixed $s$, and $2^{o(n)}$ when $s$ grows slowly enough. A try checks each clause of $G$ once for each of its variables, in $O(g s^2)$ time, where $g$ is the number of clauses of $G$. The number of tries until the first success is geometric with mean at most $1/p$. So the expected time is

$$2^{(1 - \mu_k/(k-1)) n + o(n)},$$

which is $O(1.3071^n)$ for 3-SAT, about $O(1.469^n)$ for 4-SAT, and $2^{(1 - \Theta(1/k)) n}$ in general, since $\mu_k$ tends to $\pi^2/6$. For PPZ the bound is $O^*(2^{(1 - 1/k) n})$, which is $O(1.588^n)$ for 3-SAT. The extra space is $O(g s)$ for $G$ and its lists of occurrences.

## Properties

- **One-sided error.** "Model found" is always right; "no model found" is wrong with probability at most $(1-p)^T$.
- **No local search.** Unlike [Schöning's algorithm](/schoning-algorithm/), a try builds one assignment in one pass and never changes a value.
- **Unique models are the hard case.** For PPZ and PPSZ, the analysis is simplest when the model is unique, and Hertli showed that many models do not make the bound worse.
- **Fits the hypotheses.** Its bound $2^{(1 - \Theta(1/k)) n}$ has the form that the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) predicts to be close to the truth for large $k$.

## Variants and improvements

- **PPZ.** The version without resolution, with the bound $O^*(2^{(1 - 1/k) n})$.
- **Implication by small subformulas.** Later expositions replace bounded resolution by a direct rule: $v$ is forced if some set of at most $D$ clauses of $F$, under the values set so far, implies the value of $v$. With $D$ growing slowly the same bounds hold.
- **Biased PPSZ.** Hansen, Kaplan, Zamir and Zwick (2019) guess with a bias toward values that are more likely and get a small gain for 3-SAT and 4-SAT, to about $1.30698^n$ for 3-SAT.
- **Combinations with Schöning's walk.** Before Hertli's result, the best bounds for general 3-SAT came from running PPSZ and [Schöning's algorithm](/schoning-algorithm/) together (Iwama and Tamaki 2004, and later work).
- **Derandomization.** For formulas with one model, PPSZ has been derandomized with a small loss in the base; a full derandomization for all formulas is not known.

## When to use it

Use it in theory: it gives the best known worst-case bounds for $k$-SAT, and its critical clause argument is a standard tool for exponential algorithms and for lower bounds on depth-3 circuits. For real formulas, use a [CDCL](/cdcl/) solver: its unit propagation and learned clauses do the work of lines L5 and L1 far better in practice, and it also proves unsatisfiability. For 2-SAT use the [2-SAT algorithm](/two-sat-algorithm/).

## Pitfalls

- **Large $s$.** The closure of line L1 can have about $(2n)^s$ clauses. The proved bound needs $s$ to grow only very slowly; in code, a small fixed $s$ such as $k$ is the practical choice, and it keeps the PPZ guarantee.
- **Forcing from the wrong formula.** Line L5 must use the unit clauses of $G$ under the current partial values. Using full unit propagation is allowed and can only help, but the value of a variable must be set when the variable comes up in the order, not before, or the analysis no longer applies.
- **Treating "no model found" as a proof.** As with all one-sided algorithms, use a complete method to prove that a formula has no model. If line L1 derives the empty clause, that is a proof.

## Implementations

## History

Paturi, Pudlák and Zane (1997) gave PPZ with the satisfiability coding lemma: a formula with isolated models has short encodings of its models, which bounds the number of guesses. Paturi, Pudlák, Saks and Zane added bounded resolution at FOCS 1998, and the journal version appeared in 2005. Their bound for formulas with one model was about $1.3071^n$ for 3-SAT, and for general formulas it was weaker. Hertli (FOCS 2011, journal version 2014) proved that the unique-SAT bound holds in general, and Hansen, Kaplan, Zamir and Zwick (2019) improved it slightly with biased guesses.

## References
