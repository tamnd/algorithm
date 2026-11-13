---
tag: 68S38Z
kind: problem
slug: comparative-modeling
name: Comparative (homology) modeling
aliases:
- Homology modeling
- Template-based modeling
area: biology/structure-prediction
level: core
summary: Build a 3D model of a target protein from the known structure of a homologous template, through an alignment of the two sequences. The error grows as the sequence identity falls.
prereqs: [global-alignment, rmsd]
see_also: [modeller, protein-fold-recognition, protein-threading, loop-modeling, side-chain-packing, protein-structure-prediction, i-tasser, alphafold]
sources:
  - paper: doi:10.1002/j.1460-2075.1986.tb04288.x
    title: Cyrus Chothia and Arthur M. Lesk, The relation between the divergence of sequence and structure in proteins, The EMBO Journal 5(4), 1986, 823-826
    locator: the relation between the fraction of mutated residues in the core and the r.m.s. deviation of the main-chain atoms of the core
  - paper: doi:10.1006/jmbi.1993.1626
    title: Andrej Sali and Tom L. Blundell, Comparative protein modelling by satisfaction of spatial restraints, Journal of Molecular Biology 234(3), 1993, 779-815
    locator: the restraint-based method of building the model from the alignment
  - paper: doi:10.1146/annurev.biophys.29.1.291
    title: Marc A. Marti-Renom, Ashley C. Stuart, Andras Fiser, Roberto Sanchez, Francisco Melo and Andrej Sali, Comparative protein structure modeling of genes and genomes, Annual Review of Biophysics and Biomolecular Structure 29, 2000, 291-325
    locator: the steps of comparative modeling and the kinds of error in the models
  - paper: doi:10.1093/protein/12.2.85
    title: Burkhard Rost, Twilight zone of protein sequence alignments, Protein Engineering 12(2), 1999, 85-94
    locator: the twilight zone of pairwise sequence identity, where identity alone no longer tells homologs apart
  - paper: doi:10.1110/ps.9.9.1753
    title: Andras Fiser, Richard Kinh Gian Do and Andrej Sali, Modeling of loops in protein structures, Protein Science 9(9), 2000, 1753-1773
    locator: the accuracy of loop models as a function of loop length
---

Comparative modeling, also called homology modeling, builds a three-dimensional model of a *target* protein from the experimental structure of a related *template* protein. It rests on one observation: proteins that share an ancestor keep their fold much longer than they keep their sequence. So if the target sequence aligns well with a protein of known structure, most of the target backbone can be copied from that structure. The method has four steps: find a template, align the target to it, build the model, and check the model. The quality of the model depends mostly on the sequence identity between target and template and on the quality of the alignment.

## In plain words

Two related proteins are like two editions of the same machine. Some parts change from edition to edition, but the main frame stays. If you have the plans of one edition and a list of the parts of the other, you can draw a good plan of the second one: keep the frame, swap the parts that changed, and redraw the places where a part was added or removed.

In the same way, we line up the amino acid letters of the new protein with those of a protein whose shape is known. Where the letters line up, we copy the position of the backbone. Where the new protein has extra letters or fewer letters, we must build new loops. Then we put the side chains of the new protein in place. The closer the two sequences are, the better the model.

## Definition

**Input.** A target sequence $a = a_1 \ldots a_n$ over the 20 amino acids, and one or more template structures. A template is a sequence $b = b_1 \ldots b_m$ with the coordinates of its atoms. Usually the templates are found by a search of the Protein Data Bank with the target sequence or its profile.

**Output.** Coordinates for the atoms of all $n$ residues of the target, that is a model structure, and often an estimate of its error.

**Quality.** The model is good if it is close to the true structure of the target, measured after the [optimal superposition](/optimal-superposition/), for example by the [RMSD](/rmsd/) of the $C_\alpha$ atoms, by [GDT-TS](/gdt-ts/) or by [TM-score](/tm-score/). The true structure is not known when the model is built, so the problem is a prediction problem, not an optimization problem with a single correct answer.

**The steps.** The usual method splits the problem into parts that each have a clear form:

1. *Template search.* Find structures whose sequences are similar to $a$, with [BLAST](/blast/), [profile HMMs](/profile-hmm/) or [fold recognition](/protein-fold-recognition/) when the similarity is weak.
2. *Alignment.* Align $a$ to each template sequence. This is a [global alignment](/global-alignment/) or a profile alignment. Each aligned pair $(a_i, b_k)$ says "residue $i$ of the target sits where residue $k$ of the template sits".
3. *Model building.* Copy or restrain the backbone of the aligned residues, rebuild the inserted and deleted regions ([loop modeling](/loop-modeling/)), and place the side chains ([side-chain packing](/side-chain-packing/)). [MODELLER](/modeller/) does these together by the satisfaction of spatial restraints.
4. *Assessment.* Check the stereochemistry and score the model with a statistical [energy function](/energy-function/) to estimate its error.

## Variants

- **Single template or multiple templates.** With several templates, each region of the model can come from the template that fits it best, or the restraints of all templates can be combined.
- **Rigid-body assembly.** Copy the conserved core from the template, then add loops and side chains. This is the older method.
- **Satisfaction of spatial restraints.** Turn the template distances and angles into restraints on the target, and find coordinates that satisfy them best ([MODELLER](/modeller/)).
- **Segment matching.** Build the model from short fragments of known structures that match guide positions taken from the template.
- **Template-based modeling with weak templates.** When identity is low, the template comes from [protein threading](/protein-threading/), and methods such as [I-TASSER](/i-tasser/) reassemble template fragments and refine them.

## Examples

**An alignment and what it means for the model.** Consider the alignment

```text
target    M K V L - - A T G
template  M R V L G S A S G
```

There are 7 aligned pairs, and 5 of them are identical (M, V, L, A, G), so the identity is $5/7 \approx 71\%$. The backbone of the 7 aligned target residues comes from the template. Residues K and T differ from R and S, so their side chains must be placed again. The template residues G and S have no partner: the target has a *deletion* there, so target residues L and A, which are next to each other in the target, sit at template positions that are three residues apart. The model must close this gap with a new local backbone, which is a [loop modeling](/loop-modeling/) problem. An insertion in the target, the opposite case, needs a new loop of the inserted length.

**The Chothia and Lesk relation.** Chothia and Lesk (1986) compared pairs of related proteins and fitted the r.m.s. deviation $\Delta$ of the main-chain atoms of the common core to the fraction $H$ of mutated residues in the core:

$$\Delta \approx 0.40\, e^{1.87 H} \text{ Å}.$$

Some values of this curve:

| fraction mutated $H$ | 0 | 0.2 | 0.5 | 0.7 | 0.8 | 1 |
|---|---|---|---|---|---|---|
| core $\Delta$ (Å) | 0.40 | 0.58 | 1.02 | 1.48 | 1.79 | 2.60 |

The curve doubles each time $H$ grows by $\ln 2 / 1.87 \approx 0.37$. At 50% identity in the core ($H = 0.5$) the cores differ by about 1 Å, and at 20% to 30% core identity by about 1.5 to 1.8 Å. These numbers hold for the core only, after superposition; the loops and the regions outside the common core differ more. They give a rough scale for the core error of a model built from one template with a correct alignment, because a model that copies the template core also copies its difference from the target.

**A non-example.** A target with 15% identity to its best hit, over a short alignment, is below even the twilight zone of about 20% to 35% identity that Rost (1999) described: at that level identity alone does not tell a homolog from an unrelated protein. Then the problem is [fold recognition](/protein-fold-recognition/), and the alignment, not the model building, limits the accuracy.

## Known algorithms

- **Alignment.** [Needleman-Wunsch](/needleman-wunsch/) or [profile-profile alignment](/sequence-profile-alignment/), in $O(nm)$ time for lengths $n$ and $m$. Profile methods such as [HMMER](/hmmer/) and HHpred give better alignments at low identity.
- **[MODELLER](/modeller/)** (Sali and Blundell 1993). Derives distance and angle restraints from the templates and optimizes their sum with conjugate gradients and molecular dynamics with simulated annealing.
- **Loop building.** Database search for fragments that fit the anchor geometry, or ab initio sampling with closure methods such as cyclic coordinate descent ([loop modeling](/loop-modeling/)). Fiser, Do and Sali (2000) report that the accuracy falls fast with the loop length.
- **Side chains.** Rotamer packing on the fixed backbone, for example with SCWRL ([side-chain packing](/side-chain-packing/), [dead-end elimination](/dead-end-elimination/)).
- **Combined pipelines.** [I-TASSER](/i-tasser/) and [Rosetta](/rosetta/) use templates as a start and refine them. [AlphaFold](/alphafold/) can read templates too, but it gets most of its accuracy from the alignment of many homologs.

## Bounds

There is no complexity bound for the problem as a whole, because the true answer is a physical fact, not the optimum of a fixed function. The parts have clear costs:

- Pairwise alignment takes $O(nm)$ time and space, or $O(nm)$ time and $O(n + m)$ space with Hirschberg's method.
- Copying the coordinates of the aligned residues takes $O(n)$ time.
- Side-chain packing with a general pairwise energy is NP-hard ([side-chain packing](/side-chain-packing/)), so exact packing uses pruning or the sparse contact graph.

On the accuracy side, the Chothia and Lesk relation gives the expected core divergence between target and template. With the alignment errors that grow at low identity, models from templates at about 30% identity or less often have large errors in loops and in the relative position of secondary structures, and models from templates above about 50% identity are often close to the experimental structure in the core. These are trends from data, not guarantees for one protein.

## Reductions

- **To alignment.** Given the template, the main decision is the alignment. Once it is fixed, the backbone of the aligned core follows.
- **To loop modeling and side-chain packing.** The gaps of the alignment turn into [loop modeling](/loop-modeling/) problems with fixed ends, and the changed residues into a [side-chain packing](/side-chain-packing/) problem on a fixed backbone.
- **From fold recognition.** When no template is found by sequence search, the problem becomes [fold recognition](/protein-fold-recognition/) first, and comparative modeling follows on the recognized template.

## Applications

- **Function and mutations.** A model shows where a mutation sits, for example in the core or at a binding site, and helps to explain its effect.
- **Drug discovery.** Models of a binding site support docking and the design of ligands when no experimental structure exists.
- **Experimental structure determination.** A model can serve as the search model for molecular replacement in X-ray crystallography, or as a start for fitting into a cryo-EM map.
- **Genome-scale coverage.** Databases of comparative models cover many proteins of whole genomes whose structures were not solved, which was the main way to get such coverage before deep learning methods.

## References
