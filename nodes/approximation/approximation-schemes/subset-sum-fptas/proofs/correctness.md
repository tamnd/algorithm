---
title: The trimmed lists give a subset sum of at least OPT/(1 + ε) in polynomial time
proves: [correctness, time.worst]
status: full
---

We use the names of the pseudocode. The input is $n \ge 1$ positive integers $x_1, \ldots, x_n$, an integer target $t \ge 0$ and a number $0 < \varepsilon \le 1$, and $\delta = \varepsilon / (2n)$ as in line L1. Let $P_i$ be the set of all subset sums of $x_1, \ldots, x_i$, so $P_0 = \{0\}$ and $P_i = P_{i-1} \cup (P_{i-1} + x_i)$. Let $\mathrm{OPT} = \max \{ y \in P_n : y \le t \}$, which exists because $0 \in P_n$.

**Lemma 1 (TRIM).** Let $L = \langle y_1 < y_2 < \cdots < y_m \rangle$ be the input of TRIM and $L'$ its output. Then $L'$ is a sublist of $L$ that holds $y_1$, each two consecutive entries $a < b$ of $L'$ have $b > (1 + \delta) a$, and for each $y \in L$ there is a $z \in L'$ with $y / (1 + \delta) \le z \le y$.

*Proof.* Line L8 puts $y_1$ in $L'$, and line L10 appends $y_k$ only when $y_k > (1 + \delta) \cdot \mathit{last}$, where $\mathit{last}$ is the last entry of $L'$; this gives the first two claims. For the third, if $y \in L'$ take $z = y$. If $y = y_k$ was not appended, then at that moment $y_k \le (1 + \delta) \cdot \mathit{last}$, and $\mathit{last} = y_j$ for some $j < k$, so $\mathit{last} < y_k$. Take $z = \mathit{last}$. $\square$

**Lemma 2 (the lists are subset sums).** For each $i$, the list $L_i$ is sorted with no repeated entries, $L_i \subseteq P_i$, each entry is at most $t$, and $0 \in L_i$.

*Proof.* By induction on $i$. $L_0 = \langle 0 \rangle$ by line L2. If $L_{i-1} \subseteq P_{i-1}$, then $L_{i-1} + x_i \subseteq P_{i-1} + x_i$, so the merged list of line L4 is in $P_i$, and lines L5 and L6 only remove entries. The merge of line L4 keeps the order and drops repeats. The value 0 is the first entry of the merged list, so TRIM keeps it, and $0 \le t$. Line L6 removes the entries above $t$. $\square$

**Lemma 3 (the invariant).** For each $i$ and each $y \in P_i$ with $y \le t$, there is a $z \in L_i$ with

$$
\frac{y}{(1 + \delta)^i} \le z \le y.
$$

*Proof.* By induction on $i$. For $i = 0$, $y = 0 \in L_0$. Let $i \ge 1$ and $y \in P_i$ with $y \le t$. There are two cases.

- If $y \in P_{i-1}$, the induction gives $z' \in L_{i-1}$ with $y / (1 + \delta)^{i-1} \le z' \le y$.
- Otherwise $y = y' + x_i$ with $y' \in P_{i-1}$ and $y' < y \le t$. The induction gives $z'' \in L_{i-1}$ with $y' / (1 + \delta)^{i-1} \le z'' \le y'$. Let $z' = z'' + x_i$, which is in the merged list of line L4. Then $z' \le y$, and $z' \ge y' / (1 + \delta)^{i-1} + x_i \ge (y' + x_i) / (1 + \delta)^{i-1} = y / (1 + \delta)^{i-1}$, because $x_i > 0$.

In both cases $z'$ is in the merged list, and $y / (1 + \delta)^{i-1} \le z' \le y$. By Lemma 1, after line L5 there is a $z$ with $z' / (1 + \delta) \le z \le z'$. So $z \le y \le t$, and line L6 does not remove $z$. Also $z \ge y / (1 + \delta)^i$. $\square$

**Lemma 4 (the bound on the factor).** For $n \ge 1$ and $0 < \varepsilon \le 1$, $(1 + \varepsilon / (2n))^n \le 1 + \varepsilon$.

*Proof.* Since $1 + u \le e^u$ for each real $u$, $(1 + \varepsilon / (2n))^n \le e^{\varepsilon / 2}$. For $0 \le u \le 1$, the series gives $e^u = 1 + u + u^2 \sum_{k \ge 2} u^{k-2} / k! \le 1 + u + u^2 (e - 2) \le 1 + u + u^2$. With $u = \varepsilon / 2 \le 1/2$, this is $e^{\varepsilon/2} \le 1 + \varepsilon / 2 + \varepsilon^2 / 4 \le 1 + \varepsilon / 2 + \varepsilon / 4 < 1 + \varepsilon$. $\square$

**Theorem (correctness).** Line L7 returns a value $z^*$ with $z^* \in P_n$, $z^* \le t$ and

$$
z^* \ge \frac{\mathrm{OPT}}{1 + \varepsilon} \ge (1 - \varepsilon)\,\mathrm{OPT}.
$$

*Proof.* By Lemma 2, $z^*$ is a subset sum of at most $t$, so it is a feasible value, and the parent pointers of the implementation recover a subset with this sum. Apply Lemma 3 to $y = \mathrm{OPT}$ and $i = n$: some $z \in L_n$ has $z \ge \mathrm{OPT} / (1 + \delta)^n$. The largest entry $z^*$ of $L_n$ is at least $z$. By Lemma 4, $(1 + \delta)^n \le 1 + \varepsilon$, so $z^* \ge \mathrm{OPT} / (1 + \varepsilon)$. Last, $1 / (1 + \varepsilon) \ge 1 - \varepsilon$, because $(1 - \varepsilon)(1 + \varepsilon) = 1 - \varepsilon^2 \le 1$. $\blacksquare$

**Lemma 5 (the length of the lists).** For each $i \ge 1$ and $t \ge 1$,

$$
|L_i| \le \log_{1 + \delta} t + 2 \le \frac{3 n \ln t}{\varepsilon} + 2.
$$

*Proof.* Write $L_i = \langle 0 = z_0 < z_1 < \cdots < z_k \rangle$. Line L6 removes a suffix of the trimmed list, so the entries of $L_i$ are consecutive in the output of TRIM, and Lemma 1 gives $z_{j} > (1 + \delta) z_{j-1}$ for $j \ge 1$. The values are integers, so $z_1 \ge 1$, and $t \ge z_k > (1 + \delta)^{k-1} z_1 \ge (1 + \delta)^{k-1}$ when $k \ge 2$. So $k - 1 < \log_{1 + \delta} t$, or $k \le 1$, and in both cases $|L_i| = k + 1 \le \log_{1 + \delta} t + 2$. For the second bound, $\ln(1 + \delta) \ge \delta / (1 + \delta)$, so

$$
\log_{1 + \delta} t = \frac{\ln t}{\ln(1 + \delta)} \le \frac{(1 + \delta) \ln t}{\delta} = \frac{(2n + \varepsilon) \ln t}{\varepsilon} \le \frac{3 n \ln t}{\varepsilon},
$$

since $\varepsilon \le 1 \le n$. For $t = 0$ the list is $\langle 0 \rangle$. $\square$

**Running time.** Lines L4, L5 and L6 each take $O(|L_{i-1}|)$ time: the merge of two sorted lists of length $|L_{i-1}|$ is linear, and TRIM and the cut each make one pass. By Lemma 5 each step costs $O(n \log t / \varepsilon)$, and the $n$ steps cost $O(n^2 \log t / \varepsilon)$ in total. The numbers are at most $t + \max_i x_i$, and on the [word RAM](/word-ram/) an addition or a comparison of such numbers costs $O(1)$. With $\varepsilon = a / b$ rational, the test of line L10 is the integer test $2nb \cdot y_k > (2nb + a) \cdot \mathit{last}$. The input has $\Omega(n + \log t)$ bits, so the time is polynomial in the input size and in $1 / \varepsilon$. $\blacksquare$
