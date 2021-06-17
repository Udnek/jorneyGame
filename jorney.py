from geopy import distance
from math import radians, sin, cos, acos
import csv
import folium #pip install folium
from IPython.core.display import HTML
import random as rd


def dist(crd1, crd2):
    slat = radians(float(crd1[0]))
    slon = radians(float(crd1[1]))
    elat = radians(float(crd2[0]))
    elon = radians(float(crd2[1]))
    dist = 6371.01 * acos(sin(slat) * sin(elat) + cos(slat) * cos(elat) * cos(slon - elon))
    return (dist)


def fc(count, cities):
    with open('worldcities.csv') as data:
        reader = csv.reader(data)
        crd1 = []
        for row in reader:
            if (row[1].lower() == cities[0].lower()):
                crd1.append(float(row[2]))
                crd1.append(float(row[3]))
                break

        if crd1 == []:
            return False

        elif count != 1:
            crd2 = []
            for row in reader:
                if (row[1].lower() == cities[1].lower()):
                    crd2.append(float(row[2]))
                    crd2.append(float(row[3]))
                    break
            if crd2 == []:
                return False
            else:
                return ([crd1, crd2])
        else:
            return crd1


def marker(c, mtype, color, name):
    global m
    if mtype == "c":
        folium.CircleMarker(
            location=c,
            radius=5,
            popup=(name[0].upper() + name[1:].lower()),
            color=color,
            fill=True,
            fill_color=color,
        ).add_to(m)

    else:
        folium.Marker(
            location=c,
            popup=(name[0].upper() + name[1:].lower()),
            icon=folium.Icon(color=color)  # icon="info-sign"),
        ).add_to(m)


def circle(c):
    global m
    folium.Circle(
        radius=200000,
        location=c,
        popup="radius",
        color="green",
        fill=False,
    ).add_to(m)


def line(c):
    global m
    folium.PolyLine(c, weight=3, color="red").add_to(m)


###################################
###################################
###################################
###################################
###################################

mess = "Start city: "
while True:
    startcity = input(mess)
    cordsstartcity = fc(1, [startcity])
    if cordsstartcity == False:
        mess = "City not found! Enter correct start city: "
    else:
        break

mess = "Finish city: "
while True:
    finishcity = input(mess)
    cordsfinishcity = fc(1, [finishcity])
    if cordsfinishcity == False:
        mess = "City not found! Enter correct finish city: "
    else:
        break

# startcity ="Moscow"
# finishcity = "Warsaw"
# cordsstartcity = fc(1, [startcity])
# cordsfinishcity = fc(1, [finishcity])


m = folium.Map(location=cordsstartcity, zoom_start=7)

marker(cordsstartcity, "d", "green", startcity)
marker(cordsfinishcity, "d", "red", finishcity)
circle(cordsstartcity)

# HTML(m._repr_html_())

points = [[startcity, cordsstartcity]]
days = 1

# food = 10
# money = 1000

food = input("Input amount of food, default = 10: ")
try:
    food = int(food)
except:
    food = 10

money = input("Input amount of money, default = 100: ")
try:
    money = int(money)
except:
    money = 100

display(m)

game = True
while game:
    pmoney = rd.randint(1, 3)
    money += pmoney
    print()
    print("Your money: " + str(money) + "(+" + str(pmoney) + ")")
    print("Your food: " + str(food))
    print()

    if food <= -4:
        game = False
        print("You died! Because of food!")

    mess = "Next city: "
    action = input("Do you want to trade (t) or move (m)?: ")

    if action.lower() != "t":
        while True:
            city = input(mess)
            cordcity = fc(1, [city])
            if cordcity == False:
                mess = "City not found! Enter correct city: "
            elif 200 < dist(points[-1][1], cordcity):
                mess = "City too far! Enter city closer than 200 km: "
            else:
                break

        m = folium.Map(location=cordcity, zoom_start=7)

        for i in range(1, len(points)):
            line([points[i - 1][1], points[i][1]])
            marker(points[i][1], "c", "blue", points[i][0])

        line([points[-1][1], cordcity])

        marker(cordcity, "d", "blue",
               city + ", Day: " + str(days))

        points.append([city, cordcity])

        marker(cordsstartcity, "d", "green", startcity)
        marker(cordsfinishcity, "d", "red", finishcity)

        mfood = rd.randint(1, 3)

        food -= mfood

        print()
        print("Your money: " + str(money))
        print("Your food: " + str(food) + "(-" + str(mfood) + ")")
        print()

        if city.lower() == finishcity.lower():
            print("You win! You finaly got to " + str(city[0].upper() + city[1:].lower()) + "!")
            game = False
        else:
            circle(cordcity)

        display(m)

    else:
        price = rd.randint(3, 40)
        while True:
            print()
            print("Food price:" + str(price))
            print()
            print("Your money: " + str(money))
            print("Your food: " + str(food))
            print()
            choice = input("What do you want to buy food(b) or sell(s), or cancel(c)?: ")
            if choice == "b":
                amount = input("Enter amount of food to buy, default = 0: ")
                try:
                    amount = int(amount)
                    if money >= price * amount:
                        food += amount
                        money -= price * amount
                        print("You buy " + str(amount) + " food.")
                    else:
                        print("You dont have enough money!")
                except:
                    print("You dont buy anything!")
            elif choice == "s":
                amount = input("Enter amount of food to sell, default = 0: ")
                try:
                    amount = int(amount)
                    if food >= amount:
                        food -= amount
                        money += price * amount
                        print("You sell " + str(amount) + " food.")
                    else:
                        print("You dont have enough food to sell!")
                except:
                    print("You dont buy anything!")

            else:
                mfood = rd.randint(1, 3)
                food -= mfood
                print()
                print("Your money: " + str(money))
                print("Your food: " + str(food) + "(-" + str(mfood) + ")")
                print()
                break

    days += 1

display(m)