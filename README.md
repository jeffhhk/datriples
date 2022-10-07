
# Data augmentation triple extraction

Deep learning model WIP for extracting triple relations over biomedical text, using data augmentation.

## Prerequisites

Tested with python 3.7.9

Third party packages specified in requirements.txt.

## Conventions

The library lib/diskgenmem.py provides caching of previously computed streams, with transparent compression.  Initially, the package joblib was used, but joblib could not pickle streams, so memory grew in proportion to the size of the data.  In addition, joblib time constant factors were slow.

Each program under bin/ determines the project directory from the program location, appending sys.path so that namespaces can be referred to from the project directory.

Currently external upstream data is manually downloaded, listed in lib/altname_paths.py.

## Code directories

|   |   |
|---|---|
| bin/ | Runnable programs.  Favor creating more programs to creating more command line flags. |
| lib/resource/ | Each data resource X gets built with lib/resource/X.py and functionally tested with bin/benchmarks/X.py. |
| test/ | Unit tests |

The file lib/resource/altname_paths.py contains the catalog of files and paths for data.

## Data directories

|   |   |
|---|---|
| cache/external | Copies of data obtained from third parties. |
| cache/managed | Managed cache of intermediate computations |
