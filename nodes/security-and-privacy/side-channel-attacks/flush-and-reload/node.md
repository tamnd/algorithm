---
tag: C2M070
kind: technique
slug: flush-and-reload
name: Flush+Reload
aliases:
- flush and reload attack
area: security-and-privacy/side-channel-attacks
level: core
summary: A cache side channel in which an observer that shares memory with a victim learns, one memory line at a time, whether the victim used that line in each interval.
prereqs: [timing-attack, set-associative-cache]
see_also: [prime-and-probe, constant-time-programming, cache, side-channel-attack, meltdown-attack, spectre-attack, binary-exponentiation, covert-channel]
sources:
  - url: "https://www.usenix.org/conference/usenixsecurity14/technical-sessions/presentation/yarom"
    title: Yuval Yarom and Katrina Falkner, FLUSH+RELOAD, a high resolution, low noise, L3 cache side-channel attack, USENIX Security Symposium 2014, pages 719-732
    locator: the threat model with shared memory pages, the description of the technique, the results on GnuPG RSA and the discussion of countermeasures
  - paper: "Dag Arne Osvik, Adi Shamir and Eran Tromer, Cache attacks and countermeasures, the case of AES, CT-RSA 2006, LNCS 3860, pages 1 to 20"
    locator: the earlier cache attacks Evict+Time and Prime+Probe, and the countermeasures
  - url: "https://cr.yp.to/antiforgery/cachetiming-20050414.pdf"
    title: Daniel J. Bernstein, Cache-timing attacks on AES, 2005
    locator: why a secret-dependent memory access leaks through the cache, and why table-free code is the remedy
  - paper: "José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, François Dupressoir and Michael Emmi, Verifying constant-time implementations, 25th USENIX Security Symposium, 2016, pages 53-70"
    locator: the constant-time policy, under which memory addresses do not depend on secrets
---

Flush+Reload is a cache side channel in which an observer learns whether a victim used one particular memory line during an interval. It needs memory that the observer and the victim share, such as the pages of a shared library, and a cache that both use. Yarom and Falkner (2014) showed that it works through the last-level cache, across processor cores and across virtual machines, and used it to read the exponent of an RSA implementation. It works at the level of a single line; [Prime+Probe](/prime-and-probe/) works at the level of a cache set and needs no shared memory. Both are defeated by code whose memory accesses do not depend on secrets.

## In plain words

Two people use the same library and the same shelf. One of them wants to know if the other read a certain book. He puts the book back in the store room. Later he asks for the book. If it comes fast, it was on the shelf, so the other person must have taken it out again. If it comes slowly, nobody used it.

A cache is that shelf. The observer cannot see the victim's data, but he can learn which shared pieces of code or data the victim used, and when. If the victim uses a piece only when a bit of the key is 1, the observer learns that bit.

## When it applies

### Threat model

The observer is an unprivileged program on the same machine as the victim. He can run code at the same time as the victim and he sees only the effect of the cache on his own memory accesses: whether one of his own accesses was a hit or a miss. He cannot read the victim's memory or registers. The guarantees of every defense below hold against this observer.

### Conditions

The technique needs all of these. Each defense removes at least one.

1. **Shared memory.** The observer and the victim map the same physical memory line, for example the read-only code of a shared library, or a page that the operating system or the hypervisor merged because two copies had the same content.
2. **A shared cache.** Both use a cache level that holds the line. On processors with an inclusive last-level cache, removing a line from that level also removes it from the private caches of the other cores, so the channel works across cores.
3. **A way to remove the line.** The observer can evict one given line from the cache, for example with a flush instruction that ordinary programs may use.
4. **A visible difference.** The observer can tell a hit from a miss on his own access to the line.
5. **A secret-dependent use.** The victim uses the line, or does not use it, depending on a secret. Without this condition the record is the same for every secret.

### What removes a condition

| defense | condition it removes | cost |
|---|---|---|
| [constant-time code](/constant-time-programming/): no secret-dependent branch or address | 5 | more work in the cryptographic routine, for example a full table scan |
| no sharing of pages across trust domains (no page merging, separate copies of libraries) | 1 | more memory |
| cache partitioning by trust domain | 2 | less cache for each domain |
| making the flush instruction privileged, or removing coarse timers | 3 or 4 | software that uses them needs another way; a counting thread can rebuild a timer |
| noise and detection by performance counters | none, it only raises the cost (heuristic) | false alarms and a cost on every program |

Constant-time code is the only defense that removes the dependence itself. The others make the channel harder to use, and they hold only for the observer that they model.

## The template

The stages below are the stages of the method at the level of the paper's abstract. They name holes and have no parameters.

```pseudo id=main
FLUSH-RELOAD-SHAPE(victim V, shared line ℓ)
L1  establish that the observer and V map the same line ℓ   ▷ hole SHARE: condition 1, removed by no page sharing
L2  repeat for each interval
L3      remove ℓ from the shared cache                       ▷ hole REMOVE: condition 3
L4      let V run
L5      learn whether ℓ is in the cache again                ▷ hole OBSERVE: condition 4
L6      record one bit: V used ℓ in this interval or not
L7  relate the record to the secret of V                     ▷ hole DEPEND: condition 5, removed by constant-time code
```

### An abstract model

Take an abstract victim that runs in rounds $i = 1, \ldots, n$ with secret bits $k_1, \ldots, k_n$. In each round it uses a line $\ell_A$, and it also uses a second line $\ell_B$ when $k_i = 1$. This is the shape of square and multiply in [binary exponentiation](/binary-exponentiation/), where $\ell_B$ holds the code of the multiply. The observer shares $\ell_B$ and records $o_i = 1$ when $\ell_B$ is in the cache after round $i$.

| victim | secret $k$ | record $o$ of the observer |
|---|---|---|
| uses $\ell_B$ only when $k_i = 1$ | 1 0 1 1 | 1 0 1 1 |
| Montgomery ladder: uses $\ell_B$ in every round | 1 0 1 1 | 1 1 1 1 |
| any victim, with a private copy of $\ell_B$ | 1 0 1 1 | 0 0 0 0 |

**Claim (theorem, in the abstract model).** If the set of lines that the victim uses in each round does not depend on the secret, then the record $o$ is the same for every secret. If the observer's line is not shared with the victim, $o$ depends only on the observer's own accesses. Both follow because in the model the content of a line in the cache after a round is a function of the lines used in that round and before it. The first statement is the constant-time policy; [constant-time verification](/constant-time-verification/) checks it on a program.

### Flush+Reload and the set-associative cache

A [set-associative cache](/set-associative-cache/) maps each line to one set and keeps a few lines in each set. Flush+Reload ignores the sets: it asks about one line that both parties share, so it sees one line exactly and needs condition 1. Prime+Probe asks about a whole set, by filling it with the observer's own lines, so it needs no shared memory but sees only which set the victim used, with more noise from other lines of the same set.

## Classic examples

- **Before 2014.** Bernstein (2005) and [Osvik, Shamir and Tromer](/prime-and-probe/) (2006) showed that the cache leaks the table indices of AES, which made table lookups with a secret index unsafe. Gullasch, Bangerter and Krenn (2011) used a flush of shared lines against AES on one core.
- **Yarom and Falkner, 2014 (measurement).** On Intel processors with an inclusive last-level cache, they observed the use of the square, the reduce and the multiply code of GnuPG RSA through shared library pages. They report the recovery of most bits of the private exponent from one observed operation, across processes and across virtual machines that shared pages through page merging. Their lessons: secret-dependent code paths in shared pages leak, and pages should not be shared across trust domains. GnuPG changed its exponentiation code in response.
- **Transient execution, 2018.** [Meltdown](/meltdown-attack/) and [Spectre](/spectre-attack/) use a cache channel such as Flush+Reload as the last stage, to carry a value out of instructions that the processor later discards. The channel is the same; the source of the secret is new.
- **Covert channels.** Two cooperating programs that are not allowed to communicate can use the same mechanism as a [covert channel](/covert-channel/).

## Variations

- **Evict+Reload.** Remove the line by filling its cache set instead of a flush instruction, for processors or settings where the flush instruction is not available.
- **Flush+Flush.** Use a property of the flush instruction itself instead of a reload. It causes fewer cache misses, which makes detection by miss counters harder.
- **Cache template attacks.** Find automatically which shared lines of a program depend on a secret or on user input, for example key presses.
- **Other shared structures.** The same idea applies to other caches that two domains share, such as translation caches and branch predictors.

## Pitfalls

- **Thinking the cache is private.** On a machine with a shared last-level cache and page merging, programs in different virtual machines share both the line and the cache.
- **Defending only one condition.** Removing a timer or the flush instruction does not remove the dependence. Evict+Reload, counting threads and other channels come back. Remove condition 5 in the cryptographic code.
- **Balancing the work but not the addresses.** Code that does a dummy multiply when $k_i = 0$ has a constant operation count, but if the dummy uses other code or data lines, the record still shows the bit. The addresses must be the same, not only the count.
- **Naming the result a proof.** A measured attack on one processor shows that the channel exists there. The absence of a measured leak shows nothing; the statement that a defense works is a theorem only in a model.

## References
