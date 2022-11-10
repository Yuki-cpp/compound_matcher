import cirpy
import urllib.parse

import webview

from .molecule import Molecule


def complete_molecule(m: Molecule):
    if m.iupac_name is None:
        for n in m.names:
            m.iupac_name = cirpy.resolve(n, "iupac_name")
            if m.iupac_name is not None:
                break

        if m.iupac_name is None:
            # Couldn't find a match
            return False

    print(m.iupac_name)
    m.cas_registry_number = cirpy.resolve(m.iupac_name, "cas")
    m.formula = cirpy.resolve(m.iupac_name, "formula")

    return True


def build_molecule_from_name(name):
    try:
        iupac = cirpy.resolve(name, "iupac_name")
        cas = cirpy.resolve(name, "cas")
        formula = cirpy.resolve(name, "formula")

        return Molecule(names=[name], cas=cas, iupac=iupac, formula=formula)
    except:
        return None


def show_molecule(m: Molecule):
    url_name = urllib.parse.quote(m.iupac_name)

    webview.create_window(
        m.iupac_name,
        f"https://cactus.nci.nih.gov/chemical/structure/{url_name}/twirl",
        width=1000,
        height=710,
        resizable=False,
    )
    webview.start()
