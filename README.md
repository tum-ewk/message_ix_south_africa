# message_ix South Africa

This repository contains the scripts and data of the manuscript: 
*"South Africa After Paris - Fracking Its Way to the NDCs?"*. 

The folder `db` contains the ixmp-HSQLDB database with the calibrated 
baseline scenario.

## Setup Instructions

Before running or editing scenarios, you need to tell git not to track 
the changes you make to the local database `db/message_sa`. To do so,
open a git bash in your local repository (`../message_ix_south_africa`)
and run `git update-index --skip-worktree db/*` .

## Runing Scenarios

The baseline scenario, described in the manuscript, can be found in the 
the ixmp-HSQL database included in this repository The described shale 
gas and carbon price scenarios can be reproduced by running the `run.py`
script. 
The functions required for running the scenarios, post process and 
generating the figures used in the manuscript can be found in the 
`../utils` folder.