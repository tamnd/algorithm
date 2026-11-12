---
tag: GHBQBX
kind: definition
slug: generational-hypothesis
name: Generational hypothesis
aliases:
- weak generational hypothesis
- strong generational hypothesis
area: systems/garbage-collection
level: intro
summary: "The weak generational hypothesis: most objects die young. So a collection of the youngest objects finds much garbage and copies few survivors."
prereqs: [garbage, heap-reachability]
see_also: [generational-garbage-collection, generational-collector-pause-tradeoff, generational-collector-beltway, remembered-set, copying-collection, geometric-distribution]
sources:
  - paper: doi:10.1145/358141.358147
    title: Henry Lieberman and Carl Hewitt, A real-time garbage collector based on the lifetimes of objects, Communications of the ACM 26(6), 419-429, 1983
    locator: the argument that recently created objects are the most likely to become garbage, and the division of the heap into regions by age
  - paper: doi:10.1145/800020.808261
    title: David Ungar, Generation scavenging, a non-disruptive high performance storage reclamation algorithm, ACM SIGSOFT/SIGPLAN Software Engineering Symposium on Practical Software Development Environments, 157-167, 1984
    locator: the observation that most new objects die young, which is the base of the scavenger
  - paper: doi:10.1145/118014.117957
    title: Barry Hayes, Using key object opportunism to collect old objects, OOPSLA 1991, ACM SIGPLAN Notices 26(11), 33-46
    locator: the distinction between the weak and the strong generational hypothesis, and the Cedar lifetime data
  - paper: doi:10.1145/258915.258925
    title: William D. Clinger and Lars T. Hansen, Generational garbage collection and the radioactive decay model, PLDI 1997, 97-108
    locator: the radioactive decay (constant mortality) model, and the finding of little support for the strong hypothesis in their benchmarks
  - book: isbn:9781032218038
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, second edition, CRC Press, 2023
    locator: Chapter 9, Sections 9.2 (Measuring time) and 9.3 (Generational hypotheses)
---

The *generational hypothesis* is a claim about the lifetimes of the objects that programs allocate. The *weak* generational hypothesis says that most objects die young: most objects become [garbage](/garbage/) soon after their allocation. The *strong* generational hypothesis says more: an older object is less likely to die than a younger one, at every age. The weak form holds in measurements of many programs and is the base of [generational garbage collection](/generational-garbage-collection/). The strong form does not hold in general.

## Definition

**Time and age.** Measure time by the amount of memory allocated, in bytes or, in a model where each object has size one, in objects. This clock moves only when the program allocates, so it is the clock that decides when a collector runs. An object allocated at time $b$ has *age* $t - b$ at time $t$. Its *lifetime* $L \ge 1$ is the amount allocated between its birth and the moment it stops being [reachable](/heap-reachability/): the object is live at time $t$ exactly when $t - b < L$.

**Lifetime distribution.** Treat the lifetime of a newly allocated object as a random variable $L$ with values in $\{1, 2, \ldots\}$. Its survival function is $S(a) = \Pr[L > a]$, so $S(0) = 1$ and $S$ is non-increasing. Its *hazard* (mortality rate) at age $a$ is

$$h(a) = \Pr[L = a + 1 \mid L > a] = \frac{S(a) - S(a+1)}{S(a)}, \qquad S(a) > 0.$$

**Weak generational hypothesis.** For a region of size $N$ that is small compared with the heap, most objects die before they reach age $N$. In terms of the model, the expected fraction of a nursery of $N$ objects that is still live when the nursery is collected,

$$\sigma(N) = \frac{1}{N} \sum_{a=0}^{N-1} S(a),$$

is small, for example 0.1 or less, at a nursery size that is a small fraction of the heap.

**Strong generational hypothesis.** The hazard $h(a)$ is non-increasing for all $a$: at every age, an older object is at most as likely to die next as a younger object. This is a claim about old objects too, not only about the first few allocations of an object's life.

**Why the weak form makes young collections cheap.** Assume one object of size one is allocated per time step, and that the nursery is collected each time it holds $N$ objects. At a collection at time $t$, the nursery holds exactly one object of each age $0, 1, \ldots, N - 1$. The object of age $a$ is live with probability $S(a)$, so by linearity of expectation the expected number of live objects in the nursery is $\sum_{a=0}^{N-1} S(a) = N \sigma(N)$. A [copying](/copying-collection/) collection of the nursery traces and copies only the live objects, so its work is proportional to $N\sigma(N)$, not to $N$. This step needs no independence between lifetimes. The work per allocated object is $\sigma(N)$, and the weak hypothesis says exactly that this number is small.

Both hypotheses are claims about observed programs, not theorems. They hold or fail for a given program and a given input. Measured lifetimes depend on the language, the compiler (escape analysis removes many short-lived objects from the heap) and the workload.

## Examples and non-examples

**A two-class mixture (weak form holds).** Let 90 percent of the objects have a geometric lifetime with mean 10 and 10 percent a geometric lifetime with mean 10000, all in objects allocated. For a geometric lifetime with mean $\mu$, $S(a) = (1 - 1/\mu)^a$ and $\sum_{a<N} S(a) = \mu\,(1 - (1 - 1/\mu)^N)$. The expected survivors of one nursery collection are:

| nursery size $N$ | expected survivors $N\sigma(N)$ | fraction $\sigma(N)$ |
|---|---|---|
| 10 | 6.86 | 0.6861 |
| 100 | 18.95 | 0.1895 |
| 1000 | 104.17 | 0.1042 |
| 10000 | 641.14 | 0.0641 |

With a nursery of 1000 objects, a collection copies about 104 objects and reclaims about 896. Almost all of the short-lived class is dead by age 100. The survivors are mostly from the long-lived class, so the fraction falls slowly once $N$ passes a few times the short mean. The hazard falls with age: $h(0) = 0.09001$, $h(10) = 0.07588$, $h(50) = 0.00455$, $h(100) = 0.00012$ and $h(1000) = 0.0001$ to five places. So this model also meets the strong form. A finite mixture of geometric lifetimes always has a non-increasing hazard, because the surviving objects are more and more those of the long-lived class.

**One long-lived class (weak form fails).** If all objects have a geometric lifetime with mean 10000, then $\sigma(1000) = 0.9517$ and $\sigma(100) = 0.9951$. A nursery collection copies almost every object it holds, and a generational collector is slower than a plain collector of the whole heap, because it copies the same objects again later.

**The radioactive decay model.** A geometric lifetime has a constant hazard $h(a) = 1/\mu$. Age then gives no information about the future: an old object and a new object are equally likely to die next. Clinger and Hansen studied this model and showed that a collector then does better if it collects the objects that have had the longest time to die, which are the oldest ones. This is the idea of older-first collection, which [Beltway](/generational-collector-beltway/) can express.

**A phase structure (strong form fails).** Let 90 percent of the objects live for 1 step and 10 percent for exactly 50 steps, for example the temporary objects and the tables of one phase of a program. Then $h(0) = 0.9$, $h(a) = 0$ for $1 \le a \le 48$, and $h(49) = 1$. The weak form holds: $\sigma(50) = 5.9/50 = 0.118$ and $\sigma(100) = 5.9/100 = 0.059$. But the hazard rises at age 49: these old objects are about to die together. Measured programs show this pattern often, for example at the end of a compiler pass or of a request. Hayes described clusters of objects that are allocated together and die together, and Clinger and Hansen found little support for the strong form in their benchmarks.

**Not about reachability.** The hypothesis does not say which objects are garbage. A collector must still prove that an object is unreachable before it frees it. The hypothesis only says where garbage is likely to be, so that a collector can choose the region to collect.

## Related definitions

- [Garbage](/garbage/) and [heap reachability](/heap-reachability/): the hypothesis speaks of the time at which objects become unreachable.
- [Generational garbage collection](/generational-garbage-collection/): the technique that uses the weak form. It collects a small nursery often and the old generation rarely.
- [Pause time and nursery size](/generational-collector-pause-tradeoff/): the exact cost model behind the table above, with promotion and premature tenuring.
- [Remembered set](/remembered-set/): the cost that a generational collector pays for the hypothesis. It must record pointers from old objects to young ones.
- [Beltway](/generational-collector-beltway/): a framework that also covers collectors built on other lifetime models, such as older-first.
- [Geometric distribution](/geometric-distribution/): the memoryless lifetime of the radioactive decay model.

## References
