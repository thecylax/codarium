import json
import os
import shutil
import tarfile

from jsonschema import ValidationError, validate

from src.core.database import Database


def load_packages():
    """Load all core packages."""
    lib_dir = 'src/core/lib'
    for filename in os.listdir(lib_dir):
        pkg_name = os.path.splitext(filename)[0]
        if filename.endswith('.xz'):
            package_path = os.path.join(lib_dir, filename)
            extract_dir = os.path.join('/tmp/coda', pkg_name)
        os.makedirs(extract_dir, exist_ok=True)
        try:
            with tarfile.open(package_path, mode='r:xz') as tar:
                tar.extractall(extract_dir)
        except tarfile.TarError as e:
            print(f"Erro ao processar {filename}: {e}")

        status = validate_package(os.path.join(f'/tmp/coda/{pkg_name}', f'{pkg_name}.json'))
        if status:
            install_package(os.path.join(f'/tmp/coda/{pkg_name}', f'{pkg_name}.json'))
        else:
            print(f'Ignoring package {pkg_name} due to previous error.')

def validate_package(pkg_path: str) -> bool:
    """Validate a loaded package."""
    with open(pkg_path) as fp:
        data = json.load(fp)

    with open('src/helper/schema.json') as fp:
        schema = json.load(fp)

    schema_version = data.get("schema_version")
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        print(f'Not valid: {e}')

    return False

def install_package(source_path: str):
    """Install a core or custom package."""
    with open(source_path) as fp:
        data = json.load(fp)

    pkg_version = data.get('version')
    db = Database('codadb.json', 'blocks')
    reg = db.get_one('name', data.get('name'))
    if not reg:
        _id = db.insert_one(data)

