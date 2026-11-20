---
tag: J42M0N
kind: concept
slug: bidding-languages
name: Bidding languages
aliases:
- OR bids
- XOR bids
area: algorithmic-game-theory/auctions
level: advanced
summary: "Ways to describe a valuation on bundles with a few atomic package bids combined by OR and XOR. They trade how many valuations they can express against how short the description is."
prereqs: [combinatorial-auction]
see_also: [winner-determination-problem, demand-query, single-minded-bidder-mechanism, submodular-function, communication-complexity, set-packing, simultaneous-ascending-auction, gross-substitutes]
sources:
  - paper: "Noam Nisan, Bidding and allocation in combinatorial auctions, Proceedings of the 2nd ACM Conference on Electronic Commerce (EC 2000), 1-12"
    locator: the OR, XOR, OR-of-XOR and XOR-of-OR languages, the OR* language with dummy items, and the comparison of their expressive power and size
  - book: isbn:9780521872829
    title: "Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007"
    locator: Chapter 11 (Blumrosen and Nisan, Combinatorial auctions), Section 11.4 (bidding languages)
  - book: isbn:9780262033428
    title: "Peter Cramton, Yoav Shoham and Richard Steinberg (eds.), Combinatorial Auctions, MIT Press, 2006"
    locator: Chapter 9 (Nisan, Bidding languages for combinatorial auctions)
---

A bidding language is a way for a bidder in a [combinatorial auction](/combinatorial-auction/) to describe its valuation without listing a number for each of the $2^m$ bundles. The building block is an *atomic bid* $(S, p)$: the bidder will pay $p$ for the bundle $S$. Atomic bids are combined with two rules. An **OR** of bids means that the bidder may win any number of them with disjoint bundles and pays the sum. An **XOR** means that it may win at most one. XOR can describe every valuation but may need exponentially many atoms; OR is short for additive valuations but cannot describe substitutes. Richer languages mix the two, and the *OR\** language adds dummy items to get the power of XOR with the short form of OR. The choice of language decides both what bidders can say and how hard the [winner determination problem](/winner-determination-problem/) becomes.

## In plain words

A buyer in a package auction may care about many combinations of items, far too many to price one by one. A bidding language lets it write a few simple offers, each for one group of items at one price, and say how the offers combine. With "or", the auctioneer may accept any of the offers that do not overlap and add up the prices. With "exclusive or", it may accept only one of them. "Or" is good for items whose values just add up. "Exclusive or" can say anything, but sometimes only with a very long list. Mixing the two, or adding fake items that mark offers as conflicting, gives short and flexible bids.

## The idea

Let $M$ be the set of $m$ items. An atomic bid $(S, p)$ defines the single-minded valuation $v(T) = p$ if $S \subseteq T$ and $0$ otherwise. For valuations $u$ and $w$:

- **OR:** $(u \lor w)(T) = \max \{ u(R) + w(T \setminus R) : R \subseteq T \}$. The bidder may get a bundle for each part, on disjoint items.
- **XOR:** $(u \oplus w)(T) = \max(u(T), w(T))$. The bidder gets the better of the two.

An OR bid is an OR of atoms and an XOR bid is an XOR of atoms. The size of a bid is its number of atoms. Known facts (Nisan 2000):

- **XOR is complete.** Every monotone valuation is the XOR of the atoms $(S, v(S))$ for all nonempty $S$, so at most $2^m - 1$ atoms.
- **OR is not complete.** An OR bid always has $v(S \cup T) \ge v(S) + v(T)$ for disjoint $S$ and $T$, so it cannot express any substitutes. The valuations that OR bids express are exactly those with no substitutabilities.
- **The two languages are not comparable in size.** The additive valuation on $m$ items needs $m$ atoms in OR and $2^m - 1$ in XOR. The unit-demand valuation $v(S) = \max_{j \in S} v_j$ needs $m$ atoms in XOR and cannot be written in OR at all.
- **Combinations.** OR-of-XORs and XOR-of-ORs mix the two, and each is short for valuations where the other is long. Some valuations, such as the symmetric valuation that is 1 for any bundle of at least $m/2$ items, cannot be written in polynomial size in any of these languages.
- **OR\*.** OR bids over the items and some *dummy items*. A dummy item appears in several atoms and makes them conflict, so OR\* can express XOR, and any OR-of-XOR or XOR-of-OR bid, with size close to the size of the original. The winner determination algorithm treats dummy items like real ones.

## Examples

**Additive.** Values $3$ for $a$ and $2$ for $b$. OR bid: $(\{a\}, 3) \lor (\{b\}, 2)$, two atoms. XOR bid: $(\{a\}, 3) \oplus (\{b\}, 2) \oplus (\{a, b\}, 5)$, three atoms.

**Unit demand.** The bidder wants one of $a$ or $b$, at $3$ or $2$. XOR bid: $(\{a\}, 3) \oplus (\{b\}, 2)$. An OR bid with the same atoms gives 5 for $\{a, b\}$, which is wrong.

**OR\* for unit demand.** Add a dummy item $d$ and bid $(\{a, d\}, 3) \lor (\{b, d\}, 2)$. The two atoms share $d$, so at most one wins, as in the XOR bid.

**Complements.** A bidder that values $\{a, b\}$ at 10 and each single item at 0 uses one atom $(\{a, b\}, 10)$ in either language.

## Where it is used

- **Winner determination.** The language fixes the input of the [winner determination problem](/winner-determination-problem/). OR\* bids turn every case into plain weighted [set packing](/set-packing/).
- **Package auctions in practice.** Spectrum and procurement auctions let bidders submit lists of package bids, usually with an XOR rule, and some add a few logical rules.
- **Single-minded mechanisms.** A single atom is the language of the [Lehmann-O'Callaghan-Shoham mechanism](/single-minded-bidder-mechanism/).
- **Lower bounds.** The sizes of bids in a language and the number of [queries](/demand-query/) needed to learn a valuation are tools for [communication complexity](/communication-complexity/) bounds on combinatorial auctions.

## References
