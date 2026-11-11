---
title: EME-PKCS1-v1_5 decoding inverts the encoding, and every conforming answer keeps the true plaintext
proves: [correctness]
status: full
---

Let $N = pq$ be an RSA modulus with $k = \lceil \log_{256} N \rceil$ octets and $k \ge 11$, let $e$ and $d$ be the exponents with $\mathrm{RSADP}(\mathrm{RSAEP}(m)) = m$ for every $0 \le m < N$, and set

$$B = 2^{8(k-2)} .$$

Write $\mathrm{OS2IP}$ and $\mathrm{I2OSP}$ for the conversions of RFC 8017 Section 4, so that $\mathrm{OS2IP}(\mathrm{I2OSP}(x, k)) = x$ for every $0 \le x < 256^k$, and $\mathrm{EM}[i]$ for the octet at index $i$, counted from 0.

## Part 1: the encoding

**Lemma 1 (the shape of an encoded message).** Let $M$ have $\mathrm{mLen} \le k - 11$ octets and let $\mathrm{EM} = \texttt{0x00} \Vert \texttt{0x02} \Vert \mathrm{PS} \Vert \texttt{0x00} \Vert M$ be the output of line L3, with $\mathrm{PS}$ of $k - \mathrm{mLen} - 3$ nonzero octets. Then $\mathrm{EM}$ has $k$ octets, $\mathrm{PS}$ has at least 8 octets, and $m = \mathrm{OS2IP}(\mathrm{EM})$ satisfies

$$2B \le m < 3B .$$

*Proof.* The length is $2 + (k - \mathrm{mLen} - 3) + 1 + \mathrm{mLen} = k$. The length of $\mathrm{PS}$ is $k - \mathrm{mLen} - 3 \ge k - (k - 11) - 3 = 8$. For the bounds, $\mathrm{EM}[0] = 0$ and $\mathrm{EM}[1] = 2$, so

$$m = \sum_{i=0}^{k-1} \mathrm{EM}[i] \cdot 256^{\,k-1-i} = 2 \cdot 256^{\,k-2} + \sum_{i=2}^{k-1} \mathrm{EM}[i] \cdot 256^{\,k-1-i} .$$

The first term is $2B$. The rest is at least 0 and at most $\sum_{i=2}^{k-1} 255 \cdot 256^{k-1-i} = 256^{k-2} - 1 = B - 1$. So $2B \le m \le 3B - 1$. $\square$

**Corollary 2 (no overflow).** $m < 3B = 3 \cdot 256^{k-2} \le 256^{k-1} \le N$, because $3 \le 256$, and $256^{k-1} \le N$ by the definition of $k$. So $m$ is a valid message representative for RSAEP on line L6.

**Lemma 3 (the separator is found).** With $\mathrm{EM}$ as in Lemma 1, the least index $i > 1$ with $\mathrm{EM}[i] = \texttt{0x00}$ is $i = k - \mathrm{mLen} - 1$, and this index is at least 10.

*Proof.* The octets at the indices $2, \ldots, k - \mathrm{mLen} - 2$ are the octets of $\mathrm{PS}$, and each one is nonzero, so none of them is the least zero index. The octet at index $k - \mathrm{mLen} - 1$ is the separator $\texttt{0x00}$. So the least zero index above 1 is $i = k - \mathrm{mLen} - 1$. From $\mathrm{mLen} \le k - 11$ we get $i \ge k - (k - 11) - 1 = 10$. $\square$

**Theorem 4 (correctness of the scheme).** For every message $M$ of at most $k - 11$ octets and every padding string $\mathrm{PS}$ of nonzero octets that line L2 can draw, the decryption of lines L7 to L12 applied to the encryption of lines L4 to L6 returns $M$.

*Proof.* Line L4 gives $\mathrm{EM}$ as in Lemma 1, line L5 gives $m$ with $2B \le m < 3B \le N$ by Corollary 2, and line L6 outputs $C = \mathrm{I2OSP}(m^e \bmod N, k)$, which has $k$ octets. On decryption, line L7 passes, because $|C| = k$ and $k \ge 11$. Line L8 recovers $\mathrm{RSADP}(\mathrm{OS2IP}(C)) = m$ and $\mathrm{I2OSP}(m, k) = \mathrm{EM}$, since the conversions are inverse on the range $[0, 256^k)$. Line L9 passes, because $\mathrm{EM}[0] = \texttt{0x00}$ and $\mathrm{EM}[1] = \texttt{0x02}$. Line L10 finds $i = k - \mathrm{mLen} - 1$ and line L11 passes, both by Lemma 3. Line L12 returns the octets at the indices $i+1, \ldots, k-1$, which are the $\mathrm{mLen}$ octets of $M$. $\square$

The decoding is a left inverse only. It is not injective on all of $\{0, 1\}^{8k}$: many encoded messages give the same $M$, which is what makes the scheme randomized.

## Part 2: the attack keeps the true plaintext

Fix a ciphertext with the representative $c_0 = m^e \bmod N$ for the unknown $m$, and let the oracle answer "yes" to a query $c$ exactly when $\mathrm{I2OSP}(\mathrm{RSADP}(c), k)$ starts with $\texttt{0x00}\,\texttt{0x02}$. Call $s$ *conforming* when the oracle says yes to $c_0 \cdot s^e \bmod N$.

**Lemma 5 (what one answer says).** $s \ge 1$ is conforming if and only if there is an integer $r \ge 0$ with

$$2B \le ms - rN \le 3B - 1 .$$

*Proof.* The query decrypts to $u = (ms) \bmod N$, because $(c_0 s^e)^d \equiv m s \pmod N$. By Lemma 1 applied in reverse, the octet string $\mathrm{I2OSP}(u, k)$ starts with $\texttt{0x00}\,\texttt{0x02}$ if and only if $2B \le u \le 3B - 1$. Writing $u = ms - rN$ with $r = \lfloor ms/N \rfloor \ge 0$ gives the claim. $\square$

**Lemma 6 (the narrowing step is sound).** Let $a \le m \le b$ and let $s$ be conforming. Then there is an integer $r$ with

$$\left\lceil \frac{as - 3B + 1}{N} \right\rceil \le r \le \left\lfloor \frac{bs - 2B}{N} \right\rfloor
\qquad \text{and} \qquad
\left\lceil \frac{2B + rN}{s} \right\rceil \le m \le \left\lfloor \frac{3B - 1 + rN}{s} \right\rfloor .$$

*Proof.* Take the $r$ of Lemma 5. From $2B \le ms - rN$ and $m \le b$ we get $rN \le ms - 2B \le bs - 2B$, so $r \le \lfloor (bs - 2B)/N \rfloor$ because $r$ is an integer. From $ms - rN \le 3B - 1$ and $m \ge a$ we get $rN \ge ms - 3B + 1 \ge as - 3B + 1$, so $r \ge \lceil (as - 3B + 1)/N \rceil$. The same two inequalities, read as bounds on $m$, give $ms \ge 2B + rN$ and $ms \le 3B - 1 + rN$, and $m$ is an integer, so the stated floor and ceiling bound it. $\square$

**Theorem 7 (the invariant).** If $m$ lies in the range set $\mathcal{M}$ before a call of NARROW with a conforming $s$, then $m$ lies in the range set that NARROW returns.

*Proof.* Let $[a, b] \in \mathcal{M}$ be a range with $a \le m \le b$. By Lemma 6 there is an $r$ in the loop range of NARROW for which the new bounds hold, so the range $[\max(a, \lceil (2B + rN)/s \rceil), \min(b, \lfloor (3B - 1 + rN)/s \rfloor)]$ contains $m$; in particular it is not empty, so NARROW adds it. The union of the added ranges therefore contains $m$. $\square$

The first call uses $\mathcal{M} = \{[2B, 3B-1]\}$, which contains $m$ by Lemma 1, because the ciphertext under attack is the encryption of a correctly encoded message. So by induction the true $m$ is in the range set at every step, and when one value is left, that value is $m$. This is the correctness of the attack; its output is $\mathrm{I2OSP}(m, k)$, which is $\mathrm{EM}$.

**Progress.** In step 2c the algorithm takes $r \ge 2(bs - 2B)/N$ and a new $s' \ge (2B + rN)/b$, so

$$s' \ge \frac{2B + 2(bs - 2B)}{b} = 2s - \frac{2B}{b} \ge 2s - 1 ,$$

because $b \ge 2B$. Every round of step 2c therefore at least doubles $s$, and by Lemma 6 the width of the one range that is left after NARROW is at most $(B-1)/s' + 1$. So the width falls by a factor near 2 in each round, and after $O(\log_2 N)$ rounds it is 1. This bounds the number of rounds, not the number of queries inside a round: the count of queries is a probabilistic claim of Bleichenbacher's Section 4, under the heuristic that $ms \bmod N$ is close to uniform, and it is about $N/B$ queries for step 2a and a small constant for each later round.
