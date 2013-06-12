g2 Functional Tests
=============================

Howto:

To run the tests:

1. Exports
 * export DFTS_SUT=srm-devel.desy.de
 * export DFTS_BASEPATH=/pnfs/desy.de/data/dteam/tigran

2. Configure your voms and run:
 * voms-proxy-init --voms ......

3. Run commands:
 * python srmcopy.py
 * python spacemanager.py
 * python lcgcopy.py
 * python serviceports.py
 * python gsiftp.py
 * python dcap.py





