import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


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


def run_optimizer(sheet, order_list_raw, strategies):
    all_results = []

    order_list = []
    for form in order_list_raw:
        if not all(k in form for k in ("width", "height", "quantity")):
            continue
        if form["width"] is None or form["height"] is None or form["quantity"] is None:
            continue
        if form["width"] <= 0 or form["height"] <= 0 or form["quantity"] <= 0:
            continue

        form["area"] = form["width"] * form["height"]
        form["max_side"] = max(form["width"], form["height"])
        order_list.append(form)

    for strategy in strategies:
        list_of_vacancies = [sheet.copy()]
        arranged_forms = []
        unarranged_forms = []

        current_order_list = [item.copy() for item in order_list]

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
            for j in range(int(i["quantity"])):
                forms_to_arrange.append({
                    "name": f"{i['name']} #{j + 1}",
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

        total_sheet_area = sheet["width"] * sheet["height"]
        arranged_area = sum(f["width"] * f["height"] for f in arranged_forms)

        if total_sheet_area == 0:
            waste_percentage = 0
        else:
            waste_percentage = 100 * (total_sheet_area - arranged_area) / total_sheet_area

        all_results.append({
            "strategy": strategy,
            "sheet": sheet.copy(),
            "arranged": arranged_forms.copy(),
            "waste_spaces": list_of_vacancies.copy(),
            "unarranged": unarranged_forms.copy(),
            "number_of_unused": len(unarranged_forms),
            "waste_percentage": waste_percentage
        })

    all_results.sort(key=lambda x: x["number_of_unused"])
    return all_results[0]


def draw_layout(result):
    fig, ax = plt.subplots(1, figsize=(10, 10))

    sheet = result["sheet"]

    ax.add_patch(patches.Rectangle(
        (sheet["x"], sheet["y"]), sheet["width"], sheet["height"],
        facecolor=(0.9, 0.9, 0.9, 0.8),
        edgecolor='black',
        linewidth=2,
        label='Płyta'
    ))

    for i, form in enumerate(result["arranged"]):
        x0, y0 = form["x"], form["y"]

        rect = patches.Rectangle(
            (x0, y0), form["width"], form["height"],
            facecolor=(0.0, 0.0, 1.0, 0.5),
            edgecolor="blue",
            linewidth=2
        )
        ax.add_patch(rect)

        ax.text(
            x0 + form["width"] / 2,
            y0 + form["height"] / 2,
            form["name"],
            color="white",
            ha='center',
            va='center',
            fontsize=8
        )

    ax.set_title(f"Najlepsza Strategia: {result['strategy']} (Odpad: {result['waste_percentage']:.2f}%)")
    ax.set_xlim(-5, sheet["width"] + 5)
    ax.set_ylim(-5, sheet["height"] + 5)
    ax.set_aspect('equal', adjustable='box')
    plt.axis('off')

    return fig





st.set_page_config(layout="wide", page_title="Optymalizator Rozkroju")
st.title("Optymalizator Rozkroju Płyt")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("1. Wprowadź Dane")

    st.subheader("Wymiary Płyty (Sheet)")
    sheet_width = st.number_input("Szerokość Płyty (Sheet Width)", min_value=1, value=100)
    sheet_height = st.number_input("Wysokość Płyty (Sheet Height)", min_value=1, value=100)
    sheet = {"x": 0, "y": 0, "width": sheet_width, "height": sheet_height}

    st.subheader("Lista Elementów (Order List)")


    st.session_state.order_items = [
        {"name": "Formatka A", "width": 60, "height": 40, "quantity": 2},
        {"name": "Formatka B", "width": 30, "height": 50, "quantity": 1},
        {"name": "Formatka C", "width": 20, "height": 20, "quantity": 3}
    ]

    edited_df = st.data_editor(
        st.session_state.order_items,
        num_rows="dynamic",
        column_config={
            "name": st.column_config.TextColumn("Nazwa Elementu", required=True),
            "width": st.column_config.NumberColumn("Szerokość (Width)", min_value=1, required=True),
            "height": st.column_config.NumberColumn("Wysokość (Height)", min_value=1, required=True),
            "quantity": st.column_config.NumberColumn("Ilość (Quantity)", min_value=1, step=1, required=True),
        },
        use_container_width=True,
        key="data_editor_key"
    )

    strategies = ['area', 'max_side', 'width', 'height']

with col2:
    st.header("2. Uruchom Optymalizację")

    if st.button("Znajdź Najlepsze Ułożenie", type="primary", use_container_width=True):

        order_list_raw = edited_df

        if not order_list_raw or all(r['quantity'] == 0 for r in order_list_raw):
            st.error("Lista elementów jest pusta. Dodaj przynajmniej jeden element.")
        else:
            with st.spinner("Przetwarzanie..."):
                best_result = run_optimizer(sheet, order_list_raw, strategies)

            st.header("3. Wyniki")

            st.pyplot(draw_layout(best_result), use_container_width=True)

            st.subheader(f"Najlepsza strategia: {best_result['strategy']}")
            st.metric(
                label="Procent Odpadu (Waste)",
                value=f"{best_result['waste_percentage']:.2f}%",
                help="Im niżej, tym lepiej."
            )

            if best_result["unarranged"]:
                st.warning("Nie udało się zmieścić wszystkich elementów!")
                st.subheader("Elementy, które się nie zmieściły:")
                unarranged_df = pd.DataFrame(best_result["unarranged"])[["name", "width", "height"]]
                st.dataframe(unarranged_df, use_container_width=True)

            with st.expander("Zobacz surowe dane (JSON) dla najlepszego wyniku"):
                st.json(best_result)