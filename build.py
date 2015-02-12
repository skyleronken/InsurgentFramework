#!/usr/bin/env python

import config
import sys
import os
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
import xml.etree.ElementTree as ET

def parse_module_types(xml, pkg):
    
    modules_list = [pkg]

    for e in xml.findall(config.MOD_T):
        type_e = e.find(config.MOD_TYPE_T)
        modules_list.append(pkg + '.' + type_e.text)
    
    return modules_list

def main():
    
    ########################
    # Parse Arguments here #
    ########################
    
    framework_location = "/home/ubuntu/workspace/"
    base_location = framework_location + "base.py"
    settings_file_name = "settings.xml"
    settings_file = framework_location + settings_file_name
    hooks_dir = list()
    hooks_dir.append(framework_location + "hooks")
    
    working_dirs = list()
    working_dirs.append("/tmp/")
    project_name = "testbot"
    
    debug = "False"
    strip = "None"
    upx = "True"
    console = "True"
    
    #######################################
    # Parse settings for required modules #
    #######################################
    
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
    
    modules_to_import = beacon_types + decoder_types + command_types + encoder_types + responder_types
    modules_to_import = modules_to_import + [config.BEACON_ABC, config.COMMAND_ABC, config.DECODER_ABC, config.ENCODER_ABC, config.RESPONDR_ABC]
    modules_to_import = list(set(modules_to_import)) # remove duplicates
    hidden_imports = str(modules_to_import)
    
    for pkg in (config.BEACON_PKG, config.DECODER_PKG, config.ENCODER_PKG, config.COMMAND_PKG, config.RESPONDER_PKG):
        working_dirs.append(framework_location + pkg.replace(".",os.path.sep))
    
    working_dirs = list(set(working_dirs)) #remove dupes
    working_dirs = str(working_dirs)
    
    ##################
    # Make Spec File #
    ##################
    
    spec_file = NamedTemporaryFile(suffix=".spec",delete=False)
    
    spec_file.write("# -*- mode: python -*-%s" % os.linesep)
    spec_file.write("a = Analysis(['%s'],pathex=%s,hiddenimports=%s,hookspath=%s,runtime_hooks=None)%s" % (base_location,working_dirs,hidden_imports,hooks_dir,os.linesep))
    spec_file.write("a.datas += [('%s','%s','DATA')]%s" % (settings_file_name, settings_file, os.linesep))
    spec_file.write("pyz = PYZ(a.pure)%s" % os.linesep)
    spec_file.write("exe = EXE(pyz,a.scripts,a.binaries,a.zipfiles,a.datas,name='%s',debug=%s,strip=%s,upx=%s,console=%s)" % (project_name, debug, strip, upx, console))
    
    spec_file.flush()
    spec_file.seek(0)
    
    #print spec_file.name
    #print spec_file.read()
    
    spec_file.close()

    ####################
    # Build Executable #
    ####################

    make_cmd_line = []
    make_cmd_line.append("pyinstaller")
    make_cmd_line.append(spec_file.name)
    
    results = Popen(make_cmd_line, stdout=PIPE).communicate()[0]
    

    #################
    # Cleanup Build #
    #################
    os.remove(spec_file.name)


if __name__ == "__main__":
    main()