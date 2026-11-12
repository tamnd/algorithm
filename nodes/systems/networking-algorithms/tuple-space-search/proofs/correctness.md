---
title: Tuple space search returns the best matching rule, with or without early exit and pruning
proves: [correctness]
status: full
---

We use the notation of the page. Field $i$ has width $W_i$. A rule $r$ has one prefix $(p_i, \ell_i)$ for each field, a priority, and a unique id; we order rules by the pair (priority, id), and the smallest pair is the best. The *tuple* of $r$ is $t(r) = (\ell_1, \ldots, \ell_d)$ and its *key* is $(p_1, \ldots, p_d)$. For a packet $x$ and a tuple $t$, let $\mathrm{key}_t(x) = (\lfloor x_1 / 2^{W_1 - \ell_1} \rfloor, \ldots, \lfloor x_d / 2^{W_d - \ell_d} \rfloor)$, the top $\ell_i$ bits of each field.

**The invariant (H).** For the current rule set $S$: there is one hash table $H_t$ for each tuple $t$ of a rule of $S$ and for no other tuple. $H_t$ maps each key $k$ to the list, sorted by (priority, id), of the rules $r \in S$ with $t(r) = t$ and key $k$, and it has no other keys.

**Fact.** Rule $r$ matches $x$ if and only if the key of $r$ equals $\mathrm{key}_{t(r)}(x)$. This is the definition of a prefix match, field by field.

## The basic lookup is correct

**Claim.** If (H) holds, TSS-LOOKUP$(x)$ returns the best rule of $S$ that matches $x$, or "no match" if none does, and it makes one probe for each tuple.

*Proof.* Let $M$ be the set of rules of $S$ that match $x$. For a tuple $t$, the probe of line L4 reads the list of the rules with tuple $t$ and key $\mathrm{key}_t(x)$. By the fact, these are exactly the rules of $M$ with tuple $t$; call this set $M_t$. The list is sorted, so its first entry is the best rule of $M_t$, and the probe returns nothing when $M_t$ is empty. The sets $M_t$ over all tuples $t$ of (H) partition $M$, because each rule has one tuple and that tuple has a table. Line L5 keeps the best of the first entries, which is the best rule of $M$. If $M$ is empty, every probe misses and line L6 returns "no match". The loop of line L2 runs once for each table. $\square$

## Early exit by priority

Let $\mathrm{top}(t)$ be the best rule of all of $H_t$, and visit the tuples in the order of increasing $\mathrm{top}(t)$. The lookup stops before tuple $t$ if it already has a rule $b$ with $b \le \mathrm{top}(t)$.

**Claim.** The early-exit lookup returns the same rule as the basic lookup.

*Proof.* Up to the stop, it does the same probes as the basic lookup on a subset of the tuples. Every rule $r$ of a skipped tuple $t'$ satisfies $r \ge \mathrm{top}(t') \ge \mathrm{top}(t) \ge b$, by the order of the visit, and $r \ne b$ because $b$ lies in an earlier tuple. So no skipped rule is better than $b$, and the best rule found is the best of $M$. If the lookup does not stop, it probes every tuple and is the basic lookup. $\square$

## Pruning

For field $i$, let $A_i(x)$ be the set of tuples $t$ such that some rule of $S$ with tuple $t$ has a field-$i$ prefix that matches $x_i$. Pruned tuple space search probes only the tuples in $A_1(x) \cap \cdots \cap A_d(x)$.

**Claim.** The pruned lookup returns the same rule as the basic lookup.

*Proof.* If a rule $r \in M$ has tuple $t$, then for each field $i$ its prefix matches $x_i$, so $t \in A_i(x)$ for all $i$. So each tuple $t$ with $M_t \ne \emptyset$ is probed, and the argument of the basic lookup applies to these tuples. The other tuples have $M_t = \emptyset$ and add nothing. $\square$

The implementation finds $A_i(x)$ by looking up every prefix of $x_i$ in an index from (prefix, length) to the tuples that use it with a count of rules. A real system finds the same set with one longest prefix match per field, as in the original paper.

## Updates keep the invariant

**Insert $r$.** The insert adds $r$ to the list of $H_{t(r)}$ at the key of $r$, in sorted position, and creates the table or the list if it is missing. This is what (H) asks for $S \cup \{r\}$. It adds $t(r)$ to the index of each field.

**Delete $r$.** The delete removes $r$ from its list. If the list becomes empty it removes the key, and if the table becomes empty it removes the table, so (H) holds for $S \setminus \{r\}$ with no table for an unused tuple. It lowers the counts of the field index and removes an entry when its count reaches 0, so $A_i(x)$ stays exact.

Each update does one hash operation on one table, plus $d$ index updates and a sorted insert into one list (the rules with the same tuple and key, usually one). So an update costs $O(d)$ expected time when the lists are short. The empty structure satisfies (H), so by induction it holds after any sequence of updates, and every lookup is correct.
