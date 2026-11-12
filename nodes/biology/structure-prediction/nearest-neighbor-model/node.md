---
tag: GM70KW
kind: model
slug: nearest-neighbor-model
name: Nearest-neighbor thermodynamic model
aliases:
- Turner model
- Nearest-neighbor energy model
- Turner 2004 parameters
- Loop energy model
area: biology/structure-prediction
level: advanced
summary: Energy model that gives the folding free energy of an RNA secondary structure as a sum of terms for its loops, with stacks of neighbor base pairs as the main term.
history:
  year: 1998
  people: [Douglas H. Turner, Tianbing Xia, David H. Mathews, Michael Zuker]
  note: Loop energies go back to Tinoco and others in the 1970s. Xia and others measured the Watson-Crick stacks in 1998, Mathews and others gave the 1999 and 2004 parameter sets, and the NNDB database collects them.
prereqs: [rna-secondary-structure]
see_also: [zuker-algorithm, mccaskill-algorithm, nussinov-algorithm, energy-function, energy-landscape, thermodynamic-hypothesis, rna-pseudoknot-prediction, rna-folding-kinetics]
sources:
  - paper: doi:10.1021/bi9809425
    title: Tianbing Xia, John SantaLucia Jr., Mark E. Burkard, Ryszard Kierzek, Susan J. Schroeder, Xiaoqi Jiao, Christopher Cox and Douglas H. Turner, Thermodynamic parameters for an expanded nearest-neighbor model for formation of RNA duplexes with Watson-Crick base pairs, Biochemistry 37(42), 1998, pages 14719 to 14735
    locator: the stacking free energies of the Watson-Crick nearest neighbors, the initiation term and the terminal AU penalty
  - paper: doi:10.1006/jmbi.1999.2700
    title: David H. Mathews, Jeffrey Sabina, Michael Zuker and Douglas H. Turner, Expanded sequence dependence of thermodynamic parameters improves prediction of RNA secondary structure, Journal of Molecular Biology 288(5), 1999, pages 911 to 940
    locator: the loop parameters of the 1999 set and the test of prediction on known structures
  - paper: doi:10.1073/pnas.0401799101
    title: David H. Mathews, Matthew D. Disney, Jessica L. Childs, Susan J. Schroeder, Michael Zuker and Douglas H. Turner, Incorporating chemical modification constraints into a dynamic programming algorithm for prediction of RNA secondary structure, PNAS 101(19), 2004, pages 7287 to 7292
    locator: the Turner 2004 free energy parameters, including the multibranch loop terms
  - paper: doi:10.1093/nar/gkp892
    title: Douglas H. Turner and David H. Mathews, NNDB, the nearest neighbor parameter database for predicting stability of nucleic acid secondary structure, Nucleic Acids Research 38 (database issue), 2010, pages D280 to D282
    locator: the rules and tables of the Turner 1999 and Turner 2004 sets, with worked examples
  - paper: doi:10.1186/1748-7188-6-26
    title: Ronny Lorenz, Stephan H. Bernhart, Christian Höner zu Siederdissen, Hakim Tafer, Christoph Flamm, Peter F. Stadler and Ivo L. Hofacker, ViennaRNA Package 2.0, Algorithms for Molecular Biology 6, 2011, article 26
    locator: the use of the Turner 2004 parameters in RNAfold, with a linear multiloop energy
---

The nearest-neighbor model gives the standard free energy change $\Delta G^\circ_{37}$ of the folding of an RNA strand into a [secondary structure](/rna-secondary-structure/), as a sum of terms for the loops of the structure. The main negative term is the stacking of two neighbor base pairs in a helix, and it depends on the two pairs only: this is the "nearest neighbor" of the name. Hairpins, bulges, interior loops and multiloops add positive terms for the loss of entropy. The parameters come from optical melting experiments on short duplexes and hairpins, mostly by the group of Douglas Turner. The current standard set is Turner 2004, collected in the NNDB database. It is the model of the [Zuker algorithm](/zuker-algorithm/), the [McCaskill algorithm](/mccaskill-algorithm/), mfold, RNAfold and RNAstructure.

## The machine

**Objects.** A sequence $s_1 \cdots s_n$ over $\{A, C, G, U\}$ and a secondary structure $P$ on it. The allowed pairs are the Watson-Crick pairs AU and GC and the wobble pair GU. A hairpin has at least 3 unpaired bases. The basic model has no pseudoknots.

**Loop decomposition.** Each pair $(i, j)$ of $P$ closes exactly one loop: the bases and pairs that are inside $(i, j)$ and not inside a pair that is inside $(i, j)$. The bases that no pair encloses form the exterior loop. The loop closed by $(i, j)$ is

- a **hairpin** if no pair is inside it;
- a **stack** if the only pair inside it is $(i + 1, j - 1)$;
- a **bulge** if there is one pair $(k, l)$ inside, with unpaired bases on one side only;
- an **interior loop** if there is one pair inside, with unpaired bases on both sides;
- a **multiloop** (multibranch loop) if two or more pairs are directly inside.

**The energy.** The free energy is

$$\Delta G(P) = \sum_{\text{loops } \ell \text{ of } P} \Delta G(\ell),$$

and the open strand, with no pairs, has $\Delta G = 0$. The terms of Turner 2004, in kcal/mol at 37 °C, are:

- **Stacks.** A table of $\Delta G$ for each stack, indexed by the two pairs. For example, the stack $5'$GC$3'$/$3'$CG$5'$ is $-3.42$, the stack $5'$CG$3'$/$3'$GC$5'$ is $-2.36$, and the stack $5'$AG$3'$/$3'$UC$5'$ is $-2.08$. Each end of a helix with an AU or GU pair adds a terminal penalty of $+0.45$.
- **Hairpins.** An initiation term that depends on the loop size $n$, a terminal mismatch term for the closing pair and the first unpaired bases, and bonuses for some special loops. For $n > 9$ the initiation term is extended as $\Delta G_{\mathrm{init}}(9) + 1.75\, RT \ln(n / 9)$.
- **Bulges.** An initiation term that depends on the size. A bulge of one base also adds the stack of the two pairs next to it, as if the bulge were not there.
- **Interior loops.** An initiation term that depends on the size $n_1 + n_2$, an asymmetry term that grows with $|n_1 - n_2|$, and mismatch terms for the two closing pairs. Small loops ($1 \times 1$, $1 \times 2$ and $2 \times 2$) have their own tables.
- **Multiloops.** The Turner 2004 set fits the energy as $a + b \cdot (\text{average asymmetry}) + c \cdot (\text{number of helices})$ with $a = 9.25$, $b = 0.91$ and $c = -0.63$, plus the stacking of terminal mismatches or coaxial helices. Folding programs use a linear form $a' + b' \cdot (\text{branches}) + c' \cdot (\text{unpaired bases})$ with their own constants, because it fits the dynamic program.
- **The exterior loop.** No initiation term, but dangling ends and terminal mismatches on the helices, and the terminal penalties.

**An example duplex.** Two strands of $5'$AGCGCU$3'$ pair with each other in a duplex of six pairs. The NNDB rules give the intermolecular initiation $+4.09$, two AU ends $2 \times 0.45$, the symmetry term $+0.43$ for a self-complementary duplex, and five stacks:

$$\Delta G = 4.09 + 0.90 + 0.43 - 2.08 - 3.42 - 2.36 - 3.42 - 2.08 = -7.94 \text{ kcal/mol}.$$

**An example hairpin.** In the hairpin example of the NNDB, a stem of four pairs has three stacks ($-2.11$, $-2.24$ and $-2.11$), one terminal AU penalty ($+0.45$), a terminal mismatch term of $-0.8$ for the closing pair, and the initiation term $+5.4$ of a loop of six bases. The sum is $-1.4$ kcal/mol: the stacks pay for the loop, but only just.

## What it counts

The model gives $\Delta G^\circ_{37}(P)$, the standard free energy change of the folding from the open strand to the structure $P$, in kcal/mol at 37 °C and in 1 M NaCl. A lower value means a more stable structure. Under the [thermodynamic hypothesis](/thermodynamic-hypothesis/) that the molecule is in equilibrium, the probability of $P$ is $e^{-\Delta G(P)/RT} / Z$, with $R = 1.987 \times 10^{-3}$ kcal/(mol K), $T$ in kelvin, and the [partition function](/partition-function/) $Z = \sum_P e^{-\Delta G(P)/RT}$. Each parameter also has an enthalpy $\Delta H$, so that $\Delta G(T) = \Delta H - T \Delta S$ gives the energy at other temperatures.

The cost measure of the algorithms is the number of loop evaluations: each loop term is a table lookup and a few additions, so it is $O(1)$ time on the [word RAM](/word-ram/).

## Relation to other models

- **Base pair counting.** The [Nussinov algorithm](/nussinov-algorithm/) scores $-1$ per pair and 0 per loop. It is a special case with no stacking, so it gives no reason for pairs to form helices.
- **Stacking-pair models.** Many complexity results use a simpler model with an energy only for each stack of two pairs. Under this model, finding a minimum energy structure with pseudoknots is NP-hard; see [pseudoknot NP-hardness](/pseudoknot-np-hardness/).
- **Pseudoknot models.** The energy models of Rivas and Eddy (1999) and Dirks and Pierce (2003) add terms for pseudoknots to the nearest-neighbor terms. They are fits with fewer measurements than the nested loops; see [RNA pseudoknot prediction](/rna-pseudoknot-prediction/).
- **Grammars and learned scores.** A [probabilistic context-free grammar](/probabilistic-context-free-grammar/) with the same loop types gives a probabilistic model, and its rule weights play the role of the Boltzmann factors. CONTRAfold and other programs learn loop scores from known structures instead of melting experiments.
- **Kinetics.** The same energies give the rates of moves in [RNA folding kinetics](/rna-folding-kinetics/) and the landscape of an [energy landscape](/energy-landscape/) analysis.

## Known results in the model

- **Minimum free energy.** The [Zuker algorithm](/zuker-algorithm/) finds a minimum free energy structure in $O(n^3)$ time and $O(n^2)$ space, worst case, when the size of interior loops is at most a constant (usually 30), and in $O(n^4)$ time without this bound. Lyngsø, Zuker and Pedersen (1999) do all interior loops in $O(n^3)$ total time for loop energies of the Turner form.
- **Partition function.** The [McCaskill algorithm](/mccaskill-algorithm/) computes $Z$ and all pair probabilities in the same time and space.
- **Pseudoknots.** With general pseudoknots and an energy per pair that depends on its neighbors, the minimum free energy is NP-hard (Lyngsø and Pedersen 2000). For restricted classes there are polynomial algorithms, in $O(n^4)$ to $O(n^6)$ time.
- **Design.** Finding a sequence whose only optimal structure is a given structure is NP-complete in the Watson-Crick base pair model when some positions must have given bases (Bonnet, Rzążewski and Sikora 2020). They left the case with no fixed positions open, and no hardness proof for the full Turner model is known. See [RNA inverse folding](/rna-inverse-folding/).
- **Accuracy.** The model is a fit, and the minimum free energy structure is often not the known structure, in particular for long RNAs. The tests of Mathews and others (1999, 2004) report the fraction of known pairs that the prediction finds on sets of RNAs with known structures.

## References
