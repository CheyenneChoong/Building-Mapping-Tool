from process.route import Route
from process.load import loadData

data:dict = loadData("project/Test3.json")
tester = Route()
tester.setPath("project/Test3.json")

floorList = data["floors"]
nameList = data["names"]
pointList1 = list(set(nameList) - set(floorList))
pointList2 = list(set(nameList) - set(floorList))

# pointList1 = data["1"]["room"] + list(set(data["1"]["checkpoint"]) |set(data["1"]["connector"]))
# pointList2 = data["1"]["room"] + list(set(data["1"]["checkpoint"]) |set(data["1"]["connector"]))

print("Test Starting")
counter = 0
success = 0
for point1 in pointList1:
    for point2 in pointList2:
        counter += 1
        try:
            # print(f"{point1} -> {point2} | {tester.navigate(point1, point2)}")
            result =tester.navigate(point1, point2)
            
            if result:
                success += 1
            else:
                print(f"{point1} -> {point2} | No route")
                # print(result)
        except:
            print(f"{point1} -> {point2} | Failed.")
print(f"Test Completed. {success}/{counter}")

# result = tester.navigate("R4-1", "R4-2")
# print(result)