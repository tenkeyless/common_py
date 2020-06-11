sphinx-apidoc -o doc/source common_py/ --separate --ext-coverage -f
cd doc
make html
cd ..
doc2dash -n common_py -f -i doc/dash_icon.png -A doc/build/html/
