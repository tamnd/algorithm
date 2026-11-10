---
tag: 2PHH3V
kind: theorem
slug: nearest-codeword-inapproximability
name: Nearest codeword inapproximability
aliases:
- ABSS nearest codeword hardness
- hardness of approximate decoding of linear codes
- min unsatisfied linear equations hardness
area: approximation/hardness-of-approximation
level: research
summary: Nearest codeword is NP-hard to approximate within any constant, and within 2^(log^(1-ε) n) unless NP has quasi-polynomial algorithms (Arora, Babai, Stern and Sweedyk 1997).
prereqs: [nearest-codeword-problem, linear-code, label-cover, hastad-3bit-pcp, gap-problem]
see_also: [cvp-np-hardness, set-cover-inapproximability, parallel-repetition-theorem, two-prover-one-round-game, xor-sat, max-3sat-inapproximability, gap-preserving-reduction]
sources:
  - paper: doi:10.1006/jcss.1997.1472
    title: S. Arora, L. Babai, J. Stern and Z. Sweedyk, The hardness of approximate optima in lattices, codes, and systems of linear equations, Journal of Computer and System Sciences 54(2), 1997
    locator: pages 317 to 331 (nearest codeword within any constant is NP-hard, and within 2^(log^(1-ε) n) is hard unless NP is in quasi-polynomial time)
  - paper: doi:10.1145/502090.502098
    title: Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48(4), 2001
    locator: the gap 1 - ε against 1/2 + ε for equations mod 2 with three variables
  - paper: doi:10.1137/S0097539795280895
    title: Ran Raz, A parallel repetition theorem, SIAM Journal on Computing 27(3), 1998
    locator: the soundness 2^(-ck) of the k-fold repeated game
  - paper: "E. R. Berlekamp, R. J. McEliece and H. C. A. van Tilborg, On the inherent intractability of certain coding problems, IEEE Transactions on Information Theory 24(3), 1978"
    locator: NP-completeness of maximum likelihood decoding of linear codes
  - paper: "I. Dumer, D. Micciancio and M. Sudan, Hardness of approximating the minimum distance of a linear code, IEEE Transactions on Information Theory 49(1), 2003"
    locator: the minimum distance problem within any constant is hard under RP ≠ NP
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 10, by S. Arora and C. Lund (label cover and the problems that reduce from it)
---

The nearest codeword inapproximability theorem says that, for a general binary linear code, finding a codeword close to a received word is hard even approximately. Arora, Babai, Stern and Sweedyk (ABSS) proved in 1993 that no constant ratio is possible unless P = NP, and that a ratio of $2^{\log^{1 - \varepsilon} n}$ would put NP in quasi-polynomial time. The problem is the same as finding an assignment that makes the fewest equations mod 2 false. This page proves the constant bound from Håstad's theorem for such equations, and gives the reduction from [label cover](/label-cover/) behind the larger bound, with its soundness proof. The exact NP-hardness is on the [nearest codeword problem](/nearest-codeword-problem/) page.

## Statement

A [binary linear code](/linear-code/) of length $n$ and dimension $k$ is $C = \{ A x : x \in \mathbb{F}_2^k \}$ for a matrix $A \in \mathbb{F}_2^{n \times k}$. In the **nearest codeword problem** (NCP), the input is $A$ and a word $y \in \mathbb{F}_2^n$, and the goal is an $x$ that makes the Hamming weight $\lvert A x - y \rvert$ least. $\mathrm{OPT}$ is this least weight, the distance from $y$ to $C$. It is a minimization problem, so a ratio $\rho \ge 1$ means a codeword at distance at most $\rho \cdot \mathrm{OPT}$ on every instance.

Row $i$ of $A x = y$ is a linear equation $\langle a_i, x \rangle = y_i$ over $\mathbb{F}_2$, and $\lvert A x - y \rvert$ is the number of false equations. So NCP is the problem of finding an assignment that makes the fewest equations false, with the $n$ equations as the code length. The code for this page builds this map and checks it by brute force.

**Theorem 1 (constant ratios).** For each constant $\rho \ge 1$, a polynomial algorithm for NCP with ratio $\rho$ gives P = NP.

**Theorem 2 (Arora, Babai, Stern and Sweedyk 1997).** For each $\varepsilon > 0$, a polynomial algorithm for NCP with ratio $2^{\log^{1 - \varepsilon} n}$ gives $\mathrm{NP} \subseteq \mathrm{DTIME}(2^{\mathrm{polylog}(n)})$.

**Lemma 3 (label cover to NCP).** Let $L$ be a label cover instance with left vertices $U$, right vertices $W$, label sets $\Sigma_U$ and $\Sigma_W$, and a projection $\pi_e : \Sigma_U \to \Sigma_W$ on each edge $e$. A **total cover** gives each vertex $v$ a set $L_v$ of labels such that each edge $e = (u, w)$ has $a \in L_u$ with $\pi_e(a) \in L_w$, and its size is $\sum_v \lvert L_v \rvert$. In polynomial time one can build an NCP instance with $K = \lvert U \rvert \lvert \Sigma_U \rvert + \lvert W \rvert \lvert \Sigma_W \rvert$ unknowns and $n = K + (K + 1)(\lvert E \rvert \lvert \Sigma_W \rvert + \lvert W \rvert)$ equations such that:

- if $L$ has a labeling that satisfies every edge, then $\mathrm{OPT} \le \lvert U \rvert + \lvert W \rvert$;
- in every case, $\mathrm{OPT}$ is at least the least size of a total cover.

## In plain words

A code is a set of allowed messages. When a message is sent, noise flips some bits, and the receiver wants the allowed message that differs from the received one in the fewest bits. For codes with no special structure, this is hard even if an answer a fixed factor worse than the best is enough.

The reason is that the question is the same as this one: given many equations of the form "these bits add up to 0" or "to 1", set the bits so that as few equations as possible fail. Håstad showed that it is hard to tell systems where almost all equations can hold from systems where almost half must fail. The ratio between almost none and almost half is as large as you want. A second method, built from label cover, gives an even larger ratio, which grows with the length of the code.

## Proof

*Theorem 1.* Fix $\rho$ and choose $\varepsilon > 0$ with $\frac{1/2 - \varepsilon}{\varepsilon} > \rho$. Håstad's theorem, on the [Håstad 3-bit PCP](/hastad-3bit-pcp/) page, says that for a system of $m$ equations mod 2, each with three variables, it is NP-hard to tell whether at least $(1 - \varepsilon) m$ equations can hold at once or at most $(\frac12 + \varepsilon) m$. Make each equation a row of $A$ and its right side an entry of $y$, so $n = m$. In the first case $\mathrm{OPT} \le \varepsilon m$, and in the second $\mathrm{OPT} \ge (\frac12 - \varepsilon) m > 0$. An algorithm with ratio $\rho$ returns at most $\rho \varepsilon m < (\frac12 - \varepsilon) m$ in the first case, and at least $(\frac12 - \varepsilon) m$ in the second, so it decides the NP-hard question. $\blacksquare$

The first case cannot be $\mathrm{OPT} = 0$: whether $y \in C$ is decided by Gaussian elimination. This is why the hard instances need imperfect completeness, and why Håstad's theorem has $1 - \varepsilon$ and not 1.

*Lemma 3.* There is an unknown $x_{v, a}$ for each vertex $v$ and each label $a$ of $v$. The **heavy** equations are

$$\sum_{a : \pi_e(a) = b} x_{u, a} = x_{w, b} \quad \text{for each edge } e = (u, w) \text{ and each } b \in \Sigma_W, \qquad \sum_{b \in \Sigma_W} x_{w, b} = 1 \quad \text{for each } w \in W,$$

and each is written $K + 1$ times. The **light** equations are $x_{v, a} = 0$, once for each unknown. This gives the stated $K$ and $n$.

*Completeness.* Let $\ell$ satisfy every edge, and set $x_{v, a} = 1$ exactly when $a = \ell(v)$. For a right vertex the sum is 1. For an edge $e = (u, w)$ and a label $b$, the left side is 1 exactly when $\pi_e(\ell(u)) = b$, and since $\pi_e(\ell(u)) = \ell(w)$ this is exactly when $x_{w, b} = 1$. So all heavy equations hold, and the false light equations are the $\lvert U \rvert + \lvert W \rvert$ unknowns equal to 1.

*Soundness.* Setting $L_v = \Sigma_v$ for all $v$ is a total cover of size $K$, so the least cover size is at most $K$. Take any $x$. If some heavy equation is false, it is false $K + 1$ times, so the cost is more than $K$ and so more than the least cover size. If every heavy equation holds, let $L_v = \{ a : x_{v, a} = 1 \}$; the cost is $\sum_v \lvert L_v \rvert$. For an edge $e = (u, w)$, the sum over $b$ is odd, so some $b \in L_w$. Then the equation for $e$ and $b$ says that an odd number of $a \in L_u$ have $\pi_e(a) = b$, so at least one. So the sets are a total cover. $\blacksquare$

*Theorem 2, from Lemma 3.* This is an outline of the parameter choice; the counting is complete, but Raz's theorem is cited.

1. *Label cover with a gap.* By the [parallel repetition theorem](/parallel-repetition-theorem/) of Raz, applied $t$ times to the clause and variable game of a satisfiability problem with bounded occurrences, there is a constant $c > 0$ and a reduction from SAT on $s$ variables to label cover with $s^{O(t)}$ vertices and edges, labels of size $2^{O(t)}$, value 1 on satisfiable inputs and value at most $\delta = 2^{-c t}$ on the others. Copies make the two sides equal, of size $N_0$ each, and the graph regular, without a change of value, as in step 1 of [set cover inapproximability](/set-cover-inapproximability/).
2. *Cover size against value.* Let a total cover have size at most $g N_0$. At most $N_0 / 4$ vertices have more than $4 g$ labels, and since all degrees are equal to some $d$ and $\lvert E \rvert = d N_0$, at most a quarter of the edges touch such a vertex. Pick a label of each $L_v$ uniformly at random. Each of the other edges has both sets of size at most $4 g$ and a covering pair, so it is satisfied with probability at least $\frac{1}{16 g^2}$. So the value is at least $\frac{3}{64 g^2}$. If the value is at most $\delta$, then $\frac{3}{64 g^2} \le \delta$, so every total cover has size at least $g N_0$ with $g = \sqrt{3 / (64 \delta)}$.
3. *The gap for NCP.* By Lemma 3, $\mathrm{OPT} \le 2 N_0$ on satisfiable inputs and $\mathrm{OPT} \ge g N_0$ on the others. The ratio is $\frac{g}{2} = \Omega(2^{c t / 2})$.
4. *Sizes.* With $t$ a constant, the instance is polynomial and the ratio is any constant, which is a second proof of Theorem 1. With $t = \log^{r} s$, the instance has $N = 2^{O(\log^{r + 1} s)}$ vertices, and its code length $n$ is polynomial in $N$, so $\log n = \Theta(\log^{r + 1} s)$. The ratio is $2^{\Omega(\log^{r} s)} = 2^{\Omega(\log^{r / (r + 1)} n)}$. For $r$ large enough, this exceeds $2^{\log^{1 - \varepsilon} n}$. The reduction runs in time $2^{\mathrm{polylog}(s)}$, so an algorithm with this ratio decides SAT in that time. $\blacksquare$

### Example

The system $x_0 + x_1 + x_2 = 0$, $x_0 + x_3 + x_4 = 0$, $x_1 + x_3 + x_5 = 0$, $x_2 + x_4 + x_5 = 1$ is an NCP instance with $n = 4$ and $k = 6$. Each variable occurs in two equations, so the left sides add to 0 while the right sides add to 1, and at least one equation is false. Setting all variables to 0 makes only the last equation false, so $\mathrm{OPT} = 1$.

For Lemma 3, a label cover with two left vertices with 3 labels each, two right vertices with 2 labels each, and all four edges gives $K = 10$ unknowns, $4 \cdot 2 + 2 = 10$ heavy equations each written 11 times, and $n = 10 + 110 = 120$. The code for this page checks, on random instances of this size with and without a satisfying labeling, that the least distance is at least the least total cover, and is exactly 4 when a satisfying labeling exists.

## Consequences

- **Decoding needs structure.** Maximum likelihood decoding of a general linear code is hard even within a large factor, so codes used in practice have structure, such as [Reed-Solomon codes](/reed-solomon-code/) or [LDPC codes](/ldpc-code/), that allows fast decoding up to a bound.
- **Lattices.** The same paper proves the same bounds for the closest vector problem in every $\ell_p$ norm, by a reduction of the same shape with integer vectors; see [CVP NP-hardness](/cvp-np-hardness/).
- **Equations mod 2.** The least number of false equations, and the least number of equations to delete to make a system consistent, have the same bounds, since they are the same problem.
- **Minimum distance.** Finding the minimum distance of a code is a different problem. Dumer, Micciancio and Sudan (2003) showed that no constant ratio is possible for it unless RP = NP.

## Tightness

The constant bound of Theorem 1 is not the true threshold: Theorem 2 rules out much larger ratios under a stronger assumption. On the upper side, Gaussian elimination decides whether $\mathrm{OPT} = 0$, and otherwise the codeword 0 is at distance at most $n \le n \cdot \mathrm{OPT}$, so a ratio $n$ is trivial. Known algorithms improve this only to ratios of order $n / \log n$. The gap between $2^{\log^{1 - \varepsilon} n}$ and $n / \log n$ is open. The parameter choice in Theorem 2 loses a square root in step 2, which costs nothing in the exponent $1 - \varepsilon$.

## History

Berlekamp, McEliece and van Tilborg (1978) proved that maximum likelihood decoding of linear codes is NP-hard. Arora, Babai, Stern and Sweedyk proved the approximation bounds at FOCS 1993, with the journal version in 1997, using label cover from the early PCP results, and treated lattices, codes and linear equations together. Raz's parallel repetition theorem (1995) gave the soundness needed for the larger ratio. Håstad's theorem (1997, journal version 2001) gave the direct proof of the constant bound through equations mod 2.

## References
