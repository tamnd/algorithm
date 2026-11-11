---
title: The 4-list tree outputs only solutions and finds L^4/2^(n+ℓ) of them on average
proves: [correctness]
status: full
---

Let $L_1, L_2, L_3, L_4$ be lists of $n$-bit values, each of size $L$, and $1 \le \ell \le n$. For an $n$-bit value $x$, $\mathrm{low}_\ell(x)$ is $x \bmod 2^\ell$. Note that $\mathrm{low}_\ell(x) = \mathrm{low}_\ell(y)$ if and only if $\mathrm{low}_\ell(x \oplus y) = 0$.

**Lemma 1 (the joins).** Line L2 makes exactly the set of triples $(x_1 \oplus x_2, i_1, i_2)$ with $x_1 = L_1[i_1]$, $x_2 = L_2[i_2]$ and $\mathrm{low}_\ell(x_1 \oplus x_2) = 0$, and line L3 the same for $L_3, L_4$.

*Proof.* The join puts each entry of $L_1$ in a table under the key $\mathrm{low}_\ell(x_1)$, then for each entry of $L_2$ visits exactly the entries of $L_1$ with the same key. So it visits each pair $(i_1, i_2)$ with $\mathrm{low}_\ell(x_1) = \mathrm{low}_\ell(x_2)$ exactly once, and no other pair. $\square$

**Lemma 2 (soundness).** Each tuple output at line L5 satisfies $L_1[i_1] \oplus L_2[i_2] \oplus L_3[i_3] \oplus L_4[i_4] = 0$.

*Proof.* By Lemma 1, $u = L_1[i_1] \oplus L_2[i_2]$ and $v = L_3[i_3] \oplus L_4[i_4]$. Line L4 requires $u = v$, so the XOR of the four values is $u \oplus v = 0$. $\square$

**Lemma 3 (what is found).** The output is exactly the set of index tuples $(i_1, i_2, i_3, i_4)$ such that the four values XOR to 0 and $\mathrm{low}_\ell(L_1[i_1] \oplus L_2[i_2]) = 0$.

*Proof.* Lemma 2 gives one direction, together with Lemma 1 for the second condition. Conversely, take such a tuple. By Lemma 1 the triple $(u, i_1, i_2)$ is in $L_{12}$. Since the four values XOR to 0, $v = L_3[i_3] \oplus L_4[i_4] = u$, so $\mathrm{low}_\ell(v) = 0$ and $(v, i_3, i_4)$ is in $L_{34}$. Line L4 pairs them since $u = v$, and line L5 outputs the tuple. $\square$

**Lemma 4 (expected output).** If all $4L$ values are independent and uniform on $\{0,1\}^n$, then $\mathbb{E}|L_{12}| = L^2/2^\ell$ and the expected number of outputs is $L^4/2^{n+\ell}$.

*Proof.* For a fixed pair $(i_1, i_2)$, $x_1 \oplus x_2$ is uniform, so its low $\ell$ bits are zero with probability $2^{-\ell}$. Summing over the $L^2$ pairs gives the first claim by linearity.

For a fixed tuple, write $a = x_1 \oplus x_2$ and $b = x_3 \oplus x_4$. These are independent and uniform. By Lemma 3, the tuple is output when $\mathrm{low}_\ell(a) = 0$ and $a = b$. The probability is $2^{-\ell} \cdot 2^{-n}$. Summing over the $L^4$ tuples gives $L^4/2^{n+\ell}$. $\square$

**Theorem.** WAGNER-4 outputs only index tuples whose values XOR to zero. With $L = 2^\ell$ and $\ell = \lceil n/3 \rceil$, on uniform random lists it outputs at least one expected solution, $2^{3\ell - n} \ge 1$, in expected time and memory $O(2^\ell) = O(2^{n/3})$, counting hash table operations as $O(1)$.

*Proof.* Soundness is Lemma 2. With $L = 2^\ell$, Lemma 4 gives $\mathbb{E}[\text{outputs}] = 2^{4\ell - n - \ell} = 2^{3\ell - n}$, and $3\ell \ge n$. The joins at lines L2 and L3 take $O(L + |L_{12}|)$ and $O(L + |L_{34}|)$ time, of expected size $O(2^\ell)$ by Lemma 4. The join at line L4 takes $O(|L_{12}| + |L_{34}| + \text{outputs})$, again $O(2^\ell)$ in expectation since $3\ell - n \le 2 \le \ell$ for $n \ge 3$. Memory is bounded by the sizes of the lists and tables. $\blacksquare$

**Remark (the tree for $k = 2^t$).** The same argument applies level by level. With $\ell = n/(1+t)$, each value at level $j$ is the XOR of $2^j$ inputs and is zero on its low $j\ell$ bits. At each level below the root, the join keeps a pair with probability $2^{-\ell}$, so lists of size $2^\ell$ keep expected size $2^\ell$. The root keeps a pair with probability $2^{-(n - (t-1)\ell)} = 2^{-2\ell}$, so the expected number of outputs is $2^{2\ell - 2\ell} = 1$. Soundness holds as in Lemma 2, by induction on the level. The expected sizes are exact at every level, by linearity over the tuples of leaves as in Lemma 4: a fixed tuple of $2^j$ leaves passes all the joins below level $j$ with probability $2^{-(2^j - 1)\ell}$. What is lost above the first level is independence: entries of one list share leaves, so the list sizes are less concentrated around their means. This is why the code and Wagner's paper check the success rate by experiment.
