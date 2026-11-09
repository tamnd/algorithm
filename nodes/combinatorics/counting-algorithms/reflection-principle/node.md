---
tag: J3TJHA
kind: technique
slug: reflection-principle
name: Reflection principle
aliases:
- method of images
- André's reflection
- reflection method
area: combinatorics/counting-algorithms
level: core
summary: Counts constrained paths by reflecting them to unconstrained ones.
prereqs: [counting-lattice-paths]
see_also: [counting-lattice-paths, ballot-theorem, catalan-numbers, cycle-lemma, counting-balanced-bracket-sequences, bijective-proof, inclusion-exclusion-principle, counting-standard-young-tableaux]
sources:
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume 1, third edition, Wiley, 1968
    locator: Chapter III, Fluctuations in Coin Tossing and Random Walks (Section 1, the reflection principle, and Section 7, maxima)
  - book: isbn:9781107427747
    title: Richard P. Stanley, Catalan Numbers, Cambridge University Press, 2015
    locator: Chapter 1, Basic properties (the reflection proof of the formula for Catalan numbers)
  - paper: doi:10.1080/00029890.2008.11920537
    title: Marc Renault, Lost (and found) in translation, André's actual method and its application to the generalized ballot problem, American Mathematical Monthly 115 (2008), 358-363
    locator: the whole paper (what André did in 1887, and the swap of steps that is often called reflection)
  - paper: doi:10.1090/S0002-9939-1992-1092920-8
    title: Ira M. Gessel and Doron Zeilberger, Random walk in a Weyl chamber, Proceedings of the American Mathematical Society 115 (1992), 27-31
    locator: the whole paper (reflection in several hyperplanes and the signed sum over a reflection group)
---

The reflection principle counts the walks that touch a forbidden level by mapping them, one to one, to all walks that end at a mirror image of the target. The good walks are then the difference of two free counts, each a [binomial coefficient](/binomial-coefficient/). It gives one-line proofs of the formula for the [Catalan numbers](/catalan-numbers/), of the [ballot theorem](/ballot-theorem/) and of the law of the maximum of a random walk. Repeated reflection handles walks between two barriers, and reflection groups handle walks in several dimensions.

## In plain words

Draw a walk that goes up or down one unit at each step, and a horizontal line it is not allowed to touch. Take a bad walk and find the first moment it touches the line. Flip the rest of the walk over the line, like a mirror image. The flipped walk ends at the mirror image of the old end point, and every walk to that mirror point arises this way exactly once. So the bad walks are as many as all walks to the mirror point, which are easy to count. Subtract them from all walks to the real end point, and what is left are the good walks.

## When it applies

- The objects are walks, or lattice paths, with steps that the reflection maps to allowed steps. Steps $+1$ and $-1$ on a line, and steps $E$ and $N$ in the plane with a line of slope 1, are the main cases.
- The constraint is "never touch a given level", or "stay between two levels".
- The walk cannot jump over the forbidden level without touching it. With unit steps this holds automatically.
- Free walks between two points are easy to count, usually by one binomial coefficient.

## The template

**Notation.** A *walk* of length $n$ is a sequence of $n$ steps, each $+1$ or $-1$, and its positions are the partial sums added to a start $x$. $W_n(x \to y)$ is the number of walks of length $n$ from $x$ to $y$. $C(n, k)$ is the binomial coefficient, with $C(n, k) = 0$ outside $0 \le k \le n$, and $[n] = \{1, \ldots, n\}$.

**Free count.** A walk from $x$ to $y$ with $u$ steps up and $d$ steps down has $u + d = n$ and $u - d = y - x$, so

$$W_n(x \to y) = C\Big(n, \frac{n + y - x}{2}\Big),$$

which is $0$ when $n + y - x$ is odd or $|y - x| > n$.

**Lemma (reflection).** Let $m$ be an integer, and let $x$ and $y$ both differ from $m$ and lie on the same side of it. The number of walks of length $n$ from $x$ to $y$ that touch level $m$ equals $W_n(x \to 2m - y)$.

*Proof.* Let a walk from $x$ to $y$ touch $m$, and let $t$ be its first time at $m$. Reflect the part after $t$ in level $m$: replace each later position $s$ by $2m - s$. The new walk is a walk, since the steps after $t$ only change sign, and it ends at $2m - y$. Conversely, $2m - y$ lies on the other side of $m$ from $x$, so every walk from $x$ to $2m - y$ touches $m$, and reflecting it after its first time $t$ at $m$ gives back a walk to $y$. The first time at $m$ is the same before and after the reflection, because the part before $t$ does not change. So the two maps are inverse to each other. $\square$

**Recipe.**

1. Write the objects as walks and the constraint as "never touch level $m$". For "never go below $0$", the forbidden level is $m = -1$. For "stay strictly above $0$", it is $m = 0$.
2. Count all free walks: $W_n(x \to y)$.
3. Subtract the bad walks: $W_n(x \to 2m - y)$.

The answer $W_n(x \to y) - W_n(x \to 2m - y)$ is exact, has $O(n)$ bits, and costs two binomial coefficients, that is $O(n)$ multiplications of $O(n)$-bit numbers, or $O(1)$ operations modulo a prime $p > n$ after a factorial table.

## Classic examples

**Catalan numbers.** Dyck paths of semilength $n$ are walks of length $2n$ from $0$ to $0$ that never touch $-1$. The count is

$$W_{2n}(0 \to 0) - W_{2n}(0 \to -2) = C(2n, n) - C(2n, n + 1) = \frac{1}{n + 1} C(2n, n).$$

For $n = 3$: $20 - 15 = 5$. See [Catalan numbers](/catalan-numbers/) and [counting balanced bracket sequences](/counting-balanced-bracket-sequences/).

**Ballot theorem.** In an election, $A$ gets $a$ votes and $B$ gets $b < a$ votes, counted one by one in random order. The counts in which $A$ is strictly ahead throughout are walks from $0$ to $a - b$ with positions $\ge 1$ after the first step. The first step must be $+1$, and the rest is a walk of length $a + b - 1$ from $1$ to $a - b$ that never touches $0$:

$$C(a + b - 1, a - 1) - C(a + b - 1, a) = \frac{a - b}{a + b}\, C(a + b, a).$$

The last form uses $C(a + b - 1, a - 1) = \frac{a}{a + b} C(a + b, a)$ and $C(a + b - 1, a) = \frac{b}{a + b} C(a + b, a)$. So the probability that $A$ leads throughout is $\frac{a - b}{a + b}$. See [ballot theorem](/ballot-theorem/).

**Maximum of a walk.** Let $S_n$ be the end of a walk of length $n$ from $0$, and $M_n$ its maximum position. For $r \ge 1$, the number of walks with $M_n \ge r$ is

$$\#\{S_n = r\} + 2\,\#\{S_n > r\}.$$

*Proof.* Walks with $S_n \ge r$ all have $M_n \ge r$. Walks with $M_n \ge r$ and $S_n < r$ touch $r$, and reflection after the first time at $r$ maps them one to one onto the walks with $S_n > r$. $\square$ Dividing by $2^n$ gives Feller's law of the maximum of a fair coin-tossing game.

**Walks that never go below 0.** The walks of length $n$ from $0$ that never touch $-1$, with any end, number $C(n, \lfloor n/2 \rfloor)$: $1, 1, 2, 3, 6, 10, 20, 35, 70, 126, 252, 462$ for $n = 0, \ldots, 11$ (OEIS A001405).

*Proof.* Those that end at $y \ge 0$ number $W_n(0 \to y) - W_n(0 \to -2 - y) = C(n, \frac{n + y}{2}) - C(n, \frac{n + y}{2} + 1)$, using $C(n, k) = C(n, n - k)$ for the second term. Summing over the $y \ge 0$ of the right parity, the terms telescope to $C(n, \lceil n/2 \rceil) = C(n, \lfloor n/2 \rfloor)$. $\square$

## Variations

- **Two barriers.** Walks from $0$ to $0$ of length $2n$ that stay in $[0, h]$ avoid the levels $-1$ and $h + 1$. Reflecting in both lines again and again generates the images of the target, which repeat with period $2(h + 2)$, and [inclusion-exclusion](/inclusion-exclusion-principle/) over the alternating sequences of touches gives

$$\sum_{k \in \mathbb{Z}} \Big[ C(2n, n + k(h + 2)) - C(2n, n + 1 + k(h + 2)) \Big].$$

Only $O(n/h)$ terms are nonzero. For $h = 2$ the count is $2^{n-1}$ for $n \ge 1$. For $h = 3$ it is $1, 1, 2, 5, 13, 34, 89, 233, 610, 1597$ for $n = 0, \ldots, 9$, the Fibonacci numbers of odd index (OEIS A001519). This is the classical gambler's ruin count. The name "method of images" comes from the method of the same name in electrostatics.

*Proof sketch.* For a walk, write the sequence of barriers it touches, with repeated letters merged, as an alternating word in $L$ (level $-1$) and $U$ (level $h + 1$). Let $A_j$ be the walks whose word contains $L U L \cdots$ of length $j$ as a subsequence, and $B_j$ the same with $U L U \cdots$. Reflecting after each of the $j$ greedy first touches maps $A_j$ and $B_j$ one to one onto the free walks to a $j$-fold image of the target. A walk whose word has length $\ell \ge 1$ lies in $A_j$ for $j \le \ell$ or $j \le \ell - 1$, depending on its first letter, and in $B_j$ for the other range, so its total weight in $\sum_{j \ge 1} (-1)^{j-1} (|A_j| + |B_j|)$ is $1$. So this sum counts the bad walks, and its terms are the shifted binomials above. $\square$

- **Shifted lines in the plane.** For paths with steps $E$ and $N$, reflection in the line $y = x + t + 1$ swaps $E$ and $N$. The paths from $(0, 0)$ to $(a, b)$ that stay weakly below $y = x + t$ number $C(a + b, b) - C(a + b, b - t - 1)$, see [counting lattice paths](/counting-lattice-paths/).
- **Several dimensions.** For walks in $\mathbb{Z}^k$ that must keep $x_1 > x_2 > \cdots > x_k$, the forbidden set is the union of the hyperplanes $x_i = x_j$, and the reflections in them generate the symmetric group. Gessel and Zeilberger showed that the good walks are a signed sum over the group of free counts to the images of the target. With unit steps $e_i$, this counts the ballot sequences with $k$ candidates, which are the [standard Young tableaux](/counting-standard-young-tableaux/) of a shape with $k$ rows, and the signed sum becomes the determinant $n! \det[1/(\lambda_i - i + j)!]$.
- **André's own bijection.** The principle is usually credited to Désiré André, who proved the ballot theorem in 1887. His proof used a different bijection on the vote sequences, not a reflection of the path; Renault describes it and shows how it extends to the generalized ballot problem.
- **Continuous time.** For Brownian motion, reflection after the first hitting time of a level gives $P(\max_{s \le t} B_s \ge r) = 2 P(B_t \ge r)$, the limit of the formula for the maximum above.

## Pitfalls

- **Wrong level.** "Never below $0$" forbids the level $-1$, and "strictly positive" forbids the level $0$. Reflecting in the wrong one gives an off-by-one error in the result, such as $C(2n, n) - C(2n, n + 2)$ in place of $C(2n, n) - C(2n, n + 1)$.
- **Reflecting after a later touch.** Only the first touch gives a map that can be inverted. After a later touch, two different walks can have the same image.
- **Steps that jump.** With steps $+2$ and $-1$, a walk can cross a level without touching it, and the reflected walk uses steps $-2$ and $+1$, which are not allowed. Use the [cycle lemma](/cycle-lemma/) for such step sets.
- **Lines of other slopes.** In the plane with steps $E$ and $N$, reflection in a line of slope other than 1 does not map lattice paths to lattice paths. For the line through $(0, 0)$ and $(a, b)$ with $\gcd(a, b) = 1$, use the cycle lemma, which gives $C(a + b, a)/(a + b)$.
- **Parity.** $W_n(x \to y) = 0$ when $n + y - x$ is odd, and code that computes $\frac{n + y - x}{2}$ with integer division gives a wrong nonzero term.

## Exercises

1. Show that the walks of length $2n$ from $0$ that never return to $0$ number $C(2n, n)$.
2. Count the paths with steps $E$ and $N$ from $(0, 0)$ to $(n, n)$ that stay weakly below $y = x + 1$, and check your answer for $n = 3$ by listing.
3. A walk of length $n$ starts at $0$. Count the walks with maximum at least $r$ that end at $y \le r$, and derive the formula for the maximum above from your answer.
4. Use the two-barrier formula with $h = 2$ to prove that the count is $2^{n-1}$, and give a direct bijection.
5. Use reflection to show that the number of paths with steps $(1, 1)$, $(1, 0)$ and $(1, -1)$ of length $n$ from height $0$ to height $0$ that never go below $0$ is $\sum_{k} C(n, 2k)\, C_k$, where $C_k$ is the $k$-th Catalan number.

## References
