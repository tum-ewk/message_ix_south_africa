# MESSAGEix South Africa

## Overview
This repository contains the scripts and data for the following manuscript:

 > Clara Luisa Orthofer, Daniel Huppmann, and Volker Krey (2019).  
 > South Africa After Paris - Fracking Its Way to the NDCs?  
 > *Frontiers in Energy Research* 7(20).   
 > doi: [10.3389/fenrg.2019.00020](https://doi.org/10.3389/fenrg.2019.00020)

## Dependencies
The code included in this repository depends on the open-source, dynamic
systems-optimization model [MESSAGEix](https://messageix.iiasa.ac.at/).
For download, installation and setup instruction please refere to 
[github.com/iiasa/message_ix](https://github.com/iiasa/message_ix). 

## Baseline Scenario
The folder `db` contains the ixmp-HSQLDB database with the calibrated 
baseline scenario.

## Setup Instructions
Before running or editing scenarios, you need to tell git not to track 
the changes you make to the local database `db/message_sa`. To do so,
open a git bash in your local repository (`message_ix_south_africa`)
and run `git update-index --skip-worktree db/*` .

## Runing Scenarios
The described shale gas and carbon price scenarios can be reproduced
by running the `run.py` script.
The functions required for running the scenarios, post-processing results,
and generating the figures used in the manuscript can be found in the 
`utils` folder.

## Acknowledgement 
This research was initiated as part of the Young Scientists Summer Program
(YSSP) at the International Institute for Systems Analysis, Laxenburg (Austria)
with financial support from the
[Austrian Academy of Sciences](https://www.oeaw.ac.at),
the Austrian National Member Organization of IIASA.

Clara Luisa Orthofer ([@ClaraLuisa](https://github.com/ClaraLuisa) received
the [Peccei Award](http://www.iiasa.ac.at/web/home/education/yssp/awards.html)
for an earlier version of the published manuscript.
