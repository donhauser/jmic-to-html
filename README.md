Author: Jonas Donhauser
donhauserjonas@gmail.com

# JMIC to HTML converter

Version: v1.0

A python programm which extracts a [JMIC v1.4](http://wwwi10.lrr.in.tum.de/~eti/Praktikum/JMic.jar) microprogram and exports its content as html table(s)

This project is licensed under the therms of the MIT license

The most mappings were taken from the [JMIC application](http://wwwi10.lrr.in.tum.de/~eti/Praktikum/JMic.jar) (v. 1.4) (c) TUM
Link: [http://wwwi10.lrr.in.tum.de/~eti/Vorlesung/WS1415/Software/jmic-1.4.jar](http://wwwi10.lrr.in.tum.de/~eti/Praktikum/JMic.jar)

## Usage

The basic usage of the program is: jmic.py [-options] input output
Note that whitespaces in a path must be escaped with '\'
`python jmic.py test.mpr examples/default.html`
will result in [this table](examples/default.html)

## Options

### -css=<stylesheet>

Link a css file

For Example
`python jmic.py -css=../mi_table.css test.mpr examples/default_css.html`
will result in [this table](examples/default_css.html)

### -f=<col1>[,<col2>,<col3>,...]

Filter: Display only the listed columns (seperate with,)

For Example
`python jmic.py -css=../mi_table.css -f=cmd,bar,shift test.mpr examples/filter_cmd_bar_shift.html`
will result in [this table](examples/filter_cmd_bar_shift.html)

### -i

Ignore IFETCH (Opcode 0x0)

For Example
`python jmic.py -css=../mi_table.css -i test.mpr examples/no_ifetch.html`
will result in [this table](examples/no_ifetch.html)

### -m

Merge 1bit cells

For Example
`python jmic.py -css=../mi_table.css -m test.mpr examples/merged_1bit_cells.html`
will result in [this table](examples/merged_1bit_cells.html)

### -nobits

Do not display the used bit-width of each column

For Example
`python jmic.py -css=../mi_table.css -nobits test.mpr examples/no_bit_row.html`
will result in [this table](examples/no_bit_row.html)

### -nodesc

Do not set the cell title to the long description

For Example
`python jmic.py -css=../mi_table.css -nodesc test.mpr examples/no_decription.html`
will result in [this table](examples/no_decription.html)

### -nofunc

Do not display the function names as table head

For Example
`python jmic.py -css=../mi_table_simple.css -nofunc test.mpr examples/no_function_row.html`
will result in [this table](examples/no_function_row.html)

### -nohighlight

Do not highlight non default entries

For Example
`python jmic.py -css=../mi_table.css -nohighlight test.mpr examples/no_highlight.html`
will result in [this table](examples/no_highlight.html)

### -noname

Do not display the instruction name

For Example
`python jmic.py -css=../mi_table.css -noname test.mpr examples/no_name_column.html`
will result in [this table](examples/no_name_column.html)

### -noopcodes

Do not display the opcode of each row

For Example
`python jmic.py -css=../mi_table.css -noopcodes test.mpr examples/no_opcode_column.html`
will result in [this table](examples/no_opcode_column.html)

### -nowrap

Do not generate the html outline (html, head, body)

For Example
`python jmic.py -nowrap test.mpr examples/no_html_wrap.html`
will result in [this table](examples/no_html_wrap.html)

### -r

Reverse the horizontal order of the table

For Example
`python jmic.py -css=../mi_table.css -r test.mpr examples/reverse_the_table.html`
will result in [this table](examples/reverse_the_table.html)

### -s

Split the program into separate tables for each MA instruction

For Example
`python jmic.py -css=../mi_table_split.css -s test.mpr examples/split_the_table.html`
will result in [this table](examples/split_the_table.html)

## More Examples

`python jmic.py -css=../mi_table_split.css -s -m test.mpr examples/split_and_merge.html`
will result in [this table](examples/split_and_merge.html)

`python jmic.py -css=../mi_table_split.css -s -r test.mpr examples/split_and_reverse.html`
will result in [this table](examples/split_and_reverse.html)

`python jmic.py -css=../mi_table_split.css -s -m -r test.mpr examples/split_merge_reverse.html`
will result in [this table](examples/split_merge_reverse.html)

`python jmic.py -css=../mi_table_split.css -s -m -r -f=cmd,bar,shift test.mpr examples/split_merge_reverse_filter.html`
will result in [this table](examples/split_merge_reverse_filter.html)

`python jmic.py -css=../mi_table_simple.css -nobits -nofunc -noname -noopcodes test.mpr examples/no_table_outline.html`
will result in [this table](examples/no_table_outline.html)
