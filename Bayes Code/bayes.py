
import sys
import random
import itertools

import numpy as np
import cv2 as cv


MAP_FILE = 'cape_python.png'

SA1_CORNERS = (130, 265, 180, 315) #(UL-X, UL-Y, LR-X, LR-Y)
SA2_CORNERS = (80, 255, 130, 305) #(UL-X, UL-Y, LR-X, LR-Y)
SA3_CORNERS = (105, 205, 155, 255) #(UL-X, UL-Y, LR-X, LR-Y)


class Search():
    """Bayesian Search and Resucue game with 3 search areas."""

    def __init__(self, name):
        self.name = name
        self.img = cv.imread(MAP_FILE, cv.IMREAD_COLOR)

        if self.img is None:
            print("Could not map file {}".format(MAP_FILE), file=sys.stderr)
            sys.exit(1)

        self.area_acutal = 0
        self.sailor_actual = [0,0]

        self.sa1 = self.img[SA1_CORNERS[1] : SA1_CORNERS[3], SA1_CORNERS[0] : SA1_CORNERS[2]]
        self.sa2 = self.img[SA2_CORNERS[1] : SA2_CORNERS[3], SA2_CORNERS[0] : SA2_CORNERS[2]]
        self.sa3 = self.img[SA3_CORNERS[1] : SA3_CORNERS[3], SA3_CORNERS[0] : SA3_CORNERS[2]]

        self.p1 = 0.2
        self.p2 = 0.5
        self.p3 = 0.3

        self.sept1 = 0
        self.sept2 = 0
        self.sept3 = 0

        self.area_searched1 = []
        self.area_searched2 = []
        self.area_searched3 = []

        self.draw_map((0,0))

    def draw_map(self, last_known):
        """Display basemap with scale, last known xy location search areas."""

        cv.line(self.img, (20,370), (70,370), (0,0,0), 2)
        cv.putText(self.img, '0', (8, 370), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0))
        cv.putText(self.img, '50 Nautical Miles', (71,370), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0))

        cv.rectangle(self.img, (SA1_CORNERS[0], SA1_CORNERS[1]), (SA1_CORNERS[2], SA1_CORNERS[3]), (0,0,0), 1)
        cv.putText(self.img, '1', (SA1_CORNERS[0] + 3,SA1_CORNERS[1] + 15), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0))
        cv.rectangle(self.img, (SA2_CORNERS[0], SA2_CORNERS[1]), (SA2_CORNERS[2], SA2_CORNERS[3]), (0,0,0), 1)
        cv.putText(self.img, '2', (SA2_CORNERS[0] + 3,SA2_CORNERS[1] + 15), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0))
        cv.rectangle(self.img, (SA3_CORNERS[0], SA3_CORNERS[1]), (SA3_CORNERS[2], SA3_CORNERS[3]), (0,0,0), 1)
        cv.putText(self.img, '3', (SA3_CORNERS[0] + 3,SA3_CORNERS[1] + 15), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0))

        cv.putText(self.img, '+', (last_known), cv.FONT_HERSHEY_PLAIN, 1, (0,0,255))
        cv.putText(self.img, '+ = Last Known Position', (274, 355), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0))
        cv.putText(self.img, '* = Actual Position', (275, 370), cv.FONT_HERSHEY_PLAIN, 1, (255,0,0))

        cv.imshow('Search Area', self.img)
        cv.moveWindow('Search Area', 750, 10)
        cv.waitKey(500)

    def sailor_final_location(self, num_search_areas):
        """Return the actual x,y location of the missing sailor."""
        # Find sailor coordinates with respect to any Search Area subarray.
        self.sailor_actual[0] = np.random.choice(self.sa1.shape[1])
        self.sailor_actual[1] = np.random.choice(self.sa1.shape[0])

        area = int(random.triangular(1, num_search_areas + 1))

        match area:
            case 1:
                x = self.sailor_actual[0] + SA1_CORNERS[0]
                y = self.sailor_actual[1] + SA1_CORNERS[1]
                self.area_acutal = 1
            case 2:
                x = self.sailor_actual[0] + SA2_CORNERS[0]
                y = self.sailor_actual[1] + SA2_CORNERS[1]
                self.area_acutal = 2
            case 2:
                x = self.sailor_actual[0] + SA3_CORNERS[0]
                y = self.sailor_actual[1] + SA3_CORNERS[1]
                self.area_acutal = 3
            case _:
                x = 0
                y = 0
                self.area_acutal = 0

        print(x,y)

        return x, y

    def calc_search_effectiveness(self):
        """Set decimal search effectiveness value per search areas."""

        self.sept1 = random.uniform(0.2, 0.9) # Seqrch at least 20% of area but never more than 90% of area
        self.sept2 = random.uniform(0.2, 0.9)
        self.sept3 = random.uniform(0.2, 0.9)

    def conduct_search(self, area_num, area_array, effectiveness_prob):
        """Return search result and list of searched coordinates"""

        local_y_range = range(area_array.shape[0])
        local_x_range = range(area_array.shape[1])
        coords = list(itertools.product(local_x_range, local_y_range))
        if area_num == 1:
            coords = [x for x in coords if x not in self.area_searched1]
        if area_num == 2:
            coords = [x for x in coords if x not in self.area_searched2]
        if area_num == 3:
            coords = [x for x in coords if x not in self.area_searched3]
        random.shuffle(coords)
        coords = coords[:int((len(coords) * effectiveness_prob))]

        if area_num == 1:
            for x in coords:
                self.area_searched1.append(x)
        if area_num == 2:
            for x in coords:
                self.area_searched2.append(x)
        if area_num == 3:
            for x in coords:
                self.area_searched3.append(x)


        loc_actual = (self.sailor_actual[0], self.sailor_actual[1])
        if area_num == self.area_acutal and loc_actual in coords:
            return 'Found in Area {}'.format(area_num), coords
        else:
            return 'Not Found', coords

    def revise_target_probs(self):
        """Update area target probabilities based on search effectiveness."""

        denom = self.p1 * (1 - self.sept1) + self.p2 * (1 - self.sept2) + self.p3 * (1 - self.sept3)

        self.p1 = self.p1 * (1 - self.sept1) / denom
        self.p2 = self.p2 * (1 - self.sept2) / denom
        self.p3 = self.p3 * (1 - self.sept3) / denom

def draw_menu(search_num):
    """Print menu of choices for conducting area search."""

    print('\nSearch {}'.format(search_num))
    print(
        """
        Choose next area to search

        0 ~ Quit
        1 ~ Search Area 1 twice
        2 ~ Search Area 2 twice
        3 ~ Search Area 3 twice
        4 ~ Search Area 1 & 2
        5 ~ Search Area 1 & 3
        6 ~ Search Area 2 & 3
        7 ~ Start Over
        """
    )

def main():
    app = Search("Cape_Python")
    app.draw_map(last_known=(160, 290))
    sailor_x, sailor_y = app.sailor_final_location(num_search_areas=3)
    print("-" * 65)
    print("\nInitial Target (P) Probabilities:")
    print("P1 = {:.3f}, P2 = {:.3f}, P3 = {:.3f}".format(app.p1, app.p2, app.p3))
    print(sailor_x, sailor_y)
    search_num = 1
    found = False

    while True:
        app.calc_search_effectiveness()
        draw_menu(search_num)
        if not found:
            choice = input("Choice: ")
            result_1 = 0
            result_2 = 0
            match choice:
                case "0": sys.exit()
                case "1":
                    result_1, coords_1 = app.conduct_search(1, app.sa1, app.sept1)
                    result_2, coords_2 = app.conduct_search(1, app.sa1, app.sept1)
                    app.sept1 = (len(set(coords_1 + coords_2))) / (len(app.sa1)**2)
                    app.sept2 = 0
                    app.sept3 = 0
                case "2":
                    result_1, coords_1 = app.conduct_search(2, app.sa2, app.sept2)
                    result_2, coords_2 = app.conduct_search(2, app.sa2, app.sept2)
                    app.sept1 = 0
                    app.sept2 = (len(set(coords_1 + coords_2))) / (len(app.sa2)**2)
                    app.sept3 = 0
                case "3":
                    result_1, coords_1 = app.conduct_search(3, app.sa3, app.sept3)
                    result_2, coords_2 = app.conduct_search(3, app.sa3, app.sept3)
                    app.sept1 = 0
                    app.sept2 = 0
                    app.sept3 = (len(set(coords_1 + coords_2))) / (len(app.sa3)**2)
                case "4":
                    result_1, coords_1 = app.conduct_search(1, app.sa1, app.sept1)
                    result_2, coords_2 = app.conduct_search(2, app.sa2, app.sept2)
                    app.sept3 = 0
                case "5":
                    result_1, coords_1 = app.conduct_search(1, app.sa1, app.sept1)
                    result_2, coords_2 = app.conduct_search(3, app.sa3, app.sept3)
                    app.sept2 = 0
                case "6":
                    result_1, coords_1 = app.conduct_search(2, app.sa2, app.sept2)
                    result_2, coords_2 = app.conduct_search(3, app.sa3, app.sept3)
                    app.sept1 = 0
                case "7":
                    main()
                case _:
                    print("\n Sorry, but that is not a vaild choice")
                    continue
            print(found)
            app.revise_target_probs()

            print("\nSearch {} Result 1 = {}".format(search_num, result_1), file=sys.stderr)
            print("Search {} Result 2 = {}".format(search_num, result_2), file=sys.stderr)
            print("Search {} Effectiveness (E)".format(search_num))
            print("E1 = {:.3f}, E2 = {:.3f}, E3 = {:.3f}".format(app.sept1, app.sept2, app.sept3))

            if result_1 == 'Not Found' and result_2 == 'Not Found':
                print('\nNew Target Probabilities (P) for Search {}:'.format(search_num + 1))
                print('P1 = {:.3f}, P2 = {:.3f}, P3 = {:.3f}'.format(app.p1, app.p2, app.p3))
            else:
                cv.circle(app.img, (sailor_x, sailor_y), 3, (255, 0, 0), -1)
                cv.imshow('Search Area', app.img)
                cv.waitKey(500)
                found = True

            search_num += 1
        else:
            print("You found the lost sailer!!!")
            print(
        """
        0 ~ Play Again
        Enter ~ Quit
        """
            )
            choice = input("Choice: ")

            match choice:
                case "0": main()
                case _:
                    sys.exit()




if __name__ == '__main__':
    main()
