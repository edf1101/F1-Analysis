# Config Folder

### config.json
This file contains basic configuration settings for the project. Encoding should be utf-8.
- "season_train_start": The first season to train the model on
- "season_train_end": The last season (inclusive) to train the model on
- "path_to_excludes": The path (relative to config directory) to the file containing the list of 
races we want to exclude from the training data

### excludes.txt
This file contains the races that we don't want to include in the training data. This is useful for excluding outliers.
Encoding should be utf-8.

It is formatted so each Race we want to exclude is on a new line. The format is Season:Race
eg. 2021:Monaco.
