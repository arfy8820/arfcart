# arfcart
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm-project.org)

## What is it?
Arfcart is a simple cart machine, based on the bass audio library. Configure up to 12 carts to play either a single file, or a folder of files (including subfolders), sequentially or at random.
Being based on bass, several file formats will play out of the box.

## Installing
This is a python project that uses pdm as the build tool. Install it with either pip, pipx, or, if using homebrew, you can `brew install pdm`
Once you clone this repository, simply pdm build to produce a sdist and a python wheel in the dist directory.
Note: This *requires* python <3.12 at the moment.
Once installed, arfcart-cli is available as a console app that you can run.
Yes, once more development on this is done, I'll publish this to PyPi.
Enjoy!
