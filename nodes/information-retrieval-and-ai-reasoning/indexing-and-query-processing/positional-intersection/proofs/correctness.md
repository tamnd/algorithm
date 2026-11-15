---
title: Positional intersection returns exactly the pairs of positions within distance k, in time linear in the input and the output
proves: [correctness]
status: full
---

The input is two positional lists $p_1$ and $p_2$, of lengths $m$ and $n$, and an integer $k \ge 0$. Each list holds pairs $(d, X)$ with strictly increasing ids $d$, and each position list $X$ is strictly increasing. The output is the set
$$\mathcal{A} = \{(d, x, y) : (d, X) \in p_1,\ (d, Y) \in p_2,\ x \in X,\ y \in Y,\ |x - y| \le k\},$$
listed in increasing order of $(d, x, y)$. The line numbers are those of the main block of the page.

**Lemma 1 (the documents).** Lines L1, L2 and L12 to L14 run the inner block of lines L4 to L11 exactly once for each id common to both lists, in increasing order of the id, and make at most $m + n - 1$ passes of line L2 when $m, n \ge 1$.

*Proof.* This is the merge of the two id lists, with the pairs in place of the ids. Before each test of line L2, every common id that has not been handled is at index at least $i$ in $p_1$ and at least $j$ in $p_2$: line L13 drops an id less than every id left in $p_2$, line L14 drops an id less than every id left in $p_1$, and line L12 drops a common id after the block has handled it. Each pass adds one to $i$ or to $j$ or to both, and the loop stops when one index reaches the end, so there are at most $m + n - 1$ passes. The full proof of the merge is on the [merge-based list intersection](/merge-based-list-intersection/) page. $\square$

**Lemma 2 (the window).** Fix a common document $d$ with position lists $X = (x_1 < \cdots < x_a)$ and $Y = (y_0 < \cdots < y_{c-1})$. After line L10 runs for $x = x_i$, the queue $W$ holds exactly the positions $y \in Y$ with $|x_i - y| \le k$, in increasing order.

*Proof.* Let $b_i$ be the value of $b$ after the loop of lines L6 to L9 for $x_i$, and put $b_0 = 0$. We prove by induction on $i$ three facts after line L10 for $x_i$:

- (a) every $y_q$ with $q < b_i$ satisfies $y_q \le x_i + k$;
- (b) if $b_i < c$, then $y_{b_i} > x_i + k$;
- (c) $W$ holds, in increasing order, exactly the $y_q$ with $q < b_i$ and $x_i - k \le y_q \le x_i + k$.

The loop of lines L6 to L9 looks at $y_b$ for $b = b_{i-1}, b_{i-1} + 1, \ldots$. Line L7 adds $y_b$ to $W$ when $|x_i - y_b| \le k$. Line L8 stops the loop, with no change to $b$, when $y_b > x_i + k$. Otherwise $y_b < x_i - k$, and line L9 moves on with no change to $W$. So each $y_q$ with $b_{i-1} \le q < b_i$ is at most $x_i + k$, and it is added to $W$ if and only if it is at least $x_i - k$. Together with (a) for $i - 1$ and $x_{i-1} < x_i$, this gives (a) for $i$, and the stop rule gives (b).

For (c), the elements of $W$ are added in increasing order of $q$, and so of value, and line L10 removes only from the front, so $W$ stays increasing. Every element of $W$ is at most $x_i + k$: those added for $x_i$ by line L7, and the older ones by (a) for $i - 1$. So the test $|front(W) - x_i| > k$ of line L10 means $front(W) < x_i - k$, and since $W$ is increasing, line L10 removes exactly the elements less than $x_i - k$. It remains to see that $W$, before line L10, holds every $y_q$ with $q < b_i$ and $y_q \ge x_i - k$. For $b_{i-1} \le q < b_i$ this was shown above. For $q < b_{i-1}$, (a) for $i - 1$ gives $y_q \le x_{i-1} + k$, so by (c) for $i - 1$, $y_q$ is in $W$ after step $i - 1$ if and only if $y_q \ge x_{i-1} - k$. A $y_q \ge x_i - k$ satisfies this, because $x_i > x_{i-1}$, so it is in $W$. For $i = 1$, the facts for step 0 hold with $b_0 = 0$ and $W$ empty, and the same argument applies.

Finally, by (b) and because $Y$ is increasing, every $y_q$ with $q \ge b_i$ is greater than $x_i + k$. So the $y \in Y$ with $|x_i - y| \le k$ are exactly the $y_q$ with $q < b_i$ and $x_i - k \le y_q \le x_i + k$, which is $W$ by (c). $\square$

**Theorem 1 (correctness).** POSITIONAL-INTERSECT$(p_1, p_2, k)$ returns $\mathcal{A}$, in increasing order of $(d, x, y)$.

*Proof.* A triple of $\mathcal{A}$ has $d$ common to both lists. By Lemma 1, the block of lines L4 to L11 runs for each common $d$ once, in increasing order of $d$. In it, line L11 appends $(d, x, y)$ for $y \in W$, which by Lemma 2 are exactly the $y \in Y$ with $|x - y| \le k$, in increasing order, for each $x \in X$ in increasing order. $\blacksquare$

**Theorem 2 (cost).** Let $P$ be the total length of the position lists of the two terms in their common documents, and let $z = |\mathcal{A}|$. The algorithm runs in $O(m + n + P + z)$ time. The passes of line L6 number at most $P$, and the queue holds at most $\min(2k + 1, |Y|)$ positions.

*Proof.* Lemma 1 bounds the passes of line L2 by $m + n - 1$. In a common document, each pass of line L6 either moves $b$ forward, at most $|Y|$ times, or stops the loop at line L8, at most once for each $x \in X$. So the passes are at most $|X| + |Y|$ for this document, and at most $P$ in total. Each position of $Y$ enters $W$ at most once, so line L10 removes at most $|Y|$ elements in this document. Line L11 does one step for each output triple. By Lemma 2, $W$ holds distinct integers of the range $[x - k, x + k]$ after line L10, so at most $2k + 1$ of them. $\blacksquare$

**Theorem 3 (phrases).** For a phrase of terms $w_0, \ldots, w_{r-1}$ with positional lists $L_0, \ldots, L_{r-1}$, the function `phrase_matches` of the code returns exactly the pairs $(d, x)$ such that $w_j$ stands at position $x + j$ of $d$ for each $j$, in increasing order.

*Proof.* The outer loop takes the largest current id $top$ and moves forward every list whose current id is less than $top$. Such an id cannot be common, because the list with id $top$ has no smaller id left. When no list moves, all current ids equal $top$, which is then common; after it, all indices move. So the loop handles each common id once, in increasing order, and stops when a list ends. In a common document, let $X_j$ be the positions of $w_j$. The candidate list starts as $X_0$ and, for $j = 1, \ldots, r - 1$, keeps the $x$ with $x \in X_j - j$, where $X_j - j = \{y - j : y \in X_j\}$ is increasing. This is the merge intersection of two increasing lists with one forward index $b$: an element $y - j < x$ that the loop skips is less than every later candidate. So after round $j$ the list holds the $x \in X_0$ with $x + j' \in X_{j'}$ for all $j' \le j$, and after the last round the matches of the phrase in $d$. The number of passes of the inner loops is at most $|X_j| + |X_0|$ for round $j$, and that of the outer loop is at most $\sum_j |L_j|$. $\blacksquare$
