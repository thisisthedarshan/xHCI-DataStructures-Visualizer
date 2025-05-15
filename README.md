# xHCI Data Structure Visualizer

A Python tool to visualize xHCI data structures using GraphViz. This is based on the xHCI Specification Rev 1.2b [Document Number 625472] which can be found here <https://cdrdv2-public.intel.com/625472/625472_xHCI_Rev1_2b.pdf>

## Setup

1. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Install GraphViz: Follow instructions at [GraphViz Downloads](https://graphviz.org/download/).

## Usage

Run the tool with data or a file to visualize xHCI structures.

### Input Options

- **Bytes (default)**: Space-separated bytes - Little Endian

  ```
  python main.py 03 00 07 04 08
  ```

- **32-bit Words**: Use `--word` flag  - Little Endian

  ```
  python main.py --word 03000704 08000000
  ```

- **File Input**: Use `--file` flag (add `--word` if 32-bit words)  

  ```
  python main.py --file data.txt [--word]
  ```

### Visualization Options

- **Direct Structure**: Specify structure with `--struct`  

  ```
  python main.py --struct <codename> 03 00 07 04 08
  ```
  See [Supported Data Structure](#supported-data-structures) for the codename to use

- **Interactive**: Omit `--struct` to prompt for structure type.

### Output

- Save visualization: Use `--save` flag  

  ```
  python main.py 03 00 07 04 08 --save output.png
  ```

- **Default outpu**t**: Saved as `xhci-Ds.png` if `--save` not specified.

## Supported Data Structures

| Type of Structure                     | codename |
----------------------------------------|----------|
| Device Context Data Structure         | `devctx` |
| Input Context Data Strcuture          | `ipctx`  |

## Flags and their usages

| Flag            | Additional Param |                                Usage                                       |
------------------|------------------|----------------------------------------------------------------------------|
| `--word`        |        N/A       | Indicates that the input is in 32-bit word format (32-bit raw data)        |
| `--file`        |  File Name/Path  | Tells the tool to pickup content from a file name which precedes this flag.|
| `--struct`      |  Struct CodeName | Informs the tool that it needs to visualize one of the Structures. The structure codenames can be found in the section [Supported Data Structures](#supported-data-structures) |
| `--save`        |   **filename**   | Tells the tool to save the visualization as **filename**.png               |

## Defaults

|  Default Value/behavior   |                                                          Explanation                                                               |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------------|
|      `xhci-Ds.png`        | The visualized file is saved with this default value unless filename is passed with `--save` flag                                  |
|Prompt User for DataStruct | By default, the tool prompts the user if he/she wants to decode a particular data structure unless told using `--struct` flag      |
|     Read as bytes         | By default assumes data is in 8-bit wide byte segments separated by spaces. Can be told its in 32-bit form using `--word` flag     |
|    Reads from STDIN       | Assumes data is being passed from STDIN, unless filename is passed using `--file` flag.                                            |
|    Little Endian System   | Always assumes data is in little endian format                                                                                     |
