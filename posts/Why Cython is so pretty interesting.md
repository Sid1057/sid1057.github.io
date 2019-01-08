
## Let's speak ~~from my heart~~ about cython

#### *Sorry, this article will be done later*

And science we are developers, we will use code right here.

I don't want to do boring things later. So I include numpy, cython compiler in IPython and small package for profiling parts of code.


```python
%load_ext autotime
```


```python
import numpy as np
```

    time: 132 ms



```python
%load_ext cython
%load_ext autotime
```

    The autotime extension is already loaded. To reload it, use:
      %reload_ext autotime
    time: 342 ms



```python
sections = 1000000
```

    time: 1.18 ms


I would like to do this topic as short and informative as possible. And the format which i choose - to show 5 most obviously reasons for using cython in your projects right now.

## 5 reasons to use cython instead python

### 1: for using cython you could stay code as it exist

We define to python functions: some f(x) and integrator. Each reason will modificate this code. Every next reason for using cython will change your code more, but also it would have better effect.


```python
def f(x):
    return x**2-x

def integrate_f(a, b, N):
    s = 0
    dx = (b-a)/N
    for i in range(N):
        s += f(a + dx * i)
    return s * dx
    
```

    time: 3.35 ms


Important note: initialization of python function (at least in jupyter notebook) faster then cython function. But it's only initialization!


```python
integrate_f(0, 10, sections)
```




    283.3328833334909



    time: 337 ms


That's time for python function to calculate integral of f(x) on [0, 10] with 10 million sections.


```cython
%%cython

def f_cython(x):
    return x**2-x

def integrate_f_cython(a, b, N):
    s = 0
    dx = (b-a)/N
    for i in range(N):
        s += f_cython(a + dx * i)
    return s * dx
```

    time: 16.7 ms



```python
integrate_f_cython(0, 10, sections)
```




    283.3328833334909



    time: 240 ms


#### Total:

So in my notebook I have speed ~ x1.33 without any changes in my code. Probably, it's my favorite thing in Cython. Nobody require some actions from you: just replace python on cython. Just use %%cython in your jupyter or add setup file to compile your code in object module.

### 2: you could use fast types conversion

What if i want to do requirement for my function: numbers in interval have to be integer.


```python
integrate_f(0, 10.1, sections)
```




    292.42820252133953



    time: 328 ms


It's a bad behaviour for my requirement. I have to change my integrate_f function:


```python
def integrate_f_ver2(a, b, N):
    a, b = int(a), int(b)
    
    s = 0
    dx = (b-a)/N
    for i in range(N):
        s += f(a + dx * i)
    return s * dx
    
```

    time: 4.98 ms



```python
print(integrate_f(0, 10.1, sections))
print(integrate_f_ver2(0, 10.1, sections))
```

    292.42820252133953
    283.3328833334909
    time: 623 ms


Works pretty, but how to do this in cython?


```cython
%%cython

def f_cython(x):
    return x**2-x

def integrate_f_cython_ver2(int a, int b, N):
    s = 0
    dx = (b-a)/N
    for i in range(N):
        s += f_cython(a + dx * i)
    return s * dx
```

    time: 11 ms



```python
print(integrate_f_cython(0, 10.1, sections))
print(integrate_f_cython_ver2(0, 10.1, sections))
```

    292.42820252133953
    283.3328833334909
    time: 484 ms


#### Total:

### 3: you could make your code faster very well

Let's add some C stuff in Cython:


```cython
%%cython


cdef float f_cython(x):
    return x**2-x

cpdef float integrate_f_cython_ver3(int a, int b, int N):
    cdef float s = 0
    cdef float dx = (b-a)/N
    cdef int i 
    
    for i in range(N):
        s += f_cython(a + dx * i)
    return s * dx
```

    time: 421 ms



```python
integrate_f_ver2(0, 10.1, sections)
```




    283.3328833334909



    time: 340 ms



```python
integrate_f_cython_ver2(0, 10.1, sections)
```




    283.3328833334909



    time: 233 ms



```python
integrate_f_cython_ver3(0, 10.1, sections)
```




    283.33111572265625



    time: 97 ms


#### Total:

### 3: you could use functions from C and C++ which haven't bindings to python

For me it was CUDA functions in OpenCV

### 5: you can use a simple mechanism to do effective multithreading behaviour

## Conclusion



## Recommendations for reading:

## P.S.:


```python
!pip3 freeze
```

    absl-py==0.2.2
    apturl==0.5.2
    astor==0.7.1
    astroid==2.0.4
    backcall==0.1.0
    beautifulsoup4==4.4.1
    bleach==3.0.2
    Brlapi==0.6.4
    chardet==2.3.0
    command-not-found==0.3
    cycler==0.9.0
    Cython==0.23.4
    decorator==4.0.6
    defer==1.0.6
    defusedxml==0.5.0
    docutils==0.12
    entrypoints==0.2.3
    flake8==3.5.0
    gast==0.2.0
    grpcio==1.13.0
    h5py==2.7.1
    html5lib==0.999
    ipykernel==5.1.0
    ipython==2.4.1
    ipython-genutils==0.2.0
    ipywidgets==7.4.2
    isort==4.3.4
    jedi==0.13.1
    Jinja2==2.10
    jsonschema==2.6.0
    jupyter==1.0.0
    jupyter-client==5.2.3
    jupyter-console==6.0.0
    jupyter-core==4.4.0
    Keras==2.1.3
    language-selector==0.1
    lazy-object-proxy==1.3.1
    lightdm-gtk-greeter-settings==1.2.1
    louis==2.6.4
    lxml==3.5.0
    Mako==1.0.3
    Markdown==2.6.6
    Markups==1.0.1
    MarkupSafe==0.23
    mate-tweak==3.5.10
    matplotlib==1.5.1
    mccabe==0.6.1
    mgen==1.2.0
    mistune==0.8.4
    moderngl==5.4.2
    mpmath==0.19
    nbconvert==5.4.0
    nbformat==4.4.0
    notebook==5.7.0
    numexpr==2.4.3
    numpy==1.11.0
    onboard==1.2.0
    pandas==0.17.1
    pandocfilters==1.4.2
    parso==0.3.1
    pbr==5.1.1
    pep8==1.7.0
    pexpect==4.0.1
    pickleshare==0.7.5
    pilkit==1.1.13
    Pillow==3.1.2
    polib==1.0.7
    prometheus-client==0.4.2
    prompt-toolkit==2.0.7
    protobuf==3.6.0
    psutil==3.4.2
    ptyprocess==0.5
    pycodestyle==2.3.1
    pycups==1.9.73
    pycurl==7.43.0
    pyenchant==1.6.6
    pyflakes==1.6.0
    Pygments==2.1
    pygobject==3.20.0
    pygpu==0.7.5+11.g04c2892
    PyICU==1.9.2
    pylint==2.1.1
    pyparsing==2.0.3
    python-apt==1.1.0b1+ubuntu0.16.4.1
    python-dateutil==2.4.2
    python-debian==0.1.27
    python-systemd==231
    pytz==2014.10
    pyxdg==0.25
    PyYAML==3.11
    pyzmq==17.1.2
    qtconsole==4.4.2
    reportlab==3.3.0
    requests==2.9.1
    roman==2.0.0
    scapy==2.4.0
    scikit-learn==0.19.1
    scipy==0.17.0
    screen-resolution-extra==0.0.0
    Send2Trash==1.5.0
    sessioninstaller==0.0.0
    simplegeneric==0.8.1
    six==1.10.0
    sympy==0.7.6.1
    tables==3.2.2
    tensorboard==1.9.0
    tensorflow==1.9.0
    tensorflow-gpu==1.9.0
    termcolor==1.1.0
    terminado==0.8.1
    testpath==0.4.2
    textile==2.2.2
    Theano==1.0.1+36.g91f71fc
    tornado==5.1.1
    traitlets==4.3.2
    typed-ast==1.1.0
    ubuntu-drivers-common==0.0.0
    ufw==0.35
    unattended-upgrades==0.1
    urllib3==1.13.1
    usb-creator==0.3.0
    virtualenv==16.0.0
    wcwidth==0.1.7
    webencodings==0.5.1
    Werkzeug==0.14.1
    widgetsnbextension==3.4.2
    wrapt==1.10.11
    xkit==0.0.0
    [33mYou are using pip version 8.1.1, however version 18.1 is available.
    You should consider upgrading via the 'pip install --upgrade pip' command.[0m
    time: 1.05 s



```python

```
