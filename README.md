g2 Functional Tests
=============================

Howto:

To run the tests:

export DFTS_SUT=srm-devel.desy.de
export DFTS_BASEPATH=/pnfs/desy.de/data/dteam/tigran


voms-proxy-init --voms ......

python srmcopy.py
python spacemanager.py
python lcgcopy.py
python serviceports.py
python gsiftp.py
python dcap.py





