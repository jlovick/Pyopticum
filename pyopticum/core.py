# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['ureg', 'ureg', 'Help_system', 'Lens', 'Sensor', 'Camera', 'aPyopticum']

# Cell
#nbdev_comment from __future__ import print_function
from typing import overload
import random

import pint

#from functools import singledispatch
from multipledispatch import dispatch

import math
import inspect
import os
import pytest
import ipytest
ipytest.autoconfig()


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
ureg = pint.UnitRegistry(system='SI')
ureg.define('Circle_of_confusion = millimeter = coc')
ureg.define('Aperture =  = fnumber')

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
        self.__dict__["echo_params"] = False

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

    def noisy_params(self):
        self.__dict__['echo_params'] = True

    def silence_params(self):
        self.__dict__['echo_params'] = False

# Cell
class Lens(Help_system):
    class Raw_lens_data():
        def __init__(self):
            self.focal_length = 0*ureg.mm
            self.aperture = 0*ureg.Aperture
            self.focus_distance = 0 * ureg.meters



    @ureg.wraps(None,(None,'mm','Aperture','m'))
    def __init__(self, focal_length=40*ureg.mm, aperture=2.0*ureg.Aperture, focus_distance=4.0*ureg.meters):
        # system setup
        self.initialize_help_system()
        self.__dict__['class_preamble'] = self.__class__.__name__
        self.__dict__['pod_name'] = "lens_data"
        self.__dict__[self.pod_name] = self.Raw_lens_data()

        self.lens_data.focal_length = focal_length*ureg.mm
        self.lens_data.aperture = aperture*ureg.Aperture
        self.lens_data.focus_distance = focus_distance*ureg.meters

    @property
    @ureg.wraps('mm',(None))
    def focal_length(self):
        return self.lens_data.focal_length

    @focal_length.setter
    def focal_length(self,args):
        if isinstance(args,(int,float)):
            self.lens_data.focal_length = args*ureg.mm
            return
        try:
            if not (args.check('[length]')):
                raise Exception(f"die setter is not suitable quantity (mm) {args}")
            self.lens_data.focal_length = args
        except:
            raise Exception(f"die setter is not suitable quantity (mm) {args}")

    @property
    @ureg.wraps('Aperture',(None))
    def aperture(self):
        return self.lens_data.aperture

    @aperture.setter
    def aperture(self,inargs):
        if isinstance(inargs,(int,float)):
            self.lens_data.aperture = inargs*ureg.Aperture
            return
        if isinstance(inargs, ureg.Aperture):
            self.lens_data.aperture = inargs
        else:
            raise Exception(f"aperture is not suitable quantity (Aperture) {inargs}")

    @property
    @ureg.wraps('mm',(None))
    def focus_distance(self):
        return self.lens_data.focus_distance

    @focus_distance.setter
    def focus_distance(self, inargs):
        if isinstance(inargs,(int,float)):
            self.lens_data.focus_distance = inargs*ureg.m
            return
        try:
            if not (args.check('[length]')):
                raise Exception(f"focus_distance is not suitable quantity (m) {inargs}")
            self.lens_data.focus_distance = inargs
        except:
            raise Exception(f"focus_distance is not suitable quantity (m) {inargs}")



# Cell
class Sensor(Help_system):
    """
    class to hold sensor data and methods
    """
    class Raw_sensor_data:
        def __init__(self):
            self.die_size = (0,0)
            self.pixel_size = (0,0)
            self.diagonal = 0
            self.circle_of_confusion = 0
            self.circle_of_confusion_method = "Modern"
            self.pixel_count = (0,0)


    @ureg.wraps(None, (None, 'mm','mm','micrometer','micrometer'))
    def __init__(self, die_size_x,die_size_y, pixel_size_x,pixel_size_y):
        # system setup
        self.initialize_help_system()
        self.__dict__['class_preamble'] = self.__class__.__name__
        self.__dict__['pod_name'] = "sensor_data"
        self.sensor_data = self.Raw_sensor_data()
        #class variable setup
        self.sensor_data.die_size = (die_size_x*ureg.mm,   die_size_y*ureg.mm)
        self.sensor_data.diagonal = self.diagonal
        self.sensor_data.pixel_size = (pixel_size_x *ureg.micrometer,pixel_size_y * ureg.micrometer)
        self.sensor_data.circle_of_confusion_method = "Modern"
        self.calculate_circle_of_confusion()
        self.sensor_data.pixel_count = (( self.sensor_data.die_size[0]/self.sensor_data.pixel_size[0]) ,
                                          (self.sensor_data.die_size[1]/self.sensor_data.pixel_size[1]) )
        #self.print_sensor_properties()

    def print_sensor_properties(self):
        print(HTML(f"<span> pixel size cell ({self.sensor_data.pixel_size[0]},{self.sensor_data.pixel_size[1]}) </span>"))
        print(HTML(f"<span> pixel count ({self.sensor_data.pixel_count[0]},{self.sensor_data.pixel_count[1]}) </span>"))
        print(HTML(f"<span> die size ({self.sensor_data.die_size[0]},{self.sensor_data.die_size[1]}) </span>"))
        print(HTML(f"<span> Die Diagonal {self.sensor_data.diagonal} </span>"))
        print(HTML(f"<span> circle of confusion {self.sensor_data.circle_of_confusion} </span>"))
        print(HTML(f"<span> circle of confusion method {self.sensor_data.circle_of_confusion_method} </span>"))


    @property
    def die_size(self):
        """
        the size of the physical sensor
        """
        return self.sensor_data.die_size

    @die_size.setter
    def die_size(self,args):
        if len(args) > 2:
            raise Exception("die_size args should size 2, (x,y) ")
        in_x = args[0]
        in_y = args[1]
        try:
            if not (in_x.check('[length]') & in_y.check('[length]')):
                raise Exception(f"die setter is not suitable quantity (mm,mm) {in_x},{in_y}")
        except:
            raise Exception(f"die setter is not suitable quantity (mm,mm) {in_x},{in_y}")

        self.sensor_data.die_size = (in_x,in_y)


    @die_size.deleter
    def die_size(self):
        self.sensor_data.die_size = (None, None)
        self.sensor_data.diagonal = None

    @property
    @ureg.wraps('mm',(None))
    def diagonal(self):
        """
        The diagonal size of the sensor (re-calculated upon calling)
        """
        self.sensor_data.diagonal = math.sqrt( math.pow(self.sensor_data.die_size[0].magnitude,2)
                                              + math.pow(self.sensor_data.die_size[1].magnitude,2) )*ureg.mm
        return self.sensor_data.diagonal

    @diagonal.setter
    def diagonal(self,args):
        raise Exception("Diagonal is Read Only")

    @diagonal.deleter
    def diagonal(self):
        self.sensor_data.diagonal = None

    @property
    def pixel_size(self):
        return self.sensor_data.pixel_size

    @pixel_size.setter
    def pixel_size(self, args):
        if len(args) > 2:
            raise Exception("pixel_size args should size 2, (x,y) ")
        in_x = args[0]
        in_y = args[1]
        try:
            if not (in_x.check('[length]') & in_y.check('[length]')):
                raise Exception(f"die setter is not suitable quantity (um,um) {in_x},{in_y}")
        except:
            raise Exception(f"die setter is not suitable quantity (um,um) {in_x},{in_y}")

        self.sensor_data.pixel_size = (in_x,in_y)


    @pixel_size.deleter
    def pixel_size(self):
        self.sensor_data.pixel_size = (None,None)
        self.sensor_data.circle_of_confusion = None

    @property
    def pixel_count(self):
        return self.sensor_data.pixel_count

    @pixel_count.setter
    def pixel_count(self, inargs):
        if not len(inargs) == 2:
            raise Exception(f" pixel count expects a tuple (x,y) not {inargs}")
        self.sensor_data.pixel_count = inargs

    @property
    def circle_of_confusion_method(self):
        return self.sensor_data.circle_of_confusion_method

    @circle_of_confusion_method.setter
    def circle_of_confusion_method(self, in_args ):
        #method="modern",*args, **kwargs):
        if isinstance(in_args,str):
            method = in_args
        elif len(in_args) == 2:
            method = in_args[0]
            focus_object = in_args[1]
        else:
            raise LookupError(f"Too many arguments in the supplied arguments [{len(in_args)}] {in_args}")

        coc_method = [ "modern", "zeiss","kodak", "archaic" ]
        if method not in coc_method:
            raise ValueError(f"Circle of confusion method not supported [{method}]")
        self.sensor_data.circle_of_confusion_method = method


        if method == "kodak":
            self.calculate_circle_of_confusion(focus_object)
        else:
            self.calculate_circle_of_confusion()


    @circle_of_confusion_method.deleter
    def circle_of_confusion_method(self):
        self.sensor_data.circle_of_confusion_method = "modern"
        self.sensor_data.circle_of_confusion = None


    def circle_of_confusion_help(self)->None:
        print(HTML("<H2>Circle of Confusion</H2>"))
        print(HTML("Modern, Standard Method (Default)	Frame???s diagonal / 1500"))
        print(HTML("Zeiss, Formula	Frame???s diagonal / 1730"))
        print(HTML("Kodak, Formula	Focal length / 1720"))
        print(HTML("Archaic, Standard	Frame???s diagonal / 1000"))
        print(HTML("<code> circle_confusion(frame_diagonal,focal_length,method = 'modern')</code>"))
        return 1

    @property
    def circle_of_confusion(self):
        if (self.sensor_data.circle_of_confusion is None):
            raise Exception(f" Circle of confusion has not been calculated yet")

        return self.sensor_data.circle_of_confusion


    @dispatch( ureg.Quantity )
    def calculate_circle_of_confusion(self, inarg):
        #ok we have been given a lens length
        if self.sensor_data.circle_of_confusion_method.lower() != "kodak":
            raise Exception("Given a lens length, but circle of confusion method is not kodak")
        self.__calculate_circle_of_confusion(inarg)

    @dispatch( Lens )
    def calculate_circle_of_confusion(self, inarg):
        self.__calculate_circle_of_confusion(inarg)

    @dispatch()
    def calculate_circle_of_confusion(self):
        self.__calculate_circle_of_confusion(0*ureg.mm)

    def __calculate_circle_of_confusion(self, inarg):

        def modern(frame_diagonal, ignore):
            return frame_diagonal/1500
        def zeiss(frame_diagonal, ignore):
            return frame_diagonal/1730
        def kodak(ignore, focal_length):
            return focal_length/1720
        def archaic(frame_diagonal, ignore):
            return frame_diagonal/1000

        coc_method = { "modern": modern,
                      "zeiss": zeiss,
                      "kodak": kodak,
                      "archaic": archaic}
        focal_length = 0
        if isinstance(inarg,Lens):
            focal_length = inarg.focal_length
        elif(self.sensor_data.circle_of_confusion_method.lower() == 'kodak' ):
            try:
                if not (inarg.check('[length]')):
                    raise Exception(f"focal length is not suitable quantity (mm) {inarg}")
            except:
                raise Exception(f"focal length is not suitable quantity (mm) {inarg}")
            #ok looks like we can use this as a focal length
            focal_length = in_arg

        if self.sensor_data.circle_of_confusion_method.lower() not in coc_method:
            raise ValueError(f"Unknown Circle of Confusion Method {method}")

        #if focal_length
        coc = coc_method.get(self.sensor_data.circle_of_confusion_method.lower())(self.sensor_data.diagonal,focal_length)
        self.sensor_data.circle_of_confusion = (coc.magnitude) * ureg['mm']

    @circle_of_confusion.deleter
    def circle_of_confusion(self):
        self.sensor_data.circle_of_confusion = None

    def set_exact_die_size_from_resolution_and_cell_size_help(self):
        print(HTML("<h2>set_exact_die_size_from_resolution_and_cell_size</h2>"))
        print(HTML("<pre>recaluculates the exect sensor surface area based on pixel dimensions and the cell size</pre>"))
        print(HTML("<span> this is useful when you only know the approximate size of the die, and not exact</span>"))

    def set_exact_die_size_from_resolution_and_cell_size(self):
        print(HTML(f"<span> using pixel size cell ({self.sensor_data.pixel_size[0]},{self.sensor_data.pixel_size[1]}) </span>"))
        self.sensor_data.die_size = ( self.sensor_data.pixel_count[0]* self.sensor_data.pixel_size[0].to_base_units(),
                                      self.sensor_data.pixel_count[1]* self.sensor_data.pixel_size[1].to_base_units() )
        print(HTML(f"<span> set die size to ({self.sensor_data.die_size[0]},{self.sensor_data.die_size[1]}) </span>"))
        print()


# Cell
class Camera(Help_system):
    class Camera_data:
        def __init__(self):
            self.angle_of_view = (None,None)
            self.field_of_view = (None,None)

    def __init__(self, sensor: Sensor, lens: Lens):
        # system setup
        self.initialize_help_system()
        self.__dict__['class_preamble'] = self.__class__.__name__
        self.__dict__['pod_name'] = "camera_data"
        self.camera_data = self.Camera_data()

        self.sensor = sensor
        self.lens = lens

    def replace_lens(self, inlens: Lens):
        if not isinstance(inlens, Lens):
            raise Exception(f" passed object is not a lens")
        self.lens = inlens

    def replace_senspr(self, insensor: Sensor):
        if not isinstance(insensor, Sensor):
            raise Exception(f" passed object is not a sensor")
        self.sensor = insensor

    def angle_of_view_help(self):
        print(HTML("<h2>Angle of view</h2>"))
        print(HTML("<span>Figures out the witdh of the angle of view, given sensor / lens characteristics.</span>"))
        print(self.wrap_unit(r"\theta=2\cdot\arctan\left(\frac{h(s-f)}{2sf}\right)","math"))
        print(HTML("<code> angle_of_view(frame_dimension, focal_length, focus_distance)</code>"))

    @ureg.wraps(('radians','radians'),(None))
    def angle_of_view(self):
        aov_x = 2.0 * math.atan(((self.sensor.die_size[0] * (self.lens.focus_distance - self.lens.focal_length)) /
                                 (2*self.lens.focus_distance*self.lens.focal_length)))
        aov_y = 2.0 * math.atan(((self.sensor.die_size[1] * (self.lens.focus_distance - self.lens.focal_length)) /
                                 (2*self.lens.focus_distance*self.lens.focal_length)))
        self.camera_data.angle_of_view = (aov_x * ureg.radians ,aov_y * ureg.radians)
        return self.camera_data.angle_of_view

    def field_of_view_help(self):
        print(self.wrap_unit("<h2>Field of View</h2>","html"))
        print(self.wrap_unit("<a> implementation of this equation </a>","html"))
        print(self.wrap_unit(r'w=2s\cdot\tan\left(\frac{\theta}{2}\right)',"Math"))

    @ureg.wraps(('m','m'),(None))
    def field_of_view(self):
        if self.camera_data.angle_of_view[0] is None:
            self.angle_of_view()
        view_width_x = 2*self.lens.focus_distance*math.tan( self.camera_data.angle_of_view[0] / 2.0)
        view_width_y = 2*self.lens.focus_distance*math.tan( self.camera_data.angle_of_view[1] / 2.0)
        print(f" field of view : {view_width_x},{view_width_y}")
        self.camera_data.field_of_view = (view_width_x, view_width_y)
        return self.camera_data.field_of_view

    def hyperfocal_distance_help(self):
        print(HTML("<H2>Hyperfocal Distance</H2>"))
        print(HTML("<span> calculates hyperfocal distance"))
        print(self.wrap_unit(r"H=\frac{f^{2}}{N\cdot{c}}+f","Math"))

    @ureg.wraps(ureg.meters, (None))
    def hyperfocal_distance(self):
        # aperture for us is unitless but really is should be in 1/m
        # TODO fix aperture to be correct units
        bottom = (1/(self.lens.aperture.magnitude*self.sensor.circle_of_confusion.magnitude))
        hfd = (pow(self.lens.focal_length.magnitude,2)/(bottom)+self.lens.focal_length.magnitude)
        return hfd*ureg('m')

    def near_DOF_limit_help(self):
        print(HTML("<H2>Near Depth of Field</H2>"))
        print(self.wrap_unit(r"D_{n}=\frac{s(H-f)}{H+s-2f}","Math"))

    @ureg.wraps(ureg.meters,(None))
    def near_DOF_limit(self):
        top = self.lens.focus_distance*(self.hyperfocal_distance() -self.lens.focal_length)
        bottom = self.hyperfocal_distance() + self.lens.focus_distance - 2*self.lens.focal_length
        return top/bottom

    def far_DOF_limit_help(self):
        print(HTML("<H2>Far Depth of Field</H2>"))
        print(self.wrap_unit(r"D_{f}=\frac{s(H-f)}{H-s}","Math"))

    @ureg.wraps(ureg.meters,(None))
    def far_DOF_limit(self):
        top = self.lens.focus_distance*(self.hyperfocal_distance() -self.lens.focal_length)
        bottom = self.hyperfocal_distance() - self.lens.focus_distance
        return top/bottom

    def DOF_help(self):
        print(HTML("<H2>Depth of Field</H2>"))
        print(self.wrap_unit(r"DOF = Far Limit - Near Limt","Math"))

    @ureg.wraps(ureg.meters,(None))
    def DOF(self):
        return self.far_DOF_limit() - self.near_DOF_limit()

    def GSD_help(self):
        print(HTML("<H2>GSD, Geospatial Sampling Distance</H2>"))
        print(self.wrap_unit(r"GSD=\frac{Field\ of\ View}{Number\ of\ Pixels}","Math"))

    @ureg.wraps((ureg.mm, ureg.mm), (None))
    def GSD(self):
        self.field_of_view()
        gsd_x = self.camera_data.field_of_view[0] / self.sensor.pixel_count[0]
        gsd_y = self.camera_data.field_of_view[1] / self.sensor.pixel_count[1]
        return (gsd_x,gsd_y)

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