#
# Copyright (c) 2020 Vitalis Salis.
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import os
import ast

from pycg import utils
from pycg.processing.base import ProcessingBase
from pycg.machinery.callgraph import CallGraph
from pycg.machinery.definitions import Definition

class CallGraphProcessor(ProcessingBase):
    def __init__(self, filename, modname, import_manager,
            scope_manager, def_manager, class_manager,
            module_manager, call_graph=None, modules_analyzed=None):
        super().__init__(filename, modname, modules_analyzed)
        # parent directory of file
        self.parent_dir = os.path.dirname(filename)

        self.import_manager = import_manager
        self.scope_manager = scope_manager
        self.def_manager = def_manager
        self.class_manager = class_manager
        self.module_manager = module_manager

        self.call_graph = call_graph

        self.closured = self.def_manager.transitive_closure()
        self.lastdir = {} # lwt
        self.dirc = os.path.dirname(os.path.realpath(__file__))
        self.fpc = open(self.dirc + "/../config.txt", 'r')
        self.diro = self.fpc.read()
        self.fpo = open(self.diro + "/output.txt", "a")
        self.defsign = 0
        self.call_count = 0

    def visit_Module(self, node):
        self.call_graph.add_node(self.modname, self.modname)
        self.fpo.flush()
        # print("visit_Module:" + self.modname)
        self.fpo.write("\n")
        self.fpo.flush()
        super().visit_Module(node)

    def visit_For(self, node):
        self.visit(node.iter)
        self.visit(node.target)
        # assign target.id to the return value of __next__ of node.iter.it
        # we need to have a visit for on the postprocessor also
        iter_decoded = self.decode_node(node.iter)
        for item in iter_decoded:
            if not isinstance(item, Definition):
                continue
            names = self.closured.get(item.get_ns(), [])
            for name in names:
                iter_ns = utils.join_ns(name, utils.constants.ITER_METHOD)
                next_ns = utils.join_ns(name, utils.constants.NEXT_METHOD)
                if self.def_manager.get(iter_ns):
                    self.call_graph.add_edge(self.current_method, iter_ns)
                if self.def_manager.get(next_ns):
                    self.call_graph.add_edge(self.current_method, next_ns)
        # print("visit_for:")
        super().visit_For(node)

    def visit_Lambda(self, node):
        counter = self.scope_manager.get_scope(self.current_ns).inc_lambda_counter()
        lambda_name = utils.get_lambda_name(counter)
        lambda_fullns = utils.join_ns(self.current_ns, lambda_name)

        self.call_graph.add_node(lambda_fullns, self.modname)
        # print("visit_lambda:")
        super().visit_Lambda(node, lambda_name)

    def visit_Raise(self, node):
        # print("visit_Raise:")
        if not node.exc:
            return
        self.visit(node.exc)
        decoded = self.decode_node(node.exc)
        for d in decoded:
            if not isinstance(d, Definition):
                continue
            names = self.closured.get(d.get_ns(), [])
            for name in names:
                pointer_def = self.def_manager.get(name)
                if pointer_def.get_type() == utils.constants.CLS_DEF:
                    init_ns = self.find_cls_fun_ns(name, utils.constants.CLS_INIT)
                    for ns in init_ns:
                        self.call_graph.add_edge(self.current_method, ns)
                if pointer_def.get_type() == utils.constants.EXT_DEF:
                    self.call_graph.add_edge(self.current_method, name)

    def visit_AsyncFunctionDef(self, node):
        # print("visit_AsyncFunctionDef:")
        self.visit_FunctionDef(node)

    def visit_FunctionDef(self, node):

        for decorator in node.decorator_list:
            self.visit(decorator)
            decoded = self.decode_node(decorator)
            for d in decoded:
                if not isinstance(d, Definition):
                    continue
                names = self.closured.get(d.get_ns(), [])
                for name in names:
                    self.call_graph.add_edge(self.current_method, name)

        self.call_graph.add_node(utils.join_ns(self.current_ns, node.name), self.modname)
        print("visit_FunctionDef:" + self.modname)
        # self.fpo.write("(" + self.current_method + ")1: ")
        # self.fpo.flush()
        self.defsign = 1
        super().visit_FunctionDef(node)

    def visit_Call(self, node):
        print("visit_call[")##lwt
        if self.current_method != self.lastdir:  # lwt
            self.fpo.write("\n")
            self.fpo.flush()
            self.lastdir = self.current_method
            if self.defsign == 1:
                self.fpo.write("(" + self.current_method + "): ")
                self.fpo.flush()
                self.defsign = 0
        # output_str = ""
        def create_ext_edge(name, ext_modname):
            self.add_ext_mod_node(name)
            self.call_graph.add_node(name, ext_modname)
            self.call_graph.add_edge(self.current_method, name)

            self.call_count += 1
            if self.call_count > 1:
                 self.fpo.write(" " + name)
            else:
                self.fpo.write(name)

            self.fpo.flush()
            # output_str += name + " "
            print("visit_call:" + name)
            self.lastdir = self.current_method# lwt

        # First visit the child function so that on the case of
        #       func()()()
        # we first visit the call to func and then the other calls
        for arg in node.args:
            self.visit(arg)

        for keyword in node.keywords:
            self.visit(keyword.value)

        self.fpo.write("[")
        self.fpo.flush()  ##lwt
        self.visit(node.func)

        names = self.retrieve_call_names(node)
        if not names:
            if isinstance(node.func, ast.Attribute) and self.has_ext_parent(node.func):
                # TODO: This doesn't work for cases where there is an assignment of an attribute
                # i.e. import os; lala = os.path; lala.dirname()
                for name in self.get_full_attr_names(node.func):
                    ext_modname = name.split(".")[0]
                    create_ext_edge(name, ext_modname)
            elif getattr(node.func, "id", None) and self.is_builtin(node.func.id):
                name = utils.join_ns(utils.constants.BUILTIN_NAME, node.func.id)
                create_ext_edge(name, utils.constants.BUILTIN_NAME)
            print("]visit_call3\n")
            self.call_count = 0
            # self.fpo.write(output_str)
            self.fpo.write("]")##lwt
            self.fpo.flush()  ##lwt
            return

        self.last_called_names = names
        for pointer in names:
            pointer_def = self.def_manager.get(pointer)
            if not pointer_def or not isinstance(pointer_def, Definition):
                continue
            if pointer_def.is_callable():
                if pointer_def.get_type() == utils.constants.EXT_DEF:
                    ext_modname = pointer.split(".")[0]
                    create_ext_edge(pointer, ext_modname)
                    continue
                self.call_graph.add_edge(self.current_method, pointer)
                print("1:" + self.current_method)# lwt
                print(pointer)
                if self.current_method != self.lastdir:  # lwt
                    self.fpo.write("\n")
                    self.fpo.flush()
                    if self.defsign == 1:
                        self.fpo.write("(" + self.current_method + "): ")
                        self.fpo.flush()
                        self.defsign = 0
                    # print("@@@@@@@@@" + self.current_method)
                self.fpo.write("<call>" + pointer)
                self.fpo.flush()
                # output_str += "<call>" + pointer + " "
                self.lastdir = self.current_method


                # TODO: This doesn't work and leads to calls from the decorators
                #    themselves to the function, creating edges to the first decorator
                #for decorator in pointer_def.decorator_names:
                #    dec_names = self.closured.get(decorator, [])
                #    for dec_name in dec_names:
                #        if self.def_manager.get(dec_name).get_type() == utils.constants.FUN_DEF:
                #            self.call_graph.add_edge(self.current_ns, dec_name)

            if pointer_def.get_type() == utils.constants.CLS_DEF:
                init_ns = self.find_cls_fun_ns(pointer, utils.constants.CLS_INIT)

                for ns in init_ns:
                    self.call_graph.add_edge(self.current_method, ns)
                    # print("2:" + self.current_method)
        self.call_count = 0
        # self.fpo.write(output_str)
        self.fpo.write("]")
        self.fpo.flush()  ##lwt
        print("]visit_call\n")


    def analyze_submodules(self):
        # print("analyze_submodules:")
        super().analyze_submodules(CallGraphProcessor, self.import_manager,
                self.scope_manager, self.def_manager, self.class_manager, self.module_manager,
                call_graph=self.call_graph, modules_analyzed=self.get_modules_analyzed())

    def analyze(self):
        # print("analyze:" + self.filename)
        self.fpo.write("\n\n" + self.filename)
        self.fpo.flush()
        self.visit(ast.parse(self.contents, self.filename))
        self.analyze_submodules()


    def get_all_reachable_functions(self):
        # print("get_all_reachable_functions:")
        reachable = set()
        names = set()
        current_scope = self.scope_manager.get_scope(self.current_ns)
        while current_scope:
            for name, defi in current_scope.get_defs().items():
                if defi.is_function_def() and not name in names:
                    closured = self.closured.get(defi.get_ns())
                    for item in closured:
                        reachable.add(item)
                    names.add(name)
            current_scope = current_scope.parent

        return reachable

    def has_ext_parent(self, node):
        # print("has_ext_parent:")
        if not isinstance(node, ast.Attribute):
            return False

        while isinstance(node, ast.Attribute):
            parents = self._retrieve_parent_names(node)
            for parent in parents:
                for name in self.closured.get(parent, []):
                    defi = self.def_manager.get(name)
                    if defi and defi.is_ext_def():
                        return True
            for name in node._fields:
                if name == "func" or name == "id":
                    value = getattr(node, name)
                    # print(value)
                    self.fpo.write(value)
                    self.fpo.flush()
                if name == "attr":
                    value = getattr(node, name)
                    # print(value)
                    self.fpo.write("#" + value)
                    self.fpo.flush()

            node = node.value
        return False

    def get_full_attr_names(self, node):
        # print("get_full_attr_names:")
        name = ""
        while isinstance(node, ast.Attribute):
            if not name:
                name = node.attr
            else:
                name = node.attr + "." + name
            node = node.value

        names = []
        if getattr(node, "id", None) == None:
            return names

        defi = self.scope_manager.get_def(self.current_ns, node.id)
        if defi and self.closured.get(defi.get_ns()):
            for id in self.closured.get(defi.get_ns()):
                names.append(id + "." + name)

        return names

    def is_builtin(self, name):
        return name in __builtins__

