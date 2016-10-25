'''
Generates the readme and examples

This project is licensed under the terms of the MIT license

Created on Oct 13, 2016

@author: Jonas Donhauser
'''

bash_file = "generate_examples.sh"
html_file = "readme.html"

d = "examples/"
c = "-css=../mi_table%s.css "
l = [('', 'default', ''),
     ('', 'default_css'),
     ('-f=cmd,bar,shift', 'filter_cmd_bar_shift'),
     ('-i', 'no_ifetch'),
     ('-m', 'merged_1bit_cells'),
     ('-nobits', 'no_bit_row'),
     ('-nodesc', 'no_decription'),
     ('-nofunc', 'no_function_row',c%'_simple'),
     ('-nohighlight','no_highlight'),
     ('-noname', 'no_name_column'),
     ('-noopcodes', 'no_opcode_column'),
     ('-nowrap', 'no_html_wrap',''),
     ('-r', 'reverse_the_table'),
     ('-s', 'split_the_table', c%'_split'),
     ('-s -m','split_and_merge', c%'_split'),
     ('-s -r','split_and_reverse', c%'_split'),
     ('-s -m -r','split_merge_reverse', c%'_split'),
     ('-s -m -r -f=cmd,bar,shift','split_merge_reverse_filter', c%'_split'),
     ('-nobits -nofunc -noname -noopcodes', 'no_table_outline', c%'_simple')
    ]

rows = []
for i in l:
    rows += ["python jmic.py "+(c%"" if len(i)<3 else i[2])+i[0]+" test.mpr "+d+i[1]+".html\n"]

with open(bash_file,"w+") as f:
    for r in rows:
        f.write(r)
print("Wrote %d lines to bash file %s"%(len(rows), bash_file))


opt = [('-css=<stylesheet>', 'Link a css file'),
('-f=<col1>[,<col2>,<col3>,...]', 'Filter: Display only the listed columns (seperate with,)'),
('-i', 'Ignore IFETCH (Opcode 0x0)'),
('-m', 'Merge 1bit cells'),
('-nobits', 'Do not display the used bit-width of each column'),
('-nodesc', 'Do not set the cell title to the long description'),
('-nofunc', 'Do not display the function names as table head'),
('-nohighlight', 'Do not highlight non default entries'),
('-noname', 'Do not display the instruction name'),
('-noopcodes', 'Do not display the opcode of each row'),
('-nowrap', 'Do not generate the html outline (html, head, body)'),
('-r', 'Reverse the horizontal order of the table'),
('-s', 'Split the program into separate tables for each MA instruction')]

jmic = "http://wwwi10.lrr.in.tum.de/~eti/Praktikum/JMic.jar"

from yattag import Doc
doc, tag, text = Doc().tagtext()
br = lambda: doc.stag("br")
with tag("html"):
    with tag("head"):
        doc.stag("link", rel="stylesheet", href="readme.css")
    with tag("body"):
        with tag("div"):
            with tag("author"):
                text("Author: Jonas Donhauser")
                br()
                text("donhauserjonas@gmail.com")
            with tag("h1"): text("JMIC to HTML converter")
            with tag("span", klass="version"): text("Version: v1.0")
            
            with tag("p"):
                text("A python programm which extracts a ")
                with tag("a", href=jmic): text("JMIC v1.4")
                text(" microprogram and exports its content as html table(s)")
            with tag("p"):
                text("""This project is licensed under the terms of the MIT license""")
                br()
                br()
                text("""The most mappings were taken from the """)
                with tag("a", href=jmic): text("JMIC application")
                text(" (v. 1.4) (c) TUM")
                br()
                text("Link: ")
                with tag("a", href=jmic): text(jmic)
            
            with tag("h2"): text("Usage")
            with tag("p"):
                text("The basic usage of the program is: jmic.py [-options] input output")
                br()
                text("Note that whitespaces in a path must be escaped with '\\'")
                br()
                
                with tag("code"):
                    text(rows[0])
                br()
                text("will result in ")
                with tag("a", href=d+l[0][1]+".html"):
                    text("this table")
            
            with tag("h2"): text("Options")
                
            for i,o in enumerate(opt):
                with tag("h3"):
                    text(o[0])
                with tag("span",klass="desc"): text(o[1])
                with tag("p"):
                    text("For Example")
                    br()
                    with tag("code"):
                        text(rows[i+1])
                    br()
                    text("will result in ")
                    with tag("a", href=d+l[i+1][1]+".html"):
                        text("this table")
            
            with tag("h2"): text("More Examples")
            
            for i,v in enumerate(l[len(opt)+1:]):
                with tag("p"):
                    with tag("code"):
                        text(rows[len(opt)+i+1])
                    br()
                    text("will result in ")
                    with tag("a", href=d+v[1]+".html"):
                        text("this table")

with open(html_file,"w+") as f:
    f.write(doc.getvalue())
print("Wrote html data to "+html_file)
print()
print("You might want to run %s to build the examples"%bash_file)
