# Ant Colony Optimisation (ACO)


## Table Of Contents

- [Description](#description)
- [Prerequisties](#prereusites)
- [How To Use](#how-to-use)
- [License](#license)
- [Author Info](#author-info)

## Description
The code is set out to solve a TSP problem using ACO. The code takes in the TSP problem from an XML file and peforms one trial of the ACO algorithm on it. The program returns the best fitness found by the ants in the trial. The program also allows for applying the Elitist ACO algorithm.

## Prerequisties
1. Python 3.9+
2. Numpy 1.24.2

## How to Use
- To use the program make sure the XML files are in the same directory as ACO.py.
- To change between Burma and Brazil, simply change the parameter for the xml_decoder on line 251 to which ever is desired (brazil, burma)
- If you wish to perform the Elitist ACO variation change the global constant ELITIST to True (line 28)
- Adjusting the settings of the algorithm can be done by changing the values of the global constants as desired (line 22-29)

## License
MIT

Copyright (c) [2023] [Jude Wallace]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## Author Info

- GitHub - [@Jude Wallace](https://github.com/JudeWallace?tab=repositories)