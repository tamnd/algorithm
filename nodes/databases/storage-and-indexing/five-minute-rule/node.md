---
tag: HGTXMZ
kind: theorem
slug: five-minute-rule
name: Five-minute rule
aliases:
- Gray-Putzolu five-minute rule
area: databases/storage-and-indexing
level: core
summary: "Keep a page in memory if it is used again within the break-even interval, set by the price of memory, the price of a disk and its access rate. In 1987 it was about five minutes."
prereqs: [buffer-pool]
see_also: [buffer-pool, external-memory-model, lru-k, working-set-model, dbmin, paging-problem, belady-algorithm, log-structured-merge-tree]
sources:
  - paper: "Jim Gray and Franco Putzolu, The 5 minute rule for trading memory for disc accesses and the 10 byte rule for trading memory for CPU time, Proceedings of the 1987 ACM SIGMOD International Conference on Management of Data, 1987"
    title: The 5 minute rule
    locator: the derivation of the break-even interval for keeping a record in memory
  - paper: doi:10.1145/271074.271094
    title: "Jim Gray and Goetz Graefe, The five-minute rule ten years later, and other computer storage rules of thumb, SIGMOD Record 26(4), 1997"
    locator: "equation 1 (the break-even reference interval), the values for 8 KB pages, and the rule for sequential access"
  - paper: "Goetz Graefe, The five-minute rule twenty years later, and how flash memory changes the rules, Proceedings of the Third International Workshop on Data Management on New Hardware (DaMoN), 2007"
    title: The five-minute rule twenty years later (DaMoN version)
    locator: "the recap of the 1987 and 1997 rules, the prices and access rates of 2007, and Table 3 (break-even intervals for page sizes from 1 KB to 256 KB)"
  - paper: doi:10.1145/1538788.1538805
    title: "Goetz Graefe, The five-minute rule 20 years later, and how flash memory changes the rules, Communications of the ACM 52(7), 2009"
    locator: the journal version of the 2007 analysis, with flash memory between RAM and disk
---

The five-minute rule says when it is cheaper to keep a page in memory than to read it from disk each time it is used. Keeping the page costs a slice of memory. Not keeping it costs a slice of the disk's accesses, since each use needs a read. The two costs are equal at a *break-even interval* $T^*$, which depends only on the prices of memory and disks, the access rate of a disk and the page size. A page used more often than once every $T^*$ should stay in memory. With the prices of 1987, Gray and Putzolu found that $T^*$ was about five minutes, and the name stayed. The result is a cost argument, not a replacement policy: it says how much memory a [buffer pool](/buffer-pool/) should have and which pages are worth a frame, and policies such as [LRU-K](/lru-k/) try to keep exactly those pages.

## Statement

Consider pages of one size, stored on disks and cached in memory, under these hypotheses.

- One MB of memory holds $K$ pages and costs $R$ dollars. So one page of memory costs $R/K$.
- One disk costs $D$ dollars and serves $A$ random page reads per second. The disks are needed for their accesses, not for their capacity, and the cost of disk accesses is linear: a load of $x$ reads per second costs $xD/A$.
- A page $q$ is used once every $T_q$ seconds on average, at a steady rate. A page in memory needs no disk read; a page not in memory needs one read per use.
- Nothing else is counted: no CPU time, no writes, no bus or controller limits.

Let

$$T^* = \frac{K}{A} \cdot \frac{D}{R}.$$

**Theorem.** Keeping page $q$ in memory costs less than reading it at every use if and only if $T_q < T^*$, and the two costs are equal when $T_q = T^*$. For a set of pages, the total cost is the least when exactly the pages with $T_q < T^*$ are in memory (pages with $T_q = T^*$ may go either way).

The first factor $K/A$ is a ratio of technology: pages per MB of memory against reads per second of a disk. The second factor $D/R$ is a ratio of prices: a disk against a MB of memory. Gray and Graefe (1997) write the rule in this form, as their equation 1.

## In plain words

Every page you keep in memory costs you a little piece of memory. Every page you leave on disk costs you a little piece of a disk, because each time you need it the disk must spend time to read it, and disk time is bought with disks.

If you use a page very often, the disk time adds up fast, and memory is the cheaper place for it. If you use it rarely, the disk time is small, and it is a waste to hold memory for it.

There is one waiting time where the two costs are the same. If you will use the page again sooner than that, keep it. If not, let it go. With the prices of the late 1980s, that waiting time was about five minutes, which gave the rule its name.

## Proof

Fix a page $q$ and measure costs in dollars of equipment.

If $q$ is in memory, it uses one page of memory, which costs $R/K$, and no disk reads.

If $q$ is not in memory, it uses no memory, and each use reads it from disk. It is used $1/T_q$ times per second, so it puts a load of $1/T_q$ reads per second on the disks. A disk serves $A$ reads per second, so this load needs $1/(A T_q)$ of a disk, which costs $D/(A T_q)$ by the linearity hypothesis.

Keeping $q$ costs less if and only if

$$\frac{R}{K} < \frac{D}{A T_q} \iff T_q < \frac{K D}{A R} = T^*,$$

where the step multiplies both sides by the positive number $K T_q / R$. Equality holds on one side if and only if it holds on the other, which gives the case $T_q = T^*$.

For a set $Q$ of pages and a choice $S \subseteq Q$ of the pages in memory, the total cost is

$$C(S) = \sum_{q \in S} \frac{R}{K} + \sum_{q \in Q \setminus S} \frac{D}{A T_q}.$$

Each page contributes one of its two terms, and the term of $q$ does not depend on the choice made for any other page. So $C(S)$ is the least exactly when each page takes the smaller of its two terms, which by the first part means $q \in S$ for $T_q < T^*$ and $q \notin S$ for $T_q > T^*$. $\square$

## Consequences

- **The rule.** Cache a page if it is used more often than once every $T^*$ seconds, and give the buffer pool enough memory to hold all such pages. This is a rule of thumb for buying and sizing memory; its value moves with prices and devices.
- **1987.** Gray and Putzolu derived the rule for records of about 1 KB and found about five minutes. Graefe (2007) recalls that the calculation gave about 400 seconds, which was rounded to five minutes, and that the same paper gave about one hour for records of 100 bytes and about two minutes for pages of 4 KB. Gray and Graefe (1997) write that in 1986 the break-even point was 100 seconds but the rule anticipated five minutes. These are measurements of their year.
- **1997.** For 8 KB pages, Gray and Graefe (1997) use $K = 128$ pages per MB, $A = 64$ reads per second, a disk of 2,000 dollars and memory at 15 dollars per MB, so $T^* = (128/64) \cdot (2000/15) \approx 2 \cdot 133 = 266$ seconds. Prices had fallen, but the two ratios moved in opposite directions, and the interval was again about five minutes. For 2 KB pages they get about 20 minutes.
- **Sequential access.** For large transfers, $K$ is the number of transfer units per MB and $A$ the number of transfers per second. With 64 KB transfers, Gray and Graefe (1997) use 16 units per MB and 80 transfers per second and get a break-even interval of 26 seconds. Data read sequentially is worth caching only if it is used again very soon.
- **2007 and flash.** Graefe (2007) repeats the computation with RAM, flash memory and SATA disks. For 4 KB pages he gets 5,248 seconds, about 90 minutes, between RAM and a SATA disk; 876 seconds, about 15 minutes, between RAM and flash; and 8,070 seconds between flash and a disk. Between RAM and disk, the five-minute rule now holds for pages of 64 KB (334 seconds in his Table 3). He concludes that flash is a good layer between RAM and disk, and that larger pages suit disks.
- **A different question for a fixed memory.** In the [external memory model](/external-memory-model/), the memory is fixed and an algorithm minimizes I/Os. In the external memory model, the memory holds M/B blocks; this is the number of buffer pages B of this page. The five-minute rule asks the opposite question: given the prices, how many buffer pages B should be bought, and for which pages.

## Tightness

The threshold cannot be moved. At $T_q = T^*$ the two costs are equal, so for any $T_q$ slightly below $T^*$ caching is strictly cheaper and for any $T_q$ slightly above it is strictly dearer. A rule with any other threshold makes the wrong choice for some page.

The hypotheses matter, and each of them fails in some real setting.

- **Disks bought for capacity.** If the disks are needed anyway to hold the data, their accesses are already paid for up to their rate, and the cost of a read is near zero until the disks are busy. Then less should be cached than $T^*$ says.
- **Whole devices.** Disks and memory are bought in units, so the cost is a step function, not a line. The rule holds for the margin of a large installation, not for one disk.
- **Steady use.** The proof uses only the mean rate $1/T_q$. A page used in bursts can be cached only during its bursts, which a policy can exploit and the rule does not see.
- **Page size.** $K$ falls in proportion to the page size, while $A$ falls slowly, since a random read of a small page is dominated by the seek. So $T^*$ falls roughly as the page size grows. In Graefe's Table 3 for RAM and a SATA disk, the interval goes from 20,978 seconds for 1 KB pages to 88 seconds for 256 KB pages.
- **Other costs.** Writes, CPU time and the energy of devices are left out. Adding a write per eviction of a dirty page raises the cost of not caching and so raises $T^*$.

## History

Gray and Putzolu (1987) stated the five-minute rule, together with a ten-byte rule for trading memory against CPU time. Gray and Graefe (1997) revisited it ten years later, wrote it as the product of a technology ratio and a price ratio, and found that it still gave about five minutes for random access to 8 KB pages, with a much shorter interval for sequential access. Graefe (2007, and the journal version in 2009) revisited it again with flash memory, and found intervals of about 15 minutes between RAM and flash and about 90 minutes between RAM and disk for 4 KB pages.

## References
