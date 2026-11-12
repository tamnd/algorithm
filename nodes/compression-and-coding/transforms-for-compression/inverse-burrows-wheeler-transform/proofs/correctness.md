---
title: The LF mapping steps one position to the left, so the walk writes the text
proves: [correctness]
status: full
---

We use the notation of the page. $T = T[0 \ldots n-1]$ is over $\Sigma$, $T' = T\$$ has length $N = n + 1$, and $\$$ occurs once and is smaller than each symbol of $\Sigma$. $R_i$ is the rotation of $T'$ that starts at index $i$, and $SA$ is the suffix array of $T'$. By the correctness proof of the [Burrows-Wheeler transform](/burrows-wheeler-transform/), the $N$ rotations are pairwise distinct, row $r$ of the sorted rotations is $R_{SA[r]}$, and $L[r] = T'[(SA[r] - 1) \bmod N]$. Also $F[r]$, the first symbol of row $r$, is $T'[SA[r]]$, and $F$ is $L$ in sorted order, because both columns hold each symbol of $T'$ once.

**Lemma 1 (the LF property).** Let $i < j$ be two rows with $L[i] = L[j] = c$. Let $i'$ and $j'$ be the rows of the rotations $c\,x$ and $c\,y$, where row $i$ is $x\,c$ and row $j$ is $y\,c$. Then $i' < j'$.

*Proof.* Row $i$ is $x c$ and row $j$ is $y c$, with $|x| = |y| = N - 1$. Since $i < j$ and the rows are sorted and distinct, $x c < y c$. If $x = y$, the two rows are equal, which is false; so $x \ne y$, and since $|x| = |y|$, the first difference of $x c$ and $y c$ is inside $x$ and $y$, so $x < y$. Then $c x$ and $c y$ agree on the first symbol and compare like $x$ and $y$, so $c x < c y$, that is $i' < j'$. $\square$

**Lemma 2 (LF is computed by counting).** For each row $i$, let $c = L[i]$ and $k = \mathrm{rank}_c(L, i)$, the number of occurrences of $c$ in $L[0 \ldots i-1]$. Then the row of the rotation $c\,x$ (where row $i$ is $x\,c$) is $C[c] + k$, where $C[c]$ is the number of symbols of $L$ smaller than $c$.

*Proof.* The rotations that start with $c$ are exactly the rotations $c\,x$ obtained from the rows $x\,c$ that end with $c$: the map from a rotation $x c$ to the rotation $c x$ is the move of the start index one to the left, a bijection of the $N$ rotations. So the number of rows that start with $c$ equals the number of rows that end with $c$, call it $m$. Since the rows are sorted, the rows that start with a symbol smaller than $c$ come first, and there are $C[c]$ of them (the multiset of first symbols equals the multiset of $L$). So the rows that start with $c$ are rows $C[c], \ldots, C[c] + m - 1$. By Lemma 1, the map from the rows that end with $c$ to the rows that start with $c$ keeps the order. An order-keeping bijection between two sorted lists of $m$ elements maps the $k$-th element to the $k$-th element (counting from 0). Row $i$ is the $k$-th row that ends with $c$, so its image is row $C[c] + k$. $\square$

**Corollary (one position to the left).** $SA[\mathrm{LF}(i)] = (SA[i] - 1) \bmod N$ for each row $i$.

*Proof.* If row $i$ is $R_p$, then $R_p = x\,c$ with $c = T'[(p - 1) \bmod N]$, and $c\,x = R_{(p-1) \bmod N}$. By Lemma 2 its row is $\mathrm{LF}(i)$. $\square$

**Lemma 3 (lines L1 to L6 compute LF).** After line L2, $C[c]$ is the number of symbols of $L$ smaller than $c$. When the loop of line L4 reaches row $i$, $seen[c] = \mathrm{rank}_c(L, i)$ for each $c$, so line L5 sets $\mathrm{LF}[i] = C[L[i]] + \mathrm{rank}_{L[i]}(L, i)$.

*Proof.* Line L1 counts each symbol, and line L2 sums the counts of the smaller symbols. For $seen$: before row $0$, all values are $0 = \mathrm{rank}_c(L, 0)$. Line L6 adds one to $seen[L[i]]$ only, after line L5 reads it, and $\mathrm{rank}_c(L, i+1) = \mathrm{rank}_c(L, i) + [L[i] = c]$. Induction on $i$ gives the claim. $\square$

**Theorem (the walk outputs $T$).** Lines L7 to L11 return $T$.

*Proof.* Row 0 is the smallest rotation. The rotation $R_n = \$T$ starts with $\$$, the smallest symbol, which occurs once, so each other rotation starts with a larger symbol and $R_n$ is row 0, that is $SA[0] = n$.

Invariant: at the start of the step of line L8 with index $j$ (for $j = n - 1$ down to $0$), $SA[r] = j + 1$.

*Start.* For $j = n - 1$, line L7 set $r = 0$, and $SA[0] = n = j + 1$.

*Step.* If $SA[r] = j + 1$, then line L9 writes $L[r] = T'[(j + 1) - 1] = T'[j] = T[j]$, since $0 \le j \le n - 1$. Line L10 sets $r$ to $\mathrm{LF}(r)$, and by the corollary $SA[\mathrm{LF}(r)] = j$, which is $(j - 1) + 1$, the invariant for the next index $j - 1$.

*End.* The loop runs for each $j$ from $n - 1$ to $0$ once, so each $T[j]$ is written once with the right symbol, and the loop ends after $n$ steps. The returned string is $T$. $\blacksquare$

**Remark (the convention without a sentinel).** If the input is the last column of the sorted rotations of $T$ itself and a row $I$ with $R_I = T$, the same argument holds with $N = n$, with the walk started at $r = I$ and the invariant $SA[r] \equiv j + 1 \pmod n$. When $T$ is a power $u^k$ with $k \ge 2$, some rows are equal strings, and we track strings, not start indices. The argument of Lemma 2 still shows that the sorted list of the strings $c x$ is the image of the sorted list of the strings $x c$ position by position, so if row $i$ holds the string $x c$, row $\mathrm{LF}(i)$ holds the string $c x$. Then the invariant "row $r$ holds the rotation of $T$ by $j + 1$ positions" holds as before, and the output is again $T$.
