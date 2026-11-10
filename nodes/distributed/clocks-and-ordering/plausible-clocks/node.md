---
tag: DY2814
kind: data-structure
slug: plausible-clocks
name: Plausible clocks
aliases:
- R-entry vector clocks
area: distributed/clocks-and-ordering
level: research
summary: Logical clocks of fixed size that never miss or reverse a happened-before pair, but may order some concurrent events. REV, KLA and their product Comb are the main examples.
model: asynchronous-model
complexity:
  vars: {n: the number of sites, r: the number of entries of the clock}
  time: {worst: Θ(r)}
  space: {extra: Θ(r)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1996
  people: [Francisco J. Torres-Rojas, Mustaque Ahamad]
  note: Torres-Rojas and Ahamad defined plausible clocks at WDAG 1996, with a journal version in Distributed Computing in 1999.
prereqs: [vector-clocks, lamport-clocks, happened-before]
see_also: [vector-clocks, lamport-clock-condition, concurrent-events, interval-tree-clocks, version-vectors]
sources:
  - paper: doi:10.1007/s004460050065
    title: Francisco J. Torres-Rojas and Mustaque Ahamad, Plausible clocks, constant size logical clocks for distributed systems, Distributed Computing 12(4), 1999
    locator: pages 179 to 195
  - paper: doi:10.1007/3-540-61769-8_6
    title: Francisco J. Torres-Rojas and Mustaque Ahamad, Plausible clocks, constant size logical clocks for distributed systems, WDAG 1996, LNCS 1151
    locator: pages 71 to 88
  - url: "https://clei.org/proceedings_data/CLEI2000/PDFClei/a000043.pdf"
    title: Francisco J. Torres-Rojas and Esteban Castro-Mora, Partially ordered sets and logical clocks for distributed systems, CLEI 2000
    locator: Definition 10 (plausible clock), Definition 11 (REV), Definition 12 (KLA) and Definition 13 (Comb)
  - paper: doi:10.1016/0020-0190(91)90055-M
    title: Bernadette Charron-Bost, Concerning the size of logical clocks in distributed systems, Information Processing Letters 39(1), 1991
    locator: pages 11 to 16 (exact clocks need n entries)
---

A plausible clock is a logical clock of fixed size whose order never contradicts [happened-before](/happened-before/): if $a \to b$, the clock reports $a$ before $b$, and it never reports $b$ before $a$. It is allowed to report an order between two [concurrent events](/concurrent-events/). Exact clocks need $n$ entries for $n$ sites, so a plausible clock trades accuracy on concurrent pairs for a size that does not grow with $n$. Torres-Rojas and Ahamad defined the notion and gave the clocks REV, KLA and Comb.

## In plain words

A [vector clock](/vector-clocks/) has one counter for each computer, so it gets big in a big system. A plausible clock keeps a fixed, small number of counters.

The price is that it sometimes says "this event came first" about two events that had nothing to do with each other. It never makes the other two mistakes: it never says that two related events are unrelated, and it never puts two related events in the wrong order. So when it says "unrelated", you can trust it.

One version shares counters: many computers use the same counter, chosen by their number. Another version keeps an ordinary Lamport counter plus a short memory of the counters it heard from others. A third version runs both and believes an order only when both agree.

## The abstract type

The setting is the [asynchronous model](/asynchronous-model/) with $n$ sites, point-to-point channels that need not be FIFO, and no failure assumption. The paper writes $N$ for the number of sites. A clock gives each event $e$ a stamp, and it has a relation $\to_P$ on stamps. Following Torres-Rojas and Castro-Mora (Definition 10), the clock is plausible if for all events $a$ and $b$:

$$a = b \iff a =_P b \qquad \text{and} \qquad a \to b \implies a \to_P b.$$

The clocks below also never report a pair in both directions. Together these give: a causal pair is reported with its true direction, and a pair reported as concurrent is concurrent. The only error is a concurrent pair reported as ordered. [Lamport clocks](/lamport-clocks/) with the process tie-break are plausible in this sense, and they report no pair as concurrent at all.

## Representation

- **REV** (R-entries vector, Definition 11). A vector $V[0 \ldots R-1]$ with $1 \le R \le n$. Site $i$ uses entry $\rho(i) = i \bmod R$. A stamp is the pair $\langle i, V \rangle$.
- **KLA** (K-Lamport, Definition 12). A vector $V[0 \ldots K-1]$ with $K \ge 2$. Entry 0 is a [Lamport clock](/lamport-clocks/). Entry $k \ge 1$ is the largest entry $k-1$ that the site has received in a message.
- **Comb** (Definition 13). One REV stamp and one KLA stamp side by side.

## Operations

The REV clock of site $p_i$:

```pseudo id=main
REV-CLOCK at site p_i, with R entries
L1  V ← (0, …, 0)                              ▷ R entries

TICK()
L2  V[i mod R] ← V[i mod R] + 1
L3  return ⟨i, a copy of V⟩

SEND(m)
L4  attach t ← TICK() to m, and send m

RECEIVE(m)                                     ▷ m carries ⟨j, W⟩
L5  for k ← 0 to R − 1 do
L6      V[k] ← max(V[k], W[k])
L7  return TICK()

BEFORE(⟨s, V⟩, ⟨t, W⟩)                          ▷ the relation →_P
L8  if s = t then return V[s mod R] < W[t mod R]
L9  return V ≤ W entrywise and V[t mod R] < W[t mod R]
```

The KLA clock of site $p_i$ and the Comb test:

```pseudo id=kla
KLA-CLOCK at site p_i, with K entries
    V ← (0, …, 0)                              ▷ K entries
TICK() and SEND: V[0] ← V[0] + 1, return ⟨i, a copy of V⟩
RECEIVE(m)                                     ▷ m carries ⟨j, W⟩
    V'[0] ← max(V[0], W[0]) + 1
    for k ← 1 to K − 1 do V'[k] ← max(V[k], W[k − 1])
    V ← V', return ⟨i, a copy of V⟩
BEFORE(⟨s, V⟩, ⟨t, W⟩)
    if s = t then return V[0] < W[0]
    return V[k] ≤ W[k + 1] for each k from 0 to K − 2

COMB-BEFORE(a, b)
    return REV-BEFORE(a, b) and KLA-BEFORE(a, b)
```

With $R = n$, REV is the vector clock, and the test of line L9 is the exact test of happened-before. With $R = 1$, REV is close to a Lamport clock.

## Example

Three sites $P_1$, $P_2$ and $P_3$, numbered 0, 1 and 2, run seven events. $P_1$ sends a message to $P_2$ (event $a$) and then does a local event $b$. $P_2$ does a local event $c$, receives the message of $a$ (event $d$) and sends a message to $P_3$ (event $e$). $P_3$ does a local event $f$ and receives the message of $e$ (event $g$). REV uses $R = 2$, so $P_1$ and $P_3$ share entry 0. KLA uses $K = 3$.

| event | site | REV stamp | KLA stamp |
|---|---|---|---|
| $a$ | 0 | $\langle 0, (1, 0) \rangle$ | $\langle 0, (1, 0, 0) \rangle$ |
| $b$ | 0 | $\langle 0, (2, 0) \rangle$ | $\langle 0, (2, 0, 0) \rangle$ |
| $c$ | 1 | $\langle 1, (0, 1) \rangle$ | $\langle 1, (1, 0, 0) \rangle$ |
| $d$ | 1 | $\langle 1, (1, 2) \rangle$ | $\langle 1, (2, 1, 0) \rangle$ |
| $e$ | 1 | $\langle 1, (1, 3) \rangle$ | $\langle 1, (3, 1, 0) \rangle$ |
| $f$ | 2 | $\langle 2, (1, 0) \rangle$ | $\langle 2, (1, 0, 0) \rangle$ |
| $g$ | 2 | $\langle 2, (2, 3) \rangle$ | $\langle 2, (4, 3, 1) \rangle$ |

The events $f$ and $b$ are concurrent. REV reports $f \to_P b$: the sites differ, $(1, 0) \le (2, 0)$, and entry $0 \bmod 2 = 0$ gives $1 < 2$. The reason is that $f$ ticked the entry that $P_3$ shares with $P_1$. KLA does not order the pair: $f \to_P b$ would need $1 \le 0$ in the first test, and $b \to_P f$ would need $2 \le 0$. So Comb reports $f \parallel b$, which is correct. For the causal pair $a \to g$, REV gives $(1,0) \le (2,3)$ with $1 < 2$ in entry 0, and KLA gives $1 \le 3$ and $0 \le 1$, so all three clocks report $a \to_P g$.

## Correctness

For REV, the vectors grow entrywise along every chain of happened-before, as for a vector clock. When $a \to b$ and $b$ is on site $j$, the tick of $b$ makes entry $j \bmod R$ larger than in $a$, which is the second test of line L9. For KLA, entry 0 is a Lamport clock. Each message moves the entries one place to the right at the receiver, so if $a \to b$ through a chain whose last message arrives on the site of $b$, each entry $k$ of $a$ is at most entry $k+1$ of $b$. Each state of KLA is non-increasing from entry 0 to entry $K-1$, which rules out an order in both directions. Comb inherits both properties. The full proofs are below.

## Complexity

| clock | time per event | stamp size | comparison |
|---|---|---|---|
| REV | $\Theta(R)$ | $R$ integers and a site number | $\Theta(R)$ |
| KLA | $\Theta(K)$ | $K$ integers and a site number | $\Theta(K)$ |
| Comb | $\Theta(R + K)$ | $R + K$ integers and a site number | $\Theta(R + K)$ |
| vector clock | $\Theta(n)$ | $n$ integers | $\Theta(n)$ |

No plausible clock of size less than $n$ can be exact on every run. Charron-Bost proved that an exact characterization of happened-before by vectors ordered entrywise needs $n$ entries. The proof is on the [clock condition](/lamport-clock-condition/) page. So the false orders of REV, KLA and Comb on some concurrent pairs are a necessary cost of the fixed size, not a weakness of these particular rules.

## Variants

- **Choice of $R$ and $K$.** A larger $R$ makes fewer sites share each entry of REV. A larger $K$ lets KLA remember more hops. Torres-Rojas and Ahamad measured the accuracy of the clocks by simulation.
- **Other products.** Any two plausible clocks give a plausible product clock by the same conjunction rule, and the product is at least as accurate as each part.
- **Exact but adaptive clocks.** [Interval tree clocks](/interval-tree-clocks/) stay exact and change size with the number of active participants, instead of using a fixed size.

## When to use it

Use a plausible clock when the number of sites is large or unknown, the stamps must have a fixed size, and the use tolerates a false order between concurrent events. It suits a use in which a false order between concurrent events costs only extra waiting or extra work, because every true order is still seen. It is not safe for a use that must find every concurrent pair, such as conflict detection for replicated writes, because it misses some conflicts.

## Pitfalls

- **Trusting a reported order.** $a \to_P b$ does not prove $a \to b$. Only a reported concurrency, and an order between two events of the same site, is certain.
- **Sharing entries badly in REV.** Sites that talk to each other rarely but share an entry produce many false orders. The paper uses the rule $i \bmod R$, and the proofs hold for any fixed map from sites to entries.
- **Mixing parameters.** Two stamps are comparable only if they come from clocks with the same $R$ and $K$.
- **Using it to find conflicts.** For replicated data, use [version vectors](/version-vectors/) or [dotted version vectors](/dotted-version-vectors/), which are exact on the replicas.

## Implementations

## History

Francisco Torres-Rojas and Mustaque Ahamad introduced plausible clocks at WDAG 1996, and published the journal version in Distributed Computing in 1999. They gave REV, KLA and their product, and studied their accuracy by simulation. Torres-Rojas and Castro-Mora restated the definitions in terms of partially ordered sets at CLEI 2000. The motivation is the bound of Charron-Bost from 1991, which shows that exact vector-like clocks need one entry per site.

## References
