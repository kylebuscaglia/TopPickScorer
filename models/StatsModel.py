import xml.etree.ElementTree as ET
import json

class StatsModel:

    def __init__(self):
        self.passing_td = 0
        self.rushing_td = 0
        self.receiving_td = 0
        self.rushing_yds = 0
        self.receiving_yds = 0
        self.passing_yds = 0
        self.fumbles_kept = 0
        self.fumbles_lost = 0
        self.int_thrown = 0
        self.pick_six = 0
        self.two_pt_con = 0
        self.catches = 0

    def convert_stat_line(self, stat_line: str):
        stat_tree_root = ET.fromstring(stat_line)
        for stat_child in stat_tree_root:
            #print(stat_child.attrib, stat_child.text)
            if 'data-stat' not in stat_child.attrib:
                continue
            if stat_child.attrib['data-stat'] == 'rush_yds':
                self.rushing_yds = float(stat_child.text)
            if stat_child.attrib['data-stat'] == 'rush_td':
                self.rushing_td = float(stat_child.text)
            if stat_child.attrib['data-stat'] == 'rec':
                self.catches = float(stat_child.text)
            if stat_child.attrib['data-stat'] == 'rec_yds':
                self.receiving_yds = float(stat_child.text)
            if stat_child.attrib['data-stat'] == 'rec_td':
                self.receiving_td = float(stat_child.text)
            if stat_child.attrib['data-stat'] == 'fumbles':
                self.fumbles_kept = float(stat_child.text)
            if stat_child.attrib['data-stat'] == 'fumbles_lost':
                self.fumbles_lost = float(stat_child.text)
            if stat_child.attrib['data-stat'] == 'pass_yds':
                self.passing_yds = float(stat_child.text)
            if stat_child.attrib['data-stat'] == 'pass_td':
                self.passing_td = float(stat_child.text)
            if stat_child.attrib['data-stat'] == 'pass_int':
                self.int_thrown = float(stat_child.text)
            if stat_child.attrib['data-stat'] == 'two_pt_md':
                if stat_child.text is None:
                    continue
                self.two_pt_con = float(stat_child.text)
        return stat_tree_root.tag

    def calculate_points(self):
        print(json.dumps(self.__dict__))
        catch_pts = self.catches / 2
        td_pts = (self.rushing_td + self.receiving_td) * 6
        qb_td_pts = self.passing_td * 4
        rush_yd_pts = self.calculate_rush_yd_pts()
        receiving_yd_pts = self.calculate_wr_yd_pts()
        passing_yd_pts = self.calculate_passing_yd_pts()
        int_points = self.int_thrown * -1
        fumble_pts = self.calculate_fumble_pts()
        two_pt_con_pts = self.two_pt_con * 2
        total_pts = catch_pts + td_pts + qb_td_pts + rush_yd_pts + \
                    receiving_yd_pts + passing_yd_pts + int_points + fumble_pts + two_pt_con_pts
        return round(total_pts, 2)

    def calculate_rush_yd_pts(self):
        rush_yd_pts = self.rushing_yds / 10
        if self.rushing_yds >= 150:
            rush_yd_pts = rush_yd_pts + 2

        return rush_yd_pts

    def calculate_wr_yd_pts(self):
        wr_yd_pts = self.receiving_yds / 10
        if self.receiving_yds >= 150:
            wr_yd_pts = wr_yd_pts + 2

        return wr_yd_pts

    def calculate_passing_yd_pts(self):
        passing_yd_pts = round(self.passing_yds / 25, 2)
        if self.passing_yds >= 350:
            passing_yd_pts = passing_yd_pts + 2

        return passing_yd_pts

    def calculate_fumble_pts(self):
        fumble_pts = (self.fumbles_kept * -0.5) + (self.fumbles_lost * -1)
        return fumble_pts
