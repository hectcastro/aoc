import fileinput
from collections import defaultdict
from fileinput import FileInput
from itertools import chain
from typing import Dict, List, Set


def handler(raw_foods: FileInput) -> str:
    all_ingredients: List[List[str]] = []
    allergen_index: Dict[str, List[int]] = defaultdict(list)

    for index, raw_food in enumerate(raw_foods):
        raw_ingredients, raw_allergens = raw_food.strip().split(" (")
        ingredients = raw_ingredients.split(" ")
        allergens = raw_allergens.replace("contains ", "").rstrip(")").split(", ")

        all_ingredients.append(ingredients)

        for allergen in allergens:
            allergen_index[allergen].append(index)

    allergen_candidates: Dict[str, Set[str]] = {}

    for allergen in allergen_index.keys():
        allergen_candidate: List[Set] = []

        for al in allergen_index[allergen]:
            allergen_candidate.append(set(all_ingredients[al]))

        allergen_candidates[allergen] = set.intersection(*allergen_candidate)

    unmatchable_ingredients: Set[str] = set(list(chain(*all_ingredients))).difference(
        set.union(*(allergen_candidates.values()))
    )

    unmatchable_ingredient_count = 0

    for ingredients in all_ingredients:
        for ingredient in ingredients:
            if ingredient in unmatchable_ingredients:
                unmatchable_ingredient_count += 1

    visited = set()
    while any(
        len(ingredient_set) > 1 for ingredient_set in allergen_candidates.values()
    ):
        for key, value in allergen_candidates.items():
            if len(value) == 1 and key not in visited:
                visited.add(key)
                break
        for key2, value2 in allergen_candidates.items():
            if key2 != key:
                value2.difference_update(value)

    return ",".join(
        next(iter(v))
        for _, v in sorted(allergen_candidates.items(), key=lambda v: v[0])
    )


if __name__ == "__main__":
    print(handler(fileinput.input()))
