---
tag: JTYPN5
kind: algorithm
slug: lipton-markakis-mehta-algorithm
name: Lipton-Markakis-Mehta algorithm
aliases:
- LMM algorithm
- quasi-polynomial approximate Nash
area: algorithmic-game-theory/computing-equilibria
level: advanced
summary: Finds an epsilon-Nash equilibrium in quasi-polynomial time by searching over uniform mixtures of O(log n / epsilon^2) actions.
solves: [nash-equilibrium-computation]
model: real-ram
complexity:
  vars: {n: the larger number of pure strategies of the two players, e: the additive approximation epsilon}
  time: {worst: "n^O(log n / e^2)"}
  space: {extra: "n^O(log n / e^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2003
  people: [Richard J. Lipton, Evangelos Markakis, Aranyak Mehta]
  note: Presented at the ACM Conference on Electronic Commerce in 2003; the sampling argument extends earlier work of Althöfer and of Lipton and Young on zero-sum games.
prereqs: [bimatrix-game, epsilon-nash-equilibrium, hoeffding-inequality, probabilistic-method, nash-existence-theorem]
see_also: [dmp-half-approximate-nash, rubinstein-approximate-nash-lower-bound, support-enumeration, quasi-polynomial-time, ppad-completeness-of-nash, nash-equilibrium-computation, union-bound, planted-clique]
sources:
  - paper: doi:10.1145/779928.779933
    title: "Richard J. Lipton, Evangelos Markakis and Aranyak Mehta, Playing large games using simple strategies, Proceedings of the 4th ACM Conference on Electronic Commerce (EC 2003), 36-41"
    locator: the existence of epsilon-equilibria with k-uniform strategies for k = O(log n / epsilon^2), the quasi-polynomial search, and the approximation of equilibrium payoffs
  - paper: doi:10.1109/FOCS.2016.35
    title: "Aviad Rubinstein, Settling the complexity of computing approximate two-player Nash equilibria, Proceedings of the 57th IEEE Symposium on Foundations of Computer Science (FOCS 2016), 258-265"
    locator: the matching quasi-polynomial lower bound under the exponential time hypothesis for PPAD
  - paper: doi:10.1016/j.tcs.2008.12.031
    title: "Constantinos Daskalakis, Aranyak Mehta and Christos H. Papadimitriou, A note on approximate Nash equilibria, Theoretical Computer Science 410(17) (2009), 1581-1588"
    locator: the remark that sublogarithmic supports cannot give better than 1/2, after Althöfer and Feder, Nazerzadeh and Saberi
---

The Lipton-Markakis-Mehta (LMM) algorithm finds an [epsilon-Nash equilibrium](/epsilon-nash-equilibrium/) of a two-player game in strategic form (a [bimatrix game](/bimatrix-game/)) with payoffs in $[0, 1]$. Its key fact is a sampling theorem: every game has an $\varepsilon$-Nash equilibrium in which each player mixes uniformly over a multiset of only $k = O(\log n / \varepsilon^2)$ pure strategies. The algorithm tries all such pairs and checks each one exactly, which takes $n^{O(\log n / \varepsilon^2)}$ time, [quasi-polynomial](/quasi-polynomial-time/) for every fixed $\varepsilon$. This is far faster than the exponential worst case of exact methods. [Rubinstein's theorem](/rubinstein-approximate-nash-lower-bound/) shows that, under a hypothesis about [PPAD](/ppad/), it cannot be improved much for small constant $\varepsilon$.

## In plain words

Two players each mix many moves with odd weights. Draw a few dozen moves at random from each mix, and let each player pick from its own sample with equal chance. With high probability every move scores about the same against the sample as against the full mix, because averages of many random draws are close to their mean. So a pair of small, plain mixes is almost as stable as a real equilibrium. We do not know the real equilibrium, so we try every pair of small, plain mixes and test each one. The number of tries grows a little faster than any polynomial in the number of moves, but much slower than an exponential.

## The problem

The input is two $m \times n$ matrices $A$ and $B$ with entries in $[0, 1]$ and a number $\varepsilon > 0$. Here $m$ and $n$ are the numbers of pure strategies of the row player and of the column player. With row $r$ and column $c$, the row player gets $A_{rc}$ and the column player gets $B_{rc}$, and both maximize. A pair of mixed strategies $(x, y)$ is an $\varepsilon$-Nash equilibrium if

$$\max_r (Ay)_r - x^{\mathsf T} A y \le \varepsilon \quad\text{and}\quad \max_c (x^{\mathsf T} B)_c - x^{\mathsf T} B y \le \varepsilon.$$

Pure deviations are enough: a mixed strategy is a [best response](/best-response/) if and only if its support is inside the set of pure best responses, and a mixed deviation earns an average of pure deviation payoffs. A strategy is **$k$-uniform** if it is uniform on a multiset of $k$ pure strategies, so that each probability is a multiple of $1/k$. The output is a pair of $k$-uniform strategies that is an $\varepsilon$-Nash equilibrium.

## The algorithm

```pseudo id=main
LMM(A, B, ε)                       ▷ A, B are m by n with entries in [0, 1]
L1  k ← the least integer with k > 2 ln(2(m + n)) / ε²
L2  for each multiset R of k rows
L3      x ← the uniform mix on R, with multiplicity
L4      for each multiset C of k columns
L5          y ← the uniform mix on C, with multiplicity
L6          if max_r (A y)_r - xᵀ A y ≤ ε and max_c (xᵀ B)_c - xᵀ B y ≤ ε
L7              return (x, y)
```

The code computes $k \cdot Ay$ and its maximum once for each column multiset, and $k \cdot x^{\mathsf T} B$ and its maximum once for each row multiset. Then line L6 costs $O(k)$ for a pair, in exact integer and rational arithmetic, with no tolerance. The constant 2 in line L1 comes from the proof below. Other texts state other constants, and any $k$ above the bound works.

## Example

Take rock-paper-scissors with the payoffs scaled to $[0, 1]$: a win gives 1, a draw $1/2$ and a loss 0, and $B = A^{\mathsf T}$. The only equilibrium is the uniform pair, with $k = 3$. The smallest largest gain over all pairs of $k$-uniform strategies is:

| $k$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| best gain | $1/2$ | $1/4$ | 0 | $1/8$ | $1/10$ |

So the search with $\varepsilon = 1/4$ already succeeds with $k = 2$, and the first pair it accepts has both players uniform on $\{\text{rock}, \text{paper}\}$. Against that mix, rock earns $1/4$, paper $3/4$ and scissors $1/2$, so each player earns $1/2$ and gains $1/4$ by a switch to paper. The bound of line L1 is much larger: it gives $k = 17$ for a $2 \times 2$ game with $\varepsilon = 1/2$, and for $\varepsilon = 1/10$ it gives $k = 738$, $1199$ and $1659$ for $n \times n$ games with $n = 10$, $100$ and $1000$. The value grows like $\log n$, but the constant $2/\varepsilon^2$ makes the method useful in theory more than in practice.

## Correctness

Let $(x^*, y^*)$ be a Nash equilibrium, which exists by [Nash's theorem](/nash-existence-theorem/), with payoffs $v_A$ and $v_B$. Draw $k$ rows independently from $x^*$ and $k$ columns from $y^*$, and let $x'$ and $y'$ be uniform on the samples. For a fixed row $r$, $(Ay')_r$ is a mean of $k$ independent values in $[0, 1]$ with mean $(Ay^*)_r$. By the [Hoeffding inequality](/hoeffding-inequality/) it is more than $\varepsilon/2$ away with probability at most $2e^{-k\varepsilon^2/2}$, and the same holds for each column payoff $(x'^{\mathsf T} B)_c$. By the [union bound](/union-bound/), the probability that one of the $m + n$ payoffs is off by $\varepsilon/2$ is at most $2(m + n) e^{-k\varepsilon^2/2} < 1$. So, by the [probabilistic method](/probabilistic-method/), some sample has all of them close.

For that sample, no row earns more than $v_A + \varepsilon/2$ against $y'$. Every sampled row lies in the support of $x^*$, so it earns exactly $v_A$ against $y^*$ by the best-response fact, and at least $v_A - \varepsilon/2$ against $y'$. So $x'$ earns at least $v_A - \varepsilon/2$, and the row gain is at most $\varepsilon$. The column player is the same. So a $k$-uniform $\varepsilon$-Nash equilibrium exists, the loops reach it, and line L6 accepts it. The [proof file](proofs/correctness.md) has the details.

## Complexity

There are $\binom{m+k-1}{k}$ row multisets and $\binom{n+k-1}{k}$ column multisets. With the precomputation, the time is $O\big(\binom{m+k-1}{k}\binom{n+k-1}{k} k + (\binom{m+k-1}{k} + \binom{n+k-1}{k}) k(m + n)\big)$. With $n$ the larger of the two strategy counts and $k = O(\log n / \varepsilon^2)$, this is $n^{O(\log n/\varepsilon^2)}$. The code keeps the column table, which takes $\binom{n+k-1}{k}$ entries of $O(m)$ numbers. Recomputing it for every row multiset gives polynomial space and the same time bound up to a factor $k m$.

For a fixed $\varepsilon$ this is quasi-polynomial. For $\varepsilon = 1/\text{poly}(n)$ it is exponential, and this is expected: finding an $\varepsilon$-Nash equilibrium for $\varepsilon = 1/n^{c}$ is PPAD-complete (Chen, Deng and Teng), see [PPAD-completeness of Nash](/ppad-completeness-of-nash/).

## Properties

- **Small supports.** Each player uses at most $k = O(\log n / \varepsilon^2)$ pure strategies, all with probabilities that are multiples of $1/k$.
- **Payoffs are kept.** For every Nash equilibrium there is a $k$-uniform $\varepsilon$-Nash equilibrium whose two payoffs are each within $\varepsilon/2$ of it. So the search can also approximate the best equilibrium payoffs, for example the best social welfare, up to $\varepsilon$, in the same time.
- **Deterministic.** The randomness is only in the proof. The search is exhaustive and exact.
- **Additive approximation.** The guarantee needs payoffs on the scale $[0, 1]$.

## Variants and improvements

- **Polynomial time for a fixed $\varepsilon$ above $1/3$.** The [DMP algorithm](/dmp-half-approximate-nash/) gives $1/2$ in linear time, and LP-based methods reach $1/3 + \delta$ in polynomial time (Deligkas, Fasoulakis and Markakis, ESA 2022). Whether every constant $\varepsilon > 0$ has a polynomial-time algorithm is open as of November 2026.
- **Lower bounds.** Rubinstein (FOCS 2016) proved that, under the exponential time hypothesis for PPAD, there is a constant $\varepsilon > 0$ such that $\varepsilon$-Nash equilibria of $n \times n$ games need $n^{\log^{1 - o(1)} n}$ time, so LMM is close to optimal for small constants. A 2026 preprint of Golowich claims the full dependence $N^{(\log N / \varepsilon^2)^{1 - o(1)}}$ under stronger conjectures, and it is not yet peer reviewed as of November 2026.
- **Small supports cannot be avoided.** Althöfer (1994) showed games where an approximation needs supports of logarithmic size, and Feder, Nazerzadeh and Saberi (EC 2007) showed that for every $\varepsilon < 1/2$ some games need supports of size $\Omega(\log n)$.
- **Sparse and low-rank games.** Barman (STOC 2015) used an approximate version of Carathéodory's theorem to get smaller supports, and so faster searches, when the matrices have few nonzero entries per column. Lipton, Markakis and Mehta also treat games whose payoff matrices have low rank.
- **Zero-sum games.** For $B = -A$ the same sampling argument goes back to Althöfer (1994) and Lipton and Young (1994), but there a [linear program](/zero-sum-game-linear-programming/) gives an exact answer in polynomial time.
- **Near-optimal equilibria.** Finding an $\varepsilon$-Nash equilibrium whose welfare is near the best one is as hard as finding a [planted clique](/planted-clique/) (Hazan and Krauthgamer), so the quasi-polynomial time is also needed for that question unless planted clique is easier than believed. For exact optimal equilibria see the [hardness of optimal Nash equilibria](/hardness-of-optimal-nash-equilibria/).

## When to use it

Use it in proofs and as an upper bound: it shows that approximate Nash equilibria in two-player games are not PPAD-hard for constant $\varepsilon$ unless PPAD has quasi-polynomial algorithms. Use the search with a small $k$ chosen by hand on small games, and grow $k$ until the gain is small enough, as in the example. For real games of medium size, an exact method such as [Lemke-Howson](/lemke-howson-algorithm/), or a method with a constant bound such as DMP, is faster.

## Pitfalls

- **Taking the bound of line L1 at face value.** It is a worst-case bound for the proof. For $\varepsilon = 1/10$ it already asks for hundreds of samples, and the search over pairs then takes far too long. Small games often succeed with a much smaller $k$.
- **Sets instead of multisets.** The proof samples with replacement, so the strategies are uniform on multisets. Uniform mixes on sets of size $k$ are a smaller family, and the theorem does not cover them.
- **Payoffs outside $[0, 1]$.** Hoeffding's bound uses the range of the payoffs. Scale the payoffs, or multiply $\varepsilon$ by the range.
- **Tolerance in the check.** With floats, a pair can pass line L6 only because of rounding. The code works with integers and rationals and compares exactly.

## Implementations

The Python code follows lines L1 to L7 with exact arithmetic, and also gives the exhaustive minimum of the gain over all $k$-uniform pairs. The tests check the sample size against the bound, matching pennies and rock-paper-scissors for small $k$, the exact mixed equilibrium of battle of the sexes with $k = 3$ and $\varepsilon = 0$, and the agreement of the fast gains with the shared exact checker on every pair. On random games they check that the search with a given $k$ fails exactly when the exhaustive minimum is above $\varepsilon$, and that the search with the $k$ of line L1 always succeeds.

## History

Althöfer (1994) and Lipton and Young (1994) showed that zero-sum games have approximately optimal strategies with small supports, by sampling. Lipton, Markakis and Mehta extended the argument to general two-player games, and to approximate equilibrium payoffs, at the ACM Conference on Electronic Commerce in 2003. After the PPAD-completeness results of 2005 and 2006, the quasi-polynomial algorithm became the main reason to expect that constant approximations are easier than exact equilibria. Rubinstein's 2016 lower bound showed that, under a hypothesis on PPAD, the quasi-polynomial time is close to the truth.

## References
