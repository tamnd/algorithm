---
title: Landlord is k/(k - h + 1)-competitive for file caching
proves: [correctness]
status: full
---

**Theorem.** Let all sizes be positive integers, with $\mathrm{size}(f) \le h \le k$ for each requested file $f$. Let Landlord (LL) use a cache of size $k$, and let OPT be any offline algorithm with a cache of size $h$. If both caches start empty, then for each request sequence $\sigma$ and each choice of the reset in line L3,

$$(k - h + 1) \cdot \mathrm{LL}(\sigma) \le k \cdot \mathrm{OPT}(\sigma).$$

With $h = k$ this is $\mathrm{LL}(\sigma) \le k \cdot \mathrm{OPT}(\sigma)$.

**Serving.** First, Landlord serves each request and stops. A hit needs nothing. On a miss, each round of the loop of line L4 either evicts a file (line L5) or makes some credit $0$ (line L6), and the next round then evicts a file. The cache holds finitely many files, and if it becomes empty, $f$ fits because $\mathrm{size}(f) \le k$. So the loop stops and line L7 puts $f$ in the cache.

**Credits.** A credit is set to $\mathrm{cost}(f)$ in line L7, it can be raised to at most $\mathrm{cost}(f)$ in line L3, and line L6 never makes it negative, by the choice of $\Delta$. So $0 \le \mathrm{credit}[f] \le \mathrm{cost}(f)$ at all times. For a file outside the cache of LL we set $\mathrm{credit}[f] = 0$.

**Potential.** Write $\mathrm{LL}$ and $\mathrm{OPT}$ also for the sets of files in the two caches, and let

$$\Phi = (h - 1) \sum_{f \in \mathrm{LL}} \mathrm{credit}[f] + k \sum_{f \in \mathrm{OPT}} \bigl( \mathrm{cost}(f) - \mathrm{credit}[f] \bigr).$$

Both sums are at least $0$, so $\Phi \ge 0$, and $\Phi = 0$ at the start. For each request for $f$, we let OPT act first, and then LL. We show that each event satisfies

$$(k - h + 1) \cdot (\text{cost of LL in the event}) + \Delta\Phi \le k \cdot (\text{cost of OPT in the event}).$$

**(1) OPT evicts a file.** A term $k(\mathrm{cost}(g) - \mathrm{credit}[g]) \ge 0$ leaves the second sum. $\Delta\Phi \le 0$.

**(2) OPT fetches $f$.** A term $k(\mathrm{cost}(f) - \mathrm{credit}[f]) \le k \cdot \mathrm{cost}(f)$ enters the second sum, and OPT pays $\mathrm{cost}(f)$. $\Delta\Phi \le k \cdot \mathrm{cost}(f)$.

After these events, $f \in \mathrm{OPT}$.

**(3) LL has a hit and raises the credit of $f$ by $\epsilon \ge 0$.** Now $f$ is in both caches. The first sum rises by $(h-1)\epsilon$ and the second falls by $k\epsilon$. So $\Delta\Phi = -(k - h + 1)\epsilon \le 0$, and LL pays nothing.

**(4) LL charges rent $\Delta$ in line L6.** Each $g \in \mathrm{LL}$ loses $\Delta \cdot \mathrm{size}(g)$ of credit. The first sum falls by $(h - 1)\Delta \cdot S_{\mathrm{LL}}$, where $S_{\mathrm{LL}}$ is the total size in the cache of LL. The second sum rises by $k\Delta \cdot S_{\cap}$, where $S_\cap$ is the total size of the files in both caches. We bound both sizes.

- LL is in the loop of line L4, so $f$ does not fit: $S_{\mathrm{LL}} + \mathrm{size}(f) > k$. All sizes are integers, so $S_{\mathrm{LL}} \ge k - \mathrm{size}(f) + 1$.
- The file $f$ is in OPT but not in LL. The cache of OPT has total size at most $h$, so $S_\cap \le h - \mathrm{size}(f)$.

Write $s = \mathrm{size}(f) \ge 1$. Then

$$\Delta\Phi \le \Delta \bigl( -(h-1)(k - s + 1) + k(h - s) \bigr) = \Delta \bigl( (k - h + 1) - s(k - h + 1) \bigr) = -\Delta (k - h + 1)(s - 1) \le 0 .$$

LL pays nothing in this event.

**(5) LL evicts a file $g$ with $\mathrm{credit}[g] = 0$ in line L5.** The first sum loses a term $0$. If $g \in \mathrm{OPT}$, its term in the second sum is $k \cdot \mathrm{cost}(g)$ before and after, since its credit is $0$ in both cases. $\Delta\Phi = 0$.

**(6) LL fetches $f$ in line L7.** LL pays $\mathrm{cost}(f)$. The first sum rises by $(h-1)\mathrm{cost}(f)$. Since $f \in \mathrm{OPT}$, its term in the second sum goes from $k \cdot \mathrm{cost}(f)$ (credit $0$) to $0$. So $\Delta\Phi = -(k - h + 1)\mathrm{cost}(f)$, and $(k - h + 1)\mathrm{cost}(f) + \Delta\Phi = 0$.

**Sum.** Add the inequality over all events. The changes of $\Phi$ add up to $\Phi_{\mathrm{end}} - \Phi_0 = \Phi_{\mathrm{end}} \ge 0$. So

$$(k - h + 1)\,\mathrm{LL}(\sigma) \le (k - h + 1)\,\mathrm{LL}(\sigma) + \Phi_{\mathrm{end}} \le k \cdot \mathrm{OPT}(\sigma).$$

If the caches do not start empty, the same sum gives $(k-h+1)\,\mathrm{LL}(\sigma) \le k \cdot \mathrm{OPT}(\sigma) + \Phi_0$, with a constant $\Phi_0$ that depends only on the start. $\blacksquare$
