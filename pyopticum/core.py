# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['ureg', 'Help_system', 'POD_as_top_level_attributes', 'Sensor', 'Lens', 'aPyopticum']

# Cell
#nbdev_comment from __future__ import print_function
from typing import overload
import random
import pint
import math
import inspect
import os

try:
      from IPython.display import display, Math, Latex, HTML, Markdown
      display(HTML("Using Ipython"))
      ascii_print = print
      def print(*args, **kwargs):
        for item in args:
            display(item)

except ImportError:
      from bs4 import BeautifulSoup
      from markdown import markdown
      print("unable to import IPython, ignoring, using basic print")


### Lets set up Pint with some useful extra entities

#export
ureg = pint.UnitRegistry()
ureg.define('Circle_of_confusion = [] = coc')
ureg.define('Aperture = [] = fnumber')

# Cell
class Help_system:
    def __init__(self):
        pass

    def initialize_help_system(self):
        #print(f"createing help system")
        self.__dict__['ureg'] = pint.UnitRegistry()
        self.__dict__['is_ipython'] = self.__is_running_under_ipython()
        if self.is_ipython:
            self.ureg.default_format = "L"
        else:
            self.ureg.default_format = "P"

    def __is_running_under_ipython(self):
        try:
            get_ipython
            return True
        except:
            return False

    def wrap_unit(self, eqn, style):
        if (self.is_ipython):
            if style.lower() == "math":
                return Math(eqn)
            if style.lower() == "html":
                return HTML(eqn)
            if style.lower() == "latex":
                return Latex(eqn)
            if style.lower() == "markdown":
                return Markdown(eqn)
        else:
            if style.lower() == "html":
                soup = BeautifulSoup(eqn)
                return soup.get_text()
            if style.lower() == "markdown":
                html = markdown(eqn)
                soup = BeautifulSoup(html, features='html.parser')
                return soup.get_text()
        return eqnprint

    def help(self, command):
        """
        runs the help function for the command
        """
        method_to_call = getattr(self, command+'_help')
        result = method_to_call()

# Cell
class POD_as_top_level_attributes:
    def __init__(self):
        print("POD init")
        self.__dict__['class_preamble'] = self.__class__.__name__
        self.__dict__['pod_name'] = ""

    def __getattr__(self, attr):
        attr = attr.replace("_"+self.__dict__['class_preamble'],"")
        #print(f"getting {attr}")
        variables = vars(self.__dict__[self.__dict__['pod_name']])
        if attr in variables:
            return getattr(self.__dict__[self.__dict__['pod_name']],attr)

        methods = [i for i in dir(self) if not inspect.ismethod(i)]
        #print(f"getattr --> {attr} --> variables :{variables} \n methods :{methods}")
        #next check if we can calculate it
        if ("__" + attr in methods):
            return getattr(self,"__"+attr)()
        else:
            raise Exception(f"__getattr__ Cannot find Attribute :{attr} ")

    def __setattr__(self, attr, value):
        attr = attr.replace("_"+self.class_preamble,"")
        variables = vars(self.__dict__[self.__dict__['pod_name']])
        methods = [i for i in dir(self) if not inspect.ismethod(i)]
        not_methods = [i for i in dir(self) if  inspect.ismethod(i)]
        print(f"setattr --> {attr} --> variables :{variables} \n methods :{methods}")
        if ("_"+self.__dict__['class_preamble']+"__" + attr in methods):
            raise Exception(f"__setattr__ Attribute [ {attr} ] is not writeable ")

        if attr == self.__dict__['class_preamble']:
            if type(value) == type(self.__dict__[self.__dict__['pod_name']]):
                self.__dict[pod_name] == self.__dict__[self.__dict__['pod_name']]
            else:
                raise Exception(f" sensor data must be of sensor data class type")
        #next make it look like these are top level attributes
        if attr in variables:
            setattr(self.__dict__[self.__dict__['pod_name']],attr,value)
        #if this is in the right class lets let it be changed here (should never be called)
        elif (attr in methods):
            #self.__dict__[attr] = value
            raise Exception(f"__setattr__ Cannot set this Attribute : {attr}")
        #ok i give up
        else:
            raise Exception(f"__setattr__ Attribute [ {attr} ] is not found ")

# Cell
class Sensor(POD_as_top_level_attributes, Help_system):
    """
    class to hold sensor data and methods
    """
    class Raw_sensor_data:
        def __init__(self):
            self.die_size_x = 0
            self.die_size_y = 0
            self.pixel_size_x = 0
            self.pixel_size_y = 0
            self.diagonal = 0
            self.circle_of_confusion = 0
            self.circle_of_confusion_method = "Modern"

    @ureg.wraps(None, (None, 'mm','mm','micrometer','micrometer'))
    def __init__(self, die_size_x,die_size_y, pixel_size_x,pixel_size_y):
        # system setup
        self.initialize_help_system()
        self.__dict__['class_preamble'] = self.__class__.__name__
        self.__dict__['pod_name'] = "sensor_data"
        self.__dict__[self.pod_name] = self.Raw_sensor_data()
        #class variable setup
        self.sensor_data.die_size_x = die_size_x*ureg.mm
        self.sensor_data.die_size_y = die_size_y*ureg.mm
        self.sensor_data.diagonal = self.__diagonal()
        self.sensor_data.pixel_size_x = 2.7 *ureg.micrometer
        self.sensor_data.pixel_size_y = 2.7 *ureg.micrometer
        self.sensor_data.circle_of_confusion_method = "Modern"
        self.sensor_data.circle_of_confusion = self.__circle_of_confusion(frame_diagonal=self.diagonal, focal_length=0*ureg.mm, method=self.sensor_data.circle_of_confusion_method)


    @ureg.wraps('mm',(None))
    def __diagonal(self):
        return math.sqrt( math.pow(self.sensor_data.die_size_x.magnitude,2) + math.pow(self.sensor_data.die_size_y.magnitude,2) )*ureg.mm


    def circle_of_confusion_help(self)->None:
        print(HTML("<H2>Circle of Confusion</H2>"))
        print(HTML("Modern, Standard Method (Default)	Frame’s diagonal / 1500"))
        print(HTML("Zeiss, Formula	Frame’s diagonal / 1730"))
        print(HTML("Kodak, Formula	Focal length / 1720"))
        print(HTML("Archaic, Standard	Frame’s diagonal / 1000"))
        print(HTML("<code> circle_confusion(frame_diagonal,focal_length,method = 'modern')</code>"))
        return 1

    def set_circle_of_confusion_method(self,method="modern",*args, **kwargs):
        coc_method = [ "modern", "zeiss","kodak", "archaic" ]
        if method not in coc_method:
            raise ValueError("Circle of confusion method not supported")
        self.sensor_data.circle_of_confusion_method = method
        focal_length = None
        if method == "archaic":
            #search for a lens
            if "focal_length" in kwargs:
                if isinstance(kwargs["focal_length"], Lens ):
                    print("got a lens object")
                    focal_length == kwargs["focal_length"].focal_length
                elif isinstance(kwargs["focal_length"], ureg.mm):
                    print("got a length in mm")
                    focal_length == kwargs["focal_length"]*ureg.mm
                elif isinstance(in_arg, (int, float, long)):
                    focal_length = in_arg*ureg.mm
            else:
                for in_arg in args:
                    if isinstance(in_arg,Lens):
                        focal_length = in_arg.focal_length
                    elif isinstance(in_arg, ureg.mm):
                        focal_length = in_arg
                    elif isinstance(in_arg, (int, float, long)):
                        focal_length = in_arg*ureg.mm
        #ok if were still dont have something valid raise an error
        if focal_length  is None:
            raise ValueError("Focal Length must be specified and greater than 0")
        print(f"focal length is {focal_length} {type(focal_length)}")
        self.sensor_data.circle_of_confusion = self.__circle_of_confusion(frame_diagonal=self.diagonal, focal_length=focal_length, method=self.sensor_data.circle_of_confusion_method)

    @ureg.wraps(ureg.coc, (None, 'mm','mm',None))
    def __circle_of_confusion(self,frame_diagonal, focal_length, method):
        def modern(frame_diagonal, ignore):
            return frame_diagonal/1500
        def zeiss(frame_diagonal, ignore):
            return frame_diagonal/1730
        def kodak(ignore, focal_length):
            return focal_length/1720
        def archaic(frame_diagonal, ignore):
            return focal_length/1000

        coc_method = { "modern": modern,
                      "zeiss": zeiss,
                      "kodak": kodak,
                      "archaic": archaic}
        if method.lower() not in coc_method:
            raise ValueError(f"Unknown Circle of Confusion Method {method}")

        #if focal_length
        coc = coc_method.get(method.lower())(frame_diagonal,focal_length)
        return coc * ureg('coc')

# Cell
class Lens(POD_as_top_level_attributes, Help_system):
    class Raw_lens_data():
        def __init__(self):
            self.focal_length = 0*ureg.mm
            self.aperture = 0*ureg.mm

    @ureg.wraps(None,(None,'mm','Aperture'))
    def __init__(self, focal_length, aperture):
        # system setup
        self.initialize_help_system()
        self.__dict__['class_preamble'] = self.__class__.__name__
        self.__dict__['pod_name'] = "lens_data"
        self.__dict__[self.pod_name] = self.Raw_lens_data()

        self.lens_data.focal_length = focal_length*ureg.mm
        self.lens_data.aperture = aperture*ureg.Aperture
        print(self.lens_data.focal_length)

    def angle_of_view_help(self):
        print(HTML("<h2>Angle of view</h2>"))
        print(HTML("<span>Figures out the witdh of the angle of view, given sensor / lens characteristics.</span>"))
        print(self.wrap_unit(r"\theta=2\cdot\arctan\left(\frac{h(s-f)}{2sf}\right)","math"))
        print(HTML("<code> angle_of_view(frame_dimension, focal_length, focus_distance)</code>"))

    @ureg.wraps(ureg.radians, (None, 'mm','mm','mm' ))
    def angle_of_view(self, frame_dimension, focal_length, focus_distance):
        if self.echo_params:
            print(HTML(f"<code>Frame Dimension {frame_dimension} </br>Focal Length {focal_length}</br>Focus Distance {focus_distance}</code>"))
        aov = 2.0 * math.atan((frame_dimension * (focus_distance - focal_length))/(2*focus_distance*focal_length))
        if self.echo_params:
            print(HTML(f"<span>Angle of View :{aov}"))
        return aov

    def field_of_view_help(self):
        print(self.wrap_unit("<h2>Field of View</h2>","html"))
        print(self.wrap_unit("<a> implementation of this equation </a>","html"))
        print(self.wrap_unit(r'w=2s\cdot\tan\left(\frac{\theta}{2}\right)',"Math"))

    @ureg.wraps(ureg.meters, (None, 'm', 'rad') )
    def field_of_view(self, focus_distance, angle_of_view):
        view_width = 2*focus_distance*math.tan( angle_of_view / 2.0)
        return view_width

    def hyperfocal_distance_help(self):
        print(HTML("<H2>Hyperfocal Distance</H2>"))
        print(HTML("<span> calculates hyperfocal distance"))
        print(self.wrap_unit(r"H=\frac{f^{2}}{N\cdot{c}}+f","Math"))

    @ureg.wraps(ureg.meters, (None, 'mm','fnumber','coc'))
    def hyperfocal_distance(self, focal_length, f_number, circle_of_confusion=-1):
        if type(circle_of_confusion) == type( Sensor ):
            this_circle_of_confusion = circle_of_confusion.circle_of_confusion
        elif type(circle_of_confusion) == type(int):
            this_circle_of_confusion = circle_of_confusion

        if type(f_number) == type ( Lens):
            this_fnumber = f_number.aperture
        elif type(f_number) == type( int ):
            this_fnumber = f_number

        hfd = (focal_length*focal_length)/(this_f_number*this_circle_of_confusion)+focal_length
        return hfd

# Cell
class aPyopticum(Help_system):
    """
    Initial class to hold optical formula's etc

    """

    ###################################################################################################################
    def __init__(self, echo_params = False):
        #system setup
        self.initialize_help_system()
        #direct setup
        self.data = []
        self.echo_params = echo_params



    def about(self):
        """
        about this library and usage
        """
        print(self.wrap_unit("<h1>Pyopticum</h1>","html"))
        print(self.wrap_unit("see <a href='https://github.com/jlovick/Pyopticum'> Pyopticum </a> for source","html"))