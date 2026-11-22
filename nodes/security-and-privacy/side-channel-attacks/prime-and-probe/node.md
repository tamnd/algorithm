---
tag: QNB0J5
kind: technique
slug: prime-and-probe
name: Prime+Probe
aliases:
- prime and probe attack
area: security-and-privacy/side-channel-attacks
level: core
summary: A cache side channel in which an observer that shares no memory with a victim learns which cache sets the victim used, through contention for the ways of each set.
prereqs: [timing-attack, set-associative-cache]
see_also: [flush-and-reload, constant-time-programming, cache-replacement-policy, advanced-encryption-standard, side-channel-attack, spectre-attack, covert-channel, software-fault-isolation]
sources:
  - paper: "Dag Arne Osvik, Adi Shamir and Eran Tromer, Cache attacks and countermeasures, the case of AES, CT-RSA 2006, LNCS 3860, pages 1 to 20"
    locator: the definition of Prime+Probe and Evict+Time, the attacks on AES table lookups, and the section on countermeasures
  - paper: "Fangfei Liu, Yuval Yarom, Qian Ge, Gernot Heiser and Ruby B. Lee, Last-level cache side-channel attacks are practical, IEEE Symposium on Security and Privacy 2015, pages 605-622"
    locator: the Prime+Probe channel on the last-level cache across cores and virtual machines without shared memory, and the attacks on GnuPG exponentiation
  - url: "http://www.daemonology.net/papers/cachemissing.pdf"
    title: Colin Percival, Cache missing for fun and profit, BSDCan 2005
    locator: the cache channel between two hardware threads of one core, and the RSA exponent windows that it exposed
  - paper: doi:10.1109/MICRO.2018.00068
    title: "Moinuddin K. Qureshi, CEASER, mitigating conflict-based cache attacks via encrypted-address and remapping, MICRO 2018, pages 775-787"
    locator: the encrypted mapping of line addresses to sets and the periodic remapping
  - paper: "Mario Werner, Thomas Unterluggauer, Lukas Giner, Michael Schwarz, Daniel Gruss and Stefan Mangard, ScatterCache, thwarting cache attacks via cache set randomization, 28th USENIX Security Symposium, 2019, pages 675-692"
    locator: the index function that depends on the security domain and on the way, and its security analysis
  - url: "https://cr.yp.to/antiforgery/cachetiming-20050414.pdf"
    title: Daniel J. Bernstein, Cache-timing attacks on AES, 2005
    locator: the leak of AES table lookups through the cache, and the case for code without secret table indices
---

Prime+Probe is a cache side channel in which an observer learns which cache sets a victim used during an interval. The observer fills a set with his own lines, lets the victim run and then finds out whether the victim pushed any of them out. It needs no shared memory, only a shared cache, so it works where [Flush+Reload](/flush-and-reload/) does not. Osvik, Shamir and Tromer (2006) named it in their attacks on AES tables, and Liu et al. (2015) made it work on the last-level cache across virtual machines. The defenses are code whose memory addresses do not depend on secrets, caches that are partitioned between trust domains, and caches with a randomized mapping of lines to sets.

## In plain words

A shared parking lot has rows, and each row holds a few cars. You fill one row with your own cars and walk away. When you come back, one of your cars was towed to make space. Then someone else parked in that row while you were away.

A cache is that parking lot. Each memory line can only go in one row, called a set. The observer fills sets with his own data. If the victim uses data that goes in the same set, the cache throws out one of the observer's lines. The observer cannot see what the victim read, only in which set it was. If the set depends on the key, that is enough to learn about the key.

## When it applies

### Threat model

The observer is an unprivileged program that runs on the same machine as the victim, at the same time or between the victim's steps. He shares no memory with the victim. He sees only the effect of the cache on his own accesses, a hit or a miss on each of his own lines. The guarantees of the defenses below hold against this observer.

### Conditions

1. **A shared cache.** The observer and the victim use the same cache level, for example the private caches of one core with two hardware threads, or a last-level cache that all cores share.
2. **Control of the mapping.** The observer can place his own lines into a chosen set, that is, he can find lines that map to the same set as the victim's line. In a [set-associative cache](/set-associative-cache/) with a fixed mapping from addresses to sets, this is a question about the address bits.
3. **Contention.** A line of the victim in a full set evicts a line of the observer. This follows from the [replacement policy](/cache-replacement-policy/), for example LRU.
4. **A visible difference.** The observer can tell a hit from a miss on his own lines.
5. **A secret-dependent set.** The set that the victim uses depends on a secret, for example through a table lookup at a secret index.

### What removes a condition

| defense | condition it removes | cost |
|---|---|---|
| [constant-time code](/constant-time-programming/) | 5 | more work in the routine, such as a full table scan or a bitsliced form |
| cache partitioning by trust domain (by ways, or by page colours) | 1 | less cache for each domain, and lost sharing |
| randomized mapping with remapping (CEASER) | 2, as a heuristic | an encryption of each address on the cache path, and periodic remaps |
| a keyed mapping for each domain and each way (ScatterCache) | 2, as a heuristic with a probabilistic analysis | an index function on the cache path |
| a cache flush on each switch of trust domain | 1, for observers that run between the victim's steps | the cost of a cold cache after each switch |

Only the first defense removes the dependence itself. Partitioning removes the shared state, so in the model it is a theorem; the randomized designs make condition 2 costly, and later analyses found weaknesses in some of them, so they are heuristics.

## The template

The stages below are those of the method at the level of the paper's abstract, with named holes and no parameters.

```pseudo id=main
PRIME-PROBE-SHAPE(victim V, cache set X)
L1  obtain own lines that map to the set X           ▷ hole MAP: condition 2, removed by a keyed or random mapping
L2  repeat for each interval
L3      fill X with the own lines                    ▷ the prime stage
L4      let V run                                    ▷ hole SHARE: condition 1, removed by partitioning
L5      learn which own lines are no longer in X     ▷ the probe stage; hole OBSERVE: condition 4
L6      record whether V used X in this interval
L7  relate the record to the secret of V             ▷ hole DEPEND: condition 5, removed by constant-time code
```

### An abstract model

Use the abstract cache of this area: $S$ sets of $W$ ways, lines of $B$ bytes, the address $a$ in the set $\lfloor a / B \rfloor \bmod S$, LRU replacement in each set, and the costs 1 for a hit and 10 for a miss. Let the victim read one entry of a table whose entries lie in two sets, called $X$ and $Y$, and let a secret bit $k$ choose the set. The observer fills $X$ and records 1 if one of his lines is gone afterwards.

| victim | $k = 0$ | $k = 1$ |
|---|---|---|
| reads the entry in $X$ when $k = 0$ and in $Y$ when $k = 1$ | 1 | 0 |
| reads both entries and keeps one with a mask | 1 | 1 |
| either victim, with $X$ split into ways for the observer and ways for the victim | 0 | 0 |

**Claim (theorem, in the abstract cache model).** Let the cache be partitioned: each set has disjoint groups of ways for the observer and for the victim, each domain places lines only in its own group, and LRU acts in each group. Then the observer's sequence of hits and misses is a function of the observer's own sequence of accesses, so it is the same for every secret. *Proof.* By induction on the merged sequence of accesses. The content of the observer's group changes only on the observer's accesses, because an access of the victim reads, inserts or evicts only lines of the victim's group. So after each prefix the observer's group is a function of the observer's accesses in the prefix, and so is the hit or miss of the next observer access.

The same induction shows that a victim whose sequence of sets does not depend on the secret gives the same record in an unpartitioned cache. That is the constant-time policy restricted to the set of each address, and [constant-time verification](/constant-time-verification/) checks the stronger policy on the full address.

### Prime+Probe and Flush+Reload

Flush+Reload watches one shared line and needs shared memory. Prime+Probe watches one set of a [set-associative cache](/set-associative-cache/) and needs only the shared cache. It sees less, because many lines map to the same set, and it is noisier, because any program that uses the set evicts the observer's lines. It works on more systems.

## Classic examples

- **Percival, 2005 (measurement).** Two hardware threads of one core share the first-level cache. Percival showed that one thread could see the table accesses of the RSA exponent windows of the other; see [timing attack](/timing-attack/).
- **Osvik, Shamir and Tromer, 2006 (measurement).** They defined Prime+Probe and Evict+Time and recovered [AES](/advanced-encryption-standard/) keys from implementations that use lookup tables, on a single machine. With Bernstein's work of 2005, this made table-free AES code, bitslicing and the AES instructions of processors the standard answer.
- **Liu, Yarom, Ge, Heiser and Lee, 2015 (measurement).** They built the channel on the shared last-level cache of Intel processors, across cores and across virtual machines, with no shared memory, and used it against exponentiation code in GnuPG. This removed the earlier view that the last-level cache was too big and too noisy for this.
- **Transient execution, 2018.** [Spectre](/spectre-attack/) variants can use Prime+Probe as the channel that carries a value out of discarded instructions.
- **Defenses in hardware, 2018 and 2019.** CEASER and ScatterCache randomize the mapping of lines to sets, so that the observer cannot find his own lines for a set at low cost.

## Variations

- **Evict+Time.** Evict a set, then measure the time of the whole victim operation. It needs a way to start the victim, but no fine timer on the observer's own lines.
- **Synchronous and asynchronous forms.** The observer probes between the victim's operations, or runs at the same time on another thread or core.
- **Other shared structures.** The same contention idea applies to translation caches, branch predictors and memory controllers, and in each case partitioning or secret-independent use removes it.
- **Covert channels.** Two cooperating programs can use set contention as a [covert channel](/covert-channel/).

## Pitfalls

- **Masking only the first access.** If a constant-time routine scans the table but then reads the chosen entry again by its index, the second read leaks the set.
- **Partitioning that leaves a shared path.** A cache partitioned by ways still has shared replacement state in some designs, and the shared state may leak. The theorem above needs the replacement of each group to depend only on that group.
- **Calling a randomized cache a proof.** The randomized designs come with probabilistic arguments about a given attacker strategy, not with a theorem for every strategy.
- **Forgetting the operating system.** A flush on every switch of trust domain covers an observer that runs between the victim's steps, but not one that runs at the same time on another core.

## References
