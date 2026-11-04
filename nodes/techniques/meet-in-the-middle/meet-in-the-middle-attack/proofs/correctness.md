---
title: The meet-in-the-middle attack returns exactly the consistent key pairs
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The keys are $\mathcal{K} = \{0, 1, \ldots, K-1\}$ and the blocks are $\mathcal{B} = \{0, 1, \ldots, N-1\}$. For each key $k$, $E_k : \mathcal{B} \to \mathcal{B}$ is a bijection and $D_k$ is its inverse. There are $t \ge 1$ known pairs $(P_i, C_i)$. The target set is

$$R^* = \{(k_1, k_2) \in \mathcal{K}^2 : E_{k_2}(E_{k_1}(P_i)) = C_i \text{ for } i = 1, \ldots, t\}.$$

**Claim.** MEET-IN-THE-MIDDLE stops after $2K + 2c(t-1)$ cipher calls, where $c$ is the number of pairs $(k_1, k_2)$ with $E_{k_2}(E_{k_1}(P_1)) = C_1$. The list $R$ that it returns holds each element of $R^*$ exactly once and holds nothing else.

**Step 1 (the table).** We show this invariant of the loop of line L2:

> **(T)** Before the iteration with $k_1 = j$, for each block $x$, the list $T[x]$ holds the keys $k \in \{0, \ldots, j-1\}$ with $E_k(P_1) = x$, each one exactly once, in increasing order.

*Initialization.* For $j = 0$ the set of keys is empty, and line L1 makes each list empty.

*Maintenance.* The iteration with $k_1 = j$ appends $j$ to the list $T[E_j(P_1)]$ and changes no other list. So the list of the block $x = E_j(P_1)$ gains the key $j$, which is larger than each key in it, and the other lists still hold the right keys. This is (T) for $j + 1$.

*Termination.* The loop stops after $j = K - 1$. Then (T) with $j = K$ says: for each block $x$, $T[x] = \{k \in \mathcal{K} : E_k(P_1) = x\}$, each key once.

**Step 2 (the candidates).** Fix $k_2 \in \mathcal{K}$ and let $X = D_{k_2}(C_1)$ (line L6). For a key $k_1$, Step 1 gives: $k_1 \in T[X]$ if and only if $E_{k_1}(P_1) = D_{k_2}(C_1)$. Apply the bijection $E_{k_2}$ to both sides. Since $E_{k_2}(D_{k_2}(C_1)) = C_1$, and since $E_{k_2}$ is one-to-one, this holds if and only if $E_{k_2}(E_{k_1}(P_1)) = C_1$. So the loop of line L7 visits exactly the keys $k_1$ such that $(k_1, k_2)$ is consistent with the first pair, each one once.

**Step 3 (the filter).** For such a candidate, line L8 appends $(k_1, k_2)$ to $R$ if and only if it is also consistent with the pairs $2, \ldots, t$. With Step 2, the iteration of line L5 for $k_2$ appends exactly the elements of $R^*$ whose second key is $k_2$, each one once.

**Step 4 (the result).** The loop of line L5 takes each $k_2 \in \mathcal{K}$ once. Different values of $k_2$ append different pairs. So at line L10, $R$ holds each element of $R^*$ exactly once and nothing else.

**Termination and cost.** The loops of lines L2 and L5 have $K$ iterations each, with one cipher call each. By Step 2, the loop of line L7 runs $c$ times in total. Each run of line L8 makes at most two cipher calls for each of the pairs $2, \ldots, t$. Each loop runs over a finite range or a finite list, so the procedure stops, after at most $2K + 2c(t-1)$ cipher calls. $\blacksquare$

**Order.** Line L5 takes $k_2$ in increasing order, and by Step 1 each list $T[X]$ is in increasing order. So $R$ is sorted by $k_2$, and by $k_1$ for equal $k_2$.
