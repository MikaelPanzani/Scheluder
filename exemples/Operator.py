# This Python file uses the following encoding: utf-8


class Operator :
    def __init__(self, stamp, name, attributions_ids_list):
        if type(stamp) == int:
            if type(name) == str:
                if type(attributions_ids_list) == list:
                    self.stamp = stamp
                    self.name = name
                    self.attributions_ids_list : list = attributions_ids_list
                else:
                    raise TypeError("TasksIDList n'est pas une list")
            else:
                raise TypeError("name n'est pas un str")
        else:
            raise TypeError("stamp n'est pas un int")
