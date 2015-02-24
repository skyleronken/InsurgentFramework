# Insurgent Framework
A framework for creating modular malware/bots to be used in training environments. Please take a look at the Wiki for usage details and development guidelines.

<h4>Priorites</h4>
<ol>
<li>Modularity</li>
<li>Capability</li>
<li>Compatability</li>
<li>Portability</li>
<li>Forensically Sound</li>
</ol>

<h5>
Dependencies
</h5>

<ul>
<li>Python 2.7</li>
<li>Pyinstaller</li>
<li>Bottle</li>
</ul>

Other dependencies will be required by specific modules

<h6>Notes: </h6>
I had to modify pyinstaller to get it to recursively analyze dynamically imported modules' dependencies.<br><br>
If not building pyinstaller from their Git repo, make sure you make the change manually: <br>
https://github.com/pyinstaller/pyinstaller/commit/e9575e1145718ecc49625b782cee7cbb41d8522b

<h4>
Installation
</h4>
<p>
Unzip the contents of the package wherever you would like to run it from.<br><br>
pip install pyinstaller<br>
pip install bottle<br>
(Other recommended dependencies)<br>
pip install scapy

</p>

<h4>
Usage
</h4>

<h5>Build.py</h5>
python build.py -h

<h5>Translator.py</h5>
python translator.py -h

<h5>Base.py</h5>
It is not recommended to use base.py for testing purposes because most errors are likely to occur within the importing.
However, if you are trying to test the module and don't want to worry about resolving pyinstaller import errors, you can
run 'base.py'. Just make sure you settings.xml file is present in the root directory of the framework and has the same
name as config.DEFAULT_CONFIG_FILE.
