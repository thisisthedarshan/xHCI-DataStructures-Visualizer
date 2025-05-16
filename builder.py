# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

# This file contains the core logic to process given data and 
# build the final output.

from graphviz import Digraph
from builders.constants import VisualizationException, createInfoTable, supportedStructures
from builders.content import *
from builders.details import *
from random import randint as unique

def buildSlotContext(byteData:list[int]) -> Digraph:
  '''
  This function builds visualization for slot context data structure
  '''
  # Check if data is properly available
  if len(byteData) < 16:
    raise VisualizationException(f"Expecting at-least 16 bytes of data. Got {len(byteData)} bytes")
  
  # Get base data
  slotDiagram = slotContext(byteData)
  slotDescription = slotContextDetails(byteData)
  
  # Create a rect and add this data
  table = createInfoTable("Slot Context",slotDiagram, slotDescription)
  
  # We have the table, build a Digraph item from it.
  dot = Digraph()
  dot.clear()
  dot.node(f"Slot Context #{unique(69,420)}",table,shape='none')
  return dot
  

def buildEndpointContext(byteData:list[int], endpointNumber:int=-1) -> Digraph:
  '''
  This function takes in raw bytes, decodes it and creates a visualization of 
  endpoint context data structure. Endpoint number = -1 indicates that we don't know which
  endpoint this data belongs to!
  '''
  
  if len(byteData) < 20: # 4 bytes per row *5 rows since remaining are 0
    raise VisualizationException(f"Expecting at-least 16 bytes of data. Got {len(byteData)} bytes")

  # Get the content
  endpointDiagram = endpointContext(byteData)
  endpointDescription = endpointContextDetails(byteData)
  
  # Create a rect and add this data
  table = createInfoTable(f"Endpoint {endpointNumber if (endpointNumber!= -1) else ''} Context",endpointDiagram, endpointDescription)
  
  # We have the table, build a Digraph item from it.
  dot = Digraph()
  dot.clear()
  dot.node(f"Endpoint Context {endpointNumber if (endpointNumber!= -1) else ''} #{unique(69,420)}",table,shape='none')
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
    case "endpctx":
      return buildEndpointContext(byteData)
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

