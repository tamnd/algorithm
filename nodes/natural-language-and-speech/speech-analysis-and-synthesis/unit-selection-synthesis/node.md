---
tag: V4WYB0
kind: algorithm
slug: unit-selection-synthesis
name: Unit selection synthesis
aliases:
- concatenative synthesis
- diphone synthesis
area: natural-language-and-speech/speech-analysis-and-synthesis
level: core
summary: "Speech synthesis that picks recorded units from a large database to minimize the sum of target costs and join costs, found by a Viterbi search over the candidates, and joins them."
solves: [text-to-speech]
model: word-ram
complexity:
  vars: {n: the number of target units, K: the number of candidates per target}
  time: {worst: "Θ(n K^2)"}
  space: {extra: "Θ(n K)"}
properties: {deterministic: true, exact: true, online: false, in_place: false}
history:
  year: 1996
  people: [Andrew J. Hunt, Alan W. Black]
  note: Hunt and Black, at ATR, framed the choice of units as a search over a state transition network with target and concatenation costs, solved by Viterbi.
prereqs: [text-to-speech, viterbi-algorithm, dag-shortest-paths]
see_also: [psola, overlap-add-method, hmm-based-speech-synthesis, mean-opinion-score, beam-search, trellis, formant-synthesis, wavenet]
sources:
  - paper: doi:10.1109/ICASSP.1996.541110
    title: Andrew J. Hunt and Alan W. Black, Unit selection in a concatenative speech synthesis system using a large speech database, ICASSP 1996, volume 1, pages 373 to 376
    locator: the target and concatenation costs, the Viterbi search over the units, and the tuning of the weights
  - book: isbn:9780521899277
    title: Paul Taylor, Text-to-Speech Synthesis, Cambridge University Press, 2009
    locator: the chapter Unit selection synthesis
  - paper: doi:10.1016/j.specom.2009.04.004
    title: Heiga Zen, Keiichi Tokuda and Alan W. Black, Statistical parametric speech synthesis, Speech Communication 51(11), 2009, pages 1039 to 1064
    locator: the comparison of unit selection with statistical parametric synthesis
  - paper: "Aäron van den Oord, Sander Dieleman, Heiga Zen, Karen Simonyan, Oriol Vinyals, Alex Graves, Nal Kalchbrenner, Andrew Senior and Koray Kavukcuoglu, WaveNet: a generative model for raw audio, arXiv:1609.03499, 2016"
    title: van den Oord et al. 2016
    locator: the subjective listening tests with the concatenative and parametric baselines
---

Unit selection synthesis makes speech for a [text-to-speech](/text-to-speech/) system by cutting pieces out of a large recorded database and joining them. For each unit of the planned utterance, usually a phone or a diphone with a target pitch and duration, many recorded candidates exist. A *target cost* measures how well a candidate fits its target, and a *join cost* measures how well two candidates fit together, and it is zero for two units that were recorded next to each other. The best sequence minimizes the sum of all these costs. It is a shortest path through a layered graph of candidates, so the [Viterbi algorithm](/viterbi-algorithm/) finds it in $\Theta(n K^2)$ time for $n$ targets and $K$ candidates each. Hunt and Black gave this formulation in 1996, and it was the most natural-sounding commercial method until neural synthesis.

## In plain words

Record one speaker reading many hours of text, and cut the recordings into small sound pieces. To say a new sentence, you need one piece for each sound. There are many recorded copies of each sound, each said with a different pitch, length and neighbors.

A good choice fits two kinds of need. Each piece should sound like what the sentence needs at that place. And each pair of pieces should join without a click or a jump in pitch. Two pieces that were next to each other in the recording join perfectly, so long stretches of the original recording are good.

Trying all choices is too slow. But the best choice up to a given sound only depends on which piece ends there. So the method goes through the sentence once, keeps the best cost for each piece at each place, and follows the links back at the end.

## The problem

The front end of the synthesizer gives a sequence of targets $t_1, \ldots, t_n$. A target names a unit type (here a phone) and the wanted prosody and context: an F0 in Hz, a duration in ms, and the left and right neighbor phones. The database holds units $u$ with the same fields, measured on the recordings, plus their recording, their position in it, and spectral vectors at their two ends, for example [MFCCs](/mel-frequency-cepstral-coefficients/).

The candidates $U_i$ for target $t_i$ are the database units of the same phone. With weights $w$, the code uses

$$TC(t, u) = w_{f0} |f_0(t) - f_0(u)| + w_{dur} |d(t) - d(u)| + w_{ctx} \bigl([\ell(t) \ne \ell(u)] + [r(t) \ne r(u)]\bigr),$$

$$JC(u, v) = \begin{cases} 0 & \text{if } v \text{ follows } u \text{ in the same recording,} \\ w_{spec} \|e(u) - s(v)\|^2 + w_{jf0} |f_0(u) - f_0(v)| & \text{otherwise,} \end{cases}$$

where $e(u)$ and $s(v)$ are the spectral vectors at the end of $u$ and the start of $v$. Hunt and Black write both costs as weighted sums of sub-costs in the same way; real systems use many more sub-costs. The task is to find $s_i \in U_i$ that minimize

$$\sum_{i=1}^{n} TC(t_i, s_i) + \sum_{i=2}^{n} JC(s_{i-1}, s_i).$$

## The algorithm

The search is Viterbi in the tropical semiring (min, +): costs are added along a path, and the minimum is taken over paths.

```pseudo id=main
UNIT-SELECTION(t_1 .. t_n, database, w, beam)
L1  for i ← 1 to n do U_i ← the database units with the phone of t_i, in database order
L2  for each u in U_1 do C_1(u) ← TC(t_1, u)
L3  for i ← 2 to n do
L4      for each u in U_i do
L5          B_i(u) ← the first kept v in U_(i-1) that minimizes C_(i-1)(v) + JC(v, u)
L6          C_i(u) ← C_(i-1)(B_i(u)) + JC(B_i(u), u) + TC(t_i, u)
L7      if a beam width is given, keep only the beam units of U_i with the smallest C_i
L8  u_n ← the first kept u in U_n that minimizes C_n(u)
L9  for i ← n downto 2 do u_(i-1) ← B_i(u_i)
L10 return u_1 .. u_n and C_n(u_n)
```

$C_i(u)$ is the least cost of a choice for $t_1, \ldots, t_i$ that ends with $u$, and $B_i(u)$ is the unit before $u$ on such a choice. Line L9 is the [traceback](/traceback/). Line L7 is optional; without it every unit is kept and the result is exact. The chosen units are then joined, usually with a short [overlap-add](/overlap-add-method/) at each join, and some systems adjust pitch and duration with [PSOLA](/psola/) when the fit is poor.

**Tie rule.** Lines L5 and L8 take the first minimizer in database order. Then the result is the optimal sequence whose reversed list of candidate indices is the smallest in lexicographic order.

## Example

Take two targets: "a" with F0 100 Hz, duration 60 ms, left neighbor silence and right neighbor "b", then "b" with 120 Hz, 70 ms, left "a" and right silence. All weights are 1, and the spectral vectors have one number. The database has three units:

| unit | recording, position | phone | F0 | duration | context | start, end vector |
|---|---|---|---|---|---|---|
| A0 | 0, 0 | a | 100 | 60 | silence, b | 0, 0 |
| A1 | 1, 0 | a | 101 | 60 | silence, b | 0, 5 |
| B1 | 1, 1 | b | 120 | 70 | a, silence | 5, 0 |

The target costs are $TC(t_1, A0) = 0$, $TC(t_1, A1) = 1$ (1 Hz off) and $TC(t_2, B1) = 0$. The join $A0 \to B1$ costs $(0 - 5)^2 + |100 - 120| = 45$. The join $A1 \to B1$ costs 0, because B1 follows A1 in recording 1. So $C_1(A0) = 0$, $C_1(A1) = 1$, and

$$C_2(B1) = \min(0 + 45,\ 1 + 0) + 0 = 1, \qquad B_2(B1) = A1.$$

The answer is A1, B1 with cost 1: a stretch of real speech wins over a better single unit with a bad join. A beam of width 1 keeps only A0 after the first target, since it has the smaller cost, and then returns A0, B1 with cost 45. This shows that the beam can lose the optimum.

## Correctness

Each choice of units is a path from a source through one candidate per layer, and its length is its total cost. The proofs file shows by induction on $i$ that $C_i(u)$ is the least cost of a choice that ends with $u$: the best choice that ends with $v \to u$ extends a best choice that ends with $v$, since the cost of the extension does not depend on the earlier units. The traceback rebuilds a choice of that cost, and the tie rule picks the stated optimum. With a beam of width at least the largest $|U_i|$ the result is the same; with a smaller beam, $C_i$ is only an upper bound and the result can be worse, as in the example. The tests check the exact search, ties included, against brute force over all $\prod_i |U_i|$ choices, and the beam case on the example.

## Complexity

Line L5 evaluates $|U_{i-1}|$ join costs for each unit of $U_i$, so the time is $\Theta(\sum_i |U_{i-1}| |U_i|)$ join cost evaluations, or $\Theta(n K^2)$ with $K$ candidates per target. The back pointers take $\Theta(n K)$ space. The brute force search takes $\Theta(n K^n)$. A large database can hold thousands of units of a common phone, so $K^2$ join costs per target are the main cost. Real systems cut $K$ by pre-selection on the phone context, cache the join costs, and prune with a beam, which gives $O(n K B)$ for a beam of width $B$.

## Properties

- **Exact for the costs.** Without pruning, the search returns a minimum of the total cost. Whether this sounds best depends on how well the costs match what listeners hear.
- **Prefers long stretches.** Since consecutive units join for free, the optimum often copies whole syllables or words from the database. This is the source of the high naturalness of the method in its domain.
- **Not online.** The best unit for an early target can depend on the last target, so the traceback needs the whole utterance. Systems with low latency run the search over a phrase at a time.
- **Bounded by the data.** The output can only use recorded speech. A target far from every recording gives a poor unit or a strong modification.
- **Fixed voice.** A new voice or speaking style needs a new database of many hours.

## Variants and improvements

- **Unit size.** Hunt and Black used phone units. Diphones (from the middle of one phone to the middle of the next) put the joins in the stable parts of phones. Half-phones and non-uniform units are also used.
- **Diphone synthesis.** The older method keeps exactly one recorded unit per diphone and changes its pitch and duration by signal processing such as [PSOLA](/psola/). It needs no search, but the output sounds more processed.
- **Pre-selection and clustering.** Group the units of each type by a [decision tree](/decision-tree/) on context and prosody, and take the candidates only from the leaf that matches the target.
- **Weight tuning.** Hunt and Black tuned the weights by comparing the selected units with natural held-out utterances under an objective distance. Later systems tuned them with listening tests.
- **Hybrid synthesis.** Use a statistical model, an HMM or a neural network, to predict the targets and score the candidates, and select natural units with this score. This combines the smoothness of [HMM-based synthesis](/hmm-based-speech-synthesis/) with real waveforms.

## When to use it

Use unit selection when one voice in a narrow domain must sound very natural and a large recorded and labeled database is affordable, for example announcements, navigation, or a product voice with a fixed set of sentence types. Use [HMM-based](/hmm-based-speech-synthesis/) or neural synthesis when you need a small footprint, many voices, control of style and prosody, or good quality on text far from the recordings. Neural vocoders such as [WaveNet](/wavenet/) and [HiFi-GAN](/hifi-gan/) behind models such as [Tacotron](/tacotron/) now give higher ratings than unit selection in most published tests. For example, in the US English test of the WaveNet paper, a concatenative system had a [mean opinion score](/mean-opinion-score/) of 3.86 ± 0.137 and WaveNet had 4.21 ± 0.081 (measurement, 100 test sentences with 8 ratings each, on a 1 to 5 scale).

## Pitfalls

- **Bad labels.** Wrong phone boundaries or pitch marks in the database give clicks and wrong sounds that no cost can see. Check the [forced alignment](/forced-alignment/) of the database.
- **Costs that do not match perception.** A low total cost does not guarantee a good result. The weights decide which sub-costs win; tune them with listeners or held-out speech.
- **Too narrow a beam.** Pruning by the cost so far drops units that are expensive alone but enable a free join, as in the example. Keep the beam wide enough to hold the long stretches.
- **Join costs for neighbors.** If the join cost of two units that are adjacent in a recording is not 0, the search loses its preference for long stretches.
- **Uneven quality.** The output is very good where the database has the right units and poor where it does not, and listeners notice the change within one sentence.

## Implementations

## History

Concatenative synthesis began with diphone systems in the 1970s and 1980s, which stored one recorded example of each diphone and changed its pitch and duration by signal processing. Andrew Hunt and Alan Black, also at ATR and working on the CHATR system, published the unit selection formulation in 1996: target costs and concatenation costs as weighted sums of sub-costs, and the best units by a Viterbi search, with the weights tuned on held-out speech. The Festival system and many commercial voices adopted it, and through the 2000s it gave the most natural synthetic speech in many evaluations. Statistical parametric synthesis offered more flexibility from the late 1990s, and neural models such as WaveNet in 2016 and Tacotron 2 in 2018 overtook unit selection in listening tests.

## References
