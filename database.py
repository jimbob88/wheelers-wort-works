import os
from typing import List, Dict, Union

__mode__ = "local"


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if __mode__ == "local":
        base_path = os.path.abspath(".")
        path = os.path.join(base_path, relative_path)
    elif __mode__ == "deb":
        if os.path.basename(relative_path) == "logo.png":
            path = "/usr/include/wheelers-wort-works/logo.png"
        elif os.path.splitext(os.path.basename(relative_path))[1] == ".html":
            path = os.path.join(
                os.path.expanduser("~/.config/Wheelers-Wort-Works/recipes/html"),
                relative_path,
            )
        path = os.path.join(
            os.path.expanduser("~/.config/Wheelers-Wort-Works/"), relative_path
        )
    return path


def write_defaults_data(constants):
    evaporation = round((constants["Boil Volume Scale"] - 1) * 100, 1)
    with open(resource_path("defaults.txt"), "w", encoding="utf-8") as f:
        f.write(
            (
                f"efficiency={constants['Efficiency'] * 100}\n"
                f"volume={constants['Volume']}\n"
                f"evaporation={evaporation}\n"
                f"LGratio={constants['Liquor To Grist Ratio']}\n"
                f"attenuation={constants['Attenuation Default']}\n"
                f"save_close={constants['Save On Close']}\n"
                f"boil_time={constants['Default Boil Time']}\n"
                f"replace_defaults={constants['Replace Defaults']}"
            )
        )


def read_defaults_data(constants=None):
    if constants is None:
        constants = {}
    with open(resource_path("defaults.txt"), "r", encoding="utf-8") as f:
        data = [line.strip().split("=") for line in f]

    rename = {
        "efficiency": "Efficiency",
        "volume": "Volume",
        "evaporation": "Boil Volume Scale",
        "LGratio": "Liquor To Grist Ratio",
        "attenuation": "Attenuation Default",
        "save_close": "Save On Close",
        "boil_time": "Default Boil Time",
        "replace_defaults": "Replace Defaults",
    }
    clean_func = {
        "efficiency": lambda x: float(x) / 100,
        "volume": lambda x: float(x),
        "evaporation": lambda x: (float(x) / 100) + 1,
        "LGratio": lambda x: float(x),
        "attenuation": lambda x: x,
        "save_close": lambda x: x == "True",
        "boil_time": lambda x: int(x),
        "replace_defaults": lambda x: x == "True",
    }
    for constant in data:
        constants[rename[constant[0]]] = clean_func[constant[0]](constant[1])
    return constants


def write_hop_data(hop_data: Union[None, List[Dict]]):
    with open(resource_path("hop_data.txt"), "w", encoding="utf-8") as f:
        for hop, value in hop_data.items():
            name = hop
            hop_type = value["Form"]
            origin = value["Origin"]
            alpha = value["Alpha"]
            use = value["Use"]
            description = value["Description"]
            f.write(
                "{name}\t{hop_type}\t{origin}\t{alpha}\t{use}\t{description}\n".format(
                    name=name,
                    hop_type=hop_type,
                    origin=origin,
                    alpha=alpha,
                    use=use,
                    description=description,
                )
            )


def read_hop_data(hop_data: Union[None, List[Dict]] = None):
    """
    Reads data from the hop_data.txt file
    Creates dictionary like the following:

    'Nelson Sauvin': {'Form': 'Whole',
            'Origin': 'New Zeland',
            'Description': '',
            'Use': 'General Purpose', '
            Alpha': 12.7}
    """
    if hop_data is None:
        hop_data = {}
    with open(resource_path("hop_data.txt"), "r", encoding="utf-8") as f:
        data = [line.strip().split("\t") for line in f]
        for hop in data:
            name = hop[0]
            hop_data[name] = {
                "Form": hop[1],
                "Origin": hop[2],
                "Alpha": float(hop[3]),
                "Use": hop[4],
                "Description": hop[5] if len(hop) >= 6 else "No Description",
            }
    return hop_data


def write_grain_data(grist_data: Union[List[Dict], None] = None):
    if grist_data is None:
        grist_data = {}
    with open(resource_path("grain_data.txt"), "w", encoding="utf-8") as f:
        for ingredient, value in grist_data.items():
            name = ingredient
            ebc = value["EBC"]
            grain_type = value["Type"]
            extract = value["Extract"]
            moisture = value["Moisture"]
            fermentability = value["Fermentability"]
            description = value["Description"]
            f.write(
                f"{name}\t{ebc}\t{grain_type}\t{extract}\t{moisture}\t{fermentability}\t{description}\n"
            )


def read_grain_data(grist_data: Union[List[Dict], None] = None) -> List[Dict]:
    """
    Reads grain_data.txt and returns grists in the following format:
    {'Wheat Flour': {'EBC': 0.0,
                    'Type': 3.0,
                    'Extract': 304.0,
                    'Description': 'No Description',
                    'Moisture': 11.0, '
                    Fermentability': 62.0}}
    """
    if grist_data is None:
        grist_data = {}
    with open(resource_path("grain_data.txt"), "r", encoding="utf-8") as f:
        data = [line.strip().split("\t") for line in f]
        for ingredient in data:

            name = ingredient[0]
            grist_data[name] = {
                "EBC": float(ingredient[1]),
                "Type": float(ingredient[2]),
                "Extract": float(ingredient[3]),
                "Description": ingredient[6],
                "Moisture": float(ingredient[4]),
                "Fermentability": float(ingredient[5]),
            }
    return grist_data


def write_yeast_data(yeast_data: Union[List[Dict], None] = None):
    if yeast_data is None:
        yeast_data = {}
    with open(resource_path("yeast_data.txt"), "w", encoding="utf-8") as f:
        for yeast, value in yeast_data.items():
            name = yeast
            yeast_type = value["Type"]
            lab = value["Lab"]
            flocculation = value["Flocculation"]
            attenuation = value["Attenuation"]
            temperature = value["Temperature"]
            origin = value["Origin"]
            description = value["Description"]
            f.write(
                f"{name}\t{yeast_type}\t{lab}\t{flocculation}\t{attenuation}\t{temperature}\t{origin}\t{description}\n"
            )

def read_yeast_data(yeast_data: Union[List[Dict], None] = None) -> List[Dict]:
    if yeast_data is None:
        yeast_data = {}
    with open(resource_path('yeast_data.txt'), 'r', encoding="utf-8") as f:
        data = [line.strip().split('\t') for line in f]
        for yeast in data:
            name = yeast[0]
            yeast_data[name] = {
                'Type': yeast[1],
                'Lab': yeast[2],
                'Flocculation': yeast[3],
                'Attenuation': yeast[4],
                'Temperature': yeast[5],
                'Description': yeast[7],
                'Origin': yeast[6]}
    return yeast_data

def write_water_chem_data(water_chemistry_additions: Union[List[Dict], None] = None):
    if water_chemistry_additions is None:
        water_chemistry_additions = {}
    with open(resource_path('water_chem_data.txt'), 'w', encoding="utf-8") as f:
        for water_chem, values in water_chemistry_additions.items():
            value = values['Values']
            name = water_chem
            time = value['Time'] if 'Time' in value else 'N/A'
            water_chem_type = value['Type']
            f.write(f'{name}\t{time}\t{water_chem_type}\n')

def read_water_chem_data(water_chemistry_additions: Union[List[Dict], None] = None):
    if water_chemistry_additions is None:
        water_chemistry_additions = {}
    with open(resource_path('water_chem_data.txt'), 'r', encoding="utf-8") as f:
        data = [line.strip().split('\t') for line in f]
        for water_chem in data:
            name = water_chem[0]
            time = float(
                water_chem[1]) if water_chem[1] != 'N/A' else water_chem[1]
            water_chem_type = water_chem[2]
            water_chemistry_additions[name] = {
                'Values': {'Type': water_chem_type}}
            if time != 'N/A':
                water_chemistry_additions[name]['Values']['Time'] = time
    return water_chemistry_additions