---
tag: 0BNE6X
kind: model
slug: overhand-shuffle-model
name: Overhand shuffle model
aliases:
- overhand shuffle
- Pemantle overhand model
area: randomized/shuffling
level: advanced
summary: Model of the overhand shuffle. Cut between each two adjacent cards with probability p, then reverse the order of the packets. It needs order n² log n shuffles to mix (Pemantle, Jonasson).
prereqs: [markov-chain, total-variation-distance, mixing-time]
see_also: [card-shuffling, gilbert-shannon-reeds-model, bayer-diaconis-theorem, top-to-random-shuffle, random-transposition-shuffle, strong-uniform-time, spectral-gap, geometric-distribution]
sources:
  - paper: "Robin Pemantle, Randomization time for the overhand shuffle, Journal of Theoretical Probability 2(1), 1989"
    locator: pp. 37 to 50; the model with independent cuts and the bounds of order n² log n above and n² below (theorem numbers to be checked)
  - paper: "Johan Jonasson, The overhand shuffle mixes in Θ(n² log n) steps, Annals of Applied Probability 16(1), 2006"
    locator: pp. 231 to 243; the lower bound of order n² log n by Wilson's eigenfunction method
  - paper: "David Bruce Wilson, Mixing times of lozenge tiling and card shuffling Markov chains, Annals of Applied Probability 14(1), 2004"
    locator: pp. 274 to 325; the eigenfunction lower bound lemma that Jonasson uses (to be checked)
  - book: "Persi Diaconis, Group Representations in Probability and Statistics, Institute of Mathematical Statistics Lecture Notes, Monograph Series, volume 11, 1988"
    locator: Chapter 4 (overhand shuffles among other shuffles) (to be checked)
---

The overhand shuffle is the shuffle in which a person holds the deck in one hand and slides small packets off the top into the other hand, one after another, so that the packets land in reverse order. The standard model, studied by Pemantle in 1989, cuts the deck between each two adjacent cards independently with a fixed probability $p$ and then reverses the order of the packets, keeping the order inside each packet. Cards that are next to each other tend to stay next to each other, so the shuffle is slow: it needs order $n^2 \log n$ shuffles to bring a deck of $n$ cards close to uniform. Pemantle proved the upper bound and a lower bound of order $n^2$, and Jonasson proved the matching lower bound of order $n^2 \log n$ in 2006. Compare with about $\frac32 \log_2 n$ riffle shuffles in the [Gilbert-Shannon-Reeds model](/gilbert-shannon-reeds-model/).

## The machine

The state is an order of a deck of $n$ cards, with the top card first. A shuffle with parameter $p \in (0, 1)$ is the following random step.

1. For each of the $n - 1$ gaps between adjacent cards, make a cut with probability $p$, independently. The cuts split the deck into packets of consecutive cards.
2. Put the packets in reverse order, top packet last, without changing the order inside any packet.

The packet sizes are [geometric](/geometric-distribution/) with mean about $1/p$, truncated at the bottom of the deck. With $p = 1$ every packet is one card and the shuffle reverses the deck; with $p$ near 0 the deck hardly changes. A human overhand shuffle moves packets of several cards, which corresponds to a small $p$.

**Example.** Deck $0\,1\,2\,3\,4\,5$ with cuts after cards 1 and 4. The packets are $(0\,1)$, $(2\,3\,4)$, $(5)$, and the new deck is $5\,2\,3\,4\,0\,1$.

**Three cards, $p = \frac12$.** The four cut patterns give the orders $0\,1\,2$ (no cut), $1\,2\,0$ (a cut after 0), $2\,0\,1$ (a cut after 1) and $2\,1\,0$ (both cuts), each with probability $\frac14$. Exact enumeration gives $d(t) = \frac13, \frac18, \frac1{16}, \frac1{32}$ for $t = 1$ to 4.

The step does not depend on the state, so the model is a random walk on the [symmetric group](/symmetric-group/). The step law is symmetric: the inverse of the move with cut set $C$ is the move with the mirrored cut set, which has the same probability. So the chain is reversible with respect to the uniform law.

## What it counts

The model counts **shuffles**, the number $t$ of steps, and measures the [total variation distance](/total-variation-distance/) $d(t)$ between the law of the deck and the uniform law, as for the other models of [card shuffling](/card-shuffling/). The parameter $p$ is fixed while $n$ grows, and the constants in the bounds depend on $p$.

## Relation to other models

- **Riffle shuffles** ([GSR model](/gilbert-shannon-reeds-model/)) interleave two packets and separate almost all neighbours in one step. Overhand shuffles never interleave, and a pair of neighbours stays together unless a cut falls between them. That is the reason for $n^2 \log n$ against $\log n$.
- **[Top-to-random](/top-to-random-shuffle/)** and **[random transpositions](/random-transposition-shuffle/)** move one or two cards a long way per step and need order $n \log n$ steps. An overhand shuffle moves many cards, but each card moves to about the mirror of its position plus a small random shift, so one card's position spreads only like a random walk.
- **Adjacent transpositions**, which swap a random pair of neighbours, are slower still, of order $n^3 \log n$ steps (Wilson 2004; to be checked). Wilson's eigenfunction method for that chain is the method Jonasson used for the overhand lower bound.
- **Reversal moves.** With $p = 1$ the step is the fixed reversal and never mixes; the randomness of the cut positions is what mixes the deck.

## Known results in the model

**Pemantle (1989).** For fixed $p$, order $n^2 \log n$ shuffles suffice, and at least order $n^2$ shuffles are necessary.

**Jonasson (2006).** For fixed $p$, at least order $n^2 \log n$ shuffles are necessary. With Pemantle's upper bound, the mixing time is $\Theta(n^2 \log n)$. Whether there is a cutoff is not settled on this page.

**Why order $n^2$: one card.** A card at position $x$ (counting from 0 at the top) is in a packet that reaches $A$ cards above it and $B$ cards below it, with $A$ and $B$ independent truncated geometric variables. After the reversal its position is
$$n - 1 - x + (A - B).$$
So the position is reflected and then moved by a random shift with mean near 0 and variance of order $1/p^2$. After two shuffles the reflections cancel, and the position does a random walk with steps of constant size. Such a walk needs order $n^2$ steps to spread over $n$ positions. The law of the whole deck is at least as far from uniform as the law of the position of one card, so $d(t)$ is near 1 for $t$ much less than $n^2$. This is the idea of Pemantle's lower bound of order $n^2$; the factor $\log n$ comes from the need to mix all $n$ cards at once, and it needs Jonasson's finer argument.

**Exact numbers for one card, recomputed.** The law of the position of the top card was computed exactly (in floating point) from the formula above with $p = \frac12$. The table gives the first $t$ at which its distance to the uniform law on positions is below $\frac14$; this is a lower bound on the number of shuffles for the whole deck.

| $n$ | 13 | 26 | 52 | 104 |
|---|---|---|---|---|
| first $t$ with one-card distance $< \frac14$ | 9 | 33 | 129 | 514 |
| $t / n^2$ | 0.053 | 0.049 | 0.048 | 0.048 |

The ratio $t / n^2$ is nearly constant, as the random-walk picture predicts. So with $p = \frac12$, packets of 2 cards on average, a 52-card deck needs well over 100 overhand shuffles even for the top card alone, against 7 to 9 riffle shuffles. Real overhand shuffles use larger packets, a smaller $p$, which is slower.

**Exact numbers for whole small decks.** With $p = \frac12$, exact enumeration over all orders gives the first $t$ with $d(t) < \frac14$: 2 shuffles for $n = 3$ and $n = 4$, 3 for $n = 5$, and 4 for $n = 6$ ($d = 0.9556, 0.5248, 0.3096, 0.1855$ at $t = 1$ to 4). Such small decks are far from the asymptotic range.

## References
