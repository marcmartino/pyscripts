#!/usr/bin/python3
import json
import readline
from getInput import *
from tabulate import tabulate

with open('./recipes.json', 'r') as f:
    recipes = json.load(f)


class autoComplete(object):

    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches
                self.matches = [s for s in self.options
                                    if text in s]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try:
            return self.matches[state]
        except IndexError:
            return None


def bakerCalc(flour: int, style: dict) -> dict:
    workingRecipe = {'flour': float(flour)}
    for i in style.keys():
        if i == "starter":
            mult = int(totalWeight(style["starter"]))
            i = "preferment"
        else:
            mult = style[i]
        workingRecipe[i] = float(flour) * mult / 100
    return workingRecipe


def dividePies(totalWeight: float, pieWeight: int) -> (float, float):
    pies = round(totalWeight / (pieWeight if pieWeight else 260))
    eachPie = round(totalWeight / pies)
    return pies, eachPie


def totalWeight(recipe: dict) ->float:
    return sum(recipe.values())


def printTable(ingredients: dict) -> str:
    total = int(sum(ingredients.values()))
    table = []
    headers = ["Ingredient", "Amount", "%"]
    for k,v in ingredients.items():
        # re-calculate the % of each ingredient so it can be printed, truncating
        # at 2 decimal places
        percent = v * 100.0 / float(ingredients['flour'])
        percent = '{:.2f}'.format(percent)
        v = '{:.2f}'.format(v)
        table.append([k, v, percent])
    table.append(["TOTAL", total, None])
    print(tabulate(table, headers, numalign='right', tablefmt="github"))
    print('\n')

completer = autoComplete(recipes.keys())
readline.set_completer(completer.complete)
readline.parse_and_bind('tab: complete')

def main():
    choice = initChoice(printRecipes())
    if choice.isdigit():
        flour = choice
        choice = "dopny"
    elif choice in recipes:
        flour = ''
        while not flour.isdigit():
            flour = input('Type the desired amount of flour: ')
    print("\n================================================")
    print("#### %s\n"% choice.upper())
    if "starter" in recipes[choice]:
        print("##### Starter")
        printTable(bakerCalc(flour, recipes[choice]["starter"]))
        print("##### Final Dough")
    recipe = bakerCalc(flour, recipes[choice])
    total = totalWeight(recipe)
    printTable(recipe)
    printPies(total)

    print("================================================\n")
    main()

if __name__ == "__main__":
    main()
