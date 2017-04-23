import tkinter.ttk as ttk


def treeview_sort_column(treeview: ttk.Treeview, col, reverse=False):
    l = [(treeview.set(k, col), k) for k in treeview.get_children('')]
    l.sort(reverse=reverse)

    # Rearranging items in sorted positions
    for index, (val, k) in enumerate(l):
        treeview.move(k, '', index)

    treeview.heading(col, command=lambda: treeview_sort_column(treeview, col, not reverse))


#Usage
'''
columns = ('col1', 'col2')
treeview = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    treeview.heading(col, text=col, command=lambda: treeview_sort_column(treeview, col,


'''

def make_treeview_sortable(treeview, columns):
    for col in columns:
        treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeview, _col))

