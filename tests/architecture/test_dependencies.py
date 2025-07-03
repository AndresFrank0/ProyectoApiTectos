import pytest
from importlib import import_module
from pathlib import Path
import ast


# Directorios base para las capas de la arquitectura
DOMAIN_PATH = Path("src")
APPLICATION_PATH = Path("src")
INFRASTRUCTURE_PATH = Path("src")
API_PATH = Path("src")

# Módulos permitidos por capa
ALLOWED_IMPORTS = {
    "domain": {"typing", "datetime", "uuid", "pydantic", "enum"},
    "application": {"domain", "core.errors", "typing", "datetime", "uuid"},
    "infrastructure": {
        "domain",
        "application",
        "core",
        "typing",
        "datetime",
        "uuid",
        "sqlmodel",
        "sqlalchemy",
        "passlib",
        "jose",
    },
    "api": {
        "application",
        "domain",
        "core",
        "typing",
        "datetime",
        "uuid",
        "fastapi",
        "pydantic",
    },
}


def get_imports_from_file(file_path: Path) -> set:
    """Extrae todos los módulos importados de un archivo Python."""
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(file_path))

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])
    return imports


def find_python_files(base_path: Path, layer_name: str):
    """Encuentra todos los archivos Python en un directorio de capa específico."""
    layer_path = base_path / layer_name
    if not layer_path.exists():
        # Adapta la búsqueda para la estructura del proyecto
        layer_path = base_path
        return list(layer_path.rglob(f"**/{layer_name}/**/*.py"))
    return list(layer_path.rglob("*.py"))


@pytest.mark.parametrize(
    "file_path",
    [
        *find_python_files(DOMAIN_PATH, "domain"),
        *find_python_files(APPLICATION_PATH, "application"),
        *find_python_files(INFRASTRUCTURE_PATH, "infrastructure"),
        *find_python_files(API_PATH, "api"),
    ],
)
def test_architecture_dependencies(file_path: Path):
    """
    Prueba que cada archivo respete las reglas de dependencias de la Arquitectura Hexagonal.
    """
    # Determinar la capa del archivo actual
    parts = file_path.parts
    layer = None
    if "domain" in parts:
        layer = "domain"
    elif "application" in parts:
        layer = "application"
    elif "infrastructure" in parts:
        layer = "infrastructure"
    elif "api" in parts:
        layer = "api"

    if not layer:
        pytest.skip(f"No se pudo determinar la capa para el archivo: {file_path}")

    # Obtener los imports y las reglas
    imports = get_imports_from_file(file_path)
    allowed = ALLOWED_IMPORTS.get(layer, set())

    # src es el root package, se permite
    if "src" in imports:
        imports.remove("src")

    # Validar dependencias
    disallowed_imports = imports - allowed
    assert not disallowed_imports, (
        f"Violación de arquitectura en '{file_path}'.\n"
        f"La capa '{layer}' no puede importar: {disallowed_imports}.\n"
        f"Permitidos: {allowed}"
    )