import datetime
import PIL.PngImagePlugin
from separated_code import *
import unittest

# please use pycharm to test these codes instead of terminal
class MyTest(unittest.TestCase):

    # test number: 1
    def test_date_time_function(self):
        """test date_time function"""
        self.assertEqual(date_time(), [str(strftime("%I:%M:%S %p")) + str(strftime("%A")) + str(strftime("%B %d, %Y"))])

    # test number: 2
    def test_about_info_function(self):
        """test about_info function"""
        # note: the tkinter.messagebox.showinfo will return ok after the message is shown on the screen
        self.assertEqual(acknowlegement(), "ok")

    # test number: 3
    def test_check_credential_function(self):
        """test check_credential function"""
        username = "admin"
        password = "admin"
        self.assertTrue(check_credential(username,password))

        username = "apple"
        password = "apple"
        self.assertFalse(check_credential(username,password))

    # test number: 4
    def test_open_json_file_function(self):
        """test open_json_file function"""
        filename = "profile.json"
        self.assertTrue(open_json_file(filename))

        filename = "banana.json"
        self.assertFalse(open_json_file(filename))

    # test number = 5
    def test_save_profile_function(self):
        """test save profile function"""
        filename = "banana.json"
        username = ""
        contact = ""
        password = ""
        self.assertFalse(save_profile(username,contact,password,filename))

        filename = "profile.json"
        username = "apple"
        contact = "apple@griffithuni.com"
        password = "apple"
        self.assertTrue(save_profile(username,contact,password,filename))

    # test number = 6
    def test_open_file_dialog_function(self):
        """test open_file_dialog function"""
        # please select "New York Restaurant.csv"
        file = open_file_dialog()
        if file:
            self.assertTrue(file)
        else:
            self.assertFalse(file)

    # test number = 7
    def test_loadfile_function(self):
        """test loadfile function"""
        filename = "New York Restaurant.csv"
        self.assertTrue(loadfile(filename))
        filename = "apple"
        self.assertFalse(loadfile(filename))

    # test number = 8
    def test_convert_date_format_function(self):
        """test convert_date_format function"""
        date = "12/31/2021"
        self.assertEqual(convert_date_format(date), "2021-12-31")

    # test number = 9
    def test_make_a_list_of_img_function(self):
        """test make_a_list_of_img function"""
        img_list = make_a_list_of_img()
        for i in img_list:
            self.assertIsInstance(i, PIL.PngImagePlugin.PngImageFile)

    # test number = 10
    def test_convert_csv_to_db_function(self):
        filename = "New York Restaurant.csv"
        self.assertTrue(convert_csv_to_db(filename))

        filename = "apple"
        self.assertFalse(convert_csv_to_db(filename))

    # test number = 11
    def test_search_by_date(self):
        start_date = "2016-01-01"
        end_date = "2016-01-05"
        self.assertTrue(search_by_date(start_date,end_date))

        start_date = "2021/01/01"
        end_date = "2021/01/05"
        self.assertFalse(search_by_date(start_date,end_date))

    # test number = 12
    def test_search_by_date_keyword(self):
        start_date = "2016-01-01"
        end_date = "2016-01-05"
        keyword = "Queens"
        self.assertTrue(search_by_date_keyword(start_date,end_date,keyword))

        start_date = "2021/01/01"
        end_date = "2021/01/05"
        keyword = "apple"
        self.assertFalse(search_by_date_keyword(start_date, end_date, keyword))

    # test number = 13
    def test_view_chart_suburbs(self):
        start_date = "2016-01-01"
        end_date = "2016-01-05"
        self.assertTrue(view_chart_suburbs(start_date, end_date))

        start_date = "2021/01/01"
        end_date = "2021/01/05"
        self.assertFalse(view_chart_suburbs(start_date, end_date))

    # test number = 14
    def test_view_graph_animal_related_case(self):
        start_date = "2016-01-01"
        end_date = "2016-01-05"
        suburb = "Queens"
        animal = "rat"
        self.assertTrue(view_graph_animal_related_case(start_date, end_date,suburb,animal))

        start_date = "2021/01/01"
        end_date = "2021/01/05"
        suburb = "apple"
        animal = "banana"
        self.assertFalse(view_graph_animal_related_case(start_date, end_date,suburb,animal))

    # test number = 15
    def test_compare_cuisine(self):
        start_date = "2016-01-01"
        end_date = "2016-01-05"
        cuisine1 = "Thai"
        cuisine2 = "Japan"
        self.assertTrue(compare_cuisine(start_date,end_date,cuisine1,cuisine2))

        start_date = "2021/01/01"
        end_date = "2021/01/05"
        cuisine1 = "apple"
        cuisine2 = "banana"
        self.assertFalse(compare_cuisine(start_date,end_date,cuisine1,cuisine2))

    # test number = 16
    def test_date_object(self):
        date = '05/05/2021'
        self.assertIsInstance(date_object(date), datetime)

    # test number = 17
    def test_get_column_name(self):
        self.assertTrue(get_column_name())

    # test number = 18
    def test_get_radio_button_value(self):
        try:
            self.assertIs(get_radio_button_value(),"Line")
        except:
            self.assertIs(get_radio_button_value(), "")

    # test number = 19
    def test_write_json_file(self):
        filename = "samsung.json"
        text = "I love Python programming language."
        self.assertTrue(write_json_file(filename,text))

    # test number = 20
    def test_read_data_by_row(self):
        try:
            self.assertTrue(read_data_by_row())
        except:
            self.assertFalse(read_data_by_row())


if __name__ == '__main__':
    unittest.main()



