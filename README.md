# PDFinjector
----
PDFinjector can insert javascript code in pdf files, useful for testing the security of a browser, for social engineering or just for fun. it can obfuscate the payload and has a lot of pre-built-in payloads
# Screenshot
----
classic use with PDFinjector
![PDFinjector](https://github.com/H4k1l/PDFinjector/blob/main/images/1.png)
use of PDFinjector alongside with JSfuck
![PDFinjector](https://github.com/H4k1l/PDFinjector/blob/main/images/2.png)
use of the pre-built-in payloads
![PDFinjector](https://github.com/H4k1l/PDFinjector/blob/main/images/3.png)
# Usage
----
```python3 .\PDFinjector.py -h
     __     _____ ____  _____
|--_ /_-| |    ||    \|  __| _  __ _  _    ___  ___  ___  ___  ___
|  / /  | | |__|| |  ||  __|| || \  || |_ | __|/ __||_ _||   || |_|
|--/----| |__|  |____/|__|  |_||_|\_|| / /|_--|\___| |_| |___||_\_\ V1.0
usage: PDFinjector.py [-h] -f FILE [-o OUTPUT] [-cp CUSTOMPAYLOAD | -cfp CUSTOMFILEPAYLOAD] [-ob]

PDFinjector can insert javascript code in pdf files, perfect for social engineering.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  the input file
  -o OUTPUT, --output OUTPUT
                        the output file, if not set it will overwrite the input file
  -cp CUSTOMPAYLOAD, --custompayload CUSTOMPAYLOAD
                        the custom payload to inject, via text
  -cfp CUSTOMFILEPAYLOAD, --customfilepayload CUSTOMFILEPAYLOAD
                        the custompayload to inject, via file.js
  -ob, --obfuscate      obfuscate the code using jsfuck
```
# Disclaimer
----
The author is not responsible for any damages, misuse or illegal activities resulting from the use of this code.
