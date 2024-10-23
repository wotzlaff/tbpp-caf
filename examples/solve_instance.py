import sys
import without_fu
from tbpp_caf import Instance

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 <executable> <instance> <solution output file>")
        return

    instance = sys.argv[1]
    instanceStruct = Instance.from_file(instance)

    f = open(sys.argv[2], "w")

    result = without_fu.solve(instanceStruct)

    if result == None:
        f.write("No solution")
    else:
        f.write(without_fu.format_result(result) + "\n")
    
    f.close()

if __name__ == '__main__':
    main()
