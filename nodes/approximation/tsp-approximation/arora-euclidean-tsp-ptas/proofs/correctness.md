---
title: The grid step and the portal lemma in full, and the structure theorem and dynamic program as a sketch
proves: [correctness]
status: sketch
---

The input is a set $P$ of $n \ge 2$ points in the plane and a number $c \ge 1$. The aim is a tour of expected length at most $(1 + 1/c) \cdot \text{OPT}$. Parts 1 and 2 below are full proofs, and they prove the guarantee of the code. Part 3 is a sketch of the rest of Arora's argument, which gives the running time $n (\log n)^{O(c)}$; it follows Arora (1998), and its constants are not checked here.

## Part 1. The grid step

Let $L_0$ be the larger side of the bounding box of $P$, and $\delta = L_0 / (8cn)$. Round each point to the nearest point of the grid $\delta \mathbb{Z}^2$ from the low corner of the box, and divide by $\delta$. The new points have integer coordinates in $\{0, \ldots, L - 1\}$, where $L$ is the least power of 2 above every coordinate, so $L = O(cn)$.

**Lemma 1 (the grid step costs little).** For each order of the points, the tour length changes by at most $\sqrt{2}\, n \delta \le \frac{\sqrt{2}}{16 c} \text{OPT}$ when the points move to the grid.

*Proof.* Rounding each coordinate moves it by at most $\delta / 2$, so each point moves by at most $\delta / \sqrt{2}$. Each of the $n$ edges has two ends, so it changes by at most $\sqrt{2}\,\delta$. A tour visits a point of least $x$ and a point of largest $x$, and must come back, so $\text{OPT} \ge 2 L_0$. Then $\sqrt{2}\, n \delta = \sqrt{2} L_0 / (8c) \le \sqrt{2}\, \text{OPT} / (16 c)$. $\square$

## Part 2. The shifted dissection and the portals

**The dissection.** Pick $a, b$ uniformly and independently from $\{0, \ldots, L - 1\}$. The dissection square has side $2L$ and its low corner at $(-a - \frac{1}{2}, -b - \frac{1}{2})$, so it holds all the points. Cut it into four equal squares, and those again, down to side 1. A square of depth $i$ has side $2L / 2^i$. The *grid lines* are the lines $x = k + \frac{1}{2}$ and $y = k + \frac{1}{2}$ for integers $k$ with $0 \le k \le L - 2$; they lie between the points, and every cut of the dissection inside the hull of the points is on a grid line. The *level* of a grid line is the least $i$ such that the line holds a side of a square of depth $i$. The line $x = k + \frac{1}{2}$ is at distance $k + a + 1$ from the left side of the dissection square, so its level is the least $i \ge 1$ such that $2L / 2^i$ divides $k + a + 1$.

**Lemma 2 (the chance of a low level).** For each grid line and each $i \ge 1$, the probability that its level is at most $i$ is $\min(1, 2^{i - 1} / L)$.

*Proof.* Let $1 \le i \le \log_2(2L)$ and $q = 2L / 2^i$, a power of 2 with $q \le L$. The level is at most $i$ exactly when $q$ divides $k + a + 1$. As $a$ runs over $\{0, \ldots, L - 1\}$, the number $k + a + 1$ runs over $L$ consecutive integers, which are $L / q$ full blocks of $q$ consecutive integers. Each block has one multiple of $q$. So the probability is $(L / q) / L = 2^{i-1} / L$, which is 1 for $i = \log_2(2L)$. Every line has a level of at least 1, since $k + a + 1 \in \{1, \ldots, 2L - 2\}$ is never a multiple of $2L$. $\square$

**Lemma 3 (crossings).** A tour on the grid points crosses grid lines at most $\sqrt{2}$ times its length in total.

*Proof.* An edge from $(x_1, y_1)$ to $(x_2, y_2)$ crosses the $|x_1 - x_2|$ vertical grid lines between $x_1$ and $x_2$ and the $|y_1 - y_2|$ horizontal ones, each once. And $|x_1 - x_2| + |y_1 - y_2| \le \sqrt{2} \cdot$ its length. $\square$

**Portals.** Let $m$ be a power of 2 with $m \ge 2\sqrt{2}\, c \log_2(2L)$. Each side of a square of depth $i$ gets $m + 1$ portals, spaced $2L / (2^i m)$, with portals at both corners. Since $m$ and all sides are powers of 2, the portals of a square are also portals of its smaller squares on the same line. Moving a crossing at point $X$ of a line of level $i$ to the nearest portal $Y$ of that level costs at most $2|XY| \le 2L / (2^i m)$: the tour runs along the line to $Y$, crosses there, and runs back.

**Lemma 4 (the portal lemma).** For a fixed tour $H$ on the grid points, the expected total cost of moving every crossing to its nearest portal is at most $\frac{\sqrt{2} \log_2(2L)}{m} |H| \le \frac{|H|}{2c}$.

*Proof.* Fix one crossing of $H$ with a grid line $\ell$. Its cost is at most $2L / (2^i m)$ when $\ell$ has level $i$. By Lemma 2, the probability of level $i$ is at most $2^{i-1} / L$. Over the levels $i = 1, \ldots, \log_2(2L)$, the expected cost is at most

$$\sum_{i=1}^{\log_2(2L)} \frac{2^{i-1}}{L} \cdot \frac{2L}{2^i m} = \frac{\log_2(2L)}{m}.$$

By Lemma 3 and the linearity of expectation, the total is at most $\frac{\log_2(2L)}{m} \cdot \sqrt{2}\,|H|$. The choice of $m$ gives the second bound. $\square$

**Theorem 1 (the guarantee of the code).** Let the algorithm return the order that minimizes the grid length plus the portal cost of Lemma 4 for the chosen shift. Then the expected length of its tour on the original points is at most $(1 + 0.73/c) \cdot \text{OPT} \le (1 + 1/c) \cdot \text{OPT}$.

*Proof.* Let $H$ be an optimal order for $P$, and let a prime mark lengths on the grid, in units of $\delta$. The returned order $A$ satisfies $|A'| \le |A'| + \text{cost}(A) \le |H'| + \text{cost}(H)$ for each shift. By Lemma 4, $\mathbb{E}[|A'|] \le (1 + \frac{1}{2c}) |H'|$. By Lemma 1, $\delta |H'| \le \text{OPT} + u\,\text{OPT}/c$ and $|A| \le \delta |A'| + u\,\text{OPT}/c$, with $u = \sqrt{2}/16 < 0.0884$. So

$$\mathbb{E}|A| \le \text{OPT} \left( (1 + \tfrac{u}{c})(1 + \tfrac{1}{2c}) + \tfrac{u}{c} \right) \le \text{OPT} \left( 1 + \tfrac{0.5 + 2u + u/2}{c} \right) \le \left( 1 + \tfrac{0.73}{c} \right) \text{OPT},$$

using $1/c^2 \le 1/c$. $\square$

The test file checks Lemmas 1 to 4 exactly, over all $L^2$ shifts, on small instances, and checks the per-shift inequality $|A'| + \text{cost}(A) \le |H'| + \text{cost}(H)$ against brute force.

## Part 3. The structure theorem and the dynamic program (sketch)

The minimum in Theorem 1 is over all $(n-1)!$ orders. Arora's scheme finds a tour at least as good in polynomial time. The route moved to portals, as in Lemma 4, crosses each side of each square only at portals: the runs along a line cross other lines only at corners, which are portals. Call such a tour *portal-respecting*. So the best portal-respecting tour has expected cost at most $(1 + \frac{1}{2c}) |H'|$.

**Patching lemma (Arora 1998).** If a closed path crosses a line segment $S$ of length $s$ at $t \ge 3$ points, then segments along $S$ of total length at most $3s$ can be added so that the result contains a closed walk through the same points that crosses $S$ at most twice. This lemma has a full proof.

*Proof.* Let the crossings be $x_1, \ldots, x_t$ in order along $S$. Cut the path at each $x_j$, which leaves copies $a_j$ and $b_j$ of $x_j$ just on the two sides of $S$, each of degree 1. A piece of the cut path runs between two copies on the same side, because the path changes sides only at crossings. Let $e_j$ be the part of $S$ from $x_j$ to $x_{j+1}$, for $j < t$. On each side, add a path through all copies along $S$, which costs at most $s$. Then add a second copy of each $e_j$ with $j$ odd, or of each $e_j$ with $j$ even, whichever costs less. The two sets together cost at most $s$, so the cheaper one costs at most $s/2$. Use the same choice on both sides. Now every inner copy has even degree, because exactly one of its two parts $e_{j-1}$ and $e_j$ was doubled. The end copies $a_1$, $a_t$ and $b_1$, $b_t$ have odd degree exactly when their part was doubled, in the same way on both sides. Add an edge of length 0 across $S$ from $a_j$ to $b_j$ for each end $j$ that has odd degree. If no end has odd degree, add two copies of the edge from $a_1$ to $b_1$. This uses at most two edges across $S$. Each side is connected by its path, and the edges across $S$ join the two sides, so the graph is connected and all degrees are even. Its Euler circuit is a closed walk through all the points, it crosses $S$ at most twice, and the added length is at most $2(s + s/2) = 3s$. $\square$

**Structure theorem (Arora 1998).** With $m = O(c \log L)$ portals per side and $r = O(c)$, the expected cost of the best portal-respecting tour that crosses each side of each square at most $r$ times is at most $(1 + 1/c) \cdot \text{OPT}$; by [Markov's inequality](/markov-inequality/) this holds within a factor $1 + 2/c$ with probability at least $1/2$. *Idea.* Apply the patching lemma on each side that has more than $r$ crossings, from the smallest squares up. A line of level $i$ is patched at the scale $2L / 2^i$ with probability at most $2^{i-1}/L$, as in Lemma 2. Each patching removes at least $r - 3$ crossings at a cost of 3 times the side, so the expected cost per line is $O(t(\ell) / r)$, where $t(\ell)$ is the number of crossings of the line. Summing with Lemma 3 gives $O(\text{OPT}/r)$. Patching can add crossings of the perpendicular lines only near corners, and the full proof bounds these.

**The dynamic program.** For a square and an *interface*, that is, at most $r$ portals on each side and a pairing of the chosen portals, compute the least cost of a set of paths inside the square that visits all its points and connects the portals as the pairing says. A tour that does not cross itself gives non-crossing pairings, and there are $2^{O(r)}$ of those. So a square has $(m + 4)^{4r} \cdot 2^{O(r)} = (\log n)^{O(c)}$ interfaces. A square is solved from the interfaces of its four children that agree on the shared sides, in $(\log n)^{O(c)}$ time. The quadtree has $O(n \log n)$ non-empty squares, so the total time is $n (\log n)^{O(c)}$. A leaf with one point, or none, is solved directly. The root, with no portals on its outer sides, gives the tour.

**Derandomization.** Trying all $L^2 = O(c^2 n^2)$ shifts and keeping the best tour gives a deterministic algorithm with the same ratio, at $O(n^2)$ times the cost.
