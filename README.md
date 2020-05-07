# Polyglot Adapters

A prototype implementation of our polyglot adapters approach for the GraalVM.


# How to Use

1. Download [GraalVM 1.0.0 RC15][graalvm].
2. Install Python and Ruby via `bin/gu install python ruby`.
3. Run [the examples](examples.py) via `bin/polyglot --jvm examples.py`.


*GraalVM is not required to run the tests (`python3 tests.py`).*


# Paper

- Fabio Niephaus, Tim Felgentreff, and Robert Hirschfeld. *Towards Polyglot
Adapters for the GraalVM.* In Proceedings of the Conference Companion of the 3rd
International Conference on Art, Science, and Engineering of Programming,
Genova, Italy, 2019, ACM DL.  
   [![doi][icw19_doi]][icw19_paper] [![bibtex][bibtex]][icw19_bibtex] [![Preprint][preprint]][icw19_pdf]


[bibtex]: https://img.shields.io/badge/bibtex-download-blue.svg
[graalvm]: https://github.com/oracle/graal/releases/tag/vm-1.0.0-rc15
[icw19]: https://2019.programming-conference.org/track/icw-2019-papers#event-overview
[icw19_bibtex]: https://dl.acm.org/downformats.cfm?id=3328458&parent_id=3328433&expformat=bibtex
[icw19_doi]: https://img.shields.io/badge/doi-10.1145/3328433.3328458-blue.svg
[icw19_paper]: https://doi.org/10.1145/3328433.3328458
[icw19_pdf]: https://fniephaus.com/2019/icw19-polyglot-adapters.pdf
[preprint]: https://img.shields.io/badge/preprint-download-blue.svg
