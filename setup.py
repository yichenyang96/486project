import pip

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

if __name__ == '__main__':
    install_and_import('flask')
    install_and_import('bs4')