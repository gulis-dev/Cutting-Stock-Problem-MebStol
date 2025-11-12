import math

def calculate_fit(format, free_space):
    area_space = free_space["width"] * free_space["height"]
    area_format = format["width"] * format["height"]

    waste_normal = math.inf
    waste_rotated = math.inf

    if format["width"] <= free_space["width"] and format["height"] <= free_space["height"]:
        waste_normal = area_space - area_format

    if format["width"] != format["height"]:
        if format["height"] <= free_space["width"] and format["width"] <= free_space["height"]:
            waste_rotated = area_space - area_format
    if waste_normal <= waste_rotated and waste_normal != math.inf:
        return waste_normal, {"width": format["width"], "height": format["height"]}
    elif waste_rotated < waste_normal and waste_rotated != math.inf:
        return waste_rotated, {"width": format["height"], "height": format["width"]}
    else:
        return math.inf, None

def split_space_gilotine(old_space, used_dimensions):
    new_spaces = []

    rest_width = old_space["width"] - used_dimensions["width"]
    rest_height = old_space["height"] - used_dimensions["height"]

    new_right = {
        "x": old_space["x"] + used_dimensions["width"],
        "y": old_space["y"],
        "width": rest_width,
        "height": used_dimensions["height"]
    }
    new_bottom = {
        "x": old_space["x"],
        "y": old_space["y"] + used_dimensions["height"],
        "width": old_space["width"],
        "height": rest_height
    }

    if new_right["width"] > 0 and new_right["height"] > 0:
        new_spaces.append(new_right)

    if new_bottom["width"] > 0 and new_bottom["height"] > 0:
        new_spaces.append(new_bottom)

    return new_spaces


def main():
    sheet = {"x": 0, "y": 0, "width": 100, "height": 100}
    order_list =  [
            {"name": "Formatka B", "width": 30, "height": 50, "quantity": 1},
            {"name": "Formatka A", "width": 60, "height": 40, "quantity": 2},
            {"name": "Formatka C", "width": 20, "height": 20, "quantity": 3}
        ]

    list_of_vacancies = [sheet.copy()]

    arranged_forms = []
    unarranged_forms = []

    all_results = []

    strategies = ['area', 'max_side', 'width', 'height']

    for form in order_list:
        form["area"] = form["width"] * form["height"]
        form["max_side"] = max(form["width"], form["height"])

    for strategy in strategies:
        list_of_vacancies = [sheet.copy()]
        arranged_forms = []
        unarranged_forms = []

        current_order_list = order_list.copy()
        if strategy == 'max_side':
            current_order_list.sort(key=lambda x: x['max_side'], reverse=True)
        elif strategy == 'area':
            current_order_list.sort(key=lambda x: x['area'], reverse=True)
        elif strategy == 'height':
            current_order_list.sort(key=lambda x: x['height'], reverse=True)
        elif strategy == 'width':
            current_order_list.sort(key=lambda x: x['width'], reverse=True)

        forms_to_arrange = []

        for i in current_order_list:
            for j in range(i["quantity"]):
                forms_to_arrange.append({
                    "name": f"{i['name']} #{j+1}",
                    "width": i["width"],
                    "height": i["height"],
                    "area": i["area"],
                })

        for form in forms_to_arrange:

            the_best_place_index = -1
            min_waste_area = math.inf
            final_format = None

            for i in range(len(list_of_vacancies)):
                vacancy = list_of_vacancies[i]
                waste, dimensions_after_adjustment = calculate_fit(form, vacancy)

                if waste < min_waste_area:
                    min_waste_area = waste
                    the_best_place_index = i
                    final_format = dimensions_after_adjustment

            if the_best_place_index != -1:
                old_space = list_of_vacancies.pop(the_best_place_index)
                arranged = {
                    "name": form["name"],
                    "width": final_format["width"],
                    "height": final_format["height"],
                    "x": old_space["x"],
                    "y": old_space["y"]
                }
                arranged_forms.append(arranged)
                new_free_spaces = split_space_gilotine(old_space, final_format)

                list_of_vacancies.extend(new_free_spaces)
            else:
                unarranged_forms.append(form)

        all_results.append({
            "strategy": strategy,
            "sheet": sheet.copy(),
            "arranged": arranged_forms.copy(),
            "waste_spaces": list_of_vacancies.copy(),
            "unarranged": unarranged_forms.copy(),
            "number_of_unused": len(unarranged_forms)
        })

    all_results.sort(key=lambda x: x["number_of_unused"])
    best_result = all_results[0]
    print("Best strategy:", best_result["strategy"])
    print("Arranged forms:", best_result["arranged"])
    print("Unarranged forms:", best_result["unarranged"])

if __name__ == "__main__":
    main()