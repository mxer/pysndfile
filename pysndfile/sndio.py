"""
sndio is a simple interface for reading and writing arbitrary sound files.
The module contains 3 functions.

|  **functions:**
|     :meth:`pysndfile.sndio.get_info`:: retrieve information from a sound file.
|     :meth:`pysndfile.sndio.read`:: read data and meta data from sound file.
|     :meth:`pysndfile.sndio.write`:: create a sound file from a given numpy array.
"""

#
# Copyright (C) 2014 IRCAM
#
# All rights reserved.
#
# This file is part of pysndfile.
#
# pysndfile is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pysndfile is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pysndfile.  If not, see <http://www.gnu.org/licenses/>.
#


from pysndfile import PySndfile, construct_format
import numpy as np

def get_info(name, extended_info=False) :
    """
    retrieve information from a sound file

    :param name: <str> sndfile name
    :param extended_info: <bool>

    :return: 3 or 5 tuple with meta information read from the soundfile
       in case extended_info is False a 3-tuple comprising samplerate, encoding (str), major format  is returned
       in case extended_info is True a 5-tuple comprising additionally the number of frames and the number of channels
       is returned.
    """
    sf  = PySndfile(name)
    if extended_info:
        return sf.samplerate(), sf.encoding_str(), sf.major_format_str(), sf.frames(), sf.channels()
    return sf.samplerate(), sf.encoding_str(), sf.major_format_str()

def write(name, data, rate=44100, format="aiff", enc='pcm16', sf_strings=None) :
    """
    Write datavector to sndfile using samplerate, format and encoding as specified
    valid format strings are all the keys in the dict pysndfile.fileformat_name_to_id
    valid encodings are those that are supported by the selected format
    from the list of keys in pysndfile.encoding_name_to_id.

    :param name: sndfile name
    :param data: array containing sound data. For mono files an 1d array can be given, for multi channel sound files
                sound frames are in the rows and data channels in the columns.
    :param rate: sample rate (int) default s to 44100
    :param format: sndfile major format (str) default=aiff
    :param enc: sndfile encoding (str) default=pcm16

    :return: <int> number of sample frames written.
    """
    nchans = len(data.shape)
    if nchans == 2 :
        nchans = data.shape[1]
    elif nchans != 1:
        raise RuntimeError("error:sndio.write:can only be called with vectors or matrices ")

    sf  = PySndfile(name, "w",
                    format=construct_format(format, enc),
                    channels = nchans, samplerate = rate)

    if sf_strings is not None:
        sf.set_strings(sf_strings)
    nf = sf.write_frames(data)

    if nf != data.shape[0]:
        raise IOError("sndio.write::error::writing of samples failed")
    return nf

enc_norm_map = {
    "pcm8" : np.float64(2**7),
    "pcm16": np.float64(2**15),
    "pcm24": np.float64(2**23),
    "pcm32": np.float64(2**31),
    }
    
def read(name, end=None, start=0, dtype=np.float64, return_format=False, sf_strings=None) :
    """
    read samples from arbitrary sound files. May return subsets of samples as specified by start and end arguments (Def all samples)
    normalizes samples to [-1,1] if the datatype is a floating point type

    *Parameters*

    :param name: (str) sndfile name
    :param end: (int) last sample frame to read default=None -> read all samples
    :param start: (int) first sample frame to read default=0
    :param dtype: (numpy.dtype) data type of the numpy array that will be returned.
    :param return_format: (bool) if set then the return tuple will contain an additional element containing the sound file major format
    :param sf_strings: (None,dict) if a dict is given the dict elements will be set to the strings that are available in the
         sound file.

    :return: 3 or 4 -tuple containing
        data (1d for mon sounds 2d for multi channel sounds, where channels are in the columns),
        samplerate (int) and encoding (str),
        in case return_format is True then the next element contains the major
        format of the sound file (can be used to recreate a sound file with an identical format).
    """
    sf  = PySndfile(name)
    enc = sf.encoding_str()

    nf = sf.seek(start, 0)
    if not nf == start:
        raise IOError("sndio.read::error:: while seeking at starting position")
    
    if end == None:
        ff = sf.read_frames(dtype=dtype)
    else:
        ff = sf.read_frames(end-start, dtype=dtype)

    if isinstance(sf_strings, dict):
        sf_strings.clear()
        sf_strings.update(sf.get_strings())

    # if norm and (enc not in ["float32" , "float64"]) :
    #     if enc in enc_norm_map :
    #         ff = ff / enc_norm_map[sf.encoding_str()]
    #     else :
    #         raise IOError("sndio.read::error::normalization of compressed pcm data is not supported")

    if return_format:
        return ff, sf.samplerate(), enc, sf.major_format_str()
    return ff, sf.samplerate(), enc
