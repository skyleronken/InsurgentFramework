#!/usr/bin/env python

import config
import sys
import os
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
import xml.etree.ElementTree as ET
from argparse import ArgumentParser

def parse_module_types(xml, pkg):
    """
    Parses the xml configuration to determine dynamic import modules
    """
    
    modules_list = [pkg]

    for e in xml.findall(config.MOD_T):
        type_e = e.find(config.MOD_TYPE_T)
        modules_list.append(pkg + '.' + type_e.text)
    
    return modules_list

def main(project_name, settings_file, framework_location, working_dir, debug):
    
    base_location = os.path.normpath(framework_location + os.path.sep + config.MODULE_PATH + os.path.sep + "base.py")
    
    #settings_file_name = settings_file.split(os.path.sep)[-1]
    settings_file_name = config.DEFAULT_CONFIG_FILE

    hooks_dir = list()
    hooks_dir.append(framework_location + os.path.sep + "hooks")
    
    working_dirs = list()
    working_dirs.append(working_dir)

    strip = "None"
    upx = "True"
    console = "True"

    #######################################
    # Parse settings for required modules #
    #######################################
    
    print "%s Parsing %s" % (config.PROMPT, settings_file)
    
    xmltree = ET.parse(settings_file)
    xmlroot = xmltree.getroot()
    xml = xmlroot.find(config.MODULES_TAG)
    
    beacon_types = parse_module_types(xml.find(config.BEACONS_MOD_T), config.BEACON_PKG)
    decoder_types = parse_module_types(xml.find(config.DECODERS_MOD_T), config.DECODER_PKG)
    command_types = parse_module_types(xml.find(config.COMMANDS_MOD_T), config.COMMAND_PKG)
    encoder_types = parse_module_types(xml.find(config.ENCODERS_MOD_T), config.ENCODER_PKG)
    responder_types = parse_module_types(xml.find(config.RESPONDERS_MOD_T), config.RESPONDER_PKG)
    
    ########################################
    # Build Hidden Imports for PyInstaller #
    ########################################
    
    print "%s Compiling hidden imports" % (config.PROMPT)
    
    modules_to_import = beacon_types + decoder_types + command_types + encoder_types + responder_types
    modules_to_import = modules_to_import + [config.COMMAND_PKG + "." + config.COMMAND_ABC
                                            , config.BEACON_PKG + "." + config.BEACON_ABC
                                            , config.DECODER_PKG + "." + config.DECODER_ABC
                                            , config.ENCODER_PKG + "." + config.ENCODER_ABC
                                            , config.RESPONDER_PKG + "." + config.RESPONDER_ABC]
    modules_to_import = list(set(modules_to_import)) # remove duplicates
    hidden_imports = str(modules_to_import)

    for pkg in (config.BEACON_PKG, config.DECODER_PKG, config.ENCODER_PKG, config.COMMAND_PKG, config.RESPONDER_PKG, config.MODULE_PATH):
        working_dirs.append(framework_location + os.path.sep +pkg.replace(".",os.path.sep))
    
    working_dirs = list(set(working_dirs)) #remove dupes
    working_dirs = str(working_dirs)
    
    runtime_opt = "('W ignore', None, 'OPTION')"

    ##################
    # Make Spec File #
    ##################
    
    print "%s Making .spec file" % (config.PROMPT)
    
    spec_file = NamedTemporaryFile(suffix=".spec",delete=False)
    
    spec_file.write("# -*- mode: python -*-%s" % os.linesep)
    spec_file.write("a = Analysis([%s],pathex=%s,hiddenimports=%s,hookspath=%s,runtime_hooks=None)%s" % (repr(base_location),working_dirs,hidden_imports,hooks_dir,os.linesep))
    spec_file.write("a.datas += [('%s','%s','DATA')]%s" % (settings_file_name, settings_file, os.linesep))
    spec_file.write("pyz = PYZ(a.pure)%s" % os.linesep)
    spec_file.write("exe = EXE(pyz,a.scripts,[%s],a.binaries,a.zipfiles,a.datas,name='%s',debug=%s,strip=%s,upx=%s,console=%s)" % (runtime_opt, project_name, debug, strip, upx, console))
    
    spec_file.flush()
    spec_file.seek(0)
    
    spec_file.close()

    ####################
    # Build Executable #
    ####################
    
    print "%s Building executable" % (config.PROMPT)

    make_cmd_line = []
    make_cmd_line.append("pyinstaller")
    make_cmd_line.append("--ascii")
    if debug:
        make_cmd_line.append("--log-level=DEBUG")
    else:
        make_cmd_line.append("--log-level=WARN")
    #make_cmd_line.append("--onedir")
    make_cmd_line.append(spec_file.name)
    
    results = Popen(make_cmd_line, stdout=PIPE).communicate()[0]
    

    #################
    # Cleanup Build #
    #################
    print "%s Cleaning up!" % (config.PROMPT)
    os.remove(spec_file.name)


if __name__ == "__main__":
    
    ap = ArgumentParser(prog='build',description='Build portable, modular bots')
    ap.add_argument('-w','--working_dir', dest='working_dir', nargs='?', default=os.path.dirname(os.path.realpath(__file__)), help='The location where you want your working file and output to be stored.')
    ap.add_argument('-l','--location', dest='framework_location',nargs='?', default=os.path.dirname(os.path.realpath(__file__)), help="The location of the framework's main directory.")
    ap.add_argument('-s','--settings', dest='settings_file',nargs='?', default='settings.xml', required=True, help="The absolute path of the settings XML file from which to create your bot.")
    ap.add_argument('-d','--debug', dest='debug', action='store_true', required=False, help="Verbose debug output.")
    ap.add_argument('name', help="The desired name of the bot.")
    parsed_args = ap.parse_args()
    main(parsed_args.name, parsed_args.settings_file, parsed_args.framework_location, parsed_args.working_dir, parsed_args.debug)