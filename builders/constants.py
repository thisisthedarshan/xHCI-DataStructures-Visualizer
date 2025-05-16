# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

# This file contains constants and mapping to specific values from data structures

class VisualizationException(Exception):
  '''Custom Exception creation function'''
  pass


# Define widths for codename and description for better looks in help message
codenameWidth = 11
descriptionWidth = 24
# This holds the list of supported data structures for the tool
supportedStructures:dict[str, str] = {
    "slotctx "    : "Slot Context"
}


def RsvdZ(numberOfBits:int = 8) -> str:
  '''This function returns 0's to represent Reserved Zero Default values'''
  return '0'*numberOfBits

def mapRouteString(routeBytes:list[int]) -> list[int]:
  ''' This function maps a list of 3-bytes to a 20-bit route list'''
  return [
    (routeBytes[3] & 0xF), ((routeBytes[3]>>4) & 0xF),
    (routeBytes[2] & 0xF), ((routeBytes[2]>>4) & 0xF),
    (routeBytes[1] & 0xF)
    ]

def mapTTThinkTime(bit2ttThinkTime:int) -> str :
  '''This function maps a 2-bit think time value to respective description'''
  ttThinkTimeDescription:str = "Invalid Input Given"
  match bit2ttThinkTime:
    case 0:
      ttThinkTimeDescription = "TT requires at most 8 FS bit times of inter-transaction gap on a full-/low-speed downstream bus."
    case 1:
      ttThinkTimeDescription = "TT requires at most 16 FS bit times."
    case 2:
      ttThinkTimeDescription = "TT requires at most 24 FS bit times."
    case 3:
      ttThinkTimeDescription = "TT requires at most 32 FS bit times."
  
  return ttThinkTimeDescription

def mapSlotState(bit5SlotStateCode:int) -> str:
  ''' This function maps a 5-bit slot state to string equivalent'''
  slotState:str = "Reserved"
  match bit5SlotStateCode:
    case 0:
      slotState = "Disabled/Enabled State"
    case 1:
      slotState = "Default State"
    case 2:
      slotState = "Addressed State"
    case 3:
      slotState = "Configured State"
      
  return slotState

