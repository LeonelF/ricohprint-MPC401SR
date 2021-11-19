# ricohprint-MPC401SR
##Ricoh Print Counter Reader and Report

ricohprint-MPC401SR is an automated counter reader and reporter for Ricoh Printer Tested Model MP C401sr

## Features

- Reads directly from printer
- Stores data in database for later consult
- Sends email with detailed print counts
- Dry run just to check current print count

## Installation

ricohprint-MPC401SR requires Python 3 to run.

Clone the repo and install dependencies.

```sh
clone https://github.com/LeonelF/ricohprint-MPC401SR.git
cd ricohprint-MPC401SR
pip install -r requirements.txt
```

## How to use

```sh
python3 ricoh.py <arg>
```

###Arguments:

- -p (Dry run, only prints the current print count)
- -te (Test email, only sends the email with the current print count)
- -e (Creates the record on database and sends the email with the print count it starts counting from 0 from this point forward)

## License

MIT License

**Free Software, Hell Yeah!**

Copyright (c) 2021 Leonel Faria

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
