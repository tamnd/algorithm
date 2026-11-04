---
title: The exact expected cost of a search in linear probing
proves: [statement]
status: full
---

This proof covers parts (a), (b) and (d) of the statement. Part (d) uses part (c), which is Knuth's result (The Art of Computer Programming, Volume 3, Section 6.4) and is not proved here.

**Setting.** Slots are $0, \ldots, m-1$, and all slot arithmetic is modulo $m$. A *hash sequence* is a word $a = (a_1, \ldots, a_n) \in \{0, \ldots, m-1\}^n$, where $a_i$ is the home of the $i$-th key. Running linear probing on $a$ (insert key $i$ at the first empty slot of $a_i, a_i + 1, \ldots$, for $i = 1, \ldots, n$) gives a final table $\tau(a)$, which says which key is in each slot. We assume $n < m$, so every insert finds an empty slot. The *path* of key $i$ is the list of slots from $a_i$ to its final slot.

**Fact 1.** A slot that is empty in $\tau(a)$ is on no path, and the home of each key is full in $\tau(a)$.

*Proof.* When key $i$ is inserted, each slot of its path before the last one is full, and the last one becomes full. No slot is ever emptied. So every slot of every path is full at the end. The home $a_i$ is the first slot of the path of key $i$. $\square$

**Lemma 1 (rotation).** For integers $a \ge 1$ and $0 \le b < a$, let $f(a, b)$ be the number of hash sequences of $b$ keys in a circle of $a$ slots after which a fixed slot $s$ is empty. Then $f(a, b) = (a - b)\, a^{b-1}$, and this number does not depend on $s$.

*Proof.* Let $\rho$ add 1 to each entry of a sequence. By induction on the number of inserts, the run on $\rho(a)$ puts each key one slot further than the run on $a$, because each probe is shifted by one and sees a shifted table. So slot $s$ is empty after $a$ exactly when slot $s + 1$ is empty after $\rho(a)$. Since $\rho$ is a bijection of the $a^b$ sequences, every slot is empty after the same number $N$ of sequences. Count the pairs (sequence, empty slot) in two ways: each sequence leaves exactly $a - b$ empty slots, so $a \cdot N = a^b (a - b)$, and $N = (a - b) a^{b-1}$. For $b = 0$ this is $1$, the empty sequence. $\square$

**Lemma 2 (splitting).** Let $1 \le k \le n$ and $k \le m - 2$. Let $g(k)$ be the number of hash sequences $a$ of length $n$ such that in $\tau(a)$ slot 0 is empty, slots $1, \ldots, k$ are full, and slot $k+1$ is empty. Then
$$g(k) = \binom{n}{k} f(k+1, k)\, f(m-k-1, n-k) = \binom{n}{k}(k+1)^{k-1} f(m-k-1, n-k).$$

*Proof.* Let $A = \{1, \ldots, k\}$ and $B = \{k+2, \ldots, m-1\}$, a set of $m - k - 2$ slots. We build a bijection between the sequences counted by $g(k)$ and the triples $(S, u, v)$, where $S$ is a set of $k$ of the $n$ keys, $u$ is a hash sequence for the keys of $S$ (in their order) in a circle of $k + 1$ slots $\{0, \ldots, k\}$ that leaves slot $k$ empty, and $v$ is a hash sequence for the other $n - k$ keys in a circle of $m - k - 1$ slots $\{0, \ldots, m-k-2\}$ that leaves slot $m-k-2$ empty. By Lemma 1 there are $\binom{n}{k} f(k+1, k) f(m-k-1, n-k)$ triples, and $f(k+1, k) = (k+1)^{k-1}$.

*From a sequence to a triple.* Take $a$ counted by $g(k)$. By Fact 1, no path contains slot 0 or slot $k+1$. A path is a run of consecutive slots, so each path lies inside $A$ or inside $B$, and so does its home. Let $S$ be the keys with home in $A$; they fill exactly the slots of $A$, so $|S| = k$. Let $u$ give each key of $S$ the home $a_i - 1$, and $v$ give each other key the home $a_i - (k+2)$, which lies in $\{0, \ldots, m-k-3\}$. We claim that the run on $u$ in the small circle places each key of $S$ in its slot in $\tau(a)$ minus 1, and leaves slot $k$ empty. By induction on the inserts: before each insert of a key of $S$, the full slots of $A$ in the run on $a$ are the shifted full slots of $\{0, \ldots, k-1\}$ in the run on $u$, and slot $k$ of the small circle is empty. The insert of a key $i \in S$ in the run on $a$ follows a path inside $A$, and the same steps, shifted by one, form the first empty slot after $a_i - 1$ in the small circle. Keys outside $S$ do not change $A$. In the same way, the run on $v$ copies the run on $a$ restricted to $B$, shifted by $k + 2$, and its last slot $m - k - 2$, which stands for slot 0 of the big table, stays empty, since no path of the big run reaches slot 0. So $(S, u, v)$ is a triple of the kind above.

*From a triple to a sequence.* Take a triple $(S, u, v)$. By Fact 1 for the small circle, no key of $S$ has home $k$, so its home in the big table, $u_i + 1$, is in $A$. By Fact 1 for the other circle, no key has home $m - k - 2$, so its home $v_i + k + 2$ is in $B$. Define $a$ this way. By induction on the inserts, as above, the run on $a$ keeps slot 0 and slot $k+1$ empty and copies the two small runs into $A$ and $B$: an insert of a key of $S$ meets only slots of $A$ before it stops, because the small run stops before slot $k$, and an insert of another key meets only slots of $B$, because its small run stops before slot $m - k - 2$. At the end, the $k$ keys of $S$ fill $A$, so $a$ is counted by $g(k)$.

The two maps are inverse to each other, because each one only shifts the homes and selects the keys by the block of their home. $\square$

**Proof of (a).** Fix a hash sequence $a$ and its table $\tau(a)$. A failed search that starts at slot $s$ probes $s, s+1, \ldots$ up to and including the first empty slot. If $s$ is empty, it costs 1. Assume first $n \le m - 2$, so the table has at least two empty slots. Then the full slots form maximal runs, and each run of $k$ slots has an empty slot just before it and a different empty slot just after it. A search that starts at the $t$-th slot from the end of a run, for $t = 1, \ldots, k$, costs $t + 1$. So the total cost over all $m$ start slots is

$$\sum_{s=0}^{m-1} \mathrm{cost}(s) = m + \sum_{k \ge 1} R_k(a)\, \frac{k(k+1)}{2},$$

where $R_k(a)$ is the number of runs of length $k$. A run of length $k$ is a slot $j$ such that $j$ is empty, $j + 1, \ldots, j + k$ are full and $j + k + 1$ is empty. By the rotation of Lemma 1, the number of sequences for which this holds at $j$ is the same for every $j$, so it is $g(k)$ for each $j$, and $\sum_a R_k(a) = m\, g(k)$. The search key has a uniform start slot, independent of $a$. Hence

$$C'_{m,n} = \frac{1}{m^n} \sum_a \frac{1}{m} \sum_{s} \mathrm{cost}(s) = 1 + \frac{1}{m^n} \sum_{k=1}^{n} g(k)\, \frac{k(k+1)}{2},$$

and Lemma 2 gives the formula of (a). A run has at most $n \le m - 2$ slots, so Lemma 2 applies to each $k$ in the sum.

If $n = m - 1$, the table has exactly one empty slot, and the $m - 1$ full slots form one run. The total cost is $m + (m-1)m/2$, and $C'_{m,m-1} = 1 + (m-1)/2 = (m+1)/2$ for every sequence. $\square$

**Proof of (b).** Fix $i \in \{1, \ldots, n\}$. The search for key $i$ probes $a_i, a_i + 1, \ldots$ until it finds key $i$. The slots before the final slot $p_i$ of key $i$ were full when key $i$ was inserted and hold other keys, and slot $p_i$ holds key $i$, so the search makes exactly as many probes as the insert of key $i$ did. The insert of key $i$ is a failed search for a key with home $a_i$ in the table $\tau(a_1, \ldots, a_{i-1})$, and it costs the same number of probes, the final empty slot counted. The value $a_i$ is uniform and independent of $a_1, \ldots, a_{i-1}$, which are themselves independent and uniform. So the expected cost of the search for key $i$ is $C'_{m, i-1}$. Averaging over $i$ uniform in $\{1, \ldots, n\}$ gives (b). $\square$

**Proof of (d), from (c).** Let $m \to \infty$ with $n/m \to \alpha < 1$. Fix $\beta$ with $\alpha < \beta < 1$. For all large $m$, $n/m \le \beta$. For $r \in \{0, 1\}$ and a fixed $k$, the term

$$t_k(m) = \binom{r+k}{k} \prod_{j=0}^{k-1} \frac{n - j}{m}$$

tends to $\binom{r+k}{k} \alpha^k$, since each factor $(n - j)/m$ tends to $\alpha$. For all large $m$ and all $k$, $0 \le t_k(m) \le \binom{r+k}{k} \beta^k$, because each factor is at most $n/m \le \beta$ (factors with $j \ge n$ make the term 0). The bound is summable, since $\sum_k \binom{r+k}{k} \beta^k = (1-\beta)^{-(r+1)}$ by the negative binomial series. By dominated convergence for series (Tannery's theorem),

$$Q_r(m, n) \to \sum_{k \ge 0} \binom{r+k}{k} \alpha^k = \frac{1}{(1-\alpha)^{r+1}}.$$

The same holds for $Q_0(m, n-1)$, since $(n-1)/m \to \alpha$ too. With (c), $C'_{m,n} \to \frac{1}{2}\left(1 + (1-\alpha)^{-2}\right)$ and $C_{m,n} \to \frac{1}{2}\left(1 + (1-\alpha)^{-1}\right)$. $\blacksquare$
