---
title: The greedy PLA is optimal, each level shrinks by a factor of 2 epsilon + 1, and the windowed search finds the rank
proves: [correctness]
status: full
---

We use the notation of the page. A level array $A[0..N-1]$ is strictly increasing. A segment $s$ covers the positions $a..b$ of $A$ and predicts $f_s(x) = s.intercept + s.slope \cdot (x - s.key)$, with $s.key = A[a]$. A segment is *valid* for the error $e$ if $|f_s(A[i]) - i| \le e$ for $a \le i \le b$. The rank of $x$ is $r(x) = |\{i : A[i] \le x\}|$. The errors $e$ are integers at least 1.

**Lemma 1 (the feasible region).** For a fixed $x_0$, the set of pairs $(s, c)$ such that the line $c + s (x - x_0)$ is within $e$ of all of the points $(A[i], i)$, $a \le i \le j$, is the intersection of the strips $i - e \le c + s (A[i] - x_0) \le i + e$. It is convex. For $j = a + 1$ it is the parallelogram with the four vertices that BUILD-PLA makes at L3.

*Proof.* Each strip is the closed set between two parallel lines in the $(s, c)$ plane, so it is convex, and an intersection of convex sets is convex. For two points, the line takes the values $c$ at $A[a] = x_0$ and $c + s d$ at $A[a+1]$, with $d = A[a+1] - x_0 > 0$. The map $(s, c) \mapsto (c, c + s d)$ is a linear bijection, and the two conditions say that the image lies in the square $[a - e, a + e] \times [a + 1 - e, a + 1 + e]$. The four vertices at L3 are the preimages of the corners of the square, in order around it. $\square$

`_clip` cuts a convex polygon with a half-plane by the Sutherland and Hodgman rule: it keeps the vertices inside and adds the point where an edge crosses the boundary. For a convex polygon this gives the exact intersection, and the arithmetic uses exact fractions. So at every step the polygon is exactly the feasible region of Lemma 1, and the loop at L5 stops at the first $j$ for which no valid line exists. The mean of the vertices is a convex combination of points of the region, so it is in the region.

**Lemma 2 (a flat line).** If some valid line over $a..b$ has a negative slope, then $b - a < 2e$, and the flat line at height $(a + b) / 2$ is valid over $a..b$.

*Proof.* Let $u = f(A[a])$ and $w = f(A[b])$. A negative slope gives $w < u$, and validity gives $u \le a + e$ and $w \ge b - e$. So $b - e < a + e$, which is $b - a < 2e$. For $a \le i \le b$, $|(a + b)/2 - i| \le (b - a)/2 < e$. $\square$

So the code replaces a mean with a negative slope by the flat line of Lemma 2, and every segment it outputs is valid and has a slope of at least 0.

**Lemma 3 (prefix closure).** If a valid segment over $a..b$ exists, then a valid segment over $a'..b'$ with $a \le a' \le b' \le b$ exists.

*Proof.* Removing points removes constraints. $\square$

**Theorem 1 (the greedy PLA is optimal).** Let $g$ be the number of segments of BUILD-PLA with the error $e$, and let $h$ be the fewest segments of any PLA of $A$ with the error $e$ in which each segment covers a run of consecutive positions. Then $g = h$.

*Proof.* Let the greedy segments end at $b_1 < b_2 < \cdots < b_g = N - 1$, and let an optimal PLA have segments that end at $c_1 < \cdots < c_h = N - 1$. We show $b_t \ge c_t$ for each $t \le \min(g, h)$ by induction. For $t = 1$: the optimal first segment covers $0..c_1$ and is valid, and the greedy segment from 0 grows as long as a valid line exists, so $b_1 \ge c_1$. For the step, suppose $b_t \ge c_t$ and $t < g$. If $b_t \ge c_{t+1}$, then $b_{t+1} > b_t \ge c_{t+1}$. Otherwise the optimal segment $t + 1$ covers $c_t + 1..c_{t+1}$, which contains $b_t + 1..c_{t+1}$. By Lemma 3 a valid segment over $b_t + 1..c_{t+1}$ exists, and the greedy segment $t + 1$ starts at $b_t + 1$, so it ends at $b_{t+1} \ge c_{t+1}$. If $g > h$, this gives $b_h \ge c_h = N - 1$, so the greedy method would have stopped after $h$ segments, which is false. So $g \le h$, and $g \ge h$ because the greedy PLA is a PLA of this kind. $\square$

**Lemma 4 (segment length).** Every segment of BUILD-PLA other than the last covers at least $2e + 1$ positions. So a level with $N$ entries has at most $\lceil N / (2e + 1) \rceil$ segments.

*Proof.* For any $a$, the flat line at height $a + e$ is within $e$ of the points $(A[i], i)$ for $a \le i \le a + 2e$, because $|i - (a + e)| \le e$. So a valid segment over $a..\min(a + 2e, N - 1)$ exists, and the greedy segment from $a$ is at least that long. A segment that is not the last ends before $N - 1$, so it covers at least $2e + 1$ positions. $\square$

The paper (Lemma 2) states the bound with $2e$ keys per segment; Lemma 4 gives the slightly better $2e + 1$ for an integer $e$. With the inner error $e' \ge 1$, each level above the bottom has at most a third of the entries of the level below, so the number of levels is at most $1 + \lceil \log_{2e'+1} m \rceil$ for $m$ bottom segments, and the construction stops with one segment.

**Lemma 5 (the window).** Let $s$ be a segment over $a..b$ of $A$ with the error $e$ and a slope of at least 0. Let $x$ satisfy $A[a] \le x$, and $x < A[b + 1]$ if $b + 1 < N$. Let $q$ be $f_s(x)$ clamped to $[a, b]$, and $p = \lfloor q \rfloor$. Then $r(x)$ lies in $[\max(a, p - e), \min(b + 1, p + e + 1)]$.

*Proof.* From the conditions on $x$, $a + 1 \le r(x) \le b + 1$. Let $i = r(x) - 1$. Then $a \le i \le b$, $A[i] \le x$, and $x < A[i + 1]$ if $i < b$. Let $\hat f$ be $f_s$ clamped to $[a, b]$. It is nondecreasing, because $f_s$ and the clamp are. Clamping a value $y$ to $[a, b]$ gives a value between $y$ and any point of $[a, b]$, so for $y$ within $e$ of a point of $[a, b]$, the clamped value is also within $e$ of that point.

So $q = \hat f(x) \ge \hat f(A[i]) \ge i - e$. If $i < b$, then $q \le \hat f(A[i + 1]) \le i + 1 + e$. If $i = b$, then $q \le b = i$. In both cases $i - e \le q \le i + 1 + e$, so $q - e \le r(x) \le q + e + 1$. Since $r(x)$ is an integer, $r(x) \ge \lceil q \rceil - e \ge p - e$ and $r(x) \le \lfloor q + e + 1 \rfloor = p + e + 1$. With $a + 1 \le r(x) \le b + 1$, the claim follows. $\square$

**Theorem 2 (search).** QUERY$(x)$ returns $r(x)$ for the key array $K$, and the window of each level has at most $2e + 2$ positions, where $e$ is the error of that level.

*Proof.* If $x < K[0]$, L13 returns $0 = r(x)$. Otherwise every level array starts with $K[0] \le x$, because the first key of the first segment of each level is $K[0]$. The root segment covers its whole array, so it satisfies the conditions of Lemma 5. Suppose a segment $s$ of some level satisfies them. By Lemma 5 the window at L17 contains $r(x)$, and the entries of the array before the window are $\le x$ and the entries after it are $> x$. So the binary search, which counts the entries $\le x$ inside the window and adds the start of the window, returns $r(x)$. If this is the bottom level, L18 returns it. Otherwise $r(x) \ge 1$, and the entry $r(x) - 1$ of the array is the first key of a segment $t$ of the level below, with $t.key \le x$, and with the first key of the next segment $> x$ if there is one. That is, $t$ satisfies the conditions of Lemma 5 for its own array, and L19 continues with $t$. The window holds $\min(b + 1, p + e + 1) - \max(a, p - e) + 1 \le 2e + 2$ candidate values of $r(x)$, which is $2e + 1$ array entries to compare. $\square$

The tests check Theorem 1 against a dynamic program over all splits into runs, with a brute-force validity test by Helly's theorem: a run is valid if and only if every three of its points are, and three points are if and only if the middle one is within $2e$ of the line through the outer two. They check Lemma 4, the error bound of every segment, and Theorem 2 against `bisect` on three key distributions.
