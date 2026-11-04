---
tag: 4GG39A
kind: theorem
slug: linear-probing-analysis
name: Analysis of linear probing
aliases:
- Knuth's linear probing analysis
area: data-structures/hashing
level: advanced
summary: Expected probes per search are about 1/2(1 + 1/(1-alpha)^2) for unsuccessful search; the derivation is due to Knuth.
prereqs: [linear-probing, uniform-hashing-assumption]
see_also: [primary-clustering, open-addressing, yao-open-addressing-lower-bound, robin-hood-hashing, load-factor, k-wise-independent-hashing, tabulation-hashing]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.4, Hashing, the analysis of Algorithm L (the formulas for C_N and C'_N in terms of the functions Q_0 and Q_1, and their limits)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.4, Hash Tables, the statement of the average costs of linear probing
  - paper: doi:10.1137/0114101
    title: Alan G. Konheim and Benjamin Weiss, An occupancy discipline and applications, SIAM Journal on Applied Mathematics 14(6), 1966
    locator: pages 1266 to 1274
  - paper: doi:10.1137/070702278
    title: Anna Pagh, Rasmus Pagh and Milan Ružić, Linear probing with constant independence, SIAM Journal on Computing 39(3), 2009
    locator: pages 1107 to 1120
  - paper: doi:10.1007/978-3-642-14165-2_60
    title: Mihai Pătraşcu and Mikkel Thorup, On the k-independence required by linear probing and minwise independence, ICALP 2010, LNCS 6198
    locator: pages 715 to 726
---

The analysis of linear probing gives the exact expected number of probes of a search in a [linear probing](/linear-probing/) hash table when the hash values are independent and uniform. At [load factor](/load-factor/) $\alpha$, a search that fails makes about $\frac{1}{2}\left(1 + 1/(1-\alpha)^2\right)$ probes and a search that succeeds about $\frac{1}{2}\left(1 + 1/(1-\alpha)\right)$. Knuth derived these formulas in 1963. They measure the cost of [primary clustering](/primary-clustering/): against the $1/(1-\alpha)$ of the [uniform hashing assumption](/uniform-hashing-assumption/), a failed search costs about $1/(2(1-\alpha))$ times more when the table is nearly full.

## Statement

**The model.** A table has $m$ slots $0, \ldots, m-1$, joined in a circle. Keys $x_1, \ldots, x_n$, with $n < m$, are inserted in this order by linear probing, with no deletions: key $x_i$ goes to the first empty slot of $h(x_i), h(x_i) + 1, \ldots$ (modulo $m$). The hash values $h(x_1), \ldots, h(x_n)$ are independent and uniform on $\{0, \ldots, m-1\}$, so all $m^n$ hash sequences are equally likely.

- $C'_{m,n}$ is the expected number of probes of a search for a key that is not in the table, whose hash value is uniform and independent of the others. The probes count each slot looked at, the final empty slot included.
- $C_{m,n}$ is the expected number of probes of a search for $x_i$, with $i$ uniform in $\{1, \ldots, n\}$, for $n \ge 1$.

For integers $a \ge 1$ and $0 \le b \le a$, let $f(a, b) = (a - b)\, a^{b-1}$. (So $f(a, 0) = 1$.)

**Theorem.**

(a) *Exact failed search.* For $0 \le n \le m - 2$,
$$C'_{m,n} = 1 + \frac{1}{m^n} \sum_{k=1}^{n} \binom{n}{k}\, (k+1)^{k-1}\, f(m-k-1,\ n-k)\, \frac{k(k+1)}{2},$$
and $C'_{m,m-1} = (m+1)/2$.

(b) *Successful search from failed search.* For $1 \le n \le m-1$,
$$C_{m,n} = \frac{1}{n} \sum_{i=0}^{n-1} C'_{m,i}.$$

(c) *Knuth's closed forms.* With $Q_r(m, n) = \sum_{k \ge 0} \binom{r+k}{k} \frac{n (n-1) \cdots (n-k+1)}{m^k}$,
$$C'_{m,n} = \frac{1}{2}\left(1 + Q_1(m, n)\right), \qquad C_{m,n} = \frac{1}{2}\left(1 + Q_0(m, n-1)\right).$$

(d) *The limits.* If $m \to \infty$ and $n/m \to \alpha$ with $0 \le \alpha < 1$, then
$$C'_{m,n} \to \frac{1}{2}\left(1 + \frac{1}{(1-\alpha)^2}\right), \qquad C_{m,n} \to \frac{1}{2}\left(1 + \frac{1}{1-\alpha}\right).$$

Parts (a), (b) and (d) are proved in full below; part (d) is proved from (c). Part (c) is Knuth's result, Section 6.4, and it is cited here, not proved.

## In plain words

Linear probing puts a colliding key into the next free slot, so the full slots form runs, and a search that starts anywhere inside a run must walk to its end. A long run is a bigger target for new keys than a short one, so long runs grow faster. The theorem counts this effect exactly.

When the table is half full, a search for a missing key looks at two and a half slots on average, and a search for a present key at one and a half. When the table is nine tenths full, a missing key costs about fifty slots, while an ideal scheme with no runs would cost ten. A present key costs only five and a half, because most keys were placed while the table was still emptier. So linear probing is fast up to a moderate fill and slow near a full table.

## Proof

The proof is in [the full proof](proofs/main.md). It has four steps.

1. **Rotation.** Adding 1 to every hash value turns the final table by one slot. So every slot is empty in the same number of the $m^n$ hash sequences. Each sequence leaves exactly $m - n$ empty slots, so a fixed slot is empty in exactly $(m-n)\, m^{n-1} = f(m, n)$ sequences.
2. **Splitting at empty slots.** A probe path never crosses a slot that is empty at the end. So if slots 0 and $k+1$ are empty and slots $1, \ldots, k$ are full, the $k$ keys with home in $\{1, \ldots, k\}$ fill exactly those slots, as in a circle of $k + 1$ slots that keeps one slot empty, and the other $n - k$ keys behave as in a circle of $m - k - 1$ slots that keeps one slot empty. This is a bijection, and with step 1 it gives $\binom{n}{k} f(k+1, k)\, f(m-k-1, n-k)$ such sequences.
3. **Cost from runs.** A failed search that starts in a maximal run of $k$ full slots, at the $t$-th slot from its end, costs $t + 1$ probes. So the total over all $m$ start slots is $m$ plus $k(k+1)/2$ for each run of length $k$. By rotation, the expected number of runs of length $k$ is $m$ times the probability of step 2. This gives (a).
4. **Search retraces insert.** A successful search for $x_i$ looks at the same slots as the insert of $x_i$, which was a failed search in the table of the first $i - 1$ keys. This gives (b). For (d), each term of $Q_r(m, n)$ tends to $\binom{r+k}{k}\alpha^k$ and is bounded by $\binom{r+k}{k}\beta^k$ for a fixed $\beta < 1$, so the sum tends to $\sum_k \binom{r+k}{k} \alpha^k = (1-\alpha)^{-(r+1)}$.

The table compares the exact values with the limits, from (c):

| $\alpha$ | $C'$, $m = 100$ | $C'$, $m = 10\,000$ | limit of $C'$ | $C$, $m = 100$ | $C$, $m = 10\,000$ | limit of $C$ |
|---|---|---|---|---|---|---|
| 0.5 | 2.395 | 2.499 | 2.5 | 1.463 | 1.500 | 1.5 |
| 0.75 | 6.703 | 8.471 | 8.5 | 2.266 | 2.497 | 2.5 |
| 0.9 | 19.699 | 49.210 | 50.5 | 3.747 | 5.451 | 5.5 |

Here $n = \alpha m$. The exact values are below the limits and approach them slowly near $\alpha = 1$, where runs are long compared with $m$. For a small case, $m = 5$ gives $C'_{5,n} = 1, \frac{6}{5}, \frac{38}{25}, \frac{257}{125}, 3$ for $n = 0, \ldots, 4$, and $C_{5,n} = 1, \frac{11}{10}, \frac{31}{25}, \frac{361}{250}$ for $n = 1, \ldots, 4$. For example $C_{5,3} = \frac{1}{3}\left(1 + \frac{6}{5} + \frac{38}{25}\right) = \frac{31}{25}$, as (b) says. These values agree with a count over all $5^n$ hash sequences.

## Consequences

- **Constant time at a constant load.** For $\alpha \le c < 1$, both costs are $O(1/(1-c)^2)$, so [linear probing](/linear-probing/) takes $\Theta(1)$ expected time per operation with truly random hash values. The limits are the numbers that guide the choice of the resize threshold in [rehashing](/rehashing/).
- **The price of clustering.** Under [uniform hashing](/uniform-hashing-assumption/), a failed search costs $1/(1-\alpha)$ and a successful one $\frac{1}{\alpha}\ln\frac{1}{1-\alpha}$. Linear probing is close to these at a low load and much worse at a high load. This is the reason for [quadratic probing](/quadratic-probing/), [double hashing](/double-hashing/) and [Robin Hood hashing](/robin-hood-hashing/).
- **Parking functions.** Step 1 with $a = k + 1$ and $b = k$ says that $(k+1)^{k-1}$ sequences of $k$ cars, each with a preferred space in a one-way street of $k$ spaces, let all cars park. These are the parking functions of Konheim and Weiss, and the rotation argument of step 1 is the standard proof of their number.
- **Deletions.** The backward-shift deletion of [linear probing](/linear-probing/) leaves a table in which each key can still be reached from its home over full slots. In such a table the set of full slots depends only on the multiset of home slots, so a failed search sees the same table as if the deleted key had never been inserted, and $C'$ still applies when the deleted keys are chosen without looking at the hash values. With [lazy deletion](/lazy-deletion/), the tombstones count as full slots, and the formulas do not apply directly.

## Tightness

Part (a) is an exact formula, so no better bound holds in this model. The limit in (d) shows that the $1/(1-\alpha)^2$ growth of a failed search is real, not an artefact of the proof.

The model needs full independence of the hash values, and this hypothesis cannot be dropped for free. Pagh, Pagh and Ružić proved that any 5-wise independent family gives $O(1)$ expected time per operation at a constant load below 1, and that a pairwise independent family can give expected time $\Omega(\log n)$. Pătraşcu and Thorup proved that 5 is the least degree of independence that works in general: some 4-wise independent families give expected time $\Omega(\log n)$. In the worst case over the keys, with a fixed hash function, all keys can share one home slot, and a failed search then costs $n + 1$ probes.

## History

Knuth found the analysis of linear probing in 1963, in notes titled "Notes on open addressing" that were not published at the time; the results and their proof are in Section 6.4 of The Art of Computer Programming, Volume 3, first published in 1973. Konheim and Weiss published an analysis of the same occupancy process in 1966, and counted the parking functions. The question of how much independence of the hash function the formulas need was settled by Pagh, Pagh and Ružić (STOC 2007) and by Pătraşcu and Thorup (ICALP 2010).

## References
