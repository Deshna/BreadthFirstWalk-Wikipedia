import wikipedia
import csv

out = csv.writer(open("myfile.csv","w"))
previous_=""


class Tree(object):
	def __init__(self,parent):
		self.parent = parent
		self.children = []
	def add_child(self,child):
		self.children.append(child)

start = True
out.writerow(["title","related"])
with open('gephi_ip.csv','rb') as csvfile:
	reader = csv.reader(csvfile)
	included_cols = [2,1]
	for row in reader:
		if row[2]!="title":
			if start:
				title = (row[2])
				node = Tree(title)
				node.add_child(row[1])
				start = False
			else:
				if title == row[2]:
					node.add_child(row[1])
				else:
					related = list(node.children)
					related.insert(0,title)
					out.writerow(related)
					title = row[2]
					node = Tree(title)
					node.add_child(row[1])
