import os
import inspect
import itertools
from tech import objects, params, instances, layers, purposes

script_dir = os.path.dirname(os.path.abspath(__file__))

def koe_actions_on_objects(filename="corpus.txt"):
    actions = ["select", "highlight", "count"]
    file_path = os.path.join(script_dir, filename)
    with open(file_path, "w") as file:
        for action in actions:
            for obj in objects:
                file.write(f"{action} all {obj}, koe_{action}_objects\n")

def koe_select_inst_with_params(filename="corpus.txt"):
    file_path = os.path.join(script_dir, filename)
    func_name = inspect.currentframe().f_code.co_name
    with open(file_path, "a") as file:
        for r in range(1, len(params) + 1):
            for param_combo in itertools.combinations(params, r):
                param_str = " and ".join(param_combo)
                for instance in instances:
                    file.write(f"select all {instance} with {param_str}, {func_name}\n")

def koe_change_LPP(filename="corpus.txt"):
    actions = ["change", "set", "update", "modify", "alter", "adjust", "switch", "assign", "replace", "convert"]
    lpp_keywords = ["layer", "LPP"]
    connectors = ["to", "as", "with"]
    file_path = os.path.join(script_dir, filename)
    func_name = inspect.currentframe().f_code.co_name
    with open(file_path, "a") as file:
        for action in actions:
            for lpp in lpp_keywords:
                for layer in layers:
                    for purpose in purposes:
                        for connector in connectors:
                            file.write(f"{action} {lpp} {connector} {layer} {purpose}, {func_name}\n")
                            file.write(f"{action} layer purpose {connector} {layer} {purpose}, {func_name}\n")
                        file.write(f"{action} {lpp} to {layer} {purpose}, {func_name}\n")
                        file.write(f"{action} layer to {layer} and purpose to {purpose}, {func_name}\n")
                        file.write(f"{action} the {lpp} to {layer} {purpose}, {func_name}\n")
                        file.write(f"{action} {lpp}={layer}, purpose={purpose}, {func_name}\n")
                        file.write(f"{action} {lpp} to {layer} and purpose to {purpose}, {func_name}\n")

if __name__ == "__main__":
    koe_actions_on_objects()
    # koe_select_inst_with_params()
    # koe_change_LPP()