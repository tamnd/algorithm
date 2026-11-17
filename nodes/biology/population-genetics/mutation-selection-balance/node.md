---
tag: 9418YH
kind: theorem
slug: mutation-selection-balance
name: Mutation-selection balance
aliases:
- mutation-selection equilibrium
area: biology/population-genetics
level: core
summary: "A deleterious allele with recurrent mutation at rate u settles near frequency u/(hs) when partly dominant, u/s when dominant (h = 1) and sqrt(u/s) when recessive (h = 0)."
prereqs: [hardy-weinberg-principle]
see_also: [hardy-weinberg-principle, allele-frequency, genetic-drift, kimura-fixation-probability, wright-fisher-model, replicator-dynamics, fixed-point-iteration, quadratic-formula]
sources:
  - paper: doi:10.1017/S0305004100015644
    title: J. B. S. Haldane, A mathematical theory of natural and artificial selection, Part V, Selection and mutation, Proceedings of the Cambridge Philosophical Society 23(7), 1927
    locator: pp. 838-844 (the equilibrium frequencies of a deleterious allele under recurrent mutation, for dominant and recessive alleles)
  - paper: doi:10.1086/280722
    title: J. B. S. Haldane, The effect of variation on fitness, The American Naturalist 71(735), 1937
    locator: pp. 337-349 (the loss of fitness at mutation-selection balance, which does not depend on s)
  - book: isbn:9780801880094
    title: John H. Gillespie, Population Genetics, A Concise Guide, 2nd edition, Johns Hopkins University Press, 2004
    locator: Section 3.4 (mutation-selection balance) and Section 3.5 (the mutation load)
  - book: isbn:9780387201917
    title: Warren J. Ewens, Mathematical Population Genetics I, Theoretical Introduction, 2nd edition, Springer, 2004
    locator: Section 2.11 (genetic loads, p. 78)
---

Mutation-selection balance is the equilibrium between mutation, which keeps making a harmful allele, and selection, which keeps removing it. At the balance, the frequency of the allele is small, and how small depends on its dominance: about $u/(hs)$ when the heterozygote is partly affected, $u/s$ when the allele is dominant and $\sqrt{u/s}$ when it is recessive. These are first-order approximations in an infinite population, and this page says when they hold.

## Statement

**The setting.** One autosomal locus in an infinite diploid population with random mating and discrete generations, so each generation starts in [Hardy-Weinberg](/hardy-weinberg-principle/) proportions. The normal allele $A$ mutates to the deleterious allele $a$ at rate $u$ per copy per generation, with no back mutation. The genotypes $AA$, $Aa$ and $aa$ have fitnesses $1$, $1 - hs$ and $1 - s$, with $0 < s \le 1$ and $0 \le h \le 1$ ($h$ is the dominance of $a$). In each generation selection acts first and then mutation. Write $q$ for the frequency of $a$ and $p = 1 - q$.

**Theorem.** (a) The change of $q$ in one generation is exactly

$$\Delta q = \frac{p\,F(q)}{\bar w}, \qquad F(q) = u - hs(1 + u)\,q - s(1 - 2h)\,q^2,$$

with $\bar w = 1 - 2pqhs - q^2 s$ the mean fitness. So the equilibria in $(0, 1)$ are the roots of $F$, and the smallest positive root

$$q^* = \frac{2u}{b + \sqrt{b^2 + 4au}}, \qquad a = s(1 - 2h), \quad b = hs(1 + u),$$

is stable: $\Delta q > 0$ below it and $\Delta q < 0$ just above it. For $h \le 1/2$, $q$ tends to $q^*$ from every start in $[0, 1)$.

(b) To first order:

- if $h > 0$ and $u \ll h^2 s$, then $q^* \approx u/(hs)$ (partial dominance; $u/s$ for $h = 1$);
- if $h = 0$, then $q^* = \sqrt{u/s}$ exactly.

(c) The mutation load $L = 1 - \bar w$ at $q^*$ is about $2u$ when $h > 0$ and $u \ll h^2 s$, and exactly $u$ when $h = 0$. It does not depend on $s$ (Haldane 1937).

## In plain words

Some gene variants harm their carriers, but new copies keep appearing by mutation. Selection removes the harmful copies, mutation adds new ones, and the two come into balance. If the variant does harm in a single copy, carriers lose fitness at once and selection removes it quickly, so it stays very rare. If it does harm only in two copies, most copies hide in healthy carriers, where selection cannot see them, so the variant stays much more common. A surprising result: the total cost to the population depends only on how often the mutation happens, not on how harmful it is. A very harmful variant is rarer, a mild one is more common, and the two effects cancel.

## Proof

**(a)** After selection, the frequency of $a$ is $q_s = (q^2(1 - s) + pq(1 - hs))/\bar w = q(1 - sq - hsp)/\bar w$. A short computation gives

$$q - q_s = \frac{pq\,s\,(h + (1 - 2h)q)}{\bar w}, \qquad 1 - q_s = \frac{p\,(1 - hsq)}{\bar w}.$$

Mutation then makes $q' = q_s + u(1 - q_s)$, so

$$\Delta q = q' - q = u(1 - q_s) - (q - q_s) = \frac{p}{\bar w}\Big(u(1 - hsq) - sq\,(h + (1 - 2h)q)\Big) = \frac{p\,F(q)}{\bar w}.$$

Since $p > 0$ and $\bar w > 0$ on $[0, 1)$, the sign of $\Delta q$ is the sign of $F(q)$. $F(0) = u > 0$, so $q$ grows from 0. The root $q^*$ is the smallest positive root of $u - bq - aq^2$ (the [quadratic formula](/quadratic-formula/), written in the form that is stable for small $u$), and $F$ changes sign from $+$ to $-$ there, so $q^*$ is stable. For $h \le 1/2$, $a \ge 0$, so $F$ is decreasing on $[0, 1]$ and has only this root there. The map $q \mapsto q' = u + (1 - u)q_s$ is increasing: $\ln(q_s/(1 - q_s)) = \ln(q/p) + \ln(1 - hs - s(1 - h)q) - \ln(1 - hsq)$, and the derivative of the middle term is at least $-1/p$, because $1 - hs - s(1 - h)q \ge s(1 - h)p$. So $q_t$ never jumps over $q^*$; it is monotone and bounded, and it tends to a fixed point, which can only be $q^*$.

**(b)** For $h = 0$, $a = s$ and $b = 0$, so $F(q) = u - sq^2$ and $q^* = \sqrt{u/s}$ exactly. For $h > 0$, write $q^* = (u/b) \cdot 2/(1 + \sqrt{1 + 4au/b^2})$. If $4au/b^2 \approx 4u(1 - 2h)/(h^2 s)$ is small, the second factor is close to 1, and $q^* \approx u/b \approx u/(hs)$. This is the condition $u \ll h^2 s$: it says that the term $aq^2$ is small next to $bq$, which means $q^* \ll h$, so that selection on heterozygotes is stronger than selection on homozygotes.

**(c)** $L = 2pqhs + q^2 s$. For $h > 0$ with $q^* \approx u/(hs)$, $L \approx 2q^* hs = 2u$, up to terms of order $q^*$. For $h = 0$, $L = s\,q^{*2} = u$. $\square$

## Consequences

**Values.** With $u = 10^{-5}$ and $s = 0.1$, the exact root $q^*$, the first-order value and the load are:

| $h$ | exact $q^*$ | first order | load $L$ |
|---|---|---|---|
| 1 (dominant) | $0.000100009$ | $u/s = 0.0001$ | $2.0 \times 10^{-5}$ |
| 0.5 (additive) | $0.000199998$ | $u/(hs) = 0.0002$ | $2.0 \times 10^{-5}$ |
| 0.2 | $0.000499247$ | $0.0005$ | $2.0 \times 10^{-5}$ |
| 0 (recessive) | $0.01$ | $\sqrt{u/s} = 0.01$ | $1.0 \times 10^{-5}$ |

Iterating $q \mapsto q'$ from $q = 0$ reaches these values; this is a [fixed-point iteration](/fixed-point-iteration/). It takes about 450 generations for $h = 1/2$ and about 12000 for $h = 0$, because selection on a rare recessive allele is very weak.

**Recessive alleles are much more common.** The recessive allele is 50 times more common than the additive one here. Most copies of a rare recessive allele are in heterozygotes, which selection does not see. This explains why carriers of recessive diseases are common while affected individuals are rare: with $q = 0.01$, one person in 50 is a carrier and one in 10000 is affected.

**The load does not depend on s.** When $h > 0$, almost every mutant copy is removed in a heterozygote, so each new mutation costs one genetic death, and an individual carries $2u$ new mutations per generation at this locus. When $h = 0$, each death of an $aa$ individual removes two copies, so the cost is $u$. Summed over many loci, this gives the total mutation load of a population.

**Estimating mutation rates.** For a dominant disease with known fitness of carriers, $u \approx hs\,q^*$ gives the mutation rate from the frequency of the disease. Haldane (1935) used a form of this argument for an X-linked gene to estimate the mutation rate of haemophilia.

## Tightness

**Weak dominance.** The value $u/(hs)$ needs $u \ll h^2 s$. When $h$ is small but not 0, this fails, and the true value is between $u/(hs)$ and $\sqrt{u/s}$. With $u = 10^{-5}$ and $s = 0.1$:

| $h$ | $h^2 s$ | exact $q^*$ | $u/(hs)$ | $\sqrt{u/s}$ |
|---|---|---|---|---|
| 0.02 | $4 \times 10^{-5}$ | $0.004167$ | $0.005$ | $0.01$ |
| 0.01 | $10^{-5}$ | $0.006215$ | $0.01$ | $0.01$ |
| 0.001 | $10^{-7}$ | $0.009522$ | $0.1$ | $0.01$ |

At $h = 0.02$, $u/(hs)$ is 20 percent too high; at $h = 0.001$ it is 10 times too high, and $\sqrt{u/s}$ is the better value. The load is $1.83 \times 10^{-5}$ for $h = 0.02$, between $u$ and $2u$.

**Dominant alleles and a second root.** For $h > 1/2$, $a < 0$, and $F$ can have a second root in $(0, 1)$. For $h = 1$ it is near $1 - u/s$: if $a$ is almost fixed, an $A$ allele is not better in a heterozygote than $aa$, and mutation pushes $q$ to 1. So for $h = 1$ the frequency tends to $q^*$ only from starts below this second root.

**Finite populations.** The theorem is deterministic. In a population of $N$ diploids there are only $2Nq^*$ copies, and [genetic drift](/genetic-drift/) moves $q$ around $q^*$. For a recessive allele, selection at frequency $q$ acts with the strength $sq$, so drift dominates when $2Nsq^*$ is below about 1, which is $N < 1/(2\sqrt{us}) = 500$ in the example above. Then the frequency fluctuates widely and its mean differs from $\sqrt{u/s}$.

**Other assumptions.** Back mutation, migration, inbreeding (which exposes recessive alleles and lowers $q^*$) and heterozygote advantage each change the result. The order of selection and mutation changes only terms of order $u^2$.

## History

Haldane (1927) found the equilibria $u/s$ for a dominant and $\sqrt{u/s}$ for a recessive harmful allele. Haldane (1937) showed that the loss of fitness at the balance is about the mutation rate, whatever $s$ is. Muller (1950) used this to argue that the human population carries a large total load of mutations, and the mutation load became a central idea of population genetics.

## References
