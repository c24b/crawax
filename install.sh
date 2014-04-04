#!/bin/bash
#Downloading virtualenv

#Create a new virtualenv in the current directory
virtualenv $PWD --no-site-packages -p /usr/bin/python2.7

# First, locate the root of the current virtualenv
while [ "$PWD" != "/" ]; do
    # Stop here if this the root of a virtualenv
    if [ \
        -x bin/python \
        -a -e lib/python*/site.py \
        -a -e include/python*/Python.h ]
    then
        break
    fi
    cd ..
done
if [ "$PWD" = "/" ]; then
    echo "Could not activate: no virtual environment found." >&2
    exit 1
fi

# Then Activate
export VIRTUAL_ENV="$PWD"
export PATH="$VIRTUAL_ENV/bin:$PATH"
#Specific installations for crawtext
pip install -r "$VIRTUAL_ENV/requirements.txt"
# Some problems observed with the pip version of lxml
easy_install lxml
#Installing python-goose from github
git clone https://github.com/grangier/python-goose.git
cd python-goose
python setup.py install
cd ..


#execute the first program as demo
$VIRTUAL_ENV/bin/python crawtext.py -h
#Desactivate
unset PYTHON_HOME
exec "${@:-$SHELL}"
echo "Virtual env installation successfull. Please run source/bin activate BEFORE running the crawtext script"