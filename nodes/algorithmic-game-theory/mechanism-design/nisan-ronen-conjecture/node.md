---
tag: 25H5W9
kind: theorem
slug: nisan-ronen-conjecture
name: Nisan-Ronen conjecture
aliases:
- Christodoulou-Koutsoupias-Kovacs theorem
area: algorithmic-game-theory/mechanism-design
level: research
summary: "A theorem with a conjecture name: no deterministic truthful mechanism for n unrelated machines has makespan ratio below n. Christodoulou, Koutsoupias and Kovacs proved it at STOC 2023."
prereqs: [truthful-scheduling-unrelated-machines, cycle-monotonicity]
see_also: [truthful-scheduling-unrelated-machines, vcg-mechanism, unrelated-machine-scheduling, roberts-theorem, truthful-in-expectation, monotone-allocation-rule, lenstra-shmoys-tardos, makespan]
sources:
  - paper: doi:10.1145/3564246.3585176
    title: "George Christodoulou, Elias Koutsoupias and Annamaria Kovacs, A proof of the Nisan-Ronen conjecture, Proceedings of the 55th ACM Symposium on Theory of Computing (STOC 2023), 672-685"
    locator: the main theorem, the lower bound n for deterministic truthful mechanisms on n unrelated machines
  - paper: doi:10.1145/3785408
    title: "George Christodoulou, Elias Koutsoupias and Annamaria Kovacs, A proof of the Nisan-Ronen conjecture, Journal of the ACM 73(1) (2026), Article 6"
    locator: the journal version of the proof
  - paper: "George Christodoulou, Elias Koutsoupias and Annamaria Kovacs, A proof of the Nisan-Ronen conjecture, an overview, ACM SIGecom Exchanges 21(1) (2023), 42-48"
    locator: the outline of the proof through boundary functions, nice multi-stars and boxes, Lemma 7 and the list of earlier lower bounds
  - paper: doi:10.1006/game.1999.0790
    title: "Noam Nisan and Amir Ronen, Algorithmic mechanism design, Games and Economic Behavior 35(1-2) (2001), 166-196 (conference version in STOC 1999)"
    locator: the conjecture, the VCG upper bound n and the lower bound 2
  - paper: "George Christodoulou, Elias Koutsoupias and Annamaria Kovacs, On the Nisan-Ronen conjecture, Proceedings of the 62nd IEEE Symposium on Foundations of Computer Science (FOCS 2021), 839-850"
    locator: the first lower bound that grows with n, 1 + sqrt(n - 1)
  - paper: "Ahuva Mu'alem and Michael Schapira, Setting lower bounds on truthfulness, Games and Economic Behavior 110 (2018), 174-193"
    locator: the short weak-monotonicity proof of the lower bound 2
---

The Nisan-Ronen conjecture is now a theorem: for scheduling jobs on $n$ unrelated machines that privately know their processing times, no deterministic truthful mechanism has approximation ratio for the makespan below $n$. Since the [VCG mechanism](/vcg-mechanism/) has ratio $n$, the simplest truthful mechanism is the best one. Nisan and Ronen conjectured this in 1999, and Christodoulou, Koutsoupias and Kovacs proved it at STOC 2023; the page keeps the historical name. Its close page, [truthful scheduling on unrelated machines](/truthful-scheduling-unrelated-machines/), describes the problem as a whole, with its variants, its randomized and single-parameter versions, and all known bounds.

## Statement

There are $n$ machines and $m$ jobs. Machine $i$ privately knows its times $t_{i1}, \dots, t_{im} \ge 0$. A mechanism maps reported times to an allocation of the jobs and payments to the machines, and machine $i$ has utility equal to its payment minus the total true time of its jobs. A mechanism is *truthful* if reporting the true times is a dominant strategy for every machine. It has *approximation ratio* $\rho$ if its makespan is at most $\rho$ times the optimal makespan for every input.

**Theorem (Christodoulou, Koutsoupias and Kovacs 2023).** For every $n \ge 2$, every deterministic truthful mechanism for scheduling unrelated machines has approximation ratio at least $n$, when the number of jobs is allowed to be large enough.

**Theorem (Nisan and Ronen 1999).** The VCG mechanism, which gives each job to the machine with the smallest reported time and pays it the second smallest time, is truthful and has approximation ratio at most $n$.

Together: the optimal approximation ratio of deterministic truthful mechanisms for $n$ unrelated machines is exactly $n$. The bounds hold with no limit on running time.

## In plain words

Some jobs must be split among computers, and each computer's owner alone knows how long the computer needs for each job. The owners are paid, and each wants high pay for little work. A rule that never uses chance and always makes honest answers the best plan has to give up a lot. With many computers, such a rule can be forced into a plan that is as many times slower than the best plan as there are computers. The rule that gives each job to the fastest computer for it already reaches this limit. So, among rules without chance, nothing beats this simplest rule. This was suspected for more than twenty years before it was proved.

## Proof

**Upper bound $n$.** VCG treats each job as a separate reverse [Vickrey auction](/vickrey-auction/), so it is truthful. For true times $t$, its makespan is at most the total work $\sum_j \min_i t_{ij}$. Every schedule puts job $j$ on some machine, which needs at least $\min_i t_{ij}$, so the total load of every schedule is at least $\sum_j \min_i t_{ij}$, and some machine has at least $\frac{1}{n}$ of it. So $\mathrm{OPT} \ge \frac{1}{n} \sum_j \min_i t_{ij}$, and the VCG makespan is at most $n \cdot \mathrm{OPT}$.

**Lower bound for two machines.** For $n = 2$ the theorem is the bound 2 of Nisan and Ronen, and it has a short proof. Truthful mechanisms satisfy weak monotonicity, the 2-cycle case of [cycle monotonicity](/cycle-monotonicity/), which in this cost setting reads: if a machine with times $t$ gets the set $A$ and with times $t'$ gets the set $A'$, the others fixed, then
$$\sum_{j \in A} (t'_j - t_j) \;\ge\; \sum_{j \in A'} (t'_j - t_j).$$
Take three jobs with $t_1 = (1, 100, 1)$ and $t_2 = (100, 1, 1)$, so that $\mathrm{OPT} = 2$. Suppose the ratio is at most $2 - \delta$ with $\delta > 0$. Then job 1 goes to machine 1 and job 2 to machine 2, and by symmetry job 3 goes to machine 2, so machine 1 gets $A = \{1\}$. Change machine 1 to $t_1' = (0, 100, 1 + \varepsilon)$ with $2 / (1 + \varepsilon) > 2 - \delta$. Now $\mathrm{OPT} = 1 + \varepsilon$, every allocation that does not give jobs 1 and 3 to machine 1 has makespan at least 2, so machine 1 gets $A' = \{1, 3\}$. The change is $(-1, 0, \varepsilon)$, its sum over $A$ is $-1$ and over $A'$ is $-1 + \varepsilon$, and weak monotonicity fails. This proof is the one of Mu'alem and Schapira.

**Lower bound for general $n$: outline.** The full proof is long; the outline below follows the overview by the authors.

1. *Instances on graphs.* Every job has very large times on all machines except two, so a mechanism with ratio at most $n$ must give it to one of these two. A job is then an edge $\{i, j\}$ of a multigraph whose vertices are the machines. The proof uses *multi-cliques*, where every pair of machines has many parallel edges, and in which every edge has time 0 at one of its two endpoints. Such edges do not raise the optimal makespan.
2. *Boundary functions.* For an edge $e = \{i, j\}$, fix all other times and let $\psi^e_{i,j}(z)$ be the threshold for machine $i$ when machine $j$ has time $z$ on $e$: the edge goes to $i$ when $i$'s time is below the threshold and to $j$ when it is above. Single-parameter monotonicity makes each boundary function nondecreasing in $z$. Truthfulness for two machines and two jobs restricts how two boundary functions can interact, and this is used again and again.
3. *Nice multi-stars.* A star with root $i$ and one edge to each other machine is *nice* if the root's times are 0, the leaves' times are all close to one value $z$, and the boundary values add up to about $(n - 1) z$. By the probabilistic method, every mechanism with bounded ratio has a multi-clique that contains a nice multi-star of any required multiplicity.
4. *Boxes.* A star is a *box* if, when the root's times are raised to just below the boundary values, the mechanism gives all the star's edges to the root. Using the 2-by-2 restriction, every nice multi-star of high enough multiplicity contains a star with $n - 1$ leaves that is a box.
5. *The final count.* Take a nice box star and add one more job, a loop at the root with time $z$ for the root. The mechanism gives all edges to the root, so its makespan is about $z + (n - 1) z = n z$, while giving the loop to the root and each edge to its leaf has makespan about $z$. Letting the approximation parameters tend to 0 gives the ratio $n$. $\square$

## Consequences

- **VCG is optimal among deterministic truthful mechanisms** for unrelated machines, even with unlimited computation. A designer who wants a better worst-case ratio must use randomization, restrict the domain, or change the model.
- **Incentives, not computation, are the obstacle.** Without incentives, the [Lenstra-Shmoys-Tardos algorithm](/lenstra-shmoys-tardos/) gets ratio 2 in polynomial time. So truthfulness can cost a factor that grows with $n$, while for related machines, a [single-parameter](/single-parameter-environment/) case, it costs almost nothing: there is a deterministic truthful PTAS.
- **Multi-parameter mechanism design is hard in a precise sense.** The proof uses only weak monotonicity on small instances, which every truthful mechanism satisfies, and the authors suggest the same approach for other multi-parameter problems such as combinatorial auctions.

## Tightness

- **The bound is exact**, since VCG has ratio $n$.
- **Determinism is needed.** For two machines, Nisan and Ronen gave a universally truthful randomized mechanism with ratio $7/4 < 2$. For randomized and fractional mechanisms on $n$ machines, the known bounds are a lower bound of about 2 and an upper bound of $(n + 1)/2$, and the gap is open; see [truthful in expectation](/truthful-in-expectation/).
- **Many jobs are needed.** With a single job, VCG gives it to the fastest machine, which is optimal. The lower bound instances use multi-cliques of high multiplicity, so the number of jobs grows with the required precision.
- **Vector types are needed.** On related machines, where each machine has one private speed, truthful mechanisms get ratio $1 + \varepsilon$.
- **Anonymity was an earlier special case.** Ashlagi, Dobzinski and Lavi (2012) proved the bound $n$ for anonymous mechanisms, which treat machines symmetrically. The 2023 theorem removes this assumption.

## History

Nisan and Ronen introduced algorithmic mechanism design at STOC 1999, with the journal version in 2001. They proved that VCG has ratio $n$ and that no truthful mechanism beats 2, and conjectured that $n$ is the right answer. Progress on the lower bound was slow: $1 + \sqrt{2} \approx 2.414$ by Christodoulou, Koutsoupias and Vidali, $1 + \varphi \approx 2.618$ by Koutsoupias and Vidali, about $2.755$ by Giannakopoulos, Hammerl and Pocas, and 3 by Dobzinski and Shaulker. Christodoulou, Koutsoupias and Kovacs gave the first bound that grows with $n$, $1 + \sqrt{n - 1}$, at FOCS 2021, and proved the full conjecture at STOC 2023. The journal version appeared in the Journal of the ACM in 2026.

## References
