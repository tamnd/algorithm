---
title: The key rule u^(1/w) gives successive sampling, and A-ExpJ has the same law as A-Res
proves: [correctness, termination]
status: full
---

**Statement.** Let items $1, \ldots, n$ have weights $w_i > 0$, let $W = \sum_i w_i$, and let $k \le n$. Assume exact real arithmetic and independent uniform random reals. Say that a random sequence $(X_1, \ldots, X_k)$ of distinct items is a *successive sample* if, for every sequence $(i_1, \ldots, i_k)$ of distinct items,
$$\Pr[(X_1, \ldots, X_k) = (i_1, \ldots, i_k)] = \prod_{j=1}^{k} \frac{w_{i_j}}{W - w_{i_1} - \cdots - w_{i_{j-1}}}.$$
This is the law of $k$ draws without replacement in which each draw picks a remaining item with probability proportional to its weight. Then:

1. A-RES returns a successive sample.
2. A-EXPJ returns a sample with the same law as A-RES.

Both stop after one pass. (For $n < k$ both return all items, ordered as a successive sample of size $n$.)

**Step 1: A-RES keeps the $k$ largest keys.** Invariant: after an item is processed, $H$ holds the $\min(k, t)$ largest keys among the first $t$ items. It holds for $t = 0$. If $|H| < k$, line L4 adds the new key. Otherwise the new key is among the $k$ largest of the first $t + 1$ keys if and only if it is larger than the least key in $H$, and then the least key of $H$ is the one that drops out, which line L5 does. Line L6 lists $H$ by decreasing key. Ties between keys have probability 0.

**Step 2: keys as exponential clocks.** Put $D_i = -\ln(u_i)/w_i$. Since $-\ln u_i$ has the exponential law with rate 1, $\Pr[D_i > x] = \Pr[u_i < e^{-w_i x}] = e^{-w_i x}$, so $D_i$ has the exponential law with rate $w_i$, and the $D_i$ are independent. The key is $r_i = u_i^{1/w_i} = e^{-D_i}$, so a larger key means a smaller $D_i$. So A-RES returns the items with the $k$ smallest values $D_i$, in increasing order of $D_i$.

**Step 3: the race lemma.** Let $A$ be a set of items with independent $D_i$ of rates $w_i$, and $W_A = \sum_{i \in A} w_i$. For $j \in A$ and $s_i \ge 0$,
$$\Pr\big[D_j \text{ is the least, and } D_i - D_j > s_i \text{ for all } i \in A \setminus \{j\}\big] = \int_0^\infty w_j e^{-w_j m} \prod_{i \ne j} e^{-w_i (m + s_i)}\,dm = \frac{w_j}{W_A} \prod_{i \ne j} e^{-w_i s_i}.$$
Taking all $s_i = 0$ gives $\Pr[D_j \text{ is the least}] = w_j / W_A$. Dividing, given that $D_j$ is the least, the differences $D_i - D_j$ for $i \ne j$ are independent and exponential with rates $w_i$, which is the same law as the $D_i$ of the set $A \setminus \{j\}$.

**Step 4: the order is a successive sample.** By induction on $j$. The item with the least $D$ is $i_1$ with probability $w_{i_1}/W$, by step 3 with $A$ all items. Given that, the remaining differences $D_i - D_{i_1}$ are independent exponentials with rates $w_i$, and their order is the order of the remaining $D_i$. So the second item is $i_2$ with probability $w_{i_2}/(W - w_{i_1})$, by step 3 again, and so on. Multiplying gives the product in the statement. With step 2, this proves part 1.

**Step 5: one entry of A-RES, seen from the threshold.** Fix the moment after the reservoir is full and an item has just been processed, with least key $T$ in $H$. The keys of the later items are independent of everything so far. A later item $i$ enters exactly when $r_i > T$, that is, when $u_i > T^{w_i}$, which has probability $1 - T^{w_i}$, independently for each item, until the first entry. Given that it enters, $u_i$ is uniform on $(T^{w_i}, 1)$, so its key is $u_i^{1/w_i}$ for such a $u_i$. So, with $S_j$ the total weight of the first $j$ later items, the first later entry is at item $j$ with probability
$$\prod_{i<j} T^{w_i} \cdot (1 - T^{w_j}) = T^{S_{j-1}} - T^{S_j}.$$

**Step 6: A-EXPJ makes the same move.** Lines L8 and L14 draw $X = \ln(V) / \ln(T)$ for a uniform $V$. For $0 < T < 1$, $\Pr[X > s] = \Pr[\ln V < s \ln T] = \Pr[V < T^s] = T^s$. Lines L10 and L11 let item $j$ enter at the first $j$ with $S_j \ge X$. So the entry is at item $j$ with probability $\Pr[S_{j-1} < X \le S_j] = T^{S_{j-1}} - T^{S_j}$, as in step 5. Line L12 gives the entering item the key $u^{1/w}$ with $u = T^w + (1 - T^w)V'$ uniform on $(T^w, 1)$, as in step 5. Line L13 removes the least key, as line L5 does. Lines L7 to L8 fill the reservoir with the same keys as A-RES.

So both methods are Markov chains on the state (position, keys in $H$), started in the same law and with the same law of each move, using fresh random numbers in each move. By induction on the number of entries, the final states have the same law, and so have the outputs. This proves part 2.

**Termination.** Each method reads each item once and does $O(\log k)$ heap work per item. $\blacksquare$
