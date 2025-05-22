# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

# This file contains the main executable and the primary data processing logic
# For the visualization tool

import argparse
import sys
import textwrap

from graphviz import Digraph

from builder import processAndBuildData
from helpers import addWatermark, addWatermarkDot, convert32BitToBytesArray
from builders.constants import supportedStructures, codenameWidth, descriptionWidth

def xHCIDataStructureVisualizer():
   '''
   ## `xHCIDataStructureVisualizer`

   ### Description
   Entry point for xHCI Data Structure Visualizer. Parses command-line arguments and visualizes xHCI data structures using GraphViz per xHCI Specification Rev 1.2b.

   ### Behavior
   1. **Argument Parsing**:
      - Uses `argparse` to handle:
      - `data`: Space-separated bytes or 32-bit words (STDIN or positional).
      - `--word`: Flag to interpret input as 32-bit words (default: bytes).
      - `--file`: Path to input file (overrides STDIN).
      - `--struct`: Structure codename (`devctx`, `ipctx`, etc.; prompts if omitted).
      - `--save`: Output filename (default: `xhci-Ds.png`).
      - `--render`: Render the generated file

   2. **Input Processing**:
      - Reads from `--file` if specified, else from `data` (STDIN).
      - Interprets as bytes (8-bit) or 32-bit words based on `--word`.
      - Assumes little-endian format.

   3. **Structure Selection**:
      - Uses `--struct` if provided.
      - Prompts user interactively if `--struct` is omitted.

   4. **Visualization**:
      - Generates GraphViz visualization of xHCI data structure.
      - Saves as `--save` filename (PNG) or `xHCI-Ds.png` if not specified.
      - Visualize it if `--render` is passed

   ### Returns
   - None (saves visualization to file & renders it).

   ### Example
   ```bash
   python3 xHCI-DS-Visualizer.py 03 00 07 04 08 --save output.png  # Bytes, saves as output.png
   python3 xHCI-DS-Visualizer.py --word 03000704 08000000  # 32-bit words, saves as xhci-Ds.png
   python3 xHCI-DS-Visualizer.py --file data.txt --struct devctx  # File input, Device Context
   ```
   '''
   # Create an info message containing supported data structures
   structsSupported = '\n'.join([f"|{k:<{codenameWidth}}| {v:<{descriptionWidth}}|" for k, v in supportedStructures.items()])
   parser = argparse.ArgumentParser(description="""
xHCI Data Structure Visualizer
A handy tool to visualize xHCI's Data Structures.

This tool is shared under the MIT License with the hope that it will be useful, but without any warranty.
To see the license, visit <https://github.com/thisisthedarshan/xHCI-DataStructures-Visualizer/blob/main/LICENSE>

The source code of this project is available on <https://github.com/thisisthedarshan/xHCI-DataStructures-Visualizer/>""",
formatter_class=argparse.RawTextHelpFormatter)
   parser.add_argument("--file", type=str, help="Path to input file")
   parser.add_argument("--save", type=str, help="Output filename for visualization", default="xHCI-DS")
   parser.add_argument("--render", action="store_true", help="Enable rendering")
   parser.add_argument("--struct", type=str, help=textwrap.dedent(f"""\
Tells tool to process data as a particular structure.
Supported Structures are:
 _____________________________________
| Codename  | Type of Data Structure  |
|-------------------------------------|
{structsSupported}
|___________|_________________________|
"""))
   parser.add_argument("--word", action="store_true", help="Input is of type 32-bit words")
   parser.add_argument("--pdf", action="store_true", help="Export as PDF instead of PNG")
   parser.add_argument("data", nargs="*", help="Input data (space/comma-separated)")
   
   args = parser.parse_args()
   
   rawDataIn:list[str] = []
   
   fileName = "xHCI-DS" if not args.save else args.save
   
   if args.file:
      try:
         with open(args.file,'r') as dataFile:
            rawDataIn = dataFile.read().strip().replace(",", " ").split()
      except:
         print("Couldn't read from file. Does the file exist?")
         sys.exit(-42)
      
   elif args.data and len(args.data)>= 4:
      rawDataIn = ' '.join(args.data).replace(",", " ").split()
   else:
      rawDataInput = input("Enter raw data separated by spaces\n")
      rawDataIn = rawDataInput.replace(",", " ").replace("  "," ").split()
   
   if len(rawDataIn) < 4:
      print("Size of data is too small to proceed. Exiting")
      sys.exit(-69)
   
   # Process Data to obtain final byte-wise data
   rawDataInt = [int(data,16) for data in rawDataIn]
   rawBytesData:list[int] = convert32BitToBytesArray(rawDataInt) if (args.word) else rawDataInt

   # Check if user has given a struct name. If not, prompt him/her to do so
   struct = args.struct
   
   if not struct:
      print("Select one of the available structures to decode from:")
      print(f"""
Supported Structures are:
 ______________________________________________
| Number | Codename  | Type of Data Structure  |
|--------|-----------|-------------------------|
{'\n'.join([f"| {format(idx+1,"02"):<{6}} |{k:<{codenameWidth}}| {v:<{descriptionWidth}}|" for idx, (k, v) in enumerate(supportedStructures.items())])}
|________|___________|_________________________|
""")
      option = int(input("Enter the number: "))
      if option > len(supportedStructures):
         print(f"Invalid option {option}. Expecting between 1 and {len(supportedStructures)}")
         sys.exit(-1)
      struct = list(supportedStructures)[option-1] 
   
   availableOptions = [codename.strip().lower() for codename in list(supportedStructures.keys())]
   if struct.strip().lower() not in availableOptions:
      print(f"Invalid Struct option {struct}.")
      sys.exit(-81)
      
   print(f"Selected option : {supportedStructures.get(struct,"")} ({struct})")

   names:list[str] = []

   dot = Digraph()
   dot.clear()
   dot = processAndBuildData(struct, rawBytesData, names)
   
   if args.pdf:
      # Process to add a watermark :)
      addWatermarkDot(dot, names)
      dot.render(fileName,format='pdf',view=args.render,cleanup=True)
   else:
      dot.render(fileName,format='png',view=args.render,cleanup=True)
      addWatermark(fileName+".png")
  
if __name__ == "__main__":
  xHCIDataStructureVisualizer()
