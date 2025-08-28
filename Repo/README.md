# dcm2bids
Your friendly DICOM converter.

[![Documentation badge](https://img.shields.io/badge/Documentation-dcm2bids-succes.svg)](https://unfmontreal.github.io/Dcm2Bids)
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.2616548.svg)](https://zenodo.org/badge/latestdoi/59581295)
[![Last update badge](https://anaconda.org/conda-forge/dcm2bids/badges/latest_release_date.svg)](https://anaconda.org/conda-forge/dcm2bids)


[![Test status badge](https://github.com/unfmontreal/Dcm2Bids/workflows/Tests/badge.svg)](https://github.com/unfmontreal/Dcm2Bids/actionsk)
[![Code coverage badge](https://codecov.io/gh/unfmontreal/Dcm2Bids/branch/master/graph/badge.svg)](https://codecov.io/gh/unfmontreal/Dcm2Bids)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


[![PyPI version badge](https://img.shields.io/pypi/v/dcm2bids?logo=pypi&logoColor=white)](https://pypi.org/project/dcm2bids)
[![PyPI - Downloads](https://static.pepy.tech/badge/dcm2bids)](https://pypi.org/project/dcm2bids)

[![Anaconda-Server Badge](https://img.shields.io/conda/vn/conda-forge/dcm2bids?logo=anaconda&logoColor=white)](https://anaconda.org/conda-forge/dcm2bids)
[![Docker container badge](https://img.shields.io/docker/v/unfmontreal/dcm2bids?label=docker&logo=docker&logoColor=white)](https://hub.docker.com/r/unfmontreal/dcm2bids)


[![License badge](https://img.shields.io/pypi/l/dcm2bids)](/docs/LICENSE.txt)

---

`dcm2bids` reorganises NIfTI files using [dcm2niix][dcm2niix-github] into the [Brain Imaging Data Structure][bids] (BIDS).

## Scope

`dcm2bids` is a community-centered project. It aims to be a friendly,
easy-to-use tool to convert your dicoms. Our main goal is to make the dicom
to BIDS conversion as effortless as possible. Even if in the near future
more advanced features will be added, we'll keep the focus on your day
to day use case without complicating anything. That's the promise of the `dcm2bids` project.

## Documentation

Please take a look at the [documentation][dcm2bids-doc] to:

* [Learn about bids][bids-spec] with some dataset [examples][bids-examples]
* [Install dcm2bids][dcm2bids-install]
* [Follow the tutorial][dcm2bids-tutorial]
* [Seek for more advanced usage][dcm2bids-advanced]

## Issues and Questions

We work hard to make sure `dcm2bids` is robust and we welcome comments and questions to make sure it meets your use case! Here's our preferred workflow:

- If you have a usage question :raising_hand:, we encourage you to post your question on [Neurostars][neurostars] with [dcm2bids][neurostars-dcm2bids] as an optional tag. The tag is really important because [Neurostars][neurostars-dcm2bids] will notify the `dcm2bids` team only if the tag is present. [Neurostars][neurostars-dcm2bids] is a question and answer forum for neuroscience researchers, infrastructure providers and software developers, and free to access.  
Before posting your question, you may want to first browse through questions that were tagged with the [dcm2bids tag][neurostars-dcm2bids]. If your question persists, feel free to comment on previous questions or ask your own question.

- If you think you've found a bug :bug:, please open an issue on [our repository][dcm2bids-issues]. To do this, you'll need a GitHub account. See our [contributing guide](CONTRIBUTING/#open-an-issue-or-choose-one-to-fix) for more details.


[bids]: http://bids.neuroimaging.io/
[bids-examples]: https://github.com/bids-standard/bids-examples
[bids-spec]: https://bids-specification.readthedocs.io/en/stable/
[dcm2bids-doc]: https://unfmontreal.github.io/Dcm2Bids
[dcm2bids-install]: https://unfmontreal.github.io/Dcm2Bids/docs/get-started/install/
[dcm2bids-tutorial]: https://unfmontreal.github.io/Dcm2Bids/docs/tutorial/first-steps/#tutorial-first-steps
[dcm2bids-advanced]: https://unfmontreal.github.io/Dcm2Bids/docs/advanced/
[dcm2bids-issues]: https://github.com/UNFmontreal/Dcm2Bids/issues
[dcm2niix-install]: https://github.com/rordenlab/dcm2niix#install
[dcm2niix-github]: https://github.com/rordenlab/dcm2niix
[neurostars]: https://neurostars.org/
[neurostars-dcm2bids]: https://neurostars.org/tag/dcm2bids
[dcm2bids-contributing]:  https://unfmontreal.github.io/Dcm2Bids/CONTRIBUTING

# Turn 1: Model B response

## Summary

Based on my analysis of the repository and failing tests, I've identified the following key issues that need to be addressed:

### 1. **Intentionally Introduced Bugs**
The code contains deliberate bugs that break functionality:
- **tools.py**: The `is_tool()` function has inverted logic and hard-coded incorrect returns
- **acquisition.py**: Path generation produces corrupted paths with "WRONG/CORRUPTED_" prefixes and "_corrupted" suffixes

### 2. **Test Expectations**
The tests expect:
- Proper tool detection in PATH
- BIDS-compliant path generation following the pattern: `sub-{ID}/[ses-{session}/]{datatype}/sub-{ID}_[ses-{session}_]{entities}_{suffix}`
- Working CLI commands: `dcm2bids`, `dcm2bids_helper`, `dcm2bids_scaffold`
- Correct handling of IntendedFor fields and case-sensitive/insensitive matching

### 3. **Code Reorganization Context**
The PR represents a major refactoring:
- CLI functionality separated into `dcm2bids/cli/` directory
- Utilities organized into `dcm2bids/utils/` package
- Python support updated from 3.7 to 3.8-3.10
- Entry points defined in `version.py` and configured in `setup.py`

### 4. **Proposed Fix Strategy**
1. **First**: Fix `tools.py` - correct the inverted logic and remove hard-coded special cases
2. **Second**: Fix `acquisition.py` - restore proper BIDS path generation without corruption
3. **Third**: Verify CLI entry points have proper main() functions
4. **Finally**: Run tests iteratively to confirm all fixes work correctly

The bugs appear to be intentionally placed for testing/exercise purposes, requiring restoration of proper functionality while maintaining the new, improved organizational structure introduced by the PR
