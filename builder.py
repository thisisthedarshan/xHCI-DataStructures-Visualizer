# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

# This file contains the core logic to process given data and 
# build the final output.

from graphviz import Digraph
from builders.constants import VisualizationException, supportedStructures
from builders.content import slotContext
from builders.details import slotContextDetails
from random import randint as unique

def buildSlotContext(byteData:list[int]) -> Digraph:
  '''
  This function builds visualization for slot context data structure
  '''
  # Check if data is properly available
  if len( byteData) < 16:
    raise VisualizationException(f"Expecting at-least 16 bytes of data. Got {len(byteData)} bytes")
  
  # Get base data
  slotDiagram = slotContext(byteData)
  slotDescription = slotContextDetails(byteData)
  
  # Create a rect and add this data
  table = f"""<
  <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="1">
    <TR> <TD COLSPAN="36"><B> SLOT CONTEXT </B></TD></TR>
    <TR> 
         <TD> {slotDiagram} </TD> 
    </TR>
    <TR > <TD HEIGHT="21"></TD> </TR>
    <TR> <TD COLSPAN="12">DESCRIPTION</TD> </TR>
    <TR> 
         <TD> {slotDescription} </TD> 
    </TR>
  </TABLE>
>
"""
  # We have the table, build a Digraph item from it.
  dot = Digraph()
  dot.clear()
  dot.node(f"Slot Context # {unique(69,420)}",table,shape='none')
  return dot
  


def createStandaloneDS(byteData:list[int], struct:str) -> Digraph:
  '''
  This function helps visualize individual data structures instead of
  grouped data structures
  '''
  print(struct.lower())
  match (struct.strip().lower()):
    case "slotctx":
      return buildSlotContext(byteData)
    case _:
      raise VisualizationException(f"Invalid Data Structure codename {struct}")


def createDeviceContextDS(byteData:list[int]) -> str:
  '''
  This function takes in raw data and returns a GraphViz object representing
  the complete Device Context Data Structure
  '''
  # Ensure that the byteData is at-least 256-bytes 
  if len(byteData) < 256:
    raise VisualizationException("Size of the data for Device Context is invalid")


def processAndBuildData(struct:str, byteData:list[int]) -> Digraph:
  '''
  This function is responsible for processing input and selecting data structure
  to create the final visuals. The function can process individual data structures
  like Slot Context, Endpoint Context, TRB etc. Or complex/combined data structures
  like Device Context Data Structure, Input Context Data Structure etc.
  '''
  
  dot = Digraph()
  dot.clear()
  result = ""
  match struct:
    case "devctx":
      pass
    case "ipctx":
      pass
    case _:
        # Creates standalone data structures 
        return createStandaloneDS(byteData,struct)

