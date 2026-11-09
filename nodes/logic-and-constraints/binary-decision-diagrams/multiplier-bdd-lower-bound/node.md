---
tag: B71ZEJ
kind: theorem
slug: multiplier-bdd-lower-bound
name: Exponential BDD size for integer multiplication
aliases:
- Bryant multiplier lower bound
area: logic-and-constraints/binary-decision-diagrams
level: advanced
summary: For every variable order, the OBDD of the middle bit of the product of two n-bit numbers has at least 2^(n/8) nodes (Bryant 1991). So no order makes BDDs of multipliers small.
prereqs: [ordered-binary-decision-diagram, variable-ordering, integer-multiplication, carry-propagation]
see_also: [variable-ordering, hidden-weighted-bit-lower-bound, binary-moment-diagram, free-binary-decision-diagram, communication-complexity, integer-multiplication, carry-propagation, ripple-carry-adder]
sources:
  - paper: doi:10.1109/12.73590
    title: Randal E. Bryant, On the complexity of VLSI implementations and graph representations of Boolean functions with application to integer multiplication, IEEE Transactions on Computers 40(2), 1991, pages 205 to 213
    locator: the main theorem on the OBDD size of the middle bit of multiplication, and its proof by crossing pairs of input bits
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 4, The OBDD size of selected functions (multiplication)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (the BDD size of multiplication, and Bryant's theorem)
  - paper: "Philipp Woelfel, New bounds on the OBDD-size of integer multiplication via universal hashing, Journal of Computer and System Sciences 71(4), 2005, pages 520 to 534"
    title: Philipp Woelfel, New bounds on the OBDD-size of integer multiplication via universal hashing
    locator: the improved lower bound for the middle bit and the upper bound
---

Bryant (1991) proved that integer multiplication has no small ordered BDD under any variable order. Let $\mathrm{MUL}_{n-1,n}$ be the middle bit, bit $n - 1$, of the product of two $n$-bit numbers. For every order of its $2n$ input variables, the reduced OBDD of $\mathrm{MUL}_{n-1,n}$ has at least $2^{n/8}$ nodes. This differs from addition, where a good order gives an OBDD of linear size. The theorem is the main reason why BDD-based verification of multiplier circuits fails, and why word-level diagrams such as [binary moment diagrams](/binary-moment-diagram/) were made. The proof counts the subfunctions at a cut of the order, so it is a [communication complexity](/communication-complexity/) argument.

## Statement

Bits are numbered from 0, the least significant bit. The input is $x = (x_0, \ldots, x_{n-1})$ and $y = (y_0, \ldots, y_{n-1})$, with the numbers $X = \sum_p x_p 2^p$ and $Y = \sum_p y_p 2^p$. Let

$$\mathrm{MUL}_{n-1,n}(x, y) = \text{bit } n - 1 \text{ of } X \cdot Y.$$

For an order $\pi$ of the $2n$ variables, $G_\pi$ is the reduced $\pi$-OBDD of $\mathrm{MUL}_{n-1,n}$, and $|G_\pi|$ counts its nodes with the sinks.

**Theorem (Bryant 1991).** For every $n$ and every order $\pi$, $|G_\pi| \ge 2^{n/8}$.

**What is proved in full below.** For every $n \ge 2$ and every order $\pi$,

$$|G_\pi| \ge 2^{k}, \quad k = \left\lceil \frac{r^2}{12(n+1)} \right\rceil, \quad r = \lfloor n/2 \rfloor - 1 .$$

This is $2^{n/48 - O(1)}$: an exponential bound for every order, with a smaller constant than Bryant's. For Bryant's constant $1/8$ we give only the proof idea.

## In plain words

A BDD reads the input bits one at a time in a fixed order and must remember enough about the bits read so far. Split the order into a first part and a second part. If the first part can leave the program in many situations that later reads can all tell apart, the BDD needs one node for each of them at that point. For multiplication, one can always find many pairs of bits of the first number that are split by the cut: one bit of the pair is read before the cut, and the other after it. A clever choice of the second number turns the middle bit of the product into the carry of an addition in which each split pair is added in one column. The carry depends on all the bits before the cut, so the BDD must remember them all.

## Proof

The proof has four lemmas. Lemmas 1 to 3 have full proofs. Lemma 4 has a full proof of a smaller constant; for Bryant's constant we give the proof idea.

**Lemma 1 (restriction does not grow).** If some variables of $f$ are set to constants, the reduced OBDD of the result for the induced order has at most $|G_\pi(f)|$ nodes.

*Proof.* This is Lemma 1 on the page [NP-completeness of OBDD variable ordering](/variable-ordering-np-hardness/): redirect each edge into a node of a fixed variable to the child for its constant, and reduce. Repeat for each fixed variable. $\square$

**Lemma 2 (fooling lemma).** Let $g$ be a function and $\pi$ an order in which every variable of a set $T$ comes before every variable of a set $B$, and $g$ depends only on $T \cup B$. If there are assignments $\alpha_1, \ldots, \alpha_N$ to $T$ such that the subfunctions $g|_{\alpha_i}$ are pairwise different, then $|G_\pi(g)| \ge N$.

*Proof.* For each $\alpha_i$, follow the path from the root that answers each test of a variable of $T$ by $\alpha_i$, and stop at the first node that does not test a variable of $T$. Since the variables of $T$ come first, the node computes $g|_{\alpha_i}$. Different functions are computed by different nodes, so there are at least $N$ nodes. $\square$

**Lemma 3 (split pairs give a large fooling set).** Let $T, B$ be a partition of the $x$-variables such that every variable of $T$ comes before every variable of $B$ in $\pi$. Let $d \ge 1$, and let $q_1 < \cdots < q_k$ be positions with $d \le q_1$, $q_k \le n - 2$ and $q_k - q_1 \le d - 2$, such that for each $j$ one of $x_{q_j - d}$ and $x_{q_j}$ is in $T$ and the other is in $B$. Then $|G_\pi| \ge 2^k$.

*Proof.* Call the $2k$ variables $x_{q_j - d}$ and $x_{q_j}$ the *members*; they are distinct, because the upper positions $q_j$ lie in the window $W = [q_1, q_k]$ and the lower positions $q_j - d$ lie in $[q_1 - d, q_k - d]$, which is below $W$ since $q_k - q_1 < d$. Fix the other variables as follows.

- Put $m = q_k + 1 \le n - 1$ and $a = n - 1 - m \ge 0$. Set $y_a = y_{a+d} = 1$ and all other $y$-bits to 0, so $Y = 2^a + 2^{a+d}$. This is an $n$-bit number, since $a + d = n - 2 - q_k + d \le n - 1$ because $q_k \ge d$.
- Set each $x_p$ that is not a member to 1 if $p \in W$, and to 0 otherwise.

By Lemma 1, the OBDD of the restricted function $g$ for the induced order has at most $|G_\pi|$ nodes. Now $X \cdot Y = 2^a (X + 2^d X)$, so $g$ is bit $m$ of $Z = X + 2^d X$. In the school addition of $X$ and $2^d X$, column $p$ adds $x_p$ and $x_{p-d}$ (with $x_{p-d} = 0$ for $p < d$).

- *Column $m$.* $x_m$ is not a member ($m > q_k$) and $m \notin W$, so $x_m = 0$. Also $m - d = q_k - d + 1 \le q_1 - 1$, so $m - d \notin W$, and it is above all lower members, so $x_{m-d} = 0$. Hence $g$ is the carry into column $m$.
- *Columns $p < q_1$.* $x_{p-d}$ is 0: $p - d < q_1 - d$, so it is not a member, and it is not in $W$. $x_p$ is a member or 0. So the column sum is at most 1, no column below $q_1$ makes a carry, and the carry into column $q_1$ is 0.
- *Columns $p \in W$ with $p \ne q_j$.* $x_p = 1$, and $x_{p-d} = 0$, since $p - d < q_1$ and $p - d$ is a lower member only if $p$ is some $q_j$. The column sum is exactly 1, so the column passes its incoming carry on.
- *Columns $q_j$.* The column adds the two members of pair $j$: one in $T$ with value $\alpha_j$, one in $B$ with value $\beta_j$.

So $g(\alpha, \beta) = 1$ if and only if some pair column has $\alpha_j + \beta_j = 2$, and every pair column above it has $\alpha_i + \beta_i = 1$. Now let $\alpha \ne \alpha'$ be two assignments to the members in $T$, and let $j^*$ be the largest $j$ with $\alpha_j \ne \alpha'_j$. Exchange the names so that $\alpha_{j^*} = 1$ and $\alpha'_{j^*} = 0$, and take $\beta = \neg \alpha'$ (each $\beta_j = 1 - \alpha'_j$). Under $(\alpha', \beta)$ every pair column has sum 1, so $g = 0$. Under $(\alpha, \beta)$ the pair columns above $j^*$ have sum 1, and column $q_{j^*}$ has sum $1 + 1 = 2$, so $g = 1$. So the $2^k$ subfunctions $g|_\alpha$ are pairwise different, and Lemma 2 gives at least $2^k$ nodes. $\square$

**Lemma 4 (many split pairs exist).** For every order $\pi$ and $n \ge 2$, there are a cut $(T, B)$ of the $x$-variables as in Lemma 3 and a distance $d$ with $k \ge r^2 / (12(n+1))$ positions as in Lemma 3, where $r = \lfloor n/2 \rfloor - 1$.

*Proof.* Let $h = \lceil n/2 \rceil$, and let $\tau(p) \in \{0, \ldots, n - 1\}$ be the rank of $x_p$ among the $x$-variables in $\pi$. For $t = 0, \ldots, n$, the cut $T_t$ holds the first $t$ of them. Let $E$ be the set of pairs $(p, q)$ with $0 \le p$, $q \le n - 2$ and $q - p \ge h$. For a distance $d = q - p \ge h$, all pairs of $E$ with this distance have their upper position in $[d, n - 2]$, an interval with $n - 2 - d \le d - 2$, since $d \ge n/2$. So for each $t$ and $d$, the pairs of distance $d$ that $T_t$ splits satisfy the hypotheses of Lemma 3. It remains to find $t$ and $d$ with many split pairs.

A pair $(p, q)$ is split by $T_t$ for exactly $|\tau(p) - \tau(q)|$ values of $t$. So the number of (pair, cut) incidences is $S = \sum_{(p,q) \in E} |\tau(p) - \tau(q)|$. In the graph with edge set $E$, the positions $p = 0, \ldots, r - 1$ have the degrees $r, r - 1, \ldots, 1$, and the positions $q = h, \ldots, n - 2$ have the degrees $1, \ldots, r$; these sets are disjoint, and $r = n - 1 - h$. A vertex $v$ of degree $\delta$ has $\delta$ neighbours with distinct ranks different from $\tau(v)$, so the sum of the rank distances to them is at least $1 + 1 + 2 + 2 + \cdots \ge \delta^2 / 4$. Each edge is counted from both ends, so

$$S \ge \frac{1}{2} \cdot 2 \sum_{\delta = 1}^{r} \frac{\delta^2}{4} = \frac{r(r+1)(2r+1)}{24} \ge \frac{r^3}{12}.$$

If $r = 0$ the claimed bound is $2^0 = 1$, which is trivial, so let $r \ge 1$. There are $n + 1$ cuts, so some $t$ splits at least $S / (n + 1)$ pairs of $E$. These pairs have at most $r$ different distances ($h \le d \le n - 2$), so some distance has at least $S / (r(n+1)) \ge r^2 / (12 (n+1))$ split pairs. $\square$

*Proof of the bound $2^{\lceil r^2 / (12(n+1)) \rceil}$.* Take $t$ and $d$ from Lemma 4. Every $x$-variable of $T_t$ comes before every $x$-variable of the rest in $\pi$. Lemma 3 gives $|G_\pi| \ge 2^k$. $\blacksquare$

**Proof idea for Bryant's constant $1/8$.** Take the cut after the first $n/2$ variables of $x$. There are $(n/2)^2 = n^2/4$ split pairs in all, and at most $2n - 1$ signed distances $q - p$, so some signed distance has at least $n^2 / (4(2n-1)) \ge n/8$ split pairs. Pairs with the same signed distance never share a variable: if $(p, p + d)$ has its lower end in $T$ and $(p + d, p + 2d)$ also had its lower end in $T$, then $x_{p+d}$ would be in both $T$ and $B$. Bryant then chooses $Y$ with two 1-bits and fixes the other bits of $X$ so that these pairs feed one carry chain, as in Lemma 3. The difficult step is to keep the chain intact when the pairs are spread over the whole word; our Lemma 3 avoids it with the window condition, and pays for it with the smaller constant. We do not reproduce Bryant's handling of this step here. See Bryant (1991) and Wegener (2000, Chapter 4) for the details.

## Consequences

- **No good order for multipliers.** BDD packages cannot verify large multiplier circuits by building the OBDDs of the outputs, whatever reordering they use, including [sifting](/bdd-sifting/).
- **Reordering has limits.** For many functions a good [variable order](/variable-ordering/) makes the OBDD small. Multiplication shows that some simple functions are hard for every order.
- **Other diagrams.** [Binary moment diagrams](/binary-moment-diagram/) represent the word-level product $X \cdot Y$ with polynomial size, because they decompose by moments instead of cofactors.
- **Composition.** Any method that builds the OBDD of the middle bit, for example by [composition](/boolean-function-composition/) of the gates of a circuit, takes exponential time.

The table shows measured sizes for small $n$ (the smallest and the largest over all orders, and two natural orders), computed by dynamic programming over sets of variables, as in the [Friedman-Supowit](/friedman-supowit-ordering/) algorithm. The natural order is $x_0, \ldots, x_{n-1}, y_0, \ldots, y_{n-1}$, and the interleaved order is $x_0, y_0, x_1, y_1, \ldots$.

| $n$ | smallest | largest | natural | interleaved |
|---|---|---|---|---|
| 1 | 4 | 4 | 4 | 4 |
| 2 | 8 | 9 | 9 | 9 |
| 3 | 14 | 24 | 19 | 16 |
| 4 | 31 | 71 | 43 | 36 |
| 5 | 63 | 207 | 99 | 73 |
| 6 | 136 | 649 | 238 | 169 |
| 7 | 315 | 2019 | 569 | 381 |

The smallest size grows by a factor of about 2 to 2.3 per added bit in this range, faster than the proved $2^{1/8} \approx 1.09$. The bound $2^{n/8}$ is weak for small $n$, but it holds for all $n$.

## Tightness

- **The exponent is linear, and the constant is not $1/8$.** Woelfel (2005) improved the lower bound to $2^{\lfloor n/2 \rfloor} / 61$ and proved an upper bound of the form $2^{O(n)}$ with a small constant in the exponent, so the true growth is $2^{\Theta(n)}$.
- **The order still matters.** Some orders are much worse than others (the largest sizes in the table are up to 6 times the smallest), but no order gives polynomial size.
- **Only the middle bits are hard.** The lowest output bits depend on few inputs: bit 0 is $x_0 \wedge y_0$. So the theorem is about the bits in the middle of the product. Bryant's result covers bit $n - 1$, and similar arguments apply to the bits near it.
- **Other models.** The bound is for OBDDs. For [free BDDs](/free-binary-decision-diagram/), where each path may use its own order, the middle bit is also exponential, but the proofs are harder (Ponzio 1995, Bollig and Woelfel 2001).

## History

Bryant (1986) introduced OBDDs and showed that the order can change the size by an exponential factor. In 1991 he proved that the middle bit of multiplication needs exponential size for every order, with the bound $2^{n/8}$, in a paper that also gave lower bounds on the area and time of VLSI circuits for the same function. This explained why BDD-based verification of multipliers failed in practice. Bryant and Chen (1995) answered with binary moment diagrams. Woelfel (2005) gave the bound $2^{\lfloor n/2 \rfloor}/61$ with universal hashing. Ponzio (1995) and Bollig and Woelfel (2001) proved exponential lower bounds for read-once branching programs.

## References
