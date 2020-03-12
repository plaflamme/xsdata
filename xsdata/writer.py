from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import List

from xsdata.exceptions import CodeWriterError
from xsdata.formats.dataclass.generator import DataclassGenerator
from xsdata.formats.generators import AbstractGenerator
from xsdata.formats.plantuml.generator import PlantUmlGenerator
from xsdata.logger import logger
from xsdata.models.codegen import Class


@dataclass
class CodeWriter:
    generators: Dict[str, AbstractGenerator] = field(default_factory=dict)
    modules: Dict = field(default_factory=dict)
    packages: Dict = field(default_factory=dict)
    module_names: Dict = field(default_factory=dict)

    @property
    def formats(self):
        return list(self.generators.keys())

    def register_format(self, name, generator: AbstractGenerator):
        self.generators[name] = generator

    def get_format(self, name) -> AbstractGenerator:
        if name in self.generators:
            return self.generators[name]
        raise CodeWriterError(f"Unknown code generator `{name}`")

    def write(self, classes: List[Class], format: str):
        engine = self.get_format(format)
        for file, package, output in engine.render(classes):
            if len(output.strip()) > 0:
                logger.info("Generating package: %s", package)

                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(output)

    def print(self, classes: List[Class], format: str):
        engine = self.get_format(format)
        for _, _, output in engine.render(classes):
            print(output, end="")

    def designate(self, classes: List[Class], format: str):
        for obj in classes:
            obj.module = self.unique_module_name(obj.module, format)
            obj.package = self.unique_package_name(obj.package, format)

    def unique_module_name(self, module: str, format: str):
        if module not in self.modules:
            engine = self.get_format(format)
            name = module[:-4] if module.endswith(".xsd") else module
            name = engine.module_name(name)
            if name in self.module_names:
                self.module_names[name] += 1
                name = engine.module_name(f"{name}_{self.module_names[name] - 1}")
            else:
                self.module_names[name] = 1

            self.modules[module] = name

        return self.modules[module]

    def unique_package_name(self, package: str, format: str):
        if package not in self.packages:
            engine = self.get_format(format)
            self.packages[package] = engine.package_name(package)
        return self.packages[package]


writer = CodeWriter()
writer.register_format("pydata", DataclassGenerator())
writer.register_format("plantuml", PlantUmlGenerator())
