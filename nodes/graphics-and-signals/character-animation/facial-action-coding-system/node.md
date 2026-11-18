---
tag: 46HKCF
kind: concept
slug: facial-action-coding-system
name: Facial action coding system
aliases:
- FACS
area: graphics-and-signals/character-animation
level: core
summary: A taxonomy of visible facial movements into action units, each tied to facial muscles, used to design blendshape sets for faces.
prereqs: []
see_also: [blendshape-model, blendshape-direct-manipulation, example-based-facial-rigging, deformation-transfer, pose-space-deformation]
sources:
  - paper: "Paul Ekman and Wallace V. Friesen, Facial Action Coding System: A Technique for the Measurement of Facial Movement, Consulting Psychologists Press, Palo Alto, 1978"
    locator: the manual as a whole (general locator; the manual was not read for this page)
  - paper: "Paul Ekman, Wallace V. Friesen and Joseph C. Hager, Facial Action Coding System: The Manual on CD ROM, A Human Face, Salt Lake City, 2002"
    locator: the revised manual as a whole (general locator; the manual was not read for this page)
  - paper: doi:10.2312/egst.20141042
    title: "J. P. Lewis, Ken Anjyo, Taehyun Rhee, Mengjie Zhang, Fred Pighin and Zhigang Deng, Practice and theory of blendshape facial models, Eurographics 2014 State of the Art Reports, 199-218"
    locator: the discussion of FACS as a guide for the choice of blendshape targets (general locator)
---

The Facial Action Coding System (FACS) is a method from psychology for describing what a face does.
Ekman and Friesen published it in 1978 as a manual for human coders, and Ekman, Friesen and Hager revised it in 2002.
It splits every visible facial movement into action units (AUs).
Each action unit is the visible effect of one facial muscle or a small group of muscles, and it has a number and a name, for example AU 12, the lip corner puller.
A coder watches a face, frame by frame, and writes down which action units are active and how strongly.
FACS is not an algorithm and not a model of a mesh.
In computer graphics it is a shared vocabulary: many face rigs build their [blendshape](/blendshape-model/) targets so that one target, or a left and a right target, matches one action unit.

## In plain words

A face can make a very large number of expressions, but they are built from a smaller set of basic movements.
The inner ends of the brows go up.
The corners of the mouth pull up and out.
The jaw drops.
FACS gives each such movement a number, and it describes in detail what each one looks like, so that two trained people who watch the same face write down the same numbers.
A smile is then not one thing but a code, such as "6 + 12": the cheeks rise and the lip corners pull.
For an animator, the same list is a checklist of the shapes that a face rig must be able to make.

## The idea

**Appearance, not emotion.**
FACS codes what moves, not what the person feels.
The code "1 + 2 + 5 + 26" says that the brows rose, the upper lids rose and the jaw dropped.
Whether that is surprise is a separate interpretation, made by other systems built on top of FACS codes.
This split is the main design choice of FACS, and it is what makes the codes repeatable between coders.

**Anatomy as the basis.**
Ekman and Friesen based the units on the anatomy of the facial muscles, starting from earlier work of the Swedish anatomist Carl-Herman Hjortsjö (1969).
An action unit is defined by the change in appearance that a muscle action makes, as a coder sees it.
The manual does not give a biomechanical model of the muscles, and some units correspond to more than one muscle, or to part of one.
So "tied to the muscles" means that the units are named and separated by their muscular basis, not that FACS simulates muscles.

**Intensity.**
FACS scores the intensity of a unit with the letters A to E, from a trace (A) to the maximum that the person can show (E).
So "12C" is a marked lip corner pull.

**What the manual contains.**
The manual lists the action units, with the muscular basis, the changes in appearance, the rules to tell similar units apart, and the rules for units that occur together.
It also has codes for head and eye positions and for some movements that are not single muscle actions.
The exact number of units and codes depends on the edition and on what one counts; this page does not give a number, because the manual was not read for it.

**Combinations are not sums.**
Two units that act together can change the face in a way that neither shows alone, and the manual describes such combinations.
This is the same effect that makes [blendshape](/blendshape-model/) rigs need corrective shapes: the offsets of two targets do not simply add.

## Examples

These are standard codes and names, as used in the FACS literature.

| code | name | main muscular basis |
|---|---|---|
| AU 1 | inner brow raiser | frontalis, medial part |
| AU 2 | outer brow raiser | frontalis, lateral part |
| AU 4 | brow lowerer | corrugator and depressor muscles of the brow |
| AU 6 | cheek raiser | orbicularis oculi, orbital part |
| AU 12 | lip corner puller | zygomaticus major |
| AU 26 | jaw drop | relaxation of the jaw muscles |

**Reading a code by hand.**
The code "6 + 12" means the cheeks rise, the skin around the eyes gathers, and the lip corners pull up.
The code "12" alone is the same mouth without the eye region.
FACS codes both and leaves the meaning to the user of the codes; the difference between the two is the usual example of why the eye region matters for a smile.

**A rig built on FACS.**
A face rig has a symmetric target for AU 26 (the jaw), and a left and a right target for AU 12.
An animator who keys "12C on the left only" sets the weight of the left AU 12 target to a middle value and leaves the right one at 0.
A capture system that detects action units in video can drive the same rig, because its output uses the same names.
The mapping from a letter grade to a weight is a choice of the rig, not part of FACS.

**A combination that needs a corrective.**
With AU 12 and AU 26 both at full weight, the delta form adds the two offsets at the corner of the mouth.
If the result looks wrong, the rigger sculpts a corrective shape for the pair "12 + 26"; the [blendshape model](/blendshape-model/) page works this case with numbers.

## Where it is used

- **Face rigs.** Many film and game face rigs name and sculpt their targets after action units, and split them into left and right halves. FACS gives the rigger a list of targets that covers the visible movements of a face, and it gives animators and riggers a common language. The 2014 survey of Lewis and others discusses this use.
- **Retargeting and capture.** Because every actor and every character can make "the same" action unit, an AU-based rig makes it easier to move a performance from one face to another. [Deformation transfer](/deformation-transfer/) and [example-based facial rigging](/example-based-facial-rigging/) build such target sets for a new face from a generic one.
- **Editing.** [Direct manipulation of blendshapes](/blendshape-direct-manipulation/) solves for target weights from dragged points. With AU-based targets the result is a readable code as well as a shape.
- **Psychology and computer vision.** FACS was made for research on facial behavior, where trained coders score video. Automatic detection of action units in images is a task of computer vision that uses FACS codes as labels.

FACS has limits as a basis for a rig.
It describes the appearance of movements, so it says nothing about the shapes of the lips for speech beyond the units that they use, or about the skin, the eyes and the tongue in detail.
Rigs add targets for speech shapes and for fine control that are not action units.

## References
