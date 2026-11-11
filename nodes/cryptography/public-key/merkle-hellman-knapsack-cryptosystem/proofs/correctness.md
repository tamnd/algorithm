---
title: "Merkle-Hellman decryption inverts encryption, and the low density lattice attack reads the message from the public key alone"
proves: [correctness]
status: full
---

Throughout, $n \ge 1$, the private key is a superincreasing sequence $a_1, \ldots, a_n$ of positive integers, a modulus $m > A := \sum_{i=1}^n a_i$, a multiplier $w$ with $\gcd(w, m) = 1$, and a permutation $\pi$ of $\{1, \ldots, n\}$. *Superincreasing* means

$$a_i > \sum_{j < i} a_j \qquad \text{for } i = 1, \ldots, n .$$

The public key is $b_j = w a_{\pi(j)} \bmod m$, encryption of $x \in \{0,1\}^n$ is $c = \sum_j x_j b_j$ computed over the integers, and decryption is lines 8 to 10 of the main block.

## Part 1. The greedy pass

**Lemma 1 (uniqueness of the subset).** For a superincreasing sequence, the map $y \mapsto \sum_i y_i a_i$ from $\{0,1\}^n$ to the integers is injective.

*Proof.* Let $y \ne z$ in $\{0,1\}^n$ and let $k$ be the largest index where they differ; say $y_k = 1$ and $z_k = 0$. Then

$$\sum_i y_i a_i - \sum_i z_i a_i = a_k + \sum_{i < k} (y_i - z_i) a_i \ge a_k - \sum_{i<k} a_i > 0$$

by the superincreasing property, so the two sums differ. $\square$

**Theorem 2 (the greedy pass is correct).** Let $s$ be an integer. The block SOLVE-SUPERINCREASING returns a vector $y$ with $\sum_i y_i a_i = s$ if such a vector exists, and ERROR otherwise.

*Proof.* Write $s_i$ for the value of the variable $s$ when the loop reaches index $i$, so $s_n = s$. We prove by downward induction on $i$ the following invariant: if some $y \in \{0,1\}^n$ with $\sum y_j a_j = s$ exists, then after the step for index $i$ the digits $y_i, \ldots, y_n$ chosen by the algorithm agree with every such $y$, and $s_{i-1} = s - \sum_{j \ge i} y_j a_j$.

For the step at index $i$, assume the invariant above index $i$, so $s_i = \sum_{j \le i} y_j a_j$ for any solution $y$. Two cases.

- If $a_i \le s_i$, then $y_i = 1$ for every solution. Indeed $y_i = 0$ would give $s_i = \sum_{j < i} y_j a_j \le \sum_{j<i} a_j < a_i \le s_i$, a contradiction. The algorithm sets $y_i = 1$ and subtracts, which keeps the invariant.
- If $a_i > s_i$, then $y_i = 0$ for every solution, because $y_i = 1$ would give $s_i \ge a_i$. The algorithm sets $y_i = 0$ and does not change $s$.

After index 1 the invariant says $s_0 = s - \sum_j y_j a_j = 0$ for the chosen $y$ whenever a solution exists, so line 4 passes and line 5 returns it. If no solution exists then the chosen $y$ is some vector with $\sum_j y_j a_j \le s$, and $s_0 = 0$ would make it a solution; so $s_0 \ne 0$ and line 4 returns ERROR. By Lemma 1 the solution, when it exists, is unique, so "every such $y$" is one vector. $\blacksquare$

The cost is $n$ comparisons and at most $n$ subtractions of integers of $O(n)$ binary digits, so $\Theta(n^2)$ binary digit operations.

## Part 2. Decryption inverts encryption

**Lemma 3 (no wrap around).** For every $y \in \{0,1\}^n$, $\sum_i y_i a_i \le A < m$.

*Proof.* The digits are 0 or 1 and the terms are positive, so the sum is at most $A$, and $m > A$ by the choice of the modulus. $\square$

**Theorem 4 (correctness).** For every $x \in \{0,1\}^n$, MH-DECRYPT$((a, m, w, \pi), \text{MH-ENCRYPT}(b, x)) = x$.

*Proof.* Let $c = \sum_j x_j b_j$ and define $y$ by $y_{\pi(j)} = x_j$, that is, $y$ is the message written in the private order. Each public term satisfies $b_j \equiv w a_{\pi(j)} \pmod m$, so

$$c \equiv \sum_j x_j \, w\, a_{\pi(j)} = w \sum_i y_i a_i \pmod m .$$

Multiplying by $w^{-1} \bmod m$, which exists because $\gcd(w, m) = 1$, line 8 computes

$$s = w^{-1} c \bmod m = \left(\sum_i y_i a_i\right) \bmod m = \sum_i y_i a_i ,$$

where the last step is Lemma 3: the integer is already in the range $[0, m)$, so reducing modulo $m$ leaves it unchanged. This is the point of the condition $m > A$. By Theorem 2 and Lemma 1, line 9 returns exactly $y$, and line 10 undoes the permutation, giving $x_j = y_{\pi(j)}$ back. $\blacksquare$

**Remark 5 (determinism and malleability).** Theorem 4 has no failure probability and uses no randomness, so the scheme is deterministic. The same linear structure that makes the proof short also makes the scheme malleable: for messages $x$ and $x'$ with disjoint supports, $c + c'$ is the ciphertext of $x \lor x'$, and $c - b_j$ is the ciphertext of $x$ with digit $j$ cleared whenever $x_j = 1$. Both facts follow from the definition of encryption as an integer sum.

**Remark 6 (the modulus must exceed the total).** If $m \le A$ the proof of Theorem 4 breaks at Lemma 3 and the scheme is simply wrong: $s$ is then $\sum y_i a_i - km$ for some $k \ge 1$, and the greedy pass either fails or returns a different vector. This is a correctness bug and not a weakness that could be traded for security.

## Part 3. The density of the public key

**Lemma 7.** $a_n \ge 2^{n-1}$, hence $m > 2^{n-1}$ and $\log_2 \max_j b_j$ is at least about $n$ for keys whose public terms fill the range $[0, m)$.

*Proof.* By induction: $a_1 \ge 1$, and $a_i > \sum_{j<i} a_j \ge a_{i-1} \cdot 1$ gives $\sum_{j \le i} a_j > 2 \sum_{j<i} a_j$, so the partial sums at least double and $\sum_{j \le n} a_j \ge 2^{n-1}$. $\square$

**Definition 8.** The density of a subset sum instance $(b_1, \ldots, b_n)$ is $d = n / \log_2 \max_j b_j$.

**Proposition 9.** With the generator of the implementation, where $a_i$ is the running total plus a uniform gap in $[1, 2^n]$, the density of the public key is $1/2 + O(1/n)$.

*Proof sketch.* Write $T_i = \sum_{j \le i} a_j$. Then $T_i = 2T_{i-1} + g_i$ with $g_i$ uniform in $[1, 2^n]$, so $T_n = \sum_i 2^{n-i} g_i$, which lies between $2^{n-1}$ and $2^{n+1} \cdot 2^n$. Hence $\log_2 T_n = 2n + O(1)$, the modulus $m \in (T_n, 2T_n]$ has the same number of binary digits up to one, and the public terms are spread over $[0, m)$ so that the largest is $2^{2n + O(1)}$. Therefore $d = n/(2n + O(1)) = 1/2 + O(1/n)$. $\square$

The measured densities in the test file are 0.5344 for $n = 8$, 0.512 for $n = 16$ and 0.4968 for $n = 24$, which match the statement.

## Part 4. The lattice attack

Fix a public key $b$ and a ciphertext $c = \sum_j x_j b_j$ with the message $x \in \{0,1\}^n$ unknown. Let $K$ be a positive integer and let $L \subset \mathbb{Z}^{n+1}$ be the lattice generated by the rows

$$v_i = (e_i, K b_i) \ \ (i = 1, \ldots, n), \qquad v_{n+1} = (0, \ldots, 0, K c) ,$$

where $e_i$ is the $i$-th standard vector of $\mathbb{Z}^n$. These $n+1$ rows are independent, since the matrix is lower triangular with nonzero diagonal after the obvious column order.

**Lemma 10 (the message is in the lattice and it is short).** The vector $t = (x, 0) = \sum_i x_i v_i - v_{n+1}$ belongs to $L$, and $\lVert t \rVert \le \sqrt{n}$.

*Proof.* The combination is integral, and its last coordinate is $K \sum_i x_i b_i - K c = 0$ by the definition of $c$. The first $n$ coordinates are the digits of $x$, so the squared length is the number of ones in $x$, at most $n$. $\square$

**Lemma 11 (soundness of the test).** If a vector $r \in L$ has last coordinate 0 and all first $n$ coordinates in $\{0, 1\}$, and if $\sum_i r_i b_i = c$, then $r$ restricted to its first $n$ coordinates is a message that encrypts to $c$.

*Proof.* Immediate from the definition of encryption. The test of line 5 of the attack block checks exactly these conditions, and it checks $\pm r$ because the lattice is symmetric and LLL may return the negative. $\square$

So the attack never returns a wrong answer; when it answers, the answer is a valid plaintext. If the public sequence happens to have two subsets with the same sum, the attack may return the other one, and then it has found a second preimage, which is as good for an attacker. For a key of this scheme no second preimage exists, by Lemma 1 applied after the disguise is removed.

**Theorem 12 (Lagarias and Odlyzko 1985, stated).** There is a polynomial time algorithm that, given $n$ and a subset sum instance $(b, c)$ with a solution in $\{0,1\}^n$, solves it for all but a fraction $O(2^{-c_0 n})$ of the instances with $b_i$ drawn uniformly from $[1, M]$ and density $d = n/\log_2 M$ below $0.6463$. The algorithm makes one call to a lattice reduction that finds a shortest vector, or in the practical form one call to LLL.

We use the theorem as stated; the proof is in Sections 1 and 2 of the paper. The counting idea behind it is the following.

**Proposition 13 (why low density works).** Let $r \in L$ have last coordinate 0 and $\lVert r \rVert \le \sqrt n$. Then $r = (z, 0)$ with $z \in \mathbb{Z}^n$, $\lVert z \rVert \le \sqrt n$ and $\sum_i z_i b_i = \lambda c$ for the integer $\lambda = -r_{n+1}$ coefficient of $v_{n+1}$ in the expansion of $r$. The number of integer vectors $z$ with $\lVert z \rVert \le \sqrt{n}$ is at most $(2\sqrt{n}+1)^n = 2^{O(n \log n)}$, while the values $\sum_i z_i b_i$ are spread over a range of about $n 2^{n/d} M$. For $d$ small enough, the expected number of such $z$ that accidentally produce a multiple of $c$ is below 1, so the only short vectors of $L$ with a zero last coordinate are the integer multiples of $t$ and the vectors $\pm t$ themselves. A basis reduction that returns vectors within a factor $2^{(n-1)/2}$ of the shortest then has $t$ among its rows for the densities the paper identifies. $\square$

**Remark 14 (the role of $K$).** The multiplier $K$ penalizes a nonzero last coordinate: a lattice vector with last coordinate $\ne 0$ has length at least $K$. Taking $K > \sqrt{n}/2$, as line 1 of the attack block does, makes every vector shorter than $t$ have last coordinate 0, which is what Proposition 13 assumes. The implementation uses $K = \lfloor \sqrt n \rfloor + 1$.

**Corollary 15 (Merkle-Hellman is broken by Theorem 12).** By Proposition 9 the density of a Merkle-Hellman public key is near $1/2 < 0.6463$, so Theorem 12 applies to almost every key the generator produces, and the message follows from the public key and the ciphertext with one basis reduction and no knowledge of $(a, m, w, \pi)$.

The test file is the experiment: for three independent keys with $n = 20$ it recovers the exact message vector, and it also recovers the message of the six term example of the page, whose density is 0.899 and which is small enough that LLL finds the vector anyway.

**Remark 16 (CJLOSS).** Replacing $e_i$ by $2e_i$ and the last row by $(1, 1, \ldots, 1, 2Kc)$ makes the target vector $2x - (1, \ldots, 1)$, whose entries are $\pm 1$ and whose length is $\sqrt n$ but which sits in a lattice of twice the determinant. The gain in the counting argument raises the density bound to 0.9408. This variant is not needed for Merkle-Hellman keys and is not implemented here.

**Remark 17 (Shamir's attack, for contrast).** Shamir's 1982 attack recovers the private key instead of a message. The quantity $w^{-1}/m$ is a real number in $(0,1)$ for which the products $b_j w^{-1}/m \bmod 1$ are the small private terms divided by $m$, so they lie in short intervals near 0 for the public positions that hold $a_1, a_2, \ldots$. Guessing which few public positions those are, the conditions become a system of linear inequalities in a fixed number of unknowns with integer variables, which Lenstra's integer programming algorithm solves in polynomial time for fixed dimension. The two attacks are independent: Shamir's uses the structure of the trapdoor, the lattice attack uses only the density.
