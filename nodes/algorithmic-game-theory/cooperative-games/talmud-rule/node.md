---
tag: J1054R
kind: algorithm
slug: talmud-rule
name: Talmud rule
aliases:
- Aumann-Maschler rule
- contested garment rule
area: algorithmic-game-theory/cooperative-games
level: core
summary: CEA on half the claims while the estate is at most half the total claims, else half claims plus CEL on the other halves. It is the nucleolus of the bankruptcy game (Aumann and Maschler 1985).
solves: [bankruptcy-problem]
model: word-ram
complexity:
  vars: {n: the number of claimants}
  time: {worst: O(n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1985
  people: [Robert J. Aumann, Michael Maschler]
  note: The numbers come from the Mishna (tractate Ketubot, the estate of a man with three wives, and tractate Bava Metzia, the contested garment); Aumann and Maschler found the rule behind them in 1985 and proved that it is the nucleolus.
prereqs: [bankruptcy-problem, nucleolus]
see_also: [nucleolus-sequential-lp, transferable-utility-game, convex-game, core-of-a-cooperative-game, shapley-value]
sources:
  - paper: doi:10.1016/0022-0531(85)90102-4
    title: "Robert J. Aumann and Michael Maschler, Game theoretic analysis of a bankruptcy problem from the Talmud, Journal of Economic Theory 36(2) (1985), 195-213"
    locator: the contested garment rule, the consistent extension to n claimants, its description by half claims, and the theorem that it is the nucleolus of the bankruptcy game
  - paper: doi:10.1016/0165-4896(82)90029-4
    title: "Barry O'Neill, A problem of rights arbitration from the Talmud, Mathematical Social Sciences 2(4) (1982), 345-371"
    locator: the first game theoretic study of the Talmud division problems, and the random arrival rule
  - paper: doi:10.1007/BF02109593
    title: "Imma J. Curiel, Michael Maschler and Stef H. Tijs, Bankruptcy games, Zeitschrift fur Operations Research 31(5) (1987), A143-A159"
    locator: bankruptcy games are convex, and the rules that correspond to solutions of the game
  - paper: doi:10.1016/S0165-4896(02)00070-7
    title: "William Thomson, Axiomatic and game-theoretic analysis of bankruptcy and taxation problems, a survey, Mathematical Social Sciences 45(3) (2003), 249-297"
    locator: the Talmud rule among the main rules, with its axioms (self-duality, consistency, order preservation)
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: Section 20.8, The bankruptcy problem (the Talmud examples and the nucleolus of the bankruptcy game)
  - book: "Bezalel Peleg and Peter Sudholter, Introduction to the Theory of Cooperative Games, 2nd edition, Theory and Decision Library C 34, Springer, 2007"
    title: Introduction to the Theory of Cooperative Games
    locator: Chapter 6, The prenucleolus (the reduced game property of Davis and Maschler, used in the proof that the rule is the nucleolus)
---

The Talmud rule divides an estate among creditors whose claims add up to more than the estate. This page is the rule as an algorithm; the [bankruptcy problem](/bankruptcy-problem/) page states the problem and compares the rules. While the estate is at most half of the total claims, the Talmud rule gives each creditor an equal share, but no creditor more than half its claim. For a larger estate, each creditor first gets half its claim, and the creditors then share the losses equally on the other halves. Aumann and Maschler found this rule in 1985 behind three numerical examples of the Mishna, and they proved that it is the [nucleolus](/nucleolus/) of the bankruptcy game. For two creditors it is the contested garment rule of the Mishna.

## In plain words

A man dies and owes more money than he leaves. If the money is short, think of half of each debt as the part that matters most. When the money covers at most half of all the debts, share it equally, but stop paying a creditor when it has half of its debt, and share the rest among the others. When the money covers more than half, give everyone half of its debt first. Then the creditors share the shortfall equally, and nobody can lose more than the other half of its debt. The two halves are mirror images: what creditors get in one case is what they lose in the other. For two creditors this says: each one gets the part of the money that the other does not claim, and they split the rest equally.

## The problem

The input is a list of claims $c_1, \ldots, c_n \ge 0$ and an estate $E$ with $0 \le E \le C$, where $C = c_1 + \cdots + c_n$. The output is an award vector $x$ with $x_1 + \cdots + x_n = E$ and $0 \le x_i \le c_i$. The bankruptcy game of the problem gives each coalition $S$ of creditors what is left after the creditors outside $S$ are paid in full: $v(S) = \max(0, E - c(N \setminus S))$, where $c(T)$ is the sum of the claims in $T$.

Two simple rules do most of the work. Constrained equal awards (CEA) gives $\min(c_i, \lambda)$, with $\lambda$ chosen so that the awards sum to $E$. Constrained equal losses (CEL) gives $\max(0, c_i - \mu)$, so that every creditor loses the same amount $\mu$ unless it then gets nothing. The Talmud rule is

$$T(c, E) = \begin{cases} \mathrm{CEA}(c/2, E) & \text{if } E \le C/2, \\ c/2 + \mathrm{CEL}(c/2, E - C/2) & \text{if } E \ge C/2. \end{cases}$$

## The algorithm

```pseudo id=main
TALMUD(c, E)
L1  C ← c_1 + ... + c_n
L2  if E ≤ C/2: return CEA(c/2, E)
L3  ℓ ← CEA(c/2, C - E)
L4  return c - ℓ
CEA(d, A)
L5  order the players so that d_1 ≤ d_2 ≤ ... ≤ d_n; rest ← A
L6  for k ← 1 to n:
L7      λ ← rest / (n - k + 1)
L8      if d_k ≤ λ: x_k ← d_k; rest ← rest - d_k
L9      else: x_j ← λ for j = k, ..., n; go to L10
L10 return x, in the original order of the players
```

Lines L3 and L4 use the identity $\mathrm{CEL}(d, B) = d - \mathrm{CEA}(d, \sum_i d_i - B)$: the losses under CEL are equal awards of losses. With $d = c/2$ and $B = E - C/2$ the losses $\ell$ on the half claims add up to $C - E$, and the award is $c/2 + (c/2 - \ell) = c - \ell$. So the second branch is CEA again, applied to the losses.

The procedure CEA is water filling. Line L7 computes the share of each creditor that is not yet paid if the rest is split equally. A creditor whose claim is at most that share is paid in full in line L8, and the share of the others grows. The first creditor whose claim is above the share stops the loop: from there on every claim is above the share, so all the remaining creditors get exactly the share (line L9).

## Example

The Mishna (tractate Ketubot) discusses a man with three wives whose marriage contracts are worth $c = (100, 200, 300)$, so $C = 600$ and $C/2 = 300$. It gives the division for estates of 100, 200 and 300.

- $E = 100$. The half claims are $(50, 100, 150)$. Line L7 gives $\lambda = 100/3 < 50$, so line L9 gives each wife $100/3$.
- $E = 200$. Line L7 gives $\lambda = 200/3 \ge 50$, so wife 1 gets 50, and $\mathit{rest} = 150$. Next, $\lambda = 150/2 = 75 < 100$, so wives 2 and 3 get 75 each: $(50, 75, 75)$.
- $E = 300 = C/2$. Every wife gets half her claim: $(50, 100, 150)$, which here is also the proportional division.
- $E = 400$ (not in the Mishna). Lines L3 and L4 give $\ell = \mathrm{CEA}((50, 100, 150), 200) = (50, 75, 75)$, and the award is $c - \ell = (50, 125, 225)$, the mirror image of $E = 200$.

The table compares the Talmud rule with three other rules on the same claims.

| estate | Talmud | CEA | CEL | proportional |
|---|---|---|---|---|
| 100 | $(100/3, 100/3, 100/3)$ | $(100/3, 100/3, 100/3)$ | $(0, 0, 100)$ | $(50/3, 100/3, 50)$ |
| 200 | $(50, 75, 75)$ | $(200/3, 200/3, 200/3)$ | $(0, 50, 150)$ | $(100/3, 200/3, 100)$ |
| 300 | $(50, 100, 150)$ | $(100, 100, 100)$ | $(0, 100, 200)$ | $(50, 100, 150)$ |
| 400 | $(50, 125, 225)$ | $(100, 150, 150)$ | $(100/3, 400/3, 700/3)$ | $(200/3, 400/3, 200)$ |

The contested garment (tractate Bava Metzia) is the case of two claimants: one claims the whole garment, worth 1, and the other claims half of it. The second claimant does not claim the other half, so the first gets it; the half that both claim is split equally. The result is $(3/4, 1/4)$, and TALMUD$((1, 1/2), 1)$ returns the same: $C = 3/2$, $E = 1 > 3/4$, $\ell = \mathrm{CEA}((1/2, 1/4), 1/2) = (1/4, 1/4)$, and $c - \ell = (3/4, 1/4)$.

## Correctness

The file proofs/correctness.md proves four things. First, lines L5 to L10 compute CEA exactly: the loop keeps the invariant that the creditors paid so far have claims at most the true level $\lambda^*$, and the first claim above the share forces $\lambda^* = \mathit{rest}/(n - k + 1)$. Second, lines L1 to L4 compute $T$ by the identity above. Third, $T$ is consistent with the contested garment rule: for every pair of creditors, the amount they get together is divided between them as the contested garment rule divides it. The proof checks the three cases of $\min(c_k/2, \lambda)$ for a pair below half of $C$, and uses the self-duality of both rules above half. At most one award vector has this property, because the contested garment awards are nondecreasing in the estate. Fourth, the nucleolus of the bankruptcy game is also consistent with the contested garment rule. For this the proof uses the reduced game property of the prenucleolus (Sobolev 1975, in Peleg and Sudholter, Chapter 6), shows that the reduced game of a bankruptcy game on a pair is the bankruptcy game of that pair, and solves the two-player case. So the nucleolus is $T$.

## Complexity

Line L5 sorts the $n$ claims in $O(n \log n)$ time, and the loop of lines L6 to L9 takes $O(n)$ more. Line L1 and line L4 take $O(n)$. The extra space is $O(n)$ for the order and the output. Sorting is not necessary: the level $\lambda$ can be found in $O(n)$ time by repeated median selection, as for a weighted median. Writing the output needs $\Omega(n)$ time, so this is optimal. The code uses exact fractions; with integer claims and estate, every award is an integer divided by $2m$ for some $m \le n$.

## Properties

- **Self-dual.** $T(c, C - E) = c - T(c, E)$: dividing the losses by the rule gives the same result as dividing the estate. The 400 row of the table is the mirror of the 200 row.
- **Consistent.** If some creditors leave with their awards, the rule applied to the others and the money left gives them the same awards. For pairs this is the contested garment property proved on this page.
- **Order preserving.** A larger claim never gets a smaller award or a smaller loss.
- **Half claims are a threshold.** Below $E = C/2$ every award is at most half its claim, and above it every award is at least half its claim.
- **Monotone in the estate.** No creditor gets less when the estate grows.
- **In the core.** As the nucleolus of a convex game, the award vector is in the [core](/core-of-a-cooperative-game/) of the bankruptcy game: no group of creditors gets less than what is left for it after the others are paid in full.

## Variants and improvements

- **Constrained equal awards.** CEA on the full claims, the rule that Maimonides proposed. It protects small claims.
- **Constrained equal losses.** CEL on the full claims. It protects large claims.
- **Proportional rule.** Awards proportional to the claims, $x_i = E c_i / C$. It agrees with the Talmud rule only at $E = C/2$ and in special cases.
- **Random arrival rule.** The creditors arrive in a random order and each is paid in full or with what is left. O'Neill studied it in 1982; it is the [Shapley value](/shapley-value/) of the bankruptcy game, while the Talmud rule is its nucleolus.
- **The general nucleolus.** For other cooperative games, the [sequential LP](/nucleolus-sequential-lp/) computes the nucleolus with exponentially many constraints. The Talmud rule is the fast special case for bankruptcy games, and the tests of the sequential LP check it against these values.

## When to use it

Use the Talmud rule when an estate, a budget or a capacity must be divided among claims that exceed it, and the parties accept the idea that half of each claim is the part to protect first. It is a good choice when the division must not change if a subgroup redivides its share (consistency), and when gains and losses must be treated in the same way (self-duality). If the claims have a natural order of time, the random arrival rule or a priority rule may be a better match. If the law asks for shares proportional to the claims, use the proportional rule.

## Pitfalls

- **CEL in place of CEA below half.** Both branches use the half claims, and the lower branch is CEA, not CEL. Using CEL on the half claims for $E = 200$ gives $(0, 50, 150)$ in place of $(50, 75, 75)$.
- **Full claims in place of half claims.** CEA on the full claims gives $(200/3, 200/3, 200/3)$ for $E = 200$, which is the rule of Maimonides, not the Talmud rule.
- **The upper branch without the half claims.** For $E > C/2$ the award is $c/2$ plus CEL on $c/2$ with the excess $E - C/2$, not CEL on $c$ with $E$. For $E = 400$ the second gives $(100/3, 400/3, 700/3)$.
- **Floating point.** The level $\lambda$ is a ratio, and float rounding can break the exact sum $E$ or the order of equal claims. Use fractions.
- **An estate above the total claims.** The rule needs $E \le C$. The code raises an error otherwise.

## Implementations

## History

The Mishna, compiled around 200 CE, gives the three divisions of the table in tractate Ketubot (in the Babylonian Talmud, Ketubot 93a) and the contested garment in tractate Bava Metzia (Bava Metzia 2a). The garment division is easy to explain, but the estate divisions looked inconsistent: the first is equal, the third is proportional, and the second is neither. O'Neill studied the problem with game theory in 1982. Aumann and Maschler showed in 1985 that all three divisions follow one rule, the unique division that is consistent with the contested garment rule, and that this rule is the nucleolus of the bankruptcy game. Curiel, Maschler and Tijs showed in 1987 that bankruptcy games are convex. Thomson's survey of 2003 places the rule among the main division rules and their axioms.

## References
