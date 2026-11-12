---
title: What the minimum distance guarantees for error detection, error correction and erasure correction
proves: [statement]
status: full
---

**Statement.** Let $\Sigma$ be a finite alphabet and let $C \subseteq \Sigma^n$ be a code with at least two codewords and minimum distance $d$. A codeword $c$ is sent. The received word $y$ has some positions erased (their symbols are replaced by the mark $?$, and the receiver knows where they are) and some positions in error (their symbols are wrong, and the receiver does not know where they are).

1. **Detection.** If there are no erasures and $1 \le d(c, y) \le d - 1$, then $y \notin C$.
2. **Correction.** If there are no erasures and $d(c, y) \le t = \lfloor (d - 1)/2 \rfloor$, then $c$ is the only codeword within distance $t$ of $y$. So a decoder that returns the nearest codeword returns $c$.
3. **Erasures.** If $y$ has $e \le d - 1$ erasures and no errors, then $c$ is the only codeword that agrees with $y$ on all positions that are not erased.
4. **Errors and erasures.** Let $E$ be the set of the $e$ erased positions, and let $\tau$ be the number of errors outside $E$. If $2\tau + e < d$, then $c$ is the only codeword that differs from $y$ in at most $\lfloor (d - 1 - e)/2 \rfloor$ of the positions outside $E$.
5. **Correction and detection together.** Let $0 \le t' \le s$ with $t' + s < d$, and let a decoder return the codeword within distance $t'$ of $y$ if there is one, and report an error otherwise. With no erasures, if $1 \le d(c, y) \le s$, the decoder returns $c$ or reports an error; it returns $c$ when $d(c, y) \le t'$.
6. **Tightness.** None of the bounds can be raised for all codes: for the code $C$ itself there are a codeword and a pattern of $d$ errors that is not detected; a pattern of $d$ erasures, and, for each $\tau, e \ge 0$ with $2\tau + e \ge d$, a pattern of at most $\tau$ errors and $e$ erasures, such that no decoder at all recovers the sent codeword in every case.

**Setup.** For a set $E$ of positions, write $d_E(x, y)$ for the number of positions outside $E$ where $x$ and $y$ differ. It is the Hamming distance of the words with the positions of $E$ deleted, so it is a metric on those shorter words and satisfies the triangle inequality. For all $x, y$, $d(x, y) \le d_E(x, y) + |E|$, because at most $|E|$ of the differing positions lie in $E$.

**Proof.**

*Step 1 (part 4).* Let $c' \in C$ with $c' \ne c$. Since $d(c, c') \ge d$, we get $d_E(c, c') \ge d - e$. Let $r = \lfloor (d - 1 - e)/2 \rfloor$, so $2r \le d - 1 - e$. The number of errors is $d_E(c, y) = \tau$, and $2\tau + e < d$ gives $2\tau \le d - 1 - e$, so $\tau \le r$ because $\tau$ is an integer. So $c$ is within $d_E$-distance $r$ of $y$. Suppose $c'$ is too. By the triangle inequality, $d_E(c, c') \le d_E(c, y) + d_E(y, c') \le 2r \le d - 1 - e$, which contradicts $d_E(c, c') \ge d - e$. So $c$ is the only one.

*Step 2 (parts 2 and 3).* Part 2 is part 4 with $e = 0$, $E = \emptyset$ and $\tau = d(c, y)$: the condition $2\tau < d$ is $\tau \le \lfloor (d - 1)/2 \rfloor$. Part 3 is part 4 with $\tau = 0$: the condition is $e < d$, and a codeword at $d_E$-distance $0$ from $y$ agrees with $y$ outside $E$.

*Step 3 (part 1).* If $y$ were a codeword, then $y$ and $c$ would be two different codewords (since $d(c, y) \ge 1$) at distance at most $d - 1$, which contradicts the definition of $d$.

*Step 4 (part 5).* If $d(c, y) \le t'$, then $t' \le \lfloor (d - 1)/2 \rfloor$ (because $2t' \le t' + s \le d - 1$), so by part 2 the only codeword within distance $t'$ is $c$, and the decoder returns it. If $t' < d(c, y) \le s$, suppose that the decoder returns some $c'$, so $d(c', y) \le t'$. Then $c' \ne c$, and $d(c, c') \le d(c, y) + d(y, c') \le s + t' < d$, a contradiction. So it reports an error.

*Step 5 (part 6).* Choose two codewords $x \ne x'$ with $d(x, x') = d$, and let $D$ be the set of the $d$ positions where they differ.

- *Detection.* Send $x$ and let the channel change it into $x'$, a pattern of $d$ errors. The received word is a codeword, so it is not detected.
- *Erasures.* Send $x$ or $x'$ and erase the positions of $D$. The two received words are the same, so any decoder gives the same output on both and is wrong for one of them.
- *Errors and erasures.* Let $2\tau + e \ge d$. If $e \ge d$, erase all of $D$ and $e - d$ more positions (this needs $e \le n$); the argument above applies with no errors. Otherwise erase $e$ positions of $D$, and let $D'$ be the other $d - e$ positions. Split $D'$ into a part $P$ of $\lceil (d - e)/2 \rceil$ positions and a part $Q$ of $\lfloor (d - e)/2 \rfloor$ positions. Let $z$ agree with $x'$ on $P$, with $x$ on $Q$, with both outside $D$, and be erased on the rest of $D$. From $x$, $z$ has $|P| = \lceil (d - e)/2 \rceil$ errors; from $x'$, it has $|Q| \le |P|$ errors. Since $2\tau \ge d - e$ and $\tau$ is an integer, $\tau \ge \lceil (d - e)/2 \rceil$. So $z$ can come from $x$ and from $x'$ with at most $\tau$ errors and $e$ erasures, and any decoder is wrong for one of them. With $e = 0$ this shows that no decoder corrects all patterns of $\lfloor (d - 1)/2 \rfloor + 1 = \lceil d/2 \rceil$ errors.

This proves all six parts. $\blacksquare$
