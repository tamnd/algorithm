---
title: Source IP hash is a function of the address prefix, marking a server down moves only its clients, and the shares follow the weights
proves: [correctness]
status: full
---

We use the pseudocode of the page. The servers $S_1, \ldots, S_n$ have positive integer weights $w_1, \ldots, w_n$ with sum $W$. Server $S_i$ *owns* the residues $r$ with $w_1 + \cdots + w_{i-1} \le r < w_1 + \cdots + w_i$, and $\sigma(h)$ is the owner of $h \bmod W$. For a key $a$ (three bytes of an IPv4 address or sixteen bytes of an IPv6 address), let $g_a(h)$ be the result of line L4 on $h$: the loop $h \leftarrow (113 h + b) \bmod 6271$ over the bytes $b$ of $a$. Define the *probe sequence* $h_1 = g_a(89)$ and $h_{j+1} = g_a(h_j)$. Let $D$ be the set of servers that are down.

**Lemma 1 (what the loop returns).** IP-HASH returns $\sigma(h_j)$ for the smallest $j \le 21$ with $\sigma(h_j) \notin D$, and it falls back if there is no such $j$.

*Proof.* Lines L6 and L7 compute $\sigma(h)$: they subtract the weights in order while the remainder is at least the current weight, so they stop at the first $i$ with $r < w_i$ for the reduced $r$, which is the server whose range holds the original $h \bmod W$. The loop of line L3 keeps the invariant that, at the start of pass $j$ (counting from 1), $h = h_{j-1}$ (with $h_0 = 89$), $tries = j - 1$, and $\sigma(h_1), \ldots, \sigma(h_{j-1})$ are all in $D$. Line L4 makes $h = h_j$. If $\sigma(h_j) \notin D$, line L8 returns it, and it is the first such probe by the invariant. Otherwise line L9 sets $tries = j$, and line L10 falls back when $j > 20$, that is after the probe $j = 21$. Else the invariant holds for pass $j + 1$. $\square$

The loop ends after at most 21 passes, because $tries$ grows by 1 in each pass that does not return.

**Lemma 2 (affinity).** The result depends only on the key $a$, the server list with its weights, and $D$. All IPv4 clients in one /24 prefix get the same server.

*Proof.* By Lemma 1 the result is a function of the probe sequence, $\sigma$ and $D$. The probe sequence depends only on $a$, and for IPv4 the key is the first three bytes, which are equal for all addresses of a /24 prefix. $\square$

**Theorem 3 (marking servers down moves only their clients).** Let $D \subseteq D'$, with the same server list and weights. If the client with key $a$ gets server $s$ under $D$, and $s \notin D'$, then it gets $s$ under $D'$.

*Proof.* Under $D$, $s = \sigma(h_j)$ for the smallest $j$ with $\sigma(h_j) \notin D$. For $i < j$, $\sigma(h_i) \in D \subseteq D'$. And $\sigma(h_j) = s \notin D'$. So $j$ is also the smallest index for $D'$, and $j \le 21$ as before. $\square$

With $D = \emptyset$ and $D' = \{s\}$, this says: marking one server down moves only the clients of that server. Its clients go to the first later probe that is up, which depends on the key, so they spread over the other servers. When the server comes back, Theorem 3 with the roles of the two sets read in the other direction shows that exactly those clients return. This is why the nginx documentation advises marking a server `down` instead of removing it from the list.

**Theorem 4 (removing a server from the list).** Assume all weights are 1, and that the first probe $h_1$ is uniform on a set of values that is a union of whole residue classes modulo $n(n-1)$. If one server is removed from the list and the others keep their order, a client keeps its server with probability $1/n$.

*Proof.* With all weights 1, the server is $S_{(h_1 \bmod n) + 1}$ before and the $((h_1 \bmod (n-1)) + 1)$-th server of the shorter list after. A client keeps its server exactly when the pair $(h_1 \bmod n, h_1 \bmod (n-1))$ is one of the $n - 1$ pairs (old index of $t$, new index of $t$) for a surviving server $t$. Since $n$ and $n - 1$ are coprime, the Chinese remainder theorem makes $h_1 \bmod n(n-1)$ determine the pair one to one, so each of the $n(n-1)$ pairs has probability $1/(n(n-1))$. The probability to stay is $(n-1)/(n(n-1)) = 1/n$. $\square$

The range $\{0, \ldots, 6270\}$ is not a union of whole classes, so for nginx the statement holds up to an error of order $n^2/6271$.

**Theorem 5 (weighted shares).** Among the 6,271 values of $h$, server $S_i$ owns between $w_i \lfloor 6271 / W \rfloor$ and $w_i \lceil 6271 / W \rceil$. So if $h_1$ is uniform on $\{0, \ldots, 6270\}$ and no server is down, the share of $S_i$ is within $w_i / 6271$ of $w_i / W$.

*Proof.* A residue $r \in \{0, \ldots, W - 1\}$ is hit by $\lfloor 6271 / W \rfloor$ or $\lceil 6271 / W \rceil$ values of $h$, and $S_i$ owns $w_i$ residues. The share is then between $w_i \lfloor 6271/W \rfloor / 6271 \ge w_i / W - w_i / 6271$ and $w_i \lceil 6271/W \rceil / 6271 \le w_i / W + w_i / 6271$. $\square$

**What the theorems do not cover.** They count client addresses, not requests. If one address carries much of the traffic, for example a large network behind one NAT address, its server gets that traffic whatever the hash does. The uniformity of $h_1$ is an assumption about the set of client addresses; the hash is a fixed function with only 6,271 values.
