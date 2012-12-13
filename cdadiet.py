#!/usr/bin/env python

# Copyright 2012 George Lilly (glilly at glilly dot net)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import problems
import medications
import cdautil
import xml.etree.ElementTree as ET
from rdflib import Literal, BNode, Namespace
from rdflib import RDF
import rdflib
#from rdflib.URIRef import URIRef
#from rdflib.constants import TYPE, VALUE

# Import RDFLib's default TripleStore implementation
#from rdflib.TripleStore import TripleStore

#store = TripleStore(  )
g = rdflib.Graph()
g.bind("dcterms","http://purl.org/dc/terms/")
g.bind("rdf","http://www.w3.org/1999/02/22-rdf-syntax-ns#")
g.bind("sp","http://smartplatforms.org/terms#")
g.bind("smart","http://sandbox-api.smartplatforms.org/records/")
g.bind("snomed","http://purl.bioontology.org/ontology/SNOMEDCT/")
g.bind("ccd","http://this.ccd.com/")

def tree(node, prefix='|--'):
    txt=('' if (node.text is None) or (len(node.text) == 0) else node.text);
    txt2 = txt.replace('\n','');
    print prefix+cdautil.clean(node.tag)+'  '+txt2;
    for att in node.attrib:
        print prefix+'  : '+cdautil.clean2(att)+'^'+node.attrib[att];
    for child in node:
        tree(child,'|  '+prefix );

def show(toc,what):
    print what;
    tree(toc[what])
    return

def listtoc(toc):
    print "toc";
    for g in sorted(toc.iterkeys()):
        print g,toc[g];
    return

# i couldn't get this bit to work... i think we should replace it with classes
# ... but i don't know how classes work in python yet... some help would be
# appreciated... gpl
# 
derive = {
    'problems': problems.derive_problems
}

yield_smart = {
    'problems': problems.smart_problems
}

def derive(section):
    return derive[section]


def yield_smart(section):
    x=yield_smart[section]
    return x(toc)
# end failed experiment...
#

def init():
    dom = ET.parse('gpl2.xml')
    root = dom.getroot()
    toc = cdautil.sections(root)
    problems.derive_problems(toc)
    medications.derive_medications(toc)
#    x=yield_smart('problems')
#    s=x()
    return (dom, root, toc)

if __name__ == '__main__':
    dom = ET.parse('gpl2.xml')
    root = dom.getroot()
#    tree(root);
    toc=cdautil.sections(root);
#    print;
#    listtoc(toc);
#    print ;
#    show(toc,'problem-1')
    problems.derive_problems(toc)
    medications.derive_medications(toc)
#    listtoc(toc)
#    g.prefix_mapping("ccd","https:this.ccd.com/patient888999/records/")
    gr=problems.smart_problems(toc)
    outn3=gr.serialize(format='n3')
    print outn3;
    gr=medications.smart_medications(toc)
    moutn3=gr.serialize(format='n3')
    print moutn3;
#    x=yield_smart['problems']
#    gr=x(toc)
#    for s,p,o in gr:
#        print ((s,p,o))
#    outnt=gr.serialize(format='nt')
#    print outnt;
#    out=gr.serialize(format='pretty-xml')
#    print out;
#    gg=rdflib.Graph()
#    gg.parse('gpl2.xml')
#    outgg=gg.serialize(format='turtle')
#    print outgg
#    outjson=gr.serialize(format='json') 
# oops did not have a serializer for json is there one?? how do i install it? gpl
#    print outjson;
