'''
Python programm, which extracts a jmic microprogram and exports its content as html table(s)

This project is licensed under the terms of the MIT license

The most mappings were taken from the JMIC application (v. 1.4) (c) TUM
http://wwwi10.lrr.in.tum.de/~eti/Vorlesung/WS1415/Software/jmic-1.4.jar

Created on Oct 5, 2016

@author: Jonas Donhauser
'''

HIGHLIGHT_CLASS = "highlight"
WRAPPER = "<!DOCTYPE html><html><head>{}</head><body>{}</body></html>"
USE_LOWER_CASE_FUNC = False

import sys

def end():
    print("Usage: jmic.py [-options] input output")
    print("       Whitespaces in a path must be escaped with '\\'")
    print("Example: jmic.py -i -css=style.css input.mpr output.html")
    
    print("\nOptions:")
    print("-css=example.css   Link a css file")
    print("-f=mwe,cmd,test    Filter: Display only the listed columns (seperate with,)")
    print("-h                 Help!")
    print("-i                 Ignore IFETCH (Opcode 0x0)")
    print("-m                 Merge 1bit cells")
    print("-nobits            Do not display the used bit-width of each column")
    print("-nodesc            Do not set the cell title to the long description")
    print("-nofunc            Do not display the function names as table head")
    print("-nohighlight       Do not highlight non default entries")
    print("-noname            Do not display the instruction name")
    print("-noopcodes         Do not display the opcode of each row")
    print("-nowrap            Do not generate the html outline (html, head, body)")
    print("-r                 Reverse the horizontal order of the table")
    print("-s                 Split the program into separate tables for each MA instruction")
    
    sys.exit(0)

# Options
css = None
wrap = True
use_highlight = True
sort_reversed = False
show_ifetch = True
descriton = True
split = False
show_name = True
show_op = True
show_func = True
show_bits = True
merge = False
filter_funcs = []

FUNC = ['MWE', 'IR_LD', 'BZ_EA', 'BZ_INC', 'BZ_ED', 'BZ_LD', 'BAR', 'CMD', 'CCEN',
         'TEST', 'SR', 'CEM', 'CE', 'Shift', 'CIN-MUX', 'DBUS', 'ABUS', 'BSEL', 'RB_Addr',
         'ASEL', 'RA_Addr', 'Dest', 'Func', 'Src', 'Konst', 'KMUX', 'I-rupt', 'IE']

FUNC_LONG = ['Memory-Write-Enable', 'Instruktionsregister Laden', 'Befehlsz&auml;hler Enable Adressbus',
              'Befehlsz&auml;hler Inkrement', 'Befehlsz&auml;hler Enable Datenbus', 'Befehlsz&auml;hler Laden',
              'Direktdatenfeld', 'Fortschaltbefehle des Am2910', 'Condition Code Enable Am2910',
              'Instruktionen des Am2904 - Test', 'Instruktionen des Am2904 - Statusregister',
              'Enablebit f&uuml;r das MSR', 'Enablebit f&uuml;r das uSR', 'Instruktionsbit des Am2904 - Schiebesteuerung',
              'Instruktionsbit des Am2904-&Uuml;bertragssteuerung', 'Datenbus Select',
              'Adressbus Select', 'RB ADDR Select', 'Register B Adresse', 'RA ADDR Select',
              'Register A Adresse', 'Instruktionsbit des Am2901 - ALU Zielsteuerung',
              'Instruktionsbit des Am2901 - ALU Funktionen', 'Instruktionsbit des Am2901-ALU Quelloperanden',
              'Konstantenfeld', 'D-Eingang Select', 'Interruptsteuerung', 'Interrupt Enable']

if USE_LOWER_CASE_FUNC: FUNC[:] = [x.lower() for x in FUNC]

BIT_MAP = [(0, 0),(1, 1),(2, 2),(3, 3),(4, 4),(5, 5),
       (6, 17),(18, 21),(22, 22),(23, 26),(27, 28),(29, 29),(30, 30),
       (31, 34),(35, 36),(37, 37),(38, 38),(39, 39),(40, 43),
       (44, 44),(45, 48),(49, 51),(52, 54),(55, 57),(58, 73),
       (74, 74),(75, 78),(79, 79)
]

""" Changed: 
        sr: 0 instead of 4
        bar: IFETCH instead of 0
        shift: <> encoded for HTML
"""
MNEMOS = [('W', 'R'), # MWE
          ('L', 'H'), # IR_LD
          ('E', 'H'), # BZ_EA
          ('I', 'H'), # BZ_INC
          ('E', 'H'), # BZ_ED
          ('L', 'H'), # BZ_LD
          ('IFETCH', ), # BAR
          ('JZ', 'JCS', 'JMAP', 'CJP', 'PUSH', 'JSRP', 'CJV', 'JRP', 'RFCT', 'RPCT', 'CRTN', 'CJPP', 'LDCT', 'LOOP', 'CONT', 'TWB'), # CMD
          ('C', 'PS'), # CCEN
          ('SGT', 'SLTEQ', 'SGTEQ', 'SLT', 'NZ', 'Z', 'NOVR', 'OVR', 'NCOZ', 'COZ', 'ULT', 'UGTEQ', 'UGT', 'ULTEQ', 'NNEG', 'NEG'), # TEST
          ('0', 'MI', 'MA'), # SR
          ('L', 'H'), # CEM
          ('L', 'H'), # CE
          ('RSL', 'RSH', 'RSCONI', 'RSDH', 'RSDC', 'RSDN', 'RSDL', 'RSDCO', 'RSRCO', 'RSRCIO', 'RSR', 'RSDIC', 'RSDRCI', 'RSDRCO', 'RSDXOR', 'RSDR',
           'LSLCO', 'LSHCO', 'LSL', 'LSH', 'LSDLCO', 'LSDHCO', 'LSDL', 'LSDH', 'LSCRO', 'LSCRIO', 'LSR', 'LSLICI', 'LSDCIO', 'LSDRCO', 'LSDCI', 'LSDR'), # Shift
          ('CI0', 'CI1', 'CIX', 'CIC'), # CIN-MUX
          ('DB', 'H'), # DBUS
          ('AB', 'H'), # ABUS
          ('IR', 'MR'), # BSEL
          (), # RB_Addr
          ('IR', 'MR'), # ASEL
          (), # RA_Addr
          ('QREG', 'NOP', 'RAMA', 'RAMF', 'RAMQD', 'RAMD', 'RAMQU', 'RAMU'), # Dest
          ('ADD', 'SUBR', 'SUBS', 'OR', 'AND', 'NOTRS', 'EXOR', 'EXNOR'), # Func
          ('AQ', 'AB', 'ZQ', 'ZB', 'ZA', 'DA', 'DQ', 'DZ'), # Src
          (), # Konst
          ('K', 'D'), # KMUX
          ('LDM', 'RDM', 'CLM', 'STM', 'BCLM', 'BSTM', 'LDST', 'RDST', 'ENI', 'DISI', 'RDVC', 'CLI', 'CLMR', 'CLMB', 'CLVC', 'MCL'), # I-rupt
          ('IE', 'Dis')] # IE

LONG = [  ('Write', 'Read'), # MWE
          ('Load', 'Hold'), # IR_LD
          ('Enable', 'Hold'), # BZ_EA
          ('Increment', 'Hold'), # BZ_INC
          ('Enable', 'Hold'), # BZ_ED
          ('Load', 'Hold'), # BZ_LD
          ('IFETCH', ), # BAR
          ('Jump Zero', 'Cond JSB PL', 'Jump Map', 'Cond Jump PL', 'Push/Cond Ld Cntr', 'Cond JSB R/PL', 'Cond Jump Vector', 'Cond Jump R/PL',
           'Repeat Loop CNTR0', 'Repeat PL CNTR0', 'Cond Rtn', 'CJP & Pop', 'Ld Cntr & Cont', 'Test End Loop', 'Continue', '3-Way-Branch'), # CMD
          ('Condition', 'Pass'), # CCEN
          ('signed &gt;', 'signed &lt;=', 'signed &gt;=', 'signed &lt;', '!=', '=', 'not Overflow', 'Overflow', 'not (CZ)', 'CZ', 'unsigned &lt;', 'unsigned &gt;=',
           'unsigned &gt;', 'unsigned &lt;=', 'not N', 'N'), # TEST
          ('0', 'SR', 'MSR'), # SR
          ('Load', 'Hold'), # CEM
          ('Load', 'Hold'), # CE
          ('RSL', 'RSH', 'RSCONI', 'RSDH', 'RSDC', 'RSDN', 'RSDL', 'RSDCO', 'RSRCO', 'RSRCIO', 'RSR', 'RSDIC', 'RSDRCI', 'RSDRCO', 'RSDXOR', 'RSDR',
           'LSLCO', 'LSHCO', 'LSL', 'LSH', 'LSDLCO', 'LSDHCO', 'LSDL', 'LSDH', 'LSCRO', 'LSCRIO', 'LSR', 'LSLICI', 'LSDCIO', 'LSDRCO', 'LSDCI', 'LSDR'), # Shift
          ('CI0', 'CI1', 'CIX', 'CIC'), # CIN-MUX
          ('Datenbus', 'Hold'), # DBUS
          ('Adressbus', 'Hold'), # ABUS
          ('Maschineninstruktion', 'Mikroinstruktion'), # BSEL
          (), # RB_Addr
          ('Maschineninstruktion', 'Mikroinstruktion'), # ASEL
          (), # RA_Addr
          ('QREG', 'NOP', 'RAMA', 'RAMF', 'RAMQD', 'RAMD', 'RAMQU', 'RAMU'), # Dest
          ('ADD', 'SUBR', 'SUBS', 'OR', 'AND', 'NOTRS', 'EXOR', 'EXNOR'), # Func
          ('AQ', 'AB', 'ZQ', 'ZB', 'ZA', 'DA', 'DQ', 'DZ'), # Src
          (), # Konst
          ('Konstante', 'Datenbus'), # KMUX
          ('LDM', 'RDM', 'CLM', 'STM', 'BCLM', 'BSTM', 'LDST', 'RDST', 'ENI', 'DISI', 'RDVC', 'CLI', 'CLMR', 'CLMB', 'CLVC', 'MCL'), # I-rupt
          ('Enable', 'Disable')] # IE


MERGE_CELLS = [(0,5),(11,12),(15,16)]
# You must add tags here!
if descriton:
    MERGE_FUNC = ['<span title="{0}">MWE</span> / <span title="{1}">IR_LD</span> / <span title="{2}, {3}, {4}, {5}">BZ</span>',
                   '', '<span title="{15}, {16}">D/ABUS</span>']
else: 
    MERGE_FUNC = ['<span>MWE</span> / <span>IR_LD</span> / <span>BZ</span>',
                   '', '<span>D/ABUS</span>']
MERGE_FUNC[:] = [x.format(*FUNC_LONG) for x in MERGE_FUNC]
if USE_LOWER_CASE_FUNC: MERGE_FUNC[:] = [x.lower() for x in MERGE_FUNC]

# JMIC default row
default = [1, 1, 1, 1, 1, 1, 0, 14, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1]

# Basic check for correct mapping
if len(set((len(FUNC), len(BIT_MAP), len(MNEMOS), len(LONG), len(FUNC_LONG)))) > 1: 
    print("ERROR: mapping wrong..")
    sys.exit(0)


# Load params
if len(sys.argv)<3: end()
else: 
    for arg in sys.argv[1:-2]:
        if arg[:5] == "-css=": css = arg[5:]
        elif arg[:3] == "-f=": filter_funcs = [v.lower() for v in arg[3:].split(",")]
        elif arg == "-nowrap": wrap = False
        elif arg == "-nohighlight": use_highlight = False
        elif arg == "-r": sort_reversed = True
        elif arg == "-i": show_ifetch = False
        elif arg == "-h": end()
        elif arg == "-nodesc": descriton = False
        elif arg == "-s": split = True
        elif arg == "-m": merge = True
        elif arg == "-noname": show_name = False
        elif arg == "-noopcodes": show_op = False
        elif arg == "-nofunc": show_func = False
        elif arg == "-nobits": show_bits = False
        else: 
            print("Unknown option: "+arg)
            end()
    file_name = sys.argv[-1]
    input_file = sys.argv[-2]

print("Writing to: "+file_name)


def get_data(file):
    """
    Reads a .jmic file
    
    Args:
        file: File name
        
    Returns:
        mi-program as list
    """
    d = []
    start = False
    with open(file, 'r') as f:
        for l in f:
            l = l.replace("\n","")
            if l == "mikroprogramm:": start = True
            elif l == "maschinenprogramm:": return d
            elif start: d += [l]

def as_row(line):
    """
    Generates a HTML row from a given line
    
    Args:
        line: JMIC mi-proramm line
        
    Returns:
        Dictionary containing 'name', 'opcode' and 'cells'
    """
    
    global HIGHLIGHT_CLASS, use_highlight, sort_reversed, show_ifetch, merge

    # Get opcode, name and data
    op = int(line[:4],16)
    if not show_ifetch and op < 16: return None
    
    data = line[-30:]
    name = line[4:-30]
    
    # To big-endian; remove whitespaces
    data = "".join(data.split(" ")[::-1])
    # Hexstring->int->Binstring; fill missing 0; reverse
    data = bin(int(data,16))[2:].zfill(80)[::-1]
    
    # For each cell
    cells = []
    for i in range(len(FUNC)):
        # Get area in the instruction; 0bit is the highest bit => reverse; to int
        x = int(data[BIT_MAP[i][0]:BIT_MAP[i][1]+1][::-1],2)
        
        if not merge: o = "<td>"
        else: o = ""
        
        # Highlight if not default value
        if use_highlight and default[i] is not x: h = ' class="%s"' % HIGHLIGHT_CLASS
        else: h=""
        
        # Check if there is a mnemo for the number
        if len(MNEMOS[i]) > x:
            if descriton: desc = ' title="'+LONG[i][x]
            else: desc = ""
            o += '<span'+h+desc+'">'+MNEMOS[i][x]+"</span>"
        # Append numeric value else (0 instead of 0x0)
        else: o += "<span"+h+">"+('0' if x is 0 else hex(x))+"</span>"
        if not merge: o += "</td>"
        cells += [o]
    
    # Merge cells
    if merge:
        for m in reversed(MERGE_CELLS): # Reverse is necessary
            cells[m[0]] = " ".join(cells[m[0]:m[1]+1])
            del cells[m[0]+1:m[1]+1]
        
        # Wrap cells
        cells[:] = ["<td>"+c+"</td>" for c in cells]
    
    return  {'name':name, 'opcode':op, 'cells':cells[::-1] if sort_reversed else cells}

def to_html(data, show_name=True, show_op=True, show_func=True, show_bits=True):
    """
    Generates HTML from the given data
    
    Args:
        data: jmic data
        show_name: display names
        show_op: display opcodes
        show_func: display functions
        show_bits: display bits
        
    Returns:
        Dictionary containing 'names', 'opcodes' and 'html'
    """
    
    global sort_reversed
    out = ""
    
    out += "<table>"
    
    func_row = []
    bit_row = []
    
    # Function tablehead
    if show_func:        
        title = lambda x: ' title="'+FUNC_LONG[x]+'"' if descriton else ""
        
        cells = list("<span"+title(i)+">{}</span>".format(n) for i, n in enumerate(FUNC))
        if merge:
            for i, m in reversed(list(enumerate(MERGE_CELLS))):
                # If a name for the merged functions is defined use it
                if len(MERGE_FUNC)>i and MERGE_FUNC[i]: cells[m[0]] = MERGE_FUNC[i]
                # Else join old ones to a new one
                else: cells[m[0]] = " / ".join(cells[m[0]:m[1]+1])
                
                # Remove old cells
                for i in reversed(range(m[0]+1,m[1]+1)): del cells[i]
        
        # Append row
        func_row += cells[::-1] if sort_reversed else cells
    
    # Bits
    if show_bits:
        cells = []
        
        tmp = [x for x in BIT_MAP]
        
        # Adjust bitmap to match merged cells
        if merge:
            for m in reversed(MERGE_CELLS):
                tmp[m[0]] = m
                del tmp[m[0]+1:m[1]+1]
        
        
        # (1,2) -> 1..2 and (1, 1)-> 1
        for m in tmp:
            if m[0]<m[1]: cells += ["<th>{}..{}</th>".format(m[0], m[1])]
            else: cells += ["<th>{}</th>".format(m[0])]
        
        #Append row
        bit_row += cells[::-1] if sort_reversed else cells
    
    # Matrix with all value cells
    names = []
    ops = []
    rows = []
    
    # Get the data rows
    for l in data:
        row = as_row(l)
        if row:
            
            names += [row['name']]
            ops += ["<th>0x%02x</th>" % row['opcode']]
            rows += [row['cells']]
    
    # Top left corner size (default 2x2)
    padding_l = show_name+show_op
    padding_t = show_bits+show_func
    
    # Prepend bit & function row (with padding)
    if show_bits: rows = [["<th></th>"]*(padding_l)+bit_row]+rows
    if show_func: rows = [[""]*(padding_l)+func_row]+rows
    
    # Returns the leading <th> cells (name & opcode) for data rows
    def fill_left(i):
        return ["<th>"+names[i]+"</th>",ops[i]][1-show_name:min(show_name+2*show_op,2)]
    
    # Insert leading <th> cells
    rows[padding_t:] = [fill_left(i)+r for i,r in enumerate(rows[padding_t:])]
    
    
    if filter_funcs:
        # Generate a list with the ids of the functions
        fltr = [i[0] for i in filter(lambda x:x[1].lower() in filter_funcs, enumerate(FUNC))]
        if sort_reversed:
            # Calculate positions for reversed table
            fltr = [len(FUNC)-v-1 for v in fltr]
            # (start, end) positions for the merged cells
            merge_cells_tmp = [(len(FUNC)-1-m[1],len(FUNC)-1-m[0]) for m in MERGE_CELLS][::-1]
        else: merge_cells_tmp = MERGE_CELLS
        
        # Correct fltr to match merged cells
        if merge:
            for m in reversed(merge_cells_tmp):
                add = False
                # Remove everything in range(start+1,end+1)
                for i in range(m[0]+1,m[1]+1):
                    try:
                        fltr.remove(i)
                        add = True
                    except: pass
                # Add start
                if add and not m[0] in fltr: fltr += [m[0]]
                # Shift all values > start to the left (step: end-start)
                fltr = [v-m[1]+m[0] if v>m[0] else v for v in fltr]       
        fltr.sort()
        # Filter columns with fltr (ignore non data columns)
        rows = [r[0:padding_l]+[r[i+padding_l] for i in fltr] for r in rows]
    
    # Wrap functions
    if show_func: rows[0] = ["<th>"+c+"</th>" for c in rows[0]]
    
    # Join data cells/rows to table
    out += "".join("<tr>"+"".join(c)+"</tr>" for c in rows)
    
    
    out += "</table>"
    
    return {'names':names, 'opcodes':ops, 'html':out}

if __name__ == "__main__":
    data = get_data(input_file)
    
    # One table for each MA-instruction
    if split:
        from itertools import groupby
        html = ""
        
        # Group by opcode (only first two numbers)
        for key, group in groupby(data, lambda x: x[:2]):
            # Ignore ifetch
            if not show_ifetch and int(key) == 0: continue
            # Get HTML of group and do not display the names
            content = to_html(list(e for e in group), False, show_op, show_func, show_bits)
            
            if show_name: html += "<h1>"+content['names'][0]+"</h1>"
            html += content['html']
        
    else: html = to_html(data, show_name, show_op, show_func, show_bits)['html']
    with open(file_name, 'w+') as f:
        # Insert css link
        if wrap: html = WRAPPER.format('<link rel="stylesheet" href="'+css+'"/>' if css else '', html)
        
        f.write(html)
    
    