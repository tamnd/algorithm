---
title: The sliding sorted window of OS-CFAR gives the k-th smallest reference value, its false alarm probability is a product that does not depend on the noise power, and few interferers cannot raise the threshold
proves: [correctness]
status: full
---

The notation is that of the page. The input is $x[0], \dots, x[n-1]$, one power value per range cell. $N = 2h$ is the even number of reference cells, $G \ge 0$ the number of guard cells on each side, $k$ the rank with $1 \le k \le N$ and $T > 0$ the factor. For a cell $i$ with $f = G + h \le i \le \ell = n - 1 - G - h$, the reference window is

$$W_i = \{i - G - h, \dots, i - G - 1\} \cup \{i + G + 1, \dots, i + G + h\}.$$

Let $M_i$ be the multiset of the values $x[c]$ for $c \in W_i$, and $X_{(k)}(i)$ its $k$-th smallest element, counted with multiplicity. The detector reports cell $i$ exactly when $x[i] > T X_{(k)}(i)$.

**Lemma 1 (the sorted window).** If $f \le \ell$, then at the start of the iteration for cell $i$ of the loop in line L2, the list $w$ is sorted and holds the multiset $M_i$.

*Proof.* By induction on $i$.

*Base, $i = f$.* Line L1 sorts the values of the cells of $W_f$, so $w$ is sorted and holds $M_f$.

*Step.* Assume the claim for $i < \ell$. As in the proof for CA-CFAR, $W_{i+1}$ is $W_i$ without the cells $i - G - h$ and $i + G + 1$, and with the cells $i - G$ and $i + G + h + 1$. The two cells that leave are different, and both are in $W_i$. So

$$M_{i+1} = M_i - \{x[i - G - h]\} + \{x[i - G]\} - \{x[i + G + 1]\} + \{x[i + G + h + 1]\},$$

where $-$ removes one copy of a value and $+$ adds one. Two copies of the same value cannot be told apart in a multiset, so removing one copy of the value $x[c]$ is the same as removing the cell $c$. Line L6 removes one copy of $x[i - G - h]$, which is in $w$, and inserts $x[i - G]$. Line L7 removes one copy of $x[i + G + 1]$ and inserts $x[i + G + h + 1]$. The value $x[i + G + 1]$ is still in $w$ when line L7 runs, because line L6 removed one copy of a different cell's value and $M_i$ held a copy for each cell. A binary search finds a copy of the value in a sorted list, and deleting it keeps the list sorted. Inserting at the position that a binary search gives also keeps it sorted. So after line L7, $w$ is sorted and holds $M_{i+1}$. $\square$

**Theorem 1 (the output).** For every input, the detector reports exactly the cells $i$ with $f \le i \le \ell$ and $x[i] > T X_{(k)}(i)$, in increasing order.

*Proof.* The loop visits $i = f, \dots, \ell$ in order. By Lemma 1, $w$ is the sorted list of $M_i$, so the element $w[k-1]$ read by line L3 (index from 0) is $X_{(k)}(i)$. Lines L4 and L5 compare $x[i]$ with $T X_{(k)}(i)$. $\square$

**Lemma 2 (the spacings of exponential order statistics).** Let $Y_1, \dots, Y_N$ be independent and exponential with mean $\mu$, with order statistics $Y_{(1)} \le \dots \le Y_{(N)}$, and put $Y_{(0)} = 0$. Then the spacings $D_j = Y_{(j)} - Y_{(j-1)}$, $j = 1, \dots, N$, are independent, and $D_j$ is exponential with mean $\mu / (N - j + 1)$.

*Proof.* The joint density of the order statistics is $N!\, \prod_{j} \mu^{-1} e^{-y_j/\mu}$ on $0 \le y_1 \le \dots \le y_N$. The map from $(y_1, \dots, y_N)$ to the spacings $d_j = y_j - y_{j-1}$ is linear with a triangular matrix of ones on the diagonal, so its Jacobian is 1, and it maps the ordered region onto $d_j \ge 0$. Each $y_j$ is $d_1 + \dots + d_j$, so $\sum_j y_j = \sum_j (N - j + 1) d_j$, because $d_j$ is part of $y_j, \dots, y_N$. With $N! = \prod_{j=1}^{N} (N - j + 1)$ the joint density of the spacings is

$$\prod_{j=1}^{N} \frac{N - j + 1}{\mu}\, e^{-(N - j + 1) d_j / \mu},$$

a product of exponential densities with means $\mu/(N - j + 1)$. $\square$

**Theorem 2 (constant false alarm rate).** Assume that the cell under test and its $N$ reference cells are independent and exponential with the same mean $\mu > 0$. Then

$$P_{fa}(T) = P(x[i] > T X_{(k)}) = \prod_{m=0}^{k-1} \frac{N - m}{N - m + T},$$

which does not depend on $\mu$. $P_{fa}(T)$ falls strictly from 1 to 0 as $T$ goes from 0 to $\infty$, so each $P_{fa}$ in $(0, 1)$ has exactly one $T$.

*Proof.* By Lemma 2, $X_{(k)} = D_1 + \dots + D_k$ with independent exponential $D_j$ of means $\mu/(N - j + 1)$. The cell under test $X$ is independent of the window, and given $X_{(k)} = z$, $P(X > Tz) = e^{-Tz/\mu}$. So

$$P_{fa}(T) = E\, e^{-T X_{(k)}/\mu} = \prod_{j=1}^{k} E\, e^{-(T/\mu) D_j} = \prod_{j=1}^{k} \left(1 + \frac{T}{N - j + 1}\right)^{-1},$$

by the transform $E\, e^{-sD} = (1 + s\nu)^{-1}$ of an exponential of mean $\nu$. Put $m = j - 1$ to get the product of the statement. Each factor is positive, equals 1 at $T = 0$, falls strictly in $T$ and goes to 0, so the product does the same. $\square$

The product equals Rohling's closed form $k \binom{N}{k} (k-1)!\, (T + N - k)! / (T + N)!$ for integer $T$. Write $k \binom{N}{k} (k-1)! = N!/(N-k)! = \prod_{m<k} (N - m)$ and $(T + N)!/(T + N - k)! = \prod_{m<k} (N - m + T)$.

**Theorem 3 (detection of a Swerling 1 target).** If the cell under test is exponential with mean $\mu(1 + S)$ and the reference cells are as in Theorem 2, then $P_d = P_{fa}(T/(1 + S))$.

*Proof.* Given $X_{(k)} = z$, $P(X > Tz) = e^{-Tz/(\mu(1+S))}$. This is the computation of Theorem 2 with $T/(1+S)$ in place of $T$. $\square$

**Theorem 4 (interfering targets).** Assume that at most $r \le N - k$ reference cells of $W_i$ hold interference, with any values, and let $c_1 \le c_2 \le \dots$ be the sorted values of the other $N - r \ge k$ cells. Then $X_{(k)}(i) \le c_k$. If moreover every interfering value is at least $c_k$, then $X_{(k)}(i) = c_k$, the same value as in a window of the $N - r$ clean cells alone.

*Proof.* The cells with the values $c_1, \dots, c_k$ are $k$ cells of the window with values at most $c_k$. So at least $k$ elements of $M_i$ are at most $c_k$, and the $k$-th smallest is at most $c_k$. If every interfering value is at least $c_k$, every element of $M_i$ below $c_k$ is one of $c_1, \dots, c_{k-1}$, so fewer than $k$ elements are below $c_k$ and $X_{(k)}(i) \ge c_k$. $\square$

So up to $N - k$ strong interferers in the window cannot raise the threshold above $T c_k$. For CA-CFAR, one interferer of power $A$ adds $A$ to the sum and raises the threshold without a limit. $\blacksquare$
