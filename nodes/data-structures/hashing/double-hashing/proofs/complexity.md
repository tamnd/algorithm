---
title: Expected probes of open addressing under uniform hashing
proves: [time.expected, time.worst]
status: full
---

**Worst case.** Each loop of the page runs at most $m$ times, by the proof of correctness, so each operation makes at most $m$ probes. For the lower bound, take $n \le m$ keys $k_1, \ldots, k_n$ with the same $h_1$ and the same $h_2$; for $h_1(k) = k \bmod m$ and $h_2(k) = 1 + (k \bmod (m-2))$ the keys $k_j = j \cdot m(m-2)$ work. They have the same probe sequence, so the insert of $k_j$ probes $j$ slots, and the last insert and each later search for $k_n$ probe $n$ slots. With $n = m$ this is $\Theta(m)$.

**Model for the expected case.** The uniform hashing assumption says that the probe sequence of each key is a uniformly random permutation of the $m$ slots, independent of the other keys. Assume a table with no DELETED slot that holds $n < m$ keys, so $\alpha = n/m < 1$, and that the keys were inserted without knowledge of the random sequences.

**Claim 1.** A search for a key that is not in the table makes at most $1/(1 - \alpha)$ probes in expectation.

*Proof.* Let $X$ be the number of probes. The search goes on after probe $i$ only if the first $i$ probed slots are all occupied. The probe sequence of the absent key is a uniform random permutation, independent of which $n$ slots are occupied. So for $i \ge 1$,

$$\Pr[X > i] = \frac{n}{m} \cdot \frac{n - 1}{m - 1} \cdots \frac{n - i + 1}{m - i + 1} \le \Big(\frac{n}{m}\Big)^{i} = \alpha^{i},$$

because $(n - j)/(m - j) \le n/m$ for $0 \le j < n \le m$. Hence $E[X] = \sum_{i \ge 0} \Pr[X > i] \le \sum_{i \ge 0} \alpha^i = 1/(1 - \alpha)$. $\square$

An insert of a new key makes the same probes as a search that fails, so it also makes at most $1/(1 - \alpha)$ probes in expectation.

**Claim 2.** With no deletions, a search for a key chosen uniformly from the $n$ keys of the table makes at most $\frac{1}{\alpha} \ln \frac{1}{1 - \alpha}$ probes in expectation.

*Proof.* A search for a key follows the same probes as its insert. With no deletions, the key inserted as the $(j + 1)$-st, for $0 \le j < n$, was inserted into a table with $j$ keys, so by Claim 1 its search makes at most $1/(1 - j/m) = m/(m - j)$ probes in expectation. Average over the $n$ keys:

$$\frac{1}{n} \sum_{j=0}^{n-1} \frac{m}{m - j} = \frac{m}{n} \sum_{t = m - n + 1}^{m} \frac{1}{t} \le \frac{1}{\alpha} \int_{m - n}^{m} \frac{dx}{x} = \frac{1}{\alpha} \ln \frac{m}{m - n} = \frac{1}{\alpha} \ln \frac{1}{1 - \alpha}.$$

The inequality holds because $1/t \le \int_{t-1}^{t} dx/x$ for each $t \ge 1$, as $1/x \ge 1/t$ on $[t - 1, t]$. $\blacksquare$

**How far double hashing is from the model.** Double hashing does not give a uniform random permutation: there are at most $m(m-1)$ sequences, one per pair $(h_1(k), h_2(k))$. The two claims are therefore exact only for the model. Guibas and Szemerédi (1978) and Lueker and Molodowitch (1993) proved that, with $h_1$ and $h_2$ ideal random functions, the expected number of probes of double hashing equals the uniform hashing value plus a term that tends to 0 as $m$ grows, for fixed $\alpha$ (below about 0.319 in the first paper, and for each $\alpha < 1$ in the second). Their proofs are long and are not repeated here.
