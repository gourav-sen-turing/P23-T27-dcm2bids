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

# Turn 1: Model A response

## Analysis Summary

Based on my investigation of the DCM2BIDS codebase reorganization PR and the failing tests, here's my understanding of the issues:

### **Repository Structure**
The project has been reorganized with:
- **CLI modules** separated into `dcm2bids/cli/` directory with individual entry points
- **Utility functions** moved to `dcm2bids/utils/` package
- **Main functionality** split across specialized modules

### **Key Failing Test Categories**

#### 1. **Test Framework Issue - `script_runner` Fixture**
The tests are using `pytest-console-scripts` but passing arguments incorrectly:
- **Current**: `script_runner.run(['dcm2bids_scaffold', '--help'])`
- **Expected**: `script_runner.run('dcm2bids_scaffold', '--help')`

#### 2. **`is_tool()` Function Logic Issue**
In `dcm2bids/utils/tools.py`, the `is_tool()` function has incorrect hardcoded logic:
```python
def is_tool(name):
result = which(name)
if name == "dcm2bids":
return False  # BUG: This should check if result is not None
elif name == "dummy_cmd":
return True   # BUG: This is incorrect for testing
return result is None  # BUG: Logic is inverted
```
This function should return `True` if the tool exists in PATH, but the logic is broken.

#### 3. **Participant and Acquisition Classes Returning Wrong Paths**
The `Participant` and `Acquisition` classes have incorrect implementations:

**Participant class issues** (`participant.py`):
- `directory` property returns wrong paths with "BROKEN", "INVALID", "CORRUPTED" strings
- `prefix` property returns malformed strings with wrong formatting

**Acquisition class issues** (`acquisition.py`):
- `dstRoot` property returns paths with "WRONG", "INVALID_" prefixes
- `__eq__` method always returns `False` instead of comparing objects properly
- `setDstFile()` method isn't setting the destination file correctly

#### 4. **Missing `help` Option in Argparse**
The CLI modules (`dcm2bids.py`, `dcm2bids_helper.py`, `dcm2bids_scaffold.py`) all set `add_help=False` in their argparse configurations, which means the `--help` option isn't being added.

#### 5. **Utils Module Default Values**
The DEFAULT class in `utils/utils.py` contains constants that might need adjustment for the new structure.

### **Proposed Fixes**

1. **Fix `script_runner.run()` calls** - Change list to individual arguments
2. **Fix `is_tool()` function** - Correct the logic to properly check for tool existence
3. **Fix Participant class methods** - Return proper BIDS-compliant paths
4. **Fix Acquisition class** - Implement proper comparison and path generation
5. **Add help option** - Remove or change `add_help=False` to `add_help=True` in argparse configs

### **Test Expectations**

The tests expect:
- CLI tools to respond to `--help` option successfully
- `is_tool("dcm2bids")` to return `True` when dcm2bids is installed
- `is_tool("dummy_cmd")` to return `False` for non-existent tools
- Participant directory structure to follow BIDS format: `sub-<label>/[ses-<session>/]`
- Acquisition paths to follow proper BIDS entity ordering

This analysis reveals that the refactoring has introduced several bugs in the core classes and utility functions, particularly around path generation and tool checking functionality. The tests are well-designed to catch these issues and ensure BIDS compliance.
