pysndfile intro
===================

pysndfile is a python package providing *PySndfile*, a
`Cython <http://cython.org/>`__ wrapper class around
`libsndfile <http://www.mega-nerd.com/libsndfile/>`__. PySndfile
provides methods for reading and writing a large variety of soundfile
formats on a variety of plattforms. PySndfile provides a rather complete
access to the different sound file manipulation options that are
available in libsndfile.

Due to the use of libsndfile nearly all sound file formats, (besides mp3
and derived formats) can be read and written with PySndfile.

The interface has been designed such that a rather large subset of the
functionality of libsndfile can be used, notably the reading and writing
of strings into soundfile formats that support these, and a number of
sf\_commands that allow to control the way libsndfile reads and writes
the samples. One of the most important ones is the use of the clipping
command.

Transparent soundfile io with libsndfile
----------------------------------------

PySndfile has been developed in the `analysis synthesis team at
IRCAM <http://anasynth.ircam.fr/home/english>`__ mainly for research on
sound analysis and sound transformation. In this context it is essential
that the reading and writing of soundfile data is transparent.

The use of the clipping mode of libsndfile is important here because
reading and writing sound data should not change the audio samples. By
default, when clipping is off, libsndfile uses slightly different
scaling factors when reading pcm format into float samples, or when
writing float samples into pcm format. Therefore whenever a complete
read/write cycle is applied to a sound file then the audio samples may
be modified even when no processing is applied.

More precisely this will happen if

-  the sound files contains pcm format,
-  *and* the data is read into float or double,
-  *and* the audio data comes close to the maximum range such that the
   difference in scaling leads to modification.

To avoid this problem PySndfile sets clipping by default to on. If you
don't like this you can set it to off individually using the PySndfile
method set\_auto\_clipping(False).

Implementation
--------------

The implementation is based on a slightly modified version of the header
sndfile.hh that is distributed with libsndfile. The only modification is
the addition of a methode querying the seekable state of the open
Sndfile.

Installation
------------

via Anaconda channel roebel
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Precompiled packages are available for `Anaconda
python3 <https://anaconda.org/roebel/pysndfile>`__ under Linux (x86\_64)
and Mac OS X (> 10.9). For these systems you can install pysndfile
simply by means of

.. code:: bash

    conda install -c roebel pysndfile

Unfortunately, I don't have a windows machine and therefore I cannot
provide any packages for Windows.

compile with conda build recipe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the conda recipe
`here <https://github.com/roebel/conda_packages>`__. This build recipe
wil automatically download and compile libsndfile building pysndfile.

compile from sources
~~~~~~~~~~~~~~~~~~~~

In case you want to manually compile pysndfile requires availability of
libsndfile http://www.mega-nerd.com/libsndfile/.

If the libsndfile (header and library) is not installed in the default
compiler search path you have to specify the library and include
directories to be added to this search paths. For this you can use
either the command line options --sndfile-libdir and --sndfile-incdir
that are available for the build\_ext command or specify these two
parameters in the setup.cfg file.

Besides this the setup is pretty standard. Note, that the cython source
\_pysndfile.pyx will be compiled with cython only if cython is
installed.

Documentation
-------------

Please see full documentation
`here <https://pysndfile.readthedocs.io/>`__

