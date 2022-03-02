"""This module allows you to filter sensor data using various linear and non-linear filtering techniques.
"""

from math import pi 
# we use pi for calculation
# of alpha from cutoff frequency

# we use a deque in the median filter
from collections import deque


class HighPassFilter:
    """  A class to perform simple first order high pass filtering on a sensor value
    """
    def __init__(self,alpha):
        """ Create a high pass filter object with a given alpha. 

        You may want to calculate alpha based on cutoff frequency 
        or time constant, in that case, you can use the static methods
        `make_from_cutoff` and `make_from_time_constant` to make the filter
        instead of using the constructor.

        Parameters
        ----------
        alpha : float
            The filter constant alpha

        Returns
        -------
        filter: HighPassFilter
            A high pass filter object

        """
        self.last_input=None
        self.last_output=None
        self.alpha=alpha


    def on_value(self,value_in):
        """Process a new value with this filter object and return the output value
        
        Parameters
        ----------
        value_in:float
            Input value to filter

        Returns
        -------
        filtered_value:float
            Filter output value
        """
        # if we haven't seen any value yet,
        # set this as our filter output        
        if self.last_input==None:
            self.last_input=value_in
            self.last_output=0
        # this is the actual filter calculation
        self.last_output=self.alpha * (self.last_output + value_in - self.last_input)
        self.last_input=value_in
        return self.last_output

    # a couple of handy static methods to create
    # filters based on time constant or cutoff frequency
    @staticmethod
    def make_from_cutoff(cutoff_frequency,time_between_samples):
        ''' Make a high-pass filter with this cutoff frequency.
        Parameters
        ----------
        cutoff_frequency: float
            Cutoff frequency in HZ
        time_between_samples: float
            seconds between samples

        Returns
        -------
        filter: HighPassFilter
            High-pass filter object
        '''
        fc=cutoff_frequency*time_between_samples*2*pi
        alpha=1/(fc+1)
        return HighPassFilter(alpha)

    @staticmethod
    def make_from_time_constant(time_constant,time_between_samples):
        ''' Make a high-pass filter with a particular time constant

        Parameters
        ----------
        time_constant: float
            Time constant in seconds
        time_between_samples: float
            Seconds between samples

        Returns
        -------
        filter:HighPassFilter
            High-pass filter object
        '''
        alpha=(time_constant)/(time_constant+time_between_samples)
        return HighPassFilter(alpha)

class LowPassFilter:
    """ A class to perform simple first order lowpass filtering on a sensor value"""
    def __init__(self,alpha):
        """ Create a low pass filter object with a given alpha. 

        You may want to calculate alpha based on cutoff frequency 
        or time constant, in that case, you can use the static methods
        `make_from_cutoff` and `make_from_time_constant` to make the filter
        instead of using the constructor.

        Parameters
        ----------
        alpha : float
            The filter constant alpha

        Returns
        -------
        filter: LowPassFilter
            A low pass filter object
        """

        self.last_value=None
        self.alpha=alpha


    def on_value(self,value_in):
        """
            Process a new value with this filter object and return the output value
            
            Parameters
            ----------
            value_in:float
                Input value to filter

            Returns
            -------
            filtered_value:float
                Filter output value
        """
        # if we haven't seen any value yet,
        # set this as our filter output        
        if self.last_value==None:
            self.last_value=value_in
        # this is the actual filter calculation
        self.last_value=self.alpha * value_in + (1-self.alpha)*self.last_value
        return self.last_value

    # a couple of handy static methods to create
    # filters based on time constant or cutoff frequency
    @staticmethod
    def make_from_cutoff(cutoff_frequency,time_between_samples):
        ''' Make a low-pass filter with this cutoff frequency .

            Parameters
            ----------
            cutoff_frequency: float
                Cutoff frequency in HZ
            time_between_samples: float
                Seconds between samples

            Returns
            -------
            filter:LowPassFilter
                Low-pass filter object
        '''
        fc=cutoff_frequency*time_between_samples*2*pi
        alpha=fc/(fc+1)
        return LowPassFilter(alpha)

    @staticmethod
    def make_from_time_constant(time_constant,time_between_samples):
        ''' Make a low-pass filter with a particular time constant.

        Parameters
        ----------
        time_constant: float
            Time constant in seconds
        time_between_samples: float
            Seconds between samples

        Returns
        -------
        filter:LowPassFilter
            Low-pass filter object
        '''
        alpha=(time_between_samples)/(time_constant+time_between_samples)
        return LowPassFilter(alpha)

class MedianFilter:
    '''A class to perform median filtering on a sensor value

    '''

    def __init__(self,block_size):
        """ Create a median filter object with a given block size

        Parameters
        ----------
        block_size : int
            The number of previous samples that we take a median over

        """
        self.history=deque(maxlen=block_size)

    def on_value(self,new_value):        
        """Process a new value with this filter object and return the output value
        
        Parameters
        ----------
        value_in:float
            Input value to filter

        Returns
        -------
        filtered_value:float
            Median of current sliding buffer
        """
        self.history.append(new_value)
        ordered=sorted(self.history)
        orderedPos=int(len(ordered)/2)        
        return ordered[orderedPos]

class SlidingAverageFilter:
    '''
    A class to perform a sliding average (mean)
    on a sensor value

    '''

    def __init__(self,block_size):
        """ Create a sliding average object with a given block size

        Parameters
        ----------
        block_size : int
            The number of previous samples that we sliding average over

        """
        self.history=deque(maxlen=block_size)

    def on_value(self,new_value):        
        """Process a new value with this filter object and return the output value
        
        Parameters
        ----------
        value_in:float
            Input value to filter

        Returns
        -------
        filtered_value:float
            Mean of current sliding average buffer
        """
        self.history.append(new_value)
        mean = sum(self.history)/len(self.history)
        return mean

class BlockMeanFilter:
    '''
    A class to perform a mean (average) on blocks of sensor data

    Sensor values are only output once per block_size input samples.
    '''

    def __init__(self,block_size):
        self.history=[]
        self.block_size=block_size

    def on_value(self,new_value):        
        """
            Process a new value with this filter object and return the output value
            
            Parameters
            ----------
            value_in:float
                Input value to filter

            Returns
            -------
            filtered_value:float
                Mean of the current block, or None if we are mid-block
        """
        self.history.append(new_value)
        if len(self.history)==self.block_size:
            output=sum(self.history)/len(self.history)
            self.history=[]
            return output
        return None

class BlockMedianFilter:
    '''
    A class to perform a median over blocks of sensor values.

    Sensor values are only output once per block_size input samples.

    '''

    def __init__(self,block_size):
        self.history=[]
        self.block_size=block_size

    def on_value(self,new_value):        
        """
            Process a new value with this filter object and return the output value
            
            Parameters
            ----------
            value_in:float
                Input value to filter

            Returns
            -------
            filtered_value:float or None
                Median of the current block, or None if we are mid block
        """
        self.history.append(new_value)
        if len(self.history)==self.block_size:
            self.history.sort()
            output=self.history[len(self.history)//2]
            self.history=[]
            return output
        return None

class BlockMaxFilter:
    '''
    A class to perform a maximum on blocks of data

    Sensor values are only output once per block_size input samples.

    '''

    def __init__(self,block_size):
        self.history=[]
        self.block_size=block_size

    def on_value(self,new_value):        
        """
            Process a new value with this filter object and return the output value
            
            Parameters
            ----------
            value_in:float
                Input value to filter

            Returns
            -------
            filtered_value:float
                Maximum of this block, or None if mid block
        """
        self.history.append(new_value)
        if len(self.history)==self.block_size:
            output=max(self.history)
            self.history=[]
            return output
        return None

class BlockMinFilter:
    '''
    A class to perform a minimum on blocks of data

    Sensor values are only output once per block_size input samples.
    '''

    def __init__(self,block_size):
        self.history=[]
        self.block_size=block_size

    def on_value(self,new_value):        
        """ Process a new value with this filter object and return the output value
            
            Parameters
            ----------
            value_in:float
                Input value to filter

            Returns
            -------
            filtered_value:float or None
                Minimum of this block, or None if mid block
        """
        self.history.append(new_value)
        if len(self.history)==self.block_size:
            output=min(self.history)
            self.history=[]
            return output
        return None



