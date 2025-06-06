# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

# This file contains the Graphviz code templates to create tables for a given
# xHCI Data Structure. It also contains data that is used to build info for that
# Data-structure.

from builders.constants import RsvdZ
from helpers import bytes2binList

def slotContext(data:list[int]):
  '''This function dumps data from input to a table form, representing'''
  
  # Convert Data to integer list
  rawBinData = bytes2binList(data)
  
  # Now split them according to rows and reverse-order them
  row1 = rawBinData[0]
  row2 = rawBinData[1]
  row3 = rawBinData[2]
  row4 = rawBinData[3]
  # Create a reserved segment
  reservedSegment32 = RsvdZ(32)
  
  # Build the table
  return f"""
<table border="1" cellborder="1" cellspacing="0" cellpadding="4">
    <!-- Row 0: Bits -->
    <tr>
        {''.join(f'<td colspan="4"><b>{format(i,"02")}</b></td>\n' for i in reversed(range(32)))}
    </tr>
    <!-- Row 1: Context Entries to Route String -->
    <tr>
        <td colspan="20"><b>Context Entries</b></td>
        <td colspan="4"><b>Hub</b></td>
        <td colspan="4"><b>MTT</b></td>
        <td colspan="4"><b>RsvdZ</b></td>
        <td colspan="16"><b>Speed</b></td>
        <td colspan="80"><b>Route String</b></td>
        <td><b>03-00H</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row1)}
        <td>—</td>
    </tr>
    <!-- Row 2: Number of Ports & Root Hub Port -->
    <tr>
        <td colspan="32"><b>Number of Ports</b></td>
        <td colspan="32"><b>Root Hub Port Number</b></td>
        <td colspan="64"><b>Max Exit Latency</b></td>
        <td><b>07-04H</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row2)}
        <td>—</td>
    </tr>
    <!-- Row 3: Interrupter Target to TT Hub Slot ID -->
    <tr>
        <td colspan="40"><b>Interrupter Target</b></td>
        <td colspan="16"><b>RsvdZ</b></td>
        <td colspan="8"><b>TTT</b></td>
        <td colspan="32"><b>TT Port Number</b></td>
        <td colspan="32"><b>TT Hub Slot ID</b></td>
        <td ><b>0B-08H</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row3)}
        <td>—</td>
    </tr>
    <!-- Row 4: Slot State and USB Device Address -->
    <tr>
        <td colspan="20"><b>Slot State</b></td>
        <td colspan="76"><b>RsvdZ</b></td>
        <td colspan="32"><b>USB Device Address</b></td>
        <td><b>0F-0CH</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row4)}
        <td>—</td>
    </tr>
    <!-- Reserved rows -->
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>13-10H</b></td>
    </tr>
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>17-14H</b></td>
    </tr>
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>1B-18H</b></td>
    </tr>
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>1F-1CH</b></td>
    </tr>
</table>
"""

def endpointContext(data:list[int]):
    '''This function creates an endpoint context data structure '''
    
    rawBinData = bytes2binList(data)
  
    # Now split them according to rows and reverse-order them
    row1 = rawBinData[0][::-1]
    row2 = rawBinData[1][::-1]
    row3 = rawBinData[2][::-1]
    row4 = rawBinData[3][::-1]
    row5 = rawBinData[4][::-1]
    # Create a reserved segment
    reservedSegment32 = RsvdZ(32)
  
    return f"""
<table border="1" cellborder="1" cellspacing="0" cellpadding="4">
    <!-- Row 0: Bits -->
    <tr>
        {''.join(f'<td colspan="4"><b>{format(i,"02")}</b></td>\n' for i in reversed(range(32)))}
    </tr>
    
    <!-- Row 1-->
    <tr>
        <td colspan="32"><b>Max ESIT Payload Hi</b></td>
        <td colspan="32"><b>Interval</b></td>
        <td colspan="4"><b>LSA</b></td>
        <td colspan="20"><b>Max Primary Streams</b></td>
        <td colspan="8"><b>Mult</b></td>
        <td colspan="20"><b>RsvdZ</b></td>
        <td colspan="12"><b>Endpoint State</b></td>
        <td><b>03-00H</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row1)}
        <td>—</td>
    </tr>
    
    <!-- Row 2 -->
    <tr>
        <td colspan="64"><b>Max Packet Size</b></td>
        <td colspan="32"><b>Max Burst Size</b></td>
        <td colspan="4"><b>HID</b></td>
        <td colspan="4"><b>RsvdZ</b></td>
        <td colspan="12"><b>EP Type</b></td>
        <td colspan="8"><b>CErr</b></td>
        <td colspan="4"><b>RsvdZ</b></td>
        <td><b>07-04H</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row2)}
        <td>—</td>
    </tr>
    
    <!-- Row 3 -->
    <tr>
        <td colspan="108"><b>TR Dequeue Pointer Lo</b></td>
        <td colspan="16"><b>RsvdZ</b></td>
        <td colspan="4"><b>DCS</b></td>
        <td ><b>0B-08H</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row3)}
        <td>—</td>
    </tr>
    
    <!-- Row 4 -->
    <tr>
        <td colspan="128"><b>TR Dequeue Pointer Hi</b></td>
        <td><b>0F-0CH</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row4)}
        <td>—</td>
    </tr>
    
    <!-- Row 5 -->
    <tr>
        <td colspan="64">Average TRB Length</td>
        <td colspan="64">Max ESIT Payload Lo</td>
        <td><b>13-10H</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row5)}
        <td>—</td>
    </tr>
    
    <!-- Row 6 -->
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>17-14H</b></td>
    </tr>
    
    <!-- Row 7 -->
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>1B-18H</b></td>
    </tr>
    
    <!-- Row 8 -->
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>1F-1CH</b></td>
    </tr>
</table>
"""

def inputControlContextContext(data:list[int]):
    '''This function creates an input control context data structure '''
    
    rawBinData = bytes2binList(data)
  
    # Now split them according to rows and reverse-order them
    row1 = rawBinData[0][::-1]
    row2 = rawBinData[1][::-1]
    row8 = rawBinData[7][::-1]
    
    # Create a reserved segment
    reservedSegment32 = RsvdZ(32)
  
    return f"""
<table border="1" cellborder="1" cellspacing="0" cellpadding="4">
    <!-- Row 0: Bits -->
    <tr>
        {''.join(f'<td colspan="4"><b>{format(i,"02")}</b></td>\n' for i in reversed(range(32)))}
    </tr>
    
    <!-- Row 1-->
    <tr>
        <td colspan="4"><b>D31</b></td>
        <td colspan="4"><b>D30</b></td>
        <td colspan="4"><b>D29</b></td>
        <td colspan="4"><b>D28</b></td>
        <td colspan="4"><b>D27</b></td>
        <td colspan="4"><b>D26</b></td>
        <td colspan="4"><b>D25</b></td>
        <td colspan="4"><b>D24</b></td>
        <td colspan="4"><b>D23</b></td>
        <td colspan="4"><b>D22</b></td>
        <td colspan="4"><b>D21</b></td>
        <td colspan="4"><b>D20</b></td>
        <td colspan="4"><b>D19</b></td>
        <td colspan="4"><b>D18</b></td>
        <td colspan="4"><b>D17</b></td>
        <td colspan="4"><b>D16</b></td>
        <td colspan="4"><b>D15</b></td>
        <td colspan="4"><b>D14</b></td>
        <td colspan="4"><b>D13</b></td>
        <td colspan="4"><b>D12</b></td>
        <td colspan="4"><b>D11</b></td>
        <td colspan="4"><b>D10</b></td>
        <td colspan="4"><b>D9</b></td>
        <td colspan="4"><b>D8</b></td>
        <td colspan="4"><b>D7</b></td>
        <td colspan="4"><b>D6</b></td>
        <td colspan="4"><b>D5</b></td>
        <td colspan="4"><b>D4</b></td>
        <td colspan="4"><b>D3</b></td>
        <td colspan="4"><b>D2</b></td>
        <td colspan="8"><b>RsvdZ</b></td>
        <td><b>03-00H</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row1)}
        <td>—</td>
    </tr>
    
    <!-- Row 2 -->
    <tr>
        <td colspan="4"><b>A31</b></td>
        <td colspan="4"><b>A30</b></td>
        <td colspan="4"><b>A29</b></td>
        <td colspan="4"><b>A28</b></td>
        <td colspan="4"><b>A27</b></td>
        <td colspan="4"><b>A26</b></td>
        <td colspan="4"><b>A25</b></td>
        <td colspan="4"><b>A24</b></td>
        <td colspan="4"><b>A23</b></td>
        <td colspan="4"><b>A22</b></td>
        <td colspan="4"><b>A21</b></td>
        <td colspan="4"><b>A20</b></td>
        <td colspan="4"><b>A19</b></td>
        <td colspan="4"><b>A18</b></td>
        <td colspan="4"><b>A17</b></td>
        <td colspan="4"><b>A16</b></td>
        <td colspan="4"><b>A15</b></td>
        <td colspan="4"><b>A14</b></td>
        <td colspan="4"><b>A13</b></td>
        <td colspan="4"><b>A12</b></td>
        <td colspan="4"><b>A11</b></td>
        <td colspan="4"><b>A10</b></td>
        <td colspan="4"><b>A9</b></td>
        <td colspan="4"><b>A8</b></td>
        <td colspan="4"><b>A7</b></td>
        <td colspan="4"><b>A6</b></td>
        <td colspan="4"><b>A5</b></td>
        <td colspan="4"><b>A4</b></td>
        <td colspan="4"><b>A3</b></td>
        <td colspan="4"><b>A2</b></td>
        <td colspan="4"><b>A1</b></td>
        <td colspan="4"><b>A0</b></td>
        <td><b>07-04H</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row2)}
        <td>—</td>
    </tr>
    
    <!-- Row 3 -->
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>1B-18H</b></td>
    </tr>
    
    <!-- Row 4 -->
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>1B-18H</b></td>
    </tr>
    
    <!-- Row 5 -->
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>1B-18H</b></td>
    </tr>
    
    <!-- Row 6 -->
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>17-14H</b></td>
    </tr>
    
    <!-- Row 7 -->
    <tr>
        <td colspan="128">{reservedSegment32}</td>
        <td><b>1B-18H</b></td>
    </tr>
    
    <!-- Row 8 -->
    <tr>
        <td colspan="32"><b>Configuration Value</b></td>
        <td colspan="32"><b>Interface Number</b></td>
        <td colspan="32"><b>Alternate Setting</b></td>
        <td colspan="32"><b>RsvdZ</b></td>
        <td><b>1F-1CH</b></td>
    </tr>
    <tr>
        {''.join(f'<td colspan="4">{bit}</td>' for bit in row8)}
        <td>—</td>
    </tr>
</table>
"""