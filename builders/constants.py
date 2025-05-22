# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

# This file contains constants and mapping to specific values from data structures

class VisualizationException(Exception):
  '''Custom Exception creation function'''
  pass


# Define widths for codename and description for better looks in help message
codenameWidth = 12
descriptionWidth = 24
# This holds the list of supported data structures for the tool
supportedStructures:dict[str, str] = {
    "slotctx "    : "Slot Context",
    "endpctx "    : "Endpoint Context",
    "icctx"       : "Input Control Context",
    "devctx "     : "Device Context",
    "ipctx "      : "Input Context",
}

# This function returns a data structure and its description graph item by
# using them on a template
def createInfoTable(structureName:str, dataStructure:str, description:str) -> str:
  '''
  This function returns a formatted (templated) data-structure + description as a string.
  This function was created since the template remained the same across all functions.
  '''
  return f"""<
  <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="1">
    <TR > <TD HEIGHT="21"><br></br></TD> </TR>
    <TR> <TD COLSPAN="36"><B> {structureName} </B></TD></TR>
    <TR> 
         <TD> {dataStructure} </TD> 
    </TR>
    <TR > <TD HEIGHT="21"><br></br></TD> </TR>
    <TR> <TD COLSPAN="12">DESCRIPTION</TD> </TR>
    <TR> 
         <TD> {description} </TD> 
    </TR>
  </TABLE>
>"""

def RsvdZ(numberOfBits:int = 8) -> str:
  '''This function returns 0's to represent Reserved Zero Default values'''
  return '0'*numberOfBits

def mapRouteString(routeBytes:list[int]) -> list[int]:
  ''' This function maps a list of 3-bytes to a 20-bit route list'''
  return [
    (routeBytes[1] & 0xF), ((routeBytes[2]>>4) & 0xF),
    (routeBytes[2] & 0xF), ((routeBytes[3]>>4) & 0xF),
    (routeBytes[3] & 0xF)
    ]

def mapTTThinkTime(bit2ttThinkTime:int) -> str :
  '''This function maps a 2-bit think time value to respective description'''
  ttThinkTimeMap = {
    0 : "TT requires at most 8 FS bit times of inter-transaction gap on a full-/low-speed downstream bus.",
    1 : "TT requires at most 16 FS bit times.",
    2 : "TT requires at most 24 FS bit times.",
    3 : "TT requires at most 32 FS bit times."
  }
  return ttThinkTimeMap.get(bit2ttThinkTime, "Invalid Input Given")

def mapSlotState(bit5SlotStateCode:int) -> str:
  ''' This function maps a 5-bit slot state to string equivalent'''
  slotStates = {
    0 : "Disabled/Enabled State",
    1 : "Default State",
    2 :"Addressed State",
    3 :"Configured State"
  }
  
  return slotStates.get(bit5SlotStateCode,"Reserved")

def mapEndpointState(bit3EpState:int) -> str:
  '''This function maps a 3-bit endpoint state code to respective string'''
  endpointStateMap = {
    0 : "Disabled",
    1 : "Running",
    2 : "Halted",
    3 : "Stopped",
    4 : "Error"
  }
  
  return endpointStateMap.get(bit3EpState,"Reserved")

def mapEPType(bit3EpTypeCode:int) -> str:
  '''This function maps a 3-bit endpoint code to respective type and direction string'''
  epTypeMap = {
    1 : "Isoch Out",
    2 : "Bulk Out",
    3 : "Interrupt Out",
    4 : "Control - Bidirectional",
    5 : "Isoch In",
    6 : "Bulk In",
    7 : "Interrupt In",
  }
  
  return epTypeMap.get(bit3EpTypeCode, "Invalid Type!")


