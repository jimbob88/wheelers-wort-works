import contextlib
from typing import Union, List

html_template = """
<!DOCTYPE html>
<html>
<head>
	<title>{recipe_name}</title>
	<link rel="shortcut icon"
		href="{logo}" />
	<!--Extracted From Graham Wheeler's Beer Engine recipe.html-->
	<!--Yeast Section added by jimbob88-->
	{css}
    {sorttable}
</head>

<body>
	<h2>{recipe_name}</h2>
	{ingredients_table}
    <p><b>Boil Time: </b>{boil_time}</p>
	{hops_table}
    {yeasts_table}
	<table style="width:800px">
		<p><b>Final Volume: </b>{final_volume} Litres</p>
		<p><b>Original Gravity: </b>{original_gravity}</p>
		<p><b>Final Gravity: </b>{final_gravity}</p>
		<p><b>Alcohol Content: </b>{abv} ABV</p>
		<p><b>Mash Efficiency: </b>{mash_efficiency}</p>
		<p><b>Bitterness: </b>{bitterness} IBU</p>
		<p><b>Colour: </b>{colour} EBC</p>
		<hr>
		<h2>Notes</h2>
		<p>{notes}<br></p>
</body>

</html>
"""

css = """
<style>
    body {text-align: left; margin-left: 30; margin-top: 15px; background: #FFFFFF; font-family: Helvetica,Verdana,Tahoma,Sans-serif; font-size: 10pt; color: #000000}
    table {border-spacing:0}
    td {text-align:left;font-family: Helvetica,Verdana,Tahoma,Sans-serif; font-size: 10pt; color: #000000;padding:0px;border-bottom: 1px solid  #000000;border-left: 1px solid  #000000;}
    td.ing1 {width:200; text-align:left;background-color: #FFFFFF;padding:4px}
    td.ing2 {width:70; text-align:right; background-color: #FFFFFF;padding:4px}
    td.ing3 {width:90; text-align:right; background-color: #FFFFFF;padding:4px}
    td.ing4 {width:40; text-align:right; background-color: #FFFFFF;padding:4px;border-right: 1px solid #000000;}
    td.hop1 {width:152; text-align:left; background-color: #FFFFFF;padding:4px}
    td.hop2 {width:60; text-align:center; background-color: #FFFFFF;padding:4px}
    td.hop3 {width:50; text-align:right; background-color: #FFFFFF;padding:4px}
    td.hop4 {width:60; text-align:right; background-color: #FFFFFF;padding:4px}
    td.hop5 {width:80; text-align:right; background-color: #FFFFFF;padding:4px}
    td.hop6 {width:40; text-align:right; background-color: #FFFFFF;padding:4px;border-right: 1px solid #000000;}
    td.yst1 {width:300; text-align:left;background-color: #FFFFFF;padding:4px}
    td.yst2 {width:100; text-align:center; background-color: #FFFFFF;padding:4px}
    td.yst3 {width:100; text-align:center; background-color: #FFFFFF;padding:4px}
    td.yst4 {width:40; text-align:center; background-color: #FFFFFF;padding:4px}
    td.yst5 {width:40; text-align:center; background-color: #FFFFFF;padding:4px}
    td.yst6 {width:20; text-align:center; background-color: #FFFFFF;padding:4px}
    td.yst7 {width:10; text-align:center; background-color: #FFFFFF;padding:4px;border-right: 1px solid #000000;}
    span.bold {font-weight: bold}
    th.subhead {font-weight:bold; text-align:center;background-color:#E8E8E8;padding:4px;border-top: 1px solid #000000;border-left: 1px solid #000000;border-bottom: 1px solid #000000;}
    th.subhead2 {font-weight:bold; text-align:center;background-color:#E8E8E8;padding:4px;border-top: 1px solid #000000;border-left: 1px solid #000000;border-right: 1px solid #000000;border-bottom: 1px solid #000000;}
    table.sortable th:not(.sorttable_sorted):not(.sorttable_sorted_reverse):not(.sorttable_nosort):after {
        content: ""
    }
</style>
"""


simple_hops_table = """
<table style="width:800px">
    <tr>
        <th class="subhead">Hop Variety</th>
        <th class="subhead">Type</th>
        <th class="subhead">Alpha</th>
        <th class="subhead">Time</th>
        <th class="subhead">lb:oz</th>
        <th class="subhead">Grams</th>
        <th class="subhead2">Ratio</th>
    </tr>
    {hops}
</table><br>
"""

complex_hops_table = """
<table style="width:800px" class="sortable">
<tr>
        <th class="subhead">Hop Variety</th>
        <th class="subhead">Type</th>
        <th class="subhead">Alpha</th>
        <th class="subhead">Time</th>
        <th class="subhead">lb:oz</th>
        <th class="subhead">Grams</th>
        <th class="subhead2">Ratio</th>
    </tr>
    {hops}
</table><br>
"""

simple_ingredients_table = """
<table style="width:800px">
    <tr>
        <th class="subhead">Fermentable</th>
        <th class="subhead">Colour</th>
        <th class="subhead">lb:oz</th>
        <th class="subhead">Grams</th>
        <th class="subhead2">Ratio</th>
    </tr>
    {ingredients}
</table><br>
"""

complex_ingredients_table = """
<table style="width:800px" class="sortable">
    <tr>
        <th class="subhead">Fermentable</th>
        <th class="subhead">Colour</th>
        <th class="subhead">lb:oz</th>
        <th class="subhead">Grams</th>
        <th class="subhead2">Ratio</th>
    </tr>
    {ingredients}
</table><br>
"""

simple_yeasts_table = """
<table style="width:800px">
    <tr>
        <th class="subhead">Yeast</th>
        <th class="subhead">Lab</th>
        <th class="subhead">Origin</th>
        <th class="subhead">Type</th>
        <th class="subhead">Flocculation</th>
        <th class="subhead">Attenuation</th>
        <th class="subhead2">Temperature</th>
    </tr>
    {yeasts}
</table><br>
"""

complex_yeasts_table = """
<table style="width:800px" class="sortable">
    <tr>
        <th class="subhead">Yeast</th>
        <th class="subhead">Lab</th>
        <th class="subhead">Origin</th>
        <th class="subhead">Type</th>
        <th class="subhead">Flocculation</th>
        <th class="subhead">Attenuation</th>
        <th class="subhead2">Temperature</th>
    </tr>
    {yeasts}
</table><br>
"""

yeast_template = """
<tr>
    <td class="yst1">{addition}</td>
    <td class="yst2">{lab}</td>
    <td class="yst3">{origin}</td>
    <td class="yst4">{yeast_type}</td>
    <td class="yst5">{flocculation}</td>
    <td class="yst6">{attenuation}</td>
    <td class="yst7">{temperature}</td>
</tr>
"""

ingredient_template = """
<tr>
    <td class="ing1">{ingredient_name}</td>
    <td class="ing2">{colour}</td>
    <td class="ing3">{lb_oz}</td>
    <td class="ing3">{grams}</td>
    <td class="ing4">{ratio}</td>
</tr>
"""

hops_template = """
<tr>
    <td class="hop1">{hop_name}</td>
    <td class="hop2">{hop_type}</td>
    <td class="hop3">{alpha}</td>
    <td class="hop4">{time}</td>
    <td class="hop5">{lb_oz}</td>
    <td class="hop5">{grams}</td>
    <td class="hop6">{ratio}%</td>
</tr>
"""


def make_ingredients_table(ingredients, added_additions, brew_data):
    ingredients_rows = []

    for addition in added_additions:
        with contextlib.suppress(KeyError):
            if (
                brew_data.water_chemistry_additions[addition]["Values"]["Type"]
                == "Malt"
            ):
                ingredients_rows.append(
                    ingredient_template.format(
                        ingredient_name=addition,
                        colour="N/A",
                        lb_oz="N/A",
                        grams="N/A",
                        ratio="N/A",
                    )
                )

    ingredients_rows.extend(
        ingredient_template.format(
            ingredient_name=ingredient["Name"],
            colour=ingredient["Values"]["EBC"],
            lb_oz=f"{int(ingredient['Values']['lb:oz'][0])}:{round(ingredient['Values']['lb:oz'][1], 1)}",
            grams=(
                (round(ingredient["Values"]["Grams"], 1))
                if (ingredient["Values"]["Grams"] - int(ingredient["Values"]["Grams"]))
                >= 2
                else round(ingredient["Values"]["Grams"])
            ),
            ratio=ingredient["Values"]["Percent"],
        )
        for ingredient in ingredients
    )
    return ingredients_rows


def make_hops_table(hops, added_additions, brew_data):
    for addition in added_additions:
        with contextlib.suppress(KeyError):
            if brew_data.water_chemistry_additions[addition]["Values"]["Type"] == "Hop":
                hops.append(
                    {
                        "Name": addition,
                        "Values": brew_data.water_chemistry_additions[addition][
                            "Values"
                        ],
                    }
                )
    hops = sorted(
        [x for x in hops if x is not None],
        key=lambda k: k["Values"]["Time"],
        reverse=True,
    )

    hops_rows = []
    for hop in hops:
        if hop["Values"]["Type"] != "Hop":
            hops_rows.append(
                hops_template.format(
                    hop_name=hop["Name"],
                    hop_type=hop["Values"]["Type"],
                    alpha=hop["Values"]["Alpha"],
                    time=round(hop["Values"]["Time"]),
                    lb_oz=f"{int(hop['Values']['lb:oz'][0])}:{round(hop['Values']['lb:oz'][1], 1)}",
                    grams=(round(hop["Values"]["Grams"], 1))
                    if (hop["Values"]["Grams"] - int(hop["Values"]["Grams"])) >= 2
                    else round(hop["Values"]["Grams"]),
                    ratio=hop["Values"]["Percent"],
                )
            )
        else:
            hops_rows.append(
                hops_template.format(
                    hop_name=hop["Name"],
                    hop_type="N/A",
                    alpha="N/A",
                    time=round(hop["Values"]["Time"]),
                    lb_oz="N/A",
                    grams="N/A",
                    ratio="N/A",
                )
            )
    return hops_rows


def make_yeasts_table(added_additions, brew_data):
    yeast_rows = []
    for addition in added_additions:
        try:
            if brew_data.yeast_data[addition]["Type"] == "D":
                yeast_type = "Dry"
            elif brew_data.yeast_data[addition]["Type"] == "L":
                yeast_type = "Liquid"
            else:
                yeast_type = brew_data.yeast_data[addition]["Type"]

            lab = brew_data.yeast_data[addition]["Lab"]
            origin = brew_data.yeast_data[addition]["Origin"]
            flocculation = brew_data.yeast_data[addition]["Flocculation"]
            attenuation = brew_data.yeast_data[addition]["Attenuation"]
            if (
                len(
                    brew_data.yeast_data[addition]["Temperature"]
                    .replace("°", "")
                    .split("-")
                )
                >= 2
            ):
                temperature = (
                    brew_data.yeast_data[addition]["Temperature"]
                    .replace("°", "")
                    .split("-")[0]
                )
                temperature += (
                    "-"
                    + brew_data.yeast_data[addition]["Temperature"]
                    .replace("°", "")
                    .split("-")[1]
                )
            yeast_rows.append(
                yeast_template.format(
                    addition=addition,
                    lab=lab,
                    origin=origin,
                    yeast_type=yeast_type,
                    flocculation=flocculation,
                    attenuation=attenuation,
                    temperature=temperature,
                )
            )
        except KeyError:
            with contextlib.suppress(KeyError):
                if (
                    brew_data.water_chemistry_additions[addition]["Values"]["Type"]
                    == "Yeast"
                ):
                    yeast_rows.append(
                        yeast_template.format(
                            addition=addition,
                            lab="N/A",
                            origin="N/A",
                            yeast_type="N/A",
                            flocculation="N/A",
                            attenuation="N/A",
                            temperature="N/A",
                        )
                    )
    return yeast_rows


def write_html(
    use_sorttable: bool,
    brew_data,
    added_additions: List,
    ingredients: List,
    hops: List,
    logo_location: str,
    recipe_name: str,
    volume: Union[float, int],
    og: Union[float, int],
    fg: Union[float, int],
    abv: Union[float, int],
    ibu: Union[float, int],
    colour: Union[float, int],
    notes: str,
    water_boil_time: Union[float, bool] = False,
) -> str:

    ingredients_rows = make_ingredients_table(
        ingredients=ingredients, added_additions=added_additions, brew_data=brew_data
    )

    hops_rows = make_hops_table(
        hops=hops, added_additions=added_additions, brew_data=brew_data
    )

    yeast_rows = make_yeasts_table(added_additions=added_additions, brew_data=brew_data)

    ingredients_table = (
        complex_ingredients_table if use_sorttable else simple_ingredients_table
    )
    hops_table = complex_hops_table if use_sorttable else simple_hops_table
    yeasts_table = complex_yeasts_table if use_sorttable else simple_yeasts_table

    return html_template.format(
        recipe_name=recipe_name,
        logo=logo_location,
        css=css,
        notes=notes,
        final_volume=volume,
        original_gravity=round(og, 1),
        final_gravity=round(fg, 1),
        abv=round(abv, 1),
        mash_efficiency=brew_data.constants["Efficiency"] * 100,
        bitterness=round(ibu),
        colour=round(colour, 1),
        yeasts_table=yeasts_table.format(yeasts="".join(yeast_rows)),
        hops_table=hops_table.format(hops="".join(hops_rows)),
        boil_time=water_boil_time,
        ingredients_table=ingredients_table.format(
            ingredients="".join(ingredients_rows)
        ),
        sorttable='<script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>'
        if use_sorttable
        else "",
    )
