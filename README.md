# Python Implant Framework
A framework for creating modular implants to be used in training environments

<h4>Priorites</h4>
<ol>
<li>Modularity</li>
<li>Capability</li>
<li>Compatability</li>
<li>Portability</li>
<li>Forensically Sound</li>
</ol>

<h5>Ideas</h5>
<ul>
<li> Beahviors modules. i.e: What to do when no nodes can be contacted; chunking up response data; chunking responses to occur per command or per beacon;</li>
</ul>

<h6>Milestones:</h6>
<i>
1/15/2015 - Dynamic Importer and beaconing handler verified
<br>
2/9/2015 - The controller works; albeit needs some documenting (DOCSTRINGS) and testing.
<br>
2/11/2015 - All configurations are now parsed from XML settings file.
<br>
2/12/2015 - Packing script (build.py) completed.
</i>

<h5>
Dependencies
</h5>

<ul>
<li>Python 2.7</li>
<li>Pyinstaller</li>
</ul>

Other dependencies will be required by specific modules

<h6>Notes: </h6>
I had to modify pyinstaller to get it to recursively analyze dynamically imported modules' dependencies.<br>
If not building pyinstaller from their Git repo, make sure you make the change manually: <br>
https://github.com/pyinstaller/pyinstaller/commit/e9575e1145718ecc49625b782cee7cbb41d8522b

<h5>
Installation
</h5>

<h5>
Usage
</h5>

