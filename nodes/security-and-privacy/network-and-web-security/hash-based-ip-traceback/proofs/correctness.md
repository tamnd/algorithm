---
title: Correctness of hash-based IP traceback
proves: [correctness]
status: full
---

**Setting.** $G$ is a graph whose nodes are the victim $v$ and the routers. The packet $x$ took the path $R_1, \ldots, R_n$ of routers, where $R_n$ is a neighbor of $v$ and $R_i$ is a neighbor of $R_{i+1}$ for $1 \le i < n$. Each router $r$ has a table $T_r$, a Bloom filter with $k$ functions, or an exact set in the oracle version. The attacker chooses $x$ and all other packets.

**Assumptions.** (A1) Each $R_i$ is not compromised and ran INSERT on $x$ in the table that TRACE asks. (A2) No router changed the fields that invariant(x) reads, so every router hashed the same input. (A3) In the oracle version, $T_r$ is the exact set of packets that $r$ forwarded.

**Lemma 1 (Bloom filters have no false negatives).** If INSERT$(T, x)$ ran on a table $T$, then QUERY$(T, x)$ returns true at any later time.

*Proof.* Lines L1 and L2 set the $k$ positions $h_{r,i}(\text{invariant}(x))$ to 1. No line sets a bit to 0, so they stay 1. Line L3 reads the same $k$ positions, because the functions and, by (A2), the input are the same, and returns true. $\square$

**Lemma 2 (the search).** A router $r$ is added to found by line L9 if and only if $r$ answers yes at line L8 and there is a sequence $v = u_0, u_1, \ldots, u_t = r$ of neighbors in which $u_1, \ldots, u_t$ all answer yes.

*Proof.* Only nodes in found, and $v$, enter the queue $Q$, and only routers that answered yes enter found. Each router enters seen once and is asked at most once (line L7), and a router's answer does not depend on who asks, so the order of the search does not matter. If $r$ is added, the chain of the nodes that added each other back to $v$ is such a sequence. Conversely, suppose such a sequence exists, and let $u_s$ be the first node of the sequence after $v$ that is not in found. Then $u_{s-1}$ is $v$ or in found, so it entered $Q$ and was removed at line L6. When it was removed, $u_s$ was either already in seen, which happens only when some node asked it, or $u_{s-1}$ asks it now. In both cases $u_s$ was asked once and answered yes, so it is in found, a contradiction. $\square$

**Theorem 1 (no false negatives).** Under (A1) and (A2), TRACE$(G, v, x)$ returns a set that contains $R_1, \ldots, R_n$.

*Proof.* By (A1) and Lemma 1, each $R_i$ answers yes. The sequence $v, R_n, R_{n-1}, \ldots, R_i$ is a sequence of neighbors in which every router answers yes. By Lemma 2, $R_i$ is in found. $\square$

**Theorem 2 (exact oracle).** Under (A1) to (A3), TRACE returns exactly $\{R_1, \ldots, R_n\}$.

*Proof.* By (A3), a router answers yes if and only if it forwarded $x$, that is, if and only if it is some $R_i$. So found is contained in $\{R_1, \ldots, R_n\}$, and Theorem 1 gives the other inclusion. $\square$

**Theorem 3 (one bit of a table).** Assume that the hash values of the inserted packets are independent and uniform on $\{0, \ldots, m - 1\}$. After $n$ packets other than $y$ were inserted into an empty table, a fixed position is 1 with probability $\beta = 1 - (1 - 1/m)^{kn}$.

*Proof.* The $n$ packets make $kn$ independent uniform writes. A fixed position is missed by one write with probability $1 - 1/m$, so it is missed by all of them with probability $(1 - 1/m)^{kn}$. $\square$

**Remark (the rate of a query).** QUERY$(T, y)$ returns true when all positions of $y$ are 1. If the bits were independent, the probability would be $\beta^k$ for $k$ distinct positions. This is the formula $(1 - (1 - 1/m)^{kn})^k$ of Snoeren et al. (Section 7.2) and of the code, and it is an approximation: the bits are not independent, and positions of $y$ may coincide. The test of the code checks the approximation by measurement, not by proof. None of Theorems 1 and 2 depends on it. $\blacksquare$
