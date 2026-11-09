---
tag: Z5V564
kind: concept
slug: satisfiability-threshold
name: Satisfiability threshold
aliases:
- phase transition of random k-SAT
- k-SAT threshold
- satisfiability threshold conjecture
area: logic-and-constraints/sat-solving
level: research
summary: The clause-to-variable ratio at which random k-SAT jumps from satisfiable to unsatisfiable. Sharp (Friedgut 1999); exactly 1 for k = 2; located for large k by Ding, Sly and Sun.
prereqs: [k-sat, 3-sat, 2-sat, markov-inequality, erdos-renyi-model]
see_also: [k-sat, 3-sat, 2-sat, survey-propagation, xor-sat, probabilistic-method, backbone, walksat]
sources:
  - paper: doi:10.1090/S0894-0347-99-00305-7
    title: "Ehud Friedgut, Sharp thresholds of graph properties, and the k-sat problem, Journal of the American Mathematical Society 12 (1999), 1017 to 1054"
    locator: the existence of a sharp threshold sequence for random k-SAT, without its location
  - paper: doi:10.4007/annals.2022.196.1.1
    title: "Jian Ding, Allan Sly and Nike Sun, Proof of the satisfiability conjecture for large k, Annals of Mathematics 196 (2022), 1 to 388"
    locator: the exact threshold for k at least a large constant k0, given by the one-step replica symmetry breaking formula
  - paper: doi:10.1109/SFCS.1992.267789
    title: "Vasek Chvátal and Bruce Reed, Mick gets some (the odds are on his side), Proceedings of the 33rd IEEE Symposium on Foundations of Computer Science (FOCS 1992), 620 to 627"
    locator: the 2-SAT threshold at ratio 1, and bounds for k-SAT
  - paper: doi:10.1006/jcss.1996.0081
    title: "Andreas Goerdt, A threshold for unsatisfiability, Journal of Computer and System Sciences 53 (1996), 469 to 486"
    locator: the 2-SAT threshold at ratio 1
  - paper: "Wenceslas Fernandez de la Vega, On random 2-SAT, manuscript (1992); see also Random 2-SAT: results and problems, Theoretical Computer Science 265 (2001), 131 to 146"
    locator: the 2-SAT threshold at ratio 1
  - paper: doi:10.1090/S0894-0347-04-00464-3
    title: "Dimitris Achlioptas and Yuval Peres, The threshold for random k-SAT is 2^k log 2 - O(k), Journal of the American Mathematical Society 17 (2004), 947 to 973"
    locator: the weighted second moment lower bound
  - paper: doi:10.1016/j.aim.2015.11.007
    title: "Amin Coja-Oghlan and Konstantinos Panagiotou, The asymptotic k-SAT threshold, Advances in Mathematics 288 (2016), 985 to 1068"
    locator: bounds that agree up to o_k(1) with 2^k ln 2 - (1 + ln 2)/2
  - paper: doi:10.1126/science.1073287
    title: "Marc Mézard, Giorgio Parisi and Riccardo Zecchina, Analytic and algorithmic solution of random satisfiability problems, Science 297 (2002), 812 to 815"
    locator: the cavity method prediction of about 4.267 for 3-SAT
  - paper: doi:10.1002/rsa.20090
    title: "Stephan Mertens, Marc Mézard and Riccardo Zecchina, Threshold values of random K-SAT from the cavity method, Random Structures and Algorithms 28 (2006), 340 to 371"
    locator: the predicted values 4.2667 for k = 3 and for larger k
  - paper: doi:10.1016/j.tcs.2009.02.020
    title: "Josep Díaz, Lefteris Kirousis, Dieter Mitsche and Xavier Pérez-Giménez, On the satisfiability threshold of formulas with three literals per clause, Theoretical Computer Science 410 (2009), 2920 to 2934"
    locator: the upper bound 4.4898 for 3-SAT
  - paper: "David Mitchell, Bart Selman and Hector Levesque, Hard and easy distributions of SAT problems, Proceedings of the 10th National Conference on Artificial Intelligence (AAAI-92), 459 to 465"
    locator: the peak of DPLL running time near the threshold of random 3-SAT
---

The satisfiability threshold is the ratio $\alpha = m/n$ of clauses to variables at which a random [$k$-CNF](/k-sat/) formula changes, with high probability, from satisfiable to unsatisfiable. Friedgut (1999) proved that the change is sharp, but his theorem does not say where it happens, and it does not even say that the location converges as $n$ grows. For $k = 2$ the threshold is exactly $\alpha = 1$ (Chvátal and Reed; Goerdt; Fernandez de la Vega). For $k$ at least a large constant, Ding, Sly and Sun proved that it is a constant $\alpha^*_k = 2^k \ln 2 - (1 + \ln 2)/2 + o_k(1)$, the value predicted by the cavity method of statistical physics. For $k = 3$ the location is not proved: it is known to lie between about $3.52$ and $4.4898$, and the value $4.267$ is a cavity method prediction, not a theorem. Near the threshold, random formulas are hardest for complete solvers.

## In plain words

Take $n$ yes-or-no switches and make rules at random, each rule naming $k$ switches and saying "at least one of these must be in the given position". With few rules, it is almost always possible to obey all of them. With many rules, it is almost never possible. The surprise is how sudden the change is: as the number of rules per switch grows past a certain value, the chance of a solution falls from nearly 1 to nearly 0, and the fall gets steeper as $n$ grows. For rules on 3 switches, experiments put this value near 4.27 rules per switch, but nobody has proved it.

## The idea

**The model.** $F_k(n, m)$ has $m$ clauses, chosen independently. Each clause takes $k$ distinct variables uniformly at random and negates each one with probability $1/2$. Write $m = \alpha n$ and let $P_k(n, \alpha)$ be the probability that $F_k(n, \alpha n)$ is satisfiable. It decreases in $\alpha$, since adding clauses can only remove models.

**Sharp threshold (Friedgut 1999).** For each $k \ge 2$ there is a sequence $r_k(n)$ such that for every $\varepsilon > 0$,

$$P_k(n, \alpha) \to 1 \text{ if } \alpha \le (1 - \varepsilon)\, r_k(n), \qquad P_k(n, \alpha) \to 0 \text{ if } \alpha \ge (1 + \varepsilon)\, r_k(n).$$

The proof is a general criterion for monotone properties of random structures: a property with a coarse threshold can be approximated by the presence of a small fixed substructure, and Friedgut showed that satisfiability cannot be. The theorem gives no value for $r_k(n)$ and does not show that it converges. The *satisfiability threshold conjecture* says that $r_k(n)$ tends to a constant $\alpha^*_k$. A useful consequence of the theorem: to prove that $\alpha$ is below the threshold, it is enough to show that $P_k(n, \alpha)$ stays bounded away from 0.

**Upper bound by the first moment.** Let $X$ be the number of models. A fixed assignment satisfies a random clause with probability $1 - 2^{-k}$, independently for each clause, so

$$\mathbb{E}[X] = 2^n (1 - 2^{-k})^{\alpha n} = \Big(2 (1 - 2^{-k})^{\alpha}\Big)^n.$$

By [Markov's inequality](/markov-inequality/), $\Pr[X \ge 1] \le \mathbb{E}[X]$, which tends to 0 when $2 (1 - 2^{-k})^\alpha < 1$, that is, when

$$\alpha > \frac{\ln 2}{-\ln(1 - 2^{-k})}.$$

The right side is less than $2^k \ln 2$, since $-\ln(1 - x) > x$. For $k = 3$ this gives $\alpha > 5.191$. The bound is not tight, because $X$ is very large on a few formulas and 0 on most: models come in big correlated clusters. Better upper bounds count only special models, for example those where no single flip to a true value gives another model; this is how the bound $4.4898$ for 3-SAT was reached (Díaz, Kirousis, Mitsche and Pérez-Giménez 2009).

**Lower bounds.** Two methods give lower bounds.

- *Algorithms.* If a simple algorithm, such as unit clause propagation with a good choice rule, finds a model with probability bounded away from 0 at ratio $\alpha$, then $\alpha$ is below the threshold, by Friedgut's theorem. Its run can be analyzed with differential equations. This gives $3.52$ for 3-SAT (Kaporis, Kirousis and Lalas; Hajiaghayi and Sorkin). For large $k$, the best such algorithms work only up to about $2^k \ln k / k$, far below $2^k \ln 2$.
- *The second moment.* By the Paley-Zygmund inequality, $\Pr[Y > 0] \ge \mathbb{E}[Y]^2 / \mathbb{E}[Y^2]$ for a nonnegative random variable $Y$. For $Y = X$ this fails, because the number of true literals correlates pairs of models. Achlioptas and Moore applied it to not-all-equal models, which are symmetric under negation, and got $2^{k-1} \ln 2 - O(1)$. Achlioptas and Peres (2004) weighted each model by its number of true literals and got $2^k \ln 2 - O(k)$, the right leading term.

**The exact threshold for large $k$.** Coja-Oghlan and Panagiotou (2016) narrowed the gap to $o_k(1)$ around $2^k \ln 2 - (1 + \ln 2)/2$. Ding, Sly and Sun (STOC 2015; Annals of Mathematics 2022) proved the satisfiability threshold conjecture for all $k \ge k_0$, where $k_0$ is a large constant that they do not compute: $\alpha^*_k$ exists and equals the value given by the one-step replica symmetry breaking formula of physics. Their proof counts clusters of models, as the cavity method does.

**$k = 2$.** A 2-CNF formula is unsatisfiable exactly when its implication graph has a path from some $x$ to $\neg x$ and back. For $\alpha < 1$, the implication graph behaves like a subcritical [random graph](/erdos-renyi-model/) and such paths are unlikely; for $\alpha > 1$, a giant structure appears and they are likely. So $r_2(n) \to 1$ (Chvátal and Reed 1992; Goerdt 1996; Fernandez de la Vega). Bollobás, Borgs, Chayes, Kim and Wilson (2001) showed that the transition happens in a window of width $\Theta(n^{-1/3})$ around 1.

**Predictions from physics.** The cavity method of Mézard, Parisi and Zecchina (2002) predicts $\alpha^*_3 \approx 4.2667$ (Mertens, Mézard and Zecchina 2006), and it predicts that below the threshold the models break into many separated clusters. These numbers for small $k$ are not proved. The same theory led to the [survey propagation](/survey-propagation/) algorithm. For large $k$, clustering has been proved (Achlioptas and Coja-Oghlan 2008) from about $2^k \ln k / k$, which is near the ratio where known efficient algorithms stop.

**Hardness peak.** For complete solvers such as [DPLL](/dpll/), random 3-SAT formulas are easy far below the threshold, where a model is found quickly, and far above it, where a short refutation exists. Near $\alpha \approx 4.3$ the running time peaks (Mitchell, Selman and Levesque 1992). Random formulas at the threshold are a standard test of solvers.

## Examples

**The first moment numbers.** For $k = 2, 3, 4, 5$, the first moment bound $\ln 2 / (-\ln(1 - 2^{-k}))$ is about $2.41$, $5.19$, $10.74$ and $21.83$. For $k = 2$ the true threshold is 1, much lower; for $k = 3$ the predicted value $4.267$ is also clearly lower. For large $k$, the bound is $2^k \ln 2 - (\ln 2)/2 + o_k(1)$, which differs from the true $\alpha^*_k$ by only about $1/2$.

**A measured experiment.** These counts are measured, from one run of a scratch script with Python's `random.Random`. Each formula has $m = \mathrm{round}(\alpha n)$ clauses; each clause takes $k$ distinct variables with `rng.sample` and a sign for each with `rng.choice`. 3-SAT formulas were decided with a DPLL solver with unit propagation, and 2-SAT formulas with the [2-SAT algorithm](/two-sat-algorithm/). The tables give the number of satisfiable formulas.

3-SAT, 100 formulas per cell, seed $1000 n + \mathrm{round}(100 \alpha)$:

| $n$ | $\alpha = 3.0$ | $3.5$ | $4.0$ | $4.27$ | $4.5$ | $5.0$ | $6.0$ |
|---|---|---|---|---|---|---|---|
| 20 | 100 | 98 | 76 | 70 | 52 | 30 | 6 |
| 50 | 100 | 100 | 89 | 55 | 37 | 4 | 0 |

2-SAT, 200 formulas per cell, seed $7 n + \mathrm{round}(100 \alpha)$:

| $n$ | $\alpha = 0.5$ | $0.8$ | $1.0$ | $1.2$ | $1.5$ |
|---|---|---|---|---|---|
| 100 | 200 | 200 | 189 | 169 | 57 |
| 1000 | 200 | 199 | 189 | 65 | 0 |
| 10000 | 200 | 200 | 182 | 0 | 0 |

The curves get steeper as $n$ grows. For 2-SAT the fall is centered near $\alpha = 1$, as the theorem says, and at $n = 10000$ every formula at $\alpha = 1.2$ was unsatisfiable. For 3-SAT, the fraction at $\alpha = 4.27$ is near one half for $n = 50$, which agrees with the prediction, but such small $n$ have large finite-size effects, and these runs do not locate the threshold.

**XOR-SAT.** For random 3-XOR-SAT, where each clause is a parity constraint on 3 variables, the threshold is proved, at about $0.918$ (Dubois and Mandler 2002). The linear structure makes the analysis easier; see [XOR-SAT](/xor-sat/).

## Where it is used

- **Benchmarks.** Random $k$-CNF formulas at the threshold ratio are a standard hard test set for complete and incomplete solvers, and the SAT Competitions have a random track.
- **Local search design.** [WalkSAT](/walksat/), [probSAT](/probsat/) and [survey propagation](/survey-propagation/) are judged by how close to the threshold they solve large random formulas.
- **Probabilistic combinatorics.** The threshold is a test case for sharp threshold theory, the [second moment method](/probabilistic-method/), and the rigorous study of predictions from spin glass physics.
- **Average-case hardness.** Assumptions about random $k$-SAT above the threshold, for example that refuting such formulas is hard at some densities, are used in learning theory and hardness of approximation.
- **Other constraint problems.** Graph coloring, not-all-equal SAT and random constraint satisfaction problems have thresholds studied with the same methods.

## References
