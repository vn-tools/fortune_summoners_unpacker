A tool for extracting sprites from Fortune Summoners: Secret of the Elemental
Stone. Tested on the Steam version only.

Usage:

1. Manually extract resources from `sotesd.dll` with a tool like ResourceHacker
   or [resextract](https://github.com/vn-tools/resextract/).
2. Run this script on the output files.

Other files contain other resources. From what I discovered:

* `sotes.exe`: almost exclusively map data. Haven't tried to decipher it.
* `sotesd.dll`: **sprites**, audio samples.
* `sotesp.dll`: more audio samples.
* `sotesp.dll`: I have no idea...

As far as I'm concerned, audio samples are encrypted in some way, even though
they have begin with uncompressed `RIFF` magic number.
