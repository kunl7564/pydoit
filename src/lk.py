from utils import file_utils as fu

content = fu.read("d:\protocol.csv")
print(content)

fu.write("d:\\2\protocol.csv", content)
