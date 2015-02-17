# Python Implant Framework
A framework for creating modular implants/bots to be used in training environments

<h4>Priorites</h4>
<ol>
<li>Modularity</li>
<li>Capability</li>
<li>Compatability</li>
<li>Portability</li>
<li>Forensically Sound</li>
</ol>

<h5>Todo</h5>
<ul>
<li> CommandObject - to_string method, to allow the building of CommandObjects manually and than transformed into a string for sending.
<li> Have results go back to the CommandObject, and the responses parsed from the CommandObject accordingly to be handed to the encoder.</li>
<li> Beahviors modules. i.e: What to do when no nodes can be contacted; chunking up response data; chunking responses to occur per command or per beacon;</li>
<li> Prevent replays </li>
<li> Add active day and active hour calculation to calculate_sleep()</li>
<li> Add a GUID for the bot type; defined in the settings xml</li>
<li> Get a GUID for the bot based off of MAC/IP/PC Name</li>
<li> Ability to alter content of packaged XML content for PERSISTENT changes from C2 node. (don't know if this is possible)</li>
<li> Create a tracking mechanism for threads started by commands from previous orders</li>
<li> Create a web GUI for building commands. Should intelligently knowh that command modules' requirements.</li>
<li> Add a server generating framework. Should be able to intelligently task bots, track respones, etc.</li>
<li> Add a transform method which allows the settings XML document to define the 'key' for commands and their KVP parameters. This will need to be a transform of the command handler that occurs AFTER the imports.</li>
<li> Wrap each node into a Node class upon initial import.</li>
<li> Fix easy_import and abstract_builder so you can hand it a list of the modules for a package (beacons, commands, etc), since the import can receive a list. More efficient.</li>
<li> more flexible designation of where to send the results/responses</li>
<li> make the sending of results/responses optional</li>
<li> make the results sending have an option of be dependant upon the command (i.e each command results can be sent somewhere different, or not at all, etc)</li>
</ul>

<h5>Milestones:</h5>
<i>
1/15/2015 - Dynamic Importer and beaconing handler verified
<br>
2/9/2015 - The controller works; albeit needs some documenting (DOCSTRINGS) and testing.
<br>
2/11/2015 - All configurations are now parsed from XML settings file.
<br>
2/12/2015 - Packing script (build.py) completed.
<br>
2/14/2015 - Created a translator for encoding C2 messages and decoding responses.
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
I had to modify pyinstaller to get it to recursively analyze dynamically imported modules' dependencies.<br><br>
If not building pyinstaller from their Git repo, make sure you make the change manually: <br>
https://github.com/pyinstaller/pyinstaller/commit/e9575e1145718ecc49625b782cee7cbb41d8522b

<h4>
Installation
</h4>

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
