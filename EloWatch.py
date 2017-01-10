import requests
import json

import sys

__author__ = 'Talaal Mirza'


#   https://api.lootbox.eu

def getAndShare(plat, region, apiTag):
    print("Gathering info. This might take a while")
    requestURL = "https://api.lootbox.eu/{}/{}/{}/profile".format(plat, region, apiTag)
    mainRequest = requests.get(requestURL)
    with open(apiTag + '.json', 'w') as outfile:
        json.dump(mainRequest.json(), outfile)
    print("DONE! Json saved as {}.json".format(apiTag))

    with open(apiTag + '.json') as userInfo:
        info = json.load(userInfo)

    #   Output info
    name, elo, hours, count, losses, wins = parseInfo(info)
    print(prettyInfo(name, elo, hours, count, losses, wins))


def prettyInfo(name, elo, hours, count, losses, wins):
    wp = str(int(wins) / int(count))
    card = '''
           Competitive Info.
           Username:            {}
           Rank:                {}
           Hours Played:        {}
           Total Games Played:  {}
           Wins:                {}
           Losses:              {}
           Win Percentage:      {}'''.format(name, elo, hours, count, wins, losses, wp)

    return card


def parseInfo(info):
    name = info["data"]["username"]
    elo = info["data"]["competitive"]["rank"]
    compHours = info["data"]["playtime"]["competitive"]
    compGamesPlayed = info["data"]["games"]["competitive"]["played"]
    compGamesLost = info["data"]["games"]["competitive"]["lost"]
    compGamesWon = info["data"]["games"]["competitive"]["wins"]

    return name, elo, compHours, compGamesPlayed, compGamesLost, compGamesWon


def checkValidPlat(plat):
    validPlatforms = ['pc', 'psn', 'xbl']

    return plat in validPlatforms


def checkValidRegion(region):
    validRegions = ['cn', 'eu', 'kr', 'us']

    return region in validRegions


def checkBattleTagForm(tag):
    if '#' not in tag or '#' == tag[0] or '#' == tag[-1]:
        return False, None, None

    uTag = tag.split('#')[0]
    uNum = tag.split('#')[1]

    if uTag[0][0].isalpha() and uTag.isalnum() and uNum.isnumeric() and len(uNum) == 4:  # BattleTag
        return True, uTag, uNum

    return False, None, None


def main():
    Tag = input("> ")
    valid, uTag, uNum = checkBattleTagForm(Tag)

    #   Improper BattleTag
    if not valid:
        print("\nPlease enter a proper BattleTag\n"
              "Example\tTPineapples#1286\n")
        main()

    apiTag = uTag + "-" + uNum

    plat = None
    platFlag = False
    print("Please enter your corresponding platform\n"
          "\tEnter This\tIf your platform is this\n"
          "\tpc\t\t\tPC\n"
          "\txbl\t\t\tXBox\n"
          "\tpsn\t\t\tPlayStation\n")

    while not platFlag:
        plat = input("> ")
        platFlag = checkValidPlat(plat)

        if not platFlag:
            print(plat + " is not a valid option\n"
                         "Please enter one of the following\n"
                         "\tEnter This\tIf your platform is this\n"
                         "\tpct\t\t\tPC\n"
                         "\txblt\t\t\tXBox\n"
                         "\tpsnt\t\t\tPlayStation\n")

    region = None
    regionFlag = False
    if plat != 'pc':
        region = 'global'
    else:
        print("Please enter your corresponding region\n"
              "\tEnter This\tIf your region is this\n"
              "\tcn\t\t\tChina\n"
              "\teu\t\t\tEurope\n"
              "\tkr\t\t\tSouth Korea\n"
              "\tus\t\t\tUS(Americas)\n")

    while not regionFlag:
        region = input("> ")
        regionFlag = checkValidRegion(region)

        if not regionFlag:
            print(region + " is not a valid option\n"
                           "Please enter one of the following\n"
                           "\tEnter This\tIf your region is this\n"
                           "\tcn\t\t\tChina\n"
                           "\teu\t\t\tEurope\n"
                           "\tkr\t\t\tSouth Korea\n"
                           "\tus\t\t\tUS(Americas)\n")

    #   Retrieve and present comp. info
    getAndShare(plat, region, apiTag)

    #   Now what?
    print("\nWhat would you like to do now?\n"
          "Enter one of the following\n"
          "\t0:\tQuit\n"
          "\t1:\tNew Search\n"
          "\t2:\tUpdate\n")
    endgame = None
    while endgame is None:
        endgame = input("> ")
        if endgame == '0':
            sys.exit()
        elif endgame == '1':
            print("\nPlease enter your BattleTag\n"
                  "\tFor example:\tTPineapples#1286")
            main()
        elif endgame == '2':
            getAndShare(plat, region, apiTag)
            endgame = None
            print("\nWhat would you like to do now?\n"
                  "Enter one of the following\n"
                  "\t0:\tQuit\n"
                  "\t1:\tNew Search\n"
                  "\t2:\tUpdate\n")
        else:
            print("\nPlease enter a valid input\n"
                  "Enter one of the following\n"
                  "\t0:\tQuit\n"
                  "\t1:\tNew Search\n"
                  "\t2:\tUpdate Current User\n")


########################################################################################################################
#   Begin
print("Welcome to EloWatch v0.1\n"
      "Please enter your BattleTag\n"
      "\tFor example:\tTPineapples#1286")
main()
