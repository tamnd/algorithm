---
tag: DFBVFN
kind: algorithm
slug: tuple-space-search
name: Tuple space search
aliases:
- tuple space search
- pruned tuple space search
area: systems/networking-algorithms
level: advanced
summary: "Classify packets by grouping the rules by their vector of prefix lengths, one hash table per vector. A lookup probes each table once; an update is one hash insert or delete."
solves: [packet-classification]
model: word-ram
complexity:
  vars: {n: the number of rules, d: the number of fields, m: the number of distinct tuples}
  time: {worst: O(m d) expected, update: O(d) expected}
  space: {extra: O(n d)}
properties: {deterministic: false, online: true}
history:
  year: 1999
  people: [V. Srinivasan, Subhash Suri, George Varghese]
  note: Presented at ACM SIGCOMM 1999. Open vSwitch made it the main software classifier of SDN switches.
prereqs: [packet-classification, hash-table, longest-prefix-match]
see_also: [hicuts, tree-bitmap, dictionary, universal-hashing, bloom-filter]
sources:
  - paper: doi:10.1145/316188.316216
    title: V. Srinivasan, Subhash Suri and George Varghese, Packet classification using tuple space search, ACM SIGCOMM 1999
    locator: pages 135 to 146 (tuples, pruned tuple search, rectangle search and its lower bound for two fields)
  - url: "https://www.usenix.org/conference/nsdi15/technical-sessions/presentation/pfaff"
    title: "Ben Pfaff, Justin Pettit, Teemu Koponen, Ethan Jackson, Andy Zhou, Jarno Rajahalme, Jesse Gross, Alex Wang, Jonathan Stringer, Pravin Shelar, Keith Amidon and Martin Casado, The design and implementation of Open vSwitch, USENIX NSDI 2015"
    locator: pages 117 to 130 (the tuple space classifier, priority sorting, staged lookup and the megaflow cache)
  - paper: doi:10.1145/3359989.3365431
    title: Levente Csikor, Dinil Mon Divakaran, Min Suk Kang, Attila Kőrösi, Balázs Sonkoly, Dávid Haja, Dimitrios P. Pezaros, Stefan Schmid and Gábor Rétvári, Tuple space explosion, a denial-of-service attack against a software packet classifier, ACM CoNEXT 2019
    locator: pages 292 to 304
  - book: isbn:9780120884773
    title: George Varghese, Network Algorithmics, Morgan Kaufmann, 2005
    locator: Chapter 12, Packet Classification
---

Tuple space search is a method for [packet classification](/packet-classification/) by V. Srinivasan, Subhash Suri and George Varghese (1999). Each rule is a vector of prefixes, one for each header field, and its *tuple* is the vector of prefix lengths. All rules with the same tuple can be found by one exact-match lookup: cut each field of the packet to the length that the tuple gives, and look up the result in a [hash table](/hash-table/). So the method keeps one hash table for each tuple, probes every table once, and keeps the best rule found. The cost is one probe for each tuple, and real rule sets have far fewer tuples than rules. An insert or a delete is one hash operation, which is why Open vSwitch uses tuple space search for the rules that an SDN controller changes all the time.

## In plain words

Think of a large set of forms, each one partly filled in. One form names a street and a house number. Another names only a city. A third names a city and a street. To find all the forms that fit one full address, you could read every form. Instead, put the forms in piles by *which* parts they fill in: one pile for "city only", one for "city and street", and so on. Inside a pile, all forms fill in the same parts, so you can sort the pile like a dictionary.

Now take the full address, keep only the parts that a pile uses, and look that up in the pile. One lookup for each pile finds every fitting form. There are usually only a few piles, even when there are many forms.

## The problem

The input is a classifier of $n$ rules over $d$ fields, where field $i$ is a $W_i$-bit integer. Each field of a rule is a prefix $(p_i, \ell_i)$: the rule wants the top $\ell_i$ bits of $x_i$ to equal $p_i$, and $\ell_i = 0$ is a wildcard. Each rule has a priority, and a smaller value wins. For a packet $x$, return the best rule that matches. Port ranges are first split into prefixes, as on the [packet classification](/packet-classification/) page; one range becomes at most $2W - 2$ prefixes. The structure must also support inserts and deletes.

## The algorithm

**Tuples.** The tuple of a rule is $t = (\ell_1, \ldots, \ell_d)$ and its key is $(p_1, \ldots, p_d)$. For a packet $x$, let $\mathrm{key}_t(x)$ be the vector of the top $\ell_i$ bits of each field $x_i$. A rule with tuple $t$ matches $x$ exactly when its key equals $\mathrm{key}_t(x)$. So all matching rules of tuple $t$ come out of one exact-match probe.

**Structure.** For each tuple $t$ that some rule uses, a hash table $H_t$ maps each key to the rules with that tuple and key, sorted by priority. Two rules with the same tuple and the same key cover the same packets, so only the first of them can ever win, but both are kept so that a delete is easy.

```pseudo id=main
TSS-LOOKUP(H, x)                           ▷ H: one hash table H_t for each tuple t
L1  best ← none
L2  for each tuple t with a table H_t do
L3      k ← key_t(x)                       ▷ the top ℓ_i bits of each field x_i
L4      r ← the best rule of H_t[k], or nil
L5      if r ≠ nil and (best = none or r is better than best) then best ← r
L6  return best
```

**Updates.** To insert a rule, compute its tuple, create $H_t$ if it does not exist, and insert the rule under its key. To delete a rule, remove it, and remove the table when it becomes empty, so that the lookup does not probe it.

**Early exit by priority.** Sort the tuples by the best priority in their table. Visit them in that order, and stop as soon as the best rule found so far is better than the best rule of the next tuple. Open vSwitch does this. It helps when high-priority rules match often.

**Pruned tuple space search.** First do a [longest prefix match](/longest-prefix-match/) on each field separately, against the prefixes that the rules use in that field. Along the way, collect for field $i$ the set $A_i$ of tuples that have a rule whose field-$i$ prefix matches $x_i$. A tuple outside $A_1 \cap \cdots \cap A_d$ cannot contain a matching rule, so probe only the tuples in the intersection.

**Rectangle search.** For two fields, the tuples form a grid of $(W+1) \times (W+1)$ cells. With markers and precomputed best rules, in the style of binary search on prefix lengths, the paper probes the grid from a corner so that each probe removes a whole row or a whole column. A lookup then takes at most $2W - 1$ probes, and the paper shows that no search that only probes tuples can do better in the worst case for two fields. Markers make updates slow, so rectangle search suits static classifiers.

## Example

Take two 4-bit fields and six rules, with priority equal to the rule number.

| rule | field 1 | field 2 | tuple |
|---|---|---|---|
| R1 | `10*` | `0*` | (2, 1) |
| R2 | `1*` | `01*` | (1, 2) |
| R3 | `101*` | `*` | (3, 0) |
| R4 | `11*` | `1*` | (2, 1) |
| R5 | `*` | `0110` | (0, 4) |
| R6 | `*` | `*` | (0, 0) |

The six rules use five tuples. $H_{(2,1)}$ has two keys: (`10`, `0`) for R1 and (`11`, `1`) for R4.

*The packet* $x = (1011, 0110)$. The probes are (`10`, `0`) in $H_{(2,1)}$, a hit on R1; (`1`, `01`) in $H_{(1,2)}$, a hit on R2; `101` in $H_{(3,0)}$, a hit on R3; `0110` in $H_{(0,4)}$, a hit on R5; and the empty key in $H_{(0,0)}$, a hit on R6. All five probes hit, and the best rule is R1. With early exit, the tuple (2, 1) has the best top priority (R1), so it is probed first; it gives R1, and every other tuple has a worse top rule, so the lookup stops after 1 probe.

*The packet* $x = (1100, 1001)$. The basic lookup probes all 5 tuples and finds R4 in $H_{(2,1)}$ and R6 in $H_{(0,0)}$; the answer is R4. With early exit, it probes (2, 1) and finds R4 (priority 4), then (1, 2) with top priority 2 and (3, 0) with top priority 3, which both miss, and stops before (0, 4), whose top priority is 5: 3 probes. With pruning, field 1 matches the prefixes `*` and `1*` and `11*` of the rules, which allow the tuples (0, 4), (0, 0), (1, 2) and (2, 1). Field 2 matches `*` and `1*`, which allow (3, 0), (0, 0) and (2, 1). The intersection is (0, 0) and (2, 1): 2 probes.

**A synthetic classifier.** With `random_prefix_classifier` and seed 7 (5 fields; addresses are prefixes of length 8, 16, 24 or 32 or wildcards; ports exact, wildcards or the range 1024 to 65535 split into 6 prefixes; the protocol exact or a wildcard), and 2000 packets drawn inside random rules:

| rules | tuples | basic probes | early exit, mean | pruned, mean and max |
|---|---|---|---|---|
| 100 | 96 | 96 | 49.64 | 2.11, 3 |
| 1000 | 519 | 519 | 235.54 | 2.98, 6 |
| 5000 | 1311 | 1311 | 454.90 | 4.49, 11 |

This set mixes many prefix lengths on purpose, so it has many tuples; the basic search is then slow, and pruning is what makes it fast. Real classifiers use fewer lengths: Srinivasan, Suri and Varghese report that the number of tuples in their real databases was much smaller than the number of rules.

## Correctness

The [proof](proofs/correctness.md) rests on one fact: a rule with tuple $t$ matches $x$ exactly when its key equals $\mathrm{key}_t(x)$. So the probe of line L4 returns the best matching rule among the rules of tuple $t$, or nothing. Every rule has exactly one tuple, and every used tuple has a table, so the best of the probe results (line L5) is the best matching rule overall. Early exit skips only tuples whose best rule is already worse than the current answer. Pruning skips only tuples that have no rule whose prefixes all match $x$. Updates keep one table for each used tuple, with each rule in the list of its key.

## Complexity

A lookup does one hash probe for each of the $m$ tuples, so it takes $O(md)$ expected time to form the keys and probe; with a [universal hash family](/universal-hashing/) the expectation is over the choice of hash function, for any rule set. In the worst case $m$ can be as large as $\min(n, \prod_i (W_i + 1))$. The space is $O(nd)$ for the rules and the tables. An insert or a delete is one hash operation, $O(d)$ expected time, plus the creation or removal of a table.

With pruning, the probes drop to the size of the intersection of the per-field tuple sets, at the cost of $d$ one-field [longest prefix matches](/longest-prefix-match/). Rectangle search uses at most $2W - 1$ probes for two fields.

## Properties

- **Fast updates.** One hash insert or delete per rule, with no rebuild. This is the main reason to use it.
- **Prefix fields only.** Ranges must be split into prefixes first, which can multiply the rules.
- **The cost depends on the tuples, not the rules.** A rule set with few distinct prefix lengths is fast, however many rules it has.
- **Randomized.** The expected time comes from the hash tables.
- **Simple.** The structure is a map of maps, and it is easy to make concurrent.

## Variants and improvements

- **Pruned tuple space search** probes only the tuples that each field allows, as above.
- **Rectangle search** for two fields reaches $2W - 1$ probes with markers.
- **Open vSwitch** (Pfaff et al., 2015) sorts the tuples by priority and stops early, and does a *staged lookup*: it checks the metadata fields first, then the L2, L3 and L4 fields, and stops a table probe early when an earlier stage fails. It also keeps a *megaflow cache*: after a slow-path lookup it installs one entry that covers all packets that the same rules would treat in the same way, with wildcards for the fields that the lookup did not need to look at.
- **Tuple merging** joins tuples with close lengths into one table with a shorter key and checks the full rule after the hit, to cut the number of tuples.
- **Bloom filters** in front of the tables, one per tuple, can skip most of the probes that would miss, as in the [Bloom filter](/bloom-filter/) method for longest prefix match.

## When to use it

Use tuple space search when the rules change often and the lookup runs in software: software switches, virtual switches in hypervisors, and SDN data planes. Use it also when the rule set has few distinct prefix lengths, for example when most rules use full addresses or wildcards.

Do not use it when the rule set has many distinct prefix lengths in several fields and the lookup must have a firm time bound. Then a decision tree such as [HiCuts](/hicuts/) or a TCAM is faster in the worst case.

## Pitfalls

- **Tuple explosion.** The lookup cost grows with the number of tuples. Csikor et al. (2019) showed that an attacker who can add rules, for example through the access control lists of a cloud tenant, can create many tuples and slow down Open vSwitch a great deal. Bound the number of tuples or use pruning.
- **Range expansion.** A rule with port ranges becomes many prefix rules, possibly in many different tuples. A range of 1024 to 65535 alone uses 6 prefix lengths.
- **Empty tables.** A delete must remove an empty table. Otherwise the lookup keeps probing it.
- **Equal keys.** Two rules with the same tuple and key can have different priorities. The table entry must keep the best one first, and a delete of the best one must expose the next.
- **Early exit needs the order.** The early-exit test is only valid if the tuples are visited in order of their best priority; that order must be updated when rules come and go.

## Implementations

## History

Srinivasan, Suri and Varghese presented tuple space search at ACM SIGCOMM 1999, the same conference where Gupta and McKeown presented Recursive Flow Classification. The paper also gave pruned tuple search and rectangle search, and showed that rectangle search is optimal among searches that probe tuples for two fields. The method had its largest impact much later, when Open vSwitch made it the core of its flow classifier in the 2010s (Pfaff et al., NSDI 2015). In 2019, Csikor et al. showed the tuple explosion attack against it.

## References
