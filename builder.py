# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

# This file contains the core logic to process given data and 
# build the final output.

from graphviz import Digraph
from builders.constants import VisualizationException, createInfoTable, supportedStructures
from builders.content import *
from builders.details import *


#########################################################################################
# The following functions contain builders for individual data structures
#########################################################################################
def buildSlotContext(byteData:list[int], name:list[str] = []) -> str:
  '''
  This function builds visualization for slot context data structure
  '''
  # Check if data is properly available
  if len(byteData) < 16:
    raise VisualizationException(f"Expecting at-least 16 bytes of data. Got {len(byteData)} bytes")
  
  # Get base data
  slotDiagram = slotContext(byteData)
  slotDescription = slotContextDetails(byteData)
  
  return createInfoTable("Slot Context",slotDiagram, slotDescription)

def buildEndpointContext(byteData:list[int], endpointType:str = "", name:list[str] = []) -> str:
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
  
  return createInfoTable(f"Endpoint {endpointType}Context",endpointDiagram, endpointDescription)


#########################################################################################
# The following functions contain logic for building chained/grouped data structures 
# containing more than 1 data structure
#########################################################################################

def buildDeviceContext(byteData:list[int]) -> Digraph:
  '''
  This function takes in raw data, processes it and builds a complex visualization of the 
  device context data structure.
  '''
  
  # Ensure that there are at-least 1024 elements in the byte array.
  # This is because Slot Context takes 32 bytes
  # Endpoint contexts take (32 endpoints) * 32 bytes each = 992
  if len(byteData) < 1024:
    raise VisualizationException(f"Device Context expects al-least 1024 bytes as input. Got {len(byteData)} bytes instead")
  
  # First split into slot data segment and endpoints data segment
  slotSegment:list[int] = byteData[:32] # 4 bytes per row * 8 rows
  endpointSegments:list[int] = byteData[32:] # Remaining Bytes will be for endpoint context
  
  # Create digraph item
  dot = Digraph()
  dot.clear()
  
  # Create a list to hold unique object names so that we can use it in mapping of contexts in graph
  name:list[str] = []
  
  # Build Slot Context
  slotContext = buildSlotContext(slotSegment,name)
  
  name.append(f"head")
  
  dot.node(name[-1],slotContext, shape='none')
  
  # Build The Endpoint Contexts
  for endpointNumber in range(31):
    if endpointNumber == 0:
      # This is a bi-directional endpoint
      endpointType = "0 - Bi-Directional "
    else:
      endpointType = f"{(endpointNumber//2)+(endpointNumber % 2)} {"- OUT" if endpointNumber % 2 == 1 else "- IN"} "
    
    name.append(f"Endpoint Context {endpointType}")
    endpointSegment = endpointSegments[(endpointNumber*32) : (endpointNumber+1)*32]
    dot.node(name[-1],buildEndpointContext(endpointSegment,endpointType,name), shape='none')

  for i in range(len(name)-1):
    dot.edge(name[i], name[i+1])
      
  return dot

#########################################################################################
# The following functions contain logic to decode inputs and call appropriate builders
#########################################################################################

def createStandaloneDS(byteData:list[int], struct:str) -> Digraph:
  '''
  This function helps visualize individual data structures instead of
  grouped data structures
  '''
  content = ""
  match (struct.strip().lower()):
    case "slotctx":
      content =  buildSlotContext(byteData)
    case "endpctx":
      content =  buildEndpointContext(byteData)
    case _:
      raise VisualizationException(f"Invalid Data Structure codename {struct}")

  # Create a Digraph and add this standalone data structure
  dot = Digraph()
  dot.clear()
  
  dot.node(f"head",content,shape='none')
  return dot
  
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
      return buildDeviceContext(byteData)
    case "ipctx":
      pass
    case _:
        # Creates standalone data structures 
        return createStandaloneDS(byteData,struct)

