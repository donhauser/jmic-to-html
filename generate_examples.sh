python jmic.py  test.mpr examples/default.html
python jmic.py -css=../mi_table.css  test.mpr examples/default_css.html
python jmic.py -css=../mi_table.css -f=cmd,bar,shift test.mpr examples/filter_cmd_bar_shift.html
python jmic.py -css=../mi_table.css -i test.mpr examples/no_ifetch.html
python jmic.py -css=../mi_table.css -m test.mpr examples/merged_1bit_cells.html
python jmic.py -css=../mi_table.css -nobits test.mpr examples/no_bit_row.html
python jmic.py -css=../mi_table.css -nodesc test.mpr examples/no_decription.html
python jmic.py -css=../mi_table_simple.css -nofunc test.mpr examples/no_function_row.html
python jmic.py -css=../mi_table.css -nohighlight test.mpr examples/no_highlight.html
python jmic.py -css=../mi_table.css -noname test.mpr examples/no_name_column.html
python jmic.py -css=../mi_table.css -noopcodes test.mpr examples/no_opcode_column.html
python jmic.py -nowrap test.mpr examples/no_html_wrap.html
python jmic.py -css=../mi_table.css -r test.mpr examples/reverse_the_table.html
python jmic.py -css=../mi_table_split.css -s test.mpr examples/split_the_table.html
python jmic.py -css=../mi_table_split.css -s -m test.mpr examples/split_and_merge.html
python jmic.py -css=../mi_table_split.css -s -r test.mpr examples/split_and_reverse.html
python jmic.py -css=../mi_table_split.css -s -m -r test.mpr examples/split_merge_reverse.html
python jmic.py -css=../mi_table_split.css -s -m -r -f=cmd,bar,shift test.mpr examples/split_merge_reverse_filter.html
python jmic.py -css=../mi_table_simple.css -nobits -nofunc -noname -noopcodes test.mpr examples/no_table_outline.html
