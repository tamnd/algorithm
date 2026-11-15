---
title: The adaptive intersection is correct and within a constant factor of the log2 C(m+n, m) lower bound
proves: [correctness]
status: full
---

The input is $k \ge 1$ lists $L_0, \ldots, L_{k-1}$, each strictly increasing, sorted so that $n_0 \le n_1 \le \cdots \le n_{k-1}$, where $n_s = |L_s|$. A test is one two-way comparison of ids, $<$ or $=$. The line numbers are those of the main block of the page. If a list is empty, the algorithm returns the empty list with no test, which is correct, so from here each $n_s \ge 1$. The state is the eliminator $e$, the set $H$ of lists that are known to hold $e$ (the set *held*), and for each list $s$ the index $pos(s)$ and the step $jump(s)$.

**Invariant.** Before each check of line L4:

- (I1) the output is strictly increasing, each output id is common to all lists, and each output id is less than $e$;
- (I2) each common id that is not in the output is at least $e$;
- (I3) for each list $s \notin H$, every id of $L_s$ at an index below $pos(s)$ is less than $e$;
- (I4) for each list $s \in H$, $L_s[pos(s) - 1] = e$, and every id of $L_s$ at a lower index is less than $e$.

**Lemma 1.** The invariant holds at the start and after each pass of the loop.

*Proof.* At the start, $e = L_0[0]$, $pos(0) = 1$, $H = \{0\}$ and $pos(s) = 0$ for $s \ne 0$. (I1) holds with an empty output, (I3) holds with no ids below index 0, and (I4) holds for list 0. A common id is in $L_0$, so it is at least $L_0[0] = e$, which is (I2).

*Lines L5 to L7.* When $H$ holds all $k$ lists, (I4) says that $e$ is in each list, so $e$ is common. By (I1) it is greater than the ids already in the output, so the output stays strictly increasing after line L5. Let $\ell$ be the list of the last search. If $pos(\ell) < n_\ell$, line L7 sets $e' = L_\ell[pos(\ell)]$, the next id of $L_\ell$ after $e$, so $e' > e$. (I1) holds because the new output id $e$ is less than $e'$. A common id that is not in the output is at least $e$ by (I2), is not $e$, and is in $L_\ell$, so it is at least $e'$, which is (I2). (I4) holds for $\ell$ after $pos(\ell)$ grows by one. For each other list, the ids below $pos(s)$ are at most $e < e'$, which is (I3), because $H$ is now $\{\ell\}$.

*Lines L10 to L13.* A step on a list $s \notin H$ probes $p \ge pos(s)$. If $L_s[p] < e$, every id of $L_s$ up to index $p$ is less than $e$, so (I3) holds after $pos(s) \leftarrow p + 1$. Nothing else changes.

*Lines L14 to L18.* If $L_s[p] \ge e$, the binary search on $[pos(s), p]$ uses $L_s[p] \ge e$ and (I3), so it returns the least index $a$ with $L_s[a] \ge e$ (Lemma 2 of the proof file of the [posting list](/posting-list/) page). Then $pos(s) = a + 1$. If $L_s[a] = e$, list $s$ joins $H$ and (I4) holds for it. Else $e' = L_s[a] > e$ and $H = \{s\}$. (I4) holds for $s$. For each other list, the ids below its index are at most $e < e'$ by (I3) and (I4), so (I3) holds for it. A common id not in the output is at least $e$ by (I2), and it is in $L_s$, so it is at least $L_s[a] = e'$, which is (I2). (I1) holds because $e' > e$. $\square$

**Theorem 1 (correctness).** The algorithm stops, and it returns the ids common to all lists, in increasing order.

*Proof.* Each pass either stops or increases $\sum_s pos(s)$: line L7 adds one to $pos(\ell)$, line L13 sets $pos(s) = p + 1$ with $p \ge pos(s)$, and line L16 sets $pos(s) = a + 1$ with $a \ge pos(s)$. This sum is at most $\sum_s n_s$, so the loop stops. It stops at one of three lines.

- Line L6: the common id $e$ was output, and the list $\ell$ has no id after $e$, so no common id is greater than $e$.
- Line L9: $pos(s) = n_s$ for a list $s \notin H$, so by (I3) every id of $L_s$ is less than $e$.
- Line L12: $L_s[n_s - 1] < e$, so every id of $L_s$ is less than $e$.

In the last two cases, no common id is at least $e$. In all three cases, (I2) says that each common id is in the output, and (I1) says that the output holds only common ids, in increasing order. $\blacksquare$

## The count of tests

A *run* of list $s$ is a maximal sequence of steps of lines L10 and L11 on $s$ that starts with $jump(s) = 1$. A run ends with a binary search (lines L14 to L18), with the stop of line L12, or when the algorithm stops at another line. Let $r_s$ be the number of runs of list $s$; the code counts it. Let $P$ be the value of $pos(s)$ at the start of a run, and let its *span* $c$ be $n_s - P$ if the run ends at line L12, and the value of $pos(s)$ at its end minus $P$ in the other cases.

**Lemma 2 (one run).** A run with span $c$ has $c \ge 1$ and makes at most $2 \log_2 c + 2$ tests.

*Proof.* Step $i$ of the run, for $i = 0, 1, \ldots$, starts with $pos(s) = P + 2^i - 1$ and $jump(s) = 2^i$, and probes $p = \min(P + 2^{i+1} - 2, n_s - 1)$. Let the run make $t$ steps with the result "less than", then one more step.

- If the last step has the result "not less", the binary search runs on $[pos(s), p]$, a range of at most $2^t$ indices whose last index is known to hold an id at least $e$. It makes at most $t$ tests, because each test halves this range. Line L17 makes one more test. The total is at most $(t + 1) + t + 1 = 2t + 2$. The new index is $a + 1 \ge P + 2^t$, so $c \ge 2^t$ and $t \le \log_2 c$.
- If the last step stops at line L12, the run made $t + 1$ tests, and $p = n_s - 1 \ge P + 2^t - 1$, so $c \ge 2^t$, and $t + 1 \le 2 \log_2 c + 2$.
- If the algorithm stops on another list after $t \ge 1$ steps of this run, the run made $t$ tests and $c = 2^t - 1 \ge 2^{t-1}$, so $t \le 2(t - 1) + 2 \le 2 \log_2 c + 2$.

In each case $c \ge 1$. $\square$

**Lemma 3 (one list).** List $s$ makes at most $2 r_s \log_2(1 + n_s / r_s) + 2 r_s$ tests, or none if $r_s = 0$.

*Proof.* Each test is made in a run of the list that makes it. The index $pos(s)$ never goes down and a run starts at the current index, so the spans of the runs of $s$ cover disjoint ranges of indices, and their sum is at most $n_s$. By Lemma 2 and Jensen's inequality for the concave function $\log_2$, the runs make at most $\sum_j (2 \log_2 c_j + 2) \le 2 r_s \log_2(n_s / r_s) + 2 r_s$ tests, which is at most the bound. $\square$

**Lemma 4.** Let $E$ be the number of values that $e$ takes. Then $r_s \le E$ for each list $s$.

*Proof.* A run of $s$ starts only when $s \notin H$. A run that does not end the algorithm ends at line L17 or L18 with $s \in H$, and $s$ leaves $H$ only when $e$ changes, at line L7 or line L18. So two runs of $s$ start under two different values of $e$. $\square$

With Lemma 4 and the fact that $h(t) = t \log_2(1 + c/t)$ is nondecreasing in $t > 0$ for each $c \ge 0$, the total number of tests is at most $\sum_s (2E \log_2(1 + n_s / E) + 2E)$. Each value of $e$ is an id of the input, and the values increase, so $E$ is at most the number of distinct ids. On inputs with a short proof of the result, $E$ is small.

**Theorem 2 (two lists).** For $k = 2$ with $m = n_0 \le n = n_1$, the algorithm makes at most

$$2m \log_2\left(1 + \frac{n}{m}\right) + 6m \;\le\; 8 \log_2 \binom{m+n}{m}$$

tests.

*Proof.* When $k = 2$ and $H$ is not full, $H$ holds one list and each step is on the other one. A run of list $s$ ends with $s \in H$, and if line L7 follows, $H$ becomes $\{s\}$ again. So the runs of the two lists alternate, and the first run is a run of list 1. This gives $r_1 \le r_0 + 1$. Each run of list 0 has span at least 1 by Lemma 2, the spans are disjoint, and none of them holds index 0, which line L2 takes with no test. So $r_0 \le m - 1$ and $r_1 \le m$. By Lemma 3 and the monotone function $h$, list 0 makes at most $2m \log_2 2 + 2m = 4m$ tests and list 1 makes at most $2m \log_2(1 + n/m) + 2m$ tests. For the second form, $\binom{m+n}{m} = \prod_{i=1}^{m} \frac{n+i}{i} \ge (1 + n/m)^m$, so $\log_2 \binom{m+n}{m} \ge m \log_2(1 + n/m) \ge m$, because $n \ge m$. $\blacksquare$

## The lower bound

The comparison model: an algorithm sees the ids only through comparisons of two input ids, with the outcomes $<$, $=$ and $>$ (a two-way test gives less information). For fixed lengths, the algorithm is a decision tree, and each leaf fixes the output as a set of positions of $A$.

**Lemma 5 (adjacent pairs).** Let the input be two lists $A$ and $B$ with all ids distinct, so that $A \cap B$ is empty. In the merged order of all $m + n$ ids, let $x$ and $y$ be adjacent and in different lists. Then every correct algorithm compares $x$ with $y$ on this input.

*Proof.* Say $x$ is in $A$, $y$ is in $B$ and $x < y$; the other cases are the same. Suppose the algorithm does not compare $x$ with $y$. Change the input by giving $y$ the value of $x$. The list $B$ stays strictly increasing: the id of $B$ before $y$ is less than $y$, is not $x$, and no id lies between $x$ and $y$, so it is less than $x$. Each comparison of $y$ with an id $z \ne x$ has the same outcome as before, because no id lies strictly between $x$ and $y$, and $z \ne x$. Comparisons that do not involve $y$ do not change. So the new input follows the same path to the same leaf, and the algorithm gives the same output, the empty set. But on the new input, $x$ is common to both lists. This is a contradiction. $\square$

**Theorem 3 (lower bound).** Every algorithm in the comparison model that intersects two sorted lists of lengths $m$ and $n$ makes at least $\lceil \log_2 \binom{m+n}{m} \rceil$ comparisons on some input.

*Proof.* Take the $\binom{m+n}{m}$ inputs made from the ids $1, \ldots, m+n$, one for each choice of the $m$ ids that go to $A$; $B$ gets the rest. Let such an input reach the leaf $v$. By Lemma 5, the path to $v$ holds the outcome of each comparison of two adjacent ids from different lists, and the order of two adjacent ids from the same list is known in advance. So the outcomes on the path, with the order inside each list, fix the whole merged order, and with it the choice of the $m$ ids of $A$. So the $\binom{m+n}{m}$ inputs reach different leaves. On these inputs no comparison has the outcome $=$, so each node on their paths has at most two children that they use. A binary tree with at least $\binom{m+n}{m}$ leaves has depth at least $\log_2 \binom{m+n}{m}$, and depth is an integer. $\blacksquare$

**Corollary 4 (equal lengths).** For $m = n$, every correct algorithm makes at least $2n - 1$ comparisons on the input $a_1 < b_1 < a_2 < b_2 < \cdots < a_n < b_n$, because all $2n - 1$ adjacent pairs of the merged order are in different lists (Lemma 5). The [merge](/merge-based-list-intersection/) makes at most $2n - 1$ three-way steps, so it is exactly optimal in this count. $\square$

**Remark.** Lemma 5 is the reason that the cost of an adaptive algorithm can depend on the input and not only on the lengths. On a given input, the comparisons that a correct algorithm must make form a certificate of the result. When the two lists interleave in few blocks, this certificate is short, and the galloping steps of the algorithm find each block boundary at a cost that is logarithmic in the block length. Theorem 3 bounds the worst case over all inputs of the given lengths, and Theorem 2 shows that the algorithm meets it up to a factor of 8.
