import os
import sys
import json

from SourceCode.SequenceGenerator.pycg.pycg import CallGraphGenerator
from SourceCode.SequenceGenerator.pycg import formats
from SourceCode.SequenceGenerator.pycg.utils.constants import CALL_GRAPH_OP, KEY_ERR_OP


def main(output=None, fasten=False, entry_point=[], package=None, product="", forge="PyPI", version="", timestamp=0,
        max_iter=-1, operation=CALL_GRAPH_OP, as_graph_output=None):


    cg = CallGraphGenerator(entry_point, package,
                        max_iter, operation)
    ret, call_dict = cg.analyze()
    print("done: cg")
    if operation == CALL_GRAPH_OP:
        if fasten:
            formatter = formats.Fasten(cg, package,
                                       product, forge, version, timestamp)
        else:
            formatter = formats.Simple(cg)
        output_json = formatter.generate()
    else:
        output_json = cg.output_key_errs()
    
    as_formatter = formats.AsGraph(cg)
    
    if output:
        with open(output, "w+") as f:
            f.write(json.dumps(output_json))
    else:
        print(json.dumps(output_json))
    
    if as_graph_output:
        with open(as_graph_output, "w+") as f:
            f.write(json.dumps(as_formatter.generate()))

    # for cfg: call_dict, file_list

    file_list = []
    for line in ret.split("\n"):
        if len(line) and line.startswith("/"):
            file_list.append(line)
    # print(file_list)
    return ret, output_json, file_list, call_dict


if __name__ == "__main__":

    ret, output_json, file_list, call_list = main(output="", fasten=True,
               entry_point=[""])
    print(ret)
    print("\n\n")
    # print(output_json)
    print(file_list)
    print(call_list)
    with open("", "w+") as f:
        f.write(json.dumps(call_list))
    f.close()
